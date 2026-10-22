import json, os, re
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
T = json.load(open(os.path.join(OUT, "tree.json")))

def hx(c):
    if not c: return None
    s = "%02x%02x%02x" % tuple(round(c[k] * 255) for k in "rgb")
    if c.get("a", 1) < 0.999: s += "%02x" % round(c["a"] * 255)
    return s

def r(v): return round(v)

def svgmin(s):
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r">\s+<", "><", s)
    s = re.sub(r'\s*class="[^"]*"', "", s)
    s = re.sub(r"(\d+\.\d{2})\d+", r"\1", s)
    s = s.replace("rgb(255, 255, 255)", "#fff")
    s = re.sub(r"rgb\((\d+), (\d+), (\d+)\)", lambda m: "#%02x%02x%02x" % tuple(int(x) for x in m.groups()), s)
    s = s.replace('"', "'").replace(" >", ">").replace(" xmlns='http://www.w3.org/2000/svg'","")
    s = re.sub(r"<svg width='[\d.]+' height='[\d.]+'", "<svg", s, count=1)
    return s

def conv(n, px, py):
    t = n["t"]
    x, y = n["x"] - px, n["y"] - py
    if t == "svg":
        return ["s", r(x), r(y), r(n["w"]), r(n["h"]), svgmin(n["svg"])]
    if t == "x":
        fam = "L" if n["fam"].lower().startswith("lora") else "N"
        txt = n["txt"].upper() if n["up"] else n["txt"]
        o = ["t", r(x), r(y), r(n["w"]) + 1, r(n["h"]), txt, fam + str(n["wt"]), round(n["fs"], 1), round(n["lh"], 1), hx(n["col"]), n.get("lines", 1)]
        ex = {}
        if n["ls"]: ex["ls"] = round(n["ls"], 2)
        if n["strike"]: ex["st"] = 1
        if n["ta"] in ("center", "right"): ex["ta"] = n["ta"][0]
        if ex: o.append(ex)
        return o
    o = {"n": n["name"][:12], "b": [r(x), r(y), r(n["w"]), r(n["h"])]}
    if "fill" in n: o["f"] = hx(n["fill"])
    if "stroke" in n:
        o["s"] = [hx(n["stroke"]), n["sw"]] + ([1] if n.get("dash") else [])
    if "rad" in n:
        rd = [r(v) for v in n["rad"]]
        o["r"] = rd[0] if len(set(rd)) == 1 else rd
    if n.get("clip"): o["c"] = 1
    if "op" in n: o["o"] = n["op"]
    if "go" in n: o["g"] = n["go"]
    o["k"] = [conv(k, n["x"], n["y"]) for k in n["kids"]]
    if not o["k"]: del o["k"]
    return o

NAMES = {1: "01 Вибір картки", 2: "02 Головна", 3: "03 Меню кухні", 4: "04 Страва", 5: "05 Продукти", 6: "06 Кошик",
         7: "07 Отримання", 8: "08 Оплата", 9: "09 Статус замовлення", 10: "10 Готово у віконці", 11: "11 Комірка-холодильник",
         12: "12 Кур'єр", 13: "13 Картка лояльності", 14: "14 Профіль"}
tot = 0
for k, t in T.items():
    c = conv(t, t["x"], t["y"])
    s = json.dumps(c, ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(OUT, "c%02d.json" % int(k)), "w").write(s)
    tot += len(s)
    print(k, len(s))
print("total", tot)
