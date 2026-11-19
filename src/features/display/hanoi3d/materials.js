// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 재질 (hanoi3d/materials.js)
// 세트마다 원판 재질이 다르다 — 사탕 칠(candy) · 금속(metal) · 유리(glass) · 네온(neon) · 나무(wood).
// 받침은 호두나무 · 검은 대리석 · 흰 대리석 · 검은 유리 · 밝은 참나무. 나뭇결 · 대리석 결은 그림 파일 없이 셰이더로 만든다(onBeforeCompile).
// 원판 색은 2D 와 같은 차례: 큰 판(아래) 따뜻한 색 → 작은 판(위) 차가운 색.
import * as THREE from "three";

export const RAMPS = {
  candy: ["#ef5a4c", "#f6b02d", "#8bcf4f", "#2fc2ad", "#4c8ff0", "#9a6ff0"],
  metal: ["#d9aa4e", "#e2a387", "#cc7a52", "#cdd1d7", "#7f9cd8", "#a585e2"],
  glass: ["#ffb08a", "#ffd47a", "#b9f2a6", "#93e8f2", "#a6c2ff", "#d9b2ff"],
  neon: ["#ff3d6e", "#ff9f1a", "#d8ff3a", "#2dffc4", "#3db8ff", "#b44dff"],
  wood: ["#4a2e1b", "#6e3f25", "#8c5a33", "#b07d4c", "#cfa56f", "#e6c99a"],
};
/** 원판 d(0 = 가장 작은 판)의 색 */
export function rampColor(name, n, d) {
  const R = RAMPS[name] || RAMPS.candy;
  const u = n > 1 ? ((n - 1 - d) / (n - 1)) * (R.length - 1) : 0;
  const i = Math.min(R.length - 2, Math.floor(u));
  return new THREE.Color(R[i]).lerp(new THREE.Color(R[i + 1]), u - i);
}

/* ── 셰이더 조각: 값 잡음 · 겹친 잡음 ── */
export const NOISE_GLSL = /* glsl */`
float h3n(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
float vnoise(vec3 x) {
  vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(mix(h3n(i), h3n(i + vec3(1,0,0)), f.x), mix(h3n(i + vec3(0,1,0)), h3n(i + vec3(1,1,0)), f.x), f.y),
             mix(mix(h3n(i + vec3(0,0,1)), h3n(i + vec3(1,0,1)), f.x), mix(h3n(i + vec3(0,1,1)), h3n(i + vec3(1,1,1)), f.x), f.y), f.z);
}
float fbm3(vec3 p) { float a = 0.5, s = 0.0; for (int i = 0; i < 4; i++) { s += a * vnoise(p); p = p * 2.03 + 7.1; a *= 0.5; } return s; }
`;

function inject(m, key, uniforms, frag, defines = "") {
  m.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, uniforms);
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vObjP;")
      .replace("#include <begin_vertex>", "#include <begin_vertex>\nvObjP = position;");
    const decl = Object.keys(uniforms).map((k) => {
      const v = uniforms[k].value;
      return `uniform ${v && v.isColor ? "vec3" : "float"} ${k};`;
    }).join("\n");
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", `#include <common>\n${defines}\nvarying vec3 vObjP;\n${decl}\n${NOISE_GLSL}`)
      .replace("#include <color_fragment>", `#include <color_fragment>\n${frag}`);
  };
  m.customProgramCacheKey = () => key;
  return m;
}

