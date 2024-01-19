import boto3
import psycopg2

def get_user_input():
    print("Enter your AWS RDS configuration:")
    database_endpoint = input("RDS Endpoint: ")
    port = input("Port Number (default 5432 for PostgreSQL): ")
    username = input("Username: ")
    password = input("Password: ")
    region = input("AWS Region: ")

    return {
        "database_endpoint": database_endpoint,
        "port": port,
        "username": username,
        "password": password,
        "region": region
    }

def connect_to_aws_rds(config):
    try:
        session = boto3.Session(region_name=config["region"])
        client = session.client('rds')

        token = client.generate_db_auth_token(
            DBHostname=config["database_endpoint"],
            Port=int(config["port"]),
            DBUsername=config["username"],
            Region=config["region"]
        )

        conn = psycopg2.connect(
            user=config["username"],
            password=token,
            host=config["database_endpoint"],
            port=int(config["port"])
        )

        print("Connected to the AWS RDS database successfully!")
        return conn

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def list_databases(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT datname FROM pg_database;")
            databases = cursor.fetchall()
            print("List of Databases:")
            for db in databases:
                print(db[0])

    except Exception as e:
        print(f"Error listing databases: {e}")

def main():
    user_config = get_user_input()
    connection = connect_to_aws_rds(user_config)

    # Perform database operations using the 'connection' object if the connection is successful
    if connection:
        list_databases(connection)

        # Don't forget to close the connection when done
        connection.close()

if __name__ == "__main__":
    main()