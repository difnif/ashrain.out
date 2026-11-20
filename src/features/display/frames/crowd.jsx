// ashrain.out — 수학 호기심 액자: 북적북적 학년별 뽑기 (frames/crowd.jsx)
// 가을 축제 날 운동장 — 가게 · 무대 · 분수대 사이로 학생(학년마다 체육복 색) · 어른 · 동생 · 강아지가 북적인다(숨은그림찾기 그림체).
// 차례마다 돋보기가 사람들 사이를 훑다가 뽑힌 학생에게 멈추고, 뽑힌 학생들에게 불이 켜진 뒤
// 「몇 학년 누가 뽑혔는지 · 그렇게 뽑힐 확률」이 잠깐 떴다가 사라진다. 사람들은 그동안에도 천천히 거닌다.
//   중등: 학년마다 {1/경우의 수}를 곱한 확률(2명이면 10 × 9 ÷ 2 꼴) · 초등: 모두 몇 가지 중 하나.
// 학년별 인원 · 뽑는 수 · 빠르기를 고르고, 「새로 모이기(R)」로 새 이름 · 새 자리. 계산: ../curio/crowd.js
import { memo } from "react";
import { W, H, SceneTitle, SANS, MText } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, uWidth, Chip } from "../kit-story.jsx";
import { hashSeed, rng, SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx } from "../curio/kit.js";
import { CROWD, CROWD_DEF, fixCrowd, crowdOf, posOf, pickOf, crowdLines, BOX, GRADE } from "../curio/crowd.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";

const LSK = "ash.display.curio.crowd";
const OL = "#3a2a1e";                       // 그림 테두리 선
export const CT = { roam: [0, 2400], spot: [2300, 5200], card: [4500, 7700], out: [7600, 8400] };

