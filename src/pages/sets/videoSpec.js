// ashrain.out — 컨셉 문제 「해설 영상」을 해설 액자 공통 틀(features/display/frames/lesson.jsx)에 얹는 spec (JSX 없음 · node 로 시험)
// 시청각 해설(교실 모니터 해설 액자)과 조작이 같다:
//   「보기 단일 | 듀얼」(D) · 「세트」(U — 컨셉 문제 세트 전부: 경우의 수와 확률 · 일차함수와 그래프, 범주 · 묶음마다) ·
//   「빠르기 0.75× · 1× · 1.5× · 2×」(S) · 번호 · 단계 목록(L — 하 · 중 · 상 칩을 고르면 그 수준만) · 두 막대(문항 이동 · 풀이 이동).
//   듀얼 모드는 판마다 세트(같은 세트 둘도 됨) · 단계 · 번호 · 빠르기 · 멈춤 · 반복 · 두 막대, 가운데 ⇄ 로 자리 바꾸기.
// 세트 key = 「범주:NN」(prob:07 · lin:03). 장면은 ./videoScenes.jsx(빠르기 · 단계마다 한 목록), 세트 문항은 고를 때 들여온다(get · load).
// 기억(기기): ash.cs.video — 단일 모드 { set, sp, st } · .mode 단일/듀얼 · .dual 두 판 · 자리(벽시계)는 세트마다
//   ash.cs.video.<범주>.<NN>(전체 — 예전 해설 영상 자리 그대로 이어진다) · ash.cs.video.<범주>.<NN>.<단계>.
import { videoScenes, VIDEO_STAGES } from "./videoScenes.jsx";

export const VIDEO_LSK = "ash.cs.video";
const pad2 = (n) => String(n).padStart(2, "0");
/** 세트 key — 「prob:07」 */
export const videoKey = (cat, no) => `${cat}:${pad2(no)}`;
/** 「prob:07」 → { cat: "prob", no: 7 } | null */
export function parseVideoKey(k) {
  const m = /^([a-z][a-z0-9]*):(\d+)$/.exec(String(k ?? ""));
  return m ? { cat: m[1], no: Number(m[2]) } : null;
}

/** 범주 index 들 → 세트 이름표 목록(범주 차례 · 묶음 차례 · 묶음 안 차례, 묶음에 없는 세트는 「그 밖의 세트」) */
export function videoSets(cats) {
  const out = [];
  for (const c of cats || []) {
    if (!c || !Array.isArray(c.sets)) continue;
    const byNo = new Map(c.sets.map((s) => [s.no, s]));
    const seen = new Set();
    const groups = [...(c.groups || []), { title: "그 밖의 세트", sets: c.sets.map((s) => s.no) }];
    for (const g of groups) for (const no of g.sets || []) {
      const s = byNo.get(no);
      if (!s || seen.has(no)) continue;
      seen.add(no);
      out.push({
        key: videoKey(c.id, no), cat: c.id, no, name: s.title || s.short, short: `${pad2(no)} ${s.short}`, icon: s.icon || c.icon,
        sub: s.title || s.short, grp: `${c.icon ? `${c.icon} ` : ""}${c.title} · ${g.title}`, lv: s.lv || null, n: s.n || 0,
      });
    }
  }
  return out;
}

/**
 * 해설 액자 spec — cats: 범주 index 들(lib/conceptsets loadIndex), src: { get(key) → 세트 JSON | undefined, load(key) → Promise }.
 * 세트 목록이 많아 「세트」는 칸 대신 목록 단추(U)로 고른다. 듀얼 판도 컨셉 문제 세트에서만(ownDual).
 */
export function videoSpec(cats, src) {
  const sets = videoSets(cats);
  const byKey = new Map(sets.map((s) => [s.key, s]));
  const stageCache = new Map();
  const stages = (k) => {
    if (stageCache.has(k)) return stageCache.get(k);
    const lv = byKey.get(k)?.lv;
    const L = VIDEO_STAGES.filter((x) => !lv || (lv[x.lv] ?? 0) > 0).map((x) => {
      const n = lv?.[x.lv];
      return { v: x.v, lab: x.lab, chip: n ? `${x.lab} ${n}` : x.lab, short: n ? `${x.lv} ${n}` : x.lv };
    });
    stageCache.set(k, L);
    return L;
  };
  const counts = (cats || []).filter((c) => c?.sets?.length).map((c) => `${c.title} ${c.sets.length}세트`).join(" · ");
  return {
    lsk: VIDEO_LSK, title: "컨셉 문제 해설 영상", ownDual: true, cols: 3,
    defSet: sets[0]?.key ?? null,
    sets,
    setMenu: { word: "세트", title: "컨셉 문제 세트", hint: `고르면 그 세트를 보던 자리에서 이어 봐요 · ${counts}` },
    stages,
    scenes: (k, sp, st) => videoScenes(src.get(k), sp, st),
    /** 자리 기억 — 전체(단계 0)는 예전 해설 영상과 같은 이름이라 그대로 이어진다 */
    posKey: (lsk, k, st) => { const p = parseVideoKey(k); return p ? `${lsk}.${p.cat}.${pad2(p.no)}${st ? `.${st}` : ""}` : `${lsk}.${k}.${st}`; },
    ready: (k) => !!src.get(k),
    load: (k) => src.load(k),
    /** 듀얼 판 머리 — 세트 · 번호 · 수준 */
    paneHead: (S, s) => `${S.short} · ${s.no}번 · ${s.lv}`,
  };
}
