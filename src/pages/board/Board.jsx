// src/pages/board/Board.jsx — 3앱(학생·강사·학부모) 공용 게시판 (ui-v3)
// 라우트: <Board sub={sub} hash={hash} theme={theme} /> — sub 는 "#/board/" 뒤 전체 문자열(디코드 전).
//   ''|notice → 공지 목록 · community → 커뮤니티 목록 · qna → 기존 질문게시판 임베드
//   write[?board=notice] → 글쓰기(FeatureBar) · post/<id> → 글 상세+댓글(FeatureBar)
//   그 밖의 값 → 레거시 질문 딥링크 <QnaBoard initialId />
// 목록은 브라우즈 화면(상단 바는 셸이 그림) — 자체 배경(bd-root)만. 테이블 미적용 시 "준비 중" 카드로 강등.
import { useCallback, useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import QnaBoard from "../../components/QnaBoard";
import FeatureBar, { FbAct } from "../../components/FeatureBar";
import { roleLabel, roleClass, timeAgo, parseSub, isMissingTable, BOARD_META } from "./boardlib";

const PAGE = 30; // 최신 30건 + "더 보기" range 페이징

const CSS = `
.bd-root { min-height: 100vh; padding: 14px 12px 90px; box-sizing: border-box; background: var(--bg);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.bd-root * { box-sizing: border-box; }
.bd-light { --bg:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488;
  --in:#F4F6F8; --inbd:#D3D9DF; --bad:#DC2626; }
.bd-dark  { --bg:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4;
  --in:#101116; --inbd:#2B2E36; --bad:#F87171; }
.bd-wrap { max-width: 680px; margin: 0 auto; }
.bd-shared { font-size: 11.5px; color: var(--mut); margin: 0 2px 10px; }
.bd-item { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 12px 14px;
  margin-bottom: 8px; cursor: pointer; }
.bd-item-t { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.bd-title { flex: 1; min-width: 0; color: var(--ink); font-size: 14.5px; font-weight: 700;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.bd-cn { flex: none; font-size: 12px; font-weight: 700; color: var(--ac); }
.bd-meta { display: flex; align-items: center; gap: 6px; font-size: 11.5px; color: var(--mut); flex-wrap: wrap; }
.bd-name { font-weight: 700; color: var(--ink); opacity: .85; }
.bd-badge { font-size: 10.5px; font-weight: 800; border-radius: 6px; padding: 2px 7px; white-space: nowrap; flex: none; }
.bd-light .bd-r-student  { background:#CCFBF1; color:#0F766E; }
.bd-dark  .bd-r-student  { background:rgba(45,212,191,.16); color:#5EEAD4; }
.bd-light .bd-r-teacher  { background:#E0E7FF; color:#4338CA; }
.bd-dark  .bd-r-teacher  { background:rgba(129,140,248,.18); color:#A5B4FC; }
.bd-light .bd-r-guardian { background:#FEF3C7; color:#B45309; }
.bd-dark  .bd-r-guardian { background:rgba(251,191,36,.16); color:#FBBF24; }
.bd-light .bd-r-admin    { background:#334155; color:#F8FAFC; }
.bd-dark  .bd-r-admin    { background:#CBD5E1; color:#0F172A; }
.bd-light .bd-r-trial, .bd-light .bd-r-etc { background:#E5E7EB; color:#4B5563; }
.bd-dark  .bd-r-trial, .bd-dark  .bd-r-etc { background:#23262D; color:#9CA3AF; }
.bd-empty { color: var(--mut); font-size: 13.5px; text-align: center; padding: 36px 0; }
.bd-more { display: block; width: 100%; background: var(--card); border: 1px solid var(--bd); border-radius: 12px;
  color: var(--ink); font-size: 13px; font-weight: 700; padding: 12px; cursor: pointer; margin-top: 4px; }
.bd-more:disabled { opacity: .5; }
.bd-fab { position: fixed; right: 16px; bottom: 86px; z-index: 45; height: 46px; padding: 0 18px;
  border-radius: 999px; background: var(--ac); border: none; color: #fff; font-size: 13.5px; font-weight: 800;
  cursor: pointer; box-shadow: 0 8px 20px rgba(0,0,0,.22); }
.bd-dark .bd-fab { color: #08302B; }
.bd-card { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 16px; margin-bottom: 10px; }
.bd-prep { text-align: center; padding: 34px 16px; }
.bd-prep-i { font-size: 34px; margin-bottom: 8px; }
.bd-prep-t { color: var(--ink); font-size: 15px; font-weight: 800; margin: 0 0 6px; }
.bd-prep-s { color: var(--mut); font-size: 12.5px; margin: 0; line-height: 1.6; }
.bd-lab { font-size: 12px; font-weight: 700; color: var(--mut); margin: 12px 2px 6px; }
.bd-in { width: 100%; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 14px; padding: 11px 12px; outline: none; }
.bd-ta { min-height: 180px; resize: vertical; line-height: 1.6; font-family: inherit; }
.bd-cnt { text-align: right; font-size: 11px; color: var(--mut); margin: 4px 2px 0; }
.bd-err { color: var(--bad); font-size: 12.5px; margin: 10px 2px 0; }
.bd-submit { display: block; width: 100%; margin-top: 14px; background: var(--ac); border: none; border-radius: 12px;
  color: #fff; font-size: 14.5px; font-weight: 800; padding: 13px; cursor: pointer; }
.bd-dark .bd-submit { color: #08302B; }
.bd-submit:disabled { opacity: .5; }
.bd-p-title { color: var(--ink); font-size: 17px; font-weight: 800; margin: 0 0 8px; line-height: 1.45; word-break: break-word; }
.bd-p-body { color: var(--ink); font-size: 14.5px; line-height: 1.7; margin: 12px 0 0; white-space: pre-wrap; word-break: break-word; }
.bd-sec { font-size: 11px; letter-spacing: 1.2px; color: var(--mut); font-weight: 700; margin: 16px 2px 8px; }
.bd-cmt { border-top: 1px solid var(--bd); padding: 10px 2px; }
.bd-cmt-h { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-size: 11px; color: var(--mut); flex-wrap: wrap; }
.bd-cmt-x { margin-left: auto; background: none; border: none; color: var(--mut); font-size: 11px; cursor: pointer; text-decoration: underline; }
.bd-cmt-b { color: var(--ink); font-size: 13.5px; margin: 0; white-space: pre-wrap; line-height: 1.55; word-break: break-word; }
.bd-row { display: flex; gap: 8px; align-items: flex-end; margin-top: 10px; }
.bd-cta { flex: 1; min-height: 44px; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 13.5px; padding: 10px 12px; outline: none; resize: vertical; font-family: inherit; }
.bd-send { background: var(--ac); border: none; border-radius: 10px; font-weight: 800; font-size: 13px;
  padding: 12px 14px; cursor: pointer; flex: none; color: #fff; }
.bd-dark .bd-send { color: #08302B; }
.bd-send:disabled { opacity: .5; }
.bd-login { color: var(--mut); font-size: 12.5px; margin: 10px 2px 0; }
`;

/* ── 로그인 사용자 (uid + 프로필 스냅샷) ─────────────────────────────── */
function useMe() {
  const [me, setMe] = useState(undefined); // undefined=확인 중, null=비로그인
  useEffect(() => {
    let on = true;
    (async () => {
      try {
        const { data } = await supabase.auth.getUser();
        const user = data?.user;
        if (!user) { if (on) setMe(null); return; }
        const { data: prof } = await supabase.from("profiles")
          .select("username, name, role").eq("id", user.id).maybeSingle();
        if (on) setMe({ uid: user.id, name: prof?.username || prof?.name || "회원", role: prof?.role || null });
      } catch { if (on) setMe(null); }
    })();
    return () => { on = false; };
  }, []);
  return me;
}

function Badge({ role }) {
  return <span className={"bd-badge " + roleClass(role)}>{roleLabel(role)}</span>;
}

function PrepCard() {
  return (
    <div className="bd-card bd-prep">
      <div className="bd-prep-i">🚧</div>
      <p className="bd-prep-t">게시판 준비 중 — 곧 열려요</p>
      <p className="bd-prep-s">학생·강사·학부모가 함께 쓰는 게시판을 만들고 있어요. 조금만 기다려 주세요.</p>
    </div>
  );
}

/* ── 목록 (브라우즈 화면: 상단 바 없음, 자체 배경만) ──────────────────── */
function ListPage({ board, theme }) {
  const me = useMe();
  const meta = BOARD_META[board];
  const [rows, setRows] = useState(null); // null=로딩
  const [more, setMore] = useState(false);
  const [missing, setMissing] = useState(false);
  const [busy, setBusy] = useState(false);

  const load = useCallback(async (offset) => {
    setBusy(true);
    const { data, error } = await supabase.from("posts")
      .select("id, board, author_name, author_role, title, comment_n, created_at")
      .eq("board", board)
      .order("created_at", { ascending: false })
      .range(offset, offset + PAGE - 1);
    setBusy(false);
    if (error) {
      if (isMissingTable(error)) setMissing(true);
      setRows((s) => s || []); setMore(false);
      return;
    }
    const got = data || [];
    setRows((s) => (offset === 0 ? got : [...(s || []), ...got]));
    setMore(got.length === PAGE);
  }, [board]);

  useEffect(() => { setRows(null); setMissing(false); setMore(false); load(0); }, [load]);

  const canWrite = board === "community" ? !!me : me?.role === "admin";

  return (
    <div className={`bd-root bd-${theme}`}>
      <style>{CSS}</style>
      <div className="bd-wrap">
        <p className="bd-shared">학생·강사·학부모가 함께 쓰는 공간</p>
        {missing && <PrepCard />}
        {!missing && rows === null && <p className="bd-empty">불러오는 중…</p>}
        {!missing && rows !== null && rows.length === 0 && <p className="bd-empty">{meta.icon} {meta.empty}</p>}
        {!missing && (rows || []).map((p) => (
          <div key={p.id} className="bd-item" onClick={() => (location.hash = "#/board/post/" + p.id)}>
            <div className="bd-item-t">
              <span className="bd-title">{p.title}</span>
              {p.comment_n > 0 && <span className="bd-cn">💬 {p.comment_n}</span>}
            </div>
            <div className="bd-meta">
              <Badge role={p.author_role} />
              <span className="bd-name">{p.author_name || "회원"}</span>
              <span>·</span>
              <span>{timeAgo(p.created_at)}</span>
            </div>
          </div>
        ))}
        {!missing && more && (
          <button className="bd-more" disabled={busy} onClick={() => load((rows || []).length)}>
            {busy ? "불러오는 중…" : "더 보기"}
          </button>
        )}
      </div>
      {!missing && canWrite && (
        <button className="bd-fab"
          onClick={() => (location.hash = board === "notice" ? "#/board/write?board=notice" : "#/board/write")}>
          ✏️ {board === "notice" ? "공지 쓰기" : "글쓰기"}
        </button>
      )}
    </div>
  );
}

/* ── 글쓰기 (기능 화면: FeatureBar) ───────────────────────────────────── */
function WritePage({ board, theme }) {
  const me = useMe();
  const meta = BOARD_META[board];
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const backTo = board === "notice" ? "#/board/notice" : "#/board/community";

  const submit = async () => {
    const t = title.trim(), b = body.trim();
    if (!t) return setErr("제목을 입력해 주세요.");
    if (t.length > 120) return setErr("제목은 120자까지 쓸 수 있어요.");
    if (!b) return setErr("내용을 입력해 주세요.");
    if (!me || busy) return;
    setBusy(true); setErr("");
    const { data, error } = await supabase.from("posts")
      .insert({ board, title: t, body: b, user_id: me.uid })
      .select("id").single();
    setBusy(false);
    if (error) {
      if (isMissingTable(error)) setErr("게시판 준비 중이에요 — 곧 열려요.");
      else if (error.code === "42501" || /policy|denied/i.test(error.message || "")) setErr("이 게시판에 글을 쓸 권한이 없어요.");
      else setErr("저장하지 못했어요. 잠시 후 다시 시도해 주세요.");
      return;
    }
    location.hash = "#/board/post/" + data.id;
  };

  return (
    <>
      <FeatureBar theme={theme} title={board === "notice" ? "공지 쓰기" : "글쓰기"} sub={meta.name} back={backTo} />
      <div className={`bd-root bd-${theme}`}>
        <style>{CSS}</style>
        <div className="bd-wrap">
          {me === null ? (
            <div className="bd-card bd-prep">
              <div className="bd-prep-i">🔒</div>
              <p className="bd-prep-t">로그인이 필요해요</p>
              <p className="bd-prep-s">글을 쓰려면 먼저 로그인해 주세요.</p>
            </div>
          ) : (
            <>
              <p className="bd-shared">학생·강사·학부모가 함께 쓰는 공간이에요. 서로 배려하는 글을 부탁해요.</p>
              <div className="bd-lab">제목</div>
              <input className="bd-in" maxLength={120} placeholder="제목 (120자까지)"
                value={title} onChange={(e) => setTitle(e.target.value)} />
              <div className="bd-cnt">{title.length}/120</div>
              <div className="bd-lab">내용</div>
              <textarea className="bd-in bd-ta" placeholder="내용을 적어 주세요"
                value={body} onChange={(e) => setBody(e.target.value)} />
              {err && <p className="bd-err">{err}</p>}
              <button className="bd-submit" disabled={busy || !me || !title.trim() || !body.trim()} onClick={submit}>
                {busy ? "올리는 중…" : board === "notice" ? "📢 공지 올리기" : "✏️ 글 올리기"}
              </button>
            </>
          )}
        </div>
      </div>
    </>
  );
}

/* ── 글 상세 + 댓글 (기능 화면: FeatureBar) ───────────────────────────── */
function PostPage({ id, theme }) {
  const me = useMe();
  const [post, setPost] = useState(null);
  const [state, setState] = useState("loading"); // loading | ok | gone | missing
  const [cmts, setCmts] = useState([]);
  const [cmt, setCmt] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let on = true;
    (async () => {
      if (!/^\d+$/.test(id)) { setState("gone"); return; }
      const { data, error } = await supabase.from("posts").select("*").eq("id", id).maybeSingle();
      if (!on) return;
      if (error) { setState(isMissingTable(error) ? "missing" : "gone"); return; }
      if (!data) { setState("gone"); return; }
      setPost(data); setState("ok");
      const { data: cs } = await supabase.from("post_comments")
        .select("*").eq("post_id", id).order("created_at", { ascending: true });
      if (on) setCmts(cs || []);
    })();
    return () => { on = false; };
  }, [id]);

  const backTo = "#/board/" + (post?.board === "notice" ? "notice" : "community");
  const canDel = (row) => !!me && !!row && (row.user_id === me.uid || me.role === "admin");

  const delPost = async () => {
    if (!post || !window.confirm("이 글을 삭제할까요? 댓글도 함께 지워져요.")) return;
    const { error } = await supabase.from("posts").delete().eq("id", post.id);
    if (!error) location.hash = backTo;
  };

  const addCmt = async () => {
    const text = cmt.trim();
    if (!text || !me || !post || busy) return;
    setBusy(true);
    const { data, error } = await supabase.from("post_comments")
      .insert({ post_id: post.id, user_id: me.uid, body: text })
      .select().single();
    setBusy(false);
    if (!error && data) {
      setCmts((s) => [...s, data]); setCmt("");
      setPost((p) => (p ? { ...p, comment_n: (p.comment_n || 0) + 1 } : p));
    }
  };

  const delCmt = async (c) => {
    if (!window.confirm("이 댓글을 삭제할까요?")) return;
    const { error } = await supabase.from("post_comments").delete().eq("id", c.id);
    if (!error) {
      setCmts((s) => s.filter((x) => x.id !== c.id));
      setPost((p) => (p ? { ...p, comment_n: Math.max((p.comment_n || 0) - 1, 0) } : p));
    }
  };

  return (
    <>
      <FeatureBar theme={theme}
        title={post ? post.title : "게시글"}
        sub={post ? BOARD_META[post.board === "notice" ? "notice" : "community"].name : undefined}
        back={backTo}
        actions={canDel(post) ? <FbAct onClick={delPost} title="글 삭제">🗑 삭제</FbAct> : undefined} />
      <div className={`bd-root bd-${theme}`}>
        <style>{CSS}</style>
        <div className="bd-wrap">
          {state === "loading" && <p className="bd-empty">불러오는 중…</p>}
          {state === "missing" && <PrepCard />}
          {state === "gone" && (
            <div className="bd-card bd-prep">
              <div className="bd-prep-i">🍃</div>
              <p className="bd-prep-t">글을 찾을 수 없어요</p>
              <p className="bd-prep-s">삭제됐거나 잘못된 주소일 수 있어요.</p>
            </div>
          )}
          {state === "ok" && post && (
            <div className="bd-card">
              <h1 className="bd-p-title">{post.title}</h1>
              <div className="bd-meta">
                <Badge role={post.author_role} />
                <span className="bd-name">{post.author_name || "회원"}</span>
                <span>·</span>
                <span>{timeAgo(post.created_at)}</span>
              </div>
              <p className="bd-p-body">{post.body}</p>

              <p className="bd-sec">댓글 {post.comment_n > 0 ? `(${post.comment_n})` : ""}</p>
              {cmts.length === 0 && <p className="bd-login">아직 댓글이 없어요. 첫 댓글을 남겨보세요.</p>}
              {cmts.map((c) => (
                <div key={c.id} className="bd-cmt">
                  <div className="bd-cmt-h">
                    <Badge role={c.author_role} />
                    <span className="bd-name">{c.author_name || "회원"}</span>
                    <span>{timeAgo(c.created_at)}</span>
                    {canDel(c) && <button className="bd-cmt-x" onClick={() => delCmt(c)}>삭제</button>}
                  </div>
                  <p className="bd-cmt-b">{c.body}</p>
                </div>
              ))}

              {me ? (
                <div className="bd-row">
                  <textarea className="bd-cta" placeholder="댓글을 남겨보세요"
                    value={cmt} onChange={(e) => setCmt(e.target.value)} />
                  <button className="bd-send" disabled={busy || !cmt.trim()} onClick={addCmt}>등록</button>
                </div>
              ) : me === null ? (
                <p className="bd-login">댓글을 쓰려면 로그인이 필요해요.</p>
              ) : null}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

/* ── 라우터 ───────────────────────────────────────────────────────────── */
export default function Board({ sub = "", hash = "", theme = "light" }) {
  const r = parseSub(sub);
  if (r.view === "qna") return <QnaBoard theme={theme} />;
  if (r.view === "legacy") return <QnaBoard theme={theme} initialId={r.id} />;
  if (r.view === "write") return <WritePage key={"w:" + r.board} board={r.board} theme={theme} />;
  if (r.view === "post") return <PostPage key={"p:" + r.id} id={r.id} theme={theme} />;
  return <ListPage key={"l:" + r.board} board={r.board} theme={theme} />;
}
