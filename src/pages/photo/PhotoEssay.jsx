// 서술형 채점·첨삭 — #/solve/photo/essay (촬영) · ?cur=1 (방금 찍은 문제로)
// 문제 촬영 → 문항 부분 인식 → 답안 촬영 → 답안 부분 인식(전사, 고칠 수 있음) → 채점 기준표·채점·첨삭.
// 답안 원문은 보관 게이트 결정(retention.where)에 따라 기기 또는 서버에 남고, 결과는 항상 기기 보관소에 남는다.
// 결과 카드는 서술형 자가채점(#/solve/essay)과 같은 시각 톤 — 큰 점수 + 막대 + 기준표 + 첨삭.
import { useEffect, useState } from "react";
import SolveShell, { useToast } from "../solve/SolveShell";
import MathText from "../../components/MathText";
import { trapText } from "../../lib/marking.js";
import { photoCall, stashCurrent } from "../../lib/photoApi";
import { newId } from "../../lib/deviceStore";
import { startJob } from "../../lib/photoJobs";
import { hwGuideDue, hwIssuesOf, addHwStrike, HW_ADVICE } from "../../lib/hw";
import Capture from "./Capture";
import { HwGuide, HwMarks } from "./HwGuide";
import { ProblemCard, Steps, KeepNote, ErrorNote, currentProblem, saveDevice, JobBusy, useJobTick } from "./shared";

const VERDICT = { excellent: "아주 잘 썼어요", good: "잘 썼어요", partial: "절반쯤 왔어요", weak: "다시 써 봐요" };
const LEVEL = { full: "만점", partial: "부분", zero: "0점" };
const LEG_KIND = { size: "글씨 크기", messy: "난잡함", glyph: "헷갈리는 글자", spacing: "간격·정렬", crossout: "지운 흔적", other: "기타" };

