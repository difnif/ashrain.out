// ashrain.out — 수학 호기심: 네트를 사이에 둔 구기 공용 계산 (curio/net.js)
// 배드민턴(실제 경기) · 테니스 · 탁구 · 배구 · 족구 · 세팍타크로(가상 경기) — 위에서 내려다본 코트, 네트 = y축.
//   한 번 친 공 = 두 점(친 곳 A · 떨어진 곳 B)을 지나는 직선. 네트(x = 0)를 지난 자리가 곧 y절편 (0, b).
//   중등: 네트 가운데가 원점 — 기울기 → 대입 → 식 → 네트를 지난 자리.
//   초등: 보이는 판의 왼쪽 아래가 원점 — 가로 · 세로 칸 수, 네트까지 가로 몇 칸이면 세로는 몇 칸(비례).
// 가상 경기는 씨앗으로 정해진다(같은 씨앗 → 같은 경기). 점수 규칙은 종목마다 실제 규칙대로.
// 화면에 나오는 수는 모두 여기서 계산한다. tests/display-curio2.test.mjs 가 따로 다시 계산해 맞춘다.
import { rng, rint, hashSeed, namesOf, lineOf, lineSteps, eqText, fs, num, pt, frac, MINUS } from "./kit.js";

/* ══════════ 종목 ══════════ */
/**
 * L: 끝선까지(칸) · W: 단식(또는 경기) 옆줄까지 · Wd: 바깥 옆줄(복식) · view: 그리는 판 반 크기 [x, y](정수 — 초등 원점)
 * unitM: 1칸이 몇 m · team: 한 편 사람 수
 */
export const NETS = {
  badminton: { key: "badminton", name: "배드민턴", unitM: 0.5, unit: "1칸 = 50 cm", L: 13.4, W: 5.18, Wd: 6.1, view: [16, 9], miniView: [16, 7.5], team: 1, ball: "셔틀콕" },
  tennis: { key: "tennis", name: "테니스", unitM: 1, unit: "1칸 = 1 m", L: 11.885, W: 4.115, Wd: 5.485, view: [15, 8], miniView: [15, 7], team: 1, ball: "공" },
  tabletennis: { key: "tabletennis", name: "탁구", unitM: 0.1, unit: "1칸 = 10 cm", L: 13.7, W: 7.625, Wd: 7.625, view: [26, 13], miniView: [26, 11], team: 1, ball: "공" },
  volleyball: { key: "volleyball", name: "배구", unitM: 1, unit: "1칸 = 1 m", L: 9, W: 4.5, Wd: 4.5, view: [13, 7], miniView: [13, 6], team: 6, ball: "공" },
  jokgu: { key: "jokgu", name: "족구", unitM: 0.5, unit: "1칸 = 50 cm", L: 15, W: 6.5, Wd: 6.5, view: [19, 9], miniView: [19, 8], team: 4, ball: "공" },
  sepak: { key: "sepak", name: "세팍타크로", unitM: 0.5, unit: "1칸 = 50 cm", L: 13.4, W: 6.1, Wd: 6.1, view: [16, 8], miniView: [16, 7.5], team: 3, ball: "공" },
};

/* ══════════ 수 ══════════ */
const cl = (v, a, b) => (v < a ? a : v > b ? b : v);
const ri = Math.round;
const sg = (v) => (v < 0 ? -1 : 1);
/** 정규분포 비슷한 난수(−1 ~ 1 에 몰림) */
const gs = (R) => (R() + R() + R() - 1.5) / 1.5;
const pick = (R, arr) => arr[rint(R, arr.length)];
/** 무게 고르기: [[값, 무게], …] */
function wpick(R, list) {
  let s = 0; for (const [, w] of list) s += w;
  let r = R() * s;
  for (const [v, w] of list) { if ((r -= w) <= 0) return v; }
  return list[list.length - 1][0];
}
/** 직선 A→B 가 x = 0 을 지나는 y(실수) — 지나지 않으면 null */
export function netY(a, b) {
  if ((a[0] < 0) === (b[0] < 0) && a[0] !== 0 && b[0] !== 0) return null;
  if (a[0] === b[0]) return a[0] === 0 ? a[1] : null;
  return a[1] + ((b[1] - a[1]) * (0 - a[0])) / (b[0] - a[0]);
}
/** 네트를 넘은 공인가(친 곳과 떨어진 곳이 네트 양쪽, 또는 네트 위) */
export const crosses = (s) => s.b[0] === 0 || (s.a[0] < 0) !== (s.b[0] < 0);

