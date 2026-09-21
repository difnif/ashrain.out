// 필기 습관 지도 UI — 촬영 전 주의 팝업(HwGuide) + 답안 사진 위 형광펜 교정(HwMarks)
// 규칙(사용자 확정): 엉망·연함은 다시 적기, 끄적임은 알아보기 어렵다고, 두 단은 한 단 서술 + 단 사이 화살표 종용.
import { HW_ADVICE, hwStrikes, HW_STRIKE_LIMIT, resetHwStrikes, muteHwGuide, markHwGuideShown } from "../../lib/hw";

/** 한 단 vs 두 단(화살표) 예시 그림 — 인라인 SVG */
function ColumnsArt() {
  const line = (x, y, w, o = 0.9) => <rect x={x} y={y} width={w} height={3} rx={1.5} fill="currentColor" opacity={o * 0.55} />;
  return (
    <svg viewBox="0 0 240 84" width="100%" height="84" aria-hidden="true" style={{ display: "block" }}>
      {/* 왼쪽: 한 단 (좋아요) */}
      <rect x={6} y={6} width={92} height={72} rx={8} fill="none" stroke="currentColor" opacity=".35" />
      {[18, 30, 42, 54, 66].map((y, i) => line(16, y, 64 - i * 6))}
      <text x={52} y={80} textAnchor="middle" fontSize="9" fill="currentColor" opacity=".8">한 단 ✓</text>
      {/* 오른쪽: 두 단 + 화살표 */}
      <rect x={122} y={6} width={112} height={72} rx={8} fill="none" stroke="currentColor" opacity=".35" />
      {[18, 30, 42].map((y, i) => line(130, y, 40 - i * 5))}
      {[18, 30, 42].map((y, i) => line(186, y, 38 - i * 4))}
      <path d="M158 46 C 158 60, 178 60, 182 22" fill="none" stroke="var(--accent)" strokeWidth="2.4" strokeLinecap="round" />
      <path d="M178 26 L182 20 L186 27" fill="none" stroke="var(--accent)" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" />
      <text x={178} y={80} textAnchor="middle" fontSize="9" fill="currentColor" opacity=".8">두 단이면 화살표로 잇기</text>
    </svg>
  );
}

/** 촬영 전 주의 팝업 — onClose() 는 닫힘 후 호출 */
export function HwGuide({ onClose }) {
  const strikes = hwStrikes();
  const nudged = strikes >= HW_STRIKE_LIMIT;
  const ok = () => { markHwGuideShown(); if (nudged) resetHwStrikes(); onClose?.(); };
  const mute = () => { markHwGuideShown(); if (nudged) resetHwStrikes(); muteHwGuide(30); onClose?.(); };
  return (
    <div className="ph-hwg" role="dialog" aria-modal="true" aria-label="필기 주의사항">
      <div className="dim" onClick={ok} />
      <div className="card">
        <div className="tt">{nudged ? `✍️ 필기 때문에 판독이 ${strikes}번 힘들었어요` : "✍️ 찍기 전에, 풀이 필기 약속 4가지"}</div>
        {nudged && <p className="ds">아래 약속만 지켜도 판독이 훨씬 정확해져요 — 한 번만 다시 볼게요.</p>}
        <ul className="rules">
          <li><b>또박또박</b> — 갈겨 쓴 글씨는 채점 선생님도, AI도 못 읽어요.</li>
          <li><b>진하게</b> — 너무 연한 글씨는 사진에서 사라져요.</li>
          <li><b>위에서 아래로 한 줄기</b> — 여기저기 끄적이면 풀이 흐름을 따라갈 수 없어요.</li>
          <li><b>두 단이 되면 화살표</b> — 첫 단 끝과 둘째 단 시작을 화살표로 이어 주세요.</li>
        </ul>
        <ColumnsArt />
        <div className="ph-actions" style={{ marginTop: 12 }}>
          <button className="sv-btn pri" onClick={ok}>알겠어요</button>
          <button className="sv-btn ghost" onClick={mute}>한 달 동안 보지 않기</button>
        </div>
      </div>
    </div>
  );
}

/** 답안 사진 위 형광펜 교정 — issues(box 비율 좌표) 를 노랗게 칠하고, 종류별 지도 문구를 붙인다 */
export function HwMarks({ thumb, issues = [] }) {
  const hw = issues.filter((i) => HW_ADVICE[i.kind]);
  if (!thumb || !hw.length) return null;
  return (
    <div className="ph-hwm">
      <div className="shot">
        <img src={thumb} alt="내 답안" />
        {hw.map((i, k) => i.box ? (
          <span key={k} className="hl" style={{ left: `${i.box.x * 100}%`, top: `${i.box.y * 100}%`, width: `${i.box.w * 100}%`, height: `${i.box.h * 100}%` }}>
            <i>{k + 1}</i>
          </span>
        ) : null)}
      </div>
      <div className="tips">
        {hw.map((i, k) => (
          <div key={k} className="tip">
            <span className="no">{i.box ? k + 1 : "!"}</span>
            <span><b>{HW_ADVICE[i.kind].nm}</b>{i.note ? ` — ${i.note}` : ""}<em>{HW_ADVICE[i.kind].tip}</em></span>
          </div>
        ))}
      </div>
    </div>
  );
}
