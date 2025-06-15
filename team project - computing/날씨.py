#웹 스크래핑, 기상청웹사이트의 데이터를 가져와 분석
import requests
from bs4 import BeautifulSoup

url = 'https://www.weather.go.kr/w/theme/world-weather.do?continentCode=C01&countryCode=127&cityCode=231'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
selector = "body > div.container > section > div > div.cont-wrap > div > div > div > div.box-b.clearfix > div.box-right > table > tbody > tr:nth-child(1) > td.icon-weather"
weather = soup.select_one(selector) #당일 날씨 분석해서 weather에 값 저장
print(weather.text)

#날씨마다 출력 실내,야외 활동 추천


if weather.text=='흐림':
  print('오늘은 흐린 날씨입니다.')
  print('흐린 날 하기 좋은 활동을 추천해 드릴까요?')
  대답 = input('응 혹은 아니 로 대답해주세요: ')
  if 대답 == '응':
    장소 = input('야외 혹은 실내를 골라주세요: ')
    if 장소 == '야외':
      print('흐린 날 하기 좋은 야외 활동 \n -간단한 야외 운동:조깅,인라인,자전거 \n -반려동물 산책 \n -노천 온천이나 야외 찜질방')
    elif 장소 == '실내':
      print('흐린 날 하기 좋은 실내 활동 \n -카페가서 조용히 과제,공부 등 집중해서 작업하기 \n -도서관가서 독서하기')

elif weather.text=='맑음':
  print('오늘은 맑은 날씨입니다.')
  print('맑은 날 하기 좋은 활동을 추천해 드릴까요?')
  대답 = input('응 혹은 아니 로 대답해주세요: ')
  if 대답 == '응':
    장소 = input('야외 혹은 실내를 골라주세요: ')
    if 장소 == '야외':
      print('맑은 날 하기 좋은 야외 활동 \n -공원 혹은 동네 산책하기 \n -야외카페에서 브런치 먹기 \n -피크닉이나 캠핑가서 힐링하기')
    elif 장소 == '실내':
      print('맑은 날 하기 좋은 실내 활동 \n -햇살 좋은 창가에서 독서하기 \n -집에서 창문열어두고 홈브런치 직접 해먹기')

elif weather.text=='구름많음':
  print('오늘은 구름이 많은 날입니다.')
  print('구름이 많은 날 하기 좋은 활동을 추천해 드릴까요?')
  대답 = input('응 혹은 아니 로 대답해주세요: ')
  if 대답 == '응':
    장소 = input('야외 혹은 실내를 골라주세요: ')
    if 장소 == '야외':
      print('구름이 많은 날 하기 좋은 야외 활동 \n -간단한 야외 운동:조깅,인라인,자전거 \n -반려동물 산책 \n -노천 온천이나 야외 찜질방')
    elif 장소 == '실내':
      print('구름이 많은 날 하기 좋은 실내 활동 \n -카페가서 조용히 과제,공부 등 집중해서 작업하기 \n -도서관가서 독서하기')

elif weather.text=='비':
  print('오늘은 비가 올 것으로 예상됩니다.')
  print('비가 오는 날 하기 좋은 활동을 추천해 드릴까요?')
  대답 = input('응 혹은 아니 로 대답해주세요: ')
  if 대답 == '응':
    장소 = input('야외 혹은 실내를 골라주세요: ')
    if 장소 == '야외':
      print('비가 오는 날 하기 좋은 야외 활동 \n -우산 쓰고 조용한 골목길 걷기 \n -빗소리 들으며 카페 투어하기 \n -비 오는 날 컨셉으로 사진 촬영하기')
    elif 장소 == '실내':
      print('비가 오는 날 하기 좋은 실내 활동 \n -영화보기 \n -미술관,박물관 관람하기 \n -집에서 베이킹하기 \n -독서,글쓰기,음악감상 등 집에서 간단한 활동하기 \n -보드게임이나 게임하기')