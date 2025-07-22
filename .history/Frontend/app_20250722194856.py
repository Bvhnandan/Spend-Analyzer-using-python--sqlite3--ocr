import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"

st.title("PyReceiptAnalyzer Dashboard")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a receipt", type=["png", "jpg", "jpeg", "pdf", "txt"])
if uploaded_file:
    with st.spinner('Processing...'):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        resp = requests.post(f"{API_BASE}/upload", files=files)
        if resp.ok:
            st.success("Receipt uploaded successfully!")
        else:
            st.error(f"Upload failed: {resp.json().get('detail')}")

# --- Show Receipts Table ---
if st.button("Refresh Receipts Table"):
    data = requests.get(f"{API_BASE}/receipts").json()
    df = pd.DataFrame(data)
    st.dataframe(df)

# --- Analytics ---
if st.sidebar.button("Show Analytics"):
    stats = requests.get(f"{API_BASE}/analytics/spending").json()
    st.sidebar.header("Spending Stats")
    st.sidebar.json(stats)

    monthly = requests.get(f"{API_BASE}/analytics/monthly").json()
    mdf = pd.DataFrame(list(monthly.items()), columns=["Month", "Total Spend"])
    st.bar_chart(mdf.set_index("Month"))

    vendors = requests.get(f"{API_BASE}/analytics/vendors").json()
    vdf = pd.DataFrame(list(vendors.items()), columns=["Vendor", "Count"])
    st.sidebar.bar_chart(vdf.set_index("Vendor"))
