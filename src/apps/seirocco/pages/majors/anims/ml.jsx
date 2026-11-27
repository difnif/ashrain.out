// 머신러닝 그림 — 최적화기 비교 · 로지스틱 회귀 · 과적합(다항 차수 · 릿지) · ROC 곡선 · 결정나무 분할 · 커널로 들어 올리기 · k-평균 · 주성분 분석 · 작은 신경망(XOR · 원)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, rng, gauss, ease, useClock } from "./kit.jsx";
import { Phi } from "./prob.jsx";

const sig = (z) => 1 / (1 + Math.exp(-z));

/* ── 최적화기: 한쪽이 20 배 가파른 골짜기에서 경사하강 · 모멘텀 · Adam · SGD ── */
const OPT_STEPS = 60;
function optPath(kind, lr) {
  let x = -4.2, y = 1.6, vx = 0, vy = 0, mx = 0, my = 0, sx = 0, sy = 0;
  const r = rng(5), pts = [[x, y]];
  for (let t = 1; t <= OPT_STEPS; t++) {
    let gx = x, gy = 20 * y;
    if (kind === "sgd") { gx += 0.8 * gauss(r); gy += 2.5 * gauss(r); const e = (lr * 15) / (15 + t); x -= e * gx; y -= e * gy; }
    else if (kind === "gd") { x -= lr * gx; y -= lr * gy; }
    else if (kind === "mom") { vx = 0.5 * vx + gx; vy = 0.5 * vy + gy; x -= lr * vx; y -= lr * vy; }
    else {
      mx = 0.9 * mx + 0.1 * gx; my = 0.9 * my + 0.1 * gy;
      sx = 0.999 * sx + 0.001 * gx * gx; sy = 0.999 * sy + 0.001 * gy * gy;
      const a = lr * 2, bc1 = 1 - 0.9 ** t, bc2 = 1 - 0.999 ** t;
      x -= (a * mx) / bc1 / (Math.sqrt(sx / bc2) + 1e-8); y -= (a * my) / bc1 / (Math.sqrt(sy / bc2) + 1e-8);
    }
    if (!Number.isFinite(x) || Math.abs(x) > 40 || Math.abs(y) > 40) break;
    pts.push([x, y]);
  }
  return pts;
}
const lossQ = ([x, y]) => 0.5 * (x * x + 20 * y * y);
const OPTS = [["gd", "경사하강", C.blue], ["mom", "모멘텀", C.green], ["adam", "Adam", C.violet], ["sgd", "SGD", C.gold]];
export function Optim({ p = {} }) {
  const [kind, setKind] = useState(OPTS.some((o) => o[0] === p.opt) ? p.opt : "gd");
  const [lr, setLr] = useState(p.lr ?? 0.085);
  const paths = useMemo(() => Object.fromEntries(OPTS.map(([k]) => [k, optPath(k, lr)])), [lr]);
  const clock = useClock({ period: 10, rest: 9 });
  const path = paths[kind], k = Math.min(path.length - 1, Math.floor((clock.t / 8) * OPT_STEPS));
  const diverged = path.length < OPT_STEPS + 1;
  const P = plot({ x0: -5, x1: 5, y0: -2.2, y1: 2.2, pad: [10, 140, 12, 12] });
  const R = plot({ x0: 0, x1: OPT_STEPS, y0: -6, y1: 2, pad: [16, 8, 24, 254] });
  const lg = (q) => clamp(Math.log10(Math.max(1e-9, lossQ(q))), -6, 2);
  const col = OPTS.find((o) => o[0] === kind)[2];
  return (
    <Frame clock={clock} title="최적화기 비교"
      read={<>손실 L = ½(w₁² + 20w₂²) — 세로가 20 배 가파른 골짜기 · {kind === "gd" ? "경사하강: 가파른 쪽으로는 튀며(지그재그) 완만한 쪽으로는 느리다" : kind === "mom" ? "모멘텀(β = 0.5): 지난 걸음을 이어 가 지그재그는 서로 지워지고 골짜기 방향으로는 속도가 붙는다" : kind === "adam" ? "Adam: 좌표마다 기울기 크기로 나눠 보폭을 맞춘다 — 학습률에 덜 민감해 η > 0.1 에서도 발산하지 않는다" : "SGD: 자료 일부로 구한 기울기라 흔들리지만 평균적으로는 내려간다 — 학습률을 점점 줄여 흔들림을 가라앉힌다"} · {k} 걸음 뒤 L = <b>{fmt(lossQ(path[k]), 4)}</b>{diverged && kind !== "adam" ? " — 걸음이 너무 커서 발산(η > 2/20 = 0.1)" : ""} · 오른쪽 = 걸음마다 log₁₀ L</>}
      controls={<>
        <Seg value={kind} onChange={(v) => { setKind(v); clock.reset(); }} options={OPTS.map(([k2, n]) => [k2, n])} />
        <Slider label="학습률 η" min={0.01} max={0.12} step={0.005} value={lr} onChange={(v) => { setLr(v); clock.reset(); }} show={(v) => fmt(v, 3)} />
      </>}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.card} />
      {[0.5, 2, 4.5, 8, 12.5].map((c) => <ellipse key={c} cx={P.X(0)} cy={P.Y(0)} rx={P.X(Math.sqrt(2 * c)) - P.X(0)} ry={P.Y(0) - P.Y(Math.sqrt((2 * c) / 20))} fill="none" stroke={C.sp} strokeWidth="1" opacity="0.45" />)}
      <path d={P.poly(path.slice(0, k + 1).map(([x, y]) => [clamp(x, -5, 5), clamp(y, -2.2, 2.2)]))} fill="none" stroke={col} strokeWidth="1.8" />
      <circle cx={P.X(clamp(path[k][0], -5, 5))} cy={P.Y(clamp(path[k][1], -2.2, 2.2))} r="4.5" fill={col} stroke={C.card} />
      <circle cx={P.X(0)} cy={P.Y(0)} r="2.5" fill={C.ink} />
      <Axes p={R} xl="" yl="" grid={false} xt={[20, 40, 60]} yt={[-6, -4, -2, 0, 2]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 0)} />
      <text x={R.r} y={R.b + 18} textAnchor="end" fontSize="9" fill={C.mut}>걸음</text>
      {OPTS.map(([k2, , c2]) => {
        const pp = paths[k2], last = k2 === kind ? k : pp.length - 1;
        return <path key={k2} d={R.poly(pp.slice(0, last + 1).map((q, i) => [i, lg(q)]))} fill="none" stroke={c2} strokeWidth={k2 === kind ? 2.2 : 1} opacity={k2 === kind ? 1 : 0.35} />;
      })}
      <text x={R.l + 4} y={R.t + 2} fontSize="9" fill={C.mut}>log₁₀ L</text>
    </Frame>
  );
}

