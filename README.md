# Office Expense Tracker

A simple command-line program written in Python that records office expenses in a CSV file and produces basic reports. This is a beginner project built to practise Python, file handling, and basic expense accounting.

## Project Overview

Small offices often track spending in a notebook or a loose spreadsheet. This project keeps every expense in one organised CSV file (Date, Description, Category, Amount) and lets the user add records and view totals, category breakdowns, and monthly summaries from a text menu.

## Features

- Add an expense with date, description, category, and amount
- View all expenses in a tidy table, sorted by date
- Calculate the total of all expenses
- Show totals by category with each category's percentage share
- Monthly summary: total spending per month, plus a category breakdown for any chosen month
- Input checking: invalid dates, empty descriptions, and non-numeric, zero, or negative amounts are rejected with a clear message
- Rows in the CSV that are damaged are skipped with a warning instead of crashing the program
- Sample data included so the project can be demonstrated immediately

## Technologies Used

- Python 3 (standard library only: `csv`, `os`, `datetime`)
- CSV file for data storage
- Git and GitHub for version control

No extra packages need to be installed.

## Project Structure

```
office-expense-tracker/
├── main.py              # Menu and user interaction (run this file)
├── expense_manager.py   # CSV reading/writing, validation, calculations
├── data/
│   └── expenses.csv     # Expense records (includes sample data)
├── README.md            # Project documentation
└── .gitignore           # Files Git should ignore
```

## How to Install and Run

1. Install Python 3.8 or newer from https://www.python.org/downloads/
2. Download or clone this repository:
   ```
   git clone https://github.com/<your-username>/office-expense-tracker.git
   cd office-expense-tracker
   ```
3. Run the program:
   ```
   python main.py
   ```
   On some systems use `python3 main.py` instead.

## Example Usage

```
============================================================
OFFICE EXPENSE TRACKER
============================================================
1. Add an expense
2. View all expenses
3. Calculate total expenses
4. Show expenses by category
5. Monthly summary
6. Exit

Enter your choice (1-6): 4

============================================================
EXPENSES BY CATEGORY
============================================================
Rent                   Rs. 45,000.00   (71.0%)
Utilities               Rs. 7,630.00   (12.0%)
Internet & Phone        Rs. 3,597.00   (5.7%)
Stationery              Rs. 3,205.50   (5.1%)
Maintenance             Rs. 1,500.00   (2.4%)
Travel                  Rs. 1,370.00   (2.2%)
Refreshments            Rs. 1,040.00   (1.6%)
----------------------------------------------------
TOTAL                  Rs. 63,342.50
```

Adding an expense:

```
Date (YYYY-MM-DD): 2026-09-30
Description: Postage
Choose a category:
  1. Stationery
  ...
Enter category number: 3
Amount in Rs.: 1250.50

Expense saved successfully.
```

## About the Sample Data

The records in `data/expenses.csv` are made-up examples for demonstration only. They do not represent any real organisation. Delete the rows (keep the header line) to start with your own records.

## Limitations

- Amounts are stored as decimal numbers (floats), which is fine for a learning project but not for professional accounting software
- Expenses can be added and viewed, but not edited or deleted from inside the program
- Single user, no login, no automated tests yet

## Future Improvements

- Edit and delete existing expenses
- Search and filter by date range or category
- Export a monthly report to a file
- Use the `decimal` module for exact money calculations
- Add automated tests with `unittest`
- Add budgets per category and warn when they are exceeded
- Build a simple graphical or web interface

## License

Free to use for learning purposes. Add a licence file (for example MIT) if you want others to reuse it formally.
