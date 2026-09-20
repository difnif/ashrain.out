// 표시 연습하기 — #/solve/photo/mark (촬영) · ?cur=1 (방금 찍은 문제로)
// 사진 → 문항 전사 → 규칙 표시를 "차례대로" 하나씩 보여 준다(동그라미·밑줄·빗금·물결) → 문장 이해하기로 넘어갈지 고른다.
// 직접 표시해 보기(연습·채점)는 기존 MarkView 를 그대로 쓴다. LLM 은 전사에만 쓴다.
import { useEffect, useMemo, useState } from "react";
import SolveShell, { useToast } from "../solve/SolveShell";
import SentenceMarks, { MarkLegend } from "../solve/SentenceMarks";
import { MarkView } from "../solve/Mark";
import { explain, FUNC_LABEL, markText, TIER1 } from "../../lib/marking.js";
import { stashCurrent } from "../../lib/photoApi";
import { newId } from "../../lib/deviceStore";
import Capture from "./Capture";
import { ProblemCard, Steps, currentProblem, saveDevice, stripMarker } from "./shared";

const ORDER = { NUM: 0, SCALE: 1, BOUND: 2, DIST: 3 };
const PLAY_MS = 1600;      // 자동 재생 간격

/** 보여 줄 순서 — 문장 순서대로, 같은 자리면 동그라미→밑줄→빗금. 마지막에 구하는 것(물결). */
function sequence(ex) {
  const list = ex.marks.filter((m) => TIER1.includes(m.func)).slice()
    .sort((a, b) => a.t0 - b.t0 || (ORDER[a.func] ?? 9) - (ORDER[b.func] ?? 9));
  if (ex.askingRange) list.push({ kind: "span", t0: ex.askingRange[0], t1: ex.askingRange[1], func: "DIST", tier: 2, required: false, note: "구하는 것 — 마지막에 이걸 구했는지 꼭 확인해요" });
  return list;
}

