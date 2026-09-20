// 시험 응시 (#/solve/test) — 8가지 시험 유형(개념 묶음 · 단원 · 연산 · 산과 · 모의고사 · Ash · Rain · Out)
//   #/solve/test                    유형 고르기 (타일 8개) + 최근 응시
//   #/solve/test/<type>             범위 고르기(개념 또는 단원) → 확인 카드 → 응시 → 결과
//   #/solve/test/<type>/<scopeId>   범위가 정해진 채로 확인 카드부터 (최근 응시에서 다시 보기)
//   산과(sangwa) 는 러너 없이 #/solve/essay 로 보낸다.
// props: { sub, hash }  (SolveRouter: #/solve/test* → <Exam sub hash/>)
// 기록: attempts(logAttempt, set_id "test:<type>:<base36>") + test_runs(없으면 localStorage "ash.test.runs", 최근 30건)
// [확정] 시험에는 Ⓟ/Ⓓ 보상이 없다 — 이 화면은 재화를 표시하지 않는다.
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../../supabaseClient";
import SolveShell, { useToast } from "./SolveShell";
import ItemPicker from "./ItemPicker";
import ItemQuestion from "../../components/ItemQuestion";
import ItemView from "../../components/ItemView";
import MathText from "../../components/MathText";
import { listConcepts } from "../../lib/concepts";
import { UNIT_NAMES, UNIT_ORDER, liveCountsByUnit, fetchLiveItems, logAttempt } from "../../lib/items";
import { kindOf } from "../../lib/answers";
import { saveItemWrongNotes } from "../../lib/wrongnotes";
import { correctAnswerText, myAnswerText, questionPreview, fmtClock, wrongEntries } from "../../lib/setplay";
import {
  TEST_TYPES, presetOf, describeTimer, presetRules, fetchPlan, buildSelection,
  emptyAnswer, isAnswered, answeredCount, judgeAll, itemPoints, scoreRun, examMessage,
  fmtTimer, remainingSec, isTimerWarn, newRunId, runToRow, saveRunLocal, loadRunsLocal, mergeRuns, describeRun,
} from "../../lib/exam";
import "./solve.css";
import "../../components/item.css";

