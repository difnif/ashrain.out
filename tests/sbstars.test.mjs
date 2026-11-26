// node tests/sbstars.test.mjs — 선빵스타즈(src/features/games/sbstars.html) 문제 · 규칙 검산. 실패 시 exit 1.
//   게임의 <script id="core">(문제 만들기 · 분수 · 직선 고르기 — 화면과 무관한 부분)만 떼어 node 에서 돌린다.
//   1) 일차함수 8꼴 × 난이도 3: 보여 준 점 · 절편 · 평행선 · 평행이동 값이 정답 직선과 맞는지(정수 산술),
//      일반형 식은 화면에 보이는 식 그대로 두 점을 넣어 본다. 동치 분수(4/6)는 받고, 틀린 y절편은 거절.
//   2) 경우의 수 14꼴: 주사위 · 동전 · 카드 · 줄 세우기를 전부 세어 정답과 비교(「배수 또는」은 겹침까지 직접 센다).
//   3) 확률 12꼴: 같은 방식으로 전부 세어 기약분수 비교, 0 < p < 1, 「주사위 눈」 이름과 집합(짝수 · 소수 · 약수 …)이 맞는지.
//   4) 일차방정식 5꼴: 보이는 식에 해를 넣으면 성립하고 해 + 1 은 성립하지 않는다(해가 하나), 탄환 3 ~ 12발.
//   5) 이차방정식 4꼴 + 중근: 보이는 식에 두 근이 성립하고 다른 값은 아니다, 두 근의 차(투척 사거리) 1 ~ 9, 순서 바꿔도 정답.
//   6) 입력 읽기(−2/3 · 0.5 · 2/−3 …), 파스칼 뽑기 × 베르누이 시행(×10 · ×100 비율이 p · pq 에 가까운지, 뽑은 직선이 경기장을 지나는지),
//      직선 고르기(조이스틱 방향 · 내 자리 → 탈 직선, 반대 방향, 허용각 · 붙는 거리 밖, 연료 0).
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(HERE, "../src/features/games/sbstars.html"), "utf8");
const core = html.match(/<script id="core">([\s\S]*?)<\/script>/)[1];
const ctx = {}; vm.createContext(ctx); vm.runInContext(core, ctx);
const SB = ctx.SB;
let seed = 20261126; SB.setRng(() => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; });

