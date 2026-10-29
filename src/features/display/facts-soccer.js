// ashrain.out — 교실 모니터 「축구」 묶음의 수 (facts-soccer.js)
// 「숫자로 경기를 읽다」(claude/SRC-스포츠데이터서술형-v1 · 10/28 수정판 1~3번) 여섯 문항을 장면으로 옮겼다.
// 화면에 나오는 수와 판서 글자는 모두 여기서 계산한다. tests/display-stories.test.mjs 가 따로 다시 계산해 맞춰 본다.
// 위치는 실제 장면을 바탕으로 계산하기 쉽게 다듬은 값, 기록표는 가상의 자료(원문항과 같음).
import { fmt } from "./core.js";

/* ── 분수 ── */
export const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
/** 기약분수 [분자, 분모] */
export function frac(n, d) { const g = gcd(n, d) || 1; return [n / g, d / g]; }
/** 기약분수 글자: {2/5} · 정수면 그대로 */
export function ftxt(n, d) { const [a, b] = frac(n, d); return b === 1 ? String(a) : `{${a}/${b}}`; }
/** 계급 찾기: [이상, 미만, …] 행들 가운데 lo ≤ d < hi 인 행 번호 */
export const classOf = (tab, d) => tab.findIndex(([lo, hi]) => lo <= d && d < hi);
/** 두 점 사이 거리 */
export const dist = (p, q) => Math.hypot(q[0] - p[0], q[1] - p[1]);
/** 제곱 글자 a² (소수는 그대로) */
const sq = (v) => `${fmt(v)}²`;

/* ══════════ 그날 선발 명단(등번호 · 이름) — 회색 상대 선수 · 옅은 같은 팀 선수의 이름표에 쓴다 ══════════ */
// 경기 기록의 선발 명단과 그 시즌 구단 등번호. 그림 속 자리는 실제 장면을 바탕으로 다듬은 값이라, 회색 선수가
// 정확히 그 자리에 있었다는 뜻은 아니다(장면 안 작은 글씨로 밝혀 둔다).
export const LINEUPS = {
  // 2012-04-30 맨시티 1−0 맨유 — 맨유 선발
  derby2012United: [[1, "데 헤아"], [4, "존스"], [5, "퍼디낸드"], [12, "스몰링"], [3, "에브라"], [17, "나니"], [16, "캐릭"],
    [22, "스콜스"], [13, "박지성"], [11, "긱스"], [10, "루니"]],
  // 2023-02-26 리그컵 결승 맨유 2−0 뉴캐슬 — 뉴캐슬 선발 · 맨유 선발
  cup2023Newcastle: [[18, "카리우스"], [2, "트리피어"], [5, "셰어"], [4, "보트만"], [33, "번"], [36, "롱스태프"], [39, "기마랑이스"],
    [7, "조엘린통"], [24, "알미론"], [9, "윌슨"], [10, "생막시맹"]],
  cup2023United: [[1, "데 헤아"], [20, "달로트"], [19, "바란"], [6, "마르티네스"], [23, "루크 쇼"], [18, "카세미루"], [17, "프레드"],
    [21, "안토니"], [8, "페르난데스"], [10, "래시포드"], [27, "베호르스트"]],
  // 2021-05-29 챔피언스리그 결승 맨시티 0−1 첼시 — 맨시티 선발
  final2021City: [[31, "에데르송"], [2, "워커"], [5, "스톤스"], [3, "디아스"], [11, "진첸코"], [8, "귄도안"], [17, "더브라위너"],
    [20, "베르나르두"], [26, "마레즈"], [7, "스털링"], [47, "포든"]],
};
/** 명단에서 이름으로 [등번호, 이름] */
export function who(team, name) {
  const hit = LINEUPS[team].find(([, nm]) => nm === name);
  if (!hit) throw new Error(`${team} 선발 명단에 없는 이름: ${name}`);
  return hit;
}

