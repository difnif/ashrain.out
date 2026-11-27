// 강사도구 엔진 — 보고서 PDF(채점 결과 · 학습 기록) · 이름 넣어 출력 · 스캔본 한 PDF로
import { pdflib, canvas, toBlob, A4W, A4H, twoPass, embedText } from "./base";

// ── 아주 작은 표 짜기 (PC html_pdf 의 모양: 제목 · 설명 줄 · 상자 · 소제목 · 표, 바닥에 제목·쪽)
async function report(blocks, footer) {
  return twoPass("초등", async ({ P, doc, R, B }) => {
  const L = 40, Rt = A4W - 40, TOP = 42, BOT = A4H - 46;
  const ink = P.rgb(0.06, 0.09, 0.16), sub = P.rgb(0.28, 0.33, 0.41), line = P.rgb(0.8, 0.84, 0.88), red = P.rgb(0.75, 0.1, 0.1), soft = P.rgb(0.95, 0.97, 0.98);
  let page = null, y = 0;
  const pages = [];
  const newPage = () => { page = doc.addPage([A4W, A4H]); pages.push(page); y = TOP; };
  newPage();
  const W = (f, s, t) => f.widthOfTextAtSize(String(t), s);
  const clipText = (f, s, t, w) => {
    t = String(t ?? "");
    if (W(f, s, t) <= w) return t;
    while (t.length > 1 && W(f, s, t + "…") > w) t = t.slice(0, -1);
    return t + "…";
  };
  const text = (t, x, yy, { f = R, s = 10, c = ink } = {}) => page.drawText(String(t), { x, y: A4H - yy, size: s, font: f, color: c });
  const need = (h) => { if (y + h > BOT) newPage(); };
  for (const b of blocks) {
    if (b.h1) { need(30); y += 18; text(b.h1, L, y, { f: B, s: 16 }); y += 10; }
    else if (b.meta) { need(16); y += 11; text(clipText(R, 9.5, b.meta, Rt - L), L, y, { s: 9.5, c: sub }); y += 6; }
    else if (b.box) {
      need(28); y += 4;
      page.drawRectangle({ x: L, y: A4H - (y + 22), width: Rt - L, height: 22, color: soft, borderColor: line, borderWidth: 0.7 });
      text(clipText(B, 10.5, b.box, Rt - L - 16), L + 8, y + 15, { f: B, s: 10.5 });
      y += 26;
    } else if (b.h2) { need(40); y += 20; text(b.h2, L, y, { f: B, s: 12 }); y += 7; }
    else if (b.table) {
      const { head, rows, left = [] } = b.table;
      const s = 8.6, rh = 15;
      const n = head.length;
      const want = head.map((h, i) => Math.max(W(B, s, h), ...rows.map((r) => W(i === 0 && false ? B : R, s, r[i] ?? ""))) + 10);
      const tot = want.reduce((a, c) => a + c, 0);
      const avail = Rt - L;
      let ws = want.slice();
      if (tot > avail) {
        // 넓은 칸(왼쪽 맞춤 칸)부터 줄인다
        const flex = ws.map((w, i) => (left.includes(i) ? w : 0));
        const fixed = tot - flex.reduce((a, c) => a + c, 0);
        const room = Math.max(40, avail - fixed);
        const fsum = flex.reduce((a, c) => a + c, 0) || 1;
        ws = ws.map((w, i) => (left.includes(i) ? (w * room) / fsum : w));
        const t2 = ws.reduce((a, c) => a + c, 0);
        if (t2 > avail) ws = ws.map((w) => (w * avail) / t2);
      } else if (left.length) {
        const extra = (avail - tot) / left.length;
        ws = ws.map((w, i) => (left.includes(i) ? w + extra : w));
      } else ws = ws.map((w) => (w * avail) / tot);
      const drawRow = (cells, bold, bg) => {
        need(rh);
        if (bg) page.drawRectangle({ x: L, y: A4H - (y + rh), width: avail, height: rh, color: bg });
        let x = L;
        for (let i = 0; i < n; i++) {
          const raw = cells[i];
          const isX = raw === "X";
          const t = clipText(bold ? B : R, s, raw ?? "", ws[i] - 6);
          const tw = W(bold ? B : R, s, t);
          const tx = left.includes(i) ? x + 4 : x + (ws[i] - tw) / 2;
          text(t, tx, y + 10.6, { f: bold || isX ? B : R, s, c: isX ? red : ink });
          x += ws[i];
        }
        page.drawLine({ start: { x: L, y: A4H - (y + rh) }, end: { x: Rt, y: A4H - (y + rh) }, thickness: 0.5, color: line });
        y += rh;
      };
      need(rh * 2);
      drawRow(head, true, soft);
      for (const r of rows) {
        if (y + rh > BOT) { newPage(); drawRow(head, true, soft); }
        drawRow(r, false, null);
      }
      y += 4;
    }
  }
  const gray = P.rgb(0.45, 0.45, 0.45);
  pages.forEach((p, i) => {
    p.drawText(clipText(R, 7.5, footer, A4W - 160), { x: 40, y: 22, size: 7.5, font: R, color: gray });
    p.drawText(`${i + 1} / ${pages.length}`, { x: A4W - 70, y: 22, size: 7.5, font: R, color: gray });
  });
  return doc.save();
  });
}
const res = (r) => ({ O: "O", X: "X", U: "안 풂", P: "넘어감", T: "풀어 줌" }[r || ""] || "·");

