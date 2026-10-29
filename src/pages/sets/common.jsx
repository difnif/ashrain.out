// ashrain.out — 컨셉 문제 화면 공용: 계정 · 세트 불러오기 · 답 입력 · 자료(문제지 · 해설지 · OMR) 인쇄/다운로드 · 해설 애니메이션
import { useEffect, useRef, useState } from "react";
import { supabase } from "../../supabaseClient";
import {
  loadIndex, loadSet, loadFiles, fileInfo, fmtBytes, DOCS, pdfUrl, pdfRawUrl, printUrl, downloadName,
  readProgress, setProgressUser,
} from "../../lib/conceptsets";
import { layoutCard, cardHtml } from "../../lib/omr/grid.js";
import { zipStore } from "../../lib/zipstore";
import { mountAll } from "../../lib/figanim";
import { composePrint, openPrintWindow, fillPrintWindow, failPrintWindow } from "./printdoc";

// ── 계정별 진도 ───────────────────────────────────────────────────────────────
let uidCache;   // undefined 미확인 | "" 없음 | id
export function useCsUser() {
  const [uid, setUid] = useState(() => { if (uidCache !== undefined) setProgressUser(uidCache); return uidCache; });
  useEffect(() => {
    let alive = true;
    supabase.auth.getSession().then(({ data }) => {
      const id = data?.session?.user?.id || "";
      uidCache = id; setProgressUser(id);
      if (alive) setUid(id);
    }).catch(() => { uidCache = ""; if (alive) setUid(""); });
    return () => { alive = false; };
  }, []);
  return uid;   // undefined 인 동안은 진도를 읽지 않는다
}

/** 세트 + 범주 목록 + 파일 목록 */
export function useSetData(cat, no) {
  const [st, setSt] = useState({ set: null, cat: null, files: null, err: null });
  useEffect(() => {
    let alive = true;
    setSt({ set: null, cat: null, files: null, err: null });
    Promise.all([loadSet(cat, no), loadIndex(cat), loadFiles(cat)])
      .then(([set, c, files]) => { if (alive) setSt({ set, cat: c, files, err: null }); })
      .catch((e) => { if (alive) setSt({ set: null, cat: null, files: null, err: e?.message || String(e) }); });
    return () => { alive = false; };
  }, [cat, no]);
  return st;
}

export function useProgress(cat, no, uid) {
  const [p, setP] = useState(() => (uid === undefined ? { items: {}, omr: [] } : readProgress(cat, no)));
  useEffect(() => { if (uid !== undefined) setP(readProgress(cat, no)); }, [cat, no, uid]);
  const refresh = () => setP(readProgress(cat, no));
  return [p, refresh];
}

// ── 토스트 ────────────────────────────────────────────────────────────────────
export function useSay() {
  const [msg, setMsg] = useState(null);
  useEffect(() => { if (!msg) return; const t = setTimeout(() => setMsg(null), 2800); return () => clearTimeout(t); }, [msg]);
  return [msg, setMsg];
}
export function Toast({ msg }) { return msg ? <div className="sv-toast cs-toast" role="status">{msg}</div> : null; }

// ── 글꼴: 도식 · 판서는 문제지와 같은 명조(Noto Serif KR) ──────────────────────
let serifDone = false;
export function ensureSerif() {
  if (serifDone || typeof document === "undefined") return;
  serifDone = true;
  const l = document.createElement("link");
  l.rel = "stylesheet";
  l.href = "https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;700&display=swap";
  document.head.appendChild(l);
}

// ── 해설 애니메이션 붙이기 (언마운트 때 멈춤) ──────────────────────────────────
export function useAnim(ref, deps) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const players = mountAll(el, { autoplay: false });
    let io = null;
    if (typeof IntersectionObserver !== "undefined" && players.length) {
      io = new IntersectionObserver((ents) => ents.forEach((e) => {
        const pl = e.target.__anim;
        if (!pl) return;
        if (e.isIntersecting && pl.i < 0) pl.play();
        if (!e.isIntersecting && pl.playing) pl.pause();
      }), { threshold: 0.45 });
      players.forEach((pl) => io.observe(pl.root));
    }
    return () => { if (io) io.disconnect(); players.forEach((pl) => { try { pl.playing = false; pl.stop(); } catch { /* 무시 */ } }); };
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps
}

// ── 답 입력 ───────────────────────────────────────────────────────────────────
const onlyNum = (v) => String(v || "").replace(/[^\d]/g, "").slice(0, 7);

