from lib import *
import json

# Summary hub, California (Pacific) time edition.
# US exchange hours are fixed in PT all year (CT/ET move with PT); foreign sessions are stored in their
# own time zone and converted in the browser so they stay right across DST changes.

PAL = pal(("#2d4f7a", "#dde6f1"), ("#2e7a55", "#d9eee3"), ("#b0601a", "#f6e5d2"), ("#6a4b96", "#e8e2f3"),
          [("#8eb2e2", "#17253a"), ("#7fd0a6", "#153026"), ("#eca86c", "#3a2614"), ("#bba4e6", "#27213c")],
          ({"bg": "#f3f4f6", "line": "#d9dce2", "muted": "#5d636c"}, {"bg": "#101216", "surface": "#191c21", "line": "#30353d"}))

L = dict(l.split() for l in open("../links.txt"))
L.update(oj="https://claude.ai/artifact/Ceb2BiwFY7LJci991bjsij", coffee="https://claude.ai/artifact/1AmSgYykjSvYAj6gme8tMU",
         rice="https://claude.ai/artifact/9teMajEtW3c7PpwWv6QWBD")

CATS = [("idx", "주가지수"), ("rate", "금리"), ("fx", "외환"), ("en", "에너지"), ("met", "금속"),
        ("gr", "곡물"), ("soft", "소프트"), ("live", "축산"), ("cry", "암호화폐"), ("vol", "변동성")]
CATC = {"idx": "c1", "rate": "c1", "fx": "c2", "en": "c3", "met": "c4", "gr": "c2", "soft": "c3", "live": "c4", "cry": "c1", "vol": "c4"}
CATN = dict(CATS)

PAGES = [  # (cat, title, symbols, link key)
    ("idx", "주가지수 선물", "ES · NQ · YM · RTY + 마이크로", "index"),
    ("rate", "국채·SOFR 선물", "ZT · ZF · ZN · ZB · SR3", "rates"),
    ("fx", "유로", "6E · M6E", "eur"), ("fx", "일본 엔", "6J · MJY", "jpy"), ("fx", "영국 파운드", "6B · M6B", "gbp"),
    ("fx", "호주달러", "6A · M6A", "aud"), ("fx", "캐나다달러", "6C · MCD", "cad"), ("fx", "스위스프랑", "6S · MSF", "chf"),
    ("fx", "달러인덱스", "DX", "dx"), ("fx", "외환 개요 (7개 비교)", "가격 읽는 법 · 비교표", "fx"),
    ("en", "원유", "CL · MCL · QM · BZ", "crude"), ("en", "천연가스", "NG · QG · MNG", "natgas"), ("en", "휘발유·경유", "RB · HO", "products"),
    ("met", "금", "GC · MGC · 1OZ", "gold"), ("met", "은", "SI · SIL · SIC", "silver"), ("met", "구리", "HG · MHG", "copper"), ("met", "백금·팔라듐", "PL · PA", "pgm"),
    ("gr", "옥수수·귀리", "ZC · XC · ZO", "corn"), ("gr", "대두 3형제", "ZS · ZM · ZL", "soy"), ("gr", "밀", "ZW · KE · XW", "wheat"), ("gr", "쌀", "ZR", "rice"),
    ("soft", "커피", "KC", "coffee"), ("soft", "오렌지주스", "OJ", "oj"), ("soft", "설탕", "SB", "sugar"), ("soft", "코코아", "CC", "cocoa"),
    ("soft", "면화", "CT", "cotton"), ("soft", "목재", "LBR", "lumber"),
    ("live", "소 (생우·비육우)", "LE · GF", "cattle"), ("live", "돼지", "HE", "hogs"),
    ("cry", "비트코인·이더리움", "BTC · MBT · ETH · MET", "crypto"),
    ("vol", "VIX", "VX · VXM", "vix"),
]

# Trading hours in PT. These never change with daylight saving because Chicago/New York switch on the same day.
HRS = {"cme": "15:00~14:00", "grain": "17:00~05:45, 06:30~11:20", "live": "06:30~11:05", "lbr": "07:00~13:05",
       "sb": "00:30~10:00", "cc": "01:45~10:30", "kc": "01:15~10:30", "oj": "05:00~11:00", "ct": "18:00~11:20", "dx": "17:00~14:00"}

# liquidity tier 1..5 (5 = best)
R = [  # cat, sym, name, size, tick, tick$, notional, liq, hours, page
    ("idx", "ES", "E-mini S&P 500", "지수 × $50", "0.25", 12.5, 387788, 5, "cme", "index"),
    ("idx", "MES", "마이크로 S&P 500", "지수 × $5", "0.25", 1.25, 38779, 5, "cme", "index"),
    ("idx", "NQ", "E-mini 나스닥 100", "지수 × $20", "0.25", 5, 593135, 5, "cme", "index"),
    ("idx", "MNQ", "마이크로 나스닥 100", "지수 × $2", "0.25", 0.5, 59314, 5, "cme", "index"),
    ("idx", "YM", "E-mini 다우", "지수 × $5", "1", 5, 264630, 3, "cme", "index"),
    ("idx", "MYM", "마이크로 다우", "지수 × $0.5", "1", 0.5, 26463, 3, "cme", "index"),
    ("idx", "RTY", "E-mini 러셀 2000", "지수 × $50", "0.1", 5, 139025, 3, "cme", "index"),
    ("idx", "M2K", "마이크로 러셀 2000", "지수 × $5", "0.1", 0.5, 13903, 3, "cme", "index"),
    ("rate", "ZT", "2년 국채", "액면 $200,000", "1/256", 7.8125, 203789, 4, "cme", "rates"),
    ("rate", "ZF", "5년 국채", "액면 $100,000", "1/128", 7.8125, 104031, 4, "cme", "rates"),
    ("rate", "ZN", "10년 국채", "액면 $100,000", "1/64", 15.625, 105484, 5, "cme", "rates"),
    ("rate", "TN", "울트라 10년 국채", "액면 $100,000", "1/64", 15.625, None, 3, "cme", "rates"),
    ("rate", "ZB", "30년 국채", "액면 $100,000", "1/32", 31.25, 106344, 4, "cme", "rates"),
    ("rate", "UB", "울트라 30년 국채", "액면 $100,000", "1/32", 31.25, None, 3, "cme", "rates"),
    ("rate", "SR3", "3개월 SOFR", "1bp = $25", "0.005", 12.5, None, 4, "cme", "rates"),
    ("fx", "6E", "유로 (IBKR: EUR)", "€125,000", "0.00005", 6.25, 140622, 5, "cme", "eur"),
    ("fx", "M6E", "마이크로 유로", "€12,500", "0.0001", 1.25, 14062, 3, "cme", "eur"),
    ("fx", "6J", "엔 (IBKR: JPY)", "¥12,500,000", "0.0000005", 6.25, 79260, 4, "cme", "jpy"),
    ("fx", "6B", "파운드 (IBKR: GBP)", "£62,500", "0.0001", 6.25, 83778, 4, "cme", "gbp"),
    ("fx", "6A", "호주달러 (IBKR: AUD)", "A$100,000", "0.00005", 5, 70168, 4, "cme", "aud"),
    ("fx", "6C", "캐나다달러 (IBKR: CAD)", "C$100,000", "0.00005", 5, 71268, 4, "cme", "cad"),
    ("fx", "6S", "스위스프랑 (IBKR: CHF)", "CHF 125,000", "0.00005", 6.25, 151985, 3, "cme", "chf"),
    ("fx", "DX", "달러인덱스 (ICE)", "지수 × $1,000", "0.005", 5, 101435, 3, "dx", "dx"),
    ("en", "CL", "WTI 원유", "1,000배럴", "0.01", 10, 98430, 5, "cme", "crude"),
    ("en", "MCL", "마이크로 WTI", "100배럴", "0.01", 1, 9843, 4, "cme", "crude"),
    ("en", "QM", "E-mini WTI", "500배럴", "0.025", 12.5, 49215, 2, "cme", "crude"),
    ("en", "BZ", "브렌트 (NYMEX)", "1,000배럴", "0.01", 10, 106530, 3, "cme", "crude"),
    ("en", "NG", "천연가스", "10,000 MMBtu", "0.001", 10, 31780, 4, "cme", "natgas"),
    ("en", "QG", "E-mini 천연가스", "2,500 MMBtu", "0.005", 12.5, 7945, 2, "cme", "natgas"),
    ("en", "MNG", "마이크로 천연가스", "1,000 MMBtu", "0.001", 1, 3178, 2, "cme", "natgas"),
    ("en", "RB", "RBOB 휘발유", "42,000갤런", "0.0001", 4.2, 129066, 3, "cme", "products"),
    ("en", "HO", "초저유황 경유", "42,000갤런", "0.0001", 4.2, 194561, 3, "cme", "products"),
    ("met", "GC", "금", "100온스", "0.10", 10, 412460, 5, "cme", "gold"),
    ("met", "MGC", "마이크로 금", "10온스", "0.10", 1, 41246, 4, "cme", "gold"),
    ("met", "1OZ", "1온스 금", "1온스", "0.25", 0.25, 4125, 2, "cme", "gold"),
    ("met", "SI", "은", "5,000온스", "0.005", 25, 282775, 4, "cme", "silver"),
    ("met", "SIL", "마이크로 은", "1,000온스", "0.005", 5, 56555, 3, "cme", "silver"),
    ("met", "SIC", "100온스 은", "100온스", "0.005", 0.5, 5656, 2, "cme", "silver"),
    ("met", "HG", "구리", "25,000파운드", "0.0005", 12.5, 162788, 4, "cme", "copper"),
    ("met", "MHG", "마이크로 구리", "2,500파운드", "0.0005", 1.25, 16279, 2, "cme", "copper"),
    ("met", "PL", "백금", "50온스", "0.10", 5, 79890, 3, "cme", "pgm"),
    ("met", "PA", "팔라듐", "100온스", "0.50", 50, 106100, 2, "cme", "pgm"),
    ("gr", "ZC", "옥수수", "5,000부셸", "¼센트", 12.5, 23188, 5, "grain", "corn"),
    ("gr", "XC", "미니 옥수수 (IBKR: YC)", "1,000부셸", "⅛센트", 1.25, 4638, 2, "grain", "corn"),
    ("gr", "ZO", "귀리", "5,000부셸", "¼센트", 12.5, 19063, 1, "grain", "corn"),
    ("gr", "ZS", "대두", "5,000부셸", "¼센트", 12.5, 62138, 5, "grain", "soy"),
    ("gr", "XK", "미니 대두 (IBKR: YK)", "1,000부셸", "⅛센트", 1.25, 12428, 2, "grain", "soy"),
    ("gr", "ZM", "대두박", "100숏톤", "$0.10", 10, 34710, 4, "grain", "soy"),
    ("gr", "ZL", "대두유", "60,000파운드", "0.01센트", 6, 39528, 4, "grain", "soy"),
    ("gr", "ZW", "시카고 밀", "5,000부셸", "¼센트", 12.5, 31388, 4, "grain", "wheat"),
    ("gr", "KE", "캔자스 밀", "5,000부셸", "¼센트", 12.5, None, 3, "grain", "wheat"),
    ("gr", "XW", "미니 밀 (IBKR: YW)", "1,000부셸", "⅛센트", 1.25, 6278, 2, "grain", "wheat"),
    ("gr", "ZR", "쌀 (벼)", "2,000cwt", "$0.005", 10, 34570, 1, "grain", "rice"),
    ("soft", "KC", "커피 (아라비카)", "37,500파운드", "0.05센트", 18.75, None, 3, "kc", "coffee"),
    ("soft", "OJ", "오렌지주스", "15,000파운드", "0.05센트", 7.5, None, 1, "oj", "oj"),
    ("soft", "SB", "원당 No.11", "112,000파운드", "0.01센트", 11.2, 22926, 4, "sb", "sugar"),
    ("soft", "CC", "코코아", "10톤", "$1", 10, 58390, 3, "cc", "cocoa"),
    ("soft", "CT", "면화", "50,000파운드", "0.01센트", 5, 40780, 3, "ct", "cotton"),
    ("soft", "LBR", "목재", "27,500보드피트", "$0.50", 13.75, 14341, 2, "lbr", "lumber"),
    ("live", "LE", "생우", "40,000파운드", "0.025센트", 10, 92420, 4, "live", "cattle"),
    ("live", "GF", "비육우", "50,000파운드", "0.025센트", 12.5, 174475, 3, "live", "cattle"),
    ("live", "HE", "돈육", "40,000파운드", "0.025센트", 10, 26300, 4, "live", "hogs"),
    ("cry", "BTC", "비트코인", "5 BTC", "$5", 25, 418125, 3, "cme", "crypto"),
    ("cry", "MBT", "마이크로 비트코인", "0.1 BTC", "$5", 0.5, 8363, 3, "cme", "crypto"),
    ("cry", "ETH", "이더리움", "50 ETH", "$0.50", 25, 125925, 2, "cme", "crypto"),
    ("cry", "MET", "마이크로 이더리움", "0.1 ETH", "$0.50", 0.05, 252, 2, "cme", "crypto"),
    ("vol", "VX", "VIX 선물 (CFE)", "VIX × $1,000", "0.05", 50, 18600, 4, "cme", "vix"),
    ("vol", "VXM", "미니 VIX", "VIX × $100", "0.05", 5, 1860, 2, "cme", "vix"),
]

