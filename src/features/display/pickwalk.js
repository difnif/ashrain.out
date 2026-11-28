// ashrain.out — 「학년별 선발」 · 「주머니 공 꺼내기」 해설 그림의 움직임 차례 (pickwalk.js) — 그리기는 frames/c100fig.jsx 의 PickFig
// 판서 식의 수 하나하나가 그림의 무엇을 센 것인지 찾아(해석기) 칠판에서 하듯 보인다:
//   · 짚어 세기 — 그 무리(학년 · 성별 · 색 · 홀짝 · 배수 …)를 하나씩 짚으며 1, 2, 3 … 세고 수를 찍는다(합의 법칙은 무리마다 차례로)
//   · 자리로 뽑기 — 아래 「뽑은 자리」 칸마다 남은 후보를 짚어 세고(n, n − 1, …) 하나를 자리로 날려 보낸다(곱의 법칙 · 뽑힌 사람은 빠진다)
//   · 순서 없음(÷ 2 · ÷ (3 × 2 × 1)) — 뽑은 자리끼리 순서를 바꿔 보여 같은 무리임을 보이고 「÷ 2」 · 「÷ (3 × 2 × 1)」을 찍는다
//   · 나열 · 순서쌍 — 적힌 수의 공이 차례로 떠오르고(순서쌍은 A · B 공을 선으로 잇고) 개수를 센다
//   · 모든 경우 N — 전체가 한 번 물결치듯 빛나고 N 을 찍는다
// 식을 그림에 맞추지 못한 줄은 움직이지 않는다(예전처럼 그 줄이 가리키는 무리만 빛남 — hl). 줄마다 움직임이 다 돌도록 hold 를 더한다(pickPrep).
import { lineLen } from "./lin10.js";

/* ══════════ 그림 속 물건 — 학생 · 공 ══════════ */
const PRIMES = new Set([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]);
/** objs[j] = { g(무리 열쇠), sx(남 · 여), name, bag, c(색), n(번호) } — 그리는 쪽과 같은 차례(학년마다 · 주머니마다) */
export function objectsOf(it) {
  const f = it.fig;
  const out = [];
  if (f.kind === "grades") {
    f.groups.forEach((gp) => {
      const kids = gp.n != null ? Array.from({ length: gp.n }, () => (gp.key === "남" ? "남" : gp.key === "여" ? "여" : "")) : [...Array(gp.m).fill("남"), ...Array(gp.f).fill("여")];
      kids.forEach((sx, j) => {
        const nm = f.named.find((q) => q.g === gp.key && q.i === j);
        out.push({ g: gp.key, sx, name: nm ? nm.name : null, gi: out.length });
      });
    });
  } else {
    f.bags.forEach((bg, bi) => bg.balls.forEach((b) => out.push({ bag: bi, g: bg.lab || "", c: b.c || null, n: b.n ?? null })));
  }
  return out.map((o, j) => ({ ...o, j }));
}

