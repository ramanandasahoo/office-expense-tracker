"""
expense_manager.py
------------------
This file holds the "logic" of the project: reading and writing the CSV file,
checking user input, and calculating totals.

It does NOT print menus or ask the user questions. That is the job of main.py.
Keeping the two jobs separate makes each file shorter and easier to understand.
"""

import csv                      # Built-in module for reading/writing CSV files
import os                       # Built-in module for working with file paths
from datetime import datetime   # Built-in module for working with dates

# ---------------------------------------------------------------------------
# Settings (constants). Written in CAPITALS by Python convention.
# ---------------------------------------------------------------------------

# Build the path to data/expenses.csv relative to THIS file, so the program
# works no matter which folder you run it from.
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_FOLDER, "data", "expenses.csv")

# The column names of the CSV file, in order.
FIELDNAMES = ["Date", "Description", "Category", "Amount"]

# Categories the user can choose from when adding an expense.
CATEGORIES = [
    "Stationery",
    "Travel",
    "Utilities",
    "Rent",
    "Internet & Phone",
    "Maintenance",
    "Refreshments",
    "Other",
]

# Text shown before money amounts. Change it if you want (for example "$").
CURRENCY = "Rs."


# ---------------------------------------------------------------------------
# Input checking (validation)
# ---------------------------------------------------------------------------

def validate_date(text):
    """Check that text is a real date in YYYY-MM-DD format.

    Returns the cleaned date string if it is valid.
    Raises ValueError with a friendly message if it is not.
    """
    text = text.strip()
    try:
        # strptime tries to read the text using the given format.
        # It fails for things like "2026-13-45" or "hello".
        parsed = datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be a real date in YYYY-MM-DD format, e.g. 2026-09-15.")
    return parsed.strftime("%Y-%m-%d")


def validate_description(text):
    """Check that the description is not empty."""
    text = text.strip()
    if text == "":
        raise ValueError("Description cannot be empty.")
    return text


def validate_amount(text):
    """Check that text is a positive number. Returns it as a float rounded to 2 decimals."""
    text = text.strip().replace(",", "")   # allow people to type 1,500
    try:
        amount = float(text)
    except ValueError:
        raise ValueError("Amount must be a number, e.g. 250 or 99.50.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if amount != amount or amount == float("inf"):
        # "nan" and "inf" are accepted by float() but are not real amounts.
        raise ValueError("Amount must be a normal number.")
    return round(amount, 2)


def validate_month(text):
    """Check that text is a month in YYYY-MM format. Returns the cleaned text."""
    text = text.strip()
    try:
        datetime.strptime(text, "%Y-%m")
    except ValueError:
        raise ValueError("Month must be in YYYY-MM format, e.g. 2026-09.")
    return text


# ---------------------------------------------------------------------------
# Reading and writing the CSV file
# ---------------------------------------------------------------------------

def ensure_file_exists():
    """Create the CSV file (with only the header row) if it does not exist yet."""
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
            writer.writeheader()


def load_expenses():
    """Read every expense from the CSV file.

    Returns a tuple: (list_of_expenses, number_of_skipped_rows).
    Each expense is a dictionary like:
        {"Date": "2026-09-01", "Description": "Printer paper", "Category": "Stationery", "Amount": 450.0}
    Rows with a bad date or amount are skipped instead of crashing the program.
    """
    ensure_file_exists()
    expenses = []
    skipped = 0

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)   # reads each row as a dictionary
        for row in reader:
            try:
                expenses.append({
                    "Date": validate_date(row["Date"]),
                    "Description": validate_description(row["Description"]),
                    "Category": (row["Category"] or "").strip() or "Other",
                    "Amount": validate_amount(row["Amount"]),
                })
            except (ValueError, KeyError, TypeError, AttributeError):
                skipped += 1            # bad row: count it and move on

    return expenses, skipped


def add_expense(date, description, category, amount):
    """Validate the four values and append them as a new row in the CSV file.

    Raises ValueError if any value is invalid, so main.py can show the message.
    """
    new_row = {
        "Date": validate_date(date),
        "Description": validate_description(description),
        "Category": category.strip() or "Other",
        "Amount": validate_amount(str(amount)),
    }

    ensure_file_exists()
    # "a" means append: add to the end of the file without erasing it.
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        # Store the amount with exactly 2 decimals, e.g. 1250.50
        new_row["Amount"] = f"{new_row['Amount']:.2f}"
        writer.writerow(new_row)

    return new_row


# ---------------------------------------------------------------------------
# Calculations and reports
# ---------------------------------------------------------------------------

def total_expenses(expenses):
    """Add up the Amount of every expense."""
    total = 0
    for expense in expenses:
        total += expense["Amount"]
    return round(total, 2)


def totals_by_category(expenses):
    """Return a dictionary like {"Travel": 1200.0, "Rent": 15000.0}."""
    totals = {}
    for expense in expenses:
        category = expense["Category"]
        # .get(key, 0) gives 0 if the category has not been seen yet.
        totals[category] = totals.get(category, 0) + expense["Amount"]
    return {category: round(amount, 2) for category, amount in totals.items()}


def monthly_totals(expenses):
    """Return the total spent in each month, like {"2026-08": 18500.0, "2026-09": 20100.0}."""
    totals = {}
    for expense in expenses:
        month = expense["Date"][:7]     # "2026-09-15" -> "2026-09"
        totals[month] = totals.get(month, 0) + expense["Amount"]
    return {month: round(amount, 2) for month, amount in totals.items()}


def expenses_for_month(expenses, month):
    """Return only the expenses that belong to one month (YYYY-MM)."""
    return [e for e in expenses if e["Date"].startswith(month)]


def format_money(amount):
    """Format a number like 1234.5 as 'Rs. 1,234.50'."""
    return f"{CURRENCY} {amount:,.2f}"
