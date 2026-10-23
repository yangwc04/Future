# Shared building blocks for the Korean futures explainer pages (same look as the rice/coffee pages).
import json, html

QUOTE_CAP_DEFAULT = "IBKR 시세, 2026-10-21 저녁 8시쯤(캘리포니아 시간) 기준. 아시아 시간대라 거래량은 하루치의 일부예요. 지금 화면과 조금 다를 수 있어요."

def css(p):
    """p = dict(light=dict(c1,c1s,c2,c2s,c3,c3s,c4,c4s,bg,surface,fg,muted,line), dark=...)"""
    def block(v):
        return ("--bg:{bg}; --surface:{surface}; --fg:{fg}; --muted:{muted}; --line:{line};"
                " --c1:{c1}; --c1-soft:{c1s}; --c2:{c2}; --c2-soft:{c2s}; --c3:{c3}; --c3-soft:{c3s};"
                " --c4:{c4}; --c4-soft:{c4s}; --alert:{al}; --alert-soft:{als};").format(**v)
    L, D = p["light"], p["dark"]
    return """
<style>
/* Layout: one reading column that follows the contract from the real-world thing to the IBKR order screen */
:root{ %s
  --display:"Black Han Sans","Noto Sans KR",system-ui,sans-serif;
  --body:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){ %s color-scheme:dark}}
:root[data-theme="dark"]{ %s color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.75;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{max-width:780px;margin:0 auto;padding-block:40px 72px;display:flex;flex-direction:column;gap:60px}
h1,h2,h3{font-family:var(--display);font-weight:400;line-height:1.3;text-wrap:balance;margin:0;letter-spacing:.01em}
h1{font-size:clamp(2rem,6vw,3.1rem)} h2{font-size:1.75rem} h3{font-size:1.15rem}
p{margin:0}
a{color:var(--c3)}
section,header{display:flex;flex-direction:column;gap:16px}
.eyebrow{font-size:.8rem;font-weight:800;letter-spacing:.08em;color:var(--c1)}
.lead{font-size:1.08rem;color:var(--muted)}
.hl{color:var(--c1)}
.answer{background:var(--c1-soft);border-radius:14px;padding:20px 22px;display:flex;flex-direction:column;gap:10px}
.answer strong{color:var(--c1)}
.quote{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.quote>div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:2px;min-width:0}
.quote small{color:var(--muted);font-size:.8rem}
.quote b{font-family:var(--mono);font-weight:500;font-size:1.2rem;font-variant-numeric:tabular-nums}
.quote span{font-size:.8rem;color:var(--muted)}
.toc{display:flex;flex-wrap:wrap;gap:8px}
.toc a{font-size:.85rem;text-decoration:none;color:var(--fg);background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:4px 12px}
.toc a:hover,.toc a:focus-visible{border-color:var(--c1);outline:none}
.fig{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;overflow-x:auto}
.fig svg{display:block;width:100%%;height:auto;min-width:600px}
.fig.narrow svg{min-width:480px}
.cap{font-size:.86rem;color:var(--muted)}
svg text{font-family:var(--body);fill:var(--fg);font-size:14px}
svg .sm{font-size:12px;fill:var(--muted)}
svg .b{font-weight:800}
.tbl{overflow-x:auto}
table{border-collapse:collapse;width:100%%;font-size:.95rem}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:.85rem;color:var(--muted);font-weight:600;white-space:nowrap}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
td.bad{color:var(--alert)} td.good{color:var(--c2);font-weight:600}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.cards>div{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:6px;min-width:0}
.tag{align-self:flex-start;font-size:.75rem;font-weight:800;padding:2px 10px;border-radius:99px}
.t-1{background:var(--c1-soft);color:var(--c1)} .t-2{background:var(--c2-soft);color:var(--c2)}
.t-3{background:var(--c3-soft);color:var(--c3)} .t-4{background:var(--c4-soft);color:var(--c4)}
.t-spec{background:var(--alert-soft);color:var(--alert)}
.drivers{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.drivers>div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:6px;min-width:0}
.drivers .dir{font-size:.8rem;font-weight:800;white-space:nowrap}
.up{color:var(--alert)} .down{color:var(--c2)} .both{color:var(--c3)}
.drivers .k{display:flex;justify-content:space-between;gap:8px;align-items:baseline;flex-wrap:wrap}
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.spec{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;min-width:0}
.spec h3{padding:12px 14px;display:flex;align-items:center;gap:8px;background:var(--c1-soft)}
.spec h3 .dot{width:12px;height:12px;border-radius:50%%;background:var(--c1);flex:none}
.spec.alt h3{background:var(--c3-soft)} .spec.alt h3 .dot{background:var(--c3)}
.spec dl{display:grid;grid-template-columns:auto 1fr;margin:0}
.spec dt,.spec dd{margin:0;padding:9px 14px;border-top:1px solid var(--line)}
.spec dt{color:var(--muted);font-size:.88rem;white-space:nowrap}
.spec dd{font-family:var(--mono);font-size:.9rem;font-variant-numeric:tabular-nums;min-width:0}
.spec dd span{font-family:var(--body);color:var(--muted);font-size:.82rem}
.calc{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:14px}
.inputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}
.inputs label{display:flex;flex-direction:column;gap:4px;font-size:.85rem;color:var(--muted);min-width:0}
.inputs input,.inputs select{font:inherit;font-family:var(--mono);font-size:1rem;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);width:100%%;box-sizing:border-box}
.inputs select{font-family:var(--body)}
.inputs input:focus-visible,.inputs select:focus-visible,.presets button:focus-visible{outline:2px solid var(--c3);outline-offset:1px}
.presets{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:.85rem;color:var(--muted)}
.presets button{font:inherit;font-size:.85rem;border:1px solid var(--line);background:var(--bg);color:var(--fg);padding:4px 12px;border-radius:99px;cursor:pointer}
.presets button:hover{border-color:var(--c1)}
.out{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.out>div{background:var(--bg);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:2px;min-width:0}
.out small{color:var(--muted);font-size:.8rem}
.out b{font-family:var(--mono);font-size:1.15rem;font-variant-numeric:tabular-nums;font-weight:500;overflow-wrap:anywhere}
.pos{color:var(--c2)} .neg{color:var(--alert)}
.note{font-size:.92rem;color:var(--muted);border-left:3px solid var(--line);padding-left:12px}
.warn{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.warn>div{border-top:3px solid var(--alert);background:var(--surface);border-radius:0 0 12px 12px;padding:14px 16px;display:flex;flex-direction:column;gap:6px;min-width:0}
.warn>div.hot{border-top-color:var(--c1);background:var(--c1-soft)}
.fun{background:var(--surface);border:1px dashed var(--c1);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:8px}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.back{font-size:.85rem;color:var(--muted)}
/* ---- refreshed look: hero header, pill eyebrows, softer cards ---- */
:root{--hero-a:color-mix(in srgb,var(--c1) 90%%,#000);--hero-b:color-mix(in srgb,color-mix(in srgb,var(--c1) 55%%,var(--c4)) 62%%,#000);--shadow:0 1px 2px rgba(20,25,35,.05),0 6px 20px rgba(20,25,35,.06)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--hero-a:color-mix(in srgb,var(--c1) 34%%,#0b0d10);--hero-b:color-mix(in srgb,var(--c4) 30%%,#0b0d10);--shadow:none}}
:root[data-theme="dark"]{--hero-a:color-mix(in srgb,var(--c1) 34%%,#0b0d10);--hero-b:color-mix(in srgb,var(--c4) 30%%,#0b0d10);--shadow:none}
main{gap:68px}
h1,h2,h3{word-break:keep-all}
main>header{background:radial-gradient(130%% 150%% at 0%% 0%%,var(--hero-a) 0%%,var(--hero-a) 30%%,var(--hero-b) 100%%);color:#fff;
  border-radius:24px;padding:32px 30px;gap:18px;position:relative;overflow:hidden;box-shadow:var(--shadow)}
main>header::after{content:"";position:absolute;right:-90px;top:-90px;width:280px;height:280px;border-radius:50%%;background:rgba(255,255,255,.07);pointer-events:none}
main>header>*{position:relative;z-index:1}
main>header .eyebrow{color:#ffe3a3}
main>header .hl{color:#ffe3a3}
main>header .lead{color:rgba(255,255,255,.88)}
main>header .lead b{color:#fff}
main>header .answer{background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.2);color:#fff}
main>header .answer strong,main>header .answer b{color:#ffe3a3}
main>header .quote>div{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.2)}
main>header .quote small,main>header .quote span,main>header .cap{color:rgba(255,255,255,.75)}
main>header .toc a{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.24);color:#fff}
main>header .toc a:hover,main>header .toc a:focus-visible{border-color:#ffe3a3}
main>header a{color:#ffe3a3}
main>header .back{color:rgba(255,255,255,.8)}
section>.eyebrow{align-self:flex-start;background:var(--c1-soft);color:var(--c1);border-radius:99px;padding:3px 12px;letter-spacing:.03em}
section>h2{font-size:clamp(1.5rem,4.2vw,1.95rem)}
section>h3{margin-top:6px}
.fig,.calc,.cards>div,.drivers>div,.spec,.quote>div,.warn>div{box-shadow:var(--shadow)}
.fig{border-radius:18px}
.cards>div,.drivers>div{border-radius:16px;transition:transform .15s,border-color .15s}
.cards>div:hover,.drivers>div:hover{transform:translateY(-2px);border-color:var(--c1)}
.cards h3,.drivers h3{font-size:1.05rem}
.warn{grid-template-columns:repeat(auto-fit,minmax(min(100%%,330px),1fr))}
.warn>div{border-radius:0 0 14px 14px}
.answer{border-radius:16px}
.fun{border-radius:18px;background:linear-gradient(135deg,var(--c1-soft),var(--surface) 70%%)}
.note{border-left-color:var(--c1)}
@media (max-width:560px){main>header{padding:22px 18px;border-radius:20px}}
@media (prefers-reduced-motion: no-preference){
  .grow{animation:grow .9s ease-out both;transform-box:fill-box;transform-origin:left}
  @keyframes grow{from{transform:scaleX(.3)}to{transform:scaleX(1)}}
}
</style>
""" % (block(L), block(D), block(D))

