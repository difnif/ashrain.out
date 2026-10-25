// 장면 6 — 구 (초등: 원이 돌며 구가 되고 각 부분의 이름 ↔ 중등: 반원이 1회전해 구, 겉넓이와 부피)
// 같은 회전축·같은 반지름(6 cm). 회전 박자, 이름 박자(↔ 겉넓이), 본 모양 박자(↔ 부피)가 맞물린다.
import { beats, seg, E, camera, lerp, rad, clamp } from "../core";
import { Board, Caption, Path, Lbl, Dot } from "../draw";
import { SPHERE } from "../facts";

const { R } = SPHERE;
const B = beats([["intro", 2400], ["spin", 8200], ["part", 11000], ["more", 7600], ["hold", 2800]]);
const CEN = [440, 452];
const SC = 34;                                     // 1 cm = 34 px → 반지름 204 px
const cam = camera({ yaw: 0, pitch: 12, scale: SC, cx: CEN[0], cy: CEN[1], target: [0, 0, 0] });
const RP = R * SC;

/** 축을 품은 평면(방향각 phi) 위의 원 둘레 점들: half=true 면 오른쪽 반원(축 포함 닫힌 도형) */
function diskPts(phi, half) {
  const out = [];
  const N = 64;
  const a0 = half ? -90 : 0, a1 = half ? 90 : 360;
  for (let i = 0; i <= N; i++) {
    const th = rad(a0 + ((a1 - a0) * i) / N);
    const rr = R * Math.cos(th);
    out.push(cam.p([rr * Math.cos(phi), rr * Math.sin(phi), R * Math.sin(th)]));
  }
  return out;
}
/** 구 위의 곡선(3D 점 목록)을 앞/뒤로 나눠 그린다 */
function SphereCurve({ pts3, C, col, sw = 2.6, o = 1, backO = 0.3 }) {
  const segs = [];
  let cur = null, curFront = null;
  for (const p of pts3) {
    const q = cam.p(p), front = cam.v(p)[2] < 0.0001;
    if (front !== curFront) { if (cur && cur.length > 1) segs.push({ front: curFront, pts: cur }); cur = cur ? [cur.at(-1)] : []; curFront = front; }
    cur.push(q);
  }
  if (cur && cur.length > 1) segs.push({ front: curFront, pts: cur });
  return <g opacity={o}>{segs.map((s, i) => <Path key={i} pts={s.pts} stroke={col || C.ink} sw={s.front ? sw : sw * 0.8}
    dash={s.front ? undefined : "7 7"} o={s.front ? 1 : backO} />)}</g>;
}
const lat = (z, rot = 0) => Array.from({ length: 73 }, (_, i) => { const a = (i / 72) * Math.PI * 2 + rot, rr = Math.sqrt(Math.max(0, R * R - z * z)); return [rr * Math.cos(a), rr * Math.sin(a), z]; });
const mer = (lam) => Array.from({ length: 49 }, (_, i) => { const th = -Math.PI / 2 + (i / 48) * Math.PI; return [R * Math.cos(th) * Math.cos(lam), R * Math.cos(th) * Math.sin(lam), R * Math.sin(th)]; });

function Ball({ C, o, rot = 0, lines = 1, gid }) {
  if (o <= 0.001) return null;
  return (
    <g opacity={o}>
      <defs>
        <radialGradient id={gid} cx="38%" cy="32%" r="72%">
          <stop offset="0" stopColor={C.sky} stopOpacity="0.95" />
          <stop offset="0.7" stopColor={C.sky} stopOpacity="0.55" />
          <stop offset="1" stopColor={C.paper} stopOpacity="0.55" />
        </radialGradient>
      </defs>
      <circle cx={CEN[0]} cy={CEN[1]} r={RP} fill={`url(#${gid})`} stroke={C.ink} strokeWidth={3} />
      <g opacity={0.55 * lines}>
        {[-3.6, 0, 3.6].map((z) => <SphereCurve key={z} pts3={lat(z)} C={C} sw={1.8} backO={0.25} />)}
        {[0, 1, 2, 3, 4, 5].map((k) => <SphereCurve key={k} pts3={mer(rot + (k * Math.PI) / 6)} C={C} sw={1.8} backO={0.2} />)}
      </g>
    </g>
  );
}

function Axis({ C, o = 1, label }) {
  const top = cam.p([0, 0, R + 1.6]), bot = cam.p([0, 0, -R - 1.6]);
  return <g opacity={o}>
    <Path pts={[top, bot]} stroke={C.soft} sw={2.6} dash="14 9" />
    {label && <Lbl x={top[0] + 26} y={top[1] + 10} s={label} size={32} fill={C.soft} C={C} />}
  </g>;
}

