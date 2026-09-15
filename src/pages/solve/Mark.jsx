// 표시 연습 — #/solve/mark (문항 고르기) · #/solve/mark/<itemId>
// 시범 탭: 규칙 키(동그라미·밑줄·빗금)와 설명.  연습 탭: 학생이 직접 표시 → 채점(scoreMarks) → 맞음·놓침·덤 표시를 색으로.
// 채점은 1층(규칙) 표시만. 결과는 localStorage "ash.mark.results" 에 최근 50개.
import { useEffect, useMemo, useRef, useState } from "react";
import SolveShell, { useToast } from "./SolveShell";
import ItemPicker from "./ItemPicker";
import SentenceMarks, { MarkLegend } from "./SentenceMarks";
import MathText from "../../components/MathText";
import ItemFigure from "../../components/ItemFigure";
import { fetchItem, fetchLiveItems, conceptOf } from "../../lib/items";
import { explain, autoMark, scoreMarks, practiceEligible, markText, markKey, FUNC_LABEL, FUNC_MEANING, TIER1 } from "../../lib/marking.js";

export const LS_RESULTS = "ash.mark.results";

const CSS = `
.mk-tabs{display:flex;gap:6px;margin-bottom:12px}
.mk-tabs .sv-chip{padding:8px 16px;font-size:14px}
.mk-sent{padding:6px 4px 2px}
.mk-tools{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 4px}
.mk-tools .sv-chip{padding:8px 12px;font-size:13.5px}
.mk-tools .sv-chip .g{font-weight:900;font-size:15px}
.mk-tools .sv-chip.on{background:color-mix(in srgb,var(--accent) 10%,var(--surface))}
.mk-hint{font-size:12.5px;color:var(--muted);line-height:1.6;margin:6px 0 2px}
.mk-row{display:flex;gap:8px;align-items:center;margin-top:10px}
.mk-row .sv-btn{flex:1}
.mk-note{margin-top:8px;padding:10px 12px;border-radius:12px;background:var(--surface2);font-size:13.5px;line-height:1.6}
.mk-note b{display:inline-block;margin-right:6px;font-size:12px;padding:1px 8px;border-radius:999px;background:var(--surface);border:1px solid var(--border)}
.mk-score{display:flex;align-items:center;gap:14px}
.mk-score .big{font-size:40px;font-weight:900;letter-spacing:-1px;line-height:1}
.mk-score .big small{font-size:16px;font-weight:800;color:var(--muted);margin-left:2px}
.mk-score .txt{font-size:14px;line-height:1.6}
.mk-list{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:8px}
.mk-list li{display:flex;gap:10px;align-items:flex-start;font-size:14px;line-height:1.6}
.mk-list .tag{flex:none;font-size:11.5px;font-weight:800;padding:2px 8px;border-radius:999px;border:1px solid var(--border);background:var(--surface2);margin-top:3px;white-space:nowrap}
.mk-list .tag.miss{border-color:var(--bad);color:var(--bad)}
.mk-list .tag.hit{border-color:var(--good);color:var(--good)}
.mk-list .tx b{font-weight:800}
.mk-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px}
@media (max-width:420px){.mk-actions{grid-template-columns:1fr}}
.mk-prev{font-size:12.5px;color:var(--muted);margin-top:6px}
`;

const TOOLS = [
  { id: "NUM", g: "◯", label: "동그라미", tip: "숫자 정보" },
  { id: "SCALE", g: "＿", label: "밑줄", tip: "숫자 앞 척도" },
  { id: "BOUND", g: "／", label: "빗금", tip: "단서 경계" },
  { id: "ERASE", g: "⌫", label: "지우개", tip: "표시 지우기" },
];
const TOOL_HINT = {
  NUM: "숫자를 탭하면 동그라미가 쳐져요. 단위까지 한 덩어리로!",
  SCALE: "숫자 앞의 척도 낱말(둘레·넓이·속력…)을 탭하면 밑줄이 그어져요. 옆 낱말을 이어 탭하면 밑줄이 길어져요.",
  BOUND: "단서가 끊기는 자리의 낱말(또는 쉼표)을 탭하면 그 뒤에 빗금이 생겨요.",
  ERASE: "표시된 낱말이나 빗금을 탭하면 지워져요.",
};