/* ══════════ 사람 ══════════ */
function Hair({ style, col, r }) {
  switch (style) {
    case 1: return <path d={`M${-r * 1.05} ${-r * 0.1}Q${-r * 1.3} ${r * 1.6} ${-r * 0.4} ${r * 1.5}L${r * 0.6} ${r * 1.3}Q${r * 1.2} ${r * 0.8} ${r * 1.05} ${-r * 0.2}A${r * 1.05} ${r * 1.1} 0 0 0 ${-r * 1.05} ${-r * 0.1}Z`} fill={col} stroke={OL} strokeWidth={1} />;
    case 2: return <g><path d={`M${-r} ${0}A${r} ${r * 1.05} 0 0 1 ${r} ${0}Q${r * 0.3} ${-r * 0.5} ${-r} ${0}Z`} fill={col} stroke={OL} strokeWidth={1} /><circle cx={-r * 1.1} cy={-r * 0.2} r={r * 0.42} fill={col} stroke={OL} strokeWidth={1} /></g>;
    case 3: return <path d={`M${-r * 1.08} ${r * 0.6}V${-r * 0.1}A${r * 1.08} ${r * 1.1} 0 0 1 ${r * 1.08} ${-r * 0.1}V${r * 0.6}H${r * 0.55}V${-r * 0.05}Q${0} ${-r * 0.55} ${-r * 0.55} ${-r * 0.05}V${r * 0.6}Z`} fill={col} stroke={OL} strokeWidth={1} />;
    case 4: return <path d={`M${-r * 0.95} ${-r * 0.25}A${r} ${r} 0 0 1 ${r * 0.95} ${-r * 0.25}Q${0} ${-r * 0.75} ${-r * 0.95} ${-r * 0.25}Z`} fill={col} opacity={0.85} />;
    case 5: return <g fill={col} stroke={OL} strokeWidth={0.9}>{[-0.8, -0.3, 0.25, 0.75].map((u, i) => <circle key={i} cx={u * r} cy={-r * (0.55 + 0.25 * Math.cos(u * 2))} r={r * 0.45} />)}</g>;
    default: return <path d={`M${-r * 1.02} ${r * 0.05}A${r * 1.02} ${r * 1.05} 0 0 1 ${r * 1.02} ${r * 0.05}Q${r * 0.3} ${-r * 0.5} ${-r * 0.4} ${-r * 0.25}Q${-r * 0.8} ${-r * 0.1} ${-r * 1.02} ${r * 0.05}Z`} fill={col} stroke={OL} strokeWidth={1} />;
  }
}
/** 사람 하나(발 = 원점, 오른쪽을 본다) */
const Figure = memo(function Figure({ p, step }) {
  if (p.kind === "dog") {
    const f = p.fur;
    const k = step === 0 ? 2 : step === 1 ? -2 : 0;
    return (
      <g>
        <ellipse cx={0} cy={1} rx={13} ry={3.5} fill="#000" opacity={0.18} />
        <path d={`M-10 0V-7M-5 0V-7M6 0V-7M10 0V-7`} stroke={OL} strokeWidth={2.4} transform={`skewX(${k * 3})`} />
        <ellipse cx={0} cy={-11} rx={13} ry={6.5} fill={f} stroke={OL} strokeWidth={1.1} />
        <path d="M-12 -13q-7 -5 -5 -11" fill="none" stroke={OL} strokeWidth={2.2} strokeLinecap="round" />
        <circle cx={12} cy={-17} r={6} fill={f} stroke={OL} strokeWidth={1.1} />
        <path d="M9 -22l-2 -6l5 3z" fill={f} stroke={OL} strokeWidth={1} />
        <circle cx={14} cy={-18} r={1} fill={OL} /><circle cx={17.6} cy={-16} r={1.3} fill={OL} />
      </g>
    );
  }
  const sc = p.kind === "adult" ? 1.2 : p.kind === "kid" ? 0.78 : 1;
  const shirt = p.kind === "student" ? GRADE[p.grade - 1] : p.shirt;
  const lg = step === 0 ? 3.2 : step === 1 ? -3.2 : 0, arm = step === 0 ? 2 : step === 1 ? -2 : 0;
  const hr = 7;
  return (
    <g transform={sc !== 1 ? `scale(${sc})` : undefined}>
      <ellipse cx={0} cy={1} rx={9} ry={3} fill="#000" opacity={0.2} />
      {p.item === "balloon" && <g><path d={`M8 -20Q10 -40 7 -58`} fill="none" stroke={OL} strokeWidth={0.8} /><ellipse cx={7} cy={-64} rx={7} ry={8.5} fill={p.bcol} stroke={OL} strokeWidth={1} /></g>}
      {p.bag && <rect x={-12} y={-31} width={6} height={13} rx={2} fill={p.bag} stroke={OL} strokeWidth={1} />}
      <rect x={-5 - lg} y={-16} width={4.2} height={15} rx={1.5} fill={p.pants} stroke={OL} strokeWidth={1} />
      <rect x={0.8 + lg} y={-16} width={4.2} height={15} rx={1.5} fill={p.pants} stroke={OL} strokeWidth={1} />
      {p.kind === "student" && <path d={`M${-3 - lg} -15v13M${3 + lg} -15v13`} stroke="#fff" strokeWidth={0.8} opacity={0.8} />}
      <ellipse cx={-3 - lg} cy={-0.5} rx={3.6} ry={1.8} fill="#2a2420" />
      <ellipse cx={3.2 + lg} cy={-0.5} rx={3.6} ry={1.8} fill="#2a2420" />
      <rect x={-10} y={-29 + arm} width={4} height={12} rx={2} fill={shirt} stroke={OL} strokeWidth={1} />
      <path d="M-8 -14C-9 -24 -7 -31 0 -31C7 -31 9 -24 8 -14Z" fill={shirt} stroke={OL} strokeWidth={1.1} />
      {p.kind === "student" && <path d="M-3 -31L0 -27L3 -31" fill="none" stroke="#fff" strokeWidth={1} />}
      <rect x={6} y={-29 - arm} width={4} height={12} rx={2} fill={shirt} stroke={OL} strokeWidth={1} />
      <circle cx={-8} cy={-17 + arm} r={2.1} fill={p.skin} stroke={OL} strokeWidth={0.7} />
      <circle cx={8} cy={-17 - arm} r={2.1} fill={p.skin} stroke={OL} strokeWidth={0.7} />
      {p.item === "icecream" && <g><path d="M8 -19l3 -8h-6z" fill="#e0b070" stroke={OL} strokeWidth={0.8} /><circle cx={8} cy={-28} r={3} fill="#f7c6d9" stroke={OL} strokeWidth={0.8} /></g>}
      {p.item === "bag" && <rect x={6} y={-22} width={7} height={8} rx={1.5} fill="#8a5a3a" stroke={OL} strokeWidth={0.8} />}
      <g transform={`translate(0, ${-31 - hr})`}>
        {p.style === 1 && <Hair style={1} col={p.hair} r={hr} />}
        <circle cx={0} cy={0} r={hr} fill={p.skin} stroke={OL} strokeWidth={1.1} />
        {p.style !== 1 && <Hair style={p.style} col={p.hair} r={hr} />}
        {p.style === 1 && <path d={`M${-hr} ${-hr * 0.1}A${hr} ${hr * 1.05} 0 0 1 ${hr} ${-hr * 0.2}Q${0} ${-hr * 0.55} ${-hr} ${-hr * 0.1}Z`} fill={p.hair} />}
        {p.hat && <g><path d={`M${-hr * 1.05} ${-hr * 0.2}A${hr * 1.05} ${hr} 0 0 1 ${hr * 1.05} ${-hr * 0.2}Z`} fill={p.hat} stroke={OL} strokeWidth={1} /><path d={`M${hr * 0.6} ${-hr * 0.25}h${hr * 0.9}`} stroke={OL} strokeWidth={2} /></g>}
        <circle cx={1.6} cy={0.6} r={0.95} fill={OL} />
        <circle cx={4.6} cy={0.6} r={0.95} fill={OL} />
        {p.glasses && <g fill="none" stroke={OL} strokeWidth={0.8}><rect x={0} y={-0.8} width={3} height={2.6} /><rect x={3.4} y={-0.8} width={3} height={2.6} /></g>}
        <path d="M2.4 3.6q1.6 1.1 3 0" fill="none" stroke={OL} strokeWidth={0.8} strokeLinecap="round" />
      </g>
    </g>
  );
});

