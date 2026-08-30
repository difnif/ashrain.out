// src/apps/jongseong/JongseongApp.jsx — 학부모앱 셸 (P0: 빈 홈)
// 반감시 원칙: 점수·문항으로 가는 경로 자체를 만들지 않는다. 홈은 서신·응원·일정 중심(P2에서 채움).
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import RoleSwitch from "../../shared/RoleSwitch";
import { getMemberships, navigatePath, studentPath } from "../../shared/roles";

export default function JongseongApp() {
  const [ms, setMs] = useState(null);
  useEffect(() => {
    let alive = true;
    getMemberships().then((m) => { if (alive) setMs(m); });
    return () => { alive = false; };
  }, []);

  const allowed = (ms || []).some((m) => m.role === "guardian");

  return (
    <div className="ap-shell">
      <div className="ap-wrap">
        <header style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 18 }}>
          <h1 style={{ fontSize: 19, margin: 0, letterSpacing: ".02em" }}>종성</h1>
          <span style={{ flex: 1 }} />
          <button className="ap-btn" onClick={async () => { await supabase.auth.signOut(); navigatePath("/"); }}>
            로그아웃
          </button>
        </header>

        <RoleSwitch current="guardian" />

        {ms === null ? null : allowed ? (
          <div className="ap-card">
            <p className="ap-sec">홈</p>
            <p style={{ fontSize: 14.5, margin: "0 0 6px", fontWeight: 700 }}>주간 서신이 준비되고 있어요</p>
            <p style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.7, margin: 0 }}>
              자녀와 연결되면 매주 서신이 도착해요. 응원과 일정도 이곳에서 열려요.
            </p>
          </div>
        ) : (
          <div className="ap-card">
            <p className="ap-sec">안내</p>
            <p style={{ fontSize: 14.5, margin: "0 0 6px", fontWeight: 700 }}>학부모 연결이 아직 없어요</p>
            <p style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.7, margin: "0 0 14px" }}>
              자녀 연결 기능이 곧 열려요. 지금은 운영자가 연결해 드려요.
            </p>
            <button className="ap-btn pri"
              onClick={async () => navigatePath(await studentPath())}>학생앱으로 가기</button>
          </div>
        )}
      </div>
    </div>
  );
}
