"""
Enhanced Knowledge Graph Integration for Data.gov API
Phase 2 Implementation - Advanced Relationship Management & Graph Analytics
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import json

from src.core.knowledge_graph_integration import KnowledgeGraphService
from src.config.datagov_config import DataGovConfig

logger = logging.getLogger(__name__)


class DataGovKnowledgeGraphIntegration:
    """
    Enhanced knowledge graph integration for Data.gov data.
    Provides advanced relationship management, graph analytics, and pattern discovery.
    """
    
    def __init__(self):
        self.config = DataGovConfig()
        self.knowledge_graph = KnowledgeGraphService()
        self.logger = logging.getLogger(__name__)
        
        # Node labels for different entity types
        self.node_labels = {
            'country': 'Country',
            'trade_data': 'TradeData',
            'economic_data': 'EconomicData',
            'environmental_data': 'EnvironmentalData',
            'commodity': 'Commodity',
            'time_period': 'TimePeriod',
            'policy': 'Policy',
            'trend': 'Trend'
        }
        
        # Relationship types
        self.relationship_types = {
            'has_trade_data': 'HAS_TRADE_DATA',
            'has_economic_data': 'HAS_ECONOMIC_DATA',
            'has_environmental_data': 'HAS_ENVIRONMENTAL_DATA',
            'trades_in': 'TRADES_IN',
            'imports_from': 'IMPORTS_FROM',
            'exports_to': 'EXPORTS_TO',
            'correlates_with': 'CORRELATES_WITH',
            'influences': 'INFLUENCES',
            'follows_trend': 'FOLLOWS_TREND',
            'implements_policy': 'IMPLEMENTS_POLICY'
        }
    
    async def create_country_node(self, country_code: str, country_name: Optional[str] = None) -> bool:
        """
        Create or update a country node in the knowledge graph.
        
        Args:
            country_code: ISO country code
            country_name: Full country name (optional)
            
        Returns:
            bool: Success status
        """
        try:
            properties = {
                "code": country_code,
                "name": country_name or country_code,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            await self.knowledge_graph.create_node(
                label=self.node_labels['country'],
                properties=properties
            )
            
            self.logger.info(f"Created/updated country node: {country_code}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating country node {country_code}: {e}")
            return False
    
    async def create_trade_data_node(self, trade_data: Dict[str, Any]) -> str:
        """
        Create a trade data node in the knowledge graph.
        
        Args:
            trade_data: Trade data dictionary
            
        Returns:
            str: Node ID
        """
        try:
            properties = {
                "date": trade_data.get('date', '').isoformat() if hasattr(trade_data.get('date', ''), 'isoformat') else str(trade_data.get('date', '')),
                "trade_value": trade_data.get('trade_value', 0),
                "commodity_code": trade_data.get('commodity_code', ''),
                "trade_type": trade_data.get('trade_type', ''),
                "currency": trade_data.get('currency', 'USD'),
                "created_at": datetime.utcnow().isoformat()
            }
            
            node_id = await self.knowledge_graph.create_node(
                label=self.node_labels['trade_data'],
                properties=properties
            )
            
            self.logger.info(f"Created trade data node: {node_id}")
            return node_id
            
        except Exception as e:
            self.logger.error(f"Error creating trade data node: {e}")
            return ""
    
    async def create_economic_data_node(self, economic_data: Dict[str, Any]) -> str:
        """
        Create an economic data node in the knowledge graph.
        
        Args:
            economic_data: Economic data dictionary
            
        Returns:
            str: Node ID
        """
        try:
            properties = {
                "date": economic_data.get('date', '').isoformat() if hasattr(economic_data.get('date', ''), 'isoformat') else str(economic_data.get('date', '')),
                "gdp": economic_data.get('gdp', 0),
                "population": economic_data.get('population', 0),
                "gdp_per_capita": economic_data.get('gdp_per_capita', 0),
                "currency": economic_data.get('currency', 'USD'),
                "created_at": datetime.utcnow().isoformat()
            }
            
            node_id = await self.knowledge_graph.create_node(
                label=self.node_labels['economic_data'],
                properties=properties
            )
            
            self.logger.info(f"Created economic data node: {node_id}")
            return node_id
            
        except Exception as e:
            self.logger.error(f"Error creating economic data node: {e}")
            return ""
    
    async def create_environmental_data_node(self, environmental_data: Dict[str, Any]) -> str:
        """
        Create an environmental data node in the knowledge graph.
        
        Args:
            environmental_data: Environmental data dictionary
            
        Returns:
            str: Node ID
        """
        try:
            properties = {
                "date": environmental_data.get('date', '').isoformat() if hasattr(environmental_data.get('date', ''), 'isoformat') else str(environmental_data.get('date', '')),
                "epi_score": environmental_data.get('epi_score', 0),
                "air_quality": environmental_data.get('air_quality', 0),
                "water_quality": environmental_data.get('water_quality', 0),
                "biodiversity": environmental_data.get('biodiversity', 0),
                "created_at": datetime.utcnow().isoformat()
            }
            
            node_id = await self.knowledge_graph.create_node(
                label=self.node_labels['environmental_data'],
                properties=properties
            )
            
            self.logger.info(f"Created environmental data node: {node_id}")
            return node_id
            
        except Exception as e:
            self.logger.error(f"Error creating environmental data node: {e}")
            return ""
    
    async def create_trade_relationships(self, country_code: str, trade_records: List[Dict[str, Any]]) -> int:
        """
        Create trade relationships for a country.
        
        Args:
            country_code: Country code
            trade_records: List of trade data records
            
        Returns:
            int: Number of relationships created
        """
        try:
            relationship_count = 0
            
            # Create country node if it doesn't exist
            await self.create_country_node(country_code)
            
            for trade_record in trade_records:
                # Create trade data node
                trade_node_id = await self.create_trade_data_node(trade_record)
                
                if trade_node_id:
                    # Create relationship between country and trade data
                    await self.knowledge_graph.create_relationship(
                        from_label=self.node_labels['country'],
                        from_properties={"code": country_code},
                        to_label=self.node_labels['trade_data'],
                        to_properties={"id": trade_node_id},
                        relationship_type=self.relationship_types['has_trade_data']
                    )
                    
                    # Create commodity relationship if commodity code exists
                    if trade_record.get('commodity_code'):
                        await self.create_commodity_relationship(trade_node_id, trade_record['commodity_code'])
                    
                    relationship_count += 1
            
            self.logger.info(f"Created {relationship_count} trade relationships for {country_code}")
            return relationship_count
            
        except Exception as e:
            self.logger.error(f"Error creating trade relationships for {country_code}: {e}")
            return 0
    
    async def create_economic_relationships(self, country_code: str, economic_records: List[Dict[str, Any]]) -> int:
        """
        Create economic relationships for a country.
        
        Args:
            country_code: Country code
            economic_records: List of economic data records
            
        Returns:
            int: Number of relationships created
        """
        try:
            relationship_count = 0
            
            # Create country node if it doesn't exist
            await self.create_country_node(country_code)
            
            for economic_record in economic_records:
                # Create economic data node
                economic_node_id = await self.create_economic_data_node(economic_record)
                
                if economic_node_id:
                    # Create relationship between country and economic data
                    await self.knowledge_graph.create_relationship(
                        from_label=self.node_labels['country'],
                        from_properties={"code": country_code},
                        to_label=self.node_labels['economic_data'],
                        to_properties={"id": economic_node_id},
                        relationship_type=self.relationship_types['has_economic_data']
                    )
                    
                    relationship_count += 1
            
            self.logger.info(f"Created {relationship_count} economic relationships for {country_code}")
            return relationship_count
            
        except Exception as e:
            self.logger.error(f"Error creating economic relationships for {country_code}: {e}")
            return 0
    
    async def create_environmental_relationships(self, country_code: str, environmental_records: List[Dict[str, Any]]) -> int:
        """
        Create environmental relationships for a country.
        
        Args:
            country_code: Country code
            environmental_records: List of environmental data records
            
        Returns:
            int: Number of relationships created
        """
        try:
            relationship_count = 0
            
            # Create country node if it doesn't exist
            await self.create_country_node(country_code)
            
            for environmental_record in environmental_records:
                # Create environmental data node
                environmental_node_id = await self.create_environmental_data_node(environmental_record)
                
                if environmental_node_id:
                    # Create relationship between country and environmental data
                    await self.knowledge_graph.create_relationship(
                        from_label=self.node_labels['country'],
                        from_properties={"code": country_code},
                        to_label=self.node_labels['environmental_data'],
                        to_properties={"id": environmental_node_id},
                        relationship_type=self.relationship_types['has_environmental_data']
                    )
                    
                    relationship_count += 1
            
            self.logger.info(f"Created {relationship_count} environmental relationships for {country_code}")
            return relationship_count
            
        except Exception as e:
            self.logger.error(f"Error creating environmental relationships for {country_code}: {e}")
            return 0
    
    async def create_commodity_relationship(self, trade_node_id: str, commodity_code: str) -> bool:
        """
        Create relationship between trade data and commodity.
        
        Args:
            trade_node_id: Trade data node ID
            commodity_code: Commodity code
            
        Returns:
            bool: Success status
        """
        try:
            # Create commodity node
            await self.knowledge_graph.create_node(
                label=self.node_labels['commodity'],
                properties={
                    "code": commodity_code,
                    "created_at": datetime.utcnow().isoformat()
                }
            )
            
            # Create relationship
            await self.knowledge_graph.create_relationship(
                from_label=self.node_labels['trade_data'],
                from_properties={"id": trade_node_id},
                to_label=self.node_labels['commodity'],
                to_properties={"code": commodity_code},
                relationship_type=self.relationship_types['trades_in']
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating commodity relationship: {e}")
            return False
    
    async def create_correlation_relationships(self, country_code: str, correlations: List[Dict[str, Any]]) -> int:
        """
        Create correlation relationships between different data types.
        
        Args:
            country_code: Country code
            correlations: List of correlation data
            
        Returns:
            int: Number of correlation relationships created
        """
        try:
            relationship_count = 0
            
            for correlation in correlations:
                # Create correlation relationship
                await self.knowledge_graph.create_relationship(
                    from_label=correlation.get('from_label', self.node_labels['country']),
                    from_properties=correlation.get('from_properties', {"code": country_code}),
                    to_label=correlation.get('to_label', self.node_labels['country']),
                    to_properties=correlation.get('to_properties', {"code": country_code}),
                    relationship_type=self.relationship_types['correlates_with'],
                    properties={
                        "correlation_coefficient": correlation.get('correlation_coefficient', 0),
                        "p_value": correlation.get('p_value', 0),
                        "created_at": datetime.utcnow().isoformat()
                    }
                )
                
                relationship_count += 1
            
            self.logger.info(f"Created {relationship_count} correlation relationships for {country_code}")
            return relationship_count
            
        except Exception as e:
            self.logger.error(f"Error creating correlation relationships for {country_code}: {e}")
            return 0
    
    async def find_related_countries(self, country_code: str, relationship_type: str = None) -> List[Dict[str, Any]]:
        """
        Find countries related to the specified country.
        
        Args:
            country_code: Country code
            relationship_type: Type of relationship to search for
            
        Returns:
            List[Dict[str, Any]]: Related countries
        """
        try:
            query = f"""
            MATCH (c1:{self.node_labels['country']} {{code: $country_code}})
            -[r{':' + relationship_type if relationship_type else ''}]-
            (c2:{self.node_labels['country']})
            RETURN c2.code as country_code, c2.name as country_name, type(r) as relationship_type
            """
            
            results = await self.knowledge_graph.execute_query(query, {"country_code": country_code})
            return results
            
        except Exception as e:
            self.logger.error(f"Error finding related countries for {country_code}: {e}")
            return []
    
    async def get_country_data_summary(self, country_code: str) -> Dict[str, Any]:
        """
        Get comprehensive data summary for a country.
        
        Args:
            country_code: Country code
            
        Returns:
            Dict[str, Any]: Country data summary
        """
        try:
            summary = {
                "country_code": country_code,
                "trade_data_count": 0,
                "economic_data_count": 0,
                "environmental_data_count": 0,
                "commodities": [],
                "date_range": {},
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Count trade data
            trade_query = f"""
            MATCH (c:{self.node_labels['country']} {{code: $country_code}})
            -[:{self.relationship_types['has_trade_data']}]->
            (t:{self.node_labels['trade_data']})
            RETURN count(t) as count
            """
            trade_result = await self.knowledge_graph.execute_query(trade_query, {"country_code": country_code})
            if trade_result:
                summary["trade_data_count"] = trade_result[0].get("count", 0)
            
            # Count economic data
            economic_query = f"""
            MATCH (c:{self.node_labels['country']} {{code: $country_code}})
            -[:{self.relationship_types['has_economic_data']}]->
            (e:{self.node_labels['economic_data']})
            RETURN count(e) as count
            """
            economic_result = await self.knowledge_graph.execute_query(economic_query, {"country_code": country_code})
            if economic_result:
                summary["economic_data_count"] = economic_result[0].get("count", 0)
            
            # Count environmental data
            environmental_query = f"""
            MATCH (c:{self.node_labels['country']} {{code: $country_code}})
            -[:{self.relationship_types['has_environmental_data']}]->
            (env:{self.node_labels['environmental_data']})
            RETURN count(env) as count
            """
            environmental_result = await self.knowledge_graph.execute_query(environmental_query, {"country_code": country_code})
            if environmental_result:
                summary["environmental_data_count"] = environmental_result[0].get("count", 0)
            
            # Get unique commodities
            commodity_query = f"""
            MATCH (c:{self.node_labels['country']} {{code: $country_code}})
            -[:{self.relationship_types['has_trade_data']}]->
            (t:{self.node_labels['trade_data']})
            -[:{self.relationship_types['trades_in']}]->
            (com:{self.node_labels['commodity']})
            RETURN DISTINCT com.code as commodity_code
            """
            commodity_result = await self.knowledge_graph.execute_query(commodity_query, {"country_code": country_code})
            summary["commodities"] = [item.get("commodity_code") for item in commodity_result]
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting country data summary for {country_code}: {e}")
            return {"error": str(e)}
    
    async def find_trends(self, country_code: str, data_type: str, time_period: str = "1Y") -> List[Dict[str, Any]]:
        """
        Find trends in data for a specific country.
        
        Args:
            country_code: Country code
            data_type: Type of data to analyze
            time_period: Time period for trend analysis
            
        Returns:
            List[Dict[str, Any]]: Trend analysis results
        """
        try:
            if data_type == "trade":
                query = f"""
                MATCH (c:{self.node_labels['country']} {{code: $country_code}})
                -[:{self.relationship_types['has_trade_data']}]->
                (t:{self.node_labels['trade_data']})
                WHERE t.date >= datetime() - duration({{days: $days}})
                RETURN t.date as date, t.trade_value as value, t.commodity_code as commodity
                ORDER BY t.date
                """
            elif data_type == "economic":
                query = f"""
                MATCH (c:{self.node_labels['country']} {{code: $country_code}})
                -[:{self.relationship_types['has_economic_data']}]->
                (e:{self.node_labels['economic_data']})
                WHERE e.date >= datetime() - duration({{days: $days}})
                RETURN e.date as date, e.gdp as gdp, e.population as population, e.gdp_per_capita as gdp_per_capita
                ORDER BY e.date
                """
            elif data_type == "environmental":
                query = f"""
                MATCH (c:{self.node_labels['country']} {{code: $country_code}})
                -[:{self.relationship_types['has_environmental_data']}]->
                (env:{self.node_labels['environmental_data']})
                WHERE env.date >= datetime() - duration({{days: $days}})
                RETURN env.date as date, env.epi_score as epi_score, env.air_quality as air_quality
                ORDER BY env.date
                """
            else:
                return []
            
            # Calculate days based on time period
            days_map = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365, "2Y": 730}
            days = days_map.get(time_period, 365)
            
            results = await self.knowledge_graph.execute_query(query, {
                "country_code": country_code,
                "days": days
            })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error finding trends for {country_code}: {e}")
            return []
    
    async def find_correlations(self, country_code: str, metric1: str, metric2: str) -> Dict[str, Any]:
        """
        Find correlations between two metrics for a country.
        
        Args:
            country_code: Country code
            metric1: First metric name
            metric2: Second metric name
            
        Returns:
            Dict[str, Any]: Correlation analysis results
        """
        try:
            # This would require more complex Cypher queries and statistical analysis
            # For now, return a placeholder structure
            correlation_result = {
                "country_code": country_code,
                "metric1": metric1,
                "metric2": metric2,
                "correlation_coefficient": 0.0,
                "p_value": 0.0,
                "sample_size": 0,
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
            
            # TODO: Implement actual correlation analysis using Cypher queries
            # This would involve querying the graph for both metrics and calculating correlations
            
            return correlation_result
            
        except Exception as e:
            self.logger.error(f"Error finding correlations for {country_code}: {e}")
            return {"error": str(e)}
    
    async def get_graph_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the knowledge graph.
        
        Returns:
            Dict[str, Any]: Graph statistics
        """
        try:
            stats = {
                "total_nodes": 0,
                "total_relationships": 0,
                "node_counts": {},
                "relationship_counts": {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Count nodes by label
            for label_name, label in self.node_labels.items():
                query = f"MATCH (n:{label}) RETURN count(n) as count"
                result = await self.knowledge_graph.execute_query(query)
                if result:
                    count = result[0].get("count", 0)
                    stats["node_counts"][label_name] = count
                    stats["total_nodes"] += count
            
            # Count relationships by type
            for rel_name, rel_type in self.relationship_types.items():
                query = f"MATCH ()-[r:{rel_type}]->() RETURN count(r) as count"
                result = await self.knowledge_graph.execute_query(query)
                if result:
                    count = result[0].get("count", 0)
                    stats["relationship_counts"][rel_name] = count
                    stats["total_relationships"] += count
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting graph statistics: {e}")
            return {"error": str(e)}
    
    async def cleanup_old_data(self, days_old: int = 30) -> Dict[str, int]:
        """
        Clean up old data from the knowledge graph.
        
        Args:
            days_old: Remove data older than this many days
            
        Returns:
            Dict[str, int]: Number of nodes/relationships removed
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            cleanup_results = {
                "nodes_removed": 0,
                "relationships_removed": 0
            }
            
            # Remove old data nodes
            data_labels = [self.node_labels['trade_data'], self.node_labels['economic_data'], self.node_labels['environmental_data']]
            
            for label in data_labels:
                query = f"""
                MATCH (n:{label})
                WHERE n.created_at < $cutoff_date
                DETACH DELETE n
                """
                result = await self.knowledge_graph.execute_query(query, {"cutoff_date": cutoff_date.isoformat()})
                # Note: The actual count of deleted nodes would need to be tracked differently
            
            self.logger.info(f"Cleaned up old data from knowledge graph")
            return cleanup_results
            
        except Exception as e:
            self.logger.error(f"Error during knowledge graph cleanup: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on knowledge graph integration."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "node_count": 0,
                "relationship_count": 0
            }
            
            # Check basic connectivity
            try:
                stats = await self.get_graph_statistics()
                health_status["node_count"] = stats.get("total_nodes", 0)
                health_status["relationship_count"] = stats.get("total_relationships", 0)
            except Exception as e:
                health_status["status"] = "unhealthy"
                health_status["error"] = str(e)
            
            return health_status
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
