import argparse # command line arguments
import os # file operations
import datetime # storing date objects
import csv
import src.helper_functions as helper_functions
from tabulate import tabulate

def make_parser():
    """
    Creates and returns an argument parser for the CLI Finance Tracker application.

    This function configures an argparse.ArgumentParser for various CLI commands related
    to finance management, including spending, depositing, updating records, listing transactions,
    summarizing reports, and deleting records. Each command has its own subparser with specific
    arguments.

    The following commands are supported:
    
    - `spend`: Logs a spending transaction with an amount, optional description, and optional date.
    - `deposit`: Logs a deposit transaction with an amount, optional description, and optional date.
    - `update`: Updates a specified field (e.g., amount, description, date) of a finance record by its ID.
    - `list`: Lists all finance records within a specified date range.
    - `summary`: Provides a summary of finance transactions within a date range.
    - `delete`: Deletes a finance record by its ID.

    Returns:
        argparse.ArgumentParser: The configured argument parser for handling CLI commands.

    Command Arguments:
        - **spend**:
            - `amount` (float): The amount spent.
            - `--desc` (str, optional): A description of the spending. Default is 'Unspecified'.
            - `--date` (str, optional): The date of the spending. Default is today's date (YYYY-MM-DD).

        - **deposit**:
            - `amount` (float): The deposit amount.
            - `--desc` (str, optional): A description of the deposit. Default is 'Unspecified'.
            - `--date` (str, optional): The date of the deposit. Default is today's date (YYYY-MM-DD).

        - **update**:
            - `id` (int): The unique ID of the finance record to update.
            - `field` (str): The field to update (e.g., 'amount', 'desc', 'date').
            - `value` (str): The new value to replace the existing field content.

        - **list**:
            - `--from_date` (str, optional): List records after this date. Default is today's date.
            - `--to_date` (str, optional): List records before this date. Default is today's date.

        - **summary**:
            - `--from_date` (str, optional): Summarize transactions after this date. Default is today's date.
            - `--to_date` (str, optional): Summarize transactions before this date. Default is today's date.

        - **delete**:
            - `id` (int): The unique ID of the finance record to delete.

    Examples:
        >>> parser = make_parser()
        >>> args = parser.parse_args(['spend', '100', '--desc', 'groceries'])
        # Parses a spend command with amount 100 and description "groceries".

        >>> args = parser.parse_args(['list', '--from_date', '2023-01-01', '--to_date', '2023-12-31'])
        # Parses a list command for transactions within the date range.

    """
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
    list_parser.add_argument('--from_date',default= str(datetime.date.today()),type=str,help='finance records dated after specified date')
    list_parser.add_argument('--to_date',default= str(datetime.date.today()),type=str,help='finance records dated before specified date')

    summary_parser = subparser.add_parser('summary')
    summary_parser.add_argument('--from_date',default= str(datetime.date.today()),type=str,help='report on finance dated after specified date')
    summary_parser.add_argument('--to_date',default= str(datetime.date.today()),type=str,help='report on finance dated before specified date')

    delete_parser = subparser.add_parser('delete')
    delete_parser.add_argument('id',type=int,help='finance record id to remove')

    return parser

cols = {'Date':1,'Description':2,'Amount':3,'Type':4}

def write_record(filename,id,date, desc,amount,type,display=True):
    """
    Appends a financial record (income/expense) to a CSV file.

    This function appends a new record containing information about a user's income or expense
    to the specified CSV file. Each record includes an ID, date, description, amount, and transaction type (income/expense).
    If the `display` argument is `True`, the function will also display the last five records in the CSV file.

    Args:
        filename (str): The name of the CSV file to write the record to.
        id (int): A unique identifier for the financial record.
        date (str): The date of the transaction in ISO format (YYYY-MM-DD).
        desc (str): A description of the transaction (e.g., "groceries", "salary").
        amount (float): The monetary value of the transaction.
        type (str): The type of transaction ('income' or 'expense').
        display (bool, optional): If `True`, displays the last five records in the CSV file after appending. Default is `True`.

    Returns:
        None

    Side Effects:
        - Appends a new row to the specified CSV file.
        - Optionally displays the last five records using the `helper_functions.last_five()` method.

    Example:
        >>> write_record('finance_records.csv', 1, '2023-09-14', 'groceries', 50.00, 'expense')
        # This will append the record to 'finance_records.csv' and display the last five records.

    """
    with open(filename,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id,date,desc,amount,type])
    if display:
        helper_functions.last_five(filename)

