// 음악 그림 — 맥놀이 · 배음과 음색 · 현과 관의 정상파 · 피타고라스 콤마와 센트 · 협화 곡선 · 유클리드 리듬 · 12 음 시계(Z₁₂) · 디지털 오디오(양자화 · 엘리어싱)
import { useMemo, useState } from "react";
import { C, Frame, Slider, Seg, plot, Arrow, Label, fmt, clamp, useClock } from "./kit.jsx";

const TAU = 2 * Math.PI;
const pth = (pts) => pts.map(([x, y], i) => (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1)).join("") || "M0 0";
const NOTE = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"];

/* ── 맥놀이: 가까운 두 음이 만드는 소리의 너울 ── */
export function Beats({ p = {} }) {
  const [d, setD] = useState(clamp(p.d ?? 2, 0.5, 6));
  const clock = useClock({ period: 8, rest: 1.3 });
  const ph = clock.t % 2;
  const P = plot({ x0: 0, x1: 2, y0: -2.3, y1: 2.3, pad: [16, 10, 30, 150] });
  const wave = useMemo(() => pth(Array.from({ length: 1201 }, (_, i) => { const t = (i / 1200) * 2; return [P.X(t), P.Y(2 * Math.cos(Math.PI * d * t) * Math.sin(TAU * 21 * t))]; })), [d]);
  const env = (t) => 2 * Math.abs(Math.cos(Math.PI * d * t));
  const th = TAU * d * ph, O = [40, 112], R = 33;
  const v1 = [O[0] + R, O[1]], v2 = [v1[0] + R * Math.cos(th), v1[1] - R * Math.sin(th)];
  return (
    <Frame clock={clock} title="맥놀이 — 가까운 두 음은 너울진다"
      read={<>440 Hz 와 {fmt(440 + d, 2)} Hz 를 함께 울리면 두 파동이 맞았다(보강) 어긋났다(상쇄)를 되풀이해 1 초에 <b>{fmt(d, 2)} 번</b> 소리가 커졌다 작아진다 — 맥놀이 · sin a + sin b = 2 cos((a − b) ÷ 2) sin((a + b) ÷ 2): 평균 진동수 {fmt(440 + d / 2, 2)} Hz 의 소리가 진폭 2cos(πΔf t) 로 흔들린다 · 왼쪽: 첫째 파동(파랑)과 함께 도는 눈으로 보면 둘째 파동(빨강)이 1 초에 Δf 바퀴 돌고, 합(보라)의 길이가 곧 소리의 세기 · 조율사는 맥놀이가 느려져 사라질 때까지 줄을 조인다</>}
      controls={<Slider label="진동수 차 Δf" min={0.5} max={6} step={0.5} value={d} onChange={setD} show={(v) => `${fmt(v, 1)} Hz`} />}>
      <circle cx={v1[0]} cy={v1[1]} r={R} fill="none" stroke={C.bd} strokeDasharray="3 3" />
      <Arrow x1={O[0]} y1={O[1]} x2={v1[0]} y2={v1[1]} color={C.blue} w={2.2} />
      <Arrow x1={v1[0]} y1={v1[1]} x2={v2[0]} y2={v2[1]} color={C.red} w={2.2} />
      <Arrow x1={O[0]} y1={O[1]} x2={v2[0]} y2={v2[1]} color={C.violet} w={2.6} />
      <circle cx={O[0]} cy={O[1]} r="2.5" fill={C.ink} />
      <text x="74" y="32" textAnchor="middle" fontSize="10" fill={C.ink}>두 파동의 화살표</text>
      <text x="74" y="186" textAnchor="middle" fontSize="9.5" fill={C.violet}>보라 길이 = 소리 세기</text>
      <text x="74" y="200" textAnchor="middle" fontSize="9.5" fill={C.violet}>{fmt(env(ph), 2)} (최대 2)</text>
      <path d={P.path(env, 0, 2, 300)} fill="none" stroke={C.violet} strokeWidth="1.2" strokeDasharray="4 3" />
      <path d={P.path((t) => -env(t), 0, 2, 300)} fill="none" stroke={C.violet} strokeWidth="1.2" strokeDasharray="4 3" />
      <path d={wave} fill="none" stroke={C.ink} strokeWidth="0.7" opacity="0.75" />
      <line x1={P.X(ph)} x2={P.X(ph)} y1={P.t} y2={P.b} stroke={C.red} strokeWidth="1.4" />
      <circle cx={P.X(ph)} cy={P.Y(env(ph))} r="4" fill={C.violet} />
      <line x1={P.l} x2={P.r} y1={P.b + 4} y2={P.b + 4} stroke={C.mut} />
      {[0, 1, 2].map((s) => <text key={s} x={P.X(s)} y={P.b + 17} textAnchor={s ? (s === 2 ? "end" : "middle") : "start"} fontSize="9" fill={C.mut}>{s ? `${s} 초` : "0"}</text>)}
      <text x={P.l} y={P.t - 4} fontSize="9" fill={C.mut}>합친 소리(파형은 느리게 그림)</text>
    </Frame>
  );
}

