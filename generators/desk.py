import os, json
from gen import plate, ic, barcode, bottle, page, OUT

DCSS = """
.d{width:1440px;height:1100px;overflow:hidden;background:var(--bg);display:flex;flex-direction:column;font-size:17px}
.nav{height:84px;flex:none;display:flex;align-items:center;gap:36px;padding:0 64px;background:var(--card);border-bottom:1px solid var(--line)}
.wm{font-family:var(--head),serif;font-weight:700;font-size:30px;color:var(--pri)}
.nav a{font-weight:700;font-size:16px}
.pill{display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 16px;border-radius:99px;background:var(--tint);color:var(--pri);font-weight:800;font-size:14px;white-space:nowrap}
.D1{font-family:var(--head),serif;font-weight:var(--hw);font-size:78px;line-height:1.02;letter-spacing:var(--ls)}
.D2{font-family:var(--head),serif;font-weight:var(--hw);font-size:32px;line-height:1.15}
.D3{font-family:var(--head),serif;font-weight:var(--hw);font-size:22px;line-height:1.2}
.wrap{padding:0 64px}
.btn.l{flex:none;height:60px;font-size:18px;padding:0 30px}
.search{flex:1;height:50px;border-radius:99px;background:var(--bg);border:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:0 20px;color:var(--soft)}
.side{width:250px;flex:none;display:flex;flex-direction:column;gap:6px}
.side div{height:44px;display:flex;align-items:center;gap:10px;padding:0 14px;border-radius:12px;font-weight:700;font-size:15px}
.side .on{background:var(--pri);color:var(--pri-ink)}
"""


def dcard(kind, name, meta, price, w=""):
    return ('<div class="card col" style="padding:12px;gap:10px;%s"><div class="tile" style="height:150px">%s</div><div class="col" style="padding:0 4px;gap:2px"><div class="b" style="font-size:17px">%s</div><div class="sm soft">%s</div></div>'
            '<div class="row" style="padding:0 4px 4px"><div class="D3">%s ₴</div><div class="sp"></div><div class="circ p">%s</div></div></div>') % (w, plate(kind, 124), name, meta, price, ic("plus", 20))


def nav(search=False):
    mid = '<div class="search">%s<span>Знайти страву, продукт або рецепт</span></div>' % ic("search", 18) if search else '<a>Меню дня</a><a>Каталог</a><a>Рецепти</a><a>Сусіди</a><a>Фермери</a><div class="sp"></div>'
    return ('<div class="nav"><div class="wm">Солом\'янка</div>%s<div class="pill"><span class="dot"></span>Працюємо до 22:00</div>'
            '<div class="btn s" style="align-self:center;height:46px">%s Кошик · 2</div></div>') % (mid, ic("cart", 18))


def site_a():
    slots = "".join('<div class="chip %s" style="height:46px;font-size:16px;padding:0 20px">%s</div>' % (c, t) for t, c in [("17:30", ""), ("18:00", ""), ("18:30", "on"), ("19:00", ""), ("19:30", "")])
    hero = ('<div class="wrap row" style="height:500px;flex:none;gap:40px"><div class="col" style="flex:1;gap:20px"><div class="badge" style="height:32px;font-size:14px">%s Готова їжа біля дому</div>'
            '<div class="D1">Вечеря<br>за 5 хвилин</div><div class="soft" style="font-size:21px;max-width:520px">Замовте дорогою додому — заберіть у віконці видачі без черги.</div>'
            '<div class="col" style="gap:10px"><div class="b sm soft">Забрати сьогодні о:</div><div class="row" style="gap:10px">%s</div></div>'
            '<div class="row" style="gap:14px"><div class="btn l">Обрати вечерю</div><div class="btn l ghost">Як це працює</div></div></div>'
            '<div style="width:520px;height:460px;position:relative;flex:none"><div style="position:absolute;left:40px;top:10px;width:440px;height:440px;border-radius:50%%;background:var(--tint)"></div>'
            '<div style="position:absolute;left:70px;top:40px">%s</div>'
            '<div class="card row" style="position:absolute;left:0;bottom:30px;box-shadow:0 12px 30px rgba(28,43,34,.14)"><div class="col"><div class="b">Курка з гречкою</div><div class="sm soft">320 г · 149 ₴</div></div><div class="circ p">%s</div></div>'
            '<div class="pill" style="position:absolute;right:0;top:50px;background:var(--acc);color:var(--acc-ink)">%s Готова до 18:30</div></div></div>') % (ic("leaf", 16), slots, plate("chicken", 380), ic("plus", 20), ic("clock", 16))
    menu = '<div class="wrap col" style="gap:18px"><div class="row"><div class="D2">Меню дня</div><div class="sp"></div><div class="b pri">Усе меню →</div></div><div style="display:grid;grid-template-columns:repeat(5,1fr);gap:18px">%s%s%s%s%s</div></div>' % (
        dcard("chicken", "Курка з гречкою", "320 г · готова страва", 149), dcard("borsch", "Борщ з пампушками", "400 мл · готова страва", 119), dcard("syrnyky", "Сирники зі сметаною", "250 г · сніданок", 99),
        dcard("salad", "Салат з овочами", "220 г · хелсі", 89), dcard("deruny", "Деруни", "Рецепт від Галини", 109))
    tiles = ('<div class="wrap" style="display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:24px">'
             '<div class="tintc row" style="padding:20px">%s<div class="col"><div class="D3">Рецепти сусідів</div><div class="sm soft">Готуйте те, що люблять поруч</div></div></div>'
             '<div class="tintc row" style="padding:20px">%s<div class="col"><div class="D3">Голосування тижня</div><div class="sm soft">Наступну страву обираєте ви</div></div></div>'
             '<div class="tintc row" style="padding:20px">%s<div class="col"><div class="D3">Сімейна картка</div><div class="sm soft">Один баланс бонусів на родину</div></div></div></div>') % (
        plate("deruny", 60), plate("holubtsi", 60), '<div class="circ p" style="width:60px;height:60px">%s</div>' % ic("users", 28))
    return '<div class="d">%s<div style="height:28px;flex:none"></div>%s%s%s</div>' % (nav(), hero, menu, tiles)


