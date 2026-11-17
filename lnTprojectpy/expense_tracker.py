"""
Personal Expense Tracking and Budget Management System
------------------------------------------------------
Records income/expenses, saves them to CSV, keeps budgets in JSON,
and produces monthly and category-wise reports.
"""

import csv
import json
import os
from datetime import datetime

# Folder where THIS file lives (all files are saved here)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- STEP 1: Constants (settings used everywhere) ----------
DATA_FILE = os.path.join(BASE_DIR, "transactions.csv")
BUDGET_FILE = os.path.join(BASE_DIR, "budgets.json")
FIELDS = ["id", "date", "type", "category", "amount", "description"]
CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Shopping",
              "Entertainment", "Health", "Education", "Other"]


# ---------- STEP 2: File handling (CSV) ----------
def load_transactions():
    """Read transactions.csv into a list of dictionaries."""
    transactions = []
    try:
        with open(DATA_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["id"] = int(row["id"])          # text -> whole number
                row["amount"] = float(row["amount"])  # text -> decimal number
                transactions.append(row)
    except FileNotFoundError:
        pass  # first run: no file yet, so start with an empty list
    except (ValueError, KeyError):
        print("Warning: the data file has a corrupted row. Some data was skipped.")
    return transactions


def save_transactions(transactions):
    """Write the whole list back to transactions.csv."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(transactions)


# ---------- STEP 3: File handling (JSON budgets) ----------
def load_budgets():
    """Read budgets.json into a dictionary like {"Food": 6000.0}."""
    try:
        with open(BUDGET_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: budgets.json is damaged. Starting with no budgets.")
        return {}


def save_budgets(budgets):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=4)


# ---------- STEP 4: Input validation (exception handling) ----------
def get_amount(prompt="Amount: "):
    """Keep asking until the user types a positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError("Amount must be greater than zero.")
            return value
        except ValueError as error:
            print(f"Invalid amount ({error}). Please type a number like 250.50")


def get_date(prompt="Date (YYYY-MM-DD, Enter for today): "):
    """Keep asking until the user types a valid date."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")  # raises ValueError if wrong
            return text
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD, e.g. 2026-11-16")


def get_category():
    """Show numbered categories; accept a number."""
    for number, name in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {name}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice. Pick a number from the list.")


# ---------- STEP 5: Core features ----------
def next_id(transactions):
    return max((t["id"] for t in transactions), default=0) + 1


def add_transaction(transactions, kind):
    """kind is 'income' or 'expense'."""
    date = get_date()
    category = "Income" if kind == "income" else get_category()
    amount = get_amount()
    description = input("Description (optional): ").strip()
    transactions.append({
        "id": next_id(transactions), "date": date, "type": kind,
        "category": category, "amount": amount, "description": description,
    })
    save_transactions(transactions)
    print(f"{kind.capitalize()} of {amount:.2f} saved.")


def view_transactions(transactions):
    if not transactions:
        print("No transactions yet.")
        return
    print(f"\n{'ID':<4}{'Date':<12}{'Type':<9}{'Category':<15}{'Amount':>10}  Description")
    print("-" * 70)
    for t in sorted(transactions, key=lambda x: x["date"]):
        print(f"{t['id']:<4}{t['date']:<12}{t['type']:<9}{t['category']:<15}"
              f"{t['amount']:>10.2f}  {t['description']}")


def delete_transaction(transactions):
    try:
        target = int(input("ID to delete: "))
    except ValueError:
        print("Please enter a number.")
        return
    for t in transactions:
        if t["id"] == target:
            transactions.remove(t)
            save_transactions(transactions)
            print("Deleted.")
            return
    print("No transaction with that ID.")


# ---------- STEP 6: Summaries ----------
def total_by_type(transactions, kind, month=None):
    """Sum of all income or expense (optionally for one month 'YYYY-MM')."""
    return sum(t["amount"] for t in transactions
               if t["type"] == kind and (month is None or t["date"].startswith(month)))


def category_summary(transactions, month=None):
    """Return {'Food': 4200.0, 'Rent': 12000.0, ...} for expenses."""
    totals = {}
    for t in transactions:
        if t["type"] == "expense" and (month is None or t["date"].startswith(month)):
            totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]
    return totals


def monthly_summary(transactions):
    """Return {'2026-10': {'income': x, 'expense': y}, ...}."""
    months = {}
    for t in transactions:
        key = t["date"][:7]  # first 7 characters = 'YYYY-MM'
        months.setdefault(key, {"income": 0.0, "expense": 0.0})
        months[key][t["type"]] += t["amount"]
    return months


def show_summaries(transactions):
    if not transactions:
        print("No data to summarise.")
        return
    print("\n--- Monthly summary ---")
    for month, data in sorted(monthly_summary(transactions).items()):
        saved = data["income"] - data["expense"]
        print(f"{month}: income {data['income']:.2f} | expense {data['expense']:.2f} | saved {saved:.2f}")
    print("\n--- Category-wise (all time) ---")
    for cat, amt in sorted(category_summary(transactions).items(), key=lambda x: -x[1]):
        print(f"{cat:<15}{amt:>10.2f}")


# ---------- STEP 7: Budget report ----------
def set_budget(budgets):
    category = get_category()
    budgets[category] = get_amount("Monthly budget for this category: ")
    save_budgets(budgets)
    print(f"Budget for {category} set to {budgets[category]:.2f}")


def build_budget_report(transactions, budgets, month):
    spent = category_summary(transactions, month)
    income = total_by_type(transactions, "income", month)
    expense = total_by_type(transactions, "expense", month)
    lines = [f"MONTHLY BUDGET REPORT - {month}", "=" * 60,
             f"{'Category':<15}{'Budget':>10}{'Spent':>10}{'Left':>10}  Status",
             "-" * 60]
    for cat in sorted(set(budgets) | set(spent)):
        budget, used = budgets.get(cat, 0), spent.get(cat, 0)
        if budget == 0:
            status = "No budget"
        elif used > budget:
            status = "OVER BUDGET"
        elif used >= 0.8 * budget:
            status = "Warning (80%+)"
        else:
            status = "OK"
        lines.append(f"{cat:<15}{budget:>10.2f}{used:>10.2f}{budget - used:>10.2f}  {status}")
    lines += ["-" * 60, f"Total income : {income:.2f}", f"Total expense: {expense:.2f}",
              f"Savings      : {income - expense:.2f}"]
    return "\n".join(lines)


def generate_report(transactions, budgets):
    month = input("Month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Example: 2026-10")
        return
    report = build_budget_report(transactions, budgets, month)
    print("\n" + report)
    report_path = os.path.join(BASE_DIR, f"report_{month}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print("\nSaved at:", report_path)


# ---------- STEP 8: Chart (optional) ----------
def show_chart(transactions):
    try:
        import matplotlib
        matplotlib.use("Agg")  # draw to a file only (no window needed)
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib is not installed for THIS Python.")
        print("Run:  python -m pip install matplotlib")
        return
    data = category_summary(transactions)
    if not data:
        print("No expenses to plot. Add expenses first.")
        return
    try:
        chart_path = os.path.join(BASE_DIR, "category_chart.png")
        plt.figure(figsize=(8, 5))
        plt.bar(list(data.keys()), list(data.values()), color="steelblue")
        plt.title("Spending by Category")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        print("Chart saved at:", chart_path)
    except Exception as error:
        print("Could not draw the chart:", error)


# ---------- STEP 9: Menu ----------
MENU = """
===== Expense Tracker =====
1. Add expense
2. Add income
3. View transactions
4. Delete transaction
5. Summaries
6. Set category budget
7. Monthly budget report
8. Spending chart
0. Exit
"""


def main():
    transactions = load_transactions()
    budgets = load_budgets()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction(transactions, "expense")
        elif choice == "2":
            add_transaction(transactions, "income")
        elif choice == "3":
            view_transactions(transactions)
        elif choice == "4":
            delete_transaction(transactions)
        elif choice == "5":
            show_summaries(transactions)
        elif choice == "6":
            set_budget(budgets)
        elif choice == "7":
            generate_report(transactions, budgets)
        elif choice == "8":
            show_chart(transactions)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose 0-8.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
