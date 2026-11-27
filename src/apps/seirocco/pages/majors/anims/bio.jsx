// 생명과학 그림 — 레슬리 행렬(연령 구조) · 종간 경쟁 · 집단 면역(격자 전염) · 유전적 부동 · 미카엘리스–멘텐 · 활동 전위(피츠휴–나구모) · 계통수(UPGMA) · 튜링 무늬(그레이–스콧)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, rng, useClock } from "./kit.jsx";

/* ── 레슬리 행렬: 연령 구조와 안정 연령 분포 ── */
function leslie(f) {
  const L = [[0, 2 * f, 1.5 * f], [0.5, 0, 0], [0, 0.5, 0]];
  const mul = (x) => L.map((r) => r[0] * x[0] + r[1] * x[1] + r[2] * x[2]);
  let x = [0, 0, 10]; const out = [x];
  for (let t = 0; t < 24; t++) { x = mul(x); out.push(x); }
  let v = [1, 1, 1], lam = 1;
  for (let i = 0; i < 300; i++) { const w = mul(v), s = w[0] + w[1] + w[2]; lam = s / (v[0] + v[1] + v[2]); v = w.map((q) => q / s); }
  return { out, lam, stable: v };
}
const AGE = ["새끼", "어린 개체", "어른"], ACOL = [C.gold, C.green, C.blue];
export function Leslie({ p = {} }) {
  const [f, setF] = useState(clamp(p.f ?? 1, 0.5, 1.5));
  const R = useMemo(() => leslie(f), [f]);
  const clock = useClock({ period: 13, rest: 12 });
  const k = Math.min(24, Math.floor(clock.t / 0.5)), x = R.out[k], tot = x[0] + x[1] + x[2];
  const P = plot({ x0: 0, x1: 24, y0: -0.5, y1: 3.5, pad: [16, 136, 26, 34] });
  const lg = (q) => Math.log10(Math.max(1e-3, q[0] + q[1] + q[2]));
  const bx = 246, bw = 104;
  return (
    <Frame clock={clock} title="레슬리 행렬 — 나이 구조가 있는 개체군"
      read={<>세 나이 무리(새끼 · 어린 개체 · 어른) — 다음 해의 새끼 = 2f × 어린 개체 + 1.5f × 어른, 어린 개체 = 0.5 × 새끼, 어른 = 0.5 × 어린 개체 · {k} 년 뒤 전체 {fmt(tot, 1)} · 가장 큰 고윳값 λ = <b>{fmt(R.lam, 3)}</b> — 해마다 {R.lam >= 1 ? `${fmt((R.lam - 1) * 100, 1)} % 씩 는다` : `${fmt((1 - R.lam) * 100, 1)} % 씩 준다`} · 어른만으로 시작해도 나이 비율(막대)이 출렁이다 고유벡터(점선 칸)로 자리 잡는다 — 안정 연령 분포</>}
      controls={<Slider label="번식률 f" min={0.5} max={1.5} step={0.05} value={f} onChange={(v) => { setF(v); clock.reset(); }} show={(v) => fmt(v, 2)} />}>
      <Axes p={P} xl="년" yl="" grid={false} xt={[8, 16, 24]} yt={[0, 1, 2, 3]} yfmt={(v) => (v === 0 ? "1" : "10" + "⁰¹²³"[v])} />
      <text x={P.l + 4} y={P.t - 5} fontSize="9.5" fill={C.mut}>전체 개체 수(로그 눈금)</text>
      <path d={P.poly(R.out.map((q, i) => [i, lg(q)]))} fill="none" stroke={C.mut} strokeWidth="1" opacity="0.35" />
      <path d={P.poly(R.out.slice(0, k + 1).map((q, i) => [i, lg(q)]))} fill="none" stroke={C.red} strokeWidth="2.2" />
      <circle cx={P.X(k)} cy={P.Y(lg(x))} r="4" fill={C.red} />
      {x.map((q, j) => {
        const fr = q / tot, sf = R.stable[j], y = 40 + j * 52;
        return (
          <g key={j}>
            <text x={bx} y={y - 6} fontSize="9.5" fill={ACOL[j]} fontWeight="800">{AGE[j]} {fmt(fr * 100, 0)} %</text>
            <rect x={bx} y={y} width={bw} height="16" fill="none" stroke={C.bd} />
            <rect x={bx} y={y} width={bw * fr} height="16" fill={ACOL[j]} opacity="0.75" />
            <line x1={bx + bw * sf} x2={bx + bw * sf} y1={y - 3} y2={y + 19} stroke={C.ink} strokeWidth="1.4" strokeDasharray="3 2" />
          </g>
        );
      })}
    </Frame>
  );
}

