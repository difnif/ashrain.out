// 시록고 강사도구 — 「서버」 자리. PC 강사도구 server.py 의 /api/* 를 브라우저에서 Supabase(tt_* · teacher-tool)로 옮김.
// 화면(ui.js)은 PC 때와 같은 모양의 응답을 받는다. PDF 일은 engine/ 이 브라우저 안에서 한다.
import { T, all, must, rpc, put, get, bytes, sign, remove, removePrefix, log, uid } from "./sb";
import {
  fmtCode, normCode, newCode, nowIso, todayStr, normName, summarize, currentMarks, roundMarks, roundsInfo, gradingStats,
  everWrong, autoJudge, guessLevel, safeName, cleanName, stripNames,
  localDay, daysBetween, parsePages, fmtPages, mergeRanges, parseProgress, uncheckedPages,
  monthStart, addMonths, parseFee, monthFlag, monthTotals,
} from "./logic";
import { groupProblems, relayout, partsFromAnswer, splitLabel, partLabel, baseHash } from "./parts";

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
// 스캔본 차수(round) = 언제 스캔한 것인지: 1 = 1차 채점 때, 2 = 2차 채점 때 …, null = 확실하지 않음.
// 운영 DB에 칸이 아직 없으면(supabase/2026-11_tt_scans_round.sql 을 안 돌렸으면) 차수 없이 그대로 쓴다.
const SCAN_COLS = "id,name,size,pages,mime,path,created_at";
let scanRoundCol = true;
const noRoundCol = (r) => !!r.error && /\bround\b/.test(r.error.message || "") && /column|schema cache/i.test(r.error.message || "");
export const scanRoundOk = () => scanRoundCol;
const cleanRound = (v) => { const n = Number(v); return v !== null && v !== "" && Number.isInteger(n) && n >= 1 && n <= 9 ? n : null; };
async function scanList(gid) {
  let r = scanRoundCol ? await T("tt_scans").select(SCAN_COLS + ",round").eq("grading_id", gid).eq("deleted", false).order("id") : null;
  if (r && noRoundCol(r)) { scanRoundCol = false; r = null; }
  if (!r) r = await T("tt_scans").select(SCAN_COLS).eq("grading_id", gid).eq("deleted", false).order("id");
  // 1차 → 2차 → … → 확실하지 않음, 같은 차는 올린 차례 (목록·한 PDF·분석용 내보내기가 모두 이 차례)
  return must(r).map((x) => ({ ...x, round: x.round ?? null, kind: /pdf/.test(x.mime) || /\.pdf$/i.test(x.name) ? "pdf" : "image", pages: x.pages || 1 }))
    .sort((a, b) => (a.round ?? 99) - (b.round ?? 99) || a.id - b.id);
}
const scanRoundsCount = (scans) => {
  const o = {};
  for (const s of scans) { const k = s.round ? `${s.round}차` : "확실하지 않음"; o[k] = (o[k] || 0) + 1; }
  return o;
};

