from sqlalchemy import create_engine, MetaData
import urllib
import json

# pyodbc 연결 문자열
connection_string = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=127.0.0.1,35791;'
    'DATABASE=_dy_solar_5.1;'
    'UID=sa;'
    'PWD=Ydsolemon#@31;'
    'TrustServerCertificate=yes;'
)

# pyodbc 연결 문자열을 URL 인코딩
params = urllib.parse.quote_plus(connection_string)

# SQLAlchemy 엔진 생성
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_url)

# 메타데이터 가져오기
metadata = MetaData()
metadata.reflect(bind=engine)

# 메타데이터를 JSON으로 변환
database_metadata = {}
for table_name, table in metadata.tables.items():
    table_info = {
        "columns": [],
        "primary_key": [key.name for key in table.primary_key.columns] if table.primary_key else [],
    }
    for column in table.columns:
        column_info = {
            "name": column.name,
            "type": str(column.type),
            "nullable": column.nullable,
            "default": str(column.default) if column.default is not None else None,
        }
        table_info["columns"].append(column_info)
    database_metadata[table_name] = table_info

# JSON 저장
with open("mssql_metadata.json", "w", encoding="utf-8") as json_file:
    json.dump(database_metadata, json_file, indent=4, ensure_ascii=False)

print("MSSQL 메타데이터가 mssql_metadata.json에 저장되었습니다.")