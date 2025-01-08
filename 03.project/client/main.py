import streamlit as st
import requests
from handler import get_sql_query  # handler.py에서 함수 임포트

# Streamlit 애플리케이션
st.title("MS SQL 데이터베이스 필터링")

# 사용자 입력
user_message = st.text_input("필터링 요청을 입력하세요:")

if user_message:
    try:
        # OpenAI를 통해 SQL 쿼리 생성
        query = get_sql_query(user_message)
        st.write(f"생성된 SQL 쿼리: {query}")

        # FastAPI 서버에 요청
        response = requests.post(
            "http://127.0.0.1:8097/query",
            json={"user_message": user_message, "query": query}
        )

        # 응답 처리
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                st.success("데이터 가져오기 성공!")
                st.dataframe(data)
            else:
                st.warning("데이터가 없습니다.")
        else:
            st.error(f"서버 오류가 발생했습니다: {response.text}")

    except Exception as e:
        st.error(f"요청 중 오류가 발생했습니다: {e}")