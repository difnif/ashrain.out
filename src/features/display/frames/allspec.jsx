// ashrain.out — 듀얼 모드 「문제 풀이 해설 전부」 (frames/allspec.jsx)
// 해설 액자(공통 틀 frames/lesson.jsx)를 듀얼로 나누면 판마다 이 액자의 세트가 아니라 문제 풀이 해설 전부에서 고른다:
//   📚 단원 100제(초등 · 중등 · 고등 — e-ten) · 🧩 유형(단원의 한 단계 20문항 — e-ten.3) · 🗓 주차별 회차(학년마다 104 — w-e3-07a)
//   · 🎬 해설 액자 세트(그래프 그리기 「graph:basic」 · 10단계 계산 「lin10:1」 · 그래프와 넓이 「area:A」 · 경우의 수와 확률 100제 「cnt100:sel」).
//   왼쪽엔 중2 일차함수 단원, 오른쪽엔 초3 회차처럼 — 학교급 · 학년 · 액자가 달라도 된다. 문항은 고를 때 들여온다.
// 액자마다 「전부」 spec 이 하나씩(기억 이름 <액자>.all — 기본기 해설은 단원 · 유형 · 주차별 보기가 한 기억 dualLsk) —
//   듀얼 두 판의 자리 · 고른 것을 액자마다 따로 기억하고, 처음 열면 두 판 다 단일 모드에서 보던 것(예전 듀얼 기억이 있으면 그대로 옮겨 온다).
// lesson.jsx 가 이 파일을 들이면 액자 모듈과 서로 물리므로, 이 파일이 읽힐 때 setDualAll 로 넣어 둔다(AdminDisplay 가 들인다).
// 📄 문서(문제지 · 해설지 · 빠른 정답 · OMR)는 단원 · 유형 · 회차 판에만 — 해설 액자 세트는 프린트 문서가 없다.
import { useEffect, useMemo, useState } from "react";
import { GD_SPEC } from "./graphdraw.jsx";
import { L10_SPEC } from "./lin10.jsx";
import { AREA_SPEC } from "./area.jsx";
import { C100_SPEC } from "./cnt100.jsx";
import { basicScenes, TYPE_NO } from "./basics.jsx";
import { DocsMenu } from "./docsmenu.jsx";
import { setDualAll } from "./lesson.jsx";
import { lsRead, lsWrite } from "./xkit.jsx";
import { LEVELS, basicOf, basicsOf, levelOf } from "../basics/index.js";
import { WGRADES, gradeOf, loadWeekIndex, weekIndexCached, weekMetaCached, parseWeekId, PERIODS, KIND_ICON, weekOfDate } from "../weeks/index.js";
import { avSource } from "../../../lib/avsrc.js";
import { typeMeta, typesOf } from "../../../lib/avtypes.js";
import { unitLabel } from "../../../lib/units.js";

/** 해설 액자 넷 — 세트 key 앞에 액자 key 를 붙인다(「graph:basic」) */
export const LESSON_FRAMES = [
  { fk: "graph", spec: GD_SPEC, icon: "📈", short: "그래프 그리기" },
  { fk: "lin10", spec: L10_SPEC, icon: "🔢", short: "10단계 계산" },
  { fk: "area", spec: AREA_SPEC, icon: "📐", short: "그래프와 넓이" },
  { fk: "cnt100", spec: C100_SPEC, icon: "🎯", short: "경우의 수 100제" },
];
const FRAME_RE = new RegExp(`^(${LESSON_FRAMES.map((f) => f.fk).join("|")}):(.+)$`);
const STAGES5 = [1, 2, 3, 4, 5];

