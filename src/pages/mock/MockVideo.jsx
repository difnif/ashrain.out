// ashrain.out — 학교별 모의고사 「해설 영상」(#/mock/<id>/video[?i=N&from=av])
// 시험의 문항을 교실 모니터처럼 차례로 넘겨 보여 준다 — 문항마다 「문제」(시험지에서 그 칸만) → 「풀이」(보관함 해설그림:
//   선택형은 읽기 표시 · 정답 · 풀이, 서답형은 모범 답안 · 채점 기준). 해설그림이 없으면 정답 · 채점 요소 카드. 마지막 다음은 처음.
//   조작 막대(화면을 건드리면 뜨고 3.6초 뒤 숨는다): 이전 · 멈춤 · 다음 · 문제 | 풀이 · 빠르기 · 밝기 · 번호 목록 · 전체 화면 · 나가기
//   키보드 ←/→ 문항 · ↑/↓ 문제 | 풀이 · 스페이스 멈춤 · L 목록 · F 전체 화면 · Esc 나가기. 재생 중에는 화면 꺼짐 방지(wake lock).
//   시청각 학습 › 학교별 모의고사(from=av)에서 열면 나가기가 그 목록으로, 시험 화면에서 열면 시험 화면으로.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { fileUrl, choiceText } from "../../lib/mockexams";
import { ItemCrop, Rich } from "./parts";

const IDLE_MS = 3600;
const SPEEDS = [0.75, 1, 1.5, 2];
const DUR = { mc: { q: 7000, s: 16000 }, sa: { q: 10000, s: 30000 }, card: 10000 };
const TK = "ash.mock.video.theme";
const SK = "ash.mock.video.speed";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, String(v)); } catch { /* 사생활 모드 등 */ } };

/** 문항 칸(잘라 본 띠들)의 가로 : 세로 */
function cropRatio(exam, it) {
  const pg = exam.docs.find((d) => d.id === "problems")?.pages?.[it.box.p];
  if (!pg) return 1;
  const segs = it.seg?.length ? it.seg : [{ y: it.box.y, h: it.box.h }];
  const h = segs.reduce((a, s) => a + s.h, 0) * pg.h;
  return h > 0 ? (it.box.w * pg.w) / h : 1;
}

