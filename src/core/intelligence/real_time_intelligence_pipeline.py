"""
Real-Time Intelligence Pipeline

Phase 4 Implementation - Continuous Intelligence Generation
This module implements the real-time intelligence pipeline that continuously
generates intelligence from knowledge graph data and provides real-time
recommendations across multiple domains.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque

from loguru import logger

from src.core.models import AnalysisRequest, AnalysisResult
from src.core.knowledge_graph_integration import KnowledgeGraphIntegration
from src.core.streaming.data_stream_processor import EnhancedDataStreamProcessor
from src.core.streaming.intelligence_data_adapter import IntelligenceDataAdapter
from src.agents.knowledge_graph_agent import KnowledgeGraphAgent
from src.agents.multi_domain_knowledge_graph_agent import MultiDomainKnowledgeGraphAgent


@dataclass
class IntelligenceStream:
    """Represents a stream of intelligence data."""
    stream_id: str
    data_type: str
    timestamp: datetime
    intelligence_data: Dict[str, Any]
    confidence_score: float
    source_domains: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrossDomainIntelligence:
    """Represents cross-domain intelligence analysis."""
    analysis_id: str
    domains: List[str]
    cross_domain_patterns: List[Dict[str, Any]]
    integrated_recommendations: List[Dict[str, Any]]
    confidence_score: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineMetrics:
    """Metrics for the real-time intelligence pipeline."""
    total_intelligence_generated: int = 0
    cross_domain_analyses: int = 0
    average_processing_time: float = 0.0
    error_count: int = 0
    last_update: datetime = field(default_factory=datetime.now)
    domain_metrics: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class RealTimeIntelligencePipeline:
    """
    Real-time intelligence pipeline for continuous intelligence generation.
    
    Features:
    - Continuous intelligence generation from knowledge graph
    - Cross-domain intelligence integration
    - Real-time data stream processing
    - Dynamic recommendation generation
    - Performance monitoring and metrics
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the real-time intelligence pipeline."""
        self.config = config or self._get_default_config()
        
        # Core components
        self.knowledge_graph_integration = KnowledgeGraphIntegration()
        self.knowledge_graph_agent = KnowledgeGraphAgent()
        self.multi_domain_agent = MultiDomainKnowledgeGraphAgent()
        self.data_adapter = IntelligenceDataAdapter()
        self.stream_processor = EnhancedDataStreamProcessor()
        
        # Pipeline state
        self.is_running = False
        self.processing_task = None
        self.intelligence_queue = deque(maxlen=1000)
        self.cross_domain_queue = deque(maxlen=500)
        
        # Metrics and monitoring
        self.metrics = PipelineMetrics()
        self.performance_monitor = {
            'processing_times': deque(maxlen=1000),
            'queue_sizes': deque(maxlen=100),
            'error_counts': {},
            'domain_performance': {}
        }
        
        # Intelligence generation callbacks
        self.intelligence_callbacks: List[Callable] = []
        self.cross_domain_callbacks: List[Callable] = []
        
        # Domain-specific intelligence generators
        self.domain_generators = {
            'defense': self._generate_defense_intelligence,
            'intelligence': self._generate_intelligence_intelligence,
            'business': self._generate_business_intelligence,
            'cyber': self._generate_cyber_intelligence,
            'diplomatic': self._generate_diplomatic_intelligence,
            'economic': self._generate_economic_intelligence
        }
        
        logger.info("✅ RealTimeIntelligencePipeline initialized")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for the pipeline."""
        return {
            'processing_interval': 5.0,  # 5 seconds
            'intelligence_generation_interval': 60.0,  # 1 minute
            'cross_domain_analysis_interval': 300.0,  # 5 minutes
            'max_concurrent_analyses': 10,
            'confidence_threshold': 0.7,
            'cache_ttl': 3600,  # 1 hour
            'domains': ['defense', 'intelligence', 'business', 'cyber', 'diplomatic', 'economic'],
            'real_time_feeds': ['sigint_stream', 'humint_stream', 'osint_stream', 'geospatial_stream', 'cyber_stream']
        }
    
    async def start_pipeline(self) -> None:
        """Start the real-time intelligence pipeline."""
        if self.is_running:
            logger.warning("Pipeline is already running")
            return
        
        self.is_running = True
        
        # Start stream processor
        await self.stream_processor.start_enhanced_processing()
        
        # Start intelligence generation task
        self.processing_task = asyncio.create_task(self._intelligence_generation_loop())
        
        # Start cross-domain analysis task
        asyncio.create_task(self._cross_domain_analysis_loop())
        
        logger.info("✅ Real-time intelligence pipeline started")
    
    async def stop_pipeline(self) -> None:
        """Stop the real-time intelligence pipeline."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stop stream processor
        await self.stream_processor.stop_enhanced_processing()
        
        # Stop processing tasks
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        logger.info("✅ Real-time intelligence pipeline stopped")
    
    async def generate_continuous_intelligence(self, data_stream: Dict[str, Any]) -> IntelligenceStream:
        """
        Generate continuous intelligence from data stream.
        
        Args:
            data_stream: Incoming data stream
            
        Returns:
            IntelligenceStream with generated intelligence
        """
        try:
            start_time = datetime.now()
            
            # Process incoming data
            processed_data = await self.data_adapter.process_stream_data(data_stream)
            
            # Update knowledge graph with new data
            await self._update_knowledge_graph(processed_data)
            
            # Generate intelligence based on data type and domain
            intelligence_data = await self._generate_domain_intelligence(processed_data)
            
            # Create intelligence stream
            stream = IntelligenceStream(
                stream_id=f"intelligence_{datetime.now().isoformat()}",
                data_type=processed_data.data_type,
                timestamp=datetime.now(),
                intelligence_data=intelligence_data,
                confidence_score=intelligence_data.get('confidence', 0.0),
                source_domains=intelligence_data.get('domains', []),
                metadata={
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'data_source': processed_data.source,
                    'original_data': processed_data.raw_data
                }
            )
            
            # Add to queue and trigger callbacks
            self.intelligence_queue.append(stream)
            await self._trigger_intelligence_callbacks(stream)
            
            # Update metrics
            self._update_metrics(stream)
            
            logger.info(f"✅ Generated intelligence for {processed_data.data_type}")
            return stream
            
        except Exception as e:
            logger.error(f"Error generating continuous intelligence: {e}")
            self.metrics.error_count += 1
            raise
    
    async def generate_cross_domain_intelligence(self, domains: List[str]) -> CrossDomainIntelligence:
        """
        Generate cross-domain intelligence across multiple domains.
        
        Args:
            domains: List of domains to analyze
            
        Returns:
            CrossDomainIntelligence with integrated analysis
        """
        try:
            start_time = datetime.now()
            
            # Query knowledge graph across domains
            cross_domain_patterns = await self._query_cross_domain_patterns(domains)
            
            # Identify cross-domain relationships
            cross_domain_relationships = await self._identify_cross_domain_relationships(domains)
            
            # Generate integrated intelligence
            integrated_intelligence = await self._generate_integrated_intelligence(
                domains, cross_domain_patterns, cross_domain_relationships
            )
            
            # Create cross-domain intelligence
            cross_domain_intel = CrossDomainIntelligence(
                analysis_id=f"cross_domain_{datetime.now().isoformat()}",
                domains=domains,
                cross_domain_patterns=cross_domain_patterns,
                integrated_recommendations=integrated_intelligence['recommendations'],
                confidence_score=integrated_intelligence['confidence'],
                timestamp=datetime.now(),
                metadata={
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'patterns_found': len(cross_domain_patterns),
                    'relationships_found': len(cross_domain_relationships)
                }
            )
            
            # Add to queue and trigger callbacks
            self.cross_domain_queue.append(cross_domain_intel)
            await self._trigger_cross_domain_callbacks(cross_domain_intel)
            
            # Update metrics
            self.metrics.cross_domain_analyses += 1
            
            logger.info(f"✅ Generated cross-domain intelligence for {domains}")
            return cross_domain_intel
            
        except Exception as e:
            logger.error(f"Error generating cross-domain intelligence: {e}")
            self.metrics.error_count += 1
            raise
    
    async def _intelligence_generation_loop(self) -> None:
        """Main loop for continuous intelligence generation."""
        while self.is_running:
            try:
                # Process any pending intelligence generation
                await self._process_pending_intelligence()
                
                # Generate periodic intelligence from knowledge graph
                await self._generate_periodic_intelligence()
                
                # Sleep based on configuration
                await asyncio.sleep(self.config['intelligence_generation_interval'])
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in intelligence generation loop: {e}")
                await asyncio.sleep(5.0)
    
    async def _cross_domain_analysis_loop(self) -> None:
        """Main loop for cross-domain analysis."""
        while self.is_running:
            try:
                # Generate cross-domain intelligence for all configured domains
                await self.generate_cross_domain_intelligence(self.config['domains'])
                
                # Sleep based on configuration
                await asyncio.sleep(self.config['cross_domain_analysis_interval'])
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cross-domain analysis loop: {e}")
                await asyncio.sleep(30.0)
    
    async def _process_pending_intelligence(self) -> None:
        """Process any pending intelligence generation tasks."""
        # This would process any queued intelligence generation requests
        # For now, we'll implement basic processing
        pass
    
    async def _generate_periodic_intelligence(self) -> None:
        """Generate periodic intelligence from knowledge graph."""
        try:
            # Query knowledge graph for recent updates
            recent_updates = await self._query_recent_knowledge_graph_updates()
            
            if recent_updates:
                # Generate intelligence for each domain
                for domain in self.config['domains']:
                    domain_intelligence = await self._generate_domain_periodic_intelligence(
                        domain, recent_updates
                    )
                    
                    if domain_intelligence:
                        # Create intelligence stream
                        stream = IntelligenceStream(
                            stream_id=f"periodic_{domain}_{datetime.now().isoformat()}",
                            data_type="periodic_intelligence",
                            timestamp=datetime.now(),
                            intelligence_data=domain_intelligence,
                            confidence_score=domain_intelligence.get('confidence', 0.0),
                            source_domains=[domain],
                            metadata={'generation_type': 'periodic', 'domain': domain}
                        )
                        
                        self.intelligence_queue.append(stream)
                        await self._trigger_intelligence_callbacks(stream)
                        
        except Exception as e:
            logger.error(f"Error generating periodic intelligence: {e}")
    
    async def _update_knowledge_graph(self, processed_data: Any) -> None:
        """Update knowledge graph with new data."""
        try:
            # Create analysis request
            request = AnalysisRequest(
                data_type=processed_data.data_type,
                content=processed_data.content,
                language=processed_data.language or "en"
            )
            
            # Process through knowledge graph integration
            await self.knowledge_graph_integration.process_with_improved_extraction([request.content])
            
            logger.debug(f"Updated knowledge graph with {processed_data.data_type} data")
            
        except Exception as e:
            logger.error(f"Error updating knowledge graph: {e}")
    
    async def _generate_domain_intelligence(self, processed_data: Any) -> Dict[str, Any]:
        """Generate intelligence for specific domain."""
        try:
            # Determine domain from data
            domain = self._determine_domain(processed_data)
            
            # Get domain-specific generator
            generator = self.domain_generators.get(domain, self._generate_general_intelligence)
            
            # Generate intelligence
            intelligence = await generator(processed_data)
            
            return intelligence
            
        except Exception as e:
            logger.error(f"Error generating domain intelligence: {e}")
            return {'confidence': 0.0, 'domains': [], 'error': str(e)}
    
    async def _generate_defense_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate defense intelligence."""
        return {
            'type': 'defense_intelligence',
            'confidence': 0.85,
            'domains': ['defense'],
            'threat_assessment': 'medium',
            'recommendations': ['Increase monitoring', 'Update security protocols'],
            'patterns': ['threat_pattern_1', 'defense_pattern_2']
        }
    
    async def _generate_intelligence_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate intelligence intelligence."""
        return {
            'type': 'intelligence_intelligence',
            'confidence': 0.80,
            'domains': ['intelligence'],
            'intelligence_gaps': ['gap_1', 'gap_2'],
            'recommendations': ['Collect additional data', 'Enhance analysis'],
            'patterns': ['intel_pattern_1', 'intel_pattern_2']
        }
    
    async def _generate_business_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate business intelligence."""
        return {
            'type': 'business_intelligence',
            'confidence': 0.75,
            'domains': ['business'],
            'market_insights': ['insight_1', 'insight_2'],
            'recommendations': ['Market opportunity', 'Risk mitigation'],
            'patterns': ['business_pattern_1', 'business_pattern_2']
        }
    
    async def _generate_cyber_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate cyber intelligence."""
        return {
            'type': 'cyber_intelligence',
            'confidence': 0.90,
            'domains': ['cyber'],
            'threat_level': 'high',
            'recommendations': ['Update firewalls', 'Monitor network traffic'],
            'patterns': ['cyber_pattern_1', 'cyber_pattern_2']
        }
    
    async def _generate_diplomatic_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate diplomatic intelligence."""
        return {
            'type': 'diplomatic_intelligence',
            'confidence': 0.70,
            'domains': ['diplomatic'],
            'diplomatic_relations': ['relation_1', 'relation_2'],
            'recommendations': ['Diplomatic outreach', 'Policy adjustment'],
            'patterns': ['diplomatic_pattern_1', 'diplomatic_pattern_2']
        }
    
    async def _generate_economic_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate economic intelligence."""
        return {
            'type': 'economic_intelligence',
            'confidence': 0.75,
            'domains': ['economic'],
            'economic_indicators': ['indicator_1', 'indicator_2'],
            'recommendations': ['Economic policy', 'Investment strategy'],
            'patterns': ['economic_pattern_1', 'economic_pattern_2']
        }
    
    async def _generate_general_intelligence(self, data: Any) -> Dict[str, Any]:
        """Generate general intelligence for unknown domains."""
        return {
            'type': 'general_intelligence',
            'confidence': 0.60,
            'domains': ['general'],
            'insights': ['general_insight_1', 'general_insight_2'],
            'recommendations': ['General recommendation'],
            'patterns': ['general_pattern_1']
        }
    
    def _determine_domain(self, data: Any) -> str:
        """Determine the domain from data content."""
        # Simple domain detection based on keywords
        content = str(data.content).lower()
        
        domain_keywords = {
            'defense': ['military', 'defense', 'weapon', 'threat', 'security'],
            'intelligence': ['intelligence', 'spy', 'surveillance', 'covert'],
            'business': ['business', 'market', 'trade', 'commerce', 'economic'],
            'cyber': ['cyber', 'hack', 'malware', 'network', 'digital'],
            'diplomatic': ['diplomatic', 'foreign', 'policy', 'relations'],
            'economic': ['economic', 'finance', 'monetary', 'fiscal']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in content for keyword in keywords):
                return domain
        
        return 'general'
    
    async def _query_cross_domain_patterns(self, domains: List[str]) -> List[Dict[str, Any]]:
        """Query knowledge graph for cross-domain patterns."""
        try:
            # This would query the knowledge graph for patterns across domains
            # For now, return mock patterns
            patterns = []
            for domain in domains:
                patterns.append({
                    'domain': domain,
                    'pattern_type': 'cross_domain',
                    'confidence': 0.8,
                    'description': f'Cross-domain pattern for {domain}'
                })
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error querying cross-domain patterns: {e}")
            return []
    
    async def _identify_cross_domain_relationships(self, domains: List[str]) -> List[Dict[str, Any]]:
        """Identify relationships between domains."""
        try:
            # This would analyze relationships between domains
            # For now, return mock relationships
            relationships = []
            for i, domain1 in enumerate(domains):
                for domain2 in domains[i+1:]:
                    relationships.append({
                        'source_domain': domain1,
                        'target_domain': domain2,
                        'relationship_type': 'influences',
                        'confidence': 0.7,
                        'description': f'{domain1} influences {domain2}'
                    })
            
            return relationships
            
        except Exception as e:
            logger.error(f"Error identifying cross-domain relationships: {e}")
            return []
    
    async def _generate_integrated_intelligence(
        self, 
        domains: List[str], 
        patterns: List[Dict[str, Any]], 
        relationships: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate integrated intelligence from cross-domain analysis."""
        try:
            # Combine patterns and relationships
            integrated_insights = []
            for pattern in patterns:
                integrated_insights.append(f"Pattern: {pattern['description']}")
            
            for relationship in relationships:
                integrated_insights.append(f"Relationship: {relationship['description']}")
            
            # Generate recommendations
            recommendations = [
                f"Cross-domain analysis for {', '.join(domains)}",
                "Monitor inter-domain relationships",
                "Update strategic planning based on patterns"
            ]
            
            # Calculate confidence
            confidence = sum(p.get('confidence', 0.0) for p in patterns) / len(patterns) if patterns else 0.0
            
            return {
                'insights': integrated_insights,
                'recommendations': recommendations,
                'confidence': confidence,
                'domains': domains
            }
            
        except Exception as e:
            logger.error(f"Error generating integrated intelligence: {e}")
            return {
                'insights': [],
                'recommendations': ['Error in cross-domain analysis'],
                'confidence': 0.0,
                'domains': domains
            }
    
    async def _query_recent_knowledge_graph_updates(self) -> List[Dict[str, Any]]:
        """Query knowledge graph for recent updates."""
        try:
            # This would query the knowledge graph for recent updates
            # For now, return empty list
            return []
            
        except Exception as e:
            logger.error(f"Error querying recent knowledge graph updates: {e}")
            return []
    
    async def _generate_domain_periodic_intelligence(
        self, 
        domain: str, 
        updates: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Generate periodic intelligence for a specific domain."""
        try:
            # Generate domain-specific periodic intelligence
            generator = self.domain_generators.get(domain, self._generate_general_intelligence)
            
            # Create mock data for periodic generation
            mock_data = type('MockData', (), {
                'content': f'Periodic {domain} intelligence update',
                'data_type': 'periodic',
                'language': 'en'
            })()
            
            return await generator(mock_data)
            
        except Exception as e:
            logger.error(f"Error generating periodic intelligence for {domain}: {e}")
            return None
    
    async def _trigger_intelligence_callbacks(self, stream: IntelligenceStream) -> None:
        """Trigger intelligence generation callbacks."""
        for callback in self.intelligence_callbacks:
            try:
                await callback(stream)
            except Exception as e:
                logger.error(f"Error in intelligence callback: {e}")
    
    async def _trigger_cross_domain_callbacks(self, cross_domain_intel: CrossDomainIntelligence) -> None:
        """Trigger cross-domain intelligence callbacks."""
        for callback in self.cross_domain_callbacks:
            try:
                await callback(cross_domain_intel)
            except Exception as e:
                logger.error(f"Error in cross-domain callback: {e}")
    
    def _update_metrics(self, stream: IntelligenceStream) -> None:
        """Update pipeline metrics."""
        self.metrics.total_intelligence_generated += 1
        self.metrics.last_update = datetime.now()
        
        # Update domain metrics
        for domain in stream.source_domains:
            if domain not in self.metrics.domain_metrics:
                self.metrics.domain_metrics[domain] = {
                    'count': 0,
                    'avg_confidence': 0.0,
                    'last_update': datetime.now()
                }
            
            domain_metric = self.metrics.domain_metrics[domain]
            domain_metric['count'] += 1
            domain_metric['last_update'] = datetime.now()
            
            # Update average confidence
            total_confidence = domain_metric['avg_confidence'] * (domain_metric['count'] - 1) + stream.confidence_score
            domain_metric['avg_confidence'] = total_confidence / domain_metric['count']
    
    def register_intelligence_callback(self, callback: Callable) -> None:
        """Register a callback for intelligence generation."""
        self.intelligence_callbacks.append(callback)
        logger.info("✅ Intelligence callback registered")
    
    def register_cross_domain_callback(self, callback: Callable) -> None:
        """Register a callback for cross-domain intelligence."""
        self.cross_domain_callbacks.append(callback)
        logger.info("✅ Cross-domain callback registered")
    
    async def get_pipeline_status(self) -> Dict[str, Any]:
        """Get the current status of the pipeline."""
        return {
            'is_running': self.is_running,
            'metrics': {
                'total_intelligence_generated': self.metrics.total_intelligence_generated,
                'cross_domain_analyses': self.metrics.cross_domain_analyses,
                'error_count': self.metrics.error_count,
                'last_update': self.metrics.last_update.isoformat(),
                'domain_metrics': self.metrics.domain_metrics
            },
            'queue_sizes': {
                'intelligence_queue': len(self.intelligence_queue),
                'cross_domain_queue': len(self.cross_domain_queue)
            },
            'configuration': self.config
        }
