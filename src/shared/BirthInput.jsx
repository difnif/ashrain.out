// src/shared/BirthInput.jsx — 생년월일 입력 v2 (단일 칸 · 자동 하이픈)
// v1(3분할+자동 포커스)은 focus()가 동기 blur를 유발해 낡은 클로저의 0-패딩이
// 입력을 덮어쓰는 버그("02"→"00")가 있었다. v2는 포커스 이동 자체를 제거:
// 숫자만 이어 치면 1996-02-02 형태로 하이픈이 자동으로 붙는다.
// · 입력: 숫자 8자리(YYYYMMDD). 붙여넣기·백스페이스 자연 동작.
// · 값 계약(v1과 동일): 8자리 완성 시 onChange("YYYY-MM-DD"), 미완성 시 onChange("").
//   날짜 유효성(2월 31일 등)은 기존 fullAge의 Date 파싱이 걸러낸다.
import { useEffect, useState } from "react";

const fmt = (d) =>
  d.length <= 4 ? d
  : d.length <= 6 ? d.slice(0, 4) + "-" + d.slice(4)
  : d.slice(0, 4) + "-" + d.slice(4, 6) + "-" + d.slice(6);

export default function BirthInput({ value = "", onChange, inputClass = "" }) {
  const [digits, setDigits] = useState(() => (value || "").replace(/\D/g, "").slice(0, 8));

  // 외부에서 완성값이 들어오면(초기 로드·자동완성) 반영
  useEffect(() => {
    const v = (value || "").replace(/\D/g, "").slice(0, 8);
    if (v.length === 8 && v !== digits) setDigits(v);
  }, [value]); // eslint-disable-line

  const onInput = (e) => {
    const d = e.target.value.replace(/\D/g, "").slice(0, 8);
    setDigits(d);
    onChange(d.length === 8 ? fmt(d) : "");
  };

  return (
    <input
      className={inputClass}
      value={fmt(digits)}
      onChange={onInput}
      inputMode="numeric"
      maxLength={10}
      autoComplete="bday"
      placeholder="생년월일 8자리 (예: 20120315)"
      aria-label="생년월일"
      style={{ fontVariantNumeric: "tabular-nums", letterSpacing: ".5px" }}
    />
  );
}
