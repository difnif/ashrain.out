// ashrain.out — 콘텐츠 파이프라인 비용·시간 시뮬레이터 (SimCost.jsx v1.0, 공개 #/sim)
// 입력값이 URL 해시에 실려 공유 가능: ashrainout.com/#/sim?tQA=20000&... → [링크 복사]

import { useEffect, useMemo, useState } from "react";

const P = { haiku: { i: 1, o: 5 }, sonnet: { i: 3, o: 15 }, opus: { i: 5, o: 25 } };
const GEN_OUT = { calc: 900, lo: 1400, mid: 1900, hi: 2600 };
const LOC_SEC = { calc: 35, lo: 55, mid: 75, hi: 100 };
const DEN = 6;
const DEF = { tQA: 20000, tQAr: "cloud", tSol: 8000, tSolr: "local", batch: 1, yld: 80,
  gCalc: 0, gLo: 5000, gMid: 10000, gHi: 10000, gpu: 1, hrs: 22,
  aH: 0, aHd: "mid", aS: 0, aSd: "mid", aO: 0, aOd: "hi", fx: 1400 };

const readHash = () => {
  const q = (location.hash.split("?")[1] || "");
  const out = { ...DEF };
  for (const kv of q.split("&")) {
    const [k, v] = kv.split("=");
    if (k in out) out[k] = isNaN(Number(v)) ? v : Number(v);
  }
  return out;
};

const RunnerRow = ({ label, val, onVal, sel, onSel }) => (
  <div className="sc-row">
    <span className="sc-lab">{label}</span>
    <input type="number" inputMode="numeric" min="0" step="1000" value={val} onChange={onVal} />
    <select value={sel} onChange={onSel}>
      <option value="cloud">클라우드</option><option value="local">로컬</option>
    </select>
  </div>
);
const ModelRow = ({ label, val, onVal, sel, onSel }) => (
  <div className="sc-row">
    <span className="sc-lab">{label}</span>
    <input type="number" inputMode="numeric" min="0" step="500" value={val} onChange={onVal} />
    <select value={sel} onChange={onSel}>
      <option value="calc">단순연산</option><option value="lo">하</option>
      <option value="mid">중</option><option value="hi">상</option>
    </select>
  </div>
);

const fmt$ = (v) => "$" + (v >= 100 ? Math.round(v).toLocaleString() : v.toFixed(v >= 10 ? 1 : 2));
const fmtD = (h, perDay) => (h <= 0 ? "0" : h / perDay < 1 ? h.toFixed(1) + "h" : (h / perDay).toFixed(1) + "일");

