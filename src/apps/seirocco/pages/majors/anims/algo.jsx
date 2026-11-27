// 알고리즘 그림 — 증가율(빅오) · 정렬(삽입 · 병합 · 퀵) · 재귀 나무(마스터 정리) · 힙 · 너비/깊이 우선 탐색 · 최소 신장 나무(크루스칼 · 프림) · 편집 거리(동적계획법) · 외판원 문제(탐욕 · 2-opt · 전수 조사)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Label, fmt, clamp, rng, sup, useClock } from "./kit.jsx";

/* ── 증가율: 1 초에 10⁹ 번 계산하는 컴퓨터로 n 이 커지면 ── */
const LG10_2 = Math.log10(2);
const lfact10 = (n) => (n < 2 ? 0 : (n * Math.log(n) - n + 0.5 * Math.log(2 * Math.PI * n)) / Math.LN10);
const GROW = [
  ["log n", (L) => Math.log10(Math.max(1, L / LG10_2)), (n) => Math.log2(Math.max(1, n)), C.green],
  ["n", (L) => L, (n) => n, C.teal],
  ["n log n", (L) => L + Math.log10(Math.max(1, L / LG10_2)), (n) => n * Math.log2(Math.max(1, n)), C.blue],
  ["n²", (L) => 2 * L, (n) => n * n, C.gold],
  ["2ⁿ", (L) => 10 ** L * LG10_2, (n) => 2 ** n, C.red],
  ["n!", (L) => lfact10(10 ** L), (n) => { let f = 1; for (let k = 2; k <= n; k++) f *= k; return f; }, C.violet],
];
const YEAR = Math.log10(3.156e7);
function human(L) {
  if (L < 3) return fmt(10 ** L, 0) + " ns";
  if (L < 6) return fmt(10 ** (L - 3), 1) + " μs";
  if (L < 9) return fmt(10 ** (L - 6), 1) + " ms";
  const s = L - 9;
  if (s < Math.log10(60)) return fmt(10 ** s, 1) + " 초";
  if (s < Math.log10(3600)) return fmt(10 ** s / 60, 1) + " 분";
  if (s < Math.log10(86400)) return fmt(10 ** s / 3600, 1) + " 시간";
  if (s < YEAR) return fmt(10 ** s / 86400, 1) + " 일";
  const y = s - YEAR;
  if (y < 4) return fmt(10 ** y, 0) + " 년";
  if (y < 8) return fmt(10 ** (y - 4), 0) + " 만 년";
  if (y < 10.14) return fmt(10 ** (y - 8), 0) + " 억 년";
  return "우주 나이보다 김";
}
export function BigO({ p = {} }) {
  const [k, setK] = useState(clamp(p.k ?? 3, 1, 7));
  const clock = useClock({ period: 9, rest: 7 });
  const P = plot({ x0: 1, x1: 20, y0: 0, y1: 300, pad: [12, 204, 24, 30] });
  const x = 1 + 19 * clamp(clock.t / 8, 0, 1);
  return (
    <Frame clock={clock} title="증가율 — 빅오"
      read={<>1 초에 10⁹ 번 계산하는 컴퓨터로 입력 n = <b>10{sup(k)}</b> 을 처리하는 시간(연산 1 번 = 1 ns) · 왼쪽: n ≤ 20 에서도 2ⁿ · n! 은 금세 그림 밖으로 · n 이 10 배가 되면 n log n 은 10 배 남짓, n² 은 100 배, 2ⁿ 은 거듭제곱으로 폭발한다 — 빠른 컴퓨터보다 <b>좋은 알고리즘</b>이 이긴다</>}
      controls={<Slider label="입력 크기" min={1} max={7} step={1} value={k} onChange={setK} show={(v) => "n = 10" + sup(v)} />}>
      <Axes p={P} xl="n" yl="연산" grid={false} xt={[5, 10, 15, 20]} yt={[100, 200, 300]} xfmt={(v) => fmt(v, 0)} yfmt={(v) => fmt(v, 0)} />
      {GROW.map(([n, , f, col]) => <path key={n} d={P.path(f, 1, 20, 240)} fill="none" stroke={col} strokeWidth="2" />)}
      <line x1={P.X(x)} x2={P.X(x)} y1={P.t} y2={P.b} stroke={C.mut} strokeDasharray="3 3" />
      {GROW.map(([n, , f, col]) => { const v = f(x); return v <= 300 ? <circle key={n} cx={P.X(x)} cy={P.Y(v)} r="3.5" fill={col} /> : null; })}
      <text x="168" y="22" fontSize="10" fontWeight="800" fill={C.ink}>n = 10{sup(k)} 일 때 걸리는 시간</text>
      {GROW.map(([n, L10, , col], i) => {
        const L = L10(k), y = 44 + i * 28, w = clamp((L / 30) * 62, 1, 62);
        return (
          <g key={n}>
            <text x="168" y={y + 4} fontSize="10.5" fontWeight="800" fill={col}>{n}</text>
            <rect x="214" y={y - 5} width={w} height="10" rx="2" fill={col} opacity="0.55" />
            {L > 30 && <text x="278" y={y + 4} fontSize="9" fill={col}>…</text>}
            <text x="286" y={y + 4} fontSize="9.5" fill={C.ink}>{human(L)}</text>
          </g>
        );
      })}
    </Frame>
  );
}

