import argparse
from influxdb import InfluxDBClient
import os

# Set up argument parser
parser = argparse.ArgumentParser(description='Count rows in InfluxDB measurements.')

# Add arguments with default values
parser.add_argument('-H', '--host', type=str, default='172.16.20.42', help='InfluxDB host IP address')
parser.add_argument('-P', '--port', type=int, default=8086, help='InfluxDB port number (default 8086)')
parser.add_argument('-u', '--username', type=str, default=os.getenv('INFLUXDB_USER', 'user'), help='InfluxDB username')
parser.add_argument('-p', '--password', type=str, default=os.getenv('INFLUXDB_PASSWORD', 'password'), help='InfluxDB password')
parser.add_argument('-d', '--database', type=str, default='supervision', help='InfluxDB database name')

# Parse the arguments
args = parser.parse_args()

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
        return "Maybe some retention policies?"
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
	print(f"Error connection to InfluxDB: {e}")
	exit(1)

try:
	# Get all measurements
	measurements = client.get_list_measurements()
except Exception as e:
	print(f"Error fetching measurements: {e}")
	exit(1)

total_count = 0

# Iterate through each measurement
for measurement in measurements:
    measurement_name = measurement['name']
    query = f'SELECT COUNT(x) FROM (SELECT *,x::INTEGER FROM "{measurement_name}" FILL(0))'
    
    # Execute the query
    result = client.query(query)
    
    # Retrieve and sum the count
    for point in result.get_points():
        count = point['count']
        total_count += count
        print(f'Database: {args.database}, Measurement: {measurement_name}, Count: {count}')

print(f'Total rows across all measurements in database {args.database}: {total_count}\n')
print(personalized_message(total_count))