/* ══════════ 운동장(그림 상자 좌표) ══════════ */
const STALLS = [
  [20, 190, "#e15b5b", "떡볶이"], [20, 380, "#4d8fd6", "솜사탕"], [20, 570, "#f2b33d", "음료"],
  [1312, 190, "#5bb36a", "풍선"], [1312, 380, "#a46fd6", "사진관"], [1312, 570, "#ef8bb0", "추억 뽑기"],
];
function Stall({ x, y, col, sign, i }) {
  const w = 220, h = 150;
  const sc = [];
  for (let k = 0; k < 8; k++) sc.push(`A13.75 10 0 0 0 ${x + (k + 1) * 27.5} ${y + 46}`);
  const R = rng(hashSeed("stall", i));
  const goods = [];
  for (let k = 0; k < 9; k++) {
    const gx = x + 24 + k * 20, gy = y + 92;
    goods.push(i === 0 ? <circle key={k} cx={gx} cy={gy} r={5} fill="#d9442f" stroke={OL} strokeWidth={0.8} />
      : i === 1 ? <circle key={k} cx={gx} cy={gy - 6} r={8} fill={["#f7c6d9", "#cfe3f7", "#fbe7a8"][k % 3]} stroke={OL} strokeWidth={0.8} />
      : i === 2 ? <rect key={k} x={gx - 4} y={gy - 9} width={8} height={12} rx={2} fill={["#f2b33d", "#6ea6f5", "#e15b5b"][k % 3]} stroke={OL} strokeWidth={0.8} />
      : i === 3 ? <g key={k}><path d={`M${gx} ${gy + 4}V${gy - 26 - R() * 12}`} stroke={OL} strokeWidth={0.7} /><ellipse cx={gx} cy={gy - 32 - R() * 12} rx={7} ry={8.5} fill={["#f2685c", "#6ea6f5", "#f5cf4e", "#a6d886", "#c6a8f6"][k % 5]} stroke={OL} strokeWidth={0.8} /></g>
      : i === 4 ? <rect key={k} x={gx - 6} y={gy - 8} width={12} height={10} rx={1.5} fill="#fff" stroke={OL} strokeWidth={0.8} />
      : <rect key={k} x={gx - 5} y={gy - 7} width={10} height={9} rx={2} fill={["#f2685c", "#5bb36a", "#4d8fd6"][k % 3]} stroke={OL} strokeWidth={0.8} />);
  }
  return (
    <g>
      <rect x={x + 6} y={y + 40} width={w - 12} height={h - 40} fill="#f7efe0" stroke={OL} strokeWidth={1.4} />
      <rect x={x + 4} y={y + 84} width={w - 8} height={30} fill="#c98d55" stroke={OL} strokeWidth={1.4} />
      {goods}
      <path d={`M${x - 4} ${y + 14}L${x + 14} ${y}H${x + w - 14}L${x + w + 4} ${y + 14}V${y + 46}H${x}${sc.join("")}Z`} fill={col} stroke={OL} strokeWidth={1.6} />
      {[1, 3, 5, 7].map((k) => <path key={k} d={`M${x + k * 27.5} ${y + 3}V${y + 46}`} stroke="#fff" strokeOpacity={0.35} strokeWidth={9} />)}
      <rect x={x + w / 2 - 54} y={y + 12} width={108} height={26} rx={6} fill="#fffaf0" stroke={OL} strokeWidth={1.2} />
      <text x={x + w / 2} y={y + 31} textAnchor="middle" fontFamily={SANS} fontSize={16} fontWeight={800} fill="#3a2a1e">{sign}</text>
      <path d={`M${x + 6} ${y + 114}V${y + h}M${x + w - 6} ${y + 114}V${y + h}`} stroke={OL} strokeWidth={2} />
    </g>
  );
}
function Tree({ x, y, r = 46 }) {
  return (
    <g>
      <ellipse cx={x + 6} cy={y + 6} rx={r * 0.8} ry={r * 0.3} fill="#000" opacity={0.15} />
      <rect x={x - 6} y={y - 30} width={12} height={34} fill="#8a5a33" stroke={OL} strokeWidth={1.2} />
      {[[-0.5, -1.2, 0.7], [0.5, -1.25, 0.7], [0, -1.7, 0.75], [-0.2, -1.05, 0.65]].map(([u, v, k], i) => (
        <circle key={i} cx={x + u * r} cy={y + v * r} r={r * k} fill={["#4f9a45", "#5aa84f", "#62b356", "#4a9140"][i]} stroke={OL} strokeWidth={1.3} />
      ))}
    </g>
  );
}
function Performer({ x, y, col, inst }) {
  return (
    <g transform={`translate(${x}, ${y})`}>
      <Figure p={{ kind: "student", grade: 1, skin: "#f1cfae", hair: "#231a15", style: inst % 6, pants: "#222" }} step={-1} />
      <rect x={-11} y={-30} width={22} height={4} fill={col} />
      {inst === 1 && <rect x={6} y={-26} width={14} height={5} rx={2} fill="#c08040" stroke={OL} strokeWidth={0.8} transform="rotate(-25 6 -26)" />}
      {inst === 2 && <circle cx={14} cy={-18} r={7} fill="#e0e0e0" stroke={OL} strokeWidth={1} />}
    </g>
  );
}
const Ground = memo(function Ground({ C }) {
  const dim = C.name === "dark";
  const flags = [];
  for (const [y0, amp] of [[176, 16], [206, 14]]) {
    for (let k = 0; k < 26; k++) {
      const x = 262 + k * 40;
      flags.push(<path key={`${y0}-${k}`} d={`M${x} ${y0 + (k % 2) * 4}l20 0l-10 ${amp}z`} fill={["#e15b5b", "#f2b33d", "#4d8fd6", "#5bb36a", "#a46fd6"][(k + y0) % 5]} stroke={OL} strokeWidth={0.8} />);
    }
  }
  return (
    <g>
      <rect x={0} y={0} width={BOX.w} height={BOX.h} rx={18} fill="#ead6a8" />
      {/* 건물 */}
      <rect x={0} y={0} width={BOX.w} height={76} fill="#f4ebd9" stroke={OL} strokeWidth={1.4} />
      <rect x={0} y={0} width={BOX.w} height={12} fill="#b85c4a" />
      {Array.from({ length: 30 }, (_, k) => k).filter((k) => k < 13 || k > 16).map((k) => (
        <g key={k}><rect x={22 + k * 51} y={22} width={34} height={20} fill="#9cc6e8" stroke={OL} strokeWidth={1} /><rect x={22 + k * 51} y={48} width={34} height={20} fill="#9cc6e8" stroke={OL} strokeWidth={1} /></g>
      ))}
      <rect x={690} y={18} width={172} height={58} fill="#d9cbb0" stroke={OL} strokeWidth={1.2} />
      <rect x={742} y={40} width={68} height={36} fill="#6b4a33" stroke={OL} strokeWidth={1.2} />
      <circle cx={776} cy={30} r={10} fill="#fff" stroke={OL} strokeWidth={1.2} /><path d="M776 30V23M776 30h5" stroke={OL} strokeWidth={1.4} />
      <rect x={480} y={6} width={190} height={30} rx={4} fill="#d9442f" stroke={OL} strokeWidth={1.2} />
      <text x={575} y={27} textAnchor="middle" fontFamily={SANS} fontSize={17} fontWeight={900} fill="#fffaf0">가을 축제 한마당</text>
      <rect x={882} y={6} width={190} height={30} rx={4} fill="#3d7fc4" stroke={OL} strokeWidth={1.2} />
      <text x={977} y={27} textAnchor="middle" fontFamily={SANS} fontSize={17} fontWeight={900} fill="#fffaf0">모두 함께 즐겨요</text>
      {/* 잔디 */}
      <rect x={0} y={76} width={BOX.w} height={78} fill="#9fcf74" stroke={OL} strokeWidth={1} />
      {Array.from({ length: 29 }, (_, k) => <circle key={k} cx={20 + k * 53} cy={84 + (k % 3) * 4} r={12} fill="#6fae4f" stroke={OL} strokeWidth={0.9} />)}
      {/* 무대 */}
      <rect x={640} y={96} width={272} height={70} fill="#2f3f6b" stroke={OL} strokeWidth={1.4} />
      {Array.from({ length: 9 }, (_, k) => <path key={k} d={`M${662 + k * 29} ${110}l3 6l6 1l-5 4l1 6l-5 -3l-5 3l1 -6l-5 -4l6 -1z`} fill="#f5cf4e" />)}
      <rect x={624} y={150} width={304} height={30} fill="#b07a48" stroke={OL} strokeWidth={1.4} />
      <rect x={630} y={120} width={20} height={34} fill="#333" stroke={OL} strokeWidth={1} /><rect x={902} y={120} width={20} height={34} fill="#333" stroke={OL} strokeWidth={1} />
      <Performer x={720} y={158} col="#e15b5b" inst={1} /><Performer x={776} y={156} col="#f5cf4e" inst={0} /><Performer x={832} y={158} col="#4d8fd6" inst={2} />
      {/* 깃발 줄 */}
      <path d="M262 176Q776 196 1290 176M262 206Q776 224 1290 206" fill="none" stroke={OL} strokeWidth={1} />
      {flags}
      {/* 트랙 */}
      <ellipse cx={776} cy={470} rx={470} ry={232} fill="none" stroke="#fff" strokeWidth={3} opacity={0.75} />
      <ellipse cx={776} cy={470} rx={440} ry={204} fill="none" stroke="#fff" strokeWidth={2} opacity={0.55} />
      {/* 분수대 */}
      <ellipse cx={780} cy={410} rx={118} ry={56} fill="#b9b2a4" stroke={OL} strokeWidth={1.6} />
      <ellipse cx={780} cy={404} rx={100} ry={44} fill="#7fc6ea" stroke={OL} strokeWidth={1.2} />
      <ellipse cx={780} cy={396} rx={30} ry={13} fill="#b9b2a4" stroke={OL} strokeWidth={1.2} />
      <path d="M780 394Q770 360 750 372M780 394Q790 356 812 370M780 394V352" fill="none" stroke="#e8f6ff" strokeWidth={3} strokeLinecap="round" />
      {[[-60, 10], [50, 14], [-20, 24], [70, -6], [-80, -8]].map(([dx, dy], k) => <ellipse key={k} cx={780 + dx} cy={404 + dy} rx={9} ry={3} fill="#fff" opacity={0.5} />)}
      {/* 벤치 · 화분 */}
      {[[560, 560], [990, 560]].map(([x, y], k) => <g key={k}><rect x={x} y={y} width={70} height={12} rx={3} fill="#a8703f" stroke={OL} strokeWidth={1.2} /><path d={`M${x + 6} ${y + 12}v10M${x + 64} ${y + 12}v10`} stroke={OL} strokeWidth={2} /></g>)}
      {Array.from({ length: 9 }, (_, k) => <g key={k}><rect x={470 + k * 70} y={738} width={22} height={16} fill="#c9714a" stroke={OL} strokeWidth={1} /><circle cx={481 + k * 70} cy={734} r={9} fill={["#f2685c", "#f5cf4e", "#c6a8f6"][k % 3]} stroke={OL} strokeWidth={0.8} /></g>)}
      {STALLS.map(([x, y, col, sign], i) => <Stall key={i} x={x} y={y} col={col} sign={sign} i={i} />)}
      <Tree x={365} y={735} r={44} /><Tree x={1185} y={735} r={44} />
      {dim && <rect x={0} y={0} width={BOX.w} height={BOX.h} rx={18} fill="#0b1330" opacity={0.16} />}
    </g>
  );
});

