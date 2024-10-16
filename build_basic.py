from influxdb import InfluxDBClient # type: ignore
from args_module import parse_args
from getpass import getpass
import sys
import requests # type: ignore

def create_database(client, db_name):
    """Create a new database in InfluxDB."""
    print(f"Creating database '{db_name}'...")
    client.create_database(db_name)
    print(f"Database '{db_name}' created successfully.")

def create_user(client, username, password, permissions):
    """Create a new user in InfluxDB with specified permissions."""
    print(f"Creating user '{username}' with {permissions} permissions...")

    # Create the user without setting permissions
    client.create_user(username, password)
    print(f"User '{username}' created successfully.")

    # Assign the correct permissions for the new user
    if permissions == 'read':
        client.query(f"GRANT READ ON {client._database} TO {username}")
    elif permissions == 'write':
        client.query(f"GRANT WRITE ON {client._database} TO {username}")
    elif permissions == 'all':
        client.grant_admin_privileges(username)
    else:
        raise ValueError(f"Invalid permissions: {permissions}")
    print(f"Permissions '{permissions}' granted to user '{username}'.")

def main():
    # Parse all arguments from args_module.py
    args = parse_args()

    # Connect to the InfluxDB instance
    try:
        # Connect to the InfluxDB instance
        client = InfluxDBClient(host=args.host, port=args.port, username=args.username, password=args.password, database=args.database)
        client.ping()  # Check connection

    except requests.exceptions.ConnectionError as e:
        print(f"Error: Unable to connect to InfluxDB at {args.host}:{args.port}. Connection refused.")
        sys.exit(1)  # Exit the script with an error status

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    # Handle database creation
    if args.database_creation:
        db_name = args.database_creation if isinstance(args.database_creation, str) else input("Enter database name: ")
        create_database(client, db_name)
    # Handle database creation
    #if args.database_creation:
    #    db_name = args.database_creation if isinstance(args.database_creation, str) else input("Enter database name: ")
    #    create_database(client, db_name)

    # Handle user creation
    if args.user_creation:
        username = args.user_creation if isinstance(args.user_creation, str) else input("Enter username: ")

        # Prompt for password if not provided
        if args.password_creation:
            password = args.password_creation
        else:
            password = getpass("Enter password for the new user: ")

        # Prompt for permissions if not provided
        if args.permissions:
            permissions = args.permissions
        else:
            permissions = input("Enter permissions for the new user (read, write, all): ")

        create_user(client, username, password, permissions)

    # Close the connection
    client.close()

if __name__ == "__main__":
    main()