/* ── 정렬: 비교 횟수를 센다 ── */
function sortFrames(kind, arr) {
  const a = arr.slice(), F = [];
  let cmp = 0;
  const snap = (hi, rg) => F.push({ a: a.slice(), hi, cmp, rg });
  if (kind === "ins") {
    for (let i = 1; i < a.length; i++) {
      let j = i;
      while (j > 0) { cmp++; snap([j - 1, j], [0, i + 1]); if (a[j - 1] > a[j]) { [a[j - 1], a[j]] = [a[j], a[j - 1]]; j--; } else break; }
    }
  } else if (kind === "merge") {
    const rec = (lo, hi) => {
      if (hi - lo < 2) return;
      const mid = (lo + hi) >> 1;
      rec(lo, mid); rec(mid, hi);
      const L = a.slice(lo, mid), R = a.slice(mid, hi);
      let i = 0, j = 0, k = lo;
      while (i < L.length && j < R.length) { cmp++; a[k++] = L[i] <= R[j] ? L[i++] : R[j++]; snap([k - 1], [lo, hi]); }
      while (i < L.length) { a[k++] = L[i++]; snap([k - 1], [lo, hi]); }
      while (j < R.length) { a[k++] = R[j++]; snap([k - 1], [lo, hi]); }
    };
    rec(0, a.length);
  } else {
    const rec = (lo, hi) => {
      if (lo >= hi) return;
      const pv = a[hi];
      let i = lo;
      for (let j = lo; j < hi; j++) { cmp++; snap([j, hi], [lo, hi + 1]); if (a[j] < pv) { [a[i], a[j]] = [a[j], a[i]]; i++; } }
      [a[i], a[hi]] = [a[hi], a[i]];
      snap([i], [lo, hi + 1]);
      rec(lo, i - 1); rec(i + 1, hi);
    };
    rec(0, a.length - 1);
  }
  snap([], null);
  return F;
}
const SN = 16;
function sortInput(kind) {
  const a = Array.from({ length: SN }, (_, i) => i + 1);
  if (kind === "rev") return a.reverse();
  if (kind === "near") { [a[3], a[4]] = [a[4], a[3]]; [a[10], a[12]] = [a[12], a[10]]; return a; }
  const r = rng(7);
  for (let i = SN - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
const SORT_NOTE = {
  ins: "삽입 정렬: 하나씩 꺼내 앞쪽 정렬된 부분의 제자리에 끼운다 — 최악 n(n − 1)/2 = 120 번, 거의 정렬된 입력에는 매우 빠르다",
  merge: "병합 정렬: 반으로 나눠 각각 정렬한 뒤 두 줄을 앞에서부터 비교하며 합친다 — 입력과 상관없이 n log₂ n ≈ 64 번 안팎",
  quick: "퀵 정렬: 기준값(맨 끝)보다 작은 것을 앞으로 모으고 양쪽을 따로 정렬 — 평균 1.39 n log₂ n, 이미 정렬된 입력에서는 최악 120 번",
};
export function Sorting({ p = {} }) {
  const [alg, setAlg] = useState(SORT_NOTE[p.alg] ? p.alg : "merge");
  const [inp, setInp] = useState(["rand", "near", "rev"].includes(p.input) ? p.input : "rand");
  const F = useMemo(() => sortFrames(alg, sortInput(inp)), [alg, inp]);
  const clock = useClock({ period: 12, rest: 11.5 });
  const fi = Math.min(F.length - 1, Math.floor((clock.t / 10) * F.length));
  const fr = F[fi], done = fi === F.length - 1;
  const X = (i) => 16 + i * 21, BASE = 186;
  return (
    <Frame clock={clock} title="정렬 알고리즘"
      read={<>{SORT_NOTE[alg]} · 지금까지 비교 <b>{fr.cmp}</b> 번{done ? " — 끝" : ""} · 비교로 정렬하려면 최악에 적어도 log₂(n!) ≈ n log₂ n 번이 필요하다(16 개면 45 번)</>}
      controls={<>
        <Seg value={alg} onChange={(v) => { setAlg(v); clock.reset(); }} options={[["ins", "삽입"], ["merge", "병합"], ["quick", "퀵"]]} />
        <Seg value={inp} onChange={(v) => { setInp(v); clock.reset(); }} options={[["rand", "무작위"], ["near", "거의 정렬"], ["rev", "역순"]]} />
      </>}>
      {fr.rg && <rect x={X(fr.rg[0]) - 2} y="22" width={X(fr.rg[1]) - X(fr.rg[0])} height={BASE - 18} rx="4" fill={C.sp} opacity="0.08" />}
      {fr.a.map((v, i) => {
        const hot = fr.hi.includes(i);
        return <rect key={i} x={X(i)} y={BASE - v * 9.4} width="17" height={v * 9.4} rx="2" fill={done ? C.green : hot ? C.red : C.blue} opacity={hot || done ? 0.9 : 0.55} />;
      })}
      <line x1="12" x2="350" y1={BASE} y2={BASE} stroke={C.mut} />
      <text x="16" y="16" fontSize="11" fontWeight="800" fill={C.ink}>비교 {fr.cmp} 번</text>
      <text x="350" y="16" textAnchor="end" fontSize="9.5" fill={C.mut}>n = 16 · n(n − 1)/2 = 120 · n log₂ n = 64</text>
      <text x="350" y="204" textAnchor="end" fontSize="9.5" fill={C.mut}>{fi + 1} / {F.length} 단계</text>
    </Frame>
  );
}

/* ── 재귀 나무: T(n) = aT(n/b) + nᵈ — 층마다 일의 양을 더한다 ── */
const REC = {
  linear: { a: 1, b: 2, d: 1, eq: "T(n) = T(n/2) + n", ans: "Θ(n)", why: "층마다 일이 절반으로 줄어 맨 위층이 전체를 좌우한다(n + n/2 + n/4 + … < 2n)" },
  merge: { a: 2, b: 2, d: 1, eq: "T(n) = 2T(n/2) + n", ans: "Θ(n log n)", why: "층마다 일이 같아(n) 층 수 log₂ n 을 곱한다 — 병합 정렬" },
  bsearch: { a: 1, b: 2, d: 0, eq: "T(n) = T(n/2) + 1", ans: "Θ(log n)", why: "층마다 일이 1 로 같아 층 수 log₂ n — 이진 탐색" },
  kara: { a: 3, b: 2, d: 1, eq: "T(n) = 3T(n/2) + n", ans: "Θ(n 의 1.585 제곱)", why: "층마다 일이 1.5 배씩 늘어 맨 아래층(잎 3 의 log₂ n 제곱 개)이 전체를 좌우한다 — 카라추바 곱셈" },
};
export function RecTree({ p = {} }) {
  const [c, setC] = useState(REC[p.rec] ? p.rec : "merge");
  const R = REC[c], K = R.a === 3 ? 4 : 5;
  const per = 1.3;
  const clock = useClock({ period: K * per + 3, rest: K * per + 1 });
  const shown = Math.min(K, Math.floor(clock.t / per) + 1);
  const r = R.a / R.b ** R.d;
  const levels = Array.from({ length: K }, (_, k) => ({ cnt: R.a ** k, size: R.b ** -k, cost: r ** k }));
  const total = levels.reduce((s, l) => s + l.cost, 0);
  const TW = 220, X0 = 14;
  return (
    <Frame clock={clock} title="재귀 나무와 마스터 정리"
      read={<>{R.eq}: 크기 n 인 문제를 크기 n/{R.b} 인 문제 {R.a} 개로 나누고, 나누고 합치는 데 {R.d ? "n" : "1"} 만큼 일한다 · 층 k 의 일 = (문제 수 {R.a}ᵏ) × (한 문제의 일) = 맨 위층의 <b>{fmt(r, 2)}ᵏ 배</b> · {R.why} → <b>{R.ans}</b> · 비율이 1 보다 작으면 뿌리, 같으면 층 수, 크면 잎이 결정한다(마스터 정리)</>}
      controls={<Seg value={c} onChange={(v) => { setC(v); clock.reset(); }} options={[["linear", "n/2 + n"], ["merge", "병합"], ["bsearch", "이진 탐색"], ["kara", "카라추바"]]} />}>
      {levels.slice(0, shown).map((L, k) => {
        const y = 26 + k * 40, n = L.cnt, gap = TW / n, rad = clamp(11 * Math.sqrt(L.size), 2.6, 11);
        return (
          <g key={k}>
            {k > 0 && Array.from({ length: n }, (_, i) => {
              const px = X0 + (Math.floor(i / R.a) + 0.5) * (TW / levels[k - 1].cnt), x = X0 + (i + 0.5) * gap;
              return <line key={"l" + i} x1={px} y1={y - 40} x2={x} y2={y} stroke={C.bd} strokeWidth="1" />;
            })}
            {Array.from({ length: n }, (_, i) => <circle key={i} cx={X0 + (i + 0.5) * gap} cy={y} r={rad} fill={k === shown - 1 ? C.sp : C.blue} opacity={k === shown - 1 ? 0.7 : 0.4} />)}
            {k === 0 && <text x={X0 + TW / 2} y={y + 3.5} textAnchor="middle" fontSize="9" fontWeight="800" fill={C.card}>n</text>}
            <text x="246" y={y - 6} fontSize="9" fill={C.mut}>층 {k}: {n} 개 × 크기 {k ? `n/${R.b ** k}` : "n"}</text>
            <rect x="246" y={y - 2} width={clamp(L.cost * 22, 2, 80)} height="9" rx="2" fill={r < 1 ? C.green : r > 1 ? C.red : C.gold} opacity="0.7" />
            <text x={250 + clamp(L.cost * 22, 2, 80)} y={y + 6} fontSize="9" fill={C.ink}>×{fmt(L.cost, 2)}</text>
          </g>
        );
      })}
      <text x="246" y="216" fontSize="9.5" fontWeight="800" fill={C.ink}>{shown === K ? `${K} 층 합 ×${fmt(total, 2)}` : "…"}</text>
    </Frame>
  );
}

/* ── 힙: 넣을 때는 위로, 꺼낼 때는 아래로 자리를 찾는다 ── */
function heapFrames() {
  const h = [], F = [], out = [];
  const snap = (hi, note) => F.push({ h: h.slice(), hi, note, out: out.slice() });
  for (const x of [5, 12, 8, 3, 15, 10, 20, 7]) {
    h.push(x); let i = h.length - 1;
    snap([i], `넣기 ${x} — 맨 끝 자리에 둔다`);
    while (i > 0) {
      const pa = (i - 1) >> 1;
      if (h[pa] >= h[i]) break;
      [h[pa], h[i]] = [h[i], h[pa]];
      snap([pa, i], `부모 ${h[i]} 보다 크니 맞바꾼다`);
      i = pa;
    }
  }
  for (let r = 0; r < 2; r++) {
    const top = h[0];
    snap([0], `꺼내기 — 맨 위가 최댓값 ${top}`);
    out.push(top);
    h[0] = h[h.length - 1]; h.pop();
    snap([0], `맨 끝 값(${h[0]})을 맨 위로 옮긴다`);
    let i = 0;
    for (;;) {
      const l = 2 * i + 1, rr = l + 1;
      let m = i;
      if (l < h.length && h[l] > h[m]) m = l;
      if (rr < h.length && h[rr] > h[m]) m = rr;
      if (m === i) break;
      [h[m], h[i]] = [h[i], h[m]];
      snap([i, m], `더 큰 자식과 맞바꾼다`);
      i = m;
    }
  }
  snap([], "다시 힙 — 부모 ≥ 자식");
  return F;
}
const HF = heapFrames();
export function Heap() {
  const per = 0.9;
  const clock = useClock({ period: HF.length * per + 2, rest: HF.length * per + 1 });
  const fi = Math.min(HF.length - 1, Math.floor(clock.t / per));
  const f = HF[fi];
  const pos = (i) => { const L = Math.floor(Math.log2(i + 1)), q = i - (2 ** L - 1); return [16 + (q + 0.5) * (300 / 2 ** L), 26 + L * 38]; };
  return (
    <Frame clock={clock} title="힙 — 우선순위 큐"
      read={<>최대 힙: 모든 부모가 자식보다 크거나 같은 완전 이진 나무 · 배열에 차례로 담으면 i 번 칸의 자식은 2i + 1, 2i + 2 번 칸 · <b>{f.note}</b> · 넣기 · 꺼내기 모두 나무의 높이 log₂ n 번 안에 끝나고, 최댓값은 늘 맨 위에 있다(힙 정렬 · 데이크스트라의 우선순위 큐)</>}>
      {f.h.map((_, i) => { if (!i) return null; const [x1, y1] = pos((i - 1) >> 1), [x2, y2] = pos(i); return <line key={"e" + i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={C.bd} strokeWidth="1.5" />; })}
      {f.h.map((v, i) => {
        const [x, y] = pos(i), hot = f.hi.includes(i);
        return (
          <g key={i}>
            <circle cx={x} cy={y} r="13" fill={hot ? "color-mix(in srgb, #b4442e 25%, var(--card))" : C.card} stroke={hot ? C.red : C.ink} strokeWidth={hot ? 2.4 : 1.3} />
            <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{v}</text>
          </g>
        );
      })}
      {f.h.map((v, i) => (
        <g key={"a" + i}>
          <rect x={16 + i * 30} y="172" width="28" height="22" rx="3" fill={f.hi.includes(i) ? "color-mix(in srgb, #b4442e 25%, var(--card))" : C.card} stroke={C.bd} />
          <text x={30 + i * 30} y="187" textAnchor="middle" fontSize="11" fontWeight="700" fill={C.ink}>{v}</text>
          <text x={30 + i * 30} y="205" textAnchor="middle" fontSize="8.5" fill={C.mut}>{i}</text>
        </g>
      ))}
      <text x="270" y="186" fontSize="9.5" fill={C.mut}>꺼낸 값</text>
      <text x="270" y="202" fontSize="11" fontWeight="800" fill={C.red}>{f.out.join(", ") || "—"}</text>
    </Frame>
  );
}

/* ── 너비 우선 · 깊이 우선 탐색 ── */
const GN = [["A", 34, 110], ["B", 104, 48], ["C", 104, 172], ["D", 176, 32], ["E", 176, 110], ["F", 176, 188], ["G", 250, 62], ["H", 250, 158], ["I", 324, 110]];
const GE = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 4], [2, 5], [3, 6], [4, 6], [4, 7], [5, 7], [6, 8], [7, 8]];
const nbr = (u) => GE.filter(([a, b]) => a === u || b === u).map(([a, b]) => (a === u ? b : a)).sort((x, y) => x - y);
function bfsFrames() {
  const F = [], seen = new Set([0]), dist = { 0: 0 }, tree = [], order = [], q = [0];
  F.push({ cur: -1, order: [], front: [0], tree: [], dist: { ...dist } });
  while (q.length) {
    const u = q.shift(); order.push(u);
    for (const v of nbr(u)) if (!seen.has(v)) { seen.add(v); dist[v] = dist[u] + 1; tree.push([u, v]); q.push(v); }
    F.push({ cur: u, order: order.slice(), front: q.slice(), tree: tree.slice(), dist: { ...dist } });
  }
  return F;
}
function dfsFrames() {
  const F = [], seen = new Set(), tree = [], order = [], st = [];
  const visit = (u) => {
    seen.add(u); order.push(u); st.push(u);
    F.push({ cur: u, order: order.slice(), front: st.slice(), tree: tree.slice() });
    for (const v of nbr(u)) if (!seen.has(v)) { tree.push([u, v]); visit(v); F.push({ cur: u, order: order.slice(), front: st.slice(), tree: tree.slice(), back: true }); }
    st.pop();
  };
  visit(0);
  F.push({ cur: -1, order: order.slice(), front: [], tree: tree.slice() });
  return F;
}
const BF = bfsFrames(), DF = dfsFrames();
export function BfsDfs({ p = {} }) {
  const [m, setM] = useState(p.mode === "dfs" ? "dfs" : "bfs");
  const F = m === "bfs" ? BF : DF, per = m === "bfs" ? 1.1 : 0.7;
  const clock = useClock({ period: F.length * per + 2.5, rest: F.length * per + 1 });
  const fi = Math.min(F.length - 1, Math.floor(clock.t / per));
  const f = F[fi];
  const inTree = (a, b) => f.tree.some(([x, y]) => (x === a && y === b) || (x === b && y === a));
  return (
    <Frame clock={clock} title={m === "bfs" ? "너비 우선 탐색" : "깊이 우선 탐색"}
      read={m === "bfs"
        ? <>A 에서 출발해 <b>가까운 점부터</b> — 큐(먼저 들어온 것이 먼저 나감)에 이웃을 넣고 앞에서 꺼낸다 · 방문 순서 {f.order.map((i) => GN[i][0]).join(" → ") || "—"} · 점 옆 숫자 = A 에서의 최소 간선 수 — 가중치 없는 그래프의 최단 경로가 바로 나온다</>
        : <>A 에서 출발해 <b>갈 수 있는 데까지 깊이</b> 들어갔다가 막히면 되돌아온다 — 스택(재귀) · 방문 순서 {f.order.map((i) => GN[i][0]).join(" → ")} · 굵은 선이 탐색 나무 · 미로 찾기 · 위상 정렬 · 회로 찾기에 쓴다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["bfs", "너비 우선(BFS)"], ["dfs", "깊이 우선(DFS)"]]} />}>
      {GE.map(([a, b]) => <line key={a + "-" + b} x1={GN[a][1]} y1={GN[a][2]} x2={GN[b][1]} y2={GN[b][2]} stroke={inTree(a, b) ? C.sp : C.bd} strokeWidth={inTree(a, b) ? 3.2 : 1.5} />)}
      {GN.map(([n, x, y], i) => {
        const k = f.order.indexOf(i), cur = i === f.cur, inF = f.front.includes(i);
        return (
          <g key={n}>
            <circle cx={x} cy={y} r="14" fill={k >= 0 ? "color-mix(in srgb, var(--sp, var(--ac)) 24%, var(--card))" : C.card} stroke={cur ? C.red : inF ? C.gold : C.ink} strokeWidth={cur ? 3 : inF ? 2.4 : 1.3} strokeDasharray={inF && k < 0 ? "4 2" : undefined} />
            <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{n}</text>
            {k >= 0 && <Label x={x + 12} y={y - 12} size={9} bold color={C.sp} bg>{k + 1}</Label>}
            {m === "bfs" && f.dist[i] != null && <text x={x} y={y + 27} textAnchor="middle" fontSize="9" fill={C.green}>거리 {f.dist[i]}</text>}
          </g>
        );
      })}
      <text x="10" y="212" fontSize="9.5" fontWeight="800" fill={C.gold}>{m === "bfs" ? "큐" : "스택"}: {f.front.map((i) => GN[i][0]).join(" ") || "비었음"}</text>
    </Frame>
  );
}

