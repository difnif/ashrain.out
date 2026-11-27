// 수치해석 그림 — 부동소수점과 상쇄 · 근 찾기의 수렴 속도 · 보간과 룽게 현상 · 수치 적분의 차수 · 조건수 · 야코비와 가우스–자이델 · 거듭제곱법 · 미분방정식 풀이의 안정성
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, fmt, clamp, lerp, sup, useClock } from "./kit.jsx";

const f32 = Math.fround;
const sci = (v) => {
  if (!Number.isFinite(v)) return "—";
  if (v === 0) return "0";
  const e = Math.floor(Math.log10(Math.abs(v)));
  if (e >= -2 && e <= 3) return fmt(v, 4);
  const m = v / 10 ** e;
  return `${fmt(m, 2)} × 10${sup(e)}`;
};
const plane = (ox, oy, s) => ({ X: (z) => ox + z[0] * s, Y: (z) => oy - z[1] * s, s, ox, oy });
const pathOf = (P, pts) => pts.map((z, i) => (i ? "L" : "M") + P.X(z).toFixed(1) + " " + P.Y(z).toFixed(1)).join("") || "M0 0";

/* ── 부동소수점: 간격은 크기에 비례, 앞자리가 지워지는 상쇄, 쌓이는 반올림 ── */
const SUMS = (() => {
  const out = []; let s = 0, k = 0, c = 0; const t = f32(0.1);
  for (let n = 1; n <= 20000; n++) {
    s = f32(s + t);
    const y = f32(t - c), z = f32(k + y); c = f32(f32(z - k) - y); k = z;
    if (Number.isInteger(Math.log2(n)) || n % 250 === 0) out.push([n, Math.abs(s - n / 10), Math.abs(k - n / 10)]);
  }
  return out;
})();
const TOY = (() => { const o = []; for (let e = -2; e <= 2; e++) for (let m = 8; m < 16; m++) o.push((m / 8) * 2 ** e); return o; })();
export function Float({ p = {} }) {
  const [m, setM] = useState(["line", "cancel", "sum"].includes(p.mode) ? p.mode : "line");
  const clock = useClock({ period: 11, rest: 9 });
  const u = clamp(clock.t / 8.5, 0, 1);
  if (m === "line") {
    const x = lerp(0.3, 7.7, u), fl = TOY.reduce((b, v) => (Math.abs(v - x) < Math.abs(b - x) ? v : b), TOY[0]);
    const P = plot({ x0: 0, x1: 8, y0: 0, y1: 1, pad: [10, 12, 30, 12] });
    const Y = 120;
    return (
      <Frame clock={clock} title="부동소수점 — 간격은 크기에 비례한다"
        read={<>가수 3 비트짜리 장난감 부동소수점(1.xxx × 2ᵉ): 1 과 2 사이는 1/8 간격, 2 와 4 사이는 1/4 간격 — 수가 커질수록 간격도 커진다 · x = {fmt(x, 3)} 은 가장 가까운 {fmt(fl, 4)} 로 저장되고 상대 오차 {fmt(Math.abs(x - fl) / x, 4)} 는 늘 1/16 = 0.0625 이하 · 실제 double 은 가수 52 비트라 상대 오차가 2{sup(-53)} ≈ 1.1 × 10⁻¹⁶ 이하(기계 엡실론의 절반)</>}
        controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["line", "간격"], ["cancel", "상쇄"], ["sum", "쌓이는 오차"]]} />}>
        <line x1={P.l} x2={P.r} y1={Y} y2={Y} stroke={C.mut} />
        {TOY.map((v, i) => <line key={i} x1={P.X(v)} x2={P.X(v)} y1={Y - 12} y2={Y} stroke={C.blue} strokeWidth="1.2" />)}
        {[0, 1, 2, 4, 8].map((v) => <text key={v} x={P.X(v)} y={Y + 16} textAnchor="middle" fontSize="10" fill={C.mut}>{v}</text>)}
        {[[1, 2, "1/8"], [2, 4, "1/4"], [4, 8, "1/2"]].map(([a, b, t]) => <text key={t} x={P.X((a + b) / 2)} y={Y - 40} textAnchor="middle" fontSize="9.5" fill={C.mut}>간격 {t}</text>)}
        <line x1={P.X(x)} x2={P.X(x)} y1={Y - 30} y2={Y + 4} stroke={C.red} strokeWidth="1.6" />
        <circle cx={P.X(fl)} cy={Y - 6} r="4" fill={C.gold} />
        <text x={P.X(x)} y={Y - 33} textAnchor="middle" fontSize="10.5" fontWeight="800" fill={C.red}>x</text>
        <text x={P.l} y="20" fontSize="10" fill={C.mut}>파랑 = 저장할 수 있는 수 · 노랑 = x 가 실제로 저장되는 값</text>
      </Frame>
    );
  }
  if (m === "cancel") {
    const xs = Array.from({ length: 70 }, (_, i) => 10 ** -(0.3 + (4.9 * i) / 69));
    const shown = Math.max(2, Math.round(70 * u));
    const naive = (x) => { const c = f32(Math.cos(x)), num = f32(1 - c), xx = f32(x), den = f32(xx * xx); return f32(num / den); };
    const stable = (x) => { const s = f32(Math.sin(f32(x / 2))), xx = f32(x), den = f32(xx * xx); return f32(f32(2 * f32(s * s)) / den); };
    const P = plot({ x0: 0.3, x1: 5.2, y0: -0.05, y1: 1.25, pad: [14, 12, 24, 36] });
    const xc = xs[shown - 1];
    return (
      <Frame clock={clock} title="파국적 상쇄"
        read={<>(1 − cos x) ÷ x² 은 x → 0 에서 1/2 로 간다 · 유효숫자 약 7 자리인 float32 로 그대로 계산하면(빨강) x 가 작아질수록 cos x 가 1 에 붙어 1 − cos x 의 앞자리가 모두 지워진다 — 지금 x = {sci(xc)}: 그대로 {fmt(naive(xc), 4)}, 고쳐 쓴 식 {fmt(stable(xc), 4)} · 같은 값을 2 sin²(x/2) ÷ x² 로 고쳐 쓰면(파랑) 빼기가 없어 1/2 을 지킨다</>}
        controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["line", "간격"], ["cancel", "상쇄"], ["sum", "쌓이는 오차"]]} />}>
        <line x1={P.l} x2={P.r} y1={P.Y(0.5)} y2={P.Y(0.5)} stroke={C.green} strokeDasharray="4 3" />
        <Axes p={P} xl="" yl="" grid={false} xt={[]} yt={[0.5, 1]} />
        {[1, 2, 3, 4, 5].map((v) => <text key={v} x={P.X(v)} y={P.b + 14} textAnchor="middle" fontSize="9.5" fill={C.mut}>10{sup(-v)}</text>)}
        <text x={P.r} y={P.t + 10} textAnchor="end" fontSize="9.5" fill={C.ink} fontStyle="italic">x (오른쪽으로 갈수록 작다)</text>
        <path d={P.poly(xs.slice(0, shown).map((x) => [-Math.log10(x), clamp(stable(x), -0.05, 1.25)]))} fill="none" stroke={C.blue} strokeWidth="2" />
        <path d={P.poly(xs.slice(0, shown).map((x) => [-Math.log10(x), clamp(naive(x), -0.05, 1.25)]))} fill="none" stroke={C.red} strokeWidth="1.6" />
        {xs.slice(0, shown).map((x, i) => <circle key={i} cx={P.X(-Math.log10(x))} cy={P.Y(clamp(naive(x), -0.05, 1.25))} r="1.8" fill={C.red} />)}
      </Frame>
    );
  }
  const N = Math.round(10 ** (4.3 * u + 0.3));
  const S = SUMS;
  const vis = S.filter(([n]) => n <= N);
  const last = vis[vis.length - 1] || S[0];
  const P = plot({ x0: 0, x1: 4.4, y0: -9, y1: 1, pad: [14, 12, 24, 46] });
  const pt = (e) => clamp(Math.log10(Math.max(1e-9, e)), -9, 1);
  return (
    <Frame clock={clock} title="쌓이는 반올림 오차"
      read={<>float32 로 0.1 을 {last[0]} 번 더했다 · 그대로 더하기(빨강)의 오차 {sci(last[1])} — 합이 커질수록 작은 0.1 의 끝자리가 잘려 나가 오차가 쌓인다 · 카한의 보정 덧셈(파랑)은 잘린 몫을 따로 모아 되돌려, 합이 늘 float32 의 가장 가까운 눈금 근처에 머문다(지금 오차 {sci(last[2])})</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["line", "간격"], ["cancel", "상쇄"], ["sum", "쌓이는 오차"]]} />}>
      <Axes p={P} xl="" yl="" grid={false} xt={[]} yt={[-8, -6, -4, -2, 0]} yfmt={(v) => "10" + sup(v)} />
      {[1, 2, 3, 4].map((v) => <text key={v} x={P.X(v)} y={P.b + 14} textAnchor="middle" fontSize="9.5" fill={C.mut}>10{sup(v)}</text>)}
      <text x={P.r} y={P.b - 4} textAnchor="end" fontSize="9.5" fill={C.ink} fontStyle="italic">더한 횟수</text>
      <text x={P.l + 4} y={P.t + 8} fontSize="9.5" fill={C.mut}>오차</text>
      <path d={P.poly(vis.map(([n, a]) => [Math.log10(n), pt(a)]))} fill="none" stroke={C.red} strokeWidth="1.8" />
      <path d={P.poly(vis.map(([n, , b]) => [Math.log10(n), pt(b)]))} fill="none" stroke={C.blue} strokeWidth="1.8" />
    </Frame>
  );
}

