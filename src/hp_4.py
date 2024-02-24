# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict
import os

def reformat_dates(old_dates):
    new_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = date_obj.strftime('%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates

def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start should be a string")
    if not isinstance(n, int):
        raise TypeError("n should be an integer")

    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]

def add_date_range(values, start_date):
    date_list = date_range(start_date, len(values))
    return list(zip(date_list, values))

def fees_report(infile, outfile):
    late_fees = defaultdict(float)

    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')  # Corrected format here
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
                late_fees[row['patron_id']] += late_fee

    with open(outfile, 'w', newline='') as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': "{:.2f}".format(fee)})
def get_data_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    return os.path.join(data_dir, filename)

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
