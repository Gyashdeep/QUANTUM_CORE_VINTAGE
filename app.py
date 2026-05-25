import streamlit as st
import psutil
import json
import asyncio
from groq import AsyncGroq
import pandas as pd

# --- SOVEREIGN CONFIGURATION ---
st.set_page_config(page_title="AETHER-KINETIC // VANTAGE", layout="wide")
st.markdown("<style>.stApp { background: #020202; color: #00FF66; font-family: monospace; }</style>", unsafe_allow_html=True)

# --- GOVERNANCE ENGINE (Consolidated for Path Stability) ---
async def execute_sovereign_edict():
    telemetry = {
        "cpu_load": psutil.cpu_percent(interval=0.1),
        "mem_load": psutil.virtual_memory().percent,
        "status": "OPERATIONAL_NODE"
    }
    
    # Secure API Call
    client = AsyncGroq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"""
    SYSTEM: AETHER-KINETIC VANTAGE. 
    CONTEXT: {telemetry}. 
    TASK: Execute kinetic arbitrage for sovereign yield.
    OUTPUT: JSON ONLY: {{ "decision": "...", "yield": "...", "rationale": "..." }}
    """
    
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.0
    )
    return json.loads(response.choices[0].message.content)

# --- UI GATEWAY ---
st.title("💠 AETHER-KINETIC // VANTAGE")
st.markdown("### Autonomous Sovereign Governance | Kinetic Arbitrage Engine")

if st.button("INITIATE SOVEREIGN PULSE"):
    with st.spinner("Reconciling silicon state-space..."):
        try:
            result = asyncio.run(execute_sovereign_edict())
            st.json(result)
        except Exception as e:
            st.error(f"Governance Failure: {str(e)}")

st.subheader("SYSTEM AUDIT TRAIL")
st.info("Awaiting live telemetry stream...")
