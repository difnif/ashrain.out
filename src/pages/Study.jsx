// 공부하기 탭 (#/study) — 서브탭: 개념 공부 · 연습문제 · 컨셉 문제 · 시청각 학습 · 시험 보기 (셸이 상·하단을 그린다)
// sub: '' | 'concept' | 'practice' | 'sets[/<범주>]' | 'av[/<범주>]' | 'exam[/school[/<학교>[/<판>]]]'  (''=concept)
//   시험 보기 › 학교별 모의고사 = 학교 찾기 → 판(융합 · 기본 …) → 회차 → #/mock/<id> (pages/mock/SchoolExams.jsx · lib/mockexams.js)
//   시청각 학습 = 교실 모니터 콘텐츠(lib/av.js) — 수학 호기심 · 문제 풀이 해설 두 범주, 고르면 #/av/<key> 가로 무대로
import { Suspense, lazy, useEffect, useMemo, useRef, useState } from "react";
import { UNIT_NAMES, UNIT_ORDER } from "../lib/items";
import { readLastResult } from "../lib/setplay";
import { getRecentConcepts } from "../lib/review";
import { TEST_TYPES, describeTimer, presetOf, isExamOpen } from "../lib/exam";
import { swrConcepts } from "../lib/studyCache";
import { koFilter } from "../lib/koSearch";
import ItemPicker from "./solve/ItemPicker";
import { CATEGORIES, loadIndex, readProgress, setProgressUser, pad2 } from "../lib/conceptsets";
import { supabase } from "../supabaseClient";
import { AV_CATS, AV_LEVELS, avOfCat, avOfLevel, weekCard, unitCard } from "../lib/av";
import { hasPrint } from "../lib/avsrc";
import { WGRADES, gradesOfLevel, loadWeekIndex, weekIndexCached, PERIODS, KIND_ICON, weekOfDate, weekLabel, periodOf } from "../features/display/weeks/index.js";
import { recommend } from "../lib/recommend";
import { loadProfile } from "../lib/recommendLoad";
import { readHist, histDone, lastSeen } from "../lib/avHistory";
import { unitLabel } from "../lib/units";
import { useWellPick } from "../components/WellPick";
import { loadMockIndex } from "../lib/mockexams";
const AvPrintSheet = lazy(() => import("../components/AvPrintSheet"));
const SchoolExams = lazy(() => import("./mock/SchoolExams"));
import "./solve/solve.css";

