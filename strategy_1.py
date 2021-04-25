# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 11:45:10 2021
가치+모멘텀 투자전략
참고- https://jsp-dev.tistory.com/92
@author: admin
"""

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

df_finance = pd.read_excel("d:/myPython/finance/naverFinance.xlsx")
df_price =  pd.read_excel("d:/myPython/finance/datas.xlsx", index_col=0)

MONTH_AGO = datetime.today()+ relativedelta(months = -1)
MONTH_AGO = MONTH_AGO.strftime('%Y-%m-%d')

YEAR_AGO = datetime.today()+ relativedelta(years = -1)
YEAR_AGO = YEAR_AGO.strftime('%Y-%m-%d')
                        
price_month_ago = []
price_year_ago = []

for index, row in df_finance.iterrows():
    name = row['종목명']
    if name in df_price.columns:
        price_month_ago.append(df_price.loc[MONTH_AGO,name])
        price_year_ago.append(df_price.loc[YEAR_AGO,name])
    else:
        price_month_ago.append(0)
        price_year_ago.append(0)

df_finance['price_month_ago'] = price_month_ago
df_finance['price_year_ago'] = price_year_ago

df_finance = df_finance.reset_index(drop=True)
# 시총상위 200개 대상
df_finance = df_finance.loc[:200]
# 1차: 가치평가
# bpr  = 1 / pbr
df_finance['BPR'] = 1 / df_finance['PBR'].astype(float)
df_finance['1/PER'] = 1 / df_finance['PER'].str.replace(',','').astype(float)
df_finance['RANK_BPR'] = df_finance['BPR'].rank(method='max',ascending=False)
df_finance['RANK_1/PER'] = df_finance['PER'].rank(method='max',ascending=False)
df_finance['RANK_VALUE'] = (df_finance['RANK_BPR']+df_finance['RANK_1/PER'])/2
df_finance = df_finance.sort_values(by=['RANK_VALUE'])
df_finance = df_finance.reset_index(drop=True)
df_finance = df_finance.loc[:75]
 
# 2차 모멘텀평가
df_finance['현재가'] = df_finance['현재가'].str.replace(',','').astype(float) 

df_finance['momentum_month'] = df_finance['현재가'] - df_finance['price_month_ago']
df_finance['1달등락율'] = (df_finance['현재가']-df_finance['price_month_ago'])/df_finance['현재가'] 

df_finance['momentum_year'] = df_finance['현재가'] - df_finance['price_year_ago']
df_finance['1년등락율'] = (df_finance['현재가']-df_finance['price_year_ago'])/df_finance['현재가'] 

df_finance['FINAL_MOMENTUM'] = df_finance['1년등락율'] - df_finance['1달등락율']
df_finance['RANK_MOMENTUM'] = df_finance['FINAL_MOMENTUM'].rank(method='max',ascending=False)

#3, 최종평가
df_finance['FINAL_RANK'] = (df_finance['RANK_VALUE'] + df_finance['RANK_MOMENTUM'] ) / 2
df_finance = df_finance.sort_values(by=['FINAL_RANK'],ascending=True)
df_finance = df_finance.reset_index(drop=True)
print(df_finance)
df_finance.to_excel("d:/myPython/finance/strategy_1.xlsx")