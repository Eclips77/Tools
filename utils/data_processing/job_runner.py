
from typing import Callable, Dict, List
import threading

class JobRunner:
    """Register and run jobs synchronously or in threads."""

    def __init__(self) -> None:
        self.jobs: Dict[str, Callable[[], None]] = {}

    def register(self, name: str, fn: Callable[[], None]) -> None:
        """Register a job by name."""
        self.jobs[name] = fn

    def run_all(self) -> None:
        """Run all jobs synchronously."""
        for name, fn in self.jobs.items():
            fn()

    def run_all_threads(self) -> None:
        """Run all jobs concurrently using threads."""
        threads: List[threading.Thread] = []
        for name, fn in self.jobs.items():
            t = threading.Thread(target=fn, name=name, daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def main() -> None:
    jr = JobRunner()
    jr.register("hello", lambda: print("hello"))
    jr.register("world", lambda: print("world"))
    jr.run_all_threads()

if __name__ == "__main__":
    main()