export default function MockVideo({ exam, school, at, back }) {
  const items = exam.items;
  const n = items.length;
  const start = Math.max(0, items.findIndex((x) => x.i === at));
  const [k, setK] = useState(start);
  const [ph, setPh] = useState("q");                       // "q" 문제 | "s" 풀이
  const [playing, setPlaying] = useState(true);
  const [si, setSi] = useState(() => { const v = Number(lsGet(SK, 1)); return SPEEDS[v] ? v : 1; });
  const [thm, setThm] = useState(() => (lsGet(TK, "dark") === "light" ? "light" : "dark"));
  const [ctl, setCtl] = useState(true);
  const [list, setList] = useState(false);
  const [fs, setFs] = useState(false);
  const rootRef = useRef(null), stageRef = useRef(null);
  const [box, setBox] = useState({ w: 0, h: 0 });
  const it = items[k];
  const sol = it?.sol?.img ? it.sol : null;
  const dur = Math.round((ph === "q" ? DUR[it.kind].q : sol ? DUR[it.kind].s : DUR.card) / SPEEDS[si]);

  // 무대 크기 — 문제 칸 · 해설그림을 무대에 맞춰 키운다
  useEffect(() => {
    const el = stageRef.current;
    if (!el) return undefined;
    const fit = () => setBox({ w: el.clientWidth, h: el.clientHeight });
    fit();
    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(fit) : null;
    ro?.observe(el);
    return () => ro?.disconnect();
  }, []);

  // 흐름 — 멈췄다 이어 가도 그 단계의 남은 시간만큼(막대 애니메이션과 같은 시계)
  const clock = useRef({ key: "", used: 0, since: 0 });
  const next = useCallback(() => {
    if (ph === "q") setPh("s");
    else { setPh("q"); setK((v) => (v + 1) % n); }
  }, [ph, n]);
  useEffect(() => {
    const key = `${k}-${ph}-${si}`;
    const c = clock.current;
    if (c.key !== key) { c.key = key; c.used = 0; }
    if (!playing) return undefined;
    c.since = Date.now();
    const t = setTimeout(next, Math.max(0, dur - c.used));
    return () => { clearTimeout(t); c.used += Date.now() - c.since; };
  }, [k, ph, si, playing, dur, next]);

  // 조작 막대 — 건드리면 뜨고 잠시 뒤 숨는다(목록이 열려 있거나 멈췄으면 그대로)
  const idle = useRef(0);
  const poke = useCallback(() => {
    setCtl(true);
    clearTimeout(idle.current);
    idle.current = setTimeout(() => setCtl(false), IDLE_MS);
  }, []);
  useEffect(() => { poke(); return () => clearTimeout(idle.current); }, [poke]);

  const go = useCallback((v, p = "q") => { setK(((v % n) + n) % n); setPh(p); poke(); }, [n, poke]);
  const exit = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
    location.hash = back;
  }, [back]);
  const toggleFs = useCallback(() => {
    const el = rootRef.current;
    if (!document.fullscreenElement) {
      el?.requestFullscreen?.().then(() => { try { screen.orientation?.lock?.("landscape").catch(() => {}); } catch { /* 무시 */ } }).catch(() => {});
    } else document.exitFullscreen?.().catch(() => {});
  }, []);
  useEffect(() => {
    const on = () => setFs(!!document.fullscreenElement);
    document.addEventListener("fullscreenchange", on);
    return () => document.removeEventListener("fullscreenchange", on);
  }, []);

  // 키보드
  useEffect(() => {
    const on = (e) => {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      const kk = e.key;
      if (kk === "ArrowRight") { go(k + 1); e.preventDefault(); }
      else if (kk === "ArrowLeft") { go(k - 1); e.preventDefault(); }
      else if (kk === "ArrowDown" || kk === "ArrowUp") { setPh((p) => (p === "q" ? "s" : "q")); poke(); e.preventDefault(); }
      else if (kk === " ") { setPlaying((p) => !p); poke(); e.preventDefault(); }
      else if (kk === "l" || kk === "L") { setList((v) => !v); poke(); }
      else if (kk === "f" || kk === "F") toggleFs();
      else if (kk === "Escape") { if (list) setList(false); else if (!document.fullscreenElement) exit(); }
    };
    window.addEventListener("keydown", on);
    return () => window.removeEventListener("keydown", on);
  }, [k, go, poke, toggleFs, exit, list]);

  // 화면 꺼짐 방지
  useEffect(() => {
    if (!playing || !navigator.wakeLock?.request) return undefined;
    let lock = null, live = true;
    navigator.wakeLock.request("screen").then((l) => { if (live) lock = l; else l.release?.(); }).catch(() => {});
    return () => { live = false; lock?.release?.().catch?.(() => {}); };
  }, [playing]);

  // 무대에 맞춘 너비
  const fitW = (ratio) => Math.max(120, Math.min(box.w * 0.97, box.h * 0.95 * ratio));
  const ratio = useMemo(() => (it ? cropRatio(exam, it) : 1), [exam, it]);
  const lbl = (x) => (x.kind === "mc" ? `${x.label}번` : x.label);
  const setSpeed = () => { const v = (si + 1) % SPEEDS.length; setSi(v); lsSet(SK, v); poke(); };
  const setTheme = () => { const v = thm === "dark" ? "light" : "dark"; setThm(v); lsSet(TK, v); poke(); };

  return (
    <div ref={rootRef} className={`mxv mxv-${thm}${ctl ? " ctl" : ""}`} onPointerDown={poke} onMouseMove={poke}>
      <div className="mxv-top">
        <span className="mxv-no">{it.kind === "mc" ? it.label : `서${it.no}`}</span>
        <span className="mxv-tt"><b>{lbl(it)} · {it.pts}점</b><small><Rich text={it.unit} /></small></span>
        <span className={"mxv-ph " + ph}>{ph === "q" ? "문제" : sol ? (it.kind === "sa" ? "모범 답안 · 채점" : "풀이") : "정답"}</span>
        {ph === "s" && <span className="mxv-ans">{it.kind === "mc" ? <>정답 <b>{choiceText(it.ans)}</b></> : <>답 <Rich text={it.answer} /></>}</span>}
        <span className="mxv-ct">{k + 1}/{n}</span>
      </div>
      <div ref={stageRef} className="mxv-stage">
        {box.w > 0 && (ph === "q" ? (
          <div className="mxv-crop" style={{ width: fitW(ratio) }}><ItemCrop exam={exam} it={it} /></div>
        ) : sol ? (
          <img className="mxv-sol" src={fileUrl(exam, sol.img)} alt={`${lbl(it)} 해설`} style={{ width: fitW(sol.w / sol.h) }} draggable={false} />
        ) : (
          <div className="mxv-card">
            <div className="a">{it.kind === "mc" ? <>정답 <b>{choiceText(it.ans)}</b></> : <><span>답</span> <Rich text={it.answer} /></>}</div>
            {it.kind === "sa" && it.rubric?.length > 0 && (
              <ul>{it.rubric.map(([t, p], j) => <li key={j}><Rich text={t} /> <b>({p}점)</b></li>)}</ul>
            )}
          </div>
        ))}
        {/* 다음 문항 그림을 미리 받아 둔다 */}
        {items[(k + 1) % n]?.sol?.img && <link rel="prefetch" href={fileUrl(exam, items[(k + 1) % n].sol.img)} />}
      </div>
      <div className="mxv-prog" aria-hidden="true">
        <i key={`${k}-${ph}-${si}`} style={{ animationDuration: `${dur}ms`, animationPlayState: playing ? "running" : "paused" }} />
      </div>
      {!playing && <div className="mxv-paused">⏸ 멈춤 — 스페이스 · ▶로 이어서</div>}

      <div className="mxv-ctl" role="toolbar" aria-label="해설 영상 조작" aria-hidden={!ctl}>
        <button type="button" onClick={() => go(k - 1)} aria-label="이전 문항" title="이전 문항 (←)">⏮</button>
        <button type="button" className="big" onClick={() => { setPlaying((p) => !p); poke(); }} aria-label={playing ? "멈춤" : "재생"} title="멈춤 · 재생 (스페이스)">{playing ? "⏸" : "▶"}</button>
        <button type="button" onClick={() => go(k + 1)} aria-label="다음 문항" title="다음 문항 (→)">⏭</button>
        <span className="sep" />
        <span className="mxv-seg" role="radiogroup" aria-label="문제 · 풀이">
          <button type="button" role="radio" aria-checked={ph === "q"} className={ph === "q" ? "on" : ""} onClick={() => { setPh("q"); poke(); }}>문제</button>
          <button type="button" role="radio" aria-checked={ph === "s"} className={ph === "s" ? "on" : ""} onClick={() => { setPh("s"); poke(); }}>풀이</button>
        </span>
        <button type="button" className="tx" onClick={setSpeed} title="빠르기">{SPEEDS[si]}×</button>
        <button type="button" onClick={setTheme} aria-label="밝기" title="밝기">{thm === "dark" ? "🌙" : "☀️"}</button>
        <button type="button" onClick={() => { setList((v) => !v); poke(); }} aria-label="번호 목록" title="번호 목록 (L)">☰</button>
        <button type="button" onClick={toggleFs} aria-label="전체 화면" title="전체 화면 (F)">{fs ? "🗗" : "⛶"}</button>
        <button type="button" onClick={exit} aria-label="나가기" title="나가기 (Esc)">✕</button>
      </div>

      {list && (
        <div className="mxv-list" role="dialog" aria-label="문항 고르기" onPointerDown={(e) => e.stopPropagation()}>
          <div className="mxv-list-in">
            <div className="mxv-list-h"><b>{school?.short || ""} {exam.title} · {exam.ed}</b><button type="button" onClick={() => setList(false)} aria-label="닫기">✕</button></div>
            <div className="mxv-grid">
              {items.map((x, j) => (
                <button key={x.i} type="button" className={"mxv-chip" + (j === k ? " on" : "") + (x.kind === "sa" ? " sa" : "")}
                  onClick={() => { go(j); setList(false); }}>
                  <b>{x.kind === "mc" ? x.label : `서${x.no}`}</b><small><Rich text={x.unit} /></small>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
      <div className="mxv-rot">가로로 돌리면 크게 보여요</div>
    </div>
  );
}
