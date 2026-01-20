def learning_agent(state):
    """Learning agent for model improvement and feedback."""
    # Log the workflow execution for continuous improvement
    import json
    from datetime import datetime
    
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "latest_sales": state.get("latest_sales"),
            "anomaly": state.get("anomaly"),
            "z_score": state.get("z_score"),
            "forecast_sales": state.get("forecast_sales"),
            "decision": state.get("decision")
        }
        
        # Append to learning log
        with open("learning_log.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        pass
    
    return state
