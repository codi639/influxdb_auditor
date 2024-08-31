import argparse
import os
import getpass

def parse_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='InfluxDB Setup Script.')

    # Connection arguments
    parser.add_argument('-H', '--host', type=str, default='172.16.20.42', help='InfluxDB host IP address')
    parser.add_argument('-P', '--port', type=int, default=8086, help='InfluxDB port number (default 8086)')
    parser.add_argument('-u', '--username', type=str, default=os.getenv('INFLUXDB_USER', 'user'), help='InfluxDB username')
    parser.add_argument('-p', '--password', type=str, nargs='?', default=None, help='InfluxDB password (will prompt if not provided)')
    parser.add_argument('-d', '--database', type=str, default='supervision', help='InfluxDB database name')
    parser.add_argument('--more-info', action='store_true', help='Display additional information about measurements')

    # Database and user creation arguments
    parser.add_argument('-dc', '--database-creation', type=str, nargs='?', const=True, help='Create a new database with the specified name.')
    parser.add_argument('-uc', '--user-creation', type=str, nargs='?', const=True, help='Create a new user with the specified username.')
    parser.add_argument('-pc', '--password-creation', type=str, nargs='?', const=True, help='Password for the new user.')
    parser.add_argument('-per', '--permissions', type=str, choices=['read', 'write', 'all'], nargs='?', const=True, help='Permissions for the new user. Choose from: read, write, all.')

    # Parse the arguments
    args = parser.parse_args()

    # Prompt for password if --password is specified without a value
    if args.password is None:
        args.password = getpass.getpass(prompt='InfluxDB Password: ')

    return args