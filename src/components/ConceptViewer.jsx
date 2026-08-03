import { useState, useRef, useEffect, useCallback } from "react";
import { getConcept, getAdoptedQna, askQuestion, listConcepts } from "../lib/concepts";
import { supabase } from "../supabaseClient";
import { qcode } from "../lib/qcode";
import QuestionChat from "./QuestionChat";
import { AnimScene } from "./AnimFigure";

// 개념 뷰어: concepts.blocks(jsonb) 렌더링 + 채택 QnA 말풍선 + 질문 접수
// props: conceptId, theme('light'|'dark')

const TONES = {
  teal:  { l: ["#F0FDFA","#99F6E4","#0F766E","#0D9488","#CCFBF1"], d: ["#0E2B27","#1E4C44","#5EEAD4","#14B8A6","#134E48"] },
  amber: { l: ["#FFFBEB","#FDE68A","#B45309","#F59E0B","#FEF3C7"], d: ["#2B230D","#584717","#FCD34D","#F59E0B","#4A3B10"] },
  coral: { l: ["#FEF2F2","#FECACA","#DC2626","#EF4444","#FEE2E2"], d: ["#2C1414","#5C2626","#FCA5A5","#EF4444","#4C1D1D"] },
  violet:{ l: ["#F5F3FF","#DDD6FE","#6D28D9","#8B5CF6","#EDE9FE"], d: ["#1E1533","#3E2D63","#C4B5FD","#8B5CF6","#332557"] },
  slate: { l: ["#FFFFFF","#E2E8F0","#334155","#475569","#E2E8F0"], d: ["#16181D","#2A2E36","#CBD5E1","#64748B","#262B33"] },
};
const SIZES = { sm: { pad: 12, body: 13, head: 15 }, md: { pad: 16, body: 14.5, head: 17 }, lg: { pad: 24, body: 16.5, head: 20 } };

function tone(t, theme) {
  const [bg, border, text, solid, hl] = (TONES[t] || TONES.slate)[theme === "dark" ? "d" : "l"];
  return { bg, border, text, solid, hl };
}

