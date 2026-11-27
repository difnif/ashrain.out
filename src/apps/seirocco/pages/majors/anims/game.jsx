// 게임이론 그림 — 2 × 2 게임의 최선 반응과 내시 균형 · 혼합 전략(무차별) · 역진 귀납(진입 게임 · 지네 게임) · 반복 죄수의 딜레마 대회 · 매-비둘기 진화 · 쿠르노 과점 · 경매(수입 동등)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Axes, Arrow, Label, fmt, clamp, rng, useClock } from "./kit.jsx";

export const GAMES = {
  pd: { name: "죄수의 딜레마", r: ["협력", "배신"], c: ["협력", "배신"], m: [[[3, 3], [0, 5]], [[5, 0], [1, 1]]], say: "배신이 우월전략 — 둘 다 배신(1, 1)이 유일한 균형인데, 둘 다 협력(3, 3)보다 나쁘다" },
  stag: { name: "사슴 사냥", r: ["사슴", "토끼"], c: ["사슴", "토끼"], m: [[[4, 4], [0, 3]], [[3, 0], [3, 3]]], say: "균형이 둘 — (사슴, 사슴)이 더 좋지만 상대를 믿어야 한다(협조의 문제)" },
  chicken: { name: "치킨 게임", r: ["피함", "직진"], c: ["피함", "직진"], m: [[[0, 0], [-1, 1]], [[1, -1], [-10, -10]]], say: "순수 균형이 둘 — 한쪽만 피한다. 누가 피할지가 다툼이다" },
  sexes: { name: "성 대결", r: ["야구", "공연"], c: ["야구", "공연"], m: [[[3, 2], [0, 0]], [[0, 0], [2, 3]]], say: "같이 가는 것이 좋지만 어디로 갈지 선호가 다르다 — 순수 균형 둘(+ 혼합 하나)" },
  pennies: { name: "동전 맞추기", r: ["앞", "뒤"], c: ["앞", "뒤"], m: [[[1, -1], [-1, 1]], [[-1, 1], [1, -1]]], say: "순수 균형이 없다 — 반반 섞는 혼합 전략만 균형이다" },
};
const nashCells = (m) => { const out = []; for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) if (m[i][j][0] >= m[1 - i][j][0] && m[i][j][1] >= m[i][1 - j][1]) out.push([i, j]); return out; };

