# AEI-2: Autonomous Enterprise Intelligence Agent System
## Technical Interview Demonstration Guide

### Project Overview
**AEI-2** is a production-ready **agentic AI system** that orchestrates 7 specialized autonomous agents to analyze enterprise sales data and generate dynamic, context-aware strategic recommendations in real-time.

---

## 🏗️ Architecture Overview

### Core Technologies
- **LangGraph**: Multi-agent orchestration using StateGraph (sequential pipeline)
- **LangChain**: Retrieval-Augmented Generation (RAG) with FAISS vector database and OpenAI embeddings
- **FastAPI**: RESTful API server with 3 endpoints
- **Streamlit**: Interactive web dashboard for visual workflow testing
- **SQLite**: Relational database with 365 days of realistic sales transactions
- **OpenAI**: GPT-based embeddings for semantic document retrieval

### The 7 Agents
1. **Monitor Agent** (Z-score anomaly detection)
2. **SQL Agent** (Database queries for historical analysis)
3. **RAG Agent** (Knowledge retrieval from domain documents)
4. **Forecasting Agent** (Trend prediction with conditional logic)
5. **Decision Agent** (Context-specific strategic recommendations with 11+ paths)
6. **Action Agent** (Concrete, measurable action items mapped to decisions)
7. **Learning Agent** (Execution logging for continuous improvement)

---

## 🎯 Interview Demo Sequence

### Demo 1: Health Check & System Status
**Purpose**: Verify system is operational

**Command:**
```bash
curl http://127.0.0.1:8080/health
```

**Expected Output:**
```json
{"status": "healthy"}
```

---

### Demo 2: CLI Parameter Testing - Normal Scenario
**Purpose**: Show CLI parameter support and agent orchestration

**Command:**
```bash
python test_agents.py --sales 75000
```

**Expected Output:**
- All 7 agents execute successfully
- Monitor agent detects sales value
- SQL agent retrieves $27,079 historical average
- Decision: Sales performing well above average
- Action: Quality scaling with market expansion

---

### Demo 3: CLI Parameter Testing - Spike Scenario
**Purpose**: Demonstrate dynamic decision-making for outlier events

**Command:**
```bash
python test_agents.py --sales 350000 --z-score 8.33
```

**Expected Output:**
- Z-Score: 8.33 (critical spike detection)
- Decision: "Critical sales spike detected (Z>3)...investigate market opportunity"
- Action: "[URGENT] Market Opportunity Response: 1) Increase production 40%, 2) Launch premium marketing..."

**Talking Points:**
- Z-score calculation: (sales - $100,000) / $30,000
- Different decision path triggered for Z > 3
- Actions include specific percentages (40%) and timelines
- This would prompt urgent inventory/scaling decisions in production

---

### Demo 4: CLI Parameter Testing - Decline Scenario
**Purpose**: Show recovery protocol activation

**Command:**
```bash
python test_agents.py --sales 25000 --z-score -2.5
```

**Expected Output:**
- Z-Score: -2.50 (severe decline detection)
- Decision: "Severe sales drop (-$2,079)...Launch customer recovery campaigns"
- Action: "[HIGH PRIORITY] Recovery Protocol: 1) Customer retention campaign, 2) Product quality review..."

**Talking Points:**
- Negative Z-score triggers different decision logic
- Recovery protocol includes customer retention focus
- This demonstrates context-awareness: system adapts recommendations based on problem type

---

### Demo 5: Full Test Suite - All Scenarios
**Purpose**: Comprehensive validation of all decision paths

**Command:**
```bash
python test_agents.py --full-test
```

**Expected Output:**
- Scenario 1: Critical Spike ($350k)
- Scenario 2: Severe Decline ($25k)
- Scenario 3: Normal/Healthy ($110k)
- Scenario 4: Below Average ($65k)
- Scenario 5: Significantly Underperforming ($20k)

**Each scenario shows:**
- Different z-score values
- Context-specific decisions (5+ unique decision types)
- Mapped actions tailored to problem type

**Validation Points:**
- System generates 5+ different decisions (proves dynamic logic)
- Same structure, different content (proves agents orchestrate properly)
- Decisions vary based on mathematical thresholds and business logic

---

### Demo 6: API Integration Testing
**Purpose**: Show REST API capability for system integration

**Command (Custom Sales Data):**
```bash
curl -X POST http://127.0.0.1:8080/run-workflow \
  -H "Content-Type: application/json" \
  -d '{"latest_sales": 150000, "period": "Q4", "region": "North America"}'
```

