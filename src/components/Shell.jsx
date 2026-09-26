// 학생앱 셸 (ui-v3 → 우물 v1) — 큰 카테고리 4개는 하단 고정 탭바, 하위 카테고리는 상단 고정 서브탭(무신사식).
// 탭바 중앙에는 「우물」 — 시간·날씨 따라 변하는 원형 버튼(카메라 기능 런처). 크기·이미지는 #/admin/well 에서.
// 브라우즈 화면(대시보드·공부하기·학습 도구·게시판 목록)에서만 그려지고,
// 기능 화면(개념 뷰어·문항 풀이·시험·글쓰기 등)은 FeatureBar(⌂·←·컨텍스트 버튼)만 쓴다 — App.jsx 가 shellMode 로 가른다.
// 홈 복귀 = 「대시보드」 탭. 로고의 모/강 앱 전환 토글은 그대로 유지(사용자 확정).
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";
import LogoTrigger from "../shared/LogoTrigger";
import { navigatePath } from "../shared/roles";
import { BETA } from "../lib/beta";
import { WellButton, WellSheet, useWellCfg, WELL_CSS } from "./Well";
import { runningJobs, unseenJobs } from "../lib/photoJobs";
import { warmStudy } from "../lib/studyCache";

// 게시판 탭은 「기록」으로 대체(사용자 확정 2026-09-20) — 게시판은 종성 작업 때 정교화 후 재공개.
export const TABS = [
  ["🏠", "대시보드", "#/"],
  ["📚", "공부하기", "#/study"],
  ["🧰", "학습 도구", "#/tools"],
  ["🗂", "기록", "#/records"],
];

const SUBTABS = {
  study: [["개념 공부", "#/study/concept"], ["연습문제", "#/study/practice"], ["시험 보기", "#/study/exam"]],
  tools: [["전체", "#/tools"], ["서술형", "#/tools/essay"], ["사진 힌트", "#/tools/hint"],
          ["문장 해설", "#/tools/read"], ["표시 연습", "#/tools/mark"], ["풀이 검사", "#/tools/check"]],
  board: [["공지", "#/board/notice"], ["커뮤니티", "#/board/community"], ["질문", "#/board/qna"]],
};

/** 현재 해시의 큰 탭 */
export function tabOf(hash) {
  if (hash.startsWith("#/study")) return "study";
  if (hash.startsWith("#/tools")) return "tools";
  if (hash.startsWith("#/records")) return "records";
  if (hash.startsWith("#/board")) return "board";
  return "dash";
}

const BOARD_BROWSE = ["", "notice", "community", "qna"];