/* ── 2 × 2 게임: 상대 행동마다 내 최선 반응 — 서로 최선 반응인 칸이 내시 균형 ── */
export function Nash2({ p = {} }) {
  const [g, setG] = useState(GAMES[p.game] ? p.game : "pd");
  const clock = useClock({ period: 11, rest: 10 });
  const G = GAMES[g], m = G.m;
  const step = Math.min(5, Math.floor(clock.t / 1.6));
  const x0 = 120, y0 = 46, cw = 104, ch = 66;
  const cx = (j) => x0 + cw * j + cw / 2, cy = (i) => y0 + ch * i + ch / 2;
  const brRow = (j) => (m[0][j][0] >= m[1][j][0] ? 0 : 1), brCol = (i) => (m[i][0][1] >= m[i][1][1] ? 0 : 1);
  const showR = (j) => step >= 1 + j, showC = (i) => step >= 3 + i;
  const ne = nashCells(m);
  const say = step === 0 ? "칸마다 (행 보수, 열 보수) — 파랑이 행 선수, 노랑이 열 선수" :
    step <= 2 ? `열 선수가 「${G.c[step - 1]}」 하면 → 행 선수는 「${G.r[brRow(step - 1)]}」 (${m[brRow(step - 1)][step - 1][0]} > ${m[1 - brRow(step - 1)][step - 1][0]}${m[0][step - 1][0] === m[1][step - 1][0] ? ", 같음" : ""})` :
    step <= 4 ? `행 선수가 「${G.r[step - 3]}」 하면 → 열 선수는 「${G.c[brCol(step - 3)]}」 (${m[step - 3][brCol(step - 3)][1]} > ${m[step - 3][1 - brCol(step - 3)][1]})` :
    ne.length ? `둘 다 최선 반응인 칸 = 내시 균형: ${ne.map(([i, j]) => `(${G.r[i]}, ${G.c[j]})`).join(" · ")}` : "둘 다 최선 반응인 칸이 없다 — 화살표가 빙빙 돈다";
  return (
    <Frame clock={clock} title={"내시 균형 — " + G.name}
      read={<>{say} · {G.say} · 화살표 = 한쪽이 혼자 바꾸면 더 나아지는 쪽(균형에서는 아무도 혼자 바꿀 까닭이 없다)</>}
      controls={<Seg value={g} onChange={(v) => { setG(v); clock.reset(); }} options={[["pd", "죄수"], ["stag", "사슴"], ["chicken", "치킨"], ["sexes", "성 대결"], ["pennies", "동전"]]} />}>
      {G.c.map((c, j) => <text key={j} x={cx(j)} y={y0 - 8} textAnchor="middle" fontSize="11" fontWeight="800" fill={C.gold}>{c}</text>)}
      {G.r.map((r, i) => <text key={i} x={x0 - 8} y={cy(i) + 4} textAnchor="end" fontSize="11" fontWeight="800" fill={C.blue}>{r}</text>)}
      <text x={x0 - 8} y={y0 - 8} textAnchor="end" fontSize="9" fill={C.mut}>행 \ 열</text>
      {[0, 1].map((i) => [0, 1].map((j) => {
        const isNE = step >= 5 && ne.some(([a, b]) => a === i && b === j);
        return (
          <g key={i + "" + j}>
            <rect x={x0 + cw * j} y={y0 + ch * i} width={cw} height={ch} fill={isNE ? "color-mix(in srgb, #3f7d3a 14%, transparent)" : C.card} stroke={isNE ? C.green : C.bd} strokeWidth={isNE ? 3 : 1.2} />
            <text x={cx(j) - 16} y={cy(i) + 6} textAnchor="middle" fontSize="17" fontWeight="800" fill={C.blue}>{m[i][j][0]}</text>
            <text x={cx(j)} y={cy(i) + 6} textAnchor="middle" fontSize="15" fill={C.mut}>,</text>
            <text x={cx(j) + 16} y={cy(i) + 6} textAnchor="middle" fontSize="17" fontWeight="800" fill={C.gold}>{m[i][j][1]}</text>
            {showR(j) && (brRow(j) === i || m[0][j][0] === m[1][j][0]) && <circle cx={cx(j) - 16} cy={cy(i)} r="13" fill="none" stroke={C.blue} strokeWidth="2" />}
            {showC(i) && (brCol(i) === j || m[i][0][1] === m[i][1][1]) && <circle cx={cx(j) + 16} cy={cy(i)} r="13" fill="none" stroke={C.gold} strokeWidth="2" />}
          </g>
        );
      }))}
      {step >= 5 && [0, 1].map((i) => [0, 1].map((j) => {
        const out = [];
        if (m[1 - i][j][0] > m[i][j][0]) out.push(<Arrow key={"r" + i + j} x1={cx(j) - 34} y1={cy(i) + (i ? -16 : 16)} x2={cx(j) - 34} y2={cy(1 - i) + (i ? 16 : -16)} color={C.blue} w={1.6} head={5} />);
        if (m[i][1 - j][1] > m[i][j][1]) out.push(<Arrow key={"c" + i + j} x1={cx(j) + (j ? -40 : 40)} y1={cy(i) + 22} x2={cx(1 - j) + (j ? 40 : -40)} y2={cy(i) + 22} color={C.gold} w={1.6} head={5} />);
        return out;
      }))}
    </Frame>
  );
}

