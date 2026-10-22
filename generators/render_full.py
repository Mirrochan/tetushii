import os, asyncio, sys
from playwright.async_api import async_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out2")
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for n in sys.argv[1:]:
            pg=await br.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
            await pg.goto("file://"+os.path.join(OUT,n+".html")); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(OUT,n+".png"),full_page=True); await pg.close()
        await br.close()
asyncio.run(main())
