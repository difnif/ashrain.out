// ashrain.out — 자료 전사 코퍼스 (AdminCorpus v3.14.1, 관리자 전용, #/admin/corpus)
// v3: 전사가 "서버 작업(job)"으로 — 시작만 하면 탭을 닫아도 계속 돌고, 재접속 시 자동 재개.
//     상단 고정 진행바 + 취소 3옵션(전체 취소 / 최근 10페이지 되돌리기 / 지금까지 저장).
//     썸네일은 저해상 고속 렌더, 고해상 렌더는 시작 시 선택 페이지만.
// v3.13: [대기 원본 내보내기] v2 — (모델 티어, 단원)별로 80쪽씩 zip 분할, 파일명 앞에 실패 모델 접두사
//        (사다리 규칙 복원: p_correct<45=오푸스까지 실패, 그 외=소넷까지 실패), T0-중복 제외,
//        manifest.json(id·doc·쪽·seq·유형·처방·p_correct·초안·빠른정답·출력 규격) 동봉.
//        전사 반영(JSON) 시 esc_triage='T1-재전사-chat' 표식.
// v3.14: 대기 원본 내보내기 v3 — 모델×단원 체크 선택, [선택 전부 받기](zip 연속 자동 다운로드) / [하나만 받기],
//        이미지 8병렬 다운로드(청크당 소요 1/6), 중단 버튼, 진행 표시.
// v3.14.1: 단원 칩 수치가 체크된 티어만 반영하도록 수정 (내려받는 내용물은 원래 정확 — 라벨만 오류였음).
// 탭: ① 전사 실행 ② 코퍼스 열람 ③ 라우팅 현황 ④ 모니터

import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { renderText } from "../lib/mathir";

const rt = (s) => { try { return renderText(String(s ?? "")); } catch { return String(s ?? ""); } };

