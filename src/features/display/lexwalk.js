// ashrain.out — 사전식 「카드로 순번 찾기」의 걸음과 박자 (lexwalk.js) — 그리기는 frames/lexcards.jsx
// 경우의 수와 확률 100제 · 사전식 세트(../cnt100-items.js 의 CNT100_LEX)의 나무 자료(fig.kind === "tree")에서 만든다.
//   걸음: 첫 자리부터 — 앞선 묶음(A 묶음 24개 · B 묶음 24개 …)을 휘리릭 지나가며 셈이 오르고, 고른 글자(C)를 자리에 고정,
//         다음 자리에서 또 앞선 묶음을 지나가고 … 마지막 묶음(최종 묶음) 안에서는 하나씩 점멸하며 마지막 순서까지 센다.
//   「○번째 문자열」이면 셈 = 번호, 「단어는 몇 번째」면 셈 = 그 단어의 순번(뒤에서는 판서 끝줄이 바꾼다).
//   박자: 판서 줄(l10Plan)에 맞춘다 — 나무의 at[단] = [묶음을 지나가는 줄, 글자를 고르는 줄] · tailAt = 최종 묶음을 세는 줄.
//         애니메이션이 줄 시간 안에 다 돌도록 모자라는 만큼 그 줄에 hold(ms)를 더한다(lexPrep — ../cnt100.js 가 불러올 때 한 번).
import { lineLen } from "./lin10.js";

/** n 개 중 k 개를 늘어놓는 가짓수 */
export const nP = (n, k) => { let v = 1; for (let i = 0; i < k; i++) v *= n - i; return v; };
/** 글자들(사전 순으로 놓고)로 만든 길이 len 의 배열 가운데 idx 번째(0부터) */
export function nthArr(letters, len, idx) {
  const rest = [...letters].sort();
  let out = "", k0 = idx;
  for (let p = 0; p < len; p++) {
    const blk = nP(rest.length - 1, len - p - 1);
    const k = Math.floor(k0 / blk);
    k0 -= k * blk;
    out += rest[k];
    rest.splice(k, 1);
  }
  return out;
}
/** 배열 s 의 순번(0부터) — 글자들(사전 순)로 만든 길이 s.length 의 배열 가운데 */
export function rankArr(letters, s) {
  const rest = [...letters].sort();
  let r = 0;
  for (let p = 0; p < s.length; p++) {
    const k = rest.indexOf(s[p]);
    r += k * nP(rest.length - 1, s.length - p - 1);
    rest.splice(k, 1);
  }
  return r;
}

const WALK = new WeakMap();
/**
 * 걸음. { cards(사전 순) · r(늘어놓는 장 수) · target(찾는 문자열) · levels[{ pos, skips[{ L, m, c0, prefix, letters, len }], pick, at }] ·
 *         final{ pos, prefix, letters, len, c0, j(최종 묶음 안의 순번 · 1부터), at } · total(= 셈) }
 *   skips 의 문자열 k 번째(0부터) = prefix + nthArr(letters, len, k) — 셈은 c0 + k + 1.
 */
export function lexWalk(it) {
  const f = it?.fig;
  if (!f || f.kind !== "tree") return null;
  if (WALK.has(it)) return WALK.get(it);
  const cards = [...f.cards].sort();
  const chosen = f.cols.map((c) => c.items.find((x) => x[2])[0]);
  const target = chosen.join("") + (f.tail || "");
  const r = target.length;
  let cnt = 0;
  const levels = f.cols.map((c, li) => {
    const pre = chosen.slice(0, li).join("");
    const rest = cards.filter((L) => !pre.includes(L));
    const skips = [];
    for (const [L, m, ch] of c.items) {
      if (ch) break;
      skips.push({ L, m, c0: cnt, prefix: pre + L, letters: rest.filter((x) => x !== L), len: r - li - 1 });
      cnt += m;
    }
    return { pos: li, skips, pick: chosen[li], at: f.at[li] };
  });
  const prefix = chosen.join("");
  const letters = cards.filter((L) => !prefix.includes(L));
  const j = rankArr(letters, f.tail || "") + 1;
  const out = { cards, r, target, levels, final: { pos: chosen.length, prefix, letters, len: r - chosen.length, c0: cnt, j, at: f.tailAt }, total: cnt + j };
  WALK.set(it, out);
  return out;
}

/* ══════════ 박자 ══════════ */
export const LEX_T = {
  DEAL: 110, DEAL_END: 520,      // 카드 늘어놓기: 한 장마다 · 마지막 장이 자리 잡는 시간
  LEAD: 260,                     // 줄이 나타난 뒤 움직임이 시작되기까지
  SKIP: 780, GAP: 150,           // 묶음 하나 휘리릭 · 묶음 사이
  PICK: 640,                     // 고른 카드가 자리로 날아가는 시간
  COUNT: 2700, STEP_MIN: 210, STEP_MAX: 560,   // 최종 묶음 점멸: 모두 합해 이쯤 · 한 번의 길이 범위
  TAIL: 160,                     // 줄 끝 여유
};
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
/**
 * 최종 묶음 세기 — j 번째까지. 6 이하면 하나씩 점멸, 더 많으면(최종 묶음을 통째로 지나 맨 끝까지 가는 문항)
 * 앞의 j − 3 개는 휘리릭 지나가고 마지막 셋만 점멸한다.  { fastN, fast(휘리릭 길이), step(점멸 한 번), len(모두) }
 */
