// 정보이론 · 암호 그림 — 엔트로피 · 허프만 부호 · LZ77 압축 · 상호정보 · 이진 대칭 채널과 반복 부호 · 해밍(7,4) · 시저 암호와 빈도 분석 · 모듈러 고리(이산로그 · RSA)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, fmt, clamp, ease, rng, sup, useClock } from "./kit.jsx";

const lg2 = (x) => Math.log(x) / Math.LN2;
const Hb = (p) => (p <= 0 || p >= 1 ? 0 : -p * lg2(p) - (1 - p) * lg2(1 - p));
const ent = (ps) => ps.reduce((s, p) => (p > 0 ? s - p * lg2(p) : s), 0);

/* ── 엔트로피: 놀라움 −log₂ p 의 평균 — 고를수록 크다 ── */
const EP = [[0.25, 0.25, 0.25, 0.25], [0.5, 0.25, 0.125, 0.125], [0.7, 0.1, 0.1, 0.1], [0.97, 0.01, 0.01, 0.01]];
export function Entropy({ p = {} }) {
  const [pb, setPb] = useState(p.p ?? 0.2);
  const clock = useClock({ period: 12, rest: 2.6 });
  const seg = Math.floor(clock.t / 3) % 4, u = ease(clamp(((clock.t % 3) - 0.4) / 1.8, 0, 1));
  const A = EP[seg], B = EP[(seg + 1) % 4], ps = A.map((a, i) => a + (B[i] - a) * u);
  const H = ent(ps);
  const R = plot({ x0: 0, x1: 1, y0: 0, y1: 1.1, pad: [18, 10, 24, 236] });
  return (
    <Frame clock={clock} title="엔트로피 — 평균 놀라움"
      read={<>기호 네 개의 확률(막대)과 각각의 놀라움 −log₂ p(위 숫자) · 엔트로피 H = Σ p × (−log₂ p) = <b>{fmt(H, 3)} 비트</b> — 고르면 가장 크고(log₂ 4 = 2 비트), 한쪽으로 쏠릴수록 작아져 확실하면 0 · 오른쪽: 동전(앞이 나올 확률 p)의 엔트로피 H(p) = <b>{fmt(Hb(pb), 3)}</b> 비트 — p = 1/2 에서 최대 1 비트</>}
      controls={<Slider label="동전 p" min={0.01} max={0.99} step={0.01} value={pb} onChange={setPb} />}>
      {ps.map((q, i) => {
        const x = 30 + i * 48, h = q * 140;
        return (
          <g key={i}>
            <rect x={x} y={186 - h} width="34" height={h} rx="3" fill={[C.blue, C.gold, C.green, C.violet][i]} opacity="0.65" />
            <text x={x + 17} y="202" textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{"ABCD"[i]}</text>
            <text x={x + 17} y={180 - h} textAnchor="middle" fontSize="9" fill={C.mut}>{fmt(q, 2)}</text>
            <text x={x + 17} y={168 - h} textAnchor="middle" fontSize="9" fontWeight="800" fill={C.red}>{q > 0 ? fmt(-lg2(q), 2) : "∞"}</text>
          </g>
        );
      })}
      <line x1="24" x2="222" y1="186" y2="186" stroke={C.mut} />
      <text x="24" y="16" fontSize="10.5" fontWeight="800" fill={C.ink}>H = {fmt(H, 2)} 비트</text>
      <text x="120" y="16" fontSize="9" fill={C.red}>빨간 숫자 = −log₂ p</text>
      <Axes p={R} xl="p" yl="H" grid={false} xt={[0.5, 1]} yt={[0.5, 1]} />
      <path d={R.path(Hb, 0.001, 0.999)} fill="none" stroke={C.sp} strokeWidth="2" />
      <circle cx={R.X(pb)} cy={R.Y(Hb(pb))} r="4.5" fill={C.red} />
    </Frame>
  );
}

