"""Сайт v3: 34 сторінки + панель персоналу + мобільна версія. Без назви й лого магазину."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import site2
from p2 import page, ic, img, OUT, qr, barcode
from site2 import CSS2, DISHES, GROC

CSS = CSS2 + """
.allg{display:flex;gap:8px;flex-wrap:wrap}.allg span{height:32px;padding:0 12px;border-radius:16px;border:1px solid var(--line);background:var(--surface);font-size:13px;font-weight:600;display:flex;align-items:center}
.tog.off{background:var(--line);justify-content:flex-start}
.ftr a{font-size:14px;color:var(--soft);text-decoration:underline}
.err{color:#B3261E;font-weight:600;font-size:14px}
.banner{display:flex;align-items:center;gap:12px;padding:16px 20px;border-radius:18px;background:var(--tint2);font-weight:600}
.banner.bad{background:#F6DCD8;color:#7A1C16}
.code{width:72px;height:80px;border-radius:16px;border:1px solid var(--line);background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:700}
.code.on{border:2px solid var(--brand)}.code.bad{border:2px solid #B3261E;color:#B3261E}
/* адмінка */
.adm{width:1440px;height:900px;display:flex;background:var(--bg);color:var(--ink)}
.aside{width:248px;flex:none;background:var(--deep);color:var(--onbrand);padding:28px 16px;display:flex;flex-direction:column;gap:4px}
.aside a{display:flex;align-items:center;gap:12px;height:46px;padding:0 14px;border-radius:12px;font-size:15px;font-weight:500;color:var(--onbrand);opacity:.82;text-decoration:none}
.aside a.on{background:rgba(255,255,255,.12);opacity:1;font-weight:700}
.amain{flex:1;padding:32px 40px;display:flex;flex-direction:column;gap:22px;min-width:0}
.kcol{flex:1;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
.ocard{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;gap:6px}
.tag{height:26px;padding:0 10px;border-radius:13px;font-size:12px;font-weight:700;display:inline-flex;align-items:center;background:var(--tint2);color:var(--ink)}
.tag.w{background:var(--tint)}.tag.l{background:var(--tint2)}.tag.c{background:var(--accent)}
.cell{height:96px;border-radius:14px;border:1px solid var(--line);background:var(--surface);display:flex;flex-direction:column;justify-content:space-between;padding:10px 12px}
.cell.busy{background:var(--tint2);border-color:var(--tint2)}.cell.late{background:#F6DCD8;border-color:#F6DCD8}
/* мобільний сайт */
.msite{width:390px;background:var(--bg);color:var(--ink);display:flex;flex-direction:column}
.mh{height:64px;display:flex;align-items:center;gap:12px;padding:0 20px;border-bottom:1px solid var(--line)}
.mm{padding:24px 20px 40px;display:flex;flex-direction:column;gap:18px}
.mf{padding:24px 20px 32px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:8px}
"""

S = dict(home=101, menu=102, dish=103, shop=104, cart=105, checkout=106, done=107, cards=108, account=109, login=110, code=111, form=112, cdone=113,
         legal=114, settings=115, bonus=116, addm=117, invite=118, student=119, check=120, coffee=121, cofdone=122, clogin=123, ccode=124,
         courier=125, locker=126, cod=127, dcour=128, dlock=129, indiv=130, empty=131, payfail=132, badcode=133, idone=134)
NAMES = {101: "Головна", 102: "Меню кухні", 103: "Страва", 104: "Продукти", 105: "Кошик", 106: "Оформлення · віконце", 107: "Замовлення прийнято",
         108: "Картки", 109: "Кабінет", 110: "Вхід", 111: "Код з SMS", 112: "Оформлення · сімейна", 113: "Сімейну картку оформлено", 114: "Умови й документи",
         115: "Налаштування", 116: "Картка й бонуси", 117: "Додати учасника", 118: "Запрошення в родину", 119: "Оформлення · студентська", 120: "Перевіряємо квиток",
         121: "Кава з собою", 122: "Кава замовлена", 123: "Вхід перед оформленням", 124: "Код перед оформленням", 125: "Оформлення · кур'єр",
         126: "Оформлення · комірка", 127: "Оформлення · при отриманні", 128: "Замовлення · кур'єр", 129: "Замовлення · комірка", 130: "Оформлення · індивідуальна",
         131: "Кошик порожній", 132: "Оплата не пройшла", 133: "Неправильний код", 134: "Індивідуальну картку оформлено",
         140: "Замовлення", 141: "Збирання замовлення", 142: "Кухня", 143: "Комірки 24/7", 144: "Картки на перевірці", 145: "Меню на сьогодні",
         146: "Картку підтверджено", 147: "Меню опубліковано",
         150: "Головна", 151: "Навігація", 152: "Меню кухні", 153: "Кошик і оформлення", 154: "Картки", 155: "Замовлення прийнято", 156: "Оформлення картки", 157: "Картку оформлено"}


def fname(n):
    if n < 140: return "С%d %s" % (n - 100, NAMES[n])
    if n < 150: return "П%d %s" % (n - 139, NAMES[n])
    return "М%d %s" % (n - 149, NAMES[n])


def go(k):
    return ' data-go="%d"' % (S[k] if isinstance(k, str) else k)


def header(active=None):
    links = [("home", "Головна"), ("menu", "Кухня"), ("coffee", "Кава"), ("shop", "Продукти"), ("cards", "Картки")]
    nav = "".join('<a class="%s"%s>%s</a>' % ("on" if k == active else "", "" if k == active else go(k), l) for k, l in links)
    return ('<div class="hdr">' + nav + '<div style="flex:1"></div>'
            '<div class="ib"%s>%s</div>' % (go("account"), ic("user", 20)) +
            '<div class="ib"%s>%s<span class="cnt">3</span></div>' % (go("cart"), ic("cart", 20)) +
            '<span class="sbtn" style="height:46px;font-size:15px;border-radius:14px"%s>Замовити онлайн</span></div>' % go("menu"))


def footer():
    return ('<div class="ftr"><div style="flex:1" class="col"><span class="b">Retail Hub «Солом\'янка»</span><span class="s">Мережа «Гермес»</span></div>'
            '<div class="col" style="width:260px"><span class="b">Адреса</span><span class="s">вул. [адреса], Солом\'янка, Київ</span></div>'
            '<div class="col" style="width:220px"><span class="b">Години</span><span class="s">Щодня 7:30–22:00</span><span class="s">Комірка видачі 24/7</span></div>'
            '<div class="col" style="width:220px"><span class="b">Покупцям</span><a%s>Умови й документи</a><a%s>Конфіденційність</a></div></div>') % (go("legal"), go("legal"))


def wrap(body, active=None):
    return '<div class="site">' + header(active) + body + footer() + "</div>"


def dcard(k, n, w, p, width=302, ph=196):
    return ('<div class="dcard" style="width:%dpx"%s>%s<div style="padding:18px 20px 20px;display:flex;flex-direction:column;gap:10px"><h3 class="h-m" style="font-size:18px">%s</h3>'
            '<div class="row"><div class="col grow"><span class="s">%s</span><span class="price">%s</span></div><span class="add"%s>%sДодати</span></div></div></div>') % (
        width, go("dish"), img(k, width, ph, 0), n, w, p, go("cart"), ic("plus", 16))


def box(title, inner, style=""):
    return '<div class="box" style="%s"><h3 class="h-m">%s</h3>%s</div>' % (style, title, inner)


def field(l, v, strong=False):
    return '<div class="col grow" style="gap:6px"><span class="s b">%s</span><span class="field" style="flex:none%s">%s</span></div>' % (l, ";border:2px solid var(--brand)" if strong else "", v)


def opt(t, s, on, g=None, icn=None):
    return '<div class="opt%s"%s><div class="rad%s"></div><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div>%s</div>' % (
        " on" if on else "", go(g) if g and not on else "", " on" if on else "", t, s, ic(icn, 22, "var(--brand)") if icn else "")


def centered(inner, width=560):
    return '<div class="main" style="align-items:center"><div class="box" style="width:%dpx;padding:40px;gap:18px">%s</div></div>' % (width, inner)


def okicon(bad=False):
    return '<div class="ib" style="width:64px;height:64px;border-radius:32px;background:%s;border:none">%s</div>' % (
        "#F6DCD8" if bad else "var(--brand)", ic("alert", 30, "#B3261E") if bad else ic("check", 30, "var(--onbrand)", 3))


# ---------- сторінки покупця ----------
def p_home():
    zones = [("z_coffee", "Кава з собою", "Окреме віконце, без входу в магазин", "coffee"), ("z_fresh", "Свіжі продукти", "Овочі, фрукти й молочне від фермерів поруч", "shop"),
             ("z_kitchen", "Готова їжа", "Сніданки, обіди й вечері з нашої кухні", "menu"), ("z_locker", "Комірка 24/7", "Замовте онлайн і заберіть, коли зручно", "locker"),
             ("z_space", "Простір для людей", "Кава, розетки, вода для собак", "legal")]
    hero = ('<div style="padding:56px 80px 0;display:flex;gap:64px;align-items:flex-end"><div style="flex:1;display:flex;flex-direction:column;gap:22px">'
            '<h1 class="h-xl" style="max-width:720px">Кухня, продукти й кава біля дому</h1>'
            '<p class="lead" style="max-width:600px">Магазин на Солом\'янці, де можна взяти каву з віконця, пообідати з нашої кухні й забрати онлайн-замовлення з комірки навіть уночі.</p>'
            '<div style="display:flex;gap:12px;margin-top:6px"><span class="sbtn"%s>Подивитися меню кухні</span><span class="sbtn ghost"%s>Каталог продуктів</span></div></div>'
            '<div style="width:420px;display:flex;gap:28px;padding-bottom:6px"><div class="fact"><b>7:30</b><span class="s">кава з віконця</span></div><div class="fact"><b>24/7</b><span class="s">комірка видачі</span></div><div class="fact"><b>30 хв</b><span class="s">доставка районом</span></div></div></div>'
            '<div style="padding:44px 80px 0">' + img("s_hero", 1280, 506, 28) + '</div>') % (go("menu"), go("shop"))
    zones[4] = ("z_space", "Простір для людей", "Кава, розетки, вода для собак", None)
    zs = ('<div class="sec"><h2 class="h-l">Що є в магазині</h2><div style="display:flex;gap:20px;margin-top:32px">' + "".join(
        '<div class="zcard"%s>%s<h3 class="h-m" style="font-size:19px">%s</h3><p class="p" style="font-size:15px">%s</p></div>' % (go(g) if g else "", img(k, 240, 160, 20), t, d) for k, t, d, g in zones) + "</div></div>")
    ks = ('<div class="sec"><div class="row" style="align-items:flex-end"><h2 class="h-l grow">Кухня сьогодні</h2><span class="sbtn ghost"%s>Усе меню</span></div>'
          '<div style="display:flex;gap:24px;margin-top:32px">' % go("menu") + "".join(dcard(*d) for d in DISHES[:4]) + "</div></div>")
    ways = [("window", "Віконце видачі", "Показуєте код із застосунку й забираєте пакет. Без черги на касі.", "checkout"),
            ("locker", "Комірка-холодильник 24/7", "Як поштомат, тільки з холодом. Код відкриває комірку в будь-яку годину.", "locker"),
            ("truck", "Кур'єр по району", "Привеземо за 30–45 хвилин по Солом\'янці. Доставка 49 ₴.", "courier")]
    ws = ('<div class="sec"><div style="background:var(--tint);border-radius:36px;padding:56px 64px"><h2 class="h-l">Як забрати замовлення</h2><div style="display:flex;gap:20px;margin-top:32px">' + "".join(
        '<div class="way"%s><div class="ib" style="width:52px;height:52px;border-radius:16px;background:var(--brand);border:none">%s</div><h3 class="h-m">%s</h3><p class="p">%s</p></div>' % (go(g), ic(i, 26, "var(--onbrand)"), t, d) for i, t, d, g in ways) + "</div></div></div>")
    cs = ('<div class="sec" style="padding-bottom:96px"><div style="background:var(--deep);color:var(--onbrand);border-radius:36px;padding:56px 64px;display:flex;align-items:center;gap:40px">'
          '<div class="col grow" style="gap:10px"><h2 class="h-l">Картка для своїх</h2><p class="lead" style="color:var(--onbrand);opacity:.8">Сімейна, студентська або індивідуальна. Бонуси з кожної покупки й обіду з кухні.</p></div>'
          '<span class="sbtn" style="background:var(--onbrand);color:var(--deep)"%s>Обрати картку</span></div></div>') % go("cards")
    return wrap(hero + zs + ks + ws + cs, "home")


CARTSIDE = ('<div class="box" style="width:320px;flex:none"><h3 class="h-m">Кошик</h3>'
            '<div class="row"><span class="s grow">Боул з куркою × 2</span><span class="b">298 ₴</span></div>'
            '<div class="row"><span class="s grow">Борщ зі сметаною</span><span class="b">119 ₴</span></div>'
            '<div class="row"><span class="s grow">Томати на гілці, 1 кг</span><span class="b">89 ₴</span></div><div class="div"></div>'
            '<div class="row"><span class="t b grow">Разом</span><span class="price">506 ₴</span></div>'
            '<span class="sbtn" style="justify-content:center"%s>Перейти до кошика</span><span class="s">Замовте до 17:00 і заберіть сьогодні ввечері</span></div>') % go("cart")


def p_menu():
    chips = '<div class="chiprow">' + "".join('<span class="chip%s">%s</span>' % (" on" if i == 1 else "", c) for i, c in enumerate(["Сніданки", "Обід і вечеря", "Супи", "Комбо", "Без глютену"])) + "</div>"
    grid = '<div style="display:grid;grid-template-columns:repeat(3,293px);gap:24px">' + "".join(dcard(k, n, w, p, 293, 190) for k, n, w, p in DISHES) + "</div>"
    body = ('<div class="main"><div class="col" style="gap:8px"><h1 class="h-l">Меню кухні на сьогодні</h1><p class="p">Одне меню на день, готуємо тут же, на кухні магазину. Склад і алергени є на сторінці страви.</p></div>'
            + chips + '<div style="display:flex;gap:40px;align-items:flex-start">' + grid + CARTSIDE + "</div></div>")
    return wrap(body, "menu")


def p_dish():
    nut = '<div style="display:flex;gap:10px">' + "".join(
        '<div class="col" style="flex:1;align-items:center;padding:14px 6px;border-radius:16px;background:var(--tint2);gap:2px"><span class="b" style="font-size:18px">%s</span><span class="s">%s</span></div>' % (a, b)
        for a, b in [("420", "ккал"), ("32 г", "білки"), ("14 г", "жири"), ("40 г", "вуглеводи")]) + "</div>"
    allg = '<div class="col" style="gap:8px"><span class="s b">Алергени</span><div class="allg"><span>Кунжут</span><span>Гірчиця</span><span>Може містити сліди горіхів</span></div></div>'
    right = ('<div class="col grow" style="gap:16px"><span class="badge" style="display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:15px;background:var(--accent);font-size:13px;font-weight:700;align-self:flex-start">%sОвочі від локальних фермерів</span>'
             '<h1 class="h-l">Боул з куркою та овочами</h1><span class="s" style="font-size:16px">380 г · готуємо 15 хв</span>'
             '<p class="t" style="max-width:520px">Курка, нут, авокадо, томати, зелень, кунжутна заправка з гірчицею.</p>' + nut + allg +
             '<div class="row" style="margin-top:8px"><span class="stepper">%s<span>1</span>%s</span><span class="sbtn grow" style="justify-content:center"%s>Додати в кошик · 149 ₴</span></div></div>') % (
        ic("leaf", 14), ic("minus", 16), ic("plus", 16), go("cart"))
    more = '<div style="display:flex;gap:24px">' + "".join(dcard(k, n, w, p, 392, 220) for k, n, w, p in DISHES[1:4]) + "</div>"
    body = ('<div class="main"><span class="crumb"%s>Меню кухні  /  Боул з куркою та овочами</span>' % go("menu") +
            '<div style="display:flex;gap:48px;align-items:flex-start">' + img("d_bowl", 640, 460, 28) + right + "</div>"
            '<h2 class="h-l" style="font-size:32px;margin-top:24px">Ще з меню сьогодні</h2>' + more + "</div>")
    return wrap(body, "menu")


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
            '<span class="sbtn" style="justify-content:center"%s>Оформити замовлення</span><span class="s" style="text-align:center"%s>Продовжити покупки</span></div>') % (go("clogin"), go("menu"))
    body = ('<div class="main"><div class="row"><h1 class="h-l grow">Кошик</h1><span class="s"%s>Очистити кошик</span></div><div style="display:flex;gap:40px;align-items:flex-start"><div class="grow">' % go("empty")
            + rows + "</div>" + summ + "</div></div>")
    return wrap(body)


SLOTS = ["17:30", "18:00", "18:30", "19:00", "19:30", "20:00"]


def checkout(way, pay_now=True):
    """way: 0 віконце, 1 комірка, 2 кур'єр"""
    ws = [("window", "Віконце видачі", "Без черги, безкоштовно", "checkout"), ("locker", "Комірка 24/7", "Заберіть самі за кодом", "locker"), ("truck", "Кур'єр", "30–45 хв, доставка 49 ₴", "courier")]
    w = '<div class="row" style="gap:12px">' + "".join(opt(t, s, i == way, g, icn) for i, (icn, t, s, g) in enumerate(ws)) + "</div>"
    slots = '<div class="row" style="gap:10px">' + "".join('<span class="slot%s">%s</span>' % (" on" if t == ("18:45" if way == 2 else "18:30") else "", t) for t in (["18:00", "18:15", "18:45", "19:15", "19:45", "20:15"] if way == 2 else SLOTS)) + "</div>"
    when = {0: "Коли забрати", 1: "Коли покласти в комірку", 2: "Коли привезти"}[way]
    note = '<span class="s">Комірка тримає +4 °C. Заберіть до 21:00, код прийде в SMS і в застосунок.</span>' if way == 1 else ""
    addr = ""
    if way == 2:
        addr = box("Адреса доставки", '<div class="row" style="gap:12px">' + field("Вулиця й будинок", "вул. Борщагівська, [номер]") + '</div><div class="row" style="gap:12px">' +
                   field("Квартира", "[номер]") + field("Під'їзд", "2") + field("Поверх", "7") + '</div>' + field("Коментар кур'єру", "Домофон не працює, наберіть"))
    alt = {0: "cod", 1: "cod", 2: "cod"}[way]
    pg = {0: "checkout", 1: "locker", 2: "courier"}[way]
    pay = '<div class="row" style="gap:12px">' + opt("Карткою зараз", "Apple Pay, Google Pay, картка", pay_now, pg) + opt("При отриманні", "Карткою або готівкою", not pay_now, alt) + "</div>"
    left = ('<div class="col grow" style="gap:20px">' + box("Як отримати", w) + addr +
            box(when, '<div class="chiprow"><span class="chip on">Сьогодні</span><span class="chip">Завтра</span></div>' + slots + note) +
            box("Оплата", pay + '<div class="row" style="background:var(--tint2);border-radius:16px;padding:14px 18px"><div class="col grow"><span class="t b">Списати бонуси</span><span class="s">На сімейній картці 1 240</span></div><div class="tog off"><i></i></div></div>') +
            box("Контакти", '<div class="row" style="gap:12px"><span class="field">Олена Коваленко</span><span class="field">+380 67 123 45 12</span></div>') + "</div>")
    rtxt = {0: "Віконце, 18:30", 1: "Комірка, до 18:30", 2: "Кур'єр, 18:45"}[way]
    total = "555" if way == 2 else "506"
    nxt = {0: "done", 1: "dlock", 2: "dcour"}[way] if pay_now else "done"
    summ = ('<div class="box" style="width:380px;flex:none"><h3 class="h-m">Ваше замовлення</h3><div class="row"><span class="s grow">Боул з куркою × 2</span><span class="b">298 ₴</span></div>'
            '<div class="row"><span class="s grow">Борщ зі сметаною</span><span class="b">119 ₴</span></div><div class="row"><span class="s grow">Томати на гілці</span><span class="b">89 ₴</span></div><div class="div"></div>'
            '<div class="row"><span class="s grow">Отримання</span><span class="b">%s</span></div>%s'
            '<div class="row"><span class="t b grow">До сплати</span><span class="price" style="font-size:24px">%s ₴</span></div>'
            '<span class="sbtn" style="justify-content:center"%s>%s</span><span class="s">Натискаючи, ви погоджуєтесь з <u%s>умовами</u></span></div>') % (
        rtxt, '<div class="row"><span class="s grow">Доставка</span><span class="b">49 ₴</span></div>' if way == 2 else "", total, go(nxt),
        ("Оплатити %s ₴" % total) if pay_now else "Підтвердити замовлення", go("legal"))
    body = '<div class="main"><span class="crumb"%s>Кошик  /  Оформлення</span><h1 class="h-l">Оформлення</h1><div style="display:flex;gap:40px;align-items:flex-start">' % go("cart") + left + summ + "</div></div>"
    return wrap(body)


def status_page(title, sub, code, steps, extra=""):
    tl = '<div class="tl" style="width:100%">' + "".join('<div class="st"><div class="dot %s">%s</div><span class="t b"%s>%s</span><span class="s">%s</span></div>' % (
        c, ic("check", 16, "var(--onbrand)") if c == "done" else "", "" if c else ' style="color:var(--soft)"', t, s) for t, s, c in steps) + "</div>"
    card = ('<div class="box" style="width:760px;align-self:center;align-items:center;padding:40px;gap:18px;text-align:center">' + okicon() +
            '<h1 class="h-l">%s</h1><p class="p">%s</p>%s%s%s'
            '<div class="row" style="gap:12px;margin-top:8px"><span class="sbtn"%s>Мої замовлення</span><span class="sbtn ghost"%s>На головну</span></div></div>') % (
        title, sub, code, tl, extra, go("account"), go("home"))
    return wrap('<div class="main">' + card + "</div>")


def qrblock(seed, txt):
    return qr(seed, 160) + '<span style="font-size:30px;font-weight:800;letter-spacing:4px">%s</span>' % txt


def p_done():
    return status_page("Замовлення А-274 прийнято", "Віконце видачі, сьогодні о 18:30. Покажіть цей код у віконці.", qrblock(274, "А-274"),
                       [("Прийнято", "18:02", "done"), ("Готуємо на кухні", "зараз", "now"), ("Готово до видачі", "о 18:30", ""), ("Видано", "", "")])


def p_dlock():
    return status_page("Замовлення А-274 прийнято", "Покладемо в комірку до 18:30. Код відкриє дверцята, зберігаємо в холоді до 21:00.", qrblock(1414, "А-274"),
                       [("Прийнято", "18:02", "done"), ("Збираємо", "зараз", "now"), ("У комірці №14", "до 18:30", ""), ("Забрано", "", "")])


def p_dcour():
    return status_page("Замовлення А-274 прийнято", "Кур'єр привезе о 18:45 на вул. Борщагівська, [номер]. Оплачено 555 ₴ разом з доставкою.", "",
                       [("Прийнято", "18:02", "done"), ("Збираємо", "зараз", "now"), ("Кур'єр у дорозі", "≈18:30", ""), ("Доставлено", "", "")],
                       '<div class="row" style="gap:14px;background:var(--tint2);border-radius:16px;padding:14px 18px;width:100%%">%s<span class="t b grow" style="text-align:left">Код для кур\'єра: А-274</span><span class="s">Кур\'єр зателефонує за 10 хв</span></div>' % ic("truck", 22, "var(--brand)"))


def p_cards():
    cards = [("Сімейна", "Один рахунок на всю родину", ["Бонуси всіх членів сім\'ї на одному балансі", "Додавайте до 5 людей", "Спільна історія замовлень"], True, "login"),
             ("Студентська", "За студентським квитком", ["Знижка на комбо з кухні", "Кава зі знижкою до 11:00", "Подвійні бонуси в сесію"], False, "login"),
             ("Індивідуальна", "Для себе", ["Бонуси з кожної покупки", "Персональні пропозиції", "Оплата бонусами до 50%"], False, "login")]
    cs = '<div style="display:flex;gap:20px">' + "".join(
        '<div class="lc%s"><h3 class="h-m" style="font-size:26px">%s</h3><p class="p">%s</p><div style="display:flex;flex-direction:column;gap:10px;margin-top:6px">%s</div>'
        '<span class="sbtn" style="justify-content:center;margin-top:10px;%s"%s>Оформити картку</span></div>' % (
            " dk" if dk else "", t, sub, "".join('<div class="li">%s<span>%s</span></div>' % (ic("check", 18, "var(--accent)" if dk else "var(--brand)"), x) for x in li),
            "background:var(--onbrand);color:var(--deep)" if dk else "", go(g)) for t, sub, li, dk, g in cards) + "</div>"
    steps = [("Оформіть сімейну картку", "На сайті, у застосунку або на касі. Потрібен лише номер телефону."), ("Додайте рідних", "Надішліть запрошення, і їхні покупки підуть на спільний баланс."), ("Витрачайте бонуси разом", "Оплачуйте ними до половини чека будь-кому з родини.")]
    how = ('<div class="box" style="padding:40px;gap:24px"><h2 class="h-l" style="font-size:32px">Як працює сімейна картка</h2><div style="display:flex;gap:28px">' + "".join(
        '<div class="col grow" style="gap:10px"><div class="ib" style="background:var(--tint2);border:none;font-weight:800;font-size:17px">%d</div><span class="t b">%s</span><span class="s">%s</span></div>' % (i + 1, t, d) for i, (t, d) in enumerate(steps)) + "</div></div>")
    have = '<div class="banner"><span class="grow">Уже маєте картку? Увійдіть за номером телефону, і бонуси підтягнуться автоматично.</span><span class="sbtn ghost" style="height:44px"%s>Увійти</span></div>' % go("login")
    body = ('<div class="main"><div class="col" style="gap:8px"><h1 class="h-l">Картка для своїх</h1><p class="p">Три типи карток. Умови бонусів умовні, їх затвердить замовник.</p></div>' + cs + have + how + "</div>")
    return wrap(body, "cards")


def side(active):
    items = [("Замовлення", "account"), ("Картка й бонуси", "bonus"), ("Учасники родини", "addm"), ("Налаштування", "settings")]
    return ('<div class="side col" style="width:240px;flex:none;gap:4px"><div class="row" style="padding:0 6px 16px"><div class="ib" style="width:52px;height:52px;border-radius:26px;background:var(--tint);border:none;font-weight:800;font-size:17px">ОК</div>'
            '<div class="col"><span class="t b">Олена Коваленко</span><span class="s">Сімейна картка</span></div></div>' +
            "".join('<a class="on">%s</a>' % l if k == active else '<a%s>%s</a>' % (go(k), l) for l, k in items) +
            '<a%s style="color:#B3261E">Вийти</a></div>' % go("home"))


def cabinet(active, main, title):
    return wrap('<div class="main"><h1 class="h-l">%s</h1><div style="display:flex;gap:40px;align-items:flex-start">' % title + side(active) + main + "</div></div>")


def famcard():
    return ('<div style="background:var(--deep);color:var(--onbrand);border-radius:24px;padding:26px;width:420px;flex:none;display:flex;flex-direction:column;gap:14px">'
            '<div class="row"><span class="t b grow">Сімейна картка</span><span class="s" style="color:var(--onbrand);opacity:.8">Родина Коваленків</span></div>'
            '<div style="background:#FFFFFF;border-radius:14px;padding:14px;display:flex;justify-content:center">%s</div>'
            '<div class="col"><span class="s" style="color:var(--onbrand);opacity:.8">Спільний баланс</span><span style="font-size:30px;font-weight:800">1 240 бонусів</span></div></div>') % barcode(282, 54)


def p_account():
    orders = [("А-274", "Сьогодні, 18:30 · віконце", "Готуємо", "506 ₴", True), ("А-251", "18 жовтня · комірка 24/7", "Видано", "342 ₴", False), ("А-233", "15 жовтня · кур\'єр", "Видано", "611 ₴", False)]
    ol = '<div class="box" style="padding:8px 24px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:18px 0"%s><div class="col grow"><span class="t b">Замовлення %s</span><span class="s">%s</span></div><span class="chip%s" style="height:32px;font-size:13px">%s</span><span class="price" style="width:90px;text-align:right">%s</span>%s</div>' % (
            go("done") if act else "", n, d, " on" if act else "", s, p, "" if act else '<span class="add"%s>Повторити</span>' % go("cart")) for n, d, s, p, act in orders) + "</div>"
    mem = ('<div class="box grow" style="justify-content:center"><span class="s">Учасники картки</span><div class="row" style="gap:10px">' + "".join(
        '<div class="ib" style="background:%s;border:none;font-weight:700">%s</div>' % (bg, l) for l, bg in [("О", "var(--accent)"), ("А", "var(--tint)"), ("М", "var(--tint2)"), ("Б", "var(--tint)")]) +
           '<div class="ib"%s>%s</div></div><span class="s">4 учасники, можна додати ще одного</span></div>') % (go("addm"), ic("plus", 18))
    main = '<div class="col grow" style="gap:24px"><div style="display:flex;gap:24px;align-items:stretch">' + famcard() + mem + '</div><h2 class="h-m" style="font-size:24px">Замовлення</h2>' + ol + "</div>"
    return cabinet("account", main, "Кабінет")


def p_bonus():
    hist = [("Сьогодні", "Замовлення А-274", "+25"), ("18 жовтня", "Замовлення А-251 · Андрій", "+17"), ("16 жовтня", "Оплата бонусами", "−120"), ("15 жовтня", "Замовлення А-233", "+31")]
    hl = '<div class="box" style="padding:8px 24px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:16px 0"><span class="s" style="width:120px">%s</span><span class="t grow">%s</span><span class="b" style="color:%s">%s</span></div>' % (d, t, "var(--brand)" if v.startswith("+") else "#B3261E", v) for d, t, v in hist) + "</div>"
    rules = box("Як нараховуємо", '<div class="li">%s<span>3%% з кожної покупки в магазині та з кухні</span></div><div class="li">%s<span>Бонусами можна оплатити до 50%% чека</span></div><div class="li">%s<span>Бонуси діють 12 місяців</span></div>' % tuple(ic("check", 18, "var(--brand)") for _ in range(3)) +
                '<span class="s">Умови умовні, їх затвердить замовник. <u%s>Повні правила</u></span>' % go("legal"))
    main = '<div class="col grow" style="gap:24px"><div style="display:flex;gap:24px;align-items:stretch">' + famcard() + rules + '</div><h2 class="h-m" style="font-size:24px">Історія бонусів</h2>' + hl + "</div>"
    return cabinet("bonus", main, "Картка й бонуси")


def p_settings():
    tg = lambda t, s, on: '<div class="row" style="padding:14px 0"><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div><div class="tog%s"><i></i></div></div>' % (t, s, "" if on else " off")
    main = ('<div class="col grow" style="gap:24px">' +
            box("Особисті дані", '<div class="row" style="gap:12px">' + field("Ім'я", "Олена") + field("Прізвище", "Коваленко") + '</div><div class="row" style="gap:12px">' + field("Телефон", "+380 67 123 45 12") + field("E-mail", "olena@[пошта]") + "</div>") +
            box("Адреса доставки", '<div class="row" style="gap:12px">' + field("Вулиця й будинок", "вул. Борщагівська, [номер]") + field("Квартира", "[номер]") + "</div>") +
            '<div class="box" style="gap:0"><h3 class="h-m" style="margin-bottom:4px">Сповіщення</h3>' + tg("Статус замовлення", "SMS і push: прийнято, готуємо, готово", True) + '<div class="div"></div>' + tg("Знижки й новинки кухні", "Не частіше разу на тиждень", False) + '<div class="div"></div>' + tg("Простий режим", "Великий шрифт і менше кнопок", False) + "</div>"
            '<div class="row" style="gap:12px"><span class="sbtn"%s>Зберегти</span><span class="sbtn ghost"%s>Скасувати</span></div></div>') % (go("account"), go("account"))
    return cabinet("settings", main, "Налаштування")


def p_addm():
    main = ('<div class="col grow" style="gap:24px">' + box("Учасники", "".join(
        '<div class="row"><div class="ib" style="background:%s;border:none;font-weight:700">%s</div><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div><span class="chip" style="height:32px;font-size:13px">%s</span></div>' % (bg, l, n, ph, st)
        for l, bg, n, ph, st in [("О", "var(--accent)", "Олена (власниця)", "+380 67 *** ** 12", "Ви"), ("А", "var(--tint)", "Андрій", "+380 50 *** ** 77", "Учасник"), ("М", "var(--tint2)", "Максим", "+380 66 *** ** 03", "Учасник"), ("Б", "var(--tint)", "Богдана", "+380 93 *** ** 58", "Учасниця")])) +
            box("Додати учасника", '<p class="p">Надішлемо SMS із запрошенням. Людина приєднається, коли підтвердить.</p><div class="row" style="gap:12px">' + field("Ім'я", "Марія") + field("Номер телефону", "+380 63 *** ** 41", True) + "</div>"
                '<div class="chiprow"><span class="chip on">Дитина</span><span class="chip">Партнер</span><span class="chip">Батьки</span></div><span class="s">У сімейній картці до 5 учасників. Зараз 4.</span>'
                '<span class="sbtn" style="align-self:flex-start"%s>Надіслати запрошення</span>' % go("account")) + "</div>")
    return cabinet("addm", main, "Учасники родини")


def p_invite():
    inner = ('<span class="s b">Запрошення з SMS</span><h1 class="h-l" style="font-size:34px">Олена запрошує вас до сімейної картки</h1><p class="p">Родина Коваленків · 4 учасники · 1 240 бонусів</p>' +
             "".join('<div class="li">%s<span>%s</span></div>' % (ic("check", 18, "var(--brand)"), t) for t in ["Ваші покупки підуть на спільний баланс", "Бонусами може платити будь-хто з родини", "Вийти з картки можна будь-коли"]) +
             field("Ваш номер", "+380 50 *** ** 77") +
             '<div class="row" style="gap:12px"><span class="sbtn grow" style="justify-content:center"%s>Приєднатися</span><span class="sbtn ghost"%s>Відхилити</span></div>') % (go("account"), go("home"))
    return wrap(centered(inner, 620))


def login(n):
    if n in (110, 123):
        extra = ('<div class="banner">%s<span>Увійдіть, щоб нарахувати бонуси за це замовлення</span></div>' % ic("gift", 20, "var(--brand)")) if n == 123 else ""
        guest = '<span class="s" style="text-align:center"%s>Оформити без входу, без бонусів</span>' % go("checkout") if n == 123 else '<span class="s" style="text-align:center"%s>Немає картки? Ми створимо її після входу</span>' % go("cards")
        inner = (extra + '<h1 class="h-l" style="font-size:34px">Вхід або реєстрація</h1><p class="p">Надішлемо SMS з кодом. Пароль не потрібен.</p>' +
                 '<div class="col" style="gap:6px"><span class="s b">Номер телефону</span><span class="field" style="flex:none;border:2px solid var(--brand)"><b style="margin-right:8px">+380</b>67 123 45 12</span></div>'
                 '<div class="row" style="gap:10px;align-items:flex-start"><span style="width:22px;height:22px;border-radius:7px;background:var(--brand);display:flex;align-items:center;justify-content:center;flex:none">%s</span><span class="s">Погоджуюсь з <u%s>умовами програми лояльності</u> й обробкою персональних даних</span></div>'
                 '<span class="sbtn" style="justify-content:center"%s>Отримати код</span>%s') % (ic("check", 14, "var(--onbrand)", 3), go("legal"), go(111 if n == 110 else 124), guest)
        return wrap(centered(inner))
    bad = n == 133
    codes = '<div class="row" style="gap:12px">' + "".join('<span class="code%s">%s</span>' % (" bad" if bad else (" on" if i == 3 else ""), d) for i, d in enumerate(["4", "8", "1", "9" if bad else ""])) + "</div>"
    back, nxt = {111: (110, 112), 124: (123, 106), 133: (110, 112)}[n]
    inner = ('<span class="crumb"%s>Змінити номер</span><h1 class="h-l" style="font-size:34px">Введіть код</h1><p class="p">Надіслали на +380 67 *** ** 12</p>' % go(back) + codes +
             ('<span class="err">Неправильний код. Залишилось 2 спроби</span>' if bad else "") +
             '<span class="s"%s>Надіслати ще раз через 0:42</span><span class="sbtn" style="justify-content:center"%s>%s</span>') % (
        go(133) if n == 111 else "", go(nxt), "Спробувати ще раз" if bad else "Підтвердити")
    return wrap(centered(inner))


def cardform(t):
    types = [("Сімейна", "Один рахунок на всю родину", "form"), ("Студентська", "За студентським квитком", "student"), ("Індивідуальна", "Для себе", "indiv")]
    tsel = '<div class="row" style="gap:12px">' + "".join(opt(a, b, i == t, g) for i, (a, b, g) in enumerate(types)) + "</div>"
    if t == 1:
        pers = '<div class="row" style="gap:12px">' + field("Ім'я та прізвище", "Марко Петренко") + field("Навчальний заклад", "КНЕУ") + "</div>"
        extra = box("Студентський квиток", '<div class="row" style="gap:14px;border:1px solid var(--line);border-radius:16px;padding:14px"><div style="width:96px;height:64px;border-radius:10px;background:var(--tint2);display:flex;align-items:center;justify-content:center">%s</div><div class="col grow"><span class="t b">kvytok.jpg</span><span class="s">Фото завантажено</span></div><span class="s">Замінити</span></div><span class="s">Перевіримо за 1 робочий день. До того картка працює як індивідуальна.</span>' % ic("card", 24, "var(--brand)"))
        btn, nxt, cname = "Надіслати на перевірку", "check", "Студентська картка"
    elif t == 2:
        pers = '<div class="row" style="gap:12px">' + field("Ім'я", "Ігор") + field("Прізвище", "Савчук") + '</div><div class="row" style="gap:12px">' + field("Дата народження", "03.09.1985") + field("E-mail, за бажанням", "ihor@[пошта]") + "</div>"
        extra = ""
        btn, nxt, cname = "Оформити картку", "idone", "Індивідуальна картка"
    else:
        pers = '<div class="row" style="gap:12px">' + field("Ім'я", "Олена") + field("Прізвище", "Коваленко") + '</div><div class="row" style="gap:12px">' + field("Дата народження", "12.04.1990") + field("E-mail, за бажанням", "olena@[пошта]") + "</div>"
        extra = box("Учасники родини", '<div class="row"><span class="ib" style="background:var(--tint);border:none;font-weight:700">А</span><div class="col grow"><span class="t b">Андрій</span><span class="s">+380 50 *** ** 77</span></div><span class="chip" style="height:32px;font-size:13px">Запрошено</span></div>'
                    '<div class="row" style="gap:12px">' + field("Ім'я", "Марія") + field("Номер телефону", "+380 63 *** ** 41") + '<span class="add" style="align-self:flex-end;height:52px">%sДодати</span></div><span class="s">До 5 людей. Кожен отримає SMS із запрошенням.</span>' % ic("plus", 16))
        btn, nxt, cname = "Оформити картку", "cdone", "Сімейна картка"
    left = '<div class="col grow" style="gap:20px">' + box("Тип картки", tsel) + box("Особисті дані", pers) + extra + "</div>"
    right = ('<div class="col" style="width:380px;flex:none;gap:16px"><div style="background:var(--deep);color:var(--onbrand);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:12px">'
             '<span class="t b">%s</span><div style="background:#FFFFFF;border-radius:14px;height:70px"></div><span class="s" style="color:var(--onbrand);opacity:.8">Номер картки з\'явиться після оформлення</span></div>'
             '<div class="box"><div class="li">%s<span>+100 вітальних бонусів</span></div><div class="li">%s<span>Картка працює на касі, на сайті й у застосунку</span></div>'
             '<span class="sbtn" style="justify-content:center"%s>%s</span></div></div>') % (cname, ic("check", 18, "var(--brand)"), ic("check", 18, "var(--brand)"), go(nxt), btn)
    body = '<div class="main"><span class="crumb"%s>Картки  /  Оформлення</span><h1 class="h-l">Оформлення картки</h1><div style="display:flex;gap:40px;align-items:flex-start">' % go("cards") + left + right + "</div></div>"
    return wrap(body, "cards")


def carddone(title, owner, extra):
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:18px;text-align:center">' + okicon() + '<h1 class="h-l">Картку оформлено</h1><p class="p">Показуйте штрихкод на касі або відкривайте картку в застосунку.</p>'
             '<div style="background:var(--deep);border-radius:24px;padding:22px;width:440px;display:flex;flex-direction:column;gap:12px"><div class="row"><span class="t b grow" style="color:var(--onbrand);text-align:left">%s</span><span class="s" style="color:var(--onbrand);opacity:.8">%s</span></div>'
             '<div style="background:#FFFFFF;border-radius:14px;padding:14px;display:flex;justify-content:center">%s</div></div>%s'
             '<div class="row" style="gap:12px"><span class="sbtn"%s>До кабінету</span><span class="sbtn ghost"%s>До меню кухні</span></div></div>') % (title, owner, barcode(282, 54), extra, go("account"), go("menu"))
    return wrap(centered(inner, 640), "cards")


def p_check():
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center"><div class="ib" style="width:64px;height:64px;border-radius:32px;background:var(--tint);border:none">%s</div>'
             '<h1 class="h-l">Перевіряємо квиток</h1><p class="p">Зазвичай до 1 робочого дня. Повідомимо SMS, щойно студентська знижка запрацює. Поки що картка працює як індивідуальна.</p>'
             '<div class="row" style="gap:12px"><span class="chip">На перевірці</span><span class="s">Марко Петренко · КНЕУ</span></div><span class="sbtn"%s>До кабінету</span></div>') % (ic("clock", 30, "var(--brand)"), go("account"))
    return wrap(centered(inner, 640), "cards")


COFFEE = [("Еспресо", "35 ₴"), ("Американо", "40 ₴"), ("Лате", "50 ₴"), ("Капучино", "50 ₴"), ("Матча", "55 ₴"), ("Чай", "40 ₴")]


def p_coffee():
    menu = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">' + "".join(
        '<div class="opt%s" style="flex:none"><div class="rad%s"></div><span class="t b grow">%s</span><span class="price">%s</span></div>' % (" on" if n == "Лате" else "", " on" if n == "Лате" else "", n, p) for n, p in COFFEE) + "</div>"
    left = ('<div class="col grow" style="gap:20px">' + box("Напій", menu) +
            box("Об'єм і молоко", '<div class="chiprow"><span class="chip">250 мл</span><span class="chip on">350 мл</span><span class="chip">Рослинне молоко +10 ₴</span><span class="chip">Без цукру</span></div>') +
            box("Заберу через", '<div class="row" style="gap:10px"><span class="slot">5 хв</span><span class="slot on">10 хв</span><span class="slot">15 хв</span><span class="slot">20 хв</span></div><span class="s">Віконце кави біля входу працює з 7:30 до 21:00</span>') + "</div>")
    right = ('<div class="col" style="width:380px;flex:none;gap:16px">' + img("z_coffee", 380, 260, 24) +
             '<div class="box"><div class="row"><span class="t b grow">Лате, 350 мл</span><span class="price">50 ₴</span></div><span class="s">+2 бонуси на картку</span>'
             '<span class="sbtn" style="justify-content:center"%s>Оплатити 50 ₴</span></div></div>') % go("cofdone")
    body = '<div class="main"><div class="col" style="gap:8px"><h1 class="h-l">Кава з собою</h1><p class="p">Замовте заздалегідь і заберіть у віконці без черги.</p></div><div style="display:flex;gap:40px;align-items:flex-start">' + left + right + "</div></div>"
    return wrap(body, "coffee")


