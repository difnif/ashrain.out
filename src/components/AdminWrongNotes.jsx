import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

// ashrain.out — 오답 관리자 화면 (v0.2.1)
// 이 파일을 src/components/AdminWrongNotes.jsx 로 업로드하세요. WrongNote.jsx가 import 합니다.
// 사전 SQL: admin_list_wrong_notes() 를 학생 이름 포함 버전으로 교체 (패치 노트의 v0.2.1 SQL 참고)
//
// 탭 ①: 학생 오답 — 공유를 허용한 학생의 오답만 조회 (메모는 별도 허용 시에만, 아니면 null)
// 탭 ②: 친구 오답 — 모든 유저에게 노출되는 공유 오답 등록(학생 오답에서 가져오기 / 직접 업로드)·삭제

const REASON_LABEL = { calc: "계산 실수", concept: "개념 부족", reading: "문제 해석", time: "시간 부족", guess: "찍음", etc: "기타" };
const STATUS_LABEL = { new: "🆕 새 오답", retried: "🔄 다시 풂", cleared: "✅ 극복" };

const CSS = `
.aw-tabs { display:flex; gap:6px; margin-bottom:12px; }
.aw-tab { flex:1; padding:9px 4px; border-radius:10px; border:1px solid var(--bd); background:var(--card);
  color:var(--mut); font-size:13px; font-weight:700; cursor:pointer; }
.aw-tab.on { color:var(--ac); border-color:var(--ac); }
.aw-flt { display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap; }
.aw-sel { background:var(--card); border:1px solid var(--bd); color:var(--ink); border-radius:8px; padding:7px 9px; font-size:12.5px; }
.aw-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(160px,1fr)); gap:8px; }
.aw-shot { border:1px solid var(--bd); border-radius:12px; overflow:hidden; background:var(--card); cursor:pointer; padding:0; text-align:left; }
.aw-shot img { width:100%; aspect-ratio:3/4; object-fit:cover; display:block; background:rgba(0,0,0,.06); }
.aw-shot p { margin:0; padding:7px 10px 8px; font-size:12px; color:var(--mut); line-height:1.5; }
.aw-shot p b { color:var(--ink); font-size:12.5px; }
.aw-empty { color:var(--mut); font-size:13.5px; text-align:center; padding:30px 0; }
.aw-btn { background:var(--card); border:1px solid var(--bd); color:var(--ink); font-size:12.5px; border-radius:8px; padding:8px 12px; cursor:pointer; }
.aw-act { width:100%; padding:12px 8px; border-radius:12px; border:1px solid var(--ac); background:transparent;
  color:var(--ac); font-weight:800; font-size:13.5px; cursor:pointer; margin-bottom:12px; }
.aw-modal-bg { position:fixed; inset:0; background:rgba(0,0,0,.5); display:flex; align-items:center; justify-content:center; z-index:80; padding:18px; }
.aw-modal { background:var(--card); border:1px solid var(--bd); border-radius:16px; max-width:460px; width:100%;
  padding:16px; color:var(--ink); max-height:88vh; overflow-y:auto; }
.aw-modal h3 { margin:0 0 8px; font-size:15px; }
.aw-img { width:100%; border-radius:10px; border:1px solid var(--bd); }
.aw-meta { font-size:12.5px; color:var(--mut); margin:8px 0; line-height:1.7; }
.aw-in { width:100%; box-sizing:border-box; background:transparent; border:1px solid var(--bd); border-radius:10px;
  padding:10px 12px; color:var(--ink); font-size:13.5px; margin-bottom:8px; }
.aw-row { display:flex; gap:8px; margin-top:10px; }
.aw-pri { flex:1; padding:10px; border-radius:10px; border:1px solid var(--ac); background:transparent; color:var(--ac); font-weight:800; font-size:13.5px; cursor:pointer; }
.aw-sec2 { padding:10px 14px; border-radius:10px; border:1px solid var(--bd); background:transparent; color:var(--mut); font-size:13px; cursor:pointer; }
.aw-del { width:100%; margin-top:8px; padding:9px; border-radius:10px; border:1px solid #E5484D55; color:#E5484D; background:transparent; font-size:12.5px; cursor:pointer; }
.aw-note { color:var(--mut); font-size:11.5px; margin:8px 2px 12px; line-height:1.6; }
`;

