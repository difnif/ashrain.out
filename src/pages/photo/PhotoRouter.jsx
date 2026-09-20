// 촬영 모듈 — #/solve/photo/* (SolveRouter 가 case "photo" 로 넘긴다)
//   #/solve/photo            허브 (네 기능 + 내 기록)
//   #/solve/photo/read       문장 이해하기   (?cur=1: 방금 찍은 문제로)
//   #/solve/photo/mark       표시 연습하기   (?cur=1)
//   #/solve/photo/essay      서술형 채점·첨삭 (?cur=1)
//   #/solve/photo/check      풀이과정 검사
//   #/solve/photo/mine       내 기록 (이 기기)
// 원칙: 사진·문항 문장은 서버에 저장하지 않는다. 답안 원문은 보관 게이트(app_settings.photo_retention)에 따라 기기/서버.
import { lazy, Suspense } from "react";
import SolveShell from "../solve/SolveShell";
import "./photo.css";

const PhotoRead = lazy(() => import("./PhotoRead"));
const PhotoMark = lazy(() => import("./PhotoMark"));
const PhotoEssay = lazy(() => import("./PhotoEssay"));
const PhotoCheck = lazy(() => import("./PhotoCheck"));
const PhotoMine = lazy(() => import("./PhotoMine"));

const TILES = [
  { ic: "🔍", tt: "문장 이해하기", ds: "문제를 찍으면 단서에 형광펜을 치고 끊어 읽으며, 식을 세우는 데까지만 함께 해요.", to: "#/solve/photo/read" },
  { ic: "✍️", tt: "표시 연습하기", ds: "동그라미·밑줄·물결·빗금을 어디에 칠지 차례대로 보여 주고, 문장 이해하기로 이어져요.", to: "#/solve/photo/mark" },
  { ic: "📝", tt: "서술형 채점·첨삭", ds: "문제와 내 답안을 찍으면 채점 기준표로 채점하고 어디를 어떻게 고칠지 알려 줘요.", to: "#/solve/photo/essay" },
  { ic: "🧾", tt: "풀이과정 검사", ds: "문제집 페이지를 찍고 영역을 잡으면 식의 연결·암산·글씨 습관을 신호등으로 봐요.", to: "#/solve/photo/check" },
];

export default function PhotoRouter({ sub = "", hash = "" }) {
  const seg = (sub || "").split("?")[0].split("/")[0];
  const q = new URLSearchParams((hash.split("?")[1] || ""));
  const useCur = q.get("cur") === "1";
  let el;
  switch (seg) {
    case "read": el = <PhotoRead key={hash} useCur={useCur} />; break;
    case "mark": el = <PhotoMark key={hash} useCur={useCur} />; break;
    case "essay": el = <PhotoEssay key={hash} useCur={useCur} />; break;
    case "check": el = <PhotoCheck />; break;
    case "mine": el = <PhotoMine />; break;
    default: el = <PhotoHub />;
  }
  return <Suspense fallback={<div className="sv-wrap sv-muted">불러오는 중…</div>}>{el}</Suspense>;
}

export function PhotoHub() {
  return (
    <SolveShell title="찍어서 배우기" sub="문제를 찍으면 문장 읽기부터 채점·첨삭까지. 사진은 서버에 남지 않아요.">
      <div className="sv-grid2">
        {TILES.map((t) => (
          <button key={t.to} className="sv-tile" onClick={() => { location.hash = t.to; }}>
            <span className="ic">{t.ic}</span><span className="tt">{t.tt}</span><span className="ds">{t.ds}</span>
          </button>
        ))}
      </div>
      <div className="sv-sec">기록</div>
      <button className="sv-item" onClick={() => { location.hash = "#/solve/photo/mine"; }}>
        <span className="no">🗂️</span><span className="tx">내 기록 — 이 기기에 남은 답안과 첨삭 결과</span><span className="rt">열기</span>
      </button>
      <p className="sv-small" style={{ marginTop: 14, lineHeight: 1.7 }}>
        사진과 문제 문장은 인식에만 쓰고 서버에 저장하지 않아요. 답안 원문과 첨삭 결과는 이 기기에 남고, 서버에는 점수·유형 같은 라벨만 남아요.
        문항 표현이 표준형인 경우에만(설정에 따라) 답안이 학습 기록으로 저장될 수 있어요.
      </p>
    </SolveShell>
  );
}
