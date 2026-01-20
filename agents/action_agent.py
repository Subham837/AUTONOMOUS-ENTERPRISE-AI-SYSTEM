def action_agent(state):
    """Action agent for executing decisions dynamically."""
    decision = state.get("decision", "")
    forecast = state.get("forecast_sales", 0)
    latest_sales = state.get("latest_sales", 0)
    z_score = state.get("z_score", 0)
    
    # Parse decision keywords and generate targeted actions
    decision_lower = decision.lower()
    
    if "critical sales spike" in decision_lower or "immediate action required" in decision_lower:
        action = f"[URGENT] Market Opportunity Response: 1) Temporarily increase production by 40%, 2) Launch premium tier marketing campaign, 3) Expected revenue: ${forecast:,.0f}, 4) Assign team to analyze campaign drivers"
    elif "significant sales increase" in decision_lower or "capitalize on opportunity" in decision_lower:
        action = f"[HIGH PRIORITY] Growth Acceleration: 1) Scale marketing spend by 25%, 2) Hire additional sales team (4-6 reps), 3) Optimize fulfillment, 4) Target revenue: ${forecast:,.0f}"
    elif "moderate sales uplift" in decision_lower:
        action = f"Sustained Growth Plan: 1) Increase marketing by 15%, 2) Launch email nurture campaigns, 3) Monitor conversion metrics, 4) Projected Q1 revenue: ${forecast:,.0f}"
    elif "critical sales decline" in decision_lower or "urgent: execute emergency" in decision_lower:
        action = f"[EMERGENCY] Crisis Management: 1) Contact top 50 customers within 24hrs, 2) Offer loyalty incentives, 3) Review pricing/features, 4) Activate backup vendors, 5) Recovery target: ${forecast:,.0f}"
    elif "severe sales drop" in decision_lower:
        action = f"[HIGH PRIORITY] Recovery Protocol: 1) Customer retention campaign (personalized offers), 2) Product quality review, 3) Competitive analysis, 4) Expected recovery: ${forecast:,.0f}"
    elif "downward trend" in decision_lower or "activate preventive" in decision_lower:
        action = f"Retention & Stabilization: 1) Increase customer touchpoints by 50%, 2) Run re-engagement campaigns, 3) Launch referral incentives, 4) Stabilize at ${forecast:,.0f}"
    elif "minor sales variance" in decision_lower or "conduct root cause" in decision_lower:
        action = "Analysis & Monitoring: 1) Deep-dive into recent changes, 2) Review customer feedback, 3) Analyze traffic sources, 4) Prepare contingency plans"
    elif "performing well above average" in decision_lower:
        action = f"Quality Scaling: 1) Maintain service levels while growing carefully, 2) Expand to adjacent markets (10% budget), 3) Build strategic partnerships, 4) Target sustained revenue: ${forecast:,.0f}"
    elif "healthy" in decision_lower and "continue" in decision_lower:
        action = f"Steady State Operations: 1) Optimize margins by 5%, 2) Launch customer satisfaction survey, 3) Test new channels (5% budget), 4) Maintain revenue at ${forecast:,.0f}"
    elif "near historical average" in decision_lower:
        action = f"Growth Exploration: 1) Identify underutilized market segments, 2) Run A/B tests for new messaging, 3) Develop adjacent product features, 4) Target growth to ${forecast:,.0f}"
    elif "below average" in decision_lower:
        action = f"Improvement Plan: 1) Analyze 5 recent lost deals, 2) Adjust pricing strategically, 3) Enhance value proposition, 4) Recovery timeline: 2-3 months, Target: ${forecast:,.0f}"
    elif "significantly underperforming" in decision_lower:
        action = f"Strategic Overhaul: 1) Complete market assessment, 2) Revise product positioning, 3) Restructure sales approach, 4) 90-day turnaround target: ${forecast:,.0f}"
    else:
        action = f"Monitor & Adapt: Closely track performance metrics. Target: ${forecast:,.0f}"
    
    state["action"] = action
    return state
