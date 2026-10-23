import re, sys
D='/tmp/claude-0/-home-claude/714c66fd-f638-5036-a341-24118051e9b2/scratchpad/old/'
HUB='https://claude.ai/artifact/23ox422LgUwgvaSdabVr6s'

def css(a, b):
    return f'''
/* ---- refreshed look: hero header, pill eyebrows, softer cards ---- */
:root{{--hero-a:color-mix(in srgb,var({a}) 88%,#000);--hero-b:color-mix(in srgb,var({b}) 62%,#000);--shadow:0 1px 2px rgba(20,25,35,.05),0 6px 20px rgba(20,25,35,.06)}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--hero-a:color-mix(in srgb,var({a}) 34%,#0b0d10);--hero-b:color-mix(in srgb,var({b}) 30%,#0b0d10);--shadow:none}}}}
:root[data-theme="dark"]{{--hero-a:color-mix(in srgb,var({a}) 34%,#0b0d10);--hero-b:color-mix(in srgb,var({b}) 30%,#0b0d10);--shadow:none}}
main{{gap:68px}}
h1,h2,h3{{word-break:keep-all}}
main>header{{display:flex;flex-direction:column;background:radial-gradient(130% 150% at 0% 0%,var(--hero-a) 0%,var(--hero-a) 30%,var(--hero-b) 100%);color:#fff;
  border-radius:24px;padding:32px 30px;gap:18px;position:relative;overflow:hidden;box-shadow:var(--shadow)}}
main>header::after{{content:"";position:absolute;right:-90px;top:-90px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.07);pointer-events:none}}
main>header>*{{position:relative;z-index:1}}
main>header .eyebrow,main>header h1 span{{color:#ffe3a3!important}}
main>header .lead{{color:rgba(255,255,255,.88)}}
main>header .lead b{{color:#fff}}
main>header .answer{{background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.2);color:#fff}}
main>header .answer strong,main>header .answer b{{color:#ffe3a3}}
main>header .quote>div{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.2);color:#fff}}
main>header .quote small,main>header .quote span,main>header .cap{{color:rgba(255,255,255,.75)}}
main>header .toc a{{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.24);color:#fff}}
main>header .toc a:hover,main>header .toc a:focus-visible{{border-color:#ffe3a3}}
main>header a{{color:#ffe3a3}}
main>header .back{{color:rgba(255,255,255,.8);font-size:.85rem;text-decoration:none}}
section>.eyebrow{{align-self:flex-start;background:var({a}-soft);color:var({a});border-radius:99px;padding:3px 12px;letter-spacing:.03em}}
section>h2{{font-size:clamp(1.5rem,4.2vw,1.95rem)}}
.fig,.calc,.spec,.quote>div,.warn>div,.who>div,.risks>div{{box-shadow:var(--shadow)}}
.fig{{border-radius:18px}}
.who>div{{border-radius:16px;transition:transform .15s,border-color .15s}}
.who>div:hover{{transform:translateY(-2px);border-color:var({a})}}
.warn{{grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr))!important}}
.fun{{border-radius:18px;background:linear-gradient(135deg,var({a}-soft),var(--surface) 70%)}}
.note{{border-left-color:var({a})}}
.ptnote{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 16px;font-size:.92rem;box-shadow:var(--shadow)}}
@media (max-width:560px){{main>header{{padding:22px 18px;border-radius:20px}}}}
</style>'''

def common(h, a, b):
    i = h.index('</style>', h.index('<main') - 4000 if False else 0)
    # inject into the page's own (second) style block: last </style> before <main>
    m = h.rfind('</style>', 0, h.index('<main'))
    h = h[:m] + css(a, b) + h[m+len('</style>'):]
    h = h.replace('<header>', f'<header>\n  <a class="back" href="{HUB}">← 미국 선물 한눈에 보기</a>', 1)
    h = h.replace('<header style="display:flex;flex-direction:column;gap:14px">', f'<header>\n  <a class="back" href="{HUB}">← 미국 선물 한눈에 보기</a>', 1)
    return h