def site_b():
    cats = [("Готові страви", 1), ("Комбо", 0), ("Овочі та фрукти", 0), ("Молочне та яйця", 0), ("М'ясо та риба", 0), ("Хліб і випічка", 0), ("Напої", 0), ("Дитячі товари", 0), ("Для дому", 0)]
    side = '<div class="side"><div class="D3" style="height:auto;padding:0 14px 8px">Каталог</div>%s<div style="height:16px"></div><div class="tintc" style="height:auto;padding:12px 14px;border-radius:12px">%s Лише від фермерів</div><div class="tintc" style="height:auto;padding:12px 14px;border-radius:12px">%s Хелсі</div></div>' % (
        "".join('<div class="%s">%s</div>' % ("on" if o else "", n) for n, o in cats), ic("leaf", 18, "var(--pri)"), ic("heart", 18, "var(--pri)"))
    grid = '<div class="col" style="flex:1;gap:16px"><div class="row"><div class="D2">Готові страви</div><div class="sp"></div><div class="chip on">Популярні</div><div class="chip">Дешевші</div><div class="chip">Є сьогодні</div></div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">%s</div></div>' % "".join([
        dcard("chicken", "Курка з гречкою", "320 г · від фермера", 149), dcard("borsch", "Борщ з пампушками", "400 мл", 119), dcard("holubtsi", "Голубці", "300 г · вибір мешканців", 139),
        dcard("pasta", "Паста з овочами", "300 г", 129), dcard("soup", "Гарбузовий суп", "350 мл · хелсі", 99), dcard("syrnyky", "Сирники зі сметаною", "250 г", 99), dcard("salad", "Салат з овочами", "220 г · хелсі", 89), dcard("deruny", "Деруни", "Рецепт від Галини", 109), dcard("sandwich", "Сендвіч з куркою", "180 г · комбо", 69)])
    def it(k, n, q, p):
        return '<div class="row">%s<div class="col" style="flex:1"><div class="b" style="font-size:15px">%s</div><div class="sm soft">%s</div></div><div class="b">%s ₴</div></div>' % (plate(k, 46), n, q, p)
    cart = ('<div class="card col" style="width:330px;flex:none;gap:16px;padding:20px;align-self:flex-start"><div class="D3">Ваше замовлення</div>%s%s%s<div style="height:1px;background:var(--line)"></div>'
            '<div class="tintc row" style="padding:12px">%s<div class="col" style="flex:1"><div class="b" style="font-size:15px">Віконце видачі</div><div class="sm soft">Сьогодні, 18:30</div></div><div class="sm b pri">Змінити</div></div>'
            '<div class="row"><div class="soft">Бонусів нарахуємо</div><div class="sp"></div><div class="b pri">+20</div></div><div class="row"><div class="D3">Разом</div><div class="sp"></div><div class="D2">401 ₴</div></div>'
            '<div class="btn" style="flex:none">Оформити замовлення</div></div>') % (it("chicken", "Курка з гречкою", "2 порції", 298), it("bread", "Хліб житній", "400 г", 34), it("coffee", "Капучино", "1 шт", 69), ic("pin", 22, "var(--pri)"))
    return '<div class="d">%s<div class="wrap row" style="align-items:flex-start;gap:28px;padding-top:32px">%s%s%s</div></div>' % (nav(True), side, grid, cart)


