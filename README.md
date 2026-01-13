Agentic AI Pharmacy System

An offline-first, agentic AI system that transforms a traditional search-and-click pharmacy into an autonomous, safety-aware, proactive ecosystem.

The system behaves like an expert pharmacist:

Understands natural language orders

Enforces prescription and stock rules

Predicts refill needs

Executes backend actions autonomously

Exposes transparent agent reasoning (Chain-of-Thought)

Core Objectives

Replace manual pharmacy workflows with multi-agent autonomy

Ensure safety, compliance, and traceability

Work offline first, deployable later

Use free and open tools

Make agent reasoning auditable by judges

System Architecture (Agentic Design)

The system is built as a multi-agent society, coordinated by a workflow graph.

Agents
Agent	Responsibility
Conversation Agent	Understands messy human input, extracts intent, medicines, dosage
Safety Agent	Enforces prescription rules, stock availability, safety checks
Action Agent	Creates orders, updates inventory, triggers fulfillment
Workflow (LangGraph)	Orchestrates agents and controls execution flow

Each agent:

Has a single responsibility

Makes independent decisions

Writes its reasoning to a shared trace

🔍 Chain-of-Thought & Observability
Structured Reasoning (Judge-Visible)

Instead of hidden LLM chain-of-thought, the system uses a structured decision trace.

Each agent appends an entry like:
{
  "agent": "safety_agent",
  "input": {...},
  "reasoning": "Prescription not required and stock sufficient",
  "decision": "approved",
  "output": {...}
}
This allows judges to clearly see:

How agents communicated

Why an order was approved or rejected

What safety rules were applied

Observability (Langfuse)

Langfuse is integrated as an optional observability layer

Reasoning is forwarded if Langfuse is configured

System runs fully without Langfuse (offline-safe)

Observability never blocks execution.

Technology Stack
Backend

Python 3.9

FastAPI (mock APIs)

SQLite (local, zero-setup)

SQLAlchemy

Agent Orchestration

LangGraph

LLM (Offline)

LLaMA 3.1 8B

Running locally via Ollama / LM Studio

Observability

Langfuse (optional)

Frontend (Planned)

Minimal chat UI

Admin dashboard (inventory + alerts)

Project Structure

AI_PHARMA/
├── backend/
│   └── app/
│       ├── agents/
│       │   ├── conversation_agent.py
│       │   ├── safety_agent.py
│       │   └── action_agent.py
│       ├── api/
│       │   ├── medicines.py
│       │   ├── customers.py
│       │   └── orders.py
│       ├── db/
│       │   ├── database.py
│       │   ├── models.py
│       │   └── seed_data.py
│       ├── graph/
│       │   └── pharmacy_workflow.py
│       ├── observability/
│       │   └── langfuse_client.py
│       └── main.py
├── OBSERVABILITY.md
├── README.md
└── requirements.txt

⚙️ How the Workflow Runs

1. User input
"I need paracetamol 500mg"
2.Conversation Agent

Extracts intent and medicine

Infers quantity if missing

3.Safety Agent

Checks prescription requirement

Validates stock availability

Approves or blocks order

4.Action Agent

Creates order

Updates inventory

Triggers mock fulfillment

5.Decision Trace

All reasoning is logged and printed

▶️ Running the System
1. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Seed database
python3 backend/app/db/seed_data.py

3. Run agent workflow
python3 -m backend.app.graph.pharmacy_workflow

You will see:

Final state

Full decision trace

Agent-by-agent reasoning

🧪 Test Scenarios

Simple OTC order (Paracetamol)

Prescription-required medicine

Out-of-stock request

Ambiguous user input

Proactive refill (logic ready)