export default function SimCost() {
  const [s, setS] = useState(readHash);
  const [copied, setCopied] = useState(false);
  const up = (k) => (e) => {
    const v = e.target.type === "checkbox" ? (e.target.checked ? 1 : 0)
      : e.target.type === "number" || e.target.type === "range" ? Math.max(0, Number(e.target.value) || 0)
      : e.target.value;
    setS((p) => ({ ...p, [k]: v }));
  };

  useEffect(() => {
    const q = Object.entries(s).filter(([k, v]) => v !== DEF[k]).map(([k, v]) => `${k}=${v}`).join("&");
    history.replaceState(null, "", "#/sim" + (q ? "?" + q : ""));
  }, [s]);

  const r = useMemo(() => {
    const batch = s.batch ? 0.5 : 1, yld = s.yld / 100, spd = Number(s.gpu);
    let cost = 0, cloudPages = 0, locPages = 0, escN = 0;
    const det = [];
    for (const [cnt, rn, pageF, unit, label] of [
      [s.tQA, s.tQAr, 1.0, 0.006, "빠른답 세트"], [s.tSol, s.tSolr, 1.7, 0.009, "해설 세트"]]) {
      if (!cnt) continue;
      const pages = Math.ceil((cnt / DEN) * pageF);
      if (rn === "cloud") { const c = cnt * unit * batch; cost += c; cloudPages += pages;
        det.push(`전사·클라우드 — ${label} ${cnt.toLocaleString()}문항 (${pages.toLocaleString()}p): ${fmt$(c)}`);
      } else { locPages += pages; const esc = Math.round(cnt * (1 - yld)); escN += esc;
        det.push(`전사·로컬 — ${label} ${cnt.toLocaleString()}문항 (${pages.toLocaleString()}p): $0 · 수동 큐 ~${esc.toLocaleString()}`);
      }
    }
    const cloudH = cloudPages / 300;
    if (cloudPages) det.push(`클라우드 전사 벽시계: 약 ${cloudH < 1 ? Math.round(cloudH * 60) + "분" : cloudH.toFixed(1) + "시간"}`);
    const locTransH = locPages / (18 * spd);
    let locGenH = 0; const gd = [];
    for (const [n, k, label] of [[s.gCalc, "calc", "단순연산"], [s.gLo, "lo", "하"], [s.gMid, "mid", "중"], [s.gHi, "hi", "상"]]) {
      if (!n) continue;
      locGenH += (n * LOC_SEC[k]) / spd / 3600;
      gd.push(`${label} ${n.toLocaleString()}`);
    }
    if (gd.length) det.push(`생성·로컬 — ${gd.join(" · ")}: $0 · GPU ${fmtD(locGenH, s.hrs)}`);
    for (const [n, d, mk, label] of [[s.aH, s.aHd, "haiku", "하이쿠"], [s.aS, s.aSd, "sonnet", "소넷"], [s.aO, s.aOd, "opus", "오푸스"]]) {
      if (!n) continue;
      const c = n * ((1200 * P[mk].i + GEN_OUT[d] * P[mk].o) / 1e6) * 1.15 * batch;
      cost += c;
      det.push(`생성·API — ${label}(${{ calc: "단순연산", lo: "하", mid: "중", hi: "상" }[d]}) ${n.toLocaleString()}문항: ${fmt$(c)}`);
    }
    return { cost, gpuH: locTransH + locGenH, locTransH, locGenH, escN, det };
  }, [s]);

  const copy = async () => {
    const url = location.origin + location.pathname + location.hash;
    try { await navigator.clipboard.writeText(url); } catch { window.prompt("복사해서 공유:", url); }
    setCopied(true); setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="sc-wrap">
      <style>{CSS}</style>
      <h2>콘텐츠 파이프라인 시뮬레이터</h2>
      <div className="sc-top">
        <div className="sc-metric"><p>총 API 비용</p><b>{fmt$(r.cost)}</b>
          <span>약 {Math.round((r.cost * s.fx) / 1000).toLocaleString()}천 원{s.batch ? " · 배치가" : ""}</span></div>
        <div className="sc-metric"><p>로컬 GPU 점유</p><b>{fmtD(r.gpuH, s.hrs)}</b>
          <span>{r.gpuH > 0 ? `전사 ${fmtD(r.locTransH, s.hrs)} + 생성 ${fmtD(r.locGenH, s.hrs)}` : "로컬 일감 없음"}</span></div>
      </div>

      <p className="sc-h">① DB 전사 입력</p>
      <div className="sc-card">
        <RunnerRow label="문항+빠른정답" val={s.tQA} onVal={up("tQA")} sel={s.tQAr} onSel={up("tQAr")} />
        <RunnerRow label="문항+해설지" val={s.tSol} onVal={up("tSol")} sel={s.tSolr} onSel={up("tSolr")} />
        <div className="sc-row">
          <label className="sc-sub">배치 API 50%</label>
          <input type="checkbox" checked={!!s.batch} onChange={up("batch")} />
          <label className="sc-sub">로컬 수율</label>
          <input type="range" min="50" max="98" step="1" value={s.yld} onChange={up("yld")} style={{ flex: 1 }} />
          <b className="sc-v">{s.yld}%</b>
        </div>
        <p className="sc-note">
          {r.escN ? <>수동 큐(구독 처리 대기) 총 <b>{r.escN.toLocaleString()}문항</b></> : "수동 큐 낙수 없음"}
        </p>
      </div>

      <p className="sc-h">② 로컬 생성 — 문항+4단 해설</p>
      <div className="sc-card">
        <div className="sc-grid">
          {[["단순 연산", "gCalc"], ["하 (d1–2)", "gLo"], ["중 (d3)", "gMid"], ["상 (d4–5)", "gHi"]].map(([l, k]) => (
            <div key={k}><label className="sc-sub">{l}</label>
              <input type="number" inputMode="numeric" min="0" step="500" value={s[k]} onChange={up(k)} style={{ width: "100%" }} /></div>
          ))}
        </div>
        <div className="sc-row" style={{ marginTop: 8 }}>
          <select value={s.gpu} onChange={up("gpu")}>
            <option value="1">RTX 3060 8GB</option><option value="3">RTX 3090 24GB</option>
          </select>
          <label className="sc-sub">하루</label>
          <input type="range" min="4" max="24" step="1" value={s.hrs} onChange={up("hrs")} style={{ flex: 1 }} />
          <b className="sc-v">{s.hrs}h</b>
        </div>
        <p className="sc-note">템플릿 트랙 생성은 결정론(GPU 0시간) — 여기는 LLM 직접 생성분만.</p>
      </div>

      <p className="sc-h">③ API 생성 — 문항+4단 해설</p>
      <div className="sc-card">
        <ModelRow label="하이쿠" val={s.aH} onVal={up("aH")} sel={s.aHd} onSel={up("aHd")} />
        <ModelRow label="소넷" val={s.aS} onVal={up("aS")} sel={s.aSd} onSel={up("aSd")} />
        <ModelRow label="오푸스" val={s.aO} onVal={up("aO")} sel={s.aOd} onSel={up("aOd")} />
        <p className="sc-note">API 생성은 병렬이라 벽시계 반나절 안쪽 — 비용만 봄.</p>
      </div>

      <div className="sc-card">
        <p className="sc-h" style={{ margin: "0 0 6px" }}>내역</p>
        {r.det.length ? r.det.map((d, i) => <p key={i} className="sc-det">{d}</p>) : <p className="sc-det">물량을 입력해봐</p>}
      </div>

      <div className="sc-row" style={{ marginTop: 10 }}>
        <label className="sc-sub">환율 ₩/$</label>
        <input type="number" inputMode="numeric" min="1000" step="10" value={s.fx} onChange={up("fx")} style={{ width: 90 }} />
        <span style={{ flex: 1 }} />
        <button className="sc-btn" onClick={copy}>{copied ? "복사됨 ✓" : "공유 링크 복사"}</button>
      </div>
      <p className="sc-note">가정: 하이쿠 $1/$5 · 소넷 $3/$15 · 오푸스 $5/$25 (MTok), 페이지당 6문항, 로컬 3060 기준 35~100초/건.</p>
    </div>
  );
}

