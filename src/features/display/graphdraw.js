// ashrain.out — 교실 모니터 「일차함수 그래프 그리기 해설」 계산 (graphdraw.js) — JSX 없음
// 문항(graphdraw-items.js)마다 박자표를 만든다: 풀이 순서 ①②③④를 차례로 형광펜 → 네모 칸에 답이 채워짐 → 그 줄이 하는 일을
// 좌표평면에 그린다(점 찍기 · 기울기만큼 가로로 세며 옮기고 세로로 세며 옮기기 · 두 점을 지나는 직선). 끝나면 정답 직선의 식.
// 그리기는 frames/graphdraw.jsx. 수는 모두 분수로 계산한다(분모 2·3·4·5) — 검산: tests/display-graph.test.mjs
import { GD_BASIC, GD_HARD } from "./graphdraw-items.js";

export const GD_SETS = {
  basic: { key: "basic", name: "기본", items: GD_BASIC },
  hard: { key: "hard", name: "심화", items: GD_HARD },
};
export const GD_SPEEDS = [1, 1.5];

export const GD_KIND = {
  "식": "식", "기울기y절편": "기울기 · y절편", "두절편": "x절편 · y절편", "두점": "두 점", "기울기한점": "기울기 · 한 점",
  "평행y절편": "평행", "평행한점": "평행", "평행": "평행 (일차방정식)", "증가량": "증가량", "방정식": "일차방정식",
};

/* ══════════ 박자 (1배속 ms) ══════════ */
// 해설 규격: 기본은 느리게(예전 속도 = 1.5×). 칸 세기는 한 칸에 0.42초.
export const GD = {
  INTRO: 1100,   // 문제를 읽는 틈
  LEAD: 650,     // 형광펜이 그 줄로
  FILL: 900,     // 네모 칸에 답이 써짐
  READ: 900,     // 그림 없는 줄(식 정리 · 기울기 계산)을 읽는 틈
  GAP: 260,
  DOT: 1300,     // 점: 찍힘(500) · 좌표(450) · 쉼
  CELL: 420,     // 한 칸 세기
  MVPAD: 320,
  LINE: 1700,    // 직선이 두 점 사이에서 양쪽으로 뻗음
  REST: 800,
  ANS: 700,
  HOLD: 5200,    // 다 그린 그림을 보여 주는 시간
};

/* ══════════ 수 ══════════ */
export const M = "−";
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
export function q(s) {
  const t = String(s).replace(M, "-").split("/");
  let n = parseInt(t[0], 10), d = t.length > 1 ? parseInt(t[1], 10) : 1;
  if (d < 0) { n = -n; d = -d; }
  const g = gcd(n, d);
  return { n: n / g, d: d / g };
}
export const qv = (x) => x.n / x.d;
export const qeq = (a, b) => a.n === b.n && a.d === b.d;
export const qadd = (a, b) => q(`${a.n * b.d + b.n * a.d}/${a.d * b.d}`);
export const qmul = (a, b) => q(`${a.n * b.n}/${a.d * b.d}`);
export const qneg = (a) => ({ n: -a.n, d: a.d });
/** 화면 글자: −3 · 3/4 · −5/2 */
export function qstr(x) {
  const s = x.n < 0 ? M : "", a = Math.abs(x.n);
  return s + (x.d === 1 ? String(a) : `${a}/${x.d}`);
}
export const ptStr = (P) => `(${qstr(P[0])}, ${qstr(P[1])})`;
/** 정답 직선 y = mx + b 의 글자 (분수 계수는 괄호: y = (3/4)x − 3) */
export function linStr(m, b) {
  let c;
  if (m.n === m.d) c = "x";
  else if (m.n === -m.d) c = M + "x";
  else if (m.d === 1) c = `${qstr(m)}x`;
  else c = (m.n < 0 ? M : "") + `(${Math.abs(m.n)}/${m.d})x`;
  let s = "y = " + c;
  if (b.n > 0) s += " + " + qstr(b);
  if (b.n < 0) s += ` ${M} ` + qstr(qneg(b));
  return s;
}