const CSS = `
.cv-root { min-height: 100vh; padding: 24px 12px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.cv-root * { box-sizing: border-box; }
.cv-light { background: #EDEFF2; --surface: #F8FAFC; --surface-bd: #E2E8F0; --ink: #1F2937; --mut: #94A3B8;
  --head-bg: linear-gradient(135deg, #115E59, #0F766E 55%, #134E4A); --bubble: #1E293B; --bubble-tx: #F1F5F9; }
.cv-dark { background: #0B0C0F; --surface: #111318; --surface-bd: #23262D; --ink: #E2E8F0; --mut: #6B7280;
  --head-bg: linear-gradient(135deg, #0D2B28, #123B36 55%, #0A1F1C); --bubble: #262B33; --bubble-tx: #E5E9F0; }
.cv-wrap { max-width: 768px; margin: 0 auto; }
.cv-cover { position: relative; border-radius: 16px 16px 0 0; overflow: hidden; background: var(--head-bg); }
.cv-cover-body { position: relative; padding: 22px 20px; color: #fff; }
.cv-eyebrow { font-size: 11px; letter-spacing: 2px; color: #99F6E4; font-weight: 700; margin: 0; }
.cv-crumb { cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }
.cv-backlist { position: absolute; top: 14px; right: 14px; background: rgba(255,255,255,.16);
  border: 1px solid rgba(255,255,255,.4); color: #fff; border-radius: 999px; font-size: 12px;
  font-weight: 700; padding: 6px 12px; cursor: pointer; }
.cv-pn { display: flex; border: 1px solid rgba(127,127,127,.3); border-radius: 12px; overflow: hidden; }
.cv-pnbtn { flex: 1; background: transparent; border: none; padding: 13px 12px; font-size: 12.5px;
  color: var(--ink); cursor: pointer; text-align: left; min-width: 0; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap; }
.cv-pnbtn b { margin: 0 3px; }
.cv-pnbtn.r { text-align: right; border-left: 1px solid rgba(127,127,127,.3); }
.cv-pnbtn:disabled { opacity: .35; cursor: default; }
.cv-title { font-size: 25px; font-weight: 800; margin: 4px 0 0; }
.cv-subtitle { font-size: 13px; color: rgba(240,253,250,.85); margin: 4px 0 0; }
.cv-main { background: var(--surface); border: 1px solid var(--surface-bd); border-top: none;
  border-radius: 0 0 16px 16px; padding: 20px 16px; display: grid; grid-template-columns: 1fr; gap: 16px; }
/* 1행 1박스 원칙 — 반쪽 배치 제거 */
.cv-bh { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
.cv-bh-l { display: flex; align-items: center; gap: 8px; min-width: 0; }
.cv-icon { width: 28px; height: 28px; border-radius: 9999px; display: flex; align-items: center; justify-content: center;
  font-size: 15px; flex-shrink: 0; border: 1px solid; }
.cv-label { font-size: 12px; font-weight: 700; letter-spacing: 1px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cv-card { overflow: hidden; border-radius: 12px; border: 1px solid; }
.cv-p { line-height: 1.65; margin: 0 0 8px; } .cv-p:last-child { margin-bottom: 0; }
.cv-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.cv-chip { min-width: 32px; height: 30px; padding: 0 10px; border-radius: 6px; color: #fff;
  font-size: 13px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center;
  white-space: nowrap; max-width: 100%; }
.cv-chiplab { margin: 12px 0 0; font-size: 11px; color: var(--mut); }
.cv-warn { display: flex; gap: 10px; margin-bottom: 10px; } .cv-warn:last-child { margin-bottom: 0; }
.cv-bang { margin-top: 3px; flex-shrink: 0; width: 20px; height: 20px; border-radius: 9999px; color: #fff;
  font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.cv-fig { margin: 12px 0 0; } .cv-fig img { width: 100%; max-height: 256px; object-fit: contain; border-radius: 8px; display: block; }
.cv-fig figcaption { margin-top: 4px; font-size: 11px; color: var(--mut); text-align: center; }
.cv-panelbar { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 12px; }
.cv-pbtn { background: transparent; border-style: solid; border-radius: 999px;
  font-size: 12.5px; font-weight: 700; padding: 7px 13px; cursor: pointer; transition: all .15s ease; }
.cv-pbtn.on { font-weight: 800; }
.cv-panel { margin-top: 10px; border-style: solid; border-radius: 12px; padding: 12px 14px 13px;
  background: rgba(127,127,127,.03); }
.cv-ph { display: flex; align-items: center; margin: 0 0 9px; }
.cv-picon { width: 26px; height: 26px; border-radius: 8px; border: 1px solid; display: flex;
  align-items: center; justify-content: center; font-size: 14px; }
.cv-pfold { margin-left: auto; width: 26px; height: 26px; border-radius: 8px; border: 1px solid;
  background: transparent; cursor: pointer; font-size: 11px; line-height: 1; padding: 0; }
.cv-panel .cv-p { margin: 0 0 9px; }
.cv-panel .cv-p:last-child { margin-bottom: 0; }
.cv-grid { display: flex; flex-wrap: wrap; gap: 6px; }
.cv-gitem { border: 1px solid var(--bd); border-radius: 8px; padding: 5px 9px; font-size: 12.5px;
  color: var(--ink); background: var(--card); line-height: 1.5; }
.cv-plinks { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 10px; }
.cv-plink { background: var(--card); border: 1.5px solid var(--ac); border-radius: 10px; color: var(--ac);
  font-size: 12.5px; font-weight: 800; padding: 8px 12px; cursor: pointer; }
.cv-extwrap { margin-top: 18px; }
.cv-twrap { overflow-x: auto; margin-top: 8px; }
.cv-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.cv-table th, .cv-table td { border: 1px solid var(--bd); padding: 5px 9px; color: var(--ink); text-align: left; line-height: 1.5; }
.cv-table th { background: rgba(127,127,127,.07); font-weight: 800; white-space: nowrap; }
.cv-table td:first-child { white-space: nowrap; }
.cv-sp { height: 10px; }
.cv-qcode { font-size: 10.5px; font-weight: 800; letter-spacing: .5px; color: var(--mut);
  opacity: .8; align-self: center; margin-right: 7px; white-space: nowrap; }
.cv-qmark { position: relative; width: 28px; height: 28px; border-radius: 9999px; font-size: 14px; font-weight: 700;
  text-decoration: none; box-sizing: border-box;
  flex-shrink: 0; cursor: pointer; display: flex; align-items: center; justify-content: center;
  background: transparent; color: #14B8A6; border: 2px solid #2DD4BF; }
.cv-qmark.on { background: #0D9488; color: #fff; }
.cv-qbadge { position: absolute; top: -5px; right: -5px; width: 16px; height: 16px; border-radius: 9999px;
  background: #EF4444; color: #fff; font-size: 10px; display: flex; align-items: center; justify-content: center; }
.cv-bubblewrap { position: relative; margin-top: 12px; }
.cv-tail { position: absolute; top: -7px; right: 16px; width: 14px; height: 14px; transform: rotate(45deg); background: var(--bubble); }
.cv-bubble { border-radius: 12px; background: var(--bubble); color: var(--bubble-tx); padding: 16px; }
.cv-btag { font-size: 11px; letter-spacing: 1px; color: #5EEAD4; font-weight: 700; }
.cv-close { background: none; border: none; color: #94A3B8; cursor: pointer; font-size: 14px; padding: 2px 4px; }
.cv-q { font-weight: 700; font-size: 14px; margin: 0; } .cv-a { margin: 4px 0 12px; font-size: 13.5px; line-height: 1.6; opacity: .88; }
.cv-ask { display: flex; gap: 6px; margin-top: 10px; }
.cv-ask input { flex: 1; background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.15);
  border-radius: 8px; color: inherit; font-size: 13px; padding: 8px 10px; outline: none; }
.cv-ask button { background: #0D9488; color: #fff; border: none; border-radius: 8px; font-size: 12.5px;
  font-weight: 700; padding: 8px 12px; cursor: pointer; }
.cv-btn { margin-top: 12px; padding: 8px 16px; border-radius: 8px; border: none; color: #fff;
  font-size: 13px; font-weight: 700; cursor: pointer; }
.cv-anschips { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; }
.cv-anschip { padding: 8px 12px; border-radius: 8px; border: 1px solid; font-size: 13.5px; }
.cv-footer { display: flex; justify-content: space-between; font-size: 11px; color: var(--mut); padding-top: 4px; }
mark.cv-hl { border-radius: 4px; padding: 1px 4px; }
`;

