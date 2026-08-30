// src/shared/BirthInput.jsx — 생년월일 3칸 입력 v3
// v1 버그 원인: 자동 focus()가 동기 blur를 유발 → blur 패딩이 렌더 전의 낡은 상태를 읽어 입력을 덮어씀.
// v3 방어 설계:
//  · 포커스 이동은 requestAnimationFrame으로 지연 — React가 먼저 그린 뒤 이동(동기 blur 경합 제거)
//  · blur 패딩은 상태가 아니라 DOM 값(e.currentTarget.value)을 읽음 — 낡은 클로저 원천 차단
//  · 연 4자리 → 월, 월 2자리 → 일 자동 이동 / "19960212" 이어치기·붙여넣기 자동 분배
//  · 월 2~9, 일 4~9는 한 자리로 즉시 확정 / 빈 칸 백스페이스 → 이전 칸
// 값 계약: 완성 시 onChange("YYYY-MM-DD"), 미완성 시 onChange("") — 기존 검증 로직 무수정.
import { useEffect, useRef, useState } from "react";

const FULL = /^(\d{4})-(\d{2})-(\d{2})$/;

export default function BirthInput({ value = "", onChange, inputClass = "" }) {
  const m0 = FULL.exec(value || "");
  const [y, setY] = useState(m0 ? m0[1] : "");
  const [mo, setMo] = useState(m0 ? m0[2] : "");
  const [d, setD] = useState(m0 ? m0[3] : "");
  const yRef = useRef(null), mRef = useRef(null), dRef = useRef(null);

  // 렌더 이후 포커스 이동 — 동기 blur가 상태 반영보다 먼저 오는 경합을 없앤다
  const focusNext = (ref) => requestAnimationFrame(() => ref.current?.focus());

  // 외부에서 완성값이 들어오면(초기 로드 등) 반영
  useEffect(() => {
    const m = FULL.exec(value || "");
    if (m && (m[1] !== y || m[2] !== mo || m[3] !== d)) { setY(m[1]); setMo(m[2]); setD(m[3]); }
  }, [value]); // eslint-disable-line

  const emit = (a, b, c) =>
    onChange(a.length === 4 && b.length === 2 && c.length === 2 ? `${a}-${b}-${c}` : "");
  const smDay = (v) => (v.length === 1 && Number(v) >= 4 ? "0" + v : v);
  // 월·일 순차 스마트 소비: 첫 자리가 2~9면 월을 한 자리로 확정("2"→"02"), 남은 자리를 일로
  const splitMD = (rest) => {
    let mm, i;
    if (rest.length && Number(rest[0]) >= 2) { mm = "0" + rest[0]; i = 1; }
    else { mm = rest.slice(0, 2); i = Math.min(2, rest.length); }
    const dr = rest.slice(i);
    const dd = dr.length === 1 ? smDay(dr) : dr.slice(0, 2);
    return [mm, dd];
  };

  const onY = (e) => {
    const raw = e.target.value.replace(/\D/g, "");
    const yy = raw.slice(0, 4);
    setY(yy);
    if (raw.length > 4) {
      const [mm, dd] = splitMD(raw.slice(4));
      setMo(mm); setD(dd); emit(yy, mm, dd);
      focusNext(mm.length === 2 ? dRef : mRef);
    } else {
      emit(yy, mo, d);
      if (yy.length === 4) focusNext(mRef);
    }
  };

  const onM = (e) => {
    const raw = e.target.value.replace(/\D/g, "");
    const [mm, dd] = splitMD(raw);
    setMo(mm);
    if (dd) {
      setD(dd); emit(y, mm, dd); focusNext(dRef);
    } else {
      emit(y, mm, d);
      if (mm.length === 2) focusNext(dRef);
    }
  };

  const onD = (e) => {
    const dd = smDay(e.target.value.replace(/\D/g, "").slice(0, 2));
    setD(dd); emit(y, mo, dd);
  };

  const backTo = (ref) => (e) => {
    if (e.key === "Backspace" && !e.currentTarget.value) { e.preventDefault(); ref.current?.focus(); }
  };
  // blur 패딩 — DOM 값 기준(상태 클로저 미사용)
  const padM = (e) => {
    const v = e.currentTarget.value.replace(/\D/g, "");
    if (v.length === 1) { const p = "0" + v; setMo(p); emit(y, p, d); }
  };
  const padD = (e) => {
    const v = e.currentTarget.value.replace(/\D/g, "");
    if (v.length === 1) { const p = "0" + v; setD(p); emit(y, mo, p); }
  };

  const seg = { width: "auto", minWidth: 0, textAlign: "center", fontVariantNumeric: "tabular-nums" };
  return (
    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
      <input ref={yRef} className={inputClass} style={{ ...seg, flex: 1.6 }} value={y} onChange={onY}
        inputMode="numeric" autoComplete="bday-year" placeholder="연도" aria-label="출생 연도" />
      <span style={{ opacity: .45 }}>–</span>
      <input ref={mRef} className={inputClass} style={{ ...seg, flex: 1 }} value={mo} onChange={onM}
        onKeyDown={backTo(yRef)} onBlur={padM}
        inputMode="numeric" autoComplete="bday-month" placeholder="월" aria-label="출생 월" />
      <span style={{ opacity: .45 }}>–</span>
      <input ref={dRef} className={inputClass} style={{ ...seg, flex: 1 }} value={d} onChange={onD}
        onKeyDown={backTo(mRef)} onBlur={padD}
        inputMode="numeric" autoComplete="bday-day" placeholder="일" aria-label="출생 일" />
    </div>
  );
}