export default function PhotoEssay({ useCur = false }) {
  const [toast, setToast] = useToast();
  const [p, setP] = useState(() => (useCur ? currentProblem() : null));
  const [a, setA] = useState(null);          // 답안 전사
  const [text, setText] = useState("");      // 학생이 고친 답안
  const [res, setRes] = useState(null);      // { result, std, retention }
  const [job, setJob] = useState(null);      // 채점 백그라운드 잡
  const [err, setErr] = useState(null);
  const [guide, setGuide] = useState(false); // 촬영 전 필기 주의 팝업
  useJobTick();
  const hasCur = !!currentProblem();
  const at = !p ? 0 : !a ? 1 : 2;
  const busy = job?.status === "running";

  // 답안 촬영 단계에 들어설 때 필기 약속 팝업 (기본 노출 · 한 달 숨김 · 5회 누적 시 재노출)
  useEffect(() => { if (at === 1 && hwGuideDue()) setGuide(true); }, [at]);

  const onProblem = (r, { thumb }) => {
    const prob = { question: r.question, choices: r.choices, qtype: r.qtype, figure_note: r.figure_note, unit_guess: r.unit_guess, std: r.std, warnings: r.warnings, thumb };
    stashCurrent(prob); setP(prob);
  };
  const onAnswer = (r, { thumb }) => {
    if (hwIssuesOf(r).length) addHwStrike();           // 학생 책임 필기 문제 누적(이 기기)
    setA({ ...r, thumb }); setText(r.answer || ""); setRes(null); setErr(null);
  };

  const grade = () => {
    const answer = text.trim();
    if (!answer) { setToast("답안이 비어 있어요"); return; }
    setErr(null);
    const meta = { p, thumb: a?.thumb || p.thumb || null, raw: a?.answer || "" };
    // 백그라운드 잡 — 화면을 떠나도 채점은 계속되고, 결과는 잡 안에서 기기 보관소에 저장된다
    const j = startJob({
      kind: "essay", title: "서술형 채점·첨삭",
      run: async (signal) => {
        const r = await photoCall("essay", { question: meta.p.question, figure_note: meta.p.figure_note, choices: meta.p.choices, answer, std: meta.p.std, unit: meta.p.unit_guess }, { signal });
        await saveDevice({ id: newId(), feature: "essay", question: meta.p.question, figure_note: meta.p.figure_note, unit: meta.p.unit_guess,
          grade: r.std?.item_grade || meta.p.std?.item_grade || null, answer,
          answer_raw: meta.raw && meta.raw !== answer ? meta.raw : undefined,   // 전사 원문(학생이 고쳤을 때만) — 오독 패턴 개선용, 기기에만
          result: r.result, retention: r.retention, thumb: meta.thumb });
        return r;
      },
    });
    setJob(j);
    j.promise.then(() => {
      if (j.status === "done") setRes(j.result);
      else if (j.status === "error") setErr(j.error);
      // canceled 는 JobBusy 의 onCanceled 가 그 자리에서 처리(잡 정산을 기다리지 않는다)
    });
  };

  const restartAnswer = () => { setA(null); setText(""); setRes(null); setErr(null); setJob(null); };
  const restartAll = () => { setP(null); restartAnswer(); };

  return (
    <SolveShell title="서술형 채점·첨삭" back="#/solve/photo" toast={toast}
      sub={at === 0 ? "문제를 먼저 찍고, 그다음 내가 쓴 답안을 찍어요. 기준표로 채점하고 어디를 어떻게 고칠지 알려 줘요." : undefined}
      right={p ? <button className="sv-btn sm" onClick={restartAll}>다른 문제</button> : null}>
      {guide && <HwGuide onClose={() => setGuide(false)} />}
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
          {hwIssuesOf(a).length > 0
            ? <HwMarks thumb={a.thumb} issues={a.legibility?.issues || []} />
            : a.thumb && <img className="ph-thumb" src={a.thumb} alt="" />}
          <textarea className="ph-ta" value={text} onChange={(e) => setText(e.target.value)} disabled={busy} />
          {(a.legibility?.issues || []).filter((i) => !HW_ADVICE[i.kind]).length > 0 && (
            <div className="ph-chips">{a.legibility.issues.filter((i) => !HW_ADVICE[i.kind]).map((i, k) => <span key={k} className="ph-chip">{LEG_KIND[i.kind] || i.kind}: {i.note}</span>)}</div>
          )}
          {busy && <div style={{ marginTop: 10 }}><JobBusy job={job} busyText="기준표를 세우고 채점하는 중… (20~40초쯤 걸려요)" onCanceled={() => { setJob(null); setErr("판독을 취소했어요"); }} /></div>}
          {err && !busy && <div style={{ marginTop: 10 }}><ErrorNote text={err} onRetry={grade} retryLabel="다시 채점받기" onShoot={restartAnswer} shootLabel="답안 다시 찍기" /></div>}
          {!busy && !err && (
            <div className="ph-actions" style={{ marginTop: 10 }}>
              <button className="sv-btn pri" onClick={grade}>채점·첨삭 받기</button>
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

/** 채점·첨삭 결과 카드들 — 풀이과정 검사 화면·내 기록도 그대로 쓴다 */
export function EssayResult({ result: r, answer }) {
  if (!r) return null;
  const pct = r.max ? Math.round((r.total / r.max) * 100) : 0;
  const color = pct >= 90 ? "var(--ph-ok-ink)" : pct >= 60 ? "var(--text)" : "var(--bad)";
  return (
    <>
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>채점 결과</div>
        <div className="ph-verdict">{VERDICT[r.verdict] || "채점했어요"}</div>
        <div className="ph-total">
          <span className="big" style={{ color }}>{r.total}</span><span className="of">/ {r.max}점</span>
          <span className="vd" style={{ color: r.final_answer_ok ? "var(--ph-ok-ink)" : "var(--bad)" }}>{r.final_answer_ok ? "답 맞음" : "답 확인 필요"}</span>
        </div>
        <div className="sv-bar"><i style={{ width: `${pct}%` }} /></div>
        <div className="ph-hint">훈련용 예상 점수예요. 실제 시험의 채점과는 다를 수 있어요.</div>
        {r.praise && <div className="ph-praise" style={{ marginTop: 10 }}>👍 {r.praise}</div>}
      </div>

      {answer && (
        <details className="ph-more">
          <summary><span className="ic">📄</span><span>내가 쓴 답안 보기</span></summary>
          <div className="bd"><MathText as="div" className="ph-ans" text={answer} /></div>
        </details>
      )}

      {r.rubric?.length > 0 && (
        <div className="sv-card" style={{ marginTop: 12 }}>
          <div className="sv-sec" style={{ marginTop: 0 }}>채점 기준표</div>
          <div className="ph-rub">
            {r.rubric.map((el) => {
              const m = (r.marks || []).find((x) => x.no === el.no) || null;
              return (
                <div key={el.no} className="el">
                  <div className="h"><span className="no">{el.no}</span><span>{el.element}</span>
                    <span className={"pt " + (m?.level || "")}>{m ? `${m.got}` : "–"} / {el.points}점{m ? ` · ${LEVEL[m.level]}` : ""}</span></div>
                  <div className="crit"><MathText text={el.criterion} /></div>
                  {m?.comment && <div className="cm"><b>한마디</b><MathText text={m.comment} /></div>}
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
              {c.why && <div className="sv-small" style={{ marginTop: 3 }}>{c.why}</div>}
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
