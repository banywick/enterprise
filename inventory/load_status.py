import pandas as pd
from sqlalchemy import create_engine

# # Параметры подключения к PostgreSQL
db_params = {
    'dbname': 'sklad_db',
    'user': 'sklad',
    'password': 'sklad',
    'host': '127.0.0.1',
    'port': '5432'
}

# Чтение данных из CSV
csv_file = r'G:\\Django projects\\enterprise\\инвент статусы.csv'
df = pd.read_csv(csv_file, encoding='utf-8', delimiter=';')

# Подключение к PostgreSQL
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

df.to_sql('inventory_remainsinventory', engine, if_exists='append', index_label="id")


