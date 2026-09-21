// src/pages/PracticeViewer.jsx — 예제·유제 v3 (해시 라우트: #/p/<conceptId>)
//
// 흐름 (2026-09-21 확정):
//   예제  문제 → 해설(단계식) → 답 표시.  답 입력 없음. 해설을 끝까지 보면 해결로 기록.
//   유제  문제 → 답 입력(한 번) → 맞든 틀리든 해설(단계식) → 답 표시 → 다음 문제.  맞히면 해결로 기록, 틀리면 "다시 풀어 보기".
//   입력 칸 힌트는 표기 방식만 (src/lib/practice.js inputHint) — 세트 JSON 의 placeholder 예시는 쓰지 않는다.
//
// 세트 JSON 규격 (practice_sets.problems):
// {
//   "id": "p01", "level": "기본"|"표준"|"상", "kind": "예제"|"유제",
//   "review": ["소인수분해"],
//   "text": [ {"t":"문장 조각"}, {"br":true}, ... ], // {{2/3}} 토큰 → 세로 분수 / {"br":true} → 줄바꿈
//   "svg": "<svg ...>",
//   "choices": ["㉠", "㉠, ㉡", ...],             // 있으면 객관식 — 답은 번호로 (보기를 눌러도 됨)
//   "steps": [ { "hl":[..], "svgHl":[..], "svgCls":[..], "note":"...", "expr":"식" | ["줄1","= 줄2"] } ],
//   "methods": [ {"title":"방법1","steps":[...]}, ... ],   // 여러 방법: 전부 봐야 끝
//   "answer": { "label":"답", "accept":["8"], "placeholder":"",   // placeholder 는 예시를 뗀 안내문만 쓴다
//               "unit":"원",                      // 단위 누락 시 주황 경고 (시도로 치지 않음)
//               "format":"fraction" }             // 분자/분모 두 칸 입력 (정확 일치 판정)
// }
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/authx";
import { CIRC, practiceKind, normAns, isCorrect, unitMissing, inputHint, displayAnswer, practicePhase } from "../lib/practice";

const HL = ["#FFF3A3", "#B9F0C8", "#BFDFFF", "#F5C9F0", "#FFD9B3"];
const HL_INK = "#1F2430";

// ---------- 리치 텍스트: {{a/b}} → 세로 분수 ----------
function rich(str) {
  const parts = String(str ?? "").split(/(\{\{[^}]+\}\})/g);
  return parts.map((p, i) => {
    const m = p.match(/^\{\{([^/}]+)\/([^}]+)\}\}$/);
    if (m) {
      return (
        <span className="pv-frac" key={i}>
          <span className="pv-fr-n">{m[1]}</span>
          <span className="pv-fr-d">{m[2]}</span>
        </span>
      );
    }
    return <span key={i}>{p}</span>;
  });
}

