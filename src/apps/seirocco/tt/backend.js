// 시록고 강사도구 — 「서버」 자리. PC 강사도구 server.py 의 /api/* 를 브라우저에서 Supabase(tt_* · teacher-tool)로 옮김.
// 화면(ui.js)은 PC 때와 같은 모양의 응답을 받는다. PDF 일은 engine/ 이 브라우저 안에서 한다.
import { T, all, must, rpc, put, get, bytes, sign, remove, removePrefix, log, uid } from "./sb";
import {
  fmtCode, normCode, newCode, nowIso, todayStr, normName, summarize, currentMarks, roundMarks, roundsInfo, gradingStats,
  everWrong, autoJudge, guessLevel, safeName, cleanName, stripNames,
} from "./logic";

const engine = () => import("./engine/index.js");
const CLASS_KINDS = ["used", "graded", "reviewed", "homework"];

// ── 올린 파일(이 화면 안에서만 기억)
const UPLOADS = new Map();
let upSeq = 0;
export async function upload(file) {
  const id = "u" + ++upSeq + "_" + Date.now().toString(36);
  const name = cleanName(file.name);
  let pages = 0;
  if (/\.pdf$/i.test(name) || file.type === "application/pdf") {
    try { pages = await (await engine()).pageCount(new Uint8Array(await file.arrayBuffer())); } catch { pages = 0; }
  }
  UPLOADS.set(id, { file, name });
  return { id, name, size: file.size, pages };
}
const takeUpload = async (id) => {
  const u = UPLOADS.get(id);
  if (!u) throw new Error("올린 파일을 찾지 못했어요. 다시 올려 주세요");
  return { name: u.name, bytes: new Uint8Array(await u.file.arrayBuffer()), file: u.file };
};

// ── 공통 읽기
async function printRow(code) {
  const c = normCode(code);
  const rows = must(await T("tt_prints").select("*").eq("code", c).limit(1));
  return rows[0] || null;
}
async function studentsMap(ids) {
  const list = [...new Set(ids.filter(Boolean))];
  if (!list.length) return new Map();
  const rows = must(await T("tt_students").select("id,name,grade,active").in("id", list));
  return new Map(rows.map((r) => [r.id, r]));
}
function briefShape(p, targets, items) {
  const f = p.files || {};
  return {
    ...p, deleted: p.shelf === "deleted", code_fmt: fmtCode(p.code), sources: p.sources || [],
    pdf: f.sheet || null, answer_pdf: f.answer || null, extras: (f.extras || []).map((x) => ({ ...x, file: x.path })),
    targets, has_name_box: (p.name_boxes || []).length > 0,
    n_answers: items.filter((i) => (i.answer || "") !== "").length,
    n_answer_imgs: items.filter((i) => i.answer_png).length,
    n_sols: items.filter((i) => i.sol_png).length,
  };
}
async function printBriefs(prints) {
  if (!prints.length) return [];
  const ids = prints.map((p) => p.id);
  const tg = await all(() => T("tt_targets").select("print_id,student_id,issued_at").in("print_id", ids));
  const sm = await studentsMap(tg.map((t) => t.student_id));
  const items = await all(() => T("tt_print_items").select("print_id,answer,answer_png,sol_png").in("print_id", ids));
  return prints.map((p) => briefShape(p,
    tg.filter((t) => t.print_id === p.id).map((t) => ({ id: t.student_id, name: sm.get(t.student_id)?.name || "?", issued_at: t.issued_at }))
      .sort((a, b) => a.name.localeCompare(b.name, "ko")),
    items.filter((i) => i.print_id === p.id)));
}
async function printBrief(pid) {
  const p = must(await T("tt_prints").select("*").eq("id", pid).single());
  return (await printBriefs([p]))[0];
}
const ITEM_COLS = "seq,src,src_no,choice,hash,png,answer,label,points,topic,answer_png,sol_png,tag,rate,scale,origin,page,bbox";
async function itemsOf(pid) {
  return all(() => T("tt_print_items").select(ITEM_COLS).eq("print_id", pid).order("seq"));
}
async function marksOf(gids) {
  if (!gids.length) return [];
  return all(() => T("tt_marks").select("id,grading_id,session_no,seq,result,answer,at").in("grading_id", gids).order("id"));
}
async function sessionsOf(gids) {
  if (!gids.length) return [];
  return all(() => T("tt_sessions").select("*").in("grading_id", gids).order("no"));
}
async function scanList(gid) {
  const rows = must(await T("tt_scans").select("id,name,size,pages,mime,path,created_at").eq("grading_id", gid).eq("deleted", false).order("id"));
  return rows.map((r) => ({ ...r, kind: /pdf/.test(r.mime) || /\.pdf$/i.test(r.name) ? "pdf" : "image", pages: r.pages || 1 }));
}

// 학생의 다른 채점에서 같은 문항(해시)을 틀린 횟수 (어느 차든 X면 그 채점에서 1번)
async function wrongHistory(sid, hashes, excludeGid = null) {
  if (!hashes.size) return new Map();
  const gs = must(await T("tt_gradings").select("id,print_id").eq("student_id", sid));
  const others = gs.filter((g) => g.id !== excludeGid);
  if (!others.length) return new Map();
  const xs = await all(() => T("tt_marks").select("grading_id,seq").in("grading_id", others.map((g) => g.id)).eq("result", "X"));
  const items = await all(() => T("tt_print_items").select("print_id,seq,hash").in("print_id", [...new Set(others.map((g) => g.print_id))]));
  const hm = new Map(items.map((i) => [i.print_id + ":" + i.seq, i.hash]));
  const res = new Map();
  for (const g of others) {
    const seqs = new Set(xs.filter((m) => m.grading_id === g.id).map((m) => m.seq));
    for (const s of seqs) {
      const h = hm.get(g.print_id + ":" + s);
      if (h && hashes.has(h)) res.set(h, (res.get(h) || 0) + 1);
    }
  }
  return res;
}

