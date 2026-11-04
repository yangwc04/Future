# Builder for the "관련 ETF" pages: one page per futures market, same look as the detail pages.
# Numbers come from etf_data.json (IBKR snapshot: last price, 90-day average USD volume, total net assets).
import json, math, os
from lib import *

_HERE = os.path.dirname(os.path.abspath(__file__))
_RAW = json.load(open(os.path.join(_HERE, "etf_data.json")))
DATA = _RAW["tickers"]
ASOF = _RAW["asof"]          # e.g. "2026-11-04 오전 6:50 (캘리포니아 시간, 정규장 개장 전)"

ETF_CSS = """<style>
.etf-t td:first-child b{font-family:var(--mono);font-size:1.02rem}
.etf-t td:first-child small{display:block;color:var(--muted);font-size:.78rem;line-height:1.35;white-space:normal;min-width:120px}
.etf-t td.memo{font-size:.85rem;color:var(--muted);min-width:180px}
.lev{display:inline-block;font-family:var(--mono);font-size:.85rem;font-weight:600;padding:1px 9px;border-radius:99px;white-space:nowrap}
.lev.l1{background:var(--c3-soft);color:var(--c3)} .lev.lx{background:var(--c1-soft);color:var(--c1)}
.lev.inv{background:var(--alert-soft);color:var(--alert)} .lev.mix{background:var(--c4-soft);color:var(--c4)}
.st{display:inline-block;font-size:.78rem;font-weight:700;padding:1px 8px;border-radius:6px;white-space:nowrap;border:1px solid var(--line)}
.liq{font-size:.8rem;font-weight:700;white-space:nowrap} .liq.g4{color:var(--c2)} .liq.g3{color:var(--c3)} .liq.g2{color:var(--muted)} .liq.g1{color:var(--alert)}
.grp{display:flex;flex-direction:column;gap:10px}
.grp+.grp{margin-top:18px}
.none-box{background:var(--alert-soft);border-radius:16px;padding:18px 20px;display:flex;flex-direction:column;gap:8px}
.none-box strong{color:var(--alert)}
.backlink{align-self:flex-start;font-size:.9rem;font-weight:700;text-decoration:none;color:#fff;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);border-radius:99px;padding:6px 14px}
.backlink:hover,.backlink:focus-visible{border-color:#ffe3a3;outline:none}
</style>
"""

STRUCT = {
    "fut":   ("선물 보유", "거래소 선물을 직접 사서 만기 전에 다음 달로 굴려요(롤오버). 선물 가격을 가장 그대로 따라가요."),
    "mix":   ("선물+스왑", "선물과 은행 스왑 계약을 섞어서 매일 정해진 배수(2배, -2배 등)를 맞춰요."),
    "swap":  ("스왑 위주", "주로 은행과 맺은 스왑 계약으로 지수 수익률을 받아요. 선물은 거의 안 써요."),
    "phys":  ("실물 보유", "금·은·백금 같은 실물을 금고에 보관해요. 선물 롤오버 비용이 없어요."),
    "stock": ("주식 보유", "지수에 들어 있는 주식을 직접 사요. 배당이 나오고 선물과 거의 같이 움직여요."),
    "bond":  ("채권 보유", "미국 국채를 직접 사요. 선물보다 이자(분배금)가 나오는 대신 만기 구간이 조금 달라요."),
    "cash":  ("외화 예금", "해당 통화를 은행 예금으로 들고 있어요. 환율을 그대로 따라가고 예금 이자가 붙어요."),
    "fwd":   ("외환 선도계약", "은행과 맺은 외환 선도(포워드) 계약으로 배수를 맞춰요. 선물과 거의 같은 효과예요."),
    "etn":   ("ETN", "펀드가 아니라 은행이 발행한 채권이에요. 지수를 약속대로 주지만 발행사가 망하면 위험해요(신용위험)."),
    "eq":    ("관련 주식", "상품이 아니라 그 상품을 만드는 회사(광산·목재·에너지 회사) 주식을 담아요. 선물과 따로 놀 때가 많아요."),
    "basket": ("여러 선물 바구니", "여러 상품 선물을 한 바구니에 담아요. 이 상품만 따로 사고팔 수는 없어요."),
}

