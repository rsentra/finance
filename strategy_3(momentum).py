# -*- coding: utf-8 -*-
"""
Created on Sat May  1 19:10:42 2021
모멘텀 전략이란 쉽게 말해서 최근에 가장 많이 오른 종목을 매수한 후 일정 기간을 보유한 후 파는 전략을 의미합니다
@author: admin
"""
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

stocks = pd.read_excel("d:/myPython/finance/datas.xlsx", index_col=0)
# ret = (금일종가 - 60일전 종가) / 60일전 종가 => pct_change() 메소드 
ret_stocks = stocks.pct_change(60)
s = ret_stocks.iloc[-1]
moment_df = pd.DataFrame(s)
moment_df.columns = ['모멘텀']
moment_df['순위'] = moment_df['모멘텀'].rank(ascending=False)
moment_df = moment_df.sort_values(by='순위')

moment_df[:10]
다른 정보와 결합하여 정제할 필요가 있음
