// ashrain.out — 자료 전사 코퍼스 (AdminCorpus v1.0, 관리자 전용, #/admin/corpus)
// PDF·이미지 업로드 → 페이지 선택 → 이중 전사(하이쿠+소넷, 불일치는 상위 중재) → 자동 채택 적재.
// 탭: ① 전사 실행 ② 코퍼스 열람 ③ 라우팅 현황

import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

const PDFJS = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
const PDFJS_WORKER = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

function loadPdfjs() {
  return new Promise((ok, no) => {
    if (window.pdfjsLib) return ok(window.pdfjsLib);
    const s = document.createElement("script");
    s.src = PDFJS;
    s.onload = () => { window.pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER; ok(window.pdfjsLib); };
    s.onerror = () => no(new Error("pdf.js 로드 실패"));
    document.head.appendChild(s);
  });
}

const JSZIP = "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";

function loadJszip() {
  return new Promise((ok, no) => {
    if (window.JSZip) return ok(window.JSZip);
    const s = document.createElement("script");
    s.src = JSZIP;
    s.onload = () => ok(window.JSZip);
    s.onerror = () => no(new Error("JSZip 로드 실패"));
    document.head.appendChild(s);
  });
}

async function unpackZip(file) {
  const JSZip = await loadJszip();
  const zip = await JSZip.loadAsync(await file.arrayBuffer());
  const out = [];
  for (const name of Object.keys(zip.files)) {
    const f = zip.files[name];
    if (f.dir || name.startsWith("__MACOSX")) continue;
    const ext = name.split(".").pop().toLowerCase();
    const type = ext === "pdf" ? "application/pdf"
      : ["jpg", "jpeg"].includes(ext) ? "image/jpeg"
      : ["png"].includes(ext) ? "image/png"
      : ["webp"].includes(ext) ? "image/webp" : null;
    if (!type) continue;
    const blob = await f.async("blob");
    out.push(new File([blob], name.split("/").pop(), { type }));
  }
  return out;
}

async function fileToPages(file, max = 40) {
  if (file.type === "application/pdf") {
    const lib = await loadPdfjs();
    const buf = await file.arrayBuffer();
    const pdf = await lib.getDocument({ data: buf }).promise;
    const out = [];
    for (let i = 1; i <= Math.min(pdf.numPages, max); i++) {
      const pg = await pdf.getPage(i);
      const vp0 = pg.getViewport({ scale: 1 });
      const scale = Math.min(2.2, 1300 / vp0.width);
      const vp = pg.getViewport({ scale });
      const cv = document.createElement("canvas");
      cv.width = vp.width; cv.height = vp.height;
      await pg.render({ canvasContext: cv.getContext("2d"), viewport: vp }).promise;
      out.push({ page: i, image: cv.toDataURL("image/jpeg", 0.82) });
    }
    return out;
  }
  // 이미지 파일 1장 = 1페이지
  const img = new Image();
  const url = URL.createObjectURL(file);
  await new Promise((ok) => { img.onload = ok; img.src = url; });
  const scale = Math.min(1, 1400 / img.width);
  const cv = document.createElement("canvas");
  cv.width = img.width * scale; cv.height = img.height * scale;
  cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
  URL.revokeObjectURL(url);
  return [{ page: 0, image: cv.toDataURL("image/jpeg", 0.82) }];
}