/* ══════════ 그리기 ══════════ */
const sid = (mode) => `curio-crowd-${mode}`;
/** 이름표 자리: 머리 위가 기본, 앞 이름표와 겹치면 발 아래 → 그래도 겹치면 옆으로 */
function labelSpots(chosen, posMap) {
  const boxes = [];
  return chosen.map(({ g, s }) => {
    const q = posMap.get(s);
    const w = 150, h = 36;
    const tries = [[q.x, q.y - 76], [q.x, q.y + 34], [q.x - 120, q.y - 30], [q.x + 120, q.y - 30], [q.x, q.y - 118]];
    let pick = tries[0];
    for (const [x, y] of tries) {
      if (!boxes.some(([bx, by]) => Math.abs(bx - x) < w && Math.abs(by - y) < h)) { pick = [x, y]; break; }
    }
    boxes.push(pick);
    return { g, s, q, lx: pick[0], ly: pick[1] };
  });
}
export function CrowdArt({ C, mode, P, at, ex = "full" }) {
  const crowd = crowdOf(P);
  const { k, t, wall } = at;            // k 번째 차례, 그 차례 안 시각, 벽시계(거닐기)
  const picks = pickOf(P, k, crowd);
  const chosen = picks.flatMap(({ g, list }) => list.map((i) => ({ g, s: crowd.byGrade[g - 1][i] })));
  const people = crowd.people.slice().sort((a, b) => a.hy - b.hy);
  const posMap = new Map(people.map((p) => [p, posOf(p, wall)]));
  // 돋보기: 아무 데나 몇 군데 → 첫 번째 뽑힌 학생
  const R = rng(hashSeed("lens", P.seed, k));
  const way = [[600 + R() * 400, 300 + R() * 300], [320 + R() * 300, 260 + R() * 420], [900 + R() * 350, 260 + R() * 420]];
  const first = chosen[0] ? posMap.get(chosen[0].s) : { x: 776, y: 470 };
  way.push([first.x, first.y - 24]);
  const kr = seg(t, CT.roam[0], CT.roam[1], E.lin);
  const segN = way.length - 1, u = Math.min(segN - 1e-6, kr * segN), si = Math.floor(u), uu = E.io(u - si);
  const lens = [lerp(way[si][0], way[si + 1][0], uu), lerp(way[si][1], way[si + 1][1], uu)];
  const lensO = seg(t, 0, 300) * (1 - seg(t, CT.spot[0] + 200, CT.spot[0] + 700));
  const kOut = 1 - seg(t, CT.out[0], CT.out[1]);
  const spotK = seg(t, CT.spot[0], CT.spot[0] + 500) * kOut;
  const showAt = (j) => CT.spot[0] + 300 + j * Math.min(700, 2200 / Math.max(1, chosen.length));
  const lid = `${sid(mode)}-lens`, mid = `${sid(mode)}-mask`;
  const top = cardTop(chosen, posMap, P, picks);
  const legO = top ? 1 : 1 - cardVis(t) * kOut;
  return (
    <g>
      <g transform={`translate(${BOX.x}, ${BOX.y})`}>
        <g id={sid(mode)}>
          <Ground C={C} />
          {people.map((p, i) => {
            const q = posMap.get(p);
            return (
              <g key={i} transform={`translate(${q.x.toFixed(1)}, ${q.y.toFixed(1)})${q.face < 0 ? " scale(-1, 1)" : ""}`}>
                <Figure p={p} step={q.step} />
              </g>
            );
          })}
        </g>
        {/* 불 켜기: 뽑힌 학생 말고는 어둡게 */}
        {spotK > 0.001 && (
          <g>
            <defs>
              <mask id={mid}>
                <rect x={0} y={0} width={BOX.w} height={BOX.h} fill="#fff" />
                {chosen.map(({ s }, j) => { const q = posMap.get(s); const kk = seg(t, showAt(j), showAt(j) + 400); return <circle key={j} cx={q.x} cy={q.y - 20} r={10 + 34 * kk} fill="#000" />; })}
              </mask>
            </defs>
            <rect x={0} y={0} width={BOX.w} height={BOX.h} rx={18} fill="#0b0f1e" opacity={0.48 * spotK} mask={`url(#${mid})`} />
            {labelSpots(chosen, posMap).map(({ g, s, q, ly, lx }, j) => {
              const kk = seg(t, showAt(j), showAt(j) + 400, E.back) * kOut;
              if (kk <= 0.001) return null;
              const lab = `${g}학년 ${s.name}`, w = uWidth(lab, 19, 800) + 22;
              return (
                <g key={j} opacity={Math.min(1, kk)}>
                  <circle cx={q.x} cy={q.y - 20} r={40} fill="none" stroke={GRADE[g - 1]} strokeWidth={4} />
                  <g transform={`translate(${lx}, ${ly}) scale(${kk})`}>
                    <rect x={-w / 2} y={-17} width={w} height={34} rx={17} fill="#fffaf0" stroke={GRADE[g - 1]} strokeWidth={3} />
                    <UText x={0} y={7} s={lab} size={19} weight={800} anchor="middle" fill="#3a2a1e" C={C} />
                  </g>
                </g>
              );
            })}
          </g>
        )}
        {/* 돋보기 */}
        {lensO > 0.001 && (
          <g opacity={lensO}>
            <defs><clipPath id={lid}><circle cx={lens[0]} cy={lens[1]} r={74} /></clipPath></defs>
            <g clipPath={`url(#${lid})`}>
              <circle cx={lens[0]} cy={lens[1]} r={74} fill="#ead6a8" />
              <use href={`#${sid(mode)}`} transform={`translate(${lens[0]} ${lens[1]}) scale(1.9) translate(${-lens[0]} ${-lens[1]})`} />
            </g>
            <circle cx={lens[0]} cy={lens[1]} r={74} fill="none" stroke="#7a5a2a" strokeWidth={9} />
            <circle cx={lens[0]} cy={lens[1]} r={74} fill="none" stroke="#e8c27a" strokeWidth={3} />
            <path d={`M${lens[0] + 52} ${lens[1] + 52}l46 46`} stroke="#5a3a1a" strokeWidth={16} strokeLinecap="round" />
            <path d={`M${lens[0] - 40} ${lens[1] - 44}q22 -16 48 -12`} fill="none" stroke="#fff" strokeWidth={4} opacity={0.6} strokeLinecap="round" />
          </g>
        )}
        <CrowdLegend P={P} C={C} o={legO} />
      </g>
      {ex !== "mini" && <CrowdCard C={C} mode={mode} P={P} picks={picks} crowd={crowd} t={t} k={k} kOut={kOut}
        top={top} />}
      {ex === "mini" && <CrowdChip C={C} mode={mode} P={P} picks={picks} crowd={crowd} t={t} k={k} kOut={kOut} top={top} />}
    </g>
  );
}

