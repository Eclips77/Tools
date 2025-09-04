
from typing import Any, Dict, List, Optional
from elasticsearch import Elasticsearch, helpers

class ElasticClient:
    """Generic Elasticsearch wrapper for indexing, searching, and admin ops."""

    def __init__(self, host: str = "http://localhost:9200") -> None:
        self.es = Elasticsearch(hosts=[host])

    def create_index(self, name: str, mapping: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create index with optional mapping/settings."""
        if self.es.indices.exists(index=name):
            return {"acknowledged": True, "message": "index exists"}
        return self.es.indices.create(index=name, body=mapping or {})

    def delete_index(self, name: str) -> Dict[str, Any]:
        """Delete index by name."""
        if self.es.indices.exists(index=name):
            return self.es.indices.delete(index=name)
        return {"acknowledged": True, "message": "index missing"}

    def index_doc(self, index: str, doc: Dict[str, Any], id: Optional[str] = None) -> Dict[str, Any]:
        """Index a single document."""
        return self.es.index(index=index, id=id, document=doc, refresh=True)

    def bulk_index(self, index: str, docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk index a list of documents."""
        actions = ({"_index": index, "_source": d} for d in docs)
        res = helpers.bulk(self.es, actions, refresh=True)
        return {"result": "ok", "items_indexed": res[0]}

    def search(self, index: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Run a search query and return hits."""
        return self.es.search(index=index, query=query)

    def get(self, index: str, id: str) -> Dict[str, Any]:
        """Get a document by ID."""
        return self.es.get(index=index, id=id)

    def update(self, index: str, id: str, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Partial update a document."""
        return self.es.update(index=index, id=id, doc={"doc": doc}, refresh=True)

    def delete(self, index: str, id: str) -> Dict[str, Any]:
        """Delete a document by ID."""
        return self.es.delete(index=index, id=id, refresh=True)

def main() -> None:
    client = ElasticClient()
    client.create_index("items")
    client.index_doc("items", {"name": "alpha"})
    print(client.search("items", {"match_all": {}}))

if __name__ == "__main__":
    main()