/* ══════════ 1. 맨시티 — 코너킥과 헤더골 (2012-04-30 맨체스터 더비 1−0) ══════════ */
export const CORNER = (() => {
  const KH = 26, HF = 10, KT = 31.5;                 // 코너킥 K→H · H에서 골라인까지 · 골라인을 따라 K→T
  const KF = Math.sqrt(KH ** 2 - HF ** 2);           // 24 (10 · 24 · 26 = 5 : 12 : 13 × 2)
  const FT = KT - KF;                                 // 7.5
  const HT = Math.sqrt(FT ** 2 + HF ** 2);            // 12.5 (7.5 · 10 · 12.5 = 3 : 4 : 5 × 2.5)
  const P = { K: [0, 0], F: [KF, 0], H: [KF, HF], T: [KT, 0] };
  const GOAL = { c: 34, w: 7.32 };                    // 구장 너비 68 m → 골대 가운데는 K에서 34 m
  const flight = KH + HT;
  return {
    KH, HF, KT, KF, FT, HT, P, GOAL, flight,
    E: {
      kh: `코너킥 K → H  ‹${fmt(KH)} m›`,
      hf: `H → 골라인  ‹${fmt(HF)} m›`,
      kt: `골라인을 따라 K → T  ‹${fmt(KT)} m›`,
      kf: `골라인을 따라 K → F  ‹${fmt(KF)} m›`,
      ft: `F → T = ${fmt(KT)} − ${fmt(KF)} = ‹${fmt(FT)} m›`,
      ht: `헤더 H → T  ‹${fmt(HT)} m›`,
      sum: `공이 날아간 길 ${fmt(KH)} + ${fmt(HT)} = ‹${fmt(flight)} m›`,
      tapeKH: `${fmt(KH)} m`, tapeHF: `${fmt(HF)} m`, tapeKT: `${fmt(KT)} m`, tapeKF: `${fmt(KF)} m`, tapeHT: `${fmt(HT)} m`,
    },
    M: {
      eq1: `KF² + ${sq(HF)} = ${sq(KH)}`,
      kf2: `KF² = ${KH ** 2} − ${HF ** 2} = ${KF ** 2} = ${sq(KF)}`,
      kf: `KF = ${fmt(KF)},  FT = ${fmt(KT)} − ${fmt(KF)} = ‹${fmt(FT)}›`,
      eq2: `HT² = ${sq(FT)} + ${sq(HF)} = ${fmt(FT ** 2 + HF ** 2)}`,
      ht: `= ${sq(HT)}  →  HT = ‹${fmt(HT)} m›`,
      ratio: `${HF / 2} : ${KF / 2} : ${KH / 2} (× 2)  ·  3 : 4 : 5 (× ${fmt(FT / 3)})`,
      lab: { KH: `${fmt(KH)}`, HF: `${fmt(HF)}`, KF: `${fmt(KF)}`, FT: `${fmt(FT)}`, KT: `${fmt(KT)} m`, HT: `${fmt(HT)}` },
    },
  };
})();

