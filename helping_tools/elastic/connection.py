"""
Elasticsearch Connection Module

This module provides a generic ElasticConnection class for establishing and managing 
connections to Elasticsearch clusters.
"""

from typing import Dict, List, Optional, Any, Union, Tuple
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ElasticsearchException


class ElasticConnection:
    """
    A generic Elasticsearch connection class that handles connection to Elasticsearch clusters.
    
    This class provides a unified interface to connect to Elasticsearch and
    can be used as the foundation for various Elasticsearch operations.
    It encapsulates common connection parameters and configuration options.
    
    Attributes:
        hosts (List[str]): List of Elasticsearch hosts.
        client (Elasticsearch): Elasticsearch client instance.
        is_connected (bool): Connection status flag.
        settings (Dict): Connection settings.
    """
    
    def __init__(
        self,
        hosts: Union[str, List[str]],
        api_key: Optional[Tuple[str, str]] = None,
        basic_auth: Optional[Tuple[str, str]] = None,
        cloud_id: Optional[str] = None,
        use_ssl: bool = True,
        verify_certs: bool = True,
        ca_certs: Optional[str] = None,
        client_cert: Optional[str] = None,
        client_key: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
        retry_on_timeout: bool = True,
        **kwargs: Any
    ) -> None:
        """
        Initialize an Elasticsearch connection with the specified parameters.
        
        Args:
            hosts (Union[str, List[str]]): Single host or list of Elasticsearch hosts.
            api_key (Tuple[str, str], optional): API key as a tuple of (id, secret). Defaults to None.
            basic_auth (Tuple[str, str], optional): Basic auth as a tuple of (username, password). Defaults to None.
            cloud_id (str, optional): Elastic Cloud ID. Defaults to None.
            use_ssl (bool, optional): Whether to use SSL for connections. Defaults to True.
            verify_certs (bool, optional): Whether to verify SSL certificates. Defaults to True.
            ca_certs (str, optional): Path to CA certificates. Defaults to None.
            client_cert (str, optional): Path to client certificate. Defaults to None.
            client_key (str, optional): Path to client key. Defaults to None.
            timeout (int, optional): Connection timeout in seconds. Defaults to 60.
            max_retries (int, optional): Maximum number of retries. Defaults to 3.
            retry_on_timeout (bool, optional): Whether to retry on timeout. Defaults to True.
            **kwargs: Additional arguments to pass to the Elasticsearch constructor.
        """
        self.hosts: List[str] = hosts if isinstance(hosts, list) else [hosts]
        self.is_connected: bool = False
        self.client: Optional[Elasticsearch] = None
        
        # Build connection settings
        self.settings: Dict[str, Any] = {
            'hosts': self.hosts,
            'timeout': timeout,
            'max_retries': max_retries,
            'retry_on_timeout': retry_on_timeout,
        }
        
        # Authentication settings
        if api_key:
            self.settings['api_key'] = api_key
        
        if basic_auth:
            self.settings['basic_auth'] = basic_auth
            
        if cloud_id:
            self.settings['cloud_id'] = cloud_id
            
        # SSL settings
        if use_ssl:
            self.settings.update({
                'use_ssl': use_ssl,
                'verify_certs': verify_certs,
            })
            
            if ca_certs:
                self.settings['ca_certs'] = ca_certs
                
            if client_cert:
                self.settings['client_cert'] = client_cert
                
            if client_key:
                self.settings['client_key'] = client_key
                
        # Add any additional settings
        self.settings.update(kwargs)
        
    def connect(self) -> 'ElasticConnection':
        """
        Establish connection to the Elasticsearch cluster.
        
        Returns:
            ElasticConnection: Self reference for method chaining.
            
        Raises:
            ElasticsearchException: If connection fails.
        """
        try:
            self.client = Elasticsearch(**self.settings)
            self.is_connected = self.client.ping()
            
            if not self.is_connected:
                raise ElasticsearchException("Failed to connect to Elasticsearch: ping returned false")
                
            return self
            
        except ElasticsearchException as e:
            self.is_connected = False
            raise ElasticsearchException(f"Failed to connect to Elasticsearch: {str(e)}")
            
    def get_client(self) -> Elasticsearch:
        """
        Get the Elasticsearch client instance.
        
        Returns:
            Elasticsearch: The Elasticsearch client.
            
        Raises:
            ElasticsearchException: If not connected.
        """
        if not self.is_connected or not self.client:
            raise ElasticsearchException("Not connected to Elasticsearch. Call connect() first.")
            
        return self.client
        
    def close(self) -> None:
        """
        Close the connection to Elasticsearch.
        
        This method should be called when the connection is no longer needed
        to free up resources and ensure proper cleanup.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.is_connected = False
            
    def info(self) -> Dict[str, Any]:
        """
        Get information about the Elasticsearch cluster.
        
        Returns:
            Dict[str, Any]: Cluster information.
            
        Raises:
            ElasticsearchException: If not connected.
        """
        client = self.get_client()
        try:
            return client.info()
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to get cluster info: {str(e)}")
            
    def health(self) -> Dict[str, Any]:
        """
        Get health information about the Elasticsearch cluster.
        
        Returns:
            Dict[str, Any]: Cluster health information.
            
        Raises:
            ElasticsearchException: If not connected.
        """
        client = self.get_client()
        try:
            return client.cluster.health()
        except ElasticsearchException as e:
            raise ElasticsearchException(f"Failed to get cluster health: {str(e)}")
            
    def __enter__(self) -> 'ElasticConnection':
        """
        Context manager enter method.
        
        Returns:
            ElasticConnection: Self reference.
        """
        if not self.is_connected:
            self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit method.
        
        Args:
            exc_type: Exception type if an exception was raised.
            exc_val: Exception value if an exception was raised.
            exc_tb: Exception traceback if an exception was raised.
        """
        self.close()