LIQ = {5: "최상", 4: "좋음", 3: "보통", 2: "얇음", 1: "매우 얇음"}

# ---------- time zones ----------
PT, NY, CH, LN, FR, TK, SH, SY, SP = ("America/Los_Angeles", "America/New_York", "America/Chicago", "Europe/London",
                                      "Europe/Berlin", "Asia/Tokyo", "Asia/Shanghai", "Australia/Sydney", "America/Sao_Paulo")
# hours ahead of California on 2026-10-23 (default render; the browser recomputes for today)
AHEAD = {PT: 0, NY: 3, CH: 2, LN: 8, FR: 9, TK: 16, SH: 15, SY: 18, SP: 4}
REG = {"us": "미국", "eu": "유럽", "as": "아시아·호주", "sa": "남미"}

def to_pt(h, tz): return (h - AHEAD[tz]) % 24
def hm(h):
    m = round(h * 60) % 1440
    return f"{m // 60:02d}:{m % 60:02d}"
def T(h, tz):
    """A time given in a foreign market's local clock, shown in PT; the page script keeps it right after DST changes."""
    return f'<span class="tz" data-h="{h}" data-tz="{tz}">{hm(to_pt(h, tz))}</span>'

def pos(h): return ((h - 14) % 24) / 24 * 100
def segs(a, b, cls, style=""):
    """Absolutely positioned pieces for PT range a->b on a 14:00->14:00 axis (split at the edge)."""
    oa = (a - 14) % 24; ln = (b - a) % 24 or 24
    parts = [(oa, min(ln, 24 - oa))]
    if oa + ln > 24: parts.append((0, oa + ln - 24))
    return "".join(f'<i class="{cls}" style="left:{s / 24 * 100:.3f}%;width:{w / 24 * 100:.3f}%{style}"></i>' for s, w in parts)

def track(trade, bands, now=True):
    t = "".join(segs(a, b, "tr") for a, b in trade)
    bd = "".join(segs(to_pt(a, tz), to_pt(b, tz), f"pk {reg} v{lv}") for a, b, tz, reg, lv in bands)
    data = esc(json.dumps([[a, b, tz, reg, lv] for a, b, tz, reg, lv in bands]))
    return (f'<div class="track" data-b="{data}"><div class="trl">{t}</div><div class="bl">{bd}</div>'
            + ('<i class="now" aria-hidden="true"></i>' if now else "") + "</div>")

AXIS = '<div class="axis" aria-hidden="true">' + "".join(
    f'<span style="left:{pos(h):.3f}%">{h:02d}시</span>' for h in (14, 18, 22, 2, 6, 10)) + '<span class="end">14시</span></div>'
PERIODS = '<div class="periods" aria-hidden="true">' + "".join(
    f'<span style="left:{pos(a):.3f}%;width:{((b - a) % 24) / 24 * 100:.3f}%">{t}</span>'
    for a, b, t in ((14, 18, "오후"), (18, 24, "저녁·밤"), (0, 6, "새벽"), (6, 12, "오전"), (12, 14, "낮"))) + "</div>"

# ---------- world sessions ----------
WORLD = [("시드니", "호주 증시", (10, 16, SY)), ("도쿄", "일본 증시", (9, 15.5, TK)), ("상하이·홍콩", "중국 증시", (9.5, 16, SH)),
         ("런던·유럽", "유럽 증시", (8, 16.5, LN)), ("뉴욕", "미국 증시", (9.5, 16, NY))]
WREG = {SY: "as", TK: "as", SH: "as", LN: "eu", NY: "us"}
TYPES = [("CME 24시간형", "지수·금리·외환·에너지·금속·코인·VIX", [(15, 14)]),
         ("곡물", "옥수수·대두·밀·쌀", [(17, 5.75), (6.5, 11.333)]),
         ("면화", "CT", [(18, 11.333)]),
         ("설탕·커피·코코아", "SB·KC·CC", [(0.5, 10.5)]),
         ("오렌지주스", "OJ", [(5, 11)]),
         ("소·돼지", "LE·GF·HE", [(6.5, 11.083)]),
         ("목재", "LBR", [(7, 13.083)])]

