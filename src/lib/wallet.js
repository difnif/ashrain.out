// 지갑 — Ⓟ Ash · Ⓓ Drop 잔액/내역 (api/points.js)
// Ⓟ = 유료 학습 기능(AI 한도 초과분)에 쓰는 재화, 충전은 쿠폰·관리자 지급 · Ⓓ = 학습 활동 보상(복습 완수), 추후 숍. 교환 불가.
import { api } from "./authx";

export const CURRENCY = {
  ash: { sym: "Ⓟ", name: "Ash", label: "Ash 포인트", desc: "무료 한도를 다 쓴 뒤 AI 힌트·채점에 쓰여요. 충전은 쿠폰이나 선생님 지급으로만." },
  drop: { sym: "Ⓓ", name: "Drop", label: "Drop 포인트", desc: "개념 복습을 완수하면 쌓여요. 나중에 숍에서 스킨·테마와 바꿀 수 있어요." },
};

export const REASON_LABEL = {
  coupon: "쿠폰 충전",
  admin_grant: "선생님 지급",
  "spend:hint": "힌트 사용",
  "spend:find": "AI 개념찾기",
  "spend:omr": "OMR 인식",
  "spend:ask": "AI 질문",
  adjust: "조정",
};

export function reasonLabel(reason) {
  if (!reason) return "";
  if (REASON_LABEL[reason]) return REASON_LABEL[reason];
  if (reason.startsWith("review:")) return "개념 복습 완수";
  if (reason.startsWith("spend:")) return reason.slice(6) + " 사용";
  return reason;
}

export const fmtPts = (n, cur = "ash") => `${CURRENCY[cur]?.sym || ""} ${Number(n || 0).toLocaleString()}`;

/** { ash, drop, ready } — 실패 시 null */
export async function getBalances() {
  try {
    const r = await api("points", { action: "balance" }, { auth: true });
    return { ash: r.ash ?? r.balance ?? 0, drop: r.drop ?? 0, ready: r.ready !== false };
  } catch { return null; }
}

export async function getHistory({ limit = 20, currency } = {}) {
  const r = await api("points", { action: "history", limit, currency }, { auth: true });
  return r.rows || [];
}

/** 적립·차감이 일어났을 때 화면들이 잔액을 다시 읽도록 알린다 */
export function notifyPoints(detail) {
  try { window.dispatchEvent(new CustomEvent("ash:points", { detail })); } catch {}
}
export function onPoints(handler) {
  const h = (e) => handler(e.detail || {});
  window.addEventListener("ash:points", h);
  return () => window.removeEventListener("ash:points", h);
}
