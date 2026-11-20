// ashrain.out — 수학 호기심 액자: 볼링으로 보는 일차함수와 점수 계산 (curio/bowl.js)
// 레인(위에서 본 모습): x = 파울 선에서 핀 쪽으로 간 거리(ft, 0 ~ 60), y = 보드 번호(오른쪽 끝 1 ~ 왼쪽 끝 39).
// 곧게 굴리는 공(스트레이트)은 직선 y = ax + b 를 따라간다 — b = 파울 선에서 공이 지나는 보드,
// 15 ft 의 화살표에서 보드 c 를 지나면 a = (c − b) ÷ 15, 핀(60 ft)에서는 y = 4c − 3b.
//   초등: 15 ft 마다 같은 칸씩 옮겨 간다(비례) — 화살표에서 1보드 틀리면 핀에서는 4보드!  · 스트라이크/스페어 보너스 덧셈
//   중등: 두 점 (0, b) · (15, c) 를 지나는 직선의 식, x = 60 대입.
// 가상 선수 · 가상 게임(씨앗) — 핀이 쓰러지는 것은 간단한 규칙(공에 닿은 핀 → 뒤 핀으로 번짐)으로 흉내 낸다.
import { rng, rint, hashSeed, namesOf, frac, fs, num, lineOf, eqText } from "./kit.js";

export const LANE = { len: 60, boards: 39, arrow: 15, pocket: 17.5 };
export const ARROWS = [5, 10, 15, 20, 25, 30, 35];
const ROW = 0.866;   // 핀 줄 사이(ft) = 12 in × sin 60°
const BW = 1.064;    // 보드 한 칸(in)
const off = (inch) => inch / BW;
/** 핀 1~10: x(ft) · y(보드) */
export const PINS = {
  1: [60, 20], 2: [60 + ROW, 20 + off(6)], 3: [60 + ROW, 20 - off(6)],
  4: [60 + 2 * ROW, 20 + off(12)], 5: [60 + 2 * ROW, 20], 6: [60 + 2 * ROW, 20 - off(12)],
  7: [60 + 3 * ROW, 20 + off(18)], 8: [60 + 3 * ROW, 20 + off(6)], 9: [60 + 3 * ROW, 20 - off(6)], 10: [60 + 3 * ROW, 20 - off(18)],
};
export const ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const BALL_R = 4.0, PIN_R = 2.25;   // 보드 단위 반지름(공 지름 8.5 in, 핀 지름 4.77 in)

/** 핀(60 ft)에서 공이 지나는 보드: y = 4c − 3b */
export const entryOf = (b, c) => 4 * c - 3 * b;
/**
 * 핀이 쓰러짐(간단한 흉내): 공이 지나는 길(보드 y = entry + a(x − 60))에 닿은 핀이 먼저 쓰러지고,
 * 쓰러진 핀은 공이 지나간 반대쪽 뒤로 날아가 뒤 핀을 넘어뜨린다(가운데를 맞으면 바로 뒤로).
 * 핀을 얇게 스친 공(가장자리)은 힘이 약하다 — 헤드핀 정면이면 2 · 3번 핀이 옆으로 빠져 스플릿이 잘 난다.
 * 반환: 쓰러진 핀 [{ n, by(누가 넘어뜨렸나, 0 = 공), k(순서) }]
 */
