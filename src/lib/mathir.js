// ashrain.out — MathIR 파서·렌더·평가기 (mathir.js, v1.0 / 스펙 v1.1 구현)
// 위치: src/lib/mathir.js — 앱(ItemCard·검토·코퍼스 화면)과 api/transcribeJob(러너 v2)이 공유.
// 파이썬 itemfactory/mathir.py 와 동형 — 함수표·문법·표시 규칙을 항상 함께 수정할 것.

// ---------------------------------------------------------------- 함수표 (단일 원천)
export const FUNCS = {
  frac:[2,2,"m1"], mixed:[3,3,"m1"], pow:[2,2,"m1"], sqrt:[1,1,"m3"], root:[2,2,"m3"],
  abs:[1,1,"m1"], recdec:[2,2,"m2"], floor:[1,1,"h1"], fact:[1,1,"h1"],
  max:[2,2,"m1"], min:[2,2,"m1"], ratio:[2,3,"m1"], pct:[1,1,"m1"],
  deg:[1,1,"m1"], dms:[2,3,"m1"], pm:[1,2,"m1"],
  seg:[1,1,"m1"], line:[1,1,"m1"], ray:[1,1,"m1"], arc:[1,1,"m1"],
  angle:[1,1,"m1"], tri:[1,1,"m1"], quad:[1,1,"m1"], par:[2,2,"m1"], perp:[2,2,"m1"],
  cong:[2,2,"m2"], sim:[2,2,"m2"], point:[2,2,"m1"], point3:[3,3,"h3"],
  vec:[1,1,"h3"], vcomp:[2,3,"h3"], dot:[2,2,"h3"],
  set:[0,99,"h1"], setb:[2,2,"h1"], in:[2,2,"h1"], notin:[2,2,"h1"],
  subset:[2,2,"h1"], nsubset:[2,2,"h1"], union:[2,2,"h1"], inter:[2,2,"h1"],
  comp:[1,2,"h1"], card:[1,1,"h1"], imp:[2,2,"h1"], iff:[2,2,"h1"], neg:[1,1,"h1"],
  itv:[3,3,"h1"], conj:[1,1,"h1"],
  log:[1,2,"h2"], ln:[1,1,"h3"],
  sin:[1,1,"h2"], cos:[1,1,"h2"], tan:[1,1,"h2"], csc:[1,1,"h2"], sec:[1,1,"h2"], cot:[1,1,"h2"],
  sub:[2,2,"h2"], sum:[4,4,"h2"], lim:[3,4,"h2"], prime:[1,2,"h2"], dydx:[2,2,"h2"],
  integ:[2,2,"h3"], dinteg:[4,4,"h3"], inv:[1,1,"h1"],
  perm:[2,2,"h1"], comb:[2,2,"h1"], pperm:[2,2,"h1"], hcomb:[2,2,"h1"],
  prob:[1,1,"h3"], cprob:[2,2,"h3"], ev:[1,1,"h3"], var:[1,1,"h3"], sd:[1,1,"h3"],
  binomd:[2,2,"h3"], normald:[2,2,"h3"],
};
const CONSTS = { pi: Math.PI, e: Math.E, inf: Infinity, empty: null, i: null };
const GREEK = new Set(["alpha","beta","gamma","delta","theta","lam","mu","omega","phi"]);
export const GRADE_ORD = { m1:1, m2:2, m3:3, h1:4, h2:5, h3:6 };
const LABEL_FNS = new Set(["seg","line","ray","arc","angle","tri","quad","vec"]);

export const FIGS = {
  numline:["min","max"], coordplane:["x","y"], table:["rows"], hist:["bins","counts"],
  stemleaf:["stems"], crossing:["angles"], parallel:["angles"], tri:["v"], rect:["w","h"],
  polygon:["n"], circle:["r"], sector:["r","angle"], solid:["kind"], net:["kind"],
  boxplot:["values"], scatter:["points"], venn:["sets"], tree:["levels"],
  funcgraph:["expr"], unitcircle:[], conic:["kind"], vecfig:["vectors"], space:[],
  normcurve:["m","v"], unsupported:["raw"],
};

