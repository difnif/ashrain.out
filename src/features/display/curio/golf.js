// ashrain.out — 수학 호기심: 골프 한 라운드(가상) 계산 (curio/golf.js)
// 9홀 가상 코스(수학 컨트리클럽)를 가상 선수가 돈다. 샷마다
//   위에서 본 길(공이 있던 곳 → 떨어진 곳 → 굴러간 곳)과 옆에서 본 포물선(높이)을 남긴다.
//   중등(중3): 옆에서 본 길 = 이차함수 y = a(x − p)² + q — 꼭짓점 (날아간 거리 ÷ 2, 가장 높은 높이), x절편 0 · 날아간 거리.
//   초등: 가장 높은 곳은 날아간 거리의 한가운데(대칭) · 남은 거리 중 몇 %를 쳤나(비율).
// 거리는 m. 날아간 거리(carry)는 짝수 정수, 높이(apex)는 정수로 둔다(꼭짓점이 정수가 되게).
import { rng, rint, hashSeed, namesOf, frac, fs } from "./kit.js";

/* ══════════ 코스 ══════════ */
// 홀: par · 중심선(티 → 그린, m) · 페어웨이 폭 · 그린 반지름 · 깃대 자리(그린 가운데에서) · 벙커 · 물 [x, y, rx, ry]
export const HOLES = [
  { par: 4, line: [[0, 0], [150, 0], [250, -18], [372, -50]], fw: 34, gr: 15, pin: [3, 4], bunk: [[262, 2, 14, 7], [384, -32, 9, 6]], water: [] },
  { par: 3, line: [[0, 0], [90, 6], [168, 10]], fw: 0, gr: 16, pin: [-4, -3], bunk: [[178, 26, 10, 6], [184, -6, 7, 9]], water: [[112, 6, 26, 22]] },
  { par: 5, line: [[0, 0], [190, 12], [330, -24], [440, -14], [518, 12]], fw: 36, gr: 16, pin: [4, -2], bunk: [[208, -8, 12, 7], [425, 6, 10, 6], [532, -6, 8, 7]], water: [[300, 30, 22, 13]] },
  { par: 4, line: [[0, 0], [200, 0], [408, 0]], fw: 32, gr: 15, pin: [-3, 3], bunk: [[240, 21, 13, 7], [252, -22, 13, 7], [392, -18, 8, 6], [394, 19, 8, 6]], water: [] },
  { par: 4, line: [[0, 0], [170, 0], [255, 36], [345, 70]], fw: 34, gr: 14, pin: [2, -4], bunk: [[186, -20, 13, 8], [356, 52, 9, 6]], water: [[250, 0, 18, 14]] },
  { par: 3, line: [[0, 0], [100, -4], [192, -8]], fw: 0, gr: 15, pin: [5, 2], bunk: [[178, 14, 9, 6], [184, -26, 9, 7], [206, -6, 6, 10]], water: [] },
  { par: 5, line: [[0, 0], [210, -6], [380, 10], [544, 20]], fw: 38, gr: 17, pin: [-5, 4], bunk: [[230, 14, 13, 7], [520, 2, 9, 7]], water: [[300, -30, 70, 14]] },
  { par: 4, line: [[0, 0], [160, 0], [262, -30], [392, -42]], fw: 32, gr: 14, pin: [3, 3], bunk: [[262, -2, 12, 7], [402, -24, 8, 6]], water: [] },
  { par: 4, line: [[0, 0], [210, 8], [428, 0]], fw: 34, gr: 16, pin: [-2, -5], bunk: [[244, -14, 14, 8], [414, 18, 9, 6], [418, -19, 9, 6]], water: [[338, 18, 16, 10]] },
];
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const lerp = (a, b, k) => a + (b - a) * k;
/** 중심선 위 길이 s(m)의 점 */
export function along(line, s) {
  let left = s;
  for (let i = 1; i < line.length; i++) {
    const L = dist(line[i - 1], line[i]);
    if (left <= L) { const k = left / L; return [lerp(line[i - 1][0], line[i][0], k), lerp(line[i - 1][1], line[i][1], k)]; }
    left -= L;
  }
  return line[line.length - 1].slice();
}
export const holeLen = (h) => { let s = 0; for (let i = 1; i < h.line.length; i++) s += dist(h.line[i - 1], h.line[i]); return s; };
/** 홀 정보: 그린 가운데 · 깃대 · 길이(정수 m) */
export function holeInfo(h) {
  const g = h.line[h.line.length - 1];
  return { green: g, pin: [g[0] + h.pin[0], g[1] + h.pin[1]], len: Math.round(holeLen(h)) };
}
/** 점에서 중심선까지 거리 · 그 점의 중심선 위 길이 */
function nearLine(line, p) {
  let best = 1e9, bs = 0, acc = 0;
  for (let i = 1; i < line.length; i++) {
    const a = line[i - 1], b = line[i], L = dist(a, b);
    const k = Math.max(0, Math.min(1, ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / (L * L)));
    const q = [lerp(a[0], b[0], k), lerp(a[1], b[1], k)];
    const d = dist(p, q);
    if (d < best) { best = d; bs = acc + k * L; }
    acc += L;
  }
  return { d: best, s: bs };
}
const inEll = (p, [x, y, rx, ry]) => ((p[0] - x) / rx) ** 2 + ((p[1] - y) / ry) ** 2 <= 1;
/** 그 자리의 땅: green · fringe · bunker · water · fairway · rough · tee */
export function lieAt(h, p) {
  const { green } = holeInfo(h);
  for (const w of h.water) if (inEll(p, w)) return "water";
  for (const b of h.bunk) if (inEll(p, b)) return "bunker";
  const dg = dist(p, green);
  if (dg <= h.gr) return "green";
  if (dg <= h.gr + 4) return "fringe";
  const n = nearLine(h.line, p);
  if (n.s < 12 && n.d < 6) return "tee";
  if (h.fw && n.d <= h.fw / 2 && n.s > 90) return "fairway";
  return "rough";
}
export const LIE = { green: "그린", fringe: "그린 가장자리", bunker: "벙커", water: "물", fairway: "페어웨이", rough: "러프", tee: "티" };

