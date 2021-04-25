# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 00:09:18 2021
네이버 시가총액 페이지에서 상장사별 시가총액,per,pbr등 수집
참고- https://jsp-dev.tistory.com/92
@author: admin
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

BASE_URL = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok='
KOSPI_CODE = 0
KOSDAK_CODE = 1
START_PAGE = 1
fields = []

def main(code):
    #total page가져오기
    res = requests.get(BASE_URL+str(code)+ "&page=" + str(START_PAGE))
    # print('ss',res)
    page_soup = BeautifulSoup(res.text,'lxml')
    total_page_num = page_soup.select_one('td.pgRR > a')
    total_page_num = int(total_page_num.get('href').split('=')[-1])
    
    # 가져올 수 있는 항목명
    item_html = page_soup.select_one('div.subcnt_sise_item_top')
    global fields
    fields = [item.get('value') for item in item_html.select('input')]
    
    # 1페이지부터 차례대로 crawl
    result = [crawl_by_page(code,str(page)) for page in range(1,total_page_num + 1)]
    # 수집한 결과를 엑셀로 
    df = pd.concat(result, axis=0, ignore_index=True)
    df.to_excel("d:/myPython/finance/naverFinance.xlsx")

def crawl_by_page(code,page):
    global fields
    if page==0:
        print(fields)
    data = {'menu': 'market_sum',
            'fieldIds': fields,
            'returnUrl': BASE_URL+str(code)+ "&page=" + str(page)}
    # post 요청
    res = requests.post('https://finance.naver.com/sise/field_submit.nhn',data=data)
    
    page_soup = BeautifulSoup(res.text,'lxml')
    table_html = page_soup.select_one('div.box_type_l')
    
    header_data = [item.get_text().strip() for item in table_html.select('thead th')][1:-1]
    #종목명/수치 추출(종목명 title이 아닌 tltle임?)
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x:
                        (x.name == 'a' and 'tltle' in x.get('class',[])) or
                        (x.name == 'td' and 'number' in x.get('class',[])) 
                   )]
    #page에 있는 종목의 순번                                                       
    no_data = [item.get_text().strip() for item in table_html.select('td.no')]
    number_data = np.array(inner_data)
    #가로,세로 resize
    number_data.resize(len(no_data), len(header_data))
    df = pd.DataFrame(data=number_data, columns = header_data)
    return df


main(KOSPI_CODE)
