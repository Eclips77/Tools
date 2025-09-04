"""
Elasticsearch Index Manager Module

This module provides classes and utilities for managing Elasticsearch indices,
including creation, deletion, mappings, and templates.
"""

from typing import Dict, List, Optional, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from elasticsearch import Elasticsearch

from elasticsearch.exceptions import ElasticsearchException


class ElasticIndexManager:
    """
    A class for managing Elasticsearch indices.
    
    This class provides methods for creating, deleting, and managing indices,
    including setting mappings, templates, and other index settings.
    
    Attributes:
        client: The Elasticsearch client instance.
    """
    
    def __init__(self, client: 'Elasticsearch') -> None:
        """
        Initialize the index manager with an Elasticsearch client.
        
        Args:
            client: An initialized Elasticsearch client.
        """
        self.client: 'Elasticsearch' = client
        
    def create_index(self, index_name: str, settings: Optional[Dict[str, Any]] = None,
                    mappings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new Elasticsearch index.
        
        Args:
            index_name (str): Name of the index to create.
            settings (Dict[str, Any], optional): Index settings. Defaults to None.
            mappings (Dict[str, Any], optional): Index mappings. Defaults to None.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If index creation fails.
        """
        body = {}
        
        if settings:
            body["settings"] = settings
            
        if mappings:
            body["mappings"] = mappings
            
        try:
            return self.client.indices.create(index=index_name, body=body if body else None)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to create index '{index_name}': {str(e)}")
            
    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """
        Delete an Elasticsearch index.
        
        Args:
            index_name (str): Name of the index to delete.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If index deletion fails.
        """
        try:
            return self.client.indices.delete(index=index_name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to delete index '{index_name}': {str(e)}")
            
    def index_exists(self, index_name: str) -> bool:
        """
        Check if an index exists.
        
        Args:
            index_name (str): Name of the index to check.
            
        Returns:
            bool: True if the index exists, False otherwise.
        """
        try:
            return self.client.indices.exists(index=index_name)
        except ElasticsearchException:
            return False
            
    def update_mapping(self, index_name: str, mapping: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the mapping of an existing index.
        
        Args:
            index_name (str): Name of the index to update.
            mapping (Dict[str, Any]): The new mapping definition.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If mapping update fails.
        """
        try:
            return self.client.indices.put_mapping(index=index_name, body=mapping)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to update mapping for index '{index_name}': {str(e)}")
            
    def get_mapping(self, index_name: str) -> Dict[str, Any]:
        """
        Get the mapping of an index.
        
        Args:
            index_name (str): Name of the index.
            
        Returns:
            Dict[str, Any]: Index mapping.
            
        Raises:
            ElasticsearchException: If getting mapping fails.
        """
        try:
            return self.client.indices.get_mapping(index=index_name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to get mapping for index '{index_name}': {str(e)}")
            
    def get_settings(self, index_name: str) -> Dict[str, Any]:
        """
        Get the settings of an index.
        
        Args:
            index_name (str): Name of the index.
            
        Returns:
            Dict[str, Any]: Index settings.
            
        Raises:
            ElasticsearchException: If getting settings fails.
        """
        try:
            return self.client.indices.get_settings(index=index_name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to get settings for index '{index_name}': {str(e)}")
            
    def update_settings(self, index_name: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the settings of an existing index.
        
        Args:
            index_name (str): Name of the index to update.
            settings (Dict[str, Any]): The new settings.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If settings update fails.
        """
        try:
            return self.client.indices.put_settings(index=index_name, body=settings)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to update settings for index '{index_name}': {str(e)}")
            
    def create_alias(self, index_name: str, alias_name: str) -> Dict[str, Any]:
        """
        Create an alias for an index.
        
        Args:
            index_name (str): Name of the index.
            alias_name (str): Name of the alias.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If alias creation fails.
        """
        try:
            return self.client.indices.put_alias(index=index_name, name=alias_name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to create alias '{alias_name}' for index '{index_name}': {str(e)}")
            
    def delete_alias(self, index_name: str, alias_name: str) -> Dict[str, Any]:
        """
        Delete an alias from an index.
        
        Args:
            index_name (str): Name of the index.
            alias_name (str): Name of the alias.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If alias deletion fails.
        """
        try:
            return self.client.indices.delete_alias(index=index_name, name=alias_name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to delete alias '{alias_name}' from index '{index_name}': {str(e)}")
            
    def create_template(self, name: str, template_body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an index template.
        
        Args:
            name (str): Name of the template.
            template_body (Dict[str, Any]): Template definition.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If template creation fails.
        """
        try:
            return self.client.indices.put_template(name=name, body=template_body)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to create template '{name}': {str(e)}")
            
    def delete_template(self, name: str) -> Dict[str, Any]:
        """
        Delete an index template.
        
        Args:
            name (str): Name of the template to delete.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If template deletion fails.
        """
        try:
            return self.client.indices.delete_template(name=name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to delete template '{name}': {str(e)}")
            
    def refresh_index(self, index_name: str) -> Dict[str, Any]:
        """
        Refresh an index to make recent changes available for search.
        
        Args:
            index_name (str): Name of the index to refresh.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If index refresh fails.
        """
        try:
            return self.client.indices.refresh(index=index_name)
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to refresh index '{index_name}': {str(e)}")
            
    def clone_index(self, source_index: str, target_index: str, settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Clone an existing index to a new index.
        
        Args:
            source_index (str): Name of the source index.
            target_index (str): Name of the target index.
            settings (Dict[str, Any], optional): Settings for the target index. Defaults to None.
            
        Returns:
            Dict[str, Any]: Elasticsearch API response.
            
        Raises:
            ElasticsearchException: If index cloning fails.
        """
        body = {}
        
        if settings:
            body["settings"] = settings
            
        try:
            return self.client.indices.clone(index=source_index, target=target_index, body=body if body else None)
        except ElasticsearchException as e:
            raise ElasticsearchException(
                f"Failed to clone index '{source_index}' to '{target_index}': {str(e)}"
            )
