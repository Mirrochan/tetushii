import os, json, asyncio, re, sys
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out2")
sys.path.insert(0, HERE)
from p2 import THEMES, TOKENS

JS = r"""
(rootSel) => {
  const root = document.querySelector(rootSel);
  const R0 = root.getBoundingClientRect();
  const rootCS = getComputedStyle(document.documentElement);
  const resolveVars = s => s.replace(/var\((--[a-z0-9-]+)\)/g, (m, v) => rootCS.getPropertyValue(v).trim() || '#000');
  const rgb = c => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const box = el => { const r = el.getBoundingClientRect(); return {x: r.left - R0.left, y: r.top - R0.top, w: r.width, h: r.height}; };
  function walk(el, arr, ctx) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const b = box(el);
    const tag = el.tagName.toLowerCase();
    if (tag === 'svg') {
      let s = el.outerHTML;
      s = resolveVars(s).replace(/currentColor/g, cs.color).replace(/style="[^"]*"/, '');
      if (!/xmlns=/.test(s)) s = s.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
      arr.push({t: 'svg', ...b, svg: s}); return;
    }
    if (tag === 'img') {
      const n = {t: 'img', ...b, key: el.dataset.img, fit: cs.objectFit === 'contain' ? 'FIT' : 'FILL', rad: parseFloat(cs.borderTopLeftRadius) || 0};
      const bg = rgb(cs.backgroundColor); if (bg && bg.a > 0) n.fill = bg;
      if (el.closest('[data-go]') === el) n.go = +el.dataset.go;
      arr.push(n); return;
    }
    const v = el.dataset && el.dataset.var ? el.dataset.var : ctx.v;
    const node = {t: 'f', ...b, name: (typeof el.className === 'string' && el.className) ? el.className.split(' ')[0] : tag, kids: []};
    const bg = rgb(cs.backgroundColor); if (bg && bg.a > 0) node.fill = bg;
    const bw = parseFloat(cs.borderTopWidth) || 0, bc = rgb(cs.borderTopColor);
    if (bw > 0 && bc && bc.a > 0 && cs.borderTopStyle !== 'none') { node.stroke = bc; node.sw = bw; }
    if (cs.borderTopLeftRadius !== '0px') node.rad = [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius].map(x => Math.min(parseFloat(x), Math.min(b.w, b.h) / 2));
    if (cs.overflow === 'hidden') node.clip = 1;
    const op = parseFloat(cs.opacity); if (op < 1) node.op = op;
    if (el.dataset && el.dataset.go) node.go = +el.dataset.go;
    if (el.dataset && el.dataset.clone) node.clone = el.dataset.clone;
    for (const ch of el.childNodes) {
      if (ch.nodeType === 3) {
        const txt = ch.textContent.replace(/\s+/g, ' ');
        if (!txt.trim()) continue;
        const rg = document.createRange(); rg.selectNodeContents(ch);
        const rects = [...rg.getClientRects()]; const rr = rg.getBoundingClientRect();
        if (!rr.width) continue;
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3;
        const lines = new Set(rects.map(r => Math.round(r.top))).size;
        node.kids.push({t: 'x', x: rr.left - R0.left, y: rr.top - R0.top, w: rr.width, h: rr.height, txt: txt.trim(),
          wt: parseInt(cs.fontWeight), fs: parseFloat(cs.fontSize), lh, col: rgb(cs.color), ls: parseFloat(cs.letterSpacing) || 0,
          ta: cs.textAlign, lines, v: v || undefined});
      } else if (ch.nodeType === 1) walk(ch, node.kids, {v});
    }
    const keep = node.fill || node.stroke || node.clip || node.go || node.op || node.clone || el === root;
    if (!keep) { for (const k of node.kids) arr.push(k); return; }
    arr.push(node);
  }
  const out = []; walk(root, out, {}); return out[0];
}
"""