export class MathIRError extends Error {
  constructor(code, msg, pos) { super(`${code}: ${msg}` + (pos != null ? ` @${pos}` : "")); this.code = code; this.pos = pos; }
}

// ---------------------------------------------------------------- 유리수 (BigInt)
function bgcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) { [a, b] = [b, a % b]; } return a; }
export class Frac {
  constructor(n, d = 1n) {
    n = BigInt(n); d = BigInt(d);
    if (d === 0n) throw new MathIRError("V-03", "0으로 나눔");
    if (d < 0n) { n = -n; d = -d; }
    const g = bgcd(n, d) || 1n;
    this.n = n / g; this.d = d / g;
  }
  static fromDecimal(s) {
    if (!s.includes(".")) return new Frac(BigInt(s));
    const [a, b] = s.split(".");
    return new Frac(BigInt(a + b) * (a.startsWith("-") && BigInt(a) === 0n ? -1n : 1n), 10n ** BigInt(b.length));
  }
  add(o) { return new Frac(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Frac(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Frac(this.n * o.n, this.d * o.d); }
  div(o) { return new Frac(this.n * o.d, this.d * o.n); }
  neg() { return new Frac(-this.n, this.d); }
  abs() { return new Frac(this.n < 0n ? -this.n : this.n, this.d); }
  powInt(k) {
    let b = this, r = new Frac(1n);
    const neg = k < 0; k = Math.abs(k);
    for (let j = 0; j < k; j++) r = r.mul(b);
    return neg ? new Frac(1n).div(r) : r;
  }
  eq(o) { return this.n === o.n && this.d === o.d; }
  cmp(o) { const L = this.n * o.d, R = o.n * this.d; return L < R ? -1 : L > R ? 1 : 0; }
  toNumber() { return Number(this.n) / Number(this.d); }
}
const isFrac = (v) => v instanceof Frac;
export function close(a, b, tol = 1e-9) {
  if (isFrac(a) && isFrac(b)) return a.eq(b);
  const A = isFrac(a) ? a.toNumber() : a, B = isFrac(b) ? b.toNumber() : b;
  return Math.abs(A - B) <= tol * Math.max(1, Math.abs(A), Math.abs(B));
}

// ---------------------------------------------------------------- 토크나이저·파서
const OPMAP = { "<=": "≤", ">=": "≥", "!=": "≠", "*": "×", "/": "÷" };
function lex(src) {
  const s = src.replace(/−/g, "-").replace(/×/g, "*").replace(/÷/g, "/")
               .replace(/≤/g, "<=").replace(/≥/g, ">=").replace(/≠/g, "!=");
  const out = []; let i = 0;
  const re = /(\d+\.\d+|\d+)|([A-Za-z]+)|(<=|>=|!=|[=<>+\-*/(),|])|(\s+)/y;
  while (i < s.length) {
    re.lastIndex = i;
    const m = re.exec(s);
    if (!m) throw new MathIRError("V-01", `허용되지 않는 문자 '${s[i]}'`, i);
    i = re.lastIndex;
    if (m[4]) continue;
    if (m[1]) out.push(["num", m[1], m.index]);
    else if (m[2]) out.push(["id", m[2], m.index]);
    else out.push(["op", OPMAP[m[3]] || m[3], m.index]);
  }
  return out;
}

class P {
  constructor(toks) { this.t = toks; this.i = 0; this.maxGrade = 0; }
  peek() { return this.t[this.i] || [null, null, null]; }
  take() { return this.t[this.i++] || [null, null, null]; }
  expect(v) { const [, got, p] = this.take(); if (got !== v) throw new MathIRError("V-01", `'${v}' 필요, '${got}' 발견`, p); }
  parse() {
    const n = this.rel();
    if (this.i < this.t.length) throw new MathIRError("V-01", `잉여 토큰 '${this.peek()[1]}'`, this.peek()[2]);
    return n;
  }
  rel() {
    const first = this.add(); const parts = [first], ops = [];
    while (["=", "<", ">", "≤", "≥", "≠"].includes(this.peek()[1])) { ops.push(this.take()[1]); parts.push(this.add()); }
    return ops.length ? { t: "rel", ops, args: parts } : first;
  }
  add() {
    let n = this.mul();
    while (this.peek()[1] === "+" || this.peek()[1] === "-") { const op = this.take()[1]; n = { t: "bin", op, a: n, b: this.mul() }; }
    return n;
  }
  mul() {
    let n = this.unary();
    for (;;) {
      const [k, v, p] = this.peek();
      if (v === "×" || v === "÷") { this.take(); n = { t: "bin", op: v, a: n, b: this.unary() }; }
      else if (k === "num" || k === "id" || v === "(") {
        if (k === "num" && n.t === "num") throw new MathIRError("V-01", "숫자 병치 불가", p);
        n = { t: "bin", op: "×", a: n, b: this.unary() };
      } else return n;
    }
  }
  unary() { if (this.peek()[1] === "-") { this.take(); return { t: "neg", a: this.unary() }; } return this.primary(); }
  primary() {
    const [k, v, p] = this.take();
    if (v === "(") { const inner = this.rel(); this.expect(")"); return { t: "paren", a: inner }; }
    if (k === "num") return { t: "num", v };
    if (k === "id") {
      if (this.peek()[1] === "(") return this.call(v, p);
      if (v in CONSTS) return { t: "const", v };
      if (v.length === 1 || GREEK.has(v)) return { t: "var", v };
      throw new MathIRError("V-01", `미지의 식별자 '${v}'`, p);
    }
    throw new MathIRError("V-01", `예상치 못한 토큰 '${v}'`, p);
  }
  call(name, pos) {
    this.expect("(");
    const args = [];
    if (this.peek()[1] !== ")") {
      for (;;) {
        if (LABEL_FNS.has(name) && this.peek()[0] === "id") args.push({ t: "label", v: this.take()[1] });
        else if (name === "lim" && args.length === 3 && (this.peek()[1] === "+" || this.peek()[1] === "-")) args.push({ t: "label", v: this.take()[1] });
        else if (name === "itv" && args.length === 2) args.push({ t: "label", v: this.take()[1] });
        else args.push(this.rel());
        if (this.peek()[1] === ",") { this.take(); continue; }
        break;
      }
    }
    this.expect(")");
    if (name in FUNCS) {
      const [lo, hi, grade] = FUNCS[name];
      if (args.length < lo || args.length > hi) throw new MathIRError("V-02", `${name} 인자 ${args.length}개 — 허용 ${lo}~${hi}`, pos);
      this.maxGrade = Math.max(this.maxGrade, GRADE_ORD[grade]);
      return { t: "fn", f: name, args };
    }
    if (name.length === 1) { this.maxGrade = Math.max(this.maxGrade, GRADE_ORD.h1); return { t: "apply", f: name, args }; }
    throw new MathIRError("V-01", `미지의 함수 '${name}'`, pos);
  }
}
export function parse(src) { const p = new P(lex(src)); return [p.parse(), p.maxGrade]; }

// ---------------------------------------------------------------- 정식 직렬화 · 표시
export function toIR(n) {
  switch (n.t) {
    case "num": case "var": case "const": case "label": return n.v;
    case "neg": return "-" + toIR(n.a);
    case "paren": return "(" + toIR(n.a) + ")";
    case "bin": return toIR(n.a) + { "×": " × ", "÷": " ÷ ", "+": " + ", "-": " - " }[n.op] + toIR(n.b);
    case "rel": { let s = toIR(n.args[0]); n.ops.forEach((op, k) => { s += ` ${op} ` + toIR(n.args[k + 1]); }); return s; }
    case "fn": case "apply": return n.f + "(" + n.args.map(toIR).join(", ") + ")";
    default: throw new MathIRError("V-04", "직렬화 불가 " + n.t);
  }
}

const SUP = { "0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹","-":"⁻" };
const SUB = { "0":"₀","1":"₁","2":"₂","3":"₃","4":"₄","5":"₅","6":"₆","7":"₇","8":"₈","9":"₉" };
const sup = (s) => [...s].map((c) => SUP[c] || c).join("");
const subs = (s) => [...s].map((c) => SUB[c] || c).join("");
const over = (s, mk) => [...s].map((c) => c + mk).join("");
const ATOM = new Set(["num","var","const","label","fn","apply","paren"]);
const wrap = (n) => ATOM.has(n.t) ? disp(n) : "(" + disp(n) + ")";

export function disp(n) {
  const t = n.t;
  if (t === "num") return n.v;
  if (t === "const") return { pi:"π", e:"e", inf:"∞", i:"i", empty:"∅" }[n.v];
  if (t === "var" || t === "label") return n.v;
  if (t === "neg") return "−" + wrap(n.a);
  if (t === "paren") return "(" + disp(n.a) + ")";
  if (t === "bin") {
    if (n.op === "×") {
      const joinless = ["var","fn","apply","paren","const"].includes(n.b.t) && ["num","var"].includes(n.a.t);
      return joinless ? wrap(n.a) + disp(n.b) : wrap(n.a) + " × " + wrap(n.b);
    }
    if (n.op === "÷") return wrap(n.a) + " ÷ " + wrap(n.b);
    const op = n.op === "-" ? "−" : n.op;
    return disp(n.a) + ` ${op} ` + (n.b.t === "neg" ? wrap(n.b) : disp(n.b));
  }
  if (t === "rel") { let s = disp(n.args[0]); n.ops.forEach((op, k) => { s += ` ${op} ` + disp(n.args[k + 1]); }); return s; }
  if (t === "apply") return n.f + "(" + n.args.map(disp).join(", ") + ")";
  const f = n.f, a = n.args, D = disp;
  const lab = () => a.map(D).join("");
  switch (f) {
    case "frac": return wrap(a[0]) + "/" + wrap(a[1]);
    case "mixed": return D(a[0]) + " " + D(a[1]) + "/" + D(a[2]);
    case "pow": { const ex = toIR(a[1]).replace(/ /g, ""); return wrap(a[0]) + (/^-?\d+$/.test(ex) ? sup(ex) : "^(" + D(a[1]) + ")"); }
    case "sqrt": return "√" + wrap(a[0]);
    case "root": return sup(toIR(a[0])) + "√" + wrap(a[1]);
    case "abs": return "|" + D(a[0]) + "|";
    case "recdec": { const r = D(a[1]); return D(a[0]) + (r.length > 1 ? r[0] + "\u0307" + r.slice(1, -1) + r[r.length - 1] + "\u0307" : r + "\u0307"); }
    case "floor": return "[" + D(a[0]) + "]";
    case "fact": return wrap(a[0]) + "!";
    case "max": case "min": return f + "(" + D(a[0]) + ", " + D(a[1]) + ")";
    case "ratio": return a.map(D).join(" : ");
    case "pct": return D(a[0]) + "%";
    case "deg": return D(a[0]) + "°";
    case "dms": return D(a[0]) + "°" + D(a[1]) + "′" + (a[2] ? D(a[2]) + "″" : "");
    case "pm": return a.length === 1 ? "±" + wrap(a[0]) : wrap(a[0]) + " ± " + wrap(a[1]);
    case "seg": case "line": return over(lab(), "\u0305");
    case "ray": case "vec": return over(lab(), "\u20d7");
    case "arc": return over(lab(), "\u0361");
    case "angle": return "∠" + lab();
    case "tri": return "△" + lab();
    case "quad": return "□" + lab();
    case "par": return D(a[0]) + " ∥ " + D(a[1]);
    case "perp": return D(a[0]) + " ⊥ " + D(a[1]);
    case "cong": return D(a[0]) + " ≡ " + D(a[1]);
    case "sim": return D(a[0]) + " ∽ " + D(a[1]);
    case "point": case "point3": case "vcomp": return "(" + a.map(D).join(", ") + ")";
    case "dot": return D(a[0]) + " · " + D(a[1]);
    case "set": return "{" + a.map(D).join(", ") + "}";
    case "setb": return "{" + D(a[0]) + " | " + D(a[1]) + "}";
    case "in": return D(a[0]) + " ∈ " + D(a[1]);
    case "notin": return D(a[0]) + " ∉ " + D(a[1]);
    case "subset": return D(a[0]) + " ⊂ " + D(a[1]);
    case "nsubset": return D(a[0]) + " ⊄ " + D(a[1]);
    case "union": return D(a[0]) + " ∪ " + D(a[1]);
    case "inter": return D(a[0]) + " ∩ " + D(a[1]);
    case "comp": return a.length === 1 ? wrap(a[0]) + "ᶜ" : D(a[0]) + "∘" + D(a[1]);
    case "card": return "n(" + D(a[0]) + ")";
    case "imp": return D(a[0]) + " → " + D(a[1]);
    case "iff": return D(a[0]) + " ↔ " + D(a[1]);
    case "neg": return "~" + wrap(a[0]);
    case "itv": { const br = { cc:"[]", co:"[)", oc:"(]", oo:"()" }[a[2].v]; return br[0] + D(a[0]) + ", " + D(a[1]) + br[1]; }
    case "conj": return over(D(a[0]), "\u0305");
    case "log": {
      if (a.length === 1) return "log " + wrap(a[0]);
      const b = toIR(a[0]);
      return (/^\d+$/.test(b) ? "log" + subs(b) : "log_(" + D(a[0]) + ")") + " " + wrap(a[1]);
    }
    case "ln": return "ln " + wrap(a[0]);
    case "sin": case "cos": case "tan": case "csc": case "sec": case "cot": return f + " " + wrap(a[0]);
    case "sub": { const ix = toIR(a[1]).replace(/ /g, ""); return D(a[0]) + (/^\d+$/.test(ix) ? subs(ix) : "_" + wrap(a[1])); }
    case "sum": return "Σ[" + D(a[0]) + "=" + D(a[1]) + ".." + D(a[2]) + "] " + wrap(a[3]);
    case "lim": { const side = a[3] ? (a[3].v === "+" ? "⁺" : "⁻") : ""; return "lim[" + D(a[0]) + "→" + D(a[1]) + side + "] " + wrap(a[2]); }
    case "prime": return wrap(a[0]) + (a.length === 1 || toIR(a[1]) === "1" ? "′" : "″");
    case "dydx": return "d" + D(a[0]) + "/d" + D(a[1]);
    case "integ": return "∫ " + D(a[0]) + " d" + D(a[1]);
    case "dinteg": return "∫[" + D(a[0]) + ".." + D(a[1]) + "] " + D(a[2]) + " d" + D(a[3]);
    case "inv": return wrap(a[0]) + "⁻¹";
    case "perm": case "comb": case "pperm": case "hcomb": {
      const L = { perm:"P", comb:"C", pperm:"Π", hcomb:"H" }[f];
      const x = toIR(a[0]), y = toIR(a[1]);
      return /^\d+$/.test(x) && /^\d+$/.test(y) ? subs(x) + L + subs(y) : x + L + y;
    }
    case "prob": return "P(" + D(a[0]) + ")";
    case "cprob": return "P(" + D(a[0]) + " | " + D(a[1]) + ")";
    case "ev": return "E(" + D(a[0]) + ")";
    case "var": return "V(" + D(a[0]) + ")";
    case "sd": return "σ(" + D(a[0]) + ")";
    case "binomd": return "B(" + D(a[0]) + ", " + D(a[1]) + ")";
    case "normald": return "N(" + D(a[0]) + ", " + D(a[1]) + ")";
    default: return toIR(n);
  }
}

// ---------------------------------------------------------------- 평가기
export function ev(n, env = {}) {
  const t = n.t;
  if (t === "num") return Frac.fromDecimal(n.v);
  if (t === "var") { if (n.v in env) return env[n.v]; throw new MathIRError("V-03", "미지 변수 " + n.v); }
  if (t === "const") { const v = CONSTS[n.v]; if (v == null) throw new MathIRError("V-03", "평가 불가 상수 " + n.v); return v; }
  if (t === "paren") return ev(n.a, env);
  if (t === "neg") { const v = ev(n.a, env); return isFrac(v) ? v.neg() : -v; }
  if (t === "bin") {
    const A = ev(n.a, env), B = ev(n.b, env);
    if (isFrac(A) && isFrac(B)) return { "+": A.add(B), "-": A.sub(B), "×": A.mul(B), "÷": A.div(B) }[n.op];
    const x = isFrac(A) ? A.toNumber() : A, y = isFrac(B) ? B.toNumber() : B;
    return { "+": x + y, "-": x - y, "×": x * y, "÷": x / y }[n.op];
  }
  if (t === "fn") {
    const f = n.f, a = n.args, E = (k) => ev(a[k], env);
    const num = (v) => (isFrac(v) ? v.toNumber() : v);
    switch (f) {
      case "frac": return E(0) instanceof Frac && E(1) instanceof Frac ? E(0).div(E(1)) : num(E(0)) / num(E(1));
      case "mixed": return E(0).add(E(1).div(E(2)));
      case "pow": { const b = E(0), x = E(1); if (isFrac(b) && isFrac(x) && x.d === 1n) return b.powInt(Number(x.n)); return Math.pow(num(b), num(x)); }
      case "sqrt": return Math.sqrt(num(E(0)));
      case "root": return Math.pow(num(E(1)), 1 / num(E(0)));
      case "abs": { const v = E(0); return isFrac(v) ? v.abs() : Math.abs(v); }
      case "recdec": {
        const pre = toIR(a[0]), rep = toIR(a[1]);
        const base = Frac.fromDecimal(pre);
        const dec = pre.includes(".") ? pre.split(".")[1].length : 0;
        return base.add(new Frac(BigInt(rep), (10n ** BigInt(rep.length) - 1n) * 10n ** BigInt(dec)));
      }
      case "floor": return new Frac(BigInt(Math.floor(num(E(0)))));
      case "fact": { let r = 1n; for (let k = 2n; k <= BigInt(Math.trunc(num(E(0)))); k++) r *= k; return new Frac(r); }
      case "max": { const A = E(0), B = E(1); return (isFrac(A) && isFrac(B) ? A.cmp(B) >= 0 : num(A) >= num(B)) ? A : B; }
      case "min": { const A = E(0), B = E(1); return (isFrac(A) && isFrac(B) ? A.cmp(B) <= 0 : num(A) <= num(B)) ? A : B; }
      case "pct": return E(0) instanceof Frac ? E(0).div(new Frac(100n)) : num(E(0)) / 100;
      case "deg": return E(0);
      case "dms": { let v = E(0).add(E(1).div(new Frac(60n))); if (a[2]) v = v.add(ev(a[2], env).div(new Frac(3600n))); return v; }
      case "log": return a.length === 1 ? Math.log10(num(E(0))) : Math.log(num(E(1))) / Math.log(num(E(0)));
      case "ln": return Math.log(num(E(0)));
      case "sin": return Math.sin(num(E(0)));
      case "cos": return Math.cos(num(E(0)));
      case "tan": return Math.tan(num(E(0)));
      case "perm": { const N = Math.trunc(num(E(0))), R = Math.trunc(num(E(1))); let r = 1n; for (let k = 0; k < R; k++) r *= BigInt(N - k); return new Frac(r); }
      case "comb": { const N = Math.trunc(num(E(0))), R = Math.trunc(num(E(1))); let r = 1n; for (let k = 1n; k <= BigInt(R); k++) r = r * BigInt(N) - 0n, r = r; let up = 1n, dn = 1n; for (let k = 0; k < R; k++) { up *= BigInt(N - k); dn *= BigInt(k + 1); } return new Frac(up, dn); }
      case "pperm": { const N = BigInt(Math.trunc(num(E(0)))), R = Math.trunc(num(E(1))); let r = 1n; for (let k = 0; k < R; k++) r *= N; return new Frac(r); }
      case "hcomb": { const N = Math.trunc(num(E(0))), R = Math.trunc(num(E(1))); let up = 1n, dn = 1n; for (let k = 0; k < R; k++) { up *= BigInt(N + R - 1 - k); dn *= BigInt(k + 1); } return new Frac(up, dn); }
      case "sum": {
        const kk = a[0].v; let lo = Math.trunc(num(ev(a[1], env))), hi = Math.trunc(num(ev(a[2], env)));
        let acc = new Frac(0n), fl = null;
        for (let kv = lo; kv <= hi; kv++) {
          const v = ev(a[3], { ...env, [kk]: new Frac(BigInt(kv)) });
          if (isFrac(v) && fl === null) acc = acc.add(v);
          else { fl = (fl ?? acc.toNumber()) + num(v); }
        }
        return fl ?? acc;
      }
      default: break;
    }
  }
  throw new MathIRError("V-03", "평가 불가 노드 " + (n.f || t));
}

// ---------------------------------------------------------------- 혼합문·검증 진입점
const MARK = /\[\[([\s\S]*?)\]\]/g;
export function parseText(text, gradeHint = null) {
  const segs = [], errs = []; let mg = 0, last = 0, m;
  MARK.lastIndex = 0;
  while ((m = MARK.exec(text))) {
    if (m.index > last) segs.push({ kind: "text", raw: text.slice(last, m.index) });
    const src = m[1].trim();
    try {
      const [node, g] = parse(src);
      const [rt] = parse(toIR(node));
      if (toIR(rt) !== toIR(node)) errs.push({ code: "V-04", src });
      segs.push({ kind: "ir", raw: src, node, ir: toIR(node), disp: disp(node) });
      mg = Math.max(mg, g);
    } catch (e) {
      errs.push({ code: e.code || "V-01", src, msg: String(e.message || e) });
      segs.push({ kind: "text", raw: m[0] });
    }
    last = MARK.lastIndex;
  }
  if (last < text.length) segs.push({ kind: "text", raw: text.slice(last) });
  if (gradeHint && mg > (GRADE_ORD[gradeHint.slice(0, 2)] || 9)) errs.push({ code: "V-09", msg: `학년 힌트 ${gradeHint} 초과 문법` });
  return { segs, maxGrade: mg, errs };
}
export function renderText(text) {
  return parseText(text).segs.map((s) => (s.kind === "ir" ? s.disp : s.raw)).join("");
}
export function parseAnswer(s) {
  s = s.trim();
  try { const [node] = parse(s); return { kind: "ir", node }; }
  catch (e) {
    if (/^[가-힣A-Za-z0-9 ,·~]+$/.test(s)) return { kind: "word", v: s };
    throw e;
  }
}
export function checkEquationAnswer(questionText, answerStr) {
  try {
    const ans = parseAnswer(answerStr);
    if (ans.kind !== "ir") return null;
    let varName = null, valNode = ans.node;
    if (ans.node.t === "rel" && ans.node.ops.length === 1 && ans.node.ops[0] === "=" && ans.node.args[0].t === "var") {
      varName = ans.node.args[0].v; valNode = ans.node.args[1];
    }
    if (!varName) return null;
    const val = ev(valNode);
    const { segs, errs } = parseText(questionText);
    if (errs.length) return null;
    const rels = segs.filter((s) => s.kind === "ir" && s.node.t === "rel" && s.node.ops.includes("=")).map((s) => s.node);
    if (!rels.length) return null;
    const oks = [];
    for (const r of rels) {
      try {
        const vals = r.args.map((p) => ev(p, { [varName]: val }));
        let ok = true;
        for (let k = 0; k + 1 < vals.length; k++) if (!close(vals[k], vals[k + 1])) ok = false;
        oks.push(ok);
      } catch { /* 평가 불가 세그먼트는 건너뜀 */ }
    }
    return oks.length ? oks.every(Boolean) : null;
  } catch { return null; }
}
export function checkFigure(figList) {
  const errs = [];
  (figList || []).forEach((f, i) => {
    if (!(f.fn in FIGS)) { errs.push({ code: "V-05", i, msg: "미지 도형 함수 " + f.fn }); return; }
    for (const k of FIGS[f.fn]) if (!(k in (f.args || {}))) errs.push({ code: "V-05", i, msg: `${f.fn}.${k} 누락` });
  });
  return errs;
}
