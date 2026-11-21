// ashrain.out — 사전식 「카드로 순번 찾기」 (frames/lexcards.jsx) — 경우의 수와 확률 100제 · 사전식 세트의 그림
// 걸음 · 박자는 ../lexwalk.js(나무 자료에서 만들고 판서 줄에 맞춘다). 받은 칸(box)에 맞춰 스스로 그린다(글자 크기 고정 · flex 그림).
//   위: 빈칸(늘어놓을 자리) — 다음에 정할 자리 위에 금빛 꺾쇠.
//   가운데: 셈(지금까지 지나온 문자열 수 · 「번째」) · 옆에 지금 지나가는 묶음 이름표. 그 아래 숫자 테이프(24 + 24 + 6 + 2 + 2 = 58 — 숫자 분석 그대로,
//           수마다 아래에 묶음 이름).
//   아래: 카드 늘어놓기(판서 「카드 A, B, C …」 줄에서 한 장씩 날아와 펼쳐진다).
//   묶음 지나가기: 그 글자 카드가 들려 빛나고, 자리에는 후보 글자(하늘색), 뒤 자리들은 묶음 안 문자열을 슬롯머신처럼 휘리릭 돌며 셈이 오른다
//                 → 다 지나가면 「+24」가 테이프로 날아가 붙는다.
//   고르기: 카드가 호를 그리며 자리로 날아가 꽂히고(금빛 고리), 카드 자리에는 빗금(소모).
//   최종 묶음: 남은 문자열을 하나씩 점멸하며 센다 — 셈이 1씩 오르고, 마지막 순서에서 멈춰 금빛으로.
import { seg, E } from "../core.js";
import { SANS, mathWidth } from "../draw.jsx";
import { l10Plan } from "../lin10.js";
import { lexWalk, lexTimes, nthArr, nP } from "../lexwalk.js";

/** 받은 칸에 맞춰 그리는 그림(../board.js 의 flex) — 가장 작게 · 가장 크게. must: 풀이의 몸통이라 자리가 모자라면 그림 칸을 먼저 뗀다 */
export const LEX_FIG = { flex: true, must: true, minW: 440, minH: 330, maxW: 700, maxH: 520 };

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, k) => a + (b - a) * k;

/** 칸 안 배치 — 빈칸 줄 · 셈 줄 · 테이프 줄 · 카드 줄을 위에서부터 */
export function lexGeom(W, B) {
  const w = B.x1 - B.x0, h = B.y1 - B.y0, pad = 8;
  const r = W.r, n = W.cards.length;
  const top = Math.min(30, h * 0.07);
  let sh = Math.min(118, h * 0.27);
  const ch = Math.min(84, h * 0.18), th = Math.min(80, h * 0.18);
  let dh = Math.min(88, h * 0.2);
  const sMax = (w - 2 * pad) / (r + (r - 1) * 0.18);
  if (sh * 0.74 > sMax) sh = sMax / 0.74;
  const sw = sh * 0.74, sg = sw * 0.18;
  const dMax = (w - 2 * pad) / (n + (n - 1) * 0.2);
  if (dh * 0.74 > dMax) dh = dMax / 0.74;
  const dw = dh * 0.74, dg = dw * 0.2;
  const used = top + sh + ch + th + dh;
  const g = clamp((h - pad - used) / 3, 6, 30);
  let y = B.y0 + top + Math.max(0, (h - pad - used - 3 * g) / 2);
  const slotY = y; y += sh + g;
  const cntY = y; y += ch + g;
  const tapeY = y; y += th + g;
  const deckY = y;
  const sx0 = B.x0 + (w - (r * sw + (r - 1) * sg)) / 2;
  const dx0 = B.x0 + (w - (n * dw + (n - 1) * dg)) / 2;
  return { B, w, h, pad, r, n, sh, sw, sg, dh, dw, dg, ch, th, slotY, cntY, tapeY, deckY, cx: B.x0 + w / 2,
    slotX: (p) => sx0 + p * (sw + sg), deckX: (i) => dx0 + i * (dw + dg) };
}

