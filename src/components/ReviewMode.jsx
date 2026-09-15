// src/components/ReviewMode.jsx — 개념 복습 모드 (ConceptViewer 안에서 단락 목록 대신 렌더)
// 흐름: 소개 카드 → 단락을 하나씩 펼쳐 읽기("다음" 은 4초 + 끝까지 스크롤해야 켜짐) → 퀴즈 3문제 → 만점이면 Ⓓ 적립
// props
//   concept, blocks            concepts 행 · 렌더할 단락 배열
//   renderBlock(block, idx)    ConceptViewer 가 주는 단락 렌더 함수 (보통 화면과 똑같이 그린다)
//   uid, theme('light'|'dark')
//   recent                     이 방문 전 최근 읽은 개념 id (가장 최근이 앞). 순위·상한은 이 목록으로 매긴다 —
//                              페이지를 여는 순간 현재 개념이 1위가 되어 버리면 상한 5·3·3·2·2 가 무의미해지기 때문.
//                              목록에 없는(처음 읽는) 개념은 맨 뒤에 붙는다 (첫 사용자 = 1위 → 5회, 5개를 읽어 온 학생 = 6위 → 2회).
//   onExit()                   복습 모드 종료 (개념으로 돌아가기)
//   onCompleted({ reward, drop_balance })    만점 완주 뒤
// 정답 판정·보상은 전부 서버(api/review.js). 여기서는 답만 모아 보낸다.
// startReview 는 「복습 시작」 때 부른다(행의 started_at 이 읽기 시간을 포함해 서버 45초 규칙이 자연스럽다). 문항은 정답 없이 내려온다.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import ItemQuestion from "./ItemQuestion";
import { useToast } from "../pages/solve/SolveShell";
import { kindOf } from "../lib/answers";
import {
  getRecentConcepts, recentIds, reviewStatus, startReview, completeReview,
  MIN_STEP_MS, REWARD, DAILY_CAP,
} from "../lib/review";
import "../pages/solve/solve.css";

