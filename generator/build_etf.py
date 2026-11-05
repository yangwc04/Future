# Build every "관련 ETF" page into ../out/etf_<key>.html
import os, sys
from etflib import build_etf
from etf_markets import markets
os.makedirs("../out", exist_ok=True)
only = set(sys.argv[1:])
for m in markets():
    if only and m["key"] not in only: continue
    h = build_etf(m)
    open(f"../out/etf_{m['key']}.html", "w").write(h)
    print(m["key"], len(h))