HEAD = """<title>%s</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;600;800&family=IBM+Plex+Mono:wght@500&display=swap">
"""

def esc(s): return html.escape(str(s), quote=True)

# ---------- header ----------
def header(eyebrow, h1, lead, answer, quotes, quote_cap, toc):
    q = "".join('<div><small>%s</small><b>%s</b><span>%s</span></div>' % t for t in quotes)
    t = "".join('<a href="#%s">%s</a>' % (a, b) for a, b in toc)
    return f"""<header>
  <span class="eyebrow">{eyebrow}</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <div class="answer">{answer}</div>
  <div class="quote" aria-label="IBKR 시세">{q}</div>
  <p class="cap">{quote_cap}</p>
  <nav class="toc" aria-label="목차">{t}</nav>
</header>"""

def section(id, eyebrow, h2, body):
    return f'<section id="{id}">\n  <span class="eyebrow">{eyebrow}</span>\n  <h2>{h2}</h2>\n{body}\n</section>'

def fig(svg, narrow=False):
    return '<div class="fig%s">%s</div>' % (" narrow" if narrow else "", svg)

def cap(t): return f'<p class="cap">{t}</p>'
def note(t): return f'<p class="note">{t}</p>'
def p(t): return f'<p>{t}</p>'

def table(head, rows, numcols=()):
    h = "".join(f"<th>{x}</th>" for x in head)
    body = ""
    for r in rows:
        cells = ""
        for i, c in enumerate(r):
            cls = ""
            if isinstance(c, tuple): c, cls = c
            elif i in numcols: cls = "num"
            cells += f'<td class="{cls}">{c}</td>' if cls else f"<td>{c}</td>"
        body += f"<tr>{cells}</tr>"
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'