/* ══════════ 2. 맨유 — 크로스 세트피스 (2023-02-26 리그컵 결승 2−0, 33분) ══════════ */
export const SETPIECE = (() => {
  const G = [0, 0], F = [26, 23], H = [6, 8];        // 골대 가운데 G · 옆(골라인 방향) · 앞(골라인에서)
  const dx = F[0] - H[0], dy = F[1] - H[1];           // 20, 15
  const FH = Math.hypot(dx, dy), HG = Math.hypot(H[0], H[1]);   // 25, 10
  // [이상, 미만, 시도, 성공]
  const CROSS = [[10, 20, 40, 22], [20, 30, 150, 60], [30, 40, 60, 15]];
  const HEAD = [[0, 5, 30, 9], [5, 10, 80, 12], [10, 15, 60, 6], [15, 20, 30, 1]];
  const ci = classOf(CROSS, FH), hi = classOf(HEAD, HG);
  const [, , cn, ck] = CROSS[ci], [, , hn, hk] = HEAD[hi];
  const p = frac(ck * hk, cn * hn);                   // 1/25
  const N = 100, nHead = (N * ck) / cn, nGoal = (nHead * hk) / hn;   // 40, 4
  const range = (r) => `${r[0]} 이상 ~ ${r[1]} 미만`;
  return {
    G, F, H, dx, dy, FH, HG, CROSS, HEAD, ci, hi, p, N, nHead, nGoal,
    tot: { cross: CROSS.reduce((a, r) => [a[0] + r[2], a[1] + r[3]], [0, 0]), head: HEAD.reduce((a, r) => [a[0] + r[2], a[1] + r[3]], [0, 0]) },
    range,
    E: {
      fh: `프리킥 F → H  ‹${fmt(FH)} m›`,
      hg: `헤더 H → G  ‹${fmt(HG)} m›`,
      cls1: `${fmt(FH)} m : 크로스 ${cn}번 중 ${ck}번 머리에`,
      cls2: `${fmt(HG)} m : 헤더 ${hn}번 중 ${hk}번 골`,
      edge: `${fmt(HG)} m는 ‘${HEAD[hi][0]} 이상 ${HEAD[hi][1]} 미만’`,
      n1: `${N}번 차면 머리에 닿는 건 ‹${nHead}›번`,
      n2: `그 ${nHead}번 가운데 골은 ‹${nGoal}›번`,
      n3: `${N}번 중 ‹${nGoal}›번 — ${N / nGoal}번에 1번꼴`,
      tapeFH: `${fmt(FH)} m`, tapeHG: `${fmt(HG)} m`,
      grid: [`${N}번`, `머리에 ${nHead}번`, `골 ${nGoal}번`],
    },
    M: {
      fh: `FH² = ${sq(dx)} + ${sq(dy)} = ${dx ** 2 + dy ** 2} = ${sq(FH)}`,
      hg: `HG² = ${sq(H[0])} + ${sq(H[1])} = ${H[0] ** 2 + H[1] ** 2} = ${sq(HG)}`,
      p1: `머리에 닿을 확률 {${ck}/${cn}} = ‹${ftxt(ck, cn)}›`,
      p2: `골이 될 확률 {${hk}/${hn}} = ‹${ftxt(hk, hn)}›`,
      edge: `HG = ${fmt(HG)} m는 ‘${HEAD[hi][0]} 이상’ 계급`,
      prod: `${ftxt(ck, cn)} × ${ftxt(hk, hn)} = ‹${ftxt(ck * hk, cn * hn)}›`,
      lab: { dx: `${dx}`, dy: `${dy}`, hx: `${H[0]}`, hy: `${H[1]}` },
      grid: [`${N}`, `× ${ftxt(ck, cn)} = ${nHead}`, `× ${ftxt(hk, hn)} = ${nGoal}`],
    },
  };
})();

/* ══════════ 3. 첼시 — 오프 더 볼과 쓰루패스 (2021-05-29 챔피언스리그 결승 1−0, 42분) ══════════ */
export const THROUGH = (() => {
  const O = [0, 0], S = [8, 19];
  const pass = [7, 24];                               // 패스: y = 7/24 x
  const run = { a: [-3, 4], b: 25 };                  // 달리기: y = −3/4 x + 25
  // 교점: 7/24 x = −3/4 x + 25 → (7 + 18) x = 600
  const x = (run.b * 24) / (pass[0] + 18), y = (pass[0] * x) / pass[1];   // 24, 7
  const M = [x, y];
  const OM = Math.hypot(x, y), SM = Math.hypot(x - S[0], S[1] - y);      // 25, 20
  const vBall = 12.5, vRun = 8;
  const tBall = OM / vBall, tRun = SM / vRun, lead = tRun - tBall;       // 2, 2.5, 0.5
  return {
    pts: { O, S, M }, pass, run, OM, SM, vBall, vRun, tBall, tRun, lead,
    defenders: [[15, 9.5], [17.5, 1.8], [20.5, 15.6]],   // 패스 길 · 달리는 길과 떨어진 곳
    E: {
      om: `공 O → M  ‹${fmt(OM)} m›`,
      sm: `하베르츠 S → M  ‹${fmt(SM)} m›`,
      v: `공은 1초에 ${fmt(vBall)} m, 하베르츠는 1초에 ${fmt(vRun)} m`,
      tb: `공  ${fmt(OM)} ÷ ${fmt(vBall)} = ‹${fmt(tBall)}›초`,
      tr: `하베르츠  ${fmt(SM)} ÷ ${fmt(vRun)} = ‹${fmt(tRun)}›초`,
      lead: `${fmt(tRun)} − ${fmt(tBall)} = ${fmt(lead)} → ‹${fmt(lead)}초› 먼저 출발`,
      tapeOM: `${fmt(OM)} m`, tapeSM: `${fmt(SM)} m`,
    },
    M: {
      eq: `{${pass[0]}/${pass[1]}}x = −{3/4}x + ${run.b}`,
      sol: `양변 × 24 : ${pass[0]}x = −18x + ${run.b * 24}  →  M(${fmt(x)}, ${fmt(y)})`,
      om: `OM² = ${sq(x)} + ${sq(y)} = ${x * x + y * y} = ${sq(OM)}`,
      sm: `SM² = ${sq(x - S[0])} + ${sq(S[1] - y)} = ${(x - S[0]) ** 2 + (S[1] - y) ** 2} = ${sq(SM)}`,
      t: `공 ${fmt(OM)} ÷ ${fmt(vBall)} = ${fmt(tBall)}(초),  하베르츠 ${fmt(SM)} ÷ ${fmt(vRun)} = ${fmt(tRun)}(초)`,
      lead: `${fmt(tRun)} − ${fmt(tBall)} = ‹${fmt(lead)}초› 전에 출발`,
      linePass: `y = {${pass[0]}/${pass[1]}}x`, lineRun: `y = −{3/4}x + ${run.b}`,
      mLab: `M(${fmt(x)}, ${fmt(y)})`, sLab: `S(${S[0]}, ${S[1]})`,
      legs: { om: [`${fmt(x)}`, `${fmt(y)}`], sm: [`${fmt(x - S[0])}`, `${fmt(S[1] - y)}`] },
    },
  };
})();

