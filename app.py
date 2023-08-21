import streamlit as st
import pandas as pd

import psycopg2

from psycopg2 import sql
from typing import List, Tuple


# Функция для определения типов данных столбцов на основе данных CSV
def get_column_data_types(csv_data: pd.DataFrame) -> List[Tuple[str, str]]:
    data_types = []
    for column, dtype in csv_data.dtypes.iteritems():
        if dtype == "int64":
            data_types.append((column, "INTEGER"))
        elif dtype == "float64":
            data_types.append((column, "FLOAT"))
        else:
            data_types.append((column, "TEXT"))
    return data_types


# Функция для загрузки данных из CSV файла в PostgreSQL
def upload_csv_to_postgres(
        csv_data: pd.DataFrame,
        connection: psycopg2.extensions.connection,
        table_name: str
):
    cursor = connection.cursor()

    # Определение типов данных столбцов на основе CSV данных
    column_data_types = get_column_data_types(csv_data)

    # Создание таблицы в PostgreSQL с соответствующими типами данных
    create_table_query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS {} ({});"
    ).format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(
            sql.SQL('{} {}').format(sql.Identifier(col_name), sql.SQL(col_type))
            for col_name, col_type in column_data_types
        )
    )
    cursor.execute(create_table_query)

    # Загрузка данных из DataFrame в таблицу PostgreSQL
    csv_data.to_sql(table_name, connection, if_exists="append", index=False)

    connection.commit()

    st.success("Данные успешно загружены в PostgreSQL!")


