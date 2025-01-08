import pyodbc
import pandas as pd

def get_db_connection():
    """
    MS SQL 데이터베이스에 연결합니다.
    """
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=127.0.0.1,35791;'
            'DATABASE=_dy_solar_5.1;'
            'UID=sa;'
            'PWD=Ydsolemon#@31;'
            'TrustServerCertificate=yes;'
        )
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        raise

def execute_query(query):
    """
    주어진 SQL 쿼리를 실행하고 결과를 반환합니다.
    """
    conn = None
    try:
        conn = get_db_connection()
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("Query execution failed:", e)
        raise
    finally:
        if conn:
            conn.close()