export default function AdminWrongNotes({ unitNames, say }) {
  const [tab, setTab] = useState("students");
  const [rows, setRows] = useState(null);       // 학생 오답 (RPC)
  const [shared, setShared] = useState(null);   // 공유(친구) 오답
  const [urls, setUrls] = useState({});
  const [fStu, setFStu] = useState("all");
  const [fUnit, setFUnit] = useState("all");
  const [fSt, setFSt] = useState("all");
  const [detail, setDetail] = useState(null);   // 학생 오답 상세
  const [shareForm, setShareForm] = useState(null); // {src:'student'|'upload', row?, file?, title, unit, comment}
  const [busy, setBusy] = useState(false);
  const [delArm, setDelArm] = useState(null);
  const fileRef = useRef(null);

  const unitIds = Object.keys(unitNames).sort((a, b) => (a[0] === b[0] ? a.localeCompare(b) : a[0] === "m" ? -1 : 1));

  useEffect(() => { loadStudents(); loadShared(); }, []); // eslint-disable-line

  async function loadStudents() {
    const { data, error } = await supabase.rpc("admin_list_wrong_notes");
    if (error) { say("학생 오답 조회 실패 — v0.2.1 SQL 실행 여부 확인: " + error.message); setRows([]); return; }
    setRows(data || []);
    signAll(data);
  }
  async function loadShared() {
    const { data } = await supabase.from("shared_wrong_notes").select("*").order("created_at", { ascending: false });
    setShared(data || []);
    signAll(data);
  }
  async function signAll(list) {
    for (const r of list || []) {
      if (!r.image_path || urls[r.image_path]) continue;
      const { data } = await supabase.storage.from("notes").createSignedUrl(r.image_path, 3600);
      if (data?.signedUrl) setUrls((m) => ({ ...m, [r.image_path]: data.signedUrl }));
    }
  }

  // ── 친구 오답으로 공유 (학생 오답 사본 or 직접 업로드) ──
  async function submitShare() {
    if (!shareForm.title.trim()) { say("제목을 입력해 주세요"); return; }
    setBusy(true);
    try {
      let blob;
      if (shareForm.src === "student") {
        const url = urls[shareForm.row.image_path];
        blob = await (await fetch(url)).blob();          // 원본과 분리된 사본으로 저장 (익명화)
      } else {
        blob = shareForm.file;
      }
      const path = `shared/wrong/${crypto.randomUUID()}.jpg`;
      const { error: e1 } = await supabase.storage.from("notes")
        .upload(path, blob, { contentType: blob.type || "image/jpeg" });
      if (e1) throw e1;
      const { error: e2 } = await supabase.from("shared_wrong_notes").insert({
        image_path: path, title: shareForm.title.trim(),
        unit_id: shareForm.unit || null, comment: shareForm.comment.trim() || null,
      });
      if (e2) throw e2;
      say("친구 오답으로 등록했어요 — 모든 학생에게 보여요");
      setShareForm(null); setDetail(null);
      loadShared();
    } catch (err) { say("등록 실패: " + err.message); }
    setBusy(false);
  }
  function pickUpload(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (f) setShareForm({ src: "upload", file: f, title: "", unit: "", comment: "" });
  }
  async function removeShared(w) {
    if (delArm !== w.id) { setDelArm(w.id); return; }
    setDelArm(null);
    setShared((s) => s.filter((x) => x.id !== w.id));
    await supabase.storage.from("notes").remove([w.image_path]);
    const { error } = await supabase.from("shared_wrong_notes").delete().eq("id", w.id);
    say(error ? "삭제 실패: " + error.message : "공유를 내렸어요");
  }

  const stuNames = [...new Set((rows || []).map((r) => r.student_name || r.user_id))];
  const shownRows = (rows || []).filter((r) =>
    (fStu === "all" || (r.student_name || r.user_id) === fStu) &&
    (fUnit === "all" || r.unit_id === fUnit) &&
    (fSt === "all" || r.status === fSt));

  return (
    <div>
      <style>{CSS}</style>
      <div className="aw-tabs">
        <button className={"aw-tab" + (tab === "students" ? " on" : "")} onClick={() => setTab("students")}>👀 학생 오답</button>
        <button className={"aw-tab" + (tab === "shared" ? " on" : "")} onClick={() => setTab("shared")}>👥 친구 오답 관리</button>
      </div>

      {tab === "students" && (
        <>
          <p className="aw-note">공유를 허용한 학생의 오답만 보여요. 메모는 학생이 메모 공유까지 켠 경우에만 표시돼요.</p>
          <div className="aw-flt">
            <select className="aw-sel" value={fStu} onChange={(e) => setFStu(e.target.value)}>
              <option value="all">학생 전체</option>
              {stuNames.map((n) => <option key={n} value={n}>{n}</option>)}
            </select>
            <select className="aw-sel" value={fUnit} onChange={(e) => setFUnit(e.target.value)}>
              <option value="all">단원 전체</option>
              {unitIds.map((u) => <option key={u} value={u}>{unitNames[u]}</option>)}
            </select>
            <select className="aw-sel" value={fSt} onChange={(e) => setFSt(e.target.value)}>
              <option value="all">상태 전체</option>
              {Object.entries(STATUS_LABEL).map(([k, l]) => <option key={k} value={k}>{l}</option>)}
            </select>
          </div>
          {rows === null && <p className="aw-empty">불러오는 중…</p>}
          {rows !== null && shownRows.length === 0 && <p className="aw-empty">조건에 맞는 오답이 없어요. (학생이 공유를 켜야 보여요)</p>}
          <div className="aw-grid">
            {shownRows.map((r) => (
              <button key={r.id} className="aw-shot" onClick={() => setDetail(r)}>
                {urls[r.image_path] && <img src={urls[r.image_path]} alt="" />}
                <p><b>{r.student_name || r.user_id.slice(0, 8)}</b><br />
                  {r.unit_id ? unitNames[r.unit_id] || r.unit_id : "단원 미지정"}
                  {r.reason ? ` · ${REASON_LABEL[r.reason]}` : ""} · {STATUS_LABEL[r.status]}</p>
              </button>
            ))}
          </div>
        </>
      )}

      {tab === "shared" && (
        <>
          <input ref={fileRef} type="file" accept="image/*" hidden onChange={pickUpload} />
          <button className="aw-act" onClick={() => fileRef.current.click()}>＋ 사진 올려서 친구 오답 등록</button>
          <p className="aw-note">학생 오답 탭에서 오답을 눌러 「친구 오답으로 공유」해도 등록돼요. 등록본은 사본이라 학생이 원본을 지워도 유지됩니다.</p>
          {shared !== null && shared.length === 0 && <p className="aw-empty">등록된 친구 오답이 없어요.</p>}
          <div className="aw-grid">
            {(shared || []).map((w) => (
              <div key={w.id} className="aw-shot" style={{ cursor: "default" }}>
                {urls[w.image_path] && <img src={urls[w.image_path]} alt="" />}
                <p><b>{w.title}</b><br />{w.unit_id ? unitNames[w.unit_id] || w.unit_id : "단원 미지정"}</p>
                <button className="aw-del" style={{ margin: "0 0 8px", width: "calc(100% - 16px)", marginLeft: 8 }}
                  onClick={() => removeShared(w)}>
                  {delArm === w.id ? "정말 내릴까요? 한 번 더" : "공유 내리기"}
                </button>
              </div>
            ))}
          </div>
        </>
      )}

      {/* 학생 오답 상세 */}
      {detail && !shareForm && (
        <div className="aw-modal-bg" onClick={() => setDetail(null)}>
          <div className="aw-modal" onClick={(e) => e.stopPropagation()}>
            <h3>{detail.student_name || detail.user_id.slice(0, 8)} 학생의 오답</h3>
            {urls[detail.image_path] && <img className="aw-img" src={urls[detail.image_path]} alt="" />}
            <p className="aw-meta">
              {detail.unit_id ? unitNames[detail.unit_id] || detail.unit_id : "단원 미지정"}
              {detail.reason ? ` · ${REASON_LABEL[detail.reason]}` : ""}
              {detail.source ? ` · ${detail.source}` : ""} · {STATUS_LABEL[detail.status]}
              {detail.tags?.length ? <><br />🏷 {detail.tags.join(", ")}</> : null}
              <br />📝 {detail.memo === null || detail.memo === undefined ? "(메모 비공개 또는 없음)" : detail.memo}
              <br />{new Date(detail.created_at).toLocaleString()}
            </p>
            <div className="aw-row">
              <button className="aw-sec2" onClick={() => setDetail(null)}>닫기</button>
              <button className="aw-pri" onClick={() =>
                setShareForm({ src: "student", row: detail, title: "", unit: detail.unit_id || "", comment: "" })}>
                👥 친구 오답으로 공유
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 공유 등록 폼 */}
      {shareForm && (
        <div className="aw-modal-bg" onClick={() => !busy && setShareForm(null)}>
          <div className="aw-modal" onClick={(e) => e.stopPropagation()}>
            <h3>👥 친구 오답으로 등록</h3>
            <p className="aw-meta">모든 학생에게 보여요. 제목은 이름이 드러나지 않게 붙여 주세요 (예: 이차함수 꼭짓점 부호 실수).</p>
            <input className="aw-in" placeholder="제목 (필수)" value={shareForm.title}
              onChange={(e) => setShareForm({ ...shareForm, title: e.target.value })} />
            <select className="aw-in" value={shareForm.unit}
              onChange={(e) => setShareForm({ ...shareForm, unit: e.target.value })}>
              <option value="">단원 선택 안 함</option>
              {unitIds.map((u) => <option key={u} value={u}>{unitNames[u]}</option>)}
            </select>
            <input className="aw-in" placeholder="원장 코멘트 (선택) — 왜 볼 가치가 있는 오답인지"
              value={shareForm.comment}
              onChange={(e) => setShareForm({ ...shareForm, comment: e.target.value })} />
            <div className="aw-row">
              <button className="aw-sec2" onClick={() => setShareForm(null)} disabled={busy}>취소</button>
              <button className="aw-pri" onClick={submitShare} disabled={busy}>{busy ? "등록 중…" : "등록하기 ✓"}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
