import time
from backend.app.autonomy.refill_engine import run_refill_engine

from backend.app.config import REFILL_INTERVAL_SECONDS


def start_scheduler():
    print("🔁 Autonomous refill scheduler started")

    while True:
        try:
            run_refill_engine()
            print("✅ Refill scan completed")
        except Exception as e:
            print(f"❌ Scheduler error: {e}")

        time.sleep(REFILL_INTERVAL_SECONDS)
