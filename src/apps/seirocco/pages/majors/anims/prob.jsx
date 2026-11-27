// 확률 그림 — 큰수의 법칙(동전) · 베이즈(넓이 그림) · 이항분포 · 정규분포 넓이 · 중심극한정리 · 상관과 산점도 · 마르코프 연쇄 · 랜덤워크 · 포아송 · 몬티 홀
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, ease, rng, gauss, useClock } from "./kit.jsx";

export const phi = (z) => Math.exp(-z * z / 2) / Math.sqrt(2 * Math.PI);
/** 표준정규 누적 Φ(z) — 아브라모위츠-스티건 근사(오차 7.5e−8) */
export function Phi(z) {
  const t = 1 / (1 + 0.2316419 * Math.abs(z));
  const d = 0.3989423 * Math.exp(-z * z / 2);
  const q = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  return z >= 0 ? 1 - q : q;
}
export function comb(n, k) { let r = 1; for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i; return r; }

/* ── 큰수의 법칙: 던질수록 앞면 비율이 p 로 ── */
export function LLN({ p = {} }) {
  const [pr, setPr] = useState(p.p ?? 0.5);
  const clock = useClock({ period: 12 });
  const N = 2000;
  const runs = useMemo(() => [11, 23, 37].map((seed) => {
    const r = rng(seed); let h = 0; const out = [];
    for (let i = 1; i <= N; i++) { if (r() < pr) h++; out.push(h / i); }
    return out;
  }), [pr]);
  const n = Math.max(2, Math.floor(Math.pow(N, clamp(clock.t / 11, 0.05, 1))));
  const P = plot({ x0: 0, x1: Math.log10(N), y0: 0, y1: 1 });
  const lx = (i) => Math.log10(i + 1);
  return (
    <Frame clock={clock} title="큰수의 법칙"
      read={<>앞면 확률 p = <b>{fmt(pr, 2)}</b> · {n}번 던졌을 때 세 사람의 앞면 비율 {runs.map((r, i) => <b key={i}> {fmt(r[n - 1], 3)}</b>)} — 횟수가 늘면 모두 p 로 모인다(가로축은 로그 눈금 10 · 100 · 1000)</>}
      controls={<Slider label="p" min={0.1} max={0.9} step={0.05} value={pr} onChange={setPr} />}>
      <Axes p={P} xl="log n" yl="비율" xt={[1, 2, 3]} xfmt={(v) => String(Math.round(Math.pow(10, v)))} />
      <line x1={P.l} x2={P.r} y1={P.Y(pr)} y2={P.Y(pr)} stroke={C.green} strokeDasharray="5 4" />
      {runs.map((r, k) => <path key={k} d={P.poly(r.slice(0, n).map((v, i) => [lx(i), v]))} fill="none" stroke={[C.sp, C.red, C.blue][k]} strokeWidth="1.6" />)}
    </Frame>
  );
}

