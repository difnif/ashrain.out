// 해석학 그림 — 상한 · ε-N · 리만 재배열 · 균등연속 · 확대와 미분 · 상합과 하합 · 균등수렴 · 축소 사상 · 칸토어 집합
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, fmt, clamp, lerp, ease, sup, useClock } from "./kit.jsx";

const sb = (n) => String(n).split("").map((d) => "₀₁₂₃₄₅₆₇₈₉"["0123456789".indexOf(d)] || d).join("");

/* ── 상한: 상계 가운데 가장 작은 것 ── */
const SETS = {
  inv: { name: "{1 − 1/n}", pts: () => Array.from({ length: 80 }, (_, i) => 1 - 1 / (i + 1)), sup: 1, supT: "1", x0: -0.25, x1: 1.75,
    end: "sup A = 1 은 A 의 원소가 아니다 — 최댓값은 없지만 상한은 있다" },
  alt: { name: "{(−1)ⁿ ÷ n}", pts: () => Array.from({ length: 60 }, (_, i) => ((i + 1) % 2 ? -1 : 1) / (i + 1)), sup: 0.5, supT: "1/2", x0: -1.25, x1: 1.45,
    end: "sup A = 1/2 은 n = 2 일 때의 원소 — 상한이 원소이면 그것이 최댓값이다" },
  sqrt2: { name: "{x ≥ 0 인 유리수, x² < 2}", pts: () => { const o = []; for (let q = 1; q <= 24; q++) for (let p0 = 0; p0 <= 2 * q; p0++) if (p0 * p0 < 2 * q * q) o.push(p0 / q); return o; }, sup: Math.SQRT2, supT: "√2", x0: -0.2, x1: 2.25,
    end: "상한 √2 는 유리수가 아니다 — 유리수만으로는 이 집합의 상한이 없고, 실수의 완비성(상한 공리)이 빈자리를 채운다" },
};
export function SupInf({ p = {} }) {
  const [k, setK] = useState(SETS[p.set] ? p.set : "inv");
  const S = SETS[k], pts = useMemo(() => SETS[k].pts(), [k]);
  const clock = useClock({ period: 12, rest: 10 });
  const t = clock.t, top = S.x1 - 0.08, low = S.sup - 0.28;
  const u = t < 5 ? lerp(top, S.sup, ease(t / 5)) : t < 7 ? lerp(S.sup, low, ease((t - 5) / 2)) : t < 9 ? lerp(low, S.sup, ease((t - 7) / 2)) : S.sup;
  const over = pts.filter((x) => x > u + 1e-9);
  const atSup = Math.abs(u - S.sup) < 1e-6;
  const P = plot({ x0: S.x0, x1: S.x1, y0: 0, y1: 1, pad: [10, 14, 30, 14] });
  const Y = 128, dense = k === "sqrt2";
  const ticks = [];
  for (let v = Math.ceil(S.x0 * 2) / 2; v <= S.x1 + 1e-9; v += 0.5) ticks.push(v);
  return (
    <Frame clock={clock} title="상한 — 가장 작은 상계"
      read={<>A = {S.name} · 세로선 u {atSup ? <>가 상한에 왔다: <b>{S.end}</b> · u 보다 조금만 작아도(u − ε) 그보다 큰 원소가 반드시 있다</> : over.length ? <>= {fmt(u, 3)} 는 <b>상계가 아니다</b> — u 보다 큰 원소(빨강)가 있다</> : <>= {fmt(u, 3)} 는 <b>상계</b>다 — A 의 모든 원소가 u 이하 · 상계는 많지만 가장 작은 상계(상한)는 하나뿐</>}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["inv", "1 − 1/n"], ["alt", "(−1)ⁿ ÷ n"], ["sqrt2", "x² < 2 인 유리수"]]} />}>
      <line x1={P.l} x2={P.r} y1={Y} y2={Y} stroke={C.mut} strokeWidth="1.3" />
      {ticks.map((v) => (
        <g key={v}>
          <line x1={P.X(v)} x2={P.X(v)} y1={Y - 4} y2={Y + 4} stroke={C.mut} />
          <text x={P.X(v)} y={Y + 18} textAnchor="middle" fontSize="10" fill={C.mut}>{fmt(v, 1)}</text>
        </g>
      ))}
      {pts.map((x, i) => (dense
        ? <line key={i} x1={P.X(x)} x2={P.X(x)} y1={Y - 9} y2={Y} stroke={x > u + 1e-9 ? C.red : C.blue} strokeWidth="1" opacity="0.7" />
        : <circle key={i} cx={P.X(x)} cy={Y - 7} r="2.6" fill={x > u + 1e-9 ? C.red : C.blue} opacity="0.75" />))}
      <line x1={P.X(S.sup)} x2={P.X(S.sup)} y1={Y - 70} y2={Y + 6} stroke={C.gold} strokeWidth="1.4" strokeDasharray="4 3" />
      <text x={P.X(S.sup)} y={Y - 74} textAnchor="middle" fontSize="10.5" fontWeight="800" fill={C.gold}>sup = {S.supT}</text>
      <line x1={P.X(u)} x2={P.X(u)} y1={Y - 52} y2={Y + 6} stroke={over.length ? C.red : C.green} strokeWidth="2.4" />
      <text x={P.X(u) + 6} y={Y - 42} fontSize="11" fontWeight="800" fill={over.length ? C.red : C.green}>u</text>
      {!over.length && <rect x={P.X(u)} y={Y - 24} width={Math.max(0, P.r - P.X(u))} height="10" fill={C.green} opacity="0.12" />}
      <text x={P.l} y="20" fontSize="10" fill={C.mut}>파랑 = A 의 원소 · 초록 막대 = 상계 · 빨강 = u 를 넘는 원소</text>
      <text x={P.l} y={Y + 40} fontSize="10" fill={C.ink}>{over.length ? `u 를 넘는 원소 ${over.length} 개(그림에 보이는 것만)` : "u 오른쪽에는 원소가 하나도 없다"}</text>
    </Frame>
  );
}

