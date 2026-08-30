// src/shared/LogoTrigger.jsx — 로고 트리거 v2: 우/하 슬롯으로 "당겨서" 앱 전환
// v2: src(이미지) 또는 handle(임의 노드 — 임시 글자 타일 등)을 손잡이로 사용. 세 앱 공용.
// · 드래그(포인터 통합): 슬롯 거리 55% 넘겨 놓으면 스냅 후 이동, 미달이면 복귀
// · 슬롯 탭/클릭: 당김 애니메이션 후 이동 · 손잡이 단순 클릭: onLogoClick(홈)
// last_role은 건드리지 않는다 — 의도적 전환은 RoleSwitch 소관.
import { useRef, useState } from "react";

const CSS = `
.lt-grid{display:grid;grid-template-columns:auto 22px;grid-template-rows:auto 22px;gap:5px;align-items:center}
.lt-logo{grid-area:1/1;cursor:grab;touch-action:none;user-select:none;-webkit-user-drag:none;position:relative;z-index:2}
.lt-logo.drag{cursor:grabbing}
.lt-logo.snap{transition:transform .16s ease}
.lt-tile{width:28px;height:28px;display:flex;align-items:center;justify-content:center;
  border:1.5px solid var(--bd);border-radius:9px;background:var(--card);color:var(--ink);
  font-family:var(--font-display, inherit);font-size:15px;font-weight:700;line-height:1}
.lt-slot{width:22px;height:22px;border:1.5px dashed var(--bd);border-radius:8px;background:transparent;
  color:var(--mut);font-size:11px;font-weight:800;font-family:inherit;line-height:1;
  display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.lt-slot img{height:12px;filter:grayscale(1) brightness(0);opacity:.75}
.lt-slot.r{grid-area:1/2}
.lt-slot.d{grid-area:2/1;justify-self:start;margin-left:1px}
.lt-slot.hot,.lt-slot:hover{border-color:var(--ac);border-style:solid;color:var(--ac)}
`;

export default function LogoTrigger({ src, handle, alt = "app", height = 28, right, down, onLogoClick }) {
  const logoRef = useRef(null), rRef = useRef(null), dRef = useRef(null);
  const st = useRef(null);
  const [xy, setXY] = useState([0, 0]);
  const [mode, setMode] = useState("");
  const [hot, setHot] = useState("");

  const travel = (which) => {
    const l = logoRef.current?.getBoundingClientRect();
    const s = (which === "r" ? rRef : dRef).current?.getBoundingClientRect();
    if (!l || !s) return 40;
    return which === "r"
      ? s.left + s.width / 2 - (l.left + l.width / 2)
      : s.top + s.height / 2 - (l.top + l.height / 2);
  };

  const commit = (which) => {
    setMode("snap"); setHot(which);
    setXY(which === "r" ? [travel("r"), 0] : [0, travel("d")]);
    setTimeout(() => (which === "r" ? right : down).go(), 170);
  };

  const onDown = (e) => {
    e.preventDefault();
    logoRef.current.setPointerCapture(e.pointerId);
    st.current = { x: e.clientX, y: e.clientY, moved: false, tx: travel("r"), ty: travel("d") };
    setMode("drag");
  };
  const onMove = (e) => {
    const s = st.current;
    if (!s) return;
    let dx = e.clientX - s.x, dy = e.clientY - s.y;
    if (Math.abs(dx) > 6 || Math.abs(dy) > 6) s.moved = true;
    dx = Math.max(0, Math.min(dx, s.tx));
    dy = Math.max(0, Math.min(dy, s.ty));
    if (dx >= dy) dy = 0; else dx = 0;
    setXY([dx, dy]);
    setHot(dx > s.tx * 0.55 ? "r" : dy > s.ty * 0.55 ? "d" : "");
  };
  const onUp = () => {
    const s = st.current;
    st.current = null;
    if (!s) return;
    if (!s.moved) { setMode(""); setXY([0, 0]); onLogoClick && onLogoClick(); return; }
    if (xy[0] > s.tx * 0.55) return commit("r");
    if (xy[1] > s.ty * 0.55) return commit("d");
    setMode("snap"); setXY([0, 0]); setHot("");
    setTimeout(() => setMode(""), 170);
  };

  const hp = {
    ref: logoRef, draggable: false,
    onPointerDown: onDown, onPointerMove: onMove, onPointerUp: onUp, onPointerCancel: onUp,
  };
  const tf = { transform: "translate(" + xy[0] + "px," + xy[1] + "px)" };

  return (
    <span className="lt-grid">
      <style>{CSS}</style>
      {src ? (
        <img {...hp} src={src} alt={alt} className={"lt-logo tb-logo " + mode} style={{ height, ...tf }} />
      ) : (
        <span {...hp} className={"lt-logo " + mode} style={tf}>{handle}</span>
      )}
      <button ref={rRef} className={"lt-slot r" + (hot === "r" ? " hot" : "")}
        aria-label={right.label + "으로 전환"} title={right.label} onClick={() => commit("r")}>{right.tag}</button>
      <button ref={dRef} className={"lt-slot d" + (hot === "d" ? " hot" : "")}
        aria-label={down.label + "으로 전환"} title={down.label} onClick={() => commit("d")}>{down.tag}</button>
    </span>
  );
}
