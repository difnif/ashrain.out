// 사진 채점 (OMR) — 시험지 + 답안 카드 인쇄 → 칠한 카드를 사진으로 → 브라우저 인식(마커·호모그래피·버블) → 확인 → 채점
// 라우트: #/solve/omr (홈) · #/solve/omr/new (시험지 만들기) · #/solve/omr/grade[/<code>] (채점)
// 인식은 src/lib/omr/detect.js(순수) 가 하고, 마커를 못 찾거나 신뢰도가 낮으면 /api/ai (task "omr") 로 보조한다.
// 확인 화면을 거치지 않고는 채점하지 않는다 (인식은 틀릴 수 있다 — 학생이 고친 답이 최종).
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../../supabaseClient";
import SolveShell, { useToast } from "./SolveShell";
import ItemPicker from "./ItemPicker";
import MathText from "../../components/MathText";
import ItemFigure from "../../components/ItemFigure";
import ItemQuestion from "../../components/ItemQuestion";
import { fetchLiveItems, fetchItemsByIds, logAttempt, solutionLevels, UNIT_NAMES } from "../../lib/items";
import { CIRCLED, isChoiceCorrect, isCorrect, correctChoiceIndex, displayAnswer, kindOf } from "../../lib/answers";
import { distractorTag } from "../../lib/misconceptions";
import { saveItemWrongNotes } from "../../lib/wrongnotes";
import { askAboutItem } from "../../lib/ask";
import { layoutSheet, packetHtml } from "../../lib/omr/sheet.js";
import { readSheet, mergeAnswers, CONF_OK, CONFIDENCE_OK } from "../../lib/omr/detect.js";
import { newCode, saveSet, listSets, getSet, removeSet, fmtCode } from "../../lib/omr/sets.js";
import "./solve.css";
import "../../components/item.css";

const CSS = `
.om-tiles .ic { font-size: 26px; }
.om-code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 32px; font-weight: 900; letter-spacing: 3px; text-align: center; padding: 14px; border: 2px dashed var(--accent); border-radius: 14px; color: var(--accent); }
.om-code.sm { font-size: 15px; padding: 4px 10px; letter-spacing: 1px; border-width: 1px; border-style: solid; display: inline-block; }
.om-set { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 10px 12px; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
.om-set .cd { font-family: ui-monospace, monospace; font-weight: 800; font-size: 14px; }
.om-set .tx { flex: 1 1 120px; min-width: 0; font-size: 13px; color: var(--muted); line-height: 1.5; }
.om-set .acts { display: flex; gap: 6px; flex: none; }
.om-steps { display: flex; gap: 6px; flex-wrap: wrap; margin: 0 0 12px; }
.om-steps span { font-size: 12px; font-weight: 700; color: var(--muted); padding: 3px 9px; border-radius: 999px; border: 1px solid var(--border); }
.om-steps span.on { color: var(--accent); border-color: var(--accent); }
.om-pv { display: flex; gap: 8px; align-items: flex-start; padding: 8px 10px; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
.om-pv .no { flex: none; min-width: 24px; height: 24px; border-radius: 999px; background: var(--surface2); display: inline-flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800; }
.om-pv .tx { flex: 1; font-size: 13.5px; line-height: 1.5; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.om-pv .kd { flex: none; font-size: 11px; color: var(--muted); border: 1px solid var(--border); border-radius: 999px; padding: 1px 7px; }
.om-drop { border: 2px dashed var(--border); border-radius: 14px; padding: 16px 14px; text-align: center; color: var(--muted); font-size: 13px; line-height: 1.6; }
.om-drop.on { border-color: var(--accent); color: var(--accent); }
.om-photo-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0; }
.om-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; padding: 8px 10px; border: 1px solid var(--border); border-radius: 12px; background: var(--surface); }
.om-row.low { border-color: #F59E0B; background: color-mix(in srgb, #F59E0B 12%, var(--surface)); }
.om-row .no { flex: none; min-width: 26px; height: 26px; border-radius: 999px; background: var(--surface2); display: inline-flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 800; }
.om-row .q { flex: 1 1 110px; min-width: 0; font-size: 12.5px; color: var(--muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.om-row .hint { flex: none; font-size: 11px; font-weight: 800; color: #B45309; }
.om-bubbles { display: flex; gap: 4px; flex: none; margin-left: auto; }
.om-bubbles button { width: 34px; height: 34px; border-radius: 999px; border: 1.5px solid var(--border); background: var(--surface); color: var(--text); font-size: 16px; cursor: pointer; padding: 0; line-height: 1; }
.om-bubbles button.on { background: var(--accent); border-color: var(--accent); color: #fff; }
.om-short { flex: none; width: 150px; margin-left: auto; padding: 8px 10px; font-size: 15px; border-radius: 10px; border: 1px solid var(--border); background: var(--surface); color: var(--text); }
.om-src { font-size: 10.5px; font-weight: 800; padding: 1px 6px; border-radius: 999px; border: 1px solid var(--border); color: var(--muted); flex: none; }
.om-src.ai { color: #7C3AED; border-color: #7C3AED; }
.om-src.me { color: var(--accent); border-color: var(--accent); }
.om-prev { width: 100%; max-width: 300px; display: block; margin: 8px auto 0; border: 1px solid var(--border); border-radius: 10px; background: #fff; }
.om-score { font-size: 36px; font-weight: 900; text-align: center; margin: 4px 0; }
.om-score small { font-size: 16px; color: var(--muted); font-weight: 700; }
.om-res { border: 1px solid var(--border); border-radius: 12px; background: var(--surface); overflow: hidden; }
.om-res > button.hd { display: flex; align-items: center; gap: 8px; width: 100%; padding: 10px 12px; background: none; border: none; color: var(--text); text-align: left; cursor: pointer; font-size: 13.5px; }
.om-res .mark { flex: none; font-weight: 900; width: 20px; text-align: center; }
.om-res .ans { flex: 1; min-width: 0; color: var(--muted); font-size: 12.5px; }
.om-res .ans b { color: var(--text); }
.om-res .body { padding: 4px 12px 12px; border-top: 1px dashed var(--border); }
.om-busy { text-align: center; padding: 30px 12px; color: var(--muted); font-size: 14px; line-height: 1.7; }
.om-busy .sp { display: inline-block; width: 22px; height: 22px; border: 3px solid var(--border); border-top-color: var(--accent); border-radius: 999px; animation: om-spin .8s linear infinite; margin-bottom: 8px; }
@keyframes om-spin { to { transform: rotate(360deg); } }
.om-note { font-size: 12.5px; color: var(--muted); line-height: 1.6; margin: 6px 0 0; }
.om-badge { display: inline-block; font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 999px; background: var(--surface2); color: var(--text); }
`;

