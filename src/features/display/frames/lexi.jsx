// ashrain.out — 수학 호기심 액자: 알파벳 카드 사전식 배열 (frames/lexi.jsx)
// 카드 n장(단어 섞기 · A부터 · 직접 입력)을 한 줄로 늘어놓는 모든 경우를 사전식(오름차순 · 내림차순)으로 쉬지 않고 넘긴다.
// 계산은 하지 않고 넘기기만 — 다만 늘어놓은 글자가 영어 낱말이면 멈춰서 사전처럼 발음기호 · 품사 · 뜻을 보인다.
//   · 카드는 다음 배열로 갈 때 바뀐 자리만 들려 옮겨진다(사전식이라 뒤쪽 카드가 자주, 앞쪽 카드는 드물게 바뀐다).
//   · 오른쪽 목록은 지나온 배열 — 첫 글자가 바뀌는 곳에 금을 긋는다(○로 시작하는 것이 몇 가지인지 눈으로).
//   · 숨은 낱말: 배열 속 세 글자 이상 이어진 낱말을 작은 꼬리표로.
// 계산: ../curio/lexi.js · 사전: ../curio/data-dict.js(늦게 들여온다 — 발음은 미국식, CMUdict 바탕 ipa-dict)
import { memo, useEffect, useState } from "react";
import { W, H, MText, SceneTitle, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip } from "../kit-story.jsx";
import { comma } from "../curio/kit.js";
import { LEXI, LEXI_DEF, fixLexi, lexiAt, setOf, countText } from "../curio/lexi.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { Panel, Small } from "./curio-kit.jsx";

const LSK = "ash.display.curio.lexi";
const LIST_X = 1176, LIST_W = 386;
const HUE = (ch) => (ch.charCodeAt(0) - 65) * (360 / 26);

/** 카드 자리(글자 j번째 나옴 → 카드 이름) */
function idsOf(s) { const seen = {}; return s.split("").map((c) => { seen[c] = (seen[c] || 0) + 1; return c + seen[c]; }); }
function layout(set) {
  const r = set.r, n = set.cards.length;
  const cw = Math.min(138, (1040 - (r - 1) * 18) / r), ch = cw * 1.34;
  const x0 = 600 - (r * cw + (r - 1) * 18) / 2;
  const main = Array.from({ length: r }, (_, j) => [x0 + j * (cw + 18), 330 - ch / 2]);
  const sw = cw * 0.52, sx0 = 600 - ((n - r) * sw + (n - r - 1) * 10) / 2;
  const spare = Array.from({ length: Math.max(0, n - r) }, (_, j) => [sx0 + j * (sw + 10), 330 + ch / 2 + 30]);
  return { cw, ch, main, spare, sw };
}
/** 배열 s 에서 카드 이름 → 자리 [x, y, 작게?] */
function placeOf(set, s, L) {
  const ids = idsOf(s);
  const pos = {};
  ids.forEach((id, j) => { pos[id] = [...L.main[j], 0]; });
  // 안 쓴 카드(r < n)는 아래 작은 줄에 — 남은 글자 정렬 순
  const all = idsOf(set.cards.join(""));
  const rest = all.filter((id) => !(id in pos));
  rest.forEach((id, j) => { pos[id] = [...L.spare[j], 1]; });
  return pos;
}