/* ══════════ 4. 맨유 삼각패스 — 패스 삼각형의 넓이 ══════════ */
export const TRIANGLE = (() => {
  const C = [28, 2];
  const ab = [4, 3, -2];                              // A → B: y = 4/3 x − 2
  const bcSlope = [-3, 4];                            // B → C: 기울기 −3/4
  const bcB = C[1] - (bcSlope[0] / bcSlope[1]) * C[0];   // 23
  const A = [(C[1] - ab[2]) / (ab[0] / ab[1]), C[1]];    // (3, 2)
  const xB = (bcB - ab[2]) / (ab[0] / ab[1] - bcSlope[0] / bcSlope[1]);
  const B = [xB, (ab[0] / ab[1]) * xB + ab[2]];          // (12, 14)
  const base = C[0] - A[0], height = B[1] - C[1];        // 25, 12
  const area = (base * height) / 2;                      // 150
  const rect = base * height;                            // 300
  const left = ((B[0] - A[0]) * height) / 2;             // 54
  const right = ((C[0] - B[0]) * height) / 2;            // 96
  const r = (v) => Math.round(v * 1e9) / 1e9;
  return {
    A: A.map(r), B: B.map(r), C, bcB: r(bcB), base: r(base), height: r(height), area: r(area), rect: r(rect), left: r(left), right: r(right),
    E: {
      w: `가로 ${C[0]} − ${r(A[0])} = ‹${r(base)} m›`,
      h: `세로 ${r(B[1])} − ${C[1]} = ‹${r(height)} m›`,
      rect: `직사각형 ${r(base)} × ${r(height)} = ${r(rect)}`,
      left: `왼쪽 삼각형 ${r(B[0] - A[0])} × ${r(height)} ÷ 2 = ${r(left)}`,
      right: `오른쪽 삼각형 ${r(C[0] - B[0])} × ${r(height)} ÷ 2 = ${r(right)}`,
      area: `${r(rect)} − ${r(left)} − ${r(right)} = ‹${r(area)} m²›`,
      check: `밑변 × 높이 ÷ 2 = ${r(base)} × ${r(height)} ÷ 2 = ${r(area)} ⟪✓t⟫`,
      lab: { w: `${r(base)} m`, h: `${r(height)} m`, lw: `${r(B[0] - A[0])}`, rw: `${r(C[0] - B[0])}`, left: `${r(left)}`, right: `${r(right)}` },
    },
    M: {
      b: `B → C : ${C[1]} = −{3/4} × ${C[0]} + b  →  b = ${r(bcB)}`,
      a: `A : {4/3}x − 2 = ${C[1]}  →  A(${r(A[0])}, ${r(A[1])})`,
      bb: `B : {4/3}x − 2 = −{3/4}x + ${r(bcB)}  →  B(${r(B[0])}, ${r(B[1])})`,
      bh: `밑변 AC = ${C[0]} − ${r(A[0])} = ${r(base)},  높이 ${r(B[1])} − ${C[1]} = ${r(height)}`,
      area: `넓이 {1/2} × ${r(base)} × ${r(height)} = ‹${r(area)} m²›`,
      trap: `높이를 ${r(B[1])}로 쓰면 ${r((base * B[1]) / 2)} ⟪×r⟫`,
      lineAB: `y = {4/3}x − 2`, lineBC: `y = −{3/4}x + b`, lineCA: `y = ${C[1]}`,
      labA: `A(${r(A[0])}, ${r(A[1])})`, labB: `B(${r(B[0])}, ${r(B[1])})`, labC: `C(${C[0]}, ${C[1]})`,
    },
  };
})();

