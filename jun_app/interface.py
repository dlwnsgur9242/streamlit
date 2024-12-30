import streamlit as st
import requests
import pandas as pd

st.title("📊 Excel 데이터 필터링")
st.write("날짜 범위를 선택하세요:")

start_date = st.date_input("시작 날짜")
end_date = st.date_input("종료 날짜")

if st.button("데이터 가져오기"):
    # Flask API 호출
    response = requests.post(
        "http://127.0.0.1:5000/filter-data",
        json={"start_date": str(start_date), "end_date": str(end_date)}
    )

    if response.status_code == 200:
        filtered_data = pd.DataFrame(response.json())
        st.write("### 필터링된 데이터:")
        st.dataframe(filtered_data)
    else:
        st.error(f"오류 발생: {response.json().get('error')}")