/* ── 혼합 전략: 상대를 무차별하게 만드는 확률 — 최선 반응 그래프의 만남 ── */
export function Mixed({ p = {} }) {
  const [g, setG] = useState(["pennies", "sexes", "chicken"].includes(p.game) ? p.game : "sexes");
  const clock = useClock({ period: 10, rest: 3 });
  const m = GAMES[g].m, G = GAMES[g];
  const q = 0.5 - 0.5 * Math.cos((2 * Math.PI * clock.t) / 10);
  const eR = (a, qq) => qq * m[a][0][0] + (1 - qq) * m[a][1][0];
  const eC = (b, pp) => pp * m[0][b][1] + (1 - pp) * m[1][b][1];
  const qs = (m[1][1][0] - m[0][1][0]) / (m[0][0][0] - m[0][1][0] - m[1][0][0] + m[1][1][0]);
  const ps = (m[1][1][1] - m[1][0][1]) / (m[0][0][1] - m[1][0][1] - m[0][1][1] + m[1][1][1]);
  const all = [m[0][0][0], m[0][1][0], m[1][0][0], m[1][1][0]];
  const lo = Math.min(...all) - 0.5, hi = Math.max(...all) + 0.5;
  const P = plot({ x0: 0, x1: 1, y0: lo, y1: hi, pad: [14, 196, 26, 30] });
  const S = plot({ x0: 0, x1: 1, y0: 0, y1: 1, pad: [14, 14, 26, 214] });
  const brR = (qq) => (eR(0, qq) > eR(1, qq) + 1e-9 ? 1 : eR(0, qq) < eR(1, qq) - 1e-9 ? 0 : null);
  const brC = (pp) => (eC(0, pp) > eC(1, pp) + 1e-9 ? 1 : eC(0, pp) < eC(1, pp) - 1e-9 ? 0 : null);
  const rowPts = [[brR(0.001), 0], [brR(0.001), qs], [brR(0.999), qs], [brR(0.999), 1]];
  const colPts = [[0, brC(0.001)], [ps, brC(0.001)], [ps, brC(0.999)], [1, brC(0.999)]];
  const ne = [...nashCells(m).map(([i, j]) => [i === 0 ? 1 : 0, j === 0 ? 1 : 0]), ...(qs > 0 && qs < 1 && ps > 0 && ps < 1 ? [[ps, qs]] : [])];
  const better = eR(0, q) > eR(1, q) + 1e-9 ? G.r[0] : eR(0, q) < eR(1, q) - 1e-9 ? G.r[1] : "아무거나";
  return (
    <Frame clock={clock} title={"혼합 전략 — " + G.name}
      read={<>열 선수가 「{G.c[0]}」 을 확률 q = <b>{fmt(q, 2)}</b> 로 내면: 행 선수의 「{G.r[0]}」 기대보수 {fmt(eR(0, q), 2)}, 「{G.r[1]}」 {fmt(eR(1, q), 2)} → <b>{better}</b> · q* = {fmt(qs, 2)} 에서 두 직선이 만나 행 선수는 무엇을 해도 같다 · 혼합 균형 (p*, q*) = (<b>{fmt(ps, 2)}</b>, <b>{fmt(qs, 2)}</b>) — 각자 상대를 무차별하게 만드는 확률을 쓴다 · 오른쪽: 최선 반응 그래프가 만나는 점 = 균형(초록)</>}
      controls={<Seg value={g} onChange={setG} options={[["sexes", "성 대결"], ["pennies", "동전"], ["chicken", "치킨"]]} />}>
      <Axes p={P} xl="q" yl="기대보수" grid={false} xt={[0.5, 1]} />
      <path d={P.path((x) => eR(0, x), 0, 1)} fill="none" stroke={C.blue} strokeWidth="2.2" />
      <path d={P.path((x) => eR(1, x), 0, 1)} fill="none" stroke={C.violet} strokeWidth="2.2" strokeDasharray="5 3" />
      <line x1={P.X(qs)} x2={P.X(qs)} y1={P.t} y2={P.b} stroke={C.green} strokeDasharray="3 3" />
      <line x1={P.X(q)} x2={P.X(q)} y1={P.t} y2={P.b} stroke={C.mut} strokeWidth="0.8" />
      <circle cx={P.X(q)} cy={P.Y(eR(0, q))} r="4" fill={C.blue} />
      <circle cx={P.X(q)} cy={P.Y(eR(1, q))} r="4" fill={C.violet} />
      <Label x={P.X(0.02) + 2} y={P.Y(eR(0, 0.02)) - 5} size={9.5} color={C.blue} bg>{G.r[0]}</Label>
      <Label x={P.X(0.98)} y={P.Y(eR(1, 0.98)) - 5} size={9.5} color={C.violet} anchor="end" bg>{G.r[1]}</Label>
      <Axes p={S} xl="p" yl="q" grid={false} xt={[0.5, 1]} yt={[0.5, 1]} />
      <rect x={S.l} y={S.t} width={S.r - S.l} height={S.b - S.t} fill="none" stroke={C.bd} />
      <path d={S.poly(rowPts)} fill="none" stroke={C.blue} strokeWidth="2.4" />
      <path d={S.poly(colPts)} fill="none" stroke={C.gold} strokeWidth="2.4" strokeDasharray="6 3" />
      {ne.map(([a, b], k) => <circle key={k} cx={S.X(a)} cy={S.Y(b)} r="5.5" fill={C.green} />)}
    </Frame>
  );
}