/* ── ε-N: 어떤 ε 이든 그 뒤로는 모두 띠 안 ── */
const SEQ = {
  inv: { f: (n) => 1 / n, L: 0, Lt: "0", y0: -0.15, y1: 1.05, name: "aₙ = 1/n" },
  alt: { f: (n) => (n % 2 ? -1 : 1) / n, L: 0, Lt: "0", y0: -1.05, y1: 0.6, name: "aₙ = (−1)ⁿ ÷ n" },
  e: { f: (n) => (1 + 1 / n) ** n, L: Math.E, Lt: "e ≈ 2.718", y0: 1.95, y1: 2.82, name: "aₙ = (1 + 1/n)ⁿ" },
  sinn: { f: (n) => Math.sin(n) / Math.sqrt(n), L: 0, Lt: "0", y0: -0.9, y1: 0.9, name: "aₙ = sin n ÷ √n" },
};
const NMAX = 80, ET = 9;
const epsAt = (t) => 0.5 * 25 ** (-Math.min(t, ET) / ET);
function findN(f, L, eps) { let last = 0; for (let n = 1; n <= 6000; n++) if (Math.abs(f(n) - L) >= eps) last = n; return last + 1; }
export function EpsN({ p = {} }) {
  const [k, setK] = useState(SEQ[p.seq] ? p.seq : "inv");
  const S = SEQ[k];
  const clock = useClock({ period: 12, rest: 9.5 });
  const eps = epsAt(clock.t), N = findN(S.f, S.L, eps);
  const P = plot({ x0: 0, x1: NMAX + 1, y0: S.y0, y1: S.y1, pad: [14, 12, 24, 40] });
  const yb = clamp(S.L + eps, S.y0, S.y1), ya = clamp(S.L - eps, S.y0, S.y1);
  return (
    <Frame clock={clock} title="수열의 수렴 — ε 과 N"
      read={<>{S.name} → L = {S.Lt} · 띠의 반폭 ε = <b>{fmt(eps, 3)}</b> → <b>N = {N}</b>{N > NMAX ? "(그림 밖)" : ""}: n ≥ N 인 모든 항이 |aₙ − L| &lt; ε 안에 든다(초록) · ε 을 아무리 작게 줘도 N 을 찾을 수 있다 — 이것이 ‘aₙ → L’ 의 뜻이다</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["inv", "1/n"], ["alt", "(−1)ⁿ ÷ n"], ["e", "(1 + 1/n)ⁿ"], ["sinn", "sin n ÷ √n"]]} />
        <Slider label="ε" min={0.02} max={0.5} step={0.01} value={Math.round(eps * 100) / 100} onChange={(v) => { clock.setT((-ET * Math.log(v / 0.5)) / Math.log(25)); clock.setPlaying(false); }} show={(v) => fmt(v, 2)} />
      </>}>
      <rect x={P.l} y={P.Y(yb)} width={P.r - P.l} height={Math.max(0, P.Y(ya) - P.Y(yb))} fill={C.green} opacity="0.12" />
      <line x1={P.l} x2={P.r} y1={P.Y(S.L)} y2={P.Y(S.L)} stroke={C.green} strokeDasharray="5 4" />
      <Axes p={P} xl="" yl="aₙ" grid={false} xt={[]} />
      {[20, 40, 60].map((v) => <text key={v} x={P.X(v)} y={P.b + 14} textAnchor="middle" fontSize="10" fill={C.mut}>{v}</text>)}
      <text x={P.r} y={P.b + 14} textAnchor="end" fontSize="10" fontStyle="italic" fill={C.ink}>n</text>
      {N <= NMAX && <line x1={P.X(N)} x2={P.X(N)} y1={P.t} y2={P.b} stroke={C.gold} strokeWidth="1.6" />}
      {N <= NMAX && <text x={P.X(N) + 3} y={P.t + 24} fontSize="10" fontWeight="800" fill={C.gold}>N = {N}</text>}
      {Array.from({ length: NMAX }, (_, i) => {
        const n = i + 1, a = S.f(n), inB = Math.abs(a - S.L) < eps;
        return <circle key={n} cx={P.X(n)} cy={P.Y(clamp(a, S.y0, S.y1))} r="2.4" fill={n >= N ? C.green : inB ? C.blue : C.red} opacity={n >= N ? 1 : 0.75} />;
      })}
    </Frame>
  );
}

