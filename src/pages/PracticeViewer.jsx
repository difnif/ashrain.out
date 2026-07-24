// src/pages/PracticeViewer.jsx — 예제·유제 단계식 해설 (해시 라우트: #/p/<conceptId>)
//
// 세트 JSON 규격 (practice_sets.problems):
// {
//   "id": "p01", "level": "기본"|"표준"|"상", "kind": "예제"|"유제",
//   "review": ["소인수분해"],                       // 앞 단원 연계 표시 (선택)
//   "text": [ {"t":"문장 조각"}, ... ],              // 문제 문장을 의미 단위로 쪼갠 배열
//   "svg": "<svg viewBox=...>...</svg>",             // 도형 (선택) — id 붙은 부위는 하이라이트 대상
//   "steps": [                                       // 순서대로 공개되는 해설 단계
//     { "hl": [0,2], "svgHl": ["seg-ab"],            // 이 단계에서 칠할 문장 조각 index / 도형 부위 id
//       "note": "이 조각이 뜻하는 것…",               // 문장 해설 (형광펜과 같은 색으로 표시)
//       "expr": "식 한 줄" },                          // 풀이 노트에 누적되는 식 (선택)
//   ],
//   "methods": [ {"title":"방법1 — …","steps":[...]}, ... ],  // 있으면 steps 대신 방법 탭
//   "answer": { "label": "답", "accept": ["4","x=4"], "placeholder": "" }
// }
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/authx";

const HL = ["#FFF3A3", "#B9F0C8", "#BFDFFF", "#F5C9F0", "#FFD9B3"]; // 단계별 형광펜 (라이트/다크 공용 가독)
const HL_INK = "#1F2430";

// ── 답 판정: 공백 제거·기호 통일 + 숫자/분수 동치 허용 ──
function normAns(s) {
  return String(s ?? "")
    .replace(/\s+/g, "")
    .replace(/−/g, "-").replace(/×/g, "x").replace(/÷/g, "/")
    .replace(/[，]/g, ",")
    .toLowerCase();
}
function numVal(s) {
  const t = normAns(s);
  if (/^-?\d+(\.\d+)?$/.test(t)) return parseFloat(t);
  const m = t.match(/^(-?\d+)\/(\d+)$/);
  if (m && +m[2] !== 0) return +m[1] / +m[2];
  return null;
}
function isCorrect(input, accept) {
  const inN = normAns(input);
  if (!inN) return false;
  for (const a of accept || []) {
    if (inN === normAns(a)) return true;
    const va = numVal(a), vi = numVal(input);
    if (va !== null && vi !== null && Math.abs(va - vi) < 1e-9) return true;
  }
  return false;
}

