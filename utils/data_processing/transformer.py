
from typing import Any, Callable, Dict, Iterable, List
import pandas as pd

class Transformer:
    """Generic collection/dataframe transformation helpers."""

    @staticmethod
    def map_list(items: Iterable[Any], fn: Callable[[Any], Any]) -> List[Any]:
        """Map a function over iterable and return list."""
        return [fn(x) for x in items]

    @staticmethod
    def filter_list(items: Iterable[Any], pred: Callable[[Any], bool]) -> List[Any]:
        """Filter iterable by predicate and return list."""
        return [x for x in items if pred(x)]

    @staticmethod
    def to_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
        """Convert list of dicts to pandas DataFrame."""
        return pd.DataFrame(records)

    @staticmethod
    def select_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Select subset of columns from DataFrame."""
        return df[cols].copy()

def main() -> None:
    data = [{"a":1,"b":2}, {"a":2,"b":3}]
    df = Transformer.to_dataframe(data)
    print(Transformer.select_columns(df, ["a"]))

if __name__ == "__main__":
    main()
