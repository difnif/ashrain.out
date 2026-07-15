import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

// ashrain.out — 힌트 (v0.3.0)
// src/components/Hint.jsx — Home.jsx(v0.3.0)가 힌트 탭에서 import 합니다.
// 흐름: 문제 사진 촬영/선택 → (선택) 질문 입력 → /api/ai(task:hint) → 접근법 힌트 (정답 없음)
// 저장: storage notes/{uid}/hint/{id}.jpg + hint_logs (계정별 격리, 공유 토글 시 관리자만 열람)
// 모델: DB app_settings.hint_model 값 사용 — SQL 한 줄로 소넷↔오푸스 전환 가능

const fmtDate = (s) => new Date(s).toLocaleDateString();

const CSS = `
.ht-top { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:12px; flex-wrap:wrap; }
.ht-title { font-size:15px; font-weight:800; color:var(--ink); }
.ht-act { width:100%; padding:13px 8px; border-radius:12px; border:1px solid var(--ac); background:transparent;
  color:var(--ac); font-weight:800; font-size:14px; cursor:pointer; margin-bottom:10px; }
.ht-note { color:var(--mut); font-size:12px; line-height:1.6; margin:0 2px 14px; }
.ht-sec { font-size:13px; font-weight:800; color:var(--mut); letter-spacing:1px; margin:18px 0 8px; }
.ht-empty { color:var(--mut); font-size:13.5px; text-align:center; padding:28px 0; }
.ht-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:8px; }
.ht-shot { border:1px solid var(--bd); border-radius:12px; overflow:hidden; background:var(--card); cursor:pointer; padding:0; text-align:left; }
.ht-shot img { width:100%; aspect-ratio:3/4; object-fit:cover; display:block; background:rgba(0,0,0,.06); }
.ht-shot p { margin:0; padding:7px 10px 8px; font-size:12px; color:var(--mut); }
.ht-shot p b { color:var(--ink); }

/* 질문·결과 */
.ht-stage { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:14px; }
.ht-step { font-size:12.5px; color:var(--mut); margin:0 0 10px; }
.ht-img { width:100%; border-radius:10px; border:1px solid var(--bd); display:block; }
.ht-ta { width:100%; box-sizing:border-box; background:transparent; border:1px solid var(--bd); border-radius:10px;
  padding:10px 12px; color:var(--ink); font-size:14px; min-height:64px; resize:vertical; font-family:inherit; margin-top:10px; }
.ht-row { display:flex; gap:8px; margin-top:12px; }
.ht-go { flex:1; padding:11px; border-radius:10px; border:1px solid var(--ac); background:transparent; color:var(--ac); font-weight:800; font-size:14px; cursor:pointer; }
.ht-go:disabled { opacity:.45; }
.ht-back { padding:11px 14px; border-radius:10px; border:1px solid var(--bd); background:transparent; color:var(--mut); font-size:13px; cursor:pointer; }
.ht-ans { white-space:pre-wrap; font-size:14px; line-height:1.75; color:var(--ink);
  background:rgba(127,127,127,.07); border-radius:10px; padding:13px; margin-top:12px; word-break:keep-all; }
.ht-model { font-size:11px; color:var(--mut); text-align:right; margin-top:6px; }

/* 상세 모달 */
.ht-modal-bg { position:fixed; inset:0; background:rgba(0,0,0,.5); display:flex; align-items:center; justify-content:center; z-index:70; padding:18px; }
.ht-modal { background:var(--card); border:1px solid var(--bd); border-radius:16px; max-width:460px; width:100%;
  padding:16px; color:var(--ink); max-height:88vh; overflow-y:auto; }
.ht-modal h3 { margin:0 0 8px; font-size:15.5px; }
`;