/* ── 리만 재배열: 조건수렴 급수는 순서를 바꾸면 아무 값으로나 ── */
export function Rearrange({ p = {} }) {
  const [S, setS] = useState(clamp(p.S ?? 1.5, -1, 2));
  const K = 400;
  const R = useMemo(() => {
    let s = 0, ip = 0, ineg = 0;
    const out = [0], sg = [];
    for (let k = 0; k < K; k++) {
      if (s <= S) { s += 1 / (2 * ip + 1); ip++; sg.push(1); } else { ineg++; s -= 1 / (2 * ineg); sg.push(-1); }
      out.push(s);
    }
    return { out, sg };
  }, [S]);
  const orig = useMemo(() => { let s = 0; const o = [0]; for (let k = 1; k <= K; k++) { s += (k % 2 ? 1 : -1) / k; o.push(s); } return o; }, []);
  const clock = useClock({ period: 11, rest: 9 });
  const shown = Math.max(3, Math.round(K * clamp(clock.t / 8, 0, 1)));
  const np = R.sg.slice(0, shown).filter((x) => x > 0).length, nn = shown - np;
  const lo = Math.min(S, 0) - 0.3, hi = Math.max(S, 1) + 0.45;
  const P = plot({ x0: 0, x1: K, y0: lo, y1: hi, pad: [14, 12, 24, 36] });
  const path = (arr) => arr.slice(0, shown + 1).map((v, i) => (i ? "L" : "M") + P.X(i).toFixed(1) + " " + P.Y(clamp(v, lo, hi)).toFixed(1)).join("");
  return (
    <Frame clock={clock} title="리만 재배열 정리"
      read={<>1 − 1/2 + 1/3 − 1/4 + … 은 이 순서로 더하면 ln 2 ≈ 0.693 (회색) · 같은 항들을 ‘합이 S 보다 작으면 양수 항, 크면 음수 항’ 순서로 다시 늘어놓으면 부분합이 <b>S = {fmt(S, 1)}</b> 로 간다(파랑) — 지금까지 양수 항 {np} 개 · 음수 항 {nn} 개, 부분합 {fmt(R.out[shown], 4)} · 양수 항만 더해도, 음수 항만 더해도 발산하기 때문에 가능하다(조건수렴) · 절대수렴 급수는 순서를 바꿔도 합이 같다</>}
      controls={<Slider label="목표 S" min={-1} max={2} step={0.1} value={S} onChange={(v) => { setS(v); clock.reset(); }} show={(v) => fmt(v, 1)} />}>
      <line x1={P.l} x2={P.r} y1={P.Y(S)} y2={P.Y(S)} stroke={C.red} strokeDasharray="5 4" />
      <line x1={P.l} x2={P.r} y1={P.Y(Math.LN2)} y2={P.Y(Math.LN2)} stroke={C.mut} strokeDasharray="2 3" />
      <Axes p={P} xl="더한 항 수" yl="부분합" grid={false} xt={[100, 200, 300, 400]} />
      <path d={path(orig)} fill="none" stroke={C.mut} strokeWidth="1.2" opacity="0.8" />
      <path d={path(R.out)} fill="none" stroke={C.blue} strokeWidth="1.6" />
      <text x={P.r - 4} y={P.Y(S) - 5} textAnchor="end" fontSize="10" fontWeight="800" fill={C.red}>S = {fmt(S, 1)}</text>
      <text x={P.r - 4} y={P.Y(Math.LN2) + (S > Math.LN2 ? 13 : -5)} textAnchor="end" fontSize="10" fill={C.mut}>ln 2</text>
    </Frame>
  );
}

