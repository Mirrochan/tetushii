"""Застосунок v3: усі 41 екран, без назви й лого, з закритими сценаріями."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p2
p2.mark = lambda *a, **k: ""
p2.TABS = [("home", "Головна", 2), ("dish", "Меню", 3), ("bag", "Продукти", 5), ("cart", "Кошик", 6), ("user", "Профіль", 14)]


def tabbar(active):
    out = []
    for i, (icn, lab, go) in enumerate(p2.TABS):
        on = " on" if i == active else ""
        dg = "" if i == active else ' data-go="%d"' % go
        badge = '<span style="position:absolute;left:50%%;margin-left:6px;top:-4px;min-width:18px;height:18px;border-radius:9px;background:var(--accent);color:var(--ink);font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center">3</span>' if icn == "cart" and not getattr(p2, 'NOBADGE', False) else ""
        out.append('<div class="tab%s"%s style="position:relative">%s<span>%s</span>%s</div>' % (on, dg, p2.ic(icn, 24), lab, badge))
    return '<div class="tabbar">' + "".join(out) + "</div>"


p2.tabbar = tabbar
from p2 import ic, phone, top, content, page, img, OUT, ready, barcode, qr, MENU, GROC
import extra, p3
from p3 import CSS, g

CSS = CSS + ".allg{display:flex;gap:6px;flex-wrap:wrap}.allg span{height:28px;padding:0 10px;border-radius:14px;border:1px solid var(--line);background:var(--surface);font-size:12px;font-weight:600;display:flex;align-items:center}\n.code.bad{border:2px solid #B3261E;color:#B3261E}"


def opt(icn, t, s, on, go=None):
    return '<div class="opt%s"%s><div class="rad%s"></div><div class="col grow"><h3>%s</h3><span class="s">%s</span></div>%s</div>' % (
        " on" if on else "", g(go) if go and not on else "", " on" if on else "", t, s, ic(icn, 22, "var(--brand)"))


# ---------- головні ----------
def s02():
    head = '<div class="top"><div class="ib"%s style="margin-left:auto">%s</div></div>' % (g(13), ic("card", 20))
    feat = ('<div class="card" style="padding:0;overflow:hidden"%s>' % g(4) + img("d_bowl", 350, 170, 0) +
            '<div class="row" style="padding:14px 16px 16px;align-items:flex-end"><div class="col grow"><span class="xs">Кухня сьогодні</span><h3>Боул з куркою та овочами</h3><span class="s">420 ккал · готуємо 15 хв</span></div>'
            '<div class="btn sm"%s>Меню</div></div></div>' % g(3))
    tiles = '<div class="row" style="gap:8px;align-items:stretch">' + "".join(
        '<div class="tint2 col" style="flex:1;padding:12px 10px;gap:8px;border-radius:16px"%s>%s<span style="font-size:12px;font-weight:600;line-height:1.2">%s</span></div>' % (
            g(go), ic(i, 22, "var(--brand)"), l) for i, l, go in [("dish", "Готова їжа", 3), ("bag", "Продукти", 5), ("coffee", "Кава з собою", 19), ("locker", "Комірка 24/7", 32)]) + "</div>"
    order = ('<div class="tint row" style="padding:12px 14px"%s>%s<div class="col grow"><h3>Замовлення А-274</h3><span class="s">Готуємо, буде о 18:30</span></div>%s</div>' % (
        g(9), '<div class="ib" style="background:var(--surface);border:none">%s</div>' % ic("clock", 20, "var(--brand)"), ic("next", 18, "var(--soft)")))
    body = head + content('<div class="col" style="gap:2px"><span class="s">Привіт, Олено!</span><h1>Що сьогодні на обід?</h1></div>',
                          '<div class="card row" style="padding:12px 14px;border-radius:16px"%s>%s<span class="s">Що приготувати сьогодні?</span></div>' % (g(3), ic("search", 18, "var(--soft)")),
                          feat, tiles, order, style="gap:14px")
    return phone(body, tab=0)


def dishrow(key, name, meta, price, go=4):
    return ('<div class="card row" style="padding:10px;gap:12px"%s>%s<div class="col grow"><h3>%s</h3><span class="s">%s</span>'
            '<span class="price" style="margin-top:4px">%s</span></div><div class="ib sm p"%s>%s</div></div>') % (
        g(go), img(key, 76, 76, 14), name, meta, price, g(6), ic("plus", 16))


def s03():
    chips = '<div class="row" style="gap:8px">' + "".join('<span class="chip%s">%s</span>' % (" on" if i == 1 else "", c) for i, c in enumerate(["Сніданки", "Обід", "Супи", "Комбо"])) + "</div>"
    rows = "".join(dishrow(k, n, m, p) for k, n, m, p, _ in MENU[:5])
    body = top("Меню кухні", back=2) + content(chips, '<span class="s">Одне меню на день, готуємо тут, у магазині</span>', rows, style="gap:10px")
    return phone(body, tab=1)


def s04():
    hero = '<div style="position:relative;height:270px;flex:none">' + img("d_bowl", 390, 270, 0, "position:absolute;left:0;top:0") + \
           '<div class="ib"%s style="position:absolute;left:20px;top:52px">%s</div></div>' % (g(3), ic("back", 20))
    nut = '<div class="row" style="gap:8px">' + "".join(
        '<div class="tint2 col" style="flex:1;align-items:center;padding:10px 4px;border-radius:14px;gap:2px"><span class="b" style="font-size:15px">%s</span><span class="xs">%s</span></div>' % (a, b)
        for a, b in [("420", "ккал"), ("32 г", "білки"), ("14 г", "жири"), ("40 г", "вуглеводи")]) + "</div>"
    allg = '<div class="col" style="gap:6px"><span class="lbl">Алергени</span><div class="allg"><span>Кунжут</span><span>Гірчиця</span><span>Може містити сліди горіхів</span></div></div>'
    body = hero + content('<span class="badge">%sОвочі від локальних фермерів</span>' % ic("leaf", 14),
                          '<h1>Боул з куркою та овочами</h1>', '<span class="s">380 г · готуємо 15 хв</span>',
                          '<p class="t">Курка, нут, авокадо, томати й зелень. Готуємо на кухні магазину щодня.</p>', nut, allg,
                          style="gap:10px;padding-top:16px")
    bottom = ('<div class="row"><div class="card row" style="padding:0 14px;height:54px;border-radius:16px;gap:16px">%s<span class="b">1</span>%s</div>'
              '<div class="btn grow"%s>Додати · 149 ₴</div></div>') % (ic("minus", 18), ic("plus", 18), g(6))
    return phone(body, bottom=bottom)


def s05():
    chips = '<div class="row" style="gap:8px">' + "".join('<span class="chip%s">%s</span>' % (" on" if i == 0 else "", c) for i, c in enumerate(["Овочі й фрукти", "Молочне", "Хліб", "Для тварин"])) + "</div>"
    grid = '<div class="grid2">' + "".join(
        '<div class="card col" style="padding:10px;gap:6px;border-radius:18px">%s<span style="font-size:14px;font-weight:600">%s</span><div class="row"><div class="col grow"><span class="xs">%s</span><span class="price">%s</span></div><div class="ib sm p"%s>%s</div></div></div>' % (
            img(k, 153, 92, 12, "object-fit:contain;background:#FFFFFF"), n, w, p, g(6), ic("plus", 16)) for k, n, w, p in GROC[:4]) + "</div>"
    body = top("Продукти", back=2) + content(
        '<div class="card row" style="padding:12px 14px;border-radius:16px">%s<span class="s">Знайти продукт</span></div>' % ic("search", 18, "var(--soft)"),
        chips, grid, '<span class="xs">Ціни умовні, реальні підтягнемо з BAS</span>', style="gap:12px")
    return phone(body, tab=2)


def s06():
    items = [("d_bowl", "Боул з куркою", "298 ₴"), ("d_borsch", "Борщ зі сметаною", "119 ₴"), ("g_tomato", "Томати на гілці, 1 кг", "89 ₴")]
    qty = ["2", "1", "1"]
    rows = "".join('<div class="card row" style="padding:10px">%s<div class="col grow" style="gap:6px"><h3>%s</h3><div class="row" style="gap:12px">%s<span class="b">%s</span>%s</div></div><span class="price">%s</span></div>' % (
        img(k, 60, 60, 12, "object-fit:%s;background:%s" % (("contain", "#FFFFFF") if k.startswith("g_") else ("cover", "var(--photo)"))), n, ic("minus", 16, "var(--soft)"), q, ic("plus", 16, "var(--soft)"), p) for (k, n, p), q in zip(items, qty))
    summ = ('<div class="col" style="gap:10px;margin-top:auto"><div class="row"><span class="t grow" style="color:var(--soft)">Бонусів нарахуємо</span><span class="b" style="color:var(--brand)">+25</span></div>'
            '<div class="div"></div><div class="row"><h2 class="grow">Разом</h2><h2>506 ₴</h2></div></div>')
    body = top("Кошик", back=3, right='<span class="s" style="margin-left:auto"%s>Очистити</span>' % g(35)) + content(rows, summ, style="gap:10px")
    return phone(body, tab=3, bottom='<div class="btn"%s>Оформити замовлення</div>' % g(7))


SLOTS = ["17:30", "18:00", "18:30", "19:00", "19:30", "20:00"]


def recv(sel, back, nxt):
    o = (opt("window", "Віконце видачі", "Без черги, безкоштовно", sel == 0, 7) +
         opt("locker", "Комірка-холодильник 24/7", "Заберіть самі за кодом", sel == 1, 32) +
         opt("truck", "Кур'єр", "30–45 хв, доставка 49 ₴", sel == 2, 21))
    days = '<div class="row" style="gap:8px"><span class="chip on">Сьогодні</span><span class="chip">Завтра</span></div>'
    slots = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">' + "".join(
        '<span class="chip%s" style="justify-content:center;height:42px">%s</span>' % (" on" if t == "18:30" else "", t) for t in SLOTS) + "</div>"
    note = '<span class="xs">Покладемо в комірку до 18:30 і триматимемо в холоді до 21:00</span>' if sel == 1 else ""
    body = top("Отримання", back=back) + content('<h3>Як отримати</h3>', o, '<h3 style="margin-top:6px">Коли %s</h3>' % ("покласти" if sel == 1 else ""), days, slots, note, style="gap:10px")
    return phone(body, bottom='<div class="btn"%s>Далі до оплати</div>' % g(nxt))


def pay(now, back, recv_txt, total, nxt, deliv=False, alt=None):
    o = (opt("card", "Карткою зараз", "Apple Pay, Google Pay, картка", now, alt) +
         opt("bag", "При отриманні", "Карткою або готівкою", not now, alt))
    bon = '<div class="tint2 row" style="padding:14px 16px"><div class="col grow"><h3>Списати бонуси</h3><span class="s">На сімейній картці 1 240</span></div><div class="tog off"><i></i></div></div>'
    summ = ('<div class="card col" style="gap:8px;margin-top:auto"><div class="row"><span class="s grow">Отримання</span><span class="t b">%s</span></div>'
            '<div class="row"><span class="s grow">3 позиції</span><span class="t b">506 ₴</span></div>%s'
            '<div class="div"></div><div class="row"><span class="t b grow">Разом</span><span class="t b">%s ₴</span></div></div>') % (
        recv_txt, '<div class="row"><span class="s grow">Доставка</span><span class="t b">49 ₴</span></div>' if deliv else "", total)
    btn = ("Оплатити %s ₴" % total) if now else "Підтвердити замовлення"
    body = top("Оплата", back=back) + content(o, bon, summ, style="gap:10px")
    return phone(body, bottom='<div class="btn"%s>%s</div>' % (g(nxt), btn))


s07 = lambda: recv(0, 6, 8)
s32 = lambda: recv(1, 6, 33)
s08 = lambda: pay(True, 7, "Віконце, сьогодні 18:30", "506", 9, alt=34)
s34 = lambda: pay(False, 7, "Віконце, сьогодні 18:30", "506", 9, alt=8)
s33 = lambda: pay(True, 32, "Комірка, до 18:30", "506", 11, alt=34)
s22 = lambda: pay(True, 21, "Кур'єр, сьогодні 18:45", "555", 12, deliv=True, alt=34)


def s13():
    card = ('<div class="dark col" style="gap:12px;padding:18px 18px 16px"><div class="row"><span class="t b grow">Сімейна картка</span><span class="s">Родина Коваленків</span></div>'
            '<div style="background:#FFFFFF;border-radius:12px;padding:12px 14px;display:flex;justify-content:center">%s</div>'
            '<span class="xs" style="text-align:center;letter-spacing:2px">2200 4417 0935</span></div>') % barcode(282, 54)
    av = '<div class="row" style="gap:8px">' + "".join('<div class="ib" style="background:%s;border:none;font-weight:700;color:%s">%s</div>' % (bg, c, l) for l, bg, c in [
        ("О", "var(--accent)", "var(--ink)"), ("А", "var(--brand)", "var(--onbrand)"), ("М", "var(--tint)", "var(--ink)"), ("Б", "var(--tint2)", "var(--ink)")]) + \
         '<div class="ib"%s>%s</div><span class="s" style="margin-left:4px">4 учасники</span></div>' % (g(29), ic("plus", 18))
    body = top("Моя картка", back=14) + content(card, '<div class="col" style="gap:0"><span class="s">Спільний баланс</span><span style="font-size:32px;font-weight:800;letter-spacing:-.5px">1 240 бонусів</span></div>', av,
                                              '<div class="card col" style="gap:10px"><span class="s">Змінити тип картки</span><div class="row" style="gap:8px"><span class="chip"%s>Студентська</span><span class="chip"%s>Індивідуальна</span></div></div>' % (g(25), g(38)),
                                              style="gap:14px")
    return phone(body, tab=4)


def s14():
    items = [("card", "Моя картка", "Сімейна · 1 240 бонусів", 13), ("list", "Мої замовлення", "Останнє: А-274", 30), ("pin", "Адреси доставки", "вул. Борщагівська", 41),
             ("alert", "Сповіщення", "", 31), ("check", "Простий режим", "Великий шрифт і менше кнопок", 31)]
    li = '<div class="card col" style="padding:6px 14px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:10px 0"%s>%s<div class="col grow"><h3>%s</h3>%s</div>%s</div>' % (
            g(go), '<div class="ib sm" style="background:var(--tint2);border:none">%s</div>' % ic(i, 16, "var(--brand)"), t,
            ('<span class="xs">%s</span>' % s) if s else "", ic("next", 16, "var(--soft)")) for i, t, s, go in items) + "</div>"
    body = top("Профіль") + content('<div class="row"><div class="ib" style="width:60px;height:60px;border-radius:30px;background:var(--tint);border:none;font-size:22px;font-weight:800">ОК</div>'
                                    '<div class="col"><h2>Олена Коваленко</h2><span class="s">+380 67 *** ** 12</span></div></div>', li, style="gap:14px")
    return phone(body, tab=4)


# ---------- вхід / картки ----------
def login(n):
    if n == 23:
        body = top("Вхід", back=1) + content('<h1>З поверненням</h1>', '<p class="t" style="color:var(--soft)">Введіть номер, до якого прив\'язана картка. Надішлемо SMS з кодом.</p>',
                                             '<div class="col" style="gap:6px;margin-top:8px"><span class="lbl">Номер телефону</span><div class="fld" style="border:2px solid var(--brand)"><span class="b">+380</span><span>67 123 45 12</span></div></div>',
                                             '<span class="s"%s>Ще немає картки? Оформити</span>' % g(15), style="gap:12px;padding-top:12px")
        return phone(body, bottom='<div class="btn"%s>Отримати код</div>' % g(24))
    bad = n == 36
    codes = '<div class="row" style="gap:10px;justify-content:center">' + "".join('<div class="code%s">%s</div>' % (" bad" if bad else (" on" if i == 3 else ""), d) for i, d in enumerate(["4", "8", "1", "9" if bad else ""])) + "</div>"
    msg = '<span class="err" style="text-align:center">Неправильний код. Залишилось 2 спроби</span>' if bad else ""
    back, nxt = {24: (23, 2), 36: (15, 17)}.get(n, (15, 17))
    body = top("Код з SMS", back=back) + content('<h1>Введіть код</h1>', '<p class="t" style="color:var(--soft)">Надіслали на +380 67 *** ** 12</p>', codes, msg,
                                                 '<span class="s" style="text-align:center">Надіслати ще раз через 0:42</span>', style="gap:14px;padding-top:12px")
    return phone(body, bottom='<div class="btn"%s>%s</div>' % (g(nxt), "Спробувати ще раз" if bad else "Підтвердити"))


def a16():
    codes = '<div class="row" style="gap:10px;justify-content:center">' + "".join('<div class="code%s">%s</div>' % (" on" if i == 3 else "", d) for i, d in enumerate(["4", "8", "1", ""])) + "</div>"
    body = top("Код з SMS", back=15) + content('<h1>Введіть код</h1>', '<p class="t" style="color:var(--soft)">Надіслали на +380 67 *** ** 12</p>', codes,
                                               '<span class="s" style="text-align:center"%s>Надіслати ще раз через 0:42</span>' % g(36), style="gap:14px;padding-top:12px")
    return phone(body, bottom='<div class="btn"%s>Підтвердити</div>' % g(17))


def seg(on):
    labs = [("Сімейна", 17), ("Студентська", 25), ("Індивідуальна", 38)]
    return '<div class="seg">' + "".join('<span class="on">%s</span>' % l if i == on else '<span%s>%s</span>' % (g(go), l) for i, (l, go) in enumerate(labs)) + "</div>"


def fld(l, v):
    return '<div class="col" style="gap:6px"><span class="lbl">%s</span><div class="fld">%s</div></div>' % (l, v)


def a17():
    mem = ('<div class="card col" style="gap:10px;padding:12px 14px"><span class="lbl">Учасники родини</span>'
           '<div class="row"><div class="ib sm" style="background:var(--tint);border:none;font-weight:700;font-size:13px">А</div><div class="col grow"><span class="t b">Андрій</span><span class="xs">+380 50 *** ** 77</span></div><span class="xs">запрошено</span></div>'
           '<div class="dash"%s>%sДодати учасника</div></div>') % (g(40), ic("plus", 18, "var(--brand)"))
    body = top("Оформлення картки", back=16) + content(seg(0), fld("Ім'я", "Олена"), fld("Прізвище", "Коваленко"), fld("Дата народження", "12.04.1990"), mem,
                                                       style="gap:12px;padding-top:6px")
    return phone(body, bottom='<div class="btn"%s>Оформити картку</div>' % g(18))


def a25():
    body = top("Оформлення картки", back=16) + content(seg(1), fld("Ім'я та прізвище", "Марко Петренко"), fld("Навчальний заклад", "КНЕУ"),
        '<div class="col" style="gap:6px"><span class="lbl">Студентський квиток</span><div class="card row" style="padding:12px">'
        '<div style="width:64px;height:44px;border-radius:8px;background:var(--tint2);display:flex;align-items:center;justify-content:center">%s</div>'
        '<div class="col grow"><span class="t b">kvytok.jpg</span><span class="xs">Фото завантажено</span></div><span class="s">Замінити</span></div></div>' % ic("card", 20, "var(--brand)"),
        '<span class="xs">Перевіримо квиток за 1 робочий день. До того картка працює як індивідуальна.</span>', style="gap:12px;padding-top:6px")
    return phone(body, bottom='<div class="btn"%s>Надіслати на перевірку</div>' % g(26))


def a38():
    body = top("Оформлення картки", back=16) + content(seg(2), fld("Ім'я", "Ігор"), fld("Прізвище", "Савчук"), fld("Дата народження", "03.09.1985"),
        '<div class="tint2 row" style="padding:12px 14px">%s<span class="t">Бонуси з кожної покупки, лише для вас</span></div>' % ic("gift", 20, "var(--brand)"),
        style="gap:12px;padding-top:6px")
    return phone(body, bottom='<div class="btn"%s>Оформити картку</div>' % g(39))


def cardview(title, sub, extra_html):
    card = ('<div class="dark col" style="gap:12px;padding:18px"><div class="row"><span class="t b grow">%s</span><span class="s">%s</span></div>'
            '<div style="background:#FFFFFF;border-radius:12px;padding:12px 14px;display:flex;justify-content:center">%s</div>'
            '<span class="xs" style="text-align:center;letter-spacing:2px">2200 4417 0935</span></div>') % (title, sub, barcode(282, 54))
    return card, extra_html


def a28():
    c, e = cardview("Сімейна картка", "Родина Коваленків", '<div class="tint2 row" style="padding:12px 16px">%s<span class="t b">Спільний баланс: 1 240 бонусів</span></div>' % ic("gift", 20, "var(--brand)"))
    return ready("Ви в сімейній картці", "Родина Коваленків · 5 учасників", c, e)


def a39():
    c, e = cardview("Індивідуальна картка", "Ігор Савчук", '<div class="tint2 row" style="padding:12px 16px">%s<span class="t b">+100 вітальних бонусів</span></div>' % ic("gift", 20, "var(--brand)"))
    return ready("Картку оформлено", "Показуйте її на касі або в застосунку", c, e)


def a29(ret=13):
    body = top("Додати учасника", back=ret) + content(
        '<p class="t" style="color:var(--soft)">Надішлемо SMS із запрошенням. Людина приєднається, коли підтвердить.</p>',
        fld("Ім'я", "Марія"), fld("Номер телефону", "+380 63 *** ** 41"),
        '<span class="lbl">Хто це</span><div class="row" style="gap:8px"><span class="chip on">Дитина</span><span class="chip">Партнер</span><span class="chip">Батьки</span></div>',
        '<span class="xs">У сімейній картці до 5 учасників. Зараз 4.</span>', style="gap:12px")
    return phone(body, bottom='<div class="btn"%s>Надіслати запрошення</div>' % g(ret))


def a20():
    card = ('<div class="card col" style="align-items:center;gap:10px;padding:22px">%s<span style="font-size:28px;font-weight:800;letter-spacing:3px">К-12</span>'
            '<span class="s" style="text-align:center">Назвіть код або покажіть QR у віконці кави</span></div>') % qr(12, 170)
    e = '<div class="card row" style="padding:12px 16px">%s<div class="col"><h3>Лате, 350 мл · 50 ₴</h3><span class="s">Оплачено, +2 бонуси</span></div></div>' % ic("coffee", 20, "var(--brand)")
    return ready("Кава буде за 10 хв", "Віконце кави біля входу", card, e)


def a21(profile=False):
    f = lambda l, v, grow=False: '<div class="col%s" style="gap:6px"><span class="lbl">%s</span><div class="fld">%s</div></div>' % (" grow" if grow else "", l, v)
    body = top("Адреса доставки", back=14 if profile else 7) + content(
        '<div style="height:130px;border-radius:18px;background:var(--photo);display:flex;align-items:center;justify-content:center;gap:8px">%s<span class="t b">Тут буде карта</span></div>' % ic("map", 22, "var(--ink)"),
        f("Вулиця й будинок", "вул. Борщагівська, [номер]"),
        '<div class="row" style="gap:10px">' + f("Квартира", "[номер]", True) + f("Під'їзд", "2", True) + f("Поверх", "7", True) + "</div>",
        f("Коментар кур'єру", "Домофон не працює, наберіть"),
        '<div class="row"><span class="t grow">Залишити біля дверей</span><div class="tog off"><i></i></div></div>',
        '<div class="tint2 row" style="padding:12px 14px">%s<span class="t">Доставка 49 ₴, 30–45 хв по Солом\'янці</span></div>' % ic("truck", 20, "var(--brand)"),
        style="gap:10px")
    return phone(body, bottom='<div class="btn"%s>%s</div>' % (g(14), "Зберегти адресу") if profile else '<div class="btn"%s>Далі до оплати</div>' % g(22))


def a30():
    rows = [("А-274", "Сьогодні, 18:30 · віконце", "Готуємо", True), ("А-251", "18 жовтня · комірка 24/7", "Видано", False), ("А-233", "15 жовтня · кур'єр", "Видано", False)]
    cards = "".join('<div class="card col" style="gap:8px"%s><div class="row"><span class="t b grow">Замовлення %s</span><span class="chip%s" style="height:28px;font-size:12px">%s</span></div><span class="s">%s</span>%s</div>' % (
        g(9) if act else "", n, " on" if act else "", s, d, "" if act else '<div class="row"><span class="s grow">3 позиції · 342 ₴</span><span class="btn sm"%s>Повторити</span></div>' % g(6)) for n, d, s, act in rows)
    return phone(top("Мої замовлення", back=14) + content(cards, style="gap:10px"), tab=4)


def a35():
    p2.NOBADGE = True
    try:
        return _a35()
    finally:
        p2.NOBADGE = False


def _a35():
    body = top("Кошик", back=3) + ('<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:0 32px;text-align:center">'
                                   '<div class="ib" style="width:72px;height:72px;border-radius:36px;background:var(--tint2);border:none">%s</div><h2>Кошик порожній</h2>'
                                   '<p class="t" style="color:var(--soft)">Додайте страву з меню кухні або продукти з полиць.</p></div>') % ic("cart", 30, "var(--brand)")
    return phone(body, tab=3, bottom='<div class="btn"%s>Перейти до меню</div>' % g(3))


T = {1: ("Старт", p3.a01), 2: ("Головна", s02), 3: ("Меню кухні", s03), 4: ("Страва", s04), 5: ("Продукти", s05), 6: ("Кошик", s06),
     7: ("Отримання · віконце", s07), 8: ("Оплата", s08), 9: ("Статус замовлення", p2.s09), 10: ("Готово у віконці", p2.s10), 11: ("Комірка-холодильник", p2.s11),
     12: ("Кур'єр", p2.s12), 13: ("Моя картка", s13), 14: ("Профіль", s14), 15: ("Номер телефону", extra.a15), 16: ("Код з SMS", a16),
     17: ("Оформлення · сімейна", a17), 18: ("Сімейну картку оформлено", extra.a18), 19: ("Кава з собою", p3.a19), 20: ("Кава замовлена", a20),
     21: ("Адреса доставки", a21), 22: ("Оплата · кур'єр", s22), 23: ("Вхід", lambda: login(23)), 24: ("Вхід · код", lambda: login(24)),
     25: ("Оформлення · студентська", a25), 26: ("Перевіряємо квиток", p3.a26), 27: ("Запрошення в родину", p3.a27), 28: ("Ви в сімейній картці", a28),
     29: ("Додати учасника", a29), 30: ("Мої замовлення", a30), 31: ("Налаштування", p3.a31), 32: ("Отримання · комірка", s32),
     33: ("Оплата · комірка", s33), 34: ("Оплата при отриманні", s34), 35: ("Кошик порожній", a35), 36: ("Неправильний код", lambda: login(36)),
     37: ("Оплата не пройшла", p3.a37), 38: ("Оформлення · індивідуальна", a38), 39: ("Індивідуальну картку оформлено", a39),
     40: ("Додати учасника · реєстрація", lambda: a29(17)), 41: ("Адреса в профілі", lambda: a21(True))}

if __name__ == "__main__":
    for n, (_, fn) in T.items():
        h = page("pulse", fn(), extra=CSS)
        assert "{NAME}" not in h and "Пульс" not in h, n
        open(os.path.join(OUT, "v3-%02d.html" % n), "w").write(h)
    json.dump([["v3-%02d" % n, 390, 844] for n in T], open(os.path.join(OUT, "jv3.json"), "w"))
    json.dump([["app%02d" % n, "v3-%02d.html" % n, ".phone", 390, 844] for n in T], open(os.path.join(OUT, "xv3.json"), "w"))
    json.dump({n: "%02d %s" % (n, t) for n, (t, _) in T.items()}, open(os.path.join(OUT, "names3.json"), "w"), ensure_ascii=False)
    print(len(T))
