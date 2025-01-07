import pandas as pd
from io import BytesIO

async def process_excel(file, keyword: str):
    """
    업로드된 Excel 파일에서 특정 키워드로 데이터를 필터링.
    
    Args:
        file (UploadFile): 업로드된 파일.
        keyword (str): 필터링할 키워드 (e.g., '과전압').

    Returns:
        List[Dict]: 월별 필터링된 데이터.
    """
    try:
        # 비동기로 파일 읽기
        contents = await file.read()
        # 판다스로 Excel 파일 읽기
        df = pd.read_excel(BytesIO(contents))

        # 첫 번째 행을 컬럼으로 설정하고, 불필요한 첫 두 행 제거
        df.columns = df.iloc[1]
        df = df[2:].reset_index(drop=True)
        df.columns = ['사이트명', '해당장비', '발생일시', '해제일시', '알람내용', '확인일시', '확인계정']

        # 발생일시를 datetime 형식으로 변환
        df['발생일시'] = pd.to_datetime(df['발생일시'], errors='coerce')

        # 키워드로 필터링
        filtered_data = df[df['알람내용'].str.contains(keyword, na=False)]

        # 월별 그룹화 및 필요한 컬럼만 반환
        filtered_monthly = filtered_data.groupby(df['발생일시'].dt.month).apply(
            lambda x: x[['사이트명', '해당장비', '발생일시', '알람내용']]
        ).reset_index(drop=True)

        return filtered_monthly.to_dict(orient="records")

    except Exception as e:
        raise ValueError(f"Error processing file: {e}")
