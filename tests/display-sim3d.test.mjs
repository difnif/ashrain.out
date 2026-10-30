// node tests/display-sim3d.test.mjs — 교실 모니터 「3D 축구」(sim3d) 검산. 실패 시 exit 1.
//   1) 원근 카메라(persp.js)가 three.js PerspectiveCamera 와 같은 곳에 점을 찍는지(무대 16:9 · 화면이 더 길쭉하거나 넓을 때도)
//   2) 박자표(play · hold) · 자리 잇기 · 공 · 설명 컷 맞추기(frameCam)의 성질
//   3) 여섯 장면: 길이, 처음부터 끝까지 50 ms 마다 세계(카메라 · 선수 자세 · 공)에 NaN 이 없고, 카메라가 땅속 · 경기장 밖으로 가지 않으며,
//      설명(hold) 동안 밝게 남긴 선수가 화면 안에 보이는지
//   4) 3D 글자(SVG)를 두 판 · 두 테마로 그려 오류 · NaN 이 없는지, 설명 카드에 맞는 수가 나오는지
//   5) 명단(3D 판에서 더 쓰는 넷) · 축구 액자에만 3D 판이 붙었는지 · 3D 를 켜면 이어 돌기가 3D 길이로 계산되는지
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import * as THREE from "three";
import { lookCam, project, projectPath, canvasFov, frameCam, camMix, FW, FH } from "../src/features/display/sim3d/persp.js";
import { timeline, track, ballPath, smooth, HOLD_IN, FADE_IN, FADE_OUT } from "../src/features/display/sim3d/script.js";
import { REST, JOINTS, runPose, kickPose, headerPose, divePose, mixPose } from "../src/features/display/sim3d/rig.js";
import { LINEUPS, who } from "../src/features/display/facts-soccer.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const near = (a, b, eps, msg) => assert.ok(Math.abs(a - b) <= eps, `${msg || ""} ${a} ≠ ${b} (±${eps})`);
let seed = 7;
const rnd = () => { seed ^= seed << 13; seed >>>= 0; seed ^= seed >> 17; seed ^= seed << 5; seed >>>= 0; return seed / 4294967296; };

