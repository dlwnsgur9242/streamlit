import requests
from client.handler import get_filter_keyword

# 사용자 입력
user_message = "2024-12.xlsx 파일에서 '전압부족'만 필터링해줘."

# ChatGPT를 통해 필터링 키워드 추출
keyword = get_filter_keyword(user_message)

# FastAPI 서버와 통신
file_path = "2024-12.xlsx"
with open(file_path, "rb") as file:
    response = requests.post(
        "http://127.0.0.1:8000/filter",
        files={"file": file},
        data={"keyword": keyword}
    )

# 결과 출력
filtered_data = response.json()
print(filtered_data)
