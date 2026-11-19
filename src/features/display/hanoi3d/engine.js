// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 엔진 (hanoi3d/engine.js)
// createHanoiEngine(canvas, { theme, getElapsed, onError }) → { setConfig({ TL, sets, speed }), setTheme, setPaused, dispose, stats }
// 스스로 requestAnimationFrame 으로 돈다(최대 60fps, 멈춤이면 30fps) — React 는 설정이 바뀔 때만 부른다. 시계는 getElapsed()(ms)로 읽는다.
// 그리는 순서: 바닥 반사(거울에 비친 장면 · 밉맵으로 흐리게) → 장면(그림자 · 환경광) → 빛 번짐 → (대각선 보기면) 틸트시프트 → 색 · 비네트 · 입자.
// 품질: 그래픽 칩 이름으로 처음 정하고(소프트웨어면 낮음), 실제 그리는 시간을 재며 낮춘다. localStorage "ash.display.hanoi3d.q" = low|medium|high 로 고정.
import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { FXAAPass } from "three/addons/postprocessing/FXAAPass.js";
import { canvasFov } from "../sim3d/persp.js";
import { setAt } from "../hanoi.js";
import { dims, layoutSets, cameraFor, sceneRadius, robotPlan, STYLES, ROBOTS, ROBOT_SETS, PL, smooth } from "./plan.js";
import { Kit, Station } from "./station.js";
import { makeRobot } from "./robots.js";
import { robotMaterials, NOISE_GLSL } from "./materials.js";
import { createParty } from "./party.js";

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const QKEY = "ash.display.hanoi3d.q";
const TIERS = [
  { name: "low", pr: 0.85, msaa: 0, fxaa: true, shadow: 1024, refl: 0, tilt: false, grain: 0.6 },
  { name: "medium", pr: 1, msaa: 0, fxaa: true, shadow: 1024, refl: 0.32, tilt: true, grain: 1 },
  { name: "high", pr: 1.5, msaa: 4, fxaa: false, shadow: 2048, refl: 0.5, tilt: true, grain: 1 },
];

/* ══════════ 밝기(테마) ══════════ */
const THEMES = {
  dark: {
    zen: "#04070f", hor: "#161e38", glow: "#26355f", glowK: 0.5, noise: 0.16, ao: 0.55,
    floor: "#0b1020", seam: "#18203b", seamK: 0.6, refl: 0.62, shadow: 0.34, spot: "#b4c4ff", spotK: 0.075,
    envSky: ["#070a14", "#222b4c", "#11152a"],
    boxes: [[8, 4, "#fff2e0", 5.2, [0, 9, 2]], [1.4, 6, "#dbe7ff", 3.6, [-8, 3, 3]], [1.4, 6, "#ffefd9", 3, [8, 3.5, -1]],
      [6, 1.2, "#b9d0ff", 1.8, [0, 2.5, -9]], [3, 3, "#ffe5c2", 1.6, [5, 1.4, 8]], [3, 2, "#e8eeff", 1.4, [-6, 1.2, 7]],
      [10, 0.6, "#ffffff", 1.2, [0, 0.4, 10]]],
    key: ["#fff1df", 2.5], hemi: ["#9db2ff", "#1b140e", 0.16], rimL: ["#8db6ff", 1.4], rimR: ["#ffcf98", 0.9],
    bloom: [0.34, 0.42, 1.7], exposure: 1.0, grain: 0.028, vig: 0.42, envI: 1.15,
  },
  light: {
    zen: "#fbf9f4", hor: "#eee6d4", glow: "#fffaf0", glowK: 0.18, noise: 0.035, ao: 0.32,
    floor: "#ebe2cd", seam: "#d4c5a3", seamK: 0, refl: 0.13, shadow: 0.62, spot: "#ffffff", spotK: 0,
    envSky: ["#ffffff", "#efe6d2", "#d2c19b"],
    boxes: [[8, 4, "#ffffff", 3.2, [0, 9, 2]], [1.4, 6, "#ffffff", 2.2, [-8, 3, 3]], [1.4, 6, "#fff6e8", 1.8, [8, 3.5, -1]],
      [6, 1.2, "#ffffff", 1.2, [0, 2.5, -9]]],
    key: ["#fff7ea", 3.3], hemi: ["#ffffff", "#cbb88b", 0.36], rimL: ["#e2eaff", 0.7], rimR: ["#ffe8c8", 0.5],
    bloom: [0.14, 0.4, 2.2], exposure: 0.97, grain: 0.012, vig: 0.2, envI: 0.74,
  },
};

function envScene(T) {
  const sc = new THREE.Scene();
  const trash = [];
  const sg = new THREE.SphereGeometry(20, 48, 24);
  const sm = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: { a: { value: new THREE.Color(T.envSky[0]) }, b: { value: new THREE.Color(T.envSky[1]) }, c: { value: new THREE.Color(T.envSky[2]) } },
    vertexShader: "varying vec3 vP; void main(){ vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
    fragmentShader: "uniform vec3 a, b, c; varying vec3 vP; void main(){ float h = normalize(vP).y; vec3 col = h > 0.0 ? mix(b, a, pow(h, 0.6)) : mix(b, c, pow(-h, 0.5)); gl_FragColor = vec4(col, 1.0); }",
  });
  trash.push(sg, sm);
  sc.add(new THREE.Mesh(sg, sm));
  for (const [w, h, hex, k, pos] of T.boxes) {
    const g = new THREE.PlaneGeometry(w, h), m = new THREE.MeshBasicMaterial({ color: new THREE.Color(hex).multiplyScalar(k), side: THREE.DoubleSide });
    trash.push(g, m);
    const mesh = new THREE.Mesh(g, m);
    mesh.position.set(...pos); mesh.lookAt(0, 0.5, 0);
    sc.add(mesh);
  }
  return { sc, trash };
}

