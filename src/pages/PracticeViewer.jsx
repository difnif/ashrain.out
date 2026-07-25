// src/pages/PracticeViewer.jsx — 예제·유제 단계식 해설 v2 (해시 라우트: #/p/<conceptId>)
//
// 세트 JSON 규격 (practice_sets.problems):
// {
//   "id": "p01", "level": "기본"|"표준"|"상", "kind": "예제"|"유제",
//   "review": ["소인수분해"],
//   "text": [ {"t":"문장 조각"}, {"br":true}, ... ], // {{2/3}} 토큰 → 세로 분수 / {"br":true} → 줄바꿈
//   "svg": "<svg ...>", 
//   "choices": ["㉠", "㉠, ㉡", ...],             // 있으면 객관식 — 답은 번호로
//   "steps": [ { "hl":[..], "svgHl":[..], "svgCls":[..], "note":"...", "expr":"식" | ["줄1","= 줄2"] } ],
//   "methods": [ {"title":"방법1","steps":[...]}, ... ],   // 여러 방법: 전부 봐야 답 입력 열림
//   "answer": { "label":"답", "accept":["8"], "placeholder":"", 
//               "unit":"원",                      // 단위 누락 시 주황 경고
//               "format":"fraction" }             // 분자/분모 두 칸 입력 (정확 일치 판정)
// }
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/authx";

const HL = ["#FFF3A3", "#B9F0C8", "#BFDFFF", "#F5C9F0", "#FFD9B3"];
const HL_INK = "#1F2430";
const CIRC = ["①", "②", "③", "④", "⑤", "⑥"];

// ---------- 리치 텍스트: {{a/b}} → 세로 분수 ----------
function rich(str) {
  const parts = String(str ?? "").split(/(\{\{[^}]+\}\})/g);
  return parts.map((p, i) => {
    const m = p.match(/^\{\{([^/}]+)\/([^}]+)\}\}$/);
    if (m) {
      return (
        <span className="pv-frac" key={i}>
          <span className="pv-fr-n">{m[1]}</span>
          <span className="pv-fr-d">{m[2]}</span>
        </span>
      );
    }
    return <span key={i}>{p}</span>;
  });
}

// ---------- 답 판정 ----------
function normAns(s) {
  let t = String(s ?? "").replace(/\s+/g, "")
    .replace(/−/g, "-").replace(/×/g, "x").replace(/÷/g, "/")
    .replace(/[，]/g, ",").toLowerCase();
  CIRC.forEach((c, i) => { t = t.replace(new RegExp(c, "g"), String(i + 1)); });
  return t;
}
function numVal(s) {
  const t = normAns(s);
  if (/^-?\d+(\.\d+)?$/.test(t)) return parseFloat(t);
  const m = t.match(/^(-?\d+)\/(\d+)$/);
  if (m && +m[2] !== 0) return +m[1] / +m[2];
  return null;
}
function isCorrect(input, accept, { exact = false } = {}) {
  const inN = normAns(input);
  if (!inN) return false;
  for (const a of accept || []) {
    if (inN === normAns(a)) return true;
    if (!exact) {
      const va = numVal(a), vi = numVal(input);
      if (va !== null && vi !== null && Math.abs(va - vi) < 1e-9) return true;
    }
  }
  return false;
}

