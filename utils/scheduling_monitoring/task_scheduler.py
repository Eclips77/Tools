
import schedule
import time
from typing import Callable

class TaskScheduler:
    """Wrapper around `schedule` for periodic jobs."""

    def every_seconds(self, seconds: int, job: Callable[[], None]) -> None:
        """Schedule a job to run every N seconds."""
        schedule.every(seconds).seconds.do(job)

    def run_forever(self) -> None:
        """Run the scheduler loop forever."""
        while True:
            schedule.run_pending()
            time.sleep(0.5)

def main() -> None:
    ts = TaskScheduler()
    ts.every_seconds(1, lambda: print("tick"))
    # Uncomment to run forever:
    # ts.run_forever()
    print("Scheduler set (example).")

if __name__ == "__main__":
    main()
