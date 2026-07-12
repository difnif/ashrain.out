// 리브드 글라스 필터 코어 — 결정론적, 온디바이스, Canvas 2D
// 스튜디오에서 검증: 300x400 기준 23ms, 동일 입력 → 동일 출력

export const PRESETS = {
  pink:  { name: "핑크 매직",   shadow: [86, 30, 74],  highlight: [255, 219, 235], glow: "rgba(255,182,213,.35)", bg: ["#F3D7E6", "#C9A0BC"] },
  gray:  { name: "그레이 레인", shadow: [40, 44, 52],  highlight: [229, 233, 240], glow: "rgba(180,195,215,.30)", bg: ["#E5E9F0", "#B9C1CC"] },
  green: { name: "시그널 그린", shadow: [10, 58, 44],  highlight: [216, 245, 227], glow: "rgba(80,220,150,.28)",  bg: ["#DDF3E6", "#9FC9B2"] },
  amber: { name: "애쉬 옐로",   shadow: [56, 48, 18],  highlight: [255, 240, 190], glow: "rgba(255,220,90,.30)",  bg: ["#F7EFD8", "#CBBD92"] },
};

function ribHash(i) {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return (x - Math.floor(x)) * 2 - 1;
}

export function applyRibbedGlass(srcCanvas, params = {}) {
  const { ribWidth = 14, strength = 10, preBlur = 2, preset = "pink" } = params;
  const W = srcCanvas.width, H = srcCanvas.height;
  const p = PRESETS[preset] || PRESETS.pink;

  const blurred = document.createElement("canvas");
  blurred.width = W; blurred.height = H;
  const bctx = blurred.getContext("2d");
  bctx.filter = `blur(${preBlur}px)`;
  bctx.drawImage(srcCanvas, 0, 0);
  bctx.filter = "none";

  const out = document.createElement("canvas");
  out.width = W; out.height = H;
  const octx = out.getContext("2d");
  const fine = Math.max(3, ribWidth / 3);
  for (let x = 0; x < W; x++) {
    const rib = Math.floor(x / ribWidth);
    const u = (x % ribWidth) / ribWidth;
    const uf = (x % fine) / fine;
    const off = strength * Math.sin(2 * Math.PI * u)
      + strength * 0.35 * Math.sin(2 * Math.PI * uf)
      + ribHash(rib) * strength * 0.5;
    const sx = Math.min(W - 1, Math.max(0, Math.round(x + off)));
    octx.drawImage(blurred, sx, 0, 1, H, x, 0, 1, H);
  }

  const fctx = out.getContext("2d");
  fctx.filter = "blur(0.6px)"; fctx.drawImage(out, 0, 0); fctx.filter = "none";

  const img = fctx.getImageData(0, 0, W, H);
  const d = img.data;
  const [sr, sg, sb] = p.shadow, [hr, hg, hb] = p.highlight;
  for (let i = 0; i < d.length; i += 4) {
    let t = (0.2126 * d[i] + 0.7152 * d[i+1] + 0.0722 * d[i+2]) / 255;
    t = t * t * (3 - 2 * t);
    d[i] = sr + (hr - sr) * t; d[i+1] = sg + (hg - sg) * t; d[i+2] = sb + (hb - sb) * t;
  }
  fctx.putImageData(img, 0, 0);

  const glow = fctx.createRadialGradient(W/2, H*0.32, H*0.05, W/2, H*0.45, H*0.75);
  glow.addColorStop(0, p.glow); glow.addColorStop(1, "rgba(0,0,0,0)");
  fctx.fillStyle = glow; fctx.fillRect(0, 0, W, H);
  const vig = fctx.createRadialGradient(W/2, H/2, H*0.35, W/2, H/2, H*0.85);
  vig.addColorStop(0, "rgba(0,0,0,0)"); vig.addColorStop(1, "rgba(0,0,0,.22)");
  fctx.fillStyle = vig; fctx.fillRect(0, 0, W, H);

  fctx.globalAlpha = 0.10; fctx.fillStyle = "#FFFFFF";
  for (let x = 0; x < W; x += ribWidth) fctx.fillRect(x + Math.round(ribWidth * 0.15), 0, 1, H);
  fctx.globalAlpha = 1;

  return out;
}
