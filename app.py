import streamlit as st
import pandas as pd
import sqlite3
import requests
import plotly.express as px

st.set_page_config(page_title="VANTAGE // GOVERNOR HUD", layout="wide")
st.markdown("<h1 style='color:#00FF66;'>💠 QUANTUM-CORE VANTAGE</h1>", unsafe_allow_html=True)

# Self-Healing Ledger Query
def fetch_logs():
    try:
        conn = sqlite3.connect("quantum_ledger.db")
        return pd.read_sql("SELECT * FROM logs ORDER BY ts DESC LIMIT 20", conn)
    except:
        return pd.DataFrame()

# Visual Logic
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("SYSTEM VECTORS")
    if st.button("EXECUTE GOVERNANCE PING"):
        res = requests.get("http://127.0.0.1:8000/api/v1/governance/status").json()
        st.write(res['governance'])

with col2:
    st.subheader("YIELD ARBITRAGE LOG")
    df = fetch_logs()
    if not df.empty:
        st.line_chart(df['ts']) # Simple trend line
        st.dataframe(df)