# ---------- peak-volume explanations ----------
# bands: (local start, local end, tz, region, level 2 strong / 1 medium / 0 light)
G = [
 dict(k="index", cat="idx", t="주가지수", s="ES · NQ · YM · RTY · 마이크로", pg="index", trade=[(15, 14)], best="06:30~13:00",
      bands=[(9.5, 16, NY, "us", 2), (8, 10, LN, "eu", 1), (9, 11.5, TK, "as", 0)],
      why=[("us", "<b>06:30 뉴욕 증시 개장부터 13:00 마감까지</b>. 주식·ETF·옵션이 한꺼번에 거래돼서 하루 거래량 대부분이 이 6시간 반에 몰려요. 그중에서도 개장 후 30분과 마감 전 1시간(장 마감 주문)이 가장 붐벼요."),
           ("us", "<b>05:30 미국 경제지표</b>(CPI·고용보고서, 동부 8:30)와 <b>11:00 FOMC 발표</b>(동부 14:00)가 나오는 순간 거래가 폭발해요."),
           ("eu", f"<b>{T(8, LN)} 전후 유럽 개장</b>. 런던·프랑크푸르트 아침 8~9시라 유럽 기관이 미국 지수로 헤지를 걸어요. 캘리포니아는 한밤중이지만 꽤 움직여요."),
           ("as", f"<b>{T(9, TK)} 도쿄 개장</b>. 캘리 저녁이 도쿄·서울 아침이라 아시아 투자자가 거래하지만, 규모는 정규장의 일부예요.")]),
 dict(k="rates", cat="rate", t="국채·SOFR", s="ZT · ZF · ZN · TN · ZB · UB · SR3", pg="rates", trade=[(15, 14)], best="05:00~12:00",
      bands=[(8, 15, NY, "us", 2), (8, 13, LN, "eu", 1), (9, 15, TK, "as", 0)],
      why=[("us", "<b>05:30 경제지표</b>가 하루 최대 이벤트예요. 고용·물가 숫자가 나오는 순간 10년물이 몇 초 만에 크게 움직여요."),
           ("us", "<b>10:00 국채 입찰 결과</b>(동부 13:00)와 <b>11:00 FOMC</b>. <b>12:00</b>(시카고 14:00)에 정산가가 정해지고 나면 조용해져요."),
           ("eu", f"<b>{T(8, LN)}부터 런던 시간</b>. 독일 분트·영국 길트 같은 유럽 국채와 함께 움직이고, 유럽 은행들이 거래해요."),
           ("as", f"<b>{T(9, TK)} 도쿄 시간</b>엔 일본 연기금·보험사와 아시아 중앙은행 수요가 있지만 얇아요. 일본은행 발표가 있는 날은 예외예요.")]),
 dict(k="fx_eu", cat="fx", t="유로·파운드·스위스프랑", s="6E · M6E · 6B · 6S", pg="eur", trade=[(15, 14)], best=f"{T(8, LN)}~08:30",
      bands=[(8, 13, LN, "eu", 1), (13, 16.5, LN, "eu", 2), (11.5, 16, NY, "us", 1)],
      why=[("eu", f"외환은 <b>런던이 세계 거래의 약 40%</b>를 차지해요. 런던 오전 8시 = 캘리 {T(8, LN)}. 캘리 기준으로는 한밤중~새벽이 유로·파운드·프랑의 '본장'이에요."),
           ("eu", f"<b>{T(13, LN)}~08:30, 런던 오후와 뉴욕 오전이 겹치는 시간</b>이 하루 중 가장 활발해요. 미국 지표(05:30)도 이때 나와요."),
           ("eu", f"<b>{T(16, LN)} 런던 픽스</b>(WM/R 기준환율). 펀드·기업이 이 환율로 거래하려고 주문이 몰려요. ECB 금리 발표는 {T(14.25, FR)}, 영란은행은 {T(12, LN)}."),
           ("as", "아시아 시간엔 유로·파운드 거래가 얇아서 호가 간격이 벌어져요.")]),
 dict(k="fx_jp", cat="fx", t="일본 엔", s="6J", pg="jpy", trade=[(15, 14)], best=f"{T(9, TK)}~{T(15.5, TK)}, 05:00~09:00",
      bands=[(9, 15.5, TK, "as", 1), (8, 10, LN, "eu", 1), (8, 12, NY, "us", 2)],
      why=[("as", f"<b>캘리 저녁 {T(9, TK)} = 도쿄 오전 9시</b>. 일본 수출기업, 생명보험사, 일본 개인 투자자(일명 '와타나베 부인')가 움직이는 시간이라 캘리 기준 저녁~밤에도 거래량이 받쳐줘요."),
           ("as", f"<b>{T(9 + 55 / 60, TK)} 도쿄 중값(TTM) 고시</b>. 일본 은행들이 그날 고객 환율을 정하는 시각이라 결제용 주문이 몰려요. 일본은행(BOJ) 금리 발표는 보통 도쿄 점심 무렵, 캘리 {T(12, TK)} 전후예요."),
           ("us", "그래도 CME 엔 선물 자체의 거래량 최대는 <b>캘리 오전 05:00~09:00</b>이에요. 엔 환율을 가장 크게 흔드는 게 미국 금리·지표이고, 선물 참가자 대부분이 미국 기관이라서요."),
           ("eu", f"<b>{T(8, LN)} 런던 개장</b> 때 한 번 더 활발해져요.")]),
 dict(k="fx_au", cat="fx", t="호주달러", s="6A", pg="aud", trade=[(15, 14)], best=f"{T(9, SY)}~{T(17, SY)}, 05:00~09:00",
      bands=[(9, 17, SY, "as", 1), (8, 12, NY, "us", 2)],
      why=[("as", f"<b>캘리 오후 {T(9, SY)} = 시드니 오전 9시</b>. 세계에서 하루가 가장 먼저 시작되는 곳이라 호주달러는 캘리 오후부터 거래가 붙어요. 중국 경제와 얽혀 있어 {T(9.5, SH)} 상하이·홍콩 개장 때도 활발해요."),
           ("as", f"호주중앙은행(RBA) 발표는 {T(14.5, SY)}, 호주 고용·물가 지표는 {T(11.5, SY)}. 캘리 기준 저녁이에요."),
           ("us", "선물 거래량 최대는 역시 <b>05:00~09:00</b>, 미국 지표와 뉴욕 오전 시간이에요.")]),
 dict(k="fx_ca", cat="fx", t="캐나다달러", s="6C", pg="cad", trade=[(15, 14)], best="05:00~11:00",
      bands=[(8, 14, NY, "us", 2)],
      why=[("us", "캐나다는 미국과 같은 시간대예요. <b>05:30에 캐나다·미국 지표가 함께</b> 나오고(동부 8:30), 캐나다은행 금리 발표는 <b>06:45</b>(동부 9:45)."),
           ("us", "원유와 같이 움직이는 통화라 <b>원유가 활발한 06:00~11:30</b>에 함께 거래가 많아요."),
           ("as", "아시아·유럽 시간엔 매우 조용해요.")]),
 dict(k="dx", cat="fx", t="달러인덱스", s="DX (ICE)", pg="dx", trade=[(17, 14)], best=f"{T(8, LN)}~09:00",
      bands=[(8, 13, LN, "eu", 1), (8, 12, NY, "us", 2)],
      why=[("eu", "DX는 <b>유로 비중이 57.6%</b>인 지수라 유로가 활발한 런던 시간에 같이 움직여요."),
           ("us", "가장 붐비는 건 <b>05:00~09:00</b> 런던·뉴욕 겹침과 미국 지표 발표 때예요. ICE 상품이라 거래량 자체는 CME 통화선물보다 적어요.")]),
 dict(k="crude", cat="en", t="원유", s="CL · MCL · QM · BZ", pg="crude", trade=[(15, 14)], best="06:00~11:30",
      bands=[(9, 14.5, NY, "us", 2), (8, 13, LN, "eu", 1), (9, 15, SH, "as", 0)],
      why=[("us", "<b>06:00~11:30</b>은 예전 뉴욕상업거래소 객장 시간(동부 9:00~14:30)이에요. 지금도 정산가가 <b>11:28~11:30</b> 2분 평균으로 정해져서 기관 주문이 이 시간에 몰려요."),
           ("us", "<b>수요일 07:30 EIA 원유 재고</b> 발표가 매주 최대 이벤트예요. 화요일 13:30 API 재고는 장 마감 직전이라 저녁까지 반응이 이어져요."),
           ("eu", f"<b>{T(8, LN)}부터 런던 시간</b>. 브렌트를 쓰는 유럽 정유사·트레이더가 거래하고, 중동·OPEC 뉴스(빈 시간)가 이때 많이 나와요."),
           ("as", f"아시아 시간({T(9, SH)}~)엔 중국·싱가포르 수요가 조금 있지만 얇아요. 마이크로(MCL)는 이 시간에 특히 호가가 벌어져요.")]),
 dict(k="natgas", cat="en", t="천연가스", s="NG · QG · MNG", pg="natgas", trade=[(15, 14)], best="06:00~11:30",
      bands=[(9, 14.5, NY, "us", 2), (8, 11, LN, "eu", 0)],
      why=[("us", "<b>06:00~11:30</b> 뉴욕 시간이 핵심이고 정산은 <b>11:28~11:30</b>이에요."),
           ("us", "<b>목요일 07:30 EIA 저장량 발표</b>가 한 주 최대 변동 시간이에요."),
           ("us", "천연가스는 <b>날씨 상품</b>이에요. 미국·유럽 날씨 모델이 업데이트되는 이른 아침~오전에 예보가 바뀌면 크게 움직여요."),
           ("eu", "미국 내수 상품이라 아시아·유럽 시간엔 매우 얇아요. 유럽 가스(TTF)가 급등할 때만 새벽에 따라 움직여요.")]),
 dict(k="products", cat="en", t="휘발유·경유", s="RB · HO", pg="products", trade=[(15, 14)], best="06:00~11:30",
      bands=[(9, 14.5, NY, "us", 2), (8, 13, LN, "eu", 0)],
      why=[("us", "원유와 같이 <b>06:00~11:30</b>, 정산은 <b>11:28~11:30</b>."),
           ("us", "수요일 07:30 EIA 발표에 휘발유·경유 재고도 함께 나와요. 여름엔 드라이빙 시즌(휘발유), 겨울엔 난방(경유) 날씨 뉴스에 반응해요."),
           ("eu", f"경유(HO)는 런던 ICE 가스오일과 연결돼 있어 {T(8, LN)}부터 런던 시간에도 거래가 있어요.")]),
 dict(k="gold", cat="met", t="금", s="GC · MGC · 1OZ", pg="gold", trade=[(15, 14)], best=f"05:20~10:30, {T(9, SH)}~",
      bands=[(8 + 1 / 3, 13.5, NY, "us", 2), (8, 16, LN, "eu", 1), (9, 15, SH, "as", 1)],
      why=[("us", "<b>05:20~10:30</b>은 예전 뉴욕 금 객장 시간(동부 8:20~13:30)이에요. 05:30 지표, 11:00 FOMC처럼 달러·금리 뉴스에 가장 크게 반응해요."),
           ("eu", f"<b>런던이 세계 현물 금 거래의 중심</b>이에요. 런던 금 가격 결정(LBMA)이 {T(10.5, LN)}와 {T(15, LN)}에 있어 그때 거래가 몰려요."),
           ("as", f"<b>캘리 저녁 {T(9, SH)} = 상하이 오전 9시</b>. 세계 최대 금 소비국 중국(상하이금거래소)과 인도의 실물 수요가 들어와서 아시아 시간에도 꽤 활발해요. 금이 캘리 저녁에 갑자기 움직이면 대개 중국발이에요.")]),
 dict(k="silver", cat="met", t="은", s="SI · SIL · SIC", pg="silver", trade=[(15, 14)], best="05:25~10:25",
      bands=[(8 + 25 / 60, 13 + 25 / 60, NY, "us", 2), (8, 13, LN, "eu", 1), (9, 15, SH, "as", 0)],
      why=[("us", "금처럼 <b>05:25~10:25</b>(동부 8:25~13:25)가 핵심이에요. 은은 금보다 변동이 커서 지표 발표 때 더 크게 튀어요."),
           ("eu", f"런던 은 가격 결정은 {T(12, LN)}. 런던 시간엔 유럽 산업 수요와 금을 따라가는 거래가 있어요."),
           ("as", f"{T(9, SH)} 상하이 개장 때 중국 태양광 패널 수요 관련 거래가 들어와요. 다만 금보다 얇아요.")]),
 dict(k="copper", cat="met", t="구리", s="HG · MHG", pg="copper", trade=[(15, 14)], best=f"05:10~10:00, {T(9, SH)}~",
      bands=[(8 + 1 / 6, 13, NY, "us", 2), (8, 17, LN, "eu", 1), (9, 15, SH, "as", 1)],
      why=[("us", "<b>05:10~10:00</b> 뉴욕 시간(동부 8:10~13:00)이 COMEX 구리 거래량의 중심이에요."),
           ("eu", f"<b>런던금속거래소(LME)</b>가 세계 구리 가격의 기준이에요. LME 객장(Ring)이 {T(11 + 40 / 60, LN)}~{T(17, LN)}에 열려서 캘리 새벽~오전에 활발해요."),
           ("as", f"<b>캘리 저녁 {T(9, SH)} = 상하이 오전 9시</b>. 중국이 세계 구리의 절반 넘게 쓰기 때문에 상하이선물거래소가 열리는 저녁~밤에 거래가 붙어요. 중국 경제지표도 이 시간에 나와요.")]),
 dict(k="pgm", cat="met", t="백금·팔라듐", s="PL · PA", pg="pgm", trade=[(15, 14)], best="05:20~10:05",
      bands=[(8 + 1 / 3, 13 + 5 / 60, NY, "us", 2), (8, 16, LN, "eu", 0), (9, 15, TK, "as", 0)],
      why=[("us", "<b>05:20~10:05</b> 뉴욕 시간(동부 8:20~13:05)에 거래가 몰려요. 그래도 금·은보다 훨씬 얇은 시장이에요."),
           ("eu", f"런던 백금·팔라듐 가격 결정이 {T(9.75, LN)}, {T(14, LN)}. 공급지인 남아프리카가 런던과 1~2시간 차이라 유럽 시간에 뉴스가 많아요."),
           ("as", f"{T(9, TK)} 도쿄 시간엔 일본 개인 투자자(백금이 인기)와 중국 실물 수요가 있지만 얇아요.")]),
 dict(k="grains", cat="gr", t="옥수수·대두·쌀", s="ZC · ZS · ZM · ZL · ZO · ZR", pg="corn", trade=[(17, 5.75), (6.5, 11 + 1 / 3)], best="06:30~11:20",
      bands=[(8.5, 13 + 1 / 3, CH, "us", 2), (9, 11.5, SH, "as", 0)],
      why=[("us", "<b>06:30~11:20 낮 세션</b>(시카고 8:30~13:20)이 거래량 대부분이에요. 특히 개장 직후와 <b>11:00~11:20 마감 전</b>에 몰려요. 정산가가 마감 직전에 정해지거든요."),
           ("us", "<b>USDA 보고서</b>: 월간 수급 전망(WASDE)은 <b>09:00</b>, 수출 판매는 <b>목요일 05:30</b>, 작황 보고는 <b>월요일 13:00</b>(장 마감 후라 17:00 저녁 세션에 반응)."),
           ("as", f"<b>17:00~05:45 저녁 세션</b>은 얇아요. 다만 캘리 저녁 {T(9, SH)}이 중국 오전이라 중국 수입 뉴스, 남미(브라질·아르헨티나) 날씨 소식에 반응해요."),
           ("us", "쌀(ZR)과 귀리(ZO)는 같은 시간에 열리지만 하루 거래가 아주 적어서 낮 세션 밖에선 거의 비어 있어요.")]),
 dict(k="wheat", cat="gr", t="밀", s="ZW · KE · XW", pg="wheat", trade=[(17, 5.75), (6.5, 11 + 1 / 3)], best="06:30~11:20",
      bands=[(8.5, 13 + 1 / 3, CH, "us", 2), (10.75, 18.5, FR, "eu", 0)],
      why=[("us", "옥수수·대두처럼 <b>06:30~11:20 낮 세션</b>이 핵심이에요."),
           ("eu", f"밀은 <b>흑해(러시아·우크라이나)와 유럽</b>이 큰 수출지라 파리 밀 선물(유로넥스트, {T(10.75, FR)}~)과 같이 움직여요. 전쟁·수출 뉴스가 캘리 새벽에 나오는 일이 많아요."),
           ("us", "캔자스 밀(KE)과 미니 밀은 낮 세션 밖에선 거의 거래가 없어요.")]),
 dict(k="sugar", cat="soft", t="설탕", s="SB", pg="sugar", trade=[(0.5, 10)], best="05:00~10:00",
      bands=[(8, 13, NY, "us", 2), (9, 13, SP, "sa", 1), (8.75, 12, LN, "eu", 1)],
      why=[("us", "<b>05:00~10:00</b> 뉴욕 오전이 거래량 중심이에요. 정산가는 마감 직전에 정해져요."),
           ("sa", f"<b>세계 최대 생산국 브라질</b>. 상파울루 오전 9시 = 캘리 {T(9, SP)}. 브라질 사탕수수협회(UNICA) 보고서와 헤알화 환율이 이 시간에 반영돼요."),
           ("eu", f"<b>런던 백설탕 선물(ICE 유럽)</b>과 함께 유럽·중동 정제업자가 거래해서 뉴욕 원당이 캘리 00:30(런던 아침)부터 열려요."),
           ("as", "인도·태국 작황 뉴스도 중요하지만 거래소가 닫혀 있는 시간이라 개장 때 한꺼번에 반영돼요.")]),
 dict(k="coffee", cat="soft", t="커피", s="KC", pg="coffee", trade=[(1.25, 10.5)], best="05:00~10:30",
      bands=[(8, 13.5, NY, "us", 2), (9, 14, SP, "sa", 1), (9.25, 13, LN, "eu", 1)],
      why=[("us", "<b>05:00~10:30</b> 뉴욕 오전에 가장 많이 거래되고, 정산은 10:25~10:30이에요."),
           ("sa", f"<b>브라질이 세계 아라비카의 약 40%</b>. 상파울루 오전({T(9, SP)}~)에 브라질 수출업자 주문과 서리·가뭄 날씨 뉴스가 반영돼요."),
           ("eu", "<b>런던 로부스타 선물</b>과 유럽 로스터·무역상(독일·이탈리아·스위스)이 거래하는 시간이라 뉴욕 커피가 캘리 01:15부터 열려요."),
           ("as", "베트남(로부스타 1위) 뉴스는 아시아 시간에 나오지만, 반영은 런던 개장 이후예요.")]),
 dict(k="cocoa", cat="soft", t="코코아", s="CC", pg="cocoa", trade=[(1.75, 10.5)], best="01:45~10:30",
      bands=[(9.75, 13, LN, "eu", 1), (8, 13.5, NY, "us", 2)],
      why=[("eu", f"<b>코코아는 런던 비중이 커요</b>. 1·2위 생산국 코트디부아르·가나가 런던과 같은 시간대고, 유럽 초콜릿·가공업체가 런던 코코아 선물을 많이 써요. 그래서 캘리 새벽 {T(9.75, LN)}부터 활발해요."),
           ("us", "<b>05:00~10:30</b>, 런던 오후와 뉴욕 오전이 겹칠 때 가장 많이 거래돼요. 미국 허쉬·몬델리즈도 이때 거래해요."),
           ("as", "아시아 시간엔 문이 닫혀 있어요. 서아프리카 날씨·수확 소식은 캘리 새벽 개장 때 한꺼번에 반영돼요.")]),
 dict(k="cotton", cat="soft", t="면화", s="CT", pg="cotton", trade=[(18, 11 + 1 / 3)], best="06:30~11:20",
      bands=[(9.5, 14 + 1 / 3, NY, "us", 2), (9, 15, SH, "as", 0)],
      why=[("us", "<b>06:30~11:20</b> 뉴욕 낮(동부 9:30~14:20)에 거래 대부분이 몰려요. 목요일 05:30 수출 판매 보고서가 핵심 이벤트예요."),
           ("as", f"면화는 저녁 18:00(동부 21:00)부터 열려 있어요. <b>중국·베트남·방글라데시 방적공장</b>이 주요 수입자라 캘리 저녁 {T(9, SH)}, 아시아 오전에 정저우 면화 선물과 같이 조금 거래돼요. 그래도 얇아요."),
           ("us", "미국 텍사스·남부 날씨(가뭄·허리케인)가 가격을 크게 흔들어요.")]),
 dict(k="oj", cat="soft", t="오렌지주스", s="OJ", pg="oj", trade=[(5, 11)], best="07:00~10:00",
      bands=[(10, 13, NY, "us", 2), (9, 14, SP, "sa", 0)],
      why=[("us", "<b>05:00~11:00</b>만 열리고, 그중에서도 <b>07:00~10:00</b>에 몰려요. 하루 거래가 매우 적어서 이 시간 밖엔 호가가 거의 없어요."),
           ("sa", f"<b>브라질 상파울루주가 세계 오렌지주스 수출의 70% 이상</b>이에요. 상파울루 업무 시간({T(9, SP)}~)과 겹쳐요."),
           ("us", "플로리다 허리케인·한파 뉴스가 나오는 날엔 거래가 갑자기 늘어요.")]),
 dict(k="lumber", cat="soft", t="목재", s="LBR", pg="lumber", trade=[(7, 13 + 5 / 60)], best="07:00~08:30, 12:30~13:05",
      bands=[(9, 10.5, CH, "us", 2), (14.5, 15 + 5 / 60, CH, "us", 2), (10.5, 14.5, CH, "us", 0)],
      why=[("us", "<b>07:00 개장 직후</b>와 <b>12:30~13:05 마감 전</b>에 거래가 몰리고, 중간엔 몇 분씩 체결이 없기도 해요."),
           ("us", "<b>캘리포니아와 같은 시간대</b>인 미국 북서부·캐나다 브리티시컬럼비아 제재소가 주요 공급자예요. 캘리 업무 시간 그대로라 거래하기 편한 상품이에요."),
           ("us", "주택 착공 지표(05:30)는 개장 전에 나와서 07:00 개장 때 반영돼요.")]),
 dict(k="cattle", cat="live", t="소", s="LE · GF", pg="cattle", trade=[(6.5, 11 + 5 / 60)], best="06:30~07:30, 10:30~11:05",
      bands=[(8.5, 9.5, CH, "us", 2), (9.5, 12.5, CH, "us", 1), (12.5, 13 + 5 / 60, CH, "us", 2)],
      why=[("us", "<b>06:30~07:30 개장</b>과 <b>10:30~11:05 마감</b>(시카고 8:30·13:05)에 몰려요. 하루 4시간 반만 열려요."),
           ("us", "점심 무렵 USDA 현물 소 거래·박스 비프(부위별 도매가) 시세가 나와요. 월간 <b>사육 두수(Cattle on Feed)</b>는 금요일 12:00, 장 마감 후라 월요일 개장 때 반영돼요."),
           ("us", "네브래스카·텍사스·캔자스 등 미국 중부 시장이라 해외 참가자가 거의 없어요.")]),
 dict(k="hogs", cat="live", t="돼지", s="HE", pg="hogs", trade=[(6.5, 11 + 5 / 60)], best="06:30~07:30, 10:30~11:05",
      bands=[(8.5, 9.5, CH, "us", 2), (9.5, 12.5, CH, "us", 1), (12.5, 13 + 5 / 60, CH, "us", 2)],
      why=[("us", "소와 같은 <b>06:30~11:05</b>. 개장과 마감 전에 거래가 몰려요."),
           ("us", "분기별 <b>돼지 재고(Hogs and Pigs)</b> 보고서가 12:00(장 마감 후)에 나와 다음 거래일 개장 때 크게 움직여요."),
           ("as", "중국·멕시코 수출 뉴스가 중요하지만, 거래는 미국 낮에만 할 수 있어요.")]),
 dict(k="crypto", cat="cry", t="비트코인·이더리움", s="BTC · MBT · ETH · MET", pg="crypto", trade=[(15, 14)], best="06:30~13:00",
      bands=[(9.5, 16, NY, "us", 2), (9, 12, TK, "as", 0)],
      why=[("us", "<b>06:30~13:00</b> 미국 증시 시간에 가장 많이 거래돼요. CME 코인 선물은 기관·ETF 운용사가 주로 쓰는 시장이라 미국 낮에 몰려요."),
           ("as", f"현물 코인은 24시간 365일 거래되고 아시아 비중도 커요. 캘리 저녁({T(9, TK)}~)에도 거래가 있지만 CME 선물은 상대적으로 얇아요."),
           ("us", "<b>주말 갭</b>: CME는 금요일 14:00에 닫고 일요일 15:00에 열어요. 그 사이 현물이 움직이면 일요일 오후 개장 때 가격이 건너뛰어요.")]),
 dict(k="vix", cat="vol", t="VIX", s="VX · VXM", pg="vix", trade=[(15, 14)], best="06:30~13:15",
      bands=[(9.5, 16.25, NY, "us", 2), (8, 10, LN, "eu", 0)],
      why=[("us", "<b>06:30~13:15</b>. VIX 지수는 S&amp;P 500 옵션 가격으로 계산되는데, 옵션 거래가 미국 정규장에 몰려 있어서 VIX 선물도 이 시간에 몰려요."),
           ("us", "월물 정산은 <b>만기 수요일 06:30</b> 개장 때 옵션 특별호가(SOQ)로 정해져요."),
           ("eu", "밤에도 열리지만 얇아요. 유럽·아시아 증시가 급락할 때만 거래가 붙어요.")]),
]
GK = {g["k"]: g for g in G}
ROWG = {"6E": "fx_eu", "M6E": "fx_eu", "6B": "fx_eu", "6S": "fx_eu", "6J": "fx_jp", "6A": "fx_au", "6C": "fx_ca", "DX": "dx",
        "ZW": "wheat", "KE": "wheat", "XW": "wheat"}
