"""
Data.gov Configuration
Configuration settings for Data.gov API integration.
"""

import os
from typing import List
from src.config.base_config import BaseConfig


class DataGovConfig(BaseConfig):
    """Configuration for Data.gov integration."""
    
    # API Keys
    CENSUS_API_KEY: str = os.getenv('CENSUS_API_KEY', '')
    
    # API Base URLs
    CENSUS_BASE_URL: str = "http://api.census.gov/data/timeseries/intltrade/imports/"
    USDA_BASE_URL: str = "https://www.ers.usda.gov/data-products/"
    USITC_BASE_URL: str = "https://data.usitc.gov/"
    EPI_BASE_URL: str = "https://epi.yale.edu/"
    
    # Rate limiting
    CENSUS_RATE_LIMIT_PER_DAY: int = 10000
    CENSUS_RATE_LIMIT_PER_MINUTE: int = 100
    
    # Data sources
    ENABLED_DATA_SOURCES: List[str] = ["census", "usda", "usitc", "epi"]
    
    # Storage
    VECTOR_DB_COLLECTION: str = "datagov_embeddings"
    KNOWLEDGE_GRAPH_LABEL: str = "DataGovEntity"
    
    # Analysis settings
    DEFAULT_COUNTRIES: List[str] = ["CHN", "RUS"]
    DEFAULT_FORECAST_PERIOD: str = "1Y"
    DEFAULT_TIME_PERIOD: str = "latest"
    
    # Model settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    NLP_MODEL: str = "gpt2"
    
    # Cache settings
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    CACHE_ENABLED: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Error handling
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: int = 5
    
    # Performance
    REQUEST_TIMEOUT_SECONDS: int = 30
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Data quality
    MIN_DATA_QUALITY_SCORE: float = 0.7
    DATA_VALIDATION_ENABLED: bool = True
    
    # Monitoring
    METRICS_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL_SECONDS: int = 300  # 5 minutes
    
    # Security
    API_KEY_ENCRYPTION_ENABLED: bool = True
    REQUEST_SIGNING_ENABLED: bool = False
    
    # Development/Testing
    MOCK_DATA_ENABLED: bool = True  # Set to False in production
    DEBUG_MODE: bool = False
    
    @classmethod
    def get_api_key(cls, api_name: str) -> str:
        """Get API key for specified service."""
        if api_name.lower() == "census":
            return cls.CENSUS_API_KEY
        else:
            return ""
    
    @classmethod
    def get_base_url(cls, api_name: str) -> str:
        """Get base URL for specified service."""
        url_mapping = {
            "census": cls.CENSUS_BASE_URL,
            "usda": cls.USDA_BASE_URL,
            "usitc": cls.USITC_BASE_URL,
            "epi": cls.EPI_BASE_URL
        }
        return url_mapping.get(api_name.lower(), "")
    
    @classmethod
    def is_data_source_enabled(cls, source_name: str) -> bool:
        """Check if a data source is enabled."""
        return source_name.lower() in [s.lower() for s in cls.ENABLED_DATA_SOURCES]
    
    @classmethod
    def get_rate_limit(cls, api_name: str) -> dict:
        """Get rate limit settings for specified API."""
        if api_name.lower() == "census":
            return {
                "requests_per_day": cls.CENSUS_RATE_LIMIT_PER_DAY,
                "requests_per_minute": cls.CENSUS_RATE_LIMIT_PER_MINUTE
            }
        else:
            return {
                "requests_per_day": 1000,
                "requests_per_minute": 10
            }
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Check required API keys
        if not cls.CENSUS_API_KEY and "census" in cls.ENABLED_DATA_SOURCES:
            issues.append("Census API key is required when Census data source is enabled")
        
        # Check rate limits
        if cls.CENSUS_RATE_LIMIT_PER_DAY <= 0:
            issues.append("Census rate limit per day must be positive")
        
        if cls.CENSUS_RATE_LIMIT_PER_MINUTE <= 0:
            issues.append("Census rate limit per minute must be positive")
        
        # Check timeouts
        if cls.REQUEST_TIMEOUT_SECONDS <= 0:
            issues.append("Request timeout must be positive")
        
        # Check data quality threshold
        if cls.MIN_DATA_QUALITY_SCORE < 0 or cls.MIN_DATA_QUALITY_SCORE > 1:
            issues.append("Minimum data quality score must be between 0 and 1")
        
        # Check retry settings
        if cls.MAX_RETRIES < 0:
            issues.append("Max retries must be non-negative")
        
        if cls.RETRY_DELAY_SECONDS < 0:
            issues.append("Retry delay must be non-negative")
        
        return issues
    
    @classmethod
    def get_config_summary(cls) -> dict:
        """Get a summary of the current configuration."""
        return {
            "api_keys_configured": {
                "census": bool(cls.CENSUS_API_KEY)
            },
            "enabled_data_sources": cls.ENABLED_DATA_SOURCES,
            "rate_limits": {
                "census": cls.get_rate_limit("census")
            },
            "storage": {
                "vector_db_collection": cls.VECTOR_DB_COLLECTION,
                "knowledge_graph_label": cls.KNOWLEDGE_GRAPH_LABEL
            },
            "analysis": {
                "default_countries": cls.DEFAULT_COUNTRIES,
                "default_forecast_period": cls.DEFAULT_FORECAST_PERIOD,
                "default_time_period": cls.DEFAULT_TIME_PERIOD
            },
            "performance": {
                "request_timeout": cls.REQUEST_TIMEOUT_SECONDS,
                "max_concurrent_requests": cls.MAX_CONCURRENT_REQUESTS,
                "cache_enabled": cls.CACHE_ENABLED,
                "cache_ttl": cls.CACHE_TTL_SECONDS
            },
            "development": {
                "mock_data_enabled": cls.MOCK_DATA_ENABLED,
                "debug_mode": cls.DEBUG_MODE
            },
            "validation_issues": cls.validate_config()
        }