/* ── 베이즈: 병이 드문데 양성이면 정말 병일까? — 1 만 명을 넓이로(비율 그대로), 아래는 양성인 사람만 모은 막대 ── */
export function Bayes({ p = {} }) {
  const [prev, setPrev] = useState(p.prev ?? 0.01);
  const [sens, setSens] = useState(p.sens ?? 0.95);
  const [spec, setSpec] = useState(p.spec ?? 0.95);
  const clock = useClock({ period: 5 });
  const W = 330, H = 92, x0 = 15, y0 = 26, yb = 166, hb = 16;
  const wS = Math.max(2, W * prev);                                   // 환자 칸 — 넓이가 그대로 사람 수(부풀리지 않는다)
  const tp = prev * sens, fp = (1 - prev) * (1 - spec), post = tp / (tp + fp);
  const nS = Math.round(10000 * prev), nTP = Math.round(nS * sens), nFP = Math.round((10000 - nS) * (1 - spec));
  const pulse = 0.6 + 0.3 * Math.sin(clock.t * Math.PI * 0.8);
  // 아래 막대: 진짜 양성(붉음)이 먼저 모이고, 이어서 가짜 양성(주황)이 모인다
  const k = ease(clamp(((clock.t + 2.4) % 5) / 2.4, 0, 1));          // 첫 장면(t = 0 · 움직임 줄이기)은 다 모인 막대
  const wTP = W * post * clamp(k / 0.45, 0, 1), wFP = W * (1 - post) * clamp((k - 0.45) / 0.55, 0, 1);
  return (
    <Frame clock={clock} title="베이즈 정리" vb="0 0 360 214"
      read={<>유병률 {fmt(prev * 100, 1)}% · 민감도 {fmt(sens * 100, 0)}% · 특이도 {fmt(spec * 100, 1)}% → 1 만 명 가운데 양성 <b>{nTP + nFP}</b>명, 그중 진짜 병 <b>{nTP}</b>명 — P(병 | 양성) = <b>{fmt(post * 100, 1)}%</b></>}
      controls={<>
        <Slider label="유병률" min={0.001} max={0.3} step={0.001} value={prev} onChange={setPrev} show={(v) => fmt(v * 100, 1) + "%"} />
        <Slider label="민감도" min={0.5} max={1} step={0.01} value={sens} onChange={setSens} show={(v) => fmt(v * 100, 0) + "%"} />
        <Slider label="특이도" min={0.5} max={0.999} step={0.001} value={spec} onChange={setSpec} show={(v) => fmt(v * 100, 1) + "%"} />
      </>}>
      <Label x={x0} y={16} size={10} color={C.mut}>1 만 명 — 넓이가 곧 사람 수(색칠 = 양성 판정)</Label>
      <rect x={x0} y={y0} width={wS} height={H} fill={C.red} opacity="0.16" />
      <rect x={x0} y={y0} width={wS} height={H * sens} fill={C.red} opacity={pulse} />
      <rect x={x0 + wS} y={y0} width={W - wS} height={H} fill={C.blue} opacity="0.08" />
      <rect x={x0 + wS} y={y0} width={W - wS} height={Math.max(0.8, H * (1 - spec))} fill={C.gold} opacity={pulse} />
      <rect x={x0} y={y0} width={W} height={H} fill="none" stroke={C.bd} />
      <line x1={x0 + wS} x2={x0 + wS} y1={y0} y2={y0 + H} stroke={C.mut} strokeWidth="0.8" />
      <Label x={x0} y={y0 + H + 13} size={10} color={C.red}>병 있음 {nS}명</Label>
      <Label x={x0 + W} y={y0 + H + 13} size={10} color={C.blue} anchor="end">병 없음 {10000 - nS}명</Label>
      <Label x={x0} y={yb - 6} size={10} color={C.ink}>양성인 사람만 모으면 — {nTP + nFP}명</Label>
      <rect x={x0} y={yb} width={W} height={hb} rx="3" fill={C.in} stroke={C.bd} />
      <rect x={x0} y={yb} width={wTP} height={hb} fill={C.red} />
      <rect x={x0 + W * post} y={yb} width={wFP} height={hb} fill={C.gold} />
      <Label x={x0} y={yb + hb + 13} size={10} color={C.red} bold>진짜 양성 {nTP}명 ({fmt(post * 100, 1)}%)</Label>
      <Label x={x0 + W} y={yb + hb + 13} size={10} color={C.gold} anchor="end" bold>가짜 양성 {nFP}명</Label>
    </Frame>
  );
}

