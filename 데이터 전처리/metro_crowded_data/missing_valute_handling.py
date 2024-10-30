# 역번호로 역명 찾기 함수
def get_station_name(station_number):
    result = final_df_2.loc[final_df_2['역번호'] == station_number, '역명']
    if not result.empty:
        return result.values[0]  # 역명 반환
    else:
        return "해당 역번호에 대한 역명이 없습니다."
    
print(get_station_name("2555"))
    
    # 역명으로 역번호 찾기 함수
def get_station_number(station_name):
    result = final_df_2.loc[final_df_2['역명'] == station_name, '역번호']
    if not result.empty:
        return result.values[0]  # 역번호 반환
    else:
        return "해당 역명에 대한 역번호가 없습니다."
print(get_station_number("서울역"))

#역이름이 NaN인 역번호 출력
#9000번 역번호는 어떤번호인지 알수 없음
#2828 8호선 828 존재하지 않음 827번이 종착역인 모란역
#405 406 408 은 4호선 진접역 오남역 별내별가람역
result = pd.unique(final_df_2[final_df_2['역명'].isnull()]['역번호'])
print(result)

final_df_2.loc[final_df_2['역번호'] == '405', '역명'] = '전접'
final_df_2.loc[final_df_2['역번호'] == '406', '역명'] = '오남'
final_df_2.loc[final_df_2['역번호'] == '408', '역명'] = '별내별가람'
final_df_2 = final_df_2.drop(final_df_2[final_df_2['역번호'].isin('9001','9002','9003','9005','9006')])