/* ── 로지스틱 회귀: 시그모이드 확률과 결정 경계가 학습으로 자리 잡는다 ── */
function blobs2(sd, seed, n = 24) {
  const r = rng(seed), out = [];
  for (let i = 0; i < n; i++) out.push([-1 + sd * gauss(r), -0.6 + sd * gauss(r), 0]);
  for (let i = 0; i < n; i++) out.push([1 + sd * gauss(r), 0.8 + sd * gauss(r), 1]);
  return out;
}
function trainLogReg(data, iters = 120, lr = 0.6) {
  let w1 = -0.8, w2 = 0.6, b = 0.5;
  const snaps = [];
  for (let it = 0; it <= iters; it++) {
    let g1 = 0, g2 = 0, gb = 0, loss = 0, acc = 0;
    for (const [x, y, t] of data) { const pp = sig(w1 * x + w2 * y + b); g1 += (pp - t) * x; g2 += (pp - t) * y; gb += pp - t; loss -= t ? Math.log(pp + 1e-12) : Math.log(1 - pp + 1e-12); acc += (pp > 0.5) === (t === 1) ? 1 : 0; }
    const n = data.length;
    snaps.push({ w1, w2, b, loss: loss / n, acc: acc / n });
    w1 -= (lr * g1) / n; w2 -= (lr * g2) / n; b -= (lr * gb) / n;
  }
  return snaps;
}
export function LogReg({ p = {} }) {
  const [d, setD] = useState(p.data === "overlap" ? "overlap" : "clear");
  const data = useMemo(() => blobs2(d === "clear" ? 0.5 : 1.0, 11), [d]);
  const S = useMemo(() => trainLogReg(data), [data]);
  const clock = useClock({ period: 10, rest: 9 });
  const k = Math.min(S.length - 1, Math.floor((clock.t / 8) * (S.length - 1)));
  const s = S[k];
  const P = plot({ x0: -3, x1: 3, y0: -2.6, y1: 2.6, pad: [8, 112, 12, 10] });
  const R = plot({ x0: 0, x1: S.length - 1, y0: 0, y1: Math.max(0.8, S[0].loss * 1.1), pad: [24, 8, 26, 270] });
  const cells = [];
  for (let i = 0; i < 24; i++) for (let j = 0; j < 18; j++) {
    const x = -3 + (i + 0.5) * 0.25, y = -2.6 + (j + 0.5) * (5.2 / 18), pp = sig(s.w1 * x + s.w2 * y + s.b);
    cells.push(<rect key={i + "-" + j} x={P.X(-3 + i * 0.25)} y={P.Y(-2.6 + (j + 1) * (5.2 / 18))} width={P.X(0.25) - P.X(0) + 0.4} height={P.Y(0) - P.Y(5.2 / 18) + 0.4} fill={pp > 0.5 ? C.red : C.blue} opacity={Math.abs(pp - 0.5) * 0.5} />);
  }
  const line = (z) => (Math.abs(s.w2) > 1e-6 ? P.path((x) => (z - s.b - s.w1 * x) / s.w2, -3, 3) : "M0 0");
  return (
    <Frame clock={clock} title="로지스틱 회귀"
      read={<>점수 z = w₁x + w₂y + b 를 시그모이드에 넣어 확률 p = σ(z) — 색이 진할수록 확신 · 검은 선 p = 0.5 (결정 경계, 직선), 점선 p = 0.1 · 0.9 · 교차엔트로피 손실을 경사하강으로 줄인다: {k} 번째 손실 <b>{fmt(s.loss, 3)}</b>, 정확도 <b>{fmt(s.acc * 100, 0)} %</b>{d === "overlap" ? " — 두 무리가 겹치면 어떤 직선도 모두를 맞히지 못하고, 확률이 0.5 근처인 넓은 띠가 남는다" : ""}</>}
      controls={<Seg value={d} onChange={(v) => { setD(v); clock.reset(); }} options={[["clear", "잘 나뉨"], ["overlap", "겹침"]]} />}>
      {cells}
      <path d={line(0)} fill="none" stroke={C.ink} strokeWidth="2" />
      <path d={line(Math.log(9))} fill="none" stroke={C.ink} strokeWidth="1" strokeDasharray="4 3" opacity="0.6" />
      <path d={line(-Math.log(9))} fill="none" stroke={C.ink} strokeWidth="1" strokeDasharray="4 3" opacity="0.6" />
      {data.map(([x, y, t], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r="3.6" fill={t ? C.red : C.blue} stroke={C.card} strokeWidth="1" />)}
      <Axes p={R} xl="반복" yl="" grid={false} xt={[60, 120]} yt={[0.5]} xfmt={(v) => fmt(v, 0)} />
      <path d={R.poly(S.slice(0, k + 1).map((q, i) => [i, q.loss]))} fill="none" stroke={C.sp} strokeWidth="2" />
      <text x={R.l} y={R.t - 8} fontSize="9.5" fontWeight="800" fill={C.ink}>손실 {fmt(s.loss, 3)}</text>
    </Frame>
  );
}

/* ── 과적합: 다항식 차수를 올리면 훈련 오차는 줄지만 시험 오차는 U 자 ── */
function solve(A, bv) {
  const n = bv.length, M = A.map((r, i) => [...r, bv[i]]);
  for (let c = 0; c < n; c++) {
    let pr = c; for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[pr][c])) pr = r;
    [M[c], M[pr]] = [M[pr], M[c]];
    const d = M[c][c] || 1e-12;
    for (let r = 0; r < n; r++) if (r !== c) { const f = M[r][c] / d; for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
  }
  return M.map((r, i) => r[n] / (M[i][i] || 1e-12));
}
const truth = (x) => Math.sin(2 * Math.PI * x);
function polyData() {
  const r = rng(21), tr = [], te = [];
  for (let i = 0; i < 12; i++) { const x = 0.03 + (0.94 * i) / 11; tr.push([x, truth(x) + 0.28 * gauss(r)]); }
  for (let i = 0; i < 12; i++) { const x = 0.07 + (0.86 * i) / 11; te.push([x, truth(x) + 0.28 * gauss(r)]); }
  return { tr, te };
}
function fitPoly(tr, d, lam) {
  const u = (x) => 2 * x - 1, n = d + 1;
  const A = Array.from({ length: n }, () => Array(n).fill(0)), bv = Array(n).fill(0);
  for (const [x, y] of tr) { const pw = Array.from({ length: n }, (_, k) => u(x) ** k); for (let i = 0; i < n; i++) { bv[i] += pw[i] * y; for (let j = 0; j < n; j++) A[i][j] += pw[i] * pw[j]; } }
  for (let i = 1; i < n; i++) A[i][i] += lam;
  const c = solve(A, bv);
  return (x) => c.reduce((s, ck, k) => s + ck * u(x) ** k, 0);
}
const mse = (f, pts) => pts.reduce((s, [x, y]) => s + (f(x) - y) ** 2, 0) / pts.length;
export function Overfit({ p = {} }) {
  const [lam, setLam] = useState([0, 0.001, 0.1].includes(p.lam) ? p.lam : 0);
  const D = useMemo(polyData, []);
  const fits = useMemo(() => Array.from({ length: 12 }, (_, d) => { const f = fitPoly(D.tr, d, lam); return { f, tr: mse(f, D.tr), te: mse(f, D.te) }; }), [D, lam]);
  const best = fits.reduce((b, q, i) => (q.te < fits[b].te ? i : b), 0);
  const per = 1.1;
  const clock = useClock({ period: 12 * per + 2, rest: best * per + 0.5 });
  const d = Math.min(11, Math.floor(clock.t / per));
  const F = fits[d];
  const P = plot({ x0: 0, x1: 1, y0: -2, y1: 2, pad: [10, 140, 22, 26] });
  const R = plot({ x0: 0, x1: 11, y0: -3, y1: 1.5, pad: [30, 8, 26, 254] });
  const lg = (v) => clamp(Math.log10(Math.max(1e-6, v)), -3, 1.5);
  return (
    <Frame clock={clock} title="과적합 — 다항식 차수"
      read={<>점 12 개(●)에 d 차 다항식을 최소제곱으로 맞추고, 따로 둔 시험 점(○)으로 잰다 · 지금 d = <b>{d}</b>: 훈련 오차 {fmt(F.tr, 3)}, 시험 오차 <b>{fmt(F.te, 3)}</b> · 차수를 올리면 훈련 오차는 계속 줄지만(11 차면 모든 점을 지나 0) 시험 오차는 U 자 — 가장 좋은 차수는 {best} · {lam ? `릿지 규제(λ = ${lam})가 계수를 눌러 높은 차수에서도 덜 출렁인다` : "규제가 없으면 높은 차수에서 곡선이 점 사이를 크게 출렁인다(과적합)"}</>}
      controls={<>
        <Slider label="차수 d" min={0} max={11} step={1} value={d} onChange={(v) => { clock.setT(v * per + 0.3); clock.setPlaying(false); }} />
        <Seg value={lam} onChange={setLam} options={[[0, "규제 없음"], [0.001, "약한 릿지"], [0.1, "강한 릿지"]]} />
      </>}>
      <Axes p={P} xl="x" yl="y" grid={false} xt={[0.5, 1]} yt={[-1, 1]} />
      <path d={P.path(truth, 0, 1)} fill="none" stroke={C.green} strokeWidth="1.3" strokeDasharray="4 3" />
      <path d={P.path(F.f, 0, 1, 240)} fill="none" stroke={C.red} strokeWidth="2.2" />
      {D.tr.map(([x, y], i) => <circle key={"a" + i} cx={P.X(x)} cy={P.Y(y)} r="3.6" fill={C.blue} />)}
      {D.te.map(([x, y], i) => <circle key={"b" + i} cx={P.X(x)} cy={P.Y(y)} r="3.4" fill={C.card} stroke={C.gold} strokeWidth="1.5" />)}
      <Axes p={R} xl="d" yl="" grid={false} xt={[0, 5, 10]} yt={[-3, -2, -1, 0, 1]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 0)} />
      <path d={R.poly(fits.map((q, i) => [i, lg(q.tr)]))} fill="none" stroke={C.blue} strokeWidth="1.8" />
      <path d={R.poly(fits.map((q, i) => [i, lg(q.te)]))} fill="none" stroke={C.gold} strokeWidth="1.8" />
      <line x1={R.X(d)} x2={R.X(d)} y1={R.t} y2={R.b} stroke={C.red} strokeWidth="1.2" />
      <text x={R.l - 18} y="14" fontSize="9" fill={C.mut}>log₁₀ 오차:</text>
      <text x={R.l + 34} y="14" fontSize="9.5" fontWeight="800" fill={C.blue}>훈련</text>
      <text x={R.l + 62} y="14" fontSize="9.5" fontWeight="800" fill={C.gold}>시험</text>
    </Frame>
  );
}

