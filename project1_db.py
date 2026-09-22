import pandas as pd
import pymysql
from sqlalchemy import create_engine

# 1. 새롭게 정리된 CSV 파일 로드
df_type = pd.read_csv('car_registration_by_type_2.csv')
df_year = pd.read_csv('car_registration_by_year_2.csv')

# 2. MySQL 접속 정보 설정
DB_USER = 'root'
DB_PASSWORD = '1234' 
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'korea_car'

# 3. 데이터베이스 생성 (문자셋 utf8mb4)
conn = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT,
    charset='utf8mb4'
)
try:
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    conn.commit()
finally:
    conn.close()

# 4. 데이터 적재
engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

df_type.to_sql(name='car_by_type_v2', con=engine, if_exists='replace', index=False)
df_year.to_sql(name='car_by_year_v2', con=engine, if_exists='replace', index=False)

print("성공적으로 계층형 데이터가 적재되었습니다.")