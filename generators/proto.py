import os
import gen
from gen import plate, ic, qr, barcode, page, content, topbar, phone, dishcard, OUT

gen.TABS = [("home", "Головна"), ("book", "Меню"), ("card", "Картка"), ("user", "Профіль")]
tabbar = gen.tabbar
BRAND = "Пульс Солом'янки"


def greet(sub, title):
    return ('<div class="top"><div class="col" style="flex:1"><div class="sm soft">%s</div><div class="h1">%s</div></div>'
            '<div class="av" style="width:44px;height:44px;font-size:17px">О</div></div>') % (sub, title)


def marker(t):
    return '<span style="display:none">%s</span>' % t


def opt(icon, title, sub, on=False, right=""):
    return ('<div class="card row" style="%s"><div class="rad%s"></div><div class="circ" style="width:42px;height:42px">%s</div>'
            '<div class="col" style="flex:1"><div class="b">%s</div><div class="sm soft">%s</div></div>%s</div>') % (
        "border:2px solid var(--pri)" if on else "", " on" if on else "", ic(icon, 20, "var(--pri)"), title, sub, right)


def s01():
    body = content(
        '<div class="col" style="gap:6px;margin-top:20px"><div class="h1" style="font-size:34px;color:var(--pri)">%s</div><div class="xs soft">робоча назва</div></div>' % BRAND,
        '<div class="soft">Їжа від нашої кухні, продукти й фермерський холодильник поруч із домом.</div>',
        '<div class="h2" style="margin-top:8px">Оберіть картку</div>',
        opt("users", "Сімейна", "Один баланс бонусів на всю родину", True),
        opt("star", "Студентська", "Знижки на комбо за студентським квитком"),
        opt("user", "Індивідуальна", "Бонуси за кожну покупку"),
        '<div class="sp"></div>', '<div class="sm soft" style="text-align:center">Тип картки можна змінити в профілі</div>')
    return phone(body, bottom='<div class="bottom"><div class="btn">Продовжити</div></div>')


def s02():
    hero = ('<div class="hero" style="min-height:168px"><div class="eyebrow" style="opacity:.85">Кухня сьогодні</div><div class="h1" style="font-size:27px;max-width:200px">Обід і вечеря від нашої кухні</div>'
            '<div class="sp"></div><div class="btn acc s">Обрати страву</div><div style="position:absolute;right:-30px;bottom:-30px">%s</div></div>') % plate("chicken", 150)
    def q(i, t):
        return '<div class="card col" style="flex:1;gap:8px;padding:12px;align-items:flex-start"><div class="circ p" style="width:36px;height:36px">%s</div><div class="b sm" style="line-height:1.2">%s</div></div>' % (ic(i, 18), t)
    quick = '<div class="row" style="gap:10px;align-items:stretch">%s%s%s</div>' % (q("book", "Меню кухні"), q("cart", "Продукти"), q("leaf", "Холодильник 24/7"))
    menu = '<div class="row"><div class="h2">Популярне сьогодні</div></div><div class="hs">%s%s%s</div>' % (
        dishcard("chicken", "Курка з гречкою та овочами", 149), dishcard("salad", "Салат з печеним гарбузом", 119), dishcard("syrnyky", "Сирники зі сметаною", 99))
    order = '<div class="tintc row">%s<div class="col" style="flex:1"><div class="b">Замовлення А-274</div><div class="sm soft">Готуємо · буде о 18:30</div></div>%s</div>' % (plate("chicken", 44), ic("next", 18, "var(--soft)"))
    return phone(greet("Добрий вечір", "Олено, що сьогодні?") + content(hero, quick, menu, order), tab=0)


def s03():
    items = [("chicken", "Курка з гречкою та овочами", "320 г", 149), ("borsch", "Борщ з пампушками", "400 мл", 119), ("salad", "Салат з печеним гарбузом", "250 г", 119),
             ("pasta", "Паста з овочами", "300 г", 129), ("soup", "Крем-суп гарбузовий", "350 мл", 99), ("deruny", "Деруни зі сметаною", "280 г", 109)]
    rows = "".join(('<div class="card row" style="padding:10px"><div class="tile" style="width:68px;height:68px">%s</div><div class="col" style="flex:1"><div class="b">%s</div><div class="sm soft">%s</div></div>'
                    '<div class="col" style="align-items:flex-end;gap:6px"><div class="b">%d ₴</div><div class="circ p" style="width:30px;height:30px">%s</div></div></div>') % (plate(k, 58), n, w, p, ic("plus", 16)) for k, n, w, p in items)
    chips = '<div class="hs"><div class="chip">Сніданок</div><div class="chip on">Обід і вечеря</div><div class="chip">Комбо</div><div class="chip">Напої</div></div>'
    return phone(topbar("Меню кухні") + content(chips, '<div class="sm soft">Одне меню на день · готуємо на кухні магазину</div>', rows, style="gap:10px"), tab=1)


