import asyncio, pathlib, sys
from playwright.async_api import async_playwright
BASE = pathlib.Path.home() / "workspace/gfx-v1"
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=str(pathlib.Path.home() / ".cache/ms-playwright/chromium-1248/chrome-linux64/chrome"), args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        await pg.goto((BASE / "gfx.html").resolve().as_uri())
        await pg.wait_for_timeout(700)
        for ts in sys.argv[1:]:
            await pg.evaluate(f"window.seek({ts})")
            await pg.wait_for_timeout(90)
            await pg.screenshot(path=str(BASE / f"gst_{ts}.png"))
        await b.close()
    print("stills done")
asyncio.run(main())
