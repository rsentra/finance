# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:20:26 2021

@author: User
"""

import pandas as pd
import requests

def get_financial_statement(code):
    url = f'http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode={code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
    #url = f'http://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode={code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701'
    res = requests.get(url)
    fs_tables = pd.read_html(res.text)
    
    temp_df = fs_tables[0]
    if temp_df.loc[0][0] != "매출액":
        print("매출액없음")
        return None
        
    temp_df = temp_df.set_index(temp_df.columns[0]) # 첫컬럼으로 index
    
    temp_df = temp_df.loc[['매출액','매출총이익','영업이익','당기순이익']]
    
    temp_df2 = fs_tables[2]
    temp_df2 = temp_df2.set_index(temp_df2.columns[0])
    temp_df2 = temp_df2.loc[['자산','부채','자본']]
    
    temp_df = temp_df[list(temp_df2.columns)]
    fs_df = pd.concat([temp_df,temp_df2])
    return fs_df

code ='A108320'
df = get_financial_statement(code)