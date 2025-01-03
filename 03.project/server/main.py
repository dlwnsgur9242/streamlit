from fastapi import FastAPI, UploadFile, Form
from server.utils import filter_excel_file

app = FastAPI()

@app.post("/filter")
async def filter_excel(file: UploadFile, keyword: str = Form(...)):
    """
    Excel 파일을 업로드하고 특정 키워드로 필터링.
    """
    filtered_data = await filter_excel_file(file, keyword)
    return {"filtered_data": filtered_data}

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)