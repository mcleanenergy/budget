# budget

## A command line tool that automates the monthly budget process with Python and Pandas to track every dollar!

Quickly categorize income and expenses to see where your money is going. Set a reminder for the first of every month to track your spending habits with this budget tool.

For Chase only:
* Sign in to chase.com and download the transaction history of the previous month in CSV format
* Edit categories.csv with all income sources and expenses in alphabetical order
* Run budget.py
* Open the output file in spreadsheet form to copy the cells, then insert into the correct month on budget.xlsx

For Chase and Disover:
* Sign in to chase.com and download the transaction history of the previous month in CSV format
* Sign in to discover.com and download the transaction history under Year-to-Date
* Edit categories.csv with all income sources and expenses in alphabetical order, note 'Discover' is required in Expenses
* Run budget-discover.py
* Open the output file in spreadsheet form to copy the cells, then insert into the correct month on budget.xlsx

Requires Python and Pandas