/* ── 배음과 음색: 푸리에 합성 ── */
const TIMB = {
  sine: { name: "사인파", a: (n) => (n === 1 ? 1 : 0), ideal: null, desc: "배음이 없는 순수한 사인파 — 소리굽쇠나 휘파람 소리에 가깝다" },
  odd: { name: "홀수 배음", a: (n) => (n % 2 ? 1 / n : 0), ideal: (x) => (Math.PI / 4) * Math.sign(Math.sin(x)), desc: "홀수 배음만 1, 1/3, 1/5 … 의 세기로 더하면 네모파(점선)에 다가간다 — 낮은 음역의 클라리넷 소리에 가깝다 · 모서리 옆의 뾰족한 튀어나옴(약 9 %)은 배음을 아무리 더해도 남는다(깁스 현상)" },
  saw: { name: "모든 배음", a: (n) => 1 / n, ideal: (x) => { const u = ((x % TAU) + TAU) % TAU; return (Math.PI - u) / 2; }, desc: "모든 배음을 1, 1/2, 1/3 … 의 세기로 더하면 톱니파(점선)에 다가간다 — 활로 켠 바이올린 줄의 소리와 닮았다" },
  flute: { name: "부드러운 소리", a: (n) => [1, 0.35, 0.12, 0.05, 0.02][n - 1] || 0, ideal: null, desc: "기본음이 강하고 배음이 빠르게 약해진다(세기는 어림값) — 사인파에 가까운 플루트 소리" },
};
export function Timbre({ p = {} }) {
  const [w, setW] = useState(TIMB[p.w] ? p.w : "odd");
  const clock = useClock({ period: 11, rest: 10.5 });
  const T = TIMB[w], k = clamp(1 + Math.floor(clock.t / 0.75), 1, 12);
  const sum = (x, kk) => { let s = 0; for (let n = 1; n <= kk; n++) s += T.a(n) * Math.sin(n * x); return s; };
  const ymax = useMemo(() => { let m = 0; for (let i = 0; i <= 400; i++) m = Math.max(m, Math.abs(sum((i / 400) * TAU, 12))); return m * 1.2; }, [w]);
  const P = plot({ x0: 0, x1: 4 * Math.PI, y0: -ymax, y1: ymax, pad: [16, 136, 26, 10] });
  const Q = plot({ x0: 0.4, x1: 12.6, y0: 0, y1: 1.12, pad: [24, 8, 26, 236] });
  return (
    <Frame clock={clock} title="배음과 음색 — 사인파를 쌓아 소리를 만든다"
      read={<>{T.name}: 기본음(1 번)에 배음을 차례로 더한다 — 지금 {w === "sine" ? "배음 없음" : `${k} 번 배음까지`} · {T.desc} · 같은 높이(기본 진동수)의 소리라도 배음의 세기(오른쪽 막대)가 다르면 파형과 음색이 다르다</>}
      controls={<Seg value={w} onChange={(v) => { setW(v); clock.reset(); }} options={[["sine", "사인파"], ["odd", "홀수 배음"], ["saw", "모든 배음"], ["flute", "플루트"]]} />}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.bd} />
      {T.ideal && <path d={P.path(T.ideal, 0, 4 * Math.PI, 800)} fill="none" stroke={C.mut} strokeWidth="1.2" strokeDasharray="4 3" />}
      <path d={P.path((x) => sum(x, k), 0, 4 * Math.PI, 500)} fill="none" stroke={C.red} strokeWidth="2" />
      <text x={P.l} y={P.t - 4} fontSize="9" fill={C.mut}>파형(두 주기)</text>
      <text x={Q.l} y={Q.t - 8} fontSize="9" fill={C.mut}>배음의 세기</text>
      {Array.from({ length: 12 }, (_, i) => {
        const n = i + 1, a = T.a(n), bw = 6.4;
        return (
          <g key={n}>
            <rect x={Q.X(n) - bw / 2} y={Q.Y(a)} width={bw} height={Math.max(0, Q.b - Q.Y(a))} fill={n <= k ? C.blue : C.mut} opacity={n <= k ? 0.9 : 0.25} />
            {(n === 1 || n % 3 === 0) && <text x={Q.X(n)} y={Q.b + 12} textAnchor="middle" fontSize="8.5" fill={C.mut}>{n}</text>}
          </g>
        );
      })}
      <line x1={Q.l} x2={Q.r} y1={Q.b} y2={Q.b} stroke={C.mut} />
      <text x={Q.r} y={Q.b + 23} textAnchor="end" fontSize="8.5" fill={C.mut}>배음 번호 →</text>
    </Frame>
  );
}

