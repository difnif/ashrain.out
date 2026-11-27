// 강사도구 엔진 — 시험지 만들기·저장 (PC make_prints · mf2exam.prepare/_compose · wrong_make)
import { MM, toPng, pngToImg, imgHash, openPdf } from "./base";
import { nn } from "../sb";
import { DEFAULTS, GEO, colBox, plan, renderSheet, buildAnswerPdf, dividerPage, fmtCode } from "./layout";
import { variants, info } from "./partsplit";
import { parse, titleOf, isAnswerOnly, answerPages, parseQuick, renderQuick, solutionPages, parseSolutions, pageImageNoNames } from "./mathflat";
import { twoPass, A4W, A4H } from "./base";
import { partsFromAnswer, expandParts, splitLabel, baseHash, partLabel } from "../parts";

export function settings(opts = {}) {
  const cfg = { ...DEFAULTS };
  try { Object.assign(cfg, JSON.parse(localStorage.getItem("tt:cfg") || "{}")); } catch { /* 기본값 */ }
  cfg.양식 = opts.template || cfg.양식 || "문정중";
  cfg.주관식_이름 = opts.label || cfg.주관식_이름 || "서답형";
  for (const [ko, kc] of [["title", "제목"], ["sub", "부제"], ["upper", "윗줄"], ["footer", "바닥글_왼쪽"]]) {
    if (opts[ko] != null && String(opts[ko]).trim() !== "") cfg[kc] = String(opts[ko]).trim();
  }
  if (opts.target_space_mm) cfg.목표_여백_mm = Number(opts.target_space_mm);
  cfg.대상 = "";
  return cfg;
}

// 문항 준비 — 변형 후보·크기·객관식 여부·지문
export async function prepare(items, cfg) {
  const [x0, , x1] = colBox(1, 0);
  const widthPt = x1 - x0 - GEO.gutter;
  const k = widthPt / 930;
  items.forEach((it, idx) => {
    it.seq = idx + 1;
    let a = null;
    try { a = info(it.img); } catch { a = { choice: false, A: null }; }
    let vs = [[it.img, 0]];
    if (cfg.그림_선택지_변형) { try { vs = vs.concat(variants(it.img, a.A)); } catch { /* 원본만 */ } }
    it.vimgs = vs.map(([v]) => v);
    it.pens = vs.map(([, p]) => p);
    const kk = it.k || k;
    it.sizes = vs.map(([v]) => { const wpt = Math.min(v.w * kk, widthPt); return [wpt, (v.h * wpt) / v.w]; });
    it.heights = it.sizes.map((s) => s[1]);
    if (it.choice == null) it.choice = !!a.choice;
    if (!it.hash) it.hash = imgHash(it.img);
    it.w = it.choice ? 1.0 : 1.25;
    it.renders = [];
  });
}
export async function composeSheet(items, cfg, title, sub) {
  const layout = plan(items, cfg);
  if (!layout) throw new Error("알맞은 배치를 찾지 못했어요 — 설정의 최소 여백을 줄여 보세요.");
  for (const [k, i, pick] of layout.cols) for (let t = k; t < i; t++) {
    const it = items[t], v = pick[t - k];
    if (!it.renders[v]) it.renders[v] = v === 0 && it.raw ? it.raw : await toPng(it.vimgs[v]);
  }
  const pdf = await renderSheet(items, layout, cfg, title, sub);
  return { pdf, layout, name_boxes: cfg._name_box ? [cfg._name_box] : [] };
}

// 코드 잡기 (내 프린트끼리 겹치지 않게)
export async function reserveCode(ctx, want = null) {
  const { T, must, newCode, normCode } = ctx;
  if (want) {
    const c = normCode(want);
    if (c.length === 6 && !must(await T("tt_prints").select("id").eq("code", c).limit(1)).length) return c;
  }
  for (let i = 0; i < 50; i++) {
    const c = newCode();
    if (!must(await T("tt_prints").select("id").eq("code", c).limit(1)).length) return c;
  }
  throw new Error("코드를 만들지 못했어요");
}

