#서울교통공사 지하철 혼잡도 (https://www.data.go.kr/data/15071311/fileData.do#/tab-layer-openapi)
#서울교통공사 1-8호선 30분 단위 평균 혼잡도로 30분간 지나는 열차들의 평균 혼잡도(정원대비 승차인원으로,
#승차인과 좌석수가 일치할 경우를 혼잡도 34%로 산정) 입니다.(단위: %). 서울교통공사 혼잡도 데이터는 요일구분(평일, 토요일, 일요일),
#호선, 역번호, 역명, 상하선구분, 30분단위 별 혼잡도 데이터로 구성되어 있습니다. (2024년 부터 분기별 데이터가 제공됩니다.)
#연평균, 24년이후 분기 평균 데이터(시간별, 탑승역, 탑승라인, 주말여부, 해당연도, 방향)
#컬럼 [year, line, direction, staion_name, staion_id, day_type, time, time_nomallized, time_float, congstion]
#결측값은 0 으로 처리됨
#1호선은 서울역부터 동묘앞까지의 데이터 밖에 없음[station_id = 150~159] (이외의 역 혼잡도 제공x)
#2호선 신정지선, 성수내선의 실제 역번호와 다름(영향 x)
#3호선 실제 역번호보다 전부 -10 되어있음 (영향x)
#4호선 과천선 안산선 데이터x , 진접선 데이터 o, 407번 개통아직이라 데이터x

#5~8호선 역번호 실제 역번호에 +2001
#5호선 본선의 하남선 데이터x, 마천지선 데이터 o
#6호선 전부 정상
#7호선 역번호에 추가로 +1, 장암역(실제번호 709) ~ 부평구청역(실제번호 759)
#8호선 역번호 추가로 -1, 암사역(실제번호 810) ~ 모란역(실제번호 827)

import pandas as pd
import requests
import xml.etree.ElementTree as ET
import numpy as np

# API 설정
page = 1
perPage = 1667
merged_data = {}
api = [
    'uddi:70e3a3d3-0872-4828-8234-f0bca459b44f',  # 2019
    'uddi:99771417-a036-46f1-8ad5-8edf4591c2ee',  # 2020
    'uddi:b3803d43-ffe3-4d17-9024-fd6cfa37c284',  # 2021
    'uddi:75461a18-17a3-42fe-9322-a51148003b69',  # 2022
    'uddi:e477f1d9-2c3a-4dc8-b147-a55584583fa2',  # 2023
    'uddi:c87b6af0-0ef7-4182-b172-fd2680a79d6f',  # 2024/03
    'uddi:9aff0ee6-26e7-42c4-af0c-84bf31680ca9',  # 2024/06
    'uddi:da7cd08f-94f0-4dba-b33d-d02dcb35b57b'   # 2024/09
]

# API 데이터 요청
service_key = '9bi5h25Oa1d6yB2qd+7vNhE7qWLhgJvDSr4dTv6vhlZ3rvlpNTbs6NZv/B+R/CvFLssD7Flh+jSDAYydOoaRfQ=='
for uddi in api:
    url = f'https://api.odcloud.kr/api/15071311/v1/{uddi}'
    params = {'serviceKey': service_key, 'returnType': 'XML', 'page': page, 'perPage': perPage}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        merged_data[uddi] = response.text
    except requests.RequestException as e:
        print(f"API 요청 실패: {uddi}, 에러: {e}")

# XML 데이터 파싱
def parsing(data, year):
    xml_obj = ET.fromstring(data)
    rows = []

    # XML 데이터를 딕셔너리로 변환
    for row in xml_obj.findall('.//item'):
        row_data = {}
        for col in row.findall('.//col'):
            if col.attrib['name'] == "조사일자":
                row_data['요일구분'] = col.text  # 조사일자 -> 요일구분
            elif col.attrib['name'] == "구분":
                row_data['상하구분'] = col.text  # 구분 -> 상하구분
            elif col.attrib['name'] == "출발역": # 출발역 -> 역명
                row_data['역명'] = col.text
            else:
                row_data[col.attrib['name']] = col.text  # 그 외의 경우 일반적으로 처리
        if row_data:
            rows.append(row_data)

    df = pd.DataFrame(rows)

    # 기본 매핑
    column_mapping = {
        '년도': 'year', '호선': 'line', '상하구분': 'direction',
        '역명': 'station_name', '역번호': 'station_id', '요일구분': 'day_type'
    }


    # 기본 컬럼명 매핑
    df = df.rename(columns=column_mapping)

    # 년도 추가
    df['year'] = year

    # '연번' 컬럼 제거
    if '연번' in df.columns:
        df = df.drop(columns=['연번'])

    return df

