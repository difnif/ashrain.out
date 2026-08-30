// src/apps/jongseong/JongseongApp.jsx — 학부모앱 셸 v2 (전 페이지 골격 + 데모 라우팅)
// 반감시 원칙: 점수·문항으로 가는 경로 자체가 없다. 홈은 서신·응원·일정 중심.
// 내부 해시: #/ 홈 · #/letters(/:id) · #/cheer · #/calendar · #/more
//           #/board · #/pay · #/gift · #/survey · #/link
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import RoleSwitch from "../../shared/RoleSwitch";
import { getMemberships, navigatePath, studentPath } from "../../shared/roles";
import { Kit, useAppHash } from "../../shared/demo";
import Home from "./pages/Home";
import Letters from "./pages/Letters";
import Cheer from "./pages/Cheer";
import Calendar from "./pages/Calendar";
import Board from "./pages/Board";
import Pay from "./pages/Pay";
import Gift from "./pages/Gift";
import Survey from "./pages/Survey";
import Link from "./pages/Link";
import More from "./pages/More";

const NAV = [["", "홈"], ["letters", "서신"], ["cheer", "응원"], ["calendar", "일정"], ["more", "더보기"]];
const MORE_SET = ["board", "pay", "gift", "survey", "link", "more"];

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
  const PAGES = { "": Home, letters: Letters, cheer: Cheer, calendar: Calendar,
    board: Board, pay: Pay, gift: Gift, survey: Survey, link: Link, more: More };
  const Cmp = PAGES[page] || Home;
  const navCur = MORE_SET.includes(page) ? "more" : page;

  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <header style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
          <h1 style={{ fontSize: 19, margin: 0, letterSpacing: ".02em", cursor: "pointer" }}
            onClick={() => (location.hash = "")}>종성</h1>
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
            <Cmp param={param} />
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
