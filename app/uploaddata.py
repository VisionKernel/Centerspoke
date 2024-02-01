# Import necessary libraries
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

# Function to map pandas data types to MySQL data types
def get_mysql_data_type(pandas_dtype):
    """Maps pandas data types to MySQL data types."""
    if pandas_dtype.name.startswith('int'):
        return 'INT'  # MySQL integer type
    elif pandas_dtype.name.startswith('float'):
        return 'FLOAT'  # or 'DOUBLE' for higher precision
    elif pandas_dtype.name.startswith('datetime'):
        return 'DATETIME'  # MySQL datetime type
    elif pandas_dtype.name.startswith('bool'):
        return 'BOOLEAN'
    else:
        return 'VARCHAR(255)'  # Default to VARCHAR for other types

# Function to create a MySQL table based on the structure of an Excel file
def auto_create_table_from_excel(connection, table_name, excel_file_path, sheet_name):
    try:
        # Read Excel file into a Pandas DataFrame
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

        # df = clean_data(df)

        # Start creating the SQL statement
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        # Generate column definitions
        column_definitions = []
        for col in df.columns:
            # Format column name for SQL (replace spaces, etc.)
            formatted_col = str(col).replace(" ", "_").lower()
            col_data_type = get_mysql_data_type(df[col].dtype)
            column_definitions.append(f"{formatted_col} {col_data_type}")

        # Combine column definitions and complete SQL statement
        create_table_sql += ', '.join(column_definitions) + ");"

        # Execute the SQL statement to create a new table
        with mysql_cursor(connection) as cursor:
            cursor.execute(create_table_sql)
            connection.commit()

        print(f"Table '{table_name}' created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")

# Function to upload data from an Excel file to a MySQL table

def upload_excel_data(connection, table_name, excel_file_path, sheet_name):
    try:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        df = df.dropna(how='all')  # Remove rows with all NaN values
        
        # Explicitly check column names for "DATE" or date-like naming to apply datetime formatting
        for col in df.columns:
            if 'date' in col.lower():  # A simple heuristic to target date columns
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
            else:
                # Handle numeric data, preserving original values
                col_type = get_mysql_data_type(df[col].dtype)
                if col_type == 'FLOAT':
                    df[col] = df[col].apply(lambda x: Decimal(str(x)) if pd.notnull(x) else None)
                elif col_type == 'BOOLEAN':
                    df[col] = df[col].astype(int)
        
        print(df.head())  # Print after processing all columns

        # Convert NaN values to None for SQL compatibility
        df = df.where(pd.notna(df), None)

        # Format column names and create SQL statement
        columns = ', '.join([f'`{col}`' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

        # Create a list of tuples from the DataFrame
        records = [tuple(row) for row in df.to_records(index=False)]

        with mysql_cursor(connection) as cursor:
            # Execute the SQL query for insertion
            print("Insert Query:", insert_query)
            print("Sample Records:", records[:5])  # Print first 5 records as a sample
            cursor.executemany(insert_query, records)
            connection.commit()

        print(f"Data uploaded successfully to '{table_name}'.")

    except Exception as e:
        print(f"Error uploading data: {e}")

def upload_data_to_mysql(connection, table_name, df: pd.DataFrame):
    try:
        # Ensure data types are compatible with MySQL
        for col in df.columns:
            col_type = get_mysql_data_type(df[col].dtype)
            if col_type == 'DATETIME':
                df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
            elif col_type == 'INT':
                df[col] = df[col].apply(lambda x: round(x) if pd.notna(x) else None)
            elif col_type == 'FLOAT':
                df[col] = df[col].apply(lambda x: Decimal(str(x)) if pd.notna(x) else None)
            elif col_type == 'BOOLEAN':
                df[col] = df[col].astype(int)

        # Convert NaN values to None for SQL compatibility
        df = df.where(pd.notna(df), None)

        # Format column names and create SQL statement
        columns = ', '.join([f'`{col}`' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

        # Create a list of tuples from the DataFrame
        records = [tuple(row) for row in df.to_records(index=False)]

        with mysql_cursor(connection) as cursor:
            # Execute the SQL query for insertion
            cursor.executemany(insert_query, records)
            connection.commit()

        print(f"Data uploaded successfully to '{table_name}'.")

    except Exception as e:
        print(f"Error uploading data: {e}")