/* ── 역진 귀납: 끝에서부터 거꾸로 — 믿을 수 없는 위협은 걸러진다 ── */
export function Backward({ p = {} }) {
  const [g, setG] = useState(p.game === "centipede" ? "centipede" : "entry");
  const clock = useClock({ period: 9, rest: 8.5 });
  if (g === "entry") {
    const st = clock.t < 2 ? 0 : clock.t < 4.5 ? 1 : 2;
    const node = (x, y, s, col) => <g><circle cx={x} cy={y} r="18" fill={C.card} stroke={col} strokeWidth="2" /><text x={x} y={y + 4} textAnchor="middle" fontSize="10" fontWeight="800" fill={col}>{s}</text></g>;
    const leaf = (x, y, a, b) => <text x={x} y={y} textAnchor="middle" fontSize="12" fontWeight="800"><tspan fill={C.blue}>{a}</tspan><tspan fill={C.mut}>, </tspan><tspan fill={C.gold}>{b}</tspan></text>;
    return (
      <Frame clock={clock} title="역진 귀납 — 진입 게임"
        read={<>{st === 0 ? "새 기업(파랑)이 들어갈지 정하고, 들어오면 기존 기업(노랑)이 싸울지 나눌지 정한다 — 보수는 (새 기업, 기존 기업)" : st === 1 ? "끝에서부터: 들어온 뒤라면 기존 기업은 싸우면 1, 나누면 2 → 나눈다" : "그걸 아는 새 기업은 들어간다(2 > 0) — 부분게임 완전균형 (들어감, 나눔)"} · 「들어오면 싸우겠다」는 위협은 막상 그 순간이 오면 손해라 믿을 수 없다 — 믿게 하려면 미리 손을 묶는 약속(설비 투자 등)이 필요하다</>}
        controls={<Seg value={g} onChange={(v) => { setG(v); clock.reset(); }} options={[["entry", "진입 게임"], ["centipede", "지네 게임"]]} />}>
        <line x1="70" y1="110" x2="160" y2="172" stroke={st >= 2 ? C.mut : C.ink} strokeWidth={st >= 2 ? 1.2 : 2} strokeDasharray={st >= 2 ? "4 3" : ""} />
        <line x1="70" y1="110" x2="186" y2="66" stroke={st >= 2 ? C.green : C.ink} strokeWidth={st >= 2 ? 3.5 : 2} />
        <line x1="186" y1="66" x2="300" y2="34" stroke={st >= 1 ? C.mut : C.ink} strokeWidth={st >= 1 ? 1.2 : 2} strokeDasharray={st >= 1 ? "4 3" : ""} />
        <line x1="186" y1="66" x2="300" y2="124" stroke={st >= 1 ? C.green : C.ink} strokeWidth={st >= 1 ? 3.5 : 2} />
        {node(70, 110, "새", C.blue)}{node(186, 66, "기존", C.gold)}
        <text x="104" y="160" fontSize="10" fill={C.ink}>안 들어감</text><text x="112" y="78" fontSize="10" fill={C.ink}>들어감</text>
        <text x="236" y="40" fontSize="10" fill={C.ink}>싸움</text><text x="236" y="112" fontSize="10" fill={C.ink}>나눔</text>
        {leaf(172, 194, 0, 4)}{leaf(326, 38, -1, 1)}{leaf(326, 128, 2, 2)}
        {st >= 1 && <text x="186" y="100" textAnchor="middle" fontSize="10" fill={C.green}>→ (2, 2)</text>}
      </Frame>
    );
  }
  const PAY = [[1, 0], [0, 2], [3, 1], [2, 4], [5, 3], [4, 6]], END = [6, 5];
  const k = clock.t < 1.2 ? 6 : Math.max(0, 6 - Math.floor((clock.t - 1.2) / 0.9) - 1);
  const X = (i) => 34 + i * 52;
  return (
    <Frame clock={clock} title="역진 귀납 — 지네 게임"
      read={<>A(파랑)와 B(노랑)가 번갈아 「가져감」(아래, 게임 끝)과 「넘김」(오른쪽, 판이 커짐)을 고른다 · 끝에서부터: B 는 마지막에 가져간다(6 &gt; 5) → 그걸 아는 A 는 그 앞에서 가져간다(5 &gt; 4) → … → {k === 0 ? <><b>A 가 첫 수에 바로 가져간다(1, 0)</b> — (6, 5) 가 가능한데도!</> : "거꾸로 따라가는 중"} · 실험에서 사람들은 꽤 오래 넘긴다 — 상대도 합리적이라는 믿음이 몇 단계나 이어져야 하기 때문</>}
      controls={<Seg value={g} onChange={(v) => { setG(v); clock.reset(); }} options={[["entry", "진입 게임"], ["centipede", "지네 게임"]]} />}>
      <line x1={X(5)} y1="70" x2="338" y2="70" stroke={k <= 5 ? C.mut : C.ink} strokeWidth="1.6" strokeDasharray={k <= 5 ? "4 3" : ""} />
      {PAY.map(([a, b], i) => {
        const decided = i >= k;
        return (
          <g key={i}>
            {i < 5 && <line x1={X(i)} y1="70" x2={X(i + 1)} y2="70" stroke={decided ? C.mut : C.ink} strokeWidth="1.6" strokeDasharray={decided ? "4 3" : ""} />}
            <line x1={X(i)} y1="70" x2={X(i)} y2="140" stroke={decided ? C.green : C.ink} strokeWidth={decided ? 3.4 : 1.6} />
            <circle cx={X(i)} cy="70" r="13" fill={C.card} stroke={i % 2 ? C.gold : C.blue} strokeWidth="2" />
            <text x={X(i)} y="74" textAnchor="middle" fontSize="10" fontWeight="800" fill={i % 2 ? C.gold : C.blue}>{i % 2 ? "B" : "A"}</text>
            <text x={X(i)} y="158" textAnchor="middle" fontSize="11" fontWeight="800"><tspan fill={C.blue}>{a}</tspan><tspan fill={C.mut}>,</tspan><tspan fill={C.gold}>{b}</tspan></text>
          </g>
        );
      })}
      <text x="342" y="66" textAnchor="end" fontSize="11" fontWeight="800"><tspan fill={C.blue}>{END[0]}</tspan><tspan fill={C.mut}>,</tspan><tspan fill={C.gold}>{END[1]}</tspan></text>
      <text x="34" y="190" fontSize="9.5" fill={C.mut}>아래 = 가져감(끝) · 오른쪽 = 넘김 · 초록 = 역진 귀납이 고른 수</text>
    </Frame>
  );
}