/* ── 근 찾기의 수렴 속도: 맞은 자릿수 ── */
const RF = {
  sq: { f: (x) => x * x - 2, df: (x) => 2 * x, g: (x) => x - (x * x - 2) / 4, root: Math.SQRT2, a: 1, b: 2, x0: 2, name: "x² − 2 = 0" },
  cos: { f: (x) => Math.cos(x) - x, df: (x) => -Math.sin(x) - 1, g: Math.cos, root: 0.7390851332151607, a: 0, b: 1, x0: 1, name: "cos x − x = 0" },
};
function runs(F) {
  const K = 12, out = { bis: [], fix: [], sec: [], nwt: [] };
  let a = F.a, b = F.b;
  for (let k = 0; k <= K; k++) { const m = (a + b) / 2; out.bis.push(Math.abs(m - F.root)); if (F.f(a) * F.f(m) <= 0) b = m; else a = m; }
  let x = F.x0; for (let k = 0; k <= K; k++) { out.fix.push(Math.abs(x - F.root)); x = F.g(x); }
  let x0 = F.a, x1 = F.b; out.sec.push(Math.abs(x1 - F.root));
  for (let k = 1; k <= K; k++) { const f0 = F.f(x0), f1 = F.f(x1); const x2 = f1 === f0 ? x1 : x1 - (f1 * (x1 - x0)) / (f1 - f0); x0 = x1; x1 = x2; out.sec.push(Math.abs(x1 - F.root)); }
  x = F.x0; for (let k = 0; k <= K; k++) { out.nwt.push(Math.abs(x - F.root)); const d = F.df(x); x = d ? x - F.f(x) / d : x; }
  return out;
}
const digits = (e) => clamp(-Math.log10(Math.max(1e-16, e)), 0, 16);
export function ConvRate({ p = {} }) {
  const [k, setK] = useState(RF[p.f] ? p.f : "sq");
  const R = useMemo(() => runs(RF[k]), [k]);
  const clock = useClock({ period: 12, rest: 9.4 });
  const n = Math.min(12, Math.floor(clock.t / 0.75));
  const P = plot({ x0: 0, x1: 12.6, y0: 0, y1: 16.5, pad: [14, 56, 24, 34] });
  const L = [["bis", C.gold, "이분법"], ["fix", C.green, "고정점"], ["sec", C.violet, "할선법"], ["nwt", C.red, "뉴턴"]];
  const labY = (() => { const ys = L.map(([key]) => P.Y(digits(R[key][n]))); const ord = ys.map((y, i) => [y, i]).sort((a2, b2) => a2[0] - b2[0]); for (let j = 1; j < ord.length; j++) if (ord[j][0] - ord[j - 1][0] < 12) ord[j][0] = ord[j - 1][0] + 12; const out = []; ord.forEach(([y, i]) => { out[i] = y; }); return out; })();
  return (
    <Frame clock={clock} title="근 찾기 — 맞은 자릿수의 경주"
      read={<>{RF[k].name} · {n} 번 반복 뒤 맞은 자릿수: 이분법 {fmt(digits(R.bis[n]), 1)}, 고정점 반복 {fmt(digits(R.fix[n]), 1)}, 할선법 {fmt(digits(R.sec[n]), 1)}, 뉴턴 {fmt(digits(R.nwt[n]), 1)} · 이분법과 고정점 반복은 매번 일정한 비율로 줄어 곧은 선(일차 수렴), 뉴턴은 맞은 자릿수가 매번 약 두 배(이차 수렴), 할선법은 약 1.6 배 — 16 자리에서 멈추는 것은 컴퓨터 숫자의 한계</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["sq", "x² − 2"], ["cos", "cos x − x"]]} />}>
      <Axes p={P} xl="반복" yl="맞은 자릿수" grid={false} xt={[4, 8, 12]} yt={[4, 8, 12, 16]} />
      {L.map(([key, col, name]) => {
        const pts = R[key].slice(0, n + 1).map((e, i) => [i, digits(e)]);
        return (
          <g key={key}>
            <path d={P.poly(pts)} fill="none" stroke={col} strokeWidth="2" />
            {pts.map(([i, d]) => <circle key={i} cx={P.X(i)} cy={P.Y(d)} r="2.4" fill={col} />)}
            <text x={P.r + 4} y={labY[L.findIndex((q) => q[0] === key)] + 4} fontSize="9.5" fontWeight="800" fill={col}>{name}</text>
          </g>
        );
      })}
    </Frame>
  );
}

