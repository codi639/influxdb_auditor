import requests # type: ignore
from faker import Faker # type: ignore
import random
import time
from args_module import parse_args
from spinner_module import start_spinner, stop_spinner

def generate_lorem_data():
    """Generate a single line of Lorem Ipsum data in InfluxDB line protocol format."""
    fake = Faker()
    measurement = "lorem_ipsum"
    tags = {
        "source": fake.company().replace(' ', '_').replace(',', '_').replace('\'', '_'),
        "category": fake.word().replace(' ', '_').replace(',', '_').replace('\'', '_')
    }
    # Generate text and ensure it's properly quoted and sanitized
    text = fake.text(max_nb_chars=100).replace('\n', ' ').replace('\r', ' ').replace('\\', '\\\\').replace('"', '\\"')
    fields = {
        "text": f'"{text}"',  # String fields must be enclosed in double quotes
        "number": random.randint(1, 100)
    }
    timestamp = int(time.time() * 1e9)  # Convert current time to nanoseconds

    tags_str = ','.join(f'{key}={value}' for key, value in tags.items() if value)  # Filter out empty tag values
    fields_str = ','.join(f'{key}={value}' for key, value in fields.items())

    # Ensure that both tags and fields are not empty
    if tags_str and fields_str:
        return f"{measurement},{tags_str} {fields_str} {timestamp}"
    else:
        # Return an empty string or handle the case where the data cannot be generated
        return ""


def write_lorem_data(host, port, database, num_points):
    """Write a number of Lorem Ipsum data points to InfluxDB."""
    url = f"http://{host}:{port}/write?db={database}"
    headers = {'Content-Type': 'text/plain'}
    points = [generate_lorem_data() for _ in range(num_points)]
    data = '\n'.join(points)

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 204:
        print(f"\nSuccessfully inserted {num_points} Lorem Ipsum data points.")
    else:
        print(f"\nFailed to insert data points: {response.content}")

def main():
    # Parse command-line arguments
    args = parse_args()

    # Start spinner
    stop_event, spinner_thread = start_spinner("Generating and inserting data")

    try:
        # Write data points to InfluxDB
        write_lorem_data(args.host, args.port, args.database, args.num_points)
    finally:
        # Stop spinner
        stop_spinner(stop_event, spinner_thread)

if __name__ == "__main__":
    main()