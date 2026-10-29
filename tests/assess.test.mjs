// node tests/assess.test.mjs — 서술형 평가 순수 로직: 쪽 번호 띠(부호·판독) · 사진 파이프라인(합성 사진) · 평가 JSON 검사·공개 분리·합산
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { checkOf, encodePage, decodeBits, codeCells, readPageCode, pageQuality, judgeQuality, sheetSpec, readRegion, relBoxes, unionBox, markerRects, ORIENT, PAGECODE } from "../src/lib/assess/sheet.js";
import { validateSpec, publicView, answerKey, canReveal, aggregate, policyOf, normGrade, normName, personKey, gradeLabel } from "../src/lib/assess/spec.js";
import { analyzePhoto } from "../src/lib/assess/pipeline.js";
import { homography, applyH } from "../src/lib/omr/detect.js";

let pass = 0, fail = 0;
const ok = (c, name) => { if (c) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SPEC = JSON.parse(fs.readFileSync(path.join(HERE, "fixtures/assess-SAMPLE01.json"), "utf8"));
const clone = (o) => JSON.parse(JSON.stringify(o));

// ── 1. 확인값 · 띠 부호 ───────────────────────────────────────────────────────
// 생성기(build_assess.py check_of)가 낸 값과 같아야 한다
const PY = { SAMPLE01: 10, SAMPLE02: 14, M1014A: 12, E1015B: 24, ABCD: 22, ZZZZZZZZZZZZ: 29 };
ok(Object.entries(PY).every(([c, v]) => checkOf(c) === v), "checkOf = 생성기(Python) 값");
// 생성기(build_assess.py encode_page)가 낸 비트 — 해밍(13,9)+전체 패리티 14칸
const PYBITS = { "3,10": "00101000010100", "5,17": "10100100100011", "15,31": "01111111111110", "1,0": "11100000000001" };
ok(Object.entries(PYBITS).every(([k, s]) => { const [p, c] = k.split(",").map(Number); return encodePage(p, c).join("") === s; }), "encodePage = 생성기 비트 (14칸)");
let rt = true;
for (let p = 1; p <= 15; p++) for (let c = 0; c < 32; c++) { const d = decodeBits(encodePage(p, c)); if (!(d.ok && d.page === p && d.check === c)) rt = false; }
ok(rt, "모든 쪽(1~15)·확인값(0~31) 왕복");
// 칸 1~3개를 잘못 읽으면 어떤 값으로도 통과하지 않는다 (최소 거리 4)
let flips = 0, leaked = 0;
for (let p = 1; p <= 15; p++) for (let c = 0; c < 32; c++) {
  const base = encodePage(p, c);
  for (let i = 0; i < 14; i++) {
    const b1 = base.slice(); b1[i] ^= 1; flips++; if (decodeBits(b1).ok) leaked++;
    for (let j = i + 1; j < 14; j++) {
      const b2 = b1.slice(); b2[j] ^= 1; flips++; if (decodeBits(b2).ok) leaked++;
      for (let k = j + 1; k < 14; k++) { const b3 = b2.slice(); b3[k] ^= 1; flips++; if (decodeBits(b3).ok) leaked++; }
    }
  }
}
ok(leaked === 0 && flips === 480 * (14 + 91 + 364), `칸 1~3개 오독 ${flips}가지 모두 거부`);
ok(!decodeBits(new Array(14).fill(0)).ok && !decodeBits(new Array(14).fill(1)).ok, "빈 띠·전부 검은 띠는 실패");
ok(!decodeBits(encodePage(3, 10).slice(0, 10)).ok, "칸 수가 다르면 실패");
ok(SPEC.sheet.pagecode.check === checkOf(SPEC.code), "샘플 JSON 확인값 = checkOf(code)");

// ── 2. 합성 래스터에서 띠 읽기 ────────────────────────────────────────────────
function paintPage(page, check, { scale = 1.4, noise = 0, paper = 240, ink = 25, holes = [] } = {}) {
  const W = Math.round(1000 * scale), H = Math.round(1414 * scale);
  const g = new Uint8Array(W * H).fill(paper);
  const rect = (x, y, w, h, v) => {
    for (let yy = Math.round(y * scale); yy < Math.round((y + h) * scale); yy++)
      for (let xx = Math.round(x * scale); xx < Math.round((x + w) * scale); xx++) if (xx >= 0 && yy >= 0 && xx < W && yy < H) g[yy * W + xx] = v;
  };
  for (const m of markerRects()) rect(m.x, m.y, m.size, m.size, ink);
  rect(ORIENT.x, ORIENT.y, ORIENT.w, ORIENT.h, ink);
  encodePage(page, check).forEach((b, i) => { if (b && !holes.includes(i)) { const c = codeCells()[i]; rect(c.x, c.y, c.w, c.h, ink); } });
  // 본문 흉내: 글줄
  for (let y = 160; y < 1280; y += 26) rect(40, y, 700 + ((y * 7) % 200), 4, 90);
  if (noise) for (let i = 0; i < g.length; i++) g[i] = Math.max(0, Math.min(255, g[i] + Math.round((Math.sin(i * 12.9898) * 43758.5453 % 1) * noise)));
  return { gray: g, width: W, height: H, scale };
}
const p5 = readPageCode(paintPage(5, 17), null);
ok(p5.ok && p5.page === 5 && p5.check === 17, "합성 쪽: 5쪽·확인 17 판독");
const p12 = readPageCode(paintPage(12, 3, { noise: 30, paper: 200, ink: 60 }), null);
ok(p12.ok && p12.page === 12 && p12.check === 3, "잡음·낮은 대비에서도 판독");
const firstBlack = encodePage(7, 9).indexOf(1);
const holed = readPageCode(paintPage(7, 9, { holes: [firstBlack] }), null);
ok(!holed.ok, "검은 칸 하나가 지워지면(손가락·빛 반사) 거부");
// 애매한 칸(회색) → 여유(margin) 부족으로 거부
const grayCell = paintPage(6, 21);
{ const c = codeCells()[encodePage(6, 21).indexOf(0)], s = grayCell.scale;
  for (let yy = Math.round(c.y * s); yy < Math.round((c.y + c.h) * s); yy++) for (let xx = Math.round(c.x * s); xx < Math.round((c.x + c.w) * s); xx++) grayCell.gray[yy * grayCell.width + xx] = 140; }
const gc = readPageCode(grayCell, null);
ok(!gc.ok && gc.margin < 0.12, `회색으로 번진 칸 → 여유 ${gc.margin} 로 거부`);
const q1 = pageQuality(paintPage(3, 1));
ok(judgeQuality(q1).ok, "또렷한 합성 쪽 품질 통과");
const dark = paintPage(3, 1, { paper: 70, ink: 20 });
ok(judgeQuality(pageQuality(dark)).reason === "dark", "어두운 사진 → dark");

// ── 3. 합성 '사진'(원근 변형) → analyzePhoto ───────────────────────────────────
function photoOf(page, check, { rot = 0 } = {}) {
  const src = paintPage(page, check, { scale: 1 });               // 1단위 = 1px 원본 종이
  const W = 1700, H = 2300;                                         // 사진 크기
  const g = new Uint8Array(W * H).fill(90);                         // 어두운 책상
  // 종이 네 귀퉁이(종이 좌표 0,0 ~ 1000,1414)를 사진 위 비뚤어진 사각형으로
  const pageCorners = [[0, 0], [1000, 0], [1000, 1414], [0, 1414]];
  let dst = [[180, 160], [1540, 230], [1600, 2120], [120, 2050]];
  if (rot === 180) dst = dst.map(([x, y]) => [W - x, H - y]);
  const Hm = homography(dst, pageCorners);                          // 사진 → 종이
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const [u, v] = applyH(Hm, x, y);
    if (u >= 0 && v >= 0 && u < 1000 && v < 1414) g[y * W + x] = src.gray[Math.floor(v) * 1000 + Math.floor(u)];
  }
  return { gray: g, width: W, height: H };
}
const set = { sheet: SPEC.sheet, pages: SPEC.pages };
const ph3 = photoOf(3, SPEC.sheet.pagecode.check);
const a3 = analyzePhoto(ph3, null, set);
ok(a3.ok && a3.page === 3 && a3.kind === "item", "합성 사진 → 3쪽(문제 쪽)으로 펴서 판독");
const a180 = analyzePhoto(photoOf(4, SPEC.sheet.pagecode.check, { rot: 180 }), null, set);
ok(a180.ok && a180.page === 4, "거꾸로 찍은 사진도 4쪽");
const aOther = analyzePhoto(photoOf(3, (SPEC.sheet.pagecode.check + 5) % 32), null, set);
ok(!aOther.ok && aOther.reason === "other", "다른 평가 시험지 → other");
const aNone = analyzePhoto({ gray: new Uint8Array(1200 * 1600).fill(230), width: 1200, height: 1600 }, null, set);
ok(!aNone.ok && aNone.reason === "markers", "마커 없는 사진 → markers");
const aGhost = analyzePhoto(photoOf(9, SPEC.sheet.pagecode.check), null, set);
ok(!aGhost.ok && aGhost.reason === "other", "이 평가에 없는 쪽(9쪽) → other");