const CSS = `
.ex-tiles { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }
@media (max-width:420px) { .ex-tiles { grid-template-columns:1fr; } }
.ex-tile .tt { display:flex; align-items:center; gap:6px; flex-wrap:wrap; }
.ex-meta { display:flex; gap:5px; flex-wrap:wrap; margin-top:4px; }
.ex-tag { font-size:11px; font-weight:700; color:var(--muted); border:1px solid var(--border); border-radius:999px; padding:1px 7px; }
.ex-badge { display:inline-flex; align-items:center; font-size:10.5px; font-weight:900; letter-spacing:.6px; padding:2px 8px; border-radius:999px; color:#fff; background:var(--accent); line-height:1.4; }
.ex-title { display:flex; align-items:center; gap:8px; font-size:18px; font-weight:800; line-height:1.4; }
.ex-err { margin-top:10px; font-size:13px; color:var(--bad); font-weight:700; line-height:1.5; }
.ex-rules { margin:0; padding-left:18px; font-size:13.5px; line-height:1.7; }
.ex-note { font-size:12.5px; color:var(--muted); line-height:1.6; margin:10px 0 0; padding:10px 12px; border-radius:10px; background:var(--surface2); }
.ex-units { display:flex; flex-wrap:wrap; gap:6px; }
.ex-units .sv-chip:disabled { opacity:.45; cursor:default; }
.ex-recent .sv-item .tx b { font-weight:800; }
.ex-head { position:sticky; top:0; z-index:5; display:flex; align-items:center; gap:8px; padding:8px 12px; margin:0 0 6px; background:var(--surface); border:1px solid var(--border); border-radius:12px; }
.ex-head.ex-ash, .sv-card.ex-ash { border-color:#7C3AED; box-shadow:0 0 0 2px color-mix(in srgb, #7C3AED 22%, transparent); background:linear-gradient(90deg, color-mix(in srgb, #7C3AED 14%, var(--surface)), var(--surface) 70%); }
.ex-head .ex-name { font-size:13.5px; font-weight:800; white-space:nowrap; }
.ex-head .ex-scope { flex:1; min-width:0; font-size:12px; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.ex-timer { flex:none; font-variant-numeric:tabular-nums; font-weight:900; font-size:17px; white-space:nowrap; }
.ex-timer.warn { color:var(--bad); animation:ex-blink 1s steps(2) infinite; }
.ex-timer.over { color:var(--bad); }
@keyframes ex-blink { 50% { opacity:.4; } }
.ex-bar { height:4px; border-radius:999px; background:var(--surface3); overflow:hidden; margin:0 0 10px; }
.ex-bar > i { display:block; height:100%; background:var(--accent); transition:width .25s linear; }
.ex-bar.warn > i { background:var(--bad); }
.ex-qhead { display:flex; align-items:center; gap:8px; margin-bottom:6px; }
.ex-pts { font-size:12px; font-weight:800; color:var(--accent); border:1px solid var(--accent); border-radius:999px; padding:1px 8px; }
.ex-kind { font-size:11.5px; color:var(--muted); }
.ex-short { display:flex; gap:8px; margin-top:10px; align-items:stretch; }
.ex-short .sv-in { flex:1 1 auto; min-width:0; }
.ex-short .sv-btn { flex:none; }
.ex-hint { font-size:11.5px; color:var(--muted); margin-top:6px; line-height:1.5; }
.ex-nav { display:flex; align-items:center; gap:8px; margin:12px 0; }
.ex-nav .sv-btn { flex:1; }
.ex-nav .ex-pos { flex:none; min-width:64px; text-align:center; font-size:13px; font-weight:800; font-variant-numeric:tabular-nums; }
.ex-grid-cap { display:flex; justify-content:space-between; font-size:12px; color:var(--muted); margin:0 0 8px; }
.ex-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(38px, 1fr)); gap:6px; }
.ex-grid.dense { grid-template-columns:repeat(10, 1fr); gap:3px; }
.ex-cell { height:34px; padding:0; border-radius:8px; border:1px solid var(--border); background:var(--surface); color:var(--muted); font-size:12.5px; font-weight:700; cursor:pointer; font-variant-numeric:tabular-nums; }
.ex-grid.dense .ex-cell { height:26px; font-size:11px; border-radius:6px; }
.ex-cell.done { background:var(--accent); border-color:var(--accent); color:#fff; }
.ex-cell.cur { box-shadow:0 0 0 2px var(--accent); color:var(--text); }
.ex-cell.done.cur { color:#fff; }
.ex-cell:disabled { cursor:default; }
.ex-submit { margin-top:14px; }
.ex-modal-bg { position:fixed; inset:0; background:rgba(0,0,0,.45); display:flex; align-items:center; justify-content:center; z-index:60; padding:20px; }
.ex-modal { background:var(--surface); color:var(--text); border-radius:16px; padding:18px 16px; width:100%; max-width:360px; box-shadow:0 12px 40px rgba(0,0,0,.3); }
.ex-modal h3 { margin:0 0 6px; font-size:17px; }
.ex-modal p { margin:0 0 14px; font-size:13.5px; color:var(--muted); line-height:1.6; }
.ex-mrow { display:flex; flex-direction:column; gap:8px; }
.ex-score { text-align:center; padding:20px 14px; }
.ex-score .ex-badge { font-size:11.5px; padding:3px 10px; }
.ex-big { font-size:40px; font-weight:900; line-height:1.1; letter-spacing:-1px; margin-top:8px; }
.ex-big .ex-of { font-size:18px; font-weight:700; color:var(--muted); letter-spacing:0; }
.ex-pct { font-size:14px; font-weight:800; color:var(--accent); margin:2px 0 6px; }
.ex-score .sv-bar { margin:10px auto 0; max-width:280px; }
.ex-msg { font-size:13.5px; color:var(--muted); margin:10px 0 0; line-height:1.6; }
.ex-saved { font-size:11.5px; color:var(--muted); margin-top:8px; }
.ex-filter { display:flex; gap:6px; margin:0 0 8px; }
.ex-row { border:1px solid var(--border); border-radius:12px; background:var(--surface); overflow:hidden; }
.ex-rowbtn { display:flex; align-items:center; gap:8px; width:100%; padding:10px 12px; background:none; border:none; color:var(--text); text-align:left; cursor:pointer; font:inherit; }
.ex-mark { flex:none; width:22px; height:22px; border-radius:999px; display:inline-flex; align-items:center; justify-content:center; font-size:13px; font-weight:900; color:#fff; }
.ex-mark.ok { background:var(--good); }
.ex-mark.bad { background:var(--bad); }
.ex-rowno { flex:none; font-size:12px; color:var(--muted); font-weight:700; }
.ex-rowq { flex:1; font-size:13.5px; line-height:1.45; overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; }
.ex-rowpt { flex:none; font-size:11.5px; color:var(--muted); white-space:nowrap; }
.ex-chev { flex:none; color:var(--muted); font-size:12px; }
.ex-ansline { display:flex; flex-wrap:wrap; gap:4px 10px; align-items:baseline; padding:0 12px 10px 42px; font-size:13.5px; }
.ex-ansline .ex-lab { font-size:11.5px; color:var(--muted); margin-right:2px; }
.ex-row .sv-card { border:none; border-radius:0; margin:0; padding:6px 12px 12px; background:var(--surface2); }
.ex-actions { display:flex; flex-direction:column; gap:8px; margin-top:16px; }
`;

// ── 공용 ─────────────────────────────────────────────────────────────────────
let _conceptsP = null;
function conceptsOnce() {
  if (!_conceptsP) _conceptsP = listConcepts().catch(() => { _conceptsP = null; return []; });
  return _conceptsP;
}
const toTop = () => { try { window.scrollTo({ top: 0, behavior: "smooth" }); } catch { /* 무시 */ } };
const dec = (v) => { if (!v) return null; try { return decodeURIComponent(v); } catch { return v; } };
const fmtDate = (iso) => {
  const t = iso ? new Date(iso) : null;
  if (!t || Number.isNaN(t.getTime())) return "";
  try { return t.toLocaleDateString("ko-KR", { month: "short", day: "numeric" }); } catch { return ""; }
};
const iconOf = (code) => presetOf(code)?.icon || "📄";
/** 시험에서는 "건너뜀" 대신 "무응답" */
const myAns = (item, r) => (!r || r.skipped ? "(무응답)" : myAnswerText(item, r));

