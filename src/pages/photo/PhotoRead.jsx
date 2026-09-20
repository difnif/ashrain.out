// 문장 이해하기 — #/solve/photo/read (촬영) · #/solve/photo/read?cur=1 (방금 찍은 문제로)
// 사진 → 문항 전사 → 규칙 표시(동그라미·밑줄·빗금 "/") + AI 방침(단서 형광펜 · 구하는 것 · 개념 · 첫 줄 · 세울 식)까지만. 정답은 없다.
// 위계: ① 형광펜 친 문장 ② 구하는 것 ③ 식 세우기 — 이 셋을 앞에 크게. 끊어 읽기·단서·조심할 것은 접어 둔다.
import { useEffect, useMemo, useState } from "react";
import SolveShell, { useToast } from "../solve/SolveShell";
import SentenceMarks, { MarkLegend } from "../solve/SentenceMarks";
import MathText from "../../components/MathText";
import { explain, trapText, FUNC_LABEL, markText } from "../../lib/marking.js";
import { photoCall, stashCurrent } from "../../lib/photoApi";
import { newId } from "../../lib/deviceStore";
import { startJob } from "../../lib/photoJobs";
import Capture from "./Capture";
import { ProblemCard, Steps, Busy, ErrorNote, currentProblem, findSpan, cutText, saveDevice, stripMarker, JobBusy, useJobTick } from "./shared";

export default function PhotoRead({ useCur = false }) {
  const [toast, setToast] = useToast();
  const [p, setP] = useState(() => (useCur ? currentProblem() : null));
  const [ap, setAp] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const [tick, setTick] = useState(0);
  const sid = useMemo(() => (p ? newId() : null), [p]);
  const hasCur = !!currentProblem();

  // 문항이 정해지면 방침을 백그라운드 잡으로 받아 온다 — 화면을 떠나도 계속되고 결과는 기록에 저장
  const [job, setJob] = useState(null);
  useJobTick();
  useEffect(() => {
    if (!p?.question) return;
    let alive = true;
    setAp(null); setErr(null); setBusy(true);
    const snap = p;
    const j = startJob({
      kind: "read", title: "문장 이해하기",
      run: async (signal) => {
        const r = await photoCall("approach", { question: snap.question, figure_note: snap.figure_note, choices: snap.choices }, { signal });
        await saveDevice({ id: sid, feature: "read", question: snap.question, figure_note: snap.figure_note, unit: snap.unit_guess, grade: snap.std?.item_grade || null, result: { approach: r }, thumb: snap.thumb || null });
        return r;
      },
    });
    setJob(j);
    j.promise.then(() => {
      if (!alive) return;
      if (j.status === "done") setAp(j.result);
      else if (j.status === "error") setErr(j.error);
      setBusy(false);
    });
    return () => { alive = false; };
  }, [p, tick, sid]);

  const onScan = (r, { thumb }) => {
    const prob = { question: r.question, choices: r.choices, qtype: r.qtype, figure_note: r.figure_note, unit_guess: r.unit_guess, std: r.std, warnings: r.warnings, thumb };
    stashCurrent(prob);
    setP(prob);
  };

  if (!p) {
    return (
      <SolveShell title="문장 이해하기" back="#/solve/photo" toast={toast}
        sub="문제를 찍으면 단서에 형광펜을 치고, 끊어 읽으면서 식을 세우는 데까지만 함께 해요. 답은 직접 구해요.">
        <Steps list={["문제 찍기", "문장 읽기"]} at={0} />
        <div className="sv-card">
          <Capture mode="problem" region onScan={onScan} setToast={setToast}
            extra={hasCur ? <button className="sv-btn sm" onClick={() => setP(currentProblem())}>방금 찍은 문제로</button> : null} />
        </div>
        <p className="sv-small" style={{ lineHeight: 1.6 }}>사진은 인식에만 쓰고 서버에 남기지 않아요.</p>
      </SolveShell>
    );
  }

  return (
    <SolveShell title="문장 이해하기" back="#/solve/photo" toast={toast}
      right={<button className="sv-btn sm" onClick={() => { setP(null); setAp(null); }}>다른 문제</button>}>
      <Steps list={["문제 찍기", "문장 읽기"]} at={1} />
      <ReadBody p={p} ap={ap} busy={busy} err={err} onRetry={() => setTick((t) => t + 1)} onReshoot={() => { setP(null); setAp(null); }}
        jobBusy={busy ? <JobBusy job={job} busyText="단서와 식 세우기 방침을 정리하는 중…" onCanceled={() => { setJob(null); setBusy(false); setErr("판독을 취소했어요"); }} /> : null} />
      <div className="ph-actions">
        <button className="sv-btn pri" onClick={() => { stashCurrent(p); location.hash = "#/solve/photo/mark?cur=1"; }}>이 문장으로 표시 연습</button>
        <button className="sv-btn" onClick={() => { stashCurrent(p); location.hash = "#/solve/photo/essay?cur=1"; }}>답안 찍어 채점받기</button>
        <button className="sv-btn" onClick={() => { setP(null); setAp(null); }}>다른 문제 찍기</button>
        <button className="sv-btn ghost" onClick={() => { location.hash = "#/solve/photo/mine"; }}>내 기록</button>
      </div>
    </SolveShell>
  );
}

/** 접는 보조 카드 — 요약줄만 보이고, 펼치면 내용 */
function More({ ic, title, sub, children, open = false }) {
  return (
    <details className="ph-more" open={open}>
      <summary><span className="ic">{ic}</span><span>{title}</span>{sub && <span className="sub">{sub}</span>}</summary>
      <div className="bd">{children}</div>
    </details>
  );
}

