// 서술형 채점·첨삭 — #/solve/photo/essay (촬영) · ?cur=1 (방금 찍은 문제로)
// 문제 촬영 → 문항 부분 인식 → 답안 촬영 → 답안 부분 인식(전사, 고칠 수 있음) → 채점 기준표·채점·첨삭.
// 답안 원문은 보관 게이트 결정(retention.where)에 따라 기기 또는 서버에 남고, 결과는 항상 기기 보관소에 남는다.
import { useState } from "react";
import SolveShell, { useToast } from "../solve/SolveShell";
import MathText from "../../components/MathText";
import { trapText } from "../../lib/marking.js";
import { photoCall, stashCurrent } from "../../lib/photoApi";
import { newId } from "../../lib/deviceStore";
import Capture from "./Capture";
import { ProblemCard, Steps, Busy, KeepNote, currentProblem, saveDevice } from "./shared";

const VERDICT = { excellent: "아주 잘 썼어요", good: "잘 썼어요", partial: "절반쯤 왔어요", weak: "다시 써 봐요" };
const LEVEL = { full: "만점", partial: "부분", zero: "0점" };
const LEG_KIND = { size: "글씨 크기", messy: "난잡함", glyph: "헷갈리는 글자", spacing: "간격·정렬", crossout: "지운 흔적", other: "기타" };

export default function PhotoEssay({ useCur = false }) {
  const [toast, setToast] = useToast();
  const [p, setP] = useState(() => (useCur ? currentProblem() : null));
  const [a, setA] = useState(null);          // 답안 전사
  const [text, setText] = useState("");      // 학생이 고친 답안
  const [res, setRes] = useState(null);      // { result, std, retention }
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const hasCur = !!currentProblem();
  const at = !p ? 0 : !a ? 1 : 2;

  const onProblem = (r, { thumb }) => {
    const prob = { question: r.question, choices: r.choices, qtype: r.qtype, figure_note: r.figure_note, unit_guess: r.unit_guess, std: r.std, warnings: r.warnings, thumb };
    stashCurrent(prob); setP(prob);
  };
  const onAnswer = (r, { thumb }) => { setA({ ...r, thumb }); setText(r.answer || ""); setRes(null); setErr(null); };

  const grade = async () => {
    const answer = text.trim();
    if (!answer) { setToast("답안이 비어 있어요"); return; }
    setBusy(true); setErr(null);
    try {
      const r = await photoCall("essay", { question: p.question, figure_note: p.figure_note, choices: p.choices, answer, std: p.std, unit: p.unit_guess });
      setRes(r);
      saveDevice({ id: newId(), feature: "essay", question: p.question, figure_note: p.figure_note, unit: p.unit_guess, grade: r.std?.item_grade || p.std?.item_grade || null, answer, result: r.result, retention: r.retention });
    } catch (e) { setErr(e?.message || "채점에 실패했어요 — 잠시 뒤 다시 시도해 주세요."); }
    finally { setBusy(false); }
  };

  const restartAnswer = () => { setA(null); setText(""); setRes(null); setErr(null); };
  const restartAll = () => { setP(null); restartAnswer(); };

  return (
    <SolveShell title="서술형 채점·첨삭" back="#/solve/photo" toast={toast}
      sub={at === 0 ? "문제를 먼저 찍고, 그다음 내가 쓴 답안을 찍어요. 기준표로 채점하고 어디를 어떻게 고칠지 알려 줘요." : undefined}
      right={p ? <button className="sv-btn sm" onClick={restartAll}>다른 문제</button> : null}>
      <Steps list={["문제 찍기", "답안 찍기", "채점·첨삭"]} at={at} />

      {at === 0 && (
        <>
          <div className="sv-card">
            <Capture mode="problem" region onScan={onProblem} setToast={setToast}
              extra={hasCur ? <button className="sv-btn sm" onClick={() => setP(currentProblem())}>방금 찍은 문제로</button> : null} />
          </div>
          <p className="sv-small" style={{ lineHeight: 1.6 }}>사진은 인식에만 쓰고 서버에 남기지 않아요. 답안 원문은 기본적으로 이 기기에만 남아요.</p>
        </>
      )}

      {at >= 1 && <ProblemCard p={p} thumb={at === 1 ? p.thumb : null} />}

      {at === 1 && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>내 답안</div>
          <Capture mode="answer" region onScan={onAnswer} setToast={setToast} />
        </div>
      )}

      {at === 2 && !res && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>읽어 낸 내 답안 <span className="sv-small">· 잘못 읽은 글자가 있으면 고쳐 주세요</span></div>
          {a.thumb && <img className="ph-thumb" src={a.thumb} alt="" />}
          <textarea className="ph-ta" value={text} onChange={(e) => setText(e.target.value)} disabled={busy} />
          {a.legibility?.issues?.length > 0 && (
            <div className="ph-chips">{a.legibility.issues.map((i, k) => <span key={k} className="ph-chip">{LEG_KIND[i.kind] || i.kind}: {i.note}</span>)}</div>
          )}
          {busy && <div style={{ marginTop: 10 }}><Busy text="기준표를 세우고 채점하는 중… (20초쯤 걸려요)" /></div>}
          {err && !busy && <div className="ph-err" style={{ marginTop: 10 }}>{err}</div>}
          {!busy && (
            <div className="ph-actions" style={{ marginTop: 10 }}>
              <button className="sv-btn pri" onClick={grade}>{err ? "다시 채점받기" : "채점·첨삭 받기"}</button>
              <button className="sv-btn" onClick={restartAnswer}>답안 다시 찍기</button>
            </div>
          )}
        </div>
      )}

      {res && (
        <>
          <EssayResult result={res.result} answer={text} />
          <KeepNote retention={res.retention} />
          <div className="ph-actions" style={{ marginTop: 12 }}>
            <button className="sv-btn pri" onClick={restartAll}>다른 문제 찍기</button>
            <button className="sv-btn" onClick={restartAnswer}>같은 문제, 답안 다시 쓰기</button>
            <button className="sv-btn" onClick={() => { stashCurrent(p); location.hash = "#/solve/photo/read?cur=1"; }}>이 문제 문장 이해하기</button>
            <button className="sv-btn ghost" onClick={() => { location.hash = "#/solve/photo/mine"; }}>내 기록</button>
          </div>
        </>
      )}
    </SolveShell>
  );
}