/* ── 보간: 등간격 고차 다항식의 출렁임(룽게) · 체비쇼프 점 · 스플라인 ── */
const runge = (x) => 1 / (1 + 25 * x * x);
function bary(xs, ys) {
  const w = xs.map((xi, i) => 1 / xs.reduce((pr, xj, j) => (j === i ? pr : pr * (xi - xj)), 1));
  return (x) => { let num = 0, den = 0; for (let i = 0; i < xs.length; i++) { const d = x - xs[i]; if (Math.abs(d) < 1e-14) return ys[i]; num += (w[i] * ys[i]) / d; den += w[i] / d; } return num / den; };
}
function spline(xs, ys) {
  const n = xs.length, h = xs[1] - xs[0], M = Array(n).fill(0);
  if (n > 2) {
    const m = n - 2, a = Array(m).fill(1), b = Array(m).fill(4), c = Array(m).fill(1), d = Array.from({ length: m }, (_, i) => (6 / (h * h)) * (ys[i + 2] - 2 * ys[i + 1] + ys[i]));
    for (let i = 1; i < m; i++) { const r = a[i] / b[i - 1]; b[i] -= r * c[i - 1]; d[i] -= r * d[i - 1]; }
    const s = Array(m).fill(0); s[m - 1] = d[m - 1] / b[m - 1];
    for (let i = m - 2; i >= 0; i--) s[i] = (d[i] - c[i] * s[i + 1]) / b[i];
    for (let i = 0; i < m; i++) M[i + 1] = s[i];
  }
  return (x) => {
    const i = clamp(Math.floor((x - xs[0]) / h), 0, n - 2), x0 = xs[i], x1 = xs[i + 1];
    return (M[i] * (x1 - x) ** 3) / (6 * h) + (M[i + 1] * (x - x0) ** 3) / (6 * h) + (ys[i] / h - (M[i] * h) / 6) * (x1 - x) + (ys[i + 1] / h - (M[i + 1] * h) / 6) * (x - x0);
  };
}
export function Interp({ p = {} }) {
  const [kind, setKind] = useState(["eq", "cheb", "spl"].includes(p.nodes) ? p.nodes : "eq");
  const per = 1.1, NS = [3, 5, 7, 9, 11, 13, 15, 17, 19];
  const clock = useClock({ period: NS.length * per + 2, rest: 5 * per + 0.4 });
  const n = NS[Math.min(NS.length - 1, Math.floor(clock.t / per))];
  const xs = kind === "cheb" ? Array.from({ length: n }, (_, i) => Math.cos(((2 * i + 1) * Math.PI) / (2 * n))).reverse() : Array.from({ length: n }, (_, i) => -1 + (2 * i) / (n - 1));
  const ys = xs.map(runge);
  const pf = kind === "spl" ? spline(xs, ys) : bary(xs, ys);
  let mx = 0; for (let i = 0; i <= 400; i++) { const x = -1 + i / 200; mx = Math.max(mx, Math.abs(pf(x) - runge(x))); }
  const P = plot({ x0: -1.05, x1: 1.05, y0: -0.6, y1: 1.35, pad: [14, 12, 24, 32] });
  return (
    <Frame clock={clock} title="보간 — 룽게 현상"
      read={<>f(x) = 1 ÷ (1 + 25x²)(파랑)를 점 {n} 개로 보간했다(빨강) · 최대 오차 <b>{fmt(mx, 3)}</b> · {kind === "eq" ? "등간격 점을 지나는 고차 다항식은 점을 늘릴수록 양 끝에서 더 크게 출렁인다(룽게 현상)" : kind === "cheb" ? "체비쇼프 점(양 끝으로 갈수록 촘촘)을 쓰면 점을 늘릴수록 오차가 줄어든다" : "조각마다 3 차식을 매끈하게 이어 붙인 스플라인은 출렁이지 않는다 — 실제 곡선 그리기와 글꼴이 이 방법을 쓴다"}</>}
      controls={<Seg value={kind} onChange={(v) => { setKind(v); clock.reset(); }} options={[["eq", "등간격 다항식"], ["cheb", "체비쇼프 점"], ["spl", "3 차 스플라인"]]} />}>
      <Axes p={P} xl="x" yl="" grid={false} xt={[-1, -0.5, 0.5, 1]} yt={[0.5, 1]} />
      <path d={P.path(runge, -1, 1, 300)} fill="none" stroke={C.blue} strokeWidth="2.2" />
      <path d={P.path(pf, -1, 1, 500)} fill="none" stroke={C.red} strokeWidth="1.6" />
      {xs.map((x, i) => <circle key={i} cx={P.X(x)} cy={P.Y(ys[i])} r="3.2" fill={C.ink} />)}
      <text x={P.r} y={P.t + 10} textAnchor="end" fontSize="10.5" fontWeight="800" fill={C.ink}>점 {n} 개</text>
    </Frame>
  );
}

