"""
Phase 2 Integration Module
Integrates IntelligenceStorageManager, VersionHistoryManager, and IntelligenceBuilder
with the existing unified search orchestrator from Phase 1.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .intelligence_storage_manager import IntelligenceStorageManager, StorageMetrics
from .version_history_manager import VersionHistoryManager, Version, VersionHistory
from .intelligence_builder import IntelligenceBuilder, Pattern, TrendAnalysis, Connection, IntelligenceScore, AggregatedIntelligence, ValidationResult
from ..unified_search_orchestrator import UnifiedSearchOrchestrator, SearchResult, SearchResults
from ..mcp_tool_manager import MCPToolManager


class Phase2Integration:
    """Phase 2 integration manager that ties all components together."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize Phase 1 components
        self.unified_search_orchestrator = UnifiedSearchOrchestrator(config.get("unified_search", {}))
        self.mcp_tool_manager = MCPToolManager(config.get("mcp_tools", {}))
        
        # Initialize Phase 2 components
        self.intelligence_storage_manager = IntelligenceStorageManager(config.get("intelligence_storage", {}))
        self.version_history_manager = VersionHistoryManager(config.get("version_history", {}))
        self.intelligence_builder = IntelligenceBuilder(config.get("intelligence_builder", {}))
        
        # Integration settings
        self.auto_store_results = config.get("auto_store_results", True)
        self.auto_version_content = config.get("auto_version_content", True)
        self.auto_build_intelligence = config.get("auto_build_intelligence", True)
        
        # Performance monitoring
        self.integration_metrics = {
            "total_searches": 0,
            "total_stored_results": 0,
            "total_versions_created": 0,
            "total_intelligence_built": 0,
            "last_operation_time": datetime.now()
        }
    
    async def perform_enhanced_search(self, query: str, search_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform enhanced search with automatic storage and intelligence building."""
        try:
            self.logger.info(f"Starting enhanced search for query: {query}")
            start_time = datetime.now()
            
            # Step 1: Perform unified search (Phase 1)
            search_results = await self.unified_search_orchestrator.search(query, search_options or {})
            
            # Step 2: Automatically store results (Phase 2)
            storage_operation_ids = []
            if self.auto_store_results and search_results.results:
                storage_operation_ids = await self.intelligence_storage_manager.store_search_results(search_results.results)
                self.integration_metrics["total_stored_results"] += len(search_results.results)
            
            # Step 3: Create versions for significant content (Phase 2)
            version_ids = []
            if self.auto_version_content and search_results.results:
                version_ids = await self._create_versions_for_results(search_results.results)
                self.integration_metrics["total_versions_created"] += len(version_ids)
            
            # Step 4: Build intelligence from results (Phase 2)
            intelligence_results = {}
            if self.auto_build_intelligence and search_results.results:
                intelligence_results = await self._build_intelligence_from_results(search_results.results)
                self.integration_metrics["total_intelligence_built"] += 1
            
            # Update metrics
            self.integration_metrics["total_searches"] += 1
            self.integration_metrics["last_operation_time"] = datetime.now()
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare response
            response = {
                "search_results": search_results,
                "storage_operations": {
                    "operation_ids": storage_operation_ids,
                    "count": len(storage_operation_ids)
                },
                "version_operations": {
                    "version_ids": version_ids,
                    "count": len(version_ids)
                },
                "intelligence_results": intelligence_results,
                "processing_time": processing_time,
                "metrics": self.integration_metrics.copy()
            }
            
            self.logger.info(f"Enhanced search completed in {processing_time:.2f} seconds")
            return response
            
        except Exception as e:
            self.logger.error(f"Enhanced search failed: {e}")
            raise
    
    async def _create_versions_for_results(self, results: List[SearchResult]) -> List[str]:
        """Create versions for significant search results."""
        version_ids = []
        
        try:
            for result in results:
                # Only create versions for high-confidence results
                if result.confidence >= 0.7:
                    metadata = {
                        "source_type": result.source_metadata.source_type.value,
                        "source_name": result.source_metadata.source_name,
                        "confidence": result.confidence,
                        "search_query": "auto_generated",  # Would be passed from search context
                        "auto_versioned": True
                    }
                    
                    version_id = await self.version_history_manager.create_version(
                        content=result.content,
                        metadata=metadata,
                        user_id="system"
                    )
                    version_ids.append(version_id)
            
            self.logger.info(f"Created {len(version_ids)} versions for search results")
            
        except Exception as e:
            self.logger.error(f"Failed to create versions for results: {e}")
        
        return version_ids
    
    async def _build_intelligence_from_results(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Build intelligence from search results."""
        intelligence_results = {}
        
        try:
            # Identify patterns
            patterns = await self.intelligence_builder.identify_patterns(results)
            intelligence_results["patterns"] = patterns
            
            # Analyze trends (if temporal data available)
            if len(results) >= 3:
                try:
                    trend_analysis = await self.intelligence_builder.analyze_trends(results, "recent")
                    intelligence_results["trends"] = trend_analysis
                except Exception as e:
                    self.logger.warning(f"Trend analysis failed: {e}")
            
            # Cross-reference analysis
            entities = self._extract_entities_from_results(results)
            if len(entities) >= 2:
                connections = await self.intelligence_builder.cross_reference_analysis(entities)
                intelligence_results["connections"] = connections
            
            # Score intelligence
            if intelligence_results:
                intelligence_score = await self.intelligence_builder.score_intelligence(intelligence_results)
                intelligence_results["score"] = intelligence_score
            
            # Aggregate intelligence
            if results:
                aggregated_intelligence = await self.intelligence_builder.aggregate_intelligence(results)
                intelligence_results["aggregated"] = aggregated_intelligence
            
            # Validate intelligence
            if intelligence_results:
                validation_result = await self.intelligence_builder.validate_intelligence(intelligence_results)
                intelligence_results["validation"] = validation_result
            
            self.logger.info(f"Built intelligence with {len(intelligence_results)} components")
            
        except Exception as e:
            self.logger.error(f"Failed to build intelligence from results: {e}")
        
        return intelligence_results
    
    def _extract_entities_from_results(self, results: List[SearchResult]) -> List[str]:
        """Extract entities from search results."""
        entities = set()
        
        for result in results:
            if hasattr(result, 'content') and isinstance(result.content, str):
                # Simple entity extraction
                words = result.content.split()
                for word in words:
                    if word[0].isupper() and len(word) > 2:
                        entities.add(word)
        
        return list(entities)
    
    async def get_storage_metrics(self) -> StorageMetrics:
        """Get storage operation metrics."""
        return await self.intelligence_storage_manager.monitor_storage_operations()
    
    async def get_version_history(self, content_id: str) -> VersionHistory:
        """Get version history for content."""
        return await self.version_history_manager.get_version_history(content_id)
    
    async def compare_versions(self, version1_id: str, version2_id: str):
        """Compare two versions of content."""
        return await self.version_history_manager.compare_versions(version1_id, version2_id)
    
    async def rollback_to_version(self, content_id: str, version_id: str) -> bool:
        """Rollback content to a specific version."""
        return await self.version_history_manager.rollback_to_version(content_id, version_id)
    
    async def identify_patterns(self, data: List[Any]) -> List[Pattern]:
        """Identify patterns in data."""
        return await self.intelligence_builder.identify_patterns(data)
    
    async def analyze_trends(self, data: List[Any], timeframe: str) -> TrendAnalysis:
        """Analyze trends in data."""
        return await self.intelligence_builder.analyze_trends(data, timeframe)
    
    async def cross_reference_analysis(self, entities: List[str]) -> List[Connection]:
        """Perform cross-reference analysis."""
        return await self.intelligence_builder.cross_reference_analysis(entities)
    
    async def score_intelligence(self, intelligence: Any) -> IntelligenceScore:
        """Score intelligence."""
        return await self.intelligence_builder.score_intelligence(intelligence)
    
    async def aggregate_intelligence(self, related_data: List[Any]) -> AggregatedIntelligence:
        """Aggregate intelligence data."""
        return await self.intelligence_builder.aggregate_intelligence(related_data)
    
    async def validate_intelligence(self, intelligence: Any) -> ValidationResult:
        """Validate intelligence."""
        return await self.intelligence_builder.validate_intelligence(intelligence)
    
    async def cleanup_old_versions(self, retention_days: Optional[int] = None) -> int:
        """Clean up old versions."""
        return await self.version_history_manager.cleanup_old_versions(retention_days)
    
    async def cleanup_duplicate_cache(self) -> int:
        """Clean up duplicate cache."""
        return await self.intelligence_storage_manager.cleanup_duplicate_cache()
    
    async def get_integration_metrics(self) -> Dict[str, Any]:
        """Get integration metrics."""
        storage_metrics = await self.get_storage_metrics()
        
        return {
            "integration_metrics": self.integration_metrics.copy(),
            "storage_metrics": {
                "total_operations": storage_metrics.total_operations,
                "successful_operations": storage_metrics.successful_operations,
                "failed_operations": storage_metrics.failed_operations,
                "duplicate_operations": storage_metrics.duplicate_operations,
                "average_processing_time": storage_metrics.average_processing_time,
                "storage_size_bytes": storage_metrics.storage_size_bytes
            },
            "system_health": {
                "auto_store_results": self.auto_store_results,
                "auto_version_content": self.auto_version_content,
                "auto_build_intelligence": self.auto_build_intelligence,
                "last_operation_time": self.integration_metrics["last_operation_time"].isoformat()
            }
        }
    
    async def shutdown(self):
        """Shutdown all Phase 2 components."""
        try:
            await self.intelligence_storage_manager.shutdown()
            self.logger.info("Phase 2 integration shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during Phase 2 shutdown: {e}")


# Convenience functions for easy integration
async def create_phase2_integration(config: Dict[str, Any]) -> Phase2Integration:
    """Create a Phase 2 integration instance."""
    return Phase2Integration(config)


async def perform_phase2_search(query: str, config: Dict[str, Any], 
                              search_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Perform a Phase 2 enhanced search."""
    integration = await create_phase2_integration(config)
    try:
        return await integration.perform_enhanced_search(query, search_options)
    finally:
        await integration.shutdown()