def cards(items):
    """items: (tagclass, tagtext, title, text)"""
    return '<div class="cards">' + "".join(
        f'<div><span class="tag {a}">{b}</span><h3>{c}</h3><p>{d}</p></div>' for a, b, c, d in items) + "</div>"

def drivers(items):
    """items: (title, dirclass, dirtext, text)"""
    return '<div class="drivers">' + "".join(
        f'<div><div class="k"><h3>{a}</h3><span class="dir {b}">{c}</span></div><p>{d}</p></div>' for a, b, c, d in items) + "</div>"

def warn(items):
    """items: (hot?, title, text)"""
    return '<div class="warn">' + "".join(
        f'<div{" class=\"hot\"" if h else ""}><h3>{t}</h3><p>{x}</p></div>' for h, t, x in items) + "</div>"

def spec(title, rows, alt=False):
    dl = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows)
    return f'<div class="spec{" alt" if alt else ""}"><h3><span class="dot"></span>{title}</h3><dl>{dl}</dl></div>'

def specs(*blocks): return '<div class="specs">' + "".join(blocks) + "</div>"

def fun(title, text): return f'<section class="fun"><h3>{title}</h3><p>{text}</p></section>'

# ---------- SVG helpers ----------
def _wrap_svg(w, h, label, inner):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">{inner}</svg>'