def update(filename,id,field,value):
    """
    Updates a specific field of a record in a CSV file.

    This function reads a CSV file, updates a specific field (column) of a record (row) 
    identified by the `id`, and writes the updated rows back to the file. The `id` 
    corresponds to the row number in the CSV file, and the `field` is the name of the 
    column to update.

    Args:
        filename (str): The name of the CSV file to update.
        id (int): The unique identifier for the record (row number) to be updated. 
                  Must be greater than 0 and less than the total number of rows.
        field (str): The name of the field (column) to update. Must match one of the 
                     column headers.
        value (str): The new value to insert in the specified field.

    Raises:
        ValueError: If the `id` is out of bounds or if the specified `field` does not exist.

    Returns:
        None

    Example:
        >>> update('finance_records.csv', 1, 'amount', '75.00')
        # Updates the 'amount' field of the first record (ID 1) to '75.00' in 'finance_records.csv'.
    """
    with open(filename,'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

        if len(rows) == 0:
            raise ValueError("The CSV file is empty.")
        if field not in cols:
            raise ValueError(f'The field {field} is not an available column!')
        if id<1 and id>=len(rows):
            raise ValueError(f'Invalid ID. ID must be in range 1 to {len(rows)-1}')
        rows[id][cols[field]] = value
    
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def list_finance(filename,fdate,tdate):
    """
    Displays finance records within a date range from a CSV file.

    This function filters and displays finance records from the specified CSV file 
    based on a date range provided by `fdate` (from date) and `tdate` (to date). 
    The finance records are sorted by the date in ascending order before being displayed.

    Args:
        filename (str): The name of the CSV file containing finance records.
        fdate (str): The start date (YYYY-MM-DD) for filtering records (inclusive).
        tdate (str): The end date (YYYY-MM-DD) for filtering records (inclusive).

    Returns:
        None

    Side Effects:
        - Displays the whole list of csv records when no dates are provided.
        - Displays a table of filtered finance records, sorted by date, using the `tabulate` library.
        - Calls the `helper_functions.filter_records()` to filter records based on the date range.

    Example:
        >>> list_finance('finance_records.csv', '2023-01-01', '2023-12-31')
        # Displays all finance records between January 1, 2023, and December 31, 2023.

    """
    filtered_rows = helper_functions.filter_records(filename,fdate,tdate)
    if len(filtered_rows) > 2:
        sorted_rows = sorted(filtered_rows[1:],key= lambda row: datetime.date.fromisoformat(row[1])) 
    elif len(filtered_rows) == 2:
        sorted_rows = filtered_rows[1]
    else:
        sorted_rows = []
    print(tabulate(sorted_rows,headers=['ID','Date','Description','Amount','Type'],tablefmt='fancy_grid'))

def summary(filename,fdate,tdate):
    """
    Calculates and displays a financial summary (income, expense, and savings) for a given date range.

    This function reads a CSV file, filters finance records based on the specified date range, 
    and calculates total income, total expenses, and savings. The summary is printed to the console.

    Args:
        filename (str): The name of the CSV file containing finance records.
        fdate (str): The start date (YYYY-MM-DD) for filtering records (inclusive).
        tdate (str): The end date (YYYY-MM-DD) for filtering records (inclusive).

    Returns:
        None

    Side Effects:
        - Prints the financial summary to the console, including total income, total expenses, and savings.
        - Calls the `helper_functions.filter_records()` to filter records by the date range.

    Example:
        >>> summary('finance_records.csv', '2023-01-01', '2023-12-31')
        # Displays the total income, total expenses, and savings for the year 2023.

    """
    filtered_rows = helper_functions.filter_records(filename,fdate,tdate)
    expense = 0
    income = 0
    for row in filtered_rows[1:]:
        try:
            value = float(row[3])
            if value < 0:
                expense += abs(value)
            else:
                income += value
        except:
            print('skipping row due to invalid amount')
    savings = income-expense
    print(f'Savings: {savings}')
    print(f'Income: {income}')
    print(f'Expense: {expense}')
    

def delete(filename,id):
    """
    Deletes a record from the CSV file based on the specified ID.

    This function removes a record from a CSV file based on its unique ID, 
    then reorders the remaining records and updates their IDs sequentially.

    Args:
        filename (str): The name of the CSV file containing finance records.
        id (int): The unique ID of the record to be deleted.

    Returns:
        None

    Side Effects:
        - Writes the updated rows back to the CSV file, excluding the deleted record.
        - Reorders the remaining records and adjusts their IDs.

    Raises:
        ValueError: If the record with the specified ID does not exist.

    Example:
        >>> delete('finance_records.csv', 2)
        # Deletes the record with ID 2 from 'finance_records.csv' and updates the IDs of the remaining records.
    """
    edited_rows = []
    record_found = False
    with open(filename,'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) <= 1:
            raise ValueError('No records found in the file.')
        edited_rows.append(rows[0])
        row_num = 1
        for row in rows[1:]:
            if row[0] != str(id):
                row[0] = row_num
                edited_rows.append(row)
                row_num+=1
            else:
                record_found= True
    if not record_found:
        raise ValueError(f'Record with {id} not found.')
            
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(edited_rows)
        

def main():
    """
    Main entry point for the CLI finance tracker.
    
    - Ensures the finance CSV file exists.
    - Parses command-line arguments to perform various actions (e.g., spend, deposit, update, list, delete, summary).
    """
    filename = 'finance.csv'
    id = 1
    if not os.path.isfile(filename):
        write_record(filename,'ID','Date','Description','Amount','Type',display=False)
    else:
        id = helper_functions.get_last_id(filename) + 1
    parser = make_parser()
    args = parser.parse_args()
    
    try:
        if args.mode =='spend':
            write_record(filename,id,args.date,args.desc,args.amount,'Expense')
        elif args.mode == 'deposit':
            write_record(filename,id,args.date,args.desc,args.amount,'Income')
        elif args.mode == 'update':
            update(filename,args.id,args.field,args.value)
        elif args.mode == 'list':
            list_finance(filename,args.from_date,args.to_date)
        elif args.mode == 'delete':
            delete(filename,args.id)
        elif args.mode == 'summary':
            summary(filename,args.from_date,args.to_date)
        else:
            parser.print_help()
    except Exception as e:
        print(f"An unexpected error occured: {e}")

if __name__ == "__main__":
    main()
