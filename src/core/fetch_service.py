#!/usr/bin/env python3
"""
Enhanced Fetch Service with Timeout and Error Handling

This module provides a robust fetch service that implements best practices for:
- Configurable timeouts for different operations
- Circuit breaker pattern to prevent cascading failures
- Intelligent retry logic with exponential backoff
- URL-specific error tracking
- Graceful degradation when moving to alternative URLs
- Resource management to prevent memory leaks
"""

import asyncio
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
from urllib.parse import urlparse
import aiohttp
import requests
from loguru import logger

# Configure logging
logger = logging.getLogger(__name__)


class FetchErrorType(Enum):
    """Types of fetch errors for intelligent handling."""
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    DNS_ERROR = "dns_error"
    SSL_ERROR = "ssl_error"
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    CLIENT_ERROR = "client_error"
    UNKNOWN = "unknown"


@dataclass
class FetchConfig:
    """Configuration for fetch operations."""
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    exponential_backoff: bool = True
    max_backoff: float = 60.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: float = 300.0  # 5 minutes
    user_agent: str = "DIA3-Fetch-Service/1.0"
    verify_ssl: bool = True
    follow_redirects: bool = True
    max_redirects: int = 5
    chunk_size: int = 8192
    max_content_length: int = 10 * 1024 * 1024  # 10MB


