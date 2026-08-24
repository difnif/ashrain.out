// ashrain.out — 자료 전사 코퍼스 (AdminCorpus v3.0, 관리자 전용, #/admin/corpus)
// v3: 전사가 "서버 작업(job)"으로 — 시작만 하면 탭을 닫아도 계속 돌고, 재접속 시 자동 재개.
//     상단 고정 진행바 + 취소 3옵션(전체 취소 / 최근 10페이지 되돌리기 / 지금까지 저장).
//     썸네일은 저해상 고속 렌더, 고해상 렌더는 시작 시 선택 페이지만.
// 탭: ① 전사 실행 ② 코퍼스 열람 ③ 라우팅 현황

import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

const PDFJS = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
const PDFJS_WORKER = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
const JSZIP = "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";

function loadScript(src, ready) {
  return new Promise((ok, no) => {
    if (ready()) return ok(ready());
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => ok(ready());
    s.onerror = () => no(new Error("스크립트 로드 실패: " + src));
    document.head.appendChild(s);
  });
}
const loadPdfjs = async () => {
  const lib = await loadScript(PDFJS, () => window.pdfjsLib);
  lib.GlobalWorkerOptions.workerSrc = PDFJS_WORKER;
  return lib;
};
const loadJszip = () => loadScript(JSZIP, () => window.JSZip);

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
      : ext === "png" ? "image/png"
      : ext === "webp" ? "image/webp" : null;
    if (!type) continue;
    const blob = await f.async("blob");
    out.push(new File([blob], name.split("/").pop(), { type }));
  }
  return out;
}