export function readResults() {
  try { const a = JSON.parse(localStorage.getItem(LS_RESULTS) || "[]"); return Array.isArray(a) ? a : []; } catch { return []; }
}
function saveResult(row) {
  try { localStorage.setItem(LS_RESULTS, JSON.stringify([row, ...readResults()].slice(0, 50))); }
  catch { /* 저장 못 해도 흐름은 막지 않는다 */ }
}

/** a < b 이고 사이가 모두 공백이면 이웃 */
function adjacent(tokens, a, b) {
  if (a >= b) return false;
  for (let k = a + 1; k < b; k++) if (tokens[k].kind !== "space") return false;
  return true;
}

const stripMarker = (s) => String(s || "").replace(/\[\[|\]\]/g, "");

// ── 페이지 (라우트 · 로딩) ───────────────────────────────────────────────────
export default function Mark({ itemId }) {
  const [toast, setToast] = useToast();
  const [item, setItem] = useState(null);
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    setItem(null); setErr(null);
    if (!itemId) return;
    let alive = true;
    fetchItem(itemId).then((it) => { if (!alive) return; if (!it) setErr("문항을 찾을 수 없어요. 공개되지 않은 문항일 수도 있어요."); else setItem(it); })
      .catch(() => alive && setErr("문항을 불러오지 못했어요. 잠시 뒤 다시 시도해 주세요."));
    return () => { alive = false; };
  }, [itemId]);

  // 고른 문항이 너무 짧으면 같은 개념의 연습용 문항으로 바꿔 준다
  const pickItem = async (it) => {
    if (practiceEligible(it.question)) { location.hash = `#/solve/mark/${it.id}`; return; }
    setBusy(true);
    try {
      const pool = await fetchLiveItems({ conceptId: conceptOf(it), n: 30, pool: 120 });
      const ok = pool.filter((x) => practiceEligible(x.question));
      if (ok.length) {
        setToast("고른 문항은 짧아서 같은 개념의 다른 문항으로 바꿨어요");
        location.hash = `#/solve/mark/${ok[Math.floor(Math.random() * ok.length)].id}`;
      } else setToast("이 개념에는 표시 연습에 맞는 긴 문항이 아직 없어요");
    } catch { setToast("문항을 불러오지 못했어요"); }
    setBusy(false);
  };

  if (!itemId) {
    return (
      <SolveShell title="표시 연습" sub="문장에 직접 표시해요 — 숫자에 동그라미, 척도에 밑줄, 단서가 끊기는 곳에 빗금." toast={toast}>
        <ItemPicker mode="item" hint={busy ? "문항을 고르는 중…" : "문항을 하나 골라 주세요. 조건이 여러 개인 문장이 연습하기 좋아요."} onPickItem={pickItem} />
      </SolveShell>
    );
  }

  return (
    <SolveShell title="표시 연습" toast={toast}
      right={<button className="sv-btn sm" onClick={() => { location.hash = "#/solve/mark"; }}>다른 문항</button>}>
      <style>{CSS}</style>
      {err && <div className="sv-empty">{err}</div>}
      {!err && !item && <div className="sv-muted">문항을 불러오는 중…</div>}
      {item && <MarkView item={item} setToast={setToast} />}
    </SolveShell>
  );
}

