// ashrain.out — 교실 모니터 「서술형」 묶음의 수 (facts-essay.js)
// 「손글씨 데이터 수집 문제 생성」 방의 「경로」(두 갈래 선로 · 역주행 차 앞의 선택과 세 번째 길)와 「게임의 규칙」(동아리 지원 ·
// 가위바위보), 「축제 서술형 10제」(claude/WORKSHEET-축제서술형10제-v1 — 3번 반티 · 5번 불이 켜지는 간판)를 장면으로 옮겼다.
// 화면에 나오는 수와 판서 글자는 모두 여기서 계산한다. tests/display-stories.test.mjs 가 따로 다시 계산해 맞춰 본다.
import { fmt } from "./core.js";
import { frac, ftxt } from "./facts-soccer.js";

const addF = ([a, b], [c, d]) => frac(a * d + c * b, b * d);

/* ══════════ 1. 「경로」 — 두 갈래 선로 ══════════ */
export const RAILS = (() => {
  // 갈림목 A → B(왼쪽·위) / C(오른쪽·아래), B → ①, ②, C → ③, D, D → ④, ⑤. 갈림목마다 왼쪽·오른쪽 같은 가능성.
  const TREE = { A: ["B", "C"], B: ["1", "2"], C: ["3", "D"], D: ["4", "5"] };
  const PEOPLE = { 1: 5, 2: 0, 3: 1, 4: 0, 5: 2 };            // 선로 위 작업자 수
  const ENDS = ["1", "2", "3", "4", "5"];
  const P = {}, PATH = {};
  const walk = (n, d, path) => {
    if (!TREE[n]) { P[n] = frac(1, d); PATH[n] = path; return; }
    for (const k of TREE[n]) walk(k, d * 2, [...path, n]);
  };
  walk("A", 1, []);
  const EMPTY = ENDS.filter((e) => PEOPLE[e] === 0);           // ②, ④
  const pEmpty = EMPTY.map((e) => P[e]).reduce(addF, [0, 1]);   // 3/8
  const N = 8;
  const COUNT = Object.fromEntries(ENDS.map((e) => [e, (N * P[e][0]) / P[e][1]]));   // 2, 2, 2, 1, 1
  // 장면에서 보내는 전차 8대: i 번째 전차는 i 를 이진수로 읽어 갈림목마다 0 이면 왼쪽(위), 1 이면 오른쪽(아래)으로 간다
  // (A 는 첫째 자리, B·C 는 둘째 자리, D 는 셋째 자리) — 갈림목마다 정확히 반씩 나뉘므로 선로마다 N × P 대가 들어간다.
  const TRAM_ENDS = Array.from({ length: N }, (_, i) => {
    let node = "A", bit = 0;
    while (TREE[node]) { node = TREE[node][(i >> bit) & 1]; bit++; }
    return node;
  });
  const nEmpty = EMPTY.reduce((a, e) => a + COUNT[e], 0);       // 3
  const wrong = frac(EMPTY.length, ENDS.length);                // 2/5
  const circ = (e) => "①②③④⑤"[Number(e) - 1];
  const halfs = (e) => Array(PATH[e].length).fill("{1/2}").join(" × ");
  return {
    TREE, PEOPLE, ENDS, P, PATH, EMPTY, pEmpty, N, COUNT, TRAM_ENDS, nEmpty, wrong, circ,
    E: {
      split: `갈림목마다 반씩 : ${N} → ${N / 2} · ${N / 2}`,
      ends: `①②③에 ${COUNT[1]}대씩, ④⑤에 ${COUNT[4]}대씩`,
      empty: `빈 선로 ${EMPTY.map((e) => `${circ(e)} ${COUNT[e]}대`).join(" + ")} = ‹${nEmpty}대›`,
      ans: `${N}대 중 ${nEmpty}대 → ‹${ftxt(nEmpty, N)}›`,
      trap: `다섯 갈래라서 ${ftxt(...wrong)}? ⟪×r⟫`,
      why: "갈래마다 들어간 전차 수가 달라요",
      count: (e) => `${COUNT[e]}대`,
    },
    M: {
      half: "갈림목마다 {1/2}",
      p: EMPTY.map((e) => `${circ(e)} : ${halfs(e)} = ${ftxt(...P[e])}`),
      sum: `${EMPTY.map((e) => ftxt(...P[e])).join(" + ")} = ‹${ftxt(...pEmpty)}›`,
      trap: `${ftxt(...wrong)} ⟪×r⟫ 다섯 갈래의 가능성이 같지 않아요`,
      each: `①②③ ${ftxt(...P[1])},  ④⑤ ${ftxt(...P[4])}`,
      prob: (e) => ftxt(...P[e]),
    },
  };
})();

