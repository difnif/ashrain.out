// ashrain.out — 이미지 등록 현황 (v2.0, 관리자 전용)
// v2.0: ① 교육과정 순 정렬 ② 컷 이름 클릭 → 프롬프트·미리보기·개별 업로드(✂️ 잘라오기 포함) 모달
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";
import { qcode, UNIT_LETTER, UNIT_NAME } from "../lib/qcode";
import { CropAssign, MJ_STYLE } from "./AnimFigure";

const CSS = `
.ai-root { min-height: 100vh; padding: 18px 12px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ai-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.ai-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#1B1E24; --inbd:#2A2E36; }
.ai-wrap { max-width: 720px; margin: 0 auto; }
.ai-top { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.ai-h { color: var(--ink); font-size: 18px; font-weight: 800; margin: 0; flex: 1; }
.ai-back { color: var(--mut); font-size: 13px; cursor: pointer; text-decoration: underline; }
.ai-filters { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; align-items: center; }
.ai-sel { background: var(--card); border: 1px solid var(--bd); border-radius: 10px; color: var(--ink); font-size: 13px; padding: 8px 10px; }
.ai-tgl { background: transparent; border: 1px solid var(--bd); border-radius: 999px; color: var(--mut);
  font-size: 12.5px; font-weight: 700; padding: 7px 12px; cursor: pointer; }
.ai-tgl.on { border-color: var(--ac); color: var(--ac); }
.ai-sum { font-size: 12.5px; color: var(--mut); margin: 0 0 10px; }
.ai-row { display: flex; align-items: center; gap: 10px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 10px; padding: 9px 12px; margin-bottom: 6px; }
.ai-code { font-size: 11.5px; font-weight: 800; letter-spacing: .5px; color: var(--ac); cursor: pointer;
  text-decoration: underline; white-space: nowrap; }
.ai-name { flex: 1; min-width: 0; color: var(--ink); font-size: 13.5px; cursor: pointer;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ai-name:active { color: var(--ac); }
.ai-key { font-size: 11px; color: var(--mut); white-space: nowrap; }
.ai-ok { font-size: 13px; font-weight: 800; color: var(--ac); }
.ai-no { font-size: 13px; font-weight: 800; color: #DC2626; }
.ai-empty { color: var(--mut); text-align: center; padding: 36px 0; font-size: 14px; }
/* ── 컷 모달 ── */
.ai-dim { position: fixed; inset: 0; background: rgba(0,0,0,.45); z-index: 80; }
.ai-modal { position: fixed; left: 50%; top: 50%; transform: translate(-50%,-50%); z-index: 81;
  width: min(560px, 94vw); max-height: 88vh; overflow-y: auto; background: var(--card, #fff);
  border: 1px solid var(--bd, #DFE3E8); border-radius: 16px; padding: 16px; box-sizing: border-box; }
.ai-mh { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 4px; }
.ai-mt { font-size: 15px; font-weight: 800; color: var(--ink); margin: 0; flex: 1; line-height: 1.45; }
.ai-x { background: none; border: none; color: var(--mut); font-size: 16px; cursor: pointer; }
.ai-sub { font-size: 12px; color: var(--mut); margin: 0 0 10px; }
.ai-chain { font-size: 12px; color: var(--mut); background: var(--in); border-radius: 8px; padding: 8px 10px; margin: 0 0 10px; line-height: 1.6; }
.ai-chain b { color: var(--ac); }
.ai-pcard { border: 1px solid var(--bd); border-radius: 10px; padding: 9px 11px; margin-bottom: 8px; }
.ai-plab { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.ai-plab b { font-size: 12px; color: var(--ink); flex: 1; }
.ai-ptxt { font-size: 11px; color: var(--mut); margin: 0; line-height: 1.6; word-break: break-all; }
.ai-btn { border: none; border-radius: 10px; font-size: 13px; font-weight: 800; padding: 9px 14px; cursor: pointer; }
.ai-bok { background: var(--ac); color: #fff; }
.ai-bghost { background: transparent; color: var(--mut); border: 1px solid var(--bd); }
.ai-bdel { background: transparent; color: #DC2626; border: 1px solid #DC2626; }
.ai-pill { background: transparent; border: 1px solid var(--inbd); border-radius: 999px; color: var(--mut);
  font-size: 12px; font-weight: 700; padding: 6px 11px; cursor: pointer; }
.ai-pill.hot { border-color: var(--ac); color: var(--ac); }
.ai-prev { width: 100%; max-width: 260px; height: 170px; margin: 0 auto 10px; border: 1.5px dashed var(--inbd);
  border-radius: 12px; background: var(--in); display: flex; align-items: center; justify-content: center; overflow: hidden; }
.ai-prev img { width: 100%; height: 100%; object-fit: contain; }
.ai-prev.has { border-style: solid; }
.ai-foot { display: flex; gap: 8px; justify-content: flex-end; margin-top: 12px; flex-wrap: wrap; }
.ai-warn { color: #DC2626; font-size: 12px; margin: 8px 0 0; }
`;

