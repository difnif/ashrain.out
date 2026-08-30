// src/shared/RoleSwitch.jsx — 보유 역할이 2개 이상일 때만 나타나는 전환기 (프로필·셸 헤더 공용)
import { useEffect, useState } from "react";
import { getMemberships, switchRole, ROLE_LABELS } from "./roles";

export default function RoleSwitch({ current }) {
  const [roles, setRoles] = useState(null);
  useEffect(() => {
    let alive = true;
    getMemberships().then((ms) => { if (alive) setRoles(ms.map((m) => m.role)); });
    return () => { alive = false; };
  }, []);
  if (!roles || roles.length < 2) return null;
  return (
    <div style={{ display: "flex", gap: 6, alignItems: "center", flexWrap: "wrap", margin: "0 0 14px" }}>
      <span style={{ fontSize: 12, color: "var(--mut)", fontWeight: 700 }}>역할</span>
      {roles.map((r) => (
        <button key={r} onClick={() => r !== current && switchRole(r)}
          style={{
            fontFamily: "inherit", cursor: r === current ? "default" : "pointer",
            background: r === current ? "var(--ac)" : "var(--card)",
            color: r === current ? "var(--bg, #0B0C0F)" : "var(--ink)",
            border: "1px solid " + (r === current ? "var(--ac)" : "var(--bd)"),
            borderRadius: 999, fontSize: 12, fontWeight: 700, padding: "6px 11px",
          }}>
          {ROLE_LABELS[r] || r}
        </button>
      ))}
    </div>
  );
}