/* ══════════ 초등 ══════════ */
function Elem({ t, C }) {
  const tau = t - B.a.spin;
  // 빠르게 돌수록 잔상이 겹쳐 공 모양이 된다
  const turns = tau <= 0 ? 0 : tau < 4200 ? 0.5 * Math.pow(tau / 4200, 2) * 4.2 : 2.1 + (tau - 4200) / 1000 * 2.2;
  const phi = turns * Math.PI * 2;
  const ballO = seg(t, B.a.spin + 4600, B.b.spin, E.sine);
  const diskO = 1 - seg(t, B.b.spin - 1600, B.b.spin);
  const trail = clamp(tau / 2600, 0, 1);
  const rot = t * 0.00022;
  const pt = (deg2) => cam.p([R * Math.cos(rad(deg2)), 0, R * Math.sin(rad(deg2))]);
  const radii = [0, 125, 215];
  const rT = (i) => B.a.part + 2200 + i * 900;
  const diaT = B.a.part + 6400;
  const views = [["위에서", 300], ["앞에서", 452], ["옆에서", 604]];
  const vO = (i) => seg(t, B.a.more + 600 + i * 900, B.a.more + 1100 + i * 900);
  return (
    <g>
      <Axis C={C} o={seg(t, 300, 1200) * (1 - 0.6 * ballO)} />
      {/* 도는 원판과 잔상 */}
      <g opacity={diskO}>
        {trail > 0 && Array.from({ length: 9 }, (_, k) => k + 1).map((k) => (
          <Path key={k} pts={diskPts(phi - k * 0.16, false)} closed fill={C.coral} fo={0.07 * trail} stroke={C.coral} sw={1.6} o={(1 - k / 10) * 0.6 * trail} />
        ))}
        <Path pts={diskPts(phi, false)} closed fill={C.coral} fo={0.45} stroke={C.ink} sw={3} o={seg(t, 200, 1200)} />
      </g>
      <Ball C={C} o={ballO} rot={rot} gid={`sphE-${C.name}`} />
      {/* 이름 */}
      <g opacity={seg(t, B.a.part + 400, B.a.part + 900)}>
        <Dot p={CEN} r={9} fill={C.gold} />
        <Lbl x={CEN[0] + 18} y={CEN[1] + 40} s="구의 중심" size={30} anchor="start" fill={C.gold} C={C} />
      </g>
      {radii.map((a, i) => {
        const k = seg(t, rT(i), rT(i) + 700, E.out);
        if (k <= 0) return null;
        const end = pt(a), e2 = [lerp(CEN[0], end[0], k), lerp(CEN[1], end[1], k)];
        const mid = [(CEN[0] + end[0]) / 2, (CEN[1] + end[1]) / 2];
        return <g key={a}>
          <Path pts={[CEN, e2]} stroke={C.gold} sw={5} />
          {k >= 1 && <Lbl x={mid[0] + (i === 1 ? -6 : 14)} y={mid[1] - 26} s={`${R} cm`} size={28} fill={C.gold} C={C} />}
        </g>;
      })}
      {t >= diaT && <g opacity={seg(t, diaT, diaT + 600)}>
        <Path pts={[pt(200), pt(20)]} stroke={C.coral} sw={5} />
        <Lbl x={pt(20)[0] + 70} y={pt(20)[1] - 10} s={`${2 * R} cm`} size={30} fill={C.coral} C={C} />
      </g>}
      {/* 어느 쪽에서 보아도 원 */}
      {views.map(([s, y], i) => (
        <g key={s} opacity={vO(i)}>
          <circle cx={812} cy={y} r={50} fill={C.sky} fillOpacity={0.35} stroke={C.ink} strokeWidth={2.6} />
          <Lbl x={892} y={y} s={s} size={28} anchor="start" C={C} />
        </g>
      ))}
      <Board x={1090} y={250} t={t} C={C} size={36} lh={60} lines={[
        { t: B.a.part + 500, s: "구의 중심", k: "h" },
        { t: B.a.part + 800, s: "가장 안쪽에 있는 점" },
        { t: B.a.part + 2200, s: "구의 반지름", k: "h" },
        { t: B.a.part + 2500, s: `중심과 겉면을 잇는 선분 · ${R} cm` },
        { t: diaT, s: "구의 지름", k: "h" },
        { t: diaT + 300, s: SPHERE.E.dia },
        { t: B.a.more + 600, s: "위·앞·옆에서 본 모양", k: "h" },
        { t: B.a.more + 3200, s: "‹모두 원›" },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "원을 지름을 축으로 빙글빙글 돌리면?" },
        { t: B.a.spin + 3400, s: "공 모양이 생겨요 — 구" },
        { t: B.a.part + 300, s: "구에서 가장 안쪽에 있는 점이 구의 중심" },
        { t: B.a.part + 3600, s: "구의 반지름은 모두 같아요" },
        { t: diaT, s: "지름은 반지름의 2배" },
        { t: B.a.more, s: "구는 어느 쪽에서 보아도 원 모양" },
      ]} />
    </g>
  );
}

