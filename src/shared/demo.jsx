// src/shared/demo.jsx — 데모 UI 공용 키트
// 페이지 골격 단계에서 전 화면이 공유. 기능이 채워질 때 페이지별로 자연 대체된다.
import { useEffect, useState } from "react";

export function useAppHash() {
  const read = () => location.hash.replace(/^#\/?/, "");
  const [h, setH] = useState(read);
  useEffect(() => {
    const f = () => setH(read());
    window.addEventListener("hashchange", f);
    return () => window.removeEventListener("hashchange", f);
  }, []);
  const seg = h.split("/");
  return [seg[0] || "", seg[1] || "", h];
}

export const go = (hash) => { location.hash = hash; };

const CSS = `
.d-page{display:flex;flex-direction:column;gap:12px}
.d-head{display:flex;align-items:center;gap:8px;margin-top:2px}
.d-head h2{font-size:17px;margin:0}
.d-demo{font-size:10px;font-weight:800;color:var(--ac);border:1px solid var(--ac);border-radius:999px;padding:2px 7px;opacity:.85}
.d-card{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:14px;position:relative}
.d-ct{color:var(--mut);font-size:11.5px;font-weight:800;letter-spacing:.04em;margin:0 0 10px}
.d-row{display:flex;align-items:center;gap:10px;padding:10px 2px;border-bottom:1px solid var(--bd)}
.d-row:last-child{border-bottom:0}
.d-row.click{cursor:pointer}
.d-main{font-size:13.5px;font-weight:700}
.d-sub{font-size:12px;color:var(--mut);margin-top:2px}
.d-sp{flex:1}
.d-chip{font-size:11px;font-weight:800;border-radius:999px;padding:3px 9px;border:1px solid var(--bd);color:var(--mut);white-space:nowrap}
.d-chip.ac{color:var(--ac);border-color:var(--ac)}
.d-chip.ok{color:var(--ok);border-color:var(--ok)}
.d-chip.warn{color:var(--warn);border-color:var(--warn)}
.d-chip.down{color:var(--down);border-color:var(--down)}
.d-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:8px}
.d-stat{background:var(--in);border-radius:10px;padding:10px 12px}
.d-stat b{display:block;font-size:16px}
.d-stat span{font-size:11px;color:var(--mut)}
.d-tabs{display:flex;gap:6px;flex-wrap:wrap}
.d-tab{background:var(--card);border:1px solid var(--bd);border-radius:999px;color:var(--mut);font-size:12px;font-weight:700;padding:7px 12px;cursor:pointer;font-family:inherit}
.d-tab.on{border-color:var(--ac);color:var(--ac)}
.d-btn{background:var(--card);border:1px solid var(--bd);border-radius:10px;color:var(--ink);font-size:12.5px;font-weight:700;padding:9px 13px;cursor:pointer;font-family:inherit}
.d-btn.pri{background:var(--ac);border-color:var(--ac);color:var(--bg)}
.d-btn.full{width:100%}
.d-in{width:100%;box-sizing:border-box;background:var(--in);border:1px solid var(--bd);border-radius:10px;padding:10px 12px;color:var(--ink);font-family:inherit;font-size:13.5px}
textarea.d-in{min-height:84px;resize:vertical}
.d-lbl{font-size:12px;color:var(--mut);font-weight:700;margin:4px 0 6px}
.d-grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.d-serif{font-family:var(--font-serif);line-height:1.85}
.d-bar{height:6px;background:var(--in);border-radius:99px;overflow:hidden}
.d-bar>i{display:block;height:100%;background:var(--ac)}
.d-note{font-size:12px;color:var(--mut);line-height:1.65}
.d-vault{background:var(--in);border:1px dashed var(--bd);border-radius:10px;padding:10px 12px}
.d-cell{width:100%;aspect-ratio:1;border:1px solid var(--bd);border-radius:8px;background:var(--card);color:var(--mut);font-weight:800;font-size:12px;cursor:pointer;font-family:inherit}
.d-cell.o{border-color:var(--ok);color:var(--ok)}
.d-cell.x{border-color:var(--down);color:var(--down)}
`;
export function Kit() { return <style>{CSS}</style>; }

export function Demo() { return <span className="d-demo">데모</span>; }
export function Page({ title, right, children }) {
  return (
    <div className="d-page">
      <div className="d-head"><h2>{title}</h2><Demo />{right && <><span className="d-sp" />{right}</>}</div>
      {children}
    </div>
  );
}
export function Card({ title, children }) {
  return <div className="d-card">{title && <p className="d-ct">{title}</p>}{children}</div>;
}
export function Row({ main, sub, right, onClick }) {
  return (
    <div className={"d-row" + (onClick ? " click" : "")} onClick={onClick}>
      <div><div className="d-main">{main}</div>{sub && <div className="d-sub">{sub}</div>}</div>
      <span className="d-sp" />{right}
    </div>
  );
}
export function Chip({ tone = "", children }) { return <span className={"d-chip " + tone}>{children}</span>; }
export function Stat({ label, value }) { return <div className="d-stat"><b>{value}</b><span>{label}</span></div>; }
export function Tabs({ items, cur, onSel }) {
  return (
    <div className="d-tabs">
      {items.map(([k, l]) => (
        <button key={k} className={"d-tab" + (cur === k ? " on" : "")} onClick={() => onSel(k)}>{l}</button>
      ))}
    </div>
  );
}
export function Nav({ items, cur }) {
  return (
    <div className="d-tabs" style={{ margin: "2px 0 6px" }}>
      {items.map(([k, l]) => (
        <button key={k} className={"d-tab" + (cur === k ? " on" : "")} onClick={() => go("#/" + k)}>{l}</button>
      ))}
    </div>
  );
}
