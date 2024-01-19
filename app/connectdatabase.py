# Import necessary libraries
import boto3
import mysql.connector
import pyodbc
from google.cloud import storage

# Function to connect to AWS RDS
def connect_to_aws_rds(database_name, username, password, database_endpoint, port):
    try:
        # Establish connection
        conn = mysql.connector.connect(
            user=username,
            password=password,
            host=database_endpoint,
            database=database_name,
            port=int(port)
        )

        print("Connected to the AWS RDS database successfully!")
        return conn

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to connect to Azure SQL
def connect_to_azure_sql(server_name, database_name, username, password):
    try:
        # Establish connection
        connection_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server_name}.database.windows.net;Database={database_name};UID={username};PWD={password};"
        conn = pyodbc.connect(connection_str)

        print("Connected to Azure SQL Database successfully!")
        return conn

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to connect to Google Cloud SQL
def connect_to_google_cloud_sql(instance_connection_name, database_name, username, password):
    try:
        # Establish connection
        conn = mysql.connector.connect(
            user=username,
            password=password,
            host=instance_connection_name,
            database=database_name
        )

        print("Connected to Google Cloud SQL Database successfully!")
        return conn

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to connect to Google Cloud Storage
def connect_to_google_cloud_storage(bucket_name):
    try:
        # Establish connection
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)

        print(f"Connected to Google Cloud Storage bucket '{bucket_name}' successfully!")
        return bucket

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to create a table in MySQL
def create_table_mysql(connection, table_name, column_definitions):
    try:
        cursor = connection.cursor()
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to create a table in Azure SQL
def create_table_azure_sql(connection, table_name, column_definitions):
    try:
        cursor = connection.cursor()
        create_table_query = f"CREATE TABLE {table_name} ({column_definitions})"
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully in Azure SQL Database!")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to create a table in Google Cloud SQL
def create_table_gcloud_sql(connection, table_name, column_definitions):
    try:
        cursor = connection.cursor()
        create_table_query =  f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully in Google Cloud SQL Database!")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
