// 시록고 강사도구 — Supabase 연결(표 tt_* · 저장 공간 teacher-tool/<uid>/tt/…)
// 표는 RLS로 「본인 것만」이라 여기서 owner를 따로 거르지 않는다(넣을 때는 기본값 auth.uid()).
import { supabase } from "../../../supabaseClient";

export const BUCKET = "teacher-tool";
let _uid = null;

export async function uid() {
  if (_uid) return _uid;
  const { data } = await supabase.auth.getSession();
  _uid = data?.session?.user?.id || null;
  if (!_uid) throw new Error("로그인이 필요해요");
  return _uid;
}
supabase.auth.onAuthStateChange?.(() => { _uid = null; });

export const T = (name) => supabase.from(name);

export function must(res, what = "") {
  if (res.error) {
    const m = res.error.message || String(res.error);
    throw new Error(what ? `${what}: ${m}` : m);
  }
  return res.data;
}

// 1000행 넘게 읽기 (PostgREST 한 번에 최대 1000)
export async function all(build, page = 1000) {
  const out = [];
  for (let from = 0; ; from += page) {
    const rows = must(await build().range(from, from + page - 1));
    out.push(...rows);
    if (rows.length < page) return out;
  }
}

export async function rpc(fn, args) {
  return must(await supabase.rpc(fn, args));
}

// ── 저장 공간: rel = "<코드>/sheet.pdf" 처럼 tt 폴더 안 상대 경로
export async function fullPath(rel) {
  return `${await uid()}/tt/${String(rel).replace(/^\/+/, "")}`;
}

export async function put(rel, body, contentType = "application/octet-stream", upsert = true) {
  const p = await fullPath(rel);
  const { error } = await supabase.storage.from(BUCKET).upload(p, body, { contentType, upsert, cacheControl: "3600" });
  if (error) throw new Error(`올리기 실패 (${rel}): ${error.message}`);
  return rel;
}

export async function get(rel) {
  const p = await fullPath(rel);
  const { data, error } = await supabase.storage.from(BUCKET).download(p);
  if (error) throw new Error(`받기 실패 (${rel}): ${error.message || error}`);
  return data; // Blob
}

export async function bytes(rel) {
  return new Uint8Array(await (await get(rel)).arrayBuffer());
}

const signCache = new Map(); // rel → {url, exp}
export async function sign(rels, ttl = 3600) {
  const now = Date.now();
  const need = [...new Set(rels.filter((r) => r && !(signCache.get(r)?.exp > now + 60000)))];
  for (let i = 0; i < need.length; i += 200) {
    const part = need.slice(i, i + 200);
    const full = await Promise.all(part.map(fullPath));
    const { data, error } = await supabase.storage.from(BUCKET).createSignedUrls(full, ttl);
    if (error) throw new Error("파일 주소를 만들지 못했어요: " + error.message);
    (data || []).forEach((d, k) => { if (d?.signedUrl) signCache.set(part[k], { url: d.signedUrl, exp: now + ttl * 1000 }); });
  }
  const out = {};
  for (const r of rels) if (signCache.get(r)) out[r] = signCache.get(r).url;
  return out;
}

export async function remove(rels) {
  const list = [...new Set(rels.filter(Boolean))];
  for (let i = 0; i < list.length; i += 100) {
    const full = await Promise.all(list.slice(i, i + 100).map(fullPath));
    await supabase.storage.from(BUCKET).remove(full);
  }
  list.forEach((r) => signCache.delete(r));
}

// 폴더째 지우기 (rel 머리 아래 전부)
export async function removePrefix(prefix) {
  const base = await fullPath(prefix.replace(/\/+$/, ""));
  const walk = async (dir) => {
    const out = [];
    for (let off = 0; ; off += 1000) {
      const { data, error } = await supabase.storage.from(BUCKET).list(dir, { limit: 1000, offset: off });
      if (error || !data) break;
      for (const x of data) {
        if (x.id === null || x.metadata == null) out.push(...(await walk(`${dir}/${x.name}`)));
        else out.push(`${dir}/${x.name}`);
      }
      if (data.length < 1000) break;
    }
    return out;
  };
  const files = await walk(base);
  for (let i = 0; i < files.length; i += 100) await supabase.storage.from(BUCKET).remove(files.slice(i, i + 100));
}

export async function log(kind, studentId = null, printId = null, detail = {}) {
  try {
    await supabase.rpc("tt_log", { p_kind: kind, p_student: studentId, p_print: printId, p_detail: detail });
  } catch { /* 로그는 실패해도 됨 */ }
}

// 표에 넣기 전 빈 값 채우기 — NOT NULL 열에 null 이 가면 막히므로 기본값으로 (여러 줄을 한 번에 넣을 때 빠진 열은 null 이 되므로 있는 열만 채움)
const DEF = {
  tt_students: { grade: "", memo: "", active: true },
  tt_prints: { title: "", sub: "", kind: "registered", template: "", label: "서답형", level: "", n_items: 0, n_choice: 0, pages: 0, sources: [], files: {}, name_boxes: [], options: {}, shelf: "active" },
  tt_print_items: { label: "", src: "", src_no: "", choice: false, answer: "", topic: "", tag: "", rate: "" },
  tt_gradings: { status: "open", mode: "ox" },
  tt_sessions: { round: 1, kind: "solve" },
  tt_marks: { answer: "" },
  tt_scans: { name: "", size: 0, mime: "", deleted: false },
  tt_events: { detail: {} },
};
const NOW_COLS = new Set(["created_at", "updated_at", "issued_at", "started_at", "at"]);
export function nn(table, rows) {
  const d = DEF[table] || {};
  const now = new Date().toISOString();
  const fix = (r) => {
    const o = { ...r };
    for (const k of Object.keys(o)) {
      if (o[k] !== null && o[k] !== undefined) continue;
      if (k in d) o[k] = d[k];
      else if (NOW_COLS.has(k)) o[k] = now;
    }
    return o;
  };
  return Array.isArray(rows) ? rows.map(fix) : fix(rows);
}