// ── 4. 판독 영역 ──────────────────────────────────────────────────────────────
const itemPage = SPEC.pages.find((p) => p.kind === "item");
const reg = readRegion(itemPage);
ok(reg && reg[1] <= itemPage.regions.s1[1] && reg[3] >= itemPage.regions.s3[3], "문제 쪽 판독 영역 = ①~③ 칸 합집합");
const rb = relBoxes(itemPage);
ok(rb.s1 && rb.s3 && rb.s1.y < rb.s2.y && rb.s2.y < rb.s3.y && !rb.q, "칸 상대 위치(위→아래, 문제 상자 제외)");
const infoReg = readRegion(SPEC.pages.find((p) => p.kind === "info"));
ok(infoReg && infoReg[3] - infoReg[1] > 300, "2쪽 판독 영역(학년·이름·필적·닉네임)");
ok(readRegion(SPEC.pages[0]) === null, "1쪽(안내)은 판독 영역 없음");
ok(JSON.stringify(unionBox([[10, 10, 20, 20], [5, 30, 40, 50]], 2)) === "[3,8,42,52]", "unionBox 여백");
ok(sheetSpec(SPEC.sheet).markers.length === 4 && sheetSpec(null).orient.x === 122, "sheetSpec 기본값");

// ── 5. JSON 검사 ──────────────────────────────────────────────────────────────
const v = validateSpec(SPEC, { bytes: 8000 });
ok(v.ok && v.summary.n_items === 3 && v.summary.max === 30, "샘플 JSON 통과 (3문제 30점)");
const bad1 = clone(SPEC); bad1.code = "SAMPLE99";
ok(validateSpec(bad1).errors.some((e) => e.includes("확인값")), "code 를 손으로 바꾸면 확인값 오류");
const bad2 = clone(SPEC); delete bad2.items[1].answer;
ok(validateSpec(bad2).errors.some((e) => e.includes("answer")), "정답 없으면 오류");
const bad3 = clone(SPEC); bad3.items[1].figure_svg = '<svg onload="alert(1)"></svg>';
ok(validateSpec(bad3).errors.some((e) => e.includes("실행 코드")), "그림 SVG 에 실행 코드 → 오류");
const bad4 = clone(SPEC); bad4.items[0].points = 9;
ok(validateSpec(bad4).errors.some((e) => e.includes("rubric 합")), "배점 합 불일치 → 오류");
const bad5 = clone(SPEC); bad5.pages[2].regions.s2 = [0, 0, 2000, 10];
ok(validateSpec(bad5).errors.some((e) => e.includes("좌표")), "칸 좌표가 시트 밖 → 오류");
const bad3b = clone(SPEC); bad3b.items[1].figure_svg = '<svg><use xlink:href="data:x"/></svg>';
ok(validateSpec(bad3b).errors.some((e) => e.includes("실행 코드")), "그림 SVG 에 <use>/href → 오류");
const bad5b = clone(SPEC); bad5b.sheet.pagecode = { ...bad5b.sheet.pagecode, n: 10 };
ok(validateSpec(bad5b).errors.some((e) => e.includes("14칸")), "옛 10칸 띠 JSON → 다시 만들라는 오류");
const bad5c = clone(SPEC); delete bad5c.sheet.orient; bad5c.sheet.pagecode.check = (bad5c.sheet.pagecode.check + 1) % 32;
const e5c = validateSpec(bad5c).errors;
ok(e5c.some((e) => e.includes("orient")) && e5c.some((e) => e.includes("확인값")), "orient 누락·확인값 불일치를 함께 알림");
const bad6 = clone(SPEC); bad6.kind = "other";
ok(!validateSpec(bad6).ok, "kind 다르면 거부");
const bad7 = clone(SPEC); bad7.pages = bad7.pages.filter((p) => p.kind !== "info").map((p, i) => ({ ...p, no: i + 1 }));
ok(validateSpec(bad7).errors.some((e) => e.includes("응시 정보")), "2쪽(응시 정보) 없으면 오류");
ok(!validateSpec(null).ok && !validateSpec([]).ok, "객체가 아니면 거부");

