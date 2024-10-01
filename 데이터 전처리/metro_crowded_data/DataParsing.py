import requests
#import pprint
import pandas as pd
#from os import name
#import bs4
#import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse as ps

page = 1
perPage = 1667 #모든 데이터의 최대 페이지
year = 2019 #초기값

#api 목록
api = [#'uddi:a5158b81-27c7-4151-ba6c-b912a6f13d39', 2017 --> column namspace 동떨어진 일관성 데이터삭제
        'uddi:70e3a3d3-0872-4828-8234-f0bca459b44f', #2019
        'uddi:99771417-a036-46f1-8ad5-8edf4591c2ee', #2020
        'uddi:b3803d43-ffe3-4d17-9024-fd6cfa37c284', #2021
        'uddi:75461a18-17a3-42fe-9322-a51148003b69', #2022
        'uddi:e477f1d9-2c3a-4dc8-b147-a55584583fa2', #2023
        'uddi:c87b6af0-0ef7-4182-b172-fd2680a79d6f', #2024/03
        'uddi:9aff0ee6-26e7-42c4-af0c-84bf31680ca9'] #2024/06 --> 최근년도는 분기마다 나오고 다음해에 통합되는 데이터인지 확인 불가


url = 'https://api.odcloud.kr/api/15071311/v1/' + api[0]
params = {'serviceKey' : '9bi5h25Oa1d6yB2qd+7vNhE7qWLhgJvDSr4dTv6vhlZ3rvlpNTbs6NZv/B+R/CvFLssD7Flh+jSDAYydOoaRfQ==', #decoding key
          'returnType' : 'XML',
        'page' : page, 'perPage' : perPage}

response = requests.get(url, params=params)
data = response.text

#XML 데이터를 순회하며 데이터프레임에 추가
def parsing(data):
  xml_obj = ET.fromstring(data)
  rows = []
  for row in xml_obj.findall('.//item'):
     row_data = {}
     for col in row.findall('.//col'):
          if col.attrib['name'] == "조사일자": 
            row_data['요일구분'] = col.text #조사일자(19,21) = 요일구분(나머지모두), 구분(19,21) = 상하구분(나머지모두)
          if col.attrib['name'] == "구분":
            row_data['상하구분'] = col.text
          else:
           row_data[col.attrib['name']] = col.text
     if row_data:
          rows.append(row_data)
  column_list = ['년도', '호선', '상하구분', '역명', '역번호', '요일구분','5시30분', '6시00분', '6시30분', '7시00분', '7시30분', '8시00분',
                '8시30분', '9시00분', '9시30분', '10시00분', '10시30분', '11시00분', '11시30분', '12시00분', '12시30분', '13시00분',
                  '13시30분', '14시00분', '14시30분', '15시00분', '15시30분', '16시00분', '16시30분', '17시00분', '17시30분', '18시00분',
                      '18시30분', '19시00분', '19시30분', '20시00분', '20시30분', '21시00분', '21시30분', '22시00분', '22시00분', '23시00분',
                        '23시30분', '24시00분', '24시30분']
  df = pd.DataFrame(rows, columns=column_list)
  df['년도'] = year
  return df

df = parsing(data)
print(df)
#df.to_csv('output.csv', index=False)
#result = pd.concat([df1, df2], ignore_index=True)

