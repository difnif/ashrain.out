// ashrain.out — 서술형 평가 (/e · /e/<코드>) — 학생앱 셸 밖 단독 페이지. 로그인 여부와 무관하게 연다(로그인돼 있으면 계정에 바로 남는다).
//   /e            열린 평가 · 내 응시 목록
//   /e/<코드>     표지 → 문제 열람(종이와 대조) → 쪽마다 안내 따라 촬영(찍는 동안 앞 쪽은 판독·채점) → 2쪽 이름 확인 → 제출 → 결과
// 서버: api/_lib/assess.js (POST /api/photo task:"assess"). 사진 처리: src/lib/assess/capture.js. 대기열: src/lib/assess/queue.js
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import MathText from "../../components/MathText";
import { ASSESS_CSS } from "./assessCss";
import { assessCall, deviceId, readLocalFor, writeLocal, localSessions, addPendingClaim, markSeen, goAssess, accessToken, currentUid } from "../../lib/assess/api";
import { ClaimPrompt } from "./AssessCard";
import { processPhoto, REASON_TEXT } from "../../lib/assess/capture";
import { setQueueContext, enqueue, jobOf, retryJob, regrade, busyCount } from "../../lib/assess/queue";
import { invalidateAssessList } from "../../lib/assess/notify";
import { gradeLabel } from "../../lib/assess/spec";
import { studentPath } from "../../shared/roles";

const svgUrl = (svg) => "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
const fmtDate = (d) => { if (!d) return ""; const [, m, dd] = String(d).split("-"); return `${+m}월 ${+dd}일`; };
const fmtTime = (iso) => { try { const d = new Date(iso); return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; } catch { return ""; } };

function useCodeFromPath() {
  const read = () => decodeURIComponent((location.pathname.split("/")[2] || "").trim()).toUpperCase();
  const [code, setCode] = useState(read);
  useEffect(() => {
    const h = () => setCode(read());
    window.addEventListener("popstate", h);
    window.addEventListener("pathchange", h);
    return () => { window.removeEventListener("popstate", h); window.removeEventListener("pathchange", h); };
  }, []);
  return code;
}
function useTick(ev) {
  const [, set] = useState(0);
  useEffect(() => {
    const on = () => set((t) => t + 1);
    window.addEventListener(ev, on);
    return () => window.removeEventListener(ev, on);
  }, [ev]);
}

async function goApp() {
  const tok = await accessToken();
  const path = tok ? await studentPath("") : "/walking";
  history.pushState(null, "", path);
  window.dispatchEvent(new Event("pathchange"));
  window.scrollTo(0, 0);
}

function Top({ title, sub, onBack }) {
  return (
    <div className="as-top">
      <button className="as-ic" aria-label="뒤로" title="뒤로" onClick={onBack || (() => goApp())}>←</button>
      <div className="as-tt"><b>{title}</b>{sub && <small>{sub}</small>}</div>
    </div>
  );
}

