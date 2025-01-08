from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import execute_query  # utils.py에서 함수 임포트

app = FastAPI()

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

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8097)