/* ══════════ 무리(후보 집합) ══════════ */
const COL = ["빨간", "파란", "노란", "흰", "검은", "초록"];
const setKey = (a) => a.join(",");
/** 이 문항에서 생각할 수 있는 무리들 — { ids[], tag, cost, keys(무리 열쇠 목록) } */
function poolsOf(it, objs, text) {
  const f = it.fig, P = [];
  const add = (ids, tag, cost, keys = []) => { if (ids.length) P.push({ ids: ids.slice().sort((a, b) => a - b), tag, cost, keys }); };
  const all = objs.map((o) => o.j);
  if (f.kind === "grades") {
    const gs = f.groups.map((g) => g.key);
    add(all, "모두", 0, ["*"]);
    const n = gs.length;
    for (let mask = 1; mask < 1 << n; mask++) {
      const ks = gs.filter((_, i) => mask & (1 << i));
      const ids = objs.filter((o) => ks.includes(o.g)).map((o) => o.j);
      if (ks.length < n) add(ids, ks.join("·"), ks.length === 1 ? 0.2 : 0.8 + ks.length * 0.1, ks);
      if (ks.length < n) add(all.filter((j) => !ids.includes(j)), `${ks.join("·")} 빼고`, 1.2, ks.map((k) => "!" + k));
    }
    if (f.groups.some((g) => g.m != null)) {
      for (const sx of ["남", "여"]) {
        add(objs.filter((o) => o.sx === sx).map((o) => o.j), sx, 0.4, ["sx" + sx]);
        for (const g of gs) add(objs.filter((o) => o.sx === sx && o.g === g).map((o) => o.j), `${g}학년 ${sx}`, 0.3, [g, "sx" + sx]);
      }
    }
    const named = f.named.map((q) => q.name);
    for (const nm of named) {
      const j = objs.find((o) => o.name === nm)?.j;
      if (j == null) continue;
      add(all.filter((x) => x !== j), `${nm} 빼고`, 0.9, ["-" + nm]);
    }
    if (named.length === 2) {
      const js = named.map((nm) => objs.find((o) => o.name === nm)?.j);
      add(all.filter((x) => !js.includes(x)), `${named.join(" · ")} 빼고`, 0.9, named.map((nm) => "-" + nm));
    }
  } else {
    f.bags.forEach((bg, bi) => {
      const mine = objs.filter((o) => o.bag === bi);
      const tag = bg.lab ? `${bg.lab} ` : "";
      add(mine.map((o) => o.j), `${tag}모두`, f.bags.length > 1 ? 0.1 : 0, [bg.lab || "*"]);
      const cols = [...new Set(mine.map((o) => o.c).filter(Boolean))];
      for (const c of cols) {
        add(mine.filter((o) => o.c === c).map((o) => o.j), `${tag}${c}`, 0.2, [bg.lab, c]);
        add(mine.filter((o) => o.c !== c).map((o) => o.j), `${tag}${c} 빼고`, 0.9, [bg.lab, "!" + c]);
      }
      if (mine[0]?.n != null) {
        add(mine.filter((o) => o.n % 2 === 1).map((o) => o.j), `${tag}홀수`, 0.3, [bg.lab, "홀수"]);
        add(mine.filter((o) => o.n % 2 === 0).map((o) => o.j), `${tag}짝수`, 0.3, [bg.lab, "짝수"]);
        for (const m of (text.match(/(\d+)의 (?:배수|약수)/g) || [])) {
          const k = +m.match(/\d+/)[0];
          if (m.includes("배수")) add(mine.filter((o) => o.n % k === 0).map((o) => o.j), `${tag}${k}의 배수`, 0.3, [bg.lab, "배수" + k]);
          else add(mine.filter((o) => k % o.n === 0).map((o) => o.j), `${tag}${k}의 약수`, 0.3, [bg.lab, "약수" + k]);
        }
        if (/소수/.test(text)) add(mine.filter((o) => PRIMES.has(o.n)).map((o) => o.j), `${tag}소수`, 0.3, [bg.lab, "소수"]);
        const ex = text.match(/(\d+) 제외/);
        if (ex) add(mine.filter((o) => o.n !== +ex[1]).map((o) => o.j), `${tag}${ex[1]} 빼고`, 0.5, [bg.lab, "제외"]);
        for (const m of text.matchAll(/(\d+)보다 작은/g)) add(mine.filter((o) => o.n < +m[1]).map((o) => o.j), `${tag}${m[1]}보다 작은`, 0.4, [bg.lab, "작은"]);
      }
    });
  }
  // 같은 무리가 겹치면 하나만(가장 싼 것)
  const seen = new Map();
  for (const p of P) { const k = setKey(p.ids); if (!seen.has(k) || seen.get(k).cost > p.cost) seen.set(k, p); }
  return [...seen.values()];
}