export default function AssessApp({ theme = "light" }) {
  const code = useCodeFromPath();
  useEffect(() => { document.title = code ? `서술형 평가 ${code} · 애쉬레인` : "서술형 평가 · 애쉬레인"; }, [code]);
  return (
    <div className={`as-root as-${theme}`}>
      <style>{ASSESS_CSS}</style>
      <div className="as-wrap">{code ? <Take key={code} code={code} /> : <ListView />}</div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────── 목록
function ListView() {
  const [list, setList] = useState(null);
  const [err, setErr] = useState("");
  const [logged, setLogged] = useState(null);
  useEffect(() => {
    let alive = true;
    (async () => {
      const tok = await accessToken();
      if (alive) setLogged(!!tok);
      try { const r = await assessCall("list", { device: deviceId() }); if (alive) setList(r); }
      catch (e) { if (alive) { setErr(e.message); setList({ open: [], mine: [] }); } }
    })();
    return () => { alive = false; };
  }, []);
  const local = useMemo(() => localSessions(), []);
  const done = new Set((list?.mine || []).filter((m) => m.status === "submitted").map((m) => m.code));
  return (
    <>
      <Top title="서술형 평가" sub="선생님이 낸 시험지를 쪽마다 찍으면 채점돼요" />
      {logged && <ClaimPrompt className="as-card" btnClass="as-btn as-tiny" onClaimed={async () => { try { setList(await assessCall("list", { device: deviceId() })); } catch { /* */ } }} />}
      {!list && <div className="as-busy"><span className="as-sp" />불러오는 중…</div>}
      {list && (
        <>
          <p className="as-sec">지금 열린 평가</p>
          {list.open?.length ? (
            <div className="as-list">
              {list.open.map((s) => (
                <button key={s.code} className="as-item" onClick={() => { markSeen(s.code); goAssess(s.code); }}>
                  <span className="ic">📝</span>
                  <span className="tx"><b>{s.title}</b><small>{[fmtDate(s.date), s.grade_label, `${s.n_items}문제`].filter(Boolean).join(" · ")}</small></span>
                  <span className="rt">{done.has(s.code) ? "결과 →" : "열기 →"}</span>
                </button>
              ))}
            </div>
          ) : (
            <div className="as-card as-mut">지금 열린 서술형 평가가 없어요. 시험지 2쪽의 QR을 찍으면 그 평가가 바로 열려요.</div>
          )}
          {(list.mine?.length > 0 || (!logged && local.length > 0)) && <p className="as-sec">{logged ? "내 응시 기록" : "이 기기의 응시 기록"}</p>}
          <div className="as-list">
            {(logged ? list.mine : list.mine?.length ? list.mine : local.map((l) => ({ sid: l.sid, code: l.code, title: l.code, status: l.step === "result" ? "submitted" : "open" }))).map((m) => (
              <button key={m.sid} className="as-item" onClick={() => m.code && goAssess(m.code)}>
                <span className="ic">{m.status === "submitted" ? "✅" : "⏳"}</span>
                <span className="tx"><b>{m.title || m.code}</b><small>{m.status === "submitted" ? `제출 ${fmtTime(m.submitted_at)}` : "찍는 중 — 이어서 하기"}</small></span>
                <span className="rt">{m.status === "submitted" && m.max ? `${m.total}/${m.max}점` : "→"}</span>
              </button>
            ))}
          </div>
          {err && <div className="as-note bad">{err}</div>}
          {logged === false && <p className="as-small" style={{ marginTop: 14 }}>로그인하지 않아도 응시할 수 있어요. 결과를 내 기록에 모으려면 결과 화면에서 로그인하세요.</p>}
        </>
      )}
    </>
  );
}

// ─────────────────────────────────────────────────────────────── 응시
function Take({ code }) {
  const [load, setLoad] = useState({ busy: true, err: null });
  const [set, setSet] = useState(null);
  const [meta, setMeta] = useState({ store: false, anon: true, me: null, mine: null });
  const [sess, setSess] = useState(null);           // { sid, secret, status, pages, info, suggestion, userBound }
  const uidRef = useRef(undefined);                 // 지금 보는 사람(계정 id 또는 null) — 이 기기의 남의 기록은 쓰지 않는다
  const [step, setStep] = useState("cover");        // cover | view | shoot | wrap | result
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState("");
  useTick("ash:assess");

  useEffect(() => { if (!toast) return; const t = setTimeout(() => setToast(""), 3200); return () => clearTimeout(t); }, [toast]);

  // 평가 불러오기 + 이 기기 기록
  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [g, uid] = await Promise.all([assessCall("get", { code }), currentUid()]);
        if (!alive) return;
        uidRef.current = uid;
        setSet(g.set); setMeta({ store: !!g.store_images, anon: g.anon !== false, me: g.me, mine: g.mine || null });
        markSeen(code);
        const loc = readLocalFor(code, uid);
        if (loc?.sid && (loc?.secret || uid)) {                 // 계정 기록은 비밀값 없이도(로그인으로) 이어 간다
          if (loc.step === "result") {
            try { const r = await assessCall("result", { sid: loc.sid, secret: loc.secret }); if (!alive) return; setSess({ sid: loc.sid, secret: loc.secret, status: r.result.status, pages: [] }); setResult(r.result); setStep("result"); }
            catch { /* 기록이 사라졌으면 표지부터 */ }
          } else setSess({ sid: loc.sid, secret: loc.secret, status: "open", pages: [], local: true });
        }
        setLoad({ busy: false, err: null });
      } catch (e) { if (alive) setLoad({ busy: false, err: e.message }); }
    })();
    return () => { alive = false; };
  }, [code]);

  // 떠나려 할 때 분석 중이면 경고
  useEffect(() => {
    const h = (e) => { if (busyCount() > 0) { e.preventDefault(); e.returnValue = ""; } };
    window.addEventListener("beforeunload", h);
    return () => window.removeEventListener("beforeunload", h);
  }, []);

  const showResult = useCallback((res) => {
    setResult(res); setStep("result");
    if (res?.sid) writeLocal(code, { sid: res.sid, step: "result" }, uidRef.current);      // 지금 보는 사람의 칸에만
    invalidateAssessList();
    window.scrollTo(0, 0);
  }, [code]);

  /** 응시 시작·이어 하기. 이미 제출한 응시였으면(결과 응답을 놓친 경우 등) 결과로 간다 → true */
  const start = useCallback(async ({ fresh = false } = {}) => {
    const uid = uidRef.current !== undefined ? uidRef.current : await currentUid();
    const loc = fresh ? null : readLocalFor(code, uid);
    const r = await assessCall("start", { code, device: deviceId(), sid: loc?.sid, secret: loc?.secret, fresh });
    if (r.status === "submitted") {
      const rr = await assessCall("result", { sid: r.sid, secret: loc?.secret });
      writeLocal(code, { sid: r.sid, secret: loc?.secret, step: "result" }, uid);
      setSess({ sid: r.sid, secret: loc?.secret, status: "submitted", pages: [], userBound: !!r.user_bound });
      showResult(rr.result);
      return true;
    }
    const s = { sid: r.sid, secret: r.secret || loc?.secret, status: r.status, pages: r.pages || [], info: r.info, suggestion: r.suggestion || null, userBound: !!r.user_bound };
    writeLocal(code, { sid: s.sid, secret: s.secret, step: "shoot" }, uid);
    setQueueContext({ code, sid: s.sid, secret: s.secret });
    setSess(s);
    return false;
  }, [code, showResult]);

  const myResult = useCallback(async () => {
    const sid = meta.mine?.sid;
    if (!sid) return;
    const r = await assessCall("result", { sid });
    setSess({ sid, secret: null, status: "submitted", pages: [], userBound: true });
    showResult(r.result);
  }, [meta.mine?.sid, showResult]);

  if (load.busy) return <><Top title="서술형 평가" /><div className="as-busy"><span className="as-sp" />평가를 여는 중…</div></>;
  if (load.err) return (
    <>
      <Top title="서술형 평가" />
      <div className="as-card as-err"><div className="ic">🔎</div><h2>{load.err}</h2>
        <p className="as-mut">시험지 2쪽 QR을 다시 찍거나, 선생님께 평가 코드를 확인해 주세요.</p>
        <div className="as-row"><button className="as-btn" onClick={() => goAssess("")}>열린 평가 보기</button></div></div>
    </>
  );

  const sub = [fmtDate(set.date), set.grade_label, `${set.n_items ?? set.items.length}문제`].filter(Boolean).join(" · ");
  return (
    <>
      <Top title={set.title} sub={sub} onBack={step === "view" ? () => setStep("cover") : step === "shoot" || step === "wrap" ? () => setStep("view") : undefined} />
      {step === "cover" && <Cover set={set} meta={meta} sess={sess} onGo={() => { setStep("view"); window.scrollTo(0, 0); }}
        onResume={async () => { try { if (!(await start())) setStep("shoot"); } catch (e) { setToast(e.message); } }}
        onMyResult={async () => { try { await myResult(); } catch (e) { setToast(e.message); } }} />}
      {step === "view" && <Viewer set={set} onStart={async () => {
        try { if (!(await start())) { setStep("shoot"); window.scrollTo(0, 0); } } catch (e) { setToast(e.message); }
      }} />}
      {(step === "shoot" || step === "wrap") && sess && (
        <Shoot set={set} meta={meta} sess={sess} setSess={setSess} wrap={step === "wrap"} setToast={setToast}
          onAllCaptured={() => { setStep("wrap"); window.scrollTo(0, 0); }} onBackToShoot={() => setStep("shoot")} onSubmitted={showResult} />
      )}
      {step === "result" && result && <ResultView set={set} result={result} sess={sess} setToast={setToast} onRetake={async () => {
        // 새 응시가 만들어진 뒤에만 이 기기의 기록을 바꾼다(실패하면 지금 결과 기록을 그대로 둔다)
        try { if (!(await start({ fresh: true }))) { setResult(null); setStep("view"); } } catch (e) { setToast(e.message); }
      }} />}
      {toast && <div style={{ position: "fixed", left: "50%", transform: "translateX(-50%)", bottom: 22, zIndex: 50, maxWidth: "min(480px, calc(100vw - 28px))" }}
        className="as-note bad" role="alert">{toast}</div>}
    </>
  );
}

