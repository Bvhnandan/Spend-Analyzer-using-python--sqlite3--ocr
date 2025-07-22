import sqlite3

conn = sqlite3.connect("receipts.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor TEXT,
    date TEXT,
    amount REAL,
    category TEXT
)
""")
conn.commit()

def insert_receipt(vendor, date, amount, category=None):
    cursor.execute("""
    INSERT INTO receipts (vendor, date, amount, category)
    VALUES (?, ?, ?, ?)""", (vendor, date, amount, category))
    conn.commit()

def get_all_receipts():
    cursor.execute("SELECT * FROM receipts")
    return cursor.fetchall()

def search_receipts_db(vendor=None, date=None, min_amount=None, max_amount=None, sort_by="date", desc=False):
    query = "SELECT * FROM receipts WHERE 1=1"
    params = []
    
    if vendor:
        query += " AND vendor LIKE ?"
        params.append(f"%{vendor}%")
    if date:
        query += " AND date = ?"
        params.append(date)
    if min_amount is not None:
        query += " AND amount >= ?"
        params.append(min_amount)
    if max_amount is not None:
        query += " AND amount <= ?"
        params.append(max_amount)

    if sort_by in ["date", "amount", "vendor"]:
        query += f" ORDER BY {sort_by} {'DESC' if desc else 'ASC'}"

    cursor.execute(query, tuple(params))
    receipts = cursor.fetchall()
    return [
        {"id": r[0], "vendor": r[1], "date": r[2], "amount": r[3], "category": r[4]}
        for r in receipts
    ]
