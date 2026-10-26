// ashrain.out — 교실 모니터 장면의 수치 (facts.js)
// 화면에 나오는 수는 모두 여기서 계산해 장면으로 넘긴다. tests/display.test.mjs 가 하나하나 다시 검산한다.
import { fmt, rng } from "./core.js";

/* ── 1. 쌓기나무 ↔ 최단 경로 ── */
export const BLOCKS = (() => {
  const COLS = 4, ROWS = 3;
  // HT[y][x] — y=0 앞줄, y=2 뒷줄 (쌓은 높이)
  const HT = [[1, 1, 1, 0], [2, 2, 1, 1], [3, 2, 2, 1]];
  const LAYERS = [1, 2, 3].map((k) => HT.flat().filter((h) => h >= k).length);
  const ROW_SUM = HT.map((r) => r.reduce((a, b) => a + b, 0));
  const TOTAL = HT.flat().reduce((a, b) => a + b, 0);
  const PASCAL = [];
  for (let y = 0; y <= ROWS; y++) {
    PASCAL.push([]);
    for (let x = 0; x <= COLS; x++) PASCAL[y].push(x === 0 || y === 0 ? 1 : PASCAL[y - 1][x] + PASCAL[y][x - 1]);
  }
  const PATHS = ["RRRRUUU", "UUURRRR", "RURURUR", "RRUURUR"];
  return { COLS, ROWS, HT, LAYERS, ROW_SUM, TOTAL, PASCAL, PATHS };
})();

export { fmt };

/** π 의 계수 표기: 1 → "π", 10 → "10π" */
export const piK = (k) => (k === 1 ? "π" : `${fmt(k)}π`);

/* ── 2. 원주·원의 넓이 ↔ 부채꼴 ── */
export const CIRCLE = (() => {
  const R_CM = 5, ANG = 72, D = 2 * R_CM;
  const circE = D * 3.14, areaE = R_CM * R_CM * 3.14;
  const circK = 2 * R_CM, arcK = (2 * R_CM * ANG) / 360, secK = (R_CM * R_CM * ANG) / 360, halfRL = (R_CM * arcK) / 2;
  return {
    R_CM, ANG, D, circE, areaE, circK, arcK, secK, halfRL,
    E_TXT: {
      circ: fmt(circE),
      circLine: `= ${D} × 3.14 = ‹${fmt(circE)}›(cm)`,
      areaLine: `= ${R_CM} × ${R_CM} × 3.14 = ‹${fmt(areaE)}›(cm²)`,
    },
    M_TXT: {
      circ: piK(circK),
      arcLine1: `*l* = 2π × ${R_CM} × {${ANG}/360}`,
      arcLine2: `= ‹${piK(arcK)}›(cm)`,
      perLine: `둘레 = *l* + 2*r* = ‹${piK(arcK)} + ${2 * R_CM}›(cm)`,
      per: `${piK(arcK)} + ${2 * R_CM}`,
      areaLine1: `*S* = π × ${R_CM}² × {${ANG}/360} = ‹${piK(secK)}›(cm²)`,
      areaLine2: `= {1/2} × ${R_CM} × ${piK(arcK)} = ‹${piK(halfRL)}›(cm²)`,
    },
  };
})();

/* ── 3. 색칠한 부분(은행잎) — 3.14 ↔ π ── */
export const LEAF = (() => {
  const SIDE = 10;
  const quarterE = (SIDE * SIDE * 3.14) / 4, tri = (SIDE * SIDE) / 2, halfE = quarterE - tri;
  const areaE = halfE * 2, arcE = (SIDE * 2 * 3.14) / 4, perE = arcE * 2;
  const qK = (SIDE * SIDE) / 4, arcK = (2 * SIDE) / 4;
  return {
    SIDE, quarterE, tri, halfE, areaE, arcE, perE, qK, arcK,
    E: {
      quarter: fmt(quarterE), tri: fmt(tri), halfLeaf: fmt(halfE), arc: `${fmt(arcE)} cm`,
      qLine: `${SIDE} × ${SIDE} × 3.14 ÷ 4 = ${fmt(quarterE)}`,
      tLine: `${SIDE} × ${SIDE} ÷ 2 = ${fmt(tri)}`,
      areaLine1: `(${fmt(quarterE)} − ${fmt(tri)}) × 2`,
      areaLine2: `= ‹${fmt(areaE)}›(cm²)`,
      arcLine: `${SIDE} × 2 × 3.14 ÷ 4 = ${fmt(arcE)}`,
      perLine: `${fmt(arcE)} × 2 = ‹${fmt(perE)}›(cm)`,
      area: fmt(areaE), per: fmt(perE),
    },
    M: {
      quarter: piK(qK), tri: fmt(tri), halfLeaf: `${piK(qK)} − ${fmt(tri)}`, arc: `${piK(arcK)} cm`,
      qLine: `π × ${SIDE}² × {1/4} = ${piK(qK)}`,
      tLine: `{1/2} × ${SIDE} × ${SIDE} = ${fmt(tri)}`,
      areaLine1: `(${piK(qK)} − ${fmt(tri)}) × 2`,
      areaLine2: `= ‹${piK(2 * qK)} − ${fmt(2 * tri)}›(cm²)`,
      arcLine: `2π × ${SIDE} × {1/4} = ${piK(arcK)}`,
      perLine: `${piK(arcK)} × 2 = ‹${piK(2 * arcK)}›(cm)`,
      area: `(${piK(2 * qK)} − ${fmt(2 * tri)})`, per: piK(2 * arcK),
    },
  };
})();