/* ── 종간 경쟁: 로트카–볼테라 경쟁 모형의 상평면 ── */
const CMP = {
  coex: { a12: 0.6, a21: 0.5, name: "공존", note: "두 종 모두 자기 종끼리의 경쟁이 더 세서(α < 1) 안쪽 평형점에서 공존한다" },
  excl: { a12: 0.6, a21: 1.4, name: "경쟁 배제", note: "종 1 이 종 2 를 더 세게 누른다(α₂₁ > 1) — 종 2 는 사라지고 종 1 만 남는다(가우세의 원리)" },
  bist: { a12: 1.5, a21: 1.5, name: "먼저 자리 잡은 쪽이 이김", note: "서로를 세게 누르면 안쪽 평형점은 안장점 — 처음에 많은 쪽이 이긴다" },
};
const STARTS = [[0.05, 0.05], [0.95, 0.12], [0.12, 0.95], [0.9, 0.9], [0.35, 0.05], [0.05, 0.35], [0.55, 0.6]];
function compTraj(S) {
  const g = (x, y) => [x * (1 - x - S.a12 * y), y * (1 - y - S.a21 * x)], dt = 0.05;
  return STARTS.map(([x0, y0]) => { let x = x0, y = y0; const out = [[x, y]]; for (let i = 0; i < 500; i++) { const k1 = g(x, y), k2 = g(x + (dt / 2) * k1[0], y + (dt / 2) * k1[1]), k3 = g(x + (dt / 2) * k2[0], y + (dt / 2) * k2[1]), k4 = g(x + dt * k3[0], y + dt * k3[1]); x += (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); y += (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]); if (i % 4 === 3) out.push([x, y]); } return out; });
}
export function Compete({ p = {} }) {
  const [k, setK] = useState(CMP[p.case] ? p.case : "coex");
  const S = CMP[k];
  const T = useMemo(() => compTraj(S), [k]);
  const clock = useClock({ period: 12, rest: 11 });
  const n = Math.min(T[0].length - 1, Math.floor((clock.t / 10) * (T[0].length - 1)));
  const P = plot({ x0: 0, x1: 1.12, y0: 0, y1: 1.12, W: 360, H: 220, pad: [10, 150, 26, 34] });
  const D = 1 - S.a12 * S.a21, xs = (1 - S.a12) / D, ys = (1 - S.a21) / D, inner = xs > 0 && ys > 0;
  const lx = P.r + 12;
  return (
    <Frame clock={clock} title="종간 경쟁 — 로트카–볼테라 상평면"
      read={<>두 종의 개체 수 x, y(환경 수용력 1 로 맞춤) · dx/dt = x(1 − x − α₁₂y), dy/dt = y(1 − y − α₂₁x) · α₁₂ = {S.a12}, α₂₁ = {S.a21} · 파란 선은 x 가 더 자라지 않는 곳, 빨간 선은 y 가 더 자라지 않는 곳(널클라인) — 두 선이 만나는 곳이 평형점 · {S.note}{inner ? ` · 안쪽 평형점 (${fmt(xs, 2)}, ${fmt(ys, 2)})` : ""}</>}
      controls={<Seg value={k} onChange={(v) => { setK(v); clock.reset(); }} options={[["coex", "공존"], ["excl", "경쟁 배제"], ["bist", "쌍안정"]]} />}>
      <Axes p={P} xl="종 1 (x)" yl="종 2 (y)" grid={false} xt={[0.5, 1]} yt={[0.5, 1]} />
      <line x1={P.X(1)} y1={P.Y(0)} x2={P.X(Math.max(0, 1 - S.a12 * 1.12))} y2={P.Y(Math.min(1.12, 1 / S.a12))} stroke={C.blue} strokeWidth="1.6" strokeDasharray="5 3" />
      <line x1={P.X(0)} y1={P.Y(1)} x2={P.X(Math.min(1.12, 1 / S.a21))} y2={P.Y(Math.max(0, 1 - S.a21 * 1.12))} stroke={C.red} strokeWidth="1.6" strokeDasharray="5 3" />
      {T.map((tr, i) => <path key={i} d={P.poly(tr.slice(0, n + 1))} fill="none" stroke={C.ink} strokeWidth="1.2" opacity="0.7" />)}
      {T.map((tr, i) => <circle key={"s" + i} cx={P.X(tr[n][0])} cy={P.Y(tr[n][1])} r="3" fill={C.violet} />)}
      {inner && <circle cx={P.X(xs)} cy={P.Y(ys)} r="4" fill={k === "bist" ? "none" : C.green} stroke={k === "bist" ? C.gold : C.green} strokeWidth="2" />}
      <g fontSize="10" fill={C.ink}>
        <text x={lx} y={30} fontWeight="800">{S.name}</text>
        <line x1={lx} x2={lx + 14} y1={48} y2={48} stroke={C.blue} strokeWidth="1.6" strokeDasharray="5 3" /><text x={lx + 18} y={52}>dx/dt = 0</text>
        <line x1={lx} x2={lx + 14} y1={66} y2={66} stroke={C.red} strokeWidth="1.6" strokeDasharray="5 3" /><text x={lx + 18} y={70}>dy/dt = 0</text>
        <circle cx={lx + 6} cy={86} r="3" fill={C.violet} /><text x={lx + 18} y={90}>지금 상태</text>
        <text x={lx} y={118} fill={C.mut}>α₁₂ = {S.a12}</text>
        <text x={lx} y={134} fill={C.mut}>α₂₁ = {S.a21}</text>
      </g>
    </Frame>
  );
}