def flow(steps, hi, box_title, box_lines, label):
    """steps: [(title, sub)], hi: index highlighted (what the contract trades). box under the row."""
    n = len(steps); W = 760; gap = 34; x0 = 20
    w = (W - 2 * x0 - gap * (n - 1)) / n
    out = ['<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--muted)"/></marker></defs>']
    for i, (t, s) in enumerate(steps):
        x = x0 + i * (w + gap)
        on = i == hi
        out.append(f'<rect x="{x:.1f}" y="20" width="{w:.1f}" height="84" rx="12" fill="var({"--c1-soft" if on else "--bg"})" stroke="var({"--c1" if on else "--line"})" stroke-width="{2 if on else 1}"/>')
        out.append(f'<text x="{x + w/2:.1f}" y="54" text-anchor="middle" class="b"{" style=\"fill:var(--c1)\"" if on else ""}>{t}</text>')
        out.append(f'<text x="{x + w/2:.1f}" y="78" text-anchor="middle" class="sm">{s}</text>')
        if i < n - 1:
            ax = x + w + 4
            out.append(f'<line x1="{ax:.1f}" y1="62" x2="{ax + gap - 8:.1f}" y2="62" stroke="var(--muted)" stroke-width="2" marker-end="url(#ar)"/>')
    hx = x0 + hi * (w + gap) + w / 2
    by = 136; bh = 40 + 24 * len(box_lines)
    out.append(f'<line x1="{hx:.1f}" y1="106" x2="{hx:.1f}" y2="{by}" stroke="var(--c1)" stroke-width="2" stroke-dasharray="4 3"/>')
    out.append(f'<rect x="20" y="{by}" width="720" height="{bh}" rx="12" fill="var(--c1-soft)"/>')
    out.append(f'<text x="40" y="{by + 28}" class="b" style="fill:var(--c1)">{box_title}</text>')
    for i, l in enumerate(box_lines):
        out.append(f'<text x="40" y="{by + 54 + 24 * i}">{l}</text>')
    return _wrap_svg(W, by + bh + 10, label, "".join(out))

def bars(title, rows, vmax, ticks, label, unitfmt="{}%", lw=150, W=720):
    """rows: (name, value, colorvar, valuetext, note). colorvar like '--c1'. ticks: values for gridlines."""
    x0 = lw + 20
    # reserve room on the right for the widest value + note so nothing runs off the viewBox
    reserve = max(9 * len(r[3]) + 16 + (12 * len(r[4]) + 14 if r[4] else 0) for r in rows)
    x1 = min(W - 40, W - reserve + (vmax - max(r[1] for r in rows)) / vmax * (W - 40 - x0))
    x1 = max(x1, x0 + 200)
    sc = (x1 - x0) / vmax
    top = 40; rh = 28
    h = top + rh * len(rows) + 30
    out = [f'<text x="20" y="22" class="sm">{title}</text>']
    for t in ticks:
        x = x0 + t * sc
        out.append(f'<line x1="{x:.1f}" y1="{top - 4}" x2="{x:.1f}" y2="{top + rh * len(rows)}" stroke="var(--line)"/>')
        out.append(f'<text x="{x:.1f}" y="{h - 8}" text-anchor="middle" class="sm">{unitfmt.format(t)}</text>')
    for i, (n, v, c, vt, nt) in enumerate(rows):
        y = top + rh * i
        hl = c == "--c1"
        st = ' style="fill:var(--c1)"' if hl else ""
        out.append(f'<text x="20" y="{y + 17}" class="b"{st}>{n}</text>')
        bw = max(2, v * sc)
        out.append(f'<rect class="grow" x="{x0}" y="{y + 2}" width="{bw:.1f}" height="20" rx="4" fill="var({c})"/>')
        out.append(f'<text x="{x0 + bw + 8:.1f}" y="{y + 17}" class="b"{st}>{vt}</text>')
        if nt:
            out.append(f'<text x="{x0 + bw + 8 + 9 * len(vt) + 8:.1f}" y="{y + 17}" class="sm">{nt}</text>')
    return _wrap_svg(W, h, label, "".join(out))

