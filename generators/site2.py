"""Сайт: 9 сторінок для клікабельного десктоп-прототипу. Без назви магазину."""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from p2 import page, ic, img, SITE_CSS, OUT, qr, barcode

CSS2 = SITE_CSS + """
.site{min-height:900px;display:flex;flex-direction:column}
.hdr{height:88px;display:flex;align-items:center;gap:36px;padding:0 80px;border-bottom:1px solid var(--line)}
.hdr a{font-size:15px;font-weight:500;color:var(--ink);text-decoration:none}
.hdr a.on{color:var(--brand);font-weight:700}
.main{flex:1;padding:48px 80px 96px;display:flex;flex-direction:column;gap:28px}
.crumb{font-size:14px;color:var(--soft)}
.chiprow{display:flex;gap:10px}
.chip{height:40px;padding:0 18px;border-radius:20px;border:1px solid var(--line);background:var(--surface);display:inline-flex;align-items:center;font-size:14px;font-weight:600}
.chip.on{background:var(--brand);border-color:var(--brand);color:var(--onbrand)}
.box{background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:14px}
.row{display:flex;align-items:center;gap:14px}
.col{display:flex;flex-direction:column;gap:4px}
.grow{flex:1;min-width:0}
.s{font-size:14px;line-height:1.4;color:var(--soft)}
.t{font-size:16px;line-height:1.45}
.b{font-weight:700}
.price{font-size:18px;font-weight:700}
.add{height:44px;padding:0 18px;border-radius:12px;background:var(--brand);color:var(--onbrand);display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700}
.stepper{display:inline-flex;align-items:center;gap:14px;height:44px;padding:0 14px;border-radius:12px;border:1px solid var(--line);background:var(--surface);font-weight:700}
.opt{display:flex;align-items:center;gap:14px;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:16px 18px;flex:1}
.opt.on{border:2px solid var(--brand);padding:15px 17px}
.rad{width:22px;height:22px;border-radius:11px;border:2px solid var(--line);flex:none}
.rad.on{border:7px solid var(--brand)}
.slot{height:44px;border-radius:12px;border:1px solid var(--line);background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;flex:1}
.slot.on{background:var(--brand);color:var(--onbrand);border-color:var(--brand)}
.field{height:52px;border-radius:14px;border:1px solid var(--line);background:var(--surface);display:flex;align-items:center;padding:0 16px;font-size:15px;flex:1}
.div{height:1px;background:var(--line)}
.tog{width:46px;height:28px;border-radius:14px;background:var(--brand);padding:3px;display:flex;justify-content:flex-end;flex:none}
.tog i{width:22px;height:22px;border-radius:11px;background:var(--onbrand);display:block}
.ib{width:44px;height:44px;border-radius:22px;background:var(--surface);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;flex:none;position:relative}
.cnt{position:absolute;right:-4px;top:-4px;min-width:20px;height:20px;border-radius:10px;background:var(--brand);color:var(--onbrand);font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;padding:0 5px}
.side a{display:flex;align-items:center;gap:10px;height:44px;padding:0 14px;border-radius:12px;font-size:15px;font-weight:500;color:var(--ink);text-decoration:none}
.side a.on{background:var(--tint2);font-weight:700;color:var(--brand)}
.ftr{padding:40px 80px 48px;border-top:1px solid var(--line);display:flex;gap:60px}
.tl{display:flex;gap:0;align-items:flex-start}
.tl .st{flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center}
.dot{width:32px;height:32px;border-radius:16px;border:2px solid var(--line);background:var(--surface);display:flex;align-items:center;justify-content:center}
.dot.done{background:var(--brand);border-color:var(--brand)}
.dot.now{background:var(--tint);border-color:var(--brand)}
"""

S = dict(home=101, menu=102, dish=103, shop=104, cart=105, checkout=106, done=107, cards=108, account=109)
NAMES = {101: "С1 Головна", 102: "С2 Меню кухні", 103: "С3 Страва", 104: "С4 Продукти", 105: "С5 Кошик",
         106: "С6 Оформлення", 107: "С7 Замовлення прийнято", 108: "С8 Картки", 109: "С9 Кабінет"}