/* ── 이항분포 ── */
export function Binomial({ p = {} }) {
  const [n, setN] = useState(p.n ?? 20);
  const [pr, setPr] = useState(p.p ?? 0.3);
  const [nrm, setNrm] = useState(false);
  const clock = useClock({ period: 3 });
  const ks = Array.from({ length: n + 1 }, (_, k) => comb(n, k) * Math.pow(pr, k) * Math.pow(1 - pr, n - k));
  const mx = Math.max(...ks) * 1.15;
  const P = plot({ x0: -0.8, x1: n + 0.8, y0: 0, y1: mx });
  const mu = n * pr, sd = Math.sqrt(n * pr * (1 - pr));
  const bw = Math.max(1, ((P.r - P.l) / (n + 1.6)) * 0.8);
  const hi = Math.round(mu + Math.sin(clock.t * 2) * 0);
  return (
    <Frame clock={clock} title="이항분포"
      read={<>B(n = {n}, p = {fmt(pr, 2)}) · 평균 np = <b>{fmt(mu, 2)}</b> · 표준편차 √(np(1 − p)) = <b>{fmt(sd, 2)}</b>{nrm ? " · 곡선 = 같은 평균 · 분산의 정규분포(n 이 크면 잘 맞는다)" : ""}</>}
      controls={<>
        <Slider label="n" min={1} max={60} value={n} onChange={setN} />
        <Slider label="p" min={0.02} max={0.98} step={0.02} value={pr} onChange={setPr} />
        <Seg value={nrm} onChange={setNrm} options={[[false, "막대만"], [true, "정규 근사"]]} />
      </>}>
      <Axes p={P} xl="k" yl="P" yfmt={(v) => fmt(v, 2)} />
      {ks.map((v, k) => <rect key={k} x={P.X(k) - bw / 2} width={bw} y={P.Y(v)} height={P.Y(0) - P.Y(v)} fill={k === hi ? C.red : C.sp} opacity="0.75" />)}
      {nrm && <path d={P.path((x) => phi((x - mu) / sd) / sd, -0.8, n + 0.8)} fill="none" stroke={C.ink} strokeWidth="2" />}
    </Frame>
  );
}

/* ── 정규분포: μ · σ 와 넓이(확률) ── */
export function Normal({ p = {} }) {
  const [mu, setMu] = useState(p.mu ?? 0);
  const [sd, setSd] = useState(p.sd ?? 1);
  const [k, setK] = useState(1);
  const clock = useClock({ period: 6 });
  const P = plot({ x0: -5, x1: 5, y0: 0, y1: 0.85 });
  const f = (x) => phi((x - mu) / sd) / sd;
  const a = mu - k * sd, b = mu + k * sd;
  let area = `M${P.X(a)} ${P.Y(0)}`;
  for (let i = 0; i <= 80; i++) { const x = a + ((b - a) * i) / 80; area += `L${P.X(x).toFixed(1)} ${P.Y(Math.min(f(x), 0.85)).toFixed(1)}`; }
  area += `L${P.X(b)} ${P.Y(0)}Z`;
  const pr = Phi(k) - Phi(-k);
  const sweep = mu - 4 * sd + ((clock.t / 6) * 8 * sd);
  return (
    <Frame clock={clock} title="정규분포"
      read={<>N(μ = {fmt(mu, 1)}, σ = {fmt(sd, 2)}) · μ ± {k}σ 안의 확률 <b>{fmt(pr * 100, 2)}%</b> (68 · 95 · 99.7 규칙) · 아무 정규분포도 z = (x − μ)/σ 로 표준정규가 된다</>}
      controls={<>
        <Slider label="μ" min={-2} max={2} step={0.1} value={mu} onChange={setMu} />
        <Slider label="σ" min={0.5} max={2} step={0.05} value={sd} onChange={setSd} />
        <Seg value={k} onChange={setK} options={[[1, "±1σ"], [2, "±2σ"], [3, "±3σ"]]} />
      </>}>
      <Axes p={P} yl="밀도" />
      <path d={area} fill={C.sp} opacity="0.3" />
      <path d={P.path(f)} fill="none" stroke={C.sp} strokeWidth="2.4" />
      <line x1={P.X(mu)} x2={P.X(mu)} y1={P.Y(0)} y2={P.Y(f(mu))} stroke={C.ink} strokeDasharray="3 3" />
      <circle cx={P.X(clamp(sweep, -5, 5))} cy={P.Y(f(clamp(sweep, -5, 5)))} r="3.5" fill={C.red} />
    </Frame>
  );
}