/* ══════════ 1. 카메라 ══════════ */
/** three.js 로 같은 카메라를 만들어 캔버스 픽셀 → 무대 좌표 */
function threeProject(c, p, cw = FW, ch = FH, fh = FH) {
  const cam = new THREE.PerspectiveCamera(canvasFov(c.fov, fh, ch), cw / ch, 0.1, 5000);
  cam.position.set(...c.pos); cam.up.set(0, 1, 0); cam.lookAt(...c.at); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
  const v = new THREE.Vector3(...p).project(cam);
  // 캔버스 픽셀 → 무대(가운데 맞춤, 무대 폭 fw = fh·16/9)
  const px = ((v.x + 1) / 2) * cw, py = ((1 - v.y) / 2) * ch;
  const fw = (fh * 16) / 9, s = FH / fh;
  return [(px - (cw - fw) / 2) * s, (py - (ch - fh) / 2) * s];
}
test("원근 투영: persp.project 가 three.js PerspectiveCamera 와 같은 자리(무대 16:9)", () => {
  for (let i = 0; i < 400; i++) {
    const c = { pos: [rnd() * 100 - 50, 0.5 + rnd() * 40, rnd() * 70 - 35], at: [rnd() * 100 - 50, rnd() * 3, rnd() * 70 - 35], fov: 20 + rnd() * 40 };
    const L = lookCam(c);
    const p = [L.pos[0] + L.f[0] * 20 + (rnd() - 0.5) * 12, L.pos[1] + L.f[1] * 20 + (rnd() - 0.5) * 8, L.pos[2] + L.f[2] * 20 + (rnd() - 0.5) * 12];
    const a = project(L, p), b = threeProject(c, p);
    assert.ok(a, "카메라 앞인데 null");
    near(a[0], b[0], 0.05, "x"); near(a[1], b[1], 0.05, "y");
  }
});
test("원근 투영: 캔버스가 화면 전체(무대보다 길쭉 · 넓음)일 때 canvasFov 로 무대 부분이 똑같다", () => {
  for (const [cw, ch, fh] of [[1600, 1200, 900], [1920, 1200, 1080], [2400, 900, 900], [1366, 1024, 768.375]]) {
    for (let i = 0; i < 60; i++) {
      const c = { pos: [rnd() * 60 - 30, 1 + rnd() * 20, rnd() * 50 - 25], at: [rnd() * 60 - 30, rnd() * 2, rnd() * 50 - 25], fov: 25 + rnd() * 30 };
      const L = lookCam(c);
      const p = [L.pos[0] + L.f[0] * 15 + (rnd() - 0.5) * 6, L.pos[1] + L.f[1] * 15 + (rnd() - 0.5) * 4, L.pos[2] + L.f[2] * 15 + (rnd() - 0.5) * 6];
      const a = project(L, p), b = threeProject(c, p, cw, ch, fh);
      near(a[0], b[0], 0.05, `${cw}×${ch} x`); near(a[1], b[1], 0.05, `${cw}×${ch} y`);
    }
  }
});
test("카메라 뒤 점은 null, 꺾은선은 가까운 면에서 잘린다", () => {
  const L = lookCam({ pos: [0, 2, 0], at: [10, 2, 0], fov: 40 });
  assert.equal(project(L, [-5, 2, 0]), null);
  const S = projectPath(L, [[-5, 0, 0], [20, 0, 0]]);
  assert.ok(S.length >= 2 && S.every((p) => Number.isFinite(p[0]) && Number.isFinite(p[1])));
  const m = camMix({ pos: [0, 0, 0], at: [1, 0, 0], fov: 30 }, { pos: [2, 2, 2], at: [3, 0, 0], fov: 50 }, 0.5);
  assert.deepEqual(m, { pos: [1, 1, 1], at: [2, 0, 0], fov: 40 });
});
test("frameCam: 점들이 화면 상자 안에 꽉 차게(가로나 세로 한쪽은 상자에 맞닿는다)", () => {
  for (let i = 0; i < 40; i++) {
    const pts = Array.from({ length: 3 + Math.floor(rnd() * 4) }, () => [rnd() * 80 - 40, rnd() * 50 - 25]);
    const box = [860 + rnd() * 60, 180 + rnd() * 40, 1440 + rnd() * 60, 700 + rnd() * 40];
    const c = frameCam(pts, { yaw: rnd() * 360 - 180, pitch: 50 + rnd() * 25, fov: 30 + rnd() * 8, box });
    const L = lookCam(c);
    const S = pts.map((p) => project(L, [p[0], 0, p[1]]));
    assert.ok(S.every(Boolean));
    const xs = S.map((s) => s[0]), ys = S.map((s) => s[1]);
    const tol = 6;
    assert.ok(Math.min(...xs) >= box[0] - tol && Math.max(...xs) <= box[2] + tol && Math.min(...ys) >= box[1] - tol && Math.max(...ys) <= box[3] + tol, `상자 밖 ${xs} ${ys}`);
    const fillX = (Math.max(...xs) - Math.min(...xs)) / (box[2] - box[0]), fillY = (Math.max(...ys) - Math.min(...ys)) / (box[3] - box[1]);
    assert.ok(Math.max(fillX, fillY) > 0.93, `덜 참 ${fillX.toFixed(2)} ${fillY.toFixed(2)}`);
  }
});

