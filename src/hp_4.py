# hp_4.py
import os
import csv
from datetime import datetime


def fees_report(infile, outfile):
    if not os.path.exists(infile):
        raise FileNotFoundError(f"Input file '{infile}' not found.")
    late_fees_dict = {}

    with open(infile, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = days_late * 0.25
            else:
                late_fee = 0.0
            patron_id = row['patron_id']
            if patron_id in late_fees_dict:
                late_fees_dict[patron_id] += late_fee
            else:
                late_fees_dict[patron_id] = late_fee
    with open(outfile, 'w', newline='') as csvfile:
        fieldnames = ['patron_id', 'late_fees']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for patron_id, late_fee in late_fees_dict.items():
            writer.writerow({'patron_id': patron_id, 'late_fees': '{:.2f}'.format(late_fee)})

infile = 'C:\\Users\\ambat\\Documents\\GitHub\\homework-project-4-Ambatidileep\\tests\\fixtures\\book_returns_short.csv'
outfile = 'fees_report_out.csv'
fees_report(infile, outfile)

