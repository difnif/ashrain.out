// 개념 → 문항 고르기 (문제풀이 기능 공용)
// mode="concept": 개념을 고르면 onPickConcept(concept, count) — 세트 풀기·OMR 시험지처럼 여러 문항을 쓰는 흐름
// mode="item":    개념을 고른 뒤 문항 목록에서 하나를 고르면 onPickItem(item) — 문장 해설·표시 연습·서술형
// filter: fetchLiveItems/countLive 옵션 ({ withRubric, qtypes, withFigure })
import { useEffect, useMemo, useState } from "react";
import { listConcepts } from "../../lib/concepts";
import { UNIT_NAMES, UNIT_ORDER, countLive, fetchLiveItems } from "../../lib/items";
import "./solve.css";

const LS_UNIT = "ash.solve.unit";
const LS_CONCEPT = "ash.solve.concept";

export default function ItemPicker({ mode = "concept", filter = {}, onPickConcept, onPickItem, hint, counts: useCounts = true }) {
  const [concepts, setConcepts] = useState(null);
  const [unit, setUnit] = useState(() => { try { return localStorage.getItem(LS_UNIT) || "m1-1"; } catch { return "m1-1"; } });
  const [unitCounts, setUnitCounts] = useState({});
  const [counts, setCounts] = useState({});          // concept id → n
  const [concept, setConcept] = useState(null);      // item 모드에서 고른 개념
  const [items, setItems] = useState(null);
  const [busy, setBusy] = useState(false);
  const fkey = JSON.stringify(filter);

  useEffect(() => { listConcepts().then(setConcepts).catch(() => setConcepts([])); }, []);

  // 단원별 공개 문항 수 (필터 적용)
  useEffect(() => {
    if (!useCounts) return;
    let alive = true;
    (async () => {
      const pairs = await Promise.all(UNIT_ORDER.map(async (u) => [u, await countLive({ ...filter, unitId: u })]));
      if (alive) setUnitCounts(Object.fromEntries(pairs));
    })();
    return () => { alive = false; };
  }, [fkey, useCounts]);

  const inUnit = useMemo(() => (concepts || []).filter((c) => c.unit_id === unit).sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0)), [concepts, unit]);

  // 개념별 수 — 단원을 펼칠 때만
  useEffect(() => {
    if (!inUnit.length || !useCounts) return;
    let alive = true;
    (async () => {
      const pairs = await Promise.all(inUnit.map(async (c) => [c.id, await countLive({ ...filter, conceptId: c.id })]));
      if (alive) setCounts((prev) => ({ ...prev, ...Object.fromEntries(pairs) }));
    })();
    return () => { alive = false; };
  }, [inUnit, fkey, useCounts]);

  const pickUnit = (u) => { setUnit(u); setConcept(null); setItems(null); try { localStorage.setItem(LS_UNIT, u); } catch {} };

  const pickConcept = async (c) => {
    try { localStorage.setItem(LS_CONCEPT, c.id); } catch {}
    if (mode === "concept") { onPickConcept?.(c, counts[c.id] ?? 0); return; }
    setConcept(c); setItems(null); setBusy(true);
    try { setItems(await fetchLiveItems({ ...filter, conceptId: c.id, n: 30, pool: 120 })); }
    catch { setItems([]); }
    setBusy(false);
  };

  if (concepts === null) return <div className="sv-muted">개념 목록을 불러오는 중…</div>;

  // 문항 목록 화면 (item 모드)
  if (mode === "item" && concept) {
    return (
      <div>
        <div className="sv-row" style={{ marginBottom: 10 }}>
          <button className="sv-btn sm" onClick={() => { setConcept(null); setItems(null); }}>← 개념 다시 고르기</button>
          <span className="sv-muted">{UNIT_NAMES[unit]} · {concept.title}</span>
        </div>
        {busy && <div className="sv-muted">문항을 불러오는 중…</div>}
        {items && !items.length && <div className="sv-empty">이 개념에는 아직 공개된 문항이 없어요.<br />다른 개념을 골라 주세요.</div>}
        {items && items.length > 0 && (
          <div className="sv-list">
            {items.map((it, i) => (
              <button key={it.id} className="sv-item" onClick={() => onPickItem?.(it)}>
                <span className="no">{i + 1}</span>
                <span className="tx">{String(it.question || "").replace(/\[\[|\]\]/g, "").replace(/\s+/g, " ").slice(0, 90)}</span>
                <span className="rt">{it.qtype === "choice" ? "객관식" : "단답"}{it.figure ? " · 도형" : ""}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div>
      {hint && <p className="sv-sub">{hint}</p>}
      <div className="sv-row wrap" style={{ gap: 6, marginBottom: 12 }}>
        {UNIT_ORDER.map((u) => {
          const n = unitCounts[u];
          const empty = n === 0;
          return (
            <button key={u} className={"sv-chip" + (u === unit ? " on" : "")} style={empty ? { opacity: .45 } : undefined} onClick={() => pickUnit(u)}>
              {UNIT_NAMES[u]}{n != null ? <span className="sv-small"> {n}</span> : null}
            </button>
          );
        })}
      </div>
      {!inUnit.length && <div className="sv-empty">이 학기의 개념이 아직 등록되지 않았어요.</div>}
      <div className="sv-list">
        {inUnit.map((c) => {
          const n = useCounts ? counts[c.id] : undefined;
          const dis = useCounts && n === 0;
          return (
            <button key={c.id} className="sv-item" style={dis ? { opacity: .5 } : undefined} disabled={dis} onClick={() => pickConcept(c)}>
              <span className="no">{String(c.id).split("-").pop()}</span>
              <span className="tx">{c.title}{c.subtitle ? <span className="sv-small"> · {c.subtitle}</span> : null}</span>
              <span className="rt">{!useCounts ? "" : n == null ? "…" : n === 0 ? "준비 중" : `${n}문항`}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

