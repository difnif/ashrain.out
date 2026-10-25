// 장면 4 — 직육면체·정육면체·삼각기둥의 전개도(초등) ↔ 공간에서의 위치 관계(중등)
// 세 입체가 같은 박자로 펼쳐졌다 접힌다. 펼친 동안 초등은 "만나는 모서리" 짝을, 중등은 모서리 AB 의
// 두 자리를 같은 색으로 보여 주고(접으면 하나로 합쳐진다), 접힌 뒤 초등은 면·모서리·꼭짓점을, 중등은
// 모서리 AB 와 다른 모서리(정육면체는 면)의 위치 관계를 색으로 나눈다.
import { seg, E, camera, lerp, mix3, normal3, mul3, facing, sub2, add2, mul2, len2 } from "../core";
import { Board, Caption, Faces, Path, Lbl, Dot } from "../draw";
import { SOLIDS, foldAt, netEdgesOf } from "../solids";
import { NETS, sameEdge } from "../facts";

const ORDER = ["cuboid", "cube", "prism"];
const PH = [["show", 1500], ["unfold", 3200], ["flat", 3000], ["fold", 3200], ["facts", 5600]];
const SEGLEN = PH.reduce((a, [, m]) => a + m, 0);
const AT = {};
{ let a = 0; for (const [n, m] of PH) { AT[n] = [a, a + m]; a += m; } }
const DUR = SEGLEN * ORDER.length;
const VIEW = {
  cuboid: { sSolid: 104, sNet: 62 },
  cube: { sSolid: 100, sNet: 54 },
  prism: { sSolid: 106, sNet: 62 },
};

/* ── 정적 자료: 면-모서리 인접, 하이라이트할 전개도 변 ── */
const KEY = (p) => p.map((v) => Math.round(v * 1000)).join(",");
const PREP = Object.fromEntries(ORDER.map((id) => {
  const S = SOLIDS[id];
  const folded = foldAt(S, 0);
  const faceKeys = Object.fromEntries(S.faces.map((f) => [f.id, new Set(folded[f.id].map(KEY))]));
  const adj = Object.fromEntries(S.edges.map((e) => {
    const [p, q] = [S.V[e[0]], S.V[e[1]]];
    return [e, S.faces.filter((f) => faceKeys[f.id].has(KEY(p)) && faceKeys[f.id].has(KEY(q))).map((f) => f.id)];
  }));
  const net = (name) => netEdgesOf(S, S.V[name[0]], S.V[name[1]]);
  return [id, { S, adj, pairsE: NETS[id].pairsE.map((nm) => ({ nm, at: net(nm) })), abM: net("AB") }];
}));

function camFor(id, tau, t) {
  const v = VIEW[id], S = SOLIDS[id];
  const fk = seg(tau, AT.unfold[0], AT.unfold[1], E.io) - seg(tau, AT.fold[0], AT.fold[1], E.io);
  const sway = -30 + 9 * Math.sin((t / 26000) * Math.PI * 2);
  return {
    fk,
    cam: camera({
      yaw: lerp(sway, -6, fk), pitch: lerp(24, 66, fk), scale: lerp(v.sSolid, v.sNet, fk),
      cx: 540, cy: lerp(486, 468, fk), target: mix3(S.center, S.netCenter, fk),
    }),
  };
}