// ── 6. 공개 분리 · 정답 · 공개 시점 ───────────────────────────────────────────
const pub = publicView(SPEC);
const pubText = JSON.stringify(pub);
ok(!pubText.includes('"answer"') && !pubText.includes('"solution"') && !pubText.includes('"criterion"') && !pubText.includes("partial"), "공개용에 정답·풀이·기준 문장 없음");
ok(pub.items[0].points === 10 && pub.items[0].elements.length === 3 && pub.items[1].figure_svg?.startsWith("<svg"), "공개용: 배점·요소 이름·그림");
ok(answerKey(SPEC)[2].answer.includes("frac(3,10)"), "정답 키");
ok(canReveal({ reveal: "after_submit", submitted: true }) && !canReveal({ reveal: "after_submit", submitted: false }), "after_submit");
ok(!canReveal({ reveal: "after_submit", submitted: true, complete: false }), "after_submit: 문제 쪽을 다 찍지 않고 제출했으면 마감 전엔 비공개");
ok(canReveal({ reveal: "after_submit", submitted: true, complete: false, status: "closed" }), "after_submit: 빠진 쪽이 있어도 마감 뒤엔 공개");
ok(!canReveal({ reveal: "after_close", submitted: true, status: "live" }) && canReveal({ reveal: "after_close", submitted: true, status: "closed" }), "after_close: 마감 뒤에만");
ok(canReveal({ reveal: "after_close", submitted: true, status: "live", closes_at: "2020-01-01T00:00:00Z" }), "after_close: 마감 시각이 지났으면");
ok(!canReveal({ reveal: "never", submitted: true, status: "closed" }), "never");

