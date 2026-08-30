// src/apps/seirocco/SeiroccoApp.jsx — 강사앱 셸 (P0: 빈 홈)
// 층 게이트: instructor(강사) = 정상 진입 / assistant(아전 조교) = 제한 모드 / 그 외 = 안내.
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import RoleSwitch from "../../shared/RoleSwitch";
import { getMemberships, navigatePath, studentPath } from "../../shared/roles";

export default function SeiroccoApp() {
  const [ms, setMs] = useState(null);
  useEffect(() => {
    let alive = true;
    getMemberships().then((m) => { if (alive) setMs(m); });
    return () => { alive = false; };
  }, []);

  const roles = (ms || []).map((m) => m.role);
  const isInstructor = roles.includes("instructor");
  const isAssistant = !isInstructor && roles.includes("assistant");
  const allowed = isInstructor || isAssistant;

  return (
    <div className="ap-shell">
      <div className="ap-wrap">
        <header style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 18 }}>
          <h1 style={{ fontSize: 19, margin: 0, letterSpacing: ".02em" }}>세이로코</h1>
          {isAssistant && (
            <span style={{ fontSize: 11, fontWeight: 800, color: "var(--ac)",
              border: "1px solid var(--ac)", borderRadius: 999, padding: "3px 9px" }}>조교 모드</span>
          )}
          <span style={{ flex: 1 }} />
          <button className="ap-btn" onClick={async () => { await supabase.auth.signOut(); navigatePath("/"); }}>
            로그아웃
          </button>
        </header>

        <RoleSwitch current={isAssistant ? "assistant" : "instructor"} />

        {ms === null ? null : allowed ? (
          <div className="ap-card">
            <p className="ap-sec">홈</p>
            <p style={{ fontSize: 14.5, margin: "0 0 6px", fontWeight: 700 }}>준비 중이에요</p>
            <p style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.7, margin: 0 }}>
              {isAssistant
                ? "조교 기능이 순서대로 열려요. 지금은 학생앱에서 하던 활동을 계속해 주세요."
                : "계약, 내 학생, 예측–확인이 순서대로 열려요."}
            </p>
          </div>
        ) : (
          <div className="ap-card">
            <p className="ap-sec">안내</p>
            <p style={{ fontSize: 14.5, margin: "0 0 6px", fontWeight: 700 }}>강사 권한이 아직 없어요</p>
            <p style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.7, margin: "0 0 14px" }}>
              운영자가 권한을 부여하면 이곳이 열려요.
            </p>
            <button className="ap-btn pri"
              onClick={async () => navigatePath(await studentPath())}>학생앱으로 가기</button>
          </div>
        )}
      </div>
    </div>
  );
}