/* ══════════ 식 읽기 ══════════ */
/** 줄 글자 → 앞쪽 식(첫 「=」 앞) 낱말 목록: { t: "n", v, lab } · { t: "op", v } · { t: "(" } · { t: ")" } */
function tokens(src) {
  let s = String(src).replace(/\{[^}]*\}/g, " F ");
  const cut = s.indexOf(" = ");
  if (cut >= 0) s = s.slice(0, cut);
  s = s.replace(/\(([^()]*[가-힣][^()]*)\)/g, " ");     // 한글이 든 괄호는 풀이 말(…제외) — 식에서 뺀다
  const out = [];
  let lab = "";
  const re = /(\d+)|([+−×÷])|([()])|([^\d+−×÷()]+)/g;
  let m;
  while ((m = re.exec(s))) {
    if (m[1]) { out.push({ t: "n", v: +m[1], lab: lab.trim() }); lab = ""; }
    else if (m[2]) { out.push({ t: "op", v: m[2] }); lab = ""; }
    else if (m[3]) { out.push({ t: m[3] }); lab = ""; }
    else lab += m[4];
  }
  return out;
}
/** 식 나무 — sum{ terms[{ sign, prod }] } · prod{ fs[], div } · num{ v, lab } */
function parse(tk) {
  let i = 0;
  const peek = () => tk[i];
  function sum() {
    const terms = [{ sign: 1, prod: prod() }];
    while (peek() && peek().t === "op" && (peek().v === "+" || peek().v === "−")) {
      const sg = tk[i++].v === "+" ? 1 : -1;
      terms.push({ sign: sg, prod: prod() });
    }
    return { k: "sum", terms };
  }
  function prod() {
    const fs = [factor()];
    let div = null;
    while (peek() && peek().t === "op" && (peek().v === "×" || peek().v === "÷")) {
      const op = tk[i++].v;
      // ÷ 2 · ÷ (3 × 2 × 1) — 나누는 수는 괄호 안을 펼쳐 쓴 것도(그 값으로)
      if (op === "÷") { const d = factor(); const dv = d.k === "num" ? d.v : evalTree(d); if (!(dv > 0)) throw new Error("÷"); div = dv; break; }
      fs.push(factor());
    }
    return { k: "prod", fs, div };
  }
  function factor() {
    const t = tk[i++];
    if (!t) throw new Error("끝");
    if (t.t === "n") return { k: "num", v: t.v, lab: t.lab };
    if (t.t === "(") { const e = sum(); if (!peek() || peek().t !== ")") throw new Error(")"); i++; return e; }
    throw new Error("?");
  }
  const e = sum();
  if (i < tk.length) throw new Error("남음");
  return e;
}
const FACT = [1, 1, 2, 6, 24, 120];
/** 식 나무의 값(시험이 움직임으로 센 값과 맞춰 본다) */
export function evalTree(e) {
  if (e.k === "num") return e.v;
  if (e.k === "sum") return e.terms.reduce((a, t) => a + t.sign * evalTree(t.prod), 0);
  const v = e.fs.reduce((a, f) => a * evalTree(f), 1);
  return e.div ? v / e.div : v;
}

/* ══════════ 해석 — 식의 수를 무리에 맞추기 ══════════ */
function scorePool(p, n, lab, ctx) {
  if (p.ids.length !== n) return -Infinity;
  let s = -p.cost;
  const words = `${lab} `;
  const lit = ctx.lit;
  let best = 0, litB = 0, sum = 0;
  const kindOf = (k) => (/^[!-]?\d$/.test(k) ? "g" : /^sx/.test(k) ? "sx" : /^[AB*]?$/.test(k) ? "bag" : "attr");
  const mixed = new Set(p.keys.map(kindOf)).size > 1;
  for (const k of p.keys) {
    if (!k) continue;
    const kk = k.replace(/^[!-]/, "");
    const said = (w) => (/^\d$/.test(kk) ? new RegExp(`${kk}(?:·\\d)*학년|\\d·${kk}학년|${kk}, \\d학년`).test(w) : w.includes(kk.replace("sx", "")));
    const b = said(words) ? 4 : said(ctx.line) ? 2 : said(ctx.neg) ? 1 : 0;
    best = Math.max(best, b); sum += b;
    if (lit && /^\d$|^남$|^여$/.test(kk) && lit.has(kk) && !k.startsWith("!")) litB = 1.5;
  }
  s += (mixed ? sum : best) + litB;     // 「B 짝수」처럼 주머니 · 성질을 함께 말하면 둘 다 맞는 무리가 낫다
  if (p.keys[0] === "*" && /모두|모든|전체/.test(lab + ctx.line + ctx.neg)) s += 1.5;
  if (p.keys.some((k) => k.startsWith("!")) && /없음|아닌|적어도|빼|제외/.test(lab + ctx.line + ctx.neg)) s += 2.5;
  if (p.keys.some((k) => k.startsWith("-")) && /제외|빼/.test(ctx.neg)) s += 2;
  if (p.rest) s += 0.5;
  return s;
}
function bestPool(pools, n, lab, ctx, avoid, sxPref = null, gAvoid = null) {
  let best = null, bs = -Infinity;
  for (const p of pools) {
    if (avoid && !p.rest && p.ids.some((j) => avoid.has(j))) continue;
    let sc = scorePool(p, n, lab, ctx);
    if (sxPref && sc > -Infinity) sc += p.keys.includes("sx" + sxPref) ? 2 : p.keys.some((k) => /^sx/.test(k)) ? -2 : 0;
    if (gAvoid && sc > -Infinity && p.keys.some((k) => gAvoid.has(k))) sc -= 2;
    if (sc > bs) { bs = sc; best = p; }
  }
  return best ? { ...best, score: bs } : null;
}
/**
 * 곱 하나를 뽑기 차례로 — { picks: [{ pool, k(뽑는 수), div } · { arrange: k }], score } · 못 맞추면 null.
 * 두 가지로 읽어 보고 그럴듯한 쪽을 고른다:
 *   chain — 하나씩 줄어드는 수(6 × 5 × 4)는 한 무리에서 차례로 뽑기(같은 학년 · 자격이 다르다 · 회장 …)
 *   sep   — 수마다 다른 무리에서 하나씩(학년마다 · 각각 · 씩 · 서로 다른 · 학년 차례대로)
 * 뽑힌 사람은 다음 무리에서 빠진다 — 「조장은 조원이 될 수 없다」처럼 남은 사람에서 뽑는 것도(rest).
 * (k × … × 1) 이나 k! 이 앞에서 뽑은 k 명의 자리를 정하는 것이면 뽑은 자리끼리 줄 세우기(arrange).
 */
