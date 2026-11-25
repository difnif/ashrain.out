// 시록고 · 격언 도우미 — PRZ-1 정식 코드 한 줄 → 고르기에 쓰는 달 기록
// 코드 형식: 프로젝트 ME-수학 교육의 claude/SPEC-프리즘코드-PRZ1-코드북-v1.md
//   PRZ1 러비·초5 2609#10 │ 1125↓30 │ P1 │ 87F0·121300 │ 900401000 │ 000000663 │ 100000000 │ Σ023
//   ①②③ 이름·학년 YYMM#순번 │ ④ 입사광(정답률·학습량·난이도·기복 밴드, 방향, 이달 비율 밴드, 집계 누락) │ ⑤ 관측(관측자·새로 봄)
//   │ ⑥ 프리즘 │ ⑦ 스펙트럼 S(16진 9자리, 한 칸 = 1/15) │ ⑧ D │ ⑨ ◆ │ ⑩ Σ(누적 문항 ÷ 100)
// 같은 코드면 같은 달 기록이 된다. 정답률 밴드는 읽지만 고르는 데 쓰지 않는다(방향만 '오른 달 덤'에 씀).
import { TYPES, dominantType } from "./gyPick.js";

const WHO = { P: "P", O: "O", A: "AI", E: "E" };
const ARROW = { "↑": 1, "↓": -1, "→": 0, "○": 0 };
const HEAD = /^PRZ1\s+([^\s·]+)·(\S+)\s+(\d{2})(\d{2})#(\d{1,3})$/u;
const INC = /^([0-9-])([0-9-])([0-9-])([0-5])([↑↓→○])([1-5])([01])$/u;

/** 코드 한 줄 → 달 기록. 읽을 수 없으면 { error } */
export function parseCodeLine(line) {
  const raw = String(line || "").trim();
  const parts = raw.split("│").map((s) => s.trim());
  if (parts.length !== 8) return { error: "칸이 8개가 아니에요(│로 나눈 구역)" };
  const h = parts[0].match(HEAD);
  if (!h) return { error: "머리(PRZ1 이름·학년 YYMM#순번)를 못 읽었어요" };
  const inc = parts[1].match(INC);
  if (!inc) return { error: "입사광 7자리를 못 읽었어요" };
  const ob = parts[2].match(/^([POAE])([01])$/);
  if (!ob) return { error: "관측 2자리를 못 읽었어요" };
  if (!/^[0-9A-F]{9}$/i.test(parts[4])) return { error: "스펙트럼 9자리를 못 읽었어요" };
  const sig = parts[7].match(/^Σ(\d{1,4})$/);
  if (!sig) return { error: "누적(Σ)을 못 읽었어요" };

  const [, short, grade, yy, mm, nn] = h;
  const digits = [...parts[4]].map((c) => parseInt(c, 16));
  const S = {};
  TYPES.forEach((k, j) => { S[k] = digits[j] / 15; });
  const type = dominantType(S);   // 그달 주 유형(동점·미분화 222222222면 null) — 화면에 보이는 값, 고르기도 S에서 같은 값을 쓴다
  return {
    short, grade, code: raw,
    label: `20${yy}.${Number(mm)}`, nth: Number(nn),
    who: WHO[ob[1]], seen: ob[2] === "1",
    S, type, dacc: ARROW[inc[5]], R: Number(inc[6]), vb: Number(inc[4]), gap: inc[7] === "1",
    cum: Number(sig[1]) * 100,
  };
}

/** 붙여 넣은 글 → 학생별 달 기록(순번 차례). 학생은 머리의 이름으로 나눈다 */
export function monthsFromCodes(text) {
  const groups = new Map(), errors = [];
  String(text || "").split(/\r?\n/).forEach((line, i) => {
    if (!line.trim() || !line.includes("│")) return;
    const m = parseCodeLine(line);
    if (m.error) { errors.push({ line: i + 1, error: m.error }); return; }
    if (!groups.has(m.short)) groups.set(m.short, new Map());
    groups.get(m.short).set(m.nth, m);                     // 같은 순번이 두 번이면 나중 줄
  });
  const students = [...groups].map(([short, byNth]) => {
    const months = [...byNth.values()].sort((a, b) => a.nth - b.nth);
    // 첫 줄이 첫 달이 아니면 그 앞 누적을 모른다 → 그 줄에서는 누적 사건이 터지지 않게 앞 누적 = 지금 누적
    months.forEach((m, j) => { m.prevCum = j === 0 ? (m.nth === 1 ? 0 : m.cum) : months[j - 1].cum; });
    const gaps = months.some((m, j) => j > 0 && m.nth !== months[j - 1].nth + 1);
    return { short, grade: months[months.length - 1].grade, months, fromFirst: months[0].nth === 1, gaps };
  });
  return { students, errors };
}
