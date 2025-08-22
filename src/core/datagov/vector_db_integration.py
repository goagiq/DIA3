"""
Enhanced Vector Database Integration for Data.gov API
Phase 2 Implementation - Advanced Embedding Storage & Retrieval
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import json
import hashlib

from src.core.vector_db import VectorDBManager
from src.config.datagov_config import DataGovConfig

logger = logging.getLogger(__name__)


class DataGovVectorDBIntegration:
    """
    Enhanced vector database integration for Data.gov data.
    Provides advanced embedding storage, retrieval, and similarity search capabilities.
    """
    
    def __init__(self):
        self.config = DataGovConfig()
        self.vector_db = VectorDBManager()
        self.logger = logging.getLogger(__name__)
        
        # Collection names for different data types
        self.collections = {
            'trade_data': 'datagov_trade_embeddings',
            'macroeconomic_data': 'datagov_economic_embeddings',
            'environmental_data': 'datagov_environmental_embeddings',
            'combined_data': 'datagov_combined_embeddings'
        }
        
        # Initialize collections
        self._initialize_collections()
    
    def _initialize_collections(self):
        """Initialize vector database collections for Data.gov data."""
        try:
            for collection_name in self.collections.values():
                self.vector_db.client.get_or_create_collection(
                    name=collection_name,
                    metadata={
                        "description": f"Data.gov {collection_name} embeddings",
                        "created_at": datetime.utcnow().isoformat(),
                        "version": "2.0"
                    }
                )
            self.logger.info("Data.gov vector database collections initialized")
        except Exception as e:
            self.logger.error(f"Error initializing vector database collections: {e}")
    
    async def store_trade_embeddings(self, data: Dict[str, Any], embeddings: List[float]) -> bool:
        """
        Store trade data embeddings in vector database.
        
        Args:
            data: Processed trade data
            embeddings: Generated embeddings
            
        Returns:
            bool: Success status
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['trade_data'])
            
            # Create document ID
            doc_id = self._generate_document_id(data, 'trade')
            
            # Prepare metadata
            metadata = {
                "data_type": "trade_data",
                "countries": data.get('summary', {}).get('countries', []),
                "date_range": data.get('summary', {}).get('date_range', {}),
                "record_count": data.get('summary', {}).get('total_records', 0),
                "total_trade_value": data.get('summary', {}).get('total_trade_value', 0),
                "processing_timestamp": datetime.utcnow().isoformat(),
                "version": "2.0"
            }
            
            # Store embeddings
            collection.add(
                embeddings=[embeddings],
                documents=[json.dumps(data)],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            self.logger.info(f"Stored trade embeddings for document {doc_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing trade embeddings: {e}")
            return False
    
    async def store_macroeconomic_embeddings(self, data: Dict[str, Any], embeddings: List[float]) -> bool:
        """
        Store macroeconomic data embeddings in vector database.
        
        Args:
            data: Processed macroeconomic data
            embeddings: Generated embeddings
            
        Returns:
            bool: Success status
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['macroeconomic_data'])
            
            # Create document ID
            doc_id = self._generate_document_id(data, 'economic')
            
            # Prepare metadata
            metadata = {
                "data_type": "macroeconomic_data",
                "countries": data.get('summary', {}).get('countries', []),
                "date_range": data.get('summary', {}).get('date_range', {}),
                "record_count": data.get('summary', {}).get('total_records', 0),
                "total_gdp": data.get('summary', {}).get('total_gdp', 0),
                "total_population": data.get('summary', {}).get('total_population', 0),
                "processing_timestamp": datetime.utcnow().isoformat(),
                "version": "2.0"
            }
            
            # Store embeddings
            collection.add(
                embeddings=[embeddings],
                documents=[json.dumps(data)],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            self.logger.info(f"Stored macroeconomic embeddings for document {doc_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing macroeconomic embeddings: {e}")
            return False
    
    async def store_environmental_embeddings(self, data: Dict[str, Any], embeddings: List[float]) -> bool:
        """
        Store environmental data embeddings in vector database.
        
        Args:
            data: Processed environmental data
            embeddings: Generated embeddings
            
        Returns:
            bool: Success status
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['environmental_data'])
            
            # Create document ID
            doc_id = self._generate_document_id(data, 'environmental')
            
            # Prepare metadata
            metadata = {
                "data_type": "environmental_data",
                "countries": data.get('summary', {}).get('countries', []),
                "date_range": data.get('summary', {}).get('date_range', {}),
                "record_count": data.get('summary', {}).get('total_records', 0),
                "avg_epi_score": data.get('summary', {}).get('avg_epi_score', 0),
                "processing_timestamp": datetime.utcnow().isoformat(),
                "version": "2.0"
            }
            
            # Store embeddings
            collection.add(
                embeddings=[embeddings],
                documents=[json.dumps(data)],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            self.logger.info(f"Stored environmental embeddings for document {doc_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing environmental embeddings: {e}")
            return False
    
    async def store_combined_embeddings(self, data: Dict[str, Any], embeddings: List[float]) -> bool:
        """
        Store combined data embeddings in vector database.
        
        Args:
            data: Combined processed data
            embeddings: Generated embeddings
            
        Returns:
            bool: Success status
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['combined_data'])
            
            # Create document ID
            doc_id = self._generate_document_id(data, 'combined')
            
            # Prepare metadata
            metadata = {
                "data_type": "combined_data",
                "data_types": list(data.keys()),
                "countries": self._extract_countries_from_combined_data(data),
                "processing_timestamp": datetime.utcnow().isoformat(),
                "version": "2.0"
            }
            
            # Store embeddings
            collection.add(
                embeddings=[embeddings],
                documents=[json.dumps(data)],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            self.logger.info(f"Stored combined embeddings for document {doc_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error storing combined embeddings: {e}")
            return False
    
    async def search_similar_trade_data(self, query_embedding: List[float], 
                                      countries: Optional[List[str]] = None,
                                      limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar trade data using embeddings.
        
        Args:
            query_embedding: Query embedding
            countries: Filter by countries
            limit: Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: Similar trade data
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['trade_data'])
            
            # Prepare where clause for filtering
            where_clause = {}
            if countries:
                where_clause["countries"] = {"$in": countries}
            
            # Search for similar embeddings
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause if where_clause else None
            )
            
            # Process results
            processed_results = []
            for i, doc_id in enumerate(results['ids'][0]):
                processed_results.append({
                    'id': doc_id,
                    'data': json.loads(results['documents'][0][i]),
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Error searching similar trade data: {e}")
            return []
    
    async def search_similar_economic_data(self, query_embedding: List[float],
                                         countries: Optional[List[str]] = None,
                                         limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar economic data using embeddings.
        
        Args:
            query_embedding: Query embedding
            countries: Filter by countries
            limit: Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: Similar economic data
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['macroeconomic_data'])
            
            # Prepare where clause for filtering
            where_clause = {}
            if countries:
                where_clause["countries"] = {"$in": countries}
            
            # Search for similar embeddings
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause if where_clause else None
            )
            
            # Process results
            processed_results = []
            for i, doc_id in enumerate(results['ids'][0]):
                processed_results.append({
                    'id': doc_id,
                    'data': json.loads(results['documents'][0][i]),
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Error searching similar economic data: {e}")
            return []
    
    async def search_similar_environmental_data(self, query_embedding: List[float],
                                              countries: Optional[List[str]] = None,
                                              limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar environmental data using embeddings.
        
        Args:
            query_embedding: Query embedding
            countries: Filter by countries
            limit: Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: Similar environmental data
        """
        try:
            collection = self.vector_db.client.get_collection(self.collections['environmental_data'])
            
            # Prepare where clause for filtering
            where_clause = {}
            if countries:
                where_clause["countries"] = {"$in": countries}
            
            # Search for similar embeddings
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause if where_clause else None
            )
            
            # Process results
            processed_results = []
            for i, doc_id in enumerate(results['ids'][0]):
                processed_results.append({
                    'id': doc_id,
                    'data': json.loads(results['documents'][0][i]),
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Error searching similar environmental data: {e}")
            return []
    
    async def search_across_all_data_types(self, query_embedding: List[float],
                                         data_types: Optional[List[str]] = None,
                                         countries: Optional[List[str]] = None,
                                         limit: int = 20) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across all data types using embeddings.
        
        Args:
            query_embedding: Query embedding
            data_types: Filter by data types
            countries: Filter by countries
            limit: Maximum number of results per data type
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Results organized by data type
        """
        try:
            results = {}
            
            # Define which collections to search
            search_collections = {}
            if data_types:
                for data_type in data_types:
                    if data_type == 'trade_data':
                        search_collections['trade_data'] = self.collections['trade_data']
                    elif data_type == 'macroeconomic_data':
                        search_collections['macroeconomic_data'] = self.collections['macroeconomic_data']
                    elif data_type == 'environmental_data':
                        search_collections['environmental_data'] = self.collections['environmental_data']
            else:
                search_collections = {
                    'trade_data': self.collections['trade_data'],
                    'macroeconomic_data': self.collections['macroeconomic_data'],
                    'environmental_data': self.collections['environmental_data']
                }
            
            # Search each collection
            for data_type, collection_name in search_collections.items():
                try:
                    collection = self.vector_db.client.get_collection(collection_name)
                    
                    # Prepare where clause for filtering
                    where_clause = {}
                    if countries:
                        where_clause["countries"] = {"$in": countries}
                    
                    # Search for similar embeddings
                    search_results = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=limit,
                        where=where_clause if where_clause else None
                    )
                    
                    # Process results
                    processed_results = []
                    for i, doc_id in enumerate(search_results['ids'][0]):
                        processed_results.append({
                            'id': doc_id,
                            'data': json.loads(search_results['documents'][0][i]),
                            'metadata': search_results['metadatas'][0][i],
                            'distance': search_results['distances'][0][i] if 'distances' in search_results else None
                        })
                    
                    results[data_type] = processed_results
                    
                except Exception as e:
                    self.logger.error(f"Error searching {data_type}: {e}")
                    results[data_type] = []
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching across all data types: {e}")
            return {}
    
    async def get_data_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored Data.gov data.
        
        Returns:
            Dict[str, Any]: Statistics about stored data
        """
        try:
            stats = {
                'total_collections': len(self.collections),
                'collections': {},
                'total_documents': 0,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            for data_type, collection_name in self.collections.items():
                try:
                    collection = self.vector_db.client.get_collection(collection_name)
                    count = collection.count()
                    
                    stats['collections'][data_type] = {
                        'name': collection_name,
                        'document_count': count,
                        'metadata': collection.metadata
                    }
                    
                    stats['total_documents'] += count
                    
                except Exception as e:
                    self.logger.error(f"Error getting statistics for {data_type}: {e}")
                    stats['collections'][data_type] = {
                        'name': collection_name,
                        'document_count': 0,
                        'error': str(e)
                    }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting data statistics: {e}")
            return {'error': str(e)}
    
    async def cleanup_old_data(self, days_old: int = 30) -> Dict[str, int]:
        """
        Clean up old data from vector database.
        
        Args:
            days_old: Remove data older than this many days
            
        Returns:
            Dict[str, int]: Number of documents removed from each collection
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            cleanup_results = {}
            
            for data_type, collection_name in self.collections.items():
                try:
                    collection = self.vector_db.client.get_collection(collection_name)
                    
                    # Get all documents with their metadata
                    all_docs = collection.get()
                    
                    # Find documents to delete
                    docs_to_delete = []
                    for i, metadata in enumerate(all_docs['metadatas']):
                        if 'processing_timestamp' in metadata:
                            try:
                                doc_timestamp = datetime.fromisoformat(metadata['processing_timestamp'])
                                if doc_timestamp < cutoff_date:
                                    docs_to_delete.append(all_docs['ids'][i])
                            except:
                                # If timestamp parsing fails, keep the document
                                pass
                    
                    # Delete old documents
                    if docs_to_delete:
                        collection.delete(ids=docs_to_delete)
                        cleanup_results[data_type] = len(docs_to_delete)
                        self.logger.info(f"Cleaned up {len(docs_to_delete)} old documents from {data_type}")
                    else:
                        cleanup_results[data_type] = 0
                    
                except Exception as e:
                    self.logger.error(f"Error cleaning up {data_type}: {e}")
                    cleanup_results[data_type] = 0
            
            return cleanup_results
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            return {'error': str(e)}
    
    def _generate_document_id(self, data: Dict[str, Any], data_type: str) -> str:
        """Generate unique document ID for vector database storage."""
        # Create a hash based on data content and timestamp
        content_str = json.dumps(data, sort_keys=True)
        timestamp = datetime.utcnow().isoformat()
        
        hash_input = f"{data_type}_{content_str}_{timestamp}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _extract_countries_from_combined_data(self, data: Dict[str, Any]) -> List[str]:
        """Extract unique countries from combined data."""
        countries = set()
        
        for data_type, data_content in data.items():
            if isinstance(data_content, dict) and 'summary' in data_content:
                countries_list = data_content['summary'].get('countries', [])
                countries.update(countries_list)
        
        return list(countries)
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on vector database integration."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "collections": {},
                "total_documents": 0
            }
            
            for data_type, collection_name in self.collections.items():
                try:
                    collection = self.vector_db.client.get_collection(collection_name)
                    count = collection.count()
                    
                    health_status["collections"][data_type] = {
                        "status": "healthy",
                        "document_count": count
                    }
                    
                    health_status["total_documents"] += count
                    
                except Exception as e:
                    health_status["collections"][data_type] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
                    health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
