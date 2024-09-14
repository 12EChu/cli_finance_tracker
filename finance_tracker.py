import argparse # command line arguments
import os # file operations
import datetime # storing date objects

def make_parser():
    '''
    Defines the Command Line Finance tracking arguments

    spend [amount] [--desc] [--date]
    deposit [amount] [--desc] [--date]
    update [id] [field] [value]
    list [--from date/month/year] [--to date/month/year]
    summary [--from date/month/year] [--to date/month/year]
    delete [id]
    budget [amount]

    '''
    parser = argparse.ArgumentParser(description='CLI Finance Tracker')
    subparser = parser.add_subparsers()
    
    spend_parser = subparser.add_parser('spend')
    spend_parser.add_argument('amount',type=float,help='expense amount')
    spend_parser.add_argument('--desc',type=str,help='description of expense origin')
    spend_parser.add_argument('--date',type=str,help='date of spending') #check what type should be inputted

    deposit_parser = subparser.add_parser('deposit')
    deposit_parser.add_argument('amount',type=float,help='deposit amount')
    deposit_parser.add_argument('--desc',type=str,help='description of income origin')
    deposit_parser.add_argument('--date',type=str,help='date of deposit')

    update_parser = subparser.add_parser('update')
    update_parser.add_argument('id',type=int,help='finance record id')
    update_parser.add_argument('field',type=str,help='name of the field to change')
    update_parser.add_argument('value',help='value that will replace the cell of interest')

    list_parser = subparser.add_parser('list')
    list_parser.add_argument('--from',type=str,help='finance records dated after specified date')
    list_parser.add_argument('--upto',type=str,help='finance records dated before specified date')

    summary_parser = subparser.add_parser('summary')
    summary_parser.add_argument('--from',type=str,help='report on finance dated after specified date')
    summary_parser.add_argument('--upto',type=str,help='report on finance dated before specified date')

    delete_parser = subparser.add_parser('delete')
    delete_parser.add_argument('id',type=int,help='finance record id to remove')

    budget_parser = subparser.add_parser('budget')
    budget_parser.add_argument('id',type=float,help='set your monthly budget')

    return parser

parser = make_parser()
args = parser.parse_args()
print(args)
    