// ── 문항 하나: 시범 · 연습 ───────────────────────────────────────────────────
export function MarkView({ item, setToast = () => {}, defaultTab }) {
  const [tab, setTab] = useState(() => defaultTab || (readResults().length ? "practice" : "demo"));
  const [tool, setTool] = useState("NUM");
  const [marks, setMarks] = useState([]);
  const [hist, setHist] = useState([]);
  const [sel, setSel] = useState(null);
  const [result, setResult] = useState(null);
  const [picked, setPicked] = useState(null);
  const [busy, setBusy] = useState(false);
  const topRef = useRef(null);

  useEffect(() => { setMarks([]); setHist([]); setSel(null); setResult(null); setPicked(null); }, [item?.id]);

  const ex = useMemo(() => explain(item?.question || "", item), [item]);
  const tokens = ex.tokens;
  const key = useMemo(() => autoMark(tokens), [tokens]);                       // 1층 키(채점용)
  const requiredN = key.filter((m) => m.required).length;
  const prev = useMemo(() => readResults().filter((r) => r.itemId === item?.id), [item, result]);

  const commit = (next, range) => { setHist((h) => [...h, marks]); setMarks(next); setSel(range || null); };

  const tapToken = (i) => {
    if (result) return;
    const t = tokens[i];
    if (!t || t.kind === "space" || t.kind === "newline") return;
    if (tool === "ERASE") {
      const next = marks.filter((m) => !(m.kind === "span" ? i >= m.t0 && i <= m.t1 : m.t0 === i));
      if (next.length === marks.length) { setToast("여기엔 지울 표시가 없어요"); return; }
      commit(next, null); return;
    }
    if (tool === "BOUND") {
      if (marks.some((m) => m.kind === "point" && m.t0 === i)) { setToast("이미 빗금이 있어요"); return; }
      commit([...marks, { kind: "point", t0: i, func: "BOUND" }], null); return;
    }
    if (t.kind === "punct") { setToast("동그라미·밑줄은 낱말이나 숫자에 쳐요"); return; }
    const same = marks.filter((m) => m.kind === "span" && m.func === tool);
    if (same.some((m) => i >= m.t0 && i <= m.t1)) { setToast("이미 표시한 곳이에요 — 지우개로 지울 수 있어요"); return; }
    const ext = same.find((m) => adjacent(tokens, m.t1, i) || adjacent(tokens, i, m.t0));
    if (ext) {
      const grown = { ...ext, t0: Math.min(ext.t0, i), t1: Math.max(ext.t1, i) };
      commit(marks.map((m) => (m === ext ? grown : m)), [grown.t0, grown.t1]);
    } else commit([...marks, { kind: "span", t0: i, t1: i, func: tool }], [i, i]);
  };

  const tapMark = (m) => {
    if (result) { setPicked(m); return; }
    if (m.kind === "point") { commit(marks.filter((x) => x !== m), null); setToast("빗금을 지웠어요"); }
  };

  const undo = () => { if (!hist.length) return; const h = hist.slice(); const last = h.pop(); setHist(h); setMarks(last); setSel(null); };

  const grade = () => {
    const r = scoreMarks(marks, key, tokens);
    setResult(r); setPicked(null); setSel(null);
    saveResult({ itemId: item.id, score: r.score, required: r.required, hit: r.hit, at: new Date().toISOString() });
    setTimeout(() => topRef.current?.scrollIntoView?.({ behavior: "smooth", block: "start" }), 50);
  };

  const reset = () => { setMarks([]); setHist([]); setSel(null); setResult(null); setPicked(null); };

  const nextItem = async () => {
    setBusy(true);
    try {
      const pool = await fetchLiveItems({ conceptId: conceptOf(item), n: 30, pool: 120 });
      const ok = pool.filter((x) => x.id !== item.id && practiceEligible(x.question));
      if (!ok.length) setToast("같은 개념에 연습할 다른 문항이 아직 없어요");
      else location.hash = `#/solve/mark/${ok[Math.floor(Math.random() * ok.length)].id}`;
    } catch { setToast("문항을 불러오지 못했어요"); }
    setBusy(false);
  };

  // 채점 후 화면에 그릴 표시: 학생 표시(맞음·덤) + 놓친 키
  const shown = result ? [...marks.filter((m) => TIER1.includes(m.func)), ...result.missed] : marks;
  const diff = result ? { hit: result.detail.filter((d) => d.matched).map((d) => d.matched), missed: result.missed, extra: result.extra } : null;

  return (
    <>
      <div ref={topRef} />
      <div className="mk-tabs">
        <button className={"sv-chip" + (tab === "demo" ? " on" : "")} onClick={() => { setTab("demo"); setPicked(null); }}>시범</button>
        <button className={"sv-chip" + (tab === "practice" ? " on" : "")} onClick={() => { setTab("practice"); setPicked(null); }}>연습</button>
      </div>
      {!practiceEligible(item?.question) && (
        <div className="sv-small" style={{ margin: "-4px 0 10px" }}>이 문장은 짧아서 표시할 것이 적어요. 조건이 여러 개인 문항이 연습하기 좋아요.</div>
      )}

      {tab === "demo" && (
        <>
          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>이렇게 표시해요 <span className="sv-small">· 표시를 탭하면 이유가 나와요</span></div>
            <SentenceMarks className="mk-sent" tokens={tokens} marks={ex.marks} onMarkTap={(m) => setPicked(m)} />
            {picked && <MarkNote mark={picked} tokens={tokens} />}
            <ItemFigure figure={item.figure} width={320} />
          </div>
          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>표시 읽는 법</div>
            <MarkLegend tier2={ex.marks.some((m) => m.func === "EMPH")} />
          </div>
          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>왜 이 표시?</div>
            <WhyList keyMarks={key} tokens={tokens} />
            {ex.marks.some((m) => m.tier === 2) && (
              <div className="sv-small" style={{ marginTop: 10 }}>두 줄 밑줄(강조)은 이 유형의 함정을 보고 붙인 참고 표시예요 — 채점에는 들어가지 않아요.</div>
            )}
          </div>
          <div className="mk-actions">
            <button className="sv-btn pri" onClick={() => { setTab("practice"); setPicked(null); }}>직접 표시해 보기</button>
            <button className="sv-btn" onClick={() => { location.hash = `#/solve/read/${item.id}`; }}>문장 해설 보기</button>
          </div>
        </>
      )}

      {tab === "practice" && (
        <>
          <div className="sv-card">
            {!result && (
              <>
                <div className="mk-tools">
                  {TOOLS.map((t) => (
                    <button key={t.id} className={"sv-chip" + (tool === t.id ? " on" : "")} onClick={() => setTool(t.id)} title={t.tip}>
                      <span className="g">{t.g}</span> {t.label}
                    </button>
                  ))}
                </div>
                <div className="mk-hint">{TOOL_HINT[tool]}</div>
              </>
            )}
            {result && <div className="mk-hint">초록 = 맞음 · 빨간 점선 = 놓침 · 회색 = 키에 없는 표시(감점은 없어요). 표시를 탭하면 설명이 나와요.</div>}
            <SentenceMarks className="mk-sent" tokens={tokens} marks={shown} selectable={!result} selection={sel} diff={diff}
              onTokenTap={tapToken} onMarkTap={tapMark} />
            {result && picked && <MarkNote mark={picked} tokens={tokens} fallback="키에 없는 표시예요. 틀린 건 아니지만 꼭 필요한 표시는 아니에요." />}
            <ItemFigure figure={item.figure} width={320} />
            {!result && (
              <>
                <div className="mk-row">
                  <button className="sv-btn" onClick={undo} disabled={!hist.length}>되돌리기</button>
                  <button className="sv-btn pri" onClick={grade}>채점</button>
                </div>
                <div className="mk-prev">필수 표시 {requiredN}개 · 지금 {marks.length}개 표시했어요{prev.length ? ` · 이전 점수 ${prev[0].score}점` : ""}</div>
              </>
            )}
          </div>

          {result && (
            <>
              <ResultCards result={result} keyMarks={key} tokens={tokens} prev={prev} />
              <div className="mk-actions">
                <button className="sv-btn pri" onClick={reset}>다시 하기</button>
                <button className="sv-btn" onClick={nextItem} disabled={busy}>{busy ? "고르는 중…" : "다른 문항"}</button>
                <button className="sv-btn" onClick={() => { location.hash = `#/solve/item/${item.id}`; }}>이 문제 풀기</button>
                <button className="sv-btn ghost" onClick={() => { setTab("demo"); setPicked(null); }}>시범 다시 보기</button>
              </div>
            </>
          )}
        </>
      )}
    </>
  );
}