/* ── 반복 죄수의 딜레마 대회: 착하고 · 보복하고 · 용서하는 전략이 이긴다 ── */
const STRATS = [
  ["팃포탯", (me, op) => (op.length ? op[op.length - 1] : 0)],
  ["항상 협력", () => 0],
  ["항상 배신", () => 1],
  ["그러지", (me, op) => (op.includes(1) ? 1 : 0)],
  ["무작위", (me, op, r) => (r() < 0.5 ? 1 : 0)],
  ["파블로프", (me, op) => (!me.length ? 0 : me[me.length - 1] === op[op.length - 1] ? 0 : 1)],
];
const PD = [[3, 0], [5, 1]]; // PD[내 행동][상대 행동] — 0 협력, 1 배신
export function Repeated({ p = {} }) {
  const [noise, setNoise] = useState(p.noise ?? 0);
  const clock = useClock({ period: 12, rest: 11 });
  const R = 60;
  const cum = useMemo(() => {
    const r = rng(41), n = STRATS.length, sc = Array.from({ length: n }, () => Array(R + 1).fill(0));
    for (let a = 0; a < n; a++) for (let b = a; b < n; b++) {
      const ha = [], hb = [];
      let sa = 0, sb = 0;
      for (let t = 0; t < R; t++) {
        let x = STRATS[a][1](ha, hb, r), y = STRATS[b][1](hb, ha, r);
        if (r() < noise / 100) x = 1 - x;
        if (r() < noise / 100) y = 1 - y;
        ha.push(x); hb.push(y);
        sa += PD[x][y]; sb += PD[y][x];
        sc[a][t + 1] += sa; if (a !== b) sc[b][t + 1] += sb;
      }
    }
    return sc;
  }, [noise]);
  const t = Math.max(1, Math.min(R, Math.round(clamp(clock.t / 10, 0, 1) * R)));
  const n = STRATS.length;
  const avg = STRATS.map((s, i) => ({ name: s[0], v: cum[i][t] / (n * t) }));
  const order = avg.slice().sort((x, y) => y.v - x.v);
  return (
    <Frame clock={clock} title="반복 죄수의 딜레마 대회"
      read={<>여섯 전략이 서로(자기 자신과도) {R} 판씩 · {t} 판까지 한 판 평균 점수 — 1 위 <b>{order[0].name}</b> {fmt(order[0].v, 2)}(누가 이기는지는 참가자 구성에 달렸다) · 보수: 둘 다 협력 3, 둘 다 배신 1, 혼자 배신 5, 당하면 0 · 팃포탯은 먼저 배신하지 않고(착함), 배신엔 바로 갚고(보복), 다시 협력하면 용서한다 · 잡음 {noise} %: 실수 한 번에 팃포탯끼리 보복이 이어진다 — 파블로프(이기면 그대로, 지면 바꿈)는 실수에서 빨리 회복한다</>}
      controls={<Slider label="실수(잡음)" min={0} max={10} step={1} value={noise} onChange={setNoise} show={(x) => x + " %"} />}>
      {order.map((o, k) => {
        const y = 26 + k * 30, w = (o.v / 3.2) * 210;
        return (
          <g key={o.name}>
            <text x="86" y={y + 15} textAnchor="end" fontSize="11" fontWeight={k === 0 ? 800 : 500} fill={C.ink}>{o.name}</text>
            <rect x="94" y={y + 3} width={Math.max(0, w)} height="18" rx="3" fill={k === 0 ? C.sp : C.mut} opacity={k === 0 ? 0.9 : 0.55} />
            <text x={100 + Math.max(0, w)} y={y + 16} fontSize="10.5" fill={C.ink}>{fmt(o.v, 2)}</text>
          </g>
        );
      })}
      <line x1={94 + (3 / 3.2) * 210} x2={94 + (3 / 3.2) * 210} y1="22" y2="206" stroke={C.green} strokeDasharray="3 3" />
      <text x={94 + (3 / 3.2) * 210} y="216" textAnchor="middle" fontSize="9" fill={C.green}>늘 협력 3</text>
    </Frame>
  );
}