/** 문장 읽기 본문 — 다른 화면(표시 연습 뒤)에서도 그대로 쓴다 */
export function ReadBody({ p, ap, busy, err, onRetry, onReshoot, jobBusy = null }) {
  const [picked, setPicked] = useState(null);
  const ex = useMemo(() => explain(p?.question || "", { labels: { L21_traps: ap?.traps || [] } }), [p, ap]);
  // 단서 형광펜 — AI 가 짚은 단서 문구를 문장 토큰 위에서 찾아 칠한다
  const clueMarks = useMemo(() => {
    const out = [];
    (ap?.clues || []).forEach((c, i) => {
      const sp = findSpan(ex.tokens, c.text);
      if (sp) out.push({ kind: "span", t0: sp.t0, t1: sp.t1, func: "HILITE", tier: 2, required: false, note: `단서 ${i + 1} — ${c.why || ""}` });
    });
    return out;
  }, [ap, ex]);
  const marks = useMemo(() => [...clueMarks, ...ex.marks], [clueMarks, ex]);
  const cut = useMemo(() => cutText(ex.tokens, ex.marks), [ex]);
  const asking = ap?.asking || ex.asking;
  const traps = ap ? (ap.traps || []).map(trapText) : ex.traps;

  return (
    <>
      {/* ① 형광펜 친 문장 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>문제 문장 <span className="sv-small">· 표시를 탭하면 설명이 나와요</span></div>
        <SentenceMarks className="ph-sent" tokens={ex.tokens} marks={marks} onMarkTap={(m) => setPicked(m)} />
        {picked && (
          <div className="ph-step-note">
            <b>{picked.func === "HILITE" ? "형광펜" : FUNC_LABEL[picked.func] || picked.func}</b>
            <span>{stripMarker(markText(picked, ex.tokens)) ? `${stripMarker(markText(picked, ex.tokens))} — ` : ""}{picked.note || "단서예요."}</span>
          </div>
        )}
        {clueMarks.length > 0 && <div className="sv-small" style={{ marginTop: 8 }}><span className="ph-hl">노란 형광펜</span> = 풀이의 열쇠가 되는 단서</div>}
      </div>

      {/* ② 구하는 것 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>구하는 것</div>
        {asking ? <MathText as="div" className="ph-ask" text={asking} /> : <div className="sv-muted">구하는 것을 딱 잘라 찾지 못했어요. 마지막 문장을 다시 읽어 보세요 — 보통 "…를 구하시오" 앞에 있어요.</div>}
      </div>

      {busy && (jobBusy || <Busy text="단서와 식 세우기 방침을 정리하는 중…" />)}
      {err && !busy && <div style={{ marginBottom: 12 }}><ErrorNote text={err} onRetry={onRetry} retryLabel="다시 받기" onShoot={onReshoot} /></div>}

      {/* ③ 식 세우기 — 여기까지만 */}
      {ap && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>여기까지 함께 — 식 세우기</div>
          {ap.concept && <div className="ph-setup"><div className="lb">떠올릴 개념</div><MathText text={ap.concept} /></div>}
          {ap.first_step && <div className="ph-setup"><div className="lb">종이에 쓸 첫 줄</div><MathText text={ap.first_step} /></div>}
          {ap.setup?.length > 0 && (
            <div className="ph-setup"><div className="lb">세울 식</div>
              {ap.setup.map((s, i) => <MathText key={i} as="div" text={s} />)}
            </div>
          )}
          <div className="ph-stop">✋ 여기서부터는 직접! 세운 식을 풀고 답을 구하는 건 네 몫이에요. 다 풀었으면 답안을 찍어 채점받을 수 있어요.</div>
        </div>
      )}

      {/* 보조 — 필요할 때만 펼쳐 본다 */}
      <div className="sv-sec">더 자세히</div>
      <More ic="✂" title="끊어 읽기" sub="빗금(／)에서 한 번 쉬어요">
        <MathText as="div" className="ph-cut" text={cut} />
        {ap?.reading && <div className="sv-small" style={{ marginTop: 8, lineHeight: 1.6 }}>{ap.reading}</div>}
        <div style={{ marginTop: 10 }}><MarkLegend tier2={marks.some((m) => m.func === "EMPH")} /></div>
      </More>

      {ap && (
        <More ic="🔑" title="단서" sub={ap.clues?.length ? `${ap.clues.length}개 · 왜 열쇠인지` : "왜 열쇠인지"}>
          {ap.clues?.length
            ? <ul className="ph-clues">{ap.clues.map((c, i) => <li key={i}><span className="no">{i + 1}</span><span><MathText text={c.text} /><span className="why">{c.why}</span></span></li>)}</ul>
            : <div className="sv-muted">따로 짚을 단서가 없어요 — 문장 전체가 조건이에요.</div>}
        </More>
      )}

      {traps.length > 0 && (
        <More ic="⚠" title="이 문제에서 조심할 것" sub={`${traps.length}가지`}>
          <div className="ph-chips" style={{ marginTop: 0 }}>{traps.map((t, i) => <span key={i} className="ph-chip warn">⚠ {t}</span>)}</div>
        </More>
      )}

      <More ic="📷" title="원문 그대로 보기" sub="찍은 사진">
        <ProblemCard p={p} thumb={p.thumb} title="읽어 낸 문항" />
      </More>
    </>
  );
}
