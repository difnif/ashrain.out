// src/apps/seirocco/SeiroccoApp.jsx — 강사앱 셸 v2 (전 페이지 골격 + 데모 라우팅)
// 내부 해시: #/ 홈 · #/students(/:id) · #/predict · #/contracts · #/interview
//           #/career · #/survey · #/verify · #/support · #/more
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import RoleSwitch from "../../shared/RoleSwitch";
import { getMemberships, navigatePath, studentPath } from "../../shared/roles";
import { Kit, useAppHash } from "../../shared/demo";
import Home from "./pages/Home";
import Students from "./pages/Students";
import StudentDetail from "./pages/StudentDetail";
import Predict from "./pages/Predict";
import Interview from "./pages/Interview";
import Contracts from "./pages/Contracts";
import Career from "./pages/Career";
import Survey from "./pages/Survey";
import Verify from "./pages/Verify";
import Support from "./pages/Support";
import More from "./pages/More";

const NAV = [["", "홈"], ["students", "학생"], ["predict", "예측"], ["contracts", "계약"], ["more", "더보기"]];
const MORE_SET = ["interview", "career", "survey", "verify", "support", "more"];

export default function SeiroccoApp() {
  const [ms, setMs] = useState(null);
  const [adm, setAdm] = useState(false);
  const [page, param] = useAppHash();

  useEffect(() => {
    let alive = true;
    (async () => {
      const m = await getMemberships();
      let ad = false;
      const { data: s } = await supabase.auth.getSession();
      const uid = s?.session?.user?.id;
      if (uid) {
        const { data: p } = await supabase.from("profiles").select("role").eq("id", uid).maybeSingle();
        ad = p?.role === "admin";
      }
      if (alive) { setMs(m); setAdm(ad); }
    })();
    return () => { alive = false; };
  }, []);

  const roles = (ms || []).map((m) => m.role);
  const isInstructor = roles.includes("instructor") || adm; // 운영자는 전 앱 열람
  const isAssistant = !isInstructor && roles.includes("assistant");
  const allowed = isInstructor || isAssistant;

  const PAGES = {
    "": Home, students: param ? StudentDetail : Students, predict: Predict,
    contracts: Contracts, interview: Interview, career: Career, survey: Survey,
    verify: Verify, support: Support, more: More,
  };
  // 조교 제한 모드: 1층 화면만
  const AST = { "": Home, interview: Interview, support: Support, more: More };
  const Cmp = (isAssistant ? AST[page] : PAGES[page]) || Home;
  const navCur = MORE_SET.includes(page) ? "more" : page;

  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <header style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
          <h1 style={{ fontSize: 19, margin: 0, letterSpacing: ".02em", cursor: "pointer" }}
            onClick={() => (location.hash = "")}>세이로코</h1>
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
          <>
            <div className="d-tabs" style={{ marginBottom: 10 }}>
              {(isAssistant ? [["", "홈"], ["interview", "면담"], ["support", "문의"]] : NAV).map(([k, l]) => (
                <button key={k} className={"d-tab" + (navCur === k ? " on" : "")}
                  onClick={() => (location.hash = "#/" + k)}>{l}</button>
              ))}
            </div>
            <Cmp param={param} isAssistant={isAssistant} />
          </>
        ) : (
          <div className="ap-card">
            <p className="ap-sec">안내</p>
            <p style={{ fontSize: 14.5, margin: "0 0 6px", fontWeight: 700 }}>강사 권한이 아직 없어요</p>
            <p style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.7, margin: "0 0 14px" }}>
              운영자가 권한을 부여하면 이곳이 열려요.
            </p>
            <button className="ap-btn pri" onClick={async () => navigatePath(await studentPath())}>학생앱으로 가기</button>
          </div>
        )}
      </div>
    </div>
  );
}