/* ── 중심극한정리: 치우친 모집단이라도 표본평균은 종 모양으로 ── */
const POP = {
  exp: { draw: (r) => -Math.log(Math.max(1e-12, r())), mu: 1, sd: 1, name: "지수분포(오른쪽으로 긴 꼬리)" },
  uni: { draw: (r) => r(), mu: 0.5, sd: Math.sqrt(1 / 12), name: "균등분포 [0, 1]" },
  die: { draw: (r) => 1 + Math.floor(r() * 6), mu: 3.5, sd: Math.sqrt(35 / 12), name: "주사위 눈" },
  bern: { draw: (r) => (r() < 0.15 ? 1 : 0), mu: 0.15, sd: Math.sqrt(0.15 * 0.85), name: "베르누이(p = 0.15)" },
};
export function CLT({ p = {} }) {
  const [pop, setPop] = useState(p.pop || "exp");
  const [n, setN] = useState(p.n ?? 2);
  const Pp = POP[pop] || POP.exp;
  const clock = useClock({ period: 10 });
  const M = 1200;
  const means = useMemo(() => {
    const r = rng(7 + n * 13 + pop.length);
    return Array.from({ length: M }, () => { let s = 0; for (let i = 0; i < n; i++) s += Pp.draw(r); return s / n; });
  }, [n, pop, Pp]);
  const shown = Math.max(20, Math.floor((clock.t / 9) * M));
  const se = Pp.sd / Math.sqrt(n);
  const lo = Pp.mu - 4 * Pp.sd / Math.sqrt(Math.max(1, n * 0.6)), hi = Pp.mu + 4 * Pp.sd / Math.sqrt(Math.max(1, n * 0.6));
  const B = 36, w = (hi - lo) / B, cnt = new Array(B).fill(0);
  for (let i = 0; i < Math.min(shown, M); i++) { const b = Math.floor((means[i] - lo) / w); if (b >= 0 && b < B) cnt[b]++; }
  const dens = cnt.map((c) => c / (Math.min(shown, M) * w));
  const top = Math.max(...dens, phi(0) / se) * 1.1;
  const P = plot({ x0: lo, x1: hi, y0: 0, y1: top });
  return (
    <Frame clock={clock} title="중심극한정리"
      read={<>{Pp.name} 에서 {n}개씩 뽑아 평균 — 표본평균 {Math.min(shown, M)}개의 히스토그램 · 곡선 = N(μ, σ²/n), 표준오차 σ/√n = <b>{fmt(se, 3)}</b>. n 을 키우면 종 모양으로, 폭은 1/√n 으로</>}
      controls={<>
        <Seg value={pop} onChange={(v) => { setPop(v); clock.reset(); }} options={[["exp", "지수"], ["uni", "균등"], ["die", "주사위"], ["bern", "베르누이"]]} />
        <Slider label="n" min={1} max={50} value={n} onChange={(v) => { setN(v); clock.reset(); }} />
      </>}>
      <Axes p={P} xl="x̄" yl="" yfmt={() => ""} />
      {dens.map((d, i) => <rect key={i} x={P.X(lo + i * w) + 0.5} width={Math.max(0.5, P.X(lo + (i + 1) * w) - P.X(lo + i * w) - 1)} y={P.Y(d)} height={P.Y(0) - P.Y(d)} fill={C.sp} opacity="0.6" />)}
      <path d={P.path((x) => phi((x - Pp.mu) / se) / se)} fill="none" stroke={C.red} strokeWidth="2" />
    </Frame>
  );
}