PGG = {"corn": "grains", "soy": "grains", "rice": "grains"}
def row_group(sym, pg): return GK[ROWG.get(sym) or PGG.get(pg) or pg]

UPCOMING = [
    ("10/25 (일)", "영국 서머타임 종료 → 11/1까지 일주일 동안 런던 시간이 캘리 기준 1시간 늦어요 (런던 08:00 = 캘리 01:00)", None),
    ("10/28 (수)", "NG 11월물 마지막 거래일", "natgas"),
    ("10/30 (금)", "대두 11월물(ZSX6) 첫 통지일 · RB/HO 11월물 만기 · LE 10월물 만기", "soy"),
    ("11/1 (일)", "미국 서머타임 종료 → 미국 거래소 시간은 캘리 기준 그대로. 서머타임이 없는 도쿄·상하이 시간은 캘리 기준 1시간 빨라지고, 시드니는 이미 서머타임이라 2시간 차이가 1시간 앞당겨져요", None),
    ("11월 중순", "CC 12월물 첫 통지일 · CT 롤오버 · LBR 11월물 만기", "cocoa"),
    ("11/18 (수)", "VIX 11월물 만기 (06:30 개장 특별호가로 정산)", "vix"),
    ("11/20 (금)", "CL 12월물(CLZ6) 마지막 거래일", "crude"),
    ("11월 하순", "국채(ZN·ZF·ZT·ZB)·금·은·구리·곡물 12월물 → 다음 월물 롤오버", "rates"),
    ("11/27 (금)", "비트코인·이더리움 11월물 만기", "crypto"),
    ("11/30 (월)", "브렌트 1월물(BZF7) 마지막 거래일 · 곡물 12월물 첫 통지일", "crude"),
    ("12/14 (월)", "외환 12월물 마지막 거래일 (캐나다달러 6C는 12/15)", "fx"),
    ("12/18 (금)", "주가지수 12월물 만기 (현금정산)", "index"),
]

