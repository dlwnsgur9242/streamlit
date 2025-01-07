import pandas as pd
from io import BytesIO

async def process_excel(file, keyword: str):
    """
    업로드된 Excel 파일에서 특정 키워드로 데이터를 필터링.

    Args:
        file (UploadFile): 업로드된 파일.
        keyword (str): 필터링할 키워드.

    Returns:
        List[Dict]: 필터링된 데이터.
    """
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # 첫 번째 행을 컬럼으로 설정하고, 필요 없는 첫 두 행 제거
        df.columns = df.iloc[1]
        df = df[2:].reset_index(drop=True)

        # 발생일시를 datetime 형식으로 변환
        if '발생일시' in df.columns:
            df['발생일시'] = pd.to_datetime(df['발생일시'], errors='coerce')

        # 키워드로 필터링
        if '알람내용' in df.columns:
            filtered_data = df[df['알람내용'].str.contains(keyword, na=False)]
            return filtered_data.to_dict(orient="records")
        else:
            raise ValueError("알람내용 컬럼이 없습니다.")
    except Exception as e:
        raise ValueError(f"파일 처리 중 오류 발생: {e}")
