"""Тутешні: нова головна, «Подарунок з дому» (десктоп + мобільна), нова мобільна головна."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p2
p2.ICONS["plane"] = "<path d='M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z'/>"
import s3
from p2 import page, ic, img, OUT, qr
from s3 import CSS, S, go, box, field, opt, okicon, centered, DISHES, dcard, qrblock

S.update(gift=160, giftset=161, giftco=162, giftdone=163, giftzone=164, mgift=170, mgiftset=171, mgiftco=172, mgiftdone=173)
CSS = CSS + """
.logo{font-size:22px;font-weight:800;letter-spacing:1.5px;color:var(--brand)}
.board{background:var(--deep);color:var(--onbrand);border-radius:28px;padding:26px 28px;display:flex;flex-direction:column;gap:6px}
.board .r{display:flex;align-items:center;gap:16px;padding:12px 0;border-top:1px solid rgba(255,255,255,.14);font-size:16px}
.board .h{font-size:12px;letter-spacing:1.5px;opacity:.7;font-weight:700}
.gate{background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:22px;display:flex;flex-direction:column;gap:8px;flex:1}
.gate b.g{font-size:13px;letter-spacing:1.5px;color:var(--soft)}
.arch{background:var(--photo);border-radius:20px;display:flex;align-items:flex-end;padding:16px;font-size:14px;font-weight:600}
.card3{background:var(--surface);border:1px solid var(--line);border-radius:24px;overflow:hidden;display:flex;flex-direction:column}
.ta{border-radius:14px;border:1px solid var(--line);background:var(--surface);padding:14px 16px;font-size:15px;line-height:1.5;min-height:96px}
"""

LOGO = '<span class="logo" data-var="brand/name">ТУТЕШНІ</span>'


def header(active=None):
    links = [("home", "Головна"), ("menu", "Кухня"), ("coffee", "Кава"), ("shop", "Продукти"), ("cards", "Картки")]
    nav = "".join('<a class="%s"%s>%s</a>' % ("on" if k == active else "", "" if k == active else go(k), l) for k, l in links)
    gift = '<span class="sbtn%s" style="height:46px;font-size:15px;border-radius:14px;gap:8px"%s>%sПодарунок з дому</span>' % (
        "" if active == "gift" else " ghost", "" if active == "gift" else go("gift"), ic("plane", 18))
    return ('<div class="hdr"><span%s>%s</span>' % (go("home") if active != "home" else "", LOGO) + nav + '<div style="flex:1"></div>' + gift +
            '<div class="ib"%s>%s</div>' % (go("account"), ic("user", 20)) +
            '<div class="ib"%s>%s<span class="cnt">3</span></div>' % (go("cart"), ic("cart", 20)) +
            '<span class="sbtn" style="height:46px;font-size:15px;border-radius:14px"%s>Замовити онлайн</span></div>' % go("menu"))


def footer():
    return ('<div class="ftr"><div style="flex:1" class="col">%s<span class="s">Retail Hub «Солом\'янка», мережа «Гермес»</span></div>'
            '<div class="col" style="width:260px"><span class="b">Адреса</span><span class="s">вул. [адреса], Солом\'янка, Київ</span></div>'
            '<div class="col" style="width:220px"><span class="b">Години</span><span class="s">Щодня 7:30–22:00</span><span class="s">Комірка видачі 24/7</span></div>'
            '<div class="col" style="width:220px"><span class="b">Покупцям</span><a%s>Умови й документи</a><a%s>Подарунок з дому</a></div></div>') % (LOGO, go("legal"), go("gift"))


s3.header = header
s3.footer = footer
wrap = s3.wrap

BOARD = [("08:00", "Кава перед роботою", "Кава", "coffee"), ("12:30", "Обід без черги", "A", "menu"), ("18:00", "Вечеря за 20 хв", "A", "menu"), ("19:00", "Гості на порозі", "B", "shop")]
GATES = [("A", "Вечеря сьогодні", "Ready to Eat і Ready to Cook з нашої кухні", "menu"), ("B", "Звичні покупки", "Основні продукти на кожен день", "shop"),
         ("C", "Duty Free · Смаки світу", "Імпорт і гастротижні: цього місяця Italy Week", "shop"), ("D", "Місцеві на борту", "Продукція виробників Київщини", "shop"),
         ("E", "Швидка посадка", "Видача онлайн-замовлень і каси", "checkout")]
SETS = [("Мамі й татові", "Продуктовий набір для дому: молочне, хліб, овочі, фрукти, крупи", "850 ₴", "≈ €18", "z_fresh"),
        ("Обійми на відстані", "Солодощі, чай, кава, випічка й листівка від руки", "650 ₴", "≈ €14", "d_syrnyky"),
        ("Вечеря від мене", "Готові страви з нашої кухні або продукти для сімейної вечері", "780 ₴", "≈ €17", "d_borsch")]


def board(compact=False):
    rows = BOARD[:3] if compact else BOARD
    return ('<div class="board"><span class="h">ТАБЛО ТВОГО ДНЯ</span><div class="r" style="border:none;padding:4px 0 8px;font-size:12px;opacity:.7;font-weight:700;letter-spacing:1px"><span style="width:64px">ЧАС</span><span style="flex:1">МАРШРУТ</span><span>GATE</span></div>' +
            "".join('<div class="r"%s><span style="width:64px;font-weight:700">%s</span><span style="flex:1">%s</span><span class="b">%s</span></div>' % (go(g), t, r, gt) for t, r, gt, g in rows) + "</div>")


def p_home():
    hero = ('<div style="padding:56px 80px 0;display:flex;gap:56px;align-items:center"><div style="flex:1;display:flex;flex-direction:column;gap:20px">'
            '<span class="s b" style="letter-spacing:1.5px">ПРОДУКТОВИЙ МАГАЗИН · СОЛОМ\'ЯНКА</span>'
            '<h1 class="h-xl" style="max-width:640px">Дім ближче, ніж здається</h1>'
            '<p class="lead" style="max-width:600px">Поруч із тими, хто вдома, і з тими, хто далеко. Кава, готова їжа й продукти біля дому. А якщо ви за кордоном, передайте рідним подарунок з дому.</p>'
            '<div style="display:flex;gap:12px;margin-top:6px"><span class="sbtn"%s>Меню кухні</span><span class="sbtn ghost" style="gap:8px"%s>%sПодарунок з дому</span></div></div>'
            '<div style="width:520px">' % (go("menu"), go("gift"), ic("plane", 18)) + board() + '</div></div>'
            '<div style="padding:44px 80px 0">' + img("s_hero", 1280, 460, 28) + '</div>')
    gates = ('<div class="sec"><h2 class="h-l">Навігація магазину</h2><p class="p" style="margin-top:8px">Як в аеропорту: кожна зона має свій Gate.</p><div style="display:flex;gap:16px;margin-top:28px">' + "".join(
        '<div class="gate"%s><b class="g">GATE %s</b><h3 class="h-m" style="font-size:19px">%s</h3><p class="p" style="font-size:14px">%s</p></div>' % (go(g), l, t, d) for l, t, d, g in GATES) + "</div></div>")
    ks = ('<div class="sec"><div class="row" style="align-items:flex-end"><div class="col grow" style="gap:6px"><span class="s b" style="letter-spacing:1.5px">GATE A</span><h2 class="h-l">Сьогодні готує Солом\'янка</h2>'
          '<p class="p">Частину страв готуємо за родинними рецептами мешканців району.</p></div><span class="sbtn ghost"%s>Усе меню</span></div>'
          '<div style="display:flex;gap:24px;margin-top:32px">' % go("menu") + "".join(dcard(*d) for d in [DISHES[5], DISHES[1], DISHES[0], DISHES[3]]) + "</div></div>")
    gift = ('<div class="sec"><div style="background:var(--deep);color:var(--onbrand);border-radius:36px;padding:56px 64px;display:flex;gap:48px;align-items:center">'
            '<div class="col" style="gap:12px;width:420px;flex:none"><span class="s b" style="color:var(--onbrand);opacity:.7;letter-spacing:1.5px">GATE HOME</span><h2 class="h-l">Подарунок з дому</h2>'
            '<p class="lead" style="color:var(--onbrand);opacity:.8">Не можеш завітати? Передай турботу. Зберемо набір і привеземо рідним на Солом\'янці.</p>'
            '<span class="sbtn" style="background:var(--onbrand);color:var(--deep);align-self:flex-start;margin-top:8px"%s>Обрати набір</span></div>'
            '<div style="display:flex;gap:16px;flex:1">' % go("gift") + "".join(
                '<div class="col" style="gap:10px;flex:1"%s>%s<span class="t b" style="font-size:17px">%s</span><span class="s" style="color:var(--onbrand);opacity:.75">від %s</span></div>' % (go("giftset"), img(k, 230, 170, 18), n, p) for n, d, p, e, k in SETS) + "</div></div></div>")
    hist = ('<div class="sec" style="padding-bottom:96px"><div style="display:flex;gap:48px;align-items:center"><div class="col" style="gap:12px;width:420px;flex:none"><span class="s b" style="letter-spacing:1.5px">СОЛОМ\'ЯНКА В СЕРЦІ</span>'
            '<h2 class="h-l">Від залізниці до неба</h2><p class="p">Залізниця, інженери, авіація: історія району живе в інтер\'єрі магазину. Архівні фото й історії мешканців на стінах.</p></div>'
            '<div style="display:flex;gap:16px;flex:1">' + "".join('<div class="arch" style="flex:1;height:240px">Тут буде архівне фото: %s</div>' % t for t in ["залізниця", "авіація", "мешканці району"]) + "</div></div></div>")
    return wrap(hero + gates + ks + gift + hist, "home")


def setcard(n, d, p, e, k, w=392):
    return ('<div class="card3" style="width:%dpx"%s>%s<div style="padding:20px 22px 22px;display:flex;flex-direction:column;gap:10px"><h3 class="h-m">%s</h3><p class="p" style="font-size:15px">%s</p>'
            '<div class="row"><div class="col grow"><span class="price">від %s</span><span class="s">%s</span></div><span class="add"%s>Обрати</span></div></div></div>') % (w, go("giftset"), img(k, w, 220, 0), n, d, p, e, go("giftset"))


def p_gift():
    hero = ('<div class="main" style="gap:40px"><div style="display:flex;gap:48px;align-items:center"><div class="col grow" style="gap:16px"><span class="s b" style="letter-spacing:1.5px">GATE HOME · ДЛЯ ТИХ, ХТО ДАЛЕКО</span>'
            '<h1 class="h-xl" style="font-size:60px">Подарунок з дому</h1><p class="lead">Не можеш завітати? Передай турботу. Оберіть набір, адресу й дату, а ми зберемо його з наших полиць і привеземо рідним.</p>'
            '<div class="row" style="gap:12px;margin-top:6px"><span class="sbtn"%s>Обрати набір</span><span class="s">Оплата карткою будь-якої країни</span></div></div>' % go("giftset") +
            img("z_space", 520, 340, 28) + "</div>")
    sets = '<div class="col" style="gap:20px"><h2 class="h-l">Набори</h2><div style="display:flex;gap:24px">' + "".join(setcard(*s) for s in SETS) + "</div></div>"
    steps = [("Оберіть набір", "Три готові варіанти, можна додати квіти чи торт"), ("Вкажіть адресу й дату", "Доставляємо по Солом'янці й до 5 км від магазину"),
             ("Напишіть привітання", "Надрукуємо на листівці або напишемо від руки"), ("Отримайте фото вручення", "Кур'єр надішле фото, коли рідні отримають набір")]
    how = ('<div class="box" style="padding:40px;gap:24px"><h2 class="h-l" style="font-size:32px">Як це працює</h2><div style="display:flex;gap:28px">' + "".join(
        '<div class="col grow" style="gap:10px"><div class="ib" style="background:var(--tint2);border:none;font-weight:800;font-size:17px">%d</div><span class="t b">%s</span><span class="s">%s</span></div>' % (i + 1, t, d) for i, (t, d) in enumerate(steps)) + "</div></div>")
    zone = ('<div class="banner">%s<span class="grow">Зона доставки: Солом\'янка й 5 км навколо магазину. Якщо адреса далі, рідні можуть забрати набір у віконці Gate Home.</span></div>' % ic("pin", 20, "var(--brand)"))
    return wrap(hero + sets + how + zone + "</div>", "gift")


CONTENTS = ["Молоко 2,5%, 1 л", "Сир кисломолочний, 400 г", "Хліб житній", "Яйця, 10 шт", "Яблука, 1 кг", "Картопля, 2 кг", "Гречка, 1 кг", "Сезонні овочі"]


def p_giftset():
    li = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 24px">' + "".join('<div class="li">%s<span>%s</span></div>' % (ic("check", 18, "var(--brand)"), c) for c in CONTENTS) + "</div>"
    sizes = '<div class="row" style="gap:12px">' + opt("Малий", "650 ₴ · ≈ €14", False) + opt("Стандарт", "850 ₴ · ≈ €18", True) + opt("Великий", "1 200 ₴ · ≈ €26", False) + "</div>"
    extra = '<div class="chiprow"><span class="chip on">Листівка від руки</span><span class="chip">Квіти +350 ₴</span><span class="chip">Торт +420 ₴</span></div>'
    right = ('<div class="col grow" style="gap:18px"><span class="badge" style="display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 12px;border-radius:15px;background:var(--accent);font-size:13px;font-weight:700;align-self:flex-start">%sGate Home</span>'
             '<h1 class="h-l">Мамі й татові</h1><p class="t" style="max-width:560px">Продуктовий набір для дому. Збираємо з актуальних залишків, тож склад може трохи змінитися: замінюємо рівноцінним.</p>'
             '<span class="s b">У наборі</span>' % ic("plane", 14) + li + '<span class="s b" style="margin-top:6px">Розмір</span>' + sizes + '<span class="s b" style="margin-top:6px">Додати</span>' + extra +
             '<span class="sbtn" style="justify-content:center;margin-top:8px"%s>Далі: адреса й дата · 850 ₴</span></div>' % go("giftco"))
    body = ('<div class="main"><span class="crumb"%s>Подарунок з дому  /  Мамі й татові</span><div style="display:flex;gap:48px;align-items:flex-start">' % go("gift") +
            img("z_fresh", 560, 520, 28) + right + "</div></div>")
    return wrap(body, "gift")


def p_giftco():
    left = ('<div class="col grow" style="gap:20px">' +
            box("Кому", '<div class="row" style="gap:12px">' + field("Ім'я отримувача", "Галина Іванівна") + field("Телефон отримувача", "+380 67 *** ** 45") + "</div>") +
            box("Адреса", field("Вулиця й будинок", "вул. Ніжинська, [номер]") + '<div class="row" style="gap:12px">' + field("Квартира", "[номер]") + field("Коментар кур'єру", "Подзвоніть за 10 хв") + "</div>"
                '<div class="banner">%s<span>Адреса в зоні доставки · 2,1 км від магазину</span><span class="s" style="margin-left:auto"%s>Інша адреса?</span></div>' % (ic("check", 20, "var(--brand)"), go("giftzone"))) +
            box("Коли привезти", '<div class="chiprow"><span class="chip">Завтра</span><span class="chip on">Сб, 25 жовтня</span><span class="chip">Нд, 26 жовтня</span></div><div class="row" style="gap:10px">' +
                "".join('<span class="slot%s">%s</span>' % (" on" if t == "12:00–14:00" else "", t) for t in ["10:00–12:00", "12:00–14:00", "16:00–18:00", "18:00–20:00"]) + "</div>") +
            box("Привітання", '<div class="ta">Мамо, тату, обіймаю вас! Скоро приїду. Ваша Оля</div><div class="row"><div class="col grow"><span class="t b">Надіслати мені фото вручення</span><span class="s">Кур\'єр сфотографує набір у руках отримувача, якщо вони не проти</span></div><div class="tog"><i></i></div></div>') +
            box("Від кого", '<div class="row" style="gap:12px">' + field("Ваше ім'я", "Оля") + field("E-mail для чека й фото", "olya@[пошта]") + field("Країна", "Польща") + "</div>") + "</div>")
    summ = ('<div class="box" style="width:380px;flex:none"><h3 class="h-m">Подарунок</h3>%s<div class="row"><span class="t b grow">Мамі й татові</span><span class="b">850 ₴</span></div>'
            '<div class="row"><span class="s grow">Стандарт · листівка від руки</span><span class="b">0 ₴</span></div><div class="row"><span class="s grow">Доставка</span><span class="b">60 ₴</span></div><div class="div"></div>'
            '<div class="row"><span class="t b grow">Разом</span><div class="col" style="align-items:flex-end"><span class="price" style="font-size:24px">910 ₴</span><span class="s">≈ €20, курс вашого банку</span></div></div>'
            '<span class="sbtn" style="justify-content:center"%s>Оплатити 910 ₴</span><span class="s">Картка будь-якої країни, Apple Pay, Google Pay. Натискаючи, ви погоджуєтесь з <u%s>умовами</u></span></div>') % (
        img("z_fresh", 330, 150, 16), go("giftdone"), go("legal"))
    body = '<div class="main"><span class="crumb"%s>Подарунок з дому  /  Оформлення</span><h1 class="h-l">Оформлення подарунка</h1><div style="display:flex;gap:40px;align-items:flex-start">' % go("giftset") + left + summ + "</div></div>"
    return wrap(body, "gift")


def p_giftdone():
    steps = [("Прийнято", "сьогодні", "done"), ("Збираємо набір", "сб, 10:30", "now"), ("Кур'єр у дорозі", "сб, 12:00", ""), ("Вручено + фото", "", "")]
    tl = '<div class="tl" style="width:100%">' + "".join('<div class="st"><div class="dot %s">%s</div><span class="t b"%s>%s</span><span class="s">%s</span></div>' % (
        c, ic("check", 16, "var(--onbrand)") if c == "done" else "", "" if c else ' style="color:var(--soft)"', t, s) for t, s, c in steps) + "</div>"
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:18px;text-align:center">' + okicon() +
             '<h1 class="h-l">Подарунок прийнято</h1><p class="p" style="max-width:560px">Зберемо «Мамі й татові» і привеземо на вул. Ніжинську в суботу, 25 жовтня, 12:00–14:00. Фото вручення надішлемо на olya@[пошта].</p>' + tl +
             '<div class="ta" style="width:100%;text-align:left;min-height:0"><span class="s b">Листівка</span><br>Мамо, тату, обіймаю вас! Скоро приїду. Ваша Оля</div>'
             + '<div class="row" style="gap:12px"><span class="sbtn"%s>Надіслати ще один подарунок</span><span class="sbtn ghost"%s>На головну</span></div></div>' % (go("gift"), go("home")))
    return wrap(centered(inner, 760), "gift")


def p_giftzone():
    inner = ('<div style="display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center">' + okicon(True) +
             '<h1 class="h-l">Адреса поза зоною доставки</h1><p class="p">Доставляємо подарунки по Солом\'янці й до 5 км від магазину. Вкажіть іншу адресу або попросіть рідних забрати набір у віконці Gate Home.</p>'
             '<div class="row" style="gap:12px"><span class="sbtn"%s>Змінити адресу</span><span class="sbtn ghost"%s>Заберуть у магазині</span></div></div>') % (go("giftco"), go("giftco"))
    return wrap(centered(inner, 640), "gift")


# ---------- мобільна ----------
def mwrap(body):
    hdr = ('<div class="mh"><div class="ib"%s>%s</div><div style="flex:1;display:flex;justify-content:center"><span%s>%s</span></div><div class="ib"%s>%s<span class="cnt">3</span></div></div>' % (
        go(151), ic("list", 20), go(150), LOGO.replace("22px", "18px"), go(153), ic("cart", 20)))
    ftr = ('<div class="mf">%s<span class="s">вул. [адреса], Солом\'янка · щодня 7:30–22:00 · комірка 24/7</span></div>' % LOGO)
    return '<div class="msite">' + hdr + body + ftr + "</div>"


def m_home():
    zones = [("z_kitchen", "Gate A · Вечеря сьогодні", 152), ("z_coffee", "Кава з собою", 152), ("z_fresh", "Gate B · Звичні покупки", 152), ("z_locker", "Комірка 24/7", 153)]
    zs = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' + "".join('<div class="col" style="gap:8px"%s>%s<span class="t b">%s</span></div>' % (go(g), img(k, 169, 120, 16), t) for k, t, g in zones) + "</div>"
    body = ('<div class="mm"><span class="s b" style="letter-spacing:1.5px">ПРОДУКТОВИЙ МАГАЗИН · СОЛОМ\'ЯНКА</span><h1 class="h-l" style="font-size:34px">Дім ближче, ніж здається</h1>'
            '<p class="p">Поруч із тими, хто вдома, і з тими, хто далеко.</p>'
            '<span class="sbtn" style="justify-content:center"%s>Меню кухні</span><span class="sbtn ghost" style="justify-content:center;gap:8px"%s>%sПодарунок з дому</span>' % (go(152), go(170), ic("plane", 18)) +
            board(True) + '<h2 class="h-m" style="font-size:24px">Що є в магазині</h2>' + zs +
            '<div style="background:var(--deep);color:var(--onbrand);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:12px"><span class="s b" style="color:var(--onbrand);opacity:.7;letter-spacing:1.5px">GATE HOME</span><h2 class="h-m" style="font-size:24px">Подарунок з дому</h2>'
            '<p class="p" style="color:var(--onbrand);opacity:.8">Не можеш завітати? Передай турботу рідним на Солом\'янці.</p>'
            '<span class="sbtn" style="justify-content:center;background:var(--onbrand);color:var(--deep)"%s>Обрати набір</span></div></div>') % go(170)
    return mwrap(body)


def m_gift():
    cards = "".join('<div class="card3" style="width:350px"%s>%s<div style="padding:16px;display:flex;flex-direction:column;gap:8px"><span class="t b" style="font-size:17px">%s</span><span class="s">%s</span>'
                    '<div class="row"><span class="price grow">від %s</span><span class="add"%s>Обрати</span></div></div></div>' % (go(171), img(k, 350, 170, 0), n, d, p, go(171)) for n, d, p, e, k in SETS)
    body = ('<div class="mm"><span class="s b" style="letter-spacing:1.5px">GATE HOME</span><h1 class="h-l" style="font-size:32px">Подарунок з дому</h1><p class="p">Не можеш завітати? Передай турботу. Привеземо набір рідним на Солом\'янці.</p>' + cards +
            '<div class="banner" style="font-size:14px">%s<span>Доставка по Солом\'янці й до 5 км. Оплата карткою будь-якої країни.</span></div></div>' % ic("pin", 20, "var(--brand)"))
    return mwrap(body)


def m_giftset():
    li = "".join('<div class="li">%s<span>%s</span></div>' % (ic("check", 18, "var(--brand)"), c) for c in CONTENTS[:6])
    sizes = "".join('<div class="opt%s" style="flex:none"><div class="rad%s"></div><span class="t b grow">%s</span><span class="s">%s</span></div>' % (" on" if on else "", " on" if on else "", a, b) for a, b, on in [("Малий", "650 ₴", False), ("Стандарт", "850 ₴", True), ("Великий", "1 200 ₴", False)])
    body = ('<div class="mm">' + img("z_fresh", 350, 220, 20) + '<h1 class="h-l" style="font-size:30px">Мамі й татові</h1><p class="p">Продуктовий набір для дому. Збираємо з актуальних залишків.</p>' + li +
            '<span class="s b">Розмір</span>' + sizes + '<span class="sbtn" style="justify-content:center"%s>Далі: адреса й дата</span></div>' % go(172))
    return mwrap(body)


def m_giftco():
    f = lambda l, v: '<div class="col" style="gap:6px"><span class="s b">%s</span><span class="field" style="flex:none">%s</span></div>' % (l, v)
    body = ('<div class="mm"><h1 class="h-l" style="font-size:30px">Оформлення подарунка</h1>' + f("Кому", "Галина Іванівна, +380 67 *** ** 45") + f("Адреса", "вул. Ніжинська, [номер], кв. [номер]") +
            '<div class="banner" style="font-size:14px">%s<span>У зоні доставки · 2,1 км</span></div>' % ic("check", 18, "var(--brand)") +
            '<span class="s b">Коли</span><div class="row" style="gap:8px"><span class="chip">Завтра</span><span class="chip on">Сб, 25 жовтня</span></div>'
            '<div class="row" style="gap:8px"><span class="slot">10:00–12:00</span><span class="slot on">12:00–14:00</span></div>'
            '<span class="s b">Привітання</span><div class="ta">Мамо, тату, обіймаю вас! Скоро приїду. Ваша Оля</div>' + f("Ваш e-mail", "olya@[пошта]") +
            '<div class="row"><span class="t b grow">Разом</span><div class="col" style="align-items:flex-end"><span class="price" style="font-size:24px">910 ₴</span><span class="s">≈ €20</span></div></div>'
            '<span class="sbtn" style="justify-content:center"%s>Оплатити 910 ₴</span></div>') % go(173)
    return mwrap(body)


def m_giftdone():
    body = ('<div class="mm" style="align-items:center;text-align:center">' + okicon() + '<h1 class="h-l" style="font-size:30px">Подарунок прийнято</h1>'
            '<p class="p">Привеземо «Мамі й татові» в суботу, 25 жовтня, 12:00–14:00. Фото вручення надішлемо на e-mail.</p>'
            '<div class="ta" style="text-align:left;min-height:0;align-self:stretch"><span class="s b">Листівка</span><br>Мамо, тату, обіймаю вас! Скоро приїду. Ваша Оля</div>'
            '<span class="sbtn" style="justify-content:center;align-self:stretch"%s>Надіслати ще один</span><span class="sbtn ghost" style="justify-content:center;align-self:stretch"%s>На головну</span></div>') % (go(170), go(150))
    return mwrap(body)


NAMES = {101: "С1 Головна", 150: "М1 Головна", 160: "Г1 Подарунок з дому", 161: "Г2 Набір «Мамі й татові»", 162: "Г3 Оформлення подарунка", 163: "Г4 Подарунок прийнято",
         164: "Г5 Адреса поза зоною", 170: "МГ1 Подарунок з дому", 171: "МГ2 Набір", 172: "МГ3 Оформлення подарунка", 173: "МГ4 Подарунок прийнято"}
PAGES = {101: p_home, 160: p_gift, 161: p_giftset, 162: p_giftco, 163: p_giftdone, 164: p_giftzone, 150: m_home, 170: m_gift, 171: m_giftset, 172: m_giftco, 173: m_giftdone}

if __name__ == "__main__":
    jobs = []
    for n, fn in PAGES.items():
        h = page("pulse", fn(), extra=CSS).replace("body{background:#ddd", "body{background:var(--bg)")
        open(os.path.join(OUT, "w4-%d.html" % n), "w").write(h)
        sel, w = (".msite", 390) if n == 150 or n >= 170 else (".site", 1440)
        jobs.append(["web%d" % n, "w4-%d.html" % n, sel, w, 900])
    json.dump(jobs, open(os.path.join(OUT, "xw4.json"), "w"))
    json.dump(NAMES, open(os.path.join(OUT, "wnames4.json"), "w"), ensure_ascii=False)
    print(len(PAGES))