export async function gradingDetail(gid) {
  const g = must(await T("tt_gradings").select("*").eq("id", gid).maybeSingle());
  if (!g) throw new Error("채점 기록이 없어요 (지웠을 수 있어요)");
  const [p, st, items, marks, sessions, scans] = await Promise.all([
    printBrief(g.print_id), T("tt_students").select("id,name").eq("id", g.student_id).single().then((r) => must(r)),
    itemsOf(g.print_id), marksOf([gid]), sessionsOf([gid]), scanList(gid)]);
  const cur = currentMarks(marks, sessions);
  const rm = roundMarks(marks, sessions);
  const hist = await wrongHistory(g.student_id, new Set(items.map((i) => i.hash).filter(Boolean)), gid);
  for (const it of items) {
    it.mark = cur.get(it.seq) || null;
    it.rounds = [...rm.keys()].sort((a, b) => a - b).filter((r) => rm.get(r).has(it.seq))
      .map((r) => ({ round: r, result: rm.get(r).get(it.seq).result, answer: rm.get(r).get(it.seq).answer }));
    it.wrong_before = hist.get(it.hash) || 0;
    it.repeat = it.wrong_before + (it.rounds.some((x) => x.result === "X") ? 1 : 0) >= 2;
  }
  const last = sessions[sessions.length - 1] || {};
  return {
    grading: g, print: p, student: st, items, sessions, rounds: roundsInfo(sessions, marks, items.map((i) => i.seq)),
    cur: { round: last.round || 1, kind: last.kind || "solve", targets: last.targets || null, no: last.no || 1 },
    summary: summarize(items), scans,
    retry_candidates: items.filter((i) => ["X", "U"].includes(i.mark?.result)).map((i) => i.seq),
  };
}

async function ensureStudents(names) {
  const ids = [];
  const want = [...new Set(names.map(normName).filter(Boolean))];
  if (!want.length) return ids;
  const have = must(await T("tt_students").select("id,name,active").in("name", want));
  const hm = new Map(have.map((r) => [r.name, r]));
  for (const n of want) {
    const r = hm.get(n);
    if (r) {
      ids.push(r.id);
      if (!r.active) await T("tt_students").update({ active: true }).eq("id", r.id);
    } else {
      const row = must(await T("tt_students").insert({ name: n }).select("id").single());
      ids.push(row.id);
      log("student_add", row.id, null, { name: n });
    }
  }
  return ids;
}
export async function knownNames() {
  const rows = await all(() => T("tt_students").select("name"));
  return rows.map((r) => r.name);
}

async function studentDetail(sid) {
  const st = must(await T("tt_students").select("*").eq("id", sid).maybeSingle());
  if (!st) throw new Error("그런 학생이 없어요");
  const tg = must(await T("tt_targets").select("print_id,issued_at").eq("student_id", sid).order("issued_at", { ascending: false }));
  const pids = tg.map((t) => t.print_id);
  const prints = pids.length ? must(await T("tt_prints").select("id,code,title,n_items,shelf").in("id", pids)) : [];
  const pm = new Map(prints.map((p) => [p.id, p]));
  const gs = must(await T("tt_gradings").select("id,print_id,status").eq("student_id", sid));
  const gids = gs.map((g) => g.id);
  const [marks, sessions] = await Promise.all([marksOf(gids), sessionsOf(gids)]);
  const scans = gids.length ? await all(() => T("tt_scans").select("grading_id").in("grading_id", gids).eq("deleted", false)) : [];
  const out = [];
  for (const t of tg) {
    const p = pm.get(t.print_id);
    if (!p || p.shelf !== "active") continue;
    const row = { id: p.id, code: p.code, code_fmt: fmtCode(p.code), title: p.title, n_items: p.n_items, issued_at: t.issued_at, grading: null };
    const g = gs.find((x) => x.print_id === p.id);
    if (g) {
      row.grading = { id: g.id, status: g.status };
      Object.assign(row, gradingStats(marks.filter((m) => m.grading_id === g.id), sessions.filter((s) => s.grading_id === g.id), p.n_items));
      row.n_scans = scans.filter((s) => s.grading_id === g.id).length;
    }
    out.push(row);
  }
  // 반복 오답: 같은 문항(해시)을 두 번 넘게(채점마다 1번, 어느 차든 X) 틀린 것
  const allPids = [...new Set(gs.map((g) => g.print_id))];
  const items = allPids.length ? await all(() => T("tt_print_items").select("print_id,seq,hash,png").in("print_id", allPids)) : [];
  const allPrints = allPids.length ? must(await T("tt_prints").select("id,code,title,shelf").in("id", allPids)) : [];
  const apm = new Map(allPrints.map((p) => [p.id, p]));
  const wrong = new Map();
  for (const g of gs) {
    const p = apm.get(g.print_id);
    if (!p || p.shelf === "deleted") continue;
    for (const seq of [...everWrong(marks.filter((m) => m.grading_id === g.id))].sort((a, b) => a - b)) {
      const it = items.find((i) => i.print_id === g.print_id && i.seq === seq);
      if (!it || !it.hash) continue;
      if (!wrong.has(it.hash)) wrong.set(it.hash, { hash: it.hash, count: 0, png: it.png ? `${p.code}/${it.png}` : null, where: [] });
      const w = wrong.get(it.hash);
      w.count += 1;
      w.where.push({ code: fmtCode(p.code), title: p.title, seq });
    }
  }
  const rep = [...wrong.values()].filter((w) => w.count >= 2).sort((a, b) => b.count - a.count);
  const recs = must(await T("tt_class_records").select("day,kind,print_id").eq("student_id", sid).order("day", { ascending: false }));
  const records = recs.map((r) => ({ date: r.day, kind: r.kind, code: apm.get(r.print_id)?.code || pm.get(r.print_id)?.code || "", title: apm.get(r.print_id)?.title || pm.get(r.print_id)?.title || "" }));
  return { student: st, prints: out, repeat_wrong: rep, records };
}

