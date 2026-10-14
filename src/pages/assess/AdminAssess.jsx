// 관리자 — 서술형 평가 (#/admin/assess)
// ① 채팅방에서 받은 JSON 을 올려 평가 등록(검사 → 미리보기 → 등록) ② 평가 목록(열기·마감·정답 공개 시점·QR 주소) ③ 응시 기록(응시자·점수·쪽별 판독·채점·사진) ④ JSON 내보내기
import { useEffect, useRef, useState } from "react";
import { supabase } from "../../supabaseClient";
import FeatureBar from "../../components/FeatureBar";
import MathText from "../../components/MathText";
import { assessCall } from "../../lib/assess/api";
import { validateSpec, gradeLabel } from "../../lib/assess/spec";

const CSS = `
.aa { max-width: 980px; margin: 0 auto; padding: 12px 14px 80px; color: var(--text); font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.aa * { box-sizing: border-box; }
.aa-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 14px; margin-bottom: 12px; }
.aa-card h2 { margin: 0 0 8px; font-size: 15px; font-weight: 800; }
.aa-mut { color: var(--muted); font-size: 12.5px; line-height: 1.6; }
.aa-btn { border: 1px solid var(--border); background: var(--surface2); color: var(--text); font: inherit; font-size: 12.5px; font-weight: 700; padding: 7px 12px; border-radius: 10px; cursor: pointer; }
.aa-btn.pri { background: var(--accent); border-color: var(--accent); color: #fff; }
.aa-btn:disabled { opacity: .45; cursor: default; }
.aa-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.aa-drop { border: 2px dashed var(--border); border-radius: 12px; padding: 18px; text-align: center; cursor: pointer; color: var(--muted); font-size: 13px; }
.aa-drop.on { border-color: var(--accent); color: var(--text); }
.aa textarea { width: 100%; min-height: 80px; font: 12px ui-monospace, monospace; padding: 8px; border-radius: 10px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); }
.aa-err { color: var(--bad); font-size: 12.5px; margin: 4px 0; }
.aa-warn { color: #B45309; font-size: 12.5px; margin: 4px 0; }
.aa-chip { display: inline-block; font-size: 11px; font-weight: 800; border-radius: 999px; padding: 2px 8px; background: var(--surface3); }
.aa-chip.open { background: #DCFCE7; color: #166534; } .aa-chip.closed { background: #F1F5F9; color: #475569; } .aa-chip.soon { background: #FEF3C7; color: #92400E; }
.aa-chip.flag { background: #FEE2E2; color: #991B1B; }
.aa-pg { display: inline-flex; gap: 3px; flex-wrap: wrap; }
.aa-pg i { font-style: normal; width: 18px; height: 18px; border-radius: 5px; font-size: 10px; font-weight: 800; display: inline-flex; align-items: center; justify-content: center; background: var(--surface3); color: var(--muted); }
.aa-pg i.g { background: #DCFCE7; color: #166534; } .aa-pg i.r { background: #E0F2FE; color: #075985; } .aa-pg i.f { outline: 2px solid #EF4444; }
.aa-list { display: flex; flex-direction: column; gap: 8px; }
.aa-set { display: block; width: 100%; text-align: left; border: 1px solid var(--border); border-radius: 12px; padding: 10px 12px; background: var(--surface); color: var(--text); font: inherit; }
.aa-set.on { border-color: var(--accent); box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 25%, transparent); }
.aa-click { cursor: pointer; }
.aa-set-hd { display: flex; align-items: center; gap: 8px; justify-content: space-between; margin-bottom: 2px; }
.aa-set-hd b { font-size: 14px; }
.aa-score { font-weight: 900; font-size: 14px; white-space: nowrap; }
.aa-detail { border-top: 2px solid var(--accent); margin-top: 10px; padding-top: 10px; }
.aa-page { border: 1px solid var(--border); border-radius: 12px; padding: 10px; margin-bottom: 8px; }
.aa-page h3 { margin: 0 0 6px; font-size: 13.5px; }
.aa-lines { font-size: 12.5px; line-height: 1.6; background: var(--surface2); border-radius: 8px; padding: 6px 8px; margin: 4px 0; }
.aa-lines .st { text-decoration: line-through; color: var(--muted); }
.aa-img { max-width: 100%; border-radius: 8px; border: 1px solid var(--border); margin-top: 6px; }
.aa-sel { font: inherit; font-size: 12px; padding: 4px 6px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); }
.aa-toast { position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%); background: #111; color: #fff; padding: 9px 14px; border-radius: 10px; font-size: 13px; z-index: 90; }
`;

