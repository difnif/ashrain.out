// src/shared/roles.js — 역할·경로 유틸 (P0 셸)
// memberships 테이블이 아직 없거나 조회가 실패해도 앱이 죽지 않도록 전부 방어적으로 처리.
import { supabase } from "../supabaseClient";

export const ROLE_LABELS = { student: "학생", instructor: "강사", guardian: "학부모", assistant: "조교" };

// 역할 → 1단계 경로. 학생은 명예 플래그(honor)에 따라 /running.
export function rolePath(role, honor = false) {
  if (role === "instructor" || role === "assistant") return "/seirocco";
  if (role === "guardian") return "/jongseong";
  return honor ? "/running" : "/walking";
}

// 리로드 없는 경로 이동. PathRouter가 pathchange를 듣는다.
export function navigatePath(path) {
  history.pushState(null, "", path);
  window.dispatchEvent(new Event("pathchange"));
}

// 학생앱 내부 해시로 가는 절대 경로 — 항상 "현재 사용자" 자격 기준으로 생성.
// 공유 링크·전환 버튼이 타인의 자격(/running)을 노출하지 않게 하는 정규화 지점.
let _honorCache = null;
export async function studentPath(hash = "") {
  if (_honorCache === null) {
    try {
      const { data: s } = await supabase.auth.getSession();
      const uid = s?.session?.user?.id;
      if (!uid) _honorCache = false;
      else {
        const { data, error } = await supabase
          .from("profiles").select("honor_path").eq("id", uid).maybeSingle();
        _honorCache = !error && !!data?.honor_path;
      }
    } catch { _honorCache = false; }
  }
  const tail = hash ? (hash.startsWith("#") ? hash : "#" + hash) : "";
  return rolePath("student", _honorCache) + tail;
}

// 내 역할 목록. 테이블 미존재·행 없음이면 학생 단일로 폴백.
export async function getMemberships() {
  try {
    const { data: s } = await supabase.auth.getSession();
    const uid = s?.session?.user?.id;
    if (!uid) return [];
    const { data, error } = await supabase
      .from("memberships").select("role, academy_code, rank, status")
      .eq("user_id", uid).eq("status", "active");
    if (error || !data || data.length === 0) return [{ role: "student" }];
    return data;
  } catch { return [{ role: "student" }]; }
}

// 마지막 역할 기록 (관문 리다이렉트 근거 — user_metadata, localStorage 금지)
export async function setLastRole(role) {
  try { await supabase.auth.updateUser({ data: { last_role: role } }); } catch { /* 다음 전환에서 재시도 */ }
}

// 역할 전환 = 기록 + 해당 앱으로 리로드 없이 이동
export async function switchRole(role) {
  await setLastRole(role);
  if (role === "student") navigatePath(await studentPath(""));
  else navigatePath(rolePath(role));
}