async function gradingsList(q) {
  let qq = () => {
    let x = T("tt_gradings").select("id,status,updated_at,print_id,student_id").order("updated_at", { ascending: false }).limit(100);
    if (q.status === "unfinished") x = x.neq("status", "done");
    if (q.student) x = x.eq("student_id", Number(q.student));
    return x;
  };
  const gs = must(await qq());
  if (!gs.length) return [];
  const prints = must(await T("tt_prints").select("id,code,title,n_items,shelf").in("id", [...new Set(gs.map((g) => g.print_id))]));
  const pm = new Map(prints.map((p) => [p.id, p]));
  const sm = await studentsMap(gs.map((g) => g.student_id));
  const gids = gs.map((g) => g.id);
  const [marks, sessions] = await Promise.all([marksOf(gids), sessionsOf(gids)]);
  return gs.filter((g) => pm.get(g.print_id)?.shelf === "active").map((g) => {
    const p = pm.get(g.print_id);
    return { ...g, name: sm.get(g.student_id)?.name || "?", code: p.code, code_fmt: fmtCode(p.code), title: p.title, n_items: p.n_items,
             ...gradingStats(marks.filter((m) => m.grading_id === g.id), sessions.filter((s) => s.grading_id === g.id), p.n_items) };
  });
}

async function classView(date, sids, days) {
  const d0 = new Date(new Date(date + "T00:00:00").getTime() - days * 86400000);
  const from = `${d0.getFullYear()}-${String(d0.getMonth() + 1).padStart(2, "0")}-${String(d0.getDate()).padStart(2, "0")}`;
  const out = [];
  const sm = await studentsMap(sids);
  for (const sid of sids) {
    const st = sm.get(sid);
    if (!st) continue;
    const tg = must(await T("tt_targets").select("print_id,issued_at").eq("student_id", sid)
      .gte("issued_at", from + "T00:00:00").lte("issued_at", date + "T23:59:59.999").order("issued_at", { ascending: false }));
    const prints = tg.length ? must(await T("tt_prints").select("id,code,title,n_items,shelf").in("id", tg.map((t) => t.print_id))) : [];
    const pm = new Map(prints.map((p) => [p.id, p]));
    const gs = tg.length ? must(await T("tt_gradings").select("id,print_id,status").eq("student_id", sid).in("print_id", tg.map((t) => t.print_id))) : [];
    const marks = await marksOf(gs.map((g) => g.id));
    const sessions = await sessionsOf(gs.map((g) => g.id));
    const issued = [];
    for (const t of tg) {
      const p = pm.get(t.print_id);
      if (!p || p.shelf !== "active") continue;
      const d = new Date(t.issued_at);
      const row = { id: p.id, code: p.code, code_fmt: fmtCode(p.code), title: p.title, n_items: p.n_items,
                    issued: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`, grading: null };
      const g = gs.find((x) => x.print_id === p.id);
      if (g) {
        row.grading = { id: g.id, status: g.status };
        row.summary = summarize([...currentMarks(marks.filter((m) => m.grading_id === g.id), sessions.filter((s) => s.grading_id === g.id)).values()].map((m) => ({ mark: m })));
      }
      issued.push(row);
    }
    const recs = must(await T("tt_class_records").select("kind,print_id,created_at").eq("day", date).eq("student_id", sid));
    const records = Object.fromEntries(CLASS_KINDS.map((k) => [k, recs.filter((r) => r.kind === k).map((r) => r.print_id)]));
    const saved = Object.fromEntries(CLASS_KINDS.map((k) => [k, recs.some((r) => r.kind === k)]));
    out.push({ student: { id: st.id, name: st.name }, today: issued.filter((p) => p.issued === date), recent: issued, records, saved });
  }
  return out;
}
async function classSave(date, sid, kind, pids) {
  if (!CLASS_KINDS.includes(kind)) throw new Error("kind");
  const old = must(await T("tt_class_records").select("print_id").eq("day", date).eq("student_id", sid).eq("kind", kind)).map((r) => r.print_id);
  const want = new Set(pids.map(Number));
  const gone = old.filter((x) => !want.has(x));
  if (gone.length) must(await T("tt_class_records").delete().eq("day", date).eq("student_id", sid).eq("kind", kind).in("print_id", gone));
  const add = [...want].filter((x) => !old.includes(x)).map((pid) => ({ day: date, student_id: sid, kind, print_id: pid }));
  if (add.length) must(await T("tt_class_records").insert(add));
  log("class_" + kind, sid, null, { date, prints: [...want].sort(), edited: old.length > 0 });
}

// ── 오답 후보 (PC wrong_candidates)
async function transcriptsOf(keys) {
  if (!keys.length) return new Map();
  const rows = await all(() => T("tt_transcripts").select("item_key,question,solution").in("item_key", keys));
  return new Map(rows.filter((r) => r.question || r.solution).map((r) => [r.item_key, r]));
}
const itemKey = (code, it) => it.hash || `${code}:${it.seq}`;
export async function wrongCandidates(f) {
  const sids = (f.students || []).map(Number).filter(Boolean);
  const codes = (f.codes || []).map(normCode).filter((c) => c.length === 6);
  const which = ["final", "ever", "repeat"].includes(f.which) ? f.which : "final";
  const withU = !!f.include_u;
  let gq = T("tt_gradings").select("id,student_id,print_id,created_at").order("created_at").order("id");
  if (sids.length) gq = gq.in("student_id", sids);
  if (f.from) gq = gq.gte("created_at", f.from + "T00:00:00");
  if (f.to) gq = gq.lte("created_at", f.to + "T23:59:59.999");
  let gs = must(await gq.limit(1000));
  const prints = gs.length ? must(await T("tt_prints").select("id,code,title,kind,level,shelf").in("id", [...new Set(gs.map((g) => g.print_id))])) : [];
  const pm = new Map(prints.map((p) => [p.id, p]));
  gs = gs.filter((g) => pm.get(g.print_id)?.shelf === "active" && (!codes.length || codes.includes(pm.get(g.print_id).code)));
  const sm = await studentsMap(gs.map((g) => g.student_id));
  const gids = gs.map((g) => g.id);
  const [marks, sessions] = await Promise.all([marksOf(gids), sessionsOf(gids)]);
  const items = gs.length ? await all(() => T("tt_print_items").select(ITEM_COLS + ",print_id").in("print_id", [...new Set(gs.map((g) => g.print_id))]).order("seq")) : [];
  let hist = new Map();
  if (which === "repeat") {
    for (const sid of new Set(gs.map((g) => g.student_id))) {
      const hs = new Set(items.filter((i) => i.hash).map((i) => i.hash));
      hist.set(sid, await wrongHistory(sid, hs, null));
    }
  }
  const out = new Map(), order = [];
  for (const g of gs) {
    const p = pm.get(g.print_id);
    const gm = marks.filter((m) => m.grading_id === g.id), gsn = sessions.filter((s) => s.grading_id === g.id);
    const cur = currentMarks(gm, gsn), rm = roundMarks(gm, gsn);
    for (const it of items.filter((i) => i.print_id === g.print_id)) {
      const m = cur.get(it.seq) || {};
      const fin = m.result || "";
      const seqR = [...rm.keys()].sort((a, b) => a - b).filter((r) => rm.get(r).has(it.seq)).map((r) => ({ round: r, result: rm.get(r).get(it.seq).result }));
      const ever = seqR.some((x) => x.result === "X");
      const hit = which === "final" ? fin === "X" || (withU && fin === "U")
        : which === "ever" ? ever || (withU && fin === "U")
        : !!it.hash && (hist.get(g.student_id)?.get(it.hash) || 0) >= 2;
      if (!hit) continue;
      const key = itemKey(p.code, it);
      if (!out.has(key)) {
        out.set(key, { key, code: p.code, code_fmt: fmtCode(p.code), title: p.title, level: p.level || "", kind: p.kind,
          seq: it.seq, label: it.label || String(it.src_no || it.seq), png: it.png ? `${p.code}/${it.png}` : null,
          answer: it.answer || "", answer_png: it.answer_png ? `${p.code}/${it.answer_png}` : null, sol_png: it.sol_png ? `${p.code}/${it.sol_png}` : null,
          choice: !!it.choice, points: it.points, topic: it.topic || "", tag: it.tag || "", rate: it.rate || "", scale: it.scale,
          students: [], n_wrong: 0 });
        order.push(key);
      }
      const e = out.get(key);
      e.students.push({ id: g.student_id, name: sm.get(g.student_id)?.name || "?", final: fin, rounds: seqR, answer: m.answer || "", when: (g.created_at || "").slice(0, 10) });
      e.n_wrong += seqR.filter((x) => x.result === "X").length;
    }
  }
  const tr = await transcriptsOf(order);
  for (const k of order) {
    const t = tr.get(k);
    if (t) Object.assign(out.get(k), { question: t.question, solution: t.solution });
  }
  return { items: order.map((k) => out.get(k)), n_gradings: gs.length,
    filter: { students: sids, codes: codes.map(fmtCode), from: f.from || "", to: f.to || "", which, include_u: withU } };
}

// ── 받기용 JSON (PC print_data · grading_data · student_data)
const CIRC_ANS = { 1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤" };
const RES_KO = { O: "맞음", X: "틀림", U: "안 풂", "": "안 매김" };
const ansText = (it) => { const a = String(it.answer || ""); return (it.choice ? CIRC_ANS[a] || a : a) || (it.answer_png ? "(그림)" : ""); };

export async function printData(code) {
  const pr = await printRow(code);
  if (!pr) return null;
  const p = await printBrief(pr.id);
  const items = await itemsOf(pr.id);
  const gs = must(await T("tt_gradings").select("id").eq("print_id", pr.id));
  const marks = await marksOf(gs.map((g) => g.id)), sessions = await sessionsOf(gs.map((g) => g.id));
  const curs = gs.map((g) => currentMarks(marks.filter((m) => m.grading_id === g.id), sessions.filter((s) => s.grading_id === g.id)));
  const tr = await transcriptsOf(items.map((it) => itemKey(pr.code, it)));
  return {
    kind: "ashrain.print.data", version: 1, made: nowIso(), code: p.code_fmt, title: p.title, sub: p.sub || "", level: p.level || "",
    print_kind: p.kind || "", n_items: items.length, students_graded: gs.length,
    note: "문항 그림은 같은 코드의 시험지 PDF에 같은 번호로 있다. question/solution은 강사도구에 전사본이 있을 때만(mathir).",
    items: items.map((it) => {
      const res = curs.map((c) => c.get(it.seq)?.result || "");
      const key = itemKey(pr.code, it), t = tr.get(key);
      return { no: it.seq, label: it.label || String(it.src_no || it.seq), choice: !!it.choice, answer: ansText(it), points: it.points,
        topic: it.topic || "", tag: it.tag || "", rate: it.rate || "", key, origin: it.origin || null,
        image: it.png ? `시험지 ${it.seq}번` : null, answer_image: !!it.answer_png, solution_image: !!it.sol_png,
        results: { graded: res.filter(Boolean).length, O: res.filter((x) => x === "O").length, X: res.filter((x) => x === "X").length, U: res.filter((x) => x === "U").length },
        ...(t ? { question: t.question, solution: t.solution } : {}) };
    }),
  };
}
export async function gradingData(gid) {
  const d = await gradingDetail(gid);
  const p = d.print;
  const wrongKeys = d.items.filter((it) => ["X", "U"].includes(it.mark?.result)).map((it) => itemKey(p.code, it));
  const tr = await transcriptsOf(wrongKeys);
  return {
    kind: "ashrain.grading", version: 1, made: nowIso(), student: d.student.name, code: p.code_fmt, title: p.title,
    status: d.grading.status, started: d.grading.created_at, updated: d.grading.updated_at,
    rounds: d.rounds.map((r) => ({ round: r.round, kind: r.kind, targets: r.targets, sessions: r.sessions, started_at: r.started_at, ended_at: r.ended_at, summary: r.summary })),
    summary: d.summary, scans: d.scans.length,
    items: d.items.map((it) => {
      const m = it.mark || {};
      const key = itemKey(p.code, it), t = ["X", "U"].includes(m.result) ? tr.get(key) : null;
      return { no: it.seq, label: it.label || String(it.src_no || it.seq), choice: !!it.choice, answer: ansText(it), final: m.result || "",
        final_ko: RES_KO[m.result || ""], given: m.answer || "", rounds: it.rounds, repeat_wrong: !!it.repeat, wrong_before: it.wrong_before || 0,
        tag: it.tag || it.topic || "", rate: it.rate || "", key, ...(t ? { question: t.question, solution: t.solution } : {}) };
    }),
  };
}
export async function studentData(sid, f = {}) {
  const st = must(await T("tt_students").select("id,name,grade,memo").eq("id", sid).maybeSingle());
  if (!st) return null;
  let q = T("tt_gradings").select("id,print_id,created_at").eq("student_id", sid).order("created_at");
  if (f.from) q = q.gte("created_at", f.from + "T00:00:00");
  if (f.to) q = q.lte("created_at", f.to + "T23:59:59.999");
  const gs = must(await q);
  const prints = gs.length ? must(await T("tt_prints").select("id,shelf").in("id", gs.map((g) => g.print_id))) : [];
  const ok = new Set(prints.filter((p) => p.shelf === "active").map((p) => p.id));
  const gr = [];
  for (const g of gs.filter((g) => ok.has(g.print_id))) {
    const d = await gradingData(g.id);
    delete d.student; delete d.kind; delete d.version; delete d.made;
    gr.push(d);
  }
  const wr = (await wrongCandidates({ students: [sid], from: f.from, to: f.to, which: "ever" })).items;
  return {
    kind: "ashrain.student", version: 1, made: nowIso(), student: st.name, grade: st.grade || "", period: { from: f.from || "", to: f.to || "" },
    gradings: gr,
    wrong_items: wr.map((w) => {
      const o = {};
      for (const k of ["code_fmt", "title", "seq", "label", "answer", "choice", "tag", "rate", "key", "question", "solution", "n_wrong"]) if (w[k] !== undefined && w[k] !== "" && w[k] !== null) o[k] = w[k];
      o.final = w.students[0].final; o.rounds = w.students[0].rounds;
      return o;
    }),
  };
}

// ── 프린트 지우기·되살리기
async function purgePrint(pid) {
  const r = await rpc("tt_purge_print", { p_print: pid });
  try { await remove(r.paths || []); await removePrefix(r.code + "/"); } catch { /* 파일 지우기는 다음에 다시 */ }
  return { ok: true, gradings: r.gradings };
}

// ── 라우터 (PC /api/* 와 같은 경로·모양)
export async function api(path, body) {
  const [p, qs] = String(path).split("?");
  const q = Object.fromEntries(new URLSearchParams(qs || ""));
  const post = body !== undefined;
  let m;
  if (p === "ping") return { ok: true, version: "web-2026-11" };
  if (p === "settings") {
    if (post) { localStorage.setItem("tt:defaults", JSON.stringify(body.defaults || {})); return { ok: true }; }
    let d = {};
    try { d = JSON.parse(localStorage.getItem("tt:defaults") || "{}"); } catch { d = {}; }
    return { defaults: d, today: todayStr() };
  }
  if (p === "students") {
    if (post) return { ids: await ensureStudents(body.names || []) };
    const sts = must(await T("tt_students").select("*").order("active", { ascending: false }).order("name"));
    const tg = await all(() => T("tt_targets").select("student_id,issued_at"));
    return sts.map((s) => {
      const mine = tg.filter((t) => t.student_id === s.id);
      return { ...s, n_prints: mine.length, last_issued: mine.map((t) => t.issued_at).sort().pop() || null };
    });
  }
  if ((m = /^students\/(\d+)$/.exec(p))) {
    const sid = Number(m[1]);
    if (!post) return studentDetail(sid);
    const f = {};
    for (const k of ["name", "grade", "memo", "active"]) if (k in body) f[k] = k === "name" ? normName(body[k]) : body[k];
    if (Object.keys(f).length) {
      must(await T("tt_students").update({ ...f, updated_at: nowIso() }).eq("id", sid));
      log("student_edit", sid, null, f);
    }
    return { ok: true };
  }
  if (p === "prints" && !post) {
    let x = T("tt_prints").select("*").eq("shelf", q.deleted === "1" ? "deleted" : q.shelf === "library" ? "library" : "active").order("id", { ascending: false }).limit(300);
    if (q.q) {
      const s = q.q.replace(/[%,()]/g, " ").trim();
      const c = normCode(s);
      x = x.or(`title.ilike.%${s}%,code.ilike.%${c || s}%,sub.ilike.%${s}%`);
    }
    let prints = must(await x);
    if (q.student) {
      const tg = must(await T("tt_targets").select("print_id").eq("student_id", Number(q.student)));
      const ids = new Set(tg.map((t) => t.print_id));
      prints = prints.filter((pr) => ids.has(pr.id));
    }
    return printBriefs(prints);
  }
  if ((m = /^prints\/([A-Za-z0-9-]+)\/(restore|purge|unshelve)$/.exec(p))) {
    const pr = await printRow(m[1]);
    if (!pr) throw new Error("그런 코드의 프린트가 없어요");
    if (m[2] === "purge") return purgePrint(pr.id);
    must(await T("tt_prints").update({ shelf: "active", updated_at: nowIso() }).eq("id", pr.id));
    log(m[2] === "restore" ? "print_restore" : "library_register", null, pr.id, { code: pr.code });
    return { ok: true };
  }
  if ((m = /^prints\/([A-Za-z0-9-]+)$/.exec(p))) {
    const pr = await printRow(m[1]);
    if (!pr || (!post && pr.shelf !== "active")) throw new Error("그런 코드의 프린트가 없어요");
    if (!post) {
      const d = await printBrief(pr.id);
      d.items = await itemsOf(pr.id);
      const gs = must(await T("tt_gradings").select("id,status,updated_at,student_id").eq("print_id", pr.id).order("id", { ascending: false }));
      const sm = await studentsMap(gs.map((g) => g.student_id));
      const marks = await marksOf(gs.map((g) => g.id)), sessions = await sessionsOf(gs.map((g) => g.id));
      d.gradings = gs.map((g) => ({ ...g, name: sm.get(g.student_id)?.name || "?",
        ...gradingStats(marks.filter((x) => x.grading_id === g.id), sessions.filter((x) => x.grading_id === g.id), d.n_items) }));
      d.answer_pages = d.answer_pdf ? await pagesOf(d.answer_pdf, pr.files?.answer_pages) : [];
      d.sheet_pages = d.items.some((it) => !it.png) && d.pdf ? await pagesOf(d.pdf, pr.pages) : [];
      return d;
    }
    const up = { updated_at: nowIso() };
    if ("title" in body) up.title = String(body.title || "").trim();
    if (["초등", "중등", "고등"].includes(body.level)) up.level = body.level;
    if (Object.keys(up).length > 1) must(await T("tt_prints").update(up).eq("id", pr.id));
    if (body.answers) {
      for (const [seq, a] of Object.entries(body.answers)) must(await T("tt_print_items").update({ answer: String(a || "").trim() }).eq("print_id", pr.id).eq("seq", Number(seq)));
      log("answers_edit", null, pr.id, { n: Object.keys(body.answers).length });
    }
    if (body.targets) {
      const sids = await ensureStudents(body.targets);
      if (sids.length) must(await T("tt_targets").upsert(sids.map((s) => ({ print_id: pr.id, student_id: s })), { onConflict: "print_id,student_id", ignoreDuplicates: true }));
      log("targets_add", null, pr.id, { students: sids });
    }
    if (body.remove_target) must(await T("tt_targets").delete().eq("print_id", pr.id).eq("student_id", Number(body.remove_target)));
    if (body.delete) {
      if (body.purge) return purgePrint(pr.id);
      must(await T("tt_prints").update({ shelf: "deleted", updated_at: nowIso() }).eq("id", pr.id));
      log("print_delete", null, pr.id, { code: pr.code });
    }
    const res = { ok: true };
    if (body.answer_upload) res.quick = await (await engine()).attachAnswer(pr, await takeUpload(body.answer_upload), ctx());
    return res;
  }
  if (p === "gradings" && !post) return gradingsList(q);
  if (p === "gradings" && post) {
    const pr = await printRow(body.code);
    if (!pr || pr.shelf !== "active") throw new Error("그런 코드의 프린트가 없어요");
    let sid = body.student_id;
    if (!sid && body.student_name) sid = (await ensureStudents([body.student_name]))[0];
    if (!sid) throw new Error("학생을 골라 주세요");
    const gid = await rpc("tt_open_grading", { p_print: pr.id, p_student: Number(sid), p_purpose: body.purpose || null });
    return gradingDetail(gid);
  }
  if ((m = /^gradings\/(\d+)$/.exec(p))) return gradingDetail(Number(m[1]));
  if ((m = /^gradings\/(\d+)\/scans$/.exec(p))) return scanList(Number(m[1]));
  if ((m = /^gradings\/(\d+)\/delete$/.exec(p))) {
    const r = await rpc("tt_delete_grading", { p_grading: Number(m[1]), p_scope: body.scope || "all" });
    if (r.paths?.length) { try { await remove(r.paths); } catch { /* 다음에 */ } }
    return r;
  }
  if ((m = /^gradings\/(\d+)\/mark$/.exec(p))) {
    const gid = Number(m[1]);
    let result = body.result;
    if (result === "auto") {
      const g = must(await T("tt_gradings").select("print_id").eq("id", gid).single());
      const it = must(await T("tt_print_items").select("answer").eq("print_id", g.print_id).eq("seq", Number(body.seq)).single());
      result = autoJudge(it.answer, body.answer);
      if (!result) return gradingDetail(gid);
    }
    if (!["O", "X", "U", ""].includes(result)) throw new Error("result");
    await rpc("tt_mark", { p_grading: gid, p_seq: Number(body.seq), p_result: result, p_answer: body.answer || "" });
    if (body.mode) await T("tt_gradings").update({ mode: body.mode }).eq("id", gid);
    if (body.light) return { ok: true };            // 화면이 먼저 적어 두고 차례로 보내는 경우 — 다 보낸 뒤 한 번만 다시 읽는다
    return gradingDetail(gid);
  }
  if ((m = /^gradings\/(\d+)\/close$/.exec(p))) {
    const st = await rpc("tt_close_grading", { p_grading: Number(m[1]), p_reason: body.reason || "done", p_untouched: !!body.untouched });
    return { status: st };
  }
  if ((m = /^scans\/(\d+)$/.exec(p)) && post && body.delete) {
    const r = must(await T("tt_scans").select("*").eq("id", Number(m[1])).maybeSingle());
    if (!r) throw new Error("없음");
    must(await T("tt_scans").update({ deleted: true }).eq("id", r.id));
    try { await remove([r.path]); } catch { /* 다음에 */ }
    const g = must(await T("tt_gradings").select("student_id,print_id").eq("id", r.grading_id).single());
    log("scan_delete", g.student_id, g.print_id, { grading: r.grading_id, name: r.name });
    return { scans: await scanList(r.grading_id) };
  }
  if (p === "class") {
    if (post) { await classSave(body.date, Number(body.student_id), body.kind, body.print_ids || []); return { ok: true }; }
    return classView(q.date || todayStr(), (q.students || "").split(",").filter((x) => /^\d+$/.test(x)).map(Number), Number(q.days || 7));
  }
  if (p === "events") {
    const lim = Math.min(Number(q.limit || 200), 2000);
    const ev = must(await T("tt_events").select("*").order("id", { ascending: false }).limit(lim));
    const sm = await studentsMap(ev.map((e) => e.student_id));
    const pids = [...new Set(ev.map((e) => e.print_id).filter(Boolean))];
    const prints = pids.length ? must(await T("tt_prints").select("id,code,title").in("id", pids)) : [];
    const pm = new Map(prints.map((x) => [x.id, x]));
    return ev.map((e) => ({ ...e, student: sm.get(e.student_id)?.name || null, code: pm.get(e.print_id)?.code || null, title: pm.get(e.print_id)?.title || null }));
  }
  if (p === "event" && post) { log("ui_" + String(body.kind || "x").replace(/[^a-z_]/g, "").slice(0, 30), body.student_id, body.print_id, body.detail || {}); return { ok: true }; }
  if (p === "wrongset/preview") return wrongCandidates(body || {});
  if (p === "wrongset/make") return (await engine()).wrongMake(body, ctx());
  if (p === "convert") return (await engine()).convert(body, ctx());
  if (p === "register/analyze") return (await engine()).registerAnalyze(body, ctx());
  if (p === "register/commit") return (await engine()).registerCommit(body, ctx());
  if (p === "library") return libraryIndex();
  if (p === "library/register") return libraryRegister(body.code);
  if (p === "export/prints") return (await engine()).exportPrints(q, ctx());
  if (p === "export/transcribe") return (await engine()).exportTranscribe(body, ctx());
  if (p === "export/analysis") return (await engine()).exportAnalysis(body, ctx());
  if (p === "export/import") return (await engine()).importTranscripts(body, ctx());
  if (p === "inbox") return [];
  throw new Error("없는 요청: " + p);
}

// ── 보관함 (= shelf 'library' 인 프린트 — 옮겨 오기로 들어온 Claude 프린트 원본)
async function libraryIndex() {
  const rows = must(await T("tt_prints").select("id,code,title,sub,level,options,created_at,shelf,files,n_items").in("shelf", ["library", "active", "deleted"]).order("created_at", { ascending: false }).limit(2000));
  const lib = rows.filter((r) => r.shelf === "library" || (r.options && r.options.library));
  return { updated: lib[0]?.created_at || null, prints: lib.map((r) => ({
    code: r.code, code_fmt: fmtCode(r.code), title: r.title, sub: r.sub, level: r.level, grade: r.options?.library?.grade || "",
    made: r.options?.library?.made || (r.created_at || "").slice(0, 10), for: r.options?.library?.for || [],
    roles: (r.options?.library?.roles || []), n_files: (r.options?.library?.roles || []).length,
    registered: r.shelf === "active", deleted: r.shelf === "deleted" })) };
}
async function libraryRegister(code) {
  const pr = await printRow(code);
  if (!pr) throw new Error(`보관함에 ${fmtCode(normCode(code))} 코드가 없어요`);
  if (pr.shelf === "active") throw new Error("이미 등록한 코드예요");
  if (pr.shelf === "deleted") throw new Error("지운 프린트 목록에 같은 코드가 있어요. 프린트함 → 「지운 프린트」에서 되살리세요.");
  // 옮겨 오기 때 이미 문항을 나눠 두었으면 바로 꺼내고, 아니면 등록 확인 화면으로
  const items = must(await T("tt_print_items").select("seq").eq("print_id", pr.id).limit(1));
  if (items.length) {
    must(await T("tt_prints").update({ shelf: "active", updated_at: nowIso() }).eq("id", pr.id));
    log("library_register", null, pr.id, { code: pr.code });
    return { done: true, print: await printBrief(pr.id) };
  }
  return (await engine()).libraryDraft(pr, ctx());
}

// 쪽 그림 (정답해설 보기 · 쪽 단위 시험지) — 「@page:<pdf rel>:<쪽>」 를 화면이 그림으로 바꿈
async function pagesOf(pdfRel, n) {
  let count = Number(n) || 0;
  if (!count) {
    try { count = await (await engine()).pageCount(await bytes(pdfRel)); } catch { count = 0; }
  }
  return Array.from({ length: count }, (_, i) => `@page:${pdfRel}:${i + 1}`);
}

// 엔진에 넘기는 손잡이
function ctx() {
  return { T, all, must, rpc, put, get, bytes, sign, remove, log, uid, takeUpload, ensureStudents, knownNames, printBrief, printRow, itemsOf, gradingDetail,
    wrongCandidates, printData, gradingData, studentData, newCode, normCode, fmtCode, guessLevel, safeName, cleanName, stripNames, nowIso, todayStr };
}

// ── 화면 주소 풀기: 저장 공간 파일 → 서명 주소, 「@page:」 → 그린 그림
const pageCache = new Map();
export async function resolve(rels) {
  const out = {};
  const drafts = rels.filter((r) => r.startsWith("_draft/"));
  if (drafts.length) { const E = await engine(); for (const r of drafts) { const u = E.draftUrl(r); if (u) out[r] = u; } }
  const files = rels.filter((r) => !r.startsWith("@page:") && !r.startsWith("_draft/"));
  if (files.length) Object.assign(out, await sign(files));
  for (const r of rels.filter((x) => x.startsWith("@page:"))) {
    if (!pageCache.has(r)) {
      const [, pdf, no] = /^@page:(.+):(\d+)$/.exec(r) || [];
      pageCache.set(r, (async () => {
        const blob = await (await engine()).renderPagePng(await bytes(pdf), Number(no), 2);
        return URL.createObjectURL(blob);
      })());
    }
    try { out[r] = await pageCache.get(r); } catch { pageCache.delete(r); }
  }
  return out;
}

// ── /dl · /out · /scan 주소 (PC가 내려 주던 것) → 브라우저에서 만들어 열거나 받기
export async function link(href) {
  const u = new URL(href, location.origin);
  const q = Object.fromEntries(u.searchParams);
  let m;
  if ((m = /^\/dl\/(print|grading|student)\/([A-Za-z0-9-]+)\.(json|pdf)$/.exec(u.pathname))) {
    const [, what, key, ext] = m;
    const f = { from: q.from || "", to: q.to || "" };
    if (ext === "json") {
      if (what === "print") { const d = await printData(key); return { json: d, name: `${safeName(d.title)}_${d.code}_문항.json` }; }
      if (what === "grading") { const d = await gradingData(Number(key)); return { json: d, name: `${d.student}_${safeName(d.title)}_${d.code}_채점결과.json` }; }
      const d = await studentData(Number(key), f);
      return { json: d, name: `${d.student}_학습기록_${todayStr()}.json` };
    }
    const E = await engine();
    if (what === "grading") { const d = await gradingData(Number(key)); return { pdf: await E.gradingPdf(d), name: `${d.student}_${safeName(d.title)}_${d.code}_채점결과.pdf`, view: q.view === "1" }; }
    const d = await studentData(Number(key), f);
    return { pdf: await E.studentPdf(d), name: `${d.student}_학습기록_${todayStr()}.pdf`, view: q.view === "1" };
  }
  if ((m = /^\/out\/([A-Za-z0-9-]+)\/sheet\.pdf$/.exec(u.pathname))) {
    const pr = await printRow(m[1]);
    if (!pr) throw new Error("그런 코드의 프린트가 없어요");
    const sids = (q.sid || "").split(",").filter((x) => /^\d+$/.test(x)).map(Number);
    const sm = await studentsMap(sids);
    const names = sids.map((s) => sm.get(s)?.name).filter(Boolean);
    if (q.blank === "1" || !names.length) names.unshift("");
    const E = await engine();
    const out = await E.stampNames(await bytes(pr.files.sheet), pr.name_boxes || [], names, pr.template, pr.kind);
    if (sids.length && q.record !== "0") {
      must(await T("tt_targets").upsert(sids.map((s) => ({ print_id: pr.id, student_id: s })), { onConflict: "print_id,student_id", ignoreDuplicates: true }));
      log("print_out", null, pr.id, { students: sids, blank: q.blank === "1" });
    }
    return { pdf: out, name: `${safeName(pr.title)}_${fmtCode(pr.code)}${names.filter(Boolean).length === 1 ? "_" + names.filter(Boolean)[0] : ""}.pdf`, view: true };
  }
  if ((m = /^\/scan\/all\/(\d+)\.pdf$/.exec(u.pathname))) {
    const scans = await scanList(Number(m[1]));
    const files = await Promise.all(scans.map(async (s) => ({ name: s.name, mime: s.mime, bytes: await bytes(s.path) })));
    const E = await engine();
    return { pdf: await E.mergeScans(files), name: `스캔본_${m[1]}.pdf`, view: q.dl !== "1" };
  }
  if ((m = /^\/scan\/(\d+)$/.exec(u.pathname))) {
    const r = must(await T("tt_scans").select("*").eq("id", Number(m[1])).single());
    const url = (await sign([r.path]))[r.path];
    return { url, name: r.name, view: q.dl !== "1" };
  }
  throw new Error("없는 주소: " + u.pathname);
}

// 스캔본 올리기
export async function uploadScan(gid, file) {
  const g = must(await T("tt_gradings").select("id,print_id,student_id").eq("id", gid).single());
  const pr = must(await T("tt_prints").select("code").eq("id", g.print_id).single());
  const name = cleanName(file.name);
  const ext = (/\.[A-Za-z0-9]{1,5}$/.exec(name) || [".bin"])[0].toLowerCase();
  const n = must(await T("tt_scans").select("id").eq("grading_id", gid)).length + 1;
  const rel = `${pr.code}/scans/${gid}/${String(n).padStart(2, "0")}_${Date.now().toString(36)}${ext}`;
  const buf = new Uint8Array(await file.arrayBuffer());
  let pages = 1;
  if (ext === ".pdf") { try { pages = await (await engine()).pageCount(buf); } catch { pages = 1; } }
  await put(rel, file, file.type || (ext === ".pdf" ? "application/pdf" : "application/octet-stream"));
  must(await T("tt_scans").insert({ grading_id: gid, path: rel, name, size: file.size, mime: file.type || "", pages }));
  log("scan_upload", g.student_id, g.print_id, { grading: gid, name, pages });
  return { scans: await scanList(gid) };
}
