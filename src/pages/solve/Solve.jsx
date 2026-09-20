// 문제풀이 허브 (#/solve) — 학생앱 베타의 두 기둥 중 하나.
// 개념별 문항 세트 · 예제·유제 · 시험 보기 · 사진 채점(OMR) · 문장 해설 · 표시 연습 · 서술형 자가채점 · 찍어서 배우기(촬영 모듈) · 사진 힌트 · 스피드 연산
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import { BETA } from "../../lib/beta";
import { recentAttempts, summarizeAttempts } from "../../lib/items";
import { countOpenWrongNotes } from "../../lib/wrongnotes";
import { mcLabel } from "../../lib/misconceptions";
import { readLastResult } from "../../lib/setplay";
import ItemPicker from "./ItemPicker";
import SolveShell from "./SolveShell";
import "./solve.css";

const TILES = [
  { ic: "✏️", tt: "문제 풀기", ds: "개념을 고르고 문항 세트를 풀어요. 풀고 나면 해설과 도형 애니메이션이 열려요.", to: "#/solve/set" },
  { ic: "📖", tt: "예제·유제", ds: "개념 카드의 예제를 한 줄씩 따라가며 풀어요.", to: "#/solve/practice" },
  { ic: "🧪", tt: "시험 보기", ds: "개념 묶음·단원·연산·모의고사 등 8가지 시험을 시간 안에 풀고 결과를 남겨요.", to: "#/solve/test" },
  { ic: "📸", tt: "찰칵 채점", ds: "시험지를 뽑아 종이에 풀고, 답안 카드를 찍으면 채점돼요.", to: "#/solve/omr" },
  { ic: "🔍", tt: "문장 해설", ds: "문제 문장에서 숫자·척도·단서 경계를 짚고, 무엇을 구하는지 정리해요.", to: "#/solve/read" },
  { ic: "✍️", tt: "표시 연습", ds: "동그라미·밑줄·빗금으로 문제에 표시하는 습관을 연습해요.", to: "#/solve/mark" },
  { ic: "📝", tt: "서술형 자가채점", ds: "풀이를 쓰고 채점 기준표로 스스로 점수를 매겨 봐요.", to: "#/solve/essay" },
  { ic: "📸", tt: "찍어서 배우기", ds: "문제를 찍으면 문장 이해·표시 연습·서술형 첨삭·풀이과정 검사까지. 사진은 서버에 남지 않아요.", to: "#/solve/photo" },
  { ic: "🗝️", tt: "사진 힌트", ds: "막힌 문제를 찍으면 답 대신 첫걸음을 알려줘요.", to: "#/learn/hint" },
  { ic: "🧮", tt: "스피드 연산", ds: "제한 시간 안에 연산을 푸는 훈련이에요.", to: "#/learn/calc", key: "calc" },
];

export default function Solve() {
  const [uid, setUid] = useState(null);
  const [recent, setRecent] = useState(null);
  const [wrongN, setWrongN] = useState(null);
  const [calcReady, setCalcReady] = useState(null);
  const last = readLastResult();

  useEffect(() => {
    let alive = true;
    (async () => {
      const { data } = await supabase.auth.getUser();
      const id = data?.user?.id || null;
      if (!alive) return;
      setUid(id);
      if (!id) return;
      const [rows, wn] = await Promise.all([recentAttempts(id, { days: 7 }), countOpenWrongNotes(id)]);
      if (!alive) return;
      setRecent(summarizeAttempts(rows));
      setWrongN(wn);
    })();
    supabase.from("calc_units").select("id", { count: "exact", head: true })
      .then(({ count, error }) => { if (alive) setCalcReady(!error && (count || 0) > 0); });
    return () => { alive = false; };
  }, []);

  return (
    <SolveShell title={<>문제풀이{BETA.on && <span className="sv-badge beta">{BETA.label}</span>}</>} back={null}
      sub="개념을 익혔으면 여기서 풀어요. 풀이 기록은 오답노트와 이어져요.">
      {last && (
        <div className="sv-card flat">
          <div className="sv-row">
            <div style={{ flex: 1 }}>
              <div className="sv-small">최근 세트</div>
              <div style={{ fontWeight: 800 }}>{last.title || last.conceptId} · {last.ok}/{last.n} 정답</div>
            </div>
            <button className="sv-btn sm pri" onClick={() => (location.hash = `#/solve/set/${last.conceptId}`)}>같은 개념 새 세트</button>
          </div>
        </div>
      )}
      <div className="sv-grid2">
        {TILES.map((t) => {
          const soon = t.key === "calc" && calcReady === false;
          return (
            <button key={t.to} className={"sv-tile" + (soon ? " soon" : "")} disabled={soon}
              onClick={() => { if (!soon) location.hash = t.to; }}>
              <span className="ic">{t.ic}</span>
              <span className="tt">{t.tt}{soon && <span className="sv-badge" style={{ background: "var(--surface3)", color: "var(--muted)" }}>준비 중</span>}</span>
              <span className="ds">{t.ds}</span>
            </button>
          );
        })}
      </div>

      <div className="sv-sec">이번 주 기록</div>
      <div className="sv-card">
        {!uid ? <div className="sv-muted">로그인하면 기록이 쌓여요.</div>
        : recent === null ? <div className="sv-muted">불러오는 중…</div>
        : recent.n === 0 ? <div className="sv-muted">아직 푼 문항이 없어요. 첫 세트를 풀어 볼까요?</div>
        : (
          <>
            <div className="sv-row" style={{ gap: 18 }}>
              <Stat label="푼 문항" value={`${recent.n}개`} />
              <Stat label="정답률" value={`${recent.rate}%`} />
              <Stat label="오답노트" value={wrongN == null ? "…" : `${wrongN}개`} onClick={() => (location.hash = "#/learn/wrong")} />
            </div>
            {recent.topTags.length > 0 && (
              <div style={{ marginTop: 10 }}>
                <div className="sv-small" style={{ marginBottom: 4 }}>자주 나온 실수</div>
                <div className="sv-row wrap" style={{ gap: 6 }}>
                  {recent.topTags.map(([code, n]) => <span key={code} className="sv-chip bad">{mcLabel(code)} ×{n}</span>)}
                </div>
              </div>
            )}
          </>
        )}
      </div>
      <p className="sv-small" style={{ marginTop: 14, lineHeight: 1.6 }}>{BETA.notice} 불편한 점은 <a href={BETA.feedbackUrl} target="_blank" rel="noreferrer" style={{ color: "var(--accent)" }}>문의</a>로 알려 주세요.</p>
    </SolveShell>
  );
}

function Stat({ label, value, onClick }) {
  return (
    <div onClick={onClick} style={{ cursor: onClick ? "pointer" : "default" }}>
      <div className="sv-small">{label}</div>
      <div style={{ fontSize: 18, fontWeight: 800 }}>{value}</div>
    </div>
  );
}

/** 예제·유제 개념 고르기 (#/solve/practice) — practice_sets 는 개념마다 있으므로 수를 세지 않는다 */
export function PracticePick() {
  return (
    <SolveShell title="예제·유제" sub="개념을 고르면 그 개념의 예제·유제 풀이로 이어져요.">
      <ItemPicker mode="concept" counts={false} onPickConcept={(c) => (location.hash = `#/p/${encodeURIComponent(c.id)}`)} />
    </SolveShell>
  );
}