/** 탭한 표시의 설명 한 줄 */
function MarkNote({ mark, tokens, fallback = "단서예요." }) {
  const what = stripMarker(markText(mark, tokens));
  return (
    <div className="mk-note">
      <b>{FUNC_LABEL[mark.func] || mark.func}</b>
      <span>{what ? `${what} — ` : ""}{mark.note || fallback}</span>
    </div>
  );
}

const scoreWord = (s) => (s === 100 ? "완벽해요!" : s >= 75 ? "잘 읽었어요" : s >= 50 ? "절반은 잡았어요" : "다시 천천히 읽어 봐요");

/** 채점 결과 카드들 — 점수 · 놓친 표시 · 왜 이 표시? */
export function ResultCards({ result, keyMarks, tokens, prev = [] }) {
  return (
    <>
      <div className="sv-card">
        <div className="mk-score">
          <div className="big" style={{ color: result.score >= 75 ? "var(--good)" : result.score >= 50 ? "var(--text)" : "var(--bad)" }}>{result.score}<small>점</small></div>
          <div className="txt">
            <div style={{ fontWeight: 800 }}>{scoreWord(result.score)}</div>
            <div>필수 표시 {result.required}개 중 {result.hit}개를 찾았어요.</div>
            <div className="sv-small">
              {result.bonusHit ? `덤으로 있으면 좋은 자리 ${result.bonusHit}곳도 맞혔어요. ` : ""}
              {result.extra.length ? `키에 없는 표시 ${result.extra.length}개는 점수에 들어가지 않아요.` : ""}
            </div>
          </div>
        </div>
        {prev.length > 1 && <div className="mk-prev">이 문항 이전 점수: {prev.slice(1, 4).map((r) => r.score + "점").join(" · ")}</div>}
      </div>

      {result.missed.length > 0 && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>놓친 표시</div>
          <ul className="mk-list">
            {result.missed.map((m) => (
              <li key={markKey(m)}>
                <span className="tag miss">{FUNC_LABEL[m.func]}</span>
                <span className="tx"><b><MathText text={markText(m, tokens)} /></b> — {m.note}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>왜 이 표시?</div>
        <WhyList keyMarks={keyMarks} tokens={tokens} result={result} />
      </div>
    </>
  );
}

/** 키 표시 목록 — 종류별로 묶어 "무엇 — 왜" */
export function WhyList({ keyMarks, tokens, result }) {
  const matched = new Set(result ? result.detail.filter((d) => d.matched).map((d) => markKey(d.key)) : []);
  const groups = ["NUM", "SCALE", "BOUND"].map((f) => [f, keyMarks.filter((m) => m.func === f)]).filter(([, l]) => l.length);
  if (!groups.length) return <div className="sv-muted">이 문장에는 규칙으로 잡히는 표시가 없어요.</div>;
  return (
    <div className="sv-list" style={{ gap: 12 }}>
      {groups.map(([f, list]) => (
        <div key={f}>
          <div className="sv-small" style={{ marginBottom: 6 }}>{FUNC_LABEL[f]} · {FUNC_MEANING[f]}</div>
          <ul className="mk-list">
            {list.map((m) => {
              const k = markKey(m);
              const st = result ? (matched.has(k) ? "hit" : m.required ? "miss" : "") : "";
              return (
                <li key={k}>
                  <span className={"tag" + (st ? " " + st : "")}>{st === "hit" ? "맞음" : st === "miss" ? "놓침" : m.required ? "필수" : "있으면 좋음"}</span>
                  <span className="tx"><b><MathText text={markText(m, tokens)} /></b> — {m.note}</span>
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </div>
  );
}
