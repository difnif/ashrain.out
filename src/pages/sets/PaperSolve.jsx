// ashrain.out — 컨셉 문제 「종이처럼 풀기」(#/sets/<범주>/<NN>/paper)
// 문제지를 PDF 보듯 그대로 펼쳐 놓고 푼다.
//   · 칸을 누르면 답 시트 — 손글씨(손가락 · 펜) 또는 타자. 쓴 답은 문제지 괄호 안에 연필 글씨로 보인다.
//   · 보기 고르기는 <보기> 줄을 누르면 빨간 색연필 체크 — 여러 개 가능, 다시 누르면 해제(실수를 막지 않는다).
//   · 빈칸이 있어도 그냥 제출된다. 제출하면 바로 채점(손글씨는 AI 로 읽어서) — 빨간 동그라미 · 빗금 · 정답 · 점수.
//   · 채점 뒤 문항을 누르면 3단 해설(움직이는 판서 · 도식)이 시트로 열린다. 「틀린 문제만 다시」 · 「처음부터」.
// 답안은 이 기기 · 계정에 바로바로 저장된다(나갔다 와도 이어서).
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { printUrl, readPaper, savePaper, clearPaper, saveAttempt, saveOmrResult, pad2 } from "../../lib/conceptsets";
import { splitDoc } from "./printdoc";
import { Paper, PAGE_W_PX, ensureLinks, answerTextHtml } from "./paper";
import { gradePaper, isAnswered, togglePick, levelSummary, answerLabel } from "./paperlogic";
import { hasInk, inkSvg } from "./ink";
import { readInkAnswers } from "./recognize";
import InkPad from "./InkPad";
import { AnswerInput, ensureSerif, useAnim } from "./common";
import { headHtml, questionHtml, solutionHtml, answerHtml, LV_COLOR } from "./render";
import { kindLabel, LEVELS } from "./labels";

const ZOOMS = [1, 1.25, 1.5, 2];                 // 폭 맞춤의 배수
const ZK = "ash.cs.paper.zoom", MK = "ash.cs.inmode";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 무시 */ } };

