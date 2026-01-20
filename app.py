import os
from dotenv import load_dotenv

# Load environment variables FIRST before importing anything else
load_dotenv()

# ========== FASTAPI ==========
# FastAPI: Web framework for creating REST APIs
from fastapi import FastAPI
# =============================

from workflow import app_workflow

# ========== FASTAPI ==========
# FastAPI: Initialize FastAPI application instance
app = FastAPI(title="AEI-2 Agent System", version="1.0.0")
# =============================

# ========== FASTAPI ==========
# FastAPI: GET endpoint for root path
@app.get("/")
def read_root():
    return {"message": "AEI-2 Agent System API", "status": "online"}

# ========== FASTAPI & LANGGRAPH ==========
# FastAPI: POST endpoint to execute workflow
# LANGGRAPH: app_workflow.invoke() executes the multi-agent pipeline
@app.post("/run-workflow")
def run_workflow(sales_data: dict):
    """Run the agent workflow with sales data."""
    try:
        result = app_workflow.invoke(sales_data)  # LANGGRAPH executes here
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========== FASTAPI ==========
# FastAPI: GET endpoint for health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}
# =============================