def p_cofdone():
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center">' + okicon() + '<h1 class="h-l">Кава буде за 10 хв</h1><p class="p">Назвіть код або покажіть QR у віконці кави біля входу.</p>' +
             qrblock(12, "К-12") + '<span class="s">Лате, 350 мл · 50 ₴ · оплачено</span><div class="row" style="gap:12px"><span class="sbtn"%s>На головну</span><span class="sbtn ghost"%s>Меню кухні</span></div></div>') % (go("home"), go("menu"))
    return wrap(centered(inner, 640), "coffee")


def p_legal():
    secs = [("Умови програми лояльності", "Як нараховуються й списуються бонуси, хто може бути учасником сімейної картки, термін дії бонусів."),
            ("Обробка персональних даних", "Які дані збираємо (ім'я, телефон, історія покупок), навіщо і як довго зберігаємо. Як видалити акаунт."),
            ("Умови доставки й видачі", "Віконце видачі, комірка 24/7 (зберігання до 21:00 у день замовлення), кур'єр по Солом'янці за 49 ₴."),
            ("Повернення й заміна", "Якщо щось не так зі стравою чи продуктом, повернемо гроші або замінимо. Що потрібно для повернення."),
            ("Алергени й склад", "Склад і алергени кожної страви вказані на її сторінці. Кухня працює з горіхами й глютеном.")]
    toc = '<div class="side col" style="width:280px;flex:none;gap:4px">' + "".join('<a class="%s">%s</a>' % ("on" if i == 0 else "", t) for i, (t, _) in enumerate(secs)) + "</div>"
    main = '<div class="col grow" style="gap:20px">' + "".join(
        '<div class="box"><h3 class="h-m">%s</h3><p class="p">%s</p><p class="p" style="opacity:.7">Повний текст підготує юрист замовника.</p></div>' % (t, d) for t, d in secs) + "</div>"
    body = '<div class="main"><h1 class="h-l">Умови й документи</h1><div style="display:flex;gap:40px;align-items:flex-start">' + toc + main + "</div></div>"
    return wrap(body)