def go(k):
    return ' data-go="%d"' % S[k]


def header(active=None):
    links = [("menu", "Кухня"), ("shop", "Продукти"), ("cards", "Картки")]
    nav = "".join('<a class="%s"%s>%s</a>' % ("on" if k == active else "", "" if k == active else go(k), l) for k, l in links)
    home = '<a class="%s"%s>Головна</a>' % ("on" if active == "home" else "", "" if active == "home" else go("home"))
    return ('<div class="hdr">' + home + nav + '<div style="flex:1"></div>'
            '<div class="ib"%s>%s</div>' % (go("account"), ic("user", 20)) +
            '<div class="ib"%s>%s<span class="cnt">4</span></div>' % (go("cart"), ic("cart", 20)) +
            '<span class="sbtn" style="height:46px;font-size:15px;border-radius:14px"%s>Замовити онлайн</span></div>' % go("menu"))


def footer():
    return ('<div class="ftr"><div style="flex:1" class="col"><span class="b">Retail Hub «Солом\'янка»</span><span class="s">Мережа «Гермес»</span></div>'
            '<div class="col" style="width:280px"><span class="b">Адреса</span><span class="s">вул. [адреса], Солом\'янка, Київ</span></div>'
            '<div class="col" style="width:240px"><span class="b">Години</span><span class="s">Щодня 7:30–22:00</span><span class="s">Комірка видачі 24/7</span></div>'
            '<div class="col" style="width:200px"><span class="b">Контакти</span><span class="s">+380 [номер]</span></div></div>')


def wrap(body, active):
    return '<div class="site">' + header(active) + body + footer() + "</div>"


DISHES = [("d_bowl", "Боул з куркою та овочами", "380 г", "149 ₴"), ("d_borsch", "Борщ зі сметаною", "400 мл", "119 ₴"),
          ("d_soup", "Крем-суп гарбузовий", "350 мл", "99 ₴"), ("d_holubtsi", "Голубці", "2 шт, 320 г", "139 ₴"),
          ("d_deruny", "Деруни зі сметаною", "280 г", "109 ₴"), ("d_syrnyky", "Сирники зі сметаною", "3 шт, 240 г", "99 ₴")]


def dcard(k, n, w, p, width=302, ph=196):
    return ('<div class="dcard" style="width:%dpx"%s>%s<div style="padding:18px 20px 20px;display:flex;flex-direction:column;gap:10px"><h3 class="h-m" style="font-size:18px">%s</h3>'
            '<div class="row"><div class="col grow"><span class="s">%s</span><span class="price">%s</span></div><span class="add">%sДодати</span></div></div></div>') % (
        width, go("dish"), img(k, width, ph, 0), n, w, p, ic("plus", 16))


