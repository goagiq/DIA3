"""
Intelligence Storage Manager for Phase 2 Implementation
Automatically stores all search results in vector DB and knowledge graph DB
with duplicate detection and storage monitoring capabilities.
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from ..vector_db_manager import VectorDBManager
from ..database_manager import DatabaseManager
from ..unified_search_orchestrator import SearchResult, SourceMetadata, SourceType


class StorageStatus(Enum):
    """Storage operation status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DUPLICATE = "duplicate"


@dataclass
class StorageMetrics:
    """Storage operation metrics."""
    total_operations: int
    successful_operations: int
    failed_operations: int
    duplicate_operations: int
    average_processing_time: float
    last_operation_time: datetime
    storage_size_bytes: int
    vector_db_size: int
    knowledge_graph_size: int


@dataclass
class StorageOperation:
    """Storage operation record."""
    operation_id: str
    search_result: SearchResult
    status: StorageStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    processing_time: Optional[float] = None
    error_message: Optional[str] = None
    storage_locations: List[str] = None


class IntelligenceStorageManager:
    """Intelligence storage manager for automatic storage of search results."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.operation_id = str(uuid.uuid4())
        
        # Initialize storage components
        self.vector_db_manager = VectorDBManager(config.get("vector_db", {}))
        self.database_manager = DatabaseManager(config.get("database", {}))
        
        # Storage monitoring
        self.metrics = StorageMetrics(
            total_operations=0,
            successful_operations=0,
            failed_operations=0,
            duplicate_operations=0,
            average_processing_time=0.0,
            last_operation_time=datetime.now(),
            storage_size_bytes=0,
            vector_db_size=0,
            knowledge_graph_size=0
        )
        
        # Duplicate detection cache
        self.duplicate_cache = {}
        self.cache_ttl = config.get("duplicate_cache_ttl", 3600)  # 1 hour
        
        # Storage operations queue
        self.storage_queue = asyncio.Queue()
        self.processing_task = None
        
        # Start background processing
        self._start_background_processing()
        
    def _start_background_processing(self):
        """Start background storage processing task."""
        if self.processing_task is None or self.processing_task.done():
            self.processing_task = asyncio.create_task(self._process_storage_queue())
            self.logger.info("Background storage processing started")
    
    async def _process_storage_queue(self):
        """Process storage queue in background."""
        while True:
            try:
                # Get operation from queue
                operation = await self.storage_queue.get()
                
                # Process the operation
                await self._process_storage_operation(operation)
                
                # Mark as done
                self.storage_queue.task_done()
                
            except asyncio.CancelledError:
                self.logger.info("Storage queue processing cancelled")
                break
            except Exception as e:
                self.logger.error(f"Error processing storage operation: {e}")
                await asyncio.sleep(1)  # Wait before retrying
    
    async def _process_storage_operation(self, operation: StorageOperation):
        """Process a single storage operation."""
        start_time = datetime.now()
        operation.status = StorageStatus.PROCESSING
        
        try:
            # Check for duplicates
            if await self._is_duplicate(operation.search_result):
                operation.status = StorageStatus.DUPLICATE
                operation.completed_at = datetime.now()
                operation.processing_time = (operation.completed_at - operation.created_at).total_seconds()
                self.metrics.duplicate_operations += 1
                self.logger.info(f"Duplicate detected for operation {operation.operation_id}")
                return
            
            # Store in vector database
            await self._store_in_vector_db(operation.search_result)
            
            # Store in knowledge graph
            await self._store_in_knowledge_graph(operation.search_result)
            
            # Update operation status
            operation.status = StorageStatus.COMPLETED
            operation.completed_at = datetime.now()
            operation.processing_time = (operation.completed_at - operation.created_at).total_seconds()
            operation.storage_locations = ["vector_db", "knowledge_graph"]
            
            # Update metrics
            self.metrics.successful_operations += 1
            self.metrics.last_operation_time = datetime.now()
            
            self.logger.info(f"Storage operation {operation.operation_id} completed successfully")
            
        except Exception as e:
            operation.status = StorageStatus.FAILED
            operation.error_message = str(e)
            operation.completed_at = datetime.now()
            operation.processing_time = (operation.completed_at - operation.created_at).total_seconds()
            
            self.metrics.failed_operations += 1
            self.logger.error(f"Storage operation {operation.operation_id} failed: {e}")
        
        finally:
            self.metrics.total_operations += 1
            # Update average processing time
            if self.metrics.total_operations > 0:
                total_time = sum([
                    op.processing_time or 0 
                    for op in [operation]  # In real implementation, track all operations
                ])
                self.metrics.average_processing_time = total_time / self.metrics.total_operations
    
    async def store_search_results(self, results: List[SearchResult]) -> List[str]:
        """Store multiple search results automatically."""
        operation_ids = []
        
        for result in results:
            operation_id = await self._queue_storage_operation(result)
            operation_ids.append(operation_id)
        
        self.logger.info(f"Queued {len(results)} search results for storage")
        return operation_ids
    
    async def _queue_storage_operation(self, search_result: SearchResult) -> str:
        """Queue a storage operation for background processing."""
        operation = StorageOperation(
            operation_id=str(uuid.uuid4()),
            search_result=search_result,
            status=StorageStatus.PENDING,
            created_at=datetime.now(),
            storage_locations=[]
        )
        
        await self.storage_queue.put(operation)
        return operation.operation_id
    
    async def _is_duplicate(self, search_result: SearchResult) -> bool:
        """Check if search result is a duplicate."""
        # Generate content hash
        content_hash = self._generate_content_hash(search_result)
        
        # Check cache first
        if content_hash in self.duplicate_cache:
            cache_entry = self.duplicate_cache[content_hash]
            if datetime.now() - cache_entry["timestamp"] < timedelta(seconds=self.cache_ttl):
                return True
        
        # Check vector database for similar content
        similar_results = await self.vector_db_manager.search_similar(
            content=search_result.content,
            threshold=0.95,  # High similarity threshold for duplicates
            limit=5
        )
        
        # If similar content found, mark as duplicate
        if similar_results:
            self.duplicate_cache[content_hash] = {
                "timestamp": datetime.now(),
                "similar_id": similar_results[0].id
            }
            return True
        
        return False
    
    def _generate_content_hash(self, search_result: SearchResult) -> str:
        """Generate hash for content to detect duplicates."""
        content_str = str(search_result.content) + str(search_result.source_metadata)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    async def _store_in_vector_db(self, search_result: SearchResult) -> None:
        """Store search result in vector database."""
        try:
            # Prepare metadata
            metadata = {
                "source_type": search_result.source_metadata.source_type.value,
                "source_name": search_result.source_metadata.source_name,
                "source_title": search_result.source_metadata.source_title,
                "source_url": search_result.source_metadata.source_url,
                "confidence": search_result.confidence,
                "timestamp": search_result.timestamp.isoformat(),
                "content_type": type(search_result.content).__name__,
                "content_length": len(str(search_result.content))
            }
            
            # Store in vector database
            await self.vector_db_manager.store_content(
                content=search_result.content,
                metadata=metadata,
                namespace=f"intelligence_{search_result.source_metadata.source_type.value}"
            )
            
            self.logger.debug(f"Stored in vector DB: {search_result.source_metadata.source_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to store in vector DB: {e}")
            raise
    
    async def _store_in_knowledge_graph(self, search_result: SearchResult) -> None:
        """Store search result in knowledge graph database."""
        try:
            # Extract entities and relationships from content
            entities = await self._extract_entities(search_result.content)
            relationships = await self._extract_relationships(search_result.content)
            
            # Store entities
            for entity in entities:
                await self.database_manager.store_entity(
                    entity_id=entity["id"],
                    entity_type=entity["type"],
                    entity_name=entity["name"],
                    properties=entity.get("properties", {}),
                    source_metadata=search_result.source_metadata
                )
            
            # Store relationships
            for relationship in relationships:
                await self.database_manager.store_relationship(
                    relationship_id=relationship["id"],
                    source_entity=relationship["source"],
                    target_entity=relationship["target"],
                    relationship_type=relationship["type"],
                    properties=relationship.get("properties", {}),
                    source_metadata=search_result.source_metadata
                )
            
            self.logger.debug(f"Stored in knowledge graph: {len(entities)} entities, {len(relationships)} relationships")
            
        except Exception as e:
            self.logger.error(f"Failed to store in knowledge graph: {e}")
            raise
    
    async def _extract_entities(self, content: Any) -> List[Dict[str, Any]]:
        """Extract entities from content for knowledge graph storage."""
        entities = []
        
        # Simple entity extraction (can be enhanced with NLP)
        if isinstance(content, str):
            # Extract potential entities (names, organizations, locations)
            # This is a simplified implementation
            words = content.split()
            for i, word in enumerate(words):
                if word[0].isupper() and len(word) > 2:
                    entities.append({
                        "id": f"entity_{i}_{hash(word)}",
                        "type": "PERSON" if word.endswith(('Mr.', 'Ms.', 'Dr.')) else "ORGANIZATION",
                        "name": word,
                        "properties": {"confidence": 0.7}
                    })
        
        return entities
    
    async def _extract_relationships(self, content: Any) -> List[Dict[str, Any]]:
        """Extract relationships from content for knowledge graph storage."""
        relationships = []
        
        # Simple relationship extraction (can be enhanced with NLP)
        if isinstance(content, str):
            # Extract potential relationships
            # This is a simplified implementation
            sentences = content.split('.')
            for sentence in sentences:
                if ' and ' in sentence or ' with ' in sentence:
                    parts = sentence.split(' and ' if ' and ' in sentence else ' with ')
                    if len(parts) >= 2:
                        relationships.append({
                            "id": f"rel_{hash(sentence)}",
                            "source": parts[0].strip(),
                            "target": parts[1].strip(),
                            "type": "ASSOCIATED_WITH",
                            "properties": {"confidence": 0.6}
                        })
        
        return relationships
    
    async def process_content_for_storage(self, content: Any) -> Dict[str, Any]:
        """Process and normalize content before storage."""
        processed_content = {
            "original_content": content,
            "content_type": type(content).__name__,
            "content_length": len(str(content)),
            "processed_at": datetime.now().isoformat(),
            "normalized_content": self._normalize_content(content)
        }
        
        return processed_content
    
    def _normalize_content(self, content: Any) -> str:
        """Normalize content for consistent storage."""
        if isinstance(content, str):
            # Basic text normalization
            normalized = content.strip()
            normalized = ' '.join(normalized.split())  # Remove extra whitespace
            return normalized
        elif isinstance(content, dict):
            return json.dumps(content, sort_keys=True)
        elif isinstance(content, list):
            return json.dumps(content, sort_keys=True)
        else:
            return str(content)
    
    async def detect_duplicates(self, content: Any) -> bool:
        """Detect if content is a duplicate."""
        content_hash = hashlib.sha256(str(content).encode()).hexdigest()
        
        # Check cache
        if content_hash in self.duplicate_cache:
            return True
        
        # Check vector database
        similar_results = await self.vector_db_manager.search_similar(
            content=content,
            threshold=0.95,
            limit=1
        )
        
        return len(similar_results) > 0
    
    async def monitor_storage_operations(self) -> StorageMetrics:
        """Monitor storage operations and return metrics."""
        # Update storage size metrics
        try:
            self.metrics.storage_size_bytes = await self._get_storage_size()
            self.metrics.vector_db_size = await self.vector_db_manager.get_collection_size()
            self.metrics.knowledge_graph_size = await self.database_manager.get_knowledge_graph_size()
        except Exception as e:
            self.logger.error(f"Failed to update storage metrics: {e}")
        
        return self.metrics
    
    async def _get_storage_size(self) -> int:
        """Get total storage size in bytes."""
        try:
            # This would integrate with actual storage systems
            # For now, return estimated size
            return self.metrics.vector_db_size + self.metrics.knowledge_graph_size
        except Exception as e:
            self.logger.error(f"Failed to get storage size: {e}")
            return 0
    
    async def cleanup_duplicate_cache(self) -> int:
        """Clean up expired entries from duplicate cache."""
        current_time = datetime.now()
        expired_keys = []
        
        for key, entry in self.duplicate_cache.items():
            if current_time - entry["timestamp"] > timedelta(seconds=self.cache_ttl):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.duplicate_cache[key]
        
        self.logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        return len(expired_keys)
    
    async def shutdown(self):
        """Shutdown the storage manager."""
        if self.processing_task and not self.processing_task.done():
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Intelligence storage manager shutdown complete")
