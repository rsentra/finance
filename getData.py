# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:22:45 2021
krx 상장사의 종가를 수집하는 스크립트
참고- https://jsp-dev.tistory.com/92
@author: admin
"""

import pandas as pd
import FinanceDataReader as fdr
from time import time
from concurrent.futures import ProcessPoolExecutor

df_krx = fdr.StockListing('KRX')
df_krx['SymbolName'] = df_krx['Symbol'] + df_krx['Name']
codes = df_krx['SymbolName']
START_YEAR = '2020' #종가 수집 시작년도

def get_price(code):
    if code[:5].isdigit(): 
        df_price = fdr.DataReader(code[:6],START_YEAR)
    else:
        return None
    
    if  len(df_price) > 0:
        df_price = df_price[['Close']]
        df_price.columns = [code[6:]]
        return df_price


if __name__ == "__main__":
    start = time()
    pool = ProcessPoolExecutor(max_workers=10)
    # stock list에 대해 종가 수집
    results = list(pool.map(get_price,codes))
    df_stocks = pd.concat(results, axis= 1)
    end = time()
    print('processing time = ', end - start)
    df_stocks.to_excel("d:/myPython/finance/datas.xlsx")

