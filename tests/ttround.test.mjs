// 강사도구 — 2차를 시작한 뒤에도 1차(앞 차) 결과 고치기: 차 순서로 고르는 지금 결과 · 틀린 적 판정 (node --test tests/ttround.test.mjs)
import { test } from "node:test";
import assert from "node:assert/strict";
import { currentMarks, roundMarks, roundsInfo, gradingStats, everWrong, resultBefore, effectiveMarks } from "../src/apps/seirocco/tt/logic.js";

// 회차 1·2 = 1차(처음 풀기 + 이어서), 3 = 2차(다시 풀기 4 · 5번)
const sessions = [
  { no: 1, round: 1, kind: "solve", targets: null },
  { no: 2, round: 1, kind: "solve", targets: null },
  { no: 3, round: 2, kind: "retry", targets: [4, 5] },
];
let id = 0;
const mk = (session_no, seq, result, answer = "") => ({ id: ++id, session_no, seq, result, answer });

test("앞 차를 고친 기록은 id 가 커도 늦은 차 결과를 덮지 않음", () => {
  id = 0;
  const marks = [mk(1, 1, "O"), mk(1, 2, "O"), mk(1, 3, "O"), mk(1, 4, "X"), mk(2, 5, "U"),
    mk(3, 4, "O"), // 2차에서 4번 맞힘
    mk(2, 4, "X", "고친 답"), // 2차를 시작한 뒤 1차 4번을 다시 매김(id 가 가장 큼)
    mk(2, 3, "X")]; // 1차 3번 O → X 로 고침(2차 대상 아님)
  const cur = currentMarks(marks, sessions);
  assert.equal(cur.get(4).result, "O", "4번 최종 = 2차 결과");
  assert.equal(cur.get(4).round, 2);
  assert.equal(cur.get(3).result, "X", "3번 최종 = 고친 1차 결과");
  assert.equal(cur.get(5).result, "U", "5번은 2차에서 안 매김 → 1차 결과");
  const r1 = roundMarks(marks, sessions).get(1);
  assert.equal(r1.get(4).answer, "고친 답", "1차 결과 = 1차의 마지막 기록");
  assert.equal(r1.get(3).result, "X");
  const info = roundsInfo(sessions, marks, [1, 2, 3, 4, 5]);
  assert.deepEqual([info[0].summary.O, info[0].summary.X, info[0].summary.U], [2, 2, 1], "1차 요약은 고친 결과로");
  assert.deepEqual([info[1].summary.total, info[1].summary.O, info[1].summary.none], [2, 1, 1], "2차 요약은 그대로");
  const st = gradingStats(marks, sessions, 5);
  assert.deepEqual([st.summary.O, st.summary.X, st.summary.U], [3, 1, 1], "최종");
  assert.deepEqual([st.summary1.O, st.summary1.X], [2, 2], "1차 점수");
});

test("이제까지 쌓인 기록(차가 늦을수록 id 도 큼)은 전과 같은 결과", () => {
  id = 0;
  const marks = [mk(1, 1, "X"), mk(1, 1, "O"), mk(1, 2, "X"), mk(2, 3, "U"), mk(3, 2, "O"), mk(3, 2, "X")];
  const byId = new Map();
  for (const m of [...marks].sort((a, b) => a.id - b.id)) byId.set(m.seq, m.result);
  const cur = currentMarks(marks, sessions);
  for (const [seq, r] of byId) assert.equal(cur.get(seq).result, r, `${seq}번`);
});

test("틀린 적 = 어느 차든 그 차의 마지막 결과가 X", () => {
  id = 0;
  const marks = [
    mk(1, 1, "X"), mk(1, 1, "O"), // 같은 차에서 X 를 잘못 눌렀다 고침 → 틀린 적 없음
    mk(1, 2, "X"), mk(3, 2, "O"), // 1차 X · 2차 O → 그 채점에서 한 번 틀림
    mk(1, 4, "X"), mk(3, 4, "O"), mk(2, 4, "O"), // 1차 X 를 2차 뒤에 O 로 고침 → 틀린 적 없음
    mk(1, 5, "O"), mk(3, 5, "X"), // 2차에서 틀림
  ];
  assert.deepEqual([...everWrong(marks, sessions)].sort(), [2, 5]);
});

test("다음 차는 앞 차를 따름: 다시 풀기 차의 기록은 그 차 다시 풀 문항 것만 셈", () => {
  id = 0;
  const ss = [{ no: 1, round: 1, kind: "solve", targets: null }, { no: 2, round: 2, kind: "retry", targets: [4] }];
  const marks = [mk(1, 4, "X"), mk(1, 5, "X"), mk(2, 4, "O"), mk(2, 5, "O")]; // 5번은 1차를 고쳐 2차에서 빠졌다가 …
  assert.deepEqual(effectiveMarks(marks, ss).map((m) => m.id), [1, 2, 3]);
  assert.equal(currentMarks(marks, ss).get(5).result, "X", "2차 대상이 아니면 2차 기록은 셈에서 빠짐");
  assert.equal(roundMarks(marks, ss).get(2).has(5), false);
  const info = roundsInfo(ss, marks, [1, 2, 3, 4, 5]);
  assert.deepEqual([info[1].summary.total, info[1].summary.O], [1, 1]);
  const ss2 = [ss[0], { ...ss[1], targets: [4, 5] }];
  assert.equal(currentMarks(marks, ss2).get(5).result, "O", "다시 들어오면 2차 기록이 다시 보임");
  const ss3 = [ss[0], { ...ss[1], targets: [4, 5, 6] }];
  assert.equal(roundsInfo(ss3, marks, [1, 2, 3, 4, 5, 6])[1].summary.none, 1, "새로 들어간 6번은 2차 남음");
});

test("앞 차까지의 결과", () => {
  const rounds = [{ round: 1, result: "X" }, { round: 2, result: "O" }, { round: 3, result: "" }];
  assert.equal(resultBefore(rounds, 2), "X");
  assert.equal(resultBefore(rounds, 3), "O");
  assert.equal(resultBefore(rounds, 1), "");
  assert.equal(resultBefore([], 2), "");
});

test("넘어감(P) — 셈에서 따로, 다시 풀 문항(n_retry)에 넣지 않음, 나중에 매기면 그 결과", async () => {
  const { summarize, gradingStats } = await import("../src/apps/seirocco/tt/logic.js");
  const s = summarize([{ result: "O" }, { result: "X" }, { result: "P" }, { result: "P" }, { result: "U" }, {}]);
  assert.deepEqual([s.O, s.X, s.U, s.P, s.none, s.total], [1, 1, 1, 2, 1, 6]);
  const sessions = [{ no: 1, round: 1, kind: "solve" }];
  const marks = [
    { id: 1, seq: 1, result: "O", session_no: 1 }, { id: 2, seq: 2, result: "X", session_no: 1 },
    { id: 3, seq: 3, result: "P", session_no: 1 }, { id: 4, seq: 4, result: "P", session_no: 1 },
    { id: 5, seq: 4, result: "O", session_no: 1 },          // 넘긴 뒤 풀어 와서 O
  ];
  const st = gradingStats(marks, sessions, 4);
  assert.deepEqual([st.summary.O, st.summary.X, st.summary.P, st.summary.none], [2, 1, 1, 0]);
  assert.equal(st.n_retry, 1);                                // 넘어감은 다시 풀 문항이 아님
});
