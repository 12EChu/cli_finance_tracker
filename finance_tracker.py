import argparse # command line arguments
import os # file operations
import datetime # storing date objects
import csv
import helper.helper_functions as helper_functions

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

    id: simply refers to the row number in the csv file
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
    update_parser.add_argument('value',type=str,help='value that will replace the cell of interest')

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

cols = {'Date':1,'Description':2,'Amount':3,'Type':4}

def write_record(filename,id,date, desc,amount,type):
    '''
    write_record appends the user income/expenses input into a csv file
    '''
    with open(filename,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id,date,desc,amount,type])

def update(filename,id,field,value):
    with open(filename,'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if id <= len(rows)-1 and id> 0:
        rows[id][cols[field]] = value
    
    with open(filename,'w',newline='') as f:
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

def delete(filename,id):
    edited_rows = []
    with open(filename,'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        edited_rows.append(rows[0])
        row_num = 1
        for row in rows[1:]:
            if row[0] != str(id):
                row[0] = row_num
                edited_rows.append(row)
                row_num+=1
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(edited_rows)
        

def main():
    filename = 'finance.csv'
    id = 1
    if not os.path.isfile(filename):
        write_record(filename,'ID','Date','Description','Amount','Type')
    else:
        id = helper_functions.get_last_id(filename) + 1
    parser = make_parser()
    args = parser.parse_args()
    
    if args.mode =='spend':
        write_record(filename,id,args.date,args.desc,-args.amount,'Expense')
    elif args.mode == 'deposit':
        write_record(filename,id,args.date,args.desc,args.amount,'Income')
    elif args.mode == 'update':
        update(filename,args.id,args.field,args.value)
    elif args.mode == 'list':
        list_finance(args.from_date,args.upto)
    elif args.mode == 'delete':
        delete(filename,args.id)
    elif args.mode == 'summary':
        summary(args.from_date,args.upto)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


# python src\finance_tracker.py spend 20 --desc 'Shopping' --date '2024-01-20'
# python src\finance_tracker.py deposit 100 --desc 'Investment' --date '2024-12-25'
# python src\finance_tracker.py update 1 Description 'Changed'
# python src\finance_tracker.py delete 2