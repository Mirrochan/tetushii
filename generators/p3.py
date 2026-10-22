"""Нові екрани застосунку (без назви магазину)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from p2 import ic, phone, top, content, page, img, OUT, ready
from extra import APP_CSS

CSS = APP_CSS + """
.tog{width:46px;height:28px;border-radius:14px;background:var(--brand);padding:3px;display:flex;justify-content:flex-end;flex:none}
.tog i{width:22px;height:22px;border-radius:11px;background:var(--onbrand);display:block}
.tog.off{background:var(--line);justify-content:flex-start}
.err{color:#B3261E;font-size:13px;font-weight:600}
"""


def g(n):
    return ' data-go="%d"' % n


def a01():
    photos = '<div class="row" style="gap:8px">' + img("d_bowl", 160, 150, 20) + '<div class="col" style="gap:8px">' + img("d_borsch", 162, 71, 16) + img("d_syrnyky", 162, 71, 16) + "</div></div>"
    perks = "".join('<div class="row" style="gap:10px">%s<span class="t">%s</span></div>' % (ic("check", 18, "var(--brand)"), t) for t in [
        "Бонуси з кожної покупки й обіду з кухні", "Сімейна, студентська або індивідуальна картка", "Замовлення з віконця, комірки чи кур'єром"])
    body = '<div class="top" style="padding-top:52px"></div>' + content(photos, '<h1 style="margin-top:6px">Кухня, продукти й кава біля дому</h1>', perks, style="gap:14px")
    bottom = ('<div class="col" style="gap:10px"><div class="btn"%s>Оформити картку</div><div class="btn ghost"%s>Увійти, у мене вже є картка</div>'
              '<span class="s" style="text-align:center;padding:6px 0"%s>Продовжити без картки</span></div>') % (g(15), g(23), g(2))
    return phone(body, bottom=bottom)


COFFEE = [("Еспресо", "35 ₴"), ("Американо", "40 ₴"), ("Лате", "50 ₴"), ("Капучино", "50 ₴"), ("Матча", "55 ₴"), ("Чай", "40 ₴")]


def a19():
    hero = '<div style="position:relative;height:190px;flex:none">' + img("z_coffee", 390, 190, 0, "position:absolute;left:0;top:0") + '<div class="ib"%s style="position:absolute;left:20px;top:52px">%s</div></div>' % (g(2), ic("back", 20))
    rows = '<div class="card col" style="padding:4px 14px;gap:0">' + '<div class="div"></div>'.join(
        '<div class="row" style="padding:11px 0"><span class="t b grow">%s</span><span class="price">%s</span>%s</div>' % (
            n, p, '<div class="rad on"></div>' if n == "Лате" else '<div class="rad"></div>') for n, p in COFFEE) + "</div>"
    opts = ('<div class="row" style="gap:8px"><span class="chip">250 мл</span><span class="chip on">350 мл</span><span class="chip">Рослинне молоко +10 ₴</span></div>'
            '<span class="lbl">Заберу через</span><div class="row" style="gap:8px"><span class="chip">5 хв</span><span class="chip on">10 хв</span><span class="chip">15 хв</span></div>')
    body = hero + content('<h1 style="font-size:26px">Кава з собою</h1><span class="s">Віконце кави працює з 7:30, без входу в магазин</span>', rows, opts, style="gap:10px;padding-top:14px")
    return phone(body, bottom='<div class="btn"%s>Замовити лате · 50 ₴</div>' % g(20))


def a21():
    fld = lambda l, v, grow=True: '<div class="col%s" style="gap:6px"><span class="lbl">%s</span><div class="fld">%s</div></div>' % (" grow" if grow else "", l, v)
    body = top("Адреса доставки", back=7) + content(
        '<div style="height:130px;border-radius:18px;background:var(--photo);display:flex;align-items:center;justify-content:center;gap:8px">%s<span class="t b">Тут буде карта</span></div>' % ic("map", 22, "var(--ink)"),
        fld("Вулиця й будинок", "вул. Борщагівська, [номер]", False),
        '<div class="row" style="gap:10px">' + fld("Квартира", "[номер]") + fld("Під'їзд", "2") + fld("Поверх", "7") + "</div>",
        fld("Коментар кур'єру", "Домофон не працює, наберіть", False),
        '<div class="row"><span class="t grow">Залишити біля дверей</span><div class="tog off"><i></i></div></div>',
        '<div class="tint2 row" style="padding:12px 14px">%s<span class="t">Доставка 49 ₴, 30–45 хв по Солом\'янці</span></div>' % ic("truck", 20, "var(--brand)"),
        style="gap:10px")
    return phone(body, bottom='<div class="btn"%s>Далі до оплати</div>' % g(22))


def a25():
    fld = lambda l, v: '<div class="col" style="gap:6px"><span class="lbl">%s</span><div class="fld">%s</div></div>' % (l, v)
    body = top("Оформлення картки", back=17) + content(
        '<div class="seg"><span%s>Сімейна</span><span class="on">Студентська</span><span%s>Індивідуальна</span></div>' % (g(17), g(38)),
        fld("Ім'я та прізвище", "Марко Петренко"), fld("Навчальний заклад", "КНЕУ"),
        '<div class="col" style="gap:6px"><span class="lbl">Студентський квиток</span><div class="card row" style="padding:12px">'
        '<div style="width:64px;height:44px;border-radius:8px;background:var(--tint2);display:flex;align-items:center;justify-content:center">%s</div>'
        '<div class="col grow"><span class="t b">kvytok.jpg</span><span class="xs">Фото завантажено</span></div><span class="s">Замінити</span></div></div>' % ic("card", 20, "var(--brand)"),
        '<span class="xs">Перевіримо квиток за 1 робочий день. До того картка працює як індивідуальна.</span>', style="gap:12px;padding-top:6px")
    return phone(body, bottom='<div class="btn"%s>Надіслати на перевірку</div>' % g(26))


def a26():
    body = ('<div style="padding:110px 24px 0;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center">'
            '<div class="ib" style="width:72px;height:72px;border-radius:36px;background:var(--tint);border:none">%s</div>'
            '<h1>Перевіряємо квиток</h1><p class="t" style="color:var(--soft)">Зазвичай до 1 робочого дня. Повідомимо, щойно студентська знижка запрацює.</p></div>' % ic("clock", 32, "var(--brand)") +
            content('<div class="card col" style="gap:8px"><div class="row"><span class="s grow">Статус</span><span class="chip" style="height:30px;font-size:12px">На перевірці</span></div>'
                    '<div class="row"><span class="s grow">Поки що</span><span class="t b">Індивідуальна картка</span></div></div>', style="padding-top:20px"))
    return phone(body, bottom='<div class="btn"%s>На головну</div>' % g(2))


def a27():
    perks = "".join('<div class="row" style="gap:10px">%s<span class="t">%s</span></div>' % (ic("check", 18, "var(--brand)"), t) for t in [
        "Ваші покупки підуть на спільний баланс", "Бонусами може платити будь-хто з родини", "Вийти з картки можна будь-коли"])
    body = ('<div style="background:var(--deep);color:var(--onbrand);padding:72px 24px 28px;display:flex;flex-direction:column;gap:10px">'
            '<span class="s" style="color:var(--onbrand);opacity:.8">Запрошення з SMS</span><h1>Олена запрошує вас до сімейної картки</h1>'
            '<span class="t" style="opacity:.85">Родина Коваленків · 4 учасники · 1 240 бонусів</span></div>' +
            content(perks, '<div class="col" style="gap:6px"><span class="lbl">Ваш номер</span><div class="fld">+380 50 *** ** 77</div></div>', style="gap:12px;padding-top:20px"))
    return phone(body, bottom='<div class="col" style="gap:10px"><div class="btn"%s>Приєднатися</div><span class="s" style="text-align:center"%s>Відхилити</span></div>' % (g(28), g(2)))


def a29():
    fld = lambda l, v: '<div class="col" style="gap:6px"><span class="lbl">%s</span><div class="fld">%s</div></div>' % (l, v)
    body = top("Додати учасника", back=13) + content(
        '<p class="t" style="color:var(--soft)">Надішлемо SMS із запрошенням. Людина приєднається, коли підтвердить.</p>',
        fld("Ім'я", "Марія"), fld("Номер телефону", "+380 63 *** ** 41"),
        '<span class="lbl">Хто це</span><div class="row" style="gap:8px"><span class="chip on">Дитина</span><span class="chip">Партнер</span><span class="chip">Батьки</span></div>',
        '<span class="xs">У сімейній картці до 5 учасників. Зараз 4.</span>', style="gap:12px")
    return phone(body, bottom='<div class="btn"%s>Надіслати запрошення</div>' % g(13))


def a30():
    rows = [("А-274", "Сьогодні, 18:30 · віконце", "Готуємо", True, 9), ("А-251", "18 жовтня · комірка 24/7", "Видано", False, None), ("А-233", "15 жовтня · кур'єр", "Видано", False, None)]
    cards = "".join('<div class="card col" style="gap:8px"%s><div class="row"><span class="t b grow">Замовлення %s</span><span class="chip%s" style="height:28px;font-size:12px">%s</span></div><span class="s">%s</span>%s</div>' % (
        g(go) if go else "", n, " on" if act else "", s, d, "" if act else '<div class="row"><span class="s grow">3 позиції · 342 ₴</span><span class="btn sm"%s>Повторити</span></div>' % g(6)) for n, d, s, act, go in rows)
    body = top("Мої замовлення", back=14) + content(cards, style="gap:10px")
    return phone(body, tab=None)


def a31():
    tg = lambda t, s, on: '<div class="row" style="padding:12px 0"><div class="col grow"><span class="t b">%s</span>%s</div><div class="tog%s"><i></i></div></div>' % (t, '<span class="xs">%s</span>' % s if s else "", "" if on else " off")
    body = top("Налаштування", back=14) + content(
        '<div class="card col" style="padding:2px 14px;gap:0"><span class="lbl" style="padding-top:12px">Сповіщення</span>' + tg("Статус замовлення", "Прийнято, готуємо, готово", True) + '<div class="div"></div>' + tg("Знижки й новинки кухні", "Не частіше разу на тиждень", False) + '<div class="div"></div>' + tg("SMS замість push", "", False) + "</div>",
        '<div class="card col" style="padding:2px 14px;gap:0"><span class="lbl" style="padding-top:12px">Зручність</span>' + tg("Простий режим", "Великий шрифт і менше кнопок", False) + '<div class="div"></div><div class="row" style="padding:12px 0"><span class="t b grow">Мова</span><span class="s">Українська</span></div></div>',
        '<span class="s" style="text-align:center;color:#B3261E;font-weight:600"%s>Вийти з акаунта</span>' % g(1), style="gap:12px")
    return phone(body)


def a35():
    body = top("Кошик", back=3) + ('<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:0 32px;text-align:center">'
                                   '<div class="ib" style="width:72px;height:72px;border-radius:36px;background:var(--tint2);border:none">%s</div><h2>Кошик порожній</h2>'
                                   '<p class="t" style="color:var(--soft)">Додайте страву з меню кухні або продукти з полиць.</p></div>') % ic("cart", 30, "var(--brand)")
    return phone(body, bottom='<div class="btn"%s>Перейти до меню</div>' % g(3))


def a37():
    body = ('<div style="padding:120px 24px 0;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center">'
            '<div class="ib" style="width:72px;height:72px;border-radius:36px;background:#F6DCD8;border:none">%s</div>'
            '<h1>Оплата не пройшла</h1><p class="t" style="color:var(--soft)">Банк відхилив платіж. Гроші не списано. Спробуйте іншу картку або оплатіть при отриманні.</p></div>') % ic("alert", 30, "#B3261E")
    return phone(body, bottom='<div class="col" style="gap:10px"><div class="btn"%s>Спробувати ще раз</div><div class="btn ghost"%s>Оплатити при отриманні</div></div>' % (g(8), g(34)))


SCREENS = [(1, a01), (19, a19), (21, a21), (25, a25), (26, a26), (27, a27), (29, a29), (30, a30), (31, a31), (35, a35), (37, a37)]

if __name__ == "__main__":
    for n, fn in SCREENS:
        open(os.path.join(OUT, "app-pulse-%02d.html" % n), "w").write(page("pulse", fn(), extra=CSS))
    json.dump([["app-pulse-%02d" % n, 390, 844] for n, _ in SCREENS], open(os.path.join(OUT, "j3.json"), "w"))
    print("ok")