export async function gradingPdf(d) {
  const nr = Math.max(1, ...d.rounds.map((r) => r.round));
  const head = ["번호", "정답", ...Array.from({ length: nr }, (_, k) => `${k + 1}차`), "최종", "학생 답", "유형", "정답률"];
  const rows = d.items.map((it) => {
    const by = Object.fromEntries((it.rounds || []).map((x) => [x.round, x.result === "O" && x.taught ? "T" : x.result]));
    return [it.label, it.answer, ...Array.from({ length: nr }, (_, k) => res(by[k + 1])), res(it.final), it.given, it.tag, it.rate];
  });
  const hasP = (d.summary.P || 0) > 0 || d.rounds.some((r) => r.summary.P);
  const rs = d.rounds.map((r) => [`${r.round}차`, r.kind === "solve" ? "처음 풀기" : "다시 풀기", r.summary.total, r.summary.O, r.summary.X, r.summary.U, ...(hasP ? [r.summary.P || 0] : []), r.summary.none, String(r.started_at || "").slice(0, 10)]);
  const s = d.summary;
  return report([
    { h1: `채점 결과 — ${d.title}` },
    { meta: `${d.student} · 코드 ${d.code} · 처음 채점 ${String(d.started || "").slice(0, 10)} · 스캔본 ${d.scans}개` },
    { box: `최종: 맞음 ${s.O}${s.T ? `(풀어 줌 ${s.T})` : ""} · 틀림 ${s.X} · 안 풂 ${s.U}${s.P ? ` · 넘어감 ${s.P}` : ""} · 안 매김 ${s.none} / ${s.total}문항` },
    ...(s.T ? [{ meta: "풀어 줌 = 선생님이 풀어 준 문제(번호에 박스) — 맞음으로 셈" }] : []),
    ...(s.P ? [{ meta: "넘어감 = 푼 만큼만 매기고 넘긴 문항(학습 계획상 풀지 않음 — 틀림 · 안 풂으로 세지 않음)" }] : []),
    { h2: "차수별" }, { table: { head: ["차", "종류", "문항", "맞음", "틀림", "안 풂", ...(hasP ? ["넘어감"] : []), "안 매김", "날짜"], rows: rs } },
    { h2: "문항별" }, { table: { head, rows, left: [head.length - 2] } },
  ], `${d.title} · ${d.code} · ${d.student}`);
}
export async function studentPdf(d) {
  const rows = d.gradings.map((g) => {
    const s = g.summary, s1 = g.rounds.length ? g.rounds[0].summary : s;
    const tot = (x) => x.total - (x.P || 0);                 // 넘어감(푼 만큼만 매기고 넘긴 문항)은 문항 수에서 뺌
    return [String(g.started || "").slice(0, 10), g.title, g.code, `${s1.O}/${tot(s1)}`, g.rounds.length, `${s.O}/${tot(s)}${s.P ? ` (넘어감 ${s.P})` : ""}`, s.X, s.U];
  });
  const wr = d.wrong_items.map((w) => [`${w.title || ""} ${w.code_fmt || ""}`, w.label, w.answer, (w.rounds || []).map((x) => `${x.round}차 ${x.result}`).join(" → "), res(w.final), w.tag]);
  const per = `${d.period.from || "처음"} ~ ${d.period.to || "오늘"}`;
  return report([
    { h1: `${d.student} 학습 기록` },
    { meta: `기간 ${per} · 채점 ${d.gradings.length}건 · 틀린 적 있는 문항 ${d.wrong_items.length}개` },
    { h2: "프린트별" }, { table: { head: ["날짜", "프린트", "코드", "1차 맞음", "차 수", "최종 맞음", "틀림", "안 풂"], rows: rows.length ? rows : [["채점 기록이 없어요", "", "", "", "", "", "", ""]], left: [1] } },
    { h2: "틀린 적 있는 문항" }, { table: { head: ["프린트", "번호", "정답", "차수별", "최종", "유형"], rows: wr.length ? wr : [["없어요", "", "", "", "", ""]], left: [0, 5] } },
  ], `${d.student} 학습 기록 · ${per}`);
}