@dataclass
class FetchResult:
    """Result of a fetch operation."""
    url: str
    success: bool
    status_code: Optional[int] = None
    content: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    error_type: Optional[FetchErrorType] = None
    error_message: Optional[str] = None
    response_time: float = 0.0
    retry_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CircuitBreaker:
    """Circuit breaker implementation for URL-specific failure tracking."""
    url: str
    failure_threshold: int
    recovery_timeout: float
    failure_count: int = 0
    last_failure_time: Optional[datetime] = None
    state: str = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def record_failure(self):
        """Record a failure and potentially open the circuit."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker opened for {self.url} after {self.failure_count} failures")
    
    def record_success(self):
        """Record a success and potentially close the circuit."""
        self.failure_count = 0
        self.last_failure_time = None
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logger.info(f"Circuit breaker closed for {self.url} after successful request")
    
    def can_attempt(self) -> bool:
        """Check if a request can be attempted."""
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if (self.last_failure_time and 
                datetime.now() - self.last_failure_time > timedelta(seconds=self.recovery_timeout)):
                self.state = "HALF_OPEN"
                logger.info(f"Circuit breaker half-open for {self.url}")
                return True
            return False
        else:  # HALF_OPEN
            return True


class EnhancedFetchService:
    """Enhanced fetch service with comprehensive error handling and timeout management."""
    
    def __init__(self, config: Optional[FetchConfig] = None):
        self.config = config or FetchConfig()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.url_blacklist: Dict[str, datetime] = {}
        self.blacklist_duration = timedelta(minutes=30)
        self.session: Optional[aiohttp.ClientSession] = None
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "timeout_errors": 0,
            "connection_errors": 0,
            "circuit_breaker_trips": 0
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._create_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._close_session()
    
    async def _create_session(self):
        """Create aiohttp session with proper configuration."""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(
                total=self.config.timeout,
                connect=10.0,
                sock_read=30.0
            )
            
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=10,
                keepalive_timeout=30,
                enable_cleanup_closed=True,
                ssl=self.config.verify_ssl
            )
            
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={"User-Agent": self.config.user_agent}
            )
    
    async def _close_session(self):
        """Close aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    def _get_circuit_breaker(self, url: str) -> CircuitBreaker:
        """Get or create a circuit breaker for a URL."""
        if url not in self.circuit_breakers:
            self.circuit_breakers[url] = CircuitBreaker(
                url=url,
                failure_threshold=self.config.circuit_breaker_threshold,
                recovery_timeout=self.config.circuit_breaker_timeout
            )
        return self.circuit_breakers[url]
    
    def _is_url_blacklisted(self, url: str) -> bool:
        """Check if a URL is blacklisted."""
        if url in self.url_blacklist:
            if datetime.now() - self.url_blacklist[url] > self.blacklist_duration:
                del self.url_blacklist[url]
                return False
            return True
        return False
    
    def _blacklist_url(self, url: str):
        """Add a URL to the blacklist."""
        self.url_blacklist[url] = datetime.now()
        logger.warning(f"URL blacklisted: {url}")
    
    def _classify_error(self, error: Exception) -> FetchErrorType:
        """Classify the type of error for intelligent handling."""
        error_str = str(error).lower()
        
        if isinstance(error, asyncio.TimeoutError) or "timeout" in error_str:
            return FetchErrorType.TIMEOUT
        elif isinstance(error, aiohttp.ClientConnectorError) or "connection" in error_str:
            return FetchErrorType.CONNECTION_ERROR
        elif "dns" in error_str or "name resolution" in error_str:
            return FetchErrorType.DNS_ERROR
        elif "ssl" in error_str or "certificate" in error_str:
            return FetchErrorType.SSL_ERROR
        elif "429" in error_str or "rate limit" in error_str:
            return FetchErrorType.RATE_LIMIT
        elif any(code in error_str for code in ["500", "502", "503", "504"]):
            return FetchErrorType.SERVER_ERROR
        elif any(code in error_str for code in ["400", "401", "403", "404"]):
            return FetchErrorType.CLIENT_ERROR
        else:
            return FetchErrorType.UNKNOWN
    
    def _should_retry(self, error_type: FetchErrorType, retry_count: int) -> bool:
        """Determine if the operation should be retried."""
        if retry_count >= self.config.max_retries:
            return False
        
        # Don't retry certain error types
        if error_type in [FetchErrorType.CLIENT_ERROR, FetchErrorType.SSL_ERROR]:
            return False
        
        # Always retry network and timeout errors
        if error_type in [FetchErrorType.TIMEOUT, FetchErrorType.CONNECTION_ERROR, FetchErrorType.DNS_ERROR]:
            return True
        
        # Retry server errors with limits
        if error_type == FetchErrorType.SERVER_ERROR and retry_count < 2:
            return True
        
        # Retry rate limit errors with exponential backoff
        if error_type == FetchErrorType.RATE_LIMIT:
            return True
        
        return False
    
    def _calculate_delay(self, retry_count: int) -> float:
        """Calculate delay for retry attempt."""
        if self.config.exponential_backoff:
            delay = self.config.retry_delay * (2 ** retry_count)
        else:
            delay = self.config.retry_delay
        
        return min(delay, self.config.max_backoff)
    
    async def fetch_url(self, url: str, method: str = "GET", **kwargs) -> FetchResult:
        """
        Fetch a URL with comprehensive error handling and timeout management.
        
        Args:
            url: The URL to fetch
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional arguments for the request
            
        Returns:
            FetchResult with success status and content
        """
        start_time = time.time()
        self.stats["total_requests"] += 1
        
        # Check if URL is blacklisted
        if self._is_url_blacklisted(url):
            return FetchResult(
                url=url,
                success=False,
                error_type=FetchErrorType.UNKNOWN,
                error_message="URL is blacklisted due to previous failures",
                response_time=time.time() - start_time
            )
        
        # Check circuit breaker
        circuit_breaker = self._get_circuit_breaker(url)
        if not circuit_breaker.can_attempt():
            self.stats["circuit_breaker_trips"] += 1
            return FetchResult(
                url=url,
                success=False,
                error_type=FetchErrorType.UNKNOWN,
                error_message="Circuit breaker is open",
                response_time=time.time() - start_time
            )
        
        # Ensure session exists
        await self._create_session()
        
        retry_count = 0
        last_error = None
        
        while retry_count <= self.config.max_retries:
            try:
                # Make the request
                async with self.session.request(method, url, **kwargs) as response:
                    # Check content length
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) > self.config.max_content_length:
                        raise ValueError(f"Content too large: {content_length} bytes")
                    
                    # Read content with timeout
                    content = await asyncio.wait_for(
                        response.text(),
                        timeout=self.config.timeout
                    )
                    
                    response_time = time.time() - start_time
                    
                    # Record success
                    circuit_breaker.record_success()
                    self.stats["successful_requests"] += 1
                    
                    return FetchResult(
                        url=url,
                        success=True,
                        status_code=response.status,
                        content=content,
                        headers=dict(response.headers),
                        response_time=response_time,
                        retry_count=retry_count
                    )
                    
            except Exception as e:
                last_error = e
                error_type = self._classify_error(e)
                retry_count += 1
                
                # Record failure
                circuit_breaker.record_failure()
                
                # Update stats
                if error_type == FetchErrorType.TIMEOUT:
                    self.stats["timeout_errors"] += 1
                elif error_type == FetchErrorType.CONNECTION_ERROR:
                    self.stats["connection_errors"] += 1
                
                logger.warning(f"Fetch attempt {retry_count} failed for {url}: {e}")
                
                # Check if we should retry
                if not self._should_retry(error_type, retry_count):
                    break
                
                # Wait before retry
                delay = self._calculate_delay(retry_count - 1)
                await asyncio.sleep(delay)
        
        # All retries failed
        self.stats["failed_requests"] += 1
        
        # Blacklist URL if it's consistently failing
        if circuit_breaker.failure_count >= self.config.circuit_breaker_threshold * 2:
            self._blacklist_url(url)
        
        return FetchResult(
            url=url,
            success=False,
            error_type=self._classify_error(last_error) if last_error else FetchErrorType.UNKNOWN,
            error_message=str(last_error) if last_error else "Unknown error",
            response_time=time.time() - start_time,
            retry_count=retry_count
        )
    
    async def fetch_multiple_urls(
        self, 
        urls: List[str], 
        method: str = "GET",
        max_concurrent: int = 10,
        **kwargs
    ) -> List[FetchResult]:
        """
        Fetch multiple URLs concurrently with rate limiting.
        
        Args:
            urls: List of URLs to fetch
            method: HTTP method
            max_concurrent: Maximum concurrent requests
            **kwargs: Additional arguments for requests
            
        Returns:
            List of FetchResult objects
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fetch_with_semaphore(url: str) -> FetchResult:
            async with semaphore:
                return await self.fetch_url(url, method, **kwargs)
        
        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to FetchResult
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(FetchResult(
                    url=urls[i],
                    success=False,
                    error_type=FetchErrorType.UNKNOWN,
                    error_message=str(result),
                    response_time=0.0
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def fetch_with_fallback(
        self, 
        primary_url: str, 
        fallback_urls: List[str],
        method: str = "GET",
        **kwargs
    ) -> FetchResult:
        """
        Fetch from primary URL with fallback to alternative URLs.
        
        Args:
            primary_url: Primary URL to try first
            fallback_urls: List of fallback URLs to try if primary fails
            method: HTTP method
            **kwargs: Additional arguments for requests
            
        Returns:
            FetchResult from the first successful URL
        """
        # Try primary URL first
        result = await self.fetch_url(primary_url, method, **kwargs)
        if result.success:
            return result
        
        # Try fallback URLs
        all_urls = [primary_url] + fallback_urls
        for url in all_urls[1:]:  # Skip primary URL since we already tried it
            logger.info(f"Trying fallback URL: {url}")
            result = await self.fetch_url(url, method, **kwargs)
            if result.success:
                return result
        
        # All URLs failed, return the last result
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get fetch service statistics."""
        return {
            **self.stats,
            "circuit_breakers": len(self.circuit_breakers),
            "blacklisted_urls": len(self.url_blacklist),
            "success_rate": (
                self.stats["successful_requests"] / max(self.stats["total_requests"], 1)
            )
        }
    
    def reset_stats(self):
        """Reset fetch service statistics."""
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "timeout_errors": 0,
            "connection_errors": 0,
            "circuit_breaker_trips": 0
        }
    
    def clear_blacklist(self):
        """Clear the URL blacklist."""
        self.url_blacklist.clear()
        logger.info("URL blacklist cleared")
    
    def clear_circuit_breakers(self):
        """Clear all circuit breakers."""
        self.circuit_breakers.clear()
        logger.info("Circuit breakers cleared")


# Global fetch service instance
_fetch_service: Optional[EnhancedFetchService] = None


async def get_fetch_service(config: Optional[FetchConfig] = None) -> EnhancedFetchService:
    """Get the global fetch service instance."""
    global _fetch_service
    if _fetch_service is None:
        _fetch_service = EnhancedFetchService(config)
    return _fetch_service


async def fetch_url_safe(url: str, **kwargs) -> FetchResult:
    """Safe wrapper for fetching a single URL."""
    service = await get_fetch_service()
    return await service.fetch_url(url, **kwargs)


async def fetch_multiple_urls_safe(urls: List[str], **kwargs) -> List[FetchResult]:
    """Safe wrapper for fetching multiple URLs."""
    service = await get_fetch_service()
    return await service.fetch_multiple_urls(urls, **kwargs)


async def fetch_with_fallback_safe(
    primary_url: str, 
    fallback_urls: List[str], 
    **kwargs
) -> FetchResult:
    """Safe wrapper for fetching with fallback URLs."""
    service = await get_fetch_service()
    return await service.fetch_with_fallback(primary_url, fallback_urls, **kwargs)
