// src/pages/QrLogin.jsx — PC에서 QR 로그인 (해시 라우트: #/qr)
// 흐름: PC가 QR 생성 → 로그인된 폰이 스캔·승인 → PC가 토큰 수령 → 세션 발급
import { useEffect, useRef, useState } from "react";
import { QRCodeSVG } from "qrcode.react";
import { supabase, api, recordLoginMethod } from "../lib/authx";

export default function QrLogin() {
  const [sess, setSess] = useState(null);    // { qr_id, poll_key, expires_at }
  const [state, setState] = useState("init"); // init | waiting | signing | done | expired | error
  const [err, setErr] = useState("");
  const timer = useRef(null);

  const stop = () => { if (timer.current) { clearInterval(timer.current); timer.current = null; } };

  const create = async () => {
    stop();
    setErr(""); setState("init");
    try {
      const r = await api("qr", { action: "create" });
      setSess(r);
      setState("waiting");
    } catch (e) {
      setErr(e.message || String(e));
      setState("error");
    }
  };

  useEffect(() => { create(); return stop; }, []);

  useEffect(() => {
    if (state !== "waiting" || !sess) return;
    timer.current = setInterval(async () => {
      try {
        if (new Date(sess.expires_at) < new Date()) { stop(); setState("expired"); return; }
        const r = await api("qr", { action: "claim", qr_id: sess.qr_id, poll_key: sess.poll_key });
        if (r.pending) return;
        if (r.token_hash) {
          stop(); setState("signing");
          let out = await supabase.auth.verifyOtp({ type: "magiclink", token_hash: r.token_hash });
          if (out.error) out = await supabase.auth.verifyOtp({ type: "email", token_hash: r.token_hash });
          if (out.error) throw new Error("세션 발급에 실패했어요. QR을 새로 만들어주세요.");
          recordLoginMethod("qr");
          setState("done"); // App이 세션 변화를 감지해 홈으로 전환됨
          location.hash = "";
        }
      } catch (e) {
        if (e.status === 410) { stop(); setState("expired"); return; }
        stop(); setErr(e.message || String(e)); setState("error");
      }
    }, 2000);
    return stop;
  }, [state, sess]);

  const payload = sess
    ? `${location.origin}${location.pathname}#/qr-approve?sid=${sess.qr_id}`
    : "";

  return (
    <div className="ql-wrap"><Style />
      <h2 className="ql-title">QR 로그인</h2>
      <p className="ql-desc">폰의 카메라(또는 ashrain 앱)에서 아래 QR을 스캔하고,
        폰 화면에서 <b>승인</b>을 누르면 이 PC가 바로 로그인돼요.</p>

      <div className="ql-card">
        {state === "waiting" && sess && (
          <>
            <div className="ql-qrbox"><QRCodeSVG value={payload} size={196} marginSize={2} /></div>
            <p className="ql-hint">유효시간 2분 · 폰이 이미 로그인돼 있어야 해요</p>
          </>
        )}
        {state === "init" && <p className="ql-hint">QR 만드는 중…</p>}
        {state === "signing" && <p className="ql-hint">승인 확인! 로그인 중…</p>}
        {state === "done" && <p className="ql-ok">로그인 완료! 이동 중…</p>}
        {state === "expired" && (
          <>
            <p className="ql-hint">QR이 만료됐어요.</p>
            <button className="ql-btn ql-btn-main" onClick={create}>새 QR 만들기</button>
          </>
        )}
        {state === "error" && (
          <>
            <p className="ql-err">{err}</p>
            <button className="ql-btn" onClick={create}>다시 시도</button>
          </>
        )}
      </div>

      <a className="ql-back" href="#/">← 아이디로 로그인</a>
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .ql-wrap{max-width:420px;margin:0 auto;padding:32px 16px 48px;color:var(--text,#1c1c1e);text-align:center}
      .ql-title{margin:4px 0 8px;font-size:22px}
      .ql-desc{font-size:14px;line-height:1.7;color:var(--muted,#4b5563);margin:0 0 14px;text-align:left}
      .ql-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:16px;padding:22px;display:flex;flex-direction:column;gap:10px;align-items:center}
      .ql-qrbox{background:#fff;padding:10px;border-radius:12px}
      .ql-hint{font-size:12px;color:var(--muted,#8a8f98);margin:0}
      .ql-ok{font-size:14px;color:var(--good,#16a34a);margin:0}
      .ql-err{font-size:13px;color:var(--bad,#dc2626);margin:0}
      .ql-btn{padding:11px 16px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:14px;color:inherit}
      .ql-btn-main{background:var(--accent,#3b82f6);border-color:var(--accent,#3b82f6);color:#fff}
      .ql-back{display:inline-block;margin-top:16px;font-size:13px;color:var(--muted,#6b7280)}
    `}</style>
  );
}
