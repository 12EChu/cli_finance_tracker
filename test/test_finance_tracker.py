import os
import csv
import unittest
from src import finance_tracker

class TestFinance_Tracker(unittest.TestCase):
    def test_write_record(self):
        finance_tracker.write_record('test.csv',1,'2024-11-13','Shopping',100,'Expense')
        with open('test.csv','r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            expected = ['1','2024-11-13','Shopping','100','Expense']
            self.assertEqual(expected,rows[0])
        os.remove('test.csv')

if __name__ == '__main__':
    unittest.main()
