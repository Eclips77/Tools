
# Database Utilities & Infrastructure Components

A comprehensive collection of production-grade Python utilities and infrastructure components designed for enterprise-level database operations and system integration. This project provides battle-tested, modular solutions for common database patterns, messaging systems, API development, and data processing workflows.

## 🎯 Project Overview

This repository contains **31 specialized modules** organized into cohesive packages, each addressing critical aspects of modern application development. Every module is designed with production requirements in mind, featuring proper error handling, logging, configuration management, and comprehensive testing.

## 📋 Module Categories

### 🗄️ Database Operations (`databases/`)
- **MongoDB Client** - Advanced MongoDB operations with connection pooling and aggregation support
- **SQL Manager** - SQLAlchemy-based ORM with migration support and query optimization
- **CRUD Operations** - Generic CRUD patterns with validation and error handling
- **Elasticsearch Client** - Full-text search and analytics with index management
- **Redis Cache** - Distributed caching with pub/sub messaging capabilities
- **File Storage** - Local file operations with metadata tracking
- **S3 Integration** - AWS S3 operations with multipart upload and lifecycle management

### 📨 Messaging & Communication (`messaging/`)
- **Kafka Producer/Consumer** - High-throughput message streaming with error recovery
- **RabbitMQ Client** - Message queuing with routing and dead letter handling
- **WebSocket Server** - Real-time bidirectional communication
- **Event Bus** - In-memory event system with subscription management
- **Task Queue** - Asynchronous job processing with priority scheduling

### 🌐 API & Web Services (`api/`)
- **FastAPI Server** - High-performance REST API with automatic documentation
- **HTTP Client** - Resilient HTTP client with retry logic and circuit breaker
- **JWT Authentication** - Token-based security with refresh token support
- **Rate Limiter** - API throttling with multiple strategies (token bucket, sliding window)
- **Middleware Components** - Request/response processing with logging and metrics

### 🛠️ Core Utilities (`utils/`)
- **Advanced Logger** - Structured logging with multiple outputs and log rotation
- **Configuration Manager** - Environment-aware config with validation and hot-reload
- **TTL Cache** - Time-based caching with LRU eviction policies
- **Encryption Service** - AES encryption with key management and secure storage
- **Data Validator** - Schema validation with custom rules and error reporting

### 📊 Data Processing (`data_processing/`)
- **Data Cleaner** - ETL operations with data quality checks and profiling
- **Data Transformer** - Format conversion and data normalization pipelines
- **Serialization Engine** - Multi-format serialization (JSON, XML, Avro, Parquet)
- **Metrics Collector** - Performance monitoring with custom metric aggregation
- **Job Runner** - Batch processing framework with dependency management

### ⏰ Scheduling & Monitoring (`scheduling_monitoring/`)
- **Task Scheduler** - Cron-like scheduling with distributed coordination
- **Health Check System** - Service monitoring with alerting and dashboards
- **File Watchdog** - Real-time file system monitoring with event processing

### ⚡ Big Data Processing (`spark/`)
- **Spark Manager** - PySpark integration with cluster management and optimization

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker (for backing services)
- pip or poetry for dependency management

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd db-utils

# Install dependencies
pip install -r requirements.txt

# Or using poetry
poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Quick Start Examples
```bash
# Database operations
python databases/mongo_client.py

# Start API server
python api/api_server.py

# Run data processing job
python data_processing/job_runner.py

# Monitor system health
python scheduling_monitoring/health_check.py
```

## 🏗️ Architecture & Design Principles

- **Modular Design**: Each component is self-contained and independently testable
- **Configuration-Driven**: All modules support environment-based configuration
- **Production-Ready**: Comprehensive error handling, logging, and monitoring
- **Scalable**: Designed for horizontal scaling and high-throughput scenarios
- **Extensible**: Clear interfaces for custom implementations and plugins

## 📋 Infrastructure Requirements

Some modules require external services. Use the provided Docker Compose file for local development:

```bash
docker-compose up -d  # Starts MongoDB, Redis, Kafka, Elasticsearch
```

**Required Services by Module:**
- MongoDB: `databases/mongo_client.py`
- Redis: `databases/redis_cache.py`, `utils/cache.py`
- Kafka: `messaging/kafka_client.py`
- Elasticsearch: `databases/elasticsearch_client.py`
- PostgreSQL: `databases/sql_manager.py`

## 🧪 Testing & Quality Assurance

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Code quality checks
flake8 .
mypy .
black --check .
```

## 📊 Performance & Monitoring

Each module includes built-in metrics collection and performance monitoring. Access metrics via:
- Prometheus endpoints (when enabled)
- CloudWatch integration (AWS environments)
- Custom metric collectors

## 🤝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and coding standards.