/** 나뭇결: 원판은 나이테(가운데에서 둥글게), 받침은 길게 뻗은 결 */
const WOOD = /* glsl */`
{
  #ifdef WOOD_PLANK
    float wob = fbm3(vec3(vObjP.x * 2.2, vObjP.z * 7.0, uSeed)) * 1.4;
    float rings = fract(vObjP.z * uRing + vObjP.y * uRing * 0.6 + wob);
    float fine = vnoise(vec3(vObjP.x * 3.0, vObjP.z * 260.0, uSeed));
  #else
    float rr = length(vObjP.xz);
    float wob = fbm3(vec3(vObjP.xz * 13.0, uSeed)) * 0.7;
    float rings = fract(rr * uRing + wob);
    float fine = vnoise(vec3(vObjP.xz * 230.0, uSeed));
  #endif
  float late = smoothstep(0.0, 0.16, rings) * (1.0 - smoothstep(0.5, 1.0, rings));
  diffuseColor.rgb *= mix(0.74, 1.07, late) * mix(0.9, 1.05, fine);
}
`;
export function woodMaterial(color, { plank = false, ring = 60, seed = 1.7, rough = 0.5, coat = 0.55 } = {}) {
  const m = new THREE.MeshPhysicalMaterial({ color, roughness: rough, metalness: 0, clearcoat: coat, clearcoatRoughness: 0.22 });
  return inject(m, plank ? "ash-wood-plank" : "ash-wood-ring", { uRing: { value: ring }, uSeed: { value: seed } }, WOOD, plank ? "#define WOOD_PLANK" : "");
}

/** 대리석 결 */
const MARBLE = /* glsl */`
{
  float m = fbm3(vObjP * 2.6 + uSeed);
  float v = abs(sin((vObjP.x * 1.7 + vObjP.z * 2.9 + m * 4.2) * 3.14159));
  float vein = 1.0 - smoothstep(0.0, 0.09, v);
  float thin = 1.0 - smoothstep(0.0, 0.035, abs(sin((vObjP.x * 4.1 - vObjP.z * 3.3 + m * 6.0) * 3.14159)));
  diffuseColor.rgb = mix(diffuseColor.rgb, uVein, clamp(vein * 0.8 + thin * 0.35, 0.0, 1.0));
  diffuseColor.rgb *= 0.94 + 0.1 * vnoise(vObjP * 40.0);
}
`;
export function marbleMaterial(color, vein, { rough = 0.2, coat = 1, seed = 3.3 } = {}) {
  const m = new THREE.MeshPhysicalMaterial({ color, roughness: rough, metalness: 0, clearcoat: coat, clearcoatRoughness: 0.08 });
  return inject(m, "ash-marble", { uVein: { value: new THREE.Color(vein) }, uSeed: { value: seed } }, MARBLE);
}

/** HDR 빛(블룸이 번지게) — 1 보다 밝은 색 */
export function glowMaterial(hex, k = 3, extra = {}) {
  const c = new THREE.Color(hex).multiplyScalar(k);
  return new THREE.MeshBasicMaterial({ color: c, ...extra });
}

/**
 * 세트 재질 한 벌: 원판 n 개 · 기둥 · 기둥 받침 고리 · 받침 · 글자색 · (네온) 띠
 * tier: 0 낮음 · 1 보통 · 2 높음 — 유리는 높음에서만 진짜 투과(굴절 · 분산), 나머지는 수정 같은 무지개 막
 */
