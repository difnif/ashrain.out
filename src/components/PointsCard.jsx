// src/components/PointsCard.jsx — 마이페이지 「포인트」 카드 (mp-* 스타일 재사용)
import { useEffect, useState } from "react";
import { api, quickCheckCode, normCode, codeRoleType } from "../lib/authx";

const REASON_LABEL = {
  coupon: "쿠폰 충전",
  admin_grant: "선생님 지급",
  "spend:hint": "힌트 사용",
  "spend:find": "AI 개념찾기",
  "spend:omr": "OMR 인식",
  adjust: "조정",
};

export default function PointsCard() {
  const [balance, setBalance] = useState(null);
  const [coupon, setCoupon] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [rows, setRows] = useState(null);      // null = 접힘

  const loadBalance = async () => {
    try {
      const r = await api("points", { action: "balance" }, { auth: true });
      setBalance(r.balance);
    } catch { setBalance(0); }
  };
  useEffect(() => { loadBalance(); }, []);

  const redeem = async () => {
    setMsg(""); setBusy(true);
    try {
      if (!quickCheckCode(coupon)) throw new Error("쿠폰 번호를 다시 확인해주세요");
      if (codeRoleType(coupon) !== 7) throw new Error("포인트 쿠폰이 아니에요. (가입 코드는 회원가입에서 사용)");
      const r = await api("points", { action: "redeem", member_code: normCode(coupon) }, { auth: true });
      setBalance(r.balance);
      setCoupon("");
      setMsg(`✓ ${r.added.toLocaleString()}P가 충전됐어요.`);
      if (rows) loadHistory();
    } catch (e) { setMsg("⚠ " + (e.message || String(e))); }
    setBusy(false);
  };

  const loadHistory = async () => {
    try {
      const r = await api("points", { action: "history", limit: 10 }, { auth: true });
      setRows(r.rows || []);
    } catch (e) { setMsg("⚠ " + (e.message || String(e))); }
  };

  return (
    <div className="mp-card">
      <p className="mp-sec">포인트</p>

      <div className="mp-tgl" style={{ paddingTop: 0 }}>
        <span>보유 포인트<small>무료 한도를 다 쓴 뒤 AI 기능에 사용돼요</small></span>
        <b style={{ color: "var(--ink)", fontSize: 18 }}>
          {balance === null ? "…" : `${balance.toLocaleString()}P`}
        </b>
      </div>

      <div className="mp-row">
        <input className="mp-in" value={coupon} onChange={(e) => setCoupon(e.target.value)}
          placeholder="쿠폰 번호 (ASH37-7…)" autoCapitalize="characters" style={{ marginBottom: 0 }} />
        <button className="mp-mini" disabled={busy || !coupon.trim()} onClick={redeem}
          style={{ flex: "0 0 auto" }}>등록</button>
      </div>

      {rows === null ? (
        <button className="mp-mini" style={{ marginTop: 8 }} onClick={loadHistory}>사용 내역 보기</button>
      ) : (
        <div style={{ marginTop: 8 }}>
          {rows.length === 0 && <p className="mp-msg" style={{ color: "var(--mut)" }}>아직 내역이 없어요.</p>}
          {rows.map((r, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between",
              fontSize: 12.5, padding: "6px 2px", borderTop: "1px solid var(--inbd)" }}>
              <span style={{ color: "var(--mut)" }}>
                {REASON_LABEL[r.reason] || r.reason}
                {" · "}{new Date(r.created_at).toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" })}
              </span>
              <b style={{ color: r.delta > 0 ? "var(--ac)" : "var(--ink)" }}>
                {r.delta > 0 ? "+" : ""}{r.delta.toLocaleString()}P
              </b>
            </div>
          ))}
        </div>
      )}

      {msg && <p className={"mp-msg" + (msg.startsWith("✓") ? "" : " mp-err")}>{msg}</p>}
    </div>
  );
}
