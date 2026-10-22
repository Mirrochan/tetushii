import os, random
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

FONTS = "".join(
    '<link rel="stylesheet" href="../node_modules/@fontsource/%s/%s.css">' % (f, w)
    for f, ws in [("lora", [500, 600, 700]), ("nunito-sans", [400, 600, 700, 800]),
                  ("rubik", [400, 500, 700, 800]), ("playfair-display", [600, 700])]
    for w in ws)

THEMES = {
    "a": "--bg:#F4F1E8;--card:#FFFDF8;--ink:#1C2B22;--soft:#5E6C62;--line:#E3DFD1;--pri:#2E6B45;--pri-ink:#FFFFFF;--acc:#E2A12B;--acc-ink:#1C2B22;--tint:#E3E9D8;--plate:#FFFFFF;--head:'Lora';--body:'Nunito Sans';--r:18px;--hw:600;--ls:0",
    "b": "--bg:#FFFFFF;--card:#F5F4EF;--ink:#191919;--soft:#6A6A66;--line:#E9E8E2;--pri:#E5432D;--pri-ink:#FFFFFF;--acc:#FFC93C;--acc-ink:#191919;--tint:#FFEFE9;--plate:#FFFFFF;--head:'Rubik';--body:'Rubik';--r:12px;--hw:800;--ls:-0.5px",
    "c": "--bg:#171512;--card:#25221D;--ink:#F4ECDD;--soft:#A99F8E;--line:#37332B;--pri:#F0B44C;--pri-ink:#171512;--acc:#8CC49A;--acc-ink:#171512;--tint:#302C25;--plate:#F4ECDD;--head:'Playfair Display';--body:'Nunito Sans';--r:24px;--hw:600;--ls:0",
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body),sans-serif;font-size:15px;line-height:1.35;-webkit-font-smoothing:antialiased}
.phone{width:390px;height:844px;overflow:hidden;display:flex;flex-direction:column;background:var(--bg)}
.safe{height:30px;flex:none}
.top{flex:none;display:flex;align-items:center;gap:12px;padding:6px 18px 12px}
.content{flex:1;overflow:hidden;padding:0 18px;display:flex;flex-direction:column;gap:14px}
.bottom{flex:none;padding:12px 18px 26px;display:flex;gap:12px;align-items:center;background:var(--bg)}
.h1{font-family:var(--head),serif;font-weight:var(--hw);font-size:26px;line-height:1.15;letter-spacing:var(--ls)}
.h2{font-family:var(--head),serif;font-weight:var(--hw);font-size:19px;line-height:1.2;letter-spacing:var(--ls)}
.b{font-weight:800}.soft{color:var(--soft)}.sm{font-size:13px}.xs{font-size:12px}.pri{color:var(--pri)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px}
.tintc{background:var(--tint);border-radius:var(--r);padding:14px}
.btn{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;height:54px;border-radius:calc(var(--r) - 2px);background:var(--pri);color:var(--pri-ink);font-weight:800;font-size:16px;white-space:nowrap;padding:0 18px}
.btn.ghost{background:transparent;color:var(--pri);border:2px solid var(--pri)}
.btn.acc{background:var(--acc);color:var(--acc-ink)}
.btn.s{flex:none;height:40px;font-size:14px;border-radius:999px;align-self:flex-start}
.chip{display:inline-flex;align-items:center;gap:6px;height:34px;padding:0 14px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-weight:700;font-size:13px;white-space:nowrap;flex:none}
.chip.on{background:var(--pri);color:var(--pri-ink);border-color:var(--pri)}
.chip.off{opacity:.45;text-decoration:line-through}
.badge{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 11px;border-radius:999px;background:var(--tint);color:var(--pri);font-weight:800;font-size:12px;align-self:flex-start;white-space:nowrap}
.row{display:flex;align-items:center;gap:12px}.col{display:flex;flex-direction:column}.sp{flex:1}
.hs{display:flex;gap:10px;overflow:hidden;flex:none}
.tile{background:var(--tint);border-radius:calc(var(--r) - 4px);display:flex;align-items:center;justify-content:center;flex:none}
.tabbar{flex:none;height:82px;background:var(--card);border-top:1px solid var(--line);display:flex;padding:10px 10px 0}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;font-size:11px;font-weight:700;color:var(--soft)}
.tab.on{color:var(--pri)}
.circ{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none;background:var(--card);border:1px solid var(--line)}
.circ.p{background:var(--pri);color:var(--pri-ink);border:none}
.av{width:36px;height:36px;border-radius:50%;background:var(--acc);color:var(--acc-ink);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;flex:none}
.hero{background:var(--pri);color:var(--pri-ink);border-radius:calc(var(--r) + 6px);padding:18px;position:relative;overflow:hidden;display:flex;flex-direction:column;gap:6px;flex:none}
.eyebrow{font-size:11px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase}
.cb{width:24px;height:24px;border-radius:7px;border:2px solid var(--line);flex:none;display:flex;align-items:center;justify-content:center}
.cb.on{background:var(--pri);border-color:var(--pri);color:var(--pri-ink)}
.rad{width:22px;height:22px;border-radius:50%;border:2px solid var(--soft);flex:none}
.rad.on{border:7px solid var(--pri)}
.bar{height:8px;border-radius:99px;background:var(--line);overflow:hidden}.bar i{display:block;height:8px;border-radius:99px;background:var(--pri)}
.li{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}
.li:last-child{border-bottom:none}
.dot{width:10px;height:10px;border-radius:50%;background:var(--pri);flex:none}.dot.w{background:var(--acc)}
.num{width:26px;height:26px;border-radius:50%;background:var(--tint);color:var(--pri);font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;flex:none}
"""

ICONS = {
    "home": '<path d="M3 11l9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 5v16M8 8h7"/>',
    "card": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "back": '<path d="M15 5l-7 7 7 7"/>',
    "next": '<path d="M9 5l7 7-7 7"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "cart": '<path d="M3 4h2l2.5 11h10l2-8H7"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
    "leaf": '<path d="M5 19c0-9 5-14 14-14 0 9-5 14-14 14z"/><path d="M5 19l8-8"/>',
    "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>',
    "bottle": '<path d="M10 3h4v4l2 3v10a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V10l2-3z"/><path d="M8 13h8"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-5.5 7-5.5s7 2 7 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 1.5 5 4.5"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "cloud": '<path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9.5 4.3 4.3 0 0 1 17.5 18z"/>',
    "list": '<path d="M8 6h12M8 12h12M8 18h12M4 6h.5M4 12h.5M4 18h.5"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "gift": '<rect x="3" y="9" width="18" height="12" rx="1"/><path d="M3 13h18M12 9v12M12 9c-4 0-5-5-2-5 2 0 2 5 2 5zM12 9c4 0 5-5 2-5-2 0-2 5-2 5z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/>',
    "thumb": '<path d="M7 11v9H4v-9zM7 11l4-8c2 0 3 1 3 3l-1 4h5a2 2 0 0 1 2 2l-1.5 6a2 2 0 0 1-2 2H7"/>',
}


def ic(n, s=22, c="currentColor", w=2):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" style="flex:none">%s</svg>' % (s, s, c, w, ICONS[n])


def plate(kind, s=110):
    P = '<circle cx="60" cy="60" r="56" fill="var(--plate)"/><circle cx="60" cy="60" r="55.2" fill="none" stroke="rgba(0,0,0,.08)" stroke-width="1.6"/><circle cx="60" cy="60" r="43" fill="none" stroke="rgba(0,0,0,.07)" stroke-width="1.2"/>'
    F = {
        "chicken": '<ellipse cx="46" cy="68" rx="24" ry="17" fill="#8B5E3C"/><ellipse cx="42" cy="64" rx="13" ry="8" fill="#A0704A"/><ellipse cx="74" cy="52" rx="20" ry="13" transform="rotate(-25 74 52)" fill="#E3A857"/><ellipse cx="72" cy="50" rx="12" ry="6" transform="rotate(-25 72 50)" fill="#F0C27A"/><circle cx="80" cy="76" r="7" fill="#5E9E57"/><circle cx="70" cy="82" r="6" fill="#77B46B"/><circle cx="88" cy="68" r="4" fill="#E25B3C"/>',
        "borsch": '<circle cx="60" cy="60" r="44" fill="#F2EEE6"/><circle cx="60" cy="60" r="38" fill="#B3232B"/><circle cx="60" cy="60" r="38" fill="none" stroke="#8F1A22" stroke-width="2"/><ellipse cx="54" cy="56" rx="13" ry="9" fill="#FFF7EE"/><circle cx="74" cy="50" r="2.5" fill="#4E9A4E"/><circle cx="70" cy="72" r="2.5" fill="#4E9A4E"/><circle cx="44" cy="74" r="2.5" fill="#4E9A4E"/><circle cx="80" cy="64" r="2" fill="#4E9A4E"/>',
        "syrnyky": '<circle cx="42" cy="66" r="16" fill="#D8962F"/><circle cx="42" cy="66" r="10" fill="#E7B255"/><circle cx="60" cy="52" r="16" fill="#E0A23A"/><circle cx="60" cy="52" r="10" fill="#EDBE66"/><circle cx="76" cy="68" r="16" fill="#E6AD48"/><circle cx="76" cy="68" r="10" fill="#F0C470"/><ellipse cx="86" cy="44" rx="9" ry="7" fill="#FFF8EF"/><circle cx="34" cy="44" r="4" fill="#C2313F"/><circle cx="42" cy="38" r="3.5" fill="#C2313F"/><circle cx="58" cy="84" r="3" fill="#4E9A4E"/>',
        "salad": '<circle cx="48" cy="54" r="14" fill="#6FAE5C"/><circle cx="70" cy="50" r="15" fill="#84C06E"/><circle cx="60" cy="72" r="16" fill="#5C9E50"/><circle cx="78" cy="70" r="10" fill="#98CF7F"/><circle cx="46" cy="72" r="6" fill="#E2483A"/><circle cx="70" cy="60" r="5.5" fill="#E2483A"/><circle cx="56" cy="50" r="4" fill="#F3C64B"/><circle cx="80" cy="56" r="3.5" fill="#F3C64B"/><circle cx="62" cy="80" r="4" fill="#8E2B56"/>',
        "deruny": '<ellipse cx="42" cy="64" rx="18" ry="13" transform="rotate(-20 42 64)" fill="#B97A2A"/><ellipse cx="60" cy="56" rx="18" ry="13" transform="rotate(-20 60 56)" fill="#C98A34"/><ellipse cx="78" cy="62" rx="18" ry="13" transform="rotate(-20 78 62)" fill="#D39A45"/><ellipse cx="56" cy="84" rx="12" ry="7" fill="#FFF8EF"/><circle cx="52" cy="83" r="1.8" fill="#4E9A4E"/><circle cx="60" cy="86" r="1.8" fill="#4E9A4E"/><circle cx="84" cy="40" r="2.5" fill="#4E9A4E"/>',
        "holubtsi": '<ellipse cx="60" cy="64" rx="36" ry="27" fill="#E8833A"/><ellipse cx="60" cy="64" rx="30" ry="21" fill="#EE9550"/><rect x="28" y="38" width="38" height="18" rx="9" transform="rotate(-18 47 47)" fill="#9BB05C"/><rect x="41" y="52" width="38" height="18" rx="9" transform="rotate(-18 60 61)" fill="#A9BC6A"/><rect x="54" y="66" width="38" height="18" rx="9" transform="rotate(-18 73 75)" fill="#B4C777"/><circle cx="84" cy="48" r="2.5" fill="#FFF8EF"/><circle cx="38" cy="78" r="2.5" fill="#FFF8EF"/>',
        "pasta": '<circle cx="60" cy="60" r="30" fill="#EFCB6B"/><path d="M40 56c8-10 30-12 40-2M38 66c10-8 34-8 44 0M44 76c8-6 24-6 32 0" stroke="#D9AE45" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="52" cy="54" r="5" fill="#D8452F"/><circle cx="70" cy="68" r="5" fill="#D8452F"/><circle cx="64" cy="50" r="3" fill="#4E9A4E"/><circle cx="50" cy="72" r="3" fill="#4E9A4E"/>',
        "soup": '<circle cx="60" cy="60" r="44" fill="#F2EEE6"/><circle cx="60" cy="60" r="38" fill="#E9B44C"/><circle cx="50" cy="54" r="6" fill="#F4D58A"/><circle cx="70" cy="62" r="7" fill="#F4D58A"/><circle cx="56" cy="72" r="5" fill="#E28A3A"/><circle cx="72" cy="48" r="2.5" fill="#4E9A4E"/><circle cx="46" cy="68" r="2.5" fill="#4E9A4E"/>',
        "sandwich": '<path d="M30 78L60 34l30 44z" fill="#E8C98A"/><path d="M36 74L60 40l24 34z" fill="#F6E3B5"/><path d="M38 70h44" stroke="#5E9E57" stroke-width="5" stroke-linecap="round"/><path d="M42 62h36" stroke="#D8452F" stroke-width="5" stroke-linecap="round"/><path d="M46 54h28" stroke="#F3C64B" stroke-width="5" stroke-linecap="round"/>',
        "coffee": '<circle cx="60" cy="60" r="40" fill="#F2EEE6"/><circle cx="60" cy="60" r="30" fill="#FFFFFF" stroke="rgba(0,0,0,.08)" stroke-width="1.5"/><circle cx="60" cy="60" r="24" fill="#6B4630"/><path d="M50 60c4-8 12-8 14 0s8 6 8 0" stroke="#E8D3B5" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
        "bread": '<ellipse cx="60" cy="62" rx="34" ry="22" fill="#C98A45"/><ellipse cx="60" cy="58" rx="30" ry="17" fill="#DBA35E"/><path d="M44 50l6 14M58 47l6 16M72 49l5 13" stroke="#B5762F" stroke-width="3.5" stroke-linecap="round"/>',
        "cheese": '<path d="M26 74l46-32 22 32z" fill="#F0C64A"/><path d="M26 74h68v12H26z" fill="#E2B235"/><circle cx="58" cy="66" r="5" fill="#E2B235"/><circle cx="76" cy="70" r="3.5" fill="#E2B235"/><circle cx="46" cy="80" r="3" fill="#C99A25"/>',
        "eggs": '<ellipse cx="46" cy="60" rx="14" ry="18" fill="#F3E3C7"/><ellipse cx="74" cy="60" rx="14" ry="18" fill="#E9D2AE"/><ellipse cx="60" cy="72" rx="14" ry="18" fill="#F8ECD8"/>',
    }
    return '<svg width="%d" height="%d" viewBox="0 0 120 120" style="flex:none">%s%s</svg>' % (s, s, "" if kind in ("bread", "cheese", "eggs", "sandwich") and False else P, F[kind])


def bottle(s=180):
    return '<svg width="%d" height="%d" viewBox="0 0 120 160" style="flex:none"><rect x="48" y="8" width="24" height="16" rx="4" fill="#2E6B45"/><path d="M48 24h24v18l14 22v78a10 10 0 0 1-10 10H44a10 10 0 0 1-10-10V64l14-22z" fill="#FFFFFF" stroke="rgba(0,0,0,.12)" stroke-width="2"/><path d="M36 74h48v52H36z" fill="#F6F1E4"/><circle cx="60" cy="100" r="15" fill="#2E6B45"/><path d="M52 102c2-8 8-10 16-10-1 8-4 13-12 13M52 106l8-8" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>' % (int(s * 0.75), s)


def hills(w=390, h=220):
    return '<svg width="%d" height="%d" viewBox="0 0 390 220" preserveAspectRatio="none" style="display:block;flex:none"><rect width="390" height="220" fill="#DCE9D0"/><circle cx="300" cy="62" r="30" fill="#F3C64B"/><path d="M0 130c60-40 120-40 190 0s130 20 200-20v110H0z" fill="#9CC47F"/><path d="M0 160c70-30 150-20 220 6s120 10 170-14v68H0z" fill="#6FAE5C"/><path d="M0 190c90-20 180-10 250 4s100 6 140-6v32H0z" fill="#4F8F48"/><rect x="88" y="118" width="46" height="34" fill="#FFF7EA"/><path d="M82 120l29-22 29 22z" fill="#C2553A"/><rect x="104" y="132" width="12" height="20" fill="#8B5E3C"/></svg>' % (w, h)


def qr(seed, s=170):
    rnd = random.Random(seed)
    n = 21
    c = s / n
    cells = []
    def finder(x, y):
        return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#111"/><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff"/><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#111"/>'
                % (x * c, y * c, 7 * c, 7 * c, (x + 1) * c, (y + 1) * c, 5 * c, 5 * c, (x + 2) * c, (y + 2) * c, 3 * c, 3 * c))
    for y in range(n):
        for x in range(n):
            if (x < 8 and y < 8) or (x > 12 and y < 8) or (x < 8 and y > 12):
                continue
            if rnd.random() < 0.48:
                cells.append('<rect x="%.1f" y="%.1f" width="%.2f" height="%.2f" fill="#111"/>' % (x * c, y * c, c + .3, c + .3))
    return '<svg width="%d" height="%d" viewBox="0 0 %d %d" style="flex:none;background:#fff"><rect width="%d" height="%d" fill="#fff"/>%s%s%s%s</svg>' % (s, s, s, s, s, s, "".join(cells), finder(0, 0), finder(14, 0), finder(0, 14))


def barcode(w=300, h=64, seed=7):
    rnd = random.Random(seed)
    x = 0
    bars = []
    while x < w:
        bw = rnd.choice([2, 2, 3, 4, 6])
        bars.append('<rect x="%d" y="0" width="%d" height="%d" fill="#111"/>' % (x, bw, h))
        x += bw + rnd.choice([2, 3, 4, 5])
    return '<svg width="%d" height="%d" viewBox="0 0 %d %d" style="display:block">%s</svg>' % (w, h, w, h, "".join(bars))


TABS = [("home", "Головна"), ("book", "Рецепти"), ("card", "Картка"), ("user", "Профіль")]


def tabbar(a):
    return '<div class="tabbar">%s</div>' % "".join(
        '<div class="tab%s">%s<span>%s</span></div>' % (" on" if i == a else "", ic(n, 24), l) for i, (n, l) in enumerate(TABS))


def topbar(title, right=""):
    return '<div class="top"><div class="circ">%s</div><div class="h2" style="flex:1">%s</div>%s</div>' % (ic("back", 20), title, right)


def phone(body, tab=None, bottom="", safe=True):
    return '<div class="phone">%s%s%s%s</div>' % ('<div class="safe"></div>' if safe else "", body, bottom, tabbar(tab) if tab is not None else "")


def content(*parts, style=""):
    return '<div class="content" style="%s">%s</div>' % (style, "".join(parts))


def dishcard(kind, name, price):
    return ('<div class="col" style="width:146px;flex:none;gap:8px"><div class="tile" style="height:112px">%s</div><div class="b sm" style="line-height:1.25;height:33px">%s</div>'
            '<div class="row"><div class="b" style="font-size:16px">%s ₴</div><div class="sp"></div><div class="circ p" style="width:32px;height:32px">%s</div></div></div>') % (plate(kind, 96), name, price, ic("plus", 18))


# ---------------- screens ----------------
def greet(sub="Добрий вечір", title="Олено, що на вечерю?"):
    return '<div class="top"><div class="col" style="flex:1"><div class="sm soft">%s</div><div class="h1">%s</div></div><div class="av" style="width:44px;height:44px;font-size:17px">О</div></div>' % (sub, title)


def s_home():
    hero = ('<div class="hero" style="min-height:176px"><div class="eyebrow" style="opacity:.85">Вечеря сьогодні</div><div class="h1" style="font-size:28px;max-width:200px">Готова до&nbsp;18:30</div>'
            '<div class="sm" style="opacity:.9;max-width:190px">Заберіть у віконці без черги</div><div class="sp"></div><div class="btn acc s">Обрати вечерю</div>'
            '<div style="position:absolute;right:-30px;bottom:-30px">%s</div></div>') % plate("chicken", 156)
    menu = '<div class="row"><div class="h2">Меню дня</div><div class="sp"></div><div class="sm b pri">Усе меню</div></div><div class="hs">%s%s%s</div>' % (
        dishcard("chicken", "Курка з гречкою та овочами", 149), dishcard("borsch", "Борщ з пампушками", 119), dishcard("syrnyky", "Сирники зі сметаною", 99))
    chips = '<div class="hs"><div class="chip">Комбо</div><div class="chip">Рецепти сусідів</div><div class="chip">Від фермерів</div><div class="chip">Хелсі</div></div>'
    vote = '<div class="card row"><div class="circ p">%s</div><div class="col" style="flex:1"><div class="b">Голосування тижня</div><div class="sm soft">Яку страву додати в меню?</div></div>%s</div>' % (ic("thumb", 20), ic("next", 18, "var(--soft)"))
    nb = '<div class="card row" style="padding:10px"><div class="tile" style="width:60px;height:60px">%s</div><div class="col" style="flex:1"><div class="xs b pri">РЕЦЕПТ ВІД СУСІДА</div><div class="b">Деруни як у бабусі</div></div>%s</div>' % (plate("deruny", 50), ic("next", 18, "var(--soft)"))
    return phone(greet() + content(hero, menu, chips, vote, nb), tab=0)


def s_dish():
    top = ('<div style="background:var(--tint);height:300px;flex:none;position:relative;display:flex;align-items:center;justify-content:center">%s'
           '<div class="circ" style="position:absolute;left:18px;top:36px">%s</div><div class="circ" style="position:absolute;right:18px;top:36px">%s</div></div>') % (plate("chicken", 236), ic("back", 20), ic("heart", 20))
    body = content(
        '<div class="badge" style="margin-top:16px">%s Від локального фермера</div>' % ic("leaf", 14),
        '<div class="h1">Курка з гречкою та овочами</div>',
        '<div class="row sm soft"><span>320 г</span><span>·</span>%s<span>розігріти за 5 хв</span></div>' % ic("clock", 15),
        '<div class="sm soft">Філе курки, гречка, броколі, морква. Готуємо щодня на кухні магазину.</div>',
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">%s</div>' % "".join('<div class="tintc col" style="padding:8px 10px;align-items:center"><div class="b">%s</div><div class="xs soft">%s</div></div>' % (a, b) for a, b in [("410", "ккал"), ("34 г", "білки"), ("12 г", "жири"), ("38 г", "вуглев.")]),
        '<div class="card row"><div class="circ p">%s</div><div class="col" style="flex:1"><div class="b">Приготувати самому</div><div class="sm soft">Рецепт і всі інгредієнти в кошик</div></div>%s</div>' % (ic("book", 20), ic("next", 18, "var(--soft)")),
    )
    bottom = '<div class="bottom"><div class="card row" style="padding:0 12px;height:54px;gap:14px">%s<span class="b">1</span>%s</div><div class="btn">Додати · 149 ₴</div></div>' % (ic("minus", 18), ic("plus", 18))
    return phone(top + body, bottom=bottom, safe=False)


def s_time():
    slots = [("17:00", ""), ("17:30", ""), ("18:00", ""), ("18:30", "on"), ("19:00", ""), ("19:30", "off")]
    grid = '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">%s</div>' % "".join(
        '<div class="chip %s" style="justify-content:center;height:44px;font-size:15px">%s</div>' % (c, t) for t, c in slots)
    opt1 = '<div class="card row" style="border:2px solid var(--pri)"><div class="rad on"></div><div class="col" style="flex:1"><div class="b">Віконце видачі</div><div class="sm soft">Без черги · безкоштовно</div></div>%s</div>' % ic("pin", 20, "var(--pri)")
    opt2 = '<div class="card row"><div class="rad"></div><div class="col" style="flex:1"><div class="b">Доставка додому</div><div class="sm soft">30–45 хв · від 49 ₴</div></div></div>'
    summ = '<div class="row"><div class="soft">2 страви</div><div class="sp"></div><div class="h2">298 ₴</div></div>'
    body = content('<div class="h2">Коли забрати?</div>', '<div class="hs"><div class="chip on">Сьогодні</div><div class="chip">Завтра</div></div>', grid,
                   '<div class="h2" style="margin-top:6px">Як отримати?</div>', opt1, opt2, '<div class="tintc row sm b">%s<span>Нагадаємо за 15 хвилин до видачі</span></div>' % ic("clock", 18, "var(--pri)"), '<div class="sp"></div>', summ)
    return phone(topbar("Оформлення") + body, bottom='<div class="bottom"><div class="btn">Оплатити 298 ₴</div></div>')


def s_ready():
    top = ('<div style="background:var(--pri);color:var(--pri-ink);padding:44px 22px 26px;border-radius:0 0 28px 28px;display:flex;flex-direction:column;gap:8px;align-items:center;text-align:center;flex:none">'
           '<div style="width:56px;height:56px;border-radius:50%%;background:var(--acc);color:var(--acc-ink);display:flex;align-items:center;justify-content:center">%s</div>'
           '<div class="h1">Замовлення готове</div><div class="sm" style="opacity:.9">Віконце видачі · чекаємо до 19:00</div></div>') % ic("check", 30, w=3)
    q = '<div class="card col" style="align-items:center;gap:10px;padding:18px">%s<div class="h1" style="letter-spacing:3px">А-274</div><div class="sm soft">Покажіть код у віконці</div></div>' % qr(11, 168)
    steps = '<div class="row sm b" style="justify-content:center;gap:8px"><span class="dot"></span>Прийнято<span class="soft">—</span><span class="dot"></span>Зібрано<span class="soft">—</span><span class="dot"></span>Готово</div>'
    bonus = '<div class="tintc row"><div class="circ p">%s</div><div class="b" style="flex:1">+15 бонусів на сімейну картку</div></div>' % ic("gift", 20)
    items = '<div class="card row">%s<div class="col" style="flex:1"><div class="b">Курка з гречкою × 2</div><div class="sm soft">Оплачено · 298 ₴</div></div></div>' % plate("chicken", 46)
    return phone(top + content(q, steps, items, bonus, style="padding-top:16px"), bottom='<div class="bottom"><div class="btn ghost">Як пройти до віконця</div></div>', safe=False)


def s_recipe():
    top = ('<div style="background:var(--tint);height:250px;flex:none;position:relative;display:flex;align-items:center;justify-content:center">%s'
           '<div class="circ" style="position:absolute;left:18px;top:36px">%s</div></div>') % (plate("borsch", 200), ic("back", 20))
    meta = '<div class="row sm soft">%s<span>50 хв</span>%s<span>4 порції</span>%s<span>9 інгредієнтів</span></div>' % (ic("clock", 15), ic("users", 15), ic("list", 15))
    steps = "".join('<div class="row" style="align-items:flex-start"><div class="num">%d</div><div class="sm" style="flex:1">%s</div></div>' % (i + 1, t) for i, t in enumerate(
        ["Зваріть бульйон зі свинини, 30 хвилин.", "Натріть буряк і моркву, протушкуйте з томатною пастою.", "Додайте капусту й картоплю, варіть до готовності."]))
    body = content('<div class="badge" style="margin-top:16px">%s Рецепт тижня</div>' % ic("star", 14), '<div class="h1">Борщ з пампушками</div>', meta,
                   '<div class="btn" style="flex:none">%s Усі інгредієнти в кошик</div>' % ic("cart", 20), '<div class="h2">Як готувати</div>', steps)
    return phone(top + body, safe=False)


def s_ingr():
    items = [("Буряк", "2 шт", 24, 1), ("Капуста", "½ качана", 28, 1), ("Свинина", "400 г", 156, 1), ("Морква", "2 шт", 12, 1), ("Томатна паста", "70 г", 38, 1),
             ("Сметана", "200 г", 46, 1), ("Пампушки", "6 шт", 82, 1), ("Картопля", "4 шт", 0, 0), ("Цибуля", "1 шт", 0, 0)]
    rows = ""
    for n, q, p, on in items:
        if on:
            rows += '<div class="li"><div class="cb on">%s</div><div class="col" style="flex:1"><div class="b">%s</div><div class="xs soft">%s</div></div><div class="b">%d ₴</div></div>' % (ic("check", 15, w=3), n, q, p)
        else:
            rows += '<div class="li" style="opacity:.55"><div class="cb"></div><div class="col" style="flex:1"><div class="b">%s</div><div class="xs soft">%s</div></div><div class="badge">є вдома</div></div>' % (n, q)
    port = '<div class="card row" style="padding:10px 14px"><div class="b" style="flex:1">Порцій</div><div class="circ" style="width:34px;height:34px">%s</div><div class="h2">4</div><div class="circ p" style="width:34px;height:34px">%s</div></div>' % (ic("minus", 16), ic("plus", 16))
    return phone(topbar("Інгредієнти для борщу") + content(port, '<div class="col">%s</div>' % rows, style="gap:8px"), bottom='<div class="bottom"><div class="btn">Додати 7 товарів · 386 ₴</div></div>')


def s_cart():
    g = ('<div class="card col" style="gap:10px"><div class="row">%s<div class="col" style="flex:1"><div class="b">Для борщу</div><div class="sm soft">7 товарів · на 4 порції</div></div><div class="b">386 ₴</div></div>'
         '<div class="sm soft">Буряк, капуста, свинина, морква та ще 3</div></div>') % plate("borsch", 52)
    it = '<div class="card row">%s<div class="col" style="flex:1"><div class="b">Курка з гречкою</div><div class="sm soft">2 порції · готова страва</div></div><div class="b">298 ₴</div></div>' % plate("chicken", 52)
    up = '<div class="tintc row">%s<div class="col" style="flex:1"><div class="b">Додати хліб до борщу?</div><div class="sm soft">Житній, 400 г · 34 ₴</div></div><div class="circ p" style="width:34px;height:34px">%s</div></div>' % (plate("bread", 46), ic("plus", 16))
    tot = '<div class="col" style="gap:6px"><div class="row"><div class="soft">Бонусів нарахуємо</div><div class="sp"></div><div class="b pri">+34</div></div><div class="row"><div class="h2">Разом</div><div class="sp"></div><div class="h1">684 ₴</div></div></div>'
    return phone(topbar("Кошик") + content(g, it, up, '<div class="sp"></div>', tot), bottom='<div class="bottom"><div class="btn">Обрати час видачі</div></div>')


def s_family():
    card = ('<div class="hero" style="gap:12px"><div class="row"><div class="col" style="flex:1"><div class="eyebrow" style="opacity:.85">Сімейна картка</div><div class="h2">Родина Коваленків</div></div>%s</div>'
            '<div style="background:#fff;border-radius:12px;padding:12px 14px">%s</div><div class="sm" style="text-align:center;letter-spacing:2px;opacity:.9">2200 4417 0935</div></div>') % (ic("users", 26), barcode(286, 58))
    bal = '<div class="row"><div class="col" style="flex:1"><div class="sm soft">Спільний баланс</div><div class="h1" style="font-size:32px">1 240 бонусів</div></div></div>'
    avs = '<div class="row" style="gap:8px">%s<div class="circ" style="width:36px;height:36px">%s</div><div class="sm soft" style="margin-left:6px">4 учасники</div></div>' % (
        "".join('<div class="av" style="%s">%s</div>' % (st, l) for l, st in [("О", ""), ("А", "background:var(--pri);color:var(--pri-ink)"), ("М", "background:var(--tint);color:var(--pri)"), ("Б", "")]), ic("plus", 16))
    def t(i, a, b):
        return '<div class="card col" style="gap:8px"><div class="circ p" style="width:36px;height:36px">%s</div><div class="b">%s</div><div class="sm soft">%s</div></div>' % (ic(i, 18), a, b)
    grid = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">%s%s%s%s</div>' % (
        t("list", "Спільний список", "6 товарів"), t("gift", "Історія бонусів", "+62 за тиждень"), t("bottle", "Тара", "3 пляшки у вас"), t("users", "Запросити рідних", "за посиланням"))
    return phone(topbar("Картка") + content(card, bal, avs, grid), tab=2)


def s_flist():
    items = [("Молоко фермерське", "А", 1), ("Хліб житній", "О", 0), ("Яйця, 10 шт", "М", 0), ("Сир кисломолочний", "О", 0), ("Яблука, 1 кг", "Б", 0), ("Кава мелена", "А", 0)]
    rows = "".join('<div class="li"><div class="cb%s">%s</div><div class="b" style="flex:1;%s">%s</div><div class="av" style="width:28px;height:28px;font-size:12px">%s</div></div>' % (
        " on" if d else "", ic("check", 15, w=3) if d else "", "opacity:.5;text-decoration:line-through" if d else "", n, a) for n, a, d in items)
    add = '<div class="card row" style="padding:12px 14px">%s<div class="soft" style="flex:1">Додати товар…</div></div>' % ic("plus", 18, "var(--soft)")
    note = '<div class="row sm soft">%s<span>Список бачать усі в родині</span></div>' % ic("users", 15)
    return phone(topbar("Спільний список") + content(add, '<div class="col">%s</div>' % rows, note), bottom='<div class="bottom"><div class="btn">Замовити все · 6 товарів</div></div>')


def s_bonus():
    hist = [("cart", "Онлайн-замовлення", "Сьогодні, 18:32", "+15"), ("bottle", "Повернення тари", "Учора", "+10"), ("card", "Покупка в магазині", "2 жовтня", "+32"),
            ("thumb", "Голосування тижня", "1 жовтня", "+5"), ("gift", "Списано на вечерю", "29 вересня", "−200")]
    rows = "".join('<div class="li"><div class="circ">%s</div><div class="col" style="flex:1"><div class="b">%s</div><div class="xs soft">%s</div></div><div class="h2 %s">%s</div></div>' % (
        ic(i, 18, "var(--pri)"), a, b, "pri" if v[0] == "+" else "", v) for i, a, b, v in hist)
    top = '<div class="hero" style="align-items:flex-start"><div class="eyebrow" style="opacity:.85">Спільний баланс родини</div><div class="h1" style="font-size:36px">1 240</div><div class="sm" style="opacity:.9">бонусів · можна списати на будь-яку покупку</div></div>'
    return phone(topbar("Історія бонусів") + content(top, '<div class="col">%s</div>' % rows), tab=2)


def s_neighbor():
    c1 = ('<div class="card col" style="gap:10px;padding:10px"><div class="tile" style="height:150px">%s</div><div class="col" style="padding:0 4px 4px;gap:8px"><div class="h2">Деруни як у бабусі</div>'
          '<div class="row"><div class="av" style="width:28px;height:28px;font-size:12px">Г</div><div class="sm soft" style="flex:1">Галина, буд. 175</div>%s<span class="sm b">128</span></div>'
          '<div class="btn s" style="align-self:stretch;height:44px">%s Інгредієнти в кошик</div></div></div>') % (plate("deruny", 130), ic("heart", 16, "var(--pri)"), ic("cart", 18))
    c2 = ('<div class="card row" style="padding:10px"><div class="tile" style="width:76px;height:76px">%s</div><div class="col" style="flex:1;gap:4px"><div class="b">Сирники без борошна</div>'
          '<div class="sm soft">Андрій, буд. 181</div></div>%s<span class="sm b">94</span></div>') % (plate("syrnyky", 64), ic("heart", 16, "var(--pri)"))
    chips = '<div class="hs"><div class="chip on">Усі</div><div class="chip">Перші страви</div><div class="chip">Випічка</div><div class="chip">Швидко</div></div>'
    fab = '<div style="padding:0 18px 12px;flex:none"><div class="btn acc" style="height:48px">%s Поділитися своїм рецептом</div></div>' % ic("plus", 18)
    c3 = ('<div class="card row" style="padding:10px"><div class="tile" style="width:76px;height:76px">%s</div><div class="col" style="flex:1;gap:4px"><div class="b">Гарбузовий суп-пюре</div><div class="sm soft">Марія, буд. 173</div></div>%s<span class="sm b">71</span></div>') % (plate("soup", 64), ic("heart", 16, "var(--pri)"))
    return phone(topbar("Рецепти сусідів") + content(chips, c1, c2, c3), bottom=fab, tab=1)


def s_vote():
    def o(k, n, p, on):
        return ('<div class="card row" style="%s"><div class="tile" style="width:58px;height:58px">%s</div><div class="col" style="flex:1;gap:8px"><div class="row"><div class="b" style="flex:1">%s</div><div class="b %s">%d%%</div></div>'
                '<div class="bar"><i style="width:%d%%"></i></div></div></div>') % ("border:2px solid var(--pri)" if on else "", plate(k, 50), n, "pri" if on else "soft", p, p)
    body = content('<div class="h1">Яку страву додати в меню?</div>', '<div class="row sm soft">%s<span>Залишилося 2 дні · голосують мешканці району</span></div>' % ic("clock", 15),
                   o("holubtsi", "Голубці", 46, 1), o("pasta", "Паста з овочами", 31, 0), o("soup", "Гарбузовий суп", 23, 0),
                   '<div class="tintc row sm b">%s<span>За голос — 5 бонусів на картку</span></div>' % ic("gift", 18, "var(--pri)"))
    return phone(topbar("Голосування тижня") + body, bottom='<div class="bottom"><div class="btn">Проголосувати за голубці</div></div>')


def s_voteres():
    top = '<div style="background:var(--tint);height:310px;flex:none;display:flex;align-items:center;justify-content:center;position:relative">%s<div class="circ" style="position:absolute;left:18px;top:36px">%s</div></div>' % (plate("holubtsi", 230), ic("back", 20))
    body = content('<div class="badge" style="margin-top:18px;background:var(--acc);color:var(--acc-ink)">%s Переможець голосування</div>' % ic("star", 14),
                   '<div class="h1" style="font-size:30px">Голубці — у меню з понеділка</div>', '<div class="soft">Дякуємо, що обирали разом із сусідами. Ваші 5 бонусів уже на картці.</div>')
    return phone(top + body, bottom='<div class="bottom" style="flex-direction:column"><div class="btn" style="align-self:stretch;flex:none">Нагадати, коли з\'явиться</div><div class="btn ghost" style="align-self:stretch;flex:none">Запропонувати свій рецепт</div></div>', safe=False)


def s_product():
    top = '<div style="background:var(--tint);height:290px;flex:none;display:flex;align-items:center;justify-content:center;position:relative">%s<div class="circ" style="position:absolute;left:18px;top:36px">%s</div></div>' % (bottle(230), ic("back", 20))
    body = content('<div class="badge" style="margin-top:16px">%s Від локального фермера</div>' % ic("leaf", 14), '<div class="h1">Молоко фермерське, 1 л</div>',
                   '<div class="card row"><div class="tile" style="width:48px;height:48px;border-radius:50%%">%s</div><div class="col" style="flex:1"><div class="b">Ферма «Зелений хутір»</div><div class="sm soft">Київщина · 38 км від магазину</div></div>%s</div>' % (ic("leaf", 22, "var(--pri)"), ic("next", 18, "var(--soft)")),
                   '<div class="tintc row">%s<div class="col" style="flex:1"><div class="b">Багаторазова пляшка</div><div class="sm soft">Поверніть — отримаєте 10 бонусів</div></div></div>' % ic("bottle", 24, "var(--pri)"))
    return phone(top + body, bottom='<div class="bottom"><div class="h1" style="width:92px">62 ₴</div><div class="btn">У кошик</div></div>', safe=False)


def s_farmer():
    def p(k, n, pr):
        return '<div class="col" style="width:112px;flex:none;gap:6px"><div class="tile" style="height:96px">%s</div><div class="sm b">%s</div><div class="sm soft">%s ₴</div></div>' % (k, n, pr)
    top = '<div style="position:relative;flex:none">%s<div class="circ" style="position:absolute;left:18px;top:36px">%s</div></div>' % (hills(), ic("back", 20))
    body = content('<div class="h1" style="margin-top:16px">Ферма «Зелений хутір»</div>', '<div class="row sm soft">%s<span>Київщина · 38 км від магазину</span></div>' % ic("pin", 15),
                   '<div class="soft">Сімейна ферма: молоко, сир і яйця. Привозять тричі на тиждень, тару забирають назад.</div>', '<div class="h2">Продукти ферми</div>',
                   '<div class="hs">%s%s%s</div>' % (p(bottle(84), "Молоко, 1 л", 62), p(plate("cheese", 84), "Сир твердий", 148), p(plate("eggs", 84), "Яйця, 10 шт", 74)),
                   '<div class="btn ghost" style="flex:none;height:46px">Усі товари ферми</div>')
    return phone(top + body, safe=False)


def s_tara():
    q = '<div class="card col" style="align-items:center;gap:10px;padding:18px">%s<div class="b">Покажіть код у пункті прийому</div><div class="sm soft">Автомат біля входу або каса</div></div>' % qr(5, 150)
    st = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><div class="tintc col"><div class="h1">3</div><div class="sm soft">пляшки зараз у вас</div></div><div class="tintc col"><div class="h1 pri">+50</div><div class="sm soft">бонусів за жовтень</div></div></div>'
    steps = "".join('<div class="row"><div class="num">%d</div><div class="sm b" style="flex:1">%s</div></div>' % (i + 1, t) for i, t in enumerate(["Принесіть чисту тару", "Відскануйте код", "Бонуси одразу на картці"]))
    return phone(topbar("Поверни тару") + content(q, st, '<div class="col" style="gap:10px">%s</div>' % steps), tab=2)


def s_alert():
    ban = '<div style="background:var(--acc);color:var(--acc-ink);border-radius:var(--r);padding:16px" class="row">%s<div class="col" style="flex:1"><div class="h2">Повітряна тривога</div><div class="sm">Видача на паузі. Замовлення збережено</div></div></div>' % ic("alert", 30)
    order = ('<div class="card col" style="gap:10px"><div class="row">%s<div class="col" style="flex:1"><div class="b">Ваша вечеря · А-274</div><div class="sm soft">Була на 18:30</div></div></div>'
             '<div class="tintc row sm b" style="padding:10px 12px">%s<span>Нове вікно: одразу після відбою</span></div><div class="btn ghost s" style="align-self:stretch;height:44px">Змінити час або скасувати</div></div>') % (plate("chicken", 50), ic("clock", 18, "var(--pri)"))
    sh = '<div class="card row"><div class="circ p">%s</div><div class="col" style="flex:1"><div class="b">Найближче укриття</div><div class="sm soft">Показати маршрут</div></div>%s</div>' % (ic("pin", 20), ic("next", 18, "var(--soft)"))
    off = '<div class="card row"><div class="circ">%s</div><div class="col" style="flex:1"><div class="b">Картка працює без інтернету</div><div class="sm soft">Код збережено в телефоні</div></div></div>' % ic("cloud", 20, "var(--pri)")
    return phone(greet("Солом'янка", "Магазин на паузі") + content(ban, order, sh, off), tab=0)


def s_status():
    big = '<div class="hero" style="flex-direction:row;align-items:center;gap:14px"><div style="width:52px;height:52px;border-radius:50%%;background:var(--acc);color:var(--acc-ink);display:flex;align-items:center;justify-content:center;flex:none">%s</div><div class="col"><div class="h2">Працюємо від генератора</div><div class="sm" style="opacity:.9">Усе як завжди, до 22:00</div></div></div>' % ic("bolt", 26)
    items = [("Каси самообслуговування", "працюють", 0), ("Оплата карткою", "працює", 0), ("Віконце видачі", "працює", 0), ("Доставка додому", "затримка до 20 хв", 1), ("Кава і гарячі страви", "працюють", 0)]
    rows = "".join('<div class="li"><div class="dot%s"></div><div class="b" style="flex:1">%s</div><div class="sm %s">%s</div></div>' % (" w" if w else "", n, "b" if w else "soft", s) for n, s, w in items)
    return phone(topbar("Магазин зараз") + content(big, '<div class="card col" style="padding:4px 14px">%s</div>' % rows, '<div class="row sm soft">%s<span>Оновлено 2 хвилини тому</span></div>' % ic("clock", 15),
                                                '<div class="tintc row">%s<div class="col" style="flex:1"><div class="b">Сповіщати про зміни</div><div class="sm soft">Тривога, світло, графік роботи</div></div><div style="width:46px;height:28px;border-radius:99px;background:var(--pri);position:relative;flex:none"><div style="position:absolute;right:3px;top:3px;width:22px;height:22px;border-radius:50%%;background:#fff"></div></div></div>' % ic("alert", 22, "var(--pri)")), tab=0)


def s_simple():
    def b(i, t, cls=""):
        return '<div class="btn %s" style="flex:none;height:112px;font-size:24px;justify-content:flex-start;gap:18px;padding:0 24px">%s%s</div>' % (cls, ic(i, 36), t)
    body = content('<div class="col" style="gap:6px;margin-top:10px"><div class="h1" style="font-size:38px">Вітаємо!</div><div style="font-size:20px" class="soft">Що бажаєте зробити?</div></div>',
                   b("cart", "Замовити вечерю"), b("card", "Моя картка"), b("phone", "Подзвонити нам", "ghost"), '<div class="sp"></div>',
                   '<div class="row" style="justify-content:center;font-size:17px;padding-bottom:26px" class="b"><span class="b pri">Перейти у звичайний режим</span></div>', style="gap:18px")
    return phone(body)


def s_combo():
    def c(k, n, d, p, on=0):
        return ('<div class="card row" style="%s"><div class="tile" style="width:78px;height:78px">%s</div><div class="col" style="flex:1;gap:3px"><div class="b" style="font-size:16px">%s</div><div class="sm soft">%s</div></div>'
                '<div class="h2 pri">%d ₴</div></div>') % ("border:2px solid var(--pri)" if on else "", plate(k, 66), n, d, p)
    chips = '<div class="hs"><div class="chip on">До 100 ₴</div><div class="chip">Обід</div><div class="chip">Сніданок</div><div class="chip">Хелсі</div></div>'
    note = '<div class="tintc row sm b">%s<span>Готово за 2 хвилини · забираєте без черги</span></div>' % ic("bolt", 18, "var(--pri)")
    return phone(topbar("Комбо дня") + content(chips, c("sandwich", "Перекус + напій", "Сендвіч або сирники та узвар", 79, 1), c("soup", "Обід студента", "Суп, друга страва, напій", 119), c("coffee", "Кава + випічка", "Капучино та круасан", 59), c("salad", "Хелсі-бокс", "Салат, йогурт, вода", 99), note), tab=0)


def s_builder():
    def o(k, n, on=0):
        return '<div class="col" style="flex:1;gap:6px;align-items:center"><div class="tile" style="width:100%%;height:96px;%s">%s</div><div class="sm b" style="text-align:center">%s</div></div>' % ("outline:3px solid var(--pri)" if on else "", plate(k, 78), n)
    body = content('<div class="h2">1. Оберіть перекус</div>', '<div class="row" style="align-items:flex-start;gap:10px">%s%s%s</div>' % (o("sandwich", "Сендвіч", 1), o("syrnyky", "Сирники"), o("salad", "Салат")),
                   '<div class="h2" style="margin-top:6px">2. Оберіть напій</div>', '<div class="hs" style="flex-wrap:wrap"><div class="chip on">Узвар</div><div class="chip">Капучино</div><div class="chip">Чай</div><div class="chip">Вода</div></div>',
                   '<div class="h2" style="margin-top:6px">3. Де забрати</div>', '<div class="card row"><div class="rad on"></div><div class="col" style="flex:1"><div class="b">Полиця «Комбо» біля входу</div><div class="sm soft">Готово за 2 хвилини</div></div></div>',
                   '<div class="sp"></div>', '<div class="row"><div class="soft">Разом</div><div class="sp"></div><div class="h1">79 ₴</div></div>')
    return phone(topbar("Перекус + напій") + body, bottom='<div class="bottom"><div class="btn">Оплатити 79 ₴</div></div>')


def s_payqr():
    top = ('<div style="background:var(--pri);color:var(--pri-ink);padding:44px 22px 26px;border-radius:0 0 28px 28px;display:flex;flex-direction:column;gap:8px;align-items:center;text-align:center;flex:none">'
           '<div style="width:56px;height:56px;border-radius:50%%;background:var(--acc);color:var(--acc-ink);display:flex;align-items:center;justify-content:center">%s</div>'
           '<div class="h1">Оплачено · 79 ₴</div><div class="sm" style="opacity:.9">Комбо буде готове о 13:12</div></div>') % ic("check", 30, w=3)
    q = '<div class="card col" style="align-items:center;gap:10px;padding:18px">%s<div class="b" style="text-align:center">Відскануйте код на полиці «Комбо»</div><div class="sm soft">або покажіть на касі самообслуговування</div></div>' % qr(23, 168)
    b = '<div class="tintc row">%s<div class="b" style="flex:1">+4 бонуси на картку</div></div>' % ic("gift", 20, "var(--pri)")
    return phone(top + content(q, b, style="padding-top:16px"), bottom='<div class="bottom"><div class="btn ghost">Повторити завтра</div></div>', safe=False)


def s_home_feed():
    st = [("chicken", "Меню дня"), ("sandwich", "Комбо"), ("deruny", "Сусіди"), ("cheese", "Фермери"), ("coffee", "Акції")]
    stories = '<div class="hs" style="gap:12px">%s</div>' % "".join(
        '<div class="col" style="align-items:center;gap:5px;flex:none"><div style="width:66px;height:66px;border-radius:50%%;border:3px solid var(--pri);padding:3px;display:flex"><div class="tile" style="flex:1;border-radius:50%%">%s</div></div><div class="xs b">%s</div></div>' % (plate(k, 46), n) for k, n in st)
    c1 = ('<div class="card col" style="padding:10px;gap:10px"><div class="tile" style="height:170px;position:relative">%s<div class="badge" style="position:absolute;left:10px;top:10px;background:var(--acc);color:var(--acc-ink)">Вечеря сьогодні</div></div>'
          '<div class="row" style="padding:0 4px 4px"><div class="col" style="flex:1"><div class="h2">Курка з гречкою</div><div class="sm soft">Готова до 18:30 · 149 ₴</div></div><div class="btn s" style="align-self:center">Замовити</div></div></div>') % plate("chicken", 150)
    c2 = '<div class="card row" style="padding:10px"><div class="tile" style="width:76px;height:76px">%s</div><div class="col" style="flex:1;gap:3px"><div class="xs b pri">ГОЛОСУВАННЯ</div><div class="b">Що додати в меню?</div><div class="sm soft">Лідирують голубці · 46%%</div></div></div>' % plate("holubtsi", 64)
    c3 = '<div class="card row" style="padding:10px"><div class="tile" style="width:76px;height:76px">%s</div><div class="col" style="flex:1;gap:3px"><div class="xs b pri">РЕЦЕПТ ВІД СУСІДА</div><div class="b">Деруни як у бабусі</div><div class="sm soft">Галина, буд. 175</div></div></div>' % plate("deruny", 64)
    return phone(greet("Солом'янка", "Сьогодні у нас") + content(stories, c1, c2, c3), tab=0)


def s_home_card():
    card = ('<div class="hero" style="gap:10px"><div class="row"><div class="col" style="flex:1"><div class="eyebrow" style="opacity:.85">Покажіть на касі</div><div class="h2">1 240 бонусів</div></div>%s</div>'
            '<div style="background:#fff;border-radius:12px;padding:12px 14px">%s</div></div>') % (ic("users", 26), barcode(286, 64, 3))
    def t(i, a):
        return '<div class="card col" style="gap:10px;padding:16px"><div class="circ p">%s</div><div class="b">%s</div></div>' % (ic(i, 20), a)
    grid = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">%s%s%s%s</div>' % (t("cart", "Замовити вечерю"), t("bolt", "Комбо дня"), t("book", "Рецепти"), t("list", "Наш список"))
    order = '<div class="tintc row">%s<div class="col" style="flex:1"><div class="b">Замовлення А-274</div><div class="sm soft">Буде готове до 18:30</div></div><div class="badge" style="background:var(--pri);color:var(--pri-ink);align-self:center">Збираємо</div></div>' % plate("chicken", 46)
    vote = '<div class="card row"><div class="circ p">%s</div><div class="col" style="flex:1"><div class="b">Голосування тижня</div><div class="sm soft">Яку страву додати в меню?</div></div>%s</div>' % (ic("thumb", 20), ic("next", 18, "var(--soft)"))
    return phone(greet("Добрий вечір", "Олено") + content(card, grid, order, vote), tab=0)


SCREENS = {
    "home": s_home, "dish": s_dish, "time": s_time, "ready": s_ready, "recipe": s_recipe, "ingr": s_ingr, "cart": s_cart,
    "family": s_family, "flist": s_flist, "bonus": s_bonus, "neighbor": s_neighbor, "vote": s_vote, "voteres": s_voteres,
    "product": s_product, "farmer": s_farmer, "tara": s_tara, "alert": s_alert, "status": s_status, "simple": s_simple,
    "combo": s_combo, "builder": s_builder, "payqr": s_payqr, "homefeed": s_home_feed, "homecard": s_home_card,
}


def page(theme, body, w, h, extra=""):
    return '<!doctype html><html lang="uk"><head><meta charset="utf-8">%s<style>:root{%s}%s%s html,body{width:%dpx;height:%dpx;overflow:hidden}</style></head><body>%s</body></html>' % (FONTS, THEMES[theme], CSS, extra, w, h, body)


jobs = []
for name, fn in SCREENS.items():
    jobs.append(("a-" + name, page("a", fn(), 390, 844), 390, 844))
for th in ("b", "c"):
    for name in ("home", "dish", "ready"):
        jobs.append((th + "-" + name, page(th, SCREENS[name](), 390, 844), 390, 844))

if __name__ == "__main__":
    import json
    for n, html, w, h in jobs:
        open(os.path.join(OUT, n + ".html"), "w", encoding="utf-8").write(html)
    json.dump([(n, w, h) for n, _, w, h in jobs], open(os.path.join(OUT, "jobs.json"), "w"))
    print(len(jobs), "screens")