**Expected Output:**
```json
{
  "status": "success",
  "result": {
    "latest_sales": 150000,
    "anomaly": true,
    "z_score": 1.67,
    "forecast": 157500,
    "decision": "Significant sales increase detected...",
    "action": "[PRIORITY] Opportunity Capitalization: ...",
    "timestamp": "2024-01-15T14:23:45"
  }
}
```

**Talking Points:**
- API enables integration with external systems (CRM, reporting dashboards)
- POST endpoint processes complete workflow through all 7 agents
- Returns structured JSON with all agent outputs
- Real-time processing: from request to complete analysis in <2 seconds

---

### Demo 7: Code Architecture Walkthrough
**Purpose**: Technical depth validation

**File: workflow.py - LangGraph Pipeline**
```python
graph = StateGraph(AgentState)
graph.add_node("monitor", monitor_agent)
graph.add_node("sql", sql_agent)
graph.add_node("rag", rag_agent)
graph.add_node("forecast", forecasting_agent)
graph.add_node("decision", decision_agent)
graph.add_node("action", action_agent)
graph.add_node("learning", learning_agent)

# Sequential execution: monitor → sql → rag → forecast → decision → action → learning
graph.add_edge("monitor", "sql")
graph.add_edge("sql", "rag")
# ... more edges
graph.add_edge("action", "learning")
graph.add_edge("learning", END)
```

**Key Architecture Points:**
- LangGraph StateGraph manages 7 sequential nodes
- AgentState TypedDict enforces type safety
- State flows through agents: each agent adds output to state
- Final learning agent logs complete execution for audit trail

**File: agents/decision_agent.py - Dynamic Logic**
```python
if z_score > 3:
    return "Critical sales spike detected (Z>3)..."
elif 2 < z_score <= 3:
    return "Significant sales increase detected..."
# ... 11+ conditional paths total
elif z_score < -3:
    return "Critical decline (Z<-3). URGENT retention protocol..."
```

**Talking Points:**
- 11+ distinct decision paths based on z-score ranges
- Each path generates unique, contextual recommendations
- Moves beyond generic template responses
- Decision determines action mapping in next agent

**File: agents/rag_agent.py - LangChain Integration**
```python
docs = TextLoader("data/knowledge_docs/").load()
split_docs = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
db = FAISS.from_documents(split_docs, embeddings)
context = db.similarity_search(query, k=3)
```

**Talking Points:**
- Retrieval-Augmented Generation enables domain-specific knowledge
- FAISS provides efficient vector similarity search (<100ms per query)
- Knowledge base contains 550+ lines of enterprise sales strategy
- Embeddings capture semantic meaning, not just keyword matching

---

## 🗣️ Interview Discussion Topics

### Q1: "Why is this an Agentic AI System?"
**Answer:**
1. **Autonomous Agents**: 7 independent specialized agents make decisions without human intervention
2. **Sequential Orchestration**: LangGraph ensures proper information flow and state management
3. **Tool Use**: Agents use tools (database queries, vector search, embeddings) to gather information
4. **Context Awareness**: Decisions vary dynamically based on input, not hardcoded responses
5. **Feedback Loop**: Learning agent logs executions for continuous improvement

### Q2: "How does the system handle different sales scenarios?"
**Answer:**
- **Z-Score Based Anomaly Detection**: Identifies statistical outliers
  - Normal range: -1.5 to 1.5
  - Moderate spike: 1.5-3.0
  - Critical spike: >3.0
  - Severe decline: <-3.0
- **Context-Specific Decisions**: 11+ decision paths triggered by different conditions
- **Action Mapping**: Each decision type maps to specific, measurable actions
- **Example**: $350k spike triggers "Market Opportunity Response" vs $25k decline triggers "Recovery Protocol"

### Q3: "How does the RAG system work?"
**Answer:**
- **Document Loading**: TextLoader reads knowledge documents (sales_analysis.txt, customer_retention.txt)
- **Chunking**: CharacterTextSplitter breaks documents into 500-char chunks with 50-char overlap
- **Embedding**: OpenAI Embeddings convert text to 1536-dimensional vectors
- **Vector Search**: FAISS similarity_search finds top-3 most relevant documents based on query
- **Integration**: Retrieved context provided to decision agent for informed recommendations

### Q4: "What makes decisions 'dynamic' vs 'static'?"
**Answer:**
- **Static Approach**: Generic response like "Review sales performance" regardless of input
- **Dynamic Approach**: Context-specific response that varies by:
  - Sales magnitude vs historical average
  - Z-score magnitude and direction
  - Forecasted trend (up/down)
  - Specific metrics (e.g., "40% production increase" for spikes, "customer retention campaign" for declines)