const CSS = `
.st-root { min-height: 100vh; padding: 12px 14px 96px; box-sizing: border-box; background: var(--pbg); overflow-wrap: break-word;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; color: var(--text); }
.st-root * { box-sizing: border-box; }
.st-light { --pbg:#EDEFF2; --text:#1F2937; --muted:#8A929C; --surface:#fff; --surface2:#F4F6F8; --surface3:#E7EAEE;
  --border:#DFE3E8; --accent:#0D9488; --good:#16A34A; --bad:#DC2626; }
.st-dark { --pbg:#0B0C0F; --text:#E2E8F0; --muted:#8A929C; --surface:#15171C; --surface2:#101116; --surface3:#1C1F26;
  --border:#23262D; --accent:#5EEAD4; --good:#4ADE80; --bad:#F87171; }
.st-wrap { max-width: 680px; margin: 0 auto; }
.st-chips { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding: 2px 0 8px; }
.st-chips::-webkit-scrollbar { display: none; }
.st-chip { flex: none; background: var(--surface); border: 1px solid var(--border); border-radius: 999px;
  color: var(--text); font-size: 12px; font-weight: 700; padding: 7px 12px; cursor: pointer; font-family: inherit; }
.st-chip.on { border-color: var(--accent); color: var(--accent); border-width: 1.5px; }
.st-chip small { color: var(--muted); font-weight: 600; margin-left: 3px; }
.st-list { display: flex; flex-direction: column; gap: 8px; }
.st-item { display: flex; align-items: center; gap: 10px; width: 100%; text-align: left; background: var(--surface);
  border: 1px solid var(--border); border-radius: 12px; padding: 12px; color: var(--text); cursor: pointer; font-family: inherit; }
.st-item .num { flex: none; font-size: 11px; font-weight: 800; color: var(--muted); width: 24px; }
.st-item .nm { flex: 1; min-width: 0; }
.st-item .nm b { display: block; font-size: 14px; font-weight: 700; }
.st-item .nm small { display: block; font-size: 11.5px; color: var(--muted); margin-top: 1px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.st-item .tag { flex: none; font-size: 10.5px; font-weight: 800; color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent); border-radius: 999px; padding: 3px 8px; }
.st-sec { font-size: 12.5px; font-weight: 800; color: var(--muted); margin: 16px 2px 8px; }
.st-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 14px 15px; margin-bottom: 10px; }
.st-empty { background: var(--surface2); border: 1px dashed var(--border); border-radius: 12px; padding: 16px 12px;
  font-size: 12.5px; color: var(--muted); line-height: 1.65; text-align: center; }
.st-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
@media (max-width: 380px) { .st-grid { grid-template-columns: minmax(0, 1fr); } }
.st-tile { display: flex; flex-direction: column; gap: 4px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 12px; text-align: left; color: var(--text); cursor: pointer; font-family: inherit; }
.st-tile .tt { font-size: 13.5px; font-weight: 800; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.st-tile .ds { font-size: 11px; color: var(--muted); line-height: 1.5; }
.st-dev { opacity: .6; cursor: default; }
.st-devb { display: inline-flex; margin-left: 6px; font-size: 9px; font-weight: 900; letter-spacing: .5px; color: #fff;
  background: #94A3B8; border-radius: 999px; padding: 2px 7px; vertical-align: middle; }
.st-dark .st-devb { background: #475569; }
.st-devnote { background: var(--surface); border: 1px dashed var(--muted); border-radius: 12px;
  padding: 12px 14px; font-size: 12.5px; color: var(--muted); line-height: 1.6; margin-bottom: 4px; }
.st-devnote b { color: var(--text); }
.st-badge { display: inline-flex; font-size: 9.5px; font-weight: 900; letter-spacing: .5px; color: #fff;
  border-radius: 999px; padding: 2px 7px; line-height: 1.4; }
.st-meta { display: flex; gap: 5px; flex-wrap: wrap; margin-top: 2px; }
.st-tag { font-size: 10.5px; font-weight: 700; color: var(--muted); border: 1px solid var(--border);
  border-radius: 999px; padding: 1px 7px; }
/* 컨셉 문제 — 범주 폴더 · 세트 아이콘 */
.st-folder { display: flex; align-items: center; gap: 12px; width: 100%; text-align: left; background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 14px; color: var(--text); cursor: pointer; font-family: inherit; }
.st-folder .fi { flex: none; width: 52px; height: 52px; border-radius: 15px; background: var(--surface2); display: flex; align-items: center;
  justify-content: center; font-size: 28px; position: relative; }
.st-folder .fi::after { content: ""; position: absolute; left: 7px; right: 7px; top: -4px; height: 6px; border-radius: 4px 4px 0 0; background: var(--surface3); }
.st-folder .nm { flex: 1; min-width: 0; }
.st-folder .nm b { display: block; font-size: 15px; font-weight: 800; }
.st-folder .nm small { display: block; font-size: 12px; color: var(--muted); margin-top: 2px; line-height: 1.5; }
.st-folder .go { flex: none; color: var(--muted); font-size: 18px; }
.st-crumb { display: flex; align-items: center; gap: 6px; margin: 2px 0 10px; font-size: 13px; }
.st-crumb button { background: none; border: none; padding: 0; color: var(--muted); font: inherit; font-weight: 700; cursor: pointer; }
.st-crumb b { font-weight: 800; }
.st-cdesc { font-size: 12px; color: var(--muted); line-height: 1.6; margin: 0 2px 4px; }
.st-icons { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(76px, 100%), 1fr)); gap: 8px; }
.st-ic { position: relative; display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 12px 4px 9px; background: var(--surface);
  border: 1px solid var(--border); border-radius: 16px; color: var(--text); cursor: pointer; font-family: inherit; -webkit-tap-highlight-color: transparent; }
.st-ic:active { transform: scale(.97); }
.st-ic .em { font-size: 30px; line-height: 1.1; }
.st-ic .nm { font-size: 12px; font-weight: 800; text-align: center; line-height: 1.25; word-break: keep-all; }
.st-ic .no { position: absolute; top: 5px; left: 7px; font-size: 9.5px; font-weight: 800; color: var(--muted); }
.st-ic .pg { width: 70%; height: 4px; border-radius: 999px; background: var(--surface3); overflow: hidden; }
.st-ic .pg i { display: block; height: 100%; background: var(--accent); }
.st-ic.done { border-color: var(--good); }
.st-ic.done .pg i { background: var(--good); }
.st-avic { flex: none; width: 44px; height: 44px; border-radius: 13px; background: var(--surface2); display: flex; align-items: center;
  justify-content: center; font-size: 24px; }
.st-item .nm small.wrap { white-space: normal; line-height: 1.5; }
.st-item .nm small.unit { color: var(--accent); font-weight: 700; margin-top: 2px; }
.st-lv { display: flex; gap: 6px; margin: 4px 0 10px; padding: 4px; border-radius: 14px; background: var(--surface2); }
.st-lv button { flex: 1; border: 0; border-radius: 11px; padding: 9px 4px; font: inherit; font-size: 14px; font-weight: 800; color: var(--muted);
  background: transparent; cursor: pointer; }
.st-lv button small { font-size: 11px; font-weight: 700; margin-left: 4px; opacity: .8; }
.st-lv button.on { background: var(--surface); color: var(--ink, inherit); box-shadow: 0 1px 4px rgba(0,0,0,.12); }
.st-gk { display: flex; gap: 6px; overflow-x: auto; margin: 0 0 8px; padding-bottom: 2px; }
.st-gk button { flex: none; border: 1px solid var(--border); background: var(--surface); color: var(--muted); border-radius: 999px; padding: 6px 13px;
  font: inherit; font-size: 13px; font-weight: 800; cursor: pointer; }
.st-gk button.on { background: var(--accent); border-color: var(--accent); color: #fff; }
.st-view { display: flex; gap: 6px; margin: 0 0 6px; }
.st-view button { flex: 1; border: 1px solid var(--border); background: var(--surface); color: var(--muted); border-radius: 12px; padding: 8px 6px;
  font: inherit; font-size: 13px; font-weight: 800; cursor: pointer; }
.st-view button small { font-weight: 700; opacity: .7; margin-left: 3px; }
.st-view button.on { color: var(--text); border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
.st-cont { display: flex; gap: 8px; margin: 2px 0 8px; }
.st-cont-b { flex: 1; min-width: 0; text-align: left; border: 1px solid var(--border); background: var(--surface); color: inherit; border-radius: 14px;
  padding: 9px 11px; font: inherit; cursor: pointer; }
.st-cont-b small { display: block; font-size: 11px; font-weight: 800; color: var(--accent); }
.st-cont-b b { display: block; font-size: 13.5px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.st-cont-b.now { background: var(--surface2); }
.st-find input { width: 100%; border: 1px solid var(--border); background: var(--surface); color: inherit; border-radius: 12px; padding: 9px 12px;
  font: inherit; font-size: 13.5px; }
.st-uchips { display: flex; gap: 6px; overflow-x: auto; margin: 8px 0 4px; padding-bottom: 2px; }
.st-uchips button { flex: none; border: 1px solid var(--border); background: var(--surface); color: var(--muted); border-radius: 999px; padding: 5px 11px;
  font: inherit; font-size: 12px; font-weight: 700; cursor: pointer; }
.st-uchips button.on { color: var(--text); border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
.st-gap { font-size: 11.5px; color: var(--muted); margin: 4px 2px; }
.st-per { margin-top: 8px; }
.st-per-h { display: flex; align-items: baseline; gap: 8px; width: 100%; border: 0; background: none; color: inherit; font: inherit; padding: 8px 2px; cursor: pointer; }
.st-per-h b { font-size: 15px; font-weight: 800; }
.st-per-h small { flex: 1; text-align: left; font-size: 12px; color: var(--muted); }
.st-wk { display: grid; grid-template-columns: 3.6em minmax(0, 1fr); gap: 8px; align-items: stretch; padding: 6px 0; border-top: 1px solid var(--border); }
.st-wk .wl { display: flex; flex-direction: column; justify-content: center; }
.st-wk .wl b { font-size: 14px; font-weight: 800; }
.st-wk .wl small { font-size: 10.5px; color: var(--muted); }
.st-wk .wl em { font-style: normal; font-size: 10px; font-weight: 800; color: var(--accent); }
.st-wk.now { background: var(--surface2); border-radius: 12px; padding: 6px; }
.st-wk .ws { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; min-width: 0; }
.st-sess { position: relative; display: flex; flex-direction: column; gap: 2px; min-width: 0; text-align: left; border: 1px solid var(--border);
  background: var(--surface); color: inherit; border-radius: 12px; padding: 8px 9px; font: inherit; cursor: pointer; }
.st-sess .k { font-size: 10.5px; font-weight: 800; color: var(--muted); display: flex; align-items: center; gap: 4px; }
.st-sess .k em { font-style: normal; color: var(--accent); margin-left: auto; }
.st-sess b { font-size: 13px; font-weight: 800; line-height: 1.35; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.st-sess small { font-size: 10.5px; color: var(--muted); overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.st-sess.done { opacity: .72; }
.st-sess .pg { height: 3px; border-radius: 2px; background: var(--surface3); overflow: hidden; margin-top: 3px; }
.st-sess .pg i { display: block; height: 100%; background: var(--accent); }
.st-hold { font-size: 11.5px; color: var(--muted); margin: -2px 2px 10px; line-height: 1.5; }
.st-item .tag em { display: block; font-style: normal; font-size: 9.5px; opacity: .8; text-align: center; margin-top: 1px; }
.st-print { position: relative; }
.st-print.done { opacity: .78; }
.st-print .pg { position: absolute; left: 14px; right: 14px; bottom: 4px; height: 2px; border-radius: 2px; background: var(--surface3); overflow: hidden; }
.st-print .pg i { display: block; height: 100%; background: var(--accent); }
`;

