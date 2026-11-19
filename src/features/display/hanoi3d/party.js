// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 4배속 파티 (hanoi3d/party.js)
// 4배속이면 켜진다 — 움직이는 조명 빛줄기 · 미러볼(바닥과 하늘에 빛 점) · 레이저 · 콘페티(GPU 로 수천 장) · 바닥 LED.
// 조명은 진짜 빛을 늘리지 않는다(재질을 다시 만들지 않게) — 빛줄기는 더하기 그리기, 바닥의 빛 웅덩이는 바닥 셰이더가 그린다.
// 눈 건강: 화면 전체가 번쩍이는 섬광은 쓰지 않는다. 박자(124 BPM)에 맞춰 밝기가 살짝 숨쉴 뿐이다.
import * as THREE from "three";

export const BPM = 124;
export const BEAT = 60 / BPM;
const NB = 8;            // 빛줄기
const NL = 12;           // 레이저

const hsv = (h, s, v, out = new THREE.Color()) => out.setHSL(((h % 1) + 1) % 1, s, v * 0.5);

// 빛줄기: 원뿔 옆면이 보는 쪽을 향할수록 밝게(가운데 진하고 가장자리 흐리게). 길이 · 굵기를 따로 늘이므로 법선은 normalMatrix 로.
const BEAM_VS = /* glsl */`
varying vec3 vN; varying vec3 vV; varying vec3 vW; varying float vT;
void main() {
  vT = -position.y;
  vec4 w = modelMatrix * vec4(position, 1.0);
  vW = w.xyz;
  vec4 mv = viewMatrix * w;
  vN = normalize(normalMatrix * normal);
  vV = normalize(-mv.xyz);
  gl_Position = projectionMatrix * mv;
}`;
const BEAM_FS = /* glsl */`
uniform vec3 uColor; uniform float uI; uniform float uTime;
varying vec3 vN; varying vec3 vV; varying vec3 vW; varying float vT;
void main() {
  float f = abs(dot(normalize(vN), normalize(vV)));
  float core = pow(f, 2.4);
  float fall = (1.0 - vT * 0.8) * smoothstep(0.0, 0.06, vT);
  float dust = 0.78 + 0.22 * sin(vT * 37.0 - uTime * 2.7 + vW.x * 3.0) * sin(vT * 11.0 + uTime * 1.3);
  gl_FragColor = vec4(uColor * (uI * core * fall * dust), 1.0);
}`;

const CONF_VS = /* glsl */`
attribute vec4 aSeed; attribute vec3 aColor;
uniform float uTime, uStart, uEnd, uTb, uSize, uR, uTop, uVis;
uniform vec3 uC;
varying vec3 vColor; varying vec3 vN; varying float vFade; varying float vFoil; varying vec3 vW;
mat3 rotA(vec3 a, float t) {
  a = normalize(a); float s = sin(t), c = cos(t), o = 1.0 - c;
  return mat3(o*a.x*a.x + c, o*a.x*a.y + a.z*s, o*a.z*a.x - a.y*s,
              o*a.x*a.y - a.z*s, o*a.y*a.y + c, o*a.y*a.z + a.x*s,
              o*a.z*a.x + a.y*s, o*a.y*a.z - a.x*s, o*a.z*a.z + c);
}
void main() {
  float id = aSeed.x;
  float cannon = step(0.4, aSeed.y);
  float life = 2.0 * uTb;
  float par = step(0.5, fract(id * 7.31));
  float rel = uTime - (uStart + par * uTb);
  float tt = rel + (cannon > 0.5 ? 0.0 : aSeed.z * life);
  float age = tt - floor(tt / life) * life;
  float spawn = uTime - age;
  float alive = step(0.0, rel) * step(spawn, uEnd) * step(uStart - 0.02, spawn);
  float side = fract(id * 13.7) < 0.5 ? -1.0 : 1.0;
  float a1 = fract(id * 91.3) * 6.2831853, a2 = fract(id * 47.9), sc = sqrt(uR / 2.0);
  vec3 p0, v0;
  if (cannon > 0.5) {
    p0 = uC + vec3(side * uR * 0.92, 0.04, uR * 0.5);
    vec3 dir = normalize(vec3(-side * (0.32 + 0.34 * a2), 1.0, -0.3 + 0.28 * sin(a1)));
    v0 = dir * (4.0 + 2.6 * fract(id * 3.1)) * sc + vec3(cos(a1), 0.0, sin(a1)) * 0.5 * sc;
  } else {
    p0 = uC + vec3((fract(id * 5.3) - 0.5) * 2.3 * uR, uTop, (fract(id * 8.9) - 0.5) * 2.0 * uR);
    v0 = vec3(0.0, -0.2, 0.0);
  }
  float k = 2.3, e = exp(-k * age);
  vec3 vt = vec3(0.0, -0.52 * sc * (0.7 + 0.6 * aSeed.w), 0.0);
  vec3 pos = p0 + vt * age + (v0 - vt) * (1.0 - e) / k;
  float fl = 0.09 * sc * (1.0 - e * 0.7);
  pos.x += fl * sin(age * (3.0 + 2.0 * aSeed.z) + a1);
  pos.z += fl * cos(age * (2.6 + 2.0 * aSeed.w) + a1);
  float land = step(pos.y, 0.004);
  pos.y = max(pos.y, 0.002 + aSeed.w * 0.003);
  mat3 R = land > 0.5 ? rotA(vec3(0.0, 1.0, 0.0), a1) * mat3(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0)
                      : rotA(vec3(aSeed.y - 0.5, aSeed.z - 0.49, aSeed.w - 0.5), age * (5.0 + 9.0 * aSeed.y) + a1);
  vec3 lp = R * (position * uSize * (0.7 + 0.6 * aSeed.z));
  vN = R * vec3(0.0, 0.0, 1.0);
  vec4 w = vec4(pos + lp, 1.0);
  vW = w.xyz;
  gl_Position = projectionMatrix * viewMatrix * w;
  vColor = aColor;
  vFoil = step(0.78, fract(id * 3.77));
  vFade = alive * (1.0 - smoothstep(life - 1.1, life, age)) * uVis;
}`;
const CONF_FS = /* glsl */`
uniform vec3 uL; uniform float uGain;
varying vec3 vColor; varying vec3 vN; varying float vFade; varying float vFoil; varying vec3 vW;
float hh(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
void main() {
  if (vFade < 0.01 || vFade < hh(floor(gl_FragCoord.xy))) discard;
  vec3 n = normalize(vN);
  float nl = abs(dot(n, uL));
  vec3 V = normalize(cameraPosition - vW);
  float sp = pow(abs(dot(n, normalize(uL + V))), mix(20.0, 80.0, vFoil)) * mix(0.3, 2.4, vFoil);
  vec3 c = vColor * (0.34 + 0.66 * nl) + sp * mix(vec3(1.0), vColor, 0.45 * vFoil);
  gl_FragColor = vec4(c * uGain, 1.0);
}`;

