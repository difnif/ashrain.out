// ashrain.out — 인라인 씬 시스템 (v2.0)
// 본문 lines 사이 [[fig:씬id]] 마커 자리에 씬이 삽입되는 "글·그림 교차" 구조.
// - sequence 씬: 업로드 컷 크로스페이드 (화면에 보일 때 재생) / 미업로드 시 설명 플레이스홀더
// - diagram 씬: 코드 다이어그램 (equal-bars, hanja-modify) — 이미지 불필요
// - 관리자: sequence 씬 우상단 ✏️ → 업로드 에디터 (순서대로 / 드래그앤드롭·zip, Enter/ESC 확인)
// 저장: Supabase Storage 'figures' 버킷, {conceptId}/{blockId}/{씬id}{n}.png
import { useEffect, useRef, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";

const CSS = `
.afs { margin: 14px auto; max-width: 430px; }
.afs-frame { position: relative; width: 100%; height: 205px; border-radius: 12px; overflow: hidden;
  background: #FFFFFF; border: 1px solid #E2E8F0; }
.afs-frame.diag { height: auto; padding: 10px 8px; box-sizing: border-box; }
.afs-frame img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;
  opacity: 0; transition: opacity .6s ease; }
.afs-frame img.on { opacity: 1; }
.afs-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 7px;
  width: 100%; height: 205px; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 12px; box-sizing: border-box; }
.afs-empty-l { font-size: 13px; font-weight: 800; color: #475569; text-align: center; }
.afs-empty-t { font-size: 12px; color: #64748B; text-align: center; line-height: 1.55; }
.afs-empty-n { font-size: 11px; font-weight: 800; color: #94A3B8; }
.afs-cap { font-size: 12px; color: var(--mut, #64748B); text-align: center; margin: 7px 4px 0; line-height: 1.5; }
.afs-pen { position: absolute; top: 7px; right: 7px; z-index: 5; background: #fff; border: 1px solid #E2E8F0;
  border-radius: 8px; font-size: 12.5px; padding: 4px 7px; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.1); }
.afs-penwrap { position: relative; }
/* ── 에디터 모달 ── */
.af-dim2 { position: fixed; inset: 0; background: rgba(0,0,0,.45); z-index: 80; }
.af-modal { position: fixed; left: 50%; top: 50%; transform: translate(-50%,-50%); z-index: 81;
  width: min(680px, 94vw); max-height: 88vh; overflow-y: auto; background: var(--card, #fff);
  border: 1px solid var(--bd, #DFE3E8); border-radius: 16px; padding: 16px;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; box-sizing: border-box; }
.af-mh { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.af-mt { font-size: 15px; font-weight: 800; color: var(--ink, #1F2937); margin: 0; flex: 1; }
.af-x { background: none; border: none; color: var(--mut, #8A929C); font-size: 16px; cursor: pointer; }
.af-tabs { display: flex; gap: 6px; margin-bottom: 12px; }
.af-tab { background: transparent; border: 1px solid var(--inbd, #D3D9DF); border-radius: 999px;
  color: var(--mut, #8A929C); font-size: 12.5px; font-weight: 700; padding: 7px 13px; cursor: pointer; }
.af-tab.on { border-color: var(--ac, #0DA95F); color: var(--ac, #0DA95F); }
.af-slab { font-size: 12.5px; font-weight: 800; color: var(--ink, #1F2937); margin: 12px 0 6px; }
.af-cells { display: flex; gap: 8px; flex-wrap: wrap; }
.af-cell { position: relative; width: 96px; }
.af-cellbox { width: 96px; height: 96px; border: 1.5px dashed var(--inbd, #CBD5E1); border-radius: 10px;
  background: var(--in, #F4F6F8); display: flex; align-items: center; justify-content: center;
  cursor: pointer; overflow: hidden; }
.af-cellbox img { width: 100%; height: 100%; object-fit: contain; }
.af-cellbox.has { border-style: solid; }
.af-cell-n { font-size: 10.5px; color: var(--mut, #8A929C); text-align: center; margin-top: 3px; font-weight: 700; }
.af-del { position: absolute; top: -6px; right: -6px; background: #DC2626; color: #fff; border: none;
  border-radius: 999px; width: 20px; height: 20px; font-size: 11px; cursor: pointer; line-height: 1; }
.af-newtag { position: absolute; left: 4px; top: 4px; background: var(--ac, #0DA95F); color: #fff;
  font-size: 9.5px; font-weight: 800; border-radius: 5px; padding: 1px 5px; }
.af-drop { border: 2px dashed var(--inbd, #CBD5E1); border-radius: 12px; padding: 22px 14px;
  text-align: center; color: var(--mut, #8A929C); font-size: 13px; line-height: 1.7; }
.af-drop.over { border-color: var(--ac, #0DA95F); color: var(--ac, #0DA95F); }
.af-conv { font-size: 12px; color: var(--mut, #8A929C); background: var(--in, #F4F6F8);
  border-radius: 8px; padding: 8px 10px; margin-top: 8px; word-break: break-all; }
.af-warn { color: #DC2626; font-size: 12px; margin-top: 8px; }
.af-foot { display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px; }
.af-btn { border: none; border-radius: 10px; font-size: 13.5px; font-weight: 800; padding: 10px 16px; cursor: pointer; }
.af-ok { background: var(--ac, #0DA95F); color: #fff; }
.af-cancel { background: transparent; color: var(--mut, #8A929C); border: 1px solid var(--bd, #DFE3E8); }
.af-hint { font-size: 11.5px; color: var(--mut, #8A929C); margin-top: 6px; }
`;

const FRAME_MS = 1600;
export const MJ_STYLE = "flat minimal vector illustration, thick clean outlines, white background, teal and warm amber accent colors, no text, no letters, no numbers, simple friendly educational style for a middle school math app, square 1:1 --style raw --no text, letters, numbers, watermark";

/* ══════════ 코드 다이어그램들 ══════════ */
function EqualBars({ params, play }) {
  const [t, b] = [params?.top || [6, 8], params?.bottom || [3, 4]];
  const W = 250, H = 26, fw = (n, d) => (W * n) / d;
  const cells = (d, color) => Array.from({ length: d - 1 }, (_, i) => (
    <line key={i} x1={(W * (i + 1)) / d} y1={0} x2={(W * (i + 1)) / d} y2={H} stroke={color} strokeWidth="1.5" />
  ));
  return (
    <svg viewBox="0 0 330 122" style={{ width: "100%", display: "block" }}>
      <g transform="translate(10,14)">
        <rect width={W} height={H} rx="5" fill="#fff" stroke="#94A3B8" strokeWidth="2" />
        <rect width={play ? fw(t[0], t[1]) : 0} height={H} rx="5" fill="#99F6E4" style={{ transition: "width .9s ease" }} />
        <g>{cells(t[1], "#94A3B8")}</g>
        <text x={W + 10} y={H - 7} fontSize="15" fontWeight="700" fill="#64748B">{t[0]}/{t[1]}</text>
      </g>
      <g transform="translate(10,60)">
        <rect width={W} height={H} rx="5" fill="#fff" stroke="#0D9488" strokeWidth="2.5" />
        <rect width={play ? fw(b[0], b[1]) : 0} height={H} rx="5" fill="#5EEAD4" style={{ transition: "width .9s ease .5s" }} />
        <g>{cells(b[1], "#0D9488")}</g>
        <text x={W + 10} y={H - 6} fontSize="15" fontWeight="800" fill="#0D9488">{b[0]}/{b[1]}</text>
      </g>
      <text x="135" y="112" textAnchor="middle" fontSize="12" fontWeight="700" fill="#0D9488">색칠된 크기 똑같죠? 칸만 줄었을 뿐!</text>
    </svg>
  );
}

function HanjaModify({ params, play }) {
  const p = { left: "約", leftSub: "줄일 약", right: "數", rightSub: "셈 수",
    note: "約이 數를 꾸며요", result: '= "줄여 주는 수"', ...(params || {}) };
  const st = (d) => ({ opacity: play ? 1 : 0, transition: `opacity .6s ease ${d}s` });
  return (
    <svg viewBox="0 0 340 150" style={{ width: "100%", display: "block" }}>
      <g style={st(0)}>
        <text x="105" y="58" textAnchor="middle" fontSize="46" fontWeight="800" fill="#1F2937">{p.left}</text>
        <text x="235" y="58" textAnchor="middle" fontSize="46" fontWeight="800" fill="#1F2937">{p.right}</text>
        <text x="105" y="82" textAnchor="middle" fontSize="13" fontWeight="800" fill="#D97706">{p.leftSub}</text>
        <text x="235" y="82" textAnchor="middle" fontSize="13" fontWeight="800" fill="#64748B">{p.rightSub}</text>
      </g>
      <g style={st(0.7)}>
        <path d="M 122 92 C 150 112, 190 112, 218 94" fill="none" stroke="#0D9488" strokeWidth="3" strokeLinecap="round" />
        <path d="M 218 94 l -13 2 l 7 11 z" fill="#0D9488" />
        <text x="170" y="126" textAnchor="middle" fontSize="12.5" fontWeight="700" fill="#0D9488">{p.note}</text>
      </g>
      <text x="170" y="146" textAnchor="middle" fontSize="17" fontWeight="800" fill="#0D9488" style={st(1.4)}>{p.result}</text>
    </svg>
  );
}
const DIAGRAMS = { "equal-bars": EqualBars, "hanja-modify": HanjaModify };

/* ══════════ 인라인 씬 ══════════ */
export function AnimScene({ sceneId, figure, conceptId, blockId, isAdmin = false, theme = "light" }) {
  const scene = (figure?.scenes || []).find((s) => s.id === sceneId);
  const dir = `${conceptId}/${blockId}`;
  const [files, setFiles] = useState(null);
  const [frame, setFrame] = useState(0);
  const [play, setPlay] = useState(false);
  const [edit, setEdit] = useState(false);
  const ref = useRef(null);

  const refresh = useCallback(async () => {
    if (!scene || scene.anim === "diagram") { setFiles({}); return; }
    const { data } = await supabase.storage.from("figures").list(dir, { limit: 100 });
    const map = {};
    for (const f of data || []) {
      const key = f.name.replace(/\.[^.]+$/, "");
      const { data: pu } = supabase.storage.from("figures").getPublicUrl(`${dir}/${f.name}`);
      map[key] = { name: f.name, url: pu.publicUrl + "?v=" + encodeURIComponent(f.updated_at || "") };
    }
    setFiles(map);
  }, [dir, scene?.id]); // eslint-disable-line
  useEffect(() => { refresh(); }, [refresh]);

  // 화면에 보일 때만 재생
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") { setPlay(true); return; }
    const ob = new IntersectionObserver(([e]) => setPlay(e.isIntersecting), { threshold: 0.35 });
    ob.observe(el);
    return () => ob.disconnect();
  }, []);

  const urls = scene && scene.anim !== "diagram" && files
    ? Array.from({ length: scene.count || 0 }, (_, i) => files[`${scene.id}${i + 1}`]?.url).filter(Boolean) : [];

  useEffect(() => {
    if (!play || urls.length < 2) return;
    const iv = setInterval(() => setFrame((f) => (f + 1) % urls.length), FRAME_MS);
    return () => clearInterval(iv);
  }, [play, urls.length]);

  if (!scene) return null;
  const Diag = scene.anim === "diagram" ? DIAGRAMS[scene.diagram] : null;

  return (
    <div className="afs" ref={ref}>
      <style>{CSS}</style>
      <div className="afs-penwrap">
        {isAdmin && scene.anim !== "diagram" && (
          <button className="afs-pen" onClick={() => setEdit(true)} title="이미지 업로드/수정">✏️</button>
        )}
        {Diag ? (
          <div className="afs-frame diag"><Diag params={scene.params} play={play} /></div>
        ) : urls.length ? (
          <div className="afs-frame">
            {urls.map((u, i) => <img key={u} src={u} alt="" className={i === (urls.length > 1 ? frame : 0) ? "on" : ""} />)}
          </div>
        ) : (
          <div className="afs-empty">
            <span className="afs-empty-l">{scene.label}</span>
            <span className="afs-empty-t">{scene.desc}</span>
            <span className="afs-empty-n">🖼 이미지 {scene.count}장 자리{isAdmin ? " — ✏️로 업로드" : " (준비 중)"}</span>
          </div>
        )}
      </div>
      {(scene.caption || (urls.length && scene.label)) ? <p className="afs-cap">{scene.caption || scene.label}</p> : null}
      {edit && <Editor scenes={(figure.scenes || []).filter((s) => s.anim !== "diagram")} dir={dir}
        files={files || {}} onClose={() => setEdit(false)} onSaved={() => { setEdit(false); refresh(); }} />}
    </div>
  );
}