export function pinAction(R, standing, a, entry) {
  const yAt = (x) => entry + a * (x - 60);
  if (entry < 0.5 || entry > LANE.boards + 0.5) return [];   // 도랑(거터)
  const reach = BALL_R + PIN_R;
  const down = new Map();
  let k = 0;
  const order = [...standing].sort((u, v) => PINS[u][0] - PINS[v][0] || u - v);
  for (const n of order) {
    const [px, py] = PINS[n], d = py - yAt(px), ad = Math.abs(d);
    if (ad < reach) down.set(n, { s: ad < 3.6 ? 0.95 : 0.95 - (ad - 3.6) * 0.17, dir: ad < 1.2 ? 0 : Math.sign(d), by: 0, k: k++ });
  }
  for (let pass = 0; pass < 2; pass++) {
    for (const n of order) {
      if (!down.has(n)) continue;
      const P = PINS[n], { s, dir } = down.get(n);
      for (const m of order) {
        if (down.has(m)) continue;
        const Q = PINS[m], dx = Q[0] - P[0], dy = Q[1] - P[1];
        let p = 0;
        if (dx > 0.1 && dx < 0.95 && Math.abs(dy) < 6.5) p = Math.min(0.95, s * (dir === 0 ? 0.72 : Math.sign(dy) === dir ? 0.82 : 0.2));   // 바로 뒤 대각선
        else if (dx > 0.95 && dx < 1.9 && Math.abs(dy) < 1) p = s * (dir === 0 ? 0.7 : 0.25);                                                  // 두 줄 뒤 같은 보드
        else if (Math.abs(dx) < 0.1 && Math.abs(dy) < 12 && Math.sign(dy) === dir) p = s * 0.3;                                              // 같은 줄, 날아가는 쪽
        if (p > 0 && R() < p) down.set(m, { s: s * 0.88, dir: dir === 0 ? Math.sign(dy) : dir, by: n, k: k++ });
      }
    }
  }
  return [...down.entries()].map(([n, v]) => ({ n, by: v.by, k: v.k })).sort((u, v) => u.k - v.k);
}

/* ══════════ 한 게임 ══════════ */
const MEMO = new Map();
/** 가상 선수: 공을 놓는 보드 b(오른손 · 파울 선) — 핀에서 17~18 보드(포켓)가 되는 정수 화살표가 있는 자리 */
const BASES = [5, 6, 9, 10, 13, 14];
/**
 * 한 게임: { seed, name, base, rolls: [{ f, r, b, c, aimC, entry, a([n, d]), before, down, after, mark }], frames: [{ rolls: [i…], score, total, bonus }] }
 */
