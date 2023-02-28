import csv
import psycopg2

# Database credentials
db_host = "localhost"
db_port = "5432"
db_name = "mydatabase"
db_user = "myusername"
db_password = "mypassword"

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# Open CSV files and read data
with open('store_status.csv', 'r') as f:
    store_status_data = list(csv.reader(f))[1:]  # skip header row

with open('store_hours.csv', 'r') as f:
    store_hours_data = list(csv.reader(f))[1:]  # skip header row

with open('store_timezone.csv', 'r') as f:
    store_timezone_data = list(csv.reader(f))[1:]  # skip header row

# Insert data into the database
with conn.cursor() as cur:
    # Create table for store_status data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS store_status (
            store_id INTEGER,
            timestamp_utc TIMESTAMP,
            status TEXT
        )
    """)
    # Insert store_status data
    cur.executemany("""
        INSERT INTO store_status (store_id, timestamp_utc, status)
        VALUES (%s, %s, %s)
    """, store_status_data)

    # Create table for store_hours data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS store_hours (
            store_id INTEGER,
            day_of_week INTEGER,
            start_time_local TIME,
            end_time_local TIME
        )
    """)
    # Insert store_hours data
    cur.executemany("""
        INSERT INTO store_hours (store_id, day_of_week, start_time_local, end_time_local)
        VALUES (%s, %s, %s, %s)
    """, store_hours_data)

    # Create table for store_timezone data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS store_timezone (
            store_id INTEGER,
            timezone_str TEXT
        )
    """)
    # Insert store_timezone data
    cur.executemany("""
        INSERT INTO store_timezone (store_id, timezone_str)
        VALUES (%s, %s)
    """, store_timezone_data)

conn.commit()
conn.close()