function readLastConcept() {
  try { const v = JSON.parse(localStorage.getItem("ash.lastConcept") || "null"); if (v && v.id) return v; } catch { /* 무시 */ }
  const r = getRecentConcepts();
  return r[0] || null;
}

/* ── 개념 공부: 학기 고르고 개념 목록 (+검색) — 목록·수는 studyCache 로 즉시 그린다 ── */
function ConceptSub() {
  const [all, setAll] = useState(null);
  const [q, setQ] = useState("");
  const [moreU, setMoreU] = useState(false);
  const last = useMemo(readLastConcept, []);
  const [unit, setUnit] = useState(() => {
    try { return localStorage.getItem("ash.study.unit") || (last?.id ? last.id.split("-").slice(0, 2).join("-") : "m1-1"); }
    catch { return "m1-1"; }
  });
  useEffect(() => { let ok = true; swrConcepts((v) => { if (ok) setAll(v || []); }); return () => { ok = false; }; }, []);
  const pick = (u) => { setUnit(u); try { localStorage.setItem("ash.study.unit", u); } catch { /* 무시 */ } };
  const byUnit = useMemo(() => {
    const m = {};
    for (const c of all || []) (m[c.unit_id] = m[c.unit_id] || []).push(c);
    for (const k of Object.keys(m)) m[k].sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
    return m;
  }, [all]);
  const rows = byUnit[unit] || [];
  // 개념이 등록된 학기만 기본 노출 — 나머지는 「다른 학기」로
  const visUnits = all === null || moreU ? UNIT_ORDER : UNIT_ORDER.filter((u) => u === unit || (byUnit[u] || []).length > 0);
  const hiddenN = UNIT_ORDER.length - visUnits.length;
  // 검색 — 학기 무관 전체 개념에서 (이름·부제·학기명, 초성 지원)
  const found = useMemo(() => {
    if (!q.trim()) return null;
    const list = (all || []).slice().sort((a, b) => UNIT_ORDER.indexOf(a.unit_id) - UNIT_ORDER.indexOf(b.unit_id) || (a.sort_order ?? 0) - (b.sort_order ?? 0));
    return koFilter(list, q, (c) => [c.title, c.subtitle, UNIT_NAMES[c.unit_id]], 30);
  }, [all, q]);

  const item = (c, withUnit) => (
    <button key={c.id} className="st-item" onClick={() => (location.hash = `#/c/${encodeURIComponent(c.id)}`)}>
      <span className="num">{String(c.sort_order ?? "").padStart(2, "0")}</span>
      <span className="nm"><b>{c.title}</b>{(c.subtitle || withUnit) && <small>{withUnit ? `${UNIT_NAMES[c.unit_id] || c.unit_id}${c.subtitle ? " · " : ""}` : ""}{c.subtitle || ""}</small>}</span>
      {last?.id === c.id && <span className="tag">이어보기</span>}
    </button>
  );

  return (
    <>
      <input className="sv-search" type="search" value={q} onChange={(e) => setQ(e.target.value)}
        placeholder="개념 검색 — 이름이나 초성(ㅈㅅ)으로 바로 찾기" aria-label="개념 검색" enterKeyHint="search" />
      {found !== null ? (
        found.length === 0
          ? <div className="st-empty">「{q.trim()}」에 맞는 개념이 없어요. 철자를 바꾸거나 초성으로 찾아보세요.</div>
          : <div className="st-list">{found.map((c) => item(c, true))}</div>
      ) : (
        <>
          <div className="st-chips">
            {visUnits.map((u) => (
              <button key={u} className={"st-chip" + (u === unit ? " on" : "")} onClick={() => pick(u)}>
                {UNIT_NAMES[u] || u}{byUnit[u] ? <small>{byUnit[u].length}</small> : null}
              </button>
            ))}
            {all !== null && (hiddenN > 0 || moreU) && (
              <button className="st-chip" style={{ color: "var(--muted)" }} onClick={() => setMoreU((m) => !m)}>
                {moreU ? "접기" : `다른 학기 +${hiddenN}`}
              </button>
            )}
          </div>
          {all === null ? <div className="st-empty">개념을 불러오는 중…</div>
            : rows.length === 0 ? <div className="st-empty">이 학기에는 아직 등록된 개념이 없어요.</div>
            : <div className="st-list">{rows.map((c) => item(c, false))}</div>}
        </>
      )}
      <p className="st-sec" style={{ fontWeight: 600 }}>예제·유제는 각 개념 카드 안에서 바로 이어져요. 복습 모드(Ⓓ 적립)는 개념 화면의 🔁 버튼.</p>
    </>
  );
}

