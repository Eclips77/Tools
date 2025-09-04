
import re
from typing import Iterable, List

class DataCleaner:
    """Generic text cleaning utilities for normalization and sanitization."""

    @staticmethod
    def to_lower(text: str) -> str:
        """Lowercase a string."""
        return text.lower()

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Collapse repeated whitespace to single spaces."""
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def strip_html(text: str) -> str:
        """Remove naive HTML tags."""
        return re.sub(r"<[^>]*>", "", text)

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """Remove punctuation characters."""
        return re.sub(r"[\.,;:!?\-\(\)\[\]{}"'`~\/\\]", "", text)

    @staticmethod
    def pipeline(texts: Iterable[str]) -> List[str]:
        """Apply a basic cleaning pipeline to an iterable of strings."""
        out = []
        for t in texts:
            t = DataCleaner.to_lower(t)
            t = DataCleaner.strip_html(t)
            t = DataCleaner.normalize_whitespace(t)
            out.append(t)
        return out

def main() -> None:
    texts = ["<b>Hello</b>   World!", "This, is... COOL?  "]
    print(DataCleaner.pipeline(texts))

if __name__ == "__main__":
    main()