// 여러 파일을 몇 개씩 함께 올린다 — 하나씩 차례로 올리면 파일마다 오가는 시간이 쌓여 문항이 많을수록 오래 걸림.
// done: 올린 경로를 모음(실패하면 지우기용). 하나라도 실패하면 남은 것은 올리지 않고 그 오류를 던짐.
export async function putAll(put, files, limit = 8, done = []) {
  let k = 0, err = null;
  const worker = async () => {
    while (!err && k < files.length) {
      const f = files[k++];
      try { await put(f.rel, f.data, f.type || "application/octet-stream"); done.push(f.rel); } catch (e) { err = err || e; }
    }
  };
  await Promise.all(Array.from({ length: Math.min(limit, files.length) }, worker));
  if (err) throw err;
  return done;
}

// 파일 올리고 표에 넣기 → printBrief
export async function storePrint(ctx, { code, row, items, files, targets = [], logKind, logDetail = {} }) {
  const { T, must, put, remove, log } = ctx;
  const done = [];
  try {
    await putAll(put, files, 8, done);
  } catch (e) { try { await remove(done); } catch { /* */ } throw e; }
  let pid = null;
  try {
    const pr = must(await T("tt_prints").insert(nn("tt_prints", { code, ...row })).select("id").single());
    pid = pr.id;
    for (let i = 0; i < items.length; i += 200) must(await T("tt_print_items").insert(nn("tt_print_items", items.slice(i, i + 200).map((it) => ({ print_id: pid, ...it })))));
    if (targets.length) must(await T("tt_targets").upsert(targets.map((s) => ({ print_id: pid, student_id: s })), { onConflict: "print_id,student_id", ignoreDuplicates: true }));
  } catch (e) {
    if (pid) await T("tt_prints").delete().eq("id", pid);
    try { await remove(done); } catch { /* */ }
    throw e;
  }
  if (logKind) log(logKind, null, pid, { code, ...logDetail });
  return ctx.printBrief(pid);
}

const natKey = (s) => String(s).split(/(\d+)/).map((t) => (/^\d+$/.test(t) ? t.padStart(8, "0") : t.toLowerCase())).join("");
const strip = (ctx, s, names) => ctx.stripNames(s, names);
// 첫 쪽 「이름」 칸에 적힌 값 (제목에서 빼려고)
async function nameValues(doc) {
  const { pageSpans, pageLines } = await import("./base");
  try {
    const page = await doc.getPage(1);
    const lines = pageLines(await pageSpans(page));
    const out = [];
    for (const l of lines) {
      const i = l.spans.findIndex((s) => /^(이름|성명)\s*[:：]?$/.test(s.t));
      if (i >= 0) for (const s of l.spans.slice(i + 1, i + 2)) if (/^[가-힣]{2,4}$/.test(s.t)) out.push(s.t);
      const m = /(?:이름|성명)\s*[:：]\s*([가-힣]{2,4})/.exec(l.text);
      if (m) out.push(m[1]);
    }
    return out;
  } catch { return []; }
}

// ── 매쓰플랫 변환
export async function convert(body, ctx) {
  const opts = body.options || {};
  const cfg0 = settings(opts);
  if (opts.answer_design === false) cfg0.정답해설_원본모양 = true;
  try { localStorage.setItem("tt:defaults", JSON.stringify(Object.fromEntries(["template", "label", "mode", "upper", "footer", "answer_design"].map((k) => [k, opts[k]])))); } catch { /* */ }
  const ups = [], answers = [];
  for (const u of body.uploads || []) {
    const f = await ctx.takeUpload(u.id);
    const doc = await openPdf(f.bytes);
    const d = { ...f, name: ctx.cleanName(u.name || f.name), doc, title: await titleOf(doc) };
    ((await isAnswerOnly(doc)) ? answers : ups).push(d);
  }
  if (!ups.length) throw new Error(answers.length ? "변환할 시험지 PDF가 없어요 (빠른정답만 들어 있어요)" : "변환할 PDF가 없어요");
  const pair = (u) => (!answers.length ? null : ups.length === 1 ? answers[0] : answers.find((a) => a.title && a.title === u.title) || null);
  const sids = await ctx.ensureStudents(opts.targets || []);
  const known = await ctx.knownNames();
  const groups = (opts.mode === "merge" ? [ups] : ups.map((u) => [u])).map((g) => [...g].sort((a, b) => (natKey(a.name) < natKey(b.name) ? -1 : 1)));
  const made = [], errors = [];
  for (const g of groups) {
    try { made.push(await buildMathflat(g, pair, cfg0, opts, ctx, known, sids)); }
    catch (e) { console.error(e); errors.push({ files: g.map((u) => u.name), error: e.message || String(e) }); }
  }
  const unpaired = answers.filter((a) => !ups.some((u) => pair(u) === a)).map((a) => a.name);
  if (unpaired.length) errors.push({ files: unpaired, error: "어느 시험지의 빠른정답인지 몰라 붙이지 못했어요. 프린트함에서 그 프린트를 열고 [정답 PDF 첨부]로 붙여 주세요." });
  return { made, errors };
}

