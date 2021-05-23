import requests
import pandas as pd
import time
import webbrowser
import smtplib
from email.mime.text import MIMEText


count = 0



while True:
  answer = int(input("1 / 3 / 5 / 10 / 15 / 60 / 240 \n"))
  result = [1,3,5,10,15,60,240]
  if answer not in result:
    print("다시 선택해주세요\n")
  else:
    print(f"{answer}분을 선택했습니다.\n")
    break


while True:
  # 세션 생성
  s = smtplib.SMTP('smtp.gmail.com', 587)

  # TLS 보안 시작
  s.starttls()

  s.login('구글이메일', '2차앱인증번호')

  if count == 6: # 심볼의 총 개수만큼 rsi를 체크하면 다시 0으로 초기화시켜서 재 진행하게 만듬
    count = 0
  
  '''symbols = ['BTC','ETH','DOGE','XRP','DAWN','BTT','ETC','VET','CHZ','BTG','MED','NEO','EOS',
              'BCHA','AXS','QTUM','STRK','HIVE','ELF','MANA','ANKR','BCH','MLK','SC','ZIL','SAND',
              'XEM','MTL','WAXP','CBK','TRX','SNT','MARO','EMC2','SRM','MVL','PUNDIX','SXP','STMX',
              'FLOW','CRO','PXL','ADA','DKA','META','MBL','STX','CRE','XLM','BSV','OBSR','GLM','TON',
              'WAVES','MOC','TSHP','SSX','LINK','GAS','REP','ARDR','DOT','ZRX','ORBS','POWR','RFR',
              'EDR','KNC','PCI','ONT','IOST','LSK','LTC','ENJ','POLY','HUM','STEEM','STPT','TFUEL',
              'BORA','QTCON','ARK','GRS','AERGO','TT','STORJ','IGNIS','HUNT','SBD','LAMB','UPP','PLA',
              'XTZ','OMG','IQ','JST','KMD','DMT','AHT','MFT','AQT','STRAX','QKC','FCT2','THETA','SOLVE',
              'ICX','ATOM','KAVA','BAT','LOOM','CVC','HBAR','ADX','ONG','LBC','IOTA']
  '''  # 이건 5.21일기준 업비트 원화마켓에 있는 모든 티커 

  # symbols = ['LTC','BTC','VET','DOGE','MANA','ADA','LINK','ETC','EOS','BCH','BTG','NEO','DOT','XRP','ATOM','ETH','HBAR','FLOW','CVC','GLM','ONT','ADA','EOS','XLM','QTUM','MARO','SAND','STORJ']
  # 이건 꽤 괜찮다고 생각하는애들 티커들

  symbols = ['BTC','ETH','BCH','ETC','DOGE','LINK']
  # 이건 현재 포트폴리오로 가지고 있는 애들 


  url = "https://api.upbit.com/v1/candles/minutes/{0}?market=KRW-{1}&count=500".format(answer,symbols[count])
  # 5분봉으로 받아오지만 1,3,5,10,15,30,60,240분으로 수정 가능
  # 분봉 뿐만 아니라 일봉,주봉,월봉도 가능하다.

  response = requests.request("GET", url)
  count += 1
  data = response.json()

  df = pd.DataFrame(data)

  df=df.reindex(index=df.index[::-1]).reset_index()

  df['close']=df["trade_price"]



  # rsi 계산 함수
  def rsi(ohlc: pd.DataFrame, period: int = 14):
      ohlc["close"] = ohlc["close"]
      delta = ohlc["close"].diff()

      up, down = delta.copy(), delta.copy()
      up[up < 0] = 0
      down[down > 0] = 0

      _gain = up.ewm(com=(period - 1), min_periods=period).mean()
      _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

      RS = _gain / _loss
      return pd.Series(100 - (100 / (1 + RS)), name="RSI")

  rsi = rsi(df, 14).iloc[-1]

  print(' {0} 분봉 기준 < {1} > 현재 RSI:'.format(answer,symbols[count-1]), rsi,'\n')


  # rsi 가 32로 오면 메일로 알림을 보내게 만듬
  # 나같은 경우엔 네이버로 보내는데 네이버 메일 어플을 깔면 알림이 참 잘와서 좋음

  
  if rsi <= 31:
    print(" ----- {0} 분봉 기준  < {1} > rsi 30 이하 ------\n".format(answer,symbols[count-1]),rsi)
    # 보낼 메시지 설정
    msg = MIMEText(' ')
    msg['Subject'] = '{0} 분봉 기준 < {1} > 는 현재 RSI 30이하 - rsi : {2}!! '.format(symbols[count-1],answer,rsi)
    s.sendmail("os1227os@gmail.com", "os1227os@naver.com", msg.as_string())
    s.quit()
    time.sleep(10)

  time.sleep(5)


