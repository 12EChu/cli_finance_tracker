import csv
import os
import datetime

def get_last_id(filename):
    with open(filename,'rb') as f:
        f.seek(-2,os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2,os.SEEK_CUR)
        return int(f.readlines()[0].decode()[0])

def last_five():
    # display the last five records added
    pass