import requests
import pprint
import pandas as pd
from os import name
import bs4
import re
import xml.etree.cElementTree as ET

page = 0
url = 'https://api.odcloud.kr/api/15071311/v1/uddi:a5158b81-27c7-4151-ba6c-b912a6f13d39'
params = {'serviceKey' : '9bi5h25Oa1d6yB2qd+7vNhE7qWLhgJvDSr4dTv6vhlZ3rvlpNTbs6NZv/B+R/CvFLssD7Flh+jSDAYydOoaRfQ==', #decoding key
          'returnType' : 'XML',
        'page' : page, 'perPage' : '1'}
response = requests.get(url, params=params)
""" for npage in page(0,5):
    response = requests.get(url, params=params)
    print("현재페이지", page)
    print(response.content)
"""
data = response.text


#pp = pprint.PrettyPrinter(indent=4)
#print(pp.pprint(data))

"""
xml_obj = bs4.BeautifulSoup(data, 'lxml-xml')
matchCount = xml_obj.find('matchCount')
page = xml_obj.find('page')
perPage = xml_obj.find('perPage')
totalCount = xml_obj.find('totalCount')
rows = xml_obj.find('item')
 
#print(rows)
#print(page, perPage, matchCount, totalCount)


rows = xml_obj.find('class':re.compile('^col')) <-- bs4에서만 작동 et에서 x
"""
xml_obj = ET.fromstring(data)
match_Cnt = xml_obj.find('matchCount').text

#pattern = re.compile('^item')
#rows = [elem for elem in xml_obj.iter() if any(pattern.match(key) for key in elem.attrib)]
#xml 객체의 모든 하위 요소들을 순회하면서 조건에 만족하는 요소를 리스트에 포함

#for row in rows:
#    print(ET.tostring(row, encoding='unicode'))

"""
# 속성 이름이 'col'로 시작하는 요소 찾기 및 딕셔너리에 저장
columns = {}
for elem in xml_obj.iter('col'):
    col_name = elem.get('name')
    col_value = elem.text
    columns[col_name] = col_value

# 결과 출력
print(columns)
print(match_Cnt)
"""

xml_obj = bs4.BeautifulSoup(data, 'lxml-xml')
item = xml_obj.findAll('item')
print(item)
print(match_Cnt)