// 학생의 다른 채점에서 같은 문항(해시)을 틀린 횟수 (어느 차든 X면 그 채점에서 1번)
async function wrongHistory(sid, hashes, excludeGid = null) {
  if (!hashes.size) return new Map();
  const gs = must(await T("tt_gradings").select("id,print_id").eq("student_id", sid));
  const others = gs.filter((g) => g.id !== excludeGid);
  if (!others.length) return new Map();
  const xs = await all(() => T("tt_marks").select("grading_id,seq").in("grading_id", others.map((g) => g.id)).eq("result", "X"));
  if (!xs.length) return new Map();
  // X 기록이 있는 문항만 그 채점의 기록을 다 읽어 차마다 마지막 기록으로 본다 — 잘못 눌렀다 고친 X · 앞 차를 고친 X는 빼고
  const xg = [...new Set(xs.map((m) => m.grading_id))], xseq = [...new Set(xs.map((m) => m.seq))];
  const [ms, ss] = await Promise.all([
    all(() => T("tt_marks").select("id,grading_id,session_no,seq,result").in("grading_id", xg).in("seq", xseq).order("id")), sessionsOf(xg)]);
  const items = await all(() => T("tt_print_items").select("print_id,seq,hash").in("print_id", [...new Set(others.map((g) => g.print_id))]));
  const hm = new Map(items.map((i) => [i.print_id + ":" + i.seq, i.hash]));
  const res = new Map();
  for (const g of others) {
    if (!xg.includes(g.id)) continue;
    const seqs = everWrong(ms.filter((m) => m.grading_id === g.id), ss.filter((s) => s.grading_id === g.id));
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
  const prints = pids.length ? must(await T("tt_prints").select("id,code,title,n_items,shelf,options,created_at").in("id", pids)) : [];
  const pm = new Map(prints.map((p) => [p.id, p]));
  const gs = must(await T("tt_gradings").select("id,print_id,status").eq("student_id", sid));
  const gids = gs.map((g) => g.id);
  const [marks, sessions] = await Promise.all([marksOf(gids), sessionsOf(gids)]);
  const scans = gids.length ? await all(() => T("tt_scans").select("grading_id,created_at").in("grading_id", gids).eq("deleted", false)) : [];
  const out = [], books = [];
  for (const t of tg) {
    const p = pm.get(t.print_id);
    if (!p || p.shelf !== "active") continue;
    const g = gs.find((x) => x.print_id === p.id);
    const bk = bookOf(p);
    if (bk) {             // 교재: 학생마다 교재 하나 = 채점 기록 하나 (스캔본은 프린트처럼) — 진도 · 채점 · 해설지는 아래에서
      if (bk.role === "student") books.push({ p, g, row: { id: p.id, code: p.code, code_fmt: fmtCode(p.code), title: p.title, master_code: bk.master_code || "",
        publisher: bk.publisher || "", grade: bk.grade || "", issued_at: t.issued_at, grading: g ? { id: g.id, status: g.status } : null } });
      continue;
    }
    const row = { id: p.id, code: p.code, code_fmt: fmtCode(p.code), title: p.title, n_items: p.n_items, issued_at: t.issued_at, grading: null };
    if (g) {
      row.grading = { id: g.id, status: g.status };
      Object.assign(row, gradingStats(marks.filter((m) => m.grading_id === g.id), sessions.filter((s) => s.grading_id === g.id), p.n_items));
      row.n_scans = scans.filter((s) => s.grading_id === g.id).length;
    }
    out.push(row);
  }
  // 반복 오답: 같은 문항(해시)을 두 번 넘게(채점마다 1번, 어느 차든 X) 틀린 것
  const allPids = [...new Set(gs.map((g) => g.print_id))];
  const items = allPids.length ? await all(() => T("tt_print_items").select("print_id,seq,hash,png,label").in("print_id", allPids)) : [];
  const allPrints = allPids.length ? must(await T("tt_prints").select("id,code,title,shelf").in("id", allPids)) : [];
  const apm = new Map(allPrints.map((p) => [p.id, p]));
  const wrong = new Map();
  for (const g of gs) {
    const p = apm.get(g.print_id);
    if (!p || p.shelf === "deleted") continue;
    for (const seq of [...everWrong(marks.filter((m) => m.grading_id === g.id), sessions.filter((s) => s.grading_id === g.id))].sort((a, b) => a - b)) {
      const it = items.find((i) => i.print_id === g.print_id && i.seq === seq);
      if (!it || !it.hash) continue;
      if (!wrong.has(it.hash)) wrong.set(it.hash, { hash: it.hash, count: 0, png: it.png ? `${p.code}/${it.png}` : null, where: [] });
      const w = wrong.get(it.hash);
      w.count += 1;
      w.where.push({ code: fmtCode(p.code), title: p.title, seq, label: it.label || "" });
    }
  }
  const rep = [...wrong.values()].filter((w) => w.count >= 2).sort((a, b) => b.count - a.count);
  const recs = must(await T("tt_class_records").select("day,kind,print_id").eq("student_id", sid).order("day", { ascending: false }));
  const records = recs.map((r) => ({ date: r.day, kind: r.kind, code: apm.get(r.print_id)?.code || pm.get(r.print_id)?.code || "", title: apm.get(r.print_id)?.title || pm.get(r.print_id)?.title || "" }));
  const blogs = await bookLogs(books.map((b) => b.p.id));
  const bookRows = books.map((b) => ({ ...b.row, ...bookState({ x: b.p, g: b.g }, blogs, scans) }));
  const curM = monthStart(todayStr()), mrows = await monthRows(null, sid);
  return { student: st, prints: out, books: bookRows, logs_ok: bookLogTable, repeat_wrong: rep, records,
    month: mflagOut(monthFlag(st, mrows.filter((r) => r.month <= curM), curM)), months: mrows.slice().reverse().slice(0, 24).map(snapMonth), months_ok: monthTable,
    month_prev: snapMonth(mrows.find((r) => r.month === addMonths(curM, -1)) || null), this_month: curM };
}

// ── 교재 — 프린트 표(tt_prints)에 options.textbook 으로 둔다(DB는 그대로).
//   role 'master' = 교재 자체(이름 · 출판사 · 학년), role 'student' = 학생마다 붙인 교재(채점 기록 · 스캔본이 여기 달림)
const bookOf = (p) => (p && p.options && p.options.textbook) || null;
async function freeCode() {
  for (let i = 0; i < 50; i++) { const c = newCode(); if (!must(await T("tt_prints").select("id").eq("code", c).limit(1)).length) return c; }
  throw new Error("코드를 만들지 못했어요");
}
async function bookPrints() {
  const ps = must(await T("tt_prints").select("id,code,title,options,created_at,shelf").eq("shelf", "active").order("id", { ascending: false }).limit(2000));
  return ps.filter((x) => bookOf(x));
}
// 학생마다 붙인 교재(role student) — { x: 학생 교재, sid, st: 학생, master: 교재 자체, g: 채점 기록 }
async function bookCopies() {
  const bs = await bookPrints();
  const masters = new Map(bs.filter((x) => bookOf(x).role === "master").map((x) => [x.id, x]));
  const studs = bs.filter((x) => bookOf(x).role === "student" && masters.has(bookOf(x).master));
  const ids = studs.map((x) => x.id);
  const gs = ids.length ? await all(() => T("tt_gradings").select("id,print_id,student_id,status").in("print_id", ids)) : [];
  const old = studs.filter((x) => !bookOf(x).student && !gs.some((g) => g.print_id === x.id));
  const tg = old.length ? must(await T("tt_targets").select("print_id,student_id").in("print_id", old.map((x) => x.id))) : [];
  const sidOf = (x) => bookOf(x).student || gs.find((g) => g.print_id === x.id)?.student_id || tg.find((t) => t.print_id === x.id)?.student_id || null;
  const sm = await studentsMap(studs.map(sidOf));
  const copies = studs.map((x) => {
    const sid = sidOf(x);
    return { x, sid, st: sm.get(sid) || null, master: masters.get(bookOf(x).master), g: gs.find((g) => g.print_id === x.id && g.student_id === sid) || null };
  }).filter((c) => c.st);
  return { masters, copies };
}

// ── 교재 기록 (supabase/2026-11_tt_book_logs.sql) — solved: 그날 몇 쪽까지 · graded: 채점한 날(몇 차 · 쪽) · solution: 해설지 준 날
let bookLogTable = true;           // 표가 아직 없으면(SQL을 안 넣었으면) 기록 없이 그대로 보여 준다
const LOG_SQL = "교재 기록 표가 DB에 아직 없어요 — supabase/2026-11_tt_book_logs.sql 을 넣어야 적을 수 있어요";
const noLogTable = (e) => { const t = String((e && e.message) || e || ""); return /tt_book_logs/.test(t) && /does not exist|schema cache|Could not find/i.test(t); };
export const bookLogsOk = () => bookLogTable;
async function bookLogs(pids) {
  if (!pids.length || !bookLogTable) return [];
  try { return await all(() => T("tt_book_logs").select("*").in("print_id", pids).order("day").order("id")); }
  catch (e) { if (noLogTable(e)) { bookLogTable = false; return []; } throw e; }
}
async function bookScans(gids) {
  return gids.length ? all(() => T("tt_scans").select("*").in("grading_id", gids).eq("deleted", false).order("id")) : [];
}
const byDay = (a, b) => String(a.day).localeCompare(String(b.day)) || a.id - b.id;
// 학생 교재 하나의 지금 모습 — 진도 · 마지막 채점(채점 기록 · 스캔본 올린 날 중 늦은 것) · 그대로 둔 날수 · 해설지 · 채점 기록이 없는 쪽(어림)
function bookState(c, logs, scans, today = todayStr()) {
  const mine = logs.filter((l) => l.print_id === c.x.id);
  const solved = mine.filter((l) => l.kind === "solved").sort(byDay);
  const graded = mine.filter((l) => l.kind === "graded").sort(byDay);
  const sol = mine.find((l) => l.kind === "solution") || null;
  const sc = c.g ? scans.filter((s) => s.grading_id === c.g.id) : [];
  const gdays = [...graded.map((l) => l.day), ...sc.map((s) => localDay(s.created_at))].filter(Boolean).sort();
  const lastG = gdays.length ? gdays[gdays.length - 1] : null;
  const ls = solved.length ? solved[solved.length - 1] : null;
  const since = localDay(c.x.created_at);
  return {
    last_solved: ls ? { day: ls.day, page_to: ls.page_to, pages: ls.pages } : null,
    last_graded: lastG, idle_days: daysBetween(lastG || since, today), never_graded: !lastG, since,
    solution: sol ? { id: sol.id, day: sol.day } : null,
    unchecked: uncheckedPages(solved, graded), n_scans: sc.length,
  };
}
const logOut = (l) => ({ id: l.id, day: l.day, kind: l.kind, page_to: l.page_to, pages: l.pages || "", round: l.round, note: l.note || "" });
async function booksList(onlyMaster = null) {
  const { masters, copies } = await bookCopies();
  const sel = onlyMaster ? copies.filter((c) => c.master.id === onlyMaster) : copies;
  const [logs, scans] = await Promise.all([bookLogs(sel.map((c) => c.x.id)), bookScans(sel.map((c) => c.g?.id).filter(Boolean))]);
  const today = todayStr();
  return [...masters.values()].filter((mst) => !onlyMaster || mst.id === onlyMaster).map((mst) => {
    const b = bookOf(mst);
    const students = sel.filter((c) => c.master.id === mst.id).map((c) => ({
      code: c.x.code, sid: c.sid, name: c.st.name, active: c.st.active !== false, gid: c.g ? c.g.id : null, since: c.x.created_at,
      ...bookState(c, logs, scans, today),
      logs: onlyMaster ? logs.filter((l) => l.print_id === c.x.id).sort(byDay).reverse().map(logOut) : undefined,
    })).sort((a, c) => a.name.localeCompare(c.name, "ko"));
    return { id: mst.id, code: mst.code, code_fmt: fmtCode(mst.code), title: mst.title, publisher: b.publisher || "", grade: b.grade || "", memo: b.memo || "",
      created_at: mst.created_at, students, logs_ok: bookLogTable };
  });
}
// 학생 교재 하나 찾기(코드 = 학생 몫 교재 코드)
async function bookCopyByCode(code) {
  const c = (await bookCopies()).copies.find((y) => y.x.code === normCode(code));
  if (!c) throw new Error("그런 학생 교재가 없어요");
  return c;
}
const cleanDay = (d) => { const t = String(d || "").trim(); if (!/^\d{4}-\d{2}-\d{2}$/.test(t) || isNaN(Date.parse(t + "T00:00:00Z"))) throw new Error("날짜를 골라 주세요"); return t; };
const cleanNote = (t) => String(t || "").trim().slice(0, 300);
function logErr(e) { if (noLogTable(e)) { bookLogTable = false; throw new Error(LOG_SQL); } throw e; }
// ── 업무 기록 — 입력마다 전 · 후를 남기고(tt_events), 「되돌리기」로 되돌린다. 되돌린 기록에는 undone_by 를 단다.
async function logRow(kind, sid, pid, detail) {
  try { return must(await T("tt_events").insert({ kind, student_id: sid ?? null, print_id: pid ?? null, detail }).select("id").single()).id; }
  catch { return null; }          // 기록은 실패해도 입력은 그대로
}
const snapLog = (r) => (r ? { id: r.id, day: r.day, kind: r.kind, page_to: r.page_to ?? null, pages: r.pages || "", round: r.round ?? null, note: r.note || "" } : null);
const sameLog = (a, b) => !!a && !!b && a.day === b.day && (a.page_to ?? null) === (b.page_to ?? null) && (a.pages || "") === (b.pages || "") && (a.round ?? null) === (b.round ?? null) && (a.note || "") === (b.note || "");
async function bookLogEvent(c, before, after) {
  const id = await logRow("book_log", c.sid, c.x.id, { table: "tt_book_logs", row_id: (after || before).id, title: c.x.title, kind: (after || before).kind, before: snapLog(before), after: snapLog(after) });
  return id ? [id] : [];
}
// 기록 하나 적기 — 진도는 그날 하나(고침), 채점은 같은 날 · 같은 차에 하나(쪽을 합침), 해설지는 한 번(날짜를 고침). 바뀐 것이 없으면 아무것도 안 함
async function bookLogPut(c, b) {
  if (!bookLogTable) throw new Error(LOG_SQL);
  const day = cleanDay(b.day || todayStr()), kind = b.kind;
  const put = async (old, row) => {
    const next = old ? { ...old, ...row } : { day, kind, page_to: null, pages: "", round: null, note: "", ...row };
    if (old && sameLog(old, next)) return { ok: true, events: [] };
    const saved = old ? must(await T("tt_book_logs").update({ ...row, updated_at: nowIso() }).eq("id", old.id).select("*").single())
      : must(await T("tt_book_logs").insert({ print_id: c.x.id, student_id: c.sid, day, kind, ...row }).select("*").single());
    return { ok: true, events: await bookLogEvent(c, old, saved) };
  };
  const drop = async (old) => {
    if (!old) return { ok: true, events: [] };
    must(await T("tt_book_logs").delete().eq("id", old.id));
    return { ok: true, removed: true, events: await bookLogEvent(c, old, null) };
  };
  try {
    if (kind === "solved") {
      const pr = parseProgress(b.progress ?? (b.page_to != null ? String(b.page_to) : ""));
      if (!pr) throw new Error("진도는 45 또는 30-45 처럼 적어 주세요");
      const old = must(await T("tt_book_logs").select("*").eq("print_id", c.x.id).eq("kind", "solved").eq("day", day).limit(1))[0];
      if (pr.empty) return drop(old);
      return put(old, { page_to: pr.to, pages: pr.pages, ...("note" in b ? { note: cleanNote(b.note) } : {}) });
    }
    if (kind === "graded") {
      const rg = parsePages(b.pages || "");
      if (!rg) throw new Error("채점한 쪽은 12-20, 25 처럼 적어 주세요");
      const round = b.round == null || b.round === "" ? null : Number(b.round);
      if (round !== null && !(Number.isInteger(round) && round >= 1 && round <= 9)) throw new Error("몇 차인지 골라 주세요");
      let q = T("tt_book_logs").select("*").eq("print_id", c.x.id).eq("kind", "graded").eq("day", day);
      q = round === null ? q.is("round", null) : q.eq("round", round);
      const old = must(await q.limit(1))[0];
      if (b.replace && !rg.length) return drop(old);          // 진도 적기에서 칸을 비움
      const pages = fmtPages(b.replace ? rg : mergeRanges([...(old ? parsePages(old.pages) || [] : []), ...rg]));
      return put(old, { round, pages, ...("note" in b ? { note: cleanNote(b.note) } : {}) });
    }
    if (kind === "solution") {
      const old = must(await T("tt_book_logs").select("*").eq("print_id", c.x.id).eq("kind", "solution").limit(1))[0];
      return put(old, { day, ...("note" in b ? { note: cleanNote(b.note) } : {}) });
    }
    throw new Error("무엇을 적을지 몰라요");
  } catch (e) { logErr(e); }
}
async function bookLogDelete(id) {
  try {
    const r = must(await T("tt_book_logs").select("*").eq("id", id).maybeSingle());
    if (!r) return { ok: true, events: [] };
    const { copies } = await bookCopies();
    const c = copies.find((y) => y.x.id === r.print_id) || { sid: r.student_id, x: { id: r.print_id, title: "" } };
    must(await T("tt_book_logs").delete().eq("id", r.id));
    return { ok: true, events: await bookLogEvent(c, r, null) };
  } catch (e) { logErr(e); }
}
// ── 재원 · 원비 (supabase/2026-11_tt_student_months.sql) — 학생 · 달마다 다님 · 휴원 · 그만둠 + 그달 원비. 매출 = 그달 다님 학생 원비 합
let monthTable = true;
const MONTH_SQL = "재원 · 원비 표가 DB에 아직 없어요 — supabase/2026-11_tt_student_months.sql 을 넣어야 적을 수 있어요";
const noMonthTable = (e) => { const t = String((e && e.message) || e || ""); return /tt_student_months/.test(t) && /does not exist|schema cache|Could not find/i.test(t); };
async function monthRows(to = null, sid = null) {
  if (!monthTable) return [];
  try {
    return await all(() => { let x = T("tt_student_months").select("*").order("month").order("id"); if (to) x = x.lte("month", to); if (sid) x = x.eq("student_id", sid); return x; });
  } catch (e) { if (noMonthTable(e)) { monthTable = false; return []; } throw e; }
}
const snapMonth = (r) => (r ? { id: r.id, month: r.month, status: r.status, fee: r.fee ?? null, note: r.note || "" } : null);
const sameMonth = (a, b) => !!a && !!b && a.month === b.month && a.status === b.status && (a.fee ?? null) === (b.fee ?? null) && (a.note || "") === (b.note || "");
const mflagOut = (f) => ({ status: f.status, fee: f.fee ?? null, flag: f.flag, quit: !!f.quit, last_month: f.last ? f.last.month : null, last_status: f.last ? f.last.status : null, last_fee: f.last ? f.last.fee ?? null : null });
// 재원으로 학생의 「다니는 중 · 쉬는 중」(active — 학생 고르기 칩 등에 쓰임)을 맞춘다: 이번 달까지의 마지막 기록이 다님이면 다니는 중
async function syncActive(sid) {
  const r = must(await T("tt_student_months").select("status").eq("student_id", sid).lte("month", monthStart(todayStr())).order("month", { ascending: false }).limit(1))[0];
  if (r) must(await T("tt_students").update({ active: r.status === "attend", updated_at: nowIso() }).eq("id", sid));
}
async function monthsView(m) {
  const cur = monthStart(/^\d{4}-\d{2}/.test(m || "") ? m : todayStr());
  const sts = must(await T("tt_students").select("id,name,grade,active").order("name"));
  const rows = await monthRows(cur);
  const prevM = addMonths(cur, -1);
  const students = sts.map((st) => {
    const row = rows.find((r) => r.student_id === st.id && r.month === cur) || null;
    const prev = rows.find((r) => r.student_id === st.id && r.month === prevM) || null;
    return { id: st.id, name: st.name, grade: st.grade || "", active: st.active !== false, row: snapMonth(row), prev: snapMonth(prev), ...mflagOut(monthFlag(st, rows, cur)) };
  });
  return { month: cur, this_month: monthStart(todayStr()), ok: monthTable, students, totals: monthTotals(rows, cur),
    history: Array.from({ length: 12 }, (_, i) => monthTotals(rows, addMonths(cur, -i))) };
}
// 달 재원 · 원비 적기 — 바뀐 줄만. 상태를 비우면 그달 기록을 지움. 줄마다 업무 기록(되돌리기)
async function monthsSave(b) {
  if (!monthTable) throw new Error(MONTH_SQL);
  const cur = monthStart(b.month);
  if (!/^\d{4}-\d{2}-01$/.test(cur)) throw new Error("달을 골라 주세요");
  const sm = await studentsMap((b.rows || []).map((r) => Number(r.sid)));
  const plan = (b.rows || []).map((r) => {
    const st = sm.get(Number(r.sid));
    const fee = parseFee(r.fee);
    if (st && (Number.isNaN(fee) || (fee != null && fee > 100000000))) throw new Error(`${st.name}: 원비는 300000 · 30만 처럼 적어 주세요`);
    if (r.status && !["attend", "pause", "quit"].includes(r.status)) throw new Error("재원 상태를 골라 주세요");
    return { st, status: r.status || "", fee, note: "note" in r ? String(r.note || "").trim().slice(0, 300) : null };
  }).filter((r) => r.st);
  const thisM = monthStart(todayStr()), events = [];
  try {
    for (const r of plan) {
      const sid = r.st.id;
      const old = must(await T("tt_student_months").select("*").eq("student_id", sid).eq("month", cur).limit(1))[0] || null;
      let saved = null;
      if (!r.status) { if (!old) continue; must(await T("tt_student_months").delete().eq("id", old.id)); }
      else {
        const row = { status: r.status, fee: r.fee, note: r.note ?? (old ? old.note : "") };
        if (old && sameMonth(old, { ...old, ...row })) continue;
        saved = old ? must(await T("tt_student_months").update({ ...row, updated_at: nowIso() }).eq("id", old.id).select("*").single())
          : must(await T("tt_student_months").insert({ student_id: sid, month: cur, ...row }).select("*").single());
      }
      if (cur <= thisM) await syncActive(sid);
      const id = await logRow("student_month", sid, null, { table: "tt_student_months", row_id: (saved || old).id, name: r.st.name, month: cur, before: snapMonth(old), after: snapMonth(saved) });
      if (id) events.push(id);
    }
  } catch (e) { if (noMonthTable(e)) { monthTable = false; throw new Error(MONTH_SQL); } throw e; }
  return { ok: true, n: events.length, events };
}

// ── 되돌리기 — 지금 모습이 그 기록의 「후」와 같을 때만 「전」으로 돌린다(그 뒤에 또 바뀌었으면 막음). 되돌릴 수 있는 표:
const UNDO = {
  tt_book_logs: {
    fields: (x) => ({ day: x.day, page_to: x.page_to ?? null, pages: x.pages || "", round: x.round ?? null, note: x.note || "" }),
    keys: (ev, x) => ({ print_id: ev.print_id, student_id: ev.student_id, kind: x.kind }), same: sameLog, snap: snapLog, missing: noLogTable, sql: LOG_SQL, where: "교재 화면",
  },
  tt_student_months: {
    fields: (x) => ({ month: x.month, status: x.status, fee: x.fee ?? null, note: x.note || "" }),
    keys: (ev) => ({ student_id: ev.student_id }), same: sameMonth, snap: snapMonth, missing: noMonthTable, sql: MONTH_SQL, where: "재원 · 원비 화면",
    after: (ev) => syncActive(ev.student_id),
  },
};
async function undoEvent(id) {
  const ev = must(await T("tt_events").select("*").eq("id", id).maybeSingle());
  if (!ev) throw new Error("그런 기록이 없어요");
  const d = ev.detail || {};
  if (d.undone_by) throw new Error("이미 되돌린 기록이에요");
  const U = UNDO[d.table];
  if (!U) throw new Error("이 기록은 되돌릴 수 없어요");
  try {
    const cur = d.row_id ? must(await T(d.table).select("*").eq("id", d.row_id).maybeSingle()) : null;
    if (d.after ? !U.same(cur, d.after) : !!cur) throw new Error(`그 뒤에 또 바뀌어서 되돌릴 수 없어요 — ${U.where}에서 고쳐 주세요`);
    let restored = null;
    if (!d.before) must(await T(d.table).delete().eq("id", cur.id));
    else if (!d.after) {
      const r = await T(d.table).insert({ ...U.keys(ev, d.before), ...U.fields(d.before) }).select("*").single();
      if (r.error && /duplicate|unique/i.test(r.error.message || "")) throw new Error(`같은 기록이 이미 있어서 되돌릴 수 없어요 — ${U.where}에서 고쳐 주세요`);
      restored = must(r);
    } else restored = must(await T(d.table).update({ ...U.fields(d.before), updated_at: nowIso() }).eq("id", cur.id).select("*").single());
    if (U.after) await U.after(ev, restored);
    const keep = Object.fromEntries(["title", "name", "kind", "month"].filter((k) => k in d).map((k) => [k, d[k]]));
    const nid = await logRow(ev.kind, ev.student_id, ev.print_id, { ...keep, table: d.table, row_id: (restored || cur).id, before: U.snap(cur), after: U.snap(restored), undo_of: ev.id });
    must(await T("tt_events").update({ detail: { ...d, undone_by: nid || -1, undone_at: nowIso() } }).eq("id", ev.id));
    return nid;
  } catch (e) { if (U.missing(e)) throw new Error(U.sql); throw e; }
}
async function undoEvents(ids) {
  const list = [...new Set((ids || []).map(Number).filter(Boolean))].sort((a, b) => b - a);       // 나중 것부터
  if (!list.length) throw new Error("되돌릴 기록을 골라 주세요");
  const done = [];
  for (const id of list) done.push(await undoEvent(id));
  return { ok: true, n: done.length, events: done.filter(Boolean) };
}
// 수업 끝 진도 적기 — 그날 학생 × 교재 (다니는 학생만)
async function bookDay(date) {
  const day = cleanDay(date || todayStr());
  const { copies } = await bookCopies();
  const sel = copies.filter((c) => c.st.active !== false);
  const logs = await bookLogs(sel.map((c) => c.x.id));
  const by = new Map();
  for (const c of sel) {
    const mine = logs.filter((l) => l.print_id === c.x.id).sort(byDay);
    const prev = mine.filter((l) => l.kind === "solved" && l.day < day).pop() || null;
    const cur = mine.find((l) => l.kind === "solved" && l.day === day) || null;
    const gr = mine.filter((l) => l.kind === "graded" && l.day === day);
    if (!by.has(c.sid)) by.set(c.sid, { sid: c.sid, name: c.st.name, grade: c.st.grade || "", books: [] });
    by.get(c.sid).books.push({ code: c.x.code, title: c.x.title, master_code: c.master.code, publisher: bookOf(c.master).publisher || "",
      prev: prev ? { day: prev.day, page_to: prev.page_to } : null,
      today: cur ? { page_to: cur.page_to, pages: cur.pages || "" } : null,
      graded: gr.map((l) => ({ round: l.round, pages: l.pages || "" })) });
  }
  const students = [...by.values()].sort((a, b) => a.name.localeCompare(b.name, "ko"));
  students.forEach((x) => x.books.sort((a, b) => a.title.localeCompare(b.title, "ko")));
  return { date: day, logs_ok: bookLogTable, students };
}
async function bookDaySave(b) {
  if (!bookLogTable) throw new Error(LOG_SQL);
  const day = cleanDay(b.date);
  const { copies } = await bookCopies();
  const rows = (b.rows || []).map((r) => ({ ...r, c: copies.find((y) => y.x.code === normCode(r.code)) })).filter((r) => r.c);
  const bad = rows.filter((r) => ("progress" in r && !parseProgress(r.progress)) || ("graded" in r && !parsePages(r.graded)));
  if (bad.length) throw new Error(`알아볼 수 없는 칸이 ${bad.length}개 있어요 — 진도는 45 또는 30-45, 채점한 쪽은 12-20, 25 처럼`);
  const events = [];
  for (const r of rows) {
    if ("progress" in r) events.push(...(await bookLogPut(r.c, { kind: "solved", day, progress: r.progress })).events);
    if ("graded" in r) events.push(...(await bookLogPut(r.c, { kind: "graded", day, pages: r.graded, round: r.round ?? 1, replace: true })).events);
  }
  return { ok: true, n: rows.length, events };
}
// 교재 기록 데이터(학생별) — JSON · CSV 받기, 학생 학습 기록 JSON
async function booksData(sid = null) {
  const { copies } = await bookCopies();
  const sel = copies.filter((c) => !sid || c.sid === sid);
  const [logs, scans] = await Promise.all([bookLogs(sel.map((c) => c.x.id)), bookScans(sel.map((c) => c.g?.id).filter(Boolean))]);
  const today = todayStr();
  const by = new Map();
  for (const c of sel) {
    const st = bookState(c, logs, scans, today), mine = logs.filter((l) => l.print_id === c.x.id).sort(byDay), b = bookOf(c.master);
    if (!by.has(c.sid)) by.set(c.sid, { student: c.st.name, grade: c.st.grade || "", active: c.st.active !== false, books: [] });
    by.get(c.sid).books.push({
      title: c.x.title, publisher: b.publisher || "", grade: b.grade || "", since: st.since,
      progress: mine.filter((l) => l.kind === "solved").map((l) => ({ day: l.day, page_to: l.page_to, ...(l.pages ? { pages: l.pages } : {}), ...(l.note ? { note: l.note } : {}) })),
      graded: mine.filter((l) => l.kind === "graded").map((l) => ({ day: l.day, round: l.round, pages: l.pages || "", ...(l.note ? { note: l.note } : {}) })),
      scans: c.g ? scans.filter((s) => s.grading_id === c.g.id).map((s) => ({ day: localDay(s.created_at), round: s.round ?? null, name: s.name, pages: s.pages || 1 })) : [],
      solution_given: st.solution ? st.solution.day : null,
      last_solved: st.last_solved, last_graded: st.last_graded, idle_days: st.idle_days,
      unchecked_pages_guess: st.unchecked.known ? st.unchecked.text : null,
      wrong_pages: [],
    });
  }
  return {
    kind: "ashrain.books", version: 1, made: nowIso(), today,
    notes: ["idle_days = 마지막 채점(채점 기록 · 스캔본 올린 날)부터 오늘까지 날수, 채점이 없으면 교재를 붙인 날부터",
      "unchecked_pages_guess = 적은 진도와 채점한 쪽으로 어림한 「채점 기록이 없는 쪽」 (채점한 쪽을 적은 기록이 없으면 null)",
      "wrong_pages = 스캔본 분석 기능이 들어간 뒤 채워져요"],
    students: [...by.values()].sort((a, b) => a.student.localeCompare(b.student, "ko")),
  };
}
function booksCsv(d) {
  const head = ["학생", "교재", "출판사", "학년", "붙인 날", "진도 날짜", "진도(쪽까지)", "마지막 채점", "그대로 둔 날수", "채점 기록이 없는 쪽(어림)", "해설지 준 날", "스캔본 수", "오답 쪽"];
  const q = (v) => { const t = v == null ? "" : String(v); return /[",\n]/.test(t) ? `"${t.replace(/"/g, '""')}"` : t; };
  const rows = [head];
  for (const s of d.students) for (const b of s.books) rows.push([s.student, b.title, b.publisher, b.grade, b.since, b.last_solved?.day || "", b.last_solved?.page_to ?? "",
    b.last_graded || "", b.idle_days, b.unchecked_pages_guess ?? "", b.solution_given || "", b.scans.length, (b.wrong_pages || []).join(" ")]);
  return "﻿" + rows.map((r) => r.map(q).join(",")).join("\r\n") + "\r\n";
}
async function bookMaster(code) {
  const mst = await printRow(code);
  if (!mst || mst.shelf !== "active" || bookOf(mst)?.role !== "master") throw new Error("그런 교재가 없어요");
  return mst;
}
// 그 학생 몫(role student) 찾기 — 없으면 null
async function bookCopy(mst, sid) {
  const mine = (await bookPrints()).filter((x) => bookOf(x).role === "student" && bookOf(x).master === mst.id);
  const direct = mine.find((x) => bookOf(x).student === sid);
  if (direct) return direct;
  const old = mine.filter((x) => !bookOf(x).student);
  if (!old.length) return null;
  const tg = must(await T("tt_targets").select("print_id").in("print_id", old.map((x) => x.id)).eq("student_id", sid));
  return (tg.length && old.find((y) => y.id === tg[0].print_id)) || null;
}
// 학생에게 교재 붙이기: 그 학생 몫을 만들고 채점 기록(스캔본이 달릴 자리)을 연다 — 이미 붙였으면 그대로
async function bookAssign(mst, sid) {
  if (!must(await T("tt_students").select("id").eq("id", sid)).length) throw new Error("그런 학생이 없어요");
  const x = await bookCopy(mst, sid);
  if (x) {
    const g = must(await T("tt_gradings").select("id").eq("print_id", x.id).eq("student_id", sid).limit(1));
    return { code: x.code, gid: g.length ? g[0].id : await rpc("tt_open_grading", { p_print: x.id, p_student: sid, p_purpose: null }), existed: true };
  }
  const b = bookOf(mst);
  const code = await freeCode();
  const row = must(await T("tt_prints").insert({ code, title: mst.title, kind: "registered", label: "교재", shelf: "active",
    options: { textbook: { role: "student", master: mst.id, master_code: mst.code, student: sid, publisher: b.publisher || "", grade: b.grade || "" } } }).select("id,code").single());
  const gid = await rpc("tt_open_grading", { p_print: row.id, p_student: sid, p_purpose: null });
  log("book_assign", sid, row.id, { code, master: mst.code, title: mst.title });
  return { code, gid, existed: false };
}
async function bookCreate(b) {
  const title = String(b.title || "").trim().slice(0, 80);
  if (!title) throw new Error("교재 이름을 넣어 주세요");
  const pub = String(b.publisher || "").trim().slice(0, 40);
  const same = (await bookPrints()).find((x) => bookOf(x).role === "master" && x.title === title && (bookOf(x).publisher || "") === pub);
  if (same) throw new Error("같은 이름의 교재가 이미 있어요");
  const code = await freeCode();
  const tb = { role: "master", publisher: pub, grade: String(b.grade || "").trim().slice(0, 20), memo: String(b.memo || "").trim().slice(0, 200) };
  const row = must(await T("tt_prints").insert({ code, title, kind: "registered", label: "교재", shelf: "active", options: { textbook: tb } }).select("id,code,title,options").single());
  log("book_add", null, row.id, { code, title });
  const sids = [...new Set([...(b.student_ids || []).map(Number).filter(Boolean), ...(b.students?.length ? await ensureStudents(b.students) : [])])];
  for (const sid of sids) await bookAssign(row, sid);
  return { ok: true, code, n_students: sids.length };
}
async function bookEdit(code, b) {
  const mst = await bookMaster(code);
  const studs = (await bookPrints()).filter((x) => bookOf(x).role === "student" && bookOf(x).master === mst.id);
  if (b.assign) return { ok: true, ...(await bookAssign(mst, Number(b.assign))) };
  if (b.unassign) {
    const sid = Number(b.unassign);
    const x = await bookCopy(mst, sid);
    if (!x) return { ok: true };
    const gs = must(await T("tt_gradings").select("id").eq("print_id", x.id));
    const gids = gs.map((g) => g.id);
    const nScan = gids.length ? must(await T("tt_scans").select("id").in("grading_id", gids).eq("deleted", false)).length : 0;
    const nMark = gids.length ? must(await T("tt_marks").select("id").in("grading_id", gids).limit(1)).length : 0;
    if (nScan || nMark) throw new Error("올린 스캔본이나 채점 기록이 있어서 뺄 수 없어요 — 스캔본을 먼저 지워 주세요");
    if ((await bookLogs([x.id])).length) throw new Error("진도 · 채점 · 해설지 기록이 있어서 뺄 수 없어요 — 기록을 먼저 지워 주세요");
    await purgePrint(x.id);
    log("book_unassign", sid, mst.id, { code: x.code, master: mst.code, title: mst.title });
    return { ok: true };
  }
  if (b.delete) {
    if (studs.length) throw new Error("이 교재를 쓰는 학생이 있어서 지울 수 없어요 — 학생에게서 먼저 빼 주세요");
    await purgePrint(mst.id);
    log("book_delete", null, null, { code: mst.code, title: mst.title });
    return { ok: true };
  }
  const tb = { ...bookOf(mst) };
  const up = {};
  if ("title" in b) { const t = String(b.title || "").trim().slice(0, 80); if (!t) throw new Error("교재 이름을 넣어 주세요"); up.title = t; }
  for (const k of ["publisher", "grade", "memo"]) if (k in b) tb[k] = String(b[k] || "").trim().slice(0, k === "memo" ? 200 : k === "grade" ? 20 : 40);
  const dup = (await bookPrints()).find((x) => x.id !== mst.id && bookOf(x).role === "master" && x.title === (up.title || mst.title) && (bookOf(x).publisher || "") === (tb.publisher || ""));
  if (dup) throw new Error("같은 이름의 교재가 이미 있어요");
  must(await T("tt_prints").update({ ...up, options: { ...mst.options, textbook: tb }, updated_at: nowIso() }).eq("id", mst.id));
  for (const x of studs) {          // 학생 몫에도 이름 · 출판사 · 학년을 맞춘다
    const xb = { ...bookOf(x), publisher: tb.publisher || "", grade: tb.grade || "" };
    must(await T("tt_prints").update({ ...up, options: { ...x.options, textbook: xb }, updated_at: nowIso() }).eq("id", x.id));
  }
  log("book_edit", null, mst.id, { code: mst.code, ...up });
  return { ok: true };
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
  const prints = must(await T("tt_prints").select("id,code,title,n_items,shelf,options").in("id", [...new Set(gs.map((g) => g.print_id))]));
  const pm = new Map(prints.map((p) => [p.id, p]));
  const sm = await studentsMap(gs.map((g) => g.student_id));
  const gids = gs.map((g) => g.id);
  const [marks, sessions] = await Promise.all([marksOf(gids), sessionsOf(gids)]);
  // 교재는 늘 열려 있는 기록(스캔본 자리)이라 「이어서 채점할 것」에는 넣지 않는다
  return gs.filter((g) => pm.get(g.print_id)?.shelf === "active" && !(q.status === "unfinished" && bookOf(pm.get(g.print_id)))).map((g) => {
    const p = pm.get(g.print_id), bk = bookOf(p);
    return { ...g, name: sm.get(g.student_id)?.name || "?", code: p.code, code_fmt: fmtCode(p.code), title: p.title, n_items: p.n_items,
             book: bk ? bk.master_code || p.code : null,
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
    const prints = tg.length ? must(await T("tt_prints").select("id,code,title,n_items,shelf,options").in("id", tg.map((t) => t.print_id))) : [];
    const pm = new Map(prints.filter((p) => !bookOf(p)).map((p) => [p.id, p]));        // 교재는 수업 기록의 「받은 프린트」에서 뺌
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
const itemKey = (code, it) => baseHash(it.hash) || `${code}:${it.seq}`;      // 하위 문제(「…#2」)는 문제 하나의 전사본을 같이 씀
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
      const key = it.hash || `${p.code}:${it.seq}`;          // 하위 문제마다 따로(「…#2」)
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
  const tr = await transcriptsOf([...new Set(order.map((k) => baseHash(k) || k))]);
  for (const k of order) {
    const t = tr.get(baseHash(k) || k);
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
        image: it.png ? `시험지 ${splitLabel(it.label || String(it.seq)).base}번` : null, answer_image: !!it.answer_png, solution_image: !!it.sol_png,
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
    summary: d.summary, scans: d.scans.length, ...(d.scans.length ? { scans_when: scanRoundsCount(d.scans) } : {}),
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
  const prints = gs.length ? must(await T("tt_prints").select("id,shelf,options").in("id", gs.map((g) => g.print_id))) : [];
  const ok = new Set(prints.filter((p) => p.shelf === "active" && !bookOf(p)).map((p) => p.id));        // 교재는 아래 books 로
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
    books: ((await booksData(sid)).students[0] || { books: [] }).books,
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
    const [tg, bk] = await Promise.all([all(() => T("tt_targets").select("student_id,print_id,issued_at")), bookPrints()]);
    const bids = new Set(bk.map((x) => x.id));
    const curM = monthStart(todayStr()), mrows = await monthRows(curM);
    return sts.map((s) => {
      const mine = tg.filter((t) => t.student_id === s.id && !bids.has(t.print_id));
      return { ...s, n_prints: mine.length, n_books: tg.filter((t) => t.student_id === s.id && bids.has(t.print_id)).length,
        last_issued: mine.map((t) => t.issued_at).sort().pop() || null,
        month: monthTable ? mflagOut(monthFlag(s, mrows, curM)) : null };          // 이번 달 재원 (표가 없으면 null)
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
    let prints = must(await x).filter((pr) => !bookOf(pr));       // 교재는 교재 탭에서
    if (q.student) {
      const tg = must(await T("tt_targets").select("print_id").eq("student_id", Number(q.student)));
      const ids = new Set(tg.map((t) => t.print_id));
      prints = prints.filter((pr) => ids.has(pr.id));
    }
    return printBriefs(prints);
  }
  if ((m = /^prints\/([A-Za-z0-9-]+)\/parts$/.exec(p))) return printParts(m[1], post ? body : null);
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
      const scans = gs.length ? await all(() => T("tt_scans").select("grading_id").in("grading_id", gs.map((g) => g.id)).eq("deleted", false)) : [];
      d.gradings = gs.map((g) => ({ ...g, name: sm.get(g.student_id)?.name || "?", n_scans: scans.filter((s) => s.grading_id === g.id).length,
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
  // 교재 — 등록 · 학생에게 붙이기 · 빼기 · 고치기 · 지우기 (스캔본은 학생 몫의 채점 기록에: gradings/<id>/scans 그대로)
  if (p === "months") return post ? monthsSave(body) : monthsView(q.month);            // 재원 · 원비
  if (p === "books") return post ? bookCreate(body) : booksList();
  if (p === "books/day") return post ? bookDaySave(body) : bookDay(q.date);          // 수업 끝 진도 적기
  if (p === "booklogs" && post) return bookLogPut(await bookCopyByCode(body.code), body);   // 교재 기록 하나 (진도 · 채점한 날 · 해설지)
  if ((m = /^booklogs\/(\d+)$/.exec(p)) && post && body.delete) return bookLogDelete(Number(m[1]));
  if (p === "undo" && post) return undoEvents(body.events);                         // 업무 기록 되돌리기
  if ((m = /^books\/([A-Za-z0-9-]+)$/.exec(p))) {
    if (post) return bookEdit(m[1], body);
    const mst = await bookMaster(m[1]);
    return (await booksList(mst.id))[0];
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
  // 앞 차(1차 …) 결과 고치기 — 다음 차를 시작한 뒤에도 (supabase/2026-11_tt_round_fix.sql 의 tt_mark_round · tt_retry_add)
  if ((m = /^gradings\/(\d+)\/fix$/.exec(p))) {
    const gid = Number(m[1]);
    const result = String(body.result || "");
    if (!["O", "X", "U"].includes(result)) throw new Error("앞 차 결과는 O · X · 안 풂 중에서 골라 바꿔요");
    const r = await roundFn(() => rpc("tt_mark_round", { p_grading: gid, p_round: Number(body.round), p_seq: Number(body.seq), p_result: result, p_answer: body.answer ?? null }));
    if (body.light) return r;
    return { ...(await gradingDetail(gid)), fix: r };
  }
  // 채점 취소 — 읽기(GET): 무엇을 되돌릴지만, 보내기(POST): 지금 열린 회차와 그 뒤 매긴 것을 되돌림(처음 연 채점이면 기록째 없앰)
  // (supabase/2026-11_tt_round_follow.sql 의 tt_cancel_grading)
  if ((m = /^gradings\/(\d+)\/cancel$/.exec(p))) {
    const r = await roundFn(() => rpc("tt_cancel_grading", { p_grading: Number(m[1]), p_dry: !post }));
    if (post && r && r.paths?.length) { try { await remove(r.paths); } catch { /* 다음에 */ } }
    return r;
  }
  if ((m = /^gradings\/(\d+)\/close$/.exec(p))) {
    const st = await rpc("tt_close_grading", { p_grading: Number(m[1]), p_reason: body.reason || "done", p_untouched: !!body.untouched });
    return { status: st };
  }
  if ((m = /^scans\/(\d+)$/.exec(p)) && post && "round" in body && !body.delete) {      // 언제 스캔한 것인지 바꾸기
    const r = must(await T("tt_scans").select("id,grading_id,name").eq("id", Number(m[1])).maybeSingle());
    if (!r) throw new Error("없음");
    const rd = cleanRound(body.round);
    const u = await T("tt_scans").update({ round: rd }).eq("id", r.id);
    if (noRoundCol(u)) { scanRoundCol = false; throw new Error("차수를 적을 칸이 DB에 아직 없어요 — supabase/2026-11_tt_scans_round.sql 을 SQL Editor에서 한 번 실행해 주세요"); }
    must(u);
    const g = must(await T("tt_gradings").select("student_id,print_id").eq("id", r.grading_id).single());
    log("scan_round", g.student_id, g.print_id, { grading: r.grading_id, name: r.name, round: rd });
    return { scans: await scanList(r.grading_id) };
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
  if (p === "library/register") return libraryRegister(body.code, body);
  if (p === "export/prints") return (await engine()).exportPrints(q, ctx());
  if (p === "export/transcribe") return (await engine()).exportTranscribe(body, ctx());
  if (p === "export/analysis") return (await engine()).exportAnalysis(body, ctx());
  if (p === "export/import") return (await engine()).importTranscripts(body, ctx());
  if (p === "inbox") return [];
  throw new Error("없는 요청: " + p);
}

// 앞 차 고치기 · 채점 취소 함수가 운영 DB에 아직 없으면 알아듣게
async function roundFn(call) {
  try { return await call(); } catch (e) {
    const msg = e.message || "";
    if (/tt_mark_round|tt_cancel_grading/.test(msg) && /function|schema cache/i.test(msg)) {
      throw new Error(/tt_cancel_grading/.test(msg)
        ? "DB에 「채점 취소」 함수가 아직 없어요 — supabase/2026-11_tt_round_follow.sql 을 한 번 실행해야 해요"
        : "DB에 「앞 차 고치기」 함수가 아직 없어요 — supabase/2026-11_tt_round_fix.sql 을 한 번 실행해야 해요");
    }
    throw e;
  }
}

// ── 하위 문제 (1)(2)(3) 따로 채점 — 이미 있는 프린트의 문항 줄 나누기 · 다시 묶기 (supabase/2026-11_tt_item_parts.sql 의 tt_relayout_items)
async function printParts(code, body) {
  const pr = await printRow(code);
  if (!pr || pr.shelf !== "active") throw new Error("그런 코드의 프린트가 없어요");
  const rows = await itemsOf(pr.id);
  if (!body) {
    // 문제마다 지금 하위 문제 + 찾은 하위 문제(정답 글자 「(1) … (2) …」 · 문제지 글자의 줄머리 (1) (2))
    let inSheet = {};
    if (pr.files && pr.files.sheet && rows.some((r) => r.page && r.bbox && !splitLabel(r.label).part)) {
      try { inSheet = await (await engine()).partsInSheet(await bytes(pr.files.sheet), rows.filter((r) => r.page && r.bbox)); } catch { inSheet = {}; }
    }
    const gs = must(await T("tt_gradings").select("id").eq("print_id", pr.id));
    return {
      print: await printBrief(pr.id), n_gradings: gs.length,
      groups: groupProblems(rows).map((g) => {
        const r0 = g.rows[0];
        const a = g.parts || r0.choice ? null : partsFromAnswer(r0.answer);
        const found = r0.choice ? 0 : Math.max(a ? a.length : 0, inSheet[r0.seq] || 0);
        return { base: g.base, seq: r0.seq, png: r0.png, choice: !!r0.choice, answer: g.parts ? "" : r0.answer || "", answer_png: r0.answer_png,
          parts: g.parts ? g.rows.map((r) => ({ seq: r.seq, label: partLabel(splitLabel(r.label).part), answer: r.answer || "" })) : null,
          found: found >= 2 ? found : 0, found_answers: a ? a.map((x) => x.answer) : [] };
      }),
    };
  }
  // body.plan: [[문제 첫 줄 seq, [{answer}, …](둘 이상) | null(나누지 않음)], …] — 적지 않은 문제는 그대로
  const plan = new Map((body.plan || []).map(([sq, v]) => [Number(sq), Array.isArray(v) && v.length >= 2
    ? v.map((x, k) => ({ label: partLabel(k + 1), answer: String((x && x.answer) || "").trim() })) : null]));
  const layout = relayout(rows, plan);
  try {
    const r = await rpc("tt_relayout_items", { p_print: pr.id, p_layout: layout });
    return { ok: true, items: r.items, marks: r.marks, parts: layout.filter((x) => splitLabel(x.label).part).length };
  } catch (e) {
    if (/tt_relayout_items|function|schema cache/i.test(e.message)) throw new Error("DB에 「문항 나누기」 함수가 아직 없어요 — supabase/2026-11_tt_item_parts.sql 을 한 번 실행해야 해요");
    throw e;
  }
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
async function libraryRegister(code, opts = {}) {
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
  // 등록 정보로 문항 자리를 다 찾으면 확인 화면 없이 바로 등록 (코드만 넣으면 끝) — opts.review 면 확인 화면
  if (opts.review) return (await engine()).libraryDraft(pr, ctx());
  const r = await (await engine()).libraryAuto(pr, ctx());
  if (!r.done) return r.draft;
  return { done: true, auto: true, print: r.print, n_items: r.n_items, n_answers: r.n_answers, n_sols: r.n_sols, targets: r.targets };
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
  if ((m = /^\/dl\/books\.(json|csv)$/.exec(u.pathname))) {                 // 교재 기록 받기 (?student=학생)
    const sid = /^\d+$/.test(q.student || "") ? Number(q.student) : null;
    const d = await booksData(sid);
    const who = sid ? (d.students[0]?.student || "학생") + "_" : "";
    if (m[1] === "json") return { json: d, name: `${who}교재기록_${todayStr()}.json` };
    return { blob: new Blob([booksCsv(d)], { type: "text/csv;charset=utf-8" }), name: `${who}교재기록_${todayStr()}.csv`, view: false };
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

// 스캔본 올리기 — round: 1 = 1차 채점 때, 2 = 2차 채점 때 …, null = 확실하지 않음
export async function uploadScan(gid, file, round = null) {
  const rd = cleanRound(round);
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
  const row = { grading_id: gid, path: rel, name, size: file.size, mime: file.type || "", pages };
  let r = await T("tt_scans").insert(scanRoundCol ? { ...row, round: rd } : row);
  if (scanRoundCol && noRoundCol(r)) { scanRoundCol = false; r = await T("tt_scans").insert(row); }
  must(r);
  log("scan_upload", g.student_id, g.print_id, { grading: gid, name, pages, round: scanRoundCol ? rd : undefined });
  return { scans: await scanList(gid) };
}
