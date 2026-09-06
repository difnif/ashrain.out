// ashrain.out — MathIR 파서·렌더·평가기 (mathir.js, v1.5 r2 / 파이썬 itemfactory/mathir.py v1.5 r2 동형)
// 위치: src/lib/mathir.js — 앱(ItemCard·검토·코퍼스 화면)과 api/transcribeJob(러너 v2)이 공유.
// 파이썬 itemfactory/mathir.py 와 동형 — 함수표·문법·표시 규칙을 항상 함께 수정할 것.
// 이력: v1.0(스펙 v1.1) → v1.4 답 표기층(ㄱ~ㅎ·①~⑳ 낱말 답, '21°'→deg, 단위 꼬리, 'a = 5, b = -1' 병립, '좌변:' 접두 제거)
//       → v1.5(cases·app·iter·xbar·hat·box·cdots·sigma·라벨 첨자/프라임·point3 렉서 수정·image/scene 도형)
//       → v1.5 r2(op·nota·idx·tr·dig·문자 recdec·3인자 recdec·변수 프라임 a'·원문자 답·양의 부호 답·표시 수정 3건)
//   v1.4 이하 문법은 전부 그대로 통과하며 IR(toIR)은 바뀌지 않는다. 표시(disp)만 recdec 소수점·곱 병치·op 괄호가 고쳐졌다.

// ---------------------------------------------------------------- 함수표 (단일 원천)
export const FUNCS = {
  frac:[2,2,"m1"], mixed:[3,3,"m1"], pow:[2,2,"m1"], sqrt:[1,1,"m3"], root:[2,2,"m3"],
  abs:[1,1,"m1"], recdec:[2,3,"m2"], floor:[1,1,"h1"], fact:[1,1,"h1"],          // v1.5r2 recdec 3인자형
  max:[2,2,"m1"], min:[2,2,"m1"], ratio:[2,3,"m1"], pct:[1,1,"m1"],
  deg:[1,1,"m1"], dms:[2,3,"m1"], pm:[1,2,"m1"],
  seg:[1,1,"m1"], line:[1,1,"m1"], ray:[1,1,"m1"], arc:[1,1,"m1"],
  angle:[1,1,"m1"], tri:[1,1,"m1"], quad:[1,1,"m1"], par:[2,2,"m1"], perp:[2,2,"m1"],
  cong:[2,2,"m2"], sim:[2,2,"m2"], point:[2,2,"m1"], point3:[3,3,"h3"],
  vec:[1,1,"h3"], vcomp:[2,3,"h3"], dot:[2,2,"h3"],
  set:[0,99,"h1"], setb:[2,2,"h1"], in:[2,2,"h1"], notin:[2,2,"h1"],
  mat:[3,99,"h1"],
  subset:[2,2,"h1"], nsubset:[2,2,"h1"], union:[2,2,"h1"], inter:[2,2,"h1"],
  comp:[1,2,"h1"], card:[1,1,"h1"], imp:[2,2,"h1"], iff:[2,2,"h1"], neg:[1,1,"h1"],
  itv:[3,3,"h1"], conj:[1,1,"h1"],
  log:[1,2,"h2"], ln:[1,1,"h3"],
  sin:[1,1,"h2"], cos:[1,1,"h2"], tan:[1,1,"h2"], csc:[1,1,"h2"], sec:[1,1,"h2"], cot:[1,1,"h2"],
  sub:[2,3,"h1"], sum:[4,4,"h2"], lim:[3,4,"h2"], prime:[1,2,"h2"], dydx:[2,2,"h2"],
  integ:[2,2,"h3"], dinteg:[4,4,"h3"], inv:[1,1,"h1"],
  perm:[2,2,"h1"], comb:[2,2,"h1"], pperm:[2,2,"h1"], hcomb:[2,2,"h1"],
  prob:[1,1,"h3"], cprob:[2,2,"h3"], ev:[1,1,"h3"], var:[1,1,"h3"], sd:[1,1,"h3"],
  binomd:[2,2,"h3"], normald:[2,2,"h3"],
  // v1.5
  cases:[2,8,"h1"],        // 경우 나눔 (식, 조건) 쌍 — 짝수 인자
  app:[2,6,"h1"],          // 파생 함수 적용 app(F, x, …)
  iter:[3,3,"h2"],         // 거듭 합성 fⁿ(x)
  xbar:[1,1,"h3"], hat:[1,1,"h3"],
  box:[1,1,"m1"],          // 빈칸 상자 □(가)
  // v1.5 r2
  op:[3,3,"m1"],           // 사용자 정의 이항연산 op(기호, a, b) — 기호는 OPSYMS 이름
  nota:[2,3,"m1"],         // 약속 괄호 기호 nota(괄호, x[, y]) — 괄호는 NOTASYMS 이름
  idx:[2,2,"h1"],          // P[x]
  tr:[1,1,"h1"],           // 전치 Aᵗ
  dig:[1,8,"m1"],          // 자릿수 나열 abc
};
const CONSTS = { pi: Math.PI, e: Math.E, inf: Infinity, empty: null, i: null, cdots: null };
const GREEK = new Set(["alpha","beta","gamma","delta","theta","lam","mu","omega","phi","sigma"]);
export const GREEK_DISP = { alpha:"α", beta:"β", gamma:"γ", delta:"δ", theta:"θ", lam:"λ", mu:"μ", omega:"ω", phi:"φ", sigma:"σ" };
const BOX = "가나다라마바사아자차카타파하";
export const GRADE_ORD = { m1:1, m2:2, m3:3, h1:4, h2:5, h3:6 };
const LABEL_FNS = new Set(["seg","line","ray","arc","angle","tri","quad","vec"]);
export const OPSYMS = {   // v1.5r2 op(기호, a, b)의 기호 이름 → 글자
  star:"★", wstar:"☆", circ:"○", dcirc:"◎", bcirc:"●", fisheye:"◉", odot:"⊙", oplus:"⊕",
  otimes:"⊗", ominus:"⊖", oslash:"⊘", sq:"□", bsq:"■", dsq:"▣", diamond:"◇", bdiamond:"◆",
  tri:"△", btri:"▲", dtri:"▽", bdtri:"▼", ltri:"◁", rtri:"▷", heart:"♡", bheart:"♥",
  spade:"♠", club:"♣", ast:"∗", bullet:"•", ring:"∘", dagger:"†", ddagger:"‡", sharp:"♯",
  flat:"♭", natural:"♮", ref:"※", hash:"#", at:"@", amp:"&", sun:"☀", cloud:"☁",
  umbrella:"☂", snow:"☃", smile:"☺", note:"♪", dnote:"♫", check:"✓", cross:"✗", flower:"✿",
  arrow:"→", larrow:"←", uarrow:"↑", darrow:"↓", bowtie:"⋈", wr:"≀", hexagon:"⬡", pentagon:"⬠",
};
export const NOTASYMS = { // v1.5r2 nota(괄호, …)의 괄호 이름 → [여는 글자, 닫는 글자]
  angle:["⟨","⟩"], lt:["<",">"], brace:["{","}"], sq:["[","]"], paren:["(",")"],
  dsq:["⟦","⟧"], dangle:["⟪","⟫"], ceil:["⌈","⌉"], flr:["⌊","⌋"], dbar:["‖","‖"],
};