/** key 하나 → 무엇인가 — { key, kind: "frame" | "unit" | "type" | "week", … } | null */
const SRC = new Map();
export function allSource(k) {
  const key = String(k ?? "");
  if (SRC.has(key)) return SRC.get(key);
  let r = null;
  const m = FRAME_RE.exec(key);
  if (m) {
    const F = LESSON_FRAMES.find((f) => f.fk === m[1]), S = F.spec.sets.find((x) => String(x.key) === m[2]);
    if (S) r = { key, kind: "frame", F, fs: F.spec, set: S.key, S };
  } else r = avSource(key);
  SRC.set(key, r);
  return r;
}
/** 이 액자(origin)의 세트 key → 「전부」 key */
const toAll = (origin, set) => {
  const F = LESSON_FRAMES.find((f) => f.spec === origin);
  return F ? `${F.fk}:${set}` : set;
};

/** 세트 이름표 */
function labelOf(key) {
  const r = allSource(key);
  if (!r) return null;
  if (r.kind === "frame") return { key, name: `${r.fs.title} · ${r.S.name}`, short: `${r.F.short} ${r.S.short || r.S.name}`, icon: r.F.icon, sub: r.S.name };
  if (r.kind === "unit") { const b = basicOf(key); return { key, name: b.title, short: b.short, icon: b.icon, note: b.span, sub: unitLabel(b.unit) }; }
  if (r.kind === "type") { const m = typeMeta(key); return { key, name: m.title, short: m.short, icon: TYPE_NO[m.st], note: m.span, sub: `${m.name} · ${unitLabel(m.unit)}` }; }
  const m = weekMetaCached(key), p = parseWeekId(key), g = gradeOf(p.gk);
  return m ? { key, name: `${m.grade} ${m.week}주 ${m.slot} · ${m.title}`, short: `${m.grade} ${m.week}주 ${m.slot}`, icon: KIND_ICON[m.kind] || "🗓", note: m.kind, sub: m.title }
    : { key, name: `${g.grade} ${p.week}주 ${p.slot}`, short: `${g.grade} ${p.week}주 ${p.slot}`, icon: "🗓" };
}

/** 액자 하나의 「전부」 spec — 액자마다 한 번 만든다 */
const SPECS = new Map();
export function allSpecFor(origin) {
  if (!origin?.lsk) return null;
  if (SPECS.has(origin.lsk)) return SPECS.get(origin.lsk);
  const lsk = `${origin.dualLsk || origin.lsk}.all`;
  // 예전 듀얼 기억(이 액자 세트끼리) → 「전부」 key 로 옮겨 온다(한 번)
  const old = lsRead(`${origin.lsk}.dual`);
  if (old && !lsRead(`${lsk}.dual`)) {
    const mv = (p) => (p && p.set != null ? { ...p, set: toAll(origin, p.set) } : p);
    lsWrite(`${lsk}.dual`, { L: mv(old.L), R: mv(old.R) });
  }
  const spec = {
    all: true, lsk, title: origin.title, defSet: toAll(origin, origin.defSet ?? origin.sets?.[0]?.key), cols: 5,
    setMenu: { word: "콘텐츠", title: "문제 풀이 해설 전부" },
    single0: () => { const o = lsRead(origin.lsk) || {}; const v = o.set ?? o.id; return v == null ? null : toAll(origin, v); },
    hasSet: (k) => !!allSource(k),
    setOf: (k) => labelOf(k),
    stages: (k) => {
      const r = allSource(k);
      if (!r) return [];
      if (r.kind === "frame") return r.fs.stages(r.set);
      if (r.kind === "type") return [];
      const m = r.meta();
      return STAGES5.map((v) => ({ v, lab: `${v}단계${m?.stages?.[v] ? ` ${m.stages[v]}` : ""}` }));
    },
    ready: (k) => { const r = allSource(k); return !r ? true : r.kind === "frame" ? (r.fs.ready ? r.fs.ready(r.set) : true) : r.ready(); },
    load: (k) => {
      const r = allSource(k);
      if (!r) return Promise.reject(new Error(`없는 콘텐츠: ${k}`));
      return r.kind === "frame" ? Promise.resolve(r.fs.load ? r.fs.load(r.set) : null) : r.load();
    },
    scenes: (k, sp, st) => { const r = allSource(k); return r.kind === "frame" ? r.fs.scenes(r.set, sp, st) : basicScenes(r.meta(), r.set(), sp, st); },
    paneHead: (S, s) => { const r = allSource(S.key); return r?.kind === "frame" && r.fs.paneHead ? r.fs.paneHead(r.S, s) : null; },
    topExtra: ({ set, open, onOpen, poke }) => {
      const r = allSource(set);
      if (!r || r.kind === "frame" || !r.ready()) return null;
      return <DocsMenu meta={r.meta()} set={r.set()} open={open} onOpen={onOpen} poke={poke} />;
    },
    titleOf: (k) => {
      const r = allSource(k);
      if (!r) return origin.title;
      if (r.kind === "frame") return r.fs.title;
      if (r.kind === "week") return `${gradeOf(parseWeekId(k).gk).grade} 주차별 기초 다지기`;
      return levelOf(r.meta()?.level)?.title || origin.title;
    },
    colsOf: (k) => { const r = allSource(k); return r?.kind === "frame" ? r.fs.cols || 5 : 5; },
    Menu: AllMenu,
  };
  SPECS.set(origin.lsk, spec);
  return spec;
}
setDualAll(allSpecFor);

