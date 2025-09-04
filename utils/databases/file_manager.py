
from typing import Any, List
from pathlib import Path
import shutil
import json
import yaml

class FileManager:
    """Generic file manager for text, JSON, YAML and file operations."""

    def __init__(self, base_path: str = ".") -> None:
        self.base = Path(base_path)

    def read_text(self, name: str) -> str:
        """Read a text file and return content."""
        return (self.base / name).read_text(encoding="utf-8")

    def write_text(self, name: str, content: str) -> None:
        """Write text to a file, creating parents if needed."""
        path = self.base / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def read_json(self, name: str) -> Any:
        """Read JSON file and return data."""
        return json.loads(self.read_text(name))

    def write_json(self, name: str, data: Any, indent: int = 2) -> None:
        """Write data as JSON."""
        self.write_text(name, json.dumps(data, indent=indent))

    def read_yaml(self, name: str) -> Any:
        """Read YAML file and return data."""
        return yaml.safe_load(self.read_text(name))

    def write_yaml(self, name: str, data: Any) -> None:
        """Write data as YAML."""
        self.write_text(name, yaml.safe_dump(data, sort_keys=False))

    def exists(self, name: str) -> bool:
        """Check if file exists."""
        return (self.base / name).exists()

    def list_files(self, subdir: str = "") -> List[str]:
        """List file names under a subdirectory (non-recursive)."""
        p = self.base / subdir
        return [str(x.name) for x in p.iterdir() if x.is_file()]

    def delete(self, name: str) -> None:
        """Delete a file."""
        (self.base / name).unlink(missing_ok=True)

    def copy(self, src: str, dst: str) -> None:
        """Copy a file from src to dst."""
        shutil.copy2(self.base / src, self.base / dst)

    def move(self, src: str, dst: str) -> None:
        """Move/rename a file from src to dst."""
        shutil.move(self.base / src, self.base / dst)

def main() -> None:
    fm = FileManager("./data")
    fm.write_text("hello.txt", "Hi there")
    print(fm.read_text("hello.txt"))
    fm.write_json("cfg.json", {"a": 1})
    print(fm.read_json("cfg.json"))

if __name__ == "__main__":
    main()