// ── 이름 넣어 출력: 학생마다 이름 찍은 사본을 한 파일로 ("" 은 이름 없는 1부)
export async function stampNames(bytes, boxes, names, template, kind) {
  void kind;
  if (!names.some(Boolean)) {
    if (names.length <= 1) return bytes;
  }
  const P = await pdflib();
  const base = await P.PDFDocument.load(bytes, { ignoreEncryption: true, updateMetadata: false });
  const out = await P.PDFDocument.create();
  const fk = template === "문정중" ? "serifR" : String(template || "").startsWith("초등") ? "sansB" : "sansR";
  const font = await embedText(out, fk, names.join("") + "이름 ");
  const n = base.getPageCount();
  const idx = [...Array(n).keys()];
  for (const name of names) {
    const pages = await out.copyPages(base, idx);
    pages.forEach((p) => out.addPage(p));
    if (!name) continue;
    const targets = boxes && boxes.length ? boxes : [{ page: 0, corner: true }];
    for (const b of targets) {
      const pi = b.page || 0;
      if (pi >= n) continue;
      const page = pages[pi];
      const cb = page.getCropBox();
      const topY = (yy) => cb.y + cb.height - yy;
      if (b.corner) {
        page.drawText(`이름  ${name}`, { x: cb.x + 16, y: topY(14), size: 9, font, color: P.rgb(0.2, 0.2, 0.2) });
        continue;
      }
      const [x0, y0, x1, y1] = b.rect;
      let size = Number(b.size || 10.5);
      let w = font.widthOfTextAtSize(name, size);
      const room = Math.max(10, x1 - x0 - 6);
      if (w > room) { size = Math.max(6, (size * room) / w); w = font.widthOfTextAtSize(name, size); }
      const x = (b.align || "center") === "center" ? x0 + (x1 - x0 - w) / 2 : x0 + 6;
      const yb = (y0 + y1) / 2 + size * 0.36;
      page.drawText(name, { x: cb.x + x, y: topY(yb), size, font, color: P.rgb(0.05, 0.05, 0.05) });
    }
  }
  return out.save();
}

// ── 스캔본 여러 개 → 한 PDF (PDF는 쪽을 그대로, 사진은 A4 한 쪽씩)
export async function mergeScans(files) {
  const P = await pdflib();
  const out = await P.PDFDocument.create();
  for (const f of files) {
    const isPdf = /pdf/.test(f.mime || "") || /\.pdf$/i.test(f.name || "");
    try {
      if (isPdf) {
        const src = await P.PDFDocument.load(f.bytes, { ignoreEncryption: true });
        (await out.copyPages(src, src.getPageIndices())).forEach((p) => out.addPage(p));
        continue;
      }
      let img;
      if (/png/.test(f.mime || "") || /\.png$/i.test(f.name || "")) img = await out.embedPng(f.bytes);
      else if (/jpe?g/.test(f.mime || "") || /\.jpe?g$/i.test(f.name || "")) img = await out.embedJpg(f.bytes);
      else {
        const bmp = await createImageBitmap(new Blob([f.bytes], { type: f.mime || "" }));
        const c = canvas(bmp.width, bmp.height);
        c.getContext("2d").drawImage(bmp, 0, 0);
        img = await out.embedJpg(new Uint8Array(await (await toBlob(c, "image/jpeg", 0.9)).arrayBuffer()));
      }
      const land = img.width > img.height;
      const [pw, ph] = land ? [A4H, A4W] : [A4W, A4H];
      const s = Math.min((pw - 24) / img.width, (ph - 24) / img.height);
      const page = out.addPage([pw, ph]);
      page.drawImage(img, { x: (pw - img.width * s) / 2, y: (ph - img.height * s) / 2, width: img.width * s, height: img.height * s });
    } catch (e) {
      console.warn("스캔본 합치기 실패", f.name, e);
    }
  }
  if (!out.getPageCount()) throw new Error("합칠 스캔본이 없어요");
  return out.save();
}