# ---- pages
def p_home():
    zones = [("z_coffee", "Кава з собою", "Окреме віконце, без входу в магазин", None), ("z_fresh", "Свіжі продукти", "Овочі, фрукти й молочне від фермерів поруч", "shop"),
             ("z_kitchen", "Готова їжа", "Сніданки, обіди й вечері з нашої кухні", "menu"), ("z_locker", "Комірка 24/7", "Замовте онлайн і заберіть, коли зручно", "checkout"),
             ("z_space", "Простір для людей", "Кава, розетки, вода для собак", None)]
    hero = ('<div style="padding:56px 80px 0;display:flex;gap:64px;align-items:flex-end"><div style="flex:1;display:flex;flex-direction:column;gap:22px">'
            '<h1 class="h-xl" style="max-width:720px">Кухня, продукти й кава біля дому</h1>'
            '<p class="lead" style="max-width:600px">Магазин на Солом\'янці, де можна взяти каву з віконця, пообідати з нашої кухні й забрати онлайн-замовлення з комірки навіть уночі.</p>'
            '<div style="display:flex;gap:12px;margin-top:6px"><span class="sbtn"%s>Подивитися меню кухні</span><span class="sbtn ghost"%s>Каталог продуктів</span></div></div>'
            '<div style="width:420px;display:flex;gap:28px;padding-bottom:6px"><div class="fact"><b>7:30</b><span class="s">кава з віконця</span></div><div class="fact"><b>24/7</b><span class="s">комірка видачі</span></div><div class="fact"><b>30 хв</b><span class="s">доставка районом</span></div></div></div>'
            '<div style="padding:44px 80px 0">' + img("s_hero", 1280, 506, 28) + '</div>') % (go("menu"), go("shop"))
    zs = ('<div class="sec"><h2 class="h-l">Що є в магазині</h2><div style="display:flex;gap:20px;margin-top:32px">' + "".join(
        '<div class="zcard"%s>%s<h3 class="h-m" style="font-size:19px">%s</h3><p class="p" style="font-size:15px">%s</p></div>' % (go(g) if g else "", img(k, 240, 160, 20), t, d) for k, t, d, g in zones) + "</div></div>")
    ks = ('<div class="sec"><div class="row" style="align-items:flex-end"><h2 class="h-l grow">Кухня сьогодні</h2><span class="sbtn ghost"%s>Усе меню</span></div>'
          '<div style="display:flex;gap:24px;margin-top:32px">' % go("menu") + "".join(dcard(*d) for d in DISHES[:4]) + "</div></div>")
    ways = [("window", "Віконце видачі", "Показуєте код із застосунку й забираєте пакет. Без черги на касі."),
            ("locker", "Комірка-холодильник 24/7", "Як поштомат, тільки з холодом. Код відкриває комірку в будь-яку годину."),
            ("truck", "Кур'єр по району", "Привеземо за 30–45 хвилин по Солом\'янці.")]
    ws = ('<div class="sec"><div style="background:var(--tint);border-radius:36px;padding:56px 64px"><h2 class="h-l">Як забрати замовлення</h2><div style="display:flex;gap:20px;margin-top:32px">' + "".join(
        '<div class="way"><div class="ib" style="width:52px;height:52px;border-radius:16px;background:var(--brand);border:none">%s</div><h3 class="h-m">%s</h3><p class="p">%s</p></div>' % (ic(i, 26, "var(--onbrand)"), t, d) for i, t, d in ways) + "</div></div></div>")
    cs = ('<div class="sec" style="padding-bottom:96px"><div style="background:var(--deep);color:var(--onbrand);border-radius:36px;padding:56px 64px;display:flex;align-items:center;gap:40px">'
          '<div class="col grow" style="gap:10px"><h2 class="h-l">Картка для своїх</h2><p class="lead" style="color:var(--onbrand);opacity:.8">Сімейна, студентська або індивідуальна. Бонуси з кожної покупки й обіду з кухні.</p></div>'
          '<span class="sbtn" style="background:var(--onbrand);color:var(--deep)"%s>Обрати картку</span></div></div>') % go("cards")
    return wrap(hero + zs + ks + ws + cs, "home")


def p_menu():
    chips = '<div class="chiprow">' + "".join('<span class="chip%s">%s</span>' % (" on" if i == 1 else "", c) for i, c in enumerate(["Сніданки", "Обід і вечеря", "Супи", "Комбо", "Напої"])) + "</div>"
    grid = '<div style="display:grid;grid-template-columns:repeat(3,293px);gap:24px">' + "".join(dcard(k, n, w, p, 293, 190) for k, n, w, p in DISHES) + "</div>"
    side = ('<div class="box" style="width:320px;flex:none;position:sticky;top:0"><h3 class="h-m">Кошик</h3>'
            '<div class="row"><span class="s grow">Боул з куркою × 2</span><span class="b">298 ₴</span></div>'
            '<div class="row"><span class="s grow">Борщ зі сметаною</span><span class="b">119 ₴</span></div>'
            '<div class="row"><span class="s grow">Томати на гілці, 1 кг</span><span class="b">89 ₴</span></div><div class="div"></div>'
            '<div class="row"><span class="t b grow">Разом</span><span class="price">506 ₴</span></div>'
            '<span class="sbtn" style="justify-content:center"%s>Перейти до кошика</span><span class="s">Замовте до 17:00 і заберіть сьогодні ввечері</span></div>') % go("cart")
    body = ('<div class="main"><div class="col" style="gap:8px"><h1 class="h-l">Меню кухні на сьогодні</h1><p class="p">Одне меню на день, готуємо тут же, на кухні магазину. Асортимент ще узгоджуємо.</p></div>'
            + chips + '<div style="display:flex;gap:40px;align-items:flex-start">' + grid + side + "</div></div>")
    return wrap(body, "menu")


