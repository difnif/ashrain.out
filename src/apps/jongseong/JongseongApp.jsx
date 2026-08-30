// src/apps/jongseong/JongseongApp.jsx — 학부모앱 셸 v3 (소통 허브 재편)
// 공통 공간(하소·방)은 shared/spaces에서 임포트 — 추후 학생앱·시록고도 같은 컴포넌트를 쓴다.
// 내부 해시: #/ 홈 · #/haso · #/maru · #/bang · #/more
//           #/firewood(밥 짓는 소리) · #/stoke(아궁이) · #/offering(정안수) · #/reading(글 읽는 소리)
//           #/baekdol · #/pigeon · #/link · #/vault(관리자)
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import RoleSwitch from "../../shared/RoleSwitch";
import LogoTrigger from "../../shared/LogoTrigger";
import { getMemberships, navigatePath, studentPath } from "../../shared/roles";
import { Kit, useAppHash } from "../../shared/demo";
import Haso from "../../shared/spaces/Haso";
import Bang from "../../shared/spaces/Bang";
import Home from "./pages/Home";
import Maru from "./pages/Maru";
import Firewood from "./pages/Firewood";
import Stoke from "./pages/Stoke";
import Offering from "./pages/Offering";
import Reading from "./pages/Reading";
import Baekdol from "./pages/Baekdol";
import Pigeon from "./pages/Pigeon";
import My from "./pages/My";
import Vault from "./pages/Vault";
import More from "./pages/More";

const NAV = [["", "홈"], ["haso", "하소"], ["maru", "마루"], ["bang", "방"], ["more", "더보기"]];
const MORE_SET = ["firewood", "stoke", "offering", "reading", "baekdol", "pigeon", "my", "vault", "more"];

export default function JongseongApp() {
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

  const allowed = adm || (ms || []).some((m) => m.role === "guardian");
  const PAGES = { "": Home, haso: Haso, maru: Maru, bang: Bang,
    firewood: Firewood, stoke: Stoke, offering: Offering, reading: Reading,
    baekdol: Baekdol, pigeon: Pigeon, my: My, vault: Vault, more: More };
  const Cmp = PAGES[page] || Home;
  const navCur = MORE_SET.includes(page) ? "more" : page;

  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <header style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
          <LogoTrigger handle={<span className="lt-tile">종</span>}
            right={{ tag: "강", label: "시록고", go: () => navigatePath("/seirocco") }}
            down={{ tag: <img src="/brand/ashrain_logo.png" alt="학생" />, label: "학생앱",
              go: async () => navigatePath(await studentPath()) }}
            onLogoClick={() => (location.hash = "")} />
          <h1 style={{ fontSize: 19, margin: 0, letterSpacing: ".02em", cursor: "pointer" }}
            onClick={() => (location.hash = "")}>종성 <span style={{ fontSize: 15, color: "var(--mut)", fontWeight: 400 }}>JONGSEONG</span></h1>
          <span style={{ flex: 1 }} />
          <button className="ap-btn" onClick={async () => { await supabase.auth.signOut(); navigatePath("/"); }}>
            로그아웃
          </button>
        </header>

        <RoleSwitch current="guardian" />

        {ms === null ? null : allowed ? (
          <>
            <div className="d-tabs" style={{ marginBottom: 10 }}>
              {NAV.map(([k, l]) => (
                <button key={k} className={"d-tab" + (navCur === k ? " on" : "")}
                  onClick={() => (location.hash = "#/" + k)}>{l}</button>
              ))}
            </div>
            <Cmp param={param} isAdmin={adm} />
          </>
        ) : (
          <div className="ap-card">
            <p className="ap-sec">안내</p>
            <p style={{ fontSize: 14.5, margin: "0 0 6px", fontWeight: 700 }}>학부모 연결이 아직 없어요</p>
            <p style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.7, margin: "0 0 14px" }}>
              자녀 연결이 확인되면 이곳이 열려요.
            </p>
            <button className="ap-btn pri" onClick={async () => navigatePath(await studentPath())}>학생앱으로 가기</button>
          </div>
        )}
      </div>
    </div>
  );
}
