// src/shared/BirthInput.jsx — 생년월일 분할 입력
// · 연도 4자리 입력(또는 붙여넣기) 시 월로 자동 이동, 월 2자리 → 일로 이동
// · "19960212"처럼 이어 입력하면 연·월·일로 자동 분배
// · 월 2~9, 일 4~9는 한 자리만 눌러도 0을 붙여 즉시 확정
// · 빈 칸에서 백스페이스 → 이전 칸으로
// 값 계약: 완성 시 onChange("YYYY-MM-DD"), 미완성 시 onChange("") — 기존 검증 로직 그대로 동작.
import { useEffect, useRef, useState } from "react";

const FULL = /^(\d{4})-(\d{2})-(\d{2})$/;
const pad2 = (s) => (s.length === 1 ? "0" + s : s);

export default function BirthInput({ value = "", onChange, inputClass = "" }) {
  const m0 = FULL.exec(value || "");
  const [y, setY] = useState(m0 ? m0[1] : "");
  const [mo, setMo] = useState(m0 ? m0[2] : "");
  const [d, setD] = useState(m0 ? m0[3] : "");
  const yRef = useRef(null), mRef = useRef(null), dRef = useRef(null);

  // 외부에서 완성값이 들어오면(초기 로드 등) 반영
  useEffect(() => {
    const m = FULL.exec(value || "");
    if (m && (m[1] !== y || m[2] !== mo || m[3] !== d)) { setY(m[1]); setMo(m[2]); setD(m[3]); }
  }, [value]); // eslint-disable-line

  const emit = (yy, mm, dd) =>
    onChange(yy.length === 4 && mm.length === 2 && dd.length === 2 ? `${yy}-${mm}-${dd}` : "");

  const smartMonth = (v) => (v.length === 1 && Number(v) >= 2 ? "0" + v : v);
  const smartDay = (v) => (v.length === 1 && Number(v) >= 4 ? "0" + v : v);

  const onY = (e) => {
    const raw = e.target.value.replace(/\D/g, "");
    const yy = raw.slice(0, 4);
    setY(yy);
    if (raw.length > 4) {
      // 이어 입력·붙여넣기 → 월·일로 분배
      const mm = smartMonth(raw.slice(4, 6));
      const dd = smartDay(raw.slice(6, 8));
      setMo(mm); setD(dd); emit(yy, mm, dd);
      (mm.length === 2 ? dRef : mRef).current?.focus();
    } else {
      emit(yy, mo, d);
      if (yy.length === 4) mRef.current?.focus();
    }
  };

  const onMo = (e) => {
    const raw = e.target.value.replace(/\D/g, "");
    let mm = smartMonth(raw.slice(0, 2));
    setMo(mm);
    if (raw.length > 2) {
      const dd = smartDay(raw.slice(2, 4));
      setD(dd); emit(y, mm, dd); dRef.current?.focus();
    } else {
      emit(y, mm, d);
      if (mm.length === 2) dRef.current?.focus();
    }
  };

  const onD = (e) => {
    const dd = smartDay(e.target.value.replace(/\D/g, "").slice(0, 2));
    setD(dd); emit(y, mo, dd);
  };

  const backTo = (ref) => (e) => {
    if (e.key === "Backspace" && !e.currentTarget.value) { e.preventDefault(); ref.current?.focus(); }
  };
  const padOnBlur = (val, set, pos) => () => {
    if (val.length === 1) {
      const p = pad2(val); set(p);
      emit(y, pos === "m" ? p : mo, pos === "d" ? p : d);
    }
  };

  const seg = { width: "auto", minWidth: 0, textAlign: "center" };
  return (
    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
      <input ref={yRef} className={inputClass} style={{ ...seg, flex: 1.6 }} value={y} onChange={onY}
        inputMode="numeric" autoComplete="bday-year" placeholder="연도" aria-label="출생 연도" />
      <span style={{ opacity: .45 }}>–</span>
      <input ref={mRef} className={inputClass} style={{ ...seg, flex: 1 }} value={mo} onChange={onMo}
        onKeyDown={backTo(yRef)} onBlur={padOnBlur(mo, setMo, "m")}
        inputMode="numeric" autoComplete="bday-month" placeholder="월" aria-label="출생 월" />
      <span style={{ opacity: .45 }}>–</span>
      <input ref={dRef} className={inputClass} style={{ ...seg, flex: 1 }} value={d} onChange={onD}
        onKeyDown={backTo(mRef)} onBlur={padOnBlur(d, setD, "d")}
        inputMode="numeric" autoComplete="bday-day" placeholder="일" aria-label="출생 일" />
    </div>
  );
}