export default function AdminCorpus() {
  const [me, setMe] = useState(null);
  const [tab, setTab] = useState("run");
  const [units, setUnits] = useState([]);

  // 전사 탭
  const [title, setTitle] = useState("");
  const [unit, setUnit] = useState("");
  const [pages, setPages] = useState([]);       // {page, image}
  const [sel, setSel] = useState(new Set());
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState([]);
  const [result, setResult] = useState([]);
  const fileRef = useRef(null);
  const origFile = useRef(null);

  // 코퍼스·라우팅 탭
  const [cUnit, setCUnit] = useState("all");
  const [corpus, setCorpus] = useState([]);
  const [routing, setRouting] = useState([]);
  const [openItem, setOpenItem] = useState(null);

  useEffect(() => { (async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) { setMe("no"); return; }
    const { data: p } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    setMe(p?.role === "admin" ? "admin" : "no");
    const { data: cs } = await supabase.from("concepts").select("unit_id");
    setUnits([...new Set((cs || []).map((c) => c.unit_id))].sort());
  })(); }, []);

  const [drag, setDrag] = useState(false);

  async function onFile(e) {
    await handleFiles(e.target.files);
    e.target.value = "";
  }

  async function handleFiles(f) {
    if (!f?.length) return;
    setBusy(true); setLog((l) => [...l, "페이지 렌더 중…"]);
    try {
      let files = [];
      for (const file of f) {
        if (/\.zip$/i.test(file.name)) {
          const inner = await unpackZip(file);
          setLog((l) => [...l, `zip 해제 — ${inner.length}개 파일`]);
          files = [...files, ...inner];
        } else files.push(file);
      }
      let all = [];
      for (const file of files) {
        const ps = await fileToPages(file);
        const base = all.length;
        all = [...all, ...ps.map((p, i) => ({ ...p, page: base + i + 1 }))];
      }
      origFile.current = files[0];
      if (!title) setTitle(files[0].name.replace(/\.\w+$/, ""));
      setPages(all); setSel(new Set(all.map((p) => p.page)));
      setLog((l) => [...l, `${all.length}페이지 준비됨 — 전사할 페이지를 선택해`]);
    } catch (err) { setLog((l) => [...l, "실패: " + err.message]); }
    setBusy(false);
  }

  async function run() {
    if (!unit) { setLog((l) => [...l, "단원을 먼저 선택해"]); return; }
    const picked = pages.filter((p) => sel.has(p.page));
    if (!picked.length) return;
    setBusy(true); setResult([]);
    try {
      const { data: { session } } = await supabase.auth.getSession();
      // 문서 등록 + 원본 보관
      let storage_path = null;
      if (origFile.current) {
        storage_path = `docs/${Date.now()}_${origFile.current.name.replace(/[^\w.\-]/g, "_")}`;
        await supabase.storage.from("corpus").upload(storage_path, origFile.current).catch(() => (storage_path = null));
      }
      const { data: doc, error: de } = await supabase.from("corpus_docs")
        .insert({ title: title || "무제", unit_hint: unit, storage_path, pages: pages.length }).select().single();
      if (de) throw de;

      let saved = 0, arb = 0;
      for (const p of picked) {
        setLog((l) => [...l, `p.${p.page} 전사 중…`]);
        const r = await fetch("/api/transcribeCorpus", {
          method: "POST",
          headers: { "content-type": "application/json", Authorization: `Bearer ${session.access_token}` },
          body: JSON.stringify({ doc_id: doc.id, page: p.page, image: p.image, unit_id: unit }),
        });
        const j = await r.json();
        if (!r.ok) { setLog((l) => [...l, `p.${p.page} 실패: ${j.error}`]); continue; }
        saved += j.saved; arb += j.arbitrated;
        setResult((rs) => [...rs, ...(j.items || [])]);
        setLog((l) => [...l, `p.${p.page} — ${j.saved}문항 (중재 ${j.arbitrated})`]);
      }
      setLog((l) => [...l, `완료 — 총 ${saved}문항 적재, 중재 ${arb}건`]);
    } catch (err) { setLog((l) => [...l, "실패: " + String(err.message || err)]); }
    setBusy(false);
  }

  async function loadCorpus() {
    let q = supabase.from("corpus_items").select("*").order("created_at", { ascending: false }).limit(100);
    if (cUnit !== "all") q = q.eq("unit_id", cUnit);
    const { data } = await q;
    setCorpus(data || []);
  }
  async function loadRouting() {
    const { data } = await supabase.from("transcribe_routing").select("*").order("cluster_key");
    setRouting(data || []);
  }
  useEffect(() => { if (me === "admin" && tab === "browse") loadCorpus(); },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, tab, cUnit]);
  useEffect(() => { if (me === "admin" && tab === "route") loadRouting(); },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, tab]);

  if (me === null) return <div className="cp-wrap">확인 중…</div>;
  if (me === "no") return <div className="cp-wrap">관리자 전용 페이지입니다.</div>;

  return (
    <div className="cp-wrap">
      <style>{CSS}</style>
      <h2>자료 전사 코퍼스</h2>
      <div className="cp-tabs">
        {[["run", "① 전사 실행"], ["browse", "② 코퍼스"], ["route", "③ 라우팅"]].map(([k, l]) => (
          <button key={k} className={"cp-tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>
        ))}
      </div>

      {tab === "run" && (
        <>
          <div className={"cp-card cp-drop" + (drag ? " on" : "")}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); handleFiles(e.dataTransfer.files); }}>
            <div className="cp-row">
              <input className="cp-in" placeholder="자료 제목" value={title} onChange={(e) => setTitle(e.target.value)} />
              <select className="cp-in" value={unit} onChange={(e) => setUnit(e.target.value)}>
                <option value="">단원 선택</option>
                {units.map((u) => <option key={u} value={u}>{u}</option>)}
              </select>
              <button className="cp-btn" onClick={() => fileRef.current?.click()} disabled={busy}>PDF/이미지 열기</button>
              <input ref={fileRef} type="file" accept="application/pdf,image/*,.zip" multiple hidden onChange={onFile} />
            </div>
            <p className="cp-note">파일을 이 상자에 끌어다 놔도 됨 (PDF·이미지·zip). 해당 단원 페이지만 골라 전사 — 원문은 유형 참고 전용(서비스 노출·복제 금지), 원본 파일은 corpus 버킷에 보관.</p>
          </div>

          {pages.length > 0 && (
            <div className="cp-card">
              <div className="cp-row" style={{ justifyContent: "space-between" }}>
                <b>페이지 선택 ({sel.size}/{pages.length})</b>
                <span>
                  <button className="cp-btn sm" onClick={() => setSel(new Set(pages.map((p) => p.page)))}>전체</button>
                  <button className="cp-btn sm" onClick={() => setSel(new Set())}>해제</button>
                  <button className="cp-btn go" disabled={busy || !sel.size} onClick={run}>선택 페이지 전사</button>
                </span>
              </div>
              <div className="cp-grid">
                {pages.map((p) => (
                  <div key={p.page} className={"cp-thumb" + (sel.has(p.page) ? " on" : "")}
                    onClick={() => setSel((s) => { const n = new Set(s); n.has(p.page) ? n.delete(p.page) : n.add(p.page); return n; })}>
                    <img src={p.image} alt={"p" + p.page} />
                    <span>p.{p.page}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {log.length > 0 && <div className="cp-log">{log.slice(-8).map((l, i) => <p key={i}>{l}</p>)}</div>}

          {result.map((it, i) => (
            <div key={i} className="cp-item">
              <p className="cp-q"><b>{it.seq}.</b> {it.question}</p>
              {(it.choices || []).map((c, j) => <p key={j} className="cp-c">{"①②③④⑤"[j] || "·"} {c}</p>)}
              <p className="cp-meta">{it.qtype} · d{it.difficulty_est ?? "?"} · {it.has_math ? "수식 " : ""}{it.has_figure ? "도형 " : ""}
                · {it.agree ? "일치" : "중재:" + it.model_final}{it.answer != null ? " · 답 " + it.answer : ""}</p>
            </div>
          ))}
        </>
      )}

      {tab === "browse" && (
        <>
          <div className="cp-row">
            <select className="cp-in" value={cUnit} onChange={(e) => setCUnit(e.target.value)}>
              <option value="all">단원 전체</option>
              {units.map((u) => <option key={u} value={u}>{u}</option>)}
            </select>
            <span className="cp-note">{corpus.length}건 (최근 100)</span>
          </div>
          {corpus.map((it) => (
            <div key={it.id} className="cp-item" onClick={() => setOpenItem(openItem === it.id ? null : it.id)}>
              <p className="cp-q">{it.question.split("\n")[0]}</p>
              {openItem === it.id && (
                <>
                  {(it.choices || []).map((c, j) => <p key={j} className="cp-c">{"①②③④⑤"[j] || "·"} {c}</p>)}
                  {it.figure && <p className="cp-meta">도형: {it.figure.kind} — {(it.figure.relations || []).join(" / ")}</p>}
                </>
              )}
              <p className="cp-meta">{it.unit_id} · {it.qtype} · d{it.difficulty_est ?? "?"} · {it.cluster_key} · {it.agree ? "일치" : it.model_final}</p>
            </div>
          ))}
        </>
      )}

      {tab === "route" && (
        <table className="cp-tb">
          <thead><tr><th>유형(cluster)</th><th>담당</th><th>상태</th><th>표본</th><th>일치율</th></tr></thead>
          <tbody>
            {routing.map((r) => (
              <tr key={r.cluster_key}>
                <td>{r.cluster_key}</td><td>{r.primary_model}</td><td>{r.state}</td>
                <td>{r.sample_n}</td>
                <td>{r.sample_n ? Math.round((r.agree_n / r.sample_n) * 100) + "%" : "-"}</td>
              </tr>
            ))}
            {!routing.length && <tr><td colSpan={5} style={{ textAlign: "center", color: "#94a3b8" }}>아직 데이터 없음</td></tr>}
          </tbody>
        </table>
      )}
    </div>
  );
}

const CSS = `
.cp-wrap{max-width:860px;margin:0 auto;padding:16px 14px 60px;color:#1e293b}
.cp-wrap h2{margin:6px 0 10px;font-size:20px}
.cp-tabs{display:flex;gap:6px;margin-bottom:10px}
.cp-tab{padding:6px 12px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;font-size:13px;cursor:pointer}
.cp-tab.on{background:#0f172a;color:#fff;border-color:#0f172a}
.cp-card{border:1px solid #e2e8f0;border-radius:10px;padding:10px 12px;background:#fff;margin-bottom:10px}
.cp-drop{border-style:dashed;border-width:2px;transition:border-color .15s, background .15s}
.cp-drop.on{border-color:#16a34a;background:#f0fdf4}
.cp-row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.cp-in{padding:7px 9px;border:1px solid #cbd5e1;border-radius:8px;font-size:13px;background:#fff}
.cp-btn{padding:7px 12px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;font-size:13px;cursor:pointer}
.cp-btn.sm{padding:4px 8px;font-size:12px;margin-right:4px}
.cp-btn.go{background:#16a34a;border-color:#16a34a;color:#fff}
.cp-btn:disabled{opacity:.45}
.cp-note{font-size:12px;color:#64748b;margin:6px 0 0}
.cp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin-top:10px}
.cp-thumb{border:2px solid #e2e8f0;border-radius:8px;overflow:hidden;cursor:pointer;position:relative}
.cp-thumb.on{border-color:#16a34a}
.cp-thumb img{width:100%;display:block}
.cp-thumb span{position:absolute;left:4px;bottom:4px;background:#0f172acc;color:#fff;font-size:11px;padding:1px 5px;border-radius:5px}
.cp-log{background:#0f172a;color:#e2e8f0;border-radius:8px;padding:8px 12px;font-size:12px;margin-bottom:10px}
.cp-log p{margin:2px 0}
.cp-item{border:1px solid #e2e8f0;border-radius:10px;padding:8px 12px;background:#fff;margin-bottom:6px;cursor:pointer}
.cp-q{margin:2px 0;font-size:13.5px;white-space:pre-line}
.cp-c{margin:1px 0 1px 8px;font-size:13px}
.cp-meta{margin:4px 0 0;font-size:11.5px;color:#94a3b8}
.cp-tb{width:100%;border-collapse:collapse;font-size:12.5px}
.cp-tb th{background:#0f172a;color:#fff;padding:6px 8px;text-align:left}
.cp-tb td{border:1px solid #e2e8f0;padding:5px 8px}
`;
