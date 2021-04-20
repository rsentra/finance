# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:38:58 2021
 
financedatareader를 이용해 상장종목,시세정보를 읽어온다

@author: admin
"""

# 소스 :  https://github.com/FinanceData/FinanceDataReader


import FinanceDataReader as fdr

# 1. 한국거래소 상장종목 리스트/시총
df_krx = fdr.StockListing('KRX') # KRX, KOSPI, KOSDAQ, KONEX 중 하나 
df_krx.head()
df_kospi = fdr.StockListing('KOSPI')
df_marcap = fdr.StockListing('KRX-MARCAP') # 시가총액
df_del = fdr.StockListing('KRX-DELISTING') # 상폐종목


# 2. 개별종목 일자별 시세 ---------------------
# 카카오, 2021년 일자별 시세
df = fdr.DataReader('035720', '2021')
df.head(10)

df['Close'].plot()

# KS11 (KOSPI 지수), 2019년~현재
df = fdr.DataReader('KS11', '2019')
df['Close'].plot()


# 여러종목
stock_list = [
  ["삼성전자", "005930"],
  ["SK하이닉스", "000660"],
  ["현대차", "005380"],
  ["셀트리온", "068270"],
  ["LG화학", "051910"],
  ["POSCO", "005490"],
  ["삼성물산", "028260"],
  ["NAVER", "035420"],
  ["KAKAO", "035720"],
]
import pandas as pd

df_list = [fdr.DataReader(code, '2020-01-01', '2021-04-30')['Close'] for name, code in stock_list]
len(df_list)

# pd.concat()로 합치기
df = pd.concat(df_list, axis=1)
df.columns = [name for name, code in stock_list] 
df.head(10)

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'C:/Windows/Fonts/mglugunsl.ttf'
fontprop = fm.FontProperties(fname=font_path, size=14)
df.plot()


df[['NAVER', 'KAKAO']].plot()

# 가격차가 큰 경우 비교
df[['LG화학', '삼성전자']].plot(secondary_y=['LG화학'])
df[['NAVER', 'KAKAO']].plot(secondary_y=['KAKAO'])


# 시작점을 같게하고 비교
df2 = df[['NAVER', 'KAKAO']]

df_plot = df2 / df2.iloc[0] - 1.0
df_plot.plot()

# 기간 수익율 비교
df = pd.concat(df_list, axis=1)
df.columns = [name for name, code in stock_list] 
df_norm = df / df.iloc[0] - 1.0
df_norm.iloc[-1].sort_values(ascending=False)


# 3. 상장종목 리스트로 1) 시총 비교 2)전일대비 하락 ------------------------
df_sorted = df_marcap.sort_values('Marcap',ascending=False)

# 시총 1000억대
df_1000 = df_sorted[(df_sorted['Marcap']>=1000) & (df_sorted['Marcap']<=2000)]
df_1000.query("Market=='KOSPI'")

# 전일 5% 하락
df_sorted.query("Market=='KOSPI' & Changes / Open < -0.05") 


url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
df_listing = pd.read_html(url, header=0)[0]