def sub(h, old, new):
    assert old in h, old[:60]
    return h.replace(old, new)

# ---------- rice ----------
h = open(D+'rice/index.html').read()
h = common(h, '--paddy', '--field')
h = sub(h, '2026-10-22 오전 10:18(한국 시간)', '2026-10-21 오후 6:18(캘리포니아 시간)')
h = sub(h, '한국 시간 새벽 1~2시에 나와요', '캘리포니아 시간 오전 9시에 나와요(장중이라 바로 반영돼요)')
h = sub(h, '특히 한국 낮 시간(미국 야간)에는 호가가 거의 비어 있으니 미국 주간 세션(밤 10:30 이후)에', '특히 캘리포니아 저녁~새벽(야간 세션)에는 호가가 거의 비어 있으니 주간 세션(오전 6:30~11:20)에')
h = re.sub(r'\s*<label for="in-fx">.*?</label>', '', h)
h = sub(h, '<small>손익 (원화 환산)</small>', '<small>가격 변화율</small>')
h = sub(h, '환율 1,400원은 예시 값이니 실제 환율로 바꿔 넣으세요. ', '')
h = sub(h, "    var fx = parseFloat($('in-fx').value) || 0;\n", '')
h = sub(h, "k.textContent = fx ? ((pnl>0?'+':'') + krw(pnl*fx)) : '–';", "var pct = (x-e)/e*100*side; k.textContent = (pct>0?'+':'') + pct.toFixed(2) + '%';")
h = sub(h, ",'in-fx']", "]")
RICE_SVG = '''<section id="hours">
  <span class="eyebrow">9. 캘리포니아 시간으로 언제 열리나</span>
  <h2>저녁에 열리고, 아침에 진짜 거래가 붙어요</h2>
  <div class="fig">
    <svg viewBox="0 0 740 190" role="img" aria-label="캘리포니아 시간 기준 ZR 거래 시간. 야간(전자) 세션 오후 5:00~다음날 오전 5:45, 주간 세션 오전 6:30~11:20. 일년 내내 같음">
      <!-- axis 15:00 → 12:00 next day (21h), x 150..720, 27.14px/h -->
      <g class="sm" text-anchor="middle"><text x="150" y="28">15시</text><text x="231" y="28">18시</text><text x="313" y="28">21시</text><text x="394" y="28">00시</text><text x="476" y="28">03시</text><text x="557" y="28">06시</text><text x="639" y="28">09시</text><text x="720" y="28">12시</text></g>
      <g stroke="var(--line)"><line x1="150" y1="36" x2="150" y2="130"/><line x1="231" y1="36" x2="231" y2="130"/><line x1="313" y1="36" x2="313" y2="130"/><line x1="394" y1="36" x2="394" y2="130"/><line x1="476" y1="36" x2="476" y2="130"/><line x1="557" y1="36" x2="557" y2="130"/><line x1="639" y1="36" x2="639" y2="130"/><line x1="720" y1="36" x2="720" y2="130"/></g>
      <text x="16" y="70" class="b" style="fill:var(--paddy)">ZR (일년 내내)</text>
      <rect x="204" y="54" width="346" height="24" rx="12" fill="var(--paddy-soft)" stroke="var(--paddy)"/>
      <text x="377" y="71" text-anchor="middle" style="font-size:12px;fill:var(--paddy)" class="b">17:00 ~ 05:45 · 야간(전자) 세션</text>
      <rect x="571" y="54" width="131" height="24" rx="12" fill="var(--paddy)"/>
      <text x="636" y="71" text-anchor="middle" style="font-size:12px;fill:var(--surface)" class="b">06:30 ~ 11:20</text>
      <line x1="625" y1="40" x2="625" y2="100" stroke="var(--water)" stroke-dasharray="3 3"/>
      <text x="625" y="114" text-anchor="middle" class="sm" style="fill:var(--water)">09:00 USDA 보고서</text>
      <text x="377" y="104" text-anchor="middle" class="sm">캘리 저녁·밤 = 열려 있지만 호가가 아주 얇음</text>
      <text x="636" y="150" text-anchor="middle" class="sm">진한 칸 = 주간 세션</text>
      <text x="636" y="166" text-anchor="middle" class="sm">거래량 대부분이 여기</text>
    </svg>
  </div>
  <p class="cap">현지(시카고) 시간: 일~금 19:00~다음날 07:45, 월~금 08:30~13:20. 캘리포니아는 시카고보다 항상 2시간 늦어서, 서머타임이 끝나도(11월 1일) <b>캘리 시간은 바뀌지 않아요</b>. 일요일 오후 5시에 한 주가 시작되고, 금요일 오전 11:20에 끝나요. 정확한 세션은 IBKR 계약 정보(Contract Info)에서 다시 확인하세요.</p>
</section>'''
h = re.sub(r'<section id="hours">.*?</section>', lambda m: RICE_SVG, h, count=1, flags=re.S)
open(D+'out/rice.html','w').write(h)

