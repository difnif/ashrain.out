// 내 기록 — #/solve/photo/mine  (이 기기의 IndexedDB 에 남은 촬영 학습 기록. 서버에는 라벨만 있으므로 여기서만 원문을 볼 수 있다)
// 지우기는 창이 뜨는 confirm() 대신 그 자리에서 한 번 더 묻는 2단계 확인.
import { useEffect, useState } from "react";
import SolveShell, { useToast } from "../solve/SolveShell";
import MathText from "../../components/MathText";
import { listSessions, getSession, deleteSession, clearSessions } from "../../lib/deviceStore";
import { EssayResult } from "./PhotoEssay";
import { ProblemCard, Lights, KeepNote, EmptyArt, FEATURE_LABEL, FEATURE_ICON, fmtWhen, GRADE_LABEL } from "./shared";

const FILTERS = [["", "전체"], ["essay", "서술형"], ["check", "풀이검사"], ["read", "문장 이해"], ["mark", "표시 연습"]];

export default function PhotoMine() {
  const [toast, setToast] = useToast();
  const [feature, setFeature] = useState("");
  const [rows, setRows] = useState(null);
  const [open, setOpen] = useState(null);      // 상세 레코드
  const [sure, setSure] = useState(null);      // 'one:<id>' | 'all' — 한 번 더 묻는 중

  const load = async () => { try { setRows(await listSessions({ feature: feature || undefined, limit: 100 })); } catch { setRows([]); } };
  useEffect(() => { setRows(null); setSure(null); load(); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, [feature]);

  const remove = async (id) => { try { await deleteSession(id); setToast("지웠어요"); } catch { setToast("지우지 못했어요"); } setSure(null); setOpen(null); load(); };
  const clearAll = async () => { try { await clearSessions(); setToast("모두 지웠어요"); } catch { setToast("지우지 못했어요"); } setSure(null); setOpen(null); load(); };

  if (open) {
    const r = open;
    return (
      <SolveShell title={FEATURE_LABEL[r.feature] || "기록"} back={null} toast={toast}
        right={<button className="sv-btn sm" onClick={() => { setSure(null); setOpen(null); }}>목록</button>}>
        <div className="sv-small" style={{ marginBottom: 8 }}>{fmtWhen(r.at)}{r.grade ? ` · 문항 표현 ${GRADE_LABEL[r.grade] || r.grade}` : ""}</div>
        <ProblemCard p={{ question: r.question, figure_note: r.figure_note, unit_guess: r.unit }} thumb={r.thumb} showGrade={false} />
        {r.answer && (
          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>내 답안</div>
            <MathText as="div" className="ph-ans" text={r.answer} />
          </div>
        )}
        {r.feature === "essay" && <EssayResult result={r.result} />}
        {r.feature === "check" && r.result && (
          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>신호등</div>
            <Lights criteria={r.result.criteria} />
            {r.result.summary && <div style={{ marginTop: 10, fontSize: 14, lineHeight: 1.65 }}><MathText text={r.result.summary} /></div>}
          </div>
        )}
        {r.feature === "read" && r.result?.approach && (
          <div className="sv-card">
            <div className="sv-sec" style={{ marginTop: 0 }}>구하는 것 · 세울 식</div>
            {r.result.approach.asking && <MathText as="div" className="ph-ask" text={r.result.approach.asking} />}
            {r.result.approach.setup?.length > 0 && <div className="ph-setup" style={{ marginTop: 8 }}>{r.result.approach.setup.map((s, i) => <MathText key={i} as="div" text={s} />)}</div>}
          </div>
        )}
        <KeepNote retention={r.retention} />
        {sure === "one:" + r.id ? (
          <div className="ph-sure" style={{ marginTop: 12 }}>
            <span className="tx">이 기록을 지울까요? 되돌릴 수 없어요.</span>
            <button className="sv-btn sm" onClick={() => setSure(null)}>아니요</button>
            <button className="sv-btn sm pri" onClick={() => remove(r.id)}>네, 지울게요</button>
          </div>
        ) : (
          <div className="ph-actions" style={{ marginTop: 12 }}>
            <button className="sv-btn" onClick={() => setOpen(null)}>목록으로</button>
            <button className="sv-btn ghost" style={{ color: "var(--bad)" }} onClick={() => setSure("one:" + r.id)}>이 기록 지우기</button>
          </div>
        )}
      </SolveShell>
    );
  }

  return (
    <SolveShell title="내 기록" back="#/solve/photo" toast={toast} sub="촬영 학습 기록은 이 기기에만 남아요. 기기를 바꾸거나 브라우저 데이터를 지우면 사라져요.">
      <div className="sv-row wrap" style={{ gap: 6, marginBottom: 12 }}>
        {FILTERS.map(([k, l]) => <button key={k} className={"sv-chip" + (feature === k ? " on" : "")} onClick={() => setFeature(k)}>{l}</button>)}
      </div>
      {rows === null && <div className="sv-muted">불러오는 중…</div>}
      {rows && !rows.length && (
        <div className="ph-blank">
          <EmptyArt kind="box" />
          <div className="tt">{feature ? "이 갈래의 기록이 아직 없어요" : "아직 기록이 없어요"}</div>
          <div className="ds">
            문제를 찍어 문장을 읽거나 답안을 채점받으면 여기에 쌓여요.<br />
            답안 원문과 첨삭 결과는 이 기기에만 남아요.
          </div>
          <div className="ph-actions">
            <button className="sv-btn pri" onClick={() => { location.hash = "#/solve/photo/read"; }}>문제 찍으러 가기</button>
            <button className="sv-btn" onClick={() => { location.hash = "#/solve/photo"; }}>촬영 모듈 홈으로</button>
          </div>
        </div>
      )}
      {rows && rows.length > 0 && (
        <div className="sv-list">
          {rows.map((r) => (
            <button key={r.id} className="ph-rec" onClick={async () => { let full = null; try { full = await getSession(r.id); } catch { /* 목록 행으로 대신 */ } setSure(null); setOpen(full || r); }}>
              {r.thumb
                ? <img className="th" src={r.thumb} alt="" />
                : <span className="ic" aria-hidden="true">{FEATURE_ICON[r.feature] || "📄"}</span>}
              <span className="tx"><div className="tt">{r.title || "(제목 없음)"}</div><div className="dt">{FEATURE_LABEL[r.feature] || r.feature} · {fmtWhen(r.at)}</div></span>
              <span className="rt">{r.feature === "essay" && r.result ? `${r.result.total}/${r.result.max}` : r.feature === "check" && r.result ? (r.result.final_answer_ok ? "✓" : "✗") : ""}</span>
            </button>
          ))}
        </div>
      )}
      {rows && rows.length > 0 && (
        sure === "all" ? (
          <div className="ph-sure" style={{ marginTop: 12 }}>
            <span className="tx">이 기기의 촬영 학습 기록을 모두 지울까요? 되돌릴 수 없어요.</span>
            <button className="sv-btn sm" onClick={() => setSure(null)}>아니요</button>
            <button className="sv-btn sm pri" onClick={clearAll}>네, 모두 지울게요</button>
          </div>
        ) : (
          <div style={{ textAlign: "right", marginTop: 12 }}><button className="sv-btn sm ghost" onClick={() => setSure("all")}>모두 지우기</button></div>
        )
      )}
    </SolveShell>
  );
}
