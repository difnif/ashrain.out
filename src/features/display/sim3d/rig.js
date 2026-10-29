// ashrain.out — 교실 모니터 「3D 축구」: 사람 모형의 자세 (sim3d/rig.js)
// 순수 계산. 선수는 머리·몸통·팔다리만 있는 단순한 사람 모형(더 지니어스 규칙 설명 그림처럼)이고,
// 자세는 관절 각(라디안)으로만 정한다 — engine.js 가 이 값을 모형에 그대로 얹는다.
//   hipL/hipR  다리를 앞으로 든 각(+ 앞)        kneeL/kneeR 무릎 굽힘(+)
//   shL/shR    팔을 앞으로 든 각(+ 앞·위)       abL/abR     팔을 옆으로 벌린 각(+ 바깥)    elL/elR 팔꿈치 굽힘(+)
//   lean       몸통 앞으로 숙임(+)              neck        고개 숙임(+)
//   y          엉덩이를 띄운 높이(m, 달리기 출렁임 · 점프)
//   roll       몸 전체를 옆으로 눕힌 각(+ 오른쪽으로 — 골키퍼 다이빙) · pitch 몸 전체를 앞으로 기울인 각
import { clamp, lerp } from "../core.js";

export const BODY = {
  hip: 0.93, hipW: 0.1, thigh: 0.44, shin: 0.43, foot: 0.2,
  shoulder: 1.43, shW: 0.215, upper: 0.29, fore: 0.27, head: 1.66, top: 1.84,
};

export const JOINTS = ["hipL", "hipR", "kneeL", "kneeR", "shL", "shR", "abL", "abR", "elL", "elR", "lean", "neck", "y", "roll", "pitch"];

/** 서 있는 기본 자세 */
export const REST = Object.freeze({ hipL: 0, hipR: 0, kneeL: 0.06, kneeR: 0.06, shL: 0.06, shR: 0.06, abL: 0.12, abR: 0.12, elL: 0.22, elR: 0.22,
  lean: 0.02, neck: 0.04, y: 0, roll: 0, pitch: 0 });

/** 두 자세를 섞기 (w = 0 → a, 1 → b) */
export function mixPose(a, b, w) {
  if (w <= 0) return a;
  if (w >= 1) return b;
  const o = {};
  for (const k of JOINTS) o[k] = lerp(a[k] ?? REST[k], b[k] ?? REST[k], w);
  return o;
}

/** 숨쉬기 · 무게 옮기기 — 가만히 서 있어도 조금씩 움직인다 (tw ms, seed 로 선수마다 다르게) */
export function idlePose(tw, seed = 0) {
  const s = Math.sin((tw / 1000) * 1.7 + seed * 2.1), c = Math.sin((tw / 1000) * 0.9 + seed * 1.3);
  return { ...REST, lean: 0.05 + 0.015 * s, kneeL: 0.1 + 0.04 * c, kneeR: 0.1 - 0.04 * c, hipL: 0.02 + 0.03 * c, hipR: 0.02 - 0.03 * c,
    shL: 0.08 + 0.02 * s, shR: 0.08 - 0.02 * s, y: -0.008 * (1 + s) };
}

/** 준비 자세(무릎을 굽히고 공을 본다) — 수비 · 골키퍼 */
export function readyPose(tw, seed = 0, deep = 0.6) {
  const s = Math.sin((tw / 1000) * 3.1 + seed * 2.3);
  return { ...REST, hipL: 0.35 * deep, hipR: 0.3 * deep, kneeL: 0.75 * deep + 0.04 * s, kneeR: 0.7 * deep - 0.04 * s, lean: 0.32 * deep,
    shL: 0.45 * deep, shR: 0.45 * deep, abL: 0.35 * deep, abR: 0.35 * deep, elL: 0.6 * deep, elR: 0.6 * deep, y: -0.12 * deep };
}

/**
 * 달리기 — phase(라디안, 간 거리로 정해진다) · amp 0(걷기 직전) ~ 1(전력 질주)
 * 한 걸음 주기 STRIDE m 에 2π 가 돈다.
 */
export const STRIDE = 3.2;
export function runPose(phase, amp) {
  const a = clamp(amp, 0, 1.2), s = Math.sin(phase), c = Math.cos(phase);
  const legSwing = 0.18 + 0.62 * a, armSwing = 0.15 + 0.55 * a;
  // 무릎: 다리가 뒤로 갔다가 앞으로 나올 때(회복기) 많이 굽는다
  const knee = (p) => (0.14 + 0.25 * a) + (0.35 + 0.95 * a) * Math.max(0, Math.sin(p - 0.9)) ** 1.4;
  return {
    hipL: legSwing * s, hipR: -legSwing * s,
    kneeL: knee(phase + Math.PI), kneeR: knee(phase),
    shL: -armSwing * s + 0.05, shR: armSwing * s + 0.05, abL: 0.1, abR: 0.1,
    elL: 0.5 + 0.9 * a, elR: 0.5 + 0.9 * a,
    lean: 0.05 + 0.24 * a, neck: -0.05 * a,
    y: (0.015 + 0.06 * a) * Math.abs(c) - 0.04 * a, roll: 0, pitch: 0,
  };
}