def p_empty():
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center"><div class="ib" style="width:72px;height:72px;border-radius:36px;background:var(--tint2);border:none">%s</div>'
             '<h1 class="h-l">Кошик порожній</h1><p class="p">Додайте страву з меню кухні або продукти з полиць.</p><div class="row" style="gap:12px"><span class="sbtn"%s>Меню кухні</span><span class="sbtn ghost"%s>Продукти</span></div></div>') % (
        ic("cart", 30, "var(--brand)"), go("menu"), go("shop"))
    return wrap(centered(inner, 640))


def p_payfail():
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center">' + okicon(True) + '<h1 class="h-l">Оплата не пройшла</h1>'
             '<p class="p">Банк відхилив платіж. Гроші не списано. Спробуйте іншу картку або оплатіть при отриманні.</p><div class="row" style="gap:12px"><span class="sbtn"%s>Спробувати ще раз</span><span class="sbtn ghost"%s>Оплатити при отриманні</span></div></div>') % (go("checkout"), go("cod"))
    return wrap(centered(inner, 640))


# ---------- панель персоналу ----------
ANAV = [("Замовлення", 140, "list"), ("Кухня", 142, "dish"), ("Комірки 24/7", 143, "locker"), ("Картки на перевірці", 144, "card"), ("Меню на сьогодні", 145, "book")]