/* ── 연습문제: 최근 세트 + 개념 골라 세트 시작 ── */
function PracticeSub() {
  const last = readLastResult();
  return (
    <>
      {last && (
        <div className="st-card">
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 12, color: "var(--muted)", fontWeight: 700 }}>최근 세트</div>
              <div style={{ fontWeight: 800 }}>{last.title || last.conceptId} · {last.ok}/{last.n} 정답</div>
            </div>
            <button className="sv-btn sm pri" onClick={() => (location.hash = `#/solve/set/${last.conceptId}`)}>새 세트</button>
          </div>
        </div>
      )}
      <ItemPicker hint="개념을 고르면 문항 세트(5·10·20)가 시작돼요. 풀고 나면 해설과 도형 애니메이션이 열려요."
        onPickConcept={(c) => (location.hash = `#/solve/set/${encodeURIComponent(c.id)}`)} />
    </>
  );
}

/* ── 시험 보기: 8종 그대로, 가볍게/실전/스페셜 그룹 ── */
const EXAM_GROUPS = [
  ["가볍게", ["concept_set"]],
  ["실전", ["unit", "calc", "mock", "sangwa"]],
  ["스페셜", ["ash", "rain", "out"]],
];

// 시험 보기 부분 개방(2026-09-21, 사용자 확정) — 개념 묶음·단원 테스트는 열고, 나머지는 개발중 표시.
// 맨 위 「학교별 모의고사」(2026-11-24) — 학교 찾기 → 판 → 회차 → 시험지 그대로 풀기 · 강사 모드 · 시청각 해설.
function ExamSub({ path = [] }) {
  if (path[0] === "school") {
    return <Suspense fallback={<div className="st-empty">불러오는 중…</div>}><SchoolExams path={path.slice(1)} /></Suspense>;
  }
  return (
    <>
      <p className="st-sec">학교별 모의고사</p>
      <SchoolFolder />
      <div className="st-devnote" style={{ marginTop: 14 }}>🧩 <b>개념 묶음</b>과 📘 <b>단원 테스트</b>부터 열었어요 — 나머지 유형은 문항을 쌓는 대로 차례차례 열려요.</div>
      {EXAM_GROUPS.map(([label, codes]) => (
        <div key={label}>
          <p className="st-sec">{label}</p>
          <div className="st-grid">
            {codes.map((code) => {
              const t = presetOf(code) || TEST_TYPES.find((x) => x.code === code);
              if (!t) return null;
              const open = isExamOpen(code);
              const body = (
                <>
                  <span className="tt">{t.icon} {t.name}{!open && <span className="st-devb">개발중</span>}</span>
                  <span className="ds">{t.desc}</span>
                  <span className="st-meta">
                    {t.n > 0 && <span className="st-tag">{t.n}문항</span>}
                    <span className="st-tag">{describeTimer(t)}</span>
                  </span>
                </>
              );
              return open ? (
                <button key={code} className="st-tile" onClick={() => (location.hash = `#/solve/test/${code}`)}>{body}</button>
              ) : (
                <div key={code} className="st-tile st-dev" aria-disabled="true">{body}</div>
              );
            })}
          </div>
        </div>
      ))}
    </>
  );
}