/* ── ROC: 임계값을 옮기면 재현율과 위양성률이 함께 움직인다 ── */
export function ROC({ p = {} }) {
  const [dp, setDp] = useState([1, 2, 3].includes(p.d) ? p.d : 2);
  const clock = useClock({ period: 10, rest: 2.5 });
  const lo = -2.4, hi = dp + 2.4;
  const th = lo + (hi - lo) * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10));
  const tpr = 1 - Phi(th - dp), fpr = 1 - Phi(th), auc = Phi(dp / Math.SQRT2);
  const N = 1000, prev = 0.1, TP = tpr * N * prev, FP = fpr * N * (1 - prev), prec = TP / Math.max(1e-9, TP + FP);
  const den = (x, m) => Math.exp(-0.5 * (x - m) ** 2) / Math.sqrt(2 * Math.PI);
  const P = plot({ x0: -3.4, x1: 6.4, y0: 0, y1: 0.46, pad: [12, 150, 24, 10] });
  const R = plot({ x0: 0, x1: 1, y0: 0, y1: 1, pad: [12, 10, 24, 236] });
  const area = (m, a, b) => P.poly([[a, 0], ...Array.from({ length: 61 }, (_, i) => { const x = a + ((b - a) * i) / 60; return [x, den(x, m)]; }), [b, 0]]) + "Z";
  return (
    <Frame clock={clock} title="ROC 곡선과 임계값"
      read={<>음성(파랑)과 양성(빨강)의 점수 분포 · 임계값(검은 선)보다 높으면 양성으로 판정 · 재현율 TPR = <b>{fmt(tpr * 100, 0)} %</b>, 위양성률 FPR = <b>{fmt(fpr * 100, 0)} %</b> · 양성이 10 % 인 1000 명이면 참양성 {fmt(TP, 0)} · 거짓양성 {fmt(FP, 0)} → 정밀도 {fmt(prec * 100, 0)} % · 임계값을 훑으면 ROC 곡선이 그려진다: AUC = <b>{fmt(auc, 3)}</b>(무작위 양성 하나가 무작위 음성 하나보다 높은 점수를 받을 확률)</>}
      controls={<Seg value={dp} onChange={(v) => { setDp(v); clock.reset(); }} options={[[1, "약한 모형"], [2, "보통"], [3, "강한 모형"]]} />}>
      <path d={area(0, th, 6.4)} fill={C.blue} opacity="0.25" />
      <path d={area(dp, th, 6.4)} fill={C.red} opacity="0.25" />
      <path d={P.path((x) => den(x, 0), -3.4, 6.4)} fill="none" stroke={C.blue} strokeWidth="2" />
      <path d={P.path((x) => den(x, dp), -3.4, 6.4)} fill="none" stroke={C.red} strokeWidth="2" />
      <line x1={P.l} x2={P.r} y1={P.b} y2={P.b} stroke={C.mut} />
      <line x1={P.X(th)} x2={P.X(th)} y1={P.t} y2={P.b} stroke={C.ink} strokeWidth="2" />
      <Label x={P.X(0)} y={P.t + 10} size={9.5} color={C.blue} anchor="middle" bg>음성</Label>
      <Label x={P.X(dp)} y={P.t + 24} size={9.5} color={C.red} anchor="middle" bg>양성</Label>
      <text x={P.X(th) + 3} y={P.b + 14} fontSize="9" fill={C.ink}>임계값</text>
      <rect x={R.l} y={R.t} width={R.r - R.l} height={R.b - R.t} fill={C.card} stroke={C.bd} />
      <line x1={R.X(0)} y1={R.Y(0)} x2={R.X(1)} y2={R.Y(1)} stroke={C.mut} strokeDasharray="3 3" />
      <path d={R.curve((t) => 1 - Phi(t), (t) => 1 - Phi(t - dp), 7, -4, 160) + `L${R.X(1)} ${R.Y(0)}L${R.X(0)} ${R.Y(0)}Z`} fill={C.sp} opacity="0.12" />
      <path d={R.curve((t) => 1 - Phi(t), (t) => 1 - Phi(t - dp), 7, -4, 160)} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={R.X(fpr)} cy={R.Y(tpr)} r="4.5" fill={C.ink} />
      <text x={R.l + 4} y={R.t + 11} fontSize="9" fill={C.mut}>TPR</text>
      <text x={R.r - 3} y={R.b + 14} textAnchor="end" fontSize="9" fill={C.mut}>FPR</text>
    </Frame>
  );
}

