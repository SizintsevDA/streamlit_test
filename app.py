import streamlit as st
import pandas as pd
import psycopg2

# Streamlit configuration
st.set_page_config(page_title="CSV to PostgreSQL", layout="wide")


# Database connection function
def create_connection():
    conn = psycopg2.connect(
        database="your_database",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    return conn


# Streamlit app
def main():
    st.title("CSV to PostgreSQL Upload")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded data:")
        st.write(df)

        if st.button("Upload to PostgreSQL"):
            conn = create_connection()
            cursor = conn.cursor()

            for index, row in df.iterrows():
                query = "INSERT INTO your_table (column1, column2, ...) VALUES (%s, %s, ...)"
                data = tuple(row)  # Make sure the order matches the columns in the query
                cursor.execute(query, data)

            conn.commit()
            conn.close()

            st.success("Data uploaded to PostgreSQL!")


if __name__ == "__main__":
    main()
