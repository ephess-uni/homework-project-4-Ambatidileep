# hp_4.py
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    reformatted_dates = []
    for date_str in old_dates:
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
        reformatted_date = datetime_obj.strftime('%d %b %Y')
        reformatted_dates.append(reformatted_date)
    return reformatted_dates

def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start must be a string")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]

def add_date_range(values, start_date):
    if not isinstance(start_date, str):
        raise TypeError("start_date must be a string")
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    return [(start_datetime + timedelta(days=i), value) for i, value in enumerate(values)]

def fees_report(infile, outfile):
    try:
        with open(infile, 'r', newline='') as csvfile:
            reader = DictReader(csvfile)
            fees = defaultdict(float)
            for row in reader:
                date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
                try:
                    date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
                except ValueError:
                    date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
                if date_returned > date_due:
                    days_late = (date_returned - date_due).days
                    patron_id = row['patron_id']
                    late_fee = days_late * 0.25
                    fees[patron_id] += late_fee

        with open(outfile, 'w', newline='') as csvfile:
            writer = DictWriter(csvfile, fieldnames=['patron_id', 'late_fees'])
            writer.writeheader()
            for patron_id, late_fee in fees.items():
                writer.writerow({'patron_id': patron_id, 'late_fees': round(late_fee, 2)})
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{infile}' not found.")

if __name__ == '__main__':
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)
    with open(OUTFILE) as f:
        print(f.read())