function CrowdLegend({ P, o = 1 }) {
  const items = [1, 2, 3].map((g) => `${g}학년 ${P[`a${g}`]}명 · ${P[`r${g}`]}명 뽑기`);
  const ws = items.map((s) => uWidth(s, 18, 800) + 44);
  const tw = ws.reduce((a, v) => a + v, 0) + 24;
  let x = 262 + 12;
  if (o <= 0.001) return null;
  return (
    <g opacity={o}>
      <rect x={262} y={704} width={tw} height={44} rx={22} fill="#fffaf0" opacity={0.92} stroke={OL} strokeWidth={1.2} />
      {items.map((s, i) => {
        const x0 = x; x += ws[i];
        return (
          <g key={i}>
            <circle cx={x0 + 16} cy={726} r={10} fill={GRADE[i]} stroke={OL} strokeWidth={1.2} />
            <text x={x0 + 32} y={732} fontFamily={SANS} fontSize={18} fontWeight={800} fill="#3a2a1e">{s}</text>
          </g>
        );
      })}
    </g>
  );
}

/** 결과 카드를 위 · 아래 어디에 둘지: 뽑힌 학생을 덜 가리는 쪽(같으면 아래) */
function cardTop(chosen, posMap, P, picks) {
  const lines = picks.filter((q) => q.list.length).length;
  const h = 120 + lines * 44;
  const cover = (y0, y1) => chosen.filter(({ s }) => { const y = posMap.get(s).y + BOX.y - 20; return y > y0 - 50 && y < y1 + 50; }).length;
  return cover(150, 150 + h) < cover(860 - h, 860);
}
const cardVis = (t) => seg(t, CT.card[0], CT.card[0] + 500, E.out) * (1 - seg(t, CT.card[1], CT.out[1]));
function CrowdCard({ C, mode, P, picks, crowd, t, k, kOut, top }) {
  const ko = cardVis(t);
  if (ko <= 0.001) return null;
  const { lines, last } = crowdLines(P, picks, crowd, mode);
  const who = picks.filter((q) => q.list.length).map(({ g, list }) => `${g}학년 ${list.map((i) => crowd.byGrade[g - 1][i].name).join(" · ")}`);
  const x = 330, w = 940, h = 120 + lines.length * 44, y = top ? 150 : 860 - h;
  return (
    <g opacity={ko * kOut} transform={`translate(0, ${(1 - ko) * 30})`}>
      <rect x={x} y={y} width={w} height={h} rx={24} fill={C.card} stroke={C.gold} strokeWidth={2.6} />
      <UText x={x + 30} y={y + 46} s={`${k + 1}번째 뽑기 — ${who.join(" / ")}`} size={25} weight={800} C={C} />
      {lines.map((L, j) => (
        <g key={j}>
          <circle cx={x + 40} cy={y + 82 + j * 44} r={9} fill={GRADE[L.g - 1]} />
          <MText x={x + 60} y={y + 90 + j * 44} s={L.s} size={22} weight={650} C={C} />
        </g>
      ))}
      <MText x={x + 30} y={y + h - 24} s={last} size={27} weight={800} fill={C.gold} C={C} />
    </g>
  );
}

