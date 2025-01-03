import openai

openai.api_key = "SEARCH_API_KEY"

def get_filter_keyword(user_message):
    """
    ChatGPT API를 통해 사용자의 의도를 분석하여 키워드를 추출.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 데이터 분석 보조 AI야."},
            {"role": "user", "content": user_message}
        ]
    )
    keyword = response['choices'][0]['message']['content']
    return keyword