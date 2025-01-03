import sys
import os
import requests
import streamlit as st

# 현재 파일의 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handler import get_filter_keyword

# Streamlit 애플리케이션
st.title("Excel 파일 필터링")

# 사용자 입력
user_message = st.text_input("필터링 요청을 입력하세요:")

 # 파일 업로드
uploaded_file = st.file_uploader("Excel 파일을 업로드하세요", type=["xlsx"])

if user_message:
    # ChatGPT를 통해 필터링 키워드 추출
    keyword = get_filter_keyword(user_message)
    st.write(f"추출된 키워드: {keyword}")

    if uploaded_file is not None:
        # FastAPI 서버와 통신
        response = requests.post(
            "http://127.0.0.1:8097/filter",
            files={"file": uploaded_file},
            data={"keyword": keyword}
        )

        # 결과 출력
        if response.status_code == 200:
            filtered_data = response.json()
            st.write("필터링된 데이터:", filtered_data)
        else:
            st.write("서버 오류:", response.text)