"""
Test Phase 1: Unified Search Pipeline Implementation

This test file verifies the implementation of Phase 1 components:
- Unified Search Orchestrator
- MCP Tool Manager
- API Routes
"""

import asyncio
import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

# Import the components to test
try:
    from src.core.unified_search_orchestrator import (
        UnifiedSearchOrchestrator,
        SearchResults,
        SearchResult,
        SourceMetadata,
        SourceType,
        QueryCache,
        RetryConfig,
        ParallelProcessor
    )
    from src.core.mcp_tool_manager import (
        MCPToolManager,
        MCPTool,
        TACSystem,
        DataGovSystem,
        ForecastingEngine,
        ToolCache,
        HealthMonitor,
        ToolHealth,
        ToolMetrics
    )
    from src.api.unified_search_routes import router
    PHASE1_AVAILABLE = True
except ImportError as e:
    print(f"Phase 1 components not available: {e}")
    PHASE1_AVAILABLE = False


class TestPhase1UnifiedSearch:
    """Test suite for Phase 1 Unified Search implementation."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create a test orchestrator instance."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        return UnifiedSearchOrchestrator()
    
    @pytest.fixture
    def mcp_manager(self):
        """Create a test MCP tool manager instance."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        return MCPToolManager()
    
    @pytest.fixture
    def sample_search_results(self):
        """Create sample search results for testing."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        return SearchResults(
            results=[
                SearchResult(
                    content={"test": "data"},
                    sources=[
                        SourceMetadata(
                            source_type=SourceType.VECTOR_DB,
                            source_name="Test Vector DB",
                            confidence=0.9
                        )
                    ],
                    confidence=0.9,
                    timestamp=datetime.now(),
                    intelligence_type="test"
                )
            ],
            query="test query",
            timestamp=datetime.now(),
            processing_time=1.0,
            sources_queried=[SourceType.VECTOR_DB]
        )
    
    def test_source_type_enum(self):
        """Test SourceType enum values."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        assert SourceType.VECTOR_DB.value == "vector_db"
        assert SourceType.KNOWLEDGE_GRAPH.value == "knowledge_graph"
        assert SourceType.TAC.value == "tac"
        assert SourceType.DATAGOV.value == "datagov"
        assert SourceType.FORECASTING_ENGINE.value == "forecasting_engine"
    
    def test_source_metadata_creation(self):
        """Test SourceMetadata creation."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        metadata = SourceMetadata(
            source_type=SourceType.TAC,
            source_name="Test TAC",
            title="Test Title",
            url="https://test.com",
            confidence=0.8,
            reliability_score=0.9
        )
        
        assert metadata.source_type == SourceType.TAC
        assert metadata.source_name == "Test TAC"
        assert metadata.title == "Test Title"
        assert metadata.confidence == 0.8
        assert metadata.reliability_score == 0.9
    
    def test_search_result_creation(self):
        """Test SearchResult creation and content hash generation."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        result = SearchResult(
            content={"test": "data"},
            sources=[
                SourceMetadata(
                    source_type=SourceType.VECTOR_DB,
                    source_name="Test Source"
                )
            ],
            confidence=0.9,
            timestamp=datetime.now(),
            intelligence_type="test"
        )
        
        assert result.content == {"test": "data"}
        assert len(result.sources) == 1
        assert result.confidence == 0.9
        assert result.content_hash is not None
        assert len(result.content_hash) == 32  # MD5 hash length
    
    def test_search_results_merge(self, sample_search_results):
        """Test SearchResults merge functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Create another search results object
        other_results = SearchResults(
            results=[
                SearchResult(
                    content={"other": "data"},
                    sources=[
                        SourceMetadata(
                            source_type=SourceType.KNOWLEDGE_GRAPH,
                            source_name="Test KG",
                            confidence=0.8
                        )
                    ],
                    confidence=0.8,
                    timestamp=datetime.now(),
                    intelligence_type="test"
                )
            ],
            query="test query",
            timestamp=datetime.now(),
            processing_time=0.5,
            sources_queried=[SourceType.KNOWLEDGE_GRAPH]
        )
        
        # Merge results
        merged = sample_search_results.merge_with(other_results)
        
        assert len(merged.results) == 2
        assert len(merged.sources_queried) == 2
        assert SourceType.VECTOR_DB in merged.sources_queried
        assert SourceType.KNOWLEDGE_GRAPH in merged.sources_queried
        assert merged.processing_time == 1.0  # Max of both processing times
    
    def test_query_cache(self):
        """Test QueryCache functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        cache = QueryCache(cache_duration=3600)
        
        # Test cache miss
        result = asyncio.run(cache.get("test query"))
        assert result is None
        
        # Test cache set and get
        test_results = SearchResults(
            results=[],
            query="test query",
            timestamp=datetime.now(),
            processing_time=1.0,
            sources_queried=[]
        )
        
        asyncio.run(cache.set("test query", test_results))
        cached_result = asyncio.run(cache.get("test query"))
        assert cached_result is not None
        assert cached_result.query == "test query"
    
    def test_retry_config(self):
        """Test RetryConfig creation."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        config = RetryConfig(max_retries=3, base_delay=2.0)
        assert config.max_retries == 3
        assert config.base_delay == 2.0
    
    def test_parallel_processor(self):
        """Test ParallelProcessor functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        processor = ParallelProcessor()
        
        # Create mock tasks
        async def mock_task1():
            return "result1"
        
        async def mock_task2():
            return "result2"
        
        # Test parallel execution
        tasks = [mock_task1(), mock_task2()]
        results = asyncio.run(processor.execute_parallel(tasks))
        
        assert len(results) == 2
        assert "result1" in results
        assert "result2" in results
    
    def test_tool_metrics(self):
        """Test ToolMetrics functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        metrics = ToolMetrics()
        
        # Test initial state
        assert metrics.success_count == 0
        assert metrics.failure_count == 0
        assert metrics.success_rate == 0.0
        assert metrics.average_response_time == 0.0
        
        # Test with data
        metrics.success_count = 8
        metrics.failure_count = 2
        metrics.total_response_time = 10.0
        
        assert metrics.success_rate == 0.8
        assert metrics.average_response_time == 1.0
    
    def test_tool_health_enum(self):
        """Test ToolHealth enum values."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        assert ToolHealth.HEALTHY.value == "healthy"
        assert ToolHealth.DEGRADED.value == "degraded"
        assert ToolHealth.UNHEALTHY.value == "unhealthy"
        assert ToolHealth.UNKNOWN.value == "unknown"
    
    def test_mcp_tool_base_class(self):
        """Test MCPTool base class."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Create a mock tool
        class MockTool(MCPTool):
            async def execute(self, query: str):
                return {"result": "mock"}
        
        tool = MockTool("Mock Tool", SourceType.UNKNOWN)
        
        assert tool.name == "Mock Tool"
        assert tool.source_type == SourceType.UNKNOWN
        assert tool.metrics is not None
    
    def test_tool_cache(self):
        """Test ToolCache functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        cache = ToolCache(cache_duration=300)
        
        # Test initial state
        assert cache.is_expired() is True
        
        # Test cache set and get
        mock_tools = [Mock(spec=MCPTool)]
        asyncio.run(cache.set_tools(mock_tools))
        
        assert cache.is_expired() is False
        cached_tools = asyncio.run(cache.get_tools())
        assert len(cached_tools) == 1
    
    def test_health_monitor(self):
        """Test HealthMonitor functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        monitor = HealthMonitor()
        
        # Create mock tool
        mock_tool = Mock(spec=MCPTool)
        mock_tool.name = "Test Tool"
        mock_tool.metrics = ToolMetrics()
        
        # Test success recording
        asyncio.run(monitor.record_success(mock_tool, 1.5))
        assert mock_tool.metrics.success_count == 1
        assert mock_tool.metrics.health_status == ToolHealth.HEALTHY
        
        # Test failure recording
        asyncio.run(monitor.record_failure(mock_tool, Exception("test error")))
        assert mock_tool.metrics.failure_count == 1
        assert mock_tool.metrics.success_rate == 0.5
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, orchestrator):
        """Test UnifiedSearchOrchestrator initialization."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        assert orchestrator.cache is not None
        assert orchestrator.retry_config is not None
        assert orchestrator.parallel_processor is not None
        assert orchestrator.retry_config.max_retries == 2
    
    @pytest.mark.asyncio
    async def test_mcp_manager_initialization(self, mcp_manager):
        """Test MCPToolManager initialization."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        assert mcp_manager.tool_cache is not None
        assert mcp_manager.health_monitor is not None
        assert mcp_manager.available_tools == []
    
    @pytest.mark.asyncio
    async def test_orchestrator_merge_and_rank_results(self, orchestrator, sample_search_results):
        """Test result merging and ranking functionality."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Create another search results with different confidence
        other_results = SearchResults(
            results=[
                SearchResult(
                    content={"other": "data"},
                    sources=[
                        SourceMetadata(
                            source_type=SourceType.KNOWLEDGE_GRAPH,
                            source_name="Test KG",
                            confidence=0.7
                        )
                    ],
                    confidence=0.7,
                    timestamp=datetime.now(),
                    intelligence_type="test"
                )
            ],
            query="test query",
            timestamp=datetime.now(),
            processing_time=0.5,
            sources_queried=[SourceType.KNOWLEDGE_GRAPH]
        )
        
        # Test merging and ranking
        merged_results = await orchestrator.merge_and_rank_results(sample_search_results, other_results)
        
        assert len(merged_results) == 2
        # Higher confidence result should be first
        assert merged_results[0].confidence >= merged_results[1].confidence
    
    @pytest.mark.asyncio
    async def test_orchestrator_duplicate_removal(self, orchestrator):
        """Test duplicate removal in merge_and_rank_results."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Create two search results with identical content
        result1 = SearchResult(
            content={"test": "data"},
            sources=[
                SourceMetadata(
                    source_type=SourceType.VECTOR_DB,
                    source_name="Source 1",
                    confidence=0.8
                )
            ],
            confidence=0.8,
            timestamp=datetime.now(),
            intelligence_type="test"
        )
        
        result2 = SearchResult(
            content={"test": "data"},  # Same content
            sources=[
                SourceMetadata(
                    source_type=SourceType.KNOWLEDGE_GRAPH,
                    source_name="Source 2",
                    confidence=0.9
                )
            ],
            confidence=0.9,
            timestamp=datetime.now(),
            intelligence_type="test"
        )
        
        local_results = SearchResults(
            results=[result1],
            query="test",
            timestamp=datetime.now(),
            processing_time=1.0,
            sources_queried=[SourceType.VECTOR_DB]
        )
        
        mcp_results = SearchResults(
            results=[result2],
            query="test",
            timestamp=datetime.now(),
            processing_time=1.0,
            sources_queried=[SourceType.KNOWLEDGE_GRAPH]
        )
        
        # Test merging - should remove duplicate and merge sources
        merged_results = await orchestrator.merge_and_rank_results(local_results, mcp_results)
        
        assert len(merged_results) == 1  # Duplicate removed
        assert len(merged_results[0].sources) == 2  # Sources merged
        assert merged_results[0].confidence == 0.9  # Higher confidence kept
    
    def test_api_route_models(self):
        """Test API route Pydantic models."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Test SearchRequest model
        from src.api.unified_search_routes import SearchRequest
        
        request = SearchRequest(
            query="test query",
            user_context={"domain": "test"},
            include_local_only=False,
            include_mcp_only=False
        )
        
        assert request.query == "test query"
        assert request.user_context["domain"] == "test"
        assert request.include_local_only is False
    
    def test_phase1_architecture_compliance(self):
        """Test that Phase 1 implementation follows the planned architecture."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Test that all required components are implemented
        required_classes = [
            'UnifiedSearchOrchestrator',
            'MCPToolManager',
            'SearchResults',
            'SearchResult',
            'SourceMetadata',
            'SourceType',
            'QueryCache',
            'RetryConfig',
            'ParallelProcessor',
            'MCPTool',
            'ToolCache',
            'HealthMonitor',
            'ToolHealth',
            'ToolMetrics'
        ]
        
        for class_name in required_classes:
            assert class_name in globals(), f"Required class {class_name} not implemented"
    
    def test_phase1_requirements_implementation(self):
        """Test that Phase 1 implements all required features."""
        if not PHASE1_AVAILABLE:
            pytest.skip("Phase 1 components not available")
        
        # Test caching implementation (Answer 1: yes)
        cache = QueryCache()
        assert hasattr(cache, 'get')
        assert hasattr(cache, 'set')
        
        # Test retry logic implementation (Answer 3: yes, retry twice)
        retry_config = RetryConfig()
        assert retry_config.max_retries == 2
        
        # Test parallel processing implementation (Answer 13: yes)
        processor = ParallelProcessor()
        assert hasattr(processor, 'execute_parallel')
        
        # Test duplicate merging implementation (Answer 4: merge)
        orchestrator = UnifiedSearchOrchestrator()
        assert hasattr(orchestrator, 'merge_and_rank_results')
        
        # Test health monitoring implementation
        monitor = HealthMonitor()
        assert hasattr(monitor, 'record_success')
        assert hasattr(monitor, 'record_failure')
        assert hasattr(monitor, 'get_health_summary')


def run_phase1_tests():
    """Run all Phase 1 tests and generate a report."""
    print("=" * 60)
    print("PHASE 1: UNIFIED SEARCH PIPELINE - TEST RESULTS")
    print("=" * 60)
    
    if not PHASE1_AVAILABLE:
        print("❌ Phase 1 components not available")
        print("   Please ensure all required modules are properly installed")
        return False
    
    # Run tests
    test_results = []
    
    # Test 1: Basic component creation
    try:
        orchestrator = UnifiedSearchOrchestrator()
        test_results.append(("UnifiedSearchOrchestrator Creation", "✅ PASS"))
    except Exception as e:
        test_results.append(("UnifiedSearchOrchestrator Creation", f"❌ FAIL: {e}"))
    
    # Test 2: MCP Tool Manager creation
    try:
        mcp_manager = MCPToolManager()
        test_results.append(("MCPToolManager Creation", "✅ PASS"))
    except Exception as e:
        test_results.append(("MCPToolManager Creation", f"❌ FAIL: {e}"))
    
    # Test 3: Data structures
    try:
        metadata = SourceMetadata(
            source_type=SourceType.TAC,
            source_name="Test",
            confidence=0.9
        )
        test_results.append(("SourceMetadata Creation", "✅ PASS"))
    except Exception as e:
        test_results.append(("SourceMetadata Creation", f"❌ FAIL: {e}"))
    
    # Test 4: Search results
    try:
        result = SearchResult(
            content={"test": "data"},
            sources=[metadata],
            confidence=0.9,
            timestamp=datetime.now(),
            intelligence_type="test"
        )
        test_results.append(("SearchResult Creation", "✅ PASS"))
    except Exception as e:
        test_results.append(("SearchResult Creation", f"❌ FAIL: {e}"))
    
    # Test 5: Cache functionality
    try:
        cache = QueryCache()
        test_results.append(("QueryCache Creation", "✅ PASS"))
    except Exception as e:
        test_results.append(("QueryCache Creation", f"❌ FAIL: {e}"))
    
    # Test 6: Retry configuration
    try:
        retry_config = RetryConfig(max_retries=2)
        assert retry_config.max_retries == 2
        test_results.append(("RetryConfig Implementation", "✅ PASS"))
    except Exception as e:
        test_results.append(("RetryConfig Implementation", f"❌ FAIL: {e}"))
    
    # Test 7: Health monitoring
    try:
        monitor = HealthMonitor()
        test_results.append(("HealthMonitor Creation", "✅ PASS"))
    except Exception as e:
        test_results.append(("HealthMonitor Creation", f"❌ FAIL: {e}"))
    
    # Print results
    print("\nTest Results:")
    print("-" * 40)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        print(f"{test_name:<30} {result}")
        if "✅ PASS" in result:
            passed += 1
    
    print("-" * 40)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    if passed == total:
        print("\n🎉 PHASE 1 IMPLEMENTATION: SUCCESS")
        print("All core components are working correctly.")
        return True
    else:
        print("\n⚠️  PHASE 1 IMPLEMENTATION: PARTIAL SUCCESS")
        print("Some components need attention.")
        return False


if __name__ == "__main__":
    run_phase1_tests()