/** raw(쓰는 꼴) ↔ 칸. kind: int · frac · pick · pair */
export function AnswerInput({ item, value, onChange, onSubmit, disabled, state }) {
  const a = item?.a || {};
  const k = a.k;
  const first = useRef(null);
  useEffect(() => { if (!disabled) setTimeout(() => first.current?.focus?.({ preventScroll: true }), 30); }, [item?.id]); // eslint-disable-line
  const key = (e) => { if (e.key === "Enter") { e.preventDefault(); onSubmit?.(); } };
  const cls = "cs-ain" + (state ? " " + state : "");
  if (k === "frac") {
    const [n = "", d = ""] = String(value || "").split("/");
    const set = (nn, dd) => onChange(dd ? `${nn}/${dd}` : nn);
    return (
      <div className={"cs-fin " + cls} role="group" aria-label="분수로 답하기">
        <input ref={first} className="cs-fi" inputMode="numeric" pattern="[0-9]*" aria-label="분자" placeholder="분자"
          value={n} disabled={disabled} onChange={(e) => set(onlyNum(e.target.value), d)} onKeyDown={key} />
        <i className="cs-fbar" aria-hidden="true" />
        <input className="cs-fi" inputMode="numeric" pattern="[0-9]*" aria-label="분모" placeholder="분모"
          value={d} disabled={disabled} onChange={(e) => set(n, onlyNum(e.target.value))} onKeyDown={key} />
      </div>
    );
  }
  if (k === "pick") {
    const on = new Set(String(value || "").match(/[ㄱ-ㅎ]/gu) || []);
    const opts = a.o || ["ㄱ", "ㄴ", "ㄷ", "ㄹ"];
    const tog = (o) => { const s = new Set(on); if (s.has(o)) s.delete(o); else s.add(o); onChange(opts.filter((x) => s.has(x)).join(", ")); };
    return (
      <div className={"cs-pin " + cls} role="group" aria-label="옳은 것을 모두 고르기">
        {opts.map((o, i) => (
          <button key={o} ref={i === 0 ? first : undefined} type="button" className={"cs-pick" + (on.has(o) ? " on" : "")}
            aria-pressed={on.has(o)} disabled={disabled} onClick={() => tog(o)}>{o}</button>
        ))}
        <span className="cs-pin-h">맞는 것을 모두 눌러요</span>
      </div>
    );
  }
  if (k === "pair") {
    const [x = "", y = ""] = String(value || "").split(/,\s*/);
    const labels = a.l || ["첫째", "둘째"];
    const set = (xx, yy) => onChange(xx || yy ? `${xx}, ${yy}` : "");
    return (
      <div className={"cs-pair " + cls}>
        {[0, 1].map((i) => (
          <label key={i} className="cs-pl">
            <span>{labels[i]}</span>
            <input ref={i === 0 ? first : undefined} className="sv-in cs-ii" inputMode="numeric" pattern="[0-9]*"
              value={i === 0 ? x : y} disabled={disabled}
              onChange={(e) => (i === 0 ? set(onlyNum(e.target.value), y) : set(x, onlyNum(e.target.value)))} onKeyDown={key} />
            {a.u && <em>{a.u}</em>}
          </label>
        ))}
      </div>
    );
  }
  return (
    <div className={"cs-iin " + cls}>
      <input ref={first} className="sv-in cs-ii" inputMode="numeric" pattern="[0-9]*" aria-label="답"
        value={value || ""} disabled={disabled} placeholder="숫자"
        onChange={(e) => onChange(onlyNum(e.target.value))} onKeyDown={key} />
      {a.u && <em className="cs-unit">{a.u}</em>}
    </div>
  );
}

// ── 자료: 문제지 · 해설지 · OMR — 바로 인쇄 / 다운로드 ─────────────────────────
const PICK_KEY = "ash.cs.docs";
function readPick() {
  try { const v = JSON.parse(localStorage.getItem(PICK_KEY) || "null"); if (Array.isArray(v) && v.length) return v.filter((x) => DOCS.some((d) => d.id === x)); } catch { /* 무시 */ }
  return ["problems", "omr"];
}

async function fetchText(url) {
  const r = await fetch(url, { cache: "no-cache" });
  if (!r.ok) throw new Error(`인쇄 파일을 불러오지 못했어요 (${r.status})`);
  return r.text();
}

/** 고른 문서를 한 창에서 인쇄 */
export async function printDocs(catId, set, picks, win) {
  const order = DOCS.map((d) => d.id).filter((id) => picks.includes(id));
  const parts = [];
  for (const id of order) {
    if (id === "omr") parts.push({ kind: "omr", html: cardHtml(layoutCard({ cat: catId, no: set.no, title: set.title, short: set.short, items: set.items })) });
    else parts.push({ kind: "doc", cls: id === "problems" ? "cs-p" : "cs-s", html: await fetchText(printUrl(catId, set.no, id)) });
  }
  const names = order.map((id) => DOCS.find((d) => d.id === id).label).join(" · ");
  fillPrintWindow(win, composePrint(parts, `${set.key} ${names}`));
}