/* ── 허프만 부호: 가장 드문 둘을 합치기를 되풀이 — 자주 나오는 기호에 짧은 부호 ── */
const HSETS = { clrs: [["A", 45], ["B", 13], ["C", 12], ["D", 16], ["E", 9], ["F", 5]], dyadic: [["A", 50], ["B", 25], ["C", 12.5], ["D", 12.5]] };
function huffman(set) {
  let id = 0;
  const leaves = set.map(([s, f]) => ({ id: id++, s, f, leaf: true }));
  let pool = leaves.slice();
  const merges = [];
  while (pool.length > 1) {
    pool.sort((a, b) => a.f - b.f || a.id - b.id);
    const [a, b] = pool.splice(0, 2);
    const nd = { id: id++, f: a.f + b.f, kids: [a, b] };
    merges.push(nd); pool.push(nd);
  }
  const root = pool[0], codes = {};
  let li = 0;
  const lay = (n, d, code) => {
    n.depth = d; n.code = code;
    if (n.leaf) { n.xi = li++; codes[n.s] = code; return; }
    n.kids.forEach((k, i) => lay(k, d + 1, code + i));
    n.xi = (n.kids[0].xi + n.kids[1].xi) / 2;
  };
  lay(root, 0, "");
  return { leaves, merges, root, codes, nl: li };
}
export function Huffman({ p = {} }) {
  const [sk, setSk] = useState(HSETS[p.set] ? p.set : "clrs");
  const T = useMemo(() => huffman(HSETS[sk]), [sk]);
  const per = 1.3;
  const clock = useClock({ period: T.merges.length * per + 4, rest: T.merges.length * per + 2 });
  const s = Math.min(T.merges.length, Math.floor(clock.t / per));
  const made = new Set(T.merges.slice(0, s).map((n) => n.id));
  const done = s === T.merges.length;
  const tot = HSETS[sk].reduce((a, [, f]) => a + f, 0);
  const avg = HSETS[sk].reduce((a, [sym, f]) => a + (f / tot) * T.codes[sym].length, 0);
  const H = ent(HSETS[sk].map(([, f]) => f / tot));
  const X = (xi) => 18 + ((xi + 0.5) * 216) / T.nl, Y = (d) => 22 + d * 38;
  const nodes = [...T.leaves, ...T.merges];
  return (
    <Frame clock={clock} title="허프만 부호"
      read={<>빈도가 가장 작은 둘을 하나로 합치기를 되풀이한다(왼쪽 가지 0, 오른쪽 1) — {done ? <>다 만들었다: 평균 부호 길이 <b>{fmt(avg, 2)} 비트</b> ≥ 엔트로피 <b>{fmt(H, 2)} 비트</b>, 고정 길이 {Math.ceil(lg2(HSETS[sk].length))} 비트보다 짧다{Math.abs(avg - H) < 1e-9 ? " — 확률이 모두 2 의 거듭제곱 분의 1 이라 엔트로피와 꼭 같다" : ""}</> : s === 0 ? <>기호 {HSETS[sk].length} 개가 저마다 따로 있다(아래 숫자 = 빈도)</> : <>{s} 번 합쳤다(빨강 = 방금 만든 마디)</>} · 어느 부호도 다른 부호의 앞부분이 아니라(접두 부호) 구분 기호 없이 이어 써도 풀린다</>}
      controls={<Seg value={sk} onChange={(v) => { setSk(v); clock.reset(); }} options={[["clrs", "글자 6 개"], ["dyadic", "2 의 거듭제곱 확률"]]} />}>
      {T.merges.filter((n) => made.has(n.id)).map((n) => n.kids.map((k, i) => (
        <g key={n.id + "-" + i}>
          <line x1={X(n.xi)} y1={Y(n.depth)} x2={X(k.xi)} y2={Y(k.depth)} stroke={C.mut} strokeWidth="1.4" />
          <text x={(X(n.xi) + X(k.xi)) / 2 + (i ? 4 : -9)} y={(Y(n.depth) + Y(k.depth)) / 2} fontSize="9" fontWeight="800" fill={i ? C.red : C.blue}>{i}</text>
        </g>
      )))}
      {nodes.filter((n) => n.leaf || made.has(n.id)).map((n) => {
        const hot = !n.leaf && T.merges[s - 1] && T.merges[s - 1].id === n.id;
        return (
          <g key={n.id}>
            <circle cx={X(n.xi)} cy={Y(n.depth)} r={n.leaf ? 12 : 10} fill={n.leaf ? C.card : hot ? "color-mix(in srgb, #b4442e 25%, var(--card))" : C.card} stroke={hot ? C.red : n.leaf ? C.ink : C.mut} strokeWidth={hot ? 2.4 : 1.3} />
            <text x={X(n.xi)} y={Y(n.depth) + 3.5} textAnchor="middle" fontSize={n.leaf ? 10 : 8.5} fontWeight="800" fill={C.ink}>{n.leaf ? n.s : fmt(n.f, 1)}</text>
            {n.leaf && <text x={X(n.xi)} y={Y(n.depth) + 24} textAnchor="middle" fontSize="8.5" fill={C.mut}>{fmt(n.f, 1)}</text>}
          </g>
        );
      })}
      <text x="250" y="20" fontSize="10" fontWeight="800" fill={C.ink}>기호 · 부호</text>
      {HSETS[sk].map(([sym, f], i) => (
        <g key={sym}>
          <text x="250" y={40 + i * 19} fontSize="10.5" fontWeight="800" fill={C.ink}>{sym}</text>
          <text x="266" y={40 + i * 19} fontSize="10.5" fill={done ? C.sp : C.bd} fontFamily="monospace">{done ? T.codes[sym] : "…"}</text>
          <text x="352" y={40 + i * 19} textAnchor="end" fontSize="9" fill={C.mut}>{fmt(f / tot * 100, 1)}%</text>
        </g>
      ))}
    </Frame>
  );
}