def share(title, segs, label, W=720):
    """segs: (name, pct, colorvar). Narrow segments get a legend line instead of an inside label."""
    x = 20.0; sc = (W - 40) / 100.0
    out = [f'<text x="20" y="24" class="sm">{title}</text>']
    legend = []
    for n, pc, c in segs:
        w = pc * sc
        soft = c.endswith("-soft") or c == "--line"
        out.append(f'<rect class="grow" x="{x:.1f}" y="40" width="{w:.1f}" height="40" fill="var({c})"/>')
        txt = f"{n} {pc:g}%"
        if w >= 9 * len(txt) + 10:
            fill = "var(--fg)" if soft else "var(--surface)"
            out.append(f'<text x="{x + w/2:.1f}" y="65" text-anchor="middle" class="b" style="fill:{fill}">{txt}</text>')
        else:
            legend.append((txt, c))
        x += w
    lx = 20
    for txt, c in legend:
        out.append(f'<rect x="{lx}" y="96" width="12" height="12" rx="2" fill="var({c})"/>')
        out.append(f'<text x="{lx + 18}" y="107" class="sm">{txt}</text>')
        lx += 18 + 8 * len(txt) + 22
    h = 120 if legend else 96
    return _wrap_svg(W, h, label, "".join(out))

MONTHS = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]

def calendar(rows, label, today=(10, 22)):
    """rows: (name, items). item: ('bar', m1, m2, text, color) months inclusive, wraps if m2<m1;
    ('dots', [months], color) ; ('pin', month, day, text, color)"""
    X0, MW = 150, 48
    top = 50; rh = 38
    h = top + rh * len(rows) + 24
    out = ['<g class="sm" text-anchor="middle">' + "".join(
        f'<text x="{X0 + MW * i + 24}" y="28">{m}</text>' for i, m in enumerate(MONTHS)) + "</g>"]
    out.append('<g stroke="var(--line)">' + "".join(
        f'<line x1="{X0 + MW * i}" y1="38" x2="{X0 + MW * i}" y2="{h - 20}"/>' for i in (0, 3, 6, 9, 12)) + "</g>")
    tx = X0 + MW * (today[0] - 1) + MW * today[1] / 31
    out.append(f'<line x1="{tx:.0f}" y1="38" x2="{tx:.0f}" y2="{h - 20}" stroke="var(--alert)" stroke-dasharray="3 3"/>')
    out.append(f'<text x="{tx:.0f}" y="{h - 4}" text-anchor="middle" class="sm" style="fill:var(--alert)">지금</text>')
    for i, (name, items) in enumerate(rows):
        y = top + rh * i
        out.append(f'<text x="16" y="{y + 16}" class="b">{name}</text>')
        for it in items:
            if it[0] == "bar":
                _, m1, m2, text, c = it
                segs = [(m1, m2)] if m2 >= m1 else [(m1, 12), (1, m2)]
                longest = max(range(len(segs)), key=lambda k: segs[k][1] - segs[k][0])
                for j, (a, b) in enumerate(segs):
                    x = X0 + MW * (a - 1) + 2; w = MW * (b - a + 1) - 4
                    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="var({c}-soft)" stroke="var({c})"/>')
                    if j == longest:
                        long_ = w >= 7.5 * len(text) + 10
                        tx2 = x + w / 2 if long_ else x + w + 6
                        anchor = "middle" if long_ else "start"
                        if not long_ and x + w + 6 + 7.5 * len(text) > 735:
                            tx2, anchor = x - 6, "end"
                        out.append(f'<text x="{tx2:.0f}" y="{y + 17}" text-anchor="{anchor}" style="font-size:12px;fill:var({c})" class="b">{text}</text>')
            elif it[0] == "dots":
                _, ms, c = it
                out.append("".join(f'<circle cx="{X0 + MW * (m - 1) + 24}" cy="{y + 12}" r="4" fill="var({c})"/>' for m in ms))
            elif it[0] == "pin":
                _, m, d, text, c = it
                cx = X0 + MW * (m - 1) + MW * d / 31
                out.append(f'<circle cx="{cx:.0f}" cy="{y + 12}" r="7" fill="var({c})"/>')
                anchor, tx3 = ("start", cx + 12) if cx < 600 else ("end", cx - 12)
                out.append(f'<text x="{tx3:.0f}" y="{y + 17}" text-anchor="{anchor}" style="font-size:12px;fill:var({c})" class="b">{text}</text>')
    return _wrap_svg(740, h, label, "".join(out))

