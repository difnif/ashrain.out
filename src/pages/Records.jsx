// 기록 탭 (#/records) — 촬영 학습 기록(기기 보관소)을 셸(탭바) 안에서 본다.
// 진행 중인 판독 잡도 여기서 보인다(백그라운드 판독 — 화면을 떠나도 계속, 끝나면 여기로).
// 구 게시판 탭 자리(사용자 확정 2026-09-20). 게시판(#/board)은 라우트만 잠들어 있고, 종성 작업 때 재공개.
import { useEffect, useState } from "react";
import PhotoMine from "./photo/PhotoMine";
import { runningJobs, cancelJob, markJobsSeen } from "../lib/photoJobs";
import "./solve/solve.css";
import "./photo/photo.css";

const CSS = `
.rc-root { min-height: 100vh; padding: 14px 14px 96px; box-sizing: border-box; color: var(--text);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.rc-wrap { max-width: 680px; margin: 0 auto; }
.rc-h { margin: 2px 2px 12px; font-size: 17px; font-weight: 800; }
.rc-jobs { border: 1px solid var(--border); border-radius: 12px; padding: 10px 12px; margin-bottom: 12px;
  background: var(--surface); display: flex; flex-direction: column; gap: 8px; }
.rc-job { display: flex; align-items: center; gap: 8px; font-size: 12.5px; }
.rc-job .sp2 { flex: none; width: 12px; height: 12px; border-radius: 999px; border: 2px solid var(--accent);
  border-top-color: transparent; animation: rc-spin .9s linear infinite; }
.rc-job .tx { flex: 1; line-height: 1.5; }
.rc-job button { flex: none; background: none; border: 1px solid var(--border); border-radius: 999px; color: var(--muted);
  font-size: 11px; font-weight: 700; padding: 4px 10px; cursor: pointer; font-family: inherit; }
@keyframes rc-spin { to { transform: rotate(360deg); } }
`;

export default function Records() {
  const [, setT] = useState(0);
  useEffect(() => {
    const on = () => setT((t) => t + 1);
    window.addEventListener("ash:jobs", on);
    return () => window.removeEventListener("ash:jobs", on);
  }, []);
  useEffect(() => { markJobsSeen(); });   // 보고 있는 동안 끝난 잡도 본 것으로
  const running = runningJobs();
  return (
    <div className="rc-root">
      <style>{CSS}</style>
      <div className="rc-wrap">
        <p className="rc-h">🗂 기록</p>
        {running.length > 0 && (
          <div className="rc-jobs">
            {running.map((j) => (
              <div key={j.id} className="rc-job">
                <span className="sp2" aria-hidden="true" />
                <span className="tx"><b>{j.title}</b> — {j.progress?.label || "진행 중…"} <span style={{ color: "var(--muted)" }}>끝나면 여기에 저장돼요. 브라우저를 닫으면 멈춰요.</span></span>
                <button onClick={() => cancelJob(j.id)}>취소</button>
              </div>
            ))}
          </div>
        )}
        <PhotoMine embed />
      </div>
    </div>
  );
}
