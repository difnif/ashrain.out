// ashrain.out — 관리자 보호자 승인 화면 (v1.0, #/admin/guardians)
// 학생이 제출한 보호자 동의를 강사가 최종 확인·승인/반려.
// ⚠ 배지: 나이간극(보호자-학생 출생연도 차 16년 미만), 다계정(같은 번호가 3명 이상의 학생 보호자로 등록).
// 반려 건은 5일 뒤 자동 파기됩니다(제출 API가 청소).
import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

const TABS = [["pending", "⏳ 대기"], ["active", "✅ 활성"], ["rejected", "❌ 반려"]];

export default function AdminGuardians() {
  const [isAdmin, setIsAdmin] = useState(null);
  const [tab, setTab] = useState("pending");
  const [rows, setRows] = useState(null);      // 전체 동의 목록
  const [students, setStudents] = useState({}); // id → {name, grade}
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const load = async () => {
    setErr("");
    const { data, error } = await supabase.from("guardian_consents")
      .select("*").order("created_at", { ascending: false });
    if (error) { setErr(error.message); return; }
    setRows(data || []);
    const ids = [...new Set((data || []).map((r) => r.student_id))];
    if (ids.length) {
      const { data: ps } = await supabase.from("profiles")
        .select("id, name, grade").in("id", ids);
      const m = {};
      (ps || []).forEach((p) => { m[p.id] = p; });
      setStudents(m);
    }
  };

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      if (!data?.user) return setIsAdmin(false);
      supabase.from("profiles").select("role").eq("id", data.user.id).single()
        .then(({ data: p }) => {
          const ok = p?.role === "admin";
          setIsAdmin(ok);
          if (ok) load();
        });
    });
  }, []);

  // 같은 보호자 번호가 몇 명의 학생에게 등록됐는지 (반려 제외)
  const phoneCount = {};
  (rows || []).forEach((r) => {
    if (r.status === "rejected") return;
    phoneCount[r.guardian_phone] = (phoneCount[r.guardian_phone] || 0) + 1;
  });

  const approve = async (r) => {
    if (busy) return; setBusy(true); setMsg(""); setErr("");
    const { data: { user } } = await supabase.auth.getUser();
    const { error } = await supabase.from("guardian_consents").update({
      status: "active", approved_by: user?.id || null,
      approved_at: new Date().toISOString(), reject_reason: null,
      updated_at: new Date().toISOString(),
    }).eq("id", r.id);
    setBusy(false);
    if (error) setErr("승인 실패: " + error.message);
    else { setMsg(`「${r.guardian_name}」 승인 완료`); load(); }
  };

  const reject = async (r) => {
    const reason = window.prompt("반려 사유를 입력하세요 (학생 화면에 표시됩니다):", "보호자 확인 필요 — 학원으로 문의해주세요");
    if (reason == null) return;
    if (busy) return; setBusy(true); setMsg(""); setErr("");
    const { error } = await supabase.from("guardian_consents").update({
      status: "rejected", reject_reason: reason.trim() || null,
      updated_at: new Date().toISOString(),
    }).eq("id", r.id);
    setBusy(false);
    if (error) setErr("반려 실패: " + error.message);
    else { setMsg(`「${r.guardian_name}」 반려 처리 (5일 뒤 자동 파기)`); load(); }
  };

  const removeRow = async (r) => {
    if (!window.confirm(`「${r.guardian_name}」 보호자 정보를 지금 삭제할까요?\n되돌릴 수 없습니다.`)) return;
    setBusy(true); setMsg(""); setErr("");
    const { error } = await supabase.from("guardian_consents").delete().eq("id", r.id);
    setBusy(false);
    if (error) setErr("삭제 실패: " + error.message);
    else { setMsg("삭제 완료"); load(); }
  };

  if (isAdmin === false) return (
    <div className="ag-wrap"><style>{CSS}</style>
      <p className="ag-empty" style={{ paddingTop: 40, textAlign: "center" }}>관리자 전용 화면입니다.</p></div>
  );

  const view = (rows || []).filter((r) => r.status === tab);

  return (
    <div className="ag-wrap">
      <style>{CSS}</style>
      <div className="ag-head">
        <span className="ag-back" onClick={() => (location.hash = "")}>← 홈</span>
        <h1 className="ag-h1">🛡️ 보호자 승인</h1>
      </div>
      <p className="ag-desc">
        문자 인증을 마친 보호자 동의를 강사가 최종 확인합니다. 등록 상담 등에서 <b>실제 학부모임을 확인한 경우에만</b> 승인하세요.
        반려 건의 보호자 정보는 5일 뒤 자동 파기됩니다.
      </p>
      <div className="ag-tabs">
        {TABS.map(([v, l]) => (
          <button key={v} className={"ag-tab" + (tab === v ? " on" : "")} onClick={() => setTab(v)}>
            {l} <b>{(rows || []).filter((r) => r.status === v).length}</b>
          </button>
        ))}
      </div>
      {msg && <p className="ag-msg">{msg}</p>}
      {err && <p className="ag-msg ag-err">{err}</p>}

      {rows && view.length === 0 && <p className="ag-empty">해당 상태의 건이 없습니다.</p>}
      {view.map((r) => {
        const s = students[r.student_id];
        const multi = phoneCount[r.guardian_phone] >= 3;
        return (
          <div key={r.id} className="ag-item">
            <div className="ag-line">
              <span className="ag-stu">{s ? `${s.name}${s.grade ? ` (${s.grade})` : ""}` : r.student_id.slice(0, 8)}</span>
              <span className="ag-arrow">←</span>
              <span className="ag-gname">{r.guardian_name} <i>({r.relation}{r.guardian_birth_year ? ` · ${r.guardian_birth_year}년생` : ""})</i></span>
              <span className="ag-ph">{String(r.guardian_phone).replace(/(\d{3})(\d{3,4})(\d{4})/, "$1-$2-$3")}</span>
            </div>
            <div className="ag-line ag-sub">
              <span>동의 {r.consented_at ? new Date(r.consented_at).toLocaleString("ko-KR") : "-"}</span>
              {r.age_gap_warn && <span className="ag-warn">⚠ 나이 간극</span>}
              {multi && <span className="ag-warn">⚠ 다계정 ({phoneCount[r.guardian_phone]}명)</span>}
              {r.status === "rejected" && r.reject_reason && <span className="ag-warn">사유: {r.reject_reason}</span>}
              <span className="ag-sp" />
              {r.status === "pending" && (
                <>
                  <button className="ag-btn ag-ok" disabled={busy} onClick={() => approve(r)}>승인</button>
                  <button className="ag-btn ag-no" disabled={busy} onClick={() => reject(r)}>반려</button>
                </>
              )}
              {r.status === "active" && (
                <button className="ag-btn ag-no" disabled={busy} onClick={() => reject(r)}>연결 해제(반려)</button>
              )}
              {r.status === "rejected" && (
                <button className="ag-btn ag-no" disabled={busy} onClick={() => removeRow(r)}>즉시 파기</button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

const CSS = `
.ag-wrap { max-width: 720px; margin: 0 auto; padding: 24px 16px 64px; }
.ag-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 10px; }
.ag-h1 { font-size: 1.3rem; margin: 0; }
.ag-back { cursor: pointer; opacity: .65; font-size: .9rem; }
.ag-back:hover { opacity: 1; }
.ag-desc { font-size: .84rem; opacity: .75; line-height: 1.6; margin: 0 0 12px; }
.ag-tabs { display: flex; gap: 6px; margin-bottom: 12px; }
.ag-tab { border: 1px solid rgba(127,127,127,.3); background: transparent; color: inherit;
  border-radius: 999px; padding: 6px 12px; font-size: .82rem; cursor: pointer; opacity: .7; }
.ag-tab.on { border-color: rgba(20,164,148,.7); color: #16a08f; opacity: 1; font-weight: 700; }
.ag-msg { font-size: .84rem; margin: 6px 0; color: #16a08f; }
.ag-err { color: #e05252; }
.ag-empty { font-size: .85rem; opacity: .6; }
.ag-item { border: 1px solid rgba(127,127,127,.22); background: rgba(127,127,127,.05);
  border-radius: 12px; padding: 10px 12px; margin-bottom: 10px; }
.ag-line { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; font-size: .88rem; }
.ag-sub { margin-top: 6px; font-size: .76rem; opacity: .8; }
.ag-stu { font-weight: 700; }
.ag-arrow { opacity: .4; }
.ag-gname i { font-style: normal; opacity: .6; font-size: .8rem; }
.ag-ph { opacity: .6; font-size: .8rem; }
.ag-warn { color: #d97706; font-weight: 700; }
.ag-sp { flex: 1; }
.ag-btn { border-radius: 9px; padding: 5px 12px; font-size: .8rem; cursor: pointer;
  border: 1px solid rgba(127,127,127,.3); background: rgba(127,127,127,.08); color: inherit; }
.ag-btn:disabled { opacity: .45; cursor: default; }
.ag-ok { background: rgba(20,164,148,.16); border-color: rgba(20,164,148,.5); }
.ag-ok:not(:disabled):hover { background: rgba(20,164,148,.26); }
.ag-no { background: rgba(244,99,99,.1); border-color: rgba(244,99,99,.4); }
.ag-no:not(:disabled):hover { background: rgba(244,99,99,.2); }
`;