async def main():
    res = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        jobs = [("app%02d" % i, "app-pulse-%02d.html" % i, ".phone", 390, 844) for i in range(1, 15)] + [("site", "site-pulse.html", ".site", 1440, 900)]
        for key, f, sel, w, h in jobs:
            pg = await br.new_page(viewport={"width": w, "height": h})
            await pg.goto("file://" + os.path.join(OUT, f))
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            res[key] = await pg.evaluate(JS, sel)
            await pg.close()
        await br.close()
    json.dump(res, open(os.path.join(OUT, "tree.json"), "w"), ensure_ascii=False)

    # compact
    tok = {THEMES["pulse"][k].lower().lstrip("#"): k for k in TOKENS}
    def hx(c):
        s = "%02x%02x%02x" % (round(c["r"]), round(c["g"]), round(c["b"]))
        if c.get("a", 1) < 0.999: s += "%02x" % round(c["a"] * 255)
        return s
    def col(c):
        h = hx(c)
        return "@" + tok[h] if h in tok else h
    def svgmin(s):
        s = re.sub(r"\s+", " ", s); s = re.sub(r">\s+<", "><", s); s = re.sub(r'\s*class="[^"]*"', "", s)
        s = re.sub(r"rgb\((\d+), (\d+), (\d+)\)", lambda m: "#%02x%02x%02x" % tuple(int(x) for x in m.groups()), s)
        s = s.replace('"', "'").replace(" >", ">").replace(" xmlns='http://www.w3.org/2000/svg'", "")
        s = re.sub(r"<svg width='[\d.]+' height='[\d.]+'", "<svg", s, count=1)
        s = s.replace("<rect", "<rect").replace("></rect>", "/>").replace("></path>", "/>").replace("></circle>", "/>")
        return s
    r = round
    def conv(n, px, py):
        t = n["t"]; x, y = n["x"] - px, n["y"] - py
        if t == "svg": return ["s", r(x), r(y), r(n["w"]), r(n["h"]), svgmin(n["svg"])]
        if t == "img":
            o = ["i", r(x), r(y), r(n["w"]), r(n["h"]), n["key"], "n" if n["fit"] == "FIT" else "c", r(n["rad"])]
            ex = {}
            if "fill" in n: ex["f"] = col(n["fill"])
            if "go" in n: ex["g"] = n["go"]
            if ex: o.append(ex)
            return o
        if t == "x":
            o = ["t", r(x), r(y), r(n["w"]) + 1, r(n["h"]), n["txt"], n["wt"], round(n["fs"], 1), round(n["lh"], 1), col(n["col"]), n["lines"]]
            ex = {}
            if n["ls"]: ex["ls"] = round(n["ls"], 2)
            if n["ta"] in ("center", "right"): ex["ta"] = n["ta"][0]
            if n.get("v"): ex["v"] = n["v"]
            if ex: o.append(ex)
            return o
        o = {"n": n["name"][:10], "b": [r(x), r(y), r(n["w"]), r(n["h"])]}
        if "fill" in n: o["f"] = col(n["fill"])
        if "stroke" in n: o["s"] = [col(n["stroke"]), n["sw"]]
        if "rad" in n:
            rd = [r(v) for v in n["rad"]]; o["r"] = rd[0] if len(set(rd)) == 1 else rd
        if n.get("clip"): o["c"] = 1
        if "op" in n: o["o"] = n["op"]
        if "go" in n: o["g"] = n["go"]
        if "clone" in n: o["cl"] = n["clone"]
        k = [conv(c, n["x"], n["y"]) for c in n["kids"]]
        if k: o["k"] = k
        return o
    comp = {k: conv(v, v["x"], v["y"]) for k, v in res.items()}
    json.dump(comp, open(os.path.join(OUT, "comp.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    for k, v in comp.items():
        print(k, len(json.dumps(v, ensure_ascii=False, separators=(",", ":"))))

asyncio.run(main())
