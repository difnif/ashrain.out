// 세트 풀기 페이지 (문제풀이 홈 → 개념 고르기 → 설정 → 풀기 → 결과)
//   #/solve/set                 개념 고르기 (ItemPicker) → #/solve/set/<conceptId>
//   #/solve/set/<conceptId>     설정 카드 → 세트 풀기 → 결과 화면
//   #/solve/item/<itemId>       문항 1개 다시 풀기 (오답노트 등에서) — hash 에 from=wrong 이 있으면 오답노트로 돌아간다
// props: { conceptId, itemId, hash }  (App.jsx 가 라우팅)
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import SolveShell, { useToast } from "./SolveShell";
import ItemPicker from "./ItemPicker";
import ItemView from "../../components/ItemView";
import MathText from "../../components/MathText";
import { listConcepts } from "../../lib/concepts";
import { UNIT_NAMES, countLive, fetchLiveItems, fetchItem, diversify } from "../../lib/items";
import { saveItemWrongNotes } from "../../lib/wrongnotes";
import {
  N_OPTIONS, QTYPE_OPTIONS, BAND_OPTIONS, bandLevels, qtypesOf, readSetConfig, saveSetConfig,
  assembleSet, newSetId, summarizeResults, groupMisconceptions, wrongEntries, resultMessage,
  correctAnswerText, myAnswerText, questionPreview, fmtClock, saveLastResult, readLastResult,
} from "../../lib/setplay";
import "./solve.css";

const CSS = `
.ip-title { font-size:18px; font-weight:800; line-height:1.4; }
.ip-last { font-size:12px; color:var(--muted); margin-top:4px; }
.ip-err { margin-top:10px; font-size:13px; color:var(--bad); font-weight:700; line-height:1.5; }
.ip-prog { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.ip-count { font-size:13px; font-weight:800; white-space:nowrap; font-variant-numeric:tabular-nums; }
.ip-prog .sv-bar { flex:1; }
.ip-score { text-align:center; padding:20px 14px; }
.ip-big { font-size:40px; font-weight:900; line-height:1.1; letter-spacing:-1px; }
.ip-big .ip-of { font-size:18px; font-weight:700; color:var(--muted); letter-spacing:0; }
.ip-pct { font-size:14px; font-weight:800; color:var(--accent); margin:2px 0 6px; }
.ip-score .sv-bar { margin:10px auto 0; max-width:280px; }
.ip-msg { font-size:13.5px; color:var(--muted); margin:10px 0 0; line-height:1.6; }
.ip-mc { margin:0; padding-left:18px; font-size:13.5px; line-height:1.7; }
.ip-row { border:1px solid var(--border); border-radius:12px; background:var(--surface); overflow:hidden; }
.ip-rowbtn { display:flex; align-items:center; gap:8px; width:100%; padding:10px 12px; background:none; border:none; color:var(--text); text-align:left; cursor:pointer; font:inherit; }
.ip-mark { flex:none; width:22px; height:22px; border-radius:999px; display:inline-flex; align-items:center; justify-content:center; font-size:13px; font-weight:900; color:#fff; }
.ip-mark.ok { background:var(--good); }
.ip-mark.bad { background:var(--bad); }
.ip-no { flex:none; font-size:12px; color:var(--muted); font-weight:700; }
.ip-q { flex:1; font-size:13.5px; line-height:1.45; overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; }
.ip-chev { flex:none; color:var(--muted); font-size:12px; }
.ip-ansline { display:flex; flex-wrap:wrap; gap:4px 10px; align-items:baseline; padding:0 12px 10px 42px; font-size:13.5px; }
.ip-ansline .ip-lab { font-size:11.5px; color:var(--muted); margin-right:2px; }
.ip-row .sv-card { border:none; border-radius:0; margin:0; padding:6px 12px 12px; background:var(--surface2); }
.ip-actions { display:flex; flex-direction:column; gap:8px; margin-top:16px; }
`;