def admin(active, title, body, right=""):
    nav = "".join('<a class="on">%s%s</a>' % (ic(i, 20, "var(--onbrand)"), l) if g == active else '<a%s>%s%s</a>' % (go(g), ic(i, 20, "var(--onbrand)"), l) for l, g, i in ANAV)
    asd = ('<div class="aside"><span class="t b" style="padding:0 14px 6px">Панель магазину</span><span class="s" style="padding:0 14px 20px;color:var(--onbrand);opacity:.7">Зміна: Ірина, адміністраторка</span>' + nav +
           '<div style="flex:1"></div><span class="s" style="padding:0 14px;color:var(--onbrand);opacity:.7">Дані з BAS · оновлено 18:05</span></div>')
    return '<div class="adm">' + asd + '<div class="amain"><div class="row"><h1 class="h-l grow" style="font-size:32px">%s</h1>%s</div>%s</div></div>' % (title, right, body)


def ocard(n, way, items, t, tagc, g=141):
    return '<div class="ocard"%s><div class="row"><span class="t b grow">%s</span><span class="tag %s">%s</span></div><span class="s">%s</span><span class="s b">%s</span></div>' % (go(g), n, tagc, way, items, t)


def a_orders():
    cols = [("Нові", "3", [("А-281", "Віконце", "Боул × 1, Сирники × 2", "до 19:00", "w"), ("А-280", "Кур'єр", "Борщ × 2, Томати 1 кг", "до 18:45", "c"), ("К-14", "Кава", "Капучино 350 мл", "за 5 хв", "w")]),
            ("Готуються", "2", [("А-274", "Віконце", "Боул × 2, Борщ × 1, Томати", "до 18:30", "w"), ("А-277", "Комірка", "Голубці × 2, Яблука 1 кг", "до 18:30", "l")]),
            ("Готові", "2", [("А-270", "Комірка", "У комірці №9", "забрати до 21:00", "l"), ("А-268", "Віконце", "Чекає клієнта", "з 18:10", "w")]),
            ("Видані", "14", [("А-266", "Кур'єр", "Доставлено 18:02", "Максим", "c"), ("А-265", "Віконце", "Видано 17:55", "", "w")])]
    board = '<div style="display:flex;gap:16px;align-items:flex-start;flex:1">' + "".join(
        '<div class="kcol"><div class="row"><span class="t b grow">%s</span><span class="chip" style="height:28px;padding:0 10px;font-size:13px">%s</span></div>%s</div>' % (t, c, "".join(ocard(*o) for o in os)) for t, c, os in cols) + "</div>"
    filt = '<div class="chiprow"><span class="chip on">Усі</span><span class="chip">Віконце</span><span class="chip">Комірка</span><span class="chip">Кур\'єр</span><span class="chip">Кава</span></div>'
    return admin(140, "Замовлення сьогодні", filt + board, '<span class="s">21 жовтня · 18:05</span>')