function Card({ x, y, w, h, ch, C, glow = 0, small = 0, o = 1 }) {
  const light = C.name === "light";
  const ww = small ? w * 0.52 : w, hh = small ? h * 0.52 : h;
  const hue = HUE(ch);
  const face = light ? `hsl(${hue} 70% 96%)` : `hsl(${hue} 32% 26%)`;
  const edge = light ? `hsl(${hue} 45% 55%)` : `hsl(${hue} 55% 70%)`;
  const ink = light ? `hsl(${hue} 55% 30%)` : `hsl(${hue} 80% 86%)`;
  return (
    <g opacity={o}>
      <rect x={x + 4} y={y + 6} width={ww} height={hh} rx={ww * 0.12} fill="#000" opacity={0.18} />
      {glow > 0.001 && <rect x={x - 6} y={y - 6} width={ww + 12} height={hh + 12} rx={ww * 0.16} fill="none" stroke={C.gold} strokeWidth={5} opacity={glow} />}
      <rect x={x} y={y} width={ww} height={hh} rx={ww * 0.12} fill={face} stroke={glow > 0.5 ? C.gold : edge} strokeWidth={2.6} />
      <text x={x + ww / 2} y={y + hh * 0.66} textAnchor="middle" fontFamily={SERIF} fontWeight={700} fontSize={hh * 0.52} fill={ink}>{ch}</text>
      <text x={x + ww * 0.13} y={y + hh * 0.16} textAnchor="middle" fontFamily={SANS} fontWeight={800} fontSize={hh * 0.1} fill={ink} opacity={0.7}>{ch}</text>
    </g>
  );
}

/** 사전 한 칸 */
function DictCard({ w, entry, C, o, y = 520 }) {
  if (!entry || o <= 0.001) return null;
  const [ipa, mean, base, form] = entry;
  const parts = mean.split("; ").map((p) => { const m = /^(명|동|형|부|전|접|대|감|수|조동|관) (.*)$/.exec(p); return m ? [m[1], m[2]] : ["", p]; });
  const x = 120, cw = 960;
  const h = 96 + parts.length * 44 + (base ? 40 : 0);
  return (
    <g opacity={o} transform={`translate(0, ${(1 - o) * 30})`}>
      <rect x={x} y={y} width={cw} height={h} rx={22} fill={C.card} stroke={C.gold} strokeWidth={2.4} />
      <text x={x + 34} y={y + 64} fontFamily={SERIF} fontWeight={700} fontSize={50} fill={C.ink} letterSpacing="0.04em">{w.toLowerCase()}</text>
      <text x={x + 44 + w.length * 31 + 20} y={y + 62} fontFamily={"'Noto Serif', 'Times New Roman', serif"} fontSize={30} fill={C.teal}>{ipa}</text>
      {parts.map(([pos, m], j) => (
        <g key={j}>
          {pos && <><rect x={x + 34} y={y + 92 + j * 44} width={38} height={30} rx={8} fill={C.gold} opacity={0.9} />
            <text x={x + 53} y={y + 114 + j * 44} textAnchor="middle" fontFamily={SANS} fontWeight={800} fontSize={18} fill={C.name === "light" ? "#fffdf6" : "#1c2647"}>{pos}</text></>}
          <UText x={x + (pos ? 86 : 34)} y={y + 116 + j * 44} s={m} size={26} weight={650} C={C} />
        </g>
      ))}
      {base && <UText x={x + 34} y={y + 108 + parts.length * 44} s={`‘${base}’의 ${form}`} size={20} weight={700} fill={C.soft} C={C} />}
    </g>
  );
}

