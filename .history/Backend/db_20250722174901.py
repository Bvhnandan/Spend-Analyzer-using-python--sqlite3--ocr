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
