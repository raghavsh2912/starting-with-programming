"""Creates a sample expense dataset (transactions.csv) and budgets.json."""
import csv, json, random

random.seed(42)  # same "random" numbers every run
FIELDS = ["id", "date", "type", "category", "amount", "description"]
rows = []

def add(date, kind, cat, amount, desc):
    rows.append({"id": len(rows) + 1, "date": date, "type": kind,
                 "category": cat, "amount": round(amount, 2), "description": desc})

for month in ["2026-08", "2026-09", "2026-10"]:
    add(f"{month}-01", "income", "Income", 20000, "Monthly allowance")
    add(f"{month}-02", "expense", "Rent", 8000, "Hostel/room rent")
    add(f"{month}-05", "expense", "Utilities", random.randint(600, 900), "Mobile + internet")
    for day in range(3, 29, 3):
        add(f"{month}-{day:02d}", "expense", "Food", random.randint(120, 450), "Meals")
    for day in (4, 11, 18, 25):
        add(f"{month}-{day:02d}", "expense", "Transport", random.randint(50, 250), "Bus/metro/cab")
    add(f"{month}-12", "expense", "Entertainment", random.randint(200, 800), "Movie/games")
    add(f"{month}-20", "expense", "Shopping", random.randint(500, 2500), "Clothes/accessories")
    add(f"{month}-15", "expense", "Education", random.randint(300, 1200), "Books/courses")
    add(f"{month}-22", "expense", "Health", random.randint(100, 600), "Medicine")

with open("transactions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)

json.dump({"Food": 4000, "Transport": 800, "Rent": 8000, "Utilities": 900,
           "Shopping": 2000, "Entertainment": 700, "Health": 500, "Education": 1000},
          open("budgets.json", "w"), indent=4)
print(f"Created transactions.csv with {len(rows)} rows and budgets.json")
