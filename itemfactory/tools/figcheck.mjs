// ashrain.out — 도형 렌더러 전수 검사 (itemfactory/tools/figcheck.mjs, v1.0)
//
// corpus_items(+선택적으로 test_items)의 figure를 전부 figsvg로 그려 보고,
//   · 설명 상자로 떨어진 것(= 못 그린 것)의 fn별 통계
//   · 예외가 난 것의 목록
//   · 눈검수용 HTML 대조표(fn별 표본)
// 를 out/ 에 남긴다. DB는 읽기만 한다.
//
// 실행:  node itemfactory/tools/figcheck.mjs            # active 전량
//        node itemfactory/tools/figcheck.mjs --sample 20  # fn별 20건만
//        node itemfactory/tools/figcheck.mjs --table test_items
//
// .env: SUPABASE_URL / SUPABASE_SERVICE_KEY (itemfactory/.env)

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";
import { figureToHtml1, figureAudit } from "../../src/lib/figsvg.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const OUT = path.join(ROOT, "out");

function loadEnv() {
  for (const p of [path.join(ROOT, ".env"), path.join(process.cwd(), ".env")]) {
    if (!fs.existsSync(p)) continue;
    for (const line of fs.readFileSync(p, "utf8").split(/\r?\n/)) {
      const t = line.trim();
      if (!t || t.startsWith("#") || !t.includes("=")) continue;
      const [k, v] = t.split(/=(.*)/s);
      if (!(k.trim() in process.env)) process.env[k.trim()] = v.trim();
    }
  }
}

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };
const TABLE = arg("--table", "corpus_items");
const SAMPLE = Number(arg("--sample", 0)) || 0;

loadEnv();
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const rows = [];
for (let i = 0; ; i += 1000) {
  const q = sb.from(TABLE).select("id,figure").not("figure", "is", null).range(i, i + 999);
  if (TABLE === "corpus_items") q.eq("status", "active");
  const { data, error } = await q;
  if (error) { console.error(error.message); process.exit(1); }
  rows.push(...(data || []));
  if ((data || []).length < 1000) break;
}
console.log(`· ${TABLE} figure 보유 ${rows.length}건`);

const stat = {};                 // fn → {n, ok, note, err}
const samples = {};              // fn → [{id, fig}]
const failures = [];

for (const r of rows) {
  const list = Array.isArray(r.figure) ? r.figure : [r.figure];
  for (const f of list) {
    const fn = (f && f.fn) || "(null)";
    const s = (stat[fn] = stat[fn] || { n: 0, ok: 0, note: 0, err: 0 });
    s.n++;
    let res;
    try { res = figureToHtml1(f, { width: 260 }); }
    catch (e) { s.err++; failures.push({ id: r.id, fn, why: "throw: " + e.message }); continue; }
    if (res.kind === "note") {
      s.note++;
      if (fn !== "unsupported") failures.push({ id: r.id, fn, why: res.warnings.join(" / ") });
    } else s.ok++;
    const bag = (samples[fn] = samples[fn] || []);
    if (bag.length < (SAMPLE || 12)) bag.push({ id: r.id, fig: f, kind: res.kind });
  }
}

fs.mkdirSync(OUT, { recursive: true });
const table = Object.entries(stat).sort((a, b) => b[1].n - a[1].n)
  .map(([fn, s]) => `${fn.padEnd(12)} 전체 ${String(s.n).padStart(5)} · 그림 ${String(s.ok).padStart(5)} · 설명상자 ${String(s.note).padStart(5)} · 예외 ${s.err}`);
console.log("\n" + table.join("\n"));

fs.writeFileSync(path.join(OUT, "figcheck_report.json"),
  JSON.stringify({ table: TABLE, rows: rows.length, stat, failures: failures.slice(0, 2000) }, null, 1), "utf8");

// 눈검수용 대조표
let h = `<meta charset="utf-8"><title>figcheck</title><style>
body{font-family:system-ui;margin:16px;background:#fff;color:#111}
h2{margin:22px 0 8px;font-size:15px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:10px}
.c{border:1px solid #ddd;border-radius:8px;padding:6px}
.t{font:11px/1.35 ui-monospace,monospace;color:#666;margin-bottom:4px;max-height:44px;overflow:hidden}
</style><h1 style="font-size:17px">figcheck — ${TABLE} (${rows.length}행)</h1><pre style="font-size:12px">${table.join("\n")}</pre>`;
for (const [fn, bag] of Object.entries(samples).sort()) {
  h += `<h2>${fn} — ${stat[fn].n}건 (설명상자 ${stat[fn].note}, 예외 ${stat[fn].err})</h2><div class="g">`;
  for (const b of bag) {
    h += `<div class="c"><div class="t">${b.id.slice(0, 8)} ${escapeHtml(JSON.stringify(b.fig.args || {}).slice(0, 150))}</div>`
       + figureToHtml1(b.fig, { width: 250 }).html + `</div>`;
  }
  h += `</div>`;
}
fs.writeFileSync(path.join(OUT, "figcheck.html"), h, "utf8");
function escapeHtml(s) { return String(s).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }

console.log(`\n· out/figcheck_report.json · out/figcheck.html (브라우저로 열어 눈검수)`);
console.log(`· 못 그린 것(unsupported 제외) ${failures.length}건`);
