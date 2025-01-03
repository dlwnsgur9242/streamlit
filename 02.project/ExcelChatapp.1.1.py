import streamlit as st
import pandas as pd

# Streamlit 앱 제목
st.title("Excel 데이터 대화형 필터링")

# 파일 업로드
uploaded_file = st.file_uploader("Excel 파일을 업로드하세요", type=["xlsx"])
if uploaded_file is not None:
    # Excel 파일 읽기
    sheet_name = "2024-12"  # 시트 이름 변경 가능
    data = pd.read_excel(uploaded_file, sheet_name=sheet_name)

    # 데이터 헤더 정리
    data.columns = data.iloc[1]  # 헤더 설정
    data = data[2:]  # 데이터 시작 지점 조정

    # 알람내용 열 확인
    st.write("데이터 미리보기")
    st.dataframe(data.head())

    # 사용자 입력: 필터링 키워드
    keyword = st.text_input("필터링할 키워드를 입력하세요", "전압부족")
    
    if keyword:
        # 필터링
        filtered_data = data[data['알람내용'].str.contains(keyword, na=False)]
        st.write(f"'{keyword}' 키워드가 포함된 데이터:")
        st.dataframe(filtered_data)

        # 결과 다운로드
        st.download_button(
            label="필터링된 데이터 다운로드",
            data=filtered_data.to_csv(index=False).encode('utf-8'),
            file_name="filtered_data.csv",
            mime="text/csv"
        )
