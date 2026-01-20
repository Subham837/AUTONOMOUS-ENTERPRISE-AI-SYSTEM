def decision_agent(state):
    """Decision agent for making recommendations based on multiple factors."""
    anomaly = state.get("anomaly", False)
    z_score = state.get("z_score", 0)
    latest_sales = state.get("latest_sales", 100000)
    sql_avg = state.get("sql_avg_sales", 100000)
    rag_insight = state.get("rag_insight", "")
    
    # Dynamic decision logic based on multiple factors
    if anomaly:
        if z_score > 3:
            decision = "Critical sales spike detected (Z>3). Immediate action required: investigate market opportunity, optimize inventory, prepare scaling resources."
        elif z_score > 2:
            decision = f"Significant sales increase (+${latest_sales - sql_avg:,.0f}). Capitalize on opportunity: expand marketing budget, enhance customer support, analyze campaign drivers."
        elif z_score > 1.5:
            decision = "Moderate sales uplift detected. Monitor trends closely and prepare marketing campaigns to sustain momentum."
        elif z_score < -3:
            decision = "Critical sales decline (Z<-3). URGENT: Execute emergency retention protocol, contact top customers, review pricing strategy."
        elif z_score < -2:
            decision = f"Severe sales drop (-${sql_avg - latest_sales:,.0f}). Launch customer recovery campaigns, review product quality, analyze competitor activity."
        elif z_score < -1.5:
            decision = "Downward trend detected. Activate preventive retention strategies, increase customer engagement, conduct competitive analysis."
        else:
            decision = "Minor sales variance. Conduct root cause analysis to prevent further decline."
    else:
        # Non-anomalous but dynamic decisions based on sales level
        if latest_sales > sql_avg * 1.3:
            decision = "Sales performing well above average. Focus on maintaining quality while scaling operations cautiously."
        elif latest_sales > sql_avg * 1.1:
            decision = f"Sales performance is healthy at ${latest_sales:,.0f}. Continue current strategy with incremental optimization."
        elif latest_sales > sql_avg * 0.9:
            decision = "Sales near historical average. Maintain current operations while exploring new market segments."
        elif latest_sales > sql_avg * 0.7:
            decision = f"Sales below average by {((1 - latest_sales/sql_avg)*100):.0f}%. Implement gradual improvement plan without major disruption."
        else:
            decision = "Sales significantly underperforming. Review pricing, product fit, and marketing effectiveness."
    
    state["decision"] = decision
    return state