/* ── 최소 신장 나무: 크루스칼(가벼운 변부터, 회로가 생기면 버림) · 프림(나무에서 나가는 가장 가벼운 변) ── */
const MN = [["A", 40, 40], ["B", 160, 30], ["C", 300, 42], ["D", 58, 140], ["E", 200, 112], ["F", 112, 198], ["G", 292, 190]];
const ME = [[0, 1, 7], [0, 3, 5], [1, 2, 8], [1, 3, 9], [1, 4, 7], [2, 4, 5], [3, 4, 15], [3, 5, 6], [4, 5, 8], [4, 6, 9], [5, 6, 11]];
function kruskalFrames() {
  const par = MN.map((_, i) => i), find = (x) => (par[x] === x ? x : (par[x] = find(par[x])));
  const order = ME.map((e, i) => i).sort((a, b) => ME[a][2] - ME[b][2]);
  const F = [{ cur: -1, ok: [], bad: [], comp: MN.map((_, i) => i) }], ok = [], bad = [];
  for (const ei of order) {
    const [a, b] = ME[ei], ra = find(a), rb = find(b);
    if (ra !== rb) { par[ra] = rb; ok.push(ei); } else bad.push(ei);
    F.push({ cur: ei, ok: ok.slice(), bad: bad.slice(), comp: MN.map((_, i) => find(i)), acc: ra !== rb });
  }
  return F;
}
function primFrames() {
  const inT = new Set([0]), ok = [], F = [{ cur: -1, ok: [], bad: [], tree: [0] }];
  while (inT.size < MN.length) {
    let best = -1;
    ME.forEach(([a, b, w], i) => { if (inT.has(a) !== inT.has(b) && (best < 0 || w < ME[best][2])) best = i; });
    const [a, b] = ME[best];
    inT.add(a); inT.add(b); ok.push(best);
    F.push({ cur: best, ok: ok.slice(), bad: [], tree: [...inT], acc: true });
  }
  return F;
}
const KF = kruskalFrames(), PF = primFrames();
export function MST({ p = {} }) {
  const [m, setM] = useState(p.mode === "prim" ? "prim" : "kruskal");
  const F = m === "kruskal" ? KF : PF, per = 1.0;
  const clock = useClock({ period: F.length * per + 2.5, rest: F.length * per + 1 });
  const fi = Math.min(F.length - 1, Math.floor(clock.t / per));
  const f = F[fi];
  const wsum = f.ok.reduce((s, i) => s + ME[i][2], 0);
  const pal = [C.blue, C.gold, C.teal, C.violet, C.green, C.red, C.mut];
  const inTree = (i) => (m === "prim" ? f.tree.includes(i) : true);
  return (
    <Frame clock={clock} title="최소 신장 나무"
      read={m === "kruskal"
        ? <>크루스칼: 변을 가벼운 것부터 보며 두 끝이 이미 이어져 있으면(같은 색 무리) 회로가 생기니 버리고(빨간 점선), 아니면 고른다(초록) · 점의 색 = 지금 이어진 무리 · 고른 무게 합 <b>{wsum}</b>{fi === F.length - 1 ? " — 최소 신장 나무(변 6 개)" : ""}</>
        : <>프림: A 에서 시작해, 지금 나무(색칠한 점)에서 <b>밖으로 나가는 변 가운데 가장 가벼운 것</b>을 하나씩 더한다 · 고른 무게 합 <b>{wsum}</b>{fi === F.length - 1 ? " — 크루스칼과 같은 나무, 같은 합" : ""} · 두 방법 모두 탐욕인데도 최적이다(자르기 성질)</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["kruskal", "크루스칼"], ["prim", "프림"]]} />}>
      {ME.map(([a, b, w], i) => {
        const ok = f.ok.includes(i), bad = f.bad.includes(i), cur = i === f.cur;
        const cand = m === "prim" && f.tree.includes(a) !== f.tree.includes(b);
        return (
          <g key={i}>
            <line x1={MN[a][1]} y1={MN[a][2]} x2={MN[b][1]} y2={MN[b][2]} stroke={ok ? C.green : bad ? C.red : cand ? C.gold : C.bd} strokeWidth={ok ? 4 : cur ? 3 : 1.6} strokeDasharray={bad ? "5 4" : undefined} opacity={bad ? 0.7 : 1} />
            <Label x={(MN[a][1] + MN[b][1]) / 2} y={(MN[a][2] + MN[b][2]) / 2 + 4} size={9.5} bold anchor="middle" color={cur ? C.red : ok ? C.green : C.mut} bg>{w}</Label>
          </g>
        );
      })}
      {MN.map(([n, x, y], i) => (
        <g key={n}>
          <circle cx={x} cy={y} r="13" fill={m === "kruskal" ? pal[f.comp[i]] : inTree(i) ? C.sp : C.card} opacity={m === "kruskal" ? 0.35 : inTree(i) ? 0.35 : 1} stroke={C.ink} strokeWidth="1.3" />
          <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{n}</text>
        </g>
      ))}
      <text x="350" y="214" textAnchor="end" fontSize="10" fontWeight="800" fill={C.ink}>무게 합 {wsum}</text>
    </Frame>
  );
}