/** 「학교별 모의고사」 폴더 — 학교 · 회차 수는 목록(index.json)을 읽은 뒤 */
function SchoolFolder() {
  const [n, setN] = useState(null);
  useEffect(() => {
    let ok = true;
    loadMockIndex().then((ix) => { if (ok) setN({ s: ix.schools.filter((x) => (x.n || 0) > 0).length, e: ix.exams.length }); }).catch(() => {});
    return () => { ok = false; };
  }, []);
  return (
    <div className="st-list">
      <button className="st-folder" onClick={() => (location.hash = "#/study/exam/school")}>
        <span className="fi" aria-hidden="true">🏫</span>
        <span className="nm"><b>학교별 모의고사</b><small>{n?.e ? `학교 ${n.s}곳 · 모의고사 ${n.e}회 — ` : ""}우리 학교 시험지 그대로 · 학교를 고르면 융합 · 기본으로 나눠 풀어요</small></span>
        <span className="go" aria-hidden="true">›</span>
      </button>
    </div>
  );
}

/* ── 컨셉 문제: 범주 폴더 → 세트(파일)별 아이콘 ── */
function useCsProgressUser() {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let ok = true;
    supabase.auth.getSession().then(({ data }) => { setProgressUser(data?.session?.user?.id || ""); if (ok) setReady(true); })
      .catch(() => { if (ok) setReady(true); });
    return () => { ok = false; };
  }, []);
  return ready;
}