/* ── 수치 적분: 사다리꼴 · 중점 · 심프슨, 오차의 차수 ── */
const QF = (x) => Math.sin(x);
const QA = 0, QB = Math.PI, QE = 2;
const trap = (n) => { const h = (QB - QA) / n; let s = (QF(QA) + QF(QB)) / 2; for (let i = 1; i < n; i++) s += QF(QA + i * h); return s * h; };
const midp = (n) => { const h = (QB - QA) / n; let s = 0; for (let i = 0; i < n; i++) s += QF(QA + (i + 0.5) * h); return s * h; };
const simp = (n) => { const h = (QB - QA) / n; let s = QF(QA) + QF(QB); for (let i = 1; i < n; i++) s += (i % 2 ? 4 : 2) * QF(QA + i * h); return (s * h) / 3; };
export function Quad({ p = {} }) {
  const [mth, setMth] = useState(["trap", "mid", "simp"].includes(p.m) ? p.m : "trap");
  const NS = [2, 4, 8, 16, 32, 64], per = 1.3;
  const clock = useClock({ period: NS.length * per + 2, rest: 2 * per + 0.3 });
  const idx = Math.min(NS.length - 1, Math.floor(clock.t / per)), n = NS[idx];
  const errs = useMemo(() => NS.map((m) => [Math.abs(trap(m) - QE), Math.abs(midp(m) - QE), Math.abs(simp(m) - QE)]), []);
  const P = plot({ x0: 0, x1: Math.PI, y0: 0, y1: 1.15, pad: [16, 186, 24, 26] });
  const G = plot({ x0: 0.2, x1: 1.9, y0: -10, y1: 0, pad: [16, 12, 24, 216] });
  const h = Math.PI / n, cells = Array.from({ length: n }, (_, i) => [i * h, (i + 1) * h]);
  const val = mth === "trap" ? trap(n) : mth === "mid" ? midp(n) : simp(n);
  return (
    <Frame clock={clock} title="수치 적분 — 오차가 줄어드는 빠르기"
      read={<>∫ sin x dx (0 → π) = 2 를 {n} 칸으로: 사다리꼴 오차 {sci(errs[idx][0])}, 중점 {sci(errs[idx][1])}, 심프슨 {sci(errs[idx][2])} · 지금 그림({mth === "trap" ? "사다리꼴" : mth === "mid" ? "중점" : "심프슨"}) = {fmt(val, 6)} · 칸을 두 배로 하면 사다리꼴 · 중점은 오차가 1/4(2 차 수렴), 심프슨은 1/16(4 차 수렴) — 오른쪽 로그 그림의 기울기가 그 차수다</>}
      controls={<Seg value={mth} onChange={setMth} options={[["trap", "사다리꼴"], ["mid", "중점"], ["simp", "심프슨"]]} />}>
      {mth === "trap" && cells.map(([a, b], i) => <path key={i} d={`M${P.X(a)} ${P.Y(0)}L${P.X(a)} ${P.Y(QF(a))}L${P.X(b)} ${P.Y(QF(b))}L${P.X(b)} ${P.Y(0)}Z`} fill={C.gold} opacity="0.35" stroke={C.gold} strokeWidth="0.8" />)}
      {mth === "mid" && cells.map(([a, b], i) => { const y = QF((a + b) / 2); return <rect key={i} x={P.X(a)} y={P.Y(y)} width={P.X(b) - P.X(a)} height={P.Y(0) - P.Y(y)} fill={C.green} opacity="0.3" stroke={C.green} strokeWidth="0.8" />; })}
      {mth === "simp" && Array.from({ length: n / 2 }, (_, i) => {
        const a = 2 * i * h, m2 = a + h, b = a + 2 * h, fa = QF(a), fm = QF(m2), fb = QF(b);
        const q = (x) => fa * ((x - m2) * (x - b)) / ((a - m2) * (a - b)) + fm * ((x - a) * (x - b)) / ((m2 - a) * (m2 - b)) + fb * ((x - a) * (x - m2)) / ((b - a) * (b - m2));
        const pts = Array.from({ length: 21 }, (_, j) => { const x = a + (2 * h * j) / 20; return [x, q(x)]; });
        return <path key={i} d={P.poly([[a, 0], ...pts, [b, 0]]) + "Z"} fill={C.violet} opacity="0.3" stroke={C.violet} strokeWidth="0.8" />;
      })}
      <Axes p={P} xl="x" yl="" grid={false} xt={[Math.PI / 2, Math.PI]} xfmt={(v) => (v < 2 ? "π/2" : "π")} yt={[1]} />
      <path d={P.path(QF, 0, Math.PI, 200)} fill="none" stroke={C.ink} strokeWidth="1.8" />
      <Axes p={G} xl="" yl="" grid={false} xt={[]} yt={[-8, -6, -4, -2]} yfmt={(v) => "10" + sup(v)} />
      {NS.map((m) => <text key={m} x={G.X(Math.log10(m))} y={G.b + 14} textAnchor="middle" fontSize="9" fill={C.mut}>{m}</text>)}
      {[[0, C.gold], [1, C.green], [2, C.violet]].map(([j, col]) => (
        <g key={j}>
          <path d={G.poly(NS.slice(0, idx + 1).map((m, i) => [Math.log10(m), Math.log10(Math.max(1e-12, errs[i][j]))]))} fill="none" stroke={col} strokeWidth="1.8" />
          {NS.slice(0, idx + 1).map((m, i) => <circle key={m} cx={G.X(Math.log10(m))} cy={G.Y(clamp(Math.log10(Math.max(1e-12, errs[i][j])), -10, 0))} r="2.2" fill={col} />)}
        </g>
      ))}
      <text x={G.r} y={G.t + 16} textAnchor="end" fontSize="9" fill={C.mut}>오차 · 칸 수(로그)</text>
    </Frame>
  );
}

