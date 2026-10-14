// 대시보드 카드 — 서술형 평가 알림(앱 안). 열린 평가 중 아직 제출하지 않은 것을 맨 위에 보여 주고, 새로 열린 것은 한 번 토스트로 알린다.
// 열린 평가가 없고 최근 결과도 없으면 아무것도 그리지 않는다.
import { useEffect, useState } from "react";
import { assessList, pendingSets, isNew, toastNewSets } from "../../lib/assess/notify";
import { goAssess, markSeen } from "../../lib/assess/api";

const fmtDate = (d) => { if (!d) return ""; const [, m, dd] = String(d).split("-"); return `${+m}월 ${+dd}일`; };

export default function AssessCard() {
  const [list, setList] = useState(null);
  useEffect(() => {
    let alive = true;
    assessList().then((l) => { if (!alive) return; setList(l); toastNewSets(l); });
    return () => { alive = false; };
  }, []);
  if (!list) return null;
  const pend = pendingSets(list);
  const last = (list.mine || []).find((m) => m.status === "submitted");
  if (!pend.length && !last) return null;
  return (
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
  );
}