/* ══════════ 클럽 ══════════ */
// [이름, 평균 날아간 거리(m), 가장 높은 높이(m)] — 프로 선수 평균에 가깝게
const CLUBS = [["드라이버", 238, 32], ["3번 우드", 216, 30], ["5번 우드", 202, 30], ["4번 아이언", 188, 28], ["5번 아이언", 177, 29],
  ["6번 아이언", 166, 30], ["7번 아이언", 154, 30], ["8번 아이언", 142, 30], ["9번 아이언", 130, 29], ["피칭 웨지", 117, 28], ["갭 웨지", 102, 27], ["샌드 웨지", 86, 25]];
const even = (v) => 2 * Math.round(v / 2);

/* ══════════ 한 라운드 ══════════ */
// 샷 = { kind: "full" | "chip" | "putt", club, from, land, rest, carry, apex, d0, d1(남은 거리 · 정수 m), lie, pen?, made?, ms }
function playHole(R, h, skill) {
  const { pin } = holeInfo(h);
  const shots = [];
  let pos = h.line[0].slice(), lie = "tee", strokes = 0, guard = 0;
  while (guard++ < 14) {
    const d0 = dist(pos, pin);
    if (lie === "green") {
      // 퍼트
      const pMake = d0 <= 0.9 ? 0.97 : d0 <= 2 ? 0.82 : d0 <= 3.5 ? 0.55 : d0 <= 6 ? 0.3 : d0 <= 10 ? 0.12 : 0.05;
      const made = R() < pMake * skill.putt;
      let rest = pin.slice();
      if (!made) {
        const k = 0.08 + R() * 0.14, ang = (R() - 0.5) * 1.6;
        const ux = (pin[0] - pos[0]) / (d0 || 1), uy = (pin[1] - pos[1]) / (d0 || 1);
        const over = d0 * k * (R() < 0.6 ? 1 : -1);
        rest = [pin[0] + ux * over * Math.cos(ang) - uy * Math.max(0.3, d0 * k) * Math.sin(ang), pin[1] + uy * over * Math.cos(ang) + ux * Math.max(0.3, d0 * k) * Math.sin(ang)];
      }
      strokes += 1;
      shots.push({ kind: "putt", club: "퍼터", from: pos, land: rest, rest, carry: 0, apex: 0, d0: Math.round(d0 * 10) / 10, d1: made ? 0 : Math.round(dist(rest, pin) * 10) / 10, lie: made ? "cup" : "green", made, ms: 3200 });
      if (made) break;
      pos = rest; continue;
    }
    // 어프로치(그린 가까이) · 그린 옆 벙커에서는 샌드 웨지로 띄운다
    if (d0 < 34 || (lie === "bunker" && d0 < 46)) {
      const sand = lie === "bunker";
      const carry = even(Math.max(4, d0 * (sand ? 0.72 + R() * 0.22 : 0.55 + R() * 0.25)));
      const ang = Math.atan2(pin[1] - pos[1], pin[0] - pos[0]) + (R() - 0.5) * (sand ? 0.2 : 0.12);
      const land = [pos[0] + Math.cos(ang) * carry, pos[1] + Math.sin(ang) * carry];
      const roll = Math.max(0.5, d0 - carry + (R() - 0.5) * d0 * (sand ? 0.5 : 0.35));
      const rest = [land[0] + Math.cos(ang) * roll, land[1] + Math.sin(ang) * roll];
      strokes += 1;
      let lie2 = lieAt(h, rest);
      if (lie2 === "water" || lie2 === "fringe" || lie2 === "tee") lie2 = "green";
      shots.push({ kind: "chip", club: sand ? "샌드 웨지" : "어프로치", from: pos, land, rest, carry, apex: sand ? 4 + rint(R, 4) : 2 + rint(R, 4), d0: Math.round(d0), d1: Math.round(dist(rest, pin)), lie: lie2, sand, ms: 3600 });
      pos = rest; lie = lie2;
      continue;
    }
    // 풀 스윙: 클럽 고르기
    const tee = lie === "tee";
    const par3 = h.par === 3;
    let want = d0 - (lie === "rough" ? 4 : 10);
    let club = CLUBS[CLUBS.length - 1];
    if (tee && !par3) club = d0 > 330 ? CLUBS[0] : CLUBS[1];
    else for (const c of CLUBS.slice(1)) { if (c[1] <= want + 6) { club = c; break; } }   // 페어웨이에서는 드라이버 대신 우드부터
    if (lie === "bunker" && club[1] > 150) club = CLUBS[7];
    const pen = lie === "rough" ? 0.9 : lie === "bunker" ? 0.8 : 1;
    // 거리 오차(±8 %, 가운데가 잦다) · 가끔 빗맞음
    const mis = R() < skill.miss;
    let carry = even(club[1] * pen * (skill.dist + (R() + R() - 1) * 0.08) * (mis ? 0.78 + R() * 0.12 : 1));
    if (!tee || par3) carry = even(Math.min(carry, d0 + 12));
    const apex = Math.round(club[2] * (0.92 + R() * 0.14) * (lie === "rough" ? 0.85 : 1));
    // 겨냥: 티샷(파 4 · 5)은 그 거리의 중심선, 아니면 깃대
    const aim = tee && !par3 ? along(h.line, Math.min(holeLen(h) - 20, carry + 12)) : pin;
    const sd = (club[0] === "드라이버" ? 0.085 : 0.07) * skill.acc * (mis ? 2.2 : 1);
    const ang = Math.atan2(aim[1] - pos[1], aim[0] - pos[0]) + (R() + R() + R() - 1.5) * sd;
    const land = [pos[0] + Math.cos(ang) * carry, pos[1] + Math.sin(ang) * carry];
    const lie1 = lieAt(h, land);
    const roll = lie1 === "fairway" ? 8 + R() * 12 : lie1 === "green" || lie1 === "fringe" ? 1 + R() * 3 : lie1 === "rough" ? 1 + R() * 3 : 0;
    let rest = [land[0] + Math.cos(ang) * roll, land[1] + Math.sin(ang) * roll];
    let lie2 = lie1 === "water" || lie1 === "bunker" ? lie1 : lieAt(h, rest);
    if (lie1 === "water" || lie1 === "bunker") rest = land.slice();
    strokes += 1;
    const sh = { kind: "full", club: club[0], from: pos, land, rest, carry, apex, d0: Math.round(d0), d1: Math.round(dist(rest, pin)), lie: lie2, ms: 5600 };
    if (lie2 === "water") {
      // 벌타 1타 — 물에 들어간 자리에서 홀 쪽 반대로 조금 물러나 드롭
      strokes += 1; sh.pen = true;
      const n = nearLine(h.line, land);
      // 물가에서 6 m 넘게 떨어진 곳까지 물러난다
      const wet = (q) => h.water.some(([x, y, rx, ry]) => ((q[0] - x) / (rx + 6)) ** 2 + ((q[1] - y) / (ry + 6)) ** 2 <= 1);
      let drop = along(h.line, Math.max(0, n.s - 25));
      for (let t = 0; t < 12 && wet(drop); t++) drop = along(h.line, Math.max(0, n.s - 25 - 8 * (t + 1)));
      sh.drop = drop; sh.d1 = Math.round(dist(drop, pin));
      rest = drop; lie2 = lieAt(h, drop) === "green" ? "green" : "rough";
    }
    shots.push(sh);
    pos = rest; lie = lie2 === "fringe" ? "fringe" : lie2;
    if (lie === "fringe") lie = dist(pos, pin) < 32 ? "rough" : "rough";
  }
  return { shots, strokes };
}