/** 셸(탭바·서브탭)을 그릴 화면인가 — 아니면 기능 화면(FeatureBar만) */
export function shellMode(hash) {
  const h = (hash || "").split("?")[0];
  if (h === "" || h === "#" || h === "#/") return "browse";
  if (h.startsWith("#/study") || h.startsWith("#/tools") || h.startsWith("#/records")) return "browse";
  if (h.startsWith("#/board")) {
    const seg = h.replace(/^#\/board\/?/, "").split("/")[0];
    return BOARD_BROWSE.includes(seg) ? "browse" : "feature";
  }
  return "feature";
}

/** 서브탭 활성 판정 — 기본 탭(#/study, #/tools)은 첫 항목 활성 */
function subOn(hash, to, list) {
  const h = hash.split("?")[0].replace(/\/$/, "");
  const t = to.replace(/\/$/, "");
  if (h === t) return true;
  if (h.startsWith(t + "/")) return true;
  // 탭 루트(#/study 등)면 첫 서브탭 활성
  const root = t.split("/").slice(0, 2).join("/");
  return (h === root || h === root + "") && to === list[0][1];
}

// ── 화면 전환마다 상단·하단이 늦게 뜨지 않도록: 인증·역할·디데이를 모듈 캐시로 ──
// getSession 은 로컬 저장소만 봐서 즉시고, 역할·디데이는 첫 조회 뒤 재사용(디데이 10분).
let authCache = null;   // null 미확인 | true | false
let roleCache = null;   // { isAdmin } | null
let ddayCache;          // undefined 미조회 | null 없음 | { days, title }
let ddayAt = 0;

/** 상단: 로고(모/강 토글 유지) · 베타 · D-day · 마이페이지 + 현재 탭의 서브탭 */
export function ShellTop({ theme, hash }) {
  const [me, setMe] = useState(() => (authCache === true ? { isAdmin: roleCache?.isAdmin || false } : authCache));
  const [dday, setDday] = useState(() => (ddayCache === undefined ? null : ddayCache));
  useEffect(() => {
    let alive = true;
    supabase.auth.getSession().then(async ({ data }) => {
      const u = data?.session?.user;
      authCache = !!u;
      if (!u) { if (alive) setMe(false); return; }
      if (alive) setMe({ isAdmin: roleCache?.isAdmin || false });
      if (!roleCache) {
        const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
        roleCache = { isAdmin: p?.role === "admin" };
        if (alive) setMe({ isAdmin: roleCache.isAdmin });
      }
    });
    if (ddayCache === undefined || Date.now() - ddayAt > 10 * 60e3) {
      const today = new Date().toISOString().slice(0, 10);
      supabase.from("events").select("date, title").eq("dday", true).gte("date", today)
        .order("date").limit(1).then(({ data }) => {
          ddayAt = Date.now();
          if (data?.[0]) {
            const d = Math.round((new Date(data[0].date + "T00:00:00") - new Date(today + "T00:00:00")) / 86400000);
            ddayCache = { days: d, title: data[0].title };
          } else ddayCache = null;
          if (alive) setDday(ddayCache);
        });
    }
    return () => { alive = false; };
  }, []);
  if (!me) return null;
  const tab = tabOf(hash);
  const subs = SUBTABS[tab];
  return (
    <div className={"sh-top sh-" + theme}>
      <style>{SH_CSS}</style>
      <div className="sh-in">
        <div className="sh-r1">
          <LogoTrigger src="/brand/ashrain_logo.png" height={26}
            right={{ tag: "모", label: "학부모", go: () => navigatePath("/jongseong") }}
            down={{ tag: "강", label: "강사", go: () => navigatePath("/seirocco") }}
            onLogoClick={() => (location.hash = "")} />
          {BETA.on && <span className="sh-beta" title={BETA.notice}>{BETA.label}</span>}
          {dday && (
            <span className="sh-dday" title={dday.title}>{dday.days === 0 ? "D-DAY" : `D-${dday.days}`}</span>
          )}
          <span className="sh-sp" />
          <button className="sh-my" title="마이페이지" onClick={() => (location.hash = "#/me")}>👤</button>
        </div>
        {me.isAdmin && (
          <div className="sh-admin">
            {[["📚 등록", "#/admin/concepts"], ["🔍 문항", "#/admin/items"], ["📄 자료", "#/admin/corpus"],
              ["💬 검토", "#/admin/qna"], ["🗂 대화", "#/admin/chats"], ["🖼 이미지", "#/admin/images"],
              ["🗓 일정", "#/admin/calendar"], ["⛲ 우물", "#/admin/well"], ["🛡 보호자", "#/admin/guardians"]].map(([l, to]) => (
              <button key={to} className="sh-abtn" onClick={() => (location.hash = to)}>{l}</button>
            ))}
          </div>
        )}
        {subs && (
          <div className="sh-subtabs" role="tablist">
            {subs.map(([label, to]) => (
              <button key={to} role="tab" aria-selected={subOn(hash, to, subs)}
                className={"sh-stab" + (subOn(hash, to, subs) ? " on" : "")}
                onClick={() => (location.hash = to)}>{label}</button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * 탭줄 한 벌 — 납작한 탭 2+2 사이에 우물. 하단 고정 탭바(ShellTabs)와
 * 관리자 미리보기(#/admin/well)가 같은 모양을 쓰도록 분리해 두었다.
 */
export function TabsRow({ theme, hash, cfg, onWell, wellProps = {}, recDot = null }) {
  const tab = tabOf(hash);
  const onOf = (to) => (to === "#/" ? tab === "dash"
    : to === "#/study" ? tab === "study" : to === "#/tools" ? tab === "tools" : tab === "records");
  const btn = ([ic, label, to]) => (
    <button key={to} className={"sh-tab" + (onOf(to) ? " on" : "")}
      onClick={() => (location.hash = to === "#/" ? "" : to)}>
      <span className="ic">{ic}{to === "#/records" && recDot && <i className={"sh-dot " + recDot} aria-hidden="true" />}</span>
      <span className="lb">{label}</span>
    </button>
  );
  return (
    <div className={"sh-row sh-" + theme}
      style={{ "--wt-h": cfg.bar.h + "px", "--wt-s": cfg.bar.tab / 100 }}>
      <style>{SH_CSS + WELL_CSS}</style>
      <div className="sh-tabs-in">
        {TABS.slice(0, 2).map(btn)}
        <WellButton theme={theme} cfg={cfg} onOpen={onWell} {...wellProps} />
        {TABS.slice(2).map(btn)}
      </div>
    </div>
  );
}

/** 하단 고정 탭바 — 대시보드 · 공부하기 | ⛲ | 학습 도구 · 기록. 판독 잡 뱃지·완료 토스트도 여기서 */
export function ShellTabs({ theme, hash }) {
  const [ok, setOk] = useState(() => authCache === true);
  const [sheet, setSheet] = useState(false);
  const [, setJt] = useState(0);
  const [jtoast, setJtoast] = useState(null);
  const cfg = useWellCfg();
  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => { authCache = !!data?.session; setOk(authCache); });
  }, []);
  // 한가할 때 공부하기 화면·데이터를 미리 데워 둔다 — 첫 진입도 즉시 (세션 1회)
  useEffect(() => { const t = setTimeout(warmStudy, 1800); return () => clearTimeout(t); }, []);
  useEffect(() => {
    let timer = null;
    const on = () => setJt((t) => t + 1);
    const onToast = (e) => {
      setJtoast(e.detail || null);
      clearTimeout(timer);
      timer = setTimeout(() => setJtoast(null), 4500);
    };
    window.addEventListener("ash:jobs", on);
    window.addEventListener("ash:job-toast", onToast);
    return () => { window.removeEventListener("ash:jobs", on); window.removeEventListener("ash:job-toast", onToast); clearTimeout(timer); };
  }, []);
  if (!ok) return null;
  const recDot = runningJobs().length ? "run" : unseenJobs().length ? "new" : null;
  return (
    <>
      <nav className={"sh-tabs sh-" + theme} aria-label="주 메뉴">
        <TabsRow theme={theme} hash={hash} cfg={cfg} onWell={() => setSheet(true)} recDot={recDot} />
      </nav>
      {jtoast && (
        <button type="button" className={"sh-jtoast sh-" + theme} onClick={() => { setJtoast(null); location.hash = "#/records"; }}>
          <b>{jtoast.title}</b>{jtoast.body ? <span>{jtoast.body}</span> : null}
        </button>
      )}
      <WellSheet open={sheet} onClose={() => setSheet(false)} theme={theme} />
    </>
  );
}

const SH_CSS = `
.sh-light { --sbg:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; }
.sh-dark  { --sbg:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; }
.sh-top { position: sticky; top: 0; z-index: 70; background: var(--sbg);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.sh-top * , .sh-tabs * , .sh-row * { box-sizing: border-box; }
.sh-in { max-width: 1200px; margin: 0 auto; padding: 8px 14px 0; }
.sh-r1 { display: flex; align-items: center; gap: 8px; padding-bottom: 6px; }
.sh-light .sh-r1 img { filter: grayscale(1) brightness(0); }
.sh-sp { flex: 1; }
.sh-beta { font-size: 10px; font-weight: 800; color: #fff; background: #7C3AED; border-radius: 999px; padding: 2px 7px; }
.sh-dday { min-width: 34px; border-radius: 999px; background: #EF4444; color: #fff; display: inline-flex;
  align-items: center; justify-content: center; font-size: 10.5px; font-weight: 800; padding: 4px 8px; }
.sh-my { width: 32px; height: 32px; border-radius: 999px; background: var(--card); border: 1px solid var(--bd);
  color: var(--ink); font-size: 15px; cursor: pointer; flex: none; }
.sh-admin { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding-bottom: 6px; }
.sh-admin::-webkit-scrollbar { display: none; }
.sh-abtn { flex: none; background: var(--card); border: 1px solid var(--bd); border-radius: 999px; color: var(--ink);
  font-size: 11px; font-weight: 700; padding: 5px 10px; cursor: pointer; }
.sh-subtabs { display: flex; gap: 18px; overflow-x: auto; scrollbar-width: none; border-bottom: 1px solid var(--bd); }
.sh-subtabs::-webkit-scrollbar { display: none; }
.sh-stab { background: none; border: none; padding: 9px 2px 10px; font-size: 14.5px; font-weight: 700; color: var(--mut);
  white-space: nowrap; cursor: pointer; border-bottom: 2.5px solid transparent; margin-bottom: -1px; font-family: inherit; }
.sh-stab.on { color: var(--ink); border-bottom-color: var(--ink); }
.sh-tabs { position: fixed; left: 0; right: 0; bottom: 0; z-index: 80; background: var(--card);
  border-top: 1px solid var(--bd);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif;
  padding-bottom: env(safe-area-inset-bottom, 0px); }
.sh-row { font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.sh-tabs-in { isolation: isolate; max-width: 520px; margin: 0 auto; display: flex; align-items: stretch;
  height: var(--wt-h, 52px); padding: 0 10px; }
.sh-tab { -webkit-tap-highlight-color: transparent; flex: 1; background: none; border: none; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 1px; color: var(--mut); cursor: pointer; padding: 3px 0 4px; font-family: inherit; }
.sh-tab .ic { font-size: calc(17px * var(--wt-s, 1)); line-height: 1; position: relative; }
.sh-tab .lb { font-size: calc(9.5px * var(--wt-s, 1)); font-weight: 800;
  text-shadow: 0 0 2px var(--card), 0 0 4px var(--card); } /* 우물 해 그림자가 탭 밑으로 지나가도 글자가 읽히게 */
.sh-tab.on { color: var(--ac); }
.sh-dot { position: absolute; top: -2px; right: -7px; width: 8px; height: 8px; border-radius: 999px; }
.sh-dot.new { background: #EF4444; }
.sh-dot.run { background: var(--ac); animation: sh-pulse 1.2s ease-in-out infinite; }
@keyframes sh-pulse { 0%,100% { opacity: 1; } 50% { opacity: .35; } }
.sh-jtoast { position: fixed; left: 50%; transform: translateX(-50%); bottom: calc(64px + env(safe-area-inset-bottom, 0px));
  z-index: 110; max-width: min(480px, calc(100vw - 28px)); display: flex; flex-direction: column; gap: 2px; text-align: left;
  background: var(--card); color: var(--ink); border: 1px solid var(--bd); border-radius: 14px; padding: 10px 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,.25); cursor: pointer; font-family: inherit; }
.sh-jtoast b { font-size: 13px; }
.sh-jtoast span { font-size: 11.5px; color: var(--mut); }
`;
