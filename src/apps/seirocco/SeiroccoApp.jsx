// src/apps/seirocco/SeiroccoApp.jsx — 시록고 셸 v3 (기록 중심 재편)
// 본질: 기록. 서고(장서고·문서고·기록고) · 사무(행정, 무료) · 서무(코퍼스, 유료) + 공통 광장(하소·방).
// 내부 해시: #/ 홈 · #/seogo(/:tab) · #/samu(/:id) · #/seomu(/:tab) · #/more
//           #/haso · #/bang · #/my · #/support · #/fonts(관리자)
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import RoleSwitch from "../../shared/RoleSwitch";
import LogoTrigger from "../../shared/LogoTrigger";
import { getMemberships, navigatePath, studentPath } from "../../shared/roles";
import { Kit, useAppHash } from "../../shared/demo";
import Haso from "../../shared/spaces/Haso";
import Bang from "../../shared/spaces/Bang";
import Home from "./pages/Home";
import Seogo from "./pages/Seogo";
import Samu from "./pages/Samu";
import Seomu from "./pages/Seomu";
import My from "./pages/My";
import Support from "./pages/Support";
import Fonts from "./pages/Fonts";
import More from "./pages/More";

const NAV = [["", "홈"], ["seogo", "서고"], ["samu", "사무"], ["seomu", "서무"], ["more", "더보기"]];
const MORE_SET = ["haso", "bang", "my", "support", "fonts", "more"];

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
  const isInstructor = roles.includes("instructor") || adm;
  const isAssistant = !isInstructor && roles.includes("assistant");
  const allowed = isInstructor || isAssistant;

  const PAGES = { "": Home, seogo: Seogo, samu: Samu, seomu: Seomu,
    haso: Haso, bang: Bang, my: My, support: Support, fonts: Fonts, more: More };
  // 조교 제한 모드: 광장과 문의만
  const AST = { "": Home, haso: Haso, bang: Bang, support: Support };
  const Cmp = (isAssistant ? AST[page] : PAGES[page]) || Home;
  const navCur = MORE_SET.includes(page) ? "more" : page;

  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <header style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
          <LogoTrigger handle={<span className="lt-tile">시</span>}
            right={{ tag: "모", label: "학부모앱", go: () => navigatePath("/jongseong") }}
            down={{ tag: <img src="/brand/ashrain_logo.png" alt="학생" />, label: "학생앱",
              go: async () => navigatePath(await studentPath()) }}
            onLogoClick={() => (location.hash = "")} />
          <h1 style={{ fontSize: 19, margin: 0, letterSpacing: ".02em", cursor: "pointer" }}
            onClick={() => (location.hash = "")}>시록고 <span style={{ fontSize: 15, color: "var(--mut)", fontWeight: 400 }}>SEIROCCO</span></h1>
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
              {(isAssistant ? [["", "홈"], ["haso", "하소"], ["bang", "방"], ["support", "문의"]] : NAV).map(([k, l]) => (
                <button key={k} className={"d-tab" + (navCur === k ? " on" : "")}
                  onClick={() => (location.hash = "#/" + k)}>{l}</button>
              ))}
            </div>
            <Cmp param={param} isAssistant={isAssistant} isAdmin={adm} />
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
