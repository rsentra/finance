# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 17:53:41 2021
업종별 시세를 크롤링
@author: admin
"""
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from naverCrawl import get_fields

fields = []
    
# --업종별시세 및 네이버 분류 코드
def upjong_sise():
    res= requests.get('https://finance.naver.com/sise/sise_group.nhn?type=upjong')
    page_soup = BeautifulSoup(res.text,'lxml')
    table_html = page_soup.select_one('table.type_1')
            
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x:
                            (x.name == 'a' and 'upjong' in x.get('href',[])) or
                            (x.name == 'td' and 'number' in x.get('class',[])) 
                       )]
        
    upjong_code = [item.get('href').split('=')[-1] for item in table_html.find_all(lambda x:
                            (x.name == 'a' and 'upjong' in x.get('href',[])) 
                       )]
    number_data = np.array(inner_data)
    number_data.resize(len(upjong_code), int(len(inner_data)/len(upjong_code)))
    df = pd.DataFrame(data=number_data)    
    df.index = upjong_code
    
    global fields
    total_page_num, fields = get_fields('0') # kospi기준 필드명 추출
    
    return df.reset_index()

# 업종내 종목별 시세
def upjong_sise_detail(upjong_code):
    BASE_URL='https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no='
    # post방식으로 지정필드 가져오는것 안됨
    # global fields
    # data = {'menu': 'sise_group_detail',
    #             'fieldIds': fields,
    #             'returnUrl': BASE_URL+str(upjong_code)}
    # # post 요청
    # res = requests.post('https://finance.naver.com/sise/field_submit.nhn',data=data)
    
    res = requests.get(BASE_URL+str(upjong_code)) 
       
    page_soup = BeautifulSoup(res.text,'lxml')
    table_html = page_soup.select('div.box_type_l')[1] #한페이지에 class 이름동일-2번째
    header_data = [item.get_text().strip() for item in table_html.select('thead th')][1:-1]
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x:
                            (x.name == 'a' and 'tltle' in x.get('class',[])) or
                            (x.name == 'td' and 'number' in x.get('class',[])) 
                       )]
    
    # no_data = [item.get_text().strip() for item in table_html.select('td.name')]
    # 종목코드/회사명 찾기
    no_data = [ item.get('href').split('=')[-1] + item.get_text().strip()  for item in table_html.find_all(lambda x:
                            (x.name == 'a' and 'main' in x.get('href',[])) 
                       )]
    stock_code = [ x[:6] for x in no_data]
    stock_name = [ x[6:] for x in no_data]
    
    number_data = np.array(inner_data)
    #가로,세로 resize
    number_data.resize(len(no_data), len(header_data))
    df = pd.DataFrame(data=number_data, columns = header_data)
    df['code'] = stock_code
    df['name'] = stock_name
    return df

if __name__ == "__main__":
    #업종목록
    df = upjong_sise()
    df.rename(columns={'index':'업종코드',0:'업종명'},inplace=True)
    #업종별 종목시세
    df_detail = pd.DataFrame()
    for i, row in df.iterrows():
        upjong_code = row['업종코드']
        df = upjong_sise_detail(upjong_code)  
        df['업종코드'] = upjong_code
        df['업종명'] = row['업종명']
        df_detail = df_detail.append(df)      #df 합침
        # if i > 10:
        #     break
    
    df_detail.to_excel("d:/myPython/finance/naverFinance-upjong.xlsx")
    print("job completed")

