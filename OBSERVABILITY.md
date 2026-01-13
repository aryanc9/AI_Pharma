# Observability & Agent Reasoning

This system uses structured agent reasoning rather than hidden chain-of-thought.

## How reasoning is captured
Each agent appends a decision record to `decision_trace`:

- Agent name
- Input context
- Reasoning summary
- Decision
- Output

This allows judges to inspect:
- Why a request was approved or rejected
- How agents communicated
- What safety checks were enforced

## Langfuse Integration
Langfuse is integrated as an optional observability layer.

- If configured, traces are forwarded to Langfuse
- If unavailable, the system continues to function
- Core reasoning remains accessible in application logs

This design ensures:
- Full transparency
- Zero runtime coupling
- Offline-first development
