// ashrain.out — 교실 모니터 「3D 축구」: 장면 대본에서 자주 쓰는 작은 도구 (sim3d/kit3d.js)
import { actor } from "./script.js";
import { lerp, E, clamp, seg } from "../core.js";
import { who } from "../facts-soccer.js";

export const lerp3 = (p, q, k) => [lerp(p[0], q[0], k), lerp(p[1], q[1], k), lerp(p[2], q[2], k)];
/** 설명 컷에 머무는 동안 아주 조금 다가간다 */
export const drift = (c, k, amt = 0.06) => ({ pos: lerp3(c.pos, lerp3(c.pos, c.at, amt), E.sine(k)), at: c.at, fov: c.fov });
/** 설명 그림이 나타났다 사라지는 정도(hold 구간 안의 시각 l, 구간 길이 d) */
// 끝은 카메라가 눈높이로 내려오기(RET 1.3초) 전에 먼저 사라진다
export const OUT0 = 1650, OUT1 = 1250;
// 처음은 카메라가 설명 자리로 올라가 멈출 때(ENTER) 나타난다
export const ENTER = 1300;
export const showO = (l, d) => Math.min(seg(l, ENTER - 400, ENTER + 100), 1 - seg(l, d - OUT0, d - OUT1));

/**
 * 명단에서 선수 하나: team = LINEUPS 의 이름, name = 명단의 한국어 이름.
 * at = 서 있는 세계 자리 [x, z] (keys 를 주면 그것으로 움직인다). kit · role 은 그대로.
 */
export function player(team, name, kit, role, at, extra = {}) {
  const [n] = who(team, name);
  return actor({ id: `${team}:${name}`, kit, n, name, role, keys: [[-9e4, at[0], at[1]], [9e4, at[0], at[1]]],
    stance: role === "rival" ? "ready" : undefined, ...extra });
}
/** 이름 없는 선수(가상의 장면) */
export function extra(id, kit, at, more = {}) {
  return actor({ id, kit, role: "rival", label: false, keys: [[-9e4, at[0], at[1]], [9e4, at[0], at[1]]], stance: "ready", ...more });
}
/** 자리 열쇠를 다른 좌표계에서 옮겨 쓰기: keys = [[tw, a, b], …] → [[tw, X, Z], …] */
export const mapKeys = (keys, f) => keys.map(([tw, a, b]) => [tw, ...f([a, b])]);
/** 선수가 공을 몰고 갈 때 공 자리 — 발 앞 ahead m, 살짝 튄다 */
export function dribble(A, ahead = 0.62, bounce = 0.06) {
  return (tw) => {
    const [x, z] = A.tr.at(tw), [vx, vz] = A.tr.vel(tw);
    const v = Math.hypot(vx, vz) || 1;
    const k = clamp(v / 4);
    const ph = (A.tr.dist(tw) / 1.6) * Math.PI;
    return [x + (vx / v) * ahead * k, 0.2 + bounce * Math.abs(Math.sin(ph)) * k, z + (vz / v) * ahead * k];
  };
}

export { lerp, E, clamp, seg };
