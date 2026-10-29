// 대시보드 카드 — 서술형 평가 알림(앱 안). 열린 평가 중 아직 제출하지 않은 것을 맨 위에 보여 주고, 새로 열린 것은 한 번 토스트로 알린다.
// 열린 평가가 없고 최근 결과도 없으면 아무것도 그리지 않는다.
import { useEffect, useState } from "react";
import { assessList, pendingSets, isNew, toastNewSets, invalidateAssessList } from "../../lib/assess/notify";
import { goAssess, markSeen, pendingClaims, claimOne, dropClaim, accessToken } from "../../lib/assess/api";

const fmtDate = (d) => { if (!d) return ""; const [, m, dd] = String(d).split("-"); return `${+m}월 ${+dd}일`; };

/**
 * 로그인한 뒤 "이 기기에서 방금 응시한 기록을 내 계정에 담을까요?" — 결과 화면에서 '로그인하고 담기'를 누른 것만, 30분 안에만.
 * 저절로 담지 않는다: 공용 기기에서 다른 학생이 이어서 로그인해도 남의 결과가 들어가지 않게, 2쪽 이름을 보여 주고 묻는다.
 */
export function ClaimPrompt({ onClaimed, className = "hd-card wide", btnClass = "hd-mini" }) {
  const [list, setList] = useState([]);
  const [busy, setBusy] = useState(null);
  const [msg, setMsg] = useState("");
  useEffect(() => {
    let alive = true;
    accessToken().then((t) => { if (alive && t) setList(pendingClaims()); });
    return () => { alive = false; };
  }, []);
  if (!list.length && !msg) return null;
  const yes = async (c) => {
    setBusy(c.sid); setMsg("");
    try { await claimOne(c.sid); setMsg("내 기록에 담았어요."); invalidateAssessList(); onClaimed?.(); }
    catch (e) { setMsg(e.message || "담지 못했어요"); }
    finally { setBusy(null); setList(pendingClaims()); }
  };
  const no = (c) => { dropClaim(c.sid); setList(pendingClaims()); };
  return (
    <div className={className} role="region" aria-label="응시 기록 담기">
      <div className="hd-thead"><p className="hd-t">🗂 방금 이 기기에서 낸 서술형 평가</p></div>
      {list.map((c) => (
        <div key={c.sid} style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginTop: 6 }}>
          <span style={{ flex: "1 1 180px", fontSize: 13.5 }}><b>{c.title || c.code || "서술형 평가"}</b>{c.name ? ` — 2쪽 이름 ${c.name}` : ""}<br />
            <small style={{ opacity: 0.75 }}>내가 낸 것이 맞으면 내 계정 기록에 담아요.</small></span>
          <button type="button" className={btnClass} disabled={busy === c.sid} onClick={() => yes(c)}>{busy === c.sid ? "담는 중…" : "내 것이 맞아요"}</button>
          <button type="button" className={btnClass} disabled={busy === c.sid} onClick={() => no(c)}>아니에요</button>
        </div>
      ))}
      {msg && <p style={{ margin: "6px 0 0", fontSize: 12.5 }}>{msg}</p>}
    </div>
  );
}

export default function AssessCard() {
  const [list, setList] = useState(null);
  const load = (force = false) => assessList({ force }).then((l) => { setList(l); toastNewSets(l); });
  useEffect(() => {
    let alive = true;
    assessList().then((l) => { if (!alive) return; setList(l); toastNewSets(l); });
    return () => { alive = false; };
  }, []);
  const claim = <ClaimPrompt onClaimed={() => load(true)} />;
  if (!list) return <>{claim}</>;                       // 늘 같은 모양(조각 + 담기 카드)으로 — 목록이 와도 담기 카드 상태가 그대로
  const pend = pendingSets(list);
  const last = (list.mine || []).find((m) => m.status === "submitted");
  if (!pend.length && !last) return <>{claim}</>;
  return (
    <>
    {claim}
    <div className="hd-card wide" style={pend.length ? { borderColor: "var(--ac)", boxShadow: "0 0 0 2px color-mix(in srgb, var(--ac) 25%, transparent)" } : undefined}>
      <div className="hd-thead">
        <p className="hd-t">📝 서술형 평가</p>
        <span className="hd-tsub">{pend.length ? `${pend.length}개 열림` : "최근 결과"}</span>
      </div>
      <div className="hd-rows">
        {pend.slice(0, 3).map((s) => (
          <button key={s.code} type="button" className="hd-row" onClick={() => { markSeen(s.code); goAssess(s.code); }}>
            <span className="ic">📝</span>
            <span className="tx"><b>{s.title}{isNew(s.code) && <span style={{ marginLeft: 6, fontSize: 10, fontWeight: 900, color: "#fff", background: "#EF4444", borderRadius: 999, padding: "1px 6px", verticalAlign: 2 }}>NEW</span>}</b>
              <small>{[fmtDate(s.date), s.grade_label, `${s.n_items}문제`, "다 풀었으면 쪽마다 찍어 채점받기"].filter(Boolean).join(" · ")}</small></span>
            <span className="hd-mini">열기 →</span>
          </button>
        ))}
        {!pend.length && last && (
          <button type="button" className="hd-row" onClick={() => last.code && goAssess(last.code)}>
            <span className="ic">✅</span>
            <span className="tx"><b>{last.title || last.code}</b><small>채점 결과와 AI가 읽은 내 풀이를 볼 수 있어요</small></span>
            <span className="hd-mini">{last.max ? `${last.total}/${last.max}점` : "결과 →"}</span>
          </button>
        )}
      </div>
    </div>
    </>
  );
}
