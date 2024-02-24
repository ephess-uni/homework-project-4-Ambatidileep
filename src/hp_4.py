# hp_4.py

from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    new_dates = []
    for date_str in old_dates:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        new_dates.append(dt.strftime('%d %b %Y'))
    return new_dates


def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start should be a string")
    if not isinstance(n, int):
        raise TypeError("n should be an integer")
    start_date = datetime.strptime(start, '%Y-%m-%d')
    return [start_date + timedelta(days=i) for i in range(n)]


def add_date_range(values, start_date):
    dates = date_range(start_date, len(values))
    return list(zip(dates, values))


def fees_report(infile, outfile):
    pass

import pytest
from src.hp_4 import reformat_dates, date_range, add_date_range, fees_report


def test_reformat_dates():
    old_dates = ['2000-01-01', '2000-01-02', '2000-01-03']
    expected_dates = ['01 Jan 2000', '02 Jan 2000', '03 Jan 2000']
    assert reformat_dates(old_dates) == expected_dates


def test_date_range():
    start = '2000-01-01'
    n = 3
    expected_dates = [
        datetime(2000, 1, 1),
        datetime(2000, 1, 2),
        datetime(2000, 1, 3)
    ]
    assert date_range(start, n) == expected_dates


def test_add_date_range():
    values = [100, 101, 102]
    start_date = '2000-01-01'
    expected_result = [
        (datetime(2000, 1, 1), 100),
        (datetime(2000, 1, 2), 101),
        (datetime(2000, 1, 3), 102)
    ]
    assert add_date_range(values, start_date) == expected_result


def test_fees_report():
    pass
