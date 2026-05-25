import streamlit as st
import requests

# Set page config once
st.set_page_config(page_title="AETHER-FRACTAL // GOVERNOR CORE", page_icon="💠", layout="wide")

# High-density terminal styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    * { font-family: 'JetBrains+Mono', monospace !important; }
    .reportview-container { background: #0A0A0C; }
    .stMetric { background: #111216; border: 1px solid #1E2028; padding: 15px; border-radius: 4px; }
    div.stButton > button { background-color: #111216; color: #00FF66; border: 1px solid #00FF66; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #FFFFFF; font-size: 26px; margin-bottom: 0px;'>💠 AETHER-FRACTAL // CORE HUD</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #1E2028; margin-top: 10px; margin-bottom: 20px;' />", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("<p style='color: #FF3366; font-size: 12px; font-weight: bold;'>⚡ LIVE TELEMETRY SIMULATOR</p>", unsafe_allow_html=True)
    
    node_id = st.selectbox("TARGET NODE", ["NODE_ALPHA_01", "NODE_ALPHA_04", "NODE_OMEGA_09"])
    temp = st.slider("SILICON TEMP (°C)", min_value=40.0, max_value=120.0, value=94.2, step=0.1)
    power = st.slider("POWER DRAW (kW)", min_value=1.0, max_value=30.0, value=14.8, step=0.1)
    flow = st.slider("COOLANT FLOW (LPM)", min_value=0.5, max_value=10.0, value=2.1, step=0.1)
    
    anomaly_msg = st.text_area("ANOMALY EVENT", value="Thermal vector spike exceeding 92C threshold.")
    trigger_actuation = st.button("DISPATCH COMMAND")

with col_right:
    if trigger_actuation:
        # Build payload using raw Streamlit secrets configuration
        payload = {
            "telemetry_context": {
                "node_id": node_id,
                "silicon_temperature_celsius": temp,
                "power_draw_kw": power,
                "coolant_flow_rate_lpm": flow
            },
            "query_anomaly": anomaly_msg
        }
        
        try:
            # Send immediate payload request over local networking port
            response = requests.post("http://127.0.0.1:8000/api/v1/actuate", json=payload)
            
            if response.status_code == 200:
                res_data = response.json()
                
                m1, m2, m3 = st.columns(3)
                m1.metric(label="GATEWAY STATUS", value=res_data["status"])
                m2.metric(label="LOOP LATENCY", value=f"{res_data['elapsed_ms']} ms")
                m3.metric(label="FIREWALL CLAMP", value="ACTIVE (100%)")
                
                st.markdown("<p style='color: #00FF66; font-size: 12px; font-weight: bold; margin-top: 20px;'>🛡️ COMMAND OUTBOUND PAYLOAD</p>", unsafe_allow_html=True)
                st.json(res_data["command"])
            else:
                st.error(f"ENGINE CRITICAL ERROR: {response.status_code}")
        except Exception as e:
            st.error(f"CONNECTION FAILURE: Is Terminal 1 engine running? Details: {e}")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric(label="GATEWAY STATUS", value="ONLINE")
        m2.metric(label="LOOP LATENCY", value="0.00 ms")
        m3.metric(label="FIREWALL CLAMP", value="READY")
