from app.autonomy.refill_engine import run_refill_engine
from app.autonomy.scheduler import start_scheduler

if __name__ == "__main__":
    print("🔁 Running autonomous refill scheduler...")
    run_refill_engine()
    print("✅ Refill scan complete")
    start_scheduler()
