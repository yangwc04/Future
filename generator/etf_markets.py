# Definitions for every "관련 ETF" page. Rows: (ticker, short Korean name, leverage, structure key, memo)
import importlib, os
from etflib import LEV_DECAY, ROLL, K1, EXT, THIN, ETN_RISK

_HERE = os.path.dirname(os.path.abspath(__file__))
_L = dict(l.split() for l in open(os.path.join(_HERE, "..", "links.txt")) if l.strip())
_L.update(oj="https://claude.ai/artifact/Ceb2BiwFY7LJci991bjsij", coffee="https://claude.ai/artifact/1AmSgYykjSvYAj6gme8tMU",
          rice="https://claude.ai/artifact/9teMajEtW3c7PpwWv6QWBD")

def P(mod): return importlib.import_module(mod).PAL

def M(key, links_key, mod, name, fut, h1, lead, answer, groups, picks, cautions, **kw):
    d = dict(key=key, back=_L[links_key], back_name=name, pal=P(mod), name=name, fut=fut, h1=h1, lead=lead, answer=answer,
             groups=groups, picks=picks, cautions=cautions)
    d.update(kw)
    return d

def G(title, rows, note=None): return dict(title=title, rows=rows, note=note)

# ------------------------------------------------------------------ equity
EQ_SP = [("SPY", "SPDR S&P 500", 1, "stock", "세계에서 거래가 가장 많은 ETF. 옵션도 제일 활발"),
         ("VOO", "뱅가드 S&P 500", 1, "stock", "보수 0.03%, 오래 들고 갈 때"),
         ("IVV", "아이셰어즈 S&P 500", 1, "stock", "VOO와 거의 같음"),
         ("SSO", "ProShares Ultra S&P500", 2, "swap", ""),
         ("UPRO", "ProShares UltraPro S&P500", 3, "swap", ""),
         ("SPXL", "Direxion S&P500 Bull 3X", 3, "swap", "3배 롱 중 거래 1위"),
         ("SH", "ProShares Short S&P500", -1, "swap", "-1배 숏 대표"),
         ("SDS", "ProShares UltraShort S&P500", -2, "swap", ""),
         ("SPXU", "ProShares UltraPro Short S&P500", -3, "swap", ""),
         ("SPXS", "Direxion S&P500 Bear 3X", -3, "swap", "3배 숏 중 거래 1위")]
EQ_NQ = [("QQQ", "인베스코 QQQ", 1, "stock", "나스닥100 대표, 거래대금 세계 2위급"),
         ("QQQM", "인베스코 나스닥100", 1, "stock", "QQQ보다 보수 낮고 주가 낮음"),
         ("QLD", "ProShares Ultra QQQ", 2, "swap", ""),
         ("TQQQ", "ProShares UltraPro QQQ", 3, "swap", "레버리지 ETF 중 거래 1위"),
         ("PSQ", "ProShares Short QQQ", -1, "swap", ""),
         ("QID", "ProShares UltraShort QQQ", -2, "swap", ""),
         ("SQQQ", "ProShares UltraPro Short QQQ", -3, "swap", "인버스 중 거래 1위")]
EQ_YM = [("DIA", "SPDR 다우존스", 1, "stock", ""),
         ("DDM", "ProShares Ultra Dow30", 2, "swap", "거래 적음"),
         ("UDOW", "ProShares UltraPro Dow30", 3, "swap", ""),
         ("DOG", "ProShares Short Dow30", -1, "swap", ""),
         ("DXD", "ProShares UltraShort Dow30", -2, "swap", ""),
         ("SDOW", "ProShares UltraPro Short Dow30", -3, "swap", "")]
EQ_RTY = [("IWM", "아이셰어즈 러셀2000", 1, "stock", "러셀 대표, 옵션도 활발"),
          ("VTWO", "뱅가드 러셀2000", 1, "stock", ""),
          ("UWM", "ProShares Ultra Russell2000", 2, "swap", ""),
          ("TNA", "Direxion Small Cap Bull 3X", 3, "swap", "3배 롱 대표"),
          ("URTY", "ProShares UltraPro Russell2000", 3, "swap", ""),
          ("RWM", "ProShares Short Russell2000", -1, "swap", "AUM 대비 거래 많음"),
          ("TWM", "ProShares UltraShort Russell2000", -2, "swap", ""),
          ("TZA", "Direxion Small Cap Bear 3X", -3, "swap", "3배 숏 대표"),
          ("SRTY", "ProShares UltraPro Short Russell2000", -3, "swap", "")]

