// ashrain.out — 학교별 모의고사 「한 문제씩」(#/mock/<id>/q/<i>)
// 시험지에서 그 문항 칸만 잘라 크게 보여 주고 바로 채점한다.
//   · 선택형: 잘라 본 문항의 보기 번호를 누르거나 아래 ①~⑤ → 「채점」. 맞히면 정답 · 단원 · 🎬 시청각 해설, 틀리면 「다시 풀기」 또는 「정답 보기」.
//   · 서답형: 하위 문항마다 손글씨 · 타자로 쓰고 → 「모범 답 보고 채점」에서 채점 요소에 체크(스스로 채점).
// 기록은 이 기기 · 계정에(시험지 풀기와 따로) — 시험 화면 문항 목록의 ✓ · ✗.
import { useEffect, useState } from "react";
import { readMockRecord, saveMockAttempt, judgeMc, toggleChoice, isAnswered, choiceText } from "../../lib/mockexams";
import { ItemCrop, ChoicePad, SaWriter, SaMine, SaGrader, AvButtons, Rich } from "./parts";

export default function MockItem({ exam, i, uid }) {
  const it = exam.items.find((x) => x.i === i) || exam.items[0];
  return <MockItemInner key={it.i} exam={exam} it={it} uid={uid} />;
}

function MockItemInner({ exam, it, uid }) {
  const [rec, setRec] = useState(() => (uid === undefined ? { items: {} } : readMockRecord(exam.id)));
  useEffect(() => { if (uid !== undefined) setRec(readMockRecord(exam.id)); }, [uid, exam.id]);
  const prev = rec.items[it.i] || null;
  const [ans, setAns] = useState(null);           // 선택형 {k:"mc", sel} · 서답형 {k:"sa", parts}
  const [res, setRes] = useState(null);           // 선택형 "ok" | "wrong"
  const [open, setOpen] = useState(false);        // 정답 · 해설 열림
  const [grade, setGrade] = useState(null);       // 서답형 { got, checks }
  useEffect(() => { window.scrollTo?.(0, 0); }, []);
  const k = exam.items.findIndex((x) => x.i === it.i);
  const prevIt = exam.items[k - 1], nextIt = exam.items[k + 1];
  const go = (x) => { location.hash = `#/mock/${exam.id}/q/${x.i}`; };
  const from = `#/mock/${exam.id}/q/${it.i}`;
  const sel = ans?.k === "mc" ? ans.sel || [] : [];
  const lbl = (x) => (x.kind === "mc" ? `${x.label}번` : x.label);

  const check = () => {
    if (!sel.length) return;
    const r = judgeMc(it, ans);
    setRes(r);
    setRec(saveMockAttempt(exam.id, it.i, { sel, ok: r === "ok" }));
    if (r === "ok") setOpen(true);
  };
  const retry = () => { setAns(null); setRes(null); setOpen(false); };
  const saveGrade = (gr) => {
    setGrade(gr);
    setRec(saveMockAttempt(exam.id, it.i, { got: gr.got, ok: gr.got >= it.pts }));
  };
  const mark = res && it.kind === "mc" && (open || res === "ok") ? { ok: it.ans, bad: sel.filter((c) => !it.ans.includes(c)) } : null;

  return (
    <div className="cs-wrap mx-item">
      <div className="mx-ih">
        <span className="mx-ino">{it.kind === "mc" ? it.label : "서답"}</span>
        <div className="tx"><b>{lbl(it)} · {it.pts}점{it.multi ? ` · 정답 ${it.ans.length}개` : ""}</b><small><Rich text={it.unit} /></small></div>
        {prev && !res && !grade && (
          <span className={"mx-prev " + (prev.ok ? "ok" : "bad")}>{prev.ok ? "✓ 맞힌 문제" : "✗ 틀렸던 문제"}{prev.n > 1 ? ` · ${prev.n}번` : ""}</span>
        )}
      </div>
      <div className="mx-icrop"><ItemCrop exam={exam} it={it} sel={sel} mark={mark} onPick={it.kind === "mc" && !res ? (c) => setAns((p) => toggleChoice(p, c, it.multi)) : undefined} /></div>

      {it.kind === "mc" ? (
        <div className="cs-card cs-ansbox">
          <ChoicePad it={it} sel={sel} disabled={!!res} mark={mark} onPick={(c) => setAns((p) => toggleChoice(p, c, it.multi))} />
          {!res && <button type="button" className="sv-btn pri full mx-chk" disabled={!sel.length} onClick={check}>채점</button>}
          {res && (
            <div className={"cs-verdict iv-banner " + (res === "ok" ? "ok" : "bad")}>
              <div className="iv-verdict">{res === "ok" ? "정답! 🎉" : "아쉬워요"}</div>
              {(res === "ok" || open) && <div className="iv-ans"><span className="iv-lab">정답</span>{choiceText(it.ans)}</div>}
              {res !== "ok" && <div className="iv-mine"><span className="iv-lab">내 답</span>{choiceText(sel)}</div>}
              {res !== "ok" && !open && (
                <div className="iv-row">
                  <button type="button" className="sv-btn sm" onClick={retry}>↺ 다시 풀기</button>
                  <button type="button" className="sv-btn sm pri" onClick={() => setOpen(true)}>정답 보기</button>
                </div>
              )}
            </div>
          )}
          {!res && !open && <button type="button" className="sv-btn ghost sm cs-giveup" onClick={() => setOpen(true)}>모르겠어요 · 정답과 시청각 해설 먼저 보기</button>}
          {!res && open && <div className="iv-ans cs-ansline"><span className="iv-lab">정답</span>{choiceText(it.ans)}</div>}
        </div>
      ) : (
        <div className="cs-card">
          {!open ? (
            <>
              <SaWriter it={it} value={ans} onChange={setAns} />
              <button type="button" className="sv-btn pri full mx-chk" onClick={() => setOpen(true)}>{isAnswered(it, ans) ? "모범 답 보고 채점" : "모범 답 먼저 보기"}</button>
            </>
          ) : (
            <>
              <div className="mx-h">내 답</div>
              <SaMine it={it} value={ans} />
              <div className="mx-h">모범 답과 채점 요소</div>
              <SaGrader it={it} grade={grade} onGrade={saveGrade} />
              <button type="button" className="sv-btn sm" onClick={() => setOpen(false)}>✍ 답 다시 보기 · 고치기</button>
            </>
          )}
        </div>
      )}

      {(open || res === "ok") && <AvButtons it={it} from={from} />}
      {open && res && res !== "ok" && <button type="button" className="sv-btn full cs-retry" onClick={retry}>↺ 다시 풀어 보기</button>}

      <div className="cs-nav">
        <button type="button" className="sv-btn" disabled={!prevIt} onClick={() => prevIt && go(prevIt)}>← {prevIt ? lbl(prevIt) : "처음"}</button>
        <button type="button" className={"sv-btn" + (res || open ? " pri" : "")} disabled={!nextIt} onClick={() => nextIt && go(nextIt)}>{nextIt ? `${lbl(nextIt)} →` : "마지막 문제"}</button>
      </div>
    </div>
  );
}
