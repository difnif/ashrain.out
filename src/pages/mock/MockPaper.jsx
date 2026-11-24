// ashrain.out — 학교별 모의고사 「시험지 그대로 풀기」(#/mock/<id>/paper) · 강사 모드(#/mock/<id>/board)
// 실제 시험지(쪽 그림)를 PDF 보듯 펼쳐 놓고 푼다.
//   · 선택형: 문항을 누르면 답 시트(문항 확대 + ①~⑤). 크게 보일 때(태블릿 · 확대)는 시험지의 보기 번호를 바로 눌러 연필 동그라미.
//     「OMR」 시트에서 실제 시험처럼 답안지에 칠해도 된다. 정답 2개 문항은 여럿 고른다.
//   · 서답형: 문항을 누르면 하위 문항마다 손글씨(줄 공책) · 타자.
//   · ⏱ 시간(시험 시간만큼 거꾸로) — 눌러서 시작 · 멈춤. 시간이 지나도 막지 않는다(넘긴 만큼 + 로).
//   · 제출하면 선택형은 바로 채점(빨간 동그라미 · 빗금 · 정답), 서답형은 모범 답 · 채점 요소로 스스로 채점 → 합계 /100.
//   · 채점 뒤 문항을 누르면 해설 시트(내 답 · 정답 · 단원 · 🎬 시청각 해설로 가기). 「틀린 것만 다시」 · 「처음부터」.
// 관리자에겐 막대에 「학생 | 강사」 — 강사 모드는 컨셉 문제와 같은 필기 창(PaperBoard.jsx)이 같은 화면 위에 들어온다.
// 답안 · 필기는 이 기기 · 계정에 바로바로 저장된다.
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import {
  readMockPaper, saveMockPaper, clearMockPaper, saveMockResult, saveMockAttempt, gradeMock, isAnswered, toggleChoice, choiceRects,
  timerLeft, fmtClock, fileUrl, CIRCLED, choiceText,
} from "../../lib/mockexams";
import PaperBoard, { ModeSwitch, boardPads, loadBoardCfg } from "../sets/PaperBoard";
import { anchorScroll, clampZoom, stepZoom, zoomLabel } from "../sets/boardview";
import { PAGE_W_PX } from "../sets/paper";
import { ItemCrop, ChoicePad, SaWriter, SaMine, SaGrader, AvButtons, PencilRing, RING_PATH, SLASH_PATH, seedRot, Rich, useIsAdmin, scrollCropTo } from "./parts";

const ZK = "ash.mock.paper.zm";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 무시 */ } };
const PICK_MIN_W = 560;               // 쪽이 이만큼(px) 넓게 보이면 시험지의 보기 번호를 바로 누른다
const headerBottom = () => { const fb = document.querySelector(".fb"); return fb ? Math.max(0, Math.round(fb.getBoundingClientRect().bottom)) : 0; };

