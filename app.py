from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# 엑셀 데이터 로드
data = pd.read_excel("data/2024.xlsx", engine='openpyxl', header=None)  # 헤더를 None으로 설정해 모든 데이터를 읽음
print("Raw Data Preview:")
print(data.head())  # 데이터의 첫 몇 줄 출력

# 데이터 헤더 설정
data.columns = ['사이트명', '해당장비', '발생일시', '해제일시', '알람내용', '확인일시', '확인계정']  # 열 이름 수동 설정

# 발생일시 열을 datetime으로 변환
data['발생일시'] = pd.to_datetime(data['발생일시'], errors='coerce')  # 잘못된 날짜는 NaT로 처리
data = data.dropna(subset=['발생일시'])  # 날짜가 없는 행은 제거

print("Processed Data Preview:")
print(data.head())  # 변환된 데이터 미리보기

@app.route('/filter-data', methods=['POST'])
def filter_data():
    try:
        # 클라이언트에서 날짜 범위 받기
        request_data = request.json
        start_date = request_data.get("start_date")
        end_date = request_data.get("end_date")

        # 입력값 검증
        if not start_date or not end_date:
            return jsonify({"error": "Both 'start_date' and 'end_date' are required"}), 400

        # 날짜 변환
        start_date = pd.to_datetime(start_date, errors='coerce')
        end_date = pd.to_datetime(end_date, errors='coerce')

        if pd.isnull(start_date) or pd.isnull(end_date):
            return jsonify({"error": "Invalid date format for 'start_date' or 'end_date'"}), 400

        # 데이터 필터링
        filtered_data = data[(data['발생일시'] >= start_date) & (data['발생일시'] <= end_date)]

        # 결과가 없는 경우 처리
        if filtered_data.empty:
            return jsonify({"message": "No data found for the given date range"}), 200

        return jsonify(filtered_data.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
2022025250
if __name__ == "__main__":
    app.run(debug=True)
