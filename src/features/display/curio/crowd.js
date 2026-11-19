// ashrain.out — 수학 호기심 「북적북적 학년별 뽑기」 계산 (curio/crowd.js)
// 1 · 2 · 3학년 학생 수와 학년마다 뽑는 수를 고르면, 축제 날 운동장 그림 속에 학생들(학년마다 체육복 색) · 어른 · 동생 · 강아지를
// 씨앗으로 흩어 놓고 천천히 거닐게 한다. 차례마다 학년별로 정해진 수만큼 무작위로 뽑는다.
//   그렇게 뽑힐 확률 = Π 1 / C(학년 인원, 그 학년에서 뽑는 수)
// 사람마다 집(머무는 자리)과 거니는 길(느린 사인 곡선)이 씨앗으로 정해져 벽시계 시각만으로 어디 있는지 다시 계산된다.
import { hashSeed, rng, rint, namesOf, comb, shuffle } from "./kit.js";

export const CROWD = { AS: [4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 30], RS: [0, 1, 2, 3], TURN: 8400, EXTRA: 30 };
export const CROWD_DEF = { a1: 12, a2: 10, a3: 8, r1: 1, r2: 1, r3: 1, sp: 1, seed: 1 };
export function fixCrowd(p = {}) {
  const pick = (v, list, d) => (list.includes(v) ? v : d);
  const o = { a1: pick(p.a1, CROWD.AS, 12), a2: pick(p.a2, CROWD.AS, 10), a3: pick(p.a3, CROWD.AS, 8),
    r1: pick(p.r1, CROWD.RS, 1), r2: pick(p.r2, CROWD.RS, 1), r3: pick(p.r3, CROWD.RS, 1),
    sp: [0.5, 1, 1.5, 2].includes(p.sp) ? p.sp : 1, seed: Number.isInteger(p.seed) && p.seed > 0 ? p.seed : 1 };
  for (const g of [1, 2, 3]) if (o[`r${g}`] > o[`a${g}`]) o[`r${g}`] = o[`a${g}`];
  if (!o.r1 && !o.r2 && !o.r3) o.r1 = 1;
  return o;
}

/* ── 그림 상자(무대 좌표) · 걸어 다닐 수 없는 곳 ── */
export const BOX = { x: 24, y: 124, w: 1552, h: 760 };
// [x0, y0, x1, y1] — 그림 상자 안 좌표
export const BLOCKS = [
  [0, 0, 1552, 168],            // 건물 · 잔디 · 무대 앞까지
  [0, 0, 250, 760],             // 왼쪽 가게 줄
  [1300, 0, 1552, 760],         // 오른쪽 가게 줄
  [660, 330, 900, 470],         // 가운데 분수대
  [300, 640, 430, 760],         // 나무(아래 왼쪽)
  [1120, 640, 1250, 760],       // 나무(아래 오른쪽)
];
const free = (x, y) => x > 262 && x < 1290 && y > 190 && y < 742 && !BLOCKS.some(([a, b, c, d]) => x > a - 10 && x < c + 10 && y > b - 6 && y < d + 4);

const SKIN = ["#f8dcc2", "#efc9a6", "#dcaa82", "#c48b60", "#9c6a46"];
const HAIR = ["#231a15", "#3b2a1d", "#5b3a22", "#141418", "#7a4b2b", "#9a6a3a", "#c9c3b8"];
const ADULT = ["#4a5a78", "#6b6f78", "#c9b48d", "#7a5a44", "#3f6b4f", "#8a4c5a", "#5d6aa8", "#a37a5a", "#2f4f6f"];
const KIDC = ["#f4a9c0", "#9ed7e8", "#f6d86b", "#b9e3a0", "#d7b4f0"];
export const GRADE = ["#7cc242", "#3fa3e0", "#f08c2c"];         // 체육복: 1학년 연두 · 2학년 하늘 · 3학년 주황