const CSS = `
.rv-root { position: relative; }
.rv-root.rv-light { --text:#1F2937; --muted:#6B7480; --surface2:#F1F2F4; --surface3:#E4E7EB; --border:#D9DEE4; --accent:#0D9488; --good:#16A34A; --bad:#DC2626; }
.rv-root.rv-dark  { --text:#E2E8F0; --muted:#8A929C; --surface2:#1C1F26; --surface3:#23262D; --border:#2B2E36; --accent:#14B8A6; --good:#4ADE80; --bad:#F87171; }
.rv-kit { color: var(--text); font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.rv-kit * { box-sizing: border-box; }
.rv-kit .sv-card { margin-bottom: 0; }
.rv-head { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.rv-head h3 { margin: 0; font-size: 17px; font-weight: 800; }
.rv-tag { font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 999px; background: var(--accent); color: #fff; white-space: nowrap; }
.rv-tag.off { background: var(--surface3); color: var(--muted); }
.rv-rules { margin: 10px 0 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px; }
.rv-rules li { display: flex; gap: 10px; align-items: flex-start; font-size: 14px; line-height: 1.55; }
.rv-rules .no { flex: none; width: 22px; height: 22px; border-radius: 999px; background: var(--surface2); font-size: 12px; font-weight: 800; display: inline-flex; align-items: center; justify-content: center; }
.rv-stat { margin-top: 12px; padding: 10px 12px; border-radius: 10px; background: var(--surface2); font-size: 13px; line-height: 1.6; }
.rv-stat b { color: var(--accent); }
.rv-stat.warn { color: var(--bad); }
.rv-actions { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
.rv-actions .sv-btn { flex: 1 1 45%; }
.rv-blocks { display: grid; grid-template-columns: 1fr; gap: 16px; }
.rv-blk { animation: rv-in .35s ease both; }
.rv-sentinel { height: 1px; }
.rv-more { text-align: center; font-size: 12.5px; color: var(--muted); padding: 8px 0 0; margin: 0; }
.rv-bar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 30; background: var(--surface); border-top: 1px solid var(--border);
  padding: 10px 14px calc(10px + env(safe-area-inset-bottom, 0px)); box-shadow: 0 -6px 20px rgba(0,0,0,.08); }
.rv-bar-in { max-width: 768px; margin: 0 auto; display: flex; align-items: center; gap: 12px; }
.rv-prog { flex: 1; min-width: 0; }
.rv-prog .sv-bar { margin-top: 5px; }
.rv-prog .lab { font-size: 12.5px; font-weight: 800; }
.rv-prog .hint { font-size: 11.5px; color: var(--muted); margin-left: 6px; font-weight: 600; }
.rv-bar .sv-btn { flex: none; min-width: 108px; }
.rv-quiz-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; font-size: 13px; color: var(--muted); }
.rv-quiz-top b { color: var(--text); font-size: 14px; }
.rv-dots { display: flex; gap: 6px; }
.rv-dots i { width: 8px; height: 8px; border-radius: 999px; background: var(--surface3); display: block; }
.rv-dots i.on { background: var(--accent); }
.rv-dots i.cur { outline: 2px solid var(--accent); outline-offset: 1px; }
.rv-short { display: flex; gap: 8px; margin-top: 10px; }
.rv-short .sv-in { flex: 1; min-width: 0; }
.rv-note { font-size: 12px; color: var(--muted); margin: 8px 0 0; line-height: 1.5; }
.rv-result { text-align: center; padding: 22px 14px; }
.rv-result h3 { margin: 0 0 6px; font-size: 20px; font-weight: 800; }
.rv-drop { position: relative; display: inline-block; margin: 10px 0 6px; font-size: 38px; font-weight: 900; color: var(--accent); letter-spacing: -1px;
  animation: rv-pop .7s cubic-bezier(.2,.9,.3,1.3) both; }
.rv-drop.none { font-size: 15px; font-weight: 700; color: var(--muted); animation: none; letter-spacing: 0; line-height: 1.5; }
.rv-drop .sp { position: absolute; top: 0; font-size: 16px; opacity: 0; animation: rv-float 1.6s ease-out both; }
.rv-drop .sp:nth-child(1) { left: -22px; animation-delay: .25s; }
.rv-drop .sp:nth-child(2) { right: -24px; animation-delay: .45s; }
.rv-drop .sp:nth-child(3) { left: 40%; top: -8px; animation-delay: .6s; }
.rv-lines { font-size: 13.5px; color: var(--muted); line-height: 1.8; }
.rv-lines b { color: var(--text); }
.rv-wrong { margin: 10px 0 2px; font-size: 14px; }
.rv-wrong b { color: var(--bad); }
@keyframes rv-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
@keyframes rv-pop { 0% { transform: scale(.5); opacity: 0; } 60% { transform: scale(1.15); opacity: 1; } 100% { transform: scale(1); } }
@keyframes rv-float { 0% { transform: translateY(6px); opacity: 0; } 25% { opacity: 1; } 100% { transform: translateY(-38px); opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .rv-drop, .rv-drop .sp, .rv-blk { animation: none; opacity: 1; } }
`;

const BAR_H = 84;   // 고정 하단 바 높이(대략) — "끝까지 읽음" 판정 여유

/** 소개·결과 카드의 보상 배지 */
function rewardLabel(s) {
  if (!s) return null;
  if (s.ready === false) return { text: "보상 준비 중", off: true };
  if (s.ready === null) return null;
  if (s.rewardable === false) {
    if ((s.today_done ?? 0) >= (s.today_cap ?? DAILY_CAP)) return { text: "오늘 보상 마감", off: true };
    return { text: "보상 없음", off: true };
  }
  return { text: `Ⓓ +${s.reward ?? REWARD}`, off: false };
}

const scrollTop = () => { try { window.scrollTo({ top: 0, behavior: "smooth" }); } catch { /* 무시 */ } };