def p_dish():
    nut = '<div style="display:flex;gap:10px">' + "".join(
        '<div class="col" style="flex:1;align-items:center;padding:14px 6px;border-radius:16px;background:var(--tint2);gap:2px"><span class="b" style="font-size:18px">%s</span><span class="s">%s</span></div>' % (a, b)
        for a, b in [("420", "ккал"), ("32 г", "білки"), ("14 г", "жири"), ("40 г", "вуглеводи")]) + "</div>"
    right = ('<div class="col grow" style="gap:16px"><span class="badge" style="display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:15px;background:var(--accent);font-size:13px;font-weight:700;align-self:flex-start">%sОвочі від локальних фермерів</span>'
             '<h1 class="h-l">Боул з куркою та овочами</h1><span class="s" style="font-size:16px">380 г · готуємо 15 хв</span>'
             '<p class="t" style="max-width:520px">Курка, нут, авокадо, томати й зелень. Готуємо на кухні магазину щодня, з ранку до вечора.</p>' + nut +
             '<div class="row" style="margin-top:8px"><span class="stepper">%s<span>1</span>%s</span><span class="sbtn grow" style="justify-content:center"%s>Додати в кошик · 149 ₴</span></div></div>') % (
        ic("leaf", 14), ic("minus", 16), ic("plus", 16), go("cart"))
    more = '<div style="display:flex;gap:24px">' + "".join(dcard(k, n, w, p, 392, 220) for k, n, w, p in DISHES[1:4]) + "</div>"
    body = ('<div class="main"><span class="crumb"%s>Меню кухні  /  Боул з куркою та овочами</span>' % go("menu") +
            '<div style="display:flex;gap:48px;align-items:flex-start">' + img("d_bowl", 640, 420, 28) + right + "</div>"
            '<h2 class="h-l" style="font-size:32px;margin-top:24px">Ще з меню сьогодні</h2>' + more + "</div>")
    return wrap(body, "menu")


GROC = [("g_tomato", "Томати на гілці", "1 кг", "89 ₴"), ("g_gala", "Яблука Гала", "1 кг", "54 ₴"), ("g_potato", "Картопля", "1 кг", "22 ₴"), ("g_carrots", "Морква", "1 кг", "19 ₴")]


def p_shop():
    cats = ["Овочі й фрукти", "Молочне", "Хліб і випічка", "Бакалія", "Напої", "Для тварин"]
    side = '<div class="side col" style="width:240px;flex:none;gap:4px">' + "".join('<a class="%s">%s</a>' % ("on" if i == 0 else "", c) for i, c in enumerate(cats)) + "</div>"
    grid = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px">' + "".join(
        '<div class="box" style="padding:14px;gap:10px">%s<span class="t b">%s</span><div class="row"><span class="s grow">%s</span><span class="price">%s</span></div><span class="add" style="justify-content:center"%s>%sУ кошик</span></div>' % (
            img(k, 207, 150, 14, "object-fit:contain;background:#FFFFFF"), n, w, p, go("cart"), ic("plus", 16)) for k, n, w, p in GROC) + "</div>"
    main = ('<div class="col grow" style="gap:20px"><div class="field" style="flex:none;gap:10px">%s<span class="s" style="font-size:15px">Знайти продукт</span></div>' % ic("search", 18, "var(--soft)") +
            '<div style="background:var(--tint);border-radius:24px;padding:22px 26px;display:flex;align-items:center;gap:16px">%s<div class="col grow"><h3 class="h-m">Від фермерів поруч</h3><span class="s">Овочі, молоко й сир щодня з Київщини</span></div></div>' % ic("leaf", 26, "var(--brand)") +
            '<h2 class="h-m" style="font-size:24px">Овочі й фрукти</h2>' + grid + '<span class="s">Ціни й асортимент умовні, реальні підтягнемо з BAS</span></div>')
    body = '<div class="main"><h1 class="h-l">Продукти</h1><div style="display:flex;gap:40px;align-items:flex-start">' + side + main + "</div></div>"
    return wrap(body, "shop")