def s04():
    top = ('<div style="background:var(--tint);height:290px;flex:none;position:relative;display:flex;align-items:center;justify-content:center">%s'
           '<div class="circ" style="position:absolute;left:18px;top:36px">%s</div></div>') % (plate("chicken", 226), ic("back", 20))
    nut = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">%s</div>' % "".join(
        '<div class="tintc col" style="padding:8px 10px;align-items:center"><div class="b">%s</div><div class="xs soft">%s</div></div>' % (a, b) for a, b in [("410", "ккал"), ("34 г", "білки"), ("12 г", "жири"), ("38 г", "вуглев.")])
    body = content('<div class="badge" style="margin-top:16px">%s Овочі від локальних фермерів</div>' % ic("leaf", 14), '<div class="h1">Курка з гречкою та овочами</div>',
                   '<div class="row sm soft"><span>320 г</span><span>·</span><span>готуємо 15 хв</span></div>', '<div class="sm soft">Філе курки, гречка, броколі, морква.</div>', nut)
    bottom = '<div class="bottom"><div class="card row" style="padding:0 12px;height:54px;gap:14px">%s<span class="b">1</span>%s</div><div class="btn">Додати · 149 ₴</div></div>' % (ic("minus", 18), ic("plus", 18))
    return phone(top + body, bottom=bottom, safe=False)


def s05():
    cats = [("salad", "Овочі й фрукти"), ("cheese", "Молочне"), ("bread", "Хліб"), ("eggs", "Яйця"), ("coffee", "Кава й чай"), ("sandwich", "Снеки")]
    grid = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">%s</div>' % "".join(
        '<div class="card col" style="gap:8px;padding:10px"><div class="tile" style="height:86px">%s</div><div class="b sm">%s</div></div>' % (plate(k, 72), n) for k, n in cats)
    search = '<div class="card row" style="padding:12px 14px">%s<div class="soft" style="flex:1">Знайти продукт</div></div>' % ic("search", 18, "var(--soft)")
    farm = '<div class="tintc row">%s<div class="col" style="flex:1"><div class="b">Від локальних фермерів</div><div class="sm soft">Молоко, сир, овочі</div></div>%s</div>' % (ic("leaf", 22, "var(--pri)"), ic("next", 18, "var(--soft)"))
    return phone(topbar("Продукти") + content(search, farm, grid), tab=0)


def s06():
    def it(k, n, q, p):
        return '<div class="card row">%s<div class="col" style="flex:1"><div class="b">%s</div><div class="sm soft">%s</div></div><div class="b">%s ₴</div></div>' % (plate(k, 50), n, q, p)
    tot = '<div class="col" style="gap:6px"><div class="row"><div class="soft">Бонусів нарахуємо</div><div class="sp"></div><div class="b pri">+22</div></div><div class="row"><div class="h2">Разом</div><div class="sp"></div><div class="h1">431 ₴</div></div></div>'
    return phone(topbar("Кошик") + content(it("chicken", "Курка з гречкою", "2 порції · кухня", 298), it("salad", "Салат з печеним гарбузом", "1 порція · кухня", 119), it("bread", "Хліб житній", "400 г", 34),
                                           '<div class="sp"></div>', tot), bottom='<div class="bottom"><div class="btn">Оформити замовлення</div></div>')


def s07():
    slots = "".join('<div class="chip %s" style="justify-content:center;height:42px;font-size:15px">%s</div>' % (c, t) for t, c in [("17:30", ""), ("18:00", ""), ("18:30", "on"), ("19:00", ""), ("19:30", ""), ("20:00", "")])
    body = content('<div class="h2">Як отримати?</div>',
                   opt("pin", "Віконце видачі", "Без черги · безкоштовно", True),
                   opt("lock", "Комірка-холодильник", "Заберіть самі за кодом · безкоштовно") if "lock" in gen.ICONS else opt("bottle", "Комірка-холодильник", "Заберіть самі за кодом · безкоштовно"),
                   opt("bolt", "Кур'єр", "30–45 хв · від 49 ₴"),
                   '<div class="h2" style="margin-top:6px">Коли?</div>', '<div class="hs"><div class="chip on">Сьогодні</div><div class="chip">Завтра</div></div>',
                   '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">%s</div>' % slots)
    return phone(topbar("Отримання") + body, bottom='<div class="bottom"><div class="btn">Далі до оплати</div></div>')