/* ── 4. 전개도 ↔ 공간에서의 위치 관계 ── */
// 모서리 이름은 글자 순서와 무관(같은 두 꼭짓점이면 같은 모서리). solids.js 의 꼭짓점 좌표로 테스트가 검산한다.
export const sameEdge = (a, b) => a.length === 2 && b.length === 2 && [...a].sort().join("") === [...b].sort().join("");
export const NETS = {
  cuboid: {
    pairsE: ["AE", "BC"],
    relM: [
      { cat: "meet", list: ["AD", "AE", "BC", "BF"] },
      { cat: "parallel", list: ["DC", "EF", "HG"] },
      { cat: "skew", list: ["CG", "DH", "EH", "FG"] },
    ],
    count: { V: 8, E: 12, F: 6 },
    E: {
      board: [{ s: "직육면체", k: "h" }, { s: "면 :  6개" }, { s: "모서리 :  12개" }, { s: "꼭짓점 :  8개" }],
      cap: ["직육면체를 펼치면?", "같은 색 모서리끼리 만나요", "다시 접으면 직육면체", "면 6개 · 모서리 12개 · 꼭짓점 8개"],
    },
    M: {
      board: [{ s: "모서리 AB와", k: "h" }, { s: "만난다 :  AD, AE, BC, BF", dot: "coral" },
        { s: "평행하다 :  DC, EF, HG", dot: "sky" }, { s: "꼬인 위치 :  CG, DH, EH, FG", dot: "leaf" }],
      cap: ["직육면체 ABCD-EFGH", "모서리 AB는 전개도에서 두 곳에 있어요", "접으면 하나로 만나요", "공간의 두 직선: 만나거나, 평행하거나, 꼬인 위치"],
    },
  },
  cube: {
    pairsE: ["AE", "BC"],
    faceName: { top: "ABCD", bottom: "EFGH", front: "ABFE", back: "DCGH", left: "AEHD", right: "BFGC" },
    planesM: [
      { cat: "contain", list: ["ABCD", "ABFE"] },
      { cat: "parallel", list: ["EFGH", "DCGH"] },
      { cat: "perp", list: ["AEHD", "BFGC"] },
    ],
    count: { V: 8, E: 12, F: 6 },
    nets: 11,
    E: {
      board: [{ s: "정육면체", k: "h" }, { s: "면 :  정사각형 6개" }, { s: "모서리 :  12개" }, { s: "전개도 :  11가지" }],
      cap: ["정육면체는 다르게 펼쳐 볼까요?", "같은 색 모서리끼리 만나요", "모서리의 길이가 모두 같은 정육면체", "정육면체의 전개도는 모두 11가지예요"],
    },
    M: {
      board: [{ s: "직선 AB와 면", k: "h" }, { s: "포함한다 :  ABCD, ABFE", dot: "coral" },
        { s: "평행하다 :  EFGH, DCGH", dot: "sky" }, { s: "수직이다 :  AEHD, BFGC", dot: "leaf" }],
      cap: ["정육면체 ABCD-EFGH", "모서리 AB의 두 자리", "접으면 하나로 만나요", "직선과 평면: 포함 · 평행 · 한 점에서 만남(수직)"],
    },
  },
  prism: {
    pairsE: ["AD", "AB"],
    relM: [
      { cat: "meet", list: ["AC", "BC", "AD", "BE"] },
      { cat: "parallel", list: ["DE"] },
      { cat: "skew", list: ["CF", "DF", "EF"] },
    ],
    count: { V: 6, E: 9, F: 5 },
    E: {
      board: [{ s: "삼각기둥", k: "h" }, { s: "밑면 2개 · 옆면 3개" }, { s: "모서리 :  9개" }, { s: "꼭짓점 :  6개" }],
      cap: ["삼각기둥을 펼치면?", "직사각형 3개와 삼각형 2개", "다시 접으면 삼각기둥", "밑면 2개 · 옆면 3개 · 모서리 9개 · 꼭짓점 6개"],
    },
    M: {
      board: [{ s: "모서리 AB와", k: "h" }, { s: "만난다 :  AC, BC, AD, BE", dot: "coral" },
        { s: "평행하다 :  DE", dot: "sky" }, { s: "꼬인 위치 :  CF, DF, EF", dot: "leaf" }],
      cap: ["삼각기둥 ABC-DEF", "모서리 AB의 두 자리", "접으면 하나로 만나요", "꼬인 위치: 만나지도 않고 평행하지도 않아요"],
    },
  },
};

