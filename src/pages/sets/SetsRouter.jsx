// ashrain.out — 공부하기 › 컨셉 문제 (#/sets/*) — 기능 화면(FeatureBar)
//   #/sets/<범주>/<NN>            세트: 바로 풀기 · 자료(문제지 · 해설지 · OMR) 인쇄/다운로드 · OMR 채점 · 문항 목록 · 실제 자료
//   #/sets/<범주>/<NN>/q/<번호>    문항 하나 풀기 → 3단 해설(방침 · 전개 · 확인) + 움직이는 판서·도식
//   #/sets/<범주>/<NN>/omr         OMR 카드 사진 → 판독 → 확인 → 채점
//   #/sets/<범주>/<NN>/paper       종이처럼 풀기 — 문제지를 그대로 펼쳐 손글씨 · 타자 · 체크 → 제출하면 자동 채점
//   #/sets/<범주>/<NN>/video       해설 영상 — 50문항 해설을 교실 모니터처럼 끝없이 돈다(조작 막대 · 전체 화면)
// 목록(범주 · 아이콘)은 공부하기 탭(#/study/sets[/<범주>])에 있다.
import { lazy, Suspense, useMemo, useState } from "react";
import FeatureBar, { FbAct } from "../../components/FeatureBar";
import { pad2, progressSummary, readPaper } from "../../lib/conceptsets";
import { LEVELS } from "./labels";
import { DocsPanel, Toast, useCsUser, useProgress, useSay, useSetData } from "./common";
import { LV_COLOR, safeHtml } from "./render";
import "../solve/solve.css";
import "../../components/item.css";
import "./sets.css";

const ItemSolve = lazy(() => import("./ItemSolve"));
const OmrGrade = lazy(() => import("./OmrGrade"));
const PaperSolve = lazy(() => import("./PaperSolve"));
const SetVideo = lazy(() => import("./SetVideo"));