def a_detail():
    items = [("Боул з куркою та овочами", "× 2", "Кухня · готово", True), ("Борщ зі сметаною", "× 1", "Кухня · готується", False), ("Томати на гілці, 1 кг", "× 1", "Зал · зібрано", True)]
    il = '<div class="box" style="gap:0;padding:8px 24px">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:14px 0"><span style="width:24px;height:24px;border-radius:7px;flex:none;display:flex;align-items:center;justify-content:center;%s">%s</span><span class="t b grow">%s</span><span class="s" style="width:60px">%s</span><span class="s" style="width:180px">%s</span></div>' % (
            "background:var(--brand)" if ok else "border:2px solid var(--line)", ic("check", 14, "var(--onbrand)", 3) if ok else "", n, q, s) for n, q, s, ok in items) + "</div>"
    info = box("Клієнт", '<div class="row"><span class="s grow">Ім\'я</span><span class="b">Олена К.</span></div><div class="row"><span class="s grow">Картка</span><span class="b">Сімейна · 1 240 бонусів</span></div>'
                         '<div class="row"><span class="s grow">Отримання</span><span class="b">Віконце, 18:30</span></div><div class="row"><span class="s grow">Оплата</span><span class="b">Оплачено карткою · 506 ₴</span></div>', "width:400px;flex:none")
    btns = '<div class="row" style="gap:12px"><span class="sbtn"%s>Готово до видачі</span><span class="sbtn ghost"%s>Покласти в комірку</span><span class="sbtn ghost"%s>Повернутися до дошки</span></div>' % (go(140), go(143), go(140))
    body = ('<span class="crumb"%s>Замовлення  /  А-274</span>' % go(140) + '<div style="display:flex;gap:24px;align-items:flex-start"><div class="col grow" style="gap:16px"><h3 class="h-m">Збирання</h3>' + il +
            '<div class="banner">%s<span>Борщ буде готовий за 4 хв, кухня вже бачить замовлення</span></div></div>' % ic("clock", 20, "var(--brand)") + info + "</div>" + btns)
    return admin(140, "Замовлення А-274", body, '<span class="tag w">Віконце · до 18:30</span>')


