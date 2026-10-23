# Shared builder for the one-currency FX futures pages (6E, 6J, 6B, 6A, 6C, 6S, DX).
from lib import *

# spot rates from IBKR IDEALPRO, 2026-10-21 ~20:20 PT
EUR, JPY, GBP, AUD, CAD, CHF, DXF = 1.124975, 157.71, 1.34045, 0.701675, 1.40315, 0.82245, 101.435
QCAP = ("IBKR 시세, 2026-10-21 저녁 8시 20분쯤(캘리포니아 시간). CME 외환 선물 시세는 이 연결에서 바로 조회되지 않아서 "
        "같은 시각 IBKR 현물 환율(IDEALPRO)을 선물 표기로 바꿔 보여드려요. 12월물 선물은 두 나라 금리 차이만큼 현물과 조금 달라요.")
OVERVIEW = "https://claude.ai/artifact/Gx253oiVqCZKXsqpeUCX9c"

def r(x, t): return round(round(x / t) * t, 7)

TOC = [("story", "이 통화 이야기"), ("quote", "가격 읽는 법"), ("drivers", "가격 요인"), ("calendar", "1년 달력"), ("who", "누가 거래하나"),
       ("specs", "IBKR 계약 정보"), ("calc", "손익 계산기"), ("hours", "캘리 시간 · 거래 몰리는 시간"), ("cautions", "주의점")]

def quote_section(c):
    if c.get("quote_html"):
        return section("quote", "2. 가격 읽는 법", c["quote_h2"], c["quote_html"])
    if not c["inverse"]:
        body = (table(["뉴스 환율", "선물 가격", "의미"],
                      [[f"{c['pair']} {v:.{c['dec_news']}f}", f"{v:.{c['dec']}f}", t] for v, t in c["examples"]], numcols=(0, 1)) + "\n" +
                note(f"{c['name']}는 뉴스 환율과 선물 가격이 <b>같은 숫자, 같은 방향</b>이에요. {c['name']} 강세 = {c['sym']} 상승. "
                     f"선물 쪽 소수 자릿수가 하나 더 많을 뿐이에요."))
        return section("quote", "2. 가격 읽는 법", "뉴스 환율 그대로 읽으면 돼요", body)
    rows = [[f"{c['pair']} {v:,.{c['dec_news']}f}", f"{1 / v:.{c['dec']}f}", t] for v, t in c["examples"]]
    body = (table(["뉴스 환율", f"{c['sym']} 가격 (1 ÷ 환율)", "의미"], rows, numcols=(0, 1)) + "\n" +
            note(f"CME는 미국 거래소라 모든 통화를 <b>'외화 1단위 = 몇 달러'</b>로 표시해요. 그런데 뉴스는 {c['pair']}처럼 '1달러 = 몇 {c['unit']}'로 말하죠. "
                 f"그래서 {c['sym']}는 뉴스 숫자의 <b>역수</b>이고 방향도 <b>반대</b>예요. 뉴스 숫자가 오르면({c['name']} 약세) {c['sym']}는 내려가요."))
    return section("quote", "2. 가격 읽는 법", "뉴스 환율과 거꾸로 움직여요", body)

def build_fx(c):
    H = header(c["eyebrow"], c["h1"], c["lead"], c["answer"], c["quotes"], c.get("qcap", QCAP), TOC)
    H = H.replace('<nav class="toc"', f'<p class="back"><a href="{OVERVIEW}" target="_blank" rel="noopener">← 외환 선물 개요 (7개 통화 한눈에)</a></p>\n  <nav class="toc"', 1)
    s1 = section("story", "1. 이 통화 이야기", c["story_h2"], c["story"])
    s2 = quote_section(c)
    s3 = section("drivers", "3. 가격을 흔드는 것들", c["drivers_h2"], drivers(c["drivers"]))
    s4 = section("calendar", "4. 1년 동안 언제 뭘 봐야 하나", c["cal_h2"], fig(calendar(c["cal"], c["cal_label"], today=(10, 23))) + "\n" + cap(c["cal_cap"]))
    s5 = section("who", "5. 이 시장은 왜 존재하나", c["who_h2"], fig(hedge(*c["hedge"]), narrow=True) + "\n" + cards(c["who"]))
    s6 = section("specs", "6. 트레이딩할 때 알아야 할 것", "IBKR 계약 기본 정보", specs(*c["specs"]) + "\n" + note(c["spec_note"]))
    s7 = section("calc", "7. 직접 눌러보기", c["calc_h2"], calc(c["calc"], c["presets"], c["calc_unit"], c["calc_note"]))
    s8 = section("hours", "8. 캘리포니아 시간으로 언제 열리나", c["hours_h2"],
        fig(hours(c["sessions"], c.get("tz", "CT"), c.get("foot_soft", "CME 글로벡스 (매일 14:00~15:00 쉬는 시간)"), c["foot_solid"], c["hours_alt"])) + "\n" +
        cap(c["hours_cap"]) + "\n" + "<h3>거래가 몰리는 시간과 그 이유</h3>\n" + cards(c["peaks"]))
    s9 = section("cautions", "9. 주의점", "들어가기 전에 꼭 알아둘 것", warn(c["cautions"]))
    return page(c["title"], c["pal"], H, [s1, s2, s3, s4, s5, s6, s7, s8, s9], fun(*c["fun"]))