def p_cart():
    items = [("d_bowl", "Боул з куркою та овочами", "380 г", 2, "298 ₴"), ("d_borsch", "Борщ зі сметаною", "400 мл", 1, "119 ₴"), ("g_tomato", "Томати на гілці", "1 кг", 1, "89 ₴")]
    rows = '<div class="box" style="padding:8px 24px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:16px 0">%s<div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div><span class="stepper">%s<span>%d</span>%s</span><span class="price" style="width:90px;text-align:right">%s</span></div>' % (
            img(k, 72, 72, 14, "object-fit:%s;background:%s" % (("contain", "#FFFFFF") if k.startswith("g_") else ("cover", "var(--photo)"))), n, w, ic("minus", 16), q, ic("plus", 16), p)
        for k, n, w, q, p in items) + "</div>"
    summ = ('<div class="box" style="width:380px;flex:none"><h3 class="h-m">Разом</h3><div class="row"><span class="s grow">3 позиції</span><span class="b">506 ₴</span></div>'
            '<div class="row"><span class="s grow">Бонусів нарахуємо</span><span class="b" style="color:var(--brand)">+25</span></div><div class="div"></div>'
            '<div class="row"><span class="t b grow">До сплати</span><span class="price" style="font-size:24px">506 ₴</span></div>'
            '<span class="sbtn" style="justify-content:center"%s>Оформити замовлення</span><span class="s" style="text-align:center"%s>Продовжити покупки</span></div>') % (go("checkout"), go("menu"))
    body = '<div class="main"><h1 class="h-l">Кошик</h1><div style="display:flex;gap:40px;align-items:flex-start"><div class="grow">' + rows + "</div>" + summ + "</div></div>"
    return wrap(body, None)


def p_checkout():
    ways = [("window", "Віконце видачі", "Без черги, безкоштовно", True), ("locker", "Комірка 24/7", "Заберіть самі за кодом", False), ("truck", "Кур'єр", "30–45 хв, від 49 ₴", False)]
    w = '<div class="row" style="gap:12px">' + "".join('<div class="opt%s"><div class="rad%s"></div><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div>%s</div>' % (
        " on" if on else "", " on" if on else "", t, s, ic(i, 22, "var(--brand)")) for i, t, s, on in ways) + "</div>"
    slots = '<div class="row" style="gap:10px">' + "".join('<span class="slot%s">%s</span>' % (" on" if t == "18:30" else "", t) for t in ["17:30", "18:00", "18:30", "19:00", "19:30", "20:00"]) + "</div>"
    pay = '<div class="row" style="gap:12px">' + "".join('<div class="opt%s"><div class="rad%s"></div><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div></div>' % (
        " on" if on else "", " on" if on else "", t, s) for t, s, on in [("Карткою зараз", "Apple Pay, Google Pay, картка", True), ("При отриманні", "Карткою або готівкою", False)]) + "</div>"
    left = ('<div class="col grow" style="gap:20px">'
            '<div class="box"><h3 class="h-m">Як отримати</h3>' + w + '</div>'
            '<div class="box"><h3 class="h-m">Коли</h3><div class="chiprow"><span class="chip on">Сьогодні</span><span class="chip">Завтра</span></div>' + slots + '</div>'
            '<div class="box"><h3 class="h-m">Оплата</h3>' + pay + '<div class="row" style="background:var(--tint2);border-radius:16px;padding:14px 18px"><div class="col grow"><span class="t b">Списати бонуси</span><span class="s">На сімейній картці 1 240</span></div><div class="tog"><i></i></div></div></div>'
            '<div class="box"><h3 class="h-m">Контакти</h3><div class="row" style="gap:12px"><span class="field">Олена Коваленко</span><span class="field">+380 [номер]</span></div></div></div>')
    summ = ('<div class="box" style="width:380px;flex:none"><h3 class="h-m">Ваше замовлення</h3><div class="row"><span class="s grow">Боул з куркою × 2</span><span class="b">298 ₴</span></div>'
            '<div class="row"><span class="s grow">Борщ зі сметаною</span><span class="b">119 ₴</span></div><div class="row"><span class="s grow">Томати на гілці</span><span class="b">89 ₴</span></div><div class="div"></div>'
            '<div class="row"><span class="s grow">Отримання</span><span class="b">Віконце, 18:30</span></div>'
            '<div class="row"><span class="t b grow">До сплати</span><span class="price" style="font-size:24px">506 ₴</span></div>'
            '<span class="sbtn" style="justify-content:center"%s>Оплатити 506 ₴</span></div>') % go("done")
    body = '<div class="main"><span class="crumb"%s>Кошик  /  Оформлення</span><h1 class="h-l">Оформлення</h1><div style="display:flex;gap:40px;align-items:flex-start">' % go("cart") + left + summ + "</div></div>"
    return wrap(body, None)