- **Validation**: Run `python test_agents.py --full-test` to see 5+ different decision types

### Q5: "How would this scale to production?"
**Answer:**
- **API First**: FastAPI endpoints enable integration with CRM, analytics platforms
- **Async Processing**: Can implement async agents for parallel execution instead of sequential
- **Database**: SQLite can migrate to PostgreSQL/MySQL for multi-user scenarios
- **Caching**: Add Redis for frequently accessed queries (historical averages, embeddings)
- **Monitoring**: Learning agent currently logs to JSONL; upgrade to production logging (ELK, DataDog)
- **Deployment**: Docker containerization for cloud deployment (AWS Lambda, GCP Cloud Run)

### Q6: "What is the role of each agent?"
**Answer:**
| Agent | Input | Output | Key Logic |
|-------|-------|--------|-----------|
| Monitor | Latest sales | Z-score, anomaly flag | Statistical anomaly detection |
| SQL | State | Avg sales, historical context | Database query for benchmarking |
| RAG | Decision-critical info | Domain knowledge context | Vector search + semantic retrieval |
| Forecasting | Anomaly flag, sales | Forecast value | Conditional trend prediction |
| Decision | All prior outputs | Strategic recommendation | 11+ conditional decision paths |
| Action | Decision string | Specific action items | Maps decisions to concrete actions |
| Learning | Complete state | Logged execution | Audit trail for ML fine-tuning |

---

## 📊 Performance Metrics (Optional Demo)

### Query the Learning Log
```bash
cat learning_log.jsonl | wc -l  # Total executions logged
tail -1 learning_log.jsonl | python -m json.tool  # Last execution details
```

### Database Statistics
```bash
sqlite3 sales.db "SELECT COUNT(*) FROM sales; SELECT AVG(amount) FROM sales;"
```

---

## 🚀 Quick Reference Commands

| Scenario | Command |
|----------|---------|
| Help & options | `python test_agents.py --help` |
| Default test | `python test_agents.py` |
| Custom sales | `python test_agents.py --sales 200000` |
| Spike scenario | `python test_agents.py --sales 350000 --z-score 8.33` |
| Decline scenario | `python test_agents.py --sales 25000 --z-score -2.5` |
| All scenarios | `python test_agents.py --full-test` |
| Health check | `curl http://127.0.0.1:8080/health` |
| API test | `curl -X POST http://127.0.0.1:8080/run-workflow -H "Content-Type: application/json" -d '{"latest_sales": 100000}'` |
| Dashboard | `python -m streamlit run dashboard.py` |

---

## ✅ Interview Preparation Checklist

- [ ] Verify all dependencies installed: `pip list | grep -i langchain`
- [ ] Test CLI parameter support: `python test_agents.py --help`
- [ ] Run one custom scenario: `python test_agents.py --sales 150000`
- [ ] Run full test suite: `python test_agents.py --full-test` (should show 5 different decisions)
- [ ] Start API server: `python -m uvicorn app:app --host 127.0.0.1 --port 8080`
- [ ] Test health endpoint: `curl http://127.0.0.1:8080/health`
- [ ] Review workflow.py for LangGraph architecture
- [ ] Review agents/decision_agent.py for dynamic logic (11+ paths)
- [ ] Check learning_log.jsonl for execution history
- [ ] Prepare architecture diagram (7 nodes → sequential pipeline)

---

## 🎓 Key Concepts to Emphasize

1. **Agentic AI**: Multiple autonomous agents + LangGraph orchestration = true agentic system
2. **Dynamic Decisions**: 11+ decision paths prove system adapts to context
3. **LangChain RAG**: Production-grade retrieval using embeddings + FAISS
4. **Production-Ready**: API, logging, error handling, structured outputs
5. **Scalability**: Async-ready, database-agnostic, containerizable
6. **Interview-Friendly**: CLI parameters enable live testing with interviewer input

---

## 📞 Support

For questions during the interview about specific components:
- **Architecture**: See workflow.py (StateGraph + 7 nodes)
- **Decision Logic**: See agents/decision_agent.py (11+ paths)
- **RAG Implementation**: See agents/rag_agent.py (LangChain pipeline)
- **Testing**: Run `python test_agents.py --help` for parameter options
- **API**: Review app.py endpoints (/health, /run-workflow, /)

