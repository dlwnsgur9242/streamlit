import streamlit as st
import requests
import pandas as pd

# Streamlit 애플리케이션
st.title("Excel 파일 필터링")

# 사용자 입력
user_message = st.text_input("필터링 요청을 입력하세요:")

# 파일 업로드
uploaded_file = st.file_uploader("Excel 파일을 업로드하세요", type=["xlsx"])

if user_message and uploaded_file:
    keyword = user_message.strip()
    st.write(f"추출된 키워드: {keyword}")

    try:
        # FastAPI 서버에 요청
        response = requests.post(
            "http://127.0.0.1:8097/filter",
            files={"file": uploaded_file.getvalue()},
            data={"keyword": keyword},
        )

        # 응답 처리
        if response.status_code == 200:
            filtered_data = response.json().get("filtered_data", [])
            if filtered_data:
                st.success("필터링 성공!")
                # 데이터프레임으로 출력
                st.dataframe(pd.DataFrame(filtered_data))
            else:
                st.warning("필터링 결과가 없습니다.")
        else:
            st.error(f"서버 오류: {response.status_code}\n{response.text}")

    except Exception as e:
        st.error(f"요청 처리 중 오류 발생: {e}")