/* ── 결정나무: 지니 불순도를 가장 많이 줄이는 축 방향 분할을 하나씩 ── */
function treeData() {
  const r = rng(17), pts = [];
  for (let i = 0; i < 56; i++) {
    const x = r(), y = r();
    let t = (x > 0.5 && y > 0.3) || (x < 0.35 && y > 0.72) ? 1 : 0;
    if (i === 7 || i === 31) t = 1 - t;
    pts.push([x, y, t]);
  }
  return pts;
}
const gini = (pts) => { if (!pts.length) return 0; const q = pts.filter((s) => s[2]).length / pts.length; return 1 - q * q - (1 - q) * (1 - q); };
function buildTree(pts) {
  const nodes = [], queue = [{ pts, box: [0, 0, 1, 1], depth: 0 }];
  while (queue.length) {
    const nd = queue.shift(); nd.id = nodes.length; nodes.push(nd);
    const g = gini(nd.pts);
    if (nd.depth >= 3 || g === 0 || nd.pts.length < 6) continue;
    let best = null;
    for (const f of [0, 1]) {
      const vs = [...new Set(nd.pts.map((s) => s[f]))].sort((a, b) => a - b);
      for (let i = 0; i + 1 < vs.length; i++) {
        const t = (vs[i] + vs[i + 1]) / 2, L = nd.pts.filter((s) => s[f] < t), Rr = nd.pts.filter((s) => s[f] >= t);
        if (L.length < 2 || Rr.length < 2) continue;
        const w = (L.length * gini(L) + Rr.length * gini(Rr)) / nd.pts.length;
        if (!best || w < best.w - 1e-12) best = { f, t, w, L, R: Rr };
      }
    }
    if (!best || g - best.w < 0.02) continue;
    nd.split = { f: best.f, t: best.t, g, w: best.w };
    const [x0, y0, x1, y1] = nd.box;
    const bl = best.f === 0 ? [x0, y0, best.t, y1] : [x0, y0, x1, best.t], br = best.f === 0 ? [best.t, y0, x1, y1] : [x0, best.t, x1, y1];
    nd.kids = [{ pts: best.L, box: bl, depth: nd.depth + 1 }, { pts: best.R, box: br, depth: nd.depth + 1 }];
    queue.push(...nd.kids);
  }
  return nodes;
}
export function Tree2D() {
  const pts = useMemo(treeData, []);
  const nodes = useMemo(() => buildTree(pts), [pts]);
  const splits = nodes.filter((n) => n.split);
  const per = 1.3;
  const clock = useClock({ period: splits.length * per + 3, rest: splits.length * per + 1 });
  const s = Math.min(splits.length, Math.floor(clock.t / per) + 1);
  const done = new Set(splits.slice(0, s).map((n) => n.id));
  const leaves = [];
  const walk = (n) => { if (done.has(n.id)) n.kids.forEach(walk); else leaves.push(n); };
  walk(nodes[0]);
  const acc = leaves.reduce((a, l) => { const ones = l.pts.filter((q) => q[2]).length; return a + Math.max(ones, l.pts.length - ones); }, 0) / pts.length;
  const X = (v) => 14 + v * 196, Y = (v) => 206 - v * 192;
  const cur = splits[s - 1];
  return (
    <Frame clock={clock} title="결정나무 — 축을 따라 자르기"
      read={<>영역마다 x 나 y 를 한 번 잘라 지니 불순도(1 − Σ 비율²)가 가장 많이 줄어드는 곳을 고른다 — 탐욕적 분할 · 지금 {s} 번째 분할 {cur.split.f ? "y" : "x"} &lt; {fmt(cur.split.t, 2)}: 지니 {fmt(cur.split.g, 3)} → <b>{fmt(cur.split.w, 3)}</b> · 영역의 색 = 그 안의 다수 무리, 맞히는 비율 <b>{fmt(acc * 100, 0)} %</b> · 깊이를 끝없이 늘리면 잡음까지 외운다(과적합) — 그래서 깊이를 제한하거나 나무 여러 그루를 평균한다(랜덤 포레스트)</>}>
      {leaves.map((l) => {
        const ones = l.pts.filter((q) => q[2]).length, maj = ones * 2 >= l.pts.length, pur = l.pts.length ? Math.max(ones, l.pts.length - ones) / l.pts.length : 0.5;
        const [x0, y0, x1, y1] = l.box;
        return <rect key={l.id} x={X(x0)} y={Y(y1)} width={X(x1) - X(x0)} height={Y(y0) - Y(y1)} fill={maj ? C.red : C.blue} opacity={0.08 + 0.22 * (pur - 0.5) * 2} stroke={C.ink} strokeWidth="0.6" />;
      })}
      {splits.slice(0, s).map((n, i) => {
        const [x0, y0, x1, y1] = n.box, { f, t } = n.split, last = i === s - 1;
        return f === 0
          ? <line key={n.id} x1={X(t)} x2={X(t)} y1={Y(y0)} y2={Y(y1)} stroke={last ? C.ink : C.mut} strokeWidth={last ? 2.4 : 1.4} />
          : <line key={n.id} y1={Y(t)} y2={Y(t)} x1={X(x0)} x2={X(x1)} stroke={last ? C.ink : C.mut} strokeWidth={last ? 2.4 : 1.4} />;
      })}
      {pts.map(([x, y, t], i) => <circle key={i} cx={X(x)} cy={Y(y)} r="3.3" fill={t ? C.red : C.blue} stroke={C.card} strokeWidth="0.8" />)}
      <text x="220" y="22" fontSize="10" fontWeight="800" fill={C.ink}>분할 (지니 → 나눈 뒤)</text>
      {splits.map((n, i) => (
        <text key={n.id} x={220 + n.depth * 8} y={40 + i * 19} fontSize="9.5" fill={i < s ? (i === s - 1 ? C.ink : C.mut) : C.bd} fontWeight={i === s - 1 ? 800 : 500}>
          {i + 1}. {n.split.f ? "y" : "x"} &lt; {fmt(n.split.t, 2)} · {fmt(n.split.g, 2)} → {fmt(n.split.w, 2)}
        </text>
      ))}
    </Frame>
  );
}

