import pandas as pd
import joblib
import datetime
from flask import Flask, request, jsonify

# 1호선부터 8호선 데이터 및 모델 로드
data = [pd.read_csv(f'dataprep/getcongestion/dataset/line_{i}.csv') for i in range(1, 9)]
model = [joblib.load(f'dataprep/getcongestion/trainpicle/xgb_reg_{i}.pkl') for i in range(1, 9)]

# 30분 단위로 반올림하는 함수
def adjust_to_nearest_30_minutes(time_str):
    time_obj = datetime.datetime.strptime(time_str, "%H시%M분")
    if time_obj.minute < 15:
        rounded_time = time_obj.replace(minute=0, second=0)
    elif time_obj.minute < 45:
        rounded_time = time_obj.replace(minute=30, second=0)
    else:
        rounded_time = (time_obj + datetime.timedelta(hours=1)).replace(minute=0, second=0)
    return rounded_time.strftime("%H시%M분")

def format_time(time_str):
    # "15시1분"과 같은 문자열을 "15시01분"으로 변환
    hour, minute = time_str.split("시")
    minute = minute.replace("분", "").zfill(2)  # zfill(2): 한 자리 수일 때 앞에 0을 붙임
    return f"{hour}시{minute}분"

# Flask 애플리케이션
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def get_data():
    input_data = request.json
    direction = input_data.get('direction')
    day_type = input_data.get('day_type')
    time = input_data.get('time')
    station_name = input_data.get('station_name')
    line = input_data.get('line')  # 1~8 사이의 정수값
    print("받은 데이터:", input_data)


    # 올바른 데이터와 모델 선택
    print("line : " , line)
    selected_data = data[line - 1]  # 인덱스는 0부터 시작
    selected_model = model[line - 1]

    # 중앙값 계산용 시간 반올림
    adjust_time = adjust_to_nearest_30_minutes(time)
    formatted_time = format_time(time)

    # 중앙값 계산용 데이터 필터링 (반올림된 시간 사용)
    filtered_data_m = selected_data[
        (selected_data['direction'] == direction) &
        (selected_data['day_type'] == day_type) &
        (selected_data['time'] == adjust_time) &
        (selected_data['station_name'] == station_name) &
        (selected_data['line'] == line)
    ]

    # 중앙값 계산
    median = float(filtered_data_m['congestion'].median()) if not filtered_data_m.empty else None

    # 모델 예측용 입력 데이터 준비
    model_input = pd.DataFrame({
        'time': [formatted_time],  
        'day_type': [day_type],
        'direction': [direction],
        'station_name': [station_name],
        'line': [line]
    })

    # 모델 예측
    predicted_congestion = float(selected_model.predict(model_input)[0])

    print(f"중앙값 혼잡도 (line {line}):", median)
    print(f"예측 혼잡도 (line {line}):", predicted_congestion)

    return jsonify({
        "line": line,
        "median_congestion": median,
        "predict_congestion": predicted_congestion
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


#python -m waitress --port=5000 dataprep.getcongestion.Predict_Flask:app

