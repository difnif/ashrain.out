// src/gate/Gate.jsx — 관문(/) 비로그인 화면: 소개 + 역할 선택
// 로그인 상태의 관문 처리는 PathRouter가 담당(마지막 역할로 즉시 이동).
import { navigatePath } from "../shared/roles";

const ROLES = [
  { label: "학생", desc: "개념·연산·오답노트로 공부해요", path: "/walking" },
  { label: "강사", desc: "학생을 살피고 지도해요", path: "/seirocco" },
  { label: "학부모", desc: "주간 소식을 받고 응원을 보내요", path: "/jongseong" },
];

export default function Gate() {
  return (
    <div className="ap-shell">
      <div className="ap-wrap" style={{ maxWidth: 440, paddingTop: 72, textAlign: "center" }}>
        <img src="/brand/ashrain_logo.png" alt="ashrain.out" style={{ height: 40, marginBottom: 10 }} />
        <p style={{ color: "var(--mut)", fontSize: 14, margin: "0 0 28px" }}>애쉬레인 수학 학습 플랫폼</p>
        <div style={{ display: "grid", gap: 10, textAlign: "left" }}>
          {ROLES.map((r) => (
            <button key={r.path} className="ap-card" onClick={() => navigatePath(r.path)}
              style={{ cursor: "pointer", display: "flex", alignItems: "center", gap: 14,
                fontFamily: "inherit", textAlign: "left", width: "100%", color: "var(--ink)" }}>
              <span style={{ fontSize: 16, fontWeight: 800, color: "var(--ac)", minWidth: 52 }}>{r.label}</span>
              <span style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.5 }}>{r.desc}</span>
            </button>
          ))}
        </div>
        <p style={{ color: "var(--mut)", fontSize: 12, marginTop: 26 }}>
          이미 계정이 있어요? 역할을 고르면 로그인으로 이어져요.
        </p>
      </div>
    </div>
  );
}
