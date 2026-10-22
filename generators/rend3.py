import asyncio, json, os, sys
from playwright.async_api import async_playwright
OUT="out2"
async def main():
    jobs=json.load(open(sys.argv[1]))
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for key,f,sel,w,h in jobs:
            pg=await br.new_page(viewport={"width":w,"height":h})
            await pg.goto("file://"+os.path.abspath(os.path.join(OUT,f)))
            await pg.evaluate("document.fonts.ready");await pg.wait_for_timeout(150)
            el=await pg.query_selector(sel)
            await el.screenshot(path=os.path.join(OUT,f.replace(".html",".png")))
            await pg.close()
        await br.close()
asyncio.run(main())
