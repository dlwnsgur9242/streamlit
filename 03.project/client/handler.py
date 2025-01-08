import openai
import os

# OpenAI API 키 설정
openai.api_key = os.environ.get("SEARCH_API_KEY")

def get_sql_query(user_message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 데이터베이스 쿼리를 생성하는 AI야."},
            {"role": "user", "content": user_message}
        ]
    )
    query = response.choices[0].message.content
    return query