def a_kitchen():
    dishes = [("d_bowl", "Боул з куркою та овочами", 18, 11, "3 у роботі"), ("d_borsch", "Борщ зі сметаною", 25, 19, "1 у роботі"), ("d_holubtsi", "Голубці", 14, 12, "2 у роботі"),
              ("d_deruny", "Деруни зі сметаною", 16, 6, "—"), ("d_syrnyky", "Сирники зі сметаною", 20, 20, "Розпродано")]
    rows = '<div class="box" style="gap:0;padding:8px 24px">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:12px 0">%s<span class="t b grow">%s</span><span class="s" style="width:110px">Продано %d з %d</span><div style="width:110px;height:8px;border-radius:4px;background:var(--line)"><div style="width:%dpx;height:8px;border-radius:4px;background:var(--brand)"></div></div><span class="s" style="width:90px;text-align:right">%s</span></div>' % (
            img(k, 56, 56, 12), n, s, p, int(110 * s / p), st) for k, n, p, s, st in dishes) + "</div>"
    queue = box("Черга кухні", "".join('<div class="row"><span class="tag %s">%s</span><span class="t grow">%s</span><span class="b">%s</span></div>' % (c, n, d, t) for n, d, t, c in [
        ("А-274", "Борщ × 1", "4 хв", "w"), ("А-277", "Голубці × 2", "8 хв", "l"), ("А-281", "Боул × 1, Сирники × 2", "12 хв", "w"), ("А-280", "Борщ × 2", "15 хв", "c")]) +
                '<span class="sbtn" style="justify-content:center"%s>Позначити готовим</span>' % go(140), "width:340px;flex:none")
    body = '<div style="display:flex;gap:24px;align-items:flex-start"><div class="col grow" style="gap:14px"><h3 class="h-m">План на сьогодні</h3>' + rows + "</div>" + queue + "</div>"
    return admin(142, "Кухня", body, '<span class="s">Одне меню на день</span>')


