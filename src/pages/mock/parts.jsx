// ashrain.out — 학교별 모의고사 화면 공용: 계정 · 관리자 · 시험 불러오기 · 문항 잘라 보기 · 답 고르기 · 서답형 답 쓰기 · 스스로 채점 · 시청각 해설 고리
import { useEffect, useMemo, useState } from "react";
import { supabase } from "../../supabaseClient";
import { avItem } from "../../lib/av";
import { parseTypeKey, typeMeta } from "../../lib/avtypes";
import {
  loadMockExam, loadMockIndex, setMockUser, fileUrl, richHtml, CIRCLED, rubricScore, rubricPart, avHref, avLinksOf, isAnswered,
} from "../../lib/mockexams";
import InkPad from "../sets/InkPad";
import { hasInk, inkSvg } from "../sets/ink";

// ── 글꼴: 채점 표시(빨간 색연필 글씨) Gaegu · 보기 번호 ①~⑤ 명조 ──────────────────
let fontsDone = false;
export function ensureMockFonts() {
  if (fontsDone || typeof document === "undefined") return;
  fontsDone = true;
  const l = document.createElement("link");
  l.rel = "stylesheet";
  l.href = "https://fonts.googleapis.com/css2?family=Gaegu:wght@700&family=Noto+Serif+KR:wght@500;700&display=swap";
  document.head.appendChild(l);
}

