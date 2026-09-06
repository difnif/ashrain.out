// mathir.js v1.5 r2 자가 시험 — 파이썬 mathir.py 하단 자가 시험과 동일 케이스
import { parse, toIR, disp, ev, close, Frac, parseText, renderText, parseAnswer, checkEquationAnswer, checkFigure, MathIRError, GRADE_ORD } from "../../src/lib/mathir.js";
const eq = (a, b, m) => { if (a !== b) throw new Error(`${m}: ${JSON.stringify(a)} !== ${JSON.stringify(b)}`); };
const F = (n, d = 1) => new Frac(BigInt(n), BigInt(d));

const T = [
  ["frac(1,2) + frac(1,3)", "1/2 + 1/3", F(5, 6)],
  ["pow(-2,3) + 10", "(−2)³ + 10", F(2)],
  ["mixed(2,1,3) × 6", null, F(14)],
  ["recdec(0.2,45)", null, F(2, 10).add(F(45, 990))],
  ["fact(5) ÷ fact(3)", null, F(20)],
  ["perm(5,2) + comb(5,2)", "₅P₂ + ₅C₂", F(30)],
  ["hcomb(3,2)", null, F(6)],
  ["sum(k,1,10,k)", null, F(55)],
  ["dms(35,30)", null, F(71, 2)],
];
for (const [src, d, val] of T) {
  const [n] = parse(src); const [rt] = parse(toIR(n));
  eq(toIR(rt), toIR(n), "왕복 " + src);
  if (d) eq(disp(n), d, "표시 " + src);
  if (!close(ev(n), val)) throw new Error("평가 " + src);
}
for (const src of ["log(2,8)", "lim(x,inf,frac(1,x))", "dinteg(0,1,pow(x,2),x)", "sin(frac(pi,6))", "abs(-7)"]) { const [n] = parse(src); parse(toIR(n)); }
if (!close(ev(parse("log(2,8)")[0]), 3)) throw new Error("log");
if (!close(ev(parse("sin(frac(pi,6))")[0]), 0.5)) throw new Error("sin");
{ const r = parseText("일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오."); if (r.errs.length || r.maxGrade !== GRADE_ORD.m1) throw new Error("parseText"); }
eq(renderText("[[pow(x,2) - 4 = 0]]"), "x² − 4 = 0", "renderText");
eq(checkEquationAnswer("일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오.", "x = 8"), true, "check1");
eq(checkEquationAnswer("일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오.", "x = 7"), false, "check2");
eq(checkEquationAnswer("[[3x + 2 = 11]]", "x = 3"), true, "check3");
{ const r = parseText("[[lim(x,0,frac(1,x))]]", "m1"); if (!r.errs.some((e) => e.code === "V-09")) throw new Error("V-09"); }
try { parse("frak(1,2)"); throw new Error("frak"); } catch (e) { if (e.code !== "V-01") throw e; }
try { parse("frac(1)"); throw new Error("frac(1)"); } catch (e) { if (!(e instanceof MathIRError)) throw e; }
if (checkFigure([{ fn: "numline", args: { min: -5, max: 5 } }]).length) throw new Error("fig1");
if (!checkFigure([{ fn: "banana", args: {} }]).length) throw new Error("fig2");
// ---- v1.4 답 표기층
eq(parseAnswer("③").kind, "word", "ans ③"); eq(parseAnswer("ㄱ, ㄴ").kind, "word", "ans ㄱㄴ");
eq(toIR(parseAnswer("21°").node), "deg(21)", "ans deg"); eq(parseAnswer("49.5 kg").unit, "kg", "ans unit");
eq(toIR(parseAnswer("72pi cm³").node), "72 × pi", "ans pi"); eq(parseAnswer("72pi cm³").unit, "cm³", "ans unit2");
eq(parseAnswer("a = 5, b = -1").kind, "set", "ans set"); eq(parseAnswer("[[x = 1]] 또는 [[x = 2]]").items.length, 2, "ans or");
eq(toIR(parseAnswer("좌변: [[x + 3y]]").node), "x + 3 × y", "ans label");
// ---- v1.5
for (const [src, d] of [["cases(pow(3,x) + 1, x <= 1, 9 - 3 log(3,x), x > 1)", "{3^(x) + 1 (x ≤ 1) ; 9 − 3log₃ x (x > 1)}"],
  ["app(prime(f), x)", "f′(x)"], ["app(comp(f, g), x)", "(f∘g)(x)"], ["app(inv(f), 2)", "f⁻¹(2)"],
  ["app(sub(S, 1), t)", "S₁(t)"], ["alpha(t) + beta(t) = 5", "α(t) + β(t) = 5"],
  ["iter(f, 3, x)", "f³(x)"], ["xbar(X)", "X̄"], ["hat(p)", "p̂"], ["box(1)", "□(가)"],
  ["angle(A'PB)", "∠A′PB"], ["tri(P1P2P3)", "△P₁P₂P₃"], ["point3(1, 2, 3)", "(1, 2, 3)"],
  ["sub(a,1) + cdots + sub(a,n)", "a₁ + ⋯ + a_n"], ["sigma", "σ"]]) {
  const [n] = parse(src); const [rt] = parse(toIR(n));
  eq(toIR(rt), toIR(n), "v1.5 왕복 " + src); eq(disp(n), d, "v1.5 표시 " + src);
}
{ const [n] = parse("seg(O1A) = 21"); if (!disp(n).includes("₁") || toIR(parse(toIR(n))[0]) !== toIR(n)) throw new Error("seg(O1A)"); }
try { parse("cases(x, x > 0, y)"); throw new Error("cases odd"); } catch (e) { if (e.code !== "V-02") throw e; }
if (checkFigure([{ fn: "image", args: { src: "figs/x.png", raw: "설명" } }]).length) throw new Error("image ok");
if (!checkFigure([{ fn: "image", args: {} }]).length) throw new Error("image missing src");
{ const r = parseText("[[f(x) = cases(pow(x,2), x < 1, 2x - 1, x >= 1)]]에서 [[app(prime(f), 3)]]의 값은?"); if (r.errs.length) throw new Error("v1.5 text"); }
// ---- v1.5 r2
for (const [src, d] of [["op(dcirc, 2, 3)", "2 ◎ 3"], ["op(star, op(dcirc, 2, 3), 4)", "(2 ◎ 3) ★ 4"],
  ["op(dcirc, a, b) = a b - a + b", "a ◎ b = ab − a + b"], ["op(tri, 2x, y)", "2x △ y"],
  ["nota(angle, x)", "⟨x⟩"], ["nota(lt, a, b)", "<a, b>"], ["nota(brace, 12)", "{12}"], ["nota(sq, a, b)", "[a, b]"],
  ["idx(P, 2)", "P[2]"], ["idx((A - B), 2)", "(A − B)[2]"], ["tr(B)", "Bᵗ"], ["dig(a, b, c, d)", "abcd"],
  ["dig(2, 0, B, 5) - dig(1, B, A, 6) = dig(A, 3, 9)", "20B5 − 1BA6 = A39"],
  ["recdec(0, a0bc)", "0.ȧ0bċ"], ["recdec(0, ab, cd)", "0.abċḋ"], ["recdec(0, 3)", "0.3̇"], ["recdec(0.2, 45)", "0.24̇5̇"],
  ["a' x + b'", "a′x + b′"], ["y = a'' x", "y = a″x"],
  ["2 a b", "2ab"], ["-5x", "−5x"], ["2 sqrt(3) x", "2√3x"], ["9 × pow(2, n+1)", "9 × 2^(n + 1)"], ["(x+1)(x+2)", "(x + 1)(x + 2)"],
  ["-(x+1)(x-2)", "−(x + 1)(x − 2)"], ["4 op(dcirc, a, b)", "4(a ◎ b)"], ["pow(op(dcirc,a,b),2)", "(a ◎ b)²"], ["2 frac(1,3)", "2 × 1/3"]]) {
  const [n] = parse(src); const [rt] = parse(toIR(n));
  eq(toIR(rt), toIR(n), "r2 왕복 " + src); eq(disp(n), d, "r2 표시 " + src);
}
eq(toIR(parse("f'(x)")[0]), "app(prime(f), x)", "f'(x)"); eq(toIR(parse("f''(2)")[0]), "app(prime(f, 2), 2)", "f''(2)");
if (!close(ev(parse("recdec(0, 12, 34)")[0]), F(12, 100).add(F(34, 9900)))) throw new Error("recdec3 ev");
if (!close(ev(parse("dig(4, 3, 5, 8)")[0]), F(4358))) throw new Error("dig ev");
for (const bad of ["op(banana, 1, 2)", "nota(round, x)", "op(star, 1)", "recdec(0, 3", "seg(AB"]) { try { parse(bad); throw new Error("should fail " + bad); } catch (e) { if (!(e instanceof MathIRError)) throw e; } }
try { ev(parse("recdec(0, ab)")[0]); throw new Error("recdec letters ev"); } catch (e) { if (e.code !== "V-03") throw e; }
eq(parseAnswer("㉢").kind, "word", "ans ㉢"); eq(parseAnswer("㉠, ㉣").kind, "word", "ans ㉠㉣");
eq(parseAnswer("+23").sign, "+", "ans +23"); eq(parseAnswer("+3000").kind, "ir", "ans +3000"); if ("sign" in parseAnswer("23")) throw new Error("sign leak");
eq(renderText("[[op(dcirc, op(dcirc, 2, 3), 4)]]의 값은?"), "(2 ◎ 3) ◎ 4의 값은?", "render op");
console.log("mathir.js 자가 시험 전부 통과 (v1.5 r2)");
