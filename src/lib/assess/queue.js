// ashrain.out — 서술형 평가 쪽 분석 대기열: 찍기와 분석을 떼어 놓는다(다음 쪽을 찍는 동안 앞 쪽이 판독·채점된다).
// 모듈 상태라 화면을 떠나도(앱 안 이동) 계속된다. 브라우저를 닫으면 멈춘다 — 끝난 쪽은 서버에 있으니 다시 열면 이어서 찍는다.
import { assessCall } from "./api.js";

const CONCURRENCY = 2;
const state = { ctx: null, jobs: new Map(), active: 0 };
const emit = () => { try { window.dispatchEvent(new Event("ash:assess")); } catch { /* */ } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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

/** 쪽 하나 넣기. payload: { crop, image, quality } — 같은 쪽이 다시 들어오면 새 사진으로 바꾼다 */
export function enqueue(page, kind, payload, thumb = null) {
  const prev = state.jobs.get(page);
  if (prev && ["sending", "grading"].includes(prev.status)) prev.stale = true;    // 진행 중인 옛 사진 결과는 버린다
  state.jobs.set(page, { page, kind, status: "queued", payload, thumb, result: null, error: null, tries: 0, at: Date.now(), seq: (prev?.seq || 0) + 1 });
  emit();
  pump();
}

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

async function run(job) {
  const ctx = state.ctx;
  if (!ctx) return;
  const seq = job.seq;
  job.status = "sending"; state.active++; emit();
  try {
    let res = null;
    for (;;) {
      try {
        res = await assessCall("page", { sid: ctx.sid, secret: ctx.secret, page_no: job.page, ...job.payload });
        break;
      } catch (e) {
        job.tries++;
        if (transient(e) && job.tries <= 2) { await sleep(job.tries * 2500); continue; }
        throw e;
      }
    }
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
    if (state.jobs.get(job.page)?.seq === seq) { job.status = "error"; job.error = e?.message || "실패"; job.errStatus = e?.status || 0; }
  } finally {
    state.active--; emit(); pump();
  }
}

async function runGrade(job, inner = false) {
  const ctx = state.ctx;
  if (!ctx || !job) return;
  const seq = job.seq;
  let tries = 0;
  for (;;) {
    try {
      const g = await assessCall("grade", { sid: ctx.sid, secret: ctx.secret, page_no: job.page });
      if (state.jobs.get(job.page)?.seq !== seq) return;
      job.result = { ...(job.result || {}), kind: "item", status: "graded", grade: g.grade };
      job.status = "done"; job.payload = null; job.error = null;
      break;
    } catch (e) {
      tries++;
      if (transient(e) && tries <= 2) { await sleep(tries * 2500); continue; }
      if (state.jobs.get(job.page)?.seq === seq) { job.status = "error"; job.error = e?.message || "채점 실패"; job.errStatus = e?.status || 0; job.gradeOnly = true; }
      break;
    }
  }
  if (!inner) emit();
}
