import csv
import os
import datetime
from collections import deque
from tabulate import tabulate

def get_last_id(filename):
    with open(filename,'rb') as f:
        f.seek(-2,os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2,os.SEEK_CUR)
        return int(f.readlines()[0].decode()[0])

def last_five(filename):
    with open(filename,'r') as f:
        q = deque(f,5)
        reader = csv.reader(q)
        rows = list(reader)
        headers = ['ID','Date','Description','Amount','Type']
        if rows[0] != headers:
            rows.insert(0,headers)
        print('The last five records added: ')
        print(tabulate(rows,headers='firstrow',tablefmt='fancy_grid'))

def filter_records(filename,fdate,tdate):
    from_date = datetime.date.fromisoformat(fdate)
    to_date = datetime.date.fromisoformat(tdate)

    with open(filename,'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if from_date < to_date:
            filtered_rows = [['ID','Date','Description','Amount','Type']]
            for row in rows[1:]:
                curr_date = datetime.date.fromisoformat(row[1])
                if curr_date >= from_date and curr_date <= to_date:
                    filtered_rows.append(row)
    return rows if from_date >= to_date else filtered_rows