export function bowlGame(seed) {
  if (MEMO.has(seed)) return MEMO.get(seed);
  const R = rng(hashSeed("bowl", seed));
  const name = namesOf(hashSeed("bowler", seed), 1)[0];
  const base = BASES[rint(R, BASES.length)];
  const acc = 0.36 + R() * 0.26;   // 화살표를 정확히 지날 확률
  const rolls = [];
  const frames = [];
  const aimFor = (target) => Math.round((target + 3 * base) / 4);
  const miss = () => { const u = R(); if (u < acc) return 0; const v = R() < 0.82 ? 1 : 2; return R() < 0.5 ? -v : v; };
  const roll = (f, r, standing, target) => {
    const aimC = Math.max(1, Math.min(39, aimFor(target)));
    const c = Math.max(1, Math.min(39, aimC + miss()));
    const entry = entryOf(base, c);
    const a = frac(c - base, 15);
    const down = pinAction(R, standing, (c - base) / 15, entry);
    const dn = new Set(down.map((d) => d.n));
    const after = standing.filter((n) => !dn.has(n));
    const o = { f, r, b: base, c, aimC, target, entry, a, before: standing, down, after, n: down.length };
    rolls.push(o);
    return o;
  };
  // 남은 핀에서 겨냥할 보드: 가장 앞 핀(여럿이면 그 줄 가운데)
  const spareTarget = (left) => {
    const fx = Math.min(...left.map((n) => PINS[n][0]));
    const front = left.filter((n) => Math.abs(PINS[n][0] - fx) < 0.1);
    const ys = left.map((n) => PINS[n][1]);
    const spread = Math.max(...ys) - Math.min(...ys);
    if (spread > 13) return (Math.max(...ys) + Math.min(...ys)) / 2 + (R() - 0.5) * 2;   // 갈라진 핀(스플릿): 가운데로
    return front.reduce((s, n) => s + PINS[n][1], 0) / front.length;
  };
  for (let f = 0; f < 10; f++) {
    const ids = [];
    let s1 = roll(f, 0, ALL.slice(), LANE.pocket);
    ids.push(rolls.length - 1);
    if (f < 9) {
      if (s1.after.length) { roll(f, 1, s1.after, spareTarget(s1.after)); ids.push(rolls.length - 1); }
    } else {
      // 10프레임: 스트라이크나 스페어면 한 번 더(세 번까지) — 다 쓰러지면 핀을 새로 세운다
      const tgt = (left) => (left.length === 10 ? LANE.pocket : spareTarget(left));
      const st1 = s1.after.length === 0;
      const left2 = st1 ? ALL.slice() : s1.after;
      const s2 = roll(f, 1, left2, tgt(left2));
      ids.push(rolls.length - 1);
      if (st1 || s2.after.length === 0) {
        const left3 = s2.after.length === 0 ? ALL.slice() : s2.after;
        roll(f, 2, left3, tgt(left3));
        ids.push(rolls.length - 1);
      }
    }
    frames.push({ rolls: ids });
  }
  // 점수: 스트라이크 10 + 다음 두 번, 스페어 10 + 다음 한 번
  const pins = rolls.map((o) => o.n);
  let total = 0;
  frames.forEach((F, f) => {
    const i = F.rolls[0];
    const r1 = pins[i];
    let score, bonus = [];
    if (f < 9) {
      if (r1 === 10) { bonus = [i + 1, i + 2]; score = 10 + pins[i + 1] + pins[i + 2]; F.kind = "strike"; }
      else if (r1 + pins[i + 1] === 10) { bonus = [i + 2]; score = 10 + pins[i + 2]; F.kind = "spare"; }
      else { score = r1 + pins[i + 1]; F.kind = "open"; }
    } else {
      score = F.rolls.reduce((s, j) => s + pins[j], 0);
      F.kind = r1 === 10 ? "strike" : r1 + pins[i + 1] === 10 ? "spare" : "open";
    }
    total += score;
    F.score = score; F.total = total; F.bonus = bonus;
    F.done = Math.max(...F.rolls, ...bonus);   // 이 프레임 점수가 정해지는 투구
  });
  // 표시 글자: X · / · − · 숫자
  rolls.forEach((o, i) => {
    const F = frames[o.f];
    const first = F.rolls[0] === i, prev = first ? null : rolls[i - 1];
    if (o.before.length === 10 && o.n === 10) o.mark = "X";
    else if (!first && prev && prev.f === o.f && o.before.length < 10 && o.after.length === 0) o.mark = "/";
    else o.mark = o.n === 0 ? "−" : String(o.n);
    o.split = o.before.length === 10 && isSplit(o.after);
  });
  const g = { seed, name, base, rolls, frames, total };
  MEMO.set(seed, g);
  if (MEMO.size > 8) MEMO.delete(MEMO.keys().next().value);
  return g;
}
/** 스플릿: 헤드핀(1번)이 쓰러지고, 남은 핀 사이에 쓰러진 핀이 끼어 있음 */
export function isSplit(left) {
  if (left.length < 2 || left.includes(1)) return false;
  const ys = left.map((n) => PINS[n][1]).sort((a, b) => a - b);
  for (let i = 1; i < ys.length; i++) if (ys[i] - ys[i - 1] > 12) return true;
  return false;
}

