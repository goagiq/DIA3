# Fetch Operations with Timeout and Error Handling - Best Practices Guide

## Overview

This guide explains the best practices for implementing robust fetch operations with comprehensive timeout and error handling to prevent infinite loops and provide graceful degradation.

## Problem Statement

The original implementation had several critical issues:

1. **Infinite Loops**: Fetch operations could run indefinitely without proper timeout handling
2. **No Error Classification**: All errors were treated the same way, leading to inappropriate retry strategies
3. **Resource Leaks**: No proper session management or connection pooling
4. **No Circuit Breaker**: Failed URLs would continue to be retried indefinitely
5. **No Fallback Strategy**: When one URL failed, there was no mechanism to try alternative sources

## Solution Implemented

### 1. Enhanced Fetch Service (`src/core/fetch_service.py`)

The enhanced fetch service implements the following best practices:

#### Key Features:
- **Configurable Timeouts**: Different timeout settings for different operations
- **Circuit Breaker Pattern**: Prevents cascading failures by temporarily blocking problematic URLs
- **Intelligent Retry Logic**: Exponential backoff with jitter for different error types
- **URL Blacklisting**: Temporarily blacklist consistently failing URLs
- **Resource Management**: Proper session management and connection pooling
- **Error Classification**: Different handling strategies for different error types

#### Configuration Options:
```python
@dataclass
class FetchConfig:
    timeout: float = 30.0                    # Total timeout per request
    max_retries: int = 3                     # Maximum retry attempts
    retry_delay: float = 1.0                 # Base delay between retries
    exponential_backoff: bool = True         # Use exponential backoff
    max_backoff: float = 60.0                # Maximum backoff delay
    circuit_breaker_threshold: int = 5       # Failures before opening circuit
    circuit_breaker_timeout: float = 300.0   # Circuit breaker recovery time
    user_agent: str = "DIA3-Fetch-Service/1.0"
    verify_ssl: bool = True
    max_content_length: int = 10 * 1024 * 1024  # 10MB limit
```

#### Error Types and Handling:
```python
class FetchErrorType(Enum):
    TIMEOUT = "timeout"              # Always retry with exponential backoff
    CONNECTION_ERROR = "connection_error"  # Always retry
    DNS_ERROR = "dns_error"          # Always retry
    SSL_ERROR = "ssl_error"          # Never retry
    RATE_LIMIT = "rate_limit"        # Retry with exponential backoff
    SERVER_ERROR = "server_error"    # Retry with limits
    CLIENT_ERROR = "client_error"    # Never retry
    UNKNOWN = "unknown"              # Retry with caution
```

#### Usage Examples:

**Basic URL Fetching:**
```python
from src.core.fetch_service import fetch_url_safe

# Fetch a single URL with automatic error handling
result = await fetch_url_safe("https://example.com")
if result.success:
    print(f"Content: {result.content}")
else:
    print(f"Error: {result.error_message}")
```

**Multiple URLs with Fallback:**
```python
from src.core.fetch_service import fetch_with_fallback_safe

# Try primary URL, fallback to alternatives
result = await fetch_with_fallback_safe(
    primary_url="https://primary-source.com",
    fallback_urls=[
        "https://backup-source-1.com",
        "https://backup-source-2.com"
    ]
)
```

**Multiple URLs Concurrently:**
```python
from src.core.fetch_service import fetch_multiple_urls_safe

# Fetch multiple URLs with rate limiting
urls = ["https://url1.com", "https://url2.com", "https://url3.com"]
results = await fetch_multiple_urls_safe(urls, max_concurrent=5)

for result in results:
    if result.success:
        print(f"Success: {result.url}")
    else:
        print(f"Failed: {result.url} - {result.error_message}")
```

### 2. Sequential Thinking Service (`src/core/sequential_thinking_service.py`)

The sequential thinking service provides robust analysis with proper timeout handling:

#### Key Features:
- **Step-by-Step Timeouts**: Each thinking step has its own timeout
- **Dependency Management**: Steps can depend on previous steps
- **Fallback Strategies**: Alternative approaches when steps fail
- **Resource Management**: Proper cleanup and memory management
- **Progress Tracking**: Detailed logging and statistics

