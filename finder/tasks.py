import os
from django.shortcuts import redirect
import pandas as pd
from sqlalchemy import create_engine
from celery import shared_task
import re


# def change_symbol():
#     pattern = r'\d\w[xXхХ]\d|\w\d[xXхХ]\d|\d[xXхХ]\d'
#     file_url = '/home/banywick/Документы/ОКБТСП разработка поисковика/меняем сиввал/13.07.23.xlsx'
    
#     # Чтение данных из файла Excel
#     df = pd.read_excel(file_url,usecols=[11, 12, 13, 14, 15, 16, 17, 18] , skiprows=10)
    
#     # Замена символов
#     for col in df.columns:
#         df[col][15] = df[col].apply(lambda x: re.sub(pattern, '*', str(x)))
    
#     # Сохранение изменений
#     df.to_excel(file_url, index=False)
#     print('готово')

# Вызов функции
# change_symbol()






@shared_task
def data_save_db(file_url):
    try:
        collums_document = []
        collums_template = [
            "Комментарий",
            "Код",
            "Артикул",
            "Партия.Код",
            "Номенклатура",
            "Базовая единица измерения",
            "Склад",
            "Конечный остаток (Количество)",
        ]
        df = pd.read_excel(file_url, usecols=[11, 12, 13, 14, 15, 16, 17, 18])
        order_colums = df.iloc[7].fillna("Конечный остаток (Количество)")
        for col in order_colums:
            collums_document.append(col)
        if collums_document == collums_template:
            df = df.iloc[10:]  # Начинаем с 10 строки
            engine = create_engine("postgresql://sklad:sklad@127.0.0.1:5432/sklad_db")
            df.columns = [
                "comment",
                "code",
                "article",
                "party",
                "title",
                "base_unit",
                "project",
                "quantity",
            ]
            df["quantity"] = df["quantity"].astype(float).round(2)
            df.to_sql("finder_remains", engine, if_exists="replace", index_label="id")
            os.remove(file_url)
        else:
            os.remove(file_url)
            raise "Не соответсвует порядок столбцов в документе"

    except Exception as e:
        os.remove(file_url)
        raise "Файл который вы загружаете не соответсвует структуре"
