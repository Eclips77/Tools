
from typing import Optional
from pyspark.sql import SparkSession, DataFrame

class SparkManager:
    """Create and manage a Spark session with convenient readers and SQL."""

    def __init__(self, app_name: str = "GenericSparkApp", master: Optional[str] = None) -> None:
        builder = SparkSession.builder.appName(app_name)
        if master:
            builder = builder.master(master)
        self.spark = builder.getOrCreate()

    def read_csv(self, path: str, header: bool = True, infer_schema: bool = True) -> DataFrame:
        """Read a CSV file into a DataFrame."""
        return self.spark.read.csv(path, header=header, inferSchema=infer_schema)

    def read_json(self, path: str, multiline: bool = False) -> DataFrame:
        """Read a JSON file into a DataFrame."""
        return self.spark.read.json(path, multiLine=multiline)

    def sql(self, query: str):
        """Run a SQL query against registered temp views."""
        return self.spark.sql(query)

    def stop(self) -> None:
        """Stop the Spark session."""
        self.spark.stop()

def main() -> None:
    sm = SparkManager()
    print("Spark version:", sm.spark.version)
    sm.stop()

if __name__ == "__main__":
    main()