def s08():
    body = content('<div class="h2">Спосіб оплати</div>',
                   opt("card", "Карткою зараз", "Apple Pay, Google Pay, картка", True),
                   opt("pin", "При отриманні", "Карткою або готівкою"),
                   '<div class="tintc row"><div class="col" style="flex:1"><div class="b">Списати бонуси</div><div class="sm soft">На сімейній картці 1 240</div></div>'
                   '<div style="width:46px;height:28px;border-radius:99px;background:var(--line);position:relative;flex:none"><div style="position:absolute;left:3px;top:3px;width:22px;height:22px;border-radius:50%;background:#fff"></div></div></div>',
                   '<div class="sp"></div>',
                   '<div class="card col" style="gap:8px"><div class="row sm"><span class="soft">Отримання</span><span class="sp"></span><span class="b">Віконце · 18:30</span></div>'
                   '<div class="row sm"><span class="soft">3 позиції</span><span class="sp"></span><span class="b">431 ₴</span></div></div>')
    return phone(topbar("Оплата") + body, bottom='<div class="bottom"><div class="btn">Оплатити 431 ₴</div></div>')


def s09():
    steps = [("Прийнято", "18:02", 2), ("Готуємо на кухні", "зараз", 1), ("Готово до видачі", "о 18:30", 0), ("Видано", "", 0)]
    rows = ""
    for i, (t, s, st) in enumerate(steps):
        dot = ('<div class="circ p" style="width:30px;height:30px">%s</div>' % ic("check", 16, w=3)) if st == 2 else (
            '<div style="width:30px;height:30px;border-radius:50%;border:3px solid var(--pri);background:var(--tint);flex:none"></div>' if st == 1 else '<div style="width:30px;height:30px;border-radius:50%;border:2px solid var(--line);flex:none"></div>')
        rows += '<div class="row" style="gap:14px"><div>%s</div><div class="col" style="flex:1"><div class="b%s">%s</div><div class="sm soft">%s</div></div></div>' % (dot, "" if st else " soft", t, s)
    head = '<div class="hero"><div class="eyebrow" style="opacity:.85">Замовлення А-274</div><div class="h1">Готуємо вашу вечерю</div><div class="sm" style="opacity:.9">Віконце видачі · о 18:30</div></div>'
    demo = '<div class="col" style="gap:8px"><div class="xs soft b">ПОКАЗАТИ ВАРІАНТ ВИДАЧІ</div><div class="row" style="gap:8px"><div class="chip">Віконце</div><div class="chip">Комірка</div><div class="chip">Кур\'єр</div></div></div>'
    return phone(topbar("Статус") + content(head, '<div class="card col" style="gap:16px;padding:18px">%s</div>' % rows, '<div class="sp"></div>', demo),
                 bottom='<div class="bottom"><div class="btn ghost">Змінити час</div></div>')


def ready(title, sub, codehint, extra, seed):
    top = ('<div style="background:var(--pri);color:var(--pri-ink);padding:44px 22px 26px;border-radius:0 0 28px 28px;display:flex;flex-direction:column;gap:8px;align-items:center;text-align:center;flex:none">'
           '<div style="width:56px;height:56px;border-radius:50%%;background:var(--acc);color:var(--acc-ink);display:flex;align-items:center;justify-content:center">%s</div>'
           '<div class="h1">%s</div><div class="sm" style="opacity:.9">%s</div></div>') % (ic("check", 30, w=3), title, sub)
    q = '<div class="card col" style="align-items:center;gap:10px;padding:18px">%s<div class="h1" style="letter-spacing:3px">А-274</div><div class="sm soft">%s</div></div>' % (qr(seed, 160), codehint)
    return phone(top + content(q, extra, style="padding-top:16px"), bottom='<div class="bottom"><div class="btn ghost">На головну</div></div>', safe=False)


def s10():
    return ready("Готово у віконці", "Чекаємо до 19:30", "Покажіть код у віконці видачі",
                 '<div class="tintc row">%s<div class="b" style="flex:1">+22 бонуси на сімейну картку</div></div>' % ic("gift", 20, "var(--pri)"), 11)


def s11():
    return ready("Комірка №14", "Готово · зберігаємо до 21:00", "Відскануйте код на дверцятах комірки",
                 '<div class="card row">%s<div class="col" style="flex:1"><div class="b">Холодильна комірка</div><div class="sm soft">Біля входу, ліворуч · працює 24/7</div></div></div>' % ic("pin", 22, "var(--pri)"), 14)


