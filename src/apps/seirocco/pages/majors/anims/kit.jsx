// 전공 수학 「움직이는 그림」 공용 키트 — 시계(보일 때만 돈다) · 틀(SVG + 조작 줄) · 미끄럼 막대 · 고르기 · 좌표 그리기
// 그림마다 viewBox 360×220 을 기본으로(화면 폭에 맞춰 늘고 준다). 색은 앱 변수(--ink · --mut · --ac · --sp)를 따른다.
// 서버 그리기(검산 tests/majors.test.mjs)에서는 효과가 돌지 않아 t = 0 의 첫 장면만 그린다 — 그래서 첫 장면도 뜻이 통하게 만든다.
import { useCallback, useEffect, useRef, useState } from "react";

export const C = {
  ink: "var(--ink)", mut: "var(--mut)", bd: "var(--bd)", ac: "var(--ac)", sp: "var(--sp, var(--ac))", card: "var(--card)", in: "var(--in)",
  red: "#b4442e", gold: "#b07d12", green: "#3f7d3a", blue: "#2f6db0", violet: "#7254b8", teal: "#1f8f84",
};

export const CSS = `
.ma{border:1px solid var(--bd);border-radius:12px;background:var(--card);overflow:hidden}
.ma-svg{display:block;width:100%;height:auto;max-height:340px;background:var(--in);touch-action:pan-y}
.ma-svg text{font-family:inherit}
.ma-ctl{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;padding:8px 10px;border-top:1px solid var(--bd)}
.ma-btn{min-width:34px;height:30px;border-radius:8px;border:1px solid var(--bd);background:var(--card);color:var(--ink);font:inherit;font-weight:800;font-size:13px;cursor:pointer;padding:0 8px}
.ma-btn.on{background:var(--sp,var(--ac));border-color:var(--sp,var(--ac));color:var(--bg)}
.ma-sl{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--mut);flex:1 1 150px;min-width:0}
.ma-sl b{color:var(--ink);font-variant-numeric:tabular-nums;min-width:38px;text-align:right}
.ma-sl input{flex:1;min-width:60px;accent-color:var(--sp,var(--ac))}
.ma-seg{display:inline-flex;flex-wrap:wrap;max-width:100%;border:1px solid var(--bd);border-radius:8px;overflow:hidden}
.ma-seg button{border:0;background:var(--card);color:var(--mut);font:inherit;font-size:12px;font-weight:800;padding:6px 9px;cursor:pointer;flex:1 1 auto}
.ma-seg button+button{border-left:1px solid var(--bd)}
.ma-seg button.on{background:var(--sp,var(--ac));color:var(--bg)}
.ma-read{font-size:12px;color:var(--ink);padding:6px 10px 0;line-height:1.6;font-variant-numeric:tabular-nums}
.ma-read b{color:var(--sp,var(--ac))}
.ma-mat{display:inline-grid;vertical-align:middle;column-gap:7px;padding:1px 5px;margin:0 2px;border-left:1.5px solid currentColor;border-right:1.5px solid currentColor;border-radius:5px;line-height:1.3;text-align:center;font-size:.95em}
`;

/** 같은 씨앗이면 같은 난수 — 모의 실험(중심극한 · 랜덤워크)이 그릴 때마다 같은 모양에서 시작하게 */
export function rng(seed = 1) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
/** 표준정규 난수(박스-뮬러) */
export const gauss = (r) => { const u = Math.max(1e-12, r()), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
export const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const ease = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));
export const fmt = (v, d = 2) => {
  if (!Number.isFinite(v)) return "—";
  const s = Math.abs(v) >= 1000 ? v.toFixed(0) : v.toFixed(d);
  const out = s.replace(/\.?0+$/, (m) => (m.includes(".") ? "" : m)).replace("-", "−");
  return out === "−0" ? "0" : out;
};

/** 시계 한 걸음 — 시간이 거꾸로 가면 그림이 음수 칸(배열[−1])을 읽어 장 전체가 멈추므로 0 아래로 내려가지 않게, 주기는 0 부터 다시 */
export function advanceT(x, dt, period = 0, speed = 1) {
  const v = x + Math.max(0, dt) * speed;
  return period ? ((v % period) + period) % period : Math.max(0, v);
}

/**
 * 시계 — 화면에 보이면 저절로 돌고(줄인 움직임 설정이면 멈춘 채), 안 보이면 쉰다.
 * period 가 있으면 0 … period 를 되풀이한다. rest: 움직임 줄이기 설정에서 멈춰 보여 줄 시각(전 → 후를 보여 주는 그림).
 * 반환: { t, playing, toggle, reset, setT, ref }
 */