/* ══════════ 관리자 에디터 (블록의 이미지 씬 전체) ══════════ */
function Editor({ scenes, dir, files, onClose, onSaved }) {
  const keys = scenes.flatMap((s) => Array.from({ length: s.count }, (_, i) => `${s.id}${i + 1}`));
  const [mode, setMode] = useState("cells");
  const [pending, setPending] = useState({});
  const [removed, setRemoved] = useState({});
  const [warn, setWarn] = useState("");
  const [confirming, setConfirming] = useState(false);
  const [busy, setBusy] = useState(false);
  const [over, setOver] = useState(false);
  const pickKey = useRef(null);
  const fileRef = useRef(null);

  const assign = (fileList) => {
    const w = []; const next = { ...pending };
    for (const f of fileList) {
      const base = f.name.replace(/\.[^.]+$/, "").toLowerCase();
      const hit = keys.find((k) => base === k || base.endsWith("_" + k) || base.endsWith(k));
      if (hit) next[hit] = f; else w.push(f.name);
    }
    setPending(next);
    setWarn(w.length ? "규칙에 안 맞아 건너뜀: " + w.join(", ") : "");
  };

  const onDrop = async (e) => {
    e.preventDefault(); setOver(false);
    const items = [...e.dataTransfer.files];
    const zips = items.filter((f) => /\.zip$/i.test(f.name));
    const plain = items.filter((f) => !/\.zip$/i.test(f.name));
    if (zips.length) {
      try {
        const mod = await import(/* @vite-ignore */ "https://cdn.jsdelivr.net/npm/jszip@3.10.1/+esm");
        const JSZip = mod.default;
        for (const z of zips) {
          const zip = await JSZip.loadAsync(z);
          for (const name of Object.keys(zip.files)) {
            const entry = zip.files[name];
            if (entry.dir || !/\.(png|jpe?g|webp)$/i.test(name)) continue;
            const blob = await entry.async("blob");
            plain.push(new File([blob], name.split("/").pop(), { type: "image/png" }));
          }
        }
      } catch { setWarn("zip 해제 실패 — 개별 파일로 드래그해 주세요"); }
    }
    assign(plain);
  };

  const doSave = async () => {
    setBusy(true);
    try {
      for (const k of Object.keys(removed)) {
        if (!pending[k] && files[k]) await supabase.storage.from("figures").remove([`${dir}/${files[k].name}`]);
      }
      for (const [k, f] of Object.entries(pending)) {
        const ext = (f.name.match(/\.[^.]+$/) || [".png"])[0].toLowerCase();
        const { error } = await supabase.storage.from("figures")
          .upload(`${dir}/${k}${ext}`, f, { upsert: true, contentType: f.type || "image/png" });
        if (error) throw error;
        if (files[k] && files[k].name !== `${k}${ext}`)
          await supabase.storage.from("figures").remove([`${dir}/${files[k].name}`]);
      }
      onSaved();
    } catch (e) {
      setWarn("업로드 실패: " + (e?.message || String(e)) + " (figures 버킷 SQL 실행 여부 확인)");
      setBusy(false); setConfirming(false);
    }
  };

  useEffect(() => {
    const h = (e) => {
      if (!confirming) { if (e.key === "Escape") onClose(); return; }
      if (e.key === "Enter") { e.preventDefault(); if (!busy) doSave(); }
      if (e.key === "Escape") { e.preventDefault(); setConfirming(false); }
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }); // eslint-disable-line

  const cellView = (k) => {
    const p = pending[k];
    const cur = !removed[k] && files[k];
    const url = p ? URL.createObjectURL(p) : cur ? files[k].url : null;
    return (
      <div key={k} className="af-cell">
        <div className={"af-cellbox" + (url ? " has" : "")}
          onClick={() => { pickKey.current = k; fileRef.current.click(); }}>
          {url ? <img src={url} alt="" /> : <span style={{ color: "var(--mut,#8A929C)", fontSize: 20 }}>＋</span>}
          {p && <span className="af-newtag">새 파일</span>}
        </div>
        {(p || cur) && <button className="af-del" onClick={(e) => { e.stopPropagation();
          if (p) setPending((s) => { const n = { ...s }; delete n[k]; return n; });
          else setRemoved((s) => ({ ...s, [k]: true }));
        }}>✕</button>}
        <p className="af-cell-n">{k}</p>
      </div>
    );
  };

  const delCount = Object.keys(removed).filter((k) => !pending[k] && files[k]).length;
  // eslint-disable-next-line
  function PromptCard({ scene }) {
    const [ok, setOk] = useState(false);
    const full = (scene.prompt ? scene.prompt + ", " : "") + (scene.style || MJ_STYLE);
    const copy = async () => {
      try { await navigator.clipboard.writeText(full); }
      catch { const ta = document.createElement("textarea"); ta.value = full; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); document.body.removeChild(ta); }
      setOk(true); setTimeout(() => setOk(false), 1400);
    };
    return (
      <div style={{ border: "1px solid var(--bd,#DFE3E8)", borderRadius: 10, padding: "10px 12px", marginBottom: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
          <b style={{ fontSize: 12.5, color: "var(--ink,#1F2937)", flex: 1 }}>{scene.label} ({scene.count}컷: {Array.from({length: scene.count}, (_,i)=>scene.id+(i+1)).join(", ")})</b>
          <button className="af-tab" onClick={copy}>{ok ? "✓ 복사됨" : "📋 복사"}</button>
        </div>
        {scene.prompt && (
          <p style={{ fontSize: 11.5, color: "var(--mut,#8A929C)", margin: 0, lineHeight: 1.6, wordBreak: "break-all" }}>{full}</p>
        )}
        {scene.cutPrompts?.map((cp, i) => <CutPrompt key={i} label={(scene.cuts?.[i] || `${i + 1}컷`) + ` (${scene.id}${i + 1})`} text={cp + ", " + (scene.style || MJ_STYLE)} />)}
        {!scene.prompt && !scene.cutPrompts && <p style={{ fontSize: 11.5, color: "var(--mut,#8A929C)", margin: 0 }}>(프롬프트 미작성)</p>}
        {scene.cuts && !scene.cutPrompts && <p style={{ fontSize: 11.5, color: "var(--mut,#8A929C)", margin: "6px 0 0" }}>컷 구성: {scene.cuts.join(" → ")}</p>}
      </div>
    );
  }
  const changes = Object.keys(pending).length + delCount;

  return (
    <>
      <div className="af-dim2" onClick={busy ? undefined : onClose} />
      <div className="af-modal">
        <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }}
          onChange={(e) => { const f = e.target.files?.[0]; if (f && pickKey.current) {
            setPending((s) => ({ ...s, [pickKey.current]: f }));
            setRemoved((s) => { const n = { ...s }; delete n[pickKey.current]; return n; });
          } e.target.value = ""; }} />
        {!confirming ? (
          <>
            <div className="af-mh"><h3 className="af-mt">🖼 이미지 업로드 / 수정</h3><button className="af-x" onClick={onClose}>✕</button></div>
            <div className="af-tabs">
              <button className={"af-tab" + (mode === "cells" ? " on" : "")} onClick={() => setMode("cells")}>순서대로 넣기</button>
              <button className={"af-tab" + (mode === "drop" ? " on" : "")} onClick={() => setMode("drop")}>드래그앤드롭</button>
              <button className={"af-tab" + (mode === "prompt" ? " on" : "")} onClick={() => setMode("prompt")}>🎨 프롬프트</button>
            </div>
            {mode === "prompt" && scenes.map((s) => (
              <PromptCard key={s.id} scene={s} />
            ))}
            {mode === "cells" && scenes.map((s) => (
              <div key={s.id}>
                <p className="af-slab">{s.label}</p>
                <div className="af-cells">{Array.from({ length: s.count }, (_, i) => cellView(`${s.id}${i + 1}`))}</div>
              </div>
            ))}
            {mode === "drop" && (
              <>
                <div className={"af-drop" + (over ? " over" : "")}
                  onDragOver={(e) => { e.preventDefault(); setOver(true); }}
                  onDragLeave={() => setOver(false)} onDrop={onDrop}>
                  이미지 파일들(또는 zip)을 여기에 놓으세요<br />파일명 규칙에 따라 자동으로 자리에 들어가요
                </div>
                <p className="af-conv">규칙: {keys.map((k) => k + ".png").join(" · ")} (끝이 이 이름이면 인식 — 예: yaksu_a1.png ✓)</p>
                <div className="af-cells" style={{ marginTop: 10 }}>{keys.map(cellView)}</div>
              </>
            )}
            {warn && <p className="af-warn">⚠ {warn}</p>}
            <div className="af-foot">
              <button className="af-btn af-cancel" onClick={onClose}>닫기</button>
              <button className="af-btn af-ok" disabled={!changes} onClick={() => changes && setConfirming(true)}>확인 ({changes}건)</button>
            </div>
          </>
        ) : (
          <>
            <div className="af-mh"><h3 className="af-mt">이 이미지가 맞나요?</h3></div>
            <div className="af-cells">{keys.filter((k) => pending[k] || (!removed[k] && files[k])).map(cellView)}</div>
            <p className="af-hint">Enter = 업로드 · ESC = 취소{delCount ? ` · 삭제 예정 ${delCount}건 포함` : ""}</p>
            <div className="af-foot">
              <button className="af-btn af-cancel" onClick={() => setConfirming(false)} disabled={busy}>취소</button>
              <button className="af-btn af-ok" onClick={doSave} disabled={busy}>{busy ? "업로드 중…" : "확인 — 업로드"}</button>
            </div>
          </>
        )}
      </div>
    </>
  );
}

function CutPrompt({ label, text }) {
  const [ok, setOk] = useState(false);
  const copy = async () => {
    try { await navigator.clipboard.writeText(text); }
    catch { const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); document.body.removeChild(ta); }
    setOk(true); setTimeout(() => setOk(false), 1300);
  };
  return (
    <div style={{ display: "flex", gap: 8, alignItems: "flex-start", borderTop: "1px dashed var(--bd,#DFE3E8)", padding: "7px 0 2px", marginTop: 7 }}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <b style={{ fontSize: 11.5, color: "var(--ink,#1F2937)" }}>{label}</b>
        <p style={{ fontSize: 11, color: "var(--mut,#8A929C)", margin: "3px 0 0", lineHeight: 1.55, wordBreak: "break-all" }}>{text}</p>
      </div>
      <button className="af-tab" onClick={copy}>{ok ? "✓" : "📋"}</button>
    </div>
  );
}

export { Editor as SceneEditor };
export default AnimScene;