async function renderPdfPage(pg, width, q) {
  const vp0 = pg.getViewport({ scale: 1 });
  const vp = pg.getViewport({ scale: Math.min(2.2, width / vp0.width) });
  const cv = document.createElement("canvas");
  cv.width = vp.width; cv.height = vp.height;
  await pg.render({ canvasContext: cv.getContext("2d"), viewport: vp }).promise;
  return cv.toDataURL("image/jpeg", q);
}
async function renderImgFile(file, width, q) {
  const img = new Image();
  const url = URL.createObjectURL(file);
  await new Promise((ok) => { img.onload = ok; img.src = url; });
  const scale = Math.min(1, width / img.width);
  const cv = document.createElement("canvas");
  cv.width = img.width * scale; cv.height = img.height * scale;
  cv.getContext("2d").drawImage(img, 0, 0, cv.width, cv.height);
  URL.revokeObjectURL(url);
  return cv.toDataURL("image/jpeg", q);
}
const dataUrlToBlob = async (d) => (await fetch(d)).blob();
async function sha256(buf) {
  const h = await crypto.subtle.digest("SHA-256", buf);
  return [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export default function AdminCorpus() {
  const [me, setMe] = useState(null);
  const [tab, setTab] = useState("run");
  const [units, setUnits] = useState([]);
  const [cmap, setCmap] = useState({});
  const [uncOnly, setUncOnly] = useState(false);
  const [arbMode, setArbMode] = useState("api");
  const [mFilter, setMFilter] = useState("all");
  const [mStats, setMStats] = useState(null);
  const impRef = useRef(null);

  // 준비 단계
  const [title, setTitle] = useState("");
  const [unit, setUnit] = useState("");
  const [pages, setPages] = useState([]);          // {page, thumb}
  const [sel, setSel] = useState(new Set());
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState([]);
  const [drag, setDrag] = useState(false);
  const fileRef = useRef(null);
  const srcRef = useRef([]);                        // page → {kind:'pdf',doc,idx} | {kind:'img',file}
  const origRef = useRef(null);

  // 진행 중 작업
  const [job, setJob] = useState(null);             // transcribe_jobs 행
  const [prog, setProg] = useState(null);           // {done,err,pending,total,saved,arb}
  const [cancelUi, setCancelUi] = useState(false);
  const pollRef = useRef(null);

  // 코퍼스·라우팅
  const [cUnit, setCUnit] = useState("all");
  const [corpus, setCorpus] = useState([]);
  const [routing, setRouting] = useState([]);
  const [openItem, setOpenItem] = useState(null);

  const say = (m) => setLog((l) => [...l.slice(-30), m]);

  useEffect(() => { (async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) { setMe("no"); return; }
    const { data: p } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    setMe(p?.role === "admin" ? "admin" : "no");
    const { data: cs } = await supabase.from("concepts").select("id,unit_id,title");
    setUnits([...new Set((cs || []).map((c) => c.unit_id))].sort());
    setCmap(Object.fromEntries((cs || []).map((c) => [c.id, c.title])));
    // 돌고 있던 작업 자동 재개
    const { data: j } = await supabase.from("transcribe_jobs").select("*")
      .eq("status", "running").order("created_at", { ascending: false }).limit(1);
    if (j?.length) setJob(j[0]);
  })(); }, []);

  // ---- 진행 폴링 + 워치독 (체인 끊기면 재점화)
  useEffect(() => {
    if (!job) { clearInterval(pollRef.current); setProg(null); return; }
    const tick = async () => {
      const { data: jrow } = await supabase.from("transcribe_jobs").select("*").eq("id", job.id).single();
      const { data: pgs } = await supabase.from("transcribe_job_pages")
        .select("status,saved,arbitrated,updated_at").eq("job_id", job.id);
      const agg = { done: 0, err: 0, pending: 0, doing: 0, total: pgs?.length || 0, saved: 0, arb: 0 };
      for (const p of pgs || []) {
        if (p.status === "done") agg.done++;
        else if (p.status === "error") agg.err++;
        else if (p.status === "pending") agg.pending++;
        else if (p.status === "doing") agg.doing++;
        agg.saved += p.saved || 0; agg.arb += p.arbitrated || 0;
      }
      setProg(agg);
      if (jrow) setJob(jrow);
      if (jrow?.status === "running" && (agg.pending > 0 || agg.doing > 0)) {
        const stale = Date.now() - new Date(jrow.updated_at).getTime() > 25000;
        if (stale) kick(job.id);                    // 워치독
      }
    };
    tick();
    pollRef.current = setInterval(tick, 2500);
    return () => clearInterval(pollRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [job?.id, job?.status]);

  async function kick(jobId) {
    const { data: { session } } = await supabase.auth.getSession();
    fetch("/api/transcribeJob", {
      method: "POST",
      headers: { "content-type": "application/json", Authorization: `Bearer ${session.access_token}` },
      body: JSON.stringify({ job_id: jobId }),
    }).catch(() => {});
  }

  // ---- 파일 열기 (버튼·드롭 공용) — 저해상 썸네일 고속 렌더
  async function onFile(e) { await handleFiles(e.target.files); e.target.value = ""; }
  async function handleFiles(f) {
    if (!f?.length) return;
    setBusy(true); say("파일 여는 중…");
    try {
      let files = [];
      for (const file of f) {
        if (/\.zip$/i.test(file.name)) {
          const inner = await unpackZip(file);
          say(`zip 해제 — ${inner.length}개 파일`);
          files = [...files, ...inner];
        } else files.push(file);
      }
      const src = [], thumbs = [];
      for (const file of files) {
        const buf = await file.arrayBuffer();
        const fh = await sha256(buf);
        if (file.type === "application/pdf") {
          const lib = await loadPdfjs();
          const doc = await lib.getDocument({ data: buf.slice(0) }).promise;
          for (let i = 1; i <= Math.min(doc.numPages, 60); i++) {
            const pg = await doc.getPage(i);
            thumbs.push(await renderPdfPage(pg, 340, 0.6));
            src.push({ kind: "pdf", doc, idx: i, key: fh + ":" + i });
          }
        } else {
          thumbs.push(await renderImgFile(file, 340, 0.6));
          src.push({ kind: "img", file, key: fh + ":1" });
        }
      }
      // 이미 전사 완료된 페이지 조회 (지문 대조)
      const keys = src.map((x) => x.key);
      const doneSet = new Set();
      for (let i = 0; i < keys.length; i += 100) {
        const { data: dp } = await supabase.from("transcribe_job_pages")
          .select("page_key").in("page_key", keys.slice(i, i + 100)).eq("status", "done");
        (dp || []).forEach((r) => doneSet.add(r.page_key));
      }
      srcRef.current = src;
      origRef.current = files[0] || null;
      if (!title && files[0]) setTitle(files[0].name.replace(/\.\w+$/, ""));
      setPages(thumbs.map((t, i) => ({ page: i + 1, thumb: t, done: doneSet.has(src[i].key) })));
      setSel(new Set(thumbs.map((_, i) => i + 1).filter((p) => !doneSet.has(src[p - 1].key))));
      const dn = [...doneSet].length;
      say(`${thumbs.length}페이지 준비됨${dn ? ` — 이미 전사된 ${dn}페이지는 자동 제외 (배지 표시, 클릭하면 재전사 가능)` : " — 전사할 페이지를 선택해"}`);
    } catch (err) { say("실패: " + err.message); }
    setBusy(false);
  }

  // ---- 작업 시작: 선택 페이지만 고해상 렌더 → Storage 업로드 → job 생성 → 러너 점화 2개
  async function start() {
    const picked = pages.filter((p) => sel.has(p.page));
    if (!picked.length) return;
    setBusy(true);
    try {
      let storage_path = null;
      if (origRef.current) {
        storage_path = `docs/${Date.now()}_${origRef.current.name.replace(/[^\w.\-]/g, "_")}`;
        await supabase.storage.from("corpus").upload(storage_path, origRef.current).catch(() => (storage_path = null));
      }
      const { data: doc, error: de } = await supabase.from("corpus_docs")
        .insert({ title: title || "무제", unit_hint: unit || null, storage_path, pages: pages.length }).select().single();
      if (de) throw de;
      const { data: jb, error: je } = await supabase.from("transcribe_jobs")
        .insert({ doc_id: doc.id, title: title || "무제", unit_hint: unit || null, total_pages: picked.length, arb_mode: arbMode }).select().single();
      if (je) throw je;

      const rows = [];
      for (let i = 0; i < picked.length; i++) {
        const p = picked[i];
        say(`p.${p.page} 준비 ${i + 1}/${picked.length}…`);
        const s = srcRef.current[p.page - 1];
        const full = s.kind === "pdf"
          ? await renderPdfPage(await s.doc.getPage(s.idx), 1300, 0.82)
          : await renderImgFile(s.file, 1400, 0.82);
        const path = `jobs/${jb.id}/p${p.page}.jpg`;
        const { error: ue } = await supabase.storage.from("corpus").upload(path, await dataUrlToBlob(full), { contentType: "image/jpeg" });
        if (ue) throw ue;
        rows.push({ job_id: jb.id, page: p.page, storage_path: path, page_key: srcRef.current[p.page - 1]?.key || null });
      }
      await supabase.from("transcribe_job_pages").insert(rows);
      kick(jb.id); kick(jb.id);                     // 병렬 러너 2개
      setJob(jb);
      setPages([]); setSel(new Set()); srcRef.current = []; origRef.current = null; setTitle("");
      say("작업 시작 — 탭을 닫아도 계속 진행됩니다.");
    } catch (err) { say("시작 실패: " + String(err.message || err)); }
    setBusy(false);
  }

  // ---- 취소 3옵션
  async function cancelAll() {
    if (!job) return;
    await supabase.from("transcribe_jobs").update({ status: "cancelled" }).eq("id", job.id);
    if (job.doc_id) {
      const { data: d } = await supabase.from("corpus_docs").select("storage_path").eq("id", job.doc_id).single();
      await supabase.from("transcribe_runs").delete().eq("doc_id", job.doc_id);
      await supabase.from("corpus_docs").delete().eq("id", job.doc_id);  // corpus_items는 cascade 삭제
      if (d?.storage_path) await supabase.storage.from("corpus").remove([d.storage_path]);
    }
    await supabase.from("transcribe_job_pages").update({ status: "skipped" }).eq("job_id", job.id).neq("status", "skipped");
    setCancelUi(false); setJob(null); say("전체 취소 — 이 작업의 저장분을 모두 삭제했습니다.");
  }
  async function cancelKeepBefore(n = 10) {
    if (!job) return;
    const { data: done } = await supabase.from("transcribe_job_pages")
      .select("page").eq("job_id", job.id).eq("status", "done").order("page", { ascending: false }).limit(n);
    const back = (done || []).map((x) => x.page);
    if (back.length && job.doc_id) {
      await supabase.from("corpus_items").delete().eq("doc_id", job.doc_id).in("page", back);
      await supabase.from("transcribe_job_pages").update({ status: "skipped" }).eq("job_id", job.id).in("page", back);
    }
    await supabase.from("transcribe_job_pages").update({ status: "skipped" }).eq("job_id", job.id).in("status", ["pending"]);
    await supabase.from("transcribe_jobs").update({ status: "stopped" }).eq("id", job.id);
    setCancelUi(false); setJob(null);
    say(`중단 — 최근 ${back.length}페이지 저장분을 되돌리고, 그 이전까지만 남겼습니다.`);
  }
  async function cancelKeepAll() {
    if (!job) return;
    await supabase.from("transcribe_job_pages").update({ status: "skipped" }).eq("job_id", job.id).in("status", ["pending"]);
    await supabase.from("transcribe_jobs").update({ status: "stopped" }).eq("id", job.id);
    setCancelUi(false); setJob(null); say("중단 — 지금까지 작업분은 저장했습니다.");
  }

  async function loadCorpus() {
    let q = supabase.from("corpus_items").select("*").order("created_at", { ascending: false }).limit(100);
    if (cUnit !== "all") q = q.eq("unit_id", cUnit);
    if (uncOnly) q = q.or("confidence.lt.0.7,concept_main.is.null");
    if (mFilter === "esc") q = q.eq("status", "escalated");
    else if (mFilter !== "all") q = q.eq("model_final", mFilter);
    const { data } = await q;
    setCorpus(data || []);
    const cnt = async (f) => (await f(supabase.from("corpus_items").select("id", { count: "exact", head: true }))).count || 0;
    setMStats({
      haiku: await cnt((x) => x.eq("model_final", "haiku")),
      sonnet: await cnt((x) => x.eq("model_final", "sonnet")),
      opus: await cnt((x) => x.eq("model_final", "opus")),
      fable: await cnt((x) => x.eq("model_final", "fable-chat")),
      esc: await cnt((x) => x.eq("status", "escalated")),
    });
  }
  async function exportEsc() {
    setBusy(true); say("대기 문항 내보내기 준비…");
    try {
      const { data: rows } = await supabase.from("corpus_items").select("id,doc_id,page,seq,question,choices,drafts,unit_id")
        .eq("status", "escalated").order("doc_id").order("page").limit(400);
      if (!rows?.length) { say("대기 문항 없음"); setBusy(false); return; }
      const JSZip = await loadJszip();
      const zip = new JSZip();
      const pages = [...new Set(rows.map((r) => `${r.doc_id}|${r.page}`))].slice(0, 40);
      const pageSet = new Set(pages);
      const use = rows.filter((r) => pageSet.has(`${r.doc_id}|${r.page}`));
      for (const pk of pages) {
        const [d, p] = pk.split("|");
        const { data: blob } = await supabase.storage.from("corpus").download(`esc/${d}/p${p}.jpg`);
        if (blob) zip.file(`images/${d.slice(0, 8)}_p${p}.jpg`, blob);
      }
      zip.file("tasks.json", JSON.stringify({
        instructions: "각 항목의 image를 보고 seq 문항을 최종 전사·분류하라. draft_a/draft_b와 diff를 참고하되 이미지가 근거다. 출력은 [{id, final:{seq,qtype,question,choices,answer,difficulty_est,has_math,has_figure,figure,unit_id,concept_main,concept_subs,pattern_tags,confidence}}] JSON 배열만.",
        items: use.map((r) => ({ id: r.id, image: `images/${String(r.doc_id).slice(0, 8)}_p${r.page}.jpg`, seq: r.seq, unit_id: r.unit_id, diff: r.drafts?.diff || [], draft_a: r.drafts?.a || null, draft_b: r.drafts?.b || null })),
      }, null, 1));
      const blob = await zip.generateAsync({ type: "blob" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `escalation_${Date.now()}.zip`;
      a.click(); URL.revokeObjectURL(a.href);
      say(`내보내기 완료 — 문항 ${use.length} · 페이지 ${pages.length}${rows.length > use.length ? " (남은 분량은 반영 후 다시 내보내기)" : ""}`);
    } catch (e) { say("내보내기 실패: " + String(e.message || e)); }
    setBusy(false);
  }

  async function importFinal(e) {
    const f = e.target.files?.[0]; e.target.value = "";
    if (!f) return;
    setBusy(true);
    let ok = 0, dup = 0, skip = 0;
    try {
      const arr = JSON.parse(await f.text());
      const list = Array.isArray(arr) ? arr : arr.items || [];
      for (const row of list) {
        if (!row?.id || !row?.final) { skip++; continue; }
        const fi = row.final;
        const cm = fi.concept_main && cmap[fi.concept_main] !== undefined ? fi.concept_main : fi.concept_main || null;
        const upd = {
          qtype: fi.qtype || "short", question: fi.question || "",
          choices: fi.choices || null, answer: fi.answer ?? null,
          difficulty_est: fi.difficulty_est ?? null,
          has_math: !!fi.has_math, has_figure: !!fi.has_figure, figure: fi.figure || null,
          unit_id: (String(fi.unit_id || "").match(/^[mh]\d-\d/) || [null])[0],
          concept_main: cm, concept_subs: (fi.concept_subs || []).slice(0, 2),
          concept_ids: [cm, ...(fi.concept_subs || [])].filter(Boolean),
          pattern_tags: (fi.pattern_tags || []).slice(0, 3),
          confidence: fi.confidence ?? null,
          status: "active", model_final: "fable-chat", drafts: null, agree: true,
        };
        const { error } = await supabase.from("corpus_items").update(upd).eq("id", row.id);
        if (error) {
          if (/duplicate|unique/i.test(error.message)) { await supabase.from("corpus_items").delete().eq("id", row.id); dup++; }
          else skip++;
        } else ok++;
      }
      say(`전사 반영 — 적용 ${ok} · 중복 병합 ${dup} · 무시 ${skip}`);
      loadCorpus();
    } catch (err) { say("반영 실패: " + String(err.message || err)); }
    setBusy(false);
  }

  async function loadRouting() {
    const { data } = await supabase.from("transcribe_routing").select("*").order("cluster_key");
    setRouting(data || []);
  }
  useEffect(() => { if (me === "admin" && tab === "browse") loadCorpus(); },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, tab, cUnit, uncOnly, mFilter]);
  useEffect(() => { if (me === "admin" && tab === "route") loadRouting(); },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, tab]);

  if (me === null) return <div className="cp-wrap">확인 중…</div>;
  if (me === "no") return <div className="cp-wrap">관리자 전용 페이지입니다.</div>;

  const pct = prog?.total ? Math.round(((prog.done + prog.err) / prog.total) * 100) : 0;
  const jobDone = job && job.status !== "running";

  return (
    <div className="cp-wrap">
      <style>{CSS}</style>

      {job && (
        <div className={"cp-jobbar" + (jobDone ? " fin" : "")}>
          <div className="cp-jobline">
            <b>{jobDone ? (job.status === "done" ? "전사 완료" : "중단됨") : "전사 중"}</b>
            <span> — {job.title} · {prog ? `${prog.done + prog.err}/${prog.total}p` : "…"}
              {prog ? ` · 문항 ${prog.saved} · 중재 ${prog.arb}` : ""}{prog?.err ? ` · 오류 ${prog.err}p` : ""}</span>
            <span className="cp-jobsp" />
            {!jobDone && <button className="cp-btn danger sm" onClick={() => setCancelUi(true)}>취소</button>}
            {jobDone && <button className="cp-btn sm" onClick={() => setJob(null)}>닫기</button>}
          </div>
          <div className="cp-bar"><div className="cp-barfill" style={{ width: pct + "%" }} /></div>
          {!jobDone && <p className="cp-note">탭을 닫거나 새로고침해도 서버에서 계속 진행됩니다 — 다시 열면 이 자리에서 이어집니다.</p>}
        </div>
      )}

      {cancelUi && (
        <div className="cp-modal" onClick={() => setCancelUi(false)}>
          <div className="cp-mbox" onClick={(e) => e.stopPropagation()}>
            <p className="cp-mtitle">전사를 어떻게 취소할까요?</p>
            <button className="cp-btn danger w" onClick={cancelAll}>전체 취소 — 이 작업의 저장분 모두 삭제</button>
            <button className="cp-btn w" onClick={() => cancelKeepBefore(10)}>최근 10페이지 되돌리고 중단 — 그 이전까지만 저장</button>
            <button className="cp-btn go w" onClick={cancelKeepAll}>지금까지 작업분 저장하고 중단</button>
            <button className="cp-btn w" onClick={() => setCancelUi(false)}>계속 진행 (닫기)</button>
          </div>
        </div>
      )}

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
                <option value="">단원 힌트 (선택)</option>
                {units.map((u) => <option key={u} value={u}>{u}</option>)}
              </select>
              <select className="cp-in" value={arbMode} onChange={(e) => setArbMode(e.target.value)}>
                <option value="api">중재: API 자동(오푸스)</option>
                <option value="queue">중재: 수동 큐(구독 크레딧)</option>
              </select>
              <button className="cp-btn" onClick={() => fileRef.current?.click()} disabled={busy}>PDF/이미지/zip 열기</button>
              <input ref={fileRef} type="file" accept="application/pdf,image/*,.zip" multiple hidden onChange={onFile} />
            </div>
            <p className="cp-note">파일을 이 상자에 끌어다 놔도 됨. 단원·개념은 자동 분류 — 힌트를 주면 정확도·속도가 조금 오름. 원문은 유형 참고 전용(서비스 노출·복제 금지).</p>
          </div>

          {pages.length > 0 && (
            <div className="cp-card">
              <div className="cp-row" style={{ justifyContent: "space-between" }}>
                <b>페이지 선택 ({sel.size}/{pages.length})</b>
                <span>
                  <button className="cp-btn sm" onClick={() => setSel(new Set(pages.map((p) => p.page)))}>전체</button>
                  <button className="cp-btn sm" onClick={() => setSel(new Set())}>해제</button>
                  <button className="cp-btn go" disabled={busy || !sel.size || !!(job && !jobDone)} onClick={start}>전사 시작</button>
                </span>
              </div>
              <div className="cp-grid">
                {pages.map((p) => (
                  <div key={p.page} className={"cp-thumb" + (sel.has(p.page) ? " on" : "")}
                    onClick={() => setSel((s) => { const n = new Set(s); n.has(p.page) ? n.delete(p.page) : n.add(p.page); return n; })}>
                    <img src={p.thumb} alt={"p" + p.page} />
                    <span>p.{p.page}</span>
                    {p.done && <em className="cp-done">전사됨</em>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {log.length > 0 && <div className="cp-log">{log.slice(-8).map((l, i) => <p key={i}>{l}</p>)}</div>}
          {job && <p className="cp-note">전사된 문항은 <b>② 코퍼스</b> 탭에서 실시간으로 확인할 수 있어.</p>}
        </>
      )}

      {tab === "browse" && (
        <>
          <div className="cp-row">
            <select className="cp-in" value={cUnit} onChange={(e) => setCUnit(e.target.value)}>
              <option value="all">단원 전체</option>
              {units.map((u) => <option key={u} value={u}>{u}</option>)}
            </select>
            <button className={"cp-tab" + (uncOnly ? " on" : "")} onClick={() => setUncOnly(!uncOnly)}>분류불확실만</button>
            <span className="cp-note">{corpus.length}건 (최근 100)</span>
          </div>
          <div className="cp-row">
            {[["all", "전체"], ["haiku", "하이쿠"], ["sonnet", "소넷"], ["opus", "오푸스"], ["fable-chat", "페이블"], ["esc", "상위 대기"]].map(([k, l]) => (
              <button key={k} className={"cp-tab" + (mFilter === k ? " on" : "")} onClick={() => setMFilter(k)}>
                {l}{mStats ? ` ${k === "all" ? "" : k === "esc" ? mStats.esc : k === "fable-chat" ? mStats.fable : mStats[k] ?? ""}` : ""}
              </button>
            ))}
            {mStats?.esc > 0 && <button className="cp-btn" onClick={exportEsc} disabled={busy}>대기 내보내기(zip)</button>}
            <button className="cp-btn" onClick={() => impRef.current?.click()} disabled={busy}>전사 반영(JSON)</button>
            <input ref={impRef} type="file" accept="application/json,.json" hidden onChange={importFinal} />
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
              <p className="cp-meta">
                <b>{it.unit_id || "?"}</b> · {it.concept_main ? `${it.concept_main} ${cmap[it.concept_main] || ""}` : "미분류"}
                {(it.pattern_tags || []).length ? " · " + it.pattern_tags.join("/") : ""} · {it.qtype} · d{it.difficulty_est ?? "?"}
                · {it.agree ? "일치" : it.model_final}
                {it.status === "escalated" && <span className="cp-warn">상위 대기</span>}
                {(it.confidence != null && it.confidence < 0.7) && <span className="cp-warn">분류불확실</span>}
              </p>
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
.cp-jobbar{position:sticky;top:0;z-index:30;background:#0f172a;color:#e2e8f0;border-radius:10px;padding:9px 12px;margin-bottom:12px}
.cp-jobbar.fin{background:#14532d}
.cp-jobline{display:flex;align-items:center;gap:6px;font-size:13px;flex-wrap:wrap}
.cp-jobsp{flex:1}
.cp-bar{height:6px;background:#334155;border-radius:99px;margin-top:7px;overflow:hidden}
.cp-barfill{height:100%;background:#22c55e;border-radius:99px;transition:width .5s}
.cp-jobbar .cp-note{color:#94a3b8;margin:6px 0 0}
.cp-modal{position:fixed;inset:0;background:#0008;z-index:50;display:flex;align-items:center;justify-content:center;padding:16px}
.cp-mbox{background:#fff;border-radius:12px;padding:16px;max-width:380px;width:100%}
.cp-mtitle{font-weight:800;font-size:14.5px;margin:0 0 10px}
.cp-btn.w{display:block;width:100%;margin:6px 0;text-align:left}
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
.cp-btn.danger{border-color:#dc2626;color:#dc2626;background:#fff}
.cp-btn:disabled{opacity:.45}
.cp-note{font-size:12px;color:#64748b;margin:6px 0 0}
.cp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin-top:10px}
.cp-thumb{border:2px solid #e2e8f0;border-radius:8px;overflow:hidden;cursor:pointer;position:relative}
.cp-thumb.on{border-color:#16a34a}
.cp-thumb img{width:100%;display:block}
.cp-thumb span{position:absolute;left:4px;bottom:4px;background:#0f172acc;color:#fff;font-size:11px;padding:1px 5px;border-radius:5px}
.cp-done{position:absolute;right:4px;top:4px;background:#16a34a;color:#fff;font-style:normal;font-size:10.5px;padding:1px 5px;border-radius:5px}
.cp-log{background:#0f172a;color:#e2e8f0;border-radius:8px;padding:8px 12px;font-size:12px;margin-bottom:10px}
.cp-log p{margin:2px 0}
.cp-item{border:1px solid #e2e8f0;border-radius:10px;padding:8px 12px;background:#fff;margin-bottom:6px;cursor:pointer}
.cp-q{margin:2px 0;font-size:13.5px;white-space:pre-line}
.cp-c{margin:1px 0 1px 8px;font-size:13px}
.cp-meta{margin:4px 0 0;font-size:11.5px;color:#94a3b8}
.cp-warn{display:inline-block;margin-left:6px;padding:0 5px;border-radius:5px;background:#fffbeb;border:1px solid #fcd34d;color:#b45309;font-size:10.5px}
.cp-tb{width:100%;border-collapse:collapse;font-size:12.5px}
.cp-tb th{background:#0f172a;color:#fff;padding:6px 8px;text-align:left}
.cp-tb td{border:1px solid #e2e8f0;padding:5px 8px}
`;