export default function PhotoMark({ useCur = false }) {
  const [toast, setToast] = useToast();
  const [p, setP] = useState(() => (useCur ? currentProblem() : null));
  const [k, setK] = useState(0);                 // 보여 준 표시 수
  const [play, setPlay] = useState(false);       // 자동 재생 중인가
  const [mode, setMode] = useState("show");      // show | practice
  const sid = useMemo(() => newId(), [p]);           // 문제마다 새 기록 id
  const hasCur = !!currentProblem();

  const ex = useMemo(() => explain(p?.question || ""), [p]);
  const seq = useMemo(() => sequence(ex), [ex]);
  const shown = seq.slice(0, k);
  const last = k > 0 ? seq[k - 1] : null;
  const done = k >= seq.length;
  const item = useMemo(() => ({ id: "photo:" + sid, question: p?.question || "", figure: null }), [sid, p]);   // MarkView 메모 키

  useEffect(() => { setK(0); setMode("show"); setPlay(false); }, [p]);
  useEffect(() => {
    if (!p?.question) return;
    saveDevice({ id: sid, feature: "mark", question: p.question, figure_note: p.figure_note, unit: p.unit_guess, grade: p.std?.item_grade || null, result: { marks: seq.length }, thumb: p.thumb || null });
  }, [p, sid, seq.length]);

  // 자동 재생 — 마지막 표시까지 가면 스스로 멈춘다
  useEffect(() => {
    if (!play) return;
    if (k >= seq.length) { setPlay(false); return; }
    const t = setTimeout(() => setK((v) => Math.min(seq.length, v + 1)), PLAY_MS);
    return () => clearTimeout(t);
  }, [play, k, seq.length]);

  const onScan = (r, { thumb }) => {
    const prob = { question: r.question, choices: r.choices, qtype: r.qtype, figure_note: r.figure_note, unit_guess: r.unit_guess, std: r.std, warnings: r.warnings, thumb };
    stashCurrent(prob);
    setP(prob);
  };

  if (!p) {
    return (
      <SolveShell title="표시 연습하기" back="#/solve/photo" toast={toast}
        sub="문제를 찍으면 어디에 동그라미·밑줄·물결·빗금을 칠지 차례대로 보여 줘요. 그다음 문장 이해하기로 이어져요.">
        <Steps list={["문제 찍기", "차례대로 보기", "문장 이해하기"]} at={0} />
        <div className="sv-card">
          <Capture mode="problem" region onScan={onScan} setToast={setToast}
            extra={hasCur ? <button className="sv-btn sm" onClick={() => setP(currentProblem())}>방금 찍은 문제로</button> : null} />
        </div>
        <p className="sv-small" style={{ lineHeight: 1.6 }}>사진은 인식에만 쓰고 서버에 남기지 않아요.</p>
      </SolveShell>
    );
  }

  if (mode === "practice") {
    return (
      <SolveShell title="표시 연습하기" back="#/solve/photo" toast={toast}
        right={<button className="sv-btn sm" onClick={() => setMode("show")}>차례대로 다시</button>}>
        <Steps list={["문제 찍기", "차례대로 보기", "문장 이해하기"]} at={1} />
        <MarkView item={item} setToast={setToast} defaultTab="practice" readHref="#/solve/photo/read?cur=1"
          actions={<>
            <button className="sv-btn" onClick={() => { stashCurrent(p); location.hash = "#/solve/photo/read?cur=1"; }}>문장 이해하기로</button>
            <button className="sv-btn" onClick={() => setP(null)}>다른 문제 찍기</button>
          </>} />
      </SolveShell>
    );
  }

  return (
    <SolveShell title="표시 연습하기" back="#/solve/photo" toast={toast}
      right={<button className="sv-btn sm" onClick={() => setP(null)}>다른 문제</button>}>
      <Steps list={["문제 찍기", "차례대로 보기", "문장 이해하기"]} at={1} />
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>이렇게 표시해요 <span className="sv-small">· {seq.length ? `${Math.min(k, seq.length)} / ${seq.length}` : "표시할 것이 없어요"}</span></div>
        <div className="ph-seq" key={"seq" + k}>
          <SentenceMarks className="ph-sent" tokens={ex.tokens} marks={shown} />
        </div>
        {last && (
          <div className="ph-step-note ph-seq" key={"note" + k}>
            <b>{last.func === "DIST" ? "물결" : FUNC_LABEL[last.func] || last.func}</b>
            <span>{stripMarker(markText(last, ex.tokens)) ? `${stripMarker(markText(last, ex.tokens))} — ` : ""}{last.note || "단서예요."}</span>
          </div>
        )}
        {!seq.length && <div className="sv-muted" style={{ marginTop: 8 }}>이 문장은 짧아서 규칙으로 잡히는 표시가 없어요. 문장 이해하기로 바로 넘어가도 좋아요.</div>}
        {seq.length > 0 && (
          <>
            <div className="ph-step-bar">
              <button className="sv-btn" onClick={() => { setPlay(false); setK((v) => Math.max(0, v - 1)); }} disabled={k === 0}>◀ 이전</button>
              <span className="cnt">{Math.min(k, seq.length)}/{seq.length}</span>
              {!done
                ? <button className="sv-btn pri" onClick={() => { setPlay(false); setK((v) => Math.min(seq.length, v + 1)); }}>{k === 0 ? "첫 표시 보기" : "다음 ▶"}</button>
                : <button className="sv-btn" onClick={() => { setPlay(false); setK(0); }}>처음부터</button>}
            </div>
            <div className="sv-row wrap" style={{ gap: 6, marginTop: 8 }}>
              <button className={"sv-chip" + (play ? " on" : "")} aria-pressed={play}
                onClick={() => { if (done) { setK(0); setPlay(true); } else setPlay((v) => !v); }}>
                {play ? "⏸ 일시정지" : done ? "▶ 처음부터 재생" : "▶ 자동 재생"}
              </button>
              <span className="sv-small">1.6초마다 표시가 하나씩 생겨요</span>
              <span className="sv-sp" style={{ flex: 1 }} />
              {!done && <button className="sv-btn sm ghost" onClick={() => { setPlay(false); setK(seq.length); }}>한 번에 보기</button>}
            </div>
          </>
        )}
      </div>

      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>표시 읽는 법</div>
        <MarkLegend />
        <div className="sm-wrap sm-legend ph-sent" style={{ padding: 0, marginTop: 4 }}><span><span className="sm-t sm-dist">구하는 것</span> 물결 = 마지막에 확인할 것</span></div>
      </div>

      <details className="ph-more">
        <summary><span className="ic">📷</span><span>원문 그대로 보기</span><span className="sub">찍은 사진</span></summary>
        <div className="bd"><ProblemCard p={p} thumb={p.thumb} title="읽어 낸 문항" /></div>
      </details>

      {(done || !seq.length) && (
        <div className="sv-card" style={{ marginTop: 12, borderColor: "color-mix(in srgb, var(--accent) 45%, var(--border))" }}>
          <div style={{ fontWeight: 800, fontSize: 15.5, marginBottom: 10 }}>문장 이해하기로 넘어갈까요?</div>
          <div className="sv-small" style={{ marginBottom: 10, lineHeight: 1.6 }}>단서에 형광펜을 치고, 무엇을 구하는지·어떤 식을 세울지까지 함께 읽어요.</div>
          <div className="ph-actions">
            <button className="sv-btn pri" onClick={() => { stashCurrent(p); location.hash = "#/solve/photo/read?cur=1"; }}>네, 문장 이해하기로</button>
            {seq.length > 0 && <button className="sv-btn" onClick={() => setMode("practice")}>아니요, 직접 표시해 볼래요</button>}
            <button className="sv-btn ghost wide" onClick={() => setP(null)}>다른 문제 찍기</button>
          </div>
        </div>
      )}
    </SolveShell>
  );
}