def hedge(left, right, center, foot, label):
    """left/right: (title, quote, action)"""
    (lt, lq, la), (rt, rq, ra), (ct, cs) = left, right, center
    inner = f"""
<rect x="10" y="30" width="200" height="112" rx="14" fill="var(--c2-soft)"/>
<text x="110" y="62" text-anchor="middle" class="b" style="fill:var(--c2)">{lt}</text>
<text x="110" y="90" text-anchor="middle">{lq}</text>
<text x="110" y="116" text-anchor="middle" class="sm">{la}</text>
<rect x="450" y="30" width="200" height="112" rx="14" fill="var(--c3-soft)"/>
<text x="550" y="62" text-anchor="middle" class="b" style="fill:var(--c3)">{rt}</text>
<text x="550" y="90" text-anchor="middle">{rq}</text>
<text x="550" y="116" text-anchor="middle" class="sm">{ra}</text>
<circle cx="330" cy="86" r="56" fill="var(--c1-soft)" stroke="var(--c1)" stroke-width="2"/>
<text x="330" y="82" text-anchor="middle" class="b" style="fill:var(--c1)">{ct}</text>
<text x="330" y="102" text-anchor="middle" class="sm">{cs}</text>
<line x1="215" y1="86" x2="270" y2="86" stroke="var(--c2)" stroke-width="3"/>
<line x1="390" y1="86" x2="445" y2="86" stroke="var(--c3)" stroke-width="3"/>
<text x="330" y="182" text-anchor="middle" class="sm">{foot}</text>"""
    return _wrap_svg(660, 200, label, inner)

# ---------- trading hours ----------
# Shown in California time. Chicago and New York change clocks on the same days as California,
# so exchange hours in PT are the same all year: PT = CT - 2 = ET - 3.
OFF = {"CT": 2, "ET": 3}

def _pt(hhmm, tz):
    h, m = map(int, hhmm.split(":"))
    return (h + m / 60 - OFF[tz]) % 24

def _fmt(x):
    x %= 24
    return "%02d:%02d" % (int(x), round((x - int(x)) * 60))

# reference sessions in PT (summer; Tokyo/Shanghai come one hour earlier Nov~Mar)
WORLD_REF = [("도쿄·상하이", (17, 24.0), "--c4"), ("런던", (0, 8.5), "--c2"), ("뉴욕 증시", (6.5, 13), "--c1")]

