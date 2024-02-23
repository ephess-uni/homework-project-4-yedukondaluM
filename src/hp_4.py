# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return [datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y") for d in old_dates]


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError
    elif not isinstance(n, int):
        raise TypeError
    else:
        return [datetime.strptime(start, "%Y-%m-%d") + timedelta(days=y) for y in range(0, n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    list1 = []
    temp = 0
    for value in values:
        time = []
        time.append(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=temp))
        time.append(value)
        list1.append(tuple(time))
        temp += 1
    return list1


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        length = []
        obj = DictReader(f)
        for i in obj:
            sample_dict = {}
            day1 = datetime.strptime(i['date_returned'], '%m/%d/%Y') - datetime.strptime(i['date_due'],
                                                                                         '%m/%d/%Y')
            if (day1.days > 0):
                sample_dict["patron_id"] = i['patron_id']
                sample_dict["late_fees"] = round(day1.days * 0.25, 2)
                length.append(sample_dict)
            else:
                sample_dict["patron_id"] = i['patron_id']
                sample_dict["late_fees"] = float(0)
                length.append(sample_dict)
        aggregated_data = {}

        for d in length:
            aggregated_data[d['patron_id']] = aggregated_data.get(d['patron_id'], 0) + d['late_fees']

        r = [{'patron_id': key, 'late_fees': value} for key, value in aggregated_data.items()]
        for d in r:
            for key, value in d.items():
                if key == "late_fees":
                    if len(str(value).split('.')[-1]) != 2:
                        d[key] = str(value) + '0'

    with open(outfile, "w", newline="") as file:
        column = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=column)
        writer.writeheader()
        writer.writerows(r)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':

    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())