/* ══════════ 5. 박지성·루니·호날두 역습 (2009-05-05 챔피언스리그 준결승 2차전 아스널 1−3 맨유, 61분) ══════════ */
export const COUNTER = (() => {
  // 박지성 O · 루니 R(교점) · 호날두 슈팅 C(교점)
  const l1 = [3, 4, 0], l2 = [-4, 3, 100], l3 = [16, 63, 0];      // y = (a/b) x + c
  const meet = (p, q) => { const x = (q[2] - p[2]) / (p[0] / p[1] - q[0] / q[1]); return [x, (p[0] / p[1]) * x + p[2]]; };
  const r9 = (v) => Math.round(v * 1e9) / 1e9;
  const R = meet(l1, l2).map(r9), Cc = meet(l2, l3).map(r9);       // (48, 36), (63, 16)
  const O = [0, 0], Hh = [Cc[0], 0], K = [0, R[1]], T = [Cc[0], R[1]];
  const OR = Math.hypot(R[0], R[1]), RC = Math.hypot(Cc[0] - R[0], R[1] - Cc[1]), OC = Math.hypot(Cc[0], Cc[1]);   // 60, 25, 65
  const ball = OR + RC, more = ball - OC;                            // 85, 20
  const rect = Cc[0] * R[1], tri = ((Cc[0] - R[0]) * (R[1] - Cc[1])) / 2, penta = rect - tri;   // 2268, 150, 2118
  return {
    O, R, C: Cc, H: Hh, K, T, OR, RC, OC, ball, more, rect, tri, penta,
    E: {
      or: `공 O → R  ‹${fmt(OR)} m›`,
      rc: `공 R → C  ‹${fmt(RC)} m›`,
      oc: `호날두 O → C  ‹${fmt(OC)} m›`,
      ball: `공 ${fmt(OR)} + ${fmt(RC)} = ${fmt(ball)} m,  호날두 ${fmt(OC)} m`,
      more: `${fmt(ball)} − ${fmt(OC)} = ‹${fmt(more)} m› 더`,
      rect: `직사각형 OHTK  ${Cc[0]} × ${R[1]} = ${rect}`,
      tri: `삼각형 CTR  ${Cc[0] - R[0]} × ${R[1] - Cc[1]} ÷ 2 = ${tri}`,
      penta: `오각형 ${rect} − ${tri} = ‹${penta} m²›`,
      tape: { or: `${fmt(OR)} m`, rc: `${fmt(RC)} m`, oc: `${fmt(OC)} m` },
      lab: { w: `${Cc[0]} m`, h: `${R[1]} m`, tw: `${Cc[0] - R[0]}`, th: `${R[1] - Cc[1]}` },
    },
    M: {
      r: `R : {3/4}x = −{4/3}x + 100  →  R(${R[0]}, ${R[1]})`,
      c: `C : {16/63}x = −{4/3}x + 100  →  C(${Cc[0]}, ${Cc[1]})`,
      or: `OR² = ${sq(R[0])} + ${sq(R[1])} = ${sq(OR)}`,
      rc: `RC² = ${sq(Cc[0] - R[0])} + ${sq(R[1] - Cc[1])} = ${sq(RC)},  OC² = ${sq(Cc[0])} + ${sq(Cc[1])} = ${sq(OC)}`,
      more: `${fmt(OR)} + ${fmt(RC)} − ${fmt(OC)} = ‹${fmt(more)} m›`,
      penta: `오각형 = ${Cc[0]} × ${R[1]} − {1/2} × ${Cc[0] - R[0]} × ${R[1] - Cc[1]} = ‹${penta} m²›`,
      lines: { or: `y = {3/4}x`, rc: `y = −{4/3}x + 100`, oc: `y = {16/63}x` },
      labR: `R(${R[0]}, ${R[1]})`, labC: `C(${Cc[0]}, ${Cc[1]})`,
    },
  };
})();

