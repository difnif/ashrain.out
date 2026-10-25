// 장면 5 — 원기둥의 전개도(초등 3.14 ↔ 중등 π)
// 뚜껑(밑면)이 앞쪽 접선을 경첩으로 열리고, 옆면이 앞쪽 모선을 붙든 채 곡률이 풀리며 직사각형으로 펴진다.
// 밑면의 둘레와 옆면의 가로를 같은 금빛 선으로 그려 "가로 = 밑면의 둘레"가 눈으로 보이게 한다.
import { beats, seg, E, camera, lerp, mix3, axisRot, apply, rad, lambert, shade, facing } from "../core";
import { Board, Caption, Path, Lbl, Dim } from "../draw";
import { CYL } from "../facts";

const { R, H } = CYL;
const B = beats([["intro", 2400], ["open", 2600], ["unroll", 3800], ["dims", 2200], ["calc", 9400], ["roll", 3800], ["vol", 3400], ["hold", 2200]]);
const NS = 72;                                  // 옆면 띠 수
const LIDN = 56;

/** 옆면 위의 점: 호 길이 s(−πr~πr, 앞 모선 0) · 높이 z · 펼침 u */
function sidePt(s, z, u) {
  if (u >= 0.9995) return [s, -R, z];
  const rho = R / (1 - u), b = s / rho;
  return [rho * Math.sin(b), -R + rho * (1 - Math.cos(b)), z];
}
const sideN = (s, u) => { const rho = R / (1 - Math.min(u, 0.9995)), b = s / rho; return [Math.sin(b), -Math.cos(b), 0]; };

function lid(top, ang) {
  // 뚜껑: 앞쪽 접선(y = −R)을 경첩으로 회전. 위 뚜껑은 위로, 아래 뚜껑은 아래로 젖혀진다.
  const z = top ? H : 0;
  const M = axisRot([0, -R, z], [1, 0, 0], rad(top ? ang : -ang));
  const pts = [];
  for (let i = 0; i < LIDN; i++) { const a = (i / LIDN) * Math.PI * 2; pts.push(apply(M, [R * Math.cos(a), R * Math.sin(a), z])); }
  const n = apply({ R: M.R, t: [0, 0, 0] }, [0, 0, top ? 1 : -1]);
  return { pts, n, c: apply(M, [0, 0, z]) };
}

function camAt(t) {
  const k = seg(t, B.a.unroll, B.b.unroll, E.io) - seg(t, B.a.roll, B.b.roll, E.io);
  // 뚜껑이 열리기 시작할 때부터 물러선다 — 펼친 전개도(세로 20칸)가 화면에 들어오게
  const z = seg(t, B.a.open - 300, B.a.unroll + 600, E.io) - seg(t, B.a.roll + 1600, B.a.vol + 1000, E.io);
  const sway = -24 + 8 * Math.sin((t / 22000) * Math.PI * 2);
  return {
    k,
    cam: camera({
      yaw: lerp(sway, 0, k), pitch: lerp(20, 3, k), scale: lerp(47, 29.5, z),
      cx: 470, cy: lerp(470, 456, z), target: mix3([0, 0, H / 2], [0, -R, H / 2], k),
    }),
  };
}

