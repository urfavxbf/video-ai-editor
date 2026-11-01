#!/usr/bin/env python3
"""Compose the 1920x1080 Video AI Editor showreel.

Each scene = one real FxPreview render (or the generated sample take for intro/how-to/outro) in a 9:16 screen,
UrFavXBF + PIX approved pixel poses on stage, the exact cut-list / CLI usage typed on a code card, captions,
Chatterbox dialogue, the effect's own SFX, and an RGB/pixel-slice glitch at every scene boundary.
Character bounce follows the measured RMS of the real Chatterbox WAV (this is not lip-sync).
"""
from __future__ import annotations
import argparse, json, math, random, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1920, 1080, 30
LEAD, TAIL = 8, 16
GREEN = (57, 255, 136); CYAN = (90, 220, 255); PINK = (255, 120, 200); LAV = (170, 140, 255)
INK = (14, 22, 30); PAPER = (240, 252, 246)
PANEL = (1302, 72, 526, 936)  # x, y, w, h  (9:16)

def font(paths, size, variation=None):
    for p in paths:
        try:
            f = ImageFont.truetype(str(p), size)
            if variation:
                try: f.set_variation_by_name(variation)
                except Exception: pass
            return f
        except Exception:
            continue
    return ImageFont.load_default()

class Fonts:
    def __init__(self, root: Path):
        mont, inter = root / "public/fonts/Montserrat.ttf", root / "public/fonts/Inter.ttf"
        bold = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        reg = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
        mono = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
        self.display = font([mont] + bold, 92, "ExtraBold")
        self.display_xl = font([mont] + bold, 132, "Black")
        self.sub = font([mont] + bold, 40, "SemiBold")
        self.pill = font([inter] + bold, 26, "Bold")
        self.cap = font([inter] + reg, 34, "Medium")
        self.cap_b = font([inter] + bold, 30, "Bold")
        self.mono = font(mono, 27)

# ---------- assets ----------
def load_poses(chars: Path, who: str, height: int, names):
    out = {}
    for n in names:
        p = chars / who / f"{n}.png"
        if not p.exists():
            continue
        im = Image.open(p).convert("RGBA")
        im = im.crop(im.getchannel("A").getbbox())
        r = height / im.height
        out[n] = im.resize((max(1, int(im.width * r)), height), Image.NEAREST)
    if "idle" not in out:
        raise SystemExit(f"missing approved {who} poses in {chars}")
    return out

def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255); return m

def make_background():
    g = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    top = np.array([10, 30, 26]); bot = np.array([28, 14, 52])
    base = (top * (1 - g[..., None]) + bot * g[..., None]) + (np.array([0, 10, 18]) * x[..., None])
    base = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    blobs = Image.new("RGBA", (W + 600, H + 600), (0, 0, 0, 0))
    d = ImageDraw.Draw(blobs)
    for (cx, cy, r, c, a) in [(420, 520, 420, GREEN, 60), (1500, 420, 380, LAV, 70), (900, 1100, 460, CYAN, 40),
                              (1800, 1100, 300, PINK, 45), (200, 1150, 260, CYAN, 35)]:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*c, a))
    blobs = blobs.filter(ImageFilter.GaussianBlur(120))
    return base, blobs