let n = 0, failed = 0;
const notes = new Map();
const ok = (c, name, p) => { n++; if (c) return; failed++; const k = name; notes.set(k, (notes.get(k) || 0) + 1); if (notes.get(k) <= 2) console.log("FAIL -", name, p ? "— " + strip(p.html + " " + (p.extra || "")) : ""); };
const strip = (h) => String(h || "").replace(/<span class="fr"><i>([^<]*)<\/i><i>([^<]*)<\/i><\/span>/g, "($1/$2)").replace(/<sup>2<\/sup>/g, "²").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
function toJS(h) {
  let s = h.replace(/<sup>2<\/sup>/g, "^2").replace(/<span class="fr"><i>([^<]*)<\/i><i>([^<]*)<\/i><\/span>/g, "(($1)/($2))").replace(/<[^>]+>/g, "").replace(/−/g, "-").replace(/×/g, "*");
  return s.replace(/x\^2/g, "(x**2)").replace(/\)\^2/g, ")**2").replace(/(\d|\))\s*(?=[xy(])/g, "$1*");
}
const holds = (h, x, y) => { const [L, R] = toJS(h).split("="); const [l, r] = new Function("x", "y", `return [${L},${R}]`)(x, y); return Math.abs(l - r) < 1e-9; };
const { F, feq, fs: fstr } = SB;
const bad = (s) => /undefined|NaN|null|\[object/.test(s);
const range = (k) => Array.from({ length: k }, (_, i) => i + 1);
const pairs = []; for (const i of range(6)) for (const j of range(6)) pairs.push([i, j]);
const perms = (k) => { let c = 0; const rec = (u, d) => { if (d === k) { c++; return; } for (let i = 0; i < k; i++) if (!u[i]) { u[i] = 1; rec(u, d + 1); u[i] = 0; } }; rec([], 0); return c; };
const seen = new Set();

// 1) 일차함수 → 길
for (let tier = 0; tier < 3; tier++) for (let i = 0; i < 3000; i++) {
  const p = SB.genLin(tier, null), { a, b } = p.ans, d = p.data; seen.add("lin." + p.tpl);
  const on = (q) => q.y * a.d === a.n * q.x + b * a.d;
  ok(a.n !== 0 && !bad(p.html + (p.extra || "") + p.reveal + p.hint), "1 일차함수 — 기울기 0 아님 · 글에 빈값 없음", p);
  ok(p.check({ a: fstr(a), b: String(b) }) && p.check({ a: `${2 * a.n}/${2 * a.d}`, b: String(b) }) && !p.check({ a: fstr(a), b: String(b + 1) }), "1 일차함수 — 정답 · 동치 분수는 받고 틀린 절편은 거절", p);
  if (p.tpl === "two") ok(on(d.A) && on(d.B) && !(d.A.x === d.B.x && d.A.y === d.B.y), "1 두 점이 정답 직선 위", p);
  if (p.tpl === "slope" || p.tpl === "par") ok(on(d.P) && (p.tpl !== "par" || d.c !== b), "1 점 P · 평행선", p);
  if (p.tpl === "icpt") ok(d.X !== 0 && a.n * d.X + b * a.d === 0 && d.Y === b, "1 x절편 · y절편", p);
  if (p.tpl === "gen") ok(holds(d.eq, 0, b) && holds(d.eq, a.d, b + a.n) && !holds(d.eq, 0, b + 1), "1 일반형 — 보이는 식에 두 점이 맞고 다른 점은 아님", p);
  if (p.tpl === "shift") ok(b === d.d && b !== 0, "1 y = ax 평행이동", p);
  if (p.tpl === "shift2") ok(b === d.c + d.d && d.d !== 0, "1 y = ax + c 평행이동", p);
  if (p.tpl === "graph") ok(on(d.p2) && Math.abs(d.p2.x) <= 5 && Math.abs(d.p2.y) <= 5 && Math.abs(b) <= 3, "1 그래프 읽기 — 표시한 두 점이 창 안 · 직선 위", p);
}
// 2) 경우의 수 → 파스칼 뽑기
for (let tier = 0; tier < 3; tier++) for (let i = 0; i < 2500; i++) {
  const p = SB.genCnt(tier), d = p.data; seen.add("cnt." + p.tpl);
  const bf = {
    coins: () => 2 ** d.N, coindie: () => 2 ** d.N * 6, clothes: () => d.a * d.b, roads: () => d.a * d.b, trans: () => d.a + d.b,
    dsum: () => pairs.filter(([x, y]) => x + y === d.S).length, dor: () => pairs.filter(([x, y]) => x + y === d.A || x + y === d.B).length,
    ddiff: () => pairs.filter(([x, y]) => Math.abs(x - y) === d.D).length, line: () => perms(d.N), front: () => perms(d.N - 1),
    pres: () => { let c = 0; for (const x of range(d.N)) for (const y of range(d.N)) if (x !== y) c++; return c; },
    pair: () => { let c = 0; for (let x = 0; x < d.N; x++) for (let y = x + 1; y < d.N; y++) c++; return c; },
    league: () => { let c = 0; for (let x = 0; x < d.N; x++) for (let y = x + 1; y < d.N; y++) c++; return c; },
    cards: () => { let c = 0; for (const t of range(d.N)) for (const u of range(d.N)) if (t !== u) c++; return c; },
    cards0: () => { let c = 0; for (let t = 0; t < d.N; t++) for (let u = 0; u < d.N; u++) if (t && t !== u) c++; return c; },
    mult: () => range(d.N).filter((x) => x % d.k === 0 || x % d.m === 0).length,
  }[p.tpl]();
  ok(bf === p.ans, `2 경우의 수 ${p.tpl} — 직접 센 값과 같다`, p);
  ok(p.check({ n: String(p.ans) }) && !p.check({ n: String(p.ans + 1) }) && !bad(p.html + p.reveal + p.hint), "2 경우의 수 — 정답 받기 · 오답 거절 · 글", p);
}
// 3) 확률 → 베르누이 시행
const PRED = { "짝수의 눈": (x) => x % 2 === 0, "홀수의 눈": (x) => x % 2 === 1, "소수의 눈": (x) => [2, 3, 5].includes(x), "3의 배수의 눈": (x) => x % 3 === 0, "4 이상의 눈": (x) => x >= 4, "5 이상의 눈": (x) => x >= 5, "6의 약수의 눈": (x) => 6 % x === 0, "2 이하의 눈": (x) => x <= 2 };
for (const [nm, set] of SB.DIE) ok(JSON.stringify(range(6).filter(PRED[nm])) === JSON.stringify(set), `3 주사위 눈 「${nm}」 집합`);
for (let tier = 0; tier < 3; tier++) for (let i = 0; i < 2500; i++) {
  const p = SB.genPrb(tier), d = p.data; seen.add("prb." + p.tpl);
  const T = d.w + d.k;
  const [num, den] = {
    die: () => [range(6).filter(PRED[d.nm]).length, 6], bag: () => [d.r, d.r + d.b], card: () => [range(d.N).filter((x) => x % d.k === 0).length, d.N],
    coinall: () => [1, 2 ** d.N], coinone: () => [2 ** d.N - 1, 2 ** d.N], dsum: () => [pairs.filter(([x, y]) => x + y === d.S).length, 36],
    dsame: () => [d.v === "same" ? pairs.filter(([x, y]) => x === y).length : pairs.filter(([x, y]) => (x + y) % 2 === 0).length, 36],
    bag3: () => [d.b + d.y, d.r + d.b + d.y], coindie: () => [range(6).filter(PRED[d.nm]).length, 12], rep: () => [d.w * d.w, T * T],
    norep: () => { let c = 0, all = 0; for (let x = 0; x < T; x++) for (let y = 0; y < T; y++) if (x !== y) { all++; if (x < d.w && y < d.w) c++; } return [c, all]; },
    atleast: () => [d.v === "even" ? pairs.filter(([x, y]) => x % 2 === 0 || y % 2 === 0).length : pairs.filter(([x, y]) => x !== y).length, 36],
  }[p.tpl]();
  ok(feq(F(num, den), p.ans) && SB.fv(p.ans) > 0 && SB.fv(p.ans) < 1, `3 확률 ${p.tpl} — 직접 센 값 · 0 < p < 1`, p);
  ok(p.check({ p: `${3 * p.ans.n}/${3 * p.ans.d}` }) && !p.check({ p: `${p.ans.n}/${p.ans.d + 1}` }) && !bad(p.html + p.reveal + p.hint), "3 확률 — 약분 전 분수도 정답 · 오답 거절 · 글", p);
}
// 4) 일차방정식 → 탄환
for (let tier = 0; tier < 3; tier++) for (let i = 0; i < 2500; i++) {
  const p = SB.genEq1(tier), x = p.ans; seen.add("eq1." + p.tpl);
  ok(holds(p.data.eq, x, 0) && !holds(p.data.eq, x + 1, 0), `4 일차방정식 ${p.tpl} — 보이는 식에 해가 맞고 하나뿐`, p);
  ok(Number.isInteger(x) && x >= 3 && x <= 12 && p.check({ x: String(x) }) && !p.check({ x: String(x + 1) }) && !bad(p.extra + p.reveal), "4 탄환 3 ~ 12발 · 정답 받기 · 글", p);
}
// 5) 이차방정식 → 브라마굽타 투척 · 알콰리즈미 충격파
for (let tier = 0; tier < 3; tier++) for (let i = 0; i < 2500; i++) {
  const p = SB.genEq2(tier), [r1, r2] = p.ans; seen.add("eq2." + p.tpl + (p.dbl ? ".중근" : ""));
  const others = [r1 - 1, r2 + 1, (r1 + r2) / 2 + 0.37].filter((t) => t !== r1 && t !== r2);
  ok(holds(p.data.eq, r1, 0) && holds(p.data.eq, r2, 0) && others.every((t) => !holds(p.data.eq, t, 0)), `5 이차방정식 ${p.tpl} — 보이는 식에 두 근만 맞다`, p);
  ok(p.dbl === (r1 === r2) && (p.dbl || (r2 - r1 >= 1 && r2 - r1 <= 9)), "5 중근 표시 · 투척 사거리(두 근의 차) 1 ~ 9", p);
  ok(p.check({ r1: String(r2), r2: String(r1) }) && (p.dbl || !p.check({ r1: String(r1), r2: String(r1) })) && !bad(p.extra + p.reveal + p.hint), "5 근 순서 상관없이 정답 · 한 근만 두 번은 오답", p);
}
// 6) 입력 · 뽑기 · 직선 고르기
for (const [s, a, b] of [["−2/3", -2, 3], ["-4/6", -2, 3], ["2/-3", -2, 3], ["0.5", 1, 2], ["-.25", -1, 4], ["1.5/3", 1, 2], ["3", 3, 1], ["−0", 0, 1]]) { const f = SB.parseNum(s); ok(f && feq(f, F(a, b)), `6 입력 읽기 「${s}」`); }
for (const s of ["", "-", "/", "2/0", "1/2/3", "a", "--2", "."]) ok(!SB.parseNum(s), `6 잘못된 입력 「${s}」 거절`);
let tot = 0, ten = 0, hund = 0;
for (let i = 0; i < 4000; i++) {
  const dr = SB.rollDraws(F(2), 1, 6, [F(1, 2), F(1, 3)]);
  ok(dr.length === 6 && dr[0].b === 1, "6 파스칼 6 → 6번 뽑기, 첫 번째는 정답 직선");
  for (const x of dr) { tot++; if (x.m === 10) ten++; if (x.m === 100) hund++; ok(Number.isInteger(x.b) && (x.b - 1) % 2 === 0 && (x.k === 0 || SB.lineInArena(2, x.b)), "6 뽑은 직선 — 정수 y절편 · 간격 √5 ≈ 2 · 경기장을 지난다"); }
}
ok(Math.abs(ten / tot - 1 / 3) < 0.02 && Math.abs(hund / tot - 1 / 6) < 0.015, `6 베르누이 — ×10 비율 ${(ten / tot).toFixed(3)}(≈ ½ × ⅔) · ×100 비율 ${(hund / tot).toFixed(3)}(≈ ½ × ⅓)`);
ok(SB.rollDraws(F(1, 2), 0, 0, []).length === 1 && SB.rollDraws(F(1, 2), 0, 99, []).length === 30, "6 부스터 없으면 1번, 많아도 30번까지");
const L1 = { n: 1, d: 1, b: 0, fuel: 5 }, L2 = { n: 1, d: 1, b: 1, fuel: 5 }, L3 = { n: -1, d: 2, b: -3, fuel: 5 };
const pickL = (ls, x, y, ang, tol = 35, reach = 1.25) => SB.selectLine(ls, x, y, Math.cos(ang), Math.sin(ang), tol, reach, null, null);
let r = pickL([L1], 0, 0, Math.PI / 4); ok(r.best && r.best.L === L1 && r.best.dist < 1e-9 && r.best.ux > 0, "6 고르기 — 지금 선 위, 같은 방향");
r = pickL([L1], 0, 0, Math.PI * 1.25); ok(r.best && r.best.ux < 0, "6 고르기 — 같은 직선을 반대 방향으로");
r = pickL([L1], 0, 0, 0); ok(!r.best, "6 고르기 — 45° 어긋나면(허용 35°) 못 탄다");
r = pickL([L2], 0, 0, Math.PI / 4); ok(r.best && Math.abs(r.best.fx + 0.5) < 1e-9 && Math.abs(r.best.fy - 0.5) < 1e-9, "6 고르기 — 수선의 발(−½, ½)로 붙는다");
r = pickL([L2], 0, 0, Math.PI / 4, 35, 0.5); ok(!r.best && r.far === L2, "6 고르기 — 붙는 거리 밖이면 「가까운 직선」으로만 알린다");
r = pickL([L1, L3], 2, -4, Math.atan2(-1, 2)); ok(r.best && r.best.L === L3, "6 고르기 — 방향이 맞는 기울기(−½)를 고른다");
r = pickL([{ ...L1, fuel: 0 }], 0, 0, Math.PI / 4); ok(!r.best, "6 고르기 — 연료 0 인 직선은 안 탄다");
const want = ["lin.two", "lin.slope", "lin.par", "lin.icpt", "lin.gen", "lin.shift", "lin.shift2", "lin.graph", "eq2.sq", "eq2.re", "eq2.fac", "eq2.std.중근"];
ok(want.every((k) => seen.has(k)), "모든 꼴이 한 번 이상 나왔다 — " + [...seen].length + "꼴");

for (const [k, c] of notes) if (c > 2) console.log(`      (${k} — 모두 ${c}번)`);
console.log(`\n${n} checks · ${failed} failed`);
process.exit(failed ? 1 : 0);
