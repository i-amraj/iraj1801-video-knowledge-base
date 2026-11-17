import wave, json, subprocess, pathlib, shutil
import numpy as np
BASE = pathlib.Path.home() / "workspace/gfx-v1"
SCRIPT = {"V1": "Ye captions maine haath se NAHI likhe!",
          "V2": "Ek free tool tumhari awaaz sunke, khud word-by-word captions bana deta hai.",
          "V3": "Step ek, bas apni video upload karo.",
          "V4": "Step do, tool khud sunega, aur har shabd ko sahi jagah par bitha dega.",
          "V5": "Step teen, font aur rang apne style se badal lo.",
          "V6": "Aur ye raha final result, bilkul professional captions, ek bhi shabd haath se nahi likha.",
          "V7": "Teen steps yaad kar lo: upload, auto captions, style.",
          "V8": "Tool ka naam aur link chahiye? Comment me TOOL likho, mera agent bhej dega. Follow kar lena, main Raj."}
ORDER = ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]
proc = BASE / "proc"; proc.mkdir(exist_ok=True)
def trim_tempo(src, dst):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af",
                    "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo=1.18",
                    str(dst)], check=True)
def read_wav(p):
    with wave.open(str(p), "rb") as w:
        n, ch, sr = w.getnframes(), w.getnchannels(), w.getframerate()
        d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    return (d.reshape(-1, ch).mean(axis=1) if ch > 1 else d), sr
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
lines = []; t = 0.15
for lid in ORDER:
    dst = proc / f"{lid}.wav"
    if lid == "V1":
        shutil.copy(pathlib.Path.home() / "workspace/duo-v2/proc/H1.wav", dst)
    else:
        trim_tempo(BASE / "vo" / f"{lid}.wav", dst)
    audio, sr = read_wav(dst); dur = len(audio) / sr
    win = int(0.05 * sr); env = []
    for i in range(0, len(audio), win):
        seg = audio[i:i + win]
        env.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
    peak = np.percentile(env, 95) if env else 1.0
    env = [round(min(1.0, e / (peak * 0.92 + 1e-9)), 3) for e in env]
    a16 = audio[::3].astype(np.float32) if sr == 48000 else audio.astype(np.float32)
    segs, _ = model.transcribe(a16, language="hi", word_timestamps=True, beam_size=1, vad_filter=False)
    aw = [{"s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in (s.words or [])]
    swords = SCRIPT[lid].replace(",", " ").replace(".", " ").replace("!", " ").split()
    # word times: ASR anchors if counts match, else proportional over env-active span
    a, b = 0, len(env) - 1
    while a < b and env[a] < 0.08: a += 1
    while b > a and env[b] < 0.08: b -= 1
    t0, t1 = a * 0.05, max(b * 0.05, a * 0.05 + 0.3)
    words = []
    if len(aw) == len(swords):
        for wtxt, wt in zip(swords, aw):
            words.append({"w": wtxt, "s": round(t + wt["s"], 2), "e": round(t + wt["e"], 2)})
    else:
        lens = [len(w) + 1 for w in swords]; tot = sum(lens); acc = 0
        for wtxt, L in zip(swords, lens):
            s_ = t + t0 + (t1 - t0) * acc / tot; acc += L
            words.append({"w": wtxt, "s": round(s_, 2), "e": round(t + t0 + (t1 - t0) * acc / tot, 2)})
    lines.append({"id": lid, "text": SCRIPT[lid], "start": round(t, 2), "dur": round(dur, 2), "env": env, "words": words})
    print(lid, "start", round(t, 2), "dur", round(dur, 2), "words", len(words), "asr", len(aw))
    t += dur + 0.32
total = round(t - 0.32 + 0.45, 2)
json.dump({"lines": lines, "total": total}, open(BASE / "gfx_full_data.json", "w"), ensure_ascii=False, indent=1)
print("TOTAL", total)