const SEP_W = /마다|각각|씩|서로 다른|짝지어|다른 학년|모두 다르/;
const CHAIN_W = /같은 학년|같은 색|자격이 다르|다른 사람|회장|부회장|부장|차장/;
function resolveProd(pr, pools, ctx, st) {
  let best = null;
  for (const mode of ["chain", "sep"]) {
    const st2 = { ...st, used: new Set(st.used), picked: new Set(st.picked) };
    const r = resolveMode(pr, pools, ctx, st2, mode);
    if (!r) continue;
    const words = ctx.neg + ctx.line + (st.lab0 || "");
    const flip = ctx.flip && /다른 학년|서로 다른/.test(words);     // 「다른 학년」을 빼는 쪽(같은 학년)은 거꾸로
    if (mode === "sep" && SEP_W.test(words) && !flip) r.score += 3;
    if (mode === "chain" && (CHAIN_W.test(words) || flip)) r.score += 3;
    if (!best || r.score > best.score + 1e-9) best = { ...r, st: st2 };
  }
  if (!best) return null;
  st.used = best.st.used; st.picked = best.st.picked;
  return best;
}
function resolveMode(pr, pools, ctx, st, mode) {
  const back = /다시 넣음|다시 넣는|다시 넣고/.test(ctx.pos + ctx.neg + ctx.line);   // 꺼낸 공을 다시 넣으면 다음에도 같은 무리에서
  const fs = pr.fs;
  const runs = [];
  for (let i = 0; i < fs.length; i++) {
    const f = fs[i];
    if (f.k === "num") {
      const last = runs[runs.length - 1];
      if (mode === "chain" && last && last.kind === "chain" && last.vals[last.vals.length - 1] - 1 === f.v && f.v > 0 && !f.lab) last.vals.push(f.v);
      else runs.push({ kind: "chain", vals: [f.v], lab: `${st.lab0 || ""} ${f.lab}`.trim() });
    } else if (f.k === "sum" && f.terms.every((t) => t.sign > 0 && t.prod.fs.length === 1 && t.prod.fs[0].k === "num" && !t.prod.div)) {
      runs.push({ kind: "union", vals: f.terms.map((t) => t.prod.fs[0].v), labs: f.terms.map((t) => t.prod.fs[0].lab) });
    } else if (f.k === "sum" && f.terms.length === 1 && f.terms[0].sign > 0) {
      runs.push({ kind: "sub", prod: f.terms[0].prod });
    } else if (f.k === "sum" && f.terms.every((t) => t.prod.fs.length === 1 && t.prod.fs[0].k === "num" && !t.prod.div) && f.terms.some((t) => t.sign < 0)) {
      // (9 − 2) — 앞 무리를 뺀 나머지에서 하나
      runs.push({ kind: "chain", vals: [f.terms.reduce((a, t) => a + t.sign * t.prod.fs[0].v, 0)], lab: `${st.lab0 || ""} 빼고`.trim() });
    } else return null;
  }
  const picks = [];
  let score = 0;
  const nPicked = () => picks.reduce((a, p) => a + (p.k || 0), 0);
  let lastSx = null, lastG = -1, inOrder = true;
  for (const r of runs) {
    if (r.kind === "sub") {
      const fsv = r.prod.fs.every((x) => x.k === "num") ? r.prod.fs.map((x) => x.v) : null;
      const k = nPicked();
      if (fsv && !r.prod.div && k > 1 && fsv.length === k && fsv.every((v, q) => v === k - q)) { picks.push({ arrange: k }); continue; }
      const subSt = { ...st, inner: true };
      const sub = resolveProd(r.prod, pools, ctx, subSt);
      if (!sub) return null;
      st.used = subSt.used; st.picked = subSt.picked; st.grades = subSt.grades;     // 괄호 안에서 쓴 무리는 밖에서도 쓴 것
      picks.push(...sub.picks);
      score += sub.score;
      continue;
    }
    if (r.kind === "union") {
      const parts = [];
      for (let q = 0; q < r.vals.length; q++) {
        const got = bestPool(pools, r.vals[q], r.labs[q], ctx, new Set([...st.used, ...parts.flatMap((x) => x.ids)]));
        if (!got) return null;
        parts.push(got);
        score += got.score;
      }
      const ids = [...new Set(parts.flatMap((p) => p.ids))];
      if (ids.length !== r.vals.reduce((a, b) => a + b, 0)) return null;
      const pool = { ids: ids.sort((a, b) => a - b), tag: parts.map((p) => p.tag).join(" + "), parts };
      picks.push({ pool, k: 1, div: null });
      take(pool, 1, st);
      continue;
    }
    if (!st.inner && r === runs[runs.length - 1] && r.vals.length === 1 && nPicked() > 2 && r.vals[0] === FACT[nPicked()] && /자격이 다르|순서/.test(ctx.neg)) { picks.push({ arrange: nPicked() }); continue; }
    const rest = st.picked.size && !back ? { ids: st.all.filter((j) => !st.picked.has(j)), tag: "남은 것", cost: 0.6, keys: ["*"], rest: true } : null;
    const cand = rest ? [...pools, rest] : pools;
    const sxPref = /성별도 다름|성별이 다/.test(ctx.neg) && lastSx ? (lastSx === "남" ? "여" : "남") : null;
    const gAvoid = /학년도 다름|학년이 모두 다르|다른 학년/.test(ctx.neg) ? st.grades : null;
    const got = bestPool(cand, r.vals[0], r.lab, ctx, back ? null : runs.length > 1 || st.used.size ? st.used : null, sxPref, gAvoid);
    if (!got) {
      if (r.vals[0] === 1 && r.vals.length === 1 && runs.length > 1) { picks.push({ pool: null, k: 0, one: true }); score -= 5; continue; }
      return null;
    }
    score += got.score;
    const sx = got.keys.find((k) => /^sx/.test(k));
    lastSx = sx ? sx.slice(2) : lastSx;
    const gk = got.keys.find((k) => /^\d$/.test(k));
    if (gk != null) { if (+gk < lastG) inOrder = false; lastG = +gk; (st.grades ||= new Set()).add(gk); } else inOrder = false;
    picks.push({ pool: got, k: r.vals.length, div: null, back });
    if (!back) take(got, r.vals.length, st);
  }
  const nP = picks.filter((x) => x.pool).length;
  if (nP > 1) score /= nP;          // 무리 수가 많다고 점수가 쌓이지 않게(평균)
  if (mode === "sep" && inOrder && runs.length > 1) score += 1.5;
  if (pr.div) {
    const last = [...picks].reverse().find((x) => x.pool);
    if (!last || FACT[last.k] !== pr.div) return null;
    last.div = pr.div;
  }
  return { picks, score };
}
/** 무리에서 k 명을 뽑았다 — 짚는 차례의 끝에서(뽑힌 사람 · 그 무리 사람은 다음에 쓰지 않음) */
function take(pool, k, st) {
  const left = pool.ids.filter((j) => !st.picked.has(j));
  for (let q = 0; q < k; q++) { const j = left[left.length - 1 - q]; if (j != null) st.picked.add(j); }
  pool.ids.forEach((j) => st.used.add(j));
}

