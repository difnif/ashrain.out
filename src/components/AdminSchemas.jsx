// ashrain.out — 스키마 승인대 (AdminSchemas.jsx v1.0, #/admin/schemas)
// 마이닝 산출물을 스키마 단위로 입법: 승인/반려(사유)/등급 조정/생산 배정(chat·local)
// P1 원칙 — 문항 개별 검토가 아니라 규칙(스키마) 단위 결정만 한다.

import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";
import { renderText } from "../lib/mathir";

const UNITS = ["m1-1","m1-2","m2-1","m2-2","m3-1","m3-2","h1-1","h1-2","h2-1","h2-2","h3-1","h3-2","h3-3"];
const ST = { draft: "채굴됨", fit_ok: "적합", fit_fail: "적합실패", approved: "승인", rejected: "반려" };

export default function AdminSchemas() {
  const [authed, setAuthed] = useState(null);
  const [unit, setUnit] = useState("all");
  const [st, setSt] = useState("all");
  const [rows, setRows] = useState([]);
  const [counts, setCounts] = useState({});
  const [msg, setMsg] = useState("");

  useEffect(() => { supabase.auth.getSession().then(({ data }) => setAuthed(!!data.session)); }, []);

  async function load() {
    let q = supabase.from("schemas").select("*").order("unit_id").order("src_tag").limit(300);
    if (unit !== "all") q = q.eq("unit_id", unit);
    if (st !== "all") q = q.eq("status", st);
    const { data, error } = await q;
    if (error) { setMsg("로드 실패: " + error.message); return; }
    setRows(data || []);
    const { data: all } = await supabase.from("schemas").select("status");
    const c = {};
    (all || []).forEach((r) => { c[r.status] = (c[r.status] || 0) + 1; });
    setCounts(c);
  }
  useEffect(() => { if (authed) load(); }, [authed, unit, st]);  // eslint-disable-line

  async function setField(id, patch, note) {
    const { error } = await supabase.from("schemas")
      .update({ ...patch, decided_at: new Date().toISOString() }).eq("id", id);
    setMsg(error ? "실패: " + error.message : note);
    if (!error) load();
  }
  const approve = (r) => setField(r.id, { status: "approved" }, `승인 — ${r.name || r.src_tag}`);
  const reject = (r) => {
    const why = window.prompt("반려 사유 (규칙 증류의 원료가 됩니다):", r.note || "");
    if (why === null) return;
    setField(r.id, { status: "rejected", note: why }, `반려 — ${r.src_tag}`);
  };

  if (authed === false) return <div className="sk-wrap"><style>{CSS}</style><p className="sk-note">관리자 로그인 필요 — 코퍼스 화면에서 로그인 후 새로고침.</p></div>;
  return (
    <div className="sk-wrap">
      <style>{CSS}</style>
      <h2>스키마 승인대</h2>
      <div className="sk-row">
        <select value={unit} onChange={(e) => setUnit(e.target.value)}>
          <option value="all">전 단원</option>
          {UNITS.map((u) => <option key={u} value={u}>{u}</option>)}
        </select>
        {["all", "draft", "fit_ok", "approved", "rejected"].map((k) => (
          <button key={k} className={"sk-chip" + (st === k ? " on" : "")} onClick={() => setSt(k)}>
            {k === "all" ? "전체" : ST[k]}{k !== "all" && counts[k] ? ` ${counts[k]}` : ""}
          </button>
        ))}
        <span className="sk-note" style={{ marginLeft: "auto" }}>{msg || `${rows.length}건`}</span>
      </div>

      {rows.map((r) => (
        <div key={r.id} className="sk-card">
          <div className="sk-row">
            <b>{r.name || "(이름 없음)"}</b>
            <span className={"sk-badge g" + (r.grade || "")}>{r.grade || "?"}급</span>
            <span className="sk-badge">{ST[r.status] || r.status}</span>
            {r.ir_errs > 0 && <span className="sk-badge warn">IR오류 {r.ir_errs}</span>}
            <span className="sk-note">{r.unit_id} · 「{r.src_tag}」 · 표본 {r.n_items}</span>
          </div>
          {(r.relations || []).length > 0 && (
            <p className="sk-rel">{(r.relations || []).map((x, i) => <span key={i} className="sk-ir">{safeIR(x)}</span>)}</p>
          )}
          {r.roles && <p className="sk-det">역할 — {Object.entries(r.roles).map(([k, v]) => `${k}: ${v}`).join(" · ")}</p>}
          {(r.axes || []).map((ax, i) => <p key={i} className="sk-det">변주축 [{ax.axis}] {(ax.values || []).join(" / ")}</p>)}
          {(r.implicit || []).length > 0 && <p className="sk-det">암묵 — {r.implicit.join(" · ")}</p>}
          {r.conditions && ["declarations", "singularities", "uniqueness"].map((k) =>
            (r.conditions[k] || []).length > 0 && <p key={k} className="sk-det cond">
              {{ declarations: "필수 선언", singularities: "특이점 배제", uniqueness: "유일성" }[k]} — {r.conditions[k].join(" · ")}</p>)}
          {r.note && <p className="sk-det" style={{ color: "#fbbf24" }}>메모 — {r.note}</p>}
          <div className="sk-row" style={{ marginTop: 8 }}>
            {r.status !== "approved" && <button className="sk-btn ok" onClick={() => approve(r)}>승인</button>}
            {r.status !== "rejected" && <button className="sk-btn" onClick={() => reject(r)}>반려</button>}
            <select value={r.grade || ""} onChange={(e) => setField(r.id, { grade: e.target.value }, "등급 변경")}>
              {["A", "B", "C"].map((g) => <option key={g} value={g}>{g}급</option>)}
            </select>
            <select value={r.assignee || ""} onChange={(e) => setField(r.id, { assignee: e.target.value || null }, "배정 변경")}>
              <option value="">배정 없음</option><option value="chat">채팅(Claude)</option><option value="local">로컬 GPU</option>
            </select>
          </div>
        </div>
      ))}
      {rows.length === 0 && <p className="sk-note">표시할 스키마 없음 — mine_schemas.py로 채굴부터.</p>}
    </div>
  );
}

