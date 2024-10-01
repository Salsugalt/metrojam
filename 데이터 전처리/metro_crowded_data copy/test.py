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
year = 2017
uddi = 'uddi:70e3a3d3-0872-4828-8234-f0bca459b44f'
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
# 2017_column_list
column_list = ['년도','호선', '방향','역명','역번호','요일',"5:30~ (%)","6:00~ (%)","6:30~ (%)","7:00~ (%)","7:30~ (%)","8:00~ (%)","8:30~ (%)","9:00~ (%)","9:30~ (%)","10:00~ (%)","10:30~ (%)","11:00~ (%)",
               "11:30~ (%)","12:00~ (%)","12:30~ (%)","13:00~ (%)","13:30~ (%)","14:00~ (%)","14:30~ (%)","15:00~ (%)","15:30~ (%)","16:00~ (%)","16:30~ (%)","17:00~ (%)","17:30~ (%)","18:00~ (%)",
               "18:30~ (%)","19:00~ (%)","19:30~ (%)","20:00~ (%)","20:30~ (%)","21:00~ (%)","21:30~ (%)","22:00~ (%)","22:30~ (%)","23:00~ (%)","23:30~ (%)","24:00~ (%)","24:30~ (%)"]
df = pd.DataFrame(rows, columns=column_list)
df.columns = ['year','line','direction','st_name','st_no','day','530','600','630','700','730','800','830','900','930','1000','1030','1100','1130','1200','1230','1300','1330','1400','1430',
                   '1500','1530','1600','1630','1700','1730','1800','1830','1900','1930','2000','2030','2100','2130','2200','2230','2300','2330','2400','2430']
df['year'] = year
print(df)
df.to_csv('output.csv', index=False)