/* ══════════ 2. 박자표 · 자리 · 공 · 자세 ══════════ */
test("박자표: play 는 세계가 흐르고 hold 는 멈춘다 · 어둡기 0~1 · 처음과 끝은 검다 · tAt 은 거꾸로 찾기", () => {
  const TL = timeline([
    { name: "a", kind: "play", tw: [-1000, 2000], dur: 3000 },
    { name: "b", kind: "play", tw: [2000, 4000], dur: 2600, speed: "into" },
    { name: "h", kind: "hold", dur: 5000 },
    { name: "c", kind: "play", tw: [4000, 6000], dur: 2400, speed: "both" },
    { name: "h2", kind: "hold", dur: 3000 },
    { name: "h3", kind: "hold", dur: 3000 },
  ]);
  assert.equal(TL.dur, 3000 + 2600 + 5000 + 2400 + 3000 + 3000);
  let prev = -Infinity;
  for (let t = 0; t <= TL.a.h; t += 10) { const w = TL.at(t).tw; assert.ok(w >= prev - 1e-9, `되감김 t=${t}`); prev = w; }
  near(TL.at(TL.a.h - 1).tw, 4000, 2); near(TL.at(TL.a.h + 2500).tw, 4000, 1e-9);
  near(TL.at(TL.b.c - 0.5).tw, 6000, 2);
  for (let t = 0; t <= TL.dur; t += 25) { const d = TL.dimAt(t); assert.ok(d >= 0 && d <= 1); }
  near(TL.dimAt(0), 1, 1e-9); near(TL.dimAt(TL.dur), 1, 1e-9); near(TL.dimAt(FADE_IN + 10), 0, 1e-9);
  near(TL.dimAt(TL.a.h + 2500), 0.62, 1e-9);
  near(TL.edgeAt(TL.dur - FADE_OUT / 2), smooth(TL.dur - FADE_OUT, TL.dur, TL.dur - FADE_OUT / 2), 1e-9);
  // hold 다음 hold — 사이에서 밝아지지 않는다
  for (let t = TL.b.h2 - 300; t < TL.b.h2 + 300; t += 20) near(TL.dimAt(t), 0.62, 1e-9, `t=${t}`);
  // 들어갈 때만 어두워진다
  assert.ok(TL.dimAt(TL.a.h + HOLD_IN / 3) < 0.62);
  for (const w of [2100, 2900, 3700, 3990]) near(TL.at(TL.tAt("b", w)).tw, w, 1.5, `tAt ${w}`);
});
test("자리 잇기: 열쇠 자리를 지나고 넘치지 않으며, 간 거리는 줄지 않는다 · 같은 자리면 서 있다", () => {
  const T = track([[0, 0, 0], [1000, 10, 0], [2000, 10, 10], [2600, 10, 10], [4000, 0, 0]]);
  near(T.at(1000)[0], 10, 1e-9); near(T.at(2000)[1], 10, 1e-9); near(T.at(-500)[0], 0, 1e-9);
  for (let t = 0; t <= 2000; t += 20) assert.ok(T.at(t)[0] <= 10 + 1e-9, "넘침");
  near(Math.hypot(...T.vel(2300)), 0, 1e-9);
  let d0 = -1;
  for (let t = -200; t <= 4200; t += 30) { const d = T.dist(t); assert.ok(d >= d0 - 1e-9); d0 = d; }
  near(T.dist(4200), 10 + 10 + Math.hypot(10, 10), 0.6);
});
test("공: 날기 · 굴러가기 · 휘기 · 그물 — 끝자리가 맞고 땅 아래로 가지 않는다", () => {
  const B = ballPath([
    { t0: 0, t1: 1000, kind: "air", a: [0, 0.2, 0], b: [20, 2, 5], h: 5, bend: 2 },
    { t0: 1200, t1: 2000, kind: "ground", a: [20, 5], b: [30, 5], ease: "slow" },
    { t0: 2000, t1: 2300, kind: "air", a: [30, 0.2, 5], b: [31, 0.2, 5], ease: "fall" },
  ]);
  assert.deepEqual(B.at(1000).map((v) => +v.toFixed(9)), [20, 2, 5]);
  near(B.at(1100)[0], 20, 1e-9);                                  // 구간 사이에는 앞 구간 끝에 머문다
  near(B.at(2000)[0], 30, 1e-9);
  for (let t = -100; t <= 2400; t += 10) { const p = B.at(t); assert.ok(p.every(Number.isFinite) && p[1] >= 0.19, `t=${t} ${p}`); }
  assert.ok(B.at(500)[1] > 5, "포물선 꼭대기");
  assert.ok(B.spin(2300) > B.spin(1000) && B.spin(1000) > 0);
});
test("자세: 모든 관절 값이 수이고, 섞기 끝값이 그대로", () => {
  const poses = [REST, runPose(1.3, 0.9), kickPose(-0.5), kickPose(0.3, 0.6, "L"), headerPose(0.5), divePose(0.7, -1), mixPose(REST, runPose(2, 1), 0.4)];
  for (const p of poses) for (const k of JOINTS) assert.ok(Number.isFinite(p[k] ?? REST[k]), k);
  const a = runPose(0.4, 0.7), b = kickPose(0.2);
  for (const k of JOINTS) { near(mixPose(a, b, 0)[k] ?? a[k], a[k], 1e-12); near(mixPose(a, b, 1)[k] ?? b[k], b[k], 1e-12); }
  near(headerPose(0.5, 0.7).y, 0.7, 1e-9);
});

