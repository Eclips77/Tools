"""
MongoDB Connection Module

This module provides a simple and clear MongoDB connection class.
"""

from typing import Dict, List, Optional, Any, Union
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError


class MongoConnection:
    """
    A simple MongoDB connection class.
    
    This class handles connecting to MongoDB servers or clusters and
    provides easy access to databases and collections.
    
    Attributes:
        client (MongoClient): The MongoDB client instance.
        database (Database): The currently selected MongoDB database.
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 27017,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_source: str = 'admin',
        database: Optional[str] = None,
        connection_string: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize a MongoDB connection.
        
        Args:
            host: MongoDB host. Defaults to 'localhost'.
            port: MongoDB port. Defaults to 27017.
            username: Authentication username. Defaults to None.
            password: Authentication password. Defaults to None.
            auth_source: Authentication database. Defaults to 'admin'.
            database: Default database to use. Defaults to None.
            connection_string: Full MongoDB connection string (if provided, other connection
                             parameters will be ignored). Defaults to None.
            **kwargs: Additional arguments to pass to MongoClient.
        """
        self.client = None
        self.database = None
        self._conn_params = {}
        
        # If a connection string is provided, use it directly
        if connection_string:
            self._conn_params['host'] = connection_string
        else:
            # Build connection parameters
            self._conn_params['host'] = host
            self._conn_params['port'] = port
            
            # Add authentication if credentials are provided
            if username and password:
                self._conn_params['username'] = username
                self._conn_params['password'] = password
                self._conn_params['authSource'] = auth_source
        
        # Add any additional connection parameters
        self._conn_params.update(kwargs)
        
        # Store the default database name
        self._database_name = database

    def connect(self) -> 'MongoConnection':
        """
        Establish connection to MongoDB.
        
        Returns:
            MongoConnection: Self reference for method chaining.
            
        Raises:
            ConnectionFailure: If connection to MongoDB fails.
        """
        try:
            self.client = MongoClient(**self._conn_params)
            
            # Test the connection
            self.client.admin.command('ismaster')
            
            # Connect to the specified database if provided
            if self._database_name:
                self.database = self.client[self._database_name]
                
            return self
            
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Failed to connect to MongoDB: {str(e)}")
        except ConfigurationError as e:
            raise ConfigurationError(f"MongoDB configuration error: {str(e)}")
    
    def get_database(self, database_name: str) -> Any:
        """
        Get a database by name.
        
        Args:
            database_name: Name of the database to get.
            
        Returns:
            Database: The MongoDB database object.
            
        Raises:
            ConnectionFailure: If not connected to MongoDB.
        """
        if not self.client:
            raise ConnectionFailure("Not connected to MongoDB. Call connect() first.")
            
        self.database = self.client[database_name]
        self._database_name = database_name
        return self.database
    
    def get_collection(self, collection_name: str, database_name: Optional[str] = None) -> Any:
        """
        Get a collection by name.
        
        Args:
            collection_name: Name of the collection to get.
            database_name: Name of the database containing the collection. 
                         If None, uses the current database. Defaults to None.
            
        Returns:
            Collection: The MongoDB collection object.
            
        Raises:
            ConnectionFailure: If not connected to MongoDB.
            ValueError: If no database is selected or provided.
        """
        if not self.client:
            raise ConnectionFailure("Not connected to MongoDB. Call connect() first.")
            
        if database_name:
            db = self.client[database_name]
        elif self.database:
            db = self.database
        else:
            raise ValueError("No database selected. Use get_database() first or provide database_name.")
            
        return db[collection_name]
    
    def close(self) -> None:
        """
        Close the connection to MongoDB.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.database = None
    
    def __enter__(self) -> 'MongoConnection':
        """
        Context manager enter method.
        
        Returns:
            MongoConnection: Self reference.
        """
        if not self.client:
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
