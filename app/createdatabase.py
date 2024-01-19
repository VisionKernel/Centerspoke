import mysql.connector

def create_database(connection, new_database_name):
    cursor = None
    try:
        # Ensure autocommit mode is enabled
        connection.autocommit = True

        cursor = connection.cursor()
        # Execute a SQL query to create a new database
        cursor.execute(f"CREATE DATABASE {new_database_name};")
        print(f"Database '{new_database_name}' created successfully!")

    except Exception as e:
        print(f"An error occurred while creating the database: {e}")

    finally:
        if cursor:
            cursor.close()
        # Restore autocommit mode to its original state
        connection.autocommit = False