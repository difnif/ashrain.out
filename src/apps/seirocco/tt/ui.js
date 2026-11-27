/* 애쉬레인 강사도구 PC — 화면 (2026-11-10)
   라우트: #/tt/convert · #/tt/register · #/tt/grade[/코드[/학생id]] · #/tt/class · #/tt/students[/id] · #/tt/prints · #/tt/print/코드 · #/tt/log */
import * as B from "./backend";
import { importView, pcAutoSync } from "./importer";
import { autoJudge, judge, TEMPLATES, parseProgress, parsePages, todayStr } from "./logic";
import * as S from "./share";
import { splitLabel, partLabel } from "./parts";

const PH = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7";

export function mountTeacherTool(root) {
const $ = (s, el = root) => el.querySelector(s);
const $$ = (s, el = root) => [...el.querySelectorAll(s)];
const view = $("#tt-view");
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const CODE_ALPHA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ";
const normCode = (s) => String(s || "").toUpperCase().split("").filter((c) => CODE_ALPHA.includes(c)).join("");
const fmtCode = (c) => (c && c.length === 6 ? c.slice(0, 3) + "-" + c.slice(3) : c || "");
// 저장 공간 파일은 비공개라 서명 주소가 필요 — 일단 빈 그림 + #tt=경로 로 두고 아래 풀이기가 바꾼다
const urlCache = new Map();          // rel → {u, t} — 다시 그릴 때 깜빡이지 않게 (서명 주소는 1시간이라 45분만 씀)
const fileUrl = (rel) => {
  const c = urlCache.get(String(rel));
  return c && (c.u.startsWith("blob:") || Date.now() - c.t < 45 * 60 * 1000) ? c.u : PH + "#tt=" + encodeURIComponent(String(rel));
};
const splitNames = (s) => String(s || "").split(/[\n,，、;·\t]+|\s{2,}/).map((x) => x.trim()).filter(Boolean)
  .flatMap((x) => (/^[가-힣]{2,4}( [가-힣]{2,4})+$/.test(x) ? x.split(" ") : [x]));
const store = {
  get(k, d) { try { const v = localStorage.getItem("tt:" + k); return v == null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("tt:" + k, JSON.stringify(v)); } catch { /* 저장 안 돼도 됨 */ } },
};
// 화면을 그리는 중에 다른 화면으로 옮기면(또는 다시 그리면), 앞 화면이 늦게 받은 읽기(GET) 결과는 버린다 — 늦게 끝난 앞 화면이 새 화면을 덮지 않게.
// 보내기(POST)는 늘 끝까지 간다.
let routeSeq = 0;
const api = (path, body) => {
  if (body !== undefined) return B.api(path, body);
  const seq = routeSeq;
  return B.api(path).then((r) => (seq === routeSeq ? r : new Promise(() => {})), (e) => (seq === routeSeq ? Promise.reject(e) : new Promise(() => {})));
};
const upload = (file) => B.upload(file);
const uploadScan = (gid, file, round = null) => B.uploadScan(gid, file, round);

// PC가 내려 주던 /dl · /out · /scan 주소와 저장 공간 파일 열기·받기
async function openLink(href, download = false) {
  const w = download ? null : window.open("", "_blank");
  try {
    const r = href.startsWith("@file:") ? { url: (await B.resolve([href.slice(6)]))[href.slice(6)], name: href.slice(6).split("/").pop() } : await B.link(href);
    let url = r.url, name = r.name || "파일";
    if (r.json) url = URL.createObjectURL(new Blob([JSON.stringify(r.json, null, 1)], { type: "application/json" }));
    if (r.pdf) url = URL.createObjectURL(new Blob([r.pdf], { type: "application/pdf" }));
    if (r.blob) url = URL.createObjectURL(r.blob);
    if (!url) throw new Error("파일을 찾지 못했어요");
    if (w && !r.json && (r.view !== false)) { w.location.href = url; return; }
    if (w) w.close();
    const a = document.createElement("a");
    a.href = url; a.download = name; document.body.appendChild(a); a.click();
    setTimeout(() => a.remove(), 1000);
  } catch (e) {
    if (w) w.close();
    toast(e.message, 4000);
  }
}
root.addEventListener("click", (e) => {
  const a = e.target.closest("a[href]");
  if (!a || !root.contains(a)) return;
  const h = a.getAttribute("href");
  if (/^\/(dl|out|scan)\//.test(h)) { e.preventDefault(); openLink(h, a.hasAttribute("download") || /[?&]dl=1/.test(h)); }
  else if (h.includes("#tt=")) { e.preventDefault(); openLink("@file:" + decodeURIComponent(h.split("#tt=")[1]), a.hasAttribute("download")); }
}, true);
// 그림 주소 풀이기 (서명 주소·쪽 그림)
let resolving = false;
async function resolveFiles() {
  if (resolving) return;
  resolving = true;
  try {
    for (let pass = 0; pass < 3; pass++) {
      const els = $$('[src*="#tt="]').concat($$('a[href*="#tt="]').filter((a) => a.dataset.keep !== "1"));
      if (!els.length) break;
      const rels = [...new Set(els.map((el) => decodeURIComponent((el.getAttribute("src") || el.getAttribute("href")).split("#tt=")[1])))];
      let map = {};
      try { map = await B.resolve(rels); } catch (err) { console.warn(err); break; }
      for (const el of els) {
        const at = el.hasAttribute("src") ? "src" : "href";
        const rel = decodeURIComponent(el.getAttribute(at).split("#tt=")[1]);
        if (map[rel]) { el.setAttribute(at, map[rel]); urlCache.set(rel, { u: map[rel], t: Date.now() }); }
        else if (at === "src") el.setAttribute(at, PH);
      }
    }
  } finally { resolving = false; }
}
const mo = new MutationObserver(() => { clearTimeout(mo.t); mo.t = setTimeout(resolveFiles, 30); });
mo.observe(root, { subtree: true, childList: true, attributes: true, attributeFilter: ["src", "href"] });

/* 스캔본 칸: 채점 하나의 학생 풀이 스캔본 올리기·보기·내려받기·지우기
   + 언제 스캔한 것인지(1차 채점 때 · 2차 채점 때 · 확실하지 않음) — 안 고르고 파일을 놓으면 잡아 두었다가 고르면 올림.
   opts.rounds = 그 채점의 차 수(3차까지 했으면 3차도 고를 수 있게) · opts.meta = {title, student}(vFlat 공유로 받을 때 파일 이름)
   안드로이드: 「vFlat으로 스캔」 → vFlat에서 「공유 → 강사도구」(앱으로 설치했을 때) → 이 채점 · 고른 차수로 저절로 올라감(#/tt/inbox) */
const whenText = (r) => (r ? `${r}차 채점 때` : "확실하지 않음");
const BOOK_R = 3;           // 교재 스캔본은 1 · 2 · 3차 채점 때 / 확실하지 않음 중에서 고름
function scanPanel(el, gid, scans, onChange = () => {}, opts = {}) {
  let pick = "";                 // "1" · "2" · … · "u"(확실하지 않음)
  let pending = [], busy = false, vwant = false;
  const android = S.isAndroid() && B.scanRoundOk();
  const nR = () => Math.max(2, opts.rounds || 1, ...scans.map((x) => x.round || 0));
  const choices = () => [...Array.from({ length: nR() }, (_, i) => [String(i + 1), whenText(i + 1)]), ["u", "확실하지 않음"]];
  const roundOf = (v) => (v && v !== "u" ? Number(v) : null);
  const counts = () => {
    const c = new Map();
    for (const x of scans) c.set(x.round || 0, (c.get(x.round || 0) || 0) + 1);
    return [...c.entries()].sort((a, b) => (a[0] || 99) - (b[0] || 99)).map(([r, n]) => `${r ? r + "차" : "확실하지 않음"} ${n}`).join(" · ");
  };
  const add = async (files) => {
    if (!files.length) return;
    if (busy) return toast("올리는 중이에요. 끝난 뒤에 다시 놓아 주세요");
    const ok = B.scanRoundOk();
    if (ok && !pick) { pending = files; draw(); return; }         // 언제 스캔한 것인지부터
    busy = true; pending = []; draw();
    const rd = ok ? roundOf(pick) : null;
    let n = 0;
    for (const f of files) {
      try { const r = await uploadScan(gid, f, rd); scans = r.scans; n++; } catch (e) { toast(f.name + ": " + e.message, 4000); }
    }
    busy = false;
    if (n) toast(`${n === 1 ? files[0].name : `스캔본 ${n}개`} 올렸어요${ok ? ` · ${whenText(rd)}` : ""}`);
    if (el.isConnected) draw();
    onChange(scans);
  };
  const draw = () => {
    const ok = B.scanRoundOk(), wait = (pending.length || vwant) && !pick;
    const sw = S.getScanWait(), waiting = sw && sw.gid === gid;
    el.innerHTML = `${ok ? `<div class="scanwhen${wait ? " need" : ""}"><b>언제 스캔한 것인가요?</b><span data-sseg></span>
        ${pending.length && !pick ? `<span class="small"><b>파일 ${pending.length}개를 골랐어요.</b> 언제 스캔한 것인지 고르면 바로 올라가요.</span><button class="btn ghost small" data-scancel>그만두기</button>`
          : vwant && !pick ? `<span class="small"><b>먼저 언제 스캔한 것인지 골라 주세요.</b> 그다음 「vFlat으로 스캔」</span>`
          : `<span class="sub small">${pick ? `지금 올리는 것: <b>${esc(whenText(roundOf(pick)))}</b>` : "먼저 고른 뒤 파일을 놓아도, 파일을 놓은 뒤 골라도 돼요"}</span>`}</div>`
        : `<p class="sub small" style="margin:0 0 8px">1차·2차 표시는 DB에 칸을 하나 더하면 켜져요 (supabase/2026-11_tt_scans_round.sql)</p>`}
      ${android ? `<div class="vflat"><a class="btn" data-vflat href="${esc(S.vflatHref())}">📷 vFlat으로 스캔</a>
        ${waiting ? `<span class="small"><b>vFlat에서 「공유 → 강사도구」를 기다리는 중</b> · ${esc(whenText(sw.round))} <button class="btn ghost small" data-vstop>그만두기</button></span>`
          : `<span class="sub small">스캔한 뒤 vFlat에서 「공유 → 강사도구」를 누르면 이 채점에 프린트 이름으로 올라와요</span>`}
        ${S.isStandalone() ? "" : S.canPromptInstall() ? `<button class="btn ghost small" data-install>강사도구를 이 기기에 앱으로 설치</button>`
          : `<span class="sub small">처음 한 번: Chrome 메뉴 ⋮ → 「앱 설치」(또는 「홈 화면에 추가」)를 해야 공유 목록에 「강사도구」가 생겨요</span>`}</div>` : ""}
      <div class="drop small-drop" data-sdrop>${busy ? `<b><span class="busy"></span>올리는 중…</b>` : `<b>스캔본(PDF·사진)을 끌어다 놓거나 눌러서 고르기</b><span class="sub small">여러 개 가능 · 나중에 분석용 내보내기에 같이 들어가요</span>`}
        <input type="file" accept=".pdf,image/*" multiple hidden></div>
      ${scans.length ? `<div class="scanlist">${scans.map((x) => `<div class="file">${x.kind === "pdf" ? "📄" : "🖼"} <a href="/scan/${x.id}" target="_blank">${esc(x.name)}</a>
        <span class="muted small">${x.pages}쪽 · ${(x.size / 1048576).toFixed(1)}MB · ${shortWhen(x.created_at)}</span>
        ${ok ? `<select class="tin sround${x.round ? "" : " unk"}" data-sround="${x.id}" title="언제 스캔한 것인지">${choices().map(([v, t]) => `<option value="${v}"${String(x.round || "u") === v ? " selected" : ""}>${esc(t)}</option>`).join("")}</select>` : ""}
        <a class="btn ghost small"${ok ? "" : ` style="margin-left:auto"`} href="/scan/${x.id}?dl=1">받기</a><button class="x" data-sdel="${x.id}" title="지우기">×</button></div>`).join("")}</div>
        <div class="row" style="margin-top:8px">${ok ? `<span class="sub small">${esc(counts())}</span>` : ""}<a class="btn ghost small" href="/scan/all/${gid}.pdf" target="_blank" title="1차 → 2차 → 확실하지 않음 차례">한 PDF로 보기</a><a class="btn ghost small" href="/scan/all/${gid}.pdf?dl=1">한 PDF로 받기</a></div>` : ""}`;
    if (ok) seg($("[data-sseg]", el), choices(), pick, (v) => { pick = v; vwant = false; if (pending.length) add(pending); else draw(); });
    if ($("[data-scancel]", el)) $("[data-scancel]", el).onclick = () => { pending = []; draw(); };
    if ($("[data-vflat]", el)) $("[data-vflat]", el).onclick = (e) => {
      if (!pick) { e.preventDefault(); vwant = true; draw(); return; }          // 언제 스캔한 것인지부터
      S.setScanWait({ gid, round: roundOf(pick), title: (opts.meta || {}).title || "", student: (opts.meta || {}).student || "" });
      setTimeout(() => { if (el.isConnected) draw(); }, 300);                   // 기다리는 중 표시 (vFlat이 열리는 동안)
    };
    if ($("[data-vstop]", el)) $("[data-vstop]", el).onclick = () => { S.clearScanWait(); draw(); };
    if ($("[data-install]", el)) $("[data-install]", el).onclick = async () => { const okI = await S.promptInstall(); toast(okI ? "앱으로 설치했어요. 이제 vFlat 공유 목록에 「강사도구」가 보여요" : "설치하지 않았어요"); draw(); };
    const dz = $("[data-sdrop]", el), fin = $("input", dz);
    dz.onclick = () => { if (!busy) fin.click(); };
    fin.onchange = () => { add([...fin.files]); fin.value = ""; };
    ["dragenter", "dragover"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.add("over"); }));
    ["dragleave", "drop"].forEach((ev) => dz.addEventListener(ev, (e) => { e.preventDefault(); dz.classList.remove("over"); }));
    dz.addEventListener("drop", (e) => add([...e.dataTransfer.files]));
    $$("[data-sround]", el).forEach((s) => (s.onchange = async () => {
      try { const r = await api("scans/" + s.dataset.sround, { round: roundOf(s.value) }); scans = r.scans; toast(`${whenText(roundOf(s.value))}(으)로 바꿨어요`); }
      catch (e) { toast(e.message, 5000); }
      draw(); onChange(scans);
    }));
    $$("[data-sdel]", el).forEach((b) => (b.onclick = async () => {
      const x = scans.find((s) => String(s.id) === b.dataset.sdel);
      if (!confirmInline(b)) return;
      try { const r = await api("scans/" + b.dataset.sdel, { delete: true }); scans = r.scans; toast(`${x ? x.name : "스캔본"} 지웠어요`); } catch (e) { toast(e.message); }
      draw(); onChange(scans);
    }));
  };
  draw();
}
// 창 안에서는 창을 하나 더 띄울 수 없어서(창이 하나뿐) 지우기 확인은 그 자리에서: 한 번 누르면 「지울까요?」, 3초 안에 한 번 더 누르면 지움
function confirmInline(b) {
  if (b.dataset.armed === "1") return true;
  b.dataset.armed = "1"; const t = b.textContent; b.textContent = "지울까요?"; b.classList.add("armed");
  setTimeout(() => { if (b.isConnected) { b.dataset.armed = ""; b.textContent = t; b.classList.remove("armed"); } }, 3000);
  return false;
}
const scanLabel = (scans) => (scans && scans.length ? `스캔본 ${scans.length}` : "스캔본 올리기");
// [data-scan=채점id] 단추 (data-r = 차 수, data-t = 프린트 제목, data-n = 학생 이름) → 스캔본 창, 닫으면 단추 글자를 개수로
// afterClose(단추, 스캔본 목록) — 창을 닫은 뒤 화면을 다시 그릴 때(교재 화면: 스캔본이 생기면 「빼기」를 감춤)
function bindScanButtons(el, nameOf = (b) => b.dataset.n || "", afterClose = null) {
  $$("[data-scan]", el).forEach((b) => (b.onclick = async (e) => {
    e.stopPropagation();
    const sc = await scanModal(+b.dataset.scan, `${esc(nameOf(b))} · ${esc(b.dataset.t || "")} · 스캔본`, { rounds: +b.dataset.r || 1, meta: { title: b.dataset.t || "", student: nameOf(b) },
      onChange: (x) => { b.textContent = scanLabel(x); } });
    if (afterClose && sc) afterClose(b, sc);
  }));
}
// 스캔본 창 — 채점 화면·학생 기록·프린트 채점 기록에서 같이 씀
async function scanModal(gid, titleHtml, { rounds = 1, scans = null, meta = null, onChange = () => {} } = {}) {
  if (!scans) { try { scans = await api(`gradings/${gid}/scans`); } catch (e) { toast(e.message); return null; } }
  await modal(`<h2>${titleHtml}</h2><div id="scanBox"></div>`, [{ label: "닫기", value: null, cls: "ghost" }],
    { cls: "scanmodal", onOpen: (box) => scanPanel($("#scanBox", box), gid, scans, (sc) => { scans = sc; onChange(sc); }, { rounds, meta }) });
  return scans;
}

let toastT = 0;
// action = { label, fn } — 알림 안에 단추(예: 「되돌리기」)를 붙이고 조금 더 오래 보여 준다
function toast(msg, ms = 2600, action = null) {
  const t = $("#tt-toast");
  if (action) {
    t.innerHTML = `<span>${esc(msg)}</span><button type="button" class="tbtn">${esc(action.label)}</button>`;
    $("button", t).onclick = async () => { t.hidden = true; try { await action.fn(); } catch (e) { toast(e.message, 5000); } };
    ms = Math.max(ms, 8000);
  } else t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastT);
  toastT = setTimeout(() => (t.hidden = true), ms);
}
// 입력을 마친 뒤 알림 + 「되돌리기」(업무 기록에 남긴 것을 되돌림)
function undoToast(msg, events) {
  if (!events || !events.length) return toast(msg);
  toast(msg, 8000, { label: "되돌리기", fn: async () => { const r = await api("undo", { events }); toast(r.n > 1 ? `${r.n}개 되돌렸어요` : "되돌렸어요"); route(); } });
}

/* 모달: actions = [{label, value, cls}] → 고른 value (바깥 클릭·Esc = null) */
function modal(html, actions = [{ label: "닫기", value: null, cls: "ghost" }], opts = {}) {
  return new Promise((resolve) => {
    const m = $("#tt-modal"), box = $("#tt-modalBox");
    box.className = "modal-box" + (opts.cls ? " " + opts.cls : "");
    box.innerHTML = html + (actions.length ? `<div class="modal-actions">${actions.map((a, i) =>
      `<button class="btn ${a.cls || ""}" data-i="${i}">${esc(a.label)}</button>`).join("")}</div>` : "");
    m.hidden = false;
    const done = (v) => { m.hidden = true; box.innerHTML = ""; document.removeEventListener("keydown", onKey, true); resolve(v); };
    const onKey = (e) => { if (e.key === "Escape") { e.stopPropagation(); done(null); } };
    document.addEventListener("keydown", onKey, true);
    m.onclick = (e) => { if (e.target === m) done(null); };
    $$(".modal-actions button", box).forEach((b) => (b.onclick = () => done(actions[+b.dataset.i].value)));
    if (opts.onOpen) opts.onOpen(box, done);
  });
}
const zoom = (src) => modal(`<img src="${esc(src)}" alt="">`, [], { cls: "zoom" });

const STATUS = {
  open: ["채점 중", "open"], done: ["채점 완료", "done"],
  paused_unsolved: ["덜 풂 · 이어서 채점", "pause"], paused_ungraded: ["채점 덜 함", "pause"],
};
const statusTag = (s) => { const [t, c] = STATUS[s] || [s, ""]; return `<span class="tag ${c}">${esc(t)}</span>`; };
const sumText = (s) => !s ? "" : `<span class="tag o">O ${s.O}</span> <span class="tag x">X ${s.X}</span>` +
  (s.U ? ` <span class="tag u">안 풂 ${s.U}</span>` : "") + (s.none ? ` <span class="tag">남음 ${s.none}</span>` : "");
const CIRC = { 1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤" };
// 목록용: 2차 이상이면 "1차 O 13 · X 8 → 최종" 한 줄을 덧붙임
const roundNote = (g) => !g || !g.n_rounds || g.n_rounds < 2 || !g.summary1 ? "" :
  `<div class="small muted">1차 O ${g.summary1.O} · X ${g.summary1.X}${g.summary1.U ? " · 안 풂 " + g.summary1.U : ""} → ${g.n_rounds}차까지 다시 풀어 최종</div>`;
const KIND_KO = { registered: "등록", wrong: "오답 모음" };
const nolab = (it) => it.label || String(it.seq);            // 등록 프린트는 "서답형 1" 같은 원래 번호
const nob = (it) => (/^\d+$/.test(nolab(it)) ? nolab(it) + "번" : nolab(it));
const groupBy = (arr, key) => { const m = new Map(); for (const x of arr) { const k = key(x); if (!m.has(k)) m.set(k, []); m.get(k).push(x); } return m; };
const day = (s) => (s || "").slice(0, 10);
const hm = (s) => (s || "").slice(11, 16);
const shortWhen = (s) => { if (!s) return ""; const d = day(s); return (d === today ? "오늘 " : d.slice(5).replace("-", "/") + " ") + hm(s); };
let today = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);

/* ───────────────────────── 라우터 (채점 중 이탈 확인 포함) */
let leaveGuard = null;      // () => Promise<boolean>
let curHash = location.hash;
let busyNav = false;
const onHash = async () => {
  if (busyNav) return;
  if (!location.hash.startsWith("#/tt")) return;      // 시록고의 다른 탭으로 — 뒷정리는 unmount 에서
  if (leaveGuard) {
    const target = location.hash;
    history.replaceState(null, "", curHash || "#/tt/convert");
    busyNav = true;
    let ok = false;
    try { ok = await leaveGuard(); } finally { busyNav = false; }
    if (!ok) return;
    leaveGuard = null;
    if (location.hash === target) route(); else location.hash = target;
    return;
  }
  route();
};
window.addEventListener("hashchange", onHash);
const onUnload = (e) => { if (leaveGuard && leaveGuard.dirty && leaveGuard.dirty()) { e.preventDefault(); e.returnValue = ""; } };
window.addEventListener("beforeunload", onUnload);

