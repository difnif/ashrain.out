// 이산수학 그림 — 진리표(동치 확인) · 포함배제(벤 다이어그램) · 트로미노 귀납 · 파스칼 삼각형(값 · 나머지 무늬) · 하노이 탑 · 오일러 경로 · 유클리드 호제법(정사각형 떼기) · 유한 오토마타(3 의 배수)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, Label, clamp, ease, lerp, sup, useClock } from "./kit.jsx";

/** 곡선 끝 화살촉 — 끝점과 그 직전 방향(제어점)으로 */
function head(x2, y2, cx, cy, size = 7) {
  const a = Math.atan2(y2 - cy, x2 - cx), s = size;
  const bx = x2 - s * Math.cos(a), by = y2 - s * Math.sin(a);
  return `${x2},${y2} ${bx - s * 0.45 * Math.sin(a)},${by + s * 0.45 * Math.cos(a)} ${bx + s * 0.45 * Math.sin(a)},${by - s * 0.45 * Math.cos(a)}`;
}
const quad = (a, c, b, u) => (1 - u) * (1 - u) * a + 2 * (1 - u) * u * c + u * u * b;
const cubic = (a, c1, c2, b, u) => (1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * c1 + 3 * (1 - u) * u * u * c2 + u ** 3 * b;

/* ── 진리표: 두 명제가 모든 경우에 같은 값이면 동치 ── */
const PAIRS = {
  contra: ["p → q", "¬q → ¬p", (p, q) => !p || q, (p, q) => q || !p],
  conv: ["p → q", "q → p", (p, q) => !p || q, (p, q) => !q || p],
  demorgan: ["¬(p ∧ q)", "¬p ∨ ¬q", (p, q) => !(p && q), (p, q) => !p || !q],
  impl: ["p → q", "¬p ∨ q", (p, q) => !p || q, (p, q) => !p || q],
};
const PAIR_NOTE = {
  contra: "대우는 원래 명제와 늘 같은 값 — 「비가 오면 땅이 젖는다」와 「땅이 젖지 않았으면 비가 오지 않았다」",
  conv: "역은 원래 명제와 다를 수 있다 — p 거짓 · q 참인 줄(빨강)에서 갈린다",
  demorgan: "「둘 다 참은 아니다」 = 「적어도 하나는 거짓」 — 부정이 ∧ 를 ∨ 로 바꾼다",
  impl: "조건문 p → q 는 「p 가 거짓이거나 q 가 참」 — p 가 거짓이면 q 와 상관없이 참이다",
};
export function Truth({ p = {} }) {
  const [pair, setPair] = useState(PAIRS[p.pair] ? p.pair : "contra");
  const clock = useClock({ period: 8, rest: 7 });
  const [na, nb, fa, fb] = PAIRS[pair];
  const rows = [[true, true], [true, false], [false, true], [false, false]];
  const shown = Math.min(4, Math.floor(clock.t / 1.3) + 1);
  const diff = rows.map(([a, b]) => fa(a, b) !== fb(a, b));
  const done = shown === 4, same = !diff.some(Boolean);
  const X = [42, 86, 152, 222], Y0 = 52, RH = 34;
  const cell = (v) => (v ? "참" : "거짓");
  return (
    <Frame clock={clock} title="진리표로 동치 확인"
      read={<>{na} 와 {nb} 를 p, q 의 네 경우(참 · 거짓 조합)마다 계산한다 · {done ? (same ? <><b>네 줄이 모두 같다 → 동치</b>(≡)</> : <><b>다른 줄이 있다 → 동치가 아니다</b></>) : `${shown} 번째 줄까지`} · {PAIR_NOTE[pair]}</>}
      controls={<Seg value={pair} onChange={(v) => { setPair(v); clock.reset(); }} options={[["contra", "대우"], ["conv", "역"], ["demorgan", "드모르간"], ["impl", "조건문"]]} />}>
      {["p", "q", na, nb].map((h, i) => <text key={i} x={X[i]} y={Y0 - 14} textAnchor="middle" fontSize="12" fontWeight="800" fill={i < 2 ? C.mut : i === 2 ? C.blue : C.gold}>{h}</text>)}
      <line x1="16" x2="258" y1={Y0 - 6} y2={Y0 - 6} stroke={C.ink} strokeWidth="1.2" />
      <line x1="108" x2="108" y1={Y0 - 28} y2={Y0 + RH * 4 - 6} stroke={C.bd} strokeWidth="1.2" />
      {rows.map(([a, b], i) => {
        const y = Y0 + i * RH, vis = i < shown, cur = i === shown - 1 && !done;
        return (
          <g key={i} opacity={vis ? 1 : 0.28}>
            {cur && <rect x="16" y={y - 4} width="242" height={RH - 4} rx="5" fill={C.sp} opacity="0.12" />}
            {vis && diff[i] && <rect x="16" y={y - 4} width="242" height={RH - 4} rx="5" fill="none" stroke={C.red} strokeWidth="1.8" />}
            <text x={X[0]} y={y + 17} textAnchor="middle" fontSize="12" fill={C.ink}>{cell(a)}</text>
            <text x={X[1]} y={y + 17} textAnchor="middle" fontSize="12" fill={C.ink}>{cell(b)}</text>
            {vis && <text x={X[2]} y={y + 17} textAnchor="middle" fontSize="12.5" fontWeight="800" fill={fa(a, b) ? C.green : C.red}>{cell(fa(a, b))}</text>}
            {vis && <text x={X[3]} y={y + 17} textAnchor="middle" fontSize="12.5" fontWeight="800" fill={fb(a, b) ? C.green : C.red}>{cell(fb(a, b))}</text>}
          </g>
        );
      })}
      <rect x="270" y="58" width="80" height="96" rx="9" fill={done ? (same ? C.green : C.red) : C.card} opacity={done ? 0.14 : 1} stroke={done ? (same ? C.green : C.red) : C.bd} strokeWidth="1.5" />
      <text x="310" y="94" textAnchor="middle" fontSize="20" fontWeight="800" fill={done ? (same ? C.green : C.red) : C.mut}>{done ? (same ? "≡" : "≢") : "…"}</text>
      <text x="310" y="118" textAnchor="middle" fontSize="11" fontWeight="800" fill={done ? (same ? C.green : C.red) : C.mut}>{done ? (same ? "동치" : "동치 아님") : "확인 중"}</text>
      <text x="310" y="136" textAnchor="middle" fontSize="9.5" fill={C.mut}>{done ? `같은 줄 ${4 - diff.filter(Boolean).length} / 4` : `${shown} / 4 줄`}</text>
    </Frame>
  );
}

/* ── 포함배제: 1 ~ 100 에서 세 수 중 어느 하나의 배수인 수 — 한 번씩만 세도록 더하고 빼고 더한다 ── */
const gcd = (a, b) => (b ? gcd(b, a % b) : a);
const lcm = (a, b) => (a / gcd(a, b)) * b;
const VENN_SETS = { s235: [2, 3, 5], s237: [2, 3, 7], s4610: [4, 6, 10] };
export function Venn({ p = {} }) {
  const [set, setSet] = useState(VENN_SETS[p.set] ? p.set : "s235");
  const clock = useClock({ period: 10, rest: 9 });
  const [a, b, c] = VENN_SETS[set], N = 100;
  const reg = useMemo(() => {
    const r = Array(8).fill(0);
    for (let n = 1; n <= N; n++) r[(n % a === 0 ? 1 : 0) + (n % b === 0 ? 2 : 0) + (n % c === 0 ? 4 : 0)]++;
    return r;
  }, [a, b, c]);
  const cnt = (m) => reg.reduce((s, v, i) => ((i & m) === m ? s + v : s), 0);
  const nA = cnt(1), nB = cnt(2), nC = cnt(4), nAB = cnt(3), nAC = cnt(5), nBC = cnt(6), nABC = cnt(7);
  const S1 = nA + nB + nC, S2 = S1 - nAB - nAC - nBC, S3 = S2 + nABC;
  const phase = clock.t < 3 ? 1 : clock.t < 6 ? 2 : 3;
  const bits = (i) => (i & 1) + ((i >> 1) & 1) + ((i >> 2) & 1);
  const mult = (i) => { const k = bits(i); return phase === 1 ? k : phase === 2 ? k - (k * (k - 1)) / 2 : k - (k * (k - 1)) / 2 + (k === 3 ? 1 : 0); };
  const POS = { 1: [98, 76], 2: [202, 76], 4: [150, 172], 3: [150, 66], 5: [121, 130], 6: [179, 130], 7: [150, 108] };
  const tone = (m) => (m === 1 ? C.green : m === 0 ? C.red : C.gold);
  return (
    <Frame clock={clock} title="포함배제의 원리"
      read={<>1 ~ {N} 에서 A = {a} 의 배수, B = {b} 의 배수, C = {c} 의 배수 · |A| + |B| + |C| = {nA} + {nB} + {nC} = {S1} − (|A∩B| + |A∩C| + |B∩C|) = − ({nAB} + {nAC} + {nBC}) + |A∩B∩C| = + {nABC} → <b>|A∪B∪C| = {S3}</b> · 셋 중 어느 것의 배수도 아닌 수 <b>{N - S3}</b> 개 · 겹친 칸이 몇 번 세어졌는지(×) 보자 — 마지막엔 모두 한 번</>}
      controls={<Seg value={set} onChange={(v) => { setSet(v); clock.reset(); }} options={[["s235", "2 · 3 · 5"], ["s237", "2 · 3 · 7"], ["s4610", "4 · 6 · 10"]]} />}>
      {[[120, 90, C.blue, "A"], [180, 90, C.gold, "B"], [150, 142, C.violet, "C"]].map(([x, y, col, n]) => (
        <g key={n}>
          <circle cx={x} cy={y} r="52" fill={col} opacity="0.08" stroke={col} strokeWidth="1.8" />
          <text x={n === "A" ? x - 46 : n === "B" ? x + 46 : x + 44} y={n === "C" ? y + 44 : y - 40} textAnchor="middle" fontSize="12" fontWeight="800" fill={col}>{n}</text>
        </g>
      ))}
      {[1, 2, 4, 3, 5, 6, 7].map((i) => {
        const [x, y] = POS[i], m = mult(i);
        return (
          <g key={i}>
            <text x={x} y={y} textAnchor="middle" fontSize="11.5" fontWeight="800" fill={C.ink}>{reg[i]}</text>
            <text x={x} y={y + 11} textAnchor="middle" fontSize="9" fontWeight="800" fill={tone(m)}>×{m}</text>
          </g>
        );
      })}
      <text x="150" y="212" textAnchor="middle" fontSize="9.5" fill={C.mut}>바깥(어느 것의 배수도 아님) {reg[0]}</text>
      <g fontSize="10.5">
        <text x="258" y="44" fontWeight="800" fill={C.ink}>세는 중</text>
        <text x="258" y="70" fill={phase >= 1 ? C.ink : C.mut} fontWeight={phase === 1 ? 800 : 500}>① 하나씩 + {S1}</text>
        <text x="258" y="94" fill={phase >= 2 ? C.ink : C.mut} opacity={phase >= 2 ? 1 : 0.4} fontWeight={phase === 2 ? 800 : 500}>② 둘씩 − {nAB + nAC + nBC}</text>
        <text x="258" y="118" fill={phase >= 3 ? C.ink : C.mut} opacity={phase >= 3 ? 1 : 0.4} fontWeight={phase === 3 ? 800 : 500}>③ 셋 + {nABC}</text>
        <text x="258" y="148" fontSize="12" fontWeight="800" fill={phase === 3 ? C.green : C.mut}>= {phase === 1 ? S1 : phase === 2 ? S2 : S3}</text>
        <text x="258" y="168" fontSize="9" fill={C.mut}>{phase === 3 ? "모든 칸이 ×1" : "아직 겹친 칸이 틀림"}</text>
      </g>
    </Frame>
  );
}

/* ── 트로미노 귀납: 2ⁿ × 2ⁿ 판에서 한 칸을 빼면 ㄱ자 조각으로 늘 덮인다 ── */
function trominoes(n, hx, hy) {
  const out = [];
  const rec = (x0, y0, s, hx0, hy0, d) => {
    if (s === 1) return;
    const h = s / 2, cx = x0 + h, cy = y0 + h;
    const quads = [[x0, y0], [cx, y0], [x0, cy], [cx, cy]];
    const mid = [[cx - 1, cy - 1], [cx, cy - 1], [cx - 1, cy], [cx, cy]];
    const qi = (hx0 >= cx ? 1 : 0) + (hy0 >= cy ? 2 : 0);
    out.push({ cells: mid.filter((_, i) => i !== qi), d, box: [x0, y0, s] });
    quads.forEach(([qx, qy], i) => rec(qx, qy, h, i === qi ? hx0 : mid[i][0], i === qi ? hy0 : mid[i][1], d + 1));
  };
  rec(0, 0, 1 << n, hx, hy, 0);
  return out.map((x, i) => ({ ...x, i })).sort((u, v) => u.d - v.d || u.i - v.i);
}
export function Tromino({ p = {} }) {
  const [n, setN] = useState(clamp(p.n ?? 3, 1, 3));
  const [hole, setHole] = useState(p.hole ?? 19);
  const size = 1 << n, hpos = hole % (size * size), hx = hpos % size, hy = Math.floor(hpos / size);
  const T = useMemo(() => trominoes(n, hx, hy), [n, hx, hy]);
  const per = n === 3 ? 0.34 : 0.8;
  const clock = useClock({ period: T.length * per + 2.5, rest: T.length * per + 1 });
  const shown = Math.min(T.length, Math.floor(clock.t / per) + 1);
  const curD = T[Math.max(0, shown - 1)].d;
  const cs = 176 / size, X0 = 16, Y0 = 20;
  const owner = {};
  T.slice(0, shown).forEach((tr, k) => tr.cells.forEach(([x, y]) => { owner[x + "," + y] = k; }));
  const col = [C.red, C.gold, C.blue];
  const edges = [];
  T.slice(0, shown).forEach((tr, k) => tr.cells.forEach(([x, y]) => {
    [[0, -1, x, y, x + 1, y], [0, 1, x, y + 1, x + 1, y + 1], [-1, 0, x, y, x, y + 1], [1, 0, x + 1, y, x + 1, y + 1]].forEach(([dx, dy, a1, b1, a2, b2]) => {
      if (owner[(x + dx) + "," + (y + dy)] !== k) edges.push([a1, b1, a2, b2]);
    });
  }));
  const cur = T[Math.max(0, shown - 1)].box;
  return (
    <Frame clock={clock} title="트로미노 덮기 — 수학적 귀납법"
      read={<>{size} × {size} 판에서 한 칸(검정)을 빼면 ㄱ자 조각 <b>{(size * size - 1) / 3}</b> 개로 덮인다 · 귀납: 판을 넷으로 나눠 가운데에 조각 하나를 놓으면, 네 조각 판이 모두 「구멍 하나짜리 작은 판」이 된다 — 작은 판이 되면 큰 판도 된다 · {shown === T.length ? <b>다 덮었다</b> : <>지금 {curD + 1} 단계({1 << (n - curD)} × {1 << (n - curD)} 판을 나누는 중)</>} · 4ⁿ − 1 은 늘 3 의 배수</>}
      controls={<>
        <Seg value={n} onChange={(v) => { setN(v); clock.reset(); }} options={[[1, "2 × 2"], [2, "4 × 4"], [3, "8 × 8"]]} />
        <Slider label="빼는 칸" min={0} max={size * size - 1} step={1} value={hpos} onChange={(v) => { setHole(v); clock.reset(); }} show={() => `(${hx + 1}, ${hy + 1})`} />
      </>}>
      {Array.from({ length: size * size }, (_, k) => {
        const x = k % size, y = Math.floor(k / size), o = owner[x + "," + y];
        const isHole = x === hx && y === hy;
        return <rect key={k} x={X0 + x * cs} y={Y0 + y * cs} width={cs} height={cs} fill={isHole ? C.ink : o != null ? col[T[o].d % 3] : C.card} opacity={isHole ? 0.9 : o != null ? 0.5 : 1} stroke={C.bd} strokeWidth="0.6" />;
      })}
      {edges.map(([a1, b1, a2, b2], k) => <line key={k} x1={X0 + a1 * cs} y1={Y0 + b1 * cs} x2={X0 + a2 * cs} y2={Y0 + b2 * cs} stroke={C.ink} strokeWidth="1.8" strokeLinecap="round" />)}
      {shown < T.length && <rect x={X0 + cur[0] * cs} y={Y0 + cur[1] * cs} width={cur[2] * cs} height={cur[2] * cs} fill="none" stroke={C.sp} strokeWidth="2.2" strokeDasharray="5 3" />}
      {shown < T.length && cur[2] > 1 && <>
        <line x1={X0 + (cur[0] + cur[2] / 2) * cs} x2={X0 + (cur[0] + cur[2] / 2) * cs} y1={Y0 + cur[1] * cs} y2={Y0 + (cur[1] + cur[2]) * cs} stroke={C.sp} strokeWidth="1.2" strokeDasharray="3 3" />
        <line y1={Y0 + (cur[1] + cur[2] / 2) * cs} y2={Y0 + (cur[1] + cur[2] / 2) * cs} x1={X0 + cur[0] * cs} x2={X0 + (cur[0] + cur[2]) * cs} stroke={C.sp} strokeWidth="1.2" strokeDasharray="3 3" />
      </>}
      <g fontSize="10.5" fill={C.ink}>
        <text x="206" y="36" fontWeight="800">조각 {shown} / {T.length}</text>
        {Array.from({ length: n }, (_, d) => (
          <g key={d}>
            <rect x="206" y={52 + d * 26} width="12" height="12" fill={col[d % 3]} opacity="0.5" stroke={C.ink} strokeWidth="1" />
            <text x="224" y={62 + d * 26} fontSize="10" fill={d === curD ? C.ink : C.mut} fontWeight={d === curD ? 800 : 500}>{d + 1} 단계: 조각 {4 ** d} 개</text>
          </g>
        ))}
        <text x="206" y={70 + n * 26} fontSize="9.5" fill={C.mut}>칸 수 4ⁿ − 1 = {size * size - 1}</text>
        <text x="206" y={86 + n * 26} fontSize="9.5" fill={C.mut}>= 3 × {(size * size - 1) / 3}</text>
      </g>
    </Frame>
  );
}

/* ── 파스칼 삼각형: 위의 두 수를 더한다 — 나머지로 칠하면 프랙털 ── */
export function Pascal({ p = {} }) {
  const [mode, setMode] = useState(["val", "m2", "m3"].includes(p.mode) ? p.mode : "val");
  const [row, setRow] = useState(clamp(p.row ?? 5, 0, 9));
  const clock = useClock({ period: 11, rest: 10.5 });
  const R = mode === "val" ? 10 : 32, m = mode === "m3" ? 3 : 2;
  const tri = useMemo(() => {
    const t = [[1]];
    for (let r = 1; r < R; r++) { const prev = t[r - 1], cur = [1]; for (let k = 1; k < r; k++) cur.push(mode === "val" ? prev[k - 1] + prev[k] : (prev[k - 1] + prev[k]) % m); cur.push(1); t.push(cur); }
    return t;
  }, [R, mode, m]);
  if (mode === "val") {
    const total = (R * (R + 1)) / 2, shownN = Math.min(total, 6 + Math.floor(clock.t / 0.15));
    let idx = 0, last = [0, 0];
    const cells = [];
    tri.forEach((rr, r) => rr.forEach((v, k) => { if (idx < shownN) { cells.push([r, k, v]); last = [r, k]; } idx++; }));
    const pos = (r, k) => [180 + (k - r / 2) * 34, 22 + r * 19.5];
    const isPar = (r, k) => last[0] > 0 && r === last[0] - 1 && (k === last[1] - 1 || k === last[1]);
    const sum = 2 ** row;
    return (
      <Frame clock={clock} title="파스칼 삼각형"
        read={<>칸마다 바로 위 두 수의 합 — C(n, k) = C(n − 1, k − 1) + C(n − 1, k) · n 번째 줄(파랑) {tri[row].join(", ")} 의 합 = <b>2{sup(row)} = {sum}</b>(부분집합의 수) · 좌우가 같다 C(n, k) = C(n, n − k) · 칸의 값은 꼭대기에서 그 칸까지 내려가는 길의 수</>}
        controls={<>
          <Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["val", "값"], ["m2", "짝홀(÷2 나머지)"], ["m3", "÷3 나머지"]]} />
          <Slider label="줄 n" min={0} max={9} step={1} value={row} onChange={setRow} />
        </>}>
        {cells.map(([r, k, v]) => {
          const [x, y] = pos(r, k), isLast = r === last[0] && k === last[1] && shownN < total;
          return (
            <g key={r + "-" + k}>
              <rect x={x - 15} y={y - 8} width="30" height="16" rx="4" fill={isLast ? C.red : isPar(r, k) && shownN < total ? C.gold : r === row ? C.blue : C.card} opacity={isLast || (isPar(r, k) && shownN < total) || r === row ? 0.3 : 1} stroke={r === row ? C.blue : C.bd} strokeWidth="1" />
              <text x={x} y={y + 3.5} textAnchor="middle" fontSize={v >= 100 ? 9 : 10} fontWeight="700" fill={C.ink}>{v}</text>
            </g>
          );
        })}
        {row <= 6 && shownN >= ((row + 1) * (row + 2)) / 2 && <Label x={180 + (row / 2) * 34 + 22} y={22 + row * 19.5 + 4} size={9.5} color={C.blue} bold bg>합 {sum}</Label>}
      </Frame>
    );
  }
  const shownR = Math.min(R, 4 + Math.floor(clock.t / 0.28));
  return (
    <Frame clock={clock} title="파스칼 삼각형의 나머지 무늬"
      read={<>{R} 줄까지의 C(n, k) 를 {m} 로 나눈 나머지 — 0 이 아닌 칸만 칠했다 · {m === 2 ? "짝홀로 칠하면 시에르핀스키 삼각형이 나타난다(2ᵏ 줄마다 같은 모양이 세 개로 되풀이)" : "÷3 나머지(1 은 파랑, 2 는 빨강)는 3ᵏ 줄마다 같은 모양이 여섯 개로 되풀이"} · 값을 다 계산하지 않고도 위 두 칸의 나머지끼리 더해 나머지를 구한다(합동식)</>}
      controls={<Seg value={mode} onChange={(v) => { setMode(v); clock.reset(); }} options={[["val", "값"], ["m2", "짝홀(÷2 나머지)"], ["m3", "÷3 나머지"]]} />}>
      {tri.slice(0, shownR).map((rr, r) => rr.map((v, k) => (
        <circle key={r + "-" + k} cx={180 + (k - r / 2) * 10.6} cy={14 + r * 6.2} r={v ? 2.9 : 1.1} fill={v === 0 ? C.bd : v === 1 ? C.blue : C.red} />
      )))}
    </Frame>
  );
}