/* ── LZ77: 앞에 나온 글자열을 (거리, 길이)로 가리킨다 ── */
const LZT = { kj: "간장 공장 공장장은 강 공장장", ab: "ABABABABABABABAB", none: "가나다라마바사아자차카타" };
function lz77(s) {
  const out = [];
  let i = 0;
  while (i < s.length) {
    let bl = 0, bo = 0;
    for (let j = 0; j < i; j++) { let k = 0; while (i + k < s.length && s[j + k] === s[i + k]) k++; if (k > bl) { bl = k; bo = i - j; } }
    if (bl >= 2) { out.push({ ref: true, off: bo, len: bl, at: i }); i += bl; } else { out.push({ ref: false, ch: s[i], at: i }); i++; }
  }
  return out;
}
export function LZ({ p = {} }) {
  const [tk, setTk] = useState(LZT[p.text] ? p.text : "kj");
  const s = LZT[tk], toks = useMemo(() => lz77(s), [s]);
  const per = 0.9;
  const clock = useClock({ period: toks.length * per + 3, rest: toks.length * per + 1.5 });
  const k = Math.min(toks.length - 1, Math.floor(clock.t / per));
  const cur = toks[k], cw = Math.min(22, 330 / s.length), X0 = 180 - (cw * s.length) / 2;
  const covered = cur.at + (cur.ref ? cur.len : 1);
  const tokStr = (t) => (t.ref ? `(${t.off}, ${t.len})` : t.ch === " " ? "␣" : t.ch);
  return (
    <Frame clock={clock} title="LZ77 압축"
      read={<>글자를 왼쪽부터 읽으며, 앞에 나온 글자열과 같으면 글자 대신 <b>(얼마나 뒤로, 몇 글자)</b> 를 적는다 · {cur.ref ? <>지금: {cur.off} 칸 뒤에서 {cur.len} 글자를 베낀다{cur.len > cur.off ? " — 베끼는 중인 글자를 다시 베끼는 겹침 복사(같은 무늬의 반복)" : ""}</> : <>지금: 앞에 없는 글자라 그대로 적는다</>} · 글자 {s.length} 개 → 토큰 <b>{toks.length}</b> 개{tk === "none" ? " — 반복이 없으면 줄지 않는다" : ""} · ZIP · PNG 가 이 방법에 허프만 부호를 더해 쓴다</>}
      controls={<Seg value={tk} onChange={(v) => { setTk(v); clock.reset(); }} options={[["kj", "간장 공장"], ["ab", "ABAB…"], ["none", "반복 없음"]]} />}>
      {[...s].map((ch, i) => {
        const inCur = i >= cur.at && i < covered, src = cur.ref && i >= cur.at - cur.off && i < cur.at - cur.off + cur.len;
        return (
          <g key={i}>
            <rect x={X0 + i * cw} y="40" width={cw - 1.5} height="24" rx="3" fill={inCur ? "color-mix(in srgb, #b4442e 22%, var(--card))" : src ? "color-mix(in srgb, #2f6db0 22%, var(--card))" : i < cur.at ? C.card : C.in} stroke={inCur ? C.red : src ? C.blue : C.bd} strokeWidth={inCur || src ? 1.8 : 0.8} />
            <text x={X0 + i * cw + cw / 2 - 0.7} y="57" textAnchor="middle" fontSize={cw < 16 ? 9.5 : 11} fontWeight="700" fill={i < covered ? C.ink : C.mut}>{ch === " " ? "␣" : ch}</text>
          </g>
        );
      })}
      {cur.ref && (() => {
        const x1 = X0 + (cur.at - cur.off + cur.len / 2) * cw, x2 = X0 + (cur.at + cur.len / 2) * cw;
        return <path d={`M${x1} 38 Q ${(x1 + x2) / 2} ${8} ${x2} 38`} fill="none" stroke={C.blue} strokeWidth="1.6" strokeDasharray="4 3" />;
      })()}
      <text x="14" y="96" fontSize="10" fontWeight="800" fill={C.ink}>적은 토큰</text>
      {toks.slice(0, k + 1).map((t, i) => (
        <text key={i} x={14 + (i % 8) * 43} y={116 + Math.floor(i / 8) * 20} fontSize="10.5" fontWeight={i === k ? 800 : 500} fill={t.ref ? C.blue : C.ink}>{tokStr(t)}</text>
      ))}
      <text x="350" y="210" textAnchor="end" fontSize="9.5" fill={C.mut}>파랑 = 베낀 곳, 빨강 = 지금 적는 곳</text>
    </Frame>
  );
}