export default function PracticeViewer({ conceptId }) {
  const [set, setSet] = useState(undefined);
  const [uid, setUid] = useState(null);
  const [solved, setSolved] = useState([]);
  const [pi, setPi] = useState(0);
  const [mi, setMi] = useState(0);
  const [stepByM, setStepByM] = useState({});     // 방법별 공개 단계 수
  const [ans, setAns] = useState("");
  const [ansN, setAnsN] = useState("");           // 분수 분자
  const [ansD, setAnsD] = useState("");           // 분수 분모
  const [flash, setFlash] = useState("");         // ok | no | warn
  const [warnMsg, setWarnMsg] = useState("");
  const [shake, setShake] = useState(false);
  const [justSolved, setJustSolved] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    (async () => {
      const { data: s } = await supabase.auth.getSession();
      const u = s?.session?.user?.id || null;
      setUid(u);
      const { data: row } = await supabase.from("practice_sets")
        .select("*").eq("concept_id", conceptId).maybeSingle();
      setSet(row || null);
      if (u) {
        const { data: pg } = await supabase.from("practice_progress")
          .select("solved").eq("user_id", u).eq("concept_id", conceptId).maybeSingle();
        setSolved(Array.isArray(pg?.solved) ? pg.solved : []);
      }
    })();
  }, [conceptId]);

  const problems = set?.problems || [];
  const p = problems[pi];
  const isFraction = p?.answer?.format === "fraction";

  // 방법 통합: methods 없으면 steps를 단일 방법으로
  const methodsArr = useMemo(() => {
    if (!p) return [];
    return p.methods?.length ? p.methods : [{ steps: p.steps || [] }];
  }, [p]);
  const multi = (p?.methods?.length || 0) > 1;
  const curSteps = methodsArr[mi]?.steps || [];
  const shownCount = stepByM[mi] || 0;
  const shown = curSteps.slice(0, shownCount);
  const methodDone = (i) => (stepByM[i] || 0) >= (methodsArr[i]?.steps.length || 0);
  const allDone = methodsArr.length > 0 && methodsArr.every((_, i) => methodDone(i));
  const nextUndone = methodsArr.findIndex((_, i) => !methodDone(i));
  const doneThis = p && solved.includes(p.id);
  const cleared = problems.length > 0 && problems.every((x) => solved.includes(x.id));
  const isLast = pi === problems.length - 1;

  const segHl = useMemo(() => {
    const map = {};
    shown.forEach((st, i) => (st.hl || []).forEach((idx) => { map[idx] = i % HL.length; }));
    return map;
  }, [shown]);
  const svgHlIds = useMemo(() => {
    const map = {};
    shown.forEach((st, i) => (st.svgHl || []).forEach((id) => { map[id] = i % HL.length; }));
    return map;
  }, [shown]);
  const svgCls = useMemo(() => shown.flatMap((st) => st.svgCls || []), [shown]);

  const goProblem = (i) => {
    setPi(i); setMi(0); setStepByM({});
    setAns(""); setAnsN(""); setAnsD("");
    setWarnMsg(""); setJustSolved(false);
  };

  const saveProgress = async (newSolved) => {
    if (!uid) return;
    await supabase.from("practice_progress").upsert({
      user_id: uid, concept_id: conceptId,
      solved: newSolved,
      cleared: problems.every((x) => newSolved.includes(x.id)),
      updated_at: new Date().toISOString(),
    });
  };

  const leave = () => {
    if (window.history.length > 1) window.history.back();
    else window.location.hash = "#/";
  };

  const submit = () => {
    if (!p || flash) return;
    const a = p.answer || {};
    const input = isFraction ? `${ansN}/${ansD}` : ans;
    if (isCorrect(input, a.accept, { exact: isFraction })) {
      setFlash("ok"); setWarnMsg("");
      const ns = solved.includes(p.id) ? solved : [...solved, p.id];
      setSolved(ns); setJustSolved(true);
      saveProgress(ns);
      setTimeout(() => setFlash(""), 700);
      return;
    }
    // 단위 누락 경고 (값은 맞는데 단위만 빠진 경우)
    if (a.unit && !normAns(input).includes(normAns(a.unit)) &&
        isCorrect(input + a.unit, a.accept)) {
      setFlash("warn");
      setWarnMsg(`⚠ 단위가 빠졌어요! '${(a.accept?.[0] || "")}'처럼 단위까지 써주세요.`);
      setTimeout(() => { setFlash(""); inputRef.current?.focus(); }, 800);
      return;
    }
    setFlash("no"); setShake(true); setWarnMsg("");
    setTimeout(() => { setFlash(""); setShake(false); inputRef.current?.focus(); }, 550);
  };

  const svgHtml = useMemo(() => {
    if (!p?.svg) return null;
    let s = p.svg;
    Object.entries(svgHlIds).forEach(([id, c]) => {
      s = s.replace(new RegExp(`id="${id}"`, "g"),
        `id="${id}" style="stroke:${HL[c]};stroke-width:4;filter:drop-shadow(0 0 2px ${HL[c]})"`);
      s = s.replace(new RegExp(`id='${id}'`, "g"),
        `id='${id}' style='stroke:${HL[c]};stroke-width:4;filter:drop-shadow(0 0 2px ${HL[c]})'`);
    });
    return s;
  }, [p, svgHlIds]);

  if (set === undefined) return <div className="pv-wrap"><Style /></div>;
  if (set === null || problems.length === 0) {
    return (
      <div className="pv-wrap"><Style />
        <p className="pv-empty">아직 이 개념의 예제·유제가 준비되지 않았어요.</p>
        <a className="pv-btn" href="#/">← 홈으로</a>
      </div>
    );
  }

  const solvedInput = justSolved || doneThis;

  return (
    <div className="pv-wrap"><Style />
      {flash && <div className={`pv-flash pv-flash-${flash}`} />}

      <header className="pv-head">
        <button className="pv-back" onClick={leave}>← 나가기</button>
        <h2 className="pv-title">{set.title || "예제 · 유제"}</h2>
        <span className="pv-count">{solved.filter((id) => problems.some((x) => x.id === id)).length}/{problems.length}</span>
      </header>

      {cleared && (
        <div className="pv-clear">
          🎉 챕터 클리어! 모든 문제를 해결했어요.
          <button className="pv-clear-btn" onClick={leave}>학습 완료 →</button>
        </div>
      )}

      <div className="pv-nav">
        {problems.map((x, i) => (
          <button key={x.id}
            className={"pv-chip" + (i === pi ? " on" : "") + (solved.includes(x.id) ? " done" : "")}
            onClick={() => goProblem(i)}>
            {solved.includes(x.id) ? "✓" : i + 1}
          </button>
        ))}
      </div>

      <div className="pv-card">
        <div className="pv-meta">
          <span className={"pv-lv lv-" + (p.level || "기본")}>{p.level || "기본"}</span>
          <span className="pv-kind">{p.kind || "유제"} {pi + 1}</span>
          {(p.review || []).map((r) => <span className="pv-review" key={r}>🔁 {r}</span>)}
        </div>

        <p className="pv-text">
          {(p.text || []).map((seg, i) => (
            seg.br ? <br key={i} /> : (
              <span key={i}
                className={"pv-seg" + (segHl[i] !== undefined ? " on" : "") + (/\{\{/.test(seg.t || "") ? " tall" : "")}
                style={segHl[i] !== undefined ? { background: HL[segHl[i]], color: HL_INK } : undefined}>
                {rich(seg.t)}
              </span>
            )
          ))}
        </p>

        {p.choices?.length > 0 && (
          <div className="pv-choices">
            {p.choices.map((c, i) => (
              <div className="pv-choice" key={i}>
                <b>{CIRC[i]}</b> {rich(c)}
              </div>
            ))}
          </div>
        )}

        {svgHtml && (
          <div className={["pv-svg", ...svgCls].join(" ")} dangerouslySetInnerHTML={{ __html: svgHtml }} />
        )}

        {multi && (
          <div className="pv-tabs">
            {methodsArr.map((m, i) => (
              <button key={i} className={"pv-tab" + (i === mi ? " on" : "") + (methodDone(i) ? " ok" : "")}
                onClick={() => setMi(i)}>
                {methodDone(i) ? "✓ " : ""}{m.title || `방법 ${i + 1}`}
              </button>
            ))}
          </div>
        )}
        {p.methods?.length === 1 && <p className="pv-mtitle">{p.methods[0].title}</p>}

        <div className="pv-steps">
          {shown.map((st, i) => (
            <div className="pv-step" key={i}>
              <span className="pv-dot" style={{ background: HL[i % HL.length] }} />
              <div className="pv-step-body">
                {st.note && <p className="pv-note">{rich(st.note)}</p>}
                {st.expr && (
                  <div className="pv-expr">
                    {(Array.isArray(st.expr) ? st.expr : [st.expr]).map((line, li) => (
                      <div className="pv-expr-line" key={li}>{rich(line)}</div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {!allDone ? (
          shownCount < curSteps.length ? (
            <button className="pv-btn pv-btn-main"
              onClick={() => setStepByM((s) => ({ ...s, [mi]: shownCount + 1 }))}>
              {shownCount === 0 ? (multi ? `${methodsArr[mi].title || `방법 ${mi + 1}`} 시작하기` : "해설 시작하기") : "다음 단계 →"}
              <span className="pv-prog"> {shownCount}/{curSteps.length}</span>
            </button>
          ) : (
            <button className="pv-btn pv-btn-main" onClick={() => setMi(nextUndone)}>
              {methodsArr[nextUndone]?.title || `방법 ${nextUndone + 1}`} 보기 →
              <span className="pv-prog"> (모든 방법을 봐야 답을 입력할 수 있어요)</span>
            </button>
          )
        ) : (
          <div className="pv-answer">
            <label className="pv-alabel">{p.answer?.label || "답"}</label>
            <div className="pv-arow">
              {isFraction ? (
                <div className={"pv-fracin" + (shake ? " shake" : "") + (solvedInput ? " ok" : "")}>
                  <input ref={inputRef} className="pv-fr-in" inputMode="numeric"
                    value={solvedInput ? (p.answer.accept?.[0] || "").split("/")[0] : ansN}
                    disabled={solvedInput}
                    onChange={(e) => setAnsN(e.target.value)} placeholder="분자" />
                  <div className="pv-fr-bar" />
                  <input className="pv-fr-in" inputMode="numeric"
                    value={solvedInput ? (p.answer.accept?.[0] || "").split("/")[1] : ansD}
                    disabled={solvedInput}
                    onChange={(e) => setAnsD(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && submit()} placeholder="분모" />
                </div>
              ) : (
                <input ref={inputRef}
                  className={"pv-input" + (shake ? " shake" : "") + (solvedInput ? " ok" : "") + (flash === "warn" ? " warn" : "")}
                  value={solvedInput ? (p.answer?.accept?.[0] ?? ans) : ans}
                  disabled={solvedInput}
                  onChange={(e) => { setAns(e.target.value); setWarnMsg(""); }}
                  onKeyDown={(e) => e.key === "Enter" && submit()}
                  placeholder={p.answer?.placeholder || "직접 계산해서 입력"} />
              )}
              {solvedInput ? (
                isLast || cleared ? (
                  <button className="pv-btn pv-btn-main" onClick={leave}>🎉 학습 완료 →</button>
                ) : (
                  <button className="pv-btn pv-btn-main" onClick={() => goProblem(pi + 1)}>다음 문제 →</button>
                )
              ) : (
                <button className="pv-btn pv-btn-main" onClick={submit}>확인</button>
              )}
            </div>
            {warnMsg && <p className="pv-warnmsg">{warnMsg}</p>}
            {solvedInput && (
              <p className="pv-okmsg">정답! 잘 이해했어요 👏
                {(isLast || cleared) && <button className="pv-again" onClick={() => goProblem(0)}>다시 풀기</button>}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .pv-wrap{max-width:640px;margin:0 auto;padding:16px 14px 60px;color:var(--text,#1c1c1e);
        font-family:'Pretendard Variable',Pretendard,'Malgun Gothic',system-ui,sans-serif}
      .pv-flash{position:fixed;inset:0;pointer-events:none;z-index:50;animation:pvFlash .55s ease-out}
      .pv-flash-no{background:radial-gradient(circle at 50% 40%, rgba(220,38,38,.28), rgba(220,38,38,.12) 60%, transparent)}
      .pv-flash-ok{background:radial-gradient(circle at 50% 40%, rgba(22,163,74,.30), rgba(22,163,74,.12) 60%, transparent)}
      .pv-flash-warn{background:radial-gradient(circle at 50% 40%, rgba(245,158,11,.30), rgba(245,158,11,.12) 60%, transparent)}
      @keyframes pvFlash{0%{opacity:0}20%{opacity:1}100%{opacity:0}}
      .pv-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
      .pv-back{font-size:13px;color:var(--muted,#6b7280);background:none;border:none;padding:0;white-space:nowrap;cursor:pointer}
      .pv-title{flex:1;font-size:17px;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
      .pv-count{font-size:12px;color:var(--muted,#8a8f98)}
      .pv-clear{background:var(--accent,#0DA95F);color:#fff;border-radius:12px;padding:10px 14px;
        font-size:14px;font-weight:700;text-align:center;margin-bottom:10px;display:flex;
        align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}
      .pv-clear-btn{background:rgba(255,255,255,.22);border:none;color:#fff;font-weight:800;
        padding:7px 12px;border-radius:9px;font-size:13px;cursor:pointer}
      .pv-nav{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
      .pv-chip{width:34px;height:34px;border-radius:10px;border:1px solid var(--border,#d6d9de);
        background:var(--surface,#fff);color:var(--muted,#6b7280);font-size:13px;font-weight:700}
      .pv-chip.on{border-color:var(--accent,#0DA95F);color:var(--text,#111);box-shadow:0 0 0 2px var(--accent,#0DA95F) inset}
      .pv-chip.done{background:var(--accent,#0DA95F);border-color:var(--accent,#0DA95F);color:#fff}
      .pv-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:16px;padding:16px}
      .pv-meta{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:10px}
      .pv-lv{font-size:11px;font-weight:800;padding:3px 9px;border-radius:999px}
      .lv-기본{background:#DCFCE7;color:#166534}.lv-표준{background:#DBEAFE;color:#1E40AF}.lv-상{background:#FEE2E2;color:#991B1B}
      .pv-kind{font-size:12px;color:var(--muted,#8a8f98);font-weight:700}
      .pv-review{font-size:11px;background:var(--surface2,#f1f2f4);color:var(--muted,#6b7280);
        padding:3px 8px;border-radius:999px}
      .pv-text{font-size:16.5px;line-height:2.2;margin:0 0 6px;word-break:keep-all}
      .pv-seg{border-radius:5px;padding:1px 2px;transition:background .35s}
      .pv-choices{display:flex;flex-direction:column;gap:6px;margin:8px 0 4px;
        border:1px solid var(--border,#e5e7eb);border-radius:12px;padding:12px 14px}
      .pv-choice{font-size:15px;line-height:1.6}
      .pv-choice b{margin-right:6px}
      .pv-svg{margin:10px 0 4px;text-align:center;color:var(--text,#1c1c1e)}
      .pv-svg svg{max-width:100%;height:auto}
      .pv-tabs{display:flex;gap:6px;margin:10px 0 4px;flex-wrap:wrap}
      .pv-tab{font-size:12.5px;padding:8px 12px;border-radius:999px;border:1px solid var(--border,#d6d9de);
        background:var(--surface,#fff);color:var(--muted,#6b7280)}
      .pv-tab.on{background:var(--text,#1F2937);border-color:var(--text,#1F2937);color:var(--surface,#fff);font-weight:700}
      .pv-tab.ok{border-color:var(--accent,#0DA95F)}
      .pv-mtitle{font-size:13px;color:var(--muted,#6b7280);margin:10px 0 0;font-weight:700}
      .pv-steps{display:flex;flex-direction:column;gap:10px;margin:12px 0 4px}
      .pv-step{display:flex;gap:10px;animation:pvIn .3s ease-out}
      @keyframes pvIn{from{opacity:0;transform:translateY(6px)}}
      .pv-dot{width:12px;height:12px;border-radius:999px;margin-top:6px;flex-shrink:0;border:1px solid rgba(0,0,0,.12)}
      .pv-step-body{flex:1;min-width:0}
      .pv-note{margin:0;font-size:14px;line-height:1.65;color:var(--text,#374151)}
      .pv-expr{margin:6px 0 0;background:var(--surface2,#f4f6f8);
        border:1px solid var(--border,#e5e7eb);border-radius:10px;padding:9px 12px;overflow-x:auto}
      .pv-expr-line{font-size:14.5px;letter-spacing:.2px;white-space:pre;
        font-family:'Pretendard Variable',ui-monospace,monospace;line-height:1.9;
        font-variant-numeric:tabular-nums}
      .pv-frac{display:inline-flex;flex-direction:column;vertical-align:middle;
        text-align:center;margin:0 3px;line-height:1.1;font-size:.78em}
      .pv-seg.on{box-decoration-break:clone;-webkit-box-decoration-break:clone}
      .pv-seg.tall{display:inline-block;vertical-align:middle;line-height:1.25}
      .pv-seg.on.tall{padding:4px 8px;border-radius:8px}
      .pv-fr-n{padding:0 4px;border-bottom:1.6px solid currentColor}
      .pv-fr-d{padding:0 4px}
      .pv-btn{display:inline-flex;align-items:center;justify-content:center;gap:4px;padding:12px 16px;
        border-radius:11px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);
        font-size:14.5px;color:inherit;text-decoration:none;cursor:pointer}
      .pv-btn-main{width:100%;margin-top:10px;background:var(--accent,#0DA95F);border-color:var(--accent,#0DA95F);
        color:#fff;font-weight:800}
      .pv-prog{font-weight:400;font-size:12px;opacity:.85}
      .pv-answer{margin-top:12px;border-top:1px dashed var(--border,#e5e7eb);padding-top:12px}
      .pv-alabel{font-size:12px;color:var(--muted,#6b7280);font-weight:700}
      .pv-arow{display:flex;gap:8px;margin-top:6px;align-items:stretch}
      .pv-input{flex:1;min-width:0;padding:13px 14px;font-size:17px;border-radius:11px;
        border:1.5px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#111);outline:none}
      .pv-input:focus{border-color:var(--accent,#0DA95F)}
      .pv-input.ok{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .pv-input.warn{border-color:#F59E0B!important}
      .pv-input.shake,.pv-fracin.shake{animation:pvShake .45s}
      .pv-input.shake{border-color:var(--bad,#dc2626)!important}
      .pv-fracin.shake{outline:1.5px solid var(--bad,#dc2626);border-radius:12px}
      @keyframes pvShake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}
        30%,50%,70%{transform:translateX(-7px)}40%,60%{transform:translateX(7px)}}
      .pv-fracin{display:flex;flex-direction:column;align-items:center;gap:4px;flex:0 0 auto;
        padding:8px 10px;border:1.5px solid var(--border,#d6d9de);border-radius:12px;background:var(--surface,#fff)}
      .pv-fracin.ok{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .pv-fr-in{width:88px;text-align:center;font-size:17px;padding:7px 6px;border-radius:8px;
        border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#111);outline:none}
      .pv-fr-bar{width:96px;height:2px;background:var(--text,#1F2937);border-radius:2px}
      .pv-arow .pv-btn-main{width:auto;margin-top:0;flex-shrink:0}
      .pv-okmsg{margin:8px 0 0;font-size:13.5px;color:var(--good,#16a34a);font-weight:700;display:flex;align-items:center;gap:10px}
      .pv-again{background:none;border:none;color:var(--muted,#8a8f98);font-size:12px;text-decoration:underline;cursor:pointer;padding:0}
      .pv-warnmsg{margin:8px 0 0;font-size:13px;color:#D97706;font-weight:700}
      .pv-empty{text-align:center;color:var(--muted,#8a8f98);margin:60px 0 16px}
    `}</style>
  );
}