/* ── 상관과 산점도 ── */
export function Scatter({ p = {} }) {
  const [rho, setRho] = useState(p.rho ?? 0.7);
  const clock = useClock({ period: 8 });
  const pts = useMemo(() => {
    const r = rng(42);
    return Array.from({ length: 140 }, () => { const z1 = gauss(r), z2 = gauss(r); return [z1, rho * z1 + Math.sqrt(1 - rho * rho) * z2]; });
  }, [rho]);
  const P = plot({ x0: -3.2, x1: 3.2, y0: -3.2, y1: 3.2, W: 360, H: 220, pad: [8, 70, 18, 70] });
  const mx = pts.reduce((s, q) => s + q[0], 0) / pts.length, my = pts.reduce((s, q) => s + q[1], 0) / pts.length;
  let sxy = 0, sxx = 0, syy = 0;
  for (const [x, y] of pts) { sxy += (x - mx) * (y - my); sxx += (x - mx) ** 2; syy += (y - my) ** 2; }
  const r = sxy / Math.sqrt(sxx * syy), b1 = sxy / sxx;
  const hi = Math.floor((clock.t / 8) * pts.length);
  return (
    <Frame clock={clock} title="상관계수"
      read={<>모집단 상관 ρ = <b>{fmt(rho, 2)}</b> · 표본 상관 r = <b>{fmt(r, 3)}</b> · 회귀직선 기울기 = r × (y 의 표준편차 ÷ x 의 표준편차) = <b>{fmt(b1, 3)}</b> · r 은 「직선에 얼마나 몰렸나」 — 기울기의 크기가 아니다</>}
      controls={<Slider label="ρ" min={-0.98} max={0.98} step={0.02} value={rho} onChange={setRho} />}>
      <rect x={P.l} y={P.t} width={P.r - P.l} height={P.b - P.t} fill={C.card} />
      {pts.map(([x, y], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r={i === hi ? 4.5 : 2.6} fill={i === hi ? C.red : C.sp} opacity="0.65" />)}
      <path d={P.path((x) => my + b1 * (x - mx))} fill="none" stroke={C.red} strokeWidth="2" />
    </Frame>
  );
}

/* ── 마르코프 연쇄: 날씨 셋 — 어디서 시작하든 같은 정상분포로 ── */
export function Markov({ p = {} }) {
  const clock = useClock({ period: 12 });
  const T = [[0.7, 0.2, 0.1], [0.3, 0.4, 0.3], [0.2, 0.3, 0.5]];       // 행 = 오늘, 열 = 내일
  const names = ["맑음", "흐림", "비"], col = [C.gold, C.mut, C.blue];
  const starts = [[1, 0, 0], [0, 0, 1]];
  const steps = Math.min(12, Math.floor(clock.t));
  const walk = (s) => { const out = [s]; for (let i = 0; i < 12; i++) { const v = out[i]; out.push([0, 1, 2].map((j) => v[0] * T[0][j] + v[1] * T[1][j] + v[2] * T[2][j])); } return out; };
  const A = walk(starts[0]), B = walk(starts[1]);
  const pos = [[70, 60], [140, 160], [210, 60]];
  return (
    <Frame clock={clock} title="마르코프 연쇄" vb="0 0 360 210"
      read={<>{steps}일 뒤 — 맑은 날 출발: [{A[steps].map((v) => fmt(v, 3)).join(", ")}] · 비 오는 날 출발: [{B[steps].map((v) => fmt(v, 3)).join(", ")}] → 둘 다 정상분포 π = πP 로 모인다</>}>
      {[0, 1, 2].map((i) => [0, 1, 2].map((j) => (i === j ? null : (
        <line key={i + "" + j} x1={pos[i][0]} y1={pos[i][1]} x2={pos[j][0]} y2={pos[j][1]} stroke={C.bd} strokeWidth={1 + 6 * T[i][j]} />
      ))))}
      {pos.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r={14 + 26 * A[steps][i]} fill={col[i]} opacity="0.75" />
          <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{names[i]}</text>
        </g>
      ))}
      <text x="246" y="34" fontSize="9.5" fill={C.mut}>칠한 막대 = 맑음 출발</text>
      <text x="246" y="46" fontSize="9.5" fill={C.mut}>점선 막대 = 비 출발</text>
      {[0, 1, 2].map((j) => (
        <g key={j}>
          <rect x={250 + j * 34} y={190 - A[steps][j] * 130} width="14" height={A[steps][j] * 130} fill={col[j]} opacity="0.8" />
          <rect x={265 + j * 34} y={190 - B[steps][j] * 130} width="14" height={B[steps][j] * 130} fill="none" stroke={col[j]} strokeWidth="1.6" strokeDasharray="2 2" />
        </g>
      ))}
    </Frame>
  );
}

