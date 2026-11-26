// ashrain.out — 시그니처 프린트 해설 액자 둘의 세트 머리 정보 · 늦게 들여오기 (prints/index.js) — JSX 없음
// 액자 「두 점을 지나는 일차함수의 식 해설」(lin2 — 프린트 1 ~ 5세트) · 「직선의 교점 · 만날 조건 해설」(meet — 교점 활용 ·
//   만날 조건 쉬운 판 · 중~상 판 · 세 직선으로 삼각형이 만들어질 조건). 문항 자료는 세트마다 따로(lin2-1.js … meet-tri.js) —
//   고를 때 들여온다(frames/prints.jsx 의 spec.ready · load — 해설 액자 공통 틀이 「불러오는 중」을 보인다).
// 문항 파일은 생성기가 만든 것(손으로 고치지 말 것 — 프로젝트 SRC-새시그니처프린트-해설내보내기-v1.py). 한 문항 꼴은 기본기 해설과 같다:
//   { no, st 단계, sub 단계 이름, q 발문, plan 방침, lines [{ s, memo? }], ans, fig 그림 DSL(frames/figdsl.jsx — must 1 이면 꼭 보이게) }
const TIERS = ["기울기가 양수", "기울기가 음수", "음수 좌표", "순서가 바뀐 두 점", "정수 기울기 종합", "멀리 떨어진 두 점",
  "분수 기울기", "분수 기울기 · 약분", "분수 상수항", "분수 종합"];
const stageOf = (names) => Object.fromEntries(names.map((s, i) => [i + 1, s]));

export const PRINT_FRAMES = {
  lin2: {
    title: "두 점을 지나는 일차함수의 식 해설",
    keys: [1, 2, 3, 4, 5],
    sets: Object.fromEntries([1, 2, 3, 4, 5].map((k) => [k, {
      key: k, name: `${k}세트`, short: `${k}세트`, code: ["BZ8-R58", "YKT-CEU", "4QJ-4QH", "45X-K5T", "S7M-8KF"][k - 1], stage: stageOf(TIERS),
    }])),
  },
  meet: {
    title: "직선의 교점 · 만날 조건 해설",
    keys: ["ix", "mE", "mH", "tri"],
    sets: {
      ix: { key: "ix", name: "교점 활용 100제", short: "교점 활용", code: "MAC-KR8",
        stage: stageOf(["처음 값과 변화량이 바로 보이는 문장", "그래프에서 두 점 읽기", "변화량 환산 · 표", "같아질 때의 값 · 차 · 늦게 시작 · 역전", "거꾸로 구하기 · 그래프 일부 · 두 단계"]) },
      mE: { key: "mE", name: "만날 조건 · 쉬운 판", short: "쉬운 판", code: "N59-X84",
        stage: stageOf(["y = ax와 선분", "y = ax와 삼각형 · 직사각형", "기울기가 정해진 직선 y = mx + b", "y절편이 정해진 직선 y = ax + c", "만나지 않을 조건 · 종합"]) },
      mH: { key: "mH", name: "만날 조건 · 중~상 판", short: "중~상 판", code: "Z3H-9RC",
        stage: stageOf(["y = ax · 여러 사분면", "y절편 고정 · 분수 기울기", "정점을 지나는 직선", "묻는 방식 바꾸기", "꼭짓점의 미지수 · 종합"]) },
      tri: { key: "tri", name: "삼각형이 만들어질 조건", short: "삼각형 조건", code: "WF7-QYN",
        stage: stageOf(["기울기가 모두 다른 세 직선", "기울기가 미지수인 직선", "일차방정식 꼴의 세 직선", "좌표축에 평행한 직선", "묻는 방식 바꾸기 · 종합"]) },
    },
  },
};

// 세트 문항 들여오기 — 경로는 글자 그대로 적어야 번들러가 세트마다 따로 나눈다
const LOADERS = {
  "lin2:1": () => import("./lin2-1.js"), "lin2:2": () => import("./lin2-2.js"), "lin2:3": () => import("./lin2-3.js"),
  "lin2:4": () => import("./lin2-4.js"), "lin2:5": () => import("./lin2-5.js"),
  "meet:ix": () => import("./meet-ix.js"), "meet:mE": () => import("./meet-mE.js"), "meet:mH": () => import("./meet-mH.js"),
  "meet:tri": () => import("./meet-tri.js"),
};
const CACHE = new Map();
const WAIT = new Map();
/** 들여온 세트의 문항(아직이면 null) */
export const printCached = (fk, set) => CACHE.get(`${fk}:${set}`) || null;
/** 세트 문항 들여오기 → Promise<문항 목록> (한 번만) */
export function loadPrintSet(fk, set) {
  const k = `${fk}:${set}`;
  if (CACHE.has(k)) return Promise.resolve(CACHE.get(k));
  if (!LOADERS[k]) return Promise.reject(new Error(`없는 세트: ${k}`));
  if (!WAIT.has(k)) {
    WAIT.set(k, LOADERS[k]().then((m) => { CACHE.set(k, m.ITEMS); WAIT.delete(k); return m.ITEMS; })
      .catch((e) => { WAIT.delete(k); throw e; }));
  }
  return WAIT.get(k);
}
/** 액자 하나의 세트 전부 들여오기(시험 · 미리 보기) */
export const loadPrintFrame = (fk) => Promise.all(PRINT_FRAMES[fk].keys.map((s) => loadPrintSet(fk, s)));