/** #/solve/test/<type>/<scopeId> → { type, scopeId } (hash 우선, 없으면 sub) */
function parseRoute(hash, sub) {
  const parts = String(hash || "").replace(/^#\/?/, "").split("?")[0].split("/").filter(Boolean);   // ["solve","test","unit","m1-1"]
  let type = parts[2], scopeId = parts[3];
  if (!type && sub) {
    const s = String(sub).split("?")[0].split("/").filter(Boolean);
    type = s[0]; scopeId = s[1];
  }
  return { type: dec(type), scopeId: dec(scopeId) };
}

function Badge({ preset, style }) {
  if (!preset?.badge) return null;
  return <span className="ex-badge" style={{ background: preset.badge.color, ...style }}>{preset.badge.text}</span>;
}

function Modal({ title, text, children }) {
  return (
    <div className="ex-modal-bg">
      <div className="ex-modal" role="dialog" aria-modal="true">
        <h3>{title}</h3>
        {text && <p>{text}</p>}
        <div className="ex-mrow">{children}</div>
      </div>
    </div>
  );
}

// ── 진입 ─────────────────────────────────────────────────────────────────────
export default function Exam({ sub, hash }) {
  const [toast, setToast] = useToast();
  const [uid, setUid] = useState(undefined);      // undefined 확인 중 · null 로그인 없음
  useEffect(() => {
    let alive = true;
    supabase.auth.getUser().then(({ data }) => { if (alive) setUid(data?.user?.id || null); }).catch(() => { if (alive) setUid(null); });
    return () => { alive = false; };
  }, []);

  const h = hash ?? (typeof location !== "undefined" ? location.hash : "");
  const { type, scopeId } = parseRoute(h, sub);
  const preset = type ? presetOf(type) : null;

  let body;
  if (!type) body = <TypePicker uid={uid} toast={toast} />;
  else if (!preset) {
    body = (
      <SolveShell title="시험 응시" back="#/solve/test" toast={toast}>
        <div className="sv-empty">없는 시험 유형이에요.<br /><a href="#/solve/test">시험 고르기</a></div>
      </SolveShell>
    );
  } else if (preset.route) body = <RouteCard preset={preset} toast={toast} />;
  else body = <ExamFlow key={`${type}:${scopeId || ""}`} preset={preset} scopeId={scopeId} uid={uid} toast={toast} setToast={setToast} />;
  return <><style>{CSS}</style>{body}</>;
}

// ── 유형 고르기 + 최근 응시 ───────────────────────────────────────────────────
function TypePicker({ uid, toast }) {
  const [runs, setRuns] = useState(null);
  useEffect(() => {
    if (uid === undefined) return;
    let alive = true;
    (async () => {
      let db = [];
      if (uid) {
        try {
          const { data, error } = await supabase.from("test_runs")
            .select("id, test_type, unit_id, n, correct_n, score, max, finished_at, meta")
            .eq("user_id", uid).order("finished_at", { ascending: false }).limit(10);
          if (!error && Array.isArray(data)) db = data;
        } catch { /* 표가 아직 없을 수 있다 → 로컬만 */ }
      }
      if (alive) setRuns(mergeRuns(db, loadRunsLocal(), 8));
    })();
    return () => { alive = false; };
  }, [uid]);

  return (
    <SolveShell title="시험 응시" back="#/study/exam" toast={toast}
      sub="유형을 고르면 범위를 정하고 바로 시작해요. 결과는 응시 기록으로 남아요.">
      <div className="ex-tiles">
        {TEST_TYPES.map((t) => (
          <button key={t.code} className="sv-tile ex-tile" onClick={() => { location.hash = t.route || `#/solve/test/${t.code}`; }}>
            <span className="ic">{t.icon}</span>
            <span className="tt">{t.name}<Badge preset={t} /></span>
            <span className="ds">{t.desc}</span>
            <span className="ex-meta">
              {t.n > 0 && <span className="ex-tag">{t.n}문항</span>}
              <span className="ex-tag">{describeTimer(t)}</span>
              <span className="ex-tag">{t.scope === "concept" ? "개념 하나" : "단원 하나"}</span>
              {t.route && <span className="ex-tag">서술형 자가채점으로</span>}
            </span>
          </button>
        ))}
      </div>

      <div className="sv-sec">최근 응시</div>
      {runs === null ? <div className="sv-muted">불러오는 중…</div>
      : !runs.length ? <div className="sv-empty">아직 응시한 시험이 없어요.<br />위에서 유형을 골라 시작해 보세요.</div>
      : (
        <div className="sv-list ex-recent">
          {runs.map((r) => {
            const d = describeRun(r, UNIT_NAMES);
            return (
              <button key={String(r.id)} className="sv-item" onClick={() => { location.hash = d.link; }}>
                <span className="no">{iconOf(r.test_type)}</span>
                <span className="tx"><b>{d.name}</b>{d.scope ? ` · ${d.scope}` : ""} · {d.score}{d.local && <span className="sv-small"> · 기기 저장</span>}</span>
                <span className="rt">{fmtDate(d.when)}</span>
              </button>
            );
          })}
        </div>
      )}
    </SolveShell>
  );
}

// ── 산과 시험 — 서술형 자가채점으로 안내 ───────────────────────────────────────
function RouteCard({ preset, toast }) {
  return (
    <SolveShell title={preset.name} back="#/solve/test" toast={toast}>
      <div className="sv-card">
        <div className="ex-title"><span>{preset.icon}</span>{preset.name}</div>
        <p className="sv-sub" style={{ marginTop: 8 }}>{preset.desc}</p>
        <p className="sv-sub">산과 시험은 서술·증명 문항이라 시간을 재는 대신 채점 기준표로 스스로 채점해요. 서술형 자가채점 화면에서 문항을 골라 시작하면 돼요.</p>
        <button className="sv-btn pri full" onClick={() => { location.hash = preset.route; }}>서술형 자가채점으로 가기</button>
      </div>
    </SolveShell>
  );
}

// ── 흐름: 범위 → 확인 → 응시 → 결과 ──────────────────────────────────────────
function ExamFlow({ preset, scopeId, uid, toast, setToast }) {
  const isConcept = preset.scope === "concept";
  const [scope, setScope] = useState(() => (
    !isConcept && scopeId && UNIT_NAMES[scopeId] ? { kind: "unit", id: scopeId, title: UNIT_NAMES[scopeId], unitId: scopeId } : null
  ));
  const [resolving, setResolving] = useState(() => isConcept && !!scopeId);
  const [phase, setPhase] = useState(() => (scope ? "confirm" : "scope"));   // scope | confirm | loading | play | result
  const [counts, setCounts] = useState(null);
  const [items, setItems] = useState([]);
  const [notice, setNotice] = useState(null);
  const [err, setErr] = useState(null);
  const [run, setRun] = useState(null);           // { runId, results, ctx, score, saved }
  const uidRef = useRef(uid);
  uidRef.current = uid;

  // 개념 범위 딥링크 → 개념 제목 찾기
  useEffect(() => {
    if (!isConcept || !scopeId) return;
    let alive = true;
    conceptsOnce().then((list) => {
      if (!alive) return;
      const c = (list || []).find((x) => x.id === scopeId);
      if (c) { setScope({ kind: "concept", id: c.id, title: c.title, unitId: c.unit_id }); setPhase("confirm"); }
      setResolving(false);
    });
    return () => { alive = false; };
  }, [isConcept, scopeId]);

  // 단원별 공개 문항 수 (단원 고르기)
  useEffect(() => {
    if (isConcept || phase !== "scope") return;
    let alive = true;
    liveCountsByUnit().then((c) => { if (alive) setCounts(c || {}); }).catch(() => { if (alive) setCounts({}); });
    return () => { alive = false; };
  }, [isConcept, phase]);

  useEffect(() => { toTop(); }, [phase]);

  const pickScope = (id) => { location.hash = `#/solve/test/${preset.code}/${encodeURIComponent(id)}`; };
  const rechoose = () => { location.hash = `#/solve/test/${preset.code}`; };

  /** 출제 계획대로 문항을 모아 시험을 시작한다 */
  const start = async () => {
    if (!scope) return;
    setErr(null); setNotice(null); setPhase("loading");
    try {
      const plan = fetchPlan(preset, scope);
      const primary = plan.filter((p) => p.stage !== "fill"), fill = plan.filter((p) => p.stage === "fill");
      let failed = 0;
      const fetchOne = async ({ stage, ...opts }) => { try { return await fetchLiveItems(opts); } catch { failed += 1; return []; } };
      let pool = (await Promise.all(primary.map(fetchOne))).flat();
      if (failed >= primary.length && primary.length) throw new Error("fetch");
      if (fill.length && new Set(pool.map((x) => x.id)).size < preset.n) pool = pool.concat((await Promise.all(fill.map(fetchOne))).flat());
      const sel = buildSelection(preset, pool);
      if (!sel.items.length) { setPhase("confirm"); setErr("이 범위에는 아직 공개된 문항이 없어요. 다른 범위를 골라 주세요."); return; }
      const msgs = [];
      if (sel.short) msgs.push(`준비된 문항이 ${sel.items.length}개뿐이라 ${sel.items.length}문항으로 진행해요.`);
      if (sel.relaxed) msgs.push("조건에 맞는 문항이 부족해서 다른 난이도도 섞었어요.");
      setNotice(msgs.length ? msgs.join(" ") : null);
      setItems(sel.items); setRun(null); setPhase("play");
    } catch {
      setPhase("confirm"); setErr("문항을 불러오지 못했어요. 잠시 후 다시 시도해 주세요.");
    }
  };

  /** 제출 → 채점 → 결과 화면 (기록은 뒤에서) */
  const finish = ({ answers, elapsed, startedAt, finishedAt, timedOut, overtimeSec }) => {
    const results = judgeAll(items, answers, elapsed);
    const runId = newRunId(preset.code, startedAt);
    const ctx = {
      unitId: scope.unitId || (scope.kind === "unit" ? scope.id : null),
      conceptId: scope.kind === "concept" ? scope.id : null,
      scopeTitle: scope.title, startedAt, finishedAt, timedOut, overtimeSec,
      short: Math.max(0, preset.n - items.length), runId,
    };
    setRun({ runId, results, ctx, score: scoreRun(preset, results), saved: null });
    setPhase("result");
    persist(runId, results, ctx);
  };

  /** 기록 — test_runs(실패하면 localStorage) 먼저, attempts 는 뒤에 10개씩 (rain 100문항). 실패해도 화면을 막지 않는다 */
  const persist = async (runId, results, ctx) => {
    const u = uidRef.current || null;
    let saved = "local";
    try {
      const row = runToRow(u, preset, ctx, results);
      if (u) {
        try { const { error } = await supabase.from("test_runs").insert(row); if (!error) saved = "db"; }
        catch { /* 표가 아직 없음 등 → 로컬 */ }
      }
      if (saved !== "db") saveRunLocal(row);
    } catch { /* 무시 */ }
    setRun((prev) => (prev && prev.runId === runId ? { ...prev, saved } : prev));
    if (!u) return;
    for (let i = 0; i < results.length; i += 10) {
      await Promise.allSettled(results.slice(i, i + 10).map((r, j) => logAttempt({
        uid: u, item: r.item, rawAnswer: r.rawAnswer, correct: r.correct, chosenIndex: r.chosenIndex, chosenChoice: r.chosenChoice,
        elapsedSec: r.elapsedSec, hintLevel: 0, solutionSeen: false, retryN: 0, setId: runId, seq: i + j + 1,
      })));
    }
  };

  // ── 범위 고르기 ──
  if (phase === "scope") {
    if (resolving) return <SolveShell title={preset.name} back="#/solve/test" toast={toast}><div className="sv-muted">범위를 확인하는 중…</div></SolveShell>;
    if (isConcept) {
      return (
        <SolveShell title={preset.name} back="#/solve/test" toast={toast}>
          <ItemPicker mode="concept" filter={{ qtypes: ["choice", "short"] }}
            hint={`개념을 고르면 그 개념의 문항 ${preset.n}개로 시험을 봐요. ${describeTimer(preset)}.`}
            onPickConcept={(c) => pickScope(c.id)} />
        </SolveShell>
      );
    }
    let last = null;
    try { last = localStorage.getItem("ash.solve.unit"); } catch { /* 무시 */ }
    return (
      <SolveShell title={preset.name} back="#/solve/test" toast={toast}
        sub={`단원을 고르면 그 단원 전체에서 ${preset.n}문항이 나와요. ${describeTimer(preset)}.`}>
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>단원</div>
          <div className="ex-units">
            {UNIT_ORDER.map((u) => {
              const c = counts ? counts[u] : undefined;
              return (
                <button key={u} className={"sv-chip" + (u === last ? " on" : "")} disabled={c === 0} onClick={() => pickScope(u)}>
                  {UNIT_NAMES[u]}{c != null ? <span className="sv-small"> {c}</span> : null}
                </button>
              );
            })}
          </div>
          {counts && UNIT_ORDER.every((u) => !counts[u]) && <div className="sv-empty" style={{ marginTop: 12 }}>아직 공개된 문항이 없어요.</div>}
        </div>
      </SolveShell>
    );
  }

  // ── 확인 카드 ──
  if (phase === "confirm" || phase === "loading") {
    return (
      <SolveShell title={preset.name} back="#/solve/test" toast={toast}>
        <div className={"sv-card" + (preset.code === "ash" ? " ex-ash" : "")}>
          <div className="ex-title"><span>{preset.icon}</span>{preset.name}<Badge preset={preset} /></div>
          <div className="sv-small" style={{ marginTop: 4 }}>
            {scope?.title}{scope?.kind === "concept" && scope.unitId ? ` · ${UNIT_NAMES[scope.unitId] || scope.unitId}` : ""}
          </div>
          <div className="sv-sec">이 시험은</div>
          <ul className="ex-rules">{presetRules(preset).map((r, i) => <li key={i}>{r}</li>)}</ul>
          {preset.note && <p className="ex-note">{preset.note}</p>}
          {err && <div className="ex-err">{err}</div>}
          <button className="sv-btn pri full" style={{ marginTop: 16 }} disabled={phase === "loading" || !scope} onClick={start}>
            {phase === "loading" ? "문항을 고르는 중…" : "시작"}
          </button>
          <button className="sv-btn ghost full" style={{ marginTop: 8 }} disabled={phase === "loading"} onClick={rechoose}>범위 다시 고르기</button>
        </div>
      </SolveShell>
    );
  }

  // ── 응시 ──
  if (phase === "play") {
    return (
      <Runner preset={preset} scope={scope} items={items} notice={notice} toast={toast}
        onSubmit={finish} onQuit={() => { setItems([]); setPhase("confirm"); }} />
    );
  }

  // ── 결과 ──
  if (phase === "result" && run) {
    return <Result preset={preset} scope={scope} items={items} run={run} notice={notice} uid={uid} toast={toast} setToast={setToast} onRetry={start} />;
  }
  return <SolveShell title={preset.name} back="#/solve/test" toast={toast}><div className="sv-muted">…</div></SolveShell>;
}

// ── 러너: 타이머 · 문항 · 답안 현황 · 제출 ───────────────────────────────────
// props: { preset, scope:{kind,id,title}, items, notice, toast, onSubmit({answers, elapsed, startedAt, finishedAt, timedOut, overtimeSec}), onQuit }
export function Runner({ preset, scope, items, notice, toast, onSubmit, onQuit }) {
  const n = items.length;
  const timer = preset.timer || { kind: "none", sec: 0 };
  const total = timer.kind === "total" && timer.sec > 0;
  const perItem = timer.kind === "item" && timer.sec > 0;
  const linear = perItem;                          // 문항당 제한 시간 → 앞으로만 간다
  const dense = preset.grid === "dense";
  const showPts = preset.pointsMode === "points" || preset.pointsMode === "scaled100";

  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState(() => items.map(() => emptyAnswer()));
  const [now, setNow] = useState(() => Date.now());
  const [modal, setModal] = useState(null);        // null | timeover | submit | quit
  const [overtime, setOvertime] = useState(false); // soft 타이머: 시간이 끝난 뒤 계속 풀기
  const startedAtRef = useRef(Date.now());
  const enteredRef = useRef(Date.now());
  const elapsedRef = useRef(items.map(() => 0));
  const idxRef = useRef(0);
  const doneRef = useRef(false);
  const warnedRef = useRef(false);
  const answersRef = useRef(answers);
  const onSubmitRef = useRef(onSubmit);
  onSubmitRef.current = onSubmit;
  const inputRef = useRef(null);

  // 시계 — 문항당 타이머는 0.25초, 총 타이머는 0.5초마다
  useEffect(() => {
    if (!total && !perItem) return;
    const t = setInterval(() => setNow(Date.now()), perItem ? 250 : 500);
    return () => clearInterval(t);
  }, [total, perItem]);

  useEffect(() => {
    toTop();
    if (kindOf(items[idx]) !== "choice") { const t = setTimeout(() => inputRef.current?.focus(), 0); return () => clearTimeout(t); }
  }, [idx]); // eslint-disable-line react-hooks/exhaustive-deps

  const flush = () => {
    const t = Date.now();
    elapsedRef.current[idxRef.current] = (elapsedRef.current[idxRef.current] || 0) + (t - enteredRef.current) / 1000;
    enteredRef.current = t;
  };
  const goTo = (i) => {
    if (doneRef.current || i < 0 || i >= n || i === idxRef.current) return;
    flush(); idxRef.current = i; setIdx(i);
  };
  const submit = () => {
    if (doneRef.current) return;
    doneRef.current = true;
    flush();
    const finishedAt = Date.now();
    const rem = total ? remainingSec(preset, { startedAt: startedAtRef.current, now: finishedAt }) : null;
    onSubmitRef.current?.({
      answers: answersRef.current, elapsed: elapsedRef.current.map((s) => Math.round(s)),
      startedAt: startedAtRef.current, finishedAt,
      timedOut: rem != null && rem <= 0, overtimeSec: rem != null && rem < 0 ? -rem : 0,
    });
  };
  const setAns = (i, patch) => {
    const next = answersRef.current.slice();
    next[i] = { ...(next[i] || emptyAnswer()), ...patch };
    answersRef.current = next; setAnswers(next);
  };
  const advance = () => { if (idxRef.current + 1 < n) goTo(idxRef.current + 1); else if (linear) submit(); else requestSubmit(); };
  const requestSubmit = () => {
    if (doneRef.current) return;
    const left = n - answeredCount(items, answersRef.current);
    if (left > 0) setModal("submit"); else submit();
  };
  const onSelect = (ci) => {
    if (doneRef.current || modal) return;
    setAns(idxRef.current, { sel: ci });
    if (linear) advance();
  };

  const remaining = total ? remainingSec(preset, { startedAt: startedAtRef.current, now }) : null;
  const itemRemaining = perItem ? remainingSec(preset, { enteredAt: enteredRef.current, now }) : null;

  // 총 제한 시간 종료 → 모달 (한 번만; soft 면 계속 풀기 가능)
  useEffect(() => {
    if (!total || overtime || warnedRef.current || doneRef.current) return;
    if (remaining <= 0) { warnedRef.current = true; setModal("timeover"); }
  }, [remaining, total, overtime]);

  // 문항당 제한 시간 종료 → 자동으로 다음 (무응답은 오답), 마지막이면 제출
  useEffect(() => {
    if (!perItem || doneRef.current || modal) return;
    if (itemRemaining <= 0) advance();
  }, [itemRemaining, perItem, modal]); // eslint-disable-line react-hooks/exhaustive-deps

  // 객관식: 숫자 키 1~5 로 고르기, Enter 로 다음
  const cur = items[idx];
  const kind = kindOf(cur);
  useEffect(() => {
    if (kind !== "choice" || modal || typeof window === "undefined") return;
    const h = (e) => {
      if (e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
      const tag = e.target?.tagName || "";
      if (/^(INPUT|TEXTAREA|SELECT)$/.test(tag)) return;
      if (/^[1-5]$/.test(e.key) && cur?.choices?.[Number(e.key) - 1] != null) onSelect(Number(e.key) - 1);
      else if (e.key === "Enter" && !/^(BUTTON|A)$/.test(tag)) advance();   // 버튼 위의 Enter 는 그 버튼의 몫
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [kind, modal, cur]); // eslint-disable-line react-hooks/exhaustive-deps

  const a = answers[idx] || emptyAnswer();
  const answered = answeredCount(items, answers);
  let timerText, timerCls = "ex-timer", warn = false;
  if (total) {
    if (overtime || remaining < 0) { timerText = `+${fmtTimer(Math.max(0, -remaining))}`; timerCls += " over"; }   // 초과 시간
    else { timerText = fmtTimer(remaining); warn = isTimerWarn(preset, remaining); if (warn) timerCls += " warn"; }
  } else if (perItem) {
    const r = Math.max(0, itemRemaining ?? 0);
    timerText = `${r}초`; warn = isTimerWarn(preset, r); if (warn) timerCls += " warn";
  } else timerText = `${answered} / ${n}`;
  const barPct = perItem
    ? Math.max(0, Math.min(100, ((enteredRef.current + timer.sec * 1000 - now) / (timer.sec * 1000)) * 100))   // ms 단위로 부드럽게
    : n ? (answered / n) * 100 : 0;
  const left = n - answered;

  return (
    <SolveShell title="시험 응시" back={null} toast={toast}
      right={<button className="sv-btn sm ghost" onClick={() => setModal("quit")}>나가기</button>}>
      <div className={"ex-head" + (preset.code === "ash" ? " ex-ash" : "")}>
        {preset.badge ? <Badge preset={preset} /> : <span className="ex-name">{preset.name}</span>}
        <span className="ex-scope">{scope?.title || ""}</span>
        <span className={timerCls} aria-live="polite">{timerText}</span>
      </div>
      <div className={"ex-bar" + (warn ? " warn" : "")}><i style={{ width: `${barPct}%` }} /></div>
      {notice && <p className="sv-sub" style={{ marginTop: 0 }}>{notice}</p>}

      {cur && (
        <div className="sv-card">
          <div className="ex-qhead">
            <span className="iq-no">{idx + 1}</span>
            {showPts && <span className="ex-pts">{itemPoints(cur)}점</span>}
            <span className="ex-kind">{kind === "choice" ? "객관식" : "단답"}</span>
          </div>
          <ItemQuestion item={cur} index={null} selected={a.sel} onSelect={kind === "choice" ? onSelect : undefined} />
          {kind !== "choice" && (
            <>
              <div className="ex-short">
                <input ref={inputRef} className="sv-in" type="text" inputMode="text" autoComplete="off" autoCapitalize="off" autoCorrect="off" spellCheck={false}
                  enterKeyHint="next" placeholder="답 입력 (예: 3, 1/2, 60°, 3π)" value={a.text}
                  onChange={(e) => setAns(idx, { text: e.target.value })}
                  onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); advance(); } }} />
                <button className="sv-btn pri" onClick={advance}>{idx + 1 < n ? "다음" : "제출"}</button>
              </div>
              <div className="ex-hint">분수는 1/2 처럼, 각도는 60 또는 60°, π는 π 또는 pi 로 써도 돼요. Enter 를 누르면 다음 문제로 가요.</div>
            </>
          )}
        </div>
      )}

      <div className="ex-nav">
        {!linear && <button className="sv-btn" disabled={idx === 0} onClick={() => goTo(idx - 1)}>이전</button>}
        <span className="ex-pos">{idx + 1} / {n}</span>
        {linear
          ? <button className="sv-btn" onClick={advance}>{idx + 1 < n ? "넘기기" : "제출"}</button>
          : <button className="sv-btn" disabled={idx + 1 >= n} onClick={() => goTo(idx + 1)}>다음</button>}
      </div>

      <div className="sv-card">
        <div className="ex-grid-cap"><span>답안 현황{linear ? " (연산 테스트는 앞으로만 가요)" : ""}</span><span>{answered} / {n} 답함</span></div>
        <div className={"ex-grid" + (dense ? " dense" : "")}>
          {items.map((it, i) => (
            <button key={it.id || i} type="button" disabled={linear}
              className={"ex-cell" + (isAnswered(it, answers[i]) ? " done" : "") + (i === idx ? " cur" : "")}
              onClick={() => goTo(i)} aria-label={`${i + 1}번`}>{i + 1}</button>
          ))}
        </div>
        <button className="sv-btn pri full ex-submit" onClick={requestSubmit}>제출{left > 0 ? ` (안 푼 문항 ${left})` : ""}</button>
      </div>

      {modal === "timeover" && (
        <Modal title="시간이 끝났어요" text={timer.soft ? "지금까지 쓴 답으로 제출할 수 있어요. 조금 더 풀고 싶으면 계속 풀기를 눌러요 (초과 시간이 기록에 남아요)." : "지금까지 쓴 답으로 제출할게요."}>
          <button className="sv-btn pri full" onClick={submit}>제출하기</button>
          {timer.soft && <button className="sv-btn full" onClick={() => { setOvertime(true); setModal(null); }}>계속 풀기</button>}
        </Modal>
      )}
      {modal === "submit" && (
        <Modal title="제출할까요?" text={`아직 안 푼 문항이 ${left}개 있어요. 안 푼 문항은 오답으로 채점돼요.`}>
          <button className="sv-btn pri full" onClick={submit}>지금 제출하기</button>
          <button className="sv-btn full" onClick={() => setModal(null)}>계속 풀기</button>
        </Modal>
      )}
      {modal === "quit" && (
        <Modal title="시험을 그만둘까요?" text="지금 나가면 이번 시험은 채점되지 않고 기록도 남지 않아요.">
          <button className="sv-btn full" onClick={() => { doneRef.current = true; onQuit?.(); }}>나가기</button>
          <button className="sv-btn pri full" onClick={() => setModal(null)}>계속 풀기</button>
        </Modal>
      )}
    </SolveShell>
  );
}