// ── 표지 ─────────────────────────────────────────────────────────────────────
function Cover({ set, meta, sess, onGo, onResume, onMyResult }) {
  const closed = set.state !== "open";
  const nItems = set.n_items ?? set.items.length;
  const pts = set.max ?? set.items.reduce((a, it) => a + it.points, 0);
  const done = meta.mine?.status === "submitted";                          // 로그인: 이 평가의 마지막 응시를 이미 제출함(다른 기기에서 등)
  const canResume = !done && (!!sess?.sid || meta.mine?.status === "open");  // 마감 뒤에도 — 제출해 둔 기록이면 결과로 간다
  return (
    <div className="as-card">
      <p className="as-kick">서술형 평가 · {set.code}</p>
      <h2>{set.title}</h2>
      <div className="as-facts">
        {set.date && <span className="as-chip">🗓 {fmtDate(set.date)}</span>}
        {set.grade_label && <span className="as-chip">🎒 {set.grade_label}</span>}
        <span className="as-chip">📝 {nItems}문제 · {pts}점</span>
        {set.open_book && <span className="as-chip">📖 오픈북</span>}
        <span className="as-chip">📄 {set.n_pages ?? set.pages.length}쪽</span>
      </div>
      <p className="as-mut" style={{ marginTop: 10 }}>
        종이에 다 풀었으면, 먼저 화면의 문제가 내 시험지와 같은지 확인하고 <b>1쪽부터 한 장씩</b> 찍어요. 찍는 동안 앞 쪽은 바로 채점돼요.
      </p>
      {meta.me ? (
        <div className="as-note info">👤 <span><b>{meta.me.name || meta.me.nick || "내 계정"}</b>으로 응시해요 — 결과가 내 기록에 남아요.</span></div>
      ) : (
        <div className="as-note info">🔓 <span>로그인 없이 응시해요. 2쪽에 쓴 <b>이름·학년</b>으로 선생님께 결과가 전달돼요.</span></div>
      )}
      {closed && <div className="as-note warn">⏰ {set.state === "soon" ? "아직 열리지 않은 평가예요." : "마감된 평가예요 — 새로 찍을 수 없어요."}</div>}
      {!meta.me && !meta.anon && <div className="as-note warn">🔒 이 평가는 로그인한 뒤 응시할 수 있어요.</div>}
      <div className="as-row">
        {done && <button className="as-btn pri" onClick={onMyResult}>내 결과 보기</button>}
        {canResume && <button className="as-btn pri" onClick={onResume}>{closed ? "내 기록 보기" : "이어서 찍기"}</button>}
        <button className={"as-btn" + (canResume || done ? "" : " pri")} disabled={closed || (!meta.me && !meta.anon)} onClick={onGo}>{done ? "다시 응시하기" : "문제 보고 시작하기"}</button>
      </div>
      {meta.store && <p className="as-small" style={{ marginTop: 10 }}>찍은 쪽 사진은 채점 확인과 판독 개선을 위해 선생님께 보관돼요.</p>}
    </div>
  );
}

// ── 문제 열람(종이와 대조) ───────────────────────────────────────────────────
export function ProblemCard({ it }) {
  return (
    <div className="as-q">
      <div className="as-qh"><span className="as-qn">문제 {it.no}</span>{it.topic && <span className="as-qt">{it.topic}</span>}<span className="as-qp">{it.page}쪽 · {it.points}점</span></div>
      <div className="as-qbody">
        {it.story && <MathText as="div" text={it.story} />}
        {it.conditions?.length > 0 && <ul className="conds">{it.conditions.map((c, i) => <li key={i}><MathText text={c} /></li>)}</ul>}
        {it.figure_svg && <div className="as-fig"><img src={svgUrl(it.figure_svg)} alt={`문제 ${it.no} 그림`} /></div>}
        {it.ask && <MathText as="div" className="ask" text={it.ask} />}
      </div>
      <div className="as-els">{it.elements.map((e) => <span key={e.no}>{"①②③④⑤"[e.no - 1] || e.no} {e.element} {e.points}점</span>)}</div>
    </div>
  );
}

