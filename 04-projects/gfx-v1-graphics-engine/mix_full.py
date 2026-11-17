import wave, json, subprocess, pathlib
import numpy as np
BASE = pathlib.Path.home() / "workspace/gfx-v1"
SFX = pathlib.Path.home() / "workspace/sfx-library/drive-bundle"
DATA = json.load(open(BASE / "gfx_full_data.json")); SR = 48000
def read_any(p):
    w = BASE / f".cache_{pathlib.Path(p).stem}.wav"
    if not w.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(p), "-ar", "48000", "-ac", "1", str(w)], check=True)
    with wave.open(str(w), "rb") as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
total = DATA["total"]; mix = np.zeros(int(total * SR) + SR // 4, dtype=np.float32)
def place(p, at, vol=1.0, trim=None):
    a = read_any(p)
    if trim: a = a[:int(trim * SR)]
    i = int(at * SR); n = min(len(a), len(mix) - i)
    if n > 0: mix[i:i + n] += a[:n] * vol
for l in DATA["lines"]:
    place(BASE / "proc" / f"{l['id']}.wav", l["start"], 1.0)
for l in DATA["lines"][1:]:
    place(SFX / "Short Whoosh.mp3", l["start"] - 0.05, 0.26, 0.8)
V6, V7, V8 = DATA["lines"][5], DATA["lines"][6], DATA["lines"][7]
for fr in (0.42, 0.62, 0.82):
    place(SFX / "Pop 1.mp3", V6["start"] + V6["dur"] * fr, 0.16, 0.3)
for w in V7["words"]:
    if w["w"].lower() in ("upload", "captions", "style"):
        place(SFX / "Pop 1.mp3", w["s"], 0.18, 0.3)
for w in V8["words"]:
    if w["w"] == "TOOL":
        place(SFX / "Pop 1.mp3", w["s"] + 0.5, 0.2, 0.3)
with wave.open(str(BASE / "mix_full_raw.wav"), "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(BASE / "mix_full_raw.wav"), "-af",
                "alimiter=limit=0.70:level=false,loudnorm=I=-14.5:TP=-1.5:LRA=11,alimiter=limit=0.60:level=false,volume=1.2dB",
                str(BASE / "audio_full.wav")], check=True)
print("mix done")