def usd(v):
    if v is None: return "–"
    if v >= 1e12: return f"${v/1e12:,.1f}조"
    if v >= 1e8:
        x = v / 1e8
        return f"${x:,.0f}억" if x >= 100 else f"${x:,.1f}억"
    if v >= 1e4:
        x = v / 1e4
        return f"${x:,.0f}만"
    return f"${v:,.0f}"

def shares(v, px):
    if not v or not px: return "–"
    n = v / px
    if n >= 1e8: return f"{n/1e8:,.1f}억 주"
    if n >= 1e5: return f"{n/1e4:,.0f}만 주"
    if n >= 1e4: return f"{n/1e4:,.1f}만 주"
    return f"{n:,.0f}주"

def liq(v):
    if v is None: return ("g1", "–")
    if v >= 1e8: return ("g4", "아주 좋음")
    if v >= 1e7: return ("g3", "좋음")
    if v >= 1e6: return ("g2", "보통")
    return ("g1", "얇음")

def lev_html(lev):
    if isinstance(lev, str): return f'<span class="lev mix">{lev}</span>'
    if lev < 0: return f'<span class="lev inv">{lev:g}배</span>'
    if lev == 1: return '<span class="lev l1">1배</span>'
    return f'<span class="lev lx">{lev:g}배</span>'

def d(t): return DATA.get(t, {})

def etf_table(rows):
    """rows: (ticker, name, lev, struct, memo)"""
    out = []
    for t, name, lev, st, memo in rows:
        x = d(t)
        v, px, aum = x.get("v90"), x.get("px"), x.get("aum")
        g, gt = liq(v)
        out.append([f"<b>{t}</b><small>{name}</small>", lev_html(lev), (usd(v), "num"), (shares(v, px), "num"),
                    (usd(aum), "num"), f'<span class="st">{STRUCT[st][0]}</span>', f'<span class="liq {g}">{gt}</span>', (memo, "memo")])
    h = "".join(f"<th>{x}</th>" for x in ["티커", "레버리지", "90일 평균 거래대금", "≈ 하루 주식 수", "운용자산", "구조", "유동성", "메모"])
    body = "".join("<tr>" + "".join(f'<td class="{c[1]}">{c[0]}</td>' if isinstance(c, tuple) else f"<td>{c}</td>" for c in r) + "</tr>" for r in out)
    return f'<div class="tbl"><table class="etf-t"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'

def vol_chart(rows, label):
    """horizontal bars on a log scale: $1만 .. $100억+"""
    rows = [(t, d(t).get("v90")) for t, *_ in rows if d(t).get("v90")]
    rows.sort(key=lambda r: -r[1])
    lo, hi = 4, max(10, math.ceil(math.log10(max(v for _, v in rows))))
    W, x0, x1, top, rh = 720, 90, 600, 34, 26
    sc = (x1 - x0) / (hi - lo)
    h = top + rh * len(rows) + 30
    tick_lbl = {4: "$1만", 5: "$10만", 6: "$100만", 7: "$1천만", 8: "$1억", 9: "$10억", 10: "$100억", 11: "$1천억"}
    o = ['<text x="20" y="20" class="sm">90일 평균 하루 거래대금 (로그 눈금: 한 칸 = 10배)</text>']
    for t in range(lo, hi + 1):
        x = x0 + (t - lo) * sc
        o.append(f'<line x1="{x:.1f}" y1="{top - 4}" x2="{x:.1f}" y2="{top + rh * len(rows)}" stroke="var(--line)"/>')
        o.append(f'<text x="{x:.1f}" y="{h - 8}" text-anchor="middle" class="sm">{tick_lbl.get(t, "")}</text>')
    for i, (t, v) in enumerate(rows):
        y = top + rh * i
        lv = max(lo, math.log10(v))
        bw = max(3, (lv - lo) * sc)
        c = "--c2" if v >= 1e8 else "--c3" if v >= 1e7 else "--c4" if v >= 1e6 else "--alert"
        o.append(f'<text x="20" y="{y + 16}" class="b" style="font-family:var(--mono)">{t}</text>')
        o.append(f'<rect class="grow" x="{x0}" y="{y + 3}" width="{bw:.1f}" height="17" rx="4" fill="var({c})"/>')
        o.append(f'<text x="{x0 + bw + 8:.1f}" y="{y + 16}" class="sm">{usd(v)}</text>')
    return f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="{esc(label)}">{"".join(o)}</svg>'

