// 문장 해설 — #/solve/read (문항 고르기) · #/solve/read/<itemId>
// 문제 문장을 규칙(marking.js)으로 뜯어 보여 준다: 표시(동그라미·밑줄·빗금) · 구하는 것 · 주어진 조건 · 함정 · 선수 개념 · 방침.
// 정답은 어디에도 내보내지 않는다 (방침 단계 텍스트에 정답 숫자가 섞여 있으면 ▢ 로 가린다).
import { useEffect, useMemo, useState } from "react";
import SolveShell, { useToast } from "./SolveShell";
import ItemPicker from "./ItemPicker";
import SentenceMarks, { MarkLegend } from "./SentenceMarks";
import MathText from "../../components/MathText";
import ItemFigure from "../../components/ItemFigure";
import { fetchItem, solutionLevels } from "../../lib/items";
import { askAboutItem } from "../../lib/ask";
import { kindOf, CIRCLED, displayAnswer } from "../../lib/answers";
import { explain, practiceEligible, FUNC_LABEL, markText } from "../../lib/marking.js";

const CSS = `
.rd-sent{padding:6px 4px 2px}
.rd-note{margin-top:8px;padding:10px 12px;border-radius:12px;background:var(--surface2);font-size:13.5px;line-height:1.6}
.rd-note b{display:inline-block;margin-right:6px;font-size:12px;padding:1px 8px;border-radius:999px;background:var(--surface);border:1px solid var(--border)}
.rd-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.rd-chip{font-size:12.5px;padding:4px 10px;border-radius:999px;border:1px solid var(--border);background:var(--surface2);color:var(--text)}
.rd-chip.warn{border-color:color-mix(in srgb,var(--bad) 50%,var(--border));}
.rd-ask{font-size:17px;font-weight:800;line-height:1.6;padding:10px 12px;border-radius:12px;background:color-mix(in srgb,var(--accent) 10%,var(--surface));border:1px solid color-mix(in srgb,var(--accent) 35%,var(--border))}
.rd-ol{margin:0;padding-left:0;list-style:none;display:flex;flex-direction:column;gap:8px}
.rd-ol li{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.6}
.rd-ol .no{flex:none;min-width:24px;height:24px;border-radius:999px;background:var(--surface2);display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;margin-top:2px}
.rd-ul{margin:0;padding-left:18px;font-size:14.5px;line-height:1.7}
.rd-details summary{cursor:pointer;font-weight:800;font-size:14px;padding:4px 0;list-style:none;display:flex;align-items:center;gap:8px}
.rd-details summary::-webkit-details-marker{display:none}
.rd-details summary::before{content:"▸";font-size:12px;color:var(--muted);transition:transform .15s}
.rd-details[open] summary::before{transform:rotate(90deg)}
.rd-details .body{margin-top:8px;font-size:14.5px;line-height:1.7;color:var(--text)}
.rd-details ol{margin:4px 0 0 20px;padding:0}
.rd-choices{margin-top:8px;display:flex;flex-direction:column;gap:4px;font-size:14px;color:var(--muted)}
.rd-choices .c{display:flex;gap:8px;align-items:baseline}
.rd-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px}
@media (max-width:420px){.rd-actions{grid-template-columns:1fr}}
`;

/** 방침 문장에서 정답(숫자형)만 가린다 — 낱말형 답(소수·합성수 등)은 개념어라 그대로 둔다 */
export function maskAnswer(text, item) {
  let out = String(text ?? "");
  const cands = [item?.answer, ...(Array.isArray(item?.answer_alt) ? item.answer_alt : [])].filter((x) => x != null && String(x).trim());
  for (const c of cands) {
    const forms = new Set([String(c), displayAnswer(c)].map((s) => s.trim()).filter((s) => s && s.length <= 12 && /\d/.test(s)));
    for (const f of forms) {
      const esc = f.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      out = out.replace(new RegExp(`(^|[^0-9A-Za-z가-힣.])${esc}(?![0-9.])`, "g"), "$1▢");
    }
  }
  return out;
}

export default function Read({ itemId }) {
  const [toast] = useToast();
  const [item, setItem] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    setItem(null); setErr(null);
    if (!itemId) return;
    let alive = true;
    fetchItem(itemId).then((it) => { if (!alive) return; if (!it) setErr("문항을 찾을 수 없어요. 공개되지 않은 문항일 수도 있어요."); else setItem(it); })
      .catch(() => alive && setErr("문항을 불러오지 못했어요. 잠시 뒤 다시 시도해 주세요."));
    return () => { alive = false; };
  }, [itemId]);

  if (!itemId) {
    return (
      <SolveShell title="문장 해설" sub="문제 문장을 뜯어 읽어요 — 무엇이 주어졌고, 무엇을 구하는지, 단서는 어디서 끊기는지." toast={toast}>
        <ItemPicker mode="item" hint="문항을 하나 골라 주세요. 문장을 함께 읽어 볼게요." onPickItem={(it) => { location.hash = `#/solve/read/${it.id}`; }} />
      </SolveShell>
    );
  }

  return (
    <SolveShell title="문장 해설" toast={toast}
      right={<button className="sv-btn sm" onClick={() => { location.hash = "#/solve/read"; }}>다른 문항</button>}>
      <style>{CSS}</style>
      {err && <div className="sv-empty">{err}</div>}
      {!err && !item && <div className="sv-muted">문항을 불러오는 중…</div>}
      {item && <ReadView item={item} />}
    </SolveShell>
  );
}