/* ── 상호정보: 함께 움직일수록 겹치는 정보가 커진다 ── */
export function Mutual() {
  const clock = useClock({ period: 10, rest: 2.82 });
  const rho = 0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10), c = 0.21 * rho;
  const J = [[0.49 + c, 0.21 - c], [0.21 - c, 0.09 + c]];
  const HX = Hb(0.3), HY = Hb(0.3), HXY = ent([J[0][0], J[0][1], J[1][0], J[1][1]]), I = HX + HY - HXY;
  const S = 78, x0 = 212;
  return (
    <Frame clock={clock} title="상호정보"
      read={<>X = 비가 오나(30 %), Y = 우산을 쓰나(30 %) · 왼쪽 칸의 넓이 = 함께 일어날 확률 · H(X) = H(Y) = {fmt(HX, 3)} 비트, 둘을 함께 적는 데 H(X, Y) = {fmt(HXY, 3)} 비트 · 겹친 부분 <b>I(X; Y) = H(X) + H(Y) − H(X, Y) = {fmt(I, 3)} 비트</b> — Y 를 보면 X 에 대해 얻는 정보 · 서로 독립이면 0, 우산을 보면 비를 확실히 알면 H(X) 전부</>}>
      {[0, 1].map((x) => [0, 1].map((y) => {
        const pp = J[x][y], side = Math.sqrt(pp) * 80, cx = 74 + y * 84, cy = 64 + x * 84;
        return (
          <g key={x + "-" + y}>
            <rect x={cx - 40} y={cy - 40} width="80" height="80" fill="none" stroke={C.bd} />
            <rect x={cx - side / 2} y={cy - side / 2} width={side} height={side} rx="3" fill={x === y ? C.sp : C.gold} opacity="0.55" />
            <text x={cx} y={cy + 4} textAnchor="middle" fontSize="10.5" fontWeight="800" fill={C.ink}>{fmt(pp, 2)}</text>
          </g>
        );
      }))}
      <text x="74" y="16" textAnchor="middle" fontSize="9.5" fill={C.mut}>우산 안 씀</text>
      <text x="158" y="16" textAnchor="middle" fontSize="9.5" fill={C.mut}>우산 씀</text>
      <text x="22" y="68" textAnchor="middle" fontSize="9.5" fill={C.mut}>맑음</text>
      <text x="22" y="152" textAnchor="middle" fontSize="9.5" fill={C.mut}>비</text>
      <rect x={x0} y="54" width={HX * S} height="22" rx="4" fill={C.blue} opacity="0.35" />
      <rect x={x0 + (HX - I) * S} y="84" width={HY * S} height="22" rx="4" fill={C.red} opacity="0.35" />
      {I > 0.005 && <rect x={x0 + (HX - I) * S} y="54" width={I * S} height="52" fill={C.violet} opacity="0.25" stroke={C.violet} />}
      <text x={x0} y="48" fontSize="9.5" fontWeight="800" fill={C.blue}>H(X)</text>
      <text x={x0 + (HX - I + HY) * S} y="122" textAnchor="end" fontSize="9.5" fontWeight="800" fill={C.red}>H(Y)</text>
      <text x={x0 + (HX - I / 2) * S} y="140" textAnchor="middle" fontSize="10" fontWeight="800" fill={C.violet}>I = {fmt(I, 2)}</text>
      <line x1={x0} x2={x0 + HXY * S} y1="160" y2="160" stroke={C.ink} strokeWidth="1.4" />
      <text x={x0} y="176" fontSize="9" fill={C.ink}>H(X, Y) = {fmt(HXY, 2)}</text>
      <text x={x0} y="196" fontSize="9" fill={C.mut}>의존 정도 {fmt(rho * 100, 0)} %</text>
    </Frame>
  );
}

