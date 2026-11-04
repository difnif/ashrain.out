// src/pages/AdminContest.jsx — 경시 대비 (해시 라우트: #/admin/contest, admin 전용)
// ① 학생 등록 → ② 프린트 골라 답안 입력·채점 → ③ 채점한 프린트로 오답 프린트 생성(→ ②에서 다시 채점)
// → ④ 분석할 프린트 골라 분석 파일 추출 · 채팅방 분석을 다듬어 브리핑 입력.  ⑤ 프린트 관리(JSON 가져오기·파일).
// 앱은 AI 를 부르지 않는다. 규격: docs/SPEC-contest-v1.md
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/authx";
import { readZip } from "../lib/unzip";
import {
  HALVES, validatePackage, packageToRows, judge, gradeAll, takerCode, setLabel,
  collectWrong, wrongPrintRows, printHtml, buildStudentExport,
} from "../lib/contest";

const TABS = [["takers", "① 학생"], ["grade", "② 채점"], ["wrong", "③ 오답 프린트"], ["analyze", "④ 분석·브리핑"], ["prints", "프린트 관리"]];
const today = () => new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);

export default function AdminContest() {
  const [ok, setOk] = useState(null);
  const [missing, setMissing] = useState(false);
  const [tab, setTab] = useState("takers");
  const [sets, setSets] = useState([]);
  const [takers, setTakers] = useState([]);
  const [attempts, setAttempts] = useState([]);
  const [tid, setTid] = useState("");

  useEffect(() => {
    (async () => {
      const { data: s } = await supabase.auth.getSession();
      if (!s?.session) { setOk(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", s.session.user.id).maybeSingle();
      setOk(p?.role === "admin");
      if (p?.role === "admin") loadAll();
    })();
  }, []);

  const loadAll = async () => {
    const [a, b, c] = await Promise.all([
      supabase.from("contest_sets").select("id, code, kind, title, contest, year, half, grade_label, test_date, taker_id, parent_ids, n_items, max_score, files, created_at").order("created_at", { ascending: false }),
      supabase.from("contest_takers").select("id, seq, name, grade, phone4, memo").order("name"),
      supabase.from("contest_attempts").select("*"),
    ]);
    if (a.error) { setMissing(true); return; }
    setSets(a.data || []); setTakers(b.data || []); setAttempts(c.data || []);
  };

  const taker = takers.find((t) => t.id === tid) || null;
  const setById = useMemo(() => new Map(sets.map((s) => [s.id, s])), [sets]);

  if (ok === null) return null;
  if (ok === false) return <div className="cx-wrap"><Style /><p className="cx-err">관리자만 접근할 수 있어요.</p></div>;

  return (
    <div className="cx-wrap"><Style />
      <h2 className="cx-title">🏆 경시 대비</h2>
      {missing && <p className="cx-err">표가 아직 없어요 — supabase/2026-11_contest.sql 을 SQL Editor 에서 실행해 주세요.</p>}
      <div className="cx-tabs">
        {TABS.map(([k, l]) => <button key={k} className={"cx-tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>)}
      </div>
      {["grade", "wrong", "analyze"].includes(tab) && (
        <TakerBar takers={takers} tid={tid} setTid={setTid} attempts={attempts} />
      )}

      {tab === "takers" && <TakersView takers={takers} attempts={attempts} reload={loadAll} pick={(id) => { setTid(id); setTab("grade"); }} />}
      {tab === "grade" && taker && <GradeView taker={taker} sets={sets} attempts={attempts} reload={loadAll} />}
      {tab === "wrong" && taker && <WrongView taker={taker} sets={sets} attempts={attempts} setById={setById} reload={loadAll} />}
      {tab === "analyze" && taker && <AnalyzeView taker={taker} sets={sets} attempts={attempts} setById={setById} />}
      {tab === "prints" && <PrintsView sets={sets.filter((s) => s.kind === "original")} reload={loadAll} />}
    </div>
  );
}

// ── 학생 고르기 (②③④ 공통) ───────────────────────────────────────────────
function TakerBar({ takers, tid, setTid, attempts }) {
  const n = (id) => attempts.filter((a) => a.taker_id === id).length;
  return (
    <div className="cx-card">
      <select className="cx-sel" value={tid} onChange={(e) => setTid(e.target.value)}>
        <option value="">— 학생 선택 —</option>
        {takers.map((t) => <option key={t.id} value={t.id}>{t.name} · {t.grade || "학년 —"} · {t.phone4 || "----"} (채점 {n(t.id)})</option>)}
      </select>
      {!tid && <p className="cx-hint">학생을 먼저 골라 주세요. 없으면 ① 학생 탭에서 등록해요.</p>}
    </div>
  );
}

// ── ① 학생 ───────────────────────────────────────────────────────────────
function TakersView({ takers, attempts, reload, pick }) {
  const [f, setF] = useState({ name: "", grade: "", phone4: "" });
  const [q, setQ] = useState("");
  const [msg, setMsg] = useState("");
  const add = async () => {
    const name = f.name.trim(), phone4 = f.phone4.trim();
    if (!name) { setMsg("이름을 써 주세요."); return; }
    if (!/^\d{4}$/.test(phone4)) { setMsg("전화번호 뒷자리 4자리를 써 주세요."); return; }
    const { error } = await supabase.from("contest_takers").insert({ name, grade: f.grade.trim(), phone4 });
    if (error) { setMsg(error.code === "23505" ? "같은 이름·뒷자리 학생이 이미 있어요." : error.message); return; }
    setF({ name: "", grade: "", phone4: "" }); setMsg(""); reload();
  };
  const edit = async (t) => {
    const grade = window.prompt(`${t.name} 학년`, t.grade || "");
    if (grade == null) return;
    await supabase.from("contest_takers").update({ grade: grade.trim() }).eq("id", t.id);
    reload();
  };
  const del = async (t) => {
    if (!window.confirm(`${t.name} 학생과 채점·오답 프린트·브리핑을 모두 지울까요?`)) return;
    await supabase.from("contest_takers").delete().eq("id", t.id);
    reload();
  };
  const shown = takers.filter((t) => !q.trim() || (t.name + t.grade + t.phone4).includes(q.trim()));
  return (
    <>
      <div className="cx-card">
        <h3 className="cx-sub">분석 대상 등록</h3>
        <p className="cx-hint">앱 회원과 상관없이 직접 적어 등록해요. 앱에 가입하지 않은 학생도 됩니다.</p>
        <div className="cx-row">
          <input className="cx-in" placeholder="이름" value={f.name} onChange={(e) => setF({ ...f, name: e.target.value })} />
          <input className="cx-in cx-short" placeholder="학년" value={f.grade} onChange={(e) => setF({ ...f, grade: e.target.value })} />
          <input className="cx-in cx-short" placeholder="뒷자리" inputMode="numeric" maxLength={4} value={f.phone4} onChange={(e) => setF({ ...f, phone4: e.target.value.replace(/\D/g, "") })} />
          <button className="cx-btn cx-primary" onClick={add}>등록</button>
        </div>
        {msg && <p className="cx-err">{msg}</p>}
      </div>
      <div className="cx-card">
        <div className="cx-row cx-between">
          <h3 className="cx-sub">학생 {takers.length}명</h3>
          <input className="cx-in cx-search" placeholder="찾기" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        {shown.map((t) => (
          <div key={t.id} className="cx-line">
            <button className="cx-link" onClick={() => pick(t.id)}><b>{t.name}</b> <span className="cx-muted">{t.grade || "학년 —"} · {t.phone4} · {takerCode(t)} · 채점 {attempts.filter((a) => a.taker_id === t.id).length}</span></button>
            <button className="cx-btn cx-mini" onClick={() => edit(t)}>학년</button>
            <button className="cx-btn cx-mini" onClick={() => del(t)}>삭제</button>
          </div>
        ))}
        {!shown.length && <p className="cx-hint">학생이 없어요.</p>}
      </div>
    </>
  );
}

// ── ② 채점 ───────────────────────────────────────────────────────────────
function GradeView({ taker, sets, attempts, reload }) {
  const years = [...new Set(sets.filter((s) => s.kind === "original").map((s) => s.year).filter(Boolean))].sort((a, b) => b - a);
  const [year, setYear] = useState("");
  const [half, setHalf] = useState("");
  const [sid, setSid] = useState("");
  const [items, setItems] = useState([]);
  const [ans, setAns] = useState({});
  const [day, setDay] = useState(today());
  const [result, setResult] = useState(null);
  const [msg, setMsg] = useState("");

  const choices = sets.filter((s) =>
    (s.kind === "original" && (!year || String(s.year) === year) && (!half || s.half === half))
    || (s.kind === "wrong" && s.taker_id === taker.id && !year && !half));
  const done = (id) => attempts.find((a) => a.set_id === id && a.taker_id === taker.id);

  useEffect(() => { setSid(""); }, [taker.id]);
  useEffect(() => {
    setResult(null); setMsg("");
    if (!sid) { setItems([]); return; }
    (async () => {
      const [{ data: it }, { data: rs }] = await Promise.all([
        supabase.from("contest_items").select("no, points, answer_type, n_choices, accept").eq("set_id", sid).order("no"),
        supabase.from("contest_responses").select("item_no, response").eq("set_id", sid).eq("taker_id", taker.id),
      ]);
      setItems(it || []);
      const a = {};
      for (const r of rs || []) a[r.item_no] = r.response ?? "";
      setAns(a);
      const at = done(sid);
      setDay(at?.taken_on || today());
      if (at) setResult(gradeAll(it || [], a));
    })();
  }, [sid, taker.id]);

  const grade = async () => {
    const g = gradeAll(items, ans);
    const now = new Date().toISOString();
    const { error } = await supabase.from("contest_responses").upsert(g.rows.map((r) => ({ ...r, set_id: sid, taker_id: taker.id, updated_at: now })));
    if (error) { setMsg("저장 실패: " + error.message); return; }
    const { error: e2 } = await supabase.from("contest_attempts").upsert({
      set_id: sid, taker_id: taker.id, taken_on: day || null, score: g.score, max_score: g.max,
      n_right: g.right, n_wrong: g.wrong, n_blank: g.blank, graded_at: now,
    });
    if (e2) { setMsg("채점 기록 실패: " + e2.message); return; }
    setResult(g); setMsg("채점했어요."); reload();
  };
  const ungrade = async () => {
    if (!window.confirm("이 프린트의 답안·채점을 지울까요?")) return;
    await supabase.from("contest_responses").delete().eq("set_id", sid).eq("taker_id", taker.id);
    await supabase.from("contest_attempts").delete().eq("set_id", sid).eq("taker_id", taker.id);
    setAns({}); setResult(null); reload();
  };
  const fillLine = (line) => {
    const parts = line.trim().split(/[\s,]+/).filter(Boolean);
    const a = {};
    items.forEach((x, i) => { a[x.no] = parts[i] === "-" ? "" : (parts[i] ?? ""); });
    setAns(a); setResult(null);
  };

  const set = sets.find((s) => s.id === sid);
  return (
    <>
      <div className="cx-card">
        <h3 className="cx-sub">프린트 선택</h3>
        <div className="cx-row">
          <select className="cx-sel" value={year} onChange={(e) => setYear(e.target.value)}>
            <option value="">연도 전체</option>{years.map((y) => <option key={y} value={y}>{y}</option>)}
          </select>
          <select className="cx-sel" value={half} onChange={(e) => setHalf(e.target.value)}>
            <option value="">상·하반기</option>{HALVES.map((h) => <option key={h} value={h}>{h}</option>)}
          </select>
        </div>
        <div className="cx-list">
          {choices.map((s) => {
            const at = done(s.id);
            return (
              <button key={s.id} className={"cx-set" + (s.id === sid ? " on" : "")} onClick={() => setSid(s.id)} disabled={!s.n_items}>
                <b>{s.kind === "wrong" ? "📝 " : ""}{setLabel(s)}</b>
                <span className="cx-muted">{s.code} · {s.n_items ? `${s.n_items}문항` : "문항 대기"}{at ? ` · ✔ 채점 ${at.score}/${at.max_score}` : ""}</span>
              </button>
            );
          })}
          {!choices.length && <p className="cx-hint">맞는 프린트가 없어요.</p>}
        </div>
        <p className="cx-hint">📝 = 이 학생의 오답 프린트 (연도·반기 필터를 비우면 보여요)</p>
      </div>

      {set && items.length > 0 && (
        <div className="cx-card">
          <div className="cx-row cx-between">
            <h3 className="cx-sub">{taker.name} · {set.code}</h3>
            <label className="cx-muted">응시일 <input type="date" className="cx-in cx-date" value={day} onChange={(e) => setDay(e.target.value)} /></label>
          </div>
          <input className="cx-in" placeholder="한 줄로 입력: 3 5 12 - 4 … (빈칸은 -)" onKeyDown={(e) => { if (e.key === "Enter") { fillLine(e.currentTarget.value); e.currentTarget.value = ""; } }} />
          <div className="cx-grid">
            {items.map((x) => {
              const c = result ? judge(x, ans[x.no]) : undefined;
              return (
                <label key={x.no} className={"cx-cell" + (c === true ? " good" : c === false ? " bad" : c === null ? " blank" : "")}>
                  <span>{x.no}{result && c !== true ? ` (${x.accept[0]})` : ""}</span>
                  <input inputMode={x.answer_type === "text" ? "text" : "numeric"} value={ans[x.no] ?? ""}
                    onChange={(e) => { setAns({ ...ans, [x.no]: e.target.value }); setResult(null); }} />
                </label>
              );
            })}
          </div>
          <div className="cx-row">
            <button className="cx-btn cx-primary" onClick={grade}>채점</button>
            {done(sid) && <button className="cx-btn cx-mini" onClick={ungrade}>채점 지우기</button>}
            {result && <span className="cx-score">{result.score}/{result.max}점 · 정답 {result.right} · 오답 {result.wrong} · 무응답 {result.blank}</span>}
          </div>
          {msg && <p className="cx-hint">{msg}</p>}
        </div>
      )}
    </>
  );
}

// ── ③ 오답 프린트 ────────────────────────────────────────────────────────
function WrongView({ taker, sets, attempts, setById, reload }) {
  const mine = attempts.filter((a) => a.taker_id === taker.id).map((a) => ({ a, s: setById.get(a.set_id) })).filter((x) => x.s)
    .sort((x, y) => String(y.a.graded_at).localeCompare(String(x.a.graded_at)));
  const [pick, setPick] = useState(new Set());
  const [preview, setPreview] = useState(null);
  const [perPage, setPerPage] = useState(2);
  const [msg, setMsg] = useState("");
  const wrongSets = sets.filter((s) => s.kind === "wrong" && s.taker_id === taker.id);

  useEffect(() => { setPick(new Set()); setPreview(null); }, [taker.id]);

  const load = async (ids) => {
    const [{ data: it }, { data: rs }] = await Promise.all([
      supabase.from("contest_items").select("*").in("set_id", ids).order("no"),
      supabase.from("contest_responses").select("set_id, item_no, response, is_correct").in("set_id", ids).eq("taker_id", taker.id),
    ]);
    return ids.map((id) => ({
      set: setById.get(id),
      items: (it || []).filter((x) => x.set_id === id),
      responses: (rs || []).filter((r) => r.set_id === id),
    }));
  };
  const toggle = (id) => { const n = new Set(pick); n.has(id) ? n.delete(id) : n.add(id); setPick(n); setPreview(null); };
  const check = async () => { setPreview(collectWrong(await load([...pick]))); };

  const create = async () => {
    if (!preview?.length) return;
    const rows = wrongPrintRows(preview);
    const n = wrongSets.length + 1;
    const code = `W-${takerCode(taker)}-${today().replace(/-/g, "")}-${n}`;
    const srcNames = [...pick].map((id) => setById.get(id)?.code).join(", ");
    const { data, error } = await supabase.from("contest_sets").insert({
      code, kind: "wrong", title: `${taker.name} 오답 프린트 ${n} (${rows.length}문항)`,
      taker_id: taker.id, parent_ids: [...pick], grade_label: taker.grade || null,
      n_items: rows.length, max_score: rows.reduce((a, r) => a + Number(r.points), 0),
      spec: { sources: srcNames },
    }).select("id").single();
    if (error) { setMsg("생성 실패: " + error.message); return; }
    const { error: e2 } = await supabase.from("contest_items").insert(rows.map((r) => ({ ...r, set_id: data.id })));
    if (e2) { setMsg("문항 복사 실패: " + e2.message); await supabase.from("contest_sets").delete().eq("id", data.id); return; }
    setMsg(`${code} 를 만들었어요 — ② 채점 탭에서 📝 표시로 찾을 수 있어요.`);
    setPick(new Set()); setPreview(null);
    await reload();
  };

  const print = async (s) => {
    const { data: it } = await supabase.from("contest_items").select("*").eq("set_id", s.id).order("no");
    const items = it || [];
    const paths = items.map((x) => x.crop).filter(Boolean);
    if (paths.length) {
      const { data: signed } = await supabase.storage.from("contest-files").createSignedUrls(paths, 3600);
      const url = new Map((signed || []).map((u) => [u.path, u.signedUrl]));
      for (const x of items) if (x.crop && url.get(x.crop)) x.cropUrl = url.get(x.crop);
    }
    const html = printHtml({
      set: s, items, taker, perPage,
      srcLabel: (x) => (x.src_set_id ? `${setById.get(x.src_set_id)?.code || "원본"} ${x.src_no}번` : ""),
    });
    const w = window.open("", "_blank");
    if (!w) { alert("팝업이 막혀 있어요."); return; }
    w.document.write(html); w.document.close();
  };
  const remove = async (s) => {
    if (!window.confirm(`${s.code} 를 지울까요? 이 프린트의 채점 기록도 지워져요.`)) return;
    await supabase.from("contest_sets").delete().eq("id", s.id);
    reload();
  };

  return (
    <>
      <div className="cx-card">
        <h3 className="cx-sub">채점한 프린트에서 고르기</h3>
        {mine.map(({ a, s }) => (
          <label key={s.id} className="cx-check">
            <input type="checkbox" checked={pick.has(s.id)} onChange={() => toggle(s.id)} />
            <span>{s.kind === "wrong" ? "📝 " : ""}{setLabel(s)} <span className="cx-muted">· {a.score}/{a.max_score} · 오답 {a.n_wrong} · 무응답 {a.n_blank}</span></span>
          </label>
        ))}
        {!mine.length && <p className="cx-hint">채점한 프린트가 없어요.</p>}
        <div className="cx-row">
          <button className="cx-btn" onClick={check} disabled={!pick.size}>오답 모아 보기</button>
          {preview && <button className="cx-btn cx-primary" onClick={create} disabled={!preview.length}>오답 프린트 생성 ({preview.length}문항)</button>}
        </div>
        {preview && (
          <div className="cx-pv">
            {preview.map((w, i) => (
              <p key={i} className="cx-muted">{i + 1}. {w.from.code} {w.item.no}번{w.item.src_set_id ? ` (원본 ${setById.get(w.rootSet)?.code} ${w.rootNo}번)` : ""} · 쓴 답 {w.response ?? "없음"} · {w.item.features?.type_name || w.item.features?.domain || ""}</p>
            ))}
            {!preview.length && <p className="cx-hint">틀린 문항이 없어요.</p>}
          </div>
        )}
        <p className="cx-hint">오답과 무응답을 모두 담고, 같은 원본 문항은 한 번만 넣어요.</p>
        {msg && <p className="cx-hint">{msg}</p>}
      </div>

      <div className="cx-card">
        <div className="cx-row cx-between">
          <h3 className="cx-sub">{taker.name}의 오답 프린트 {wrongSets.length}개</h3>
          <label className="cx-muted">한 쪽에 <select className="cx-sel cx-tiny" value={perPage} onChange={(e) => setPerPage(Number(e.target.value))}>{[1, 2, 3, 4].map((n) => <option key={n} value={n}>{n}</option>)}</select> 문항</label>
        </div>
        {wrongSets.map((s) => {
          const at = attempts.find((a) => a.set_id === s.id && a.taker_id === taker.id);
          return (
            <div key={s.id} className="cx-line">
              <span className="cx-grow"><b>{s.title}</b> <span className="cx-muted">{s.code}{at ? ` · ✔ ${at.score}/${at.max_score}` : " · 미채점"}</span></span>
              <button className="cx-btn cx-mini" onClick={() => print(s)}>인쇄</button>
              <button className="cx-btn cx-mini" onClick={() => remove(s)}>삭제</button>
            </div>
          );
        })}
        <p className="cx-hint">그림은 문항 패키지에 그림이 들어 있을 때만 인쇄돼요.</p>
      </div>
    </>
  );
}

// ── ④ 분석 · 브리핑 ──────────────────────────────────────────────────────
function AnalyzeView({ taker, sets, attempts, setById }) {
  const mine = attempts.filter((a) => a.taker_id === taker.id).map((a) => ({ a, s: setById.get(a.set_id) })).filter((x) => x.s)
    .sort((x, y) => String(x.a.graded_at).localeCompare(String(y.a.graded_at)));
  const [pick, setPick] = useState(new Set());
  const [md, setMd] = useState("");
  const [busy, setBusy] = useState(false);
  const [briefs, setBriefs] = useState([]);
  const [edit, setEdit] = useState(null);

  const loadBriefs = async () => {
    const { data } = await supabase.from("contest_briefings").select("*").eq("taker_id", taker.id).order("created_at", { ascending: false });
    setBriefs(data || []);
  };
  useEffect(() => { setPick(new Set()); setMd(""); setEdit(null); loadBriefs(); }, [taker.id]);

  const toggle = (id) => { const n = new Set(pick); n.has(id) ? n.delete(id) : n.add(id); setPick(n); setMd(""); };
  const build = async () => {
    setBusy(true);
    const ids = [...pick];
    const [{ data: it }, { data: rs }] = await Promise.all([
      supabase.from("contest_items").select("*").in("set_id", ids).order("no"),
      supabase.from("contest_responses").select("set_id, item_no, response, is_correct").in("set_id", ids).eq("taker_id", taker.id),
    ]);
    const items = it || [];
    // 집단 정답률: 고른 프린트의 원본 문항을 모든 학생 기준으로
    const roots = [...new Set(items.map((x) => x.src_set_id || x.set_id))];
    const { data: all } = await supabase.from("contest_responses").select("set_id, item_no, is_correct").in("set_id", roots);
    const group = new Map();
    for (const r of all || []) {
      const k = r.set_id + "#" + r.item_no;
      if (!group.has(k)) group.set(k, { n: 0, right: 0 });
      const g = group.get(k); g.n++; if (r.is_correct === true) g.right++;
    }
    const prints = mine.filter(({ s }) => pick.has(s.id)).map(({ a, s }) => ({
      set: s, attempt: a, items: items.filter((x) => x.set_id === s.id), responses: (rs || []).filter((r) => r.set_id === s.id),
    }));
    setMd(buildStudentExport({ taker, prints, group, setById }));
    setBusy(false);
  };
  const download = () => {
    const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `contest-${takerCode(taker)}-${today()}.md`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };
  const copy = async () => { try { await navigator.clipboard.writeText(md); alert("복사했어요."); } catch { alert("복사 실패 — 파일로 받아 주세요."); } };

  const saveBrief = async () => {
    const row = { taker_id: taker.id, title: edit.title.trim() || `${today()} 브리핑`, body: edit.body, set_ids: edit.set_ids, updated_at: new Date().toISOString() };
    const q = edit.id ? supabase.from("contest_briefings").update(row).eq("id", edit.id) : supabase.from("contest_briefings").insert(row);
    const { error } = await q;
    if (error) { alert(error.message); return; }
    setEdit(null); loadBriefs();
  };
  const delBrief = async (b) => {
    if (!window.confirm(`「${b.title}」 브리핑을 지울까요?`)) return;
    await supabase.from("contest_briefings").delete().eq("id", b.id);
    loadBriefs();
  };

  return (
    <>
      <div className="cx-card">
        <h3 className="cx-sub">분석할 프린트</h3>
        {mine.map(({ a, s }) => (
          <label key={s.id} className="cx-check">
            <input type="checkbox" checked={pick.has(s.id)} onChange={() => toggle(s.id)} />
            <span>{s.kind === "wrong" ? "📝 " : ""}{setLabel(s)} <span className="cx-muted">· {a.taken_on || "—"} · {a.score}/{a.max_score}</span></span>
          </label>
        ))}
        {!mine.length && <p className="cx-hint">채점한 프린트가 없어요.</p>}
        <div className="cx-row">
          <button className="cx-btn" onClick={() => setPick(new Set(mine.map(({ s }) => s.id)))} disabled={!mine.length}>전체 선택</button>
          <button className="cx-btn cx-primary" onClick={build} disabled={!pick.size || busy}>{busy ? "정리 중…" : "분석 진행"}</button>
        </div>
        {md && (
          <>
            <div className="cx-row">
              <button className="cx-btn cx-primary" onClick={download}>분석 파일 받기 (md)</button>
              <button className="cx-btn" onClick={copy}>복사</button>
            </div>
            <p className="cx-hint">받은 파일을 채팅방에 올려 분석을 의뢰하세요. 학생은 익명 코드로만 나가요.</p>
            <details><summary className="cx-hint">미리보기</summary><pre className="cx-pre">{md}</pre></details>
          </>
        )}
      </div>

      <div className="cx-card">
        <div className="cx-row cx-between">
          <h3 className="cx-sub">브리핑 {briefs.length}</h3>
          {!edit && <button className="cx-btn cx-mini" onClick={() => setEdit({ title: `${today()} 브리핑`, body: "", set_ids: [...pick] })}>+ 새 브리핑</button>}
        </div>
        {edit && (
          <div className="cx-col">
            <input className="cx-in" value={edit.title} onChange={(e) => setEdit({ ...edit, title: e.target.value })} />
            <textarea className="cx-ta" rows={14} value={edit.body} placeholder="채팅방 분석을 다듬어 붙여 넣으세요 (마크다운)" onChange={(e) => setEdit({ ...edit, body: e.target.value })} />
            <div className="cx-row">
              <button className="cx-btn cx-primary" onClick={saveBrief}>저장</button>
              <button className="cx-btn" onClick={() => setEdit(null)}>취소</button>
              <span className="cx-muted">연결된 프린트 {edit.set_ids.length}개</span>
            </div>
          </div>
        )}
        {briefs.map((b) => (
          <details key={b.id} className="cx-brief">
            <summary><b>{b.title}</b> <span className="cx-muted">{new Date(b.updated_at).toLocaleDateString("ko-KR")} · 프린트 {b.set_ids.length}</span></summary>
            <pre className="cx-pre">{b.body}</pre>
            <div className="cx-row">
              <button className="cx-btn cx-mini" onClick={() => setEdit({ id: b.id, title: b.title, body: b.body, set_ids: b.set_ids })}>고치기</button>
              <button className="cx-btn cx-mini" onClick={() => delBrief(b)}>삭제</button>
            </div>
          </details>
        ))}
      </div>
    </>
  );
}

// ── 프린트 관리 ──────────────────────────────────────────────────────────
function PrintsView({ sets, reload }) {
  const [log, setLog] = useState([]);
  const [busy, setBusy] = useState(false);
  const [sid, setSid] = useState("");
  const [mk, setMk] = useState(null);
  const fileRef = useRef(null);

  const [prog, setProg] = useState("");

  // 패키지 하나 반영 — pdfs: { student, teacher } (Uint8Array), crops: Map(no → Uint8Array PNG)
  const importOne = async (label, j, pdfs = {}, crops = new Map()) => {
    const why = validatePackage(j);
    if (why) return `✗ ${label}: ${why}`;
    const { set: srow, items: irows } = packageToRows(j);
    const code = srow.code;
    // 1) 파일 올리기 (같은 경로면 덮어씀)
    const put = async (path, bytes, type) => {
      const { error } = await supabase.storage.from("contest-files").upload(path, new Blob([bytes], { type }), { contentType: type, upsert: true });
      if (error) throw new Error(`${path}: ${error.message}`);
    };
    const newFiles = [];
    if (pdfs.student) { setProg(`${code} 학생용 PDF`); await put(`${code}/student.pdf`, pdfs.student, "application/pdf"); newFiles.push({ name: `${code}_학생용.pdf`, path: `${code}/student.pdf`, kind: "problem", size: pdfs.student.length }); }
    if (pdfs.teacher) { setProg(`${code} 교사용 PDF`); await put(`${code}/teacher.pdf`, pdfs.teacher, "application/pdf"); newFiles.push({ name: `${code}_교사용.pdf`, path: `${code}/teacher.pdf`, kind: "solution", size: pdfs.teacher.length }); }
    let nCrop = 0;
    for (const r of irows) {
      const png = crops.get(r.no);
      if (!png) continue;
      setProg(`${code} 문항 이미지 ${r.no}/${irows.length}`);
      const path = `${code}/items/${String(r.no).padStart(2, "0")}.png`;
      await put(path, png, "image/png");
      r.crop = path; nCrop++;
    }
    // 2) 프린트 행 (기존 파일 목록은 경로 기준으로 합침)
    const { data: prev } = await supabase.from("contest_sets").select("files").eq("code", code).maybeSingle();
    const files = [...(prev?.files || []).filter((f) => !newFiles.some((n) => n.path === f.path)), ...newFiles];
    const { data: up, error } = await supabase.from("contest_sets")
      .upsert({ ...srow, files, updated_at: new Date().toISOString() }, { onConflict: "code" }).select("id").single();
    if (error) return `✗ ${label}: ${error.message}`;
    // 3) 문항 교체 — 이미지 경로를 이전 것에서 이어받기
    const { data: oldItems } = await supabase.from("contest_items").select("no, crop").eq("set_id", up.id);
    const oldCrop = new Map((oldItems || []).map((x) => [x.no, x.crop]));
    for (const r of irows) if (!r.crop && oldCrop.get(r.no)) r.crop = oldCrop.get(r.no);
    await supabase.from("contest_items").delete().eq("set_id", up.id);
    const { error: e2 } = await supabase.from("contest_items").insert(irows.map((r) => ({ ...r, set_id: up.id })));
    if (e2) return `✗ ${label}: 문항 저장 실패 (${e2.message})`;
    // 4) 정답이 바뀌었을 수 있으니 기존 응답·채점을 다시 매긴다
    const { data: old } = await supabase.from("contest_responses").select("*").eq("set_id", up.id);
    let regraded = 0;
    if (old?.length) {
      const byNo = new Map(irows.map((r) => [r.no, r]));
      await supabase.from("contest_responses").upsert(old.map((r) => ({ ...r, is_correct: byNo.has(r.item_no) ? judge(byNo.get(r.item_no), r.response) : null })));
      const who = [...new Set(old.map((r) => r.taker_id))];
      for (const t of who) {
        const ans = Object.fromEntries(old.filter((r) => r.taker_id === t).map((r) => [r.item_no, r.response]));
        const g = gradeAll(irows, ans);
        await supabase.from("contest_attempts").update({ score: g.score, max_score: g.max, n_right: g.right, n_wrong: g.wrong, n_blank: g.blank }).eq("set_id", up.id).eq("taker_id", t);
      }
      regraded = who.length;
    }
    return `✓ ${code} · ${irows.length}문항 · 만점 ${srow.max_score}${newFiles.length ? ` · PDF ${newFiles.length}` : ""}${nCrop ? ` · 문항 이미지 ${nCrop}` : ""}${regraded ? ` · ${regraded}명 재채점` : ""}`;
  };

  const importFiles = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    setBusy(true);
    const out = [];
    for (const f of files) {
      try {
        if (/\.zip$/i.test(f.name)) {
          // 묶음: <코드>/package.json · student.pdf · teacher.pdf · items/NN.png
          const entries = await readZip(await f.arrayBuffer());
          const groups = new Map();
          for (const z of entries) {
            const parts = z.name.split("/").filter(Boolean);
            if (parts.length < 2) continue;
            const key = parts.length > 2 && parts[parts.length - 2] === "items" ? parts.slice(0, -2).join("/") : parts.slice(0, -1).join("/");
            if (!groups.has(key)) groups.set(key, { pkg: null, pdfs: {}, crops: new Map() });
            const g = groups.get(key), base = parts[parts.length - 1];
            if (base === "package.json") g.pkg = JSON.parse(new TextDecoder().decode(z.data));
            else if (/^student\.pdf$/i.test(base)) g.pdfs.student = z.data;
            else if (/^teacher\.pdf$/i.test(base)) g.pdfs.teacher = z.data;
            else if (parts.includes("items") && /^\d+\.png$/i.test(base)) g.crops.set(parseInt(base, 10), z.data);
          }
          if (!groups.size) { out.push(`✗ ${f.name}: 묶음 안에 프린트 폴더가 없어요`); continue; }
          for (const [key, g] of groups) {
            if (!g.pkg) { out.push(`✗ ${f.name} › ${key}: package.json 없음`); continue; }
            try { out.push(await importOne(`${f.name} › ${key}`, g.pkg, g.pdfs, g.crops)); }
            catch (err) { out.push(`✗ ${f.name} › ${key}: ${err.message}`); }
            setLog([...out]);
          }
        } else {
          out.push(await importOne(f.name, JSON.parse(await f.text())));
        }
      } catch (err) { out.push(`✗ ${f.name}: ${err.message}`); }
      setLog([...out]);
    }
    setLog(out); setBusy(false); setProg("");
    if (fileRef.current) fileRef.current.value = "";
    reload();
  };

  const create = async () => {
    if (!mk.code.trim() || !mk.title.trim()) { alert("코드와 제목을 써 주세요."); return; }
    const { error } = await supabase.from("contest_sets").insert({
      code: mk.code.trim(), kind: "original", title: mk.title.trim(), contest: "KUT",
      year: mk.year ? Number(mk.year) : null, half: mk.half || null, grade_label: mk.grade_label || null,
    });
    if (error) { alert(error.message); return; }
    setMk(null); reload();
  };

  const set = sets.find((s) => s.id === sid);
  return (
    <>
      <div className="cx-card">
        <h3 className="cx-sub">프린트 등록 — 묶음(zip) 또는 문항 패키지(JSON)</h3>
        <input ref={fileRef} type="file" accept=".zip,.json,application/zip,application/json" multiple onChange={importFiles} disabled={busy} className="cx-file" />
        {busy && prog && <p className="cx-hint">올리는 중… {prog}</p>}
        <p className="cx-hint">채팅방에서 받은 묶음(zip) 하나로 학생용·교사용 PDF, 문항, 문항 이미지가 한꺼번에 들어가요. 같은 코드면 교체하고, 이미 채점한 학생은 새 정답으로 다시 채점해요.</p>
        {log.map((l, i) => <p key={i} className={"cx-log" + (l.startsWith("✓") ? " good" : " bad")}>{l}</p>)}
      </div>
      <div className="cx-card">
        <div className="cx-row cx-between">
          <h3 className="cx-sub">기출 프린트 {sets.length}</h3>
          <button className="cx-btn cx-mini" onClick={() => setMk(mk ? null : { code: "", title: "", year: "", half: "상반기", grade_label: "" })}>{mk ? "닫기" : "+ 파일만 먼저"}</button>
        </div>
        {mk && (
          <div className="cx-new">
            <input className="cx-in" placeholder="코드 (KUT-2025-H1-M2)" value={mk.code} onChange={(e) => setMk({ ...mk, code: e.target.value })} />
            <input className="cx-in" placeholder="제목" value={mk.title} onChange={(e) => setMk({ ...mk, title: e.target.value })} />
            <input className="cx-in" placeholder="연도" inputMode="numeric" value={mk.year} onChange={(e) => setMk({ ...mk, year: e.target.value })} />
            <select className="cx-sel" value={mk.half} onChange={(e) => setMk({ ...mk, half: e.target.value })}>{HALVES.map((h) => <option key={h}>{h}</option>)}</select>
            <input className="cx-in" placeholder="학년 (중2)" value={mk.grade_label} onChange={(e) => setMk({ ...mk, grade_label: e.target.value })} />
            <button className="cx-btn cx-primary" onClick={create}>만들기</button>
          </div>
        )}
        <div className="cx-list">
          {sets.map((s) => (
            <button key={s.id} className={"cx-set" + (s.id === sid ? " on" : "")} onClick={() => setSid(s.id === sid ? "" : s.id)}>
              <b>{setLabel(s)}</b>
              <span className="cx-muted">{s.code} · {s.n_items ? `${s.n_items}문항 · 만점 ${s.max_score}` : "문항 대기"} · 파일 {(s.files || []).length}</span>
            </button>
          ))}
        </div>
      </div>
      {set && <FilesView set={set} reload={reload} />}
    </>
  );
}

const KIND = { problem: "문제지", answer: "정답지", solution: "해설지", etc: "기타" };
function FilesView({ set, reload }) {
  const [kind, setKind] = useState("problem");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const ref = useRef(null);
  const files = set.files || [];
  const upload = async (e) => {
    const fs = Array.from(e.target.files || []);
    if (!fs.length) return;
    setBusy(true);
    const next = [...files];
    for (const f of fs) {
      const safe = f.name.replace(/[^\w.\-가-힣]/g, "_");
      const path = `${set.code}/${Date.now()}-${safe}`;
      const { error } = await supabase.storage.from("contest-files").upload(path, f, { contentType: f.type || "application/pdf" });
      if (error) { setMsg(`✗ ${f.name}: ${error.message}`); continue; }
      next.push({ name: f.name, path, kind, size: f.size });
    }
    await supabase.from("contest_sets").update({ files: next, updated_at: new Date().toISOString() }).eq("id", set.id);
    setBusy(false);
    if (ref.current) ref.current.value = "";
    reload();
  };
  const open = async (f) => {
    const { data, error } = await supabase.storage.from("contest-files").createSignedUrl(f.path, 600, { download: f.name });
    if (error) { setMsg("열기 실패: " + error.message); return; }
    window.open(data.signedUrl, "_blank");
  };
  const remove = async (f) => {
    if (!window.confirm(`${f.name} 을(를) 지울까요?`)) return;
    await supabase.storage.from("contest-files").remove([f.path]);
    await supabase.from("contest_sets").update({ files: files.filter((x) => x.path !== f.path) }).eq("id", set.id);
    reload();
  };
  return (
    <div className="cx-card">
      <h3 className="cx-sub">{set.code} 파일</h3>
      {files.map((f) => (
        <div key={f.path} className="cx-line">
          <span className="cx-tag">{KIND[f.kind] || f.kind}</span>
          <span className="cx-grow cx-ell">{f.name}</span>
          <span className="cx-muted">{f.size ? Math.round(f.size / 1024) + "KB" : ""}</span>
          <button className="cx-btn cx-mini" onClick={() => open(f)}>받기</button>
          <button className="cx-btn cx-mini" onClick={() => remove(f)}>삭제</button>
        </div>
      ))}
      {!files.length && <p className="cx-hint">아직 올린 파일이 없어요.</p>}
      <div className="cx-row">
        <select className="cx-sel" value={kind} onChange={(e) => setKind(e.target.value)}>
          {Object.entries(KIND).map(([k, l]) => <option key={k} value={k}>{l}</option>)}
        </select>
        <input ref={ref} type="file" accept=".pdf,application/pdf,image/*" multiple onChange={upload} disabled={busy} className="cx-file" />
      </div>
      {msg && <p className="cx-err">{msg}</p>}
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .cx-wrap{max-width:760px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .cx-title{margin:4px 0 12px;font-size:22px}
      .cx-sub{margin:0;font-size:15px}
      .cx-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
      .cx-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
      .cx-col{display:flex;flex-direction:column;gap:8px}
      .cx-between{justify-content:space-between}
      .cx-grow{flex:1;min-width:0}
      .cx-ell{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
      .cx-btn{padding:9px 12px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:13px;color:inherit}
      .cx-btn:disabled{opacity:.45}
      .cx-primary{background:var(--accent,#1f2937);color:#fff;border-color:transparent}
      .cx-mini{padding:6px 10px;font-size:12px}
      .cx-sel,.cx-in,.cx-ta{padding:9px 10px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:inherit;font-size:14px;min-width:0}
      .cx-sel{flex:1}
      .cx-in{flex:1}
      .cx-short{flex:0 0 84px}
      .cx-search{flex:0 1 160px}
      .cx-date{padding:5px 8px;font-size:13px}
      .cx-tiny{flex:none;padding:4px 6px}
      .cx-ta{width:100%;box-sizing:border-box;font-size:13.5px;line-height:1.6}
      .cx-file{font-size:13px}
      .cx-log{font-size:12.5px;margin:0}
      .cx-log.good{color:var(--good,#16a34a)} .cx-log.bad{color:var(--bad,#dc2626)}
      .cx-hint{font-size:12.5px;color:var(--muted,#8a8f98);margin:0}
      .cx-muted{font-size:12px;color:var(--muted,#8a8f98);font-weight:400}
      .cx-err{font-size:13px;color:var(--bad,#dc2626);margin:0}
      .cx-tabs{display:flex;gap:6px;margin-bottom:12px;overflow-x:auto}
      .cx-tab{flex:1 0 auto;padding:9px 10px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:transparent;color:inherit;font-size:13px;white-space:nowrap}
      .cx-tab.on{background:var(--accent,#1f2937);color:#fff;border-color:transparent}
      .cx-list{display:flex;flex-direction:column;gap:6px;max-height:340px;overflow:auto}
      .cx-set{all:unset;cursor:pointer;display:flex;flex-direction:column;gap:2px;padding:9px 11px;border:1px solid var(--border,#e5e7eb);border-radius:10px;font-size:13.5px}
      .cx-set.on{border-color:var(--accent,#1f2937);background:var(--bg2,#f6f7f9)}
      .cx-set:disabled{opacity:.5;cursor:default}
      .cx-line{display:flex;gap:8px;align-items:center;border-top:1px solid var(--border,#eef0f3);padding:8px 0;font-size:13.5px}
      .cx-link{all:unset;cursor:pointer;flex:1;min-width:0}
      .cx-check{display:flex;gap:8px;align-items:flex-start;font-size:13.5px;padding:4px 0}
      .cx-check input{margin-top:3px}
      .cx-pv{border-top:1px dashed var(--border,#e5e7eb);padding-top:6px}
      .cx-pv p{margin:2px 0}
      .cx-new{display:grid;grid-template-columns:1fr 1fr;gap:6px}
      .cx-tag{font-size:11px;padding:2px 7px;border-radius:99px;background:var(--bg2,#f1f2f4)}
      .cx-pre{white-space:pre-wrap;font-size:12.5px;background:var(--bg2,#f6f7f9);padding:10px;border-radius:10px;margin:6px 0 0;max-height:420px;overflow:auto}
      .cx-score{font-size:13px;font-weight:600}
      .cx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px}
      .cx-cell{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:11.5px;color:var(--muted,#8a8f98)}
      .cx-cell input{width:100%;box-sizing:border-box;text-align:center;padding:8px 2px;border-radius:9px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#1c1c1e);font-size:15px}
      .cx-cell.good input{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .cx-cell.bad input{border-color:var(--bad,#dc2626);background:rgba(220,38,38,.07)}
      .cx-cell.blank input{border-color:#d97706;background:rgba(217,119,6,.07)}
      .cx-brief{border-top:1px solid var(--border,#eef0f3);padding:8px 0}
      .cx-brief summary{cursor:pointer;font-size:13.5px}
    `}</style>
  );
}