function Viewer({ set, onStart }) {
  const [ok, setOk] = useState(false);
  const [busy, setBusy] = useState(false);
  const [diff, setDiff] = useState(false);
  return (
    <>
      <div className="as-card">
        <h3>📄 내 시험지와 같은지 확인해요</h3>
        <p className="as-mut" style={{ margin: 0 }}>종이를 옆에 두고 문제를 하나씩 맞춰 보세요. 서두르지 않아도 돼요 — 확인이 끝나면 아래에서 촬영을 시작해요.</p>
      </div>
      {set.items.map((it) => <ProblemCard key={it.no} it={it} />)}
      <label className="as-check"><input type="checkbox" checked={ok} onChange={(e) => setOk(e.target.checked)} />내 시험지와 문제가 같아요</label>
      <div className="as-row">
        <button className="as-btn pri" disabled={!ok || busy} onClick={async () => { setBusy(true); try { await onStart(); } finally { setBusy(false); } }}>{busy ? "준비하는 중…" : "📷 촬영 시작"}</button>
        <button className="as-btn ghost" onClick={() => setDiff((v) => !v)}>시험지가 달라요</button>
      </div>
      {diff && <div className="as-note warn">🙋 <span>다른 날 시험지이거나 다른 반 시험지일 수 있어요. 시험지 2쪽 QR을 다시 찍어 보고, 그래도 다르면 선생님께 알려 주세요. (평가 코드 <b>{set.code}</b>)</span></div>}
    </>
  );
}

// ── 쪽 그림 (안내용) ────────────────────────────────────────────────────────
function PageArt({ kind }) {
  return (
    <svg className="as-art" viewBox="0 0 100 141" aria-hidden="true">
      <rect x="1" y="1" width="98" height="139" rx="4" fill="var(--card)" stroke="currentColor" strokeOpacity=".35" />
      {[[6, 6], [86, 6], [86, 127], [6, 127]].map(([x, y], i) => <rect key={i} x={x} y={y} width="8" height="8" fill="currentColor" />)}
      <rect x="15.5" y="6" width="3" height="8" fill="currentColor" />
      {Array.from({ length: 14 }, (_, i) => <rect key={i} x={30.8 + i * 2.8} y={130.5} width="2" height="2" fill={[2, 4, 9, 11].includes(i) ? "currentColor" : "none"} stroke="currentColor" strokeWidth=".3" strokeOpacity=".7" />)}
      <rect x="30" y="7" width="40" height="4" rx="1" fill="currentColor" opacity=".5" />
      {kind === "guide" && [22, 30, 38, 52, 60, 68, 82, 90, 98, 106, 114].map((y, i) => <rect key={i} x="8" y={y} width={i % 3 === 2 ? 58 : 84} height="3" rx="1" fill="currentColor" opacity=".25" />)}
      {kind === "info" && (<>
        <rect x="30" y="20" width="18" height="18" fill="currentColor" opacity=".55" />
        <rect x="8" y="44" width="34" height="9" rx="1.5" fill="none" stroke="var(--ac)" strokeWidth="1.6" />
        <rect x="46" y="44" width="46" height="9" rx="1.5" fill="none" stroke="var(--ac)" strokeWidth="1.6" />
        <rect x="8" y="58" width="84" height="44" rx="2" fill="none" stroke="currentColor" strokeOpacity=".5" />
        {[66, 78, 90].map((y) => <rect key={y} x="12" y={y} width="76" height="2.5" fill="currentColor" opacity=".25" />)}
        <rect x="8" y="106" width="84" height="8" rx="1.5" fill="none" stroke="currentColor" strokeOpacity=".5" />
      </>)}
      {kind === "item" && (<>
        <rect x="6" y="19" width="88" height="26" rx="2" fill="none" stroke="currentColor" strokeOpacity=".55" />
        {[25, 31, 37].map((y) => <rect key={y} x="10" y={y} width="70" height="2.5" fill="currentColor" opacity=".25" />)}
        <rect x="6" y="48" width="88" height="22" rx="2" fill="none" stroke="var(--ac)" strokeWidth="1.6" />
        <rect x="6" y="73" width="88" height="36" rx="2" fill="none" stroke="var(--ac)" strokeWidth="1.6" />
        <rect x="6" y="112" width="88" height="12" rx="2" fill="none" stroke="var(--ac)" strokeWidth="1.6" />
      </>)}
    </svg>
  );
}

function guideOf(set, page, nextNo = null) {
  if (page.kind === "guide") return { title: `${page.no}쪽 · 학생 확인 사항`, sub: "카메라 연습", lines: [
    "시험지를 평평한 곳에 놓고, 바로 위에서 찍어요.",
    "네 귀퉁이의 ■ 네 개와 아래 가운데 작은 네모 줄이 모두 화면에 들어오게.",
    "그림자가 지지 않게 밝은 곳에서 — 이 쪽이 잘 찍히면 나머지도 똑같이 찍으면 돼요."] };
  if (page.kind === "info") return { title: `${page.no}쪽 · 이름·학년`, sub: "응시자 확인", lines: [
    "이 쪽의 이름·학년 글씨로 누가 응시했는지 확인해요.",
    "이름 칸과 필적 확인 줄이 또렷하게 나오게 찍어요.",
    "찍고 나면 읽은 이름이 맞는지 한 번 물어볼게요."] };
  const it = set.items.find((x) => x.no === page.item);
  return { title: `${page.no}쪽 · 문제 ${page.item}`, sub: it?.topic || "", lines: [
    "①②③ 세 칸이 모두 들어오게 찍어요.",
    "줄을 그어 고친 곳은 그대로 두세요 — 그은 곳은 채점하지 않아요(감점 없음).",
    nextNo ? `찍고 나면 바로 ${nextNo}쪽으로 넘어가요. 이 쪽은 그동안 채점돼요.` : "이 쪽이 마지막이에요! 찍고 나면 채점 결과를 기다려요."] };
}

