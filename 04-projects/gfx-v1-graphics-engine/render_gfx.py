import asyncio, pathlib, json
from playwright.async_api import async_playwright
BASE = pathlib.Path.home() / "workspace/gfx-v1"
TOTAL = json.load(open(BASE / "gfx_data.json"))["total"]; FPS = 30
OUT = BASE / "frames_gfx"; OUT.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=str(pathlib.Path.home() / ".cache/ms-playwright/chromium-1248/chrome-linux64/chrome"), args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        await pg.goto((BASE / "gfx.html").resolve().as_uri())
        await pg.wait_for_timeout(700)
        n = int(TOTAL * FPS)
        for i in range(n):
            f = OUT / f"f{i:05d}.jpg"
            if f.exists(): continue
            await pg.evaluate(f"window.seek({i / FPS:.4f})")
            await pg.wait_for_timeout(12)
            await pg.screenshot(path=str(f), type="jpeg", quality=88)
        await b.close()
    print("RENDER DONE", n)
asyncio.run(main())