/* ── 이진 대칭 채널: 비트가 확률 p 로 뒤집힌다 — 반복 부호와 다수결 ── */
const choose = (n, k) => { let r = 1; for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i; return r; };
const repErr = (n, p) => { let s = 0; for (let k = Math.floor(n / 2) + 1; k <= n; k++) s += choose(n, k) * p ** k * (1 - p) ** (n - k); return s; };
export function BSC({ p = {} }) {
  const [pf, setPf] = useState(p.p ?? 0.1);
  const [n, setN] = useState([1, 3, 5].includes(p.n) ? p.n : 3);
  const msg = useMemo(() => { const r = rng(4); return Array.from({ length: 20 }, () => (r() < 0.5 ? 1 : 0)); }, []);
  const noise = useMemo(() => { const r = rng(8); return Array.from({ length: 100 }, () => r()); }, []);
  const clock = useClock({ period: 11, rest: 9.5 });
  const shown = Math.min(20, Math.floor((clock.t / 8.5) * 20) + 1);
  const enc = msg.flatMap((b) => Array(n).fill(b));
  const rec = enc.map((b, j) => (noise[j] < pf ? 1 - b : b));
  const dec = msg.map((_, i) => (rec.slice(i * n, i * n + n).reduce((a, b) => a + b, 0) * 2 > n ? 1 : 0));
  const errs = dec.slice(0, shown).filter((b, i) => b !== msg[i]).length;
  const flips = rec.slice(0, shown * n).filter((b, j) => b !== enc[j]).length;
  const cap = 1 - Hb(pf);
  const cw = 15, X0 = 52, ew = (cw * 20) / (20 * n);
  const G = plot({ x0: 0, x1: 1.05, y0: 0, y1: 6, pad: [146, 10, 18, 52] });
  return (
    <Frame clock={clock} title="잡음 채널과 반복 부호"
      read={<>비트마다 확률 p = {fmt(pf, 2)} 로 뒤집히는 채널 · {n === 1 ? "비트를 한 번씩 그대로 보낸다" : `비트를 ${n} 번씩 보내고 다수결로 되살린다`} · 뒤집힌 비트 {flips} 개 → 되살린 뒤 틀린 비트 <b>{errs}</b> 개 · 반복할수록 오류는 줄지만 전송률이 1/n 로 떨어진다(아래 점) · 섀넌: 전송률이 채널 용량 <b>C = 1 − H(p) = {fmt(cap, 3)}</b> 보다 낮으면 긴 부호로 오류를 얼마든지 작게 할 수 있다(초록 선 왼쪽 어디서나)</>}
      controls={<>
        <Slider label="뒤집힐 확률 p" min={0} max={0.3} step={0.01} value={pf} onChange={setPf} />
        <Seg value={n} onChange={setN} options={[[1, "그대로"], [3, "3 번 반복"], [5, "5 번 반복"]]} />
      </>}>
      {[["보낸 것", 22], ["부호", 50], ["받은 것", 78], ["되살림", 106]].map(([t, y]) => <text key={t} x="8" y={y + 12} fontSize="9" fill={C.mut}>{t}</text>)}
      {msg.map((b, i) => <g key={"m" + i} opacity={i < shown ? 1 : 0.25}><rect x={X0 + i * cw} y="22" width={cw - 1.5} height="16" rx="2" fill={b ? C.ink : C.card} stroke={C.bd} /></g>)}
      {enc.map((b, j) => <rect key={"e" + j} x={X0 + j * ew} y="50" width={Math.max(0.8, ew - 0.6)} height="16" fill={b ? C.ink : C.card} stroke={C.bd} strokeWidth="0.4" opacity={j < shown * n ? 1 : 0.25} />)}
      {rec.map((b, j) => <rect key={"r" + j} x={X0 + j * ew} y="78" width={Math.max(0.8, ew - 0.6)} height="16" fill={b !== enc[j] ? C.red : b ? C.ink : C.card} stroke={C.bd} strokeWidth="0.4" opacity={j < shown * n ? 1 : 0.25} />)}
      {dec.map((b, i) => <rect key={"d" + i} x={X0 + i * cw} y="106" width={cw - 1.5} height="16" rx="2" fill={i < shown && b !== msg[i] ? C.red : b ? C.ink : C.card} stroke={i < shown && b !== msg[i] ? C.red : C.bd} strokeWidth={i < shown && b !== msg[i] ? 2 : 1} opacity={i < shown ? 1 : 0.25} />)}
      <Axes p={G} xl="" yl="" grid={false} xt={[0.2, 0.4, 0.6, 0.8, 1]} yt={[2, 4, 6]} yfmt={(v) => "10" + sup(-v)} />
      <text x={G.l + 4} y={G.t + 2} fontSize="8.5" fill={C.mut}>오류율(위로 갈수록 작다)</text>
      <text x={G.l + 2} y={G.b + 13} fontSize="9" fill={C.ink} fontStyle="italic">전송률</text>
      <line x1={G.X(cap)} x2={G.X(cap)} y1={G.t} y2={G.b} stroke={C.green} strokeWidth="1.6" strokeDasharray="4 3" />
      <text x={G.X(cap) + 3} y={G.t + 10} fontSize="9" fill={C.green}>C</text>
      {[1, 3, 5, 7, 9].map((m) => { const e = repErr(m, pf), y = clamp(-Math.log10(Math.max(1e-9, e)), 0, 6); return <g key={m}><circle cx={G.X(1 / m)} cy={G.Y(y)} r={m === n ? 4.5 : 3} fill={m === n ? C.red : C.sp} /><text x={G.X(1 / m)} y={G.Y(y) - 6} textAnchor="middle" fontSize="8.5" fill={C.mut}>{m}</text></g>; })}
    </Frame>
  );
}

