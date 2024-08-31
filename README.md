# InfluxDB Auditor - The Ultimate Auditor Tool

Welcome to the **InfluxDB V1 Auditor**! 🕵️‍♂️ Whether you’re on a quest to count rows, create databases and users, or fill them with dummy data, this tool’s got your back. Think of it as your trusty sidekick in the wild world of data adventures!

## Prerequisites

Before diving in, make sure you have the following:

- **Python 3** - Because Python 2 is so last decade.
- **InfluxDB Python Client** - To interact with your InfluxDB instance.
- **Faker** - To generate dummy data.

### Installing Dependencies

To check if the `influxdb` Python package is installed, use:
```bash
pip3 show influxdb
```

If pip itself isn't installed, you can install it with:
```bash
apt install -y python3-pip
```

To install the influxdb Python package, use pip:
```bash
pip3 install influxdb
```

If you prefer to use apt, you can install it with:
```bash
apt update
apt install -y python3-influxdb
```

For Faker, install it with:
```bash
pip3 install faker
```

Or, in case iut don't work (which was my case...):
```bash
apt update
apt install -y python3-fake-factory
```

Note: Depending on your Linux distribution, the package names may vary. Ensure you have the appropriate packages installed for Faker.

## Script Overview

### 1. Count Rows Script

**Filename: `count_rows.py`**

This script counts the number of rows in each measurement of your InfluxDB database and provides a total count.

**Usage:**

```bash
Connection Arguments:
  Arguments for connecting to InfluxDB

  -H HOST, --host HOST  InfluxDB host IP address
  -P PORT, --port PORT  InfluxDB port number (default 8086)
  -u USERNAME, --username USERNAME
                        InfluxDB username
  -p [PASSWORD], --password [PASSWORD]
                        InfluxDB password (will prompt if not provided)
  -d DATABASE, --database DATABASE
                        InfluxDB database name

Information Arguments:
  Arguments for displaying additional information

  --more-info           Display additional information about measurements
```

**Let the script run.** - ☕️ Take a Coffee Break

Relax while the script crunches the numbers like a caffeinated data wizard.

**Example:**

```bash
root@TIG-Database:~# python3 count_rows.py -u hello -p world
Database: supervision, Measurement: cpu_load, Count: 6197318
Database: supervision, Measurement: interfaces, Count: 214209058
Database: supervision, Measurement: ping, Count: 653752
Database: supervision, Measurement: snmp, Count: 662102
Total rows across all measurements in database supervision: 221722230
```

### 2. Build Database and User Script

**Filename: `build_basic.py`**

This script allows you to create a new database and user in your InfluxDB instance.

**Usage:**

```bash
Connection Arguments:
  Arguments for connecting to InfluxDB

  -H HOST, --host HOST  InfluxDB host IP address
  -P PORT, --port PORT  InfluxDB port number (default 8086)
  -u USERNAME, --username USERNAME
                        InfluxDB username
  -p [PASSWORD], --password [PASSWORD]
                        InfluxDB password (will prompt if not provided)
  -d DATABASE, --database DATABASE
                        InfluxDB database name

Database and User Creation:
  Arguments for creating databases and users

  -dc [DATABASE_CREATION], --database-creation [DATABASE_CREATION]
                        Create a new database with the specified name.
  -uc [USER_CREATION], --user-creation [USER_CREATION]
                        Create a new user with the specified username.
  -pc [PASSWORD_CREATION], --password-creation [PASSWORD_CREATION]
                        Password for the new user.
  -per [{read,write,all}], --permissions [{read,write,all}]
                        Permissions for the new user. Choose from: read, write, all.

```

Note: There's an interactive mode if no value are provided for the databse name, username, password and permissions.

**Example:**

```bash
python3 build_basic.py -u admin -p -H localhost -dc -uc -per all
InfluxDB Password:
Enter database name: test6
Creating database 'test6'...
Database 'test6' created successfully.
Enter username: test6
Enter password for the new user:
Creating user 'test6' with all permissions...
User 'test6' created successfully.
```

### 3. Fill Database Script
**Filename: `fill_lorem.py`**

This script populates the specified database with dummy data using Faker. It create a measurement `Lorem_ipsum`, if it already exist just fill it.

**Usage:**
```bash
Connection Arguments:
  Arguments for connecting to InfluxDB

  -H HOST, --host HOST  InfluxDB host IP address
  -P PORT, --port PORT  InfluxDB port number (default 8086)
  -u USERNAME, --username USERNAME
                        InfluxDB username
  -p [PASSWORD], --password [PASSWORD]
                        InfluxDB password (will prompt if not provided)
  -d DATABASE, --database DATABASE
                        InfluxDB database name

Data Generation:
  Arguments for generating data

  -n NUM_POINTS, --num-points NUM_POINTS
                        Number of data points to generate (default 1000)
```

**Example:**
```bash
python3 fill_lorem.py -u admin -p -H localhost -d test6 -n 10000
InfluxDB Password:
Generating and inserting data... /
Successfully inserted 10000 Lorem Ipsum data points.
```

## Important Note

These scripts might take a bit of time to run, especially with large datasets or lots of records. Be patient—good things come to those who wait!

## Troubleshooting

If you encounter any issues:

- 401 Authorization Failed - Double-check your credentials. Even the best spies get caught if they use the wrong password!
- Connection Issues - Ensure your InfluxDB server is running and accessible. It's hard to count rows if the server is playing hide and seek.

## License
This toolset is provided as-is. Use it responsibly, and remember: with great power (to manage databases) comes great responsibility. 🚀

Happy auditing!

## **TODO**

- Automate backups ❌
- Check latest base connection with timerange ❌
- Automatically remove data given a timerange ❌
