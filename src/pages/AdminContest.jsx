// src/pages/AdminContest.jsx — 경시 대비 (해시 라우트: #/admin/contest, admin 전용)
// 채팅방에서 만든 문항 패키지 JSON 가져오기 → 응시자·응답 입력(정오 판정은 앱) → 분석용 md 내보내기.
// 앱은 AI 를 부르지 않는다. 규격: 프로젝트 문서 claude/SPEC-경시대비-v1.md
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/authx";
import {
  validatePackage, packageToRows, judge, normAnswer, takerCode, aggregate, buildExportMd,
} from "../lib/contest";

export default function AdminContest() {
  const [ok, setOk] = useState(null);
  const [sets, setSets] = useState([]);
  const [setId, setSetId] = useState(null);
  const [tab, setTab] = useState("resp");
  const [items, setItems] = useState([]);
  const [takers, setTakers] = useState([]);
  const [resps, setResps] = useState([]);
  const [log, setLog] = useState([]);
  const [busy, setBusy] = useState(false);
  const [missing, setMissing] = useState(false);
  const fileRef = useRef(null);

  useEffect(() => {
    (async () => {
      const { data: s } = await supabase.auth.getSession();
      if (!s?.session) { setOk(false); return; }
      const { data: p } = await supabase.from("profiles").select("role").eq("id", s.session.user.id).maybeSingle();
      setOk(p?.role === "admin");
      if (p?.role === "admin") { loadSets(); loadTakers(); }
    })();
  }, []);

  const loadSets = async () => {
    const { data, error } = await supabase.from("contest_sets")
      .select("id, code, title, contest, year, round, grade_label, test_date, n_items, max_score, files, created_at")
      .order("code", { ascending: false });
    if (error) { setMissing(true); return; }
    setSets(data || []);
  };
  const loadTakers = async () => {
    const { data } = await supabase.from("contest_takers").select("id, seq, name, grade, memo").order("seq");
    setTakers(data || []);
  };
  const loadSet = async (id) => {
    if (!id) { setItems([]); setResps([]); return; }
    const [{ data: it }, { data: rs }] = await Promise.all([
      supabase.from("contest_items").select("*").eq("set_id", id).order("no"),
      supabase.from("contest_responses").select("taker_id, item_no, response, is_correct").eq("set_id", id),
    ]);
    setItems(it || []);
    setResps(rs || []);
  };
  useEffect(() => { loadSet(setId); }, [setId]);

  const set = sets.find((s) => s.id === setId) || null;

  const pickFiles = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    setBusy(true);
    const out = [];
    let lastId = null;
    for (const f of files) {
      try {
        const j = JSON.parse(await f.text());
        const why = validatePackage(j);
        if (why) { out.push(`✗ ${f.name}: ${why}`); continue; }
        const { set: srow, items: irows } = packageToRows(j);
        const { data: up, error } = await supabase.from("contest_sets")
          .upsert({ ...srow, updated_at: new Date().toISOString() }, { onConflict: "code" })
          .select("id").single();
        if (error) { out.push(`✗ ${f.name}: ${error.message}`); continue; }
        // 문항은 통째로 교체 (응답은 번호로 붙어 있으니 그대로 남는다)
        await supabase.from("contest_items").delete().eq("set_id", up.id);
        const { error: e2 } = await supabase.from("contest_items").insert(irows.map((r) => ({ ...r, set_id: up.id })));
        if (e2) { out.push(`✗ ${f.name}: 문항 저장 실패 (${e2.message})`); continue; }
        // 정답이 바뀌었을 수 있으니 기존 응답의 정오를 다시 매긴다
        const { data: old } = await supabase.from("contest_responses").select("*").eq("set_id", up.id);
        if (old?.length) {
          const byNo = new Map(irows.map((r) => [r.no, r]));
          const fixed = old.map((r) => ({ ...r, is_correct: byNo.has(r.item_no) ? judge(byNo.get(r.item_no), r.response) : null }));
          await supabase.from("contest_responses").upsert(fixed);
        }
        lastId = up.id;
        out.push(`✓ ${f.name} › ${srow.code} · ${irows.length}문항 · 만점 ${srow.max_score}${old?.length ? ` · 기존 응답 ${old.length}칸 재채점` : ""}`);
      } catch (err) {
        out.push(`✗ ${f.name}: JSON 해석 실패 (${err.message})`);
      }
    }
    setLog(out);
    setBusy(false);
    if (fileRef.current) fileRef.current.value = "";
    await loadSets();
    if (lastId) { setSetId(lastId); loadSet(lastId); }
  };

  const removeSet = async () => {
    if (!set || !window.confirm(`${set.code} 세트와 그 응답을 모두 삭제할까요?`)) return;
    await supabase.from("contest_sets").delete().eq("id", set.id);
    setSetId(null);
    loadSets();
  };

  if (ok === null) return null;
  if (ok === false) return <div className="cx-wrap"><Style /><p className="cx-err">관리자만 접근할 수 있어요.</p></div>;

  return (
    <div className="cx-wrap"><Style />
      <h2 className="cx-title">🏆 경시 대비</h2>
      {missing && <p className="cx-err">표가 아직 없어요 — supabase/2026-11_contest.sql 을 SQL Editor 에서 실행해 주세요.</p>}

      <div className="cx-card">
        <h3 className="cx-sub">문항 패키지 가져오기 (JSON)</h3>
        <input ref={fileRef} type="file" accept=".json,application/json" multiple onChange={pickFiles} disabled={busy} className="cx-file" />
        <p className="cx-hint">같은 세트 코드면 문항을 교체하고, 이미 입력한 응답은 새 정답으로 다시 채점해요.</p>
        {log.map((l, i) => <p key={i} className={"cx-log" + (l.startsWith("✓") ? " good" : " bad")}>{l}</p>)}
      </div>

      <SetPicker sets={sets} setId={setId} onPick={(id) => { setSetId(id); setTab("resp"); }} onCreated={async (id) => { await loadSets(); setSetId(id); }} />

      {set && (
        <div className="cx-card">
          <div className="cx-row cx-between">
            <h3 className="cx-sub">{set.code} · {set.title}</h3>
            <button className="cx-btn cx-mini" onClick={removeSet}>세트 삭제</button>
          </div>
          <p className="cx-hint">{[set.contest, set.year, set.round, set.grade_label, set.test_date].filter(Boolean).join(" · ") || "—"} · {set.n_items ? `${set.n_items}문항 · 만점 ${set.max_score}` : "문항 패키지 대기 중"}</p>
          <div className="cx-tabs">
            {[["resp", "응답 입력"], ["files", `파일 ${(set.files || []).length}`], ["items", "문항"], ["export", "분석용 내보내기"]].map(([k, l]) => (
              <button key={k} className={"cx-tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>
            ))}
          </div>
        </div>
      )}

      {set && tab === "files" && <FilesView set={set} reload={loadSets} />}
      {set && tab !== "files" && !items.length && <div className="cx-card"><p className="cx-hint">아직 문항 패키지가 없어요. 이 프린트의 PDF로 채팅방에서 만든 JSON을 위에서 가져오면 응답 입력이 열려요.</p></div>}
      {set && items.length > 0 && tab === "items" && <ItemsView items={items} />}
      {set && items.length > 0 && tab === "resp" && (
        <ResponsesView set={set} items={items} takers={takers} resps={resps}
          reloadTakers={loadTakers} reload={() => loadSet(set.id)} />
      )}
      {set && items.length > 0 && tab === "export" && <ExportView set={set} items={items} takers={takers} resps={resps} />}
    </div>
  );
}

