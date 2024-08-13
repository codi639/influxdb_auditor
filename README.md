# Count Rows in InfluxDB - The Ultimate Row Counter Script

Welcome to the **Count Rows in InfluxDB V1** script! 🕵️‍♂️ If you’ve ever wondered how many rows are hiding in your InfluxDB measurements, you’ve come to the right place. This script counts them all and gives you a grand total. It’s like a treasure hunt, but with data!

## Prerequisites

Before diving into the script, make sure you have the following:

- **Python 3** - Because Python 2 is so last decade.
- **InfluxDB Python Client** - To interact with your InfluxDB instance.

### Installing Dependencies

Not sure if the `influxdb` Python package is installed? Check it using:
```bash
pip3 show influxdb
```

If `pip` itself isn't installed, you might be in a bit of a pickle. Just kidding! 😜 You can install `pip3` with:
```bash
apt install -y pip3
```

If you find that the `influxdb` Python package is missing, you can easily install it using `pip`:

```bash
pip3 install influxdb
```

If you really don’t want to use `pip` (why not, though?), you can also install the package via `apt`:

```bash
apt update
apt install -y python3-influxdb
```

Note: `apt install` is like taking the easy way out—you cheater. 😎

## How to Use the Script

Ready to count some rows? Here’s how you can run the script:

1. **Save the Script** - Copy the script into a file named `count_database.py` (or any name with `.py`, it's your computer).
2. **Customize the Arguments** - Take a quick look at the arguments section to ensure it suits your needs (default credentials, etc.).
3. **Make It Executable** - You don’t strictly need this step if you run it with python3, but it’s good practice:

```bash
chmod +x count_database.py
```

4. **Run the Script** - Use the following command to count rows. You can provide arguments or stick with the defaults:

```bash
python3 count_database.py -H YOUR_HOST --P YOUR_PORT -u YOUR_USER -p YOUR_PASS -d YOUR_BASE
```

If you prefer the defaults, just run (it will probably not work without modification):

```bash
python3 count_database.py
```

Default values used:

- Host: 172.16.20.42
- Port: 8086
- Username: user
- Password: password
- Database: supervision

## Script Arguments

- -H, --host - IP address of your InfluxDB server.
- -P, --port - Port number of your InfluxDB server (default: 8086).
- -u, --username - Your InfluxDB username.
- -p, --password - Your InfluxDB password.
- -d, --database - The InfluxDB database name you want to count rows in.

## Example

Here’s an example of how the script works in action:

```bash
root@TIG-Database:~# python3 count_database.py -u hello -p world
Database: supervision, Measurement: cpu_load, Count: 6079612
Database: supervision, Measurement: interfaces, Count: 155335468
Database: supervision, Measurement: ping, Count: 638220
Database: supervision, Measurement: snmp, Count: 648693
Total rows across all measurements in database supervision: 162701993
```

In this example, the script reports the number of rows for each measurement and provides a grand total.

## Important Note

The script can take quite a long time to execute. This is because it performs a COUNT operation on each measurement within the database. Depending on the size of your measurements and the performance of your InfluxDB instance, this can be time-consuming. The script processes each measurement individually and retrieves counts by executing a query for every measurement, which might lead to longer execution times for databases with many measurements or large datasets.

## Troubleshooting

If you encounter any errors:

- 401 Authorization Failed - Double-check your credentials. Even the best spies get caught if they use the wrong password!
- Connection Issues - Ensure your InfluxDB server is up and running. It's hard to count rows if the server is playing hide and seek.

## License

This script is provided as-is. Use it wisely, and remember: with great power (to count rows) comes great responsibility. 🚀

Happy counting!
