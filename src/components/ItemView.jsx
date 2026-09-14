// 문항 1개 풀기 — ItemQuestion(본문) 위에 답 입력 · 채점 · 해설(애니메이션) · 행동 버튼을 얹는다.
// 세트 풀기(ItemPlay) · 오답노트 재풀이 · 결과 복기(reveal) 가 공유한다.
//
// props
//   item, index(0부터; null 이면 번호 없음), uid, setId, seq
//   onAnswered({ correct, rawAnswer, chosenIndex, chosenChoice, elapsedSec, tag, retryN, solutionSeen })
//   onNext, nextLabel="다음 문제"
//   autoLog=true          답을 낼 때 attempts 에 기록 (uid 필요)
//   showSolution=true     답을 낸 뒤 해설 표시
//   allowAsk / allowWrongNote  하단 버튼
//   reveal=false          복기 모드 — 입력 없이 정답·해설을 바로 보여 준다 (initialAnswer 로 학생 답 표시)
//   initialAnswer         reveal 용: 문자열(학생 답) 또는 { rawAnswer, chosenIndex, chosenChoice, correct, skipped }
//   onToast(msg)          바깥 SolveShell 의 토스트를 쓰고 싶을 때. 없으면 자체 토스트
import { useEffect, useMemo, useRef, useState } from "react";
import ItemQuestion from "./ItemQuestion";
import MathText, { mathHtml, ensureMathCss } from "./MathText";
import { figureHtml } from "./ItemFigure";
import { CIRCLED, isChoiceCorrect, isCorrect, kindOf } from "../lib/answers";
import { solutionLevels, hasRubric, logAttempt } from "../lib/items";
import { distractorTag, mcLabel } from "../lib/misconceptions";
import { saveItemWrongNotes } from "../lib/wrongnotes";
import { askAboutItem } from "../lib/ask";
import { mountAll } from "../lib/figanim";
import { correctAnswerText, myAnswerText, fmtClock } from "../lib/setplay";
import { useToast } from "../pages/solve/SolveShell";
import "./item.css";
import "../pages/solve/solve.css";

const CSS = `
.iv-time { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--muted); margin:-2px 0 8px; font-variant-numeric:tabular-nums; }
.iv-time .iv-clock { font-weight:800; }
.iv-time .iv-over { color:var(--bad); font-weight:700; }
.iv-submit { margin-top:10px; }
.iv-short { display:flex; gap:8px; margin-top:10px; align-items:stretch; }
.iv-short .sv-in { flex:1 1 auto; min-width:0; }
.iv-short .sv-btn { flex:none; }
.iv-ta { display:block; margin-top:10px; }
.iv-ox { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:10px; }
.iv-ox .sv-btn { font-size:22px; padding:14px; }
.iv-hint { font-size:11.5px; color:var(--muted); margin-top:6px; line-height:1.5; }
.iv-banner { margin-top:12px; padding:12px 14px; border-radius:12px; border:1px solid var(--border); background:var(--surface2); line-height:1.6; }
.iv-banner.ok { border-color:var(--good); background:color-mix(in srgb, var(--good) 10%, var(--surface)); }
.iv-banner.bad { border-color:var(--bad); background:color-mix(in srgb, var(--bad) 8%, var(--surface)); }
.iv-verdict { font-size:16px; font-weight:800; }
.iv-banner.ok .iv-verdict { color:var(--good); }
.iv-banner.bad .iv-verdict { color:var(--bad); }
.iv-ans, .iv-mine { font-size:14.5px; margin-top:4px; }
.iv-ans .iv-lab, .iv-mine .iv-lab { color:var(--muted); font-size:12.5px; margin-right:4px; }
.iv-mc { margin-top:6px; font-size:13px; color:var(--bad); font-weight:700; }
.iv-banner .iv-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
.iv-sol { margin-top:12px; }
.iv-sol .lv li, .iv-sol .lv p { white-space:pre-wrap; word-break:keep-all; }
.iv-sol .lv .fig-stage { margin:6px 0 8px; }
.iv-nosol { margin-top:12px; font-size:13px; color:var(--muted); }
.iv-details { margin-top:8px; border:1px solid var(--border); border-radius:10px; padding:8px 12px; font-size:13.5px; line-height:1.6; }
.iv-details summary { cursor:pointer; font-weight:800; font-size:13px; color:var(--muted); }
.iv-details[open] summary { margin-bottom:6px; }
.iv-rubric { width:100%; border-collapse:collapse; font-size:12.5px; }
.iv-rubric th, .iv-rubric td { border-top:1px solid var(--border); padding:6px 4px; text-align:left; vertical-align:top; }
.iv-rubric th { color:var(--muted); font-weight:700; border-top:none; }
.iv-rubric td:first-child { white-space:nowrap; font-weight:700; }
.iv-rubric .iv-pt { display:block; font-weight:400; color:var(--muted); font-size:11.5px; }
.iv-rubric .iv-partial { display:block; color:var(--muted); font-size:11.5px; margin-top:2px; }
.iv-actions { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
.iv-actions .sv-btn { flex:1 1 40%; }
.iv-actions .sv-btn.pri { flex-basis:100%; }
`;
let cssDone = false;
function ensureIvCss() {
  if (cssDone || typeof document === "undefined") return;
  const st = document.createElement("style");
  st.id = "ash-iv-css"; st.textContent = CSS;
  document.head.appendChild(st);
  cssDone = true;
}

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const DEFAULT_TITLES = ["방침", "전개", "확인"];

