"""
Kafka Connection Module

This module provides a generic KafkaConnection class for establishing and managing 
connections to Apache Kafka clusters.
"""

from typing import Dict, List, Optional, Any
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import KafkaError


class KafkaConnection:
    """
    A generic Kafka connection class that handles connection to Kafka brokers.
    
    This class provides a unified interface to connect to Kafka clusters and
    can be used as the foundation for both consumer and publisher operations.
    It encapsulates common connection parameters and configuration options,
    providing methods to create consumers, producers, and perform administrative tasks.
    
    Attributes:
        bootstrap_servers (List[str]): List of Kafka broker addresses.
        client_id (str): Identifier for this client.
        security_protocol (str): Protocol used to communicate with brokers.
        ssl_config (Dict): SSL configuration if security protocol requires SSL.
        sasl_config (Dict): SASL configuration for authentication if needed.
        producer (KafkaProducer): Kafka producer instance.
        consumer (KafkaConsumer): Kafka consumer instance.
        admin_client (KafkaAdminClient): Kafka admin client instance.
    """
    
    def __init__(
        self,
        bootstrap_servers: List[str],
        client_id: str = "kafka-python-client",
        security_protocol: str = "PLAINTEXT",
        ssl_config: Optional[Dict[str, Any]] = None,
        sasl_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a Kafka connection with the specified parameters.
        
        Args:
            bootstrap_servers (List[str]): List of Kafka broker addresses in the format 'host:port'.
            client_id (str, optional): Identifier for this client. Defaults to "kafka-python-client".
            security_protocol (str, optional): Protocol used to communicate with brokers.
                                              Defaults to "PLAINTEXT".
            ssl_config (Dict, optional): SSL configuration if security protocol requires SSL.
                                        Should contain relevant SSL parameters. Defaults to None.
            sasl_config (Dict, optional): SASL configuration for authentication if needed.
                                         Should contain mechanism, username and password. Defaults to None.
        """
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self.security_protocol = security_protocol
        self.ssl_config = ssl_config or {}
        self.sasl_config = sasl_config or {}
        
        # These will be initialized when needed
        self.producer = None
        self.consumer = None
        self.admin_client = None
        
        # Basic connection configuration
        self.config = {
            'bootstrap_servers': self.bootstrap_servers,
            'client_id': self.client_id,
            'security_protocol': self.security_protocol
        }
        
        # Add SSL configuration if provided
        if self.ssl_config:
            self.config.update(self.ssl_config)
            
        # Add SASL configuration if provided
        if self.sasl_config:
            self.config.update(self.sasl_config)

    def create_producer(self, **kwargs) -> KafkaProducer:
        """
        Create and return a Kafka producer instance.
        
        Args:
            **kwargs: Additional configuration parameters for the KafkaProducer.
                    These will override any conflicting parameters from the base configuration.
                    
        Returns:
            KafkaProducer: Configured Kafka producer instance.
            
        Raises:
            KafkaError: If there's an error creating the producer.
        """
        try:
            producer_config = self.config.copy()
            producer_config.update(kwargs)
            self.producer = KafkaProducer(**producer_config)
            return self.producer
        except KafkaError as e:
            raise KafkaError(f"Failed to create Kafka producer: {str(e)}")

    def create_consumer(self, topics: List[str] = None, group_id: str = None, **kwargs) -> KafkaConsumer:
        """
        Create and return a Kafka consumer instance.
        
        Args:
            topics (List[str], optional): List of topics to subscribe to. Defaults to None.
            group_id (str, optional): Consumer group ID. Defaults to None.
            **kwargs: Additional configuration parameters for the KafkaConsumer.
                    These will override any conflicting parameters from the base configuration.
                    
        Returns:
            KafkaConsumer: Configured Kafka consumer instance.
            
        Raises:
            KafkaError: If there's an error creating the consumer.
        """
        try:
            consumer_config = self.config.copy()
            if group_id:
                consumer_config['group_id'] = group_id
                
            consumer_config.update(kwargs)
            
            if topics:
                self.consumer = KafkaConsumer(*topics, **consumer_config)
            else:
                self.consumer = KafkaConsumer(**consumer_config)
                
            return self.consumer
        except KafkaError as e:
            raise KafkaError(f"Failed to create Kafka consumer: {str(e)}")

    def create_admin_client(self, **kwargs) -> KafkaAdminClient:
        """
        Create and return a Kafka admin client instance.
        
        Args:
            **kwargs: Additional configuration parameters for the KafkaAdminClient.
                    These will override any conflicting parameters from the base configuration.
                    
        Returns:
            KafkaAdminClient: Configured Kafka admin client instance.
            
        Raises:
            KafkaError: If there's an error creating the admin client.
        """
        try:
            admin_config = self.config.copy()
            admin_config.update(kwargs)
            self.admin_client = KafkaAdminClient(**admin_config)
            return self.admin_client
        except KafkaError as e:
            raise KafkaError(f"Failed to create Kafka admin client: {str(e)}")

    def create_topic(self, topic_name: str, num_partitions: int = 1, 
                    replication_factor: int = 1) -> None:
        """
        Create a new Kafka topic.
        
        Args:
            topic_name (str): Name of the topic to create.
            num_partitions (int, optional): Number of partitions for the topic. Defaults to 1.
            replication_factor (int, optional): Replication factor for the topic. Defaults to 1.
            
        Raises:
            KafkaError: If there's an error creating the topic.
        """
        if not self.admin_client:
            self.create_admin_client()
            
        try:
            topic = NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
            self.admin_client.create_topics([topic])
        except KafkaError as e:
            raise KafkaError(f"Failed to create topic '{topic_name}': {str(e)}")

    def close(self) -> None:
        """
        Close all open Kafka connections (producer, consumer, admin client).
        
        This method should be called when the connection is no longer needed
        to free up resources and ensure proper cleanup.
        """
        if self.producer:
            self.producer.close()
            self.producer = None
            
        if self.consumer:
            self.consumer.close()
            self.consumer = None
            
        if self.admin_client:
            self.admin_client.close()
            self.admin_client = None