// node tests/hw.test.mjs — 필기 습관 지도 로직 (팝업 노출·1달 숨김·5회 누적·학생 책임 이슈 골라내기)
const mem = new Map();
globalThis.localStorage = { getItem: (k) => (mem.has(k) ? mem.get(k) : null), setItem: (k, v) => mem.set(k, String(v)), removeItem: (k) => mem.delete(k) };
const smem = new Map();
globalThis.sessionStorage = { getItem: (k) => (smem.has(k) ? smem.get(k) : null), setItem: (k, v) => smem.set(k, String(v)), removeItem: (k) => smem.delete(k) };

const { hwIssuesOf, hwStrikes, addHwStrike, resetHwStrikes, muteHwGuide, hwMuted, hwGuideDue, markHwGuideShown, HW_ADVICE, HW_STRIKE_LIMIT } =
  await import("../src/lib/hw.js");

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; } else { fail++; console.log("FAIL -", name); } };

// 기본: 숨김 전이면 노출
ok(hwGuideDue() === true, "처음엔 팝업을 보여준다");
markHwGuideShown();
ok(hwGuideDue() === false, "알겠어요(세션 확인) 뒤에는 같은 세션에서 다시 안 띄움");
smem.clear();
ok(hwGuideDue() === true, "새 세션이면 다시 보여준다");

// 1달 숨김
muteHwGuide(30);
smem.clear();
ok(hwMuted() === true && hwGuideDue() === false, "한 달 보지 않기 동안은 숨김");

// 5회 누적이면 숨김 중이어도 재노출
for (let i = 0; i < HW_STRIKE_LIMIT; i++) addHwStrike();
ok(hwStrikes() === HW_STRIKE_LIMIT, "누적 카운트");
ok(hwGuideDue() === true, "5회 누적이면 숨김 중이어도 다시 띄운다");
resetHwStrikes();
ok(hwStrikes() === 0 && hwGuideDue() === false, "확인하면 카운트 리셋 · 다시 숨김 상태로");

// 학생 책임 이슈 골라내기
const scan = { legibility: { score: 4, issues: [
  { kind: "glyph", note: "7을 1처럼" },           // 학생 책임 아님(교정 대상 아님)
  { kind: "messy", note: "3~4번째 줄", box: { x: 0.1, y: 0.5, w: 0.8, h: 0.2 } },
  { kind: "two_column", note: "두 단" },
] } };
const hw = hwIssuesOf(scan);
ok(hw.length === 2 && hw.every((i) => HW_ADVICE[i.kind]), "messy·two_column 만 학생 책임으로 골라냄");
ok(hwIssuesOf({ legibility: { score: 2, issues: [] } })[0]?.kind === "messy", "이슈가 없어도 판독 점수 1~2점이면 messy 취급");
ok(hwIssuesOf({ legibility: { score: 4, issues: [] } }).length === 0, "깨끗하면 빈 배열");
ok(["messy", "faint", "scribble", "two_column"].every((k) => HW_ADVICE[k]?.tip), "네 종류 모두 지도 문구가 있다");
ok(HW_ADVICE.two_column.tip.includes("화살표"), "두 단 지도 문구는 화살표를 종용한다");

console.log(`${pass}/${pass + fail} passed`);
if (fail) process.exit(1);
