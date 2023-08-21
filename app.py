import streamlit as st
import pandas as pd
import psycopg2

# Настройки окна приложения в streamlit
st.set_page_config(page_title="Загрузка файлов CSV в хранилище данных (PostgreSQL)", layout="wide")


# Параметры подключения к PostgreSQL
def create_connection():
    conn = psycopg2.connect(
        database="your_database",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    return conn


# Само приложение
def main():
    st.title("Загрузка файлов CSV ввввв хранилище данных (PostgreSQL)")

    uploaded_file = st.file_uploader("Загрузите CSV файл с вашего компьютера", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Загруженный файл:")
        st.write(df)

        if st.button("Загрузить в PostgreSQL"):
            conn = create_connection()
            cursor = conn.cursor()

            for index, row in df.iterrows():
                query = "INSERT INTO your_table (column1, column2, ...) VALUES (%s, %s, ...)"
                data = tuple(row)  # надо подумать насчет размера таблиц
                cursor.execute(query, data)

            conn.commit()
            conn.close()

            st.success("Данные успешно загружены!")


if __name__ == "__main__":
    main()
