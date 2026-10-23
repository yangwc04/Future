import sys, importlib, os
os.makedirs("../out", exist_ok=True)
for m in sys.argv[1:]:
    mod = importlib.import_module(m)
    html = mod.build()
    open(f"../out/{m}.html", "w").write(html)
    print(m, len(html))