/* ══════════ 점수 ══════════ */
/** 랠리 점수 세트가 끝났나(to 점 · 2점 차 · cap 이 있으면 cap 점에서 끝) */
export function setDone(a, b, to, cap) {
  const m = Math.max(a, b);
  if (cap && m >= cap) return true;
  return m >= to && Math.abs(a - b) >= 2;
}
/** 종목별 세트 목표 [to, cap] · 이길 세트 수 */
const RULES = {
  badminton: { win: 2, set: () => [21, 30] },
  tabletennis: { win: 3, set: () => [11, 0] },
  volleyball: { win: 3, set: (i) => (i < 4 ? [25, 0] : [15, 0]) },
  jokgu: { win: 2, set: () => [15, 19] },
  sepak: { win: 2, set: (i) => (i < 2 ? [21, 25] : [15, 17]) },
};
export const ruleText = {
  badminton: "21점 · 2점 차 · 3세트 2선승",
  tennis: "6게임 세트 · 3세트 2선승",
  tabletennis: "11점 · 2점 차 · 5게임 3선승",
  volleyball: "25점 · 2점 차 · 5세트 3선승",
  jokgu: "15점 · 2점 차(상한 19점) · 3세트 2선승",
  sepak: "21점 · 2점 차(상한 25점) · 3세트 2선승",
};
const TPT = ["0", "15", "30", "40"];
/** 테니스 게임 점수 글자 [p0, p1] (타이브레이크면 그냥 수) */
export function tennisPts(p, tb) {
  if (tb) return [String(p[0]), String(p[1])];
  if (p[0] >= 3 && p[1] >= 3) {
    if (p[0] === p[1]) return ["듀스", "듀스"];
    return p[0] > p[1] ? ["AD", ""] : ["", "AD"];
  }
  return [TPT[Math.min(3, p[0])], TPT[Math.min(3, p[1])]];
}

/* ══════════ 시간(1× 기준 ms) ══════════ */
export const NT = { intro: 1300, end: 1500, replay: 8400, out: 700 };
/** 다시 보기 안의 박자 */
export const RP = { pts: [0, 900], tri: [1000, 2000], line: [2000, 3000], net: [4300, 5100], step0: 700, stepGap: 750 };

/* ══════════ 랠리 만들기(가상 경기) ══════════ */
// 샷 = { t: 편(0 왼쪽 · 1 오른쪽), w: 그 편의 몇 번째 사람, ty: 이름, a: 친 곳[정수], b: 떨어진 곳[정수], r?: "in" | "out" | "net" (마지막 샷), d: 1× 길이(ms), h: 띄우는 높이(0~1) }
const shot = (t, w, ty, a, b, d, h = 0.4, r) => ({ t, w, ty, a: [ri(a[0]), ri(a[1])], b: [ri(b[0]), ri(b[1])], d, h, ...(r ? { r } : {}) });
/** 네트에 걸린 샷: 떨어진 곳 = 네트 위 (0, y) */
function netShot(t, w, ty, a, aim, d) {
  const y = netY([ri(a[0]), ri(a[1])], aim);
  return shot(t, w, ty, a, [0, y == null ? aim[1] : y], d, 0.2, "net");
}

/* ── 테니스(1칸 = 1 m, 단식) ── */
function tennisPoint(R, srv, deuce) {
  const f = srv === 0 ? 1 : -1;                         // 서버가 보는 쪽
  const shots = [];
  const ys = (deuce ? -1 : 1) * f;                      // 오른쪽(듀스 코트)에 서면 −f 쪽
  const A = [-f * 12, ys];
  const tsg = -sg(ys);                                  // 대각선 서비스 박스
  let ok = false;
  for (const k of [1, 2]) {
    const ty = k === 1 ? "첫 서브" : "두 번째 서브";
    const T = [f * (2 + rint(R, 5)), tsg * (1 + rint(R, 4))];
    if (R() < (k === 1 ? 0.62 : 0.9)) { shots.push(shot(srv, 0, ty, A, T, 1300, 0.35)); ok = true; break; }
    const err = R() < 0.4 ? netShot(srv, 0, ty, A, T, 1100)
      : R() < 0.6 ? shot(srv, 0, ty, A, [f * (7 + rint(R, 2)), T[1]], 1300, 0.35, "out")
        : shot(srv, 0, ty, A, [T[0], tsg * 5], 1300, 0.35, "out");
    shots.push(err);
    if (k === 2) return { shots, win: 1 - srv, end: "더블 폴트" };
  }
  const last = shots[shots.length - 1];
  if (R() < 0.07) { last.r = "in"; return { shots, win: srv, end: "에이스" }; }
  // 랠리
  let hitter = 1 - srv, prev = last, atNet = false;
  for (let n = 1; n < 22; n++) {
    const fh = hitter === 0 ? 1 : -1;
    const u = [prev.b[0] - prev.a[0], prev.b[1] - prev.a[1]], L = Math.hypot(u[0], u[1]) || 1;
    const short = Math.abs(prev.b[0]) <= 4;
    const go = short ? 1 : 3 + R() * 3;
    let H = [prev.b[0] + (u[0] / L) * go, prev.b[1] + (u[1] / L) * go];
    H = [-fh * cl(Math.abs(H[0]), short ? 1 : 9, 15), cl(H[1], -7, 7)];
    atNet = Math.abs(H[0]) <= 4;
    const kind = atNet ? "발리" : prev.ty === "로브" ? "스매시"
      : wpick(R, [["포핸드", 0.5], ["백핸드", 0.38], ["드롭샷", n > 2 ? 0.07 : 0], ["로브", n > 3 ? 0.05 : 0]]);
    const depth = kind === "드롭샷" ? 1 + rint(R, 3) : kind === "로브" ? 9 + rint(R, 3) : atNet ? 3 + rint(R, 8) : wpick(R, [[9 + rint(R, 3), 0.7], [5 + rint(R, 4), 0.3]]);
    const T = [fh * depth, cl(ri(gs(R) * 4), -4, 4)];
    const ty = n === 1 ? "리턴" : kind;
    const d = kind === "로브" ? 2000 : kind === "스매시" ? 1000 : kind === "드롭샷" ? 1700 : atNet ? 1100 : 1500;
    const h = kind === "로브" ? 0.95 : kind === "드롭샷" ? 0.5 : kind === "스매시" ? 0.15 : 0.35;
    const pErr = (n === 1 ? 0.13 : 0.1) + (kind === "드롭샷" ? 0.08 : 0) + (n > 12 ? 0.08 : 0);
    if (R() < pErr) {
      const s = R() < 0.42 ? netShot(hitter, 0, ty, H, T, d * 0.8)
        : R() < 0.55 ? shot(hitter, 0, ty, H, [fh * (12 + rint(R, 2)), T[1]], d, h, "out")
          : shot(hitter, 0, ty, H, [T[0] || fh * 6, sg(T[1] || 1) * (5 + rint(R, 2))], d, h, "out");
      shots.push(s);
      return { shots, win: 1 - hitter, end: s.r === "net" ? "네트에 걸림" : "밖으로 나감" };
    }
    const s = shot(hitter, 0, ty, H, T, d, h);
    shots.push(s);
    if (R() < (kind === "스매시" ? 0.55 : n === 1 ? 0.04 : 0.08)) { s.r = "in"; return { shots, win: hitter, end: kind === "스매시" ? "스매시 득점" : "위너" }; }
    prev = s; hitter = 1 - hitter;
  }
  const s = shots[shots.length - 1]; s.r = "in";
  return { shots, win: s.t, end: "위너" };
}

