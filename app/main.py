import os
import argparse
import getpass
from convert import convert_to_excel
from connectdatabase import connect_to_aws_rds, connect_to_azure_sql, connect_to_google_cloud_sql, connect_to_google_cloud_storage, create_table_mysql, create_table_azure_sql, create_table_gcloud_sql
from createtable import create_custom_table, list_tables
from uploaddata import upload_excel_data, auto_create_table_from_excel


def main():
    connection = None

    parser = argparse.ArgumentParser(description="Database Connection and CSV/Text to Excel Converter")

    # Add subparsers for different actions
    subparsers = parser.add_subparsers(dest='action', help="Choose an action")

    # Subparser for CSV/Text to Excel conversion
    csv_to_excel_parser = subparsers.add_parser('convert', help="Convert CSV/Text to Excel")
    csv_to_excel_parser.add_argument("input_file", help="Input file to convert")
    csv_to_excel_parser.add_argument("output_file", help="Output Excel file")

    # Subparser for AWS RDS database connection
    aws_db_parser = subparsers.add_parser('aws', help="Connect to AWS RDS Database")
    aws_db_parser.add_argument("--database-endpoint", help="AWS RDS database instance identifier")
    aws_db_parser.add_argument("--database-name", help="Database Name")
    aws_db_parser.add_argument("--port", help="Port Number")
    aws_db_parser.add_argument("--username", help="Database username")
    aws_db_parser.add_argument("--password", help="Database password")

    # Add subparser for AWS function
    aws_db_subparsers = aws_db_parser.add_subparsers(dest='aws_action', help='AWS action to perform')

    # Create database via AWS RDS
    create_aws_db_parser = aws_db_subparsers.add_parser('newdatabase', help="Create a new database in AWS RDS")
    create_aws_db_parser.add_argument("--new-database-name", help="Name of the new database to create")

    # Create table via AWS RDS database
    create_aws_table_parser = aws_db_subparsers.add_parser('createtable', help="Create a new table in AWS RDS")
    create_aws_table_parser.add_argument("--table-name", help="Name of the new table to create")

    # Subparser for Azure SQL database connection
    azure_db_parser = subparsers.add_parser('azure', help="Connect to Azure SQL Database")
    azure_db_parser.add_argument("--server-name", help="Azure SQL server name")
    azure_db_parser.add_argument("--database-name", help="Name of the database")
    azure_db_parser.add_argument("--username", help="Database username")

    # Subparser for Google Cloud SQL database connection
    gcp_db_parser = subparsers.add_parser('gcp', help="Connect to Google Cloud SQL Database")
    gcp_db_parser.add_argument("--instance-connection-name", help="Google Cloud SQL instance connection name")
    gcp_db_parser.add_argument("--database-name", help="Name of the database")
    gcp_db_parser.add_argument("--username", help="Database username")

    # Subparser for Google Cloud Storage connection
    gcp_storage_parser = subparsers.add_parser('gcp-storage', help="Connect to Google Cloud Storage")
    gcp_storage_parser.add_argument("--bucket-name", help="Google Cloud Storage bucket name")

    args = parser.parse_args()


    if args.action == 'convert':
        convert_to_excel(args.input_file, args.output_file)
    # ...

    elif args.action == 'aws':
        # AWS RDS database connection setup
        database_name = args.database_name or input("Enter database name: ")
        database_endpoint = args.database_endpoint or input("Enter the AWS RDS database instance identifier: ")
        username = args.username or input("Enter the database username: ")
        password = args.password or input("Enter the database password: ")
        port = args.port or input("Enter port: ")

        connection = connect_to_aws_rds(database_name, username, password, database_endpoint, port)

        existing_tables = list_tables(connection)
        decoded_table_names = [table_name.decode('utf-8') for table_name in existing_tables]
        print("Existing tables:", decoded_table_names)

        if connection:
            upload_data_response = input("Would you like to upload data from an excel file? (y/n): ").lower()

            if upload_data_response == 'y':
                excel_file_path = input("Enter the path to the excel file: ")
                sheet_name = input("Enter the name of the sheet to upload: ")

                create_table_response = input("Would you like to create a new table? (y/n): ").lower()

                if create_table_response == 'y':
                    table_name = input("Enter the name of the new table: ")
                    auto_create_table_from_excel(connection, table_name, excel_file_path, sheet_name)
                else:
                    table_name = input("Enter the name of the table to upload to: ")

                upload_excel_data(connection, table_name, excel_file_path, sheet_name)

                connection.close()

        # ... similar structure for 'azure' and 'gcp' ...



    elif args.action == 'azure':
        # Azure SQL database connection
        server_name = args.server_name or input("Enter the Azure SQL server name: ")
        database_name = args.database_name or input("Enter the name of the database: ")
        username = args.username or input("Enter the database username: ")
        password = getpass.getpass("Enter the database password: ")
        connection = connect_to_azure_sql(server_name, database_name, username, password)
        # Perform database operations using the 'connection' object

    elif args.action == 'gcp':
        # Google Cloud SQL database connection
        instance_connection_name = args.instance_connection_name or input("Enter the Google Cloud SQL instance connection name: ")
        database_name = args.database_name or input("Enter the name of the database: ")
        username = args.username or input("Enter the database username: ")
        password = getpass.getpass("Enter the database password: ")
        connection = connect_to_google_cloud_sql(instance_connection_name, database_name, username, password)
        # Perform database operations using the 'connection' object

    elif args.action == 'gcp-storage':
        # Google Cloud Storage connection
        bucket_name = args.bucket_name or input("Enter the Google Cloud Storage bucket name: ")
        bucket = connect_to_google_cloud_storage(bucket_name)
        # Perform Google Cloud Storage operations using the 'bucket' object

    elif args.action == 'create-table':
        # Create a new table in the database
        if args.action == 'create-table':
            # Database-specific create table function based on the connection type
            create_table_function = None

            if args.database_endpoint:
                connection = connect_to_aws_rds(args.database_endpoint, args.database_name, args.username, password)
                create_table_mysql(connection, args.table_name, args.column_definitions)
            elif args.server_name:
                connection = connect_to_azure_sql(args.server_name, args.database_name, args.username, password)
                create_table_azure_sql(connection, args.table_name, args.column_definitions)
            elif args.instance_connection_name:
                connection = connect_to_google_cloud_sql(args.instance_connection_name, args.database_name, args.username, password)
                create_table_gcloud_sql(connection, args.table_name, args.column_definitions)

            if create_table_function:
                create_table_function(connection, args.table_name, args.column_definitions)


if __name__ == "__main__":
    main()