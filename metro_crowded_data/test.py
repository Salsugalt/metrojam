import requests
import pprint
import pandas as pd
from os import name
import bs4
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse as ps
page = 1
perPage = 1667
url = 'https://api.odcloud.kr/api/15071311/v1/uddi:a5158b81-27c7-4151-ba6c-b912a6f13d39'
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
# 정규식
pattern = re.compile(r"%")
# XML 데이터를 순회하며 데이터프레임에 추가
for row in xml_obj.findall('.//item'):
    row_data = {}
    for col in row.findall('.//col'):
        if pattern.search(col.attrib['name']):
            row_data[col.attrib['name']] = col.text
    if row_data:  # row_data가 비어있지 않으면 추가
        rows.append(row_data)

# pddf
df = pd.DataFrame(rows)
print(df)
#df.to_csv('output.csv', index=False)

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