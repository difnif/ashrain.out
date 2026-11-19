// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 로봇 다섯 대의 모양 (hanoi3d/robots.js)
// 관절 자리는 kin.js 가 낸다 — 여기서는 그 자리에 맞춰 몸통 · 팔다리 · 집게를 놓기만 한다.
// 모두 기본 도형(둥근 상자 · 캡슐 · 원기둥 · 공)과 세라믹 · 카본 · 금속 재질, 빛나는 LED 로 만든다(파일을 내려받지 않는다).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { KINS } from "./kin.js";

const _y = new THREE.Vector3(0, 1, 0), _v = new THREE.Vector3(), _x = new THREE.Vector3(), _z = new THREE.Vector3(), _m = new THREE.Matrix4();
const put = (o, p) => o.position.set(p[0], p[1], p[2]);
/**
 * 막대(+Y 로 만든 모양)를 a → b 로 놓는다. side 를 주면 모양의 +X 가 그쪽을 보게(모난 팔이 비틀리지 않게).
 * len 을 주면 길이 len 으로 만든 모양을 두 점 사이 길이에 맞춰 늘인다.
 */
function bar(o, a, b, side = null, len = 0) {
  _v.set(b[0] - a[0], b[1] - a[1], b[2] - a[2]);
  const L = _v.length() || 1e-6;
  _v.multiplyScalar(1 / L);
  o.position.set(a[0], a[1], a[2]);
  if (side) {
    _x.set(side[0], side[1], side[2]).addScaledVector(_v, -(side[0] * _v.x + side[1] * _v.y + side[2] * _v.z));
    if (_x.lengthSq() < 1e-8) _x.set(_v.y, -_v.x, 0);
    _x.normalize();
    _z.crossVectors(_x, _v);
    _m.makeBasis(_x, _v, _z);
    o.quaternion.setFromRotationMatrix(_m);
  } else o.quaternion.setFromUnitVectors(_y, _v);
  if (len) o.scale.set(1, L / len, 1);
}

/* ── 모양 만들기 ── */
function Geo(store) {
  const keep = (g) => { store.push(g); return g; };
  return {
    cap: (r, len, seg = 16) => { const g = new THREE.CapsuleGeometry(r, len, 6, seg); g.translate(0, len / 2, 0); return keep(g); },
    box: (w, h, d, r = 0.01, along = false) => { const g = new RoundedBoxGeometry(w, h, d, 3, Math.min(r, w / 2.01, h / 2.01, d / 2.01)); if (along) g.translate(0, h / 2, 0); return keep(g); },
    cyl: (rt, rb, h, seg = 24, along = false, open = false) => { const g = new THREE.CylinderGeometry(rt, rb, h, seg, 1, open); if (along) g.translate(0, h / 2, 0); return keep(g); },
    sph: (r, w = 24, h = 16) => keep(new THREE.SphereGeometry(r, w, h)),
    tor: (r, t, rs = 12, ts = 32) => keep(new THREE.TorusGeometry(r, t, rs, ts)),
    cone: (r, h, seg = 18) => { const g = new THREE.ConeGeometry(r, h, seg, 1, true); g.translate(0, -h / 2, 0); return keep(g); },
    disc: (r, seg = 32) => { const g = new THREE.CircleGeometry(r, seg); g.rotateX(-Math.PI / 2); return keep(g); },
  };
}
function mk(geo, mat, parent, cast = true) {
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = cast; m.receiveShadow = true;
  parent.add(m);
  return m;
}

