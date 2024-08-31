from influxdb import InfluxDBClient
from args_module import parse_args
from getpass import getpass

def create_database(client, db_name):
    """Create a new database in InfluxDB."""
    print(f"Creating database '{db_name}'...")
    client.create_database(db_name)
    print(f"Database '{db_name}' created successfully.")

def create_user(client, username, password, permissions):
    """Create a new user in InfluxDB with specified permissions."""
    print(f"Creating user '{username}' with {permissions} permissions...")
    if permissions == 'read':
        client.create_user(username, password, permissions=['read'])
    elif permissions == 'write':
        client.create_user(username, password, permissions=['write'])
    elif permissions == 'all':
        client.create_user(username, password, admin=True)
    else:
        raise ValueError(f"Invalid permissions: {permissions}")
    print(f"User '{username}' created successfully.")

def main():
    # Parse all arguments from args_module.py
    args = parse_args()

    # Connect to the InfluxDB instance
    client = InfluxDBClient(host=args.host, port=args.port, username=args.username, password=args.password, database=args.database)

    # Handle database creation
    if args.database_creation:
        db_name = args.database_creation if isinstance(args.database_creation, str) else input("Enter database name: ")
        create_database(client, db_name)

    # Handle user creation
    if args.user_creation:
        username = args.user_creation if isinstance(args.user_creation, str) else input("Enter username: ")
        password = args.password_creation if isinstance(args.password_creation, str) else getpass("Enter password: ")
        permissions = args.permissions if isinstance(args.permissions, str) else input("Enter permissions (read, write, all): ")
        create_user(client, username, password, permissions)

    # Close the connection
    client.close()

if __name__ == "__main__":
    main()