/* ── 하노이 탑: n 개를 옮기려면 n − 1 개를 두 번 — 2ⁿ − 1 번 ── */
function hanoiMoves(n) {
  const out = [];
  const rec = (k, a, b, c) => { if (!k) return; rec(k - 1, a, c, b); out.push([k, a, c]); rec(k - 1, b, a, c); };
  rec(n, 0, 1, 2);
  return out;
}
export function Hanoi({ p = {} }) {
  const [n, setN] = useState(clamp(p.n ?? 4, 2, 6));
  const mv = useMemo(() => hanoiMoves(n), [n]);
  const D = n <= 3 ? 0.9 : n === 4 ? 0.6 : n === 5 ? 0.42 : 0.3;
  const mid = 2 ** (n - 1) - 1;
  const clock = useClock({ period: mv.length * D + 2.5, rest: (mid + 0.5) * D });
  const k = Math.min(mv.length, Math.floor(clock.t / D));
  const f = k < mv.length ? clock.t / D - k : 0;
  const pegs = [Array.from({ length: n }, (_, i) => n - i), [], []];
  for (let i = 0; i < k; i++) { const [d, a, c] = mv[i]; pegs[a].pop(); pegs[c].push(d); }
  const moving = k < mv.length ? mv[k] : null;
  if (moving) pegs[moving[1]].pop();
  const PX = [62, 180, 298], BASE = 192, DH = 12;
  const wid = (d) => 18 + d * 13;
  const disk = (d, x, y, key, hot) => <rect key={key} x={x - wid(d) / 2} y={y - DH} width={wid(d)} height={DH - 1} rx="4" fill={d === n ? C.red : [C.blue, C.gold, C.teal, C.violet, C.green][(d - 1) % 5]} opacity={hot ? 1 : 0.85} stroke={C.ink} strokeWidth={hot ? 1.6 : 0.6} />;
  let mx = 0, my = 0;
  if (moving) {
    const [, a, c] = moving, h0 = BASE - pegs[a].length * DH, h1 = BASE - pegs[c].length * DH, top = 64;
    if (f < 0.3) { mx = PX[a]; my = lerp(h0, top, ease(f / 0.3)); }
    else if (f < 0.7) { mx = lerp(PX[a], PX[c], ease((f - 0.3) / 0.4)); my = top; }
    else { mx = PX[c]; my = lerp(top, h1, ease((f - 0.7) / 0.3)); }
  }
  return (
    <Frame clock={clock} title="하노이 탑"
      read={<>원판 {n} 개를 A 에서 C 로 · 큰 원판은 작은 원판 위에 놓을 수 없다 · 가장 큰 원판(빨강)을 옮기려면 먼저 위의 {n - 1} 개를 B 로 비켜 두고, 옮긴 뒤 다시 그 위로 — <b>T(n) = 2T(n − 1) + 1</b> · T(1) = 1 이므로 <b>T(n) = 2ⁿ − 1 = {mv.length}</b> 번 · 지금 {k} 번째 이동{k === mid ? " — 가장 큰 원판이 단 한 번 움직이는 순간" : ""} · 원판이 64 개면 1 초에 한 번씩 옮겨도 약 5850 억 년</>}
      controls={<Slider label="원판 수 n" min={2} max={6} step={1} value={n} onChange={(v) => { setN(v); clock.reset(); }} />}>
      <rect x="14" y={BASE} width="332" height="6" rx="2" fill={C.mut} opacity="0.6" />
      {PX.map((x, i) => (
        <g key={i}>
          <rect x={x - 2.5} y={BASE - 112} width="5" height="112" fill={C.mut} opacity="0.55" />
          <text x={x} y={BASE + 20} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{"ABC"[i]}</text>
        </g>
      ))}
      {pegs.map((st, i) => st.map((d, j) => disk(d, PX[i], BASE - j * DH, i + "-" + d, false)))}
      {moving && disk(moving[0], mx, my, "mv", true)}
      <text x="180" y="24" textAnchor="middle" fontSize="12" fontWeight="800" fill={C.ink}>이동 {Math.min(k + (moving ? 1 : 0), mv.length)} / {mv.length}</text>
      <text x="180" y="40" textAnchor="middle" fontSize="9.5" fill={C.mut}>{n} 개 = ({n - 1} 개 옮기기) + 1 + ({n - 1} 개 옮기기)</text>
    </Frame>
  );
}

