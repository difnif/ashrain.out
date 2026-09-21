// 백그라운드 판독 잡 — 판독·채점·검사를 화면이 아니라 앱 전역에서 돌린다 (사용자 확정 2026-09-21).
// 화면을 떠나도(뒤로가기·다른 탭) 작업은 계속되고, 결과는 run() 안에서 기기 보관소에 저장되므로 유실되지 않는다.
// 끝나면: 화면에 있으면 그 화면이, 아니면 토스트(셸)와 브라우저 알림 + 기록 탭 뱃지.
// 브라우저 창을 완전히 닫으면 중단된다(서버에 아무것도 저장하지 않는 원칙 때문) — UI 문구가 이를 알린다.

let seq = 0;
const jobs = new Map();
const emit = () => { try { window.dispatchEvent(new Event("ash:jobs")); } catch { /* 무시 */ } };

export const listJobs = () => [...jobs.values()].sort((a, b) => b.at - a.at);
export const getJob = (id) => jobs.get(id) || null;
export const runningJobs = () => listJobs().filter((j) => j.status === "running");
export const unseenJobs = () => listJobs().filter((j) => j.status !== "running" && !j.seen);

/**
 * 잡 시작. run(signal, setProgress) 은 결과 저장(saveDevice)까지 스스로 끝내야 한다.
 * 반환: job — { id, title, status(running|done|error|canceled), progress, promise, ... }
 */
export function startJob({ kind, title, run }) {
  const id = `${++seq}-${Date.now().toString(36)}`;
  const ctrl = new AbortController();
  const job = { id, kind, title, status: "running", at: Date.now(), ctrl, progress: null, result: null, error: null, seen: false };
  job.promise = (async () => {
    try {
      const r = await run(ctrl.signal, (p) => { job.progress = p; emit(); });
      job.status = ctrl.signal.aborted ? "canceled" : "done";
      job.result = r;
    } catch (e) {
      job.status = ctrl.signal.aborted ? "canceled" : "error";
      job.error = String(e?.message || e || "실패");
    }
    emit();
    if (job.status === "done") notifyDone(`${title} — 끝났어요`, "결과는 기록 탭에 있어요.");
    else if (job.status === "error") notifyDone(`${title} — 잘 되지 않았어요`, job.error);
    return job.result;
  })();
  jobs.set(id, job);
  emit();
  return job;
}

export function cancelJob(id) {
  const j = jobs.get(id);
  if (j && j.status === "running") { try { j.ctrl.abort(); } catch { /* 무시 */ } }
}
export function markJobsSeen() { let dirty = false; for (const j of jobs.values()) if (j.status !== "running" && !j.seen) { j.seen = true; dirty = true; } if (dirty) emit(); }

/** iOS·안드로이드 공통 — 자리 비우기 전에 알림 권한을 한 번 청해 둔다(제스처 안에서만 유효) */
export function askNotifyPermission() {
  try {
    if ("Notification" in window && Notification.permission === "default") Notification.requestPermission().catch(() => {});
  } catch { /* 무시 */ }
}

function notifyDone(title, body) {
  try {
    if ("Notification" in window && Notification.permission === "granted" && document.visibilityState !== "visible") {
      new Notification(title, { body, icon: "/brand/well/base.webp", tag: "ash-photo-job" });
    }
  } catch { /* 무시 */ }
  try { window.dispatchEvent(new CustomEvent("ash:job-toast", { detail: { title, body } })); } catch { /* 무시 */ }
}
