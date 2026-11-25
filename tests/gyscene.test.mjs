// node tests/gyscene.test.mjs — 시록고 격언 그림(gyScene.js): 1,009개 항목이 모두 그려지는지 · 같은 입력이면 같은 그림 · 코드 결 · 정답률 없음
import { readFileSync } from "node:fs";
import { drawScene, circleKind, whoOf, sceneInfo, TYPE_COLOR } from "../src/apps/seirocco/gyeokeon/gyScene.js";

const data = JSON.parse(readFileSync(new URL("../public/gyeokeon/gyeokeon.v2.json", import.meta.url), "utf8"));
let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; } else { fail++; console.log("FAIL -", name); } };

/** 아주 작은 XML 짝 맞춤 검사: 여는 태그 · 닫는 태그 · 스스로 닫는 태그, 글자 속 날 '<' 없음 */
function wellFormed(svg) {
  const stack = [], re = /<(\/?)([a-zA-Z][\w:-]*)([^<>]*?)(\/?)>|([^<>]+)/g;
  let m, at = 0;
  while ((m = re.exec(svg))) {
    if (m.index !== at) return false;
    at = re.lastIndex;
    if (m[5] != null) continue;
    if (m[1]) { if (stack.pop() !== m[2]) return false; }
    else if (!m[4]) stack.push(m[2]);
  }
  return at === svg.length && stack.length === 0;
}

// 합성 달 기록(실제 학생 아님): 첫 달 · 코멘트 없음 · 동점 달이 섞여 있다
const S0 = { rush: 0, shadow: 0, cross: 0, steady: 0, stubborn: 0, cue: 0, evap: 0, shrink: 0, auto: 0 };
const months = [
  { S: { ...S0, steady: .6, cue: .2 }, who: "P", seen: 1 },
  { S: { ...S0 }, who: "E", seen: 0 },
  { S: { ...S0, rush: .4, cue: .4 }, who: "AI", seen: 1 },
  { S: { ...S0, cue: .7 }, who: "O", seen: 1 },
];
const code = { months, cum: 2100, R: 4, name: "하늘", label: "2026.11", nth: 4 };

// 1) 모든 항목: 밝은 바탕 · 어두운 바탕 · 코드 결
let drawn = 0, broken = [], big = 0, total = 0;
for (const e of data.entries) {
  for (const o of [{}, { theme: "dark" }, code]) {
    let svg = "";
    try { svg = drawScene(e, o); } catch (err) { broken.push(e.id + " " + err.message); continue; }
    const good = svg.startsWith("<svg") && svg.endsWith("</svg>") && !/NaN|undefined|Infinity/.test(svg) && wellFormed(svg);
    if (good) drawn++; else broken.push(e.id);
    total += svg.length; big = Math.max(big, svg.length);
  }
}
ok(drawn === data.entries.length * 3, `모든 항목이 그려짐 ${drawn}/${data.entries.length * 3} ${broken.slice(0, 5).join(" · ")}`);
ok(total / drawn < 40000 && big < 120000, `그림 크기 평균 ${(total / drawn / 1024).toFixed(1)}KB · 가장 큰 것 ${(big / 1024).toFixed(1)}KB`);

// 2) 같은 입력이면 같은 그림, 이름이 다르면 붓 결이 달라진다
const e0 = data.entries.find((e) => e.id === "ZL21");
ok(drawScene(e0) === drawScene(e0), "같은 항목 → 같은 그림");
ok(drawScene(e0, code) === drawScene(e0, { ...code }), "같은 코드 → 같은 그림");
ok(drawScene(e0, code) !== drawScene(e0, { ...code, name: "바다" }), "다른 아이 → 다른 붓 결");

// 3) 코드 결: 달마다 한 겹, 그달 주 유형 색, 도장 · 날짜
const withCode = drawScene(e0, code);
ok(withCode.includes(TYPE_COLOR.steady) && withCode.includes(TYPE_COLOR.cue), "지난 달 주 유형 색이 결에 든다");
ok((withCode.match(/stroke-dasharray=".3 2.2"/g) || []).length === 1, "코멘트 없는 달은 점선 한 겹");
ok(withCode.includes(">하<") && withCode.includes(">늘<") && withCode.includes("2026.11 · 4번째 달"), "도장 · 날짜");
ok(!drawScene(e0).includes("번째 달"), "찾아보기 그림에는 도장 · 날짜가 없다");
ok(drawScene(e0, { ...code, name: "<b>" }).includes("&lt;"), "이름 글자는 이스케이프");

// 4) 정답률은 그림에 들어가지 않는다 — 방향(dacc) · 정답률 밴드가 달라도 그림이 같다
const up = months.map((m, i) => (i === 3 ? { ...m, dacc: 1, acc: 4 } : m)), down = months.map((m, i) => (i === 3 ? { ...m, dacc: -1, acc: 1 } : m));
ok(drawScene(e0, { ...code, months: up }) === drawScene(e0, { ...code, months: down }), "정답률이 달라도 같은 그림");
ok(!/정답률/.test(drawScene(e0, code)), "그림 글자에 정답률 없음");

// 5) 장면 읽기
const ck = (t) => circleKind(t).kind;
ok(ck("해") === "sun" && ck("산 위의 해") === "sun" && ck("바다 위의 해") === "sun", "원: 해(곁말은 배경)");
ok(ck("해시계") === "sundial" && ck("수레바퀴") === "wheel" && ck("우물") === "well" && ck("엽전") === "coin", "원: 해시계 · 바퀴 · 우물 · 엽전");
ok(ck("저녁 대야 물에 비친 얼굴") !== "gate", "원: '얼굴'의 '굴'은 굴 입구가 아니다");
ok(ck("둥근 논배미 — 둘레에 모가 섬") === "paddy" && ck("나무 밑동 나이테") === "rings", "원: 논배미 · 나이테");
ok(whoOf("아이").child && whoOf("어머니").hat === "bun" && whoOf("임금").hat === "crown" && whoOf("장수").hat === "helm", "인물: 아이 · 여인 · 임금 · 장수");
ok(whoOf("말").animal === "horse" && whoOf("학").animal === "crane" && whoOf("어린 여우").animal === "fox" && whoOf("용").animal === "dragon", "동물: 말 · 학 · 여우 · 용");
const six = ["LI01", "LS01", "MZ01", "GT01", "ZG01", "SN01"];
ok(six.every((id) => sceneInfo(data.entries.find((e) => e.id === id)).bespoke), "시안 여섯 장면은 손그림 그대로");
const kinds = new Set(data.entries.map((e) => ck(e.scene.circle)));
ok(!kinds.has("plain") || data.entries.filter((e) => ck(e.scene.circle) === "plain").length < 10, "원 갈래를 못 읽은 항목이 10개 미만");

console.log(fail ? `실패 ${fail} · 통과 ${pass}` : `통과 ${pass} — 그림 ${drawn}장`);
process.exit(fail ? 1 : 0);