function saveBlob(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = name; a.rel = "noopener";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
function clickLink(url) {
  const a = document.createElement("a");
  a.href = url; a.rel = "noopener";
  document.body.appendChild(a); a.click(); a.remove();
}

/** 공개 버킷의 PDF 를 받아 온다 — 단순 GET 이라 CORS 사전 요청이 없다. 없으면 NOFILE, 막히면(네트워크 · CORS) NET */
async function fetchPdf(url) {
  let r;
  try { r = await fetch(url, { cache: "no-cache" }); } catch { throw new Error("NET"); }
  if (!r.ok) throw new Error("NOFILE");
  return new Uint8Array(await r.arrayBuffer());
}

export function DocsPanel({ catId, set, files, say }) {
  const [picks, setPicks] = useState(readPick);
  const [busy, setBusy] = useState(null);   // "print" | "down" | null
  const [prog, setProg] = useState("");
  const tog = (id) => setPicks((p) => {
    const n = p.includes(id) ? p.filter((x) => x !== id) : [...p, id];
    try { localStorage.setItem(PICK_KEY, JSON.stringify(n)); } catch { /* 무시 */ }
    return n;
  });
  const pages = (id) => fileInfo(files, set.no, id)?.pages || (id === "omr" ? 2 : null);
  const size = (id) => fmtBytes(fileInfo(files, set.no, id)?.bytes);

  const onPrint = () => {
    if (!picks.length) { say("인쇄할 자료를 하나 이상 골라 주세요"); return; }
    const win = openPrintWindow();        // 클릭 순간에 창부터 (팝업 차단 회피)
    if (!win) { say("새 창이 막혔어요 — 브라우저에서 이 사이트의 팝업을 허용해 주세요"); return; }
    setBusy("print");
    printDocs(catId, set, picks, win)
      .catch((e) => failPrintWindow(win, e?.message || "인쇄를 준비하지 못했어요"))
      .finally(() => setBusy(null));
  };

  const onDown = async () => {
    if (!picks.length) { say("받을 자료를 하나 이상 골라 주세요"); return; }
    const order = DOCS.map((d) => d.id).filter((id) => picks.includes(id));
    setBusy("down"); setProg("");
    // 파일 이름은 앱이 붙인다(blob + a.download) — 서버 Content-Disposition 의 한글 처리와 상관없이 「01-야구-문제.pdf」
    try {
      if (order.length === 1) {
        const id = order[0];
        let data;
        try { data = await fetchPdf(pdfRawUrl(catId, set.no, id)); }
        catch (e) {
          if (e.message !== "NET") throw e;
          clickLink(pdfUrl(catId, set, id));          // 받아 오기가 막히면 서버가 붙이는 이름(?download=)으로
          say(`${DOCS.find((d) => d.id === id).label}를 받는 중이에요`);
          return;
        }
        saveBlob(new Blob([data], { type: "application/pdf" }), downloadName(set, id));
        say(`${DOCS.find((d) => d.id === id).label}를 받았어요`);
      } else {
        const out = [];
        for (let i = 0; i < order.length; i++) {
          setProg(`${i + 1}/${order.length}`);
          out.push({ name: downloadName(set, order[i]), data: await fetchPdf(pdfRawUrl(catId, set.no, order[i])) });
        }
        saveBlob(new Blob([zipStore(out)], { type: "application/zip" }), `${set.key}.zip`);
        say(`${order.length}개 파일을 ZIP 하나로 받았어요`);
      }
    } catch (e) {
      say(e?.message === "NOFILE" ? "파일이 아직 올라가지 않았어요 — 지금은 「바로 인쇄」에서 PDF로 저장할 수 있어요" : "받지 못했어요 — 연결을 확인하고 다시 시도해 주세요");
    } finally { setBusy(null); setProg(""); }
  };

  return (
    <div className="cs-card cs-docs">
      <div className="cs-ch"><b>📂 자료</b><span>고른 것만 인쇄하거나 받아요</span></div>
      <div className="cs-dchips" role="group" aria-label="자료 고르기">
        {DOCS.map((d) => {
          const on = picks.includes(d.id);
          const pg = pages(d.id);
          return (
            <button key={d.id} type="button" className={"cs-dchip" + (on ? " on" : "")} aria-pressed={on} onClick={() => tog(d.id)}>
              <span className="ck" aria-hidden="true">{on ? "✓" : ""}</span>
              <span className="ic" aria-hidden="true">{d.ic}</span>
              <span className="nm">{d.label}<small>{pg ? `${pg}쪽` : ""}{size(d.id) ? ` · ${size(d.id)}` : ""}</small></span>
            </button>
          );
        })}
      </div>
      <div className="cs-dbtns">
        <button className="sv-btn pri" disabled={!!busy} onClick={onPrint}>{busy === "print" ? "준비 중…" : "🖨 바로 인쇄"}</button>
        <button className="sv-btn" disabled={!!busy} onClick={onDown}>{busy === "down" ? `받는 중… ${prog}` : "⬇ 다운로드"}</button>
      </div>
      <p className="cs-dnote">여러 개를 고르면 인쇄는 한 번에 이어서, 다운로드는 ZIP 파일 하나로 받아요. OMR 카드는 A4 2쪽(1쪽에 앞 번호, 2쪽에 나머지)이에요.</p>
    </div>
  );
}