/* ── 집단 면역: 격자 위의 전염 ── */
const HW = 32, HH = 20;
function herdRun(v) {
  const r = rng(7), N = HW * HH, st = new Uint8Array(N), age = new Uint8Array(N);
  const order = Array.from({ length: N }, (_, i) => i);
  for (let i = N - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [order[i], order[j]] = [order[j], order[i]]; }
  const nv = Math.round(v * N); for (let j = 0; j < nv; j++) st[order[j]] = 3;
  const mid = [Math.floor(HH / 2) * HW + Math.floor(HW / 2), Math.floor(HH / 2) * HW + Math.floor(HW / 2) + 1, (Math.floor(HH / 2) + 1) * HW + Math.floor(HW / 2)];
  mid.forEach((i) => { st[i] = 1; });
  const frames = [st.slice()];
  for (let t = 0; t < 60; t++) {
    const nx = st.slice(); let any = false;
    for (let i = 0; i < N; i++) if (st[i] === 1) {
      any = true; const x = i % HW, y = (i / HW) | 0;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { if (!dx && !dy) continue; const X = x + dx, Y = y + dy; if (X < 0 || Y < 0 || X >= HW || Y >= HH) continue; const j = Y * HW + X; if (st[j] === 0 && nx[j] === 0 && r() < 0.3) nx[j] = 1; }
      age[i] += 1; if (age[i] >= 2) nx[i] = 2;
    }
    st.set(nx); frames.push(st.slice()); if (!any) break;
  }
  return frames;
}
const HCOL = ["#cfc6b2", C.red, C.mut, C.blue];
export function Herd({ p = {} }) {
  const [v, setV] = useState(clamp(p.v ?? 0.3, 0, 0.9));
  const F = useMemo(() => herdRun(v), [v]);
  const clock = useClock({ period: 14, rest: 13 });
  const k = Math.min(F.length - 1, Math.floor(clock.t / 0.35)), st = F[k];
  const cnt = [0, 0, 0, 0]; st.forEach((q) => { cnt[q] += 1; });
  const fin = F[F.length - 1], ever = fin.reduce((a, q) => a + (q === 1 || q === 2 ? 1 : 0), 0), unv = HW * HH - Math.round(v * HW * HH);
  const cw = 10.2, x0 = 17, y0 = 8;
  return (
    <Frame clock={clock} title="집단 면역 — 접종률에 문턱이 있다"
      read={<>사람 640 명이 격자에 살고(빨강 감염 · 회색 회복 · 파랑 접종), 감염자는 둘레 8 명에게 하루 30 % 확률로 옮긴 뒤 이틀 만에 회복한다(접종 없으면 감염자 한 명이 평균 약 4.8 명에게 옮길 기회) · 접종률 <b>{fmt(v * 100, 0)} %</b>(파랑) · 지금 감염 {cnt[1]} 명, 회복 {cnt[2]} 명 · 유행이 끝났을 때 걸린 사람은 접종 안 한 {unv} 명 가운데 <b>{fmt((100 * ever) / Math.max(1, unv), 0)} %</b> · 접종률이 문턱을 넘으면 감염이 퍼질 길이 끊겨 접종 못 한 사람까지 보호된다 — 섞여 사는 모형의 문턱은 1 − 1 ÷ R₀</>}
      controls={<Slider label="접종률" min={0} max={0.9} step={0.05} value={v} onChange={(q) => { setV(q); clock.reset(); }} show={(q) => fmt(q * 100, 0) + " %"} />}>
      {Array.from(st).map((q, i) => <rect key={i} x={x0 + (i % HW) * cw} y={y0 + ((i / HW) | 0) * cw} width={cw - 1.4} height={cw - 1.4} rx="1.5" fill={HCOL[q]} opacity={q === 2 ? 0.55 : 1} />)}
    </Frame>
  );
}

