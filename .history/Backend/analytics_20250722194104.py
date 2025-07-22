import pandas as pd

def spending_stats(conn):
    df = pd.read_sql("SELECT amount FROM receipts", conn)
    return {
        "sum": df['amount'].sum(),
        "mean": df['amount'].mean(),
        "median": df['amount'].median(),
        "mode": df['amount'].mode().tolist()
    }

def vendor_frequency(conn):
    df = pd.read_sql("SELECT vendor FROM receipts", conn)
    return df['vendor'].value_counts().to_dict()

def monthly_spending(conn):
    df = pd.read_sql("SELECT date, amount FROM receipts", conn)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().to_dict()
    return {str(period): float(amount) for period, amount in monthly.items()}