const CSS = `
.sc-wrap{max-width:560px;margin:0 auto;padding:16px 14px 60px;color:#1e293b}
.sc-wrap h2{font-size:19px;margin:4px 0 10px}
.sc-top{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:sticky;top:0;z-index:5;background:#fff;padding:6px 0;border-bottom:1px solid #e2e8f0;margin-bottom:10px}
.sc-metric{background:#f8fafc;border-radius:10px;padding:10px}
.sc-metric p{margin:0;font-size:12px;color:#64748b}
.sc-metric b{font-size:21px;font-weight:700}
.sc-metric span{display:block;font-size:11.5px;color:#94a3b8}
.sc-h{font-size:14px;font-weight:700;margin:14px 0 6px}
.sc-card{border:1px solid #e2e8f0;border-radius:12px;padding:12px;background:#fff;margin-bottom:4px}
.sc-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.sc-row:last-child{margin-bottom:0}
.sc-lab{font-size:13px;flex:1;min-width:84px}
.sc-sub{font-size:12px;color:#64748b}
.sc-v{font-size:13px;min-width:34px;text-align:right}
.sc-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.sc-note{font-size:12px;color:#94a3b8;margin:8px 0 0}
.sc-det{font-size:13px;color:#475569;margin:2px 0;line-height:1.6}
.sc-wrap input[type=number],.sc-wrap select{padding:7px 8px;border:1px solid #cbd5e1;border-radius:8px;font-size:13px;background:#fff;width:96px}
.sc-btn{padding:8px 14px;border:1px solid #0f172a;border-radius:8px;background:#0f172a;color:#fff;font-size:13px;cursor:pointer}
`;