export function parseSetsHash(hash) {
  const parts = String(hash || "").split("?")[0].replace(/^#\/sets\/?/, "").split("/").filter(Boolean);
  const cat = parts[0] || "prob";
  const no = parseInt(parts[1], 10);
  const view = ["q", "omr", "paper", "video"].includes(parts[2]) ? parts[2] : "home";
  const qno = view === "q" ? parseInt(parts[3], 10) || 1 : null;
  const at = Number((String(hash || "").split("?")[1] || "").match(/(?:^|&)no=(\d+)/)?.[1]) || null;   // ?no=7 — 영상을 그 문항부터
  return { cat, no: Number.isFinite(no) ? no : null, view, qno, at };
}

export default function SetsRouter({ hash, theme }) {
  const r = parseSetsHash(hash);
  if (!r.no) { location.replace("#/study/sets"); return null; }
  return <SetScreen key={`${r.cat}/${r.no}`} r={r} theme={theme} />;
}

function SetScreen({ r, theme }) {
  const { set, cat, files, err } = useSetData(r.cat, r.no);
  const uid = useCsUser();
  const [say, setSay] = useSay();
  const title = set ? `${pad2(set.no)} ${set.short}` : "컨셉 문제";
  const back = r.view === "home" ? `#/study/sets/${r.cat}` : `#/sets/${r.cat}/${pad2(r.no)}`;
  const fall = <div className="cs-wrap sv-muted">불러오는 중…</div>;
  let body;
  if (err) body = <div className="cs-wrap"><div className="sv-empty">세트를 불러오지 못했어요.<br />{err}</div></div>;
  else if (!set) body = fall;
  else if (r.view === "q") body = <Suspense fallback={fall}><ItemSolve catId={r.cat} set={set} qno={r.qno} uid={uid} say={setSay} /></Suspense>;
  else if (r.view === "omr") body = <Suspense fallback={fall}><OmrGrade catId={r.cat} set={set} uid={uid} say={setSay} /></Suspense>;
  else if (r.view === "paper") body = uid === undefined ? fall : <Suspense fallback={fall}><PaperSolve catId={r.cat} set={set} say={setSay} /></Suspense>;
  else if (r.view === "video") return set ? <Suspense fallback={fall}><SetVideo catId={r.cat} set={set} at={r.at} /></Suspense> : fall;
  else body = <SetHome catId={r.cat} set={set} cat={cat} files={files} uid={uid} say={setSay} />;
  const actions = set && (r.view === "q" || r.view === "paper")
    ? <FbAct onClick={() => (location.hash = `#/sets/${r.cat}/${pad2(r.no)}`)}>목록</FbAct>
    : set && r.view === "home" ? <FbAct pri onClick={() => (location.hash = `#/sets/${r.cat}/${pad2(r.no)}/omr`)}>📷 OMR 채점</FbAct> : null;
  return (
    <>
      <FeatureBar theme={theme} title={title} sub={r.view === "q" ? `${r.qno}번` : r.view === "omr" ? "OMR 채점" : r.view === "paper" ? "종이처럼 풀기" : cat?.title || ""} back={back} actions={actions} />
      {body}
      <Toast msg={say} />
    </>
  );
}

// ── 세트 첫 화면 ───────────────────────────────────────────────────────────────
const FILTERS = [["all", "전체"], ...LEVELS.map((l) => [l, l]), ["todo", "안 푼 문제"], ["wrong", "틀린 문제"]];

function SetHome({ catId, set, cat, files, uid, say }) {
  const [prog] = useProgress(catId, set.no, uid);
  const [flt, setFlt] = useState(() => { try { return sessionStorage.getItem("ash.cs.flt") || "all"; } catch { return "all"; } });
  const pickF = (f) => { setFlt(f); try { sessionStorage.setItem("ash.cs.flt", f); } catch { /* 무시 */ } };
  const sum = progressSummary(set, prog);
  const nextNo = useMemo(() => (set.items.find((it) => !prog.items[it.id]) || set.items.find((it) => !prog.items[it.id]?.ok) || set.items[0]).no, [set, prog]);
  const list = set.items.filter((it) => {
    const p = prog.items[it.id];
    if (flt === "all") return true;
    if (flt === "todo") return !p;
    if (flt === "wrong") return p && !p.ok;
    return it.lv === flt;
  });
  const go = (no) => { location.hash = `#/sets/${catId}/${pad2(set.no)}/q/${no}`; };
  const lastOmr = prog.omr?.[0];
  const paper = useMemo(() => (uid === undefined ? { answers: {}, graded: null } : readPaper(catId, set.no)), [catId, set.no, uid]);
  const paperN = Object.keys(paper.answers || {}).length;
  const pct = sum.n ? Math.round((sum.done / sum.n) * 100) : 0;
  return (
    <div className="cs-wrap">
      <div className="cs-hero">
        <span className="ic" aria-hidden="true">{set.icon}</span>
        <div className="tx">
          <h1>{set.title}</h1>
          <div className="sub">{set.sub} · {LEVELS.map((l) => `${l} ${set.items.filter((it) => it.lv === l).length}`).join(" · ")}</div>
          <div className="cs-pbar" aria-label={`푼 문항 ${sum.done}/${sum.n}`}><i style={{ width: `${pct}%` }} /></div>
          <div className="cs-pt">푼 문항 <b>{sum.done}</b>/{sum.n} · 맞힘 <b>{sum.ok}</b>{lastOmr ? ` · 최근 채점 ${lastOmr.score}/${lastOmr.n}` : ""}</div>
        </div>
      </div>
      <button className="sv-btn pri full cs-go" onClick={() => (location.hash = `#/sets/${catId}/${pad2(set.no)}/paper`)}>
        📝 {paper.graded ? `채점한 문제지 보기 · ${paper.graded.score}/${paper.graded.n}` : paperN ? `이어서 풀기 · 문제지 ${paperN}/${set.items.length}칸` : "바로 풀기 · 문제지 그대로"}
      </button>
      <div className="cs-go2">
        <button className="sv-btn" onClick={() => go(nextNo)}>☝ 한 문제씩 풀기{sum.done ? ` · ${nextNo}번` : ""}</button>
        <button className="sv-btn" onClick={() => (location.hash = `#/sets/${catId}/${pad2(set.no)}/video`)}>🎬 해설 영상</button>
      </div>

      <DocsPanel catId={catId} set={set} files={files} say={say} />

      <div className="cs-card cs-omrcard">
        <div className="cs-ch"><b>📷 OMR 채점</b><span>카드에 칠하고 찍으면 바로 채점</span></div>
        <p className="cs-dnote" style={{ marginTop: 0 }}>문제지를 풀고 OMR 카드(2쪽)에 답을 칠한 뒤, 쪽마다 사진을 찍어요. 읽은 답을 확인하고 채점하면 틀린 문항의 해설로 바로 가요.</p>
        <div className="cs-dbtns">
          <button className="sv-btn pri" onClick={() => (location.hash = `#/sets/${catId}/${pad2(set.no)}/omr`)}>📷 OMR 카드 찍어서 채점</button>
        </div>
        {prog.omr?.length > 0 && (
          <div className="cs-omrhist">
            {prog.omr.slice(0, 3).map((h, i) => (
              <span key={i} className="cs-tagx">{new Date(h.at).toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" })} · {h.score}/{h.n}</span>
            ))}
          </div>
        )}
      </div>

      <div className="cs-sec">문항 <small>{list.length}</small></div>
      <div className="cs-chips">
        {FILTERS.map(([f, l]) => (
          <button key={f} className={"cs-chip" + (flt === f ? " on" : "")} onClick={() => pickF(f)}>{l}</button>
        ))}
      </div>
      {list.length === 0 ? <div className="sv-empty">{flt === "wrong" ? "틀린 문제가 없어요 👍" : flt === "todo" ? "모두 풀었어요 🎉" : "문항이 없어요"}</div> : (
        <div className="cs-list">
          {list.map((it) => {
            const p = prog.items[it.id];
            return (
              <button key={it.id} className="cs-row" onClick={() => go(it.no)}>
                <span className="no">{it.no}</span>
                <span className="lv" style={{ background: LV_COLOR[it.lv] }}>{it.lv}</span>
                <span className="tx"><b dangerouslySetInnerHTML={{ __html: safeHtml(it.ty) }} /><small>{it.cat} · {it.sp}</small></span>
                <span className={"st" + (p ? (p.ok ? " ok" : " bad") : "")}>{p ? (p.ok ? "✓" : "✗") : ""}</span>
              </button>
            );
          })}
        </div>
      )}

      {Array.isArray(set.note) && set.note.length > 0 && (
        <div className="cs-notes">{set.note.map((t, i) => <p key={i} dangerouslySetInnerHTML={{ __html: safeHtml(t) }} />)}</div>
      )}
      {Array.isArray(set.facts) && set.facts.length > 0 && (
        <details className="cs-facts">
          <summary>이 주제에 쓴 실제 자료 <small>{set.facts.length}</small></summary>
          {set.facts_intro && <p className="fi" dangerouslySetInnerHTML={{ __html: safeHtml(set.facts_intro) }} />}
          <ol>{set.facts.map(([f, src], i) => <li key={i}><span dangerouslySetInnerHTML={{ __html: safeHtml(f) }} /> <span className="src">— {src}</span></li>)}</ol>
        </details>
      )}
    </div>
  );
}