export default function Hint({ uid, isAdmin, unitNames, say }) {
  const [step, setStep] = useState(null);         // null | ask | busy | result
  const [imgCv, setImgCv] = useState(null);       // 축소된 문제 사진 캔버스
  const [imgUrlLocal, setImgUrlLocal] = useState("");
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);     // {hint, model}
  const [myLogs, setMyLogs] = useState(null);
  const [shared, setShared] = useState(null);
  const [urls, setUrls] = useState({});
  const [detail, setDetail] = useState(null);     // {title, path, body, comment}
  const fileRef = useRef(null);

  useEffect(() => { loadMine(); loadShared(); }, [uid]); // eslint-disable-line

  async function loadMine() {
    if (!uid) { setMyLogs([]); return; }
    const { data } = await supabase.from("hint_logs").select("*")
      .eq("user_id", uid).order("created_at", { ascending: false }).limit(24);
    setMyLogs(data || []);
    signAll(data);
  }
  async function loadShared() {
    const { data } = await supabase.from("shared_hints").select("*")
      .order("created_at", { ascending: false }).limit(12);
    setShared(data || []);
    signAll(data);
  }
  async function signAll(rows) {
    const paths = (rows || []).map((r) => r.image_path).filter((p) => p && !urls[p]);
    if (!paths.length) return;
    const { data } = await supabase.storage.from("notes").createSignedUrls(paths, 3600);
    if (data) {
      const add = {};
      data.forEach((d) => { if (d.signedUrl && d.path) add[d.path] = d.signedUrl; });
      setUrls((m) => ({ ...m, ...add }));
    }
  }

  // ── 사진 선택 → 1200px 축소 ──
  function pickFile(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (!f) return;
    const im = new Image();
    im.onload = () => {
      const cap = 1200, sc = Math.min(1, cap / Math.max(im.width, im.height));
      const cv = document.createElement("canvas");
      cv.width = Math.round(im.width * sc); cv.height = Math.round(im.height * sc);
      cv.getContext("2d").drawImage(im, 0, 0, cv.width, cv.height);
      URL.revokeObjectURL(im.src);
      setImgCv(cv);
      setImgUrlLocal(cv.toDataURL("image/jpeg", 0.85));
      setQuestion("");
      setStep("ask");
    };
    im.onerror = () => say("사진을 열 수 없어요");
    im.src = URL.createObjectURL(f);
  }

  // ── 힌트 요청 ──
  async function getHint() {
    if (!uid) { say("로그인 후 이용할 수 있어요"); return; }
    setStep("busy");
    try {
      const dataUrl = imgCv.toDataURL("image/jpeg", 0.85);
      const base64 = dataUrl.split(",")[1];
      // 1) 사진 업로드 (내 폴더 — 계정별 격리)
      const path = `${uid}/hint/${crypto.randomUUID()}.jpg`;
      const blob = await (await fetch(dataUrl)).blob();
      const { error: e1 } = await supabase.storage.from("notes")
        .upload(path, blob, { contentType: "image/jpeg" });
      if (e1) throw e1;
      // 2) AI 호출
      const { data: sess } = await supabase.auth.getSession();
      const token = sess?.session?.access_token;
      if (!token) throw new Error("세션이 만료됐어요 — 다시 로그인해 주세요");
      const r = await fetch("/api/ai", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
        body: JSON.stringify({ task: "hint", image: base64, question: question.trim() || undefined }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j?.error || "요청 실패");
      // 3) 기록 저장
      const { error: e2 } = await supabase.from("hint_logs").insert({
        user_id: uid, image_path: path, model: j.model, response: j.hint,
      });
      if (e2) say("기록 저장 실패: " + e2.message);   // 힌트는 이미 받았으니 표시는 계속
      setResult({ hint: j.hint, model: j.model });
      setStep("result");
      loadMine();
    } catch (err) {
      say("힌트 실패: " + (err?.message || String(err)));
      setStep("ask");
    }
  }
  function resetAsk() { setStep(null); setImgCv(null); setImgUrlLocal(""); setQuestion(""); setResult(null); }

  return (
    <div>
      <style>{CSS}</style>
      <input ref={fileRef} type="file" accept="image/*" capture="environment" hidden onChange={pickFile} />

      {/* ── 촬영 → 질문 → 결과 ── */}
      {step && (
        <div className="ht-stage">
          {step === "ask" && (
            <>
              <p className="ht-step"><b style={{ color: "var(--ac)" }}>1/2</b> 사진을 확인하고, 궁금한 점이 있으면 적어 주세요 (안 적어도 돼요).</p>
              <img className="ht-img" src={imgUrlLocal} alt="" />
              <textarea className="ht-ta" placeholder="예: 어디서부터 시작해야 할지 모르겠어요 / 2번 문제요"
                value={question} onChange={(e) => setQuestion(e.target.value)} />
              <div className="ht-row">
                <button className="ht-back" onClick={resetAsk}>취소</button>
                <button className="ht-back" onClick={() => fileRef.current.click()}>사진 다시</button>
                <button className="ht-go" onClick={getHint}>💡 힌트 받기</button>
              </div>
            </>
          )}
          {step === "busy" && (
            <>
              <p className="ht-step">문제를 읽고 있어요… 10~20초 정도 걸려요.</p>
              <img className="ht-img" src={imgUrlLocal} alt="" style={{ opacity: 0.55 }} />
            </>
          )}
          {step === "result" && result && (
            <>
              <p className="ht-step"><b style={{ color: "var(--ac)" }}>2/2</b> 정답 대신, 스스로 풀 수 있게 접근법만 안내해요.</p>
              <img className="ht-img" src={imgUrlLocal} alt="" />
              <div className="ht-ans">{result.hint}</div>
              <p className="ht-model">답변 모델: {result.model}</p>
              <div className="ht-row">
                <button className="ht-back" onClick={resetAsk}>닫기</button>
                <button className="ht-go" onClick={() => fileRef.current.click()}>📷 다른 문제 힌트 받기</button>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── 기본 화면 ── */}
      {!step && (
        <>
          <div className="ht-top">
            <span className="ht-title">💡 힌트</span>
          </div>
          <button className="ht-act" onClick={() => (uid ? fileRef.current.click() : say("로그인 후 이용할 수 있어요"))}>
            💡 문제 사진으로 힌트 받기
          </button>
          <p className="ht-note">
            정답을 알려주지 않아요 — 문제의 문장과 단서를 분석해서, 어떤 개념으로 어떻게 접근할지까지만 안내해요.
            사진은 내 계정에만 저장되고, 환경설정에서 공유를 켠 경우에만 선생님이 볼 수 있어요.
          </p>

          {uid && (
            <>
              <p className="ht-sec">🗂 내 힌트 기록</p>
              {myLogs === null && <p className="ht-empty">불러오는 중…</p>}
              {myLogs !== null && myLogs.length === 0 && <p className="ht-empty">아직 힌트를 받은 문제가 없어요.</p>}
              <div className="ht-grid">
                {(myLogs || []).map((h) => (
                  <button key={h.id} className="ht-shot"
                    onClick={() => setDetail({ title: "내가 질문한 문제", path: h.image_path, body: h.response, comment: null })}>
                    {urls[h.image_path] && <img src={urls[h.image_path]} alt="" />}
                    <p><b>{fmtDate(h.created_at)}</b> · 탭해서 힌트 다시 보기</p>
                  </button>
                ))}
              </div>
            </>
          )}

          <p className="ht-sec">👥 친구들이 고민한 문제</p>
          {shared === null && <p className="ht-empty">불러오는 중…</p>}
          {shared !== null && shared.length === 0 && <p className="ht-empty">아직 공유된 문제가 없어요.</p>}
          <div className="ht-grid">
            {(shared || []).map((h) => (
              <button key={h.id} className="ht-shot"
                onClick={() => setDetail({ title: h.title, path: h.image_path, body: h.ai_response, comment: h.comment })}>
                {urls[h.image_path] && <img src={urls[h.image_path]} alt="" />}
                <p><b>{h.title}</b>{h.unit_id ? ` · ${unitNames?.[h.unit_id] || h.unit_id}` : ""}</p>
              </button>
            ))}
          </div>
        </>
      )}

      {/* ── 상세 모달 ── */}
      {detail && (
        <div className="ht-modal-bg" onClick={() => setDetail(null)}>
          <div className="ht-modal" onClick={(e) => e.stopPropagation()}>
            <h3>{detail.title}</h3>
            {urls[detail.path] && <img className="ht-img" src={urls[detail.path]} alt="" />}
            {detail.comment && <p className="ht-note" style={{ marginTop: 10 }}>💬 {detail.comment}</p>}
            {detail.body && <div className="ht-ans">{detail.body}</div>}
            <div className="ht-row">
              <button className="ht-go" onClick={() => setDetail(null)}>닫기</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
