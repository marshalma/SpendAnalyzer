#!/usr/local/bin/python3

import csv
import sys

from az_log import log_error, log_info
from datetime import datetime

AMEX_CSV_HEADER = ["Date","Description","Amount","Extended Details","Appears On Your Statement As","Address","City/State","Zip Code","Country","Reference","Category"]
CHASE_CSV_HEADER = ["Transaction Date","Post Date","Description","Category","Type","Amount","Memo"]
CITI_CSV_HEADER = ["Date", "Description", "Debit", "Credit", "Category"]

header_map = {
    "amex": AMEX_CSV_HEADER,
    "chase": CHASE_CSV_HEADER,
    "citi": CITI_CSV_HEADER,
}

key_map = {
    "amex": {"Date":"Date", "Category":"Category", "Merchant":"Description", "Amount":"Amount"},
    "chase": {"Date":"Transaction Date", "Category":"Category", "Merchant":"Description", "Amount":"Amount"},
    "citi": {"Date":"Date", "Category":"Category", "Merchant":"Description", "Amount":"Debit"},
}

date_format_map = {
    "amex": "%m/%d/%Y",
    "chase": "%m/%d/%Y",
    "citi": "%b %d, %Y",
}

sign_map = {
    "amex": lambda x:x,
    "chase": lambda x:-x,
    "citi": lambda x:x
}

STANDARD_DATE_FORMAT="%m/%d/%y"

def fetch_header(row):
    for csv_type, header in header_map.items():
        header_col = row.split(",")

        if len(header_col) != len(header):
            continue

        for i in range(len(header)):
            if header[i].strip() != header_col[i].strip():
                break
        else:
            return csv_type

    return None

class csv_processor:
    def __init__(self, f):
        self.fp = open(f, 'r')
        header_row = self.fp.readline()
        self.reader = csv.reader(self.fp)

        self.csv_type = fetch_header(header_row)
        if self.csv_type is None:
            log_error("Didn't find any matching header for file {}. Abort.".format(f))
            sys.exit(1)

        self.date_col = header_map[self.csv_type].index(key_map[self.csv_type]["Date"])
        self.cate_col = header_map[self.csv_type].index(key_map[self.csv_type]["Category"])
        self.merc_col = header_map[self.csv_type].index(key_map[self.csv_type]["Merchant"])
        self.amount_col = header_map[self.csv_type].index(key_map[self.csv_type]["Amount"])
        
        log_info("CSV file {} is from {}".format(f, self.csv_type))

    def get_rows(self):
        for row in self.reader:
            date = datetime.strptime(row[self.date_col], date_format_map[self.csv_type]).strftime(STANDARD_DATE_FORMAT)
            cate = row[self.cate_col]
            merc = row[self.merc_col]
            amount = sign_map[self.csv_type](float(row[self.amount_col] if len(row[self.amount_col]) > 0 else 0))

            yield date, cate, merc, amount

    def get_standard_header():
        return ["Date", "Category", "Merchant", "Amount"]

    def close(self):
        self.fp.close()


if __name__ == "__main__":
    # Simple test
    csv_obj = csv_processor(sys.argv[1])
    for row in csv_obj.get_rows():
        print(row)
    csv_obj.close()
