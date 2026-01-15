from typing import TypedDict, List, Dict, Any

class MedicineRequest(TypedDict):
    name: str
    quantity: int
    dosage: str

class SafetyResult(TypedDict):
    approved: bool
    reason: str
    violations: List[str]

class ExecutionResult(TypedDict):
    order_id: int
    actions: List[str]

class AgentDecision(TypedDict):
    agent: str
    input: Any
    reasoning: str
    decision: str
    output: Any

class PharmacyState(TypedDict):
    conversation: Dict[str, Any]
    customer: Dict[str, Any]
    extraction: Dict[str, Any]
    safety: SafetyResult
    execution: ExecutionResult
    decision_trace: List[AgentDecision]
    meta: Dict[str, Any]

class PharmacyState(TypedDict):
    conversation: Dict[str, str]   # INPUT ONLY
    customer: Dict[str, Any]

    extraction: Dict[str, Any]
    safety: Dict[str, Any]
    execution: Dict[str, Any]

    decision_trace: List[Dict[str, Any]]
    meta: Dict[str, Any]