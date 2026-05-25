# Inside app.py under: with col_right: if trigger_actuation:
try:
    # 1. Attempt to communicate with local decoupled server engine
    response = requests.post("http://127.0.0.1:8000/api/v1/actuate", json=payload, timeout=2)
    res_data = response.json()
    command = res_data["command"]
    elapsed = res_data["elapsed_ms"]
    status_msg = res_data["status"]
except Exception:
    # 2. CLOUD FALLBACK MODE: Import logic directly to run inside the UI process
    import main
    from groq import AsyncGroq
    import asyncio

    # Securely retrieve the key from Streamlit's container vault
    api_key = st.secrets["GROQ_API_KEY"]
    client = AsyncGroq(api_key=api_key)
    
    start_time = time.perf_counter()
    # Call the fallback method directly from main.py without network serialization overhead
    command = asyncio.run(main.run_resilient_cascade(client, payload["telemetry_context"], payload["query_anomaly"]))
    elapsed = round((time.perf_counter() - start_time) * 1000, 2)
    status_msg = "SUCCESS (CLOUD DIRECT)"
