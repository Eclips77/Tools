"""
MongoDB Collection Manager Module

This module provides utilities for managing MongoDB collections,
including collection creation, indexing, and schema validation.
"""

from typing import Dict, List, Optional, Any, Union, Callable
from pymongo.collection import Collection
from pymongo.errors import OperationFailure


class MongoCollectionManager:
    """
    A simple class for managing MongoDB collections.
    
    This class provides methods to create and manage collections,
    including creating indexes and setting up validation rules.
    
    Attributes:
        collection (Collection): The MongoDB collection being managed.
    """
    
    def __init__(self, collection: Collection) -> None:
        """
        Initialize with a MongoDB collection.
        
        Args:
            collection: MongoDB collection to manage.
        """
        self.collection = collection
    
    def create_index(self, keys: Union[str, List[tuple]], unique: bool = False, 
                   sparse: bool = False, background: bool = True, **kwargs: Any) -> str:
        """
        Create an index on the collection.
        
        Args:
            keys: Field(s) to index. Can be a string or list of (field, direction) tuples.
            unique: Whether the index enforces uniqueness. Defaults to False.
            sparse: Whether the index is sparse (only includes documents with field). Defaults to False.
            background: Whether the index should be created in the background. Defaults to True.
            **kwargs: Additional index options.
            
        Returns:
            str: Name of the created index.
            
        Raises:
            OperationFailure: If index creation fails.
        """
        try:
            return self.collection.create_index(keys, unique=unique, sparse=sparse, 
                                              background=background, **kwargs)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to create index: {str(e)}")
    
    def drop_index(self, index_name: str) -> None:
        """
        Drop an index from the collection.
        
        Args:
            index_name: Name of the index to drop.
            
        Raises:
            OperationFailure: If index drop fails.
        """
        try:
            self.collection.drop_index(index_name)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to drop index: {str(e)}")
    
    def list_indexes(self) -> List[Dict[str, Any]]:
        """
        List all indexes on the collection.
        
        Returns:
            List[Dict[str, Any]]: List of index information.
        """
        return list(self.collection.list_indexes())
    
    def set_validation(self, validation_rules: Dict[str, Any], 
                      validation_level: str = 'strict',
                      validation_action: str = 'error') -> None:
        """
        Set document validation rules for the collection.
        
        Args:
            validation_rules: MongoDB validation rules.
            validation_level: Validation level ('strict', 'moderate', 'off'). Defaults to 'strict'.
            validation_action: Validation action ('error', 'warn'). Defaults to 'error'.
            
        Raises:
            OperationFailure: If setting validation fails.
        """
        try:
            db = self.collection.database
            db.command({
                'collMod': self.collection.name,
                'validator': validation_rules,
                'validationLevel': validation_level,
                'validationAction': validation_action
            })
        except OperationFailure as e:
            raise OperationFailure(f"Failed to set validation rules: {str(e)}")
    
    def get_validation_info(self) -> Dict[str, Any]:
        """
        Get validation information for the collection.
        
        Returns:
            Dict[str, Any]: Collection validation information.
            
        Raises:
            OperationFailure: If getting validation info fails.
        """
        try:
            db = self.collection.database
            result = db.command({'listCollections': 1, 'filter': {'name': self.collection.name}})
            for collection_info in result['cursor']['firstBatch']:
                return collection_info.get('options', {})
            return {}
        except OperationFailure as e:
            raise OperationFailure(f"Failed to get validation info: {str(e)}")
    
    def estimated_document_count(self) -> int:
        """
        Get estimated document count for the collection.
        
        Returns:
            int: Estimated number of documents.
        """
        return self.collection.estimated_document_count()
    
    def count_documents(self, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents matching the filter.
        
        Args:
            filter_dict: Filter criteria. Defaults to None (all documents).
            
        Returns:
            int: Number of matching documents.
        """
        return self.collection.count_documents(filter_dict or {})
    
    def rename(self, new_name: str) -> None:
        """
        Rename the collection.
        
        Args:
            new_name: New name for the collection.
            
        Raises:
            OperationFailure: If renaming fails.
        """
        try:
            self.collection.rename(new_name)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to rename collection: {str(e)}")
    
    def drop(self) -> None:
        """
        Drop the collection.
        
        Raises:
            OperationFailure: If dropping fails.
        """
        try:
            self.collection.drop()
        except OperationFailure as e:
            raise OperationFailure(f"Failed to drop collection: {str(e)}")