/* ── 유전적 부동: 라이트–피셔 모형 ── */
function driftRuns(N) {
  const r = rng(11 + N), G = 120, out = [];
  for (let k = 0; k < 8; k++) {
    let pp = 0.5; const tr = [pp];
    for (let g = 0; g < G; g++) { let c = 0; for (let i = 0; i < 2 * N; i++) if (r() < pp) c += 1; pp = c / (2 * N); tr.push(pp); }
    out.push(tr);
  }
  return out;
}
const DCOL = [C.red, C.blue, C.green, C.gold, C.violet, C.teal, "#b5517d", "#6b7f2a"];
export function Drift({ p = {} }) {
  const [N, setN] = useState([10, 50, 200].includes(p.n) ? p.n : 50);
  const R = useMemo(() => driftRuns(N), [N]);
  const clock = useClock({ period: 13, rest: 12 });
  const g = Math.min(120, Math.floor((clock.t / 12) * 120));
  const P = plot({ x0: 0, x1: 120, y0: 0, y1: 1, pad: [12, 12, 26, 34] });
  const fixed = R.filter((tr) => tr[g] === 0 || tr[g] === 1).length;
  const H = 0.5 * (1 - 1 / (2 * N)) ** g;
  return (
    <Frame clock={clock} title="유전적 부동 — 우연만으로 변하는 대립유전자 빈도"
      read={<>개체 수 N = {N} 인 집단 8 개, 대립유전자 A 의 빈도 0.5 에서 시작 · 세대마다 2N 개의 유전자를 무작위로 다시 뽑을 뿐(자연선택 없음)인데도 빈도가 떠돌다 0(사라짐) 또는 1(고정)에 닿는다 · {g} 세대 뒤 고정되거나 사라진 집단 {fixed} 개 · 이형접합도의 기대값은 매 세대 (1 − 1 ÷ 2N) 배 — 지금 {fmt(H, 3)} · 집단이 작을수록 부동이 세다(멸종 위기종의 유전 다양성 문제)</>}
      controls={<Seg value={N} onChange={(v) => { setN(v); clock.reset(); }} options={[[10, "N = 10"], [50, "N = 50"], [200, "N = 200"]]} />}>
      <Axes p={P} xl="세대" yl="A 의 빈도" grid={false} xt={[40, 80, 120]} yt={[0.5, 1]} />
      {R.map((tr, i) => <path key={i} d={P.poly(tr.slice(0, g + 1).map((q, j) => [j, q]))} fill="none" stroke={DCOL[i]} strokeWidth="1.5" opacity="0.85" />)}
      {R.map((tr, i) => <circle key={"e" + i} cx={P.X(g)} cy={P.Y(tr[g])} r="2.6" fill={DCOL[i]} />)}
    </Frame>
  );
}