/* ── 현과 관의 정상파 ── */
export function Pipe({ p = {} }) {
  const [kind, setKind] = useState(["string", "open", "closed"].includes(p.kind) ? p.kind : "string");
  const [n, setN] = useState(clamp(p.n ?? 2, 1, 5));
  const clock = useClock({ period: 12, rest: 0.35 });
  const h = kind === "closed" ? 2 * n - 1 : n;
  const x0 = 40, x1 = 320, cy = 92, A = 36, X = (u) => x0 + u * (x1 - x0);
  const shape = (u) => (kind === "string" ? Math.sin(h * Math.PI * u) : kind === "open" ? Math.cos(h * Math.PI * u) : Math.sin((h * Math.PI * u) / 2));
  const ct = Math.cos(TAU * 0.3 * h * clock.t);
  const us = Array.from({ length: 241 }, (_, i) => i / 240);
  const nodes = kind === "string" ? Array.from({ length: h + 1 }, (_, j) => j / h)
    : kind === "open" ? Array.from({ length: h }, (_, j) => (j + 0.5) / h)
      : Array.from({ length: Math.floor(h / 2) + 1 }, (_, j) => (2 * j) / h);
  const txt = kind === "string"
    ? <>양 끝이 묶인 현 — 묶인 끝은 늘 마디 · n 번째 모양의 파장 2L ÷ n, 진동수 fₙ = n × v ÷ (2L) — 기본음의 모든 정수배가 나온다</>
    : kind === "open"
      ? <>양 끝이 열린 관(플루트) — 열린 끝에서는 공기가 가장 크게 움직인다(배) · 파장 2L ÷ n → 모든 배음이 나온다 · 점들은 공기 알갱이: 소리는 앞뒤로 흔들리는 세로 파동</>
      : <>한쪽이 닫힌 관(클라리넷에 가까움) — 닫힌 끝은 마디, 열린 끝은 배 · 파장 4L ÷ (2n − 1) → 홀수 배음만 나오고, 기본음은 같은 길이의 열린 관보다 한 옥타브 낮다 · 점들은 공기 알갱이</>;
  return (
    <Frame clock={clock} title="현과 관의 정상파 — 어떤 배음이 허락되는가"
      read={<>{txt} · 지금 <b>{h} 배음</b>(진동수 {h} × f₁)</>}
      controls={<>
        <Seg value={kind} onChange={(v) => { setKind(v); clock.reset(); }} options={[["string", "현"], ["open", "열린 관"], ["closed", "닫힌 관"]]} />
        <Slider label="모양 번호 n" min={1} max={5} step={1} value={n} onChange={setN} />
      </>}>
      {kind !== "string" && (
        <g>
          <line x1={x0} x2={x1} y1={cy - A - 10} y2={cy - A - 10} stroke={C.mut} strokeWidth="2" />
          <line x1={x0} x2={x1} y1={cy + A + 10} y2={cy + A + 10} stroke={C.mut} strokeWidth="2" />
          {kind === "closed" && <line x1={x0} x2={x0} y1={cy - A - 10} y2={cy + A + 10} stroke={C.ink} strokeWidth="4" />}
        </g>
      )}
      <path d={pth([...us.map((u) => [X(u), cy - A * Math.abs(shape(u))]), ...us.slice().reverse().map((u) => [X(u), cy + A * Math.abs(shape(u))])]) + "Z"} fill={C.blue} fillOpacity="0.1" stroke="none" />
      {kind !== "string" && [-22, 0, 22].map((dy) => Array.from({ length: 29 }, (_, j) => { const u = j / 28; return <circle key={dy + "_" + j} cx={X(u) + 7 * shape(u) * ct} cy={cy + dy} r="2.3" fill={C.mut} opacity="0.7" />; }))}
      <path d={pth(us.map((u) => [X(u), cy - A * shape(u) * ct]))} fill="none" stroke={kind === "string" ? C.ink : C.blue} strokeWidth={kind === "string" ? 2.6 : 2} />
      {kind === "string" && [x0, x1].map((x) => <rect key={x} x={x - 4} y={cy - 12} width="8" height="24" fill={C.ink} />)}
      {nodes.map((u, i) => <circle key={"n" + i} cx={X(u)} cy={cy + A + 22} r="3.4" fill={C.red} />)}
      <text x={x0} y={cy + A + 40} fontSize="9" fill={C.red}>● 마디(움직임 0)</text>
      <text x={x0 + 96} y={cy + A + 40} fontSize="9" fill={C.blue}>■ 흔들리는 폭</text>
      <text x={x0} y="208" fontSize="9" fill={C.ink}>나오는 배음:</text>
      {Array.from({ length: 9 }, (_, i) => {
        const m = i + 1, ok = kind !== "closed" || m % 2 === 1;
        return (
          <g key={"h" + m}>
            <rect x={110 + i * 24} y="196" width="18" height="16" rx="3" fill={m === h ? C.red : ok ? C.blue : "none"} fillOpacity={m === h ? 0.9 : ok ? 0.25 : 0} stroke={ok ? C.blue : C.bd} strokeDasharray={ok ? undefined : "2 2"} />
            <text x={119 + i * 24} y="208" textAnchor="middle" fontSize="9" fill={m === h ? C.card : ok ? C.ink : C.mut}>{m}</text>
          </g>
        );
      })}
      <text x={x1} y="20" textAnchor="end" fontSize="9" fill={C.mut}>길이 L</text>
    </Frame>
  );
}

