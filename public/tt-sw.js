// 시록고 강사도구 — 받는 일꾼(서비스 워커), 범위 /seirocco
// 하는 일은 하나: 안드로이드에서 강사도구를 앱으로 설치했을 때, 다른 앱(vFlat 등)의 「공유 → 강사도구」로 온
// POST /seirocco/tt-share 의 파일(scan)을 IndexedDB tt-share/inbox 에 두고 /seirocco#/tt/inbox 를 연다.
// 다른 요청은 건드리지 않고(캐시 없음) 그대로 네트워크로 보낸다.
const DB = "tt-share", STORE = "inbox";

function idb() {
  return new Promise((ok, no) => {
    const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(STORE, { keyPath: "id", autoIncrement: true });
    r.onsuccess = () => ok(r.result);
    r.onerror = () => no(r.error);
  });
}

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== "POST" || u.origin !== self.location.origin || u.pathname !== "/seirocco/tt-share") return;
  e.respondWith((async () => {
    try {
      const fd = await e.request.formData();
      const files = fd.getAll("scan").filter((f) => f && typeof f === "object" && f.size > 0);
      if (files.length) {
        const db = await idb();
        await new Promise((ok, no) => {
          const t = db.transaction(STORE, "readwrite");
          const st = t.objectStore(STORE);
          const at = Date.now();
          for (const f of files) st.add({ at, name: f.name || "scan", type: f.type || "", size: f.size, blob: f });
          t.oncomplete = ok;
          t.onerror = () => no(t.error);
        });
        db.close();
      }
    } catch (err) { /* 못 받았으면 화면에서 「받은 파일이 없어요」 */ }
    return Response.redirect("/seirocco#/tt/inbox", 303);
  })());
});
