# 🧠 Agentic AI Pharmacy System

An autonomous, agent-based pharmacy backend that transforms traditional
search-and-click ordering into a proactive, safety-first AI system.

This system behaves like an expert pharmacist:
- Understands natural language (text)
- Enforces prescription and stock rules
- Predicts refill needs
- Executes real backend actions autonomously
- Provides full, judge-visible decision traces

---

## 🚀 Key Features

### 🗣 Conversational Ordering
- Natural language input
- Robust extraction of medicine, dosage, and quantity
- Handles messy human language

### 🛡 Safety & Policy Enforcement
- Inventory is the single source of truth
- Prescription enforcement
- Stock validation
- Quantity limits

### 🔁 Autonomous Refill Intelligence
- Background scheduler scans patient history
- Predicts when medicines are running low
- Generates proactive refill alerts

### 🤖 Agentic Architecture
Multiple specialized agents collaborate:
- Memory Agent
- Conversation Agent (LLM-powered)
- Safety Agent (deterministic)
- Action Agent
- Predictive Refill Agent

### 🔍 Full Observability
- Judge-visible decision traces
- Clear explanation of why actions were approved or blocked
- No black-box behavior

---

## 🧩 System Architecture

User → /chat API
→ Memory Agent
→ Conversation Agent (LLM)
→ Safety Agent
→ Action Agent
→ Refill Intelligence
→ Database + Alerts


---

## 🛠 Tech Stack

- **Backend**: FastAPI
- **Agents**: LangGraph
- **LLM**: LLaMA 3.1 (via Ollama, optional)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Containerization**: Docker
- **Observability**: Decision Trace Logs

---

## ⚙️ How to Run (Local)

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Initialize database
python3 -m backend.app.db.seed_data

3. Start server
uvicorn backend.app.main:app --reload

4. Open Swagger
http://127.0.0.1:8000/docs

💬 Chat API Example
curl -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"message":"I need paracetamol 500mg"}'


  
Response:
{
  "approved": true,
  "reply": "Order placed successfully",
  "order_id": 3
}


