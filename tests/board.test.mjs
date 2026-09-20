// node tests/board.test.mjs — 게시판 순수 로직(src/pages/board/boardlib.js) 검사. 실패 시 exit 1.
import assert from "node:assert/strict";
import {
  ROLE_LABELS, roleLabel, roleClass, timeAgo, safeDecode, parseSub, isMissingTable, BOARD_META,
} from "../src/pages/board/boardlib.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}

// ── roleLabel: profiles.role → 한글 배지 ────────────────────────────────────
test("roleLabel — schema.sql 의 role 값(student|teacher|admin) + ui-v3 확장(guardian|trial)", () => {
  assert.equal(roleLabel("student"), "학생");
  assert.equal(roleLabel("teacher"), "강사");
  assert.equal(roleLabel("admin"), "학원");
  assert.equal(roleLabel("guardian"), "학부모");
  assert.equal(roleLabel("trial"), "체험");
});
test("roleLabel — 모르는 값·빈 값은 그대로 노출하지 않고 '회원'", () => {
  assert.equal(roleLabel("superuser"), "회원");
  assert.equal(roleLabel(""), "회원");
  assert.equal(roleLabel(null), "회원");
  assert.equal(roleLabel(undefined), "회원");
});
test("ROLE_LABELS — 정확히 5개 역할만 정의", () => {
  assert.deepEqual(Object.keys(ROLE_LABELS).sort(), ["admin", "guardian", "student", "teacher", "trial"]);
});

// ── roleClass: 배지 색 클래스 (학생 teal · 강사 indigo · 학부모 amber · 학원 slate) ──
test("roleClass — 알려진 역할은 bd-r-<role>, 그 외는 bd-r-etc", () => {
  assert.equal(roleClass("student"), "bd-r-student");
  assert.equal(roleClass("teacher"), "bd-r-teacher");
  assert.equal(roleClass("guardian"), "bd-r-guardian");
  assert.equal(roleClass("admin"), "bd-r-admin");
  assert.equal(roleClass("trial"), "bd-r-trial");
  assert.equal(roleClass("hacker"), "bd-r-etc");
  assert.equal(roleClass(null), "bd-r-etc");
  assert.equal(roleClass("hasOwnProperty"), "bd-r-etc"); // 프로토타입 오염 방어
});

// ── timeAgo ────────────────────────────────────────────────────────────────
const NOW = Date.parse("2026-09-19T12:00:00+09:00");
const ago = (sec) => new Date(NOW - sec * 1000).toISOString();
test("timeAgo — 1분 미만은 방금 전", () => {
  assert.equal(timeAgo(ago(0), NOW), "방금 전");
  assert.equal(timeAgo(ago(59), NOW), "방금 전");
});
test("timeAgo — 분·시간·일 경계", () => {
  assert.equal(timeAgo(ago(60), NOW), "1분 전");
  assert.equal(timeAgo(ago(59 * 60), NOW), "59분 전");
  assert.equal(timeAgo(ago(3600), NOW), "1시간 전");
  assert.equal(timeAgo(ago(23 * 3600 + 59 * 60), NOW), "23시간 전");
  assert.equal(timeAgo(ago(86400), NOW), "1일 전");
  assert.equal(timeAgo(ago(6 * 86400 + 3600), NOW), "6일 전");
});
test("timeAgo — 7일 이상은 yy.M.d 날짜", () => {
  assert.match(timeAgo(ago(8 * 86400), NOW), /^\d{2}\.\d{1,2}\.\d{1,2}$/);
  assert.match(timeAgo("2026-01-02T00:00:00+09:00", NOW), /^26\.\d{1,2}\.\d{1,2}$/);
});
test("timeAgo — 미래값(시계 오차)은 방금 전, 잘못된 값은 빈 문자열", () => {
  assert.equal(timeAgo(ago(-120), NOW), "방금 전");
  assert.equal(timeAgo("garbage", NOW), "");
  assert.equal(timeAgo("", NOW), "");
  assert.equal(timeAgo(null, NOW), "");
});