def p_done():
    steps = [("Прийнято", "18:02", "done"), ("Готуємо на кухні", "зараз", "now"), ("Готово до видачі", "о 18:30", ""), ("Видано", "", "")]
    tl = '<div class="tl" style="width:100%">' + "".join('<div class="st"><div class="dot %s">%s</div><span class="t b"%s>%s</span><span class="s">%s</span></div>' % (
        c, ic("check", 16, "var(--onbrand)") if c == "done" else "", "" if c else ' style="color:var(--soft)"', t, s) for t, s, c in steps) + "</div>"
    card = ('<div class="box" style="width:760px;align-self:center;align-items:center;padding:40px;gap:18px;text-align:center">'
            '<div class="ib" style="width:64px;height:64px;border-radius:32px;background:var(--brand);border:none">%s</div>'
            '<h1 class="h-l">Замовлення А-274 прийнято</h1><p class="p">Віконце видачі, сьогодні о 18:30. Покажіть цей код у віконці.</p>%s'
            '<span style="font-size:30px;font-weight:800;letter-spacing:4px">А-274</span>%s'
            '<div class="row" style="gap:12px;margin-top:8px"><span class="sbtn"%s>Мої замовлення</span><span class="sbtn ghost"%s>На головну</span></div></div>') % (
        ic("check", 30, "var(--onbrand)", 3), qr(274, 160), tl, go("account"), go("home"))
    return wrap('<div class="main">' + card + "</div>", None)


def p_cards():
    cards = [("Сімейна", "Один рахунок на всю родину", ["Бонуси всіх членів сім\'ї на одному балансі", "Додавайте до 5 людей", "Спільна історія замовлень"], True),
             ("Студентська", "За студентським квитком", ["Знижка на комбо з кухні", "Кава зі знижкою до 11:00", "Подвійні бонуси в сесію"], False),
             ("Індивідуальна", "Для себе", ["Бонуси з кожної покупки", "Персональні пропозиції", "Оплата бонусами до 50%"], False)]
    cs = '<div style="display:flex;gap:20px">' + "".join(
        '<div class="lc%s"><h3 class="h-m" style="font-size:26px">%s</h3><p class="p">%s</p><div style="display:flex;flex-direction:column;gap:10px;margin-top:6px">%s</div>'
        '<span class="sbtn" style="justify-content:center;margin-top:10px;%s"%s>Оформити картку</span></div>' % (
            " dk" if dk else "", t, sub, "".join('<div class="li">%s<span>%s</span></div>' % (ic("check", 18, "var(--accent)" if dk else "var(--brand)"), x) for x in li),
            "background:var(--onbrand);color:var(--deep)" if dk else "", go("account")) for t, sub, li, dk in cards) + "</div>"
    steps = [("Оформіть сімейну картку", "У застосунку або на касі, потрібен лише номер телефону."), ("Додайте рідних", "Надішліть запрошення, і їхні покупки підуть на спільний баланс."), ("Витрачайте бонуси разом", "Оплачуйте ними до половини чека будь-кому з родини.")]
    how = ('<div class="box" style="padding:40px;gap:24px"><h2 class="h-l" style="font-size:32px">Як працює сімейна картка</h2><div style="display:flex;gap:28px">' + "".join(
        '<div class="col grow" style="gap:10px"><div class="ib" style="background:var(--tint2);border:none;font-weight:800;font-size:17px">%d</div><span class="t b">%s</span><span class="s">%s</span></div>' % (i + 1, t, d) for i, (t, d) in enumerate(steps)) + "</div></div>")
    body = ('<div class="main"><div class="col" style="gap:8px"><h1 class="h-l">Картка для своїх</h1><p class="p">Три типи карток. Умови бонусів умовні, їх затвердить замовник.</p></div>' + cs + how + "</div>")
    return wrap(body, "cards")


