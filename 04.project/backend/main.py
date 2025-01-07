import sys
import os
from fastapi import FastAPI, UploadFile, Form, HTTPException
from excel_utils import process_excel
import openai

# 현재 파일 경로를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# OpenAI API 키 설정
openai.api_key = "YOUR_API_KEY"

@app.post("/analyze")
async def analyze_file(file: UploadFile, user_request: str = Form(...)):
    """
    엑셀 파일에서 사용자 요청에 따라 데이터를 필터링하고 분석 결과 반환.
    """
    try:
        # 데이터 필터링
        filtered_data = await process_excel(file, user_request)

        if not filtered_data:
            return {"message": "필터링된 데이터가 없습니다.", "filtered_data": []}

        # OpenAI API 요청
        text_data = "\n".join([str(row) for row in filtered_data])
        prompt = f"""
        요청: "{user_request}"
        데이터:
        {text_data}

        위 데이터를 기반으로 추가 분석을 요약해줘.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for data analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        result = response['choices'][0]['message']['content']

        return {"filtered_data": filtered_data, "analysis_result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 처리 중 오류 발생: {e}")