// ── 프린트 찾기 · 새로 만들기 ────────────────────────────────────────────
function SetPicker({ sets, setId, onPick, onCreated }) {
  const [q, setQ] = useState("");
  const [mk, setMk] = useState(null);
  const [err, setErr] = useState("");
  const terms = q.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const shown = sets.filter((s) => {
    const hay = [s.code, s.title, s.contest, s.year, s.round, s.grade_label].join(" ").toLowerCase();
    return terms.every((t) => hay.includes(t));
  });
  const create = async () => {
    if (!mk.code.trim() || !mk.title.trim()) { setErr("코드와 제목을 써 주세요."); return; }
    const { data, error } = await supabase.from("contest_sets").insert({
      code: mk.code.trim(), title: mk.title.trim(), contest: mk.contest || null,
      year: mk.year ? Number(mk.year) : null, grade_label: mk.grade_label || null,
    }).select("id").single();
    if (error) { setErr(error.message); return; }
    setMk(null); setErr("");
    onCreated(data.id);
  };
  return (
    <div className="cx-card">
      <div className="cx-row cx-between">
        <h3 className="cx-sub">기출 프린트 ({sets.length})</h3>
        <button className="cx-btn cx-mini" onClick={() => setMk(mk ? null : { code: "", title: "", contest: "KUT", year: "", grade_label: "" })}>{mk ? "닫기" : "+ 새 프린트"}</button>
      </div>
      {mk && (
        <div className="cx-new">
          {[["code", "코드 (예: KUT-2025-1-M2)"], ["title", "제목"], ["contest", "대회"], ["year", "연도"], ["grade_label", "학년"]].map(([k, ph]) => (
            <input key={k} className="cx-in" placeholder={ph} value={mk[k]} onChange={(e) => setMk({ ...mk, [k]: e.target.value })} />
          ))}
          <button className="cx-btn cx-primary" onClick={create}>만들기</button>
          {err && <p className="cx-err">{err}</p>}
        </div>
      )}
      <input className="cx-in" placeholder="찾기 — 연도·학년·회차 (예: 2025 중2)" value={q} onChange={(e) => setQ(e.target.value)} />
      <div className="cx-list">
        {shown.map((s) => (
          <button key={s.id} className={"cx-set" + (s.id === setId ? " on" : "")} onClick={() => onPick(s.id)}>
            <b>{s.title}</b>
            <span className="cx-muted">{s.code} · {s.n_items ? `${s.n_items}문항` : "문항 대기"} · 파일 {(s.files || []).length}</span>
          </button>
        ))}
        {!shown.length && <p className="cx-hint">{sets.length ? "맞는 프린트가 없어요." : "아직 프린트가 없어요."}</p>}
      </div>
    </div>
  );
}

