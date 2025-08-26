"""
Unified Search Orchestrator

This module implements a central orchestrator that routes all queries through local knowledge first,
then all available MCP tools with caching, retry logic, and parallel processing.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

from loguru import logger

# Import existing components
try:
    from src.core.vector_database import VectorDatabase
    from src.core.knowledge_graph import KnowledgeGraph
    from src.core.file_search import FileSearch
    VECTOR_DB_AVAILABLE = True
except ImportError:
    logger.warning("Vector database components not available")
    VECTOR_DB_AVAILABLE = False

try:
    from src.core.mcp_tool_manager import MCPToolManager
    MCP_TOOLS_AVAILABLE = True
except ImportError:
    logger.warning("MCP tool manager not available")
    MCP_TOOLS_AVAILABLE = False


class SourceType(Enum):
    """Enumeration of data source types."""
    VECTOR_DB = "vector_db"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    LOCAL_FILES = "local_files"
    TAC = "tac"
    DATAGOV = "datagov"
    FORECASTING_ENGINE = "forecasting_engine"
    EXTERNAL_NEWS = "external_news"
    UNKNOWN = "unknown"


@dataclass
class SourceMetadata:
    """Metadata for a data source."""
    source_type: SourceType
    source_name: str
    title: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    confidence: float = 1.0
    reliability_score: float = 1.0
    version_id: Optional[str] = None


@dataclass
class SearchResult:
    """A single search result with source metadata."""
    content: Any
    sources: List[SourceMetadata]
    confidence: float
    timestamp: datetime
    intelligence_type: str
    content_hash: Optional[str] = None
    
    def __post_init__(self):
        if self.content_hash is None:
            self.content_hash = self.generate_content_hash()
    
    def generate_content_hash(self) -> str:
        """Generate a hash of the content for deduplication."""
        content_str = json.dumps(self.content, sort_keys=True, default=str)
        return hashlib.md5(content_str.encode()).hexdigest()


@dataclass
class SearchResults:
    """Container for search results from multiple sources."""
    results: List[SearchResult]
    query: str
    timestamp: datetime
    processing_time: float
    sources_queried: List[SourceType]
    cache_hit: bool = False
    
    def merge_with(self, other: 'SearchResults') -> 'SearchResults':
        """Merge with another SearchResults object."""
        all_results = self.results + other.results
        all_sources = list(set(self.sources_queried + other.sources_queried))
        
        return SearchResults(
            results=all_results,
            query=self.query,
            timestamp=datetime.now(),
            processing_time=max(self.processing_time, other.processing_time),
            sources_queried=all_sources
        )


class QueryCache:
    """Cache for query results to avoid repeated API calls."""
    
    def __init__(self, cache_duration: int = 3600):  # 1 hour default
        self.cache = {}
        self.cache_duration = cache_duration
    
    async def get(self, query: str) -> Optional[SearchResults]:
        """Get cached results for a query."""
        if query in self.cache:
            cached_data = self.cache[query]
            if datetime.now() - cached_data['timestamp'] < timedelta(seconds=self.cache_duration):
                logger.info(f"Cache hit for query: {query[:50]}...")
                return cached_data['results']
            else:
                # Expired cache entry
                del self.cache[query]
        return None
    
    async def set(self, query: str, results: SearchResults) -> None:
        """Cache results for a query."""
        self.cache[query] = {
            'results': results,
            'timestamp': datetime.now()
        }
        logger.info(f"Cached results for query: {query[:50]}...")


class RetryConfig:
    """Configuration for retry logic."""
    
    def __init__(self, max_retries: int = 2, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay


class ParallelProcessor:
    """Handles parallel processing of search operations."""
    
    async def execute_parallel(self, tasks: List[asyncio.Task]) -> List[Any]:
        """Execute multiple tasks in parallel."""
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        except Exception as e:
            logger.error(f"Error in parallel execution: {e}")
            return []


class UnifiedSearchOrchestrator:
    """
    Central orchestrator for unified search operations.
    
    Routes all queries through local knowledge first, then all available MCP tools
    with caching, retry logic, and parallel processing.
    """
    
    def __init__(self):
        self.cache = QueryCache()
        self.retry_config = RetryConfig(max_retries=2)
        self.parallel_processor = ParallelProcessor()
        
        # Initialize components
        if VECTOR_DB_AVAILABLE:
            self.vector_db = VectorDatabase()
            self.knowledge_graph = KnowledgeGraph()
            self.file_search = FileSearch()
        else:
            self.vector_db = None
            self.knowledge_graph = None
            self.file_search = None
        
        if MCP_TOOLS_AVAILABLE:
            self.mcp_tool_manager = MCPToolManager()
        else:
            self.mcp_tool_manager = None
        
        logger.info("Unified Search Orchestrator initialized")
    
    async def process_query(self, query: str, user_context: Dict[str, Any] = None) -> SearchResults:
        """
        Process a query through the unified search pipeline.
        
        Args:
            query: The search query
            user_context: Additional context for the search
            
        Returns:
            SearchResults: Combined results from all sources
        """
        start_time = datetime.now()
        
        try:
            # 1. Check cache first
            cached_results = await self.cache.get(query)
            if cached_results:
                cached_results.cache_hit = True
                return cached_results
            
            # 2. Execute local knowledge search and MCP search in parallel
            local_task = asyncio.create_task(self.search_local_knowledge(query))
            mcp_task = asyncio.create_task(self.search_all_mcp_tools(query))
            
            # 3. Wait for both to complete
            local_results, mcp_results = await asyncio.gather(local_task, mcp_task)
            
            # 4. Merge and rank results
            combined_results = await self.merge_and_rank_results(local_results, mcp_results)
            
            # 5. Store new results with version history
            await self.store_new_results_with_versioning(combined_results)
            
            # 6. Cache results
            processing_time = (datetime.now() - start_time).total_seconds()
            final_results = SearchResults(
                results=combined_results,
                query=query,
                timestamp=datetime.now(),
                processing_time=processing_time,
                sources_queried=self.get_sources_queried(local_results, mcp_results)
            )
            
            await self.cache.set(query, final_results)
            
            logger.info(f"Query processed successfully in {processing_time:.2f}s")
            return final_results
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            # Return empty results on error
            return SearchResults(
                results=[],
                query=query,
                timestamp=datetime.now(),
                processing_time=(datetime.now() - start_time).total_seconds(),
                sources_queried=[]
            )
    
    async def search_local_knowledge(self, query: str) -> SearchResults:
        """Search local knowledge sources (vector DB, knowledge graph, local files)."""
        if not VECTOR_DB_AVAILABLE:
            logger.warning("Local knowledge search not available")
            return SearchResults(
                results=[],
                query=query,
                timestamp=datetime.now(),
                processing_time=0.0,
                sources_queried=[]
            )
        
        start_time = datetime.now()
        
        try:
            # Execute searches in parallel
            tasks = [
                asyncio.create_task(self._search_vector_db(query)),
                asyncio.create_task(self._search_knowledge_graph(query)),
                asyncio.create_task(self._search_local_files(query))
            ]
            
            vector_results, kg_results, file_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            all_results = []
            sources_queried = []
            
            if not isinstance(vector_results, Exception):
                all_results.extend(vector_results)
                sources_queried.append(SourceType.VECTOR_DB)
            
            if not isinstance(kg_results, Exception):
                all_results.extend(kg_results)
                sources_queried.append(SourceType.KNOWLEDGE_GRAPH)
            
            if not isinstance(file_results, Exception):
                all_results.extend(file_results)
                sources_queried.append(SourceType.LOCAL_FILES)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return SearchResults(
                results=all_results,
                query=query,
                timestamp=datetime.now(),
                processing_time=processing_time,
                sources_queried=sources_queried
            )
            
        except Exception as e:
            logger.error(f"Error in local knowledge search: {e}")
            return SearchResults(
                results=[],
                query=query,
                timestamp=datetime.now(),
                processing_time=(datetime.now() - start_time).total_seconds(),
                sources_queried=[]
            )
    
    async def _search_vector_db(self, query: str) -> List[SearchResult]:
        """Search vector database."""
        try:
            results = await self.vector_db.search(query)
            return [
                SearchResult(
                    content=result['content'],
                    sources=[SourceMetadata(
                        source_type=SourceType.VECTOR_DB,
                        source_name="Vector Database",
                        timestamp=datetime.now(),
                        confidence=result.get('confidence', 1.0)
                    )],
                    confidence=result.get('confidence', 1.0),
                    timestamp=datetime.now(),
                    intelligence_type="vector_db"
                )
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            return []
    
    async def _search_knowledge_graph(self, query: str) -> List[SearchResult]:
        """Search knowledge graph."""
        try:
            results = await self.knowledge_graph.search(query)
            return [
                SearchResult(
                    content=result['content'],
                    sources=[SourceMetadata(
                        source_type=SourceType.KNOWLEDGE_GRAPH,
                        source_name="Knowledge Graph",
                        timestamp=datetime.now(),
                        confidence=result.get('confidence', 1.0)
                    )],
                    confidence=result.get('confidence', 1.0),
                    timestamp=datetime.now(),
                    intelligence_type="knowledge_graph"
                )
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching knowledge graph: {e}")
            return []
    
    async def _search_local_files(self, query: str) -> List[SearchResult]:
        """Search local files."""
        try:
            results = await self.file_search.search(query)
            return [
                SearchResult(
                    content=result['content'],
                    sources=[SourceMetadata(
                        source_type=SourceType.LOCAL_FILES,
                        source_name=result.get('file_name', 'Local File'),
                        title=result.get('title'),
                        timestamp=datetime.now(),
                        confidence=result.get('confidence', 1.0)
                    )],
                    confidence=result.get('confidence', 1.0),
                    timestamp=datetime.now(),
                    intelligence_type="local_files"
                )
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching local files: {e}")
            return []
    
    async def search_all_mcp_tools(self, query: str) -> SearchResults:
        """Search all available MCP tools in parallel."""
        if not MCP_TOOLS_AVAILABLE:
            logger.warning("MCP tools not available")
            return SearchResults(
                results=[],
                query=query,
                timestamp=datetime.now(),
                processing_time=0.0,
                sources_queried=[]
            )
        
        start_time = datetime.now()
        
        try:
            # Get all available MCP tools
            mcp_tools = await self.mcp_tool_manager.discover_mcp_tools()
            
            # Execute all tools in parallel with retry logic
            tasks = []
            for tool in mcp_tools:
                task = asyncio.create_task(
                    self.execute_mcp_tool_with_retry(tool, query)
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            all_results = []
            sources_queried = []
            
            for i, result in enumerate(results):
                if not isinstance(result, Exception) and result is not None:
                    all_results.extend(result)
                    sources_queried.append(mcp_tools[i].source_type)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return SearchResults(
                results=all_results,
                query=query,
                timestamp=datetime.now(),
                processing_time=processing_time,
                sources_queried=sources_queried
            )
            
        except Exception as e:
            logger.error(f"Error in MCP tools search: {e}")
            return SearchResults(
                results=[],
                query=query,
                timestamp=datetime.now(),
                processing_time=(datetime.now() - start_time).total_seconds(),
                sources_queried=[]
            )
    
    async def execute_mcp_tool_with_retry(self, tool, query: str) -> Optional[List[SearchResult]]:
        """Execute MCP tool with retry logic."""
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                result = await tool.execute(query)
                return self.convert_mcp_result_to_search_results(result, tool)
            except Exception as e:
                logger.warning(f"Tool {tool.name} failed (attempt {attempt + 1}): {e}")
                if attempt == self.retry_config.max_retries:
                    logger.error(f"Tool {tool.name} failed after {self.retry_config.max_retries + 1} attempts")
                    return None
                await asyncio.sleep(self.retry_config.base_delay * (2 ** attempt))
        
        return None
    
    def convert_mcp_result_to_search_results(self, result: Any, tool) -> List[SearchResult]:
        """Convert MCP tool result to SearchResult format."""
        if not result:
            return []
        
        # Convert based on tool type
        if hasattr(tool, 'source_type'):
            source_type = tool.source_type
        else:
            source_type = SourceType.UNKNOWN
        
        return [
            SearchResult(
                content=item.get('content', item),
                sources=[SourceMetadata(
                    source_type=source_type,
                    source_name=tool.name,
                    title=item.get('title'),
                    url=item.get('url'),
                    timestamp=datetime.now(),
                    confidence=item.get('confidence', 1.0)
                )],
                confidence=item.get('confidence', 1.0),
                timestamp=datetime.now(),
                intelligence_type=str(source_type.value)
            )
            for item in (result if isinstance(result, list) else [result])
        ]
    
    async def merge_and_rank_results(self, local_results: SearchResults, mcp_results: SearchResults) -> List[SearchResult]:
        """Merge and rank results from local and MCP sources."""
        all_results = local_results.results + mcp_results.results
        
        # Remove duplicates based on content hash
        seen_hashes = set()
        unique_results = []
        
        for result in all_results:
            if result.content_hash not in seen_hashes:
                seen_hashes.add(result.content_hash)
                unique_results.append(result)
            else:
                # Merge with existing result
                existing = next(r for r in unique_results if r.content_hash == result.content_hash)
                existing.sources.extend(result.sources)
                existing.confidence = max(existing.confidence, result.confidence)
        
        # Sort by confidence and timestamp
        unique_results.sort(key=lambda x: (x.confidence, x.timestamp), reverse=True)
        
        return unique_results
    
    async def store_new_results_with_versioning(self, results: List[SearchResult]) -> None:
        """Store new results with version history."""
        # This will be implemented in Phase 2
        logger.info(f"Storing {len(results)} results with versioning")
        pass
    
    def get_sources_queried(self, local_results: SearchResults, mcp_results: SearchResults) -> List[SourceType]:
        """Get list of all sources that were queried."""
        return list(set(local_results.sources_queried + mcp_results.sources_queried))


# Global instance
unified_search_orchestrator = UnifiedSearchOrchestrator()
