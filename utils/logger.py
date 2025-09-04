import logging

class Logger:
    """Generic logger with adjustable level."""
    def __init__(self, name="AppLogger", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, message: str, level=logging.INFO):
        self.logger.log(level, message)

def main():
    log = Logger()
    log.log("Logger initialized")

if __name__ == "__main__":
    main()