/* ══════════ 목록 — 단원 100제 · 유형 · 주차별 · 해설 액자 ══════════ */
const TABS = [
  { k: "unit", lab: "📚 단원 100제", hint: "단원 100문항 전부 — 학년을 넘나드는 단원, 고르면 그 판이 1번부터 돌아요" },
  { k: "type", lab: "🧩 유형", hint: "단원 100제를 단계마다 나눈 20문항 — 번호 1 ~ 20 · 프린트도 유형마다 따로" },
  { k: "week", lab: "🗓 주차별", hint: "학년마다 주 2회(A · B) × 52주 = 104회차 · 회차마다 20문항" },
  { k: "frame", lab: "🎬 해설 액자", hint: "학원 프린트 문항 해설 — 일차함수 그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 경우의 수와 확률 100제" },
];
const LVS = LEVELS.map((L) => L.level);

/** 지금 판이 보는 것으로 처음 탭 · 학교급 · 학년 */
function startOf(cur) {
  const r = allSource(cur);
  const m = r && r.kind !== "frame" ? r.meta() : null;
  const p = r?.kind === "week" ? parseWeekId(cur) : null;
  const lv = (r?.kind === "unit" || r?.kind === "type") ? m?.level : p ? gradeOf(p.gk).level : "중등";
  const gk = p ? p.gk : (WGRADES.find((g) => g.level === lv) || WGRADES[0]).gk;
  return { tab: r ? (r.kind === "frame" ? "frame" : r.kind) : "unit", lv: LVS.includes(lv) ? lv : LVS[0], gk };
}