// ── 촬영 · 마무리 ────────────────────────────────────────────────────────────
function Shoot({ set, meta, sess, setSess, wrap, setToast, onAllCaptured, onBackToShoot, onSubmitted }) {
  const camRef = useRef(null), albRef = useRef(null);
  const [cur, setCur] = useState(null);         // 지금 찍을 쪽 번호
  const [pinned, setPinned] = useState(false);  // 사용자가 고른 쪽(다시 찍기) — 찍기 전까지 자동으로 넘기지 않는다
  const [proc, setProc] = useState(false);
  const [fail, setFail] = useState(null);       // { reason, page }
  const [flash, setFlash] = useState(null);     // { page, thumb, note }
  const [ask, setAsk] = useState(null);         // { r, expected } — 이미 찍은 다른 쪽이 나왔을 때 바꿀지 묻기
  const lastFile = useRef(null);                // 품질에서 걸린 사진 — '이대로 보내기'용
  const serverPages = useMemo(() => new Map((sess.pages || []).map((p) => [p.no, p])), [sess.pages]);
  useTick("ash:assess");

  // 이어 하기: 서버 기록 새로 받기(로컬 기록만 있던 경우)
  useEffect(() => {
    setQueueContext({ code: set.code, sid: sess.sid, secret: sess.secret });
  }, [set.code, sess.sid, sess.secret]);

  const state = (no) => {
    const j = jobOf(no);
    if (j) {
      if (j.status === "error") return "err";
      if (j.status === "done") return "done";
      return "busy";
    }
    const sp = serverPages.get(no);
    if (sp) {
      if (sp.kind === "guide") return "done";
      if (sp.status === "reading" || sp.status === "error") return "todo";     // 끊긴 판독 — 다시 찍기
      if (sp.kind === "info") return "done";
      return sp.status === "graded" ? "done" : "read";
    }
    return "todo";
  };
  const captured = (no) => ["done", "busy", "read"].includes(state(no));
  const missing = set.pages.filter((p) => !captured(p.no) && state(p.no) !== "err").map((p) => p.no);
  const errPages = set.pages.filter((p) => state(p.no) === "err").map((p) => p.no);

  useEffect(() => {
    if (pinned) return;
    if (cur == null || (captured(cur) && !fail)) {
      const next = set.pages.find((p) => !captured(p.no));
      const to = next ? next.no : set.pages[set.pages.length - 1].no;
      if (to !== cur) setCur(to);
    }
  }); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!wrap && !pinned && !proc && set.pages.every((p) => captured(p.no))) { const t = setTimeout(onAllCaptured, flash ? 1100 : 250); return () => clearTimeout(t); }
  });

  const page = set.pages.find((p) => p.no === cur) || set.pages[0];
  const nextMissing = set.pages.find((p) => p.no !== page.no && !captured(p.no))?.no || null;
  const g = guideOf(set, page, nextMissing);

  /** 확인된 사진을 대기열에 넣고 다음 쪽으로 */
  const accept = (r, expected) => {
    const before = captured(r.page);              // 넣기 전에 판단해야 한다(넣고 나면 늘 '찍은 쪽')
    enqueue(r.page, r.kind, { crop: r.crop, image: r.image, quality: r.quality }, r.thumb);
    const note = r.page === expected ? (before ? `${r.page}쪽을 새 사진으로 바꿨어요` : `${r.page}쪽을 받았어요`)
      : (before ? `${r.page}쪽을 새 사진으로 바꿨어요` : `${expected}쪽이 아니라 ${r.page}쪽이었어요 — ${r.page}쪽으로 받았어요`);
    setFlash({ page: r.page, thumb: r.thumb, note });
    setTimeout(() => setFlash((f) => (f && f.page === r.page ? null : f)), 1800);
    if (r.page === expected) {
      setPinned(false);
      const next = set.pages.find((p) => p.no !== r.page && !captured(p.no));
      if (next) setCur(next.no);
    }
  };
  const onFile = async (file, { force = false } = {}) => {
    if (!file) return;
    setProc(true); setFail(null); setFlash(null); setAsk(null);
    try {
      const r = await processPhoto(file, set, { wantImage: meta.store, skipQuality: force });
      if (!r.ok) { lastFile.current = ["blur", "flat", "dark"].includes(r.reason) ? file : null; setFail({ reason: r.reason, page: r.page || null }); return; }
      lastFile.current = null;
      const expected = page.no;
      // 찍으려던 쪽이 아니라 이미 찍은 다른 쪽이면, 잘 찍힌 사진을 말없이 바꾸지 않고 물어본다
      if (r.page !== expected && captured(r.page)) { setAsk({ r, expected }); return; }
      accept(r, expected);
    } catch (e) {
      setFail({ reason: "open", msg: e?.message });
    } finally { setProc(false); }
  };

  const steps = (
    <div className="as-steps" role="list">
      {set.pages.map((p) => {
        const st = state(p.no);
        const cls = p.no === cur && !wrap ? "cur" : st === "done" ? "done" : st === "busy" || st === "read" ? "busy" : st === "err" ? "err" : "";
        return (
          <button key={p.no} role="listitem" className={"as-st " + cls} onClick={() => { setCur(p.no); setPinned(true); setFail(null); if (wrap) onBackToShoot(); }}
            title={`${p.no}쪽`} aria-label={`${p.no}쪽 ${st === "done" ? "완료" : st === "err" ? "다시 찍기 필요" : st === "todo" ? "아직" : "채점 중"}`}>
            {st === "done" ? "✓" : st === "err" ? "!" : p.no}
            <small>{p.kind === "guide" ? "안내" : p.kind === "info" ? "이름" : `문${p.item}`}</small>
          </button>
        );
      })}
    </div>
  );

  if (wrap) return <>{steps}<Wrap set={set} sess={sess} setSess={setSess} state={state} errPages={errPages} missing={missing} setToast={setToast}
    onRetake={(no) => { setCur(no); setPinned(true); onBackToShoot(); }} onSubmitted={onSubmitted} /></>;

  return (
    <>
      {steps}
      <div className="as-card">
        <div className="as-shoot">
          <PageArt kind={page.kind} />
          <div>
            <p className="as-kick">{page.no} / {set.pages.length}쪽{g.sub ? ` · ${g.sub}` : ""}</p>
            <h3 style={{ marginBottom: 2 }}>{g.title}</h3>
            <ul className="as-gl">{g.lines.map((l, i) => <li key={i}>{l}</li>)}</ul>
          </div>
        </div>
        <input ref={camRef} type="file" accept="image/*" capture="environment" hidden onChange={(e) => { onFile(e.target.files?.[0]); e.target.value = ""; }} />
        <input ref={albRef} type="file" accept="image/*" hidden onChange={(e) => { onFile(e.target.files?.[0]); e.target.value = ""; }} />
        {proc ? <div className="as-busy"><span className="as-sp" />사진을 반듯하게 펴고 몇 쪽인지 확인하는 중…</div> : (
          <button className="as-cam" onClick={() => camRef.current?.click()}>
            <span className="ic">📷</span><b>{page.no}쪽 찍기</b><small>{captured(page.no) ? "이미 찍었어요 — 다시 찍으면 새 사진으로 바꿔요" : "카메라가 열려요"}</small>
          </button>
        )}
        {!proc && <div className="as-row" style={{ marginTop: 8 }}><button className="as-btn ghost as-tiny" onClick={() => albRef.current?.click()}>앨범에서 고르기</button></div>}
        {fail && (
          <div className="as-note bad" role="alert">📸 <span style={{ flex: 1 }}>{fail.reason === "other" && fail.page ? REASON_TEXT.other : REASON_TEXT[fail.reason] || fail.msg || "다시 찍어 주세요."}</span>
            {lastFile.current && <button className="as-btn as-tiny" onClick={() => onFile(lastFile.current, { force: true })}>이대로 보내기</button>}
          </div>
        )}
        {ask && (
          <div className="as-note warn" role="alert">🔁 <span style={{ flex: 1 }}>{ask.expected}쪽이 아니라 이미 찍은 <b>{ask.r.page}쪽</b>이 찍혔어요. {ask.r.page}쪽을 이 사진으로 바꿀까요?</span>
            <span style={{ display: "flex", gap: 6 }}>
              <button className="as-btn as-tiny" onClick={() => { const a = ask; setAsk(null); accept(a.r, a.expected); }}>바꾸기</button>
              <button className="as-btn as-tiny ghost" onClick={() => setAsk(null)}>그대로 두기</button>
            </span>
          </div>
        )}
        {flash && <div className="as-flash">{flash.thumb && <img src={flash.thumb} alt="" />}<span>✓ {flash.note}</span></div>}
      </div>
      <QueueNote set={set} state={state} />
    </>
  );
}