/* ── 음률: 피타고라스 콤마와 센트 ── */
const CENTS = [["장2도", 203.91, 203.91], ["단3도", 294.13, 315.64], ["장3도", 407.82, 386.31], ["완전4도", 498.04, 498.04], ["완전5도", 701.96, 701.96], ["장6도", 905.87, 884.36], ["장7도", 1109.78, 1088.27]];
const FIFTHS = ["C", "G", "D", "A", "E", "B", "F♯", "C♯", "G♯", "D♯", "A♯", "E♯", "B♯"];
export function Temper({ p = {} }) {
  const [m, setM] = useState(p.m === "cents" ? "cents" : "spiral");
  const clock = useClock({ period: 13, rest: 11 });
  const cx = 112, cy = 114;
  const at = (c, r) => [cx + r * Math.sin((c / 1200) * TAU), cy - r * Math.cos((c / 1200) * TAU)];
  const k = clamp(1 + Math.floor(clock.t / 0.8), 1, 12);
  const pts = Array.from({ length: k + 1 }, (_, i) => at((i * 701.955) % 1200, 42 + i * 3.3));
  const P = plot({ x0: 0, x1: 7, y0: -18, y1: 18, pad: [16, 10, 34, 34] });
  const grow = clamp(clock.t / 3, 0, 1);
  return (
    <Frame clock={clock} title="음률 — 5도를 쌓으면 옥타브에 맞지 않는다"
      read={m === "spiral"
        ? <>완전5도(진동수 3 : 2, 702 센트)를 쌓아 올라가면 12 번 만에 출발음 근처로 돌아오지만 딱 맞지 않는다 — (3/2)¹² ÷ 2⁷ ≈ 1.0136, 약 23.5 센트 어긋남(피타고라스 콤마) · log₂(3/2) 가 무리수라 5도를 아무리 쌓아도 옥타브와 딱 맞을 수 없다 · 평균율은 5도를 700 센트로 2 센트 좁혀 고리를 닫는다 · 지금 {k} 번 쌓음 → {FIFTHS[k]}</>
        : <>센트 = 1200 × log₂(진동수 비) — 평균율의 반음이 100 센트 · 0 선이 평균율 · 피타고라스 음률(금색)은 5도를 순수하게 쌓아 장3도가 약 8 센트 높고, 순정률(초록)은 장3도를 5 : 4 로 맞춰 약 14 센트 낮다 · 평균율은 모든 조에서 똑같이 조금씩 어긋나는 대신 어느 조로든 자유롭게 옮길 수 있다</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["spiral", "피타고라스 콤마"], ["cents", "평균율과의 차이"]]} />}>
      {m === "spiral" ? (
        <g>
          <circle cx={cx} cy={cy} r="86" fill="none" stroke={C.bd} />
          {NOTE.map((nm, j) => { const [x, y] = at(j * 100, 98); return <text key={nm} x={x} y={y + 3.5} textAnchor="middle" fontSize="9" fill={C.mut}>{nm}</text>; })}
          {NOTE.map((nm, j) => { const [x1, y1] = at(j * 100, 82), [x2, y2] = at(j * 100, 90); return <line key={"t" + nm} x1={x1} y1={y1} x2={x2} y2={y2} stroke={C.bd} />; })}
          <path d={pth(pts)} fill="none" stroke={C.gold} strokeWidth="1.2" opacity="0.6" />
          {pts.map(([x, y], i) => <circle key={i} cx={x} cy={y} r={i === 12 ? 4.6 : 3.4} fill={i === 12 ? C.red : C.gold} />)}
          {k === 12 && <path d={(() => { const a = at(0, 86), b = at(23.46, 86); return `M ${a[0]} ${a[1]} A 86 86 0 0 1 ${b[0]} ${b[1]}`; })()} fill="none" stroke={C.red} strokeWidth="3" />}
          {[["완전5도 3 : 2 를 12 번", C.ink], ["(3/2)¹² ≈ 129.75", C.gold], ["7 옥타브 2⁷ = 128", C.ink], ["차이 1.0136 배", C.red], ["= 약 23.5 센트", C.red], ["평균율: 5도를 700 센트로", C.blue], ["2 센트씩 좁혀 딱 맞춘다", C.blue]].map(([s, col], i) => <text key={s} x="228" y={42 + i * 22} fontSize="10" fill={col}>{s}</text>)}
        </g>
      ) : (
        <g>
          <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.ink} />
          {[-15, -10, -5, 5, 10, 15].map((v) => <g key={v}><line x1={P.l} x2={P.r} y1={P.Y(v)} y2={P.Y(v)} stroke={C.bd} strokeWidth="0.6" /><text x={P.l - 4} y={P.Y(v) + 3} textAnchor="end" fontSize="8.5" fill={C.mut}>{v > 0 ? `+${v}` : `−${-v}`}</text></g>)}
          <text x={P.l - 4} y={P.Y(0) + 3} textAnchor="end" fontSize="8.5" fill={C.ink}>0</text>
          {CENTS.map(([nm, py, ju], i) => {
            const ref = Math.round(py / 100) * 100, dp = (py - ref) * grow, dj = (ju - ref) * grow, xc = P.X(i + 0.5);
            return (
              <g key={nm}>
                <rect x={xc - 13} y={Math.min(P.Y(0), P.Y(dp))} width="12" height={Math.abs(P.Y(dp) - P.Y(0))} fill={C.gold} />
                <rect x={xc + 1} y={Math.min(P.Y(0), P.Y(dj))} width="12" height={Math.abs(P.Y(dj) - P.Y(0))} fill={C.green} />
                <text x={xc} y={P.b + 14} textAnchor="middle" fontSize="9" fill={C.ink}>{nm}</text>
              </g>
            );
          })}
          <text x={P.l} y={P.t - 4} fontSize="9" fill={C.mut}>평균율과의 차이(센트)</text>
          <rect x="214" y={P.t - 12} width="9" height="9" fill={C.gold} /><text x="226" y={P.t - 4} fontSize="9" fill={C.ink}>피타고라스</text>
          <rect x="284" y={P.t - 12} width="9" height="9" fill={C.green} /><text x="296" y={P.t - 4} fontSize="9" fill={C.ink}>순정률</text>
        </g>
      )}
    </Frame>
  );
}