/* ══════════ 2. 「경로」 — 역주행 차 앞의 선택 · 세 번째 길(점프) ══════════ */
export const WRONGWAY = (() => {
  // 확률은 10분의 몇으로 둔다: 반대 차로의 차 두 대가 각각 9, 인도의 사람 두 명이 각각 7, 뒷차 8, 점프 성공 9
  const OPP = 9, PED = 7, REAR = 8, JUMP = 9;
  const N = 1000;
  const chain = (fs) => { const out = [N]; for (const f of fs) out.push((out.at(-1) * f) / 10); return out; };
  const LEFT = chain([OPP, OPP, REAR]);      // 1000, 900, 810, 648
  const RIGHT = chain([PED, PED, REAR]);     // 1000, 700, 490, 392
  const JMP = chain([JUMP, REAR]);           // 1000, 900, 720
  const dec = (v) => fmt(v / N, 3);          // 648 → 0.648
  const d1 = (k) => fmt(k / 10, 1);          // 9 → 0.9
  const p = { stop: 0, left: LEFT.at(-1) / N, right: RIGHT.at(-1) / N, jump: JMP.at(-1) / N };
  const best2 = p.left >= p.right ? "left" : "right";
  const best3 = p.jump > p[best2] ? "jump" : best2;
  const word = { left: "왼쪽", right: "오른쪽", jump: "점프", stop: "멈춤 · 직진" };
  return {
    OPP, PED, REAR, JUMP, N, LEFT, RIGHT, JMP, p, best2, best3, word,
    E: {
      head: `같은 순간이 ${N}번 온다면 — 모두 무사한 횟수`,
      stop: "멈춤 · 직진 : 모두 무사 ‹0›번",
      left: `왼쪽 : ${LEFT.join(" → ")}번`.replace(`${LEFT.at(-1)}번`, `‹${LEFT.at(-1)}›번`),
      right: `오른쪽 : ${RIGHT.join(" → ")}번`.replace(`${RIGHT.at(-1)}번`, `‹${RIGHT.at(-1)}›번`),
      best: `가장 바람직한 선택 : ${word[best2]}`,
      jump: `점프 : ${JMP.join(" → ")}번`.replace(`${JMP.at(-1)}번`, `‹${JMP.at(-1)}›번`),
      change: `점프가 생기면 ${JMP.at(-1)} > ${LEFT.at(-1)} — 가장 좋은 선택이 바뀌어요`,
      ops: { left: ["10번 중 9번", "10번 중 9번", "10번 중 8번"], right: ["10번 중 7번", "10번 중 7번", "10번 중 8번"], jump: ["10번 중 9번", "10번 중 8번"] },
    },
    M: {
      head: "모두 무사할 확률 — 서로 영향을 주지 않으니 곱해요",
      stop: "멈춤 · 직진 : 0",
      left: `왼쪽 : ${d1(OPP)} × ${d1(OPP)} × ${d1(REAR)} = ‹${dec(LEFT.at(-1))}›`,
      right: `오른쪽 : ${d1(PED)} × ${d1(PED)} × ${d1(REAR)} = ‹${dec(RIGHT.at(-1))}›`,
      best: `→ ${word[best2]}이 가장 높아요`,
      jump: `점프 : ${d1(JUMP)} × ${d1(REAR)} = ‹${dec(JMP.at(-1))}› > ${dec(LEFT.at(-1))}`,
      change: "→ 가장 바람직한 선택이 점프로 바뀌어요",
      ops: { left: [`× ${d1(OPP)}`, `× ${d1(OPP)}`, `× ${d1(REAR)}`], right: [`× ${d1(PED)}`, `× ${d1(PED)}`, `× ${d1(REAR)}`], jump: [`× ${d1(JUMP)}`, `× ${d1(REAR)}`] },
      vals: { left: ["1", d1(OPP), dec(LEFT[2]), dec(LEFT[3])], right: ["1", d1(PED), dec(RIGHT[2]), dec(RIGHT[3])], jump: ["1", d1(JUMP), dec(JMP[2])] },
    },
    chips: { opp: d1(OPP), ped: d1(PED), rear: d1(REAR), jump: d1(JUMP) },
  };
})();