/* ── 탁구(1칸 = 10 cm, 단식) ── */
function ttPoint(R, srv) {
  const f = srv === 0 ? 1 : -1;
  const shots = [];
  const A = [-f * (16 + rint(R, 3)), rint(R, 9) - 4];
  const T = [f * (4 + rint(R, 9)), rint(R, 13) - 6];
  const sv = R();
  if (sv < 0.05) { shots.push(netShot(srv, 0, "서브", A, T, 900)); return { shots, win: 1 - srv, end: "서브 네트" }; }
  if (sv < 0.08) { shots.push(shot(srv, 0, "서브", A, [f * 14, T[1]], 1000, 0.25, "out")); return { shots, win: 1 - srv, end: "서브 실수" }; }
  shots.push(shot(srv, 0, "서브", A, T, 1100, 0.25));
  if (R() < 0.04) { shots[0].r = "in"; return { shots, win: srv, end: "서브 에이스" }; }
  let hitter = 1 - srv, prev = shots[0];
  for (let n = 1; n < 30; n++) {
    const fh = hitter === 0 ? 1 : -1;
    const u = [prev.b[0] - prev.a[0], prev.b[1] - prev.a[1]], L = Math.hypot(u[0], u[1]) || 1;
    const short = Math.abs(prev.b[0]) <= 6;
    const go = short ? 4 : 5 + R() * 7;
    let H = [prev.b[0] + (u[0] / L) * go, prev.b[1] + (u[1] / L) * go];
    H = [-fh * cl(Math.abs(H[0]), short ? 9 : 15, 26), cl(H[1], -11, 11)];
    const kind = n === 1 ? (short ? "플릭" : "리시브")
      : short ? "커트" : wpick(R, [["드라이브", 0.48], ["백핸드 드라이브", 0.28], ["블록", 0.14], ["스매싱", prev.h > 0.6 ? 0.6 : 0.04], ["로빙", n > 4 ? 0.05 : 0]]);
    const T2 = [fh * (kind === "커트" || kind === "블록" ? 5 + rint(R, 8) : 8 + rint(R, 6)), cl(ri(gs(R) * 7), -7, 7)];
    const d = kind === "로빙" ? 1700 : kind === "스매싱" ? 700 : 950;
    const h = kind === "로빙" ? 0.9 : kind === "커트" ? 0.25 : 0.3;
    if (R() < 0.12 + (n > 10 ? 0.06 : 0)) {
      const s = R() < 0.45 ? netShot(hitter, 0, kind, H, T2, d * 0.8)
        : R() < 0.6 ? shot(hitter, 0, kind, H, [fh * (14 + rint(R, 2)), T2[1]], d, h, "out")
          : shot(hitter, 0, kind, H, [T2[0], sg(T2[1] || 1) * (8 + rint(R, 2))], d, h, "out");
      shots.push(s);
      return { shots, win: 1 - hitter, end: s.r === "net" ? "네트에 걸림" : "탁구대 밖으로" };
    }
    const s = shot(hitter, 0, kind, H, T2, d, h);
    shots.push(s);
    if (R() < (kind === "스매싱" ? 0.6 : 0.07)) { s.r = "in"; return { shots, win: hitter, end: kind === "스매싱" ? "스매싱 득점" : "득점" }; }
    prev = s; hitter = 1 - hitter;
  }
  const s = shots[shots.length - 1]; s.r = "in";
  return { shots, win: s.t, end: "득점" };
}

