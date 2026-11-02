// 공부하기 탭 (#/study) — 서브탭: 개념 공부 · 연습문제 · 컨셉 문제 · 시험 보기 (셸이 상·하단을 그린다)
// sub: '' | 'concept' | 'practice' | 'sets[/<범주>]' | 'exam'  (''=concept)
import { useEffect, useMemo, useState } from "react";
import { UNIT_NAMES, UNIT_ORDER } from "../lib/items";
import { readLastResult } from "../lib/setplay";
import { getRecentConcepts } from "../lib/review";
import { TEST_TYPES, describeTimer, presetOf, isExamOpen } from "../lib/exam";
import { swrConcepts } from "../lib/studyCache";
import { koFilter } from "../lib/koSearch";
import ItemPicker from "./solve/ItemPicker";
import { CATEGORIES, loadIndex, readProgress, setProgressUser, pad2 } from "../lib/conceptsets";
import { supabase } from "../supabaseClient";
import "./solve/solve.css";

const CSS = `
.st-root { min-height: 100vh; padding: 12px 14px 96px; box-sizing: border-box; background: var(--pbg);
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
.st-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
@media (max-width: 380px) { .st-grid { grid-template-columns: 1fr; } }
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
.st-icons { display: grid; grid-template-columns: repeat(auto-fill, minmax(76px, 1fr)); gap: 8px; }
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
function ExamSub() {
  return (
    <>
      <div className="st-devnote">🧩 <b>개념 묶음</b>과 📘 <b>단원 테스트</b>부터 열었어요 — 나머지 유형은 문항을 쌓는 대로 차례차례 열려요.</div>
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
        <p className="st-cdesc">주제 하나로 경우의 수와 확률을 끝까지 — 스포츠 · 음악 · 역사 · 판례까지, 실제 자료로 만든 50제 묶음이에요. 앱에서 바로 풀고 3단 해설을 보거나, 문제지 · 해설지 · OMR 카드를 인쇄해 풀고 OMR 사진으로 채점해요.</p>
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

export default function Study({ sub = "", theme = "light" }) {
  const segs = (sub || "concept").split("?")[0].split("/").filter(Boolean);
  const s = segs[0] || "concept";
  return (
    <div className={`st-root st-${theme}`}>
      <style>{CSS}</style>
      <div className="st-wrap">
        {s === "practice" ? <PracticeSub /> : s === "exam" ? <ExamSub /> : s === "sets" ? <SetsSub path={segs.slice(1)} /> : <ConceptSub />}
      </div>
    </div>
  );
}