#### Configuration Options:
```python
@dataclass
class SequentialThinkingConfig:
    max_total_time: float = 300.0        # 5 minutes total
    step_timeout: float = 60.0           # 1 minute per step
    max_concurrent_steps: int = 3
    enable_circuit_breaker: bool = True
    enable_fallback: bool = True
    max_retries_per_step: int = 2
    retry_delay: float = 1.0
    exponential_backoff: bool = True
    max_backoff: float = 30.0
    enable_caching: bool = True
    cache_duration: float = 3600.0       # 1 hour
```

#### Usage Example:
```python
from src.core.sequential_thinking_service import analyze_sequential_thinking_safe

# Perform sequential thinking analysis
result = await analyze_sequential_thinking_safe(
    scenario="Analyze market trends for Q4 2024",
    steps=5,
    iterations=10,
    urls=[
        "https://market-data-source.com",
        "https://economic-indicators.com"
    ]
)

if result.success:
    print(f"Analysis completed: {result.final_conclusion}")
    print(f"Steps completed: {len(result.steps_completed)}")
else:
    print(f"Analysis failed: {result.error_messages}")
```

## Best Practices Implementation

### 1. Timeout Configuration

**Recommended Timeout Settings:**
```python
# For different types of operations
FAST_OPERATIONS = 10.0      # Quick API calls
STANDARD_OPERATIONS = 30.0  # Regular web requests
SLOW_OPERATIONS = 120.0     # Large file downloads
ANALYSIS_OPERATIONS = 300.0 # Complex analysis tasks
```

### 2. Circuit Breaker Configuration

**Recommended Circuit Breaker Settings:**
```python
# For different types of services
RELIABLE_SERVICE = {
    "failure_threshold": 3,
    "recovery_timeout": 60.0
}

UNRELIABLE_SERVICE = {
    "failure_threshold": 5,
    "recovery_timeout": 300.0
}

EXTERNAL_API = {
    "failure_threshold": 2,
    "recovery_timeout": 600.0
}
```

### 3. Retry Strategy

**Recommended Retry Strategies:**
```python
# For different error types
RETRY_STRATEGIES = {
    "timeout": {
        "max_retries": 3,
        "exponential_backoff": True,
        "max_backoff": 30.0
    },
    "connection_error": {
        "max_retries": 5,
        "exponential_backoff": True,
        "max_backoff": 60.0
    },
    "rate_limit": {
        "max_retries": 2,
        "exponential_backoff": True,
        "max_backoff": 300.0
    },
    "server_error": {
        "max_retries": 2,
        "exponential_backoff": False,
        "max_backoff": 10.0
    }
}
```

### 4. Resource Management

**Best Practices:**
- Use async context managers for proper cleanup
- Implement connection pooling
- Set appropriate limits for concurrent operations
- Monitor memory usage and implement cleanup strategies

```python
# Example of proper resource management
async with EnhancedFetchService() as fetch_service:
    results = await fetch_service.fetch_multiple_urls(urls)
    # Resources automatically cleaned up
```

### 5. Error Handling and Logging

**Best Practices:**
- Log all errors with appropriate levels
- Include context information in error messages
- Implement structured logging
- Monitor error rates and patterns

```python
# Example of proper error logging
try:
    result = await fetch_url_safe(url)
    if not result.success:
        logger.warning(f"Fetch failed for {url}: {result.error_type} - {result.error_message}")
except Exception as e:
    logger.error(f"Unexpected error fetching {url}: {e}", exc_info=True)
```

### 6. Monitoring and Metrics

**Key Metrics to Track:**
- Success rate by URL/domain
- Response times
- Error rates by type
- Circuit breaker trips
- Cache hit rates

```python
# Example of metrics collection
stats = fetch_service.get_stats()
print(f"Success rate: {stats['success_rate']:.2%}")
print(f"Average response time: {stats.get('avg_response_time', 0):.2f}s")
print(f"Circuit breaker trips: {stats['circuit_breaker_trips']}")
```

## Integration with Existing Code

### 1. Updating Web Agents