/* ── 균등연속: 한 δ 로 모든 점에서 통하나 ── */
const UF = {
  inv: { f: (x) => 1 / x, name: "1/x", lo: 1e-6, xmin: 0.1, unif: false, y0: 0, y1: 11, dom: "(0, 1]" },
  sin: { f: (x) => Math.sin(1 / x), name: "sin(1/x)", lo: 1e-6, xmin: 0.04, unif: false, y0: -1.35, y1: 1.35, dom: "(0, 1]" },
  sqrt: { f: (x) => Math.sqrt(x), name: "√x", lo: 0, xmin: 0, unif: true, y0: -0.1, y1: 1.15, dom: "[0, 1]" },
  sq: { f: (x) => x * x, name: "x²", lo: 0, xmin: 0, unif: true, y0: -0.1, y1: 1.15, dom: "[0, 1]" },
};
function deltaAt(F, x0, eps) {
  const y0 = F.f(x0);
  const ok = (d) => { const a = Math.max(F.lo, x0 - d), b = Math.min(1, x0 + d); for (let i = 0; i <= 240; i++) { const x = a + ((b - a) * i) / 240; if (!(Math.abs(F.f(x) - y0) < eps)) return false; } return true; };
  let lo = 0, hi = 1;
  for (let k = 0; k < 28; k++) { const m = (lo + hi) / 2; if (ok(m)) lo = m; else hi = m; }
  return lo;
}
export function UnifCont({ p = {} }) {
  const [k, setK] = useState(UF[p.f] ? p.f : "inv");
  const [eps, setEps] = useState(clamp(p.eps ?? 0.2, 0.05, 0.5));
  const F = UF[k];
  const xs = useMemo(() => Array.from({ length: 48 }, (_, i) => (F.xmin > 0 ? F.xmin * (1 / F.xmin) ** (i / 47) : i / 47)), [k]);
  const ds = useMemo(() => xs.map((x) => deltaAt(F, x, eps)), [k, eps, xs]);
  const clock = useClock({ period: 11, rest: 8.6 });
  const u = clamp(clock.t / 8, 0, 1);
  const x0 = F.xmin > 0 ? 0.9 * (F.xmin / 0.9) ** ease(u) : lerp(0.9, 0, ease(u));
  const d = deltaAt(F, x0, eps), fx = F.f(x0);
  const dmin = Math.min(...ds), dmax = Math.max(...ds, 0.05);
  const P1 = plot({ x0: 0, x1: 1, y0: F.y0, y1: F.y1, pad: [14, 196, 26, 28] });
  const P2 = plot({ x0: 0, x1: 1, y0: 0, y1: dmax * 1.1, pad: [14, 12, 26, 220] });
  return (
    <Frame clock={clock} title="연속과 균등연속"
      read={<>f(x) = {F.name}, 정의역 {F.dom}, ε = {fmt(eps, 2)} · 점 x₀ = {fmt(x0, 3)} 에서 |x − x₀| &lt; δ 이면 |f(x) − f(x₀)| &lt; ε 이 되는 가장 큰 δ = <b>{fmt(d, 4)}</b>(오른쪽 그림) · {F.unif ? <>δ 가 어디서나 {fmt(dmin, 3)} 이상 — δ 하나로 모든 점에서 통한다: <b>균등연속</b></> : <>x₀ 가 0 에 다가가면 δ 가 0 으로 줄어든다 — 모든 점에 통하는 δ 하나가 없다: 연속이지만 <b>균등연속이 아니다</b></>}</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["inv", "1/x"], ["sin", "sin(1/x)"], ["sqrt", "√x"], ["sq", "x²"]]} />
        <Slider label="ε" min={0.05} max={0.5} step={0.05} value={eps} onChange={setEps} show={(v) => fmt(v, 2)} />
      </>}>
      {fx > F.y0 && fx < F.y1 && <rect x={P1.l} y={P1.Y(Math.min(F.y1, fx + eps))} width={P1.r - P1.l} height={Math.max(0, P1.Y(Math.max(F.y0, fx - eps)) - P1.Y(Math.min(F.y1, fx + eps)))} fill={C.green} opacity="0.14" />}
      <rect x={P1.X(Math.max(0, x0 - d))} y={P1.t} width={Math.max(0.8, P1.X(Math.min(1, x0 + d)) - P1.X(Math.max(0, x0 - d)))} height={P1.b - P1.t} fill={C.gold} opacity="0.2" />
      <Axes p={P1} xl="x" yl="" grid={false} xt={[0.5, 1]} />
      <path d={P1.path(F.f, Math.max(F.lo, 0.004), 1, 400)} fill="none" stroke={C.sp} strokeWidth="1.6" />
      {fx > F.y0 && fx < F.y1 && <circle cx={P1.X(x0)} cy={P1.Y(fx)} r="4" fill={C.red} />}
      <text x={P1.l + 4} y={P1.t + 10} fontSize="9" fill={C.mut}>초록 = f(x₀) ± ε · 노랑 = x₀ ± δ</text>
      <Axes p={P2} xl="x₀" yl="δ" grid={false} xt={[0.5, 1]} yt={[]} />
      <path d={P2.poly(xs.map((x, i) => [x, ds[i]]))} fill="none" stroke={C.gold} strokeWidth="1.8" />
      <circle cx={P2.X(x0)} cy={P2.Y(d)} r="4" fill={C.red} />
      {F.unif && <line x1={P2.l} x2={P2.r} y1={P2.Y(dmin)} y2={P2.Y(dmin)} stroke={C.green} strokeDasharray="4 3" />}
      <text x={P2.r} y={P2.t + 10} textAnchor="end" fontSize="9.5" fill={C.mut}>δ(x₀)</text>
    </Frame>
  );
}

