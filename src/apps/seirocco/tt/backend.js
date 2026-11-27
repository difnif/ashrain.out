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
// taught = 풀어 줌(맞음으로 셈) — 칸이 아직 없으면(supabase/2026-11_tt_taught.sql 전) 그 칸 없이
let taughtCol = true;
const TAUGHT_SQL = "「풀어 줌」은 DB에 supabase/2026-11_tt_taught.sql 을 넣어야 써요";
async function marksOf(gids) {
  if (!gids.length) return [];
  if (taughtCol) {
    try { return await all(() => T("tt_marks").select("id,grading_id,session_no,seq,result,answer,at,taught").in("grading_id", gids).order("id")); }
    catch (e) { if (!/taught/.test(String(e.message || e))) throw e; taughtCol = false; }
  }
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
      .map((r) => ({ round: r, result: rm.get(r).get(it.seq).result, answer: rm.get(r).get(it.seq).answer, taught: !!rm.get(r).get(it.seq).taught }));
    it.wrong_before = hist.get(it.hash) || 0;
    it.repeat = it.wrong_before + (it.rounds.some((x) => x.result === "X") ? 1 : 0) >= 2;
  }
  const last = sessions[sessions.length - 1] || {};
  // 마지막 넘어가기(푼 만큼만) — 그 뒤 다시 열지 않았으면 결과 화면에서 되돌릴 수 있음
  const pe = must(await T("tt_events").select("id,at,detail").eq("kind", "grading_pass").eq("print_id", g.print_id).eq("student_id", g.student_id)
    .order("id", { ascending: false }).limit(1))[0];
  const pd = (pe && pe.detail) || {};
  const pass = pe && Number(pd.grading) === g.id && Number(pd.session) === last.no && last.ended_at
    ? { id: pe.id, at: pe.at, kind: pd.kind, round: pd.round, n: pd.n, undone: !!pd.undone_by } : null;
  return {
    pass,
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
    month_prev: snapMonth(mrows.find((r) => r.month === addMonths(curM, -1)) || null), this_month: curM, plans: await feePlans(), per_week_ok: perWeekCol,
    attendance: (await attOut(await attRows(addDays(todayStr(), -120), addDays(todayStr(), 60), sid))).reverse(), att_ok: attTable };
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
  const ids = sel.map((c) => c.x.id);
  const [logs, scans, bm, bq] = await Promise.all([bookLogs(ids), bookScans(sel.map((c) => c.g?.id).filter(Boolean)),
    ids.length ? anaRows("tt_book_marks", () => T("tt_book_marks").select("print_id,item_id,round,result").in("print_id", ids)) : [],
    ids.length ? anaRows("tt_questions", () => T("tt_questions").select("print_id,status,reason,reason_later").in("print_id", ids)) : []]);
  const today = todayStr();
  const postits = (pid) => {                       // 지금 틀림인 문항 수(문항마다 가장 늦은 차)
    const last = new Map();
    for (const m of bm) if (m.print_id === pid && (!last.has(m.item_id) || last.get(m.item_id).round < m.round)) last.set(m.item_id, m);
    return { n_items: last.size, n_postits: [...last.values()].filter((m) => m.result === "X").length };
  };
  const asks = (pid) => bq.filter((q) => q.print_id === pid && (q.status === "open" || (q.status === "accepted" && q.reason_later && !q.reason))).length;
  return [...masters.values()].filter((mst) => !onlyMaster || mst.id === onlyMaster).map((mst) => {
    const b = bookOf(mst);
    const students = sel.filter((c) => c.master.id === mst.id).map((c) => ({
      code: c.x.code, sid: c.sid, name: c.st.name, active: c.st.active !== false, gid: c.g ? c.g.id : null, since: c.x.created_at,
      ...bookState(c, logs, scans, today), ...postits(c.x.id), n_ask: asks(c.x.id),
      n_unanalyzed: c.g ? scans.filter((x) => x.grading_id === c.g.id && !x.analyzed_at).length : 0,
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
    const rows = await all(() => { let x = T("tt_student_months").select("*").order("month").order("id"); if (to) x = x.lte("month", to); if (sid) x = x.eq("student_id", sid); return x; });
    if (rows.length) perWeekCol = "per_week" in rows[0];          // 주당 횟수 칸이 있는지(원비표 SQL을 넣었는지)
    return rows;
  } catch (e) { if (noMonthTable(e)) { monthTable = false; return []; } throw e; }
}
const snapMonth = (r) => (r ? { id: r.id, month: r.month, status: r.status, fee: r.fee ?? null, per_week: r.per_week ?? null, note: r.note || "" } : null);
const sameMonth = (a, b) => !!a && !!b && a.month === b.month && a.status === b.status && (a.fee ?? null) === (b.fee ?? null) && (a.per_week ?? null) === (b.per_week ?? null) && (a.note || "") === (b.note || "");
// 주당 횟수 칸(supabase/2026-11_tt_fee_plans.sql)이 아직 없으면 그 칸 없이 쓴다
let perWeekCol = true;
const noPerWeek = (e) => /per_week/.test(String((e && e.message) || e || "")) && /column|schema cache|Could not find/i.test(String((e && e.message) || e || ""));
async function monthWrite(build) {
  const r = await build(perWeekCol);
  if (r.error && perWeekCol && noPerWeek(r.error)) { perWeekCol = false; return build(false); }
  return r;
}
// ── 원비표 (supabase/2026-11_tt_fee_plans.sql) — 언제부터 · 대상(학년 묶음) · 주당 횟수마다 월 원비. 학원 영업 정보라 이 표에만 둔다.
let feeTable = true;
const FEE_SQL = "원비표 표가 DB에 아직 없어요 — supabase/2026-11_tt_fee_plans.sql 을 넣어야 해요";
const noFeeTable = (e) => { const t = String((e && e.message) || e || ""); return /tt_fee_plans/.test(t) && /does not exist|schema cache|Could not find/i.test(t); };
const FEE_F = ["start_month", "level", "grades", "per_week", "minutes", "fee", "note"];
const snapFee = (r) => (r ? { id: r.id, ...Object.fromEntries(FEE_F.map((k) => [k, r[k] ?? null])) } : null);
const sameFee = (a, b) => !!a && !!b && FEE_F.every((k) => JSON.stringify(a[k] ?? null) === JSON.stringify(b[k] ?? null));
async function feePlans() {
  if (!feeTable) return [];
  try { return await all(() => T("tt_fee_plans").select("*").order("start_month").order("level").order("per_week")); }
  catch (e) { if (noFeeTable(e)) { feeTable = false; return []; } throw e; }
}
const GRADE_OK = /^(초[1-6]|중[1-3]|고[1-3])$/;
// 원비표 한 벌(그 달부터) 바꾸기 — 그 달 것을 모두 지우고 새로 넣음, 업무 기록 하나(여러 줄)로 되돌리기
async function feePlanSave(b) {
  if (!feeTable) throw new Error(FEE_SQL);
  const start = monthStart(b.start_month || "");
  if (!/^\d{4}-\d{2}-01$/.test(start)) throw new Error("언제부터인지 달을 골라 주세요");
  const rows = (b.rows || []).map((r) => ({
    level: String(r.level || "").trim().slice(0, 40), grades: [...new Set((r.grades || []).map((g) => String(g).trim()).filter((g) => GRADE_OK.test(g)))],
    per_week: Number(r.per_week), minutes: r.minutes === "" || r.minutes == null ? null : Number(r.minutes), fee: parseFee(r.fee), note: String(r.note || "").trim().slice(0, 200),
  }));
  for (const r of rows) {
    if (!r.level || !r.grades.length) throw new Error("대상 이름과 학년(초1 ~ 고3)을 적어 주세요");
    if (!Number.isInteger(r.per_week) || r.per_week < 1 || r.per_week > 7) throw new Error(`${r.level}: 주당 횟수는 1 ~ 7`);
    if (r.fee == null || Number.isNaN(r.fee) || r.fee > 100000000) throw new Error(`${r.level} 주${r.per_week}회: 원비는 300000 · 30만 처럼 적어 주세요`);
    if (r.minutes != null && !(Number.isInteger(r.minutes) && r.minutes >= 10 && r.minutes <= 600)) throw new Error(`${r.level}: 수업 길이(분)는 10 ~ 600`);
  }
  const key = (r) => `${r.level}|${r.per_week}`;
  if (new Set(rows.map(key)).size !== rows.length) throw new Error("같은 대상 · 같은 주당 횟수가 두 번 있어요");
  try {
    const old = must(await T("tt_fee_plans").select("*").eq("start_month", start));
    const out = [];
    for (const o of old) if (!rows.some((r) => key(r) === key(o))) { must(await T("tt_fee_plans").delete().eq("id", o.id)); out.push({ table: "tt_fee_plans", row_id: o.id, before: snapFee(o), after: null }); }
    for (const r of rows) {
      const o = old.find((x) => key(x) === key(r));
      const want = { start_month: start, ...r };
      if (o && sameFee(o, want)) continue;
      const saved = o ? must(await T("tt_fee_plans").update({ ...r, updated_at: nowIso() }).eq("id", o.id).select("*").single())
        : must(await T("tt_fee_plans").insert(want).select("*").single());
      out.push({ table: "tt_fee_plans", row_id: saved.id, before: snapFee(o || null), after: snapFee(saved) });
    }
    if (!out.length) return { ok: true, events: [] };
    const eid = await logRow("fee_plan", null, null, { table: "multi", rows: out, month: start, summary: { n: rows.length } });
    return { ok: true, events: eid ? [eid] : [] };
  } catch (e) { if (noFeeTable(e)) { feeTable = false; throw new Error(FEE_SQL); } throw e; }
}
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
  return { month: cur, this_month: monthStart(todayStr()), ok: monthTable, students, totals: monthTotals(rows, cur), plans: await feePlans(), fees_ok: feeTable, per_week_ok: perWeekCol,
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
    const pw = r.per_week === "" || r.per_week == null ? null : Number(r.per_week);
    if (st && pw !== null && !(Number.isInteger(pw) && pw >= 1 && pw <= 7)) throw new Error(`${st.name}: 주당 횟수는 1 ~ 7`);
    return { st, status: r.status || "", fee, per_week: "per_week" in r ? pw : undefined, note: "note" in r ? String(r.note || "").trim().slice(0, 300) : null };
  }).filter((r) => r.st);
  const thisM = monthStart(todayStr()), events = [];
  try {
    for (const r of plan) {
      const sid = r.st.id;
      const old = must(await T("tt_student_months").select("*").eq("student_id", sid).eq("month", cur).limit(1))[0] || null;
      if (old) perWeekCol = "per_week" in old;
      let saved = null;
      if (!r.status) { if (!old) continue; must(await T("tt_student_months").delete().eq("id", old.id)); }
      else {
        const row = { status: r.status, fee: r.fee, note: r.note ?? (old ? old.note : ""), per_week: !perWeekCol ? null : r.per_week !== undefined ? r.per_week : old ? old.per_week ?? null : null };
        if (old && sameMonth(old, { ...old, ...row })) continue;
        const strip = (x, withPw) => { const y = { ...x }; if (!withPw) delete y.per_week; return y; };
        saved = must(old ? await monthWrite((pw) => T("tt_student_months").update({ ...strip(row, pw), updated_at: nowIso() }).eq("id", old.id).select("*").single())
          : await monthWrite((pw) => T("tt_student_months").insert({ student_id: sid, month: cur, ...strip(row, pw) }).select("*").single()));
      }
      if (cur <= thisM) await syncActive(sid);
      const id = await logRow("student_month", sid, null, { table: "tt_student_months", row_id: (saved || old).id, name: r.st.name, month: cur, before: snapMonth(old), after: snapMonth(saved) });
      if (id) events.push(id);
    }
  } catch (e) { if (noMonthTable(e)) { monthTable = false; throw new Error(MONTH_SQL); } throw e; }
  return { ok: true, n: events.length, events };
}

// ── 결석부 (supabase/2026-11_tt_attendance.sql) — 학생 · 날마다 하나: 결석 확정 · 결석 예정 · 지각 · 지각 예정 · 조퇴 예정 · 연락 없음 + 사유.
//   당일 확인(왔음 · 안 옴 · 늦음). source = 누가 넣었나(강사 · 나중에 학부모 모드 종성에서 학부모)
let attTable = true;
const ATT_SQL = "결석부 표가 DB에 아직 없어요 — supabase/2026-11_tt_attendance.sql 을 넣어야 적을 수 있어요";
const noAttTable = (e) => { const t = String((e && e.message) || e || ""); return /tt_attendance/.test(t) && /does not exist|schema cache|Could not find/i.test(t); };
const ATT_KINDS = ["absent", "absent_maybe", "late", "late_maybe", "early_maybe", "no_contact"];
const ATT_UNSURE = ["absent_maybe", "late_maybe", "early_maybe", "no_contact"];        // 당일에 확인해야 하는 것
const snapAtt = (r) => (r ? { id: r.id, day: r.day, kind: r.kind, reason: r.reason || "", checked: r.checked ?? null, source: r.source || "teacher" } : null);
const sameAtt = (a, b) => !!a && !!b && a.day === b.day && a.kind === b.kind && (a.reason || "") === (b.reason || "") && (a.checked ?? null) === (b.checked ?? null);
const addDays = (d, k) => new Date(Date.parse(d + "T00:00:00Z") + k * 86400000).toISOString().slice(0, 10);
async function attRows(from, to, sid = null) {
  if (!attTable) return [];
  try { return await all(() => { let x = T("tt_attendance").select("*").order("day").order("id"); if (from) x = x.gte("day", from); if (to) x = x.lte("day", to); if (sid) x = x.eq("student_id", sid); return x; }); }
  catch (e) { if (noAttTable(e)) { attTable = false; return []; } throw e; }
}
async function attOut(rows) {
  const sm = await studentsMap(rows.map((r) => r.student_id));
  return rows.map((r) => ({ ...snapAtt(r), sid: r.student_id, name: sm.get(r.student_id)?.name || "?", checked_at: r.checked_at || null }));
}
const attFail = (e) => { if (noAttTable(e)) { attTable = false; throw new Error(ATT_SQL); } throw e; };
// 결석부 적기 — 학생 · 날마다 하나(이미 있으면 종류 · 사유를 고침)
async function attPut(b) {
  if (!attTable) throw new Error(ATT_SQL);
  const sid = Number(b.sid), day = cleanDay(b.day || todayStr());
  if (!ATT_KINDS.includes(b.kind)) throw new Error("결석 · 지각 · 조퇴 중에서 골라 주세요");
  const st = (await studentsMap([sid])).get(sid);
  if (!st) throw new Error("학생을 골라 주세요");
  try {
    const old = must(await T("tt_attendance").select("*").eq("student_id", sid).eq("day", day).limit(1))[0] || null;
    const row = { kind: b.kind, reason: String(b.reason ?? (old ? old.reason : "")).trim().slice(0, 300) };
    if (old && sameAtt(old, { ...old, ...row })) return { ok: true, events: [] };
    const saved = old ? must(await T("tt_attendance").update({ ...row, updated_at: nowIso() }).eq("id", old.id).select("*").single())
      : must(await T("tt_attendance").insert({ student_id: sid, day, ...row }).select("*").single());
    const id = await logRow("attendance", sid, null, { table: "tt_attendance", row_id: saved.id, name: st.name, day, before: snapAtt(old), after: snapAtt(saved) });
    return { ok: true, events: id ? [id] : [] };
  } catch (e) { attFail(e); }
}
// 당일 확인 · 고치기 · 지우기
async function attEdit(id, b) {
  if (!attTable) throw new Error(ATT_SQL);
  try {
    const old = must(await T("tt_attendance").select("*").eq("id", id).maybeSingle());
    if (!old) throw new Error("그런 결석부 기록이 없어요");
    const st = (await studentsMap([old.student_id])).get(old.student_id);
    let saved = null;
    if (b.delete) must(await T("tt_attendance").delete().eq("id", id));
    else {
      const up = {};
      if ("check" in b) {
        if (b.check !== null && !["came", "absent", "late"].includes(b.check)) throw new Error("왔음 · 안 옴 · 늦음 중에서 골라 주세요");
        up.checked = b.check; up.checked_at = b.check ? nowIso() : null;
      }
      if ("kind" in b) { if (!ATT_KINDS.includes(b.kind)) throw new Error("결석 · 지각 · 조퇴 중에서 골라 주세요"); up.kind = b.kind; }
      if ("reason" in b) up.reason = String(b.reason || "").trim().slice(0, 300);
      if (sameAtt(old, { ...old, ...up })) return { ok: true, events: [] };
      saved = must(await T("tt_attendance").update({ ...up, updated_at: nowIso() }).eq("id", id).select("*").single());
    }
    const eid = await logRow("attendance", old.student_id, null, { table: "tt_attendance", row_id: id, name: st ? st.name : "", day: old.day, before: snapAtt(old), after: snapAtt(saved) });
    return { ok: true, events: eid ? [eid] : [] };
  } catch (e) { attFail(e); }
}
// 오늘 대시보드 — 그날 결석부 · 확인 안 한 지난 것 · 다가오는 7일 · 지난 30일 · 재원을 안 적은 학생 · 오래 채점하지 않은 교재
async function todayView(date) {
  const day = cleanDay(date || todayStr()), thisM = monthStart(todayStr());
  const out = await attOut(await attRows(addDays(day, -30), addDays(day, 7)));
  const sts = must(await T("tt_students").select("id,name,grade,active").order("name"));
  const mrows = await monthRows(thisM);
  const needMonth = monthTable ? sts.map((s) => ({ id: s.id, name: s.name, ...mflagOut(monthFlag(s, mrows, thisM)) })).filter((x) => x.flag) : [];
  let stale = [];
  try {
    stale = (await booksList()).flatMap((b) => b.students.filter((x) => x.active && (x.idle_days ?? 0) >= 14)
      .map((x) => ({ book: b.title, code: b.code, sid: x.sid, name: x.name, idle_days: x.idle_days, never_graded: x.never_graded, last_graded: x.last_graded, since: x.since })))
      .sort((a, b) => b.idle_days - a.idle_days);
  } catch { stale = []; }
  const qs = await anaRows("tt_questions", () => T("tt_questions").select("status,reason,reason_later"));
  return {
    date: day, today: todayStr(), ok: attTable, months_ok: monthTable, this_month: thisM,
    ask: { open: qs.filter((q) => q.status === "open").length, later: qs.filter((q) => q.status === "accepted" && q.reason_later && !q.reason).length },
    day_rows: out.filter((r) => r.day === day),
    unchecked: out.filter((r) => r.day < day && !r.checked && ATT_UNSURE.includes(r.kind)),
    upcoming: out.filter((r) => r.day > day),
    recent: out.filter((r) => r.day < day).reverse(),
    need_month: needMonth, stale_books: stale,
    students: sts.map((s) => ({ id: s.id, name: s.name, active: s.active !== false })),
  };
}

// ── 교재 분석 (supabase/2026-11_tt_book_analysis.sql) — 교재 문항(tt_book_items, 교재 자체에) · 채점 결과(tt_book_marks, 학생 교재에) · 물어볼 것(tt_questions)
//   분석은 채팅에서 Claude가 한다: 「분석 맡기기」 묶음(스캔본 + 가이드 + 지금까지 기록) → 결과 JSON → 「분석 결과 넣기」
let anaTable = true;
const ANA_SQL = "교재 분석 표가 DB에 아직 없어요 — supabase/2026-11_tt_book_analysis.sql 을 넣어야 해요";
const noAnaTable = (e) => { const t = String((e && e.message) || e || ""); return /tt_book_items|tt_book_marks|tt_questions|analyzed_at/.test(t) && /does not exist|schema cache|Could not find/i.test(t); };
const anaFail = (e) => { if (noAnaTable(e)) { anaTable = false; throw new Error(ANA_SQL); } throw e; };
const pick = (x, ks) => Object.fromEntries(ks.map((k) => [k, x[k] ?? null]));
const sameBy = (ks) => (a, b) => !!a && !!b && ks.every((k) => JSON.stringify(a[k] ?? null) === JSON.stringify(b[k] ?? null));
const snapBy = (ks, fs) => (r) => (r ? { id: r.id, ...pick(r, ks), ...pick(r, fs) } : null);
const ITEM_F = ["page", "label", "answer", "answer_src", "topic", "crop"];
const MARK_F = ["round", "result", "unsolved", "mark", "answer", "graded_by", "day", "report_day", "scan_id", "note"];
const Q_K = ["student_id", "print_id", "item_id", "mark_id", "grading_id", "seq"];
const Q_F = ["kind", "detail", "status", "answer", "reason", "reason_later", "answered_at"];
const snapItem = snapBy(["print_id"], ITEM_F), snapMark = snapBy(["print_id", "student_id", "item_id"], MARK_F), snapQ = snapBy(Q_K, Q_F);
const QKIND = { o_but_wrong: "선생님 ○인데 틀림", red_note_o: "빨간 표시 · 메모 + ○", unsolved_mark: "안 푼 문제 표시", unsure_mark: "애매한 표시", late_grade: "늦은 채점" };
async function anaRows(t, build) {
  if (!anaTable) return [];
  try { return await all(build); } catch (e) { if (noAnaTable(e)) { anaTable = false; return []; } throw e; }
}
// 스캔본 「분석함」 때 — 칸이 아직 없으면(SQL 전) 빈 것
async function analyzedMap(gid) {
  const r = gid ? await anaRows("tt_scans", () => T("tt_scans").select("id,analyzed_at").eq("grading_id", gid)) : [];
  return new Map(r.map((x) => [x.id, x.analyzed_at || null]));
}
// 문항마다 지금 결과 = 가장 늦은 차. 포스트잇 = 지금 틀림(안 풀었지만 오답 포함)인 문항, 색은 그 차(1 노랑 · 2 주황 · 3 이상 빨강)
function itemState(marks) {
  const rs = marks.slice().sort((a, b) => a.round - b.round);
  const cur = rs.length ? rs[rs.length - 1] : null;
  return { rounds: rs.map((m) => ({ id: m.id, round: m.round, result: m.result, unsolved: !!m.unsolved, mark: m.mark || "", answer: m.answer || "", day: m.day, report_day: m.report_day, graded_by: m.graded_by, scan_id: m.scan_id, note: m.note || "" })),
    cur: cur ? { round: cur.round, result: cur.result, unsolved: !!cur.unsolved, taught: cur.result === "O" && cur.mark === "box" } : null, postit: cur && cur.result === "X" ? Math.min(cur.round, 3) : null };
}
// 학생 교재 하나의 문항 · 결과 · 물어볼 것
async function bookCopyItems(code) {
  const c = await bookCopyByCode(code);
  const [items, marks, qs, scans, am] = await Promise.all([
    anaRows("tt_book_items", () => T("tt_book_items").select("*").eq("print_id", c.master.id).order("page").order("id")),
    anaRows("tt_book_marks", () => T("tt_book_marks").select("*").eq("print_id", c.x.id).order("id")),
    anaRows("tt_questions", () => T("tt_questions").select("*").eq("print_id", c.x.id).order("id")),
    c.g ? scanList(c.g.id) : [], analyzedMap(c.g ? c.g.id : null)]);
  const out = items.map((it) => ({ id: it.id, page: it.page, label: it.label, answer: it.answer || "", answer_src: it.answer_src || "", topic: it.topic || "", crop: it.crop || null,
    ...itemState(marks.filter((m) => m.item_id === it.id)) })).filter((it) => it.rounds.length);
  return { ok: anaTable, copy: c.x.code, master: c.master.code, title: c.x.title, student: { id: c.sid, name: c.st.name }, gid: c.g ? c.g.id : null,
    items: out, n_postits: out.filter((x) => x.postit).length, n_taught: out.filter((x) => x.cur && x.cur.taught).length, scans: scans.map((x) => ({ id: x.id, name: x.name, round: x.round, kind: x.kind, pages: x.pages, created_at: x.created_at, analyzed_at: am.get(x.id) || null })),
    questions: qs.filter((q) => q.status === "open" || (q.status === "accepted" && q.reason_later && !q.reason)).map((q) => ({ id: q.id, kind: q.kind, status: q.status, item_id: q.item_id })) };
}
// 「분석 맡기기」 묶음에 넣을 지금까지 기록
async function bookPackData(code, all = false) {
  const c = await bookCopyByCode(code);
  const [items, marks, logs, scans, am] = await Promise.all([
    anaRows("tt_book_items", () => T("tt_book_items").select("*").eq("print_id", c.master.id).order("page").order("id")),
    anaRows("tt_book_marks", () => T("tt_book_marks").select("*").eq("print_id", c.x.id).order("id")),
    bookLogs([c.x.id]), c.g ? scanList(c.g.id) : [], analyzedMap(c.g ? c.g.id : null)]);
  scans.forEach((x) => { x.analyzed_at = am.get(x.id) || null; });
  const pick2 = scans.filter((x) => all || !x.analyzed_at);
  const b = bookOf(c.master);
  return {
    c, scans: pick2,
    context: {
      kind: "ashrain.book.context", version: 1, made: nowIso(), today: todayStr(), copy: c.x.code,
      book: { title: c.x.title, publisher: b.publisher || "", grade: b.grade || "", master: c.master.code },
      student: { name: c.st.name, grade: c.st.grade || "" },
      items: items.map((it) => ({ page: it.page, label: it.label, answer: it.answer || "", answer_src: it.answer_src || "", topic: it.topic || "" })),
      history: items.map((it) => ({ page: it.page, label: it.label, rounds: marks.filter((m) => m.item_id === it.id).sort((a, x) => a.round - x.round)
        .map((m) => ({ round: m.round, result: m.result, unsolved: !!m.unsolved, mark: m.mark || "", day: m.day, graded_by: m.graded_by })) })).filter((h) => h.rounds.length),
      progress: logs.filter((l) => l.kind === "solved").map((l) => ({ day: l.day, page_to: l.page_to, pages: l.pages || "" })),
      graded: logs.filter((l) => l.kind === "graded").map((l) => ({ day: l.day, round: l.round, pages: l.pages || "" })),
      scans: pick2.map((x, i) => ({ file: `스캔본/${String(i + 1).padStart(2, "0")}_${x.round ? x.round + "차" : "차수모름"}${(/\.[A-Za-z0-9]{1,5}$/.exec(x.name) || [x.kind === "pdf" ? ".pdf" : ".jpg"])[0].toLowerCase()}`,
        scan_id: x.id, round: x.round ?? null, uploaded: localDay(x.created_at), pages: x.pages || 1, analyzed: !!x.analyzed_at })),
    },
  };
}
// 분석 결과 읽기 — 코드 블록 · 앞뒤 글이 섞여 있어도 JSON 한 덩어리를 찾는다
function parseResult(text) {
  const t = String(text || "").replace(/^﻿/, "").trim();
  let o = null;
  try { o = JSON.parse(t); } catch {
    const m = /```(?:json)?\s*([\s\S]*?)```/.exec(t) || /(\{[\s\S]*\})/.exec(t);
    if (m) { try { o = JSON.parse(m[1]); } catch { o = null; } }
  }
  if (!o || o.kind !== "ashrain.book.result") throw new Error("분석 결과 파일(ashrain.book.result)을 읽지 못했어요");
  return o;
}
const ROUND_OK = (r) => Number.isInteger(r) && r >= 1 && r <= 9;
const cleanLabel = (s) => String(s ?? "").trim().slice(0, 40);
// 분석 결과 넣기 — dry 면 무엇이 바뀌는지만. 넣으면 문항 · 결과 · 물어볼 것을 한 업무 기록(여러 줄)으로 남기고, 채점한 날은 교재 기록에 더한다
async function bookImport(b) {
  if (!anaTable) throw new Error(ANA_SQL);
  const o = parseResult(b.text);
  const c = await bookCopyByCode(o.copy || b.code || "");
  const today = todayStr();
  try {
    const items = await anaRows("tt_book_items", () => T("tt_book_items").select("*").eq("print_id", c.master.id));
    const marks = await anaRows("tt_book_marks", () => T("tt_book_marks").select("*").eq("print_id", c.x.id));
    const key = (pg, lb) => `${pg}|${cleanLabel(lb)}`;
    const im = new Map(items.map((it) => [key(it.page, it.label), it]));
    const scanIds = new Set(c.g ? (await scanList(c.g.id)).map((x) => x.id) : []);
    const bad = [];
    // 1) 문항
    const itemPlan = new Map();
    const wantItem = (pg, lb) => {
      const k = key(pg, lb);
      if (!itemPlan.has(k)) itemPlan.set(k, { page: pg, label: cleanLabel(lb), old: im.get(k) || null, set: {} });
      return itemPlan.get(k);
    };
    for (const it of o.items || []) {
      const pg = Number(it.page), lb = cleanLabel(it.label);
      if (!Number.isInteger(pg) || pg < 0 || pg > 9999 || !lb) { bad.push(`문항 ${it.page}쪽 ${it.label}`); continue; }
      const p = wantItem(pg, lb);
      const ans = String(it.answer ?? "").trim().slice(0, 300), src = ["claude", "teacher", "book"].includes(it.answer_src) ? it.answer_src : ans ? "claude" : "";
      if (ans && (!p.old || !p.old.answer || (p.old.answer_src !== "teacher" && p.old.answer !== ans))) { p.set.answer = ans; p.set.answer_src = src; }
      if (it.topic && (!p.old || !p.old.topic)) p.set.topic = String(it.topic).trim().slice(0, 100);
      if (it.crop && it.crop.scan_id && Array.isArray(it.crop.box) && it.crop.box.length === 4 && (!p.old || !p.old.crop)) p.set.crop = { scan_id: Number(it.crop.scan_id), page_index: Number(it.crop.page_index) || 0, box: it.crop.box.map((v) => Math.max(0, Math.min(1, Number(v) || 0))) };
    }
    // 2) 채점 결과
    const markPlan = [];
    for (const m of o.marks || []) {
      const pg = Number(m.page), lb = cleanLabel(m.label), rd = Number(m.round);
      if (!Number.isInteger(pg) || !lb || !ROUND_OK(rd) || !["O", "X", "U"].includes(m.result)) { bad.push(`결과 ${m.page}쪽 ${m.label} ${m.round}차`); continue; }
      const day = /^\d{4}-\d{2}-\d{2}$/.test(m.day || "") ? m.day : today;
      const row = { round: rd, result: m.result, unsolved: !!m.unsolved && m.result === "X", mark: String(m.mark || "").slice(0, 20), answer: String(m.answer ?? "").slice(0, 300),
        graded_by: m.graded_by === "claude" ? "claude" : "teacher", day, scan_id: scanIds.has(Number(m.scan_id)) ? Number(m.scan_id) : null, note: String(m.note || "").slice(0, 300) };
      const p = wantItem(pg, lb);
      const old = p.old ? marks.find((x) => x.item_id === p.old.id && x.round === rd) || null : null;
      markPlan.push({ p, row, old });
    }
    // 3) 물어볼 것
    const qPlan = [];
    for (const q of o.checks || []) {
      if (!QKIND[q.kind] || q.kind === "late_grade") { bad.push(`확인할 것 ${q.kind}`); continue; }
      const pg = Number(q.page), lb = cleanLabel(q.label);
      if (!Number.isInteger(pg) || !lb) { bad.push(`확인할 것 ${q.page}쪽 ${q.label}`); continue; }
      qPlan.push({ p: wantItem(pg, lb), q });
    }
    const nNewItems = [...itemPlan.values()].filter((p) => !p.old).length;
    const markChanged = markPlan.filter((x) => !x.old || !sameBy(MARK_F)(x.old, { ...x.old, ...x.row, report_day: x.old.report_day }));
    const summary = { items_new: nNewItems, items_changed: [...itemPlan.values()].filter((p) => p.old && Object.keys(p.set).length).length,
      marks_new: markChanged.filter((x) => !x.old).length, marks_changed: markChanged.filter((x) => x.old).length, marks_same: markPlan.length - markChanged.length,
      checks: qPlan.length, postits_after: null, scans: (o.analyzed_scans || []).filter((id) => scanIds.has(Number(id))).length, graded_days: (o.graded_days || []).length, skipped: bad };
    if (b.dry) return { ok: true, dry: true, copy: c.x.code, title: c.x.title, student: c.st.name, summary };
    // 넣기
    const rows = [];
    for (const p of itemPlan.values()) {
      if (!p.old) {
        const saved = must(await T("tt_book_items").insert({ print_id: c.master.id, page: p.page, label: p.label, ...p.set }).select("*").single());
        p.id = saved.id; rows.push({ table: "tt_book_items", row_id: saved.id, before: null, after: snapItem(saved) });
      } else {
        p.id = p.old.id;
        if (Object.keys(p.set).length) {
          const saved = must(await T("tt_book_items").update({ ...p.set, updated_at: nowIso() }).eq("id", p.old.id).select("*").single());
          rows.push({ table: "tt_book_items", row_id: saved.id, before: snapItem(p.old), after: snapItem(saved) });
        }
      }
    }
    const markIds = new Map();
    for (const x of markPlan) {
      if (x.old && !markChanged.includes(x)) { markIds.set(`${x.p.id}|${x.row.round}`, x.old.id); continue; }
      const saved = x.old ? must(await T("tt_book_marks").update({ ...x.row, updated_at: nowIso() }).eq("id", x.old.id).select("*").single())
        : must(await T("tt_book_marks").insert({ print_id: c.x.id, student_id: c.sid, item_id: x.p.id, ...x.row }).select("*").single());
      markIds.set(`${x.p.id}|${x.row.round}`, saved.id);
      rows.push({ table: "tt_book_marks", row_id: saved.id, before: snapMark(x.old), after: snapMark(saved) });
    }
    for (const { p, q } of qPlan) {
      const rd = ROUND_OK(Number(q.round)) ? Number(q.round) : null;
      const detail = { page: p.page, label: p.label, round: rd, why: String(q.why || "").slice(0, 500), student_answer: String(q.student_answer ?? "").slice(0, 200),
        correct_answer: String(q.correct_answer ?? "").slice(0, 200), candidates: Array.isArray(q.candidates) ? q.candidates.slice(0, 4) : undefined, scan_id: q.scan_id ?? null, title: c.x.title };
      const saved = must(await T("tt_questions").insert({ kind: q.kind, student_id: c.sid, print_id: c.x.id, item_id: p.id, mark_id: rd ? markIds.get(`${p.id}|${rd}`) || null : null, detail }).select("*").single());
      rows.push({ table: "tt_questions", row_id: saved.id, before: null, after: snapQ(saved) });
    }
    const analyzed = (o.analyzed_scans || []).map(Number).filter((id) => scanIds.has(id));
    if (analyzed.length) must(await T("tt_scans").update({ analyzed_at: nowIso() }).in("id", analyzed));
    const events = [];
    const eid = await logRow("book_import", c.sid, c.x.id, { table: "multi", rows, title: c.x.title, summary: { ...summary, skipped: bad.length } });
    if (eid) events.push(eid);
    for (const g of o.graded_days || []) {                // 채점한 날 → 교재 기록
      if (!/^\d{4}-\d{2}-\d{2}$/.test(g.day || "")) continue;
      try { events.push(...(await bookLogPut(c, { kind: "graded", day: g.day, round: ROUND_OK(Number(g.round)) ? Number(g.round) : null, pages: String(g.pages || "") })).events); } catch { /* 쪽을 못 읽으면 건너뜀 */ }
    }
    return { ok: true, copy: c.x.code, master: c.master.code, summary, events };
  } catch (e) { anaFail(e); }
}
// 포스트잇 문항 바로 매기기 — 다음 차(또는 고른 차)를 오늘 날짜 · 선생님 채점으로
async function bookMarkSet(b) {
  if (!anaTable) throw new Error(ANA_SQL);
  const c = await bookCopyByCode(b.copy);
  try {
    const it = must(await T("tt_book_items").select("*").eq("id", Number(b.item_id)).eq("print_id", c.master.id).maybeSingle());
    if (!it) throw new Error("그런 문항이 없어요");
    const rd = Number(b.round);
    if (!ROUND_OK(rd) || !["O", "X", "U", "T"].includes(b.result)) throw new Error("몇 차 · 결과를 골라 주세요");
    const old = must(await T("tt_book_marks").select("*").eq("print_id", c.x.id).eq("item_id", it.id).eq("round", rd).maybeSingle());
    // T = 풀어 줌(맞음 + 표시 box). 다른 결과로 바꾸면 box 표시는 뗌
    const mk = b.result === "T" ? "box" : old && old.mark !== "box" ? old.mark : "";
    const row = { result: b.result === "T" ? "O" : b.result, unsolved: !!b.unsolved && b.result === "X", graded_by: "teacher", day: cleanDay(b.day || todayStr()), mark: mk, note: old ? old.note : "" };
    if (old && sameBy(MARK_F)(old, { ...old, ...row })) return { ok: true, events: [] };
    const saved = old ? must(await T("tt_book_marks").update({ ...row, updated_at: nowIso() }).eq("id", old.id).select("*").single())
      : must(await T("tt_book_marks").insert({ print_id: c.x.id, student_id: c.sid, item_id: it.id, round: rd, ...row }).select("*").single());
    const eid = await logRow("book_mark", c.sid, c.x.id, { table: "tt_book_marks", row_id: saved.id, title: c.x.title, page: it.page, label: it.label, before: snapMark(old), after: snapMark(saved) });
    return { ok: true, events: eid ? [eid] : [] };
  } catch (e) { anaFail(e); }
}
// 물어볼 것 목록 — 열린 것 · 이유를 나중에 적기로 한 것 · 모은 이유
async function questionsView() {
  const qs = await anaRows("tt_questions", () => T("tt_questions").select("*").order("id", { ascending: false }).limit(1000));
  const sm = await studentsMap(qs.map((q) => q.student_id));
  const pids = [...new Set(qs.map((q) => q.print_id).filter(Boolean))], iids = [...new Set(qs.map((q) => q.item_id).filter(Boolean))], mids = [...new Set(qs.map((q) => q.mark_id).filter(Boolean))];
  const [ps, its, ms] = await Promise.all([
    pids.length ? must(await T("tt_prints").select("id,code,title,options").in("id", pids)) : [],
    iids.length ? anaRows("tt_book_items", () => T("tt_book_items").select("*").in("id", iids)) : [],
    mids.length ? anaRows("tt_book_marks", () => T("tt_book_marks").select("*").in("id", mids)) : []]);
  const pm = new Map(ps.map((x) => [x.id, x])), itm = new Map(its.map((x) => [x.id, x])), mm = new Map(ms.map((x) => [x.id, x]));
  const out = qs.map((q) => {
    const p = pm.get(q.print_id), it = itm.get(q.item_id), mk = mm.get(q.mark_id), bk = bookOf(p);
    return { id: q.id, kind: q.kind, kind_ko: QKIND[q.kind], status: q.status, detail: q.detail || {}, answer: q.answer, reason: q.reason || "", reason_later: !!q.reason_later,
      created_at: q.created_at, answered_at: q.answered_at, sid: q.student_id, name: sm.get(q.student_id)?.name || "?",
      copy: p ? p.code : null, master: bk ? bk.master_code || "" : "", title: p ? p.title : "",
      item: it ? { id: it.id, page: it.page, label: it.label, answer: it.answer || "", crop: it.crop || null } : null,
      mark: mk ? { id: mk.id, round: mk.round, result: mk.result, unsolved: !!mk.unsolved, mark: mk.mark || "", answer: mk.answer || "", day: mk.day } : null };
  });
  return { ok: anaTable, open: out.filter((q) => q.status === "open"), later: out.filter((q) => q.status === "accepted" && q.reason_later && !q.reason),
    reasons: out.filter((q) => q.status === "accepted" && q.reason), done: out.filter((q) => q.status !== "open").slice(0, 100) };
}
// 물어볼 것에 답하기 — fix(내 실수: 틀림으로) · accept(맞다고 인정 + 이유 · 나중에) · reason(이유만 적기) · set(결과 고르기: O · X · U · T 풀어 줌 · wrong_unsolved) · dismiss
async function questionAnswer(id, b) {
  if (!anaTable) throw new Error(ANA_SQL);
  try {
    const q = must(await T("tt_questions").select("*").eq("id", id).maybeSingle());
    if (!q) throw new Error("그런 물어볼 것이 없어요");
    const rows = [];
    const setMark = async (patch) => {
      if (!q.mark_id) return;
      const old = must(await T("tt_book_marks").select("*").eq("id", q.mark_id).maybeSingle());
      if (!old || sameBy(MARK_F)(old, { ...old, ...patch })) return;
      const saved = must(await T("tt_book_marks").update({ ...patch, updated_at: nowIso() }).eq("id", old.id).select("*").single());
      rows.push({ table: "tt_book_marks", row_id: saved.id, before: snapMark(old), after: snapMark(saved) });
    };
    const up = { updated_at: nowIso() };
    const reason = String(b.reason || "").trim().slice(0, 1000);
    if (b.action === "fix") { await setMark({ result: "X", unsolved: false, note: "선생님 실수로 고침" }); Object.assign(up, { status: "fixed", answer: { action: "fix" }, answered_at: nowIso() }); }
    else if (b.action === "accept") Object.assign(up, { status: "accepted", answer: { action: "accept" }, reason, reason_later: !reason, answered_at: nowIso() });
    else if (b.action === "reason") { if (!reason) throw new Error("이유를 적어 주세요"); Object.assign(up, { reason, reason_later: false }); }
    else if (b.action === "set") {
      const v = b.result;
      if (!["O", "X", "U", "T", "wrong_unsolved"].includes(v)) throw new Error("결과를 골라 주세요");
      await setMark(v === "wrong_unsolved" ? { result: "X", unsolved: true } : v === "T" ? { result: "O", unsolved: false, mark: "box" } : { result: v, unsolved: false });
      Object.assign(up, { status: "answered", answer: { action: "set", result: v }, answered_at: nowIso() });
    } else if (b.action === "dismiss") Object.assign(up, { status: "dismissed", answer: { action: "dismiss" }, answered_at: nowIso() });
    else throw new Error("무엇을 할지 몰라요");
    const saved = must(await T("tt_questions").update(up).eq("id", q.id).select("*").single());
    rows.push({ table: "tt_questions", row_id: saved.id, before: snapQ(q), after: snapQ(saved) });
    const eid = await logRow("question", q.student_id, q.print_id, { table: "multi", rows, title: (q.detail || {}).title || "", kind: q.kind,
      summary: { action: b.action, page: (q.detail || {}).page, label: (q.detail || {}).label } });
    return { ok: true, events: eid ? [eid] : [] };
  } catch (e) { anaFail(e); }
}

// ── 되돌리기 — 지금 모습이 그 기록의 「후」와 같을 때만 「전」으로 돌린다(그 뒤에 또 바뀌었으면 막음). 되돌릴 수 있는 표:
const UNDO = {
  tt_book_logs: {
    fields: (x) => ({ day: x.day, page_to: x.page_to ?? null, pages: x.pages || "", round: x.round ?? null, note: x.note || "" }),
    keys: (ev, x) => ({ print_id: ev.print_id, student_id: ev.student_id, kind: x.kind }), same: sameLog, snap: snapLog, missing: noLogTable, sql: LOG_SQL, where: "교재 화면",
  },
  tt_student_months: {
    fields: (x) => ({ month: x.month, status: x.status, fee: x.fee ?? null, note: x.note || "", ...(perWeekCol ? { per_week: x.per_week ?? null } : {}) }),
    keys: (ev) => ({ student_id: ev.student_id }), same: sameMonth, snap: snapMonth, missing: noMonthTable, sql: MONTH_SQL, where: "재원 · 원비 화면",
    after: (ev) => syncActive(ev.student_id),
  },
  tt_attendance: {
    fields: (x) => ({ day: x.day, kind: x.kind, reason: x.reason || "", checked: x.checked ?? null, checked_at: x.checked ? nowIso() : null, source: x.source || "teacher" }),
    keys: (ev) => ({ student_id: ev.student_id }), same: sameAtt, snap: snapAtt, missing: noAttTable, sql: ATT_SQL, where: "오늘 화면",
  },
  tt_fee_plans: { fields: (x) => pick(x, FEE_F), keys: () => ({}), same: sameFee, snap: snapFee, missing: noFeeTable, sql: FEE_SQL, where: "원비표" },
  tt_book_items: { fields: (x) => pick(x, ITEM_F), keys: (ev, x) => ({ print_id: x.print_id }), same: sameBy(ITEM_F), snap: snapItem, missing: noAnaTable, sql: ANA_SQL, where: "교재 문항 화면" },
  tt_book_marks: { fields: (x) => pick(x, MARK_F), keys: (ev, x) => pick(x, ["print_id", "student_id", "item_id"]), same: sameBy(MARK_F), snap: snapMark, missing: noAnaTable, sql: ANA_SQL, where: "교재 문항 화면" },
  tt_questions: { fields: (x) => pick(x, Q_F), keys: (ev, x) => pick(x, Q_K), same: sameBy(Q_F), snap: snapQ, missing: noAnaTable, sql: ANA_SQL, where: "물어볼 것 화면" },
};
// 한 줄 되돌리기 — 지금 모습이 그 줄의 「후」와 같은지 본 뒤 「전」으로 돌린다
async function undoCheck(r) {
  const U = UNDO[r.table];
  const cur = r.row_id ? must(await T(r.table).select("*").eq("id", r.row_id).maybeSingle()) : null;
  return { U, cur, ok: r.after ? U.same(cur, r.after) : !cur };
}
async function undoApply(r, ev, cur) {
  const U = UNDO[r.table];
  let restored = null;
  if (!r.before) { if (cur) must(await T(r.table).delete().eq("id", cur.id)); }
  else if (!r.after) {
    const x = await T(r.table).insert({ ...U.keys(ev, r.before), ...U.fields(r.before) }).select("*").single();
    if (x.error && /duplicate|unique/i.test(x.error.message || "")) throw new Error(`같은 기록이 이미 있어서 되돌릴 수 없어요 — ${U.where}에서 고쳐 주세요`);
    restored = must(x);
  } else restored = must(await T(r.table).update({ ...U.fields(r.before), updated_at: nowIso() }).eq("id", cur.id).select("*").single());
  if (U.after) await U.after(ev, restored);
  return { table: r.table, row_id: (restored || cur) ? (restored || cur).id : r.row_id, before: U.snap(cur), after: U.snap(restored) };
}
// 기록 하나(한 줄 또는 여러 줄 = table "multi") 되돌리기 — 여러 줄은 모두 되돌릴 수 있을 때만
async function undoEvent(id) {
  const ev = must(await T("tt_events").select("*").eq("id", id).maybeSingle());
  if (!ev) throw new Error("그런 기록이 없어요");
  const d = ev.detail || {};
  if (d.undone_by) throw new Error("이미 되돌린 기록이에요");
  if (ev.kind === "grading_pass") {               // 넘어가기 되돌리기 — DB 함수가 넘기기 전 상태로(그 뒤 다시 열었으면 안 됨)
    const r = await passFn(() => rpc("tt_unpass_grading", { p_event: ev.id }));
    return r && r.event;
  }
  const rows = d.table === "multi" ? d.rows || [] : [{ table: d.table, row_id: d.row_id, before: d.before, after: d.after }];
  if (!rows.length || rows.some((r) => !UNDO[r.table])) throw new Error("이 기록은 되돌릴 수 없어요");
  try {
    const plan = [];
    for (const r of [...rows].reverse()) {              // 나중에 바뀐 줄부터
      const c = await undoCheck(r);
      if (!c.ok) throw new Error(`그 뒤에 또 바뀌어서 되돌릴 수 없어요 — ${c.U.where}에서 고쳐 주세요`);
      plan.push([r, c.cur]);
    }
    const out = [];
    for (const [r, cur] of plan) out.push(await undoApply(r, ev, cur));
    const keep = Object.fromEntries(["title", "name", "kind", "month", "day", "summary"].filter((k) => k in d).map((k) => [k, d[k]]));
    const nd = d.table === "multi" ? { ...keep, table: "multi", rows: out.reverse(), undo_of: ev.id } : { ...keep, ...out[0], undo_of: ev.id };
    const nid = await logRow(ev.kind, ev.student_id, ev.print_id, nd);
    must(await T("tt_events").update({ detail: { ...d, undone_by: nid || -1, undone_at: nowIso() } }).eq("id", ev.id));
    return nid;
  } catch (e) {
    const U = rows.map((r) => UNDO[r.table]).find((u) => u.missing(e));
    if (U) throw new Error(U.sql);
    throw e;
  }
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
const RES_KO = { O: "맞음", X: "틀림", U: "안 풂", P: "넘어감", T: "풀어 줌(맞음)", "": "안 매김" };
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
        results: { graded: res.filter((x) => x && x !== "P").length, O: res.filter((x) => x === "O").length, X: res.filter((x) => x === "X").length, U: res.filter((x) => x === "U").length, P: res.filter((x) => x === "P").length },
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
      const fin = m.result === "O" && m.taught ? "T" : m.result || "";
      return { no: it.seq, label: it.label || String(it.src_no || it.seq), choice: !!it.choice, answer: ansText(it), final: fin,
        final_ko: RES_KO[fin], given: m.answer || "", rounds: it.rounds, repeat_wrong: !!it.repeat, wrong_before: it.wrong_before || 0,
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
  if (p === "feeplans") return post ? feePlanSave(body) : feePlans();                // 원비표
  if (p === "today") return todayView(q.date);                                        // 오늘 대시보드
  if ((m = /^bookcopy\/([A-Za-z0-9-]+)$/.exec(p)) && !post) return bookCopyItems(m[1]);     // 학생 교재 문항 · 포스트잇
  if ((m = /^bookcopy\/([A-Za-z0-9-]+)\/pack$/.exec(p))) {                                   // 분석 맡기기 묶음
    const d = await bookPackData(m[1], !!(body && body.all));
    return (await engine()).exportBookPack(d, ctx());
  }
  if (p === "books/import" && post) return bookImport(body);                         // 분석 결과 넣기(dry = 미리 보기)
  if (p === "bookmarks" && post) return bookMarkSet(body);                            // 포스트잇 문항 바로 매기기
  if (p === "questions" && !post) return questionsView();                             // 물어볼 것
  if ((m = /^questions\/(\d+)$/.exec(p)) && post) return questionAnswer(Number(m[1]), body);
  if (p === "attendance" && post) return attPut(body);                                // 결석부 적기
  if ((m = /^attendance\/(\d+)$/.exec(p)) && post) return attEdit(Number(m[1]), body);  // 당일 확인 · 고치기 · 지우기
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
    if (!["O", "X", "U", "T", ""].includes(result)) throw new Error("result");
    try { await rpc("tt_mark", { p_grading: gid, p_seq: Number(body.seq), p_result: result, p_answer: body.answer || "" }); }
    catch (e) { if (result === "T" && /tt_marks_result_check|taught|check constraint/i.test(String(e.message || e))) throw new Error(TAUGHT_SQL); throw e; }
    if (body.mode) await T("tt_gradings").update({ mode: body.mode }).eq("id", gid);
    if (body.light) return { ok: true };            // 화면이 먼저 적어 두고 차례로 보내는 경우 — 다 보낸 뒤 한 번만 다시 읽는다
    return gradingDetail(gid);
  }
  // 앞 차(1차 …) 결과 고치기 — 다음 차를 시작한 뒤에도 (supabase/2026-11_tt_round_fix.sql 의 tt_mark_round · tt_retry_add)
  if ((m = /^gradings\/(\d+)\/fix$/.exec(p))) {
    const gid = Number(m[1]);
    const result = String(body.result || "");
    if (!["O", "X", "U", "T"].includes(result)) throw new Error("앞 차 결과는 O · X · 안 풂 · 풀어 줌 중에서 골라 바꿔요");
    const r = await roundFn(() => rpc("tt_mark_round", { p_grading: gid, p_round: Number(body.round), p_seq: Number(body.seq), p_result: result, p_answer: body.answer ?? null }))
      .catch((e) => { if (result === "T" && /O · X · 안 풂 중|taught|check constraint/i.test(String(e.message || e))) throw new Error(TAUGHT_SQL); throw e; });
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
  // 푼 만큼만 매기고 넘어가기(패스) — 남은 문항을 넘어감(1차) · 이번 차에서 뺌(2차부터)으로 두고 끝냄 (supabase/2026-11_tt_pass.sql)
  if ((m = /^gradings\/(\d+)\/pass$/.exec(p)) && post) {
    const seqs = [...new Set((body.seqs || []).map(Number).filter(Number.isInteger))];
    if (!seqs.length) throw new Error("넘길 문항이 없어요");
    return passFn(() => rpc("tt_pass_grading", { p_grading: Number(m[1]), p_seqs: seqs }));
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
async function passFn(call) {
  try { return await call(); } catch (e) {
    const msg = e.message || "";
    if (/tt_(un)?pass_grading/.test(msg) && /function|schema cache/i.test(msg)) throw new Error(PASS_SQL);
    if (/tt_marks_result_check/.test(msg)) throw new Error(PASS_SQL);
    throw e;
  }
}
const PASS_SQL = "DB에 「넘어가기」가 아직 없어요 — supabase/2026-11_tt_pass.sql 을 넣어야 해요";
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

// 스캔본 한 쪽 그림(문항 그림 자리 보기) — PDF면 그 쪽을 그림으로, 사진이면 그대로. 한 번 만든 것은 기억
const scanImgCache = new Map();
export async function scanImage(scanId, pageIndex = 0) {
  const k = `${scanId}:${pageIndex}`;
  if (!scanImgCache.has(k)) scanImgCache.set(k, (async () => {
    const r = must(await T("tt_scans").select("path,mime,name").eq("id", Number(scanId)).single());
    const buf = await bytes(r.path);
    if (/pdf/.test(r.mime || "") || /\.pdf$/i.test(r.name || "")) return (await engine()).renderPagePng(buf, Number(pageIndex) + 1, 2);
    return new Blob([buf], { type: r.mime || "image/jpeg" });
  })());
  try { return await scanImgCache.get(k); } catch (e) { scanImgCache.delete(k); throw e; }
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
