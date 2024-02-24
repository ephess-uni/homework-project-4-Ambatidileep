# hp_4.py
from datetime import datetime
from csv import DictReader, DictWriter
from collections import defaultdict
import os

def fees_report(infile, outfile):
    late_fees = defaultdict(float)

    with open(infile, 'r') as file:
        reader = DictReader(file)
        for row in reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
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
