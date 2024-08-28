from itertools import product
import os
from django.http import FileResponse
from django.shortcuts import redirect
import pandas as pd
import pytz
from sqlalchemy import create_engine
from celery import shared_task
import re
from datetime import datetime

from finder.models import Data_Table
from inventory.models import OrderInventory


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
    


def backup_sahr_table():
    timezone = pytz.timezone('Europe/Minsk')
    current_date = datetime.now(timezone).strftime('%d.%m.%Y %H:%M:%S')
    queryset = Data_Table.objects.all()  # Получите все записи из модели
    df = pd.DataFrame(list(queryset.values()))  # Преобразуйте в DataFrame
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    folder_path = 'finder/document/backup_sahr'  # Замените на свой путь
    # Сохраняем в файл Excel с читаемой датой в названии
    file_path = os.path.join(folder_path, f'CAXP_{current_date}.xlsx')
    n = f'CAXP_{current_date}.xlsx'
    df.to_excel(file_path, index=False)
    filename = f'CAXP_{current_date}.xlsx'
    return [file_path, filename]  


def backup_inventory_table():
    timezone = pytz.timezone('Europe/Minsk')
    current_date = datetime.now(timezone).strftime('%d.%m.%Y %H:%M:%S')
    
    # Получите данные из базы
    queryset = OrderInventory.objects.select_related('product').values(
        'product__article', 
        'product__title', 
        'product__base_unit', 
        'product__status', 
        'quantity_ord', 
        'created_at', 
        'address', 
        'comment'
    ).filter(product__status__iexact='Сошлось')
    
    # Преобразование в DataFrame
    df = pd.DataFrame(list(queryset))

    # Переименовываем столбцы
    df.rename(columns={
        'product__article': 'Артикул',
        'product__title': 'Наименование',
        'product__base_unit': 'Единица',
        'quantity_ord': 'Посчитанно',
        'address': 'Адрес',
        'comment': 'Комментарий',
        'created_at': 'Дата создания',
        'product__status': 'Статус',
    }, inplace=True)

    # Задайте порядок столбцов
    columns_order = ['Артикул', 'Наименование', 'Единица', 'Посчитанно', 'Адрес', 'Комментарий', 'Дата создания', 'Статус']  # Замените на нужный порядок
    df = df[columns_order]  # Измените порядок столбцов
    
    # Задайте путь к папке и создайте его, если он не существует
    folder_path = os.path.join('finder', 'document', 'report_inventory')  # путь к папке
    os.makedirs(folder_path, exist_ok=True)
    
    # Сохраняем в файл Excel с читаемой датой в названии
    file_path = os.path.join(folder_path, f'report_inv.xlsx')
    df.to_excel(file_path, index=True)
    
    return [file_path, f'report_inv.xlsx']