/* ── 해밍(7,4): 세 원의 홀짝 검사로 틀린 한 비트의 자리를 찾는다 ── */
const HPOS = { 1: [98, 76], 2: [202, 76], 3: [150, 64], 4: [150, 174], 5: [121, 128], 6: [179, 128], 7: [150, 106] };
const HCIR = [[1, 3, 5, 7], [2, 3, 6, 7], [4, 5, 6, 7]];
export function Hamming({ p = {} }) {
  const [v, setV] = useState(clamp(p.v ?? 11, 0, 15));
  const clock = useClock({ period: 2 + 7 * 1.6, rest: 2 + 4 * 1.6 + 1.3 });
  const d = [(v >> 3) & 1, (v >> 2) & 1, (v >> 1) & 1, v & 1];
  const p1 = d[0] ^ d[1] ^ d[3], p2 = d[0] ^ d[2] ^ d[3], p3 = d[1] ^ d[2] ^ d[3];
  const code = [p1, p2, d[0], p3, d[1], d[2], d[3]];
  const ph = clock.t < 2 ? 0 : Math.min(7, Math.floor((clock.t - 2) / 1.6) + 1), lt = clock.t < 2 ? 0 : (clock.t - 2) % 1.6;
  const err = ph, recv = code.map((b, i) => (i + 1 === err ? 1 - b : b));
  const showCheck = err > 0 && lt > 0.5, fixed = err > 0 && lt > 1.05;
  const fails = HCIR.map((cs) => cs.reduce((s, q) => s + recv[q - 1], 0) % 2);
  const syn = fails[0] + 2 * fails[1] + 4 * fails[2];
  const shownBits = fixed ? code : recv;
  return (
    <Frame clock={clock} title="해밍(7,4) 부호"
      read={<>데이터 4 비트 {d.join("")} 에 검사 비트 3 개를 붙여 7 비트로 보낸다 — 원마다 1 의 개수가 짝수가 되게 · {err === 0 ? "오류 없이 받으면 세 원 모두 짝수" : !showCheck ? <>{err} 번 자리가 뒤집혔다 — 받는 쪽은 아직 어디인지 모른다</> : <>세 원을 검사하면 홀수인 원(빨강)이 생긴다 — 틀린 비트는 빨간 원 모두에 들고 나머지 원에는 없는 단 한 자리 · 증후 (C B A) = {fails[2]}{fails[1]}{fails[0]} 을 이진수로 읽으면 <b>{syn}</b> 번 자리{fixed ? " → 그 비트를 뒤집어 고쳤다" : ""}</>} · 비트 3 개를 더해 오류 하나를 고친다(부호율 4/7)</>}
      controls={<Slider label="데이터" min={0} max={15} step={1} value={v} onChange={setV} show={(x) => x.toString(2).padStart(4, "0")} />}>
      {[[120, 90, "A"], [180, 90, "B"], [150, 142, "C"]].map(([x, y, n], i) => {
        const bad = showCheck && fails[i];
        return (
          <g key={n}>
            <circle cx={x} cy={y} r="52" fill={bad ? C.red : C.sp} opacity={bad ? 0.12 : 0.06} stroke={bad ? C.red : C.sp} strokeWidth={bad ? 2.4 : 1.4} />
            <text x={n === "A" ? x - 48 : n === "B" ? x + 48 : x + 46} y={n === "C" ? y + 44 : y - 40} textAnchor="middle" fontSize="11" fontWeight="800" fill={bad ? C.red : C.sp}>{n}</text>
          </g>
        );
      })}
      {Object.entries(HPOS).map(([pos, [x, y]]) => {
        const i = +pos, b = shownBits[i - 1], isErr = i === err && !fixed, isFix = i === err && fixed;
        return (
          <g key={pos}>
            <circle cx={x} cy={y} r="11" fill={isErr ? "color-mix(in srgb, #b4442e 30%, var(--card))" : isFix ? "color-mix(in srgb, #3f7d3a 30%, var(--card))" : C.card} stroke={isErr ? C.red : isFix ? C.green : [1, 2, 4].includes(i) ? C.gold : C.ink} strokeWidth={isErr || isFix ? 2.4 : 1.4} />
            <text x={x} y={y + 4} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.ink}>{b}</text>
            <text x={x + 12} y={y - 9} fontSize="7.5" fill={C.mut}>{i}</text>
          </g>
        );
      })}
      <text x="250" y="22" fontSize="9.5" fontWeight="800" fill={C.ink}>보낸 7 비트</text>
      {code.map((b, i) => (
        <g key={"c" + i}>
          <rect x={250 + i * 15} y="30" width="13" height="18" rx="2" fill={C.card} stroke={[0, 1, 3].includes(i) ? C.gold : C.bd} />
          <text x={256.5 + i * 15} y="43" textAnchor="middle" fontSize="10" fontWeight="700" fill={C.ink}>{b}</text>
        </g>
      ))}
      <text x="250" y="68" fontSize="9.5" fontWeight="800" fill={C.ink}>받은 7 비트</text>
      {recv.map((b, i) => (
        <g key={"r" + i}>
          <rect x={250 + i * 15} y="76" width="13" height="18" rx="2" fill={i + 1 === err ? "color-mix(in srgb, #b4442e 30%, var(--card))" : C.card} stroke={i + 1 === err ? C.red : C.bd} />
          <text x={256.5 + i * 15} y="89" textAnchor="middle" fontSize="10" fontWeight="700" fill={C.ink}>{b}</text>
        </g>
      ))}
      <text x="250" y="116" fontSize="9" fill={C.gold}>노랑 = 검사 비트</text>
      <text x="250" y="134" fontSize="9" fill={C.mut}>A: 1 · 3 · 5 · 7 번</text>
      <text x="250" y="148" fontSize="9" fill={C.mut}>B: 2 · 3 · 6 · 7 번</text>
      <text x="250" y="162" fontSize="9" fill={C.mut}>C: 4 · 5 · 6 · 7 번</text>
      {err > 0 && showCheck && <text x="250" y="186" fontSize="10.5" fontWeight="800" fill={fixed ? C.green : C.red}>증후 {syn} → {fixed ? "고침" : "찾음"}</text>}
    </Frame>
  );
}