def pick_best(rows, cond):
    c = [(d(t).get("v90") or 0, t) for t, _, lev, _, _ in rows if cond(lev)]
    return max(c)[1] if c and max(c)[0] > 0 else None

def common_compare(has_k1, has_lev):
    rows = [["거래 시간 (캘리포니아)", "거의 24시간 (일~금)", "정규장 06:30~13:00 · IBKR 확장시간 01:00~17:00, 확장시간엔 호가가 얇아요"],
            ["최소 단위", "1계약 (명목가치 수만~수십만 달러)", "1주 (수십 달러부터)"],
            ["레버리지", "증거금으로 자연스럽게 큼", "상품에 정해진 배수만큼 (매일 리셋)" if has_lev else "1배 위주"],
            ["만기·롤오버", "직접 다음 월물로 넘겨야 해요", "펀드가 알아서 굴려요 (비용은 가격에 녹아 있음)"],
            ["비용", "수수료 + 스프레드", "연 보수(0.1~1%대) + 스프레드"],
            ["세금 서류", "1256 계약 (60/40 과세)", "보통 1099" + (" · 일부 상품은 K-1 (조합형)" if has_k1 else "")]]
    return table(["", "선물 (IBKR)", "ETF"], rows)

def build_etf(m):
    """m: dict(key, name, fut, h1, lead, answer, back(url), back_name, pal, groups=[dict(title, note, rows)], picks, cautions,
              none (optional html), alt_title(optional), extra_sections(optional list), k1=bool)"""
    all_rows = [r for g in m["groups"] for r in g["rows"]]
    best = pick_best(all_rows, lambda l: True)
    best_long = pick_best(all_rows, lambda l: not isinstance(l, str) and l > 1)
    best_short = pick_best(all_rows, lambda l: not isinstance(l, str) and l < 0)
    best1 = pick_best(all_rows, lambda l: l == 1)
    q = [("관련 ETF 수", f"{len(all_rows)}개", "이 페이지에 정리한 미국 상장 상품")]
    if best: q.append(("거래 제일 많은 상품", best, usd(d(best).get("v90")) + " / 하루"))
    if best_long: q.append(("레버리지 롱 대표", best_long, usd(d(best_long).get("v90")) + " / 하루"))
    if best_short: q.append(("인버스(숏) 대표", best_short, usd(d(best_short).get("v90")) + " / 하루"))
    elif best1 and best1 != best: q.append(("1배 대표", best1, usd(d(best1).get("v90")) + " / 하루"))
    toc = [("pick", "추천"), ("list", "ETF 목록")] + ([("volume", "거래량 비교")] if any(d(r[0]).get("v90") for r in all_rows) else []) + [ ("struct", "구조 읽는 법"), ("vsfut", "선물 vs ETF"), ("cautions", "주의점")]
    back = f'<a class="backlink" href="{m["back"]}" target="_blank" rel="noopener">← {m["back_name"]} 선물 설명으로 돌아가기</a>'
    H = header(f"관련 ETF · {m['fut']}", m["h1"], m["lead"], m["answer"], q,
               f"IBKR 조회: {ASOF}. 거래대금은 IBKR의 최근 90일 하루 평균, 주식 수는 그 금액을 현재가로 나눈 근사치예요. 운용자산(AUM)은 IBKR 순자산 값이에요.",
               toc)
    H = H.replace('<span class="eyebrow">', back + '\n  <span class="eyebrow">', 1)

    secs = []
    if m.get("none"):
        secs.append(section("none", "먼저 결론", m.get("none_title", "이 선물만 따라가는 미국 ETF는 없어요"),
                            f'<div class="none-box">{m["none"]}</div>'))
    secs.append(section("pick", "1. 이렇게 고르세요", "목적별 추천", cards(m["picks"])))
    gl = []
    for g in m["groups"]:
        gl.append(f'<div class="grp"><h3>{g["title"]}</h3>' + (note(g["note"]) if g.get("note") else "") + etf_table(g["rows"]) + "</div>")
    secs.append(section("list", "2. 한 줄씩 비교", m.get("list_title", "관련 ETF 전체 목록"), "\n".join(gl) +
                        cap("유동성 등급: 하루 거래대금 $1억 이상 아주 좋음 · $1천만 이상 좋음 · $100만 이상 보통 · 그 아래 얇음(스프레드 주의).")))
    if any(d(r[0]).get("v90") for r in all_rows):
        secs.append(section("volume", "3. 거래량 한눈에", "어디에 돈이 몰려 있나", fig(vol_chart(all_rows, f"{m['name']} 관련 ETF 90일 평균 거래대금 비교")) +
                            cap("막대 색: 초록 $1억 이상 · 파랑 $1천만 이상 · 보라 $100만 이상 · 빨강 그 아래. 로그 눈금이라 한 칸 차이가 10배예요.")))
    used = []
    for r in all_rows:
        if r[3] not in used: used.append(r[3])
    secs.append(section("struct", "4. 구조 읽는 법", "이 페이지에 나오는 상품 구조", cards([("t-3", STRUCT[s][0], STRUCT[s][0], STRUCT[s][1]) for s in used])))
    for s in m.get("extra_sections", []): secs.append(s)
    has_lev = any(not isinstance(r[2], str) and r[2] not in (1,) for r in all_rows)
    secs.append(section("vsfut", "5. 선물로 할까, ETF로 할까", "IBKR 선물과 ETF 차이", common_compare(m.get("k1", False), has_lev)))
    secs.append(section("cautions", "6. 주의점", "사기 전에 꼭 알아둘 것", warn(m["cautions"])))
    F = fun(m["fun"][0], m["fun"][1]) if m.get("fun") else ""
    html_ = page(f"{m['name']} 관련 ETF", m["pal"], H, secs, F)
    return html_.replace("</style>\n", "</style>\n" + ETF_CSS, 1)