function QueueNote({ set, state }) {
  const items = set.pages.filter((p) => p.kind !== "guide");
  const done = items.filter((p) => state(p.no) === "done").length;
  const busy = items.filter((p) => ["busy", "read"].includes(state(p.no))).length;
  if (!busy && !done) return null;
  return (
    <div className="as-card">
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, fontWeight: 800 }}>
        <span>{busy ? "앞 쪽을 채점하는 중" : "찍은 쪽 채점 완료"}</span><span>{done}/{items.length}</span>
      </div>
      <div className="as-prog"><i style={{ width: `${Math.round((done / Math.max(1, items.length)) * 100)}%` }} /></div>
      <p className="as-small" style={{ margin: 0 }}>다음 쪽을 찍는 동안 앞 쪽은 뒤에서 판독·채점돼요. 모든 쪽이 끝날 때까지 이 화면을 닫지 마세요.</p>
    </div>
  );
}

function Wrap({ set, sess, setSess, state, errPages, missing, setToast, onRetake, onSubmitted }) {
  const [busy, setBusy] = useState(false);
  const [force, setForce] = useState(false);
  const itemPages = set.pages.filter((p) => p.kind === "item");
  const graded = itemPages.filter((p) => state(p.no) === "done").length;
  const pending = itemPages.filter((p) => ["busy", "read"].includes(state(p.no)));
  const infoPage = set.pages.find((p) => p.kind === "info");
  const infoJob = infoPage ? jobOf(infoPage.no) : null;
  const suggestion = infoJob?.result?.suggestion || sess.suggestion || null;
  const infoReady = !!sess.info?.name;
  const needInfo = !infoReady && !sess.userBound;          // 계정 응시면 이름 확인 없이도(프로필 이름) — 서버와 같은 기준
  const allDone = graded === itemPages.length && !errPages.length && !missing.length;

  // 판독만 되고 채점이 안 된 쪽(이어 하기 등)은 채점을 다시 건다
  useEffect(() => {
    for (const p of itemPages) if (state(p.no) === "read" && !jobOf(p.no)) regrade(p.no);
  }); // eslint-disable-line react-hooks/exhaustive-deps

  const submit = async () => {
    setBusy(true);
    try {
      const r = await assessCall("finish", { sid: sess.sid, secret: sess.secret, force: !allDone && force });
      onSubmitted(r.result);
    } catch (e) { setToast(e.message); } finally { setBusy(false); }
  };
  return (
    <>
      <div className="as-card">
        <h3>{allDone ? "✅ 채점이 끝났어요" : "⏳ 채점하는 중이에요"}</h3>
        <div className="as-prog"><i style={{ width: `${Math.round((graded / Math.max(1, itemPages.length)) * 100)}%` }} /></div>
        <p className="as-small" style={{ margin: 0 }}>문제 {graded}/{itemPages.length} 채점 완료{pending.length ? ` · ${pending.map((p) => `문제 ${p.item}`).join(", ")} 채점 중` : ""}</p>
        {errPages.map((no) => {
          const j = jobOf(no);
          return (
            <div key={no} className="as-note bad">⚠ <span style={{ flex: 1 }}><b>{no}쪽</b> — {j?.error || "다시 찍어 주세요"}</span>
              <span style={{ display: "flex", gap: 6 }}>
                {j?.payload || j?.gradeOnly ? <button className="as-btn as-tiny" onClick={() => retryJob(no)}>다시 보내기</button> : null}
                <button className="as-btn as-tiny" onClick={() => onRetake(no)}>다시 찍기</button>
              </span>
            </div>
          );
        })}
        {missing.length > 0 && <div className="as-note warn">📄 아직 안 찍은 쪽: {missing.map((n) => `${n}쪽`).join(", ")} <button className="as-btn as-tiny" style={{ marginLeft: "auto" }} onClick={() => onRetake(missing[0])}>찍으러 가기</button></div>}
      </div>
      {infoPage && <InfoCard set={set} sess={sess} setSess={setSess} suggestion={suggestion} reading={!suggestion && ["busy"].includes(state(infoPage.no))} setToast={setToast} />}
      <div className="as-card">
        {!allDone && <label className="as-check" style={{ marginTop: 0 }}><input type="checkbox" checked={force} onChange={(e) => setForce(e.target.checked)} />채점이 안 된 문제는 0점으로 하고 지금 제출할게요</label>}
        <button className="as-btn pri wide" style={{ marginTop: allDone ? 0 : 10 }} disabled={busy || (!allDone && !force) || needInfo} onClick={submit}>
          {busy ? "제출하는 중…" : "제출하고 결과 보기"}</button>
        {needInfo && <p className="as-small" style={{ margin: "8px 0 0" }}>위에서 2쪽 이름·학년을 확인하면 제출할 수 있어요.</p>}
      </div>
    </>
  );
}

