"""Оформлення картки: 4 екрани застосунку (15–18) і 4 сторінки сайту (110–113)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p2
from p2 import ic, phone, top, content, page, barcode, OUT, ready
import site2
from site2 import wrap, CSS2

APP_CSS = """
.fld{height:54px;border-radius:14px;border:1px solid var(--line);background:var(--surface);display:flex;align-items:center;padding:0 16px;font-size:16px;gap:10px}
.lbl{font-size:13px;color:var(--soft);font-weight:600}
.code{width:62px;height:68px;border-radius:16px;border:1px solid var(--line);background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700}
.code.on{border:2px solid var(--brand)}
.seg{display:flex;gap:6px;background:var(--tint2);border-radius:14px;padding:4px}
.seg span{flex:1;height:38px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:var(--soft)}
.seg span.on{background:var(--surface);color:var(--ink)}
.dash{border:1.5px dashed var(--line);border-radius:16px;padding:14px 16px;display:flex;align-items:center;gap:12px;color:var(--brand);font-weight:700;font-size:14px}
.chk{width:22px;height:22px;border-radius:7px;background:var(--brand);display:flex;align-items:center;justify-content:center;flex:none}
"""


def a15():
    body = top("Вхід", back=1) + content(
        '<h1>Вхід за номером телефону</h1>', '<p class="t" style="color:var(--soft)">Надішлемо SMS з кодом. Пароль не потрібен.</p>',
        '<div class="col" style="gap:6px;margin-top:8px"><span class="lbl">Номер телефону</span><div class="fld" style="border:2px solid var(--brand)"><span class="b">+380</span><span>67 123 45 12</span></div></div>',
        '<div class="row" style="gap:10px;align-items:flex-start;margin-top:4px"><div class="chk">%s</div><span class="s">Погоджуюсь з умовами програми лояльності й обробкою персональних даних</span></div>' % ic("check", 14, "var(--onbrand)", 3),
        style="gap:12px;padding-top:12px")
    return phone(body, bottom='<div class="btn" data-go="16">Отримати код</div>')


def a16():
    codes = '<div class="row" style="gap:10px;justify-content:center">' + "".join('<div class="code%s">%s</div>' % (" on" if i == 3 else "", d) for i, d in enumerate(["4", "8", "1", ""])) + "</div>"
    body = top("Код з SMS", back=15) + content(
        '<h1>Введіть код</h1>', '<p class="t" style="color:var(--soft)">Надіслали на +380 67 *** ** 12</p>', codes,
        '<span class="s" style="text-align:center">Надіслати ще раз через 0:42</span>', style="gap:14px;padding-top:12px")
    return phone(body, bottom='<div class="btn" data-go="17">Підтвердити</div>')


def a17():
    fld = lambda l, v: '<div class="col" style="gap:6px"><span class="lbl">%s</span><div class="fld">%s</div></div>' % (l, v)
    mem = ('<div class="card col" style="gap:10px;padding:12px 14px"><span class="lbl">Учасники родини</span>'
           '<div class="row"><div class="ib sm" style="background:var(--tint);border:none;font-weight:700;font-size:13px">А</div><div class="col grow"><span class="t b">Андрій</span><span class="xs">+380 50 *** ** 77</span></div><span class="xs">запрошено</span></div>'
           '<div class="dash">%sДодати учасника</div></div>') % ic("plus", 18, "var(--brand)")
    body = top("Оформлення картки", back=16) + content(
        '<div class="seg"><span class="on">Сімейна</span><span>Студентська</span><span>Індивідуальна</span></div>',
        fld("Ім'я", "Олена"), fld("Прізвище", "Коваленко"), fld("Дата народження", "12.04.1990"), mem,
        '<span class="xs">Для студентської картки попросимо фото студентського квитка</span>', style="gap:12px;padding-top:6px")
    return phone(body, bottom='<div class="btn" data-go="18">Оформити картку</div>')


def a18():
    card = ('<div class="dark col" style="gap:12px;padding:18px"><div class="row"><span class="t b grow">Сімейна картка</span><span class="s">Родина Коваленків</span></div>'
            '<div style="background:#FFFFFF;border-radius:12px;padding:12px 14px;display:flex;justify-content:center">%s</div>'
            '<span class="xs" style="text-align:center;letter-spacing:2px">2200 4417 0935</span></div>') % barcode(282, 54)
    extra = ('<div class="tint2 row" style="padding:12px 16px">%s<span class="t b">+100 вітальних бонусів</span></div>'
             '<div class="card row" style="padding:12px 16px">%s<span class="t">Запрошення надіслано Андрію</span></div>') % (ic("gift", 20, "var(--brand)"), ic("users", 20, "var(--brand)"))
    return ready("Картку оформлено", "Показуйте її на касі або в застосунку", card, extra)


def w110():
    body = ('<div class="main" style="align-items:center"><div class="box" style="width:520px;padding:40px;gap:18px">'
            '<h1 class="h-l" style="font-size:34px">Вхід або реєстрація</h1><p class="p">Надішлемо SMS з кодом. Пароль не потрібен.</p>'
            '<div class="col" style="gap:6px"><span class="s b">Номер телефону</span><span class="field" style="flex:none;border:2px solid var(--brand)"><b style="margin-right:8px">+380</b>67 123 45 12</span></div>'
            '<div class="row" style="gap:10px;align-items:flex-start"><span style="width:22px;height:22px;border-radius:7px;background:var(--brand);display:flex;align-items:center;justify-content:center;flex:none">%s</span><span class="s">Погоджуюсь з умовами програми лояльності й обробкою персональних даних</span></div>'
            '<span class="sbtn" style="justify-content:center"%s>Отримати код</span></div></div>') % (ic("check", 14, "var(--onbrand)", 3), ' data-go="111"')
    return wrap(body, None)


def w111():
    codes = '<div class="row" style="gap:12px">' + "".join('<span style="width:72px;height:80px;border-radius:16px;border:%s;background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:700">%s</span>' % (
        "2px solid var(--brand)" if i == 3 else "1px solid var(--line)", d) for i, d in enumerate(["4", "8", "1", ""])) + "</div>"
    body = ('<div class="main" style="align-items:center"><div class="box" style="width:520px;padding:40px;gap:18px"><span class="crumb" data-go="110">Змінити номер</span>'
            '<h1 class="h-l" style="font-size:34px">Введіть код</h1><p class="p">Надіслали на +380 67 *** ** 12</p>' + codes +
            '<span class="s">Надіслати ще раз через 0:42</span><span class="sbtn" style="justify-content:center" data-go="112">Підтвердити</span></div></div>')
    return wrap(body, None)


def w112():
    types = [("Сімейна", "Один рахунок на всю родину", True), ("Студентська", "За студентським квитком", False), ("Індивідуальна", "Для себе", False)]
    t = '<div class="row" style="gap:12px">' + "".join('<div class="opt%s"><div class="rad%s"></div><div class="col grow"><span class="t b">%s</span><span class="s">%s</span></div></div>' % (
        " on" if on else "", " on" if on else "", a, b, ) for a, b, on in types) + "</div>"
    f = lambda l, v: '<div class="col grow" style="gap:6px"><span class="s b">%s</span><span class="field" style="flex:none">%s</span></div>' % (l, v)
    left = ('<div class="col grow" style="gap:20px"><div class="box"><h3 class="h-m">Тип картки</h3>' + t + '</div>'
            '<div class="box"><h3 class="h-m">Особисті дані</h3><div class="row" style="gap:12px">' + f("Ім'я", "Олена") + f("Прізвище", "Коваленко") + '</div><div class="row" style="gap:12px">' + f("Дата народження", "12.04.1990") + f("E-mail, за бажанням", "olena@[пошта]") + '</div></div>'
            '<div class="box"><h3 class="h-m">Учасники родини</h3><div class="row"><span class="ib" style="background:var(--tint);border:none;font-weight:700">А</span><div class="col grow"><span class="t b">Андрій</span><span class="s">+380 50 *** ** 77</span></div><span class="chip" style="height:32px;font-size:13px">Запрошено</span></div>'
            '<div style="border:1.5px dashed var(--line);border-radius:16px;padding:14px 18px;display:flex;align-items:center;gap:10px;color:var(--brand);font-weight:700">%sДодати учасника за номером</div><span class="s">До 5 людей. Кожен отримає SMS із запрошенням.</span></div>'
            '<div class="box"><h3 class="h-m">Студентський квиток</h3><div style="border:1.5px dashed var(--line);border-radius:16px;padding:22px;display:flex;align-items:center;gap:12px">%s<div class="col"><span class="t b">Завантажте фото квитка</span><span class="s">Потрібно лише для студентської картки. Перевіримо за день.</span></div></div></div></div>') % (ic("plus", 18, "var(--brand)"), ic("card", 26, "var(--soft)"))
    right = ('<div class="col" style="width:380px;flex:none;gap:16px"><div style="background:var(--deep);color:var(--onbrand);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:12px">'
             '<span class="t b">Сімейна картка</span><div style="background:#FFFFFF;border-radius:14px;height:70px"></div><span class="s" style="color:var(--onbrand);opacity:.8">Номер картки з\'явиться після оформлення</span></div>'
             '<div class="box"><div class="li">%s<span>+100 вітальних бонусів</span></div><div class="li">%s<span>Бонуси всіх учасників на одному балансі</span></div><div class="li">%s<span>Картка працює на касі й у застосунку</span></div>'
             '<span class="sbtn" style="justify-content:center" data-go="113">Оформити картку</span></div></div>') % tuple(ic("check", 18, "var(--brand)") for _ in range(3))
    body = '<div class="main"><span class="crumb" data-go="108">Картки  /  Оформлення</span><h1 class="h-l">Оформлення картки</h1><div style="display:flex;gap:40px;align-items:flex-start">' + left + right + "</div></div>"
    return wrap(body, "cards")


def w113():
    body = ('<div class="main" style="align-items:center"><div class="box" style="width:640px;padding:40px;gap:18px;align-items:center;text-align:center">'
            '<div class="ib" style="width:64px;height:64px;border-radius:32px;background:var(--brand);border:none">%s</div><h1 class="h-l">Картку оформлено</h1>'
            '<p class="p">Показуйте штрихкод на касі або відкривайте картку в застосунку.</p>'
            '<div style="background:var(--deep);border-radius:24px;padding:22px;width:440px;display:flex;flex-direction:column;gap:12px"><div class="row"><span class="t b grow" style="color:var(--onbrand);text-align:left">Сімейна картка</span><span class="s" style="color:var(--onbrand);opacity:.8">Родина Коваленків</span></div>'
            '<div style="background:#FFFFFF;border-radius:14px;padding:14px;display:flex;justify-content:center">%s</div></div>'
            '<div class="row" style="gap:24px"><span class="t b" style="color:var(--brand)">+100 вітальних бонусів</span><span class="s">Запрошення надіслано Андрію</span></div>'
            '<div class="row" style="gap:12px"><span class="sbtn" data-go="109">До кабінету</span><span class="sbtn ghost" data-go="102">До меню кухні</span></div></div></div>') % (ic("check", 30, "var(--onbrand)", 3), barcode(282, 54))
    return wrap(body, "cards")


if __name__ == "__main__":
    for n, fn in [(15, a15), (16, a16), (17, a17), (18, a18)]:
        open(os.path.join(OUT, "app-pulse-%02d.html" % n), "w").write(page("pulse", fn(), extra=APP_CSS))
    for n, fn in [(110, w110), (111, w111), (112, w112), (113, w113)]:
        open(os.path.join(OUT, "web-%d.html" % n), "w").write(page("pulse", fn(), extra=CSS2).replace("body{background:#ddd", "body{background:var(--bg)"))
    json.dump([["app-pulse-%02d" % n, 390, 844] for n in (15, 16, 17, 18)], open(os.path.join(OUT, "jx.json"), "w"))
    print("ok")