/* ── 시저 암호: 모든 글자를 같은 칸만큼 민다 — 글자 빈도가 열쇠를 드러낸다 ── */
const ENG = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.8, 4.0, 2.4, 6.7, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.15, 2.0, 0.07];
const PLAIN = "SECRET MESSAGES HAVE TRAVELED IN WAR AND IN PEACE FOR THOUSANDS OF YEARS AND THE OLDEST TRICK IS TO SHIFT EVERY LETTER OF THE ALPHABET BY THE SAME NUMBER OF PLACES SO THAT ONLY A FRIEND WHO KNOWS THE KEY CAN READ THEM";
const KEY = 7;
const shiftStr = (s, k) => s.replace(/[A-Z]/g, (ch) => String.fromCharCode(((ch.charCodeAt(0) - 65 + k + 26) % 26) + 65));
const CIPHER = shiftStr(PLAIN, KEY);
export function Caesar() {
  const cnt = useMemo(() => { const c = Array(26).fill(0); for (const ch of CIPHER) if (ch >= "A" && ch <= "Z") c[ch.charCodeAt(0) - 65]++; return c; }, []);
  const N = cnt.reduce((a, b) => a + b, 0);
  const chi = useMemo(() => Array.from({ length: 26 }, (_, k) => ENG.reduce((s, e, L) => { const o = cnt[(L + k) % 26], ex = (e / 100) * N; return s + (o - ex) ** 2 / ex; }, 0)), [cnt, N]);
  const best = chi.indexOf(Math.min(...chi));
  const per = 0.38;
  const clock = useClock({ period: 26 * per + 3, rest: 26 * per + 1.5 });
  const k = clock.t < 26 * per ? Math.floor(clock.t / per) : best;
  const dec = shiftStr(CIPHER, -k);
  const B = plot({ x0: -0.5, x1: 25.5, y0: 0, y1: 16, pad: [44, 10, 80, 26] });
  const G = plot({ x0: -0.5, x1: 25.5, y0: 0, y1: Math.max(...chi) * 1.05, pad: [164, 10, 6, 26] });
  return (
    <Frame clock={clock} title="시저 암호와 빈도 분석"
      read={<>모든 글자를 같은 칸만큼 민 암호문을 받았다 · 밀린 칸 k 를 하나씩 시험해 되돌린 글의 글자 빈도(막대)가 영어의 빈도(점)와 얼마나 닮았는지 χ² 로 잰다 · 지금 k = <b>{k}</b>, χ² = {fmt(chi[k], 0)}{k === best ? <> — 가장 닮았다: 열쇠는 <b>{best}</b></> : ""} · 열쇠가 26 가지뿐이라 다 해 봐도 금방이고, 글자를 아무렇게나 바꾼 치환 암호도 빈도 분석에 무너진다</>}
      controls={<Slider label="되돌릴 칸 k" min={0} max={25} step={1} value={k} onChange={(x) => { clock.setT(x * per + 0.05); clock.setPlaying(false); }} />}>
      <text x="14" y="16" fontSize="9" fill={C.mut} fontFamily="monospace">암호: {CIPHER.slice(0, 44)}…</text>
      <text x="14" y="32" fontSize="9" fill={k === best ? C.green : C.ink} fontFamily="monospace" fontWeight="700">해독: {dec.slice(0, 44)}…</text>
      {cnt.map((_, L) => {
        const o = (cnt[(L + k) % 26] / N) * 100;
        return (
          <g key={L}>
            <rect x={B.X(L - 0.38)} y={B.Y(Math.min(16, o))} width={B.X(0.76) - B.X(0)} height={B.Y(0) - B.Y(Math.min(16, o))} fill={C.sp} opacity="0.55" />
            <circle cx={B.X(L)} cy={B.Y(ENG[L])} r="2.6" fill={C.red} />
            <text x={B.X(L)} y={B.b + 10} textAnchor="middle" fontSize="7.5" fill={C.mut}>{String.fromCharCode(65 + L)}</text>
          </g>
        );
      })}
      <line x1={B.l} x2={B.r} y1={B.b} y2={B.b} stroke={C.mut} />
      <text x={B.r} y={B.t + 6} textAnchor="end" fontSize="8.5" fill={C.red}>● 영어 빈도 %</text>
      <path d={G.poly(chi.map((c, i) => [i, c]))} fill="none" stroke={C.mut} strokeWidth="1.2" />
      {chi.map((c, i) => <circle key={i} cx={G.X(i)} cy={G.Y(c)} r={i === k ? 4 : 1.8} fill={i === best ? C.green : i === k ? C.red : C.mut} />)}
      <text x={G.r} y={G.t + 8} textAnchor="end" fontSize="8.5" fill={C.mut}>k 마다 χ² (작을수록 영어답다)</text>
    </Frame>
  );
}

