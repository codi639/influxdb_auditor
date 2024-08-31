import argparse
import os
import getpass

def parse_args():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='InfluxDB Setup Script.')

    # Connection arguments group
    conn_group = parser.add_argument_group('Connection Arguments', 'Arguments for connecting to InfluxDB')
    conn_group.add_argument('-H', '--host', type=str, default='localhost', help='InfluxDB host IP address')
    conn_group.add_argument('-P', '--port', type=int, default=8086, help='InfluxDB port number (default 8086)')
    conn_group.add_argument('-u', '--username', type=str, default=os.getenv('INFLUXDB_USER', 'user'), help='InfluxDB username')
    conn_group.add_argument('-p', '--password', type=str, nargs='?', default=os.getenv('INFLUXDB_PASS', None), help='InfluxDB password (will prompt if not provided)')
    conn_group.add_argument('-d', '--database', type=str, default='lorem_ipsum', help='InfluxDB database name')

    # Additional information arguments group
    info_group = parser.add_argument_group('Information Arguments', 'Arguments for displaying additional information')
    info_group.add_argument('--more-info', action='store_true', help='Display additional information about measurements')

    # Database and user creation arguments group
    db_user_group = parser.add_argument_group('Database and User Creation', 'Arguments for creating databases and users')
    db_user_group.add_argument('-dc', '--database-creation', type=str, nargs='?', const=True, help='Create a new database with the specified name.')
    db_user_group.add_argument('-uc', '--user-creation', type=str, nargs='?', const=True, help='Create a new user with the specified username.')
    db_user_group.add_argument('-pc', '--password-creation', type=str, nargs='?', const=True, help='Password for the new user.')
    db_user_group.add_argument('-per', '--permissions', type=str, choices=['read', 'write', 'all'], nargs='?', const=True, help='Permissions for the new user. Choose from: read, write, all.')

    # Data generation arguments group
    data_group = parser.add_argument_group('Data Generation', 'Arguments for generating data')
    data_group.add_argument('-n', '--num-points', type=int, default=1000, help='Number of data points to generate (default 1000)')

    # Parse the arguments
    args = parser.parse_args()

    # Prompt for password if --password is specified without a value
    if args.password is None:
        args.password = getpass.getpass(prompt='InfluxDB Password: ')

    return args