let _conceptsP = null;
function conceptsOnce() {
  if (!_conceptsP) _conceptsP = listConcepts().catch(() => { _conceptsP = null; return []; });
  return _conceptsP;
}
const clean = (s) => String(s || "").split(/[?&#]/)[0].trim();
const toTop = () => { try { window.scrollTo({ top: 0, behavior: "smooth" }); } catch { /* 무시 */ } };

export default function ItemPlay({ conceptId, itemId, hash }) {
  const [toast, setToast] = useToast();
  const [uid, setUid] = useState(null);
  useEffect(() => {
    let alive = true;
    supabase.auth.getUser().then(({ data }) => { if (alive) setUid(data?.user?.id || null); }).catch(() => {});
    return () => { alive = false; };
  }, []);

  const h = hash ?? (typeof location !== "undefined" ? location.hash : "");
  const cid = clean(conceptId), iid = clean(itemId);

  if (iid) return <><style>{CSS}</style><SingleItem itemId={iid} uid={uid} hash={h} toast={toast} setToast={setToast} /></>;
  if (!cid) {
    return (
      <SolveShell title="문제 풀기" back="#/study/practice" toast={toast}>
        <ItemPicker mode="concept" filter={{ qtypes: ["choice", "short"] }}
          hint="개념을 고르면 문항 수·유형·난이도를 정하고 바로 풀 수 있어요."
          onPickConcept={(c) => { location.hash = `#/solve/set/${c.id}`; }} />
      </SolveShell>
    );
  }
  return <><style>{CSS}</style><ConceptSet key={cid} conceptId={cid} uid={uid} toast={toast} setToast={setToast} /></>;
}

// ── 개념 세트: 설정 → 풀기 → 결과 ─────────────────────────────────────────────
function ConceptSet({ conceptId, uid, toast, setToast }) {
  const [concept, setConcept] = useState(undefined);   // undefined 로딩 · null 없음
  const [cfg, setCfg] = useState(() => readSetConfig());
  const [count, setCount] = useState(null);
  const [phase, setPhase] = useState("config");         // config | loading | play | result
  const [items, setItems] = useState([]);
  const [setId, setSetId] = useState(null);
  const [idx, setIdx] = useState(0);
  const [results, setResults] = useState([]);
  const [notice, setNotice] = useState(null);
  const [err, setErr] = useState(null);
  const [noteState, setNoteState] = useState("idle");   // idle | saving | done
  const [openIdx, setOpenIdx] = useState(null);

  useEffect(() => {
    let alive = true;
    conceptsOnce().then((list) => { if (alive) setConcept((list || []).find((c) => c.id === conceptId) || null); });
    return () => { alive = false; };
  }, [conceptId]);

  useEffect(() => {
    let alive = true;
    setCount(null);
    countLive({ conceptId, qtypes: qtypesOf(cfg.qtype) }).then((n) => { if (alive) setCount(n); });
    return () => { alive = false; };
  }, [conceptId, cfg.qtype]);

  useEffect(() => { toTop(); }, [phase, idx]);

  // 결과 화면에 들어오면 최근 결과를 남긴다 (홈에서 보여 줄 용도)
  useEffect(() => {
    if (phase !== "result" || !items.length) return;
    const s = summarizeResults(results, items.length);
    saveLastResult({ conceptId, title: concept?.title || null, n: s.n, ok: s.ok });
  }, [phase]); // eslint-disable-line react-hooks/exhaustive-deps

  /** 세트 시작. fixed 가 있으면 그 문항들로(틀린 문제 다시 풀기), 없으면 설정대로 새로 뽑는다 */
  const start = async (fixed = null) => {
    setErr(null); setNotice(null); setPhase("loading");
    try {
      let picked, relaxed = false, short = 0;
      if (fixed) {
        ({ items: picked } = assembleSet({ primary: fixed, n: fixed.length }));
      } else {
        const n = cfg.n, qtypes = qtypesOf(cfg.qtype), levels = bandLevels(cfg.band);
        let primary, fallback = [];
        if (levels) {
          const pools = await Promise.all(levels.map((d) => fetchLiveItems({ conceptId, qtypes, difficulty: d, n, pool: Math.max(60, n * 4) })));
          primary = pools.flat();
          if (primary.length < n) fallback = await fetchLiveItems({ conceptId, qtypes, n: n * 2, pool: Math.max(80, n * 8) });
        } else {
          primary = await fetchLiveItems({ conceptId, qtypes, n, pool: Math.max(80, n * 4) });
        }
        ({ items: picked, relaxed, short } = assembleSet({ primary, fallback, n, diversify }));
        saveSetConfig(cfg);
      }
      if (!picked.length) { setPhase("config"); setErr("조건에 맞는 문항이 없어요. 유형이나 난이도를 바꿔 보세요."); return; }
      const msgs = [];
      if (relaxed) msgs.push("고른 난이도의 문항이 부족해서 다른 난이도도 섞었어요.");
      if (short) msgs.push(`문항이 ${picked.length}개만 준비됐어요.`);
      setNotice(msgs.length ? msgs.join(" ") : null);
      setItems(picked); setSetId(newSetId(conceptId)); setIdx(0); setResults([]); setOpenIdx(null); setNoteState("idle");
      setPhase("play");
    } catch {
      setPhase("config"); setErr("문항을 불러오지 못했어요. 잠시 후 다시 시도해 주세요.");
    }
  };

  const cur = items[idx];
  const record = (r) => setResults((prev) => {
    if (prev[idx]) return prev;                       // 첫 답만 점수에 반영 (다시 풀기는 학습용)
    const next = prev.slice(); next[idx] = { ...r, item: cur }; return next;
  });
  const goNext = () => { if (idx + 1 < items.length) setIdx(idx + 1); else setPhase("result"); };
  const skip = () => {
    record({ correct: false, skipped: true, rawAnswer: null, chosenIndex: null, chosenChoice: null, elapsedSec: 0, tag: null });
    goNext();
  };
  const quit = () => {
    const done = results.filter(Boolean).length;
    if (!done) { setPhase("config"); return; }
    setItems(items.slice(0, done)); setResults(results.slice(0, done)); setPhase("result");
  };

  const sum = summarizeResults(results, items.length);
  const groups = phase === "result" ? groupMisconceptions(results) : [];
  const wrong = phase === "result" ? wrongEntries(results) : [];

  const saveWrong = async () => {
    if (noteState !== "idle" || !wrong.length) return;
    if (!uid) { setToast("로그인이 필요해요"); return; }
    setNoteState("saving");
    const r = await saveItemWrongNotes({ uid, entries: wrong, source: "문제풀이" });
    if (r.error) { setNoteState("idle"); setToast("오답노트에 저장하지 못했어요"); return; }
    setNoteState("done");
    setToast(r.added ? `오답노트에 ${r.added}문항을 추가했어요${r.skipped ? ` · 이미 있는 ${r.skipped}문항은 건너뜀` : ""}` : "이미 오답노트에 있는 문항이에요");
  };

  const title = concept?.title || (concept === null ? conceptId : "…");
  const unitName = UNIT_NAMES[concept?.unit_id] || "";

  // ── 설정 ──
  if (phase === "config" || phase === "loading") {
    const empty = count === 0;
    const last = readLastResult();
    return (
      <SolveShell title="문제 풀기" back="#/study/practice" toast={toast}>
        <div className="sv-card">
          <div className="ip-title">{title}</div>
          <div className="sv-small">
            {unitName}{concept?.subtitle ? ` · ${concept.subtitle}` : ""} · 공개 문항 {count == null ? "…" : `${count}개`}
          </div>
          {last && last.conceptId === conceptId && last.n > 0 && (
            <div className="ip-last">최근 결과 {last.ok}/{last.n} · {new Date(last.at).toLocaleDateString("ko-KR", { month: "short", day: "numeric" })}</div>
          )}
          <div className="sv-sec">문항 수</div>
          <div className="sv-row wrap" style={{ gap: 6 }}>
            {N_OPTIONS.map((n) => (
              <button key={n} className={"sv-chip" + (cfg.n === n ? " on" : "")} onClick={() => setCfg({ ...cfg, n })}>{n}문항</button>
            ))}
          </div>
          <div className="sv-sec">유형</div>
          <div className="sv-row wrap" style={{ gap: 6 }}>
            {QTYPE_OPTIONS.map((q) => (
              <button key={q.key} className={"sv-chip" + (cfg.qtype === q.key ? " on" : "")} onClick={() => setCfg({ ...cfg, qtype: q.key })}>{q.label}</button>
            ))}
          </div>
          <div className="sv-sec">난이도</div>
          <div className="sv-row wrap" style={{ gap: 6 }}>
            {BAND_OPTIONS.map((b) => (
              <button key={b.key} className={"sv-chip" + (cfg.band === b.key ? " on" : "")} onClick={() => setCfg({ ...cfg, band: b.key })}>
                {b.label}{b.sub ? <span className="sv-small"> {b.sub}</span> : null}
              </button>
            ))}
          </div>
          {err && <div className="ip-err">{err}</div>}
          <button className="sv-btn pri full" style={{ marginTop: 16 }} disabled={empty || count == null || phase === "loading"} onClick={() => start()}>
            {phase === "loading" ? "문항을 고르는 중…" : "시작"}
          </button>
        </div>
        {empty && (
          <div className="sv-empty">
            이 개념에는 아직 공개된 문항이 없어요.<br />
            <a href="#/solve/set">다른 개념 고르기</a>
          </div>
        )}
      </SolveShell>
    );
  }

  // ── 풀기 ──
  if (phase === "play" && cur) {
    const done = results[idx] ? 1 : 0;
    return (
      <SolveShell title="문제 풀기" back="#/study/practice" toast={toast}
        right={<button className="sv-btn sm ghost" onClick={quit}>그만하기</button>}>
        <div className="ip-prog">
          <span className="ip-count">{idx + 1} / {items.length}</span>
          <div className="sv-bar"><i style={{ width: `${((idx + done) / items.length) * 100}%` }} /></div>
          {!done && <button className="sv-btn sm ghost" onClick={skip}>건너뛰기</button>}
        </div>
        {notice && <p className="sv-sub">{notice}</p>}
        <ItemView key={cur.id} item={cur} index={idx} uid={uid} setId={setId} seq={idx + 1}
          onAnswered={record} onNext={goNext} nextLabel={idx + 1 < items.length ? "다음 문제" : "결과 보기"} onToast={setToast} />
      </SolveShell>
    );
  }

  // ── 결과 ──
  return (
    <SolveShell title="문제 풀기" back="#/study/practice" toast={toast}>
      <div className="sv-card ip-score">
        <div className="ip-big">{sum.ok} <span className="ip-of">/ {sum.n}</span></div>
        <div className="ip-pct">정답률 {sum.pct}%</div>
        <div className="sv-small">{title} · 푼 시간 {fmtClock(sum.totalSec)}</div>
        <div className="sv-bar"><i style={{ width: `${sum.pct}%` }} /></div>
        <p className="ip-msg">{resultMessage(sum.pct, sum.n)}</p>
      </div>

      {groups.length > 0 && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>이런 실수를 했어요</div>
          <ul className="ip-mc">
            {groups.map((g) => (
              <li key={g.tag}><b>{g.label}</b> <span className="sv-small">{g.count}문항 · {g.idx.map((i) => i + 1).join(", ")}번</span></li>
            ))}
          </ul>
        </div>
      )}

      <div className="sv-sec">문항별 결과 <span className="sv-small">(누르면 해설을 볼 수 있어요)</span></div>
      <div className="sv-list">
        {items.map((it, i) => {
          const r = results[i];
          const ok = r?.correct === true;
          const open = openIdx === i;
          return (
            <div key={it.id} className="ip-row">
              <button className="ip-rowbtn" onClick={() => setOpenIdx(open ? null : i)}>
                <span className={"ip-mark " + (ok ? "ok" : "bad")}>{ok ? "✓" : "✗"}</span>
                <span className="ip-no">{i + 1}</span>
                <span className="ip-q">{questionPreview(it.question, 60)}</span>
                <span className="ip-chev">{open ? "▴" : "▾"}</span>
              </button>
              <div className="ip-ansline">
                <span><span className="ip-lab">내 답</span><MathText text={myAnswerText(it, r)} className={ok ? "sv-ok" : "sv-bad"} /></span>
                {!ok && <span><span className="ip-lab">정답</span><MathText text={correctAnswerText(it)} className="sv-ok" /></span>}
              </div>
              {open && <ItemView item={it} index={i} uid={uid} reveal initialAnswer={r} autoLog={false} showSolution onToast={setToast} />}
            </div>
          );
        })}
      </div>

      <div className="ip-actions">
        {wrong.length > 0 && (
          <button className="sv-btn pri full" disabled={noteState !== "idle"} onClick={saveWrong}>
            {noteState === "done" ? "오답노트에 저장했어요" : noteState === "saving" ? "저장 중…" : `틀린 문제 오답노트에 저장 (${wrong.length})`}
          </button>
        )}
        {wrong.length > 0 && <button className="sv-btn full" onClick={() => start(wrong.map((e) => e.item))}>틀린 문제만 다시 풀기</button>}
        <div className="sv-grid2">
          <button className="sv-btn" onClick={() => start()}>같은 개념 새 세트</button>
          <button className="sv-btn" onClick={() => { location.hash = "#/solve/set"; }}>다른 개념 고르기</button>
        </div>
        <button className="sv-btn ghost full" onClick={() => { location.hash = "#/study/practice"; }}>공부하기 홈</button>
      </div>
    </SolveShell>
  );
}

// ── 문항 1개 다시 풀기 ─────────────────────────────────────────────────────────
function SingleItem({ itemId, uid, hash, toast, setToast }) {
  const [item, setItem] = useState(undefined);
  const fromWrong = String(hash || "").includes("from=wrong");
  const backTo = fromWrong ? "#/learn/wrong" : "#/study/practice";
  const [setId] = useState(() => `${fromWrong ? "replay" : "single"}:${Date.now().toString(36)}`);

  useEffect(() => {
    let alive = true;
    setItem(undefined);
    fetchItem(itemId).then((it) => { if (alive) setItem(it || null); }).catch(() => { if (alive) setItem(null); });
    return () => { alive = false; };
  }, [itemId]);

  return (
    <SolveShell title="문제 풀기" back={backTo} toast={toast}>
      {item === undefined && <div className="sv-muted">문항을 불러오는 중…</div>}
      {item === null && (
        <div className="sv-empty">지금은 볼 수 없는 문항이에요.<br /><a href={backTo}>돌아가기</a></div>
      )}
      {item && (
        <ItemView item={item} uid={uid} setId={setId} seq={1} onToast={setToast}
          onNext={() => { location.hash = backTo; }} nextLabel={fromWrong ? "오답노트로 돌아가기" : "문제풀이 홈으로"} />
      )}
    </SolveShell>
  );
}
