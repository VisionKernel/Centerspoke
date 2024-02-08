import pandas as pd
import mysql.connector
from contextlib import contextmanager
from decimal import Decimal
from data_processing import clean_data

@contextmanager
def mysql_cursor(connection):
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()

def get_mysql_data_type(pandas_dtype):
    if pandas_dtype.name.startswith('int'):
        return 'INT'
    elif pandas_dtype.name.startswith('float'):
        return 'FLOAT'
    elif pandas_dtype.name.startswith('datetime'):
        return 'DATETIME'
    elif pandas_dtype.name.startswith('bool'):
        return 'BOOLEAN'
    else:
        return 'VARCHAR(255)'

def auto_create_table_from_excel(connection, table_name, excel_file_path, sheet_name):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    df = clean_data(df)  # Enhanced cleaning with the updated data_processing script

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    column_definitions = []
    for col in df.columns:
        formatted_col = col.replace(" ", "_").lower()
        col_data_type = get_mysql_data_type(df[col].dtype)
        column_definitions.append(f"{formatted_col} {col_data_type}")
    create_table_sql += ', '.join(column_definitions) + ");"

    with mysql_cursor(connection) as cursor:
        cursor.execute(create_table_sql)
        connection.commit()
    print(f"Table '{table_name}' created successfully.")

def upload_excel_data(connection, table_name, excel_file_path, sheet_name):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    df = clean_data(df)  # Apply comprehensive cleaning and processing

    df = df.where(pd.notna(df), None)

    columns = ', '.join([f'`{col.replace(" ", "_").lower()}`' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    records = [tuple(row) for row in df.to_records(index=False)]

    with mysql_cursor(connection) as cursor:
        cursor.executemany(insert_query, records)
        connection.commit()
    print(f"Data uploaded successfully to '{table_name}'.")

def upload_data_to_mysql(connection, table_name, df: pd.DataFrame):
    df = clean_data(df)  # Apply comprehensive cleaning and processing

    df = df.where(pd.notna(df), None)

    columns = ', '.join([f'`{col}`' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    records = [tuple(row) for row in df.to_records(index=False)]

    with mysql_cursor(connection) as cursor:
        cursor.executemany(insert_query, records)
        connection.commit()
    print(f"Data uploaded successfully to '{table_name}'.")