// ── 결과 ─────────────────────────────────────────────────────────────────────
// props: { preset, scope, items, run:{ runId, results, ctx, score, saved:null|"db"|"local" }, notice, uid, toast, setToast, onRetry }
export function Result({ preset, scope, items, run, notice, uid, toast, setToast, onRetry }) {
  const { results, ctx, score, saved } = run;
  const [openIdx, setOpenIdx] = useState(null);
  const [onlyWrong, setOnlyWrong] = useState(false);
  const [noteState, setNoteState] = useState("idle");   // idle | saving | done
  const wrong = useMemo(() => wrongEntries(results), [results]);
  const mode = preset.pointsMode || "count";
  const usedSec = ctx.startedAt && ctx.finishedAt ? Math.round((ctx.finishedAt - ctx.startedAt) / 1000) : results.reduce((s, r) => s + (r?.elapsedSec || 0), 0);
  const unanswered = results.filter((r) => r?.skipped).length;

  const saveWrong = async () => {
    if (noteState !== "idle" || !wrong.length) return;
    if (!uid) { setToast("로그인이 필요해요"); return; }
    setNoteState("saving");
    const r = await saveItemWrongNotes({ uid, entries: wrong, source: `시험:${preset.name}` });
    if (r.error) { setNoteState("idle"); setToast("오답노트에 저장하지 못했어요"); return; }
    setNoteState("done");
    setToast(r.added ? `오답노트에 ${r.added}문항을 추가했어요${r.skipped ? ` · 이미 있는 ${r.skipped}문항은 건너뜀` : ""}` : "이미 오답노트에 있는 문항이에요");
  };

  const savedText = saved === null ? "기록을 저장하는 중…"
    : saved === "db" ? "응시 기록을 저장했어요."
    : uid ? "서버에 저장하지 못해 이 기기에만 기록했어요." : "로그인하지 않아 이 기기에만 기록했어요.";

  const rows = results.map((r, i) => [r, i]).filter(([r]) => !onlyWrong || r?.correct !== true);

  return (
    <SolveShell title="시험 결과" back={null} toast={toast}
      right={<button className="sv-btn sm ghost" onClick={() => { location.hash = "#/solve/test"; }}>다른 시험</button>}>
      <div className={"sv-card ex-score" + (preset.code === "ash" ? " ex-ash" : "")}>
        <div>{preset.badge ? <Badge preset={preset} /> : <span className="ex-tag">{preset.name}</span>}</div>
        {mode === "scaled100" ? (
          <>
            <div className="ex-big">{score.score}<span className="ex-of">점</span></div>
            <div className="ex-pct">정답 {score.correct_n} / {score.n} · 배점 {score.raw} / {score.rawMax}점</div>
          </>
        ) : mode === "points" ? (
          <>
            <div className="ex-big">{score.score} <span className="ex-of">/ {score.max}점</span></div>
            <div className="ex-pct">정답 {score.correct_n} / {score.n} · 정답률 {score.pct}%</div>
          </>
        ) : (
          <>
            <div className="ex-big">{score.correct_n} <span className="ex-of">/ {score.n}</span></div>
            <div className="ex-pct">정답률 {score.pct}%</div>
          </>
        )}
        <div className="sv-small">
          {preset.name} · {scope?.title}{" · "}걸린 시간 {fmtClock(usedSec)}
          {ctx.timedOut ? ` · 시간 초과${ctx.overtimeSec > 0 ? ` +${fmtTimer(ctx.overtimeSec)}` : ""}` : ""}
          {unanswered ? ` · 무응답 ${unanswered}` : ""}
        </div>
        <div className="sv-bar"><i style={{ width: `${score.pct}%` }} /></div>
        <p className="ex-msg">{examMessage(preset, score, unanswered)}</p>
        <div className="ex-saved">{savedText}</div>
      </div>
      {notice && <p className="sv-sub">{notice}</p>}

      <div className="sv-sec">문항별 결과 <span className="sv-small">(누르면 해설을 볼 수 있어요)</span></div>
      {wrong.length > 0 && wrong.length < results.length && (
        <div className="ex-filter">
          <button className={"sv-chip" + (!onlyWrong ? " on" : "")} onClick={() => setOnlyWrong(false)}>전체 {results.length}</button>
          <button className={"sv-chip" + (onlyWrong ? " on" : "")} onClick={() => setOnlyWrong(true)}>틀린 문제만 {wrong.length}</button>
        </div>
      )}
      <div className="sv-list">
        {rows.map(([r, i]) => {
          const it = items[i] || r?.item;
          if (!it) return null;
          const ok = r?.correct === true;
          const open = openIdx === i;
          return (
            <div key={it.id || i} className="ex-row">
              <button className="ex-rowbtn" onClick={() => setOpenIdx(open ? null : i)}>
                <span className={"ex-mark " + (ok ? "ok" : "bad")}>{ok ? "✓" : "✗"}</span>
                <span className="ex-rowno">{i + 1}</span>
                <span className="ex-rowq">{questionPreview(it.question, 60)}</span>
                <span className="ex-rowpt">{mode !== "count" ? `${itemPoints(it)}점 · ` : ""}{fmtClock(r?.elapsedSec || 0)}</span>
                <span className="ex-chev">{open ? "▴" : "▾"}</span>
              </button>
              <div className="ex-ansline">
                <span><span className="ex-lab">내 답</span><MathText text={myAns(it, r)} className={ok ? "sv-ok" : "sv-bad"} /></span>
                {!ok && <span><span className="ex-lab">정답</span><MathText text={correctAnswerText(it)} className="sv-ok" /></span>}
              </div>
              {open && <ItemView item={it} index={i} uid={uid} reveal initialAnswer={r ? { ...r, skipped: false } : null} autoLog={false} showSolution onToast={setToast} />}
            </div>
          );
        })}
        {!rows.length && <div className="sv-empty">보여 줄 문항이 없어요.</div>}
      </div>

      <div className="ex-actions">
        {wrong.length > 0 && (
          <button className="sv-btn pri full" disabled={noteState !== "idle"} onClick={saveWrong}>
            {noteState === "done" ? "오답노트에 저장했어요" : noteState === "saving" ? "저장 중…" : `틀린 문제 오답노트에 저장 (${wrong.length})`}
          </button>
        )}
        <div className="sv-grid2">
          <button className="sv-btn" onClick={onRetry}>같은 유형 다시</button>
          <button className="sv-btn" onClick={() => { location.hash = "#/solve/test"; }}>다른 시험</button>
        </div>
        <button className="sv-btn ghost full" onClick={() => { location.hash = "#/study/exam"; }}>시험 홈</button>
      </div>
    </SolveShell>
  );
}