/* ══════════ 줄마다 움직임 ══════════ */
const PLANS = new WeakMap();
/**
 * 줄마다 움직임 목록. acts: count{ ids, val } · pick{ pool, k, div, slot0 } · clear{ sign } · list{ ids, nums } · pairs{ pairs[[a, b]] } · all{ val }
 * 그 줄이 「F(분수)」만이거나 맞추지 못하면 빈 목록.
 */
export function pickPlan(it) {
  if (PLANS.has(it)) return PLANS.get(it);
  const objs = objectsOf(it), f = it.fig;
  const neg = it.lines[1] ? `${it.lines[1].pre || ""} ${it.lines[1].s}` : "";
  const lines = it.lines.map((ln, i) => {
    if (i < 2) return { acts: [], why: "머리" };
    const s = ln.s;
    const lit = (() => {
      const h = f.hl?.[i];
      if (!h || h === "all") return null;
      if (f.kind === "grades") return new Set([...(h.g || [])]);
      return null;
    })();
    const ctx = { line: `${ln.pre || ""} ${s}`, neg, lit, pos: it.lines[0] ? it.lines[0].s : "" };
    const pools = poolsOf(it, objs, `${neg} ${s}`);
    const pre0 = (s.match(/^(.*?):\s*/) || [null, ""])[1];
    const body = s.replace(/^.*?:\s*/, (m) => (/\d/.test(s.slice(m.length)) ? "" : m));
    if (/^\s*\d학년 \d명$/.test(pre0)) return { acts: [], why: "경우 나눔(조합 수)" };
    // 나열 · 순서쌍(번호 공)
    if (f.kind === "bag" && objs[0]?.n != null) {
      if (/^\s*\d+(?:,\s*\d+)+\s*$/.test(body)) {
        const nums = body.split(",").map((x) => +x.trim());
        const ids = nums.map((v) => objs.find((o) => o.n === v)?.j);
        if (ids.every((x) => x != null)) return { acts: [{ type: "list", ids, nums }] };
      }
      const prs = [...s.matchAll(/\((\d+),\s*(\d+)\)/g)].map((m) => [+m[1], +m[2]]);
      if (prs.length >= 2 && f.bags.length === 2 && /^\s*(\(\d+,\s*\d+\)(,\s*)?)+\s*$/.test(s)) {
        const pairs = prs.map(([a, b]) => [objs.find((o) => o.bag === 0 && o.n === a)?.j, objs.find((o) => o.bag === 1 && o.n === b)?.j]);
        if (pairs.every((p) => p[0] != null && p[1] != null)) return { acts: [{ type: "pairs", pairs }] };
      }
      const rg = s.match(/^\s*(\d+)\s*~\s*(\d+):\s*(\d+)개\s*$/);
      if (rg) {
        const ids = objs.filter((o) => o.n >= +rg[1] && o.n <= +rg[2]).map((o) => o.j);
        if (ids.length === +rg[3]) return { acts: [{ type: "count", ids, val: ids.length, tag: `${rg[1]} ~ ${rg[2]}` }] };
      }
      const mults = [...s.matchAll(/(\d+)의 배수 (\d+)개/g)];
      if (mults.length >= 2) {
        const acts = [];
        for (const m of mults) {
          const k = +m[1], ids = objs.filter((o) => o.n % k === 0).map((o) => o.j);
          if (ids.length !== +m[2]) return { acts: [] };
          acts.push({ type: "count", ids, val: ids.length, tag: `${k}의 배수` });
        }
        return { acts };
      }
    }
    // 모든 경우 N(수 하나)
    const allN = s.match(/^\s*모든 경우\s+(\d+)\s*$/);
    if (allN) return { acts: [{ type: "all", val: +allN[1] }] };
    if (/\bF\b/.test(s.replace(/\{[^}]*\}/g, "F")) && !/[×+−]\s*\d/.test(s.replace(/\{[^}]*\}/g, ""))) return { acts: [], why: "확률" };
    // 식 — 앞의 이름표(「2학년 2명」 · 「모든 경우」 · 「1학년 없음」)를 떼고 식이 시작하는 곳부터 읽는다
    let tree = null, lab0 = "";
    const eq = body.indexOf(" = "), head = eq >= 0 ? body.slice(0, eq) : body;
    const starts = [0, ...[...head.matchAll(/(?<=\s)(?=[\d(])/g)].map((m) => m.index)];
    for (const st0 of starts) {
      const lb = body.slice(0, st0).trim();
      if (/[×+−÷,()]/.test(lb)) break;
      try { tree = parse(tokens(body.slice(st0))); lab0 = `${body === s ? "" : pre0} ${lb}`.trim(); break; } catch (e) { tree = null; }
    }
    if (!tree) return { acts: [], why: "식 못 읽음" };
    // −(a + b + c) 처럼 괄호로 묶은 합은 경우마다 풀어서
    tree = { k: "sum", terms: tree.terms.flatMap((t) => (t.prod.fs.length === 1 && t.prod.fs[0].k === "sum" && !t.prod.div && t.prod.fs[0].terms.length > 1
      ? t.prod.fs[0].terms.map((u) => ({ sign: t.sign * u.sign, prod: u.prod })) : [t])) };
    if (tree.terms.some((t) => t.prod.fs.some((x) => x.k === "num" && x.v === 0))) return { acts: [], why: "0" };
    // 수 하나뿐인 줄(「5개」 · 「1」)은 셀 것을 찾을 때만
    if (tree.terms.length === 1 && tree.terms[0].prod.fs.length === 1 && tree.terms[0].prod.fs[0].k === "num") {
      const v = tree.terms[0].prod.fs[0].v;
      const lb = `${lab0} ${tree.terms[0].prod.fs[0].lab}`.trim();
      const p = bestPool(pools, v, lb, ctx);
      if (p && p.keys[0] !== "*" && lb) return { acts: [{ type: "count", ids: p.ids, val: v, tag: p.tag }] };
      return { acts: [], why: "수 하나" };
    }
    // 합의 법칙: 수만 더하는 줄이면 무리마다 짚어 세기
    const plainSum = tree.terms.length > 1 && tree.terms.every((t) => t.sign > 0 && t.prod.fs.length === 1 && t.prod.fs[0].k === "num" && !t.prod.div);
    if (plainSum) {
      const used = new Set(), acts = [];
      for (const t of tree.terms) {
        const nf = t.prod.fs[0];
        const p = bestPool(pools, nf.v, `${lab0} ${nf.lab}`, ctx, used);
        if (!p) return { acts: [], why: `합 ${nf.v} 못 찾음` };
        p.ids.forEach((j) => used.add(j));
        acts.push({ type: "count", ids: p.ids, val: nf.v, tag: p.tag });
      }
      return { acts };
    }
    const acts = [];
    let slot = 0, expect = 0;
    const all = objs.map((o) => o.j);
    for (let ti = 0; ti < tree.terms.length; ti++) {
      const t = tree.terms[ti];
      const st = { inner: false, lab0: ti === 0 ? lab0 : "", used: new Set(), picked: new Set(), all };
      if (/학년 \d명:$/.test(lab0)) return { acts: [], why: "경우 나눔(조합 수)" };
      const got = resolveProd(t.prod, pools, { ...ctx, flip: t.sign < 0 }, st);
      if (!got) return { acts: [], why: `곱 ${ti + 1} 못 맞춤` };
      const picks = got.picks;
      expect += t.sign * evalTree(t.prod);
      if (ti > 0) { acts.push({ type: "clear", sign: t.sign }); slot = 0; }
      const picked = new Set();
      for (const p of picks) {
        if (p.one) continue;
        if (p.arrange) { acts.push({ type: "arrange", k: p.arrange, slot0: 0 }); continue; }
        const left = p.back ? p.pool.ids.slice() : p.pool.ids.filter((j) => !picked.has(j));
        const got = p.back ? Array.from({ length: p.k }, () => left[left.length - 1]) : left.slice(-p.k).reverse();
        if (!p.back) got.forEach((j) => picked.add(j));
        acts.push({ type: "pick", pool: { ...p.pool, ids: left }, k: p.k, div: p.div, slot0: slot, got, back: !!p.back });
        slot += p.k;
      }
    }
    return { acts, expect };
  });
  // 그림에 slow 가 있으면(개념 설명의 움직이는 예시) 짚는 박자를 그만큼 천천히
  if (f.slow) for (const L of lines) for (const a of L.acts) a.slow = f.slow;
  const out = { objs, lines };
  PLANS.set(it, out);
  return out;
}