def hours(sessions, tz, foot_soft, foot_solid, label):
    """sessions: list of (start, end, solid?) in exchange local time (tz CT or ET). Drawn in PT on a 14:00 -> 14:00 axis."""
    X0, X1 = 150, 722; SPAN = 24; sc = (X1 - X0) / SPAN
    def off(v): return (v - 14) % 24
    def bar(a, b, y, h, fill, stroke=""):
        oa = off(a); ln = (b - a) % 24 or 24
        out = []
        for s, w in ([(oa, min(ln, 24 - oa))] + ([(0, oa + ln - 24)] if oa + ln > 24 else [])):
            out.append(f'<rect x="{X0 + s * sc:.1f}" y="{y}" width="{w * sc:.1f}" height="{h}" rx="7" fill="{fill}"{stroke}/>')
        return "".join(out)
    out = [f'<rect x="{X0 + 4 * sc:.1f}" y="32" width="{12 * sc:.1f}" height="164" fill="var(--line)" opacity=".35"/>']
    out.append('<g class="sm" text-anchor="middle">')
    for i, t in enumerate(["14시", "18시", "22시", "02시", "06시", "10시", "14시"]):
        out.append(f'<text x="{X0 + 4 * i * sc:.0f}" y="24">{t}</text>')
    out.append(f'<text x="{X0 + 10 * sc:.0f}" y="44">밤</text></g><g stroke="var(--line)">')
    for i in range(7):
        out.append(f'<line x1="{X0 + 4 * i * sc:.0f}" y1="32" x2="{X0 + 4 * i * sc:.0f}" y2="196"/>')
    out.append("</g>")
    y = 54
    out.append(f'<text x="16" y="{y + 16}" class="b" style="fill:var(--c1)">이 상품</text>')
    labels = []
    for s, e, solid in sessions:
        a = _pt(s, tz); b = _pt(e, tz)
        if solid: out.append(bar(a, b, y + 3, 16, "var(--c1)", ' stroke="var(--c1)"'))
        else: out.append(bar(a, b, y, 22, "var(--c1-soft)", ' stroke="var(--c1)"'))
        labels.append(("집중 " if solid else "") + f"{_fmt(a)}~{_fmt(b)}")
    out.append(f'<text x="{X0}" y="{y + 42}" class="sm">{"  ·  ".join(labels)} (캘리 기준, 일년 내내 같음)</text>')
    for i, (name, (a, b), c) in enumerate(WORLD_REF):
        yy = 120 + i * 24
        out.append(f'<text x="16" y="{yy + 11}" class="sm">{name}</text>' + bar(a, b, yy + 2, 10, f"var({c})", ' opacity=".45"'))
    sx = X0
    if foot_soft:
        out.append(f'<rect x="{X0}" y="206" width="14" height="10" rx="3" fill="var(--c1-soft)" stroke="var(--c1)"/><text x="{X0 + 20}" y="215" class="sm">{foot_soft}</text>')
        sx = X0 + 300
    out.append(f'<rect x="{sx}" y="206" width="14" height="10" rx="3" fill="var(--c1)"/><text x="{sx + 20}" y="215" class="sm">{foot_solid}</text>')
    return _wrap_svg(740, 226, label, "".join(out))

def pt_range(s, e, tz):
    return f"{_fmt(_pt(s, tz))}~{_fmt(_pt(e, tz))}"

