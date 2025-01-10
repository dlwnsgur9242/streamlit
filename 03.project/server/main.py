from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import execute_query, get_db_schema  # utils.py에서 함수 임포트
import openai
import os

app = FastAPI()

# OpenAI API 키 설정
openai.api_key = os.environ.get("SEARCH_API_KEY")

class QueryRequest(BaseModel):
    user_message: str
    query: str

@app.post("/query")
async def run_query(request: QueryRequest):
    try:
        df = execute_query(request.query)
        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 처리 중 오류 발생: {e}")

@app.post("/generate-query")
async def generate_query(request: QueryRequest):
    try:
        # 데이터베이스 스키마 정보 가져오기
        schema_df = get_db_schema()
        schema_info = schema_df.to_csv(index=False)
        
        # OpenAI API 요청
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"너는 데이터베이스 쿼리를 생성하는 AI야. 다음은 데이터베이스의 스키마 정보야:\n{schema_info}"},
                {"role": "user", "content": request.user_message}
            ]
        )
        query = response.choices[0].message.content

         # 설명 텍스트 제거
        sql_query = extract_sql_query(query)
        
        # 실제 SQL 쿼리 실행
        df = execute_query(sql_query)

        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 처리 중 오류 발생: {e}")

def extract_sql_query(response_text):
    """
    OpenAI 응답에서 실제 SQL 쿼리만 추출합니다.
    """
    query_lines = response_text.split('\n')
    sql_query = []
    for line in query_lines:
        if line.strip().lower().startswith('select') or line.strip().lower().startswith('from') or line.strip().lower().startswith('where'):
            sql_query.append(line)
    return '\n'.join(sql_query)

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8097)