/* ── 배구 · 족구 · 세팍타크로(편마다 여러 명, 세 번 안에 넘긴다) ── */
// 왼쪽 편(+x 를 본다) 기준 자리. 오른쪽 편은 (−x, −y).
const TEAM = {
  volleyball: {
    // 자리 1(오른쪽 뒤) ~ 6(가운데 뒤) — 서브는 1번 자리, 이긴 편이 서브권을 되찾으면 시계 방향으로 돈다
    home: [[-7, -3], [-2, -3], [-2, 0], [-2, 3], [-7, 3], [-7, 0]],
    srvAt: () => [-10, -2], srvT: (R) => [2 + rint(R, 7), rint(R, 9) - 4],
    // 공격: 왼쪽 앞(4번 자리) · 가운데 속공(3번) · 뒤에서 뛰어드는 후위 공격(1번 · 6번) — 토스는 오른쪽 앞(2번 자리)이 올린다
    setterSpot: [-1, -1], atk: [[-2, 3], [-1, 0], [-4, -2], [-4, 1]], atkSlot: [3, 2, 0, 5],
    names: { srv: "서브", rec: "리시브", set: "토스", atk: ["스파이크", "속공", "후위 공격", "후위 공격"], dig: "디그", blk: "블로킹", free: "넘기기" },
    p: { srvErr: 0.1, ace: 0.06, kill: 0.45, block: 0.12, dug: 0.33, atkErr: 0.1 },
    deep: [3, 8], wide: 4, d: { srv: 1500, rec: 1100, set: 1000, atk: 850, blk: 700, dig: 1100 },
  },
  jokgu: {
    // 0 공격수 · 1 세터 · 2 좌수비 · 3 우수비 — 서브는 우수비 → 좌수비 → 공격수 → 세터 순서
    home: [[-5, 0], [-9, 1], [-12, 3], [-12, -3]], order: [3, 2, 0, 1],
    srvAt: (R) => [-17, rint(R, 7) - 3], srvT: (R) => [6 + rint(R, 8), rint(R, 11) - 5],
    setterSpot: [-4, 1], atk: [[-3, 0], [-3, 2], [-3, -2]],
    names: { srv: "서브", rec: "받기", set: "띄우기", atk: ["차기", "차기", "넘어 차기"], dig: "받아 올리기", blk: "", free: "넘기기" },
    p: { srvErr: 0.08, ace: 0.07, kill: 0.42, block: 0, dug: 0.43, atkErr: 0.12 },
    deep: [5, 14], wide: 6, d: { srv: 1600, rec: 1200, set: 1100, atk: 900, blk: 700, dig: 1200 },
  },
  sepak: {
    // 0 테콩(서버) · 1 피더 · 2 공격수 — 서브는 늘 테콩이 서비스 원에서
    home: [[-9, 0], [-3, 4], [-3, -4]],
    srvAt: () => [-8.5, 0], srvT: (R) => [4 + rint(R, 9), rint(R, 11) - 5],
    setterSpot: [-3, 2], atk: [[-2, -2], [-2, 1], [-2, 3]],
    names: { srv: "서브", rec: "받기", set: "토스", atk: ["롤링 스파이크", "시저스 킥", "헤딩 공격"], dig: "받아 올리기", blk: "블로킹", free: "넘기기" },
    p: { srvErr: 0.12, ace: 0.08, kill: 0.5, block: 0.12, dug: 0.28, atkErr: 0.1 },
    deep: [2, 12], wide: 5, d: { srv: 1400, rec: 1100, set: 1000, atk: 750, blk: 650, dig: 1100 },
  },
};
const mir = (q, t) => (t === 0 ? q : [-q[0], -q[1]]);

