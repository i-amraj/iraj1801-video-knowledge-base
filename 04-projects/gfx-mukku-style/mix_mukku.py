import subprocess, pathlib, json
BASE = pathlib.Path.home() / "workspace/gfx-mukku"
PROC = pathlib.Path.home() / "workspace/gfx-v1/proc"
SFX = pathlib.Path.home() / "workspace/sfx-library/drive-bundle"
DATA = json.load(open(pathlib.Path.home() / "workspace/gfx-v1/gfx_full_data.json"))
lines = DATA["lines"][:4]
def run(cmd): subprocess.run(cmd, check=True)
# 1) silent video from frames @60fps
run(["ffmpeg", "-y", "-v", "error", "-framerate", "60", "-i", str(BASE / "frames/f%04d.jpg"),
     "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "60", str(BASE / "video_silent.mp4")])
# 2) audio: VO lines at their starts + soft pops
inputs, filters, labels = [], [], []
for i, L in enumerate(lines):
    inputs += ["-i", str(PROC / f"V{i+1}.wav")]
    d = int(L["start"] * 1000)
    filters.append(f"[{i}:a]aresample=48000,adelay={d}|{d}[v{i}]"); labels.append(f"[v{i}]")
pop = SFX / "Pop 1.mp3"
pop_times = [2.95, 3.3, 3.62, 4.35, 4.95, 5.6, 6.15] + [w["s"] for w in lines[3]["words"][6:]]
for j, t in enumerate(pop_times):
    inputs += ["-i", str(pop)]
    idx = 4 + j; d = int(t * 1000)
    filters.append(f"[{idx}:a]aresample=48000,volume=0.35,adelay={d}|{d}[p{j}]"); labels.append(f"[p{j}]")
filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0[mx]")
filters.append("[mx]alimiter=limit=0.45:level=false,volume=2.2dB,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
     "-map", "[aout]", "-t", "15", "-ar", "48000", str(BASE / "audio_mukku.wav")])
# 3) mux
OUT = pathlib.Path.home() / "workspace/your_files/raj-captions-reel-mukku-style-15s.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", str(BASE / "video_silent.mp4"), "-i", str(BASE / "audio_mukku.wav"),
     "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", "15", str(OUT)])
run(["ffmpeg", "-y", "-v", "error", "-ss", "1.2", "-i", str(OUT), "-frames:v", "1", "-q:v", "3",
     str(pathlib.Path.home() / "workspace/your_files/raj-captions-reel-mukku-style-15s-cover.jpg")])
print("MUXED", OUT)
