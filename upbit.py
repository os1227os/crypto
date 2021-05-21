import requests
import pandas as pd
import time
import webbrowser
import smtplib
from email.mime.text import MIMEText


count = 0

while True:
  # 세션 생성
  s = smtplib.SMTP('smtp.gmail.com', 587)

  # TLS 보안 시작
  s.starttls()

  s.login('os1227os@gmail.com', 'ecysiuyyfqzkjiqm')

  if count == 6:
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
  '''
  # symbols = ['LTC','BTC','VET','DOGE','MANA','ADA','LINK','ETC','EOS','BCH','BTG','NEO','DOT','XRP','ATOM','ETH','HBAR','FLOW','CVC','GLM','ONT','ADA','EOS','XLM','QTUM','MARO','SAND','STORJ']
  symbols = ['BTC','ETH','BCH','ETC','DOGE','LINK']


  url = "https://api.upbit.com/v1/candles/minutes/5?market=KRW-{0}&count=500".format(symbols[count])
  #url = "https://api.upbit.com/v1/candles/days/?market=KRW-{0}&count=500".format(symbols[count])
  #url = "https://api.upbit.com/v1/candles/minutes/10?market=KRW-{0}&count=500".format(symbols[count]) ( 분봉 )

  response = requests.request("GET", url)
  count += 1
  data = response.json()

  df = pd.DataFrame(data)

  df=df.reindex(index=df.index[::-1]).reset_index()

  df['close']=df["trade_price"]




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

  print(' {0} 현재 RSI:'.format(symbols[count-1]), rsi)

  if rsi <= 32:
    print(" ----- {0} rsi 30 이하 ------".format(symbols[count-1]),rsi)
    # 보낼 메시지 설정
    msg = MIMEText(' ')
    msg['Subject'] = '{0} 는 현재 RSI 30이하 - rsi : {1}!! '.format(symbols[count-1],rsi)
    s.sendmail("os1227os@gmail.com", "os1227os@naver.com", msg.as_string())
    s.quit()

  time.sleep(5)