export default function MockPaper({ exam, school, say, startMode = "student" }) {
  const hostRef = useRef(null), wrapRef = useRef(null), boxRef = useRef(null), paperRef = useRef(null);
  const admin = useIsAdmin();
  const [mode, setMode] = useState(startMode === "teacher" ? "teacher" : "student");
  const teacher = mode === "teacher" && admin === true;
  const [hand, setHand] = useState(() => loadBoardCfg().hand);
  const pads = teacher ? boardPads(hand) : { l: 0, r: 0 };
  const [st, setSt] = useState(() => readMockPaper(exam.id));       // { answers, sa, submitted, timer }
  const [sheet, setSheet] = useState(null);       // 답 시트 i
  const [sol, setSol] = useState(null);           // 채점 뒤 해설 시트 i
  const [omr, setOmr] = useState(false);
  const [ask, setAsk] = useState(false);          // 빈칸이 있을 때 제출 확인
  const [ready, setReady] = useState(false);
  const [zm, setZm] = useState(() => clampZoom(Number(lsGet(ZK, 1))));
  const [pick, setPick] = useState(false);        // 시험지 보기 번호 바로 누르기
  const [now, setNow] = useState(Date.now());
  const S = useRef({});
  S.current = { st, teacher };
  const doc = exam.docs.find((d) => d.id === "problems");
  const items = exam.items;
  const byI = useMemo(() => Object.fromEntries(items.map((it) => [it.i, it])), [items]);
  const g = useMemo(() => (st.submitted ? gradeMock(exam, st.answers, st.sa) : null), [exam, st]);
  const rowOf = useMemo(() => (g ? Object.fromEntries(g.rows.map((r) => [r.i, r])) : {}), [g]);

  // 문제지(쪽 그림) — PaperBoard 가 쓰는 꼴(root · firstPage · setZoom · reveal)
  useLayoutEffect(() => {
    paperRef.current = {
      get root() { return hostRef.current; },
      get firstPage() { return hostRef.current?.querySelector(".pg") || null; },
      setZoom(z) { if (wrapRef.current) wrapRef.current.style.zoom = String(z); },
      reveal(i) {
        const el = hostRef.current?.querySelector(`.mx-q[data-i="${i}"]`);
        if (!el) return;
        const r = el.getBoundingClientRect(), box = boxRef.current;
        window.scrollBy({ top: r.top - headerBottom() - 14, behavior: "smooth" });
        if (box) { const br = box.getBoundingClientRect(); if (r.left < br.left || r.right > br.right) box.scrollLeft += r.left - br.left - 8; }
      },
    };
    setReady(true);
    return () => { paperRef.current = null; };
  }, []);

  // 확대: 폭 맞춤 × 배수 — 기준점(손가락 가운데 · 화면 가운데) 아래 내용이 제자리에 남게 (컨셉 문제와 같은 방식)
  const zRef = useRef(0), zmRef = useRef(zm), padsRef = useRef(pads);
  padsRef.current = pads;
  const applyZoom = useCallback((zm1, anchor) => {
    zm1 = clampZoom(zm1);
    zmRef.current = zm1;
    setZm(zm1);
    const box = boxRef.current, p = paperRef.current;
    if (!box || !p || !wrapRef.current) return;
    const pd = padsRef.current;
    const z1 = Math.max(0.3, (box.clientWidth - pd.l - pd.r - 8) / PAGE_W_PX) * zm1, z0 = zRef.current;
    const ref = p.firstPage || hostRef.current;
    const r0 = ref.getBoundingClientRect();
    p.setZoom(z1.toFixed(4));
    zRef.current = z1;
    setPick(PAGE_W_PX * z1 >= PICK_MIN_W);
    if (anchor === false || !z0) return;
    const a = anchor || { x: (pd.l + window.innerWidth - pd.r) / 2, y: window.innerHeight / 2 };
    const { dx, dy } = anchorScroll(r0, z0, ref.getBoundingClientRect(), z1, a.x, a.y, a.tx || 0, a.ty || 0);
    if (dx) box.scrollLeft += dx;
    if (dy) window.scrollBy(0, dy);
  }, []);
  useEffect(() => { if (ready) applyZoom(zmRef.current, false); }, [ready, applyZoom]);
  useEffect(() => {
    const on = () => applyZoom(zmRef.current);
    window.addEventListener("resize", on);
    return () => window.removeEventListener("resize", on);
  }, [applyZoom]);
  useEffect(() => { lsSet(ZK, zm); }, [zm]);
  useLayoutEffect(() => { if (ready) applyZoom(zmRef.current); }, [teacher, hand]);   // eslint-disable-line react-hooks/exhaustive-deps

  // 학생 | 강사
  const switchMode = useCallback((m) => {
    if (m === "teacher" && admin !== true) return;
    setSheet(null); setSol(null); setOmr(false);
    setMode(m);
    try { history.replaceState(history.state, "", `#/mock/${exam.id}/${m === "teacher" ? "board" : "paper"}`); } catch { /* 무시 */ }
  }, [admin, exam.id]);
  useEffect(() => { if (startMode === "teacher" && admin === false) say?.("강사 모드는 관리자만 쓸 수 있어요 — 학생 모드로 열었어요"); }, [startMode, admin, say]);

  // 저장 — 나갈 때는 바로(돌던 시간은 멈춘 채로 — 다시 들어와 이어서 누르면 이어 간다)
  useEffect(() => { const t = setTimeout(() => saveMockPaper(exam.id, st), 250); return () => clearTimeout(t); }, [exam.id, st]);
  useEffect(() => () => {
    const s = S.current.st;
    const timer = s.timer && s.timer.paused == null && !s.submitted ? { ...s.timer, paused: Date.now() } : s.timer;
    saveMockPaper(exam.id, { ...s, timer });
  }, [exam.id]);
  // 시간 — 도는 동안 1초마다
  const running = !!st.timer && st.timer.paused == null && !st.submitted;
  useEffect(() => { if (!running) return undefined; const t = setInterval(() => setNow(Date.now()), 1000); return () => clearInterval(t); }, [running]);
  const left = timerLeft(st.timer, exam.minutes, st.timer?.paused ?? now);
  const timerTap = () => setSt((s) => {
    if (s.submitted) return s;
    const t = Date.now();
    if (!s.timer) return { ...s, timer: { start: t, paused: null, used: 0 } };
    if (s.timer.paused == null) return { ...s, timer: { ...s.timer, paused: t } };
    return { ...s, timer: { start: t, paused: null, used: (s.timer.used || 0) + (s.timer.paused - s.timer.start) } };
  });
  const timeUp = useRef(false);
  useEffect(() => {
    if (running && left <= 0 && !timeUp.current) { timeUp.current = true; say?.(`${exam.minutes}분이 지났어요 — 마무리하고 제출해 보세요`); }
  }, [running, left, exam.minutes, say]);

  // 답 바꾸기
  const setAnswer = useCallback((i, ans) => {
    setSt((s) => {
      if (s.submitted) return s;
      const answers = { ...s.answers };
      const next = typeof ans === "function" ? ans(s.answers[i]) : ans;
      if (next) answers[i] = next; else delete answers[i];
      return { ...s, answers };
    });
  }, []);
  const pickChoice = useCallback((i, c) => {
    const it = byI[i];
    if (!it || S.current.teacher || S.current.st.submitted) return;
    setAnswer(i, (prev) => toggleChoice(prev, c, it.multi));
  }, [byI, setAnswer]);
  const openItem = useCallback((i) => {
    if (S.current.teacher) return;
    if (S.current.st.submitted) setSol(i); else setSheet(i);
  }, []);

  const nAnswered = items.filter((it) => isAnswered(it, st.answers[it.i])).length;
  const blanks = items.length - nAnswered;

  // 제출 → 채점
  const submit = () => {
    setAsk(false);
    const at = new Date().toISOString();
    setSt((s) => {
      const timer = s.timer && s.timer.paused == null ? { ...s.timer, paused: Date.now() } : s.timer;
      const sa = { ...s.sa };
      for (const it of items) if (it.kind === "sa" && !isAnswered(it, s.answers[it.i])) sa[it.i] = { got: 0, checks: [] };
      const next = { ...s, sa, timer, submitted: { at } };
      const gg = gradeMock(exam, next.answers, next.sa);
      saveMockResult(exam.id, { kind: "paper", sid: at, at, score: gg.score, max: gg.max, pending: gg.counts.pending || 0 });
      for (const r of gg.rows) {
        if (r.kind === "mc" && r.status !== "blank") saveMockAttempt(exam.id, r.i, { sel: next.answers[r.i]?.sel || [], ok: r.status === "ok", via: "paper" });
      }
      return next;
    });
    setSheet(null); setOmr(false);
    const first = items.find((it) => it.kind === "sa" && isAnswered(it, st.answers[it.i]));
    if (first) setTimeout(() => setSol(first.i), 350);
    window.scrollTo?.({ top: 0, behavior: "smooth" });
  };
  const setGrade = (i, grade) => setSt((s) => {
    const next = { ...s, sa: { ...s.sa, [i]: grade } };
    const gg = gradeMock(exam, next.answers, next.sa);
    if (s.submitted) {
      saveMockResult(exam.id, { kind: "paper", sid: s.submitted.at, at: s.submitted.at, score: gg.score, max: gg.max, pending: gg.counts.pending || 0 });
      const it = byI[i];
      if (it && Number.isFinite(grade.got)) saveMockAttempt(exam.id, i, { got: grade.got, ok: grade.got >= it.pts, via: "paper" }, { count: false });
    }
    return next;
  });
  const retryWrong = () => {
    setSt((s) => {
      const gg = gradeMock(exam, s.answers, s.sa);
      const keep = new Set(gg.rows.filter((r) => r.status === "ok").map((r) => r.i));
      const answers = {}, sa = {};
      for (const [i, a] of Object.entries(s.answers)) if (keep.has(Number(i))) answers[i] = a;
      for (const [i, v] of Object.entries(s.sa)) if (keep.has(Number(i))) sa[i] = v;
      return { answers, sa, submitted: null, timer: null };
    });
    setSol(null); timeUp.current = false;
  };
  const restart = () => { clearMockPaper(exam.id); setSt({ answers: {}, sa: {}, submitted: null, timer: null }); setSol(null); timeUp.current = false; };

  const nextOf = (i, d = 1) => { const k = items.findIndex((it) => it.i === i); return items[k + d]?.i ?? null; };
  const sheetNext = (i) => { const n = nextOf(i); if (n == null) { setSheet(null); return; } setSheet(n); paperRef.current?.reveal(n); };

  const pages = doc?.pages || [];
  return (
    <div className="cs-paperpage mx-paperpage">
      {g && (
        <div className="cs-gsum mx-gsum" role="status">
          <b>{g.score}<small>/{g.max}</small></b>
          <span><i>선택형 {g.mc.got}/{g.mc.max}</i><i>서답형 {g.sa.got}/{g.sa.max}</i></span>
          {g.counts.pending > 0 && <span className="cs-gx warn">서답형 스스로 채점 {g.counts.pending}개 남음</span>}
          <span className="cs-gx">문항을 누르면 해설 · 🎬 시청각 해설</span>
        </div>
      )}
      {!g && st.timer == null && nAnswered === 0 && (
        <div className="mx-tip">문항을 누르면 답을 써요{pick ? " · 보기 번호를 바로 눌러도 돼요" : ""} · ⏱을 누르면 {exam.minutes}분 시간을 재요</div>
      )}
      <div ref={boxRef} className={"cs-paperbox" + (teacher ? " pb-on" : "")} style={teacher ? { paddingLeft: pads.l, paddingRight: pads.r } : undefined}>
        <div ref={hostRef} className="cs-paperhost">
          <div ref={wrapRef} className={"mx-paper" + (teacher ? " teach" : "") + (pick && !g ? " pick" : "")}>
            {pages.map((pg, pi) => (
              <div key={pg.img} className="pg mx-pg" style={{ width: PAGE_W_PX, height: (PAGE_W_PX * pg.h) / pg.w }}>
                <img className="mx-pimg" src={fileUrl(exam, pg.img)} alt={`${pi + 1}쪽`} draggable={false} loading={pi < 2 ? "eager" : "lazy"} />
                {pi === 0 && g && <div className="mx-score" aria-hidden="true">{g.score}<small>/{g.max}</small></div>}
                {items.filter((it) => it.box.p === pi).map((it) => (
                  <PageItem key={it.i} it={it} ans={st.answers[it.i]} row={rowOf[it.i]} graded={!!g} pick={pick && !g && !teacher}
                    onOpen={openItem} onPick={pickChoice} />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
      <PaperBoard on={teacher} ready={ready} admin={admin === true} catId="mock" set={{ no: exam.id, short: `${school?.short || ""} ${exam.title}`.trim() }}
        paperRef={paperRef} hostRef={hostRef} boxRef={boxRef} zm={zm} onZoom={applyZoom} onMode={switchMode} onCfg={(c) => setHand(c.hand)} />

      <div className={"cs-pbar2" + (teacher ? " pb-out" : "")} role="toolbar" aria-label="시험지 도구" aria-hidden={teacher}>
        {admin === true && <ModeSwitch mode={teacher ? "teacher" : "student"} onChange={switchMode} />}
        <div className="cs-zoom">
          <button type="button" className="cs-tb" disabled={zm <= 1.001} onClick={() => applyZoom(stepZoom(zm, -1))} aria-label="작게">−</button>
          <button type="button" className="cs-tb cs-zv" onClick={() => applyZoom(1)} title="폭 맞춤">{zoomLabel(zm)}</button>
          <button type="button" className="cs-tb" disabled={zm >= 2.999} onClick={() => applyZoom(stepZoom(zm, 1))} aria-label="크게">＋</button>
        </div>
        {!g && (
          <button type="button" className={"cs-tb mx-timer" + (left < 0 ? " over" : "") + (running ? " run" : "")} onClick={timerTap}
            title={!st.timer ? `${exam.minutes}분 시간 재기` : running ? "멈추기" : "이어서"}>
            {!st.timer ? `⏱ ${exam.minutes}분` : `${running ? "⏱" : "⏸"} ${fmtClock(left)}`}
          </button>
        )}
        <button type="button" className="cs-tb" onClick={() => setOmr(true)}>OMR{g ? "" : ` ${nAnswered}/${items.length}`}</button>
        <span className="cs-fill" />
        {!g ? (
          <button type="button" className="sv-btn pri cs-submit mx-submit" onClick={() => (blanks > 0 ? setAsk(true) : submit())}><span className="lg">제출하고 채점</span><span className="sm">채점</span></button>
        ) : (
          <div className="cs-gbar">
            <b className="cs-gs">{g.score}<small>/{g.max}</small></b>
            {g.rows.some((r) => r.status !== "ok") && <button type="button" className="sv-btn sm pri" onClick={retryWrong}>틀린 것만 다시</button>}
            <button type="button" className="sv-btn sm" onClick={restart}>처음부터</button>
          </div>
        )}
      </div>

      {ask && (
        <div className="cs-sheetbg" onClick={() => setAsk(false)}>
          <div className="cs-sheet mx-ask" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="제출 확인">
            <div className="cs-shb">
              <b>아직 답을 안 쓴 문항이 {blanks}개 있어요</b>
              <p className="sv-muted">{items.filter((it) => !isAnswered(it, st.answers[it.i])).map((it) => (it.kind === "sa" ? it.label : `${it.label}번`)).join(" · ")}</p>
            </div>
            <div className="cs-shf">
              <button type="button" className="sv-btn sm" onClick={() => { setAsk(false); setOmr(true); }}>OMR에서 확인</button>
              <span className="cs-fill" />
              <button type="button" className="sv-btn sm pri" onClick={submit}>그래도 제출</button>
            </div>
          </div>
        </div>
      )}
      {sheet != null && byI[sheet] && (
        <AnswerSheet key={sheet} exam={exam} it={byI[sheet]} value={st.answers[sheet]} onPick={(c) => pickChoice(sheet, c)}
          onSa={(v) => setAnswer(sheet, v)} onClose={() => setSheet(null)} onNext={nextOf(sheet) != null ? () => sheetNext(sheet) : null} />
      )}
      {sol != null && byI[sol] && g && (
        <SolutionSheet key={sol} exam={exam} it={byI[sol]} ans={st.answers[sol]} row={rowOf[sol]} grade={st.sa[sol]}
          onGrade={(gr) => setGrade(sol, gr)} onClose={() => setSol(null)}
          onMove={(d) => { const n = nextOf(sol, d); if (n != null) { setSol(n); paperRef.current?.reveal(n); } }}
          from={`#/mock/${exam.id}/paper`} />
      )}
      {omr && (
        <OmrSheet exam={exam} answers={st.answers} rows={g ? rowOf : null} onPick={pickChoice} onClose={() => setOmr(false)}
          onGo={(i) => { setOmr(false); setTimeout(() => paperRef.current?.reveal(i), 30); }}
          onOpen={(i) => { setOmr(false); openItem(i); }} />
      )}
    </div>
  );
}

/* ── 시험지 위 문항 하나: 누르는 칸 · 보기 자리 · 연필 동그라미 · 채점 표시 ── */
function PageItem({ it, ans, row, graded, pick, onOpen, onPick }) {
  const b = it.box;
  const sel = ans?.k === "mc" ? ans.sel || [] : [];
  const rects = useMemo(() => (pick ? choiceRects(it) : []), [pick, it]);
  const pos = (x, y) => ({ left: `${((x - b.x) / b.w) * 100}%`, top: `${((y - b.y) / b.h) * 100}%` });
  const ringW = (c, k = 3.6) => ({ width: `${((c.r * k) / b.w) * 100}%` });
  const st = row?.status;
  return (
    <div className="mx-q" data-i={it.i} style={{ left: `${b.x * 100}%`, top: `${b.y * 100}%`, width: `${b.w * 100}%`, height: `${b.h * 100}%` }}
      onClick={() => onOpen(it.i)} role="button" tabIndex={0} aria-label={`${it.label}${it.kind === "mc" ? "번" : ""} 답 쓰기`}
      onKeyDown={(e) => { if (e.key === "Enter") onOpen(it.i); }}>
      {it.kind === "mc" && (it.ch || []).map((c, k) => {
        const n = k + 1, on = sel.includes(n);
        const ok = graded && st !== "ok" && it.ans.includes(n), bad = graded && on && !it.ans.includes(n);
        if (!on && !ok && !bad) return null;
        return <span key={n} className="mx-ring" style={{ ...pos(c.x, c.y), ...ringW(c) }}><PencilRing on={on} ok={ok} bad={bad} seed={it.i * 7 + n} /></span>;
      })}
      {pick && rects.map((r, k) => (
        <button key={k} type="button" className="mx-pick" aria-label={`${it.label}번 ${CIRCLED[k + 1]}`}
          style={{ left: `${((r.x - b.x) / b.w) * 100}%`, top: `${((r.y - b.y) / b.h) * 100}%`, width: `${(r.w / b.w) * 100}%`, height: `${(r.h / b.h) * 100}%` }}
          onClick={(e) => { e.stopPropagation(); onPick(it.i, k + 1); }} />
      ))}
      {it.kind === "sa" && !graded && isAnswered(it, ans) && <span className="mx-wrote">✍ 답을 썼어요</span>}
      {graded && (
        <span className={"mx-mark " + (st === "ok" ? "ok" : st === "part" ? "part" : st === "pending" ? "pending" : "bad")} aria-hidden="true">
          <svg viewBox="0 0 40 40" style={{ transform: `rotate(${seedRot(it.i * 3)}deg)` }}>
            {st === "ok" || st === "part" ? <path d={RING_PATH} fill="none" stroke="#d42a3c" strokeWidth="2.4" strokeLinecap="round" />
              : st === "pending" ? null : <path d={SLASH_PATH} fill="none" stroke="#d42a3c" strokeWidth="2.6" strokeLinecap="round" />}
          </svg>
        </span>
      )}
      {graded && it.kind === "mc" && st !== "ok" && <span className="mx-key">→ {choiceText(it.ans)}</span>}
      {graded && it.kind === "sa" && <span className="mx-key sa">{st === "pending" ? "스스로 채점 →" : `${row.got}/${it.pts}점`}</span>}
    </div>
  );
}

/* ── 답 시트: 선택형 ①~⑤ · 서답형 손글씨/타자 ── */
function AnswerSheet({ exam, it, value, onPick, onSa, onClose, onNext }) {
  const sel = value?.k === "mc" ? value.sel || [] : [];
  const cropRef = useRef(null);
  return (
    <div className="cs-sheetbg" onClick={onClose}>
      <div className="cs-sheet mx-sheet" onClick={(e) => e.stopPropagation()} role="dialog" aria-label={`${it.label} 답 쓰기`}>
        <div className="cs-shh">
          <span className="cs-shno">{it.kind === "mc" ? it.label : "서"}</span>
          <div className="cs-sht"><b>{it.kind === "mc" ? `${it.label}번` : it.label} · {it.pts}점</b><small>{it.kind === "mc" ? (it.multi ? `정답 ${it.ans.length}개를 모두 골라요` : "보기를 하나 골라요") : "하위 문항마다 풀이 과정과 답을 써요"}</small></div>
          <span className="cs-fill" />
          <button type="button" className="cs-x" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="cs-shb">
          <div ref={cropRef} className={"mx-cropbox" + (it.kind === "sa" ? " sa" : "")}><ItemCrop exam={exam} it={it} sel={sel} onPick={it.kind === "mc" ? onPick : undefined} /></div>
          {it.kind === "mc" ? <ChoicePad it={it} sel={sel} onPick={onPick} />
            : <SaWriter it={it} value={value} onChange={onSa} onPart={(n) => scrollCropTo(cropRef.current, it, n)} />}
        </div>
        <div className="cs-shf">
          <span className="sv-muted">{it.kind === "mc" ? (sel.length ? `고른 답 ${choiceText(sel)}` : "아직 안 골랐어요") : ""}</span>
          <span className="cs-fill" />
          {onNext && <button type="button" className="sv-btn sm" onClick={onNext}>다음 ›</button>}
          <button type="button" className="sv-btn sm pri" onClick={onClose}>확인</button>
        </div>
      </div>
    </div>
  );
}

/* ── 채점 뒤 해설 시트: 내 답 · 정답 · 단원 · 서답형 스스로 채점 · 🎬 시청각 해설 ── */
function SolutionSheet({ exam, it, ans, row, grade, onGrade, onClose, onMove, from }) {
  const st = row?.status;
  const sel = ans?.k === "mc" ? ans.sel || [] : [];
  const mark = it.kind === "mc" ? { ok: it.ans, bad: sel.filter((c) => !it.ans.includes(c)) } : null;
  const verdict = st === "ok" ? "맞았어요 ○" : st === "part" ? `부분 점수 ${row.got}/${it.pts}` : st === "pending" ? "스스로 채점해요" : st === "blank" ? "답을 쓰지 않았어요" : "틀렸어요";
  return (
    <div className="cs-sheetbg" onClick={onClose}>
      <div className="cs-sheet cs-solsheet mx-sheet" onClick={(e) => e.stopPropagation()} role="dialog" aria-label={`${it.label} 해설`}>
        <div className="cs-shh">
          <span className={"cs-shno mx-st " + (st || "")}>{it.kind === "mc" ? it.label : "서"}</span>
          <div className="cs-sht"><b>{it.kind === "mc" ? `${it.label}번` : it.label} · {it.pts}점</b><small><Rich text={it.unit} /></small></div>
          <span className="cs-fill" />
          <button type="button" className="cs-x" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="cs-shb cs-solbody">
          <div className="mx-cropbox"><ItemCrop exam={exam} it={it} sel={sel} mark={mark} /></div>
          <div className={"cs-verdict iv-banner " + (st === "ok" ? "ok" : st === "pending" || st === "part" ? "" : "bad")}>
            <div className="iv-verdict">{verdict}</div>
            {it.kind === "mc" && (
              <>
                <div className="iv-mine"><span className="iv-lab">내 답</span>{sel.length ? choiceText(sel) : "무응답"}</div>
                <div className="iv-ans"><span className="iv-lab">정답</span>{choiceText(it.ans)}</div>
              </>
            )}
          </div>
          {it.kind === "sa" && (
            <>
              <div className="mx-h">내 답</div>
              <SaMine it={it} value={ans} />
              <div className="mx-h">모범 답과 채점 요소</div>
              <SaGrader it={it} grade={grade} onGrade={onGrade} />
            </>
          )}
          <AvButtons it={it} from={from} />
          {exam.notes?.length > 0 && it.kind === "sa" && <p className="cs-dnote">{exam.notes.join(" ")}</p>}
        </div>
        <div className="cs-shf">
          <button type="button" className="sv-btn sm" onClick={() => onMove(-1)}>‹ 이전</button>
          <span className="cs-fill" />
          <a className="sv-btn sm" href={`#/mock/${exam.id}/q/${it.i}`}>한 문제씩</a>
          <button type="button" className="sv-btn sm" onClick={() => onMove(1)}>다음 ›</button>
        </div>
      </div>
    </div>
  );
}

/* ── OMR 답안지: 선택형 칠하기 · 서답형 쓴 것 · 번호 눌러 그 문항으로 ── */
function OmrSheet({ exam, answers, rows, onPick, onClose, onGo, onOpen }) {
  const mcs = exam.items.filter((it) => it.kind === "mc"), sas = exam.items.filter((it) => it.kind === "sa");
  return (
    <div className="cs-sheetbg" onClick={onClose}>
      <div className="cs-sheet mx-omr" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="OMR 답안지">
        <div className="cs-shh">
          <div className="cs-sht"><b>OMR 답안지</b><small>{rows ? "빨간 동그라미 = 정답 · 빗금 = 틀림" : "칸을 눌러 칠해요 · 번호를 누르면 그 문항으로"}</small></div>
          <span className="cs-fill" />
          <button type="button" className="cs-x" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="cs-shb mx-omrb">
          <div className="mx-omrg">
            {mcs.map((it) => {
              const sel = answers[it.i]?.k === "mc" ? answers[it.i].sel : [];
              const r = rows?.[it.i];
              return (
                <div key={it.i} className={"mx-orow" + (r ? " " + r.status : "")}>
                  <button type="button" className="no" onClick={() => onGo(it.i)}>{it.label}</button>
                  {[1, 2, 3, 4, 5].map((n) => {
                    const on = sel.includes(n), key = rows && it.ans.includes(n);
                    return (
                      <button key={n} type="button" className={"bub" + (on ? " on" : "") + (key ? " key" : "") + (rows && on && !it.ans.includes(n) ? " bad" : "")}
                        disabled={!!rows} onClick={() => onPick(it.i, n)} aria-label={`${it.label}번 ${CIRCLED[n]}`} aria-pressed={on}>{n}</button>
                    );
                  })}
                  {it.multi && <i className="mx-m2">2개</i>}
                </div>
              );
            })}
          </div>
          {sas.length > 0 && (
            <div className="mx-osa">
              {sas.map((it) => {
                const r = rows?.[it.i];
                const done = isAnswered(it, answers[it.i]);
                return (
                  <button key={it.i} type="button" className={"mx-osab" + (done ? " done" : "") + (r ? " " + r.status : "")} onClick={() => onOpen(it.i)}>
                    <b>{it.label}</b><small>{r ? (r.status === "pending" ? "채점 전" : `${r.got}/${it.pts}점`) : done ? "썼어요" : "안 썼어요"}</small>
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

