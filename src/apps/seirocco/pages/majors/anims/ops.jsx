// 경영과학(OR) 그림 — 선형계획(등이익선 · 꼭짓점 걷기) · 최단 경로(데이크스트라) · 주공정(CPM 간트) · 경제적 주문량(EOQ) · 신문팔이(임계 비율) · 대기행렬(M/M/1 시뮬레이션 · 리틀의 법칙)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, ease, rng, useClock } from "./kit.jsx";
import { Phi, phi } from "./prob.jsx";

/* ── 선형계획: 등이익선을 밀어 마지막으로 닿는 꼭짓점 — 최적해는 늘 꼭짓점 ── */
const VERT = [[0, 0], [6, 0], [5, 3], [2, 6], [0, 7]];
export function LP({ p = {} }) {
  const [c1, setC1] = useState(p.c1 ?? 3);
  const [mode, setMode] = useState(p.mode === "walk" ? "walk" : "slide");
  const clock = useClock({ period: 10, rest: 8 });
  const c2 = 2, z = ([x, y]) => c1 * x + c2 * y;
  const zs = VERT.map(z), best = zs.indexOf(Math.max(...zs)), zmax = zs[best];
  const walk = useMemo(() => {
    const path = [0]; let cur = 0;
    for (let g = 0; g < 5; g++) { const nb = [(cur + 1) % 5, (cur + 4) % 5].filter((k) => zs[k] > zs[cur] + 1e-9); if (!nb.length) break; cur = nb.reduce((a, b) => (zs[b] > zs[a] ? b : a)); path.push(cur); }
    return path;
  }, [c1]); // eslint-disable-line react-hooks/exhaustive-deps
  const P = plot({ x0: 0, x1: 9, y0: 0, y1: 9, pad: [12, 128, 24, 28] });
  const level = mode === "slide" ? zmax * ease(clamp(clock.t / 6, 0, 1)) : 0;
  const ws = Math.min(walk.length - 1, Math.floor(clock.t / 1.4));
  const iso = (zz) => P.path((x) => (zz - c1 * x) / c2, 0, 9);
  return (
    <Frame clock={clock} title="선형계획"
      read={<>이익 z = {fmt(c1, 1)}x + 2y 를 가장 크게 · 제약: x + 2y ≤ 14 · 3x + y ≤ 18 · x + y ≤ 8 · x, y ≥ 0 (색 다각형 = 가능 영역) · {mode === "slide" ? <>등이익선(z 가 같은 점들)을 밀면 마지막으로 닿는 꼭짓점 ({VERT[best].join(", ")}) 에서 z = <b>{fmt(zmax, 1)}</b></> : <>꼭짓점 걷기(심플렉스): 이웃 꼭짓점 중 z 가 커지는 쪽으로만 — {walk.slice(0, ws + 1).map((k) => `(${VERT[k].join(",")})`).join(" → ")}{ws === walk.length - 1 ? " — 더 나아지는 이웃이 없으면 최적" : ""}</>} · 이익 비가 바뀌면 최적 꼭짓점이 옮겨 간다 — 최적해는 늘 꼭짓점</>}
      controls={<>
        <Slider label="x 의 이익 c₁" min={0.5} max={7} step={0.25} value={c1} onChange={(v) => { setC1(v); clock.reset(); }} />
        <Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["slide", "등이익선 밀기"], ["walk", "꼭짓점 걷기"]]} />
      </>}>
      <Axes p={P} xl="x" yl="y" />
      <path d={P.poly(VERT) + "Z"} fill={C.sp} opacity="0.16" stroke={C.sp} strokeWidth="1.6" />
      {[[(x) => (14 - x) / 2, "x + 2y = 14"], [(x) => 18 - 3 * x, "3x + y = 18"], [(x) => 8 - x, "x + y = 8"]].map(([f, n], k) => (
        <path key={n} d={P.path(f, 0, 9)} fill="none" stroke={[C.blue, C.gold, C.violet][k]} strokeWidth="1.2" strokeDasharray="4 3" opacity="0.8" />
      ))}
      {mode === "slide" && level > 0.01 && <path d={iso(level)} fill="none" stroke={C.red} strokeWidth="2" />}
      {mode === "walk" && <path d={P.poly(walk.slice(0, ws + 1).map((k) => VERT[k]))} fill="none" stroke={C.red} strokeWidth="2.6" />}
      {VERT.map((v, k) => <circle key={k} cx={P.X(v[0])} cy={P.Y(v[1])} r={k === best && (mode === "walk" ? ws === walk.length - 1 : level >= zmax - 1e-6) ? 6 : 3.5} fill={k === best ? C.red : C.ink} />)}
      <text x="244" y="30" fontSize="10" fontWeight="800" fill={C.ink}>꼭짓점 · z</text>
      {VERT.map((v, k) => <text key={k} x="244" y={50 + k * 20} fontSize="10" fill={k === best ? C.red : C.ink} fontWeight={k === best ? 800 : 500}>({v[0]}, {v[1]}) → {fmt(zs[k], 1)}</text>)}
    </Frame>
  );
}