/* ══════════ 박자 ══════════ */
export const BT = { roll: 7800, gameEnd: 5200, aim: [0, 700], travel: [700, 3100], fall: [3050, 4300], math: 3300, clear: [6700, 7600] };
const DUR = new Map();
/** 씨앗 seed 의 k 번째 게임 길이(ms) — 지나간 게임은 길이만 기억해 다시 만들지 않는다 */
function gameDur(seed, k) {
  const key = seed * 1000003 + k;
  let d = DUR.get(key);
  if (d == null) { d = bowlGame(seed + k).rolls.length * BT.roll + BT.gameEnd; DUR.set(key, d); if (DUR.size > 4000) DUR.clear(); }
  return d;
}
/** 경과 e → { g(게임), k, i(투구 번호 · 끝나면 rolls.length), t(투구 안 시각) } */
export function bowlAt(seed, e) {
  let at = Math.max(0, e), k = 0;
  for (;;) {
    const d = gameDur(seed, k);
    if (at < d || k > 5000) {
      const g = bowlGame(seed + k);
      const i = Math.min(g.rolls.length, Math.floor(at / BT.roll));
      return { g, k, i, t: at - i * BT.roll, start: e - at };
    }
    at -= d; k++;
  }
}

/* ══════════ 판서 ══════════ */
/** 핀에서 지나는 보드의 이름 */
export function entryName(entry) {
  if (entry < 0.5 || entry > LANE.boards + 0.5) return "도랑(거터)";
  if (entry >= 16 && entry <= 19) return "포켓";
  if (entry >= 21.5 && entry <= 23.5) return "브루클린(반대쪽 포켓)";
  if (Math.abs(entry - 20) < 1.5) return "헤드핀 정면";
  return entry < 16 ? "오른쪽으로 비낌" : "왼쪽으로 비낌";
}
/** 투구 o 의 판서 줄 */
export function bowlSteps(o, mode) {
  const d = o.c - o.b;
  const res = { s: `핀에서 ${num(o.entry)}번 보드 — ${entryName(o.entry)}`, hi: true };
  const miss = o.c === o.aimC ? null : { s: `겨냥은 화살표 ${o.aimC}번 — ${Math.abs(o.c - o.aimC)}보드 빗나감`, small: true, col: "coral" };
  if (mode === "m") {
    const a = fs(o.a[0], o.a[1]);
    return [
      { s: `(0, ${o.b}) · (15, ${o.c})를 지나는 직선` },
      ...(miss ? [miss] : []),
      { s: `기울기 = {${o.c} − ${o.b}/15} = ${a}` },
      { s: eqText(lineOf([0, o.b], [15, o.c])) },
      { s: `x = 60 → y = ${a} × 60 + ${o.b} = ${num(o.entry)}`, small: true },
      res,
    ];
  }
  return [
    { s: `파울 선 ${o.b}번 보드 → 화살표 ${o.c}번 보드` },
    ...(miss ? [miss] : []),
    { s: `15 ft 가는 동안 ${d === 0 ? "옆으로 그대로" : `${d > 0 ? "왼쪽" : "오른쪽"}으로 ${Math.abs(d)}칸`}` },
    ...(d === 0 ? [] : [{ s: `60 ft는 15 ft의 4배 → ${Math.abs(d)} × 4 = ${Math.abs(4 * d)}칸`, small: true }, { s: `${o.b} ${d > 0 ? "+" : "−"} ${Math.abs(4 * d)} = ${num(o.entry)}`, small: true }]),
    res,
  ];
}
/** 프레임 f 점수 글자: 스트라이크 10 + 7 + 2 = 19 */
export function frameCalc(g, f) {
  const F = g.frames[f], pins = g.rolls.map((o) => o.n);
  if (f === 9) return `10프레임: ${F.rolls.map((j) => pins[j]).join(" + ")} = ${F.score}`;
  if (F.kind === "strike") return `${f + 1}프레임 스트라이크: 10 + ${pins[F.bonus[0]]} + ${pins[F.bonus[1]]} = ${F.score}`;
  if (F.kind === "spare") return `${f + 1}프레임 스페어: 10 + ${pins[F.bonus[0]]} = ${F.score}`;
  return `${f + 1}프레임: ${pins[F.rolls[0]]} + ${pins[F.rolls[1]]} = ${F.score}`;
}
