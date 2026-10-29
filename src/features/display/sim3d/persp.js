// ashrain.out — 교실 모니터 「3D 축구」: 원근 카메라 계산 (sim3d/persp.js)
// 순수 계산 — three.js 를 쓰지 않는다. 같은 카메라로 WebGL 그림(engine.js)과 SVG 글자(overlay.jsx)를 맞춘다.
//   세계 좌표(m): X = 경기장 길이 방향(오른쪽 골대 +52.5) · Y = 위 · Z = 너비 방향(+X 를 볼 때 오른쪽이 +Z).
//   경기장 가운데 점이 원점. 화면은 1600×900 무대(SVG 와 같은 좌표).
//   three.js PerspectiveCamera(fov 세로각, lookAt, up = +Y)와 같은 투영이다(tests/display-sim3d.test.mjs 가 맞춰 본다).
import { clamp, lerp, rad } from "../core.js";

export const FW = 1600, FH = 900;
export const NEAR = 0.25;

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const unit = (a) => { const L = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / L, a[1] / L, a[2] / L]; };

/**
 * 카메라: pos(눈) · at(보는 곳) · fov(세로 시야각, 도). 위쪽은 늘 +Y.
 * 반환 { pos, at, fov, f(앞) · r(오른쪽) · u(위) 단위벡터, F(초점 거리, 무대 px) }
 */
export function lookCam({ pos, at, fov = 40 }) {
  const f = unit(sub(at, pos));
  let r = cross(f, [0, 1, 0]);
  if (Math.hypot(r[0], r[1], r[2]) < 1e-6) r = [1, 0, 0];      // 바로 아래·위를 볼 때
  r = unit(r);
  const u = cross(r, f);
  const F = FH / 2 / Math.tan(rad(fov) / 2);
  return { pos, at, fov, f, r, u, F };
}

/** 세계 점 → [무대 x, 무대 y, 깊이(m)]. 카메라 뒤(깊이 < NEAR)면 null */
export function project(cam, p) {
  const d = sub(p, cam.pos);
  const z = dot(d, cam.f);
  if (z < NEAR) return null;
  return [FW / 2 + (dot(d, cam.r) / z) * cam.F, FH / 2 - (dot(d, cam.u) / z) * cam.F, z];
}

/** 깊이 z 에서 길이 m(미터)가 화면에서 몇 px 인가 */
export const pxAt = (cam, z, m = 1) => (m * cam.F) / z;

/** 꺾은선(세계) → 화면 꺾은선. 카메라 뒤로 넘어가는 부분은 가까운 면에서 자른다(앞부분만 남김) */
export function projectPath(cam, pts) {
  const out = [];
  const depth = (p) => dot(sub(p, cam.pos), cam.f);
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i], zp = depth(p);
    if (i > 0) {
      const q = pts[i - 1], zq = depth(q);
      if ((zq < NEAR) !== (zp < NEAR)) {                       // 가까운 면을 가로지른다 — 만나는 점을 더한다
        const k = (NEAR - zq) / (zp - zq);
        const m = [lerp(q[0], p[0], k), lerp(q[1], p[1], k), lerp(q[2], p[2], k)];
        const s = project(cam, [m[0] + cam.f[0] * 1e-6, m[1] + cam.f[1] * 1e-6, m[2] + cam.f[2] * 1e-6]);
        if (s) out.push([s[0], s[1]]);
      }
    }
    if (zp >= NEAR) { const s = project(cam, p); out.push([s[0], s[1]]); }
  }
  return out;
}

/**
 * 캔버스가 16:9 무대보다 크게(전체 화면) 깔릴 때의 세로 시야각.
 * 무대 높이 frameH(px)가 캔버스 높이 canvasH(px) 가운데에 있으면, 캔버스 시야각을 키워 무대 부분이 fov 와 같게 보이게 한다.
 */
export function canvasFov(fov, frameH, canvasH) {
  const k = canvasH / Math.max(1, frameH);
  return (2 * Math.atan(Math.tan(rad(fov) / 2) * k) * 180) / Math.PI;
}