export function styleMaterials(style, n, tier) {
  const out = { discs: [], bands: null, peg: null, collar: null, board: null, ink: "#f4ead2", inkOpacity: 0.7, edge: null };
  for (let d = 0; d < n; d++) {
    const c = rampColor(style, n, d);
    let m;
    if (style === "metal") {
      m = new THREE.MeshPhysicalMaterial({ color: c, metalness: 1, roughness: 0.26 + 0.08 * ((d * 7) % 3) / 2,
        anisotropy: tier >= 1 ? 0.7 : 0, clearcoat: 0.35, clearcoatRoughness: 0.12 });
    } else if (style === "glass") {
      m = tier >= 2
        ? new THREE.MeshPhysicalMaterial({ color: new THREE.Color(1, 1, 1).lerp(c, 0.25), transmission: 1, thickness: 0.018, ior: 1.52,
          roughness: 0.035, attenuationColor: c, attenuationDistance: 0.045, dispersion: 2.5, specularIntensity: 1 })
        : new THREE.MeshPhysicalMaterial({ color: new THREE.Color(1, 1, 1).lerp(c, 0.55), roughness: 0.06, metalness: 0, clearcoat: 1,
          clearcoatRoughness: 0.03, iridescence: 0.7, iridescenceIOR: 1.4, iridescenceThicknessRange: [200, 480],
          transparent: true, opacity: 0.58, depthWrite: false, specularIntensity: 1 });
    } else if (style === "neon") {
      m = new THREE.MeshPhysicalMaterial({ color: "#16181f", roughness: 0.24, metalness: 0.35, clearcoat: 1, clearcoatRoughness: 0.05 });
    } else if (style === "wood") {
      m = woodMaterial(c, { ring: 46 + (d % 5) * 9, seed: 1.3 + d * 0.71, rough: 0.48, coat: 0.6 });
    } else {
      m = new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.3, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.05, sheen: 0.25,
        sheenColor: new THREE.Color(1, 1, 1), sheenRoughness: 0.5 });
    }
    out.discs.push(m);
  }
  if (style === "neon") {
    out.bands = Array.from({ length: n }, (_, d) => glowMaterial(`#${rampColor("neon", n, d).getHexString()}`, 3.2));
    out.bandBase = out.bands.map((m) => m.color.clone());
  }
  // 기둥 · 받침
  if (style === "metal") {
    out.peg = new THREE.MeshPhysicalMaterial({ color: "#d7dae0", metalness: 1, roughness: 0.12 });
    out.board = marbleMaterial("#15171c", "#c8ccd4", { rough: 0.16 });
  } else if (style === "glass") {
    out.peg = new THREE.MeshPhysicalMaterial({ color: "#aeb4bd", metalness: 1, roughness: 0.34 });
    out.board = marbleMaterial("#ece8e0", "#8f939c", { rough: 0.22, coat: 0.8, seed: 5.1 });
    out.ink = "#4a4f5a"; out.inkOpacity = 0.75;
  } else if (style === "neon") {
    out.peg = new THREE.MeshPhysicalMaterial({ color: "#2a2d36", metalness: 1, roughness: 0.12 });
    out.board = new THREE.MeshPhysicalMaterial({ color: "#0b0d12", roughness: 0.05, metalness: 0.2, clearcoat: 1, clearcoatRoughness: 0.02 });
    out.edge = glowMaterial("#3db8ff", 2.6);
    out.ink = "#8fd8ff"; out.inkOpacity = 0.9;
  } else if (style === "wood") {
    out.peg = woodMaterial("#d6b688", { plank: true, ring: 90, seed: 9.1, rough: 0.55, coat: 0.3 });
    out.board = woodMaterial("#c4975f", { plank: true, ring: 26, seed: 2.2, rough: 0.5, coat: 0.45 });
    out.ink = "#5a3a22"; out.inkOpacity = 0.72;
  } else {
    out.peg = new THREE.MeshPhysicalMaterial({ color: "#d9b26a", metalness: 1, roughness: 0.16 });
    out.board = woodMaterial("#5b3923", { plank: true, ring: 18, seed: 4.4, rough: 0.42, coat: 0.5 });
  }
  out.collar = new THREE.MeshPhysicalMaterial({ color: style === "wood" ? "#8a6a45" : "#1c1e24", metalness: style === "wood" ? 0 : 0.9, roughness: 0.3 });
  return out;
}