LEGEND = ('<div class="legend" aria-label="범례"><span><i class="lg tr"></i>거래 가능</span><span><i class="lg pk us v2"></i>미국 시간</span>'
          '<span><i class="lg pk eu v2"></i>유럽 시간</span><span><i class="lg pk as v2"></i>아시아·호주 시간</span><span><i class="lg pk sa v2"></i>남미 시간</span>'
          '<span><i class="lg now"></i>지금</span><span class="lv">진할수록 거래가 많아요</span></div>')

def world_chart():
    rows = ['<div class="wc-row head"><div></div><div>' + PERIODS + "</div></div>"]
    for name, sub, (a, b, tz) in WORLD:
        rows.append(f'<div class="wc-row"><div class="wl"><b>{name}</b><span>{sub} · 현지 {hm(a)}~{hm(b)}</span></div>'
                    + track([], [(a, b, tz, WREG[tz], 2)]) + "</div>")
    rows.append('<div class="wc-sep">미국 거래소 선물 거래 시간 (캘리 기준, 일년 내내 같음)</div>')
    for name, sub, trade in TYPES:
        rows.append(f'<div class="wc-row"><div class="wl"><b>{name}</b><span>{sub}</span></div>' + track(trade, []) + "</div>")
    rows.append('<div class="wc-row"><div></div><div>' + AXIS + "</div></div>")
    return '<div class="wc" role="img" aria-label="캘리포니아 시간 기준 세계 증시와 선물 거래 시간표. 시드니 오후, 도쿄·상하이 저녁, 런던 새벽, 뉴욕 오전 6시 30분부터 오후 1시.">' + "".join(rows) + "</div>"