def admin():
    items = [("cart", "Замовлення", 1), ("book", "Меню дня", 0), ("list", "Товари й ціни", 0), ("star", "Рецепти", 0), ("thumb", "Голосування", 0), ("alert", "Сповіщення", 0), ("bolt", "Статус магазину", 0)]
    side = '<div style="width:270px;flex:none;background:#1C2B22;color:#F4F1E8;padding:28px 18px;display:flex;flex-direction:column;gap:6px"><div class="wm" style="color:#F4F1E8;padding:0 12px 4px">Солом\'янка</div><div class="sm" style="opacity:.6;padding:0 12px 18px">Панель магазину</div>%s<div class="sp"></div><div class="row" style="padding:12px"><div class="av">І</div><div class="col"><div class="b sm">Ірина, зміна Б</div><div class="xs" style="opacity:.6">адміністратор</div></div></div></div>' % "".join(
        '<div class="row" style="height:48px;padding:0 14px;border-radius:12px;font-weight:700;font-size:15px;%s">%s%s</div>' % ("background:#2E6B45" if o else "opacity:.8", ic(i, 20), n) for i, n, o in items)
    def st(a, b):
        return '<div class="card col" style="flex:1;padding:16px 20px"><div class="D2">%s</div><div class="sm soft">%s</div></div>' % (a, b)
    stats = '<div class="row" style="gap:16px">%s%s%s%s</div>' % (st("34", "замовлення сьогодні"), st("9", "на слот 18:30"), st("6 хв", "середній час збирання"), '<div class="card row" style="flex:1;padding:16px 20px"><div class="col" style="flex:1"><div class="b">Магазин працює</div><div class="sm soft">Видача відкрита</div></div><div style="width:52px;height:30px;border-radius:99px;background:var(--pri);position:relative;flex:none"><div style="position:absolute;right:3px;top:3px;width:24px;height:24px;border-radius:50%;background:#fff"></div></div></div>')
    def oc(code, slot, what, who, act, k, hot=0):
        return ('<div class="card col" style="gap:10px;%s"><div class="row"><div class="D3">%s</div><div class="sp"></div><div class="badge" style="align-self:center;%s">%s %s</div></div>'
                '<div class="row">%s<div class="col" style="flex:1"><div class="b" style="font-size:15px">%s</div><div class="sm soft">%s</div></div></div>%s</div>') % (
            "border:2px solid var(--acc)" if hot else "", code, "background:var(--acc);color:var(--acc-ink)" if hot else "", ic("clock", 13), slot, plate(k, 44), what, who,
            '<div class="btn %s" style="flex:none;height:42px;font-size:14px">%s</div>' % ("" if act[0] != "-" else "ghost", act.lstrip("-")) if act else "")
    def colm(t, n, cards, tint=0):
        return '<div class="col" style="flex:1;gap:12px;%s"><div class="row"><div class="D3">%s</div><div class="chip" style="height:26px;padding:0 10px">%d</div></div>%s</div>' % ("", t, n, "".join(cards))
    board = '<div class="row" style="align-items:flex-start;gap:18px">%s%s%s%s</div>' % (
        colm("Нові", 3, [oc("А-281", "19:00", "Борщ × 2, хліб", "Андрій · віконце", "Почати збирати", "borsch"), oc("А-280", "19:00", "Набір для борщу, 7 товарів", "Марія · доставка", "Почати збирати", "salad"), oc("А-279", "18:30", "Комбо «Обід студента»", "Богдан · полиця", "Почати збирати", "soup")]),
        colm("Збираємо", 2, [oc("А-276", "18:30", "Сирники × 3, молоко", "Родина Коваленків", "Готово", "syrnyky", 1), oc("А-275", "18:30", "Паста, салат", "Катерина · віконце", "Готово", "pasta", 1)]),
        colm("Готові до видачі", 3, [oc("А-274", "18:30", "Курка з гречкою × 2", "Олена · віконце", "-Видати за кодом", "chicken"), oc("А-272", "18:00", "Голубці, узвар", "Тарас · віконце", "-Видати за кодом", "holubtsi"), oc("А-271", "18:00", "Кава + випічка", "Ілля · полиця", "-Видати за кодом", "coffee")]),
        colm("Видано", 22, [oc("А-270", "17:30", "Деруни × 2", "Галина · віконце", "", "deruny"), oc("А-269", "17:30", "Курка з гречкою", "Юлія · доставка", "", "chicken")]))
    head = '<div class="row"><div class="D2">Замовлення на сьогодні</div><div class="sp"></div><div class="chip on">Усі слоти</div><div class="chip">17:30</div><div class="chip">18:00</div><div class="chip">18:30</div><div class="chip">19:00</div></div>'
    return '<div class="d" style="flex-direction:row">%s<div class="col" style="flex:1;padding:28px 32px;gap:20px">%s%s%s</div></div>' % (side, head, stats, board)


jobs = [("d-site-a", page("a", site_a(), 1440, 1100, DCSS), 1440, 1100), ("d-site-b", page("a", site_b(), 1440, 1100, DCSS), 1440, 1100), ("d-admin", page("a", admin(), 1440, 860, DCSS + ".d{height:860px}"), 1440, 860)]
for n, html, w, h in jobs:
    open(os.path.join(OUT, n + ".html"), "w", encoding="utf-8").write(html)
json.dump([(n, w, h) for n, _, w, h in jobs], open(os.path.join(OUT, "djobs.json"), "w"))
print("desk ok")
