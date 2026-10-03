"""
main.py
-------
This is the file you run:  python main.py

It shows a menu, asks the user for input, and prints results.
All the real work (CSV handling, calculations, validation) is done by
functions imported from expense_manager.py.
"""

import expense_manager as em   # "em" is a short nickname for our other file


# ---------------------------------------------------------------------------
# Small helper functions for printing and asking questions
# ---------------------------------------------------------------------------

def print_header(title):
    """Print a title with lines around it so output looks tidy."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_expense_table(expenses):
    """Print a list of expenses as a neat table."""
    if not expenses:
        print("No expenses to show.")
        return

    # {:<12} means "left-align in 12 characters"; {:>12} means right-align.
    print(f"{'Date':<12}{'Description':<28}{'Category':<18}{'Amount':>14}")
    print("-" * 72)
    for e in expenses:
        description = e["Description"]
        if len(description) > 26:                  # shorten long text so the table stays tidy
            description = description[:23] + "..."
        print(f"{e['Date']:<12}{description:<28}{e['Category']:<18}{em.format_money(e['Amount']):>14}")


def ask_until_valid(prompt, validator):
    """Keep asking the same question until the answer passes the validator.

    The validator is one of the validate_... functions from expense_manager.py.
    """
    while True:
        answer = input(prompt)
        try:
            return validator(answer)
        except ValueError as error:
            print(f"  Invalid input: {error}")


def choose_category():
    """Show the category list and let the user pick by number."""
    print("Choose a category:")
    for number, name in enumerate(em.CATEGORIES, start=1):
        print(f"  {number}. {name}")

    while True:
        choice = input("Enter category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(em.CATEGORIES):
            return em.CATEGORIES[int(choice) - 1]
        print(f"  Invalid input: please enter a number from 1 to {len(em.CATEGORIES)}.")


def load_with_warning():
    """Load expenses, and warn the user if any rows in the CSV had to be skipped."""
    expenses, skipped = em.load_expenses()
    if skipped:
        print(f"Note: {skipped} row(s) in the CSV file were invalid and were skipped.")
    return expenses


# ---------------------------------------------------------------------------
# One function per menu option
# ---------------------------------------------------------------------------

def add_expense_screen():
    print_header("ADD AN EXPENSE")
    date = ask_until_valid("Date (YYYY-MM-DD): ", em.validate_date)
    description = ask_until_valid("Description: ", em.validate_description)
    category = choose_category()
    amount = ask_until_valid(f"Amount in {em.CURRENCY}: ", em.validate_amount)

    em.add_expense(date, description, category, amount)
    print("\nExpense saved successfully.")


def view_all_screen():
    print_header("ALL EXPENSES")
    expenses = load_with_warning()
    # sorted() with key=... puts the oldest date first.
    print_expense_table(sorted(expenses, key=lambda e: e["Date"]))
    print(f"\nNumber of records: {len(expenses)}")


def total_screen():
    print_header("TOTAL EXPENSES")
    expenses = load_with_warning()
    print(f"Total of {len(expenses)} expense(s): {em.format_money(em.total_expenses(expenses))}")


def category_screen():
    print_header("EXPENSES BY CATEGORY")
    expenses = load_with_warning()
    totals = em.totals_by_category(expenses)

    if not totals:
        print("No expenses to show.")
        return

    grand_total = em.total_expenses(expenses)
    # Show the biggest category first.
    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        share = amount / grand_total * 100
        print(f"{category:<20}{em.format_money(amount):>16}   ({share:.1f}%)")
    print("-" * 52)
    print(f"{'TOTAL':<20}{em.format_money(grand_total):>16}")


def monthly_screen():
    print_header("MONTHLY SUMMARY")
    expenses = load_with_warning()
    month_totals = em.monthly_totals(expenses)

    if not month_totals:
        print("No expenses to show.")
        return

    print("Total spending per month:")
    for month in sorted(month_totals):
        print(f"  {month}   {em.format_money(month_totals[month]):>16}")

    # Let the user look inside one month. Pressing Enter skips this part.
    print()
    while True:
        month = input("Enter a month (YYYY-MM) for a category breakdown, or press Enter to go back: ").strip()
        if month == "":
            return
        try:
            month = em.validate_month(month)
        except ValueError as error:
            print(f"  Invalid input: {error}")
            continue

        month_expenses = em.expenses_for_month(expenses, month)
        if not month_expenses:
            print(f"  No expenses found for {month}.")
            continue

        print(f"\nSummary for {month}")
        print(f"Number of expenses: {len(month_expenses)}")
        print(f"Total: {em.format_money(em.total_expenses(month_expenses))}")
        print("By category:")
        for category, amount in sorted(em.totals_by_category(month_expenses).items(),
                                       key=lambda item: item[1], reverse=True):
            print(f"  {category:<20}{em.format_money(amount):>16}")
        return


# ---------------------------------------------------------------------------
# The main menu loop
# ---------------------------------------------------------------------------

def main():
    em.ensure_file_exists()

    # A dictionary connecting each menu number to its function.
    actions = {
        "1": add_expense_screen,
        "2": view_all_screen,
        "3": total_screen,
        "4": category_screen,
        "5": monthly_screen,
    }

    while True:
        print_header("OFFICE EXPENSE TRACKER")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. Calculate total expenses")
        print("4. Show expenses by category")
        print("5. Monthly summary")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "6":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


# This line means: only start the program when this file is run directly
# (python main.py), not when it is imported by another file.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or Ctrl+D: exit politely instead of showing an error.
        print("\nProgram closed. Goodbye!")
