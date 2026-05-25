import os
import time
import asyncio
import orjson
import streamlit as st
from pydantic import BaseModel, Field, ValidationError
from groq import AsyncGroq, RateLimitError

# =====================================================================
# 1. HARDWARE BOUNDARY ENFORCEMENT (The Physics Firewall)
# =====================================================================
class ActuationCommand(BaseModel):
    target_node_id: str
    action: str = Field(description="Must match exact hardware registry operation codes.")
    intensity_percentage: int = Field(ge=0, le=100, description="Clamp bounds to prevent kinetic damage.")
    risk_mitigation_reason: str

ACTUATION_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "actuate_cluster_state",
            "description": "Executes immediate hardware actuation overrides based on cluster telemetry anomalies.",
            "parameters": ActuationCommand.model_json_schema()
        }
    }
]

MODEL_FALLBACK_CASCADE = [
    "deepseek-r1-distill-qwen-1.5b",
    "llama3-70b-8192"
]

# =====================================================================
# 2. DIRECT INFERENCE PIPELINE (Bypasses FastAPI Network Layer)
# =====================================================================
async def run_resilient_cascade(telemetry: dict, anomaly: str) -> dict:
    """Runs high-speed inference directly inside the Streamlit container thread."""
    api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("CRITICAL: GROQ_API_KEY is missing from Streamlit Secrets.")
        
    async with AsyncGroq(api_key=api_key) as client:
        system_prompt = (
            "SYSTEM CRITICAL: You are an autonomous industrial hardware controller. "
            "Analyze the provided live telemetry state vectors and execute the required function tool. "
            "Do not output conversational text or pleasantries. Output raw JSON function arguments only."
        )
        
        serialized_vectors = orjson.dumps(telemetry).decode("utf-8")
        user_content = f"TELEMETRY STATE VECTORS:\n{serialized_vectors}\n\nCRITICAL ANOMALY EVENT: {anomaly}"

        for model in MODEL_FALLBACK_CASCADE:
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    tools=ACTUATION_TOOL,
                    tool_choice={"type": "function", "function": {"name": "actuate_cluster_state"}},
                    temperature=0.0
                )
                
                raw_args = response.choices[0].message.tool_calls[0].function.arguments
                parsed_json = orjson.loads(raw_args)
                
                validated_command = ActuationCommand(**parsed_json)
                return validated_command.model_dump()
                
            except (ValidationError, orjson.JSONDecodeError, RateLimitError, Exception) as err:
                st.warning(f"[TRAFFIC SHIFT] Node fallback active. Failure on {model}: {err}")
                continue

        raise RuntimeError("CRITICAL SHUTDOWN: Entire multi-model fallback loop exhausted.")

# =====================================================================
# 3. HUD TERMINAL STYLING & INTERFACE
# =====================================================================
st.set_page_config(page_title="AETHER-FRACTAL // GOVERNOR CORE", page_icon="💠", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght=400;700&display=swap');
    * { font-family: 'JetBrains+Mono', monospace !important; }
    .stApp { background-color: #0A0A0C; }
    .stMetric { background: #111216; border: 1px solid #1E2028; padding: 15px; border-radius: 4px; }
    .stMetric label { color: #8F93A2 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }
    .stMetric div { color: #00FF66 !important; font-weight: 700 !important; }
    div.stButton > button { background-color: #111216; color: #00FF66; border: 1px solid #00FF66; font-weight: bold; width: 100%; transition: all 0.3s; }
    div.stButton > button:hover { background-color: #00FF66; color: #0A0A0C; box-shadow: 0 0 15px rgba(0,255,102,0.6); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #FFFFFF; font-size: 26px; margin-bottom: 0px;'>💠 AETHER-FRACTAL // CORE HUD</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #4E5266; font-size: 11px; text-transform: uppercase; letter-spacing: 2px;'>Autonomous Edge Actuation & Sovereign Hardware Governance Subsystem</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #1E2028; margin-top: 10px; margin-bottom: 20px;' />", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("<p style='color: #FF3366; font-size: 12px; font-weight: bold;'>⚡ LIVE TELEMETRY SIMULATOR</p>", unsafe_allow_html=True)
    
    node_id = st.selectbox("TARGET INSTANCE NODE", ["NODE_ALPHA_01", "NODE_ALPHA_04", "NODE_OMEGA_09"])
    temp = st.slider("SILICON TEMP (°C)", min_value=40.0, max_value=120.0, value=94.2, step=0.1)
    power = st.slider("POWER DRAW (kW)", min_value=1.0, max_value=30.0, value=14.8, step=0.1)
    flow = st.slider("COOLANT FLOW (LPM)", min_value=0.5, max_value=10.0, value=2.1, step=0.1)
    
    anomaly_msg = st.text_area(
        "CRITICAL ANOMALY EVENT TRIGGER", 
        value="Thermal vector spike exceeding 92C threshold during localized training job load."
    )
    
    trigger_actuation = st.button("DISPATCH COMMAND")

with col_right:
    if trigger_actuation:
        payload = {
            "node_id": node_id,
            "silicon_temperature_celsius": temp,
            "power_draw_kw": power,
            "coolant_flow_rate_lpm": flow
        }
        
        try:
            with st.spinner("Executing direct low-latency inference loop via LPU cascade..."):
                start_time = time.perf_counter()
                
                command = asyncio.run(run_resilient_cascade(payload, anomaly_msg))
                
                elapsed = round((time.perf_counter() - start_time) * 1000, 2)
                
                m1, m2, m3 = st.columns(3)
                m1.metric(label="GATEWAY PIPELINE", value="SUCCESS (DIRECT)")
                m2.metric(label="LOOP LATENCY", value=f"{elapsed} ms")
                m3.metric(label="FIREWALL CLAMP", value="ACTIVE (100%)")
                
                st.markdown("<p style='color: #00FF66; font-size: 12px; font-weight: bold; margin-top: 20px;'>🛡️ VERIFIED HARDWARE COMMAND OUTBOUND PAYLOAD</p>", unsafe_allow_html=True)
                st.json(command)
                st.info(f"**GOVERNOR DECISION RATIONALE:** {command['risk_mitigation_reason']}")
                
        except Exception as ex:
            st.error(f"AIR-GAP CRITICAL INTERVENTION ERROR: {str(ex)}")
            
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric(label="GATEWAY STATUS", value="ONLINE")
        m2.metric(label="LOOP LATENCY", value="0.00 ms")
        m3.metric(label="FIREWALL CLAMP", value="READY")
        
        st.markdown("<div style='border: 1px dashed #1E2028; padding: 40px; text-align: center; color: #4E5266; margin-top: 20px; font-size: 12px;'>SYSTEM IDLE // AWAITING STREAM PAYLOAD TRANSMISSION</div>", unsafe_allow_html=True)