/* ── 확대와 미분: 미분 가능 = 확대하면 직선 ── */
const Wf = (x) => { let s = 0, a = 1, b = 1; for (let k = 0; k < 15; k++) { s += a * Math.cos(b * Math.PI * x); a *= 0.5; b *= 3; } return s; };
const ZF = {
  sq: { f: (x) => x * x, x0: 0.5, name: "x²(x₀ = 0.5)", fix: true },
  abs: { f: (x) => Math.abs(x), x0: 0, name: "|x|(x₀ = 0)", fix: true },
  weier: { f: Wf, x0: 0.3, name: "바이어슈트라스 함수(x₀ = 0.3)", fix: false },
};
export function ZoomDiff({ p = {} }) {
  const [k, setK] = useState(ZF[p.f] ? p.f : "sq");
  const Z = ZF[k];
  const clock = useClock({ period: 12, rest: 9.5 });
  const lev = 3 * Math.min(clock.t, 9) / 9, w = 10 ** -lev;
  const fx = Z.f(Z.x0), N = 320;
  const ys = Array.from({ length: N + 1 }, (_, i) => Z.f(Z.x0 - w + (2 * w * i) / N));
  let y0, y1;
  if (Z.fix) { y0 = fx - 1.3 * w; y1 = fx + 1.3 * w; } else { const mn = Math.min(...ys), mx = Math.max(...ys), pad = (mx - mn) * 0.12 + 1e-12; y0 = mn - pad; y1 = mx + pad; }
  const P = plot({ x0: Z.x0 - w, x1: Z.x0 + w, y0, y1, pad: [16, 12, 22, 12] });
  const h = w / 2, sl = (fx - Z.f(Z.x0 - h)) / h, sr = (Z.f(Z.x0 + h) - fx) / h;
  const d = ys.map((y, i) => (i ? "L" : "M") + P.X(Z.x0 - w + (2 * w * i) / N).toFixed(1) + " " + P.Y(y).toFixed(1)).join("");
  return (
    <Frame clock={clock} title="확대하면 보이는 미분"
      read={<>{Z.name} 둘레를 <b>{fmt(1 / w, 0)} 배</b> 확대했다(창의 반폭 {w < 0.01 ? w.toExponential(1).replace("e-", " × 10⁻").replace(/⁻(\d)$/, (m, g) => "⁻" + "⁰¹²³⁴⁵⁶⁷⁸⁹"[+g]) : fmt(w, 3)}) · 왼쪽 기울기 {fmt(sl, 3)}, 오른쪽 기울기 {fmt(sr, 3)} · {k === "sq" ? "확대할수록 그래프가 직선(접선, 기울기 1)에 붙는다 — 미분 가능하다는 것은 ‘아주 가까이서 보면 직선’이라는 뜻" : k === "abs" ? "아무리 확대해도 꺾인 모양 그대로 — 왼쪽 · 오른쪽 기울기가 −1 과 1 로 끝내 만나지 않아 0 에서 미분 불가능" : "어디를 확대해도 똑같이 들쭉날쭉하다 — 연속이지만 어느 점에서도 미분할 수 없다(1872 년 바이어슈트라스)"}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sq", "x²"], ["abs", "|x|"], ["weier", "바이어슈트라스"]]} />}>
      {k === "sq" && <line x1={P.l} x2={P.r} y1={P.Y(fx + 2 * Z.x0 * (P.x0 - Z.x0))} y2={P.Y(fx + 2 * Z.x0 * (P.x1 - Z.x0))} stroke={C.gold} strokeWidth="1.4" strokeDasharray="5 4" />}
      <path d={d} fill="none" stroke={C.sp} strokeWidth="1.6" />
      <circle cx={P.X(Z.x0)} cy={P.Y(fx)} r="3.6" fill={C.red} />
      <line x1={P.l} x2={P.r} y1={P.b} y2={P.b} stroke={C.bd} />
      <text x={P.l} y={P.b + 15} fontSize="10" fill={C.mut}>{fmt(Z.x0 - w, 4)}</text>
      <text x={P.r} y={P.b + 15} textAnchor="end" fontSize="10" fill={C.mut}>{fmt(Z.x0 + w, 4)}</text>
      <text x={P.l + 2} y={P.t + 2} fontSize="10.5" fontWeight="800" fill={C.ink}>× {fmt(1 / w, 0)}</text>
    </Frame>
  );
}

/* ── 상합과 하합: U − L → 0 이면 적분 가능 ── */
const DF = {
  sq: { name: "x²", mm: (a, b) => [a * a, b * b], g: (x) => x * x, exact: "1/3" },
  step: { name: "계단 함수", mm: (a, b) => (a >= 0.5 ? [0.9, 0.9] : b < 0.5 ? [0.3, 0.3] : [0.3, 0.9]), g: (x) => (x < 0.5 ? 0.3 : 0.9), exact: "0.6" },
  dir: { name: "디리클레 함수", mm: () => [0, 1], g: null, exact: null },
};
const QS = (() => { const o = []; for (let q = 1; q <= 28; q++) for (let p0 = 0; p0 <= q; p0++) { let a = p0, b = q; while (b) [a, b] = [b, a % b]; if (a === 1) o.push(p0 / q); } return o; })();
export function Darboux({ p = {} }) {
  const [k, setK] = useState(DF[p.f] ? p.f : "sq");
  const D = DF[k], per = 1.4;
  const clock = useClock({ period: 7 * per + 2.5, rest: 6 * per + 0.6 });
  const lv = Math.min(6, Math.floor(clock.t / per)), n = 2 ** lv, hstep = 1 / n;
  const cells = Array.from({ length: n }, (_, i) => { const a = i * hstep, b = a + hstep, [m, M] = D.mm(a, b); return { a, b, m, M }; });
  const U = cells.reduce((s, c) => s + c.M * hstep, 0), L = cells.reduce((s, c) => s + c.m * hstep, 0);
  const P = plot({ x0: 0, x1: 1, y0: 0, y1: 1.08, pad: [14, 12, 24, 30] });
  return (
    <Frame clock={clock} title="상합과 하합 — 리만 적분"
      read={<>[0, 1] 을 {n} 칸으로: 상합 U = {fmt(U, 4)}(빨간 테두리), 하합 L = {fmt(L, 4)}(파랑) · U − L = <b>{fmt(U - L, 4)}</b> · {D.exact ? <>칸을 늘리면 U − L → 0 — 적분 가능하고 값은 {D.exact}{k === "step" ? " (끊긴 점이 있어도 칸 하나에만 걸려 차이가 줄어든다)" : ""}</> : <>어느 칸에도 유리수(값 1)와 무리수(값 0)가 다 있어 칸을 아무리 늘려도 U = 1, L = 0 — 리만 적분이 없다(르베그 적분으로는 0)</>}</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sq", "x²"], ["step", "계단"], ["dir", "디리클레"]]} />
        <Slider label="칸 수" min={0} max={6} step={1} value={lv} onChange={(v) => { clock.setT(v * per + 0.05); clock.setPlaying(false); }} show={(v) => String(2 ** v)} />
      </>}>
      {cells.map((c, i) => (
        <g key={i}>
          <rect x={P.X(c.a)} y={P.Y(c.M)} width={P.X(c.b) - P.X(c.a)} height={P.Y(0) - P.Y(c.M)} fill={C.red} opacity="0.1" stroke={C.red} strokeWidth={n > 32 ? 0.5 : 1} />
          <rect x={P.X(c.a)} y={P.Y(c.m)} width={P.X(c.b) - P.X(c.a)} height={P.Y(0) - P.Y(c.m)} fill={C.blue} opacity="0.35" />
        </g>
      ))}
      <Axes p={P} xl="x" yl="" grid={false} xt={[0.5, 1]} yt={[0.5, 1]} />
      {D.g && <path d={P.path(D.g, 0, 1, 400)} fill="none" stroke={C.ink} strokeWidth="1.6" />}
      {!D.g && QS.map((x, i) => <circle key={i} cx={P.X(x)} cy={P.Y(1)} r="1.3" fill={C.ink} />)}
      {!D.g && <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.ink} strokeWidth="1.6" strokeDasharray="1 2" />}
    </Frame>
  );
}

