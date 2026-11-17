import subprocess, wave
import numpy as np
from faster_whisper import WhisperModel
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "/home/hatch/workspace/your_files/raj-captions-reel-graphics-v1.mp4", "-ar", "16000", "-ac", "1", "/tmp/qcg.wav"], check=True)
with wave.open("/tmp/qcg.wav", "rb") as w:
    d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(d, language="hi", beam_size=1)
for s in segs: print(f"{s.start:5.2f}-{s.end:5.2f}  {s.text.strip()}")