/* ── 랜덤워크: 평균은 0 인데 퍼짐은 √n 으로 ── */
export function RandomWalk({ p = {} }) {
  const clock = useClock({ period: 10 });
  const N = 400, K = 14;
  const walks = useMemo(() => Array.from({ length: K }, (_, k) => {
    const r = rng(100 + k); let x = 0; const out = [0];
    for (let i = 0; i < N; i++) { x += r() < 0.5 ? 1 : -1; out.push(x); }
    return out;
  }), []);
  const n = Math.max(1, Math.floor((clock.t / 9.5) * N));
  const P = plot({ x0: 0, x1: N, y0: -60, y1: 60 });
  const rms = Math.sqrt(walks.reduce((s, w) => s + w[Math.min(n, N)] ** 2, 0) / K);
  return (
    <Frame clock={clock} title="랜덤워크"
      read={<>동전 앞이면 +1, 뒤면 −1 · {n}걸음 뒤 퍼짐(제곱평균) <b>{fmt(rms, 1)}</b> ≈ √n = <b>{fmt(Math.sqrt(n), 1)}</b> — 걸음 수를 4배로 늘려야 퍼짐이 2배(점선 ±2√n 안에 거의 다 있다)</>}>
      <Axes p={P} xl="n" yl="위치" />
      <path d={P.path((x) => 2 * Math.sqrt(x), 0, N)} fill="none" stroke={C.gold} strokeDasharray="4 3" />
      <path d={P.path((x) => -2 * Math.sqrt(x), 0, N)} fill="none" stroke={C.gold} strokeDasharray="4 3" />
      {walks.map((w, k) => <path key={k} d={P.poly(w.slice(0, n + 1).map((v, i) => [i, v]))} fill="none" stroke={k % 3 === 0 ? C.red : C.sp} strokeWidth="1.1" opacity="0.7" />)}
    </Frame>
  );
}