function Rich({ text, tn, theme }) {
  const t = tone(tn, theme);
  const parts = String(text).split(/(\*\*(?:(?!\*\*).)+\*\*|==(?:(?!==).)+==|\[\[\w+:[^\]]+\]\])/g);
  return (<>{parts.map((p, i) => {
    if (/^\*\*(?:(?!\*\*).)+\*\*$/.test(p)) return <b key={i} style={{ color: "var(--ink)" }}>{p.slice(2,-2)}</b>;
    if (/^==(?:(?!==).)+==$/.test(p)) return <mark key={i} className="cv-hl" style={{ background: t.hl, color: "var(--ink)" }}>{p.slice(2,-2)}</mark>;
    const m = p.match(/^\[\[(\w+):([^\]]+)\]\]$/);
    if (m && TONES[m[1]]) return <span key={i} style={{ fontWeight: 700, color: tone(m[1], theme).text }}>{m[2]}</span>;
    return <span key={i}>{p}</span>;
  })}</>);
}

function Panels({ panels, figure, conceptId, blockId, isAdmin, theme, sz }) {
  const [open, setOpen] = useState({});
  if (!panels?.length) return null;
  const PTONES = ["amber", "teal", "coral", "slate"];
  const toggle = (id) => setOpen((s) => ({ ...s, [id]: !s[id] }));
  return (
    <>
      <div className="cv-panelbar">
        {panels.map((p, pi) => {
          const t = tone(p.tone || PTONES[pi % PTONES.length], theme);
          const on = !!open[p.id];
          return (
            <button key={p.id} className={"cv-pbtn" + (on ? " on" : "")}
              style={{
                borderColor: on ? t.solid : t.border,
                borderWidth: on ? 2 : 1.5,
                color: on ? t.text : "var(--mut)",
                background: on ? t.bg : "transparent",
              }}
              onClick={() => toggle(p.id)}>
              {p.title} {on ? "▴" : "▾"}
            </button>
          );
        })}
      </div>
      {panels.map((p, pi) => {
        if (!open[p.id]) return null;
        const t = tone(p.tone || PTONES[pi % PTONES.length], theme);
        const icon = p.icon || p.title.trim().split(" ")[0];
        return (
          <div key={p.id} className="cv-panel" style={{ borderColor: t.solid, borderWidth: 1.5 }}>
            <div className="cv-ph">
              <span className="cv-picon" style={{ background: t.bg, borderColor: t.border }}>{icon}</span>
              <button className="cv-pfold" style={{ color: t.solid, borderColor: t.border }}
                aria-label="접기" title="접기" onClick={() => toggle(p.id)}>▲</button>
            </div>
            {(p.lines || []).map((l, i) => {
              if (l === "") return <div key={i} className="cv-sp" />;
              const fm = typeof l === "string" && l.match(/^\[\[fig:([\w-]+)\]\]$/);
              if (fm) return <AnimScene key={i} sceneId={fm[1]} figure={figure} conceptId={conceptId} blockId={blockId} isAdmin={isAdmin} theme={theme} />;
              return <p key={i} className="cv-p" style={{ fontSize: (sz?.body || 15) - 0.5, color: "var(--ink)" }}><Rich text={l} tn={p.tone || PTONES[pi % PTONES.length]} theme={theme} /></p>;
            })}
            {p.kind === "table" && p.table && (
              <div className="cv-twrap">
                <table className="cv-table">
                  <thead><tr>{p.table.headers.map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
                  <tbody>
                    {p.table.rows.map((r, ri) => (
                      <tr key={ri}>{r.map((c, ci) => <td key={ci}><Rich text={String(c)} tn={p.tone || "slate"} theme={theme} /></td>)}</tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {p.kind === "grid" && (
              <div className="cv-grid">{(p.items || []).map((it, i) => <span key={i} className="cv-gitem"><Rich text={it} tn={p.tone || "slate"} theme={theme} /></span>)}</div>
            )}
            {p.links?.length > 0 && (
              <div className="cv-plinks">
                {p.links.map((lk) => (
                  <button key={lk.id} className="cv-plink" onClick={() => (location.hash = `#/c/${encodeURIComponent(lk.id)}`)}
                    style={{ borderColor: t.solid, color: t.text }}>
                    {lk.label} →
                  </button>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </>
  );
}

function Figure({ figure, conceptId, blockId, isAdmin, theme }) {
  if (figure?.kind === "animset") return null; // animset은 본문 [[fig:씬id]] 마커 자리에서 렌더
  if (!figure?.src) return null;
  return (
    <figure className="cv-fig">
      <img src={figure.src} alt={figure.alt || ""} />
      {figure.caption && <figcaption>{figure.caption}</figcaption>}
    </figure>
  );
}

function TextBlock({ b, sz, t, theme, conceptId, isAdmin }) {
  return (
    <div className="cv-card" style={{ background: t.bg, borderColor: t.border, padding: sz.pad }}>
      {b.lines.map((l, i) => {
        if (l === "") return <div key={i} className="cv-sp" />;
        const fm = typeof l === "string" && l.match(/^\[\[fig:([\w-]+)\]\]$/);
        if (fm) return <AnimScene key={i} sceneId={fm[1]} figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} />;
        return <p key={i} className="cv-p" style={{ fontSize: sz.body, color: "var(--ink)" }}><Rich text={l} tn={b.style?.tone} theme={theme} /></p>;
      })}
<Figure figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} />
      <Panels panels={b.panels} figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} sz={sz} />
    </div>
  );
}
function DefinitionBlock({ b, sz, t, theme, conceptId, isAdmin }) {
  return (
    <div className="cv-card" style={{ background: t.bg, borderColor: t.border, padding: sz.pad }}>
      <p style={{ fontSize: sz.head, lineHeight: 1.45, color: "var(--ink)", margin: 0 }}>
        <b style={{ color: t.text }}>{b.term}</b>
        <span style={{ color: "var(--mut)", fontSize: 12, marginLeft: 4 }}>{b.hanja}</span>
        <span style={{ margin: "0 6px", color: "var(--mut)" }}>:</span>
        <Rich text={b.text} tn={b.style?.tone} theme={theme} />
      </p>
      <p className="cv-chiplab">{b.chipLabel}</p>
      <div className="cv-chips">{b.chips?.map((n) => <span key={n} className="cv-chip" style={{ background: t.solid }}>{n}</span>)}</div>
      <Figure figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} />
      <Panels panels={b.panels} figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} sz={sz} />
    </div>
  );
}
function WarningBlock({ b, sz, t, theme, conceptId, isAdmin }) {
  return (
    <div className="cv-card" style={{ background: t.bg, borderColor: t.border, padding: sz.pad }}>
      {b.items.map((it, i) => (
        <div key={i} className="cv-warn">
          <span className="cv-bang" style={{ background: t.solid }}>!</span>
          <p className="cv-p" style={{ fontSize: sz.body, margin: 0, color: "var(--ink)" }}><Rich text={it} tn={b.style?.tone} theme={theme} /></p>
        </div>
      ))}
      <Figure figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} />
      <Panels panels={b.panels} figure={b.figure} conceptId={conceptId} blockId={b.id} isAdmin={isAdmin} theme={theme} sz={sz} />
    </div>
  );
}
function CheckBlock({ b, sz, t, theme, conceptId, isAdmin }) {
  const [show, setShow] = useState(false);
  return (
    <div className="cv-card" style={{ background: "var(--surface)", borderColor: t.border, padding: sz.pad }}>
      <p style={{ fontSize: sz.head, fontWeight: 600, color: "var(--ink)", margin: 0 }}><Rich text={b.question} tn={b.style?.tone} theme={theme} /></p>
      <button className="cv-btn" style={{ background: t.solid }} onClick={() => setShow((v) => !v)}>
        {show ? "정답 가리기" : "먼저 풀어 본 다음, 정답 보기"}
      </button>
      {show && (
        <div className="cv-anschips">
          {b.answer.map((a) => {
            const at = tone(a.tone, theme);
            return <span key={a.group} className="cv-anschip" style={{ background: at.bg, borderColor: at.border }}>
              <b style={{ color: at.text }}>{a.group}</b><span style={{ color: "var(--ink)", marginLeft: 8 }}>{a.nums}</span></span>;
          })}
        </div>
      )}
    </div>
  );
}
function ImageBlock({ b, sz, t }) {
  return (
    <div className="cv-card" style={{ background: "var(--surface)", borderColor: t.border, padding: sz.pad }}>
      {b.src ? <img src={b.src} alt={b.alt} style={{ width: "100%", maxHeight: 320, objectFit: "contain", borderRadius: 8, display: "block" }} />
        : <div style={{ height: 128, borderRadius: 8, border: `1px dashed ${t.border}`, background: t.bg,
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, color: "var(--mut)" }}>이미지 준비 중</div>}
      {b.caption && <p style={{ margin: "8px 0 0", fontSize: 12, color: "var(--mut)" }}>{b.caption}</p>}
    </div>
  );
}
const RENDER = { text: TextBlock, definition: DefinitionBlock, warning: WarningBlock, check: CheckBlock, image: ImageBlock };

// 관리자 도구용: 학생 화면과 동일한 단락 미리보기 (물음표·질문 말풍선 제외)
export function BlockPreview({ b, theme = "light" }) {
  if (!b) return null;
  const st = b.style || {};
  const t = tone(st.tone, theme);
  const sz = SIZES[st.size] || SIZES.md;
  const R = RENDER[b.type];
  return (
    <div className={"cv-" + theme} style={{ background: "transparent" }}>
      <style>{CSS}</style>
      <section>
        <div className="cv-bh">
          <div className="cv-bh-l">
            {b.icon && (b.icon.kind === "image" && b.icon.src
              ? <img className="cv-icon" src={b.icon.src} alt="" style={{ objectFit: "cover", borderColor: t.border }} />
              : <span className="cv-icon" style={{ background: t.bg, borderColor: t.border }}>{b.icon.value}</span>)}
            <h2 className="cv-label" style={{ color: t.text }}>{b.label}</h2>
          </div>
        </div>
        {R ? <R b={b} sz={sz} t={t} theme={theme} conceptId={conceptId} isAdmin={isAdmin} />
           : <p style={{ color: "var(--mut)", fontSize: 13 }}>알 수 없는 단락 유형: {String(b.type)}</p>}
      </section>
    </div>
  );
}

function BlockShell({ b, qna, theme, conceptId, isAdmin, onAsk }) {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [sent, setSent] = useState(false);
  const ref = useRef(null);
  useEffect(() => {
    if (!open) return;
    const h = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, [open]);

  const st = b.style || {};
  const t = tone(st.tone, theme);
  const sz = SIZES[st.size] || SIZES.md;
  const R = RENDER[b.type];
  if (!R) return null;

  const send = async () => {
    const text = q.trim();
    if (!text) return;
    try { await askQuestion(conceptId, b.id, text); setSent(true); setQ(""); }
    catch { /* 접수 실패 시 조용히 유지 */ }
  };

  return (
    <section ref={ref} className={st.width === "half" ? "" : "cv-span2"} style={{ position: "relative" }}>
      <div className="cv-bh">
        <div className="cv-bh-l">
          {b.icon && (b.icon.kind === "image" && b.icon.src
            ? <img className="cv-icon" src={b.icon.src} alt="" style={{ objectFit: "cover", borderColor: t.border }} />
            : <span className="cv-icon" style={{ background: t.bg, borderColor: t.border }}>{b.icon.value}</span>)}
          <h2 className="cv-label" style={{ color: t.text }}>{b.label}</h2>
        </div>
        <span className="cv-qcode">{qcode(conceptId, b.id)}</span>
        <button className="cv-qmark" onClick={() => onAsk(b)} aria-label="질문하기">
          ?{qna.length > 1 && <span className="cv-qbadge">{qna.length}</span>}
        </button>
      </div>
      <R b={b} sz={sz} t={t} theme={theme} conceptId={conceptId} isAdmin={isAdmin} />
      {open && (
        <div className="cv-bubblewrap">
          <div className="cv-tail" />
          <div className="cv-bubble">
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span className="cv-btag">친구들이 했던 질문</span>
              <button className="cv-close" onClick={() => setOpen(false)} aria-label="닫기">✕</button>
            </div>
            {qna.length === 0 && <p className="cv-a" style={{ margin: 0 }}>아직 채택된 질문이 없어요. 첫 질문의 주인공이 되어 볼까요?</p>}
            {qna.map((it) => (<div key={it.id}><p className="cv-q">Q. {it.question}</p><p className="cv-a">{it.answer}</p></div>))}
            {sent ? <p className="cv-a" style={{ margin: 0, color: "#5EEAD4" }}>질문이 접수됐어요! 선생님 확인 후 여기에 올라와요.</p> : (
              <div className="cv-ask">
                <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="이 부분에서 궁금한 점 물어보기"
                  onKeyDown={(e) => e.key === "Enter" && send()} />
                <button onClick={send}>질문 보내기</button>
              </div>
            )}
          </div>
        </div>
      )}
    </section>
  );
}

export default function ConceptViewer({ conceptId, theme = "light" }) {
  const [concept, setConcept] = useState(null);
  const [qna, setQna] = useState([]);
  const [err, setErr] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [chatBlock, setChatBlock] = useState(null); // 질문챗이 열린 단락
  const [sibs, setSibs] = useState([]);             // 같은 학기 개념 목록 (이전/다음용)
  useEffect(() => { window.scrollTo(0, 0); }, [conceptId]);
  useEffect(() => {
    if (!concept?.unit_id) return;
    listConcepts().then((all) => {
      setSibs(all.filter((x) => x.unit_id === concept.unit_id).sort((a, b) => a.sort_order - b.sort_order));
    }).catch(() => {});
  }, [concept?.unit_id]);
  const goHome = (focus) => { sessionStorage.setItem("home_focus", focus); location.hash = "#/learn"; };
  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      if (!data?.user) return;
      const { data: prof } = await supabase.from("profiles").select("role").eq("id", data.user.id).maybeSingle();
      setIsAdmin(prof?.role === "admin");
    });
  }, []);

  const load = useCallback(async () => {
    try {
      const [c, q] = await Promise.all([getConcept(conceptId), getAdoptedQna(conceptId)]);
      setConcept(c); setQna(q);
    } catch { setErr("개념을 불러오지 못했어요. 잠시 후 다시 시도해 주세요."); }
  }, [conceptId]);
  useEffect(() => { load(); }, [load]);

  if (err) return <div className={`cv-root cv-${theme}`}><style>{CSS}</style><p style={{ color: "var(--mut)", textAlign: "center" }}>{err}</p></div>;
  if (!concept) return <div className={`cv-root cv-${theme}`}><style>{CSS}</style></div>;

  const byBlock = (id) => qna.filter((q) => q.block_id === id);
  return (
    <div className={`cv-root cv-${theme}`}>
      <style>{CSS}</style>
      <div className="cv-wrap">
        <header className="cv-cover">
          {concept.cover?.src && <img src={concept.cover.src} alt="" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: .45 }} />}
          <div className="cv-cover-body">
            <button className="cv-backlist" onClick={() => goHome(concept.id)}>← 목록</button>
            <p className="cv-eyebrow">
              <span className="cv-crumb" onClick={() => goHome(concept.unit_id)}>{concept.unit_id.toUpperCase()}</span>
              {" · "}
              <span className="cv-crumb" onClick={() => goHome(concept.id)}>개념 {String(concept.sort_order).padStart(2, "0")}</span>
            </p>
            <h1 className="cv-title">{concept.title}</h1>
            <p className="cv-subtitle">{concept.subtitle}</p>
          </div>
        </header>
        <main className="cv-main">
          {concept.blocks.map((b) => <BlockShell key={b.id} b={b} qna={byBlock(b.id)} theme={theme} conceptId={conceptId} isAdmin={isAdmin} onAsk={setChatBlock} />)}
          <a className="cv-span2" href={`#/p/${encodeURIComponent(concept.id)}`}
            style={{ display: "block", textAlign: "center", padding: "14px 0", borderRadius: 12,
              background: "#0D9488", color: "#fff", fontWeight: 800, fontSize: 15, textDecoration: "none" }}>
            ✏️ 예제·유제 풀러 가기
          </a>
          <footer className="cv-footer cv-span2">
            <span>물음표 ? 를 누르면 질문을 보거나 보낼 수 있어요</span><span>{concept.id}</span>
          </footer>
        </main>
      </div>
      {sibs.length > 0 && (() => {
        const idx = sibs.findIndex((s) => s.id === concept.id);
        const prev = idx > 0 ? sibs[idx - 1] : null;
        const next = idx >= 0 && idx < sibs.length - 1 ? sibs[idx + 1] : null;
        return (
          <div className="cv-pn cv-span2" style={{ marginTop: 4 }}>
            <button className="cv-pnbtn" disabled={!prev}
              onClick={() => prev && (location.hash = `#/c/${encodeURIComponent(prev.id)}`)}>
              {prev ? <>← <b>{String(prev.sort_order).padStart(2, "0")}</b>{prev.title}</> : "첫 개념이에요"}
            </button>
            <button className="cv-pnbtn r" disabled={!next}
              onClick={() => next && (location.hash = `#/c/${encodeURIComponent(next.id)}`)}>
              {next ? <><b>{String(next.sort_order).padStart(2, "0")}</b>{next.title} →</> : "마지막 개념이에요"}
            </button>
          </div>
        );
      })()}
      {concept.ext_panels?.length > 0 && (
        <div className="cv-extwrap">
          <Panels panels={concept.ext_panels} figure={concept.ext_figure || null}
            conceptId={conceptId} blockId="ext" isAdmin={isAdmin} theme={theme} />
        </div>
      )}
      {chatBlock && (
        <QuestionChat conceptId={conceptId} block={chatBlock} theme={theme} isAdmin={isAdmin}
          answered={byBlock(chatBlock.id)} onClose={() => setChatBlock(null)} />
      )}
    </div>
  );
}
