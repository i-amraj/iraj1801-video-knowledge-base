#!/usr/bin/env python3
"""Khir-khir surgery on vo_full.wav.pcm: silence noisy word-free gaps, cut tail burst,
soxr resample to 48k, gentle peak cap -> vo_final.wav. Re-measures all gaps at the end."""
import numpy as np, json, subprocess, pathlib

VO = pathlib.Path(__file__).parent
sr = 24000
pcm = np.frombuffer((VO / "vo_full.wav.pcm").read_bytes(), dtype=np.int16).astype(np.float32) / 32768.0
words = json.loads((VO / "words.json").read_text())
last_end = words[-1]["e"]

# cut tail: keep up to last word end + 0.10s (tail noise burst sits right after speech)
cut = min(len(pcm), int((last_end + 0.10) * sr))
pcm = pcm[:cut].copy()
print("cut at", round(cut / sr, 2), "s (last word ends", last_end, ")")

# detect gaps >= 0.25s (10ms windows, rms<=0.02 or chaotic = non-speech)
w = int(sr * 0.01); n = len(pcm) // w
seg = pcm[:n * w].reshape(n, w)
rms = np.sqrt(np.mean(seg ** 2, axis=1))
chaos = np.mean(np.abs(np.diff(np.sign(seg), axis=1)) > 0, axis=1)
speech = (rms > 0.02) & (chaos < 0.35)
gaps = []
run = 0; start = 0
for i in range(n):
    if not speech[i]:
        if run == 0: start = i
        run += 1
    else:
        if run >= 25: gaps.append((start, start + run))
        run = 0
if run >= 25: gaps.append((start, start + run))

def word_overlap(g0, g1):
    for wd in words:
        if wd["s"] < g1 - 0.04 and wd["e"] > g0 + 0.04:
            return True
    return False

fixed = []
for (a, b) in gaps:
    g0, g1 = a * 0.01, b * 0.01
    grms = float(np.sqrt(np.mean(seg[a:b] ** 2)))
    if grms > 0.008 and not word_overlap(g0, g1):
        # zero the interior, keep 40ms edges
        i0 = int((g0 + 0.04) * sr); i1 = int((g1 - 0.04) * sr)
        if i1 > i0:
            pcm[i0:i1] = 0.0
            fixed.append((round(g0, 2), round(g1, 2), round(grms, 4)))
print("silenced gaps:", fixed)

# write 24k wav -> soxr resample + peak cap via ffmpeg
import wave
with wave.open(str(VO / "vo_cut24.wav"), "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes((np.clip(pcm, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(VO / "vo_cut24.wav"),
                "-af", "aresample=48000:resampler=soxr,alimiter=limit=0.7:level=false",
                str(VO / "vo_final.wav")], check=True)

# re-measure gaps on the final file
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(VO / "vo_final.wav"), "-ac", "1", "-ar", "48000", str(VO / "vo_check.wav")], check=True)
with wave.open(str(VO / "vo_check.wav"), "rb") as wf:
    a = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
sr2 = 48000; w2 = int(sr2 * 0.01); n2 = len(a) // w2
seg2 = a[:n2 * w2].reshape(n2, w2)
rms2 = np.sqrt(np.mean(seg2 ** 2, axis=1))
speech2 = rms2 > 0.02
worst = []
run = 0; start = 0
for i in range(n2):
    if not speech2[i]:
        if run == 0: start = i
        run += 1
    else:
        if run >= 25: worst.append((round(start * 0.01, 2), round(float(np.sqrt(np.mean(seg2[start:start + run] ** 2))), 4)))
        run = 0
print("final gaps >=0.25s (start, rms):", worst)
print("max gap rms:", max([g[1] for g in worst], default=0))
print("final dur:", round(len(a) / sr2, 2))
