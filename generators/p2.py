"""Прототип v2: стиль із бордів замовника, реальні фото, два режими бренду."""
import os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import qr, barcode

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out2")
os.makedirs(OUT, exist_ok=True)
IMG = "../../img/"

THEMES = {
    "pulse": dict(bg="#F7EEE2", surface="#FFFAF3", ink="#142A1F", soft="#5D6B60", line="#E8DCCB",
                  brand="#23402C", deep="#0E2319", onbrand="#FFFFFF", tint="#F3DCC6", tint2="#DFE4D2",
                  accent="#FA7F52", photo="#EEC39E",
                  name="Пульс Солом'янки", slogan="Більше, ніж магазин. Їжа поруч."),
    "fd": dict(bg="#F5F3EA", surface="#FFFFFE", ink="#2C3B40", soft="#687A7F", line="#E2E0D6",
               brand="#485C62", deep="#3A4B50", onbrand="#FFFFFF", tint="#DCE7E9", tint2="#E6ECE6",
               accent="#DBC3A6", photo="#A7C1C6",
               name="Food Daily", slogan="Готуй смачно і живи простіше"),
}
TOKENS = ["bg", "surface", "ink", "soft", "line", "brand", "deep", "onbrand", "tint", "tint2", "accent", "photo"]

ICONS = dict(gen.ICONS)
ICONS.update({
    "coffee": '<path d="M4 8h13v5a6 6 0 0 1-6 6h-1a6 6 0 0 1-6-6z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 3v2M12 3v2"/>',
    "locker": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 3v18M8 11v2M16 11v2"/>',
    "bag": '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "truck": '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="1.8"/><circle cx="17.5" cy="18" r="1.8"/>',
    "window": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 12h18M9 16h6"/>',
    "dish": '<path d="M3 15h18M5 15a7 7 0 0 1 14 0M12 6v2M2 18h20"/>',
    "paw": '<circle cx="7" cy="9" r="1.8"/><circle cx="12" cy="6.5" r="1.8"/><circle cx="17" cy="9" r="1.8"/><path d="M12 12c-3 0-5 3.5-5 5.5S9 20 12 19s5 .5 5-1.5S15 12 12 12z"/>',
    "map": '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
})


def ic(n, s=22, c="currentColor", w=2):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" style="flex:none">%s</svg>' % (s, s, c, w, ICONS[n]))