/** 기둥 이름(A B C …) 글자판 — 받침 앞면에 붙인다(기둥 자리에 맞춰) */
export function labelTexture(G, ink) {
  const W = 2048, H = 96;
  const cv = document.createElement("canvas");
  cv.width = W; cv.height = H;
  const g = cv.getContext("2d");
  g.clearRect(0, 0, W, H);
  g.fillStyle = ink;
  g.font = "800 66px Pretendard, 'Pretendard Variable', system-ui, sans-serif";
  g.textAlign = "center"; g.textBaseline = "middle";
  const names = ["A", "B", "C", "D", "E"];
  G.X.forEach((x, i) => g.fillText(names[i], ((x + G.W / 2) / G.W) * W, H / 2 + 3));
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

/** 부드러운 둥근 빛(바닥의 쉼 표시 · 그림자 얼룩) */
export function radialTexture(stops = [[0, 1], [0.55, 0.35], [1, 0]]) {
  const S = 128, cv = document.createElement("canvas");
  cv.width = cv.height = S;
  const g = cv.getContext("2d");
  const gr = g.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
  for (const [o, a] of stops) gr.addColorStop(o, `rgba(255,255,255,${a})`);
  g.fillStyle = gr; g.fillRect(0, 0, S, S);
  const tex = new THREE.CanvasTexture(cv);
  return tex;
}

/* ══════════ 로봇 재질 ══════════ */
export function robotMaterials() {
  const carbonTex = (() => {
    const S = 256, cv = document.createElement("canvas");
    cv.width = cv.height = S;
    const g = cv.getContext("2d");
    g.fillStyle = "#15161a"; g.fillRect(0, 0, S, S);
    const c = 16;
    for (let y = 0; y < S; y += c) for (let x = 0; x < S; x += c) {
      const k = ((x / c + y / c) % 2) === 0;
      const gr = g.createLinearGradient(x, y, k ? x + c : x, k ? y : y + c);
      gr.addColorStop(0, "#202227"); gr.addColorStop(0.5, "#34363d"); gr.addColorStop(1, "#1b1c21");
      g.fillStyle = gr; g.fillRect(x + 1, y + 1, c - 2, c - 2);
    }
    const t = new THREE.CanvasTexture(cv);
    t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 3); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
    return t;
  })();
  return {
    white: new THREE.MeshPhysicalMaterial({ color: "#f1f1ee", roughness: 0.3, clearcoat: 0.9, clearcoatRoughness: 0.12 }),
    grey: new THREE.MeshPhysicalMaterial({ color: "#8d939c", roughness: 0.35, metalness: 0.6, clearcoat: 0.3 }),
    joint: new THREE.MeshStandardMaterial({ color: "#1c1f26", roughness: 0.42, metalness: 0.65 }),
    metal: new THREE.MeshStandardMaterial({ color: "#b9c0c9", roughness: 0.2, metalness: 1 }),
    rubber: new THREE.MeshStandardMaterial({ color: "#111216", roughness: 0.85, metalness: 0 }),
    carbon: new THREE.MeshPhysicalMaterial({ color: "#ffffff", map: carbonTex, roughness: 0.32, metalness: 0.2, clearcoat: 1, clearcoatRoughness: 0.05 }),
    visor: new THREE.MeshPhysicalMaterial({ color: "#05070c", roughness: 0.04, metalness: 0.3, clearcoat: 1, clearcoatRoughness: 0.02 }),
    yellow: new THREE.MeshPhysicalMaterial({ color: "#f3c12f", roughness: 0.34, clearcoat: 0.7, clearcoatRoughness: 0.1 }),
    orange: new THREE.MeshPhysicalMaterial({ color: "#ff7417", roughness: 0.3, clearcoat: 0.8, clearcoatRoughness: 0.08 }),
    teal: new THREE.MeshPhysicalMaterial({ color: "#1fc7bd", roughness: 0.28, clearcoat: 0.8, clearcoatRoughness: 0.08 }),
    lens: new THREE.MeshPhysicalMaterial({ color: "#0a0f1a", roughness: 0.02, metalness: 0.1, clearcoat: 1, iridescence: 0.8 }),
    led: glowMaterial("#5fe6ff", 3.2),
    ledWarm: glowMaterial("#ffb347", 3),
    ledRed: glowMaterial("#ff3b3b", 3),
    ledGreen: glowMaterial("#3bff7a", 3),
    thrust: glowMaterial("#6fb8ff", 4, { transparent: true, opacity: 0.85, depthWrite: false, blending: THREE.AdditiveBlending }),
    prop: new THREE.MeshBasicMaterial({ color: "#c9d2dd", transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide }),
    cable: new THREE.MeshStandardMaterial({ color: "#2b2e35", roughness: 0.6, metalness: 0.4 }),
    tex: [carbonTex],
  };
}
