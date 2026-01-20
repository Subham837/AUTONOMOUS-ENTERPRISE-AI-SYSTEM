def forecasting_agent(state):
    """Forecasting agent for predicting future trends."""
    latest_sales = state.get("latest_sales", 100000)
    sql_avg = state.get("sql_avg_sales", 100000)
    
    # Simple forecast: if anomaly detected, predict return to average, else slight growth
    if state.get("anomaly", False):
        forecast = sql_avg * 1.1  # 10% growth prediction
    else:
        forecast = latest_sales * 1.05  # 5% growth prediction
    
    state["forecast_sales"] = forecast
    return state