LEV_DECAY = (False, "레버리지·인버스는 '하루' 기준", "2배, -2배 같은 배수는 하루 수익률에만 맞춰져 있어요. 오르락내리락하는 장에서 며칠 이상 들고 있으면 기초자산이 제자리여도 손실이 쌓여요(변동성 손실). 단기 매매용으로 쓰세요.")
ROLL = (False, "롤오버 비용", "선물을 담은 ETF는 매달(또는 정해진 달) 다음 월물로 갈아타요. 먼 월물이 더 비싼 콘탱고 구간에서는 갈아탈 때마다 조금씩 손해가 나서, 오래 들면 선물 그래프보다 뒤처져요.")
K1 = (False, "K-1 세금 서류", "USO·UNG·DBA처럼 조합(LP) 형태 상품은 1099 대신 K-1 서류가 나오고, 세금 신고가 조금 번거로워요. 한국 거주자라면 세무사에게 먼저 확인하세요.")
EXT = (False, "장 시간 밖에서는 얇아요", "ETF는 캘리포니아 06:30~13:00 정규장에 거래가 몰려요. 선물은 밤에도 움직이는데, 그 사이 ETF는 다음 날 아침에 갭으로 따라가요.")
THIN = (False, "거래가 적은 상품은 지정가로", "하루 거래대금이 $100만도 안 되는 상품은 호가 사이가 넓어요. 시장가 주문 대신 지정가로 넣으세요.")
ETN_RISK = (False, "ETN은 발행사 신용위험", "ETN은 은행이 발행한 채권이라, 발행사가 상장폐지나 조기상환을 결정하면 원하지 않는 시점에 정리될 수 있어요.")
