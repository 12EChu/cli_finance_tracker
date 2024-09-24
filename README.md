# cli_finance_tracker
Track income and expenses via command line


# Prerequisites
Before installing the CLI app, you need to have Python installed. If you don't have Python installed, follow these steps:

Download and install Python from the official [Python website](https://www.python.org/downloads/ "Python Download").
Make sure to check the box "Add Python to PATH" during the installation.

# Getting Started
Clone the Repository

```
git clone https://github.com/Edboch/cli_finance_tracker.git
```

Navigate to the project directory

```
cd <file_path>\cli_finance_tracker
```

Install dependencies

```
pip install .
```

# Use

Commands:
```
spend [amount] [--desc] [--date]
deposit [amount] [--desc] [--date]
update [row_id] [column_title] [new_value]
list [--from_date] [--upto]
summary [--from_date] [--upto]
delete [row_id]
```

Note: commands with '--' mean they are optional and those without are necessary.

Example use of Spend:

```
finance-tracker spend 20 --desc coffee --date 2023-09-10
```

```
finance-tracker spend 20
```

Example use of deposit:

```
finance-tracker deposit 20 --desc income
```

```
finance-tracker deposit 20
```

Example use of update:

```
finance-tracker update 1 Description investment
```

Example use of list:

```
finance-tracker list
```

```
finance-tracker list --from_date 2020-06-10 --upto 2024-03-02
```

Example use of summary:

```
finance-tracker summary
```

```
finance-tracker summary --from_date 2020-06-10 --upto 2024-03-02
```

Example use of delete:

```
finance-tracker delete 1
```