/** 해설 levels → HTML 문자열 (figanim 마크업 계약: .lv.anim-level[data-anim] > .fig-stage + [data-step]) */
export function solutionHtml(item) {
  const levels = solutionLevels(item);
  if (!levels.length) return "";
  return levels.map((lv, i) => {
    const l = lv && typeof lv === "object" ? lv : {};
    const steps = Array.isArray(l.steps) ? l.steps.filter((s) => s != null && String(s).trim() !== "") : [];
    const text = steps.length ? "" : String(l.text ?? "").trim();
    const fig = figureHtml(l.figure, 320);
    const anim = Array.isArray(l.anim) && l.anim.length && fig ? l.anim : null;
    const title = l.title || DEFAULT_TITLES[i] || `${i + 1}단계`;
    let body = "";
    if (steps.length) {
      body = `<ol>${steps.map((s, j) => `<li data-step="${j}">${mathHtml(s)}</li>`).join("")}</ol>`;
    } else if (text) {
      body = `<p data-step="0">${mathHtml(text)}</p>`;
      if (anim) for (let j = 1; j < anim.length; j++) body += `<span data-step="${j}" hidden></span>`;
    }
    if (!fig && !body) return "";
    return `<div class="lv${anim ? " anim-level" : ""}"${anim ? ` data-anim="${esc(JSON.stringify(anim))}"` : ""}>`
      + `<div class="lv-title">${esc(title)}</div>`
      + (fig ? `<div class="fig-stage">${fig}</div>` : "")
      + body
      + `</div>`;
  }).join("");
}

/** reveal 용 initialAnswer → 결과 객체 */
function normInitial(item, ia) {
  const choices = Array.isArray(item?.choices) ? item.choices : [];
  if (ia == null) return { correct: null, rawAnswer: null, chosenIndex: null, chosenChoice: null, tag: null };
  if (typeof ia === "string" || typeof ia === "number") {
    const raw = String(ia);
    const idx = kindOf(item) === "choice" ? choices.findIndex((c) => String(c) === raw) : -1;
    const chosenIndex = idx >= 0 ? idx : null;
    const chosenChoice = idx >= 0 ? choices[idx] : null;
    const correct = idx >= 0 ? isChoiceCorrect(item, idx) : isCorrect(item, raw);
    return { correct, rawAnswer: raw, chosenIndex, chosenChoice, tag: correct ? null : distractorTag(item, chosenChoice) };
  }
  const chosenIndex = Number.isInteger(ia.chosenIndex) ? ia.chosenIndex : null;
  const chosenChoice = ia.chosenChoice ?? (chosenIndex != null ? choices[chosenIndex] ?? null : null);
  const rawAnswer = ia.rawAnswer ?? chosenChoice ?? null;
  let correct = typeof ia.correct === "boolean" ? ia.correct : null;
  if (ia.skipped) correct = false;
  else if (correct === null) {
    if (chosenIndex != null) correct = isChoiceCorrect(item, chosenIndex);
    else if (rawAnswer != null && String(rawAnswer).trim()) correct = isCorrect(item, rawAnswer);
  }
  return {
    correct, rawAnswer, chosenIndex, chosenChoice, skipped: !!ia.skipped, elapsedSec: ia.elapsedSec ?? null,
    tag: ia.tag ?? (correct === false ? distractorTag(item, chosenChoice) : null),
  };
}

