// src/gate/Gate.jsx — 관문(/) 비로그인 화면: 소개 + 역할 선택
// 로그인 상태의 관문 처리는 PathRouter가 담당(마지막 역할로 즉시 이동).
// 베타(2026-09): 학생앱을 먼저 공개한다. 강사·학부모 앱은 막지 않되 "미리보기"로만 안내.
import { navigatePath } from "../shared/roles";
import { BETA } from "../lib/beta";

const OTHERS = [
  { label: "강사 (시록고)", desc: "학생을 살피고 지도해요 · 미리보기", path: "/seirocco" },
  { label: "학부모 (종성)", desc: "소식을 받고 응원을 보내요 · 미리보기", path: "/jongseong" },
];

export default function Gate() {
  return (
    <div className="ap-shell">
      <div className="ap-wrap" style={{ maxWidth: 440, paddingTop: 64, textAlign: "center" }}>
        <img src="/brand/ashrain_logo.png" alt="ashrain.out" style={{ height: 40, marginBottom: 10 }} />
        <p style={{ color: "var(--mut)", fontSize: 14, margin: "0 0 22px" }}>애쉬레인 수학 학습 플랫폼</p>

        <button className="ap-card" onClick={() => navigatePath("/walking")}
          style={{ cursor: "pointer", display: "block", width: "100%", textAlign: "left", fontFamily: "inherit",
            color: "var(--ink)", borderColor: "var(--ac)", borderWidth: 1.5, padding: "18px 18px 16px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
            <span style={{ fontSize: 18, fontWeight: 800, color: "var(--ac)" }}>학생으로 시작하기</span>
            {BETA.on && <span style={{ fontSize: 10.5, fontWeight: 800, color: "#fff", background: "#7C3AED", borderRadius: 999, padding: "2px 7px" }}>{BETA.label}</span>}
          </div>
          <div style={{ fontSize: 13.5, color: "var(--mut)", lineHeight: 1.6 }}>
            개념 카드로 배우고, 문제를 찍어 문장 해설·표시 연습·서술형 첨삭으로 익혀요.
          </div>
          <div style={{ marginTop: 10, fontSize: 13, fontWeight: 800, color: "var(--ac)" }}>시작 →</div>
        </button>

        <p style={{ color: "var(--mut)", fontSize: 12, margin: "22px 0 8px" }}>다른 앱 미리보기</p>
        <div style={{ display: "grid", gap: 8, textAlign: "left" }}>
          {OTHERS.map((r) => (
            <button key={r.path} className="ap-card" onClick={() => navigatePath(r.path)}
              style={{ cursor: "pointer", display: "flex", alignItems: "center", gap: 12, opacity: .85,
                fontFamily: "inherit", textAlign: "left", width: "100%", color: "var(--ink)", padding: "12px 14px" }}>
              <span style={{ fontSize: 14, fontWeight: 800, color: "var(--ink)", minWidth: 110 }}>{r.label}</span>
              <span style={{ fontSize: 12.5, color: "var(--mut)", lineHeight: 1.5 }}>{r.desc}</span>
            </button>
          ))}
        </div>
        <p style={{ color: "var(--mut)", fontSize: 12, marginTop: 24, lineHeight: 1.6 }}>
          이미 계정이 있어요? 역할을 고르면 로그인으로 이어져요.<br />{BETA.notice}
        </p>
      </div>
    </div>
  );
}