/* ══════════ 6. 맨시티 vs 첼시 — 적어도 한 골 (xG) ══════════ */
export const XG = (() => {
  const SHOTS = [[3, 4], [-8, 6], [16, 12]];           // 골대 가운데 O에서 옆 · 앞 (S2는 반대쪽)
  const D = SHOTS.map(([a, b]) => Math.hypot(a, b));   // 5, 10, 20
  const TAB = [[0, 10, 120, 30], [10, 20, 400, 50], [20, 30, 200, 8]];
  const cls = D.map((d) => classOf(TAB, d));
  const P = cls.map((i) => frac(TAB[i][3], TAB[i][2]));             // 1/4, 1/8, 1/25
  // 모두 골이 안 될 확률 = Π (1 − p)
  let nn = 1, dd = 1;
  for (const [a, b] of P) { nn *= b - a; dd *= b; }
  const none = frac(nn, dd), atLeast = frac(none[1] - none[0], none[1]);   // 63/100, 37/100
  // 자연 빈도: 800경기 — 경기마다 S1·S2·S3 차례로
  const N = P.reduce((a, [, b]) => a * b, 1);                       // 4 × 8 × 25 = 800 — 사슬의 수가 모두 자연수
  const miss = [N];
  for (const [a, b] of P) miss.push((miss.at(-1) * (b - a)) / b);  // 800, 600, 525, 504
  const goals = P.map(([a, b], i) => (miss[i] * a) / b);           // 200, 75, 21
  const hit = N - miss.at(-1), per100 = (hit * 100) / N;           // 296, 37
  const word = (k) => ["S1", "S2", "S3"][k];
  return {
    SHOTS, D, TAB, cls, P, none, atLeast, N, miss, goals, hit, per100,
    tot: TAB.reduce((a, r) => [a[0] + r[2], a[1] + r[3]], [0, 0]),
    E: {
      d: `S1 ‹${D[0]} m›,  S2 ‹${D[1]} m›,  S3 ‹${D[2]} m›`,
      s: P.map(([a, b], i) => `${word(i)}  ${TAB[cls[i]][2]}번 중 ${TAB[cls[i]][3]}번 → ‹${b / a}번에 1번›`),
      goals: goals.map((g) => `골 ${g}`),
      head: `${N}경기로 생각하면`,
      chain: miss.map(String),
      ops: P.map(([a, b]) => `${b}번 중 ${b - a}번`),
      opHead: P.map((_, i) => `${word(i)} 빗나감`),
      hit: `적어도 한 골  ${N} − ${miss.at(-1)} = ${hit}경기`,
      per: `→ 100경기마다 ‹${per100}›경기`,
      tape: D.map((d) => `${d} m`),
    },
    M: {
      d1: `OS1² = ${sq(3)} + ${sq(4)} = ${sq(D[0])},  OS2² = ${sq(8)} + ${sq(6)} = ${sq(D[1])}`,
      d2: `OS3² = ${sq(16)} + ${sq(12)} = ${sq(D[2])}`,
      p: `골 확률  ${P.map(([a, b]) => ftxt(a, b)).join(",  ")}`,
      side: P.map(([a, b], i) => `{${TAB[cls[i]][3]}/${TAB[cls[i]][2]}} = ${ftxt(a, b)}`),
      edge: `${D[1]} m, ${D[2]} m는 경계값 — ‘이상’ 쪽 계급`,
      none: `${P.map(([a, b]) => ftxt(b - a, b)).join(" × ")} = ${ftxt(nn, dd)}`,
      ans: `적어도 한 골 1 − ${ftxt(nn, dd)} = ‹${ftxt(dd - nn, dd)}›`,
      trap: `${P.map(([a, b]) => ftxt(a, b)).join(" + ")}로 더하면 ⟪×r⟫`,
      chain: ["1", ...P.map((_, i) => ftxt(miss[i + 1], N))],
      ops: P.map(([a, b]) => `× ${ftxt(b - a, b)}`),
    },
  };
})();
