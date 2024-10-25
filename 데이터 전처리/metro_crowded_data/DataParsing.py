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
    
    # 컬럼 리스트
    column_list = ['년도', '호선', '상하구분', '역명', '역번호', '요일구분', '5시30분', '6시00분', '6시30분', '7시00분', '7시30분', '8시00분',
                   '8시30분', '9시00분', '9시30분', '10시00분', '10시30분', '11시00분', '11시30분', '12시00분', '12시30분', '13시00분',
                   '13시30분', '14시00분', '14시30분', '15시00분', '15시30분', '16시00분', '16시30분', '17시00분', '17시30분', '18시00분',
                   '18시30분', '19시00분', '19시30분', '20시00분', '20시30분', '21시00분', '21시30분', '22시00분', '22시30분', '23시00분',
                   '23시30분', '24시00분', '24시30분']
    
    # DataFrame 생성
    df = pd.DataFrame(rows, columns=column_list)
    
    # 년도 컬럼 추가
    df['년도'] = year
    
    return df

# 각 년도의 데이터를 데이터프레임으로 변환하고 병합
final_df = pd.DataFrame()  # 최종 데이터프레임을 위한 빈 데이터프레임

years = [2020, 2021, 2022, 2023, 2024_3]  # API에 해당하는 년도 목록
for uddi, year in zip(api, years):
    df = parsing(merged_data[uddi], year)  # 각 년도의 데이터를 파싱
    final_df = pd.concat([final_df, df], ignore_index=True)  # 데이터프레임 병합

# 데이터를 '시간'과 '혼잡도'로 변형
final_df_2 = pd.melt(final_df,
                      id_vars=['년도', '호선', '상하구분', '역명', '역번호', '요일구분']
                     ,var_name='시간',
                     value_name='혼잡도')

final_df_2['혼잡도'] = final_df_2['혼잡도'].fillna(0)

# 기존 역명과 역번호가 있는 DataFrame을 기준으로 매핑 생성
station_mapping = final_df_2.dropna(subset=['역명']).set_index('역번호')['역명'].to_dict()

# 역번호를 기준으로 NaN 값을 역명으로 채우기
final_df_2['역명'] = final_df_2['역명'].fillna(final_df_2['역번호'].map(station_mapping))


# 최종 데이터프레임 출력 (454740행 * 8열) -> 일관성 없는 2019년도 데이터 추가 삭제
print(final_df_2)
final_df_2.to_csv('output.csv', index=False)
#혼잡도 데이터타입 OBJECT형 형변환 필요할듯?
#final_df_2.shape