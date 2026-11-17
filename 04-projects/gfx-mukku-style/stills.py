import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = pathlib.Path.home() / "workspace/gfx-mukku"
TIMES = [float(x) for x in sys.argv[1:]] or [0.9, 2.2, 4.6, 6.9, 8.9, 12.6, 14.6]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=str(pathlib.Path.home() / ".cache/ms-playwright/chromium-1248/chrome-linux64/chrome"),
                                    args=["--force-color-profile=srgb", "--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        await pg.goto("file://" + str(BASE / "mukku.html"))
        await pg.wait_for_timeout(600)
        for t in TIMES:
            await pg.evaluate(f"window.seek({t})")
            await pg.wait_for_timeout(60)
            await pg.screenshot(path=str(BASE / f"st_{t}.png"))
        await b.close()
asyncio.run(main())
print("stills done")