/* ── 매-비둘기: 싸우는 쪽(매)과 양보하는 쪽(비둘기)의 비율이 V/C 로 모인다 — 진화적으로 안정한 상태 ── */
export function HawkDove({ p = {} }) {
  const [V, setV] = useState(p.V ?? 4);
  const [Cc, setCc] = useState(p.C ?? 10);
  const clock = useClock({ period: 11, rest: 10 });
  const sims = useMemo(() => [0.05, 0.5, 0.95].map((x0) => {
    const out = [x0]; let x = x0;
    for (let i = 0; i < 600; i++) { const ph = x * (V - Cc) / 2 + (1 - x) * V, pd = (1 - x) * V / 2; x = clamp(x + 0.05 * x * (1 - x) * (ph - pd) * 0.6, 0, 1); out.push(x); }
    return out;
  }), [V, Cc]);
  const i = Math.min(600, Math.round(clamp(clock.t / 9, 0, 1) * 600));
  const P = plot({ x0: 0, x1: 30, y0: 0, y1: 1, pad: [12, 150, 24, 32] });
  const star = V < Cc ? V / Cc : 1, xm = sims[1][i];
  const nh = Math.round(xm * 100);
  return (
    <Frame clock={clock} title="매-비둘기 게임과 진화"
      read={<>자원 값 V = {V}, 싸움 비용 C = {Cc} · 매끼리는 싸워 (V − C)/2, 매는 비둘기에게서 V 를 빼앗고, 비둘기끼리는 V/2 씩 나눈다 · 더 버는 쪽이 늘어난다(복제자 동학) → {V < Cc ? <>매의 비율이 <b>V/C = {fmt(star, 2)}</b> 로 모인다 — 진화적으로 안정한 상태(ESS): 매가 많으면 싸움 비용 때문에 비둘기가, 적으면 매가 더 번다</> : <>V ≥ C 면 싸워도 남는 장사라 <b>매가 다 차지한다</b></>} · 지금 매 {nh} %</>}
      controls={<>
        <Slider label="자원 V" min={1} max={10} step={1} value={V} onChange={(v) => { setV(v); clock.reset(); }} />
        <Slider label="싸움 비용 C" min={2} max={20} step={1} value={Cc} onChange={(v) => { setCc(v); clock.reset(); }} />
      </>}>
      <Axes p={P} xl="세대" yl="매 비율" xt={[10, 20, 30]} yt={[0.5, 1]} />
      <line x1={P.l} x2={P.r} y1={P.Y(star)} y2={P.Y(star)} stroke={C.green} strokeDasharray="4 3" />
      {sims.map((s, k) => <path key={k} d={P.poly(s.slice(0, i + 1).filter((_, j) => j % 4 === 0 || j === i).map((x, j, arr) => [j === arr.length - 1 ? i * 0.05 : j * 0.2, x]))} fill="none" stroke={k === 1 ? C.red : C.mut} strokeWidth={k === 1 ? 2.4 : 1.5} />)}
      <Label x={P.r - 4} y={P.Y(star) - 5} size={9.5} color={C.green} anchor="end" bg>V/C</Label>
      {Array.from({ length: 100 }, (_, k) => <circle key={k} cx={232 + (k % 10) * 12} cy={36 + Math.floor(k / 10) * 15} r="4.5" fill={k < nh ? C.red : C.blue} opacity="0.85" />)}
      <text x="292" y="200" textAnchor="middle" fontSize="9.5" fill={C.mut}><tspan fill={C.red}>●</tspan> 매 · <tspan fill={C.blue}>●</tspan> 비둘기</text>
    </Frame>
  );
}

