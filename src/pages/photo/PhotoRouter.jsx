// 촬영 모듈 — #/solve/photo/* (SolveRouter 가 case "photo" 로 넘긴다)
//   #/solve/photo            허브 (네 기능 + 내 기록)
//   #/solve/photo/read       문장 이해하기   (?cur=1: 방금 찍은 문제로)
//   #/solve/photo/mark       표시 연습하기   (?cur=1)
//   #/solve/photo/essay      서술형 채점·첨삭 (?cur=1)
//   #/solve/photo/check      풀이과정 검사
//   #/solve/photo/mine       내 기록 (이 기기)
// 원칙: 사진·문항 문장은 서버에 저장하지 않는다. 답안 원문은 보관 게이트(app_settings.photo_retention)에 따라 기기/서버.
import { lazy, Suspense, useEffect, useState } from "react";
import SolveShell from "../solve/SolveShell";
import { listSessions } from "../../lib/deviceStore";
import { EmptyArt, FEATURE_LABEL, FEATURE_ICON, fmtWhen } from "./shared";
import "./photo.css";

const PhotoRead = lazy(() => import("./PhotoRead"));
const PhotoMark = lazy(() => import("./PhotoMark"));
const PhotoEssay = lazy(() => import("./PhotoEssay"));
const PhotoCheck = lazy(() => import("./PhotoCheck"));
const PhotoMine = lazy(() => import("./PhotoMine"));

const TILES = [
  { ic: "🔍", tt: "문장 이해하기", ds: "단서에 형광펜을 치고 끊어 읽으며 식 세우기까지. 답은 직접 구해요.", to: "#/solve/photo/read" },
  { ic: "✍️", tt: "표시 연습하기", ds: "동그라미·밑줄·물결·빗금을 어디에 칠지 차례대로 보여 줘요.", to: "#/solve/photo/mark" },
  { ic: "📝", tt: "서술형 채점·첨삭", ds: "문제와 답안을 찍으면 기준표로 채점하고 고칠 곳을 짚어 줘요.", to: "#/solve/photo/essay" },
  { ic: "🧾", tt: "풀이과정 검사", ds: "문제집 한 쪽을 찍으면 식의 연결·암산·글씨 습관을 신호등으로 봐요.", to: "#/solve/photo/check" },
];

const GUIDE = [
  { t: "문제를 찍어요", d: "문항 하나가 꽉 차게, 그림자 없이." },
  { t: "무엇을 할지 골라요", d: "문장 읽기 · 표시 연습 · 채점 · 풀이 검사." },
  { t: "결과는 이 기기에 남아요", d: "사진은 인식에만 쓰고 서버에 저장하지 않아요." },
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
  const [recent, setRecent] = useState(undefined);      // undefined = 아직 읽는 중
  useEffect(() => {
    let alive = true;
    listSessions({ limit: 3 }).then((r) => alive && setRecent(r || [])).catch(() => alive && setRecent([]));
    return () => { alive = false; };
  }, []);
  const first = Array.isArray(recent) && recent.length === 0;

  return (
    <SolveShell title="찍어서 배우기" sub="문제를 찍으면 문장 읽기부터 채점·첨삭까지. 사진은 서버에 남지 않아요.">
      {first && (
        <div className="sv-card">
          <div className="sv-sec" style={{ marginTop: 0 }}>처음이라면 <span className="sv-small">· 세 걸음이면 돼요</span></div>
          <div className="ph-guide">
            {GUIDE.map((g, i) => (
              <div key={g.t} className="st"><span className="no">{i + 1}</span><span className="tx"><b>{g.t}</b><span>{g.d}</span></span></div>
            ))}
          </div>
        </div>
      )}

      <div className="sv-grid2">
        {TILES.map((t) => (
          <button key={t.to} className="sv-tile" onClick={() => { location.hash = t.to; }}>
            <span className="ic">{t.ic}</span><span className="tt">{t.tt}</span><span className="ds">{t.ds}</span>
          </button>
        ))}
      </div>

      <div className="sv-sec">내 기록 <span className="sv-small">· 이 기기에만 남아요</span></div>
      {recent === undefined && <div className="sv-muted">불러오는 중…</div>}
      {first && (
        <div className="ph-blank">
          <EmptyArt kind="shot" />
          <div className="tt">아직 찍은 문제가 없어요</div>
          <div className="ds">문제 하나를 찍어 보면 여기에 기록이 쌓여요.<br />답안 원문과 첨삭 결과는 이 기기에만 남아요.</div>
          <div className="ph-actions">
            <button className="sv-btn pri" onClick={() => { location.hash = "#/solve/photo/read"; }}>첫 문제 찍어 보기</button>
          </div>
        </div>
      )}
      {Array.isArray(recent) && recent.length > 0 && (
        <>
          <div className="sv-list">
            {recent.map((r) => (
              <button key={r.id} className="ph-rec" onClick={() => { location.hash = "#/solve/photo/mine"; }}>
                {r.thumb ? <img className="th" src={r.thumb} alt="" /> : <span className="ic" aria-hidden="true">{FEATURE_ICON[r.feature] || "📄"}</span>}
                <span className="tx"><div className="tt">{r.title || "(제목 없음)"}</div><div className="dt">{FEATURE_LABEL[r.feature] || r.feature} · {fmtWhen(r.at)}</div></span>
                <span className="rt">보기</span>
              </button>
            ))}
          </div>
          <button className="sv-item" style={{ marginTop: 8 }} onClick={() => { location.hash = "#/solve/photo/mine"; }}>
            <span className="no">🗂️</span><span className="tx">내 기록 — 이 기기에 남은 답안과 첨삭 결과</span><span className="rt">모두 보기</span>
          </button>
        </>
      )}

      <p className="sv-small" style={{ marginTop: 14, lineHeight: 1.7 }}>
        사진과 문제 문장은 인식에만 쓰고 서버에 저장하지 않아요. 답안 원문과 첨삭 결과는 이 기기에 남고, 서버에는 점수·유형 같은 라벨만 남아요.
        문항 표현이 표준형인 경우에만(설정에 따라) 답안이 학습 기록으로 저장될 수 있어요.
      </p>
    </SolveShell>
  );
}