/** 문항 하나의 해설 본문 (SolveShell 안에서) */
export function ReadView({ item }) {
  const [picked, setPicked] = useState(null);
  const ex = useMemo(() => explain(item?.question || "", item), [item]);
  const level0 = useMemo(() => solutionLevels(item)[0] || null, [item]);
  const eligible = useMemo(() => practiceEligible(item?.question), [item]);
  const counts = { NUM: 0, SCALE: 0, BOUND: 0 };
  for (const m of ex.marks) if (m.tier === 1 && m.required) counts[m.func] = (counts[m.func] || 0) + 1;

  return (
    <>
      {/* 문장 + 표시 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>문제 문장 <span className="sv-small">· 표시를 탭하면 설명이 나와요</span></div>
        <SentenceMarks className="rd-sent" tokens={ex.tokens} marks={ex.marks} onMarkTap={(m) => setPicked(m)} />
        {picked && (
          <div className="rd-note">
            <b>{FUNC_LABEL[picked.func] || picked.func}</b>
            <span>{markText(picked, ex.tokens) ? `${markText(picked, ex.tokens).replace(/\[\[|\]\]/g, "")} — ` : ""}{picked.note || "단서예요."}</span>
          </div>
        )}
        {ex.traps.length > 0 && (
          <div className="rd-chips">
            {ex.traps.map((t, i) => <span key={i} className="rd-chip warn">⚠ {t}</span>)}
          </div>
        )}
        <ItemFigure figure={item.figure} width={320} />
        {kindOf(item) === "choice" && Array.isArray(item.choices) && (
          <div className="rd-choices">
            {item.choices.map((c, i) => <div key={i} className="c"><span>{CIRCLED[i] || i + 1}</span><MathText text={c} /></div>)}
          </div>
        )}
      </div>

      {/* 구하는 것 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>구하는 것</div>
        {ex.asking
          ? <MathText as="div" className="rd-ask" text={ex.asking} />
          : <div className="sv-muted">구하는 것을 딱 잘라 찾지 못했어요. 마지막 문장을 다시 읽어 보세요 — 보통 "…를 구하시오" 앞에 있어요.</div>}
        <div className="sv-small" style={{ marginTop: 8 }}>답을 쓰기 전에, 이걸 구했는지 꼭 확인해요.</div>
      </div>

      {/* 주어진 조건 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>주어진 조건 <span className="sv-small">· 단서 경계마다 한 줄</span></div>
        {ex.givens.length
          ? <ol className="rd-ol">{ex.givens.map((g, i) => <li key={i}><span className="no">{i + 1}</span><MathText as="span" text={g} /></li>)}</ol>
          : <div className="sv-muted">따로 떨어져 있는 조건이 없어요 — 구하는 문장 안에 조건이 함께 들어 있어요.</div>}
      </div>

      {/* 표시 읽는 법 */}
      <div className="sv-card">
        <div className="sv-sec" style={{ marginTop: 0 }}>표시 읽는 법</div>
        <MarkLegend tier2={ex.marks.some((m) => m.func === "EMPH")} />
        <div className="sv-small" style={{ marginTop: 10 }}>
          이 문장에는 동그라미 {counts.NUM}개 · 밑줄 {counts.SCALE}개 · 빗금 {counts.BOUND}개가 필수예요.
          {ex.marks.some((m) => m.required === false && m.func === "BOUND") && " 연한 빗금은 있으면 좋은 자리예요."}
        </div>
      </div>

      {/* 함정 · 선수 개념 (있을 때만) */}
      {(ex.traps.length > 0 || ex.discriminates) && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>이 유형에서 조심할 것</div>
          <ul className="rd-ul">
            {ex.traps.map((t, i) => <li key={i}>{t}</li>)}
            {ex.discriminates && <li><span className="sv-small">가르는 지점 · </span>{ex.discriminates}</li>}
          </ul>
        </div>
      )}
      {ex.prereq.length > 0 && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>먼저 알아야 하는 것</div>
          <ul className="rd-ul">{ex.prereq.map((p, i) => <li key={i}><MathText text={p} /></li>)}</ul>
        </div>
      )}

      {/* 방침 (접힘) */}
      {level0 && (level0.text || (Array.isArray(level0.steps) && level0.steps.length > 0)) && (
        <div className="sv-card">
          <details className="rd-details">
            <summary>어떻게 시작할까 (방침) <span className="sv-small">· 답은 안 보여 줘요</span></summary>
            <div className="body">
              {level0.text && <MathText as="p" text={maskAnswer(level0.text, item)} style={{ margin: 0 }} />}
              {Array.isArray(level0.steps) && level0.steps.length > 0 && (
                <ol>{level0.steps.map((s, i) => <li key={i}><MathText text={maskAnswer(s, item)} /></li>)}</ol>
              )}
            </div>
          </details>
        </div>
      )}

      {/* 행동 */}
      <div className="rd-actions">
        <button className="sv-btn pri" disabled={!eligible} onClick={() => { location.hash = `#/solve/mark/${item.id}`; }}>
          이 문장으로 표시 연습
        </button>
        <button className="sv-btn" onClick={() => { location.hash = `#/solve/item/${item.id}`; }}>이 문제 풀기</button>
        <button className="sv-btn" onClick={() => askAboutItem(item)}>질문하기</button>
        <button className="sv-btn ghost" onClick={() => { location.hash = "#/solve/read"; }}>다른 문항</button>
      </div>
      {!eligible && <div className="sv-small" style={{ marginTop: 8 }}>이 문장은 짧아서 표시 연습은 건너뛰어요. 조건이 여러 개인 문항에서 연습할 수 있어요.</div>}
    </>
  );
}