// ── 7. 합산 · 정책 · 이름/학년 정리 ───────────────────────────────────────────
const agg = aggregate(SPEC, { 1: { marks: [{ no: 1, got: 4 }, { no: 2, got: 9 }, { no: 3, got: -2 }] }, 3: { marks: [{ no: 1, got: 2.6 }, { no: 2, got: 3 }, { no: 3, got: 3 }] } });
ok(agg.items[0].got === 7 && agg.items[1].got === 0 && !agg.items[1].graded && agg.items[2].got === 9 && agg.total === 16 && agg.max === 30, "합산: 배점 상한·음수 0·반올림·빠진 문항 0");
ok(policyOf({ policy: { carry: "weird", answer_only_max: "4" } }).carry === "half" && policyOf({ policy: { answer_only_max: "4" } }).answer_only_max === 4, "정책 기본값·정리");
ok(normGrade("2", "mid") === "m2" && normGrade("중학교 3학년", "mid") === "m3" && normGrade("4", "elem") === "e4" && normGrade("7", "mid") === null && normGrade("", "mid") === null, "학년 정리");
ok(normName(" 김 민준 ") === "김민준" && normName("!!") === null && normName("홍길동(1)") === "홍길동1", "이름 정리");
ok(normName("김⍰준") === null && normName("김?준") === null, "못 읽은 글자가 섞인 이름은 버림(글자를 빼고 붙이지 않음)");
ok(personKey({ name: "김민준", grade: "m2" }) === "n:김민준|m2" && personKey({ name: "", grade: "m2" }) === null, "응시자 키");
ok(gradeLabel("m2") === "중2" && gradeLabel("e4") === "초4" && gradeLabel("x") === "x", "학년 표시");
ok(PAGECODE.n === SPEC.sheet.pagecode.n && PAGECODE.x0 === SPEC.sheet.pagecode.x0, "앱·생성기 띠 좌표 일치");

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