export default function ReviewMode({ concept, blocks, renderBlock, uid, theme = "light", recent: recentProp, onExit, onCompleted }) {
  const list = useMemo(() => (Array.isArray(blocks) ? blocks : []), [blocks]);
  const [toast, setToast] = useToast();
  const [phase, setPhase] = useState("intro");        // intro | read | quiz | result
  const [status, setStatus] = useState(null);         // reviewStatus 의 이 개념 항목 + 오늘 현황
  const [session, setSession] = useState(null);       // startReview 응답
  const [busy, setBusy] = useState(false);
  const [step, setStep] = useState(0);                // 마지막으로 펼친 단락 index
  const [timeOk, setTimeOk] = useState(false);
  const [seen, setSeen] = useState(false);
  const [left, setLeft] = useState(Math.ceil(MIN_STEP_MS / 1000));
  const [qi, setQi] = useState(0);
  const [answers, setAnswers] = useState({});         // item_id → { index } | { answer }
  const [result, setResult] = useState(null);
  const [waitUntil, setWaitUntil] = useState(0);      // too_fast 뒤 재제출 가능 시각
  const readStartRef = useRef(0);
  const readMsRef = useRef(0);
  const lastRef = useRef(null);
  const sentinelRef = useRef(null);
  const recent = useMemo(() => {
    const id = concept?.id;
    const base = (Array.isArray(recentProp) ? recentIds(recentProp) : recentIds(getRecentConcepts()).filter((x) => x !== id)).slice(0, 5);
    if (!id || base.includes(id)) return base;
    return base.length >= 5 ? [...base.slice(0, 4), id] : [...base, id];   // 처음 읽는 개념은 맨 뒤(최대 5위)
  }, [concept?.id, recentProp]);
  const N = list.length;
  const items = session?.items || [];

  // 소개 카드용 현황
  useEffect(() => {
    let alive = true;
    setStatus(null);
    reviewStatus(recent).then((r) => {
      if (!alive) return;
      const mine = (r.concepts || []).find((c) => c.concept_id === concept?.id) || { rank: 1, cap: 5, done: 0, remaining: r.ready ? 5 : 0 };
      const today_done = r.today_done ?? 0, today_cap = r.today_cap ?? DAILY_CAP;
      setStatus({ ready: r.ready, today_done, today_cap, reward: r.reward ?? REWARD, ...mine,
        rewardable: !!r.ready && mine.remaining > 0 && today_done < today_cap });
    }).catch(() => { if (alive) setStatus({ ready: null }); });
    return () => { alive = false; };
  }, [concept?.id, recent]);

  // ── 읽기 단계: 4초 타이머 ───────────────────────────────────────────────────
  useEffect(() => {
    if (phase !== "read") return;
    setTimeOk(false); setSeen(false); setLeft(Math.ceil(MIN_STEP_MS / 1000));
    const t0 = Date.now();
    const tick = setInterval(() => setLeft(Math.max(0, Math.ceil((MIN_STEP_MS - (Date.now() - t0)) / 1000))), 1000);
    const t = setTimeout(() => setTimeOk(true), MIN_STEP_MS);
    return () => { clearTimeout(t); clearInterval(tick); };
  }, [phase, step]);

  // ── 읽기 단계: 마지막 단락의 아래 끝이 화면(하단 바 위)에 들어왔는가 ────────
  useEffect(() => {
    if (phase !== "read" || typeof window === "undefined") return;
    const check = () => {
      const el = sentinelRef.current;
      if (!el) return;
      if (el.getBoundingClientRect().bottom <= window.innerHeight - BAR_H + 4) setSeen(true);
    };
    window.addEventListener("scroll", check, { passive: true });
    window.addEventListener("resize", check);
    let io = null;
    if (typeof IntersectionObserver !== "undefined" && sentinelRef.current) {
      io = new IntersectionObserver(check, { rootMargin: `0px 0px -${BAR_H}px 0px`, threshold: 0 });
      io.observe(sentinelRef.current);
    }
    const t1 = setTimeout(check, 400), t2 = setTimeout(check, 1500);   // 그림·패널이 늦게 펼쳐지는 경우
    return () => { window.removeEventListener("scroll", check); window.removeEventListener("resize", check); io?.disconnect(); clearTimeout(t1); clearTimeout(t2); };
  }, [phase, step]);

  // 새로 펼친 단락: 접힌 패널을 열어 주고(다 읽도록) 화면에 맞춘다
  useEffect(() => {
    if (phase !== "read" || typeof window === "undefined") return;
    const el = lastRef.current;
    if (!el) return;
    const raf = requestAnimationFrame(() => {
      try {
        const folded = el.querySelectorAll(".cv-pbtn:not(.on)");
        if (folded.length) { folded.forEach((b) => b.click()); setSeen(false); }   // 패널이 펼쳐져 길어졌으니 "끝까지 읽음" 을 다시 잰다
      } catch { /* 무시 */ }
      if (step > 0) {
        const top = el.getBoundingClientRect().top + window.scrollY - 12;
        try { window.scrollTo({ top, behavior: "smooth" }); } catch { window.scrollTo(0, top); }
      }
    });
    return () => cancelAnimationFrame(raf);
  }, [phase, step]);

  // too_fast 대기 해제
  useEffect(() => {
    if (!waitUntil) return;
    const t = setTimeout(() => setWaitUntil(0), Math.max(0, waitUntil - Date.now()) + 50);
    return () => clearTimeout(t);
  }, [waitUntil]);

  const fail = (e) => setToast(e?.status === 401 ? "로그인이 필요해요" : (e?.message || "연결이 불안정해요. 잠시 후 다시 시도해 주세요"));

  const submit = useCallback(async (ans, sess) => {
    setBusy(true);
    try {
      const arr = (sess?.items || []).map((it) => ({ item_id: it.id, ...(ans[it.id] || {}) }));
      const r = await completeReview(sess?.review_id ?? null, arr, readMsRef.current, { concept_id: concept.id, recent });
      if (r?.ok === false && r.reason === "too_fast") {
        const w = Math.max(1, Number(r.wait) || 5);
        setWaitUntil(Date.now() + w * 1000);
        setToast(`조금만 더 천천히 읽어요. ${w}초 뒤에 다시 제출할 수 있어요`);
      } else {
        setResult(r); setPhase("result"); scrollTop();
        if (r?.ok) onCompleted?.({ reward: r.reward || 0, drop_balance: r.drop_balance ?? null });
      }
    } catch (e) { fail(e); }
    setBusy(false);
  }, [concept?.id, recent, onCompleted]); // eslint-disable-line react-hooks/exhaustive-deps

  /** 복습 시작 — 서버에 기록을 만들고 문항(정답 없음)을 받아 둔 뒤 읽기 단계로 */
  const begin = async () => {
    if (busy) return;
    setBusy(true);
    try {
      const s = await startReview(concept.id, recent);
      setSession(s); setAnswers({}); setQi(0); setResult(null);
      readStartRef.current = Date.now(); readMsRef.current = 0;
      if (N > 0) { setStep(0); setPhase("read"); scrollTop(); }
      else if (s.items?.length) { setPhase("quiz"); scrollTop(); }
      else { await submit({}, s); return; }     // 읽을 단락도 낼 문제도 없으면 바로 완료 처리
    } catch (e) { fail(e); }
    setBusy(false);
  };

  const next = async () => {
    if (!timeOk || !seen || busy) return;
    if (step < N - 1) { setStep(step + 1); return; }
    readMsRef.current = Date.now() - readStartRef.current;
    if (!items.length) { await submit({}, session); return; }     // 낼 문제가 없으면 읽기만으로 완료
    setPhase("quiz"); setQi(0); scrollTop();
  };

  /** 오답 뒤 새 문제로 다시 도전 (읽기는 이미 했으므로 퀴즈부터) */
  const retry = async () => {
    if (busy) return;
    setBusy(true);
    try {
      const s = await startReview(concept.id, recent);
      setSession(s); setAnswers({}); setQi(0); setResult(null);
      if (!s.items?.length) { await submit({}, s); return; }
      setPhase("quiz"); scrollTop();
    } catch (e) { fail(e); }
    setBusy(false);
  };

  // 펼친 단락들 — 초 단위 카운트다운 렌더 때 단락 트리를 다시 그리지 않도록 같은 엘리먼트를 재사용한다
  const revealed = useMemo(() => (
    <div className="rv-blocks">
      {list.slice(0, step + 1).map((b, i) => (
        <div key={b?.id ?? i} className="rv-blk" ref={i === step ? lastRef : null}>{renderBlock(b, i)}</div>
      ))}
    </div>
  ), [list, step, renderBlock]);

  const setAns = (id, v) => setAnswers((a) => ({ ...a, [id]: v }));
  const answered = (it) => {
    const a = it && answers[it.id];
    if (!a) return false;
    return kindOf(it) === "choice" ? Number.isInteger(a.index) : !!(a.answer && a.answer.trim());
  };
  const allAnswered = items.length > 0 && items.every(answered);
  const label = rewardLabel(session || status);
  const waiting = waitUntil > Date.now();

  // ── 화면 ────────────────────────────────────────────────────────────────────
  let body = null;

  if (phase === "intro") {
    const remaining = status?.remaining ?? 0;
    const stat = !status ? "현황을 불러오는 중…"
      : status.ready === null ? "현황을 불러오지 못했어요. 복습은 그대로 할 수 있어요."
      : status.ready === false ? "보상 적립은 준비 중이에요. 지금은 복습만 할 수 있어요."
      : (status.today_done ?? 0) >= (status.today_cap ?? DAILY_CAP) ? `오늘 보상 ${status.today_done}/${status.today_cap}회를 모두 받았어요. 복습은 계속할 수 있지만 오늘은 보상이 없어요.`
      : remaining <= 0 ? `이 개념은 보상 횟수(${status.cap}회)를 모두 채웠어요. 복습은 계속할 수 있지만 보상은 없어요.`
      : null;
    const warn = !!stat && status?.ready === true;
    body = (
      <div className="sv-card">
        <div className="rv-head"><h3>🔁 복습 모드</h3>{label && <span className={"rv-tag" + (label.off ? " off" : "")}>{label.text}</span>}</div>
        <p className="sv-muted" style={{ margin: 0 }}>「{concept?.title}」을(를) 처음부터 끝까지 다시 읽고 퀴즈로 확인해요.</p>
        <ul className="rv-rules">
          <li><span className="no">1</span><span>단락을 <b>순서대로</b> 하나씩 펼쳐 읽어요. 한 단락에 4초 이상 머물고 끝까지 스크롤해야 다음으로 넘어가요.</span></li>
          <li><span className="no">2</span><span>다 읽으면 이 개념의 <b>퀴즈 3문제</b>를 풀어요. 답은 제출한 뒤 한꺼번에 확인돼요.</span></li>
          <li><span className="no">3</span><span><b>만점</b>이면 Ⓓ {REWARD}을 받아요. 틀리면 새 문제로 다시 도전할 수 있어요.</span></li>
        </ul>
        <div className={"rv-stat" + (warn ? " warn" : "")}>
          {stat ? <span>{stat}</span> : (
            <span>이 개념 남은 보상 <b>{remaining}회</b> (최근 읽은 순서 {status.rank}번째 · 최대 {status.cap}회) · 오늘 <b>{status.today_done}/{status.today_cap}</b></span>
          )}
        </div>
        <div className="rv-actions">
          <button className="sv-btn" onClick={onExit}>그냥 읽기</button>
          <button className="sv-btn pri" disabled={busy || !uid} onClick={begin}>{busy ? "준비 중…" : "복습 시작"}</button>
        </div>
        {!uid && <p className="rv-note">복습 모드는 로그인한 뒤에 쓸 수 있어요.</p>}
      </div>
    );
  }

  if (phase === "read") {
    const last = step >= N - 1;
    const hint = !timeOk ? `천천히 읽어요 (${left}초)` : !seen ? "끝까지 스크롤하면 넘어갈 수 있어요" : last ? "다 읽었어요!" : "다음 단락으로";
    body = (
      <>
        {!last && <p className="rv-more">단락 {step + 1}/{N} · 아래 「다음」을 누르면 이어져요</p>}
        <div className="rv-bar">
          <div className="rv-bar-in">
            <div className="rv-prog">
              <span className="lab">{step + 1} / {N}</span><span className="hint">{hint}</span>
              <div className="sv-bar"><i style={{ width: `${Math.round(((step + 1) / Math.max(1, N)) * 100)}%` }} /></div>
            </div>
            <button className="sv-btn pri" disabled={!timeOk || !seen || busy} onClick={next}>{last ? (busy ? "채점 중…" : "퀴즈 시작") : "다음"}</button>
          </div>
        </div>
      </>
    );
  }

  if (phase === "quiz") {
    const it = items[qi];
    const kind = it ? kindOf(it) : "short";
    const a = it ? answers[it.id] : null;
    const lastQ = qi >= items.length - 1;
    body = (
      <div className="sv-card">
        <div className="rv-quiz-top">
          <span><b>퀴즈 {qi + 1}/{items.length}</b>{it?.source === "check" ? " · 바로 확인" : ""}</span>
          <span className="rv-dots">{items.map((x, i) => <i key={x.id} className={(answered(x) ? "on" : "") + (i === qi ? " cur" : "")} />)}</span>
        </div>
        {it ? (
          <>
            <ItemQuestion item={it} index={qi} onSelect={kind === "choice" ? (i) => setAns(it.id, { index: i }) : undefined}
              selected={kind === "choice" ? (a?.index ?? null) : null} />
            {kind !== "choice" && (
              <div className="rv-short">
                <input className="sv-in" type="text" inputMode="text" autoComplete="off" autoCapitalize="off" autoCorrect="off" spellCheck={false} enterKeyHint="next"
                  placeholder="답 입력 (예: 3, 1/2, 60°, 2, 11)" value={a?.answer || ""}
                  onChange={(e) => setAns(it.id, { answer: e.target.value })}
                  onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); if (!lastQ && answered(it)) setQi(qi + 1); } }} />
              </div>
            )}
            <p className="rv-note">정답은 {items.length}문제를 모두 제출한 뒤 확인돼요. 답이 여러 개면 쉼표로 구분해요.</p>
          </>
        ) : <div className="sv-empty">문제를 불러오지 못했어요.</div>}
        <div className="rv-actions">
          <button className="sv-btn" disabled={qi === 0} onClick={() => setQi(qi - 1)}>이전</button>
          {!lastQ
            ? <button className="sv-btn pri" disabled={!answered(it)} onClick={() => setQi(qi + 1)}>다음 문제</button>
            : <button className="sv-btn pri" disabled={!allAnswered || busy || waiting} onClick={() => submit(answers, session)}>{busy ? "채점 중…" : waiting ? "잠시 뒤 제출" : "제출"}</button>}
        </div>
      </div>
    );
  }

  if (phase === "result" && result) {
    if (result.ok) {
      const r = result.reward || 0;
      const why = r > 0 ? null
        : result.ready === false ? "보상 준비 중 — 곧 Ⓓ 적립이 열려요"
        : result.reward_error ? "보상 지급이 잠시 지연되고 있어요. 나중에 다시 확인해 주세요"
        : (result.today_done ?? 0) >= (result.today_cap ?? DAILY_CAP) && result.remaining > 0 ? "오늘 보상 한도를 모두 채웠어요"
        : "이 개념의 보상 횟수를 모두 채웠어요";
      body = (
        <div className="sv-card rv-result">
          <h3>복습 완료!</h3>
          <p className="sv-muted" style={{ margin: 0 }}>{result.max > 0 ? `퀴즈 ${result.score}/${result.max} 만점이에요.` : "끝까지 다 읽었어요."}</p>
          <div className={"rv-drop" + (r > 0 ? "" : " none")}>
            {r > 0 ? <>Ⓓ +{r}<span className="sp">💧</span><span className="sp">💧</span><span className="sp">💧</span></> : why}
          </div>
          <div className="rv-lines">
            {result.drop_balance != null && <div>내 Ⓓ <b>{Number(result.drop_balance).toLocaleString()}</b></div>}
            {result.today_cap != null && <div>오늘 <b>{result.today_done}/{result.today_cap}</b></div>}
            {result.remaining != null && result.ready !== false && <div>이 개념 남은 보상 <b>{result.remaining}회</b></div>}
          </div>
          <div className="rv-actions">
            <button className="sv-btn" onClick={onExit}>개념으로 돌아가기</button>
            <button className="sv-btn pri" onClick={() => (location.hash = "#/learn/concept")}>다른 개념 복습</button>
          </div>
        </div>
      );
    } else {
      const wrongNos = (result.wrong || []).map((id) => items.findIndex((x) => x.id === id) + 1).filter((n) => n > 0);
      body = (
        <div className="sv-card rv-result">
          <h3>아쉬워요</h3>
          <p className="sv-muted" style={{ margin: 0 }}>퀴즈 {result.score}/{result.max} — 만점이어야 완료돼요.</p>
          <p className="rv-wrong">틀린 문제: <b>{wrongNos.length ? wrongNos.map((n) => `${n}번`).join(", ") : `${(result.max || 0) - (result.score || 0)}문제`}</b></p>
          <p className="rv-note">개념을 다시 읽고 오거나, 새 문제로 바로 다시 도전할 수 있어요. (정답은 알려 주지 않아요)</p>
          <div className="rv-actions">
            <button className="sv-btn" onClick={onExit}>개념 다시 읽기</button>
            <button className="sv-btn pri" disabled={busy} onClick={retry}>{busy ? "준비 중…" : "다시 도전"}</button>
          </div>
        </div>
      );
    }
  }

  return (
    <div className={`rv-root rv-${theme}`}>
      <style>{CSS}</style>
      {phase === "read" && (
        <>
          {revealed}
          <div ref={sentinelRef} className="rv-sentinel" />
        </>
      )}
      <div className="rv-kit">{body}</div>
      {toast && <div className="sv-toast">{toast}</div>}
    </div>
  );
}