def s12():
    mp = ('<div style="height:250px;flex:none;background:#DCE5D2;position:relative;overflow:hidden">'
          '<svg width="390" height="250" viewBox="0 0 390 250" style="position:absolute;left:0;top:0"><path d="M0 70H390M0 170H390M90 0V250M250 0V250" stroke="#FFFDF8" stroke-width="14"/>'
          '<path d="M90 210V170H250V70H330" stroke="#2E6B45" stroke-width="5" fill="none" stroke-dasharray="2 10" stroke-linecap="round"/>'
          '<circle cx="90" cy="210" r="11" fill="#E2A12B"/><circle cx="330" cy="70" r="11" fill="#2E6B45"/></svg>'
          '<div class="circ" style="position:absolute;left:18px;top:36px">%s</div></div>') % ic("back", 20)
    body = content('<div class="h1" style="margin-top:16px">Кур\'єр уже їде</div>', '<div class="row sm soft">%s<span>Буде приблизно о 18:45</span></div>' % ic("clock", 15),
                   '<div class="card row"><div class="av">М</div><div class="col" style="flex:1"><div class="b">Максим</div><div class="sm soft">Кур\'єр магазину</div></div><div class="circ p">%s</div></div>' % ic("phone", 18),
                   '<div class="card col" style="gap:6px"><div class="sm soft">Адреса</div><div class="b">вул. Борщагівська, [номер], кв. [номер]</div></div>',
                   '<div class="tintc row sm b">%s<span>Код для кур\'єра: А-274</span></div>' % ic("lock" if "lock" in gen.ICONS else "card", 18, "var(--pri)"))
    return phone(mp + body, bottom='<div class="bottom"><div class="btn ghost">На головну</div></div>', safe=False)


def s13():
    card = ('<div class="hero" style="gap:12px"><div class="row"><div class="col" style="flex:1"><div class="eyebrow" style="opacity:.85">Сімейна картка</div><div class="h2">Родина Коваленків</div></div>%s</div>'
            '<div style="background:#fff;border-radius:12px;padding:12px 14px">%s</div><div class="sm" style="text-align:center;letter-spacing:2px;opacity:.9">2200 4417 0935</div></div>') % (ic("users", 26), barcode(286, 58))
    bal = '<div class="col"><div class="sm soft">Спільний баланс</div><div class="h1" style="font-size:32px">1 240 бонусів</div></div>'
    avs = '<div class="row" style="gap:8px">%s<div class="circ" style="width:36px;height:36px">%s</div><div class="sm soft" style="margin-left:6px">4 учасники</div></div>' % (
        "".join('<div class="av" style="%s">%s</div>' % (st, l) for l, st in [("О", ""), ("А", "background:var(--pri);color:var(--pri-ink)"), ("М", "background:var(--tint);color:var(--pri)"), ("Б", "")]), ic("plus", 16))
    types = '<div class="card col" style="gap:8px"><div class="sm soft">Інші типи карток</div><div class="row" style="gap:8px"><div class="chip">Студентська</div><div class="chip">Індивідуальна</div></div></div>'
    return phone(topbar("Картка") + content(card, bal, avs, types), tab=2)


def s14():
    def li(i, t, s=""):
        return '<div class="li"><div class="circ">%s</div><div class="col" style="flex:1"><div class="b">%s</div>%s</div>%s</div>' % (ic(i, 18, "var(--pri)"), t, '<div class="xs soft">%s</div>' % s if s else "", ic("next", 16, "var(--soft)"))
    head = '<div class="row" style="gap:14px"><div class="av" style="width:60px;height:60px;font-size:24px">О</div><div class="col"><div class="h2">Олена Коваленко</div><div class="sm soft">Сімейна картка</div></div></div>'
    rows = '<div class="card col" style="padding:2px 14px">%s%s%s%s%s</div>' % (li("list", "Мої замовлення", "Останнє: А-274"), li("pin", "Адреси доставки"), li("card", "Тип картки", "Сімейна"), li("alert", "Сповіщення"), li("check", "Простий режим", "Великий шрифт і менше кнопок"))
    return phone(topbar("Профіль") + content(head, rows), tab=3)


SCREENS = [("01 Вибір картки", s01), ("02 Головна", s02), ("03 Меню кухні", s03), ("04 Страва", s04), ("05 Продукти", s05), ("06 Кошик", s06), ("07 Отримання", s07),
           ("08 Оплата", s08), ("09 Статус", s09), ("10 Готово — віконце", s10), ("11 Готово — комірка", s11), ("12 Кур'єр", s12), ("13 Картка", s13), ("14 Профіль", s14)]

if __name__ == "__main__":
    import json
    body = "".join('<div class="scr" data-name="%s" style="display:inline-block;margin:20px;vertical-align:top">%s</div>' % (n, f()) for n, f in SCREENS)
    html = page("a", body, 430 * 7, 900 * 2)
    html = html.replace('<link rel="stylesheet" href="../node_modules', '<link rel="stylesheet" href="node_modules')
    open(os.path.join(OUT, "proto_all.html"), "w", encoding="utf-8").write(html)
    for n, f in SCREENS:
        open(os.path.join(OUT, "p-%s.html" % n[:2]), "w", encoding="utf-8").write(page("a", f(), 390, 844))
    json.dump([("p-%s" % n[:2], 390, 844) for n, _ in SCREENS], open(os.path.join(OUT, "pjobs.json"), "w"))
    print("ok", len(SCREENS))
