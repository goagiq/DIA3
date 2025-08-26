"""
Performance Optimized Data Processor

Optimized data processing system for handling large datasets (1-10MB) efficiently.
Part of Phase 3: Performance Optimization - Task 3.1

Features:
- Efficient data chunking and streaming
- Memory-optimized processing
- Parallel processing capabilities
- Data caching and optimization
- Load time < 3 seconds for 10MB datasets
"""

import asyncio
import json
import pickle
import gzip
from typing import Dict, Any, List, Optional, Union, Generator, Iterator
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd
import numpy as np
from functools import lru_cache
import hashlib
import time

logger = logging.getLogger(__name__)


@dataclass
class DataChunk:
    """Data chunk for efficient processing."""
    chunk_id: str
    data: Any
    size_bytes: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    processed: bool = False
    cache_key: Optional[str] = None


@dataclass
class ProcessingConfig:
    """Configuration for data processing optimization."""
    chunk_size: int = 1024 * 1024  # 1MB chunks
    max_workers: int = 4
    use_parallel: bool = True
    enable_caching: bool = True
    cache_ttl: int = 3600  # 1 hour
    compression_enabled: bool = True
    memory_limit_mb: int = 500
    target_load_time_seconds: float = 3.0


class PerformanceOptimizedDataProcessor:
    """High-performance data processor for large datasets."""
    
    def __init__(self, config: Optional[ProcessingConfig] = None):
        """Initialize the performance-optimized data processor."""
        self.config = config or ProcessingConfig()
        self.cache_dir = Path("cache/data_processing")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance monitoring
        self.processing_stats = {
            "total_processed": 0,
            "total_time": 0.0,
            "memory_usage": 0.0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        logger.info("✅ Performance Optimized Data Processor initialized")
        logger.info(f"   Chunk size: {self.config.chunk_size / 1024 / 1024:.1f}MB")
        logger.info(f"   Max workers: {self.config.max_workers}")
        logger.info(f"   Memory limit: {self.config.memory_limit_mb}MB")
    
    async def process_large_dataset(self, data: Union[Dict, List, str, Path], 
                                  dataset_name: str = "dataset") -> Dict[str, Any]:
        """Process large datasets efficiently with chunking and optimization."""
        start_time = time.time()
        
        try:
            logger.info(f"Processing large dataset: {dataset_name}")
            
            # Check cache first
            cache_key = self._generate_cache_key(data, dataset_name)
            if self.config.enable_caching:
                cached_result = await self._get_cached_result(cache_key)
                if cached_result:
                    self.processing_stats["cache_hits"] += 1
                    logger.info(f"✅ Cache hit for {dataset_name}")
                    return cached_result
            
            self.processing_stats["cache_misses"] += 1
            
            # Determine data size and chunking strategy
            data_size = self._estimate_data_size(data)
            logger.info(f"Dataset size: {data_size / 1024 / 1024:.2f}MB")
            
            if data_size > self.config.chunk_size:
                # Use chunked processing for large datasets
                result = await self._process_chunked_data(data, dataset_name, data_size)
            else:
                # Process small datasets directly
                result = await self._process_small_dataset(data, dataset_name)
            
            # Cache the result
            if self.config.enable_caching:
                await self._cache_result(cache_key, result)
            
            # Update performance stats
            processing_time = time.time() - start_time
            self.processing_stats["total_processed"] += data_size
            self.processing_stats["total_time"] += processing_time
            
            logger.info(f"✅ Dataset processed in {processing_time:.2f} seconds")
            
            # Validate performance targets
            if processing_time > self.config.target_load_time_seconds:
                logger.warning(f"⚠️ Processing time ({processing_time:.2f}s) exceeds target ({self.config.target_load_time_seconds}s)")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing dataset {dataset_name}: {e}")
            raise
    
    async def _process_chunked_data(self, data: Any, dataset_name: str, 
                                  total_size: int) -> Dict[str, Any]:
        """Process large datasets using chunking strategy."""
        chunks = self._create_data_chunks(data, total_size)
        logger.info(f"Created {len(chunks)} chunks for processing")
        
        # Process chunks in parallel if enabled
        if self.config.use_parallel and len(chunks) > 1:
            processed_chunks = await self._process_chunks_parallel(chunks)
        else:
            processed_chunks = await self._process_chunks_sequential(chunks)
        
        # Combine chunk results
        combined_result = self._combine_chunk_results(processed_chunks, dataset_name)
        
        return combined_result
    
    def _create_data_chunks(self, data: Any, total_size: int) -> List[DataChunk]:
        """Create data chunks for efficient processing."""
        chunks = []
        
        if isinstance(data, dict):
            # Split dictionary by keys
            keys = list(data.keys())
            chunk_count = max(1, total_size // self.config.chunk_size)
            keys_per_chunk = max(1, len(keys) // chunk_count)
            
            for i in range(0, len(keys), keys_per_chunk):
                chunk_keys = keys[i:i + keys_per_chunk]
                chunk_data = {k: data[k] for k in chunk_keys}
                chunk = DataChunk(
                    chunk_id=f"chunk_{i//keys_per_chunk}",
                    data=chunk_data,
                    size_bytes=len(str(chunk_data).encode())
                )
                chunks.append(chunk)
        
        elif isinstance(data, list):
            # Split list into chunks
            chunk_count = max(1, total_size // self.config.chunk_size)
            items_per_chunk = max(1, len(data) // chunk_count)
            
            for i in range(0, len(data), items_per_chunk):
                chunk_data = data[i:i + items_per_chunk]
                chunk = DataChunk(
                    chunk_id=f"chunk_{i//items_per_chunk}",
                    data=chunk_data,
                    size_bytes=len(str(chunk_data).encode())
                )
                chunks.append(chunk)
        
        else:
            # Single chunk for other data types
            chunk = DataChunk(
                chunk_id="chunk_0",
                data=data,
                size_bytes=total_size
            )
            chunks.append(chunk)
        
        return chunks
    
    async def _process_chunks_parallel(self, chunks: List[DataChunk]) -> List[DataChunk]:
        """Process chunks in parallel using thread pool."""
        loop = asyncio.get_event_loop()
        
        # Submit chunk processing tasks
        tasks = []
        for chunk in chunks:
            task = loop.run_in_executor(self.executor, self._process_single_chunk, chunk)
            tasks.append(task)
        
        # Wait for all chunks to complete
        processed_chunks = await asyncio.gather(*tasks)
        logger.info(f"✅ Processed {len(processed_chunks)} chunks in parallel")
        
        return processed_chunks
    
    async def _process_chunks_sequential(self, chunks: List[DataChunk]) -> List[DataChunk]:
        """Process chunks sequentially."""
        processed_chunks = []
        
        for chunk in chunks:
            processed_chunk = await asyncio.get_event_loop().run_in_executor(
                self.executor, self._process_single_chunk, chunk
            )
            processed_chunks.append(processed_chunk)
        
        logger.info(f"✅ Processed {len(processed_chunks)} chunks sequentially")
        return processed_chunks
    
    def _process_single_chunk(self, chunk: DataChunk) -> DataChunk:
        """Process a single data chunk."""
        try:
            # Apply optimizations based on data type
            if isinstance(chunk.data, dict):
                chunk.data = self._optimize_dict_data(chunk.data)
            elif isinstance(chunk.data, list):
                chunk.data = self._optimize_list_data(chunk.data)
            
            chunk.processed = True
            chunk.metadata["processing_time"] = time.time()
            
        except Exception as e:
            logger.error(f"Error processing chunk {chunk.chunk_id}: {e}")
            chunk.metadata["error"] = str(e)
        
        return chunk
    
    def _optimize_dict_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize dictionary data for processing."""
        optimized = {}
        
        for key, value in data.items():
            # Convert to efficient data types
            if isinstance(value, (list, tuple)) and len(value) > 1000:
                # Use numpy arrays for large numerical data
                try:
                    optimized[key] = np.array(value)
                except:
                    optimized[key] = value
            elif isinstance(value, dict):
                # Recursively optimize nested dictionaries
                optimized[key] = self._optimize_dict_data(value)
            else:
                optimized[key] = value
        
        return optimized
    
    def _optimize_list_data(self, data: List[Any]) -> List[Any]:
        """Optimize list data for processing."""
        if not data:
            return data
        
        # Check if all items are numeric
        if all(isinstance(item, (int, float)) for item in data):
            try:
                return np.array(data).tolist()
            except:
                pass
        
        # Check if all items are strings
        if all(isinstance(item, str) for item in data):
            # Optimize string list
            return [item.strip() for item in data if item.strip()]
        
        return data
    
    def _combine_chunk_results(self, chunks: List[DataChunk], dataset_name: str) -> Dict[str, Any]:
        """Combine processed chunk results into final dataset."""
        combined_data = {}
        
        for chunk in chunks:
            if chunk.processed and not chunk.metadata.get("error"):
                if isinstance(chunk.data, dict):
                    combined_data.update(chunk.data)
                elif isinstance(chunk.data, list):
                    if "data" not in combined_data:
                        combined_data["data"] = []
                    combined_data["data"].extend(chunk.data)
                else:
                    combined_data[chunk.chunk_id] = chunk.data
        
        # Add metadata
        combined_data["_metadata"] = {
            "dataset_name": dataset_name,
            "chunks_processed": len(chunks),
            "total_size_bytes": sum(chunk.size_bytes for chunk in chunks),
            "processing_time": time.time(),
            "optimization_applied": True
        }
        
        return combined_data
    
    async def _process_small_dataset(self, data: Any, dataset_name: str) -> Dict[str, Any]:
        """Process small datasets directly."""
        # Apply optimizations
        if isinstance(data, dict):
            optimized_data = self._optimize_dict_data(data)
        elif isinstance(data, list):
            optimized_data = self._optimize_list_data(data)
        else:
            optimized_data = data
        
        return {
            "data": optimized_data,
            "_metadata": {
                "dataset_name": dataset_name,
                "size_bytes": self._estimate_data_size(data),
                "processing_time": time.time(),
                "optimization_applied": True
            }
        }
    
    def _estimate_data_size(self, data: Any) -> int:
        """Estimate the size of data in bytes."""
        try:
            if isinstance(data, (str, bytes)):
                return len(data)
            elif isinstance(data, (dict, list)):
                return len(str(data).encode())
            else:
                return len(str(data).encode())
        except:
            return 1024  # Default estimate
    
    def _generate_cache_key(self, data: Any, dataset_name: str) -> str:
        """Generate cache key for data."""
        data_hash = hashlib.md5(str(data).encode()).hexdigest()
        return f"{dataset_name}_{data_hash}"
    
    async def _get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available and not expired."""
        cache_file = self.cache_dir / f"{cache_key}.pkl.gz"
        
        if not cache_file.exists():
            return None
        
        # Check if cache is expired
        if time.time() - cache_file.stat().st_mtime > self.config.cache_ttl:
            cache_file.unlink()  # Remove expired cache
            return None
        
        try:
            with gzip.open(cache_file, 'rb') as f:
                result = pickle.load(f)
            logger.info(f"Retrieved cached result: {cache_file}")
            return result
        except Exception as e:
            logger.warning(f"Failed to load cache {cache_file}: {e}")
            return None
    
    async def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache processing result."""
        cache_file = self.cache_dir / f"{cache_key}.pkl.gz"
        
        try:
            with gzip.open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            logger.info(f"Cached result: {cache_file}")
        except Exception as e:
            logger.warning(f"Failed to cache result {cache_file}: {e}")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            **self.processing_stats,
            "average_processing_time": (
                self.processing_stats["total_time"] / max(1, self.processing_stats["total_processed"])
            ),
            "cache_hit_rate": (
                self.processing_stats["cache_hits"] / 
                max(1, self.processing_stats["cache_hits"] + self.processing_stats["cache_misses"])
            ),
            "memory_usage_mb": self.processing_stats["memory_usage"] / 1024 / 1024
        }
    
    def clear_cache(self):
        """Clear all cached data."""
        try:
            for cache_file in self.cache_dir.glob("*.pkl.gz"):
                cache_file.unlink()
            logger.info("✅ Cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def __del__(self):
        """Cleanup on destruction."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)


# Global instance for easy access
performance_data_processor = PerformanceOptimizedDataProcessor()