/* ── 조건수: 거의 평행한 두 직선은 작은 흔들림을 크게 키운다 ── */
export function CondNum({ p = {} }) {
  const [deg, setDeg] = useState(clamp(p.deg ?? 20, 3, 90));
  const th = (deg * Math.PI) / 180, c = Math.cos(th), s = Math.sin(th);
  const kappa = Math.sqrt((1 + c) / (1 - c));
  const clock = useClock({ period: 8, rest: 1.2 });
  const eps = 0.08, phi = (2 * Math.PI * clock.t) / 8;
  const dx = (d) => [d[0], (-c * d[0] + d[1]) / s];
  const cur = dx([eps * Math.cos(phi), eps * Math.sin(phi)]);
  const ring = Array.from({ length: 97 }, (_, i) => { const a = (2 * Math.PI * i) / 96; return dx([eps * Math.cos(a), eps * Math.sin(a)]); });
  const maxd = eps / Math.sqrt(1 - c);
  const P = plane(180 - 55, 112 + 55, 55);
  const line = (a, b, col, dash) => { const n2 = a[0] * a[0] + a[1] * a[1], q = [(b * a[0]) / n2, (b * a[1]) / n2], t = [-a[1], a[0]]; return <line x1={P.X([q[0] - 5 * t[0], q[1] - 5 * t[1]])} y1={P.Y([q[0] - 5 * t[0], q[1] - 5 * t[1]])} x2={P.X([q[0] + 5 * t[0], q[1] + 5 * t[1]])} y2={P.Y([q[0] + 5 * t[0], q[1] + 5 * t[1]])} stroke={col} strokeWidth={dash ? 1 : 1.8} strokeDasharray={dash ? "4 3" : undefined} />; };
  const db = [eps * Math.cos(phi), eps * Math.sin(phi)];
  return (
    <Frame clock={clock} title="조건수 — 오차를 키우는 배율"
      read={<>두 직선 x = 1, (cos θ)x + (sin θ)y = cos θ + sin θ 의 교점은 (1, 1) · 사잇각 θ = {deg}° · 오른쪽 변을 0.08 만큼 흔들면(점선) 해는 노란 고리 위를 움직이며 최대 <b>{fmt(maxd, 3)}</b> 까지 벗어난다 · 조건수 κ = {fmt(kappa, 2)} — 상대 오차는 κ 배까지 불어난다. 거의 평행하면(θ → 0) κ 가 커져 작은 측정 오차에도 답이 크게 흔들린다</>}
      controls={<Slider label="사잇각 θ" min={3} max={90} step={1} value={deg} onChange={setDeg} show={(v) => v + "°"} />}>
      {line([1, 0], 1, C.blue)}
      {line([c, s], c + s, C.red)}
      {line([1, 0], 1 + db[0], C.blue, true)}
      {line([c, s], c + s + db[1], C.red, true)}
      <path d={pathOf(P, ring.map((d) => [1 + d[0], 1 + d[1]]))} fill="none" stroke={C.gold} strokeWidth="1.6" />
      <circle cx={P.X([1, 1])} cy={P.Y([1, 1])} r="3.5" fill={C.ink} />
      <circle cx={P.X([1 + cur[0], 1 + cur[1]])} cy={P.Y([1 + cur[0], 1 + cur[1]])} r="4.5" fill={C.gold} stroke={C.ink} strokeWidth="0.8" />
      <text x="12" y="18" fontSize="10.5" fontWeight="800" fill={C.ink}>κ = {fmt(kappa, 2)}</text>
    </Frame>
  );
}

