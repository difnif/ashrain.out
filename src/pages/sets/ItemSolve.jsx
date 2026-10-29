// ashrain.out — 컨셉 문제: 문항 하나 풀기 → 채점 → 3단 해설(방침 · 전개 · 확인) + 움직이는 판서 · 도식
// 맞히면 해설이 바로 열리고, 틀리면 「다시 풀기」와 「해설 보기」 중에 고른다(정답은 해설을 열 때 보인다).
import { useEffect, useMemo, useRef, useState } from "react";
import { judge, saveAttempt, pad2 } from "../../lib/conceptsets";
import { AnswerInput, ensureSerif, useAnim, useProgress } from "./common";
import { headHtml, questionHtml, solutionHtml, answerHtml } from "./render";
import { kindLabel } from "./labels";

export default function ItemSolve({ catId, set, qno, uid, say }) {
  const it = set.items.find((x) => x.no === qno) || set.items[0];
  return <ItemSolveInner key={it.id} catId={catId} set={set} it={it} uid={uid} say={say} />;
}

function ItemSolveInner({ catId, set, it, uid, say }) {
  const [prog, refresh] = useProgress(catId, set.no, uid);
  const prev = prog.items[it.id] || null;
  const [raw, setRaw] = useState("");
  const [res, setRes] = useState(null);           // { ok, note, raw }
  const [open, setOpen] = useState(false);        // 해설 열림
  const [shake, setShake] = useState(false);
  const solRef = useRef(null);
  useEffect(() => { ensureSerif(); window.scrollTo?.(0, 0); }, []);
  useAnim(solRef, [open, it.id]);

  const qHtml = useMemo(() => questionHtml(it), [it]);
  const sHtml = useMemo(() => (open ? solutionHtml(it) : ""), [open, it]);
  const idx = set.items.findIndex((x) => x.id === it.id);
  const prevIt = set.items[idx - 1], nextIt = set.items[idx + 1];
  const goNo = (no) => { location.hash = `#/sets/${catId}/${pad2(set.no)}/q/${no}`; };

  const submit = () => {
    if (res) return;
    const r = judge(it, raw);
    if (r.ok === null) {
      say(r.note || "답을 써 주세요");
      setShake(true); setTimeout(() => setShake(false), 450);
      return;
    }
    if (r.ok === false && r.note) {                       // 꼴이 틀림(예: 분모 0) — 시도로 치지 않는다
      say(r.note); setShake(true); setTimeout(() => setShake(false), 450);
      return;
    }
    saveAttempt(catId, set.no, it.id, raw, r.ok);
    refresh();
    setRes({ ...r, raw });
    if (r.ok) setOpen(true);
  };
  const retry = () => { setRes(null); setRaw(""); setOpen(false); };
  const reveal = () => setOpen(true);

  useEffect(() => {
    if (open && solRef.current) setTimeout(() => solRef.current?.scrollIntoView?.({ behavior: "smooth", block: "start" }), 60);
  }, [open]);

  const state = res ? (res.ok ? "ok" : "bad") : shake ? "shake" : "";
  return (
    <div className="cs-wrap">
      <div className="cs-q">
        <div className="cs-qh" dangerouslySetInnerHTML={{ __html: headHtml(it) }} />
        <div className="cs-qb" dangerouslySetInnerHTML={{ __html: qHtml }} />
      </div>

      <div className="cs-card cs-ansbox">
        <div className="cs-ahint">{kindLabel(it)}</div>
        <div className="cs-arow">
          <AnswerInput item={it} value={res ? res.raw : raw} onChange={setRaw} onSubmit={submit} disabled={!!res} state={state} />
          {!res && <button className="sv-btn pri cs-sub" onClick={submit}>채점</button>}
        </div>
        {prev && !res && (
          <div className="cs-prev">지난 기록 · 내 답 <b>{prev.raw || "—"}</b> {prev.ok ? <span className="sv-ok">정답</span> : <span className="sv-bad">오답</span>}{prev.n > 1 ? ` · ${prev.n}번 풀었어요` : ""}</div>
        )}
        {res && (
          <div className={"cs-verdict iv-banner " + (res.ok ? "ok" : "bad")}>
            <div className="iv-verdict">{res.ok ? "정답! 🎉" : "아쉬워요"}</div>
            {res.note && <div className="cs-note">{res.note}</div>}
            {(res.ok || open) && <div className="iv-ans"><span className="iv-lab">정답</span><span dangerouslySetInnerHTML={{ __html: answerHtml(it) }} /></div>}
            {!res.ok && <div className="iv-mine"><span className="iv-lab">내 답</span>{res.raw}</div>}
            {!res.ok && !open && (
              <div className="iv-row">
                <button className="sv-btn sm" onClick={retry}>↺ 다시 풀기</button>
                <button className="sv-btn sm pri" onClick={reveal}>해설 보기</button>
              </div>
            )}
          </div>
        )}
        {!res && !open && <button className="sv-btn ghost sm cs-giveup" onClick={reveal}>모르겠어요 · 해설 먼저 보기</button>}
        {!res && open && <div className="iv-ans cs-ansline"><span className="iv-lab">정답</span><span dangerouslySetInnerHTML={{ __html: answerHtml(it) }} /></div>}
      </div>

      {open && <div ref={solRef} className="cs-solwrap" dangerouslySetInnerHTML={{ __html: sHtml }} />}
      {open && <button className="sv-btn full cs-vlink" onClick={() => (location.hash = `#/sets/${catId}/${pad2(set.no)}/video?no=${it.no}`)}>🎬 이 문제 해설 영상으로 보기</button>}
      {open && res && !res.ok && <button className="sv-btn full cs-retry" onClick={retry}>↺ 다시 풀어 보기</button>}

      <div className="cs-nav">
        <button className="sv-btn" disabled={!prevIt} onClick={() => prevIt && goNo(prevIt.no)}>← {prevIt ? `${prevIt.no}번` : "처음"}</button>
        <button className={"sv-btn" + (res || open ? " pri" : "")} disabled={!nextIt} onClick={() => nextIt && goNo(nextIt.no)}>{nextIt ? `${nextIt.no}번 →` : "마지막 문제"}</button>
      </div>
    </div>
  );
}
