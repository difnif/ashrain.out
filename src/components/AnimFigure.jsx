// ashrain.out — 이미지 슬롯 애니메이션 figure (v1.0)
// 개념 blocks의 figure.kind === "animset" 렌더러.
// - 이미지 없으면: 씬 설명이 담긴 점선 플레이스홀더(레이아웃 검토용)
// - 이미지 있으면: 씬 순차 재생(컷 크로스페이드) + 다이어그램 씬(equal-bars)
// - 관리자: 우상단 ✏️ → [순서대로 넣기 | 드래그앤드롭(zip 지원)] → 미리보기 확인(Enter/ESC)
// 저장: Supabase Storage 'figures' 버킷, 경로 {conceptId}/{blockId}/{씬id}{n}.png
import { useEffect, useRef, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";

const CSS = `
.af-wrap { margin-top: 12px; }
.af-stage { position: relative; border: 1px solid var(--bd, #DFE3E8); border-radius: 14px;
  background: #F8FAFC; padding: 14px 14px 10px; }
.af-grid { display: flex; gap: 12px; flex-wrap: wrap; }
.af-scene { flex: 1 1 180px; min-width: 150px; }
.af-lab { font-size: 13px; font-weight: 800; color: #1F2937; margin: 0 0 6px; line-height: 1.4; }
.af-frame { position: relative; width: 100%; aspect-ratio: 1 / 1; border-radius: 10px; overflow: hidden;
  background: #fff; border: 1px solid #E2E8F0; }
.af-frame img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain;
  opacity: 0; transition: opacity .6s ease; }
.af-frame img.on { opacity: 1; }
.af-scene.dim .af-frame { opacity: .5; }
.af-empty { display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 6px; width: 100%; aspect-ratio: 1 / 1; border: 2px dashed #CBD5E1; border-radius: 10px;
  background: transparent; padding: 10px; box-sizing: border-box; }
.af-empty-t { font-size: 12px; color: #64748B; text-align: center; line-height: 1.5; }
.af-empty-n { font-size: 11px; font-weight: 800; color: #94A3B8; }
.af-cap { font-size: 12px; color: #64748B; text-align: center; margin: 10px 2px 2px; }
.af-pen { position: absolute; top: 8px; right: 8px; z-index: 5; background: #fff; border: 1px solid #E2E8F0;
  border-radius: 8px; font-size: 13px; padding: 5px 8px; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
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

const FRAME_MS = 1500, HOLD_MS = 900;

// ── 약분 등가 막대 다이어그램 ──
function EqualBars({ params, active }) {
  const [t, b] = [params?.top || [6, 8], params?.bottom || [3, 4]];
  const W = 240, H = 26, fillW = (n, d) => (W * n) / d;
  const cell = (d, y, color) => Array.from({ length: d - 1 }, (_, i) => (
    <line key={i} x1={(W * (i + 1)) / d} y1={y} x2={(W * (i + 1)) / d} y2={y + H} stroke={color} strokeWidth="1.5" />
  ));
  return (
    <svg viewBox="0 0 300 120" style={{ width: "100%", height: "100%" }}>
      <g transform="translate(8,18)">
        <rect width={W} height={H} rx="5" fill="#fff" stroke="#94A3B8" strokeWidth="2" />
        <rect width={fillW(t[0], t[1])} height={H} rx="5" fill="#99F6E4" style={{ transition: "width 1s", width: active ? fillW(t[0], t[1]) : 0 }} />
        {cell(t[1], 0, "#94A3B8")}
        <text x={W + 10} y={H - 7} fontSize="15" fontWeight="700" fill="#64748B">{t[0]}/{t[1]}</text>
      </g>
      <g transform="translate(8,64)">
        <rect width={W} height={H} rx="5" fill="#fff" stroke="#0D9488" strokeWidth="2.5" />
        <rect width={fillW(b[0], b[1])} height={H} rx="5" fill="#5EEAD4" style={{ transition: "width 1s .4s", width: active ? fillW(b[0], b[1]) : 0 }} />
        {cell(b[1], 0, "#0D9488")}
        <text x={W + 10} y={H - 6} fontSize="15" fontWeight="800" fill="#0D9488">{b[0]}/{b[1]}</text>
      </g>
      <text x="128" y="112" textAnchor="middle" fontSize="11.5" fontWeight="700" fill="#0D9488">색칠된 크기 똑같죠? 칸만 줄었을 뿐!</text>
    </svg>
  );
}

export default function AnimFigure({ figure, conceptId, blockId, isAdmin = false, theme = "light" }) {
  const scenes = figure?.scenes || [];
  const dir = `${conceptId}/${blockId}`;
  const [files, setFiles] = useState({});     // "a1" -> { url }
  const [tick, setTick] = useState(0);
  const [edit, setEdit] = useState(false);

  const refresh = useCallback(async () => {
    const { data } = await supabase.storage.from("figures").list(dir, { limit: 100 });
    const map = {};
    for (const f of data || []) {
      const key = f.name.replace(/\.[^.]+$/, "");
      const { data: pu } = supabase.storage.from("figures").getPublicUrl(`${dir}/${f.name}`);
      map[key] = { name: f.name, url: pu.publicUrl + "?v=" + encodeURIComponent(f.updated_at || "") };
    }
    setFiles(map);
  }, [dir]);
  useEffect(() => { refresh(); }, [refresh]);

  // 씬별 프레임 목록
  const frames = scenes.map((s) =>
    s.anim === "diagram" ? ["diagram"] :
    Array.from({ length: s.count || 0 }, (_, i) => files[`${s.id}${i + 1}`]?.url).filter(Boolean));
  const durations = frames.map((f) => Math.max(f.length, 1) * FRAME_MS + HOLD_MS);
  const total = durations.reduce((a, b) => a + b, 0) || 1;

  useEffect(() => {
    const iv = setInterval(() => setTick((t) => (t + 100) % total), 100);
    return () => clearInterval(iv);
  }, [total]);

  let acc = 0, activeScene = 0, activeFrame = 0;
  for (let i = 0; i < durations.length; i++) {
    if (tick < acc + durations[i]) {
      activeScene = i;
      activeFrame = Math.min(Math.floor((tick - acc) / FRAME_MS), Math.max(frames[i].length - 1, 0));
      break;
    }
    acc += durations[i];
  }

  return (
    <div className="af-wrap">
      <style>{CSS}</style>
      <div className="af-stage">
        {isAdmin && <button className="af-pen" onClick={() => setEdit(true)} title="이미지 업로드/수정">✏️</button>}
        <div className="af-grid">
          {scenes.map((s, si) => {
            const fr = frames[si];
            const has = s.anim === "diagram" || fr.length > 0;
            return (
              <div key={s.id} className={"af-scene" + (si === activeScene ? "" : " dim")}>
                <p className="af-lab">{s.label}</p>
                {!has ? (
                  <div className="af-empty">
                    <span className="af-empty-t">{s.desc}</span>
                    <span className="af-empty-n">🖼 이미지 {s.count}장 자리{isAdmin ? " — ✏️로 업로드" : " (준비 중)"}</span>
                  </div>
                ) : s.anim === "diagram" ? (
                  <div className="af-frame"><EqualBars params={s.params} active={si === activeScene} /></div>
                ) : (
                  <div className="af-frame">
                    {fr.map((u, fi) => (
                      <img key={u} src={u} alt="" className={si === activeScene && fi === activeFrame ? "on" : fi === fr.length - 1 && si !== activeScene ? "on" : ""} />
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
        {figure.caption && <p className="af-cap">{figure.caption}</p>}
      </div>
      {edit && <Editor scenes={scenes} dir={dir} files={files} onClose={() => setEdit(false)} onSaved={() => { setEdit(false); refresh(); }} theme={theme} />}
    </div>
  );
}

// ══════════════ 관리자 에디터 ══════════════
function Editor({ scenes, dir, files, onClose, onSaved, theme }) {
  const imgScenes = scenes.filter((s) => s.anim !== "diagram");
  const keys = imgScenes.flatMap((s) => Array.from({ length: s.count }, (_, i) => `${s.id}${i + 1}`));
  const [mode, setMode] = useState("cells");        // cells | drop
  const [pending, setPending] = useState({});       // key -> File
  const [removed, setRemoved] = useState({});       // key -> true
  const [warn, setWarn] = useState("");
  const [confirming, setConfirming] = useState(false);
  const [busy, setBusy] = useState(false);
  const [over, setOver] = useState(false);
  const pickKey = useRef(null);
  const fileRef = useRef(null);

  const assign = (fileList) => {
    const w = [];
    const next = { ...pending };
    for (const f of fileList) {
      const base = f.name.replace(/\.[^.]+$/, "").toLowerCase();
      const hit = keys.find((k) => base === k || base.endsWith("_" + k) || base.endsWith(k));
      if (hit) next[hit] = f;
      else w.push(f.name);
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
      } catch { setWarn("zip 해제에 실패했어요 — 개별 파일로 드래그해 주세요"); }
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
        if (files[k] && files[k].name !== `${k}${ext}`) {
          await supabase.storage.from("figures").remove([`${dir}/${files[k].name}`]);
        }
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

  const changes = Object.keys(pending).length + Object.keys(removed).filter((k) => !pending[k] && files[k]).length;

  return (
    <>
      <div className="af-dim2" onClick={busy ? undefined : onClose} />
      <div className="af-modal">
        <style>{CSS}</style>
        <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }}
          onChange={(e) => { const f = e.target.files?.[0]; if (f && pickKey.current) { setPending((s) => ({ ...s, [pickKey.current]: f })); setRemoved((s) => { const n = { ...s }; delete n[pickKey.current]; return n; }); } e.target.value = ""; }} />
        {!confirming ? (
          <>
            <div className="af-mh"><h3 className="af-mt">🖼 이미지 업로드 / 수정</h3><button className="af-x" onClick={onClose}>✕</button></div>
            <div className="af-tabs">
              <button className={"af-tab" + (mode === "cells" ? " on" : "")} onClick={() => setMode("cells")}>순서대로 넣기</button>
              <button className={"af-tab" + (mode === "drop" ? " on" : "")} onClick={() => setMode("drop")}>드래그앤드롭</button>
            </div>
            {mode === "cells" && imgScenes.map((s) => (
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
            <p className="af-hint">Enter = 업로드 · ESC = 취소{Object.keys(removed).filter((k)=>!pending[k]&&files[k]).length ? ` · 삭제 예정 ${Object.keys(removed).filter((k)=>!pending[k]&&files[k]).length}건 포함` : ""}</p>
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
