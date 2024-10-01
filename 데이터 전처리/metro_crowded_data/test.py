import requests
import pprint
import pandas as pd
from os import name
#import bs4
#import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse as ps
page = 1
perPage = 1667 #모든 데이터의 최대 페이지
year = 2017 #초기값
#api 목록
uddi = ['uddi:a5158b81-27c7-4151-ba6c-b912a6f13d39', #2017 
        'uddi:70e3a3d3-0872-4828-8234-f0bca459b44f', #2019
        ]


url = 'https://api.odcloud.kr/api/15071311/v1/' + uddi
params = {'serviceKey' : '9bi5h25Oa1d6yB2qd+7vNhE7qWLhgJvDSr4dTv6vhlZ3rvlpNTbs6NZv/B+R/CvFLssD7Flh+jSDAYydOoaRfQ==', #decoding key
          'returnType' : 'XML',
        'page' : page, 'perPage' : perPage}
response = requests.get(url, params=params)

data = response.text
#pp = pprint.PrettyPrinter(indent=4)
#print(pp.pprint(data))
# XML 데이터를 파싱
xml_obj = ET.fromstring(data)
rows = []
# XML 데이터를 순회하며 데이터프레임에 추가
for row in xml_obj.findall('.//item'):
    row_data = {}
    for col in row.findall('.//col'):
        row_data[col.attrib['name']] = col.text
    if row_data:  # row_data가 비어있지 않으면 추가
        rows.append(row_data)
# 2017년도 컬럼이름
column_list = ['년도','호선', '방향','역명','역번호','요일',"5:30~ (%)","6:00~ (%)","6:30~ (%)","7:00~ (%)","7:30~ (%)","8:00~ (%)","8:30~ (%)","9:00~ (%)","9:30~ (%)","10:00~ (%)","10:30~ (%)","11:00~ (%)",
               "11:30~ (%)","12:00~ (%)","12:30~ (%)","13:00~ (%)","13:30~ (%)","14:00~ (%)","14:30~ (%)","15:00~ (%)","15:30~ (%)","16:00~ (%)","16:30~ (%)","17:00~ (%)","17:30~ (%)","18:00~ (%)",
               "18:30~ (%)","19:00~ (%)","19:30~ (%)","20:00~ (%)","20:30~ (%)","21:00~ (%)","21:30~ (%)","22:00~ (%)","22:30~ (%)","23:00~ (%)","23:30~ (%)","24:00~ (%)","24:30~ (%)"]
df = pd.DataFrame(rows, columns=column_list)
df.columns = ['year','line','direction','st_name','st_no','day','530','600','630','700','730','800','830','900','930','1000','1030','1100','1130','1200','1230','1300','1330','1400','1430',
                   '1500','1530','1600','1630','1700','1730','1800','1830','1900','1930','2000','2030','2100','2130','2200','2230','2300','2330','2400','2430']
df['year'] = year
print(df)
df.to_csv('output.csv', index=False)

#혼잡도api model 2017년데이터와 이후데이터의 컬럼이름이 다름

column_list = ['년도','호선', '방향','역명','역번호','요일',"5:30~ (%)","6:00~ (%)","6:30~ (%)","7:00~ (%)","7:30~ (%)","8:00~ (%)","8:30~ (%)","9:00~ (%)","9:30~ (%)","10:00~ (%)","10:30~ (%)","11:00~ (%)",
               "11:30~ (%)","12:00~ (%)","12:30~ (%)","13:00~ (%)","13:30~ (%)","14:00~ (%)","14:30~ (%)","15:00~ (%)","15:30~ (%)","16:00~ (%)","16:30~ (%)","17:00~ (%)","17:30~ (%)","18:00~ (%)",
               "18:30~ (%)","19:00~ (%)","19:30~ (%)","20:00~ (%)","20:30~ (%)","21:00~ (%)","21:30~ (%)","22:00~ (%)","22:30~ (%)","23:00~ (%)","23:30~ (%)","24:00~ (%)","24:30~ (%)"]
df = pd.DataFrame(rows, columns=column_list)
df.columns = ['year','line','direction','st_name','st_no','day','530','600','630','700','730','800','830','900','930','1000','1030','1100','1130','1200','1230','1300','1330','1400','1430',
                   '1500','1530','1600','1630','1700','1730','1800','1830','1900','1930','2000','2030','2100','2130','2200','2230','2300','2330','2400','2430']
df['year'] = year






"""
xml_obj = ET.fromstring(data)
match_Cnt = xml_obj.find('matchCount').text
rows = xml_obj.findall('.//col') #xpath 표현식

for row in rows:
   if row.attrib['name'] == 
      print(f"{row.attrib['name']} : {row.text}")
   
"""
"""
xml_obj = bs4.BeautifulSoup(data, 'lxml-xml')
matchCount = xml_obj.find('matchCount')
page = xml_obj.find('page')
perPage = xml_obj.find('perPage')
totalCount = xml_obj.find('totalCount')
rows = xml_obj.find('item')
#print(page, perPage, matchCount, totalCount)

#pattern = re.compile('^item')
#rows = [elem for elem in xml_obj.iter() if any(pattern.match(key) for key in elem.attrib)]
#xml 객체의 모든 하위 요소들을 순회하면서 조건에 만족하는 요소를 리스트에 포함

for row in rows:
   print(ET.tostring(row, encoding='unicode'))

# 속성 이름이 'col'로 시작하는 요소 찾기 및 딕셔너리에 저장
columns = {}
for elem in xml_obj.iter('col'):
    col_name = elem.get('name')
    col_value = elem.text
    columns[col_name] = col_value
"""
"""
#정규식
pattern = re.compile(r"%")
# XML 데이터를 순회하며 데이터프레임에 추가
for row in xml_obj.findall('.//item'):
    row_data = {}
    for col in row.findall('.//col'):
        if pattern.search(col.attrib['name']):
            row_data[col.attrib['name']] = col.text
    if row_data:  # row_data가 비어있지 않으면 추가
        rows.append(row_data)
"""