const PDFJS = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js";
const PDFJS_WORKER = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
const JSZIP = "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";
const CHAINS = 4;   // 작업당 병렬 러너 수
const ESC_CHUNK = 80;   // 대기 원본 zip 하나당 쪽수 (≈20MB, 업로드 한도 안)
const OPUS_GATE = 45;   // 사다리 오푸스 게이트 — 이 아래면 오푸스 중재까지 거친 것
const safeName = (s) => String(s || "").replace(/[\\/:*?"<>|]/g, "_").replace(/\s+/g, " ").trim().slice(0, 60);

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
  const [runnerSel, setRunnerSel] = useState("cloud");
  const [workerState, setWorkerState] = useState(null);
  const [mon, setMon] = useState(null);
  const [budget, setBudget] = useState(() => Number(localStorage.getItem("cp_budget") || 300000));
  const alertsRef = useRef({});
  const [mFilter, setMFilter] = useState("all");
  const [mStats, setMStats] = useState(null);
  const impRef = useRef(null);

  // 대기 원본 내보내기 v3 (모델×단원 체크 → 연속 다운로드)
  const [escPlan, setEscPlan] = useState(null);        // {items, chunks:[{tier,unit,idx,of,pages:[{pk,items}]}], units:[]}
  const [escTiers, setEscTiers] = useState(new Set(["sonnet", "opus"]));
  const [escUnits, setEscUnits] = useState(new Set());
  const [escOne, setEscOne] = useState(0);             // 하나만 받기 — chunks 인덱스
  const [escRun, setEscRun] = useState(null);          // {i, n, name} 진행 중
  const escStopRef = useRef(false);

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
  const [queueN, setQueueN] = useState(0);          // 대기 중인 다른 작업 수
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
    const { data: wc } = await supabase.from("worker_control").select("state").eq("id", 1).maybeSingle();
    if (wc) setWorkerState(wc.state);
    // 돌고 있던 작업 자동 재개
    const { data: j } = await supabase.from("transcribe_jobs").select("*")
      .eq("status", "running").order("created_at", { ascending: true }).limit(1);
    if (j?.length) { setJob(j[0]); kick(j[0].id); }
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
      const { count: qn } = await supabase.from("transcribe_jobs")
        .select("id", { count: "exact", head: true }).eq("status", "running").neq("id", job.id);
      setQueueN(qn || 0);
      if (jrow && jrow.status !== "running") {
        // 현재 작업 종료 → 가장 오래된 다음 running 작업으로 자동 승계
        const { data: nx } = await supabase.from("transcribe_jobs").select("*")
          .eq("status", "running").order("created_at", { ascending: true }).limit(1);
        if (nx?.length) { say(`다음 작업 자동 시작 — ${nx[0].title}`); setJob(nx[0]); kick(nx[0].id); return; }
        setJob(jrow);
        return;
      }
      if (jrow) setJob(jrow);
      if (jrow?.status === "running") {
        const stale = Date.now() - new Date(jrow.updated_at).getTime() > 25000;
        if (stale) kick(job.id);                    // 워치독 (로컬 작업의 분류·마감 점화 겸용)
      }
    };
    tick();
    pollRef.current = setInterval(tick, 2500);
    return () => clearInterval(pollRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [job?.id, job?.status]);

  async function kick(jobId) {
    const { data: { session } } = await supabase.auth.getSession();
    for (let k = 0; k < CHAINS; k++)
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
        .insert({ doc_id: doc.id, title: title || "무제", unit_hint: unit || null, total_pages: picked.length, arb_mode: arbMode, runner: runnerSel }).select().single();
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
      if (runnerSel === "cloud") kick(jb.id);   // 병렬 CHAINS개 (로컬은 집 PC 워커가 집어감)
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
    else if (mFilter === "legacy") q = q.eq("status", "legacy");
    else { q = q.neq("status", "legacy"); if (mFilter !== "all") q = q.eq("model_final", mFilter); }
    const { data } = await q;
    setCorpus(data || []);
    const cnt = async (f) => (await f(supabase.from("corpus_items").select("id", { count: "exact", head: true }))).count || 0;
    setMStats({
      haiku: await cnt((x) => x.eq("model_final", "haiku")),
      sonnet: await cnt((x) => x.eq("model_final", "sonnet")),
      opus: await cnt((x) => x.eq("model_final", "opus")),
      fable: await cnt((x) => x.eq("model_final", "fable-chat")),
      esc: await cnt((x) => x.eq("status", "escalated")),
      legacy: await cnt((x) => x.eq("status", "legacy")),
    });
  }

  // ---- 대기 원본 내보내기 v3: 전량 계획 → 모델×단원 체크 → 선택 청크 연속 zip (이미지 8병렬)
  const tierOf = (r) => (r.p_correct != null && Number(r.p_correct) < OPUS_GATE ? "opus" : "sonnet");
  async function pmap(list, n, fn) {
    const out = new Array(list.length); let i = 0;
    await Promise.all(Array.from({ length: Math.min(n, list.length) }, async () => {
      while (i < list.length) { const k = i++; out[k] = await fn(list[k], k); }
    }));
    return out;
  }
  async function planEsc() {
    setBusy(true); say("대기 원본 계획 수집 중…");
    try {
      const rows = [];
      for (let i = 0; ; i += 1000) {
        const { data, error } = await supabase.from("corpus_items")
          .select("id,doc_id,page,seq,unit_id,src_tags,esc_triage,p_correct,drafts")
          .eq("status", "escalated").order("doc_id").order("page").order("seq").range(i, i + 999);
        if (error) throw new Error(error.message);
        rows.push(...(data || []));
        if (!data || data.length < 1000) break;
      }
      const use = rows.filter((r) => !String(r.esc_triage || "").startsWith("T0"));
      const groups = {};
      for (const r of use) {
        const gk = `${tierOf(r)}|${r.unit_id || "x"}`;
        const pk = `${r.doc_id}|${r.page}`;
        (groups[gk] ||= {});
        (groups[gk][pk] ||= []).push(r);
      }
      const chunks = [];
      for (const gk of Object.keys(groups).sort()) {
        const [tier, unit] = gk.split("|");
        const pks = Object.keys(groups[gk]).sort((a, b) => {
          const [da, pa] = a.split("|"), [db, pb] = b.split("|");
          return da < db ? -1 : da > db ? 1 : Number(pa) - Number(pb);
        });
        const of = Math.ceil(pks.length / ESC_CHUNK);
        for (let c = 0; c < of; c++)
          chunks.push({ tier, unit, idx: c + 1, of,
            pages: pks.slice(c * ESC_CHUNK, (c + 1) * ESC_CHUNK).map((pk) => ({ pk, items: groups[gk][pk] })) });
      }
      const unitList = [...new Set(chunks.map((c) => c.unit))].sort((a, b) => (a[0] === b[0] ? a.localeCompare(b) : a[0] === "m" ? -1 : 1));
      setEscPlan({ items: use.length, chunks, units: unitList });
      setEscUnits(new Set(unitList)); setEscOne(0);
      say(`계획 — 문항 ${use.length} · 쪽 ${chunks.reduce((a, c) => a + c.pages.length, 0)} · zip ${chunks.length}개. 아래에서 모델·단원 체크 후 받기`);
    } catch (e) { say("계획 실패: " + String(e.message || e)); }
    setBusy(false);
  }
  const escSelected = () => (escPlan?.chunks || []).filter((c) => escTiers.has(c.tier) && escUnits.has(c.unit));
  const escStat = (unit, tier) => {
    const cs = (escPlan?.chunks || []).filter((c) => c.unit === unit && c.tier === tier);
    return cs.length ? `${cs.reduce((a, c) => a + c.pages.length, 0)}쪽·${cs.length}zip` : "-";
  };
  async function buildEscZip(ch) {
    const JSZip = await loadJszip();
    const zip = new JSZip();
    const docIds = [...new Set(ch.pages.map((p) => p.pk.split("|")[0]))];
    const docs = {};
    for (let i = 0; i < docIds.length; i += 100) {
      const { data } = await supabase.from("corpus_docs").select("id,title,answers").in("id", docIds.slice(i, i + 100));
      (data || []).forEach((d) => { docs[d.id] = d; });
    }
    let missing = 0;
    const fnameOf = (d, p) => `${ch.tier}_${ch.unit}_${safeName(docs[d]?.title || d.slice(0, 8))}_p${p}.jpg`;
    await pmap(ch.pages, 8, async ({ pk }) => {
      const [d, p] = pk.split("|");
      const { data: blob, error } = await supabase.storage.from("corpus").download(`esc/${d}/p${p}.jpg`);
      if (blob && !error) zip.file(`images/${fnameOf(d, p)}`, blob); else missing++;
    });
    const manifest = [];
    for (const { pk, items } of ch.pages) {
      const [d, p] = pk.split("|");
      for (const r of items) manifest.push({
        id: r.id, image: `images/${fnameOf(d, p)}`, doc_id: d, doc_title: docs[d]?.title || null,
        page: Number(p), seq: r.seq, unit_id: r.unit_id, src_tag: r.src_tags?.[0] || null,
        esc_triage: r.esc_triage || null, p_correct: r.p_correct ?? null, tier: ch.tier,
        diff: r.drafts?.diff || [], draft_a: r.drafts?.a || null,
        quick_answer: docs[d]?.answers?.[String(r.seq)] ?? null,
      });
    }
    zip.file("manifest.json", JSON.stringify({
      exported_at: new Date().toISOString(),
      chunk: { tier: ch.tier, unit: ch.unit, idx: ch.idx, of: ch.of, pages: ch.pages.length, items: manifest.length, missing_images: missing },
      instructions: "각 항목의 image(쪽당 문항 1개)를 보고 seq 문항을 mathir 문법(첨부 mathir.py v1.4 기준)으로 최종 전사하라. draft_a·diff는 참고만, 이미지가 근거. quick_answer는 자료의 빠른정답(있으면 대입 검산). 출력은 전사 반영(JSON) 형식: [{id, final:{seq,qtype,question,choices,answer,difficulty_est,has_math,has_figure,figure,unit_id,concept_main,concept_subs,pattern_tags,confidence}}] JSON 배열만.",
      items: manifest,
    }, null, 1));
    const blob = await zip.generateAsync({ type: "blob" });
    return { blob, name: `esc_${ch.tier}_${ch.unit}_${ch.idx}of${ch.of}.zip`, items: manifest.length, missing };
  }
  const saveBlob = (blob, name) => {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 30000);
  };
  async function exportEscMany(list) {
    if (!list.length) { say("선택된 zip 없음"); return; }
    setBusy(true); escStopRef.current = false;
    let done = 0;
    try {
      for (let i = 0; i < list.length; i++) {
        if (escStopRef.current) { say(`중단 — ${done}/${list.length}개 받음`); break; }
        const ch = list[i];
        setEscRun({ i: i + 1, n: list.length, name: `${ch.tier} ${ch.unit} ${ch.idx}/${ch.of}` });
        const t0 = Date.now();
        const z = await buildEscZip(ch);
        saveBlob(z.blob, z.name);
        done++;
        say(`${i + 1}/${list.length} ${z.name} — 문항 ${z.items} · ${Math.round((Date.now() - t0) / 1000)}초${z.missing ? ` · 이미지 없음 ${z.missing}` : ""}`);
        if (i < list.length - 1) await new Promise((ok) => setTimeout(ok, 1500));   // 브라우저 연속 다운로드 간격
      }
      if (!escStopRef.current) say(`완료 — zip ${done}개. (브라우저가 "여러 파일 다운로드 허용" 물으면 허용)`);
    } catch (e) { say("내보내기 실패: " + String(e.message || e)); }
    setEscRun(null); setBusy(false);
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
          esc_triage: "T1-재전사-chat",
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

  const RETRO_USD = { primary: 0.005, retry: 0.005, sample: 0.015, arbiter: 0.025, answer_sheet: 0.005, classify: 0.002 };
  function monDerived(d) {
    if (!d) return null;
    const P = d.pages || {}, H = d.hour || {};
    const total = (P.done || 0) + (P.pending || 0) + (P.doing || 0) + (P.error || 0);
    const tracedUsd = (d.cost || []).reduce((a, c) => a + Number(c.usd || 0), 0);
    const retroUsd = (d.retro || []).reduce((a, r) => a + (RETRO_USD[r.role] || 0.005) * r.n, 0);
    const krw = Math.round((tracedUsd + retroUsd) * 1400);
    const rate = H.pages_done || 0;
    const callsPerPage = rate ? ((H.primary || 0) + (H.retry || 0) + (H.sample || 0) + (H.arbiter || 0)) / rate : 0;
    const leftH = rate ? (P.pending || 0) / rate : null;
    return { P, H, total, tracedUsd, retroUsd, krw, rate, callsPerPage, leftH };
  }
  function checkAlerts(d) {
    const m = monDerived(d); if (!m) return;
    const fire = (key, msg) => {
      if (!alertsRef.current[key]) { alertsRef.current[key] = msg; window.alert("⚠ 파이프라인 경보\n\n" + msg); }
      alertsRef.current[key] = msg;
    };
    const clear = (key) => { delete alertsRef.current[key]; };
    if (m.krw > budget) fire("budget", `누적 지출 추정 ${m.krw.toLocaleString()}원이 예산 상한(${budget.toLocaleString()}원)을 넘었어요 — 일시정지 권장`); else clear("budget");
    if ((d.hour?.arbiter2 || 0) > 150) fire("opus", `최근 1시간 오푸스 중재 ${d.hour.arbiter2}회 — 과열 (사다리 게이트 점검)`); else clear("opus");
    const clsN = (d.steps || []).find((x) => x.step === "classify")?.n || 0;
    if (clsN > 400) fire("clsloop", `분류 호출 ${clsN}회/1h — 좀비 마감 루프 의심 (v2.12 배포·지혈 SQL 확인)`); else clear("clsloop");
    if (m.rate > 5 && m.callsPerPage > 2.6) fire("burst", `페이지당 호출 ${m.callsPerPage.toFixed(1)}회 — 재시도 폭주 의심 (정상 1.3~2.2)`); else clear("burst");
    if ((d.chains || 0) === 0 && (m.P.pending || 0) > 0 && (d.jobs_running || 0) > 0) fire("dead", "활성 체인 0 — 진행이 멈춰 있었어요. 이 화면이 곧 재점화합니다 (탭을 닫아두면 다시 멈춰요)"); else clear("dead");
  }
  useEffect(() => {
    if (tab !== "mon") return;
    let on = true;
    const load = async () => {
      const { data, error } = await supabase.rpc("pipeline_stats", { p_hours: 1 });
      if (on && !error && data) { setMon(data); checkAlerts(data); }
      if (on && error) say("통계 RPC 실패 — v11 SQL 실행했는지 확인: " + error.message);
    };
    load();
    const iv = setInterval(load, 30000);
    return () => { on = false; clearInterval(iv); };
  }, [tab, budget]);  // eslint-disable-line

  async function pauseAll() {
    await supabase.from("transcribe_jobs").update({ status: "paused" }).eq("status", "running");
    say("전 작업 일시정지 — 체인이 1분 내 멈춥니다. [전체 재개]로 복귀");
  }
  async function resumeAll() {
    await supabase.from("transcribe_jobs").update({ status: "running" }).eq("status", "paused");
    say("재개 — 다음 틱에 자동 점화");
  }

  async function exportFiltered() {
    setBusy(true); say("필터 내보내기 수집 중…");
    try {
      const rows = [];
      for (let i = 0; ; i += 1000) {
        let q = supabase.from("corpus_items")
          .select("id,unit_id,src_tags,p_correct,seq,page,doc_id,qtype,question,choices,answer,difficulty_est,has_figure,figure,model_final,status,agree,drafts,concept_main,confidence,created_at")
          .order("created_at", { ascending: true }).range(i, i + 999);
        if (cUnit !== "all") q = q.eq("unit_id", cUnit);
        if (mFilter === "esc") q = q.eq("status", "escalated");
        else if (mFilter === "legacy") q = q.eq("status", "legacy");
        else if (mFilter === "haiku") q = q.in("model_final", ["haiku", "haiku+retry"]);
        else if (mFilter !== "all") q = q.eq("model_final", mFilter);
        const { data, error } = await q;
        if (error) throw new Error(error.message);
        rows.push(...(data || []));
        if (!data || data.length < 1000) break;
      }
      const blob = new Blob([JSON.stringify({ exported_at: new Date().toISOString(),
        filter: { model: mFilter, unit: cUnit }, count: rows.length, items: rows })], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `corpus_${mFilter}_${cUnit}_${new Date().toISOString().slice(0, 10)}.json`;
      a.click(); URL.revokeObjectURL(a.href);
      say(`내보내기 완료 — ${rows.length}건`);
    } catch (e) { say("내보내기 실패: " + e.message); }
    setBusy(false);
  }

  async function backupAll() {
    setBusy(true); say("백업 수집 중…");
    try {
      const grab = async (table, order = "created_at") => {
        const rows = [];
        for (let i = 0; ; i += 1000) {
          const { data, error } = await supabase.from(table).select("*").order(order, { ascending: true }).range(i, i + 999);
          if (error) throw new Error(table + ": " + error.message);
          rows.push(...(data || []));
          if (!data || data.length < 1000) break;
        }
        return rows;
      };
      const payload = {
        exported_at: new Date().toISOString(),
        docs: await grab("corpus_docs"),
        items: await grab("corpus_items"),
        solutions: await grab("corpus_solutions"),
        runs: await grab("transcribe_runs"),
        routing: await grab("transcribe_routing", "cluster_key"),
      };
      payload.counts = { docs: payload.docs.length, items: payload.items.length,
        solutions: payload.solutions.length, runs: payload.runs.length, routing: payload.routing.length };
      const blob = new Blob([JSON.stringify(payload)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `corpus_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click(); URL.revokeObjectURL(a.href);
      say(`백업 완료 — 문서 ${payload.counts.docs} · 문항 ${payload.counts.items} · 해설 ${payload.counts.solutions} · 로그 ${payload.counts.runs}`);
    } catch (e) { say("백업 실패: " + String(e.message || e)); }
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
              {prog ? ` · 문항 ${prog.saved} · 중재 ${prog.arb}` : ""}{prog?.err ? ` · 오류 ${prog.err}p` : ""}{queueN > 0 ? ` · 대기 작업 ${queueN}` : ""}</span>
            <span className="cp-jobsp" />
            {!jobDone && <button className="cp-btn danger sm" onClick={() => setCancelUi(true)}>취소</button>}
            {jobDone && <button className="cp-btn sm" onClick={() => setJob(null)}>닫기</button>}
          </div>
          <div className="cp-bar"><div className="cp-barfill" style={{ width: pct + "%" }} /></div>
          {!jobDone && <p className="cp-note">{job.runner === "local"
            ? "로컬 GPU 작업 — 집 PC에서 transcribe_local.py가 돌고 있어야 진행됩니다. 페이지가 끝나면 분류·마감은 이 화면이 자동 처리."
            : "탭을 닫거나 새로고침해도 서버에서 계속 진행됩니다 — 다시 열면 이 자리에서 이어집니다."}</p>}
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
        {[["run", "① 전사 실행"], ["browse", "② 코퍼스"], ["route", "③ 라우팅"], ["mon", "④ 모니터"]].map(([k, l]) => (
          <button key={k} className={"cp-tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>
        ))}
      </div>

      {tab === "run" && (
        <>
          {workerState && (
            <div className="cp-row" style={{ marginBottom: 8 }}>
              <span className="cp-note">집 PC 로컬 워커:</span>
              <button className={"cp-tab" + (workerState === "run" ? " on" : "")}
                onClick={async () => { await supabase.from("worker_control").update({ state: "run", updated_at: new Date().toISOString() }).eq("id", 1); setWorkerState("run"); }}>가동</button>
              <button className={"cp-tab" + (workerState === "paused" ? " on" : "")}
                onClick={async () => { await supabase.from("worker_control").update({ state: "paused", updated_at: new Date().toISOString() }).eq("id", 1); setWorkerState("paused"); }}>일시정지</button>
              <span className="cp-note">— PC에서 워커가 켜져 있어야 하고, 원격에선 멈춤·재개만 가능</span>
            </div>
          )}
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
              <select className="cp-in" value={runnerSel} onChange={(e) => setRunnerSel(e.target.value)}>
                <option value="cloud">전사: 클라우드 API</option>
                <option value="local">전사: 로컬 GPU (집 PC)</option>
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
            {[["all", "전체"], ["haiku", "하이쿠"], ["sonnet", "소넷"], ["opus", "오푸스"], ["fable-chat", "페이블"], ["esc", "상위 대기"], ["legacy", "구세대"]].map(([k, l]) => (
              <button key={k} className={"cp-tab" + (mFilter === k ? " on" : "")} onClick={() => setMFilter(k)}>
                {l}{mStats ? ` ${k === "all" ? "" : k === "esc" ? mStats.esc : k === "legacy" ? mStats.legacy : k === "fable-chat" ? mStats.fable : mStats[k] ?? ""}` : ""}
              </button>
            ))}
            <button className="cp-btn" onClick={exportFiltered} disabled={busy}>필터 내보내기(JSON)</button>
            <button className="cp-btn" onClick={() => impRef.current?.click()} disabled={busy}>전사 반영(JSON)</button>
            <button className="cp-btn" onClick={backupAll} disabled={busy}>전체 백업(JSON)</button>
            <input ref={impRef} type="file" accept="application/json,.json" hidden onChange={importFinal} />
          </div>
          {mStats?.esc > 0 && (
            <div className="cp-card" style={{ marginTop: 8 }}>
              <div className="cp-row">
                <b style={{ fontSize: 13 }}>대기 원본 내보내기</b>
                {!escPlan
                  ? <button className="cp-btn" onClick={planEsc} disabled={busy}>계획 세우기</button>
                  : <button className="cp-btn sm" onClick={() => setEscPlan(null)} disabled={busy}>다시 계획</button>}
                <span className="cp-note" style={{ margin: 0 }}>{ESC_CHUNK}쪽/zip · 파일명 앞에 실패 모델 · manifest 동봉 · T0-중복 제외</span>
              </div>
              {escPlan && (
                <>
                  <div className="cp-row" style={{ marginTop: 6 }}>
                    <span className="cp-note" style={{ margin: 0 }}>모델:</span>
                    {["sonnet", "opus"].map((t) => (
                      <label key={t} className={"cp-tab" + (escTiers.has(t) ? " on" : "")} style={{ cursor: "pointer" }}>
                        <input type="checkbox" hidden checked={escTiers.has(t)}
                          onChange={() => setEscTiers((s) => { const n = new Set(s); n.has(t) ? n.delete(t) : n.add(t); return n; })} />
                        {t === "sonnet" ? "소넷까지 실패" : "오푸스까지 실패"}
                      </label>
                    ))}
                    <button className="cp-btn sm" onClick={() => setEscUnits(new Set(escPlan.units))}>단원 전체</button>
                    <button className="cp-btn sm" onClick={() => setEscUnits(new Set())}>해제</button>
                  </div>
                  <div className="cp-row" style={{ marginTop: 4 }}>
                    {escPlan.units.map((u) => (
                      <label key={u} className={"cp-tab" + (escUnits.has(u) ? " on" : "")} style={{ cursor: "pointer", fontSize: 12 }}
                        title={`소넷 ${escStat(u, "sonnet")} / 오푸스 ${escStat(u, "opus")}`}>
                        <input type="checkbox" hidden checked={escUnits.has(u)}
                          onChange={() => setEscUnits((s) => { const n = new Set(s); n.has(u) ? n.delete(u) : n.add(u); return n; })} />
                        {u} <small style={{ opacity: .75 }}>{[
                          escTiers.has("sonnet") ? escStat(u, "sonnet") : null,
                          escTiers.has("opus") ? escStat(u, "opus") : null,
                        ].filter((x) => x && x !== "-").join(" + ") || "-"}</small>
                      </label>
                    ))}
                  </div>
                  <div className="cp-row" style={{ marginTop: 8 }}>
                    <button className="cp-btn go" onClick={() => exportEscMany(escSelected())} disabled={busy || !escSelected().length}>
                      선택 전부 받기 ({escSelected().length}개 zip · {escSelected().reduce((a, c) => a + c.pages.length, 0)}쪽)
                    </button>
                    <select className="cp-in" value={escOne} onChange={(e) => setEscOne(Number(e.target.value))} disabled={busy}>
                      {escPlan.chunks.map((c, i) => <option key={i} value={i}>{`${c.tier} ${c.unit} ${c.idx}/${c.of} (${c.pages.length}쪽)`}</option>)}
                    </select>
                    <button className="cp-btn" onClick={() => exportEscMany([escPlan.chunks[escOne]].filter(Boolean))} disabled={busy}>하나만 받기</button>
                    {escRun && (
                      <>
                        <span className="cp-note" style={{ margin: 0 }}>받는 중 {escRun.i}/{escRun.n} — {escRun.name}</span>
                        <button className="cp-btn danger sm" onClick={() => { escStopRef.current = true; }}>중단</button>
                      </>
                    )}
                  </div>
                </>
              )}
            </div>
          )}
          {corpus.map((it) => (
            <div key={it.id} className="cp-item" onClick={() => setOpenItem(openItem === it.id ? null : it.id)}>
              <p className="cp-q">{rt(it.question).split("\n")[0]}</p>
              {openItem === it.id && (
                <>
                  {(it.choices || []).map((c, j) => <p key={j} className="cp-c">{"①②③④⑤"[j] || "·"} {rt(c)}</p>)}
                  {it.answer != null && <p className="cp-c"><b>답</b> {rt(it.answer)}</p>}
                  {it.figure && !Array.isArray(it.figure) && <p className="cp-meta">도형: {it.figure.kind} — {(it.figure.relations || []).join(" / ")}</p>}
                  {Array.isArray(it.figure) && it.figure.map((f, j) => <p key={j} className="cp-meta">도형: {f.fn}({Object.keys(f.args || {}).join(", ")})</p>)}
                </>
              )}
              <p className="cp-meta">
                <b>{it.unit_id || "?"}</b> · {it.concept_main ? `${it.concept_main} ${cmap[it.concept_main] || ""}` : "미분류"}
                {(it.pattern_tags || []).length ? " · " + it.pattern_tags.join("/") : ""} · {it.qtype} · d{it.difficulty_est ?? "?"}
                · {it.agree ? "일치" : it.model_final}
                {it.status === "escalated" && <span className="cp-warn">상위 대기{it.esc_triage ? ` · ${it.esc_triage}` : ""}</span>}
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

      {tab === "mon" && (() => { const m = monDerived(mon); return (
        <div className="cp-card">
          <div className="cp-row" style={{ flexWrap: "wrap", gap: 8 }}>
            <button className="cp-btn" onClick={pauseAll}>⏸ 전체 일시정지</button>
            <button className="cp-btn" onClick={resumeAll}>▶ 전체 재개{mon?.jobs_paused ? ` (${mon.jobs_paused})` : ""}</button>
            <span className="cp-note" style={{ marginLeft: "auto" }}>예산 상한 ₩</span>
            <input className="cp-in" style={{ width: 110 }} type="number" step="10000" value={budget}
              onChange={(e) => { const v = Number(e.target.value) || 0; setBudget(v); localStorage.setItem("cp_budget", String(v)); }} />
          </div>
          {Object.keys(alertsRef.current).length > 0 && (
            <div style={{ background: "#7f1d1d", color: "#fecaca", borderRadius: 8, padding: "8px 10px", margin: "8px 0", fontSize: 13 }}>
              {Object.values(alertsRef.current).map((msg, i) => <div key={i}>⚠ {msg}</div>)}
            </div>
          )}
          {!m ? <p className="cp-note">통계 수집 중… (v11 SQL 실행 + v2.7 배포 후부터 계측이 쌓입니다)</p> : (
            <>
              <div className="cp-row" style={{ flexWrap: "wrap", gap: 14, margin: "10px 0" }}>
                <span>진행 <b>{(m.P.done || 0).toLocaleString()}</b>/{m.total.toLocaleString()}p{m.leftH != null ? ` · 잔여 ~${m.leftH.toFixed(1)}h` : ""}</span>
                <span>시간당 <b>{m.rate.toLocaleString()}</b>p · 문항 {(m.H.items || 0).toLocaleString()}</span>
                <span>체인 <b style={{ color: (mon.chains || 0) ? "#4ade80" : "#f87171" }}>{mon.chains || 0}</b></span>
                <span>재시도율 <b>{m.H.primary ? Math.round(100 * (m.H.retry || 0) / m.H.primary) : 0}%</b> · 대기行 {(m.H.esc || 0)}</span>
                <span>중재(1h) 소넷 <b>{m.H.arbiter || 0}</b> · 오푸스 <b style={{ color: (m.H.arbiter2 || 0) > 150 ? "#f87171" : "#4ade80" }}>{m.H.arbiter2 || 0}</b></span>
              </div>
              <div className="cp-row" style={{ flexWrap: "wrap", gap: 14 }}>
                <span>실측 지출(계측 이후) <b>${m.tracedUsd.toFixed(2)}</b></span>
                <span>소급 추정(계측 이전) ~${m.retroUsd.toFixed(0)}</span>
                <span>누적 <b>{m.krw.toLocaleString()}원</b> / {budget.toLocaleString()}원</span>
              </div>
              <p className="cp-note" style={{ margin: "10px 0 4px" }}>단계별 평균 (최근 1시간)</p>
              {(mon.steps || []).map((st) => (
                <div key={st.step} className="cp-row" style={{ gap: 8 }}>
                  <span style={{ width: 92, fontSize: 12 }}>{st.step}</span>
                  <div style={{ flex: 1, background: "#1e293b", borderRadius: 4, height: 10 }}>
                    <div style={{ width: Math.min(100, (st.avg_ms || 0) / 120) + "%", background: "#38bdf8", height: 10, borderRadius: 4 }} />
                  </div>
                  <span style={{ fontSize: 12, minWidth: 86 }}>{st.avg_ms}ms · {st.n}회</span>
                </div>
              ))}
              <p className="cp-note" style={{ margin: "10px 0 4px" }}>실시간 티커</p>
              <div style={{ fontFamily: "monospace", fontSize: 12, lineHeight: 1.7 }}>
                {(mon.recent || []).map((r, i) => (
                  <div key={i} style={{ color: r.ok === false ? "#f87171" : "#94a3b8" }}>
                    p.{r.page} {r.step}{r.model ? `·${r.model}` : ""}{r.ms ? ` ${r.ms}ms` : ""}{r.note ? ` — ${r.note}` : ""}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      ); })()}
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
