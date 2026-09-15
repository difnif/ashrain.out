// src/components/ReviewCard.jsx — 홈 「오늘의 복습」 카드 내용물 (부모가 .hd-card wide 안에 놓는다)
// props: uid, profile(profiles 행 — grade 사용), concepts([{id, unit_id, title, sort_order}] — 없으면 첫 사용자일 때만 직접 불러온다)
// 최근 읽은 개념(localStorage ash.recentConcepts, 최대 5) 과 남은 보상 횟수를 보여 주고, 누르면 #/c/<id>?review=1 로 간다.
// 읽은 기록이 없으면 학년·학기 첫 개념(defaultConceptFor)을 권한다. hd-* 변수(--ink --mut --ac --card --bd)만 쓴다.
import { useEffect, useState } from "react";
import { getRecentConcepts, reviewStatus, defaultConceptFor, capForRank, DAILY_CAP, REWARD } from "../lib/review";
import { listConcepts } from "../lib/concepts";

const rowStyle = {
  display: "flex", alignItems: "center", gap: 10, width: "100%", textAlign: "left", cursor: "pointer",
  background: "var(--card)", border: "1px solid var(--bd)", borderRadius: 12, padding: "9px 11px", color: "var(--ink)",
  fontFamily: "inherit",
};
const badge = (bg) => ({
  flex: "none", minWidth: 22, height: 22, padding: "0 6px", borderRadius: 999, background: bg, color: "#fff",
  fontSize: 11, fontWeight: 800, display: "inline-flex", alignItems: "center", justifyContent: "center",
});
const titleStyle = { flex: 1, minWidth: 0, fontSize: 13.5, fontWeight: 700, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" };

export default function ReviewCard({ uid, profile, concepts }) {
  const [recent] = useState(() => getRecentConcepts());
  const [all, setAll] = useState(Array.isArray(concepts) ? concepts : null);
  const [status, setStatus] = useState(null);   // { ready, byId, today_done, today_cap } · ready:null = 못 불러옴

  useEffect(() => { if (Array.isArray(concepts)) setAll(concepts); }, [concepts]);
  useEffect(() => {
    if (recent.length || all) return;
    let alive = true;
    listConcepts().then((c) => { if (alive) setAll(c || []); }).catch(() => { if (alive) setAll([]); });
    return () => { alive = false; };
  }, [recent.length, all]);
  useEffect(() => {
    if (!uid) return;
    let alive = true;
    reviewStatus(recent.map((r) => r.id)).then((r) => {
      if (!alive) return;
      setStatus({
        ready: r.ready, today_done: r.today_done ?? 0, today_cap: r.today_cap ?? DAILY_CAP,
        byId: Object.fromEntries((r.concepts || []).map((c) => [c.concept_id, c])),
      });
    }).catch(() => { if (alive) setStatus({ ready: null }); });
    return () => { alive = false; };
  }, [uid]); // eslint-disable-line react-hooks/exhaustive-deps

  const go = (id) => { location.hash = `#/c/${encodeURIComponent(id)}?review=1`; };
  const titleOf = (r) => (all || []).find((c) => c.id === r.id)?.title || r.title || r.id;
  const first = !recent.length && all ? defaultConceptFor(profile, all) : null;

  const rows = recent.map((r, i) => {
    const s = status?.byId?.[r.id];
    const rank = s?.rank ?? i + 1;
    const cap = s?.cap ?? capForRank(rank);
    const remaining = s ? s.remaining : null;
    const label = !status ? "" : status.ready === false ? "보상 준비 중" : status.ready === null ? "" : remaining > 0 ? `보상 ${remaining}회 남음` : "보상 완료";
    return { id: r.id, rank, cap, remaining, label, title: titleOf(r) };
  });

  const footer = !uid ? "로그인하면 복습 보상을 받을 수 있어요"
    : !status ? "…"
    : status.ready === false ? `Ⓓ 보상 준비 중 · 복습 1회 = Ⓓ ${REWARD}`
    : status.ready === null ? "현황을 불러오지 못했어요"
    : `Ⓓ 오늘 ${status.today_done}/${status.today_cap} · 복습 1회 = Ⓓ ${REWARD}`;

  return (
    <>
      <p className="hd-t">🔁 오늘의 복습</p>
      {recent.length > 0 ? (
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {rows.map((r) => (
            <button key={r.id} type="button" style={rowStyle} onClick={() => go(r.id)} title={`최근 읽은 순서 ${r.rank}번째 · 최대 ${r.cap}회`}>
              <span style={badge(r.remaining === 0 ? "var(--mut)" : "var(--ac)")}>{r.rank}</span>
              <span style={titleStyle}>{r.title}</span>
              <span style={{ flex: "none", fontSize: 11.5, fontWeight: 700, color: r.remaining > 0 ? "var(--ac)" : "var(--mut)" }}>{r.label}</span>
              <span style={{ flex: "none", color: "var(--mut)", fontSize: 12 }}>›</span>
            </button>
          ))}
        </div>
      ) : first ? (
        <button type="button" style={rowStyle} onClick={() => go(first.id)}>
          <span style={badge("var(--ac)")}>시작</span>
          <span style={{ flex: 1, minWidth: 0 }}>
            <span style={{ display: "block", fontSize: 11.5, color: "var(--mut)" }}>처음이라면 여기부터</span>
            <span style={{ ...titleStyle, display: "block" }}>{first.title || first.id}</span>
          </span>
          <span style={{ flex: "none", color: "var(--mut)", fontSize: 12 }}>›</span>
        </button>
      ) : (
        <p className="hd-sub" style={{ margin: 0 }}>{all ? "아직 등록된 개념이 없어요." : "개념을 불러오는 중…"}</p>
      )}
      <p className="hd-sub">{footer}</p>
    </>
  );
}