/* ── 반복법: 야코비와 가우스–자이델 ── */
const SYS = {
  dom: { A: [[4, 1], [1, 3]], b: [6, 7], sol: [1, 2], name: "4x + y = 6, x + 3y = 7" },
  bad: { A: [[1, 2], [2, 1]], b: [3, 3], sol: [1, 1], name: "x + 2y = 3, 2x + y = 3" },
};
export function Jacobi({ p = {} }) {
  const [k, setK] = useState(SYS[p.sys] ? p.sys : "dom");
  const S = SYS[k], [[a, b], [c, d]] = S.A, [e, f] = S.b;
  const K = 10;
  const J = useMemo(() => { const o = [[0, 0]]; for (let i = 0; i < K; i++) { const [x, y] = o[i]; o.push([(e - b * y) / a, (f - c * x) / d]); } return o; }, [k]);
  const G = useMemo(() => { const o = [[0, 0]], st = [[0, 0]]; for (let i = 0; i < K; i++) { const [x, y] = o[i]; const nx = (e - b * y) / a, ny = (f - c * nx) / d; st.push([nx, y], [nx, ny]); o.push([nx, ny]); } return { o, st }; }, [k]);
  const clock = useClock({ period: 10, rest: 6.6 });
  const n = Math.min(K, Math.floor(clock.t / 0.8));
  const P = plane(180 - S.sol[0] * 46, 120 + S.sol[1] * 46 - 46, 46);
  const ok = (q) => Math.abs(q[0]) < 6 && Math.abs(q[1]) < 6;
  const err = (q) => Math.hypot(q[0] - S.sol[0], q[1] - S.sol[1]);
  const ln = (r, rhs, col) => { const pts = r[1] !== 0 ? [[-6, (rhs - r[0] * -6) / r[1]], [8, (rhs - r[0] * 8) / r[1]]] : [[rhs / r[0], -6], [rhs / r[0], 8]]; return <line x1={P.X(pts[0])} y1={P.Y(pts[0])} x2={P.X(pts[1])} y2={P.Y(pts[1])} stroke={col} strokeWidth="1.3" opacity="0.7" />; };
  return (
    <Frame clock={clock} title="반복법 — 야코비와 가우스–자이델"
      read={<>{S.name}, 해 ({S.sol[0]}, {S.sol[1]}) · (0, 0) 에서 {n} 번 반복한 뒤 오차: 야코비(파랑) {sci(err(J[n]))}, 가우스–자이델(빨강) {sci(err(G.o[n]))} · 야코비는 두 값을 한꺼번에 고치고, 가우스–자이델은 고친 x 를 바로 다음 식에 써서 계단 모양으로 간다 · {k === "dom" ? "대각 성분이 커서(대각 우세) 둘 다 해로 가고, 가우스–자이델이 약 두 배 빠르다" : "대각 우세가 아니면 둘 다 해에서 점점 멀어진다 — 반복법을 쓰기 전에 수렴 조건(반복 행렬의 스펙트럼 반지름 < 1)을 확인해야 한다"}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["dom", "대각 우세"], ["bad", "우세 아님"]]} />}>
      {ln([a, b], e, C.mut)}
      {ln([c, d], f, C.mut)}
      <path d={pathOf(P, J.slice(0, n + 1).filter(ok))} fill="none" stroke={C.blue} strokeWidth="1.8" />
      {J.slice(0, n + 1).filter(ok).map((q, i) => <circle key={i} cx={P.X(q)} cy={P.Y(q)} r="3" fill={C.blue} />)}
      <path d={pathOf(P, G.st.slice(0, 2 * n + 1).filter(ok))} fill="none" stroke={C.red} strokeWidth="1.6" />
      {G.o.slice(0, n + 1).filter(ok).map((q, i) => <circle key={i} cx={P.X(q)} cy={P.Y(q)} r="3" fill={C.red} />)}
      <circle cx={P.X(S.sol)} cy={P.Y(S.sol)} r="5" fill="none" stroke={C.green} strokeWidth="2" />
      <circle cx={P.X([0, 0])} cy={P.Y([0, 0])} r="2.5" fill={C.ink} />
      <text x={P.X([0, 0]) + 5} y={P.Y([0, 0]) + 12} fontSize="9" fill={C.mut}>(0, 0)</text>
    </Frame>
  );
}

