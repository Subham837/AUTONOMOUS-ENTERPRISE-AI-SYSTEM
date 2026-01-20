import os
from dotenv import load_dotenv
from typing import TypedDict
# ========== LANGGRAPH ==========
# LANGGRAPH: Framework for orchestrating multi-agent workflows
from langgraph.graph import StateGraph, END
# ==============================

# Load environment variables early
load_dotenv()

from agents.monitor_agent import monitor_agent
from agents.sql_agent import sql_agent
from agents.rag_agent import rag_agent
from agents.forecasting_agent import forecasting_agent
from agents.decision_agent import decision_agent
from agents.action_agent import action_agent
from agents.learning_agent import learning_agent

# Define formal state schema
# ========== LANGGRAPH ==========
# LANGGRAPH: TypedDict defines state schema shared between all agents
class AgentState(TypedDict):
    latest_sales: float
    anomaly: bool
    z_score: float
    sql_avg_sales: float
    rag_insight: str
    forecast_sales: float
    decision: str
    action: str
# ==============================

workflow = StateGraph(AgentState)

# ========== LANGGRAPH ==========
# LANGGRAPH: Add all 7 agent nodes to the graph
workflow.add_node("monitor", monitor_agent)
workflow.add_node("sql", sql_agent)
workflow.add_node("rag", rag_agent)
workflow.add_node("forecast", forecasting_agent)
workflow.add_node("decision", decision_agent)
workflow.add_node("action", action_agent)
workflow.add_node("learning", learning_agent)

# LANGGRAPH: Set starting node
workflow.set_entry_point("monitor")

# LANGGRAPH: Define sequential execution flow/edges between agents
workflow.add_edge("monitor", "sql")
workflow.add_edge("sql", "rag")
workflow.add_edge("rag", "forecast")
workflow.add_edge("forecast", "decision")
workflow.add_edge("decision", "action")
workflow.add_edge("action", "learning")
workflow.add_edge("learning", END)

# LANGGRAPH: Compile the workflow into executable form
app_workflow = workflow.compile()
# ==============================