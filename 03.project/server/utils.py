import pyodbc
import pandas as pd

def get_db_connection():
    """
    MS SQL 데이터베이스에 연결합니다.
    """
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=127.0.0.1,35791;'
        'DATABASE=_dy_solar_5.1;'
        'UID=sa;'
        'PWD=Ydsolemon#@31;'
        'TrustServerCertificate=yes;'
    )
    return conn

def execute_query(query):
    """
    주어진 SQL 쿼리를 실행하고 결과를 반환합니다.
    """
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_db_schema():
    """
    데이터베이스의 테이블과 컬럼 정보를 가져옵니다.
    """
    conn = get_db_connection()
    query = """
    SELECT TABLE_NAME, COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    ORDER BY TABLE_NAME, ORDINAL_POSITION
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df