export default function PracticeViewer({ conceptId }) {
  const [set, setSet] = useState(undefined);        // undefined 로딩, null 없음
  const [uid, setUid] = useState(null);
  const [solved, setSolved] = useState([]);         // 푼 문제 id들
  const [pi, setPi] = useState(0);                  // 현재 문제 index
  const [mi, setMi] = useState(0);                  // 방법 탭 index
  const [step, setStep] = useState(0);              // 공개된 단계 수
  const [ans, setAns] = useState("");
  const [flash, setFlash] = useState("");           // '' | 'ok' | 'no'
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
  const stepsAll = useMemo(() => {
    if (!p) return [];
    return p.methods?.length ? (p.methods[Math.min(mi, p.methods.length - 1)]?.steps || []) : (p.steps || []);
  }, [p, mi]);
  const shown = stepsAll.slice(0, step);
  const allShown = step >= stepsAll.length;
  const doneThis = p && solved.includes(p.id);
  const cleared = problems.length > 0 && problems.every((x) => solved.includes(x.id));

  // 문장 조각별 형광펜: 나중 단계가 덮어씀
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

  const goProblem = (i) => { setPi(i); setMi(0); setStep(0); setAns(""); setJustSolved(false); };

  const saveProgress = async (newSolved) => {
    if (!uid) return;
    await supabase.from("practice_progress").upsert({
      user_id: uid, concept_id: conceptId,
      solved: newSolved,
      cleared: problems.every((x) => newSolved.includes(x.id)),
      updated_at: new Date().toISOString(),
    });
  };

  const submit = () => {
    if (!p || flash) return;
    if (isCorrect(ans, p.answer?.accept)) {
      setFlash("ok");
      const ns = solved.includes(p.id) ? solved : [...solved, p.id];
      setSolved(ns); setJustSolved(true);
      saveProgress(ns);
      setTimeout(() => setFlash(""), 700);
    } else {
      setFlash("no"); setShake(true);
      setTimeout(() => { setFlash(""); setShake(false); inputRef.current?.focus(); }, 550);
    }
  };

  // SVG 부위 하이라이트: id에 해당하는 요소에 색 주입 (문자열 치환 방식 — 규격상 id="..." 필수)
  const svgHtml = useMemo(() => {
    if (!p?.svg) return null;
    let s = p.svg;
    Object.entries(svgHlIds).forEach(([id, c]) => {
      s = s.replace(new RegExp(`id="${id}"`, "g"),
        `id="${id}" style="stroke:${HL[c]};stroke-width:4;filter:drop-shadow(0 0 2px ${HL[c]})"`);
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

  return (
    <div className="pv-wrap"><Style />
      {flash && <div className={`pv-flash pv-flash-${flash}`} />}

      <header className="pv-head">
        <a className="pv-back" href={`#/c/${encodeURIComponent(conceptId)}`}>← 개념으로</a>
        <h2 className="pv-title">{set.title || "예제 · 유제"}</h2>
        <span className="pv-count">{solved.filter((id) => problems.some((x) => x.id === id)).length}/{problems.length}</span>
      </header>

      {cleared && <div className="pv-clear">🎉 챕터 클리어! 모든 문제를 해결했어요.</div>}

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

        {/* 문제 문장 — 단계에 따라 형광펜 */}
        <p className="pv-text">
          {(p.text || []).map((seg, i) => (
            <span key={i}
              className={segHl[i] !== undefined ? "pv-seg on" : "pv-seg"}
              style={segHl[i] !== undefined ? { background: HL[segHl[i]], color: HL_INK } : undefined}>
              {seg.t}
            </span>
          ))}
        </p>

        {svgHtml && (
          <div className="pv-svg" dangerouslySetInnerHTML={{ __html: svgHtml }} />
        )}

        {/* 방법 탭 (여러 방법 풀이) */}
        {p.methods?.length > 1 && (
          <div className="pv-tabs">
            {p.methods.map((m, i) => (
              <button key={i} className={"pv-tab" + (i === mi ? " on" : "")}
                onClick={() => { setMi(i); setStep(0); }}>
                {m.title || `방법 ${i + 1}`}
              </button>
            ))}
          </div>
        )}
        {p.methods?.length === 1 && <p className="pv-mtitle">{p.methods[0].title}</p>}

        {/* 단계 해설 */}
        <div className="pv-steps">
          {shown.map((st, i) => (
            <div className="pv-step" key={i}>
              <span className="pv-dot" style={{ background: HL[i % HL.length] }} />
              <div className="pv-step-body">
                {st.note && <p className="pv-note">{st.note}</p>}
                {st.expr && <p className="pv-expr">{st.expr}</p>}
              </div>
            </div>
          ))}
        </div>

        {!allShown ? (
          <button className="pv-btn pv-btn-main" onClick={() => setStep(step + 1)}>
            {step === 0 ? "해설 시작하기" : "다음 단계 →"}
            <span className="pv-prog"> {step}/{stepsAll.length}</span>
          </button>
        ) : (
          <div className="pv-answer">
            <label className="pv-alabel">{p.answer?.label || "답"}</label>
            <div className="pv-arow">
              <input ref={inputRef}
                className={"pv-input" + (shake ? " shake" : "") + (justSolved || doneThis ? " ok" : "")}
                value={justSolved || doneThis ? (p.answer?.accept?.[0] ?? ans) : ans}
                disabled={justSolved || doneThis}
                onChange={(e) => setAns(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && submit()}
                placeholder={p.answer?.placeholder || "직접 계산해서 입력"} />
              {justSolved || doneThis ? (
                pi < problems.length - 1
                  ? <button className="pv-btn pv-btn-main" onClick={() => goProblem(pi + 1)}>다음 문제 →</button>
                  : <button className="pv-btn pv-btn-main" onClick={() => goProblem(0)}>처음으로</button>
              ) : (
                <button className="pv-btn pv-btn-main" onClick={submit}>확인</button>
              )}
            </div>
            {(justSolved || doneThis) && <p className="pv-okmsg">정답! 잘 이해했어요 👏</p>}
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
      @keyframes pvFlash{0%{opacity:0}20%{opacity:1}100%{opacity:0}}
      .pv-head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
      .pv-back{font-size:13px;color:var(--muted,#6b7280);text-decoration:none;white-space:nowrap}
      .pv-title{flex:1;font-size:17px;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
      .pv-count{font-size:12px;color:var(--muted,#8a8f98)}
      .pv-clear{background:var(--accent,#0DA95F);color:#fff;border-radius:12px;padding:10px 14px;
        font-size:14px;font-weight:700;text-align:center;margin-bottom:10px}
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
      .pv-text{font-size:16.5px;line-height:2.05;margin:0 0 6px;word-break:keep-all}
      .pv-seg{border-radius:5px;padding:1px 2px;transition:background .35s}
      .pv-svg{margin:10px 0 4px;text-align:center}
      .pv-svg svg{max-width:100%;height:auto}
      .pv-tabs{display:flex;gap:6px;margin:10px 0 4px;flex-wrap:wrap}
      .pv-tab{font-size:12.5px;padding:8px 12px;border-radius:999px;border:1px solid var(--border,#d6d9de);
        background:var(--surface,#fff);color:var(--muted,#6b7280)}
      .pv-tab.on{background:var(--text,#1F2937);border-color:var(--text,#1F2937);color:var(--surface,#fff);font-weight:700}
      .pv-mtitle{font-size:13px;color:var(--muted,#6b7280);margin:10px 0 0;font-weight:700}
      .pv-steps{display:flex;flex-direction:column;gap:10px;margin:12px 0 4px}
      .pv-step{display:flex;gap:10px;animation:pvIn .3s ease-out}
      @keyframes pvIn{from{opacity:0;transform:translateY(6px)}}
      .pv-dot{width:12px;height:12px;border-radius:999px;margin-top:6px;flex-shrink:0;border:1px solid rgba(0,0,0,.12)}
      .pv-step-body{flex:1;min-width:0}
      .pv-note{margin:0;font-size:14px;line-height:1.65;color:var(--text,#374151)}
      .pv-expr{margin:6px 0 0;font-size:15.5px;background:var(--surface2,#f4f6f8);
        border:1px solid var(--border,#e5e7eb);border-radius:10px;padding:9px 12px;
        font-family:'Pretendard Variable',ui-monospace,monospace;letter-spacing:.3px;overflow-x:auto;white-space:pre-wrap}
      .pv-btn{display:inline-flex;align-items:center;justify-content:center;gap:4px;padding:12px 16px;
        border-radius:11px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);
        font-size:14.5px;color:inherit;text-decoration:none}
      .pv-btn-main{width:100%;margin-top:10px;background:var(--accent,#0DA95F);border-color:var(--accent,#0DA95F);
        color:#fff;font-weight:800}
      .pv-prog{font-weight:400;font-size:12px;opacity:.8}
      .pv-answer{margin-top:12px;border-top:1px dashed var(--border,#e5e7eb);padding-top:12px}
      .pv-alabel{font-size:12px;color:var(--muted,#6b7280);font-weight:700}
      .pv-arow{display:flex;gap:8px;margin-top:6px}
      .pv-input{flex:1;min-width:0;padding:13px 14px;font-size:17px;border-radius:11px;
        border:1.5px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#111);outline:none}
      .pv-input:focus{border-color:var(--accent,#0DA95F)}
      .pv-input.ok{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .pv-input.shake{animation:pvShake .45s;border-color:var(--bad,#dc2626)!important}
      @keyframes pvShake{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}
        30%,50%,70%{transform:translateX(-7px)}40%,60%{transform:translateX(7px)}}
      .pv-arow .pv-btn-main{width:auto;margin-top:0;flex-shrink:0}
      .pv-okmsg{margin:8px 0 0;font-size:13.5px;color:var(--good,#16a34a);font-weight:700}
      .pv-empty{text-align:center;color:var(--muted,#8a8f98);margin:60px 0 16px}
    `}</style>
  );
}