/* ══════════ 그리기 ══════════ */
export function LexiArt({ C, mode, P, at, D }) {
  if (!D) return <MText x={600} y={460} s="사전을 불러오는 중…" size={34} anchor="middle" fill={C.soft} C={C} />;
  const { set, i, t, sum } = at;
  const L = layout(set);
  const cur = set.list[i], prev = i > 0 ? set.list[i - 1] : cur;
  const pA = placeOf(set, prev, L), pB = placeOf(set, cur, L);
  const tau = Math.min(420, set.d * 0.75);
  const k = sum >= 0 ? 1 : seg(t, 0, tau, E.io);
  const hit = set.hit[i] === 1;
  const entry = hit ? D.DICT[cur.toLowerCase()] : null;
  const glow = hit && sum < 0 ? seg(t, tau, tau + 300) * (1 - seg(t, set.d + LEXI.HOLD - 300, set.d + LEXI.HOLD)) : 0;
  const ids = idsOf(set.cards.join(""));
  // 숨은 낱말(세 글자 이상 이어진 것, 전체가 낱말이 아닐 때)
  const hidden = [];
  if (P.hid && !hit && cur.length > 3) {
    for (let a = 0; a < cur.length; a++) for (let b = a + 3; b <= cur.length; b++) {
      if (b - a === cur.length) continue;
      const w = cur.slice(a, b);
      if (D.DICT[w.toLowerCase()] && !hidden.includes(w)) hidden.push(w);
    }
  }
  const upto = set.hitIdx.filter((j) => j <= i);
  const found = upto.slice(-8).map((j) => set.list[j]);
  const nFound = upto.length;
  return (
    <g>
      {/* 카드 */}
      {ids.map((id) => {
        const a = pA[id] || pB[id], b = pB[id];
        const moved = a[0] !== b[0] || a[1] !== b[1];
        const x = lerp(a[0], b[0], k), y = lerp(a[1], b[1], k) - (moved ? Math.sin(Math.PI * k) * 46 : 0);
        const small = lerp(a[2], b[2], k) > 0.5 ? 1 : 0;
        return <Card key={id} x={x} y={y} w={L.cw} h={L.ch} ch={id[0]} C={C} glow={b[2] ? 0 : glow} small={small} o={small ? 0.55 : 1} />;
      })}
      {/* 번호 */}
      <UText x={600} y={330 + L.ch / 2 + (set.r < set.cards.length ? 152 : 56)} s={`${comma(i + 1)}번째`} size={30} weight={800} anchor="middle" fill={hit ? C.gold : C.ink} C={C} />
      {hidden.length > 0 && <MText x={600} y={330 + L.ch / 2 + (set.r < set.cards.length ? 188 : 96)} s={`숨은 낱말: ${hidden.join(" · ").toLowerCase()}`} size={20} weight={700} anchor="middle" fill={C.teal} C={C} />}
      <DictCard w={cur} entry={entry} C={C} o={glow} y={set.r < set.cards.length ? 600 : 520} />
      {/* 찾은 낱말 */}
      <UText x={70} y={858} s={`찾은 낱말 ${nFound}개${found.length ? ":" : ""}`} size={20} weight={800} fill={C.soft} C={C} />
      {found.map((w, j) => <Chip key={w} x={250 + j * 108} y={851} s={w.toLowerCase()} size={18} C={C} color={j === found.length - 1 && hit ? C.gold : undefined} />)}
      {sum >= 0 && (
        <g opacity={seg(sum, 0, 500) * (1 - seg(sum, LEXI.SUM - 500, LEXI.SUM))}>
          <rect x={220} y={520} width={760} height={150} rx={22} fill={C.card} stroke={C.cardEdge} strokeWidth={2} />
          <UText x={600} y={580} s={`${comma(set.list.length)}가지를 모두 늘어놓았어요`} size={32} weight={800} anchor="middle" C={C} />
          <UText x={600} y={630} s={set.nh ? `그중 영어 낱말 ${set.nh}개: ${set.words.slice(0, 6).join(" · ").toLowerCase()}${set.nh > 6 ? " …" : ""}` : "이번 카드로는 낱말이 없었어요"} size={22} weight={650} anchor="middle" fill={C.soft} C={C} />
        </g>
      )}
      <LexiList C={C} mode={mode} set={set} i={i} />
    </g>
  );
}

