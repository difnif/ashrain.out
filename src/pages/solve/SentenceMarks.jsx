// 문장 표시 렌더러 — 토큰을 원문 그대로 이어 붙이고 표시(동그라미·밑줄·빗금·강조·구분)를 덧그린다.
// 문장 해설(Read)·표시 연습(Mark) 공용. 표시 위치는 marking.js 의 토큰 인덱스.
//   tokens      tokenize() 결과
//   marks       [{kind:"span", t0, t1, func} | {kind:"point", t0, func}]  (func: NUM SCALE BOUND EMPH DIST)
//   selectable  true 면 토큰이 탭 대상 → onTokenTap(i)
//   selection   [t0, t1] 강조 배경 (마지막으로 만든 표시 범위)
//   diff        { hit:[mark], missed:[mark], extra:[mark] } — 채점 결과 색(초록·빨간 점선·회색)
//   onMarkTap   표시된 토큰·빗금을 탭했을 때 (mark) => void  (selectable 이 아닐 때 토큰 탭은 여기로)
import { Fragment, useEffect, useMemo } from "react";
import { mathHtml, ensureMathCss } from "../../components/MathText";
import { markKey } from "../../lib/marking.js";

const CSS = `
.sm-wrap{--sm-num:#E8590C;--sm-scale:#1971C2;--sm-bound:#7048E8;--sm-emph:#C2255C;--sm-dist:#099268;
  font-size:17px;line-height:2.25;word-break:keep-all;overflow-wrap:anywhere;padding:4px 2px;color:var(--text);user-select:none;-webkit-user-select:none}
.sm-t{display:inline;padding:4px 1px;border-radius:6px;-webkit-tap-highlight-color:transparent;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sm-k-space{white-space:pre-wrap}
.sm-k-num{white-space:nowrap}
.sm-sel .sm-tap{cursor:pointer}
.sm-sel .sm-tap:active{background:var(--surface2)}
.sm-hit-tap{cursor:pointer}
.sm-on{background:color-mix(in srgb,var(--accent) 18%,transparent)}
/* NUM 동그라미 — 여러 토큰이면 양 끝만 둥글게 */
.sm-num{border-top:2px solid var(--sm-num);border-bottom:2px solid var(--sm-num);padding-top:3px;padding-bottom:3px}
.sm-num-s{border-left:2px solid var(--sm-num);border-top-left-radius:999px;border-bottom-left-radius:999px;padding-left:7px}
.sm-num-e{border-right:2px solid var(--sm-num);border-top-right-radius:999px;border-bottom-right-radius:999px;padding-right:7px}
.sm-num-hit{border-color:var(--good)}
.sm-num-miss{border-color:var(--bad);border-style:dashed}
.sm-num-extra{border-color:var(--muted);opacity:.85}
/* SCALE 밑줄 */
.sm-scale{box-shadow:inset 0 -3px 0 var(--sm-scale);padding-bottom:1px}
.sm-scale-hit{box-shadow:inset 0 -3px 0 var(--good)}
.sm-scale-miss{box-shadow:none;border-bottom:3px dashed var(--bad)}
.sm-scale-extra{box-shadow:inset 0 -3px 0 var(--muted)}
/* EMPH 두 줄 · DIST 물결 (2층 · 채점 안 함) */
.sm-emph{text-decoration:underline double var(--sm-emph);text-decoration-thickness:2px;text-underline-offset:5px}
.sm-dist{text-decoration:underline wavy var(--sm-dist);text-underline-offset:4px}
/* BOUND 빗금 — 토큰 뒤에 끼워 넣는 글리프 */
.sm-bound{display:inline-block;color:var(--sm-bound);font-weight:900;padding:2px 3px;margin:0 1px;cursor:pointer;line-height:1;vertical-align:-1px;font-size:1.1em;-webkit-tap-highlight-color:transparent;border-radius:4px}
.sm-bound.sm-bonus{opacity:.65}
.sm-bound-hit{color:var(--good)}
.sm-bound-miss{color:var(--bad);outline:2px dashed var(--bad);outline-offset:-1px}
.sm-bound-extra{color:var(--muted)}
.sm-legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px;color:var(--muted);margin-top:6px}
.sm-legend .sm-t{font-size:14px;line-height:1.9;color:var(--text)}
`;

const PRIORITY = { NUM: 0, SCALE: 1, BOUND: 2, EMPH: 3, DIST: 4 };
const pickMark = (list) => list.slice().sort((a, b) => (PRIORITY[a.func] ?? 9) - (PRIORITY[b.func] ?? 9))[0];