/* ── 거듭제곱법: 곱하고 길이를 맞추기를 되풀이하면 가장 큰 고윳값의 방향으로 ── */
export function PowerIt({ p = {} }) {
  const [r, setR] = useState(clamp(p.r ?? 0.5, 0.1, 0.95));
  const al = Math.PI / 6, v1 = [Math.cos(al), Math.sin(al)], v2 = [-Math.sin(al), Math.cos(al)];
  const l1 = 3, l2 = 3 * r;
  const A = [[l1 * v1[0] * v1[0] + l2 * v2[0] * v2[0], l1 * v1[0] * v1[1] + l2 * v2[0] * v2[1]], [l1 * v1[0] * v1[1] + l2 * v2[0] * v2[1], l1 * v1[1] * v1[1] + l2 * v2[1] * v2[1]]];
  const K = 16;
  const xs = useMemo(() => { const o = [[Math.cos((165 * Math.PI) / 180), Math.sin((165 * Math.PI) / 180)]]; for (let i = 0; i < K; i++) { const [x, y] = o[i]; const nx = A[0][0] * x + A[0][1] * y, ny = A[1][0] * x + A[1][1] * y, m = Math.hypot(nx, ny); o.push([nx / m, ny / m]); } return o; }, [r]);
  const clock = useClock({ period: 12, rest: 8.2 });
  const n = Math.min(K, Math.floor(clock.t / 0.6));
  const x = xs[n], ray = (x[0] * (A[0][0] * x[0] + A[0][1] * x[1]) + x[1] * (A[1][0] * x[0] + A[1][1] * x[1]));
  const ang = (q) => Math.abs(Math.asin(clamp(Math.abs(q[0] * v1[1] - q[1] * v1[0]), 0, 1)));
  const P = plane(100, 112, 78);
  const G = plot({ x0: 0, x1: K, y0: -12, y1: 0.4, pad: [22, 12, 24, 224] });
  return (
    <Frame clock={clock} title="거듭제곱법 — 가장 큰 고윳값 찾기"
      read={<>벡터에 A 를 곱하고 길이를 1 로 맞추기를 {n} 번 했다 · 고윳값 λ₁ = 3, λ₂ = {fmt(l2, 2)} · 매번 λ₂ 쪽 성분이 λ₂/λ₁ = {fmt(r, 2)} 배로 줄어 벡터가 첫째 고유벡터(노란 선) 쪽으로 돌아선다 · 레일리 몫 xᵀAx = <b>{fmt(ray, 6)}</b> → λ₁ · 비가 1 에 가까울수록 느리다 — 구글의 페이지랭크가 바로 이 방법이다</>}
      controls={<Slider label="λ₂ ÷ λ₁" min={0.1} max={0.95} step={0.05} value={r} onChange={(v) => { setR(v); clock.reset(); }} show={(v) => fmt(v, 2)} />}>
      <circle cx={P.ox} cy={P.oy} r={P.s} fill="none" stroke={C.bd} />
      <line x1={P.X([-1.2 * v1[0], -1.2 * v1[1]])} y1={P.Y([-1.2 * v1[0], -1.2 * v1[1]])} x2={P.X([1.2 * v1[0], 1.2 * v1[1]])} y2={P.Y([1.2 * v1[0], 1.2 * v1[1]])} stroke={C.gold} strokeWidth="2" />
      <line x1={P.X([-1.2 * v2[0], -1.2 * v2[1]])} y1={P.Y([-1.2 * v2[0], -1.2 * v2[1]])} x2={P.X([1.2 * v2[0], 1.2 * v2[1]])} y2={P.Y([1.2 * v2[0], 1.2 * v2[1]])} stroke={C.mut} strokeWidth="1" strokeDasharray="4 3" />
      {xs.slice(0, n + 1).map((q, i) => <circle key={i} cx={P.X(q)} cy={P.Y(q)} r={i === n ? 4.5 : 2.6} fill={i === n ? C.red : C.sp} opacity={i === n ? 1 : 0.6} />)}
      <line x1={P.ox} y1={P.oy} x2={P.X(x)} y2={P.Y(x)} stroke={C.red} strokeWidth="2" />
      <Axes p={G} xl="반복" yl="" grid={false} xt={[4, 8, 12, 16]} yt={[-12, -8, -4]} yfmt={(v) => "10" + sup(v)} />
      <path d={G.poly(xs.slice(0, n + 1).map((q, i) => [i, clamp(Math.log10(Math.max(1e-13, ang(q))), -12, 0.4)]))} fill="none" stroke={C.red} strokeWidth="1.6" />
      <text x={G.l + 4} y={G.t - 8} fontSize="9" fill={C.mut}>고유벡터와의 각(라디안)</text>
    </Frame>
  );
}