def a_lockers():
    cells = []
    for i in range(1, 25):
        st = "late" if i in (5,) else ("busy" if i in (3, 9, 14, 17, 21) else "")
        lab = {"late": "Прострочено", "busy": "Зайнято", "": "Вільна"}[st]
        sub = {3: "А-262 · до 21:00", 9: "А-270 · до 21:00", 14: "А-274 · кладемо", 17: "А-259 · до 21:00", 21: "А-263 · до 21:00", 5: "А-241 · з учора"}.get(i, "")
        cells.append('<div class="cell %s"><div class="row"><span class="t b grow">№%d</span><span class="s">%s</span></div><span class="s">%s</span></div>' % (st, i, lab, sub))
    grid = '<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px">' + "".join(cells) + "</div>"
    stats = '<div class="row" style="gap:16px">' + "".join('<div class="box" style="flex:1;gap:4px"><span class="s">%s</span><span style="font-size:28px;font-weight:800">%s</span></div>' % (a, b) for a, b in [("Вільні", "18"), ("Зайняті", "5"), ("Прострочені", "1"), ("Температура", "+4 °C")]) + "</div>"
    body = stats + grid + '<div class="banner bad">%s<span class="grow">Комірка №5: замовлення А-241 не забрали вчора. Зателефонуйте клієнту або поверніть на склад.</span><span class="sbtn ghost" style="height:44px"%s>Відкрити замовлення</span></div>' % (ic("alert", 20, "#B3261E"), go(141))
    return admin(143, "Комірки 24/7", body)


def a_cards(done=False):
    lst = [("Марко Петренко", "КНЕУ · сьогодні 14:20"), ("Аліна Гуменюк", "КПІ · сьогодні 11:02"), ("Денис Ткач", "КНУ · вчора 19:40")]
    if done: lst = lst[1:]
    left = '<div class="box" style="width:380px;flex:none;gap:0;padding:8px 20px">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:14px 0%s"><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div>%s</div>' % (
            ";background:var(--tint2);margin:0 -20px;padding:14px 20px" if i == 0 else "", n, s, ic("next", 16, "var(--soft)")) for i, (n, s) in enumerate(lst)) + "</div>"
    who = lst[0]
    right = ('<div class="box grow" style="gap:16px"><div class="row"><div class="col grow"><h3 class="h-m">%s</h3><span class="s">%s</span></div><span class="tag">Студентська</span></div>'
             '<div style="height:300px;border-radius:18px;background:var(--tint2);display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px">%s<span class="s">Тут буде фото студентського квитка</span></div>'
             '<div class="row" style="gap:12px"><span class="sbtn"%s>Підтвердити</span><span class="sbtn ghost"%s>Відхилити й написати SMS</span></div></div>') % (who[0], who[1], ic("card", 36, "var(--brand)"), go(146), go(146))
    top = ('<div class="banner">%s<span>Студентську картку Марка Петренка підтверджено. Йому надіслано SMS.</span></div>' % ic("check", 20, "var(--brand)")) if done else ""
    body = top + '<div style="display:flex;gap:24px;align-items:flex-start">' + left + right + "</div>"
    return admin(144, "Картки на перевірці", body, '<span class="chip" style="height:32px;font-size:13px">%d на перевірці</span>' % len(lst))


def a_menu(done=False):
    dishes = [("d_bowl", "Боул з куркою та овочами", "149", "18", True), ("d_borsch", "Борщ зі сметаною", "119", "25", True), ("d_soup", "Крем-суп гарбузовий", "99", "12", False),
              ("d_holubtsi", "Голубці", "139", "14", True), ("d_deruny", "Деруни зі сметаною", "109", "16", True), ("d_syrnyky", "Сирники зі сметаною", "99", "20", True)]
    rows = '<div class="box" style="gap:0;padding:8px 24px">' + '<div class="row" style="padding:10px 0"><span class="s b grow">Страва</span><span class="s b" style="width:120px">Ціна</span><span class="s b" style="width:120px">Порцій</span><span class="s b" style="width:120px">У продажу</span></div>' + "".join(
        '<div class="div"></div><div class="row" style="padding:10px 0">%s<span class="t b grow">%s</span><span class="field" style="flex:none;width:100px;height:44px;margin-right:20px">%s ₴</span><span class="field" style="flex:none;width:100px;height:44px;margin-right:20px">%s</span><div style="width:120px"><div class="tog%s"><i></i></div></div></div>' % (
            img(k, 48, 48, 10), n, p, q, "" if on else " off") for k, n, p, q, on in dishes) + "</div>"
    top = ('<div class="banner">%s<span>Меню на 21 жовтня опубліковано на сайті й у застосунку</span></div>' % ic("check", 20, "var(--brand)")) if done else ""
    right = '<span class="sbtn ghost"%s>Скопіювати вчорашнє</span><span class="sbtn"%s>Опублікувати меню</span>' % (go(145), go(147))
    return admin(145, "Меню на сьогодні", top + '<div class="chiprow"><span class="chip">Вчора</span><span class="chip on">Сьогодні, 21 жовтня</span><span class="chip">Завтра</span></div>' + rows +
                 '<span class="s">Ціни умовні, реальні підтягнемо з BAS. Алергени редагуються в картці страви.</span>', right)


# ---------- мобільний сайт ----------
def mwrap(body):
    hdr = '<div class="mh"><div class="ib"%s>%s</div><div style="flex:1"></div><div class="ib"%s>%s<span class="cnt">3</span></div></div>' % (go(151), ic("list", 20), go(153), ic("cart", 20))
    ftr = '<div class="mf"><span class="b">Retail Hub «Солом\'янка»</span><span class="s">вул. [адреса], Солом\'янка · щодня 7:30–22:00 · комірка 24/7</span></div>'
    return '<div class="msite">' + hdr + body + ftr + "</div>"


def m_home():
    zones = [("z_kitchen", "Готова їжа", 152), ("z_coffee", "Кава з собою", 152), ("z_fresh", "Свіжі продукти", 152), ("z_locker", "Комірка 24/7", 153)]
    zs = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' + "".join('<div class="col" style="gap:8px"%s>%s<span class="t b">%s</span></div>' % (go(g), img(k, 169, 120, 16), t) for k, t, g in zones) + "</div>"
    body = ('<div class="mm"><h1 class="h-l" style="font-size:34px">Кухня, продукти й кава біля дому</h1><p class="p">Кава з віконця, обід з нашої кухні й онлайн-замовлення з комірки навіть уночі.</p>'
            '<span class="sbtn" style="justify-content:center"%s>Меню кухні</span>' % go(152) + img("z_space", 350, 220, 20) +
            '<h2 class="h-m" style="font-size:24px">Що є в магазині</h2>' + zs +
            '<div style="background:var(--deep);color:var(--onbrand);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:12px"><h2 class="h-m" style="font-size:24px">Картка для своїх</h2><p class="p" style="color:var(--onbrand);opacity:.8">Сімейна, студентська або індивідуальна.</p>'
            '<span class="sbtn" style="justify-content:center;background:var(--onbrand);color:var(--deep)"%s>Обрати картку</span></div></div>') % go(154)
    return mwrap(body)


