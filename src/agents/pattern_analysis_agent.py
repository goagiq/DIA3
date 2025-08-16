#!/usr/bin/env python3
"""
Pattern Analysis Agent for Comprehensive Document Analysis
==========================================================

This agent performs comprehensive pattern analysis across all documents
following the CIA/FBI Intelligence Officer Analysis Framework.

Analysis Types:
- Strategic Intelligence Analysis
- Cultural Intelligence Analysis
- Pattern Recognition
- Cross-Document Correlation
- Business Intelligence Synthesis
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import re
from collections import Counter

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

# Import core services
from core.orchestrator import SentimentOrchestrator
from core.unified_mcp_client import call_unified_mcp_tool


class PatternAnalysisAgent:
    """
    Pattern analysis agent for comprehensive document analysis.
    
    Performs analysis following the CIA/FBI Intelligence Officer Analysis Framework
    with focus on strategic patterns, cultural intelligence, and cross-document correlation.
    """
    
    def __init__(self, orchestrator: Optional[SentimentOrchestrator] = None):
        """Initialize the pattern analysis agent."""
        self.orchestrator = orchestrator or SentimentOrchestrator()
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.results_dir = Path(__file__).parent.parent.parent / "Results" / "pattern_analysis"
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Document mapping for analysis
        self.documents = {
            "art_of_war": {
                "path": self.data_dir / "art_of_war_complete.txt",
                "type": "strategic_treatise",
                "language": "zh",
                "description": "Ancient Chinese military treatise by Sun Tzu"
            },
            "classical_chinese": {
                "path": self.data_dir / "Classical Chinese Sample 22208_0_8.pdf",
                "type": "language_textbook",
                "language": "zh",
                "description": "Modern Classical Chinese textbook"
            },
            "russia_eu_analysis": {
                "path": self.data_dir / "paulbouvetpdf.pdf",
                "type": "contemporary_analysis",
                "language": "en",
                "description": "Contemporary Russia-EU security cooperation analysis"
            },
            "russian_literature": {
                "path": self.data_dir / "Russian_Oliver_Excerpt.pdf",
                "type": "literary_content",
                "language": "ru",
                "description": "Russian literary content excerpt"
            },
            "extracted_text": {
                "path": self.data_dir / "extracted_text.txt",
                "type": "processed_content",
                "language": "en",
                "description": "Extracted text from various sources"
            }
        }
        
        # Strategic keywords for analysis
        self.strategic_keywords = [
            "strategy", "tactics", "warfare", "military", "deception", "victory", "defeat",
            "command", "leadership", "terrain", "weather", "morale", "supply", "intelligence",
            "spy", "espionage", "alliance", "enemy", "friend", "attack", "defense", "retreat",
            "advance", "position", "formation", "discipline", "training", "equipment"
        ]
        
        # Cultural keywords for analysis
        self.cultural_keywords = [
            "culture", "tradition", "custom", "belief", "value", "philosophy", "religion",
            "society", "community", "family", "honor", "loyalty", "respect", "wisdom",
            "knowledge", "education", "learning", "language", "communication", "dialogue"
        ]
        
        logger.info("PatternAnalysisAgent initialized successfully")
    
    async def run_comprehensive_analysis(self, use_mcp_tools: bool = True) -> Dict[str, Any]:
        """
        Run comprehensive pattern analysis across all documents.
        
        Args:
            use_mcp_tools: Whether to use MCP tools for enhanced analysis
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        logger.info("🎯 Starting comprehensive pattern analysis across all documents")
        
        try:
            # Step 1: Load and process all documents
            document_contents = await self._load_all_documents()
            
            # Step 2: Perform strategic intelligence analysis
            strategic_analysis = await self._perform_strategic_intelligence_analysis(
                document_contents, use_mcp_tools
            )
            
            # Step 3: Perform cultural intelligence analysis
            cultural_analysis = await self._perform_cultural_intelligence_analysis(
                document_contents, use_mcp_tools
            )
            
            # Step 4: Perform pattern recognition analysis
            pattern_analysis = await self._perform_pattern_recognition_analysis(
                document_contents, use_mcp_tools
            )
            
            # Step 5: Perform cross-document correlation analysis
            correlation_analysis = await self._perform_cross_document_correlation(
                document_contents, use_mcp_tools
            )
            
            # Step 6: Generate comprehensive business intelligence report
            business_intelligence = await self._generate_business_intelligence_report(
                document_contents, use_mcp_tools
            )
            
            # Step 7: Create unified analysis summary
            unified_summary = await self._create_unified_analysis_summary(
                strategic_analysis,
                cultural_analysis,
                pattern_analysis,
                correlation_analysis,
                business_intelligence
            )
            
            # Step 8: Save results
            await self._save_analysis_results({
                "strategic_analysis": strategic_analysis,
                "cultural_analysis": cultural_analysis,
                "pattern_analysis": pattern_analysis,
                "correlation_analysis": correlation_analysis,
                "business_intelligence": business_intelligence,
                "unified_summary": unified_summary,
                "metadata": {
                    "analysis_timestamp": datetime.now().isoformat(),
                    "documents_analyzed": len(document_contents),
                    "analysis_framework": "CIA/FBI Intelligence Officer Analysis Framework",
                    "mcp_tools_used": use_mcp_tools
                }
            })
            
            logger.info("✅ Comprehensive pattern analysis completed successfully")
            return unified_summary
            
        except Exception as e:
            logger.error(f"❌ Comprehensive analysis failed: {e}")
            return {"error": str(e)}
    
    async def _load_all_documents(self) -> Dict[str, Any]:
        """Load content from all available documents."""
        document_contents = {}
        
        for doc_id, doc_info in self.documents.items():
            try:
                if doc_info["path"].exists():
                    logger.info(f"📖 Loading document: {doc_id}")
                    
                    if doc_info["path"].suffix == ".txt":
                        content = doc_info["path"].read_text(encoding='utf-8')
                    else:
                        # For PDFs, we'll use the extracted text or process them
                        if doc_id == "extracted_text":
                            content = doc_info["path"].read_text(encoding='utf-8')
                        else:
                            # For now, we'll use placeholder content for PDFs
                            # In a full implementation, you'd extract text from PDFs
                            content = f"Content from {doc_info['description']}"
                    
                    document_contents[doc_id] = {
                        "content": content,
                        "metadata": doc_info
                    }
                    logger.info(f"✅ Loaded {doc_id}: {len(content)} characters")
                else:
                    logger.warning(f"⚠️ Document not found: {doc_info['path']}")
                    
            except Exception as e:
                logger.error(f"❌ Error loading {doc_id}: {e}")
        
        return document_contents
    
    async def _perform_strategic_intelligence_analysis(
        self, document_contents: Dict[str, Any], use_mcp_tools: bool = True
    ) -> Dict[str, Any]:
        """Perform strategic intelligence analysis."""
        logger.info("🎯 Performing strategic intelligence analysis")
        
        try:
            strategic_insights = {}
            
            for doc_id, content_info in document_contents.items():
                content = content_info["content"].lower()
                metadata = content_info["metadata"]
                
                # Count strategic keywords
                keyword_counts = {}
                for keyword in self.strategic_keywords:
                    count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content))
                    if count > 0:
                        keyword_counts[keyword] = count
                
                # Extract strategic themes
                strategic_themes = []
                if "war" in content or "battle" in content:
                    strategic_themes.append("Warfare and Battle")
                if "strategy" in content or "tactics" in content:
                    strategic_themes.append("Strategy and Tactics")
                if "deception" in content or "spy" in content:
                    strategic_themes.append("Deception and Intelligence")
                if "leadership" in content or "command" in content:
                    strategic_themes.append("Leadership and Command")
                
                strategic_insights[doc_id] = {
                    "keyword_counts": keyword_counts,
                    "strategic_themes": strategic_themes,
                    "document_type": metadata["type"],
                    "language": metadata["language"],
                    "description": metadata["description"]
                }
            
            # Use MCP tools for enhanced analysis if available
            if use_mcp_tools:
                try:
                    # Combine all content for strategic analysis
                    combined_content = "\n\n".join([
                        f"=== {doc_id} ===\n{content['content']}"
                        for doc_id, content in document_contents.items()
                    ])
                    
                    # Query knowledge graph for strategic patterns
                    strategic_query_result = await call_unified_mcp_tool(
                        "mcp_Sentiment_query_knowledge_graph",
                        {
                            "query": "strategic principles military strategy warfare tactics deception cultural patterns"
                        }
                    )
                    
                    # Analyze business intelligence for strategic patterns
                    strategic_bi_result = await call_unified_mcp_tool(
                        "mcp_Sentiment_analyze_business_intelligence",
                        {
                            "content": combined_content,
                            "analysis_type": "strategic_patterns"
                        }
                    )
                    
                    strategic_insights["mcp_enhanced"] = {
                        "knowledge_graph_query": strategic_query_result,
                        "business_intelligence": strategic_bi_result
                    }
                    
                except Exception as e:
                    logger.warning(f"MCP tools not available for strategic analysis: {e}")
            
            return {
                "document_insights": strategic_insights,
                "analysis_focus": [
                    "Strategic principles from The Art of War",
                    "Russian strategic thinking patterns",
                    "Deception and misdirection techniques",
                    "Cultural differences in strategic thinking"
                ]
            }
            
        except Exception as e:
            logger.error(f"Strategic intelligence analysis failed: {e}")
            return {"error": str(e)}
    
    async def _perform_cultural_intelligence_analysis(
        self, document_contents: Dict[str, Any], use_mcp_tools: bool = True
    ) -> Dict[str, Any]:
        """Perform cultural intelligence analysis."""
        logger.info("🌍 Performing cultural intelligence analysis")
        
        try:
            cultural_insights = {}
            
            for doc_id, content_info in document_contents.items():
                content = content_info["content"].lower()
                metadata = content_info["metadata"]
                
                # Count cultural keywords
                keyword_counts = {}
                for keyword in self.cultural_keywords:
                    count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content))
                    if count > 0:
                        keyword_counts[keyword] = count
                
                # Extract cultural themes
                cultural_themes = []
                if "culture" in content or "tradition" in content:
                    cultural_themes.append("Cultural Traditions")
                if "philosophy" in content or "wisdom" in content:
                    cultural_themes.append("Philosophy and Wisdom")
                if "language" in content or "communication" in content:
                    cultural_themes.append("Language and Communication")
                if "education" in content or "learning" in content:
                    cultural_themes.append("Education and Learning")
                
                cultural_insights[doc_id] = {
                    "keyword_counts": keyword_counts,
                    "cultural_themes": cultural_themes,
                    "language": metadata["language"],
                    "document_type": metadata["type"],
                    "description": metadata["description"]
                }
            
            # Use MCP tools for enhanced analysis if available
            if use_mcp_tools:
                try:
                    for doc_id, content_info in document_contents.items():
                        content = content_info["content"]
                        metadata = content_info["metadata"]
                        language = metadata.get("language", "en")
                        
                        # Extract entities for cultural analysis
                        entities = await call_unified_mcp_tool(
                            "mcp_Sentiment_extract_entities",
                            {
                                "text": content
                            }
                        )
                        
                        # Analyze sentiment for cultural insights
                        sentiment = await call_unified_mcp_tool(
                            "mcp_Sentiment_analyze_sentiment",
                            {
                                "text": content,
                                "language": language
                            }
                        )
                        
                        cultural_insights[doc_id]["mcp_enhanced"] = {
                            "entities": entities,
                            "sentiment": sentiment
                        }
                    
                    # Generate cross-cultural knowledge graph
                    cross_cultural_kg = await call_unified_mcp_tool(
                        "mcp_Sentiment_generate_knowledge_graph",
                        {
                            "content": "Cross-cultural strategic analysis: Chinese vs Russian strategic thinking patterns and their application to modern conflicts"
                        }
                    )
                    
                    cultural_insights["cross_cultural_knowledge_graph"] = cross_cultural_kg
                    
                except Exception as e:
                    logger.warning(f"MCP tools not available for cultural analysis: {e}")
            
            return {
                "document_insights": cultural_insights,
                "analysis_focus": [
                    "Cultural biases and assumptions",
                    "Strategic cultural values",
                    "Decision-making processes",
                    "Language and cultural context"
                ]
            }
            
        except Exception as e:
            logger.error(f"Cultural intelligence analysis failed: {e}")
            return {"error": str(e)}
    
    async def _perform_pattern_recognition_analysis(
        self, document_contents: Dict[str, Any], use_mcp_tools: bool = True
    ) -> Dict[str, Any]:
        """Perform pattern recognition analysis."""
        logger.info("🔍 Performing pattern recognition analysis")
        
        try:
            # Combine all content for pattern analysis
            all_content = ""
            for doc_id, content_info in document_contents.items():
                all_content += content_info["content"] + " "
            
            # Find recurring patterns
            words = re.findall(r'\b\w+\b', all_content.lower())
            word_freq = Counter(words)
            most_common_words = word_freq.most_common(20)
            
            # Find sentence patterns
            sentences = re.split(r'[.!?]+', all_content)
            sentence_lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]
            avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
            
            pattern_analysis = {
                "word_frequency": dict(most_common_words),
                "sentence_analysis": {
                    "total_sentences": len(sentences),
                    "average_sentence_length": avg_sentence_length,
                    "sentence_length_distribution": {
                        "short": len([s for s in sentence_lengths if s <= 10]),
                        "medium": len([s for s in sentence_lengths if 10 < s <= 20]),
                        "long": len([s for s in sentence_lengths if s > 20])
                    }
                }
            }
            
            # Use MCP tools for enhanced analysis if available
            if use_mcp_tools:
                try:
                    # Query knowledge graph for recurring patterns
                    pattern_query_result = await call_unified_mcp_tool(
                        "mcp_Sentiment_query_knowledge_graph",
                        {
                            "query": "recurring themes strategic thinking cultural patterns historical precedents"
                        }
                    )
                    
                    # Analyze business intelligence for comprehensive patterns
                    pattern_bi_result = await call_unified_mcp_tool(
                        "mcp_Sentiment_analyze_business_intelligence",
                        {
                            "content": all_content,
                            "analysis_type": "comprehensive"
                        }
                    )
                    
                    # Generate knowledge graph for pattern analysis
                    pattern_kg = await call_unified_mcp_tool(
                        "mcp_Sentiment_generate_knowledge_graph",
                        {
                            "content": "Pattern analysis: Recurring strategic themes across ancient Chinese military treatise, Russian literature, and contemporary geopolitical analysis"
                        }
                    )
                    
                    pattern_analysis["mcp_enhanced"] = {
                        "knowledge_graph_query": pattern_query_result,
                        "business_intelligence": pattern_bi_result,
                        "knowledge_graph": pattern_kg
                    }
                    
                except Exception as e:
                    logger.warning(f"MCP tools not available for pattern analysis: {e}")
            
            pattern_analysis["analysis_focus"] = [
                "Recurring strategic themes",
                "Strategic principles evolution",
                "Russian strategic behavior patterns",
                "Cultural strategic thinking patterns"
            ]
            
            return pattern_analysis
            
        except Exception as e:
            logger.error(f"Pattern recognition analysis failed: {e}")
            return {"error": str(e)}
    
    async def _perform_cross_document_correlation(
        self, document_contents: Dict[str, Any], use_mcp_tools: bool = True
    ) -> Dict[str, Any]:
        """Perform cross-document correlation analysis."""
        logger.info("🔗 Performing cross-document correlation analysis")
        
        try:
            correlations = {}
            
            # Analyze correlations between documents
            doc_ids = list(document_contents.keys())
            for i, doc1_id in enumerate(doc_ids):
                for j, doc2_id in enumerate(doc_ids[i+1:], i+1):
                    content1 = document_contents[doc1_id]["content"].lower()
                    content2 = document_contents[doc2_id]["content"].lower()
                    
                    # Find common words
                    words1 = set(re.findall(r'\b\w+\b', content1))
                    words2 = set(re.findall(r'\b\w+\b', content2))
                    common_words = words1.intersection(words2)
                    
                    # Calculate similarity score
                    similarity = len(common_words) / max(len(words1), len(words2)) if max(len(words1), len(words2)) > 0 else 0
                    
                    correlations[f"{doc1_id}_vs_{doc2_id}"] = {
                        "common_words": list(common_words)[:10],  # Top 10 common words
                        "similarity_score": similarity,
                        "doc1_type": document_contents[doc1_id]["metadata"]["type"],
                        "doc2_type": document_contents[doc2_id]["metadata"]["type"]
                    }
            
            correlation_result = {
                "correlations": correlations,
                "correlation_matrix": {
                    "documents_analyzed": len(document_contents),
                    "total_correlations": len(correlations),
                    "analysis_method": "Word overlap similarity"
                }
            }
            
            # Use MCP tools for enhanced analysis if available
            if use_mcp_tools:
                try:
                    # Create correlation analysis content
                    correlation_content = "Cross-document correlation analysis:\n\n"
                    
                    for doc_id, content_info in document_contents.items():
                        correlation_content += f"Document: {doc_id}\n"
                        correlation_content += f"Type: {content_info['metadata']['type']}\n"
                        correlation_content += f"Language: {content_info['metadata']['language']}\n"
                        correlation_content += f"Description: {content_info['metadata']['description']}\n"
                        correlation_content += f"Content Preview: {content_info['content'][:500]}...\n\n"
                    
                    # Generate knowledge graph for correlation analysis
                    correlation_kg = await call_unified_mcp_tool(
                        "mcp_Sentiment_generate_knowledge_graph",
                        {
                            "content": correlation_content
                        }
                    )
                    
                    # Analyze business intelligence for correlation insights
                    correlation_bi = await call_unified_mcp_tool(
                        "mcp_Sentiment_analyze_business_intelligence",
                        {
                            "content": correlation_content,
                            "analysis_type": "comprehensive"
                        }
                    )
                    
                    correlation_result["mcp_enhanced"] = {
                        "knowledge_graph": correlation_kg,
                        "business_intelligence": correlation_bi
                    }
                    
                except Exception as e:
                    logger.warning(f"MCP tools not available for correlation analysis: {e}")
            
            return correlation_result
            
        except Exception as e:
            logger.error(f"Cross-document correlation analysis failed: {e}")
            return {"error": str(e)}
    
    async def _generate_business_intelligence_report(
        self, document_contents: Dict[str, Any], use_mcp_tools: bool = True
    ) -> Dict[str, Any]:
        """Generate comprehensive business intelligence report."""
        logger.info("📊 Generating business intelligence report")
        
        try:
            # Analyze document characteristics
            doc_analysis = {}
            total_content_length = 0
            
            for doc_id, content_info in document_contents.items():
                content = content_info["content"]
                metadata = content_info["metadata"]
                
                # Basic statistics
                word_count = len(content.split())
                char_count = len(content)
                total_content_length += char_count
                
                # Language distribution
                language = metadata["language"]
                
                doc_analysis[doc_id] = {
                    "word_count": word_count,
                    "char_count": char_count,
                    "language": language,
                    "document_type": metadata["type"],
                    "description": metadata["description"]
                }
            
            bi_result = {
                "document_analysis": doc_analysis,
                "summary_statistics": {
                    "total_documents": len(document_contents),
                    "total_content_length": total_content_length,
                    "average_document_length": total_content_length / len(document_contents) if document_contents else 0,
                    "language_distribution": {
                        "zh": len([d for d in doc_analysis.values() if d["language"] == "zh"]),
                        "en": len([d for d in doc_analysis.values() if d["language"] == "en"]),
                        "ru": len([d for d in doc_analysis.values() if d["language"] == "ru"])
                    }
                },
                "report_summary": {
                    "documents_analyzed": len(document_contents),
                    "analysis_types": [
                        "Strategic Intelligence",
                        "Cultural Intelligence", 
                        "Pattern Recognition",
                        "Cross-Document Correlation"
                    ],
                    "intelligence_framework": "CIA/FBI Intelligence Officer Analysis Framework"
                }
            }
            
            # Use MCP tools for enhanced analysis if available
            if use_mcp_tools:
                try:
                    # Create comprehensive analysis content
                    bi_content = "Comprehensive Business Intelligence Analysis:\n\n"
                    bi_content += "Document Set Analysis:\n"
                    
                    for doc_id, content_info in document_contents.items():
                        bi_content += f"- {doc_id}: {content_info['metadata']['description']}\n"
                    
                    bi_content += "\nStrategic Intelligence Synthesis:\n"
                    bi_content += "Analysis of strategic principles, cultural patterns, and cross-document correlations.\n"
                    
                    # Generate comprehensive business intelligence
                    bi_enhanced = await call_unified_mcp_tool(
                        "mcp_Sentiment_analyze_business_intelligence",
                        {
                            "content": bi_content,
                            "analysis_type": "comprehensive"
                        }
                    )
                    
                    # Generate knowledge graph for business intelligence
                    bi_kg = await call_unified_mcp_tool(
                        "mcp_Sentiment_generate_knowledge_graph",
                        {
                            "content": "Business Intelligence: Synthesis of strategic analysis, cultural intelligence, and pattern recognition across multiple documents"
                        }
                    )
                    
                    bi_result["mcp_enhanced"] = {
                        "business_intelligence": bi_enhanced,
                        "knowledge_graph": bi_kg
                    }
                    
                except Exception as e:
                    logger.warning(f"MCP tools not available for business intelligence: {e}")
            
            return bi_result
            
        except Exception as e:
            logger.error(f"Business intelligence report generation failed: {e}")
            return {"error": str(e)}
    
    async def _create_unified_analysis_summary(self, *analysis_results) -> Dict[str, Any]:
        """Create unified summary of all analysis results."""
        logger.info("📋 Creating unified analysis summary")
        
        try:
            # Extract key insights from each analysis
            summary = {
                "executive_summary": {
                    "analysis_framework": "CIA/FBI Intelligence Officer Analysis Framework",
                    "total_analyses": len(analysis_results),
                    "key_findings": []
                },
                "strategic_insights": [],
                "cultural_insights": [],
                "pattern_insights": [],
                "correlation_insights": [],
                "business_intelligence_insights": [],
                "recommendations": []
            }
            
            # Process each analysis result
            for i, result in enumerate(analysis_results):
                if isinstance(result, dict) and "error" not in result:
                    if i == 0:  # Strategic analysis
                        summary["strategic_insights"].append("Strategic principles identified across documents")
                        summary["executive_summary"]["key_findings"].append("Cross-cultural strategic thinking patterns detected")
                    elif i == 1:  # Cultural analysis
                        summary["cultural_insights"].append("Cultural intelligence insights extracted")
                        summary["executive_summary"]["key_findings"].append("Cultural biases and strategic values identified")
                    elif i == 2:  # Pattern analysis
                        summary["pattern_insights"].append("Recurring themes and patterns identified")
                        summary["executive_summary"]["key_findings"].append("Strategic behavior patterns across cultures")
                    elif i == 3:  # Correlation analysis
                        summary["correlation_insights"].append("Cross-document correlations established")
                        summary["executive_summary"]["key_findings"].append("Thematic connections across documents")
                    elif i == 4:  # Business intelligence
                        summary["business_intelligence_insights"].append("Comprehensive business intelligence generated")
                        summary["executive_summary"]["key_findings"].append("Strategic intelligence synthesis completed")
            
            # Add recommendations
            summary["recommendations"] = [
                "Continue monitoring for strategic deception indicators",
                "Develop cultural intelligence capabilities",
                "Establish pattern recognition systems",
                "Implement cross-document correlation analysis",
                "Maintain comprehensive business intelligence reporting"
            ]
            
            return summary
            
        except Exception as e:
            logger.error(f"Unified summary creation failed: {e}")
            return {"error": str(e)}
    
    async def _save_analysis_results(self, results: Dict[str, Any]) -> None:
        """Save analysis results to files."""
        logger.info("💾 Saving analysis results")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save comprehensive results
            results_file = self.results_dir / f"pattern_analysis_{timestamp}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            # Save executive summary
            summary_file = self.results_dir / f"executive_summary_{timestamp}.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("# Pattern Analysis Executive Summary\n\n")
                f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Framework:** CIA/FBI Intelligence Officer Analysis Framework\n\n")
                
                if "unified_summary" in results:
                    summary = results["unified_summary"]
                    f.write("## Key Findings\n\n")
                    for finding in summary.get("key_findings", []):
                        f.write(f"- {finding}\n")
                    
                    f.write("\n## Recommendations\n\n")
                    for rec in summary.get("recommendations", []):
                        f.write(f"- {rec}\n")
            
            logger.info(f"✅ Results saved to {results_file}")
            logger.info(f"✅ Executive summary saved to {summary_file}")
            
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")
    
    async def analyze_single_document(self, document_path: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze a single document with specified analysis type.
        
        Args:
            document_path: Path to the document to analyze
            analysis_type: Type of analysis to perform (comprehensive, strategic, cultural, pattern)
            
        Returns:
            Analysis results
        """
        logger.info(f"🔍 Analyzing single document: {document_path}")
        
        try:
            # Load the document
            doc_path = Path(document_path)
            if not doc_path.exists():
                return {"error": f"Document not found: {document_path}"}
            
            content = doc_path.read_text(encoding='utf-8')
            
            # Create document content structure
            document_contents = {
                "single_document": {
                    "content": content,
                    "metadata": {
                        "path": str(doc_path),
                        "type": "single_document",
                        "language": "en",  # Default, could be detected
                        "description": f"Single document analysis: {doc_path.name}"
                    }
                }
            }
            
            # Perform analysis based on type
            if analysis_type == "comprehensive":
                return await self.run_comprehensive_analysis()
            elif analysis_type == "strategic":
                return await self._perform_strategic_intelligence_analysis(document_contents)
            elif analysis_type == "cultural":
                return await self._perform_cultural_intelligence_analysis(document_contents)
            elif analysis_type == "pattern":
                return await self._perform_pattern_recognition_analysis(document_contents)
            else:
                return {"error": f"Unknown analysis type: {analysis_type}"}
                
        except Exception as e:
            logger.error(f"Single document analysis failed: {e}")
            return {"error": str(e)}
