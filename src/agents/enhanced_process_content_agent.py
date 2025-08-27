#!/usr/bin/env python3
"""
Enhanced Process Content Agent that integrates Open Library download functionality
with unified content processing capabilities, including classical literature support.
"""

import asyncio
import re
from typing import Any, Optional, List, Dict, Union
from urllib.parse import urlparse
from pathlib import Path

from loguru import logger
try:
    from strands import tool, Agent
    STRANDS_AVAILABLE = True
    logger.info("✅ Using real Strands implementation for enhanced process content agent")
except ImportError:
    from src.core.strands_mock import tool, Agent
    STRANDS_AVAILABLE = False
    logger.warning("⚠️ Using mock Strands implementation for enhanced process content agent - real Strands not available")

from src.agents.base_agent import StrandsBaseAgent as BaseAgent
from src.config.config import config
from src.config.language_specific_regex_config import (
    get_all_mcp_detection_patterns,
    get_mcp_processing_keywords,
    detect_language_for_mcp_detection
)
from src.core.models import (
    AnalysisRequest, 
    AnalysisResult, 
    DataType, 
    SentimentResult
)
from src.core.vector_db import VectorDBManager
from src.core.improved_knowledge_graph_utility import ImprovedKnowledgeGraphUtility
from src.agents.knowledge_graph_agent import KnowledgeGraphAgent
from src.agents.web_agent_enhanced import EnhancedWebAgent
from src.core.translation_service import TranslationService