def markets():
    out = []
    out.append(M("equity", "index", "p01_index", "주가지수", "ES · NQ · YM · RTY",
        '주가지수 선물 대신<br><span class="hl">ETF로 사면</span> 뭐가 있을까?',
        "S&P500(ES), 나스닥100(NQ), 다우(YM), 러셀2000(RTY) 선물마다 같은 지수를 따라가는 미국 ETF가 1배, 2배, 3배, 그리고 인버스까지 다 있어요. 지수 ETF는 선물을 사는 게 아니라 <b>주식을 직접 담거나 스왑</b>으로 지수를 따라가요.",
        "<p><strong>한 줄 정답:</strong> 1배는 <b>SPY · QQQ · DIA · IWM</b>, 3배 롱은 <b>SPXL · TQQQ · UDOW · TNA</b>, 3배 숏은 <b>SPXS · SQQQ · SDOW · TZA</b>가 각 지수에서 거래가 제일 많아요.</p>"
        "<p>주가지수 선물만 담아서 운용하는 ETF는 사실상 없어요. 그래도 지수가 같으니 움직임은 선물과 거의 같아요(배당과 금리 차이만큼만 달라요).</p>",
        [G("S&P 500 · ES / MES", EQ_SP), G("나스닥 100 · NQ / MNQ", EQ_NQ), G("다우존스 30 · YM / MYM", EQ_YM),
         G("러셀 2000 · RTY / M2K", EQ_RTY, "러셀 표는 10/28 조사 결과를 오늘 다시 조회해서 갱신했어요.")],
        [("t-3", "1배", "그냥 지수를 사고 싶다면", "<b>SPY</b>(S&P), <b>QQQ</b>(나스닥), <b>DIA</b>(다우), <b>IWM</b>(러셀). 오래 들고 갈 거면 보수가 싼 VOO · QQQM · VTWO도 좋아요."),
         ("t-1", "3배 롱", "하루 이틀 강하게 롱", "<b>SPXL</b> · <b>TQQQ</b> · <b>UDOW</b> · <b>TNA</b>. 같은 3배라도 거래가 많은 쪽이 스프레드가 좁아요."),
         ("t-spec", "인버스", "하락에 베팅·헤지", "-1배는 <b>SH · PSQ · DOG · RWM</b>, -3배는 <b>SPXS · SQQQ · SDOW · TZA</b>."),
         ("t-4", "선물이 나을 때", "며칠 이상 레버리지", "레버리지를 오래 들고 갈 거면 MES · MNQ · MYM · M2K 마이크로 선물이 매일 리셋이 없어서 더 깔끔해요.")],
        [LEV_DECAY, EXT, (False, "같은 지수라도 3배는 3배가 아님", "TQQQ를 한 달 들고 있으면 나스닥이 10% 올라도 30%가 아니라 그보다 적거나 많을 수 있어요. 매일 3배를 다시 맞추기 때문이에요."), THIN,
         (False, "배당", "SPY·QQQ 같은 1배 ETF는 배당을 주지만 선물은 배당이 가격에 미리 빠져 있어요. 그래서 선물과 ETF 가격 차이가 조금 나요.")],
        fun=("📈 보너스: ES 1계약 = SPY 몇 주?", "ES는 S&P500 × $50이라 지수 7,600이면 약 $38만이에요. SPY 한 주가 지수의 약 1/10이니 ES 1계약은 SPY 약 500주, MES 1계약은 약 50주와 비슷한 크기예요.")))

    # ------------------------------------------------------------------ rates
    out.append(M("rates", "rates", "p02_rates", "국채·SOFR", "ZT · ZF · ZN · ZB · SR3",
        '국채 선물 대신<br><span class="hl">채권 ETF</span>는 뭐가 있을까?',
        "국채 선물은 만기 구간(2년·5년·10년·30년)마다 따라가는 ETF가 있어요. 대부분은 <b>국채를 직접 사서 들고 있는</b> 구조이고, 레버리지·인버스 상품은 스왑과 선물을 섞어요.",
        "<p><strong>한 줄 정답:</strong> 10년물(ZN)은 <b>IEF</b>, 30년물(ZB·UB)은 <b>TLT</b>가 기본이에요. 금리 상승(채권 가격 하락)에 베팅하려면 <b>TBT</b>(-2배 장기)나 <b>TMV</b>(-3배 장기), 10년 구간은 <b>TYO</b>(-3배)예요.</p>"
        "<p>SOFR 선물(SR3)은 '3개월 금리' 자체라 따라가는 ETF가 없어요. 대신 <b>SGOV · BIL</b> 같은 초단기 국채 ETF가 비슷한 금리를 그대로 받아요.</p>",
        [G("10년 구간 · ZN / TN", [("IEF", "아이셰어즈 7-10년 국채", 1, "bond", "ZN과 가장 비슷한 대표 ETF"),
                                ("UTEN", "F/m 10년 국채", 1, "bond", "10년물 한 종목만 담음"),
                                ("UST", "ProShares Ultra 7-10년", 2, "mix", "거래 얇음"),
                                ("TYD", "Direxion 7-10년 Bull 3X", 3, "swap", ""),
                                ("PST", "ProShares UltraShort 7-10년", -2, "mix", ""),
                                ("TYO", "Direxion 7-10년 Bear 3X", -3, "swap", "")]),
         G("30년 구간 · ZB / UB", [("TLT", "아이셰어즈 20년+ 국채", 1, "bond", "장기채 대표, 거래 매우 많음"),
                                ("UBT", "ProShares Ultra 20년+", 2, "mix", ""),
                                ("TMF", "Direxion 20년+ Bull 3X", 3, "swap", "장기채 3배 롱 대표"),
                                ("TBF", "ProShares Short 20년+", -1, "mix", ""),
                                ("TBT", "ProShares UltraShort 20년+", -2, "mix", "금리 상승 베팅 대표"),
                                ("TMV", "Direxion 20년+ Bear 3X", -3, "swap", "")]),
         G("단기 · ZT / ZF / SR3", [("SHY", "아이셰어즈 1-3년 국채", 1, "bond", "ZT(2년) 구간"),
                                  ("IEI", "아이셰어즈 3-7년 국채", 1, "bond", "ZF(5년) 구간"),
                                  ("SGOV", "아이셰어즈 0-3개월 국채", 1, "bond", "SOFR 금리와 비슷한 이자"),
                                  ("BIL", "SPDR 1-3개월 T-Bill", 1, "bond", "")],
           "SR3는 금리 자체를 사고파는 선물이라 대신할 ETF가 없어요. 초단기 국채 ETF는 금리를 '받는' 상품이지 금리 변화에 베팅하는 상품이 아니에요.")],
        [("t-3", "1배", "10년물 대신", "<b>IEF</b>. 듀레이션(금리 민감도)이 ZN과 비슷해서 같이 움직여요."),
         ("t-3", "1배", "30년물 대신", "<b>TLT</b>. 거래가 아주 많고 옵션도 활발해요."),
         ("t-spec", "금리 상승 베팅", "채권 가격 하락", "<b>TBT</b>(-2배 장기), <b>TMV</b>(-3배 장기), <b>TYO</b>(-3배 10년)."),
         ("t-1", "금리 하락 베팅", "채권 가격 상승", "<b>TMF</b>(3배 장기)가 거래가 제일 많아요. 10년 구간은 <b>TYD</b>.")],
        [LEV_DECAY, (False, "선물과 듀레이션이 달라요", "ZN은 '가장 싸게 넘길 수 있는 국채(CTD)' 기준이라 듀레이션이 약 6~7년, IEF는 약 7년이에요. 비슷하지만 똑같지는 않아요."),
         (False, "분배금", "채권 ETF는 매달 이자를 분배금으로 줘요. 선물은 이자가 가격에 녹아 있어요."), THIN, EXT],
        fun=("🏦 보너스: ZN 1계약 = IEF 몇 주?", "ZN은 액면 $10만이고 가격 약 110이면 명목가치 약 $11만이에요. IEF 한 주가 약 $95 안팎이니 ZN 1계약은 IEF 약 1,150주와 금리 노출이 비슷해요(듀레이션까지 맞추면 조금 달라져요).")))

    # ------------------------------------------------------------------ FX
    FX = {
        "eur": ("p03a_eur", "유로", "6E · M6E", [("FXE", "인베스코 유로 트러스트", 1, "cash", "유로 예금을 그대로 보유"),
                                               ("ULE", "ProShares Ultra Euro", 2, "fwd", "거래 매우 얇음"),
                                               ("EUO", "ProShares UltraShort Euro", -2, "fwd", "유로 약세(달러 강세) 베팅")]),
        "jpy": ("p03b_jpy", "엔화", "6J · MJY", [("FXY", "인베스코 엔화 트러스트", 1, "cash", "엔 예금을 그대로 보유"),
                                               ("YCL", "ProShares Ultra Yen", 2, "fwd", "거래 얇음"),
                                               ("YCS", "ProShares UltraShort Yen", -2, "fwd", "엔 약세 베팅")]),
        "gbp": ("p03c_gbp", "파운드", "6B · M6B", [("FXB", "인베스코 파운드 트러스트", 1, "cash", "파운드는 레버리지 ETF가 없어요")]),
        "aud": ("p03d_aud", "호주달러", "6A · M6A", [("FXA", "인베스코 호주달러 트러스트", 1, "cash", "레버리지 ETF 없음")]),
        "cad": ("p03e_cad", "캐나다달러", "6C · MCD", [("FXC", "인베스코 캐나다달러 트러스트", 1, "cash", "레버리지 ETF 없음")]),
        "chf": ("p03f_chf", "스위스프랑", "6S · MSF", [("FXF", "인베스코 스위스프랑 트러스트", 1, "cash", "레버리지 ETF 없음")]),
        "dx": ("p03g_dx", "달러인덱스", "DX", [("UUP", "인베스코 DB 달러 강세", 1, "fut", "DX 선물을 직접 보유"),
                                         ("UDN", "인베스코 DB 달러 약세", -1, "fut", "DX 선물을 매도"),
                                         ("USDU", "위즈덤트리 달러 강세", 1, "fwd", "DX와 다른 바스켓(블룸버그 달러지수)")]),
    }
    for k, (mod, nm, fut, rows) in FX.items():
        lev_ok = any(r[2] != 1 for r in rows)
        if k == "dx":
            ans = ("<p><strong>한 줄 정답:</strong> <b>UUP</b>가 ICE 달러인덱스(DX) 선물을 직접 사서 들고 있어요. 달러 약세 쪽은 <b>UDN</b>이에요.</p>"
                   "<p>레버리지 달러인덱스 ETF는 없어요. 2배·3배로 달러에 베팅하려면 DX 선물을 직접 하거나 EUO(유로 -2배)처럼 통화별 상품을 쓰는 방법이 있어요.</p>")
        elif lev_ok:
            ans = (f"<p><strong>한 줄 정답:</strong> 1배는 <b>{rows[0][0]}</b>(인베스코 커런시셰어즈)가 {nm}를 은행 예금으로 들고 있어서 {fut.split()[0]} 선물과 거의 같이 움직여요. "
                   f"2배·-2배는 ProShares 상품이 있지만 거래가 적어요.</p>"
                   "<p>통화 ETF는 선물보다 훨씬 덜 거래돼요. 외환은 하루 24시간 움직이는데 ETF는 미국 주식시장 시간에만 거래되기 때문이에요.</p>")
        else:
            ans = (f"<p><strong>한 줄 정답:</strong> {nm}는 <b>{rows[0][0]}</b> 하나뿐이에요. 1배 상품만 있고 레버리지·인버스 ETF는 미국에 없어요.</p>"
                   f"<p>{rows[0][0]}는 {nm} 예금을 그대로 들고 있어서 환율과 거의 같이 움직이지만 거래량이 작아요. 레버리지나 숏을 원하면 {fut.split()[-1]} 마이크로 선물이 훨씬 편해요.</p>")
        out.append(M(k, k, mod, nm, fut, f'{nm} 선물 대신<br><span class="hl">ETF로 하면</span> 뭐가 있을까?',
            f"{nm} 선물({fut})과 같은 방향으로 움직이는 미국 상장 ETF를 모았어요. 통화 ETF는 대부분 <b>그 통화를 예금으로 들고 있거나</b>, 은행과 맺은 선도계약으로 배수를 맞춰요.",
            ans, [G(f"{nm} 관련 ETF", rows)],
            [("t-3", "1배", f"{nm} 강세", f"<b>{rows[0][0]}</b>. 예금 이자가 붙고 환율을 그대로 따라가요.")] +
            ([("t-spec", "반대 방향", f"{nm} 약세", f"<b>{[r for r in rows if r[2] < 0][0][0]}</b>. 거래가 많지는 않으니 지정가로 넣으세요.")] if any(r[2] < 0 for r in rows) else []) +
            [("t-4", "선물이 나을 때", "레버리지 · 숏 · 밤 시간", f"{fut.split()[-1]} 마이크로 선물은 아시아·유럽 시간에도 거래돼서, 캘리포니아 밤에 환율이 크게 움직일 때도 바로 대응할 수 있어요.")],
            [EXT, THIN] + ([LEV_DECAY] if lev_ok else []) + [(False, "역수 표기 주의", "엔·스위스프랑·캐나다달러는 뉴스 환율(USD/JPY 등)과 선물·ETF가 반대로 움직여요. FXY는 엔이 강해질 때(USD/JPY가 내려갈 때) 올라요.")],
            fwd=True))

    # FX overview: all currencies on one page
    fx_rows = []
    for k, (mod, nm, fut, rows) in FX.items():
        fx_rows.append(G(f"{nm} · {fut}", rows))
    out.append(M("fx", "fx", "p03_fx", "외환", "6E · 6J · 6B · 6A · 6C · 6S · DX",
        '외환 선물 대신<br><span class="hl">통화 ETF</span>는 뭐가 있을까?',
        "통화마다 1배 ETF는 하나씩 있고, 레버리지·인버스는 유로·엔·달러인덱스에만 있어요. 통화별 자세한 내용은 각 통화 페이지의 '관련 ETF 보기'에서도 볼 수 있어요.",
        "<p><strong>한 줄 정답:</strong> 통화 ETF 중 거래가 제일 많은 건 <b>UUP</b>(달러인덱스)와 <b>FXY</b>(엔)·<b>FXE</b>(유로)예요. 나머지 통화(FXB·FXA·FXC·FXF)는 거래가 적어요.</p>"
        "<p>외환은 24시간 시장이라 ETF보다 선물(특히 마이크로 선물)이 훨씬 유동성이 좋아요.</p>",
        fx_rows,
        [("t-3", "달러 강세", "달러 전체", "<b>UUP</b>. DX 선물을 직접 들고 있어요."),
         ("t-spec", "엔 약세 · 유로 약세", "-2배", "<b>YCS</b>(엔 -2배), <b>EUO</b>(유로 -2배)."),
         ("t-4", "선물이 나을 때", "거의 항상", "외환 ETF는 거래가 적어요. M6E · MJY 같은 마이크로 선물이 스프레드도 좁고 밤에도 거래돼요.")],
        [EXT, THIN, LEV_DECAY], fwd=True))

    # ------------------------------------------------------------------ crude
    out.append(M("crude", "crude", "p04_crude", "원유", "CL · MCL · BZ",
        '원유 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "원유는 실물을 쌓아둘 수 없어서 원유 ETF는 전부 <b>선물을 사서 매달 굴리는</b> 구조예요. 그래서 이 페이지의 상품은 진짜로 CL·BZ 선물과 직접 연결돼 있어요.",
        "<p><strong>한 줄 정답:</strong> WTI 1배는 <b>USO</b>, 브렌트는 <b>BNO</b>, 2배 롱은 <b>UCO</b>, 2배 숏은 <b>SCO</b>가 기본이에요.</p>"
        "<p>USO는 근월물 위주, USL은 12개월 월물에 나눠 담아서 롤오버 충격이 작아요. DBO는 콘탱고가 덜한 월물을 골라 담아요.</p>",
        [G("원유 선물 보유 ETF", [("USO", "United States Oil Fund", 1, "fut", "WTI 대표. 근월물 위주"),
                              ("BNO", "United States Brent Oil", 1, "fut", "브렌트(BZ) 선물"),
                              ("USL", "United States 12 Month Oil", 1, "fut", "12개 월물에 분산"),
                              ("DBO", "인베스코 DB 원유", 1, "fut", "롤 비용이 적은 월물 선택"),
                              ("OILK", "ProShares K-1 Free 원유", 1, "fut", "K-1 없음, 3개 월물 분산"),
                              ("UCO", "ProShares Ultra 원유", 2, "mix", "2배 롱 대표"),
                              ("SCO", "ProShares UltraShort 원유", -2, "mix", "2배 숏 대표")]),
         G("참고: 정유·에너지 회사 주식", [("XLE", "에너지 섹터 SPDR", 1, "eq", "엑슨·셰브론 등. 원유 가격과 다르게 움직일 때가 많음")])],
        [("t-3", "1배", "WTI 따라가기", "<b>USO</b>. 거래가 제일 많아요. 오래 들고 갈 거면 롤 비용이 적은 <b>USL</b>이나 <b>DBO</b>."),
         ("t-1", "2배 롱", "단기 상승 베팅", "<b>UCO</b>."), ("t-spec", "2배 숏", "단기 하락 베팅", "<b>SCO</b>."),
         ("t-4", "선물이 나을 때", "밤 시간 · 정확한 가격", "원유는 OPEC 회의나 재고 발표 때 밤에 크게 움직여요. MCL 마이크로 선물(100배럴)이면 소액으로 바로 대응할 수 있어요.")],
        [ROLL, K1, LEV_DECAY, (True, "2020년 마이너스 유가", "2020년 4월 WTI 근월물이 -$37까지 떨어졌을 때 USO는 구조를 급히 바꿨고, 원유 레버리지 ETN 몇 개는 사라졌어요. 극단적인 상황에서는 ETF가 선물과 다르게 움직일 수 있어요."), EXT],
        k1=True))

    out.append(M("natgas", "natgas", "p05_natgas", "천연가스", "NG · QG",
        '천연가스 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "천연가스 ETF도 원유처럼 <b>NG 선물을 사서 매달 굴리는</b> 구조예요. 천연가스는 콘탱고가 특히 심해서 오래 들면 손해가 크기로 유명해요.",
        "<p><strong>한 줄 정답:</strong> 1배는 <b>UNG</b>, 2배 롱은 <b>BOIL</b>, 2배 숏은 <b>KOLD</b>예요. 셋 다 NG 선물을 직접 담아요.</p>"
        "<p>UNG는 2008년 상장 이후 가격이 90% 넘게 빠졌어요. 천연가스 가격이 그만큼 빠진 게 아니라 매달 롤오버 비용이 쌓였기 때문이에요.</p>",
        [G("천연가스 선물 보유 ETF", [("UNG", "United States Natural Gas", 1, "fut", "1배 대표. 근월물 위주"),
                                 ("UNL", "United States 12 Month Nat Gas", 1, "fut", "12개 월물 분산, 거래 얇음"),
                                 ("BOIL", "ProShares Ultra 천연가스", 2, "fut", "2배 롱"),
                                 ("KOLD", "ProShares UltraShort 천연가스", -2, "fut", "2배 숏")]),
         G("참고: 가스 생산 회사 주식", [("FCG", "퍼스트트러스트 천연가스", 1, "eq", "가스 회사 주식. 선물과 따로 놀 때가 많음")])],
        [("t-3", "1배", "단기 반등", "<b>UNG</b>. 며칠 단위로만 쓰세요."), ("t-1", "2배 롱", "겨울 한파 베팅", "<b>BOIL</b>."),
         ("t-spec", "2배 숏", "따뜻한 겨울 · 재고 과잉", "<b>KOLD</b>."),
         ("t-4", "선물이 나을 때", "정확한 월물 선택", "천연가스는 월물마다 가격 차이가 커요. 겨울물(1·2월)만 골라서 사고 싶으면 QG(미니) 선물로 직접 고르는 게 나아요.")],
        [(True, "롤오버 비용이 아주 커요", "천연가스는 먼 월물이 비싼 콘탱고가 심해서, UNG를 1년 들고 있으면 가스 가격이 그대로여도 크게 손해 볼 수 있어요."), K1, LEV_DECAY, EXT],
        k1=True))

    out.append(M("products", "products", "p06_products", "휘발유·경유", "RB · HO",
        '휘발유·경유 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "휘발유(RB) 선물은 <b>UGA</b> 하나가 직접 담고 있어요. 경유·난방유(HO)만 따로 담는 미국 ETF는 2018년에 마지막 상품(UHN)이 문을 닫아서 지금은 없어요.",
        "<p><strong>한 줄 정답:</strong> 휘발유는 <b>UGA</b>(1배, RB 선물 보유). 경유(HO)만 따로 사는 ETF는 없고, <b>DBE</b>(에너지 바구니)에 원유·휘발유·난방유·천연가스가 섞여 있어요.</p>"
        "<p>둘 다 거래가 적어요. 정제유에 제대로 투자하려면 RB·HO 선물을 직접 하는 게 사실상 유일한 방법이에요.</p>",
        [G("정제유 선물 보유 ETF", [("UGA", "United States Gasoline Fund", 1, "fut", "RBOB 휘발유 선물 근월물"),
                                ("DBE", "인베스코 DB 에너지", 1, "basket", "WTI·브렌트·휘발유·난방유·천연가스 바구니")])],
        [("t-3", "휘발유", "여름 드라이빙 시즌", "<b>UGA</b>. 거래가 적으니 지정가로."), ("t-4", "경유", "ETF 없음", "HO 선물을 직접 거래해야 해요. 1계약 42,000갤런이라 큰 편이에요."),
         ("t-2", "에너지 전체", "바구니로", "<b>DBE</b>. 원유 비중이 커서 원유와 비슷하게 움직여요.")],
        [ROLL, K1, THIN, (False, "계절성", "휘발유는 여름용(저휘발성)·겨울용 규격이 달라서 4월물과 10월물 사이에 가격이 뚝 떨어지는 구간이 있어요. UGA도 그 롤오버를 그대로 겪어요.")],
        k1=True))

    # ------------------------------------------------------------------ metals
    out.append(M("gold", "gold", "p07_gold", "금", "GC · MGC · 1OZ",
        '금 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "금 ETF는 크게 셋이에요. <b>GC 선물을 담는 레버리지 상품</b>, <b>GLD 가격을 따라가는 ETN</b>, 그리고 금괴를 금고에 넣어두는 <b>실물 ETF</b>예요.",
        "<p><strong>한 줄 정답:</strong> GC 선물을 실제로 담는 상품 중 거래가 충분한 건 <b>UGL(2배 롱)</b>과 <b>GLL(-2배 숏)</b>이에요. 1배라면 선물형보다 <b>GLD · IAU</b> 같은 실물 ETF가 GC와 거의 같이 움직이고 유동성이 압도적이에요.</p>"
        "<p>1배로 GC만 깔끔하게 담는 선물형 ETF는 사실상 없어요(DBP는 은이 섞여 있어요).</p>",
        [G("① GC 선물 기반", [("UGL", "ProShares Ultra Gold", 2, "mix", "레버리지 롱 대표"),
                           ("GLL", "ProShares UltraShort Gold", -2, "mix", "숏 대표"),
                           ("DGP", "DB Gold Double Long ETN", 2, "etn", "도이체방크 발행"),
                           ("DZZ", "DB Gold Double Short ETN", -2, "etn", "거래 사실상 없음"),
                           ("DBP", "인베스코 DB 귀금속", 1, "fut", "금 약 80% + 은 약 20%, K-1"),
                           ("GDE", "위즈덤트리 금+주식", "금 0.9배 + S&P 0.9배", "fut", "금 선물과 주식을 함께")]),
         G("② 금 가격 연동 (GC 선물을 직접 담지는 않음)", [("SHNY", "MicroSectors 금 3배 ETN", 3, "etn", "BMO 발행, GLD 기준"),
                                                ("DULL", "MicroSectors 금 -3배 ETN", -3, "etn", "거래 얇음"),
                                                ("UGLD", "Direxion 금 2배", 2, "swap", "2026년 5월 상장, GLD 기준")]),
         G("③ 실물 금 (1배)", [("GLD", "SPDR 골드", 1, "phys", "금 ETF 대표, 옵션 활발"),
                            ("IAU", "아이셰어즈 골드", 1, "phys", "보수 더 낮음"),
                            ("GLDM", "SPDR 골드 미니", 1, "phys", "보수 0.10%"),
                            ("IAUM", "아이셰어즈 골드 마이크로", 1, "phys", ""),
                            ("SGOL", "abrdn 실물 금", 1, "phys", "스위스·런던 금고")],
           "② ③ 그룹 중 일부(DZZ·DBP·GDE·SHNY·DULL·IAU·GLDM·IAUM·SGOL)는 11/2 금 ETF 조사 때 IBKR에서 조회한 값이에요.")],
        [("t-1", "2배 롱", "GC 선물 그대로 + 레버리지", "<b>UGL</b>. GC 선물 기반 상품 중 유동성 1위."),
         ("t-spec", "2배 숏", "금 하락 베팅", "<b>GLL</b>."),
         ("t-3", "1배", "금 그 자체", "<b>GLD</b>(거래·옵션), 오래 보유는 <b>IAU · GLDM</b>(보수 낮음)."),
         ("t-4", "선물이 나을 때", "며칠 이상 레버리지", "MGC(마이크로 금, 10온스)는 매일 리셋이 없어서 레버리지를 오래 들고 가기엔 더 효율적이에요.")],
        [LEV_DECAY, ETN_RISK, THIN, (False, "실물 ETF 세금", "GLD 같은 실물 금 ETF는 미국 세법상 '수집품'으로 분류돼서 장기 보유 차익 세율이 일반 주식보다 높을 수 있어요(최대 28%)."), EXT],
        k1=True))

    out.append(M("silver", "silver", "p08_silver", "은", "SI · SIL · SIC",
        '은 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "은도 금처럼 <b>실물 은을 금고에 보관하는 ETF</b>와 <b>선물·스왑으로 배수를 맞추는 레버리지 ETF</b>로 나뉘어요.",
        "<p><strong>한 줄 정답:</strong> 1배는 <b>SLV</b>(실물), 2배 롱은 <b>AGQ</b>, 2배 숏은 <b>ZSL</b>이에요. AGQ·ZSL은 ProShares 상품으로 은 선물과 스왑을 섞어요.</p>",
        [G("은 관련 ETF", [("SLV", "아이셰어즈 실버 트러스트", 1, "phys", "은 ETF 대표, 옵션 활발"),
                        ("SIVR", "abrdn 실물 은", 1, "phys", "보수 더 낮음"),
                        ("AGQ", "ProShares Ultra Silver", 2, "mix", "2배 롱 대표"),
                        ("USLV", "Direxion 은 2배", 2, "swap", "신규 상품, SLV 기준"),
                        ("ZSL", "ProShares UltraShort Silver", -2, "mix", "2배 숏")])],
        [("t-3", "1배", "은 그 자체", "<b>SLV</b>. 오래 들고 갈 거면 보수가 싼 <b>SIVR</b>."), ("t-1", "2배 롱", "단기 상승", "<b>AGQ</b>."),
         ("t-spec", "2배 숏", "단기 하락", "<b>ZSL</b>."), ("t-4", "선물이 나을 때", "소액 레버리지", "SIL(1,000온스 소형) 선물로도 소액 레버리지가 가능해요.")],
        [LEV_DECAY, (False, "은은 금보다 2배쯤 출렁여요", "은은 하루 3~5% 움직이는 날이 흔해요. 2배 상품이면 하루 10%도 쉽게 움직여요."), THIN, EXT]))

    out.append(M("copper", "copper", "p09_copper", "구리", "HG · MHG",
        '구리 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "구리는 실물 보관 ETF가 없어서, 구리 가격을 따라가는 ETF는 <b>HG 선물을 담는 상품</b>뿐이에요. 대신 구리 광산 회사 주식 ETF가 훨씬 많이 거래돼요.",
        "<p><strong>한 줄 정답:</strong> HG 선물 1배는 <b>CPER</b>, 2배 롱은 <b>UCOP</b>(ProShares, K-1 없음)예요. 구리 숏 ETF는 없어요.</p>"
        "<p><b>COPX</b>는 구리 광산 회사 주식이라 구리 가격보다 1.5~2배 크게 움직이고, 주식시장 분위기도 같이 타요.</p>",
        [G("구리 선물 기반", [("CPER", "United States Copper Index", 1, "fut", "HG 선물 1배 대표"),
                          ("UCOP", "ProShares Ultra 구리", 2, "mix", "K-1 없는 2배 롱")]),
         G("참고: 구리 광산 주식", [("COPX", "글로벌X 구리 광산", 1, "eq", "광산 회사 주식, 구리보다 변동 큼")])],
        [("t-3", "1배", "구리 가격 그대로", "<b>CPER</b>."), ("t-1", "2배 롱", "단기 상승", "<b>UCOP</b>. 거래가 적으니 지정가로."),
         ("t-spec", "숏", "ETF 없음", "구리 하락에 베팅하려면 MHG(마이크로 구리) 선물 매도가 가장 간단해요."),
         ("t-2", "광산주", "주식으로", "<b>COPX</b>. 구리 가격이 오르면 더 크게 오르지만 따로 놀 때도 있어요.")],
        [ROLL, K1, THIN, LEV_DECAY], k1=True))

    out.append(M("pgm", "pgm", "p10_pgm", "백금·팔라듐", "PL · PA",
        '백금·팔라듐을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "백금과 팔라듐은 <b>실물을 금고에 넣어두는 1배 ETF</b>만 있어요. 미국에는 백금·팔라듐 선물 기반이나 레버리지·인버스 ETF가 없어요.",
        "<p><strong>한 줄 정답:</strong> 백금은 <b>PPLT</b>(또는 보수가 싼 <b>PLTM</b>), 팔라듐은 <b>PALL</b>이에요. 레버리지나 숏은 PL·PA 선물을 직접 해야 해요.</p>",
        [G("실물 백금·팔라듐", [("PPLT", "abrdn 실물 백금", 1, "phys", "백금 대표"),
                           ("PLTM", "그래니트셰어즈 백금", 1, "phys", "보수 더 낮음, 거래 적음"),
                           ("PALL", "abrdn 실물 팔라듐", 1, "phys", "팔라듐 유일")])],
        [("t-3", "백금 1배", "PL 대신", "<b>PPLT</b>."), ("t-3", "팔라듐 1배", "PA 대신", "<b>PALL</b>."),
         ("t-4", "레버리지·숏", "ETF 없음", "PL(50온스)·PA(100온스) 선물로만 가능해요. 둘 다 거래가 얇은 편이라 지정가를 쓰세요.")],
        [THIN, EXT, (False, "실물 ETF 세금", "실물 귀금속 ETF는 미국 세법상 수집품이라 장기 차익 세율이 일반 주식보다 높을 수 있어요.")]))

    # ------------------------------------------------------------------ grains & softs
    AG = [("DBA", "인베스코 DB 농산물", 1, "basket", "옥수수·대두·밀·설탕·커피·코코아·소·돼지"),
          ("TAGS", "Teucrium 농산물", 1, "basket", "옥수수·대두·밀·설탕 4종 동일비중, 거래 얇음")]
    def grain(key, mod, name, fut, tk, tkname, extra_note, fun=None):
        return M(key, key, mod, name, fut, f'{name} 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
                 f"{name}는 Teucrium의 <b>{tk}</b> 하나가 {fut.split()[0]} 선물을 직접 담고 있어요. 레버리지·인버스 상품은 미국에 없어요.",
                 f"<p><strong>한 줄 정답:</strong> <b>{tk}</b>(1배, {fut.split()[0]} 선물 보유)가 유일해요. 숏이나 레버리지는 선물을 직접 해야 해요.</p><p>{extra_note}</p>",
                 [G(f"{name} 선물 기반", [(tk, tkname, 1, "fut", "근월물이 아니라 3개 월물에 나눠 담아요")]),
                  G("참고: 농산물 바구니", AG)],
                 [("t-3", "1배", f"{name} 가격", f"<b>{tk}</b>. 거래가 많지 않아 지정가 필수."),
                  ("t-4", "숏·레버리지", "ETF 없음", "CBOT 미니·마이크로 곡물 선물(예: 마이크로 옥수수 MZC)로 소액 거래가 가능해요."),
                  ("t-2", "농산물 전체", "바구니로", "<b>DBA</b>. 곡물·설탕·커피·코코아·가축이 섞여 있어요.")],
                 [ROLL, K1, THIN, EXT, (False, "날씨 뉴스는 밤에도", "곡물 선물은 캘리포니아 오후 5시~다음날 오전 11:20에 거래되는데 ETF는 06:30~13:00에만 거래돼요. 주말 날씨 뉴스는 월요일 아침 갭으로 반영돼요.")],
                 k1=True, fun=fun)
    out.append(grain("corn", "p11_corn", "옥수수", "ZC · YC · MZC", "CORN", "Teucrium Corn Fund", "귀리(ZO)는 따로 담는 ETF가 없어요."))
    out.append(grain("soy", "p12_soy", "대두", "ZS · ZM · ZL", "SOYB", "Teucrium Soybean Fund", "대두박(ZM)·대두유(ZL)만 따로 담는 ETF는 없어요."))
    out.append(grain("wheat", "p13_wheat", "밀", "ZW · KE", "WEAT", "Teucrium Wheat Fund", "WEAT는 시카고 소맥(ZW)을 담아요. 캔자스 경질밀(KE)만 담는 ETF는 없어요."))
    out.append(grain("sugar", "p14_sugar", "설탕", "SB", "CANE", "Teucrium Sugar Fund", "CANE은 ICE 원당 11호(SB) 선물을 담아요."))

    def none_page(key, links_key, mod, name, fut, why, alt_rows, alt_text, picks, fun=None, extra_c=()):
        return M(key, links_key, mod, name, fut, f'{name} 선물을 담은<br><span class="hl">ETF</span>가 있을까?',
                 f"결론부터 말하면 지금 미국에는 {name}({fut}) 가격을 따라가는 ETF·ETN이 <b>없어요</b>. 아래는 대신 쓸 수 있는 상품이에요.",
                 f"<p><strong>한 줄 정답:</strong> {name}만 따로 따라가는 미국 ETF는 없어요. {alt_text}</p>",
                 [G("대신 쓸 수 있는 상품", alt_rows)] if alt_rows else [],
                 picks, [THIN, EXT] + list(extra_c), none=why, fun=fun)
    out.append(none_page("coffee", "coffee", "p15_cocoa", "커피", "KC",
        "<p><strong>커피 ETF는 없어요.</strong> 예전에 iPath 커피 ETN(JO)이 있었지만 2023년에 상장폐지됐어요. 커피는 ICE 미국 시장에서 KC 선물(37,500파운드)로만 직접 거래할 수 있어요.</p>",
        [AG[0]], "DBA(농산물 바구니)에 커피가 약 10% 정도 들어 있지만 커피만 따로 움직이지는 않아요.",
        [("t-2", "바구니", "농산물 전체", "<b>DBA</b>. 커피 비중은 일부예요."), ("t-4", "커피 그 자체", "선물만 가능", "KC 선물. 1센트 움직이면 $375예요.")],
        extra_c=[K1]))
    out.append(none_page("cocoa", "cocoa", "p15_cocoa", "코코아", "CC",
        "<p><strong>코코아 ETF는 없어요.</strong> iPath 코코아 ETN(NIB)이 2023년에 상장폐지된 뒤로 코코아만 담는 미국 상품은 없어요.</p>",
        [AG[0]], "DBA에 코코아가 일부 들어 있어요. 2024년 코코아 급등 때 DBA도 같이 올랐지만 상승폭은 훨씬 작았어요.",
        [("t-2", "바구니", "농산물 전체", "<b>DBA</b>."), ("t-4", "코코아 그 자체", "선물만 가능", "ICE CC 선물(10톤). $1 움직이면 $10예요.")],
        extra_c=[K1]))
    out.append(none_page("cotton", "cotton", "p16_cotton", "면화", "CT",
        "<p><strong>면화 ETF는 없어요.</strong> iPath 면화 ETN(BAL)이 2023년에 상장폐지됐어요. DBA에도 면화는 들어 있지 않아요.</p>",
        [], "면화에 투자하려면 ICE CT 선물(50,000파운드)을 직접 거래해야 해요.",
        [("t-4", "면화", "선물만 가능", "CT 선물. 1센트 움직이면 $500예요.")]))
    out.append(none_page("oj", "oj", "p14_sugar", "오렌지주스", "OJ",
        "<p><strong>오렌지주스 ETF는 없어요.</strong> OJ(냉동농축 오렌지주스) 선물은 거래 자체가 적어서 미국에 관련 ETF·ETN이 한 번도 크게 자리 잡은 적이 없어요.</p>",
        [], "OJ는 ICE 선물(15,000파운드)로만 직접 거래할 수 있고, 하루 거래량이 수천 계약 수준이라 선물도 얇은 편이에요.",
        [("t-4", "오렌지주스", "선물만 가능", "OJ 선물. 1센트 움직이면 $150예요.")]))
    out.append(none_page("rice", "rice", "p12_soy", "쌀", "ZR",
        "<p><strong>쌀 ETF는 없어요.</strong> CBOT 쌀(ZR) 선물은 미국 남부 장립종 쌀 한 가지인데 거래가 적어서, 미국에 쌀 ETF가 나온 적이 없어요. DBA에도 쌀은 없어요.</p>",
        [], "쌀에 투자하려면 ZR 선물(2,000헌드레드웨이트)을 직접 해야 해요.",
        [("t-4", "쌀", "선물만 가능", "ZR 선물. 0.5센트 움직이면 $10예요.")]))
    out.append(none_page("lumber", "lumber", "p17_lumber", "목재", "LBR",
        "<p><strong>목재 선물 ETF는 없어요.</strong> CME 목재 선물(LBR)만 담는 ETF는 미국에 없어요. 대신 산림·목재 회사 주식을 담는 ETF가 있어요.</p>",
        [("WOOD", "아이셰어즈 글로벌 목재·산림", 1, "eq", "목재 회사 주식. 목재 가격보다 주식시장과 더 비슷하게 움직임")],
        "<b>WOOD</b>는 목재 회사 주식이라 목재 선물 가격과 따로 움직일 때가 많아요.",
        [("t-2", "목재 회사 주식", "주식으로", "<b>WOOD</b>."), ("t-4", "목재 가격 그 자체", "선물만 가능", "LBR 선물(27,500보드피트). 거래가 얇아요.")]))
    out.append(none_page("cattle", "cattle", "p18_cattle", "소", "LE · GF",
        "<p><strong>소 선물 ETF는 없어요.</strong> iPath 가축 ETN(COW)이 2023년에 상장폐지된 뒤로 생우·비육우만 담는 미국 상품은 없어요.</p>",
        [AG[0]], "DBA에 생우·비육우가 일부 들어 있어요.",
        [("t-2", "바구니", "농산물 전체", "<b>DBA</b>."), ("t-4", "소 그 자체", "선물만 가능", "LE(생우 40,000파운드)·GF(비육우 50,000파운드) 선물.")],
        extra_c=[K1]))
    out.append(none_page("hogs", "hogs", "p19_hogs", "돼지", "HE",
        "<p><strong>돼지 선물 ETF는 없어요.</strong> 예전 가축 ETN(COW)이 2023년에 상장폐지된 뒤로 돼지만 담는 미국 상품은 없어요.</p>",
        [AG[0]], "DBA에 돼지(HE)가 일부 들어 있어요.",
        [("t-2", "바구니", "농산물 전체", "<b>DBA</b>."), ("t-4", "돼지 그 자체", "선물만 가능", "HE 선물(40,000파운드).")],
        extra_c=[K1]))

    # ------------------------------------------------------------------ crypto & vix
    out.append(M("crypto", "crypto", "p20_crypto", "비트코인·이더리움", "BTC · MBT · ETH · MET",
        '비트코인 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "CME 비트코인·이더리움 선물을 담는 미국 ETF가 1배, 2배, 인버스까지 있어요. 현물 ETF(IBIT 등)는 코인을 직접 들고 있어서 선물과는 구조가 달라요.",
        "<p><strong>한 줄 정답:</strong> 비트코인 1배는 <b>BITO</b>, 2배 롱은 <b>BITX</b>, 숏은 <b>SBIT</b>(-2배)나 <b>BITI</b>(-1배)예요. 이더리움 2배는 <b>ETHU</b>, -2배는 <b>ETHD</b>예요.</p>"
        "<p>CME 선물을 실제로 들고 있는 건 BITO·BITI·BITX·ETHU예요. ProShares의 BITU·SBIT·ETHT·ETHD와 T-Rex의 BTCL·BTCZ는 스왑을 주로 써요.</p>",
        [G("비트코인 선물 기반", [("BITO", "ProShares Bitcoin ETF", 1, "fut", "1배 대표. 매달 큰 분배금"),
                              ("BITX", "2x Bitcoin Strategy", 2, "fut", "2배 롱 대표"),
                              ("BITU", "ProShares Ultra Bitcoin", 2, "mix", ""),
                              ("BTCL", "T-Rex 2X Long Bitcoin", 2, "swap", "거래 거의 없음"),
                              ("BITI", "ProShares Short Bitcoin", -1, "fut", ""),
                              ("SBIT", "ProShares UltraShort Bitcoin", -2, "mix", ""),
                              ("BTCZ", "T-Rex 2X Inverse Bitcoin", -2, "swap", "AUM 작음, 스프레드 확인")],
           "비트코인 표는 10/30 조사 결과를 오늘 다시 조회해서 갱신했어요."),
         G("이더리움 선물 기반", [("ETHU", "2x Ether ETF", 2, "fut", "CME 이더 선물 보유"),
                              ("ETHT", "ProShares Ultra Ether", 2, "mix", ""),
                              ("ETHD", "ProShares UltraShort Ether", -2, "mix", "")]),
         G("참고: 현물 비트코인 ETF", [("IBIT", "아이셰어즈 비트코인 트러스트", 1, "phys", "비트코인 직접 보유. 선물 롤 비용 없음")])],
        [("t-3", "1배", "선물 기반", "<b>BITO</b>. 오래 보유는 현물 <b>IBIT</b>이 롤 비용이 없어서 유리해요."),
         ("t-1", "2배 롱", "비트코인 · 이더", "<b>BITX</b> · <b>ETHU</b>."), ("t-spec", "숏", "하락 베팅", "<b>SBIT</b>(-2배), <b>BITI</b>(-1배), <b>ETHD</b>(-2배)."),
         ("t-4", "선물이 나을 때", "주말 · 밤", "비트코인은 주말에도 움직이는데 ETF는 평일 낮에만 거래돼요. MBT(0.1 BTC) 마이크로 선물은 일요일 오후 3시(PT)부터 열려요.")],
        [ROLL, LEV_DECAY, (False, "주말 갭", "토·일에 비트코인이 크게 움직이면 월요일 아침 ETF가 갭으로 시작해요."), THIN, EXT]))

    out.append(M("vix", "vix", "p21_vix", "VIX", "VX · VXM",
        'VIX 선물을 담은<br><span class="hl">ETF</span>는 뭐가 있을까?',
        "VIX ETF·ETN은 전부 <b>VIX 선물을 사서 매일 굴리는</b> 구조예요. VIX 지수 자체는 살 수 없어서, VIX가 똑같이 올라도 ETF는 훨씬 덜 오르고 평소에는 꾸준히 빠져요.",
        "<p><strong>한 줄 정답:</strong> 1배 롱은 <b>VXX</b>(ETN)나 <b>VIXY</b>, 레버리지 롱은 <b>UVXY</b>(1.5배)·<b>UVIX</b>(2배), 숏은 <b>SVXY</b>(-0.5배)·<b>SVIX</b>(-1배)예요.</p>"
        "<p>롱 VIX 상품은 장기적으로 거의 0을 향해 가요. 며칠짜리 헤지나 이벤트 베팅으로만 쓰세요.</p>",
        [G("단기 VIX 선물 (1~2개월물)", [("VXX", "iPath VIX 단기 선물 ETN", 1, "etn", "VIX 상품 대표"),
                                       ("VIXY", "ProShares VIX 단기 선물", 1, "fut", ""),
                                       ("UVXY", "ProShares Ultra VIX 단기", 1.5, "fut", "1.5배 롱"),
                                       ("UVIX", "Volatility Shares 2x VIX", 2, "fut", "2배 롱"),
                                       ("SVXY", "ProShares Short VIX 단기", -0.5, "fut", "-0.5배 숏"),
                                       ("SVIX", "Volatility Shares -1x VIX", -1, "fut", "-1배 숏")]),
         G("중기 VIX 선물 (4~7개월물)", [("VIXM", "ProShares VIX 중기 선물", 1, "fut", "덜 빠지지만 덜 오름")])],
        [("t-1", "급락 헤지", "며칠짜리 보험", "<b>UVXY</b>나 <b>VXX</b>. 사고 바로 빠지기 시작한다고 생각하세요."),
         ("t-spec", "숏 VIX", "평온한 장에서", "<b>SVXY</b>(-0.5배)가 덜 위험하고, <b>SVIX</b>(-1배)는 2018년 2월 같은 폭발에 크게 다쳐요."),
         ("t-3", "중기", "덜 빠지는 대신", "<b>VIXM</b>. 롤 비용이 작지만 급등 때 반응도 작아요."),
         ("t-4", "선물이 나을 때", "월물 직접 선택", "VX·VXM(미니) 선물로 원하는 월물만 고를 수 있어요.")],
        [(True, "롱 VIX는 장기 보유 금지", "VIX 선물은 대부분 콘탱고라서 VXX·UVXY는 해마다 큰 폭으로 빠져요. 역분할(주식 병합)도 자주 해요."), ROLL, LEV_DECAY, ETN_RISK,
         (False, "숏 VIX의 꼬리 위험", "2018년 2월 하루 만에 XIV(-1배 VIX ETN)가 90% 넘게 빠져서 사라졌어요. 숏 VIX는 작은 이익을 오래 모으다 한 번에 잃을 수 있어요.")]))
    return out