/** 숫자 테이프 배치 — 마지막 모양(모든 수 + 「= 셈」) 기준으로 자리를 정해 두고, 수가 붙을 때마다 그 자리에 나타난다(칸마다 한 번 잰다) */
const TAPES = new WeakMap();
function tapeLayout(W, G) {
  let m = TAPES.get(W);
  if (!m) { m = new Map(); TAPES.set(W, m); }
  const key = `${Math.round(G.w)}|${Math.round(G.th)}|${Math.round(G.cx)}`;
  if (!m.has(key)) m.set(key, tapeLayout0(W, G));
  return m.get(key);
}
function tapeLayout0(W, G) {
  const terms = [...W.levels.flatMap((lv) => lv.skips.map((sk) => ({ v: sk.m, lab: sk.prefix }))), { v: W.final.j, lab: "최종", fin: true }];
  const maxW = G.w - 2 * G.pad;
  let tz = clamp(G.th * 0.44, 20, 34);
  for (;;) {
    const lz = Math.max(18, tz * 0.62), sp = tz * 0.5;
    const ws = terms.map((x) => Math.max(mathWidth(String(x.v), tz, 800), mathWidth(x.lab, lz, 700)));
    const plusW = mathWidth("+", tz, 700) + sp * 2, eqW = mathWidth(`= ${W.total}`, tz, 800) + sp;
    const total = ws.reduce((a, b) => a + b, 0) + plusW * (terms.length - 1) + eqW;
    if (total <= maxW || tz <= 18) {
      let x = G.cx - total / 2;
      const pos = terms.map((x0, i) => { const cx = x + ws[i] / 2; x += ws[i] + (i < terms.length - 1 ? plusW : 0); return { ...x0, cx, w: ws[i] }; });
      return { tz, lz, terms: pos, eqX: x + sp, plusW };
    }
    tz -= 1;
  }
}

/** 카드 한 장(모서리 둥근 네모 + 글자) */
function Card({ x, y, w, h, L, C, fill, stroke, sw = 2.5, ink, op = 1, dash, rot = 0, scale = 1, glow }) {
  const cx = x + w / 2, cy = y + h / 2;
  return (
    <g opacity={op} transform={rot || scale !== 1 ? `rotate(${rot.toFixed(2)} ${cx.toFixed(1)} ${cy.toFixed(1)}) translate(${cx.toFixed(1)} ${cy.toFixed(1)}) scale(${scale.toFixed(3)}) translate(${(-cx).toFixed(1)} ${(-cy).toFixed(1)})` : undefined}>
      {glow && <rect x={x - 6} y={y - 6} width={w + 12} height={h + 12} rx={w * 0.2} fill={glow} opacity={0.28} />}
      <rect x={x} y={y} width={w} height={h} rx={w * 0.14} fill={fill ?? C.card} stroke={stroke ?? C.cardEdge} strokeWidth={sw} strokeDasharray={dash} />
      {L && <text x={cx} y={y + h * 0.69} fontFamily={SANS} fontSize={h * 0.56} fontWeight={800} fill={ink ?? C.ink} textAnchor="middle">{L}</text>}
    </g>
  );
}

/** 빨리 감기 표(▶▶) */
const FF = ({ x, y, z, fill }) => (
  <path d={`M${x} ${y - z * 0.36} l${z * 0.42} ${z * 0.36} l${-z * 0.42} ${z * 0.36} z M${x + z * 0.4} ${y - z * 0.36} l${z * 0.42} ${z * 0.36} l${-z * 0.42} ${z * 0.36} z`} fill={fill} />
);

/** 슬롯머신 — 자리 pos0 부터 len 칸이 문자열 k → k+1 로 굴러간다(frac 0~1). blur: 빠르기(속도 줄) */
function reels({ key, G, y, pos0, len, a, b, frac, blur, C, id, tint }) {
  const out = [];
  for (let q = 0; q < len; q++) {
    const sx = G.slotX(pos0 + q), x0 = a[q], x1 = b[q];
    const cid = `${id}-${key}${q}`;
    out.push(
      <g key={`${key}${q}`}>
        <clipPath id={cid}><rect x={sx} y={y} width={G.sw} height={G.sh} rx={G.sw * 0.14} /></clipPath>
        <rect x={sx} y={y} width={G.sw} height={G.sh} rx={G.sw * 0.14} fill={C.card} stroke={tint || C.cardEdge} strokeWidth={tint ? 3 : 2} opacity={0.92} />
        <g clipPath={`url(#${cid})`} fontFamily={SANS} fontSize={G.sh * 0.56} fontWeight={800} textAnchor="middle">
          {x0 === x1
            ? <text x={sx + G.sw / 2} y={y + G.sh * 0.69} fill={C.ink} opacity={0.92}>{x0}</text>
            : <>
              <text x={sx + G.sw / 2} y={y + G.sh * 0.69 - frac * G.sh * 0.95} fill={C.ink} opacity={1 - frac * 0.7}>{x0}</text>
              <text x={sx + G.sw / 2} y={y + G.sh * 0.69 + (1 - frac) * G.sh * 0.95} fill={C.ink} opacity={0.3 + frac * 0.7}>{x1}</text>
            </>}
          {blur > 0.35 && [0.3, 0.5, 0.7].map((v) => (
            <line key={v} x1={sx + G.sw * 0.12} y1={y + G.sh * v} x2={sx + G.sw * 0.88} y2={y + G.sh * v} stroke={tint || C.sky} strokeWidth={2} opacity={(blur - 0.35) * 0.55} />
          ))}
        </g>
      </g>,
    );
  }
  return out;
}
/** [t0, t1] 동안 m 개를 굴리는 진행 — { k(지금 문자열 · 0부터), frac, blur } */
function spin(t, t0, t1, m) {
  const p = seg(t, t0, t1, E.io), f = p * m;
  const k = Math.min(m - 1, Math.floor(f));
  return { k, frac: k >= m - 1 ? 0 : f - k, blur: Math.sin(Math.PI * clamp((t - t0) / (t1 - t0), 0, 1)) };
}