function route() {
  routeSeq++;
  curHash = location.hash;
  const parts = (location.hash.replace(/^#\/?(tt\/?)?/, "") || "grade").split("/").map(decodeURIComponent);
  const tab = { print: "prints", wrong: "students", parts: "prints" }[parts[0]] || parts[0];
  $$("#tt-tabs a").forEach((a) => a.classList.toggle("on", a.dataset.tab === tab));
  window.scrollTo(0, 0);
  document.onkeydown = null;
  if (!location.hash.startsWith("#/tt")) return;
  const R = { convert: viewConvert, register: viewRegister, grade: viewGrade, class: viewClass, students: viewStudents, prints: viewPrints, print: viewPrint, log: viewLog,
    export: viewExport, account: viewAccount, wrong: viewWrong, inbox: viewInbox, parts: viewParts, books: viewBooks,
    import: (...a) => importView({ view, $, $$, esc, toast, modal, api, fmtCode }, ...a) }[parts[0]];
  view.innerHTML = `<div class="card"><span class="busy"></span>불러오는 중…</div>`;
  refreshInboxTab();
  (R || viewConvert)(...parts.slice(1)).catch((e) => { view.innerHTML = `<div class="card"><h2>문제가 생겼어요</h2><p class="sub">${esc(e.message)}</p></div>`; });
}

$("#tt-codeForm").onsubmit = (e) => {
  e.preventDefault();
  const c = normCode($("#tt-codeInput").value);
  if (c.length !== 6) return toast("코드 6글자를 넣어 주세요 (예: 7KQ-3MP)");
  $("#tt-codeInput").value = "";
  location.hash = "#/tt/grade/" + c;
};
$("#tt-codeInput").addEventListener("input", (e) => {
  const c = normCode(e.target.value);
  e.target.value = c.length > 3 ? c.slice(0, 3) + "-" + c.slice(3, 6) : c;
});

/* 학생 이름 칩 입력: 쉼표·줄바꿈·Enter로 나눔 + 기존 학생 고르기 */
function nameChips(el, students, initial = [], onChange = () => {}) {
  let names = [...new Set(initial)];
  const draw = () => {
    const active = students.filter((s) => s.active && !names.includes(s.name));
    el.innerHTML = `<div class="chips">${names.map((n, i) => `<span class="chip sel">${esc(n)}<button data-i="${i}" title="빼기">×</button></span>`).join("")}
      <input class="tin" placeholder="${names.length ? "더 넣기" : "이름 입력 (쉼표·Enter로 여러 명)"}"></div>
      ${active.length ? `<div class="chips" style="margin-top:6px">${active.slice(0, 40).map((s) => `<span class="chip pick" data-n="${esc(s.name)}">+ ${esc(s.name)}</span>`).join("")}</div>` : ""}`;
    const inp = $("input", el);
    const add = () => { const v = splitNames(inp.value); if (v.length) { names = [...new Set([...names, ...v])]; draw(); onChange(names); $("input", el).focus(); } };
    inp.onkeydown = (e) => {
      if (e.isComposing) return;
      if (e.key === "Enter" || e.key === ",") { e.preventDefault(); add(); }
      if (e.key === "Backspace" && !inp.value && names.length) { names.pop(); draw(); onChange(names); $("input", el).focus(); }
    };
    inp.onblur = add;
    inp.onpaste = () => setTimeout(add, 0);
    $$(".chip.sel button", el).forEach((b) => (b.onclick = () => { names.splice(+b.dataset.i, 1); draw(); onChange(names); }));
    $$(".chip.pick", el).forEach((c) => (c.onclick = () => { names.push(c.dataset.n); draw(); onChange(names); }));
  };
  draw();
  return { get: () => { const inp = $("input", el); if (inp && inp.value.trim()) { names = [...new Set([...names, ...splitNames(inp.value)])]; } return names; } };
}

function seg(el, options, value, onChange) {
  el.classList.add("seg");
  el.innerHTML = options.map(([v, t]) => `<button type="button" data-v="${esc(v)}" class="${v === value ? "on" : ""}">${esc(t)}</button>`).join("");
  $$("button", el).forEach((b) => (b.onclick = () => { $$("button", el).forEach((x) => x.classList.toggle("on", x === b)); onChange(b.dataset.v); }));
}

/* ───────────────────────── 1. 변환 */
async function viewConvert(arg) {
  const [settings, students] = await Promise.all([api("settings"), api("students")]);
  today = settings.today || today;
  const d = settings.defaults || {};
  const st = { files: [], template: d.template || "문정중", label: d.label || "서답형", mode: d.mode || "each" };
  view.innerHTML = `
    <h1>매쓰플랫 프린트 → 시험지 변환</h1>
    <div class="grid2">
      <div>
        <div class="drop" id="drop"><b>PDF를 여기에 끌어다 놓으세요</b><span class="sub">또는 눌러서 고르기 · 여러 개 가능 · 빠른정답 PDF를 같이 놓으면 정답이 채워져요</span>
          <input type="file" id="fileIn" accept=".pdf,application/pdf" multiple hidden></div>
        <div class="files" id="files"></div>
      </div>
      <div class="card" style="margin:0">
        <div class="opt">
          <label class="k">양식</label><div id="oTpl"></div>
          <label class="k">주관식 표시</label><div id="oLabel"></div>
          <label class="k" id="kMode">여러 파일</label><div id="oMode"></div>
          <label class="k">출제 대상</label><div id="oTargets"></div>
          <label class="k">정답·해설</label><label class="small"><input type="checkbox" id="oAnsDesign" ${d.answer_design === false ? "" : "checked"}> 빠른 정답·해설지도 같은 양식으로 다시 짜기</label>
        </div>
        <p class="sub small" style="margin:8px 0 0">PDF에 학생 이름이 적혀 있어도 지운 <b>이름 없는 판</b>으로 저장해요. 이름은 출력할 때 넣어요.</p>
        <details><summary>제목·윗줄 바꾸기 (비우면 설정.json 값)</summary>
          <div class="opt">
            <label class="k">제목</label><input class="tin" id="oTitle" placeholder="비우면 파일 이름에서">
            <label class="k">부제</label><input class="tin" id="oSub">
            <label class="k">윗줄</label><input class="tin" id="oUpper" value="${esc(d.upper || "")}" placeholder="예: 2026학년도 2학기">
            <label class="k">바닥글</label><input class="tin" id="oFooter" value="${esc(d.footer || "")}">
          </div></details>
        <div class="row" style="margin-top:12px"><button class="btn big" id="go" disabled>변환하기</button><span class="sub small" id="goHint">PDF를 먼저 넣어 주세요</span></div>
      </div>
    </div>
    <div id="out"></div>`;
  seg($("#oTpl"), TEMPLATES, st.template, (v) => (st.template = v));
  seg($("#oLabel"), [["서답형", "서답형"], ["단답형", "단답형"]], st.label, (v) => (st.label = v));
  seg($("#oMode"), [["each", "파일마다 따로 (일괄)"], ["merge", "하나로 합치기"]], st.mode, (v) => { st.mode = v; draw(); });
  const targets = nameChips($("#oTargets"), students, []);
  const fileIn = $("#fileIn"), drop = $("#drop");
  const add = (list) => {
    for (const f of list) {
      if (!/\.pdf$/i.test(f.name)) { toast(f.name + ": PDF만 넣을 수 있어요"); continue; }
      if (!st.files.some((x) => x.name === f.name && x.size === f.size)) st.files.push(f);
    }
    draw();
  };
  const draw = () => {
    $("#files").innerHTML = st.files.map((f, i) => `<div class="file">📄 ${esc(f.name)} <span class="muted small">${(f.size / 1048576).toFixed(1)}MB</span><button class="x" data-i="${i}" title="빼기">×</button></div>`).join("");
    $$("#files .x").forEach((b) => (b.onclick = () => { st.files.splice(+b.dataset.i, 1); draw(); }));
    const many = st.files.length > 1;
    $("#kMode").style.display = $("#oMode").style.display = many ? "" : "none";
    $("#go").disabled = !st.files.length;
    $("#goHint").textContent = !st.files.length ? "PDF를 먼저 넣어 주세요" : many && st.mode === "each" ? `시험지 ${st.files.length}개 · 코드 ${st.files.length}개` : "시험지 1개 · 코드 1개";
  };
  drop.onclick = () => fileIn.click();
  fileIn.onchange = () => { add(fileIn.files); fileIn.value = ""; };
  ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => add(e.dataTransfer.files));
  draw();
  $("#go").onclick = async () => {
    const btn = $("#go");
    btn.disabled = true;
    const out = $("#out");
    try {
      const ups = [];
      for (let i = 0; i < st.files.length; i++) {
        out.innerHTML = `<div class="card"><span class="busy"></span>올리는 중… (${i + 1}/${st.files.length})</div>`;
        ups.push(st.files[i].uploaded || await upload(st.files[i]));
      }
      out.innerHTML = `<div class="card"><span class="busy"></span>변환하는 중… 파일당 몇 초 걸려요</div>`;
      const r = await api("convert", {
        uploads: ups.map((u) => ({ id: u.id, name: u.name })),
        options: { template: st.template, label: st.label, mode: st.files.length > 1 ? st.mode : "each", targets: targets.get(),
          title: $("#oTitle").value, sub: $("#oSub").value, upper: $("#oUpper").value, footer: $("#oFooter").value,
          answer_design: $("#oAnsDesign").checked },
      });
      const anonN = r.made.reduce((a, p) => a + (p.anon_removed || 0), 0);
      out.innerHTML = `<h2 style="margin-top:18px">만든 시험지</h2>` + (anonN ? `<div class="card" style="background:#f0fdf4;border-color:#bbf7d0">PDF에 적힌 학생 이름을 지우고 이름 없는 판으로 저장했어요. 이름은 「이름 넣어 출력」에서 넣어요.</div>` : "") + r.made.map(printCard).join("") +
        r.errors.map((e) => `<div class="card" style="border-color:#fca5a5"><b>변환 못 함</b> · ${esc(e.files.join(", "))}<div class="sub small">${esc(e.error)}</div></div>`).join("");
      bindPrintCards(out);
      st.files = []; draw();
      toast(`${r.made.length}개 만들었어요` + (r.errors.length ? ` · ${r.errors.length}개 실패` : ""));
    } catch (e) {
      out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>변환 못 함</b><div class="sub">${esc(e.message)}</div></div>`;
    } finally { btn.disabled = !st.files.length; }
  };
}

function printCard(p) {
  return `<div class="card"><div class="result">
    <span class="codebig">${esc(p.code_fmt)}</span>
    <div style="flex:1;min-width:200px"><b style="font-size:17px">${esc(p.title)}</b>
      <div class="sub small">${p.kind === "registered" ? "등록한 프린트" : p.kind === "wrong" ? "오답 모음 · " + esc(p.template) + " 양식" : esc(p.template) + " 양식"} · ${p.n_items}문항 (객관식 ${p.n_choice}) · ${p.pages}쪽 · 대상 ${p.targets.length ? p.targets.map((t) => esc(t.name)).join(", ") : "<span class='muted'>미지정</span>"}</div></div>
    <div class="row">
      <a class="btn ghost" href="/out/${p.code}/sheet.pdf" target="_blank" title="저장된 이름 없는 판">시험지 PDF</a>
      <button class="btn ghost" data-out="${p.code}" title="고른 학생 이름을 넣은 사본을 한 파일로">이름 넣어 출력</button>
      ${p.answer_pdf ? `<a class="btn ghost" href="${fileUrl(p.answer_pdf)}" target="_blank">정답해설 PDF</a>` : ""}
      <a class="btn ghost" href="#/tt/print/${p.code}" title="${p.n_answer_imgs ? `빠른정답 그림 ${p.n_answer_imgs}문항 · 글자 정답 ${p.n_answers}문항(자동 채점 가능)` : ""}">정답 ${p.n_answer_imgs ? `✓ ${p.n_answer_imgs}/${p.n_items}` : p.n_answers ? `(${p.n_answers}/${p.n_items})` : "입력"}</a>
      <a class="btn" href="#/tt/grade/${p.code}">채점</a>
    </div></div></div>`;
}
function bindPrintCards(el) {
  $$("[data-out]", el).forEach((b) => (b.onclick = () => printOut(b.dataset.out)));
}

/* 이름 넣어 출력: 고른 학생마다 이름을 찍은 사본을 한 파일로 (저장본은 이름 없는 판 그대로) */
async function printOut(code, onlySid) {
  const openPdf = (sids, blank) => openLink(`/out/${code}/sheet.pdf?sid=${sids.join(",")}${blank ? "&blank=1" : ""}`);
  if (onlySid) return openPdf([onlySid], false);
  const [p, students] = await Promise.all([api("prints/" + code), api("students")]);
  const tset = new Set(p.targets.map((t) => t.id));
  const list = [...p.targets.map((t) => ({ id: t.id, name: t.name })), ...students.filter((s) => s.active && !tset.has(s.id)).map((s) => ({ id: s.id, name: s.name }))];
  const sel = new Set(p.targets.map((t) => t.id));
  let blank = false, rec = true;
  const v = await modal(`<h2>이름 넣어 출력 <span class="code sub">${esc(p.code_fmt)}</span></h2>
    <p class="sub small">고른 학생마다 이름을 넣은 사본을 <b>한 파일</b>로 이어 붙여요. 강사도구에 저장된 프린트는 이름 없는 판 그대로예요.
    ${p.has_name_box ? "" : "<br>이 프린트는 이름 칸을 못 찾아서 첫 쪽 왼쪽 위에 작게 넣어요."}</p>
    <div class="chips" id="oSel">${list.map((s) => `<span class="chip ${sel.has(s.id) ? "sel" : "pick"}" data-id="${s.id}">${esc(s.name)}${tset.has(s.id) ? ` <span class="small" style="opacity:.6">대상</span>` : ""}</span>`).join("") || `<span class="empty">학생이 없어요</span>`}</div>
    <div class="row" style="margin-top:10px"><label class="small"><input type="checkbox" id="oBlank"> 이름 없는 1부도 같이</label>
      <label class="small"><input type="checkbox" id="oRec" checked> 고른 학생을 출제 대상으로 기록</label></div>`,
    [{ label: "그만두기", value: null, cls: "ghost" }, { label: "PDF 만들기", value: "go" }],
    { onOpen: (box) => {
      $$("#oSel .chip", box).forEach((c) => (c.onclick = () => { const id = +c.dataset.id; sel.has(id) ? sel.delete(id) : sel.add(id); c.classList.toggle("sel", sel.has(id)); c.classList.toggle("pick", !sel.has(id)); }));
      $("#oBlank", box).onchange = (e) => (blank = e.target.checked);
      $("#oRec", box).onchange = (e) => (rec = e.target.checked);
    } });
  if (!v) return;
  const ids = list.filter((s) => sel.has(s.id)).map((s) => s.id);
  if (!ids.length && !blank) return openPdf([], true);
  if (rec) { const nw = list.filter((s) => sel.has(s.id) && !tset.has(s.id)).map((s) => s.name); if (nw.length) await api("prints/" + code, { targets: nw }).catch(() => {}); }
  openPdf(ids, blank);
}

/* ───────────────────────── 1-2. 프린트 등록 (내가 만든 프린트·애쉬레인 앱에서 출력한 문제) */
async function viewRegister(sub, libCode) {
  const students = await api("students");
  const st = { sheet: null, answer: null, manifest: null };
  view.innerHTML = `
    <h1>프린트 등록</h1>
    <div class="card" id="libCard"><div class="row" style="justify-content:space-between"><h2 style="margin:0">보관함에서 코드로 등록</h2>
      <span class="sub small">Claude와 만든 프린트 원본이 모여 있는 곳 — 쓸 것만 코드로 등록하면 프린트함에 보이고 채점할 수 있어요</span></div>
      <form class="row" id="libForm" autocomplete="off" style="margin-top:10px"><input class="tin" id="libCode" placeholder="프린트 코드 (예: 7KQ-3MP)" maxlength="9" style="font-size:18px;font-weight:800;letter-spacing:2px;width:230px;text-transform:uppercase">
        <button class="btn">보관함에서 받아 등록</button><button type="button" class="btn ghost" id="libList">보관함 목록</button></form>
      <div id="libOut"></div></div>
    <h2 style="margin-top:22px">PDF를 올려 등록</h2>
    <p class="sub" style="margin-top:-6px">Claude와 만든 프린트, 애쉬레인 앱에서 출력한 문제처럼 <b>매쓰플랫이 아닌 PDF</b>를 올려 코드를 붙이고 채점·기록에 씁니다.</p>
    <div class="drop" id="rdrop"><b>시험지 PDF를 끌어다 놓으세요</b><span class="sub">정답지 PDF(빠른 정답지·해설지)나 등록 정보(.json)도 같이 놓으면 정답이 미리 채워져요</span>
      <input type="file" id="rfile" accept=".pdf,.json,application/pdf,application/json" multiple hidden></div>
    <div class="slots" id="slots"></div>
    <div class="row" style="margin-top:12px"><button class="btn big" id="ranalyze" disabled>문항 나누기</button><span class="sub small" id="rhint">시험지 PDF를 먼저 넣어 주세요</span></div>
    <div id="rout"></div>`;
  const isAns = (n) => /정답|답지|해설|answer|key/i.test(n);
  const drawSlots = () => {
    const slot = (k, t, sub) => `<div class="slot ${st[k] ? "" : "empty"}"><b>${t}</b><div class="fn">${st[k] ? "📄 " + esc(st[k].name) : esc(sub)}</div>
      ${st[k] ? `<button class="btn ghost small" data-clear="${k}" style="margin-top:6px">빼기</button>${k !== "manifest" ? ` <button class="btn ghost small" data-swap="1" style="margin-top:6px">⇄ 시험지·정답지 바꾸기</button>` : ""}` : ""}</div>`;
    $("#slots").innerHTML = slot("sheet", "시험지 (필수)", "아직 없음") + slot("answer", "정답지 (선택)", "빠른 정답지·해설지 — 정답 칸 미리 채우기") +
      slot("manifest", "등록 정보 (선택)", "Claude가 함께 준 .json — 없으면 PDF 안에서 찾아요");
    $$("[data-clear]").forEach((b) => (b.onclick = () => { st[b.dataset.clear] = null; drawSlots(); }));
    $$("[data-swap]").forEach((b) => (b.onclick = () => { [st.sheet, st.answer] = [st.answer, st.sheet]; drawSlots(); }));
    $("#ranalyze").disabled = !st.sheet;
    $("#rhint").textContent = st.sheet ? "문항 번호를 찾아 문항마다 잘라 볼게요. 다음 화면에서 고칠 수 있어요." : "시험지 PDF를 먼저 넣어 주세요";
  };
  const add = (files) => {
    for (const f of files) {
      if (/\.json$/i.test(f.name)) st.manifest = f;
      else if (/\.pdf$/i.test(f.name)) {
        if (isAns(f.name) && !st.answer) st.answer = f;
        else if (!st.sheet) st.sheet = f;
        else if (!st.answer) st.answer = f;
        else toast("시험지 하나, 정답지 하나씩 등록해요");
      } else toast(f.name + ": PDF나 .json만 넣을 수 있어요");
    }
    if (!st.sheet && st.answer) { st.sheet = st.answer; st.answer = null; }
    drawSlots();
  };
  const drop = $("#rdrop"), fin = $("#rfile");
  drop.onclick = () => fin.click();
  fin.onchange = () => { add(fin.files); fin.value = ""; };
  ["dragenter", "dragover"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => drop.addEventListener(ev, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => add(e.dataTransfer.files));
  drawSlots();

  // 보관함
  const libReg = async (code) => {
    const out = $("#rout");
    out.innerHTML = `<div class="card" style="margin-top:16px"><span class="busy"></span>보관함에서 <span class="code">${esc(fmtCode(code))}</span>를 받아 문항을 나누는 중…</div>`;
    out.scrollIntoView({ block: "start", behavior: "smooth" });
    try {
      const d = await api("library/register", { code });
      if (d.done) {    // 문항을 이미 나눠 둔 것이거나, 등록 정보로 바로 등록한 것
        out.innerHTML = `<h2 style="margin-top:18px">${d.auto ? "보관함에서 바로 등록했어요" : "보관함에서 꺼냈어요"}</h2>`
          + (d.auto ? `<p class="sub small">문항 ${d.n_items}개 · 정답 ${d.n_answers}개${d.n_sols ? ` · 해설 그림 ${d.n_sols}개` : ""}${(d.targets || []).length ? ` · 대상 ${d.targets.map(esc).join(", ")}` : ""} — 학생 이름은 지운 판으로 넣었어요.</p>` : "")
          + printCard(d.print);
        bindPrintCards(out);
        toast(fmtCode(code) + " 등록했어요");
        return;
      }
      regReview(d, students);
    }
    catch (e) {
      out.innerHTML = `<div class="card" style="border-color:#fca5a5;margin-top:16px"><b>보관함에서 등록하지 못했어요</b><div class="sub">${esc(e.message)}</div>
        ${/이미 등록/.test(e.message) ? `<a class="btn ghost small" href="#/tt/print/${code}" style="margin-top:8px">그 프린트 열기</a>` : ""}${/지운 프린트/.test(e.message) ? `<a class="btn ghost small" href="#/tt/prints" style="margin-top:8px">프린트함</a>` : ""}</div>`;
    }
  };
  const showLib = async () => {
    const out = $("#libOut");
    out.innerHTML = `<div style="margin-top:10px"><span class="busy"></span>보관함을 읽는 중…</div>`;
    let idx;
    try { idx = await api("library"); } catch (e) { out.innerHTML = `<div class="sub" style="margin-top:10px">${esc(e.message)}</div>`; return; }
    const list = idx.prints || [];
    if (!list.length) { out.innerHTML = `<div class="empty" style="margin-top:10px">보관함이 비어 있어요. 프린트 저장소(GitHub)에 올려 병합하면 몇 분 뒤 여기에 보여요.</div>`; return; }
    out.innerHTML = `<div class="row" style="margin-top:10px"><input class="tin" id="libQ" placeholder="제목·코드·학년·대상 학생으로 찾기" style="flex:1">
      <label class="small"><input type="checkbox" id="libHide" ${store.get("libHide", false) ? "checked" : ""}> 등록한 것 숨기기</label>
      <span class="sub small">${list.length}개${idx.updated ? " · " + esc(day(idx.updated)) + " 갱신" : ""}</span></div><div id="libRows"></div>`;
    const draw = () => {
      const q = $("#libQ").value.trim().toLowerCase(), hide = $("#libHide").checked;
      store.set("libHide", hide);
      const rows = list.filter((e) => (!hide || !e.registered) && (!q || [e.code, e.code_fmt, e.title, e.sub, e.grade, e.level, e.topic, (e.for || []).join(" ")].join(" ").toLowerCase().includes(q)));
      $("#libRows").innerHTML = rows.length ? `<table class="t" style="margin-top:8px"><tr><th>코드</th><th>제목</th><th>학년</th><th>만든 날</th><th>파일</th><th></th></tr>
        ${rows.slice(0, 300).map((e) => `<tr><td class="code">${esc(e.code_fmt)}</td><td><b>${esc(e.title)}</b>${e.sub ? `<div class="small muted">${esc(e.sub)}</div>` : ""}${(e.for || []).length ? `<div class="small muted">대상: ${e.for.map(esc).join(", ")}</div>` : ""}</td>
          <td class="small">${esc(e.grade || e.level || "")}</td><td class="sub small">${esc(e.made || "")}</td><td class="small">${(e.roles || []).map(esc).join(" · ")}</td>
          <td>${e.registered ? `<a class="btn small ghost" href="#/tt/print/${e.code}">등록됨</a>` : e.deleted ? `<span class="tag" title="프린트함 「지운 프린트」에서 되살리세요">지운 프린트</span>` : `<button class="btn small" data-lib="${e.code}">등록</button>`}</td></tr>`).join("")}</table>
        ${rows.length > 300 ? `<p class="sub small">처음 300개만 보여요 — 찾기를 쓰세요</p>` : ""}` : `<div class="empty" style="margin-top:8px">찾는 것이 없어요</div>`;
      $$("[data-lib]").forEach((b) => (b.onclick = () => libReg(b.dataset.lib)));
    };
    $("#libQ").oninput = draw; $("#libHide").onchange = draw; draw();
  };
  $("#libCode").addEventListener("input", (e) => { const c = normCode(e.target.value); e.target.value = c.length > 3 ? c.slice(0, 3) + "-" + c.slice(3, 6) : c; });
  $("#libForm").onsubmit = (e) => { e.preventDefault(); const c = normCode($("#libCode").value); if (c.length !== 6) return toast("코드 6글자를 넣어 주세요 (예: 7KQ-3MP)"); libReg(c); };
  $("#libList").onclick = showLib;
  if (sub === "lib") {
    const c = normCode(libCode);
    if (c.length === 6) { $("#libCode").value = fmtCode(c); libReg(c); } else showLib();
  }

  $("#ranalyze").onclick = async () => {
    const btn = $("#ranalyze"); btn.disabled = true;
    const out = $("#rout");
    out.innerHTML = `<div class="card"><span class="busy"></span>올리고 문항을 찾는 중…</div>`;
    try {
      const body = {};
      for (const k of ["sheet", "answer", "manifest"]) if (st[k]) { const u = await upload(st[k]); body[k] = { id: u.id, name: u.name }; }
      const d = await api("register/analyze", body);
      regReview(d, students);
    } catch (e) {
      out.innerHTML = `<div class="card" style="border-color:#fca5a5"><b>문항을 나누지 못했어요</b><div class="sub">${esc(e.message)}</div></div>`;
      btn.disabled = false;
    }
  };
}

function regReview(d, students) {
  const out = $("#rout");
  const base = d.base;
  const items = d.items.map((it) => ({ ...it, keep: true }));
  let mode = d.method === "pages" ? "pages" : "items";
  let label = d.label || "서답형";
  const msg = { manifest: `등록 정보로 문항 ${items.length}개를 읽었어요.`, auto: `문항 번호를 찾아 ${items.length}개로 나눴어요. 그림이 문항과 맞는지 훑어봐 주세요.`,
    pages: "문항 번호를 찾지 못했어요. 문항 수를 넣으면 그림 없이(쪽 단위로) 채점할 수 있어요." }[d.method];
  const guessed = items.filter((it) => it.answer_guess).length;
  out.innerHTML = `
    <div class="card" style="margin-top:16px"><div class="row" style="justify-content:space-between"><div><b>${esc(msg)}</b>
      ${guessed ? `<div class="sub small">정답지에서 정답 ${guessed}개를 읽어 노란 칸에 넣었어요. 맞는지 확인해 주세요.</div>` : ""}
      ${d.code ? `<div class="sub small">${d.library ? "보관함 코드" : "시험지에 찍힌 코드"} <b class="code">${esc(fmtCode(d.code))}</b>로 등록돼요.</div>` : ""}
      ${d.library ? `<div class="sub small">보관함 원본: ${(d.library.files || []).map((f) => esc(f.role || "기타")).join(" · ")}${d.library.made ? " · " + esc(d.library.made) + " 만듦" : ""}${(d.extras || []).length ? ` — 같이 받은 파일(${d.extras.map((x) => esc(x.name)).join(", ")})은 프린트 화면 「받기」에 붙어요` : ""}</div>` : ""}
      ${d.anon && d.anon.length ? `<div class="sub small" style="color:#15803d">학생 이름을 지운 이름 없는 판으로 저장해요: ${[...new Set(d.anon.map((x) => x.text))].map(esc).join(", ")} (${[...new Set(d.anon.map((x) => x.page))].join(", ")}쪽)</div>` : ""}
      <div class="sub small">${d.name_boxes && d.name_boxes.length ? "이름 칸을 찾았어요 — 출력할 때 그 자리에 학생 이름을 넣어요." : "이름 칸을 못 찾았어요 — 출력할 때 첫 쪽 왼쪽 위에 작게 넣어요."}</div></div>
      <button class="btn ghost small" id="rpages">시험지 쪽 보기</button></div>
      <div class="opt" style="margin-top:12px">
        <label class="k">제목</label><input class="tin" id="rtitle" value="${esc(d.title)}">
        <label class="k">부제</label><input class="tin" id="rsub" value="${esc(d.sub || "")}" placeholder="(선택)">
        <label class="k">주관식 표시</label><div id="rlabel"></div>
        <label class="k">학교급</label><div id="rlevel"></div>
        <label class="k">출제 대상</label><div id="rtargets"></div>
        <label class="k">나누기</label><div class="row"><div id="rmode"></div><span id="rcountBox" class="row"><input type="number" class="tin" id="rcount" min="1" max="200" style="min-width:0;width:90px" value="${items.length || 10}"><span class="sub small">문항</span></span></div>
      </div></div>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">문항 · 정답 <span class="sub small" id="rcnt"></span></h2>
      <details style="margin:0"><summary style="margin:0">정답 한꺼번에 붙여넣기</summary><textarea class="tin" id="rbulk" placeholder="1) ③ 2) 5 … 또는 순서대로 3 5 12 …" style="width:min(420px,80vw)"></textarea>
        <div><button class="btn small ghost" id="rfill">칸에 채우기</button></div></details></div>
      <div class="regitems" id="ritems" style="margin-top:10px"></div></div>
    <div class="row" style="justify-content:flex-end"><button class="btn big" id="rcommit">등록하고 코드 받기</button></div>`;
  seg($("#rlabel"), [["서답형", "서답형"], ["단답형", "단답형"]], label, (v) => (label = v));
  let level = (d.library && ["초등", "중등", "고등"].includes(d.library.level) && d.library.level) || store.get("regLevel", "중등");
  seg($("#rlevel"), [["초등", "초등"], ["중등", "중등"], ["고등", "고등"]], level, (v) => { level = v; store.set("regLevel", v); });
  const known = new Set(students.map((x) => x.name));
  const targets = nameChips($("#rtargets"), students, ((d.library && d.library.for) || []).filter((n) => known.has(n)));
  const modes = [["items", "문항별로 자르기"], ["pages", "쪽 단위 (그림 없이)"]];
  seg($("#rmode"), d.method === "pages" ? [modes[1]] : modes, mode, (v) => { mode = v; draw(); });
  $("#rpages").onclick = () => modal(`<h2>시험지</h2><div class="ansimgs">${d.pages.map((s) => `<img src="${fileUrl(base + "/" + s)}" alt="">`).join("")}</div>`);
  const pageItems = () => {
    const n = Math.max(1, Math.min(200, +$("#rcount").value || 1));
    return Array.from({ length: n }, (_, i) => items[i] && mode === "pages" ? items[i] : (items[i] || { seq: i + 1, label: String(i + 1), answer: "", choice: false, keep: true, png: null }));
  };
  const cur = () => (mode === "pages" ? pageItems() : items);
  function draw() {
    $("#rcountBox").style.display = mode === "pages" ? "" : "none";
    const list = cur();
    $("#rcnt").textContent = `${list.filter((it) => it.keep).length}문항 · 정답 ${list.filter((it) => it.keep && it.answer).length}`;
    $("#ritems").innerHTML = list.map((it, i) => `<div class="regitem ${it.keep ? "" : "off"}" data-i="${i}">
      ${mode === "items" ? (it.png ? `<img src="${fileUrl(base + "/" + it.png)}" alt="">` : `<div class="noimg">위치를 못 찾음</div>`) : ""}
      <div class="row"><input class="tin lab" value="${esc(it.label)}" title="번호(시험지에 적힌 대로)">
        <label class="small"><input type="checkbox" class="ch" ${it.choice ? "checked" : ""}> 객관식</label>
        ${mode === "items" ? `<button class="btn ghost small tg" style="margin-left:auto">${it.keep ? "빼기" : "넣기"}</button>` : ""}</div>
      <div class="row">${it.choice ? `<span class="cbtns">${[1, 2, 3, 4, 5].map((n) => `<button data-c="${n}" style="${it.answer === String(n) ? "background:var(--acc);color:#fff" : ""}">${CIRC[n]}</button>`).join("")}</span>` : ""}
        <input class="tin ans ${it.answer_guess ? "guess" : ""}" value="${esc(it.answer)}" placeholder="정답"></div></div>`).join("");
    $$("#ritems .regitem").forEach((el) => {
      const it = cur()[+el.dataset.i];
      if (mode === "pages" && !items[+el.dataset.i]) items[+el.dataset.i] = it;
      const img = $("img", el); if (img) img.onclick = () => zoom(img.src);
      $(".lab", el).oninput = (e) => (it.label = e.target.value.trim());
      $(".ans", el).oninput = (e) => { it.answer = e.target.value.trim(); it.answer_guess = false; e.target.classList.remove("guess"); };
      $(".ch", el).onchange = (e) => { it.choice = e.target.checked; draw(); };
      const tg = $(".tg", el); if (tg) tg.onclick = () => { it.keep = !it.keep; draw(); };
      $$("[data-c]", el).forEach((b) => (b.onclick = () => { it.answer = b.dataset.c; it.answer_guess = false; draw(); }));
    });
  }
  $("#rcount").oninput = draw;
  $("#rfill").onclick = () => {
    const list = cur().filter((it) => it.keep);
    const r = parseKeyText($("#rbulk").value, list.length);
    Object.entries(r).forEach(([k, v]) => { const it = list[+k - 1]; if (it) { it.answer = norm1(v); it.answer_guess = false; } });
    draw(); toast(`${Object.keys(r).length}칸 채웠어요`);
  };
  $("#rcommit").onclick = async () => {
    const btn = $("#rcommit"); btn.disabled = true;
    try {
      const list = cur();
      const p = await api("register/commit", { draft: d.draft, title: $("#rtitle").value, sub: $("#rsub").value, label, level, targets: targets.get(), mode,
        count: list.length, items: list.map((it, i) => ({ seq: mode === "pages" ? i + 1 : it.seq, label: it.label, answer: it.answer, choice: it.choice, keep: it.keep })) });
      out.innerHTML = `<h2 style="margin-top:18px">등록했어요</h2>${printCard(p)}<p class="sub small">위 「시험지 PDF」는 오른쪽 위에 코드를 찍은 인쇄용이에요. 이미 뽑아 둔 종이라면 코드를 손으로 적거나 프린트함에서 제목으로 찾으면 돼요.</p>`;
      bindPrintCards(out);
      toast(`코드 ${p.code_fmt} — 등록 완료`);
    } catch (e) { toast(e.message); btn.disabled = false; }
  };
  draw();
}
const norm1 = (v) => { const t = String(v).trim(); const k = Object.keys(CIRC).find((n) => CIRC[n] === t); return k || t; };

/* ───────────────────────── 2. 채점 */
async function viewGrade(code, sid, extra) {
  if (!code) return gradeHome();
  code = normCode(code);
  let p;
  try { p = await api("prints/" + code); } catch (e) {
    if (!/없어요/.test(e.message) || code.length !== 6) throw e;
    // 보관함에 있는 코드면 그 자리에서 바로 등록하고 채점으로 (등록 정보가 모자라면 확인 화면으로 보냄)
    view.innerHTML = `<div class="card"><span class="busy"></span>보관함에서 <span class="code">${esc(fmtCode(code))}</span>를 찾아 등록하는 중…</div>`;
    let lib = null, why = "";
    try { lib = await api("library/register", { code }); } catch (e2) { why = e2.message; }
    if (lib && lib.done) {
      toast(`${fmtCode(code)} 보관함에서 등록했어요${lib.auto ? ` (문항 ${lib.n_items}개)` : ""}`);
      p = await api("prints/" + code);
    } else if (lib) {
      location.hash = "#/tt/register/lib/" + code;     // 문항 확인이 필요한 보관함 프린트
      return;
    } else {
      const inLib = !/보관함에 .* 코드가 없어요/.test(why);
      view.innerHTML = `<div class="card"><h2><span class="code">${esc(fmtCode(code))}</span> — ${inLib ? "보관함에서 등록하지 못했어요" : "아직 등록하지 않은 코드예요"}</h2>
        <p class="sub">${inLib ? esc(why) : "보관함에도 없는 코드예요. 시험지에 적힌 코드를 다시 확인하거나, 프린트 등록에서 PDF를 올려 주세요."}</p>
        <div class="row"><a class="btn" href="#/tt/register/lib">보관함 보기</a><a class="btn ghost" href="#/tt/prints">프린트함에서 찾기</a><a class="btn ghost" href="#/tt/grade">돌아가기</a></div></div>`;
      return;
    }
  }
  const bw = bookWhere(p);
  if (bw) { location.replace(bw); return; }          // 교재는 채점 화면 대신 교재 탭에서(스캔본)
  if (!sid || sid === "pick") return gradePick(p, sid === "pick");
  return gradeRun(p, +sid, extra);
}

async function gradeHome() {
  const [unf, prints] = await Promise.all([api("gradings?status=unfinished"), api("prints")]);
  view.innerHTML = `<h1>채점</h1>
    <div class="card"><form class="row" id="gForm" autocomplete="off"><input class="tin" id="gCode" placeholder="프린트 코드 (예: 7KQ-3MP)" style="font-size:20px;font-weight:800;letter-spacing:2px;width:260px;text-transform:uppercase">
      <button class="btn big">채점 열기</button><span class="sub small">시험지 오른쪽 위·아래에 적힌 6글자</span></form></div>
    <div class="card"><h2>이어서 채점할 것</h2>${unf.length ? `<table class="t"><tr><th>학생</th><th>프린트</th><th>코드</th><th>상태</th><th>지금까지</th><th>마지막</th><th></th></tr>
      ${unf.map((g) => `<tr class="click" data-href="#/tt/grade/${g.code}/${g.student_id}"><td><b>${esc(g.name)}</b></td><td>${esc(g.title)}</td><td class="code">${esc(g.code_fmt)}</td>
        <td>${statusTag(g.status)}${g.n_rounds > 1 ? ` <span class="tag ses">${g.n_rounds}차</span>` : ""}</td><td>${sumText(g.summary)}</td><td class="sub small">${shortWhen(g.updated_at)}</td>
        <td><button class="btn ghost small warn-t" data-cancel="${g.id}" title="마지막으로 연 채점을 없던 일로 — 처음 연 채점이면 이 목록에서 빠져요">채점 취소</button></td></tr>`).join("")}</table>` : `<div class="empty">없어요. 다 끝냈어요 👏</div>`}</div>
    <div class="card"><h2>최근 만든 프린트</h2>${prints.length ? `<table class="t"><tr><th>코드</th><th>제목</th><th>대상</th><th>정답</th><th>만든 때</th></tr>
      ${prints.slice(0, 15).map((p) => `<tr class="click" data-href="#/tt/grade/${p.code}"><td class="code">${esc(p.code_fmt)}</td><td>${esc(p.title)}</td>
        <td>${p.targets.map((t) => esc(t.name)).join(", ") || "<span class='muted'>-</span>"}</td><td class="small">${p.n_answers}/${p.n_items}</td><td class="sub small">${shortWhen(p.created_at)}</td></tr>`).join("")}</table>` : `<div class="empty">아직 없어요. 변환 탭에서 만들어 주세요.</div>`}</div>`;
  $("#gCode").addEventListener("input", (e) => { const c = normCode(e.target.value); e.target.value = c.length > 3 ? c.slice(0, 3) + "-" + c.slice(3, 6) : c; });
  $("#gForm").onsubmit = (e) => { e.preventDefault(); const c = normCode($("#gCode").value); if (c.length !== 6) return toast("코드 6글자를 넣어 주세요"); location.hash = "#/tt/grade/" + c; };
  $("#gCode").focus();
  bindRows(view);
  $$("[data-cancel]", view).forEach((b) => (b.onclick = async (e) => {
    e.stopPropagation();
    if (await cancelGrading(Number(b.dataset.cancel), true)) gradeHome();
  }));
}
function bindRows(el) { $$("tr[data-href]", el).forEach((tr) => (tr.onclick = (e) => { if (!e.target.closest("a,button")) location.hash = tr.dataset.href; })); }

async function gradePick(p, manual) {
  const students = await api("students");
  const byStu = Object.fromEntries(p.gradings.map((g) => [g.student_id, g]).reverse());
  if (!manual && p.targets.length === 1 && !p.gradings.some((g) => g.student_id !== p.targets[0].id)) {
    location.replace("#/tt/grade/" + p.code + "/" + p.targets[0].id);
    return;
  }
  view.innerHTML = `<h1>누구 것을 채점할까요?</h1>
    <div class="card"><div class="result"><span class="codebig">${esc(p.code_fmt)}</span><div><b>${esc(p.title)}</b><div class="sub small">${p.n_items}문항 · 정답 ${p.n_answers}/${p.n_items} 입력됨</div></div></div></div>
    <div class="card"><h2>이 프린트를 받은 학생</h2><div class="chips" id="tg">${p.targets.length ? p.targets.map((t) => {
      const g = byStu[t.id];
      return `<a class="chip ${g ? "" : "pick"}" style="font-size:16px;padding:8px 14px;text-decoration:none" href="#/tt/grade/${p.code}/${t.id}">${esc(t.name)} ${g ? statusTag(g.status) : ""}</a>`;
    }).join("") : `<span class="empty">대상을 정하지 않은 프린트예요. 아래에서 학생을 골라 주세요.</span>`}</div></div>
    <div class="card"><h2>다른 학생</h2><div class="row"><input class="tin" id="newName" placeholder="이름 입력 후 Enter"><button class="btn" id="newGo">이 학생으로 채점</button></div>
      <div class="chips" style="margin-top:8px">${students.filter((s) => s.active && !p.targets.some((t) => t.id === s.id)).map((s) =>
        `<a class="chip pick" style="text-decoration:none" href="#/tt/grade/${p.code}/${s.id}">${esc(s.name)}</a>`).join("")}</div></div>`;
  const go = async () => {
    const n = $("#newName").value.trim();
    if (!n) return;
    const r = await api("students", { names: [n] });
    location.hash = "#/tt/grade/" + p.code + "/" + r.ids[0];
  };
  $("#newGo").onclick = go;
  $("#newName").onkeydown = (e) => { if (e.key === "Enter" && !e.isComposing) go(); };
}

async function gradeRun(p, sid, extra) {
  let mode = store.get("gradeMode", "ox");
  let d = await api("gradings", { code: p.code, student_id: sid });
  let focus = -1;
  const gid = d.grading.id;
  const cur = d.cur || { round: 1, kind: "solve", targets: null, no: 1 };
  const sessNo = cur.no || (d.sessions.length ? d.sessions[d.sessions.length - 1].no : 1);
  const retry = cur.kind === "retry";                  // 2차·3차: 틀리거나 안 푼 문항만 다시 매김
  let tset = new Set(retry ? cur.targets || [] : []);
  const syncT = () => { tset = new Set(retry ? (d.cur && d.cur.targets) || [] : []); };      // 앞 차를 고치면 이번 차 다시 풀 문항이 바뀔 수 있음
  const sameRound = d.sessions.filter((s) => (s.round || 1) === cur.round);
  const prevSess = sameRound.length > 1 ? sameRound[sameRound.length - 2] : null;     // 같은 차의 지난 회차(이어서 채점)
  const REASON = { done: "다 채점함", unsolved: "아이가 덜 풂", ungraded: "채점을 덜 함" };
  let showAll = false;
  // 앞 차 고치기 — 2차(다시 풀기)를 시작한 뒤에도 1차 … 결과를 바꾼다. edRound < cur.round 이면 그 차를 보여 주고 그 차에 매긴다.
  const fixAsk = /^fix(\d+)$/.exec(extra || "");
  let edRound = fixAsk && +fixAsk[1] >= 1 && +fixAsk[1] < cur.round ? +fixAsk[1] : cur.round;
  const past = () => edRound < cur.round;
  const edInfo = () => (d.rounds || []).find((x) => x.round === edRound) || null;
  const edSet = () => { const ri = edInfo(); return ri && ri.kind === "retry" && ri.targets ? new Set(ri.targets) : null; };   // null = 모든 문항(1차)

  const roundMark = (it, r = cur.round) => (it.rounds || []).find((x) => x.round === r);
  const resCur = (it) => (retry ? (roundMark(it) || {}).result || "" : (it.mark && it.mark.result) || "");      // 이번 차 결과
  const res = (it) => (past() ? (roundMark(it, edRound) || {}).result || "" : resCur(it));                 // 보고 있는 차 결과
  const isTarget = (it) => (past() ? !edSet() || edSet().has(it.seq) : !retry || tset.has(it.seq));
  // 다 끝난 채점을 다시 연 회차(고치기) — 지난 회차의 '안 풂'은 할 일로 치지 않는다
  const reopened = !!(prevSess && prevSess.end_reason === "done");
  // 할 일 = 아직 안 매긴 문항 + 지난 회차에 '안 풂'으로 남은 문항 (다시 풀기 차에서는 이번 차에 아직 안 매긴 다시 풀 문항) — 늘 이번 차 기준
  const isTodo = (it) => (retry ? tset.has(it.seq) && !resCur(it)
    : !it.mark || !it.mark.result || (!reopened && it.mark.result === "U" && it.mark.session_no < sessNo));
  // 앞 차들에 아직 안 매긴 문항(앞 차를 고쳐 새로 들어간 것) — [{round, none}]
  const pastLeft = () => (d.rounds || []).filter((r) => r.round < cur.round && r.summary && r.summary.none > 0);
  const roundLeft = (r) => (r === cur.round ? blanks() : ((d.rounds || []).find((x) => x.round === r)?.summary?.none || 0));
  const blanks = () => d.items.filter(isTodo).length;
  // 다 끝난 차를 다시 연 것(남은 문항 없음)이면 「N차 채점 수정」, 앞 차를 고쳐 남은 문항이 생겨 이어서 매기는 것이면 「N차 채점」
  const fixingLast = reopened && blanks() === 0;
  const marked = () => d.items.filter((it) => it.mark && it.mark.result && it.mark.session_no === sessNo).length;
  const visible = () => d.items.map((it, i) => i).filter((i) => isTarget(d.items[i]) || showAll);

  view.innerHTML = `
    <div class="stickybar"><div class="card" style="margin:0">
      <div class="row" style="justify-content:space-between">
        <div><b style="font-size:19px">${esc(d.student.name)}</b> <span class="sub">· ${esc(p.title)}</span> <span class="code sub">${esc(p.code_fmt)}</span>
          ${cur.round > 1 ? `<span class="tag ses">${cur.round}차</span>` : ""} <span id="stTag"></span></div>
        <div class="row"><div id="modeSeg"></div>
          ${p.sheet_pages && p.sheet_pages.length ? `<button class="btn ghost small" id="showSheet">시험지 보기</button>` : ""}
          ${p.answer_pages.length ? `<button class="btn ghost small" id="showAns">정답해설 보기</button>` : ""}
          <a class="btn ghost small" href="#/tt/print/${p.code}">정답 입력</a>
          <button class="btn ghost small" id="scanBtn" title="학생이 푼 종이 스캔본 올리기 · 1차·2차 표시">${scanLabel(d.scans)}</button>
          <a class="btn ghost small" href="#/tt/grade/${p.code}/pick">다른 학생</a>
          <button class="btn ghost small warn-t" id="cancelG" title="이번에 연 채점을 없던 일로 — 이어서 채점할 것에 남지 않아요">채점 취소</button>
          <button class="btn" id="finish">채점 끝내기</button></div>
      </div>
      ${retry ? `<div class="row rbtns" id="roundBtns"></div>` : ""}
      <div class="gsum" style="margin-top:8px" id="gsum"></div>
    </div></div>
    ${retry ? `<div class="card roundbar" id="roundbar"></div>` : ""}
    ${prevSess && prevSess.end_reason !== "done" ? `<div class="card" style="background:#eef2ff;border-color:#c7d2fe"><b>${cur.round > 1 ? cur.round + "차 " : ""}이어서 채점 (${sameRound.length}회차)</b> · 지난번(${shortWhen(prevSess.ended_at || prevSess.started_at)}): ${esc(REASON[prevSess.end_reason] || "닫지 않음")}.
      <span class="sub small">지난번에 매긴 기록은 그대로 남고, 이번에 매기는 것은 따로 저장돼요.</span></div>` : ""}
    ${!p.n_answers ? `<div class="card" style="background:#fffbeb;border-color:#fde68a">정답이 아직 없어요. O/X로 바로 매기거나, <a href="#/tt/print/${p.code}">정답 입력</a>에서 빠른정답을 넣으면 답 입력 자동 채점을 쓸 수 있어요.</div>` : ""}
    <div id="omr" hidden></div>
    <div class="items" id="items"></div>
    <p class="sub small" style="margin-top:14px">단축키: ↑↓ 문항 이동 · <b>O</b> 맞음 · <b>X</b> 틀림 · <b>U</b> 안 풂 (한글 입력 상태여도 됨) · 켜진 O/X 버튼을 한 번 더 누르면 이번에 매긴 것이 지워져요</p>`;

  seg($("#modeSeg"), [["ox", "O/X로 매기기"], ["input", "OMR 카드 → 자동 채점"]], mode, (v) => { mode = v; store.set("gradeMode", v); drawBar(); drawOmr(true); drawItems(); });

  // 2차부터: 맨 위 띠의 차 단추로 매길 차를 고른다 — 「1차 채점 수정」 … 「2차 채점」(이번 차)
  function drawRoundBtns() {
    const btns = $("#roundBtns");
    if (!btns) return;
    const rs = [];
    for (let r = 1; r <= cur.round; r++) rs.push(r);
    btns.innerHTML = rs.map((r) => {
      const n = roundLeft(r);
      const lab = r < cur.round ? `${r}차 채점 수정` : `${r}차 채점${fixingLast ? " 수정" : ""}`;
      return `<button type="button" class="btn small ${r === edRound ? "" : "ghost"}" data-rd="${r}" aria-pressed="${r === edRound}">${lab}${n ? ` <span class="left">남음 ${n}</span>` : ""}</button>`;
    }).join("");
    $$("[data-rd]", btns).forEach((b) => (b.onclick = () => setRound(+b.dataset.rd)));
  }
  function drawBar() {
    drawRoundBtns();
    const bar = $("#roundbar");
    if (!bar) return;
    const ri = edInfo();
    const nx = edRound + 1;
    const warn = pastLeft().filter((r) => r.round !== edRound);
    bar.classList.toggle("fixing", past());
    bar.innerHTML = `<div class="rbtext">${past()
      ? `<b>${edRound}차 채점 수정</b> — ${edRound}차에 매긴 결과를 O · X · 안 풂으로 바꿔요${ri && ri.kind === "retry" ? ` (${edRound}차에 다시 푼 ${(ri.targets || []).length}문항)` : ""}.
        <span class="sub small">바꾸면 ${nx}차가 따라 바뀌어요: 틀림 · 안 풂으로 바꾼 문항은 ${nx}차 다시 풀 문항에 들어가 아직 안 매긴 문항이 되고(${nx}차 미완성),
        맞음으로 바꾼 문항은 ${nx}차에서 빠져요.${mode === "input" ? " OMR 카드는 이번 차에서만 써요." : ""}</span>`
      : `<b>${cur.round}차 채점 · 다시 풀기</b> — 지난번에 틀리거나 안 푼 <b>${tset.size}문항</b>만 매겨요.
        여기서 매긴 결과가 최종이 되고, 앞 차 결과는 그대로 남아요. 앞 차를 고치려면 위 「${cur.round - 1}차 채점 수정」.`}
      ${warn.length ? `<div class="small" style="margin-top:4px;color:#b91c1c">${warn.map((r) => `${r.round}차에 아직 안 매긴 문항 ${r.summary.none}개`).join(" · ")} — 앞 차를 고쳐 새로 들어간 문항이에요. 위 「${warn[0].round}차 채점 수정」에서 매겨 주세요.</div>` : ""}
      ${!past() || (ri && ri.kind === "retry") ? `<label class="small" style="margin-left:6px;white-space:nowrap"><input type="checkbox" id="showAll"${showAll ? " checked" : ""}> 다른 문항도 보기</label>` : ""}</div>`;
    if ($("#showAll")) $("#showAll").onchange = (e) => { showAll = e.target.checked; e.target.blur(); drawItems(); setFocus(focus, false); };
  }
  function setRound(r) {
    if (r === edRound) return;
    edRound = r;
    drawBar();
    drawItems();
    const todo = d.items.findIndex(isTodo);
    setFocus(!past() && todo >= 0 ? todo : Math.max(0, d.items.findIndex(isTarget)));
  }

  function drawSum() {
    const s = d.summary;
    if (past()) {
      const tg = d.items.filter(isTarget);
      const c = (r) => tg.filter((it) => res(it) === r).length;
      const none = tg.filter((it) => !res(it)).length;
      $("#gsum").innerHTML = `<span class="sub small" style="font-weight:700">${edRound}차 고치는 중</span><span class="n o">O ${c("O")}</span><span class="n x">X ${c("X")}</span><span class="n u">안 풂 ${c("U")}</span>${none ? `<span class="n">안 매김 ${none}</span>` : ""}
        <span class="sub small">/ ${edRound}차 ${tg.length}문항 · 최종 O ${s.O} · X ${s.X}${s.U ? " · 안 풂 " + s.U : ""} (전체 ${s.total}문항) · ${cur.round}차 다시 풀 ${tset.size}문항</span>`;
    } else if (retry) {
      const tg = d.items.filter(isTarget);
      const c = (r) => tg.filter((it) => res(it) === r).length;
      const left = tg.filter((it) => !res(it)).length;
      $("#gsum").innerHTML = `<span class="sub small" style="font-weight:700">${cur.round}차</span><span class="n o">O ${c("O")}</span><span class="n x">X ${c("X")}</span><span class="n u">안 풂 ${c("U")}</span><span class="n">남음 ${left}</span>
        <span class="sub small">/ 다시 풀 ${tg.length}문항 · 최종 O ${s.O} · X ${s.X}${s.U ? " · 안 풂 " + s.U : ""} (전체 ${s.total}문항)</span>`;
    } else {
      $("#gsum").innerHTML = `<span class="n o">O ${s.O}</span><span class="n x">X ${s.X}</span><span class="n u">안 풂 ${s.U}</span><span class="n">남음 ${s.none}</span>
        <span class="sub small">/ ${s.total}문항 · ${s.O + s.X ? Math.round((100 * s.O) / (s.O + s.X)) + "% 정답 (푼 것 기준)" : ""}</span>
        ${d.items.some((it) => it.repeat) ? `<span class="tag rep">반복 오답 ${d.items.filter((it) => it.repeat).length}</span>` : ""}`;
    }
    $("#stTag").innerHTML = statusTag(d.grading.status);
  }
  const RK = { O: "O", X: "X", U: "안 풂" };
  function itemHtml(it, i, cont = false) {
    const r = res(it);
    const lastSess = it.mark && it.mark.session_no;
    const hist = (it.rounds || []).filter((x) => (past() ? x.round !== edRound : x.round < cur.round)).map((x) => `<span class="tag ${x.result === "O" ? "o" : x.result === "X" ? "x" : "u"}">${x.round}차 ${RK[x.result] || x.result}</span>`).join("");
    // 앞 차를 고칠 때: 다음 차 다시 풀 문항인데 그 차에 아직 안 매겼으면 「2차 남음」
    const nxt = past() ? (d.rounds || []).find((x) => x.round === edRound + 1) : null;
    const nextLeft = nxt && nxt.targets && nxt.targets.includes(it.seq) && !roundMark(it, nxt.round) ? `<span class="tag left">${nxt.round}차 남음</span>` : "";
    const badges = [
      it.choice ? `<span class="tag">객관식</span>` : `<span class="tag">${esc(p.label || "서답형")}</span>`,
      it.repeat ? `<span class="tag rep">반복 오답</span>` : it.wrong_before ? `<span class="tag prev">전에 ${it.wrong_before}번 틀림</span>` : "",
      hist, nextLeft,
      !retry && !reopened && prevSess && lastSess && lastSess < sessNo && r === "U" ? `<span class="tag u">지난번 안 풂</span>` : "",
      !retry && prevSess && lastSess === sessNo ? `<span class="tag ses">이번 회차</span>` : "",
    ].join("");
    const sl = splitLabel(it.label);
    const img = cont ? `<div class="pcont">${esc(sl.base)}번 문제의 하위 문제 ${esc(partLabel(sl.part))} — 문제 그림은 위에</div>`
      : it.png ? `<img loading="lazy" src="${fileUrl(p.code + "/" + it.png)}" alt="${esc(nob(it))}">` : `<div class="noimg">${esc(nob(it))} — 그림 없이 등록 (위 '시험지 보기')</div>`;
    const key = `<div class="key">${it.answer ? `정답 <b>${esc(CIRC[it.answer] && (it.choice || it.answer_png) ? CIRC[it.answer] : it.answer)}</b>` : it.answer_png ? (cont ? `<span class="muted">정답은 위 그림</span>` : "정답") : `<span class="muted">정답 미입력</span>`}
          ${it.answer_png && !cont ? `<img class="ansimg" src="${fileUrl(p.code + "/" + it.answer_png)}" alt="정답">` : ""}</div>`;
    const f = (it.mark && it.mark.result) || "";
    if (!isTarget(it)) {
      return `<div class="item off${cont ? " cont" : ""}" data-i="${i}"><div class="no ${/^\d+$/.test(nolab(it)) ? "" : "lab"}">${esc(nolab(it))}</div><div>${img}</div>
        <div class="side">${key}<div class="badges">${badges}</div><div class="small sub">${past() ? `${edRound}차에 다시 푼 문항이 아니에요` : "이번 차에 다시 풀 문항이 아니에요"} · 최종 <b>${RK[f] || "안 매김"}</b></div></div></div>`;
    }
    const rm = past() ? roundMark(it, edRound) : retry ? roundMark(it) : it.mark;
    const given = rm && rm.answer ? `<div class="small sub">적은 답: <b>${esc(rm.answer)}</b></div>` : "";
    const inputUi = "";              // 답 입력은 위 OMR 카드에서
    // 앞 차를 고칠 때: 최종 결과가 어느 차 것인지
    const fin = past() ? `<div class="small sub">최종 <b>${RK[f] || "안 매김"}</b>${it.mark && it.mark.round && it.mark.round !== edRound ? ` · ${it.mark.round}차 결과` : ""}</div>` : "";
    return `<div class="item ${r} ${i === focus ? "focus" : ""}${cont ? " cont" : ""}" data-i="${i}">
      <div class="no ${/^\d+$/.test(nolab(it)) ? "" : "lab"}">${esc(nolab(it))}</div>
      <div>${img}</div>
      <div class="side">${key}
        <div class="badges">${badges}</div>
        ${inputUi}${given}${fin}
        <div class="marks"><button class="mo ${r === "O" ? "on" : ""}" data-r="O">O</button><button class="mx ${r === "X" ? "on" : ""}" data-r="X">X</button><button class="mu ${r === "U" ? "on" : ""}" data-r="U">안 풂</button></div>
      </div></div>`;
  }
  function drawItems() {
    const vis = visible();
    // 하위 문제(「3 (2)」)는 바로 위가 같은 문제면 그림을 다시 싣지 않음
    const cont = (k) => { if (k <= 0) return false; const a = d.items[vis[k - 1]], b = d.items[vis[k]], sa = splitLabel(a.label), sb = splitLabel(b.label);
      return sb.part > 1 && sa.part > 0 && sa.base === sb.base && (a.png || null) === (b.png || null); };
    $("#items").innerHTML = vis.map((i, k) => itemHtml(d.items[i], i, cont(k))).join("") || `<div class="empty">매길 문항이 없어요</div>`;
    drawSum();
    drawRoundBtns();
    drawOmr();
    $$("#items .item").forEach((el) => {
      const i = +el.dataset.i, it = d.items[i];
      el.onclick = (e) => { if (!e.target.closest("button,input,img")) setFocus(i, false); };
      if ($("img", el)) $("img", el).onclick = (e) => zoom(e.target.src);
      $$(".marks button", el).forEach((b) => (b.onclick = () => mark(i, res(it) === b.dataset.r ? "" : b.dataset.r)));
      $$("[data-ans]", el).forEach((b) => (b.onclick = () => mark(i, "auto", b.dataset.ans)));
      const f = $("form.ansin", el);
      if (f) f.onsubmit = (e) => { e.preventDefault(); const v = $("input", f).value.trim(); if (v) mark(i, "auto", v); };
    });
  }
  function setFocus(i, scroll = true) {
    const vis = visible().filter((k) => isTarget(d.items[k]));
    if (!vis.length) return;
    focus = vis.includes(i) ? i : vis.reduce((a, k) => (Math.abs(k - i) < Math.abs(a - i) ? k : a), vis[0]);
    $$("#items .item").forEach((el) => el.classList.toggle("focus", +el.dataset.i === focus));
    const el = $(`#items .item[data-i="${focus}"]`);
    if (scroll && el) el.scrollIntoView({ block: "center", behavior: "smooth" });
    const inp = el && $("input", el);
    if (inp && mode === "input") inp.focus({ preventScroll: true });
  }
  function move(step) {
    const vis = visible().filter((k) => isTarget(d.items[k]));
    const at = vis.indexOf(focus);
    setFocus(vis[Math.max(0, Math.min(vis.length - 1, (at < 0 ? 0 : at) + step))]);
  }
  // 웹판: 누르면 화면에 바로 적고 다음 문항으로 — 서버에는 차례로 보낸다(다 보낸 뒤 서버 기록으로 맞춤)
  const queue = [];
  let flushing = null;
  // ── OMR 카드 (OMR 카드 → 자동 채점): 선생님이 아이가 적은 답을 칸에 넣고 「채점하기」.
  //    객관식은 ①~⑤를 칠하고 단답은 칸에 적는다. 단위만 다른 답은 맞다 · 틀리다 정하지 않고 묻는다(정답 인정 / 오답 처리).
  const omrKey = `omr:${gid}:${cur.round}`;
  const omr = store.get(omrKey, {}) || {};                 // seq → 적은 답 (이 기기에 잠깐 둠 — 새로고침해도 남게)
  const omrIdx = () => d.items.map((it, k) => k).filter((k) => isTarget(d.items[k]));
  const omrSave = () => store.set(omrKey, omr);
  const curMark = (it) => (retry ? roundMark(it) : it.mark);
  function omrRow(it, i) {
    const cm = curMark(it);
    const v = omr[it.seq] ?? (cm && cm.answer) ?? "";
    const r = res(it);
    return `<div class="orow ${r}" data-i="${i}" data-seq="${it.seq}"><span class="ono" title="${it.png ? "문제 보기" : ""}">${esc(nolab(it))}</span>
      ${it.choice ? `<span class="obubs" tabindex="0">${[1, 2, 3, 4, 5].map((n) => `<button type="button" class="obub${String(v) === String(n) ? " on" : ""}" data-n="${n}" tabindex="-1">${CIRC[n]}</button>`).join("")}</span>`
        : `<input class="oin" value="${esc(v)}" placeholder="답" autocomplete="off" spellcheck="false">`}
      <span class="ores">${r ? esc(RK[r]) : ""}</span></div>`;
  }
  function drawOmr(full = false) {
    const box = $("#omr");
    if (!box) return;
    if (mode !== "input" || past()) { box.hidden = true; box.innerHTML = ""; return; }      // 앞 차를 고칠 때는 O/X로
    box.hidden = false;
    if (!full && $(".omr-grid", box)) {          // 결과만 고침(입력 중인 칸은 그대로)
      $$(".orow", box).forEach((row) => { const it = d.items[+row.dataset.i]; const r = res(it); row.className = `orow ${r}`; $(".ores", row).textContent = r ? RK[r] : ""; });
      return;
    }
    const idx = omrIdx();
    box.innerHTML = `<div class="card omr"><div class="row" style="justify-content:space-between">
        <h2 style="margin:0">OMR 카드 <span class="sub small">아이가 적은 답을 넣고 「채점하기」 · 객관식은 번호를 누르고 단답은 칸에 적어요 (Enter = 다음 칸)</span></h2>
        <div class="row"><button class="btn ghost small" id="omrClear" title="이 카드에 넣은 답 지우기(매긴 결과는 그대로)">비우기</button><button class="btn" id="omrGo">채점하기</button></div></div>
      <div class="omr-grid">${idx.map((k) => omrRow(d.items[k], k)).join("") || `<div class="empty">매길 문항이 없어요</div>`}</div>
      <p class="sub small" id="omrNote" style="margin:8px 0 0">빈칸은 매기지 않아요. 단위만 다른 답(「12」 ↔ 「12 cm」)은 정답으로 인정할지 물어요.</p></div>`;
    const rows = $$(".orow", box);
    const next = (row) => { const k = rows.indexOf(row); const nx = rows[k + 1]; if (nx) ($(".oin", nx) || $(".obubs", nx)).focus(); };
    for (const row of rows) {
      const it = d.items[+row.dataset.i];
      const inp = $(".oin", row), bubs = $(".obubs", row);
      $(".ono", row).onclick = () => { if (it.png) zoom(fileUrl(p.code + "/" + it.png)); };
      if (inp) {
        inp.oninput = () => { omr[it.seq] = inp.value; omrSave(); };
        inp.onkeydown = (e) => { if (e.key === "Enter" && !e.isComposing) { e.preventDefault(); next(row); } };
      }
      if (bubs) {
        const pickN = (n) => { omr[it.seq] = String(omr[it.seq] ?? "") === String(n) ? "" : String(n); omrSave(); $$(".obub", bubs).forEach((b) => b.classList.toggle("on", b.dataset.n === omr[it.seq])); };
        $$(".obub", bubs).forEach((b) => (b.onclick = () => { pickN(b.dataset.n); if (omr[it.seq]) next(row); }));
        bubs.onkeydown = (e) => {
          if (/^[1-5]$/.test(e.key)) { e.preventDefault(); e.stopPropagation(); pickN(e.key); next(row); }
          else if (e.key === "Enter" || e.key === "ArrowDown") { e.preventDefault(); e.stopPropagation(); next(row); }
          else if (e.key === "Backspace" || e.key === "Delete") { e.preventDefault(); e.stopPropagation(); omr[it.seq] = ""; omrSave(); $$(".obub", bubs).forEach((b) => b.classList.remove("on")); }
          else if (e.key === "ArrowUp") { e.preventDefault(); e.stopPropagation(); const pv = rows[rows.indexOf(row) - 1]; if (pv) ($(".oin", pv) || $(".obubs", pv)).focus(); }
          else if (e.key !== "Tab") e.stopPropagation();          // O · X · U 단축키가 아래 문항 카드로 가지 않게
        };
      }
    }
    $("#omrGo").onclick = () => omrGrade();
    $("#omrClear").onclick = () => { for (const k of Object.keys(omr)) delete omr[k]; omrSave(); drawOmr(true); };
  }
  // 단위만 다른 답: 문항마다 「정답 인정 / 오답 처리」 — 다 고르면 매김
  function unitAsk(list) {
    const pick = new Map();
    return modal(`<h2>단위가 달라요 — 정답으로 인정할까요?</h2>
      <p class="sub small" style="margin-top:0">숫자는 맞는데 단위가 빠졌거나 다르게 적은 답이에요. 문항마다 골라 주세요.</p>
      <div class="ulist">${list.map((u, k) => `<div class="urow"><b>${esc(nob(u.it))}</b><span>정답 <b>${esc(u.it.answer)}</b> · 적은 답 <b>${esc(u.v)}</b><br><span class="sub small">${esc(u.why || "")}</span></span><span data-useg="${k}"></span></div>`).join("")}</div>
      <div class="row" style="margin-top:10px"><button class="btn ghost small" id="uAllO">모두 정답 인정</button><button class="btn ghost small" id="uAllX">모두 오답 처리</button></div>`,
      [{ label: "그만두기", value: null, cls: "ghost" }, { label: "고른 대로 매기기", value: 1 }],
      { cls: "umodal", onOpen: (box, done) => {
        const segAll = () => list.forEach((u, k) => seg($(`[data-useg="${k}"]`, box), [["O", "정답 인정"], ["X", "오답 처리"]], pick.get(k) || "", (v) => pick.set(k, v)));
        segAll();
        $("#uAllO", box).onclick = () => { list.forEach((u, k) => pick.set(k, "O")); segAll(); };
        $("#uAllX", box).onclick = () => { list.forEach((u, k) => pick.set(k, "X")); segAll(); };
        $('.modal-actions button[data-i="1"]', box).onclick = () => { if (pick.size < list.length) return toast(`${list.length - pick.size}문항을 더 골라 주세요`); done(1); };
      } }).then((v) => (v ? pick : null));
  }
  async function omrGrade() {
    const todo = [], unk = [], nokey = [];
    for (const k of omrIdx()) {
      const it = d.items[k];
      const v = String(omr[it.seq] ?? "").trim();
      if (!v) continue;
      const cm = curMark(it);
      if (cm && cm.result && cm.round === cur.round && String(cm.answer || "") === v) continue;     // 이미 같은 답으로 매김
      const j = judge(it.answer, v);
      if (!j.result) { nokey.push(it); continue; }
      if (j.result === "?") unk.push({ k, it, v, why: j.why });
      else todo.push({ i: k, result: j.result, answer: v });
    }
    if (unk.length) {
      const pick = await unitAsk(unk);
      if (!pick) return toast("매기지 않았어요");
      unk.forEach((u, n) => todo.push({ i: u.k, result: pick.get(n), answer: u.v }));
    }
    if (todo.length) markMany(todo);
    const msg = (todo.length ? `${todo.length}문항을 매겼어요 (O ${todo.filter((x) => x.result === "O").length} · X ${todo.filter((x) => x.result === "X").length})` : "새로 매길 답이 없어요")
      + (nokey.length ? ` · 정답이 없어 못 매긴 ${nokey.length}문항(${nokey.slice(0, 6).map((x) => nolab(x)).join(", ")}${nokey.length > 6 ? " …" : ""}) — 아래에서 O/X로 매겨 주세요` : "");
    if ($("#omrNote")) $("#omrNote").textContent = msg;
    toast(msg, 4000);
  }
  function markMany(list) {
    for (const { i, result, answer } of list) {
      const it = d.items[i];
      it.mark = { ...(it.mark || {}), seq: it.seq, result, answer, session_no: sessNo, round: cur.round };
      it.rounds = (it.rounds || []).filter((x) => x.round !== cur.round).concat([{ round: cur.round, result, answer }]).sort((a, b) => a.round - b.round);
      queue.push({ seq: it.seq, result, answer, mode });
    }
    sumLocal();
    drawItems();
    flushMarks();
  }

  function sumLocal() {
    const s = { O: 0, X: 0, U: 0, none: 0, total: d.items.length };
    for (const it of d.items) { const r = (it.mark && it.mark.result) || ""; s[["O", "X", "U"].includes(r) ? r : "none"]++; }
    d.summary = s;
  }
  let sentMode = null;
  const follow = { added: [], removed: [] };      // 앞 차를 고쳐 다음 차에 들어가거나 빠진 문항(다 보낸 뒤 알림) — [{seq, round(s)}]
  function flushMarks() {
    if (flushing) return flushing;
    flushing = (async () => {
      try {
        for (;;) {
          while (queue.length) {
            const job = { ...queue[0], light: true };
            if (job.mode === sentMode) delete job.mode;
            try {
              if (job.fix) {           // 앞 차 고치기 — 다음 차가 따라 바뀜
                const r = await api(`gradings/${gid}/fix`, { round: job.fix, seq: job.seq, result: job.result, light: true });
                if (r && r.added_round) follow.added.push({ seq: job.seq, round: r.added_round });
                if (r && r.removed_rounds && r.removed_rounds.length) follow.removed.push({ seq: job.seq, rounds: r.removed_rounds });
              } else await api(`gradings/${gid}/mark`, job);
            } catch (e) {
              queue.length = 0;
              toast(e.message, 4000);
              try { d = await api("gradings/" + gid); syncT(); } catch { /* 다음에 */ }
              drawBar(); drawItems(); setFocus(focus, false);
              return;
            }
            if (job.mode) sentMode = job.mode;
            queue.shift();
          }
          const r = await api("gradings/" + gid);
          if (!queue.length) {
            d = r; syncT(); drawBar(); drawItems(); setFocus(focus, false);
            const lab = (s) => nob(d.items.find((x) => x.seq === s) || { seq: s });
            const msg = [];
            // 같은 문항을 여러 번 바꿨으면 마지막 것만
            const lastOf = (arr) => [...new Map(arr.map((x) => [x.seq, x])).values()];
            const add = lastOf(follow.added.splice(0)), rem = lastOf(follow.removed.splice(0));
            for (const [rd, xs] of groupBy(add, (x) => x.round)) msg.push(`${rd}차 다시 풀 문항에 넣었어요 — ${xs.map((x) => lab(x.seq)).join(", ")} (${rd}차 남음)`);
            for (const [rds, xs] of groupBy(rem, (x) => x.rounds.join("·"))) msg.push(`${rds}차에서 뺐어요 — ${xs.map((x) => lab(x.seq)).join(", ")}`);
            if (msg.length) toast(msg.join(" · "), 5000);
            break;
          }
        }
      } catch (e) { toast(e.message, 4000); } finally { flushing = null; }
    })();
    return flushing;
  }
  // 앞 차 고치기: 화면에 먼저 적고 차례로 보낸다(다 보낸 뒤 서버 기록으로 맞춤 — 이번 차 다시 풀 문항도)
  function fixMark(i, result) {
    const it = d.items[i];
    if (!["O", "X", "U"].includes(result)) return toast(`${edRound}차 결과는 지우지 않아요 — O · X · 안 풂 중에서 골라 바꿔 주세요`);
    if (!isTarget(it)) return;
    const vis = visible().filter((k) => isTarget(d.items[k]));
    const goNext = () => { const at = vis.indexOf(i); setFocus(at >= 0 && at + 1 < vis.length ? vis[at + 1] : i); };
    const pm = roundMark(it, edRound);
    if (pm && pm.result === result) return goNext();
    const ans = (pm && pm.answer) || "";
    it.rounds = (it.rounds || []).filter((x) => x.round !== edRound).concat([{ round: edRound, result, answer: ans }]).sort((a, b) => a.round - b.round);
    const top = it.rounds[it.rounds.length - 1];          // 최종 = 기록이 있는 가장 늦은 차의 결과
    if (top.round === edRound) it.mark = { ...(it.mark || {}), seq: it.seq, result, answer: ans, round: edRound, session_no: null };
    sumLocal();
    drawItems();
    goNext();
    queue.push({ fix: edRound, seq: it.seq, result });
    flushMarks();
  }
  async function mark(i, result, answer) {
    if (past()) return fixMark(i, result);
    const it = d.items[i];
    const rm = retry ? roundMark(it) : it.mark;
    const ans = answer ?? (rm ? rm.answer : "");
    if (result === "auto") {
      result = autoJudge(it.answer, answer);
      if (!result) { toast("정답이 없어서 자동으로 못 매겼어요. O/X를 눌러 주세요."); setFocus(i, false); return; }
    }
    if (result === "") {           // 이번에 매긴 것 지우기 — 그 전 기록은 서버가 알려 준다
      queue.push({ seq: it.seq, result: "", answer: ans, mode });
      await flushMarks();
      return;
    }
    it.mark = { ...(it.mark || {}), seq: it.seq, result, answer: ans, session_no: sessNo, round: cur.round };
    it.rounds = (it.rounds || []).filter((x) => x.round !== cur.round).concat([{ round: cur.round, result, answer: ans }]).sort((a, b) => a.round - b.round);
    sumLocal();
    drawItems();
    const next = d.items.findIndex((x, k) => k > i && isTodo(x));
    setFocus(next >= 0 ? next : Math.min(i + 1, d.items.length - 1));
    queue.push({ seq: it.seq, result, answer: ans, mode });
    flushMarks();
  }
  document.onkeydown = (e) => {
    if (!$("#tt-modal").hidden || e.target.closest("input:not([type=checkbox]),textarea") || e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.code;
    if (k === "ArrowDown" || k === "KeyJ") { e.preventDefault(); move(1); }
    else if (k === "ArrowUp" || k === "KeyK") { e.preventDefault(); move(-1); }
    else if (focus >= 0 && ["KeyO", "KeyX", "KeyU"].includes(k)) { e.preventDefault(); mark(focus, k.slice(3)); }
  };

  // 아직 안 매긴 문항(모든 차) 한 줄 — 「2차 1문항 · 3차 2문항」
  const leftText = () => (d.rounds || []).map((r) => [r.round, r.round === cur.round ? blanks() : (r.summary && r.summary.none) || 0])
    .filter(([, n]) => n > 0).map(([r, n]) => `${r}차 ${n}문항`).join(" · ");
  // 닫을 때: 다 매겼으면 완료, 덜 매겼으면 이유를 묻는다. 돌려주는 것: false(그대로 있음) · true · "deleted"(처음 연 채점을 열어 보기만 함)
  async function askClose() {
    await flushMarks();
    const b = blanks();
    if (d.grading.status !== "open") return true;
    if (marked() === 0) {     // 열어 보기만 했으면(앞 차만 고쳤어도) 원래 상태로 되돌려 닫음 — 빈 회차는 서버가 없앰
      const r = await api(`gradings/${gid}/close`, { reason: b === 0 ? "done" : (prevSess && prevSess.end_reason) || "ungraded", untouched: true });
      if (r && r.status === "deleted") { toast("열어 보기만 해서 채점 기록을 남기지 않았어요"); return "deleted"; }
      if (r && r.status === "paused_ungraded" && leftText()) toast(`아직 안 매긴 문항(${leftText()})이 있어 '채점 덜 함'(미완성)으로 두었어요`, 5000);
      return true;
    }
    if (b === 0) {
      const pl = pastLeft();
      if (pl.length) {        // 앞 차를 고쳐 앞 차에 새로 들어간 문항이 아직 안 매겨짐
        const v = await modal(`<h2>${pl.map((r) => `${r.round}차에 아직 안 매긴 문항이 ${r.summary.none}개`).join(" · ")} 있어요</h2>
          <p>앞 차를 고쳐 새로 들어간 문항이에요. 지금 매기거나, 나중에 「${pl[0].round}차 채점 수정」에서 매겨도 돼요. 다 매기기 전까지는 '채점 덜 함'(미완성)으로 남아요.</p>`,
          [{ label: "그대로 있기", value: null, cls: "ghost" }, { label: `「${pl[0].round}차 채점 수정」으로`, value: "go", cls: "ghost" }, { label: "나중에 매길게요", value: "later" }]);
        if (v === "go") { setRound(pl[0].round); return false; }
        if (!v) return false;
      }
      const r = await api(`gradings/${gid}/close`, { reason: "done" });
      if (r && r.status !== "done") toast(`아직 안 매긴 문항(${leftText()})이 있어 '채점 덜 함'(미완성)으로 두었어요`, 5000);
      else toast(retry ? `${d.student.name} · ${cur.round}차 채점 완료 (최종 O ${d.summary.O} / X ${d.summary.X})` : `${d.student.name} · 채점 완료 (O ${d.summary.O} / X ${d.summary.X})`);
      return true;
    }
    const v = retry
      ? await modal(`<h2>${cur.round}차에서 아직 안 매긴 문항이 ${b}개 있어요</h2>
        <p>고른 대로 기록해 두고, 다음에 이 코드로 다시 열면 <b>${cur.round}차를 이어서</b> 매길 수 있어요.</p>
        <ul class="sub small"><li><b>아이가 덜 풀었어요</b> → 남은 ${b}문항은 ${cur.round - 1}차 결과 그대로 두고 멈춰요.</li>
        <li><b>제가 채점을 덜 했어요</b> → 남은 문항은 비워 둔 채로 멈춰요.</li></ul>`,
        [{ label: "계속 채점하기", value: null, cls: "ghost" }, { label: "제가 채점을 덜 했어요", value: "ungraded", cls: "ghost" }, { label: "아이가 덜 풀었어요", value: "unsolved", cls: "warn" }])
      : await modal(`<h2>아직 안 매긴 문항이 ${b}개 있어요</h2>${prevSess ? `<p class="small sub">지난번 '안 풂'으로 남았는데 이번에 아직 안 매긴 문항도 포함이에요.</p>` : ""}
        <p>어떤 상황인가요? 고른 대로 기록해 두고, 다음에 이 코드로 다시 열면 <b>이어서</b> 채점할 수 있어요.</p>
        <ul class="sub small"><li><b>아이가 덜 풀었어요</b> → 남은 ${b}문항을 '안 풂'으로 남겨요. 나중에 풀어 오면 다음 회차로 이어서 매기고, 언제 무엇을 풀었는지 기록이 남아요.</li>
        <li><b>제가 채점을 덜 했어요</b> → 남은 문항은 비워 둔 채로 멈춰요.</li></ul>`,
        [{ label: "계속 채점하기", value: null, cls: "ghost" }, { label: "제가 채점을 덜 했어요", value: "ungraded", cls: "ghost" }, { label: "아이가 덜 풀었어요", value: "unsolved", cls: "warn" }]);
    if (!v) return false;
    await api(`gradings/${gid}/close`, { reason: v });
    toast(v === "unsolved" ? (retry ? `멈춰 두었어요. 다음에 ${cur.round}차를 이어서 매기세요.` : `안 푼 ${b}문항을 기록했어요. 다음에 이어서 채점하세요.`) : "멈춰 두었어요. 이어서 채점할 수 있어요.");
    return true;
  }
  leaveGuard = askClose;
  leaveGuard.dirty = () => queue.length > 0 || (d.grading.status === "open" && marked() > 0 && blanks() > 0);
  // 시록고의 다른 탭으로 나갈 때: 보내지 못한 것을 보내고, 열어 보기만 했으면 빈 회차를 닫는다(덜 매긴 채점은 열린 채로 — 다시 열면 이어서)
  leaveGuard.silent = async () => {
    await flushMarks();
    if (d.grading.status === "open" && marked() === 0) await api(`gradings/${gid}/close`, { reason: blanks() === 0 ? "done" : (prevSess && prevSess.end_reason) || "ungraded", untouched: true });
  };
  $("#finish").onclick = async () => {
    const guard = leaveGuard;
    leaveGuard = null;
    let ok = false;
    try { ok = await askClose(); } finally { if (!ok) leaveGuard = guard; }
    if (ok === "deleted") location.hash = "#/tt/grade";
    else if (ok) location.hash = "#/tt/grade/" + p.code + "/" + sid + "/done";
  };
  // 채점 취소: 이번에 연 회차와 그 뒤 매긴 것을 되돌려 연 전 상태로(처음 연 채점이면 기록째 없앰) — 이어서 채점할 것에 남지 않음
  $("#cancelG").onclick = async () => {
    const guard = leaveGuard;
    leaveGuard = null;
    queue.length = 0;           // 보내지 못한 것은 버림(어차피 되돌림)
    if (flushing) { try { await flushing; } catch { /* */ } }
    const r = await cancelGrading(gid);
    if (!r) { leaveGuard = guard; return; }
    location.hash = r.result === "deleted" ? "#/tt/grade" : "#/tt/grade/" + p.code + "/" + sid + "/done";
  };
  if ($("#showAns")) $("#showAns").onclick = () => modal(`<h2>정답해설</h2><div class="ansimgs">${p.answer_pages.map((s) => `<img src="${fileUrl(s)}" alt="">`).join("")}</div>`);
  $("#scanBtn").onclick = () => scanModal(gid, `${esc(d.student.name)} · 스캔본`, {
    rounds: Math.max(cur.round || 1, ...d.sessions.map((s) => s.round || 1)), scans: d.scans || [], meta: { title: p.title, student: d.student.name },
    onChange: (sc) => { d.scans = sc; if ($("#scanBtn")) $("#scanBtn").textContent = scanLabel(sc); } });
  if ($("#showSheet")) $("#showSheet").onclick = () => modal(`<h2>시험지</h2><div class="ansimgs">${p.sheet_pages.map((s) => `<img src="${fileUrl(s)}" alt="">`).join("")}</div>`);
  drawBar();
  drawItems();
  const firstBlank = d.items.findIndex(isTodo);
  if (past()) setFocus(Math.max(0, d.items.findIndex(isTarget)), false);
  else setFocus(firstBlank >= 0 ? firstBlank : 0, firstBlank > 0);
}

/* 채점 취소: 이번에 연 채점을 없던 일로(처음 연 채점이면 기록째 없앰). 되돌릴 기록이 있을 때만 묻는다. 돌려주는 것: 서버 결과 | null */
async function cancelGrading(gid, fromList = false) {
  let info;
  try { info = await api(`gradings/${gid}/cancel`); } catch (e) { toast(e.message, 4500); return null; }
  const nm = info.marks || 0, ns = info.scans || 0;
  const back = (STATUS[{ done: "done", unsolved: "paused_unsolved" }[info.back] || "paused_ungraded"] || [""])[0];
  if (info.result === "deleted" ? nm + ns > 0 : nm > 0) {
    const v = await modal(info.result === "deleted"
      ? `<h2>채점을 취소할까요?</h2><p>이 채점 기록이 없어져요 — ${[nm ? `매긴 기록 <b>${nm}개</b>` : "", ns ? `올린 스캔본 <b>${ns}개</b>` : ""].filter(Boolean).join(" · ")}도 함께 지워져요.</p>
        <p class="sub small">「이어서 채점할 것」에서도 빠져요.</p>`
      : `<h2>채점을 취소할까요?</h2><p>${fromList ? `마지막으로 연 ${info.round || ""}차 회차에서` : "이번에 연 뒤"} 매긴 기록 <b>${nm}개</b>(앞 차를 고친 것 포함)를 되돌리고, 열기 전 상태(<b>${esc(back)}</b>)로 돌아가요.</p>
        <p class="sub small">올린 스캔본은 그대로 둬요.</p>`,
      [{ label: "그만두기", value: null, cls: "ghost" }, { label: "채점 취소", value: 1, cls: "warn" }]);
    if (!v) return null;
  }
  try {
    const r = await api(`gradings/${gid}/cancel`, {});
    toast(r.result === "deleted" ? "채점을 취소했어요 — 채점 기록을 없앴어요" : `채점을 취소했어요 — ${(STATUS[r.status] || [r.status])[0]}(으)로 돌아갔어요`);
    return r;
  } catch (e) { toast(e.message, 4500); return null; }
}

/* 다음 차(2차·3차) 채점 시작: 틀리거나 안 푼 문항만 다시 매김 */
async function startRetry(code, sid, d) {
  const R = d.rounds || [];
  const nextR = (R.length ? R[R.length - 1].round : 1) + 1;
  const cand = d.items.filter((it) => d.retry_candidates.includes(it.seq));
  const v = await modal(`<h2>${nextR}차 채점을 시작할까요?</h2>
    <p>틀리거나 안 푼 <b>${cand.length}문항</b>만 다시 매겨요: <span class="small">${cand.map((it) => esc(nob(it))).join(", ")}</span></p>
    <p class="sub small">${nextR - 1}차까지의 결과는 그대로 남고, ${nextR}차에 매긴 결과가 최종이 돼요. 아이에게 이 문항만 모은 종이를 주려면 「오답만 출제」를 쓰세요.</p>`,
    [{ label: "그만두기", value: null, cls: "ghost" }, { label: `${nextR}차 채점 시작`, value: 1 }]);
  if (!v) return;
  try { await api("gradings", { code, student_id: sid, purpose: "retry" }); } catch (e) { return toast(e.message); }
  location.hash = "#/tt/grade/" + code + "/" + sid;
}

// 채점한 날(매긴 날) — 프린트 차마다 「1차 11/20 · 2차 11/25~26」
const dayRange = (a, b) => (!a ? "" : !b || b === a ? md(a) : `${md(a)}~${a.slice(0, 7) === b.slice(0, 7) ? String(+b.slice(8, 10)) : md(b)}`);
const gdLine = (gd) => ((gd || []).length ? `<div class="sub small nowrap" title="채점한 날(매긴 날)">채점 ${gd.map((x) => `${(gd.length > 1 ? x.round + "차 " : "")}${dayRange(x.first, x.last)}`).join(" · ")}</div>` : "");
const roundsLine = (it) => (it.rounds || []).map((x) => `${x.round}차 ${{ O: "O", X: "X", U: "안 풂" }[x.result] || x.result}`).join(" → ");

/* 채점 끝난 뒤 요약 (#/tt/grade/코드/학생/done) */
const _viewGrade = viewGrade;
viewGrade = async function (code, sid, extra) {
  if (extra !== "done") return _viewGrade(code, sid, extra);
  const gs = await api("gradings?student=" + sid);
  const g = gs.find((x) => x.code === normCode(code));
  if (!g) return _viewGrade(code);          // 채점 기록이 없으면(취소했으면) 새로 열지 않고 학생 고르기로
  if (g.book) { location.replace("#/tt/books/" + g.book); return; }
  const d = await api("gradings/" + g.id);
  const R = d.rounds || [];
  const last = R[R.length - 1] || { round: 1, kind: "solve" };
  const wrong = d.items.filter((it) => it.mark && it.mark.result === "X");
  const uns = d.items.filter((it) => it.mark && it.mark.result === "U");
  const fixed = d.items.filter((it) => it.mark && it.mark.result === "O" && (it.rounds || []).some((x) => x.result !== "O"));
  const nextN = d.retry_candidates.length;
  const done = d.grading.status === "done";
  const sm = (s) => `<td>${s.O}</td><td>${s.X}</td><td>${s.U}</td><td>${s.none}</td>`;
  view.innerHTML = `<h1>${esc(d.student.name)} · ${esc(d.print.title)} <span class="code sub">${esc(d.print.code_fmt)}</span></h1>
    <div class="card"><div class="gsum"><span class="n o">O ${d.summary.O}</span><span class="n x">X ${d.summary.X}</span><span class="n u">안 풂 ${d.summary.U}</span>${d.summary.none ? `<span class="n">남음 ${d.summary.none}</span>` : ""} ${statusTag(d.grading.status)}
      ${R.length > 1 ? `<span class="tag ses">${last.round}차까지</span>` : ""}</div>
      ${R.length === 1 && R[0].graded_first ? `<div class="sub small" style="margin-top:6px">채점한 날 ${dayRange(R[0].graded_first, R[0].graded_last)}</div>` : ""}
      ${R.length > 1 ? `<table class="t" style="margin-top:10px;max-width:640px"><tr><th>차</th><th>무엇을</th><th>문항</th><th>O</th><th>X</th><th>안 풂</th><th>남음</th><th>채점한 날</th></tr>
        ${R.map((r) => `<tr><td><b>${r.round}차</b></td><td class="small">${r.kind === "retry" ? "다시 풀기" : "처음 풀기"}</td><td>${r.summary.total}</td>${sm(r.summary)}<td class="sub small">${r.graded_first ? dayRange(r.graded_first, r.graded_last) : "-"}</td></tr>`).join("")}
        <tr style="font-weight:800"><td>최종</td><td></td><td>${d.summary.total}</td>${sm(d.summary)}<td></td></tr></table>` : ""}
      <div class="row" style="margin-top:12px">
        ${!done ? `<a class="btn" href="#/tt/grade/${d.print.code}/${sid}">${last.round > 1 ? last.round + "차 " : ""}이어서 채점</a>` : ""}
        ${done && nextN ? `<button class="btn" id="retryGo" title="틀리거나 안 푼 문항만 다시 풀게 한 뒤 매겨요">${last.round + 1}차 채점 시작 — 틀린·안 푼 ${nextN}문항</button>` : ""}
        ${(R.length ? R : [last]).filter((r) => done || r.round < last.round).map((r) => `<a class="btn ghost" data-fixr="${r.round}" href="#/tt/grade/${d.print.code}/${sid}${r.round < last.round ? "/fix" + r.round : ""}"
          title="${r.round}차에 매긴 결과를 바꿔요${r.round < last.round ? ` — 바꾸면 ${r.round + 1}차가 따라 바뀌어요` : ""}">${r.round}차 채점 수정${r.summary && r.summary.none && r.round < last.round ? ` · 남음 ${r.summary.none}` : ""}</a>`).join("")}
        <a class="btn ghost" href="#/tt/students/${sid}">학생 기록</a><a class="btn ghost" href="#/tt/grade">다른 프린트 채점</a></div>
      <div class="row" style="margin-top:8px"><span class="sub small">받기</span>
        <a class="btn ghost small" href="/dl/grading/${g.id}.pdf?view=1" target="_blank">채점 결과 PDF</a>
        <a class="btn ghost small" href="/dl/grading/${g.id}.json" download>채점 결과 JSON</a>
        ${(d.scans || []).length ? `<a class="btn ghost small" href="/scan/all/${g.id}.pdf?dl=1">스캔본 PDF</a>` : ""}
        ${wrong.length + uns.length ? `<a class="btn ghost small" href="#/tt/wrong/sp/${sid}/${d.print.code}" title="이 프린트에서 틀린 문항만 모아 새 프린트로">오답만 출제</a>` : ""}
        <span style="flex:1"></span>
        ${R.length > 1 ? `<button class="btn ghost small" id="delRound" title="${last.round}차 기록만 지워요">${last.round}차 지우기</button>` : ""}
        <button class="btn ghost small warn-t" id="delAll">채점 기록 지우기</button></div></div>
    <div class="card"><h2>스캔본 <span class="sub small">학생이 푼 종이를 스캔해 올려 두면 언제든 받고, 분석용 내보내기에 같이 들어가요</span></h2><div id="scanBox"></div></div>
    ${wrong.length ? `<div class="card"><h2>틀린 문항 ${wrong.length}개</h2><div class="wrongs">${wrong.map((it, k) => `<div class="wrong"><b>${esc(nob(it))}</b> ${it.repeat ? `<span class="tag rep">반복 오답</span>` : ""}${R.length > 1 ? ` <span class="small sub">${esc(roundsLine(it))}</span>` : ""}${it.mark.answer ? ` <span class="small sub">적은 답 ${esc(it.mark.answer)}</span>` : ""}
      ${it.png && !(k > 0 && wrong[k - 1].png === it.png) ? `<img src="${fileUrl(d.print.code + "/" + it.png)}" alt="">` : it.png ? `<div class="small sub">↑ 같은 문제</div>` : ""}</div>`).join("")}</div></div>` : ""}
    ${fixed.length ? `<div class="card"><h2>다시 풀어 고친 문항 ${fixed.length}개</h2>${fixed.map((it) => `<span class="tag o" title="${esc(roundsLine(it))}">${esc(nob(it))} · ${esc(roundsLine(it))}</span>`).join(" ")}</div>` : ""}
    ${uns.length ? `<div class="card"><h2>안 푼 문항</h2>${uns.map((it) => `<span class="tag u">${esc(nob(it))}</span>`).join(" ")}</div>` : ""}`;
  $$(".wrong img").forEach((im) => (im.onclick = () => zoom(im.src)));
  scanPanel($("#scanBox"), g.id, d.scans || [], (sc) => { d.scans = sc; }, { rounds: last.round || 1, meta: { title: d.print.title, student: d.student.name } });
  if ($("#retryGo")) $("#retryGo").onclick = () => startRetry(d.print.code, sid, d);
  if ($("#delRound")) $("#delRound").onclick = async () => {
    const v = await modal(`<h2>${last.round}차 기록을 지울까요?</h2><p>${last.round}차에 매긴 ${last.summary.total - last.summary.none}문항의 기록이 지워지고, ${last.round - 1}차까지의 결과가 최종이 돼요.</p><p class="sub small">되돌릴 수 없어요.</p>`,
      [{ label: "그만두기", value: null, cls: "ghost" }, { label: `${last.round}차 지우기`, value: 1, cls: "warn" }]);
    if (!v) return;
    try { await api(`gradings/${g.id}/delete`, { scope: "last_round" }); toast(`${last.round}차 기록을 지웠어요`); route(); } catch (e) { toast(e.message); }
  };
  $("#delAll").onclick = async () => {
    const v = await modal(`<h2>${esc(d.student.name)}의 이 프린트 채점 기록을 지울까요?</h2>
      <p>${R.length > 1 ? `1~${last.round}차 ` : ""}매긴 기록 전부${(d.scans || []).length ? `와 스캔본 ${d.scans.length}개` : ""}가 지워져요. 프린트와 출제 대상은 그대로 남아요.</p><p class="sub small">되돌릴 수 없어요. 활동 로그에는 지운 사실만 남아요.</p>`,
      [{ label: "그만두기", value: null, cls: "ghost" }, { label: "채점 기록 지우기", value: 1, cls: "warn" }]);
    if (!v) return;
    try { await api(`gradings/${g.id}/delete`, { scope: "all" }); toast("채점 기록을 지웠어요"); location.hash = "#/tt/students/" + sid; } catch (e) { toast(e.message); }
  };
};

/* ───────────────────────── 3. 수업 기록 */
async function viewClass() {
  const [students, settings] = await Promise.all([api("students"), api("settings")]);
  today = settings.today || today;
  // 오늘 이미 불러온 명단이 있으면 그대로, 없으면 오늘 프린트를 받은 학생으로 채워 둠
  const saved = store.get("classNames", null);
  const names0 = saved && saved.date === today ? saved.names : students.filter((s) => day(s.last_issued) === today).map((s) => s.name);
  const st = { date: today, days: store.get("classDays", 7), names: names0 };
  view.innerHTML = `<h1>수업 기록</h1>
    <div class="card"><div class="opt">
      <label class="k">날짜</label><div class="row"><input type="date" class="tin" id="cDate" value="${st.date}"><span class="sub small">최근</span><input type="number" class="tin" id="cDays" min="1" max="120" value="${st.days}" style="min-width:0;width:80px"><span class="sub small">일 동안 출제한 프린트를 같이 보여줘요</span></div>
      <label class="k">오늘 학생</label><div id="cNames"></div>
    </div><div class="row" style="margin-top:12px"><button class="btn big" id="cGo">불러오기</button><a class="btn ghost" href="#/tt/books/day" title="학생들이 교재를 몇 쪽까지 풀었는지 한 번에 적어요">교재 진도 적기</a></div></div>
    <div id="cOut"></div>`;
  const chips = nameChips($("#cNames"), students, st.names);
  const load = async () => {
    const names = chips.get();
    if (!names.length) return toast("학생 이름을 넣어 주세요");
    st.date = $("#cDate").value || today; st.days = Math.max(1, +$("#cDays").value || 7);
    store.set("classNames", { date: today, names }); store.set("classDays", st.days);
    const r = await api("students", { names });
    const data = await api(`class?date=${st.date}&days=${st.days}&students=${r.ids.join(",")}`);
    $("#cOut").innerHTML = data.map((s) => classCard(s, st)).join("") || `<div class="empty">학생이 없어요</div>`;
    data.forEach((s) => bindClassCard(s, st));
  };
  $("#cGo").onclick = () => load().catch((e) => toast(e.message));
  if (saved && saved.date === today && st.names.length) load().catch(() => {});
}

const KIND = {
  used: ["오늘 수업에 쓴 프린트", "오늘 출제한 것 중 수업에 쓴 것"],
  graded: ["채점한 프린트", "최근 출제한 것 중 채점한 것"],
  reviewed: ["오답 풀이한 프린트", "채점한 것 중 오답 풀이까지 한 것"],
  homework: ["숙제로 낸 프린트", "출제·채점한 것 중 숙제로 낸 것"],
};
function classLists(s, checkedGraded) {
  const appGraded = new Set(s.recent.filter((p) => p.grading && p.summary && p.summary.O + p.summary.X > 0).map((p) => p.id));
  const gradedSet = checkedGraded || new Set(s.saved.graded ? s.records.graded : [...appGraded]);
  return {
    used: s.today,
    graded: s.recent,
    reviewed: s.recent.filter((p) => gradedSet.has(p.id)),
    homework: s.recent,
    appGraded,
  };
}
function classCard(s, st) {
  const L = classLists(s);
  const pre = (k) => new Set(s.saved[k] ? s.records[k] : k === "graded" ? [...L.appGraded] : []);
  const li = (k, p) => `<label><input type="checkbox" data-k="${k}" value="${p.id}" ${pre(k).has(p.id) ? "checked" : ""}>
    <span><b>${esc(p.title)}</b> <span class="code small sub">${esc(p.code_fmt)}</span>${k !== "used" && p.issued !== st.date ? ` <span class="small muted">${p.issued.slice(5).replace("-", "/")}</span>` : ""}
    ${k === "graded" && p.summary ? ` <span class="small">${sumText(p.summary)}</span>` : ""}${k === "graded" && L.appGraded.has(p.id) && !s.saved.graded ? ` <span class="tag open">앱 채점</span>` : ""}</span></label>`;
  return `<div class="card" id="cc${s.student.id}"><div class="row" style="justify-content:space-between"><h2 style="margin:0"><a href="#/tt/students/${s.student.id}" style="color:inherit">${esc(s.student.name)}</a></h2>
    <div class="row"><span class="sub small">오늘 출제 ${s.today.length} · 최근 ${st.days}일 ${s.recent.length}</span><button class="btn small" data-all>4단계 모두 확인</button></div></div>
    <div class="steps" style="margin-top:10px">${Object.keys(KIND).map((k, i) => `<div class="step" data-step="${k}">
      <h3><span class="no">${i + 1}</span>${KIND[k][0]}</h3><div class="small muted">${KIND[k][1]}</div>
      <div class="list">${L[k].length ? L[k].map((p) => li(k, p)).join("") : `<div class="empty">${k === "used" ? "오늘 이 학생 앞으로 출제한 프린트가 없어요" : k === "reviewed" ? "2단계에서 채점한 프린트를 먼저 체크해 주세요" : "최근 출제한 프린트가 없어요"}</div>`}</div>
      <div class="row" style="justify-content:space-between;margin-top:auto"><span class="saved">${s.saved[k] ? "✓ 기록됨" : ""}</span><button class="btn small" data-save="${k}">확인</button></div></div>`).join("")}</div></div>`;
}
function bindClassCard(s, st) {
  const card = $("#cc" + s.student.id);
  const checked = (k) => $$(`input[data-k="${k}"]:checked`, card).map((x) => +x.value);
  const save = async (k) => {
    await api("class", { date: st.date, student_id: s.student.id, kind: k, print_ids: checked(k) });
    s.saved[k] = true; s.records[k] = checked(k);
    $(`[data-step="${k}"] .saved`, card).textContent = "✓ 기록됨 " + new Date().toTimeString().slice(0, 5);
  };
  // 2단계 체크가 바뀌면 3단계 후보를 다시 그림 (이미 체크한 것은 유지)
  const redrawReviewed = () => {
    const keep = new Set(checked("reviewed").concat(s.saved.reviewed ? s.records.reviewed : []));
    const g = new Set(checked("graded"));
    const list = s.recent.filter((p) => g.has(p.id));
    $(`[data-step="reviewed"] .list`, card).innerHTML = list.length ? list.map((p) => `<label><input type="checkbox" data-k="reviewed" value="${p.id}" ${keep.has(p.id) ? "checked" : ""}>
      <span><b>${esc(p.title)}</b> <span class="code small sub">${esc(p.code_fmt)}</span>${p.summary ? ` <span class="small">${sumText(p.summary)}</span>` : ""}</span></label>`).join("") : `<div class="empty">2단계에서 채점한 프린트를 먼저 체크해 주세요</div>`;
  };
  $$(`input[data-k="graded"]`, card).forEach((x) => (x.onchange = redrawReviewed));
  $$("[data-save]", card).forEach((b) => (b.onclick = () => save(b.dataset.save).then(() => toast(`${s.student.name} · ${KIND[b.dataset.save][0]} 기록했어요`)).catch((e) => toast(e.message))));
  $("[data-all]", card).onclick = async () => {
    try { for (const k of Object.keys(KIND)) await save(k); toast(`${s.student.name} · 오늘 수업 기록 완료`); } catch (e) { toast(e.message); }
  };
}

/* ───────────────────────── 4. 학생 */
async function viewStudents(id) {
  if (id) return studentDetail(+id);
  const list = await api("students");
  view.innerHTML = `<h1>학생</h1>
    <div class="card"><h2>학생 추가</h2><div class="row"><textarea class="tin" id="sNew" placeholder="이름을 쭉 적어 주세요 (줄바꿈·쉼표로 구분)" style="min-height:44px;flex:1"></textarea><button class="btn" id="sAdd">추가</button></div></div>
    <div class="card">${list.length ? `<table class="t"><tr><th>이름</th><th>학년</th><th>받은 프린트</th><th>마지막 출제</th><th>메모</th><th></th></tr>
      ${list.map((s) => `<tr class="click" data-href="#/tt/students/${s.id}" style="${s.active ? "" : "opacity:.5"}"><td><b>${esc(s.name)}</b></td><td>${esc(s.grade)}</td><td>${s.n_prints}${s.n_books ? ` <span class="small muted">· 교재 ${s.n_books}</span>` : ""}</td>
        <td class="sub small">${shortWhen(s.last_issued)}</td><td class="sub small">${esc(s.memo)}</td><td>${s.active ? "" : `<span class="tag">쉬는 중</span>`}</td></tr>`).join("")}</table>` : `<div class="empty">아직 학생이 없어요</div>`}</div>`;
  $("#sAdd").onclick = async () => {
    const names = splitNames($("#sNew").value);
    if (!names.length) return;
    await api("students", { names });
    toast(`${names.length}명 넣었어요`);
    route();
  };
  bindRows(view);
}

async function studentDetail(id) {
  const [d, allBooks] = await Promise.all([api("students/" + id), api("books").catch(() => [])]);
  const s = d.student;
  const myBooks = d.books || [];
  const freeBooks = allBooks.filter((b) => !b.students.some((x) => x.sid === s.id));
  const nWrongNow = d.prints.reduce((a, p) => a + ((p.summary && p.summary.X) || 0), 0);
  const recByDate = {};
  d.records.forEach((r) => ((recByDate[r.date] ||= {})[r.kind] ||= []).push(r));
  view.innerHTML = `<h1>${esc(s.name)} ${s.active ? "" : `<span class="tag">쉬는 중</span>`}</h1>
    <div class="card"><div class="opt">
      <label class="k">이름</label><input class="tin" id="eName" value="${esc(s.name)}">
      <label class="k">학년</label><input class="tin" id="eGrade" value="${esc(s.grade)}" placeholder="예: 중2">
      <label class="k">메모</label><input class="tin" id="eMemo" value="${esc(s.memo)}">
      <label class="k">상태</label><div id="eActive"></div>
    </div><div class="row" style="margin-top:10px"><button class="btn" id="eSave">저장</button></div></div>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">오답 · 기록 받기</h2>
      <a class="btn" href="#/tt/wrong/s/${s.id}">오답 모아 출제${nWrongNow ? ` <span class="small" style="opacity:.8">(지금 틀린 ${nWrongNow}문항)</span>` : ""}</a></div>
      <div class="row" style="margin-top:10px"><span class="sub small">기간</span><input type="date" class="tin" id="dFrom" style="min-width:0"> ~ <input type="date" class="tin" id="dTo" style="min-width:0">
        <span class="sub small">(비우면 전체)</span>
        <button class="btn ghost small" id="dPdf">학습 기록 PDF</button><button class="btn ghost small" id="dJson">학습 기록 JSON</button></div>
      <p class="sub small" style="margin:6px 0 0">JSON에는 프린트별·문항별 결과(1차·2차·3차), 틀린 적 있는 문항의 정답·유형·정답률·전사본(있으면)이 들어가요 — 유사 문항을 만들 때 Claude에게 같이 주세요.</p></div>
    <div class="card"><h2>반복 오답 <span class="sub small">같은 문항을 두 번 이상 틀린 것</span></h2>${d.repeat_wrong.length ? `<div class="wrongs">${d.repeat_wrong.map((w) => `<div class="wrong">
      <span class="tag rep">${w.count}번 틀림</span> <span class="small sub">${w.where.map((x) => `${esc(x.title)} ${esc(x.label && !/^\d+$/.test(x.label) ? x.label : (x.label || x.seq) + "번")}`).join(" · ")}</span>
      ${w.png ? `<img src="${fileUrl(w.png)}" alt="">` : ""}</div>`).join("")}</div>` : `<div class="empty">아직 없어요</div>`}</div>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">교재 <span class="sub small">스캔본은 교재마다 모아요</span></h2>
        ${freeBooks.length ? `<select class="tin" id="bkAdd" style="min-width:0"><option value="">교재 붙이기…</option>${freeBooks.map((b) => `<option value="${b.code}">${esc(b.title)}${b.publisher ? ` (${esc(b.publisher)})` : ""}</option>`).join("")}</select>`
          : `<a class="btn ghost small" href="#/tt/books">${allBooks.length ? "교재 탭" : "교재 등록하러 가기"}</a>`}</div>
      ${myBooks.length ? `<table class="t" style="margin-top:8px"><tr><th>교재</th><th>진도</th><th>마지막 채점</th><th>해설지</th><th></th></tr>
        ${myBooks.map((b) => `<tr><td><a href="#/tt/books/${b.master_code}"><b>${esc(b.title)}</b></a><div class="sub small">${bookSub(b)}${bookSub(b) ? " · " : ""}붙인 날 ${md(b.since)}</div></td>
          <td>${progText(b)}${b.unchecked && b.unchecked.known && b.unchecked.text ? `<div class="small warn-t" title="적은 진도와 채점한 쪽으로 어림했어요">채점 기록 없는 쪽 ${esc(b.unchecked.text)}</div>` : ""}</td>
          <td>${gradedText(b)}</td><td>${solText(b)}</td>
          <td>${b.grading ? bookScanBtn({ gid: b.grading.id, n_scans: b.n_scans }, b.title, s.name) : ""}</td></tr>`).join("")}</table>`
        : `<div class="empty">아직 붙인 교재가 없어요</div>`}</div>
    <div class="card"><h2>받은 프린트</h2>${d.prints.length ? `<table class="t"><tr><th>출제일</th><th>코드</th><th>제목</th><th>채점</th><th>결과</th><th></th></tr>
      ${d.prints.map((p) => `<tr><td class="sub small">${shortWhen(p.issued_at)}</td><td class="code">${esc(p.code_fmt)}</td><td>${esc(p.title)}</td>
        <td>${p.grading ? statusTag(p.grading.status) : `<span class="muted small">안 함</span>`}${p.n_rounds > 1 ? ` <span class="tag ses">${p.n_rounds}차</span>` : ""}${gdLine(p.graded_days)}</td><td>${sumText(p.summary)}${roundNote(p)}</td>
        <td class="row" style="gap:4px;flex-wrap:wrap"><button class="btn small ghost" data-pout="${p.code}" title="${esc(s.name)} 이름을 넣은 시험지">출력</button>
          ${p.grading ? `<button class="btn small ghost" data-scan="${p.grading.id}" data-r="${p.n_rounds || 1}" data-t="${esc(p.title)}" title="학생이 푼 종이 스캔본 올리기 · 1차·2차 표시">${scanLabel({ length: p.n_scans || 0 })}</button>` : ""}
          ${p.grading ? Array.from({ length: p.n_rounds || 1 }, (_, k) => k + 1).filter((r) => p.grading.status === "done" || r < (p.n_rounds || 1))
            .map((r) => `<a class="btn small ghost" href="#/tt/grade/${p.code}/${s.id}${r < (p.n_rounds || 1) ? "/fix" + r : ""}" title="${r}차에 매긴 결과를 바꿔요">${r}차 수정</a>`).join("") : ""}
          <a class="btn small ${p.grading && p.grading.status === "done" ? "ghost" : ""}" href="#/tt/grade/${p.code}/${s.id}${p.grading && p.grading.status === "done" ? "/done" : ""}">${p.grading ? (p.grading.status === "done" ? "보기" : "이어서") : "채점"}</a></td></tr>`).join("")}</table>
      <p class="sub small" style="margin:6px 0 0">스캔본은 채점을 시작한 프린트에 올려요. 아직 채점하지 않았으면 「채점」을 먼저 눌러 주세요.</p>` : `<div class="empty">아직 없어요</div>`}</div>
    <div class="card"><h2>수업 기록</h2>${Object.keys(recByDate).length ? `<table class="t"><tr><th>날짜</th>${Object.keys(KIND).map((k) => `<th>${KIND[k][0].replace(" 프린트", "").replace("오늘 ", "")}</th>`).join("")}</tr>
      ${Object.entries(recByDate).map(([dte, r]) => `<tr><td><b>${dte}</b></td>${Object.keys(KIND).map((k) => `<td class="small">${(r[k] || []).map((x) => esc(x.title)).join("<br>") || "<span class='muted'>-</span>"}</td>`).join("")}</tr>`).join("")}</table>
      <p class="sub small">고치려면 수업 기록 탭에서 그 날짜와 이 학생을 불러와 다시 확인하세요.</p>` : `<div class="empty">아직 없어요</div>`}</div>`;
  let active = s.active;
  seg($("#eActive"), [["1", "다니는 중"], ["0", "쉬는 중"]], String(s.active), (v) => (active = +v));
  $("#eSave").onclick = async () => {
    try { await api("students/" + id, { name: $("#eName").value, grade: $("#eGrade").value, memo: $("#eMemo").value, active }); toast("저장했어요"); route(); }
    catch (e) { toast(e.message.includes("UNIQUE") ? "같은 이름의 학생이 이미 있어요" : e.message); }
  };
  $$(".wrong img").forEach((im) => (im.onclick = () => zoom(im.src)));
  $$("[data-pout]").forEach((b) => (b.onclick = () => printOut(b.dataset.pout, id)));
  bindScanButtons(view, () => s.name);
  if ($("#bkAdd")) $("#bkAdd").onchange = async (e) => {
    const code = e.target.value;
    if (!code) return;
    e.target.disabled = true;
    try { await api("books/" + code, { assign: s.id }); toast(`「${allBooks.find((b) => b.code === code)?.title || "교재"}」를 붙였어요`); route(); }
    catch (err) { toast(err.message, 4000); e.target.disabled = false; e.target.value = ""; }
  };
  const per = () => { const q = new URLSearchParams(); if ($("#dFrom").value) q.set("from", $("#dFrom").value); if ($("#dTo").value) q.set("to", $("#dTo").value); return q.toString(); };
  $("#dPdf").onclick = () => openLink(`/dl/student/${id}.pdf?view=1&${per()}`);
  $("#dJson").onclick = () => openLink(`/dl/student/${id}.json?${per()}`, true);
}

/* ───────────────────────── 교재 (#/tt/books · #/tt/books/<교재 코드> · #/tt/books/day[/날짜])
   교재 하나를 학생마다 채점 기록 하나로 둔다(백엔드 options.textbook). 스캔본은 프린트와 같은 창(1 · 2 · 3차).
   교재 기록(tt_book_logs): 진도(그날 몇 쪽까지) · 채점한 날(몇 차 · 쪽) · 해설지 준 날 → 그대로 둔 날수 · 채점 기록이 없는 쪽(어림).
   분석(채점 표시 읽기 · 문항 · 정답 쌓기) · 포스트잇은 다음 단계에서 붙인다. */
const IDLE_Y = 14, IDLE_R = 30;          // 마지막 채점에서 14일 넘으면 노랑, 30일 넘으면 빨강
const md = (d) => (d ? String(d).slice(5).replace("-", "/") : "");
function bookWhere(p) {               // 교재(교재 자체나 학생 몫)면 그 교재 화면 주소, 아니면 null
  const b = p && p.options && p.options.textbook;
  return b ? "#/tt/books/" + (b.role === "master" ? p.code : b.master_code || "") : null;
}
function bookSub(b) { return [b.publisher, b.grade].filter(Boolean).map(esc).join(" · "); }
function bookScanBtn(x, title, name) {
  return x.gid ? `<button class="btn small ghost" data-scan="${x.gid}" data-r="${BOOK_R}" data-t="${esc(title)}" data-n="${esc(name)}" data-had="${x.n_scans || 0}" title="학생이 푼 교재 스캔본 올리기 · 받기 · 1·2·3차 표시">${scanLabel({ length: x.n_scans || 0 })}</button>` : "";
}
// 그대로 둔 날수 — 마지막 채점(채점 기록 · 스캔본 올린 날)부터, 채점이 없으면 붙인 날부터
function idleTag(x) {
  const n = x.idle_days ?? 0, cls = n >= IDLE_R ? " r" : n >= IDLE_Y ? " y" : "";
  if (x.never_graded) return `<span class="tag idle${cls}" title="붙인 날(${md(x.since)})부터 채점 기록이 없어요">채점 없음 · ${n}일</span>`;
  return `<span class="tag idle${cls}" title="마지막 채점 ${md(x.last_graded)}">${n ? `${n}일째 그대로` : "오늘 채점"}</span>`;
}
const progText = (x) => (x.last_solved ? `<b>${x.last_solved.page_to}쪽</b>까지 <span class="sub small">${md(x.last_solved.day)}</span>` : `<span class="muted small">없음</span>`);
const gradedText = (x) => (x.last_graded ? `${md(x.last_graded)} ${idleTag(x)}` : idleTag(x));
const solText = (x) => (x.solution ? `<span class="tag done" title="해설지를 준 날">해설지 ${md(x.solution.day)}</span>` : `<span class="muted small">안 줌</span>`);
const logsWarn = (ok) => (ok === false ? `<div class="card" style="background:#fffbeb;border-color:#fde68a"><b>교재 기록 표가 DB에 아직 없어요.</b> <span class="small">진도 · 채점한 날 · 해설지를 적으려면 supabase/2026-11_tt_book_logs.sql 을 넣어야 해요.</span></div>` : "");
function bookHowto() {
  return `<div class="card"><h2>스캔본 올리는 법 <span class="sub small">프린트와 같아요</span></h2><ol class="small" style="margin:0;padding-left:20px;line-height:1.8">
    <li>학생 이름 옆 「스캔본」을 눌러요.</li>
    <li>언제 스캔한 것인지(1차 · 2차 · 3차 채점 때 / 확실하지 않음)를 고르고, 파일(PDF · 사진)을 놓아요. 안드로이드에서는 「📷 vFlat으로 스캔」 → vFlat에서 「공유 → 강사도구」를 누르면 그 학생 교재로 저절로 올라와요.</li>
    <li>올린 스캔본은 받기 · 한 PDF로 보기 · 지우기 · 차수 바꾸기가 돼요.</li></ol>
    <p class="sub small" style="margin:8px 0 0">스캔본을 분석해 채점 · 정답을 쌓는 기능과 포스트잇은 다음에 붙여요.</p></div>`;
}
async function viewBooks(code, arg) {
  if (code === "day") return bookDayView(arg);
  if (code) return bookDetail(normCode(code));
  const [list, students] = await Promise.all([api("books"), api("students")]);
  const stale = list.flatMap((b) => b.students.filter((x) => x.active && (x.idle_days ?? 0) >= IDLE_Y).map((x) => ({ ...x, book: b })))
    .sort((a, b) => b.idle_days - a.idle_days);
  view.innerHTML = `<h1>교재</h1>
    ${logsWarn(list.length ? list[0].logs_ok : true)}
    <div class="card"><div class="row" style="justify-content:space-between"><div class="row"><a class="btn big" href="#/tt/books/day">수업 끝 진도 적기</a>
        <span class="sub small">학생들이 교재를 몇 쪽까지 풀었는지 한 번에 적어요</span></div>
      <div class="row"><span class="sub small">교재 기록 받기</span><a class="btn ghost small" href="/dl/books.json" download title="학생별 교재 · 진도 · 채점한 날 · 채점 기록이 없는 쪽 · 해설지 — 숙제 낼 때 Claude에게 주세요">JSON</a>
        <a class="btn ghost small" href="/dl/books.csv" download title="엑셀에서 여는 표">CSV</a></div></div></div>
    ${stale.length ? `<div class="card"><h2>오래 채점하지 않은 교재 <span class="sub small">마지막 채점에서 ${IDLE_Y}일 넘게 (다니는 학생만)</span></h2>
      <table class="t"><tr><th>학생</th><th>교재</th><th>마지막 채점</th><th>진도</th><th>해설지</th></tr>
      ${stale.map((x) => `<tr class="click" data-href="#/tt/books/${x.book.code}"><td><b>${esc(x.name)}</b></td><td>${esc(x.book.title)}</td><td>${gradedText(x)}</td><td>${progText(x)}</td><td>${solText(x)}</td></tr>`).join("")}</table></div>` : ""}
    <div class="card"><h2>교재 목록</h2>${list.length ? `<table class="t"><tr><th>교재</th><th>출판사 · 학년</th><th>학생 · 스캔본</th><th></th></tr>
      ${list.map((b) => `<tr class="click" data-href="#/tt/books/${b.code}"><td><b>${esc(b.title)}</b>${b.memo ? `<div class="small muted">${esc(b.memo)}</div>` : ""}</td><td class="small">${bookSub(b) || "-"}</td>
        <td><div class="chips">${b.students.map((x) => `<span class="bkst${x.active ? "" : " off"}">${esc(x.name)} ${idleTag(x)} ${bookScanBtn(x, b.title, x.name)}</span>`).join("") || `<span class="muted small">아직 없음</span>`}</div></td>
        <td><a class="btn small ghost nowrap" href="#/tt/books/${b.code}">학생 · 기록</a></td></tr>`).join("")}</table>` : `<div class="empty">아직 등록한 교재가 없어요</div>`}</div>
    <div class="card"><h2>교재 등록 <span class="sub small">학생마다 교재 하나에 스캔본 · 진도 · 채점 기록을 모아요</span></h2>
      <div class="opt">
        <label class="k">교재 이름</label><input class="tin" id="bTitle" placeholder="예: 개념원리 중2-1" autocomplete="off">
        <label class="k">출판사</label><input class="tin" id="bPub" placeholder="예: 개념원리" autocomplete="off">
        <label class="k">학년</label><input class="tin" id="bGrade" placeholder="예: 중2" autocomplete="off">
        <label class="k">메모</label><input class="tin" id="bMemo" placeholder="없어도 돼요" autocomplete="off">
        <label class="k">학생</label><div id="bStu"></div>
      </div>
      <div class="row" style="margin-top:10px"><button class="btn" id="bAdd">등록</button><span class="sub small">학생은 나중에 붙여도 돼요</span></div></div>
    ${bookHowto()}`;
  const chips = nameChips($("#bStu"), students);
  const btn = $("#bAdd");
  btn.onclick = async () => {
    const title = $("#bTitle").value.trim();
    if (!title) { toast("교재 이름을 넣어 주세요"); $("#bTitle").focus(); return; }
    btn.disabled = true;
    try {
      const r = await api("books", { title, publisher: $("#bPub").value, grade: $("#bGrade").value, memo: $("#bMemo").value, students: chips.get() });
      toast(`「${title}」 등록했어요${r.n_students ? ` · 학생 ${r.n_students}명` : ""}`);
      route();
    } catch (e) { toast(e.message, 4000); btn.disabled = false; }
  };
  bindRows(view);
  bindScanButtons(view);
}
const LOG_KIND = { solved: "진도", graded: "채점", solution: "해설지" };
function logLine(l) {
  const what = l.kind === "solved" ? `${l.pages ? esc(l.pages) + "쪽" : ""}${l.pages ? " · " : ""}<b>${l.page_to}쪽</b>까지`
    : l.kind === "graded" ? `${l.round ? l.round + "차 " : ""}${l.pages ? esc(l.pages) + "쪽" : "<span class='muted'>쪽 안 적음</span>"}` : "줌";
  return `<tr><td class="nowrap">${md(l.day)}</td><td><span class="tag ${l.kind === "graded" ? "open" : l.kind === "solution" ? "done" : "ses"}">${LOG_KIND[l.kind]}</span></td><td>${what}</td>
    <td class="sub small">${esc(l.note || "")}</td><td><button class="x" data-bldel="${l.id}" title="이 기록 지우기">×</button></td></tr>`;
}
async function bookDetail(code) {
  let b;
  try { b = await api("books/" + code); } catch (e) {
    let p = null;                      // 학생 몫 코드로 왔으면 그 교재로
    try { p = await api("prints/" + code); } catch { /* 없음 */ }
    const bw = bookWhere(p);
    if (bw && bw !== "#/tt/books/" + code) { location.replace(bw); return; }
    throw e;
  }
  const students = await api("students");
  const have = new Set(b.students.map((x) => x.sid));
  const free = students.filter((s) => s.active && !have.has(s.id));
  const today = todayStr();
  const openSid = store.get("bookOpen", null);
  view.innerHTML = `<h1>${esc(b.title)} ${bookSub(b) ? `<span class="sub small">${bookSub(b)}</span>` : ""}</h1>
    ${logsWarn(b.logs_ok)}
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">이 교재를 쓰는 학생</h2><a class="btn ghost small" href="#/tt/books/day">수업 끝 진도 적기</a></div>
      ${b.students.length ? `<table class="t" style="margin-top:8px"><tr><th>학생</th><th>진도</th><th>마지막 채점</th><th>해설지</th><th>스캔본</th><th></th></tr>
      ${b.students.map((x) => `<tr${x.active ? "" : ` style="opacity:.55"`}><td><a href="#/tt/students/${x.sid}"><b>${esc(x.name)}</b></a><div class="sub small">붙인 날 ${md(x.since)}</div></td>
        <td>${progText(x)}${x.unchecked && x.unchecked.known && x.unchecked.text ? `<div class="small warn-t" title="적은 진도와 채점한 쪽으로 어림했어요">채점 기록 없는 쪽 ${esc(x.unchecked.text)}</div>` : ""}</td>
        <td>${gradedText(x)}</td>
        <td>${x.solution ? `${solText(x)} <button class="x" data-bldel="${x.solution.id}" title="해설지 기록 지우기">×</button>` : `<button class="btn small ghost" data-sol="${x.code}" title="오늘 해설지를 줬다고 적어요">해설지 줬어요</button>`}</td>
        <td>${bookScanBtn(x, b.title, x.name)}</td>
        <td>${x.n_scans || (x.logs || []).length ? "" : `<button class="btn small ghost warn-t" data-unas="${x.sid}" title="이 학생에게서 교재를 빼요 (스캔본 · 기록이 없을 때만)">빼기</button>`}</td></tr>
        <tr class="blogrow"><td colspan="6"><details data-sid="${x.sid}"${openSid === x.sid ? " open" : ""}><summary class="small">기록 ${(x.logs || []).length} · 적기</summary>
          <div class="row blogform" data-code="${x.code}">
            <select class="tin" data-f="kind"><option value="graded">채점한 날</option><option value="solved">진도(몇 쪽까지)</option></select>
            <input type="date" class="tin" data-f="day" value="${today}">
            <select class="tin" data-f="round"><option value="1">1차</option><option value="2">2차</option><option value="3">3차</option></select>
            <input class="tin" data-f="pages" placeholder="채점한 쪽 (예: 12-20, 25) · 비워도 돼요" autocomplete="off">
            <input class="tin" data-f="note" placeholder="메모" autocomplete="off">
            <button class="btn small" data-blsave>적기</button></div>
          ${(x.logs || []).length ? `<table class="t small" style="margin-top:6px">${x.logs.map(logLine).join("")}</table>` : `<div class="sub small" style="margin-top:6px">아직 기록이 없어요</div>`}
        </details></td></tr>`).join("")}</table>`
      : `<div class="empty">아직 붙인 학생이 없어요</div>`}
      <div style="margin-top:12px"><b class="small">학생 붙이기</b> <span class="sub small">눌러서 바로 붙여요</span><div class="chips" style="margin-top:6px">${free.map((s) => `<span class="chip pick" data-as="${s.id}">+ ${esc(s.name)}</span>`).join("") || `<span class="muted small">붙일 학생이 없어요</span>`}</div></div></div>
    <div class="card"><h2>교재 정보</h2><div class="opt">
        <label class="k">교재 이름</label><input class="tin" id="bTitle" value="${esc(b.title)}" autocomplete="off">
        <label class="k">출판사</label><input class="tin" id="bPub" value="${esc(b.publisher)}" autocomplete="off">
        <label class="k">학년</label><input class="tin" id="bGrade" value="${esc(b.grade)}" autocomplete="off">
        <label class="k">메모</label><input class="tin" id="bMemo" value="${esc(b.memo)}" autocomplete="off">
      </div><div class="row" style="margin-top:10px"><button class="btn" id="bSave">저장</button>
        ${b.students.length ? "" : `<button class="btn ghost warn-t" id="bDel">교재 지우기</button>`}<a class="btn ghost" href="#/tt/books">교재 목록</a></div></div>
    ${bookHowto()}`;
  bindScanButtons(view, undefined, (bt, sc) => { if (!sc.length !== !+bt.dataset.had) route(); });     // 스캔본이 생기거나 다 지우면 「빼기」를 다시 그림
  $$("details[data-sid]", view).forEach((d) => d.addEventListener("toggle", () => { if (d.open) store.set("bookOpen", +d.dataset.sid); else if (store.get("bookOpen", null) === +d.dataset.sid) store.set("bookOpen", null); }));
  $$(".blogform", view).forEach((f) => {
    const kind = $('[data-f="kind"]', f), round = $('[data-f="round"]', f), pages = $('[data-f="pages"]', f);
    const sync = () => {
      const s = kind.value === "solved";
      round.hidden = s;
      pages.placeholder = s ? "몇 쪽까지 (예: 45 또는 30-45)" : "채점한 쪽 (예: 12-20, 25) · 비워도 돼요";
      pages.classList.remove("bad");
    };
    kind.onchange = sync;
    pages.oninput = () => pages.classList.toggle("bad", kind.value === "solved" ? !parseProgress(pages.value) || !!parseProgress(pages.value).empty : !parsePages(pages.value));
    $("[data-blsave]", f).onclick = async (e) => {
      const solved = kind.value === "solved";
      if (solved ? !parseProgress(pages.value) || parseProgress(pages.value).empty : !parsePages(pages.value)) {
        pages.classList.add("bad"); toast(solved ? "진도는 45 또는 30-45 처럼 적어 주세요" : "채점한 쪽은 12-20, 25 처럼 적어 주세요"); return;
      }
      const day = $('[data-f="day"]', f).value || todayStr(), note = $('[data-f="note"]', f).value;
      e.currentTarget.disabled = true;
      try {
        const r = await api("booklogs", solved ? { code: f.dataset.code, kind: "solved", day, progress: pages.value, note } : { code: f.dataset.code, kind: "graded", day, round: +round.value, pages: pages.value, note });
        undoToast(r.events && r.events.length ? (solved ? "진도를 적었어요" : "채점한 날을 적었어요") : "바뀐 것이 없어요", r.events); route();
      } catch (err) { toast(err.message, 5000); route(); }
    };
    sync();
  });
  $$("[data-bldel]", view).forEach((x) => (x.onclick = async () => {
    if (!confirmInline(x)) return;
    try { const r = await api("booklogs/" + x.dataset.bldel, { delete: true }); undoToast("기록을 지웠어요", r.events); route(); } catch (e) { toast(e.message, 5000); }
  }));
  $$("[data-sol]", view).forEach((x) => (x.onclick = async () => {
    try { const r = await api("booklogs", { code: x.dataset.sol, kind: "solution", day: todayStr() }); undoToast("해설지를 줬다고 적었어요", r.events); route(); } catch (e) { toast(e.message, 5000); }
  }));
  $$("[data-as]", view).forEach((c) => (c.onclick = async () => {
    if (c.dataset.busy) return;
    c.dataset.busy = "1";
    try { await api("books/" + b.code, { assign: +c.dataset.as }); toast(`${c.textContent.replace(/^\+\s*/, "")}에게 붙였어요`); route(); }
    catch (e) { toast(e.message, 4000); c.dataset.busy = ""; }
  }));
  $$("[data-unas]", view).forEach((x) => (x.onclick = async () => {
    if (!confirmInline(x)) return;
    try { await api("books/" + b.code, { unassign: +x.dataset.unas }); toast("뺐어요"); route(); } catch (e) { toast(e.message, 5000); }
  }));
  $("#bSave").onclick = async () => {
    try { await api("books/" + b.code, { title: $("#bTitle").value, publisher: $("#bPub").value, grade: $("#bGrade").value, memo: $("#bMemo").value }); toast("저장했어요"); route(); }
    catch (e) { toast(e.message, 4000); }
  };
  if ($("#bDel")) $("#bDel").onclick = async () => {
    const v = await modal(`<h2>「${esc(b.title)}」를 지울까요?</h2><p>붙인 학생이 없는 교재만 지울 수 있어요.</p>`,
      [{ label: "그만두기", value: null, cls: "ghost" }, { label: "지우기", value: 1, cls: "warn" }]);
    if (!v) return;
    try { await api("books/" + b.code, { delete: true }); toast("지웠어요"); location.hash = "#/tt/books"; } catch (e) { toast(e.message, 4000); }
  };
}
// 수업 끝 진도 적기 — 다니는 학생 × 붙인 교재, 이날 몇 쪽까지(45 · 30-45) + 채점한 쪽(있으면). 바꾼 칸만 저장, 비우면 그날 기록을 지움
async function bookDayView(date) {
  const d = await api("books/day" + (date ? "?date=" + encodeURIComponent(date) : ""));
  const nBooks = d.students.reduce((a, s) => a + s.books.length, 0);
  const g0 = (b) => b.graded.find((x) => x.round === 1) || b.graded[0] || null;
  view.innerHTML = `<h1>수업 끝 진도 적기</h1>
    ${logsWarn(d.logs_ok)}
    <div class="card"><div class="row"><b>날짜</b><input type="date" class="tin" id="dDay" value="${d.date}" style="min-width:0">
      <input class="tin" id="dQ" placeholder="학생 이름으로 찾기" autocomplete="off" style="min-width:0;width:180px">
      <span class="sub small">진도는 「45」(45쪽까지) 또는 「30-45」 · 채점한 쪽은 「46-52, 55」처럼 · 비운 칸은 저장하지 않아요</span></div></div>
    <div class="card">${nBooks ? `<table class="t dayt"><tr><th>학생</th><th>교재</th><th>지난 진도</th><th>이날 몇 쪽까지</th><th>채점한 쪽 <span class="sub small">(있으면)</span></th></tr>
      ${d.students.map((s) => s.books.map((b, i) => `<tr data-sname="${esc(s.name)}" data-code="${b.code}">
        ${i === 0 ? `<td rowspan="${s.books.length}"><b>${esc(s.name)}</b>${s.grade ? `<div class="sub small">${esc(s.grade)}</div>` : ""}</td>` : ""}
        <td>${esc(b.title)}${b.publisher ? `<div class="sub small">${esc(b.publisher)}</div>` : ""}</td>
        <td class="small">${b.prev ? `${b.prev.page_to}쪽 <span class="sub">${md(b.prev.day)}</span>` : `<span class="muted">-</span>`}</td>
        <td><input class="tin pin" data-p data-init="${esc(b.today ? b.today.pages || String(b.today.page_to) : "")}" value="${esc(b.today ? b.today.pages || String(b.today.page_to) : "")}" placeholder="${b.prev ? `예: ${b.prev.page_to + 6}` : "예: 45"}" inputmode="numeric" autocomplete="off"></td>
        <td><div class="row" style="gap:4px;flex-wrap:nowrap"><select class="tin" data-r data-init="${g0(b) ? g0(b).round || 1 : 1}" style="min-width:0">${[1, 2, 3].map((r) => `<option value="${r}"${(g0(b) ? g0(b).round || 1 : 1) === r ? " selected" : ""}>${r}차</option>`).join("")}</select>
          <input class="tin pin" data-g data-init="${esc(g0(b) ? g0(b).pages : "")}" value="${esc(g0(b) ? g0(b).pages : "")}" placeholder="예: 46-52" autocomplete="off">
          ${b.graded.filter((x) => x !== g0(b)).map((x) => `<span class="sub small nowrap">${x.round || ""}차 ${esc(x.pages)}</span>`).join(" ")}</div></td></tr>`).join("")).join("")}</table>
      <div class="row" style="margin-top:12px"><button class="btn big" id="dSave">저장</button><span class="sub small" id="dNote"></span></div>`
      : `<div class="empty">교재를 붙인 학생이 없어요. 교재 탭에서 교재를 등록하고 학생을 붙여 주세요.</div>`}</div>`;
  $("#dDay").onchange = () => { location.hash = "#/tt/books/day/" + ($("#dDay").value || ""); };
  $("#dQ").oninput = () => {
    const q = $("#dQ").value.trim();
    $$("tr[data-sname]", view).forEach((tr) => (tr.hidden = !!q && !tr.dataset.sname.includes(q)));
  };
  const check = (inp) => {
    const bad = inp.hasAttribute("data-p") ? !parseProgress(inp.value) : !parsePages(inp.value);
    inp.classList.toggle("bad", bad);
    return !bad;
  };
  const changed = () => $$("tr[data-code]", view).map((tr) => {
    const p = $("[data-p]", tr), g = $("[data-g]", tr), r = $("[data-r]", tr);
    const row = { code: tr.dataset.code };
    if (p.value.trim() !== p.dataset.init) row.progress = p.value.trim();
    if (g.value.trim() !== g.dataset.init || (g.value.trim() && r.value !== r.dataset.init)) { row.graded = g.value.trim(); row.round = +r.value; }
    return Object.keys(row).length > 1 ? row : null;
  }).filter(Boolean);
  const note = () => { if ($("#dNote")) { const n = changed().length; $("#dNote").textContent = n ? `바꾼 줄 ${n}개` : ""; } };
  $$("input.pin", view).forEach((inp) => (inp.oninput = () => { check(inp); note(); }));
  $$("select[data-r]", view).forEach((s) => (s.onchange = note));
  if ($("#dSave")) $("#dSave").onclick = async () => {
    const bad = $$("input.pin", view).filter((inp) => !check(inp));
    if (bad.length) { bad[0].focus(); return toast(`알아볼 수 없는 칸이 ${bad.length}개 있어요 — 진도는 45 또는 30-45, 채점한 쪽은 46-52, 55 처럼`, 5000); }
    const rows = changed();
    if (!rows.length) return toast("바꾼 칸이 없어요");
    $("#dSave").disabled = true;
    try { const r = await api("books/day", { date: d.date, rows }); undoToast(`${rows.length}줄 저장했어요`, r.events); route(); }
    catch (e) { toast(e.message, 5000); $("#dSave").disabled = false; }
  };
}

/* ───────────────────────── 오답 모아 출제 (#/tt/wrong/s/<학생> · #/tt/wrong/p/<코드> · #/tt/wrong/sp/<학생>/<코드>) */
async function viewWrong(kind, a, b) {
  const students = await api("students");
  const st = { sids: new Set(), codes: [], which: store.get("wrongWhich", "final"), withU: store.get("wrongU", false), tpl: store.get("wrongTpl", "문정중"),
    items: [], sel: new Set(), filter: null };
  if ((kind === "s" || kind === "sp") && a) st.sids.add(+a);
  if (kind === "sp" && b) st.codes = [normCode(b)];
  if (kind === "p" && a) {
    st.codes = [normCode(a)];
    const p = await api("prints/" + normCode(a));
    p.gradings.forEach((g) => st.sids.add(g.student_id));
  }
  const RK = { O: "O", X: "X", U: "안 풂" };
  view.innerHTML = `<h1>오답 모아 출제</h1>
    <p class="sub" style="margin-top:-6px">채점 기록에서 틀린 문항을 골라 <b>새 프린트</b>로 짜요. 새 프린트에도 코드가 붙어 그대로 채점할 수 있고, 또 틀리면 반복 오답으로 잡혀요.</p>
    <div class="card"><div class="opt">
      <label class="k">학생</label><div class="chips" id="wStu"></div>
      <label class="k">범위</label><div class="row"><span id="wCodes"></span><span class="sub small">채점한 날</span><input type="date" class="tin" id="wFrom" style="min-width:0"> ~ <input type="date" class="tin" id="wTo" style="min-width:0"><span class="sub small">(비우면 전체)</span></div>
      <label class="k">어떤 문항</label><div class="row"><div id="wWhich"></div><label class="small"><input type="checkbox" id="wU" ${st.withU ? "checked" : ""}> 안 푼 문항도</label></div>
    </div></div>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0" id="wHead">문항</h2>
      <div class="row"><button class="btn ghost small" id="wAll">모두 고르기</button><button class="btn ghost small" id="wNone">모두 빼기</button></div></div>
      <div class="wgrid" id="wList" style="margin-top:10px"></div></div>
    <div class="card"><h2>출제</h2><div class="opt">
      <label class="k">제목</label><input class="tin" id="wTitle" placeholder="오답 모음 ${today.slice(5).replace("-", "/")}">
      <label class="k">부제</label><input class="tin" id="wSub" placeholder="(비우면 원래 프린트 이름)">
      <label class="k">양식</label><div id="wTpl"></div>
      <label class="k">출제 대상</label><div class="sub" id="wTg"></div>
    </div>
    <div class="row" style="margin-top:12px"><button class="btn big" id="wMake" disabled>PDF로 출제</button><button class="btn ghost" id="wJson" disabled>JSON 받기</button></div>
    <p class="sub small"><b>PDF</b>: 고른 문항으로 시험지·정답해설을 새로 짜고 코드를 붙여 프린트함에 넣어요(학생 이름은 출력할 때 넣어요).
      <b>JSON</b>: 고른 문항의 번호·정답·유형·정답률·학생별 결과(1차·2차…)·전사본(있으면) — 유사 문항을 만들 때 시험지 PDF와 함께 Claude에게 주세요.</p>
    <div id="wOut"></div></div>`;
  seg($("#wWhich"), [["final", "지금도 틀린 문항"], ["ever", "한 번이라도 틀린 문항"], ["repeat", "두 번 넘게 틀린 문항"]], st.which, (v) => { st.which = v; store.set("wrongWhich", v); load(); });
  seg($("#wTpl"), TEMPLATES, st.tpl, (v) => { st.tpl = v; store.set("wrongTpl", v); });
  $("#wU").onchange = (e) => { st.withU = e.target.checked; store.set("wrongU", st.withU); load(); };
  ["wFrom", "wTo"].forEach((k) => ($("#" + k).onchange = () => load()));
  const drawStu = () => {
    const list = students.filter((s) => s.active || st.sids.has(s.id));
    $("#wStu").innerHTML = list.map((s) => `<span class="chip ${st.sids.has(s.id) ? "sel" : "pick"}" data-id="${s.id}">${esc(s.name)}</span>`).join("") || `<span class="empty">학생이 없어요</span>`;
    $$("#wStu .chip").forEach((c) => (c.onclick = () => { const id = +c.dataset.id; st.sids.has(id) ? st.sids.delete(id) : st.sids.add(id); drawStu(); load(); }));
    $("#wTg").textContent = st.sids.size ? students.filter((s) => st.sids.has(s.id)).map((s) => s.name).join(", ") + " (프린트에 이름은 출력할 때 넣어요)" : "(없음)";
    $("#wCodes").innerHTML = st.codes.map((c) => `<span class="chip">프린트 ${esc(fmtCode(c))}<button data-rmc="${c}" title="빼고 기간으로">×</button></span>`).join(" ");
    $$("[data-rmc]").forEach((x) => (x.onclick = () => { st.codes = st.codes.filter((c) => c !== x.dataset.rmc); drawStu(); load(); }));
  };
  const card = (x) => `<div class="wcard ${st.sel.has(x.key) ? "on" : ""} ${x.png ? "" : "nopng"}" data-key="${esc(x.key)}">
      <div class="row" style="gap:6px;flex-wrap:nowrap"><input type="checkbox" ${st.sel.has(x.key) ? "checked" : ""} ${x.png ? "" : "disabled"}>
        <span class="small" style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"><b>${esc(/^\d+$/.test(x.label) ? x.label + "번" : x.label)}</b> · ${esc(x.title)} <span class="code">${esc(x.code_fmt)}</span></span></div>
      ${x.png ? `<img loading="lazy" src="${fileUrl(x.png)}" alt="">` : `<div class="noimg">그림 없이 등록한 문항이라 출제에 못 넣어요</div>`}
      <div class="small sub">${x.answer ? `정답 <b>${esc(x.choice && CIRC[x.answer] ? CIRC[x.answer] : x.answer)}</b>` : x.answer_png ? "정답(그림)" : "정답 없음"}${x.tag ? ` · ${esc(x.tag)}` : ""}${x.rate ? ` · 정답률 ${esc(String(x.rate).replace("%", ""))}%` : ""}${x.question ? ` · <span title="전사본 있음">전사본 ✓</span>` : ""}</div>
      <div class="small" style="margin-top:4px">${x.students.map((s) => `<span class="tag ${s.final === "O" ? "o" : s.final === "X" ? "x" : "u"}" title="${esc(s.when)}">${esc(s.name)} ${esc(s.rounds.map((r) => r.round + "차 " + (RK[r.result] || r.result)).join(" → "))}</span>`).join(" ")}</div></div>`;
  const draw = () => {
    const n = st.items.filter((x) => st.sel.has(x.key)).length;
    $("#wHead").innerHTML = `문항 ${st.items.length}개 <span class="sub small">고른 ${n}개</span>`;
    $("#wList").innerHTML = st.items.map(card).join("") || `<div class="empty">${st.sids.size || st.codes.length ? "조건에 맞는 틀린 문항이 없어요" : "학생을 골라 주세요"}</div>`;
    $("#wMake").disabled = !n; $("#wJson").disabled = !n;
    $("#wMake").textContent = n ? `PDF로 출제 (${n}문항)` : "PDF로 출제";
    $$("#wList .wcard").forEach((el) => {
      const x = st.items.find((i) => i.key === el.dataset.key);
      el.onclick = (e) => {
        if (e.target.tagName === "IMG") return zoom(e.target.src);
        if (!x.png) return;
        st.sel.has(x.key) ? st.sel.delete(x.key) : st.sel.add(x.key);
        draw();
      };
    });
  };
  const load = async () => {
    if (!st.sids.size && !st.codes.length) { st.items = []; return draw(); }
    $("#wList").innerHTML = `<span class="busy"></span>찾는 중…`;
    try {
      const r = await api("wrongset/preview", { students: [...st.sids], codes: st.codes, from: $("#wFrom").value, to: $("#wTo").value, which: st.which, include_u: st.withU });
      st.items = r.items; st.filter = r.filter;
      st.sel = new Set(r.items.filter((x) => x.png).map((x) => x.key));
    } catch (e) { st.items = []; toast(e.message); }
    draw();
  };
  $("#wAll").onclick = () => { st.sel = new Set(st.items.filter((x) => x.png).map((x) => x.key)); draw(); };
  $("#wNone").onclick = () => { st.sel = new Set(); draw(); };
  $("#wMake").onclick = async () => {
    const items = st.items.filter((x) => st.sel.has(x.key) && x.png).map((x) => ({ code: x.code, seq: x.seq }));
    if (!items.length) return;
    const btn = $("#wMake"); btn.disabled = true;
    $("#wOut").innerHTML = `<div class="card" style="margin-top:12px"><span class="busy"></span>새 프린트를 짜는 중… (${items.length}문항)</div>`;
    try {
      const p = await api("wrongset/make", { items, title: $("#wTitle").value, sub: $("#wSub").value, template: st.tpl, targets: [...st.sids], which: st.which });
      $("#wOut").innerHTML = `<h2 style="margin-top:14px">만들었어요</h2>${printCard(p)}${p.skipped ? `<p class="sub small">그림이 없는 ${p.skipped}문항은 뺐어요.</p>` : ""}`;
      bindPrintCards($("#wOut"));
      toast(`오답 프린트 ${p.code_fmt} — ${p.n_items}문항`);
    } catch (e) { $("#wOut").innerHTML = ""; toast(e.message, 4000); }
    btn.disabled = false;
  };
  $("#wJson").onclick = () => {
    const sel = st.items.filter((x) => st.sel.has(x.key));
    const names = students.filter((s) => st.sids.has(s.id)).map((s) => s.name);
    const obj = { kind: "ashrain.wrongset", version: 1, made: new Date().toISOString(), students: names,
      filter: { ...(st.filter || {}), students: names, which: { final: "지금도 틀린 문항", ever: "한 번이라도 틀린 문항", repeat: "두 번 넘게 틀린 문항" }[st.which] },
      note: "문항 그림은 강사도구 프린트(code)의 같은 번호(no)에 있다. question/solution은 강사도구에 전사본이 있을 때만(mathir). rounds: 1차=처음 풀기, 2차·3차=다시 풀기.",
      items: sel.map((x) => ({ code: x.code_fmt, title: x.title, no: x.seq, label: x.label, choice: x.choice, answer: x.answer, answer_image: !!x.answer_png,
        points: x.points, topic: x.topic, tag: x.tag, rate: x.rate, key: x.key, question: x.question || null, solution: x.solution || null, n_wrong: x.n_wrong,
        students: x.students.map((s) => ({ name: s.name, final: s.final, rounds: s.rounds, answer: s.answer, when: s.when })) })) };
    const blob = new Blob([JSON.stringify(obj, null, 1)], { type: "application/json" });
    const el = document.createElement("a");
    el.href = URL.createObjectURL(blob);
    el.download = `오답_${names.join("·") || "학생"}_${today}.json`;
    document.body.appendChild(el); el.click();
    setTimeout(() => { URL.revokeObjectURL(el.href); el.remove(); }, 1500);
  };
  drawStu();
  await load();
}

/* ───────────────────────── 5. 프린트함 */
async function viewPrints() {
  const q = store.get("printQ", "");
  let trash = false;
  view.innerHTML = `<h1>프린트함</h1><div class="card"><div class="row"><input class="tin" id="pq" placeholder="제목·코드·파일 이름으로 찾기" value="${esc(q)}" style="flex:1">
    <a class="btn ghost" href="#/tt/register/lib">보관함</a><button class="btn ghost" id="pTrash">지운 프린트</button></div></div><div id="pl"></div>`;
  const loadTrash = async () => {
    const list = await api("prints?deleted=1");
    $("#pl").innerHTML = `<div class="card"><h2>지운 프린트 <span class="sub small">되살리면 프린트함에 다시 보여요. 완전히 지우면 채점 기록까지 모두 지워지고 코드가 비워져요.</span></h2>
      ${list.length ? `<table class="t"><tr><th>코드</th><th>제목</th><th>문항</th><th>대상</th><th>만든 때</th><th></th></tr>
      ${list.map((p) => `<tr><td class="code">${esc(p.code_fmt)}</td><td><b>${esc(p.title)}</b></td><td>${p.n_items}</td><td class="small">${p.targets.map((t) => esc(t.name)).join(", ") || "-"}</td>
        <td class="sub small">${shortWhen(p.created_at)}</td><td class="row" style="gap:4px;flex-wrap:nowrap"><button class="btn small" data-restore="${p.code}">되살리기</button><button class="btn small ghost warn-t" data-purge="${p.code}">완전히 지우기</button></td></tr>`).join("")}</table>`
      : `<div class="empty">지운 프린트가 없어요</div>`}</div>`;
    $$("[data-restore]").forEach((b) => (b.onclick = async () => { await api(`prints/${b.dataset.restore}/restore`, {}); toast("되살렸어요"); loadTrash(); }));
    $$("[data-purge]").forEach((b) => (b.onclick = async () => {
      const v = await modal(`<h2>완전히 지울까요? <span class="code sub">${esc(fmtCode(b.dataset.purge))}</span></h2><p>이 프린트의 채점 기록(모든 차·스캔본)·수업 기록·파일이 모두 지워지고 코드가 비워져요. <b>되돌릴 수 없어요.</b></p>`,
        [{ label: "그만두기", value: null, cls: "ghost" }, { label: "완전히 지우기", value: 1, cls: "warn" }]);
      if (!v) return;
      await api(`prints/${b.dataset.purge}/purge`, {}); toast("완전히 지웠어요"); loadTrash();
    }));
  };
  const load = async () => {
    if (trash) return loadTrash();
    const v = $("#pq").value.trim();
    store.set("printQ", v);
    const list = await api("prints" + (v ? "?q=" + encodeURIComponent(v) : ""));
    $("#pl").innerHTML = `<div class="card">${list.length ? `<table class="t"><tr><th>코드</th><th>제목</th><th>양식</th><th>문항</th><th>대상</th><th>정답</th><th>만든 때</th></tr>
      ${list.map((p) => `<tr class="click" data-href="#/tt/print/${p.code}"><td class="code">${esc(p.code_fmt)}</td><td><b>${esc(p.title)}</b><div class="small muted">${esc(p.sources.join(", "))}</div></td>
        <td class="small">${KIND_KO[p.kind] || esc(p.template)}·${esc(p.label)}</td><td>${p.n_items} <span class="small muted">(${p.pages}쪽)</span></td><td class="small">${p.targets.map((t) => esc(t.name)).join(", ") || "-"}</td>
        <td class="small">${p.n_answers ? `${p.n_answers}/${p.n_items}` : `<span class="muted">없음</span>`}</td><td class="sub small">${shortWhen(p.created_at)}</td></tr>`).join("")}</table>` : `<div class="empty">없어요</div>`}</div>`;
    bindRows($("#pl"));
  };
  let t = 0;
  $("#pq").oninput = () => { trash = false; $("#pTrash").classList.remove("on"); clearTimeout(t); t = setTimeout(load, 250); };
  $("#pTrash").onclick = () => { trash = !trash; $("#pTrash").classList.toggle("on", trash); $("#pTrash").textContent = trash ? "← 프린트함" : "지운 프린트"; load(); };
  await load();
}

/* 정답 줄 붙여넣기: "1) ③ 2) 4 3) 12cm" 또는 "3 4 12 ..." → 순서대로 */
function parseKeyText(txt, n) {
  const t = String(txt || "").replace(/\r/g, "");
  const tagged = [...t.matchAll(/(?:^|\s)(\d{1,3})\s*[).:번]\s*([^\n]*?)(?=\s+\d{1,3}\s*[).:번]|\n|$)/g)];
  if (tagged.length >= Math.min(3, n)) {
    const out = {};
    tagged.forEach((m) => { const k = +m[1]; if (k >= 1 && k <= n && m[2].trim()) out[k] = m[2].trim(); });
    return out;
  }
  const toks = t.split(/[\n,\t]+|\s+/).map((x) => x.trim()).filter(Boolean);
  const out = {};
  toks.slice(0, n).forEach((v, i) => (out[i + 1] = v));
  return out;
}

async function viewPrint(code) {
  const p = await api("prints/" + normCode(code));
  const bw = bookWhere(p);
  if (bw) { location.replace(bw); return; }
  const students = await api("students");
  const ans = Object.fromEntries(p.items.map((it) => [it.seq, it.answer || ""]));
  view.innerHTML = `<h1>${esc(p.title)}</h1>
    ${printCard(p)}
    <div class="card"><div class="row"><b>학교급</b><div id="pLevel"></div><span class="sub small">전사용 내보내기에서 가이드를 고를 때 써요</span>
      ${p.n_sols ? `<span class="tag" style="margin-left:auto">해설 그림 ${p.n_sols}문항</span>` : ""}</div>
      <div class="row" style="margin-top:10px"><b>받기</b><a class="btn ghost small" href="/dl/print/${p.code}.json" download title="번호·정답·유형·정답률·전사본(있으면)·학생들 결과 개수">문항 JSON</a>
        ${(p.extras || []).map((x) => `<a class="btn ghost small" href="${fileUrl(x.file)}" target="_blank" title="${esc(x.role)} · 보관함에서 같이 받은 파일">📎 ${esc(x.name)}</a>`).join("")}
        <span class="sub small">시험지·정답해설 PDF는 위 단추로 · JSON은 유사 문항을 만들 때 Claude에게 같이 주세요</span></div></div>
    <div class="grid2">
      <div class="card" style="margin:0"><h2>출제 대상</h2><div class="chips" id="tgs">${p.targets.map((t) => `<span class="chip">${esc(t.name)} <span class="small" style="opacity:.6">${day(t.issued_at).slice(5)}</span><button data-rm="${t.id}" title="빼기">×</button></span>`).join("") || `<span class="empty">없음</span>`}</div>
        <div id="addT" style="margin-top:8px"></div><button class="btn small" id="addTGo" style="margin-top:6px">대상 추가</button></div>
      <div class="card" style="margin:0"><div class="row" style="justify-content:space-between"><h2 style="margin:0">채점 기록</h2>
          ${p.gradings.some((g) => g.summary && (g.summary.X || g.summary.U)) ? `<a class="btn ghost small" href="#/tt/wrong/p/${p.code}" title="이 프린트를 푼 학생들의 틀린 문항을 모아 새 프린트로">오답 출제</a>` : ""}</div>
        ${p.gradings.length ? `<table class="t" style="margin-top:8px">${p.gradings.map((g) => `<tr class="click" data-href="#/tt/grade/${p.code}/${g.student_id}${g.status === "done" ? "/done" : ""}"><td style="white-space:nowrap"><b>${esc(g.name)}</b></td>
          <td>${statusTag(g.status)}${g.n_rounds > 1 ? ` <span class="tag ses">${g.n_rounds}차</span>` : ""}${gdLine(g.graded_days)}</td><td>${sumText(g.summary)}${roundNote(g)}</td><td class="sub small">${shortWhen(g.updated_at)}</td>
          <td><button class="btn small ghost" style="white-space:nowrap" data-scan="${g.id}" data-r="${g.n_rounds || 1}" data-t="${esc(p.title)}" data-n="${esc(g.name)}" title="학생이 푼 종이 스캔본 올리기 · 1차·2차 표시">${scanLabel({ length: g.n_scans || 0 })}</button></td></tr>`).join("")}</table>` : `<div class="empty">아직 없어요</div>`}</div>
    </div>
    <div class="card" style="margin-top:14px"><div class="row" style="justify-content:space-between"><h2 style="margin:0">정답 (빠른정답) <span class="sub small" id="nAns"></span></h2>
      <div class="row"><label class="btn ghost small" style="cursor:pointer">정답 PDF 첨부<input type="file" accept=".pdf" id="ansPdf" hidden></label>${p.answer_pages.length ? `<button class="btn ghost small" id="ansView">정답해설 보기</button>` : ""}<button class="btn" id="ansSave">정답 저장</button></div></div>
      <details ${p.n_answers ? "" : "open"}><summary>한꺼번에 붙여넣기</summary>
        <textarea class="tin" id="ansBulk" placeholder="예) 1) ③  2) 5  3) 12cm …  또는 그냥 순서대로: 3 5 12 …"></textarea>
        <div class="row" style="margin-top:6px"><button class="btn small ghost" id="ansFill">칸에 채우기</button><span class="sub small">채운 뒤 '정답 저장'을 눌러야 저장돼요</span></div></details>
      <div class="keygrid" id="kg" style="margin-top:10px"></div></div>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">문항 ${p.items.some((it) => splitLabel(it.label).part) ? `<span class="sub small">하위 문제로 나눈 문제 ${new Set(p.items.filter((it) => splitLabel(it.label).part).map((it) => splitLabel(it.label).base)).size}개 · 채점 칸 ${p.items.length}개</span>` : ""}</h2>
      <div class="row"><a class="btn small ghost" href="#/tt/parts/${p.code}" title="(1)·(2)·(3) 하위 문제가 있는 문제를 하위 문제마다 따로 채점">하위 문제 나누기</a><button class="btn small warn" id="pDel">프린트 지우기</button></div></div>
      <div class="wrongs" style="margin-top:10px">${p.items.map((it) => `<div class="wrong" style="border-color:var(--line)"><b>${esc(nob(it))}</b> <span class="small muted">${p.kind === "registered" ? "" : p.kind === "wrong" ? `← ${esc(it.src)} ${esc(/^\d+$/.test(String(it.src_no)) ? it.src_no + "번" : it.src_no)}` : `${esc(it.src)} ${esc(it.src_no)}번`}${it.choice ? " · 객관식" : ""}</span>${it.png ? `<img src="${fileUrl(p.code + "/" + it.png)}" alt="">` : ""}</div>`).join("")}</div></div>`;
  bindPrintCards(view);
  bindRows(view);
  bindScanButtons(view);
  seg($("#pLevel"), [["초등", "초등"], ["중등", "중등"], ["고등", "고등"]], p.level || "중등", async (v) => { await api("prints/" + p.code, { level: v }); toast("학교급: " + v); });
  const drawKeys = () => {
    $("#kg").innerHTML = p.items.map((it) => `<div class="keycell ${it.choice ? "ch" : ""}"><b title="${esc(nob(it))}">${esc(nolab(it).replace(/^(서답형|서술형|주관식|단답형)\s*/, "서"))}</b><input data-seq="${it.seq}" value="${esc(ans[it.seq])}" placeholder="${it.choice ? "1~5" : "답"}">${it.answer_png ? `<img class="kimg" src="${fileUrl(p.code + "/" + it.answer_png)}" alt="" title="빠른정답 그림">` : ""}
      ${it.choice ? `<span class="cbtns">${[1, 2, 3, 4, 5].map((n) => `<button data-c="${n}" data-seq="${it.seq}" style="${ans[it.seq] === String(n) ? "background:var(--acc);color:#fff" : ""}">${n}</button>`).join("")}</span>` : ""}</div>`).join("");
    $("#nAns").textContent = `${Object.values(ans).filter(Boolean).length}/${p.items.length} 입력`;
    $$("#kg input").forEach((i) => (i.oninput = () => { ans[i.dataset.seq] = i.value.trim(); $("#nAns").textContent = `${Object.values(ans).filter(Boolean).length}/${p.items.length} 입력`; }));
    $$("#kg [data-c]").forEach((b) => (b.onclick = () => { ans[b.dataset.seq] = b.dataset.c; drawKeys(); const nx = $(`#kg input[data-seq="${+b.dataset.seq + 1}"]`); if (nx) nx.focus(); }));
    $$("#kg input").forEach((i) => (i.onkeydown = (e) => { if (e.key === "Enter" && !e.isComposing) { const nx = $(`#kg input[data-seq="${+i.dataset.seq + 1}"]`); if (nx) nx.focus(); } }));
  };
  drawKeys();
  $("#ansFill").onclick = () => { const r = parseKeyText($("#ansBulk").value, p.items.length); Object.assign(ans, r); drawKeys(); toast(`${Object.keys(r).length}칸 채웠어요`); };
  $("#ansSave").onclick = async () => { await api("prints/" + p.code, { answers: ans }); toast("정답을 저장했어요"); };
  $("#ansPdf").onchange = async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    try { const u = await upload(f); const r = await api("prints/" + p.code, { answer_upload: u.id }); toast(r.quick ? `빠른정답에서 ${r.quick}문항의 정답을 채웠어요` : "정답 PDF를 붙였어요"); route(); } catch (err) { toast(err.message); }
  };
  if ($("#ansView")) $("#ansView").onclick = () => modal(`<h2>정답해설</h2><div class="ansimgs">${p.answer_pages.map((s) => `<img src="${fileUrl(s)}" alt="">`).join("")}</div>`);
  const addT = nameChips($("#addT"), students.filter((s) => !p.targets.some((t) => t.id === s.id)), []);
  $("#addTGo").onclick = async () => { const n = addT.get(); if (!n.length) return; await api("prints/" + p.code, { targets: n }); toast("대상을 넣었어요"); route(); };
  $$("[data-rm]").forEach((b) => (b.onclick = async () => { await api("prints/" + p.code, { remove_target: +b.dataset.rm }); route(); }));
  $$(".wrong img").forEach((im) => (im.onclick = () => zoom(im.src)));
  $("#pDel").onclick = async () => {
    const ng = p.gradings.length;
    const v = await modal(`<h2>이 프린트를 지울까요? <span class="code sub">${esc(p.code_fmt)}</span></h2>
      <p><b>프린트만 지우기</b> — 목록에서만 빠져요. 채점·수업 기록과 파일은 남고, 프린트함 「지운 프린트」에서 되살릴 수 있어요.</p>
      <p><b>기록까지 모두 지우기</b> — ${ng ? `채점 기록 ${ng}건(모든 차·스캔본), ` : ""}수업 기록, 파일이 모두 지워지고 코드도 비워져요(보관함에서 같은 코드로 다시 등록할 수 있어요). <b>되돌릴 수 없어요.</b></p>`,
      [{ label: "그만두기", value: null, cls: "ghost" }, { label: "프린트만 지우기", value: "soft", cls: "ghost" }, { label: "기록까지 모두 지우기", value: "purge", cls: "warn" }]);
    if (!v) return;
    if (v === "purge" && ng) {
      const v2 = await modal(`<h2>정말 모두 지울까요?</h2><p>${p.gradings.map((g) => esc(g.name)).join(", ")}의 채점 기록이 함께 지워져요.</p>`,
        [{ label: "그만두기", value: null, cls: "ghost" }, { label: "모두 지우기", value: 1, cls: "warn" }]);
      if (!v2) return;
    }
    try { await api("prints/" + p.code, { delete: true, purge: v === "purge" }); } catch (e) { return toast(e.message); }
    toast(v === "purge" ? "프린트와 기록을 모두 지웠어요" : "지웠어요 (프린트함 「지운 프린트」에서 되살릴 수 있어요)", 3500);
    location.hash = "#/tt/prints";
  };
}


/* ───────────────────────── 하위 문제 나누기 (#/tt/parts/코드) — (1)·(2)·(3) 하위 문제를 따로 채점 */
async function viewParts(code) {
  const d = await api(`prints/${normCode(code)}/parts`);
  const p = d.print;
  const G = d.groups;
  const NS = [["0", "나누지 않음"], ["2", "2개"], ["3", "3개"], ["4", "4개"], ["5", "5개"], ["6", "6개"]];
  const cur = new Map(G.map((g) => [g.seq, g.parts ? g.parts.length : 0]));
  const want = new Map(cur);
  const ans = new Map(G.map((g) => [g.seq, g.parts ? g.parts.map((x) => x.answer) : g.found_answers.slice()]));
  const ans0 = new Map([...ans].map(([k, v]) => [k, v.join("\u0001")]));
  const nFound = G.filter((g) => g.found && !g.parts).length;
  view.innerHTML = `<h1>하위 문제 나누기 <span class="code sub">${esc(p.code_fmt)}</span> <span class="sub small">${esc(p.title)}</span></h1>
    <div class="card"><p style="margin:0 0 6px">하위 문제 <b>(1) · (2) · (3)</b> 가 있는 문제는 하위 문제마다 따로 O · X를 매겨요. 시험지와 정답지는 그대로이고 채점 칸만 나눠요.</p>
      ${d.n_gradings ? `<p class="small" style="margin:0 0 6px;color:var(--warn)">이 프린트의 채점 기록 ${d.n_gradings}건: 나누는 문제에 이미 매긴 결과는 하위 문제마다 같은 결과로 옮겨 둬요. 틀린 문제는 채점 화면(다시 열기)에서 하위 문제별로 고쳐 주세요.</p>` : ""}
      <div class="row">${nFound ? `<button class="btn" id="pAuto">찾은 대로 고르기 — ${nFound}문제</button><span class="sub small">정답 「(1) … (2) …」 · 문제지 줄머리 (1) (2) 로 찾았어요</span>` : `<span class="sub small">저절로 찾은 하위 문제가 없어요 — 문제 그림을 보고 골라 주세요.</span>`}</div></div>
    <div class="card"><div class="plist" id="pList"></div></div>
    <div class="stickybar bottom"><div class="card row" style="margin:0;justify-content:space-between"><span id="pNote" class="sub"></span>
      <div class="row"><a class="btn ghost" href="#/tt/print/${p.code}">돌아가기</a><button class="btn" id="pSave">저장</button></div></div></div>`;
  const changed = () => G.filter((g) => want.get(g.seq) !== cur.get(g.seq) || (want.get(g.seq) >= 2 && ans.get(g.seq).slice(0, want.get(g.seq)).join("\u0001") !== (ans0.get(g.seq) || "")));
  const note = () => {
    const n = G.reduce((a, g) => a + Math.max(1, want.get(g.seq) || 0), 0);
    const c = changed().length;
    $("#pNote").textContent = `문제 ${G.length}개 → 채점 칸 ${n}개${c ? ` · 바꾼 문제 ${c}개` : ""}`;
    $("#pSave").disabled = !c;
  };
  const drawOne = (g) => {
    const box = $(`.pg[data-s="${g.seq}"]`);
    const n = want.get(g.seq) || 0;
    const a = ans.get(g.seq);
    $(".pans", box).innerHTML = n >= 2 ? Array.from({ length: n }, (_, k) => `<label class="small">${partLabel(k + 1)} <input class="tin" data-k="${k}" value="${esc(a[k] || "")}" placeholder="정답(없으면 비워 둠)"></label>`).join("") : "";
    $$(".pans input", box).forEach((inp) => (inp.oninput = () => { a[+inp.dataset.k] = inp.value; note(); }));
    box.classList.toggle("on", n >= 2);
  };
  $("#pList").innerHTML = G.map((g) => `<div class="pg" data-s="${g.seq}">
      <div class="pimg">${g.png ? `<img src="${fileUrl(p.code + "/" + g.png)}" alt="">` : `<div class="noimg">그림 없음</div>`}</div>
      <div class="pbody"><div class="row"><b>${esc(/^\d+$/.test(g.base) ? g.base + "번" : g.base)}</b>
        ${g.choice ? `<span class="tag">객관식 — 나누지 않음</span>` : ""}${g.parts ? `<span class="tag ses">지금 ${g.parts.length}개로 나뉨</span>` : ""}${g.found && !g.parts ? `<span class="tag u">찾음 ${g.found}개</span>` : ""}
        ${g.answer && !g.parts ? `<span class="small sub">정답 ${esc(g.answer)}</span>` : ""}</div>
        ${g.choice ? "" : `<div data-seg="${g.seq}" style="margin-top:6px"></div>`}<div class="pans"></div></div></div>`).join("");
  for (const g of G) {
    if (!g.choice) seg($(`[data-seg="${g.seq}"]`), NS, String(want.get(g.seq) || 0), (v) => { want.set(g.seq, Number(v)); drawOne(g); note(); });
    drawOne(g);
  }
  $$("#pList img").forEach((im) => (im.onclick = () => zoom(im.src)));
  if ($("#pAuto")) $("#pAuto").onclick = () => {
    for (const g of G) if (g.found && !g.parts) { want.set(g.seq, g.found); if (!ans.get(g.seq).length) ans.set(g.seq, g.found_answers.slice()); }
    for (const g of G) { if (!g.choice) seg($(`[data-seg="${g.seq}"]`), NS, String(want.get(g.seq) || 0), (v) => { want.set(g.seq, Number(v)); drawOne(g); note(); }); drawOne(g); }
    note();
    toast(`${nFound}문제를 찾은 대로 골랐어요 — 확인한 뒤 「저장」`);
  };
  $("#pSave").onclick = async () => {
    const ch = changed();
    if (!ch.length) return;
    const b = $("#pSave"); b.disabled = true;
    try {
      const r = await api(`prints/${p.code}/parts`, { plan: ch.map((g) => [g.seq, want.get(g.seq) >= 2 ? Array.from({ length: want.get(g.seq) }, (_, k) => ({ answer: ans.get(g.seq)[k] || "" })) : null]) });
      toast(`저장했어요 — 채점 칸 ${r.items}개${r.marks ? ` · 채점 기록 ${r.marks}개 옮김` : ""}`, 4000);
      location.hash = "#/tt/print/" + p.code;
    } catch (e) { toast(e.message, 6000); b.disabled = false; }
  };
  note();
}

/* ───────────────────────── 7. 내보내기 (전사용 Gemini · 분석용 Claude) */
async function viewExport() {
  const students = await api("students");
  const d30 = new Date(Date.now() - 30 * 864e5 - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  const st = { from: store.get("expFrom", d30), to: store.get("expTo", today), level: store.get("expLevel", ""), sel: new Set(), list: [] };
  view.innerHTML = `<h1>내보내기</h1>
    <div class="card"><div class="opt">
      <label class="k">기간</label><div class="row"><input type="date" class="tin" id="eFrom" value="${st.from}"><span>~</span><input type="date" class="tin" id="eTo" value="${st.to}"><span class="sub small">이 기간에 만든 프린트 (분석용은 이 기간에 채점한 기록)</span></div>
      <label class="k">학교급</label><div id="eLevel"></div>
    </div></div>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">프린트 <span class="sub small" id="eCnt"></span></h2>
      <div class="row"><button class="btn ghost small" id="eAll">모두 고르기</button><button class="btn ghost small" id="eNone">모두 빼기</button></div></div>
      <p class="sub small" style="margin:4px 0 8px">고르지 않으면 위 기간·학교급의 프린트 전체를 내보내요. 전사 상태: <span class="taskc all">문항+해설</span><span class="taskc sol">해설만</span><span class="taskc done">끝남</span></p>
      <div id="eList"></div></div>
    <div class="grid2">
      <div class="card" style="margin:0"><h2>전사용 <span class="sub small">Gemini</span></h2>
        <p class="sub small">문항 그림을 문항마다 한 쪽씩 모은 PDF와 <b>전사 가이드</b>를 한 묶음으로 만들어요. DB에 대조본이 없는 문항은 '문항+해설', DB에 문항이 있는데 해설이 없는 문항은 '해설만'으로 나눠 적어요.
        초등 문항은 대부분 '문항+해설'이에요. 매쓰플랫 해설 쪽이 있던 프린트는 그 해설 그림도 같이 넣어 옮겨 적게 해요.</p>
        <label class="small"><input type="checkbox" id="eDb" checked> DB와 대조하기 (로그인했을 때 · 매쓰플랫 유형명·정답률로 찾아요)</label><br>
        <label class="small"><input type="checkbox" id="eDone"> 이미 전사가 끝난 문항도 넣기</label>
        <div class="row" style="margin-top:10px"><button class="btn" id="eTr">전사용 내보내기</button></div>
        <div id="eTrOut"></div>
        <hr style="border:none;border-top:1px solid var(--line);margin:16px 0">
        <h3 style="margin:0 0 6px;font-size:15px">전사 결과 가져오기</h3>
        <p class="sub small" style="margin:0 0 8px">Gemini가 돌려준 <b>결과_…json</b>을 넣으면 수식 문법(mathir)을 검사해 통과한 것만 쌓고, 걸린 문항은 사유를 보여 줘요.</p>
        <label class="btn ghost" style="cursor:pointer">결과 JSON 고르기<input type="file" id="eImp" accept=".json,.txt,application/json" multiple hidden></label>
        <div id="eImpOut"></div></div>
      <div class="card" style="margin:0"><h2>분석용 <span class="sub small">Claude</span></h2>
        <p class="sub small">고른 프린트(없으면 위 기간에 채점한 것)의 <b>채점 결과·문항 그림·정답·학생 스캔본</b>과 분석 요청 가이드를 한 묶음으로 만들어요. 묶음을 Claude에게 올리면 풀이 과정과 오답까지 검토해 보고서를 만들어요.</p>
        <label class="k small">학생 (비우면 모두)</label><div id="eStu"></div>
        <div class="row" style="margin-top:10px"><button class="btn" id="eAn">분석용 내보내기</button></div>
        <div id="eAnOut"></div></div>
    </div>
    <p class="sub small" style="margin-top:14px">묶음(zip)은 이 브라우저에서 만들어 바로 받아요.</p>`;
  seg($("#eLevel"), [["", "전체"], ["초등", "초등"], ["중등", "중등"], ["고등", "고등"]], st.level, (v) => { st.level = v; store.set("expLevel", v); load(); });
  const stu = nameChips($("#eStu"), students, []);
  const draw = () => {
    $("#eCnt").textContent = `${st.list.length}개${st.sel.size ? ` · ${st.sel.size}개 고름` : ""}`;
    const tk = (t) => (t.all ? `<span class="taskc all">${t.all}</span>` : "") + (t.solution ? `<span class="taskc sol">${t.solution}</span>` : "") + (t.done ? `<span class="taskc done">${t.done}</span>` : "") + (t.db_item ? `<span class="taskc" title="애쉬레인 문항 key가 있는 프린트">DB ${t.db_item}</span>` : "");
    $("#eList").innerHTML = st.list.length ? `<table class="t exptbl"><tr><th></th><th>코드</th><th>제목</th><th>학교급</th><th>문항</th><th>전사 상태</th><th>채점</th><th>만든 때</th></tr>
      ${st.list.map((p) => `<tr class="click" data-c="${p.code}"><td><input type="checkbox" ${st.sel.has(p.code) ? "checked" : ""}></td><td class="code">${esc(p.code_fmt)}</td><td>${esc(p.title)}</td>
        <td class="small">${esc(p.level)}</td><td>${p.n_items}</td><td>${tk(p.tasks)}</td><td class="small">${p.n_gradings || "-"}${p.n_scans ? ` · 스캔 ${p.n_scans}` : ""}</td><td class="sub small">${shortWhen(p.created_at)}</td></tr>`).join("")}</table>` : `<div class="empty">이 기간에 만든 프린트가 없어요</div>`;
    $$("#eList tr[data-c]").forEach((tr) => (tr.onclick = (e) => { const c = tr.dataset.c; if (e.target.tagName !== "INPUT") $("input", tr).checked = !$("input", tr).checked; $("input", tr).checked ? st.sel.add(c) : st.sel.delete(c); $("#eCnt").textContent = `${st.list.length}개${st.sel.size ? ` · ${st.sel.size}개 고름` : ""}`; }));
  };
  const load = async () => {
    st.from = $("#eFrom").value; st.to = $("#eTo").value; store.set("expFrom", st.from); store.set("expTo", st.to);
    $("#eList").innerHTML = `<span class="busy"></span>불러오는 중…`;
    st.list = await api(`export/prints?from=${st.from}&to=${st.to}&level=${encodeURIComponent(st.level)}`);
    const have = new Set(st.list.map((p) => p.code));
    st.sel = new Set([...st.sel].filter((c) => have.has(c)));
    draw();
  };
  $("#eFrom").onchange = load; $("#eTo").onchange = load;
  $("#eAll").onclick = () => { st.list.forEach((p) => st.sel.add(p.code)); draw(); };
  $("#eNone").onclick = () => { st.sel.clear(); draw(); };
  const body = () => ({ codes: [...st.sel], from: st.from, to: st.to, level: st.level });
  const zips = new Map();
  const done = (r, extra) => { zips.set(r.zip_name, r.blob); return `<div class="card" style="margin:10px 0 0;background:#f0fdf4;border-color:#bbf7d0"><b>만들었어요</b> ${extra}
    <div class="sub small" style="word-break:break-all">${esc(r.zip_name)} · ${(r.blob.size / 1048576).toFixed(1)}MB</div>
    <div class="row" style="margin-top:6px"><button class="btn small" data-zip="${esc(r.zip_name)}">zip으로 받기</button></div></div>`; };
  const bindZip = (el) => $$("[data-zip]", el).forEach((b) => (b.onclick = () => {
    const a = document.createElement("a"); a.href = URL.createObjectURL(zips.get(b.dataset.zip)); a.download = b.dataset.zip; document.body.appendChild(a); a.click(); setTimeout(() => a.remove(), 1000);
  }));
  $("#eTr").onclick = async () => {
    const b = $("#eTr"); b.disabled = true; $("#eTrOut").innerHTML = `<p><span class="busy"></span>문항을 모으는 중…</p>`;
    try {
      const r = await api("export/transcribe", { ...body(), use_db: $("#eDb").checked, include_done: $("#eDone").checked });
      $("#eTrOut").innerHTML = done(r, `· ${r.n}문항 (문항+해설 ${r.n_all} · 해설만 ${r.n_sol}) · 묶음 ${esc(r.batch)}`) + (r.note ? `<p class="sub small">${esc(r.note)}</p>` : "") +
        `<p class="sub small">Gemini에 <b>00_먼저_읽기_전사가이드.md</b>와 <b>문항.pdf</b>(필요하면 목록.json·결과_양식.json·mathir.py)를 올리고 "가이드대로 해 줘"라고 하면 돼요.</p>`;
      bindZip($("#eTrOut"));
      load();
    } catch (e) { $("#eTrOut").innerHTML = `<p style="color:var(--x)">${esc(e.message)}</p>`; }
    b.disabled = false;
  };
  $("#eAn").onclick = async () => {
    const b = $("#eAn"); b.disabled = true; $("#eAnOut").innerHTML = `<p><span class="busy"></span>채점 기록과 스캔본을 모으는 중…</p>`;
    try {
      const names = stu.get();
      const ids = students.filter((x) => names.includes(x.name)).map((x) => x.id);
      const r = await api("export/analysis", { ...body(), student_ids: ids });
      $("#eAnOut").innerHTML = done(r, `· 채점 ${r.n_gradings}건 · 학생 ${r.n_students}명 · 프린트 ${r.n_prints}개 · 스캔본 ${r.n_scans}개`) +
        `<p class="sub small">Claude에게 zip(또는 폴더 안 파일들)을 올리고 "00_분석요청_가이드대로 분석해 줘"라고 하면 돼요.</p>`;
      bindZip($("#eAnOut"));
    } catch (e) { $("#eAnOut").innerHTML = `<p style="color:var(--x)">${esc(e.message)}</p>`; }
    b.disabled = false;
  };
  $("#eImp").onchange = async (e) => {
    const out = $("#eImpOut"); out.innerHTML = "";
    for (const f of e.target.files) {
      try {
        const d = await api("export/import", { name: f.name, text: await f.text() });
        out.innerHTML += `<div class="card" style="margin:10px 0 0"><b>${esc(f.name)}</b> · 통과 ${d.ok} · review ${d.review} · 걸림 ${d.bad.length}
          ${d.bad.length ? `<table class="t" style="margin-top:6px">${d.bad.slice(0, 40).map((x) => `<tr><td class="code">${esc(x.id)}</td><td class="small">${esc(x.why)}</td></tr>`).join("")}</table>` : ""}</div>`;
      } catch (err) { out.innerHTML += `<p style="color:var(--x)">${esc(f.name)}: ${esc(err.message)}</p>`; }
    }
    e.target.value = "";
    load();
  };
  await load();
}

async function viewAccount() { location.hash = "#/tt/grade"; }

/* ───────────────────────── 공유받은 스캔본 (#/tt/inbox) — vFlat 등에서 「공유 → 강사도구」 (안드로이드에서 앱으로 설치했을 때) */
async function refreshInboxTab() {
  const a = $("#tt-inboxTab");
  if (!a) return;
  const n = await S.inboxCount();
  a.hidden = !n;
  a.textContent = `받은 스캔본 ${n}`;
}
const ago = (t) => { const m = Math.round((Date.now() - t) / 60000); return m < 1 ? "방금" : m < 60 ? `${m}분 전` : m < 1440 ? `${Math.round(m / 60)}시간 전` : `${Math.round(m / 1440)}일 전`; };
const shareHowto = () => `<div class="card"><h2>vFlat에서 바로 올리기 <span class="sub small">갤럭시탭 · 안드로이드</span></h2>
  <ol class="small" style="margin:0;padding-left:20px;line-height:1.9">
    <li>Chrome에서 강사도구를 연 채로 메뉴 ⋮ → <b>「앱 설치」</b>(또는 「홈 화면에 추가」) — 처음 한 번만${S.isStandalone() ? ` <span class="tag done">이 창은 앱</span>` : S.canPromptInstall() ? ` <button class="btn ghost small" id="ibInstall">지금 설치</button>` : ""}</li>
    <li>학생 기록 · 프린트 채점 기록 · 채점 결과에서 <b>스캔본 올리기</b> → 언제 스캔한 것인지 고르고 → <b>「vFlat으로 스캔」</b></li>
    <li>vFlat에서 스캔한 뒤 <b>공유 → 강사도구</b> → 그 채점에 「프린트 제목_학생_1차.pdf」로 저절로 올라가요</li>
  </ol>
  <p class="sub small" style="margin:8px 0 0">「vFlat으로 스캔」을 누르지 않고 vFlat에서 바로 공유해도 돼요 — 여기서 어느 채점인지 골라 올려요.</p></div>`;
const bindInstall = () => { if ($("#ibInstall")) $("#ibInstall").onclick = async () => { toast((await S.promptInstall()) ? "앱으로 설치했어요" : "설치하지 않았어요"); route(); }; };
async function viewInbox() {
  const files = await S.inboxList();
  if (!files.length) {
    view.innerHTML = `<h1>공유받은 스캔본</h1><div class="card"><div class="empty">받은 파일이 없어요</div></div>${shareHowto()}`;
    bindInstall();
    return;
  }
  const wait = S.getScanWait();
  return wait ? inboxUpload(files, wait) : inboxPick(files);
}
// 받은 파일을 채점 하나에 올림 — 이름은 「프린트 제목_학생_1차.pdf」, 올린 것은 받은 목록에서 지움
async function inboxUpload(files, target) {
  S.clearScanWait();          // 한 번 쓰면 지움 — 다음 공유는 다시 묻는다(다른 학생 것이 잘못 들어가지 않게)
  let d;
  try { d = await api("gradings/" + target.gid); } catch (e) { toast(e.message, 5000); return inboxPick(files); }
  const rd = target.round ?? null;
  const bw = bookWhere(d.print);
  const head = `${esc(d.student.name)} · ${esc(d.print.title)} ${bw ? `<span class="tag">교재</span>` : `<span class="code sub">${esc(d.print.code_fmt)}</span>`} · ${esc(whenText(rd))}`;
  const taken = new Set((d.scans || []).map((x) => x.name));
  const done = [], fail = [];
  for (let i = 0; i < files.length; i++) {
    view.innerHTML = `<h1>공유받은 스캔본</h1><div class="card"><span class="busy"></span>${head}에 올리는 중… (${i + 1}/${files.length})</div>`;
    const f = files[i];
    const name = S.sharedName({ title: d.print.title, student: d.student.name, round: rd }, f, taken);
    try {
      await uploadScan(target.gid, new File([f.blob], name, { type: f.type || f.blob.type || "" }), rd);
      await S.inboxDelete([f.id]);
      done.push(name);
    } catch (e) { fail.push(`${f.name}: ${e.message}`); }
  }
  store.set("shareLast", { gid: target.gid, round: rd });
  refreshInboxTab();
  view.innerHTML = `<h1>공유받은 스캔본</h1>
    <div class="card" style="${done.length ? "background:#f0fdf4;border-color:#bbf7d0" : ""}"><h2>${done.length ? `올렸어요 — ${head}` : "올리지 못했어요"}</h2>
      ${done.length ? `<div class="files">${done.map((n) => `<div class="file">${/\.pdf$/i.test(n) ? "📄" : "🖼"} ${esc(n)}</div>`).join("")}</div>` : ""}
      ${fail.length ? `<p class="small" style="color:var(--x)">${fail.map(esc).join("<br>")}</p>` : ""}
      <div class="row" style="margin-top:10px">${bw ? `<a class="btn" href="${bw}">이 교재의 스캔본 보기</a>` : `<a class="btn" href="#/tt/grade/${d.print.code}/${d.student.id}/done">이 채점의 스캔본 보기</a>`}
        ${fail.length ? `<button class="btn ghost" id="ibAgain">남은 것 다시</button>` : ""}${bw ? `<a class="btn ghost" href="#/tt/books">교재로</a>` : `<a class="btn ghost" href="#/tt/grade">채점으로</a>`}</div></div>`;
  if ($("#ibAgain")) $("#ibAgain").onclick = () => route();
}
// 기다리는 채점이 없을 때: 어느 채점 · 몇 차인지 골라 올림
async function inboxPick(files) {
  const gs = await api("gradings");
  const last = store.get("shareLast", null);
  let sel = last && gs.some((g) => g.id === last.gid) ? last.gid : null, pick = "";
  const total = files.reduce((a, f) => a + (f.size || 0), 0);
  view.innerHTML = `<h1>공유받은 스캔본</h1>
    <div class="card"><div class="row" style="justify-content:space-between"><h2 style="margin:0">받은 파일 ${files.length}개 <span class="sub small">${(total / 1048576).toFixed(1)}MB</span></h2>
        <button class="btn ghost small warn-t" id="ibDrop" title="올리지 않고 버리기">버리기</button></div>
      <div class="files">${files.map((f) => `<div class="file">${/pdf/.test(f.type) || /\.pdf$/i.test(f.name) ? "📄" : "🖼"} ${esc(f.name)} <span class="muted small">${(f.size / 1048576).toFixed(1)}MB · ${ago(f.at)}</span></div>`).join("")}</div></div>
    <div class="card"><h2>어느 채점에 올릴까요? <span class="sub small">이름은 「프린트 제목_학생_1차.pdf」처럼 붙여요</span></h2>
      <input class="tin" id="ibQ" placeholder="학생 이름 · 프린트 제목 · 코드로 찾기" style="width:100%;max-width:420px" autocomplete="off">
      <div id="ibList" style="margin-top:8px;max-height:46vh;overflow:auto"></div>
      <div class="scanwhen" style="margin-top:12px"><b>언제 스캔한 것인가요?</b><span id="ibSeg"></span></div>
      <div class="row"><button class="btn" id="ibGo" disabled>올리기</button><span class="sub small" id="ibNote"></span></div></div>`;
  const upd = () => {
    $("#ibGo").disabled = !(sel && pick);
    $("#ibNote").textContent = !sel ? "채점을 골라 주세요" : !pick ? "언제 스캔한 것인지 골라 주세요" : "";
  };
  const drawSeg = () => {
    const g = gs.find((x) => x.id === sel);
    const n = g && g.book ? BOOK_R : Math.max(2, (g && g.n_rounds) || 1);
    seg($("#ibSeg"), [...Array.from({ length: n }, (_, i) => [String(i + 1), whenText(i + 1)]), ["u", "확실하지 않음"]], pick, (v) => { pick = v; upd(); });
    upd();
  };
  const drawList = () => {
    const q = $("#ibQ").value.trim().toLowerCase().replace(/-/g, "");
    const rows = gs.filter((g) => !q || `${g.name} ${g.title} ${g.code}`.toLowerCase().replace(/-/g, "").includes(q));
    $("#ibList").innerHTML = rows.length ? `<table class="t">${rows.slice(0, 60).map((g) => `<tr class="click${g.id === sel ? " sel" : ""}" data-g="${g.id}">
      <td style="width:28px"><input type="radio" name="ibg" ${g.id === sel ? "checked" : ""}></td><td><b>${esc(g.name)}</b></td><td>${esc(g.title)}</td><td class="code">${g.book ? "" : esc(g.code_fmt)}</td>
      <td>${g.book ? `<span class="tag">교재</span>` : `${statusTag(g.status)}${g.n_rounds > 1 ? ` <span class="tag ses">${g.n_rounds}차</span>` : ""}`}</td><td class="sub small">${shortWhen(g.updated_at)}</td></tr>`).join("")}</table>`
      : `<div class="empty">맞는 채점이 없어요</div>`;
    $$("#ibList tr[data-g]").forEach((tr) => (tr.onclick = () => { sel = +tr.dataset.g; drawList(); drawSeg(); }));
  };
  $("#ibQ").oninput = drawList;
  $("#ibGo").onclick = () => inboxUpload(files, { gid: sel, round: pick === "u" ? null : Number(pick) });
  $("#ibDrop").onclick = async (e) => {
    if (!confirmInline(e.currentTarget)) return;
    await S.inboxDelete(files.map((f) => f.id));
    toast("받은 파일을 버렸어요");
    route();
  };
  drawList(); drawSeg();
}

const EV = {
  convert: "변환", register: "프린트 등록", student_add: "학생 추가", student_edit: "학생 수정", grading_start: "채점 시작", grading_resume: "채점 이어서",
  grading_close: "채점 닫음", answers_edit: "정답 입력", answer_attach: "정답 PDF 첨부", targets_add: "대상 추가", print_delete: "프린트 지움",
  class_used: "수업 사용", class_graded: "채점 기록", class_reviewed: "오답 풀이", class_homework: "숙제",
  print_out: "출력", scan_add: "스캔본 올림", scan_upload: "스캔본 올림", scan_round: "스캔본 차수 바꿈", scan_delete: "스캔본 지움", export_transcribe: "전사용 내보내기", export_analysis: "분석용 내보내기",
  import_transcripts: "전사 결과 가져옴", anon_backfill: "예전 프린트 이름 지움", cloud_conflict: "기록 충돌 보관",
  grading_reopen: "채점 다시 엶", retry_start: "다음 차 채점 시작", round_delete: "마지막 차 지움", grading_delete: "채점 기록 지움",
  print_purge: "프린트 완전히 지움", print_restore: "프린트 되살림", wrongset_make: "오답 프린트 만듦", library_register: "보관함에서 등록",
  library_import: "보관함에 옮겨 옴", pc_import: "PC 자료 옮겨 옴",
  book_add: "교재 등록", book_edit: "교재 고침", book_assign: "교재 붙임", book_unassign: "교재 뺌", book_delete: "교재 지움", book_log: "교재 기록",
};
function evDetail(e) {
  const d = e.detail || {};
  switch (e.kind) {
    case "register": return `${d.items}문항 · ${{ manifest: "등록 정보", auto: "자동 분할", pages: "쪽 단위" }[d.mode === "pages" ? "pages" : d.method] || ""} · 정답 ${d.answers}${d.targets && d.targets.length ? " · 대상 " + d.targets.map(esc).join(", ") : ""}`;
    case "convert": return `${d.items}문항 · ${d.pages}쪽 · ${esc(d.template)}${d.targets && d.targets.length ? " · 대상 " + d.targets.map(esc).join(", ") : ""}`;
    case "grading_close": return `${{ done: "다 채점", unsolved: "아이가 덜 풂", ungraded: "채점 덜 함" }[d.reason] || ""} · ${d.session}회차 · O ${d.O} / X ${d.X} / 안 풂 ${d.U}${d.none ? " / 남음 " + d.none : ""}`;
    case "grading_resume": return `이전 상태: ${(STATUS[d.was] || [d.was])[0]}`;
    case "answers_edit": return `${d.n}칸`;
    case "scan_upload": case "scan_round": case "scan_delete":
      return [esc(d.name || ""), "round" in d ? esc(whenText(d.round)) : "", d.pages ? `${d.pages}쪽` : ""].filter(Boolean).join(" · ");
    case "grading_start": case "student_add": return "";
    case "book_add": case "book_edit": case "book_assign": case "book_unassign": case "book_delete": return esc(d.title || "");
    case "book_log": {
      const one = (x) => (!x ? "없음" : x.kind === "solved" ? `${x.pages ? x.pages + "쪽 · " : ""}${x.page_to}쪽까지` : x.kind === "graded" ? `${x.round ? x.round + "차 " : ""}${x.pages ? x.pages + "쪽" : "쪽 안 적음"}` : `${md(x.day)} 줌`);
      const k = { solved: "진도", graded: "채점한 날", solution: "해설지" }[d.kind] || d.kind;
      const day0 = (d.after || d.before || {}).day;
      const what = !d.before ? `적음: ${one(d.after)}` : !d.after ? `지움: ${one(d.before)}` : `${one(d.before)} → ${one(d.after)}`;
      return `${d.undo_of ? "<b>되돌림</b> · " : ""}${esc(d.title || "")} · ${esc(k)}${d.kind !== "solution" && day0 ? " " + md(day0) : ""} · ${esc(what)}${d.note ? "" : ""}`;
    }
    default:
      if (e.kind.startsWith("class_")) return `${d.date} · ${d.prints ? d.prints.length : 0}개${d.edited ? " (수정)" : ""}`;
      return Object.entries(d).map(([k, v]) => `${esc(k)}: ${esc(typeof v === "object" ? JSON.stringify(v) : v)}`).join(" · ");
  }
}
async function viewLog() {
  const ev = await api("events?limit=1000");
  let f = store.get("logFilter", "all");
  const groups = { all: "전체", convert: "변환·등록", grading: "채점", class: "수업 기록", book: "교재", etc: "기타" };
  const grp = (k) => (k === "convert" || k === "register" ? "convert" : k.startsWith("grading") ? "grading" : k.startsWith("class") ? "class" : k.startsWith("book") ? "book" : "etc");
  const week = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10);
  const recent = ev.filter((e) => day(e.at) >= week);
  const cnt = (pred) => recent.filter(pred).length;
  view.innerHTML = `<h1>업무 기록</h1>
    <div class="card"><h2>최근 7일</h2><div class="gsum">
      <span class="n">변환 ${cnt((e) => e.kind === "convert")}</span>
      <span class="n">등록 ${cnt((e) => e.kind === "register")}</span>
      <span class="n">채점 완료 ${cnt((e) => e.kind === "grading_close" && e.detail.reason === "done")}</span>
      <span class="n">덜 풂 ${cnt((e) => e.kind === "grading_close" && e.detail.reason === "unsolved")}</span>
      <span class="n">수업 기록 ${new Set(recent.filter((e) => e.kind.startsWith("class_")).map((e) => e.student_id + ":" + e.detail.date)).size}</span>
      <span class="n">학생 ${new Set(recent.filter((e) => e.student_id).map((e) => e.student_id)).size}명</span></div>
      <p class="sub small" style="margin-bottom:0">입력 · 활동이 모두 여기에 남아요. 잘못 넣은 교재 기록은 줄 끝 「되돌리기」로 되돌려요(그 뒤에 또 바뀌었으면 교재 화면에서 고쳐 주세요).</p></div>
    <div class="card"><div id="lf"></div><div id="lt" style="margin-top:10px"></div></div>`;
  const draw = () => {
    const list = ev.filter((e) => f === "all" || grp(e.kind) === f).slice(0, 400);
    $("#lt").innerHTML = list.length ? `<table class="t"><tr><th>때</th><th>무엇</th><th>학생</th><th>프린트</th><th>내용</th><th></th></tr>${list.map((e) => `<tr${e.detail && e.detail.undone_by ? ` style="opacity:.55"` : ""}>
      <td class="sub small" style="white-space:nowrap">${shortWhen(e.at)}</td><td><b>${esc(EV[e.kind] || e.kind)}</b></td><td>${esc(e.student || "")}</td>
      <td class="small">${e.code ? `<a href="#/tt/print/${e.code}">${esc(e.title || "")}</a>` : ""}</td><td class="small sub">${evDetail(e)}</td>
      <td>${e.detail && e.detail.table ? (e.detail.undone_by ? `<span class="tag">되돌림</span>` : `<button class="btn ghost small nowrap" data-undo="${e.id}" title="이 입력 전으로 되돌려요">되돌리기</button>`) : ""}</td></tr>`).join("")}</table>` : `<div class="empty">없어요</div>`;
    $$("[data-undo]", $("#lt")).forEach((b) => (b.onclick = async () => {
      b.disabled = true;
      try { await api("undo", { events: [+b.dataset.undo] }); toast("되돌렸어요"); route(); } catch (e) { toast(e.message, 6000); b.disabled = false; }
    }));
  };
  seg($("#lf"), Object.entries(groups), f, (v) => { f = v; store.set("logFilter", v); draw(); });
  draw();
}

route();
// PC 강사도구 자료 폴더를 기억해 두었으면(옮겨 오기), 열 때 · 창으로 돌아올 때 PC에서 새로 등록한 것을 더한다
const pcAuto = () => { pcAutoSync({ view, toast, esc }).catch(() => {}); };
const onVis = () => { if (document.visibilityState === "visible") pcAuto(); };
pcAuto();
document.addEventListener("visibilitychange", onVis);
S.registerShareWorker();
const onVisInbox = () => { if (document.visibilityState === "visible") refreshInboxTab(); };
document.addEventListener("visibilitychange", onVisInbox);
return () => {
  document.removeEventListener("visibilitychange", onVis);
  document.removeEventListener("visibilitychange", onVisInbox);
  window.removeEventListener("hashchange", onHash);
  window.removeEventListener("beforeunload", onUnload);
  document.onkeydown = null;
  mo.disconnect();
  if (leaveGuard && leaveGuard.silent) leaveGuard.silent().catch(() => {});
};
}