/** 팀 경기 한 랠리. rot[t] = 그 편의 자리 → 사람 번호(배구 로테이션) · srvWho = 서버(사람 번호) */
function teamPoint(R, sport, srv, rot, srvWho) {
  const T = TEAM[sport], S = NETS[sport];
  const shots = [];
  const posOf = (t, slot) => mir(T.home[slot], t);
  const whoAt = (t, slot) => rot[t][slot];
  const nearest = (t, q, not) => {
    let best = 0, bd = 1e9;
    for (let s = 0; s < T.home.length; s++) {
      const w = whoAt(t, s);
      if (not != null && w === not) continue;
      const d = Math.hypot(posOf(t, s)[0] - q[0], posOf(t, s)[1] - q[1]);
      if (d < bd) { bd = d; best = w; }
    }
    return best;
  };
  const fA = srv === 0 ? 1 : -1;
  // 서브
  const A = mir(T.srvAt(R), srv);
  const ST = mir(T.srvT(R), 1 - srv).map((v, i) => (i === 0 ? fA * Math.abs(v) : v));
  if (R() < T.p.srvErr) {
    const s = R() < 0.45 ? netShot(srv, srvWho, T.names.srv, A, ST, T.d.srv * 0.8)
      : shot(srv, srvWho, T.names.srv, A, [fA * (S.L + 1 + rint(R, 2)), ST[1]], T.d.srv, 0.5, "out");
    shots.push(s);
    return { shots, win: 1 - srv, end: s.r === "net" ? "서브 네트" : "서브 아웃" };
  }
  shots.push(shot(srv, srvWho, T.names.srv, A, ST, T.d.srv, 0.55));
  if (R() < T.p.ace) { shots[0].r = "in"; return { shots, win: srv, end: "서브 에이스" }; }
  // 받는 편이 세 번 안에 넘긴다(받기 → 토스 → 공격), 막히거나 받아 내면 다시
  let team = 1 - srv, at = shots[0].b, first = T.names.rec;
  for (let ex = 0; ex < 8; ex++) {
    const fh = team === 0 ? 1 : -1;
    const setter = whoAt(team, sport === "volleyball" ? 1 : 1);
    const recv = nearest(team, at, ex === 0 ? setter : null);
    const SS = mir(T.setterSpot, team);
    shots.push(shot(team, recv, first, at, SS, T.d.rec, 0.6));
    const ai = rint(R, T.atk.length), AS = mir(T.atk[ai], team);
    const atkWho = sport === "volleyball" ? whoAt(team, T.atkSlot[ai]) : sport === "jokgu" ? 0 : 2;
    const setWho = setter === recv ? nearest(team, SS, recv) : setter;
    shots.push(shot(team, setWho, T.names.set, SS, AS, T.d.set, 0.7));
    const kind = T.names.atk[ai];
    const tgt = [fh * (T.deep[0] + rint(R, T.deep[1] - T.deep[0] + 1)), rint(R, 2 * T.wide + 1) - T.wide];
    const u = R();
    if (u < T.p.atkErr) {
      const s = R() < 0.4 ? netShot(team, atkWho, kind, AS, tgt, T.d.atk * 0.8)
        : R() < 0.5 ? shot(team, atkWho, kind, AS, [fh * (S.L + 1 + rint(R, 2)), tgt[1]], T.d.atk, 0.2, "out")
          : shot(team, atkWho, kind, AS, [tgt[0], sg(tgt[1] || 1) * Math.min(S.view[1] - 1, Math.ceil(S.W) + 1 + rint(R, 2))], T.d.atk, 0.2, "out");
      shots.push(s);
      return { shots, win: 1 - team, end: s.r === "net" ? "공격이 네트에 걸림" : "공격 아웃" };
    }
    if (u < T.p.atkErr + T.p.block) {
      // 블로킹: 네트 앞에서 막아 공격한 편 코트로
      // 블로킹: 네트 위에서 막혀 공격한 편 코트로 — 70%는 그대로 떨어져 점수, 나머지는 받아 내서(커버) 다시 공격
      const bw = nearest(1 - team, [0, AS[1]]);
      const BA = [fh * 1, AS[1]], BT = [-fh * (1 + rint(R, 4)), cl(AS[1] + rint(R, 5) - 2, -T.wide, T.wide)];
      shots.push(shot(team, atkWho, kind, AS, BA, T.d.atk * 0.6, 0.15));
      if (R() < 0.7) {
        shots.push(shot(1 - team, bw, T.names.blk, BA, BT, T.d.blk, 0.25, "in"));
        return { shots, win: 1 - team, end: "블로킹 득점" };
      }
      shots.push(shot(1 - team, bw, T.names.blk, BA, BT, T.d.blk, 0.3));
      at = BT; first = "커버";
      continue;
    }
    shots.push(shot(team, atkWho, kind, AS, tgt, T.d.atk, 0.2));
    if (u < T.p.atkErr + T.p.block + T.p.kill || ex >= 6) { shots[shots.length - 1].r = "in"; return { shots, win: team, end: "공격 득점" }; }
    // 받아 냈다 — 상대 편 차례
    at = tgt; team = 1 - team; first = T.names.dig;
  }
  const s = shots[shots.length - 1]; s.r = "in";
  return { shots, win: s.t, end: "공격 득점" };
}

/* ══════════ 경기 만들기 ══════════ */
const TEAM_NAMES = {
  volleyball: [["한빛", "#e57373"], ["누리", "#64b5f6"]],
  jokgu: [["청솔", "#81c784"], ["바다", "#4fc3f7"]],
  sepak: [["태양", "#ffb74d"], ["별빛", "#9575cd"]],
};
const SOLO_COL = [["#ef5350", "#42a5f5"], ["#ab47bc", "#26a69a"], ["#ff7043", "#5c6bc0"]];

/** 선수 자리(그림): 샷마다 친 사람은 친 곳에, 다른 사람은 제자리 쪽으로. pos[k] = k번째 샷을 칠 때 모두의 자리, pos[n] = 끝 */
function positions(sport, shots, srv, rot) {
  const S = NETS[sport];
  const n = S.team;
  const home = [];
  for (let t = 0; t < 2; t++) for (let i = 0; i < n; i++) {
    if (n === 1) home.push(t === 0 ? [-S.L * 0.75, 0] : [S.L * 0.75, 0]);
    else {
      const slot = rot ? rot[t].indexOf(i) : i;
      home.push(mir(TEAM[sport].home[slot], t));
    }
  }
  const cur = home.map((q) => q.slice());
  const pos = [];
  shots.forEach((s, k) => {
    const id = s.t * n + s.w;
    cur[id] = s.a.slice();
    pos.push(cur.map((q) => q.slice()));
    // 친 사람은 제자리 쪽으로 반쯤, 받을 편은 공 쪽으로 조금
    cur[id] = [cur[id][0] + (home[id][0] - cur[id][0]) * 0.5, cur[id][1] + (home[id][1] - cur[id][1]) * 0.5];
    const nt = crosses(s) ? 1 - s.t : s.t;
    for (let i = 0; i < n; i++) {
      const j = nt * n + i;
      if (j === id) continue;
      cur[j] = [cur[j][0] + (s.b[0] - cur[j][0]) * (n === 1 ? 0.35 : 0.18), cur[j][1] + (s.b[1] - cur[j][1]) * (n === 1 ? 0.35 : 0.18)];
    }
  });
  pos.push(cur.map((q) => q.slice()));
  return pos;
}

