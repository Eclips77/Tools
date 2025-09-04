
from typing import Any
import json
import yaml
import pickle

class Serializer:
    """Serialize/deserialize helpers for JSON, YAML, and Pickle."""

    @staticmethod
    def to_json(obj: Any) -> str:
        """Serialize object to JSON string."""
        return json.dumps(obj, ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(s: str) -> Any:
        """Deserialize object from JSON string."""
        return json.loads(s)

    @staticmethod
    def to_yaml(obj: Any) -> str:
        """Serialize object to YAML string."""
        return yaml.safe_dump(obj, sort_keys=False)

    @staticmethod
    def from_yaml(s: str) -> Any:
        """Deserialize object from YAML string."""
        return yaml.safe_load(s)

    @staticmethod
    def to_pickle(obj: Any) -> bytes:
        """Serialize object to Pickle bytes."""
        return pickle.dumps(obj)

    @staticmethod
    def from_pickle(b: bytes) -> Any:
        """Deserialize object from Pickle bytes."""
        return pickle.loads(b)

def main() -> None:
    j = Serializer.to_json({"a": 1})
    print(j)

if __name__ == "__main__":
    main()