/* ══════════ 3. 「게임의 규칙」 — 동아리 지원 ══════════ */
export const CLUB = (() => {
  const CLUBS = ["밴드부", "보드게임부", "사진부", "요리부"];
  const FRIENDS = ["서아", "도윤", "지민"];
  const n = CLUBS.length;
  const CELLS = [];
  for (let s = 0; s < n; s++) for (let d = 0; d < n; d++) for (let j = 0; j < n; j++) CELLS.push({ s, d, j, ok: s !== d && d !== j && s !== j });
  const total = CELLS.length, ok = CELLS.filter((c) => c.ok).length, perBlock = ok / n;   // 64, 24, 6
  const p = frac(ok, total);                                                               // 3/8
  // 예로 보여 줄 두 번의 지원: 한 곳에 둘이 몰린 경우, 모두 다른 경우
  const TRIES = [[0, 0, 2], [3, 0, 1]];
  const admitted = (tr) => tr.map((c, i) => tr.filter((x) => x === c).length === 1);
  return {
    CLUBS, FRIENDS, n, CELLS, total, ok, perBlock, p, TRIES, admitted,
    E: {
      all: `셋이 고르는 방법을 모두 칸으로 — ‹${total}›칸`,
      block: `서아가 ${CLUBS[0]}일 때 모두 붙는 칸 ‹${perBlock}›개`,
      sum: `${Array(n).fill(perBlock).join(" + ")} = ‹${ok}›`,
      ans: `${total}번 중 ${ok}번 → ‹${ftxt(ok, total)}›`,
      talk: "미리 상의하면 모두 붙어요 → ‹1›",
    },
    M: {
      all: `모든 경우 ${Array(3).fill(n).join(" × ")} = ${total}`,
      ok: `셋이 서로 다른 곳 ${n} × ${n - 1} × ${n - 2} = ${ok}`,
      ans: `{${ok}/${total}} = ‹${ftxt(ok, total)}›`,
      trap: `${Array(3).fill(n).join(" + ")} = ${3 * n} ⟪×r⟫ 함께 고르니 곱의 법칙`,
      talk: "미리 상의하면 ‹1›",
    },
  };
})();

/* ══════════ 4. 「게임의 규칙」 — 셋이 하는 가위바위보 ══════════ */
export const RPS = (() => {
  const HANDS = ["가위", "바위", "보"];
  const ALL = [];
  for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) for (let c = 0; c < 3; c++) {
    const k = new Set([a, b, c]).size;
    ALL.push({ h: [a, b, c], same: k === 1, diff: k === 3, draw: k !== 2 });
  }
  const total = ALL.length, same = ALL.filter((x) => x.same).length, diff = ALL.filter((x) => x.diff).length;   // 27, 3, 6
  const draw = same + diff, dec = total - draw;                                                                  // 9, 18
  const p = frac(dec, total), wrong = frac(total - same, total);                                                 // 2/3, 8/9
  return {
    HANDS, ALL, total, same, diff, draw, dec, p, wrong,
    SHOW: [[2, 2, 2], [0, 1, 2], [1, 1, 0]],            // 예: 보·보·보(비김) / 가위·바위·보(비김) / 바위·바위·가위(승부)
    E: {
      all: `셋이 내는 손 — ‹${total}›가지`,
      same: `모두 같은 손 ‹${same}›가지`,
      diff: `모두 다른 손 ‹${diff}›가지`,
      draw: `비김 ${same} + ${diff} = ${draw} → 승부 ${total} − ${draw} = ‹${dec}›`,
      ans: `${total}번 중 ${dec}번 = ${p[1]}번 중 ${p[0]}번 → ‹${ftxt(dec, total)}›`,
      trap: `모두 같은 손만 빼면 ${total - same}번? ⟪×r⟫`,
      why: "모두 다른 손도 비겨요",
    },
    M: {
      all: `${Array(3).fill(HANDS.length).join(" × ")} = ${total}`,
      draw: `비김 = ${same} + ${HANDS.length} × ${HANDS.length - 1} × ${HANDS.length - 2} = ${draw}`,
      ans: `1 − {${draw}/${total}} = ‹${ftxt(dec, total)}›`,
      trap: `1 − {${same}/${total}} = ${ftxt(total - same, total)} ⟪×r⟫ 모두 다른 경우도 비김`,
    },
  };
})();