/* ── 5. 원기둥 — 3.14 ↔ π ── */
export const CYL = (() => {
  const R = 3, H = 8;
  const sideE = 2 * R * 3.14, sideAreaE = sideE * H, sidePerE = (sideE + H) * 2, baseE = R * R * 3.14, netE = baseE * 2 + sideAreaE;
  const sideK = 2 * R, sideAreaK = sideK * H, baseK = R * R, surfK = baseK * 2 + sideAreaK, volK = baseK * H;
  const d = [0, 600, 2200, 2700, 4300, 4800, 6400, 6900];
  return {
    R, H, sideE, sideAreaE, sidePerE, baseE, netE, sideK, sideAreaK, baseK, surfK, volK,
    E: {
      side: `${fmt(sideE)} cm`,
      board: [
        { k: "h", s: "옆면의 가로 = 밑면의 둘레" }, { s: `${2 * R} × 3.14 = ‹${fmt(sideE)}›(cm)` },
        { k: "h", s: "옆면의 넓이" }, { s: `${fmt(sideE)} × ${H} = ‹${fmt(sideAreaE)}›(cm²)` },
        { k: "h", s: "옆면의 둘레" }, { s: `(${fmt(sideE)} + ${H}) × 2 = ‹${fmt(sidePerE)}›(cm)` },
        { k: "h", s: "전개도의 넓이 = 밑면 2개 + 옆면" }, { s: `${R} × ${R} × 3.14 × 2 + ${fmt(sideAreaE)} = ‹${fmt(netE)}›(cm²)` },
      ].map((L, i) => ({ ...L, d: d[i] })),
    },
    M: {
      side: `${piK(sideK)} cm`,
      vol: piK(volK),
      board: [
        { k: "h", s: "옆면의 가로 = 밑면의 둘레" }, { s: `2π × ${R} = ‹${piK(sideK)}›(cm)` },
        { k: "h", s: "옆면의 넓이" }, { s: `${piK(sideK)} × ${H} = ‹${piK(sideAreaK)}›(cm²)` },
        { k: "h", s: "옆면의 둘레" }, { s: `(${piK(sideK)} + ${H}) × 2 = ‹${piK(2 * sideK)} + ${2 * H}›(cm)` },
        { k: "h", s: "겉넓이 = 밑넓이 × 2 + 옆넓이" }, { s: `π × ${R}² × 2 + ${piK(sideAreaK)} = ‹${piK(surfK)}›(cm²)` },
        { k: "h", s: "부피 = 밑넓이 × 높이", d: 13200 }, { s: `π × ${R}² × ${H} = ‹${piK(volK)}›(cm³)`, d: 13700 },
      ].map((L, i) => ({ ...L, d: L.d ?? d[i] })),
    },
  };
})();

/* ── 6. 구 ── */
export const SPHERE = (() => {
  const R = 6;
  const areaK = 4 * R * R, cylK = R * R * 2 * R, volK = (cylK * 2) / 3, volK2 = (4 / 3) * R ** 3;
  return {
    R, areaK, cylK, volK, volK2,
    E: { dia: `${R} × 2 = ‹${2 * R}›(cm)` },
    M: {
      area: `= 4π × ${R}² = ‹${piK(areaK)}›(cm²)`,
      cylV: `원기둥 : π × ${R}² × ${2 * R} = ${piK(cylK)}`,
      vol: `구 : ${piK(cylK)} × {2/3} = ‹${piK(volK)}›(cm³)`,
    },
  };
})();

/* ── 평면 도형 공통: 내각으로 다각형 만들기 ──
   angles: 꼭짓점 V1…Vn 의 내각(도), 합 = 180(n−2). sides: 앞쪽 n−2 개 변의 길이.
   V1→V2 를 오른쪽(0°)으로 두고 왼쪽으로 돌며 걷는다. 마지막 두 변은 닫히도록 푼다. (수학 좌표, y 위) */
