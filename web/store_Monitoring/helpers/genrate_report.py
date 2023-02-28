import csv
import pytz
from datetime import datetime, timedelta
from db import db
from flask import current_app

def generate_report(report_id):
    # Get current timestamp as the max timestamp among all the observations in the first CSV
    max_timestamp = get_max_timestamp()

    # Load data from CSVs into memory
    active_stores = load_active_stores()
    business_hours = load_business_hours()
    timezones = load_timezones()

    # Compute report data for each store
    report_data = []
    for store_id in active_stores:
        timezone_str = timezones.get(store_id, 'America/Chicago')
        timezone = pytz.timezone(timezone_str)

        # Get business hours for the store
        hours = business_hours.get(store_id)
        if not hours:
            # If data is missing for a store, assume it is open 24*7
            hours = [(0, 24)]

        # Compute the time intervals for the report
        report_intervals = compute_report_intervals(max_timestamp, hours, timezone)

        # Compute uptime and downtime for each interval
        for interval in report_intervals:
            interval_uptime, interval_downtime = compute_uptime_downtime(store_id, interval, timezone, active_stores)
            report_data.append((store_id, interval_uptime, interval_downtime))

    # Write report data to a CSV file
    headers = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']
    filename = f'report_{report_id}.csv'
    with open(filename, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in report_data:
            writer.writerow(row)

    # Update report status in the database
    with current_app.app_context():
        db.execute('UPDATE reports SET status = %s WHERE id = %s', ('Complete', report_id))
        db.commit()

def get_max_timestamp():
    with current_app.app_context():
        result = db.execute('SELECT MAX(timestamp_utc) FROM active_stores')
        return result.fetchone()[0]

def load_active_stores():
    with current_app.app_context():
        result = db.execute('SELECT DISTINCT store_id FROM active_stores')
        return [row[0] for row in result.fetchall()]

def load_business_hours():
    with current_app.app_context():
        result = db.execute('SELECT store_id, day_of_week, start_time_local, end_time_local FROM business_hours')
        business_hours = {}
        for row in result.fetchall():
            store_id, day_of_week, start_time_local, end_time_local = row
            if store_id not in business_hours:
                business_hours[store_id] = {}
            business_hours[store_id][day_of_week] = (start_time_local, end_time_local)
        return business_hours

def load_timezones():
    with current_app.app_context():
        result = db.execute('SELECT store_id, timezone_str FROM timezones')
        return {row[0]: row[1] for row in result.fetchall()}


def compute_report_intervals(store_hours, timestamps, timezone_str):
    timezone = pytz.timezone(timezone_str)
    intervals = []
    for store_id, hours in store_hours.items():
        tz_hours = [(datetime.strptime(s, '%H:%M:%S').time(),
                     datetime.strptime(e, '%H:%M:%S').time())
                    for d, s, e in hours]
        tz_hours.sort()

        for ts in timestamps:
            dt = datetime.fromisoformat(ts).replace(tzinfo=pytz.utc).astimezone(timezone)
            dt_local = dt.time()

            dow = dt.weekday()
            open_interval = None
            for start, end in tz_hours[dow:dow+1]:
                if dt_local >= start:
                    open_interval = (dt.replace(hour=start.hour, minute=start.minute, second=start.second, microsecond=0),
                                      dt.replace(hour=end.hour, minute=end.minute, second=end.second, microsecond=0))
                    break

            if open_interval:
                intervals.append(open_interval)
    return intervals