/* ── 쿠르노 과점: 서로의 생산량에 최선 반응을 주고받으면 균형으로 ── */
export function Cournot({ p = {} }) {
  const [c, setC] = useState(p.c ?? 0);
  const clock = useClock({ period: 10, rest: 9.5 });
  const a = 12, A = a - c, qs = A / 3;
  const path = useMemo(() => {
    const pts = []; let q1 = A / 2, q2 = 0; pts.push([q1, q2]);
    for (let k = 0; k < 8; k++) { q2 = (A - q1) / 2; pts.push([q1, q2]); q1 = (A - q2) / 2; pts.push([q1, q2]); }
    return pts;
  }, [c]); // eslint-disable-line react-hooks/exhaustive-deps
  const k = Math.min(path.length - 1, Math.floor(clock.t / 0.55));
  const P = plot({ x0: 0, x1: 12.5, y0: 0, y1: 12.5, pad: [12, 128, 24, 30] });
  const pr = a - 2 * qs;
  return (
    <Frame clock={clock} title="쿠르노 과점"
      read={<>수요 P = 12 − (q₁ + q₂), 한계비용 {c} · 각 기업의 최선 반응 qᵢ = (12 − c − qⱼ)/2 · 독점에서 시작해 번갈아 맞추면 (<b>{fmt(qs, 2)}</b>, <b>{fmt(qs, 2)}</b>) 로 모인다 — 쿠르노 균형, 값 {fmt(pr, 2)} · 비교: 독점이면 총 {fmt(A / 2, 1)} · 값 {fmt((a + c) / 2, 1)}, 완전경쟁이면 총 {fmt(A, 1)} · 값 {c} — 기업이 n 개면 값 (12 + nc)/(n + 1) 이 한계비용으로 다가간다</>}
      controls={<Slider label="한계비용 c" min={0} max={6} step={0.5} value={c} onChange={(v) => { setC(v); clock.reset(); }} />}>
      <Axes p={P} xl="q₁" yl="q₂" />
      <path d={P.poly([[A / 2, 0], [0, A]])} fill="none" stroke={C.blue} strokeWidth="2.2" />
      <path d={P.poly([[0, A / 2], [A, 0]])} fill="none" stroke={C.gold} strokeWidth="2.2" />
      <path d={P.poly([[A / 2, 0], [0, A / 2]])} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />
      <path d={P.poly(path.slice(0, k + 1))} fill="none" stroke={C.red} strokeWidth="1.6" />
      <circle cx={P.X(path[k][0])} cy={P.Y(path[k][1])} r="4.5" fill={C.red} />
      <circle cx={P.X(qs)} cy={P.Y(qs)} r="4" fill="none" stroke={C.green} strokeWidth="2" />
      <Label x={P.X((A - 0.75 * A) / 2) + 8} y={P.Y(0.75 * A) + 4} size={9.5} color={C.blue} bg>기업 1 의 반응</Label>
      <Label x={P.X(A - 0.4)} y={P.Y(0.9) - 4} size={9.5} color={C.gold} anchor="end" bg>기업 2 의 반응</Label>
      <Label x={P.X(0.3)} y={P.Y(A / 2 - 0.3) + 12} size={9} color={C.mut} bg>독점 총량</Label>
      <text x="252" y="40" fontSize="10" fill={C.ink}>값 비교</text>
      {[["독점", (a + c) / 2], ["쿠르노", pr], ["경쟁", c]].map(([n, v], j) => (
        <g key={n}><rect x="252" y={52 + j * 40} width={(v / 12) * 96} height="16" fill={[C.red, C.sp, C.green][j]} opacity="0.7" /><text x="252" y={80 + j * 40} fontSize="9.5" fill={C.ink}>{n} {fmt(v, 1)}</text></g>
      ))}
    </Frame>
  );
}

