import pandas as pd
from io import BytesIO

async def filter_excel_file(file, keyword):
    """
    Excel 파일을 읽고 특정 키워드로 필터링.
    """
    content = await file.read()
    excel_data = pd.read_excel(BytesIO(content), sheet_name="2024-12")
    
    # 헤더 조정
    excel_data.columns = excel_data.iloc[1]
    excel_data = excel_data[2:]  # 데이터 시작 지점
    
    # 키워드 필터링
    filtered_data = excel_data[excel_data['알람내용'].str.contains(keyword, na=False)]
    return filtered_data.to_dict(orient="records")
