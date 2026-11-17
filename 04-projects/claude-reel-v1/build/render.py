import asyncio, pathlib, subprocess, json
from playwright.async_api import async_playwright
B = pathlib.Path.cwd()
TOTAL = json.loads((B / "data.json").read_text())["total"]
FPS = 60
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=str(pathlib.Path.home() / ".cache/ms-playwright/chromium-1248/chrome-linux64/chrome"),
                                    args=["--force-color-profile=srgb", "--disable-lcd-text"])
        fr = B / "frames"; fr.mkdir(exist_ok=True)
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        await pg.goto("file://" + str(B / "reel.html")); await pg.wait_for_timeout(900)
        for i in range(int(FPS * TOTAL)):
            out = fr / f"f{i:04d}.jpg"
            if out.exists(): continue
            await pg.evaluate(f"window.seek({i / FPS:.4f})")
            await pg.screenshot(path=str(out), type="jpeg", quality=88)
        await pg.close(); await b.close()
asyncio.run(main())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "60", "-i", str(B / "frames/f%04d.jpg"),
                "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-r", "60", str(B / "silent.mp4")], check=True)
out = pathlib.Path.home() / "workspace/your_files/raj-claude-vs-free-tool-reel-v1.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(B / "silent.mp4"), "-i", str(B.parent / "vo/vo_final.wav"),
                "-filter_complex", "[1:a]aresample=48000,apad,atrim=0:" + str(TOTAL) + ",loudnorm=I=-14:TP=-2.0:LRA=11[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL), str(out)], check=True)
r = subprocess.run(["ffmpeg", "-i", str(out), "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True)
import re
m = re.search(r'"input_i" : "([-\d.]+)".*?"input_tp" : "([-\d.]+)"', r.stderr, re.S)
print("FINAL LUFS:", m.group(1), "TP:", m.group(2), "| TOTAL:", TOTAL)