/* ── 점별수렴과 균등수렴 ── */
const FS = {
  pow: { f: (n, x) => x ** n, lim: (x) => (x < 1 ? 0 : 1), name: "fₙ(x) = xⁿ", y0: -0.12, y1: 1.15, supd: () => 1, int: (n) => 1 / (n + 1), intL: 0 },
  bump: { f: (n, x) => 2 * n * x * Math.exp(-n * x * x), lim: () => 0, name: "fₙ(x) = 2nx · exp(−nx²)", y0: -0.3, y1: 6.2, supd: (n) => Math.sqrt(2 * n) * Math.exp(-0.5), int: (n) => 1 - Math.exp(-n), intL: 0 },
  sin: { f: (n, x) => Math.sin(2 * Math.PI * n * x) / n, lim: () => 0, name: "fₙ(x) = sin(2πnx) ÷ n", y0: -1.1, y1: 1.1, supd: (n) => 1 / n, int: () => 0, intL: 0 },
};
export function UnifConv({ p = {} }) {
  const [k, setK] = useState(FS[p.f] ? p.f : "pow");
  const [eps, setEps] = useState(clamp(p.eps ?? 0.15, 0.05, 0.5));
  const F = FS[k];
  const clock = useClock({ period: 13, rest: 10.6 });
  const n = Math.min(40, 1 + Math.floor(clock.t * 4));
  const P = plot({ x0: 0, x1: 1, y0: F.y0, y1: F.y1, pad: [14, 12, 24, 32] });
  const sd = F.supd(n), inTube = sd < eps;
  return (
    <Frame clock={clock} title="점별수렴과 균등수렴"
      read={<>{F.name}, n = {n} · 극한 함수(초록)의 둘레 ±ε 띠 · sup |fₙ − f| = <b>{fmt(sd, 3)}</b>{inTube ? " < ε — 그래프 전체가 띠 안" : " ≥ ε — 띠를 벗어난 곳이 있다"} · {k === "pow" ? "각 xⁿ 은 연속인데 극한은 x = 1 에서 끊긴다 — 1 근처가 늘 띠 밖이라 sup 이 1 에서 줄지 않는다: 점별수렴이지만 균등수렴은 아니다" : k === "bump" ? <>모든 x 에서 fₙ(x) → 0 인데 봉우리는 높아지며 0 쪽으로 몰린다 — ∫ fₙ = {fmt(F.int(n), 3)} → 1 이지만 극한의 적분은 0: 균등수렴이 아니면 극한과 적분의 순서를 바꿀 수 없다</> : "sup |fₙ| = 1/n → 0 — 균등수렴이라 연속성 · 적분은 극한으로 넘어간다. 그래도 도함수 2π cos(2πnx) 는 수렴하지 않는다: 미분에는 더 강한 조건이 필요하다"}</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["pow", "xⁿ"], ["bump", "옮겨 가는 봉우리"], ["sin", "sin(2πnx) ÷ n"]]} />
        <Slider label="ε" min={0.05} max={0.5} step={0.05} value={eps} onChange={setEps} show={(v) => fmt(v, 2)} />
      </>}>
      <rect x={P.X(0)} y={P.Y(Math.min(F.y1, eps))} width={(k === "pow" ? P.X(0.995) : P.X(1)) - P.X(0)} height={Math.max(0, P.Y(Math.max(F.y0, -eps)) - P.Y(Math.min(F.y1, eps)))} fill={C.green} opacity="0.15" />
      <Axes p={P} xl="x" yl="" grid={false} xt={[0.5, 1]} />
      <line x1={P.X(0)} x2={k === "pow" ? P.X(0.995) : P.X(1)} y1={P.Y(0)} y2={P.Y(0)} stroke={C.green} strokeWidth="2" />
      {k === "pow" && <><circle cx={P.X(1)} cy={P.Y(0)} r="3.2" fill={C.card} stroke={C.green} strokeWidth="1.6" /><circle cx={P.X(1)} cy={P.Y(1)} r="3.2" fill={C.green} /></>}
      {[Math.max(1, n - 6), Math.max(1, n - 3)].filter((m) => m < n).map((m) => <path key={m} d={P.path((x) => F.f(m, x), 0, 1, 300)} fill="none" stroke={C.mut} strokeWidth="1" opacity="0.5" />)}
      <path d={P.path((x) => F.f(n, x), 0, 1, 400)} fill="none" stroke={inTube ? C.sp : C.red} strokeWidth="1.8" />
      <text x={P.r} y={P.t + 10} textAnchor="end" fontSize="10.5" fontWeight="800" fill={C.ink}>n = {n}</text>
    </Frame>
  );
}