function safeIR(x) {
  try { return renderText(String(x)); } catch { return String(x); }
}

const CSS = `
.sk-wrap{max-width:820px;margin:0 auto;padding:18px 14px 60px;color:#e2e8f0;background:#0f172a;min-height:100vh}
.sk-wrap h2{font-size:18px;margin:0 0 12px}
.sk-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:6px 0}
.sk-wrap select{padding:7px 8px;border:1px solid #334155;border-radius:8px;background:#1e293b;color:#e2e8f0;font-size:13px}
.sk-chip{padding:6px 10px;border:1px solid #334155;border-radius:999px;background:#1e293b;color:#cbd5e1;font-size:12.5px;cursor:pointer}
.sk-chip.on{background:#334155;color:#fff}
.sk-card{border:1px solid #1e293b;background:#111c31;border-radius:12px;padding:12px;margin:10px 0}
.sk-badge{font-size:11.5px;padding:2px 8px;border-radius:999px;background:#1e293b;color:#93c5fd}
.sk-badge.gA{background:#064e3b;color:#6ee7b7}.sk-badge.gB{background:#1e3a8a;color:#93c5fd}.sk-badge.gC{background:#3f1d1d;color:#fca5a5}
.sk-badge.warn{background:#78350f;color:#fcd34d}
.sk-rel{margin:8px 0 4px;display:flex;flex-wrap:wrap;gap:6px}
.sk-ir{background:#0b1222;border:1px solid #26334d;border-radius:6px;padding:2px 8px;font-size:13.5px}
.sk-det{font-size:12.5px;color:#94a3b8;margin:3px 0}
.sk-det.cond{color:#c4b5fd}
.sk-note{font-size:12.5px;color:#64748b}
.sk-btn{padding:7px 12px;border:1px solid #334155;border-radius:8px;background:#1e293b;color:#e2e8f0;font-size:13px;cursor:pointer}
.sk-btn.ok{background:#065f46;border-color:#065f46}
`;
