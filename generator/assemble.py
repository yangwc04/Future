import os, re, glob, shutil
os.makedirs("docs", exist_ok=True)
L = dict(l.split() for l in open("links.txt"))
L.update(oj="https://claude.ai/artifact/Ceb2BiwFY7LJci991bjsij", coffee="https://claude.ai/artifact/1AmSgYykjSvYAj6gme8tMU",
         rice="https://claude.ai/artifact/9teMajEtW3c7PpwWv6QWBD")
HUB = "https://claude.ai/artifact/23ox422LgUwgvaSdabVr6s"
url2file = {u: f"{k}.html" for k, u in L.items()}
url2file[HUB] = "index.html"
mod2key = {"p00_summary": "index", "p01_index": "index-futures"}
for f in glob.glob("gen/p*.py"):
    m = os.path.basename(f)[:-3]
    if "backup" in m: continue
    key = m.split("_", 1)[1]
    mod2key.setdefault(m, key)
mod2key["p01_index"] = "index"  # placeholder fixed below
# links.txt key for stock index page is 'index'; rename it to avoid clash with hub
url2file[L["index"]] = "equity.html"
mod2key["p01_index"] = "equity"; mod2key["p00_summary"] = "index"
# generator module names vs links.txt keys
alias = {"p03a_eur": "eur", "p03b_jpy": "jpy", "p03c_gbp": "gbp", "p03d_aud": "aud", "p03e_cad": "cad", "p03f_chf": "chf", "p03g_dx": "dx"}
mod2key.update(alias)
HEAD = ('<!doctype html>\n<html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n')
BACK = ('<a href="index.html" style="position:fixed;top:12px;left:12px;z-index:50;font:600 13px/1 system-ui,sans-serif;'
        'padding:8px 12px;border-radius:999px;background:rgba(0,0,0,.6);color:#fff;text-decoration:none;backdrop-filter:blur(6px)">← 한눈에 보기</a>\n')
def fix(h):
    def rep(mm):
        u = mm.group(1)
        return url2file.get(u, u)
    h = re.sub(r'(https://claude\.ai/artifact/[A-Za-z0-9]+)', rep, h)
    # internal links open in same tab
    h = re.sub(r'(href="[a-z0-9-]+\.html")\s+target="_blank"\s+rel="noopener"', r'\1', h)
    h = re.sub(r'(href=\\?"[a-z0-9-]+\.html\\?")\s+target=\\?"_blank\\?"\s+rel=\\?"noopener\\?"', r'\1', h)
    return h
for m, key in mod2key.items():
    src = f"out/{m}.html"
    if not os.path.exists(src): continue
    h = fix(open(src).read())
    if not h.lstrip().lower().startswith("<!doctype"):
        h = HEAD + h.replace("<main>", (BACK if key != "index" else "") + "<main>", 1) + "\n</html>\n"
    open(f"docs/{key}.html", "w").write(h)
for f in glob.glob("legacy/*.html"):
    h = fix(open(f).read())
    open(f"docs/{os.path.basename(f)}", "w").write(h)
open("docs/.nojekyll", "w").write("")
left = [f for f in glob.glob("docs/*.html") if "claude.ai/artifact" in open(f).read()]
print(sorted(os.listdir("docs")), "\nleftover artifact links:", left)
