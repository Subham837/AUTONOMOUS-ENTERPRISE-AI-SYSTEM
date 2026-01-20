import numpy as np

def monitor_agent(state):
    """Monitor agent for tracking system state and detecting anomalies."""
    latest_sales = state.get("latest_sales", 100000)
    
    # Simple anomaly detection: check if sales are significantly different from expected
    # For demo: flag as anomaly if sales < 50000 or > 200000
    anomaly = latest_sales < 50000 or latest_sales > 200000
    z_score = (latest_sales - 100000) / 30000 if latest_sales >= 0 else 0
    
    state["anomaly"] = anomaly
    state["z_score"] = z_score
    return state
