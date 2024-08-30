import argparse
from influxdb import InfluxDBClient
import os
import getpass
import sys
import time
import threading

# Set up argument parser
parser = argparse.ArgumentParser(description='Count rows in InfluxDB measurements.')

# Add arguments with default values
parser.add_argument('-H', '--host', type=str, default='172.16.20.42', help='InfluxDB host IP address')
parser.add_argument('-P', '--port', type=int, default=8086, help='InfluxDB port number (default 8086)')
parser.add_argument('-u', '--username', type=str, default=os.getenv('INFLUXDB_USER', 'user'), help='InfluxDB username')
parser.add_argument('-p', '--password', type=str, default=os.getenv('INFLUXDB_PASSWORD', 'password'), help='InfluxDB password')
parser.add_argument('-d', '--database', type=str, default='supervision', help='InfluxDB database name')
parser.add_argument('-K', '--ask-pass', action='store_true', help='Prompt for the InfluxDB password')
parser.add_argument('--more-info', action='store_true', help='Display additional information about measurements')

# Parse the arguments
args = parser.parse_args()

# Prompt for password if --ask-pass is specified
if args.ask_pass:
    args.password = getpass.getpass(prompt='InfluxDB Password: ')

# Spinner animation
def spinner_animation(message="Processing"):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_spinner:
        sys.stdout.write(f"\r{message}... {spinner[idx % len(spinner)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

# Flag to stop spinner
stop_spinner = False

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

try:
    # Connect to InfluxDB using the provided or default arguments
    client = InfluxDBClient(host=args.host, port=args.port, username=args.username, password=args.password)

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

    # Start the spinner animation in a separate thread
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinner_animation)
    spinner_thread.start()

    try:
        # Execute the query
        result = client.query(query)
        
        # Stop the spinner animation
        stop_spinner = True
        spinner_thread.join()
        sys.stdout.write("\r")  # Clear the spinner line
        
        # Retrieve and sum the count
        for point in result.get_points():
            count = point['count']
            total_count += count
            print(f'Database: {args.database}, Measurement: {measurement_name}, Count: {count}')
    except Exception as e:
        stop_spinner = True
        spinner_thread.join()
        sys.stdout.write("\r")  # Clear the spinner line
        print(f"Error executing query on measurement '{measurement_name}' in database '{args.database}': {e}")
        continue

# Output results
print(f'Total rows across all measurements in database {args.database}: {total_count}\n')
print(personalized_message(total_count))