/** 최소화: 큰 결과 카드 대신 뽑힌 학생과 확률 한 줄만 — 북적이는 운동장을 가리지 않게 */
function CrowdChip({ C, mode, P, picks, crowd, t, k, kOut, top }) {
  const ko = cardVis(t);
  if (ko <= 0.001) return null;
  const { last } = crowdLines(P, picks, crowd, mode);
  const who = picks.filter((q) => q.list.length).map(({ g, list }) => `${g}학년 ${list.map((i) => crowd.byGrade[g - 1][i].name).join("·")}`);
  const y = top ? 176 : 838;
  return (
    <g opacity={ko * kOut}>
      <Chip x={800} y={y - (top ? 0 : 44)} s={`${k + 1}번째 뽑기 — ${who.join(" / ")}`} size={21} C={C} />
      <Chip x={800} y={y + (top ? 44 : 0)} s={last} size={27} C={C} color={C.gold} />
    </g>
  );
}

/* ══════════ 액자 ══════════ */
export function crowdAt(P, el) {
  const e = el * P.sp;
  const k = Math.floor(e / CROWD.TURN);
  return { k, t: e - k * CROWD.TURN, wall: el };
}
const CROWD_DEF_EX = { ...CROWD_DEF, ex: "full" };
const fixCrowdEx = (p = {}) => ({ ...fixCrowd(p), ex: fixEx(p.ex) });
export function CrowdFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, CROWD_DEF_EX, fixCrowdEx);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const at = crowdAt(P, lab.elapsed());
  const regather = () => lab.setPrm({ seed: (P.seed % 999983) + 1 });
  useKeys({ ...baseKeys({ togglePause: lab.togglePause, restart: regather, toggleFs, onMode, poke }), d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); } }, inert);
  const grade = (g) => (
    <>
      <Setting label={`${g}학년`} sep={g > 1}><Stepper ui={ui} label={`${g}학년 인원`} value={P[`a${g}`]} options={CROWD.AS} unit="명" onChange={(v) => lab.setPrm({ [`a${g}`]: v })} poke={poke} /></Setting>
      <Setting label="뽑기"><Stepper ui={ui} label={`${g}학년에서 뽑는 수`} value={P[`r${g}`]} options={CROWD.RS.filter((r) => r <= P[`a${g}`])} unit="명" onChange={(v) => lab.setPrm({ [`r${g}`]: v }, (o, n, el) => el)} poke={poke} /></Setting>
    </>
  );
  const settings = (
    <>
      {grade(1)}{grade(2)}{grade(3)}
      <Setting label="풀이" sep><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
    </>
  );
  const title = { e: "북적북적 학년별 뽑기", m: "북적북적 학년별 뽑기 — 확률" };
  const sub = "축제 날 운동장, 돋보기가 멈추는 사람은 누구?";
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="북적이는 운동장에서 학년별로 학생을 뽑는 액자">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <CrowdArt C={C} mode={Ly.mode} P={P} at={at} ex={P.ex} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={regather} restartTitle="새로 모이기"
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={at.t / CROWD.TURN} />
    </>
  );
}

export const CrowdThumb = memo(function CrowdThumb({ C, mode = "m" }) {
  const P = fixCrowd({ ...CROWD_DEF, seed: 2 });
  return <CrowdArt C={C} mode={`${mode}-thumb`} P={P} at={{ k: 0, t: 3600, wall: 3600 }} />;
});
