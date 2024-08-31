# main.py
from influxdb import InfluxDBClient # type: ignore
import sys
from args_module import parse_args
from spinner_module import start_spinner, stop_spinner

def database_exists(client, db_name):
    """Check if a database exists in InfluxDB."""
    try:
        databases = client.get_list_database()
        return any(db['name'] == db_name for db in databases), databases
    except Exception as e:
        print(f"Error retrieving database list: {e}")
        sys.exit(1)

def personalized_message(total_count):
    if total_count < 10:
        return "Do you even need this script?"
    elif total_count < 100000:
        return "You're done counting I guess..."
    elif total_count < 1000000:
        return "Your latencies are just a story, not the cause of your worry."
    elif total_count < 10000000:
        return "Damn! That's a base!"
    elif total_count < 100000000:
        return "Maybe some data retention policies?"
    elif total_count < 1000000000:
        return "You’ve got some lines, so enjoy the time!"
    else:
        return "Over the rainbow..."

# Main script execution
if __name__ == "__main__":
    # Parse arguments
    args = parse_args()

    try:
        # Connect to InfluxDB using the provided or default arguments
        client = InfluxDBClient(host=args.host, port=args.port, username=args.username, password=args.password)

        # Check if the specified database exists
        exists, databases = database_exists(client, args.database)
        if not exists:
            print(f"Error: The specified database '{args.database}' does not exist.")
            view_databases = input("Would you like to see a list of existing databases? (yes/no): ").strip().lower()
            if view_databases == 'yes':
                print("Existing databases:")
                for db in databases:
                    print(f" - {db['name']}")
            else:
                print("You can still find cute information using inspector.py")
            sys.exit(1)

        # Switch to the specified or default database
        client.switch_database(args.database)

    except Exception as e:
        print(f"Error connecting to InfluxDB database '{args.database}': {e}")
        exit(1)

    try:
        # Get all measurements
        measurements = client.get_list_measurements()
    except Exception as e:
        print(f"Error fetching measurements from database '{args.database}': {e}")
        exit(1)

    total_count = 0
    measurement_count = len(measurements)

    if args.more_info:
        print(f'Total measurements found: {measurement_count}')
        print('Measurements:')
        for measurement in measurements:
            measurement_name = measurement['name']
            print(f' - {measurement_name}')
            
            # Fetch and display field keys
            field_keys = client.query(f'SHOW FIELD KEYS FROM "{measurement_name}"')
            field_keys_list = [point['fieldKey'] for point in field_keys.get_points()]
            print(f'  Field Keys: {", ".join(field_keys_list)}')

            # Fetch and display tag keys
            tag_keys = client.query(f'SHOW TAG KEYS FROM "{measurement_name}"')
            tag_keys_list = [point['tagKey'] for point in tag_keys.get_points()]
            print(f'  Tag Keys: {", ".join(tag_keys_list)}')
            print("\n")

    # Iterate through each measurement
    for measurement in measurements:
        measurement_name = measurement['name']
        query = f'SELECT COUNT(x) FROM (SELECT *,x::INTEGER FROM "{measurement_name}" FILL(0))'

        # Start the spinner animation
        stop_event, spinner_thread = start_spinner()

        try:
            # Execute the query
            result = client.query(query)
            
            # Stop the spinner animation
            stop_spinner(stop_event, spinner_thread)

            # Retrieve and sum the count
            for point in result.get_points():
                count = point['count']
                total_count += count
                print(f'Database: {args.database}, Measurement: {measurement_name}, Count: {count}')
        except Exception as e:
            stop_spinner(stop_event, spinner_thread)
            print(f"Error executing query on measurement '{measurement_name}' in database '{args.database}': {e}")
            continue

    # Output results
    print(f'Total rows across all measurements in database {args.database}: {total_count}\n')
    print(personalized_message(total_count))

