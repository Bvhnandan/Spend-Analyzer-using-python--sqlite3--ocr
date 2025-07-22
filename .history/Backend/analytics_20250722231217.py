import pandas as pd
from fastapi import HTTPException

def spending_stats(conn):
    try:
        df = pd.read_sql("SELECT amount FROM receipts", conn)
        df['amount'] = (
            df['amount']
            .astype(str)
            .replace({',': ''}, regex=True)
            .astype(float)
        )
        return {
            "sum": round(df['amount'].sum(), 2),
            "mean": round(df['amount'].mean(), 2),
            "median": round(df['amount'].median(), 2),
            "mode": df['amount'].mode().tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

def vendor_frequency(conn):
    try:
        df = pd.read_sql("SELECT vendor FROM receipts", conn)
        freq = df['vendor'].value_counts().to_dict()
        return freq
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

def monthly_spending(conn):
    try:
        df = pd.read_sql("SELECT date, amount FROM receipts", conn)
        df = df[df['date'] != 'Unknown']  # drop unknowns
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['amount'] = (
            df['amount']
            .astype(str)
            .replace({',': ''}, regex=True)
            .astype(float)
        )
        df = df.dropna(subset=['date'])
        monthly = (df.groupby(df['date'].dt.to_period("M"))['amount'].sum())
        return {str(k): float(v) for k, v in monthly.items()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")