function Solid({ id, tau, t, C, mode }) {
  const { S, adj, pairsE, abM } = PREP[id];
  const { cam, fk } = camFor(id, tau, t);
  const U = seg(tau, AT.unfold[0], AT.unfold[1], E.lin) - seg(tau, AT.fold[0], AT.fold[1], E.lin);
  const pos = foldAt(S, U);
  const facts = tau >= AT.facts[0];
  const fT = tau - AT.facts[0];
  const center = S.center;
  const outN = (pts) => mul3(normal3(pts), -1);             // 종이의 윗면이 안쪽이 되도록 접히므로 바깥 법선은 반대
  const frontOf = (fid) => facing(cam, outN(pos[fid]));
  const isM = mode === "m";
  // 면 색 · 투명도
  const faceO = isM && facts ? lerp(0.86, 0.3, seg(fT, 0, 600)) : 0.86;
  const pulse = (i) => (!isM && facts ? seg(fT, 200 + i * 230, 420 + i * 230) * (1 - seg(fT, 520 + i * 230, 900 + i * 230)) : 0);
  // 정육면체(중등): 직선 AB 와 면의 관계로 면을 칠한다
  const planeCat = isM && id === "cube" && facts ? NETS.cube.planesM : null;
  const catCol = { meet: "coral", parallel: "sky", skew: "leaf", contain: "coral", perp: "leaf" };
  const catT = [600, 2100, 3600];
  const faceColor = (f) => {
    if (planeCat) {
      const name = NETS.cube.faceName[f.id];
      const ci = planeCat.findIndex((c) => c.list.includes(name));
      const on = ci >= 0 && fT >= catT[ci];
      return on ? C[catCol[planeCat[ci].cat]] : C.soft;
    }
    return C[f.color];
  };
  const faces = S.faces.map((f, i) => {
    let o = 1, edge, sw = 2.6 + 4 * pulse(i);
    if (planeCat) {
      const ci = planeCat.findIndex((c) => c.list.includes(NETS.cube.faceName[f.id]));
      const on = ci >= 0 && fT >= catT[ci];
      o = on ? 1.7 : 0.6;
      if (on) { edge = C[catCol[planeCat[ci].cat]]; sw = 4.5; }
    }
    return { key: f.id, pts: pos[f.id], color: faceColor(f), n: outN(pos[f.id]), o, edge, sw };
  });
  // 펼친 동안: 같은 색 모서리(초등) / 모서리 AB 의 두 자리(중등)
  const hlO = seg(tau, AT.unfold[0] + 1600, AT.flat[0] + 300) * (1 - seg(tau, AT.fold[1] - 300, AT.fold[1] + 500));
  const hl = isM ? [{ at: abM, col: C.gold }] : pairsE.map((p, i) => ({ at: p.at, col: i ? C.sky : C.coral }));
  const netSeg = (h) => {
    const pts = pos[h.face];
    return [cam.p(pts[h.i]), cam.p(pts[(h.i + 1) % pts.length])];
  };
  // 접힌 뒤: 모서리 색
  const edgeCol = (e) => {
    if (!facts) return null;
    if (isM) {
      if (sameEdge(e, "AB")) return { col: C.gold, w: 8 };
      if (id === "cube") return null;
      const cats = NETS[id].relM;
      for (let k = 0; k < cats.length; k++) if (cats[k].list.some((x) => sameEdge(x, e)) && fT >= catT[k]) return { col: C[catCol[cats[k].cat]], w: 6.5 };
      return null;
    }
    const idx = S.edges.indexOf(e);
    const k = seg(fT, 1700 + idx * 110, 2000 + idx * 110);
    return k > 0 ? { col: C.gold, w: 3 + 3.5 * k, o: k } : null;
  };
  const hidden = (e) => (adj[e] || []).every((fid) => !frontOf(fid));
  const P = (name) => cam.p(S.V[name]);
  const c2 = cam.p(center);
  const labelAt = (name) => {
    const p = P(name), d = sub2(p, c2), L = len2(d) || 1;
    return add2(p, mul2(d, 32 / L));
  };
  const labO = isM ? (1 - seg(tau, AT.unfold[0], AT.unfold[0] + 400)) + seg(tau, AT.fold[1] - 200, AT.fold[1] + 400) : 0;
  const vtxE = !isM && facts ? Object.keys(S.V).map((n, i) => ({ n, k: seg(fT, 3500 + i * 160, 3800 + i * 160, E.back) })) : [];
  return (
    <g>
      <Faces cam={cam} faces={faces} C={C} fillO={faceO} sw={2.6} backDash={U < 0.08} backO={0.55} />
      {hl.map((h, i) => hlO > 0 && h.at.map((a, j) => {
        const [p, q] = netSeg(a);
        return <g key={`${i}-${j}`} opacity={hlO}>
          <Path pts={[p, q]} stroke={h.col} sw={16} o={0.28} />
          <Path pts={[p, q]} stroke={h.col} sw={7} />
        </g>;
      }))}
      {facts && S.edges.map((e) => {
        const st = edgeCol(e);
        if (!st) return null;
        const hid = hidden(e);
        return <Path key={e} pts={[P(e[0]), P(e[1])]} stroke={st.col} sw={hid ? st.w * 0.6 : st.w}
          dash={hid ? "12 9" : undefined} o={(st.o ?? 1) * (hid ? 0.75 : 1)} />;
      })}
      {vtxE.map(({ n, k }) => k > 0 && <Dot key={n} p={P(n)} r={9 * k} fill={C.gold} ring={C.halo} />)}
      {labO > 0.01 && Object.keys(S.V).map((n) => {
        const q = labelAt(n);
        return <Lbl key={n} x={q[0]} y={q[1]} s={n} size={30} fill={n === "A" || n === "B" ? C.gold : C.ink} C={C} o={Math.min(1, labO)} />;
      })}
    </g>
  );
}

function Scene({ t, C, mode }) {
  const k = Math.min(ORDER.length - 1, Math.floor(t / SEGLEN));
  const tau = t - k * SEGLEN;
  const id = ORDER[k];
  const fadeIn = k === 0 ? 1 : seg(tau, 0, 600);
  const fadeOut = k === ORDER.length - 1 ? 1 : 1 - seg(tau, SEGLEN - 600, SEGLEN);
  const prevO = k > 0 ? 1 - seg(tau, 0, 600) : 0;
  const N = NETS[id];
  const base = k * SEGLEN;
  const at = (ph, d = 0) => base + AT[ph][0] + d;
  const T = mode === "m" ? N.M : N.E;
  return (
    <g>
      {prevO > 0 && <g opacity={prevO}><Solid id={ORDER[k - 1]} tau={SEGLEN - 1} t={t} C={C} mode={mode} /></g>}
      <g opacity={fadeIn * fadeOut}><Solid id={id} tau={tau} t={t} C={C} mode={mode} /></g>
      <Board x={1056} y={250} t={t} C={C} lines={T.board.map((L, i) => ({
        t: at("facts", L.d ?? (i === 0 ? 100 : [0, 600, 2100, 3600][i])), s: L.s, k: L.k, dot: L.dot, u: base + SEGLEN - 200, row: i,
      }))} />
      <Caption t={t} C={C} caps={[
        { t: at("show", 200), s: T.cap[0] },
        { t: at("flat", -600), s: T.cap[1] },
        { t: at("fold", 400), s: T.cap[2] },
        { t: at("facts", 300), s: T.cap[3] },
      ]} />
    </g>
  );
}

export default {
  key: "nets",
  dur: DUR,
  title: { e: "입체도형의 전개도", m: "공간에서의 위치 관계" },
  sub: { e: "초등 · 직육면체·정육면체·각기둥", m: "중등 · 직선과 직선, 직선과 평면" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
