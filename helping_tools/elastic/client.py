"""
Elasticsearch Client Module

This module provides a unified client interface that combines connection,
query building, and index management features for Elasticsearch.
"""

from typing import Dict, List, Optional, Any, Union, Generator, TypeVar, Iterator, cast
from .connection import ElasticConnection
from .query_builder import ElasticQueryBuilder
from .index_manager import ElasticIndexManager
from elasticsearch.exceptions import ElasticsearchException

# Type definition for self-reference
T = TypeVar('T', bound='ElasticClient')


class ElasticClient:
    """
    A unified Elasticsearch client that combines connection, query building,
    and index management functionality.
    
    This class serves as the main entry point for interacting with Elasticsearch,
    providing convenient methods for common operations.
    
    Attributes:
        connection (ElasticConnection): The underlying connection object.
        client: The Elasticsearch client instance.
        index_manager (ElasticIndexManager): Index management utilities.
    """
    
    def __init__(self, connection: ElasticConnection) -> None:
        """
        Initialize the Elasticsearch client.
        
        Args:
            connection (ElasticConnection): An initialized ElasticConnection instance.
        """
        self.connection = connection
        self.client = connection.get_client()
        self.index_manager = ElasticIndexManager(self.client)
    
    # ---- Document Operations ----
    
    def index_document(self, index_name: str, document: Dict[str, Any], 
                       doc_id: Optional[str] = None, refresh: bool = False) -> Dict[str, Any]:
        """
        Index a document in Elasticsearch.
        
        Args:
            index_name (str): Name of the index to store the document.
            document (Dict[str, Any]): The document to index.
            doc_id (str, optional): Document ID. Defaults to None (auto-generated).
            refresh (bool, optional): Whether to refresh the index after indexing. Defaults to False.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If document indexing fails.
        """
        try:
            return self.client.index(
                index=index_name, 
                body=document, 
                id=doc_id, 
                refresh=refresh
            )
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to index document: {str(e)}")
    
    def get_document(self, index_name: str, doc_id: str) -> Dict[str, Any]:
        """
        Get a document by ID.
        
        Args:
            index_name (str): Name of the index.
            doc_id (str): Document ID.
            
        Returns:
            Dict[str, Any]: The document.
            
        Raises:
            ElasticsearchException: If document retrieval fails.
        """
        try:
            return self.client.get(index=index_name, id=doc_id)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to get document with ID '{doc_id}': {str(e)}")
    
    def update_document(self, index_name: str, doc_id: str, 
                       update_body: Dict[str, Any], refresh: bool = False) -> Dict[str, Any]:
        """
        Update a document by ID.
        
        Args:
            index_name (str): Name of the index.
            doc_id (str): Document ID.
            update_body (Dict[str, Any]): Update body (must contain 'doc', 'script', or other valid update fields).
            refresh (bool, optional): Whether to refresh the index after updating. Defaults to False.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If document update fails.
        """
        try:
            return self.client.update(
                index=index_name, 
                id=doc_id, 
                body=update_body, 
                refresh=refresh
            )
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to update document with ID '{doc_id}': {str(e)}")
    
    def delete_document(self, index_name: str, doc_id: str, refresh: bool = False) -> Dict[str, Any]:
        """
        Delete a document by ID.
        
        Args:
            index_name (str): Name of the index.
            doc_id (str): Document ID.
            refresh (bool, optional): Whether to refresh the index after deletion. Defaults to False.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If document deletion fails.
        """
        try:
            return self.client.delete(
                index=index_name, 
                id=doc_id, 
                refresh=refresh
            )
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to delete document with ID '{doc_id}': {str(e)}")
    
    def bulk(self, operations: List[Dict[str, Any]], refresh: bool = False) -> Dict[str, Any]:
        """
        Execute bulk operations.
        
        Args:
            operations (List[Dict[str, Any]]): List of bulk operations.
            refresh (bool, optional): Whether to refresh the index after bulk operation. Defaults to False.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If bulk operation fails.
        """
        try:
            return self.client.bulk(body=operations, refresh=refresh)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to execute bulk operation: {str(e)}")
    
    # ---- Search Operations ----
    
    def search(self, index_name: str, query: Union[Dict[str, Any], ElasticQueryBuilder]) -> Dict[str, Any]:
        """
        Search documents in an index.
        
        Args:
            index_name (str): Name of the index to search.
            query (Union[Dict[str, Any], ElasticQueryBuilder]): Search query or query builder.
            
        Returns:
            Dict[str, Any]: Search results.
            
        Raises:
            ElasticsearchException: If search fails.
        """
        try:
            query_body = query.build() if isinstance(query, ElasticQueryBuilder) else query
            return self.client.search(index=index_name, body=query_body)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Search failed: {str(e)}")
    
    def count(self, index_name: str, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents in an index.
        
        Args:
            index_name (str): Name of the index.
            query (Dict[str, Any], optional): Query to filter documents. Defaults to None.
            
        Returns:
            int: Document count.
            
        Raises:
            ElasticsearchException: If count operation fails.
        """
        try:
            result = self.client.count(index=index_name, body={"query": query} if query else None)
            return result.get("count", 0)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Count operation failed: {str(e)}")
    
    def scan(self, index_name: str, query: Optional[Dict[str, Any]] = None, 
            scroll: str = "1m", size: int = 1000) -> Iterator[Dict[str, Any]]:
        """
        Scan and scroll through large result sets.
        
        Args:
            index_name (str): Name of the index.
            query (Dict[str, Any], optional): Search query. Defaults to None.
            scroll (str, optional): Scroll timeout. Defaults to "1m".
            size (int, optional): Batch size. Defaults to 1000.
            
        Yields:
            Iterator[Dict[str, Any]]: Documents one by one.
            
        Raises:
            ElasticsearchException: If scan operation fails.
        """
        try:
            search_body = {}
            if query:
                search_body["query"] = query
                
            result = self.client.search(
                index=index_name,
                body=search_body,
                scroll=scroll,
                size=size
            )
            
            scroll_id = result.get("_scroll_id")
            hits = result.get("hits", {}).get("hits", [])
            
            # Yield initial results
            for hit in hits:
                yield hit
                
            # Continue scrolling until no more hits
            while scroll_id and hits:
                result = self.client.scroll(scroll_id=scroll_id, scroll=scroll)
                scroll_id = result.get("_scroll_id")
                hits = result.get("hits", {}).get("hits", [])
                
                for hit in hits:
                    yield hit
                    
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Scan operation failed: {str(e)}")
        finally:
            # Clean up scroll
            if scroll_id:
                try:
                    self.client.clear_scroll(scroll_id=scroll_id)
                except:
                    pass
    
    # ---- Update/Delete By Query ----
    
    def update_by_query(self, index_name: str, query_body: Dict[str, Any], refresh: bool = False) -> Dict[str, Any]:
        """
        Update documents by query.
        
        Args:
            index_name (str): Name of the index.
            query_body (Dict[str, Any]): Update by query body.
            refresh (bool, optional): Whether to refresh the index. Defaults to False.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If update by query fails.
        """
        try:
            return self.client.update_by_query(
                index=index_name,
                body=query_body,
                refresh=refresh
            )
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Update by query failed: {str(e)}")
    
    def delete_by_query(self, index_name: str, query_body: Dict[str, Any], refresh: bool = False) -> Dict[str, Any]:
        """
        Delete documents by query.
        
        Args:
            index_name (str): Name of the index.
            query_body (Dict[str, Any]): Delete by query body.
            refresh (bool, optional): Whether to refresh the index. Defaults to False.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If delete by query fails.
        """
        try:
            return self.client.delete_by_query(
                index=index_name,
                body=query_body,
                refresh=refresh
            )
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Delete by query failed: {str(e)}")
    
    # ---- Convenience Methods ----
    
    def create_query_builder(self: T) -> ElasticQueryBuilder:
        """
        Create a new query builder instance.
        
        Returns:
            ElasticQueryBuilder: A new query builder instance.
        """
        return ElasticQueryBuilder()
    
    def close(self) -> None:
        """
        Close the client and connection.
        """
        self.connection.close()


# Example usage:
# connection = ElasticConnection(hosts=["http://localhost:9200"])
# connection.connect()
# client = ElasticClient(connection)
# index_manager = client.index_manager