/* ══════════ 바닥 · 하늘 ══════════ */
const FLOOR_VS = /* glsl */`
#include <common>
#include <shadowmap_pars_vertex>
uniform mat4 uReflMat;
varying vec4 vRefl; varying vec3 vW;
void main() {
  #include <beginnormal_vertex>
  #include <defaultnormal_vertex>
  #include <begin_vertex>
  #include <project_vertex>
  #include <worldpos_vertex>
  #include <shadowmap_vertex>
  vW = (modelMatrix * vec4(transformed, 1.0)).xyz;
  vRefl = uReflMat * vec4(transformed, 1.0);
}`;
const PARTY_GLSL = /* glsl */`
uniform float uParty, uBeat, uBallRot, uTime;
uniform vec4 uPool[8]; uniform vec3 uPoolCol[8];
uniform vec4 uBall; uniform float uLedTile;
float h12(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
vec3 hue3(float h) { return clamp(abs(mod(h * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0); }
vec3 ballDots(vec3 w, float cells, float k) {
  vec3 dir = normalize(w - uBall.xyz);
  float c = cos(uBallRot), s = sin(uBallRot);
  dir = vec3(c * dir.x - s * dir.z, dir.y, s * dir.x + c * dir.z);
  vec2 cell = vec2(atan(dir.z, dir.x), asin(clamp(dir.y, -1.0, 1.0))) * cells;
  vec2 fc = fract(cell) - 0.5;
  float on = step(0.8, h12(floor(cell)));
  return vec3(1.0, 0.96, 0.9) * on * smoothstep(0.16, 0.04, length(fc)) * uBall.w * k;
}`;
const SKY_GLSL = /* glsl */`
uniform vec3 uZen, uHor, uGlow; uniform vec3 uGlowDir;
vec3 skyCol(vec3 d) {
  vec3 col = mix(uHor, uZen, smoothstep(0.0, 0.5, d.y));
  vec3 gd = normalize(uGlowDir);
  float g = max(0.0, dot(normalize(vec3(d.x, max(d.y, 0.0), d.z)), gd));
  return col + uGlow * pow(g, 5.0);
}`;
const FLOOR_FS = /* glsl */`
#include <common>
#include <bsdfs>
#include <lights_pars_begin>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
uniform vec3 uBase, uSeamCol, uSpotCol;
uniform float uSeam, uTile, uRefl, uHasRefl, uShadow, uNoise, uAO;
uniform vec2 uC, uFade;
uniform vec4 uSpot[5];
uniform vec4 uBox[5];
uniform sampler2D tRefl;
varying vec4 vRefl; varying vec3 vW;
${NOISE_GLSL}
${PARTY_GLSL}
${SKY_GLSL}
void main() {
  vec2 p = vW.xz;
  float nz = vnoise(vec3(p * 2.7, 0.0)) * 0.6 + vnoise(vec3(p * 9.0, 3.0)) * 0.4;
  vec3 col = uBase * (1.0 + uNoise * (nz - 0.6));
  vec2 g = abs(fract(p / uTile + 0.5) - 0.5) * uTile;
  float seam = 1.0 - smoothstep(0.0012, 0.0045, min(g.x, g.y));
  col = mix(col, uSeamCol, seam * uSeam);
  for (int i = 0; i < 5; i++) { vec2 d = p - uSpot[i].xy; col += uSpotCol * uSpot[i].w * exp(-dot(d, d) / max(1e-4, uSpot[i].z * uSpot[i].z)); }
  col *= mix(uShadow, 1.0, getShadowMask());
  // 받침 · 테이블 아래 닿는 그늘(부드러운 상자)
  float ao = 1.0;
  for (int i = 0; i < 5; i++) {
    if (uBox[i].z <= 0.0) continue;
    vec2 q = abs(p - uBox[i].xy) - uBox[i].zw;
    float sd = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0);
    ao *= 1.0 - uAO * exp(-max(sd, 0.0) * max(sd, 0.0) / 0.012) * (sd < 0.0 ? 1.0 : 1.0);
  }
  col *= ao;
  if (uParty > 0.001) {
    vec2 tc = floor(p / uLedTile); vec2 tf = abs(fract(p / uLedTile) - 0.5);
    float edge = smoothstep(0.5, 0.42, max(tf.x, tf.y));
    float hs = h12(tc);
    float on = step(0.7, fract(hs * 7.0 + floor(uTime / 0.4839) * 0.37));
    float rr = length(p - uC);
    float wave = 0.5 + 0.5 * sin(rr / uLedTile * 0.9 - uTime * 3.5);
    float near = 1.0 - smoothstep(uFade.x * 0.55, uFade.x * 1.15, rr);
    col += hue3(fract(hs + uTime * 0.04)) * edge * on * (0.022 + 0.05 * uBeat) * uParty * (0.4 + wave) * near;
    for (int i = 0; i < 8; i++) { vec2 d = p - uPool[i].xy; col += uPoolCol[i] * uPool[i].w * exp(-dot(d, d) / max(1e-4, uPool[i].z * uPool[i].z)) * uParty; }
    col += ballDots(vW, 19.0, 0.5);
  }
  if (uHasRefl > 0.5) {
    vec3 V = normalize(cameraPosition - vW);
    float fres = 0.22 + 0.78 * pow(1.0 - clamp(V.y, 0.0, 1.0), 4.0);
    vec2 ruv = vRefl.xy / vRefl.w + (vec2(vnoise(vec3(p * 8.0, 1.0)), vnoise(vec3(p * 8.0, 5.0))) - 0.5) * 0.006;
    vec3 rc = textureLod(tRefl, ruv, 2.3 + 1.6 * nz).rgb * 0.55 + textureLod(tRefl, ruv, 0.7).rgb * 0.45;
    rc = rc / (1.0 + max(max(rc.r, rc.g), rc.b) * 0.45);   // 아주 밝은 반짝임은 눌러서(번짐 덩어리 방지)
    col = mix(col, rc, uRefl * fres);
  }
  vec3 vd = normalize(vW - cameraPosition);
  col = mix(col, skyCol(vec3(vd.x, 0.0, vd.z)), smoothstep(uFade.x, uFade.y, length(p - uC)));
  gl_FragColor = vec4(col, 1.0);
}`;
const DOME_FS = /* glsl */`
uniform vec3 uWash;
varying vec3 vW; varying vec3 vD;
${PARTY_GLSL}
${SKY_GLSL}
void main() {
  vec3 d = normalize(vD);
  vec3 col = skyCol(d);
  if (uParty > 0.001) {
    col += uWash * uParty * (0.35 + 0.25 * uBeat) * smoothstep(0.6, 0.0, d.y);
    col += ballDots(vW, 19.0, 0.3);
  }
  gl_FragColor = vec4(col, 1.0);
}`;
/** 틸트시프트(미니어처 느낌): 가운데 띠는 또렷하게, 위아래로 갈수록 흐리게 — 가로 · 세로 두 번 */
const TILT = {
  uniforms: { tDiffuse: { value: null }, uDir: { value: new THREE.Vector2(1 / 1600, 0) }, uFocus: { value: 0.47 }, uBand: { value: 0.17 }, uAmt: { value: 2.2 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
  fragmentShader: /* glsl */`
uniform sampler2D tDiffuse; uniform vec2 uDir; uniform float uFocus, uBand, uAmt; varying vec2 vUv;
void main() {
  float b = smoothstep(uBand, uBand + 0.3, abs(vUv.y - uFocus)) * uAmt;
  vec2 o1 = uDir * b * 1.3846153846, o2 = uDir * b * 3.2307692308;
  gl_FragColor = texture2D(tDiffuse, vUv) * 0.2270270270
    + (texture2D(tDiffuse, vUv + o1) + texture2D(tDiffuse, vUv - o1)) * 0.3162162162
    + (texture2D(tDiffuse, vUv + o2) + texture2D(tDiffuse, vUv - o2)) * 0.0702702703;
}`,
};
const GRADE = {
  uniforms: { tDiffuse: { value: null }, uTime: { value: 0 }, uVig: { value: 0.4 }, uGrain: { value: 0.03 }, uCA: { value: 0.0025 } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
  fragmentShader: /* glsl */`
uniform sampler2D tDiffuse; uniform float uTime, uVig, uGrain, uCA; varying vec2 vUv;
void main() {
  vec2 d = vUv - 0.5; float r2 = dot(d, d);
  vec2 o = d * uCA * r2 * 4.0;
  vec3 c = vec3(texture2D(tDiffuse, vUv + o).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - o).b);
  c *= 1.0 - uVig * smoothstep(0.08, 0.62, r2 * 1.6);
  float n = fract(sin(dot(vUv * (1.0 + fract(uTime)), vec2(12.9898, 78.233))) * 43758.5453);
  c += (n - 0.5) * uGrain;
  gl_FragColor = vec4(c, 1.0);
}`,
};

function detectTier(renderer) {
  try {
    const f = localStorage.getItem(QKEY);
    const i = TIERS.findIndex((t) => t.name === f);
    if (i >= 0) return { tier: i, forced: true, gpu: "forced" };
  } catch { /* 저장소를 못 씀 */ }
  let gpu = "";
  try {
    const gl = renderer.getContext();
    const ext = gl.getExtension("WEBGL_debug_renderer_info");
    gpu = String(ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER));
  } catch { /* 모름 */ }
  if (/swiftshader|llvmpipe|software|basic render|softpipe/i.test(gpu)) return { tier: 0, forced: false, gpu };
  if (/intel|mali|adreno|powervr|videocore|apple gpu/i.test(gpu)) return { tier: 1, forced: false, gpu };
  return { tier: 2, forced: false, gpu };
}

/**
 * 엔진. canvas 는 화면 전체를 덮고(16:9 무대 바깥 여백까지), 시야각은 부모(무대)의 높이에 맞춘다.
 */
export function createHanoiEngine(canvas, { theme = "dark", getElapsed = () => 0, onError, onFirstFrame } = {}) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: "high-performance", stencil: false });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  renderer.transmissionResolutionScale = 0.6;      // 유리 원판 굴절용 그림(높음에서만)은 조금 작게
  const det = detectTier(renderer);
  let tier = det.tier;
  const maxTier = tier;
  let Q = TIERS[tier];
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  let pr = Math.min(dpr, Q.pr);
  renderer.setPixelRatio(pr);

  const res = [];                       // 엔진이 끝날 때 버릴 것
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(28, 16 / 9, 0.05, 400);
  scene.add(camera);
  let T = THEMES[theme] || THEMES.dark, themeName = theme;

  // ── 빛 ──
  const hemi = new THREE.HemisphereLight("#fff", "#000", 0.2);
  const key = new THREE.DirectionalLight("#fff", 2.5);
  key.castShadow = true;
  key.shadow.bias = -0.0004; key.shadow.normalBias = 0.012; key.shadow.radius = 3;
  const rimL = new THREE.DirectionalLight("#fff", 1), rimR = new THREE.DirectionalLight("#fff", 1);
  scene.add(hemi, key, key.target, rimL, rimL.target, rimR, rimR.target);
  function setShadowSize(s) {
    key.shadow.mapSize.set(s, s);
    if (key.shadow.map) { key.shadow.map.dispose(); key.shadow.map = null; }
  }
  setShadowSize(Q.shadow);

  // ── 하늘(둥근 막) · 바닥 ──
  const party = createParty(scene, tier, res);
  const domeGeo = new THREE.SphereGeometry(120, 64, 32);
  const domeMat = new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: { uZen: { value: new THREE.Color() }, uHor: { value: new THREE.Color() }, uGlow: { value: new THREE.Color() },
      uGlowDir: { value: new THREE.Vector3(0, 0.08, -1) }, uWash: { value: new THREE.Color() }, uTime: { value: 0 }, uLedTile: { value: 0.3 } },
    vertexShader: "varying vec3 vW; varying vec3 vD; void main(){ vec4 w = modelMatrix * vec4(position, 1.0); vW = w.xyz; vD = position; gl_Position = projectionMatrix * viewMatrix * w; }",
    fragmentShader: DOME_FS,
  });
  Object.assign(domeMat.uniforms, party.uniforms);
  const dome = new THREE.Mesh(domeGeo, domeMat);
  dome.renderOrder = -10;
  dome.frustumCulled = false;
  scene.add(dome);
  res.push(domeGeo, domeMat);

  const reflRT = new THREE.WebGLRenderTarget(4, 4, { type: THREE.HalfFloatType, generateMipmaps: true, minFilter: THREE.LinearMipmapLinearFilter, magFilter: THREE.LinearFilter });
  res.push(reflRT);
  const floorGeo = new THREE.PlaneGeometry(260, 260, 1, 1);
  floorGeo.rotateX(-Math.PI / 2);
  const floorMat = new THREE.ShaderMaterial({
    lights: true,
    uniforms: THREE.UniformsUtils.merge([THREE.UniformsLib.lights, {
      uBase: { value: new THREE.Color() }, uSeamCol: { value: new THREE.Color() }, uSeam: { value: 0.5 }, uTile: { value: 1.2 },
      uRefl: { value: 0.5 }, uHasRefl: { value: 1 }, uShadow: { value: 0.4 }, uReflMat: { value: new THREE.Matrix4() },
      uC: { value: new THREE.Vector2() }, uFade: { value: new THREE.Vector2(8, 30) },
      uSpot: { value: Array.from({ length: 5 }, () => new THREE.Vector4()) }, uSpotCol: { value: new THREE.Color() }, uTime: { value: 0 },
      uBox: { value: Array.from({ length: 5 }, () => new THREE.Vector4()) }, uNoise: { value: 0.16 }, uAO: { value: 0.5 }, uLedTile: { value: 0.3 },
    }]),
    vertexShader: FLOOR_VS, fragmentShader: FLOOR_FS,
  });
  floorMat.uniforms.tRefl = { value: reflRT.texture };
  for (const k of ["uZen", "uHor", "uGlow", "uGlowDir"]) floorMat.uniforms[k] = domeMat.uniforms[k];
  Object.assign(floorMat.uniforms, party.uniforms);
  const floor = new THREE.Mesh(floorGeo, floorMat);
  floor.receiveShadow = true;
  floor.renderOrder = -5;
  scene.add(floor);
  res.push(floorGeo, floorMat);

  // 바닥 반사 카메라(바닥 y = 0 에 비친 카메라 + 바닥 아래를 자르는 비스듬한 가까운 면)
  const reflCam = new THREE.PerspectiveCamera();
  const _N = new THREE.Vector3(0, 1, 0), _O = new THREE.Vector3();
  const _view = new THREE.Vector3(), _tgt = new THREE.Vector3(), _look = new THREE.Vector3(), _cpos = new THREE.Vector3(), _rot = new THREE.Matrix4();
  const _plane = new THREE.Plane(), _clip = new THREE.Vector4(), _q = new THREE.Vector4();
  function renderReflection() {
    if (!Q.refl) return;
    _cpos.setFromMatrixPosition(camera.matrixWorld);
    _view.subVectors(_O, _cpos);
    if (_view.dot(_N) > 0) return;
    _view.reflect(_N).negate();
    _rot.extractRotation(camera.matrixWorld);
    _look.set(0, 0, -1).applyMatrix4(_rot).add(_cpos);
    _tgt.subVectors(_O, _look).reflect(_N).negate();
    reflCam.position.copy(_view);
    reflCam.up.set(0, 1, 0).applyMatrix4(_rot).reflect(_N);
    reflCam.lookAt(_tgt);
    reflCam.far = camera.far;
    reflCam.updateMatrixWorld();
    reflCam.projectionMatrix.copy(camera.projectionMatrix);
    const M = floorMat.uniforms.uReflMat.value;
    M.set(0.5, 0, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0, 0.5, 0.5, 0, 0, 0, 1);
    M.multiply(reflCam.projectionMatrix).multiply(reflCam.matrixWorldInverse).multiply(floor.matrixWorld);
    _plane.setFromNormalAndCoplanarPoint(_N, _O).applyMatrix4(reflCam.matrixWorldInverse);
    _clip.set(_plane.normal.x, _plane.normal.y, _plane.normal.z, _plane.constant);
    const P = reflCam.projectionMatrix.elements;
    _q.set((Math.sign(_clip.x) + P[8]) / P[0], (Math.sign(_clip.y) + P[9]) / P[5], -1, (1 + P[10]) / P[14]);
    _clip.multiplyScalar(2 / _clip.dot(_q));
    P[2] = _clip.x; P[6] = _clip.y; P[10] = _clip.z + 1 - 0.003; P[14] = _clip.w;
    reflCam.projectionMatrixInverse.copy(reflCam.projectionMatrix).invert();
    floor.visible = false;
    const sau = renderer.shadowMap.autoUpdate;
    renderer.shadowMap.autoUpdate = false;
    renderer.setRenderTarget(reflRT);
    renderer.clear();
    renderer.render(scene, reflCam);
    renderer.setRenderTarget(null);
    renderer.shadowMap.autoUpdate = sau;
    floor.visible = true;
  }

  // ── 환경광 ──
  let envRT = null;
  const pmrem = new THREE.PMREMGenerator(renderer);
  function buildEnv() {
    const { sc, trash } = envScene(T);
    const rt = pmrem.fromScene(sc, 0.035);
    for (const o of trash) o.dispose();
    if (envRT) envRT.dispose();
    envRT = rt;
    scene.environment = rt.texture;
  }

  // ── 그리기 단계 ──
  let composer = null, bloom = null, tiltH = null, tiltV = null, grade = null, outPass = null;
  let size = { cw: 0, ch: 0, fh: 0 };
  function buildComposer() {
    composer?.dispose();
    const rt = new THREE.WebGLRenderTarget(Math.max(1, size.cw * pr), Math.max(1, size.ch * pr), { type: THREE.HalfFloatType, samples: Q.msaa });
    composer = new EffectComposer(renderer, rt);
    composer.setPixelRatio(pr);
    composer.setSize(size.cw || 1, size.ch || 1);
    composer.addPass(new RenderPass(scene, camera));
    bloom = new UnrealBloomPass(new THREE.Vector2(size.cw || 1, size.ch || 1), T.bloom[0], T.bloom[1], T.bloom[2]);
    composer.addPass(bloom);
    tiltH = new ShaderPass(TILT); tiltV = new ShaderPass(TILT);
    composer.addPass(tiltH); composer.addPass(tiltV);
    outPass = new OutputPass();
    composer.addPass(outPass);
    grade = new ShaderPass(GRADE);
    composer.addPass(grade);
    if (Q.fxaa) composer.addPass(new FXAAPass());
  }

  // ── 테마 적용 ──
  function applyTheme(name) {
    themeName = THEMES[name] ? name : "dark";
    T = THEMES[themeName];
    domeMat.uniforms.uZen.value.set(T.zen); domeMat.uniforms.uHor.value.set(T.hor);
    domeMat.uniforms.uGlow.value.set(T.glow).multiplyScalar(T.glowK);
    const U = floorMat.uniforms;
    U.uBase.value.set(T.floor); U.uSeamCol.value.set(T.seam); U.uSeam.value = T.seamK;
    U.uRefl.value = T.refl; U.uShadow.value = T.shadow; U.uSpotCol.value.set(T.spot); U.uNoise.value = T.noise; U.uAO.value = T.ao;
    scene.fog = new THREE.Fog(T.hor, 30, 140);
    renderer.toneMappingExposure = T.exposure;
    buildEnv();
    if (bloom) { bloom.strength = T.bloom[0]; bloom.radius = T.bloom[1]; bloom.threshold = T.bloom[2]; }
    rebuildAll = true;
  }

  /* ══════════ 세트 ══════════ */
  let cfg = null, G = null, kit = null, S = 1, speed = "x1", rebuildAll = false, quiet = false;
  const sets = [];             // { i, root, station, robot, x, z, tx, tz, k(나타남 0~1), alive }
  let lift = 0, liftT = 0;
  let RM = null;               // 로봇 재질(처음 로봇 모드에서 만든다)
  const sceneC = { x: 0, z: 0 };
  let sceneR = 2;

  function makeSet(i) {
    const root = new THREE.Group();
    scene.add(root);
    return { i, root, station: null, robot: null, x: 0, z: 0, tx: 0, tz: 0, k: 0, alive: true, plan: {} };
  }
  function buildStation(s, drop) {
    if (s.station) { s.root.remove(s.station.root); s.station.dispose(); }
    s.station = new Station(kit, STYLES[s.i % STYLES.length], themeName);
    s.root.add(s.station.root);
    s.station.setLift(lift);
    if (drop) s.station.dropIn();
  }
  function buildRobot(s) {
    if (s.robot) { s.root.remove(s.robot.root); s.robot.dispose(); s.robot = null; }
    if (!RM) { RM = robotMaterials(); }
    s.robot = makeRobot(ROBOTS[s.i % ROBOTS.length], RM, G);
    s.robot.root.traverse((o) => { if (o.isMesh) o.frustumCulled = true; });
    s.root.add(s.robot.root);
  }
  function dropRobot(s) { if (s.robot) { s.root.remove(s.robot.root); s.robot.dispose(); s.robot = null; } }

  let camGoal = null;
  const cam = { at: new THREE.Vector3(), d: 6, az: 0, el: 0.2, fov: 28, init: false };

  function applyConfig() {
    if (!cfg) return;
    const L = cfg.TL.L;
    const geoKey = `${L.n}|${L.pegs}|${tier}`;
    const newGeo = !kit || kit.key !== geoKey;
    if (newGeo) {
      if (kit) kit.dispose();
      G = dims(L);
      kit = new Kit(G, tier);
      kit.key = geoKey;
    }
    S = clamp(cfg.sets | 0, 1, 5);
    speed = cfg.speed;
    while (sets.length < S) sets.push(makeSet(sets.length));
    const P = layoutSets(G, S);
    for (const s of sets) {
      if (s.i < S) {
        s.alive = true;
        s.tx = P[s.i].x; s.tz = P[s.i].z;
        if (!s.station || newGeo || rebuildAll) buildStation(s, !quiet && (newGeo || !s.station));
        if (s.k <= 0.001) { s.x = s.tx; s.z = s.tz; }
        if (s.robot && newGeo) buildRobot(s);
      } else s.alive = false;
    }
    rebuildAll = false; quiet = false;
    camGoal = cameraFor(G, S);
    sceneR = sceneRadius(G, S);
    if (!cam.init) {
      cam.at.set(...camGoal.at); cam.d = camGoal.d; cam.az = camGoal.az; cam.el = camGoal.el; cam.fov = camGoal.fov; cam.init = true;
    }
    // 그림자 상자 · 바닥 무늬 · 무대 빛 웅덩이
    const sr = sceneR + 1.2;
    const sc = key.shadow.camera;
    sc.left = -sr; sc.right = sr; sc.top = sr; sc.bottom = -sr; sc.near = 0.5; sc.far = 80;
    sc.updateProjectionMatrix();
    floorMat.uniforms.uFade.value.set(sceneR + 3, sceneR + 26);
    floorMat.uniforms.uTile.value = S >= 4 ? 1.6 : 1.2;

  }

  // 처음 한 번: 재질 셰이더를 미리(가능하면 나란히) 엮어 두고 그 뒤에 그린다 — 그동안 액자는 평면 그림을 보여 준다
  let compiled = false, compiling = false, firstDone = false;
  function precompile() {
    if (compiled || compiling) return;
    compiling = true;
    const done = () => { compiled = true; compiling = false; };
    setTimeout(done, 4000);            // 엮기가 오래 걸리거나 끝을 못 알려도 4초 뒤에는 그리기 시작
    try {
      camera.position.set(0, 1, 6); camera.lookAt(0, 0.4, 0); camera.updateMatrixWorld();
      const p = renderer.compileAsync ? renderer.compileAsync(scene, camera) : null;
      if (p && p.then) p.then(done, done); else done();
    } catch { done(); }
  }
  function setConfig(c) {
    cfg = c;
    try { applyConfig(); precompile(); } catch (e) { fail(e); }
  }

  /* ══════════ 크기 · 품질 ══════════ */
  function measure() {
    const cw = canvas.clientWidth || 1, ch = canvas.clientHeight || 1;
    const fr = canvas.parentElement?.getBoundingClientRect();
    const fh = fr && fr.height > 0 ? fr.height : ch;
    if (cw !== size.cw || ch !== size.ch || fh !== size.fh) {
      size = { cw, ch, fh };
      renderer.setSize(cw, ch, false);
      if (!composer) buildComposer();
      composer.setPixelRatio(pr);
      composer.setSize(cw, ch);
      const rw = Math.max(16, Math.round(cw * pr * (Q.refl || 0.25))), rh = Math.max(16, Math.round(ch * pr * (Q.refl || 0.25)));
      reflRT.setSize(rw, rh);
      tiltH.uniforms.uDir.value.set(1 / (cw * pr), 0); tiltV.uniforms.uDir.value.set(0, 1 / (ch * pr));
    }
  }
  const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(() => { size.cw = -1; }) : null;
  ro?.observe(canvas);
  if (canvas.parentElement) ro?.observe(canvas.parentElement);

  function setTier(t) {
    t = clamp(t, 0, 2);
    if (t === tier) return;
    tier = t; Q = TIERS[t];
    pr = Math.min(dpr, Q.pr);
    renderer.setPixelRatio(pr);
    setShadowSize(Q.shadow);
    floorMat.uniforms.uHasRefl.value = Q.refl ? 1 : 0;
    party.setTier(t);
    buildComposer();
    size.cw = -1;
    if (cfg) { rebuildAll = true; quiet = true; if (kit) kit.key = ""; applyConfig(); }
  }
  // 그리는 간격을 재서 느리면 한 단계씩 낮춘다(고정이면 안 바꾼다)
  const perf = { acc: 0, n: 0, slow: 0, fast: 0 };
  function adapt(dtMs) {
    if (det.forced || paused) return;
    if (dtMs <= 0 || dtMs > 250) return;
    perf.acc += dtMs; perf.n++;
    if (perf.acc < 2000) return;
    const avg = perf.acc / perf.n;
    perf.acc = 0; perf.n = 0;
    if (avg > 26) { perf.slow++; perf.fast = 0; } else if (avg < 17.5) { perf.fast++; perf.slow = 0; } else { perf.slow = 0; perf.fast = 0; }
    if (perf.slow >= 2) {
      perf.slow = 0;
      if (pr > 0.75 && tier > 0) { pr = Math.max(0.75, pr * 0.85); renderer.setPixelRatio(pr); size.cw = -1; }
      else if (tier > 0) setTier(tier - 1);
      else if (pr > 0.6) { pr = Math.max(0.6, pr * 0.85); renderer.setPixelRatio(pr); size.cw = -1; }
    } else if (perf.fast >= 6 && tier < maxTier) { perf.fast = 0; setTier(tier + 1); }
  }

  /* ══════════ 그리기 ══════════ */
  let raf = 0, last = 0, lastFrame = 0, paused = false, lost = false, dead = false;
  const camPos = new THREE.Vector3();
  const _dir = new THREE.Vector3(0.42, 0.86, 0.55).normalize();
  const _rimLd = new THREE.Vector3(-0.7, 0.55, -0.6).normalize(), _rimRd = new THREE.Vector3(0.75, 0.5, -0.55).normalize();
  const hueL = new THREE.Color(), hueR = new THREE.Color();
  const partyCtx = { level: 0, beat: 0 };

  function fail(e) {
    if (dead) return;
    dead = true;
    cancelAnimationFrame(raf);
    onError?.(e);
  }

  function frame(now) {
    raf = requestAnimationFrame(frame);
    if (lost || dead || !cfg || !compiled) return;
    const minGap = paused ? 31 : 15.5;
    if (now - lastFrame < minGap) return;
    const dtMs = last ? now - last : 16;
    last = now; lastFrame = now;
    try { step(now / 1000, Math.min(0.1, dtMs / 1000)); } catch (e) { fail(e); return; }
    adapt(dtMs);
  }

  function step(time, dt) {
    measure();
    // 로봇 모드로(세트 5개) 테이블이 솟는다
    const wantLift = S >= ROBOT_SETS ? 1 : 0;
    liftT += (wantLift ? 1 : -1) * dt / 1.4;
    liftT = clamp(liftT, 0, 1);
    lift = smooth(liftT);
    // 세트 자리 · 나타남
    for (const s of sets) {
      const k = 1 - Math.exp(-dt * 3.2);
      s.x += (s.tx - s.x) * k; s.z += (s.tz - s.z) * k;
      s.k = clamp(s.k + (s.alive ? 1 : -1) * dt / 0.6, 0, 1);
      const sk = s.alive ? 1 - Math.pow(1 - s.k, 3) : s.k * s.k;
      s.root.visible = s.k > 0.001;
      s.root.position.set(s.x, 0, s.z);
      s.root.scale.setScalar(Math.max(0.001, sk));
      if (!s.alive && s.k <= 0 && s.station) { s.root.remove(s.station.root); s.station.dispose(); s.station = null; dropRobot(s); }
      if (s.station) s.station.setLift(lift);
      if (s.alive && S >= ROBOT_SETS && !s.robot && s.station) buildRobot(s);
      if (s.robot && liftT <= 0 && S < ROBOT_SETS) dropRobot(s);
    }
    // 바닥: 세트마다 빛 웅덩이 · 닿는 그늘(움직이는 자리 그대로)
    const spots = floorMat.uniforms.uSpot.value, boxes = floorMat.uniforms.uBox.value;
    for (let i = 0; i < 5; i++) {
      const s = sets[i];
      if (s && s.station && s.k > 0.001 && G) {
        const sk = s.root.scale.x;
        spots[i].set(s.x, s.z + 0.1, G.W * 0.5 * sk, T.spotK * sk);
        const hw = lift > 0.01 ? G.plinth.w / 2 : G.W / 2 - 0.04, hd = lift > 0.01 ? G.plinth.d / 2 : G.D / 2 - 0.04;
        boxes[i].set(s.x, s.z, hw * sk, hd * sk);
      } else { spots[i].set(0, 0, 1, 0); boxes[i].set(0, 0, 0, 0); }
    }
    // 카메라(부드럽게 따라가며 아주 천천히 숨쉰다)
    const pl = party.state.level;
    if (camGoal) {
      const k = 1 - Math.exp(-dt * 2.2);
      cam.at.x += (camGoal.at[0] - cam.at.x) * k; cam.at.y += (camGoal.at[1] - cam.at.y) * k; cam.at.z += (camGoal.at[2] - cam.at.z) * k;
      cam.d += (camGoal.d - cam.d) * k; cam.az += (camGoal.az - cam.az) * k; cam.el += (camGoal.el - cam.el) * k; cam.fov += (camGoal.fov - cam.fov) * k;
    }
    const az = cam.az + 0.035 * Math.sin(time * 0.11) + pl * 0.15 * Math.sin(time * 0.23);
    const el = cam.el + 0.012 * Math.sin(time * 0.13 + 1) + pl * 0.03 * Math.sin(time * 0.31);
    const d = cam.d * (1 + 0.012 * Math.sin(time * 0.09) - pl * 0.004 * party.state.beat);
    camPos.set(cam.at.x + d * Math.sin(az) * Math.cos(el), cam.at.y + d * Math.sin(el), cam.at.z + d * Math.cos(az) * Math.cos(el));
    camera.position.copy(camPos);
    camera.up.set(0, 1, 0);
    camera.lookAt(cam.at);
    camera.aspect = size.cw / size.ch;
    camera.fov = canvasFov(cam.fov, size.fh, size.ch);
    camera.near = Math.max(0.03, d * 0.02);
    camera.far = 400;
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld();
    dome.position.copy(camPos);
    // 빛
    sceneC.x = cam.at.x; sceneC.z = cam.at.z;
    key.position.set(sceneC.x + _dir.x * 24, _dir.y * 24, sceneC.z + _dir.z * 24);
    key.target.position.set(sceneC.x, 0, sceneC.z);
    rimL.position.set(sceneC.x + _rimLd.x * 20, _rimLd.y * 20, sceneC.z + _rimLd.z * 20); rimL.target.position.set(sceneC.x, 0, sceneC.z);
    rimR.position.set(sceneC.x + _rimRd.x * 20, _rimRd.y * 20, sceneC.z + _rimRd.z * 20); rimR.target.position.set(sceneC.x, 0, sceneC.z);
    const P = party.update(speed === "x4", time, dt, sceneC, sceneR, camPos, (S >= ROBOT_SETS ? PL : 0) + (G ? G.top : 0.6) + 0.9);
    partyCtx.level = P.level; partyCtx.beat = P.beat;
    const dim = 1 - P.level * 0.55;
    key.color.set(T.key[0]); key.intensity = T.key[1] * dim;
    hemi.color.set(T.hemi[0]); hemi.groundColor.set(T.hemi[1]); hemi.intensity = T.hemi[2] * (1 - P.level * 0.4);
    hueL.setHSL((P.hue + 0.62) % 1, 1, 0.55); hueR.setHSL((P.hue + 0.95) % 1, 1, 0.55);
    rimL.color.set(T.rimL[0]).lerp(hueL, P.level); rimL.intensity = T.rimL[1] * (1 + P.level * (1.6 + 1.2 * P.beat));
    rimR.color.set(T.rimR[0]).lerp(hueR, P.level); rimR.intensity = T.rimR[1] * (1 + P.level * (2 + 1.2 * P.beat));
    scene.environmentIntensity = T.envI * (1 - P.level * 0.5);
    domeMat.uniforms.uWash.value.copy(hueL).multiplyScalar(0.08);
    domeMat.uniforms.uTime.value = time;
    floorMat.uniforms.uTime.value = time;
    floorMat.uniforms.uC.value.set(sceneC.x, sceneC.z);
    floorMat.uniforms.uLedTile.value = clamp(0.16 * Math.sqrt(sceneR), 0.18, 0.5);
    if (bloom) bloom.strength = T.bloom[0] * (1 + P.level * 0.7) + P.level * 0.12 * P.beat;
    // 원판 · 로봇
    const e = getElapsed();
    const TL = cfg.TL;
    const robotMode = S >= ROBOT_SETS;
    for (const s of sets) {
      if (!s.station || s.k <= 0) continue;
      const st = setAt(TL, e, s.i, speed);
      s.station.update(st, robotMode && !!s.robot, dt, partyCtx);
      if (s.robot) {
        const plan = robotPlan(G, st, s.plan);
        const rise = (1 - lift) * 2.3;
        s.robot.root.position.y = -rise;
        s.robot.update(G, plan, PL * lift + rise, dt, time);
      }
    }
    if (RM) {
      const hc = P.level > 0.01 ? new THREE.Color().setHSL((P.hue * 3) % 1, 1, 0.6).multiplyScalar(3.2) : null;
      RM.led.color.set("#5fe6ff").multiplyScalar(3.2);
      if (hc) RM.led.color.lerp(hc, P.level);
    }
    // 그리기
    tiltH.enabled = tiltV.enabled = Q.tilt && S > 1;
    const amt = 2.2 * pr * (S >= ROBOT_SETS ? 0.8 : 1);
    tiltH.uniforms.uAmt.value = amt; tiltV.uniforms.uAmt.value = amt;
    grade.uniforms.uTime.value = time;
    grade.uniforms.uVig.value = T.vig + P.level * 0.12;
    grade.uniforms.uGrain.value = T.grain * Q.grain;
    renderReflection();
    composer.render(dt);
    if (!firstDone) { firstDone = true; onFirstFrame?.(); }
  }

  /* ══════════ 문맥 잃음 · 정리 ══════════ */
  const onLost = (ev) => { ev.preventDefault(); lost = true; };
  const onRestored = () => { lost = false; size.cw = -1; try { buildEnv(); buildComposer(); } catch (e) { fail(e); } };
  canvas.addEventListener("webglcontextlost", onLost);
  canvas.addEventListener("webglcontextrestored", onRestored);

  applyTheme(theme);
  floorMat.uniforms.uHasRefl.value = Q.refl ? 1 : 0;
  raf = requestAnimationFrame(frame);

  return {
    setConfig,
    setTheme(name) { if (name === themeName) return; try { applyTheme(name); applyConfig(); } catch (e) { fail(e); } },
    setPaused(p) { paused = !!p; },
    get stats() { return { tier: TIERS[tier].name, pr, gpu: det.gpu, forced: det.forced, calls: renderer.info.render.calls, tris: renderer.info.render.triangles }; },
    dispose() {
      dead = true;
      cancelAnimationFrame(raf);
      ro?.disconnect();
      canvas.removeEventListener("webglcontextlost", onLost);
      canvas.removeEventListener("webglcontextrestored", onRestored);
      for (const s of sets) { if (s.station) s.station.dispose(); dropRobot(s); }
      kit?.dispose();
      if (RM) { for (const k of Object.keys(RM)) { if (k === "tex") RM.tex.forEach((t) => t.dispose()); else RM[k].dispose?.(); } }
      for (const o of res) o.dispose?.();
      envRT?.dispose();
      pmrem.dispose();
      composer?.dispose();
      renderer.dispose();
    },
  };
}