export default function PaperSolve({ catId, set, say }) {
  const hostRef = useRef(null), paperRef = useRef(null), boxRef = useRef(null);
  const [state, setState] = useState(() => readPaper(catId, set.no));      // { answers, reads, graded }
  const [ready, setReady] = useState(false);
  const [err, setErr] = useState(null);
  const [sheet, setSheet] = useState(null);       // { no, typeOnly? }
  const [sol, setSol] = useState(null);           // no
  const [jump, setJump] = useState(false);
  const [busy, setBusy] = useState("");
  const [zi, setZi] = useState(() => { const v = Number(lsGet(ZK, 0)); return v >= 0 && v < ZOOMS.length ? v : 0; });
  const S = useRef({});
  S.current = { state, sheet, sol };
  const byNo = useMemo(() => Object.fromEntries(set.items.map((it) => [it.no, it])), [set]);

  // 문제지 HTML 불러와 shadow 에 펼치기
  useEffect(() => {
    let alive = true;
    ensureSerif();
    fetch(printUrl(catId, set.no, "problems"), { cache: "no-cache" })
      .then((r) => { if (!r.ok) throw new Error(`문제지를 불러오지 못했어요 (${r.status})`); return r.text(); })
      .then((html) => {
        if (!alive || !hostRef.current) return;
        const doc = splitDoc(html);
        ensureLinks(doc.links);
        paperRef.current = new Paper(hostRef.current, doc, set, {
          cell: (no) => onCellRef.current(no),
          pick: (no, lab) => onPickRef.current(no, lab),
        });
        setReady(true);
      })
      .catch((e) => { if (alive) setErr(e?.message || String(e)); });
    return () => { alive = false; paperRef.current?.destroy(); paperRef.current = null; };
  }, [catId, set]);

  // 확대: 폭 맞춤 × 배수
  const fit = useCallback(() => {
    const host = boxRef.current, p = paperRef.current;
    if (!host || !p) return;
    const z = Math.max(0.3, (host.clientWidth - 8) / PAGE_W_PX) * ZOOMS[zi];
    p.setZoom(z.toFixed(4));
  }, [zi]);
  useEffect(() => { if (ready) fit(); }, [ready, fit]);
  useEffect(() => {
    const on = () => fit();
    window.addEventListener("resize", on);
    return () => window.removeEventListener("resize", on);
  }, [fit]);
  useEffect(() => { lsSet(ZK, zi); }, [zi]);

  // 그리기 · 저장
  useEffect(() => {
    if (!ready) return;
    paperRef.current?.render({ ...state, active: sheet?.no ?? null });
  }, [ready, state, sheet]);
  useEffect(() => { const t = setTimeout(() => savePaper(catId, set.no, state), 250); return () => clearTimeout(t); }, [catId, set.no, state]);

  /** 답 바꾸기 — ans 는 새 답 또는 (지난 답 → 새 답) 함수. 빠르게 연달아 눌러도 최신 상태에서 계산한다 */
  const setAnswer = useCallback((no, ans) => {
    setState((s) => {
      const answers = { ...s.answers };
      const next = typeof ans === "function" ? ans(s.answers[no]) : ans;
      if (next) answers[no] = next; else delete answers[no];
      const reads = { ...s.reads };
      delete reads[no];                                // 답이 바뀌면 지난 판독은 버린다
      return { ...s, answers, reads };
    });
  }, []);

  // 칸 · 보기 누르기 (shadow 안 이벤트 → 최신 상태를 ref 로)
  const onCellRef = useRef(() => {}), onPickRef = useRef(() => {});
  onCellRef.current = (no) => {
    const st = S.current.state;
    if (st.graded) {
      const row = st.graded.rows.find((r) => r.no === no);
      if (row?.status === "unread") setSheet({ no, typeOnly: true });
      else setSol(no);
      return;
    }
    setSheet({ no });
  };
  onPickRef.current = (no, lab) => {
    const st = S.current.state;
    if (st.graded) { setSol(no); return; }
    const it = byNo[no];
    setAnswer(no, (prev) => togglePick(prev, lab, it?.a?.o));
  };

  const nAnswered = set.items.filter((it) => isAnswered(state.answers[it.no])).length;

  // 제출 → 채점 (빈칸이 있어도 그냥)
  const submit = async () => {
    const st = S.current.state;
    const need = set.items.filter((it) => st.answers[it.no]?.k === "ink" && hasInk(st.answers[it.no]) && st.reads[it.no] == null)
      .map((it) => ({ no: it.no, ink: st.answers[it.no] }));
    let reads = { ...st.reads };
    if (need.length) {
      setBusy(`손글씨 답 ${need.length}개를 읽는 중…`);
      const r = await readInkAnswers(need);
      reads = { ...reads, ...r.reads };
      if (r.error) say(r.error);
    }
    finish(st.answers, reads);
    setBusy("");
  };
  const finish = (answers, reads) => {
    const g = gradePaper(set, answers, reads);
    for (const r of g.rows) if (r.status === "ok" || r.status === "wrong") saveAttempt(catId, set.no, r.id, r.raw, r.status === "ok");
    saveOmrResult(catId, set.no, { kind: "paper", score: g.score, n: g.n, answers: Object.fromEntries(g.rows.map((r) => [r.no, r.raw])) });
    setState((s) => ({ ...s, answers, reads, graded: { score: g.score, n: g.n, at: new Date().toISOString(), rows: g.rows, counts: g.counts } }));
    setSheet(null);
    window.scrollTo?.({ top: 0, behavior: "smooth" });
  };
  const retryWrong = () => {
    setState((s) => {
      const keep = new Set((s.graded?.rows || []).filter((r) => r.status === "ok").map((r) => r.no));
      const answers = {}, reads = {};
      for (const [no, a] of Object.entries(s.answers)) if (keep.has(Number(no))) { answers[no] = a; if (s.reads[no] != null) reads[no] = s.reads[no]; }
      return { answers, reads, graded: null };
    });
    setSol(null);
  };
  const restart = () => { clearPaper(catId, set.no); setState({ answers: {}, reads: {}, graded: null }); setSol(null); };

  // 시트에서 저장 — 채점 뒤 「확인 필요」 칸을 고치면 그 문항만 다시 채점
  const saveFromSheet = (no, ans) => {
    setAnswer(no, ans);
    if (S.current.state.graded) {
      const answers = { ...S.current.state.answers };
      if (ans) answers[no] = ans; else delete answers[no];
      const reads = { ...S.current.state.reads };
      delete reads[no];
      finish(answers, reads);
    }
  };
  const nextNo = (no) => { const i = set.items.findIndex((it) => it.no === no); return set.items[i + 1]?.no ?? null; };
  const openNext = (no) => {
    const n = nextNo(no);
    if (n == null) { setSheet(null); return; }
    setSheet({ no: n });
    paperRef.current?.reveal(n);
  };

  const g = state.graded;
  const lvs = g ? levelSummary(set, g, LEVELS) : null;
  const wrongNos = g ? g.rows.filter((r) => r.status !== "ok").map((r) => r.no) : [];

  return (
    <div className="cs-paperpage">
      {err && <div className="cs-wrap"><div className="sv-empty">{err}</div></div>}
      {!ready && !err && <div className="cs-wrap sv-muted">문제지를 펼치는 중…</div>}
      {g && (
        <div className="cs-gsum" role="status">
          <b>{g.score}/{g.n}</b>
          <span>{lvs.map(([lv, ok, n]) => <i key={lv}><em style={{ background: LV_COLOR[lv] }}>{lv}</em>{ok}/{n}</i>)}</span>
          {g.counts?.blank > 0 && <span className="cs-gx">빈칸 {g.counts.blank}</span>}
          {g.counts?.unread > 0 && <span className="cs-gx warn">손글씨 확인 {g.counts.unread}</span>}
          <span className="cs-gx">문항을 누르면 해설</span>
        </div>
      )}
      <div ref={boxRef} className="cs-paperbox">
        <div ref={hostRef} className="cs-paperhost" />
      </div>

      <div className="cs-pbar2" role="toolbar" aria-label="문제지 도구">
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={zi === 0} onClick={() => setZi((v) => Math.max(0, v - 1))} aria-label="작게">−</button>
          <button type="button" className="cs-tb cs-zv" onClick={() => setZi(0)} title="폭 맞춤">{zi === 0 ? "맞춤" : `${Math.round(ZOOMS[zi] * 100)}%`}</button>
          <button type="button" className="cs-tb" disabled={zi === ZOOMS.length - 1} onClick={() => setZi((v) => Math.min(ZOOMS.length - 1, v + 1))} aria-label="크게">＋</button>
        </div>
        <button type="button" className="cs-tb" onClick={() => setJump(true)}>번호 {g ? "" : `${nAnswered}/${set.items.length}`}</button>
        <span className="cs-fill" />
        {!g ? (
          <button type="button" className="sv-btn pri cs-submit" disabled={!!busy || !ready} onClick={submit}>제출하고 채점</button>
        ) : (
          <div className="cs-gbar">
            <b className="cs-gs">{g.score}<small>/{g.n}</small></b>
            {wrongNos.length > 0 && <button type="button" className="sv-btn sm pri" onClick={retryWrong}>틀린 것만 다시</button>}
            <button type="button" className="sv-btn sm" onClick={restart}>처음부터</button>
          </div>
        )}
      </div>


      {busy && <div className="cs-busyover"><div><i className="sp" />{busy}</div></div>}

      {sheet && byNo[sheet.no] && (
        <AnswerSheet key={sheet.no} it={byNo[sheet.no]} value={state.answers[sheet.no]} typeOnly={!!sheet.typeOnly}
          onSave={(ans) => saveFromSheet(sheet.no, ans)} onClose={() => setSheet(null)}
          onNext={nextNo(sheet.no) != null && !state.graded ? () => openNext(sheet.no) : null} />
      )}
      {sol != null && byNo[sol] && (
        <SolutionSheet key={sol} it={byNo[sol]} ans={state.answers[sol]} read={state.reads[sol]}
          row={g?.rows.find((r) => r.no === sol)} onClose={() => setSol(null)} video={`#/sets/${catId}/${pad2(set.no)}/video?no=${sol}`}
          onMove={(d) => { const i = set.items.findIndex((it) => it.no === sol); const t = set.items[i + d]; if (t) { setSol(t.no); paperRef.current?.reveal(t.no); } }}
          list={wrongNos} />
      )}
      {jump && (
        <JumpSheet set={set} answers={state.answers} graded={g} onClose={() => setJump(false)}
          onPick={(no) => { setJump(false); setTimeout(() => paperRef.current?.reveal(no), 30); }} />
      )}
    </div>
  );
}