/* ── 효소 반응: 미카엘리스–멘텐과 억제제 ── */
const MMI = { none: [1, 1], comp: [2, 1], non: [1, 0.5] };
export function MM({ p = {} }) {
  const [inh, setInh] = useState(MMI[p.inh] ? p.inh : "none");
  const [lb, setLb] = useState(p.mode === "lb");
  const clock = useClock({ period: 10, rest: 6 });
  const Vm = MMI[inh][1], Km = 2 * MMI[inh][0];
  const v = (S) => (Vm * S) / (Km + S), S = 0.2 + 19.8 * (0.5 - 0.5 * Math.cos((clock.t / 10) * 2 * Math.PI));
  const base = (s) => s / (2 + s);
  const name = { none: "억제제 없음", comp: "경쟁적 억제(Km 두 배)", non: "비경쟁적 억제(Vmax 절반)" }[inh];
  if (lb) {
    const P = plot({ x0: -0.8, x1: 2.2, y0: 0, y1: 7, pad: [12, 12, 26, 32] });
    const inv = (x) => (Km / Vm) * x + 1 / Vm;
    return (
      <Frame clock={clock} title="라인위버–버크 그림 — 거꾸로 그리면 직선"
        read={<>1 ÷ v = (Km ÷ Vmax)(1 ÷ [S]) + 1 ÷ Vmax — 가로 1 ÷ [S], 세로 1 ÷ v 로 그리면 직선 · {name}: 세로 절편 1 ÷ Vmax = {fmt(1 / Vm, 2)}, 가로 절편 −1 ÷ Km = {fmt(-1 / Km, 2)} · 경쟁적 억제는 세로 절편이 같고(최대 속도는 그대로) 비경쟁적 억제는 가로 절편이 같다(Km 은 그대로) — 회색은 억제제 없음</>}
        controls={<><Seg value={lb ? "lb" : "mm"} onChange={(q) => setLb(q === "lb")} options={[["mm", "속도 곡선"], ["lb", "라인위버–버크"]]} /><Seg value={inh} onChange={setInh} options={[["none", "없음"], ["comp", "경쟁적"], ["non", "비경쟁적"]]} /></>}>
        <Axes p={P} xl="1 ÷ [S]" yl="1 ÷ v" grid={false} xt={[1, 2]} yt={[2, 4, 6]} />
        <path d={P.path((x) => x + 1, -0.8, 2.2, 2)} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />
        <path d={P.path(inv, -0.8, 2.2, 2)} fill="none" stroke={C.red} strokeWidth="2.2" />
        {1 / S <= 2.2 && <circle cx={P.X(1 / S)} cy={P.Y(inv(1 / S))} r="4" fill={C.blue} />}
        <circle cx={P.X(-1 / Km)} cy={P.Y(0)} r="3.4" fill={C.gold} />
        <circle cx={P.X(0)} cy={P.Y(1 / Vm)} r="3.4" fill={C.gold} />
      </Frame>
    );
  }
  const P = plot({ x0: 0, x1: 20, y0: 0, y1: 1.15, pad: [12, 12, 26, 32] });
  return (
    <Frame clock={clock} title="효소 반응 — 미카엘리스–멘텐 식"
      read={<>v = Vmax[S] ÷ (Km + [S]) — 기질이 적으면 거의 비례, 많으면 효소가 꽉 차 Vmax 로 포화 · Km 은 속도가 Vmax 의 절반이 되는 기질 농도 · {name}: Vmax = {fmt(Vm, 2)}, Km = {fmt(Km, 1)} mM · 지금 [S] = {fmt(S, 1)} mM 에서 v = <b>{fmt(v(S), 3)}</b>(회색은 억제제 없음) · 경쟁적 억제제는 기질을 많이 넣으면 이길 수 있고, 비경쟁적 억제제는 아무리 넣어도 최대 속도가 준다</>}
      controls={<><Seg value={lb ? "lb" : "mm"} onChange={(q) => setLb(q === "lb")} options={[["mm", "속도 곡선"], ["lb", "라인위버–버크"]]} /><Seg value={inh} onChange={setInh} options={[["none", "없음"], ["comp", "경쟁적"], ["non", "비경쟁적"]]} /></>}>
      <Axes p={P} xl="[S] (mM)" yl="v" grid={false} xt={[5, 10, 15, 20]} yt={[0.5, 1]} />
      <line x1={P.l} x2={P.r} y1={P.Y(Vm)} y2={P.Y(Vm)} stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" />
      <line x1={P.X(Km)} x2={P.X(Km)} y1={P.Y(Vm / 2)} y2={P.b} stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" />
      <line x1={P.l} x2={P.X(Km)} y1={P.Y(Vm / 2)} y2={P.Y(Vm / 2)} stroke={C.gold} strokeWidth="1" strokeDasharray="4 3" />
      <path d={P.path(base, 0, 20, 160)} fill="none" stroke={C.mut} strokeWidth="1.2" opacity="0.6" />
      <path d={P.path(v, 0, 20, 160)} fill="none" stroke={C.red} strokeWidth="2.4" />
      <circle cx={P.X(S)} cy={P.Y(v(S))} r="4.4" fill={C.blue} />
      <Label x={P.X(Km) + 4} y={P.b - 6} size={9.5} color={C.gold}>Km</Label>
      <Label x={P.r - 4} y={P.Y(Vm) - 5} size={9.5} color={C.gold} anchor="end">Vmax</Label>
    </Frame>
  );
}