/**
 * 공 차기(오른발) — k: −1(뒤로 젖히기 시작) → 0(공에 닿음) → 1(따라 휘두르기 끝)
 * power 0.4(짧은 패스) ~ 1(크로스 · 슈팅)
 */
export function kickPose(k, power = 1, foot = "R") {
  const p = clamp(power, 0.3, 1.2);
  let swing, knee, lean, arm;
  if (k < 0) { const u = k + 1; swing = lerp(0.1, -0.95 * p, Math.sin((u * Math.PI) / 2)); knee = lerp(0.2, 1.5 * p, u); lean = lerp(0.1, -0.05, u); arm = u; }
  else { const u = Math.min(1, k); swing = lerp(-0.2, 1.35 * p, Math.sin((u * Math.PI) / 2)); knee = lerp(0.9 * p, 0.15, Math.min(1, u * 1.8)); lean = lerp(-0.05, -0.18 * p, u); arm = 1 - 0.4 * u; }
  const kick = { hip: swing, knee }, plant = { hip: -0.08, knee: 0.35 };
  const L = foot === "R" ? plant : kick, R = foot === "R" ? kick : plant;
  return { ...REST, hipL: L.hip, kneeL: L.knee, hipR: R.hip, kneeR: R.knee, lean,
    shL: 0.2 + 0.5 * arm * (foot === "R" ? 1 : -0.4), shR: 0.2 + 0.5 * arm * (foot === "R" ? -0.4 : 1),
    abL: 0.55 * arm + 0.15, abR: 0.55 * arm + 0.15, elL: 0.35, elR: 0.35, y: -0.03 };
}

/**
 * 뛰어올라 헤더 — k: 0(구름) → 0.5(가장 높이 · 머리에 닿음) → 1(내려옴). 높이는 hJump(m)
 */
export function headerPose(k, hJump = 0.7) {
  const u = clamp(k, 0, 1);
  const up = 4 * u * (1 - u);
  const arch = u < 0.5 ? lerp(0.1, -0.3, u / 0.5) : lerp(-0.3, 0.45, Math.min(1, (u - 0.5) / 0.22));   // 젖혔다가 숙이며 친다
  const tuck = Math.sin(Math.PI * u);
  return { ...REST, y: hJump * up, lean: arch, neck: u > 0.5 ? 0.35 * Math.min(1, (u - 0.5) / 0.15) : -0.2,
    hipL: 0.35 * tuck, hipR: 0.1 * tuck, kneeL: 0.25 + 0.95 * tuck, kneeR: 0.2 + 0.7 * tuck,
    shL: 0.6 + 0.9 * tuck, shR: 0.6 + 0.9 * tuck, abL: 0.55 + 0.3 * tuck, abR: 0.55 + 0.3 * tuck, elL: 0.9, elR: 0.9 };
}

/** 두 팔을 번쩍 — 골 세리머니 (tw ms 로 팔이 조금씩 흔들린다) */
export function cheerPose(tw, amp = 1) {
  const s = Math.sin((tw / 1000) * 7);
  return { ...REST, shL: 2.7 * amp, shR: 2.7 * amp, abL: 0.35 + 0.08 * s, abR: 0.35 - 0.08 * s, elL: 0.25, elR: 0.25, lean: -0.08, neck: -0.25 };
}

/**
 * 골키퍼 다이빙 — k: 0(준비) → 1(땅에 닿음). dir +1 = 골키퍼의 오른쪽, −1 = 왼쪽. reach 는 날아간 높이(m)
 */
export function divePose(k, dir = 1, reach = 0.5) {
  const u = clamp(k, 0, 1);
  const fly = Math.sin((Math.PI * Math.min(u, 0.85)) / 1.7);
  const up = dir > 0 ? { shR: 2.6, shL: 2.3 } : { shL: 2.6, shR: 2.3 };
  return { ...REST, roll: dir * 1.35 * Math.sin((Math.PI / 2) * u), y: reach * 0.9 * fly - 0.3 * u,
    ...Object.fromEntries(Object.entries(up).map(([k2, v]) => [k2, lerp(0.5, v, Math.min(1, u * 1.6))])),
    abL: 0.3, abR: 0.3, elL: 0.15, elR: 0.15, hipL: 0.25, hipR: 0.15, kneeL: 0.5 * (1 - u) + 0.2, kneeR: 0.4, lean: 0.1 };
}

/** 넘어지듯 미끄러지는 태클 · 몸을 던지는 수비 (k 0 → 1) */
export function lungePose(k, dir = 1) {
  const u = clamp(k, 0, 1);
  return { ...REST, lean: 0.25 + 0.3 * u, roll: dir * 0.25 * u, hipL: 0.9 * u, kneeL: 0.2, hipR: -0.3 * u, kneeR: 0.9 * u,
    shL: 0.6 * u, shR: 0.6 * u, abL: 0.6 * u, abR: 0.6 * u, y: -0.35 * u };
}
