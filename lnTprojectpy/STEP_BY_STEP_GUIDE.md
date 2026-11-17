# Personal Expense Tracker — Build It Yourself (Step by Step)

Everything here assumes you know nothing. Every new word is explained when it first appears.

---
## PART 0 — What are we building?
A program that lets you type in money you earn (**income**) and money you spend (**expenses**), saves it in a file, and then tells you where your money went and whether you stayed inside your **budget** (a spending limit you set per category).

**How to think about it:** every program does 3 things: take **input**, **process** it, give **output**. Ours:
- Input: you type an expense
- Process: store it, add things up, compare with budget
- Output: tables, reports, a chart

---
## PART 1 — Setup
1. Install Python from python.org (tick "Add to PATH" on Windows).
2. Install PyCharm Community (the editor, called an **IDE** = Integrated Development Environment, a tool where you write and run code).
3. Create a folder `expense_tracker`. Open it in PyCharm.
4. Create a file `expense_tracker.py`.
5. Optional chart library: in the terminal type `pip install matplotlib`. (**pip** = Python's app installer. **Library** = ready-made code written by others.)

---
## PART 2 — Key ideas you need first
| Term | Meaning | Example |
|---|---|---|
| **Variable** | A named box holding a value | `amount = 250` |
| **String** | Text | `"Food"` |
| **Float** | Number with decimals | `250.50` |
| **Integer** | Whole number | `7` |
| **List** | Ordered collection | `["Food", "Rent"]` |
| **Dictionary** | Collection of label→value pairs | `{"Food": 4000, "Rent": 8000}` |
| **Function** | A named reusable block of code | `def add_transaction(): ...` |
| **Loop** | Repeat code | `while True:` / `for t in list:` |
| **Condition** | Choose a path | `if x > 5:` |
| **Exception** | An error at run time (e.g. typing "abc" when a number is needed) | `ValueError` |
| **try/except** | "Try this; if an error happens, do that instead of crashing" | see Step 4 |
| **CSV** | Plain text table, values separated by commas | `2026-10-01,income,...` |
| **JSON** | Text format for dictionaries/lists | `{"Food": 4000}` |
| **Persistence** | Data survives after the program closes (because it is saved in a file) | |

**Our data design:** one transaction = one dictionary:
```python
{"id": 1, "date": "2026-10-01", "type": "expense",
 "category": "Food", "amount": 250.0, "description": "Lunch"}
```
All transactions = a **list of dictionaries**. This is how we use "lists and dictionaries to organize financial records" (objective 2).

---
## PART 3 — The steps (each maps to a block in `expense_tracker.py`)

### STEP 1 — Imports and constants
**Why:** Constants are values that never change. Writing them once at the top means you edit one place instead of fifty.
```python
import csv                      # read/write CSV files
import json                     # read/write JSON files
from datetime import datetime   # work with dates

DATA_FILE = "transactions.csv"
BUDGET_FILE = "budgets.json"
FIELDS = ["id", "date", "type", "category", "amount", "description"]
CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Shopping",
              "Entertainment", "Health", "Education", "Other"]
```
`import` loads a **module** (a Python file of ready-made tools).

### STEP 2 — Save and load transactions (CSV)
**Why:** Without this, everything vanishes when the program closes.
```python
def load_transactions():
    transactions = []
    try:
        with open(DATA_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["id"] = int(row["id"])
                row["amount"] = float(row["amount"])
                transactions.append(row)
    except FileNotFoundError:
        pass
    except (ValueError, KeyError):
        print("Warning: the data file has a corrupted row.")
    return transactions

def save_transactions(transactions):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(transactions)
```
Line-by-line:
- `open(..., "w")` opens a file for **w**riting (default is reading). `"w"` wipes the old content, which is fine because we write the whole list again.
- `with ... as f` opens the file and **automatically closes** it afterward.
- `DictReader` turns each CSV row into a dictionary using the header row as keys.
- A CSV stores everything as text, so `int()` and `float()` convert back to numbers. This is **type conversion**.
- `FileNotFoundError` happens on the first run (no file yet). `pass` means "do nothing", so we simply start with an empty list.

### STEP 3 — Budgets (JSON)
```python
def load_budgets():
    try:
        with open(BUDGET_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: budgets.json is damaged.")
        return {}

def save_budgets(budgets):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=4)
```
`json.load` = file → dictionary. `json.dump` = dictionary → file. `indent=4` makes the file readable.

### STEP 4 — Handling invalid input (exception handling)
**Why:** Users type nonsense. A good program asks again instead of crashing.
```python
def get_amount(prompt="Amount: "):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError("Amount must be greater than zero.")
            return value
        except ValueError as error:
            print(f"Invalid amount ({error}). Type a number like 250.50")
```
How it works:
1. `while True` repeats forever...
2. ...until `return` exits the function with a good value.
3. `float("abc")` raises `ValueError`. `except` catches it and prints a message; the loop runs again.
4. `raise` deliberately creates an error (for zero/negative numbers).

Date version uses `datetime.strptime(text, "%Y-%m-%d")`: it **parses** (reads) text as a date using a pattern (`%Y`=year, `%m`=month, `%d`=day) and raises `ValueError` if the text doesn't match. See `get_date()` and `get_category()` in the full file.

### STEP 5 — Core features (add, view, delete)
```python
def next_id(transactions):
    return max((t["id"] for t in transactions), default=0) + 1
```
Finds the largest existing ID and adds 1 (`default=0` handles an empty list).

`add_transaction` asks for date, category, amount, description → builds a dictionary → `append`s it to the list → calls `save_transactions`. 

`view_transactions` loops through `sorted(transactions, key=lambda x: x["date"])`. (`lambda` = a tiny nameless function; here it says "sort by the date field".) The `f"{t['amount']:>10.2f}"` part is an **f-string**: `>10` right-aligns in 10 spaces, `.2f` shows 2 decimals.

`delete_transaction` loops until the ID matches, then `remove`s it.

### STEP 6 — Summaries (the "data summarization" outcome)
```python
def category_summary(transactions, month=None):
    totals = {}
    for t in transactions:
        if t["type"] == "expense" and (month is None or t["date"].startswith(month)):
            totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]
    return totals
```
The key trick: `totals.get("Food", 0)` returns the current total for Food, or 0 if Food isn't there yet. Add the new amount and store it. After the loop you get e.g. `{"Food": 2247.0, "Rent": 8000.0}`.

`t["date"].startswith("2026-10")` checks whether a date belongs to October — works because dates are stored as `YYYY-MM-DD`.

`monthly_summary` uses `t["date"][:7]` (**slicing** = taking the first 7 characters, `2026-10`) as the key and `setdefault` to create a new entry if missing.

### STEP 7 — Monthly budget report
For each category: `budget`, `spent`, `left = budget − spent`, then a status using **conditional statements**:
```python
if used > budget:            status = "OVER BUDGET"
elif used >= 0.8 * budget:   status = "Warning (80%+)"
else:                        status = "OK"
```
`if / elif / else` checks conditions top to bottom and runs the first true one. The report text is built as a list of lines, joined with `"\n".join(lines)`, printed, and saved to `report_YYYY-MM.txt`.

### STEP 8 — Chart (optional, Matplotlib)
```python
import matplotlib.pyplot as plt
plt.bar(data.keys(), data.values())
plt.savefig("category_chart.png")
```
The import is inside `try/except ImportError` so the program still works if Matplotlib isn't installed.

### STEP 9 — The menu (ties everything together)
```python
def main():
    transactions = load_transactions()
    budgets = load_budgets()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_transaction(transactions, "expense")
        ...
        elif choice == "0":
            break
```
`break` exits the loop. The last lines:
```python
if __name__ == "__main__":
    main()
```
mean "run `main()` only when this file is run directly (not when imported)".

---
## PART 4 — Run and test
1. (Optional) run `python generate_dataset.py` to create 3 months of sample data (60 transactions) = your **Expense Dataset** deliverable.
2. Run `python expense_tracker.py`.
3. Test: add an expense, type `abc` as amount (should re-ask), view, summaries, set budget, report for `2026-10`.
4. Check that `transactions.csv` opens in Excel and updates.

**Test table for your report:**
| Test | Input | Expected |
|---|---|---|
| Bad amount | `abc`, `-5`, `0` | Re-asks |
| Bad date | `2026-13-45` | Re-asks |
| No file | delete CSV | Starts empty, no crash |
| Delete missing ID | `999` | "No transaction with that ID" |
| Over budget | Spend more than budget | "OVER BUDGET" |

---
## PART 5 — Deliverables checklist
| Deliverable | Where it comes from |
|---|---|
| Expense Dataset | `transactions.csv` from `generate_dataset.py` |
| Python Expense Tracker | `expense_tracker.py` |
| CSV/JSON records | `transactions.csv`, `budgets.json` |
| Monthly Budget Report | menu option 7 → `report_2026-10.txt` |
| Technical Report | Sections: Introduction, Problem, Objectives, Tools, Design (data structure + flowchart), Implementation (Steps 1–9), Testing (table above), Results (screenshots), Limitations, Future work |
| Final Presentation | ~8 slides: Title, Problem, Objectives, Design, Key code, Demo screenshots, Results, Future work |

**Future improvements to mention:** SQLite database, login, recurring expenses, GUI with Tkinter, export to Excel.

---
## PART 6 — Practice tips
- Type the code yourself rather than copying; run after each step.
- Use `print()` to inspect variables when confused.
- Break it on purpose, then fix it. This is how you learn.
- Extension ideas: edit a transaction, search by date range, a pie chart, a monthly chart of income vs expense.
