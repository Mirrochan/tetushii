import os, json, asyncio
from playwright.async_api import async_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# per screen: (text or @back, target screen index)
LINKS = {
    1: [("Продовжити", 2)],
    2: [("Обрати страву", 3), ("Меню кухні", 3), ("Продукти", 5), ("Курка з гречкою та овочами", 4), ("Замовлення А-274", 9)],
    3: [("@back", 2), ("Курка з гречкою та овочами", 4)],
    4: [("@back", 3), ("Додати · 149 ₴", 6)],
    5: [("@back", 2)],
    6: [("@back", 3), ("Оформити замовлення", 7)],
    7: [("@back", 6), ("Далі до оплати", 8)],
    8: [("@back", 7), ("Оплатити 431 ₴", 9)],
    9: [("@back", 2), ("Віконце", 10), ("Комірка", 11), ("Кур'єр", 12), ("Змінити час", 7)],
    10: [("На головну", 2)],
    11: [("На головну", 2)],
    12: [("@back", 9), ("На головну", 2)],
    13: [("@back", 2)],
    14: [("@back", 2), ("Тип картки", 1)],
}
TABS = {"Головна": 2, "Меню": 3, "Картка": 13, "Профіль": 14}

JS = r"""
(links) => {
  const root = document.querySelector('.phone');
  const R0 = root.getBoundingClientRect();
  const rootCS = getComputedStyle(document.documentElement);
  const resolveVars = s => s.replace(/var\((--[a-z0-9-]+)\)/g, (m, v) => rootCS.getPropertyValue(v).trim() || '#000');
  // mark links
  const go = new Map();
  const clickSel = '.btn,.chip,.tab,.card,.tintc,.li,.circ,.hero';
  for (const [txt, tgt] of links) {
    if (txt === '@back') {
      const c = [...root.querySelectorAll('.circ')].find(e => e.innerHTML.includes('M15 5l-7 7 7 7'));
      if (c) go.set(c, tgt);
      continue;
    }
    const els = [...root.querySelectorAll('*')].filter(e => e.children.length === 0 && e.textContent.trim() === txt);
    for (const e of els.slice(0, 1)) { const c = e.closest(clickSel) || e; if (!go.has(c)) go.set(c, tgt); }
  }
  const rgb = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return {r: p[0]/255, g: p[1]/255, b: p[2]/255, a: p.length > 3 ? p[3] : 1}; };
  const out = [];
  function box(el) { const r = el.getBoundingClientRect(); return {x: r.left - R0.left, y: r.top - R0.top, w: r.width, h: r.height}; }
  function walk(el, parentArr) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const b = box(el);
    if (el.tagName.toLowerCase() === 'svg') {
      let s = el.outerHTML;
      const col = cs.color;
      s = resolveVars(s).replace(/currentColor/g, col);
      s = s.replace(/style="[^"]*"/, '');
      if (!/xmlns=/.test(s)) s = s.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
      parentArr.push({t: 'svg', ...b, svg: s});
      return;
    }
    const bg = rgb(cs.backgroundColor);
    const bw = parseFloat(cs.borderTopWidth) || 0;
    const bc = rgb(cs.borderTopColor);
    const ow = cs.outlineStyle !== 'none' ? parseFloat(cs.outlineWidth) || 0 : 0;
    const node = {t: 'f', ...b, name: el.className && typeof el.className === 'string' ? el.className.split(' ')[0] : el.tagName.toLowerCase(), kids: []};
    if (bg && bg.a > 0) node.fill = bg;
    if (bw > 0 && bc && bc.a > 0 && cs.borderTopStyle !== 'none') { node.stroke = bc; node.sw = bw; if (cs.borderTopStyle === 'dashed') node.dash = 1; }
    else if (ow > 0) { node.stroke = rgb(cs.outlineColor); node.sw = ow; node.outside = 1; }
    const rad = cs.borderTopLeftRadius;
    if (rad && rad !== '0px') { const tl = parseFloat(cs.borderTopLeftRadius), tr = parseFloat(cs.borderTopRightRadius), br = parseFloat(cs.borderBottomRightRadius), bl = parseFloat(cs.borderBottomLeftRadius); node.rad = [tl, tr, br, bl].map(v => Math.min(v, Math.min(b.w, b.h) / 2)); }
    if (cs.overflow === 'hidden') node.clip = 1;
    const op = parseFloat(cs.opacity); if (op < 1) node.op = op;
    if (go.has(el)) node.go = go.get(el);
    for (const ch of el.childNodes) {
      if (ch.nodeType === 3) {
        const txt = ch.textContent.replace(/\s+/g, ' ');
        if (!txt.trim()) continue;
        const rg = document.createRange(); rg.selectNodeContents(ch);
        const rects = rg.getClientRects(); const rr = rg.getBoundingClientRect();
        if (!rr.width) continue;
        const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.35;
        node.kids.push({t: 'x', x: rr.left - R0.left, y: rr.top - R0.top, w: rr.width, h: rr.height, txt: txt.trim(),
          fam: cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim(), wt: parseInt(cs.fontWeight), fs: parseFloat(cs.fontSize), lh,
          col: rgb(cs.color), ls: parseFloat(cs.letterSpacing) || 0, up: cs.textTransform === 'uppercase', ta: cs.textAlign,
          strike: cs.textDecorationLine.includes('line-through'), lines: rects.length});
      } else if (ch.nodeType === 1) walk(ch, node.kids);
    }
    // collapse invisible wrappers
    const visible = node.fill || node.stroke || node.clip || node.go || node.op;
    if (!visible && el !== root) { for (const k of node.kids) parentArr.push(k); return; }
    parentArr.push(node);
  }
  walk(root, out);
  return out[0];
}
"""


async def main():
    res = {}
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for i in range(1, 15):
            pg = await br.new_page(viewport={"width": 390, "height": 844})
            await pg.goto("file://" + os.path.join(OUT, "p-%02d.html" % i))
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(200)
            links = LINKS.get(i, []) + [(k, v) for k, v in TABS.items()]
            res[i] = await pg.evaluate(JS, links)
            await pg.close()
        await br.close()
    json.dump(res, open(os.path.join(OUT, "tree.json"), "w"), ensure_ascii=False)
    def count(n):
        return 1 + sum(count(k) for k in n.get("kids", []))
    def gos(n):
        return ([n["go"]] if "go" in n else []) + [g for k in n.get("kids", []) for g in gos(k)]
    for i, t in res.items():
        print(i, "nodes", count(t), "links", gos(t), "chars", len(json.dumps(t, ensure_ascii=False)))

asyncio.run(main())
