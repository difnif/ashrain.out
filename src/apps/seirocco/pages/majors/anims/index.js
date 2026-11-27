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
  phys: () => import("./phys.jsx"),
  mech: () => import("./mech.jsx"),
  circuit: () => import("./circuit.jsx"),
  signal: () => import("./signal.jsx"),
  orbit: () => import("./orbit.jsx"),
  econ: () => import("./econ.jsx"),
  trade: () => import("./trade.jsx"),
  fin: () => import("./fin.jsx"),
  game: () => import("./game.jsx"),
  ops: () => import("./ops.jsx"),
  discrete: () => import("./discrete.jsx"),
  algo: () => import("./algo.jsx"),
  ml: () => import("./ml.jsx"),
  data: () => import("./data.jsx"),
  info: () => import("./info.jsx"),
  analysis: () => import("./analysis.jsx"),
  complex: () => import("./complex.jsx"),
  numer: () => import("./numer.jsx"),
  opt: () => import("./opt.jsx"),
  chem: () => import("./chem.jsx"),
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
  // 물리
  projectile: ["phys", "Projectile"], pendulum: ["phys", "Pendulum"], collision: ["phys", "Collision"], wave: ["phys", "Wave"],
  efield: ["phys", "EField"], maxwell: ["phys", "Maxwell"], qbox: ["phys", "QBox"], lightclock: ["phys", "LightClock"],
  // 기계
  beam: ["mech", "Beam"], stressstrain: ["mech", "StressStrain"], heat: ["mech", "Heat"], pv: ["mech", "PVCycle"],
  venturi: ["mech", "Venturi"], rolling: ["mech", "Rolling"],
  // 회로 · 제어
  dcircuit: ["circuit", "DCircuit"], maxpower: ["circuit", "MaxPower"], rc: ["circuit", "RC"], phasor: ["circuit", "Phasor"],
  bode: ["circuit", "Bode"], diode: ["circuit", "Diode"], adder: ["circuit", "Adder"], pid: ["circuit", "PID"],
  poles: ["circuit", "Poles"], rootlocus: ["circuit", "RootLocus"],
  // 신호
  fourier: ["signal", "Fourier"], alias: ["signal", "Alias"], convolve: ["signal", "Convolve"], modulation: ["signal", "Modulation"],
  dft: ["signal", "DFT"], dct: ["signal", "DCT"],
  // 천문우주
  kepler: ["orbit", "Kepler"], cannon: ["orbit", "Cannon"], hohmann: ["orbit", "Hohmann"], rocket: ["orbit", "Rocket"],
  parallax: ["orbit", "Parallax"], blackbody: ["orbit", "Blackbody"], transit: ["orbit", "Transit"], hubble: ["orbit", "Hubble"],
  // 경제
  market: ["econ", "Market"], tax: ["econ", "Tax"], elastic: ["econ", "Elastic"], utility: ["econ", "Utility"], costs: ["econ", "Costs"],
  monopoly: ["econ", "Monopoly"], cobweb: ["econ", "Cobweb"], solow: ["econ", "Solow"], keynes: ["econ", "Keynes"], lorenz: ["econ", "Lorenz"],
  // 무역
  comparative: ["trade", "Comparative"], ppf: ["trade", "PPF"], tariff: ["trade", "Tariff"], parity: ["trade", "Parity"], incoterms: ["trade", "Incoterms"],
  // 금융
  compound: ["fin", "Compound"], npv: ["fin", "NPV"], amort: ["fin", "Amort"], bond: ["fin", "Bond"], frontier: ["fin", "Frontier"],
  gbm: ["fin", "GBM"], option: ["fin", "Option"], bintree: ["fin", "BinTree"],
  // 게임이론
  nash2: ["game", "Nash2"], mixed: ["game", "Mixed"], backward: ["game", "Backward"], repeated: ["game", "Repeated"],
  hawkdove: ["game", "HawkDove"], cournot: ["game", "Cournot"], auction: ["game", "Auction"],
  // 경영과학
  lp: ["ops", "LP"], dijkstra: ["ops", "Dijkstra"], cpm: ["ops", "CPM"], eoq: ["ops", "EOQ"], newsvendor: ["ops", "Newsvendor"], queue: ["ops", "Queue"],
  // 이산수학
  truth: ["discrete", "Truth"], venn: ["discrete", "Venn"], tromino: ["discrete", "Tromino"], pascal: ["discrete", "Pascal"],
  hanoi: ["discrete", "Hanoi"], eulerpath: ["discrete", "EulerPath"], euclid: ["discrete", "Euclid"], dfa: ["discrete", "DFA"],
  // 알고리즘
  bigo: ["algo", "BigO"], sorting: ["algo", "Sorting"], rectree: ["algo", "RecTree"], heap: ["algo", "Heap"],
  bfsdfs: ["algo", "BfsDfs"], mst: ["algo", "MST"], dptable: ["algo", "DPTable"], tsp: ["algo", "TSP"],
  // 머신러닝
  optim: ["ml", "Optim"], logreg: ["ml", "LogReg"], overfit: ["ml", "Overfit"], roc: ["ml", "ROC"], tree2d: ["ml", "Tree2D"],
  kernel: ["ml", "Kernel"], kmeans: ["ml", "KMeans"], pca: ["ml", "PCA"], nnet: ["ml", "NNet"],
  // 데이터 공학
  knn: ["data", "KNN"], abtest: ["data", "ABTest"], hashtable: ["data", "HashTable"], bloom: ["data", "Bloom"],
  btree: ["data", "BTree"], join: ["data", "Join"], reservoir: ["data", "Reservoir"], pagerank: ["data", "PageRank"],
  // 정보이론 · 암호
  entropy: ["info", "Entropy"], huffman: ["info", "Huffman"], lz: ["info", "LZ"], mutual: ["info", "Mutual"],
  bsc: ["info", "BSC"], hamming: ["info", "Hamming"], caesar: ["info", "Caesar"], modring: ["info", "ModRing"],
  // 해석학
  supinf: ["analysis", "SupInf"], epsn: ["analysis", "EpsN"], rearrange: ["analysis", "Rearrange"], unifcont: ["analysis", "UnifCont"],
  zoomdiff: ["analysis", "ZoomDiff"], darboux: ["analysis", "Darboux"], unifconv: ["analysis", "UnifConv"], contract: ["analysis", "Contract"], cantor: ["analysis", "Cantor"],
  // 복소해석
  cmul: ["complex", "CMul"], roots: ["complex", "Roots"], cmap: ["complex", "CMap"], cr: ["complex", "CR"], branch: ["complex", "Branch"],
  winding: ["complex", "Winding"], cauchyint: ["complex", "CauchyInt"], pseries: ["complex", "PSeries"], residue: ["complex", "Residue"],
  // 수치해석
  float: ["numer", "Float"], convrate: ["numer", "ConvRate"], interp: ["numer", "Interp"], quad: ["numer", "Quad"],
  condnum: ["numer", "CondNum"], jacobi: ["numer", "Jacobi"], powerit: ["numer", "PowerIt"], odestab: ["numer", "OdeStab"],
  // 최적화
  critpt: ["opt", "CritPt"], convex: ["opt", "Convex"], linesearch: ["opt", "LineSearch"], newtonopt: ["opt", "NewtonOpt"],
  kkt: ["opt", "KKT"], barrier: ["opt", "Barrier"], bnb: ["opt", "BnB"], anneal: ["opt", "Anneal"],
  // 화학
  limiting: ["chem", "Limiting"], vdw: ["chem", "VdW"], gibbs: ["chem", "Gibbs"], equil: ["chem", "Equil"],
  titration: ["chem", "Titration"], arrhenius: ["chem", "Arrhenius"], nernst: ["chem", "Nernst"], hlines: ["chem", "HLines"],
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