# ---------- calculator ----------
def calc(contracts, presets, unit_label, note_text):
    """contracts: dict(name, tick, tv(tick value $), mult($ per 1.0 price), dec, entry, exit, f32 optional)
    presets: (label, contract_index, entry, exit)"""
    opts = "".join(f'<option value="{i}">{esc(c["name"])}</option>' for i, c in enumerate(contracts))
    pb = "".join(f'<button type="button" data-c="{c}" data-e="{e}" data-x="{x}">{l}</button>' for l, c, e, x in presets)
    c0 = contracts[0]
    data = json.dumps(contracts, ensure_ascii=False)
    return f"""<div class="calc">
    <div class="presets">빠른 입력: {pb}</div>
    <div class="inputs">
      <label for="in-ct">계약<select id="in-ct">{opts}</select></label>
      <label for="in-entry">진입가 ({unit_label})<input id="in-entry" type="number" step="any" value="{c0['entry']}" inputmode="decimal"></label>
      <label for="in-exit">청산가 ({unit_label})<input id="in-exit" type="number" step="any" value="{c0['exit']}" inputmode="decimal"></label>
      <label for="in-qty">계약 수<input id="in-qty" type="number" step="1" min="1" value="1" inputmode="numeric"></label>
      <label for="in-side">방향<select id="in-side"><option value="1">매수 (롱)</option><option value="-1">매도 (숏)</option></select></label>
    </div>
    <div class="out">
      <div><small>1계약 명목가치 (진입 기준)</small><b id="o-notional">–</b></div>
      <div><small>움직인 틱 수</small><b id="o-ticks">–</b></div>
      <div><small>손익 (달러)</small><b id="o-pnl">–</b></div>
      <div><small>가격 변화율</small><b id="o-krw">–</b></div>
    </div>
    <p class="cap" id="o-explain"></p>
  </div>
  {note(note_text)}
<script>
(function(){{
  var C = {data};
  var $ = function(id){{return document.getElementById(id)}};
  var usd = function(v,d){{var s=Math.abs(v).toLocaleString('en-US',{{minimumFractionDigits:d||0,maximumFractionDigits:d||0}});return (v<0?'−$':'$')+s}};
  function f32(v){{var w=Math.floor(v+1e-9), r=(v-w)*32; return w+'-'+(Math.round(r*1000)/1000).toString().replace(/^(\\d)(\\.|$)/,'0$1$2')}}
  function fmt(c,v){{return c.f32 ? v.toFixed(c.dec)+' ('+f32(v)+')' : v.toFixed(c.dec)}}
  function calc(){{
    var c = C[parseInt($('in-ct').value,10)];
    var e = parseFloat($('in-entry').value), x = parseFloat($('in-exit').value);
    var q = Math.max(1, parseInt($('in-qty').value,10) || 1), side = parseInt($('in-side').value,10);
    if (isNaN(e) || isNaN(x)) {{ ['o-notional','o-ticks','o-pnl','o-krw'].forEach(function(id){{$(id).textContent='–'}}); $('o-explain').textContent=''; return; }}
    // ticks = price change / minimum tick; each tick is worth a fixed dollar amount per contract
    var ticks = Math.round((x - e) / c.tick);
    var pnl = ticks * c.tv * q * side;
    var cents = c.tv % 1 !== 0 ? 2 : 0;
    $('o-notional').textContent = usd(e * c.mult);
    $('o-ticks').textContent = (ticks>0?'+':'') + ticks.toLocaleString('en-US') + '틱';
    var p = $('o-pnl'); p.textContent = (pnl>0?'+':'') + usd(pnl, cents); p.className = pnl>0?'pos':(pnl<0?'neg':'');
    var pct = (x - e) / e * 100; var k = $('o-krw'); k.textContent = (pct>0?'+':'') + pct.toFixed(2) + '%';
    $('o-explain').textContent = c.name + ' · ' + fmt(c,e) + ' → ' + fmt(c,x) + ' : ' + Math.abs(ticks).toLocaleString('en-US') + '틱 × $' + c.tv + ' × ' + q + '계약' + (side<0?' (숏이라 부호 반대)':'') + ' = ' + usd(pnl, cents);
  }}
  $('in-ct').addEventListener('change', function(){{ var c=C[parseInt(this.value,10)]; $('in-entry').value=c.entry; $('in-exit').value=c.exit; calc(); }});
  document.querySelectorAll('.presets button').forEach(function(b){{
    b.addEventListener('click', function(){{ $('in-ct').value=b.dataset.c; $('in-entry').value=b.dataset.e; $('in-exit').value=b.dataset.x; calc(); }});
  }});
  ['in-entry','in-exit','in-qty','in-side'].forEach(function(id){{$(id).addEventListener('input', calc)}});
  calc();
}})();
</script>"""

def page(title, palette, head_html, sections, fun_html=""):
    return HEAD % esc(title) + css(palette) + "\n<main>\n" + head_html + "\n" + "\n".join(sections) + "\n" + fun_html + "\n</main>\n"

# ---------- palettes ----------
def pal(c1, c2, c3, c4, dark, neutral=None):
    """c* = (light, light_soft); dark = list of 4 (color, soft). neutral optional (light dict, dark dict)."""
    nl = dict(bg="#f4f4f1", surface="#ffffff", fg="#20221f", muted="#62665f", line="#dadcd5", al="#b23b2e", als="#f7e0dc")
    nd = dict(bg="#131513", surface="#1c1f1c", fg="#eaebe6", muted="#a6aaa2", line="#343833", al="#ff8576", als="#3d1d19")
    if neutral: nl.update(neutral[0]); nd.update(neutral[1])
    L = dict(nl, c1=c1[0], c1s=c1[1], c2=c2[0], c2s=c2[1], c3=c3[0], c3s=c3[1], c4=c4[0], c4s=c4[1])
    D = dict(nd, c1=dark[0][0], c1s=dark[0][1], c2=dark[1][0], c2s=dark[1][1], c3=dark[2][0], c3s=dark[2][1], c4=dark[3][0], c4s=dark[3][1])
    return dict(light=L, dark=D)