/* ══════════ 사람 모양 로봇 ══════════ */
function buildHumanoid(M, g) {
  const root = new THREE.Group();
  const pelvis = mk(g.box(0.3, 0.13, 0.19, 0.045), M.white, root);
  const torso = new THREE.Group(); root.add(torso);          // 골반에서 어깨 쪽(+Y)
  mk(g.cyl(0.085, 0.1, 0.17, 24, true), M.joint, torso).position.y = 0.03;
  const chest = mk(g.box(0.38, 0.3, 0.23, 0.07), M.white, torso); chest.position.y = 0.33;
  const plate = mk(g.box(0.2, 0.11, 0.02, 0.008), M.grey, torso, false); plate.position.set(0, 0.36, 0.118);
  const core = mk(g.cyl(0.03, 0.03, 0.01, 24), M.led, torso, false); core.rotation.x = Math.PI / 2; core.position.set(0, 0.37, 0.13);
  const strip = mk(g.box(0.24, 0.012, 0.01, 0.004), M.led, torso, false); strip.position.set(0, 0.255, 0.115);
  const pack = mk(g.box(0.27, 0.25, 0.1, 0.03), M.grey, torso); pack.position.set(0, 0.34, -0.15);
  const head = new THREE.Group(); root.add(head);
  mk(g.cyl(0.04, 0.045, 0.08, 16, true), M.joint, head);
  const helm = mk(g.sph(0.115, 28, 20), M.white, head); helm.position.y = 0.14; helm.scale.set(1, 1.08, 1.06);
  const visor = mk(g.sph(0.1, 28, 16), M.visor, head, false); visor.position.set(0, 0.14, 0.03); visor.scale.set(1.04, 0.62, 0.95);
  const eye = mk(g.box(0.13, 0.014, 0.01, 0.005), M.led, head, false); eye.position.set(0, 0.145, 0.122);
  const arms = [0, 1].map(() => ({
    sh: mk(g.sph(0.062), M.joint, root), pad: mk(g.sph(0.078, 24, 16), M.white, root),
    up: mk(g.cap(0.043, 0.3), M.white, root), el: mk(g.sph(0.047), M.joint, root),
    fo: mk(g.cap(0.039, 0.29), M.white, root), hd: mk(g.box(0.062, 0.075, 0.036, 0.014, true), M.joint, root),
  }));
  const legs = [0, 1].map(() => {
    const L = {
      hip: mk(g.sph(0.066), M.joint, root), th: mk(g.cap(0.064, 0.43), M.white, root), kn: mk(g.sph(0.06), M.joint, root),
      cap: mk(g.sph(0.05), M.white, root), sh: mk(g.cap(0.054, 0.42), M.white, root), an: mk(g.sph(0.046), M.joint, root),
      ft: new THREE.Group(),
    };
    root.add(L.ft);
    const sole = mk(g.box(0.11, 0.055, 0.23, 0.02), M.joint, L.ft); sole.position.set(0, -0.045, 0.06);
    const led = mk(g.box(0.1, 0.008, 0.008, 0.003), M.led, L.ft, false); led.position.set(0, -0.06, 0.177);
    L.fire = mk(g.cone(0.035, 0.14), M.thrust, L.ft, false); L.fire.position.set(0, -0.075, 0.04);
    return L;
  });
  function apply(P) {
    put(pelvis, P.pelvis); pelvis.rotation.x = P.lean * 0.35;
    bar(torso, P.pelvis, P.chest, [1, 0, 0]);
    put(head, P.neck); head.rotation.set(P.headPitch, 0, 0);
    for (let i = 0; i < 2; i++) {
      const A = arms[i];
      put(A.sh, P.sh[i]);
      A.pad.position.set(P.sh[i][0] + (i ? 0.018 : -0.018), P.sh[i][1] + 0.02, P.sh[i][2]);
      bar(A.up, P.sh[i], P.el[i]); put(A.el, P.el[i]); bar(A.fo, P.el[i], P.wr[i]);
      bar(A.hd, P.wr[i], P.hd[i], [0, 1, 0]);
      const L = legs[i];
      put(L.hip, P.hip[i]); bar(L.th, P.hip[i], P.kn[i]); put(L.kn, P.kn[i]);
      L.cap.position.set(P.kn[i][0], P.kn[i][1] + 0.01, P.kn[i][2] + 0.035);
      bar(L.sh, P.kn[i], P.an[i]); put(L.an, P.an[i]);
      put(L.ft, P.an[i]);
      L.fire.visible = P.hover > 0.04;
      L.fire.scale.set(1, 0.4 + P.hover * (0.9 + 0.25 * Math.sin(performance.now() * 0.05 + i)), 1);
    }
  }
  return { root, apply };
}