// ── 공용 헬퍼 ────────────────────────────────────────────────────────────────
const escHtml = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const dateStr = (iso) => { const d = iso ? new Date(iso) : new Date(); return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")}`; };
const tick = () => new Promise((r) => setTimeout(r, 30));

function parseRoute(hash, sub) {
  const parts = String(hash || "").replace(/^#\/?/, "").split("/").filter(Boolean);   // ["solve","omr","grade","K7Q2-4M"]
  const v = parts[2] || sub || "home";
  const view = v === "new" || v === "grade" ? v : "home";
  let code = null;
  try { code = parts[3] ? decodeURIComponent(parts[3]) : null; } catch { code = parts[3] || null; }
  return { view, code };
}

/** 인쇄 창 — 팝업 차단을 피하려고 클릭 직후(동기) 창을 먼저 열고, 내용은 나중에 채운다 */
function openPrintWindow() {
  try {
    const win = window.open("", "_blank");
    if (!win) return null;
    win.document.open();
    win.document.write(`<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>인쇄 준비</title></head><body style="font-family:sans-serif;color:#555;padding:24px">인쇄할 내용을 준비하는 중이에요…</body></html>`);
    win.document.close();
    return win;
  } catch { return null; }
}
function fillPrintWindow(win, htmlBody, title) {
  const doc = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${escHtml(title)}</title>
<style>html,body{margin:0;padding:0;background:#fff;color:#111}@media screen{body{padding:10mm;background:#eee}.om-card,.om-test{background:#fff}}</style>
</head><body>${htmlBody}<script>window.onload=function(){setTimeout(function(){window.focus();window.print();},350);};</scr` + `ipt></body></html>`;
  win.document.open(); win.document.write(doc); win.document.close();
}
/** 한 번에 열고 채우기 (동기 호출용) */
function printDoc(htmlBody, title) {
  const win = openPrintWindow();
  if (!win) return false;
  fillPrintWindow(win, htmlBody, title);
  return true;
}

function loadImage(file) {
  return new Promise((res, rej) => {
    let url;
    try { url = URL.createObjectURL(file); } catch { rej(new Error("사진을 열 수 없어요")); return; }
    const im = new Image();
    im.onload = () => { URL.revokeObjectURL(url); res(im); };
    im.onerror = () => { URL.revokeObjectURL(url); rej(new Error("사진을 열 수 없어요 (지원하지 않는 형식일 수 있어요)")); };
    im.src = url;
  });
}
/** 사진 파일 → 긴 변 ≤ maxSide 캔버스 + ImageData (브라우저가 EXIF 회전을 반영해 그린다) */
async function fileToCanvas(file, maxSide = 1600) {
  const im = await loadImage(file);
  const w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
  if (!w || !h) throw new Error("사진을 열 수 없어요");
  const sc = Math.min(1, maxSide / Math.max(w, h));
  const cv = document.createElement("canvas");
  cv.width = Math.max(1, Math.round(w * sc)); cv.height = Math.max(1, Math.round(h * sc));
  const ctx = cv.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(im, 0, 0, cv.width, cv.height);
  return { canvas: cv, imageData: ctx.getImageData(0, 0, cv.width, cv.height) };
}

async function aiRead(base64, set) {
  const { data: sess } = await supabase.auth.getSession();
  const token = sess?.session?.access_token;
  if (!token) throw new Error("세션이 만료됐어요 — 다시 로그인해 주세요");
  const r = await fetch("/api/ai", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: JSON.stringify({ task: "omr", image: base64, items: set.items.map((it) => ({ no: it.no, type: it.kind === "choice" ? "choice" : "calc" })) }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j?.error || "AI 요청에 실패했어요");
  return Array.isArray(j.answers) ? j.answers : [];
}

const setItemsOf = (items) => items.map((it, i) => ({
  id: it.id, no: i + 1, kind: kindOf(it) === "choice" ? "choice" : "short",
  answer: it.answer, answer_alt: it.answer_alt, choices: it.choices, question: it.question,
}));
const setTitle = (s) => s.title || `${s.unitId ? (UNIT_NAMES[s.unitId] || "") + " " : ""}${s.conceptTitle || "시험지"}`.trim();
const setSubtitle = (s) => `${s.items.length}문항 · ${dateStr(s.createdAt)} · 코드 ${s.code}`;

// ── 페이지 ───────────────────────────────────────────────────────────────────
export default function Omr({ sub, hash }) {
  const route = parseRoute(hash, sub);
  const [toast, say] = useToast();
  const [uid, setUid] = useState(null);
  useEffect(() => { supabase.auth.getUser().then(({ data }) => setUid(data?.user?.id || null)).catch(() => setUid(null)); }, []);
  useEffect(() => {                                 // 빗나간 드롭이 페이지를 덮지 않게
    const stop = (e) => e.preventDefault();
    window.addEventListener("dragover", stop); window.addEventListener("drop", stop);
    return () => { window.removeEventListener("dragover", stop); window.removeEventListener("drop", stop); };
  }, []);

  const SUB = {
    home: "시험지와 답안 카드를 인쇄해 종이로 풀고, 칠한 카드를 사진으로 찍으면 채점해 드려요.",
    new: "개념을 고르면 객관식 위주로 문항을 뽑아 시험지와 답안 카드를 만들어요.",
    grade: null,
  };
  return (
    <SolveShell title="사진 채점" sub={SUB[route.view]} back={route.view === "home" ? "#/solve" : "#/solve/omr"} toast={toast}>
      <style>{CSS}</style>
      {route.view === "new" && <MakeView say={say} />}
      {route.view === "grade" && <GradeView key={route.code || "_"} uid={uid} code={route.code} say={say} />}
      {route.view === "home" && <HomeView say={say} />}
    </SolveShell>
  );
}

// ── 홈 ───────────────────────────────────────────────────────────────────────
function HomeView({ say }) {
  const [sets, setSets] = useState(() => listSets());
  const [busy, setBusy] = useState(null);
  const reprint = async (s) => {
    const win = openPrintWindow();
    if (!win) { say("팝업이 차단됐어요 — 브라우저에서 팝업을 허용해 주세요"); return; }
    setBusy(s.code);
    try {
      const items = await fetchItemsByIds(s.items.map((i) => i.id));
      const by = Object.fromEntries(items.map((i) => [i.id, i]));
      const aligned = s.items.map((it) => by[it.id] || { question: "(이 문항은 지금 볼 수 없어요)", choices: it.choices, qtype: it.kind });
      const missing = aligned.filter((x) => !x.id).length;
      const spec = layoutSheet({ code: s.code, items: s.items });
      fillPrintWindow(win, packetHtml({ title: setTitle(s), subtitle: setSubtitle(s), items: aligned, spec }), setTitle(s));
      if (missing) say(`${missing}문항은 지금 불러올 수 없어서 빈 자리로 인쇄했어요`);
    } catch (e) {
      try { win.close(); } catch { /* ignore */ }
      say("문항을 불러오지 못했어요: " + (e?.message || e));
    } finally { setBusy(null); }
  };
  const remove = (s) => { removeSet(s.code); setSets(listSets()); say("목록에서 지웠어요"); };
  return (
    <div>
      <div className="sv-grid2 om-tiles">
        <button className="sv-tile" onClick={() => (location.hash = "#/solve/omr/new")}>
          <span className="ic">🖨️</span><span className="tt">시험지 만들기</span>
          <span className="ds">개념을 골라 10·20문항 시험지와 답안 카드를 인쇄해요.</span>
        </button>
        <button className="sv-tile" onClick={() => (location.hash = "#/solve/omr/grade")}>
          <span className="ic">📷</span><span className="tt">답안 카드 채점하기</span>
          <span className="ds">칠한 카드를 사진으로 찍으면 자동으로 읽고 채점해요.</span>
        </button>
      </div>
      <div className="sv-sec">최근 만든 시험지</div>
      {!sets.length && <div className="sv-empty">아직 만든 시험지가 없어요.<br />시험지를 만들면 여기에 코드가 남아요.</div>}
      <div className="sv-list">
        {sets.map((s) => (
          <div key={s.code} className="om-set">
            <span className="cd">{s.code}</span>
            <span className="tx">{setTitle(s)} · {s.items.length}문항 · {dateStr(s.createdAt)}</span>
            <span className="acts">
              <button className="sv-btn sm" disabled={busy === s.code} onClick={() => reprint(s)}>{busy === s.code ? "준비 중…" : "시험지 다시 인쇄"}</button>
              <button className="sv-btn sm pri" onClick={() => (location.hash = `#/solve/omr/grade/${encodeURIComponent(s.code)}`)}>채점</button>
              <button className="sv-btn sm ghost" title="목록에서 지우기" onClick={() => remove(s)}>✕</button>
            </span>
          </div>
        ))}
      </div>
      <p className="om-note">코드는 이 기기에만 저장돼요. 다른 기기에서 만든 카드는 그 기기에서 채점해 주세요.</p>
    </div>
  );
}