/** 그림 속 사람들: 학생(학년 · 이름) + 어른 · 동생 · 강아지 */
const CACHE = new Map();
export function crowdOf(P) {
  const key = `${P.a1}|${P.a2}|${P.a3}|${P.seed}`;
  if (CACHE.has(key)) return CACHE.get(key);
  const R = rng(hashSeed("crowd", P.seed, P.a1, P.a2, P.a3));
  const total = P.a1 + P.a2 + P.a3;
  const names = namesOf(hashSeed("crowd-names", P.seed), total);
  // 자리: 간격을 두고 흩기(가까우면 다시)
  const pts = [];
  const want = total + CROWD.EXTRA;
  let minD = 46, guard = 0;
  while (pts.length < want && guard++ < 40000) {
    const x = 262 + R() * 1028, y = 192 + R() * 548;
    if (!free(x, y)) continue;
    if (pts.some((q) => Math.hypot(q[0] - x, (q[1] - y) * 1.4) < minD)) { if (guard % 4000 === 3999) minD *= 0.9; continue; }
    pts.push([x, y]);
  }
  const people = [];
  let ni = 0;
  for (const g of [1, 2, 3]) {
    for (let i = 0; i < P[`a${g}`]; i++) {
      people.push({ kind: "student", grade: g, name: names[ni++], skin: SKIN[rint(R, 4)], hair: HAIR[rint(R, 6)], style: rint(R, 6),
        pants: "#2c3a5e", bag: R() < 0.3 ? ["#d45a4a", "#3b6fb8", "#f2c14e", "#5a8a4a"][rint(R, 4)] : null, glasses: R() < 0.12 });
    }
  }
  for (let i = 0; i < CROWD.EXTRA; i++) {
    const r = R();
    if (r < 0.55) people.push({ kind: "adult", skin: SKIN[rint(R, 5)], hair: HAIR[rint(R, 7)], style: rint(R, 6), shirt: ADULT[rint(R, ADULT.length)], pants: ["#3a3a44", "#5a4a3a", "#2c3a5e", "#6a6a70"][rint(R, 4)], hat: R() < 0.25 ? ["#3f6b4f", "#c9b48d", "#4a5a78"][rint(R, 3)] : null, item: ["", "", "balloon", "icecream", "bag"][rint(R, 5)], bcol: ["#f2685c", "#6ea6f5", "#f5cf4e", "#a6d886", "#c6a8f6"][rint(R, 5)] });
    else if (r < 0.85) people.push({ kind: "kid", skin: SKIN[rint(R, 5)], hair: HAIR[rint(R, 6)], style: rint(R, 6), shirt: KIDC[rint(R, KIDC.length)], pants: "#4a5a78", item: R() < 0.5 ? "balloon" : "", bcol: ["#f2685c", "#6ea6f5", "#f5cf4e", "#c6a8f6"][rint(R, 4)] });
    else people.push({ kind: "dog", fur: ["#c98b4a", "#f0e0c0", "#5a4030", "#2a2420"][rint(R, 4)] });
  }
  // 자리 · 거니는 길(학생과 다른 사람을 섞어 놓는다)
  const order = shuffle(people.map((_, i) => i), R);
  order.forEach((pi, k) => {
    const p = people[pi], [x, y] = pts[k % pts.length];
    const still = p.kind !== "dog" && R() < 0.3;
    p.hx = x; p.hy = y;
    p.ax = still ? 0 : 14 + R() * 30; p.ay = still ? 0 : 5 + R() * 9;
    p.wx = (2 * Math.PI) / (9000 + R() * 12000); p.wy = p.wx * (1.3 + R() * 0.9);
    p.px = R() * 6.28; p.py = R() * 6.28;
    p.idle = still;
  });
  const students = people.filter((p) => p.kind === "student");
  const out = { people, students, byGrade: [1, 2, 3].map((g) => students.filter((s) => s.grade === g)) };
  CACHE.set(key, out);
  if (CACHE.size > 30) CACHE.delete(CACHE.keys().next().value);
  return out;
}

/** 시각 t(ms, 벽시계)에 사람의 자리 · 바라보는 쪽 · 걸음 */
export function posOf(p, t) {
  const x = p.hx + p.ax * Math.sin(p.wx * t + p.px), y = p.hy + p.ay * Math.sin(p.wy * t + p.py);
  const vx = p.ax * p.wx * Math.cos(p.wx * t + p.px);
  const moving = Math.abs(vx) > 0.0012 || p.ay * p.wy * Math.abs(Math.cos(p.wy * t + p.py)) > 0.0012;
  return { x, y, face: vx >= 0 ? 1 : -1, step: moving ? Math.floor(t / 230) % 2 : -1 };
}

/** k번째 차례에 뽑힌 학생들: [{ g, list: [학생 번호…] }] */
export function pickOf(P, k, crowd) {
  const R = rng(hashSeed("crowd-pick", P.seed, k, P.a1, P.a2, P.a3, P.r1, P.r2, P.r3));
  return [1, 2, 3].map((g) => {
    const pool = crowd.byGrade[g - 1].map((_, i) => i);
    const r = P[`r${g}`], got = [];
    for (let i = 0; i < r; i++) { const j = rint(R, pool.length); got.push(pool.splice(j, 1)[0]); }
    return { g, list: got.sort((a, b) => a - b) };
  });
}

/** 판서 줄 */
export function crowdLines(P, picks, crowd, mode) {
  const out = [];
  const factors = [];
  for (const { g, list } of picks) {
    const a = P[`a${g}`], r = list.length;
    if (!r) continue;
    const ways = comb(a, r);
    const expr = r === 1 ? `${a}` : r === 2 ? `${a} × ${a - 1} ÷ 2` : `${a} × ${a - 1} × ${a - 2} ÷ (3 × 2 × 1)`;
    factors.push(ways);
    out.push({ g, s: mode === "m" ? `${g}학년 ${a}명 중 ${r}명: ${r > 1 ? `${expr} = ` : ""}${ways}가지 → {1/${ways}}` : `${g}학년 ${a}명 중 ${r}명 뽑기: ${ways}가지` });
  }
  const total = factors.reduce((x, y) => x * y, 1);
  const last = mode === "m"
    ? `이렇게 뽑힐 확률 = ${factors.map((w) => `{1/${w}}`).join(" × ")}${factors.length > 1 ? ` = {1/${total}}` : ""}`
    : `모두 ${factors.join(" × ")}${factors.length > 1 ? ` = ${total}` : ""}가지 중 하나 → {1/${total}}`;
  return { lines: out, last, total };
}
