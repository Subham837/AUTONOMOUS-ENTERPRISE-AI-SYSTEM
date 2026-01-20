import streamlit as st
import pandas as pd
# ========== LANGGRAPH ==========
# LANGGRAPH: Import compiled workflow for execution in dashboard
from workflow import app_workflow
# ==============================

st.set_page_config(page_title="AEI-2 Agent System", layout="wide")

st.title("🤖 AEI-2 Agent System Dashboard")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.header("📊 Input Data")
    latest_sales = st.number_input("Latest Sales", value=100000.0, step=1000.0)
    anomaly_threshold = st.number_input("Anomaly Z-Score Threshold", value=2.5, step=0.1)

with col2:
    st.header("⚙️ Configuration")
    st.info("The system uses multiple AI agents to analyze sales data and provide insights.")

st.markdown("---")

if st.button("🚀 Run Workflow Analysis", use_container_width=True):
    st.info("Running agent workflow...")
    
    try:
        # Prepare input state
        input_state = {
            "latest_sales": latest_sales,
            "anomaly": False,
            "z_score": 0.0,
            "sql_avg_sales": 0.0,
            "rag_insight": "",
            "forecast_sales": 0.0,
            "decision": "",
            "action": "",
        }
        
        # ========== LANGGRAPH ==========
        # LANGGRAPH: Execute the multi-agent workflow with input state
        result = app_workflow.invoke(input_state)
        # ==============================
        
        st.success("✅ Workflow completed successfully!")
        
        # Display results in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Anomaly Detected", "Yes" if result.get("anomaly") else "No")
            st.metric("Z-Score", f"{result.get('z_score', 0):.2f}")
        
        with col2:
            st.metric("Forecast Sales", f"${result.get('forecast_sales', 0):,.0f}")
            st.metric("Avg Sales (SQL)", f"${result.get('sql_avg_sales', 0):,.0f}")
        
        with col3:
            st.write("**Decision:**")
            st.write(result.get("decision", "No decision"))
        
        st.markdown("---")
        st.write("**RAG Insight:**")
        st.write(result.get("rag_insight", "No insights available"))
        
        st.markdown("---")
        st.write("**Recommended Action:**")
        st.write(result.get("action", "No action recommended"))
        
    except Exception as e:
        st.error(f"❌ Error running workflow: {str(e)}")

st.markdown("---")
st.markdown("*AEI-2: Autonomous Enterprise Intelligence Agent System*")
