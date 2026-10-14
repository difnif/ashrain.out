// ashrain.out — 서술형 평가 쪽 분석 대기열: 찍기와 분석을 떼어 놓는다(다음 쪽을 찍는 동안 앞 쪽이 판독·채점된다).
// 모듈 상태라 화면을 떠나도(앱 안 이동) 계속된다. 브라우저를 닫으면 멈춘다 — 끝난 쪽은 서버에 있으니 다시 열면 이어서 찍는다.
// 사진 한 장 = shot id. 같은 사진을 다시 보내면(응답이 끊긴 뒤 재시도) 서버가 알아보고 AI 를 다시 부르지 않는다.
// 서버가 "읽는 중/채점 중(busy)"이라고 하면 잠깐 기다렸다 다시 묻는다. 제출 전에는 점수를 받지 않는다(상태만).
import { assessCall } from "./api.js";

const CONCURRENCY = 2;
const BUSY_WAIT_MS = 6000;
const BUSY_MAX = 14;                 // 6초 × 14 ≈ 84초 — 서버의 '멈춤' 기준(70초)을 넘겨 기다린다
const state = { ctx: null, jobs: new Map(), active: 0 };
const emit = () => { try { window.dispatchEvent(new Event("ash:assess")); } catch { /* */ } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
export function newShot() {
  try { return crypto.randomUUID(); } catch { return `s${Date.now().toString(36)}${Math.random().toString(36).slice(2, 12)}`; }
}

/** 응시 맥락 { code, sid, secret } — 다른 응시로 바뀌면 대기열을 비운다 */
export function setQueueContext(ctx) {
  if (!ctx?.sid) return;
  if (!state.ctx || state.ctx.sid !== ctx.sid) state.jobs.clear();
  state.ctx = { ...ctx };
  emit();
}
export const queueContext = () => state.ctx;
export const jobsList = () => [...state.jobs.values()].sort((a, b) => a.page - b.page);
export const jobOf = (page) => state.jobs.get(page) || null;
export const busyCount = () => jobsList().filter((j) => ["queued", "sending", "grading"].includes(j.status)).length;

/** 쪽 하나 넣기. payload: { crop, image, quality } — 같은 쪽이 다시 들어오면 새 사진(새 shot)으로 바꾼다 */
export function enqueue(page, kind, payload, thumb = null) {
  const prev = state.jobs.get(page);
  if (prev && ["sending", "grading"].includes(prev.status)) prev.stale = true;    // 진행 중인 옛 사진 결과는 버린다
  state.jobs.set(page, { page, kind, status: "queued", payload: { ...payload, shot: newShot() }, thumb, result: null, error: null, tries: 0, at: Date.now(), seq: (prev?.seq || 0) + 1 });
  emit();
  pump();
}

/** 실패한 쪽 다시 보내기 — 같은 사진(같은 shot)이라 서버가 이어서 처리한다 */
export function retryJob(page) {
  const j = state.jobs.get(page);
  if (j?.status === "error" && j.gradeOnly) { j.gradeOnly = false; regrade(page); return true; }
  if (!j || !j.payload || !["error"].includes(j.status)) return false;
  j.status = "queued"; j.error = null; j.tries = 0;
  emit(); pump();
  return true;
}

/** 채점만 다시(판독은 됐는데 채점이 안 된 쪽) */
export function regrade(page) {
  const j = state.jobs.get(page);
  if (!j) { state.jobs.set(page, { page, kind: "item", status: "grading", payload: null, result: null, error: null, tries: 0, at: Date.now(), seq: 1 }); }
  else { j.status = "grading"; j.error = null; }
  emit();
  runGrade(state.jobs.get(page));
}

function pump() {
  while (state.active < CONCURRENCY) {
    const next = jobsList().find((j) => j.status === "queued");
    if (!next) return;
    run(next);
  }
}

const transient = (e) => !e?.status || e.status >= 500 || e.status === 0;
const isBusy = (e) => e?.status === 409 && e?.extra?.busy;
const isSuperseded = (e) => e?.status === 409 && e?.extra?.superseded;

/** 서버 호출 — 잠깐 끊김(5xx·네트워크)은 2번까지, busy 는 기다렸다가 다시 */
async function patient(fn, job, seq) {
  let tries = 0, waits = 0;
  for (;;) {
    try { return await fn(); } catch (e) {
      if (state.jobs.get(job.page)?.seq !== seq) throw e;
      if (isBusy(e) && waits < BUSY_MAX) { waits++; await sleep(BUSY_WAIT_MS); continue; }
      tries++;
      if (transient(e) && tries <= 2) { await sleep(tries * 2500); continue; }
      throw e;
    }
  }
}

async function run(job) {
  const ctx = state.ctx;
  if (!ctx) return;
  const seq = job.seq;
  job.status = "sending"; state.active++; emit();
  try {
    const res = await patient(() => assessCall("page", { sid: ctx.sid, secret: ctx.secret, page_no: job.page, ...job.payload }), job, seq);
    if (state.jobs.get(job.page)?.seq !== seq) return;        // 그새 다시 찍었다
    job.result = res;
    if (res.kind === "item" && res.status === "read") {
      job.status = "grading"; emit();
      await runGrade(job, true);
    } else {
      job.status = "done";
      job.payload = null;                                         // 끝난 쪽 사진은 메모리에서 비운다
    }
  } catch (e) {
    if (state.jobs.get(job.page)?.seq === seq) {
      job.status = "error";
      job.error = isSuperseded(e) ? "다른 화면에서 이 쪽을 다시 찍었어요 — 여기서 다시 찍어 주세요" : e?.message || "실패";
      job.errStatus = e?.status || 0;
      if (isSuperseded(e)) job.payload = null;
    }
  } finally {
    state.active--; emit(); pump();
  }
}

async function runGrade(job, inner = false) {
  const ctx = state.ctx;
  if (!ctx || !job) return;
  const seq = job.seq;
  try {
    await patient(() => assessCall("grade", { sid: ctx.sid, secret: ctx.secret, page_no: job.page }), job, seq);
    if (state.jobs.get(job.page)?.seq !== seq) return;
    job.result = { ...(job.result || {}), kind: "item", status: "graded" };
    job.status = "done"; job.payload = null; job.error = null;
  } catch (e) {
    if (state.jobs.get(job.page)?.seq === seq) { job.status = "error"; job.error = e?.message || "채점 실패"; job.errStatus = e?.status || 0; job.gradeOnly = !isSuperseded(e); }
  }
  if (!inner) emit();
}