export default function ItemView(props) {
  // 문항이 바뀌면 내부 상태를 통째로 새로 시작한다
  return <ItemViewInner key={props.item?.id || "none"} {...props} />;
}

function ItemViewInner({
  item, index = null, uid = null, setId = null, seq = null,
  onAnswered, onNext, nextLabel = "다음 문제",
  autoLog = true, showSolution = true, allowAsk = true, allowWrongNote = true,
  reveal = false, initialAnswer = null, onToast = null,
}) {
  const kind = kindOf(item);
  const [ownToast, setOwnToast] = useToast();
  const toast = onToast || setOwnToast;

  const [sel, setSel] = useState(null);           // 고른 보기
  const [text, setText] = useState("");           // 단답 입력
  const [res, setRes] = useState(() => (reveal ? normInitial(item, initialAnswer) : null));
  const [retryN, setRetryN] = useState(0);
  const [seenSol, setSeenSol] = useState(false);  // 해설을 한 번이라도 봤는가 (다시 풀 때 solutionSeen)
  const [note, setNote] = useState("idle");       // idle | saving | added | exists
  const [, setTick] = useState(0);
  const startRef = useRef(Date.now());
  const firstInputRef = useRef(null);
  const editsRef = useRef(0);
  const inputRef = useRef(null);
  const solRef = useRef(null);

  const answered = !!res;
  const pending = !!res?.pending;                  // 서술형 자기 채점 대기
  const showSol = showSolution && (answered || reveal);
  const solHtml = useMemo(() => solutionHtml(item), [item]);
  const levelsN = useMemo(() => solutionLevels(item).length, [item]);

  useEffect(() => { ensureIvCss(); ensureMathCss(); }, []);

  // 경과 시간 — 답을 내기 전까지 1초마다 갱신
  useEffect(() => {
    if (reveal || answered) return;
    const t = setInterval(() => setTick((x) => x + 1), 1000);
    return () => clearInterval(t);
  }, [reveal, answered]);

  // 해설 DOM — 내가 직접 넣고(문자열) figanim 을 붙인다. React 는 컨테이너만 소유한다.
  useEffect(() => {
    if (!showSol || typeof document === "undefined") return;
    const el = solRef.current;
    if (!el || !solHtml) return;
    el.innerHTML = solHtml;
    let players = [];
    try { players = mountAll(el, {}) || []; } catch { players = []; }
    return () => {
      for (const p of players) { try { p.destroy?.(); p.stop?.(); } catch { /* 무시 */ } }
      el.innerHTML = "";
    };
  }, [showSol, solHtml]);

  if (!item) return null;

  const elapsedNow = Math.floor((Date.now() - startRef.current) / 1000);
  const shownSec = answered && res.elapsedSec != null ? res.elapsedSec : elapsedNow;
  const overTime = !answered && item.time_limit && elapsedNow > item.time_limit;

  const markInput = () => { if (firstInputRef.current == null) firstInputRef.current = Date.now() - startRef.current; };

  /** 채점 결과 확정 — 기록 · 배너 · 콜백 */
  const finish = (r, elapsedSec = (Date.now() - startRef.current) / 1000) => {
    const tag = r.correct ? null : distractorTag(item, r.chosenChoice);
    const full = { ...r, elapsedSec: Math.max(0, Math.round(elapsedSec)), tag, retryN, solutionSeen: seenSol, pending: false };
    if (autoLog && uid && item.id) {
      logAttempt({
        uid, item, rawAnswer: r.rawAnswer, correct: r.correct, chosenIndex: r.chosenIndex, chosenChoice: r.chosenChoice,
        elapsedSec, hintLevel: 0, solutionSeen: seenSol, retryN, setId, seq,
        firstInputMs: firstInputRef.current == null ? null : Math.round(firstInputRef.current), editsN: editsRef.current,
      });
    }
    setRes(full);
    if (showSolution) setSeenSol(true);
    onAnswered?.(full);
  };

  const submitChoice = (i) => {
    if (answered || i == null || !item.choices?.[i]) return;
    finish({ correct: isChoiceCorrect(item, i), rawAnswer: item.choices[i], chosenIndex: i, chosenChoice: item.choices[i] });
  };
  const onSelect = (i) => {
    if (answered) return;
    markInput();
    if (sel === i) { submitChoice(i); return; }   // 같은 보기를 두 번 누르면 제출
    if (sel != null) editsRef.current += 1;
    setSel(i);
  };
  const submitText = () => {
    if (answered) return;
    const t = text.trim();
    if (!t) { toast("답을 입력해 주세요"); inputRef.current?.focus(); return; }
    if (kind === "essay") {   // 자동 채점 불가 — 예시 답안을 보고 스스로 채점
      setRes({ correct: null, rawAnswer: t, chosenIndex: null, chosenChoice: null, pending: true, elapsedSec: Math.round((Date.now() - startRef.current) / 1000), tag: null });
      setSeenSol(true);
      return;
    }
    finish({ correct: isCorrect(item, t), rawAnswer: t, chosenIndex: null, chosenChoice: null });
  };
  const submitOx = (v) => {
    if (answered) return;
    markInput();
    const alt = v === "O" ? "○" : "×";
    finish({ correct: isCorrect(item, v) || isCorrect(item, alt), rawAnswer: v, chosenIndex: null, chosenChoice: null });
  };
  const selfGrade = (ok) => {
    if (!pending) return;
    finish({ correct: ok, rawAnswer: res.rawAnswer, chosenIndex: null, chosenChoice: null }, res.elapsedSec);
  };
  const retry = () => {
    setRes(null); setSel(null); setText("");
    setRetryN((n) => n + 1);
    startRef.current = Date.now(); firstInputRef.current = null; editsRef.current = 0;
    setTimeout(() => inputRef.current?.focus(), 0);
  };
  const addNote = async () => {
    if (note !== "idle") return;
    if (!uid) { toast("로그인이 필요해요"); return; }
    setNote("saving");
    const r = await saveItemWrongNotes({ uid, entries: [{ item, myAnswer: res?.chosenChoice ?? res?.rawAnswer ?? null, tag: res?.tag || null }], source: "문제풀이" });
    if (r.error) { setNote("idle"); toast("오답노트에 저장하지 못했어요"); return; }
    if (r.added) { setNote("added"); toast("오답노트에 추가했어요"); }
    else { setNote("exists"); toast("이미 오답노트에 있는 문항이에요"); }
  };

  const verdict = !answered ? null
    : res.correct === true ? "정답이에요!"
    : res.correct === false ? (res.skipped ? "건너뛴 문제예요" : "아쉬워요, 오답이에요")
    : "정답을 확인해요";
  const bannerCls = "iv-banner" + (res?.correct === true ? " ok" : res?.correct === false ? " bad" : "");
  const rubric = hasRubric(item) ? item.solution.rubric : null;
  const modelAnswer = item.solution?.model_answer ? String(item.solution.model_answer) : "";
  const noteLabel = { added: "추가됨", exists: "이미 있음", saving: "저장 중…" }[note] || "오답노트에 추가";

  return (
    <div className="sv-card iv-card">
      {!reveal && (
        <div className="iv-time">
          <span className={"iv-clock" + (overTime ? " iv-over" : "")}>⏱ {fmtClock(shownSec)}</span>
          {item.time_limit ? <span>· 권장 {item.time_limit}초</span> : null}
          {retryN > 0 && <span>· 다시 풀기 {retryN}회</span>}
        </div>
      )}

      <ItemQuestion item={item} index={index} meta
        selected={answered ? (res.chosenIndex ?? sel) : sel}
        reveal={answered && !pending}
        onSelect={kind === "choice" && !answered ? onSelect : undefined} />

      {/* 입력부 */}
      {!answered && kind === "choice" && (
        <button className="sv-btn pri full iv-submit" disabled={sel == null} onClick={() => submitChoice(sel)}>
          {sel == null ? "보기를 골라 주세요" : `${CIRCLED[sel] || sel + 1} 제출`}
        </button>
      )}
      {!answered && kind === "short" && (
        <>
          <div className="iv-short">
            <input ref={inputRef} className="sv-in" type="text" inputMode="text" autoComplete="off" autoCapitalize="off" autoCorrect="off" spellCheck={false} enterKeyHint="done"
              placeholder="답 입력 (예: 3, 1/2, 60°, 3π)" value={text}
              onChange={(e) => { markInput(); editsRef.current += 1; setText(e.target.value); }}
              onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); submitText(); } }} />
            <button className="sv-btn pri" disabled={!text.trim()} onClick={submitText}>제출</button>
          </div>
          <div className="iv-hint">분수는 1/2 처럼, 각도는 60 또는 60°, π는 π 또는 pi 로 써도 돼요</div>
        </>
      )}
      {!answered && kind === "ox" && (
        <div className="iv-ox">
          <button className="sv-btn" onClick={() => submitOx("O")}>○</button>
          <button className="sv-btn" onClick={() => submitOx("X")}>×</button>
        </div>
      )}
      {!answered && kind === "essay" && (
        <>
          <textarea ref={inputRef} className="sv-in sv-ta iv-ta" placeholder="풀이 과정과 답을 써 주세요" value={text}
            onChange={(e) => { markInput(); editsRef.current += 1; setText(e.target.value); }} />
          <button className="sv-btn pri full iv-submit" disabled={!text.trim()} onClick={submitText}>제출하고 예시 답안 보기</button>
        </>
      )}

      {/* 결과 배너 */}
      {answered && (
        <div className={bannerCls}>
          {pending ? (
            <>
              <div className="iv-verdict">아래 예시 답안과 비교해서 스스로 채점해 보세요</div>
              <div className="iv-row">
                <button className="sv-btn sm" onClick={() => selfGrade(true)}>맞았어요</button>
                <button className="sv-btn sm" onClick={() => selfGrade(false)}>틀렸어요</button>
              </div>
            </>
          ) : (
            <>
              <div className="iv-verdict">{verdict}</div>
              <div className="iv-ans"><span className="iv-lab">정답</span><MathText text={correctAnswerText(item)} /></div>
              {res.correct !== true && (res.rawAnswer || res.skipped) && (
                <div className="iv-mine"><span className="iv-lab">내 답</span><MathText text={myAnswerText(item, res)} /></div>
              )}
              {res.correct === false && res.tag && <div className="iv-mc">이런 실수를 자주 해요: {mcLabel(res.tag)}</div>}
              {res.correct === false && !reveal && (
                <div className="iv-row"><button className="sv-btn sm" onClick={retry}>다시 풀어보기</button></div>
              )}
            </>
          )}
        </div>
      )}

      {/* 해설 — 답을 낸 뒤에만 (미리 보기 없음) */}
      {showSol && (levelsN ? <div ref={solRef} className="isol iv-sol" /> : <div className="iv-nosol">이 문항은 아직 해설이 준비되지 않았어요.</div>)}
      {showSol && modelAnswer && (
        <details className="iv-details">
          <summary>서술형 답안 예시</summary>
          <MathText as="div" text={modelAnswer} />
        </details>
      )}
      {showSol && rubric && (
        <details className="iv-details">
          <summary>채점 기준{rubric.total ? ` · 총 ${rubric.total}점` : ""}</summary>
          <table className="iv-rubric">
            <thead><tr><th>요소</th><th>기준</th></tr></thead>
            <tbody>
              {rubric.items.map((r, i) => (
                <tr key={i}>
                  <td>{r.no ?? i + 1}. {r.element}<span className="iv-pt">{r.points != null ? `${r.points}점` : ""}</span></td>
                  <td>
                    <MathText text={r.criterion} />
                    {r.partial && <span className="iv-partial">부분 점수: {r.partial}</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </details>
      )}

      {/* 행동 버튼 */}
      {answered && !pending && (
        <div className="iv-actions">
          {onNext && <button className="sv-btn pri" onClick={onNext}>{nextLabel}</button>}
          {allowAsk && <button className="sv-btn" onClick={() => askAboutItem(item)}>질문하기</button>}
          {allowWrongNote && (
            <button className="sv-btn" disabled={note !== "idle"} onClick={addNote}>{noteLabel}</button>
          )}
        </div>
      )}
      {!onToast && ownToast && <div className="sv-toast">{ownToast}</div>}
    </div>
  );
}