/** 오른쪽: 지나온 배열 목록(사전식) */
function LexiList({ C, mode, set, i }) {
  const x = LIST_X, y = 150, w = LIST_W, h = 720;
  const rows = 14, rh = 40;
  const from = Math.max(0, i - rows + 1);
  const items = set.list.slice(from, i + 1);
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <UText x={x + 22} y={y + 38} s={`카드 ${set.cards.length}장${set.r < set.cards.length ? ` 중 ${set.r}장` : ""} · ${set.list.length > 1 && set.list[0] < set.list[1] ? "사전식(오름차순)" : "내림차순"}`} size={18} weight={800} fill={mode === "m" ? C.teal : C.coral} C={C} />
      <MText x={x + 22} y={y + 72} s={countText(set.cards, set.r, mode)} size={18} weight={700} fill={C.ink} C={C} />
      <line x1={x + 22} x2={x + w - 22} y1={y + 90} y2={y + 90} stroke={C.cardEdge} strokeWidth={1.2} />
      {items.map((s, j) => {
        const n = from + j, yy = y + 130 + j * rh;
        const newBlock = n > 0 && s[0] !== set.list[n - 1][0];
        const isCur = n === i, isHit = set.hit[n] === 1;
        return (
          <g key={n}>
            {newBlock && <line x1={x + 22} x2={x + w - 22} y1={yy - 28} y2={yy - 28} stroke={C.gold} strokeWidth={1.6} strokeDasharray="6 5" opacity={0.7} />}
            {isCur && <rect x={x + 14} y={yy - 27} width={w - 28} height={36} rx={9} fill={C.gold} opacity={0.16} />}
            <text x={x + 92} y={yy} textAnchor="end" fontFamily={SANS} fontWeight={700} fontSize={17} fill={C.soft}>{comma(n + 1)}</text>
            <text x={x + 110} y={yy} fontFamily={"'Noto Sans Mono', 'Courier New', monospace"} fontWeight={700} fontSize={24} letterSpacing="0.18em"
              fill={isHit ? C.gold : isCur ? C.ink : C.soft}>{s}</text>
            {isHit && <text x={x + w - 26} y={yy} textAnchor="end" fontFamily={SANS} fontWeight={800} fontSize={15} fill={C.gold}>낱말</text>}
          </g>
        );
      })}
    </g>
  );
}

/* ══════════ 액자 ══════════ */
let CACHE = null;
function useDict() {
  const [d, setD] = useState(CACHE);
  useEffect(() => {
    if (CACHE) return;
    let live = true;
    import("../curio/data-dict.js").then((m) => { CACHE = { DICT: m.DICT, SEEDS: m.SEEDS }; if (live) setD(CACHE); }).catch(() => {});
    return () => { live = false; };
  }, []);
  return d;
}