export default function SentenceMarks({ tokens = [], marks = [], selectable = false, onTokenTap, selection = null, diff = null, onMarkTap, className = "", style }) {
  useEffect(ensureMathCss, []);

  // 채점 상태: 표시 → hit | miss | extra
  const state = useMemo(() => {
    const m = new Map();
    if (!diff) return m;
    for (const mk of diff.extra || []) m.set(markKey(mk), "extra");
    for (const mk of diff.missed || []) m.set(markKey(mk), "miss");
    for (const mk of diff.hit || []) m.set(markKey(mk), "hit");
    return m;
  }, [diff]);
  const stOf = (mk) => state.get(markKey(mk)) || "";

  // 토큰별 span 표시 클래스
  const info = useMemo(() => {
    const out = tokens.map(() => ({ cls: [], marks: [] }));
    for (const mk of marks) {
      if (mk.kind !== "span") continue;
      const f = String(mk.func || "").toLowerCase();
      const st = stOf(mk);
      for (let i = mk.t0; i <= mk.t1 && i < tokens.length; i++) {
        const o = out[i]; if (!o) continue;
        o.marks.push(mk);
        o.cls.push(`sm-${f}`);
        if (i === mk.t0) o.cls.push(`sm-${f}-s`);
        if (i === mk.t1) o.cls.push(`sm-${f}-e`);
        if (st) o.cls.push(`sm-${f}-${st}`);
      }
    }
    return out;
  }, [tokens, marks, state]);

  // 토큰 뒤 빗금
  const points = useMemo(() => {
    const m = new Map();
    for (const mk of marks) if (mk.kind === "point") { if (!m.has(mk.t0)) m.set(mk.t0, []); m.get(mk.t0).push(mk); }
    return m;
  }, [marks]);

  return (
    <div className={"sm-wrap" + (selectable ? " sm-sel" : "") + (className ? " " + className : "")} style={style}>
      <style>{CSS}</style>
      {tokens.map((t) => {
        if (t.kind === "newline") return <br key={t.i} />;
        const o = info[t.i] || { cls: [], marks: [] };
        const tappable = t.kind !== "space";
        const inSel = selection && t.i >= selection[0] && t.i <= selection[1];
        let onClick;
        if (tappable) {
          if (selectable && onTokenTap) onClick = () => onTokenTap(t.i);
          else if (onMarkTap && o.marks.length) onClick = () => onMarkTap(pickMark(o.marks));
          else if (onTokenTap) onClick = () => onTokenTap(t.i);
        }
        const cls = ["sm-t", `sm-k-${t.kind}`, ...o.cls, inSel ? "sm-on" : "", selectable && tappable ? "sm-tap" : "", !selectable && onClick ? "sm-hit-tap" : ""].filter(Boolean).join(" ");
        const content = t.kind === "num" || t.kind === "math"
          ? <span dangerouslySetInnerHTML={{ __html: mathHtml(t.text) }} />
          : t.text;
        const pts = points.get(t.i);
        return (
          <Fragment key={t.i}>
            <span className={cls} role={onClick ? "button" : undefined} tabIndex={onClick ? 0 : undefined} onClick={onClick}
              onKeyDown={onClick ? (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onClick(); } } : undefined}>
              {content}
            </span>
            {pts && pts.map((mk, k) => {
              const st = stOf(mk);
              return (
                <span key={k} role="button" tabIndex={0} title={mk.note || "단서 경계"}
                  className={"sm-bound" + (st ? ` sm-bound-${st}` : "") + (mk.required === false ? " sm-bonus" : "")}
                  onClick={() => onMarkTap?.(mk)}
                  onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onMarkTap?.(mk); } }}>／</span>
              );
            })}
          </Fragment>
        );
      })}
    </div>
  );
}

/** 표시 읽는 법 — 작은 범례 (Read·Mark 공용) */
export function MarkLegend({ tier2 = false }) {
  return (
    <div className="sm-wrap sm-legend" style={{ padding: 0 }}>
      <style>{CSS}</style>
      <span><span className="sm-t sm-num sm-num-s sm-num-e">54cm</span> 동그라미 = 숫자 정보</span>
      <span><span className="sm-t sm-scale">둘레</span> 밑줄 = 척도(무엇의 값인지)</span>
      <span>빗금<span className="sm-bound" style={{ cursor: "default" }}>／</span>= 단서 경계</span>
      {tier2 && <span><span className="sm-t sm-emph">구하는 것</span> 두 줄 = 놓치면 틀리는 것 (참고용)</span>}
    </div>
  );
}