/* ── 협화와 불협화: 세서레스의 거칠기 곡선 ── */
const F0 = 261.63;
const SETH = (f1, f2, a1, a2) => { const lo = Math.min(f1, f2), x = Math.abs(f2 - f1), s = 0.24 / (0.0207 * lo + 18.96); return Math.min(a1, a2) * (Math.exp(-3.51 * s * x) - Math.exp(-5.75 * s * x)); };
const RAT = [[1, "1:1", 0], [1.2, "6:5", 1], [1.25, "5:4", 0], [4 / 3, "4:3", 1], [1.5, "3:2", 0], [5 / 3, "5:3", 1], [2, "2:1", 0]];
function dcurve(np) {
  const am = Array.from({ length: np }, (_, i) => 0.88 ** i), pts = [];
  for (let i = 0; i <= 420; i++) {
    const r = 1 + (i / 420) * 1.05;
    let D = 0;
    for (let a = 0; a < np; a++) for (let b = 0; b < np; b++) D += SETH(F0 * (a + 1), r * F0 * (b + 1), am[a], am[b]);
    pts.push([r, D]);
  }
  const mx = Math.max(...pts.map((q) => q[1]));
  return pts.map(([r, D]) => [r, D / mx]);
}
export function Dissonance({ p = {} }) {
  const [m, setM] = useState(p.m === "sine" ? "sine" : "harm");
  const clock = useClock({ period: 12, rest: 4.76 });
  const cur = useMemo(() => dcurve(m === "sine" ? 1 : 6), [m]);
  const r = 1 + 1.05 * clamp(clock.t / 10, 0, 1);
  const P = plot({ x0: 1, x1: 2.05, y0: 0, y1: 1.1, pad: [14, 12, 92, 30] });
  const i0 = Math.min(cur.length - 1, Math.round(((r - 1) / 1.05) * 420)), Dr = cur[i0][1];
  const nm = RAT.find((q) => Math.abs(q[0] - r) < 0.01);
  const np = m === "sine" ? 1 : 6, LX = (f) => 30 + (Math.log2(f / F0) / 3.75) * 318;
  const A = Array.from({ length: np }, (_, i) => F0 * (i + 1)), B = Array.from({ length: np }, (_, i) => r * F0 * (i + 1));
  const near = (f) => A.some((g) => Math.abs(Math.log2(f / g)) < 0.006);
  const rough = (f) => A.some((g) => SETH(g, f, 1, 1) > 0.12);
  return (
    <Frame clock={clock} title="협화와 불협화 — 배음이 부딪치는 곳"
      read={<>두 음의 진동수 비 r 에 따른 거칠기(불협화, 세서레스 모형) · {m === "harm"
        ? "배음 6 개를 가진 두 음: 배음끼리 아주 가까우면 거칠게 맥놀이하고 딱 겹치면 매끄럽다 — 그래서 배음이 겹치는 간단한 정수비 2:1, 3:2, 4:3, 5:4, 5:3, 6:5 에 골짜기가 생긴다"
        : "사인파 두 개: 아주 가까울 때(같은 임계 대역 안)만 거칠고 조금만 떨어지면 매끄럽다 — 정수비가 특별하지 않다. 협화음의 골짜기는 배음에서 나온다"} · 지금 r = {fmt(r, 3)}{nm ? `(${nm[1]})` : ""}, 거칠기 {fmt(Dr, 2)} · 아래 띠: 두 음의 배음 자리(초록 = 겹침, 빨강 = 가까워 거침)</>}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["harm", "배음 6 개"], ["sine", "사인파"]]} />}>
      <line x1={P.l} x2={P.r} y1={P.b} y2={P.b} stroke={C.mut} />
      <line x1={P.l} x2={P.l} y1={P.t} y2={P.b} stroke={C.mut} />
      <text x={P.l + 4} y={P.t + 8} fontSize="9" fill={C.mut}>거칠기</text>
      {RAT.map(([x, s, row]) => (
        <g key={s}>
          <line x1={P.X(x)} x2={P.X(x)} y1={P.t} y2={P.b} stroke={C.bd} strokeDasharray="2 3" />
          <text x={P.X(x)} y={P.b + 11 + row * 11} textAnchor="middle" fontSize="8.5" fill={C.ink}>{s}</text>
        </g>
      ))}
      <path d={P.poly(cur)} fill="none" stroke={C.red} strokeWidth="2" />
      <line x1={P.X(r)} x2={P.X(r)} y1={P.t} y2={P.b} stroke={C.violet} strokeWidth="1.4" />
      <circle cx={P.X(r)} cy={P.Y(Dr)} r="4.2" fill={C.violet} />
      <text x="4" y="182" fontSize="8.5" fill={C.blue}>아래 음</text>
      <text x="4" y="204" fontSize="8.5" fill={C.red}>위 음</text>
      <line x1="30" x2="348" y1="186" y2="186" stroke={C.bd} />
      {A.map((f, i) => <line key={"a" + i} x1={LX(f)} x2={LX(f)} y1="172" y2="186" stroke={C.blue} strokeWidth="2" />)}
      {B.map((f, i) => { const g = near(f), rr = !g && rough(f); return <line key={"b" + i} x1={LX(f)} x2={LX(f)} y1="186" y2="200" stroke={g ? C.green : rr ? C.red : C.mut} strokeWidth={g || rr ? 3 : 2} />; })}
      {B.filter(near).map((f, i) => <circle key={"g" + i} cx={LX(f)} cy="186" r="3" fill={C.green} />)}
    </Frame>
  );
}