/* ── 커널: 직선으로 못 가르는 점들을 들어 올리면 갈린다 ── */
const KIN = [-0.95, -0.62, -0.3, 0.02, 0.33, 0.66, 0.92], KOUT = [-2.25, -1.92, -1.62, -1.36, 1.4, 1.72, 2.02, 2.3];
const KF = { sq: { f: (x) => x * x, name: "φ(x) = (x, x²)", ymax: 5.6 }, rbf: { f: (x) => 3 * Math.exp(-x * x), name: "φ(x) = (x, 3 · exp(−x²))", ymax: 3.4 } };
export function Kernel({ p = {} }) {
  const [kf, setKf] = useState(KF[p.k] ? p.k : "sq");
  const K = KF[kf];
  const clock = useClock({ period: 11, rest: 9 });
  const u = ease(clamp((clock.t - 0.8) / 2.6, 0, 1));
  const fin = KIN.map(K.f), fout = KOUT.map(K.f);
  const innerLow = Math.max(...fin) < Math.min(...fout);
  const a = innerLow ? Math.max(...fin) : Math.max(...fout), b = innerLow ? Math.min(...fout) : Math.min(...fin);
  const c = (a + b) / 2, half = (b - a) / 2;
  const xb = kf === "sq" ? Math.sqrt(c) : Math.sqrt(-Math.log(c / 3));
  const showSep = clock.t > 4, showBack = clock.t > 6.2;
  const P = plot({ x0: -2.7, x1: 2.7, y0: -0.7, y1: K.ymax, pad: [10, 10, 22, 26] });
  return (
    <Frame clock={clock} title="커널 — 들어 올려 가르기"
      read={<>한 줄 위의 파란 점(가운데)과 빨간 점(양쪽)은 점 하나(임계값)로 가를 수 없다 · 특징 {K.name} 으로 들어 올리면 수평선 하나로 갈린다 — 두 무리 사이 여백(띠)을 가장 넓게 하는 선이 서포트 벡터 머신의 해 · 다시 내려 보면 경계는 |x| = <b>{fmt(xb, 2)}</b> 인 두 점 — 원래 공간에서는 휘어진(여기서는 두 조각) 경계 · 커널 트릭: φ 를 직접 계산하지 않고 내적 φ(x) · φ(y) 만으로 같은 일을 한다</>}
      controls={<Seg value={kf} onChange={(v) => { setKf(v); clock.reset(); }} options={[["sq", "x² 로"], ["rbf", "가우스 봉우리로"]]} />}>
      <Axes p={P} xl="x" yl={kf === "sq" ? "x²" : "φ₂"} grid={false} xt={[-2, -1, 1, 2]} yt={kf === "sq" ? [1, 2, 3, 4, 5] : [1, 2, 3]} />
      <path d={P.path(K.f, -2.7, 2.7)} fill="none" stroke={C.mut} strokeWidth="1" strokeDasharray="3 3" opacity={u} />
      {showSep && <>
        <rect x={P.l} y={P.Y(c + half)} width={P.r - P.l} height={P.Y(c - half) - P.Y(c + half)} fill={C.green} opacity="0.12" />
        <line x1={P.l} x2={P.r} y1={P.Y(c)} y2={P.Y(c)} stroke={C.green} strokeWidth="2.2" />
      </>}
      {showBack && <>
        <rect x={P.X(-xb)} y={P.Y(0) - 5} width={P.X(xb) - P.X(-xb)} height="10" fill={C.blue} opacity="0.18" />
        {[-xb, xb].map((x) => <line key={x} x1={P.X(x)} x2={P.X(x)} y1={P.Y(c)} y2={P.Y(0) + 8} stroke={C.green} strokeWidth="1.4" strokeDasharray="4 3" />)}
      </>}
      {KIN.map((x, i) => <circle key={"i" + i} cx={P.X(x)} cy={P.Y(u * fin[i])} r="4.6" fill={C.blue} stroke={C.card} />)}
      {KOUT.map((x, i) => <circle key={"o" + i} cx={P.X(x)} cy={P.Y(u * fout[i])} r="4.6" fill={C.red} stroke={C.card} />)}
    </Frame>
  );
}