/* ══════════ 수식 글자 ══════════ */
/** 발문·풀이 글자를 MText 문법으로: (3/4) · 3/4 → {3/4}, (y 증가량)/(x 증가량) → 세로 분수 */
export function toM(s) {
  return String(s)
    .replace(/\(y 증가량\)\/\(x 증가량\)/g, "{y의 증가량/x의 증가량}")
    .replace(/\((\d+)\/(\d+)\)/g, "{$1/$2}")
    .replace(/(\d+)\/(\d+)/g, "{$1/$2}");
}

/* ══════════ 풀이 줄 → 조각(글자 · 네모 칸) ══════════ */
// 프린트와 같은 자리를 네모 칸으로: 수 · 분수 · 방향(오른쪽 · 왼쪽 · 위 · 아래) · 좌표의 두 수 · 「y에 대해 풀면」의 식 전체.
// 조각: { t: "txt", s } | { t: "box", v, k: "num" | "dir" | "eq" } — glue 가 참이면 앞 조각과 붙여 둔다(줄을 바꾸지 않는다).
const TOK = /(오른쪽|왼쪽|위|아래)|(−?\(\d+\/\d+\)|−?\d+\/\d+|−?\d+)/g;
const COORD = /\((−?\d+(?:\/\d+)?), (−?\d+(?:\/\d+)?)\)/g;

const SLOPE = "(y 증가량)/(x 증가량)";   // 세로 분수 하나 — 쪼개지 않는다
function pushText(out, s) {
  if (!s) return;
  const words = s.split(/(?<= )/).reduce((acc, w) => {   // 띄어쓰기 뒤에서 자른다(띄어쓰기는 앞 낱말에 붙는다)
    const last = acc[acc.length - 1];
    if (last != null && SLOPE.startsWith(last) && last !== SLOPE && (last + w).length <= SLOPE.length + 1) acc[acc.length - 1] = last + w;
    else acc.push(w);
    return acc;
  }, []);
  words.forEach((w, i) => {
    if (!w) return;
    const glue = i === 0 && !s.startsWith(" ") && out.length > 0;
    out.push({ t: "txt", s: w, glue });
  });
}
function plain(out, s) {
  let pos = 0;
  for (const m of s.matchAll(TOK)) {
    pushText(out, s.slice(pos, m.index));
    const glue = m.index > 0 && s[m.index - 1] !== " " && out.length > 0;
    out.push({ t: "box", v: m[0].replace(/^(−?)\((\d+\/\d+)\)$/, "$1$2"), k: m[1] ? "dir" : "num", glue });
    pos = m.index + m[0].length;
  }
  pushText(out, s.slice(pos));
}
export function stepAtoms(text) {
  const out = [];
  const HEAD = "y에 대해 풀면 y = ";
  if (text.startsWith(HEAD)) {
    const body = text.slice(HEAD.length), i = body.indexOf(" → ");
    pushText(out, "y에 대해 풀면 ");
    out.push({ t: "txt", s: "y = ", glue: false });
    out.push({ t: "box", v: i < 0 ? body : body.slice(0, i), k: "eq", glue: true });
    if (i >= 0) plain(out, body.slice(i));
    return out;
  }
  let pos = 0;
  for (const m of text.matchAll(COORD)) {
    plain(out, text.slice(pos, m.index));
    const glue0 = m.index > 0 && text[m.index - 1] !== " " && out.length > 0;
    out.push({ t: "txt", s: "(", glue: glue0 });
    out.push({ t: "box", v: m[1], k: "num", glue: true });
    out.push({ t: "txt", s: ", ", glue: true });
    out.push({ t: "box", v: m[2], k: "num", glue: true });
    out.push({ t: "txt", s: ")", glue: true });
    pos = m.index + m[0].length;
  }
  plain(out, text.slice(pos));
  return out;
}