/* ── 포아송: 드문 사건이 띄엄띄엄 — 단위 시간당 개수의 분포 ── */
export function Poisson({ p = {} }) {
  const [lam, setLam] = useState(p.lam ?? 3);
  const clock = useClock({ period: 10 });
  const ev = useMemo(() => {
    const r = rng(9 + Math.round(lam * 10)); const out = []; let t = 0;
    while (t < 40) { t += -Math.log(Math.max(1e-12, r())) / lam; out.push(t); }
    return out;
  }, [lam]);
  const tNow = (clock.t / 10) * 40;
  const Q = plot({ x0: -0.6, x1: 12.6, y0: 0, y1: 0.45, W: 360, H: 150, pad: [8, 10, 18, 34] });
  const pk = (k) => { let f = 1; for (let i = 2; i <= k; i++) f *= i; return Math.exp(-lam) * Math.pow(lam, k) / f; };
  const counts = new Array(13).fill(0);
  for (let u = 0; u < Math.floor(tNow); u++) { const c = ev.filter((t) => t >= u && t < u + 1).length; if (c < 13) counts[c]++; }
  const tot = Math.max(1, Math.floor(tNow));
  return (
    <Frame clock={clock} title="포아송 분포" vb="0 0 360 210"
      read={<>단위 시간당 평균 λ = <b>{fmt(lam, 1)}</b> 번 · 위: 사건이 일어난 때 · 아래 막대: 칸마다 센 개수의 비율(초록) vs 이론 P(X = k) = e<sup>−λ</sup>λ<sup>k</sup> ÷ k! (색 테) · 평균 = 분산 = λ</>}
      controls={<Slider label="λ" min={0.5} max={8} step={0.5} value={lam} onChange={setLam} />}>
      <line x1="34" x2="350" y1="24" y2="24" stroke={C.bd} />
      {Array.from({ length: 41 }, (_, u) => <line key={u} x1={34 + u * 7.9} x2={34 + u * 7.9} y1="18" y2="30" stroke={C.bd} />)}
      {ev.filter((t) => t < tNow).map((t, i) => <circle key={i} cx={34 + t * 7.9} cy="24" r="3" fill={C.red} />)}
      <g transform="translate(0,52)">
        <Axes p={Q} xl="k" yl="" grid={false} yfmt={(v) => fmt(v, 1)} />
        {Array.from({ length: 13 }, (_, k) => (
          <g key={k}>
            <rect x={Q.X(k) - 8} width="16" y={Q.Y(counts[k] / tot)} height={Q.Y(0) - Q.Y(counts[k] / tot)} fill={C.green} opacity="0.55" />
            <rect x={Q.X(k) - 8} width="16" y={Q.Y(pk(k))} height={Q.Y(0) - Q.Y(pk(k))} fill="none" stroke={C.sp} strokeWidth="1.6" />
          </g>
        ))}
      </g>
    </Frame>
  );
}

/* ── 몬티 홀: 바꾸면 2/3 ── */
export function Monty({ p = {} }) {
  const clock = useClock({ period: 12 });
  const N = Math.min(600, Math.floor((clock.t / 11.5) * 600));
  const res = useMemo(() => {
    const r = rng(5); const out = [];
    let ws = 0, wk = 0;
    for (let i = 1; i <= 600; i++) { const car = Math.floor(r() * 3), pick = Math.floor(r() * 3); if (car === pick) wk++; else ws++; out.push([ws / i, wk / i]); }
    return out;
  }, []);
  const P = plot({ x0: 0, x1: 600, y0: 0, y1: 1 });
  const k = Math.max(1, N);
  return (
    <Frame clock={clock} title="몬티 홀 문제"
      read={<>{k}번 해 보니 — 바꾼 사람의 승률 <b>{fmt(res[k - 1][0], 3)}</b>, 그대로 둔 사람 <b>{fmt(res[k - 1][1], 3)}</b> · 처음 고른 문이 맞을 확률은 1/3 에서 바뀌지 않는다. 진행자가 염소 문을 「알고」 열어 주므로 나머지 2/3 가 남은 문 하나로 모인다</>}>
      <Axes p={P} xl="번" yl="승률" />
      <line x1={P.l} x2={P.r} y1={P.Y(2 / 3)} y2={P.Y(2 / 3)} stroke={C.green} strokeDasharray="5 4" />
      <line x1={P.l} x2={P.r} y1={P.Y(1 / 3)} y2={P.Y(1 / 3)} stroke={C.mut} strokeDasharray="5 4" />
      <path d={P.poly(res.slice(0, k).map((v, i) => [i + 1, v[0]]))} fill="none" stroke={C.red} strokeWidth="2" />
      <path d={P.poly(res.slice(0, k).map((v, i) => [i + 1, v[1]]))} fill="none" stroke={C.blue} strokeWidth="2" />
      <Label x={P.r - 4} y={P.Y(2 / 3) - 5} anchor="end" color={C.red} size={10}>바꾸기</Label>
      <Label x={P.r - 4} y={P.Y(1 / 3) - 5} anchor="end" color={C.blue} size={10}>그대로</Label>
    </Frame>
  );
}