/* ── k-평균: 가까운 중심에 배정 ↔ 중심을 평균으로 옮기기 ── */
function kmData() {
  const r = rng(23), out = [];
  [[-1.6, 1.0], [1.5, 1.3], [0.2, -1.4]].forEach(([cx, cy]) => { for (let i = 0; i < 20; i++) out.push([cx + 0.55 * gauss(r), cy + 0.55 * gauss(r)]); });
  return out;
}
function kmFrames(X, K) {
  let cen = [[-0.2, 1.9], [0.4, 1.6], [2.2, -0.6], [-1.9, -1.2]].slice(0, K).map((q) => q.slice());
  const F = [{ cen: cen.map((q) => q.slice()), asg: null, J: null, step: "처음 중심(임의)" }];
  let asg = null;
  for (let it = 0; it < 8; it++) {
    const na = X.map(([x, y]) => { let b = 0; cen.forEach(([cx, cy], k) => { if ((x - cx) ** 2 + (y - cy) ** 2 < (x - cen[b][0]) ** 2 + (y - cen[b][1]) ** 2) b = k; }); return b; });
    const J = X.reduce((s, [x, y], i) => s + (x - cen[na[i]][0]) ** 2 + (y - cen[na[i]][1]) ** 2, 0);
    const same = asg && na.every((v, i) => v === asg[i]);
    asg = na;
    F.push({ cen: cen.map((q) => q.slice()), asg, J, step: `${it + 1} 회 배정` });
    if (same) break;
    cen = cen.map((c, k) => { const m = X.filter((_, i) => asg[i] === k); return m.length ? [m.reduce((s, q) => s + q[0], 0) / m.length, m.reduce((s, q) => s + q[1], 0) / m.length] : c; });
    const J2 = X.reduce((s, [x, y], i) => s + (x - cen[asg[i]][0]) ** 2 + (y - cen[asg[i]][1]) ** 2, 0);
    F.push({ cen: cen.map((q) => q.slice()), asg, J: J2, step: `${it + 1} 회 중심 이동` });
  }
  return F;
}
export function KMeans({ p = {} }) {
  const [K, setK] = useState([2, 3, 4].includes(p.k) ? p.k : 3);
  const X = useMemo(kmData, []);
  const F = useMemo(() => kmFrames(X, K), [X, K]);
  const per = 1.1;
  const clock = useClock({ period: F.length * per + 2.5, rest: F.length * per + 1 });
  const fi = Math.min(F.length - 1, Math.floor(clock.t / per));
  const f = F[fi];
  const pal = [C.blue, C.red, C.green, C.violet];
  const P = plot({ x0: -3.4, x1: 3.4, y0: -3, y1: 3, pad: [8, 10, 10, 10] });
  return (
    <Frame clock={clock} title="k-평균 군집화"
      read={<>k = {K} · ① 점마다 가장 가까운 중심(★)의 무리에 넣고 ② 중심을 그 무리의 평균으로 옮기기를 되풀이한다 · 지금: <b>{f.step}</b>{f.J != null ? <> · 무리 안 거리 제곱합 J = <b>{fmt(f.J, 1)}</b></> : ""} · 두 단계 모두 J 를 줄이므로 반드시 멈춘다 — 다만 처음 중심에 따라 다른 답(국소 최소)에 멈출 수 있다{K !== 3 ? " · 실제 무리는 3 개 — k 를 잘못 고르면 무리를 쪼개거나 합친다" : ""}</>}
      controls={<Seg value={K} onChange={(v) => { setK(v); clock.reset(); }} options={[[2, "k = 2"], [3, "k = 3"], [4, "k = 4"]]} />}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.card} opacity="0.5" />
      {X.map(([x, y], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r="3.6" fill={f.asg ? pal[f.asg[i]] : C.mut} opacity={f.asg ? 0.75 : 0.5} />)}
      {f.cen.map((c, k) => {
        const trail = F.slice(0, fi + 1).map((q) => q.cen[k]);
        return (
          <g key={k}>
            <path d={P.poly(trail)} fill="none" stroke={pal[k]} strokeWidth="1.4" strokeDasharray="3 2" />
            <text x={P.X(c[0])} y={P.Y(c[1]) + 6} textAnchor="middle" fontSize="19" fill={pal[k]} stroke={C.card} strokeWidth="1.2">★</text>
          </g>
        );
      })}
    </Frame>
  );
}