const UORDER = Object.keys(UNIT_LETTER);
const parseCid = (cid) => { const m = String(cid).match(/^([mh]\d-\d)-(\d+)$/);
  return m ? [UORDER.indexOf(m[1]), +m[2]] : [99, 999]; };

/* ══════════ 컷 상세 모달 ══════════ */
function CutModal({ row, onClose, onChanged }) {
  const dir = `${row.concept_id}/${row.block_id}`;
  const [cur, setCur] = useState(undefined);        // {name,url} | null
  const [pend, setPend] = useState(null);           // File
  const [crop, setCrop] = useState(false);
  const [busy, setBusy] = useState(false);
  const [warn, setWarn] = useState("");
  const [copied, setCopied] = useState("");

  const loadCur = async () => {
    const { data } = await supabase.storage.from("figures").list(dir, { limit: 100 });
    const f = (data || []).find((x) => x.name.replace(/\.[^.]+$/, "") === row.key);
    if (!f) { setCur(null); return; }
    const { data: pu } = supabase.storage.from("figures").getPublicUrl(`${dir}/${f.name}`);
    setCur({ name: f.name, url: pu.publicUrl + "?v=" + encodeURIComponent(f.updated_at || Date.now()) });
  };
  useEffect(() => { loadCur(); }, []); // eslint-disable-line

  const sc = row.scene;
  const setPrompt = sc.prompt ? sc.prompt + ", " + (sc.style || MJ_STYLE) : "";
  const cutPrompt = sc.cutPrompts?.[row.ci - 1] ? sc.cutPrompts[row.ci - 1] + ", " + (sc.style || MJ_STYLE) : "";

  const copy = async (text, tag) => {
    try { await navigator.clipboard.writeText(text); }
    catch { const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta);
      ta.select(); document.execCommand("copy"); document.body.removeChild(ta); }
    setCopied(tag); setTimeout(() => setCopied(""), 1400);
  };

  const save = async () => {
    if (!pend) return; setBusy(true); setWarn("");
    try {
      const ext = (pend.name.match(/\.[^.]+$/) || [".png"])[0].toLowerCase();
      const { error } = await supabase.storage.from("figures")
        .upload(`${dir}/${row.key}${ext}`, pend, { upsert: true, contentType: pend.type || "image/png" });
      if (error) throw error;
      if (cur && cur.name !== `${row.key}${ext}`)
        await supabase.storage.from("figures").remove([`${dir}/${cur.name}`]);
      setPend(null); await loadCur(); onChanged(true);
    } catch (e) { setWarn("업로드 실패: " + (e?.message || String(e))); }
    setBusy(false);
  };
  const del = async () => {
    if (!cur) return; setBusy(true); setWarn("");
    try { await supabase.storage.from("figures").remove([`${dir}/${cur.name}`]);
      setCur(null); onChanged(false);
    } catch (e) { setWarn("삭제 실패: " + (e?.message || String(e))); }
    setBusy(false);
  };

  const prevUrl = pend ? URL.createObjectURL(pend) : cur?.url;
  return (
    <>
      <div className="ai-dim" onClick={busy ? undefined : onClose} />
      <div className="ai-modal">
        <div className="ai-mh">
          <h3 className="ai-mt">{row.name} <span style={{ color: "var(--mut)", fontWeight: 700 }}>({row.key})</span></h3>
          <button className="ai-x" onClick={onClose}>✕</button>
        </div>
        <p className="ai-sub">{row.code} · {row.title} — {sc.label}</p>
        {sc.cuts?.length ? (
          <p className="ai-chain">컷 구성: {sc.cuts.map((c, i) => i === row.ci - 1
            ? <b key={i}>▶ {c}</b> : <span key={i}>{c}</span>).reduce((a, b) => [a, " → ", b])}</p>
        ) : null}

        {setPrompt && (
          <div className="ai-pcard">
            <div className="ai-plab"><b>🎨 세트 프롬프트 (씬 전체 — 한 장에 {sc.count}컷 서사)</b>
              <button className="ai-pill" onClick={() => copy(setPrompt, "set")}>{copied === "set" ? "✓ 복사됨" : "📋 복사"}</button></div>
            <p className="ai-ptxt">{setPrompt}</p>
          </div>
        )}
        {cutPrompt && (
          <div className="ai-pcard">
            <div className="ai-plab"><b>🎯 이 컷 전용 프롬프트</b>
              <button className="ai-pill" onClick={() => copy(cutPrompt, "cut")}>{copied === "cut" ? "✓ 복사됨" : "📋 복사"}</button></div>
            <p className="ai-ptxt">{cutPrompt}</p>
          </div>
        )}
        {!setPrompt && !cutPrompt && <p className="ai-sub">(프롬프트 미작성 씬)</p>}

        {!crop ? (
          <>
            <div className={"ai-prev" + (prevUrl ? " has" : "")}>
              {prevUrl ? <img src={prevUrl} alt="" /> : <span style={{ color: "var(--mut)", fontSize: 13 }}>미등록 컷</span>}
            </div>
            {pend && <p className="ai-sub" style={{ textAlign: "center" }}>새 파일 대기 중 — 저장을 눌러야 반영돼요</p>}
            {warn && <p className="ai-warn">⚠ {warn}</p>}
            <div className="ai-foot">
              <label className="ai-pill hot" style={{ display: "inline-flex", alignItems: "center" }}>
                🖼 파일 선택
                <input type="file" accept="image/*" style={{ display: "none" }}
                  onChange={(e) => { const f = e.target.files?.[0]; if (f) setPend(f); e.target.value = ""; }} />
              </label>
              <button className="ai-pill hot" onClick={() => setCrop(true)}>✂️ 세트에서 잘라오기</button>
              {cur && <button className="ai-btn ai-bdel" disabled={busy} onClick={del}>삭제</button>}
              <button className="ai-btn ai-bghost" onClick={onClose} disabled={busy}>닫기</button>
              <button className="ai-btn ai-bok" disabled={!pend || busy} onClick={save}>{busy ? "저장 중…" : "저장"}</button>
            </div>
          </>
        ) : (
          <CropAssign single targets={[row.key]} labels={{ [row.key]: row.name }}
            onCancel={() => setCrop(false)}
            onAssign={(m) => { if (m[row.key]) setPend(m[row.key]); setCrop(false); }} />
        )}
      </div>
    </>
  );
}

