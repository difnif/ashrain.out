// ashrain.out — 공부하기 › 시험 보기 › 학교별 모의고사 › 시험 하나 (#/mock/<id>/*) — 기능 화면(FeatureBar)
//   #/mock/<id>                 시험: 바로 풀기(시험지 그대로) · 강사 모드 · 한 문제씩 · 정답과 채점 기준 · 시청각 해설 · 자료(보기 · 받기 · 인쇄) · 문항 목록
//   #/mock/<id>/paper           시험지 그대로 풀기 — 보기 누르기 · OMR · 서답형 손글씨 · 시간 · 제출하면 채점(MockPaper.jsx)
//   #/mock/<id>/board           같은 화면을 강사 모드로(관리자) — 컨셉 문제와 같은 필기 창(PaperBoard)
//   #/mock/<id>/q/<i>           한 문제씩 — 시험지에서 그 문항만 잘라 크게(MockItem.jsx)
//   #/mock/<id>/key             정답과 채점 기준(MockDocs.jsx)
//   #/mock/<id>/doc/<자료>       자료 보기 — 문제지 · 빠른 정답지 · 해설지 …(MockDocs.jsx)
//   #/mock/<id>/av              이 시험의 시청각 해설 — 단원 · 유형별 해설로(돌아오면 이 시험으로)
// 목록(학교 검색 → 판 → 회차)은 공부하기 탭(#/study/exam/school/…) — pages/mock/SchoolExams.jsx.
import { lazy, Suspense, useEffect, useMemo, useState } from "react";
import FeatureBar, { FbAct } from "../../components/FeatureBar";
import { readMockPaper, readMockRecord, gradeMock, isAnswered, edInfo, fmtBytes, choiceText } from "../../lib/mockexams";
import { useMockExam, useMockUser, useIsAdmin, AvList, Rich, ensureMockFonts } from "./parts";
import "../solve/solve.css";
import "../sets/sets.css";
import "./mock.css";

const MockPaper = lazy(() => import("./MockPaper"));
const MockItem = lazy(() => import("./MockItem"));
const MockDocs = lazy(() => import("./MockDocs").then((m) => ({ default: m.MockDoc })));
const MockKey = lazy(() => import("./MockDocs").then((m) => ({ default: m.MockKey })));