/* ── 주성분 분석: 사영한 분산이 가장 큰 방향 = 공분산 행렬의 첫 고유벡터 ── */
function pcaData() {
  const r = rng(31), a = (32 * Math.PI) / 180, out = [];
  for (let i = 0; i < 70; i++) { const u = 1.55 * gauss(r), v = 0.5 * gauss(r); out.push([u * Math.cos(a) - v * Math.sin(a), u * Math.sin(a) + v * Math.cos(a)]); }
  return out;
}
export function PCA() {
  const X = useMemo(pcaData, []);
  const st = useMemo(() => {
    const n = X.length, mx = X.reduce((s, q) => s + q[0], 0) / n, my = X.reduce((s, q) => s + q[1], 0) / n;
    let sxx = 0, syy = 0, sxy = 0;
    for (const [x, y] of X) { sxx += (x - mx) ** 2; syy += (y - my) ** 2; sxy += (x - mx) * (y - my); }
    sxx /= n - 1; syy /= n - 1; sxy /= n - 1;
    const tr = sxx + syy, dt = sxx * syy - sxy * sxy, l1 = tr / 2 + Math.sqrt((tr * tr) / 4 - dt), l2 = tr - l1;
    const th1 = 0.5 * Math.atan2(2 * sxy, sxx - syy);
    return { mx, my, sxx, syy, sxy, l1, l2, th1 };
  }, [X]);
  const clock = useClock({ period: 12, rest: 11 });
  const th1n = ((st.th1 % Math.PI) + Math.PI) % Math.PI;
  const th = clock.t < 9 ? (Math.PI * clock.t) / 9 : th1n;
  const cs = Math.cos(th), sn = Math.sin(th);
  const varTh = (t) => st.sxx * Math.cos(t) ** 2 + 2 * st.sxy * Math.sin(t) * Math.cos(t) + st.syy * Math.sin(t) ** 2;
  const P = plot({ x0: -4.2, x1: 4.2, y0: -3, y1: 3, pad: [8, 150, 10, 8] });
  const R = plot({ x0: 0, x1: 180, y0: 0, y1: st.l1 * 1.15, pad: [16, 10, 26, 232] });
  const deg = (th * 180) / Math.PI;
  return (
    <Frame clock={clock} title="주성분 분석"
      read={<>회색 직선(방향 {fmt(deg, 0)}°) 위로 점들을 수직으로 내린다(사영) · 사영한 점들의 분산 = {fmt(varTh(th), 2)} · 분산이 가장 큰 방향이 제1 주성분 — 공분산 행렬의 고유벡터({fmt((th1n * 180) / Math.PI, 0)}°)이고 그때의 분산이 가장 큰 고윳값 λ₁ = <b>{fmt(st.l1, 2)}</b>, 그와 직각인 방향이 λ₂ = {fmt(st.l2, 2)} · 한 축만 남겨도 분산의 <b>{fmt((st.l1 / (st.l1 + st.l2)) * 100, 0)} %</b> 를 설명한다(차원 축소)</>}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.card} opacity="0.5" />
      {X.map(([x, y], i) => {
        const t = (x - st.mx) * cs + (y - st.my) * sn, px = st.mx + t * cs, py = st.my + t * sn;
        return (
          <g key={i}>
            <line x1={P.X(x)} y1={P.Y(y)} x2={P.X(px)} y2={P.Y(py)} stroke={C.mut} strokeWidth="0.6" opacity="0.5" />
            <circle cx={P.X(x)} cy={P.Y(y)} r="2.8" fill={C.blue} opacity="0.65" />
            <circle cx={P.X(px)} cy={P.Y(py)} r="2.2" fill={C.red} />
          </g>
        );
      })}
      <line x1={P.X(st.mx - 5 * cs)} y1={P.Y(st.my - 5 * sn)} x2={P.X(st.mx + 5 * cs)} y2={P.Y(st.my + 5 * sn)} stroke={clock.t < 9 ? C.ink : C.red} strokeWidth="1.8" />
      <Axes p={R} xl="각" yl="" grid={false} xt={[90, 180]} yt={[]} xfmt={(v) => fmt(v, 0) + "°"} />
      <path d={R.path((d) => varTh((d * Math.PI) / 180), 0, 180)} fill="none" stroke={C.sp} strokeWidth="2" />
      <line x1={R.X((th1n * 180) / Math.PI)} x2={R.X((th1n * 180) / Math.PI)} y1={R.Y(st.l1)} y2={R.b} stroke={C.red} strokeDasharray="3 3" />
      <circle cx={R.X(deg)} cy={R.Y(varTh(th))} r="4.5" fill={C.ink} />
      <text x={R.l + 2} y={R.t - 4} fontSize="9" fill={C.mut}>사영한 분산</text>
    </Frame>
  );
}

