"""
MongoDB Client Module

This module provides a unified client interface for MongoDB, combining
connection, query building, and collection management.
"""

from typing import Dict, List, Optional, Any, Union, TypeVar, cast, Iterator
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult

from .connection import MongoConnection
from .query_builder import MongoQueryBuilder
from .collection_manager import MongoCollectionManager


T = TypeVar('T', bound='MongoClient')


class MongoClient:
    """
    A unified MongoDB client that combines connection, query building,
    and collection management functionality.
    
    This class serves as the main entry point for interacting with MongoDB,
    providing convenient methods for common operations.
    
    Attributes:
        connection (MongoConnection): The MongoDB connection.
        default_db (str, optional): Name of the default database.
    """
    
    def __init__(self, connection: MongoConnection, default_db: Optional[str] = None) -> None:
        """
        Initialize the MongoDB client.
        
        Args:
            connection: An initialized MongoConnection instance.
            default_db: Default database name. Defaults to None.
        """
        self.connection = connection
        self.default_db = default_db
    
    def get_collection(self, collection_name: str, database_name: Optional[str] = None) -> Any:
        """
        Get a MongoDB collection.
        
        Args:
            collection_name: Name of the collection.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            Collection: MongoDB collection.
            
        Raises:
            ValueError: If no database specified and no default database set.
        """
        db_name = database_name or self.default_db
        if not db_name:
            raise ValueError("No database specified and no default database set")
            
        return self.connection.get_collection(collection_name, db_name)
    
    def create_query_builder(self) -> MongoQueryBuilder:
        """
        Create a new query builder instance.
        
        Returns:
            MongoQueryBuilder: A new query builder.
        """
        return MongoQueryBuilder()
    
    def create_collection_manager(self, collection_name: str, 
                                database_name: Optional[str] = None) -> MongoCollectionManager:
        """
        Create a collection manager for the specified collection.
        
        Args:
            collection_name: Name of the collection.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            MongoCollectionManager: Collection manager instance.
        """
        collection = self.get_collection(collection_name, database_name)
        return MongoCollectionManager(collection)
    
    # ---- Document Operations ----
    
    def find_one(self, collection_name: str, query: Union[Dict[str, Any], MongoQueryBuilder], 
                database_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Find a single document.
        
        Args:
            collection_name: Name of the collection.
            query: Query filter or MongoQueryBuilder instance.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            Optional[Dict[str, Any]]: Found document or None.
        """
        collection = self.get_collection(collection_name, database_name)
        
        if isinstance(query, MongoQueryBuilder):
            query_params = query.build()
            return collection.find_one(
                filter=query_params.get('filter', {}),
                projection=query_params.get('projection', None)
            )
        else:
            return collection.find_one(query)
    
    def find(self, collection_name: str, query: Union[Dict[str, Any], MongoQueryBuilder], 
            database_name: Optional[str] = None) -> Cursor:
        """
        Find documents matching a query.
        
        Args:
            collection_name: Name of the collection.
            query: Query filter or MongoQueryBuilder instance.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            Cursor: MongoDB cursor for query results.
        """
        collection = self.get_collection(collection_name, database_name)
        
        if isinstance(query, MongoQueryBuilder):
            query_params = query.build()
            return collection.find(
                filter=query_params.get('filter', {}),
                projection=query_params.get('projection', None),
                skip=query_params.get('skip', 0),
                limit=query_params.get('limit', 0),
                sort=query_params.get('sort', None)
            )
        else:
            return collection.find(query)
    
    def find_as_list(self, collection_name: str, query: Union[Dict[str, Any], MongoQueryBuilder], 
                   database_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Find documents and return as a list.
        
        Args:
            collection_name: Name of the collection.
            query: Query filter or MongoQueryBuilder instance.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            List[Dict[str, Any]]: List of documents.
        """
        cursor = self.find(collection_name, query, database_name)
        return list(cursor)
    
    def insert_one(self, collection_name: str, document: Dict[str, Any], 
                  database_name: Optional[str] = None) -> InsertOneResult:
        """
        Insert a single document.
        
        Args:
            collection_name: Name of the collection.
            document: Document to insert.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            InsertOneResult: Result of the insert operation.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.insert_one(document)
    
    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]], 
                  ordered: bool = True, database_name: Optional[str] = None) -> InsertManyResult:
        """
        Insert multiple documents.
        
        Args:
            collection_name: Name of the collection.
            documents: List of documents to insert.
            ordered: Whether to perform an ordered insert. Defaults to True.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            InsertManyResult: Result of the insert operation.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.insert_many(documents, ordered=ordered)
    
    def update_one(self, collection_name: str, filter_dict: Dict[str, Any], 
                 update_dict: Dict[str, Any], upsert: bool = False, 
                 database_name: Optional[str] = None) -> UpdateResult:
        """
        Update a single document.
        
        Args:
            collection_name: Name of the collection.
            filter_dict: Filter to identify the document to update.
            update_dict: Update operations to perform.
            upsert: Whether to perform an upsert. Defaults to False.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            UpdateResult: Result of the update operation.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.update_one(filter_dict, update_dict, upsert=upsert)
    
    def update_many(self, collection_name: str, filter_dict: Dict[str, Any], 
                  update_dict: Dict[str, Any], upsert: bool = False, 
                  database_name: Optional[str] = None) -> UpdateResult:
        """
        Update multiple documents.
        
        Args:
            collection_name: Name of the collection.
            filter_dict: Filter to identify documents to update.
            update_dict: Update operations to perform.
            upsert: Whether to perform an upsert. Defaults to False.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            UpdateResult: Result of the update operation.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.update_many(filter_dict, update_dict, upsert=upsert)
    
    def delete_one(self, collection_name: str, filter_dict: Dict[str, Any], 
                 database_name: Optional[str] = None) -> DeleteResult:
        """
        Delete a single document.
        
        Args:
            collection_name: Name of the collection.
            filter_dict: Filter to identify the document to delete.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            DeleteResult: Result of the delete operation.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.delete_one(filter_dict)
    
    def delete_many(self, collection_name: str, filter_dict: Dict[str, Any], 
                  database_name: Optional[str] = None) -> DeleteResult:
        """
        Delete multiple documents.
        
        Args:
            collection_name: Name of the collection.
            filter_dict: Filter to identify documents to delete.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            DeleteResult: Result of the delete operation.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.delete_many(filter_dict)
    
    def count_documents(self, collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, 
                       database_name: Optional[str] = None) -> int:
        """
        Count documents matching a filter.
        
        Args:
            collection_name: Name of the collection.
            filter_dict: Filter criteria. Defaults to None (all documents).
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            int: Number of matching documents.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.count_documents(filter_dict or {})
    
    def aggregate(self, collection_name: str, pipeline: List[Dict[str, Any]], 
                database_name: Optional[str] = None) -> Cursor:
        """
        Perform an aggregation.
        
        Args:
            collection_name: Name of the collection.
            pipeline: Aggregation pipeline stages.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            Cursor: MongoDB cursor for aggregation results.
        """
        collection = self.get_collection(collection_name, database_name)
        return collection.aggregate(pipeline)
    
    def aggregate_as_list(self, collection_name: str, pipeline: List[Dict[str, Any]], 
                        database_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform an aggregation and return results as a list.
        
        Args:
            collection_name: Name of the collection.
            pipeline: Aggregation pipeline stages.
            database_name: Name of the database. If None, uses default_db. Defaults to None.
            
        Returns:
            List[Dict[str, Any]]: List of aggregation results.
        """
        cursor = self.aggregate(collection_name, pipeline, database_name)
        return list(cursor)
    
    def close(self) -> None:
        """
        Close the MongoDB connection.
        """
        self.connection.close()
