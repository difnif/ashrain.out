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

export const TABS = [
  ["🏠", "대시보드", "#/"],
  ["📚", "공부하기", "#/study"],
  ["🧰", "학습 도구", "#/tools"],
  ["💬", "게시판", "#/board"],
];

const SUBTABS = {
  study: [["개념 공부", "#/study/concept"], ["연습문제", "#/study/practice"], ["시험 보기", "#/study/exam"]],
  tools: [["전체", "#/tools"], ["오답노트", "#/tools/wrong"], ["질문하기", "#/tools/ask"], ["사진 채점", "#/tools/omr"],
          ["사진 힌트", "#/tools/hint"], ["문장 해설", "#/tools/read"], ["표시 연습", "#/tools/mark"],
          ["서술형", "#/tools/essay"], ["스피드 연산", "#/tools/calc"], ["찍어서 배우기", "#/tools/photo"]],
  board: [["공지", "#/board/notice"], ["커뮤니티", "#/board/community"], ["질문", "#/board/qna"]],
};

/** 현재 해시의 큰 탭 */
export function tabOf(hash) {
  if (hash.startsWith("#/study")) return "study";
  if (hash.startsWith("#/tools")) return "tools";
  if (hash.startsWith("#/board")) return "board";
  return "dash";
}

const BOARD_BROWSE = ["", "notice", "community", "qna"];

/** 셸(탭바·서브탭)을 그릴 화면인가 — 아니면 기능 화면(FeatureBar만) */
export function shellMode(hash) {
  const h = (hash || "").split("?")[0];
  if (h === "" || h === "#" || h === "#/") return "browse";
  if (h.startsWith("#/study") || h.startsWith("#/tools")) return "browse";
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

/** 상단: 로고(모/강 토글 유지) · 베타 · D-day · 마이페이지 + 현재 탭의 서브탭 */
export function ShellTop({ theme, hash }) {
  const [me, setMe] = useState(null);
  const [dday, setDday] = useState(null);
  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) { setMe(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      setMe({ isAdmin: p?.role === "admin" });
    });
    const today = new Date().toISOString().slice(0, 10);
    supabase.from("events").select("date, title").eq("dday", true).gte("date", today)
      .order("date").limit(1).then(({ data }) => {
        if (data?.[0]) {
          const d = Math.round((new Date(data[0].date + "T00:00:00") - new Date(today + "T00:00:00")) / 86400000);
          setDday({ days: d, title: data[0].title });
        }
      });
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
export function TabsRow({ theme, hash, cfg, onWell, wellProps = {} }) {
  const tab = tabOf(hash);
  const onOf = (to) => (to === "#/" ? tab === "dash"
    : to === "#/study" ? tab === "study" : to === "#/tools" ? tab === "tools" : tab === "board");
  const btn = ([ic, label, to]) => (
    <button key={to} className={"sh-tab" + (onOf(to) ? " on" : "")}
      onClick={() => (location.hash = to === "#/" ? "" : to)}>
      <span className="ic">{ic}</span><span className="lb">{label}</span>
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

/** 하단 고정 탭바 — 대시보드 · 공부하기 | ⛲ | 학습 도구 · 게시판 */
export function ShellTabs({ theme, hash }) {
  const [ok, setOk] = useState(false);
  const [sheet, setSheet] = useState(false);
  const cfg = useWellCfg();
  useEffect(() => { supabase.auth.getUser().then(({ data }) => setOk(!!data?.user)); }, []);
  if (!ok) return null;
  return (
    <>
      <nav className={"sh-tabs sh-" + theme} aria-label="주 메뉴">
        <TabsRow theme={theme} hash={hash} cfg={cfg} onWell={() => setSheet(true)} />
      </nav>
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
.sh-tabs-in { max-width: 520px; margin: 0 auto; display: flex; align-items: stretch;
  height: var(--wt-h, 52px); padding: 0 10px; }
.sh-tab { flex: 1; background: none; border: none; display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 1px; color: var(--mut); cursor: pointer; padding: 3px 0 4px; font-family: inherit; }
.sh-tab .ic { font-size: calc(17px * var(--wt-s, 1)); line-height: 1; }
.sh-tab .lb { font-size: calc(9.5px * var(--wt-s, 1)); font-weight: 800; }
.sh-tab.on { color: var(--ac); }
`;