/* ══════════ 박자표 ══════════ */
/**
 * 문항 하나의 박자표.
 *   steps[i] = { text, a(형광펜) , f:[a,b](칸 채우기), acts:[...], b(끝) }
 *   act: { type: "dot", P, a, b } | { type: "move", P, Q, run, rise, h:[a,b], v:[a,b] } | { type: "line", a, b }
 *   ans 정답 식이 뜨는 시각 · dur 전체
 */
const PLAN = new WeakMap();
export function gdPlan(it) {
  if (PLAN.has(it)) return PLAN.get(it);
  const m = q(it.m), b = q(it.b), P1 = it.P1.map(q), P2 = it.P2.map(q);
  const s1 = ptStr(P1), s2 = ptStr(P2);
  let t = GD.INTRO, have1 = false, have2 = false;
  const steps = it.steps.map((text) => {
    const st = { text, a: t, f: [t + GD.LEAD, t + GD.LEAD + GD.FILL], acts: [] };
    let c = st.f[1] + GD.GAP;
    const dot = (P) => { st.acts.push({ type: "dot", P, a: c, b: c + GD.DOT }); c += GD.DOT + GD.GAP; };
    if (text.includes("칸")) {
      if (!have1) { dot(P1); have1 = true; }
      const run = qv(P2[0]) - qv(P1[0]), rise = qv(P2[1]) - qv(P1[1]);
      const h = [c, c + GD.CELL * Math.abs(run) + GD.MVPAD];
      const v = [h[1] + GD.GAP, h[1] + GD.GAP + GD.CELL * Math.abs(rise) + GD.MVPAD];
      st.acts.push({ type: "move", P: P1, Q: P2, run, rise, h, v, a: h[0], b: v[1] });
      c = v[1] + GD.GAP;
      dot(P2); have2 = true;
    } else if (text.startsWith("두 점을")) {
      st.acts.push({ type: "line", a: c, b: c + GD.LINE });
      c += GD.LINE + GD.GAP;
    } else {
      const order = [[text.indexOf(s1), 1], [text.indexOf(s2), 2]].filter((x) => x[0] >= 0).sort((x, y) => x[0] - y[0]);
      for (const [, w] of order) {
        if (w === 1 && !have1) { dot(P1); have1 = true; }
        if (w === 2 && !have2) { dot(P2); have2 = true; }
      }
    }
    st.b = (st.acts.length ? c - GD.GAP : st.f[1] + GD.READ) + GD.REST;
    t = st.b;
    return st;
  });
  const out = { it, m, b, P1, P2, steps, ans: t, dur: t + GD.ANS + GD.HOLD };
  PLAN.set(it, out);
  return out;
}

/** 지금 몇 번째 줄인가(형광펜) — 모두 끝났으면 steps.length */
export function stepAt(plan, t) {
  for (let i = 0; i < plan.steps.length; i++) if (t < plan.steps[i].b) return i;
  return plan.steps.length;
}

/** 직선을 좌표평면 칸(−L ~ L) 조금 밖까지 자른 두 끝 */
export function clipLine(mv, bv, L) {
  const pts = [];
  for (const xb of [-L, L]) { const yb = mv * xb + bv; if (yb >= -L - 1e-9 && yb <= L + 1e-9) pts.push([xb, yb]); }
  for (const yb of [-L, L]) { const xb = (yb - bv) / mv; if (xb >= -L - 1e-9 && xb <= L + 1e-9) pts.push([xb, yb]); }
  pts.sort((p, r) => p[0] - r[0]);
  return [pts[0], pts[pts.length - 1]];
}

/** 한 바퀴(세트 전체) 시간 — 배속 sp */
export const lapOf = (items, sp = 1) => items.reduce((s, it) => s + gdPlan(it).dur, 0) / sp;