def m_nav():
    links = [("Головна", 150), ("Меню кухні", 152), ("Кава з собою", 152), ("Продукти", 152), ("Картки", 154), ("Кошик", 153)]
    body = ('<div class="mm" style="gap:6px"><div class="row"><span class="t b grow">Меню</span><div class="ib"%s>%s</div></div>' % (go(150), ic("back", 20)) +
            "".join('<div class="row" style="height:60px;border-bottom:1px solid var(--line)"%s><span class="h-m grow" style="font-size:22px">%s</span>%s</div>' % (go(g), l, ic("next", 18, "var(--soft)")) for l, g in links) +
            '<span class="sbtn" style="justify-content:center;margin-top:18px"%s>Увійти за номером телефону</span></div>') % go(156)
    return mwrap(body)


def m_menu():
    chips = '<div class="row" style="gap:8px"><span class="chip">Сніданки</span><span class="chip on">Обід</span><span class="chip">Супи</span></div>'
    cards = "".join('<div class="dcard" style="width:350px"%s>%s<div style="padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px"><span class="t b">%s</span><div class="row"><div class="col grow"><span class="s">%s</span><span class="price">%s</span></div><span class="add"%s>%sДодати</span></div></div></div>' % (
        "", img(k, 350, 180, 0), n, w, p, go(153), ic("plus", 16)) for k, n, w, p in DISHES[:4])
    body = '<div class="mm"><h1 class="h-l" style="font-size:32px">Меню кухні на сьогодні</h1>' + chips + cards + "</div>"
    return mwrap(body)


def m_cart():
    items = [("d_bowl", "Боул з куркою", "2", "298 ₴"), ("d_borsch", "Борщ зі сметаною", "1", "119 ₴"), ("g_tomato", "Томати на гілці, 1 кг", "1", "89 ₴")]
    rows = '<div class="box" style="padding:6px 16px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:12px 0">%s<div class="col grow"><span class="t b" style="font-size:15px">%s</span><span class="s">× %s</span></div><span class="b">%s</span></div>' % (
            img(k, 52, 52, 10, "object-fit:%s;background:%s" % (("contain", "#FFFFFF") if k.startswith("g_") else ("cover", "var(--photo)"))), n, q, p) for k, n, q, p in items) + "</div>"
    ways = "".join('<div class="opt%s" style="flex:none"><div class="rad%s"></div><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div></div>' % (" on" if on else "", " on" if on else "", t, s) for t, s, on in [
        ("Віконце видачі", "Сьогодні, 18:30", True), ("Комірка 24/7", "Заберіть за кодом до 21:00", False), ("Кур'єр", "30–45 хв, доставка 49 ₴", False)])
    body = ('<div class="mm"><h1 class="h-l" style="font-size:32px">Кошик</h1>' + rows + '<h3 class="h-m">Як отримати</h3>' + ways +
            '<div class="row" style="background:var(--tint2);border-radius:16px;padding:14px 16px"><div class="col grow"><span class="t b">Списати бонуси</span><span class="s">1 240 на картці</span></div><div class="tog off"><i></i></div></div>'
            '<div class="row"><span class="t b grow">До сплати</span><span class="price" style="font-size:24px">506 ₴</span></div><span class="sbtn" style="justify-content:center"%s>Оплатити 506 ₴</span></div>') % go(155)
    return mwrap(body)


def m_cards():
    cs = "".join('<div class="lc%s" style="flex:none"><h3 class="h-m" style="font-size:24px">%s</h3><p class="p">%s</p><span class="sbtn" style="justify-content:center;%s"%s>Оформити</span></div>' % (
        " dk" if dk else "", t, s, "background:var(--onbrand);color:var(--deep)" if dk else "", go(156)) for t, s, dk in [
        ("Сімейна", "Один баланс бонусів на всю родину, до 5 людей", True), ("Студентська", "Знижки за студентським квитком", False), ("Індивідуальна", "Бонуси з кожної покупки", False)])
    body = '<div class="mm"><h1 class="h-l" style="font-size:32px">Картка для своїх</h1>' + cs + "</div>"
    return mwrap(body)


def m_done():
    body = ('<div class="mm" style="align-items:center;text-align:center">' + okicon() + '<h1 class="h-l" style="font-size:30px">Замовлення А-274 прийнято</h1><p class="p">Віконце видачі, сьогодні о 18:30. Покажіть код у віконці.</p>' +
            qrblock(274, "А-274") + '<span class="sbtn" style="justify-content:center;align-self:stretch"%s>На головну</span></div>') % go(150)
    return mwrap(body)


def m_form():
    f = lambda l, v: '<div class="col" style="gap:6px"><span class="s b">%s</span><span class="field" style="flex:none">%s</span></div>' % (l, v)
    body = ('<div class="mm"><h1 class="h-l" style="font-size:32px">Оформлення картки</h1><div class="col" style="gap:10px">' +
            "".join('<div class="opt%s" style="flex:none"><div class="rad%s"></div><span class="t b grow">%s</span></div>' % (" on" if i == 0 else "", " on" if i == 0 else "", t) for i, t in enumerate(["Сімейна", "Студентська", "Індивідуальна"])) + "</div>" +
            f("Номер телефону", "+380 67 123 45 12") + f("Ім'я", "Олена") + f("Прізвище", "Коваленко") +
            '<span class="s">Надішлемо SMS з кодом для підтвердження. Учасників родини можна додати потім.</span><span class="sbtn" style="justify-content:center"%s>Оформити картку</span></div>') % go(157)
    return mwrap(body)


def m_cdone():
    body = ('<div class="mm" style="align-items:center;text-align:center">' + okicon() + '<h1 class="h-l" style="font-size:30px">Картку оформлено</h1>'
            '<div style="background:var(--deep);border-radius:20px;padding:18px;width:350px;display:flex;flex-direction:column;gap:10px"><span class="t b" style="color:var(--onbrand);text-align:left">Сімейна картка</span>'
            '<div style="background:#FFFFFF;border-radius:12px;padding:12px;display:flex;justify-content:center">%s</div></div><span class="t b" style="color:var(--brand)">+100 вітальних бонусів</span>'
            '<span class="sbtn" style="justify-content:center;align-self:stretch"%s>До меню кухні</span></div>') % (barcode(282, 54), go(152))
    return mwrap(body)


PAGES = {101: p_home, 102: p_menu, 103: p_dish, 104: p_shop, 105: p_cart, 106: lambda: checkout(0), 107: p_done, 108: p_cards, 109: p_account,
         110: lambda: login(110), 111: lambda: login(111), 112: lambda: cardform(0), 113: lambda: carddone("Сімейна картка", "Родина Коваленків", '<div class="row" style="gap:24px"><span class="t b" style="color:var(--brand)">+100 вітальних бонусів</span><span class="s">Запрошення надіслано Андрію</span></div>'),
         114: p_legal, 115: p_settings, 116: p_bonus, 117: p_addm, 118: p_invite, 119: lambda: cardform(1), 120: p_check, 121: p_coffee, 122: p_cofdone,
         123: lambda: login(123), 124: lambda: login(124), 125: lambda: checkout(2), 126: lambda: checkout(1), 127: lambda: checkout(0, False), 128: p_dcour, 129: p_dlock,
         130: lambda: cardform(2), 131: p_empty, 132: p_payfail, 133: lambda: login(133), 134: lambda: carddone("Індивідуальна картка", "Ігор Савчук", '<span class="t b" style="color:var(--brand)">+100 вітальних бонусів</span>'),
         140: a_orders, 141: a_detail, 142: a_kitchen, 143: a_lockers, 144: a_cards, 145: a_menu, 146: lambda: a_cards(True), 147: lambda: a_menu(True),
         150: m_home, 151: m_nav, 152: m_menu, 153: m_cart, 154: m_cards, 155: m_done, 156: m_form, 157: m_cdone}

if __name__ == "__main__":
    jobs, rj = [], []
    for n, fn in PAGES.items():
        h = page("pulse", fn(), extra=CSS).replace("body{background:#ddd", "body{background:var(--bg)")
        assert "{NAME}" not in h and "Пульс" not in h, n
        open(os.path.join(OUT, "w3-%d.html" % n), "w").write(h)
        sel, w = (".adm", 1440) if 140 <= n < 150 else ((".msite", 390) if n >= 150 else (".site", 1440))
        jobs.append(["web%d" % n, "w3-%d.html" % n, sel, w, 900])
    json.dump(jobs, open(os.path.join(OUT, "xw3.json"), "w"))
    json.dump({n: fname(n) for n in PAGES}, open(os.path.join(OUT, "wnames3.json"), "w"), ensure_ascii=False)
    print(len(PAGES))