export function LexCards({ it, t, C, box }) {
  const W = lexWalk(it);
  if (!W || !box) return null;
  const P = l10Plan(it), T = lexTimes(it, P), G = lexGeom(W, box);
  if (t < T.deal[0]) return null;
  const id = `lx${it.no}-${Math.round(box.x0)}-${Math.round(box.y0)}`;
  const picks = T.ev.filter((e) => e.type === "pick");
  const skips = T.ev.filter((e) => e.type === "skip");
  const count = T.ev.find((e) => e.type === "count");
  const F = W.final;
  const done = t >= count.t1;
  const skipNow = skips.find((e) => t >= e.t0 && t < e.t1) || null;
  const counting = t >= count.t0 && !done;
  const els = [];

  /* ── 셈 값 ── */
  let value = 0;
  for (const e of skips) {
    if (t >= e.t1) value = e.sk.c0 + e.sk.m;
    else if (t >= e.t0) value = e.sk.c0 + spin(t, e.t0, e.t1, e.sk.m).k + 1;     // 지금 보이는 문자열의 순번
  }
  let ci = -1, ph = 0, fastNow = null;      // 최종 묶음: 지금 몇 번째(0부터) · 점멸 한 번 안의 진행 · 휘리릭 중이면 그 진행
  if (t >= count.t0) {
    if (count.fastN && t < count.bt0) {
      fastNow = spin(t, count.t0, count.fastEnd, count.fastN);
      ci = fastNow.k;
    } else {
      const e = t - count.bt0;
      ci = Math.min(F.j - 1, count.fastN + Math.floor(e / count.step));
      ph = done ? 1 : (e - (ci - count.fastN) * count.step) / count.step;
    }
    value = F.c0 + ci + 1;
  }

  /* ── 빈칸(자리) ── */
  const fixedAt = (p) => { const e = picks[p]; return e && t >= e.t1 ? e : null; };
  const nextPos = picks.findIndex((e) => t < e.t1);
  for (let p = 0; p < W.r; p++) {
    const x = G.slotX(p), y = G.slotY;
    const ap = seg(t, T.slots + p * 80, T.slots + p * 80 + 420, E.back);
    if (ap <= 0) continue;
    els.push(<Card key={`sb${p}`} x={x} y={y} w={G.sw} h={G.sh} C={C} fill="none" stroke={C.soft} sw={2} dash="7 6" op={0.75 * Math.min(1, ap)} scale={0.7 + 0.3 * ap} />);
  }
  // 고정된 글자(고른 카드)
  picks.forEach((e, p) => {
    if (t < e.t1) return;
    const x = G.slotX(p), y = G.slotY;
    const gold = done;
    els.push(<Card key={`sf${p}`} x={x} y={y} w={G.sw} h={G.sh} L={e.L} C={C} stroke={gold ? C.gold : C.cardEdge} sw={gold ? 3.5 : 2.5} ink={gold ? C.gold : C.ink} />);
    const k = seg(t, e.t1, e.t1 + 520, E.out);
    if (k > 0 && k < 1) els.push(<rect key={`ring${p}`} x={x - 6 - 14 * k} y={y - 6 - 14 * k} width={G.sw + 12 + 28 * k} height={G.sh + 12 + 28 * k} rx={G.sw * 0.2} fill="none" stroke={C.gold} strokeWidth={4} opacity={1 - k} />);
  });
  // 묶음 지나가기 — 후보 글자 + 뒤 자리 슬롯머신
  if (skipNow) {
    const { sk } = skipNow, pos = skipNow.pos;
    const sp = spin(t, skipNow.t0, skipNow.t1, sk.m);
    const x = G.slotX(pos), y = G.slotY;
    const pulse = 1 + 0.04 * Math.sin((t - skipNow.t0) / 70);
    els.push(<Card key="cand" x={x} y={y} w={G.sw} h={G.sh} L={sk.L} C={C} stroke={C.sky} sw={3.5} ink={C.sky} scale={pulse} glow={C.sky} />);
    els.push(...reels({ key: "r", G, y, pos0: pos + 1, len: sk.len, a: nthArr(sk.letters, sk.len, sp.k), b: nthArr(sk.letters, sk.len, Math.min(sk.m - 1, sp.k + 1)),
      frac: sp.frac, blur: sp.blur, C, id }));
  }
  // 최종 묶음 — 하나씩 점멸
  if (fastNow) {
    els.push(...reels({ key: "f", G, y: G.slotY, pos0: F.pos, len: F.len, a: nthArr(F.letters, F.len, ci), b: nthArr(F.letters, F.len, Math.min(count.fastN - 1, ci + 1)),
      frac: fastNow.frac, blur: fastNow.blur, C, id, tint: C.gold }));
  } else if (t >= count.t0) {
    const s = nthArr(F.letters, F.len, ci);
    const last = ci === F.j - 1;
    const on = last ? 1 : ph < 0.7 ? 1 : 0.12;
    const pop = last && done ? 1 : 1 + 0.1 * (1 - seg(ph, 0, 0.3, E.out));
    for (let q = 0; q < F.len; q++) {
      const sx = G.slotX(F.pos + q);
      els.push(
        <Card key={`blink${q}`} x={sx} y={G.slotY} w={G.sw} h={G.sh} L={s[q]} C={C} op={Math.max(on, done ? 1 : 0)}
          stroke={done ? C.gold : C.gold} sw={done ? 3.5 : 3} ink={done ? C.gold : C.ink} scale={done ? 1 : pop} />,
      );
    }
    // 고정된 앞 글자도 점멸에 맞춰 금빛으로 깜빡(지금 세는 문자열 전체)
    if (!done) for (let p = 0; p < F.pos; p++) {
      els.push(<rect key={`bl${p}`} x={G.slotX(p) - 3} y={G.slotY - 3} width={G.sw + 6} height={G.sh + 6} rx={G.sw * 0.17} fill="none" stroke={C.gold} strokeWidth={2.5} opacity={on * 0.7} />);
    }
    // 다 셌다 — 줄 전체를 두르는 고리
    if (done) {
      const k = seg(t, count.t1, count.t1 + 650, E.out);
      if (k < 1) {
        const x0 = G.slotX(0) - 10, x1 = G.slotX(W.r - 1) + G.sw + 10;
        els.push(<rect key="won" x={x0 - 18 * k} y={G.slotY - 10 - 18 * k} width={x1 - x0 + 36 * k} height={G.sh + 20 + 36 * k} rx={G.sw * 0.3} fill="none" stroke={C.gold} strokeWidth={5} opacity={1 - k} />);
      }
    }
  }
  // 꺾쇠 — 다음에 정할 자리
  if (!counting && !done && nextPos >= 0 && t >= T.slots + 300) {
    const x = G.slotX(nextPos) + G.sw / 2, y = G.slotY - 9 + 3 * Math.sin(t / 260);
    els.push(<path key="caret" d={`M${x - 11} ${y - 12} L${x + 11} ${y - 12} L${x} ${y} z`} fill={C.gold} opacity={seg(t, T.slots + 300, T.slots + 700, E.sine)} />);
  }

  /* ── 카드 늘어놓기 · 소모 빗금 · 날아가는 카드 ── */
  W.cards.forEach((L, i) => {
    const x = G.deckX(i), y = G.deckY;
    const d0 = T.deal[0] + i * 110;
    const dp = seg(t, d0, d0 + 520, E.back);
    if (dp <= 0) return;
    const pe = picks.find((e) => e.L === L);
    const lifted = skipNow && skipNow.sk.L === L ? Math.min(1, (t - skipNow.t0) / 160, (skipNow.t1 - t) / 160) : 0;
    if (pe && t >= pe.t0) {
      // 자리로 떠난 카드 — 빈 자리 테두리와 빗금(소모)
      els.push(<Card key={`dg${i}`} x={x} y={y} w={G.dw} h={G.dh} L={L} C={C} fill="none" stroke={C.soft} sw={2} dash="5 5" ink={C.soft} op={0.5} />);
      const k = seg(t, pe.t1, pe.t1 + 320, E.out);
      if (k > 0) els.push(<line key={`dx${i}`} x1={x + G.dw * 0.16} y1={y + G.dh * 0.86} x2={x + G.dw * (0.16 + 0.68 * k)} y2={y + G.dh * (0.86 - 0.72 * k)} stroke={C.red} strokeWidth={4} strokeLinecap="round" />);
      if (t < pe.t1) {
        // 날아가는 중 — 호를 그리며 자리로
        const k2 = seg(t, pe.t0, pe.t1, E.out);
        const p = picks.indexOf(pe);
        const tx = G.slotX(p), ty = G.slotY;
        const fx = lerp(x, tx, k2), fy = lerp(y, ty, k2) - Math.sin(Math.PI * k2) * G.sh * 0.6;
        const fw = lerp(G.dw, G.sw, k2), fh = lerp(G.dh, G.sh, k2);
        els.push(<Card key={`fly${i}`} x={fx} y={fy} w={fw} h={fh} L={L} C={C} stroke={C.gold} sw={3} rot={-10 * Math.sin(Math.PI * k2)} glow={C.gold} />);
      }
      return;
    }
    els.push(
      <Card key={`d${i}`} x={x + (1 - dp) * 240} y={y - (1 - dp) * 36 - lifted * 14} w={G.dw} h={G.dh} L={L} C={C}
        rot={(1 - dp) * 18} op={Math.min(1, dp * 1.6)} stroke={lifted > 0 ? C.sky : undefined} sw={lifted > 0 ? 3 : 2.5} glow={lifted > 0 ? C.sky : null} />,
    );
  });

  /* ── 셈 ── */
  const first = skips[0] || count;              // 셈은 처음 세기 시작할 때부터(지나갈 묶음이 없으면 최종 묶음에서)
  const cntOn = seg(t, first.t0 - 400, first.t0, E.sine);
  if (cntOn > 0) {
    const cz = clamp(G.ch * 0.92, 40, 76), base = G.cntY + G.ch * 0.8;
    const digits = String(Math.max(W.total, nP(W.cards.length, W.r))).length;
    const numW = digits * cz * 0.6;
    const labZ = cz * 0.42;
    const pz = clamp(G.ch * 0.34, 20, 28);
    const labW = mathWidth("번째", labZ, 700);
    const all = nP(W.cards.length, W.r);
    const showBack = T.back != null && t >= T.back;
    const backTxt = showBack ? `→ 뒤에서 ${all - W.total + 1}번째` : null;
    const roomW = G.w - 2 * G.pad;
    const ff = !!skipNow || !!(fastNow && t < count.fastEnd);
    let pill = skipNow ? `${skipNow.sk.prefix} 묶음 ${skipNow.sk.m}개` : counting ? `최종 묶음 ${F.prefix || "—"}${ff ? "" : " · 하나씩"}` : null;
    let pillW = pill ? mathWidth(pill, pz, 800) + pz * (ff ? 2.6 : 1.6) : 0;
    if (pill && numW + 10 + labW + 28 + pillW > roomW) { pill = null; pillW = 0; }      // 칸이 좁으면 이름표는 뺀다
    const backW = backTxt ? mathWidth(backTxt, pz * 1.05, 800) + 26 : 0;
    const groupW = numW + 10 + labW + (pill ? 28 + pillW : 0) + backW;
    const gx = Math.max(G.B.x0 + G.pad, G.cx - groupW / 2);
    const col = done ? C.gold : skipNow ? C.sky : counting ? C.gold : C.ink;
    const popK = counting && !fastNow ? 1 + 0.12 * (1 - seg(ph, 0, 0.28, E.out)) : 1;
    const nx = gx + numW;
    els.push(
      <g key="cnt" opacity={cntOn}>
        <g transform={`translate(${nx.toFixed(1)} ${base.toFixed(1)}) scale(${popK.toFixed(3)}) translate(${(-nx).toFixed(1)} ${(-base).toFixed(1)})`}>
          <text x={nx} y={base} fontFamily={SANS} fontSize={cz} fontWeight={800} fill={col} textAnchor="end" style={{ fontVariantNumeric: "tabular-nums" }}>{value}</text>
        </g>
        <text x={nx + 10} y={base} fontFamily={SANS} fontSize={labZ} fontWeight={700} fill={C.soft}>번째</text>
        {pill && (
          <g>
            <rect x={nx + 10 + labW + 28} y={base - pz * 1.45} width={pillW} height={pz * 1.75} rx={pz * 0.87} fill={skipNow ? C.sky : C.gold} opacity={0.16} />
            {ff && <FF x={nx + 10 + labW + 28 + pz * 0.55} y={base - pz * 0.58} z={pz * 0.9} fill={skipNow ? C.sky : C.gold} />}
            <text x={nx + 10 + labW + 28 + pz * (ff ? 1.75 : 0.8)} y={base - pz * 0.24} fontFamily={SANS} fontSize={pz} fontWeight={800} fill={skipNow ? C.sky : C.gold}>{pill}</text>
          </g>
        )}
        {backTxt && (
          <text x={nx + 10 + labW + 26} y={base} fontFamily={SANS} fontSize={pz * 1.05} fontWeight={800} fill={C.coral} opacity={seg(t, T.back, T.back + 500, E.out)}>{backTxt}</text>
        )}
      </g>,
    );
  }

  /* ── 숫자 테이프 — 지나간 묶음의 수가 날아와 붙는다 ── */
  const TP = tapeLayout(W, G);
  const yN = G.tapeY + TP.tz * 1.0, yL = yN + TP.lz * 1.25;
  let ti = 0;
  skips.forEach((e) => {
    const term = TP.terms[ti++];
    if (t < e.t1) return;
    const k = seg(t, e.t1, e.t1 + 420, E.out);
    if (k < 1) {
      // 「+m」이 후보 자리에서 테이프로 날아간다
      const sx = G.slotX(e.pos) + G.sw / 2, sy = G.slotY + G.sh * 0.5;
      els.push(<text key={`chip${ti}`} x={lerp(sx, term.cx, k)} y={lerp(sy, yN, k)} fontFamily={SANS} fontSize={TP.tz * (1.4 - 0.4 * k)} fontWeight={800} fill={C.sky} textAnchor="middle" opacity={1 - k * 0.3}>+{e.sk.m}</text>);
      return;
    }
    const pop = 1 + 0.25 * (1 - seg(t, e.t1 + 420, e.t1 + 700, E.out));
    const fresh = seg(t, e.t1 + 420, e.t1 + 1400, E.sine);
    els.push(
      <g key={`term${ti}`}>
        {ti > 1 && <text x={term.cx - term.w / 2 - TP.plusW / 2} y={yN} fontFamily={SANS} fontSize={TP.tz} fontWeight={700} fill={C.soft} textAnchor="middle">+</text>}
        <g transform={`translate(${term.cx} ${yN}) scale(${pop.toFixed(3)}) translate(${-term.cx} ${-yN})`}>
          <text x={term.cx} y={yN} fontFamily={SANS} fontSize={TP.tz} fontWeight={800} fill={fresh < 1 ? C.sky : C.ink} textAnchor="middle">{e.sk.m}</text>
        </g>
        <text x={term.cx} y={yL} fontFamily={SANS} fontSize={TP.lz} fontWeight={700} fill={C.soft} textAnchor="middle">{term.lab}</text>
      </g>,
    );
  });
  if (t >= count.t0) {
    const term = TP.terms[TP.terms.length - 1];
    const v = ci + 1;
    els.push(
      <g key="termF">
        {TP.terms.length > 1 && <text x={term.cx - term.w / 2 - TP.plusW / 2} y={yN} fontFamily={SANS} fontSize={TP.tz} fontWeight={700} fill={C.soft} textAnchor="middle">+</text>}
        <text x={term.cx} y={yN} fontFamily={SANS} fontSize={TP.tz} fontWeight={800} fill={C.gold} textAnchor="middle">{v}</text>
        <text x={term.cx} y={yL} fontFamily={SANS} fontSize={TP.lz} fontWeight={700} fill={C.soft} textAnchor="middle">{term.lab}</text>
      </g>,
    );
    if (done) {
      const k = seg(t, count.t1, count.t1 + 500, E.out);
      els.push(<text key="eq" x={TP.eqX} y={yN} fontFamily={SANS} fontSize={TP.tz} fontWeight={800} fill={C.gold} opacity={k}>= {W.total}</text>);
    }
  }
  return <g>{els}</g>;
}