/* ── 동적계획법: 편집 거리 표를 한 칸씩 채운다 ── */
const PAIRS = { kitten: ["KITTEN", "SITTING"], sunday: ["SUNDAY", "SATURDAY"], intent: ["INTENTION", "EXECUTION"] };
export function DPTable({ p = {} }) {
  const [w, setW] = useState(PAIRS[p.pair] ? p.pair : "kitten");
  const [A, B] = PAIRS[w], m = A.length, n = B.length;
  const D = useMemo(() => {
    const d = Array.from({ length: m + 1 }, (_, i) => Array.from({ length: n + 1 }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)));
    for (let i = 1; i <= m; i++) for (let j = 1; j <= n; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (A[i - 1] === B[j - 1] ? 0 : 1));
    return d;
  }, [A, B, m, n]);
  const path = useMemo(() => {
    const out = []; let i = m, j = n;
    while (i > 0 || j > 0) {
      out.push([i, j]);
      if (i > 0 && j > 0 && D[i][j] === D[i - 1][j - 1] + (A[i - 1] === B[j - 1] ? 0 : 1)) { i--; j--; }
      else if (i > 0 && D[i][j] === D[i - 1][j] + 1) i--;
      else j--;
    }
    out.push([0, 0]);
    return out;
  }, [D, A, B, m, n]);
  const total = m * n, fillT = 8;
  const clock = useClock({ period: fillT + 4, rest: fillT + 2 });
  const filled = Math.min(total, Math.floor((clock.t / fillT) * total) + 1);
  const done = filled >= total && clock.t >= fillT;
  const ci = Math.floor((filled - 1) / n) + 1, cj = ((filled - 1) % n) + 1;
  const cw = Math.min(30, 300 / (n + 2)), ch = Math.min(19, 176 / (m + 2)), X0 = 30, Y0 = 16;
  const shown = (i, j) => i === 0 || j === 0 || (i - 1) * n + j <= filled;
  const onPath = (i, j) => done && path.some(([a, b]) => a === i && b === j);
  const nb = (i, j) => !done && ((i === ci - 1 && (j === cj || j === cj - 1)) || (i === ci && j === cj - 1));
  return (
    <Frame clock={clock} title="동적계획법 — 편집 거리"
      read={<>{A} → {B}: 글자를 넣기 · 지우기 · 바꾸기 몇 번이면 되나 · 칸 (i, j) = 앞 i 글자를 앞 j 글자로 바꾸는 최소 횟수 = min(위 + 1 지우기, 왼쪽 + 1 넣기, 대각선 + 글자가 다르면 1) · 작은 문제의 답을 표에 적어 두고 다시 쓴다 — 칸 {(m + 1) * (n + 1)} 개를 한 번씩, O(mn) · 편집 거리 <b>{done ? D[m][n] : "…"}</b>{done ? " (빨간 칸 = 되짚은 길)" : ""}</>}
      controls={<Seg value={w} onChange={(v) => { setW(v); clock.reset(); }} options={[["kitten", "KITTEN"], ["sunday", "SUNDAY"], ["intent", "INTENTION"]]} />}>
      {[" ", ...B].map((ch2, j) => <text key={"h" + j} x={X0 + (j + 1) * cw + cw / 2} y={Y0 + ch * 0.75} textAnchor="middle" fontSize="10" fontWeight="800" fill={C.blue}>{ch2.trim() ? ch2 : "ε"}</text>)}
      {[" ", ...A].map((ch2, i) => <text key={"r" + i} x={X0 + cw / 2} y={Y0 + (i + 1) * ch + ch * 0.72} textAnchor="middle" fontSize="10" fontWeight="800" fill={C.gold}>{ch2.trim() ? ch2 : "ε"}</text>)}
      {D.map((row, i) => row.map((v, j) => {
        const x = X0 + (j + 1) * cw, y = Y0 + (i + 1) * ch, cur = !done && i === ci && j === cj;
        const fill = onPath(i, j) ? "color-mix(in srgb, #b4442e 30%, var(--card))" : cur ? "color-mix(in srgb, var(--sp, var(--ac)) 30%, var(--card))" : nb(i, j) ? "color-mix(in srgb, #b07d12 25%, var(--card))" : C.card;
        return (
          <g key={i + "-" + j}>
            <rect x={x} y={y} width={cw - 1} height={ch - 1} fill={fill} stroke={C.bd} strokeWidth="0.6" />
            {shown(i, j) && <text x={x + cw / 2} y={y + ch * 0.72} textAnchor="middle" fontSize="9.5" fontWeight={cur || onPath(i, j) ? 800 : 500} fill={C.ink}>{v}</text>}
          </g>
        );
      }))}
    </Frame>
  );
}