# ---------- coffee ----------
h = open(D+'coffee/index.html').read()
h = common(h, '--bean', '--roast')
COF = '''<section id="hours">
  <span class="eyebrow">9. 캘리포니아 시간으로 언제 열리나</span>
  <h2>새벽 1시에 열리고 오전에 닫혀요</h2>
  <div class="fig">
    <svg viewBox="0 0 740 180" role="img" aria-label="캘리포니아 시간 기준 거래 시간. 아라비카 KC 오전 1:15~10:30 일년 내내. 로부스타 RC 평소 오전 1:00~9:30, 10월 25일~31일만 2:00~10:30">
      <!-- axis: 00:00 -> 12:00 (12h), x 150..720, 47.5px/h -->
      <g class="sm" text-anchor="middle">
        <text x="150" y="28">00시</text><text x="245" y="28">02시</text><text x="340" y="28">04시</text><text x="435" y="28">06시</text><text x="530" y="28">08시</text><text x="625" y="28">10시</text><text x="720" y="28">12시</text>
      </g>
      <g stroke="var(--line)"><line x1="150" y1="36" x2="150" y2="140"/><line x1="245" y1="36" x2="245" y2="140"/><line x1="340" y1="36" x2="340" y2="140"/><line x1="435" y1="36" x2="435" y2="140"/><line x1="530" y1="36" x2="530" y2="140"/><line x1="625" y1="36" x2="625" y2="140"/><line x1="720" y1="36" x2="720" y2="140"/></g>
      <line x1="411" y1="36" x2="411" y2="140" stroke="var(--cherry)" stroke-dasharray="3 3"/>
      <text x="411" y="158" text-anchor="middle" class="sm" style="fill:var(--cherry)">05:30 미국 지표</text>
      <text x="16" y="62" class="b" style="fill:var(--bean)">KC 아라비카</text>
      <rect x="209" y="48" width="440" height="20" rx="10" fill="var(--bean)"/>
      <text x="429" y="63" text-anchor="middle" style="font-size:12px;fill:var(--surface)" class="b">01:15 ~ 10:30 (일년 내내)</text>
      <text x="16" y="92" class="b" style="fill:var(--roast)">RC 로부스타</text>
      <rect x="198" y="78" width="404" height="20" rx="10" fill="var(--roast)"/>
      <text x="400" y="93" text-anchor="middle" style="font-size:12px;fill:var(--surface)" class="b">01:00 ~ 09:30 (평소)</text>
      <text x="16" y="122" class="b" style="fill:var(--roast)">RC 10/25~31</text>
      <rect x="245" y="108" width="404" height="20" rx="10" fill="var(--roast-soft)" stroke="var(--roast)"/>
      <text x="447" y="123" text-anchor="middle" style="font-size:12px;fill:var(--roast)" class="b">02:00 ~ 10:30 (이 일주일만)</text>
    </svg>
  </div>
  <p class="cap">현지 시간: 아라비카 뉴욕 04:15~13:30, 로부스타 런던 09:00~17:30. 아라비카는 뉴욕 시장이라 캘리 시간이 <b>일년 내내 같아요</b>. 로부스타는 런던 시장인데, 올해는 영국이 10월 25일, 미국이 11월 1일에 서머타임이 끝나서 <b>10/25~10/31 일주일만</b> 한 시간 늦게 열고 닫혀요. 거래가 가장 활발한 건 뉴욕 사람들이 출근하는 캘리 오전 6~9시 사이예요. 정확한 세션은 IBKR 계약 정보(Contract Info)에서 다시 확인하세요.</p>
</section>'''
h = re.sub(r'<section id="hours">.*?</section>', lambda m: COF, h, count=1, flags=re.S)
open(D+'out/coffee.html','w').write(h)