/* ══════════ 네 발 로봇 개 ══════════ */
function buildDog(M, g) {
  const root = new THREE.Group();
  const body = new THREE.Group(); root.add(body);
  mk(g.box(0.82, 0.19, 0.3, 0.05), M.yellow, body);
  const top = mk(g.box(0.52, 0.025, 0.22, 0.01), M.joint, body); top.position.y = 0.1;
  for (const s of [-1, 1]) { const side = mk(g.box(0.5, 0.1, 0.012, 0.005), M.joint, body, false); side.position.set(-0.02, -0.01, s * 0.151); }
  const head = mk(g.box(0.13, 0.13, 0.25, 0.03), M.joint, body); head.position.set(0.44, 0.02, 0);
  for (const s of [-1, 1]) { const lens = mk(g.sph(0.026, 16, 12), M.lens, body, false); lens.position.set(0.505, 0.03, s * 0.06); }
  const eye = mk(g.box(0.012, 0.018, 0.17, 0.005), M.led, body, false); eye.position.set(0.508, -0.02, 0);
  const rear = mk(g.box(0.09, 0.12, 0.22, 0.02), M.joint, body); rear.position.set(-0.43, 0, 0);
  const legs = [0, 1, 2, 3].map(() => ({
    hip: mk(g.cyl(0.058, 0.058, 0.1, 20), M.joint, root), th: mk(g.box(0.075, 0.31, 0.085, 0.025, true), M.yellow, root),
    kn: mk(g.sph(0.04), M.joint, root), sh: mk(g.cap(0.028, 0.33), M.joint, root), ft: mk(g.sph(0.034), M.rubber, root),
  }));
  for (const L of legs) L.hip.rotation.x = Math.PI / 2;
  const turret = mk(g.cyl(0.075, 0.085, 0.06, 24), M.joint, root);
  const up = mk(g.box(0.075, 0.62, 0.075, 0.025, true), M.yellow, root);
  const el = mk(g.cyl(0.05, 0.05, 0.1, 20), M.joint, root);
  const fo = mk(g.box(0.062, 0.56, 0.062, 0.02, true), M.yellow, root);
  const wr = mk(g.sph(0.042), M.joint, root);
  const grip = new THREE.Group(); root.add(grip);
  mk(g.box(0.09, 0.05, 0.07, 0.012, true), M.joint, grip);
  const jaws = [-1, 1].map((s) => { const j = mk(g.box(0.018, 0.075, 0.045, 0.006, true), M.metal, grip); j.position.set(s * 0.02, 0.05, 0); return j; });
  const gled = mk(g.box(0.05, 0.008, 0.008, 0.003), M.led, grip, false); gled.position.set(0, 0.03, 0.038);
  function apply(P) {
    put(body, P.body); body.rotation.set(P.roll, 0, P.pitch);
    for (let i = 0; i < 4; i++) {
      const L = legs[i];
      put(L.hip, P.hip[i]); bar(L.th, P.hip[i], P.kn[i], [0, 0, 1]); put(L.kn, P.kn[i]); bar(L.sh, P.kn[i], P.ft[i]); put(L.ft, P.ft[i]);
    }
    turret.position.set(P.sh[0], P.sh[1] - 0.05, P.sh[2]);
    bar(up, P.sh, P.el, [1, 0, 0]);
    put(el, P.el); el.rotation.set(0, 0, Math.PI / 2);
    bar(fo, P.el, P.wr, [1, 0, 0]);
    put(wr, P.wr);
    bar(grip, P.wr, P.tip, [0, 1, 0]);
    const o = P.gap + 0.009 + P.open * 0.026;
    jaws[0].position.x = -o; jaws[1].position.x = o;
  }
  return { root, apply };
}

