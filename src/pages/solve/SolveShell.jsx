// 문제풀이 화면 공용 껍데기 — 상단(뒤로·제목·오른쪽 슬롯) + 본문
import { useEffect, useState } from "react";
import "./solve.css";

export function useToast() {
  const [msg, setMsg] = useState(null);
  useEffect(() => { if (!msg) return; const t = setTimeout(() => setMsg(null), 2200); return () => clearTimeout(t); }, [msg]);
  return [msg, setMsg];
}

export default function SolveShell({ title, sub, back = "#/solve", right, children, toast }) {
  return (
    <div className="sv-wrap">
      <div className="sv-top">
        {back && <button className="sv-back" onClick={() => (location.hash = back)}>← 뒤로</button>}
        <h1 className="sv-h1">{title}</h1>
        <span className="sv-sp" />
        {right}
      </div>
      {sub && <p className="sv-sub">{sub}</p>}
      {children}
      {toast && <div className="sv-toast">{toast}</div>}
    </div>
  );
}