/* ── 신경 세포의 활동 전위: 피츠휴–나구모 모형 ── */
function fhn(Ifn, T) {
  const a = 0.7, b = 0.8, e = 0.08, dt = 0.05; let v = -1.1994, w = -0.6243; const out = [];
  const f = (t, v1, w1) => [v1 - (v1 * v1 * v1) / 3 - w1 + Ifn(t), e * (v1 + a - b * w1)];
  for (let i = 0; i * dt <= T; i++) {
    const t = i * dt; if (i % 8 === 0) out.push([t, v, w]);
    const k1 = f(t, v, w), k2 = f(t + dt / 2, v + (dt / 2) * k1[0], w + (dt / 2) * k1[1]), k3 = f(t + dt / 2, v + (dt / 2) * k2[0], w + (dt / 2) * k2[1]), k4 = f(t + dt, v + dt * k3[0], w + dt * k3[1]);
    v += (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); w += (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
  }
  return out;
}
const PULSES = [[15, 0.25], [55, 0.45], [95, 1.0], [108, 1.0], [140, 0.6]];
const FH_PULSE = fhn((t) => { for (const [s, A] of PULSES) if (t >= s && t < s + 2) return A; return 0; }, 170);
export function Neuron({ p = {} }) {
  const [m, setM] = useState(p.mode === "steady" ? "steady" : "pulse");
  const [I, setI] = useState(clamp(p.I ?? 0.5, 0, 1.6));
  const S = useMemo(() => (m === "pulse" ? FH_PULSE : fhn(() => I, 170)), [m, I]);
  const clock = useClock({ period: 13, rest: 12.5 });
  const n = Math.min(S.length - 1, Math.floor((clock.t / 12) * (S.length - 1)));
  const P = plot({ x0: 0, x1: 170, y0: -2.6, y1: 2.4, pad: [12, 12, 26, 34] });
  const cur = S[n];
  let spikes = 0; for (let i = 1; i <= n; i++) if (S[i - 1][1] < 1 && S[i][1] >= 1) spikes++;
  return (
    <Frame clock={clock} title="활동 전위 — 문턱과 ‘전부 아니면 전무’"
      read={m === "pulse" ? <>막전위 v(파랑)와 자극(아래 막대) · 피츠휴–나구모 모형 dv/dt = v − v³ ÷ 3 − w + I, dw/dt = 0.08(v + 0.7 − 0.8w) · 약한 자극(0.25)은 금방 가라앉고, 문턱을 넘는 자극(0.45)은 완전한 스파이크를 낸다 — 자극을 1.0 으로 키워도 스파이크 높이는 거의 같다(전부 아니면 전무) · 스파이크 직후의 같은 자극(108)은 무시된다(불응기) · 지금까지 스파이크 {spikes} 번</> : <>계속 흐르는 자극 전류 I = <b>{fmt(I, 2)}</b> · I 가 약 0.33 보다 작으면 조용하고, 넘으면 스파이크를 되풀이한다(정해진 리듬 — 극한 순환) · 지금까지 스파이크 {spikes} 번 · 전류가 세질수록 자주 쏘다가, 너무 세면(약 1.4 넘게) 오히려 멈춘다 — 신경은 자극의 세기를 스파이크의 ‘빈도’ 로 전한다</>}
      controls={<><Seg value={m} onChange={(q) => { setM(q); clock.reset(); }} options={[["pulse", "짧은 자극"], ["steady", "계속 자극"]]} />{m === "steady" && <Slider label="I" min={0} max={1.6} step={0.05} value={I} onChange={(q) => { setI(q); clock.reset(); }} show={(q) => fmt(q, 2)} />}</>}>
      <Axes p={P} xl="시간" yl="v" grid={false} xt={[50, 100, 150]} yt={[-2, -1, 1, 2]} />
      <line x1={P.l} x2={P.r} y1={P.Y(1)} y2={P.Y(1)} stroke={C.bd} strokeDasharray="3 3" />
      {m === "pulse" && PULSES.map(([s, A]) => <rect key={s} x={P.X(s)} y={P.Y(-2.6) - 22 * A} width={Math.max(2, P.X(s + 2) - P.X(s))} height={22 * A} fill={C.gold} opacity={s <= cur[0] ? 0.9 : 0.3} />)}
      {m === "steady" && <rect x={P.l} y={P.Y(-2.6) - 22 * Math.min(1, I)} width={P.X(cur[0]) - P.l} height={22 * Math.min(1, I)} fill={C.gold} opacity="0.5" />}
      <path d={P.poly(S.slice(0, n + 1).map((q) => [q[0], q[1]]))} fill="none" stroke={C.blue} strokeWidth="2" />
      <path d={P.poly(S.slice(0, n + 1).map((q) => [q[0], q[2]]))} fill="none" stroke={C.violet} strokeWidth="1.2" opacity="0.55" strokeDasharray="4 2" />
      <circle cx={P.X(cur[0])} cy={P.Y(cur[1])} r="3.8" fill={C.red} />
      <Label x={P.r - 4} y={P.t + 10} size={9.5} color={C.violet} anchor="end">회복 변수 w(점선)</Label>
    </Frame>
  );
}

/* ── 계통수: UPGMA 로 가까운 것부터 묶기 ── */
const SPC = ["사람", "침팬지", "고릴라", "오랑우탄", "긴팔원숭이"], ABB = ["사", "침", "고", "오", "긴"];
const DM = [[0, 1.2, 1.6, 3.1, 4.0], [1.2, 0, 1.6, 3.1, 4.0], [1.6, 1.6, 0, 3.1, 4.0], [3.1, 3.1, 3.1, 0, 4.0], [4.0, 4.0, 4.0, 4.0, 0]];
const UP = (() => {
  let cl = SPC.map((nm, i) => ({ id: i, name: nm, mem: [i], h: 0, y: i })); let D = DM.map((r) => r.slice()); const steps = [{ cl: cl.slice(), D: D.map((r) => r.slice()) }]; const joins = [];
  while (cl.length > 1) {
    let bi = 0, bj = 1; for (let i = 0; i < cl.length; i++) for (let j = i + 1; j < cl.length; j++) if (D[i][j] < D[bi][bj]) { bi = i; bj = j; }
    const A = cl[bi], B = cl[bj], h = D[bi][bj] / 2, nw = { id: 10 + joins.length, name: A.name + "+" + B.name, mem: [...A.mem, ...B.mem], h, y: (A.y + B.y) / 2, kids: [A, B] };
    joins.push(nw);
    const ND = [], keep = cl.map((_, i) => i).filter((i) => i !== bi && i !== bj);
    keep.forEach((i, a) => { ND.push(keep.map((j) => D[i][j])); ND[a].push((D[i][bi] * A.mem.length + D[i][bj] * B.mem.length) / (A.mem.length + B.mem.length)); });
    ND.push([...keep.map((i) => (D[i][bi] * A.mem.length + D[i][bj] * B.mem.length) / (A.mem.length + B.mem.length)), 0]);
    cl = [...keep.map((i) => cl[i]), nw]; D = ND; steps.push({ cl: cl.slice(), D: D.map((r) => r.slice()), join: nw, dist: 2 * h });
  }
  return { steps, joins };
})();
export function Phylo() {
  const clock = useClock({ period: 12, rest: 11 });
  const k = Math.min(UP.joins.length, Math.floor(clock.t / 2.2)), st = UP.steps[k];
  const X = (h) => 112 - h * 46, Y = (y) => 40 + y * 34;
  const shown = UP.joins.slice(0, k);
  const short = (c) => c.mem.slice().sort((a, b) => a - b).map((m) => ABB[m]).join("");
  const label = (c) => (c.mem.length === 1 ? SPC[c.mem[0]] : "(" + c.mem.slice().sort((a, b) => a - b).map((m) => SPC[m]).join(" · ") + ")");
  return (
    <Frame clock={clock} title="계통수 — 가까운 종부터 묶기(UPGMA)"
      read={<>DNA 염기 서열의 차이(%, 어림값)로 영장류 다섯 종의 계통수를 그린다 · 거리표(오른쪽)에서 가장 가까운 둘을 묶고, 새 묶음과 나머지의 거리는 평균으로 다시 계산하기를 되풀이한다(UPGMA) · {k === 0 ? "가장 가까운 둘은 사람과 침팬지(1.2 %)" : `${k} 번째: ${label(st.join.kids[0])} 와 ${label(st.join.kids[1])} 를 거리 ${fmt(st.dist, 1)} 에서 잇는다 — 갈라진 높이는 그 절반 ${fmt(st.dist / 2, 2)}`} · 분자 시계를 가정하면 가로축은 갈라진 뒤의 시간에 비례한다</>}>
      {SPC.map((nm, i) => <text key={nm} x={X(0) + 6} y={Y(i) + 4} fontSize="10.5" fill={C.ink}>{nm}</text>)}
      {SPC.map((nm, i) => <circle key={"d" + nm} cx={X(0)} cy={Y(i)} r="3" fill={C.blue} />)}
      {shown.map((j, i) => {
        const [A, B] = j.kids;
        return (
          <g key={i} stroke={i === k - 1 ? C.red : C.ink} strokeWidth={i === k - 1 ? 2.2 : 1.5} fill="none">
            <path d={`M ${X(A.h)} ${Y(A.y)} H ${X(j.h)} V ${Y(B.y)} H ${X(B.h)}`} />
          </g>
        );
      })}
      {shown.map((j, i) => <circle key={"n" + i} cx={X(j.h)} cy={Y(j.y)} r="2.6" fill={i === k - 1 ? C.red : C.ink} />)}
      <line x1={X(0)} x2={X(2)} y1="206" y2="206" stroke={C.mut} />
      {[0, 1, 2].map((h) => <text key={h} x={X(h)} y="216" textAnchor="middle" fontSize="9" fill={C.mut}>{h}</text>)}
      <text x={X(2) - 2} y="200" fontSize="9" fill={C.mut}>← 갈라진 높이</text>
      <g fontSize="9">
        <text x={300} y={30} textAnchor="middle" fill={C.mut}>거리표(%)</text>
        {st.cl.map((c, i) => <text key={"r" + i} x={236} y={66 + i * 22} textAnchor="end" fill={C.ink}>{short(c)}</text>)}
        {st.cl.map((c, i) => <text key={"c" + i} x={252 + i * 26} y={50} textAnchor="middle" fill={C.ink}>{short(c)}</text>)}
        {st.D.map((r, i) => r.map((d, j) => (j <= i ? null : <text key={i + "-" + j} x={252 + j * 26} y={66 + i * 22} textAnchor="middle" fill={st.join && j === st.cl.length - 1 ? C.red : C.mut}>{fmt(d, 1)}</text>)))}
      </g>
    </Frame>
  );
}

/* ── 튜링 무늬: 그레이–스콧 반응–확산 ── */
const GSCACHE = new Map();
function grayScott(F, k) {
  const key = F + "," + k; if (GSCACHE.has(key)) return GSCACHE.get(key);
  const N = 48, Du = 0.2, Dv = 0.1, r = rng(3); let u = new Float32Array(N * N).fill(1), v = new Float32Array(N * N);
  for (let s = 0; s < 6; s++) { const cx = Math.floor(r() * N), cy = Math.floor(r() * N); for (let dy = -3; dy <= 3; dy++) for (let dx = -3; dx <= 3; dx++) { const i = ((cy + dy + N) % N) * N + ((cx + dx + N) % N); u[i] = 0.5; v[i] = 0.25 + 0.1 * r(); } }
  let u2 = new Float32Array(N * N), v2 = new Float32Array(N * N);
  const snaps = [0, 150, 350, 650, 1000, 1500, 2100, 2800, 3500, 4200], out = [];
  for (let t = 0; t <= 4200; t++) {
    if (snaps.includes(t)) out.push({ t, v: v.slice() });
    for (let y = 0; y < N; y++) { const ym = ((y - 1 + N) % N) * N, yp = ((y + 1) % N) * N, y0 = y * N;
      for (let x = 0; x < N; x++) { const xm = (x - 1 + N) % N, xp = (x + 1) % N, i = y0 + x;
        const lu = u[ym + x] + u[yp + x] + u[y0 + xm] + u[y0 + xp] - 4 * u[i], lv = v[ym + x] + v[yp + x] + v[y0 + xm] + v[y0 + xp] - 4 * v[i], uvv = u[i] * v[i] * v[i];
        u2[i] = u[i] + Du * lu - uvv + F * (1 - u[i]); v2[i] = v[i] + Dv * lv + uvv - (F + k) * v[i]; } }
    [u, u2] = [u2, u]; [v, v2] = [v2, v];
  }
  const res = { N, out }; GSCACHE.set(key, res); return res;
}
const TP = { spots: [0.035, 0.065, "점무늬(표범 · 복어)"], stripes: [0.04, 0.06, "줄무늬 · 미로(얼룩말 · 물고기)"] };
const SHADE = ["#efe6d2", "#d9b98c", "#b98450", "#8a5a2e", "#4d3118"];
export function Turing({ p = {} }) {
  const [k, setK] = useState(TP[p.pat] ? p.pat : "spots");
  const G = grayScott(TP[k][0], TP[k][1]);
  const clock = useClock({ period: 12, rest: 11.5 });
  const i = Math.min(G.out.length - 1, Math.floor(clock.t / 1.1)), snap = G.out[i];
  const paths = useMemo(() => {
    const N = G.N, cs = 200 / N, d = ["", "", "", "", ""];
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const q = snap.v[y * N + x], b = q > 0.3 ? 4 : q > 0.22 ? 3 : q > 0.14 ? 2 : q > 0.06 ? 1 : 0; if (b) d[b] += `M${(8 + x * cs).toFixed(1)} ${(10 + y * cs).toFixed(1)}h${(cs + 0.15).toFixed(2)}v${(cs + 0.15).toFixed(2)}h${(-cs - 0.15).toFixed(2)}z`; }
    return d;
  }, [k, i]);
  return (
    <Frame clock={clock} title="튜링 무늬 — 반응과 확산이 만드는 무늬"
      read={<>두 물질이 서로 만들고 없애며(반응) 다른 빠르기로 퍼진다(확산 — 억제 물질이 두 배 빠름) · 그레이–스콧 모형, F = {TP[k][0]}, k = {TP[k][1]} · 몇 개의 얼룩에서 시작해 {snap.t} 걸음 뒤: {TP[k][2]} · 고른 상태가 스스로 무너져 정해진 간격의 무늬가 생긴다 — 1952 년 튜링이 동물 털 무늬와 손가락 형성의 원리로 내놓은 생각</>}
      controls={<Seg value={k} onChange={(q) => { setK(q); clock.reset(); }} options={[["spots", "점무늬"], ["stripes", "줄무늬"]]} />}>
      <rect x="8" y="10" width="200" height="200" fill={SHADE[0]} />
      {paths.map((d, b) => (b ? <path key={b} d={d || "M0 0"} fill={SHADE[b]} /> : null))}
      <rect x="8" y="10" width="200" height="200" fill="none" stroke={C.bd} />
      <g fontSize="10" fill={C.ink}>
        <text x="222" y="30" fontWeight="800">{TP[k][2].split("(")[0]}</text>
        <text x="222" y="50" fill={C.mut}>걸음 {snap.t}</text>
        <rect x="222" y="66" width="120" height="8" rx="4" fill="none" stroke={C.bd} />
        <rect x="222" y="66" width={(120 * snap.t) / 4200} height="8" rx="4" fill={C.gold} />
        <text x="222" y="98" fill={C.mut}>짙을수록 활성 물질</text>
        {SHADE.slice(1).map((c, j) => <rect key={j} x={222 + j * 22} y="106" width="18" height="10" fill={c} />)}
        <text x="222" y="140" fill={C.mut}>억제 물질이 더 빨리</text>
        <text x="222" y="155" fill={C.mut}>퍼져 이웃의 무늬를</text>
        <text x="222" y="170" fill={C.mut}>막는다(국소 활성 ·</text>
        <text x="222" y="185" fill={C.mut}>장거리 억제)</text>
      </g>
    </Frame>
  );
}
