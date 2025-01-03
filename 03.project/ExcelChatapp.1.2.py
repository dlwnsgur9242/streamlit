from fastapi import FastAPI, UploadFile, Form
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.post("/filter")
async def filter_excel(file: UploadFile, keyword: str = Form(...)):
    # Read Excel file
    content = await file.read()
    excel_data = pd.read_excel(BytesIO(content), sheet_name="2024-12")
    
    # Data header adjustment
    excel_data.columns = excel_data.iloc[1]
    excel_data = excel_data[2:]  # Skip metadata rows

    # Filtering
    filtered_data = excel_data[excel_data['알람내용'].str.contains(keyword, na=False)]

    # Return filtered data as JSONdir
    return {"filtered_data": filtered_data.to_dict(orient="records")}

import openai
import requests

# ChatGPT API Key 설정
openai.api_key = "your_openai_api_key"

# 사용자 입력
user_message = "2024-12.xlsx 파일에서 '전압부족'만 필터링해줘."

# ChatGPT에게 요청
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "너는 데이터 분석 보조 AI야."},
        {"role": "user", "content": user_message}
    ]
)

# 사용자의 요청에서 키워드 추출
keyword = response['choices'][0]['message']['content']

# FastAPI로 데이터 전송 및 처리
file_path = "2024-12.xlsx"  # 로컬에 저장된 파일 경로
with open(file_path, "rb") as file:
    response = requests.post(
        "http://127.0.0.1:8000/filter",
        files={"file": file},
        data={"keyword": keyword}
    )

# 결과 출력
filtered_data = response.json()
print(filtered_data)