# ---------- OJ ----------
h = open(D+'oj/index.html').read()
h = common(h, '--orange', '--leaf')
OJ = '''<section id="hours">
  <span class="eyebrow">6. 캘리포니아 시간으로 언제 열리나</span>
  <h2>오전 5시부터 11시까지, 딱 6시간</h2>
  <div class="fig">
    <svg viewBox="0 0 740 150" role="img" aria-label="캘리포니아 시간 기준 OJ 거래 시간 오전 5:00~11:00, 일년 내내 같음. 매달 둘째 주 오전 9시 USDA 보고서">
      <!-- axis 03:00 -> 13:00 (10h), x 150..720, 57px/h -->
      <g class="sm" text-anchor="middle"><text x="150" y="28">03시</text><text x="264" y="28">05시</text><text x="378" y="28">07시</text><text x="492" y="28">09시</text><text x="606" y="28">11시</text><text x="720" y="28">13시</text></g>
      <g stroke="var(--line)"><line x1="150" y1="36" x2="150" y2="100"/><line x1="264" y1="36" x2="264" y2="100"/><line x1="378" y1="36" x2="378" y2="100"/><line x1="492" y1="36" x2="492" y2="100"/><line x1="606" y1="36" x2="606" y2="100"/><line x1="720" y1="36" x2="720" y2="100"/></g>
      <text x="16" y="66" class="b" style="fill:var(--orange)">OJ (일년 내내)</text>
      <rect x="264" y="50" width="342" height="24" rx="12" fill="var(--orange)"/>
      <text x="435" y="67" text-anchor="middle" style="font-size:12px;fill:var(--surface)" class="b">05:00 ~ 11:00</text>
      <line x1="492" y1="40" x2="492" y2="100" stroke="var(--frost)" stroke-dasharray="3 3"/>
      <text x="492" y="118" text-anchor="middle" class="sm" style="fill:var(--frost)">09:00 USDA 작황 보고서</text>
      <text x="300" y="118" text-anchor="middle" class="sm">개장 직후 30분 = 밤새 나온 날씨 뉴스 반영</text>
    </svg>
  </div>
  <p class="cap">현지(뉴욕) 시간 08:00~14:00. 캘리포니아는 뉴욕보다 항상 3시간 늦어서 서머타임이 끝나도 <b>캘리 시간은 그대로</b>예요. 야간 세션이 없어서 밤사이 허리케인·한파 뉴스는 다음 날 오전 5시 개장 때 한 번에 반영되고, 큰 갭이 자주 생겨요. 정확한 세션은 IBKR 계약 정보(Contract Info)에서 다시 확인하세요.</p>
</section>

<section class="fun">'''
h = sub(h, '<section class="fun">', OJ)
open(D+'out/oj.html','w').write(h)
print('ok')