export function polyFromAngles(angles, sides) {
  const n = angles.length;
  const th = [0];
  for (let i = 1; i < n; i++) th.push(th[i - 1] + (180 - angles[i]));
  const u = th.map((d) => [Math.cos((d * Math.PI) / 180), Math.sin((d * Math.PI) / 180)]);
  let wx = 0, wy = 0;
  for (let i = 0; i < n - 2; i++) { wx -= sides[i] * u[i][0]; wy -= sides[i] * u[i][1]; }
  const [a, b] = u[n - 2], [c, d] = u[n - 1];
  const det = a * d - b * c;
  const sA = (wx * d - wy * c) / det, sB = (a * wy - b * wx) / det;
  const all = [...sides.slice(0, n - 2), sA, sB];
  const pts = [[0, 0]];
  for (let i = 0; i < n - 1; i++) pts.push([pts[i][0] + all[i] * u[i][0], pts[i][1] + all[i] * u[i][1]]);
  return { pts, sides: all };
}
/** 다각형의 내각(도) — 반시계 꼭짓점 순서 */
export function interiorAngles(pts) {
  const n = pts.length;
  return pts.map((p, i) => {
    const a = pts[(i - 1 + n) % n], b = pts[(i + 1) % n];
    const v1 = [a[0] - p[0], a[1] - p[1]], v2 = [b[0] - p[0], b[1] - p[1]];
    const ang = Math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (Math.hypot(...v1) * Math.hypot(...v2)));
    return (ang * 180) / Math.PI;
  });
}

/* ── 7. 삼각형의 세 각 ── */
export const TRI3 = (() => {
  const A = 50, B = 70, Cc = 60;
  // 중등: ∠A = (2x+10)°, ∠B = (3x+10)°, ∠C = 60° → 5x + 80 = 180
  const x = (180 - Cc - 20) / 5;
  return {
    A, B, Cc, x, ext: A + B,
    E: {
      lab: { A: `${A}°`, B: `${B}°`, C: "㉠" },
      board: [
        { s: "세 각의 크기의 합 = 180°", k: "h" },
        { s: `${A}° + ${B}° + ㉠ = 180°` },
        { s: `㉠ = 180° − ${A + B}° = ‹${Cc}°›` },
        { s: "직선이 이루는 각 = 180°", k: "h" },
        { s: `㉡ = 180° − ${Cc}° = ‹${180 - Cc}°›` },
      ],
      ext: "㉡",
    },
    M: {
      lab: { A: "(2*x* + 10)°", B: "(3*x* + 10)°", C: `${Cc}°` },
      solved: { A: `${2 * x + 10}°`, B: `${3 * x + 10}°` },
      board: [
        { s: "내각의 크기의 합 = 180°", k: "h" },
        { s: `(2*x* + 10) + (3*x* + 10) + ${Cc} = 180` },
        { s: `5*x* + ${20 + Cc} = 180,  ‹*x* = ${x}›` },
        { s: "외각 = 이웃하지 않은 두 내각의 합", k: "h" },
        { s: `∠ACD = ${2 * x + 10}° + ${3 * x + 10}° = ‹${A + B}°›` },
      ],
      ext: "∠ACD",
    },
  };
})();

/* ── 8. 다각형의 각의 합 ── */
export const POLY = (() => {
  const qa = [80, 95, 110, 75], pa = [100, 110, 115, 95, 120];
  const quad = polyFromAngles(qa, [9, 6]);
  const pent = polyFromAngles(pa, [7, 5.5, 6]);
  const hex = { pts: Array.from({ length: 6 }, (_, i) => [Math.cos(((i * 60 - 120) * Math.PI) / 180) * 5, Math.sin(((i * 60 - 120) * Math.PI) / 180) * 5]) };
  const qKnown = qa.slice(0, 3).reduce((a, b) => a + b, 0);         // 285
  const pKnown = pa.slice(0, 4).reduce((a, b) => a + b, 0);         // 420
  const pFix = pa.slice(0, 3).reduce((a, b) => a + b, 0);           // 325 (중등: 나머지 두 각이 식)
  // 중등 오각형: ∠V4 = (x + 45)°, ∠V5 = (2x + 20)° → 3x + 65 + 325 = 540
  const px = (540 - pFix - 65) / 3;
  return {
    qa, pa, quad: quad.pts, pent: pent.pts, hex: hex.pts, qKnown, pKnown, pFix, px,
    E: {
      qLab: [...qa.slice(0, 3).map((v) => `${v}°`), "㉠"],
      pLab: [...pa.slice(0, 4).map((v) => `${v}°`), "㉠"],
      board: [
        { k: "h", s: "사각형" }, { s: "삼각형 2개 → 180° × 2 = 360°" }, { s: `㉠ = 360° − ${qKnown}° = ‹${360 - qKnown}°›` },
        { k: "h", s: "오각형" }, { s: "삼각형 3개 → 180° × 3 = 540°" }, { s: `㉠ = 540° − ${pKnown}° = ‹${540 - pKnown}°›` },
        { k: "h", s: "육각형" }, { s: "삼각형 4개 → 180° × 4 = ‹720°›" },
      ],
    },
    M: {
      qLab: [...qa.slice(0, 3).map((v) => `${v}°`), "*x*°"],
      qSolved: `${360 - qKnown}°`,
      pLab: [...pa.slice(0, 3).map((v) => `${v}°`), "(*x* + 45)°", "(2*x* + 20)°"],
      pSolved: [`${px + 45}°`, `${2 * px + 20}°`],
      board: [
        { k: "h", s: "사각형" }, { s: "180° × (4 − 2) = 360°" }, { s: `${qa.slice(0, 3).join(" + ")} + *x* = 360,  ‹*x* = ${360 - qKnown}›` },
        { k: "h", s: "오각형" }, { s: "180° × (5 − 2) = 540°" }, { s: `${pFix} + (*x* + 45) + (2*x* + 20) = 540` }, { s: `3*x* = ${540 - pFix - 65},  ‹*x* = ${px}›` },
        { k: "h", s: "*n*각형의 내각의 크기의 합" }, { s: "‹180° × (*n* − 2)›" },
      ],
    },
  };
})();

