import asyncio, pathlib
from playwright.async_api import async_playwright
BASE = pathlib.Path.home() / "workspace/gfx-mukku"
FR = BASE / "frames"; FR.mkdir(exist_ok=True)
FPS, TOTAL = 60, 15.0
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=str(pathlib.Path.home() / ".cache/ms-playwright/chromium-1248/chrome-linux64/chrome"),
                                    args=["--force-color-profile=srgb", "--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        await pg.goto("file://" + str(BASE / "mukku.html"))
        await pg.wait_for_timeout(600)
        n = int(FPS * TOTAL)
        for i in range(n):
            out = FR / f"f{i:04d}.jpg"
            if out.exists(): continue
            await pg.evaluate(f"window.seek({i / FPS:.4f})")
            await pg.screenshot(path=str(out), type="jpeg", quality=88)
            if i % 180 == 0: print("frame", i, flush=True)
        await b.close()
asyncio.run(main())
print("render done")