/* ── 답 시트: 손글씨 | 타자 (보기 문항은 체크) ── */
function AnswerSheet({ it, value, onSave, onClose, onNext, typeOnly }) {
  const k = it.a?.k;
  const lay = k === "frac" ? "frac" : k === "pair" ? "pair" : "int";
  const [mode, setMode] = useState(() => {
    if (typeOnly) return "type";
    if (value?.k === "ink") return "ink";
    if (value?.k === "text") return "type";
    const pref = lsGet(MK, "");
    if (pref === "ink" || pref === "type") return pref;
    try { return window.matchMedia?.("(pointer: coarse)").matches ? "ink" : "type"; } catch { return "type"; }
  });
  const [ink, setInk] = useState(value?.k === "ink" ? value : null);
  const [text, setText] = useState(value?.k === "text" ? value.raw : value?.k === "pick" ? value.sel.join(", ") : "");
  useEffect(() => { if (!typeOnly) lsSet(MK, mode); }, [mode, typeOnly]);

  const current = () => {
    if (k === "pick") { const sel = (it.a.o || []).filter((o) => (text.match(/[ㄱ-ㅎ]/gu) || []).includes(o)); return sel.length ? { k: "pick", sel } : null; }
    if (mode === "ink") return hasInk(ink) ? ink : null;
    return String(text || "").trim() ? { k: "text", raw: String(text).trim() } : null;
  };
  const save = () => { onSave(current()); onClose(); };
  const saveNext = () => { onSave(current()); onNext(); };
  const clear = () => { setInk(null); setText(""); };

  return (
    <div className="cs-sheetbg" onClick={save}>
      <div className="cs-sheet" onClick={(e) => e.stopPropagation()} role="dialog" aria-label={`${it.no}번 답 쓰기`}>
        <div className="cs-shh">
          <span className="cs-shno">{it.no}</span>
          <div className="cs-sht"><b>{it.no}번 답</b><small>{typeOnly ? "손글씨를 읽지 못했어요 — 타자로 써 주세요" : kindLabel(it)}</small></div>
          {k !== "pick" && !typeOnly && (
            <div className="cs-modes" role="tablist">
              <button type="button" role="tab" aria-selected={mode === "ink"} className={mode === "ink" ? "on" : ""} onClick={() => setMode("ink")}>✍ 손글씨</button>
              <button type="button" role="tab" aria-selected={mode === "type"} className={mode === "type" ? "on" : ""} onClick={() => setMode("type")}>⌨ 타자</button>
            </div>
          )}
        </div>
        <div className="cs-shb">
          {k === "pick" ? (
            <AnswerInput item={it} value={text} onChange={setText} onSubmit={save} />
          ) : mode === "ink" ? (
            <InkPad lay={lay} value={ink} onChange={setInk} unit={it.a?.u || ""} labels={it.a?.l || []} />
          ) : (
            <div className="cs-typein"><AnswerInput item={it} value={text} onChange={setText} onSubmit={onNext ? saveNext : save} /></div>
          )}
        </div>
        <div className="cs-shf">
          {mode === "ink" && k !== "pick" && !typeOnly && (
            <button type="button" className="sv-btn sm" disabled={!hasInk(ink)} onClick={() => setInk(ink && ink.s.length > 1 ? { ...ink, s: ink.s.slice(0, -1), wd: (ink.wd || []).slice(0, -1) } : null)}>↶ 되돌리기</button>
          )}
          <button type="button" className="sv-btn sm ghost" onClick={clear}>지우기</button>
          <span className="cs-fill" />
          {onNext && <button type="button" className="sv-btn sm" onClick={saveNext}>다음 ›</button>}
          <button type="button" className="sv-btn sm pri" onClick={save}>확인</button>
        </div>
      </div>
    </div>
  );
}