// ── parseSub: "#/board/" 뒤 문자열 → 화면 ──────────────────────────────────
test("parseSub — ''·notice → 공지 목록, community → 커뮤니티 목록", () => {
  assert.deepEqual(parseSub(""), { view: "list", board: "notice" });
  assert.deepEqual(parseSub("notice"), { view: "list", board: "notice" });
  assert.deepEqual(parseSub("notice/"), { view: "list", board: "notice" });
  assert.deepEqual(parseSub("community"), { view: "list", board: "community" });
});
test("parseSub — qna → 기존 질문게시판 임베드", () => {
  assert.deepEqual(parseSub("qna"), { view: "qna" });
});
test("parseSub — write, write?board=…", () => {
  assert.deepEqual(parseSub("write"), { view: "write", board: "community" });
  assert.deepEqual(parseSub("write?board=notice"), { view: "write", board: "notice" });
  assert.deepEqual(parseSub("write?board=community"), { view: "write", board: "community" });
  assert.deepEqual(parseSub("write?board=bogus"), { view: "write", board: "community" });
  assert.deepEqual(parseSub("write?x=1&board=notice"), { view: "write", board: "notice" });
});
test("parseSub — post/<id> → 글 상세", () => {
  assert.deepEqual(parseSub("post/123"), { view: "post", id: "123" });
  assert.deepEqual(parseSub("post/9007199254"), { view: "post", id: "9007199254" });
});
test("parseSub — 그 밖의 값은 레거시 질문 딥링크 (uuid, 인코딩 포함)", () => {
  const uuid = "0b6f3a52-9a1e-4a7f-8c2d-5f1e2a3b4c5d";
  assert.deepEqual(parseSub(uuid), { view: "legacy", id: uuid });
  assert.deepEqual(parseSub("abc%2Fdef"), { view: "legacy", id: "abc/def" });
  assert.deepEqual(parseSub("%ZZbad"), { view: "legacy", id: "%ZZbad" }); // 디코드 실패는 원문 유지
  assert.equal(parseSub(undefined).view, "list"); // 방어
});
test("safeDecode — 실패 시 원문", () => {
  assert.equal(safeDecode("a%20b"), "a b");
  assert.equal(safeDecode("%E0%A4%A"), "%E0%A4%A");
});

// ── isMissingTable: 마이그레이션 미적용 판정 ────────────────────────────────
test("isMissingTable — 42P01/PGRST205/메시지 패턴은 true", () => {
  assert.equal(isMissingTable({ code: "42P01", message: "x" }), true);
  assert.equal(isMissingTable({ code: "PGRST205", message: "x" }), true);
  assert.equal(isMissingTable({ message: 'relation "public.posts" does not exist' }), true);
  assert.equal(isMissingTable({ message: "Could not find the table 'public.posts' in the schema cache" }), true);
});
test("isMissingTable — 그 밖의 에러·빈 값은 false", () => {
  assert.equal(isMissingTable({ code: "42501", message: "row-level security policy violation" }), false);
  assert.equal(isMissingTable({ code: "23505", message: "duplicate key" }), false);
  assert.equal(isMissingTable(null), false);
  assert.equal(isMissingTable(undefined), false);
});

// ── BOARD_META ─────────────────────────────────────────────────────────────
test("BOARD_META — 공지·커뮤니티 각각 이름·빈 상태 문구", () => {
  assert.equal(BOARD_META.notice.name, "공지");
  assert.equal(BOARD_META.community.name, "커뮤니티");
  assert.ok(BOARD_META.notice.empty && BOARD_META.community.empty);
  assert.notEqual(BOARD_META.notice.empty, BOARD_META.community.empty);
});

console.log(failed ? `\n${failed}/${n} FAILED` : `\nall ${n} passed`);
process.exit(failed ? 1 : 0);
