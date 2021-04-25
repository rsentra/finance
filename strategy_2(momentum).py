# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 16:50:44 2021
모멘텀 전략 실행
참고
https://jsp-dev.tistory.com/82?category=808569
@author: admin
"""

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
# import sys
from scipy.stats import linregress
import numpy as np

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)

stocks = pd.read_excel("d:/myPython/finance/datas.xlsx", index_col=0)
symbols = stocks.columns

start = datetime.today()
#최근 1년치만..
year_ago = datetime.today()+ relativedelta(years = -1)
year_ago = year_ago.strftime('%Y-%m-%d')
stocks = stocks.reset_index()
stocks = stocks.loc[stocks['Date']>=year_ago].set_index('Date')

# momentum function
def momentum(closes):
    returns = np.log(closes)
    x = np.arange(len(returns))
    slope, _, rvalue, _,_ = linregress(x, returns)
    return ((1+ slope) ** 252) * (rvalue ** 2) 

momentums = stocks.copy(deep=True)
for symbol in symbols:
    momentums[symbol] = stocks[symbol].rolling(90).apply(momentum,raw=False)

# 상위 5개만
bests = momentums.max().sort_values(ascending=False).index[:5]
for best in bests:
    end = momentums[best].index.get_loc(momentums[best].idxmax()) #모멘텀 가장 높은 시점
    if end - 90 < 0:
        continue
    
    rets = np.log(stocks[best].iloc[end - 90 : end])
    momentum_point = stocks[best].index[end].strftime('%Y/%m/%d')
    
    x= np.arange(len(rets))
    slope, intercept, r_value, p_value, std_err = linregress(x, rets) #회귀함수
    
    try:
        plt.plot(np.arange(180),stocks[best][end-90: end+90],label=[best,momentum_point])
        plt.plot(x, np.e ** (intercept + slope*x)) #회귀함수결과 plot
    except:
        continue
    
ax.legend(loc=5)
plt.show()
end = datetime.today()
print('processing time.. ' , end - start)