def peak_cards():
    out = []
    for g in G:
        items = "".join(f'<li><i class="dot {r}" aria-label="{REG[r]}"></i><p>{t}</p></li>' for r, t in g["why"])
        trade_txt = ", ".join(f"{hm(a)}~{hm(b)}" for a, b in g["trade"])
        out.append(f'''<article class="pc" data-cat="{g["cat"]}" style="--cc:var(--{CATC[g["cat"]]})">
  <div class="pc-h"><div><span class="ctag">{CATN[g["cat"]]}</span><h3>{g["t"]}</h3><span class="syms">{g["s"]}</span></div>
  <a class="more" href="{L[g["pg"]]}" target="_blank" rel="noopener">설명 페이지 ↗</a></div>
  <div class="best"><small>거래가 몰리는 시간</small><b>{g["best"]}</b><span>거래 가능 {trade_txt}</span></div>
  <div class="pc-t">{track(g["trade"], g["bands"])}{AXIS}</div>
  <ul class="why">{items}</ul>
</article>''')
    return "".join(out)

def build():
    n_pages = len(PAGES)
    H = f"""<header class="hero">
  <div class="hero-txt">
    <span class="eyebrow">IBKR 미국 선물 · {n_pages}개 페이지 · {len(R)}개 계약 · 캘리포니아 시간</span>
    <h1>미국 선물 <span class="hl">한눈에 보기</span></h1>
    <p class="lead">카테고리별 설명 페이지, 계약 비교표, 그리고 <b>캘리포니아 시간으로 언제 거래가 몰리는지와 그 이유</b>를 한곳에 모았어요.</p>
    <nav class="toc" aria-label="목차"><a href="#pages">페이지 모음</a><a href="#clock">세계 시장 시계</a><a href="#peaks">시간대별 거래량</a><a href="#table">비교표</a><a href="#dates">다가오는 일정</a><a href="#tips">고르는 법</a></nav>
  </div>
  <aside class="clock" aria-live="polite">
    <small>지금 캘리포니아</small>
    <b id="ptnow">--:--</b>
    <span id="ptday">&nbsp;</span>
    <div class="open"><small>지금 열려 있는 곳</small><div id="opennow"></div></div>
  </aside>
</header>"""

    cat_html = []
    for key, label in CATS:
        its = [(t, s, k) for c, t, s, k in PAGES if c == key]
        items = "".join(f'<a class="pg" href="{L[k]}" target="_blank" rel="noopener"><b>{t}</b><span>{s}</span></a>' for t, s, k in its)
        cat_html.append(f'<div class="cat" style="--cc:var(--{CATC[key]})"><h3>{label}<em>{len(its)}</em></h3><div class="pgs">{items}</div></div>')
    s1 = section("pages", "01 · 페이지 모음", "카테고리별 설명 페이지", '<div class="cats">' + "".join(cat_html) + "</div>")

    ref = ('<label class="ref" for="ref">기준 시기<select id="ref"><option value="now">오늘</option>'
           '<option value="w">겨울 (11월~3월 초)</option><option value="s">여름 (3월 중순~10월)</option></select></label>')
    s2 = section("clock", "02 · 세계 시장 시계", "캘리포니아 하루 = 아시아 → 유럽 → 미국",
        '<div class="toolbar">' + LEGEND + ref + "</div>" + world_chart() + "\n" +
        cards([("t-4", "14:00~17:00", "쉬는 시간 → 시드니", "CME는 14:00~15:00 정비 후 다시 열려요. 오후 3시쯤 시드니가, 5시에 도쿄가 아침을 맞아요."),
               ("t-4", "17:00~24:00", "저녁·밤 = 아시아", "도쿄·상하이·홍콩 오전~오후. 엔·호주달러, 금·구리가 이 시간에 움직여요."),
               ("t-2", "00:00~06:00", "새벽 = 유럽", "런던·프랑크푸르트 업무 시간. 유로·파운드, 원유·금, 코코아·설탕이 활발해요."),
               ("t-1", "05:30~13:00", "아침~오후 = 미국", "지표 05:30, 증시 06:30~13:00. 거의 모든 선물의 거래량 최대 시간이에요.")]) + "\n" +
        note("미국 거래소(시카고·뉴욕)는 캘리포니아와 같은 날 서머타임을 바꾸기 때문에 <b>선물 거래 시간은 캘리 기준으로 일년 내내 같아요</b>. 대신 서머타임이 없는 도쿄·상하이는 11월~3월에 캘리 기준 1시간 빨라지고, 런던·시드니는 바꾸는 날짜가 달라서 몇 주씩 어긋나요. 이 페이지의 해외 시간은 열어보는 날짜에 맞춰 자동으로 바뀌어요."))

    chips_p = '<button type="button" class="chip on" data-cat="all" aria-pressed="true">전체</button>' + "".join(
        f'<button type="button" class="chip" data-cat="{k}" aria-pressed="false">{v}</button>' for k, v in CATS)
    s3 = section("peaks", "03 · 시간대별 거래량", "상품별로 거래가 몰리는 시간과 그 이유",
        '<p class="lead sm">회색 막대는 거래할 수 있는 시간, 색 막대는 거래가 실제로 몰리는 시간이에요. 색은 그 시간을 움직이는 지역이고, 진할수록 거래가 많아요. 빨간 선은 지금 시각이에요.</p>'
        f'<div class="chips" id="pchips" role="group" aria-label="카테고리">{chips_p}</div>' + LEGEND +
        f'<div class="pcs">{peak_cards()}</div>')

    chips = '<button type="button" class="chip on" data-cat="all" aria-pressed="true">전체</button>' + "".join(
        f'<button type="button" class="chip" data-cat="{k}" aria-pressed="false">{v}</button>' for k, v in CATS)
    rows = []
    for c, sym, name, size, tick, tv, notional, liq, hk, pg in R:
        tvs = f"${tv:,.0f}" if tv % 1 == 0 else (f"${tv:,.2f}" if abs(tv * 100 - round(tv * 100)) < 1e-9 else "$" + f"{tv:.4f}".rstrip("0"))
        nv = f"${notional:,.0f}" if notional else "–"
        g = row_group(sym, pg)
        rows.append(f'<tr data-cat="{c}" data-q="{esc((sym + " " + name).lower())}" data-n="{notional or 0}" data-t="{tv}" data-l="{liq}">'
                    f'<td><a href="{L[pg]}" target="_blank" rel="noopener" class="sym">{sym}</a></td><td>{name}</td><td>{size}</td>'
                    f'<td class="num">{tick}</td><td class="num">{tvs}</td><td class="num">{nv}</td>'
                    f'<td><span class="liq l{liq}">{LIQ[liq]}</span></td><td class="num">{HRS[hk]}</td><td class="num peak">{g["best"]}</td></tr>')
    s4 = section("table", "04 · 비교표", "계약 크기·틱 가치·유동성·거래 시간 (캘리 기준)",
        f'<div class="filters"><div class="chips" id="tchips" role="group" aria-label="카테고리">{chips}</div>'
        f'<label class="search" for="q">검색<input id="q" type="search" placeholder="예: 금, CL, 마이크로"></label>'
        f'<label class="search" for="sort">정렬<select id="sort"><option value="">카테고리 순</option><option value="n">명목가치 작은 순</option><option value="t">틱 가치 작은 순</option><option value="l">유동성 좋은 순</option></select></label></div>'
        '<div class="tbl big"><table><thead><tr><th>심볼</th><th>이름</th><th>계약 크기</th><th>최소 틱</th><th>틱 가치</th><th>명목가치 (현재)</th><th>유동성</th><th>거래 시간 (PT)</th><th>거래 몰리는 시간 (PT)</th></tr></thead>'
        f'<tbody id="rows">{"".join(rows)}</tbody></table></div>'
        '<p class="cap" id="count"></p>' +
        note("<b>15:00~14:00</b>은 전날 오후 3시에 열려 다음날 오후 2시에 닫힌다는 뜻이에요. 한 주는 일요일 15:00에 시작해 금요일 14:00에 끝나요. "
             "명목가치는 2026-10-22 IBKR 시세(외환은 현물 환율 환산)로 계산한 1계약 크기예요. TN·UB·KE·SR3·커피·오렌지주스는 시세를 함께 받지 않아 비워뒀어요. "
             "유동성은 거래량·미결제약정·호가를 보고 매긴 대략적인 5단계예요. 심볼을 누르면 설명 페이지가 열려요."))

    up = "".join(f'<li><span class="d">{d}</span><p>{t}</p>{f"<a href=\"{L[k]}\" target=\"_blank\" rel=\"noopener\">페이지 ↗</a>" if k else "<span></span>"}</li>' for d, t, k in UPCOMING)
    s5 = section("dates", "05 · 다가오는 일정", "앞으로 두 달 만기·롤오버 체크리스트",
        f'<ol class="tl">{up}</ol>' +
        note("실물 인도 상품은 첫 통지일보다 며칠 먼저 IBKR이 청산을 요구할 수 있어요. 정확한 날짜는 IBKR 계약 정보(Contract Info)에서 다시 확인하세요."))

    s6 = section("tips", "06 · 고르는 법", "캘리포니아에서 거래할 때 보면 좋은 기준",
        warn([(True, "아침이 본장", "05:30 지표부터 13:00 증시 마감까지가 거의 모든 선물의 최대 거래 시간이에요. 출근 전·오전에 집중하기 좋아요."),
              (False, "저녁엔 아시아 상품", f"퇴근 후 저녁({T(9, TK)}~)엔 엔·호주달러, 금·구리처럼 아시아 수요가 있는 상품이 움직여요. 다른 상품은 호가가 얇아요."),
              (False, "새벽 뉴스 조심", "유럽 시간(00:00~06:00)에 원유·유로·밀 뉴스가 자주 나와요. 자는 동안 포지션을 들고 있다면 손절 주문을 걸어두세요."),
              (False, "작게 시작하기", "마이크로가 있는 상품(MES·MNQ·MCL·MGC·M6E·MBT)은 1계약 수천~수만 달러라 연습하기 좋아요."),
              (False, "유동성 먼저", "'얇음'·'매우 얇음' 상품은 스프레드와 미끄러짐이 커요. 지정가 주문을 쓰고, 거래가 몰리는 시간에만 들어가세요."),
              (False, "실물 인도 확인", "원유·금속·곡물·소프트·국채·외환은 실물 인도. 지수·VIX·코인·돼지·비육우·마이크로 원유는 현금정산이에요.")]))

    extra_css = """<style>
:root{--night:#e4e8f0;--day:#f8f9fb;--tradebar:#b9c0cc;--hero1:#23406a;--hero2:#5b3f8c;--gold:#ffd88a}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--night:#0b0d11;--day:#20242b;--tradebar:#58606d;--hero1:#1b3354;--hero2:#3d2a63}}
:root[data-theme="dark"]{--night:#0b0d11;--day:#20242b;--tradebar:#58606d;--hero1:#1b3354;--hero2:#3d2a63}
main{max-width:1000px;gap:72px}
section>.eyebrow{align-self:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:99px;padding:3px 12px;letter-spacing:.04em}
h2{font-size:clamp(1.5rem,4vw,2rem)}
.lead.sm{font-size:.95rem}
/* hero */
.hero{flex-direction:row;flex-wrap:wrap;gap:24px;align-items:stretch;padding:32px;border-radius:24px;color:#fff;
  background:radial-gradient(120% 140% at 0% 0%,var(--hero1) 0%,var(--hero1) 35%,var(--hero2) 100%);position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-80px;top:-80px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.06);pointer-events:none}
.hero-txt{flex:3 1 420px;display:flex;flex-direction:column;gap:14px;min-width:0}
.hero .eyebrow{color:var(--gold)} .hero .hl{color:var(--gold)} .hero .lead{color:rgba(255,255,255,.86)} .hero .lead b{color:#fff}
.hero .toc a{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.22);color:#fff}
.hero .toc a:hover,.hero .toc a:focus-visible{border-color:var(--gold)}
.clock{flex:1 1 240px;min-width:0;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:2px;position:relative;z-index:1}
.clock small{font-size:.78rem;color:rgba(255,255,255,.75)}
.clock>b{font-family:var(--mono);font-weight:500;font-size:2.6rem;line-height:1.15;font-variant-numeric:tabular-nums}
.clock>span{font-size:.85rem;color:rgba(255,255,255,.8)}
.clock .open{margin-top:12px;display:flex;flex-direction:column;gap:6px}
#opennow{display:flex;flex-wrap:wrap;gap:6px}
#opennow span{font-size:.78rem;font-weight:600;padding:2px 9px;border-radius:99px;background:rgba(255,255,255,.16)}
#opennow span.off{opacity:.45;text-decoration:line-through}
/* category pages */
.cats{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.cat{background:var(--surface);border:1px solid var(--line);border-top:4px solid var(--cc);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:10px;min-width:0}
.cat h3{font-size:1.05rem;display:flex;align-items:center;gap:8px}
.cat h3 em{font-style:normal;font-family:var(--mono);font-size:.75rem;color:var(--cc);border:1px solid var(--cc);border-radius:99px;padding:0 7px}
.pgs{display:flex;flex-wrap:wrap;gap:6px}
.pg{display:flex;flex-direction:column;flex:1 1 130px;min-width:0;text-decoration:none;color:var(--fg);padding:9px 11px;border-radius:12px;background:var(--bg);border:1px solid transparent;transition:border-color .15s,transform .15s}
.pg:hover,.pg:focus-visible{border-color:var(--cc);outline:none;transform:translateY(-1px)}
.pg b{font-weight:800;font-size:.95rem}
.pg span{font-family:var(--mono);font-size:.76rem;color:var(--muted)}
/* tracks */
.track{position:relative;height:28px;border-radius:9px;min-width:0;
  background:linear-gradient(to right,var(--day) 0 16.67%,var(--night) 16.67% 66.67%,var(--day) 66.67%)}
.track i{position:absolute;display:block}
.track .tr{top:10px;height:8px;border-radius:4px;background:var(--tradebar)}
.track .pk{top:4px;height:20px;border-radius:6px}
.pk.us{background:var(--c1)} .pk.eu{background:var(--c2)} .pk.as{background:var(--c4)} .pk.sa{background:var(--c3)}
.pk.v1{opacity:.62} .pk.v0{opacity:.3}
.track .now{top:-3px;bottom:-3px;width:2px;margin-left:-1px;background:var(--alert);border-radius:1px;display:none}
.axis,.periods{position:relative;height:18px;font-size:.72rem;color:var(--muted);font-family:var(--mono)}
.axis span{position:absolute;top:2px;transform:translateX(-50%);white-space:nowrap}
.axis span:first-child{transform:none} .axis .end{right:0;transform:none}
.periods span{position:absolute;top:0;text-align:center;font-family:var(--body);font-weight:600;font-size:.72rem;overflow:hidden;white-space:nowrap}
.legend{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.8rem;color:var(--muted);align-items:center}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend .lv{font-style:italic}
.lg{display:inline-block;width:18px;height:10px;border-radius:3px}
.lg.tr{background:var(--tradebar);height:6px}
.lg.pk.us{background:var(--c1)} .lg.pk.eu{background:var(--c2)} .lg.pk.as{background:var(--c4)} .lg.pk.sa{background:var(--c3)}
.lg.now{width:2px;height:14px;background:var(--alert)}
.toolbar{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:flex-end}
.ref{display:flex;flex-direction:column;gap:4px;font-size:.8rem;color:var(--muted)}
.ref select,.search input,.search select{font:inherit;font-size:.92rem;padding:7px 10px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--fg)}
/* world chart */
.wc{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px 18px 10px;display:flex;flex-direction:column;gap:8px}
.wc-row{display:grid;grid-template-columns:150px 1fr;gap:12px;align-items:center}
.wc-row.head{margin-bottom:-4px}
.wl{display:flex;flex-direction:column;line-height:1.3;min-width:0}
.wl b{font-weight:800;font-size:.92rem} .wl span{font-size:.72rem;color:var(--muted)}
.wc-sep{font-size:.78rem;font-weight:700;color:var(--muted);border-top:1px dashed var(--line);padding-top:10px;margin-top:4px}
/* peak cards */
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:inherit;font-size:.82rem;border:1px solid var(--line);background:var(--surface);color:var(--fg);padding:4px 12px;border-radius:99px;cursor:pointer}
.chip.on{background:var(--c1);border-color:var(--c1);color:var(--surface)}
.chip:focus-visible,.search input:focus-visible,.search select:focus-visible,.ref select:focus-visible{outline:2px solid var(--c3);outline-offset:1px}
.pcs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:16px}
.pc{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:12px;min-width:0;position:relative}
.pc::before{content:"";position:absolute;left:0;top:18px;bottom:18px;width:4px;border-radius:0 4px 4px 0;background:var(--cc)}
.pc[hidden]{display:none}
.pc-h{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.pc-h h3{font-size:1.3rem;margin-top:2px}
.ctag{font-size:.72rem;font-weight:800;color:var(--cc)}
.syms{display:block;font-family:var(--mono);font-size:.78rem;color:var(--muted)}
.more{font-size:.8rem;white-space:nowrap;text-decoration:none;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:2px 10px}
.more:hover,.more:focus-visible{color:var(--fg);border-color:var(--cc);outline:none}
.best{display:flex;flex-direction:column;background:var(--bg);border-radius:12px;padding:10px 12px}
.best small{font-size:.75rem;color:var(--muted)}
.best b{font-family:var(--mono);font-weight:500;font-size:1.1rem;font-variant-numeric:tabular-nums}
.best span{font-size:.76rem;color:var(--muted)}
.pc-t{display:flex;flex-direction:column;gap:2px}
.why{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.why li{display:grid;grid-template-columns:12px 1fr;gap:10px;align-items:start;font-size:.92rem;line-height:1.65}
.why .dot{width:10px;height:10px;border-radius:50%;margin-top:.5em}
.dot.us{background:var(--c1)} .dot.eu{background:var(--c2)} .dot.as{background:var(--c4)} .dot.sa{background:var(--c3)}
.why b{font-weight:800}
.tz{font-family:var(--mono);font-size:.92em;font-weight:500;background:var(--bg);border-radius:5px;padding:0 4px;white-space:nowrap}
.best .tz{background:none;padding:0;font-size:1em}
/* table */
.filters{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end}
#tchips{flex-basis:100%}
.search{display:flex;flex-direction:column;gap:4px;font-size:.8rem;color:var(--muted);min-width:0;flex:1 1 180px}
.tbl.big{max-height:660px;overflow:auto;border:1px solid var(--line);border-radius:16px;background:var(--surface)}
.tbl.big table{font-size:.86rem}
.tbl.big thead th{position:sticky;top:0;background:var(--surface);z-index:1;box-shadow:inset 0 -1px var(--line)}
.tbl.big td,.tbl.big th{padding:9px 11px;white-space:nowrap}
.tbl.big tbody tr:hover{background:var(--bg)}
td.peak .tz{background:none;padding:0}
.sym{font-family:var(--mono);font-weight:500;color:var(--c1);text-decoration:none}
.sym:hover{text-decoration:underline}
.liq{font-size:.75rem;font-weight:800;padding:2px 8px;border-radius:99px;white-space:nowrap}
.l5{background:var(--c2-soft);color:var(--c2)} .l4{background:var(--c1-soft);color:var(--c1)} .l3{background:var(--c4-soft);color:var(--c4)}
.l2{background:var(--c3-soft);color:var(--c3)} .l1{background:var(--alert-soft);color:var(--alert)}
/* timeline */
.tl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;border-left:2px solid var(--line);margin-left:6px}
.tl li{display:grid;grid-template-columns:96px 1fr auto;gap:12px;align-items:baseline;padding:10px 0 10px 18px;position:relative}
.tl li::before{content:"";position:absolute;left:-7px;top:17px;width:12px;height:12px;border-radius:50%;background:var(--surface);border:2px solid var(--c1)}
.tl .d{font-family:var(--mono);font-size:.85rem;color:var(--c1);white-space:nowrap}
.tl p{font-size:.94rem} .tl a{font-size:.8rem;white-space:nowrap}
@media (max-width:640px){
  .hero{padding:22px;border-radius:20px}
  .clock{flex-basis:100%}
  .wc{padding:14px 12px 8px}
  .wc-row{grid-template-columns:78px 1fr;gap:8px}
  .wl span{display:none}
  .axis span:nth-child(even){display:none}
  .periods span{font-size:.62rem}
  .tl li{grid-template-columns:1fr;gap:2px}
}
</style>"""

    script = """<script>
(function(){
  var PT='America/Los_Angeles';
  var WORLD=__WORLD__, TYPES=__TYPES__;
  function parts(tz,d){
    var o={}; new Intl.DateTimeFormat('en-US',{timeZone:tz,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',weekday:'short'})
      .formatToParts(d).forEach(function(p){o[p.type]=p.value;}); return o;
  }
  function off(tz,d){ var p=parts(tz,d); var u=Date.UTC(+p.year,+p.month-1,+p.day,(+p.hour)%24,+p.minute); return Math.round((u-Math.floor(d.getTime()/60000)*60000)/900000)/4; }
  var DOW={Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6};
  function refDate(){ var v=document.getElementById('ref').value; return v==='w'?new Date(Date.UTC(2026,11,1,20)):v==='s'?new Date(Date.UTC(2027,6,1,20)):new Date(); }
  function toPT(h,tz,d){ var x=h-(off(tz,d)-off(PT,d)); return ((x%24)+24)%24; }
  function hm(h){ var m=Math.round(h*60)%1440; return ('0'+Math.floor(m/60)).slice(-2)+':'+('0'+m%60).slice(-2); }
  function seg(a,b,cls){
    var oa=(((a-14)%24)+24)%24, ln=(((b-a)%24)+24)%24||24, out=[[oa,Math.min(ln,24-oa)]];
    if(oa+ln>24) out.push([0,oa+ln-24]);
    return out.map(function(s){return '<i class="'+cls+'" style="left:'+(s[0]/24*100).toFixed(3)+'%;width:'+(s[1]/24*100).toFixed(3)+'%"></i>';}).join('');
  }
  function render(){
    var d=refDate();
    document.querySelectorAll('.track').forEach(function(t){
      var b=JSON.parse(t.getAttribute('data-b')||'[]'), bl=t.querySelector('.bl');
      bl.innerHTML=b.map(function(x){return seg(toPT(x[0],x[2],d),toPT(x[1],x[2],d),'pk '+x[3]+' v'+x[4]);}).join('');
    });
    document.querySelectorAll('.tz').forEach(function(s){ s.textContent=hm(toPT(parseFloat(s.dataset.h),s.dataset.tz,d)); });
  }
  function inSegs(segs,h,dow){
    return segs.some(function(s){ var a=s[0],b=s[1];
      if(a<b) return dow>=1&&dow<=5&&h>=a&&h<b;
      return (h>=a&&dow>=0&&dow<=4)||(h<b&&dow>=1&&dow<=5); });
  }
  function tick(){
    var now=new Date(), p=parts(PT,now), h=(+p.hour%24)+(+p.minute)/60, dow=DOW[p.weekday];
    document.getElementById('ptnow').textContent=('0'+(+p.hour%24)).slice(-2)+':'+p.minute;
    var ab=new Intl.DateTimeFormat('en-US',{timeZone:PT,timeZoneName:'short'}).formatToParts(now).filter(function(x){return x.type==='timeZoneName';})[0];
    var ko=new Intl.DateTimeFormat('ko-KR',{timeZone:PT,month:'long',day:'numeric',weekday:'short'}).format(now);
    document.getElementById('ptday').textContent=ko+(ab?' · '+ab.value:'');
    var html=WORLD.map(function(w){ var q=parts(w[1],now), lh=(+q.hour%24)+(+q.minute)/60, ld=DOW[q.weekday];
      var on=ld>=1&&ld<=5&&lh>=w[2]&&lh<w[3]; return '<span class="'+(on?'':'off')+'">'+w[0]+'</span>'; });
    html=html.concat(TYPES.map(function(t){ return '<span class="'+(inSegs(t[1],h,dow)?'':'off')+'">'+t[0]+'</span>'; }));
    document.getElementById('opennow').innerHTML=html.join('');
    var left=((((h-14)%24)+24)%24)/24*100;
    document.querySelectorAll('.track .now').forEach(function(n){ n.style.left=left.toFixed(3)+'%'; n.style.display='block'; });
  }
  document.getElementById('ref').addEventListener('input',render);
  render(); tick(); setInterval(tick,30000);

  function chipGroup(id,fn){ var box=document.getElementById(id), cur='all';
    box.querySelectorAll('.chip').forEach(function(b){ b.addEventListener('click',function(){
      box.querySelectorAll('.chip').forEach(function(x){x.classList.remove('on');x.setAttribute('aria-pressed','false');});
      b.classList.add('on'); b.setAttribute('aria-pressed','true'); cur=b.dataset.cat; fn(cur); }); });
    return function(){return cur;};
  }
  chipGroup('pchips',function(c){ document.querySelectorAll('.pc').forEach(function(p){ p.hidden=!(c==='all'||p.dataset.cat===c); }); });
  var tb=document.getElementById('rows'), orig=Array.prototype.slice.call(tb.rows);
  var tcat=chipGroup('tchips',function(){apply();});
  function apply(){
    var q=document.getElementById('q').value.trim().toLowerCase(), s=document.getElementById('sort').value, c=tcat();
    var list=orig.slice();
    if(s==='n') list.sort(function(a,b){return (+a.dataset.n||1e12)-(+b.dataset.n||1e12);});
    if(s==='t') list.sort(function(a,b){return a.dataset.t-b.dataset.t;});
    if(s==='l') list.sort(function(a,b){return b.dataset.l-a.dataset.l;});
    var shown=0;
    list.forEach(function(tr){ var ok=(c==='all'||tr.dataset.cat===c)&&(!q||tr.dataset.q.indexOf(q)>=0); tr.hidden=!ok; if(ok)shown++; tb.appendChild(tr); });
    document.getElementById('count').textContent=shown+'개 계약 표시 중';
  }
  ['q','sort'].forEach(function(id){ document.getElementById(id).addEventListener('input',apply); });
  apply();
})();
</script>"""
    world_js = json.dumps([[n, tz, a, b] for n, _, (a, b, tz) in WORLD], ensure_ascii=False)
    types_js = json.dumps([["CME", [[15, 14]]], ["곡물", [[17, 5.75], [6.5, 11.333]]], ["ICE 소프트", [[0.5, 10.5]]], ["축산", [[6.5, 11.083]]]], ensure_ascii=False)
    script = script.replace("__WORLD__", world_js).replace("__TYPES__", types_js)
    return HEAD % "미국 선물 한눈에 보기" + css(PAL) + extra_css + "\n<main>\n" + H + "\n" + "\n".join([s1, s2, s3, s4, s5, s6]) + "\n</main>\n" + script