/* ══════════ 현황 페이지 ══════════ */
export default function AdminImages({ theme = "light" }) {
  const [allowed, setAllowed] = useState(null);
  const [rows, setRows] = useState(null);
  const [f, setF] = useState({ letter: "", onlyMissing: true });
  const [open, setOpen] = useState(null);   // row index in rows

  useEffect(() => {
    (async () => {
      const { data: { user } } = await supabase.auth.getUser();
      const { data: prof } = await supabase.from("profiles").select("role").eq("id", user?.id).maybeSingle();
      if (prof?.role !== "admin") { setAllowed(false); return; }
      setAllowed(true);
      const { data: cs } = await supabase.from("concepts").select("id, title, blocks");
      const targets = [];
      for (const c of cs || []) {
        (c.blocks || []).forEach((b, bi) => {
          (b.figure?.scenes || []).forEach((s, si) => {
            if (s.anim !== "diagram" && s.count > 0)
              targets.push({ concept_id: c.id, title: c.title, block_id: b.id, bi, si, scene: s });
          });
        });
      }
      const dirs = [...new Set(targets.map((t) => `${t.concept_id}/${t.block_id}`))];
      const have = {};
      await Promise.all(dirs.map(async (d) => {
        const { data } = await supabase.storage.from("figures").list(d, { limit: 100 });
        have[d] = new Set((data || []).map((x) => x.name.replace(/\.[^.]+$/, "")));
      }));
      const out = [];
      for (const t of targets) {
        const dir = `${t.concept_id}/${t.block_id}`;
        for (let i = 1; i <= t.scene.count; i++) {
          const key = `${t.scene.id}${i}`;
          out.push({
            concept_id: t.concept_id, title: t.title, block_id: t.block_id, key, ci: i,
            bi: t.bi, si: t.si, scene: t.scene,
            code: qcode(t.concept_id, t.block_id),
            name: t.scene.cuts?.[i - 1] || `${t.scene.label} ${i}컷`,
            ok: have[dir]?.has(key) || false,
          });
        }
      }
      // ── 교육과정 순 정렬: 과정 → 개념 번호 → 블록 → 씬 → 컷 ──
      out.sort((a, b) => {
        const [ua, na] = parseCid(a.concept_id), [ub, nb] = parseCid(b.concept_id);
        return (ua - ub) || (na - nb) || (a.bi - b.bi) || (a.si - b.si) || (a.ci - b.ci);
      });
      setRows(out);
    })();
  }, []);

  if (allowed === false) return (
    <div className={`ai-root ai-${theme}`}><style>{CSS}</style><p className="ai-empty">관리자 전용 화면입니다.</p></div>
  );

  const shown = (rows || []).filter((r) =>
    (!f.letter || r.code.startsWith(f.letter)) && (!f.onlyMissing || !r.ok));
  const done = (rows || []).filter((r) => r.ok).length;

  return (
    <div className={`ai-root ai-${theme}`}>
      <style>{CSS}</style>
      <div className="ai-wrap">
        <div className="ai-top">
          <h1 className="ai-h">🖼 이미지 등록 현황</h1>
          <span className="ai-back" onClick={() => (location.hash = "")}>← 홈</span>
        </div>
        <div className="ai-filters">
          <select className="ai-sel" value={f.letter} onChange={(e) => setF((s) => ({ ...s, letter: e.target.value }))}>
            <option value="">전체 과정</option>
            {Object.entries(UNIT_LETTER).map(([u, l]) => <option key={l} value={l}>{l} · {UNIT_NAME[u]}</option>)}
          </select>
          <button className={"ai-tgl" + (f.onlyMissing ? " on" : "")}
            onClick={() => setF((s) => ({ ...s, onlyMissing: !s.onlyMissing }))}>미등록만 보기</button>
        </div>
        {rows === null ? <p className="ai-empty">불러오는 중…</p> : (
          <>
            <p className="ai-sum">전체 {rows.length}컷 중 등록 {done} · 미등록 {rows.length - done} · 이름을 누르면 프롬프트·업로드 창이 열려요</p>
            {shown.length === 0 && <p className="ai-empty">{f.onlyMissing ? "미등록 컷이 없어요 🎉" : "대상 컷이 없어요"}</p>}
            {shown.map((r) => {
              const idx = rows.indexOf(r);
              return (
                <div key={idx} className="ai-row">
                  <span className="ai-code" onClick={() => (location.hash = `#/c/${encodeURIComponent(r.concept_id)}`)}>{r.code}</span>
                  <span className="ai-name" onClick={() => setOpen(idx)}>{r.name}</span>
                  <span className="ai-key">{r.key}</span>
                  <span className={r.ok ? "ai-ok" : "ai-no"}>{r.ok ? "O" : "X"}</span>
                </div>
              );
            })}
          </>
        )}
      </div>
      {open !== null && rows?.[open] && (
        <CutModal row={rows[open]} onClose={() => setOpen(null)}
          onChanged={(ok) => setRows((rs) => rs.map((r, i) => i === open ? { ...r, ok } : r))} />
      )}
    </div>
  );
}