def panel_frame():
    x, y, w, h = PANEL
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.rounded_rectangle((x - 14, y - 14, x + w + 14, y + h + 14), 40, fill=(*GREEN, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    d = ImageDraw.Draw(glow)
    d.rounded_rectangle((x - 8, y - 8, x + w + 8, y + h + 8), 36, fill=(8, 12, 14, 255), outline=(*GREEN, 255), width=4)
    return glow, rounded_mask(w, h, 28)

# ---------- media ----------
class Reader:
    """Sequential raw-frame reader; holds the last frame when the source ends."""
    def __init__(self, path: Path, start=0, loop=False):
        x, y, w, h = PANEL
        args = ["ffmpeg", "-v", "error"] + (["-stream_loop", "-1"] if loop else []) + ["-i", str(path),
                "-vf", f"select=gte(n\\,{start}),setpts=N/FRAME_RATE/TB,scale={w}:{h}:flags=bicubic", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        self.p = subprocess.Popen(args, stdout=subprocess.PIPE)
        self.size = w * h * 3; self.last = None; self.wh = (w, h)
    def next(self):
        b = self.p.stdout.read(self.size)
        if len(b) == self.size:
            self.last = Image.frombuffer("RGB", self.wh, b, "raw", "RGB", 0, 1)
        return self.last if self.last is not None else Image.new("RGB", self.wh, (0, 0, 0))
    def close(self):
        try: self.p.stdout.close(); self.p.kill()
        except Exception: pass

def probe_frames(p: Path) -> int:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0",
                                   "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(p)], text=True)
    return int(out.strip().split(",")[0])

def has_audio(p: Path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout.strip()
    return bool(out)

# ---------- drawing helpers ----------
def wrap(draw, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def glitch(frame: Image.Image, k: int, seed: int) -> Image.Image:
    """Intentional RGB / pixel-slice glitch for the first frames of a scene."""
    strength = (1 - k / 8) ** 1.5
    if strength <= 0: return frame
    a = np.asarray(frame).copy(); rnd = random.Random(seed * 131 + k)
    for _ in range(int(14 * strength) + 2):
        y0 = rnd.randrange(0, H - 8); hh = rnd.randrange(6, 70)
        a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], int(rnd.randrange(-90, 90) * strength), axis=1)
    off = int(18 * strength)
    if off:
        a[..., 0] = np.roll(a[..., 0], off, axis=1); a[..., 2] = np.roll(a[..., 2], -off, axis=1)
    # chunky pixel blocks
    if strength > 0.5:
        small = Image.fromarray(a).resize((W // 24, H // 24), Image.NEAREST).resize((W, H), Image.NEAREST)
        a = (np.asarray(small) * 0.35 + a * 0.65).astype(np.uint8)
    return Image.fromarray(a)

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--script", type=Path, default=Path("showreel/script.json"))
    ap.add_argument("--voices", type=Path, default=Path("out/showreel/voice"))
    ap.add_argument("--fx", type=Path, default=Path("out/showreel/fx"))
    ap.add_argument("--take", type=Path, default=Path("public/sample/take.mp4"))
    ap.add_argument("--chars", type=Path, default=Path("public/characters/pixel-default"))
    ap.add_argument("--out", type=Path, default=Path("out/showreel/Video_AI_Editor_Showreel.mp4"))
    ap.add_argument("--limit", type=int, default=0, help="debug: only first N scenes")
    a = ap.parse_args()
    spec = json.loads(a.script.read_text())
    scenes = spec["scenes"][: a.limit or None]
    vmeta = {l["n"]: l for l in json.loads((a.voices / "voices.json").read_text())["lines"]}
    fxman = {m["id"]: m for m in json.loads((a.fx / "manifest.json").read_text())} if (a.fx / "manifest.json").exists() else {}
    F = Fonts(a.root)
    host = load_poses(a.chars, "urfavxbf", 420, ["idle", "talk", "point_camera", "point_side", "happy", "surprised"])
    pix = load_poses(a.chars, "pix", 285, ["idle", "curious", "talk", "point", "happy", "question", "surprised"])
    base, blobs = make_background(); pglow, pmask = panel_frame()
    take_frames = probe_frames(a.take)

    # timeline
    timeline, at = [], 0
    for s in scenes:
        v = vmeta[s["n"]]; vf = math.ceil(v["seconds"] * FPS)
        clip = a.fx / fxman[s["id"]]["file"] if s["kind"] == "fx" else None
        cf = probe_frames(clip) if clip else 0
        frames = max(cf, LEAD + vf + TAIL, 54)
        timeline.append(dict(scene=s, start=at, frames=frames, clip=clip, clipFrames=cf, voiceFrames=vf, voice=v))
        at += frames
    total = at
    a.out.parent.mkdir(parents=True, exist_ok=True)
    silent = a.out.with_name(a.out.stem + ".video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-an", str(silent)],
                           stdin=subprocess.PIPE)
    contact = []
    g = 0
    for ti, item in enumerate(timeline):
        s, n = item["scene"], item["frames"]
        reader = Reader(item["clip"]) if item["clip"] else Reader(a.take, start=(ti * 37) % max(1, take_frames - 1), loop=True)
        rms = item["voice"]["rms"]
        speaker = s["speaker"]
        if s["kind"] == "fx":
            code = ["// src/edit/edit.json  -> segments[]", f'{{ "kind": "fx", "id": "{s["id"]}",', f'  "at": 10, "frames": {fxman[s["id"]]["frames"]} }}']
        else:
            code = s.get("code", [])
        code_chars = sum(len(c) for c in code)
        for f in range(n):
            t = (g + f) / FPS
            img = base.copy()
            img.alpha_composite(blobs.crop((int(300 + 120 * math.sin(t * .23)), int(300 + 90 * math.cos(t * .19)),
                                            int(300 + 120 * math.sin(t * .23)) + W, int(300 + 90 * math.cos(t * .19)) + H)))
            d = ImageDraw.Draw(img, "RGBA")
            # --- screen panel with the real render
            img.alpha_composite(pglow)
            px, py, pw, ph = PANEL
            img.paste(reader.next(), (px, py), pmask)
            # --- header
            appear = ease(f / 12)
            hx = 96 - int(40 * (1 - appear))
            if s["kind"] == "fx":
                tag = f"EFFECT {s['index']:02d} / 33   ·   {s['group'].upper()}"
                tw = d.textlength(tag, font=F.pill)
                d.rounded_rectangle((hx, 64, hx + tw + 40, 112), 24, fill=(*GREEN, int(235 * appear)))
                d.text((hx + 20, 73), tag, font=F.pill, fill=(*INK, int(255 * appear)))
                d.text((hx, 124), s["name"].upper(), font=F.display, fill=(*PAPER, int(255 * appear)))
            else:
                big = F.display_xl if s["kind"] in ("intro", "outro") else F.display
                while d.textlength(s["title"], font=big) > 1120 and big.size > 48:
                    big = big.font_variant(size=big.size - 4)
                d.text((hx, 70), s["title"], font=big, fill=(*PAPER, int(255 * appear)))
                if s.get("subtitle"):
                    d.text((hx + 4, 70 + int(big.size * 1.12)), s["subtitle"], font=F.sub, fill=(*GREEN, int(255 * appear)))
            # --- caption (speaker line), revealed with the voice timeline
            vf = item["voiceFrames"]; local = f - LEAD
            if local >= -2:
                capy = 262 if s["kind"] == "fx" or not s.get("subtitle") else 300
                if s["kind"] in ("intro", "outro"): capy = 330
                ctext = s.get("caption", s["text"])
                words = ctext.split()
                shown = len(words) if local >= vf else max(1, math.ceil(len(words) * max(0, local) / max(1, vf)))
                lines = wrap(d, ctext, F.cap, 1060)
                who = "UrFavXBF" if speaker == "host" else "PIX"
                col = GREEN if speaker == "host" else CYAN
                bh = 22 + 44 * len(lines) + 26
                d.rounded_rectangle((96, capy, 1200, capy + bh), 22, fill=(8, 14, 18, 200), outline=(*col, 200), width=2)
                d.text((122, capy + 12), who, font=F.cap_b, fill=col)
                cnt = 0
                for li, line in enumerate(lines):
                    lw = line.split(); vis = lw[: max(0, shown - cnt)]; cnt += len(lw)
                    d.text((122, capy + 52 + 44 * li), " ".join(vis), font=F.cap, fill=PAPER)
                code_y = capy + bh + 22
            else:
                code_y = 460
            # --- code card, typed on
            if code:
                typed = int(max(0, f - 6) * 3.2)
                ch = 26 + 36 * len(code) + 16
                cw = 1104
                d.rounded_rectangle((96, code_y, 96 + cw, code_y + ch), 18, fill=(6, 10, 12, 235), outline=(255, 255, 255, 40), width=2)
                for i2, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
                    d.ellipse((116 + 26 * i2, code_y + 12, 130 + 26 * i2, code_y + 26), fill=c)
                left = typed
                for li, line in enumerate(code):
                    part = line[: max(0, left)]; left -= len(line)
                    colr = (140, 160, 170) if line.startswith("//") else (GREEN if line.startswith("$") else (230, 240, 236))
                    d.text((120, code_y + 34 + 36 * li), part, font=F.mono, fill=colr)
            # --- characters (approved pose PNGs), RMS-driven bounce for the speaker
            e = rms[min(len(rms) - 1, max(0, local))] if 0 <= local < len(rms) else 0.0
            talking = 0 <= local < vf
            hp = s["hostPose"] if (speaker != "host" or talking or f < LEAD) else ("happy" if s["kind"] != "fx" else s["hostPose"])
            pp = s["pixPose"]
            himg = host.get(hp, host["idle"]); pimg = pix.get(pp, pix["idle"])
            hb = (e * 16 if speaker == "host" else 0) + 6 * math.sin(t * 2.2)
            pb = (e * 18 if speaker == "pix" else 0) + 8 * math.sin(t * 2.7 + 1)
            enter = ease((f + 4) / 14) if ti == 0 else 1
            hx0 = 70 - int(300 * (1 - enter)); hy0 = H - himg.height - 18 - int(hb)
            # shadow
            d.ellipse((hx0 + 60, H - 40, hx0 + himg.width - 60, H - 8), fill=(0, 0, 0, 90))
            img.alpha_composite(himg, (hx0, hy0))
            pxp = 1000; pyp = H - pimg.height - 22 - int(pb)
            d.ellipse((pxp + 40, H - 36, pxp + pimg.width - 40, H - 10), fill=(0, 0, 0, 90))
            img.alpha_composite(pimg, (pxp, pyp))
            frame = img.convert("RGB")
            if f < 8 and ti > 0:
                frame = glitch(frame, f, s["n"])
            enc.stdin.write(frame.tobytes())
            if f == min(n - 1, LEAD + vf // 2):
                contact.append(frame.resize((480, 270)))
        reader.close()
        g += n
        print(f"composed scene {ti + 1}/{len(timeline)} ({n} frames)", flush=True)
    enc.stdin.close()
    if enc.wait() != 0: raise SystemExit("video encode failed")

    # ---------- audio: Chatterbox dialogue + each effect's own SFX ----------
    inputs, filters, labels = [], [], []
    for item in timeline:
        k = len(inputs) // 2
        inputs += ["-i", str(a.voices / item["voice"]["file"])]
        ms = int((item["start"] + LEAD) * 1000 / FPS)
        filters.append(f"[{k}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms},volume=1.0[v{k}]"); labels.append(f"[v{k}]")
        if item["clip"] and has_audio(item["clip"]):
            k = len(inputs) // 2
            inputs += ["-i", str(item["clip"])]
            ms = int(item["start"] * 1000 / FPS)
            filters.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume=0.45[s{k}]"); labels.append(f"[s{k}]")
    dur = total / FPS
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,atrim=0:{dur:.3f},apad=whole_dur={dur:.3f},alimiter=limit=0.89[mix]")
    fc = a.out.with_name("audio-filter.txt"); fc.write_text(";\n".join(filters))
    mixwav = a.out.with_name(a.out.stem + ".mix.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex_script", str(fc), "-map", "[mix]", "-ac", "2", "-ar", "48000", str(mixwav)], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(mixwav), "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(a.out)], check=True)
    silent.unlink(missing_ok=True); mixwav.unlink(missing_ok=True)
    # contact sheet
    cols = 6; rows = math.ceil(len(contact) / cols)
    sheet = Image.new("RGB", (cols * 488 + 8, rows * 278 + 8), (20, 24, 28))
    for i, c in enumerate(contact):
        sheet.paste(c, (8 + (i % cols) * 488, 8 + (i // cols) * 278))
    sheet.save(a.out.with_name("contact-sheet.jpg"), quality=86)
    json.dump({"frames": total, "seconds": round(dur, 2), "scenes": [{k: (str(v) if isinstance(v, Path) else v) for k, v in it.items() if k not in ("scene", "voice")} | {"n": it["scene"]["n"], "kind": it["scene"]["kind"], "id": it["scene"].get("id")} for it in timeline]},
              open(a.out.with_name("timeline.json"), "w"), indent=1)
    print(f"DONE {a.out} {total} frames {dur:.1f}s")

if __name__ == "__main__":
    main()
