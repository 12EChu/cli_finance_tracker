import csv
import os
import datetime

def write_to_finance(id,date, desc,amount,type):
    with open('finance.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow([id,date,desc,amount,type])

def get_last_id():
    with open('finance.csv','rb') as f:
        f.seek(-3,os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2,os.SEEK_CUR)
        return int(f.readlines()[0].decode()[0])

def optional_inputs(date,desc):
    if date == '':
        date = datetime.date.today()
    if desc == '':
        desc == 'Unspecified'
    return date,desc