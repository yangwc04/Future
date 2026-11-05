# 선물 종목별 설명 시리즈

미국 선물 종목을 쉬운 한국어로 설명한 페이지 모음이에요. 첫 화면(`index.html`)은 한눈에 보기 허브이고, 나머지는 종목별 설명 페이지예요. 모든 시간은 캘리포니아(태평양) 시간이에요.

사이트: https://yangwc04.github.io/Future/

`generator/`에는 페이지를 만드는 파이썬 코드가 들어 있어요.

각 종목 페이지 상단의 **📊 관련 ETF 보기** 버튼을 누르면 그 선물을 따라가는 미국 ETF·ETN 페이지(`<종목>-etf.html`)로 넘어가요. 레버리지, IBKR 90일 평균 거래대금, 하루 주식 수, 운용자산, 구조(선물·스왑·실물)를 비교해요.

ETF 페이지 다시 만들기: `generator/etf_data.json`(IBKR 스냅샷)을 고친 뒤 `python3 build_etf.py`, 종목 페이지는 `python3 build.py <모듈>`, 사이트 조립은 `python3 assemble.py`.