export function LexiFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, LEXI_DEF, fixLexi);
  const P = lab.prm;
  const D = useDict();
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const at = D ? lexiAt(P, lab.elapsed(), D) : null;
  const nn = P.src === "mine" ? P.text.length : P.n;
  const rOpts = [0, ...Array.from({ length: Math.max(0, nn - 2) }, (_, j) => j + 2)].filter((v) => v === 0 || v < nn);
  const newCards = () => lab.setPrm({ seed: (P.seed % 999983) + 1 });
  const stepIn = (key, list, d) => { const i = list.indexOf(P[key]); const j = clamp(i + d, 0, list.length - 1); if (j !== i) lab.setPrm({ [key]: list[j] }); poke(); };
  const keepRate = (o, n, el) => {          // 빠르기를 바꿔도 같은 배열에서 이어지게
    if (!D) return 0;
    const A = lexiAt(o, el, D);
    let base = 0;
    for (let k = 0; k < A.s; k++) base += setOf(n, k, D).dur;
    const B = setOf(n, A.s, D);
    return base + B.start[Math.min(A.i, B.list.length - 1)];
  };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: newCards, toggleFs, onMode, poke }),
    ArrowUp: () => { const j = LEXI.RATES.indexOf(P.rate) + 1; if (j < LEXI.RATES.length) lab.setPrm({ rate: LEXI.RATES[j] }, keepRate); poke(); },
    ArrowDown: () => { const j = LEXI.RATES.indexOf(P.rate) - 1; if (j >= 0) lab.setPrm({ rate: LEXI.RATES[j] }, keepRate); poke(); },
    ArrowRight: () => stepIn("n", LEXI.NS, 1), ArrowLeft: () => stepIn("n", LEXI.NS, -1),
  }, inert);
  const settings = (
    <>
      <Setting label="카드"><Seg label="카드" value={P.src} options={[["word", "낱말 섞기"], ["abc", "A부터"], ["mine", "직접"]]} onChange={(v) => lab.setPrm({ src: v, r: 0 })} poke={poke} /></Setting>
      {P.src === "mine" ? (
        <Setting label="글자" sep>
          <input className="curio-in" defaultValue={P.text} maxLength={8} aria-label="카드 글자(영문 2~8자)"
            onChange={(e) => { const v = e.target.value.toUpperCase().replace(/[^A-Z]/g, ""); if (v.length >= 2) lab.setPrm({ text: v, r: 0 }); poke(); }}
            onKeyDown={(e) => e.stopPropagation()} />
        </Setting>
      ) : (
        <Setting label="장수" sep><Stepper ui={ui} label="장수" value={P.n} options={LEXI.NS} unit="장" onChange={(v) => lab.setPrm({ n: v, r: 0 })} poke={poke} keyHint={["←", "→"]} /></Setting>
      )}
      <Setting label="늘어놓기" sep><Stepper ui={ui} label="늘어놓기" value={P.r} options={rOpts} fmt={(v) => (v ? `${v}장` : "모두")} onChange={(v) => lab.setPrm({ r: v })} poke={poke} /></Setting>
      <Setting label="순서" sep><Seg label="순서" value={P.ord} options={[["asc", "오름차순"], ["desc", "내림차순"]]} onChange={(v) => lab.setPrm({ ord: v })} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.rate} options={LEXI.RATES} fmt={(v) => `${v}`} unit="장/초" onChange={(v) => lab.setPrm({ rate: v }, keepRate)} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="숨은 낱말" sep><Seg label="숨은 낱말" value={P.hid} options={[[true, "보기"], [false, "끄기"]]} onChange={(v) => lab.setPrm({ hid: v }, (o, n, el) => el)} poke={poke} /></Setting>
    </>
  );
  const title = { e: "알파벳 카드 늘어놓기", m: "알파벳 카드 사전식 배열" };
  const sub = at ? `${at.set.cards.join(" ")} — 모든 순서를 차례로, 낱말이 나오면 사전처럼` : "";
  return (
    <>
      <style>{`.curio-in{width:9.5cqw;font:inherit;font-size:1.5cqw;font-weight:800;letter-spacing:.12em;text-transform:uppercase;padding:.3cqw .6cqw;border-radius:.8cqw;border:1px solid var(--chipbd);background:transparent;color:var(--ink)}`}</style>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="알파벳 카드를 사전식으로 늘어놓는 액자">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <LexiArt C={C} mode={Ly.mode} P={P} at={at} D={D} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={newCards} restartTitle="새 카드"
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={at ? (at.sum >= 0 ? 1 : at.i / Math.max(1, at.set.list.length)) : 0} />
    </>
  );
}

/* 목록 그림 — 낱말 하나를 찾은 순간(사전 없이 그린다) */
const MINI = { DICT: { tears: ["/ˈtɪrz/", "명 눈물 (tear의 복수형)"], rates: ["/ˈreɪts/", "명 비율들 (rate의 복수형)"], stare: ["/ˈstɛr/", "동 빤히 보다"] }, SEEDS: ["stare"] };
export const LexiThumb = memo(function LexiThumb({ C, mode = "m" }) {
  const P = fixLexi({ src: "mine", text: "TEARS", rate: 2, hid: true });
  const at = lexiAt(P, 0, MINI);
  const i = at.set.list.indexOf("STARE");
  const at2 = { ...at, i, t: 900, sum: -1 };
  return <LexiArt C={C} mode={mode} P={P} at={at2} D={MINI} />;
});