/* ── 축소 사상: 되풀이하면 고정점으로 ── */
const CM = {
  cos: { g: Math.cos, a: 0, b: 1.2, fix: 0.7390851332, x0: 0.1, name: "g(x) = cos x", L: "|g′| ≤ sin 1 ≈ 0.84 < 1 — 축소 사상" },
  bab: { g: (x) => (x + 2 / x) / 2, a: 0.9, b: 2.2, fix: Math.SQRT2, x0: 2.1, name: "g(x) = (x + 2/x) ÷ 2", L: "고정점에서 g′ = 0 — 오차가 매번 제곱으로 줄어 √2 를 빠르게 찾는다(바빌로니아 방법)" },
  logi: { g: (x) => 3.3 * x * (1 - x), a: 0, b: 1, fix: 1 - 1 / 3.3, x0: 0.5, name: "g(x) = 3.3x(1 − x)", L: "고정점에서 |g′| = 1.3 > 1 — 축소가 아니라 고정점에서 밀려나 두 값 사이를 오간다" },
};
export function Contract({ p = {} }) {
  const [k, setK] = useState(CM[p.g] ? p.g : "cos");
  const M = CM[k];
  const [x0, setX0] = useState(M.x0);
  const seq = useMemo(() => { const o = [x0]; for (let i = 0; i < 14; i++) o.push(M.g(o[i])); return o; }, [k, x0]);
  const clock = useClock({ period: 11, rest: 9.8 });
  const m = Math.min(14, Math.floor(clock.t / 0.62));
  const P = plot({ x0: M.a, x1: M.b, y0: M.a, y1: M.b, pad: [12, 152, 22, 30] });
  const G = plot({ x0: 0, x1: 14, y0: -0.8, y1: 12.5, pad: [22, 12, 24, 236] });
  let d = `M${P.X(seq[0]).toFixed(1)} ${P.Y(M.a).toFixed(1)}`;
  for (let i = 0; i < m; i++) d += `L${P.X(seq[i]).toFixed(1)} ${P.Y(seq[i + 1]).toFixed(1)}L${P.X(seq[i + 1]).toFixed(1)} ${P.Y(seq[i + 1]).toFixed(1)}`;
  const err = seq.map((x) => clamp(-Math.log10(Math.max(1e-13, Math.abs(x - M.fix))), -0.8, 12.5));
  return (
    <Frame clock={clock} title="축소 사상과 고정점"
      read={<>{M.name} 를 되풀이한다: x{sb(m)} = {fmt(seq[m], 6)} · 고정점 x* = {fmt(M.fix, 6)} · {M.L} · 바나흐 고정점 정리: 완비 거리공간에서 축소 사상은 고정점이 꼭 하나 있고, 어디서 시작해도 되풀이하면 그리로 간다(오른쪽: 오차가 일정한 비율로 줄면 곧은 선으로 올라간다)</>}
      controls={<>
        <Seg value={k} onChange={(v) => { setK(v); setX0(CM[v].x0); clock.reset(); }} options={[["cos", "cos x"], ["bab", "√2 찾기"], ["logi", "축소가 아님"]]} />
        <Slider label="시작 x₀" min={M.a + 0.02} max={M.b - 0.02} step={0.02} value={x0} onChange={(v) => { setX0(v); clock.reset(); }} show={(v) => fmt(v, 2)} />
      </>}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill="none" stroke={C.bd} />
      <line x1={P.X(M.a)} y1={P.Y(M.a)} x2={P.X(M.b)} y2={P.Y(M.b)} stroke={C.mut} strokeDasharray="4 3" />
      <path d={P.path(M.g, M.a, M.b, 200)} fill="none" stroke={C.sp} strokeWidth="1.8" />
      <path d={d} fill="none" stroke={C.red} strokeWidth="1.3" />
      <circle cx={P.X(M.fix)} cy={P.Y(M.fix)} r="3.6" fill={C.gold} />
      <circle cx={P.X(seq[m])} cy={P.Y(M.a)} r="3.4" fill={C.red} />
      <text x={P.l + 3} y={P.t + 10} fontSize="9" fill={C.mut}>y = g(x) · 점선 y = x</text>
      <Axes p={G} xl="n" yl="" grid={false} xt={[5, 10]} yt={[4, 8, 12]} yfmt={(v) => "10" + sup(-v)} />
      <path d={G.poly(err.slice(0, m + 1).map((e, i) => [i, e]))} fill="none" stroke={C.red} strokeWidth="1.5" />
      {err.slice(0, m + 1).map((e, i) => <circle key={i} cx={G.X(i)} cy={G.Y(e)} r="2" fill={C.red} />)}
      <text x={G.l + 4} y={G.t - 6} fontSize="9" fill={C.mut}>|xₙ − x*| (위로 갈수록 작다)</text>
    </Frame>
  );
}