const RMEMO = new Map();
/** 한 라운드(9홀): { seed, name, holes: [{ i, par, len, shots, strokes, score(타수 − 파), total(그 홀까지 합) }] } */
export function roundOf(seed) {
  if (RMEMO.has(seed)) return RMEMO.get(seed);
  const R = rng(hashSeed("golf", seed));
  const name = namesOf(hashSeed("golfer", seed), 1)[0];
  const skill = { dist: 0.97 + R() * 0.06, acc: 0.8 + R() * 0.5, putt: 0.95 + R() * 0.1, miss: 0.04 + R() * 0.08 };
  let total = 0;
  const holes = HOLES.map((h, i) => {
    const { shots, strokes } = playHole(R, h, skill);
    total += strokes - h.par;
    return { i, par: h.par, len: holeInfo(h).len, shots, strokes, score: strokes - h.par, total };
  });
  const out = { seed, name, holes };
  RMEMO.set(seed, out);
  if (RMEMO.size > 12) RMEMO.delete(RMEMO.keys().next().value);
  return out;
}
export const SCORE_NAME = { "-3": "앨버트로스", "-2": "이글", "-1": "버디", "0": "파", "1": "보기", "2": "더블 보기", "3": "트리플 보기" };
export const scoreName = (d) => SCORE_NAME[String(d)] || (d > 0 ? `${d}오버` : `${-d}언더`);
export const totalText = (t) => (t === 0 ? "이븐" : t > 0 ? `${t}오버` : `${-t}언더`);