/** 다시 보기를 할 샷(점수를 낸 마지막 샷) */
export function keyShot(shots) {
  for (let k = shots.length - 1; k >= 0; k--) if (shots[k].r === "net" || crosses(shots[k])) return k;
  return shots.length - 1;
}

const MEMO = new Map();
/**
 * 가상 경기 하나: { sport, seed, teams: [{ n, c, ps }], rallies: [{ shots, pos, win, srv, end, key, sc: { pre, post } }], final }
 *   sc.pre/post = { sets: [[a, b], …](끝난 세트), cur: [a, b](이번 세트 점수 — 테니스는 게임), pts?: [a, b](테니스 게임 안 점수), tb?: bool, srv }
 */
export function genMatch(sport, seed) {
  const key = `${sport}|${seed}`;
  if (MEMO.has(key)) return MEMO.get(key);
  const R = rng(hashSeed("net", sport, seed));
  const S = NETS[sport];
  let teams;
  if (S.team === 1) {
    const nm = namesOf(hashSeed("netnames", sport, seed), 2), col = SOLO_COL[seed % SOLO_COL.length];
    teams = [{ n: nm[0], c: col[0], ps: [nm[0]] }, { n: nm[1], c: col[1], ps: [nm[1]] }];
  } else {
    const tn = TEAM_NAMES[sport];
    teams = [0, 1].map((t) => {
      const nums = [];
      while (nums.length < S.team) { const v = 1 + rint(R, 24); if (!nums.includes(v)) nums.push(v); }
      return { n: tn[t][0], c: tn[t][1], ps: nums.map(String) };
    });
  }
  const rallies = [];
  let srv = R() < 0.5 ? 0 : 1;
  const sets = [];
  if (sport === "tennis") {
    let games = [0, 0], pts = [0, 0], tb = false, server = srv, tbFirst = srv;
    while (sets.filter((s) => s[0] > s[1]).length < 2 && sets.filter((s) => s[0] < s[1]).length < 2 && rallies.length < 400) {
      const total = pts[0] + pts[1];
      const cs = tb ? (total === 0 ? tbFirst : (Math.floor((total - 1) / 2) % 2 === 0 ? 1 - tbFirst : tbFirst)) : server;
      const pre = { sets: sets.map((s) => s.slice()), cur: games.slice(), pts: pts.slice(), tb, srv: cs };
      const P = tennisPoint(R, cs, total % 2 === 0);
      pts[P.win] += 1;
      let gameOver = false;
      if (tb) { if (Math.max(pts[0], pts[1]) >= 7 && Math.abs(pts[0] - pts[1]) >= 2) gameOver = true; }
      else if (Math.max(pts[0], pts[1]) >= 4 && Math.abs(pts[0] - pts[1]) >= 2) gameOver = true;
      let note = "";
      if (gameOver) {
        games[P.win] += 1;
        note = tb ? "타이브레이크 · 세트" : P.win !== cs ? "브레이크!" : "게임";
        pts = [0, 0];
        const setOver = tb || (Math.max(games[0], games[1]) >= 6 && Math.abs(games[0] - games[1]) >= 2);
        if (tb) { tb = false; server = 1 - tbFirst; }
        else server = 1 - server;
        if (setOver) { sets.push(games.slice()); games = [0, 0]; note = "세트"; }
        else if (games[0] === 6 && games[1] === 6) { tb = true; tbFirst = server; }
      }
      const post = { sets: sets.map((s) => s.slice()), cur: games.slice(), pts: pts.slice(), tb, srv: tb ? tbFirst : server };
      rallies.push({ ...P, srv: cs, sc: { pre, post }, note });
    }
  } else if (sport === "tabletennis") {
    const RU = RULES[sport];
    let cur = [0, 0], first = srv;
    while (sets.filter((s) => s[0] > s[1]).length < RU.win && sets.filter((s) => s[0] < s[1]).length < RU.win && rallies.length < 600) {
      const total = cur[0] + cur[1];
      const cs = total >= 20 ? (total % 2 === 0 ? first : 1 - first) : (Math.floor(total / 2) % 2 === 0 ? first : 1 - first);
      const pre = { sets: sets.map((s) => s.slice()), cur: cur.slice(), srv: cs };
      const P = ttPoint(R, cs);
      cur[P.win] += 1;
      let note = "";
      if (setDone(cur[0], cur[1], 11, 0)) { sets.push(cur.slice()); cur = [0, 0]; first = 1 - first; note = "게임"; }
      const t2 = cur[0] + cur[1];
      const ns = t2 >= 20 ? (t2 % 2 === 0 ? first : 1 - first) : (Math.floor(t2 / 2) % 2 === 0 ? first : 1 - first);
      rallies.push({ ...P, srv: cs, sc: { pre, post: { sets: sets.map((s) => s.slice()), cur: cur.slice(), srv: ns } }, note });
    }
  } else {
    const RU = RULES[sport], T = TEAM[sport];
    let cur = [0, 0];
    const rot = [0, 1].map(() => Array.from({ length: S.team }, (_, i) => i));
    const oi = [0, 0];                                    // 족구 서브 차례
    const server = (t) => (sport === "volleyball" ? rot[t][0] : sport === "jokgu" ? T.order[oi[t] % 4] : 0);
    while (sets.filter((s) => s[0] > s[1]).length < RU.win && sets.filter((s) => s[0] < s[1]).length < RU.win && rallies.length < 700) {
      const [to, cap] = RU.set(sets.length);
      const pre = { sets: sets.map((s) => s.slice()), cur: cur.slice(), srv, who: server(srv) };
      const P = teamPoint(R, sport, srv, rot, server(srv));
      const rotFor = rot.map((r) => r.slice());
      cur[P.win] += 1;
      let note = "";
      if (P.win !== srv) {
        // 서브권을 되찾은 편: 배구는 시계 방향 로테이션, 족구는 다음 서버
        if (sport === "volleyball") { const r = rot[P.win]; r.push(r.shift()); note = "로테이션"; }
        if (sport === "jokgu") oi[P.win] += 1;
        srv = P.win;
      }
      if (setDone(cur[0], cur[1], to, cap)) { sets.push(cur.slice()); cur = [0, 0]; note = "세트"; }
      rallies.push({ ...P, srv: pre.srv, rot: rotFor, sc: { pre, post: { sets: sets.map((s) => s.slice()), cur: cur.slice(), srv, who: server(srv) } }, note });
    }
  }
  for (const r of rallies) { r.pos = positions(sport, r.shots, r.srv, r.rot); r.key = keyShot(r.shots); }
  const out = { sport, seed, teams, rallies, final: sets };
  MEMO.set(key, out);
  if (MEMO.size > 24) MEMO.delete(MEMO.keys().next().value);
  return out;
}

