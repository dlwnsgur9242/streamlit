import requests

def call_fastapi(file, user_request, api_url="http://127.0.0.1:8098/analyze"):
    """
    FastAPI 서버에 요청을 보내고 결과를 반환.

    Args:
        file: 업로드된 파일 객체 (Streamlit의 UploadedFile)
        user_request: 사용자 요청 텍스트
        api_url: FastAPI 엔드포인트 URL

    Returns:
        dict: FastAPI 서버 응답
    """
    try:
        response = requests.post(
            api_url,
            files={"file": file.getvalue()},
            data={"user_request": user_request}
        )
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"FastAPI 서버와의 통신 오류: {e}"}