/* ══════════ 산업용 팔 ══════════ */
function buildArm(M, g, G) {
  const root = new THREE.Group();
  const railLen = G.W + 0.7;
  const rail = mk(g.box(railLen, 0.07, 0.2, 0.012), M.joint, root); rail.position.y = 0.035;
  for (const s of [-1, 1]) { const rod = mk(g.cyl(0.012, 0.012, railLen - 0.04, 12), M.metal, root, false); rod.rotation.z = Math.PI / 2; rod.position.set(0, 0.078, s * 0.06); }
  for (const s of [-1, 1]) { const stop = mk(g.box(0.05, 0.1, 0.22, 0.01), M.orange, root); stop.position.set(s * (railLen / 2 - 0.02), 0.05, 0); }
  const led = mk(g.box(railLen - 0.1, 0.006, 0.006, 0.002), M.ledWarm, root, false); led.position.set(0, 0.045, 0.101);
  const car = mk(g.box(0.3, 0.1, 0.26, 0.02), M.joint, root);
  const ped = mk(g.cyl(0.11, 0.135, 0.34, 32, true), M.orange, root);
  const tur = new THREE.Group(); root.add(tur);
  mk(g.cyl(0.115, 0.115, 0.08, 32, true), M.joint, tur);
  const hous = mk(g.box(0.2, 0.2, 0.18, 0.04), M.orange, tur); hous.position.y = 0.09;
  const up = mk(g.box(0.12, 0.6, 0.14, 0.035, true), M.orange, root);
  const el = mk(g.cyl(0.078, 0.078, 0.17, 28), M.joint, root);
  const fo = mk(g.box(0.095, 0.55, 0.105, 0.03, true), M.orange, root);
  const wr = mk(g.cyl(0.052, 0.052, 0.12, 24), M.joint, root);
  const fl = mk(g.cyl(0.042, 0.042, 0.09, 24, true), M.metal, root);
  const tool = new THREE.Group(); root.add(tool);
  mk(g.box(0.1, 0.05, 0.06, 0.012, true), M.joint, tool);
  const ring = mk(g.tor(0.036, 0.006, 8, 32), M.ledWarm, tool, false); ring.rotation.x = Math.PI / 2; ring.position.y = 0.01;
  const fingers = [-1, 1].map((s) => { const f = mk(g.box(0.02, 0.075, 0.04, 0.006, true), M.metal, tool); f.position.set(s * 0.025, 0.05, 0); return f; });
  function apply(P) {
    car.position.set(P.cx, 0.12, P.rz);
    ped.position.set(P.cx, 0.17, P.rz);
    tur.position.set(P.cx, 0.51, P.rz); tur.rotation.y = P.yaw;
    bar(up, P.sh, P.el, [1, 0, 0]);
    put(el, P.el); el.rotation.set(0, 0, Math.PI / 2);
    bar(fo, P.el, P.wr, [1, 0, 0]);
    put(wr, P.wr); wr.rotation.set(0, 0, Math.PI / 2);
    bar(fl, P.wr, P.fl);
    bar(tool, P.fl, P.tip, [0, 1, 0]);
    tool.rotateY(P.spin);
    const o = P.gap + 0.01 + P.open * 0.026;
    fingers[0].position.x = -o; fingers[1].position.x = o;
  }
  return { root, apply };
}

/* ══════════ 두 바퀴 균형 로봇 ══════════ */
function buildRover(M, g) {
  const root = new THREE.Group();
  const wheels = [-1, 1].map((s) => {
    const w = new THREE.Group(); root.add(w);
    mk(g.tor(0.125, 0.036, 14, 40), M.rubber, w);
    const hub = mk(g.cyl(0.09, 0.09, 0.05, 32), M.teal, w); hub.rotation.x = Math.PI / 2;
    const ring = mk(g.tor(0.07, 0.006, 8, 32), M.led, w, false); ring.position.z = s * 0.027;
    for (let k = 0; k < 3; k++) { const sp = mk(g.box(0.012, 0.16, 0.012, 0.004), M.metal, w, false); sp.rotation.z = (k * Math.PI) / 3; sp.position.z = s * 0.03; }
    w.userData.s = s;
    return w;
  });
  const axle = mk(g.cyl(0.03, 0.03, 0.38, 16), M.joint, root); axle.rotation.x = Math.PI / 2;
  const body = new THREE.Group(); root.add(body);
  mk(g.box(0.2, 0.34, 0.25, 0.05, true), M.white, body);
  const bl = mk(g.box(0.012, 0.2, 0.17, 0.005), M.led, body, false); bl.position.set(0.101, 0.18, 0);
  const sleeve = mk(g.cyl(0.05, 0.055, 0.12, 24, true), M.teal, root);
  const mast = mk(g.cyl(0.03, 0.03, 1, 20, true), M.metal, root);
  const mast2 = mk(g.cyl(0.022, 0.022, 1, 16, true), M.metal, root);
  const head = new THREE.Group(); root.add(head);
  mk(g.box(0.13, 0.11, 0.16, 0.03), M.teal, head);
  const dome = mk(g.sph(0.06, 24, 16), M.visor, head, false); dome.position.set(0, 0.075, -0.02); dome.scale.set(1, 0.7, 1);
  const eye = mk(g.box(0.07, 0.012, 0.008, 0.003), M.led, head, false); eye.position.set(0, 0.08, 0.04);
  const boom = mk(g.cyl(0.018, 0.018, 1, 16, true), M.metal, root);
  const boom2 = mk(g.cyl(0.024, 0.024, 1, 16, true), M.grey, root);
  const clamp = new THREE.Group(); root.add(clamp);
  mk(g.box(0.07, 0.04, 0.05, 0.01, true), M.joint, clamp);
  const fingers = [-1, 1].map((s) => { const f = mk(g.box(0.016, 0.06, 0.035, 0.005, true), M.metal, clamp); f.position.set(s * 0.02, 0.035, 0); return f; });
  function apply(P) {
    for (const w of wheels) { w.position.set(P.axle[0], P.axle[1], P.axle[2] + w.userData.s * 0.17); w.rotation.z = P.wheel; }
    put(axle, P.axle);
    put(body, P.axle); body.rotation.set(0, 0, P.lean);
    put(sleeve, P.mb); sleeve.rotation.set(0, 0, P.lean);
    bar(mast, P.mb, [P.mb[0] + (P.mt[0] - P.mb[0]) * 0.55, P.mb[1] + (P.mt[1] - P.mb[1]) * 0.55, P.mb[2]], null, 1);
    bar(mast2, P.mb, P.mt, null, 1);
    put(head, P.mt); head.rotation.set(0, P.yaw, P.lean);
    const b0 = [P.mt[0], P.mt[1], P.mt[2] + 0.06];
    bar(boom2, b0, [b0[0], b0[1], b0[2] + (P.boomEnd[2] - b0[2]) * 0.5], null, 1);
    bar(boom, b0, P.boomEnd, null, 1);
    bar(clamp, P.boomEnd, P.tip, [0, 1, 0]);
    const o = P.gap + 0.01 + P.open * 0.026;
    fingers[0].position.x = -o; fingers[1].position.x = o;
  }
  return { root, apply };
}

