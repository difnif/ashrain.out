import { useState, useRef, useEffect, useCallback } from "react";
import { getConcept, getAdoptedQna, askQuestion } from "../lib/concepts";

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
.cv-title { font-size: 25px; font-weight: 800; margin: 4px 0 0; }
.cv-subtitle { font-size: 13px; color: rgba(240,253,250,.85); margin: 4px 0 0; }
.cv-main { background: var(--surface); border: 1px solid var(--surface-bd); border-top: none;
  border-radius: 0 0 16px 16px; padding: 20px 16px; display: grid; grid-template-columns: 1fr; gap: 16px; }
@media (min-width: 640px) { .cv-main { grid-template-columns: 1fr 1fr; } .cv-span2 { grid-column: span 2; } }
.cv-bh { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
.cv-bh-l { display: flex; align-items: center; gap: 8px; min-width: 0; }
.cv-icon { width: 28px; height: 28px; border-radius: 9999px; display: flex; align-items: center; justify-content: center;
  font-size: 15px; flex-shrink: 0; border: 1px solid; }
.cv-label { font-size: 12px; font-weight: 700; letter-spacing: 1px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cv-card { border-radius: 12px; border: 1px solid; }
.cv-p { line-height: 1.65; margin: 0 0 8px; } .cv-p:last-child { margin-bottom: 0; }
.cv-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.cv-chip { width: 32px; height: 30px; border-radius: 6px; color: #fff; font-size: 13px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; }
.cv-chiplab { margin: 12px 0 0; font-size: 11px; color: var(--mut); }
.cv-warn { display: flex; gap: 10px; margin-bottom: 10px; } .cv-warn:last-child { margin-bottom: 0; }
.cv-bang { margin-top: 3px; flex-shrink: 0; width: 20px; height: 20px; border-radius: 9999px; color: #fff;
  font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.cv-fig { margin: 12px 0 0; } .cv-fig img { width: 100%; max-height: 256px; object-fit: contain; border-radius: 8px; display: block; }
.cv-fig figcaption { margin-top: 4px; font-size: 11px; color: var(--mut); text-align: center; }
.cv-qmark { position: relative; width: 28px; height: 28px; border-radius: 9999px; font-size: 14px; font-weight: 700;
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

function Figure({ figure }) {
  if (!figure?.src) return null;
  return (
    <figure className="cv-fig">
      <img src={figure.src} alt={figure.alt || ""} />
      {figure.caption && <figcaption>{figure.caption}</figcaption>}
    </figure>
  );
}

function TextBlock({ b, sz, t, theme }) {
  return (
    <div className="cv-card" style={{ background: t.bg, borderColor: t.border, padding: sz.pad }}>
      {b.lines.map((l, i) => <p key={i} className="cv-p" style={{ fontSize: sz.body, color: "var(--ink)" }}><Rich text={l} tn={b.style?.tone} theme={theme} /></p>)}
      <Figure figure={b.figure} />
    </div>
  );
}
function DefinitionBlock({ b, sz, t, theme }) {
  return (
    <div className="cv-card" style={{ background: t.bg, borderColor: t.border, padding: sz.pad, height: "100%" }}>
      <p style={{ fontSize: sz.head, lineHeight: 1.45, color: "var(--ink)", margin: 0 }}>
        <b style={{ color: t.text }}>{b.term}</b>
        <span style={{ color: "var(--mut)", fontSize: 12, marginLeft: 4 }}>{b.hanja}</span>
        <span style={{ margin: "0 6px", color: "var(--mut)" }}>:</span>
        <Rich text={b.text} tn={b.style?.tone} theme={theme} />
      </p>
      <p className="cv-chiplab">{b.chipLabel}</p>
      <div className="cv-chips">{b.chips?.map((n) => <span key={n} className="cv-chip" style={{ background: t.solid }}>{n}</span>)}</div>
      <Figure figure={b.figure} />
    </div>
  );
}
function WarningBlock({ b, sz, t, theme }) {
  return (
    <div className="cv-card" style={{ background: t.bg, borderColor: t.border, padding: sz.pad }}>
      {b.items.map((it, i) => (
        <div key={i} className="cv-warn">
          <span className="cv-bang" style={{ background: t.solid }}>!</span>
          <p className="cv-p" style={{ fontSize: sz.body, margin: 0, color: "var(--ink)" }}><Rich text={it} tn={b.style?.tone} theme={theme} /></p>
        </div>
      ))}
      <Figure figure={b.figure} />
    </div>
  );
}
function CheckBlock({ b, sz, t, theme }) {
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

function BlockShell({ b, qna, theme, conceptId }) {
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
        <button className={"cv-qmark" + (open ? " on" : "")} onClick={() => setOpen((v) => !v)}
          aria-label="질문 보기/하기">
          ?{qna.length > 1 && <span className="cv-qbadge">{qna.length}</span>}
        </button>
      </div>
      <R b={b} sz={sz} t={t} theme={theme} />
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
            <p className="cv-eyebrow">{concept.unit_id.toUpperCase()} · 개념 {String(concept.sort_order).padStart(2, "0")}</p>
            <h1 className="cv-title">{concept.title}</h1>
            <p className="cv-subtitle">{concept.subtitle}</p>
          </div>
        </header>
        <main className="cv-main">
          {concept.blocks.map((b) => <BlockShell key={b.id} b={b} qna={byBlock(b.id)} theme={theme} conceptId={conceptId} />)}
          <footer className="cv-footer cv-span2">
            <span>물음표 ? 를 누르면 질문을 보거나 보낼 수 있어요</span><span>{concept.id}</span>
          </footer>
        </main>
      </div>
    </div>
  );
}
