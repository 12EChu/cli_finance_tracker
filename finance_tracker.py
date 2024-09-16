import argparse # command line arguments
import os # file operations
import datetime # storing date objects
import csv
from helpers.helper_functions import *

def make_parser():
    '''
    Defines the Command Line Finance tracking arguments

    spend [amount] [--desc] [--date]
    deposit [amount] [--desc] [--date]
    update [id] [field] [value]
    list [--from date/month/year] [--to date/month/year]
    summary [--from date/month/year] [--to date/month/year]
    delete [id]
    #budget [amount]

    '''
    parser = argparse.ArgumentParser(description='CLI Finance Tracker')
    parser.set_defaults()
    subparser = parser.add_subparsers(dest='mode')
    
    spend_parser = subparser.add_parser('spend')
    spend_parser.add_argument('amount',type=float,help='expense amount')
    spend_parser.add_argument('--desc',default='Unspecified',type=str,help='description of expense origin')
    spend_parser.add_argument('--date',default= str(datetime.date.today()),type=str,help='date of spending') #check what type should be inputted

    deposit_parser = subparser.add_parser('deposit')
    deposit_parser.add_argument('amount',type=float,help='deposit amount')
    deposit_parser.add_argument('--desc',default='Unspecified',type=str,help='description of income origin')
    deposit_parser.add_argument('--date',default= str(datetime.date.today()),type=str,help='date of deposit')

    update_parser = subparser.add_parser('update')
    update_parser.add_argument('id',type=int,help='finance record id')
    update_parser.add_argument('field',type=str,help='name of the field to change')
    update_parser.add_argument('value',help='value that will replace the cell of interest')

    list_parser = subparser.add_parser('list')
    list_parser.add_argument('--from_date',type=str,help='finance records dated after specified date')
    list_parser.add_argument('--upto',type=str,help='finance records dated before specified date')

    summary_parser = subparser.add_parser('summary')
    summary_parser.add_argument('--from_date',type=str,help='report on finance dated after specified date')
    summary_parser.add_argument('--upto',type=str,help='report on finance dated before specified date')

    delete_parser = subparser.add_parser('delete')
    delete_parser.add_argument('id',type=int,help='finance record id to remove')

    # ignore budget for now
    # budget_parser = subparser.add_parser('budget')
    # budget_parser.add_argument('id',type=float,help='set your monthly budget')

    return parser

cols = {'ID':0,'Date':1,'Description':2,'Amount':3,'Type':4}

def spend(id,date,desc,amount):
    '''
    Spend appends the user expenses input into the finance.csv
    it first checks for the optional date and description inputs and assigns a default values to them if there are no inputs detected.
    '''
    write_to_finance(id,date,desc,-amount,'Expense')

def deposit(id,date,desc, amount):
    write_to_finance(id,date,desc,amount,'Income')

def update(id,field,value):
    # read csv
    # need to check whether i need to rewrite the whole file
    with open('finance.csv','r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if id <= len(rows)-1 and id>= 0:
        rows[id+1][cols[field]] = value
    
    with open('finance.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def list_finance(*args):
    # assume date is in right format
    # read file, filter for dates 
    # print the dates may need a print function
    pass

def summary(*args):
    # read vals
    # return the amount spent, income, budget
    pass

def delete(id):
    pass

def main():
    id = 0
    if not os.path.isfile('finance.csv'):
        write_to_finance('ID','Date','Description','Amount','Type')
    else:
        id = get_last_id() + 1
    parser = make_parser()
    args = parser.parse_args()
    
    if args.mode =='spend':
        spend(id,args.date,args.desc,args.amount)
    elif args.mode == 'deposit':
        deposit(id,args.date,args.desc,args.amount)
    elif args.mode == 'update':
        update(args.id,args.field,args.value)
    elif args.mode == 'list':
        list_finance(args.from_date,args.upto)
    elif args.mode == 'delete':
        delete(args.id)
    elif args.mode == 'summary':
        summary(args.from_date,args.upto)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
    