/* ══════════ 배드민턴 실제 경기 → 같은 꼴 ══════════ */
const BWF_D = { "스매시": 900, "손목 스매시": 900, "러시": 800, "푸시": 1000, "드라이브": 1000, "짧은 드라이브": 1000, "뒤쪽 드라이브": 1100, "수비 드라이브": 1000,
  "클리어": 1900, "로빙": 1800, "수비 로빙": 1800, "긴 서브": 1800, "짧은 서브": 1300, "드롭": 1500, "느린 드롭": 1600, "헤어핀": 1300, "크로스 헤어핀": 1400, "네트 앞 받기": 1300 };
const BWF_H = { "클리어": 0.95, "로빙": 0.9, "수비 로빙": 0.9, "긴 서브": 0.9, "드롭": 0.55, "느린 드롭": 0.6, "헤어핀": 0.25, "크로스 헤어핀": 0.3, "네트 앞 받기": 0.3, "짧은 서브": 0.3 };
const BMEMO = new WeakMap();
/** 자료(data-badminton.js) → 경기 목록(genMatch 와 같은 꼴) */
export function badmintonMatches(data) {
  if (BMEMO.has(data)) return BMEMO.get(data);
  const out = data.matches.map((m) => {
    const teams = m.names.map((n, i) => ({ n, c: m.cols[i], ps: [n] }));
    const rallies = m.rallies.map((r) => {
      const shots = r.sh.map(([t, ty, ax, ay, bx, by]) => {
        const name = data.types[ty];
        return { t, w: 0, ty: name, a: [ax, ay], b: [bx, by], d: BWF_D[name] || 1200, h: BWF_H[name] ?? 0.4 };
      });
      const last = shots[shots.length - 1];
      last.r = /네트/.test(r.e) ? "net" : /밖/.test(r.e) ? "out" : "in";
      if (last.r === "net" && last.b[0] !== 0) {
        // 네트에 걸린 공: 떨어진 곳 대신 네트 위 자리
        const y = netY(last.a, last.b);
        if (y != null) last.b = [0, Math.round(y)];
      }
      const pos = r.sh.map(([t, , , , , , px, py, ox, oy]) => (t === 0 ? [[px, py], [ox, oy]] : [[ox, oy], [px, py]]));
      pos.push(pos[pos.length - 1].map((q) => q.slice()));
      const sets = m.sets.slice(0, r.s - 1).map((s) => s.slice());
      const win = r.w;
      const srvT = r.sh[0][0];
      return {
        shots, pos, win, srv: srvT, end: r.e, key: keyShot(shots), set: r.s,
        sc: { pre: { sets, cur: r.pre.slice(), srv: srvT }, post: { sets, cur: r.post.slice(), srv: win } },
        note: "",
      };
    });
    return { sport: "badminton", teams, rallies, final: m.sets, title: m.title, date: m.date };
  });
  BMEMO.set(data, out);
  return out;
}

/* ══════════ 시간표 ══════════ */
/** 랠리 하나의 박자: { shotsAt: [시작 …], endAt, replayAt, outAt, dur } — replay: 다시 보기를 하나 */
export function rallyTimes(r, replay) {
  const shotsAt = [];
  let t = NT.intro;
  for (const s of r.shots) { shotsAt.push(t); t += s.d; }
  const endAt = t;
  t += NT.end;
  const replayAt = t;
  if (replay) t += NT.replay;
  const outAt = t;
  t += NT.out;
  return { shotsAt, endAt, replayAt, outAt, dur: t, replay };
}
/** 다시 보기를 할 랠리인가: all 매번 · some 세 번에 한 번(점수가 크게 바뀐 랠리는 꼭) · off 안 함 */
export const doReplay = (mode, i, r) => mode === "all" || (mode === "some" && (i % 3 === 2 || r.note === "세트"));

