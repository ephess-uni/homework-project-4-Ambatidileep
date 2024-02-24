# hp_4.py
import csv
from datetime import datetime

def fees_report(infile, outfile):
    try:
        with open(infile, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fees = {}
            for row in reader:
                if 'date_due' not in row:
                    print("Warning: Column 'date_due' not found in the input file.")
                    continue
                date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
                date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
                if date_returned > date_due:
                    days_late = (date_returned - date_due).days
                    patron_id = row['patron_id']
                    late_fee = days_late * 0.25
                    if patron_id in fees:
                        fees[patron_id] += late_fee
                    else:
                        fees[patron_id] = late_fee

        with open(outfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['patron_id', 'late_fees'])
            for patron_id, late_fee in fees.items():
                writer.writerow([patron_id, late_fee])
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{infile}' not found.")

infile = 'C:/Users/ambat/Documents/GitHub/homework-project-4-Ambatidileep/src/book_fees.csv'
outfile = 'C:/Users/ambat/Documents/GitHub/homework-project-4-Ambatidileep/src/fees_report_out.csv'

fees_report(infile, outfile)