/* ── 데이크스트라: 가장 가까운 미확정 마디를 하나씩 확정하며 이웃 거리를 고친다 ── */
const NODES = [["A", 34, 110], ["B", 112, 42], ["C", 112, 178], ["D", 192, 110], ["E", 262, 42], ["F", 262, 178], ["G", 332, 110]];
const EDGES = [[0, 1, 4], [0, 2, 2], [1, 2, 1], [1, 3, 5], [2, 3, 8], [2, 5, 10], [3, 4, 2], [3, 5, 6], [4, 6, 3], [5, 6, 2]];
function dijkstraSteps() {
  const n = NODES.length, dist = Array(n).fill(Infinity), prev = Array(n).fill(-1), done = Array(n).fill(false), steps = [];
  dist[0] = 0;
  for (let s = 0; s < n; s++) {
    let u = -1; for (let i = 0; i < n; i++) if (!done[i] && (u < 0 || dist[i] < dist[u])) u = i;
    done[u] = true;
    for (const [a, b, w] of EDGES) { const v = a === u ? b : b === u ? a : -1; if (v >= 0 && !done[v] && dist[u] + w < dist[v]) { dist[v] = dist[u] + w; prev[v] = u; } }
    steps.push({ u, dist: dist.slice(), prev: prev.slice(), done: done.slice() });
  }
  return steps;
}
const DSTEPS = dijkstraSteps();
export function Dijkstra() {
  const clock = useClock({ period: 11, rest: 10 });
  const k = Math.min(DSTEPS.length - 1, Math.floor(clock.t / 1.2));
  const S = DSTEPS[k], end = k === DSTEPS.length - 1;
  const onPath = new Set();
  if (end) { let v = 6; while (S.prev[v] >= 0) { onPath.add(v + "-" + S.prev[v]); onPath.add(S.prev[v] + "-" + v); v = S.prev[v]; } }
  const route = []; { let v = 6; route.push("G"); while (S.prev[v] >= 0) { v = S.prev[v]; route.unshift(NODES[v][0]); } }
  return (
    <Frame clock={clock} title="최단 경로 — 데이크스트라"
      read={<>{k + 1} 단계: 아직 확정 안 된 마디 중 가장 가까운 <b>{NODES[S.u][0]}</b>(거리 {S.dist[S.u]})를 확정(초록)하고, 그 이웃까지의 거리를 「지금 길 + 간선」이 더 짧으면 고친다 · 길이가 음수가 아니면 한 번 확정된 거리는 다시 바뀌지 않는다 · {end ? <>A → G 최단 거리 <b>{S.dist[6]}</b>: {route.join(" → ")}</> : "G 까지 계속"}</>}>
      {EDGES.map(([a, b, w]) => {
        const hot = onPath.has(a + "-" + b), tree = S.prev[b] === a || S.prev[a] === b;
        const [, x1, y1] = NODES[a], [, x2, y2] = NODES[b];
        return (
          <g key={a + "-" + b}>
            <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={hot ? C.red : tree ? C.sp : C.bd} strokeWidth={hot ? 4 : tree ? 2.4 : 1.6} />
            <text x={(x1 + x2) / 2 + 5} y={(y1 + y2) / 2 - 4} fontSize="10" fill={C.mut}>{w}</text>
          </g>
        );
      })}
      {NODES.map(([n, x, y], i) => (
        <g key={n}>
          <circle cx={x} cy={y} r="15" fill={S.done[i] ? "color-mix(in srgb, #3f7d3a 22%, var(--card))" : C.card} stroke={i === S.u ? C.green : S.done[i] ? C.green : C.ink} strokeWidth={i === S.u ? 3 : 1.5} />
          <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{n}</text>
          <text x={x} y={y + (y > 150 ? 30 : y < 70 ? -21 : 30)} textAnchor="middle" fontSize="10" fontWeight="800" fill={S.done[i] ? C.green : C.sp}>{Number.isFinite(S.dist[i]) ? S.dist[i] : "∞"}</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── 주공정(CPM): 가장 긴 길이 공기를 정한다 — 여유가 0 인 작업들 ── */
export function CPM({ p = {} }) {
  const [dD, setDD] = useState(p.d ?? 5);
  const clock = useClock({ period: 10, rest: 9 });
  const acts = [["A", 3, []], ["B", 4, []], ["C", 2, ["A"]], ["D", dD, ["A", "B"]], ["E", 3, ["C"]], ["F", 2, ["D", "E"]]];
  const ES = {}, EF = {};
  for (const [n, d, pre] of acts) { ES[n] = Math.max(0, ...pre.map((q) => EF[q])); EF[n] = ES[n] + d; }
  const T = Math.max(...Object.values(EF)), LF = {}, LS = {};
  for (const [n, d] of acts.slice().reverse()) { const succ = acts.filter((a) => a[2].includes(n)).map((a) => LS[a[0]]); LF[n] = succ.length ? Math.min(...succ) : T; LS[n] = LF[n] - d; }
  const slack = (n) => LS[n] - ES[n];
  const crit = acts.filter(([n]) => slack(n) === 0).map(([n]) => n);
  const now = T * clamp(clock.t / 8, 0, 1);
  const X = (d) => 56 + (d / 14) * 290;
  return (
    <Frame clock={clock} title="주공정과 간트 차트"
      read={<>앞 작업: C ← A · D ← A, B · E ← C · F ← D, E · 가장 이른 시작으로 늘어놓으면 공기 <b>{T}</b> 일 · 주공정(여유 0, 빨강) <b>{crit.join(" → ")}</b> — 이 작업이 하루 늦으면 전체가 하루 늦는다 · 여유: {acts.filter(([n]) => slack(n) > 0).map(([n]) => `${n} ${slack(n)} 일`).join(", ") || "없음"} (점선 = 늦어도 되는 만큼) · D 를 줄이면 다른 길이 주공정이 된다</>}
      controls={<Slider label="D 의 기간" min={2} max={8} step={1} value={dD} onChange={setDD} show={(v) => v + " 일"} />}>
      {Array.from({ length: 15 }, (_, d) => <g key={d}><line x1={X(d)} x2={X(d)} y1="18" y2="190" stroke={C.bd} strokeWidth="0.6" />{d % 2 === 0 && <text x={X(d)} y="204" textAnchor="middle" fontSize="9" fill={C.mut}>{d}</text>}</g>)}
      {acts.map(([n, d], i) => {
        const y = 22 + i * 28, cr = slack(n) === 0, done = clamp((now - ES[n]) / d, 0, 1);
        return (
          <g key={n}>
            <text x="44" y={y + 14} textAnchor="end" fontSize="11" fontWeight="800" fill={cr ? C.red : C.ink}>{n} ({d})</text>
            <rect x={X(ES[n])} y={y} width={X(EF[n]) - X(ES[n])} height="20" rx="3" fill="none" stroke={cr ? C.red : C.blue} strokeWidth="1.5" />
            <rect x={X(ES[n])} y={y} width={(X(EF[n]) - X(ES[n])) * done} height="20" rx="3" fill={cr ? C.red : C.blue} opacity="0.6" />
            {slack(n) > 0 && <line x1={X(EF[n])} x2={X(LF[n])} y1={y + 10} y2={y + 10} stroke={C.mut} strokeWidth="1.6" strokeDasharray="3 3" />}
          </g>
        );
      })}
      <line x1={X(now)} x2={X(now)} y1="16" y2="192" stroke={C.green} strokeWidth="1.5" />
      <text x={X(T)} y="14" textAnchor="middle" fontSize="9.5" fontWeight="800" fill={C.red}>공기 {T}</text>
    </Frame>
  );
}

/* ── 경제적 주문량(EOQ): 주문비와 보관비가 같아지는 곳 — 톱니 모양 재고 ── */
export function EOQ({ p = {} }) {
  const [Q, setQ] = useState(p.Q ?? 400);
  const clock = useClock({ period: 10 });
  const D = 1200, S = 50, H = 2;
  const Qs = Math.sqrt((2 * D * S) / H), cost = (q) => (D * S) / q + (H * q) / 2;
  const cyc = Q / D, t = clamp(clock.t / 9, 0, 1);
  const inv = (x) => Q * (1 - ((x % cyc) + cyc) % cyc / cyc);
  const L = plot({ x0: 0, x1: 1, y0: 0, y1: 640, pad: [14, 168, 26, 34] });
  const R = plot({ x0: 0, x1: 640, y0: 0, y1: 1400, pad: [14, 10, 26, 232] });
  const saw = []; for (let k = 0; k * cyc < 1 + 1e-9; k++) { const a = k * cyc, b = Math.min(1, (k + 1) * cyc); saw.push([a, Q], [b, Q * (1 - (b - a) / cyc)]); }
  return (
    <Frame clock={clock} title="경제적 주문량(EOQ)"
      read={<>한 해 수요 1200 개, 한 번 주문에 50 원, 1 개를 1 년 두면 2 원 · 한 번에 Q = <b>{Q}</b> 개씩: 한 해 {fmt(D / Q, 1)} 번 주문 · 주문비 DS/Q = {fmt((D * S) / Q, 0)} · 보관비 HQ/2 = {fmt((H * Q) / 2, 0)}(평균 재고 Q/2) · 합 <b>{fmt(cost(Q), 0)}</b> · 최적 Q* = √(2DS/H) = <b>{fmt(Qs, 0)}</b> 에서 주문비 = 보관비, 합 {fmt(cost(Qs), 0)} — 바닥이 평평해서 Q 를 20 % 틀려도 비용은 2 % 남짓 는다</>}
      controls={<Slider label="한 번 주문량 Q" min={60} max={600} step={10} value={Q} onChange={setQ} />}>
      <Axes p={L} xl="년" yl="재고" grid={false} xt={[0.5, 1]} yt={[200, 400, 600]} />
      <path d={L.poly(saw)} fill="none" stroke={C.sp} strokeWidth="2" />
      <line x1={L.l} x2={L.r} y1={L.Y(Q / 2)} y2={L.Y(Q / 2)} stroke={C.gold} strokeDasharray="4 3" />
      <circle cx={L.X(t)} cy={L.Y(inv(t))} r="4.5" fill={C.red} />
      <Label x={L.r - 2} y={L.Y(Q / 2) - 4} size={9} color={C.gold} anchor="end" bg>평균 Q/2</Label>
      <Axes p={R} xl="Q" yl="비용" grid={false} xt={[200, 400, 600]} yt={[500, 1000]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 0)} />
      <path d={R.path((q) => (D * S) / q, 45, 640)} fill="none" stroke={C.gold} strokeWidth="1.5" />
      <path d={R.path((q) => (H * q) / 2, 0, 640)} fill="none" stroke={C.blue} strokeWidth="1.5" />
      <path d={R.path(cost, 45, 640)} fill="none" stroke={C.red} strokeWidth="2.3" />
      <line x1={R.X(Qs)} x2={R.X(Qs)} y1={R.Y(cost(Qs))} y2={R.Y(0)} stroke={C.green} strokeDasharray="3 3" />
      <circle cx={R.X(Q)} cy={R.Y(cost(Q))} r="4.5" fill={C.red} />
      <text x={R.X(Qs)} y={R.Y(0) - 4} textAnchor="middle" fontSize="9" fill={C.green}>Q*</text>
    </Frame>
  );
}

/* ── 신문팔이 문제: 모자라는 손해와 남는 손해의 비 — 임계 비율만큼의 분위수를 주문 ── */
export function Newsvendor({ p = {} }) {
  const [pr, setPr] = useState(p.price ?? 10);
  const clock = useClock({ period: 10 });
  const mu = 100, sg = 20, c = 4, s = 1;
  const Cu = pr - c, Co = c - s, CR = Cu / (Cu + Co);
  const zstar = useMemo(() => { let lo = -6, hi = 6; for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; if (Phi(m) < CR) lo = m; else hi = m; } return (lo + hi) / 2; }, [CR]);
  const Qs = mu + sg * zstar;
  const E = (q) => { const z = (q - mu) / sg; return (pr - c) * q - (pr - s) * sg * (z * Phi(z) + phi(z)); };
  const Q = 50 + 100 * (0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10));
  const zq = (Q - mu) / sg;
  const L = plot({ x0: 30, x1: 170, y0: 0, y1: 0.024, pad: [14, 168, 26, 14] });
  const R = plot({ x0: 30, x1: 170, y0: Math.min(0, E(30)), y1: E(Qs) * 1.2, pad: [14, 10, 26, 226] });
  const dens = (x) => phi((x - mu) / sg) / sg;
  return (
    <Frame clock={clock} title="신문팔이 문제"
      read={<>수요 ~ 평균 100, 표준편차 20 · 한 부를 {c} 원에 사서 {pr} 원에 팔고, 남으면 {s} 원에 넘긴다 · Q = <b>{fmt(Q, 0)}</b> 부: 다 팔릴 확률 {fmt((1 - Phi(zq)) * 100, 0)} %, 기대이익 {fmt(E(Q), 0)} · 모자라면 한 부에 {Cu} 원, 남으면 {Co} 원 손해 → 최적은 P(수요 ≤ Q) = Cu/(Cu + Co) = <b>{fmt(CR, 2)}</b> 인 Q* = <b>{fmt(Qs, 0)}</b> — 남는 손해가 작을수록 넉넉히 주문</>}
      controls={<Slider label="판매가" min={5} max={20} step={0.5} value={pr} onChange={setPr} show={(v) => fmt(v, 1) + " 원"} />}>
      <Axes p={L} xl="수요" yl="" grid={false} xt={[60, 100, 140]} yt={[]} xfmt={(v) => fmt(v, 0)} />
      <path d={L.poly([[30, 0], ...Array.from({ length: 81 }, (_, i) => { const x = 30 + ((Math.min(Q, 170) - 30) * i) / 80; return [x, dens(x)]; }), [Math.min(Q, 170), 0]]) + "Z"} fill={C.sp} opacity="0.25" />
      <path d={L.path(dens, 30, 170)} fill="none" stroke={C.sp} strokeWidth="2" />
      <line x1={L.X(Q)} x2={L.X(Q)} y1={L.t} y2={L.b} stroke={C.red} strokeWidth="1.8" />
      <line x1={L.X(Qs)} x2={L.X(Qs)} y1={L.t} y2={L.b} stroke={C.green} strokeDasharray="3 3" />
      <Label x={L.X(Q) + 4} y={L.t + 12} size={9.5} color={C.red} bg>Q</Label>
      <Axes p={R} xl="Q" yl="기대이익" grid={false} xt={[60, 100, 140]} yt={[]} xfmt={(v) => fmt(v, 0)} />
      <path d={R.path(E, 30, 170)} fill="none" stroke={C.sp} strokeWidth="2" />
      <line x1={R.X(Qs)} x2={R.X(Qs)} y1={R.Y(E(Qs))} y2={R.b} stroke={C.green} strokeDasharray="3 3" />
      <circle cx={R.X(Q)} cy={R.Y(E(Q))} r="4.5" fill={C.red} />
      <text x={R.X(Qs)} y={R.Y(E(Qs)) - 6} textAnchor="middle" fontSize="9" fill={C.green}>Q*</text>
    </Frame>
  );
}

/* ── 대기행렬 M/M/1: 오는 비율이 처리 비율에 다가가면 줄이 폭발한다 — 리틀의 법칙 ── */
export function Queue({ p = {} }) {
  const [lam, setLam] = useState(p.rho ?? 0.8);
  const clock = useClock({ period: 14, rest: 13 });
  const mu = 1, Tmax = 60;
  const ev = useMemo(() => {
    const r = rng(9), cs = []; let t = 0, last = 0;
    while (t < Tmax) { t += -Math.log(1 - r()) / lam; const sv = -Math.log(1 - r()) / mu; const st = Math.max(t, last); last = st + sv; cs.push({ a: t, s: st, d: last }); }
    return cs;
  }, [lam]);
  const tau = Tmax * clamp(clock.t / 12, 0, 1);
  const nAt = (x) => ev.filter((c) => c.a <= x && x < c.d).length;
  const waiting = ev.filter((c) => c.a <= tau && tau < c.s), serving = ev.find((c) => c.s <= tau && tau < c.d);
  const series = useMemo(() => { const out = []; for (let x = 0; x <= Tmax + 1e-9; x += 0.25) out.push([x, nAt(x)]); return out; }, [ev]); // eslint-disable-line react-hooks/exhaustive-deps
  const shown = series.filter(([x]) => x <= tau);
  const avg = shown.length ? shown.reduce((s, [, n]) => s + n, 0) / shown.length : 0;
  const rho = lam / mu, Lth = rho / (1 - rho);
  const P = plot({ x0: 0, x1: Tmax, y0: 0, y1: Math.max(8, Lth * 2.2), pad: [104, 14, 24, 30] });
  return (
    <Frame clock={clock} title="대기행렬 — M/M/1"
      read={<>손님이 평균 1 분에 {fmt(lam, 2)} 명 오고(λ), 창구 하나가 평균 1 분에 1 명 처리(μ) · ρ = λ/μ = <b>{fmt(rho, 2)}</b>: 이론 평균 사람 수 L = ρ/(1 − ρ) = <b>{fmt(Lth, 2)}</b>, 머무는 시간 W = 1/(μ − λ) = {fmt(1 / (mu - lam), 1)} 분 · 지금까지 시뮬레이션 평균 {fmt(avg, 2)} · 리틀의 법칙 L = λW · ρ 가 1 에 다가가면 줄이 폭발적으로 길어진다(0.9 → 9, 0.95 → 19) — 창구를 늘 여유 있게 두는 까닭</>}
      controls={<Slider label="오는 비율 λ (처리 1)" min={0.3} max={0.95} step={0.05} value={lam} onChange={(v) => { setLam(v); clock.reset(); }} />}>
      <rect x="282" y="24" width="56" height="44" rx="6" fill={C.in} stroke={C.ink} strokeWidth="1.5" />
      <text x="310" y="20" textAnchor="middle" fontSize="9.5" fill={C.mut}>창구</text>
      {serving && <circle cx="310" cy="46" r="9" fill={C.sp} />}
      {waiting.slice(0, 18).map((c, i) => <circle key={c.a} cx={264 - i * 13} cy="46" r="5.5" fill={C.gold} />)}
      {waiting.length > 18 && <text x="24" y="50" fontSize="10" fill={C.red}>+{waiting.length - 18}</text>}
      <text x="24" y="84" fontSize="10" fill={C.ink}>줄 선 사람 {waiting.length} · 창구 {serving ? 1 : 0}</text>
      <Axes p={P} xl="분" yl="사람 수" grid={false} xt={[20, 40, 60]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 0)} />
      <line x1={P.l} x2={P.r} y1={P.Y(Lth)} y2={P.Y(Lth)} stroke={C.green} strokeDasharray="4 3" />
      <path d={P.poly(shown.flatMap(([x, n], i) => (i ? [[x, shown[i - 1][1]], [x, n]] : [[x, n]])).map(([x, n]) => [x, Math.min(n, P.y1)]))} fill="none" stroke={C.sp} strokeWidth="1.5" />
      <Label x={P.r - 2} y={P.Y(Lth) - 4} size={9} color={C.green} anchor="end" bg>이론 평균 L</Label>
    </Frame>
  );
}
