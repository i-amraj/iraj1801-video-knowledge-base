#!/usr/bin/env python3
"""Playwright seek-renderer for the glass comp (HyperFrames engine too slow on this VM).
Usage: render_pw.py <start_frame> <end_frame>   (50fps, frames -> claude-reel-v2/frames50/)
Resumable: existing frames are skipped.
"""
import sys, asyncio, pathlib, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.async_api import async_playwright

ROOT = pathlib.Path('/home/hatch/workspace/claude-reel-v2')
OUT = ROOT / 'frames50'
OUT.mkdir(exist_ok=True)
FPS = 50
TOTAL_FRAMES = 2960  # 59.2s * 50
PORT = 8931

def serve():
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(ROOT / 'film'))
    ThreadingHTTPServer(('127.0.0.1', PORT), handler).serve_forever()

threading.Thread(target=serve, daemon=True).start()

async def main():
    f0, f1 = int(sys.argv[1]), int(sys.argv[2])
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            executable_path='/home/hatch/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome',
            args=['--force-color-profile=srgb', '--disable-lcd-text'])
        page = await browser.new_page(viewport={'width': 1080, 'height': 1920},
                                      device_scale_factor=1)
        await page.goto(f'http://127.0.0.1:{PORT}/index.html')
        await page.wait_for_timeout(2500)
        ok = await page.evaluate("() => !!(window.__timelines && window.__timelines['main'] && window.__frame)")
        print('timeline+frame driver registered:', ok, flush=True)
        if not ok:
            await browser.close(); return
        await page.evaluate("() => { try { return document.fonts.ready; } catch(e) { return null; } }")
        done = 0
        for f in range(f0, min(f1, TOTAL_FRAMES)):
            fp = OUT / f'f{f:05d}.jpg'
            if fp.exists() and fp.stat().st_size > 10000:
                continue
            t = f / FPS
            try:
                await asyncio.wait_for(page.evaluate(
                    "(t) => { window.__frame(t); "
                    "return new Promise(r => requestAnimationFrame(r)); }", t), timeout=30)
                await asyncio.wait_for(page.screenshot(path=str(fp), type='jpeg', quality=90), timeout=30)
            except Exception as e:
                print(f'frame {f} FAILED ({type(e).__name__}) — will retry next run', flush=True)
                continue
            done += 1
            if done % 100 == 0:
                print(f'frame {f} ({done} this run)', flush=True)
        await browser.close()
        print(f'DONE chunk {f0}-{f1}: rendered {done}', flush=True)

asyncio.run(main())
