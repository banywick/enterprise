import os
from django.shortcuts import redirect
import pandas as pd
from sqlalchemy import create_engine
from celery import shared_task


@shared_task
def data_save_db(file_url):
    try:
        df = pd.read_excel(file_url, usecols=[11, 12, 13, 14, 15, 16, 17, 18])
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
    except:
        os.remove(file_url)
        raise


# data_save_db()