# 각 년도의 데이터 병합
years = [2020, 2021, 2022, 2023, 202403, 202406, 202409]
final_df = pd.concat([parsing(merged_data[uddi], year) for uddi, year in zip(api, years)], ignore_index=True)

# 데이터 변환 및 필터링
final_df['line'] = final_df['line'].replace({'13': '2', '14': '2', '15': '5'})  # 라인 수정
final_df = final_df[~final_df['line'].isin(['성수지선', '신정지선'])]  # 특정 라인 제거
final_df['line'] = final_df['line'].replace({f'{i}호선': str(i) for i in range(1, 9)})

# 데이터를 '시간'과 '혼잡도'로 변형
final_df = pd.melt(final_df,
                      id_vars=['year', 'line', 'direction', 'station_name', 'station_id', 'day_type'],
                      var_name='time',
                      value_name='congestion')
#시간대 매핑 수치형 데이터 변환 new
def convert_time_to_float(time_str):
    hour, minute = map(int, time_str[:-1].split('시'))
    minute = minute / 60  # 분을 시간 단위로 변환
    if hour == 00:
      hour = 24.0
    return hour + minute

final_df['time_float'] = final_df['time'].apply(convert_time_to_float)

# 2. 정규화 (0~1)
min_time = 5.5  # 시작 시간 (5시 30분)
max_time = 24.5  # 종료 시간 (24시 30분)
final_df['time_normalized'] = (final_df['time_float'] - min_time) / (max_time - min_time)
# 데이터 변환 및 필터링
final_df['day_type'] = final_df['day_type'].replace({'평일': '평일', '토요일': '공휴일', '일요일': '공휴일'})
final_df['direction'] = final_df['direction'].replace({'내선': '상선', '외선':'하선'})
final_df['line'] = final_df['line'].replace({'13': '2', '14': '2', '15': '5'})  # 라인 수정
final_df = final_df[~final_df['line'].isin(['성수지선', '신정지선'])]  # 특정 라인 제거
final_df['line'] = final_df['line'].replace({f'{i}호선': str(i) for i in range(1, 9)})

final_df['congestion'] = final_df['congestion'].fillna(0)

# 기존 station_name과 station_id가 있는 DataFrame을 기준으로 매핑 생성
station_mapping = final_df.dropna(subset=['station_name']).set_index('station_id')['station_name'].to_dict()

# station_id를 기준으로 NaN 값을 station_name으로 채우기
final_df['station_name'] = final_df['station_name'].fillna(final_df['station_id'].map(station_mapping))
# 특정 ID 매핑
station_name_mapping = {'405': '전접', '406': '오남', '408': '별내별가람'}
# 데이터 타입 지정

final_df = final_df[~final_df['station_id'].isin(['2828', '9001', '9002', '9003', '9005', '9006'])]
final_df['congestion'] = final_df['congestion'].astype('float32')
final_df['station_id'] = final_df['station_id'].astype('int32')
final_df['year'] = final_df['year'].astype('int32')
final_df['line'] = final_df['line'].astype('int32')
final_df['direction'] = final_df['direction'].map({'상선': True, '하선': False})
final_df['day_type'] = final_df['day_type'].map({'평일': True, '공휴일': False})
final_df['direction'] = final_df['direction'].astype('boolean')
final_df['day_type'] = final_df['day_type'].astype('boolean')

# 1호선부터 8호선까지 반복하여 데이터 변환
station_data = {}
for line in range(1, 9):
    df_line = final_df.loc[final_df['line'] == line]
    # 'station_data'에 저장
    station_data[f'{line}'] = df_line
    # 'station_data'에서 필요한 데이터를 CSV로 저장
    station_data[f'{line}'].to_csv(f'line_{line}.csv', index=False)