// ── 시험지 만들기 ─────────────────────────────────────────────────────────────
function MakeView({ say }) {
  const [concept, setConcept] = useState(null);
  const [live, setLive] = useState(0);
  const [n, setN] = useState(10);
  const [items, setItems] = useState(null);
  const [busy, setBusy] = useState(false);
  const [code, setCode] = useState(null);
  const [saved, setSaved] = useState(null);

  const pick = (c, cnt) => { setConcept(c); setLive(cnt || 0); setItems(null); setCode(null); setSaved(null); setN(cnt >= 20 ? 20 : 10); };

  const draw = async () => {
    if (!concept) return;
    setBusy(true); setSaved(null); setCode(null);
    try {
      let list = await fetchLiveItems({ conceptId: concept.id, qtypes: ["choice"], n, pool: Math.max(80, n * 4) });
      if (list.length < n) {
        const have = new Set(list.map((i) => i.id));
        const more = await fetchLiveItems({ conceptId: concept.id, qtypes: ["short"], n: n - list.length });
        list = list.concat(more.filter((i) => !have.has(i.id)));
      }
      list = list.slice(0, n);
      if (!list.length) say("이 개념에는 아직 공개된 문항이 없어요");
      else if (list.length < n) say(`공개 문항이 ${list.length}개뿐이어서 그만큼만 뽑았어요`);
      setItems(list);
    } catch (e) { say("문항을 불러오지 못했어요: " + (e?.message || e)); setItems([]); }
    finally { setBusy(false); }
  };

  const print = () => {
    if (!items?.length) return;
    const c = code || newCode();
    const its = setItemsOf(items);
    const spec = layoutSheet({ code: c, items: its });
    const title = `${UNIT_NAMES[concept.unit_id] || ""} ${concept.title}`.trim();
    const created = saved?.createdAt || new Date().toISOString();
    const subtitle = `${items.length}문항 · ${dateStr(created)} · 코드 ${c}`;
    if (!printDoc(packetHtml({ title, subtitle, items, spec }), title)) { say("팝업이 차단됐어요 — 브라우저에서 팝업을 허용해 주세요"); return; }
    setCode(c);
    const row = saveSet({ code: c, conceptId: concept.id, conceptTitle: concept.title, unitId: concept.unit_id, title, items: its, createdAt: created });
    setSaved(row);
    say("시험지와 답안 카드를 인쇄 창으로 보냈어요");
  };

  const step = !concept ? 1 : !items ? 2 : !saved ? 3 : 4;
  return (
    <div>
      <div className="om-steps">
        {["개념 고르기", "문항 수", "미리 보기 · 인쇄", "코드 확인"].map((t, i) => <span key={t} className={step === i + 1 ? "on" : ""}>{i + 1}. {t}</span>)}
      </div>
      {!concept && (
        <ItemPicker mode="concept" filter={{ qtypes: ["choice", "short"] }} onPickConcept={pick} hint="객관식이 많은 개념일수록 카드 인식이 편해요. 단답은 카드의 답칸에 손으로 쓰고, 채점 때 직접 입력해요." />
      )}
      {concept && (
        <>
          <div className="sv-row wrap" style={{ marginBottom: 10 }}>
            <button className="sv-btn sm" onClick={() => setConcept(null)}>← 개념 다시 고르기</button>
            <span className="sv-muted">{UNIT_NAMES[concept.unit_id]} · {concept.title} · 공개 {live}문항</span>
          </div>
          {!saved && (
            <div className="sv-card">
              <div className="sv-sec" style={{ marginTop: 0 }}>문항 수</div>
              <div className="sv-row wrap" style={{ gap: 6 }}>
                {[10, 20].map((k) => (
                  <button key={k} className={"sv-chip" + (n === k ? " on" : "")} disabled={live > 0 && live < k && k !== 10} onClick={() => setN(k)}>{k}문항</button>
                ))}
                {live > 0 && live < 10 && <button className={"sv-chip" + (n === live ? " on" : "")} onClick={() => setN(live)}>전부 ({live})</button>}
              </div>
              <p className="om-note">객관식을 먼저 뽑고, 모자라면 단답으로 채워요. 16문항부터는 카드가 두 줄(1~15 · 16~30)이 돼요.</p>
              <button className="sv-btn pri full" style={{ marginTop: 8 }} disabled={busy} onClick={draw}>{busy ? "문항을 뽑는 중…" : items ? "🎲 다시 뽑기" : "문항 뽑기"}</button>
            </div>
          )}
          {items && items.length > 0 && !saved && (
            <>
              <div className="sv-sec">미리 보기 · {items.length}문항 (객관식 {items.filter((i) => kindOf(i) === "choice").length})</div>
              <div className="sv-list">
                {items.map((it, i) => (
                  <div key={it.id} className="om-pv">
                    <span className="no">{i + 1}</span>
                    <MathText as="span" className="tx" text={it.question} />
                    <span className="kd">{kindOf(it) === "choice" ? "객관식" : "단답"}{it.figure ? " · 도형" : ""}</span>
                  </div>
                ))}
              </div>
              <button className="sv-btn pri full" style={{ marginTop: 12 }} onClick={print}>🖨 인쇄하기 — 시험지 + 답안 카드</button>
              <p className="om-note">인쇄 창이 열려요 (A4 세로). 답안 카드는 마지막 쪽이에요 — 카드는 접거나 구기지 말고, 네 모서리의 검은 네모가 모두 나오게 찍어요.</p>
            </>
          )}
          {items && !items.length && <div className="sv-empty">뽑을 문항이 없어요. 다른 개념을 골라 주세요.</div>}
          {saved && (
            <div className="sv-card">
              <div className="sv-sec" style={{ marginTop: 0 }}>세트 코드</div>
              <div className="om-code">{saved.code}</div>
              <p className="om-note">카드 맨 위에도 같은 코드가 찍혀 있어요. 채점할 때 이 코드로 시험지를 찾아요 (이 기기에 저장됨).</p>
              <div className="sv-row wrap" style={{ marginTop: 10 }}>
                <button className="sv-btn pri" onClick={() => (location.hash = `#/solve/omr/grade/${encodeURIComponent(saved.code)}`)}>📷 채점하러 가기</button>
                <button className="sv-btn" onClick={print}>다시 인쇄</button>
                <button className="sv-btn ghost" onClick={() => (location.hash = "#/solve/omr")}>홈</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

// ── 채점 ─────────────────────────────────────────────────────────────────────
function GradeView({ uid, code, say }) {
  const [set] = useState(() => (code ? getSet(code) : null));          // 코드가 바뀌면 부모가 key 로 다시 마운트한다
  const [step, setStep] = useState(() => (code && getSet(code) ? "photo" : "set"));
  const [codeIn, setCodeIn] = useState("");
  const [read, setRead] = useState(null);       // readSheet 결과
  const [ai, setAi] = useState(null);           // AI answers
  const [aiBusy, setAiBusy] = useState(false);
  const [aiErr, setAiErr] = useState(null);
  const [rows, setRows] = useState(null);       // 확인 행
  const [photo, setPhoto] = useState(null);     // { canvas, base64 }
  const [drag, setDrag] = useState(false);
  const [result, setResult] = useState(null);
  const camRef = useRef(null), fileRef = useRef(null);
  const spec = useMemo(() => (set ? layoutSheet({ code: set.code, items: set.items }) : null), [set]);

  useEffect(() => { if (code && !set) say("이 기기에서 만든 시험지 중에 그 코드가 없어요"); }, []); // eslint-disable-line

  const goSet = (s) => { location.hash = `#/solve/omr/grade/${encodeURIComponent(s.code)}`; };
  const lookup = () => {
    const s = getSet(codeIn);
    if (!s) { say("이 기기에서 만든 시험지 중에 그 코드가 없어요"); return; }
    goSet(s);
  };
  const resetPhoto = () => { setRead(null); setAi(null); setAiErr(null); setRows(null); setPhoto(null); setResult(null); setStep("photo"); };

  async function onFile(f) {
    if (!f || !set) return;
    const isImg = (f.type || "").startsWith("image/") || /\.(jpe?g|png|webp|heic|heif)$/i.test(f.name || "");
    if (!isImg) { say("사진 파일만 올릴 수 있어요"); return; }
    setStep("busy"); setAiErr(null); setAi(null);
    try {
      const { canvas, imageData } = await fileToCanvas(f, 1600);
      await tick();
      const res = readSheet(imageData, spec);
      let base64 = null;
      try { base64 = canvas.toDataURL("image/jpeg", 0.85).split(",")[1]; } catch { base64 = null; }
      setPhoto({ canvas, base64 });
      setRead(res);
      setRows(mergeAnswers(set.items, res, null, null));
      setStep("confirm");
      if (res.ok && res.nMarked === 0) say("표시를 하나도 찾지 못했어요 — 이 시험지의 카드가 맞는지 확인해 주세요");
      if (!res.ok || res.confidence < CONFIDENCE_OK) runAi(base64, res, "auto");
    } catch (e) {
      say(e?.message || "사진을 처리하지 못했어요");
      setStep("photo");
    }
  }

  async function runAi(base64 = photo?.base64, res = read, mode = "manual") {
    if (!base64) { setAiErr("사진 데이터를 준비하지 못했어요"); return; }
    setAiBusy(true); setAiErr(null);
    try {
      const answers = await aiRead(base64, set);
      setAi(answers);
      setRows((prev) => mergeAnswers(set.items, res, answers, prev));
      say(mode === "auto" ? "카드 인식이 불확실해서 AI로 보조했어요 — 꼭 확인한 뒤 채점하세요" : "AI가 읽은 답을 채웠어요 — 꼭 확인한 뒤 채점하세요");
    } catch (e) {
      setAiErr(e?.message || String(e));
    } finally { setAiBusy(false); }
  }

  const setAnswer = (no, answer) => setRows((prev) => prev.map((r) => (r.no === no ? { ...r, answer, conf: 1, src: "me", edited: true, flag: null } : r)));

  async function grade() {
    if (!set || !rows) return;
    setStep("grading");
    let items;
    try { items = await fetchItemsByIds(set.items.map((it) => it.id)); }
    catch (e) { say("문항을 불러오지 못했어요: " + (e?.message || e)); setStep("confirm"); return; }
    const by = Object.fromEntries(items.map((i) => [i.id, i]));
    const results = []; let missing = 0;
    for (const it of set.items) {
      const item = by[it.id];
      if (!item) { missing++; continue; }
      const ans = String(rows.find((r) => r.no === it.no)?.answer ?? "").trim();
      let correct = false, idx = null, chosen = null;
      if (it.kind === "choice") {
        const k = CIRCLED.indexOf(ans);
        if (k >= 0) { idx = k; chosen = item.choices?.[k] ?? ans; correct = isChoiceCorrect(item, k); }
      } else correct = !!ans && isCorrect(item, ans);
      results.push({ no: it.no, item, kind: it.kind, ans, correct, idx, chosen });
    }
    if (uid && results.length) {
      await Promise.all(results.map((r) => logAttempt({
        uid, item: r.item, rawAnswer: r.ans || null, correct: r.correct, chosenIndex: r.idx, chosenChoice: r.chosen,
        setId: `omr:${set.code}`, seq: r.no,
      })));
    }
    setResult({ results, missing, path: !read?.ok ? (ai ? "ai" : "none") : ai ? "cv+ai" : "cv" });
    setStep("result");
  }

  // ── 세트 고르기 ──
  if (step === "set" || !set) {
    const sets = listSets();
    return (
      <div>
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>카드에 적힌 코드로 찾기</div>
          <div className="sv-row">
            <input className="sv-in" placeholder="예: K7Q2-4M" value={codeIn} onChange={(e) => setCodeIn(fmtCode(e.target.value))} onKeyDown={(e) => e.key === "Enter" && lookup()} autoCapitalize="characters" autoCorrect="off" spellCheck={false} />
            <button className="sv-btn pri" onClick={lookup}>찾기</button>
          </div>
        </div>
        <div className="sv-sec">최근 만든 시험지</div>
        {!sets.length && <div className="sv-empty">이 기기에서 만든 시험지가 없어요.<br /><button className="sv-btn sm" style={{ marginTop: 8 }} onClick={() => (location.hash = "#/solve/omr/new")}>시험지 만들기</button></div>}
        <div className="sv-list">
          {sets.map((s) => (
            <button key={s.code} className="sv-item" onClick={() => goSet(s)}>
              <span className="no">📄</span>
              <span className="tx"><b>{s.code}</b> · {setTitle(s)}</span>
              <span className="rt">{s.items.length}문항 · {dateStr(s.createdAt)}</span>
            </button>
          ))}
        </div>
      </div>
    );
  }

  const header = (
    <div className="sv-row wrap" style={{ marginBottom: 10 }}>
      <span className="om-code sm">{set.code}</span>
      <span className="sv-muted">{setTitle(set)} · {set.items.length}문항</span>
      <span className="sv-sp" />
      <button className="sv-btn sm" onClick={() => (location.hash = "#/solve/omr/grade")}>다른 시험지</button>
    </div>
  );

  // ── 사진 ──
  if (step === "photo") {
    return (
      <div>
        {header}
        <input ref={camRef} type="file" accept="image/*" capture="environment" hidden onChange={(e) => { onFile(e.target.files?.[0]); e.target.value = ""; }} />
        <input ref={fileRef} type="file" accept="image/*" hidden onChange={(e) => { onFile(e.target.files?.[0]); e.target.value = ""; }} />
        <div className={"om-drop" + (drag ? " on" : "")}
          onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
          onDragLeave={() => setDrag(false)}
          onDrop={(e) => { e.preventDefault(); setDrag(false); onFile(e.dataTransfer?.files?.[0]); }}>
          <div style={{ fontSize: 30 }}>📷</div>
          칠한 답안 카드를 찍어 주세요.<br />
          <b>네 모서리의 검은 네모</b>가 모두 나오게, 그림자 없이 밝은 곳에서 위에서 똑바로.<br />
          <span className="sv-small">사진 파일을 여기로 끌어와도 돼요</span>
          <div className="om-photo-btns">
            <button className="sv-btn pri" onClick={() => camRef.current?.click()}>📷 카메라로 찍기</button>
            <button className="sv-btn" onClick={() => fileRef.current?.click()}>🖼 사진 고르기</button>
          </div>
        </div>
        <p className="om-note">객관식은 자동으로 읽고, 단답은 다음 화면에서 직접 입력해요. 읽은 결과는 채점 전에 꼭 확인해요.</p>
      </div>
    );
  }

  if (step === "busy") {
    return <div>{header}<div className="om-busy"><div className="sp" /><br />사진을 분석하는 중이에요…<br /><span className="sv-small">마커를 찾고 카드를 펴서 버블을 읽어요</span></div></div>;
  }

  // ── 확인 ──
  if (step === "confirm" && rows) {
    return (
      <div>
        {header}
        <ConfirmView spec={spec} rows={rows} read={read} ai={ai} aiBusy={aiBusy} aiErr={aiErr} canAi={!!photo?.base64}
          onChange={setAnswer} onAi={() => runAi()} onRetry={resetPhoto} onGrade={grade} />
      </div>
    );
  }

  if (step === "grading") {
    return <div>{header}<div className="om-busy"><div className="sp" /><br />채점하는 중이에요…</div></div>;
  }

  if (step === "result" && result) {
    return <div>{header}<ResultView set={set} result={result} uid={uid} say={say} onRetry={resetPhoto} /></div>;
  }
  return null;
}

// ── 확인 화면 ─────────────────────────────────────────────────────────────────
// rows: mergeAnswers 결과 · read: readSheet 결과 · ai: AI answers|null
export function ConfirmView({ spec, rows, read, ai, aiBusy, aiErr, canAi, onChange, onAi, onRetry, onGrade }) {
  const [showPrev, setShowPrev] = useState(false);
  const prevRef = useRef(null);
  const nLow = rows.filter((r) => r.kind === "choice" && !r.edited && (r.conf < CONF_OK || r.flag === "double")).length;
  const nShort = rows.filter((r) => r.kind === "short").length;
  const nEmpty = rows.filter((r) => !String(r.answer || "").trim()).length;
  const pathLabel = !read?.ok ? (ai ? "AI 인식" : aiBusy ? "AI 인식 중" : "인식 실패") : ai ? "카드 인식 + AI 보조" : "카드 인식";

  // 워프된 카드 미리보기 + 인식 표시 (초록 = 확신, 노랑 = 불확실, 빨강 = 두 개 표시)
  useEffect(() => {
    const cv = prevRef.current;
    if (!cv || !showPrev || !read?.ok || !read.warped || !spec) return;
    const { width, height, gray, scale } = read.warped;
    cv.width = width; cv.height = height;
    const ctx = cv.getContext("2d");
    const id = ctx.createImageData(width, height);
    for (let i = 0; i < gray.length; i++) { const v = gray[i]; id.data[i * 4] = v; id.data[i * 4 + 1] = v; id.data[i * 4 + 2] = v; id.data[i * 4 + 3] = 255; }
    ctx.putImageData(id, 0, 0);
    ctx.lineWidth = 2.5;
    for (const row of spec.rows) {
      const r = rows.find((x) => x.no === row.no);
      if (!row.bubbles || !r) continue;
      for (const b of row.bubbles) {
        if (r.answer !== b.label) continue;
        ctx.strokeStyle = r.edited || r.conf >= CONF_OK ? "#16A34A" : "#F59E0B";
        ctx.beginPath(); ctx.arc(b.x * scale, b.y * scale, b.r * scale + 3, 0, Math.PI * 2); ctx.stroke();
      }
      if (r.flag === "double" && !r.answer) {
        const b0 = row.bubbles[0], b4 = row.bubbles[4];
        ctx.strokeStyle = "#DC2626";
        ctx.strokeRect((b0.x - b0.r - 4) * scale, (row.y - b0.r - 4) * scale, (b4.x - b0.x + 2 * b0.r + 8) * scale, (2 * b0.r + 8) * scale);
      }
    }
  }, [showPrev, read, rows, spec]);

  return (
    <div>
      <div className="sv-card flat">
        <div className="sv-row wrap">
          <span className="om-badge">{pathLabel}</span>
          {read?.ok && <span className="sv-small">신뢰도 {Math.round(read.confidence * 100)}% · 표시 {read.nMarked}개</span>}
          {!read?.ok && <span className="sv-small">{read?.reason === "markers" ? "네 모서리 마커를 찾지 못했어요" : read?.reason === "orient" ? "카드 방향을 확인하지 못했어요" : "카드를 읽지 못했어요"}</span>}
          <span className="sv-sp" />
          {read?.ok && <button className="sv-btn sm" onClick={() => setShowPrev((v) => !v)}>{showPrev ? "인식 화면 닫기" : "인식 화면 보기"}</button>}
        </div>
        {showPrev && read?.ok && <canvas ref={prevRef} className="om-prev" />}
        {aiBusy && <p className="om-note">⏳ AI가 카드를 읽는 중이에요…</p>}
        {aiErr && <p className="om-note" style={{ color: "var(--bad)" }}>AI 보조 실패: {aiErr}</p>}
        <p className="om-note">
          {nLow > 0 && <>노란 행 {nLow}개는 확실하지 않아요 — 카드와 비교해서 고쳐 주세요. </>}
          {nShort > 0 && <>단답 {nShort}문항은 카드에 쓴 답을 직접 입력해요. </>}
          빈 답은 무응답(오답)으로 채점돼요.
        </p>
        {!aiBusy && (
          <button className="sv-btn sm" onClick={onAi} disabled={!canAi}>{ai ? "🤖 AI로 다시 읽기" : "🤖 AI로 읽기 (단답 포함)"}</button>
        )}
      </div>
      <div className="sv-list">
        {rows.map((r) => {
          const low = r.kind === "choice" && !r.edited && (r.conf < CONF_OK || r.flag === "double");
          return (
            <div key={r.no} className={"om-row" + (low ? " low" : "")}>
              <span className="no">{r.no}</span>
              <span className="q" title={r.q}>{r.q || (r.kind === "choice" ? "객관식" : "단답")}</span>
              {r.src !== "none" && <span className={"om-src " + r.src}>{r.src === "cv" ? "카드" : r.src === "ai" ? "AI" : "내가 고침"}</span>}
              {low && <span className="hint">{r.flag === "double" ? "두 개 표시" : r.flag === "blank" ? "표시 없음" : r.flag === "uneven" ? "그림자?" : "불확실"}</span>}
              {r.kind === "choice" ? (
                <span className="om-bubbles">
                  {CIRCLED.map((c) => (
                    <button key={c} type="button" className={r.answer === c ? "on" : ""} onClick={() => onChange(r.no, r.answer === c ? "" : c)}>{c}</button>
                  ))}
                </span>
              ) : (
                <input className="om-short" placeholder="답 입력" value={r.answer} onChange={(e) => onChange(r.no, e.target.value)} />
              )}
            </div>
          );
        })}
      </div>
      <div className="sv-row wrap" style={{ marginTop: 14 }}>
        <button className="sv-btn" onClick={onRetry}>📷 다른 사진으로</button>
        <span className="sv-sp" />
        <button className="sv-btn pri" onClick={onGrade} disabled={aiBusy}>✅ 채점하기 ({rows.length - nEmpty}/{rows.length} 답함)</button>
      </div>
    </div>
  );
}

// ── 결과 ─────────────────────────────────────────────────────────────────────
export function ResultView({ set, result, uid, say, onRetry }) {
  const [open, setOpen] = useState({});
  const [saved, setSaved] = useState(false);
  const { results, missing, path } = result;
  const PATH = { cv: "카드 인식", "cv+ai": "카드 인식 + AI 보조", ai: "AI 인식", none: "직접 입력" };
  const nOk = results.filter((r) => r.correct).length;
  const wrong = results.filter((r) => !r.correct);
  const pct = results.length ? Math.round((nOk / results.length) * 100) : 0;

  const saveWrong = async () => {
    if (!uid) { say("로그인 정보를 확인하지 못했어요"); return; }
    const entries = wrong.map((r) => ({ item: r.item, myAnswer: r.ans, tag: r.kind === "choice" ? distractorTag(r.item, r.chosen) : null }));
    const { added, skipped, error } = await saveItemWrongNotes({ uid, entries, source: "OMR" });
    if (error) { say("오답노트 저장 실패: " + (error.message || error)); return; }
    setSaved(true);
    say(added ? `📕 ${added}문제를 오답노트에 담았어요${skipped ? ` (${skipped}개는 이미 있어요)` : ""}` : "이미 오답노트에 있는 문제예요");
  };

  const correctText = (r) => {
    if (r.kind === "choice") {
      const ci = correctChoiceIndex(r.item);
      return ci >= 0 ? `${CIRCLED[ci]} ${displayAnswer(r.item.choices?.[ci] ?? "")}` : displayAnswer(r.item.answer);
    }
    return displayAnswer(r.item.answer);
  };

  return (
    <div>
      <div className="sv-card">
        <div className="om-score">{nOk} <small>/ {results.length}</small></div>
        <div className="sv-bar" style={{ margin: "6px 0 8px" }}><i style={{ width: pct + "%" }} /></div>
        <div className="sv-muted" style={{ textAlign: "center" }}>
          {setTitle(set)} · {pct}점{wrong.length === 0 ? " · 완벽해요! 🎉" : ""}
          {path && PATH[path] ? <> · <span className="om-badge">{PATH[path]}</span></> : null}
          {missing ? <><br />{missing}문항은 지금 볼 수 없어서 채점에서 뺐어요.</> : null}
        </div>
        <div className="sv-row wrap" style={{ marginTop: 12 }}>
          {wrong.length > 0 && uid && <button className="sv-btn pri" disabled={saved} onClick={saveWrong}>{saved ? "📕 오답노트에 저장됨" : `📕 틀린 ${wrong.length}문제 오답노트에 저장`}</button>}
          <button className="sv-btn" onClick={onRetry}>📷 다시 채점</button>
          <button className="sv-btn ghost" onClick={() => (location.hash = "#/solve/omr")}>홈</button>
        </div>
      </div>
      <div className="sv-sec">문항별 결과 — 눌러서 문제·해설 보기</div>
      <div className="sv-list">
        {results.map((r) => {
          const on = !!open[r.no];
          return (
            <div key={r.no} className="om-res">
              <button className="hd" onClick={() => setOpen((o) => ({ ...o, [r.no]: !o[r.no] }))}>
                <span className="no" style={{ minWidth: 24, height: 24, borderRadius: 999, background: "var(--surface2)", display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 800, flex: "none" }}>{r.no}</span>
                <span className={"mark " + (r.correct ? "sv-ok" : "sv-bad")}>{r.correct ? "✓" : "✗"}</span>
                <span className="ans">
                  내 답 <b>{r.ans ? (r.kind === "choice" ? r.ans : displayAnswer(r.ans)) : "(무응답)"}</b>
                  {!r.correct && <> · 정답 <b className="sv-ok">{correctText(r)}</b></>}
                </span>
                <span className="sv-small">{on ? "▲" : "▼"}</span>
              </button>
              {on && (
                <div className="body">
                  <ItemQuestion item={r.item} compact reveal selected={r.idx} figWidth={300} />
                  {r.kind !== "choice" && <div className="isol"><div className="answer">정답: {displayAnswer(r.item.answer)}</div></div>}
                  <Solution item={r.item} />
                  <div className="sv-row wrap" style={{ marginTop: 8 }}>
                    <button className="sv-btn sm" onClick={() => askAboutItem(r.item)}>💬 이 문제 질문하기</button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export function Solution({ item }) {
  const levels = solutionLevels(item);
  const ma = item?.solution?.model_answer;
  if (!levels.length && !ma) return <div className="sv-muted" style={{ marginTop: 8 }}>해설이 아직 없어요.</div>;
  return (
    <div className="isol">
      {levels.map((lv, i) => (
        <div className="lv" key={i}>
          <div className="lv-title">{lv.title || `${lv.level ?? i + 1}단계`}</div>
          {Array.isArray(lv.figure) && lv.figure.length > 0 && <ItemFigure figure={lv.figure} width={300} />}
          {Array.isArray(lv.steps) && lv.steps.length > 0
            ? <ol>{lv.steps.map((s, k) => <li key={k}><MathText text={s} /></li>)}</ol>
            : lv.text ? <MathText as="p" text={lv.text} /> : null}
        </div>
      ))}
      {ma && <div className="ma"><b>모범 답안</b><MathText as="div" text={ma} /></div>}
    </div>
  );
}
