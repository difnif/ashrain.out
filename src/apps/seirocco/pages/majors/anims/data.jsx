// 데이터 공학 그림 — k-최근접 이웃 · A/B 시험(엿보기) · 해시 테이블(충돌 · 사슬) · 블룸 필터 · B-트리 · 조인 알고리즘 · 저수지 표집 · 페이지랭크
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, rng, gauss, useClock } from "./kit.jsx";
import { Phi } from "./prob.jsx";

/* ── k-최근접 이웃: 가까운 k 개의 다수결 — k 가 작으면 들쭉날쭉, 크면 무뎌진다 ── */
function knnData() {
  const r = rng(13), out = [];
  [[2.6, 7.2], [7.2, 7.4], [5, 2.6]].forEach(([cx, cy], c) => { for (let i = 0; i < 15; i++) out.push([clamp(cx + 1.35 * gauss(r), 0.2, 9.8), clamp(cy + 1.35 * gauss(r), 0.2, 9.8), c]); });
  return out;
}
const KC = [C.blue, C.red, C.green];
export function KNN({ p = {} }) {
  const [k, setK] = useState([1, 3, 7, 15].includes(p.k) ? p.k : 3);
  const [met, setMet] = useState(p.metric === "l1" ? "l1" : "l2");
  const X = useMemo(knnData, []);
  const dist = (ax, ay, bx, by) => (met === "l1" ? Math.abs(ax - bx) + Math.abs(ay - by) : Math.hypot(ax - bx, ay - by));
  const vote = (qx, qy) => {
    const nb = X.map((q, i) => [dist(qx, qy, q[0], q[1]), i]).sort((a, b) => a[0] - b[0]).slice(0, k);
    const cnt = [0, 0, 0]; nb.forEach(([, i]) => cnt[X[i][2]]++);
    const mx = Math.max(...cnt), tied = [0, 1, 2].filter((c) => cnt[c] === mx);
    const near = nb.find(([, i]) => tied.includes(X[i][2]));
    const win = tied.length === 1 ? tied[0] : near ? X[near[1]][2] : tied[0];
    return { nb, cnt, win };
  };
  const grid = useMemo(() => {
    const g = [];
    for (let i = 0; i < 30; i++) for (let j = 0; j < 27; j++) g.push([i, j, vote((i + 0.5) / 3, (j + 0.5) / 2.7).win]);
    return g;
  }, [k, met]); // eslint-disable-line react-hooks/exhaustive-deps
  const clock = useClock({ period: 12, rest: 3 });
  const a = (2 * Math.PI * clock.t) / 12, qx = 5 + 3.3 * Math.cos(a), qy = 5.2 + 3 * Math.sin(2 * a);
  const v = vote(qx, qy), R = v.nb[v.nb.length - 1][0];
  const P = plot({ x0: 0, x1: 10, y0: 0, y1: 10, pad: [8, 132, 10, 8] });
  const rx = P.X(R) - P.X(0), ry = P.Y(0) - P.Y(R);
  return (
    <Frame clock={clock} title="k-최근접 이웃"
      read={<>새 점(★)에서 {met === "l2" ? "유클리드" : "맨해튼"} 거리로 가장 가까운 <b>{k}</b> 개를 골라(선) 다수결로 무리를 정한다 · 지금 표: 파랑 {v.cnt[0]} · 빨강 {v.cnt[1]} · 초록 {v.cnt[2]} → <b style={{ color: KC[v.win] }}>{["파랑", "빨강", "초록"][v.win]}</b> · 바탕색 = 그 자리의 판정 · k = 1 이면 경계가 들쭉날쭉(분산 큼), k 가 크면 매끄럽지만 작은 무리가 묻힌다(편향 큼) · {met === "l2" ? "이웃 범위가 원" : "이웃 범위가 마름모"}</>}
      controls={<>
        <Seg value={k} onChange={setK} options={[[1, "k = 1"], [3, "k = 3"], [7, "k = 7"], [15, "k = 15"]]} />
        <Seg value={met} onChange={setMet} options={[["l2", "유클리드"], ["l1", "맨해튼"]]} />
      </>}>
      {grid.map(([i, j, c]) => <rect key={i + "-" + j} x={P.X(i / 3)} y={P.Y((j + 1) / 2.7)} width={P.X(1 / 3) - P.X(0) + 0.3} height={P.Y(0) - P.Y(1 / 2.7) + 0.3} fill={KC[c]} opacity="0.13" />)}
      {met === "l2"
        ? <ellipse cx={P.X(qx)} cy={P.Y(qy)} rx={rx} ry={ry} fill="none" stroke={C.ink} strokeWidth="1.3" strokeDasharray="4 3" />
        : <path d={`M${P.X(qx - R)} ${P.Y(qy)}L${P.X(qx)} ${P.Y(qy + R)}L${P.X(qx + R)} ${P.Y(qy)}L${P.X(qx)} ${P.Y(qy - R)}Z`} fill="none" stroke={C.ink} strokeWidth="1.3" strokeDasharray="4 3" />}
      {v.nb.map(([, i]) => <line key={"l" + i} x1={P.X(qx)} y1={P.Y(qy)} x2={P.X(X[i][0])} y2={P.Y(X[i][1])} stroke={KC[X[i][2]]} strokeWidth="1" opacity="0.7" />)}
      {X.map(([x, y, c], i) => <circle key={i} cx={P.X(x)} cy={P.Y(y)} r={v.nb.some((q) => q[1] === i) ? 4.6 : 3.4} fill={KC[c]} stroke={C.card} strokeWidth="1" />)}
      <text x={P.X(qx)} y={P.Y(qy) + 6} textAnchor="middle" fontSize="18" fill={KC[v.win]} stroke={C.ink} strokeWidth="0.8">★</text>
      <text x="238" y="30" fontSize="10" fontWeight="800" fill={C.ink}>이웃 {k} 개의 표</text>
      {v.cnt.map((c, i) => (
        <g key={i}>
          <rect x="238" y={44 + i * 26} width={clamp((c / k) * 100, 0, 100)} height="14" rx="2" fill={KC[i]} opacity="0.7" />
          <text x={244 + clamp((c / k) * 100, 0, 100)} y={55 + i * 26} fontSize="10" fill={C.ink}>{c}</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── A/B 시험: 전환율 차이와 z 통계량 — 중간에 엿보고 멈추면 속는다 ── */
function abSim(seed, pa, pb, N = 4000, step = 50) {
  const r = rng(seed), out = [];
  let ca = 0, cb = 0;
  for (let n = 1; n <= N; n++) {
    if (r() < pa) ca++;
    if (r() < pb) cb++;
    if (n % step === 0) { const pp = (ca + cb) / (2 * n), se = Math.sqrt((pp * (1 - pp) * 2) / n), z = se > 0 ? (cb / n - ca / n) / se : 0; out.push({ n, a: ca / n, b: cb / n, z }); }
  }
  return out;
}
export function ABTest({ p = {} }) {
  const [sc, setSc] = useState(p.scene === "null" ? "null" : "diff");
  const D = useMemo(() => (sc === "diff" ? abSim(7, 0.1, 0.12) : abSim(91, 0.1, 0.1)), [sc]);
  const clock = useClock({ period: 12, rest: 11 });
  const k = Math.min(D.length - 1, Math.floor((clock.t / 10) * D.length));
  const cur = D[k], peek = D.findIndex((q) => Math.abs(q.z) > 1.96);
  const pval = 2 * (1 - Phi(Math.abs(cur.z)));
  const L = plot({ x0: 0, x1: 4000, y0: 0.05, y1: 0.17, pad: [12, 186, 24, 30] });
  const R = plot({ x0: 0, x1: 4000, y0: -3.5, y1: 3.5, pad: [12, 8, 24, 208] });
  const band = (key) => {
    const up = D.slice(0, k + 1).map((q) => [q.n, q[key] + 1.96 * Math.sqrt((q[key] * (1 - q[key])) / q.n)]);
    const dn = D.slice(0, k + 1).map((q) => [q.n, q[key] - 1.96 * Math.sqrt((q[key] * (1 - q[key])) / q.n)]).reverse();
    return L.poly([...up, ...dn].map(([x, y]) => [x, clamp(y, 0.05, 0.17)])) + "Z";
  };
  return (
    <Frame clock={clock} title="A/B 시험"
      read={<>{sc === "diff" ? "B 안의 참 전환율 12 %, A 안 10 %" : "두 안의 참 전환율이 똑같이 10 %"} · 방문자 {cur.n} 명씩: A {fmt(cur.a * 100, 1)} %, B {fmt(cur.b * 100, 1)} %, z = <b>{fmt(cur.z, 2)}</b>, p 값 = <b>{fmt(pval, 3)}</b>(띠 = 95 % 신뢰구간) · 10 % → 12 % 를 검정력 80 % 로 잡으려면 한쪽에 약 3800 명이 필요해 미리 정한 4000 명까지 기다린다{peek >= 0 && peek <= k ? <> · {D[peek].n} 명에서 처음 |z| &gt; 1.96(빨간 점) — 여기서 엿보고 멈췄다면 {sc === "null" ? <b>차이가 없는데도 ‘유의’라 속았다</b> : "결론은 같지만 운이 좋았던 것"}</> : ""}</>}
      controls={<Seg value={sc} onChange={(v) => { setSc(v); clock.reset(); }} options={[["diff", "차이 있음"], ["null", "차이 없음"]]} />}>
      <Axes p={L} xl="n" yl="전환율" grid={false} xt={[2000, 4000]} yt={[0.08, 0.1, 0.12, 0.14, 0.16]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v * 100, 0) + "%"} />
      <path d={band("a")} fill={C.blue} opacity="0.15" />
      <path d={band("b")} fill={C.red} opacity="0.15" />
      <path d={L.poly(D.slice(0, k + 1).map((q) => [q.n, clamp(q.a, 0.05, 0.17)]))} fill="none" stroke={C.blue} strokeWidth="1.8" />
      <path d={L.poly(D.slice(0, k + 1).map((q) => [q.n, clamp(q.b, 0.05, 0.17)]))} fill="none" stroke={C.red} strokeWidth="1.8" />
      <Label x={L.r - 26} y={L.t + 10} size={9.5} color={C.blue} bold bg>A</Label>
      <Label x={L.r - 10} y={L.t + 10} size={9.5} color={C.red} bold bg>B</Label>
      <Axes p={R} xl="n" yl="z" grid={false} xt={[2000, 4000]} yt={[-2, 2]} xfmt={(v) => fmt(v, 0)} />
      <rect x={R.l} y={R.Y(1.96)} width={R.r - R.l} height={R.Y(-1.96) - R.Y(1.96)} fill={C.green} opacity="0.08" />
      {[1.96, -1.96].map((v) => <line key={v} x1={R.l} x2={R.r} y1={R.Y(v)} y2={R.Y(v)} stroke={C.green} strokeDasharray="4 3" />)}
      <path d={R.poly(D.slice(0, k + 1).map((q) => [q.n, clamp(q.z, -3.5, 3.5)]))} fill="none" stroke={C.ink} strokeWidth="1.8" />
      {peek >= 0 && peek <= k && <circle cx={R.X(D[peek].n)} cy={R.Y(clamp(D[peek].z, -3.5, 3.5))} r="4.5" fill={C.red} />}
      <text x={R.r - 2} y={R.Y(1.96) - 4} textAnchor="end" fontSize="9" fill={C.green}>±1.96</text>
    </Frame>
  );
}

/* ── 해시 테이블: 칸에 고르게 흩어도 충돌은 생긴다 — 사슬 길이의 분포는 푸아송 ── */
export function HashTable({ p = {} }) {
  const [m, setM] = useState(p.m === 64 ? 64 : 16);
  const nmax = 2 * m;
  const seq = useMemo(() => { const r = rng(m === 16 ? 5 : 9); return Array.from({ length: nmax }, () => Math.floor(r() * m)); }, [m, nmax]);
  const clock = useClock({ period: 12, rest: 5.5 });
  const n = Math.min(nmax, Math.floor((clock.t / 10) * nmax) + 1);
  const ch = Array(m).fill(0);
  let first = -1;
  seq.slice(0, n).forEach((b, i) => { if (ch[b] > 0 && first < 0) first = i + 1; ch[b]++; });
  const last = seq[n - 1], alpha = n / m;
  const hist = Array(7).fill(0); ch.forEach((c) => hist[Math.min(6, c)]++);
  const pois = (j) => { let f = 1; for (let i = 2; i <= j; i++) f *= i; return (m * Math.exp(-alpha) * alpha ** j) / f; };
  const bw = 300 / m, X0 = 30, BASE = 112, UH = m === 16 ? 11 : 9;
  const H = plot({ x0: -0.5, x1: 6.5, y0: 0, y1: Math.max(m * 0.45, ...hist) * 1.1, pad: [146, 10, 22, 30] });
  return (
    <Frame clock={clock} title="해시 테이블 — 충돌과 사슬"
      read={<>키를 해시로 {m} 칸 가운데 하나에 넣고, 같은 칸에 온 키는 사슬로 매단다 · 키 {n} 개, 적재율 α = n/m = <b>{fmt(alpha, 2)}</b> · 첫 충돌은 {first > 0 ? <><b>{first}</b> 번째 키</> : "아직"}(생일 문제: 대략 √(πm/2) ≈ {fmt(Math.sqrt((Math.PI * m) / 2), 1)} 번째) · 아래 막대 = 사슬 길이별 칸 수, 점 = 푸아송 분포의 기댓값(빈 칸 비율 exp(−α)) · 평균 탐색 비용 1 + α/2 — α 가 커지면 칸을 두 배로 늘린다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[[16, "칸 16"], [64, "칸 64"]]} />}>
      {ch.map((c, b) => (
        <g key={b}>
          {Array.from({ length: c }, (_, j) => <rect key={j} x={X0 + b * bw + 0.6} y={BASE - (j + 1) * UH} width={bw - 1.2} height={UH - 1} rx="1.5" fill={b === last && j === c - 1 ? C.red : C.sp} opacity={b === last && j === c - 1 ? 0.95 : 0.55} />)}
          {m === 16 && <text x={X0 + b * bw + bw / 2} y={BASE + 11} textAnchor="middle" fontSize="8" fill={C.mut}>{b}</text>}
        </g>
      ))}
      <line x1={X0} x2={X0 + 300} y1={BASE} y2={BASE} stroke={C.mut} />
      <text x="14" y="22" fontSize="10" fontWeight="800" fill={C.ink}>칸마다 사슬(키 {n} 개)</text>
      <Axes p={H} xl="사슬 길이" yl="" grid={false} xt={[0, 1, 2, 3, 4, 5, 6]} yt={[]} xfmt={(v) => (v === 6 ? "6+" : fmt(v, 0))} />
      {hist.map((c, j) => <rect key={j} x={H.X(j - 0.32)} y={H.Y(c)} width={H.X(0.64) - H.X(0)} height={H.Y(0) - H.Y(c)} fill={C.sp} opacity="0.45" />)}
      {hist.map((_, j) => <circle key={"p" + j} cx={H.X(j)} cy={H.Y(j < 6 ? pois(j) : Math.max(0, m - [0, 1, 2, 3, 4, 5].reduce((s, i) => s + pois(i), 0)))} r="3.2" fill={C.red} />)}
    </Frame>
  );
}

/* ── 블룸 필터: 비트 k 개를 켜 두고, 모두 켜져 있으면 ‘있을 수도’ ── */
const BM = 32;
const hash32 = (s) => {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  h ^= h >>> 16; h = Math.imul(h, 0x85ebca6b) >>> 0; h ^= h >>> 13; h = Math.imul(h, 0xc2b2ae35) >>> 0; h ^= h >>> 16;
  return h >>> 0;
};
const bbits = (w, k) => Array.from({ length: k }, (_, i) => hash32(w + "#" + i) % BM);
const BITEMS = ["사과", "배", "감", "귤", "포도", "딸기", "수박", "참외"], BQ = ["사과", "레몬", "망고", "키위"];
export function Bloom({ p = {} }) {
  const [k, setK] = useState(clamp(p.k ?? 3, 1, 6));
  const clock = useClock({ period: 14, rest: 12.5 });
  const ni = Math.min(BITEMS.length, Math.floor(clock.t / 0.75) + 1);
  const qt = clock.t - BITEMS.length * 0.75;
  const nq = qt < 0 ? 0 : Math.min(BQ.length, Math.floor(qt / 1.2) + 1);
  const on = new Set();
  BITEMS.slice(0, ni).forEach((w) => bbits(w, k).forEach((b) => on.add(b)));
  const hot = nq > 0 ? bbits(BQ[nq - 1], k) : bbits(BITEMS[ni - 1], k);
  const res = BQ.slice(0, nq).map((w) => { const all = bbits(w, k).every((b) => on.has(b)), real = BITEMS.includes(w); return [w, all, real]; });
  const fpTheory = (kk) => (1 - Math.exp((-kk * BITEMS.length) / BM)) ** kk;
  const F = plot({ x0: 1, x1: 6, y0: 0, y1: 0.3, pad: [130, 10, 22, 236] });
  return (
    <Frame clock={clock} title="블룸 필터"
      read={<>비트 {BM} 칸 · 낱말마다 해시 {k} 개로 고른 칸을 켠다(넣기) · 찾을 때 그 칸이 <b>모두 켜져 있으면 ‘있을 수도’</b>, 하나라도 꺼져 있으면 ‘확실히 없음’ — 없는 것을 있다고 할 수는 있어도(거짓 양성) 있는 것을 놓치지는 않는다 · 켜진 비트 {on.size} / {BM} · 거짓 양성 확률 ≈ (1 − exp(−kn/m))ᵏ = <b>{fmt(fpTheory(k) * 100, 1)} %</b>, 가장 좋은 k = (m/n) ln 2 ≈ 2.8</>}
      controls={<Slider label="해시 수 k" min={1} max={6} step={1} value={k} onChange={setK} />}>
      {Array.from({ length: BM }, (_, i) => {
        const x = 14 + (i % 16) * 21, y = 16 + Math.floor(i / 16) * 26, isHot = hot.includes(i);
        return (
          <g key={i}>
            <rect x={x} y={y} width="19" height="20" rx="3" fill={on.has(i) ? C.sp : C.card} opacity={on.has(i) ? 0.75 : 1} stroke={isHot ? C.red : C.bd} strokeWidth={isHot ? 2.2 : 1} />
            <text x={x + 9.5} y={y + 14} textAnchor="middle" fontSize="9" fontWeight="700" fill={on.has(i) ? C.card : C.mut}>{on.has(i) ? 1 : 0}</text>
          </g>
        );
      })}
      <text x="14" y="86" fontSize="10" fontWeight="800" fill={C.ink}>넣은 낱말</text>
      {BITEMS.map((w, i) => <text key={w} x={14 + (i % 4) * 54} y={102 + Math.floor(i / 4) * 16} fontSize="10" fill={i < ni ? (i === ni - 1 && nq === 0 ? C.red : C.ink) : C.bd} fontWeight={i === ni - 1 && nq === 0 ? 800 : 500}>{w}</text>)}
      <text x="14" y="146" fontSize="10" fontWeight="800" fill={C.ink}>찾기</text>
      {res.map(([w, all, real], i) => (
        <text key={w} x="14" y={162 + i * 14} fontSize="9.5" fill={!all ? C.green : real ? C.blue : C.red} fontWeight={i === nq - 1 ? 800 : 500}>
          {w}: {all ? (real ? "모두 켜짐 → 실제로 있음" : "모두 켜짐 → 실제는 없음(거짓 양성)") : "꺼진 비트 → 확실히 없음"}
        </text>
      ))}
      <Axes p={F} xl="k" yl="" grid={false} xt={[1, 2, 3, 4, 5, 6]} yt={[0.1, 0.2]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v * 100, 0) + "%"} />
      <path d={F.path(fpTheory, 1, 6)} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={F.X(k)} cy={F.Y(fpTheory(k))} r="4" fill={C.red} />
      <text x={F.l} y={F.t - 6} fontSize="9" fill={C.mut}>거짓 양성 확률(n = 8, m = 32)</text>
    </Frame>
  );
}

/* ── B-트리: 한 마디에 키를 많이 담아 나무를 낮게 — 디스크 읽기 횟수 = 높이 ── */
const BT_L1 = [[30, 60]], BT_L2 = [[10, 20], [40, 50], [70, 80]], BT_L3 = [[3, 7], [12, 16], [23, 27], [33, 37], [43, 47], [53, 57], [63, 67], [73, 77], [83, 87]];
const childIdx = (keys, x) => (x < keys[0] ? 0 : x < keys[1] ? 1 : 2);
export function BTree() {
  const keys = [37, 63, 16];
  const clock = useClock({ period: 12, rest: 3.4 });
  const ki = Math.min(2, Math.floor(clock.t / 4)), ph = clock.t - ki * 4, key = keys[ki];
  const c1 = childIdx(BT_L1[0], key), c2 = c1 * 3 + childIdx(BT_L2[c1], key);
  const lvl = ph < 1 ? 0 : ph < 2 ? 1 : 2, found = ph >= 2.6;
  const W1 = 70, W2 = 62, W3 = 34;
  const x1 = 180, x2 = [70, 180, 290], x3 = Array.from({ length: 9 }, (_, i) => 20 + i * 40);
  const box = (cx, y, w, ks, on, key2) => (
    <g key={key2}>
      <rect x={cx - w / 2} y={y} width={w} height="22" rx="4" fill={on ? "color-mix(in srgb, var(--sp, var(--ac)) 25%, var(--card))" : C.card} stroke={on ? C.sp : C.ink} strokeWidth={on ? 2.2 : 1.1} />
      {ks.map((k2, i) => <text key={i} x={cx - w / 2 + ((i + 0.5) * w) / ks.length} y={y + 15} textAnchor="middle" fontSize={w < 40 ? 9 : 11} fontWeight={found && k2 === key && on ? 800 : 600} fill={found && k2 === key && on ? C.red : C.ink}>{k2}</text>)}
      {ks.length > 1 && <line x1={cx} x2={cx} y1={y + 3} y2={y + 19} stroke={C.bd} />}
    </g>
  );
  const heights = [[2, 30], [16, 8], [256, 4], [1024, 3]];
  return (
    <Frame clock={clock} title="B-트리 색인"
      read={<>키 <b>{key}</b> 찾기: 뿌리에서 키와 비교해 들어갈 가지를 고르고 → 가운데 층 → 잎 · 마디 하나 = 디스크 블록 하나라서, 찾는 비용은 <b>나무의 높이(블록 읽기 3 번)</b> · 블록 하나에 키를 수백 개 담으면 10 억 개도 높이 3 ~ 4 — 디스크 한 번 읽기는 메모리 접근보다 수만 배 느리므로 높이가 곧 속도다 · 아래: 10 억 개(10⁹)를 담을 때 한 마디의 가지 수에 따른 높이</>}>
      {BT_L2.map((_, i) => <line key={"a" + i} x1={x1 - W1 / 2 + ((i + 0.5) * W1) / 3} y1="38" x2={x2[i]} y2="68" stroke={lvl >= 1 && i === c1 ? C.sp : C.bd} strokeWidth={lvl >= 1 && i === c1 ? 2.4 : 1.2} />)}
      {BT_L3.map((_, i) => { const pa = Math.floor(i / 3); return <line key={"b" + i} x1={x2[pa] - W2 / 2 + (((i % 3) + 0.5) * W2) / 3} y1="90" x2={x3[i]} y2="118" stroke={lvl >= 2 && i === c2 ? C.sp : C.bd} strokeWidth={lvl >= 2 && i === c2 ? 2.4 : 1.2} />; })}
      {box(x1, 16, W1, BT_L1[0], true, "r")}
      {BT_L2.map((ks, i) => box(x2[i], 68, W2, ks, lvl >= 1 && i === c1, "m" + i))}
      {BT_L3.map((ks, i) => box(x3[i], 118, W3, ks, lvl >= 2 && i === c2, "l" + i))}
      {heights.map(([b, h], i) => (
        <g key={b}>
          <text x="14" y={162 + i * 14} fontSize="9.5" fill={C.ink}>가지 {b}</text>
          <rect x="70" y={154 + i * 14} width={h * 8.4} height="10" rx="2" fill={i === 0 ? C.red : C.sp} opacity="0.6" />
          <text x={74 + h * 8.4} y={162 + i * 14} fontSize="9.5" fontWeight="800" fill={C.ink}>{h} 층</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── 조인: 같은 결과, 다른 비용 — 중첩 루프 · 해시 조인 · 정렬-병합 ── */
const JR = [[3, "지우"], [7, "민수"], [1, "서연"], [5, "하준"], [2, "유나"], [6, "도윤"]];
const JS = [[5, "미적분"], [1, "확률"], [7, "선형대수"], [3, "미적분"], [5, "통계"], [8, "물리"], [2, "확률"], [1, "알고리즘"]];
function joinFrames(kind) {
  const F = [], out = [];
  let ops = 0;
  const R = kind === "merge" ? [...JR].sort((a, b) => a[0] - b[0]) : JR, S = kind === "merge" ? [...JS].sort((a, b) => a[0] - b[0]) : JS;
  if (kind === "nested") {
    R.forEach((r, i) => S.forEach((s, j) => { ops++; const hit = r[0] === s[0]; if (hit) out.push([r[1], s[1]]); F.push({ i, j, ops, out: out.slice(), hit, R, S }); }));
  } else if (kind === "hash") {
    R.forEach((r, i) => { ops++; F.push({ i, j: -1, ops, out: [], build: i, R, S, note: "만들기" }); });
    S.forEach((s, j) => {
      const bucket = R.map((r, i) => [r, i]).filter(([r]) => r[0] % 4 === s[0] % 4);
      if (!bucket.length) { ops++; F.push({ i: -1, j, ops, out: out.slice(), R, S, note: "빈 칸" }); }
      bucket.forEach(([r, i]) => { ops++; const hit = r[0] === s[0]; if (hit) out.push([r[1], s[1]]); F.push({ i, j, ops, out: out.slice(), hit, R, S, note: "찾기" }); });
    });
  } else {
    let i = 0, j = 0;
    while (i < R.length && j < S.length) {
      ops++;
      const hit = R[i][0] === S[j][0];
      if (hit) out.push([R[i][1], S[j][1]]);
      F.push({ i, j, ops, out: out.slice(), hit, R, S });
      if (hit) j++; else if (R[i][0] < S[j][0]) i++; else j++;
    }
  }
  F.push({ ...F[F.length - 1], i: -1, j: -1, done: true });
  return F;
}
export function Join({ p = {} }) {
  const [kind, setKind] = useState(["nested", "hash", "merge"].includes(p.alg) ? p.alg : "nested");
  const F = useMemo(() => joinFrames(kind), [kind]);
  const clock = useClock({ period: 11, rest: 10.5 });
  const fi = Math.min(F.length - 1, Math.floor((clock.t / 9.5) * F.length));
  const f = F[fi];
  const row = (x, y, cells, on, hit, key) => (
    <g key={key}>
      <rect x={x} y={y} width="104" height="19" rx="3" fill={on ? (hit ? "color-mix(in srgb, #3f7d3a 28%, var(--card))" : "color-mix(in srgb, #b07d12 22%, var(--card))") : C.card} stroke={on ? (hit ? C.green : C.gold) : C.bd} strokeWidth={on ? 1.8 : 0.8} />
      <text x={x + 8} y={y + 13.5} fontSize="10" fontWeight="800" fill={C.ink}>{cells[0]}</text>
      <text x={x + 28} y={y + 13.5} fontSize="10" fill={C.ink}>{cells[1]}</text>
    </g>
  );
  const note = { nested: "중첩 루프: R 의 행마다 S 를 처음부터 끝까지 훑는다 — 6 × 8 = 48 번", hash: "해시 조인: R 의 번호로 해시표(번호 mod 4)를 만들고, S 의 행마다 같은 칸만 본다 — 대략 6 + 8 번", merge: "정렬-병합: 둘 다 번호순으로 정렬한 뒤 두 줄을 나란히 한 번 훑는다 — 정렬 비용 + 6 + 8 번" }[kind];
  return (
    <Frame clock={clock} title="조인 알고리즘"
      read={<>학생(R) ⋈ 수강(S) — 번호가 같은 행끼리 잇는다 · {note} · 지금까지 비교 <b>{f.ops}</b> 번, 결과 {f.out.length} 행 · 행이 n, m 개면 중첩 루프 n × m, 해시 n + m, 정렬-병합 n log n + m log m — 같은 결과를 내는 방법 가운데 가장 싼 것을 고르는 것이 질의 최적화기다</>}
      controls={<Seg value={kind} onChange={(v) => { setKind(v); clock.reset(); }} options={[["nested", "중첩 루프"], ["hash", "해시 조인"], ["merge", "정렬-병합"]]} />}>
      <text x="14" y="14" fontSize="10" fontWeight="800" fill={C.ink}>R 학생</text>
      <text x="134" y="14" fontSize="10" fontWeight="800" fill={C.ink}>S 수강</text>
      <text x="254" y="14" fontSize="10" fontWeight="800" fill={C.ink}>R ⋈ S</text>
      {f.R.map((r, i) => (
        <g key={"r" + i}>
          {row(14, 20 + i * 22, r, i === f.i || (f.build != null && i <= f.build), f.hit && i === f.i, "rr" + i)}
          {kind === "hash" && (f.build == null || i <= f.build || f.j >= 0) && <text x="106" y={33 + i * 22} textAnchor="end" fontSize="8.5" fill={C.violet}>칸 {r[0] % 4}</text>}
        </g>
      ))}
      {f.S.map((s, j) => (
        <g key={"s" + j}>
          {row(134, 20 + j * 22, s, j === f.j, f.hit && j === f.j, "ss" + j)}
          {kind === "hash" && j === f.j && <text x="234" y={33 + j * 22} textAnchor="end" fontSize="8.5" fill={C.violet}>칸 {s[0] % 4}</text>}
        </g>
      ))}
      {f.out.map(([a, b], k) => (
        <g key={"o" + k}>
          <rect x="254" y={20 + k * 22} width="100" height="19" rx="3" fill={C.card} stroke={C.green} strokeWidth="1" />
          <text x="260" y={33.5 + k * 22} fontSize="9.5" fill={C.ink}>{a} · {b}</text>
        </g>
      ))}
      <text x="350" y="212" textAnchor="end" fontSize="10.5" fontWeight="800" fill={C.red}>비교 {f.ops} 번</text>
    </Frame>
  );
}

/* ── 저수지 표집: 끝을 모르는 흐름에서 k 개를 고르게 — i 번째는 k/i 확률로 들어온다 ── */
const RK = 5;
function reservoirRun(N, seed) {
  const r = rng(seed), res = [], F = [];
  for (let i = 1; i <= N; i++) {
    let slot = -1;
    if (i <= RK) { res.push(i); slot = i - 1; }
    else { const j = Math.floor(r() * i); if (j < RK) { res[j] = i; slot = j; } }
    F.push({ i, slot, res: res.slice() });
  }
  return F;
}
export function Reservoir({ p = {} }) {
  const [N, setN] = useState(p.N === 50 ? 50 : 20);
  const F = useMemo(() => reservoirRun(N, 3), [N]);
  const hist = useMemo(() => {
    const h = Array(N).fill(0), runs = 3000;
    for (let s = 0; s < runs; s++) reservoirRun(N, 100 + s)[N - 1].res.forEach((v) => h[v - 1]++);
    return h.map((c) => c / runs);
  }, [N]);
  const clock = useClock({ period: 12, rest: 11 });
  const fi = Math.min(N - 1, Math.floor((clock.t / 10) * N));
  const f = F[fi], w = 330 / N;
  const H = plot({ x0: 0, x1: N, y0: 0, y1: 0.5, pad: [118, 10, 22, 30] });
  return (
    <Frame clock={clock} title="저수지 표집"
      read={<>끝없이 들어오는 자료에서 메모리 {RK} 칸만으로 고르게 표본을 뽑는다 · 처음 {RK} 개는 그냥 담고, i 번째는 확률 {RK}/i 로 뽑아 저수지의 무작위 한 칸과 바꾼다 · 지금 {f.i} 번째{f.slot >= 0 && f.i > RK ? <> — <b>{f.slot + 1} 번 칸과 바꿈</b></> : f.i > RK ? " — 버림" : ""} · 아래: 3000 번 되풀이했을 때 각 항목이 마지막 표본에 든 비율 — 모두 {RK}/{N} = <b>{fmt(RK / N, 2)}</b> 근처로 고르다(귀납법으로 증명된다)</>}
      controls={<Seg value={N} onChange={(v) => { setN(v); clock.reset(); }} options={[[20, "흐름 20 개"], [50, "흐름 50 개"]]} />}>
      {Array.from({ length: N }, (_, i) => (
        <rect key={i} x={14 + i * w} y="16" width={Math.max(1, w - 1.5)} height="16" rx="2" fill={i + 1 === f.i ? C.red : i + 1 < f.i ? C.mut : C.card} opacity={i + 1 <= f.i ? 0.75 : 1} stroke={C.bd} strokeWidth="0.6" />
      ))}
      <text x="14" y="48" fontSize="9.5" fill={C.mut}>흐름 → (빨강 = 지금 들어온 항목)</text>
      {f.res.map((v, j) => (
        <g key={j}>
          <rect x={62 + j * 50} y="58" width="42" height="34" rx="6" fill={j === f.slot && f.i > RK ? "color-mix(in srgb, #b4442e 24%, var(--card))" : C.card} stroke={j === f.slot ? C.red : C.sp} strokeWidth={j === f.slot ? 2.4 : 1.4} />
          <text x={83 + j * 50} y="80" textAnchor="middle" fontSize="13" fontWeight="800" fill={C.ink}>{v}</text>
        </g>
      ))}
      <text x="14" y="80" fontSize="10" fontWeight="800" fill={C.sp}>저수지</text>
      <Axes p={H} xl="" yl="" grid={false} xt={[N / 2, N]} yt={[0.25, 0.5]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 2)} />
      {hist.map((v, i) => <rect key={i} x={H.X(i) + 0.4} y={H.Y(v)} width={Math.max(1, H.X(1) - H.X(0) - 0.8)} height={H.Y(0) - H.Y(v)} fill={C.sp} opacity="0.5" />)}
      <line x1={H.l} x2={H.r} y1={H.Y(RK / N)} y2={H.Y(RK / N)} stroke={C.red} strokeDasharray="4 3" />
    </Frame>
  );
}

/* ── 페이지랭크: 링크를 따라 걷는 서퍼가 각 쪽에 머무는 비율 ── */
const PN = [["A", 60, 46], ["B", 160, 30], ["C", 112, 120], ["D", 34, 170], ["E", 176, 186], ["F", 214, 110]];
const PL = { 0: [1, 2], 1: [2], 2: [0], 3: [2], 4: [2, 3, 5], 5: [4, 1] };
function prIter(d = 0.85, it = 16) {
  const n = PN.length, out = [];
  let r = Array(n).fill(1 / n);
  out.push(r);
  for (let t = 0; t < it; t++) {
    const nr = Array(n).fill((1 - d) / n);
    for (let u = 0; u < n; u++) for (const v of PL[u]) nr[v] += (d * r[u]) / PL[u].length;
    r = nr; out.push(r);
  }
  return out;
}
function surfWalk(steps, d = 0.85) {
  const r = rng(29), path = [0];
  for (let s = 1; s < steps; s++) { const u = path[s - 1]; path.push(r() < d ? PL[u][Math.floor(r() * PL[u].length)] : Math.floor(r() * PN.length)); }
  return path;
}
export function PageRank({ p = {} }) {
  const [m, setM] = useState(p.mode === "surf" ? "surf" : "power");
  const IT = useMemo(() => prIter(), []);
  const W = useMemo(() => surfWalk(3000), []);
  const clock = useClock({ period: 12, rest: 11 });
  let r, label;
  if (m === "power") { const k = Math.min(IT.length - 1, Math.floor(clock.t / 0.6)); r = IT[k]; label = `거듭제곱 ${k} 번`; }
  else {
    const s = Math.max(1, Math.min(W.length, Math.floor((clock.t / 10) * W.length)));
    const cnt = Array(PN.length).fill(0); W.slice(0, s).forEach((v) => cnt[v]++);
    r = cnt.map((c) => c / s); label = `서퍼 ${s} 걸음`;
  }
  const fin = IT[IT.length - 1];
  const cur = m === "surf" ? W[Math.max(0, Math.min(W.length - 1, Math.floor((clock.t / 10) * W.length) - 1))] : -1;
  return (
    <Frame clock={clock} title="페이지랭크"
      read={<>쪽(마디)과 링크(화살표) · 서퍼가 85 % 확률로 지금 쪽의 링크 하나를 골라 따라가고, 15 % 확률로 아무 쪽으로나 순간이동한다 — 오래 걸었을 때 각 쪽에 머무는 비율이 페이지랭크다(마르코프 연쇄의 정상분포) · {m === "power" ? "거듭제곱법: r ← 0.15/6 + 0.85 × (들어오는 링크로 나눠 받은 몫) 을 되풀이하면 몇 번 만에 수렴한다" : "실제로 걸어 보며 머문 횟수를 세면 같은 값으로 다가간다"} · {label}: C 가 <b>{fmt(r[2], 3)}</b> 로 가장 높다 — 링크를 많이 받고, 높은 쪽(A)에서도 받기 때문</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["power", "거듭제곱법"], ["surf", "무작위 서퍼"]]} />}>
      {Object.entries(PL).flatMap(([u, vs]) => vs.map((v) => {
        const [, x1, y1] = PN[u], [, x2, y2] = PN[v], a = Math.atan2(y2 - y1, x2 - x1), r2 = 12 + 22 * Math.sqrt(fin[v]);
        const ex = x2 - r2 * Math.cos(a), ey = y2 - r2 * Math.sin(a), off = PL[v].includes(+u) ? 5 : 0;
        const ox = -off * Math.sin(a), oy = off * Math.cos(a);
        return (
          <g key={u + "-" + v}>
            <line x1={x1 + ox} y1={y1 + oy} x2={ex + ox} y2={ey + oy} stroke={C.mut} strokeWidth="1.3" />
            <polygon points={`${ex + ox},${ey + oy} ${ex + ox - 7 * Math.cos(a) - 3.2 * Math.sin(a)},${ey + oy - 7 * Math.sin(a) + 3.2 * Math.cos(a)} ${ex + ox - 7 * Math.cos(a) + 3.2 * Math.sin(a)},${ey + oy - 7 * Math.sin(a) - 3.2 * Math.cos(a)}`} fill={C.mut} />
          </g>
        );
      }))}
      {PN.map(([n, x, y], i) => (
        <g key={n}>
          <circle cx={x} cy={y} r={10 + 22 * Math.sqrt(r[i])} fill={i === cur ? C.red : C.sp} opacity={i === cur ? 0.5 : 0.25} stroke={i === cur ? C.red : C.sp} strokeWidth="1.5" />
          <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{n}</text>
        </g>
      ))}
      {PN.map(([n], i) => (
        <g key={"b" + n}>
          <text x="252" y={34 + i * 28} fontSize="10" fontWeight="800" fill={C.ink}>{n}</text>
          <rect x="264" y={25 + i * 28} width={clamp(r[i] * 160, 0, 62)} height="12" rx="2" fill={C.sp} opacity="0.65" />
          <line x1={264 + fin[i] * 160} x2={264 + fin[i] * 160} y1={22 + i * 28} y2={40 + i * 28} stroke={C.red} strokeWidth="1.4" />
          <text x={268 + clamp(r[i] * 160, 0, 62)} y={34 + i * 28} fontSize="9" fill={C.mut}>{fmt(r[i], 2)}</text>
        </g>
      ))}
      <text x="252" y="206" fontSize="9" fill={C.red}>| 수렴값</text>
    </Frame>
  );
}