export default function PracticeViewer({ conceptId }) {
  const [set, setSet] = useState(undefined);
  const [uid, setUid] = useState(null);
  const [solved, setSolved] = useState([]);
  const [pi, setPi] = useState(0);
  const [mi, setMi] = useState(0);
  const [stepByM, setStepByM] = useState({});     // 방법별 공개 단계 수
  const [attempts, setAttempts] = useState({});   // 유제 시도 { [pid]: { result:"ok"|"no", input } } — 세션 동안
  const [ans, setAns] = useState("");
  const [ansN, setAnsN] = useState("");           // 분수 분자
  const [ansD, setAnsD] = useState("");           // 분수 분모
  const [flash, setFlash] = useState("");         // ok | no | warn
  const [warnMsg, setWarnMsg] = useState("");
  const [shake, setShake] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    (async () => {
      const { data: s } = await supabase.auth.getSession();
      const u = s?.session?.user?.id || null;
      setUid(u);
      const { data: row } = await supabase.from("practice_sets")
        .select("*").eq("concept_id", conceptId).maybeSingle();
      setSet(row || null);
      if (u) {
        const { data: pg } = await supabase.from("practice_progress")
          .select("solved").eq("user_id", u).eq("concept_id", conceptId).maybeSingle();
        setSolved(Array.isArray(pg?.solved) ? pg.solved : []);
      }
    })();
  }, [conceptId]);

  const problems = set?.problems || [];
  const p = problems[pi];
  const kind = practiceKind(p);
  const isExample = kind === "예제";
  const isFraction = p?.answer?.format === "fraction";
  const hasChoices = (p?.choices?.length || 0) > 0;
  const attempt = p ? attempts[p.id] || null : null;
  const doneThis = !!p && solved.includes(p.id);
  const phase = practicePhase(p, { attempt, solved: doneThis });   // answer | explain

  // 방법 통합: methods 없으면 steps를 단일 방법으로
  const methodsArr = useMemo(() => {
    if (!p) return [];
    return p.methods?.length ? p.methods : [{ steps: p.steps || [] }];
  }, [p]);
  const multi = (p?.methods?.length || 0) > 1;
  const curSteps = methodsArr[mi]?.steps || [];
  const shownCount = stepByM[mi] || 0;
  const shown = phase === "explain" ? curSteps.slice(0, shownCount) : [];
  const methodDone = (i) => (stepByM[i] || 0) >= (methodsArr[i]?.steps.length || 0);
  const allDone = phase === "explain" && methodsArr.length > 0 && methodsArr.every((_, i) => methodDone(i));
  const nextUndone = methodsArr.findIndex((_, i) => !methodDone(i));
  const cleared = problems.length > 0 && problems.every((x) => solved.includes(x.id));
  const isLast = pi === problems.length - 1;

  const segHl = useMemo(() => {
    const map = {};
    shown.forEach((st, i) => (st.hl || []).forEach((idx) => { map[idx] = i % HL.length; }));
    return map;
  }, [shown]);
  const svgHlIds = useMemo(() => {
    const map = {};
    shown.forEach((st, i) => (st.svgHl || []).forEach((id) => { map[id] = i % HL.length; }));
    return map;
  }, [shown]);
  const svgCls = useMemo(() => shown.flatMap((st) => st.svgCls || []), [shown]);

  const goProblem = (i) => {
    setPi(i); setMi(0); setStepByM({});
    setAns(""); setAnsN(""); setAnsD("");
    setWarnMsg("");
  };

  const saveProgress = async (newSolved) => {
    if (!uid) return;
    await supabase.from("practice_progress").upsert({
      user_id: uid, concept_id: conceptId,
      solved: newSolved,
      cleared: problems.every((x) => newSolved.includes(x.id)),
      updated_at: new Date().toISOString(),
    });
  };
  const markSolved = (pid) => {
    if (solved.includes(pid)) return;
    const ns = [...solved, pid];
    setSolved(ns);
    saveProgress(ns);
  };

  // 예제: 해설을 끝까지 보면 해결
  useEffect(() => {
    if (p && isExample && allDone && !doneThis) markSolved(p.id);
  }, [p, isExample, allDone, doneThis]); // eslint-disable-line react-hooks/exhaustive-deps

  // 유제: 답 칸이 열리면 포커스
  useEffect(() => {
    if (phase === "answer" && !hasChoices) { const t = setTimeout(() => inputRef.current?.focus(), 0); return () => clearTimeout(t); }
  }, [phase, hasChoices, pi]);

  const leave = () => {
    if (window.history.length > 1) window.history.back();
    else window.location.hash = "#/";
  };

  /** 유제 답 확인 — 한 번만. 단위만 빠진 건 시도로 치지 않고 다시 쓰게 한다 */
  const submit = () => {
    if (!p || flash || phase !== "answer") return;
    const a = p.answer || {};
    const input = isFraction ? `${ansN}/${ansD}` : (inputRef.current?.value ?? ans);   // 입력 직후 눌러도 최신 값
    if (!normAns(input) || (isFraction && (!ansN.trim() || !ansD.trim()))) {
      setShake(true); setTimeout(() => { setShake(false); inputRef.current?.focus(); }, 450);
      return;
    }
    if (isCorrect(input, a.accept, { exact: isFraction })) {
      setFlash("ok"); setWarnMsg("");
      setAttempts((m) => ({ ...m, [p.id]: { result: "ok", input } }));
      markSolved(p.id);
      setTimeout(() => setFlash(""), 700);
      return;
    }
    if (!isFraction && unitMissing(input, a)) {
      setFlash("warn");
      setWarnMsg(`⚠ 단위가 빠졌어요. ${a.unit} 까지 붙여서 다시 써 주세요.`);
      setTimeout(() => { setFlash(""); inputRef.current?.focus(); }, 800);
      return;
    }
    setFlash("no"); setShake(true); setWarnMsg("");
    setAttempts((m) => ({ ...m, [p.id]: { result: "no", input } }));
    setTimeout(() => { setFlash(""); setShake(false); }, 550);
  };

  /** 틀린 유제 다시 풀기 — 시도를 지우고 해설을 접는다 */
  const retry = () => {
    if (!p) return;
    setAttempts((m) => { const c = { ...m }; delete c[p.id]; return c; });
    setMi(0); setStepByM({}); setAns(""); setAnsN(""); setAnsD(""); setWarnMsg("");
  };

  const svgHtml = useMemo(() => {
    if (!p?.svg) return null;
    let s = p.svg;
    Object.entries(svgHlIds).forEach(([id, c]) => {
      s = s.replace(new RegExp(`id="${id}"`, "g"),
        `id="${id}" style="stroke:${HL[c]};stroke-width:4;filter:drop-shadow(0 0 2px ${HL[c]})"`);
      s = s.replace(new RegExp(`id='${id}'`, "g"),
        `id='${id}' style='stroke:${HL[c]};stroke-width:4;filter:drop-shadow(0 0 2px ${HL[c]})'`);
    });
    return s;
  }, [p, svgHlIds]);

  if (set === undefined) return <div className="pv-wrap"><Style /></div>;
  if (set === null || problems.length === 0) {
    return (
      <div className="pv-wrap"><Style />
        <p className="pv-empty">아직 이 개념의 예제·유제가 준비되지 않았어요.</p>
        <a className="pv-btn" href="#/">← 홈으로</a>
      </div>
    );
  }

  const answerObj = p.answer || {};
  const hint = inputHint(answerObj, { hasChoices, nChoices: p.choices?.length || 0 });
  const finalAnswer = displayAnswer(answerObj, { hasChoices });
  const correctChoice = hasChoices ? Number(normAns(answerObj.accept?.[0])) : null;   // 1부터
  const chosen = hasChoices ? Number(normAns(attempt ? attempt.input : ans)) : null;
  const wrong = attempt?.result === "no";
  const nextBtn = isLast || cleared
    ? <button className="pv-btn pv-btn-main" onClick={leave}>🎉 학습 완료 →</button>
    : <button className="pv-btn pv-btn-main" onClick={() => goProblem(pi + 1)}>다음 문제 →</button>;

  return (
    <div className="pv-wrap"><Style />
      {flash && <div className={`pv-flash pv-flash-${flash}`} />}

      <header className="pv-head">
        <button className="pv-back" onClick={leave}>← 나가기</button>
        <h2 className="pv-title">{set.title || "예제 · 유제"}</h2>
        <span className="pv-count">{solved.filter((id) => problems.some((x) => x.id === id)).length}/{problems.length}</span>
      </header>

      {cleared && (
        <div className="pv-clear">
          🎉 챕터 클리어! 모든 문제를 해결했어요.
          <button className="pv-clear-btn" onClick={leave}>학습 완료 →</button>
        </div>
      )}

      <div className="pv-nav">
        {problems.map((x, i) => {
          const a = attempts[x.id];
          const done = solved.includes(x.id);
          return (
            <button key={x.id}
              className={"pv-chip" + (i === pi ? " on" : "") + (done ? " done" : "") + (!done && a?.result === "no" ? " miss" : "")}
              onClick={() => goProblem(i)}>
              {done ? "✓" : a?.result === "no" ? "✗" : i + 1}
            </button>
          );
        })}
      </div>

      <div className="pv-card">
        <div className="pv-meta">
          <span className={"pv-lv lv-" + (p.level || "기본")}>{p.level || "기본"}</span>
          <span className="pv-kind">{kind} {pi + 1}</span>
          {(p.review || []).map((r) => <span className="pv-review" key={r}>🔁 {r}</span>)}
        </div>

        <p className="pv-text">
          {(p.text || []).map((seg, i) => (
            seg.br ? <br key={i} /> : (
              <span key={i}
                className={"pv-seg" + (segHl[i] !== undefined ? " on" : "") + (/\{\{/.test(seg.t || "") ? " tall" : "")}
                style={segHl[i] !== undefined ? { background: HL[segHl[i]], color: HL_INK } : undefined}>
                {rich(seg.t)}
              </span>
            )
          ))}
        </p>

        {hasChoices && (
          <div className={"pv-choices" + (phase === "answer" ? " pick" : "")} role={phase === "answer" ? "radiogroup" : undefined}>
            {p.choices.map((c, i) => {
              const no = i + 1;
              const cls = "pv-choice"
                + (phase === "answer" && chosen === no ? " on" : "")
                + (phase === "explain" && (allDone || attempt?.result === "ok") && correctChoice === no ? " ok" : "")   // 정답 보기는 해설이 끝난 뒤에
                + (phase === "explain" && wrong && chosen === no ? " bad" : "");
              return phase === "answer" ? (
                <button type="button" className={cls} key={i} role="radio" aria-checked={chosen === no}
                  onClick={() => { setAns(String(no)); setWarnMsg(""); }}>
                  <b>{CIRC[i]}</b> {rich(c)}
                </button>
              ) : (
                <div className={cls} key={i}><b>{CIRC[i]}</b> {rich(c)}</div>
              );
            })}
          </div>
        )}

        {svgHtml && (
          <div className={["pv-svg", ...svgCls].join(" ")} dangerouslySetInnerHTML={{ __html: svgHtml }} />
        )}

        {/* ── 유제: 답 먼저 ── */}
        {!isExample && (
          <div className="pv-answer">
            <label className="pv-alabel">{answerObj.label || "답"}</label>
            <div className="pv-arow">
              {isFraction ? (
                <div className={"pv-fracin" + (shake ? " shake" : "") + (attempt?.result === "ok" || (doneThis && !attempt) ? " ok" : "") + (wrong ? " bad" : "")}>
                  <input ref={inputRef} className="pv-fr-in" inputMode="numeric"
                    value={attempt ? attempt.input.split("/")[0] : doneThis ? (answerObj.accept?.[0] || "").split("/")[0] : ansN}
                    disabled={phase !== "answer"}
                    onChange={(e) => setAnsN(e.target.value)} placeholder="분자" />
                  <div className="pv-fr-bar" />
                  <input className="pv-fr-in" inputMode="numeric"
                    value={attempt ? attempt.input.split("/")[1] : doneThis ? (answerObj.accept?.[0] || "").split("/")[1] : ansD}
                    disabled={phase !== "answer"}
                    onChange={(e) => setAnsD(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && submit()} placeholder="분모" />
                </div>
              ) : (
                <input ref={inputRef}
                  className={"pv-input" + (shake ? " shake" : "") + (attempt?.result === "ok" || (doneThis && !attempt) ? " ok" : "") + (wrong ? " bad" : "") + (flash === "warn" ? " warn" : "")}
                  value={attempt ? attempt.input : doneThis ? (answerObj.accept?.[0] ?? "") : ans}
                  disabled={phase !== "answer"}
                  inputMode={hasChoices ? "numeric" : "text"}
                  onChange={(e) => { setAns(e.target.value); setWarnMsg(""); }}
                  onKeyDown={(e) => e.key === "Enter" && submit()}
                  placeholder={hint} aria-label={answerObj.label || "답"} />
              )}
              {phase === "answer" && <button className="pv-btn pv-btn-main" onClick={submit}>확인</button>}
            </div>
            {warnMsg && <p className="pv-warnmsg">{warnMsg}</p>}
            {attempt?.result === "ok" && <p className="pv-okmsg">정답! 해설로 풀이를 확인해요 👏</p>}
            {wrong && <p className="pv-nomsg">아쉬워요. 해설을 본 다음 다시 풀어 볼 수 있어요.</p>}
          </div>
        )}

        {/* ── 해설 (예제는 바로, 유제는 답 뒤에) ── */}
        {phase === "explain" && (
          <>
            {multi && (
              <div className="pv-tabs">
                {methodsArr.map((m, i) => (
                  <button key={i} className={"pv-tab" + (i === mi ? " on" : "") + (methodDone(i) ? " ok" : "")}
                    onClick={() => setMi(i)}>
                    {methodDone(i) ? "✓ " : ""}{m.title || `방법 ${i + 1}`}
                  </button>
                ))}
              </div>
            )}
            {p.methods?.length === 1 && <p className="pv-mtitle">{p.methods[0].title}</p>}

            <div className="pv-steps">
              {shown.map((st, i) => (
                <div className="pv-step" key={i}>
                  <span className="pv-dot" style={{ background: HL[i % HL.length] }} />
                  <div className="pv-step-body">
                    {st.note && <p className="pv-note">{rich(st.note)}</p>}
                    {st.expr && (
                      <div className="pv-expr">
                        {(Array.isArray(st.expr) ? st.expr : [st.expr]).map((line, li) => (
                          <div className="pv-expr-line" key={li}>{rich(line)}</div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {!allDone ? (
              shownCount < curSteps.length ? (
                <button className="pv-btn pv-btn-main"
                  onClick={() => setStepByM((s) => ({ ...s, [mi]: shownCount + 1 }))}>
                  {shownCount === 0 ? (multi ? `${methodsArr[mi].title || `방법 ${mi + 1}`} 시작하기` : "해설 시작하기") : "다음 단계 →"}
                  <span className="pv-prog"> {shownCount}/{curSteps.length}</span>
                </button>
              ) : (
                <button className="pv-btn pv-btn-main" onClick={() => setMi(nextUndone)}>
                  {methodsArr[nextUndone]?.title || `방법 ${nextUndone + 1}`} 보기 →
                  <span className="pv-prog"> (다른 방법도 보면 끝나요)</span>
                </button>
              )
            ) : (
              <div className="pv-final">
                <div className="pv-final-row">
                  <span className="pv-alabel">{answerObj.label || "답"}</span>
                  <b className="pv-final-ans">{finalAnswer ? rich(finalAnswer) : "—"}</b>
                  {wrong && <span className="pv-final-mine">내 답 <s>{hasChoices && Number.isInteger(chosen) && CIRC[chosen - 1] ? CIRC[chosen - 1] : attempt.input}</s></span>}
                </div>
                {isExample
                  ? <p className="pv-okmsg">풀이를 끝까지 봤어요 👏</p>
                  : wrong ? null : <p className="pv-okmsg">잘 이해했어요 👏</p>}
                <div className="pv-actions">
                  {wrong && <button className="pv-btn" onClick={retry}>다시 풀어 보기</button>}
                  {nextBtn}
                </div>
                {(isLast || cleared) && <button className="pv-again" onClick={() => goProblem(0)}>처음부터 다시 보기</button>}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .pv-wrap{max-width:640px;margin:0 auto;padding:16px 14px 60px;color:var(--text,#1c1c1e);
        font-family:'Pretendard Variable',Pretendard,'Malgun Gothic',system-ui,sans-serif}
      .pv-flash{position:fixed;inset:0;pointer-events:none;z-index:50;animation:pvFlash .55s ease-out}
      .pv-flash-no{background:radial-gradient(circle at 50% 40%, rgba(220,38,38,.28), rgba(220,38,38,.12) 60%, transparent)}
      .pv-flash-ok{background:radial-gradient(circle at 50% 40%, rgba(22,163,74,.30), rgba(22,163,74,.12) 60%, transparent)}
      .pv-flash-warn{background:radial-gradient(circle at 50% 40%, rgba(245,158,11,.30), rgba(245,158,11,.12) 60%, transparent)}
      @keyframes pvFlash{0%{opacity:0}20%{opacity:1}100%{opacity:0}}
      .pv-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
      .pv-back{font-size:13px;color:var(--muted,#6b7280);background:none;border:none;padding:0;white-space:nowrap;cursor:pointer}
      .pv-title{flex:1;font-size:17px;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
      .pv-count{font-size:12px;color:var(--muted,#8a8f98)}
      .pv-clear{background:var(--accent,#0DA95F);color:#fff;border-radius:12px;padding:10px 14px;
        font-size:14px;font-weight:700;text-align:center;margin-bottom:10px;display:flex;
        align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}
      .pv-clear-btn{background:rgba(255,255,255,.22);border:none;color:#fff;font-weight:800;
        padding:7px 12px;border-radius:9px;font-size:13px;cursor:pointer}
      .pv-nav{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
      .pv-chip{width:34px;height:34px;border-radius:10px;border:1px solid var(--border,#d6d9de);
        background:var(--surface,#fff);color:var(--muted,#6b7280);font-size:13px;font-weight:700}
      .pv-chip.on{border-color:var(--accent,#0DA95F);color:var(--text,#111);box-shadow:0 0 0 2px var(--accent,#0DA95F) inset}
      .pv-chip.done{background:var(--accent,#0DA95F);border-color:var(--accent,#0DA95F);color:#fff}
      .pv-chip.miss{border-color:var(--bad,#dc2626);color:var(--bad,#dc2626)}
      .pv-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:16px;padding:16px}
      .pv-meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px}
      .pv-lv{font-size:11px;font-weight:800;padding:3px 9px;border-radius:999px}
      .lv-기본{background:#DCFCE7;color:#166534}.lv-표준{background:#DBEAFE;color:#1E40AF}.lv-상{background:#FEE2E2;color:#991B1B}
      .pv-kind{font-size:12px;color:var(--muted,#8a8f98);font-weight:700}
      .pv-review{font-size:11px;background:var(--surface2,#f1f2f4);color:var(--muted,#6b7280);
        padding:3px 8px;border-radius:999px}
      .pv-text{font-size:16.5px;line-height:2.2;margin:0 0 6px;word-break:keep-all}
      .pv-seg{border-radius:5px;padding:1px 2px;transition:background .35s}
      .pv-choices{display:flex;flex-direction:column;gap:6px;margin:8px 0 4px;
        border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:12px 14px}
      .pv-choice{font-size:15px;line-height:1.6;text-align:left;color:inherit;background:none;border:1px solid transparent;
        border-radius:9px;padding:4px 8px;margin:0 -8px;font:inherit}
      .pv-choices.pick .pv-choice{cursor:pointer}
      .pv-choices.pick .pv-choice:hover{background:var(--surface2,#f4f6f8)}
      .pv-choice.on{border-color:var(--accent,#0DA95F);background:rgba(13,169,95,.10)}
      .pv-choice.ok{border-color:var(--good,#16a34a);background:rgba(22,163,74,.10)}
      .pv-choice.bad{border-color:var(--bad,#dc2626);background:rgba(220,38,38,.08);text-decoration:line-through}
      .pv-choice b{margin-right:6px}
      .pv-svg{margin:10px 0 4px;text-align:center;color:var(--text,#1c1c1e)}
      .pv-svg svg{max-width:100%;height:auto}
      .pv-tabs{display:flex;gap:6px;margin:10px 0 4px;flex-wrap:wrap}
      .pv-tab{font-size:12.5px;padding:8px 12px;border-radius:999px;border:1px solid var(--border,#d6d9de);
        background:var(--surface,#fff);color:var(--muted,#6b7280)}
      .pv-tab.on{background:var(--text,#1F2937);border-color:var(--text,#1F2937);color:var(--surface,#fff);font-weight:700}
      .pv-tab.ok{border-color:var(--accent,#0DA95F)}
      .pv-mtitle{font-size:13px;color:var(--muted,#6b7280);margin:10px 0 0;font-weight:700}
      .pv-steps{display:flex;flex-direction:column;gap:10px;margin:12px 0 4px}
      .pv-step{display:flex;gap:10px;animation:pvIn .3s ease-out}
      @keyframes pvIn{from{opacity:0;transform:translateY(6px)}}
      .pv-dot{width:12px;height:12px;border-radius:999px;margin-top:6px;flex-shrink:0;border:1px solid rgba(0,0,0,.12)}
      .pv-step-body{flex:1;min-width:0}
      .pv-note{margin:0;font-size:14px;line-height:1.65;color:var(--text,#374151)}
      .pv-expr{margin:6px 0 0;background:var(--surface2,#f4f6f8);
        border:1px solid var(--border,#e5e7eb);border-radius:10px;padding:9px 12px;overflow-x:auto}
      .pv-expr-line{font-size:14.5px;letter-spacing:.2px;white-space:pre;
        font-family:'Pretendard Variable',ui-monospace,monospace;line-height:1.9;
        font-variant-numeric:tabular-nums}
      .pv-frac{display:inline-flex;flex-direction:column;vertical-align:middle;
        text-align:center;margin:0 3px;line-height:1.1;font-size:.78em}
      .pv-seg.on{box-decoration-break:clone;-webkit-box-decoration-break:clone}
      .pv-seg.tall{display:inline-block;vertical-align:middle;line-height:1.25}
      .pv-seg.on.tall{padding:4px 8px;border-radius:8px}
      .pv-fr-n{padding:0 4px;border-bottom:1.6px solid currentColor}
      .pv-fr-d{padding:0 4px}
      .pv-btn{display:inline-flex;align-items:center;justify-content:center;gap:4px;padding:12px 16px;
        border-radius:11px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);
        font-size:14.5px;color:inherit;text-decoration:none;cursor:pointer}
      .pv-btn-main{width:100%;margin-top:10px;background:var(--accent,#0DA95F);border-color:var(--accent,#0DA95F);
        color:#fff;font-weight:800}
      .pv-prog{font-weight:400;font-size:12px;opacity:.85}
      .pv-answer{margin-top:12px;border-top:1px dashed var(--border,#e5e7eb);padding-top:12px}
      .pv-alabel{font-size:12px;color:var(--muted,#6b7280);font-weight:700}
      .pv-arow{display:flex;gap:8px;margin-top:6px;align-items:stretch}
      .pv-input{flex:1;min-width:0;padding:13px 14px;font-size:17px;border-radius:11px;
        border:1.5px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#111);outline:none}
      .pv-input:focus{border-color:var(--accent,#0DA95F)}
      .pv-input.ok{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .pv-input.bad,.pv-fracin.bad{border-color:var(--bad,#dc2626);background:rgba(220,38,38,.06)}
      .pv-input.warn{border-color:#F59E0B!important}
      .pv-input.shake,.pv-fracin.shake{animation:pvShake .45s}
      .pv-input.shake{border-color:var(--bad,#dc2626)!important}
      .pv-fracin.shake{outline:1.5px solid var(--bad,#dc2626);border-radius:12px}
      @keyframes pvShake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}
        30%,50%,70%{transform:translateX(-7px)}40%,60%{transform:translateX(7px)}}
      .pv-fracin{display:flex;flex-direction:column;align-items:center;gap:4px;flex:0 0 auto;
        padding:8px 10px;border:1.5px solid var(--border,#d6d9de);border-radius:12px;background:var(--surface,#fff)}
      .pv-fracin.ok{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .pv-fr-in{width:88px;text-align:center;font-size:17px;padding:7px 6px;border-radius:8px;
        border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#111);outline:none}
      .pv-fr-bar{width:96px;height:2px;background:var(--text,#1F2937);border-radius:2px}
      .pv-arow .pv-btn-main{width:auto;margin-top:0;flex-shrink:0}
      .pv-okmsg{margin:8px 0 0;font-size:13.5px;color:var(--good,#16a34a);font-weight:700;display:flex;align-items:center;gap:10px}
      .pv-nomsg{margin:8px 0 0;font-size:13.5px;color:var(--bad,#dc2626);font-weight:700}
      .pv-again{background:none;border:none;color:var(--muted,#8a8f98);font-size:12px;text-decoration:underline;cursor:pointer;padding:0;margin-top:10px}
      .pv-warnmsg{margin:8px 0 0;font-size:13px;color:#D97706;font-weight:700}
      .pv-final{margin-top:12px;border-top:1px dashed var(--border,#e5e7eb);padding-top:12px}
      .pv-final-row{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
      .pv-final-ans{font-size:20px;font-weight:900;color:var(--good,#16a34a)}
      .pv-final-mine{font-size:13px;color:var(--muted,#6b7280)}
      .pv-actions{display:flex;gap:8px;margin-top:10px;align-items:stretch}
      .pv-actions .pv-btn{flex:1;margin-top:0}
      .pv-empty{text-align:center;color:var(--muted,#8a8f98);margin:60px 0 16px}
    `}</style>
  );
}