/* ══════════ 시간 ══════════ */
export const GT = { intro: 2400, end: 2600 };
/** 홀 하나의 박자 */
export function holeTimes(hole) {
  const shotsAt = [];
  let t = GT.intro;
  for (const s of hole.shots) { shotsAt.push(t); t += s.ms; }
  const endAt = t;
  return { shotsAt, endAt, dur: endAt + GT.end };
}
const SMEMO = new Map();
/** 라운드를 이어 돌리는 시간표: 씨앗 seed, seed + 1 … (라운드마다 새 선수) */
const RDUR = new Map();
/** 라운드 길이(ms) — 지나간 라운드는 길이만 기억해 다시 만들지 않는다(하루 종일 켜 두어도 가볍게) */
function roundDur(rs) {
  let d = RDUR.get(rs);
  if (d == null) { d = roundOf(rs).holes.map(holeTimes).reduce((s, T) => s + T.dur, 0); RDUR.set(rs, d); if (RDUR.size > 5000) RDUR.clear(); }
  return d;
}
export function golfAt(seed, e) {
  let at = Math.max(0, e), k = 0;
  for (;;) {
    const total = roundDur(seed + k);
    if (at < total || k > 100000) {
      const r = roundOf(seed + k);
      const key = r.seed;
      let tl = SMEMO.get(key);
      if (!tl) { tl = r.holes.map(holeTimes); SMEMO.set(key, tl); if (SMEMO.size > 12) SMEMO.delete(SMEMO.keys().next().value); }
      let i = 0;
      while (i < tl.length - 1 && at >= tl[i].dur) { at -= tl[i].dur; i++; }
      return { round: r, hi: i, T: tl[i], t: at, k };
    }
    at -= total; k++;
  }
}

