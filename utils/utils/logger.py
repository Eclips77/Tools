
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

class Logger:
    """Configurable application logger with console and rotating file handlers."""

    def __init__(self, name: str = "app", level: int = logging.INFO, to_file: Optional[str] = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        self.logger.addHandler(ch)

        if to_file:
            fh = RotatingFileHandler(to_file, maxBytes=1_000_000, backupCount=3)
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)

    def get(self) -> logging.Logger:
        """Return the underlying logger."""
        return self.logger

def main() -> None:
    log = Logger(to_file="app.log").get()
    log.info("Logger ready")

if __name__ == "__main__":
    main()