def p_account():
    side = ('<div class="side col" style="width:240px;flex:none;gap:4px"><div class="row" style="padding:0 6px 16px"><div class="ib" style="width:52px;height:52px;border-radius:26px;background:var(--tint);border:none;font-weight:800;font-size:19px">О</div>'
            '<div class="col"><span class="t b">Олена Коваленко</span><span class="s">Сімейна картка</span></div></div>' +
            "".join('<a class="%s">%s</a>' % ("on" if i == 0 else "", c) for i, c in enumerate(["Замовлення", "Картка й бонуси", "Адреси доставки", "Сповіщення", "Налаштування"])) + "</div>")
    card = ('<div style="background:var(--deep);color:var(--onbrand);border-radius:24px;padding:26px;width:420px;flex:none;display:flex;flex-direction:column;gap:14px">'
            '<div class="row"><span class="t b grow">Сімейна картка</span><span class="s" style="color:var(--onbrand);opacity:.8">Родина Коваленків</span></div>'
            '<div style="background:#FFFFFF;border-radius:14px;padding:14px;display:flex;justify-content:center">%s</div>'
            '<div class="row"><div class="col grow"><span class="s" style="color:var(--onbrand);opacity:.8">Спільний баланс</span><span style="font-size:30px;font-weight:800">1 240 бонусів</span></div></div></div>') % barcode(282, 54)
    orders = [("А-274", "Сьогодні, 18:30 · віконце", "Готуємо", "506 ₴", True), ("А-251", "18 жовтня · комірка 24/7", "Видано", "342 ₴", False), ("А-233", "15 жовтня · кур\'єр", "Видано", "611 ₴", False)]
    ol = '<div class="box" style="padding:8px 24px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:18px 0"%s><div class="col grow"><span class="t b">Замовлення %s</span><span class="s">%s</span></div><span class="chip%s" style="height:32px;font-size:13px">%s</span><span class="price" style="width:90px;text-align:right">%s</span></div>' % (
            go("done") if act else "", n, d, " on" if act else "", s, p) for n, d, s, p, act in orders) + "</div>"
    main = '<div class="col grow" style="gap:24px"><div style="display:flex;gap:24px;align-items:stretch">' + card + \
           '<div class="box grow" style="justify-content:center"><span class="s">Учасники картки</span><div class="row" style="gap:10px">' + "".join(
               '<div class="ib" style="background:%s;border:none;font-weight:700">%s</div>' % (bg, l) for l, bg in [("О", "var(--accent)"), ("А", "var(--tint)"), ("М", "var(--tint2)"), ("Б", "var(--tint)")]) + \
           '<div class="ib">%s</div></div><span class="s">4 учасники, можна додати ще одного</span></div></div><h2 class="h-m" style="font-size:24px">Замовлення</h2>' % ic("plus", 18) + ol + "</div>"
    body = '<div class="main"><h1 class="h-l">Кабінет</h1><div style="display:flex;gap:40px;align-items:flex-start">' + side + main + "</div></div>"
    return wrap(body, None)


PAGES = [(101, p_home), (102, p_menu), (103, p_dish), (104, p_shop), (105, p_cart), (106, p_checkout), (107, p_done), (108, p_cards), (109, p_account)]

if __name__ == "__main__":
    for n, fn in PAGES:
        html = page("pulse", fn(), extra=CSS2).replace("body{background:#ddd", "body{background:var(--bg)")
        open(os.path.join(OUT, "web-%d.html" % n), "w").write(html)
    print("ok")