/* ══════════ 판서 ══════════ */
/** 풀 스윙 · 어프로치의 옆에서 본 포물선: 꼭짓점 (p, q), a = −q / p² */
export function parabola(carry, apex) {
  const p = carry / 2, q = apex;
  const a = frac(-q, p * p);
  return { p, q, a };
}
/** 그 샷의 판서 줄 */
export function golfSteps(s, mode) {
  if (s.kind === "putt") {
    return mode === "m"
      ? [{ s: `그린 위 — 굴러가는 길은 곧은 선(높이 0)` }, { s: `남은 거리 ${s.d0} m → ${s.made ? "홀컵!" : `${s.d1} m`}`, hi: s.made }]
      : [{ s: `그린에서는 굴려요` }, { s: `${s.d0} m 굴려서 ${s.made ? "쏙!" : `${s.d1} m 남음`}`, hi: s.made }];
  }
  const { p, q, a } = parabola(s.carry, s.apex);
  if (mode === "m") {
    return [
      { s: `${s.sand ? "벙커에서 · " : ""}날아간 거리 ${s.carry} m · 가장 높이 ${s.apex} m` },
      { s: `꼭짓점 (${p}, ${q}) — 날아간 거리의 절반에서 가장 높다`, small: true },
      { s: `y = a(x − ${p})² + ${q}` },
      { s: `(0, 0)을 지나므로 0 = a × ${p}² + ${q}`, small: true },
      { s: `a = ${fs(a[0], a[1])}` },
      { s: `y = ${fs(a[0], a[1])}(x − ${p})² + ${q}`, hi: true },
      { s: `남은 거리 ${s.d0} m → ${s.pen ? `물! 벌타 1 · ${s.d1} m` : `${s.d1} m`}`, col: s.pen ? "coral" : "teal" },
    ];
  }
  const cut = s.d0 - s.d1, pct = Math.round((100 * Math.max(0, cut)) / Math.max(1, s.d0));
  return [
    { s: `${s.sand ? "벙커에서 띄워 " : ""}날아간 거리 ${s.carry} m` },
    { s: `가장 높은 곳: 한가운데 ${p} m 지점, 높이 ${q} m` },
    { s: `양쪽이 똑같이 생긴 길(대칭)`, small: true },
    ...(cut > 0
      ? [{ s: `남은 거리 ${s.d0} m 중 ${cut} m를 줄였어요` }, { s: `${cut} ÷ ${s.d0} → 약 ${pct}%`, hi: true }]
      : [{ s: `남은 거리 ${s.d0} m → ${s.d1} m`, hi: true }]),
    ...(s.pen ? [{ s: `물에 빠져 벌타 1타`, col: "coral" }] : []),
  ];
}
