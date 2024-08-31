import argparse
import os
import getpass

def parse_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Count rows in InfluxDB measurements.')

    # Add arguments with default values
    parser.add_argument('-H', '--host', type=str, default='172.16.20.42', help='InfluxDB host IP address')
    parser.add_argument('-P', '--port', type=int, default=8086, help='InfluxDB port number (default 8086)')
    parser.add_argument('-u', '--username', type=str, default=os.getenv('INFLUXDB_USER', 'user'), help='InfluxDB username')
    parser.add_argument('-p', '--password', type=str, nargs='?', default=None, help='InfluxDB password (will prompt if not provided)')
    parser.add_argument('-d', '--database', type=str, default='supervision', help='InfluxDB database name')
    parser.add_argument('--more-info', action='store_true', help='Display additional information about measurements')

    # Parse the arguments
    args = parser.parse_args()

    # Prompt for password if --password is specified without a value
    if args.password is None:
        args.password = getpass.getpass(prompt='InfluxDB Password: ')

    return args
