// 전공 수학 「움직이는 그림」 목록 — 책 글(majorgen ANIM("종류", …))의 종류 이름 → [묶음 파일, 내보낸 이름]
// 묶음 파일은 그림이 처음 보일 때 받는다(서가 · 차례에는 싣지 않는다). kinds.json 은 생성기(majorgen/build.py)가 종류 이름을 맞춰 보는 목록 —
// 이 표와 같아야 한다(tests/majors.test.mjs 가 맞춘다).
export const MODS = {
  calc: () => import("./calc.jsx"),
  mvc: () => import("./mvc.jsx"),
  linalg: () => import("./linalg.jsx"),
  ode: () => import("./ode.jsx"),
  prob: () => import("./prob.jsx"),
  stat: () => import("./stat.jsx"),
};

export const KINDS = {
  // 미적분
  limit: ["calc", "Limit"], tangent: ["calc", "Tangent"], riemann: ["calc", "Riemann"], taylor: ["calc", "Taylor"],
  series: ["calc", "Series"], newton: ["calc", "Newton"], mvt: ["calc", "MeanValue"], accum: ["calc", "Accumulate"],
  boxopt: ["calc", "BoxOpt"], bisect: ["calc", "Bisection"],
  // 다변수 · 벡터
  contour: ["mvc", "Contour"], gradient: ["mvc", "Gradient"], lagrange: ["mvc", "Lagrange"], dblint: ["mvc", "DoubleInt"],
  field: ["mvc", "Field"], dotproj: ["mvc", "DotProj"], polar: ["mvc", "PolarArea"],
  // 선형대수
  span: ["linalg", "Span"], linmap: ["linalg", "LinMap"], det: ["linalg", "DetArea"], eigen: ["linalg", "Eigen"],
  lines2: ["linalg", "Lines2"], rowreduce: ["linalg", "RowReduce"], svd: ["linalg", "SVD"],
  // 미분방정식
  slopefield: ["ode", "SlopeField"], growth: ["ode", "Growth"], logistic: ["ode", "Logistic"], oscillator: ["ode", "Oscillator"],
  resonance: ["ode", "Resonance"], phaseplane: ["ode", "PhasePlane"], euler: ["ode", "Euler"], predprey: ["ode", "PredPrey"],
  sir: ["ode", "SIR"], dosing: ["ode", "Dosing"],
  // 확률
  lln: ["prob", "LLN"], bayes: ["prob", "Bayes"], binomial: ["prob", "Binomial"], normal: ["prob", "Normal"], clt: ["prob", "CLT"],
  scatter: ["prob", "Scatter"], markov: ["prob", "Markov"], randomwalk: ["prob", "RandomWalk"], poisson: ["prob", "Poisson"],
  monty: ["prob", "Monty"],
  // 통계
  summary: ["stat", "Summary"], sampling: ["stat", "Sampling"], confint: ["stat", "ConfInt"], hyptest: ["stat", "HypTest"],
  regression: ["stat", "Regression"], anova: ["stat", "Anova"], beta: ["stat", "BetaUpdate"], bootstrap: ["stat", "Bootstrap"],
};

const loaded = {};
/** 종류 이름 → 그림 컴포넌트(Promise) */
export function loadKind(kind) {
  const e = KINDS[kind];
  if (!e) return Promise.reject(new Error("없는 그림 종류 " + kind));
  const [mod, name] = e;
  if (!loaded[mod]) loaded[mod] = MODS[mod]();
  return loaded[mod].then((m) => m[name]);
}