export function useClock({ period = 0, speed = 1, auto = true, rest } = {}) {
  // 검산은 서버 그리기에서 여러 순간을 보려고 globalThis.__MA_T0 (초)를 둔다 — 앱에서는 늘 0 에서 시작
  const [t, setT] = useState(() => {
    const t0 = typeof globalThis !== "undefined" && typeof globalThis.__MA_T0 === "number" ? globalThis.__MA_T0 : 0;
    return period ? ((t0 % period) + period) % period : t0;
  });
  const [playing, setPlaying] = useState(false);
  const ref = useRef(null);
  const userPaused = useRef(false);
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") return undefined;
    const reduce = typeof window !== "undefined" && window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    // 움직임 줄이기 설정이면 돌지 않으니, 한 장으로 볼 때 뜻이 가장 잘 보이는 순간(rest)에 세워 둔다(검산이 시각을 정했으면 그대로)
    if (reduce && rest != null && typeof globalThis.__MA_T0 !== "number") setT(rest);
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { if (auto && !reduce && !userPaused.current) setPlaying(true); }
      else setPlaying(false);
    }, { threshold: 0.3 });
    io.observe(el);
    return () => io.disconnect();
  }, [auto]);
  useEffect(() => {
    if (!playing) return undefined;
    let raf = 0, last = performance.now();
    const step = (now) => {
      // 첫 프레임의 시각(now)이 last 보다 이를 수 있다(rAF 는 프레임 시작 시각을 준다) — 그래서 dt 가 음수일 수 있다
      const dt = Math.min(0.05, (now - last) / 1000);
      last = Math.max(last, now);
      setT((x) => advanceT(x, dt, period, speed));
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [playing, speed, period]);
  const toggle = useCallback(() => setPlaying((p) => { userPaused.current = p; return !p; }), []);
  const reset = useCallback(() => setT(0), []);
  return { t, setT, playing, setPlaying, toggle, reset, ref };
}

/** 틀 — SVG 한 장 + (읽는 값) + 조작 줄 */
export function Frame({ clock, title, vb = "0 0 360 220", children, controls, read, noClock = false }) {
  return (
    <div className="ma" ref={clock?.ref}>
      <style>{CSS}</style>
      <svg viewBox={vb} className="ma-svg" role="img" aria-label={title}>{children}</svg>
      {read && <div className="ma-read">{read}</div>}
      <div className="ma-ctl">
        {clock && !noClock && (
          <>
            <button type="button" className="ma-btn" onClick={clock.toggle} aria-label={clock.playing ? "멈춤" : "재생"}>{clock.playing ? "❚❚" : "▶"}</button>
            <button type="button" className="ma-btn" onClick={clock.reset} aria-label="처음부터">↺</button>
          </>
        )}
        {controls}
      </div>
    </div>
  );
}

export function Slider({ label, value, min, max, step = 1, onChange, show }) {
  return (
    <label className="ma-sl">
      <span>{label}</span>
      <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} />
      <b>{show ? show(value) : fmt(value)}</b>
    </label>
  );
}

export function Seg({ value, options, onChange }) {
  return (
    <span className="ma-seg" role="radiogroup">
      {options.map(([v, label]) => (
        <button key={String(v)} type="button" role="radio" aria-checked={v === value} className={v === value ? "on" : ""} onClick={() => onChange(v)}>{label}</button>
      ))}
    </span>
  );
}

/** 좌표 — 수학 좌표 ↔ 그림 좌표. pad = [위, 오른쪽, 아래, 왼쪽] */
export function plot({ x0, x1, y0, y1, W = 360, H = 220, pad = [14, 12, 24, 32] }) {
  const [pt, pr, pb, pl] = pad;
  const X = (x) => pl + ((x - x0) / (x1 - x0)) * (W - pl - pr);
  const Y = (y) => H - pb - ((y - y0) / (y1 - y0)) * (H - pt - pb);
  const ix = (px) => x0 + ((px - pl) / (W - pl - pr)) * (x1 - x0);
  /** 함수 곡선 — 화면 밖으로 크게 튀는 곳(점근선)은 끊는다 */
  const path = (f, a = x0, b = x1, n = 180) => {
    let d = "", pen = false;
    for (let i = 0; i <= n; i++) {
      const x = a + ((b - a) * i) / n, y = f(x);
      if (!Number.isFinite(y) || y > y1 + (y1 - y0) * 3 || y < y0 - (y1 - y0) * 3) { pen = false; continue; }
      const yy = clamp(y, y0 - (y1 - y0), y1 + (y1 - y0));
      d += (pen ? "L" : "M") + X(x).toFixed(1) + " " + Y(yy).toFixed(1);
      pen = true;
    }
    return d || "M0 0";
  };
  /** 매개 곡선 (x(t), y(t)) */
  const curve = (fx, fy, a, b, n = 180) => {
    let d = "";
    for (let i = 0; i <= n; i++) { const t = a + ((b - a) * i) / n; d += (i ? "L" : "M") + X(fx(t)).toFixed(1) + " " + Y(fy(t)).toFixed(1); }
    return d;
  };
  const poly = (pts) => pts.map(([x, y], i) => (i ? "L" : "M") + X(x).toFixed(1) + " " + Y(y).toFixed(1)).join("") || "M0 0";
  return { X, Y, ix, path, curve, poly, x0, x1, y0, y1, W, H, l: pl, r: W - pr, t: pt, b: H - pb };
}