// ── 프린트 파일 ──────────────────────────────────────────────────────────
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
      <h3 className="cx-sub">프린트 파일</h3>
      {files.map((f) => (
        <div key={f.path} className="cx-file-row">
          <span className="cx-tag">{KIND[f.kind] || f.kind}</span>
          <span className="cx-fname">{f.name}</span>
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

// ── 문항 ─────────────────────────────────────────────────────────────────
function ItemsView({ items }) {
  const [open, setOpen] = useState(null);
  return (
    <div className="cx-card">
      <h3 className="cx-sub">문항 {items.length}개</h3>
      {items.map((x) => {
        const f = x.features || {}, m = x.metrics || {};
        return (
          <div key={x.no} className="cx-item">
            <button className="cx-item-head" onClick={() => setOpen(open === x.no ? null : x.no)}>
              <b>{x.no}번</b>
              <span>정답 {x.accept.join(", ")}</span>
              <span className="cx-muted">{[f.domain, f.type_name, f.difficulty && `난이도 ${f.difficulty}`].filter(Boolean).join(" · ")}</span>
            </button>
            {open === x.no && (
              <div className="cx-item-body">
                <p className="cx-muted">
                  {x.points}점 · {x.answer_type}{x.n_choices ? `/${x.n_choices}` : ""} · {m.chars}자 · {m.sentences}문장 · 수식 {m.formulas}
                  {f.figure?.has ? ` · 도형(${f.figure.kind || "?"})` : ""} · 단원 {f.concept_main || f.unit || "—"}
                </p>
                {x.text && <pre className="cx-pre">{x.text}</pre>}
                {x.solution && <pre className="cx-pre">{renderSolution(x.solution)}</pre>}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
function renderSolution(sol) {
  if (typeof sol === "string") return sol;
  if (Array.isArray(sol?.steps)) return sol.steps.map((s, i) => `${i + 1}. ${typeof s === "string" ? s : s.text || JSON.stringify(s)}`).join("\n");
  return JSON.stringify(sol, null, 2);
}

// ── 응답 입력 ────────────────────────────────────────────────────────────
function ResponsesView({ set, items, takers, resps, reloadTakers, reload }) {
  const [tid, setTid] = useState("");
  const [name, setName] = useState("");
  const [grade, setGrade] = useState("");
  const [draft, setDraft] = useState({});
  const [msg, setMsg] = useState("");
  const [paste, setPaste] = useState("");
  const [pasteLog, setPasteLog] = useState([]);

  const respOf = useMemo(() => {
    const m = new Map();
    for (const r of resps) m.set(r.taker_id + "|" + r.item_no, r.response);
    return m;
  }, [resps]);
  const entered = useMemo(() => new Set(resps.map((r) => r.taker_id)), [resps]);

  useEffect(() => {
    const d = {};
    if (tid) for (const x of items) d[x.no] = respOf.get(tid + "|" + x.no) ?? "";
    setDraft(d);
    setMsg("");
  }, [tid, items, respOf]);

  const ensureTaker = async (nm, gr) => {
    const n = nm.trim(), g = (gr || "").trim();
    const hit = takers.find((t) => t.name === n && (t.grade || "") === g);
    if (hit) return hit.id;
    const { data, error } = await supabase.from("contest_takers").insert({ name: n, grade: g }).select("id").single();
    if (error) throw error;
    return data.id;
  };

  const addTaker = async () => {
    if (!name.trim()) return;
    try {
      const id = await ensureTaker(name, grade);
      await reloadTakers();
      setTid(id); setName(""); setGrade("");
    } catch (e) { setMsg("추가 실패: " + e.message); }
  };

  const rowsFor = (takerId, answers) => items.map((x) => {
    const v = (answers[x.no] ?? "").toString().trim();
    return { set_id: set.id, taker_id: takerId, item_no: x.no, response: v || null,
      is_correct: judge(x, v), updated_at: new Date().toISOString() };
  });

  const save = async () => {
    if (!tid) return;
    const { error } = await supabase.from("contest_responses").upsert(rowsFor(tid, draft));
    if (error) { setMsg("저장 실패: " + error.message); return; }
    await reload();
    setMsg("저장했어요.");
  };

  const clearTaker = async () => {
    if (!tid || !window.confirm("이 학생의 이 세트 응답을 지울까요?")) return;
    await supabase.from("contest_responses").delete().eq("set_id", set.id).eq("taker_id", tid);
    await reload();
  };

  // 붙여넣기: 한 줄에 한 학생 — 이름 ⇥ 학년 ⇥ 1번 답 ⇥ 2번 답 … (엑셀 복사 그대로, 쉼표도 됨)
  const importPaste = async () => {
    const lines = paste.split(/\r?\n/).map((l) => l.trimEnd()).filter((l) => l.trim());
    const out = [];
    for (const l of lines) {
      const cols = (l.includes("\t") ? l.split("\t") : l.split(",")).map((c) => c.trim());
      const [nm, gr, ...ans] = cols;
      if (!nm) continue;
      if (ans.length > items.length) { out.push(`✗ ${nm}: 답이 ${ans.length}칸 — 문항은 ${items.length}개`); continue; }
      try {
        const id = await ensureTaker(nm, gr);
        const a = {};
        items.forEach((x, i) => { a[x.no] = ans[i] ?? ""; });
        const { error } = await supabase.from("contest_responses").upsert(rowsFor(id, a));
        if (error) throw error;
        out.push(`✓ ${nm}${gr ? ` (${gr})` : ""} · ${ans.filter(Boolean).length}칸`);
      } catch (e) { out.push(`✗ ${nm}: ${e.message}`); }
    }
    setPasteLog(out);
    await reloadTakers();
    await reload();
    if (out.every((x) => x.startsWith("✓"))) setPaste("");
  };

  const cur = takers.find((t) => t.id === tid);
  let score = 0, right = 0, blank = 0;
  for (const x of items) {
    const c = judge(x, draft[x.no]);
    if (c === true) { score += Number(x.points); right++; } else if (c === null) blank++;
  }

  return (
    <>
      <div className="cx-card">
        <h3 className="cx-sub">학생 선택 · 추가</h3>
        <select className="cx-sel" value={tid} onChange={(e) => setTid(e.target.value)}>
          <option value="">— 학생 선택 —</option>
          {takers.map((t) => (
            <option key={t.id} value={t.id}>{entered.has(t.id) ? "● " : "○ "}{t.name}{t.grade ? ` (${t.grade})` : ""} · {takerCode(t)}</option>
          ))}
        </select>
        <div className="cx-row">
          <input className="cx-in" placeholder="이름" value={name} onChange={(e) => setName(e.target.value)} />
          <input className="cx-in cx-short" placeholder="학년" value={grade} onChange={(e) => setGrade(e.target.value)} />
          <button className="cx-btn" onClick={addTaker}>추가</button>
        </div>
        <p className="cx-hint">● = 이 세트 응답 있음. 같은 이름·학년이면 같은 학생으로 묶여요.</p>
      </div>

      {cur && (
        <div className="cx-card">
          <div className="cx-row cx-between">
            <h3 className="cx-sub">{cur.name} · {takerCode(cur)}</h3>
            <span className="cx-score">{score} / {set.max_score}점 · 정답 {right} · 무응답 {blank}</span>
          </div>
          <div className="cx-grid">
            {items.map((x) => {
              const c = judge(x, draft[x.no]);
              return (
                <label key={x.no} className={"cx-cell" + (c === true ? " good" : c === false ? " bad" : "")}>
                  <span>{x.no}</span>
                  <input inputMode={x.answer_type === "text" ? "text" : "numeric"} value={draft[x.no] ?? ""}
                    onChange={(e) => setDraft({ ...draft, [x.no]: e.target.value })} />
                </label>
              );
            })}
          </div>
          <div className="cx-row">
            <button className="cx-btn cx-primary" onClick={save}>저장</button>
            <button className="cx-btn cx-mini" onClick={clearTaker}>응답 지우기</button>
            {msg && <span className="cx-hint">{msg}</span>}
          </div>
        </div>
      )}

      <div className="cx-card">
        <h3 className="cx-sub">여러 명 붙여넣기</h3>
        <textarea className="cx-ta" rows={5} value={paste} onChange={(e) => setPaste(e.target.value)}
          placeholder={"이름⇥학년⇥1번⇥2번⇥… (엑셀에서 복사, 쉼표 구분도 됨)\n홍길동\t중2\t3\t5\t\t120"} />
        <button className="cx-btn" onClick={importPaste} disabled={!paste.trim()}>가져오기</button>
        {pasteLog.map((l, i) => <p key={i} className={"cx-log" + (l.startsWith("✓") ? " good" : " bad")}>{l}</p>)}
      </div>

      <Overview items={items} takers={takers} resps={resps} />
    </>
  );
}

function Overview({ items, takers, resps }) {
  const ag = useMemo(() => aggregate(items, takers, resps), [items, takers, resps]);
  if (!ag.n) return null;
  return (
    <div className="cx-card">
      <h3 className="cx-sub">현황 · {ag.n}명</h3>
      <div className="cx-scroll">
        <table className="cx-table">
          <thead><tr><th>학생</th><th>점수</th>{items.map((x) => <th key={x.no}>{x.no}</th>)}</tr></thead>
          <tbody>
            {ag.students.map((s) => (
              <tr key={s.taker.id}>
                <td>{s.taker.name}</td><td>{s.score}</td>
                {items.map((x) => {
                  const r = s.cells.get(x.no)?.response;
                  const c = judge(x, r);
                  return <td key={x.no} className={c === true ? "good" : c === false ? "bad" : ""}>{c === true ? "○" : c === false ? normAnswer(r) : "·"}</td>;
                })}
              </tr>
            ))}
            <tr className="cx-foot"><td>정답률</td><td />{ag.items.map((a) => <td key={a.no}>{a.p == null ? "—" : Math.round(a.p * 100)}</td>)}</tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ── 내보내기 ─────────────────────────────────────────────────────────────
function ExportView({ set, items, takers, resps }) {
  const md = useMemo(() => buildExportMd(set, items, takers, resps), [set, items, takers, resps]);
  const n = new Set(resps.map((r) => r.taker_id)).size;
  const download = () => {
    const blob = new Blob([md], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `contest-${set.code}-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };
  const copy = async () => {
    try { await navigator.clipboard.writeText(md); alert("복사했어요."); } catch { alert("복사 실패 — 파일로 받아 주세요."); }
  };
  return (
    <div className="cx-card">
      <h3 className="cx-sub">분석용 내보내기</h3>
      <p className="cx-hint">응시 {n}명 · 학생은 익명 코드로만 나가요. 받은 md 를 채팅방에 올리면 분석해 드려요.</p>
      <div className="cx-row">
        <button className="cx-btn cx-primary" onClick={download} disabled={!n}>md 파일 받기</button>
        <button className="cx-btn" onClick={copy} disabled={!n}>복사</button>
      </div>
      <details><summary className="cx-hint">미리보기</summary><pre className="cx-pre">{md}</pre></details>
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
      .cx-between{justify-content:space-between}
      .cx-btn{padding:9px 12px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:13px;color:inherit}
      .cx-btn:disabled{opacity:.45}
      .cx-primary{background:var(--accent,#1f2937);color:#fff;border-color:transparent}
      .cx-mini{padding:6px 10px;font-size:12px}
      .cx-sel,.cx-in,.cx-ta{padding:9px 10px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:inherit;font-size:14px;min-width:0}
      .cx-sel{flex:1}
      .cx-in{flex:1}
      .cx-short{flex:0 0 80px}
      .cx-ta{width:100%;box-sizing:border-box;font-family:ui-monospace,monospace;font-size:12.5px}
      .cx-file{font-size:13px}
      .cx-log{font-size:12.5px;margin:0}
      .cx-log.good{color:var(--good,#16a34a)} .cx-log.bad{color:var(--bad,#dc2626)}
      .cx-hint{font-size:12.5px;color:var(--muted,#8a8f98);margin:0}
      .cx-muted{font-size:12px;color:var(--muted,#8a8f98)}
      .cx-err{font-size:13px;color:var(--bad,#dc2626)}
      .cx-tabs{display:flex;gap:6px}
      .cx-tab{flex:1;padding:8px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:transparent;color:inherit;font-size:13px}
      .cx-tab.on{background:var(--accent,#1f2937);color:#fff;border-color:transparent}
      .cx-item{border-top:1px solid var(--border,#eef0f3)}
      .cx-item-head{all:unset;cursor:pointer;display:flex;gap:10px;align-items:baseline;padding:9px 0;width:100%;flex-wrap:wrap;font-size:13.5px}
      .cx-item-body{padding:0 0 10px}
      .cx-pre{white-space:pre-wrap;font-size:12.5px;background:var(--bg2,#f6f7f9);padding:10px;border-radius:10px;margin:6px 0 0;max-height:420px;overflow:auto}
      .cx-score{font-size:13px;font-weight:600}
      .cx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px}
      .cx-cell{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:11.5px;color:var(--muted,#8a8f98)}
      .cx-cell input{width:100%;box-sizing:border-box;text-align:center;padding:8px 2px;border-radius:9px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);color:var(--text,#1c1c1e);font-size:15px}
      .cx-cell.good input{border-color:var(--good,#16a34a);background:rgba(22,163,74,.08)}
      .cx-cell.bad input{border-color:var(--bad,#dc2626);background:rgba(220,38,38,.07)}
      .cx-scroll{overflow-x:auto}
      .cx-table{border-collapse:collapse;font-size:12px;white-space:nowrap}
      .cx-table th,.cx-table td{border:1px solid var(--border,#eef0f3);padding:4px 6px;text-align:center}
      .cx-table td.good{color:var(--good,#16a34a)} .cx-table td.bad{color:var(--bad,#dc2626)}
      .cx-list{display:flex;flex-direction:column;gap:6px;max-height:320px;overflow:auto}
      .cx-set{all:unset;cursor:pointer;display:flex;flex-direction:column;gap:2px;padding:9px 11px;border:1px solid var(--border,#e5e7eb);border-radius:10px;font-size:13.5px}
      .cx-set.on{border-color:var(--accent,#1f2937);background:var(--bg2,#f6f7f9)}
      .cx-new{display:grid;grid-template-columns:1fr 1fr;gap:6px}
      .cx-file-row{display:flex;gap:8px;align-items:center;border-top:1px solid var(--border,#eef0f3);padding:8px 0;font-size:13px}
      .cx-fname{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
      .cx-tag{font-size:11px;padding:2px 7px;border-radius:99px;background:var(--bg2,#f1f2f4)}
      .cx-foot td{color:var(--muted,#8a8f98)}
    `}</style>
  );
}