function Scene({ t, C, mode }) {
  const T = mode === "m" ? CYL.M : CYL.E;
  const { cam, k: camK } = camAt(t);
  const lidA = 90 * (seg(t, B.a.open, B.b.open, E.io) - seg(t, B.a.roll + 1700, B.b.roll, E.io));
  const u = seg(t, B.a.unroll, B.b.unroll, E.io) - seg(t, B.a.roll, B.a.roll + 2000, E.io);
  const appear = seg(t, 100, 1300);
  // 면 모으기
  const items = [];
  for (let i = 0; i < NS; i++) {
    const s0 = -Math.PI * R + (2 * Math.PI * R * i) / NS, s1 = -Math.PI * R + (2 * Math.PI * R * (i + 1)) / NS;
    const sm = (s0 + s1) / 2;
    const pts = [sidePt(s0, 0, u), sidePt(s1, 0, u), sidePt(s1, H, u), sidePt(s0, H, u)];
    items.push({ kind: "side", pts, n: sideN(sm, u), s0, s1 });
  }
  for (const top of [true, false]) { const L = lid(top, lidA); items.push({ kind: top ? "top" : "bot", pts: L.pts, n: L.n }); }
  const P = items.map((it) => {
    const q = it.pts.map((p) => cam.p(p));
    return { ...it, q, depth: q.reduce((a, b) => a + b[2], 0) / q.length, front: facing(cam, it.n) };
  });
  P.sort((a, b) => b.depth - a.depth);
  const col = (it) => (it.kind === "side" ? C.sky : C.coral);
  const lidClosed = lidA < 4;
  // 금빛 둘레: 옆면의 위·아래 가장자리 + 뚜껑 둘레
  const rimSeg = (it, z) => [cam.p(sidePt(it.s0, z, u)), cam.p(sidePt(it.s1, z, u))];
  const dimO = seg(t, B.a.dims, B.a.dims + 600) * (1 - seg(t, B.a.roll, B.a.roll + 500));
  const lab3O = seg(t, 900, 1700) * (1 - seg(t, B.a.open, B.a.open + 400)) + seg(t, B.b.roll - 200, B.b.roll + 500);
  // 펼친 그림의 모서리 위치(화면)
  const W2 = Math.PI * R;
  const rBL = cam.p([-W2, -R, 0]), rBR = cam.p([W2, -R, 0]), rTL = cam.p([-W2, -R, H]);
  const topC = cam.p(lid(true, 90).c), botC = cam.p(lid(false, 90).c);
  const rpx = R * cam.scale;
  const c3 = cam.p([0, 0, H]);
  return (
    <g opacity={appear}>
      {P.map((it, i) => {
        const k = lambert(cam, it.n);
        const base = col(it);
        const o = it.front ? 0.9 : 0.5;
        return <path key={i} d={"M" + it.q.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join("L") + "Z"}
          fill={shade(base, k)} fillOpacity={o} stroke={it.kind === "side" ? shade(base, k) : C.ink}
          strokeWidth={it.kind === "side" ? 0.8 : 2.4} strokeOpacity={it.kind === "side" ? o : 0.9} />;
      })}
      {/* 금빛 둘레 */}
      {P.filter((it) => it.kind === "side").map((it, i) => {
        const vis = it.front || u > 0.06;
        return [H, 0].map((z) => {
          const solid = vis || (z === H && lidClosed);
          return <Path key={`${i}-${z}`} pts={rimSeg(it, z)} stroke={C.gold} sw={solid ? 5 : 3} dash={solid ? undefined : "8 8"} o={solid ? 1 : 0.6} cap="butt" />;
        });
      })}
      {P.filter((it) => it.kind !== "side").map((it) => (
        <Path key={it.kind} pts={it.q} closed stroke={C.gold} sw={it.front || lidA > 30 ? 5 : 3} dash={it.front || lidA > 30 ? undefined : "8 8"} />
      ))}
      {/* 3D 치수 */}
      {lab3O > 0.001 && <g opacity={Math.min(1, lab3O)}>
        <Path pts={[c3, cam.p([R, 0, H])]} stroke={C.ink} sw={3} />
        <Lbl x={(c3[0] + cam.p([R, 0, H])[0]) / 2} y={c3[1] - 26} s={`${R} cm`} size={30} C={C} />
        <Dim A={cam.p([R + 0.9, 0, 0])} B={cam.p([R + 0.9, 0, H])} off={-10} lofs={-50} s={`${H} cm`} C={C} size={30} />
      </g>}
      {/* 펼친 그림 치수 */}
      {dimO * camK > 0.001 && <g opacity={dimO * camK}>
        <Dim A={rBL} B={rBR} off={-36} lofs={-34} at={0.17} s={T.side} C={C} color={C.gold} size={32} />
        <Dim A={rBL} B={rTL} off={36} lofs={46} s={`${H} cm`} C={C} size={30} />
        <Path pts={[topC, [topC[0] + rpx, topC[1]]]} stroke={C.ink} sw={2.6} />
        <Lbl x={topC[0] + rpx / 2} y={topC[1] - 24} s={`${R} cm`} size={28} C={C} />
        <Path pts={[botC, [botC[0] + rpx, botC[1]]]} stroke={C.ink} sw={2.6} />
        <Lbl x={botC[0] + rpx / 2} y={botC[1] - 24} s={`${R} cm`} size={28} C={C} />
      </g>}
      <Board x={890} y={176} t={t} C={C} size={36} lh={56} lines={T.board.map((L, i) => ({ ...L, t: B.a.calc + L.d, row: i }))} />
      <Caption t={t} C={C} caps={[
        { t: 300, s: `밑면의 반지름 ${R} cm, 높이 ${H} cm인 원기둥` },
        { t: B.a.open, s: "밑면 두 개를 열고" },
        { t: B.a.unroll, s: "옆면을 펼치면 직사각형" },
        { t: B.a.dims, s: "옆면의 가로 = 밑면의 둘레, 세로 = 높이" },
        { t: B.a.calc + 4200, s: mode === "m" ? "π 를 그대로 두고 계산해요" : "원주율 3.14로 계산해요" },
        { t: B.a.roll, s: "다시 말아 올리면 원기둥" },
        { t: B.a.vol, s: mode === "m" ? `부피 = 밑넓이 × 높이 = ${CYL.M.vol} cm³` : "밑면의 둘레가 옆면의 가로가 되었어요" },
      ]} />
    </g>
  );
}

export default {
  key: "cylinder",
  dur: B.dur,
  title: { e: "원기둥의 전개도", m: "원기둥의 겉넓이와 부피" },
  sub: { e: "초등 · 원주율 3.14", m: "중등 · 원주율 π" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
