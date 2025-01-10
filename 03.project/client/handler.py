import openai
import os
import pandas as pd
from utils import get_db_schema  # utils.py에서 함수 임포트

# OpenAI API 키 설정
openai.api_key = os.environ.get("SEARCH_API_KEY")

def get_sql_query(user_message):
    # 데이터베이스 스키마 정보 가져오기
    schema_df = get_db_schema()
    schema_info = schema_df.to_csv(index=False)

    # OpenAI API 요청
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"너는 데이터베이스 쿼리를 생성하는 AI야. 다음은 데이터베이스의 스키마 정보야:\n{schema_info}"},
            {"role": "user", "content": user_message}
        ]
    )
    query = response.choices[0].message.content
    return query