/* ══════════ 중등 ══════════ */
function Mid({ t, C }) {
  const sweep = seg(t, B.a.spin + 300, B.b.spin - 1500, E.io);   // 0 → 1 바퀴
  const phi = sweep * Math.PI * 2;
  const ballO = seg(t, B.b.spin - 1600, B.b.spin, E.sine);
  const rot = t * 0.00022;
  const traceN = Math.floor(sweep * 18);
  // 겉넓이: 원 4개
  const cT = (i) => B.a.part + 1800 + i * 700;
  const cpos = [[790, 300], [970, 300], [790, 480], [970, 480]];
  const cR = 78;
  // 부피: 원기둥이 구를 감싼다
  const cyl = seg(t, B.a.more + 300, B.a.more + 1600, E.out);
  const ring = (z) => Array.from({ length: 73 }, (_, i) => { const a = (i / 72) * Math.PI * 2; return [R * Math.cos(a), R * Math.sin(a), z]; });
  const L1 = cam.p([-R, 0, R]), L2 = cam.p([-R, 0, -R]), R1 = cam.p([R, 0, R]), R2 = cam.p([R, 0, -R]);
  return (
    <g>
      <Axis C={C} o={seg(t, 300, 1200)} label="*l*" />
      {/* 쓸고 지나간 자리 */}
      {Array.from({ length: traceN }, (_, k) => k).map((k) => (
        <SphereCurve key={k} pts3={mer((k * Math.PI * 2) / 18)} C={C} col={C.lilac} sw={2} o={(1 - ballO) * 0.75} backO={0.3} />
      ))}
      <Path pts={diskPts(phi, true)} closed fill={C.coral} fo={0.5} stroke={C.ink} sw={3} o={seg(t, 200, 1200) * (1 - ballO * 0.9)} />
      <Ball C={C} o={ballO} rot={rot} lines={1 - 0.5 * cyl} gid={`sphM-${C.name}`} />
      {/* 겉넓이 */}
      <g opacity={1 - seg(t, B.a.more - 400, B.a.more + 200)}>
        <g opacity={seg(t, B.a.part + 400, B.a.part + 1000)}>
          <SphereCurve pts3={lat(0)} C={C} col={C.gold} sw={4} backO={0.5} />
          <Path pts={[CEN, cam.p([R, 0, 0])]} stroke={C.gold} sw={3} />
          <Lbl x={CEN[0] + RP / 2} y={CEN[1] - 22} s="*r*" size={34} fill={C.gold} C={C} />
        </g>
        {cpos.map(([x, y], i) => {
          const k = seg(t, cT(i), cT(i) + 600, E.back);
          if (k <= 0) return null;
          return <g key={i} transform={`translate(${x} ${y}) scale(${k})`}>
            <circle r={cR} fill={C.gold} fillOpacity={0.3} stroke={C.gold} strokeWidth={3} />
            <Path pts={[[0, 0], [cR, 0]]} stroke={C.gold} sw={2.4} />
            <Lbl x={cR / 2} y={-18} s="*r*" size={26} fill={C.gold} C={C} />
          </g>;
        })}
      </g>
      {/* 부피 */}
      {cyl > 0 && <g opacity={cyl}>
        <SphereCurve pts3={ring(R)} C={C} col={C.leaf} sw={3.4} backO={0.9} />
        <SphereCurve pts3={ring(-R)} C={C} col={C.leaf} sw={3.4} backO={0.6} />
        <Path pts={[L1, L2]} stroke={C.leaf} sw={3.4} />
        <Path pts={[R1, R2]} stroke={C.leaf} sw={3.4} />
        <Lbl x={R1[0] + 46} y={(R1[1] + R2[1]) / 2} s="2*r*" size={32} anchor="start" fill={C.leaf} C={C} />
      </g>}
      <Board x={1090} y={250} t={t} C={C} size={36} lh={60} lines={[
        { t: B.a.part + 400, s: "구의 겉넓이", k: "h" },
        { t: B.a.part + 4800, s: "*S* = (원 4개) = 4π*r*²" },
        { t: B.a.part + 6600, s: SPHERE.M.area },
        { t: B.a.more + 300, s: "구의 부피", k: "h" },
        { t: B.a.more + 1600, s: SPHERE.M.cylV },
        { t: B.a.more + 3600, s: SPHERE.M.vol },
        { t: B.a.more + 5400, s: "*V* = {4/3}π*r*³" },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: "반원을 지름(회전축 l)을 축으로 한 바퀴 돌리면?" },
        { t: B.a.spin + 3400, s: "반원이 지나간 자리 — 회전체, 구" },
        { t: B.a.part + 300, s: "구의 겉넓이는 반지름이 같은 원 4개의 넓이" },
        { t: B.a.more, s: "구를 꼭 맞게 감싸는 원기둥" },
        { t: B.a.more + 3400, s: "구의 부피는 원기둥 부피의 {2/3}" },
      ]} />
    </g>
  );
}

export default {
  key: "sphere",
  dur: B.dur,
  title: { e: "구", m: "구의 겉넓이와 부피" },
  sub: { e: "초등 · 구의 중심과 반지름", m: "중등 · 회전체" },
  render: (mode, t, C) => (mode === "m" ? <Mid t={t} C={C} /> : <Elem t={t} C={C} />),
};