function AllMenu({ cur, side = "", onPick, onClose }) {
  const st0 = useMemo(() => startOf(cur), [cur]);
  const [tab, setTab] = useState(st0.tab);
  const [lv, setLv] = useState(st0.lv);
  const [gk, setGk] = useState(st0.gk);
  const [h, setH] = useState(() => weekIndexCached(st0.gk));
  const [err, setErr] = useState(null);
  useEffect(() => {
    if (tab !== "week") return undefined;
    const c = weekIndexCached(gk);
    setErr(null);
    if (c) { setH(c); return undefined; }
    setH(null);
    let live = true;
    loadWeekIndex(gk).then((v) => { if (live) setH(v); }).catch(() => { if (live) setErr("회차 목록을 불러오지 못했어요"); });
    return () => { live = false; };
  }, [tab, gk]);
  const rows = useMemo(() => {
    if (tab === "unit") return basicsOf(lv).map((b) => ({ key: b.id, icon: b.icon, short: b.short, note: b.span, sub: unitLabel(b.unit) }));
    if (tab === "type") {
      return basicsOf(lv).flatMap((b) => typesOf(b.id).map((m) => ({ key: m.id, icon: TYPE_NO[m.st], short: m.name, note: m.span, sub: unitLabel(m.unit),
        grp: `${b.icon} ${b.title} · ${b.span}` })));
    }
    if (tab === "week") {
      if (!h || h.gk !== gk) return [];
      const now = Math.min(52, Math.max(1, weekOfDate().week));
      return h.sessions.map((m) => {
        const p = PERIODS.find((x) => m.week >= x.from && m.week <= x.to);
        return { key: m.id, icon: KIND_ICON[m.kind] || "•", short: `${m.week}주 ${m.slot}`, note: m.kind, sub: `${m.title} · ${unitLabel(m.unit)}`,
          grp: p ? `${p.key} · ${p.from} ~ ${p.to}주` : "", hot: m.week === now };
      });
    }
    return LESSON_FRAMES.flatMap((F) => F.spec.sets.map((S) => ({ key: `${F.fk}:${S.key}`, icon: F.icon, short: S.short || S.name, sub: S.name,
      grp: `${F.icon} ${F.spec.title}` })));
  }, [tab, lv, gk, h]);
  const T = TABS.find((x) => x.k === tab);
  const stop = (e) => e.stopPropagation();
  return (
    <div className="dsp-list" onPointerDown={stop} onClick={onClose}>
      <div className="dsp-list-in" onClick={stop} role="dialog" aria-label="문제 풀이 해설 전부">
        <style>{ALL_CSS}</style>
        <div className="dsp-list-h">
          <b>{side ? `${side} 판 · ` : ""}문제 풀이 해설 전부</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="dsp-chips all-tabs" role="tablist" aria-label="콘텐츠 종류">
          {TABS.map((x) => (
            <button key={x.k} type="button" role="tab" aria-selected={tab === x.k} className={"dsp-chip" + (tab === x.k ? " on" : "")} onClick={() => setTab(x.k)}>{x.lab}</button>
          ))}
        </div>
        {(tab === "unit" || tab === "type") && (
          <div className="dsp-chips all-sub" role="group" aria-label="학교급">
            {LVS.map((l) => <button key={l} type="button" className={"dsp-chip" + (lv === l ? " on" : "")} aria-pressed={lv === l} onClick={() => setLv(l)}>{l}</button>)}
          </div>
        )}
        {tab === "week" && (
          <div className="dsp-chips all-sub" role="group" aria-label="학년">
            {WGRADES.map((g) => <button key={g.gk} type="button" className={"dsp-chip" + (gk === g.gk ? " on" : "")} aria-pressed={gk === g.gk} onClick={() => setGk(g.gk)}>{g.grade}</button>)}
          </div>
        )}
        <p className="dsp-gal-sub">{T.hint}</p>
        {tab === "week" && !rows.length ? <p className="dsp-gal-sub">{err || "회차 목록을 불러오는 중…"}</p> : (
          <div className="lsn-sets">
            {rows.map((b, i) => [
              b.grp && b.grp !== rows[i - 1]?.grp ? <div key={"g" + b.key} className="lsn-grp">{b.grp}</div> : null,
              <button key={b.key} type="button" className={"lsn-set" + (b.key === cur ? " on" : "") + (b.hot ? " hot" : "")} onClick={() => onPick(b.key)}
                ref={b.key === cur ? (el) => el?.scrollIntoView?.({ block: "center" }) : undefined}>
                <span className="i" aria-hidden="true">{b.icon || "•"}</span>
                <span className="t">{b.short}{b.note && <small>{b.note}</small>}</span>
                <span className="u">{b.sub}</span>
              </button>,
            ])}
          </div>
        )}
      </div>
    </div>
  );
}

const ALL_CSS = `
.all-tabs { margin: .2cqw 0 .4cqw; }
.all-sub { margin: 0 0 .3cqw; }
.all-sub .dsp-chip { opacity: .9; }
`;