/* ══════════ 드론 ══════════ */
function buildDrone(M, g) {
  const root = new THREE.Group();
  const body = new THREE.Group(); root.add(body);
  mk(g.box(0.2, 0.055, 0.2, 0.02), M.carbon, body);
  const can = mk(g.sph(0.085, 28, 16), M.white, body); can.position.y = 0.03; can.scale.set(1, 0.42, 1.15);
  const ring = mk(g.tor(0.105, 0.006, 8, 48), M.led, body, false); ring.rotation.x = Math.PI / 2;
  const props = [];
  for (let i = 0; i < 4; i++) {
    const a = Math.PI / 4 + (i * Math.PI) / 2, cx = Math.cos(a) * 0.19, cz = Math.sin(a) * 0.19;
    const arm = mk(g.box(0.2, 0.02, 0.026, 0.008), M.carbon, body); arm.position.set(cx / 2, 0, cz / 2); arm.rotation.y = -a;
    const mot = mk(g.cyl(0.026, 0.028, 0.035, 20), M.metal, body); mot.position.set(cx, 0.02, cz);
    const blur = mk(g.disc(0.105, 40), M.prop, body, false); blur.position.set(cx, 0.043, cz);
    const blade = mk(g.box(0.2, 0.003, 0.018, 0.001), M.joint, body, false); blade.position.set(cx, 0.042, cz);
    props.push(blade);
    const nav = mk(g.sph(0.009, 10, 8), i < 2 ? (i === 0 ? M.ledGreen : M.ledRed) : M.led, body, false); nav.position.set(cx, -0.006, cz);
  }
  for (const s of [-1, 1]) { const leg = mk(g.box(0.012, 0.07, 0.16, 0.004), M.joint, body, false); leg.position.set(s * 0.07, -0.06, 0); }
  const winch = mk(g.cyl(0.03, 0.03, 0.03, 20), M.metal, body); winch.position.y = -0.04;
  const cables = [0, 1, 2].map(() => mk(g.cyl(0.0025, 0.0025, 1, 6, true), M.cable, root, false));
  const hooks = [0, 1, 2].map(() => mk(g.sph(0.009, 12, 8), M.metal, root, false));
  function apply(P) {
    put(body, P.body); body.rotation.set(P.pitch, P.yaw, P.roll);
    for (let i = 0; i < 4; i++) props[i].rotation.y = P.rotor * (i % 2 ? 1 : -1);
    const show = P.ext > 0.03;
    for (let i = 0; i < 3; i++) {
      cables[i].visible = hooks[i].visible = show;
      if (show) { bar(cables[i], P.hub[i], P.hook[i], null, 1); put(hooks[i], P.hook[i]); }
    }
  }
  return { root, apply };
}

const BUILD = { humanoid: buildHumanoid, dog: buildDog, arm: buildArm, rover: buildRover, drone: buildDrone };

/** 로봇 한 대: { root, kin, update(G, plan, yOff, dt, time), dispose } */
export function makeRobot(kind, M, G) {
  const geos = [];
  const g = Geo(geos);
  const R = BUILD[kind](M, g, G);
  const kin = KINS[kind]();
  return {
    kind, root: R.root, kin,
    update(G2, plan, yOff, dt, time) { const P = kin.update(G2, plan, yOff, dt, time); R.apply(P); return P; },
    dispose() { for (const x of geos) x.dispose(); },
  };
}