async function buildMathflat(group, pair, cfg0, opts, ctx, known, sids) {
  const cfg = { ...cfg0 };
  const code = await reserveCode(ctx);
  cfg.코드 = code;
  const items = [], parts = [], titles = [], subs = [];
  const found = new Set();
  for (const u of group) {
    (await nameValues(u.doc)).forEach((n) => found.add(n));
    const r = await parse(u.bytes);
    if (!r.items.length) { parts.push({ src: u.name, n: 0, error: "매쓰플랫 문항을 찾지 못함" }); continue; }
    const first = items.length + 1;
    let quick = {}, qdoc = null;
    try {
      if (r.ansFrom != null) { qdoc = r.doc; quick = await parseQuick(r.doc, await answerPages(r.doc, r.ansFrom)); }
      const a = pair(u);
      if (!Object.keys(quick).length && a) { qdoc = await openPdf(a.bytes); quick = await parseQuick(qdoc); }
    } catch (e) { console.warn("빠른정답", e); quick = {}; }
    const sols = {}, left = [];
    try {
      for (const [sdoc, s0] of [[r.doc, r.ansFrom], [qdoc && qdoc !== r.doc ? qdoc : null, 0]]) {
        if (!sdoc || s0 == null) continue;
        const sp = await solutionPages(sdoc, s0);
        if (!sp.length) continue;
        const [got, used] = await parseSolutions(sdoc, sp);
        Object.assign(sols, got);
        sp.filter((i) => !used.includes(i)).forEach((i) => left.push([sdoc, i]));
      }
    } catch (e) { console.warn("해설", e); }
    for (const it of r.items) {
      it.src = u.name;
      const q = quick[it.no];
      it.answer = ""; it.answer_png = null; it.answer_wh = null;
      it.sol = sols[it.no] ? { img: sols[it.no].img, w: sols[it.no].w, h: sols[it.no].h } : null;
      if (q) {
        it.answer = q.choice || q.text || "";
        // 하위 문제 (1)(2)…: 정답 글자로, 정답이 그림이면 정답 줄의 표시로 — 하위 문제마다 따로 채점
        if (!q.choice) it.parts = partsFromAnswer(q.text) || partsFromAnswer(String(q.marks || "").replace(/^[^(（⑴-⒇]*/, ""));
        try { const rq = await renderQuick(qdoc, q); it.answer_png = rq.png; it.answer_wh = rq.wh; } catch { /* */ }
      }
    }
    items.push(...r.items);
    parts.push({ src: u.name, n: r.items.length, first, last: items.length, doc: r.doc, ansFrom: r.ansFrom, left, hasQuick: !!Object.keys(quick).length });
    if (r.title && !titles.includes(r.title)) titles.push(r.title);
    if (r.sub && !subs.includes(r.sub)) subs.push(r.sub);
  }
  if (!items.length) throw new Error("매쓰플랫 문항을 찾지 못했어요 — 매쓰플랫에서 받은 학습지 PDF가 맞는지 확인해 주세요.");
  const names = [...new Set([...known, ...found])];
  const stem = group[0].name.replace(/\.pdf$/i, "");
  let title = cfg.제목 || titles[0] || stem;
  let sub = cfg.부제 || (subs.length <= 2 ? subs.join(" · ") : `${subs[0]} 외 ${subs.length - 1}개 범위`);
  title = strip(ctx, title, names) || "학습지";
  sub = strip(ctx, sub, names);
  await prepare(items, cfg);
  for (const it of items) for (let v = 0; v < it.vimgs.length; v++) void v;
  const sheet = await composeSheet(items, cfg, title, sub);
  // 정답해설
  let answerPdf = null;
  const hasAny = items.some((it) => it.answer || it.answer_png || it.sol);
  const withAns = parts.filter((p) => p.ansFrom != null || p.hasQuick || (p.left && p.left.length));
  const solPng = new Map();
  for (const it of items) if (it.sol) { it.sol.png = await toPng(it.sol.img); solPng.set(it.seq, it.sol.png); }
  if (!cfg.정답해설_원본모양 && hasAny) {
    const leftPages = [];
    for (const p of parts) for (const [d, i] of p.left || []) leftPages.push(await pageImageNoNames(d, i, names));
    const entries = items.map((it) => ({ seq: it.seq, choice: !!it.choice, answer: it.answer || "", answer_png: it.answer_png, answer_wh: it.answer_wh, sol: it.sol ? { png: it.sol.png, w: it.sol.w, h: it.sol.h } : null }));
    answerPdf = (await buildAnswerPdf(entries, cfg, title, leftPages)).pdf;
  } else if (withAns.length) {
    const imgs = [];
    for (const p of withAns) if (p.ansFrom != null) for (let i = p.ansFrom; i < p.doc.numPages; i++) imgs.push([p, await pageImageNoNames(p.doc, i, names)]);
    const many = parts.filter((p) => p.n).length > 1;
    answerPdf = await twoPass(cfg.양식, async (c2) => {
    for (const p of withAns) {
      if (p.ansFrom == null) continue;
      if (many) await dividerPage(c2, [[`시험지 ${p.first}~${p.last}번의 정답·해설`, 20, true], [`이 뒤의 정답은 원래 번호 1~${p.last - p.first + 1}번으로 적혀 있어요.`, 12, false],
        [p.first > 1 ? `(원래 번호 + ${p.first - 1} = 시험지 번호)` : "(원래 번호 = 시험지 번호)", 12, false], [p.src, 10, false]]);
      for (const [q, pg] of imgs) {
        if (q !== p) continue;
        const page = c2.doc.addPage([pg.w || A4W, pg.h || A4H]);
        page.drawImage(await c2.doc.embedPng(pg.png), { x: 0, y: 0, width: pg.w || A4W, height: pg.h || A4H });
      }
    }
    return c2.doc.getPageCount() ? c2.doc.save() : null;
    });
  }
  // 저장
  const files = [{ rel: `${code}/sheet.pdf`, data: sheet.pdf, type: "application/pdf" }];
  if (answerPdf) files.push({ rel: `${code}/answer.pdf`, data: answerPdf, type: "application/pdf" });
  const probs = [];
  for (const it of items) {
    const n3 = String(it.seq).padStart(3, "0");
    files.push({ rel: `${code}/items/${n3}.png`, data: it.raw || (await toPng(it.img)), type: "image/png" });
    if (it.answer_png) files.push({ rel: `${code}/answers/${n3}.png`, data: it.answer_png, type: "image/png" });
    if (it.sol) files.push({ rel: `${code}/sols/${n3}.png`, data: it.sol.png, type: "image/png" });
    probs.push({ no: String(it.seq), parts: it.choice ? null : it.parts || null,
      row: { seq: it.seq, src: strip(ctx, it.src, names), src_no: String(it.no), choice: !!it.choice, hash: it.hash, png: `items/${n3}.png`,
        answer: it.answer || "", answer_png: it.answer_png ? `answers/${n3}.png` : null, sol_png: it.sol ? `sols/${n3}.png` : null,
        tag: it.tag || "", rate: String(it.rate || "").replace("정답률", "").trim() } });
  }
  const rows = expandParts(probs);                 // 하위 문제가 있는 문항은 하위 문제마다 한 줄(label 「3 (1)」)
  const srcNames = group.map((u) => strip(ctx, u.name, names) || "학습지.pdf");
  const nch = rows.filter((r) => r.choice).length;
  const brief = await storePrint(ctx, {
    code, items: rows, files, targets: sids,
    row: { title, sub, kind: "mathflat", template: cfg.양식, label: cfg.주관식_이름, level: ctx.guessLevel(title, sub, cfg.양식), n_items: rows.length, n_choice: nch,
      pages: sheet.layout.P, sources: srcNames, files: { sheet: `${code}/sheet.pdf`, answer: answerPdf ? `${code}/answer.pdf` : null, src: [], extras: [] },
      name_boxes: sheet.name_boxes, options: Object.fromEntries(Object.entries(opts).filter(([k]) => k !== "targets")), shelf: "active" },
    logKind: "convert", logDetail: { title, items: items.length, parts: rows.length - items.length, pages: sheet.layout.P, template: cfg.양식, files: srcNames, anon: found.size, solutions: items.filter((it) => it.sol).length },
  });
  brief.anon_removed = found.size;
  return brief;
}

// ── 오답 모아 출제
export async function wrongMake(b, ctx) {
  const { T, must, normCode, bytes, todayStr, stripNames } = ctx;
  const picks = (b.items || []).filter((x) => x && typeof x === "object").map((x) => [normCode(x.code), Number(x.seq) || 0]).filter(([c, s]) => c && s);
  if (!picks.length) throw new Error("고른 문항이 없어요");
  if (picks.length > 120) throw new Error("한 번에 120문항까지 담을 수 있어요");
  const codes = [...new Set(picks.map(([c]) => c))];
  const prints = must(await T("tt_prints").select("id,code,title,kind,level").in("code", codes));
  const pm = new Map(prints.map((p) => [p.code, p]));
  const its = prints.length ? await ctx.all(() => T("tt_print_items").select("*").in("print_id", prints.map((p) => p.id))) : [];
  const got = [];
  let skipped = 0;
  for (const [c, s] of picks) {
    const pr = pm.get(c);
    const it = pr && its.find((x) => x.print_id === pr.id && x.seq === s);
    if (!it || !it.png) { skipped++; continue; }
    got.push([pr, it]);
  }
  if (!got.length) throw new Error("그림이 있는 문항이 없어요 (쪽 단위로 등록한 프린트의 문항은 담을 수 없어요)");
  const cfg = settings({ template: b.template, label: b.label, upper: b.upper, footer: b.footer });
  const known = await ctx.knownNames();
  const title = stripNames(String(b.title || "").trim(), known) || `오답 모음 ${todayStr().slice(5).replace("-", "/")}`;
  const srcs = [];
  for (const [pr] of got) { const t = `${pr.title} ${fmtCode(pr.code)}`; if (!srcs.includes(t)) srcs.push(t); }
  const sub = stripNames(String(b.sub || "").trim(), known) || (srcs.length === 1 ? srcs[0] : `${got[0][0].title} 외 ${srcs.length - 1}개 프린트`);
  cfg.제목 = title; cfg.부제 = sub;
  const sids = (b.targets || []).map(Number).filter(Boolean);
  const code = await reserveCode(ctx);
  cfg.코드 = code;
  // 하위 문제(「3 (2)」)는 그 문제 그림을 한 번만 싣고, 고른 하위 문제마다 채점 줄을 만든다
  const groups = [];
  for (const [pr, it] of got) {
    const last = groups[groups.length - 1];
    const part = splitLabel(it.label).part;
    if (part && last && last.pr === pr && last.parts && last.its[0].png === it.png && splitLabel(last.its[0].label).base === splitLabel(it.label).base) { last.its.push(it); continue; }
    groups.push({ pr, its: [it], parts: part > 0 });
  }
  const items = [];
  for (const { pr, its, parts } of groups) {
    const it = its[0];
    const raw = await bytes(`${pr.code}/${it.png}`);
    const e = { img: await pngToImg(raw), raw, no: it.seq, src: `${pr.title} ${fmtCode(pr.code)}`, choice: parts ? false : !!it.choice,
      hash: (parts ? baseHash(it.hash) : it.hash) || `${pr.code}:${it.seq}`,
      answer: parts ? its.map((x) => `${partLabel(splitLabel(x.label).part)} ${x.answer || ""}`.trim()).join(" ") : it.answer || "",
      answer_png: null, answer_wh: null, sol: null, tag: it.tag || "", rate: it.rate || "",
      k: it.scale || (pr.kind === "registered" ? 72 / 150 : null), from: [pr, it], parts: parts ? its : null };
    if (it.answer_png) {
      try { e.answer_png = await bytes(`${pr.code}/${it.answer_png}`); const im = await pngToImg(e.answer_png); e.answer_wh = [(im.w * 72) / 220, (im.h * 72) / 220]; } catch { /* */ }
    }
    if (it.sol_png) {
      try { const sp = await bytes(`${pr.code}/${it.sol_png}`); const im = await pngToImg(sp); e.sol = { png: sp, w: (im.w * 72) / 200, h: (im.h * 72) / 200 }; } catch { /* */ }
    }
    items.push(e);
  }
  const keep = items.map((it) => [it.choice, it.hash]);
  await prepare(items, cfg);
  items.forEach((it, i) => { const [ch, h] = keep[i]; if (ch != null) { it.choice = !!ch; it.w = ch ? 1.0 : 1.25; } if (h) it.hash = h; });
  cfg.정답해설_원본모양 = false;
  const sheet = await composeSheet(items, cfg, title, sub);
  const hasAny = items.some((it) => it.answer || it.answer_png || it.sol);
  const answerPdf = hasAny ? (await buildAnswerPdf(items.map((it) => ({ seq: it.seq, choice: !!it.choice, answer: it.answer, answer_png: it.answer_png, answer_wh: it.answer_wh, sol: it.sol })), cfg, title)).pdf : null;
  const files = [{ rel: `${code}/sheet.pdf`, data: sheet.pdf, type: "application/pdf" }];
  if (answerPdf) files.push({ rel: `${code}/answer.pdf`, data: answerPdf, type: "application/pdf" });
  const rows = [];
  for (const it of items) {
    const n3 = String(it.seq).padStart(3, "0");
    const [pr, src] = it.from;
    files.push({ rel: `${code}/items/${n3}.png`, data: it.raw, type: "image/png" });
    if (it.answer_png) files.push({ rel: `${code}/answers/${n3}.png`, data: it.answer_png, type: "image/png" });
    if (it.sol) files.push({ rel: `${code}/sols/${n3}.png`, data: it.sol.png, type: "image/png" });
    const base = { src: it.src, png: `items/${n3}.png`, answer_png: it.answer_png ? `answers/${n3}.png` : null, sol_png: it.sol ? `sols/${n3}.png` : null,
      tag: it.tag, rate: it.rate, topic: src.topic || "", scale: it.k };
    if (it.parts) {
      for (const x of it.parts) rows.push({ ...base, seq: rows.length + 1, label: `${it.seq} ${partLabel(splitLabel(x.label).part)}`, src_no: x.label || String(x.seq),
        choice: false, hash: x.hash || `${pr.code}:${x.seq}`, answer: x.answer || "", points: x.points ?? null, origin: `${pr.code}:${x.seq}:${x.label || x.seq}` });
      continue;
    }
    rows.push({ ...base, seq: rows.length + 1, src_no: String(src.label || src.seq), choice: !!it.choice, hash: it.hash,
      answer: it.answer, label: String(it.seq), points: src.points ?? null, origin: `${pr.code}:${src.seq}:${src.label || src.seq}` });
  }
  const lvl = got.map(([pr]) => pr.level).find(Boolean) || ctx.guessLevel(title, sub, cfg.양식);
  const brief = await storePrint(ctx, {
    code, items: rows, files, targets: sids,
    row: { title, sub, kind: "wrong", template: cfg.양식, label: cfg.주관식_이름, level: lvl, n_items: rows.length, n_choice: rows.filter((r) => r.choice).length,
      pages: sheet.layout.P, sources: srcs, files: { sheet: `${code}/sheet.pdf`, answer: answerPdf ? `${code}/answer.pdf` : null, src: [], extras: [] },
      name_boxes: sheet.name_boxes, options: { wrong_from: got.map(([pr, it]) => `${pr.code}:${it.seq}`), which: b.which || "" }, shelf: "active" },
    logKind: "wrongset_make", logDetail: { title, items: items.length, skipped, sources: srcs.length, targets: sids.length },
  });
  // 지문 없는 문항의 전사본은 새 프린트 번호로도 이어 둔다
  try {
    const keys = got.filter(([, it]) => !it.hash).map(([pr, it]) => `${pr.code}:${it.seq}`);
    if (keys.length) {
      const trs = must(await T("tt_transcripts").select("*").in("item_key", keys));
      const add = [];
      items.forEach((it) => {
        const [pr, src] = it.from;
        const t = trs.find((x) => x.item_key === `${pr.code}:${src.seq}`);
        if (t && !src.hash) add.push({ item_key: it.hash, print_id: brief.id, seq: it.seq, level: t.level, question: t.question, solution: t.solution, corpus_id: t.corpus_id, source: t.source, batch: t.batch });
      });
      if (add.length) await T("tt_transcripts").upsert(add, { onConflict: "owner,item_key", ignoreDuplicates: true });
    }
  } catch { /* 전사본 잇기는 실패해도 됨 */ }
  brief.skipped = skipped;
  return brief;
}
export { MM };
