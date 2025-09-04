
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Callable
import time
import os

class FileWatchdog:
    """Monitor a directory for changes and call a handler on events."""

    def __init__(self, path: str, handler: Callable[[str, str], None]) -> None:
        self.path = path
        self.handler = handler
        self.observer = Observer()

    def start(self) -> None:
        """Start watching the directory."""
        class Handler(FileSystemEventHandler):
            def __init__(self, cb: Callable[[str, str], None]):
                self.cb = cb
            def on_any_event(self, event):
                self.cb(event.event_type, event.src_path)

        self.observer.schedule(Handler(self.handler), self.path, recursive=False)
        self.observer.start()

    def stop(self) -> None:
        """Stop watching."""
        self.observer.stop()
        self.observer.join()

def main() -> None:
    def cb(evt, path):
        print("Event:", evt, "Path:", path)
    os.makedirs("watched", exist_ok=True)
    fw = FileWatchdog("watched", cb)
    fw.start()
    print("Watching ./watched for ~2 seconds...")
    time.sleep(2)
    fw.stop()

if __name__ == "__main__":
    main()