FONT_CSS = "".join(
    "@font-face{font-family:'Onest';font-weight:%d;src:url('../node_modules/@fontsource/onest/files/onest-%s-%d-normal.woff2') format('woff2');%s}"
    % (w, sub, w, "unicode-range:U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116;" if sub == "cyrillic" else "")
    for w in (400, 500, 600, 700, 800) for sub in ("latin", "cyrillic"))

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ddd;font-family:'Onest',sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
.phone{width:390px;height:844px;background:var(--bg);position:relative;overflow:hidden;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:12px;padding:52px 20px 12px}
.content{flex:1;overflow:hidden;padding:4px 20px 16px;display:flex;flex-direction:column;gap:14px}
.bottom{padding:12px 20px 30px;background:var(--bg)}
h1{font-size:28px;line-height:1.12;font-weight:700;letter-spacing:-.3px}
h2{font-size:20px;line-height:1.2;font-weight:700;letter-spacing:-.2px}
h3{font-size:16px;line-height:1.25;font-weight:600}
.t{font-size:14px;line-height:1.4}
.s{font-size:13px;line-height:1.35;color:var(--soft)}
.xs{font-size:12px;line-height:1.3;color:var(--soft)}
.b{font-weight:700}
.row{display:flex;align-items:center;gap:12px}
.col{display:flex;flex-direction:column;gap:4px}
.grow{flex:1;min-width:0}
.card{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:14px}
.tint{background:var(--tint);border-radius:20px;padding:14px}
.tint2{background:var(--tint2);border-radius:20px;padding:14px}
.btn{height:54px;border-radius:16px;background:var(--brand);color:var(--onbrand);display:flex;align-items:center;justify-content:center;gap:8px;font-size:16px;font-weight:700}
.btn.ghost{background:transparent;color:var(--brand);border:1.5px solid var(--brand)}
.btn.sm{height:40px;font-size:14px;border-radius:12px;padding:0 16px}
.chip{height:36px;padding:0 15px;border-radius:18px;border:1px solid var(--line);background:var(--surface);display:inline-flex;align-items:center;font-size:13px;font-weight:600;white-space:nowrap;flex:none}
.chip.on{background:var(--brand);border-color:var(--brand);color:var(--onbrand)}
.ib{width:40px;height:40px;border-radius:20px;background:var(--surface);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;flex:none}
.ib.p{background:var(--brand);border-color:var(--brand);color:var(--onbrand)}
.ib.sm{width:32px;height:32px}
.ph{display:block;object-fit:cover;background:var(--photo);flex:none}
.tabbar{display:flex;background:var(--surface);border-top:1px solid var(--line);padding:10px 8px 26px}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;font-weight:600;color:var(--soft)}
.tab.on{color:var(--brand)}
.rad{width:22px;height:22px;border-radius:11px;border:2px solid var(--line);flex:none}
.rad.on{border:7px solid var(--brand)}
.opt{display:flex;align-items:center;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:16px}
.opt.on{border:2px solid var(--brand);padding:15px}
.badge{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 10px;border-radius:13px;background:var(--accent);color:var(--ink);font-size:12px;font-weight:700;align-self:flex-start}
.mark{font-weight:800;font-size:17px;letter-spacing:-.2px;color:var(--brand)}
.price{font-size:15px;font-weight:700}
.div{height:1px;background:var(--line)}
.tog{width:46px;height:28px;border-radius:14px;background:var(--brand);padding:3px;display:flex;justify-content:flex-end;flex:none}
.tog i{width:22px;height:22px;border-radius:11px;background:var(--onbrand);display:block}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.dark{background:var(--deep);color:var(--onbrand);border-radius:22px;padding:18px}
.dark .s,.dark .xs{color:var(--onbrand);opacity:.78}
"""


def theme_css(t):
    th = THEMES[t]
    return ":root{" + "".join("--%s:%s;" % (k, th[k]) for k in TOKENS) + "}"


def page(theme, body, w=390, h=844, extra=""):
    return ("<!doctype html><html><head><meta charset='utf-8'><style>" + FONT_CSS + theme_css(theme) + BASE_CSS + extra +
            "</style></head><body>" + body + "</body></html>")


# ---------- building blocks ----------
TABS = [("home", "Головна", 2), ("dish", "Меню", 3), ("card", "Картка", 13), ("user", "Профіль", 14)]


def tabbar(active):
    out = []
    for i, (icn, lab, go) in enumerate(TABS):
        on = " on" if i == active else ""
        dg = "" if i == active else ' data-go="%d"' % go
        out.append('<div class="tab%s"%s>%s<span>%s</span></div>' % (on, dg, ic(icn, 24), lab))
    return '<div class="tabbar">' + "".join(out) + "</div>"


def phone(body, tab=None, bottom=""):
    return ('<div class="phone">' + body + (('<div class="bottom">' + bottom + "</div>") if bottom else "") +
            (tabbar(tab) if tab is not None else "") + "</div>")


def top(title, back=None, right=""):
    b = '<div class="ib" data-go="%d">%s</div>' % (back, ic("back", 20)) if back else ""
    return '<div class="top">%s<h2 class="grow">%s</h2>%s</div>' % (b, title, right)


def content(*parts, style=""):
    return '<div class="content" style="%s">%s</div>' % (style, "".join(parts))


def img(key, w, h, r=16, style=""):
    return '<img class="ph" data-img="%s" src="%s%s.jpg" style="width:%spx;height:%spx;border-radius:%spx;%s">' % (
        key, IMG, key, w, h, r, style)


def mark(size=17, color=None):
    st = "font-size:%dpx;" % size + ("color:%s;" % color if color else "")
    return '<span class="mark" data-var="brand/name" style="%s">{NAME}</span>' % st


def dishrow(key, name, meta, price, go=None):
    g = ' data-go="%d"' % go if go else ""
    return ('<div class="card row" style="padding:10px;gap:12px"%s>%s<div class="col grow"><h3>%s</h3><span class="s">%s</span>'
            '<span class="price" style="margin-top:4px">%s</span></div><div class="ib sm p">%s</div></div>') % (
        g, img(key, 76, 76, 14), name, meta, price, ic("plus", 16))


# ---------- screens ----------
def s01():
    photos = '<div class="row" style="gap:8px">' + img("d_bowl", 160, 150, 20) + '<div class="col" style="gap:8px">' + img(
        "d_borsch", 162, 71, 16) + img("d_syrnyky", 162, 71, 16) + "</div></div>"
    body = ('<div class="top">' + mark(18) + '<span class="xs" style="margin-left:auto">назва ще не затверджена</span></div>' +
            content(photos,
                    '<h1 style="margin-top:6px">Кухня, продукти й кава біля дому</h1>',
                    '<p class="t" style="color:var(--soft)" data-var="brand/slogan">{SLOGAN}</p>',
                    '<h3 style="margin-top:6px">Оберіть картку</h3>',
                    '<div class="opt on" data-go="2"><div class="rad on"></div><div class="col grow"><h3>Сімейна</h3><span class="s">Один рахунок бонусів на всю родину</span></div>%s</div>' % ic("users", 22),
                    '<div class="opt" data-go="2"><div class="rad"></div><div class="col grow"><h3>Студентська</h3><span class="s">Знижки за студентським квитком</span></div>%s</div>' % ic("star", 22),
                    '<div class="opt" data-go="2"><div class="rad"></div><div class="col grow"><h3>Індивідуальна</h3><span class="s">Бонуси з кожної покупки</span></div>%s</div>' % ic("user", 22),
                    style="gap:12px"))
    return phone(body, bottom='<div class="btn" data-go="2">Продовжити</div>')


def s02():
    head = '<div class="top">' + mark(18) + '<div class="ib" style="margin-left:auto;background:var(--accent);border-color:var(--accent);font-weight:700;font-size:15px">О</div></div>'
    feat = ('<div class="card" style="padding:0;overflow:hidden" data-go="4">' + img("d_bowl", 350, 170, 0) +
            '<div class="row" style="padding:14px 16px 16px;align-items:flex-end"><div class="col grow"><span class="xs">Кухня сьогодні</span><h3>Боул з куркою та овочами</h3><span class="s">420 ккал · готуємо 15 хв</span></div>'
            '<div class="btn sm" data-go="3">Меню</div></div></div>')
    tiles = '<div class="row" style="gap:8px;align-items:stretch">' + "".join(
        '<div class="tint2 col" style="flex:1;padding:12px 10px;gap:8px;border-radius:16px"%s>%s<span style="font-size:12px;font-weight:600;line-height:1.2">%s</span></div>' % (
            (' data-go="%d"' % g) if g else "", ic(i, 22, "var(--brand)"), l)
        for i, l, g in [("dish", "Готова їжа", 3), ("bag", "Продукти", 5), ("coffee", "Кава з собою", 0), ("locker", "Комірка 24/7", 7)]) + "</div>"
    order = ('<div class="tint row" style="padding:12px 14px" data-go="9">%s<div class="col grow"><h3>Замовлення А-274</h3><span class="s">Готуємо, буде о 18:30</span></div>%s</div>' % (
        '<div class="ib" style="background:var(--surface);border:none">%s</div>' % ic("clock", 20, "var(--brand)"), ic("next", 18, "var(--soft)")))
    body = head + content('<div class="col" style="gap:2px"><span class="s">Привіт, Олено!</span><h1>Що сьогодні на обід?</h1></div>',
                          '<div class="card row" style="padding:12px 14px;border-radius:16px" data-go="3">%s<span class="s">Що приготувати сьогодні?</span></div>' % ic("search", 18, "var(--soft)"),
                          feat, tiles, order, style="gap:14px")
    return phone(body, tab=0)


MENU = [("d_bowl", "Боул з куркою та овочами", "380 г, 420 ккал", "149 ₴", 4),
        ("d_borsch", "Борщ зі сметаною", "400 мл", "119 ₴", None),
        ("d_soup", "Крем-суп гарбузовий", "350 мл", "99 ₴", None),
        ("d_holubtsi", "Голубці", "2 шт, 320 г", "139 ₴", None),
        ("d_deruny", "Деруни зі сметаною", "280 г", "109 ₴", None),
        ("d_salad", "Салат з буряком і морквою", "220 г", "89 ₴", None)]


def s03():
    chips = '<div class="row" style="gap:8px">' + "".join('<span class="chip%s">%s</span>' % (" on" if i == 1 else "", c) for i, c in enumerate(["Сніданки", "Обід", "Супи", "Комбо"])) + "</div>"
    rows = "".join(dishrow(k, n, m, p, g or 4) for k, n, m, p, g in MENU[:5])
    body = top("Меню кухні", back=2) + content(chips, '<span class="s">Одне меню на день, готуємо тут, у магазині</span>', rows, style="gap:10px")
    return phone(body, tab=1)


def s04():
    hero = '<div style="position:relative;height:300px;flex:none">' + img("d_bowl", 390, 300, 0, "position:absolute;left:0;top:0") + \
           '<div class="ib" data-go="3" style="position:absolute;left:20px;top:52px">%s</div></div>' % ic("back", 20)
    nut = '<div class="row" style="gap:8px">' + "".join(
        '<div class="tint2 col" style="flex:1;align-items:center;padding:10px 4px;border-radius:14px;gap:2px"><span class="b" style="font-size:15px">%s</span><span class="xs">%s</span></div>' % (a, b)
        for a, b in [("420", "ккал"), ("32 г", "білки"), ("14 г", "жири"), ("40 г", "вуглеводи")]) + "</div>"
    body = hero + content('<span class="badge">%sОвочі від локальних фермерів</span>' % ic("leaf", 14),
                          '<h1>Боул з куркою та овочами</h1>',
                          '<span class="s">380 г · готуємо 15 хв</span>',
                          '<p class="t">Курка, нут, авокадо, томати й зелень. Готуємо на кухні магазину щодня.</p>', nut,
                          style="gap:10px;padding-top:18px")
    bottom = ('<div class="row"><div class="card row" style="padding:0 14px;height:54px;border-radius:16px;gap:16px">%s<span class="b">1</span>%s</div>'
              '<div class="btn grow" data-go="6">Додати · 149 ₴</div></div>') % (ic("minus", 18), ic("plus", 18))
    return phone(body, bottom=bottom)


GROC = [("g_tomato", "Томати на гілці", "1 кг", "89 ₴"), ("g_gala", "Яблука Гала", "1 кг", "54 ₴"),
        ("g_potato", "Картопля", "1 кг", "22 ₴"), ("g_carrots", "Морква", "1 кг", "19 ₴"),
        ("g_beet", "Буряк", "1 кг", "18 ₴"), ("g_banana", "Банани", "1 кг", "62 ₴")]


def s05():
    chips = '<div class="row" style="gap:8px">' + "".join('<span class="chip%s">%s</span>' % (" on" if i == 0 else "", c) for i, c in enumerate(["Овочі й фрукти", "Молочне", "Хліб", "Для тварин"])) + "</div>"
    grid = '<div class="grid2">' + "".join(
        '<div class="card col" style="padding:10px;gap:6px;border-radius:18px">%s<span style="font-size:14px;font-weight:600">%s</span><div class="row" style="justify-content:space-between"><span class="s">%s</span><span class="price">%s</span></div></div>' % (
            img(k, 153, 96, 12, "object-fit:contain;background:#FFFFFF"), n, w, p) for k, n, w, p in GROC[:4]) + "</div>"
    body = top("Продукти", back=2) + content(
        '<div class="card row" style="padding:12px 14px;border-radius:16px">%s<span class="s">Знайти продукт</span></div>' % ic("search", 18, "var(--soft)"),
        chips,
        '<div class="tint row" style="padding:12px 14px">%s<div class="col grow"><h3>Від фермерів поруч</h3><span class="s">Щодня свіже з Київщини</span></div>%s</div>' % (ic("leaf", 22, "var(--brand)"), ic("next", 18, "var(--soft)")),
        grid, '<span class="xs">Ціни умовні, реальні підтягнемо з BAS</span>', style="gap:12px")
    return phone(body, tab=1)


def s06():
    items = [("d_bowl", "Боул з куркою", "2 порції", "298 ₴"), ("d_borsch", "Борщ зі сметаною", "1 порція", "119 ₴"), ("g_tomato", "Томати на гілці", "1 кг", "89 ₴")]
    rows = "".join('<div class="card row" style="padding:10px">%s<div class="col grow"><h3>%s</h3><span class="s">%s</span></div><span class="price">%s</span></div>' % (
        img(k, 60, 60, 12, "object-fit:%s;background:%s" % (("contain", "#FFFFFF") if k.startswith("g_") else ("cover", "var(--photo)"))), n, m, p) for k, n, m, p in items)
    summ = ('<div class="col" style="gap:10px;margin-top:auto"><div class="row"><span class="t grow" style="color:var(--soft)">Бонусів нарахуємо</span><span class="b" style="color:var(--brand)">+25</span></div>'
            '<div class="div"></div><div class="row"><h2 class="grow">Разом</h2><h2>506 ₴</h2></div></div>')
    body = top("Кошик", back=3) + content(rows, summ, style="gap:10px")
    return phone(body, bottom='<div class="btn" data-go="7">Оформити замовлення</div>')


def s07():
    opts = [("window", "Віконце видачі", "Без черги, безкоштовно", True), ("locker", "Комірка-холодильник 24/7", "Заберіть самі за кодом", False), ("truck", "Кур'єр", "30–45 хв, від 49 ₴", False)]
    o = "".join('<div class="opt%s"><div class="rad%s"></div><div class="col grow"><h3>%s</h3><span class="s">%s</span></div>%s</div>' % (
        " on" if on else "", " on" if on else "", t, s, ic(i, 22, "var(--brand)")) for i, t, s, on in opts)
    days = '<div class="row" style="gap:8px"><span class="chip on">Сьогодні</span><span class="chip">Завтра</span></div>'
    slots = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">' + "".join(
        '<span class="chip%s" style="justify-content:center;height:42px">%s</span>' % (" on" if t == "18:30" else "", t) for t in ["17:30", "18:00", "18:30", "19:00", "19:30", "20:00"]) + "</div>"
    body = top("Отримання", back=6) + content('<h3>Як отримати</h3>', o, '<h3 style="margin-top:6px">Коли</h3>', days, slots, style="gap:10px")
    return phone(body, bottom='<div class="btn" data-go="8">Далі до оплати</div>')


def s08():
    opts = [("card", "Карткою зараз", "Apple Pay, Google Pay, картка", True), ("bag", "При отриманні", "Карткою або готівкою", False)]
    o = "".join('<div class="opt%s"><div class="rad%s"></div><div class="col grow"><h3>%s</h3><span class="s">%s</span></div>%s</div>' % (
        " on" if on else "", " on" if on else "", t, s, ic(i, 22, "var(--brand)")) for i, t, s, on in opts)
    bon = '<div class="tint2 row" style="padding:14px 16px"><div class="col grow"><h3>Списати бонуси</h3><span class="s">На сімейній картці 1 240</span></div><div class="tog"><i></i></div></div>'
    summ = ('<div class="card col" style="gap:8px;margin-top:auto"><div class="row"><span class="s grow">Отримання</span><span class="t b">Віконце, сьогодні 18:30</span></div>'
            '<div class="row"><span class="s grow">3 позиції</span><span class="t b">506 ₴</span></div></div>')
    body = top("Оплата", back=7) + content(o, bon, summ, style="gap:10px")
    return phone(body, bottom='<div class="btn" data-go="9">Оплатити 506 ₴</div>')


def s09():
    hero = '<div class="dark col" style="gap:6px"><span class="s">Замовлення А-274</span><h1 style="font-size:26px">Готуємо ваше замовлення</h1><span class="s">Віконце видачі, о 18:30</span></div>'
    steps = [("Прийнято", "18:02", 2), ("Готуємо на кухні", "зараз", 1), ("Готово до видачі", "о 18:30", 0), ("Видано", "", 0)]
    tl = '<div class="card col" style="gap:14px;padding:16px">' + "".join(
        '<div class="row">%s<div class="col grow"><h3 style="%s">%s</h3>%s</div></div>' % (
            ('<div class="ib sm p">%s</div>' % ic("check", 16)) if st == 2 else ('<div class="ib sm" style="background:var(--tint);border:2px solid var(--brand)"></div>' if st == 1 else '<div class="ib sm"></div>'),
            "" if st else "color:var(--soft)", t, ('<span class="s">%s</span>' % s) if s else "") for t, s, st in steps) + "</div>"
    demo = ('<div class="col" style="gap:8px;margin-top:auto"><span class="s">Показати, як буде з іншими способами</span><div class="row" style="gap:8px">'
            '<span class="chip" data-go="10">Віконце</span><span class="chip" data-go="11">Комірка</span><span class="chip" data-go="12">Кур\'єр</span></div></div>')
    body = top("Статус", back=2) + content(hero, tl, demo, style="gap:12px")
    return phone(body, bottom='<div class="btn ghost" data-go="7">Змінити час</div>')


def qrcard(text):
    return ('<div class="card col" style="align-items:center;gap:10px;padding:22px">%s<span style="font-size:28px;font-weight:800;letter-spacing:3px">А-274</span><span class="s" style="text-align:center">%s</span></div>' % (qr(274 if "віконці" in text else 1414, 170), text))


def ready(title, sub, card, extra):
    hero = ('<div style="background:var(--deep);color:var(--onbrand);padding:62px 20px 26px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center">'
            '<div class="ib" style="width:56px;height:56px;border-radius:28px;background:var(--accent);border:none;color:var(--ink)">%s</div>'
            '<h1 style="font-size:26px">%s</h1><span class="s" style="color:var(--onbrand);opacity:.8">%s</span></div>') % (ic("check", 28, w=3), title, sub)
    return phone(hero + content(card, extra, style="padding-top:18px;gap:12px"), bottom='<div class="btn ghost" data-go="2">На головну</div>')


def s10():
    return ready("Готово у віконці", "Чекаємо до 19:30", qrcard("Покажіть код у віконці видачі"),
                 '<div class="tint2 row" style="padding:12px 16px">%s<span class="t b">+25 бонусів на сімейну картку</span></div>' % ic("gift", 20, "var(--brand)"))


def s11():
    return ready("Комірка №14", "Готово, зберігаємо до 21:00", qrcard("Відскануйте код на дверцятах комірки"),
                 '<div class="card row" style="padding:12px 16px">%s<div class="col"><h3>Холодильна комірка</h3><span class="s">Біля входу ліворуч, працює 24/7</span></div></div>' % ic("pin", 20, "var(--brand)"))


def s12():
    mapb = ('<div style="height:260px;flex:none;background:var(--photo);position:relative;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px">'
            '<div class="ib" data-go="9" style="position:absolute;left:20px;top:52px">%s</div>%s<span class="t b" style="color:var(--ink)">Тут буде карта з кур\'єром</span></div>') % (ic("back", 20), ic("map", 30, "var(--ink)"))
    body = mapb + content('<h1 style="font-size:26px">Кур\'єр уже їде</h1>', '<div class="row" style="gap:8px">%s<span class="s">Буде приблизно о 18:45</span></div>' % ic("clock", 16, "var(--soft)"),
                          '<div class="card row">%s<div class="col grow"><h3>Максим</h3><span class="s">Кур\'єр магазину</span></div><div class="ib p">%s</div></div>' % (
                              '<div class="ib" style="background:var(--accent);border:none;font-weight:700">М</div>', ic("phone", 18)),
                          '<div class="card col"><span class="s">Адреса</span><h3>вул. Борщагівська, [номер], кв. [номер]</h3></div>',
                          '<div class="tint2 row" style="padding:12px 16px">%s<span class="t b">Код для кур\'єра: А-274</span></div>' % ic("card", 18, "var(--brand)"),
                          style="padding-top:18px;gap:10px")
    return phone(body, bottom='<div class="btn ghost" data-go="2">На головну</div>')


def s13():
    card = ('<div class="dark col" style="gap:12px;padding:18px 18px 16px"><div class="row">' + mark(17, "var(--onbrand)") + '<span class="s" style="margin-left:auto">Сімейна</span></div>'
            '<span class="s" style="margin-top:-4px">Родина Коваленків</span>'
            '<div style="background:#FFFFFF;border-radius:12px;padding:12px 14px;display:flex;justify-content:center">%s</div>'
            '<span class="xs" style="text-align:center;letter-spacing:2px">2200 4417 0935</span></div>') % barcode(282, 54)
    av = '<div class="row" style="gap:8px">' + "".join('<div class="ib" style="background:%s;border:none;font-weight:700;color:%s">%s</div>' % (bg, c, l) for l, bg, c in [
        ("О", "var(--accent)", "var(--ink)"), ("А", "var(--brand)", "var(--onbrand)"), ("М", "var(--tint)", "var(--ink)"), ("Б", "var(--tint2)", "var(--ink)")]) + \
         '<div class="ib">%s</div><span class="s" style="margin-left:4px">4 учасники</span></div>' % ic("plus", 18)
    body = top("Картка", back=2) + content(card, '<div class="col" style="gap:0"><span class="s">Спільний баланс</span><span style="font-size:32px;font-weight:800;letter-spacing:-.5px">1 240 бонусів</span></div>', av,
                                          '<div class="card col" style="gap:10px"><span class="s">Інші типи карток</span><div class="row" style="gap:8px"><span class="chip">Студентська</span><span class="chip">Індивідуальна</span></div></div>',
                                          style="gap:14px")
    return phone(body, tab=2)


def s14():
    items = [("list", "Мої замовлення", "Останнє: А-274", None), ("pin", "Адреси доставки", "", None), ("card", "Тип картки", "Сімейна", 1),
             ("alert", "Сповіщення", "", None), ("check", "Простий режим", "Великий шрифт і менше кнопок", None)]
    li = '<div class="card col" style="padding:6px 14px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:10px 0"%s>%s<div class="col grow"><h3>%s</h3>%s</div>%s</div>' % (
            (' data-go="%d"' % g) if g else "", '<div class="ib sm" style="background:var(--tint2);border:none">%s</div>' % ic(i, 16, "var(--brand)"), t,
            ('<span class="xs">%s</span>' % s) if s else "", ic("next", 16, "var(--soft)")) for i, t, s, g in items) + "</div>"
    body = top("Профіль", back=2) + content('<div class="row"><div class="ib" style="width:60px;height:60px;border-radius:30px;background:var(--accent);border:none;font-size:22px;font-weight:800">О</div>'
                                            '<div class="col"><h2>Олена Коваленко</h2><span class="s">Сімейна картка</span></div></div>', li, style="gap:14px")
    return phone(body, tab=3)


SITE_CSS = """
.site{width:1440px;background:var(--bg);color:var(--ink)}
.wrap{padding:0 80px}
.nav{height:88px;display:flex;align-items:center;gap:40px}
.nav a{font-size:15px;font-weight:500;color:var(--ink);text-decoration:none}
.sec{padding:96px 80px 0}
.h-xl{font-size:68px;line-height:1.02;font-weight:700;letter-spacing:-1.6px}
.h-l{font-size:42px;line-height:1.08;font-weight:700;letter-spacing:-.8px}
.h-m{font-size:22px;line-height:1.2;font-weight:700;letter-spacing:-.2px}
.lead{font-size:19px;line-height:1.5;color:var(--soft)}
.p{font-size:16px;line-height:1.5;color:var(--soft)}
.sbtn{height:56px;padding:0 26px;border-radius:16px;background:var(--brand);color:var(--onbrand);display:inline-flex;align-items:center;font-size:16px;font-weight:700}
.sbtn.ghost{background:transparent;color:var(--brand);border:1.5px solid var(--brand)}
.fact{display:flex;flex-direction:column;gap:2px}
.fact b{font-size:28px;font-weight:800;letter-spacing:-.5px}
.zcard{width:240px;display:flex;flex-direction:column;gap:12px}
.dcard{background:var(--surface);border:1px solid var(--line);border-radius:24px;overflow:hidden;width:302px;display:flex;flex-direction:column}
.way{flex:1;background:var(--surface);border-radius:24px;padding:28px;display:flex;flex-direction:column;gap:14px}
.lc{flex:1;border-radius:24px;padding:30px;display:flex;flex-direction:column;gap:14px;background:var(--surface);border:1px solid var(--line)}
.lc.dk{background:var(--deep);color:var(--onbrand);border-color:var(--deep)}
.lc.dk .p{color:var(--onbrand);opacity:.8}
.li{display:flex;gap:10px;align-items:flex-start;font-size:15px;line-height:1.45}
"""


def site():
    nav = ('<div class="nav wrap">' + mark(22) + '<span class="xs" style="margin-left:-28px;margin-top:4px">робоча назва</span>'
           '<div style="flex:1"></div><a>Кухня</a><a>Продукти</a><a>Як отримати</a><a>Картки</a><a>Застосунок</a>'
           '<span class="sbtn" style="height:46px;font-size:15px;border-radius:14px">Замовити онлайн</span></div>')
    hero = ('<div class="wrap" style="padding-top:48px;display:flex;gap:64px;align-items:flex-end">'
            '<div style="flex:1;display:flex;flex-direction:column;gap:22px"><h1 class="h-xl" style="max-width:720px">Кухня, продукти й кава біля дому</h1>'
            '<p class="lead" style="max-width:600px">Магазин на Солом\'янці, де можна взяти каву з віконця, пообідати з нашої кухні й забрати онлайн-замовлення з комірки навіть уночі.</p>'
            '<div style="display:flex;gap:12px;margin-top:6px"><span class="sbtn">Подивитися меню кухні</span><span class="sbtn ghost">Завантажити застосунок</span></div></div>'
            '<div style="width:420px;display:flex;flex-direction:column;gap:18px;padding-bottom:6px">'
            '<p class="p" data-var="brand/slogan" style="font-size:20px;color:var(--brand);font-weight:600">{SLOGAN}</p>'
            '<div style="display:flex;gap:28px"><div class="fact"><b>7:30</b><span class="s">кава з віконця</span></div><div class="fact"><b>24/7</b><span class="s">комірка видачі</span></div><div class="fact"><b>30 хв</b><span class="s">доставка районом</span></div></div></div></div>'
            '<div class="wrap" style="padding-top:44px">' + img("s_hero", 1280, 506, 28) + '</div>')
    zones = [("z_coffee", "Кава з собою", "Окреме віконце, без входу в магазин"), ("z_fresh", "Свіжі продукти", "Овочі, фрукти й молочне від фермерів поруч"),
             ("z_kitchen", "Готова їжа", "Сніданки, обіди й вечері з нашої кухні"), ("z_locker", "Комірка 24/7", "Замовте онлайн і заберіть, коли зручно"),
             ("z_space", "Простір для людей", "Кава, розетки, вода для собак")]
    zs = ('<div class="sec"><div style="display:flex;align-items:flex-end;gap:40px"><h2 class="h-l" style="flex:1">Що є в магазині</h2>'
          '<p class="p" style="width:420px">Планування та зони з концепції магазину. Візуалізації попередні.</p></div>'
          '<div style="display:flex;gap:20px;margin-top:36px">' + "".join(
              '<div class="zcard">%s<h3 class="h-m" style="font-size:19px">%s</h3><p class="p" style="font-size:15px">%s</p></div>' % (img(k, 240, 160, 20), t, d) for k, t, d in zones) + "</div></div>")
    dishes = [("d_bowl", "Боул з куркою та овочами", "380 г", "149 ₴"), ("d_borsch", "Борщ зі сметаною", "400 мл", "119 ₴"),
              ("d_syrnyky", "Сирники зі сметаною", "3 шт, 240 г", "99 ₴"), ("d_holubtsi", "Голубці", "2 шт, 320 г", "139 ₴")]
    ks = ('<div class="sec"><div style="display:flex;align-items:flex-end;gap:40px"><h2 class="h-l" style="flex:1">Кухня сьогодні</h2>'
          '<p class="p" style="width:420px">Одне меню на день: готуємо тут же, на кухні магазину. Асортимент ще узгоджуємо.</p></div>'
          '<div style="display:flex;gap:24px;margin-top:36px">' + "".join(
              '<div class="dcard">%s<div style="padding:18px 20px 20px;display:flex;flex-direction:column;gap:6px"><h3 class="h-m" style="font-size:18px">%s</h3>'
              '<div style="display:flex;align-items:center"><span class="s" style="flex:1">%s</span><span class="price" style="font-size:18px">%s</span></div></div></div>' % (img(k, 302, 196, 0), n, w, p) for k, n, w, p in dishes) + "</div></div>")
    ways = [("window", "Віконце видачі", "Підходите до віконця, показуєте код із застосунку й забираєте пакет. Без черги на касі."),
            ("locker", "Комірка-холодильник 24/7", "Як поштомат, тільки з холодом. Код відкриває вашу комірку в будь-яку годину."),
            ("truck", "Кур'єр по району", "Привеземо за 30–45 хвилин по Солом\'янці. Статус і час видно в застосунку.")]
    ws = ('<div class="sec"><div style="background:var(--tint);border-radius:36px;padding:64px"><h2 class="h-l">Як забрати замовлення</h2>'
          '<div style="display:flex;gap:20px;margin-top:36px">' + "".join(
              '<div class="way"><div class="ib" style="width:52px;height:52px;border-radius:16px;background:var(--brand);border:none">%s</div><h3 class="h-m">%s</h3><p class="p">%s</p></div>' % (ic(i, 26, "var(--onbrand)"), t, d) for i, t, d in ways) + "</div></div></div>")
    cards = [("Сімейна", "Один рахунок на всю родину", ["Бонуси всіх членів сім\'ї на одному балансі", "Додавайте до 5 людей", "Спільна історія замовлень"], True),
             ("Студентська", "За студентським квитком", ["Знижка на комбо з кухні", "Кава зі знижкою до 11:00", "Подвійні бонуси в сесію"], False),
             ("Індивідуальна", "Для себе", ["Бонуси з кожної покупки", "Персональні пропозиції", "Оплата бонусами до 50%"], False)]
    cs = ('<div class="sec"><div style="display:flex;align-items:flex-end;gap:40px"><h2 class="h-l" style="flex:1">Картка для своїх</h2>'
          '<p class="p" style="width:420px">Три типи карток. Умови бонусів умовні, затвердить замовник.</p></div><div style="display:flex;gap:20px;margin-top:36px">' + "".join(
              '<div class="lc%s"><h3 class="h-m" style="font-size:26px">%s</h3><p class="p">%s</p><div style="display:flex;flex-direction:column;gap:10px;margin-top:6px">%s</div></div>' % (
                  " dk" if dk else "", t, sub, "".join('<div class="li">%s<span>%s</span></div>' % (ic("check", 18, "var(--accent)" if dk else "var(--brand)"), x) for x in li)) for t, sub, li, dk in cards) + "</div></div>")
    app = ('<div class="sec"><div style="background:var(--deep);color:var(--onbrand);border-radius:36px;padding:64px 64px 0;display:flex;gap:60px;overflow:hidden">'
           '<div style="flex:1;display:flex;flex-direction:column;gap:18px;padding-bottom:64px"><h2 class="h-l">Замовляйте з телефона</h2>'
           '<p class="lead" style="color:var(--onbrand);opacity:.8;max-width:520px">Меню кухні на сьогодні, продукти з полиць, вибір віконця, комірки чи кур\'єра й картка лояльності в одному застосунку.</p>'
           '<div style="display:flex;gap:12px;margin-top:10px"><span class="sbtn" style="background:var(--onbrand);color:var(--deep)">App Store</span><span class="sbtn" style="background:var(--onbrand);color:var(--deep)">Google Play</span></div></div>'
           '<div data-clone="02" style="width:300px;height:520px;border-radius:32px 32px 0 0;background:var(--bg);flex:none;margin-right:40px"></div></div></div>')
    foot = ('<div class="wrap" style="padding-top:80px;padding-bottom:56px;display:flex;gap:60px;align-items:flex-start">'
            '<div style="flex:1;display:flex;flex-direction:column;gap:8px">' + mark(22) + '<span class="s">Retail Hub «Солом\'янка», мережа «Гермес»</span></div>'
            '<div style="display:flex;flex-direction:column;gap:6px;width:280px"><span class="b">Адреса</span><span class="s">вул. [адреса], Солом\'янка, Київ</span></div>'
            '<div style="display:flex;flex-direction:column;gap:6px;width:240px"><span class="b">Години</span><span class="s">Щодня 7:30–22:00</span><span class="s">Комірка видачі 24/7</span></div>'
            '<div style="display:flex;flex-direction:column;gap:6px;width:200px"><span class="b">Контакти</span><span class="s">+380 [номер]</span><span class="s">Instagram</span></div></div>')
    return '<div class="site">' + nav + hero + zs + ks + ws + cs + app + foot + "</div>"


SCREENS = [(1, "Вибір картки", s01), (2, "Головна", s02), (3, "Меню кухні", s03), (4, "Страва", s04), (5, "Продукти", s05),
           (6, "Кошик", s06), (7, "Отримання", s07), (8, "Оплата", s08), (9, "Статус замовлення", s09), (10, "Готово у віконці", s10),
           (11, "Комірка-холодильник", s11), (12, "Кур'єр", s12), (13, "Картка", s13), (14, "Профіль", s14)]


def fill(html, t):
    return html.replace("{NAME}", THEMES[t]["name"]).replace("{SLOGAN}", THEMES[t]["slogan"])


if __name__ == "__main__":
    jobs = []
    for t in THEMES:
        for n, _, fn in SCREENS:
            name = "app-%s-%02d" % (t, n)
            open(os.path.join(OUT, name + ".html"), "w").write(fill(page(t, fn()), t))
            jobs.append((name, 390, 844))
    for t in THEMES:
        open(os.path.join(OUT, "site-%s.html" % t), "w").write(fill(page(t, site(), extra=SITE_CSS), t).replace("body{background:#ddd", "body{background:var(--bg)"))
        jobs.append(("site-%s" % t, 1440, 900))
    json.dump(jobs, open(os.path.join(OUT, "jobs.json"), "w"))
    print(len(jobs))
