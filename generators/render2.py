import os, json, asyncio, sys
from playwright.async_api import async_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get("OUTDIR","out"))
jobs = json.load(open(os.path.join(OUT, sys.argv[1] if len(sys.argv) > 1 else "jobs.json")))


async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for n, w, h in jobs:
            pg = await br.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            await pg.goto("file://" + os.path.join(OUT, n + ".html"))
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(OUT, n + ".png"))
            await pg.close()
        await br.close()
    print("rendered", len(jobs))

asyncio.run(main())