/* ── 신경망: 은닉층이 공간을 휘어 직선으로 못 가르는 무리를 가른다 ── */
function nnData(kind) {
  const r = rng(41), out = [];
  if (kind === "xor") {
    [[1, 1, 0], [-1, -1, 0], [1, -1, 1], [-1, 1, 1]].forEach(([cx, cy, t]) => { for (let i = 0; i < 10; i++) out.push([cx + 0.3 * gauss(r), cy + 0.3 * gauss(r), t]); });
  } else {
    for (let i = 0; i < 20; i++) { const a = 2 * Math.PI * r(), rr = 0.55 * Math.sqrt(r()); out.push([rr * Math.cos(a), rr * Math.sin(a), 1]); }
    for (let i = 0; i < 24; i++) { const a = 2 * Math.PI * r(), rr = 1.05 + 0.45 * r(); out.push([rr * Math.cos(a), rr * Math.sin(a), 0]); }
  }
  return out;
}
const NH = 4;
function trainNN(data, epochs = 1500, lr = 0.5) {
  const r = rng(7);
  const W1 = Array.from({ length: NH }, () => [0.9 * gauss(r), 0.9 * gauss(r)]), b1 = Array.from({ length: NH }, () => 0.2 * gauss(r));
  const W2 = Array.from({ length: NH }, () => 0.9 * gauss(r));
  let b2 = 0;
  const snaps = [], n = data.length;
  for (let ep = 0; ep <= epochs; ep++) {
    const gW1 = W1.map(() => [0, 0]), gb1 = Array(NH).fill(0), gW2 = Array(NH).fill(0);
    let gb2 = 0, loss = 0, acc = 0;
    for (const [x, y, t] of data) {
      const h = W1.map(([a, c], j) => Math.tanh(a * x + c * y + b1[j]));
      const o = sig(h.reduce((s, v, j) => s + v * W2[j], b2));
      loss -= t ? Math.log(o + 1e-12) : Math.log(1 - o + 1e-12);
      acc += (o > 0.5) === (t === 1) ? 1 : 0;
      const d = o - t;
      gb2 += d;
      for (let j = 0; j < NH; j++) { gW2[j] += d * h[j]; const dh = d * W2[j] * (1 - h[j] * h[j]); gW1[j][0] += dh * x; gW1[j][1] += dh * y; gb1[j] += dh; }
    }
    if (ep % 25 === 0) snaps.push({ ep, W1: W1.map((q) => q.slice()), b1: b1.slice(), W2: W2.slice(), b2, loss: loss / n, acc: acc / n });
    for (let j = 0; j < NH; j++) { W2[j] -= (lr * gW2[j]) / n; W1[j][0] -= (lr * gW1[j][0]) / n; W1[j][1] -= (lr * gW1[j][1]) / n; b1[j] -= (lr * gb1[j]) / n; }
    b2 -= (lr * gb2) / n;
  }
  return snaps;
}
const nnOut = (s, x, y) => sig(s.W1.reduce((acc, [a, c], j) => acc + s.W2[j] * Math.tanh(a * x + c * y + s.b1[j]), s.b2));
export function NNet({ p = {} }) {
  const [ds, setDs] = useState(p.data === "circle" ? "circle" : "xor");
  const data = useMemo(() => nnData(ds), [ds]);
  const S = useMemo(() => trainNN(data), [data]);
  const clock = useClock({ period: 11, rest: 10 });
  const k = Math.min(S.length - 1, Math.floor((clock.t / 9) * (S.length - 1)));
  const s = S[k];
  const P = plot({ x0: -2, x1: 2, y0: -2, y1: 2, pad: [8, 150, 12, 8] });
  const cells = [];
  for (let i = 0; i < 26; i++) for (let j = 0; j < 26; j++) {
    const x = -2 + (i + 0.5) * (4 / 26), y = -2 + (j + 0.5) * (4 / 26), o = nnOut(s, x, y);
    cells.push(<rect key={i + "-" + j} x={P.X(-2 + i * (4 / 26))} y={P.Y(-2 + (j + 1) * (4 / 26))} width={P.X(4 / 26) - P.X(0) + 0.4} height={P.Y(0) - P.Y(4 / 26) + 0.4} fill={o > 0.5 ? C.red : C.blue} opacity={Math.abs(o - 0.5) * 0.55} />);
  }
  const IN = [[236, 70], [236, 130]], HID = Array.from({ length: NH }, (_, j) => [290, 40 + j * 40]), OUT = [342, 100];
  const wcol = (w) => (w >= 0 ? C.blue : C.red), wid = (w) => clamp(Math.abs(w) * 0.9, 0.4, 4.5);
  const L = plot({ x0: 0, x1: S.length - 1, y0: 0, y1: Math.max(0.75, S[0].loss * 1.05), pad: [182, 10, 12, 236] });
  return (
    <Frame clock={clock} title="신경망 — 은닉층이 공간을 휜다"
      read={<>입력 2 → 은닉 4(tanh) → 출력 1(시그모이드) · 교차엔트로피를 역전파로 구한 기울기로 줄인다 · {s.ep} 회 학습: 손실 <b>{fmt(s.loss, 3)}</b>, 정확도 <b>{fmt(s.acc * 100, 0)} %</b> · {ds === "xor" ? "XOR 은 어떤 직선으로도 못 가르지만 은닉 뉴런들이 만든 여러 경계를 합쳐 가른다" : "원 안과 밖은 직선으로 못 가르지만 은닉 뉴런 넷이 둘러싼 경계를 만든다"} · 오른쪽 선의 굵기 = 가중치 크기, 파랑 +, 빨강 −</>}
      controls={<Seg value={ds} onChange={(v) => { setDs(v); clock.reset(); }} options={[["xor", "XOR"], ["circle", "원"]]} />}>
      {cells}
      {data.map(([x, y, t], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r="3.3" fill={t ? C.red : C.blue} stroke={C.card} strokeWidth="0.8" />)}
      {HID.map(([hx, hy], j) => IN.map(([ix, iy], i) => <line key={j + "-" + i} x1={ix} y1={iy} x2={hx} y2={hy} stroke={wcol(s.W1[j][i])} strokeWidth={wid(s.W1[j][i])} opacity="0.75" />))}
      {HID.map(([hx, hy], j) => <line key={"o" + j} x1={hx} y1={hy} x2={OUT[0]} y2={OUT[1]} stroke={wcol(s.W2[j])} strokeWidth={wid(s.W2[j])} opacity="0.75" />)}
      {[...IN, ...HID, OUT].map(([x, y], i) => <circle key={"n" + i} cx={x} cy={y} r="8" fill={C.card} stroke={C.ink} strokeWidth="1.3" />)}
      <text x="236" y="74" textAnchor="middle" fontSize="8.5" fill={C.ink}>x</text>
      <text x="236" y="134" textAnchor="middle" fontSize="8.5" fill={C.ink}>y</text>
      <path d={L.poly(S.slice(0, k + 1).map((q, i) => [i, q.loss]))} fill="none" stroke={C.sp} strokeWidth="1.8" />
      <line x1={L.l} x2={L.r} y1={L.b} y2={L.b} stroke={C.mut} />
      <text x={L.l} y={L.t - 3} fontSize="9" fill={C.mut}>손실</text>
    </Frame>
  );
}