/* ══════════ 5. 「축제 서술형」 5번 — 불이 켜지는 간판 ══════════ */
export const SIGN = (() => {
  const W = 100, H = 60, V = 4;                        // 간판 가로 · 세로(cm) · 불빛 P 의 빠르기(1초에 cm)
  const start = (W * H) / 2, rate = (V * H) / 2;        // 3000, 120
  const area = (x) => ((V * x + W) * H) / 2;            // 사다리꼴 APCD = 120x + 3000
  const target = 4800;
  const x = (target - start) / rate;                    // 15
  const CP = V * x, PB = W - CP;                        // 60, 40
  const tri = (PB * H) / 2, rect = W * H;               // 1200, 6000
  const full = W / V;                                   // 25초에 B 도착
  const TABLE = [0, 5, 10, 15].map((s) => [s, area(s)]);
  return {
    W, H, V, start, rate, area, target, x, CP, PB, tri, rect, full, TABLE,
    E: {
      start: `처음에는 삼각형 ACD  ${W} × ${H} ÷ 2 = ${start} cm²`,
      rect: `간판 전체  ${W} × ${H} = ${rect} cm²`,
      dark: `불 꺼진 부분  ${rect} − ${target} = ‹${tri} cm²›`,
      pb1: `PB × ${H} ÷ 2 = ${tri}`,
      pb: `PB = ${tri} × 2 ÷ ${H} = ‹${PB} cm›`,
      time: `CP = ${W} − ${PB} = ${CP} cm,  ${CP} ÷ ${V} = ‹${x}초›`,
      rate: `1초마다 ${V} × ${H} ÷ 2 = ${rate} cm²씩 늘어요`,
      check: `${start} + ${rate} × ${x} = ${target} ⟪✓t⟫`,
      trap: `CP = ${CP} cm ⟪×r⟫ 묻는 것은 P와 B 사이`,
    },
    M: {
      cp: `CP = ${V}x`,
      y: `y = {1/2} × (${V}x + ${W}) × ${H}`,
      y2: `= ‹${rate}x + ${start}›`,
      solve: `${rate}x + ${start} = ${target}  →  x = ${x}`,
      cp2: `CP = ${V} × ${x} = ${CP}`,
      pb: `PB = ${W} − ${CP} = ‹${PB} cm›`,
      trap: `CP = ${CP} cm ⟪×r⟫ 묻는 것은 P와 B 사이의 거리`,
    },
  };
})();

/* ══════════ 6. 「축제 서술형」 3번 — 반티 두 업체 ══════════ */
export const SHIRT = (() => {
  const FEE = 24000, A1 = 6000, B1 = 8000;              // A 업체 디자인비 · 한 벌 값, B 업체 한 벌 값
  const A = (x) => FEE + A1 * x, Bc = (x) => B1 * x;
  const x = FEE / (B1 - A1), y = Bc(x);                 // 12, 96000
  const ans = Math.floor(x) + 1;                         // 13 (x > 12 인 가장 작은 자연수)
  const ROWS = [10, 11, 12, 13, 14].map((k) => [k, A(k), Bc(k)]);
  return {
    FEE, A1, B1, A, B: Bc, x, y, ans, ROWS,
    E: {
      a: `디자인비 ${FEE}원 + 한 벌에 ${A1}원`,
      b: `디자인비 없이 한 벌에 ${B1}원`,
      diff: `한 벌마다 ${B1} − ${A1} = ${B1 - A1}원씩 줄어요`,
      meet1: `${FEE} ÷ ${B1 - A1} = ${x}`,
      meet: `${x}벌에서 둘 다 ${y}원`,
      ans: `${ans}벌부터 A가 싸요 → ‹${ans}벌›`,
      trap: `${x}벌은 두 업체가 같아요 ⟪×r⟫`,
      gap: (n) => FEE + A1 * n - B1 * n,              // A − B (양수면 B 가 쌈)
    },
    M: {
      a: `A : y = ${A1}x + ${FEE}`,
      b: `B : y = ${B1}x`,
      solve: `${B1}x = ${A1}x + ${FEE}  →  x = ${x}`,
      p: `P(${x}, ${y})`,
      ans: `x > ${x}에서 A의 그래프가 아래 → ‹${ans}벌›`,
      trap: `${x}벌은 두 업체가 같아요 ⟪×r⟫`,
    },
  };
})();