/* ── 유클리드 리듬 ── */
const RNAME = { "3,8": "쿠바의 트레시요", "5,8": "쿠바의 신킬로", "7,12": "서아프리카의 종 리듬 — 장음계의 배치와 같은 꼴", "5,16": "브라질의 보사노바", "4,9": "튀르키예의 악사크", "4,16": "고른 네 박", "2,4": "고른 두 박" };
export function ERhythm({ p = {} }) {
  const [n, setN] = useState(clamp(p.n ?? 8, 3, 16));
  const [k, setK] = useState(clamp(p.k ?? 3, 1, 16));
  const kk = Math.min(k, n);
  const clock = useClock({ period: 8, rest: 1.15 });
  const on = Array.from({ length: n }, (_, i) => (i * kk) % n < kk);
  const idx = on.map((v, i) => (v ? i : -1)).filter((i) => i >= 0);
  const gaps = idx.map((v, j) => (idx[(j + 1) % idx.length] - v + n) % n || n);
  const phase = (clock.t / 4) % 1, cur = Math.floor(phase * n);
  const cx = 96, cy = 112, R = 74;
  const at = (i, r = R) => [cx + r * Math.sin((i / n) * TAU), cy - r * Math.cos((i / n) * TAU)];
  const name = RNAME[`${kk},${n}`];
  const cw = Math.min(16, 160 / n), gx = 190;
  const hand = at(phase * n, R - 10);
  return (
    <Frame clock={clock} title="유클리드 리듬 — 박을 가장 고르게 나누기"
      read={<>{n} 칸짜리 마디에 박 {kk} 개를 최대한 고르게 놓는다(유클리드 리듬) — 칸 i 에 박이 있을 조건: (i × k) mod n {"<"} k · 박 사이 간격 {gaps.join(" · ")}{name ? ` — ${name}` : ""} · 간격이 많아야 두 가지 값(n ÷ k 의 몫과 몫 + 1)뿐이라 고르게 들린다 · 유클리드 호제법과 같은 꼴의 나눗셈을 되풀이해 만들 수 있다(비요르클룬 알고리즘)</>}
      controls={<>
        <Slider label="칸 n" min={3} max={16} step={1} value={n} onChange={(v) => { setN(v); clock.reset(); }} />
        <Slider label="박 k" min={1} max={n} step={1} value={kk} onChange={(v) => { setK(v); clock.reset(); }} />
      </>}>
      <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.bd} />
      {idx.length > 1 && <path d={pth(idx.map((i) => at(i))) + "Z"} fill={C.gold} fillOpacity="0.15" stroke={C.gold} strokeWidth="1.6" />}
      <line x1={cx} y1={cy} x2={hand[0]} y2={hand[1]} stroke={C.red} strokeWidth="1.6" />
      {on.map((v, i) => { const [x, y] = at(i); return <circle key={i} cx={x} cy={y} r={v ? (i === cur ? 9 : 6.5) : 3.2} fill={v ? (i === cur ? C.red : C.ink) : C.card} stroke={v ? "none" : C.mut} />; })}
      <circle cx={cx} cy={cy} r="3" fill={C.red} />
      {on.map((v, i) => <rect key={"c" + i} x={gx + i * cw} y="62" width={cw - 2} height={cw - 2} rx="2" fill={v ? (i === cur ? C.red : C.ink) : C.card} stroke={i === cur ? C.red : C.mut} strokeWidth={i === cur ? 1.6 : 0.8} />)}
      <text x={gx} y="50" fontSize="9.5" fill={C.ink}>한 마디({n} 칸)</text>
      <text x={gx} y="104" fontSize="9.5" fill={C.ink}>간격 {gaps.join(" · ")}</text>
      <text x={gx} y="124" fontSize="9.5" fill={C.mut}>박 {kk} 개 · 칸 {n} 개</text>
      {name && <text x={gx} y="150" fontSize="9.5" fill={C.gold}>{name.split(" — ")[0]}</text>}
      {name && name.includes(" — ") && <text x={gx} y="166" fontSize="9" fill={C.mut}>{name.split(" — ")[1]}</text>}
    </Frame>
  );
}