const CONF_COLORS = ["#ffd23f", "#ff4f9a", "#3fe0ff", "#7dff5a", "#ff8a2b", "#ffffff", "#5b7cff", "#c86bff", "#ff5050"];

/**
 * 파티 무대. 엔진이 매 그림마다 update(...) 를 부르고, 바닥 · 하늘 셰이더에 uniforms 를 넘긴다.
 *   level: 0 ~ 1 (켜지고 꺼지며 부드럽게) · beat: 박자 숨(0 ~ 1)
 */
export function createParty(scene, tier, res) {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);
  const state = { level: 0, target: 0, beat: 0, hue: 0, start: 0, end: 1e9, on: false, t: 0 };

  // ── 빛줄기 ──
  const beamGeo = new THREE.CylinderGeometry(0.0, 1, 1, 40, 1, true);
  beamGeo.translate(0, -0.5, 0);
  res.push(beamGeo);
  const beams = [];
  for (let i = 0; i < NB; i++) {
    const mat = new THREE.ShaderMaterial({
      uniforms: { uColor: { value: new THREE.Color() }, uI: { value: 0 }, uTime: { value: 0 } },
      vertexShader: BEAM_VS, fragmentShader: BEAM_FS, transparent: true, depthWrite: false,
      blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
    });
    res.push(mat);
    const m = new THREE.Mesh(beamGeo, mat);
    m.frustumCulled = false; m.renderOrder = 5;
    group.add(m);
    beams.push({ mesh: m, mat, src: new THREE.Vector3(), tgt: new THREE.Vector3(), col: new THREE.Color(), r: 0.3, i: 0 });
  }
  // ── 미러볼 ──
  const ballGeo = new THREE.IcosahedronGeometry(1, 3);
  const ballMat = new THREE.MeshStandardMaterial({ color: "#e8e8ee", metalness: 1, roughness: 0.05, flatShading: true, envMapIntensity: 2.4 });
  const rodGeo = new THREE.CylinderGeometry(0.006, 0.006, 1, 8);
  rodGeo.translate(0, 0.5, 0);
  const rodMat = new THREE.MeshStandardMaterial({ color: "#555", metalness: 1, roughness: 0.3 });
  res.push(ballGeo, ballMat, rodGeo, rodMat);
  const ball = new THREE.Mesh(ballGeo, ballMat);
  const rod = new THREE.Mesh(rodGeo, rodMat);
  group.add(ball, rod);
  // ── 레이저 ──
  const lasGeo = new THREE.PlaneGeometry(1, 1);
  lasGeo.translate(0, 0.5, 0);
  res.push(lasGeo);
  const lasers = [];
  for (let i = 0; i < NL; i++) {
    const mat = new THREE.ShaderMaterial({
      uniforms: { uColor: { value: new THREE.Color() }, uI: { value: 0 } },
      vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
      fragmentShader: "uniform vec3 uColor; uniform float uI; varying vec2 vUv; void main(){ float w = 1.0 - abs(vUv.x - 0.5) * 2.0; float a = pow(w, 3.0) * (1.0 - vUv.y * 0.6); gl_FragColor = vec4(uColor * uI * a, 1.0); }",
      transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
    });
    res.push(mat);
    const m = new THREE.Mesh(lasGeo, mat);
    m.frustumCulled = false; m.renderOrder = 6;
    group.add(m);
    lasers.push({ mesh: m, mat });
  }
  // ── 콘페티 ──
  const NC = [900, 2600, 5200][tier] || 2600;
  const cg = new THREE.InstancedBufferGeometry();
  const quad = new THREE.PlaneGeometry(1, 0.55);
  cg.index = quad.index;
  cg.setAttribute("position", quad.getAttribute("position"));
  cg.setAttribute("uv", quad.getAttribute("uv"));
  const seed = new Float32Array(NC * 4), col = new Float32Array(NC * 3);
  const cc = new THREE.Color();
  for (let i = 0; i < NC; i++) {
    seed[i * 4] = Math.random() * 1000; seed[i * 4 + 1] = Math.random(); seed[i * 4 + 2] = Math.random(); seed[i * 4 + 3] = Math.random();
    cc.set(CONF_COLORS[i % CONF_COLORS.length]);
    col[i * 3] = cc.r; col[i * 3 + 1] = cc.g; col[i * 3 + 2] = cc.b;
  }
  cg.setAttribute("aSeed", new THREE.InstancedBufferAttribute(seed, 4));
  cg.setAttribute("aColor", new THREE.InstancedBufferAttribute(col, 3));
  cg.instanceCount = NC;
  quad.dispose();
  const confMat = new THREE.ShaderMaterial({
    uniforms: {
      uTime: { value: 0 }, uStart: { value: 0 }, uEnd: { value: 1e9 }, uTb: { value: BEAT * 8 }, uSize: { value: 0.03 }, uR: { value: 2 },
      uTop: { value: 3 }, uVis: { value: 1 }, uC: { value: new THREE.Vector3() }, uL: { value: new THREE.Vector3(0.3, 0.9, 0.3).normalize() }, uGain: { value: 1.3 },
    },
    vertexShader: CONF_VS, fragmentShader: CONF_FS, side: THREE.DoubleSide,
  });
  res.push(cg, confMat);
  const conf = new THREE.Mesh(cg, confMat);
  conf.frustumCulled = false;
  conf.castShadow = false;
  scene.add(conf);
  conf.visible = false;

  // 바닥 · 하늘 셰이더로 넘길 값
  const uniforms = {
    uParty: { value: 0 }, uBeat: { value: 0 },
    uPool: { value: Array.from({ length: NB }, () => new THREE.Vector4()) },
    uPoolCol: { value: Array.from({ length: NB }, () => new THREE.Color()) },
    uBall: { value: new THREE.Vector4() }, uBallRot: { value: 0 },
  };

  const _q = new THREE.Quaternion(), _d = new THREE.Vector3(), _y = new THREE.Vector3(0, 1, 0), _w = new THREE.Vector3(), _c = new THREE.Vector3(), _m = new THREE.Matrix4(), _n = new THREE.Vector3();
  /**
   * on: 4배속인가 · time: 보는 시계(s) · dt · C: 장면 가운데 {x, z} · R: 장면 반지름 · camPos: 카메라(레이저를 카메라 쪽으로 돌린다)
   */
  function update(on, time, dt, C, R, camPos, topY) {
    if (on !== state.on) {
      state.on = on;
      if (on) { state.start = time + 0.35; state.end = 1e9; } else state.end = time;
    }
    state.level += ((on ? 1 : 0) - state.level) * (1 - Math.exp(-dt * (on ? 2.6 : 1.6)));
    if (state.level < 0.002 && !on) state.level = 0;
    const L = state.level;
    const bp = time / BEAT;
    state.beat = Math.exp(-5.5 * (bp - Math.floor(bp)));
    state.hue = (time * 0.045) % 1;
    uniforms.uParty.value = L;
    uniforms.uBeat.value = state.beat;
    // 콘페티는 꺼진 뒤에도 남은 것이 다 떨어질 때까지
    const confLeft = time - state.end < BEAT * 16 + 2;
    conf.visible = (on || confLeft) && state.start > 0;
    confMat.uniforms.uTime.value = time;
    confMat.uniforms.uStart.value = state.start;
    confMat.uniforms.uEnd.value = state.end;
    confMat.uniforms.uR.value = R;
    confMat.uniforms.uTop.value = topY;
    confMat.uniforms.uSize.value = 0.022 * Math.sqrt(Math.max(1, R / 1.6));
    confMat.uniforms.uC.value.set(C.x, 0, C.z);
    confMat.uniforms.uGain.value = 1.15 + 0.35 * state.beat * L;
    group.visible = L > 0.003;
    if (!group.visible) return state;
    const H = topY * 0.92 + 0.6;
    // 빛줄기: 장면을 둘러싼 원 위에서, 바닥의 리사주 곡선을 따라 비춘다
    for (let i = 0; i < NB; i++) {
      const B = beams[i];
      const a = (i / NB) * Math.PI * 2 + 0.3;
      B.src.set(C.x + Math.cos(a) * R * 1.05, H, C.z + Math.sin(a) * R * 0.75 - R * 0.25);
      const ph = time * (0.55 + 0.07 * i) + i * 1.7;
      B.tgt.set(C.x + Math.sin(ph) * R * 0.75, 0, C.z + Math.sin(ph * 1.31 + i) * R * 0.55);
      _d.subVectors(B.tgt, B.src);
      const len = _d.length();
      _d.multiplyScalar(-1 / len);
      _q.setFromUnitVectors(_y, _d);
      B.mesh.position.copy(B.src);
      B.mesh.quaternion.copy(_q);
      const rr = len * Math.tan(0.11 + 0.03 * Math.sin(time * 0.7 + i));
      B.mesh.scale.set(rr, len, rr);
      hsv(state.hue + i / NB + 0.15 * Math.sin(time * 0.3), 1, 1, B.col);
      const I = L * (0.6 + 0.55 * state.beat) * (0.7 + 0.3 * Math.sin(time * 1.9 + i * 2.1));
      B.mat.uniforms.uColor.value.copy(B.col);
      B.mat.uniforms.uI.value = I;
      B.mat.uniforms.uTime.value = time;
      uniforms.uPool.value[i].set(B.tgt.x, B.tgt.z, rr * 0.9, I * 0.9);
      uniforms.uPoolCol.value[i].copy(B.col);
    }
    // 미러볼
    const by = H + 0.25, bs = 0.09 + R * 0.035;
    ball.position.set(C.x, by, C.z - R * 0.1);
    ball.scale.setScalar(bs);
    ball.rotation.y = time * 0.6;
    rod.position.set(C.x, by + bs * 0.9, C.z - R * 0.1);
    rod.scale.set(1, 3, 1);
    uniforms.uBall.value.set(ball.position.x, ball.position.y, ball.position.z, L * (0.9 + 0.5 * state.beat));
    uniforms.uBallRot.value = time * 0.6;
    // 레이저: 뒤 양쪽 모서리에서 부채꼴로, 카메라를 향해 판을 돌린다
    for (let i = 0; i < NL; i++) {
      const Ls = lasers[i];
      const side = i < NL / 2 ? -1 : 1, k = (i % (NL / 2)) / (NL / 2 - 1) - 0.5;
      _c.set(C.x + side * R * 0.95, 0.15, C.z - R * 0.85);
      const sweep = Math.sin(time * 1.6 + side) * 0.55 + k * 1.1;
      _d.set(-side * Math.cos(sweep) * 0.9, 0.25 + 0.18 * Math.sin(time * 2.3 + i), Math.sin(sweep) * 0.9 + 0.55).normalize();
      const len = R * 2.4;
      _w.subVectors(camPos, _c).cross(_d).normalize();
      _n.crossVectors(_w, _d);
      _m.makeBasis(_w, _d, _n);
      Ls.mesh.quaternion.setFromRotationMatrix(_m);
      Ls.mesh.position.copy(_c);
      Ls.mesh.scale.set(0.012 + R * 0.002, len, 1);
      const col = i % 3 === 0 ? 0x39ff6a : i % 3 === 1 ? 0x37d8ff : 0xff3cc8;
      Ls.mat.uniforms.uColor.value.set(col);
      const gate = Math.sin(bp * Math.PI * 0.5 + i) > -0.2 ? 1 : 0.15;
      Ls.mat.uniforms.uI.value = L * 3.2 * gate * (0.6 + 0.4 * state.beat);
    }
    return state;
  }
  function setTier(t) { cg.instanceCount = [900, 2600, 5200][t] ? Math.min(NC, [900, 2600, 5200][t]) : NC; }
  return { group, conf, update, uniforms, state, setTier, beams };
}
