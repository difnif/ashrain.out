// 개념 → 문항 고르기 (문제풀이 기능 공용)
// mode="concept": 개념을 고르면 onPickConcept(concept, count) — 세트 풀기·OMR 시험지처럼 여러 문항을 쓰는 흐름
// mode="item":    개념을 고른 뒤 문항 목록에서 하나를 고르면 onPickItem(item) — 문장 해설·표시 연습·서술형
// filter: fetchLiveItems/카운트 옵션 ({ withRubric, qtypes, withFigure })
// 문항 수는 studyCache(한 번의 질의 + 10분 캐시)로 — 화면마다 12+N번 세던 왕복을 없앴다 (2026-09-21).
// 검색: 개념 이름·부제·학기명을 부분일치/초성으로 — 학기 칩을 안 거치고 바로 찾아간다.
import { useEffect, useMemo, useState } from "react";
import { UNIT_NAMES, UNIT_ORDER, fetchLiveItems } from "../../lib/items";
import { swrConcepts, swrCounts } from "../../lib/studyCache";
import { koFilter } from "../../lib/koSearch";
import "./solve.css";

const LS_UNIT = "ash.solve.unit";
const LS_CONCEPT = "ash.solve.concept";

export default function ItemPicker({ mode = "concept", filter = {}, onPickConcept, onPickItem, hint, counts: useCounts = true }) {
  const [concepts, setConcepts] = useState(null);
  const [unit, setUnit] = useState(() => { try { return localStorage.getItem(LS_UNIT) || "m1-1"; } catch { return "m1-1"; } });
  const [cnt, setCnt] = useState(null);              // { unit: {u→n}, concept: {id→n} }
  const [more, setMore] = useState(false);           // 빈 학기 칩 펼치기
  const [q, setQ] = useState("");                    // 검색어
  const [concept, setConcept] = useState(null);      // item 모드에서 고른 개념
  const [items, setItems] = useState(null);
  const [busy, setBusy] = useState(false);
  const fkey = JSON.stringify(filter);

  useEffect(() => { let ok = true; swrConcepts((v) => { if (ok) setConcepts(v || []); }); return () => { ok = false; }; }, []);
  useEffect(() => {
    if (!useCounts) return;
    let ok = true;
    swrCounts(filter, (v) => { if (ok && v) setCnt(v); });
    return () => { ok = false; };
    /* eslint-disable-next-line react-hooks/exhaustive-deps */
  }, [fkey, useCounts]);

  const inUnit = useMemo(() => (concepts || []).filter((c) => c.unit_id === unit).sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0)), [concepts, unit]);

  // 검색 결과 — 학기 무관 전체에서
  const found = useMemo(() => {
    if (!q.trim()) return null;
    const rows = (concepts || []).slice().sort((a, b) => UNIT_ORDER.indexOf(a.unit_id) - UNIT_ORDER.indexOf(b.unit_id) || (a.sort_order ?? 0) - (b.sort_order ?? 0));
    return koFilter(rows, q, (c) => [c.title, c.subtitle, UNIT_NAMES[c.unit_id]], 30);
  }, [concepts, q]);

  // 칩: 문항(또는 개념)이 있는 학기만 기본 노출 — 나머지는 「다른 학기」로 접어 둔다
  const hasContent = (u) => (useCounts && cnt ? (cnt.unit[u] || 0) > 0 : (concepts || []).some((c) => c.unit_id === u));
  const readyToTrim = useCounts ? !!cnt : concepts !== null;
  const visUnits = !readyToTrim || more ? UNIT_ORDER : UNIT_ORDER.filter((u) => u === unit || hasContent(u));
  const hiddenN = UNIT_ORDER.length - visUnits.length;

  const pickUnit = (u) => { setUnit(u); setConcept(null); setItems(null); try { localStorage.setItem(LS_UNIT, u); } catch { /* 무시 */ } };

  const pickConcept = async (c) => {
    try { localStorage.setItem(LS_CONCEPT, c.id); } catch { /* 무시 */ }
    if (c.unit_id && c.unit_id !== unit) pickUnit(c.unit_id);           // 검색으로 다른 학기 개념을 고른 경우
    if (mode === "concept") { onPickConcept?.(c, cnt?.concept?.[c.id] ?? 0); return; }
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

  const rowsOf = (list, withUnit) => (
    <div className="sv-list">
      {list.map((c) => {
        const n = useCounts ? cnt?.concept?.[c.id] ?? (cnt ? 0 : null) : undefined;
        const dis = useCounts && n === 0;
        return (
          <button key={c.id} className="sv-item" style={dis ? { opacity: .5 } : undefined} disabled={dis} onClick={() => pickConcept(c)}>
            <span className="no">{String(c.id).split("-").pop()}</span>
            <span className="tx">{c.title}{c.subtitle ? <span className="sv-small"> · {c.subtitle}</span> : null}</span>
            <span className="rt">{withUnit ? <span className="sv-small">{UNIT_NAMES[c.unit_id] || c.unit_id} · </span> : null}{!useCounts ? "" : n == null ? "…" : n === 0 ? "준비 중" : `${n}문항`}</span>
          </button>
        );
      })}
    </div>
  );

  return (
    <div>
      {hint && <p className="sv-sub">{hint}</p>}
      <input className="sv-search" type="search" value={q} onChange={(e) => setQ(e.target.value)}
        placeholder="개념 검색 — 이름이나 초성(ㅈㅅ)으로 바로 찾기" aria-label="개념 검색" enterKeyHint="search" />
      {found !== null ? (
        found.length === 0
          ? <div className="sv-empty">「{q.trim()}」에 맞는 개념이 없어요. 철자를 바꾸거나 초성으로 찾아보세요.</div>
          : rowsOf(found, true)
      ) : (
        <>
          <div className="sv-row wrap" style={{ gap: 6, marginBottom: 12 }}>
            {visUnits.map((u) => {
              const n = useCounts ? cnt?.unit?.[u] : null;
              const empty = useCounts && cnt && !n;
              return (
                <button key={u} className={"sv-chip" + (u === unit ? " on" : "")} style={empty ? { opacity: .45 } : undefined} onClick={() => pickUnit(u)}>
                  {UNIT_NAMES[u]}{n != null ? <span className="sv-small"> {n}</span> : null}
                </button>
              );
            })}
            {readyToTrim && (hiddenN > 0 || more) && (
              <button className="sv-chip" style={{ color: "var(--muted)" }} onClick={() => setMore((m) => !m)}>
                {more ? "접기" : `다른 학기 +${hiddenN}`}
              </button>
            )}
          </div>
          {!inUnit.length && <div className="sv-empty">이 학기의 개념이 아직 등록되지 않았어요.</div>}
          {rowsOf(inUnit, false)}
        </>
      )}
    </div>
  );
}