function InfoCard({ set, sess, setSess, suggestion, reading, setToast }) {
  const lv = set.level || "mid";
  const maxG = lv === "elem" ? 6 : 3;
  const sugGrade = suggestion?.grade ? String(suggestion.grade).replace(/^[emh]/, "") : "";
  const [edit, setEdit] = useState(false);
  const [name, setName] = useState(suggestion?.name || "");
  const [grade, setGrade] = useState(sugGrade);
  const [nick, setNick] = useState(suggestion?.nickname || "");
  const [busy, setBusy] = useState(false);
  useEffect(() => { if (!edit && suggestion) { setName(suggestion.name || ""); setGrade(sugGrade); setNick(suggestion.nickname || ""); } }, [suggestion?.name, suggestion?.grade, suggestion?.nickname]); // eslint-disable-line react-hooks/exhaustive-deps
  const save = async (n = name, gr = grade, nk = nick) => {
    setBusy(true);
    try {
      const r = await assessCall("info", { sid: sess.sid, secret: sess.secret, name: n, grade: gr, nickname: nk });
      setSess((s) => ({ ...s, info: r.info })); setEdit(false);
    } catch (e) { setToast(e.message); } finally { setBusy(false); }
  };
  if (sess.info?.name && !edit) return (
    <div className="as-card">
      <h3>👤 응시자</h3>
      <p style={{ margin: 0, fontWeight: 800 }}>{gradeLabel(sess.info.grade)} · {sess.info.name}{sess.info.nickname ? ` (${sess.info.nickname})` : ""}</p>
      <div className="as-row"><button className="as-btn as-tiny" onClick={() => setEdit(true)}>고치기</button></div>
    </div>
  );
  if (reading) return <div className="as-card"><h3>👤 2쪽 이름을 읽는 중</h3><div className="as-busy"><span className="as-sp" />잠깐만요…</div></div>;
  const ask = suggestion && !edit && suggestion.name;
  return (
    <div className="as-card">
      <h3>👤 2쪽에 쓴 이름이 맞나요?</h3>
      {ask ? (
        <>
          <p style={{ margin: 0, fontSize: 17, fontWeight: 900 }}>{suggestion.grade ? gradeLabel(suggestion.grade) + " · " : ""}{suggestion.name}{suggestion.nickname ? ` (${suggestion.nickname})` : ""}</p>
          <div className="as-row">
            <button className="as-btn pri" disabled={busy || !suggestion.grade} onClick={() => save(suggestion.name, sugGrade, suggestion.nickname || "")}>맞아요</button>
            <button className="as-btn" onClick={() => setEdit(true)}>고칠게요</button>
          </div>
          {!suggestion.grade && <p className="as-small" style={{ margin: "6px 0 0" }}>학년을 읽지 못했어요 — '고칠게요'에서 골라 주세요.</p>}
        </>
      ) : (
        <>
          {!suggestion && <p className="as-small" style={{ margin: 0 }}>2쪽 글씨를 읽지 못했어요. 시험지에 쓴 그대로 적어 주세요.</p>}
          <div className="as-form">
            <label>학년<select value={grade} onChange={(e) => setGrade(e.target.value)}>
              <option value="">고르기</option>{Array.from({ length: maxG }, (_, i) => <option key={i} value={String(i + 1)}>{lv === "elem" ? "초등" : lv === "high" ? "고" : "중"} {i + 1}학년</option>)}</select></label>
            <label>이름<input value={name} onChange={(e) => setName(e.target.value)} maxLength={20} placeholder="시험지에 쓴 이름" /></label>
            <label className="full">닉네임 (선택)<input value={nick} onChange={(e) => setNick(e.target.value)} maxLength={20} placeholder="안 썼으면 비워 두기" /></label>
          </div>
          <div className="as-row"><button className="as-btn pri" disabled={busy || !name.trim() || !grade} onClick={() => save()}>{busy ? "저장하는 중…" : "확인"}</button></div>
        </>
      )}
    </div>
  );
}

