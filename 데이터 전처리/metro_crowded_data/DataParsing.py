import xml.etree.ElementTree as ET
import pandas as pd
import requests

page = 1
perPage = 1667  # 모든 데이터의 최대 페이지 수
merged_data = {}

# API 목록
api = [
    'uddi:99771417-a036-46f1-8ad5-8edf4591c2ee',  # 2020
    'uddi:b3803d43-ffe3-4d17-9024-fd6cfa37c284',  # 2021
    'uddi:75461a18-17a3-42fe-9322-a51148003b69',  # 2022
    'uddi:e477f1d9-2c3a-4dc8-b147-a55584583fa2',  # 2023
    'uddi:c87b6af0-0ef7-4182-b172-fd2680a79d6f',  # 2024/03
    'uddi:9aff0ee6-26e7-42c4-af0c-84bf31680ca9'  # 2024/06
    #'uddi:da7cd08f-94f0-4dba-b33d-d02dcb35b57b',  # 2024/09 데이터오류
]

# 각 년도의 데이터를 딕셔너리에 저장
for uddi in api:
    url = 'https://api.odcloud.kr/api/15071311/v1/' + uddi
    params = {
        'serviceKey': '9bi5h25Oa1d6yB2qd+7vNhE7qWLhgJvDSr4dTv6vhlZ3rvlpNTbs6NZv/B+R/CvFLssD7Flh+jSDAYydOoaRfQ==',
        'returnType': 'XML',
        'page': page,
        'perPage': perPage
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # API 요청 에러 처리
        data = {uddi: response.text}
        merged_data.update(data)
    except requests.exceptions.RequestException as e:
        print(f"API 요청 실패: {uddi}, 에러: {e}")

# XML 데이터를 순회하며 데이터프레임에 추가하는 함수
def parsing(data, year):
    xml_obj = ET.fromstring(data)
    rows = []

    for row in xml_obj.findall('.//item'):
        row_data = {}
        for col in row.findall('.//col'):
            if col.attrib['name'] == "조사일자":
                row_data['요일구분'] = col.text  # 조사일자 -> 요일구분
            elif col.attrib['name'] == "구분":
                row_data['상하구분'] = col.text  # 구분 -> 상하구분
            else:
                row_data[col.attrib['name']] = col.text  # 그 외의 경우 일반적으로 처리
        if row_data:
            rows.append(row_data)

    # 컬럼 매핑 딕셔너리
    column_list = ['년도', '호선', '상하구분', '역명', '역번호', '요일구분', '5시30분', '6시00분', '6시30분', '7시00분', '7시30분', '8시00분',
                   '8시30분', '9시00분', '9시30분', '10시00분', '10시30분', '11시00분', '11시30분', '12시00분', '12시30분', '13시00분',
                   '13시30분', '14시00분', '14시30분', '15시00분', '15시30분', '16시00분', '16시30분', '17시00분', '17시30분', '18시00분',
                   '18시30분', '19시00분', '19시30분', '20시00분', '20시30분', '21시00분', '21시30분', '22시00분', '22시30분', '23시00분',
                   '23시30분', '24시00분', '24시30분']
    column_mapping = {
        '년도': 'year', '호선': 'line', '상하구분': 'direction', '역명': 'station_name', '역번호': 'station_id', '요일구분': 'day_type',
        '5시30분': '5:30', '6시00분': '6:00', '6시30분': '6:30', '7시00분': '7:00', '7시30분': '7:30', '8시00분': '8:00',
        '8시30분': '8:30', '9시00분': '9:00', '9시30분': '9:30', '10시00분': '10:00', '10시30분': '10:30', '11시00분': '11:00',
        '11시30분': '11:30', '12시00분': '12:00', '12시30분': '12:30', '13시00분': '13:00', '13시30분': '13:30', '14시00분': '14:00',
        '14시30분': '14:30', '15시00분': '15:00', '15시30분': '15:30', '16시00분': '16:00', '16시30분': '16:30', '17시00분': '17:00',
        '17시30분': '17:30', '18시00분': '18:00', '18시30분': '18:30', '19시00분': '19:00', '19시30분': '19:30', '20시00분': '20:00',
        '20시30분': '20:30', '21시00분': '21:00', '21시30분': '21:30', '22시00분': '22:00', '22시30분': '22:30', '23시00분': '23:00',
        '23시30분': '23:30', '24시00분': '24:00', '24시30분': '24:30',
    }

    # DataFrame 생성 및 컬럼 이름 변경
    df = pd.DataFrame(rows, columns=column_list)
                      
    df = df.rename(columns=column_mapping)

    # 'year' 컬럼 추가
    df['year'] = year
    return df

# 각 년도의 데이터를 데이터프레임으로 변환하고 병합
final_df = pd.DataFrame()  # 최종 데이터프레임을 위한 빈 데이터프레임

years = [2020, 2021, 2022, 2023, 202403, 202406]  # API에 해당하는 년도 목록
for uddi, year in zip(api, years):
    df = parsing(merged_data[uddi], year)  # 각 년도의 데이터를 파싱
    final_df = pd.concat([final_df, df], ignore_index=True)  # 데이터프레임 병합

# 데이터를 '시간'과 '혼잡도'로 변형
final_df_2 = pd.melt(final_df,
                      id_vars=['year', 'line', 'direction', 'station_name', 'station_id', 'day_type'],
                      var_name='time',
                      value_name='congestion')

final_df_2['congestion'] = final_df_2['congestion'].fillna(0)

# 기존 station_name과 station_id가 있는 DataFrame을 기준으로 매핑 생성
station_mapping = final_df_2.dropna(subset=['station_name']).set_index('station_id')['station_name'].to_dict()

# station_id를 기준으로 NaN 값을 station_name으로 채우기
final_df_2['station_name'] = final_df_2['station_name'].fillna(final_df_2['station_id'].map(station_mapping))

<<<<<<< HEAD
final_df_2.loc[final_df_2['station_id'] == '405', 'station_name'] = '전접'
final_df_2.loc[final_df_2['station_id'] == '406', 'station_name'] = '오남'
final_df_2.loc[final_df_2['station_id'] == '408', 'station_name'] = '별내별가람'
final_df_2 = final_df_2.drop(final_df_2[final_df_2['station_id'].isin(['2828','9001','9002','9003','9005','9006'])].index)
print(final_df_2)
final_df_2.to_csv('output_check.csv', index=False)
#9000번 역번호는 어떤번호인지 알수 없음
#2828 8호선 828 존재하지 않음 827번이 종착역인 모란역
#405 406 408 은 4호선 진접역 오남역 별내별가람역

final_df_2.loc[final_df_2['역번호'] == '405', '역명'] = '전접'
final_df_2.loc[final_df_2['역번호'] == '406', '역명'] = '오남'
final_df_2.loc[final_df_2['역번호'] == '408', '역명'] = '별내별가람'
final_df_2 = final_df_2.drop(final_df_2[final_df_2['역번호'].isin(['2828','9001','9002','9003','9005','9006'])].index)

# 최종 데이터프레임 출력 (454740행 * 8열) -> 일관성 없는 2019년도 데이터 추가 삭제
print(final_df_2)
final_df_2.to_csv('output.csv', index=False)
