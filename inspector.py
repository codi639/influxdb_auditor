from influxdb import InfluxDBClient  # type: ignore
import sys
from args_module import parse_args

def list_databases(client):
    """List all databases in InfluxDB."""
    try:
        return client.get_list_database()
    except Exception as e:
        print(f"Error retrieving database list: {e}")
        sys.exit(1)

def list_users(client):
    """List all users in InfluxDB."""
    try:
        return list(client.query('SHOW USERS').get_points())  # Convert generator to list
    except Exception as e:
        print(f"Error retrieving user list: {e}")
        sys.exit(1)

def get_measurements(client, database):
    """Get all measurements for a specific database."""
    try:
        client.switch_database(database)
        measurements = client.get_list_measurements()
        return measurements
    except Exception as e:
        print(f"Error retrieving measurements for database '{database}': {e}")
        return []

def main():
    # Parse arguments
    args = parse_args()

    try:
        # Connect to InfluxDB using the provided or default arguments
        client = InfluxDBClient(host=args.host, port=args.port, username=args.username, password=args.password)

        # Retrieve all databases and users
        databases = list_databases(client)
        users = list_users(client)

        # Display all users and databases in columns
        print(f"{'Users':<30} | {'Databases':<30}")
        print('-' * 65)

        # Create a list of database names
        db_names = [db['name'] for db in databases]
        
        # Determine the maximum number of rows for columns
        max_rows = max(len(users), len(db_names))
        
        # Print users and databases in columns
        for i in range(max_rows):
            user = users[i]['user'] if i < len(users) else ''
            db_name = db_names[i] if i < len(db_names) else ''
            print(f"{user:<30} | {db_name:<30}")

        # Close the Users | Databases table
        print('-' * 65)

        # Display measurements if --more-info is provided
        if args.more_info:
            for db in db_names:
                measurements = get_measurements(client, db)
                print(f"Database: {db}")
                if measurements:
                    print("  Measurements:")
                    for measurement in measurements:
                        print(f"   - {measurement['name']}")
                else:
                    print("  No measurements found.")
                print()

    except Exception as e:
        print(f"Error connecting to InfluxDB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
