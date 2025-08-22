"""
Data.gov Data Ingestion Manager
Handles API connections and data fetching from various Data.gov services.
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

from src.core.datagov.api_connectors import (
    CensusTradeAPI,
    USDAMacroAPI,
    USITCGravityAPI,
    EPIEnvironmentalAPI
)
from src.core.vector_db import VectorDBManager
from src.core.knowledge_graph_integration import KnowledgeGraphService

logger = logging.getLogger(__name__)


class DataIngestionManager:
    """Manages data ingestion from Data.gov APIs."""
    
    def __init__(self):
        self.census_api = CensusTradeAPI()
        self.usda_api = USDAMacroAPI()
        self.usitc_api = USITCGravityAPI()
        self.epi_api = EPIEnvironmentalAPI()
        self.vector_db = VectorDBManager()
        self.knowledge_graph = KnowledgeGraphService()
        self.logger = logging.getLogger(__name__)
    
    async def fetch_live_data(self, country_codes: List[str]) -> Dict[str, Any]:
        """Fetch live data from all Data.gov APIs for specified countries."""
        try:
            self.logger.info(f"Fetching live data for countries: {country_codes}")
            
            # Parallel API calls for real-time data
            tasks = [
                self.census_api.get_trade_data(country_codes),
                self.usda_api.get_macroeconomic_data(country_codes),
                self.usitc_api.get_gravity_model_data(country_codes),
                self.epi_api.get_environmental_data(country_codes)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle any exceptions
            data = {}
            api_names = ["census", "usda", "usitc", "epi"]
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"API {api_names[i]} failed: {result}")
                    data[api_names[i]] = {"error": str(result)}
                else:
                    data[api_names[i]] = result
            
            self.logger.info(f"Successfully fetched data from {len([r for r in results if not isinstance(r, Exception)])} APIs")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to fetch live data: {e}")
            raise
    
    async def fetch_trade_data(self, countries: List[str], time_period: str = "latest") -> Dict[str, Any]:
        """Fetch trade data from Census API."""
        try:
            self.logger.info(f"Fetching trade data for countries: {countries}")
            return await self.census_api.get_trade_data(countries, time_period)
        except Exception as e:
            self.logger.error(f"Failed to fetch trade data: {e}")
            return {"error": str(e)}
    
    async def fetch_economic_data(self, countries: List[str]) -> Dict[str, Any]:
        """Fetch economic data from USDA API."""
        try:
            self.logger.info(f"Fetching economic data for countries: {countries}")
            return await self.usda_api.get_macroeconomic_data(countries)
        except Exception as e:
            self.logger.error(f"Failed to fetch economic data: {e}")
            return {"error": str(e)}
    
    async def fetch_environmental_data(self, countries: List[str]) -> Dict[str, Any]:
        """Fetch environmental data from EPI API."""
        try:
            self.logger.info(f"Fetching environmental data for countries: {countries}")
            return await self.epi_api.get_environmental_data(countries)
        except Exception as e:
            self.logger.error(f"Failed to fetch environmental data: {e}")
            return {"error": str(e)}
    
    async def fetch_gravity_model_data(self, countries: List[str]) -> Dict[str, Any]:
        """Fetch gravity model data from USITC API."""
        try:
            self.logger.info(f"Fetching gravity model data for countries: {countries}")
            return await self.usitc_api.get_gravity_model_data(countries)
        except Exception as e:
            self.logger.error(f"Failed to fetch gravity model data: {e}")
            return {"error": str(e)}
    
    async def store_embeddings(self, data: Dict[str, Any]) -> List[str]:
        """Store data embeddings in vector database."""
        try:
            self.logger.info("Storing embeddings in vector database")
            
            # Generate embeddings for the data
            embeddings = await self._generate_embeddings(data)
            
            # Store in vector database
            embedding_ids = await self.vector_db.store_datagov_embeddings(embeddings)
            
            self.logger.info(f"Stored {len(embedding_ids)} embeddings")
            return embedding_ids
            
        except Exception as e:
            self.logger.error(f"Failed to store embeddings: {e}")
            return []
    
    async def create_relationships(self, data: Dict[str, Any]) -> List[str]:
        """Create knowledge graph relationships from data."""
        try:
            self.logger.info("Creating knowledge graph relationships")
            
            # Extract entities and relationships from data
            entities = await self._extract_entities(data)
            relationships = await self._extract_relationships(data)
            
            # Add to knowledge graph
            entity_ids = await self.knowledge_graph.add_datagov_entities(entities)
            relationship_ids = await self.knowledge_graph.add_datagov_relationships(relationships)
            
            self.logger.info(f"Created {len(entity_ids)} entities and {len(relationship_ids)} relationships")
            return entity_ids + relationship_ids
            
        except Exception as e:
            self.logger.error(f"Failed to create relationships: {e}")
            return []
    
    async def _generate_embeddings(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate embeddings for data."""
        # This is a placeholder implementation
        # In a real implementation, you would use a proper embedding model
        embeddings = []
        
        for source, source_data in data.items():
            if isinstance(source_data, dict) and "error" not in source_data:
                # Create a text representation of the data
                text_data = self._data_to_text(source_data)
                
                # Generate embedding (placeholder)
                embedding = {
                    "text": text_data,
                    "source": source,
                    "timestamp": datetime.utcnow().isoformat(),
                    "embedding": [0.1] * 384  # Placeholder embedding vector
                }
                embeddings.append(embedding)
        
        return embeddings
    
    async def _extract_entities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract entities from data for knowledge graph."""
        entities = []
        
        for source, source_data in data.items():
            if isinstance(source_data, dict) and "error" not in source_data:
                # Extract entities based on data structure
                if "countries" in source_data:
                    for country_data in source_data["countries"]:
                        entity = {
                            "id": f"{source}_{country_data.get('code', 'unknown')}",
                            "type": "Country",
                            "properties": country_data,
                            "source": source
                        }
                        entities.append(entity)
        
        return entities
    
    async def _extract_relationships(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract relationships from data for knowledge graph."""
        relationships = []
        
        # This is a placeholder implementation
        # In a real implementation, you would extract meaningful relationships
        
        return relationships
    
    def _data_to_text(self, data: Dict[str, Any]) -> str:
        """Convert data to text representation for embedding generation."""
        # This is a simple text conversion
        # In a real implementation, you would create more sophisticated text representations
        
        if isinstance(data, dict):
            text_parts = []
            for key, value in data.items():
                if isinstance(value, (str, int, float)):
                    text_parts.append(f"{key}: {value}")
                elif isinstance(value, list):
                    text_parts.append(f"{key}: {len(value)} items")
                elif isinstance(value, dict):
                    text_parts.append(f"{key}: {self._data_to_text(value)}")
            
            return " | ".join(text_parts)
        
        return str(data)
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on data ingestion manager."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "components": {}
            }
            
            # Check API connections
            apis = {
                "census": self.census_api,
                "usda": self.usda_api,
                "usitc": self.usitc_api,
                "epi": self.epi_api
            }
            
            for name, api in apis.items():
                try:
                    await api.health_check()
                    health_status["components"][name] = "healthy"
                except Exception as e:
                    health_status["components"][name] = f"unhealthy: {str(e)}"
                    health_status["status"] = "degraded"
            
            # Check vector database
            try:
                await self.vector_db.health_check()
                health_status["components"]["vector_db"] = "healthy"
            except Exception as e:
                health_status["components"]["vector_db"] = f"unhealthy: {str(e)}"
                health_status["status"] = "degraded"
            
            # Check knowledge graph
            try:
                await self.knowledge_graph.health_check()
                health_status["components"]["knowledge_graph"] = "healthy"
            except Exception as e:
                health_status["components"]["knowledge_graph"] = f"unhealthy: {str(e)}"
                health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
