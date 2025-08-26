"""
Knowledge Graph Intelligence Service
Centralized service for knowledge graph intelligence extraction and analysis.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class StrategicIntelligence:
    """Strategic intelligence extracted from knowledge graph."""
    key_entities: List[str]
    relationships: List[Dict[str, Any]]
    strategic_patterns: List[str]
    risk_indicators: List[str]
    opportunities: List[str]
    historical_insights: List[Dict[str, Any]]
    predictive_trends: List[Dict[str, Any]]
    cross_domain_connections: List[Dict[str, Any]]
    confidence_score: float
    extraction_timestamp: str


@dataclass
class QueryContext:
    """Context for knowledge graph queries."""
    domain: str
    entities: List[str]
    timeframe: str
    geographic_scope: str
    strategic_objectives: List[str]
    constraints: List[str]


class KnowledgeGraphIntelligenceService:
    """Centralized service for knowledge graph intelligence extraction."""
    
    def __init__(self, knowledge_graph_agent=None):
        self.knowledge_graph_agent = knowledge_graph_agent
        self.intelligence_cache = {}
        self.pattern_cache = {}
        
        logger.info("Knowledge Graph Intelligence Service initialized")
    
    async def extract_strategic_intelligence(self, query_context: Dict[str, Any]) -> StrategicIntelligence:
        """Extract strategic intelligence from knowledge graph based on query context."""
        try:
            # Extract context parameters
            domain = query_context.get("domain", "general")
            entities = query_context.get("entities", [])
            timeframe = query_context.get("timeframe", "1y")
            geographic_scope = query_context.get("geographic_scope", "global")
            strategic_objectives = query_context.get("strategic_objectives", [])
            constraints = query_context.get("constraints", [])
            
            # Query knowledge graph for strategic intelligence
            kg_intelligence = await self._query_strategic_intelligence(domain, entities, timeframe)
            
            # Extract key entities and relationships
            key_entities = await self._extract_key_entities(domain, entities)
            relationships = await self._extract_relationships(domain, entities)
            
            # Analyze strategic patterns
            strategic_patterns = await self._analyze_strategic_patterns(domain, timeframe)
            
            # Identify risk indicators
            risk_indicators = await self._identify_risk_indicators(domain, entities)
            
            # Identify opportunities
            opportunities = await self._identify_opportunities(domain, entities)
            
            # Extract historical insights
            historical_insights = await self._extract_historical_insights(domain, timeframe)
            
            # Generate predictive trends
            predictive_trends = await self._generate_predictive_trends(domain, entities)
            
            # Generate cross-domain connections
            cross_domain_connections = await self._generate_cross_domain_connections(domain, entities)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                kg_intelligence, key_entities, relationships, strategic_patterns
            )
            
            return StrategicIntelligence(
                key_entities=key_entities,
                relationships=relationships,
                strategic_patterns=strategic_patterns,
                risk_indicators=risk_indicators,
                opportunities=opportunities,
                historical_insights=historical_insights,
                predictive_trends=predictive_trends,
                cross_domain_connections=cross_domain_connections,
                confidence_score=confidence_score,
                extraction_timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error extracting strategic intelligence: {e}")
            return self._create_default_intelligence()
    
    async def _query_strategic_intelligence(self, domain: str, entities: List[str], timeframe: str) -> Dict[str, Any]:
        """Query knowledge graph for strategic intelligence."""
        try:
            if not self.knowledge_graph_agent:
                logger.warning("Knowledge graph agent not available")
                return {}
            
            # Construct query based on domain and entities
            if domain == "military":
                query = f"military strategic intelligence for {', '.join(entities)} in {timeframe}"
            elif domain == "business":
                query = f"business strategic intelligence for {', '.join(entities)} in {timeframe}"
            elif domain == "intelligence":
                query = f"intelligence strategic intelligence for {', '.join(entities)} in {timeframe}"
            else:
                query = f"strategic intelligence for {domain} domain entities {', '.join(entities)} in {timeframe}"
            
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            if result and isinstance(result, dict):
                logger.info(f"Successfully queried strategic intelligence for {domain} domain")
                return result
            else:
                logger.warning(f"Invalid result format for strategic intelligence query: {domain}")
                return {}
                
        except Exception as e:
            logger.error(f"Error querying strategic intelligence: {e}")
            return {}
    
    async def _extract_key_entities(self, domain: str, entities: List[str]) -> List[str]:
        """Extract key entities from knowledge graph."""
        try:
            if not self.knowledge_graph_agent:
                return entities
            
            # Query for key entities in the domain
            query = f"key entities in {domain} domain related to {', '.join(entities)}"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            # Extract entities from result
            key_entities = entities.copy()  # Start with provided entities
            
            if result and isinstance(result, dict):
                # Extract additional entities from knowledge graph result
                if "entities" in result:
                    key_entities.extend(result["entities"])
                elif "nodes" in result:
                    key_entities.extend(result["nodes"])
            
            # Remove duplicates and return
            return list(set(key_entities))
            
        except Exception as e:
            logger.error(f"Error extracting key entities: {e}")
            return entities
    
    async def _extract_relationships(self, domain: str, entities: List[str]) -> List[Dict[str, Any]]:
        """Extract relationships from knowledge graph."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for relationships between entities
            query = f"relationships between entities {', '.join(entities)} in {domain} domain"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            relationships = []
            
            if result and isinstance(result, dict):
                # Extract relationships from result
                if "relationships" in result:
                    relationships = result["relationships"]
                elif "edges" in result:
                    relationships = result["edges"]
                elif "connections" in result:
                    relationships = result["connections"]
            
            return relationships
            
        except Exception as e:
            logger.error(f"Error extracting relationships: {e}")
            return []
    
    async def _analyze_strategic_patterns(self, domain: str, timeframe: str) -> List[str]:
        """Analyze strategic patterns from knowledge graph data."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for strategic patterns
            query = f"strategic patterns in {domain} domain over {timeframe}"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            patterns = []
            
            if result and isinstance(result, dict):
                # Extract patterns from result
                if "patterns" in result:
                    patterns = result["patterns"]
                elif "strategic_patterns" in result:
                    patterns = result["strategic_patterns"]
                elif "trends" in result:
                    patterns = result["trends"]
            
            # Convert to list of strings if needed
            if patterns and isinstance(patterns, list):
                if isinstance(patterns[0], dict):
                    patterns = [p.get("name", p.get("type", str(p))) for p in patterns]
                elif isinstance(patterns[0], str):
                    patterns = patterns
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing strategic patterns: {e}")
            return []
    
    async def _identify_risk_indicators(self, domain: str, entities: List[str]) -> List[str]:
        """Identify risk indicators from knowledge graph data."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for risk indicators
            query = f"risk indicators for {', '.join(entities)} in {domain} domain"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            risk_indicators = []
            
            if result and isinstance(result, dict):
                # Extract risk indicators from result
                if "risks" in result:
                    risk_indicators = result["risks"]
                elif "risk_indicators" in result:
                    risk_indicators = result["risk_indicators"]
                elif "threats" in result:
                    risk_indicators = result["threats"]
            
            # Convert to list of strings if needed
            if risk_indicators and isinstance(risk_indicators, list):
                if isinstance(risk_indicators[0], dict):
                    risk_indicators = [r.get("name", r.get("type", str(r))) for r in risk_indicators]
                elif isinstance(risk_indicators[0], str):
                    risk_indicators = risk_indicators
            
            return risk_indicators
            
        except Exception as e:
            logger.error(f"Error identifying risk indicators: {e}")
            return []
    
    async def _identify_opportunities(self, domain: str, entities: List[str]) -> List[str]:
        """Identify opportunities from knowledge graph data."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for opportunities
            query = f"opportunities for {', '.join(entities)} in {domain} domain"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            opportunities = []
            
            if result and isinstance(result, dict):
                # Extract opportunities from result
                if "opportunities" in result:
                    opportunities = result["opportunities"]
                elif "advantages" in result:
                    opportunities = result["advantages"]
                elif "strengths" in result:
                    opportunities = result["strengths"]
            
            # Convert to list of strings if needed
            if opportunities and isinstance(opportunities, list):
                if isinstance(opportunities[0], dict):
                    opportunities = [o.get("name", o.get("type", str(o))) for o in opportunities]
                elif isinstance(opportunities[0], str):
                    opportunities = opportunities
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error identifying opportunities: {e}")
            return []
    
    async def _extract_historical_insights(self, domain: str, timeframe: str) -> List[Dict[str, Any]]:
        """Extract historical insights from knowledge graph data."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for historical insights
            query = f"historical insights for {domain} domain over {timeframe}"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            historical_insights = []
            
            if result and isinstance(result, dict):
                # Extract historical insights from result
                if "historical_insights" in result:
                    historical_insights = result["historical_insights"]
                elif "historical_data" in result:
                    historical_insights = result["historical_data"]
                elif "insights" in result:
                    historical_insights = result["insights"]
            
            # Ensure it's a list of dictionaries
            if historical_insights and isinstance(historical_insights, list):
                if not isinstance(historical_insights[0], dict):
                    historical_insights = [{"insight": str(insight)} for insight in historical_insights]
            else:
                historical_insights = []
            
            return historical_insights
            
        except Exception as e:
            logger.error(f"Error extracting historical insights: {e}")
            return []
    
    async def _generate_predictive_trends(self, domain: str, entities: List[str]) -> List[Dict[str, Any]]:
        """Generate predictive trends from knowledge graph data."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for predictive trends
            query = f"predictive trends for {', '.join(entities)} in {domain} domain"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            predictive_trends = []
            
            if result and isinstance(result, dict):
                # Extract predictive trends from result
                if "predictions" in result:
                    predictive_trends = result["predictions"]
                elif "trends" in result:
                    predictive_trends = result["trends"]
                elif "forecasts" in result:
                    predictive_trends = result["forecasts"]
            
            # Ensure it's a list of dictionaries
            if predictive_trends and isinstance(predictive_trends, list):
                if not isinstance(predictive_trends[0], dict):
                    predictive_trends = [{"trend": str(trend)} for trend in predictive_trends]
            else:
                predictive_trends = []
            
            return predictive_trends
            
        except Exception as e:
            logger.error(f"Error generating predictive trends: {e}")
            return []
    
    async def _generate_cross_domain_connections(self, domain: str, entities: List[str]) -> List[Dict[str, Any]]:
        """Generate cross-domain connections from knowledge graph data."""
        try:
            if not self.knowledge_graph_agent:
                return []
            
            # Query for cross-domain connections
            query = f"cross-domain connections for {', '.join(entities)} in {domain} domain"
            result = await self.knowledge_graph_agent.query_knowledge_graph(query)
            
            cross_domain_connections = []
            
            if result and isinstance(result, dict):
                # Extract cross-domain connections from result
                if "cross_domain_connections" in result:
                    cross_domain_connections = result["cross_domain_connections"]
                elif "connections" in result:
                    cross_domain_connections = result["connections"]
                elif "relationships" in result:
                    cross_domain_connections = result["relationships"]
            
            # Ensure it's a list of dictionaries
            if cross_domain_connections and isinstance(cross_domain_connections, list):
                if not isinstance(cross_domain_connections[0], dict):
                    cross_domain_connections = [{"connection": str(conn)} for conn in cross_domain_connections]
            else:
                cross_domain_connections = []
            
            return cross_domain_connections
            
        except Exception as e:
            logger.error(f"Error generating cross-domain connections: {e}")
            return []
    
    def _calculate_confidence_score(self, kg_intelligence: Dict[str, Any], 
                                  key_entities: List[str], 
                                  relationships: List[Dict[str, Any]], 
                                  strategic_patterns: List[str]) -> float:
        """Calculate confidence score for the extracted intelligence."""
        try:
            # Base confidence score
            confidence = 0.5
            
            # Adjust based on knowledge graph intelligence quality
            if kg_intelligence and len(kg_intelligence) > 0:
                confidence += 0.2
            
            # Adjust based on number of key entities
            if len(key_entities) > 0:
                confidence += min(0.1, len(key_entities) * 0.02)
            
            # Adjust based on number of relationships
            if len(relationships) > 0:
                confidence += min(0.1, len(relationships) * 0.02)
            
            # Adjust based on number of strategic patterns
            if len(strategic_patterns) > 0:
                confidence += min(0.1, len(strategic_patterns) * 0.02)
            
            # Cap confidence at 1.0
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def _create_default_intelligence(self) -> StrategicIntelligence:
        """Create default strategic intelligence when extraction fails."""
        return StrategicIntelligence(
            key_entities=[],
            relationships=[],
            strategic_patterns=[],
            risk_indicators=[],
            opportunities=[],
            historical_insights=[],
            predictive_trends=[],
            cross_domain_connections=[],
            confidence_score=0.0,
            extraction_timestamp=datetime.now().isoformat()
        )
    
    async def get_cached_intelligence(self, cache_key: str) -> Optional[StrategicIntelligence]:
        """Get cached intelligence if available and not expired."""
        try:
            if cache_key in self.intelligence_cache:
                cached_intelligence = self.intelligence_cache[cache_key]
                
                # Check if cache is still valid (24 hours)
                cache_timestamp = datetime.fromisoformat(cached_intelligence.extraction_timestamp)
                if (datetime.now() - cache_timestamp).total_seconds() < 86400:  # 24 hours
                    logger.info(f"Returning cached intelligence for key: {cache_key}")
                    return cached_intelligence
                else:
                    # Remove expired cache
                    del self.intelligence_cache[cache_key]
            
            return None
            
        except Exception as e:
            logger.error(f"Error accessing cached intelligence: {e}")
            return None
    
    def cache_intelligence(self, cache_key: str, intelligence: StrategicIntelligence) -> None:
        """Cache strategic intelligence for future use."""
        try:
            self.intelligence_cache[cache_key] = intelligence
            logger.info(f"Cached intelligence for key: {cache_key}")
        except Exception as e:
            logger.error(f"Error caching intelligence: {e}")
    
    def export_intelligence_report(self, intelligence: StrategicIntelligence) -> Dict[str, Any]:
        """Export strategic intelligence as a report."""
        return {
            "intelligence_metadata": {
                "extraction_timestamp": intelligence.extraction_timestamp,
                "confidence_score": intelligence.confidence_score,
                "total_entities": len(intelligence.key_entities),
                "total_relationships": len(intelligence.relationships),
                "total_patterns": len(intelligence.strategic_patterns)
            },
            "strategic_intelligence": asdict(intelligence),
            "summary": {
                "key_insights": intelligence.strategic_patterns[:5],  # Top 5 patterns
                "critical_risks": intelligence.risk_indicators[:3],   # Top 3 risks
                "key_opportunities": intelligence.opportunities[:3],  # Top 3 opportunities
                "historical_context": len(intelligence.historical_insights),
                "predictive_insights": len(intelligence.predictive_trends)
            }
        }