/** 눈금 고르기 — 1 · 2 · 5 × 10ⁿ */
export function ticks(a, b, want = 5) {
  const span = b - a;
  if (!(span > 0)) return [];
  const raw = span / want, mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const st = [1, 2, 5, 10].map((k) => k * mag).find((s) => span / s <= want + 1) || 10 * mag;
  const out = [];
  for (let v = Math.ceil(a / st) * st; v <= b + 1e-9; v += st) out.push(Math.abs(v) < 1e-12 ? 0 : v);
  return out;
}

/** 축 — 원점을 지나는 축(범위 밖이면 가장자리) + 눈금 숫자 */
export function Axes({ p, xl = "x", yl = "y", xt, yt, grid = true, xfmt = (v) => fmt(v, 2), yfmt = (v) => fmt(v, 2) }) {
  const xs = xt || ticks(p.x0, p.x1, 6), ys = yt || ticks(p.y0, p.y1, 4);
  const ax = clamp(p.Y(0), p.t, p.b), ay = clamp(p.X(0), p.l, p.r);
  return (
    <g fontSize="10" fill={C.mut}>
      {grid && xs.map((v) => <line key={"gx" + v} x1={p.X(v)} x2={p.X(v)} y1={p.t} y2={p.b} stroke={C.bd} strokeWidth="0.7" />)}
      {grid && ys.map((v) => <line key={"gy" + v} y1={p.Y(v)} y2={p.Y(v)} x1={p.l} x2={p.r} stroke={C.bd} strokeWidth="0.7" />)}
      <line x1={p.l} x2={p.r} y1={ax} y2={ax} stroke={C.mut} strokeWidth="1.1" />
      <line y1={p.t} y2={p.b} x1={ay} x2={ay} stroke={C.mut} strokeWidth="1.1" />
      {xs.map((v) => (v === 0 ? null : <text key={"tx" + v} x={p.X(v)} y={Math.min(p.b + 13, ax + 13)} textAnchor="middle">{xfmt(v)}</text>))}
      {ys.map((v) => (v === 0 ? null : <text key={"ty" + v} x={Math.max(p.l - 4, ay - 4)} y={p.Y(v) + 3.5} textAnchor="end">{yfmt(v)}</text>))}
      <text x={p.r} y={ax - 5} textAnchor="end" fontStyle="italic" fill={C.ink}>{xl}</text>
      <text x={ay + 5} y={p.t + 9} fontStyle="italic" fill={C.ink}>{yl}</text>
    </g>
  );
}

/** 화살표 */
export function Arrow({ x1, y1, x2, y2, color = C.ink, w = 1.6, head = 6, dash }) {
  const a = Math.atan2(y2 - y1, x2 - x1), L = Math.hypot(x2 - x1, y2 - y1);
  if (!(L > 0.5)) return null;
  const h = Math.min(head, L * 0.5);
  const hx = x2 - h * Math.cos(a), hy = y2 - h * Math.sin(a);
  return (
    <g>
      <line x1={x1} y1={y1} x2={hx} y2={hy} stroke={color} strokeWidth={w} strokeDasharray={dash} />
      <polygon points={`${x2},${y2} ${hx - h * 0.45 * Math.sin(a)},${hy + h * 0.45 * Math.cos(a)} ${hx + h * 0.45 * Math.sin(a)},${hy - h * 0.45 * Math.cos(a)}`} fill={color} />
    </g>
  );
}

/** 행렬 — 읽을거리 줄 안의 작은 행렬(괄호 모양). m 은 행 우선 성분, c 는 열 수 */
export function Mat({ m, c = 2 }) {
  return (
    <span className="ma-mat" style={{ gridTemplateColumns: `repeat(${c}, auto)` }}>
      {m.map((v, i) => <span key={i}>{typeof v === "number" ? fmt(v, 2) : v}</span>)}
    </span>
  );
}

/** 이름표 글자 폭 어림 — 한글 · 기호는 넓게 */
const textW = (s, size) => [...String(s)].reduce((w, ch) => w + (/[\u1100-\u11ff\u3130-\u318f\uac00-\ud7a3\u2190-\u22ff]/.test(ch) ? size * 0.98 : ch === " " ? size * 0.3 : size * 0.58), 0);

/** 글자 — 그림 위 이름표(bg 면 뒤에 바탕을 깔아 눈금 · 선과 겹쳐도 읽힌다) */
export function Label({ x, y, children, color = C.ink, size = 11, anchor = "start", bold = false, bg = false }) {
  const w = textW(children, size) + 6;
  return (
    <g>
      {bg && <rect x={anchor === "middle" ? x - w / 2 : anchor === "end" ? x - w + 3 : x - 3} y={y - size + 0.5} width={w} height={size + 4.5} rx="3" fill={C.card} opacity="0.9" />}
      <text x={x} y={y} fill={color} fontSize={size} textAnchor={anchor} fontWeight={bold ? 800 : 500}>{children}</text>
    </g>
  );
}