/* ── 외판원 문제: 모든 도시를 한 번씩 돌아오는 가장 짧은 길 ── */
const TP = [[40, 60], [96, 178], [150, 36], [205, 130], [262, 196], [300, 52], [334, 140], [118, 104]];
const dist = (a, b) => Math.hypot(TP[a][0] - TP[b][0], TP[a][1] - TP[b][1]);
const tourLen = (t) => t.reduce((s, c, i) => s + dist(c, t[(i + 1) % t.length]), 0);
function tspData() {
  const n = TP.length, nn = [0], used = new Set([0]);
  while (nn.length < n) { const u = nn[nn.length - 1]; let best = -1; for (let v = 0; v < n; v++) if (!used.has(v) && (best < 0 || dist(u, v) < dist(u, best))) best = v; nn.push(best); used.add(best); }
  const opt2 = [nn.slice()]; let t = nn.slice(), improved = true;
  while (improved) {
    improved = false;
    for (let i = 1; i < n - 1 && !improved; i++) for (let k = i + 1; k < n && !improved; k++) {
      const c = t.slice(0, i).concat(t.slice(i, k + 1).reverse(), t.slice(k + 1));
      if (tourLen(c) < tourLen(t) - 1e-9) { t = c; opt2.push(t.slice()); improved = true; }
    }
  }
  let best = null, bl = Infinity;
  const perm = (arr, l) => {
    if (l === arr.length) { if (arr[1] < arr[arr.length - 1]) { const tt = [0, ...arr.slice(1)], L = tourLen(tt); if (L < bl) { bl = L; best = tt; } } return; }
    for (let i = l; i < arr.length; i++) { [arr[l], arr[i]] = [arr[i], arr[l]]; perm(arr, l + 1); [arr[l], arr[i]] = [arr[i], arr[l]]; }
  };
  perm(Array.from({ length: n }, (_, i) => i), 1);
  return { nn, opt2, best };
}
export function TSP({ p = {} }) {
  const [m, setM] = useState(["nn", "opt2", "best"].includes(p.mode) ? p.mode : "nn");
  const T = useMemo(tspData, []);
  const clock = useClock({ period: 11, rest: 10 });
  let tour, open = false, note;
  if (m === "nn") { const k = Math.min(TP.length, Math.floor(clock.t / 1.1) + 2); tour = T.nn.slice(0, k); open = k < TP.length; note = "가까운 이웃: 지금 도시에서 아직 안 간 가장 가까운 도시로 — 빠르지만 마지막에 먼 길을 되돌아오기 쉽다"; }
  else if (m === "opt2") { const k = Math.min(T.opt2.length - 1, Math.floor(clock.t / 1.6)); tour = T.opt2[k]; note = `2-opt: 서로 엇갈린 두 변을 풀어(구간 뒤집기) 길이가 줄면 바꾼다 — ${k} 번째 개선`; }
  else { tour = T.best; note = "전수 조사: 가능한 순회 (8 − 1)!/2 = 2520 개를 모두 재어 찾은 최적"; }
  const len = tourLen(tour) - (open ? dist(tour[tour.length - 1], tour[0]) : 0);
  return (
    <Frame clock={clock} title="외판원 문제"
      read={<>{note} · 지금 길이 <b>{fmt(len, 0)}</b> · 가까운 이웃 {fmt(tourLen(T.nn), 0)} → 2-opt {fmt(tourLen(T.opt2[T.opt2.length - 1]), 0)} → 최적 {fmt(tourLen(T.best), 0)} · 도시가 20 개면 순회가 약 6 × 10¹⁶ 가지 — 빠른 정확한 방법이 알려지지 않은 NP-어려운 문제라 실무에서는 근사 · 개선 방법을 쓴다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["nn", "가까운 이웃"], ["opt2", "2-opt 개선"], ["best", "최적(전수)"]]} />}>
      <path d={tour.map((c, i) => (i ? "L" : "M") + TP[c][0] + " " + TP[c][1]).join("") + (open ? "" : "Z")} fill="none" stroke={m === "best" ? C.green : C.sp} strokeWidth="2.4" strokeLinejoin="round" />
      {TP.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r={i === 0 ? 8 : 6.5} fill={i === 0 ? C.red : C.card} stroke={C.ink} strokeWidth="1.4" />
          <text x={x} y={y - 11} textAnchor="middle" fontSize="9" fill={C.mut}>{i === 0 ? "출발" : i}</text>
        </g>
      ))}
    </Frame>
  );
}