/** 두 카메라 사이(k = 0 → a, 1 → b). 보는 곳·눈·시야각을 따로 섞는다 */
export function camMix(a, b, k) {
  if (k <= 0) return a;
  if (k >= 1) return b;
  const m3 = (p, q) => [lerp(p[0], q[0], k), lerp(p[1], q[1], k), lerp(p[2], q[2], k)];
  return { pos: m3(a.pos, b.pos), at: m3(a.at, b.at), fov: lerp(a.fov ?? 40, b.fov ?? 40, k) };
}

/** 눈 위치를 「보는 곳에서 방위각 yaw · 올려본 각 pitch · 거리 dist」로 — yaw 0 = 보는 곳의 −X 쪽(+X 를 바라봄), 90 = −Z 쪽 */
export function orbit(at, yaw, pitch, dist, fov = 40) {
  const cy = Math.cos(rad(yaw)), sy = Math.sin(rad(yaw)), cp = Math.cos(rad(pitch)), sp = Math.sin(rad(pitch));
  return { pos: [at[0] - dist * cp * cy, at[1] + dist * sp, at[2] - dist * cp * sy], at, fov };
}

/** 화면 안인가(여유 pad px) */
export const onStage = (s, pad = 0) => !!s && s[0] > -pad && s[0] < FW + pad && s[1] > -pad && s[1] < FH + pad;

export { clamp };

/**
 * 설명 컷 맞추기: 세계 점들(pts)이 화면 상자 box = [x0, y0, x1, y1] 안에 꽉 차게 들어오는 카메라.
 * 보는 방향은 yaw(도, 0 = +X 를 바라봄 · 90 = +Z 를 바라봄) · pitch(내려다보는 각, 도)로 정하고, 거리와 옆 자리만 맞춘다.
 * 반환 { pos, at, fov } — 장면 대본이 모듈을 불러올 때 한 번 계산해 둔다.
 */
export function frameCam(pts, { yaw = 0, pitch = 45, fov = 38, box = [820, 170, 1520, 760], fill = 1 } = {}) {
  const P3 = pts.map((p) => (p.length === 3 ? p : [p[0], 0, p[1]]));
  const c = P3.reduce((s, p) => [s[0] + p[0] / P3.length, s[1] + p[1] / P3.length, s[2] + p[2] / P3.length], [0, 0, 0]);
  const cy = Math.cos(rad(yaw)), sy = Math.sin(rad(yaw)), cp = Math.cos(rad(pitch)), sp = Math.sin(rad(pitch));
  const dir = [cp * cy, -sp, cp * sy];                       // 보는 방향(단위)
  const bw = (box[2] - box[0]) * fill, bh = (box[3] - box[1]) * fill, bcx = (box[0] + box[2]) / 2, bcy = (box[1] + box[3]) / 2;
  let at = c, d = 60;
  for (let it = 0; it < 40; it++) {
    const pos = [at[0] - dir[0] * d, at[1] - dir[1] * d, at[2] - dir[2] * d];
    const cam = lookCam({ pos, at, fov });
    const S = P3.map((p) => project(cam, p)).filter(Boolean);
    if (S.length < P3.length) { d *= 1.4; continue; }
    const xs = S.map((s) => s[0]), ys = S.map((s) => s[1]);
    const w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys);
    const mx = (Math.max(...xs) + Math.min(...xs)) / 2, my = (Math.max(...ys) + Math.min(...ys)) / 2;
    const k = Math.max(w / bw, h / bh, 1e-3);
    // 화면에서 어긋난 만큼 카메라를 옆 · 위로 옮긴다(보는 곳도 같이)
    const zc = d;
    const ox = ((mx - bcx) * zc) / cam.F, oy = ((my - bcy) * zc) / cam.F;
    at = [at[0] + cam.r[0] * ox - cam.u[0] * oy, at[1] + cam.r[1] * ox - cam.u[1] * oy, at[2] + cam.r[2] * ox - cam.u[2] * oy];
    d = clamp(d * (0.35 + 0.65 * k), 4, 600);
  }
  return { pos: [at[0] - dir[0] * d, at[1] - dir[1] * d, at[2] - dir[2] * d], at, fov };
}