/** 채점·첨삭 결과 카드들 — 풀이과정 검사 화면도 그대로 쓴다 */
export function EssayResult({ result: r, answer }) {
  if (!r) return null;
  const pct = r.max ? r.total / r.max : 0;
  const color = pct >= 0.9 ? "var(--good)" : pct >= 0.6 ? "var(--text)" : "var(--bad)";
  return (
    <>
      <div className="sv-card">
        <div className="ph-score">
          <div className="big" style={{ color }}>{r.total}<small>/ {r.max}점</small></div>
          <div className="txt">
            <div style={{ fontWeight: 800 }}>{VERDICT[r.verdict] || ""}</div>
            <div className="sv-small">최종 답 {r.final_answer_ok ? <span className="sv-ok">맞음</span> : <span className="sv-bad">확인 필요</span>} · 훈련용 예상 점수예요</div>
          </div>
        </div>
        {r.praise && <div className="ph-praise" style={{ marginTop: 10 }}>👍 {r.praise}</div>}
      </div>

      {answer && (
        <details className="sv-card" style={{ marginBottom: 12 }}>
          <summary className="sv-small" style={{ cursor: "pointer" }}>내가 쓴 답안 보기</summary>
          <MathText as="div" className="ph-ans" text={answer} style={{ marginTop: 8 }} />
        </details>
      )}

      {r.rubric?.length > 0 && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>채점 기준표</div>
          <div className="ph-rub">
            {r.rubric.map((el) => {
              const m = (r.marks || []).find((x) => x.no === el.no) || null;
              return (
                <div key={el.no} className="el">
                  <div className="h"><span className="no">{el.no}</span><span>{el.element}</span>
                    <span className={"pt " + (m?.level || "")}>{m ? `${m.got}` : "–"} / {el.points}점{m ? ` · ${LEVEL[m.level]}` : ""}</span></div>
                  <div className="crit"><MathText text={el.criterion} /></div>
                  {m?.comment && <div className="cm">→ <MathText text={m.comment} /></div>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {r.corrections?.length > 0 && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>첨삭 <span className="sv-small">· 어디를 어떻게</span></div>
          {r.corrections.map((c, i) => (
            <div key={i} className="ph-fix">
              {c.where && <div className="w">{c.where}</div>}
              {c.wrong && <div><span className="wrong"><MathText text={c.wrong} /></span> → <span className="right"><MathText text={c.fix} /></span></div>}
              {!c.wrong && <div className="right"><MathText text={c.fix} /></div>}
              {c.why && <div className="sv-small" style={{ marginTop: 2 }}>{c.why}</div>}
            </div>
          ))}
        </div>
      )}

      {(r.feedback?.length > 0 || r.pitfall_tags?.length > 0) && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>한 줄 첨삭</div>
          {r.feedback?.length > 0 && <ul className="ph-ul">{r.feedback.map((f, i) => <li key={i}><MathText text={f} /></li>)}</ul>}
          {r.pitfall_tags?.length > 0 && <div className="ph-chips">{r.pitfall_tags.map((t, i) => <span key={i} className="ph-chip warn">⚠ {trapText(t)}</span>)}</div>}
        </div>
      )}
    </>
  );
}