// ── 결과 ─────────────────────────────────────────────────────────────────────
function ResultView({ set, result, sess, setToast, onRetake }) {
  const [res, setRes] = useState(result);
  const [logged, setLogged] = useState(null);
  useEffect(() => { accessToken().then((t) => setLogged(!!t)); }, []);
  const pct = res.max ? Math.round((res.total / res.max) * 100) : 0;
  const flag = async (no, note) => {
    try { await assessCall("flag", { sid: sess.sid, secret: sess.secret, page_no: set.items.find((x) => x.no === no)?.page, note });
      setRes((r) => ({ ...r, items: r.items.map((x) => (x.no === no ? { ...x, flagged: true } : x)) })); setToast(""); }
    catch (e) { setToast(e.message); }
  };
  const login = () => {
    addPendingClaim(sess.sid, sess.secret, { code: set.code, title: set.title, name: res.info?.name || "" });   // 로그인 뒤 "내 것이 맞아요"를 눌러야 담긴다
    history.pushState(null, "", "/walking"); window.dispatchEvent(new Event("pathchange"));
  };
  return (
    <>
      <div className="as-card">
        <p className="as-kick">결과{res.info?.name ? ` · ${gradeLabel(res.info.grade)} ${res.info.name}` : ""}</p>
        <div className="as-score"><b>{res.total}</b><span>/ {res.max}점</span></div>
        <div className="as-prog"><i style={{ width: `${pct}%` }} /></div>
        <p className="as-small" style={{ margin: 0 }}>{res.graded < res.n_items ? `채점된 문제 ${res.graded}/${res.n_items} — 채점되지 않은 문제는 0점이에요. ` : ""}AI가 읽은 내 풀이와 채점 근거를 문제마다 확인할 수 있어요. 잘못 읽었으면 알려 주세요 — 선생님이 다시 봐요.</p>
        {!res.reveal && res.reveal_policy !== "never" && <div className="as-note info">🔐 <span>{res.reveal_policy === "after_submit" && !res.complete
          ? "채점되지 않은 문제가 있어서, 정답과 모범 풀이·채점 근거는 평가가 마감되면 볼 수 있어요."
          : "정답과 모범 풀이·채점 근거는 평가가 마감되면 볼 수 있어요."}</span></div>}
      </div>
      {res.items.map((it) => <ResultItem key={it.no} it={it} set={set} onFlag={flag} />)}
      <div className="as-card">
        {logged === false && (
          <>
            <h3>🗂 내 기록에 담기</h3>
            <p className="as-small" style={{ margin: 0 }}>로그인한 뒤 "내 것이 맞아요"를 누르면 이 결과가 내 계정 기록으로 옮겨져요(30분 안에). 로그인하지 않아도 선생님께는 2쪽 이름으로 전달돼요.</p>
            <div className="as-row"><button className="as-btn pri" onClick={login}>로그인하고 담기</button></div>
          </>
        )}
        <div className="as-row">
          {logged && <button className="as-btn pri" onClick={() => goApp()}>대시보드로</button>}
          <button className="as-btn" onClick={() => goAssess("")}>다른 평가 보기</button>
          {!res.reveal && set.state === "open" && <button className="as-btn ghost" onClick={onRetake}>처음부터 다시 응시</button>}
        </div>
      </div>
    </>
  );
}

function ReadBox({ label, box }) {
  if (!box) return null;
  return (
    <div className="bx"><i>{label}</i>
      {box.lines?.length ? box.lines.map((l, i) => <div key={i} className={l.struck ? "st" : ""}>{l.arrow ? "→ " : ""}{l.t}</div>) : <span className="as-mut">(비어 있음)</span>}
    </div>
  );
}

function ResultItem({ it, set, onFlag }) {
  const [fl, setFl] = useState(false);
  const [note, setNote] = useState("");
  const q = set.items.find((x) => x.no === it.no);
  return (
    <div className="as-res">
      <div className="hd"><span className="as-qn">문제 {it.no}</span><span className="as-qt">{it.topic}</span>
        <span className="pt">{it.graded ? it.got : "–"}<small> / {it.max}</small></span></div>
      {!it.captured && <div className="as-note warn">📄 이 쪽을 찍지 않았어요.</div>}
      {it.captured && !it.graded && <div className="as-note warn">⏳ 채점되지 않았어요.</div>}
      {it.graded && (
        <div className="as-els2">
          {it.elements.map((e) => (
            <div key={e.no} className="as-el"><b>{"①②③④⑤"[e.no - 1] || e.no} {e.element}</b><span className="g">{e.got ?? 0}/{e.points}</span>{e.reason && <span className="r">{e.reason}</span>}</div>
          ))}
        </div>
      )}
      {it.feedback?.length > 0 && <div className="as-fb">{it.feedback.join(" ")}</div>}
      {it.needs_review && <div className="as-note warn">🔍 읽기 어려운 글자가 있어 선생님이 한 번 더 확인해요.</div>}
      {it.read && (
        <details className="as-read">
          <summary>AI가 읽은 내 풀이 보기</summary>
          <ReadBox label="① 식 세우기" box={it.read.s1} /><ReadBox label="② 식 풀기" box={it.read.s2} /><ReadBox label="③ 구하는 것" box={it.read.s3} />
          {it.read.outside?.length > 0 && <div className="bx"><i>칸 밖</i>{it.read.outside.map((x, i) => <div key={i}>{x}</div>)}</div>}
          {it.flagged ? <div className="as-note ok">✓ 알려 줬어요 — 선생님이 다시 확인해요.</div> : fl ? (
            <div className="as-flag"><input value={note} onChange={(e) => setNote(e.target.value)} maxLength={200} placeholder="어디를 잘못 읽었나요? (예: 2번째 줄 7을 1로)" />
              <button className="as-btn as-tiny" onClick={() => onFlag(it.no, note)}>보내기</button></div>
          ) : <div className="as-flag"><button className="as-btn as-tiny" onClick={() => setFl(true)}>🙋 잘못 읽었어요</button></div>}
        </details>
      )}
      {it.answer && (
        <div className="as-key"><b>정답</b> <MathText text={it.answer.answer} />
          {it.answer.solution?.length > 0 && <div style={{ marginTop: 6 }}>{it.answer.solution.map((s, i) => <MathText key={i} as="div" text={s} />)}</div>}
        </div>
      )}
      {q && !it.answer && <details className="as-read"><summary>문제 다시 보기</summary><div style={{ marginTop: 8 }}><ProblemCard it={q} /></div></details>}
    </div>
  );
}
