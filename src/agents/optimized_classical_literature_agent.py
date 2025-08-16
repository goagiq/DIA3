#!/usr/bin/env python3
"""
Optimized Classical Literature Processing Agent

This agent provides an enhanced pipeline for processing classical literature content
with optimized performance, advanced features, and comprehensive error handling.

Features:
- Parallel processing for multiple texts
- Advanced text cleaning and normalization
- Intelligent language detection
- Enhanced entity extraction for classical texts
- Optimized knowledge graph generation
- Caching and performance optimization
- Comprehensive metadata extraction
- Cross-references and annotations
- Quality assessment and validation
"""

import asyncio
import re
import json
import pickle
from typing import Any, Optional, List, Dict, Union, Tuple
from urllib.parse import urlparse
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

from loguru import logger
from src.agents.base_agent import StrandsBaseAgent as BaseAgent
from src.config.config import config
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
from src.core.data_ingestion_service import DataIngestionService


class OptimizedClassicalLiteratureAgent(BaseAgent):
    """
    Optimized agent for processing classical literature with enhanced performance and features.
    
    Key Optimizations:
    - Parallel processing capabilities
    - Intelligent caching
    - Advanced text preprocessing
    - Enhanced entity recognition for classical texts
    - Optimized knowledge graph generation
    - Quality assessment and validation
    - Cross-reference detection
    - Annotation support
    """
    
    def __init__(
        self, 
        model_name: Optional[str] = None,
        max_workers: int = 4,
        enable_caching: bool = True,
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
        self.data_ingestion = DataIngestionService()
        
        # Performance settings
        self.max_workers = max_workers
        self.enable_caching = enable_caching
        self.cache = {} if enable_caching else None
        
        # Classical literature specific patterns
        self.classical_patterns = {
            "chapter_markers": [
                r"Chapter\s+\d+",
                r"Book\s+\d+",
                r"Part\s+\d+",
                r"Chapter\s+[IVX]+",
                r"Book\s+[IVX]+",
                r"Part\s+[IVX]+"
            ],
            "character_references": [
                r"Mr\.\s+[A-Z][a-z]+",
                r"Mrs\.\s+[A-Z][a-z]+",
                r"Dr\.\s+[A-Z][a-z]+",
                r"Lord\s+[A-Z][a-z]+",
                r"Lady\s+[A-Z][a-z]+"
            ],
            "classical_entities": [
                r"God",
                r"Lord",
                r"King",
                r"Queen",
                r"Prince",
                r"Princess",
                r"Emperor",
                r"Empress"
            ]
        }
        
        # Set metadata
        self.metadata["model"] = model_name or default_model
        self.metadata["capabilities"] = [
            "optimized_classical_processing", "parallel_processing", "advanced_cleaning",
            "intelligent_caching", "enhanced_entities", "quality_assessment",
            "cross_references", "annotations", "performance_optimization"
        ]
        self.metadata["supported_content_types"] = [
            "classical_literature", "epic_poetry", "philosophical_texts", 
            "historical_documents", "religious_texts", "ancient_manuscripts"
        ]
        self.metadata["supported_languages"] = ["en", "ru", "zh", "ja", "ko", "ar", "la", "grc"]
        self.metadata["performance_features"] = {
            "parallel_processing": True,
            "caching": enable_caching,
            "max_workers": max_workers,
            "optimized_cleaning": True
        }
        
        logger.info(f"Initialized OptimizedClassicalLiteratureAgent with model {self.metadata['model']}")
        logger.info(f"Performance features: {self.metadata['performance_features']}")
    
    def _get_tools(self) -> list:
        """Get list of tools for this agent."""
        return [
            self.process_classical_text,
            self.process_multiple_texts,
            self.enhanced_text_cleaning,
            self.extract_classical_entities,
            self.generate_optimized_knowledge_graph,
            self.assess_text_quality,
            self.detect_cross_references,
            self.add_annotations,
            self.cache_management
        ]
    
    async def process_classical_text(
        self, 
        content: str, 
        title: str = "",
        author: str = "",
        language: str = "auto",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process classical literature text with optimized pipeline.
        
        Args:
            content: Text content or URL
            title: Title of the work
            author: Author of the work
            language: Language code or 'auto' for detection
            options: Additional processing options
            
        Returns:
            Processing results with enhanced metadata
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(content, title, author, language, options)
            if self.enable_caching and cache_key in self.cache:
                logger.info("📋 Using cached result")
                return self.cache[cache_key]
            
            # Detect if content is URL or text
            if self._is_url(content):
                processed_content = await self._process_url_content(content)
            else:
                processed_content = {
                    "text": content,
                    "title": title,
                    "author": author,
                    "source": "direct_input"
                }
            
            # Enhanced text cleaning
            cleaned_text = await self.enhanced_text_cleaning(processed_content["text"])
            
            # Auto-detect language if needed
            if language == "auto":
                language = await self._detect_language(cleaned_text)
            
            # Extract enhanced metadata
            metadata = await self._extract_enhanced_metadata(
                cleaned_text, 
                processed_content["title"], 
                processed_content["author"],
                language
            )
            
            # Quality assessment
            quality_score = await self.assess_text_quality(cleaned_text, metadata)
            
            # Extract classical entities
            entities = await self.extract_classical_entities(cleaned_text, language)
            
            # Generate optimized knowledge graph
            kg_result = await self.generate_optimized_knowledge_graph(
                cleaned_text, entities, metadata
            )
            
            # Detect cross-references
            cross_refs = await self.detect_cross_references(cleaned_text, entities)
            
            # Store in vector database
            vector_id = await self.vector_db.store_content(cleaned_text, metadata)
            
            # Generate comprehensive summary
            summary = await self._generate_comprehensive_summary(
                cleaned_text, metadata, entities, quality_score
            )
            
            # Compile results
            processing_time = asyncio.get_event_loop().time() - start_time
            
            result = {
                "success": True,
                "processing_time": processing_time,
                "content_length": len(cleaned_text),
                "language": language,
                "quality_score": quality_score,
                "metadata": metadata,
                "entities": entities,
                "knowledge_graph": kg_result,
                "cross_references": cross_refs,
                "vector_id": vector_id,
                "summary": summary,
                "cache_key": cache_key
            }
            
            # Cache result
            if self.enable_caching:
                self.cache[cache_key] = result
            
            logger.success(f"✅ Optimized classical text processing completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in optimized classical text processing: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": asyncio.get_event_loop().time() - start_time
            }
    
    async def process_multiple_texts(
        self, 
        texts: List[Dict[str, Any]], 
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Process multiple classical texts with optional parallel processing.
        
        Args:
            texts: List of text dictionaries with content, title, author, language
            parallel: Whether to process texts in parallel
            
        Returns:
            Results for all processed texts
        """
        start_time = asyncio.get_event_loop().time()
        
        if parallel and len(texts) > 1:
            logger.info(f"🔄 Processing {len(texts)} texts in parallel with {self.max_workers} workers")
            results = await self._process_parallel(texts)
        else:
            logger.info(f"🔄 Processing {len(texts)} texts sequentially")
            results = []
            for text in texts:
                result = await self.process_classical_text(**text)
                results.append(result)
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return {
            "success": True,
            "total_texts": len(texts),
            "successful_texts": len([r for r in results if r.get("success", False)]),
            "failed_texts": len([r for r in results if not r.get("success", False)]),
            "total_processing_time": processing_time,
            "average_processing_time": processing_time / len(texts),
            "results": results
        }
    
    async def enhanced_text_cleaning(self, text: str) -> str:
        """
        Enhanced text cleaning optimized for classical literature.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned and normalized text
        """
        try:
            # Basic cleaning
            cleaned = text.strip()
            
            # Remove excessive whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            # Normalize quotes and dashes
            cleaned = re.sub(r'["""]', '"', cleaned)
            cleaned = re.sub(r'[''']', "'", cleaned)
            cleaned = re.sub(r'--+', '—', cleaned)
            
            # Fix common OCR issues
            cleaned = re.sub(r'[|]', 'I', cleaned)  # Common OCR mistake
            cleaned = re.sub(r'[0O]', 'O', cleaned)  # Another common OCR issue
            
            # Preserve paragraph breaks
            cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
            
            # Remove page numbers and headers
            cleaned = re.sub(r'^\d+\s*$', '', cleaned, flags=re.MULTILINE)
            
            # Clean up chapter markers
            for pattern in self.classical_patterns["chapter_markers"]:
                cleaned = re.sub(pattern, lambda m: f"\n\n{m.group(0)}\n", cleaned)
            
            logger.info(f"🧹 Enhanced text cleaning completed: {len(text)} -> {len(cleaned)} characters")
            return cleaned
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced text cleaning: {e}")
            return text
    
    async def extract_classical_entities(self, text: str, language: str) -> List[Dict[str, Any]]:
        """
        Extract entities optimized for classical literature.
        
        Args:
            text: Text content
            language: Language code
            
        Returns:
            List of extracted entities with enhanced metadata
        """
        try:
            # Use existing knowledge graph agent for basic extraction
            entities_result = await self.kg_agent.extract_entities(text, language)
            entities = entities_result.get("content", [{}])[0].get("json", {}).get("entities", [])
            
            # Enhance with classical literature specific patterns
            enhanced_entities = []
            
            for entity in entities:
                enhanced_entity = entity.copy()
                
                # Add classical literature specific metadata
                enhanced_entity["classical_relevance"] = self._assess_classical_relevance(entity)
                enhanced_entity["historical_period"] = self._detect_historical_period(entity, text)
                enhanced_entity["cultural_context"] = self._detect_cultural_context(entity, language)
                
                enhanced_entities.append(enhanced_entity)
            
            # Add entities from classical patterns
            pattern_entities = self._extract_pattern_entities(text)
            enhanced_entities.extend(pattern_entities)
            
            logger.info(f"🏛️ Extracted {len(enhanced_entities)} classical entities")
            return enhanced_entities
            
        except Exception as e:
            logger.error(f"❌ Error extracting classical entities: {e}")
            return []
    
    async def generate_optimized_knowledge_graph(
        self, 
        text: str, 
        entities: List[Dict[str, Any]], 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate optimized knowledge graph for classical literature.
        
        Args:
            text: Text content
            entities: Extracted entities
            metadata: Content metadata
            
        Returns:
            Knowledge graph result with enhanced features
        """
        try:
            # Transform entities for knowledge graph
            transformed_entities = [
                {
                    "name": entity.get("text", ""),
                    "type": entity.get("type", "CONCEPT"),
                    "confidence": entity.get("confidence", 0.0),
                    "classical_relevance": entity.get("classical_relevance", 0.0),
                    "historical_period": entity.get("historical_period", "unknown"),
                    "cultural_context": entity.get("cultural_context", "unknown"),
                    "source": metadata.get("title", "Unknown")
                }
                for entity in entities
            ]
            
            # Extract relationships
            relationships_result = await self.kg_agent.map_relationships(text, entities)
            relationships = relationships_result.get("content", [{}])[0].get("json", {}).get("relationships", [])
            
            transformed_relationships = [
                {
                    "source": rel.get("source", ""),
                    "target": rel.get("target", ""),
                    "relationship_type": rel.get("type", "RELATED_TO"),
                    "confidence": rel.get("confidence", 0.0),
                    "source_type": metadata.get("title", "Unknown")
                }
                for rel in relationships
            ]
            
            # Create knowledge graph
            kg_result = await self.kg_utility.create_knowledge_graph(
                transformed_entities, 
                transformed_relationships
            )
            
            # Save knowledge graph
            kg_path = await self._save_knowledge_graph(kg_result, metadata)
            
            return {
                "success": True,
                "nodes": kg_result.number_of_nodes(),
                "edges": kg_result.number_of_edges(),
                "density": kg_result.number_of_edges() / max(kg_result.number_of_nodes(), 1),
                "file_path": str(kg_path),
                "entities_count": len(transformed_entities),
                "relationships_count": len(transformed_relationships)
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating optimized knowledge graph: {e}")
            return {"success": False, "error": str(e)}
    
    async def assess_text_quality(self, text: str, metadata: Dict[str, Any]) -> float:
        """
        Assess the quality of classical text content.
        
        Args:
            text: Text content
            metadata: Content metadata
            
        Returns:
            Quality score between 0 and 1
        """
        try:
            score = 0.0
            factors = {}
            
            # Length factor
            length_score = min(len(text) / 1000, 1.0)  # Normalize to 1000+ chars
            factors["length"] = length_score
            score += length_score * 0.2
            
            # Readability factor
            readability_score = self._calculate_readability(text)
            factors["readability"] = readability_score
            score += readability_score * 0.3
            
            # Structure factor
            structure_score = self._assess_text_structure(text)
            factors["structure"] = structure_score
            score += structure_score * 0.2
            
            # Entity density factor
            entity_density = self._calculate_entity_density(text)
            factors["entity_density"] = entity_density
            score += entity_density * 0.2
            
            # Language consistency factor
            language_consistency = self._assess_language_consistency(text, metadata.get("language", "en"))
            factors["language_consistency"] = language_consistency
            score += language_consistency * 0.1
            
            logger.info(f"📊 Text quality assessment: {score:.3f} ({factors})")
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"❌ Error assessing text quality: {e}")
            return 0.5
    
    async def detect_cross_references(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect cross-references within classical text.
        
        Args:
            text: Text content
            entities: Extracted entities
            
        Returns:
            List of detected cross-references
        """
        try:
            cross_refs = []
            
            # Detect character references
            character_refs = self._detect_character_references(text, entities)
            cross_refs.extend(character_refs)
            
            # Detect location references
            location_refs = self._detect_location_references(text, entities)
            cross_refs.extend(location_refs)
            
            # Detect thematic references
            thematic_refs = self._detect_thematic_references(text, entities)
            cross_refs.extend(thematic_refs)
            
            logger.info(f"🔗 Detected {len(cross_refs)} cross-references")
            return cross_refs
            
        except Exception as e:
            logger.error(f"❌ Error detecting cross-references: {e}")
            return []
    
    async def add_annotations(self, text: str, annotations: List[Dict[str, Any]]) -> str:
        """
        Add annotations to classical text.
        
        Args:
            text: Text content
            annotations: List of annotations to add
            
        Returns:
            Annotated text
        """
        try:
            annotated_text = text
            
            for annotation in annotations:
                start_pos = annotation.get("start", 0)
                end_pos = annotation.get("end", 0)
                note = annotation.get("note", "")
                
                if start_pos < len(annotated_text) and end_pos <= len(annotated_text):
                    # Insert annotation marker
                    marker = f"[{note}]"
                    annotated_text = (
                        annotated_text[:start_pos] + 
                        marker + 
                        annotated_text[start_pos:end_pos] + 
                        marker + 
                        annotated_text[end_pos:]
                    )
            
            logger.info(f"📝 Added {len(annotations)} annotations to text")
            return annotated_text
            
        except Exception as e:
            logger.error(f"❌ Error adding annotations: {e}")
            return text
    
    async def cache_management(self, action: str = "info") -> Dict[str, Any]:
        """
        Manage the caching system.
        
        Args:
            action: Cache action ('info', 'clear', 'stats')
            
        Returns:
            Cache management result
        """
        try:
            if action == "clear":
                self.cache.clear()
                return {"success": True, "message": "Cache cleared"}
            
            elif action == "stats":
                return {
                    "cache_size": len(self.cache),
                    "cache_enabled": self.enable_caching,
                    "cache_keys": list(self.cache.keys())[:10]  # First 10 keys
                }
            
            else:  # info
                return {
                    "cache_enabled": self.enable_caching,
                    "cache_size": len(self.cache),
                    "max_workers": self.max_workers
                }
                
        except Exception as e:
            logger.error(f"❌ Error in cache management: {e}")
            return {"success": False, "error": str(e)}
    
    # Helper methods
    
    def _generate_cache_key(self, content: str, title: str, author: str, language: str, options: Optional[Dict[str, Any]]) -> str:
        """Generate cache key for content."""
        key_data = f"{content[:100]}{title}{author}{language}{str(options)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_url(self, content: str) -> bool:
        """Check if content is a URL."""
        return content.startswith(('http://', 'https://'))
    
    async def _process_url_content(self, url: str) -> Dict[str, Any]:
        """Process content from URL."""
        webpage_data = await self.web_agent._fetch_webpage(url)
        cleaned_text = self.web_agent._clean_webpage_text(webpage_data["html"])
        
        return {
            "text": cleaned_text,
            "title": webpage_data.get("title", ""),
            "author": "",  # Would need to extract from metadata
            "source": url
        }
    
    async def _detect_language(self, text: str) -> str:
        """Detect language of text."""
        # Use translation service for language detection
        try:
            detected = await self.translation_service.detect_language(text[:1000])
            return detected.get("language", "en")
        except:
            return "en"
    
    async def _extract_enhanced_metadata(self, text: str, title: str, author: str, language: str) -> Dict[str, Any]:
        """Extract enhanced metadata from text."""
        metadata = {
            "title": title,
            "author": author,
            "language": language,
            "content_type": "classical_literature",
            "processing_timestamp": datetime.now().isoformat(),
            "text_length": len(text),
            "estimated_reading_time": len(text) / 200,  # Rough estimate
            "processing_agent": "OptimizedClassicalLiteratureAgent"
        }
        
        # Extract additional metadata
        metadata["chapter_count"] = len(re.findall(r'Chapter\s+\d+', text))
        metadata["paragraph_count"] = len(text.split('\n\n'))
        metadata["sentence_count"] = len(re.split(r'[.!?]+', text))
        
        return metadata
    
    async def _process_parallel(self, texts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process texts in parallel."""
        semaphore = asyncio.Semaphore(self.max_workers)
        
        async def process_with_semaphore(text):
            async with semaphore:
                return await self.process_classical_text(**text)
        
        tasks = [process_with_semaphore(text) for text in texts]
        return await asyncio.gather(*tasks)
    
    def _assess_classical_relevance(self, entity: Dict[str, Any]) -> float:
        """Assess relevance of entity to classical literature."""
        text = entity.get("text", "").lower()
        
        # Classical literature keywords
        classical_keywords = [
            "king", "queen", "prince", "princess", "lord", "lady", "duke", "duchess",
            "war", "peace", "love", "death", "life", "god", "gods", "goddess",
            "ancient", "classical", "philosophy", "wisdom", "knowledge"
        ]
        
        relevance = sum(1 for keyword in classical_keywords if keyword in text)
        return min(relevance / len(classical_keywords), 1.0)
    
    def _detect_historical_period(self, entity: Dict[str, Any], text: str) -> str:
        """Detect historical period of entity."""
        # Simplified historical period detection
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["ancient", "rome", "greece", "egypt"]):
            return "ancient"
        elif any(word in text_lower for word in ["medieval", "middle ages", "crusade"]):
            return "medieval"
        elif any(word in text_lower for word in ["renaissance", "enlightenment"]):
            return "renaissance"
        else:
            return "unknown"
    
    def _detect_cultural_context(self, entity: Dict[str, Any], language: str) -> str:
        """Detect cultural context of entity."""
        # Simplified cultural context detection
        if language in ["zh", "ja", "ko"]:
            return "east_asian"
        elif language in ["ar", "he"]:
            return "middle_eastern"
        elif language in ["ru", "uk", "pl"]:
            return "eastern_european"
        else:
            return "western"
    
    def _extract_pattern_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities using classical patterns."""
        entities = []
        
        # Extract character references
        for pattern in self.classical_patterns["character_references"]:
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append({
                    "text": match.group(0),
                    "type": "PERSON",
                    "confidence": 0.8,
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Extract classical entities
        for pattern in self.classical_patterns["classical_entities"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "text": match.group(0),
                    "type": "TITLE",
                    "confidence": 0.9,
                    "start": match.start(),
                    "end": match.end()
                })
        
        return entities
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score."""
        try:
            sentences = re.split(r'[.!?]+', text)
            words = text.split()
            
            if len(sentences) == 0 or len(words) == 0:
                return 0.5
            
            avg_sentence_length = len(words) / len(sentences)
            
            # Simple readability score (lower is better for classical texts)
            if avg_sentence_length < 10:
                return 0.8
            elif avg_sentence_length < 20:
                return 0.6
            else:
                return 0.4
        except:
            return 0.5
    
    def _assess_text_structure(self, text: str) -> float:
        """Assess text structure quality."""
        paragraphs = text.split('\n\n')
        chapters = len(re.findall(r'Chapter\s+\d+', text))
        
        # Score based on structure indicators
        score = 0.0
        
        if len(paragraphs) > 10:
            score += 0.3
        
        if chapters > 0:
            score += 0.4
        
        if len(text) > 1000:
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_entity_density(self, text: str) -> float:
        """Calculate entity density in text."""
        # Simplified entity density calculation
        words = text.split()
        if len(words) == 0:
            return 0.0
        
        # Count potential entities (capitalized words)
        entities = len(re.findall(r'\b[A-Z][a-z]+\b', text))
        density = entities / len(words)
        
        return min(density * 10, 1.0)  # Normalize
    
    def _assess_language_consistency(self, text: str, language: str) -> float:
        """Assess language consistency."""
        # Simplified language consistency check
        if language == "en":
            # Check for English patterns
            english_patterns = len(re.findall(r'\bthe\b|\band\b|\bor\b', text.lower()))
            return min(english_patterns / 100, 1.0)
        else:
            return 0.8  # Assume consistency for other languages
    
    def _detect_character_references(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect character references in text."""
        character_refs = []
        
        for entity in entities:
            if entity.get("type") == "PERSON":
                # Find all occurrences of this character
                name = entity.get("text", "")
                if name:
                    matches = list(re.finditer(re.escape(name), text))
                    if len(matches) > 1:
                        character_refs.append({
                            "character": name,
                            "occurrences": len(matches),
                            "positions": [m.start() for m in matches]
                        })
        
        return character_refs
    
    def _detect_location_references(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect location references in text."""
        location_refs = []
        
        for entity in entities:
            if entity.get("type") in ["LOCATION", "GPE"]:
                name = entity.get("text", "")
                if name:
                    matches = list(re.finditer(re.escape(name), text))
                    if len(matches) > 1:
                        location_refs.append({
                            "location": name,
                            "occurrences": len(matches),
                            "positions": [m.start() for m in matches]
                        })
        
        return location_refs
    
    def _detect_thematic_references(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect thematic references in text."""
        thematic_refs = []
        
        # Define thematic keywords
        themes = {
            "love": ["love", "romance", "passion", "affection"],
            "war": ["war", "battle", "conflict", "fighting"],
            "death": ["death", "dying", "mortality", "funeral"],
            "power": ["power", "authority", "control", "dominance"],
            "wisdom": ["wisdom", "knowledge", "learning", "understanding"]
        }
        
        for theme, keywords in themes.items():
            theme_occurrences = []
            for keyword in keywords:
                matches = list(re.finditer(rf'\b{keyword}\b', text, re.IGNORECASE))
                theme_occurrences.extend([m.start() for m in matches])
            
            if theme_occurrences:
                thematic_refs.append({
                    "theme": theme,
                    "occurrences": len(theme_occurrences),
                    "positions": theme_occurrences
                })
        
        return thematic_refs
    
    async def _save_knowledge_graph(self, kg_result, metadata: Dict[str, Any]) -> Path:
        """Save knowledge graph to file."""
        from src.config.settings import settings
        
        kg_dir = settings.paths.knowledge_graphs_dir
        kg_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = "".join(c for c in metadata.get("title", "Unknown") if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        
        pkl_filename = f"optimized_classical_kg_{safe_title}_{timestamp}.pkl"
        pkl_file_path = kg_dir / pkl_filename
        
        with open(pkl_file_path, 'wb') as f:
            pickle.dump(kg_result, f)
        
        return pkl_file_path
    
    async def _generate_comprehensive_summary(
        self, 
        text: str, 
        metadata: Dict[str, Any], 
        entities: List[Dict[str, Any]], 
        quality_score: float
    ) -> str:
        """Generate comprehensive summary of processed text."""
        summary_parts = [
            f"Title: {metadata.get('title', 'Unknown')}",
            f"Author: {metadata.get('author', 'Unknown')}",
            f"Language: {metadata.get('language', 'Unknown')}",
            f"Length: {len(text)} characters",
            f"Quality Score: {quality_score:.3f}",
            f"Entities Extracted: {len(entities)}",
            f"Processing Time: {metadata.get('processing_timestamp', 'Unknown')}"
        ]
        
        return "\n".join(summary_parts)
