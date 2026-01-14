import json
import uuid
from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def write_decision_log(state: dict) -> str:
    """
    Writes an immutable audit log for a single workflow run.
    Returns the run_id.
    """

    run_id = str(uuid.uuid4())

    record = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat(),
        "customer": state.get("customer"),
        "conversation": state.get("conversation"),
        "safety": state.get("safety"),
        "execution": state.get("execution"),
        "decision_trace": state.get("decision_trace"),
        "meta": state.get("meta"),
    }

    file_path = LOG_DIR / f"{run_id}.json"

    with open(file_path, "w") as f:
        json.dump(record, f, indent=2)

    return run_id
