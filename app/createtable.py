from contextlib import contextmanager

@contextmanager
def mysql_cursor(connection):
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


# Function to create a custom table in a database
def create_custom_table(connection, table_name, columns):
    try:
        with mysql_cursor(connection) as cursor:
            # Start the CREATE TABLE statement
            table_creation_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("

            # Add columns to the statement
            for column_name, column_type in columns:
                # Ensure column names that are numeric or reserved keywords are enclosed in backticks
                column_name = f"`{column_name}`" if column_name.isdigit() or is_reserved_keyword(column_name) else column_name
                table_creation_sql += f"{column_name} {column_type},"

            # Remove the last comma and close the parenthesis
            table_creation_sql = table_creation_sql.rstrip(',') + ');'

            # Execute the SQL statement
            cursor.execute(table_creation_sql)
        
        connection.commit()
        print(f"Table '{table_name}' created successfully!")

    except Exception as e:
        print(f"Error creating table: {e}")

def is_reserved_keyword(word):
    # Placeholder function for checking if a word is a reserved SQL keyword
    # You might need to implement a proper check based on your SQL dialect
    reserved_keywords = ["SELECT", "FROM", "WHERE"]  # Add all reserved keywords
    return word.upper() in reserved_keywords

# Function to list all tables in a database
def list_tables(connection):
    try:
        # Create a cursor object using the connection
        with mysql_cursor(connection) as cursor:
            # SQL statement to list all tables
            list_tables_sql = """
                SHOW TABLES;
            """
            # Execute the SQL statement
            cursor.execute(list_tables_sql)
            # Fetch all rows from the result of the SQL statement
            # and extract the first column (table name) from each row
            existing_tables = [row[0] for row in cursor.fetchall()]
        # Return the list of table names
        return existing_tables

    except Exception as e:
        # Print an error message if something goes wrong
        print(f"Error listing tables: {e}")
        # Return an empty list
        return []