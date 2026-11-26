// 시록고 강사도구 — 「vFlat으로 스캔」 → vFlat에서 「공유 → 강사도구」로 받은 스캔본 (안드로이드에서 앱으로 설치했을 때)
// public/tt.webmanifest 의 share_target 으로 다른 앱의 공유 목록에 「강사도구」가 생기고,
// public/tt-sw.js 가 POST /seirocco/tt-share 로 온 파일을 IndexedDB tt-share/inbox 에 두고 #/tt/inbox 를 연다.
// 「vFlat으로 스캔」을 누를 때 어느 채점 · 몇 차인지 적어 두었다가(scanWait) 받은 파일을 그 채점에 프린트 이름으로 올린다.
const DB = "tt-share", STORE = "inbox", WAIT = "tt:scanWait";
export const VFLAT_PKG = "com.voyagerx.scanner";
const PLAY = `https://play.google.com/store/apps/details?id=${VFLAT_PKG}`;

function idb() {
  return new Promise((ok, no) => {
    const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(STORE, { keyPath: "id", autoIncrement: true });
    r.onsuccess = () => ok(r.result);
    r.onerror = () => no(r.error);
  });
}
async function tx(mode, fn) {
  const db = await idb();
  return new Promise((ok, no) => {
    const t = db.transaction(STORE, mode);
    const out = fn(t.objectStore(STORE));
    t.oncomplete = () => { db.close(); ok(out && "result" in out ? out.result : out); };
    t.onerror = () => { db.close(); no(t.error); };
  });
}
// 받은 파일 [{id, at, name, type, size, blob}]
export async function inboxList() {
  try { return (await tx("readonly", (s) => s.getAll())) || []; } catch { return []; }
}
export async function inboxDelete(ids) {
  if (!ids.length) return;
  await tx("readwrite", (s) => { ids.forEach((id) => s.delete(id)); });
}
export async function inboxCount() { return (await inboxList()).length; }

// 어느 채점 · 몇 차를 기다리는지 (같은 브라우저의 앱 창과 탭이 같이 봄) — 2시간 지나면 묻는다
export function setScanWait(w) {
  try { localStorage.setItem(WAIT, JSON.stringify({ ...w, at: Date.now() })); } catch { /* */ }
}
export function getScanWait(maxAgeMs = 2 * 3600e3) {
  try {
    const w = JSON.parse(localStorage.getItem(WAIT) || "null");
    return w && w.gid && Date.now() - w.at < maxAgeMs ? w : null;
  } catch { return null; }
}
export function clearScanWait() { try { localStorage.removeItem(WAIT); } catch { /* */ } }

// 안드로이드인지 (갤럭시탭 Chrome 은 「데스크톱 사이트」가 기본이라 UA에 Android 가 없을 수 있음)
export function isAndroid() {
  const ua = navigator.userAgent || "";
  if (/Android/i.test(ua)) return true;
  if (navigator.userAgentData && /Android/i.test(navigator.userAgentData.platform || "")) return true;
  return /Linux/i.test(navigator.platform || "") && !/CrOS/i.test(ua) && (navigator.maxTouchPoints || 0) > 1;
}
export const isStandalone = () => { try { return matchMedia("(display-mode: standalone)").matches; } catch { return false; } };

// vFlat 열기: 웹 페이지는 「브라우저에서 열 수 있다」고 밝힌 화면만 열 수 있어서, Play 스토어의 「앱 열기」 주소로 연다.
// (설치돼 있으면 vFlat이 열리고, 안 되면 Play 스토어의 vFlat 쪽 — 「열기」 단추)
export const vflatHref = () =>
  `intent://launch?id=${VFLAT_PKG}#Intent;scheme=market;package=com.android.vending;S.browser_fallback_url=${encodeURIComponent(PLAY)};end`;

// 앱으로 설치 (Chrome 이 설치할 수 있다고 알려 줄 때만 — index.html 이 미리 받아 둠)
export const canPromptInstall = () => !!window.__ttInstallPrompt;
export async function promptInstall() {
  const p = window.__ttInstallPrompt;
  if (!p) return false;
  window.__ttInstallPrompt = null;
  try { p.prompt(); const r = await p.userChoice; return r && r.outcome === "accepted"; } catch { return false; }
}

// 받는 일꾼(서비스 워커) — 시록고 안에서만, 캐시는 하지 않음. 앱 설치 정보(manifest)도 없으면 붙인다(다른 앱에서 넘어온 경우)
export function registerShareWorker() {
  try {
    if (!/^\/seirocco/.test(location.pathname)) return;
    if (!document.querySelector('link[rel="manifest"]')) {
      const l = document.createElement("link"); l.rel = "manifest"; l.href = "/tt.webmanifest"; document.head.appendChild(l);
      window.addEventListener("beforeinstallprompt", (e) => { e.preventDefault(); window.__ttInstallPrompt = e; });
    }
    if ("serviceWorker" in navigator) navigator.serviceWorker.register("/tt-sw.js", { scope: "/seirocco" }).catch(() => {});
  } catch { /* */ }
}

// 공유로 받은 파일 이름 → 「프린트 제목_학생_1차.pdf」 (같은 이름이 있으면 _2, _3)
export function sharedName({ title, student, round }, file, taken = new Set()) {
  const clean = (s) => String(s || "").replace(/[\\/:*?"<>|\r\n\t]+/g, " ").replace(/\s+/g, " ").trim();
  const ext = ((/\.[A-Za-z0-9]{1,5}$/.exec(file.name || "") || [""])[0] || (/pdf/.test(file.type) ? ".pdf" : /png/.test(file.type) ? ".png" : ".jpg")).toLowerCase();
  const base = [clean(title).slice(0, 60) || "스캔본", clean(student), round ? `${round}차` : "차수모름"].filter(Boolean).join("_");
  let name = base + ext, k = 2;
  while (taken.has(name)) name = `${base}_${k++}${ext}`;
  taken.add(name);
  return name;
}