export const FIGS = {
  numline:["min","max"], coordplane:["x","y"], table:["rows"], hist:["bins","counts"],
  stemleaf:["stems"], crossing:["angles"], parallel:["angles"], tri:["v"], rect:["w","h"],
  polygon:["n"], circle:["r"], sector:["r","angle"], solid:["kind"], net:["kind"],
  boxplot:["values"], scatter:["points"], venn:["sets"], tree:["levels"],
  funcgraph:["expr"], unitcircle:[], conic:["kind"], vecfig:["vectors"], space:[],
  normcurve:["m","v"], unsupported:["raw"],
  image:["src"], scene:["pts"],   // v1.5: 도형 이미지 자산 / 선언형 장면
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
  const re = /(\d+\.\d+|\d+)|([A-Za-z]+)|(<=|>=|!=|[=<>+\-*/(),|'])|(\s+)/y;   // v1.5 ' 토큰
  while (i < s.length) {
    re.lastIndex = i;
    const m = re.exec(s);
    if (!m) throw new MathIRError("V-01", `허용되지 않는 문자 '${s[i]}'`, i);
    i = re.lastIndex;
    if (m[4]) continue;
    if (m[1]) out.push(["num", m[1], m.index]);
    else if (m[2]) {
      let v = m[2];
      if (i < s.length && /\d/.test(s[i]) && (v + s[i]) in FUNCS) { v += s[i]; i += 1; }   // v1.5⑦ point3
      out.push(["id", v, m.index]);
    }
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
  argList() {                                       // ( a, b, … ) — 일반 인자 목록
    this.expect("(");
    const args = [];
    if (this.peek()[1] !== ")") { for (;;) { args.push(this.rel()); if (this.peek()[1] === ",") { this.take(); continue; } break; } }
    this.expect(")");
    return args;
  }
  primary() {
    const [k, v, p] = this.take();
    if (v === "(") { const inner = this.rel(); this.expect(")"); return { t: "paren", a: inner }; }
    if (k === "num") return { t: "num", v };
    if (k === "id") {
      if (this.peek()[1] === "'" && !(v in CONSTS) && (v.length === 1 || GREEK.has(v))) {   // v1.5r2⑮ 변수 프라임 a', f'(x)
        let np = 0;
        while (this.peek()[1] === "'") { this.take(); np++; }
        if (this.peek()[1] === "(") {                                   // f'(x) → app(prime(f[, n]), x)
          const args = this.argList();
          this.maxGrade = Math.max(this.maxGrade, GRADE_ORD.h2);
          const pr = { t: "fn", f: "prime", args: [{ t: "var", v }, ...(np > 1 ? [{ t: "num", v: String(np) }] : [])] };
          return { t: "fn", f: "app", args: [pr, ...args] };
        }
        return { t: "var", v: v + "'".repeat(np) };
      }
      if (this.peek()[1] === "(") return this.call(v, p);
      if (v in CONSTS) return { t: "const", v };
      if (v.length === 1 || GREEK.has(v)) return { t: "var", v };
      throw new MathIRError("V-01", `미지의 식별자 '${v}'`, p);
    }
    throw new MathIRError("V-01", `예상치 못한 토큰 '${v}'`, p);
  }
  plainRun() {                                      // 다음 인자가 id·num 토큰만인지 (',' 또는 ')'까지) — recdec 자릿수 라벨용
    let j = this.i, seen = false;
    while (j < this.t.length) {
      const [k, v] = this.t[j];
      if (v === "," || v === ")") return seen;
      if (k !== "id" && k !== "num") return false;
      seen = true; j++;
    }
    return false;                                   // 종결 토큰 없음 → 일반 파싱으로(문법 오류 보고)
  }
  call(name, pos) {
    this.expect("(");
    const args = [];
    if (this.peek()[1] !== ")") {
      for (;;) {
        const pk = this.peek();
        if (LABEL_FNS.has(name) && (pk[0] === "id" || pk[0] === "num" || pk[1] === "'")) {   // 점 라벨 나열형 (v1.5 첨자·프라임)
          let lab = "";
          while (this.peek()[0] === "id" || this.peek()[0] === "num" || this.peek()[1] === "'") lab += this.take()[1];
          args.push({ t: "label", v: lab });
        }
        else if (name === "lim" && args.length === 3 && (pk[1] === "+" || pk[1] === "-")) args.push({ t: "label", v: this.take()[1] });
        else if (name === "itv" && args.length === 2) args.push({ t: "label", v: this.take()[1] });
        else if ((name === "op" || name === "nota") && args.length === 0) {                  // v1.5r2 기호 이름 라벨
          const [k2, v2, p2] = this.take();
          const table = name === "op" ? OPSYMS : NOTASYMS;
          if (k2 !== "id" || !(v2 in table)) throw new MathIRError("V-01", `${name} 기호 이름 '${v2}' 은 이름표에 없음`, p2);
          args.push({ t: "label", v: v2 });
        }
        else if (name === "recdec" && this.plainRun()) {                                     // v1.5r2 자릿수 라벨(문자 허용)
          let lab = "";
          while (this.peek()[1] !== "," && this.peek()[1] !== ")") lab += this.take()[1];
          args.push({ t: "label", v: lab });
        }
        else args.push(this.rel());
        if (this.peek()[1] === ",") { this.take(); continue; }
        break;
      }
    }
    this.expect(")");
    if (name in FUNCS) {
      const [lo, hi, grade] = FUNCS[name];
      if (args.length < lo || args.length > hi) throw new MathIRError("V-02", `${name} 인자 ${args.length}개 — 허용 ${lo}~${hi}`, pos);
      if (name === "cases" && args.length % 2) throw new MathIRError("V-02", "cases 인자는 (식, 조건) 쌍이어야 함", pos);
      this.maxGrade = Math.max(this.maxGrade, GRADE_ORD[grade]);
      return { t: "fn", f: name, args };
    }
    if (name.length === 1 || GREEK.has(name)) { this.maxGrade = Math.max(this.maxGrade, GRADE_ORD.h1); return { t: "apply", f: name, args }; }   // v1.5④ alpha(t)
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
const atom = (n) => !(n.t === "fn" && n.f === "op") && ATOM.has(n.t);      // v1.5r2: a ◎ b 는 원자가 아님
const wrap = (n) => atom(n) ? disp(n) : "(" + disp(n) + ")";
const PRIMES = { 0: "", 1: "′", 2: "″", 3: "‴" };

// 곱 표시 (v1.5r2 표시 수정): 병치 사슬 2ab, −5x, 2√3x 는 그대로 잇고, 숫자 앞 함수(9 × 2^(n+1))·숫자끼리·부호 등은 ' × '.
// 반환 [문자열, 왼쪽이 병치 사슬인지]. 종전 v1.0은 (2a) × b, (−5) × x, 92^(n+1) 로 표시됨.
const DIGITS = /^[0-9⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉]/;   // 표시 문자열이 숫자(위·아래첨자 포함)로 시작하는지 — mathir.py와 동일 집합
function xprod(n) {
  const A = n.a, B = n.b;
  let left, lchain;
  if (A.t === "bin" && A.op === "×") [left, lchain] = xprod(A);
  else {
    lchain = ["num","var","paren"].includes(A.t) || (A.t === "neg" && ["num","var","paren"].includes(A.a.t));
    left = lchain ? disp(A) : wrap(A);
  }
  const b = (B.t === "neg" || B.t === "fn") ? wrap(B) : disp(B);
  if (lchain && ["var","fn","apply","paren","const"].includes(B.t) && !(B.t === "fn" && DIGITS.test(b))) return [left + b, true];
  return [left + " × " + ((B.t === "neg" || B.t === "fn") ? b : wrap(B)), false];
}

export function disp(n) {
  const t = n.t;
  if (t === "num") return n.v;
  if (t === "const") return { pi:"π", e:"e", inf:"∞", i:"i", empty:"∅", cdots:"⋯" }[n.v];
  if (t === "var") {                                                             // v1.5r2 a′ · 그리스 문자
    const base = n.v.replace(/'+$/, ""), k = n.v.length - base.length;
    return (GREEK_DISP[base] || base) + (PRIMES[k] ?? "′".repeat(k));
  }
  if (t === "label") return n.v.replace(/\d+/g, (m) => subs(m)).replace(/'/g, "′");   // 라벨 숫자→아래첨자, '→′
  if (t === "neg") return "−" + wrap(n.a);
  if (t === "paren") return "(" + disp(n.a) + ")";
  if (t === "bin") {
    if (n.op === "×") return xprod(n)[0];
    if (n.op === "÷") return wrap(n.a) + " ÷ " + wrap(n.b);
    const op = n.op === "-" ? "−" : n.op;
    return disp(n.a) + ` ${op} ` + (n.b.t === "neg" ? wrap(n.b) : disp(n.b));
  }
  if (t === "rel") { let s = disp(n.args[0]); n.ops.forEach((op, k) => { s += ` ${op} ` + disp(n.args[k + 1]); }); return s; }
  if (t === "apply") return (GREEK_DISP[n.f] || n.f) + "(" + n.args.map(disp).join(", ") + ")";
  const f = n.f, a = n.args, D = disp;
  const lab = () => a.map(D).join("");
  switch (f) {
    case "frac": return wrap(a[0]) + "/" + wrap(a[1]);
    case "mixed": return D(a[0]) + " " + D(a[1]) + "/" + D(a[2]);
    case "pow": { const ex = toIR(a[1]).replace(/ /g, ""); return wrap(a[0]) + (/^-?\d+$/.test(ex) ? sup(ex) : "^(" + D(a[1]) + ")"); }
    case "sqrt": return "√" + wrap(a[0]);
    case "root": return sup(toIR(a[0])) + "√" + wrap(a[1]);
    case "abs": return "|" + D(a[0]) + "|";
    case "recdec": {                                   // v1.5r2: 라벨(문자 자릿수)은 원문 그대로, 3인자형 = 정수부.비순환 순환마디, 소수점 수정
      const raw = (x) => (x.t === "label" ? x.v : D(x));
      const rep = raw(a[a.length - 1]);
      const dotted = rep.length > 1 ? rep[0] + "\u0307" + rep.slice(1, -1) + rep[rep.length - 1] + "\u0307" : rep + "\u0307";
      const pre = raw(a[0]) + (raw(a[0]).includes(".") ? "" : ".");
      return a.length === 2 ? pre + dotted : pre + raw(a[1]) + dotted;
    }
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
    case "mat": {
      const r = Number(a[0]?.v), c = Number(a[1]?.v), cells = a.slice(2).map(D);
      if (Number.isInteger(r) && Number.isInteger(c) && cells.length === r * c) {
        const rows = [];
        for (let i = 0; i < r; i++) rows.push(cells.slice(i * c, (i + 1) * c).join(" "));
        return "(" + rows.join(" ; ") + ")";
      }
      return "mat(" + a.map(D).join(", ") + ")";
    }
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
    case "sub": { if (a.length === 3) return D(a[0]) + "[" + D(a[1]) + "," + D(a[2]) + "]";
      const ix = toIR(a[1]).replace(/ /g, ""); return D(a[0]) + (/^\d+$/.test(ix) ? subs(ix) : "_" + wrap(a[1])); }
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
    // ---- v1.5
    case "cases": { const ps = []; for (let i = 0; i < a.length; i += 2) ps.push(D(a[i]) + " (" + D(a[i + 1]) + ")"); return "{" + ps.join(" ; ") + "}"; }
    case "app": {
      const F = a[0];
      const head = (F.t === "var" || F.t === "label" || (F.t === "fn" && ["prime","inv","sub","iter","xbar","hat"].includes(F.f))) ? D(F) : "(" + D(F) + ")";
      return head + "(" + a.slice(1).map(D).join(", ") + ")";
    }
    case "iter": { const ex = toIR(a[1]).replace(/ /g, ""); return wrap(a[0]) + (/^-?\d+$/.test(ex) ? sup(ex) : "^(" + D(a[1]) + ")") + "(" + D(a[2]) + ")"; }
    case "xbar": return D(a[0]) + "\u0304";
    case "hat": return D(a[0]) + "\u0302";
    case "box": { const k = toIR(a[0]); return "□(" + (/^\d+$/.test(k) && Number(k) >= 1 && Number(k) <= BOX.length ? BOX[Number(k) - 1] : D(a[0])) + ")"; }
    // ---- v1.5 r2
    case "op": {                                       // 피연산자가 관계식·다른 op이면 괄호
      const w = (x) => (x.t === "rel" || (x.t === "fn" && x.f === "op")) ? "(" + D(x) + ")" : D(x);
      return w(a[1]) + " " + (OPSYMS[a[0].v] || a[0].v) + " " + w(a[2]);
    }
    case "nota": { const [o, c] = NOTASYMS[a[0].v] || ["⟨", "⟩"]; return o + a.slice(1).map(D).join(", ") + c; }
    case "idx": return wrap(a[0]) + "[" + D(a[1]) + "]";
    case "tr": return wrap(a[0]) + "ᵗ";
    case "dig": return a.map(D).join("");
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
      case "recdec": {                               // v1.5r2: 문자 자릿수는 평가 불가(V-03), 3인자형 = 정수부 + 비순환/10^k + 순환/((10^m−1)·10^k)
        const parts = a.map(toIR);
        if (!parts.every((s) => /^\d+(\.\d+)?$/.test(s))) throw new MathIRError("V-03", "평가 불가 순환소수(문자 자릿수)");
        if (a.length === 3) {
          const [pre, non, rep] = parts;
          return Frac.fromDecimal(pre).add(new Frac(BigInt(non), 10n ** BigInt(non.length)))
            .add(new Frac(BigInt(rep), (10n ** BigInt(rep.length) - 1n) * 10n ** BigInt(non.length)));
        }
        const [pre, rep] = parts;
        const base = Frac.fromDecimal(pre);
        const dec = pre.includes(".") ? pre.split(".")[1].length : 0;
        return base.add(new Frac(BigInt(rep), (10n ** BigInt(rep.length) - 1n) * 10n ** BigInt(dec)));
      }
      case "dig": {                                  // v1.5r2 자릿수 나열
        const ds = a.map(toIR);
        if (!ds.every((s) => /^\d$/.test(s))) throw new MathIRError("V-03", "평가 불가 자릿수(문자)");
        return new Frac(BigInt(ds.join("")));
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
      case "comb": { const N = Math.trunc(num(E(0))), R = Math.trunc(num(E(1))); let up = 1n, dn = 1n; for (let k = 0; k < R; k++) { up *= BigInt(N - k); dn *= BigInt(k + 1); } return new Frac(up, dn); }
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

// v1.4③ 단위 꼬리: 답 끝의 단위 토큰을 떼어 unit 주석으로 보관
const UNITS = "(?:cm³|cm²|m³|m²|km²|mm²|cm3|cm2|m3|m2|km|cm|mm|m|kg|g|L|mL|%|개|명|원|시간|분|초|번|살|점|회|장|권|마리|가지|자루|송이|그루|대|병|봉지|통|칸)";
function splitUnit(s) {
  s = s.replace(/\s*pow\((cm|m|km|mm),\s*([23])\)$/, (_, u, k) => " " + u + (k === "2" ? "²" : "³"));
  const m = s.match(new RegExp("^([\\s\\S]+?)\\s*" + UNITS + "$"));
  if (m && m[1].trim()) return [m[1].trim(), s.slice(m[1].length).trim()];
  return [s, null];
}
function parseAnswerOne(s) {
  s = s.trim();
  s = s.replace(/^[가-힣]{1,4}\s*[:：]\s*/, "");                    // v1.4⑤ '좌변:' 라벨 접두 제거
  let unit = null;
  const m = s.match(new RegExp("^\\[\\[([\\s\\S]+)\\]\\]\\s*(" + UNITS + ")?$"));   // [[마커]] 관용 탈피 (+ 단위 꼬리)
  if (m) { s = m[1].trim(); unit = m[2] || null; }
  else [s, unit] = splitUnit(s);
  s = s.replace(/(\d+(?:\.\d+)?)\s*°/g, "deg($1)");                 // v1.4② 각도
  s = s.replace(/π/g, "pi");
  s = s.replace(/(\d)\s*pi\b/g, "$1*pi");                          // '72pi' → 72*pi
  let sign = null;
  if (/^\+\s*[^\s+-]/.test(s)) { sign = "+"; s = s.slice(1).trim(); }   // v1.5r2⑯ 양의 부호 답 '+23'
  try {
    const [node] = parse(s);
    const out = { kind: "ir", node };
    if (unit) out.unit = unit;
    if (sign) out.sign = sign;
    return out;
  } catch (e) {
    if (/^[가-힣ㄱ-ㅎ㉠-㉻①-⑳○×A-Za-z0-9 ,·~]+$/.test(s)) return { kind: "word", v: s };   // v1.4① 합답형·선지·○× (+ r2 원문자)
    throw e;
  }
}
export function parseAnswer(s) {
  s = s.trim();
  const parts = s.split(/\s*(?:또는|\|)\s*/);
  if (parts.length >= 2) return { kind: "set", items: parts.filter((p) => p.trim()).map(parseAnswerOne) };
  // v1.4④ 병립 답: 'a = 5, b = -1' · 'a < 0 and b > 0' — 각 조각이 관계식/식으로 파싱될 때만 set
  const conj = s.split(/\s*,\s*|\s+and\s+/);
  if (conj.length >= 2 && conj.every((c) => c.trim())) {
    try {
      const its = conj.map(parseAnswerOne);
      if (its.every((it) => it.kind === "ir")) return { kind: "set", items: its };
    } catch (e) { if (!(e instanceof MathIRError)) throw e; }
  }
  return parseAnswerOne(s);
}
export function checkEquationAnswer(questionText, answerStr) {
  try {
    const ans = parseAnswer(answerStr);
    const { segs, errs } = parseText(questionText);
    if (errs.length) return null;
    const rels = segs.filter((s) => s.kind === "ir" && s.node.t === "rel" && s.node.ops.includes("=")).map((s) => s.node);
    if (!rels.length) return null;
    const one = (node) => {
      if (!(node.t === "rel" && node.ops.length === 1 && node.ops[0] === "=" && node.args[0].t === "var")) return null;
      const varName = node.args[0].v, val = ev(node.args[1]);
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
    };
    const nodes = ans.kind === "set" ? ans.items.filter((i) => i.kind === "ir").map((i) => i.node)
                : ans.kind === "ir" ? [ans.node] : [];
    if (!nodes.length) return null;
    const rs = nodes.map(one);                       // 복수 해: 모든 근이 성립해야 참
    if (rs.some((r) => r === false)) return false;
    if (rs.some((r) => r === null)) return null;
    return true;
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