/* ── 9. 대각선 ── */
export const DIAG = (() => {
  const count = (n) => (n * (n - 3)) / 2;
  const newPer = (n) => Array.from({ length: n - 3 }, (_, i) => (i === 0 ? n - 3 : n - 2 - i)).filter((v) => v > 0);
  // 초등: 꼭짓점 차례로 새로 생기는 대각선 수 — 육각형 3+3+2+1, 팔각형 5+5+4+3+2+1
  const seq = (n) => { const out = []; for (let i = 0; i < n; i++) { let c = 0; for (let j = i + 2; j < n; j++) if (!(i === 0 && j === n - 1)) c++; if (c) out.push(c); } return out; };
  const target = 20;
  let nFor = 0; for (let n = 4; n < 40; n++) if (count(n) === target) { nFor = n; break; }
  return {
    count, seq, newPer, target, nFor,
    E: {
      board: [
        { k: "h", s: "대각선" }, { s: "이웃하지 않는 두 꼭짓점을 이은 선분" },
        { k: "h", s: "육각형" }, { s: `${seq(6).join(" + ")} = ‹${count(6)}›(개)` },
        { k: "h", s: "팔각형" }, { s: `${seq(8).join(" + ")} = ‹${count(8)}›(개)` },
      ],
    },
    M: {
      board: [
        { k: "h", s: "육각형" }, { s: "한 꼭짓점에서 6 − 3 = 3(개)" }, { s: `6 × 3 ÷ 2 = ‹${count(6)}›(개)` },
        { k: "h", s: "*n*각형의 대각선의 개수" }, { s: "‹{*n*(*n* − 3)/2}›" },
        { k: "h", s: `대각선이 ${target}개인 다각형` }, { s: `{*n*(*n* − 3)/2} = ${target},  *n*(*n* − 3) = ${2 * target}` },
        { s: `${nFor} × ${nFor - 3} = ${2 * target}  →  ‹팔각형›` },
      ],
    },
  };
})();

/* ── 10. 이등변삼각형 ── */
export const ISO = (() => {
  const apex = 40, base = (180 - apex) / 2, BC = 10;
  // 중등: ∠A = (x+10)°, ∠B = ∠C = (2x+10)° → (x+10) + 2(2x+10) = 180 → 5x + 30 = 180
  const x = (180 - 30) / 5;
  return {
    apex, base, BC, x,
    E: {
      lab: { A: `${apex}°`, B: "㉠", C: "㉡" },
      board: [
        { k: "h", s: "이등변삼각형" }, { s: "두 변의 길이가 같아요" }, { s: "두 각의 크기가 같아요 (㉠ = ㉡)" },
        { k: "h", s: "㉠ 구하기" }, { s: `㉠ + ㉡ = 180° − ${apex}° = ${180 - apex}°` }, { s: `㉠ = ${180 - apex}° ÷ 2 = ‹${base}°›` },
        { k: "h", s: "접은 선은" }, { s: `밑변과 수직, 밑변을 반으로 (${BC / 2} cm, ${BC / 2} cm)` },
      ],
    },
    M: {
      lab: { A: "(*x* + 10)°", B: "(2*x* + 10)°", C: "" },
      solved: { A: `${x + 10}°`, B: `${2 * x + 10}°`, C: `${2 * x + 10}°` },
      board: [
        { k: "h", s: "AB = AC 인 이등변삼각형" }, { s: "두 밑각의 크기가 같다: ‹∠B = ∠C›" },
        { k: "h", s: "*x* 구하기" }, { s: "(*x* + 10) + (2*x* + 10) × 2 = 180" }, { s: `5*x* + 30 = 180,  ‹*x* = ${x}›` },
        { k: "h", s: "꼭지각의 이등분선은 밑변을 수직이등분" }, { s: `BD = CD = ${BC / 2} cm,  AD ⊥ BC` },
      ],
    },
  };
})();