export function parseMockHash(hash) {
  const parts = String(hash || "").split("?")[0].replace(/^#\/mock\/?/, "").split("/").filter(Boolean);
  const id = parts[0] || "";
  const v = parts[1] || "";
  const view = ["paper", "board", "q", "key", "doc", "av"].includes(v) ? v : "home";
  const i = view === "q" ? parseInt(parts[2], 10) || 1 : null;
  const doc = view === "doc" ? parts[2] || "problems" : null;
  return { id, view, i, doc };
}

function useSay() {
  const [msg, setMsg] = useState(null);
  const say = useMemo(() => {
    let t = 0;
    return (m) => { setMsg(m); clearTimeout(t); t = setTimeout(() => setMsg(null), 2800); };
  }, []);
  return [msg, say];
}

export default function MockRouter({ hash, theme }) {
  const r = parseMockHash(hash);
  if (!r.id) { location.replace("#/study/exam/school"); return null; }
  return <MockScreen key={r.id} r={r} theme={theme} />;
}

function MockScreen({ r, theme }) {
  const { exam, school, err } = useMockExam(r.id);
  useEffect(() => { ensureMockFonts(); }, []);
  const uid = useMockUser();
  const [msg, say] = useSay();
  const title = exam ? `${school?.short || ""} ${exam.title}`.trim() : "학교별 모의고사";
  const home = `#/mock/${r.id}`;
  const back = r.view !== "home" ? home : exam ? `#/study/exam/school/${exam.school}/${encodeURIComponent(exam.ed)}` : "#/study/exam/school";
  const fall = <div className="cs-wrap sv-muted">불러오는 중…</div>;
  let body;
  if (err) body = <div className="cs-wrap"><div className="sv-empty">시험을 불러오지 못했어요.<br />{err}</div></div>;
  else if (!exam) body = fall;
  else if (r.view === "paper" || r.view === "board") body = uid === undefined ? fall : <Suspense fallback={fall}><MockPaper exam={exam} school={school} say={say} startMode={r.view === "board" ? "teacher" : "student"} /></Suspense>;
  else if (r.view === "q") body = <Suspense fallback={fall}><MockItem exam={exam} i={r.i} uid={uid} /></Suspense>;
  else if (r.view === "doc") body = <Suspense fallback={fall}><MockDocs exam={exam} school={school} docId={r.doc} say={say} /></Suspense>;
  else if (r.view === "key") body = <Suspense fallback={fall}><MockKey exam={exam} uid={uid} /></Suspense>;
  else if (r.view === "av") body = <div className="cs-wrap"><p className="cs-cdesc mx-avnote">이 시험의 문항과 같은 단원 · 유형을 교실 모니터처럼 한 문항씩 풀어 주는 해설이에요. 보고 나서 「나가기」를 누르면 이 시험으로 돌아와요.</p>
    <AvList exam={exam} from={`#/mock/${exam.id}/av`} onItem={(i) => (location.hash = `#/mock/${exam.id}/q/${i}`)} /></div>;
  else body = <MockHome exam={exam} school={school} uid={uid} say={say} />;
  const sub = r.view === "q" ? (exam?.items.find((x) => x.i === r.i)?.label || "") + (exam?.items.find((x) => x.i === r.i)?.kind === "mc" ? "번" : "")
    : r.view === "paper" || r.view === "board" ? "시험지 그대로" : r.view === "key" ? "정답과 채점 기준" : r.view === "doc" ? "자료" : r.view === "av" ? "시청각 해설" : exam?.ed || "";
  const actions = exam && r.view === "home" ? <FbAct onClick={() => (location.hash = `${home}/key`)}>✅ 정답</FbAct>
    : exam && r.view !== "home" ? <FbAct onClick={() => (location.hash = home)}>목록</FbAct> : null;
  return (
    <>
      <FeatureBar theme={theme} title={title} sub={sub} back={back} actions={actions} />
      {body}
      {msg && <div className="sv-toast cs-toast" role="status">{msg}</div>}
    </>
  );
}

// ── 시험 첫 화면 ───────────────────────────────────────────────────────────────
const FILTERS = [["all", "전체"], ["mc", "선택형"], ["sa", "서답형"], ["todo", "안 푼 문제"], ["wrong", "틀린 문제"]];
const DOC_IC = { problems: "📄", key: "✅", solutions: "📘", answersheet: "📝", english: "🔤", vocab: "📒", subjects: "🔗" };

function MockHome({ exam, school, uid, say }) {
  const admin = useIsAdmin();
  const paper = useMemo(() => (uid === undefined ? { answers: {}, sa: {}, submitted: null } : readMockPaper(exam.id)), [exam.id, uid]);
  const rec = useMemo(() => (uid === undefined ? { items: {}, results: [] } : readMockRecord(exam.id)), [exam.id, uid]);
  const g = useMemo(() => (paper.submitted ? gradeMock(exam, paper.answers, paper.sa) : null), [exam, paper]);
  const [flt, setFlt] = useState(() => { try { return sessionStorage.getItem("ash.mock.flt") || "all"; } catch { return "all"; } });
  const pickF = (f) => { setFlt(f); try { sessionStorage.setItem("ash.mock.flt", f); } catch { /* 무시 */ } };
  const ed = edInfo(exam.ed);
  const nAns = exam.items.filter((it) => isAnswered(it, paper.answers[it.i])).length;
  const pct = Math.round((nAns / exam.items.length) * 100);
  const last = rec.results[0];
  const status = (it) => { const p = rec.items[it.i]; return p ? (p.ok ? "ok" : "bad") : ""; };
  const list = exam.items.filter((it) => {
    if (flt === "mc" || flt === "sa") return it.kind === flt;
    if (flt === "todo") return !rec.items[it.i];
    if (flt === "wrong") return rec.items[it.i] && !rec.items[it.i].ok;
    return true;
  });
  const go = (p) => { location.hash = `#/mock/${exam.id}${p}`; };
  const nextI = (exam.items.find((it) => !rec.items[it.i]) || exam.items.find((it) => !rec.items[it.i]?.ok) || exam.items[0]).i;
  const pages = exam.docs.find((d) => d.id === "problems")?.pages.length || 0;
  return (
    <div className="cs-wrap mx-home">
      <div className="cs-hero">
        <span className="ic" aria-hidden="true">{ed.icon}</span>
        <div className="tx">
          <h1>{exam.title}{exam.sub ? ` · ${exam.sub}` : ""}</h1>
          <div className="sub">{school?.name || exam.school} · {exam.year}학년도 {exam.grade} {exam.term}</div>
          <div className="mx-meta">
            <span className="cs-tagx">선택형 {exam.n.mc} · {exam.pts.mc}점</span>
            <span className="cs-tagx">서답형 {exam.n.sa} · {exam.pts.sa}점</span>
            <span className="cs-tagx">⏱ {exam.minutes}분</span>
            <span className="cs-tagx">{pages}면</span>
          </div>
          <div className="cs-pbar" aria-label={`시험지에 쓴 답 ${nAns}/${exam.items.length}`}><i style={{ width: `${pct}%` }} /></div>
          <div className="cs-pt">{g ? <>채점한 시험지 <b>{g.score}</b>/{g.max}{g.counts.pending ? ` · 서답형 채점 ${g.counts.pending}개 남음` : ""}</> : <>시험지에 쓴 답 <b>{nAns}</b>/{exam.items.length}</>}
            {last && !g ? ` · 최근 채점 ${last.score}/${last.max}` : ""}</div>
        </div>
      </div>
      {exam.range && <p className="mx-range"><b>범위</b> <Rich text={exam.range} /></p>}

      <div className={admin ? "cs-gorow" : undefined}>
        <button type="button" className="sv-btn pri full cs-go" onClick={() => go("/paper")}>
          📝 {g ? `채점한 시험지 보기 · ${g.score}/${g.max}` : nAns ? `이어서 풀기 · 답 ${nAns}/${exam.items.length}` : "바로 풀기 · 시험지 그대로"}
        </button>
        {admin && (
          <button type="button" className="sv-btn cs-go cs-board" title="관리자 — 시험지 그대로 화면을 강사 모드(필기 도구 창)로 열기 · 막대의 학생 | 강사 토글로 오간다"
            onClick={() => go("/board")}>✍ 강사 모드</button>
        )}
      </div>
      <div className="cs-go2">
        <button type="button" className="sv-btn" onClick={() => go(`/q/${nextI}`)}>☝ 한 문제씩</button>
        <button type="button" className="sv-btn" onClick={() => go("/key")}>✅ 정답 · 채점 기준</button>
        <button type="button" className="sv-btn" onClick={() => go("/av")}>🎬 시청각 해설</button>
      </div>

      <div className="cs-card">
        <div className="cs-ch"><b>📂 자료</b><span>화면으로 보거나 PDF로 받아 인쇄해요</span></div>
        <div className="mx-docs">
          {exam.docs.map((d) => (
            <div key={d.id} className="mx-doc">
              <span className="ic" aria-hidden="true">{DOC_IC[d.id] || "📄"}</span>
              <span className="nm"><b>{d.label}</b><small>{d.pages.length}쪽{d.bytes ? ` · ${fmtBytes(d.bytes)}` : ""}</small></span>
              <button type="button" className="sv-btn sm" onClick={() => go(`/doc/${d.id}`)}>보기</button>
              <DocGet exam={exam} doc={d} school={school} say={say} />
            </div>
          ))}
        </div>
        <p className="cs-dnote">시험지에는 OMR 답안지에 칠하듯 답을 고르고, 서답형은 하위 문항마다 손글씨나 타자로 써요. 제출하면 선택형은 바로 채점되고, 서답형은 모범 답과 채점 요소를 보며 스스로 채점해요.</p>
      </div>

      <div className="cs-card">
        <div className="cs-ch"><b>🎬 시청각 해설</b><span>같은 단원 · 유형을 한 문항씩 — 보고 나면 이 시험으로 돌아와요</span></div>
        <AvList exam={exam} from={`#/mock/${exam.id}`} onItem={(i) => go(`/q/${i}`)} max={4} more={() => go("/av")} />
      </div>

      <div className="cs-sec">문항 <small>{list.length}</small></div>
      <div className="cs-chips">
        {FILTERS.map(([f, l]) => <button key={f} type="button" className={"cs-chip" + (flt === f ? " on" : "")} onClick={() => pickF(f)}>{l}</button>)}
      </div>
      {list.length === 0 ? <div className="sv-empty">{flt === "wrong" ? "틀린 문제가 없어요 👍" : flt === "todo" ? "모두 풀었어요 🎉" : "문항이 없어요"}</div> : (
        <div className="cs-list">
          {list.map((it) => {
            const s = status(it);
            return (
              <button key={it.i} type="button" className="cs-row" onClick={() => go(`/q/${it.i}`)}>
                <span className="no">{it.kind === "mc" ? it.label : `서${it.no}`}</span>
                <span className={"mx-pts" + (it.kind === "sa" ? " sa" : "")}>{it.pts}점</span>
                <span className="tx"><b><Rich text={it.unit} /></b><small>{it.kind === "mc" ? (it.multi ? `선택형 · 정답 ${it.ans.length}개` : "선택형") : `서답형${it.parts?.length > 1 ? ` · 하위 문항 ${it.parts.length}개` : ""}`}{rec.items[it.i]?.sel ? ` · 내 답 ${choiceText(rec.items[it.i].sel)}` : ""}</small></span>
                <span className={"st" + (s ? " " + s : "")}>{s === "ok" ? "✓" : s === "bad" ? "✗" : ""}</span>
              </button>
            );
          })}
        </div>
      )}
      {rec.results.length > 0 && (
        <div className="cs-omrhist">
          {rec.results.slice(0, 5).map((h, k) => (
            <span key={k} className="cs-tagx">{new Date(h.at).toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" })} · {h.score}/{h.max}{h.pending ? " (채점 중)" : ""}</span>
          ))}
        </div>
      )}
      {exam.code && <p className="mx-code">프린트 코드 {exam.code}</p>}
    </div>
  );
}

function DocGet({ exam, doc, school, say }) {
  const [busy, setBusy] = useState(false);
  const get = async () => {
    setBusy(true);
    try { const m = await import("./MockDocs"); await m.downloadDoc(exam, doc, school?.short, say); } finally { setBusy(false); }
  };
  return <button type="button" className="sv-btn sm" disabled={busy} onClick={get}>{busy ? "받는 중…" : "⬇ 받기"}</button>;
}
