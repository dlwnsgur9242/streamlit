import streamlit as st
import pandas as pd
from handler import call_fastapi

st.title("엑셀 데이터 필터링 및 분석")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

# 사용자 요청 입력
user_request = st.text_input("요청 사항을 입력하세요:", "24년 이전 통신 이상 알람 내용만 출력해줘")

if uploaded_file and user_request:
    # FastAPI 서버 호출
    result = call_fastapi(uploaded_file, user_request)

    # 결과 처리
    if "error" in result:
        st.error(result["error"])
    else:
        filtered_data = result.get("filtered_data", [])
        analysis_result = result.get("analysis_result", "분석 결과가 없습니다.")

        if filtered_data:
            st.success("필터링 성공! 결과를 확인하세요:")
            st.dataframe(pd.DataFrame(filtered_data))
            st.write("추가 분석 결과:")
            st.text(analysis_result)
        else:
            st.warning("필터링된 데이터가 없습니다.")