The web agent has been updated to use the enhanced fetch service:

```python
# Before (problematic)
async def _fetch_webpage(self, url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return {"html": await response.text()}

# After (robust)
async def _fetch_webpage(self, url: str) -> dict:
    result = await fetch_url_safe(url, method="GET")
    if result.success:
        return {"html": result.content, "status_code": result.status_code}
    else:
        return {"html": "", "error": result.error_message}
```

### 2. Updating Data Ingestion

The data ingestion service has been updated:

```python
# Before (problematic)
response = requests.get(url, timeout=30)
response.raise_for_status()
content = response.text

# After (robust)
result = await fetch_url_safe(url, method="GET")
if not result.success:
    raise Exception(f"Failed to fetch URL: {result.error_message}")
content = result.content
```

## Testing and Validation

### 1. Unit Tests

Create comprehensive unit tests for the fetch service:

```python
async def test_fetch_service_timeout():
    """Test that fetch operations timeout properly."""
    service = EnhancedFetchService(FetchConfig(timeout=0.1))
    result = await service.fetch_url("http://httpbin.org/delay/1")
    assert not result.success
    assert result.error_type == FetchErrorType.TIMEOUT

async def test_circuit_breaker():
    """Test circuit breaker functionality."""
    service = EnhancedFetchService(FetchConfig(circuit_breaker_threshold=2))
    
    # First two failures
    for _ in range(2):
        result = await service.fetch_url("http://invalid-url-that-will-fail.com")
        assert not result.success
    
    # Third attempt should be blocked by circuit breaker
    result = await service.fetch_url("http://invalid-url-that-will-fail.com")
    assert not result.success
    assert "circuit breaker" in result.error_message.lower()
```

### 2. Integration Tests

Test the integration with existing services:

```python
async def test_web_agent_with_enhanced_fetch():
    """Test web agent with enhanced fetch service."""
    agent = EnhancedWebAgent()
    result = await agent._fetch_webpage("https://httpbin.org/html")
    assert "html" in result
    assert result["status_code"] == 200
```

## Performance Considerations

### 1. Connection Pooling

The enhanced fetch service uses connection pooling to improve performance:

```python
connector = aiohttp.TCPConnector(
    limit=100,              # Total connection limit
    limit_per_host=10,      # Connections per host
    keepalive_timeout=30,   # Keep connections alive
    enable_cleanup_closed=True
)
```

### 2. Concurrent Operations

Use semaphores to limit concurrent operations:

```python
semaphore = asyncio.Semaphore(max_concurrent)
async def fetch_with_semaphore(url: str) -> FetchResult:
    async with semaphore:
        return await fetch_url_safe(url)
```

### 3. Caching

Implement caching for frequently accessed data:

```python
# Cache successful results
if result.success and self.config.enable_caching:
    cache_key = hashlib.md5(url.encode()).hexdigest()
    await self.cache_manager.set(cache_key, result.content, ttl=3600)
```

## Troubleshooting

### Common Issues and Solutions

1. **High Timeout Errors**
   - Increase timeout values
   - Check network connectivity
   - Consider using CDN or closer servers

2. **Circuit Breaker Tripping Frequently**
   - Investigate target service health
   - Adjust failure threshold
   - Implement health checks

3. **Memory Leaks**
   - Ensure proper session cleanup
   - Monitor connection pool usage
   - Implement periodic cleanup

4. **Slow Performance**
   - Increase concurrent limits
   - Use connection pooling
   - Implement caching
   - Consider async operations

## Conclusion

The enhanced fetch service and sequential thinking service provide robust, production-ready solutions for handling fetch operations with proper timeout and error handling. These services implement industry best practices and can be easily integrated into existing codebases.

Key benefits:
- **Prevents Infinite Loops**: Proper timeout handling and circuit breakers
- **Graceful Degradation**: Fallback strategies and error classification
- **Resource Management**: Proper cleanup and connection pooling
- **Monitoring**: Comprehensive metrics and logging
- **Scalability**: Concurrent operations and caching support

By following these best practices, you can build reliable, performant applications that handle network failures gracefully and provide a better user experience.