/* ══════════ 명단 ══════════ */
test("명단(3D 판에서 더 쓰는 넷): 11명 · 등번호 · 이름 겹침 없음, 확인한 선수", () => {
  for (const k of ["derby2012City", "final2021Chelsea", "semi2009Arsenal", "semi2009United"]) {
    const L = LINEUPS[k];
    assert.equal(L.length, 11, k);
    assert.equal(new Set(L.map((x) => x[0])).size, 11, k + " 번호");
    assert.equal(new Set(L.map((x) => x[1])).size, 11, k + " 이름");
  }
  assert.deepEqual(who("derby2012City", "콤파니"), [4, "콤파니"]); assert.deepEqual(who("derby2012City", "실바"), [21, "실바"]);
  assert.deepEqual(who("final2021Chelsea", "크리스텐센"), [4, "크리스텐센"]);   // 39분에 티아구 실바와 교체 — 42분 골 때 경기장에
  assert.throws(() => who("final2021Chelsea", "티아구 실바"));
  assert.deepEqual(who("semi2009United", "박지성"), [13, "박지성"]); assert.deepEqual(who("semi2009United", "호날두"), [7, "호날두"]);
  assert.deepEqual(who("semi2009Arsenal", "알무니아"), [1, "알무니아"]);
});

/* ══════════ 3 · 4 · 5. 여섯 장면 ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-sim3d-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { SIM3D } from ${JSON.stringify(path.join(ROOT, "src/features/display/sim3d/index.js"))};
import { STORIES, EXPLAIN } from ${JSON.stringify(path.join(ROOT, "src/features/display/stories.js"))};
import { loadStory, durFor } from ${JSON.stringify(path.join(ROOT, "src/features/display/frames/player.jsx"))};
import { PALETTE } from ${JSON.stringify(path.join(ROOT, "src/features/display/draw.jsx"))};
import { Title3D } from ${JSON.stringify(path.join(ROOT, "src/features/display/sim3d/overlay.jsx"))};
export { SIM3D, STORIES, EXPLAIN, loadStory, durFor };
export const svg = (sc, pair, mode, t, th) => { const W = sc.world(t); return renderToStaticMarkup(<g opacity={1 - (W.edge || 0)}>{sc.overlay(mode, t, PALETTE[th], {}, W)}<Title3D title={pair.title[mode]} sub={pair.sub[mode]} mode={mode} o={1} /></g>); };
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const soccer = m.STORIES.soccer.scenes;

  test("3D 판: 축구 여섯 장면에 하나씩(키가 같다) · 서술형 · 실험 풀이에는 없음 · 길이 40~65초", () => {
    assert.equal(Object.keys(m.SIM3D).length, 6);
    for (const p of soccer) {
      assert.ok(p.sim3d && p.sim3d === m.SIM3D[p.key], p.key);
      assert.equal(p.sim3d.key, p.key);
      assert.ok(p.sim3d.dur >= 40000 && p.sim3d.dur <= 65000, `${p.key} ${p.sim3d.dur}`);
      assert.equal(typeof p.render, "function");            // 2D 판은 그대로
    }
    assert.ok(m.STORIES.essay.scenes.every((p) => !p.sim3d));
    assert.ok(Object.values(m.EXPLAIN).flat().every((p) => !p.sim3d));
  });
  test("이어 돌기: 3D 를 켜면 3D 길이로 · 끄면 2D 길이로 계산", () => {
    const L = soccer, now = 10_000_000_000;
    const d2 = L.map((p) => m.durFor(p, {}, false)), d3 = L.map((p) => m.durFor(p, {}, true));
    assert.ok(d2.every((d, i) => d === L[i].dur) && d3.every((d, i) => d === L[i].sim3d.dur));
    const s3 = m.loadStory(L, now, { i: 0, t0: now - (d3[0] + 700) }, null, true);
    assert.deepEqual([s3.i, now - s3.t0], [1, 700]);
    const s2 = m.loadStory(L, now, { i: 0, t0: now - (d2[0] + 700) }, null, false);
    assert.deepEqual([s2.i, now - s2.t0], [1, 700]);
  });

  for (const p of soccer) {
    const sc = p.sim3d;
    test(`세계 훑기: ${p.key} (${(sc.dur / 1000).toFixed(1)}초) — 50 ms 마다 NaN 없음 · 카메라는 땅 위 · 경기장 안 · 설명 때 밝은 선수가 보인다`, () => {
      const ids = new Set(sc.world(0).actors.map((a) => a.id));
      for (const s of sc.tl.segs) for (const id of s.spot || []) assert.ok(id === "ball" || ids.has(id), `${s.name} 의 spot ${id}`);
      for (let t = 0; t <= sc.dur; t += 50) {
        const W = sc.world(t);
        const c = W.cam;
        assert.ok([...c.pos, ...c.at, c.fov].every(Number.isFinite), `t=${t} 카메라`);
        if (W.seg.kind === "play") {
          // 경기가 흐를 때는 눈높이(관중석 앞줄까지) — 경기장 · 관중석 앞쪽 안
          assert.ok(c.pos[1] > 0.5 && c.pos[1] < 12, `t=${t} 카메라 높이 ${c.pos[1]}`);
          assert.ok(Math.abs(c.pos[0]) < 62 && Math.abs(c.pos[2]) < 52, `t=${t} 카메라 자리 ${c.pos}`);
        } else {
          // 설명(멈춤)은 위에서 내려다본다 — 지붕은 엔진이 감춘다
          assert.ok(c.pos[1] > 0.5 && c.pos[1] < 170 && Math.hypot(c.pos[0], c.pos[2]) < 160, `t=${t} 설명 카메라 ${c.pos}`);
        }
        assert.ok(c.fov >= 15 && c.fov <= 70, `t=${t} 시야각 ${c.fov}`);
        assert.ok(W.dim >= 0 && W.dim <= 1 && W.edge >= 0 && W.edge <= 1);
        for (const a of W.actors) {
          assert.ok(Number.isFinite(a.x) && Number.isFinite(a.z) && Number.isFinite(a.yaw), `t=${t} ${a.id}`);
          for (const k of Object.keys(a.pose)) assert.ok(Number.isFinite(a.pose[k]), `t=${t} ${a.id}.${k}`);
          assert.ok(Math.abs(a.x) < 60 && Math.abs(a.z) < 40, `t=${t} ${a.id} 경기장 밖 ${a.x},${a.z}`);
        }
        assert.ok(W.ball.p.every(Number.isFinite) && W.ball.p[1] >= 0.15, `t=${t} 공 ${W.ball.p}`);
        if (W.seg.kind === "hold" && W.local > 1600 && W.local < W.seg.dur - 1700) {
          for (const a of W.actors) if (a.hi) {
            const s = project(W.cam, [a.x, 1, a.z]);
            assert.ok(s && s[0] > 20 && s[0] < FW - 20 && s[1] > 20 && s[1] < FH - 20, `t=${t} 밝힌 ${a.id} 화면 밖 ${s}`);
          }
        }
      }
    });
    test(`3D 글자 훑기: ${p.key} — 두 판 · 두 테마, 오류 · NaN 없음`, () => {
      for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
        for (let t = 0; t <= sc.dur; t += th === "dark" ? 200 : 700) {
          const s = m.svg(sc, p, mode, t, th);
          assert.ok(!/NaN|undefined|Infinity|\[object Object\]/.test(s), `${mode}/${th} t=${t}: ${(s.match(/.{40}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0]}`);
        }
      }
    });
  }

  /** 설명 카드가 다 나온 순간(구간 끝에서 2초 전)의 글자 — 수식 글자는 조각나 그려지니 이어 붙여 본다 */
  const textAt = (p, mode, name) => {
    const s = p.sim3d.tl.seg(name);
    const svg = m.svg(p.sim3d, p, mode, s.t1 - 2000, "dark");
    return (svg.match(/<text[^>]*>([^<]*)<\/text>/g) || []).map((x) => x.replace(/<[^>]+>/g, "")).join("").replace(/\s+/g, " ");
  };
  const has = (s, frag) => assert.ok(s.includes(frag), `"${frag}" 없음: …${s.slice(0, 260)}…`);
  const P = Object.fromEntries(soccer.map((p) => [p.key, p]));
  test("설명 카드의 수: 코너킥 — 초등 24 m · 7.5 m · 38.5 m, 중등 676 − 100 = 576 · 12.5", () => {
    has(textAt(P["soc-corner"], "e", "ex1"), "24 m"); has(textAt(P["soc-corner"], "e", "ex2"), "7.5 m"); has(textAt(P["soc-corner"], "e", "wrap"), "38.5 m");
    has(textAt(P["soc-corner"], "m", "ex1"), "676 − 100 = 576"); has(textAt(P["soc-corner"], "m", "ex2"), "12.5");
    has(textAt(P["soc-corner"], "m", "wrap"), "5 : 12 : 13");
  });
  test("설명 카드의 수: 프리킥 — 25 m · 10 m · 150번 중 60번 · 4번 / 20² + 15² · 1/25", () => {
    has(textAt(P["soc-setpiece"], "e", "ex1"), "25 m"); has(textAt(P["soc-setpiece"], "e", "ex2"), "150번 중 60번"); has(textAt(P["soc-setpiece"], "e", "wrap"), "4번");
    has(textAt(P["soc-setpiece"], "m", "ex1"), "20² + 15² = 625"); has(textAt(P["soc-setpiece"], "m", "wrap"), "25");
  });
  test("설명 카드의 수: 쓰루패스 — 25 ÷ 12.5 · 0.5초 / M(24, 7) · 0.5초", () => {
    has(textAt(P["soc-through"], "e", "ex2"), "25 ÷ 12.5"); has(textAt(P["soc-through"], "e", "ex2"), "0.5초");
    has(textAt(P["soc-through"], "m", "ex1"), "M(24, 7)"); has(textAt(P["soc-through"], "m", "ex2"), "0.5초");
  });
  test("설명 카드의 수: 삼각패스 — 25 m · 12 m · 150 m² / B(12, 14) · 150 m²", () => {
    has(textAt(P["soc-triangle"], "e", "ex1"), "25 m"); has(textAt(P["soc-triangle"], "e", "ex2"), "150 m²");
    has(textAt(P["soc-triangle"], "m", "ex1"), "B(12, 14)"); has(textAt(P["soc-triangle"], "m", "ex2"), "150 m²");
  });
  test("설명 카드의 수: 역습 — 85 − 65 = 20 m · 2118 m² / 60² · 2118 m²", () => {
    has(textAt(P["soc-counter"], "e", "ex1"), "85 − 65 = 20 m"); has(textAt(P["soc-counter"], "e", "ex2"), "2118 m²");
    has(textAt(P["soc-counter"], "m", "ex1"), "60²"); has(textAt(P["soc-counter"], "m", "ex2"), "2118 m²");
  });
  test("설명 카드의 수: xG — 5 · 10 · 20 m · 296경기 · 37 / 37 (100분의)", () => {
    const e1 = textAt(P["soc-xg"], "e", "ex1"); has(e1, "5 m"); has(e1, "10 m"); has(e1, "20 m");
    const e3 = textAt(P["soc-xg"], "e", "ex3"); has(e3, "296경기"); has(e3, "37");
    has(textAt(P["soc-xg"], "m", "ex3"), "37100");                          // {37/100} — 분자 · 분모가 이어 붙는다
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