/* ── 12 음 시계: 조옮김은 회전, 5도권은 ×7 ── */
const SETS = { major: { name: "장음계", s: [0, 2, 4, 5, 7, 9, 11] }, whole: { name: "온음음계", s: [0, 2, 4, 6, 8, 10] }, dim: { name: "감7화음", s: [0, 3, 6, 9] } };
export function Clock12({ p = {} }) {
  const [m, setM] = useState(["major", "whole", "dim", "fifths"].includes(p.m) ? p.m : "major");
  const clock = useClock({ period: 13, rest: 6.6 });
  const cx = 104, cy = 112, R = 78;
  const pos = (j, r = R) => [cx + r * Math.sin((j / 12) * TAU), cy - r * Math.cos((j / 12) * TAU)];
  const k = Math.min(11, Math.floor(clock.t / 0.9));
  const S = SETS[m];
  const base = S ? S.s : [], tr = S ? base.map((x) => (x + k) % 12).sort((a, b) => a - b) : [];
  const common = tr.filter((x) => base.includes(x)).length;
  const per = S ? [1, 2, 3, 4, 6, 12].find((q) => base.every((x) => base.includes((x + q) % 12))) : 12;
  const steps = Math.min(12, Math.floor(clock.t / 0.9) + 1);
  const star = Array.from({ length: steps + 1 }, (_, i) => (7 * i) % 12);
  const read = S
    ? <>12 음을 12 시간 시계처럼 놓으면 조옮김은 회전(x → x + k, mod 12)이다 · 지금 {S.name}{m === "dim" ? "을" : "를"} {k} 칸 옮김{m === "major" ? ` → ${NOTE[k]} 장조` : ""}: 원래와 공통음 <b>{common} 개</b> · {per === 12 ? "12 칸을 다 돌아야 제자리 — 서로 다른 조가 12 개" : `${per} 칸만 돌려도 제자리 — 서로 다른 것이 ${per} 개뿐`}{m === "whole" ? "(메시앙의 ‘옮김이 제한된 선법’)" : ""}{m === "major" ? " · 5도(7 칸) 옮긴 조와는 6 음을 나눠 가져 가장 가깝다" : ""}</>
    : <>반음(1 칸) 대신 완전5도(7 칸)씩 건너뛰면 C → G → D → A → E → B → F♯ → C♯ → A♭ → E♭ → B♭ → F → C, 12 음을 모두 한 번씩 지나 제자리로 돌아온다 — 7 과 12 가 서로소이기 때문 · 3 칸(단3도)씩 가면 4 음만 돌고 제자리(감7화음), 4 칸(장3도)씩 가면 3 음(증3화음) · ×7 은 반음계를 5도권으로 바꾸는 규칙(7 × 7 = 49 ≡ 1 이라 되돌리기도 ×7)</>;
  return (
    <Frame clock={clock} title="12 음 시계 — 조옮김은 회전이다" read={read}
      controls={<Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["major", "장음계"], ["whole", "온음음계"], ["dim", "감7화음"], ["fifths", "5도권"]]} />}>
      <circle cx={cx} cy={cy} r={R} fill="none" stroke={C.bd} />
      {NOTE.map((nm, j) => { const [x, y] = pos(j, R + 14); return <text key={nm} x={x} y={y + 3.5} textAnchor="middle" fontSize="9.5" fill={C.ink}>{nm}</text>; })}
      {S && <path d={pth(base.map((j) => pos(j))) + "Z"} fill="none" stroke={C.mut} strokeDasharray="3 3" />}
      {S && <path d={pth(tr.map((j) => pos(j))) + "Z"} fill={C.violet} fillOpacity="0.15" stroke={C.violet} strokeWidth="2" />}
      {!S && <path d={pth(star.map((j) => pos(j)))} fill="none" stroke={C.gold} strokeWidth="1.8" />}
      {Array.from({ length: 12 }, (_, j) => {
        const [x, y] = pos(j), inB = base.includes(j), inT = tr.includes(j), lit = !S && star.includes(j);
        return <circle key={j} cx={x} cy={y} r={inT || lit ? 5.2 : 3} fill={inT ? C.violet : lit ? C.gold : C.card} stroke={inB ? C.ink : C.mut} strokeWidth={inB ? 1.6 : 0.8} />;
      })}
      {S ? (
        <g>
          <text x="214" y="56" fontSize="10" fill={C.violet}>{`T${k}: x → x + ${k} (mod 12)`}</text>
          <text x="214" y="80" fontSize="10" fill={C.ink}>{`공통음 ${common} 개`}</text>
          <text x="214" y="104" fontSize="10" fill={C.ink}>{`제자리 주기 ${per} 칸`}</text>
          <text x="214" y="134" fontSize="9" fill={C.mut}>점선 = 처음 자리</text>
          <text x="214" y="150" fontSize="9" fill={C.violet}>보라 = 옮긴 자리</text>
        </g>
      ) : (
        <g>
          <text x="214" y="56" fontSize="10" fill={C.gold}>x → 7x (mod 12)</text>
          {Array.from({ length: Math.min(steps, 12) + 1 }, (_, i) => <text key={i} x={214 + (i % 7) * 20} y={84 + Math.floor(i / 7) * 18} fontSize="9.5" fill={i === steps ? C.red : C.ink}>{NOTE[(7 * i) % 12]}</text>)}
        </g>
      )}
    </Frame>
  );
}