class EnhancedProcessContentAgent(BaseAgent):
    """
    Enhanced agent for processing content with Open Library and classical literature integration.
    
    Supports:
    - Open Library URL processing and download
    - Classical literature processing (War and Peace, Art of War, etc.)
    - Chinese Text Project (ctext.org) integration
    - Unified content processing for all types
    - Vector database storage
    - Knowledge graph generation
    - Multilingual support (Russian, Chinese, English, etc.)
    - Content type auto-detection
    - Classical text optimization
    """
    
    def __init__(
        self, 
        model_name: Optional[str] = None,
        **kwargs
    ):
        # Use config system instead of hardcoded values
        default_model = config.model.default_text_model
        super().__init__(
            model_name=model_name or default_model, 
            **kwargs
        )
        
        # Initialize core services
        self.vector_db = VectorDBManager()
        self.kg_utility = ImprovedKnowledgeGraphUtility()
        self.kg_agent = KnowledgeGraphAgent()
        self.web_agent = EnhancedWebAgent()
        self.translation_service = TranslationService()
        
        # Set metadata
        self.metadata["model"] = model_name or default_model
        self.metadata["capabilities"] = [
            "content_processing", "open_library_download", "classical_literature",
            "vector_storage", "knowledge_graph", "multilingual", "content_detection",
            "ctext_integration", "russian_literature", "chinese_literature"
        ]
        self.metadata["supported_content_types"] = [
            "text", "url", "open_library", "classical_literature", "ctext", 
            "pdf", "audio", "video", "image"
        ]
        self.metadata["supported_languages"] = ["en", "ru", "zh", "ja", "ko", "ar"]
        self.metadata["classical_text_sources"] = [
            "openlibrary.org", "ctext.org", "gutenberg.org", "archive.org"
        ]
        
        logger.info(f"Initialized EnhancedProcessContentAgent with model {self.metadata['model']}")
        logger.info(f"Classical literature support enabled for: {self.metadata['classical_text_sources']}")
    
    def _get_tools(self) -> list:
        """Get list of tools for this agent."""
        return [
            self.process_content,
            self.download_openlibrary_content,
            self.process_classical_literature,
            self.extract_text_from_content,
            self.summarize_content,
            self.translate_content,
            self.convert_content_format,
            self.store_in_vector_db,
            self.create_knowledge_graph,
            self.analyze_sentiment,
            self.detect_content_type,
            self.verify_ingestion
        ]
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the request."""
        return request.data_type in [
            DataType.TEXT, DataType.WEBPAGE, DataType.URL, DataType.CONTENT
        ]
    
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process content analysis request with enhanced capabilities."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Detect content type and route accordingly
            content = str(request.content)
            content_type = self._detect_content_type(content)
            
            # Handle bulk import requests
            if content_type == "bulk_import_request":
                result = await self._process_bulk_import_request(content, request)
            # Handle Open Library URLs specially
            elif self._is_openlibrary_url(content):
                result = await self._process_openlibrary_content(content, request)
            # Handle ctext.org URLs (classical Chinese literature)
            elif self._is_ctext_url(content):
                result = await self._process_ctext_content(content, request)
            # Handle classical literature URLs
            elif self._is_classical_literature_url(content):
                result = await self._process_classical_literature_content(content, request)
            else:
                result = await self._process_standard_content(content, content_type, request)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing content: {e}")
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="neutral",
                    confidence=0.0,
                    metadata={"error": str(e)}
                ),
                processing_time=asyncio.get_event_loop().time() - start_time,
                status="failed",
                metadata={"error": str(e), "agent_id": self.agent_id}
            )
    
    def _detect_content_type(self, content: str) -> str:
        """Detect content type from content string."""
        content_lower = content.lower()
        
        # Check for bulk import requests first
        if self._detect_bulk_import_request(content):
            return "bulk_import_request"
        
        # Check for classical literature sources
        if self._is_classical_literature_url(content):
            return "classical_literature"
        
        # Check for specific library URLs
        if self._is_openlibrary_url(content):
            return "open_library"
        if self._is_ctext_url(content):
            return "ctext"
        
        # Check for other content types
        if content.startswith(('http://', 'https://')):
            return "url"
        if content.endswith('.pdf'):
            return "pdf"
        if content.endswith(('.mp3', '.wav', '.m4a')):
            return "audio"
        if content.endswith(('.mp4', '.avi', '.mov')):
            return "video"
        if content.endswith(('.jpg', '.png', '.gif')):
            return "image"
        
        return "text"
    
    def _is_openlibrary_url(self, content: str) -> bool:
        """Check if content is an Open Library URL."""
        return 'openlibrary.org' in content.lower()
    
    def _is_ctext_url(self, content: str) -> bool:
        """Check if content is a ctext.org URL."""
        return 'ctext.org' in content.lower()
    
    def _is_classical_literature_url(self, content: str) -> bool:
        """Check if content is a classical literature URL."""
        content_lower = content.lower()
        classical_sources = [
            'openlibrary.org', 'ctext.org', 'gutenberg.org', 'archive.org',
            'classics.mit.edu', 'sacred-texts.com', 'ancient.eu'
        ]
        return any(source in content_lower for source in classical_sources)
    
    def _is_supported_library_url(self, content: str) -> bool:
        """Check if content is a supported library URL."""
        return (self._is_openlibrary_url(content) or 
                self._is_ctext_url(content) or 
                self._is_classical_literature_url(content))
    
    def _detect_bulk_import_request(self, content: str) -> bool:
        """Detect if this is a bulk import request with multiple URLs or MCP tool processing request."""
        import re
        
        # Detect language for multilingual pattern matching
        detected_language = detect_language_for_mcp_detection(content)
        logger.debug(f"Detected language for MCP detection: {detected_language}")
        
        # Get language-specific patterns
        bulk_patterns = get_all_mcp_detection_patterns(detected_language)
        processing_keywords = get_mcp_processing_keywords(detected_language)
        
        content_lower = content.lower()
        
        # Check for URL patterns first (most specific) - this is language-agnostic
        url_pattern = r'@(https?://[^\s]+)'
        has_urls = bool(re.search(url_pattern, content))
        
        # Check for any of the bulk patterns using language-specific patterns
        has_bulk_pattern = any(re.search(pattern, content_lower) for pattern in bulk_patterns)
        
        # Additional context-based detection using language-specific keywords
        has_processing_keywords = any(keyword in content_lower for keyword in processing_keywords)
        
        # Return True if we have URLs and processing keywords, or if we have bulk patterns
        result = (has_urls and has_processing_keywords) or has_bulk_pattern
        logger.debug(f"MCP bulk import detection result: {result} (language: {detected_language})")
        return result
        
        # Additional context-based detection
        has_processing_keywords = any(keyword in content_lower for keyword in [
            'process', 'add', 'include', 'store', 'save', 'analyze', 'extract',
            'vector', 'knowledge', 'graph', 'database', 'url', 'content'
        ])
        
        # Return True if we have URLs and processing keywords, or if we have bulk patterns
        return (has_urls and has_processing_keywords) or has_bulk_pattern
    
    def _extract_urls_from_request(self, content: str) -> List[str]:
        """Extract URLs from a bulk import request."""
        # Extract URLs that start with @
        url_pattern = r'@(https?://[^\s]+)'
        urls = re.findall(url_pattern, content)
        return urls
    
    async def _process_bulk_import_request(self, content: str, request: AnalysisRequest) -> AnalysisResult:
        """Process bulk import request with multiple URLs."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Extract URLs from the request
            urls = self._extract_urls_from_request(content)
            
            if not urls:
                raise ValueError("No URLs found in bulk import request")
            
            logger.info(f"Processing bulk import request with {len(urls)} URLs: {urls}")
            
            results = []
            total_entities = 0
            total_relationships = 0
            total_nodes = 0
            total_edges = 0
            
            # Process each URL
            for url in urls:
                try:
                    if self._is_openlibrary_url(url):
                        result = await self._process_openlibrary_content(url, request)
                    elif self._is_ctext_url(url):
                        result = await self._process_ctext_content(url, request)
                    else:
                        # Handle as standard URL
                        result = await self._process_standard_content(url, "url", request)
                    
                    results.append({
                        "url": url,
                        "success": True,
                        "title": result.metadata.get("title", "Unknown"),
                        "vector_id": result.metadata.get("vector_id"),
                        "entities_count": result.metadata.get("entities_count", 0),
                        "relationships_count": result.metadata.get("relationships_count", 0),
                        "knowledge_graph_nodes": result.metadata.get("knowledge_graph_nodes", 0),
                        "knowledge_graph_edges": result.metadata.get("knowledge_graph_edges", 0)
                    })
                    
                    total_entities += result.metadata.get("entities_count", 0)
                    total_relationships += result.metadata.get("relationships_count", 0)
                    total_nodes += result.metadata.get("knowledge_graph_nodes", 0)
                    total_edges += result.metadata.get("knowledge_graph_edges", 0)
                    
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")
                    results.append({
                        "url": url,
                        "success": False,
                        "error": str(e)
                    })
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="positive",
                    confidence=0.8,
                    metadata={"content_type": "bulk_import"}
                ),
                processing_time=processing_time,
                status="completed",
                raw_content=content,
                extracted_text=f"Processed {len(urls)} URLs",
                metadata={
                    "agent_id": self.agent_id,
                    "content_type": "bulk_import",
                    "urls_processed": len(urls),
                    "successful_imports": len([r for r in results if r["success"]]),
                    "failed_imports": len([r for r in results if not r["success"]]),
                    "total_entities": total_entities,
                    "total_relationships": total_relationships,
                    "total_knowledge_graph_nodes": total_nodes,
                    "total_knowledge_graph_edges": total_edges,
                    "results": results
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing bulk import request: {e}")
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="neutral",
                    confidence=0.0,
                    metadata={"error": str(e)}
                ),
                processing_time=asyncio.get_event_loop().time() - start_time,
                status="failed",
                metadata={"error": str(e), "agent_id": self.agent_id}
            )
    
    async def _process_ctext_content(self, url: str, request: AnalysisRequest) -> AnalysisResult:
        """Process ctext.org content with full pipeline."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Download content from ctext.org
            webpage_content = await self._download_ctext_content(url)
            
            if not webpage_content:
                raise ValueError("Failed to download content from ctext.org")
            
            # Extract text content
            content_text = webpage_content.get("text", "")
            title = webpage_content.get("title", "Unknown Text")
            
            # Extract metadata
            metadata = self._extract_metadata_from_content(content_text, title)
            metadata["source_url"] = url
            metadata.update({
                "source": "ctext.org",
                "content_type": "classical_text"
            })
            
            # Store in vector database
            vector_id = await self.vector_db.store_content(content_text, metadata)
            
            # Extract entities and create knowledge graph
            entities_result = await self.kg_agent.extract_entities(content_text, "zh")  # Chinese for classical texts
            entities = entities_result.get("content", [{}])[0].get("json", {}).get("entities", [])
            
            relationships_result = await self.kg_agent.map_relationships(content_text, entities)
            relationships = relationships_result.get("content", [{}])[0].get("json", {}).get("relationships", [])
            
            # Create knowledge graph
            transformed_entities = [
                {
                    "name": entity.get("text", ""),
                    "type": entity.get("type", "CONCEPT"),
                    "confidence": entity.get("confidence", 0.0),
                    "source": title
                }
                for entity in entities
            ]
            
            transformed_relationships = [
                {
                    "source": rel.get("source", ""),
                    "target": rel.get("target", ""),
                    "relationship_type": rel.get("type", "RELATED_TO"),
                    "confidence": rel.get("confidence", 0.0),
                    "source_type": title
                }
                for rel in relationships
            ]
            
            kg_result = await self.kg_utility.create_knowledge_graph(transformed_entities, transformed_relationships)
            
            # Save knowledge graph to Results\knowledge_graphs directory
            from src.config.settings import settings
            import pickle
            from datetime import datetime
            
            # Ensure the knowledge graphs directory exists
            kg_dir = settings.paths.knowledge_graphs_dir
            kg_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            pkl_filename = f"ctext_knowledge_graph_{safe_title}_{timestamp}.pkl"
            pkl_file_path = kg_dir / pkl_filename
            
            # Save the graph as pickle file
            with open(pkl_file_path, 'wb') as f:
                pickle.dump(kg_result, f)
            
            logger.info(f"✅ CText knowledge graph saved to: {pkl_file_path}")
            
            # Generate summary
            summary = self._generate_summary(content_text, title, metadata.get("author"))
            
            # Store summary
            summary_metadata = metadata.copy()
            summary_metadata.update({
                "content_type": "summary",
                "parent_id": vector_id,
                "summary_type": "classical_text_summary"
            })
            summary_id = await self.vector_db.store_content(summary, summary_metadata)
            
            # Create result
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="positive",
                    confidence=0.8,
                    metadata={"content_type": "ctext_classical_text"}
                ),
                processing_time=processing_time,
                status="completed",
                raw_content=url,
                extracted_text=content_text,
                metadata={
                    "agent_id": self.agent_id,
                    "content_type": "ctext_classical_text",
                    "title": title,
                    "vector_id": vector_id,
                    "summary_id": summary_id,
                    "entities_count": len(entities),
                    "relationships_count": len(relationships),
                    "knowledge_graph_nodes": kg_result.number_of_nodes(),
                    "knowledge_graph_edges": kg_result.number_of_edges(),
                    "knowledge_graph_pkl_path": str(pkl_file_path),
                    "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                    "download_success": True,
                    "content_length": len(content_text)
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing ctext.org content: {e}")
            raise
    
    async def _download_ctext_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Download content from ctext.org URL."""
        try:
            # Use the web agent's _fetch_webpage method directly
            webpage_data = await self.web_agent._fetch_webpage(url)
            
            # Process the webpage data
            cleaned_text = self.web_agent._clean_webpage_text(webpage_data["html"])
            
            webpage_content = {
                "url": url,
                "title": webpage_data["title"],
                "text": cleaned_text,
                "html": webpage_data["html"],
                "status_code": webpage_data["status_code"]
            }
            
            logger.info(f"✅ Successfully downloaded ctext.org content: {len(cleaned_text)} characters")
            return webpage_content
            
        except Exception as e:
            logger.error(f"❌ Error downloading ctext.org content: {e}")
            return None
    
    async def _process_openlibrary_content(self, url: str, request: AnalysisRequest) -> AnalysisResult:
        """Process Open Library content with full pipeline."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Download content from Open Library
            webpage_content = await self._download_openlibrary_content(url)
            
            if not webpage_content:
                raise ValueError("Failed to download content from Open Library")
            
            # Extract text content
            content_text = webpage_content.get("text", "")
            title = webpage_content.get("title", "Unknown Book")
            
            # Extract metadata
            metadata = self._extract_metadata_from_content(content_text, title)
            metadata["source_url"] = url
            
            # Store in vector database
            vector_id = await self.vector_db.store_content(content_text, metadata)
            
            # Extract entities and create knowledge graph
            entities_result = await self.kg_agent.extract_entities(content_text, "en")
            entities = entities_result.get("content", [{}])[0].get("json", {}).get("entities", [])
            
            relationships_result = await self.kg_agent.map_relationships(content_text, entities)
            relationships = relationships_result.get("content", [{}])[0].get("json", {}).get("relationships", [])
            
            # Create knowledge graph
            transformed_entities = [
                {
                    "name": entity.get("text", ""),
                    "type": entity.get("type", "CONCEPT"),
                    "confidence": entity.get("confidence", 0.0),
                    "source": title
                }
                for entity in entities
            ]
            
            transformed_relationships = [
                {
                    "source": rel.get("source", ""),
                    "target": rel.get("target", ""),
                    "relationship_type": rel.get("type", "RELATED_TO"),
                    "confidence": rel.get("confidence", 0.0),
                    "source_type": title
                }
                for rel in relationships
            ]
            
            kg_result = await self.kg_utility.create_knowledge_graph(transformed_entities, transformed_relationships)
            
            # Save knowledge graph to Results\knowledge_graphs directory
            from src.config.settings import settings
            import pickle
            from datetime import datetime
            
            # Ensure the knowledge graphs directory exists
            kg_dir = settings.paths.knowledge_graphs_dir
            kg_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            pkl_filename = f"openlibrary_knowledge_graph_{safe_title}_{timestamp}.pkl"
            pkl_file_path = kg_dir / pkl_filename
            
            # Save the graph as pickle file
            with open(pkl_file_path, 'wb') as f:
                pickle.dump(kg_result, f)
            
            logger.info(f"✅ Open Library knowledge graph saved to: {pkl_file_path}")
            
            # Generate summary
            summary = self._generate_summary(content_text, title, metadata.get("author"))
            
            # Store summary
            summary_metadata = metadata.copy()
            summary_metadata.update({
                "content_type": "summary",
                "parent_id": vector_id,
                "summary_type": "book_summary"
            })
            summary_id = await self.vector_db.store_content(summary, summary_metadata)
            
            # Create result
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="positive",
                    confidence=0.8,
                    metadata={"content_type": "open_library_book"}
                ),
                processing_time=processing_time,
                status="completed",
                raw_content=url,
                extracted_text=content_text,
                metadata={
                    "agent_id": self.agent_id,
                    "content_type": "open_library",
                    "title": title,
                    "vector_id": vector_id,
                    "summary_id": summary_id,
                    "entities_count": len(entities),
                    "relationships_count": len(relationships),
                    "knowledge_graph_nodes": kg_result.number_of_nodes(),
                    "knowledge_graph_edges": kg_result.number_of_edges(),
                    "knowledge_graph_pkl_path": str(pkl_file_path),
                    "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                    "download_success": True,
                    "content_length": len(content_text)
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing Open Library content: {e}")
            raise
    
    async def _process_classical_literature_content(self, url: str, request: AnalysisRequest) -> AnalysisResult:
        """Process classical literature content (like War and Peace) with full pipeline."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Download content from classical literature source
            webpage_content = await self._download_classical_literature_content(url)
            
            if not webpage_content:
                raise ValueError("Failed to download content from classical literature source")
            
            # Extract text content
            content_text = webpage_content.get("text", "")
            title = webpage_content.get("title", "Unknown Classical Literature")
            
            # Extract metadata
            metadata = self._extract_metadata_from_content(content_text, title)
            metadata["source_url"] = url
            metadata.update({
                "source": "classical_literature",
                "content_type": "classical_literature"
            })
            
            # Store in vector database
            vector_id = await self.vector_db.store_content(content_text, metadata)
            
            # Extract entities and create knowledge graph
            entities_result = await self.kg_agent.extract_entities(content_text, "en") # English for classical literature
            entities = entities_result.get("content", [{}])[0].get("json", {}).get("entities", [])
            
            relationships_result = await self.kg_agent.map_relationships(content_text, entities)
            relationships = relationships_result.get("content", [{}])[0].get("json", {}).get("relationships", [])
            
            # Create knowledge graph
            transformed_entities = [
                {
                    "name": entity.get("text", ""),
                    "type": entity.get("type", "CONCEPT"),
                    "confidence": entity.get("confidence", 0.0),
                    "source": title
                }
                for entity in entities
            ]
            
            transformed_relationships = [
                {
                    "source": rel.get("source", ""),
                    "target": rel.get("target", ""),
                    "relationship_type": rel.get("type", "RELATED_TO"),
                    "confidence": rel.get("confidence", 0.0),
                    "source_type": title
                }
                for rel in relationships
            ]
            
            kg_result = await self.kg_utility.create_knowledge_graph(transformed_entities, transformed_relationships)
            
            # Save knowledge graph to Results\knowledge_graphs directory
            from src.config.settings import settings
            import pickle
            from datetime import datetime
            
            # Ensure the knowledge graphs directory exists
            kg_dir = settings.paths.knowledge_graphs_dir
            kg_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            pkl_filename = f"classical_literature_knowledge_graph_{safe_title}_{timestamp}.pkl"
            pkl_file_path = kg_dir / pkl_filename
            
            # Save the graph as pickle file
            with open(pkl_file_path, 'wb') as f:
                pickle.dump(kg_result, f)
            
            logger.info(f"✅ Classical Literature knowledge graph saved to: {pkl_file_path}")
            
            # Generate summary
            summary = self._generate_summary(content_text, title, metadata.get("author"))
            
            # Store summary
            summary_metadata = metadata.copy()
            summary_metadata.update({
                "content_type": "summary",
                "parent_id": vector_id,
                "summary_type": "classical_literature_summary"
            })
            summary_id = await self.vector_db.store_content(summary, summary_metadata)
            
            # Create result
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="positive",
                    confidence=0.8,
                    metadata={"content_type": "classical_literature"}
                ),
                processing_time=processing_time,
                status="completed",
                raw_content=url,
                extracted_text=content_text,
                metadata={
                    "agent_id": self.agent_id,
                    "content_type": "classical_literature",
                    "title": title,
                    "vector_id": vector_id,
                    "summary_id": summary_id,
                    "entities_count": len(entities),
                    "relationships_count": len(relationships),
                    "knowledge_graph_nodes": kg_result.number_of_nodes(),
                    "knowledge_graph_edges": kg_result.number_of_edges(),
                    "knowledge_graph_pkl_path": str(pkl_file_path),
                    "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                    "download_success": True,
                    "content_length": len(content_text)
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing classical literature content: {e}")
            raise
    
    async def _download_classical_literature_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Download content from classical literature source URL."""
        try:
            # Use the web agent's _fetch_webpage method directly
            webpage_data = await self.web_agent._fetch_webpage(url)
            
            # Process the webpage data
            cleaned_text = self.web_agent._clean_webpage_text(webpage_data["html"])
            
            webpage_content = {
                "url": url,
                "title": webpage_data["title"],
                "text": cleaned_text,
                "html": webpage_data["html"],
                "status_code": webpage_data["status_code"]
            }
            
            logger.info(f"✅ Successfully downloaded classical literature content: {len(cleaned_text)} characters")
            return webpage_content
            
        except Exception as e:
            logger.error(f"❌ Error downloading classical literature content: {e}")
            return None
    
    async def _process_standard_content(self, content: str, content_type: str, request: AnalysisRequest) -> AnalysisResult:
        """Process standard content types."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Basic text processing
            if content_type == "text":
                # Analyze sentiment
                sentiment_result = await self._analyze_sentiment(content)
                
                # Store in vector database
                metadata = {
                    "content_type": "text",
                    "language": "en",
                    "source": "direct_input"
                }
                vector_id = await self.vector_db.store_content(content, metadata)
                
                processing_time = asyncio.get_event_loop().time() - start_time
                
                return AnalysisResult(
                    request_id=request.id,
                    data_type=request.data_type,
                    sentiment=sentiment_result,
                    processing_time=processing_time,
                    status="completed",
                    raw_content=content,
                    extracted_text=content,
                    metadata={
                        "agent_id": self.agent_id,
                        "content_type": content_type,
                        "vector_id": vector_id
                    }
                )
            
            # For other content types, return basic result
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label="neutral",
                    confidence=0.5,
                    metadata={"content_type": content_type}
                ),
                processing_time=processing_time,
                status="completed",
                raw_content=content,
                extracted_text=content,
                metadata={
                    "agent_id": self.agent_id,
                    "content_type": content_type
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing standard content: {e}")
            raise
    
    async def _download_openlibrary_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Download content from Open Library URL."""
        try:
            # Use the web agent's _fetch_webpage method directly
            webpage_data = await self.web_agent._fetch_webpage(url)
            
            # Process the webpage data
            cleaned_text = self.web_agent._clean_webpage_text(webpage_data["html"])
            
            webpage_content = {
                "url": url,
                "title": webpage_data["title"],
                "text": cleaned_text,
                "html": webpage_data["html"],
                "status_code": webpage_data["status_code"]
            }
            
            logger.info(f"✅ Successfully downloaded Open Library content: {len(cleaned_text)} characters")
            return webpage_content
            
        except Exception as e:
            logger.error(f"❌ Error downloading Open Library content: {e}")
            return None
    
    def _extract_metadata_from_content(self, content: str, title: str) -> Dict[str, Any]:
        """Extract metadata from content text."""
        content_lower = content.lower()
        
        # Try to extract author
        author = "Unknown"
        author_patterns = ["by ", "author:", "written by", "author is"]
        for pattern in author_patterns:
            if pattern in content_lower:
                start_idx = content_lower.find(pattern) + len(pattern)
                end_idx = content.find("\n", start_idx)
                if end_idx == -1:
                    end_idx = start_idx + 100
                author = content[start_idx:end_idx].strip()
                break
        
        # Try to extract publication year
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, content)
        publication_year = years[0] if years else "Unknown"
        
        # Determine genre
        genre_keywords = {
            "fiction": ["novel", "story", "tale", "fiction"],
            "non-fiction": ["history", "biography", "memoir", "essay"],
            "poetry": ["poem", "poetry", "verse"],
            "drama": ["play", "drama", "theater", "theatre"],
            "science": ["science", "physics", "chemistry", "biology"],
            "philosophy": ["philosophy", "philosophical", "ethics"],
            "religion": ["religion", "religious", "spiritual", "theology"]
        }
        
        detected_genre = "Literature"
        for genre, keywords in genre_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_genre = genre.title()
                break
        
        # Extract subjects
        subjects = []
        subject_keywords = [
            "history", "war", "peace", "love", "family", "politics", 
            "society", "culture", "art", "music", "science", "philosophy",
            "religion", "nature", "travel", "adventure", "mystery"
        ]
        
        for subject in subject_keywords:
            if subject in content_lower:
                subjects.append(subject.title())
        
        return {
            "title": title,
            "author": author,
            "publication_year": publication_year,
            "genre": detected_genre,
            "category": "Classic Literature" if "classic" in content_lower else detected_genre,
            "subjects": subjects[:10],
            "source": "Open Library",
            "source_url": "",  # Will be set by calling method
            "content_type": "book_description",
            "language": "en"
        }
    
    def _generate_summary(self, content: str, title: str, author: Optional[str] = None) -> str:
        """Generate a summary of the content."""
        content_lower = content.lower()
        
        # Extract key themes
        themes = []
        theme_keywords = {
            "war": ["war", "battle", "conflict", "military"],
            "love": ["love", "romance", "relationship", "marriage"],
            "family": ["family", "parent", "child", "sibling"],
            "society": ["society", "social", "class", "aristocracy"],
            "philosophy": ["philosophy", "meaning", "purpose", "existence"],
            "history": ["history", "historical", "past", "era"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                themes.append(theme)
        
        # Create summary
        author_text = f" by {author}" if author else ""
        themes_text = ", ".join(themes[:3]) if themes else "various themes"
        
        summary = f"{title}{author_text} is a literary work that explores {themes_text}. "
        summary += f"The book contains {len(content.split())} words and covers topics related to {', '.join(themes[:5]) if themes else 'literature and human experience'}."
        
        return summary
    
    async def _analyze_sentiment(self, content: str) -> SentimentResult:
        """Analyze sentiment of content."""
        try:
            # Simple rule-based sentiment analysis
            positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "like", "happy"]
            negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible", "worst", "sad"]
            
            content_lower = content.lower()
            positive_count = sum(1 for word in positive_words if word in content_lower)
            negative_count = sum(1 for word in negative_words if word in content_lower)
            
            if positive_count > negative_count:
                label = "positive"
                confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
            elif negative_count > positive_count:
                label = "negative"
                confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
            else:
                label = "neutral"
                confidence = 0.5
            
            return SentimentResult(
                label=label,
                confidence=confidence,
                metadata={"positive_count": positive_count, "negative_count": negative_count}
            )
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return SentimentResult(
                label="neutral",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    # Tool methods for Strands integration
    @tool
    async def process_content(
        self, 
        content: str,
        content_type: str = "auto",
        language: str = "en",
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process any type of content with unified interface."""
        try:
            # Auto-detect content type if not specified
            if content_type == "auto":
                content_type = self._detect_content_type(content)
            
            # Check for bulk import requests
            if content_type == "bulk_import_request":
                logger.info("Detected bulk import request, processing multiple URLs...")
                urls = self._extract_urls_from_request(content)
                logger.info(f"Found {len(urls)} URLs to process: {urls}")
            
            # Create analysis request
            request = AnalysisRequest(
                id=f"process_{self.agent_id}",
                content=content,
                data_type=DataType.TEXT,
                language=language
            )
            
            # Process content
            result = await self.process(request)
            
            # Enhanced response for bulk import requests
            if content_type == "bulk_import_request":
                return {
                    "success": True,
                    "content_type": content_type,
                    "bulk_import": True,
                    "urls_processed": result.metadata.get("urls_processed", 0),
                    "successful_imports": result.metadata.get("successful_imports", 0),
                    "failed_imports": result.metadata.get("failed_imports", 0),
                    "total_entities": result.metadata.get("total_entities", 0),
                    "total_relationships": result.metadata.get("total_relationships", 0),
                    "total_knowledge_graph_nodes": result.metadata.get("total_knowledge_graph_nodes", 0),
                    "total_knowledge_graph_edges": result.metadata.get("total_knowledge_graph_edges", 0),
                    "results": result.metadata.get("results", []),
                    "result": {
                        "sentiment": result.sentiment.label,
                        "confidence": result.sentiment.confidence,
                        "processing_time": result.processing_time,
                        "metadata": result.metadata
                    }
                }
            
            return {
                "success": True,
                "content_type": content_type,
                "result": {
                    "sentiment": result.sentiment.label,
                    "confidence": result.sentiment.confidence,
                    "processing_time": result.processing_time,
                    "metadata": result.metadata
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing content: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def download_openlibrary_content(self, url: str) -> Dict[str, Any]:
        """Download and process content from Open Library URL."""
        try:
            webpage_content = await self._download_openlibrary_content(url)
            
            if not webpage_content:
                return {"success": False, "error": "Failed to download content"}
            
            # Extract metadata
            metadata = self._extract_metadata_from_content(
                webpage_content.get("text", ""),
                webpage_content.get("title", "Unknown")
            )
            
            # Store in vector database
            vector_id = await self.vector_db.store_content(
                webpage_content.get("text", ""), 
                metadata
            )
            
            return {
                "success": True,
                "title": webpage_content.get("title"),
                "content_length": len(webpage_content.get("text", "")),
                "vector_id": vector_id,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error downloading Open Library content: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def extract_text_from_content(
        self,
        content: str,
        content_type: str = "auto",
        language: str = "en"
    ) -> Dict[str, Any]:
        """Extract text from any content type."""
        try:
            if content_type == "auto":
                content_type = self._detect_content_type(content)
            
            if self._is_openlibrary_url(content):
                webpage_content = await self._download_openlibrary_content(content)
                if webpage_content:
                    return {
                        "success": True,
                        "text": webpage_content.get("text", ""),
                        "title": webpage_content.get("title", ""),
                        "language": language
                    }
            
            # For other content types, return as-is
            return {
                "success": True,
                "text": content,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def summarize_content(
        self,
        content: str,
        summary_length: str = "medium"
    ) -> Dict[str, Any]:
        """Generate summary of content."""
        try:
            if self._is_openlibrary_url(content):
                webpage_content = await self._download_openlibrary_content(content)
                if webpage_content:
                    content_text = webpage_content.get("text", "")
                    title = webpage_content.get("title", "Unknown")
                else:
                    return {"success": False, "error": "Failed to download content"}
            else:
                content_text = content
                title = "Content"
            
            summary = self._generate_summary(content_text, title)
            
            return {
                "success": True,
                "summary": summary,
                "title": title
            }
            
        except Exception as e:
            logger.error(f"Error summarizing content: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def translate_content(
        self,
        content: str,
        target_language: str,
        source_language: str = "auto"
    ) -> Dict[str, Any]:
        """Translate content to target language."""
        try:
            # Extract text first
            if self._is_openlibrary_url(content):
                webpage_content = await self._download_openlibrary_content(content)
                if webpage_content:
                    content_text = webpage_content.get("text", "")
                else:
                    return {"success": False, "error": "Failed to download content"}
            else:
                content_text = content
            
            # Translate using translation service
            translated_text = await self.translation_service.translate(
                content_text, target_language, source_language
            )
            
            return {
                "success": True,
                "translated_text": translated_text,
                "target_language": target_language,
                "source_language": source_language
            }
            
        except Exception as e:
            logger.error(f"Error translating content: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def convert_content_format(
        self,
        content: str,
        source_format: str,
        target_format: str
    ) -> Dict[str, Any]:
        """Convert content between different formats."""
        try:
            # For now, return the content as-is
            # This can be extended with actual format conversion logic
            return {
                "success": True,
                "converted_content": content,
                "source_format": source_format,
                "target_format": target_format
            }
            
        except Exception as e:
            logger.error(f"Error converting content format: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def process_classical_literature(
        self,
        url: str,
        language: str = "auto",
        options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process classical literature from URL with full pipeline optimization."""
        try:
            logger.info(f"📚 Processing classical literature from: {url}")
            
            # Validate URL
            if not self._is_classical_literature_url(url):
                return {
                    "success": False, 
                    "error": f"URL is not a recognized classical literature source: {url}"
                }
            
            # Create analysis request
            request = AnalysisRequest(
                id=f"classical_lit_{hash(url) % 10000}",
                content=url,
                data_type=DataType.URL,
                language=language
            )
            
            # Process the classical literature content
            result = await self._process_classical_literature_content(url, request)
            
            if result.status == "completed":
                return {
                    "success": True,
                    "title": result.metadata.get("title", "Unknown"),
                    "author": result.metadata.get("author", "Unknown"),
                    "content_length": result.metadata.get("content_length", 0),
                    "vector_id": result.metadata.get("vector_id"),
                    "summary_id": result.metadata.get("summary_id"),
                    "entities_count": result.metadata.get("entities_count", 0),
                    "relationships_count": result.metadata.get("relationships_count", 0),
                    "knowledge_graph_nodes": result.metadata.get("knowledge_graph_nodes", 0),
                    "knowledge_graph_edges": result.metadata.get("knowledge_graph_edges", 0),
                    "knowledge_graph_pkl_path": result.metadata.get("knowledge_graph_pkl_path"),
                    "summary": result.metadata.get("summary", ""),
                    "processing_time": result.processing_time,
                    "content_type": "classical_literature",
                    "source_url": url
                }
            else:
                return {
                    "success": False,
                    "error": f"Processing failed with status: {result.status}",
                    "metadata": result.metadata
                }
                
        except Exception as e:
            logger.error(f"Error processing classical literature: {e}")
            return {"success": False, "error": str(e)}

    @tool
    async def store_in_vector_db(
        self,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Store content in vector database."""
        try:
            if metadata is None:
                metadata = {"content_type": "text", "source": "direct_input"}
            
            vector_id = await self.vector_db.store_content(content, metadata)
            
            return {
                "success": True,
                "vector_id": vector_id,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error storing in vector database: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def create_knowledge_graph(
        self,
        content: str,
        title: str = "Content"
    ) -> Dict[str, Any]:
        """Create knowledge graph from content."""
        try:
            # Extract entities
            entities_result = await self.kg_agent.extract_entities(content, "en")
            entities = entities_result.get("content", [{}])[0].get("json", {}).get("entities", [])
            
            # Extract relationships
            relationships_result = await self.kg_agent.map_relationships(content, entities)
            relationships = relationships_result.get("content", [{}])[0].get("json", {}).get("relationships", [])
            
            # Create knowledge graph
            transformed_entities = [
                {
                    "name": entity.get("text", ""),
                    "type": entity.get("type", "CONCEPT"),
                    "confidence": entity.get("confidence", 0.0),
                    "source": title
                }
                for entity in entities
            ]
            
            transformed_relationships = [
                {
                    "source": rel.get("source", ""),
                    "target": rel.get("target", ""),
                    "relationship_type": rel.get("type", "RELATED_TO"),
                    "confidence": rel.get("confidence", 0.0),
                    "source_type": title
                }
                for rel in relationships
            ]
            
            kg_result = await self.kg_utility.create_knowledge_graph(transformed_entities, transformed_relationships)
            
            # Save knowledge graph to Results\knowledge_graphs directory
            from src.config.settings import settings
            import pickle
            from datetime import datetime
            
            # Ensure the knowledge graphs directory exists
            kg_dir = settings.paths.knowledge_graphs_dir
            kg_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
            pkl_filename = f"knowledge_graph_{safe_title}_{timestamp}.pkl"
            pkl_file_path = kg_dir / pkl_filename
            
            # Save the graph as pickle file
            with open(pkl_file_path, 'wb') as f:
                pickle.dump(kg_result, f)
            
            logger.info(f"✅ Knowledge graph saved to: {pkl_file_path}")
            
            return {
                "success": True,
                "nodes": kg_result.number_of_nodes(),
                "edges": kg_result.number_of_edges(),
                "entities_count": len(entities),
                "relationships_count": len(relationships),
                "pkl_file_path": str(pkl_file_path),
                "storage_location": "Results/knowledge_graphs"
            }
            
        except Exception as e:
            logger.error(f"Error creating knowledge graph: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def analyze_sentiment(
        self,
        content: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """Analyze sentiment of content."""
        try:
            sentiment_result = await self._analyze_sentiment(content)
            
            return {
                "success": True,
                "sentiment": sentiment_result.label,
                "confidence": sentiment_result.confidence,
                "metadata": sentiment_result.metadata
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"success": False, "error": str(e)}
    
    @tool
    async def detect_content_type(self, content: str) -> Dict[str, Any]:
        """Detect the type of content."""
        try:
            content_type = self._detect_content_type(content)
            is_openlibrary = self._is_openlibrary_url(content)
            
            return {
                "success": True,
                "content_type": content_type,
                "is_openlibrary": is_openlibrary
            }
            
        except Exception as e:
            logger.error(f"Error detecting content type: {e}")
            return {"success": False, "error": str(e)}

    @tool
    async def verify_ingestion(
        self,
        search_queries: List[str] = None,
        test_knowledge_graph: bool = True,
        test_semantic_search: bool = True
    ) -> Dict[str, Any]:
        """Verify that ingested content is properly stored and searchable."""
        try:
            logger.info("🔍 Starting ingestion verification...")
            
            # Default search queries if none provided
            if search_queries is None:
                search_queries = [
                    "Sun Tzu Art of War",
                    "Leo Tolstoy War and Peace", 
                    "military strategy",
                    "Napoleonic Wars",
                    "Russian aristocracy 19th century",
                    "The Art of War principles"
                ]
            
            verification_results = {
                "success": True,
                "vector_database": {},
                "knowledge_graph": {},
                "semantic_search": {},
                "knowledge_graph_search": {},
                "summary": {}
            }
            
            # Test vector database functionality
            try:
                vector_stats = await self.vector_db.get_database_stats()
                verification_results["vector_database"] = {
                    "status": "success",
                    "stats": vector_stats
                }
                logger.info("✅ Vector database verification successful")
            except Exception as e:
                verification_results["vector_database"] = {
                    "status": "error",
                    "error": str(e)
                }
                logger.warning(f"❌ Vector database verification failed: {e}")
            
            # Test semantic search
            if test_semantic_search:
                semantic_results = {}
                for query in search_queries:
                    try:
                        search_result = await self.vector_db.query(
                            collection_name="semantic_search",
                            query_text=query,
                            n_results=5
                        )
                        semantic_results[query] = {
                            "status": "success",
                            "results_count": len(search_result),
                            "has_results": len(search_result) > 0
                        }
                    except Exception as e:
                        semantic_results[query] = {
                            "status": "error",
                            "error": str(e)
                        }
                
                verification_results["semantic_search"] = semantic_results
                logger.info("✅ Semantic search verification completed")
            
            # Test knowledge graph search
            if test_knowledge_graph:
                kg_results = {}
                kg_queries = [
                    "Sun Tzu military strategy",
                    "Leo Tolstoy War and Peace characters",
                    "Napoleonic Wars Russia",
                    "The Art of War principles",
                    "Russian aristocracy 19th century"
                ]
                
                for query in kg_queries:
                    try:
                        kg_search_result = await self.vector_db.query(
                            collection_name="knowledge_graph",
                            query_text=query,
                            n_results=5
                        )
                        kg_results[query] = {
                            "status": "success",
                            "results_count": len(kg_search_result),
                            "has_results": len(kg_search_result) > 0
                        }
                    except Exception as e:
                        kg_results[query] = {
                            "status": "error",
                            "error": str(e)
                        }
                
                verification_results["knowledge_graph_search"] = kg_results
                logger.info("✅ Knowledge graph search verification completed")
            
            # Generate summary
            total_queries = len(search_queries)
            successful_semantic = sum(1 for r in verification_results["semantic_search"].values() 
                                    if r.get("status") == "success" and r.get("has_results", False))
            successful_kg = sum(1 for r in verification_results["knowledge_graph_search"].values() 
                              if r.get("status") == "success" and r.get("has_results", False))
            
            verification_results["summary"] = {
                "total_queries_tested": total_queries,
                "semantic_search_success_rate": f"{successful_semantic}/{total_queries}",
                "knowledge_graph_success_rate": f"{successful_kg}/{len(kg_queries) if test_knowledge_graph else 0}",
                "vector_database_status": verification_results["vector_database"].get("status", "unknown"),
                "overall_status": "success" if verification_results["vector_database"].get("status") == "success" else "partial"
            }
            
            logger.info("🎉 Ingestion verification completed successfully")
            return verification_results
            
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "summary": {"overall_status": "failed"}
            }
