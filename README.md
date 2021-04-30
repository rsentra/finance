# finance
분석대상
1. 거래량 폭증
   - 당일 거래량이 최근 1년(또는 6개월 평균대비) 10배 이상 폭증
   - PER가 낮은 종목
   - 시가총액금액 또는 상위 ?%
  => 대상 종목선정
  => get_data(일별시세)로 분석
     naver_crawl (회사별 시총,per,pbr등 활용)
  
2. PER 분석
   - 업종PER보다 낮은 경우
   - 순이익 >0 / ROE >= ?%
   - 업종분류는 navercrawl_sector 활용
      
3. 저평가주 찾기
   - EPS * ROE(미래가치반영) < 주가
   - 현재 ROE의 경우 부채가 많으면 희석되므로 부채비율로 보완 필요
   - PBR 또는 다른 조건으로 보완 
   
4. 가치+모멘텀 분석
    strategy_1.py

5. 매출총이익: financial_statement.py


EPS(earing per share) = 당기순이익 / 주식수			
ROE(return in equity) = 당기순이익 / 자기자본 = EPS / BPS
BPS(book-value per share) = 자기자본 / 주식수
PER(price earning ratio) = 시가총액 / 당기순이익 = 주가/ EPS	
PBR(price book-value ratio) = 시가총액 / 자기자본 = 주가 / BPS = ROE * PER
ROA(return on asset) = 당기순이익 / 총자산
GP/A = 매출총이익 / 총자산
수퍼개미적정주가 = EPS * ROE(미래가치반영)