/* ── 경매: 둘째 가격은 정직하게, 첫째 가격은 깎아서 — 평균 판매가는 같다(수입 동등) ── */
export function Auction({ p = {} }) {
  const [N, setN] = useState(p.N ?? 4);
  const [fmtA, setFmtA] = useState(p.first ? "first" : "second");
  const clock = useClock({ period: 24, rest: 23 });
  const rounds = useMemo(() => {
    const r = rng(77), out = [];
    for (let k = 0; k < 40; k++) { const v = Array.from({ length: N }, () => r() * 100); const s = v.slice().sort((a, b) => b - a); out.push({ v, first: s[0] * (N - 1) / N, second: s[1] }); }
    return out;
  }, [N]);
  const k = Math.min(39, Math.floor(clock.t / 0.55));
  const R = rounds[k], first = fmtA === "first";
  const avg = (key) => rounds.slice(0, k + 1).reduce((s, x) => s + x[key], 0) / (k + 1);
  const theory = ((N - 1) / (N + 1)) * 100;
  const win = R.v.indexOf(Math.max(...R.v));
  const P = plot({ x0: 0, x1: 40, y0: 0, y1: 100, pad: [14, 12, 24, 204] });
  const avgLine = (key) => rounds.slice(0, k + 1).map((_, j) => [j + 1, rounds.slice(0, j + 1).reduce((s, x) => s + x[key], 0) / (j + 1)]);
  return (
    <Frame clock={clock} title="경매와 수입 동등"
      read={<>입찰자 {N} 명, 가치는 0 ~ 100 고르게 · {k + 1} 번째 경매: {first ? <>첫째 가격 — 이긴 사람이 써낸 값을 낸다 → 가치의 (N − 1)/N 만 써낸다(깎아 쓰기), 판매가 {fmt(R.first, 1)}</> : <>둘째 가격 — 이긴 사람이 둘째로 높은 값을 낸다 → 자기 가치대로 써내는 것이 우월전략, 판매가 {fmt(R.second, 1)}</>} · 평균 판매가: 첫째 {fmt(avg("first"), 1)}, 둘째 {fmt(avg("second"), 1)} → 둘 다 (N − 1)/(N + 1) × 100 = <b>{fmt(theory, 1)}</b> (수입 동등 정리)</>}
      controls={<>
        <Slider label="입찰자 수" min={2} max={8} step={1} value={N} onChange={(v) => { setN(v); clock.reset(); }} />
        <Seg value={fmtA} onChange={setFmtA} options={[["second", "둘째 가격"], ["first", "첫째 가격"]]} />
      </>}>
      {R.v.map((v, j) => {
        const bid = first ? v * (N - 1) / N : v, y = 22 + j * (170 / N), h = Math.min(18, 170 / N - 4);
        return (
          <g key={j}>
            <rect x="24" y={y} width={v * 1.5} height={h} fill="none" stroke={C.mut} strokeDasharray="3 2" />
            <rect x="24" y={y} width={bid * 1.5} height={h} fill={j === win ? C.sp : C.mut} opacity={j === win ? 0.85 : 0.45} />
            <text x="18" y={y + h - 4} textAnchor="end" fontSize="9" fill={C.ink}>{j + 1}</text>
          </g>
        );
      })}
      <line x1={24 + (first ? R.first : R.second) * 1.5} x2={24 + (first ? R.first : R.second) * 1.5} y1="18" y2="196" stroke={C.red} strokeWidth="1.5" />
      <text x="24" y="210" fontSize="9.5" fill={C.mut}>점선 = 가치, 막대 = 써낸 값, 빨강 = 판매가</text>
      <Axes p={P} xl="경매" yl="평균 판매가" grid={false} xt={[20, 40]} yt={[50, 100]} xfmt={(x) => fmt(x, 0)} />
      <line x1={P.l} x2={P.r} y1={P.Y(theory)} y2={P.Y(theory)} stroke={C.green} strokeDasharray="4 3" />
      <path d={P.poly(avgLine("first"))} fill="none" stroke={C.gold} strokeWidth="1.8" />
      <path d={P.poly(avgLine("second"))} fill="none" stroke={C.blue} strokeWidth="1.8" />
      <Label x={P.r - 2} y={P.Y(theory) - 5} size={9} color={C.green} anchor="end" bg>이론값</Label>
    </Frame>
  );
}