const STATE_LABEL = { open: "응시 중", closed: "마감", soon: "열기 전" };
const fmt = (iso) => { if (!iso) return ""; const d = new Date(iso); return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`; };

export default function AdminAssess({ theme = "light" }) {
  const [me, setMe] = useState(undefined);
  const [toast, setToast] = useState("");
  const [sets, setSets] = useState(null);
  const [ready, setReady] = useState(true);
  const [pick, setPick] = useState(null);       // 고른 평가 코드
  useEffect(() => {
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user; if (!u) { setMe(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      setMe(p?.role === "admin");
    });
  }, []);
  useEffect(() => { if (!toast) return; const t = setTimeout(() => setToast(""), 2800); return () => clearTimeout(t); }, [toast]);
  const reload = async () => {
    try { const r = await assessCall("admin_sets"); setSets(r.sets || []); setReady(r.ready !== false); }
    catch (e) { setToast(e.message); setSets([]); }
  };
  useEffect(() => { if (me) reload(); }, [me]);

  if (me === undefined) return null;
  if (!me) return <div className="aa"><style>{CSS}</style><div className="aa-card">관리자만 볼 수 있어요.</div></div>;
  return (
    <>
      <FeatureBar theme={theme} title="서술형 평가" sub="등록 · 응시 기록" back="#/" />
      <div className="aa">
        <style>{CSS}</style>
        {!ready && <div className="aa-card"><b>DB 설정 전이에요.</b> <span className="aa-mut">Supabase SQL Editor 에서 <code>supabase/2026-10_assess.sql</code> 을 실행하면 등록할 수 있어요.</span></div>}
        <Register onDone={() => reload()} setToast={setToast} />
        <SetList sets={sets} onPick={setPick} pick={pick} onChanged={reload} setToast={setToast} />
        {pick && <Sessions code={pick} setToast={setToast} />}
      </div>
      {toast && <div className="aa-toast">{toast}</div>}
    </>
  );
}

function Register({ onDone, setToast }) {
  const fileRef = useRef(null);
  const [raw, setRaw] = useState("");
  const [drag, setDrag] = useState(false);
  const [check, setCheck] = useState(null);     // { spec, v }
  const [busy, setBusy] = useState(false);
  const [conflict, setConflict] = useState(null);
  const parse = (text) => {
    setRaw(text); setConflict(null);
    try {
      const spec = JSON.parse(text);
      setCheck({ spec, v: validateSpec(spec, { bytes: new Blob([text]).size }) });
    } catch { setCheck({ spec: null, v: { ok: false, errors: ["JSON 을 읽지 못했어요 — 채팅방에서 받은 .json 파일 그대로인지 확인해 주세요"], warnings: [] } }); }
  };
  const readFile = async (f) => { if (f) parse(await f.text()); };
  const submit = async (overwrite = false) => {
    if (!check?.v?.ok) return;
    setBusy(true);
    try {
      const r = await assessCall("admin_register", { spec: raw, overwrite });
      setToast(`${r.set.code} ${r.updated ? "갱신" : "등록"} 완료`);
      setRaw(""); setCheck(null); setConflict(null); onDone();
    } catch (e) {
      if (e.status === 409) setConflict(e.message);
      else setToast(e.message + (e.extra?.errors ? " — " + e.extra.errors.join(" / ") : ""));
    } finally { setBusy(false); }
  };
  const s = check?.v?.summary;
  return (
    <div className="aa-card">
      <h2>① 평가 등록 — 채팅방에서 받은 JSON</h2>
      <input ref={fileRef} type="file" accept=".json,application/json" hidden onChange={(e) => { readFile(e.target.files?.[0]); e.target.value = ""; }} />
      <div className={"aa-drop" + (drag ? " on" : "")} onClick={() => fileRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
        onDrop={(e) => { e.preventDefault(); setDrag(false); readFile(e.dataTransfer?.files?.[0]); }}>
        📄 JSON 파일을 끌어다 놓거나 눌러서 고르기
      </div>
      <details style={{ marginTop: 8 }}><summary className="aa-mut">붙여넣기로 등록</summary>
        <textarea value={raw} onChange={(e) => parse(e.target.value)} placeholder='{"kind":"ashrain.assess", …}' /></details>
      {check && (
        <div style={{ marginTop: 10 }}>
          {check.v.errors.map((m, i) => <div key={i} className="aa-err">✕ {m}</div>)}
          {check.v.warnings.map((m, i) => <div key={i} className="aa-warn">! {m}</div>)}
          {s && (
            <>
              <p style={{ margin: "6px 0", fontWeight: 800 }}>{s.title} <span className="aa-chip">{s.code}</span></p>
              <p className="aa-mut" style={{ margin: 0 }}>{[s.date, s.grade_label, `${s.n_items}문제 · ${s.max}점`, `${s.n_pages}쪽`, `정답 공개: ${{ after_submit: "제출 뒤", after_close: "마감 뒤", never: "안 함" }[s.reveal]}`].filter(Boolean).join(" · ")}</p>
              <ol style={{ margin: "8px 0 0", paddingLeft: 20, fontSize: 12.5 }}>
                {check.spec.items.map((it) => <li key={it.no}><b>{it.topic}</b> — <span className="aa-mut">정답 <MathText text={it.answer} /></span></li>)}
              </ol>
              <div className="aa-row" style={{ marginTop: 10 }}>
                <button className="aa-btn pri" disabled={busy} onClick={() => submit(false)}>{busy ? "등록하는 중…" : "등록하기"}</button>
                <span className="aa-mut">등록하면 바로 학생앱에 알림이 뜨고 QR이 열려요.</span>
              </div>
            </>
          )}
          {conflict && (
            <div className="aa-row" style={{ marginTop: 8 }}>
              <span className="aa-warn">{conflict}</span>
              <button className="aa-btn" disabled={busy} onClick={() => submit(true)}>그래도 덮어쓰기</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SetList({ sets, onPick, pick, onChanged, setToast }) {
  const upd = async (code, patch) => {
    try { await assessCall("admin_update", { code, ...patch }); onChanged(); setToast("바꿨어요"); } catch (e) { setToast(e.message); }
  };
  const copy = async (code) => {
    const url = `${location.origin}/e/${code}`;
    try { await navigator.clipboard.writeText(url); setToast("주소를 복사했어요"); } catch { setToast(url); }
  };
  return (
    <div className="aa-card">
      <h2>② 평가 목록</h2>
      {!sets ? <p className="aa-mut">불러오는 중…</p> : !sets.length ? <p className="aa-mut">등록된 평가가 없어요.</p> : (
        <div className="aa-list">
          {sets.map((s) => (
            <div key={s.code} className={"aa-set" + (pick === s.code ? " on" : "")}>
              <div className="aa-set-hd">
                <b>{s.title}</b>
                <span className={"aa-chip " + s.state}>{STATE_LABEL[s.state] || s.status}</span>
              </div>
              <div className="aa-mut">{[s.code, s.test_date, s.grade_label, `${s.n_items}문제`, `제출 ${s.submitted}/${s.sessions}`, s.avg != null ? `평균 ${s.avg}/${s.max}` : null].filter(Boolean).join(" · ")}</div>
              <div className="aa-row" style={{ marginTop: 8 }}>
                {s.status === "live" ? <button className="aa-btn" onClick={() => upd(s.code, { status: "closed" })}>마감하기</button>
                  : <button className="aa-btn" onClick={() => upd(s.code, { status: "live" })}>다시 열기</button>}
                <label className="aa-mut" style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>정답 공개
                  <select className="aa-sel" value={s.reveal} onChange={(e) => upd(s.code, { reveal: e.target.value })}>
                    <option value="after_submit">제출 뒤</option><option value="after_close">마감 뒤</option><option value="never">안 함</option></select></label>
                <button className="aa-btn" onClick={() => copy(s.code)}>QR 주소 복사</button>
                <button className={"aa-btn" + (pick === s.code ? " pri" : "")} onClick={() => onPick(pick === s.code ? null : s.code)}>응시 기록</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Sessions({ code, setToast }) {
  const [data, setData] = useState(null);
  const [sid, setSid] = useState(null);
  const [det, setDet] = useState(null);
  const load = async () => { try { setData(await assessCall("admin_sessions", { code })); } catch (e) { setToast(e.message); setData({ sessions: [] }); } };
  useEffect(() => { setData(null); setSid(null); setDet(null); load(); }, [code]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!sid) { setDet(null); return; }
    setDet(null);
    assessCall("admin_session", { sid }).then(setDet).catch((e) => setToast(e.message));
  }, [sid]); // eslint-disable-line react-hooks/exhaustive-deps
  const exportJson = async () => {
    try {
      const r = await assessCall("admin_export", { code });
      const blob = new Blob([JSON.stringify(r, null, 1)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob); a.download = `assess-${code}-${new Date().toISOString().slice(0, 10)}.json`; a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    } catch (e) { setToast(e.message); }
  };
  return (
    <div className="aa-card">
      <div className="aa-row" style={{ justifyContent: "space-between" }}>
        <h2 style={{ margin: 0 }}>③ 응시 기록 — {code}</h2>
        <div className="aa-row"><button className="aa-btn" onClick={load}>새로고침</button><button className="aa-btn" onClick={exportJson}>JSON 내보내기</button></div>
      </div>
      {!data ? <p className="aa-mut">불러오는 중…</p> : !data.sessions.length ? <p className="aa-mut">아직 응시한 사람이 없어요.</p> : (
        <div className="aa-list" style={{ marginTop: 8 }}>
          {data.sessions.map((x) => {
            const flagged = x.pages.some((p) => p.flagged);
            return (
              <button key={x.sid} type="button" className={"aa-set aa-click" + (sid === x.sid ? " on" : "")} onClick={() => setSid(sid === x.sid ? null : x.sid)}>
                <div className="aa-set-hd">
                  <b>{x.info?.name || <span className="aa-mut">(이름 확인 전{x.ocr_name ? ` · 읽은 이름 ${x.ocr_name}` : ""})</span>}</b>
                  <span className="aa-score">{x.status === "submitted" ? `${x.total}/${x.max}` : "찍는 중"}</span>
                </div>
                <div className="aa-mut">{[x.info?.grade && gradeLabel(x.info.grade), x.info?.nickname, x.login ? "로그인" : "비로그인", x.info?.by === "user" ? "학생이 이름 고침" : null, fmt(x.started_at)].filter(Boolean).join(" · ")}
                  {flagged && <> <span className="aa-chip flag">이의</span></>}</div>
                <span className="aa-pg" style={{ marginTop: 6 }}>{x.pages.map((p) => <i key={p.no} className={(p.status === "graded" || p.status === "ok" ? "g" : p.status === "read" ? "r" : "") + (p.flagged ? " f" : "")} title={`${p.no}쪽 · ${p.status} · ${p.attempts}번`}>{p.no}</i>)}</span>
              </button>
            );
          })}
        </div>
      )}
      {sid && (
        <div className="aa-detail">
          {!det ? <p className="aa-mut">불러오는 중…</p> : (
            <>
              <p style={{ margin: "0 0 8px", fontWeight: 800 }}>{det.session.info?.name || "(이름 미확인)"} · {det.result.total}/{det.result.max}점 <span className="aa-mut">{det.session.status === "submitted" ? `제출 ${fmt(det.session.submitted_at)}` : "찍는 중"}</span></p>
              {det.session.ocr_info && <div className="aa-page"><h3>2쪽 판독(원본)</h3>
                <div className="aa-mut">학년 {det.session.ocr_info.grade ?? "–"} · 이름 {det.session.ocr_info.name ?? "–"} · 닉네임 {det.session.ocr_info.nickname ?? "–"}</div>
                <div className="aa-lines">{(det.session.ocr_info.phrase || []).map((l, i) => <div key={i}>{i + 1}) {l || <span className="aa-mut">(빈 줄)</span>}</div>)}</div></div>}
              {det.pages.filter((p) => p.kind === "item" || p.image_url).map((p) => {
                const it = det.result.items.find((x) => x.page === p.no);
                return (
                  <div key={p.no} className="aa-page">
                    <h3>{p.no}쪽{p.kind === "item" ? ` · 문제 ${p.item}` : ""} {it?.graded ? `— ${it.got}/${it.max}점` : ""} {p.flagged && <span className="aa-chip flag">이의: {p.flag_note || "잘못 읽음"}</span>}</h3>
                    {p.read && ["s1", "s2", "s3"].map((k) => (
                      <div key={k} className="aa-lines"><b>{{ s1: "①", s2: "②", s3: "③" }[k]}</b> {(p.read[k]?.lines || []).map((l, i) => <div key={i} className={l.struck ? "st" : ""}>{l.arrow ? "→ " : ""}{l.t}</div>)}</div>
                    ))}
                    {p.grade && <div className="aa-mut">{p.grade.marks.map((m) => `${m.no}) ${m.got}점 — ${m.reason}`).join(" / ")}{p.grade.needs_review ? " · 확인 필요" : ""}</div>}
                    <div className="aa-mut" style={{ fontSize: 11 }}>판독 {p.model_read || "–"} · 채점 {p.model_grade || "–"} · 시도 {p.attempts} · 선명도 {p.quality?.sharp ?? "–"} · 읽기 어려움 {p.read?.legibility?.score ?? "–"}/5</div>
                    {p.image_url && <img className="aa-img" src={p.image_url} alt={`${p.no}쪽 사진`} loading="lazy" />}
                  </div>
                );
              })}
            </>
          )}
        </div>
      )}
    </div>
  );
}