/* ── 디지털 오디오: 양자화와 엘리어싱 ── */
const SIGQ = (t) => 0.75 * Math.sin(TAU * 0.9 * t) + 0.2 * Math.sin(TAU * 2.7 * t + 1);
export function Quantize({ p = {} }) {
  const [m, setM] = useState(p.m === "alias" ? "alias" : "quant");
  const [b, setB] = useState(clamp(p.b ?? 3, 1, 8));
  const [f, setF] = useState(clamp(p.f ?? 7, 0.5, 9.5));
  const clock = useClock({ period: 9, rest: 8.5 });
  const prog = clamp(0.15 + clock.t / 7, 0, 1);
  if (m === "quant") {
    const P = plot({ x0: 0, x1: 2, y0: -1.05, y1: 1.05, pad: [12, 12, 70, 30] });
    const Q = plot({ x0: 0, x1: 2, y0: -0.55, y1: 0.55, pad: [166, 12, 20, 30] });
    const L = 2 ** b, D = 2 / L, q = (v) => clamp(D * (Math.floor(v / D) + 0.5), -1 + D / 2, 1 - D / 2);
    const N = Math.floor(prog * 40), S = Array.from({ length: N }, (_, i) => { const t = i / 20; return [t, SIGQ(t), q(SIGQ(t))]; });
    const stair = S.flatMap(([t, , v]) => [[P.X(t), P.Y(v)], [P.X(t + 0.05), P.Y(v)]]);
    return (
      <Frame clock={clock} title="디지털 오디오 — 재고, 반올림한다"
        read={<>{b} 비트 = {L} 단계로 세기를 잰다 · 점은 1 초에 20 번 잰 표본, 빨간 계단은 가장 가까운 단계로 반올림한 값 · 반올림 오차(아래, ±반 계단 안)가 잡음처럼 더해진다 · 비트가 하나 늘 때마다 계단이 반으로 줄어 잡음이 약 6 dB 준다: 신호 대 잡음비 ≈ 6.02 × b + 1.76 = <b>{fmt(6.02 * b + 1.76, 1)} dB</b>(꽉 찬 사인파 기준) — CD 의 16 비트는 약 98 dB</>}
        controls={<>
          <Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["quant", "양자화"], ["alias", "엘리어싱"]]} />
          <Slider label="비트 수" min={1} max={8} step={1} value={b} onChange={setB} />
        </>}>
        {b <= 5 && Array.from({ length: L + 1 }, (_, i) => <line key={i} x1={P.l} x2={P.r} y1={P.Y(-1 + i * D)} y2={P.Y(-1 + i * D)} stroke={C.bd} strokeWidth="0.6" />)}
        <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.mut} strokeWidth="0.8" />
        <path d={P.path(SIGQ, 0, 2, 300)} fill="none" stroke={C.blue} strokeWidth="1.6" opacity="0.6" />
        <path d={pth(stair)} fill="none" stroke={C.red} strokeWidth="1.8" />
        {S.map(([t, , v], i) => <circle key={i} cx={P.X(t)} cy={P.Y(v)} r="2.6" fill={C.red} />)}
        <text x={P.l} y={P.t + 9} fontSize="9" fill={C.blue}>원래 소리</text>
        <line x1={Q.l} x2={Q.r} y1={Q.Y(0)} y2={Q.Y(0)} stroke={C.mut} strokeWidth="0.8" />
        {[D / 2, -D / 2].map((v) => <line key={v} x1={Q.l} x2={Q.r} y1={Q.Y(v)} y2={Q.Y(v)} stroke={C.gold} strokeDasharray="3 3" strokeWidth="0.8" />)}
        {S.map(([t, s, v], i) => <line key={"e" + i} x1={Q.X(t)} x2={Q.X(t)} y1={Q.Y(0)} y2={Q.Y(v - s)} stroke={C.gold} strokeWidth="2" />)}
        <text x={Q.l} y={Q.t - 4} fontSize="9" fill={C.gold}>반올림 오차(±반 계단)</text>
      </Frame>
    );
  }
  const fs = 10, mm = Math.round(f / fs), fa = f - mm * fs;
  const P = plot({ x0: 0, x1: 1, y0: -1.2, y1: 1.2, pad: [12, 12, 50, 30] });
  const N = Math.floor(prog * 11), smp = Array.from({ length: N }, (_, i) => i / fs);
  const FX = (v) => 30 + (v / 10) * 318;
  return (
    <Frame clock={clock} title="디지털 오디오 — 너무 빠른 소리는 접혀 들어온다"
      read={<>1 초에 10 번(표본화 진동수 10 Hz) 재는데 신호는 {fmt(f, 2)} Hz · 점들만 보면 <b>{fmt(Math.abs(fa), 2)} Hz</b> 로 보인다{f > fs / 2 ? " — 나이퀴스트 한계(5 Hz)를 넘은 진동수가 낮은 진동수로 접혀 들어오는 엘리어싱" : " — 5 Hz 보다 낮아 점들로 원래 신호를 되살릴 수 있다"} · 그래서 녹음 전에 표본화 진동수의 절반보다 높은 소리를 걸러 낸다(CD 는 1 초에 44100 번 재어 사람이 듣는 20 kHz 까지 담는다) · 영화 속 마차 바퀴가 거꾸로 도는 듯 보이는 것도 같은 현상</>}
      controls={<>
        <Seg value={m} onChange={(v) => { setM(v); clock.reset(); }} options={[["quant", "양자화"], ["alias", "엘리어싱"]]} />
        <Slider label="신호 진동수" min={0.5} max={9.5} step={0.25} value={f} onChange={setF} show={(v) => `${fmt(v, 2)} Hz`} />
      </>}>
      <line x1={P.l} x2={P.r} y1={P.Y(0)} y2={P.Y(0)} stroke={C.mut} strokeWidth="0.8" />
      <path d={P.path((t) => Math.sin(TAU * f * t), 0, 1, 600)} fill="none" stroke={C.blue} strokeWidth="1.3" opacity="0.55" />
      <path d={P.path((t) => Math.sin(TAU * fa * t), 0, 1, 300)} fill="none" stroke={C.red} strokeWidth="2" strokeDasharray={f > fs / 2 ? undefined : "5 3"} />
      {smp.map((t, i) => <g key={i}><line x1={P.X(t)} x2={P.X(t)} y1={P.Y(0)} y2={P.Y(Math.sin(TAU * f * t))} stroke={C.ink} strokeWidth="1" /><circle cx={P.X(t)} cy={P.Y(Math.sin(TAU * f * t))} r="3.6" fill={C.ink} /></g>)}
      <line x1="30" x2="348" y1="200" y2="200" stroke={C.mut} />
      {[0, 5, 10].map((v) => <text key={v} x={FX(v)} y="214" textAnchor={v === 0 ? "start" : v === 10 ? "end" : "middle"} fontSize="8.5" fill={C.mut}>{v} Hz</text>)}
      <line x1={FX(5)} x2={FX(5)} y1="190" y2="206" stroke={C.gold} strokeDasharray="3 2" />
      <text x={FX(5) + 3} y="188" fontSize="8.5" fill={C.gold}>한계 5 Hz</text>
      <circle cx={FX(f)} cy="200" r="4" fill={C.blue} />
      <circle cx={FX(Math.abs(fa))} cy="200" r="4" fill={C.red} />
      <text x={P.l} y={P.t + 9} fontSize="9" fill={C.blue}>진짜 신호</text>
      <text x={P.l + 60} y={P.t + 9} fontSize="9" fill={C.red}>점들이 보여 주는 신호</text>
    </Frame>
  );
}
