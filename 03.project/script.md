# 문제 정의
    1. MSSQL 데이터베이스를 대상으로 자연어로 질의했을 때, 데이터의 의미를 파악하고 그에 맞는 결과를 출력하는 기능을 구현.
    
    2. 데이터베이스의 속성이 지니는 의미를 명확히 이해하기 어렵기 때문에, 이 정보를 OpenAI API와 연계하여 자연어 질의를 처리.
<br>

# 구성
    
    Client = Streamlit
    Server = FastAPI
    DB = MSSQL
    API = opneai api (gpt model)
<br>

# 설계
   
    1. 기능 개요
        
        사용자는 Streamlit을 통해 자연어로 MSSQL 데이터베이스에 질의.

        질의는 FastAPI 서버로 전달되고, FastAPI는 이를 OpenAI API와 MSSQL로 연결하여 처리.

        OpenAI API는 질의를 분석하고 MSSQL 데이터에 적합한 SQL 쿼리를 생성.

        FastAPI는 생성된 SQL 쿼리를 실행하고, 결과를 Streamlit으로 반환.
    

    2. 프로세스 흐름

        Streamlit: 사용자 입력 → FastAPI에 요청 전송.

        FastAPI:    MSSQL의 메타데이터(JSON 형식)를 OpenAI API에 전달하여 데이터의 구조와 의미를 설명.
                    OpenAI API를 통해 자연어 질의를 SQL 쿼리로 변환.
                    변환된 SQL 쿼리를 MSSQL에 실행하여 결과 데이터 추출.

        MSSQL: 쿼리 실행 → 결과 반환.

        FastAPI: 결과 데이터를 처리하여 Streamlit으로 반환.

        Streamlit: 결과 데이터를 사용자에게 시각적으로 출력.


    3. 핵심 포인트
        
        메타데이터 관리: MSSQL의 테이블 및 컬럼의 의미를 JSON으로 정리하여 OpenAI에 전달.
        
        OpenAI API 최적화: 비용을 절감하기 위해 메타데이터 요약본과 질의만 전달.
        
        결과 데이터 처리: FastAPI에서 결과를 가공하여 Streamlit에 적합한 형태로 반환.
        
        보안: 데이터베이스 인증 정보와 OpenAI API 키는 환경 변수로 관리.
<br>