/* ── 미분방정식 풀이의 안정성: y′ = −10y ── */
export function OdeStab({ p = {} }) {
  const [h, setH] = useState(clamp(p.h ?? 0.15, 0.02, 0.32));
  const lam = 10, z = -h * lam, T = 2;
  const N = Math.ceil(T / h);
  const fac = { ex: 1 + z, im: 1 / (1 - z), rk: 1 + z + (z * z) / 2 + (z * z * z) / 6 + (z * z * z * z) / 24 };
  const clock = useClock({ period: 9, rest: 7.4 });
  const tcur = clamp(clock.t / 7, 0, 1) * T, m = Math.min(N, Math.floor(tcur / h + 1e-9));
  const P = plot({ x0: 0, x1: T, y0: -1.6, y1: 1.6, pad: [14, 12, 24, 30] });
  const series = (q) => Array.from({ length: m + 1 }, (_, i) => [i * h, clamp(q ** i, -1.6, 1.6)]);
  const L = [["ex", C.red, "명시적 오일러"], ["im", C.green, "암시적 오일러"], ["rk", C.violet, "RK4"]];
  return (
    <Frame clock={clock} title="안정성 — 걸음이 크면 터진다"
      read={<>y′ = −10y, y(0) = 1 (참값 e 의 −10t 제곱, 파랑) 을 걸음 h = {fmt(h, 2)}(hλ = {fmt(h * lam, 2)})로 푼다 · 한 걸음마다 곱해지는 배율: 명시적 오일러 1 − hλ = {fmt(fac.ex, 3)}, 암시적 오일러 1 ÷ (1 + hλ) = {fmt(fac.im, 3)}, RK4 {fmt(fac.rk, 3)} · 배율의 절댓값이 1 을 넘으면 진동하며 폭발한다 — 명시적 오일러는 hλ > 2, RK4 는 hλ > 2.79 에서, 암시적 오일러는 어떤 h 에서도 안정하다(강성 문제에 암시적 방법을 쓰는 까닭)</>}
      controls={<Slider label="걸음 h" min={0.02} max={0.32} step={0.01} value={h} onChange={(v) => { setH(v); clock.reset(); }} show={(v) => fmt(v, 2)} />}>
      <Axes p={P} xl="t" yl="y" grid={false} xt={[0.5, 1, 1.5, 2]} yt={[-1, 1]} />
      <path d={P.path((t) => Math.exp(-lam * t), 0, T, 200)} fill="none" stroke={C.blue} strokeWidth="2.2" />
      {L.map(([k2, col, name], j) => {
        const pts = series(fac[k2]);
        return (
          <g key={k2}>
            <path d={P.poly(pts)} fill="none" stroke={col} strokeWidth="1.5" />
            {pts.map(([t, y], i) => <circle key={i} cx={P.X(t)} cy={P.Y(y)} r="2.4" fill={col} />)}
            <text x={P.r - 4} y={P.t + 12 + j * 13} textAnchor="end" fontSize="9.5" fontWeight="800" fill={col}>{name} {Math.abs(fac[k2]) > 1 ? "— 폭발" : ""}</text>
          </g>
        );
      })}
    </Frame>
  );
}