/* ── 11. 평행사변형 ── */
export const PARA = (() => {
  const angB = 65, AB = 6, BC = 9;
  // 중등: ∠B = (3x+5)°, ∠D = (2x+25)° → x = 20 ; AD = (2y+1) cm, BC = 9 cm → y = 4
  const x = 25 - 5, y = (BC - 1) / 2;
  return {
    angB, AB, BC, x, y, angA: 180 - angB,
    E: {
      lab: { A: "㉠", B: `${angB}°`, C: "", D: "㉡", AD: "㉢", BC: `${BC} cm`, AB: `${AB} cm` },
      board: [
        { k: "h", s: "마주 보는 각의 크기가 같아요" }, { s: `㉡ = ‹${angB}°›` },
        { k: "h", s: "이웃한 두 각의 합은 180°" }, { s: `㉠ = 180° − ${angB}° = ‹${180 - angB}°›` },
        { k: "h", s: "마주 보는 변의 길이가 같아요" }, { s: `㉢ = ‹${BC} cm›` },
        { k: "h", s: "마주 보는 두 쌍의 변이 서로 평행" },
      ],
    },
    M: {
      lab: { A: "", B: "(3*x* + 5)°", C: "", D: "(2*x* + 25)°", AD: "(2*y* + 1) cm", BC: `${BC} cm`, AB: "" },
      solved: { B: `${3 * x + 5}°`, D: `${2 * x + 25}°`, AD: `${2 * y + 1} cm` },
      board: [
        { k: "h", s: "두 쌍의 대각의 크기는 각각 같다" }, { s: `3*x* + 5 = 2*x* + 25,  ‹*x* = ${x}›` },
        { k: "h", s: "두 쌍의 대변의 길이는 각각 같다" }, { s: `2*y* + 1 = ${BC},  ‹*y* = ${y}›` },
        { k: "h", s: "두 대각선은 서로를 이등분한다" }, { s: "OA = OC,  OB = OD" },
      ],
    },
  };
})();

/* ── 12. 사다리꼴·마름모의 넓이 ── */
export const TRAP = (() => {
  const top = 5, bot = 9, h = 6, area = ((top + bot) * h) / 2;
  const d1 = 8, d2 = 6, rArea = (d1 * d2) / 2;
  // 중등: 윗변 x, 아랫변 x + 4 → (2x + 4) × 6 ÷ 2 = 42 → x = 5 ; 대각선 x, 6, 넓이 24 → x = 8
  const tx = (area * 2 / h - 4) / 2, rx = (rArea * 2) / d2;
  return {
    top, bot, h, area, d1, d2, rArea, tx, rx,
    E: {
      tLab: { top: `${top} cm`, bot: `${bot} cm`, h: `${h} cm` },
      rLab: { d1: `${d1} cm`, d2: `${d2} cm` },
      board: [
        { k: "h", s: "사다리꼴의 넓이" }, { s: "(윗변 + 아랫변) × 높이 ÷ 2" }, { s: `(${top} + ${bot}) × ${h} ÷ 2 = ‹${area}›(cm²)` },
        { k: "h", s: "마름모의 넓이" }, { s: "(대각선) × (대각선) ÷ 2" }, { s: `${d1} × ${d2} ÷ 2 = ‹${rArea}›(cm²)` },
      ],
    },
    M: {
      tLab: { top: "*x* cm", bot: "(*x* + 4) cm", h: `${h} cm` },
      rLab: { d1: "*x* cm", d2: `${d2} cm` },
      board: [
        { k: "h", s: `사다리꼴의 넓이가 ${area} cm²` }, { s: `{1/2} × {*x* + (*x* + 4)} × ${h} = ${area}` }, { s: `6*x* + 12 = ${area},  ‹*x* = ${tx}›` },
        { k: "h", s: `마름모의 넓이가 ${rArea} cm²` }, { s: `{1/2} × *x* × ${d2} = ${rArea}` }, { s: `3*x* = ${rArea},  ‹*x* = ${rx}›` },
      ],
    },
  };
})();


/* ══════════ 자료와 가능성(초등) ↔ 경우의 수와 확률(중2) ══════════ */
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
/** 기약분수 글자: (6, 36) → "{1/6}", (4, 4) → "1", (0, 4) → "0" */
export function fracTxt(n, d) {
  if (n === 0) return "0";
  const g = gcd(n, d), a = n / g, b = d / g;
  return b === 1 ? String(a) : `{${a}/${b}}`;
}

