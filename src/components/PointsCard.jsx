// src/components/PointsCard.jsx — 마이페이지 「지갑」 카드 (mp-* 스타일 재사용)
// Ⓟ Ash(유료 기능용, 쿠폰·지급 충전) · Ⓓ Drop(복습 보상, 추후 숍). 두 재화는 서로 바꿀 수 없다. 결제 UI 없음.
import { useEffect, useState } from "react";
import { api, quickCheckCode, normCode, codeRoleType } from "../lib/authx";
import { CURRENCY, getBalances, getHistory, onPoints, reasonLabel } from "../lib/wallet";

export default function PointsCard() {
  const [bal, setBal] = useState(null);       // { ash, drop, ready }
  const [coupon, setCoupon] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [rows, setRows] = useState(null);     // null = 접힘
  const [tab, setTab] = useState("all");      // all | ash | drop

  const load = async () => setBal((await getBalances()) || { ash: 0, drop: 0, ready: false });
  useEffect(() => { load(); return onPoints(() => load()); }, []);

  const redeem = async () => {
    setMsg(""); setBusy(true);
    try {
      if (!quickCheckCode(coupon)) throw new Error("쿠폰 번호를 다시 확인해주세요");
      if (codeRoleType(coupon) !== 7) throw new Error("포인트 쿠폰이 아니에요. (가입 코드는 회원가입에서 사용)");
      const r = await api("points", { action: "redeem", member_code: normCode(coupon) }, { auth: true });
      setBal((b) => ({ ...(b || { drop: 0, ready: false }), ash: r.ash ?? r.balance }));
      setCoupon("");
      setMsg(`✓ Ⓟ ${r.added.toLocaleString()}이 충전됐어요.`);
      if (rows) loadHistory(tab);
    } catch (e) { setMsg("⚠ " + (e.message || String(e))); }
    setBusy(false);
  };

  const loadHistory = async (t = tab) => {
    try { setRows(await getHistory({ limit: 15, currency: t === "all" ? undefined : t })); }
    catch (e) { setMsg("⚠ " + (e.message || String(e))); }
  };

  const Bal = ({ cur }) => (
    <div style={{ flex: 1, background: "var(--in)", border: "1px solid var(--inbd)", borderRadius: 12, padding: "10px 12px" }}>
      <div style={{ fontSize: 12, color: "var(--mut)", fontWeight: 700 }}>{CURRENCY[cur].sym} {CURRENCY[cur].label}</div>
      <div style={{ fontSize: 20, fontWeight: 800, color: "var(--ink)", margin: "2px 0" }}>
        {bal === null ? "…" : Number(bal[cur] || 0).toLocaleString()}
      </div>
      <div style={{ fontSize: 11.5, color: "var(--mut)", lineHeight: 1.5 }}>{CURRENCY[cur].desc}</div>
    </div>
  );

  return (
    <div className="mp-card">
      <p className="mp-sec">지갑</p>
      <div style={{ display: "flex", gap: 8 }}>
        <Bal cur="ash" /><Bal cur="drop" />
      </div>
      {bal && !bal.ready && (
        <p className="mp-msg" style={{ color: "var(--mut)" }}>Ⓓ Drop은 준비 중이에요 — 곧 복습 보상이 쌓여요.</p>
      )}
      <p className="mp-msg" style={{ color: "var(--mut)", marginTop: 6 }}>두 포인트는 서로 바꿀 수 없어요. 숍은 준비 중이에요.</p>

      <div className="mp-row" style={{ marginTop: 8 }}>
        <input className="mp-in" value={coupon} onChange={(e) => setCoupon(e.target.value)}
          placeholder="Ⓟ 쿠폰 번호 (ASH37-7…)" autoCapitalize="characters" style={{ marginBottom: 0 }} />
        <button className="mp-mini" disabled={busy || !coupon.trim()} onClick={redeem}
          style={{ flex: "0 0 auto" }}>등록</button>
      </div>

      {rows === null ? (
        <button className="mp-mini" style={{ marginTop: 8 }} onClick={() => loadHistory("all")}>내역 보기</button>
      ) : (
        <div style={{ marginTop: 8 }}>
          <div style={{ display: "flex", gap: 6, marginBottom: 6 }}>
            {[["all", "전체"], ["ash", "Ⓟ"], ["drop", "Ⓓ"]].map(([k, l]) => (
              <button key={k} className="mp-mini" style={{ opacity: tab === k ? 1 : .6 }}
                onClick={() => { setTab(k); loadHistory(k); }}>{l}</button>
            ))}
          </div>
          {rows.length === 0 && <p className="mp-msg" style={{ color: "var(--mut)" }}>아직 내역이 없어요.</p>}
          {rows.map((r, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between",
              fontSize: 12.5, padding: "6px 2px", borderTop: "1px solid var(--inbd)" }}>
              <span style={{ color: "var(--mut)" }}>
                {reasonLabel(r.reason)}
                {" · "}{new Date(r.created_at).toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" })}
              </span>
              <b style={{ color: r.delta > 0 ? "var(--ac)" : "var(--ink)" }}>
                {r.delta > 0 ? "+" : ""}{r.delta.toLocaleString()} {CURRENCY[r.currency || "ash"]?.sym}
              </b>
            </div>
          ))}
        </div>
      )}

      {msg && <p className={"mp-msg" + (msg.startsWith("✓") ? "" : " mp-err")}>{msg}</p>}
    </div>
  );
}