/* ── 오일러 경로: 모든 변을 한 번씩 — 홀수 차수 점이 0 개 또는 2 개여야 ── */
const EG = {
  house: {
    V: [["", 110, 190], ["", 230, 190], ["", 230, 104], ["", 110, 104], ["", 170, 40]],
    E: [[0, 1, 0], [1, 2, 0], [2, 3, 0], [3, 0, 0], [0, 2, 0], [2, 4, 0], [4, 3, 0], [3, 1, 0]],
    start: 0, trail: [0, 1, 2, 3, 4, 5, 6, 7],
  },
  k5: {
    V: Array.from({ length: 5 }, (_, i) => ["", 170 + 82 * Math.cos(-Math.PI / 2 + (2 * Math.PI * i) / 5), 118 + 82 * Math.sin(-Math.PI / 2 + (2 * Math.PI * i) / 5)]),
    E: [[0, 1, 0], [1, 2, 0], [2, 3, 0], [3, 4, 0], [4, 0, 0], [0, 2, 0], [2, 4, 0], [4, 1, 0], [1, 3, 0], [3, 0, 0]],
    start: 0, trail: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  },
  kb: {
    V: [["북", 160, 34], ["남", 160, 196], ["섬", 112, 115], ["동", 276, 115]],
    E: [[0, 2, -22], [2, 0, -22], [0, 3, 0], [3, 2, 0], [2, 1, -22], [1, 3, 0], [1, 2, -22]],
    start: 0, trail: [0, 1, 2, 3, 4, 5],
  },
};
export function EulerPath({ p = {} }) {
  const [g, setG] = useState(EG[p.graph] ? p.graph : "house");
  const G = EG[g];
  const per = 0.8;
  const clock = useClock({ period: G.trail.length * per + 3, rest: G.trail.length * per + 1.5 });
  const deg = G.V.map((_, i) => G.E.filter(([a, b]) => a === i || b === i).length);
  const odd = deg.filter((d) => d % 2).length;
  const k = Math.min(G.trail.length, Math.floor(clock.t / per));
  const f = k < G.trail.length ? clock.t / per - k : 1;
  const ctrl = ([a, b, off]) => {
    const [, x1, y1] = G.V[a], [, x2, y2] = G.V[b], mx = (x1 + x2) / 2, my = (y1 + y2) / 2, L = Math.hypot(x2 - x1, y2 - y1) || 1;
    return [x1, y1, mx - (off * (y2 - y1)) / L, my + (off * (x2 - x1)) / L, x2, y2];
  };
  let cur = G.start;
  const dirs = G.trail.map((e) => { const [a, b] = G.E[e]; const from = cur; cur = a === from ? b : a; return [from, cur]; });
  const at = k < dirs.length ? dirs[k][0] : cur;
  let dot = null;
  if (k < G.trail.length) {
    const e = G.E[G.trail[k]], [x1, y1, cx, cy, x2, y2] = ctrl(e), rev = dirs[k][0] !== e[0], u = rev ? 1 - f : f;
    dot = [quad(x1, cx, x2, u), quad(y1, cy, y2, u)];
  }
  const used = new Set(G.trail.slice(0, k));
  const stuck = g === "kb" && k === G.trail.length;
  return (
    <Frame clock={clock} title="오일러 경로 — 한붓그리기"
      read={<>점 옆 숫자 = 차수(그 점에 붙은 변의 수) · 한 번 지나갈 때마다 들어가고 나가며 차수를 2 씩 쓴다 → 시작점 · 끝점이 아닌 점은 차수가 짝수여야 한다 · 홀수 점 <b>{odd}</b> 개: {odd === 0 ? "어디서 시작해도 제자리로 돌아오는 오일러 회로가 있다" : odd === 2 ? "한 홀수 점에서 시작해 다른 홀수 점에서 끝나는 오일러 경로가 있다" : "오일러 경로가 없다 — 쾨니히스베르크의 일곱 다리는 어떻게 걸어도 다리가 남는다(오일러, 1736)"}{stuck ? " · 이 길은 동쪽 땅에서 막혀 남쪽 다리 하나(점선)가 남았다" : ""}</>}
      controls={<Seg value={g} onChange={(v) => { setG(v); clock.reset(); }} options={[["house", "집 그리기"], ["k5", "오각별"], ["kb", "쾨니히스베르크"]]} />}>
      {g === "kb" && <>
        <path d="M14 82 Q 120 70 200 78 T 346 70" fill="none" stroke={C.blue} strokeWidth="9" opacity="0.13" />
        <path d="M14 150 Q 120 162 200 152 T 346 160" fill="none" stroke={C.blue} strokeWidth="9" opacity="0.13" />
      </>}
      {G.E.map((e, i) => {
        const [x1, y1, cx, cy, x2, y2] = ctrl(e), on = used.has(i), left = stuck && !on;
        return <path key={i} d={`M${x1} ${y1} Q${cx} ${cy} ${x2} ${y2}`} fill="none" stroke={on ? C.red : left ? C.mut : C.bd} strokeWidth={on ? 3.4 : 2.2} strokeDasharray={left ? "5 4" : undefined} />;
      })}
      {G.V.map(([name, x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r={g === "kb" ? 16 : 9} fill={deg[i] % 2 ? "color-mix(in srgb, #b4442e 18%, var(--card))" : C.card} stroke={i === at ? C.sp : deg[i] % 2 ? C.red : C.ink} strokeWidth={i === at ? 3 : 1.6} />
          {name && <text x={x} y={y + 4} textAnchor="middle" fontSize="10" fontWeight="800" fill={C.ink}>{name}</text>}
          <Label x={x + (g === "kb" ? 22 : 13)} y={y - (g === "kb" ? 10 : 8)} size={10} bold color={deg[i] % 2 ? C.red : C.green} bg>{deg[i]}</Label>
        </g>
      ))}
      {dot && <circle cx={dot[0]} cy={dot[1]} r="5" fill={C.sp} stroke={C.card} strokeWidth="1.5" />}
      <text x="350" y="208" textAnchor="end" fontSize="10" fill={C.mut}>지난 변 {k} / {G.E.length}</text>
    </Frame>
  );
}

/* ── 유클리드 호제법: 직사각형에서 정사각형을 떼어 낸다 — 마지막 정사각형의 변이 최대공약수 ── */
function euclidSteps(a, b) {
  const st = [];
  while (b) { st.push([a, b, Math.floor(a / b), a % b]); [a, b] = [b, a % b]; }
  return { st, g: a };
}
export function Euclid({ p = {} }) {
  const [a, setA] = useState(clamp(p.a ?? 27, 2, 60));
  const [b, setB] = useState(clamp(p.b ?? 21, 1, 60));
  const A = Math.max(a, b), B = Math.min(a, b);
  const { st, g } = useMemo(() => euclidSteps(A, B), [A, B]);
  const per = 1.3;
  const clock = useClock({ period: st.length * per + 2.5, rest: st.length * per + 1 });
  const s = Math.min(196 / A, 176 / B), X0 = 14, Y0 = 18 + (176 - B * s) / 2;
  const sq = [];
  { let x = 0, y = 0, w = A, h = B; st.forEach(([, , q], j) => { const side = Math.min(w, h); for (let i = 0; i < q; i++) sq.push([w >= h ? x + i * side : x, w >= h ? y : y + i * side, side, j, i]); if (w >= h) { x += q * side; w -= q * side; } else { y += q * side; h -= q * side; } }); }
  const k = clock.t / per;
  const pal = [C.blue, C.gold, C.green, C.violet, C.teal, C.red];
  return (
    <Frame clock={clock} title="유클리드 호제법"
      read={<>{A} × {B} 직사각형에서 짧은 변으로 정사각형을 할 수 있는 만큼 떼어 내면 남는 것은 {B} × ({A} mod {B}) 직사각형 — 그래서 <b>gcd(a, b) = gcd(b, a mod b)</b> · 나머지가 0 이 되면 마지막 정사각형의 한 변이 최대공약수 <b>{g}</b> · 나눗셈 {st.length} 번(피보나치 수의 짝이 가장 오래 걸린다)</>}
      controls={<>
        <Slider label="a" min={2} max={60} step={1} value={a} onChange={(v) => { setA(v); clock.reset(); }} />
        <Slider label="b" min={1} max={60} step={1} value={b} onChange={(v) => { setB(v); clock.reset(); }} />
      </>}>
      <rect x={X0} y={Y0} width={A * s} height={B * s} fill="none" stroke={C.ink} strokeWidth="1.4" />
      {sq.map(([x, y, side, j, i]) => {
        const on = k >= j + Math.min(0.8, (i + 1) * 0.12);
        return on ? <rect key={j + "-" + i} x={X0 + x * s} y={Y0 + y * s} width={side * s} height={side * s} fill={pal[j % pal.length]} opacity={j === st.length - 1 && k >= st.length ? 0.55 : 0.3} stroke={pal[j % pal.length]} strokeWidth="1.2" /> : null;
      })}
      <g fontSize="10.5">
        {st.map(([x, y, q, r], j) => (
          <text key={j} x="222" y={30 + j * 17} fill={k >= j ? pal[j % pal.length] : C.mut} opacity={k >= j ? 1 : 0.35} fontWeight={k >= j && k < j + 1 ? 800 : 500}>{x} = {q} × {y} + {r}</text>
        ))}
        <text x="222" y={38 + st.length * 17} fontSize="12" fontWeight="800" fill={k >= st.length ? C.red : C.mut}>gcd = {k >= st.length ? g : "?"}</text>
      </g>
    </Frame>
  );
}

/* ── 유한 오토마타: 이진수를 한 자리씩 읽으며 3 으로 나눈 나머지만 기억한다 ── */
const DFA_S = [[70, 128], [180, 128], [290, 128]];
export function DFA({ p = {} }) {
  const [num, setNum] = useState(clamp(p.n ?? 21, 1, 127));
  const bits = num.toString(2).split("").map(Number);
  const per = 1.2;
  const clock = useClock({ period: bits.length * per + 3, rest: bits.length * per + 1.5 });
  const k = Math.min(bits.length, Math.floor(clock.t / per));
  const f = k < bits.length ? clock.t / per - k : 1;
  const states = [0];
  bits.forEach((bt) => states.push((2 * states[states.length - 1] + bt) % 3));
  const st = states[k], val = k ? parseInt(bits.slice(0, k).join(""), 2) : 0;
  const E = {
    "0-1": [70, 128, 125, 74, 180, 128], "1-0": [180, 128, 125, 182, 70, 128],
    "1-2": [180, 128, 235, 74, 290, 128], "2-1": [290, 128, 235, 182, 180, 128],
  };
  const trim = ([x1, y1, cx, cy, x2, y2]) => { const r = 20, a1 = Math.atan2(cy - y1, cx - x1), a2 = Math.atan2(cy - y2, cx - x2); return [x1 + r * Math.cos(a1), y1 + r * Math.sin(a1), cx, cy, x2 + (r + 1) * Math.cos(a2), y2 + (r + 1) * Math.sin(a2)]; };
  const curE = k < bits.length ? `${states[k]}-${states[k + 1]}` : null;
  let dot = null;
  if (curE) {
    if (E[curE]) { const [x1, y1, cx, cy, x2, y2] = trim(E[curE]); dot = [quad(x1, cx, x2, f), quad(y1, cy, y2, f)]; }
    else { const [x, y] = DFA_S[states[k]], sd = states[k] === 0 ? -1 : 1; dot = [cubic(x + sd * 18, x + sd * 58, x + sd * 58, x + sd * 18, f), cubic(y - 10, y - 34, y + 34, y + 10, f)]; }
  }
  const lbl = { "0-1": ["1", 125, 92], "1-0": ["1", 125, 172], "1-2": ["0", 235, 92], "2-1": ["0", 235, 172] };
  return (
    <Frame clock={clock} title="유한 오토마타 — 3 의 배수 판정"
      read={<>{num} = 이진수 {bits.join("")} 를 왼쪽부터 한 자리씩 읽는다 · 지금까지 읽은 수 v 에 비트 b 가 붙으면 v → 2v + b 이므로 나머지는 r → (2r + b) mod 3 — 수 전체 대신 <b>나머지(상태 3 개)</b>만 기억하면 된다 · 지금 v = {val}, 상태 {st}{k === bits.length ? <> → <b>{st === 0 ? "받아들임: 3 의 배수" : "거부: 3 의 배수가 아님"}</b></> : ""}</>}
      controls={<Slider label="읽을 수" min={1} max={127} step={1} value={num} onChange={(v) => { setNum(v); clock.reset(); }} show={(v) => `${v} = ${v.toString(2)}₍₂₎`} />}>
      {bits.map((bt, i) => (
        <g key={i}>
          <rect x={180 - bits.length * 12 + i * 24} y="14" width="22" height="22" rx="4" fill={i < k ? C.sp : C.card} opacity={i < k ? 0.25 : 1} stroke={i === k ? C.red : C.bd} strokeWidth={i === k ? 2.2 : 1} />
          <text x={180 - bits.length * 12 + i * 24 + 11} y="30" textAnchor="middle" fontSize="12" fontWeight="800" fill={C.ink}>{bt}</text>
        </g>
      ))}
      {Object.entries(E).map(([key, e]) => {
        const [x1, y1, cx, cy, x2, y2] = trim(e), hot = key === curE;
        return (
          <g key={key}>
            <path d={`M${x1} ${y1} Q${cx} ${cy} ${x2} ${y2}`} fill="none" stroke={hot ? C.red : C.mut} strokeWidth={hot ? 2.6 : 1.4} />
            <polygon points={head(x2, y2, cx, cy)} fill={hot ? C.red : C.mut} />
            <Label x={lbl[key][1]} y={lbl[key][2]} size={11} bold anchor="middle" color={hot ? C.red : C.ink} bg>{lbl[key][0]}</Label>
          </g>
        );
      })}
      {[[0, -1, "0"], [2, 1, "1"]].map(([s, side, bt]) => {
        const [x, y] = DFA_S[s], hot = curE === `${s}-${s}`;
        const x1 = x + side * 18, y1 = y - 10, x2 = x + side * 18, y2 = y + 10;
        return (
          <g key={s}>
            <path d={`M${x1} ${y1} C ${x + side * 58} ${y - 34}, ${x + side * 58} ${y + 34}, ${x2} ${y2}`} fill="none" stroke={hot ? C.red : C.mut} strokeWidth={hot ? 2.6 : 1.4} />
            <polygon points={head(x2, y2, x + side * 58, y + 34)} fill={hot ? C.red : C.mut} />
            <Label x={x + side * 52} y={y + 4} size={11} bold anchor="middle" color={hot ? C.red : C.ink} bg>{bt}</Label>
          </g>
        );
      })}
      <Arrow0 />
      {DFA_S.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r="19" fill={i === st ? "color-mix(in srgb, var(--sp, var(--ac)) 22%, var(--card))" : C.card} stroke={i === st ? C.sp : C.ink} strokeWidth={i === st ? 2.6 : 1.5} />
          {i === 0 && <circle cx={x} cy={y} r="15" fill="none" stroke={i === st ? C.sp : C.ink} strokeWidth="1.2" />}
          <text x={x} y={y + 4.5} textAnchor="middle" fontSize="13" fontWeight="800" fill={C.ink}>{i}</text>
          <Label x={x} y={y + 34} size={9} anchor="middle" color={C.mut} bg>나머지 {i}</Label>
        </g>
      ))}
      {dot && <circle cx={dot[0]} cy={dot[1]} r="4.5" fill={C.red} />}
      <text x="350" y="208" textAnchor="end" fontSize="9.5" fill={C.mut}>겹원 = 받아들이는 상태</text>
    </Frame>
  );
}
function Arrow0() {
  return (
    <g>
      <line x1="70" y1="70" x2="70" y2="103" stroke={C.ink} strokeWidth="1.5" />
      <polygon points={head(70, 108, 70, 70)} fill={C.ink} />
      <text x="76" y="80" fontSize="9.5" fill={C.mut}>시작</text>
    </g>
  );
}