/* ── 13. 분류하기 ↔ 사건과 경우의 수 · 합의 법칙 ── */
// 카드 12장: 모양(동그라미·세모·네모) × 색(빨강·파랑·노랑). 색 글자 r·b·y 는 아이콘 색 글자와 같다.
export const SORT = (() => {
  const spec = [["circle", "r"], ["circle", "r"], ["circle", "b"], ["circle", "b"], ["circle", "y"],
    ["tri", "r"], ["tri", "b"], ["tri", "b"], ["tri", "y"], ["square", "r"], ["square", "b"], ["square", "y"]];
  const CARDS = spec.map(([shape, color], id) => ({ id, shape, color }));
  const SHAPES = ["circle", "tri", "square"], COLORS = ["r", "b", "y"];
  const SH = { circle: "○", tri: "△", square: "□" }, CN = { r: "빨강", b: "파랑", y: "노랑" };
  const CA = { r: "빨간", b: "파란", y: "노란" };                // 꾸밈말: 파란 카드
  const byShape = SHAPES.map((k) => CARDS.filter((c) => c.shape === k).length);
  const byColor = COLORS.map((k) => CARDS.filter((c) => c.color === k).length);
  const circleRed = CARDS.filter((c) => c.shape === "circle" && c.color === "r").length;
  const orCT = byShape[0] + byShape[1];                 // 동그라미 또는 세모
  const orBY = byColor[1] + byColor[2];                 // 파랑 또는 노랑
  const orCR = byShape[0] + byColor[0] - circleRed;     // 동그라미 또는 빨강 (겹침 빼기)
  const mostColor = COLORS[byColor.indexOf(Math.max(...byColor))];
  const icon = (k) => `⟪${SH[k]}⟫`;
  return {
    CARDS, SHAPES, COLORS, SH, CN, byShape, byColor, circleRed, orCT, orBY, orCR, mostColor,
    E: {
      shapeLine: SHAPES.map((k, i) => `${icon(k)} ${byShape[i]}장`).join("   "),
      colorLine: COLORS.map((k, i) => `⟪●${k}⟫ ${CN[k]} ${byColor[i]}`).join("  "),
      most: `${CA[mostColor]} 카드가 가장 많아요 (${Math.max(...byColor)}장)`,
    },
    M: {
      all: `일어나는 모든 경우 : ‹${CARDS.length}›가지`,
      ct: `${icon("circle")} 또는 ${icon("tri")} : ${byShape[0]} + ${byShape[1]} = ‹${orCT}›(가지)`,
      by: `파랑 또는 노랑 : ${byColor[1]} + ${byColor[2]} = ‹${orBY}›(가지)`,
      cr: `${icon("circle")} 또는 빨강 : ${byShape[0]} + ${byColor[0]} − ${circleRed} = ‹${orCR}›(가지)`,
    },
  };
})();

/* ── 14. 표와 ○그래프 ↔ 두 주사위의 합 ── */
export const SEASON = (() => {
  const NAMES = ["봄", "여름", "가을", "겨울"];
  const NOTES = ["봄", "여름", "가을", "봄", "겨울", "여름", "봄", "겨울", "가을", "여름", "봄", "겨울", "여름", "가을", "봄", "겨울"];
  const COUNTS = NAMES.map((n) => NOTES.filter((x) => x === n).length);
  const TOTAL = NOTES.length;
  const most = NAMES[COUNTS.indexOf(Math.max(...COUNTS))];
  return {
    NAMES, NOTES, COUNTS, TOTAL, most,
    sumLine: `합계 : ${COUNTS.join(" + ")} = ‹${TOTAL}›(명)`,
    mostLine: `가장 많은 학생이 좋아하는 계절 : ‹${most}›`,
  };
})();
export const DICE2 = (() => {
  const CELLS = [];
  for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) CELLS.push({ a, b, s: a + b });
  const SUMS = Array.from({ length: 11 }, (_, i) => i + 2);
  const BY_SUM = SUMS.map((s) => CELLS.filter((c) => c.s === s).length);
  const TOTAL = CELLS.length;
  const best = SUMS[BY_SUM.indexOf(Math.max(...BY_SUM))];
  const n7 = BY_SUM[SUMS.indexOf(7)];
  return {
    CELLS, SUMS, BY_SUM, TOTAL, best, n7,
    mulLine: `6 × 6 = ‹${TOTAL}›(가지)`,
    n7Line: `합이 7인 경우 : ‹${n7}›가지`,
    p7Line: `(합이 7일 확률) = {${n7}/${TOTAL}} = ‹${fracTxt(n7, TOTAL)}›`,
    bestLine: `가장 일어나기 쉬운 합 : ‹${best}›`,
  };
})();

