// 공부하기 탭 (#/study) — 서브탭: 개념 공부 · 연습문제 · 시험 보기 (셸이 상·하단을 그린다)
// sub: '' | 'concept' | 'practice' | 'exam'  (''=concept)
import { useEffect, useMemo, useState } from "react";
import { supabase } from "../supabaseClient";
import { listConcepts } from "../lib/concepts";
import { UNIT_NAMES, UNIT_ORDER } from "../lib/items";
import { readLastResult } from "../lib/setplay";
import { getRecentConcepts } from "../lib/review";
import { TEST_TYPES, describeTimer, loadRunsLocal, mergeRuns, describeRun, presetOf } from "../lib/exam";
import ItemPicker from "./solve/ItemPicker";
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
.st-badge { display: inline-flex; font-size: 9.5px; font-weight: 900; letter-spacing: .5px; color: #fff;
  border-radius: 999px; padding: 2px 7px; line-height: 1.4; }
.st-meta { display: flex; gap: 5px; flex-wrap: wrap; margin-top: 2px; }
.st-tag { font-size: 10.5px; font-weight: 700; color: var(--muted); border: 1px solid var(--border);
  border-radius: 999px; padding: 1px 7px; }
`;

function readLastConcept() {
  try { const v = JSON.parse(localStorage.getItem("ash.lastConcept") || "null"); if (v && v.id) return v; } catch { /* 무시 */ }
  const r = getRecentConcepts();
  return r[0] || null;
}

/* ── 개념 공부: 학기 고르고 개념 목록 ── */
function ConceptSub() {
  const [all, setAll] = useState(null);
  const last = useMemo(readLastConcept, []);
  const [unit, setUnit] = useState(() => {
    try { return localStorage.getItem("ash.study.unit") || (last?.id ? last.id.split("-").slice(0, 2).join("-") : "m1-1"); }
    catch { return "m1-1"; }
  });
  useEffect(() => { listConcepts().then(setAll).catch(() => setAll([])); }, []);
  const pick = (u) => { setUnit(u); try { localStorage.setItem("ash.study.unit", u); } catch { /* 무시 */ } };
  const byUnit = useMemo(() => {
    const m = {};
    for (const c of all || []) (m[c.unit_id] = m[c.unit_id] || []).push(c);
    for (const k of Object.keys(m)) m[k].sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
    return m;
  }, [all]);
  const rows = byUnit[unit] || [];
  return (
    <>
      <div className="st-chips">
        {UNIT_ORDER.map((u) => (
          <button key={u} className={"st-chip" + (u === unit ? " on" : "")} onClick={() => pick(u)}>
            {UNIT_NAMES[u] || u}{byUnit[u] ? <small>{byUnit[u].length}</small> : null}
          </button>
        ))}
      </div>
      {all === null ? <div className="st-empty">개념을 불러오는 중…</div>
        : rows.length === 0 ? <div className="st-empty">이 학기에는 아직 등록된 개념이 없어요.</div>
        : (
          <div className="st-list">
            {rows.map((c) => (
              <button key={c.id} className="st-item" onClick={() => (location.hash = `#/c/${encodeURIComponent(c.id)}`)}>
                <span className="num">{String(c.sort_order ?? "").padStart(2, "0")}</span>
                <span className="nm"><b>{c.title}</b>{c.subtitle && <small>{c.subtitle}</small>}</span>
                {last?.id === c.id && <span className="tag">이어보기</span>}
              </button>
            ))}
          </div>
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

function ExamSub() {
  const [runs, setRuns] = useState(null);
  useEffect(() => {
    let alive = true;
    (async () => {
      let remote = [];
      try {
        const { data } = await supabase.from("test_runs")
          .select("id, test_type, unit_id, concept_ids, n, correct_n, score, max, finished_at")
          .order("finished_at", { ascending: false }).limit(5);
        remote = data || [];
      } catch { /* 테이블 없거나 실패 — 로컬만 */ }
      if (alive) setRuns(mergeRuns(remote, loadRunsLocal(), 3));
    })();
    return () => { alive = false; };
  }, []);
  return (
    <>
      {EXAM_GROUPS.map(([label, codes]) => (
        <div key={label}>
          <p className="st-sec">{label}</p>
          <div className="st-grid">
            {codes.map((code) => {
              const t = presetOf(code) || TEST_TYPES.find((x) => x.code === code);
              if (!t) return null;
              return (
                <button key={code} className="st-tile" onClick={() => (location.hash = t.route || `#/solve/test/${t.code}`)}>
                  <span className="tt">{t.icon} {t.name}
                    {t.badge && <span className="st-badge" style={{ background: t.badge.color }}>{t.badge.text}</span>}
                  </span>
                  <span className="ds">{t.desc}</span>
                  <span className="st-meta">
                    {t.n > 0 && <span className="st-tag">{t.n}문항</span>}
                    <span className="st-tag">{describeTimer(t)}</span>
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      ))}
      <p className="st-sec">최근 응시</p>
      {runs === null ? <div className="st-empty">불러오는 중…</div>
        : runs.length === 0 ? <div className="st-empty">아직 응시한 시험이 없어요. 위에서 유형을 골라 시작해 보세요.</div>
        : (
          <div className="st-list">
            {runs.map((r) => {
              const d = describeRun(r, UNIT_NAMES);
              return (
                <button key={String(r.id)} className="st-item" onClick={() => (location.hash = d.link)}>
                  <span className="num" style={{ width: "auto", fontSize: 15 }}>{presetOf(r.test_type)?.icon || "🧪"}</span>
                  <span className="nm"><b>{d.name}{d.scope ? ` · ${d.scope}` : ""}</b><small>{d.score}{d.local ? " · 기기 저장" : ""}</small></span>
                </button>
              );
            })}
          </div>
        )}
    </>
  );
}

export default function Study({ sub = "", theme = "light" }) {
  const s = (sub || "concept").split("?")[0].split("/")[0] || "concept";
  return (
    <div className={`st-root st-${theme}`}>
      <style>{CSS}</style>
      <div className="st-wrap">
        {s === "practice" ? <PracticeSub /> : s === "exam" ? <ExamSub /> : <ConceptSub />}
      </div>
    </div>
  );
}
