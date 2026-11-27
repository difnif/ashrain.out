// 강사도구 엔진 — 내보내기 (PC exporter.py): 전사용(Gemini) 묶음 · 분석용(Claude) 묶음 · 전사 결과 가져오기
import { zipStore } from "../../../../lib/zipstore";
import { parseText, parseAnswer, checkFigure } from "../../../../lib/mathir";
import { twoPass, A4W, A4H, pngToImg } from "./base";
import { Pen } from "./layout";
import { baseHash, splitLabel } from "../parts";
import { supabase } from "../../../../supabaseClient";
import GUIDE_T from "../guides/전사가이드.md?raw";
import GUIDE_A from "../guides/분석가이드.md?raw";

const CIRC = { 1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤" };
const TASKS = { all: "문항+정답+해설", solution: "해설만", done: "끝남(문항·해설 있음)", db_item: "DB 문항(애쉬레인 문항 key)" };
const safe = (s, n = 50) => String(s || "").replace(/[\\/:*?"<>|]+/g, " ").trim().replace(/\s+/g, " ").slice(0, n) || "이름없음";
const enc = (s) => new TextEncoder().encode(s);
const pad3 = (n) => String(n).padStart(3, "0");
const stampNow = () => { const d = new Date(); const p = (x) => String(x).padStart(2, "0"); return `${String(d.getFullYear()).slice(2)}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}`; };

async function pickPrints(ctx, f) {
  const { T, all, normCode } = ctx;
  const codes = (f.codes || []).map(normCode).filter((c) => c.length === 6);
  let ps;
  if (codes.length) ps = await all(() => T("tt_prints").select("*").eq("shelf", "active").in("code", codes).order("id"));
  else {
    const d0 = f.from || "0000-01-01", d1 = f.to || "9999-12-31";
    ps = await all(() => T("tt_prints").select("*").eq("shelf", "active").gte("created_at", d0 + "T00:00:00").lte("created_at", d1 + "T23:59:59.999").order("id"));
  }
  if (f.level) ps = ps.filter((p) => (p.level || "중등") === f.level);
  return ps.filter((p) => !(p.options && p.options.textbook));      // 교재(시험지 파일 없음)는 전사용 목록에서 뺌
}
async function itemsFor(ctx, pids) {
  if (!pids.length) return [];
  return ctx.all(() => ctx.T("tt_print_items").select("*").in("print_id", pids).order("seq"));
}
async function transcripts(ctx, keys) {
  if (!keys.length) return new Map();
  const out = new Map();
  for (let i = 0; i < keys.length; i += 200) {
    const rows = ctx.must(await ctx.T("tt_transcripts").select("*").in("item_key", keys.slice(i, i + 200)));
    rows.forEach((r) => out.set(r.item_key, r));
  }
  return out;
}
async function plan(ctx, prints, corpus, includeDone) {
  const byTag = new Map();
  for (const r of corpus || []) for (const t of r.src_tags || []) { if (!byTag.has(t)) byTag.set(t, []); byTag.get(t).push(r); }
  const items = await itemsFor(ctx, prints.map((p) => p.id));
  // 하위 문제로 나눈 문항(「3 (1)」 「3 (2)」)은 그림이 같은 한 문제 — 전사는 한 번(열쇠 = 하위 문제 표시를 뗀 지문)
  const keys = items.map((it) => baseHash(it.hash) || `${prints.find((p) => p.id === it.print_id).code}:${it.seq}`);
  const tr = await transcripts(ctx, [...new Set(keys)]);
  const out = [], seen = new Map();
  for (const p of prints) {
    for (const it of items.filter((x) => x.print_id === p.id)) {
      if (!it.png) continue;
      const key = baseHash(it.hash) || `${p.code}:${it.seq}`;
      if (seen.has(key)) { if (seen.get(key).code !== p.code) seen.get(key).also.push(`${p.code}-${pad3(it.seq)}`); continue; }
      let task, match = null;
      if (String(key).startsWith("key:")) task = "db_item";
      else {
        const t = tr.get(key) || null;
        if (t && t.corpus_id) match = { id: t.corpus_id };
        else if (it.tag && it.rate) {
          let cands = (byTag.get(it.tag) || []).filter((r) => String(r.p_correct ?? "").split(".")[0] === String(it.rate).replace(/[%\s]/g, ""));
          if (cands.length > 1 && CIRC[it.answer]) cands = cands.filter((r) => [it.answer, CIRC[it.answer]].includes(String(r.answer || "").trim())).length ? cands.filter((r) => [it.answer, CIRC[it.answer]].includes(String(r.answer || "").trim())) : cands;
          if (cands.length === 1) match = cands[0];
        }
        const q = !!(t && t.question), s = !!(t && t.solution);
        task = s && (q || match) ? "done" : q || match ? "solution" : "all";
      }
      const row = { id: `${p.code}-${pad3(it.seq)}`, key, code: p.code, title: p.title, seq: it.seq, label: splitLabel(it.label || String(it.seq)).base, level: p.level || "중등",
        task, tag: it.tag || "", rate: it.rate || "", quick_answer: it.answer || "", choice: !!it.choice, png: `${p.code}/${it.png}`,
        answer_png: it.answer_png ? `${p.code}/${it.answer_png}` : null, sol_png: it.sol_png ? `${p.code}/${it.sol_png}` : null,
        corpus: match ? Object.fromEntries(["id", "question", "choices", "answer", "qtype", "unit_id"].map((k) => [k, match[k] ?? null])) : null, also: [] };
      seen.set(key, row);
      out.push(row);
    }
  }
  return includeDone ? out : out.filter((r) => r.task === "all" || r.task === "solution");
}

export async function exportPrints(q, ctx) {
  const ps = await pickPrints(ctx, { from: q.from, to: q.to, level: q.level || "" });
  const sel = ps.slice(-400).reverse();
  const out = [];
  const { T, must } = ctx;
  const pids = sel.map((p) => p.id);
  const gs = pids.length ? await ctx.all(() => T("tt_gradings").select("id,print_id").in("print_id", pids)) : [];
  const sc = gs.length ? await ctx.all(() => T("tt_scans").select("grading_id").in("grading_id", gs.map((g) => g.id)).eq("deleted", false)) : [];
  const full = await plan(ctx, sel, null, true);
  void must;
  for (const p of sel) {
    const cnt = {};
    full.filter((r) => r.code === p.code).forEach((r) => (cnt[r.task] = (cnt[r.task] || 0) + 1));
    const g = gs.filter((x) => x.print_id === p.id);
    out.push({ code: p.code, code_fmt: ctx.fmtCode(p.code), title: p.title, level: p.level || "중등", kind: p.kind, n_items: p.n_items, created_at: p.created_at,
      tasks: cnt, n_gradings: g.length, n_scans: sc.filter((s) => g.some((x) => x.id === s.grading_id)).length });
  }
  return out;
}

async function corpusLookup(tags) {
  if (!tags.length) return null;
  const out = [];
  try {
    for (let i = 0; i < tags.length; i += 5) {
      const { data, error } = await supabase.from("corpus_items").select("id,question,choices,answer,qtype,unit_id,src_tags,p_correct")
        .overlaps("src_tags", tags.slice(i, i + 5)).eq("status", "active").limit(2000);
      if (error) return null;
      out.push(...(data || []));
    }
  } catch { return null; }
  return out;
}

async function itemsPdf(rows, ctx) {
  return twoPass("초등", async (c) => {
  for (const r of rows) {
    const page = c.doc.addPage([A4W, A4H]);
    const pen = new Pen(c, page);
    pen.rect(28, 24, A4W - 28, 64, { color: null, fill: [0.93, 0.95, 0.96] });
    pen.text(38, 41, `문항 ID  ${r.id}`, { size: 12, bold: true });
    let head2 = `할 일: ${TASKS[r.task]}   ·   학교급: ${r.level}`;
    if (r.quick_answer) head2 += `   ·   빠른정답: ${r.choice ? CIRC[r.quick_answer] || r.quick_answer : r.quick_answer}`;
    pen.text(38, 57, head2, { size: 9.5 });
    if (r.tag) pen.text(A4W - 38, 41, `유형: ${r.tag}  ${r.rate}%`, { size: 8, align: "right", color: [0.35, 0.35, 0.35] });
    let y = 80;
    const fit = async (bytes, x0, y0, maxw, maxh, grow = true, dpi = 150) => {
      if (!bytes) return y0;
      const img = await c.doc.embedPng(bytes);
      let s = Math.min(maxw / img.width, maxh / img.height, 72 / dpi);
      if (grow && img.width * s < maxw * 0.55) s = Math.min((maxw * 0.85) / img.width, maxh / img.height);
      pen.image(img, x0, y0, x0 + img.width * s, y0 + img.height * s);
      return y0 + img.height * s;
    };
    pen.text(34, y, "■ 문항", { size: 10, bold: true });
    y = (await fit(r._png, 40, y + 8, A4W - 80, 430)) + 14;
    if (r._apng && !(r.choice && CIRC[r.quick_answer])) {
      pen.text(34, y, "■ 빠른정답 (매쓰플랫 정답 칸)", { size: 10, bold: true });
      y = (await fit(r._apng, 40, y + 6, 300, 60, false, 110)) + 14;
    }
    if (r.corpus && r.corpus.question) {
      pen.text(34, y, "■ DB 문항 글 (고치지 말고 해설만 쓰기)", { size: 10, bold: true });
      let txt = r.corpus.question;
      if (r.corpus.choices) txt += "\n" + r.corpus.choices.map((ch, i) => `${CIRC[i + 1]} ${ch}`).join("  ");
      if (r.corpus.answer) txt += `\n정답: ${r.corpus.answer}`;
      let yy = y + 16;
      for (const ln of txt.split("\n")) {
        let cur = "";
        for (const ch of ln) {
          if (pen.width(cur + ch, 8.5) > A4W - 80) { pen.text(40, yy, cur, { size: 8.5, color: [0.15, 0.15, 0.15] }); yy += 12; cur = ""; if (yy > y + 150) break; }
          cur += ch;
        }
        if (cur && yy <= y + 150) { pen.text(40, yy, cur, { size: 8.5, color: [0.15, 0.15, 0.15] }); yy += 12; }
      }
      y = Math.min(A4H - 40, y + 150) + 10;
    }
    if (r._spng && y < A4H - 120) {
      pen.text(34, y, "■ 매쓰플랫 해설 (이것을 옮겨 적기)", { size: 10, bold: true });
      await fit(r._spng, 40, y + 6, A4W - 80, A4H - y - 50);
    }
    pen.text(34, A4H - 22, `${r.title} · ${r.code} ${r.label || r.seq}번`, { size: 7.5, color: [0.5, 0.5, 0.5] });
  }
  void ctx;
  return c.doc.save();
  });
}
const tmplRow = (r) => {
  const base = { id: r.id, task: r.task, review: null };
  if (r.corpus) base.corpus_id = r.corpus.id;
  if (r.task === "all") base.final = { qtype: r.choice ? "choice" : "short", question: "", choices: null, answer: "", difficulty_est: 3, has_math: false, has_figure: false, figure: null, unit_id: "", concept_main: null, concept_subs: [], pattern_tags: [], confidence: 0.9 };
  base.solution = { outline: "", steps: [], check: "", source: r.sol_png ? "mathflat" : "written" };
  return base;
};

export async function exportTranscribe(b, ctx) {
  const prints = await pickPrints(ctx, { codes: b.codes || [], from: b.from, to: b.to, level: b.level || "" });
  if (!prints.length) throw new Error("고른 프린트가 없어요");
  let corpus = null, note = "DB 대조 없이 만들었어요(모두 '문항+해설').";
  if (b.use_db !== false) {
    const its = await itemsFor(ctx, prints.map((p) => p.id));
    const tags = [...new Set(its.map((i) => i.tag).filter(Boolean))].sort();
    corpus = tags.length ? await corpusLookup(tags) : [];
    note = corpus !== null ? "" : "DB 대조를 하지 못했어요 — 모두 '문항+해설'로 넣었어요.";
  }
  const rows = await plan(ctx, prints, corpus, !!b.include_done);
  if (!rows.length) throw new Error("내보낼 문항이 없어요 (이미 다 전사했거나 그림 없이 등록한 프린트예요)");
  const batch = `T${stampNow()}`;
  const day = ctx.todayStr();
  const root = `${day} 전사용 ${batch}`;
  const files = [];
  const man = [];
  for (const r of rows) {
    const fs = {};
    for (const [k, sub, key] of [["png", "문항", "_png"], ["answer_png", "빠른정답", "_apng"], ["sol_png", "매쓰플랫해설", "_spng"]]) {
      if (!r[k]) continue;
      try { r[key] = await ctx.bytes(r[k]); } catch { continue; }
      const fn = `${r.id}_${sub}.png`;
      files.push({ name: `${root}/images/${fn}`, data: r[key] });
      fs[sub] = "images/" + fn;
    }
    man.push({ id: r.id, task: r.task, task_name: TASKS[r.task], level: r.level, title: r.title, seq: r.seq, quick_answer: r.quick_answer, choice: r.choice,
      tag: r.tag, rate: r.rate, mathflat_solution: !!r.sol_png, db_item: r.corpus, same_item_in: r.also, files: fs });
  }
  files.unshift({ name: `${root}/문항.pdf`, data: await itemsPdf(rows, ctx) });
  files.push({ name: `${root}/목록.json`, data: enc(JSON.stringify({ batch, made: new Date().toISOString().slice(0, 19), items: man }, null, 1)) });
  files.push({ name: `${root}/결과_양식.json`, data: enc(JSON.stringify(rows.map(tmplRow), null, 1)) });
  const nAll = rows.filter((r) => r.task === "all").length, nSol = rows.filter((r) => r.task === "solution").length;
  const lv = {};
  rows.forEach((r) => (lv[r.level] = (lv[r.level] || 0) + 1));
  const g = GUIDE_T.replaceAll("{{BATCH}}", batch).replaceAll("{{N}}", String(rows.length)).replaceAll("{{N_ALL}}", String(nAll)).replaceAll("{{N_SOL}}", String(nSol))
    .replaceAll("{{LEVELS}}", Object.entries(lv).map(([k, v]) => `${k} ${v}`).join(" · ") || "-").replaceAll("{{N_MFSOL}}", String(rows.filter((r) => r.sol_png).length));
  files.push({ name: `${root}/00_먼저_읽기_전사가이드.md`, data: enc(g) });
  try { const m = await import("../guides/mathir.py.txt?raw"); files.push({ name: `${root}/mathir.py`, data: enc(m.default) }); } catch { /* */ }
  const zip = zipStore(files);
  ctx.log("export_transcribe", null, null, { batch, n: rows.length, n_all: nAll, n_sol: nSol, prints: prints.map((p) => p.code) });
  return { batch, n: rows.length, n_all: nAll, n_sol: nSol, note, zip_name: `${root}.zip`, blob: new Blob([zip], { type: "application/zip" }) };
}

export async function exportAnalysis(b, ctx) {
  const { T, all, must, fmtCode } = ctx;
  const codes = (b.codes || []).map(ctx.normCode).filter((c) => c.length === 6);
  let q = () => {
    let x = T("tt_gradings").select("*").order("updated_at");
    if (!codes.length && b.from) x = x.gte("updated_at", b.from + "T00:00:00");
    if (!codes.length && b.to) x = x.lte("updated_at", b.to + "T23:59:59.999");
    const sids = (b.student_ids || []).map(Number).filter(Boolean);
    if (sids.length) x = x.in("student_id", sids);
    return x;
  };
  let gs = await all(q);
  const prints = gs.length ? must(await T("tt_prints").select("*").in("id", [...new Set(gs.map((g) => g.print_id))])) : [];
  const pm = new Map(prints.map((p) => [p.id, p]));
  gs = gs.filter((g) => pm.get(g.print_id)?.shelf === "active" && (!codes.length || codes.includes(pm.get(g.print_id).code)));
  if (!gs.length) throw new Error("고른 범위에 채점 기록이 없어요");
  const sts = must(await T("tt_students").select("id,name,grade").in("id", [...new Set(gs.map((g) => g.student_id))]));
  const sm = new Map(sts.map((s) => [s.id, s]));
  gs.sort((a, b2) => (sm.get(a.student_id)?.name || "").localeCompare(sm.get(b2.student_id)?.name || "", "ko") || String(a.updated_at).localeCompare(String(b2.updated_at)));
  const root = `${ctx.todayStr()} 분석용 A${stampNow()}`;
  const files = [], table = [], data = [], done = new Set();
  let nScans = 0;
  const KO = { O: "맞음", X: "틀림", U: "안 풂" };
  for (const g of gs) {
    const p = pm.get(g.print_id), st = sm.get(g.student_id) || { name: "?" };
    const d = await ctx.gradingDetail(g.id);
    const pdir = `${safe(p.title, 40)} ${fmtCode(p.code)}`;
    if (!done.has(p.code)) {
      done.add(p.code);
      const f = p.files || {};
      for (const [src, dst] of [[f.sheet, "시험지.pdf"], [f.answer, "정답해설.pdf"]]) if (src) { try { files.push({ name: `${root}/프린트/${pdir}/${dst}`, data: await ctx.bytes(src) }); } catch { /* */ } }
      for (const it of d.items) for (const [k, sub] of [["png", "문항"], ["answer_png", "정답"], ["sol_png", "해설"]]) {
        if (it[k]) { try { files.push({ name: `${root}/프린트/${pdir}/${sub}/${pad3(it.seq)}.png`, data: await ctx.bytes(`${p.code}/${it[k]}`) }); } catch { /* */ } }
      }
    }
    const sd = `${root}/학생/${safe(st.name, 20)}/${pdir}`;
    // 스캔본 이름 끝 = 언제 스캔한 것인지(선생님이 올릴 때 표시): _1차 = 1차 채점 때 · _2차 = 2차 채점 때 · _차수모름 = 확실하지 않음
    const scanNames = [], when = new Map();
    for (let i = 0; i < d.scans.length; i++) {
      const sc = d.scans[i];
      const ext = (/\.([A-Za-z0-9]{1,5})$/.exec(sc.name) || [, sc.kind === "pdf" ? "pdf" : "jpg"])[1].toLowerCase();
      const fn = `스캔_${String(i + 1).padStart(2, "0")}_${sc.round ? sc.round + "차" : "차수모름"}.${ext}`;
      try { files.push({ name: `${sd}/${fn}`, data: await ctx.bytes(sc.path) }); nScans++; scanNames.push(`학생/${safe(st.name, 20)}/${pdir}/${fn}`); } catch { /* */ }
      when.set(sc.round || 0, (when.get(sc.round || 0) || 0) + 1);
    }
    const whenLine = [...when.entries()].sort((a, c) => (a[0] || 99) - (c[0] || 99)).map(([r, n]) => `${r ? r + "차 채점 때" : "확실하지 않음"} ${n}`).join(" · ");
    const gItems = [];
    for (const it of d.items) {
      const m = it.mark || {};
      const rr = (it.rounds || []).filter((x) => x.result);
      const by = Object.fromEntries(rr.map((x) => [x.round, x.result]));
      const row = { 학생: st.name, 학년: st.grade || "", 코드: fmtCode(p.code), 프린트: p.title, 학교급: p.level || "", 번호: it.label || String(it.seq), 객관식: it.choice ? "예" : "",
        정답: it.answer || (it.answer_png ? "(그림)" : ""), "학생 답": m.answer || "", 결과: KO[m.result] || "안 매김", "1차": KO[by[1]] || "", "2차": KO[by[2]] || "", "3차": KO[by[3]] || "",
        차수별: rr.map((x) => `${x.round}차 ${x.result}`).join(" → "), "최종 차": m.round || "", 회차: m.session_no || "", "매긴 때": String(m.at || "").slice(0, 16),
        유형: it.tag || it.topic || "", 정답률: it.rate || "", "문항 그림": it.png ? `프린트/${pdir}/문항/${pad3(it.seq)}.png` : "" };
      table.push(row);
      gItems.push({ seq: it.seq, label: row.번호, choice: !!it.choice, key: row.정답, given: m.answer || "", result: m.result || "", rounds: rr, session: m.session_no || null, tag: row.유형, rate: row.정답률 });
    }
    const s = d.summary;
    data.push({ student: st.name, code: fmtCode(p.code), title: p.title, status: g.status, started: g.created_at, updated: g.updated_at, sessions: d.sessions, summary: s, scans: scanNames, items: gItems });
    const nr = Math.max(1, ...gItems.flatMap((gi) => gi.rounds.map((x) => x.round)));
    let md = `# ${st.name} · ${p.title} (${fmtCode(p.code)})\n\n- 결과: 맞음 ${s.O} · 틀림 ${s.X} · 안 풂 ${s.U} · 안 매김 ${s.none} / ${s.total}문항\n`;
    md += `- 채점: ${nr}차까지 · 회차 ${d.sessions.length} (2차·3차 = 틀리거나 안 푼 문항을 다시 푼 것)\n`;
    md += `- 스캔본 ${d.scans.length}개${d.scans.length ? `: ${whenLine} — 파일 이름 끝 \`_1차\` · \`_2차\` · \`_차수모름\`` : ""}\n\n`;
    md += `| 번호 | 정답 | 학생 답 | ${Array.from({ length: nr }, (_, k) => `${k + 1}차`).join(" | ")} | 최종 |\n|${"---|".repeat(nr + 4)}\n`;
    for (const gi of gItems) {
      const by = Object.fromEntries(gi.rounds.map((x) => [x.round, x.result]));
      md += `| ${gi.label} | ${gi.choice ? CIRC[gi.key] || gi.key : gi.key} | ${gi.given} | ${Array.from({ length: nr }, (_, k) => ({ O: "O", X: "X", U: "안 풂" }[by[k + 1]] || "")).join(" | ")} | ${{ O: "O", X: "X", U: "안 풂" }[gi.result] || "-"} |\n`;
    }
    files.push({ name: `${sd}/채점.md`, data: enc(md) });
  }
  const cols = Object.keys(table[0]);
  const csvCell = (v) => { v = String(v ?? ""); return /[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v; };
  files.push({ name: `${root}/채점결과.csv`, data: enc("﻿" + [cols.join(","), ...table.map((r) => cols.map((c) => csvCell(r[c])).join(","))].join("\r\n") + "\r\n") });
  files.push({ name: `${root}/채점결과.json`, data: enc(JSON.stringify({ made: new Date().toISOString().slice(0, 19), gradings: data }, null, 1)) });
  const students = [...new Set(gs.map((g) => sm.get(g.student_id)?.name || "?"))].sort((a, c) => a.localeCompare(c, "ko"));
  const gt = GUIDE_A.replaceAll("{{N_G}}", String(gs.length)).replaceAll("{{N_S}}", String(students.length)).replaceAll("{{STUDENTS}}", students.join(", "))
    .replaceAll("{{N_P}}", String(done.size)).replaceAll("{{N_SCANS}}", String(nScans)).replaceAll("{{PERIOD}}", codes.length ? "고른 프린트" : `${b.from || "처음"} ~ ${b.to || "오늘"}`);
  files.push({ name: `${root}/00_분석요청_가이드.md`, data: enc(gt) });
  const zip = zipStore(files);
  ctx.log("export_analysis", null, null, { n: gs.length, students: students.length, scans: nScans });
  return { n_gradings: gs.length, n_students: students.length, n_prints: done.size, n_scans: nScans, zip_name: `${root}.zip`, blob: new Blob([zip], { type: "application/zip" }) };
}

export async function importTranscripts(body, ctx) {
  const { T, must } = ctx;
  let obj;
  const txt = String(body.text || "").replace(/^﻿/, "");
  try { obj = JSON.parse(txt); } catch (e) {
    const m = /```(?:json)?\s*(\[[\s\S]*\])\s*```/.exec(txt) || /(\[\s*\{[\s\S]*\}\s*\])/.exec(txt);
    if (!m) throw new Error("JSON을 읽지 못했어요: " + e.message);
    obj = JSON.parse(m[1]);
  }
  const rows = Array.isArray(obj) ? obj : obj.items || obj.results || [];
  const batch = !Array.isArray(obj) ? obj.batch || null : null;
  let ok = 0, review = 0;
  const bad = [];
  const now = new Date().toISOString();
  for (const row of rows) {
    const rid = String((row || {}).id || "");
    const m = /^([23456789A-HJKMNP-Z]{6})-(\d{1,3})$/.exec(rid.toUpperCase());
    if (!m) { bad.push({ id: rid || "?", why: "id 형식이 아님(예: 8ACWPD-007)" }); continue; }
    const p = must(await T("tt_prints").select("id,level").eq("code", m[1]).maybeSingle());
    const it = p && must(await T("tt_print_items").select("*").eq("print_id", p.id).eq("seq", Number(m[2])).maybeSingle());
    if (!it) { bad.push({ id: rid, why: "강사도구에 없는 문항" }); continue; }
    const key = it.hash || `${m[1]}:${Number(m[2])}`;
    const old = must(await T("tt_transcripts").select("*").eq("item_key", key).maybeSingle());
    if (row.review) {
      review++;
      must(await T("tt_transcripts").upsert({ item_key: key, print_id: p.id, seq: it.seq, level: p.level, question: old ? old.question : null, solution: old ? old.solution : null,
        corpus_id: old ? old.corpus_id : null, source: old && old.question ? old.source : "review", batch, updated_at: now }, { onConflict: "owner,item_key" }));
      continue;
    }
    const why = [];
    const fin = row.final;
    if (fin) {
      const q = String(fin.question || "");
      if (!q.trim()) why.push("question 비어 있음");
      for (const [label, t] of [["question", q], ...(fin.choices || []).map((x, i) => [`choices[${i + 1}]`, String(x)])]) {
        const e = parseText(t).errs;
        if (e.length) why.push(`${label} 수식 오류 ${e[0].code} ${String(e[0].src || "").slice(0, 30)}`);
      }
      if (fin.answer !== undefined && fin.answer !== null && fin.answer !== "") { try { parseAnswer(String(fin.answer)); } catch (e) { why.push(`answer 표기 오류: ${String(e.message || e).slice(0, 40)}`); } }
      if (fin.figure) { const fe = checkFigure(Array.isArray(fin.figure) ? fin.figure : [fin.figure]); if (fe.length) why.push("figure 오류: " + (fe[0].msg || "")); }
      if (fin.choices && ![4, 5].includes(fin.choices.length)) why.push("choices는 4~5개");
    }
    const sol = row.solution;
    if (sol) {
      const steps = sol && typeof sol === "object" ? sol.steps : null;
      if (!Array.isArray(steps) || !steps.filter((s) => String(s).trim()).length) why.push("solution.steps 비어 있음");
      else for (const stx of [sol.outline || "", ...steps, sol.check || ""]) { const e = parseText(String(stx)).errs; if (e.length) { why.push(`해설 수식 오류 ${e[0].code} ${String(e[0].src || "").slice(0, 30)}`); break; } }
    }
    if (!fin && !sol) why.push("final·solution이 둘 다 없음");
    if (why.length) { bad.push({ id: rid, why: why.slice(0, 3).join(" / ") }); continue; }
    const qj = fin ? JSON.stringify(fin) : old ? old.question : null;
    const sj = sol ? JSON.stringify(sol) : old ? old.solution : null;
    let cid = row.corpus_id || (old ? old.corpus_id : null);
    if (!cid && !qj && row.task === "solution") cid = "db";
    must(await T("tt_transcripts").upsert({ item_key: key, print_id: p.id, seq: it.seq, level: p.level, question: qj, solution: sj, corpus_id: cid, source: "gemini", batch, updated_at: now }, { onConflict: "owner,item_key" }));
    ok++;
  }
  ctx.log("import_transcripts", null, null, { ok, review, bad: bad.length });
  return { ok, review, bad };
}
export { pngToImg };
