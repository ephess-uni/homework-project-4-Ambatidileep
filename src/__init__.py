# tests/test_hp_4.py
import os
import csv
from src.util import get_data_file_path
from src.hp_4 import fees_report

def test_fees_report():
    input_file = get_data_file_path('book_returns_short.csv')
    output_file = 'test_fees_report_out.csv'
    fees_report(input_file, output_file)
    expected_output = [{'late_fees': '15.0', 'patron_id': '17-873-8783'}]
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        for row, expected_row in zip(reader, expected_output):
            assert row == expected_row
    os.remove(output_file)