
import os
import json
import yaml
from typing import Any, Dict, Optional

class ConfigManager:
    """Load configuration from JSON, YAML and environment variables."""

    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path
        self.data: Dict[str, Any] = {}
        if path:
            self.load(path)

    def load(self, path: str) -> None:
        """Load configuration from JSON or YAML file into memory."""
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith(".json"):
                self.data = json.load(f)
            else:
                self.data = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a key from config, falling back to environment and default."""
        return self.data.get(key, os.getenv(key.upper(), default))

    def set(self, key: str, value: Any) -> None:
        """Set a value in memory (not persisted)."""
        self.data[key] = value

def main() -> None:
    cfg = ConfigManager()
    cfg.set("name", "yaakov")
    print(cfg.get("name", ""))

if __name__ == "__main__":
    main()
