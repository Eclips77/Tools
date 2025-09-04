
from typing import Any, Dict, Iterable, List, Optional
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection

class MongoClientGeneric:
    """Generic MongoDB client wrapper for common CRUD and admin operations."""

    def __init__(self, uri: str, db_name: str) -> None:
        """
        Initialize the MongoDB client.
        Args:
            uri: MongoDB connection string.
            db_name: Target database name.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name: str) -> Collection:
        """Return a collection handle by name."""
        return self.db[name]

    def create_collection(self, name: str) -> Collection:
        """Create a collection if not exists and return it."""
        if name in self.db.list_collection_names():
            return self.db[name]
        return self.db.create_collection(name)

    def drop_collection(self, name: str) -> None:
        """Drop a collection by name."""
        self.db.drop_collection(name)

    def insert_one(self, coll: str, doc: Dict[str, Any]) -> str:
        """Insert a single document and return its ID."""
        return str(self.get_collection(coll).insert_one(doc).inserted_id)

    def insert_many(self, coll: str, docs: Iterable[Dict[str, Any]]) -> List[str]:
        """Insert many documents and return their IDs."""
        res = self.get_collection(coll).insert_many(list(docs))
        return [str(_id) for _id in res.inserted_ids]

    def find(self, coll: str, query: Dict[str, Any], limit: int = 0, sort: Optional[List[tuple]] = None) -> List[Dict[str, Any]]:
        """Find documents by query with optional limit and sort."""
        cursor = self.get_collection(coll).find(query)
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    def find_one(self, coll: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document matching the query."""
        return self.get_collection(coll).find_one(query)

    def update_one(self, coll: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update a single document and return modified count."""
        return self.get_collection(coll).update_one(query, update).modified_count

    def delete_one(self, coll: str, query: Dict[str, Any]) -> int:
        """Delete a single document and return deleted count."""
        return self.get_collection(coll).delete_one(query).deleted_count

    def aggregate(self, coll: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run an aggregation pipeline and return results."""
        return list(self.get_collection(coll).aggregate(pipeline))

    def create_index(self, coll: str, field: str, ascending: bool = True, unique: bool = False) -> str:
        """Create an index on a field and return its name."""
        direction = ASCENDING if ascending else DESCENDING
        return self.get_collection(coll).create_index([(field, direction)], unique=unique)

    def list_collections(self) -> List[str]:
        """List collection names in the database."""
        return self.db.list_collection_names()

def main() -> None:
    client = MongoClientGeneric("mongodb://localhost:27017", "testdb")
    client.create_collection("items")
    _id = client.insert_one("items", {"name": "example", "price": 10})
    print("Inserted:", _id)
    print("Collections:", client.list_collections())
    print("Find:", client.find("items", {}))

if __name__ == "__main__":
    main()
