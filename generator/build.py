import sys, importlib, os
import lib
os.makedirs("../out", exist_ok=True)
L = dict(l.split() for l in open("../links.txt") if l.strip())
# generator module -> key used for its "<key>-etf" link in links.txt
KEY = {"p01_index": "equity", "p03a_eur": "eur", "p03b_jpy": "jpy", "p03c_gbp": "gbp", "p03d_aud": "aud", "p03e_cad": "cad",
       "p03f_chf": "chf", "p03g_dx": "dx"}
for m in sys.argv[1:]:
    k = KEY.get(m, m.split("_", 1)[1] if "_" in m else m)
    lib.ETF_LINK = L.get(k + "-etf")
    mod = importlib.import_module(m)
    html = mod.build()
    open(f"../out/{m}.html", "w").write(html)
    print(m, len(html), "etf:", bool(lib.ETF_LINK))