// ── 계정 · 관리자 ─────────────────────────────────────────────────────────────
let uidCache;
/** 로그인한 계정 id — undefined 확인 중 | "" 없음 | id (확인되면 진도 열쇠를 계정별로) */
export function useMockUser() {
  const [uid, setUid] = useState(() => { if (uidCache !== undefined) setMockUser(uidCache); return uidCache; });
  useEffect(() => {
    let alive = true;
    supabase.auth.getSession().then(({ data }) => {
      const id = data?.session?.user?.id || "";
      uidCache = id; setMockUser(id);
      if (alive) setUid(id);
    }).catch(() => { uidCache = ""; setMockUser(""); if (alive) setUid(""); });
    return () => { alive = false; };
  }, []);
  return uid;
}
let adminCache = null;
/** 관리자인가 — null 확인 중 | true | false (강사 모드) */
export function useIsAdmin() {
  const [a, setA] = useState(adminCache);
  useEffect(() => {
    if (adminCache !== null) return undefined;
    let alive = true;
    supabase.auth.getUser().then(async ({ data }) => {
      const u = data?.user;
      if (!u) { adminCache = false; if (alive) setA(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", u.id).maybeSingle();
      adminCache = p?.role === "admin";
      if (alive) setA(adminCache);
    }).catch(() => { if (alive) setA(false); });
    return () => { alive = false; };
  }, []);
  return a;
}

// ── 불러오기 ──────────────────────────────────────────────────────────────────
export function useMockIndex() {
  const [st, setSt] = useState({ index: null, err: null });
  useEffect(() => {
    let alive = true;
    loadMockIndex().then((index) => { if (alive) setSt({ index, err: null }); })
      .catch((e) => { if (alive) setSt({ index: null, err: e?.message || String(e) }); });
    return () => { alive = false; };
  }, []);
  return st;
}
export function useMockExam(id) {
  const [st, setSt] = useState({ exam: null, school: null, err: null });
  useEffect(() => {
    let alive = true;
    setSt({ exam: null, school: null, err: null });
    Promise.all([loadMockExam(id), loadMockIndex().catch(() => null)])
      .then(([exam, index]) => { if (alive) setSt({ exam, school: (index?.schools || []).find((s) => s.id === exam.school) || null, err: null }); })
      .catch((e) => { if (alive) setSt({ exam: null, school: null, err: e?.message || String(e) }); });
    return () => { alive = false; };
  }, [id]);
  return st;
}

// ── 글자 꾸밈 ─────────────────────────────────────────────────────────────────
export function Rich({ text, as: Tag = "span", className }) {
  const html = useMemo(() => richHtml(text), [text]);
  return <Tag className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}

// ── 문항 잘라 보기 (쪽 그림에서 그 문항 칸만) — 보기 자리를 누를 수 있게 ────────────
/**
 * exam · it: 문항. sel: 고른 보기[] · mark: { ok[], bad[] }(채점 뒤 동그라미 · 빗금) · onPick(c): 보기 누르기(없으면 못 누름)
 * 문항 칸 안에서 글 · 그림이 있는 구간(it.seg)만 띠로 잘라 쌓는다 — 서답형의 빈 풀이 칸 · 선택형 아래 빈자리는 건너뛴다.
 */
export function ItemCrop({ exam, it, sel = [], mark = null, onPick }) {
  const doc = exam.docs.find((d) => d.id === "problems");
  const pg = doc?.pages?.[it.box.p];
  if (!pg) return null;
  const b = it.box;
  const segs = it.seg?.length ? it.seg : [{ y: b.y, h: b.h }];
  return (
    <div className="mx-crop">
      {segs.map((sg, k) => {
        const ar = (b.w * pg.w) / (sg.h * pg.h);
        const imgStyle = { width: `${100 / b.w}%`, left: `${(-b.x / b.w) * 100}%`, top: `${(-sg.y / sg.h) * 100}%` };
        return (
          <div key={k} className="mx-strip" data-seg={k} style={{ aspectRatio: String(ar) }}>
            <img src={fileUrl(exam, pg.img)} alt={k === 0 ? `${it.label} 문항` : ""} style={imgStyle} draggable={false} />
            {(it.ch || []).map((c, j) => {
              if (c.y < sg.y || c.y > sg.y + sg.h) return null;
              const n = j + 1;
              const on = sel.includes(n), ok = mark?.ok?.includes(n), bad = mark?.bad?.includes(n);
              const style = { left: `${((c.x - b.x) / b.w) * 100}%`, top: `${((c.y - sg.y) / sg.h) * 100}%`, width: `${((c.r * 3.4) / b.w) * 100}%` };
              return (
                <button key={n} type="button" className={"mx-chc" + (on ? " on" : "") + (ok ? " ok" : "") + (bad ? " bad" : "")} style={style}
                  disabled={!onPick} aria-label={`${CIRCLED[n]} 고르기`} aria-pressed={on} onClick={() => onPick?.(n)}>
                  <PencilRing on={on} ok={ok} bad={bad} seed={it.i * 7 + n} />
                </button>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}
/** 잘라 보기 상자(스크롤)에서 서답형 하위 문항 (n) 자리로 */
export function scrollCropTo(box, it, n) {
  const sub = (it.sub || []).find((x) => x.n === n);
  if (!box || !sub) return;
  const segs = it.seg?.length ? it.seg : [{ y: it.box.y, h: it.box.h }];
  const k = segs.findIndex((sg) => sub.y >= sg.y - 0.002 && sub.y <= sg.y + sg.h);
  const el = box.querySelector(`.mx-strip[data-seg="${Math.max(0, k)}"]`);
  if (!el) return;
  const sg = segs[Math.max(0, k)];
  const top = el.offsetTop + ((sub.y - sg.y) / sg.h) * el.offsetHeight - 6;
  box.scrollTo?.({ top: Math.max(0, top), behavior: "smooth" });
}

// 손으로 그은 듯한 동그라미 · 빗금 (연필 · 빨간 색연필)
const RING_D = "M31.5 8.6C26 3.2 12.6 3.4 7 12.3 2.6 19.6 7.4 33.4 20.4 35.3c10.6 1.4 17.2-6.8 15.9-16-.8-5.8-5.6-10.8-12-12.2";
const SLASH_D = "M8.5 33.5C15 25.5 22.5 15.5 32.5 5.5";
export const seedRot = (s) => (((s * 37) % 13) - 6) * 1.6;
export function PencilRing({ on, ok, bad, seed = 0 }) {
  if (!on && !ok && !bad) return null;
  const col = ok || bad ? "#d42a3c" : "#2c3a52";
  return (
    <svg viewBox="0 0 40 40" aria-hidden="true" style={{ transform: `rotate(${seedRot(seed)}deg)` }}>
      {(on || ok) && <path d={RING_D} fill="none" stroke={ok && !on ? "#d42a3c" : col} strokeWidth={ok && !on ? 2.2 : 2.8} strokeLinecap="round" opacity={on ? 0.92 : 0.8} />}
      {bad && <path d={SLASH_D} fill="none" stroke="#d42a3c" strokeWidth="2.6" strokeLinecap="round" />}
    </svg>
  );
}
export const RING_PATH = RING_D;
export const SLASH_PATH = SLASH_D;

// ── 선택형 답 고르기 판 (큰 단추 ①~⑤) ─────────────────────────────────────────
export function ChoicePad({ it, sel = [], onPick, disabled, mark = null }) {
  return (
    <div className="mx-cpad" role="group" aria-label={`${it.label}번 답 고르기`}>
      {[1, 2, 3, 4, 5].map((n) => {
        const on = sel.includes(n);
        const ok = mark?.ok?.includes(n), bad = mark?.bad?.includes(n);
        return (
          <button key={n} type="button" className={"mx-cb" + (on ? " on" : "") + (ok ? " ok" : "") + (bad ? " bad" : "")}
            aria-pressed={on} disabled={disabled} onClick={() => onPick(n)}>{CIRCLED[n]}</button>
        );
      })}
      {it.multi && <span className="mx-multi">정답 {it.ans.length}개 — 모두 골라요</span>}
    </div>
  );
}

// ── 서답형 답 쓰기 (하위 문항마다 손글씨 · 타자) ───────────────────────────────────
const MK = "ash.mock.inmode";
const lsGet = (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch { /* 무시 */ } };
export const partLabel = (n) => (n ? `(${n})` : "풀이와 답");

/** value: { k:"sa", parts:{ n: ink | {k:"text", raw} } } */
export function SaWriter({ it, value, onChange, onPart }) {
  const parts = it.parts?.length ? it.parts : [0];
  const [cur, setCurS] = useState(parts[0]);
  const setCur = (n) => { setCurS(n); onPart?.(n); };
  const [mode, setMode] = useState(() => {
    const p = value?.parts?.[parts[0]];
    if (p?.k === "ink") return "ink";
    if (p?.k === "text") return "type";
    const pref = lsGet(MK, "");
    if (pref === "ink" || pref === "type") return pref;
    try { return window.matchMedia?.("(pointer: coarse)").matches ? "ink" : "type"; } catch { return "type"; }
  });
  useEffect(() => { lsSet(MK, mode); }, [mode]);
  const p = value?.parts?.[cur] || null;
  const setPart = (v) => {
    const next = { ...(value?.parts || {}) };
    if (v) next[cur] = v; else delete next[cur];
    onChange(Object.keys(next).length ? { k: "sa", parts: next } : null);
  };
  const ink = p?.k === "ink" ? p : null;
  const text = p?.k === "text" ? p.raw : "";
  return (
    <div className="mx-saw">
      <div className="mx-sawh">
        {parts.length > 1 && (
          <div className="mx-parts" role="tablist" aria-label="하위 문항">
            {parts.map((n) => {
              const has = value?.parts?.[n] && ((value.parts[n].k === "ink" && hasInk(value.parts[n])) || String(value.parts[n].raw || "").trim());
              return <button key={n} type="button" role="tab" aria-selected={cur === n} className={(cur === n ? "on" : "") + (has ? " has" : "")} onClick={() => setCur(n)}>{partLabel(n)}</button>;
            })}
          </div>
        )}
        <span className="cs-fill" />
        <div className="cs-modes" role="tablist">
          <button type="button" role="tab" aria-selected={mode === "ink"} className={mode === "ink" ? "on" : ""} onClick={() => setMode("ink")}>✍ 손글씨</button>
          <button type="button" role="tab" aria-selected={mode === "type"} className={mode === "type" ? "on" : ""} onClick={() => setMode("type")}>⌨ 타자</button>
        </div>
      </div>
      {mode === "ink" ? (
        <>
          <InkPad key={`${it.i}-${cur}`} lay="free" value={ink} onChange={(v) => setPart(v)} />
          <div className="mx-sawf">
            <button type="button" className="sv-btn sm" disabled={!hasInk(ink)} onClick={() => setPart(ink && ink.s.length > 1 ? { ...ink, s: ink.s.slice(0, -1), wd: (ink.wd || []).slice(0, -1) } : null)}>↶ 되돌리기</button>
            <button type="button" className="sv-btn sm ghost" disabled={!p} onClick={() => setPart(null)}>지우기</button>
            {p?.k === "text" && <span className="sv-muted">타자로 쓴 답이 있어요 — 손글씨로 쓰면 바뀌어요</span>}
          </div>
        </>
      ) : (
        <textarea key={`${it.i}-${cur}-t`} className="sv-in mx-sat" rows={6} value={text} placeholder={`${partLabel(cur)} 풀이 과정과 답을 써요`}
          onChange={(e) => setPart(e.target.value.trim() ? { k: "text", raw: e.target.value } : null)} />
      )}
    </div>
  );
}

/** 내가 쓴 서답형 답 보기(하위 문항마다) */
export function SaMine({ it, value }) {
  const parts = it.parts?.length ? it.parts : [0];
  if (!isAnswered(it, value)) return <div className="mx-mine none">답을 쓰지 않았어요</div>;
  return (
    <div className="mx-mine">
      {parts.map((n) => {
        const p = value?.parts?.[n];
        if (!p) return null;
        return (
          <div key={n} className="mx-minep">
            {parts.length > 1 && <b>{partLabel(n)}</b>}
            {p.k === "ink" ? <span className="mx-myink" dangerouslySetInnerHTML={{ __html: inkSvg(p, { cls: "mx-inksvg" }) }} />
              : <span className="mx-mytext">{p.raw}</span>}
          </div>
        );
      })}
    </div>
  );
}

/** 서답형 스스로 채점 — 모범 답 · 채점 요소 체크 → 점수. grade: { got, checks[] } */
export function SaGrader({ it, grade, onGrade }) {
  const rb = it.rubric || [];
  const checks = grade?.checks || rb.map(() => false);
  const got = rb.length ? rubricScore(it, checks) : grade?.got ?? null;
  const toggle = (k) => {
    const c = rb.map((_, j) => !!checks[j]);
    c[k] = !c[k];
    onGrade({ checks: c, got: rubricScore(it, c) });
  };
  return (
    <div className="mx-grader">
      <div className="mx-ans"><span className="iv-lab">답</span><Rich text={it.answer} /></div>
      {rb.length > 0 ? (
        <ul className="mx-rub">
          {rb.map(([t, pts], k) => {
            const part = rubricPart(t);
            return (
              <li key={k}>
                <label className={checks[k] ? "on" : ""}>
                  <input type="checkbox" checked={!!checks[k]} onChange={() => toggle(k)} />
                  <span className="t">{part ? <em>({part})</em> : null}<Rich text={part ? t.replace(/^\(\d\)\s*/, "") : t} /></span>
                  <span className="p">{pts}점</span>
                </label>
              </li>
            );
          })}
        </ul>
      ) : (
        <div className="mx-steps" role="group" aria-label="받은 점수">
          {Array.from({ length: it.pts + 1 }, (_, n) => (
            <button key={n} type="button" className={got === n ? "on" : ""} onClick={() => onGrade({ got: n, checks: [] })}>{n}</button>
          ))}
        </div>
      )}
      <div className="mx-gtot">맞게 쓴 요소에 체크하면 점수가 매겨져요 · <b>{got ?? 0}</b>/{it.pts}점</div>
    </div>
  );
}

// ── 시청각 해설 고리 ──────────────────────────────────────────────────────────
export const avKnown = (k) => !!avItem(k);
/** 시청각 해설 하나 → { icon, title, note } (단계 key 는 짧게 「연립방정식 2단계 · 가감법 — 곱해서 맞추기」) */
export function avLabel(k) {
  const a = avItem(k);
  if (!a) return null;
  if (parseTypeKey(k)) {
    const m = typeMeta(k);
    return { icon: a.icon || "🎬", title: `${m.short} · ${m.name}`, note: `${m.n || 20}문항 · ${m.span || a.grade || ""}` };
  }
  return { icon: a.icon || "🎬", title: a.title, note: `${a.n ? `단원 ${a.n}문항` : a.kind || ""}${a.grade ? ` · ${a.grade}` : ""}` };
}
/** 문항 하나의 시청각 해설 단추들 */
export function AvButtons({ it, from, small = false }) {
  const keys = (it.av || []).filter(avKnown);
  if (!keys.length) return null;
  return (
    <div className={"mx-avb" + (small ? " sm" : "")}>
      {keys.map((k) => {
        const a = avLabel(k);
        return (
          <a key={k} className="mx-avl" href={avHref(k, from)}>
            <span className="ic" aria-hidden="true">{a.icon}</span>
            <span className="tx"><small>🎬 시청각 해설 · {a.note}</small><b>{a.title}</b></span>
            <span className="go" aria-hidden="true">›</span>
          </a>
        );
      })}
    </div>
  );
}
/** 시험 전체의 시청각 해설 목록 — max 를 주면 그만큼만 보이고 「모두 보기」 */
export function AvList({ exam, from, onItem, max = 0, more }) {
  const links = useMemo(() => avLinksOf(exam, avKnown), [exam]);
  if (!links.length) return <div className="sv-empty">이 시험에 이어 볼 시청각 해설을 아직 잇지 않았어요</div>;
  const shown = max > 0 ? links.slice(0, max) : links;
  return (
    <div className="mx-avlist">
      {shown.map(({ key, items }) => {
        const a = avLabel(key);
        return (
          <div key={key} className="mx-avrow">
            <a className="mx-avl" href={avHref(key, from)}>
              <span className="ic" aria-hidden="true">{a.icon}</span>
              <span className="tx"><b>{a.title}</b><small>{a.note}</small></span>
              <span className="go" aria-hidden="true">›</span>
            </a>
            <div className="mx-avits">
              {items.map((x) => <button key={x.i} type="button" className="mx-tag" onClick={() => onItem?.(x.i)}>{x.label.startsWith("서답형") ? x.label : `${x.label}번`}</button>)}
            </div>
          </div>
        );
      })}
      {shown.length < links.length && more && (
        <button type="button" className="sv-btn sm mx-avmore" onClick={more}>시청각 해설 {links.length}개 모두 보기 ›</button>
      )}
    </div>
  );
}
