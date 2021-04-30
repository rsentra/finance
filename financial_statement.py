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
    if len(res.text) < 100:
        return False, None
    fs_tables = pd.read_html(res.text)
    
    temp_df = fs_tables[0]
    if temp_df.loc[0][0] != "매출액":
        print("매출액 항목이 없는 업종/ 종목code = ",code)
        return False, None
        
    temp_df = temp_df.set_index(temp_df.columns[0]) # 첫컬럼으로 index
    
    temp_df = temp_df.loc[['매출액','매출총이익','영업이익','당기순이익']]
    
    temp_df2 = fs_tables[2]
    temp_df2 = temp_df2.set_index(temp_df2.columns[0])
    temp_df2 = temp_df2.loc[['자산','부채','자본']]
    
    temp_df = temp_df[list(temp_df2.columns)]
    fs_df = pd.concat([temp_df,temp_df2])
    return True, fs_df


df_finance = pd.read_excel("naverFinance-upjong.xlsx", index_col='code')
upjong_nm ='화장품'
for i, row in df_finance.iterrows():
    if not i.isdigit():  #우선주 등 재무제표 없는 코드 skip
        print('skip = ', i)
        continue
    if  row['업종명'] == upjong_nm: 
        code = 'A' + i 
        res, df_fs = get_financial_statement(code)
        if res:
            df_finance.loc[i,'growth_margin'] = df_fs.loc['매출총이익'][df_fs.shape[1]-1]

print('job completed....')