/* ── 15. 수 카드 표 ↔ 자연수 만들기 (포지티브·네거티브 규칙) ── */
export const NUMCARDS = (() => {
  const DIGITS = [0, 1, 2, 3];
  const GRID = DIGITS.map((t) => DIGITS.map((o) => ({ t, o, zero: t === 0, same: t === o, ok: t !== 0 && t !== o, v: 10 * t + o })));
  const TWO = GRID.flat().filter((c) => c.ok).map((c) => c.v);
  const ROWS = DIGITS.filter((t) => t !== 0).map((t) => TWO.filter((v) => Math.floor(v / 10) === t));
  const THREE = [];
  for (const a of DIGITS) for (const b of DIGITS) for (const c of DIGITS)
    if (a !== 0 && a !== b && a !== c && b !== c) THREE.push(100 * a + 10 * b + c);
  const tens = DIGITS.filter((d) => d !== 0).length;            // 십의 자리: 0 빼고
  const ones = DIGITS.length - 1;                                // 일의 자리: 남은 카드
  return {
    DIGITS, GRID, TWO, ROWS, THREE, tens, ones,
    max: Math.max(...TWO), min: Math.min(...TWO),
    E: {
      count: `${ROWS.map((r) => r.length).join(" + ")} = ‹${TWO.length}›(개)`,
      maxmin: `가장 큰 수 ‹${Math.max(...TWO)}› · 가장 작은 수 ‹${Math.min(...TWO)}›`,
    },
    M: {
      pos: `포지티브 : 카드 ${DIGITS.join(", ")}`,
      neg1: "네거티브 : 2장만, 같은 카드 두 번 ×",
      neg2: "네거티브 : 십의 자리에 0 ×",
      strat: `십의 자리 ${tens}가지 × 일의 자리 ${ones}가지`,
      two: `= ${tens} × ${ones} = ‹${tens * ones}›(개)`,
      three: `세 자리 정수 : ${tens} × ${ones} × ${ones - 1} = ‹${tens * ones * (ones - 1)}›(개)`,
    },
  };
})();

/* ── 16. 막대그래프 ↔ 상대도수와 확률 ── */
// 결정적 난수(씨앗 9)로 던진 주사위 6000번. 30번·60번 결과는 가장 많은/적은 눈이 하나씩만 나오도록 고른 씨앗.
export const FREQ = (() => {
  const SEED = 9, N = 6000;
  const r = rng(SEED);
  const ROLLS = Array.from({ length: N }, () => 1 + Math.floor(r() * 6));
  const PREF = [1, 2, 3, 4, 5, 6].map((f) => { const a = [0]; for (let i = 0; i < N; i++) a.push(a[i] + (ROLLS[i] === f ? 1 : 0)); return a; });
  const countAt = (n) => PREF.map((a) => a[Math.max(0, Math.min(N, Math.floor(n)))]);
  const argOf = (c, f) => c.indexOf(f(...c)) + 1;
  const c30 = countAt(30), c60 = countAt(60);
  const max30 = argOf(c30, Math.max), max60 = argOf(c60, Math.max), min60 = argOf(c60, Math.min);
  const c6000 = countAt(6000), rf = c6000.map((c) => c / N);
  const r2 = rf.map((v) => Math.round(v * 100) / 100);           // 소수 둘째 자리까지 반올림해 보여 준다
  const lo = Math.min(...r2), hi = Math.max(...r2);
  return {
    SEED, N, ROLLS, PREF, countAt,
    max30, min30: argOf(c30, Math.min), max60, min60,
    c30, c60, c600: countAt(600), c6000, lo, hi,
    E: {
      max30: `가장 많이 나온 눈 : ⟪d${max30}⟫ ‹${c30[max30 - 1]}›번`,
      max60: `가장 많이 나온 눈 : ⟪d${max60}⟫ ‹${c60[max60 - 1]}›번`,
      min60: `가장 적게 나온 눈 : ⟪d${min60}⟫ ‹${c60[min60 - 1]}›번`,
      cap: `가장 많이 나온 눈은 ⟪d${max60}⟫, 가장 적게 나온 눈은 ⟪d${min60}⟫`,
    },
    M: {
      ex30: `30번 : ⟪d${max30}⟫ {${c30[max30 - 1]}/30} ≈ ${(c30[max30 - 1] / 30).toFixed(2)}`,
      range: `${N}번 : 모두 약 ${lo.toFixed(2)} ~ ${hi.toFixed(2)}`,
    },
  };
})();

/* ── 17. 가능성 ↔ 확률의 성질 ── */
export const CHANCE = (() => {
  const TOTAL = 4, REDS = [0, 1, 2, 3, 4];
  const WORDS = ["불가능하다", "~아닐 것 같다", "반반이다", "~일 것 같다", "확실하다"];
  const P = REDS.map((r) => fracTxt(r, TOTAL));
  const PRAW = REDS.map((r) => `{${r}/${TOTAL}}`);
  const comp = 3;                                     // 빨강 3개 주머니로 여사건
  return {
    TOTAL, REDS, WORDS, P, PRAW, comp,
    compLine: `1 − ${P[comp]} = ‹${fracTxt(TOTAL - comp, TOTAL)}›`,
  };
})();