/* ── 해설 시트: 내 답 · 정답 · 3단 해설(움직임) ── */
function SolutionSheet({ it, ans, read, row, onClose, onMove, list, video }) {
  const ref = useRef(null);
  const sHtml = useMemo(() => solutionHtml(it), [it]);
  useAnim(ref, [it.id]);
  const st = row?.status;
  const mine = !isAnswered(ans) ? "무응답" : ans.k === "ink" ? null : answerLabel(ans, read);
  return (
    <div className="cs-sheetbg" onClick={onClose}>
      <div className="cs-sheet cs-solsheet" onClick={(e) => e.stopPropagation()} role="dialog" aria-label={`${it.no}번 해설`}>
        <div className="cs-shh">
          <div className="cs-qh" dangerouslySetInnerHTML={{ __html: headHtml(it) }} />
          <span className="cs-fill" />
          <button type="button" className="cs-x" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="cs-shb cs-solbody">
          <div className="cs-qb cs-qsmall" dangerouslySetInnerHTML={{ __html: questionHtml(it) }} />
          <div className={"cs-verdict iv-banner " + (st === "ok" ? "ok" : st ? "bad" : "")}>
            <div className="iv-verdict">{st === "ok" ? "맞았어요 ○" : st === "unread" ? "손글씨 확인 필요" : st ? "틀렸어요" : "해설"}</div>
            <div className="iv-mine"><span className="iv-lab">내 답</span>
              {ans?.k === "ink" && hasInk(ans)
                ? <span className="cs-myink" dangerouslySetInnerHTML={{ __html: inkSvg(ans, { cls: "cs-myinksvg" }) }} />
                : <span dangerouslySetInnerHTML={{ __html: answerTextHtml(mine) }} />}
              {ans?.k === "ink" && read ? <small className="cs-readas"> → {read}로 읽었어요</small> : null}
            </div>
            <div className="iv-ans"><span className="iv-lab">정답</span><span dangerouslySetInnerHTML={{ __html: answerHtml(it) }} /></div>
          </div>
          <div ref={ref} className="cs-solwrap" dangerouslySetInnerHTML={{ __html: sHtml }} />
        </div>
        <div className="cs-shf">
          <button type="button" className="sv-btn sm" onClick={() => onMove(-1)}>‹ 이전</button>
          {list?.length > 0 && <span className="sv-small">틀린 문항 {list.length}개</span>}
          <span className="cs-fill" />
          {video && <button type="button" className="sv-btn sm" onClick={() => (location.hash = video)}>🎬 영상</button>}
          <button type="button" className="sv-btn sm" onClick={() => onMove(1)}>다음 ›</button>
        </div>
      </div>
    </div>
  );
}

/* ── 번호로 가기 ── */
function JumpSheet({ set, answers, graded, onPick, onClose }) {
  const st = graded ? Object.fromEntries(graded.rows.map((r) => [r.no, r.status])) : {};
  return (
    <div className="cs-sheetbg" onClick={onClose}>
      <div className="cs-sheet" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호로 가기">
        <div className="cs-shh"><div className="cs-sht"><b>번호로 가기</b><small>{graded ? "○ 맞음 · / 틀림 · 빈칸" : "칠한 칸 = 답을 쓴 문항"}</small></div><span className="cs-fill" />
          <button type="button" className="cs-x" onClick={onClose} aria-label="닫기">✕</button></div>
        <div className="cs-jump">
          {set.items.map((it) => {
            const s = st[it.no];
            const cls = graded ? (s === "ok" ? " ok" : s === "unread" ? " warn" : " bad") : isAnswered(answers[it.no]) ? " done" : "";
            return <button key={it.no} type="button" className={"cs-jn" + cls} onClick={() => onPick(it.no)}>{it.no}</button>;
          })}
        </div>
      </div>
    </div>
  );
}