/* ── 모듈러 고리: g 의 거듭제곱은 고리 위를 뒤죽박죽 뛴다(이산로그) · RSA 는 제곱-곱하기로 되돌린다 ── */
const powmod = (b, e, m) => { let r = 1, x = b % m, k = e; while (k > 0) { if (k & 1) r = (r * x) % m; x = (x * x) % m; k >>= 1; } return r; };
const RSA_STEPS = (() => {
  const n = 55, out = [{ v: 8, t: "평문 m = 8" }, { v: 17, t: "암호 c = 8³ ≡ 17" }];
  const sq = [17];
  for (let i = 1; i < 5; i++) { sq.push((sq[i - 1] * sq[i - 1]) % n); out.push({ v: sq[i], t: `c${sup(2 ** i)} = ${sq[i - 1]} × ${sq[i - 1]} ≡ ${sq[i]}` }); }
  out.push({ v: 17, t: "d = 27 = 16 + 8 + 2 + 1" });
  let acc = 17;
  [[1, 2], [3, 8], [4, 16]].forEach(([i, e]) => { const prev = acc; acc = (acc * sq[i]) % n; out.push({ v: acc, t: `× c${sup(e)}: ${prev} × ${sq[i]} ≡ ${acc}` }); });
  return out;
})();
export function ModRing({ p = {} }) {
  const [m, setM] = useState(p.mode === "rsa" ? "rsa" : "dlog");
  const P = m === "dlog" ? 23 : 55, g = 5;
  const seq = m === "dlog" ? Array.from({ length: 22 }, (_, k) => powmod(g, k + 1, 23)) : RSA_STEPS.map((s) => s.v);
  const per = m === "dlog" ? 0.45 : 1.1;
  const clock = useClock({ period: seq.length * per + 3, rest: seq.length * per + 1.5 });
  const k = Math.min(seq.length - 1, Math.floor(clock.t / per));
  const cx = 112, cy = 112, R = 88;
  const pos = (v) => [cx + R * Math.sin((2 * Math.PI * v) / P), cy - R * Math.cos((2 * Math.PI * v) / P)];
  return (
    <Frame clock={clock} title="모듈러 거듭제곱"
      read={m === "dlog"
        ? <>법 23 의 고리에서 5 를 거듭제곱하면 5, 2, 10, 4, 20, … 처럼 뒤죽박죽 뛰다가 22 번 만에 모든 수(0 빼고)를 한 번씩 지나 1 로 돌아온다(5 는 원시근) · 지금 5{sup(k + 1)} ≡ <b>{seq[k]}</b> · 거꾸로 ‘5 를 몇 번 곱하면 이 수가 되나’(이산로그)는 큰 소수에서 사실상 풀 수 없다 · 디피-헬먼: 철수 a = 6 → A = 5⁶ ≡ 8(파랑), 영희 b = 15 → B = 5¹⁵ ≡ 19(보라)를 공개해도, 둘만 같은 비밀 B 의 a 제곱 = A 의 b 제곱 ≡ <b>2</b> 를 얻는다</>
        : <>RSA(작은 예): n = 5 × 11 = 55, φ(n) = 40, 공개 지수 e = 3, 비밀 지수 d = 27(3 × 27 = 81 ≡ 1 mod 40) · 평문 8 을 세제곱해 암호 17 · 되돌릴 때 17 의 27 제곱을 그대로 계산하지 않고 제곱을 되풀이해(17 → 14 → 31 → 26 → 16) 필요한 것만 곱한다 · 지금: <b>{RSA_STEPS[k].t}</b>{k === seq.length - 1 ? " — 평문 8 이 돌아왔다" : ""}</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["dlog", "이산로그 · 디피-헬먼"], ["rsa", "RSA"]]} />}>
      <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.bd} />
      {Array.from({ length: P }, (_, v) => {
        const [x, y] = pos(v), on = seq.slice(0, k + 1).includes(v), cur = seq[k] === v;
        const [lx, ly] = [cx + (R + 11) * Math.sin((2 * Math.PI * v) / P), cy - (R + 11) * Math.cos((2 * Math.PI * v) / P) + 3];
        return (
          <g key={v}>
            <circle cx={x} cy={y} r={cur ? 5.5 : on ? 3.6 : 2.2} fill={cur ? C.red : on ? C.sp : C.mut} opacity={cur || on ? 1 : 0.5} />
            {(P === 23 || v % 5 === 0 || on) && <text x={lx} y={ly} textAnchor="middle" fontSize={P === 23 ? 8.5 : 7.5} fill={cur ? C.red : C.mut} fontWeight={cur ? 800 : 500}>{v}</text>}
          </g>
        );
      })}
      {seq.slice(0, k + 1).map((v, i) => {
        if (!i) return null;
        const [x1, y1] = pos(seq[i - 1]), [x2, y2] = pos(v);
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={i === k ? C.red : C.sp} strokeWidth={i === k ? 2 : 1} opacity={i === k ? 1 : 0.4} />;
      })}
      {m === "dlog"
        ? seq.slice(0, k + 1).map((v, i) => <text key={i} x={232 + Math.floor(i / 11) * 64} y={22 + (i % 11) * 17} fontSize="9.5" fill={i === k ? C.red : i === 5 ? C.blue : i === 14 ? C.violet : C.ink} fontWeight={i === k || i === 5 || i === 14 ? 800 : 500}>5{sup(i + 1)} ≡ {v}</text>)
        : RSA_STEPS.slice(0, k + 1).map((s, i) => <text key={i} x="226" y={22 + i * 19} fontSize="9" fill={i === k ? C.red : C.ink} fontWeight={i === k ? 800 : 500}>{s.t}</text>)}
    </Frame>
  );
}