const TMEMO = new WeakMap();
/** 경기 목록(rallies 를 이어 붙인 것)의 시간표 — [{ m, i, at, T }] 와 전체 길이 */
export function scheduleOf(matches, mode) {
  if (!TMEMO.has(matches)) TMEMO.set(matches, new Map());
  const memo = TMEMO.get(matches);
  if (memo.has(mode)) return memo.get(mode);
  const items = [];
  let at = 0, j = 0;
  matches.forEach((m, mi) => m.rallies.forEach((r, i) => {
    const T = rallyTimes(r, doReplay(mode, j++, r));
    items.push({ m: mi, i, at, T });
    at += T.dur;
  }));
  const out = { items, total: at };
  memo.set(mode, out);
  return out;
}
/** 경과 e(1× ms) → { item, t(랠리 안 시각), k(몇 번째 바퀴) } */
export function rallyAt(sched, e) {
  const { items, total } = sched;
  if (!items.length) return null;
  const k = Math.floor(Math.max(0, e) / total);
  const x = Math.max(0, e) - k * total;
  let lo = 0, hi = items.length - 1;
  while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (items[mid].at <= x) lo = mid; else hi = mid - 1; }
  return { item: items[lo], idx: lo, t: x - items[lo].at, k };
}

/* ══════════ 판서(다시 보기) ══════════ */
const dec1 = (n, d) => { const v = n / d; return (Math.round(v * 10) / 10).toFixed(1).replace("-", MINUS); };
/**
 * 한 샷의 판서 줄 — A(친 곳) · B(떨어진 곳 또는 네트에 걸린 곳)
 *   mode "m": 기울기 → 대입 → 식 → 네트(x = 0)를 지난 자리 (0, b)
 *   mode "e": 판 왼쪽 아래 원점 — 가로 · 세로 칸 → 네트까지 가로 몇 칸이면 세로 몇 칸
 */
export function netSteps(s, mode, view) {
  const A = s.a, B = s.b, isNet = s.r === "net";
  const L = lineOf(A, B);
  if (mode === "m") {
    const head = [{ s: `친 곳 ${pt(A)}` }, { s: `${isNet ? "네트에 걸린 곳" : "떨어진 곳"} ${pt(B)}` }];
    if (L.kind === "pt") return { L, lines: head };
    const { lines } = lineSteps(A, B);
    const out = [...head, ...lines];
    if (L.kind === "f" || L.kind === "h") {
      const [bn, bd] = L.b;
      out.push({ s: `네트는 x = 0 — 그때 y = b`, small: true });
      out.push({ s: `${isNet ? "걸린" : "지난"} 자리 (0, ${fs(bn, bd)})${bd !== 1 ? ` ≈ (0, ${dec1(bn, bd)})` : ""}`, col: "teal" });
    }
    return { L, lines: out };
  }
  const o = view;
  const a = [A[0] + o[0], A[1] + o[1]], b = [B[0] + o[0], B[1] + o[1]];
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const out = [{ s: `친 곳 ${pt(a)}` }, { s: `${isNet ? "네트에 걸린 곳" : "떨어진 곳"} ${pt(b)}` }];
  out.push({ s: dx === 0 ? "가로로는 그대로" : `${dx > 0 ? "오른쪽" : "왼쪽"}으로 ${Math.abs(dx)}칸` });
  out.push({ s: dy === 0 ? "세로로는 그대로" : `${dy > 0 ? "위" : "아래"}로 ${Math.abs(dy)}칸` });
  const nx = o[0] - a[0];                       // 네트까지 가로(부호 있는)
  if (dx !== 0 && !isNet) {
    const n = Math.abs(nx), h = [Math.abs(dy) * n, Math.abs(dx)];
    out.push({ s: `네트까지 가로 ${n}칸 → 세로는 ${Math.abs(dy)} × ${n} ÷ ${Math.abs(dx)} = ${fs(h[0], h[1])}칸`, small: true });
    const yn = frac(a[1] * dx + dy * nx, dx);
    out.push({ s: `네트를 지난 자리: 아래에서 ${fs(yn[0], yn[1])}칸${yn[1] !== 1 ? ` (약 ${dec1(yn[0], yn[1])})` : ""}`, col: "teal" });
  } else if (isNet) {
    out.push({ s: `네트에 걸린 자리: 아래에서 ${b[1]}칸`, col: "teal" });
  }
  return { L, lines: out };
}
/** 그 샷의 짧은 기록 줄(랠리 흐름 칸) */
export function shotLog(s, mode, view) {
  const L = lineOf(s.a, s.b);
  if (!crosses(s) && s.r !== "net") return "";
  if (mode === "m") return eqText(L) || "";
  const dx = s.b[0] - s.a[0], dy = s.b[1] - s.a[1];
  return `가로 ${Math.abs(dx)} · 세로 ${Math.abs(dy)}칸`;
}

/* ══════════ 점수 글자 ══════════ */
/** 점수판 줄: [{ name, col, sets: [n…], cur: 글자, srv: bool }] (sc = pre 또는 post) */
export function scoreRows(sport, teams, sc) {
  const won = [0, 0];
  for (const s of sc.sets) won[s[0] > s[1] ? 0 : 1] += 1;
  return [0, 1].map((t) => ({
    name: teams[t].n, col: teams[t].c, setsWon: won[t], sets: sc.sets.map((s) => s[t]),
    cur: sport === "tennis" ? String(sc.cur[t]) : String(sc.cur[t]),
    pts: sport === "tennis" ? tennisPts(sc.pts || [0, 0], sc.tb)[t] : "",
    srv: sc.srv === t,
  }));
}
