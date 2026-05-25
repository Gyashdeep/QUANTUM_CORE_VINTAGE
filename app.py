import streamlit as st
import sqlite3
import pandas as pd
import asyncio
from groq import AsyncGroq
import os

# Set page config
st.set_page_config(page_title="VANTAGE // GOVERNOR HUD", layout="wide")
st.markdown("<h1 style='color:#00FF66;'>💠 QUANTUM-CORE VANTAGE</h1>", unsafe_allow_html=True)

# Governance Engine (Now unified inside the App process)
async def run_governance():
    client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
    telemetry = {"silicon_temp": 55.0, "power_draw_kw": 12.4}
    
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "ACT AS VANTAGE GOVERNOR. JSON ONLY."},
                  {"role": "user", "content": str(telemetry)}],
        temperature=0.0
    )
    return telemetry, response.choices[0].message.content

# Visual Logic
if st.button("EXECUTE GOVERNANCE PING"):
    # Run the async engine
    telemetry, decision = asyncio.run(run_governance())
    
    # Store in Ledger
    conn = sqlite3.connect("quantum_ledger.db")
    conn.execute("CREATE TABLE IF NOT EXISTS logs (ts REAL, telemetry TEXT, decision TEXT)")
    conn.execute("INSERT INTO logs VALUES (?, ?, ?)", (pd.Timestamp.now().timestamp(), str(telemetry), decision))
    conn.commit()
    conn.close()
    
    st.success("Governance Ping Success")
    st.json(decision)

# Display Ledger
st.subheader("SYSTEM AUDIT TRAIL")
try:
    conn = sqlite3.connect("quantum_ledger.db")
    df = pd.read_sql("SELECT * FROM logs ORDER BY ts DESC LIMIT 10", conn)
    st.dataframe(df)
    conn.close()
except:
    st.info("No data yet.")
