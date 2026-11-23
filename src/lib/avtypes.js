// ashrain.out — 단원 100제의 유형(단계) 하나를 콘텐츠 하나로 (lib/avtypes.js)
// 유형 = 단원의 한 단계(20문항). key 는 「<단원 id>.<단계>」(예: e-ten.3) — 학생앱 목록에 유형마다 한 줄(#/av/e-ten.3),
//   액자에서는 그 단원을 그 단계만 돌리고(frames/basics.jsx), 프린트(문제지 · 해설지 · 빠른 정답 · OMR)는 유형마다 따로 — 번호 1 ~ 20 · 유형 코드.
//   교과서 단원 · 코드: ../features/display/basics/typetags.js(생성기 avgen/typetags.py).
import { basicOf, basicCached, loadBasic } from "../features/display/basics/index.js";
import { TYPE_TAGS } from "../features/display/basics/typetags.js";
import { TERM_LABEL } from "./units.js";

export const typeKey = (id, st) => `${id}.${st}`;

/** 「e-ten.3」 → { id, st } (없는 단원 · 단계면 null) */
export function parseTypeKey(k) {
  const m = /^([a-z]-[a-z0-9-]+)\.([1-5])$/.exec(String(k ?? ""));
  if (!m || !basicOf(m[1]) || !TYPE_TAGS[m[1]]) return null;
  return { id: m[1], st: Number(m[2]) };
}

/** 교과서 단원의 학년(「e3-1:평면도형」 → 「초3」 · 「h2-2:미분」 → 「고2」 — 고등은 과목 이름이 아니라 학년) */
const LV = { e: "초", m: "중", h: "고" };
export const gradeOfUnit = (u) => { const t = String(u || "").split(":")[0], m = /^([emh])(\d)-\d$/.exec(t); return m && TERM_LABEL[t] ? `${LV[m[1]]}${m[2]}` : ""; };

const META = new Map(), SETS = new Map();
/** 유형 머리 정보 — 단원 머리 정보와 같은 칸(id · title · short · span · level · unit · code · stages · n)에 base · st */
export function typeMeta(k) {
  if (META.has(k)) return META.get(k);
  const p = parseTypeKey(k);
  if (!p) return null;
  const b = basicOf(p.id), [unit, code] = TYPE_TAGS[p.id][p.st];
  const m = { ...b, id: k, base: p.id, st: p.st, unit, code, n: 20, name: b.stages[p.st],
    title: `${b.title} — ${p.st}단계 ${b.stages[p.st]}`, short: `${b.short} ${p.st}단계`, span: gradeOfUnit(unit) || b.span };
  META.set(k, m);
  return m;
}

/** 유형 문항 — 단원 문항에서 그 단계 20문항을 1 ~ 20번으로(단원 문항이 들어와 있어야) */
export function typeSet(k) {
  if (SETS.has(k)) return SETS.get(k);
  const p = parseTypeKey(k), S = p && basicCached(p.id);
  if (!S) return null;
  const items = S.items.filter((it) => it.st === p.st).map((it, i) => ({ ...it, no: i + 1, src: it.no }));
  const set = { id: k, pp: S.pp, note: S.note, tips: { [p.st]: S.tips?.[p.st] }, items };
  SETS.set(k, set);
  return set;
}
export const typeCached = (k) => typeSet(k);
export const loadType = (k) => { const p = parseTypeKey(k); return p ? loadBasic(p.id).then(() => typeSet(k)) : Promise.reject(new Error(`없는 유형: ${k}`)); };

/** 단원 하나의 유형 다섯 — 목록용 머리 정보 */
export const typesOf = (id) => [1, 2, 3, 4, 5].map((st) => typeMeta(typeKey(id, st))).filter(Boolean);
