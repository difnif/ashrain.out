// 필기 습관 지도 — 학생 책임의 판독 문제(글씨 엉망·연함·끄적임·두 단)를 짚고 고치게 한다 (사용자 확정 2026-09-21).
// 촬영 전 주의 팝업: 기본 노출, "한 달 보지 않기" 가능. 필기 문제 5회 누적이면 다시 노출.
// 카운트·숨김은 이 기기(localStorage)에만 — 서버로 가지 않는다.

export const HW_STRIKE_LIMIT = 5;
const K_MUTE = "ash.hw.muteUntil";
const K_STRIKES = "ash.hw.strikes";

const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, String(v)); } catch { /* 무시 */ } },
};

/** 학생 책임 필기 문제 종류와 지도 문구 */
export const HW_ADVICE = {
  messy: { nm: "글씨가 엉망", tip: "이 부분은 또박또박 다시 적어 주세요. 채점 선생님(그리고 AI)도 이 글씨를 읽어야 해요." },
  faint: { nm: "글씨가 너무 연함", tip: "이 부분은 더 진하게 다시 적어 주세요. 연필을 조금만 꾹 눌러도 판독이 훨씬 좋아져요." },
  scribble: { nm: "끄적임 — 흐름을 알아보기 어려움", tip: "위에서 아래로 한 줄기로 다시 정리해 주세요. 흐름이 보여야 어디서 틀렸는지도 찾을 수 있어요." },
  two_column: { nm: "두 단으로 나뉜 풀이", tip: "한 단으로 이어 쓰는 게 가장 좋아요. 부득이 두 단이 되면 첫 단 끝과 둘째 단 시작 사이에 화살표를 그어 주세요." },
};

/** 답안 전사 결과에서 학생 책임 필기 문제만 골라낸다 (판독 점수 1~2점이면 messy 로 간주) */
export function hwIssuesOf(scan) {
  const list = (scan?.legibility?.issues || []).filter((i) => HW_ADVICE[i.kind]);
  if (!list.length && (scan?.legibility?.score || 3) <= 2) {
    return [{ kind: "messy", note: "전체적으로 판독이 어려워요", box: null }];
  }
  return list;
}

export function hwStrikes() { const n = parseInt(store.get(K_STRIKES) || "0", 10); return Number.isFinite(n) ? n : 0; }
export function addHwStrike(n = 1) { store.set(K_STRIKES, hwStrikes() + n); }
export function resetHwStrikes() { store.set(K_STRIKES, 0); }
export function muteHwGuide(days = 30) { store.set(K_MUTE, Date.now() + days * 86400000); }
export function hwMuted() { const t = parseInt(store.get(K_MUTE) || "0", 10); return Number.isFinite(t) && Date.now() < t; }

const K_SEEN = "ash.hw.seen";       // 세션당 1회 — "알겠어요"를 눌렀으면 같은 접속에서는 다시 안 띄운다
function seenThisSession() { try { return sessionStorage.getItem(K_SEEN) === "1"; } catch { return false; } }
export function markHwGuideShown() { try { sessionStorage.setItem(K_SEEN, "1"); } catch { /* 무시 */ } }

/** 촬영 전 주의 팝업을 지금 보여야 하나 — 누적 5회면 숨김·세션과 무관하게 다시 */
export function hwGuideDue() { return hwStrikes() >= HW_STRIKE_LIMIT || (!hwMuted() && !seenThisSession()); }