/* ══════════ 박자 ══════════ */
export const PICK_T = { START: 260, TOUCH_MIN: 70, TOUCH_MAX: 165, TOUCH_ALL: 900, FLY: 420, STAMP: 240, POOL: 320, UNORDER: 1050, CLEAR: 520, LIST: 340, PAIR: 520, ALL: 900, TAIL: 300 };
export const touchTick = (n) => Math.max(PICK_T.TOUCH_MIN, Math.min(PICK_T.TOUCH_MAX, PICK_T.TOUCH_ALL / Math.max(1, n)));
export function pickActMs(a) {
  switch (a.type) {
    case "count": return PICK_T.POOL + a.ids.length * touchTick(a.ids.length) * (a.slow || 1) + PICK_T.STAMP;
    case "pick": {
      let d = PICK_T.POOL;
      for (let q = 0; q < a.k; q++) { const n = a.pool.ids.length - q; d += n * touchTick(n) * (a.slow || 1) + PICK_T.FLY + PICK_T.STAMP; }
      return d + (a.div ? PICK_T.UNORDER : 0);
    }
    case "clear": return PICK_T.CLEAR;
    case "arrange": return PICK_T.UNORDER + 250;
    case "list": return a.ids.length * PICK_T.LIST + PICK_T.STAMP;
    case "pairs": return a.pairs.length * PICK_T.PAIR + PICK_T.STAMP;
    case "all": return PICK_T.ALL;
    default: return 0;
  }
}
export function pickPrep(it) {
  if (!it.fig || (it.fig.kind !== "grades" && it.fig.kind !== "bag")) return;
  const { lines } = pickPlan(it);
  lines.forEach((L, i) => {
    if (!L.acts.length) return;
    const ln = it.lines[i];
    const need = PICK_T.START + L.acts.reduce((s, a) => s + pickActMs(a), 0) + PICK_T.TAIL;
    const len0 = lineLen({ ...ln, hold: 0 }), body = lineLen({ ...ln, hold: 0, memo: null });
    ln.hold = len0 >= need ? 0 : Math.max(0, Math.round(need - body));
  });
}
const TIMES = new WeakMap();
/** 움직임마다 t0 · t1 과 그 안의 박자(pick 은 자리마다 [세기 시작, 날기 시작, 찍기 끝]) */
export function pickTimes(it, P) {
  if (TIMES.has(it)) return TIMES.get(it);
  const { lines } = pickPlan(it);
  const acts = [];
  lines.forEach((L, i) => {
    if (!L.acts.length || !P.lines[i]) return;
    let c = P.lines[i].a + PICK_T.START;
    for (const a of L.acts) {
      const d = pickActMs(a), A = { ...a, line: i, t0: c, t1: c + d };
      if (a.type === "pick") {
        let u = c + PICK_T.POOL;
        A.steps = [];
        for (let q = 0; q < a.k; q++) {
          const n = a.pool.ids.length - q, tick = touchTick(n) * (a.slow || 1);
          A.steps.push({ q, n, tick, c0: u, fly: u + n * tick, end: u + n * tick + PICK_T.FLY + PICK_T.STAMP });
          u = A.steps[q].end;
        }
        A.un = a.div ? [u, u + PICK_T.UNORDER] : null;
      }
      acts.push(A);
      c += d;
    }
  });
  const out = { acts };
  TIMES.set(it, out);
  return out;
}
/** 문항에 쓰는 자리 칸 수(가장 많이 뽑는 줄) */
export function slotsOf(it) {
  const { lines } = pickPlan(it);
  let m = 0;
  for (const L of lines) for (const a of L.acts) if (a.type === "pick") m = Math.max(m, a.slot0 + a.k);
  return m;
}
