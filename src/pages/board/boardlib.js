// src/pages/board/boardlib.js — 게시판 순수 로직 (React·Supabase 의존 없음, tests/board.test.mjs 가 검사)

// profiles.role → 한글 배지 라벨. 실제 값은 supabase/schema.sql(student|teacher|admin) 기준이며
// ui-v3 배치에서 guardian·trial 이 추가될 수 있어 함께 매핑한다. 모르는 값은 '회원'으로만 표기.
export const ROLE_LABELS = {
  student: "학생",
  teacher: "강사",
  admin: "학원",
  guardian: "학부모",
  trial: "체험",
};

export function roleLabel(role) {
  return ROLE_LABELS[role] || "회원";
}

// 배지 색상 클래스 키 — CSS 는 bd-r-<key> 로 정의(학생 teal · 강사 indigo · 학부모 amber · 학원 slate).
export function roleClass(role) {
  return Object.prototype.hasOwnProperty.call(ROLE_LABELS, role) ? "bd-r-" + role : "bd-r-etc";
}

// 상대 시간. now 는 ms 타임스탬프(테스트 주입용). 잘못된 입력은 빈 문자열.
export function timeAgo(iso, now = Date.now()) {
  if (!iso) return "";
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return "";
  let s = Math.floor((now - t) / 1000);
  if (s < 0) s = 0; // 시계 오차·미래값은 방금 전으로
  if (s < 60) return "방금 전";
  if (s < 3600) return Math.floor(s / 60) + "분 전";
  if (s < 86400) return Math.floor(s / 3600) + "시간 전";
  if (s < 86400 * 7) return Math.floor(s / 86400) + "일 전";
  const d = new Date(t);
  return `${String(d.getFullYear()).slice(2)}.${d.getMonth() + 1}.${d.getDate()}`;
}

export function safeDecode(s) {
  try { return decodeURIComponent(s); } catch { return s; }
}

// `#/board/` 뒤 문자열(sub, 디코드 전) → 화면 결정.
//   ''|'notice' → {view:'list', board:'notice'} · 'community' → {view:'list', board:'community'}
//   'qna' → {view:'qna'} · 'write[?board=…]' → {view:'write', board} · 'post/<id>' → {view:'post', id}
//   그 밖 → {view:'legacy', id} (기존 질문게시판 딥링크 #/board/<qna uuid>)
export function parseSub(sub) {
  const raw = typeof sub === "string" ? sub : "";
  const qi = raw.indexOf("?");
  const path = (qi >= 0 ? raw.slice(0, qi) : raw).replace(/\/+$/, "");
  const query = qi >= 0 ? raw.slice(qi + 1) : "";
  if (path === "" || path === "notice") return { view: "list", board: "notice" };
  if (path === "community") return { view: "list", board: "community" };
  if (path === "qna") return { view: "qna" };
  if (path === "write") {
    let board = "community";
    for (const pair of query.split("&")) {
      const [k, v] = pair.split("=");
      if (k === "board" && (v === "notice" || v === "community")) board = v;
    }
    return { view: "write", board };
  }
  if (path.startsWith("post/")) {
    const id = safeDecode(path.slice(5));
    if (id) return { view: "post", id };
  }
  return { view: "legacy", id: safeDecode(raw) };
}

// 테이블 미존재(마이그레이션 미적용) 판정 — 42P01(postgres) / PGRST205(postgrest 스키마 캐시).
export function isMissingTable(error) {
  if (!error) return false;
  const code = error.code || "";
  if (code === "42P01" || code === "PGRST205") return true;
  const msg = String(error.message || "");
  return /does not exist|schema cache/i.test(msg);
}

// 게시판 메타(제목·빈 상태 문구) — 목록·글쓰기 화면 공용.
export const BOARD_META = {
  notice: { name: "공지", icon: "📢", empty: "아직 등록된 공지가 없어요." },
  community: { name: "커뮤니티", icon: "💬", empty: "아직 글이 없어요 — 첫 글을 남겨보세요!" },
};