export function countPlan(j) {
  if (j <= 6) { const step = clamp(LEX_T.COUNT / Math.max(1, j), LEX_T.STEP_MIN, LEX_T.STEP_MAX); return { fastN: 0, fast: 0, step, len: step * j }; }
  const fast = Math.round(LEX_T.SKIP * 1.6), step = 480;
  return { fastN: j - 3, fast, step, len: fast + 120 + step * 3 };
}

/** 줄마다 애니메이션이 차지하는 최소 길이(줄이 나타난 때부터) — 한 줄에 여러 움직임이 몰리면 모두 더한다 */
function needs(W) {
  const need = new Map();
  const add = (i, v) => need.set(i, (need.get(i) || LEX_T.LEAD + LEX_T.TAIL) + v);
  for (const lv of W.levels) {
    const [sa, pa] = lv.at, ns = lv.skips.length;
    if (ns) add(sa, ns * LEX_T.SKIP + (ns - 1) * LEX_T.GAP + 180);
    add(pa, LEX_T.PICK + 120);
  }
  const F = W.final;
  add(F.at, 100 + countPlan(F.j).len + 450);
  return need;
}
/** 판서 줄에 hold(ms)를 더해 애니메이션이 줄 안에 다 돌게 한다 — l10Plan 보다 먼저 한 번(../cnt100.js) */
export function lexPrep(it) {
  const W = lexWalk(it);
  if (!W) return;
  for (const [i, v] of needs(W)) {
    const ln = it.lines[i];
    if (!ln) continue;
    // 줄 길이 = max(글자 몫 + hold, 메모 몫) — 메모 몫이 이미 넉넉하면 hold 는 0
    const len0 = lineLen({ ...ln, hold: 0 }), body = lineLen({ ...ln, hold: 0, memo: null });
    ln.hold = len0 >= v ? 0 : Math.max(0, Math.round(v - body));
  }
}

const TIMES = new WeakMap();
/**
 * 시각표(1배속 ms). P = l10Plan(it).
 *   deal[a, b] 카드 늘어놓기 · slots 빈칸 나타남 · ev[] = skip{ pos, sk, t0, t1 } · pick{ pos, L, t0, t1 } ·
 *   count{ t0, fastN(휘리릭으로 지나갈 개수) · fastEnd, bt0(점멸 시작) · step, t1 } · back(뒤에서 줄) · done(답)
 */
export function lexTimes(it, P) {
  if (TIMES.has(it)) return TIMES.get(it);
  const W = lexWalk(it), n = W.cards.length;
  const L = (i) => P.lines[Math.min(Math.max(0, i), P.lines.length - 1)];
  const deal = [L(0).a + 150, L(0).a + 150 + n * LEX_T.DEAL + LEX_T.DEAL_END];
  const slots = L(1).a + 200;
  const ev = [];
  let lastPick = null;
  for (const lv of W.levels) {
    const [sa, pa] = lv.at, ns = lv.skips.length;
    let pickT;
    if (ns) {
      const A = L(sa), s0 = Math.max(A.a + LEX_T.LEAD, lastPick ? lastPick.t1 + 120 : 0);
      const s1min = s0 + ns * LEX_T.SKIP + (ns - 1) * LEX_T.GAP;
      // 묶음만 지나가는 줄이면 줄 끝까지 펴되, 한 묶음이 1.1초를 넘지 않게(휘리릭)
      const s1 = sa !== pa ? Math.min(Math.max(s1min, A.b - LEX_T.TAIL), s0 + ns * 1100 + (ns - 1) * LEX_T.GAP) : s1min;
      const d = (s1 - s0 - (ns - 1) * LEX_T.GAP) / ns;
      lv.skips.forEach((sk, k) => { const a = s0 + k * (d + LEX_T.GAP); ev.push({ type: "skip", pos: lv.pos, sk, t0: a, t1: a + d }); });
      pickT = sa !== pa ? Math.max(L(pa).a + LEX_T.LEAD, s1 + 120) : s1 + 180;
    } else pickT = Math.max(L(pa).a + LEX_T.LEAD, lastPick ? lastPick.t1 + 120 : 0);
    lastPick = { type: "pick", pos: lv.pos, L: lv.pick, t0: pickT, t1: pickT + LEX_T.PICK };
    ev.push(lastPick);
  }
  const F = W.final, cp = countPlan(F.j);
  const c0 = Math.max(L(F.at).a + LEX_T.LEAD, lastPick ? lastPick.t1 + 100 : 0);
  const bt0 = cp.fastN ? c0 + cp.fast + 120 : c0;
  ev.push({ type: "count", t0: c0, fastN: cp.fastN, fastEnd: c0 + cp.fast, bt0, step: cp.step, t1: c0 + cp.len });
  const bi = it.lines.findIndex((ln) => ln.pre === "뒤에서");
  const out = { deal, slots, ev, back: bi >= 0 ? L(bi).a + 300 : null, done: P.ans };
  TIMES.set(it, out);
  return out;
}