/* ── 칸토어 집합: 길이는 0, 원소는 셀 수 없이 많다 ── */
export function Cantor() {
  const per = 1.15;
  const clock = useClock({ period: 8 * per + 2.5, rest: 6 * per + 0.5 });
  const lv = Math.min(7, Math.floor(clock.t / per));
  const X0 = 20, Wd = 320;
  const rows = [];
  let segs = [[0, 1]];
  for (let k = 0; k <= lv; k++) {
    rows.push(segs);
    segs = segs.flatMap(([a, b]) => { const h = (b - a) / 3; return [[a, a + h], [b - h, b]]; });
  }
  const q = 0.25, len = (2 / 3) ** lv;
  return (
    <Frame clock={clock} title="칸토어 집합"
      read={<>[0, 1] 에서 가운데 1/3 을 빼기를 되풀이한다 · {lv} 단계: 구간 {2 ** lv} 개, 남은 길이 (2/3){sup(lv)} = <b>{fmt(len, 4)}</b> → 0 · 그런데 3 진법으로 0 과 2 만으로 쓰이는 수는 끝까지 남는다 — 2 를 1 로 바꾸면 [0, 1] 의 모든 이진수와 하나씩 짝지어지므로, 길이가 0 인데도 원소는 실수만큼 많다(셀 수 없다) · 빨간 점 1/4 = 0.0202…₃ 도 남는다</>}>
      {rows.map((ss, k) => (
        <g key={k}>
          {ss.map(([a, b], i) => {
            const hit = q >= a - 1e-12 && q <= b + 1e-12;
            return <rect key={i} x={X0 + a * Wd} y={22 + k * 21} width={Math.max(0.35, (b - a) * Wd)} height="10" fill={hit ? C.red : C.sp} opacity={hit ? 0.85 : 0.7} />;
          })}
          <text x={X0 - 4} y={31 + k * 21} textAnchor="end" fontSize="9" fill={C.mut}>{k}</text>
        </g>
      ))}
      <line x1={X0 + q * Wd} x2={X0 + q * Wd} y1="16" y2={34 + lv * 21} stroke={C.red} strokeWidth="1" strokeDasharray="2 3" />
      {[[0, "0"], [1 / 3, "1/3"], [2 / 3, "2/3"], [1, "1"]].map(([v, t]) => <text key={t} x={X0 + v * Wd} y="13" textAnchor="middle" fontSize="9.5" fill={C.mut}>{t}</text>)}
    </Frame>
  );
}