function SetsSub({ path }) {
  const catId = path[0] || "";
  const ready = useCsProgressUser();
  const [cat, setCat] = useState(null);
  const [err, setErr] = useState(null);
  useEffect(() => {
    if (!catId) return undefined;
    let ok = true;
    setCat(null); setErr(null);
    loadIndex(catId).then((c) => { if (ok) { if (c) setCat(c); else setErr("없는 범주예요"); } })
      .catch((e) => { if (ok) setErr(e?.message || String(e)); });
    return () => { ok = false; };
  }, [catId]);
  // 범주 폴더의 '○종 · ○문항'은 index.json 에서 센다(세트가 늘어도 손댈 곳 없음)
  const [counts, setCounts] = useState({});
  useEffect(() => {
    if (catId) return undefined;
    let ok = true;
    Promise.all(CATEGORIES.map((c) => loadIndex(c.id).then((x) => [c.id, x]).catch(() => [c.id, null]))).then((rows) => {
      if (!ok) return;
      setCounts(Object.fromEntries(rows.filter(([, x]) => x?.sets?.length)
        .map(([id, x]) => [id, { sets: x.sets.length, items: x.sets.reduce((a, s) => a + (s.n || 0), 0) }])));
    });
    return () => { ok = false; };
  }, [catId]);

  if (!catId) {
    return (
      <>
        <p className="st-cdesc">주제 하나로 한 단원을 끝까지 — 경우의 수와 확률은 스포츠 · 음악 · 시대별 역사 · 판례로, 일차함수는 중학교 과학 단원의 실제 법칙으로 만든 50제 묶음이에요. 앱에서 바로 풀고 3단 해설을 보거나, 문제지 · 해설지 · OMR 카드를 인쇄해 풀고 OMR 사진으로 채점해요.</p>
        <div className="st-list">
          {CATEGORIES.map((c) => (
            <button key={c.id} className="st-folder" onClick={() => (location.hash = `#/study/sets/${c.id}`)}>
              <span className="fi" aria-hidden="true">{c.icon}</span>
              <span className="nm"><b>{c.title}</b><small>{c.sub}{counts[c.id] ? ` · ${counts[c.id].sets}종 · ${counts[c.id].items.toLocaleString("ko-KR")}문항` : ""}</small></span>
              <span className="go" aria-hidden="true">›</span>
            </button>
          ))}
        </div>
      </>
    );
  }
  const crumb = (
    <div className="st-crumb">
      <button onClick={() => (location.hash = "#/study/sets")}>컨셉 문제</button><span aria-hidden="true">›</span><b>{cat?.title || "…"}</b>
    </div>
  );
  if (err) return <>{crumb}<div className="st-empty">목록을 불러오지 못했어요. {err}</div></>;
  if (!cat) return <>{crumb}<div className="st-empty">불러오는 중…</div></>;
  const byNo = Object.fromEntries(cat.sets.map((x) => [x.no, x]));
  return (
    <>
      {crumb}
      {cat.desc && <p className="st-cdesc">{cat.desc}</p>}
      {cat.groups.map((g) => (
        <div key={g.title}>
          <p className="st-sec">{g.icon ? `${g.icon} ` : ""}{g.title}</p>
          <div className="st-icons">
            {g.sets.map((no) => {
              const x = byNo[no];
              if (!x) return null;
              const p = ready ? readProgress(catId, no) : null;
              const done = p ? Object.keys(p.items).length : 0;
              const pct = x.n ? Math.min(100, Math.round((done / x.n) * 100)) : 0;
              return (
                <button key={no} className={"st-ic" + (done >= x.n ? " done" : "")} title={x.title}
                  onClick={() => (location.hash = `#/sets/${catId}/${pad2(no)}`)}>
                  <span className="no">{pad2(no)}</span>
                  <span className="em" aria-hidden="true">{x.icon}</span>
                  <span className="nm">{x.short}</span>
                  <span className="pg" aria-label={`${done}/${x.n}`}><i style={{ width: `${pct}%` }} /></span>
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </>
  );
}

/* ── 시청각 학습: 범주 폴더 → 항목(교실 모니터 무대로 연다) ── */
const lsGet = (k, d) => { try { const v = localStorage.getItem(k); return v == null ? d : v; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch { /* 무시 */ } };
let SOL_CARDS = null;
const SOL_UNITS = () => (SOL_CARDS ||= avOfCat("sol").map(unitCard));

/** 우물 추천에 쓸 카드 더미 — 읽어 둔 학년의 회차 전부 + 유형별 문제 세트(기본기 단원 · 시그니처 프린트) */
function usePool(gk) {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const i = WGRADES.findIndex((g) => g.gk === gk);
    let live = true;
    for (const g of [WGRADES[i - 1], WGRADES[i + 1]].filter(Boolean)) {
      if (!weekIndexCached(g.gk)) loadWeekIndex(g.gk).then(() => { if (live) setTick((t) => t + 1); }).catch(() => {});
    }
    return () => { live = false; };
  }, [gk]);
  return useMemo(() => {
    const out = [...SOL_UNITS()];
    for (const g of WGRADES) { const h = weekIndexCached(g.gk); if (h) for (const m of h.sessions) out.push(weekCard(m)); }
    return out;
  }, [gk, tick]);   // eslint-disable-line react-hooks/exhaustive-deps
}

/**
 * 문제 풀이 해설 — 위 「초등 | 중등 | 고등」 → 학년 → 「주차별 기초 다지기(104회차) | 유형별 문제 세트」.
 * 주차별: 1학기 · 여름방학 · 2학기 · 겨울방학으로 접고 펴며, 지금 주를 펼쳐 그 자리로. 이어 보기 · 찾기 · 단원 칩.
 * 유형별 문제 세트: 프린트마다 한 줄 — 기본기 단원과 시그니처 프린트(그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 경우의 수와 확률 100제 넷)가
 *   같은 서열로, 교과서 단원 차례(시그니처 프린트는 그 단원 바로 뒤). 단계는 프린트 안에(재생 화면의 단계 목록) — 줄을 단계로 쪼개지 않는다.
 *   줄마다 교과서 단원 · 학년 · 문항 수 · 다 봤음 ✓ · 본 만큼 진행 막대.
 * 꾹 누르면 우물이 떠서 6가지를 추천한다 — 기록이 넉넉하면 수준 맞춤(lib/recommend.js), 아니면 단원 지도 기본.
 *   프린트 문서가 있으면(기본기 단원 · 회차) 위에 「📄 프린트」도 — 그 위에서 떼면 문제지 · 해설지 · 빠른 정답 · OMR 받기 판(AvPrintSheet).
 */
function SolList() {
  const [lv, setLv] = useState(() => { const v = lsGet("ash.study.av.lv", "초등"); return AV_LEVELS.includes(v) ? v : "초등"; });
  const pickLv = (v) => { setLv(v); lsSet("ash.study.av.lv", v); };
  const grades = gradesOfLevel(lv);
  const [gkBy, setGkBy] = useState(() => Object.fromEntries(AV_LEVELS.map((l) => [l, lsGet(`ash.study.av.gk.${l}`, gradesOfLevel(l)[0].gk)])));
  const gk = grades.some((g) => g.gk === gkBy[lv]) ? gkBy[lv] : grades[0].gk;
  const pickGk = (v) => { setGkBy((o) => ({ ...o, [lv]: v })); lsSet(`ash.study.av.gk.${lv}`, v); };
  const [view, setView] = useState(() => (lsGet("ash.study.av.view", "week") === "unit" ? "unit" : "week"));
  const pickView = (v) => { setView(v); lsSet("ash.study.av.view", v); };
  const [profile, setProfile] = useState(() => ({ mastery: {}, watched: readHist() }));
  useEffect(() => { let live = true; loadProfile().then((p) => { if (live) setProfile(p); }).catch(() => {}); return () => { live = false; }; }, []);
  const pool = usePool(gk);
  const go = (it) => { location.hash = `#/av/${it.key}`; };
  const [print, setPrint] = useState(null);           // 프린트 받기 판을 연 콘텐츠 key
  const wp = useWellPick({ related: (it) => recommend(it, pool, profile).cards, onGo: go, onPrint: (it) => setPrint(it.key), canPrint: (it) => hasPrint(it.key) });
  const W = profile.watched || {};
  return (
    <>
      <div className="st-lv" role="tablist" aria-label="학교급">
        {AV_LEVELS.map((l) => (
          <button key={l} type="button" role="tab" aria-selected={l === lv} className={l === lv ? "on" : ""} onClick={() => pickLv(l)}>
            {l}<small>{gradesOfLevel(l).length * 104}</small>
          </button>
        ))}
      </div>
      <div className="st-gk" role="tablist" aria-label="학년">
        {grades.map((g) => (
          <button key={g.gk} type="button" role="tab" aria-selected={g.gk === gk} className={g.gk === gk ? "on" : ""} onClick={() => pickGk(g.gk)}>{g.grade}</button>
        ))}
      </div>
      <div className="st-view">
        <button type="button" className={view === "week" ? "on" : ""} onClick={() => pickView("week")}>🗓 주차별 기초 다지기 <small>104회차</small></button>
        <button type="button" className={view === "unit" ? "on" : ""} onClick={() => pickView("unit")}>📚 유형별 문제 세트 <small>{avOfLevel(lv).length}</small></button>
      </div>
      <p className="st-hold">꾹 누르면 우물이 떠서 6가지를 골라 줘요 — 본 기록 · 푼 기록이 쌓이면 내 수준에 맞춰서. 누른 채 손가락을 옮겨 놓으면 바로 열리고,
        위 「📄 프린트」에서 놓으면 그 문제의 프린트(문제지 · 해설지 · 빠른 정답 · OMR)를 받아요.</p>
      {view === "week" ? <WeekList key={gk} gk={gk} wp={wp} profile={profile} /> : (
        <div className="st-list" role="tabpanel">
          {avOfLevel(lv).map((it) => {
            const r = W[it.key], done = histDone(r), part = r && !done && r.max > 0 && r.n > 0;
            return (
              <button key={it.key} type="button" className={"st-item st-print wpk-able" + (wp.pressing === it.key ? " wpk-press" : "") + (done ? " done" : "")}
                {...wp.bind(unitCard(it), () => go(it))}>
                <span className="st-avic" aria-hidden="true">{it.icon}</span>
                <span className="nm"><b>{it.title}</b>{it.unit && <small className="unit">{unitLabel(it.unit)}</small>}<small className="wrap">{it.desc}</small></span>
                <span className="tag">{it.grade || it.kind}<em>{done ? "✓ " : ""}{it.n ? `${it.n}제` : ""}</em></span>
                {part && <span className="pg" aria-label={`${r.max}/${r.n}`}><i style={{ width: `${Math.round((r.max / r.n) * 100)}%` }} /></span>}
              </button>
            );
          })}
        </div>
      )}
      {wp.overlay}
      {print && <Suspense fallback={null}><AvPrintSheet key={print} itemKey={print} onClose={() => setPrint(null)} /></Suspense>}
    </>
  );
}

/** 한 학년 104회차 — 학기 · 방학으로 접고, 주마다 A · B 두 칸 */
function WeekList({ gk, wp, profile }) {
  const [h, setH] = useState(() => weekIndexCached(gk));
  const [err, setErr] = useState(null);
  useEffect(() => { let live = true; loadWeekIndex(gk).then((v) => { if (live) setH(v); }).catch(() => { if (live) setErr("회차 목록을 불러오지 못했어요 — 연결을 확인해 주세요"); }); return () => { live = false; }; }, [gk]);
  const now = weekOfDate();
  const [open, setOpen] = useState(() => ({ [periodOf(now.week)]: true }));
  const [q, setQ] = useState("");
  const [unit, setUnit] = useState("");
  const nowRef = useRef(null);
  const scrolled = useRef(false);
  useEffect(() => {
    if (h && !scrolled.current && nowRef.current && !q && !unit) { scrolled.current = true; nowRef.current.scrollIntoView({ block: "center" }); }
  }, [h, q, unit]);
  if (err) return <p className="st-cdesc">{err}</p>;
  if (!h) return <p className="st-cdesc">회차 목록을 불러오는 중…</p>;
  const W = profile.watched || {};
  const units = [...new Set(h.sessions.map((m) => m.unit))];
  const qq = q.trim();
  const hit = (m) => (!unit || m.unit === unit || (m.units || []).includes(unit)) && (!qq || `${m.title} ${m.unit} ${m.kind} ${m.week}주`.includes(qq));
  const last = lastSeen(W, `w-${gk}-`);
  const lastM = last && h.sessions.find((m) => m.id === last.key);
  const nextM = lastM && (histDone(last.r) ? h.sessions[h.sessions.indexOf(lastM) + 1] : lastM);
  const nowM = h.sessions.find((m) => m.week === now.week && m.slot === "A");
  const go = (m) => { location.hash = `#/av/${m.id}`; };
  const filtering = !!(qq || unit);
  const cardOf = (m) => {
    const r = W[m.id], done = histDone(r), part = r && !done && r.max > 0;
    const c = weekCard(m);
    return (
      <button key={m.id} type="button" className={"st-sess wpk-able" + (wp.pressing === m.id ? " wpk-press" : "") + (done ? " done" : "")} {...wp.bind(c, () => go(m))}>
        <span className="k"><i aria-hidden="true">{KIND_ICON[m.kind]}</i>{m.slot} · {m.kind}{done && <em aria-label="다 봤어요">✓</em>}</span>
        <b>{m.title}</b>
        <small>{unitLabel(m.unit)}</small>
        {part && <span className="pg" aria-label={`${r.max}/${r.n}`}><i style={{ width: `${Math.round((r.max / r.n) * 100)}%` }} /></span>}
      </button>
    );
  };
  return (
    <>
      <div className="st-cont">
        {nextM && <button type="button" className="st-cont-b" onClick={() => go(nextM)}><small>{lastM === nextM ? "이어 보기" : "다음 회차"}</small><b>{nextM.week}주 {nextM.slot} · {nextM.title}</b></button>}
        {nowM && <button type="button" className="st-cont-b now" onClick={() => go(nowM)}><small>이번 주 · {weekLabel(now.year, now.week)}</small><b>{nowM.week}주 A · {nowM.title}</b></button>}
      </div>
      <div className="st-find">
        <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="찾기 — 받아올림, 분수, 12주 …" aria-label="회차 찾기" />
      </div>
      <div className="st-uchips" role="toolbar" aria-label="단원">
        <button type="button" className={!unit ? "on" : ""} onClick={() => setUnit("")}>전체</button>
        {units.map((u) => <button key={u} type="button" className={unit === u ? "on" : ""} onClick={() => setUnit(unit === u ? "" : u)}>{u.split(":")[1]}</button>)}
      </div>
      {h.gaps?.length > 0 && !filtering && <p className="st-gap">아직 회차가 없는 단원: {h.gaps.map((u) => u.split(":")[1]).join(" · ")} — 채우는 중이에요</p>}
      {PERIODS.map((p) => {
        const ms = h.sessions.filter((m) => m.week >= p.from && m.week <= p.to && hit(m));
        if (!ms.length) return null;
        const isOpen = filtering || !!open[p.key];
        const seen = ms.filter((m) => histDone(W[m.id])).length;
        return (
          <section key={p.key} className={"st-per" + (isOpen ? " open" : "")}>
            <button type="button" className="st-per-h" aria-expanded={isOpen} onClick={() => setOpen((o) => ({ ...o, [p.key]: !isOpen }))}>
              <b>{p.key}</b><small>{p.from} ~ {p.to}주 · {ms.length}회차{seen ? ` · ${seen} 봤어요` : ""}</small><span aria-hidden="true">{isOpen ? "▾" : "▸"}</span>
            </button>
            {isOpen && [...new Set(ms.map((m) => m.week))].map((w) => (
              <div key={w} className={"st-wk" + (w === now.week ? " now" : "")} ref={w === now.week ? nowRef : null}>
                <div className="wl"><b>{w}주</b><small>{weekLabel(now.year, w)}</small>{w === now.week && <em>이번 주</em>}</div>
                <div className="ws">{ms.filter((m) => m.week === w).map(cardOf)}</div>
              </div>
            ))}
          </section>
        );
      })}
    </>
  );
}

function AvSub({ path }) {
  const catId = path[0] || "";
  const cat = AV_CATS.find((c) => c.id === catId);
  if (!cat) {
    return (
      <>
        <p className="st-cdesc">교실 모니터에서 돌던 애니메이션 · 실험 · 해설을 내 화면으로 — 가로로 돌려 크게 보세요. 화면을 건드리면 조작 막대가 떠요.</p>
        <div className="st-list">
          {AV_CATS.map((c) => (
            <button key={c.id} className="st-folder" onClick={() => (location.hash = `#/study/av/${c.id}`)}>
              <span className="fi" aria-hidden="true">{c.icon}</span>
              <span className="nm"><b>{c.title}</b><small>{c.sub} · {avOfCat(c.id).length}가지</small></span>
              <span className="go" aria-hidden="true">›</span>
            </button>
          ))}
        </div>
      </>
    );
  }
  return (
    <>
      <div className="st-crumb">
        <button onClick={() => (location.hash = "#/study/av")}>시청각 학습</button><span aria-hidden="true">›</span><b>{cat.title}</b>
      </div>
      <p className="st-cdesc">{cat.sub}</p>
      {cat.id === "sol" ? <SolList /> : (
        <div className="st-list">
          {avOfCat(cat.id).map((it) => (
            <button key={it.key} className="st-item" onClick={() => (location.hash = `#/av/${it.key}`)}>
              <span className="st-avic" aria-hidden="true">{it.icon}</span>
              <span className="nm"><b>{it.title}</b><small className="wrap">{it.desc}</small></span>
              <span className="tag">{it.kind}</span>
            </button>
          ))}
        </div>
      )}
      {cat.id === "sol" && <p className="st-sec" style={{ fontWeight: 600 }}>컨셉 문제 세트마다 있는 「🎬 해설 영상」은 각 세트 화면에서 열어요.</p>}
    </>
  );
}

export default function Study({ sub = "", theme = "light" }) {
  const segs = (sub || "concept").split("?")[0].split("/").filter(Boolean);
  const s = segs[0] || "concept";
  return (
    <div className={`st-root st-${theme}`}>
      <style>{CSS}</style>
      <div className="st-wrap">
        {s === "practice" ? <PracticeSub /> : s === "exam" ? <ExamSub path={segs.slice(1)} /> : s === "sets" ? <SetsSub path={segs.slice(1)} /> : s === "av" ? <AvSub path={segs.slice(1)} /> : <ConceptSub />}
      </div>
    </div>
  );
}
