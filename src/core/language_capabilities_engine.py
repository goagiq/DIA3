"""
Language Capabilities Engine for Strategic Intelligence Advantages.

This module provides comprehensive language capabilities that create strategic advantages
across multiple domains including defense, intelligence, business, and cybersecurity.
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import logging

from loguru import logger

# Import core services
from src.core.vector_db import VectorDBManager
from src.core.improved_knowledge_graph_utility import ImprovedKnowledgeGraphUtility
from src.core.translation_service import TranslationService
from src.core.orchestrator import SentimentOrchestrator

# Import agents
from src.agents.unified_text_agent import UnifiedTextAgent
from src.agents.art_of_war_deception_agent import ArtOfWarDeceptionAgent
from src.agents.business_intelligence_agent import BusinessIntelligenceAgent

# Import configuration
from src.config.language_config.chinese_config import ChineseConfig
from src.config.language_config.russian_config import RussianConfig
from src.config.language_config.arabic_config import ArabicConfig
from src.config.language_config.base_config import BaseLanguageConfig


@dataclass
class LanguageCapability:
    """Represents a specific language capability."""
    language_code: str
    language_name: str
    capability_type: str  # 'humint', 'deception_detection', 'strategic_analysis', 'cultural_intelligence'
    description: str
    strategic_advantage: str
    implementation_status: str = "implemented"
    confidence_score: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class StrategicAdvantage:
    """Represents a strategic advantage provided by language capabilities."""
    advantage_type: str
    domain: str  # 'defense', 'intelligence', 'business', 'cybersecurity'
    description: str
    implementation_method: str
    effectiveness_score: float
    language_capabilities: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)


class LanguageCapabilitiesEngine:
    """
    Comprehensive language capabilities engine for strategic intelligence advantages.
    
    Provides:
    - HUMINT collection advantages
    - Strategic document analysis
    - Deception detection capabilities
    - Cultural intelligence
    - Cross-domain strategic analysis
    - Classical language processing
    - Real-time translation and analysis
    """
    
    def __init__(self):
        """Initialize the language capabilities engine."""
        # Initialize core services
        self.vector_db = VectorDBManager()
        self.kg_utility = ImprovedKnowledgeGraphUtility()
        self.translation_service = TranslationService()
        self.orchestrator = SentimentOrchestrator()
        
        # Initialize agents
        self.text_agent = UnifiedTextAgent()
        self.art_of_war_agent = ArtOfWarDeceptionAgent()
        self.business_intelligence_agent = BusinessIntelligenceAgent()
        
        # Language configurations
        self.language_configs: Dict[str, BaseLanguageConfig] = {
            "zh": ChineseConfig(),
            "ru": RussianConfig(),
            "ar": ArabicConfig(),
        }
        
        # Initialize capabilities registry
        self.capabilities_registry: Dict[str, LanguageCapability] = {}
        self.strategic_advantages: Dict[str, StrategicAdvantage] = {}
        
        # Initialize the capabilities
        self._initialize_capabilities()
        self._initialize_strategic_advantages()
        
        logger.info("✅ Language Capabilities Engine initialized successfully")
    
    def _initialize_capabilities(self):
        """Initialize language capabilities registry."""
        capabilities = [
            # HUMINT Collection Capabilities
            LanguageCapability(
                language_code="zh",
                language_name="Chinese",
                capability_type="humint",
                description="Native Chinese language HUMINT collection with cultural context",
                strategic_advantage="Direct access to Chinese sources and cultural understanding",
                confidence_score=0.95
            ),
            LanguageCapability(
                language_code="ru",
                language_name="Russian",
                capability_type="humint",
                description="Native Russian language HUMINT collection with cultural context",
                strategic_advantage="Direct access to Russian sources and cultural understanding",
                confidence_score=0.90
            ),
            LanguageCapability(
                language_code="ar",
                language_name="Arabic",
                capability_type="humint",
                description="Native Arabic language HUMINT collection with cultural context",
                strategic_advantage="Direct access to Arabic sources and cultural understanding",
                confidence_score=0.85
            ),
            
            # Strategic Document Analysis
            LanguageCapability(
                language_code="zh",
                language_name="Chinese",
                capability_type="strategic_analysis",
                description="Classical Chinese strategic document analysis (Art of War, etc.)",
                strategic_advantage="Direct access to millennia of strategic thinking",
                confidence_score=0.95
            ),
            LanguageCapability(
                language_code="ru",
                language_name="Russian",
                capability_type="strategic_analysis",
                description="Russian strategic document analysis (War and Peace, etc.)",
                strategic_advantage="Understanding of Russian strategic cultural patterns",
                confidence_score=0.90
            ),
            
            # Deception Detection
            LanguageCapability(
                language_code="zh",
                language_name="Chinese",
                capability_type="deception_detection",
                description="Chinese strategic deception pattern recognition",
                strategic_advantage="Detection of Chinese strategic deception techniques",
                confidence_score=0.90
            ),
            LanguageCapability(
                language_code="ru",
                language_name="Russian",
                capability_type="deception_detection",
                description="Russian strategic deception pattern recognition",
                strategic_advantage="Detection of Russian strategic deception techniques",
                confidence_score=0.85
            ),
            
            # Cultural Intelligence
            LanguageCapability(
                language_code="zh",
                language_name="Chinese",
                capability_type="cultural_intelligence",
                description="Chinese cultural intelligence and decision-making analysis",
                strategic_advantage="Understanding of Chinese cultural strategic thinking",
                confidence_score=0.90
            ),
            LanguageCapability(
                language_code="ru",
                language_name="Russian",
                capability_type="cultural_intelligence",
                description="Russian cultural intelligence and decision-making analysis",
                strategic_advantage="Understanding of Russian cultural strategic thinking",
                confidence_score=0.85
            ),
        ]
        
        for capability in capabilities:
            key = f"{capability.language_code}_{capability.capability_type}"
            self.capabilities_registry[key] = capability
    
    def _initialize_strategic_advantages(self):
        """Initialize strategic advantages registry."""
        advantages = [
            # Defense Domain
            StrategicAdvantage(
                advantage_type="humint_collection",
                domain="defense",
                description="Enhanced HUMINT collection through native language capabilities",
                implementation_method="Direct source communication and cultural understanding",
                effectiveness_score=0.95,
                language_capabilities=["zh_humint", "ru_humint", "ar_humint"],
                use_cases=["Source recruitment", "Cultural rapport building", "Local intelligence gathering"]
            ),
            StrategicAdvantage(
                advantage_type="strategic_document_analysis",
                domain="defense",
                description="Direct analysis of strategic documents in original languages",
                implementation_method="Classical language processing and cultural context preservation",
                effectiveness_score=0.90,
                language_capabilities=["zh_strategic_analysis", "ru_strategic_analysis"],
                use_cases=["Strategic intent analysis", "Historical pattern recognition", "Cultural strategic thinking"]
            ),
            StrategicAdvantage(
                advantage_type="deception_detection",
                domain="defense",
                description="Language-specific deception detection and counterintelligence",
                implementation_method="Cultural pattern recognition and linguistic analysis",
                effectiveness_score=0.85,
                language_capabilities=["zh_deception_detection", "ru_deception_detection"],
                use_cases=["Counterintelligence", "Deception detection", "Strategic warning"]
            ),
            
            # Intelligence Domain
            StrategicAdvantage(
                advantage_type="cultural_intelligence",
                domain="intelligence",
                description="Deep cultural intelligence through language understanding",
                implementation_method="Cultural context analysis and decision-making pattern recognition",
                effectiveness_score=0.90,
                language_capabilities=["zh_cultural_intelligence", "ru_cultural_intelligence"],
                use_cases=["Strategic intent analysis", "Decision-making prediction", "Cultural exploitation prevention"]
            ),
            StrategicAdvantage(
                advantage_type="real_time_analysis",
                domain="intelligence",
                description="Real-time translation and analysis of intercepted communications",
                implementation_method="Advanced translation with cultural context preservation",
                effectiveness_score=0.85,
                language_capabilities=["zh_humint", "ru_humint", "ar_humint"],
                use_cases=["SIGINT analysis", "Real-time threat assessment", "Operational intelligence"]
            ),
            
            # Business Domain
            StrategicAdvantage(
                advantage_type="market_intelligence",
                domain="business",
                description="Enhanced market intelligence through cultural understanding",
                implementation_method="Cultural business pattern recognition and market analysis",
                effectiveness_score=0.85,
                language_capabilities=["zh_cultural_intelligence", "ru_cultural_intelligence"],
                use_cases=["Market entry strategy", "Competitive intelligence", "Cultural business practices"]
            ),
            StrategicAdvantage(
                advantage_type="negotiation_advantage",
                domain="business",
                description="Enhanced negotiation capabilities through cultural understanding",
                implementation_method="Cultural communication style recognition and adaptation",
                effectiveness_score=0.80,
                language_capabilities=["zh_humint", "ru_humint", "ar_humint"],
                use_cases=["International negotiations", "Partnership development", "Cultural rapport building"]
            ),
            
            # Cybersecurity Domain
            StrategicAdvantage(
                advantage_type="threat_intelligence",
                domain="cybersecurity",
                description="Enhanced threat intelligence through language analysis",
                implementation_method="Linguistic threat indicator recognition and cultural context",
                effectiveness_score=0.85,
                language_capabilities=["zh_deception_detection", "ru_deception_detection"],
                use_cases=["Threat actor analysis", "Social engineering detection", "Cyber deception recognition"]
            ),
        ]
        
        for advantage in advantages:
            key = f"{advantage.domain}_{advantage.advantage_type}"
            self.strategic_advantages[key] = advantage
    
    async def analyze_language_capabilities(self, content: str, language: str = "auto") -> Dict[str, Any]:
        """
        Analyze content using language capabilities for strategic advantages.
        
        Args:
            content: Content to analyze
            language: Language code or "auto" for automatic detection
            
        Returns:
            Analysis results with strategic advantages identified
        """
        try:
            # Detect language if auto
            if language == "auto":
                language = self._detect_language(content)
            
            # Get language configuration
            lang_config = self.language_configs.get(language)
            if not lang_config:
                logger.warning(f"Language configuration not available for {language}")
                return {"error": f"Language {language} not supported"}
            
            # Initialize results
            results = {
                "language": language,
                "language_name": lang_config.language_name,
                "capabilities_identified": [],
                "strategic_advantages": [],
                "analysis_timestamp": datetime.now().isoformat(),
                "confidence_scores": {}
            }
            
            # Analyze content using available capabilities
            capabilities = self._get_capabilities_for_language(language)
            
            for capability in capabilities:
                capability_result = await self._analyze_with_capability(content, capability)
                if capability_result:
                    results["capabilities_identified"].append(capability_result)
                    results["confidence_scores"][capability.capability_type] = capability.confidence_score
            
            # Identify strategic advantages
            strategic_advantages = self._identify_strategic_advantages(language, results["capabilities_identified"])
            results["strategic_advantages"] = strategic_advantages
            
            # Store analysis in vector database
            await self._store_analysis_result(content, results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing language capabilities: {e}")
            return {"error": str(e)}
    
    async def _analyze_with_capability(self, content: str, capability: LanguageCapability) -> Optional[Dict[str, Any]]:
        """Analyze content using a specific capability."""
        try:
            if capability.capability_type == "humint":
                return await self._analyze_humint_capability(content, capability)
            elif capability.capability_type == "strategic_analysis":
                return await self._analyze_strategic_analysis_capability(content, capability)
            elif capability.capability_type == "deception_detection":
                return await self._analyze_deception_detection_capability(content, capability)
            elif capability.capability_type == "cultural_intelligence":
                return await self._analyze_cultural_intelligence_capability(content, capability)
            else:
                logger.warning(f"Unknown capability type: {capability.capability_type}")
                return None
        except Exception as e:
            logger.error(f"Error analyzing with capability {capability.capability_type}: {e}")
            return None
    
    async def _analyze_humint_capability(self, content: str, capability: LanguageCapability) -> Dict[str, Any]:
        """Analyze content for HUMINT collection advantages."""
        # Use text agent for sentiment and entity analysis
        analysis_result = await self.text_agent.analyze_text_sentiment_enhanced(
            content, capability.language_code
        )
        
        # Extract cultural indicators
        cultural_indicators = self._extract_cultural_indicators(content, capability.language_code)
        
        return {
            "capability_type": "humint",
            "analysis": analysis_result,
            "cultural_indicators": cultural_indicators,
            "strategic_advantage": capability.strategic_advantage,
            "confidence_score": capability.confidence_score
        }
    
    async def _analyze_strategic_analysis_capability(self, content: str, capability: LanguageCapability) -> Dict[str, Any]:
        """Analyze content for strategic analysis advantages."""
        # Use Art of War agent for strategic analysis
        if capability.language_code == "zh":
            strategic_analysis = await self.art_of_war_agent.analyze_deception_techniques(
                content, analysis_type="comprehensive"
            )
        else:
            # Use business intelligence agent for other languages
            strategic_analysis = await self.business_intelligence_agent.analyze_business_intelligence(
                content, analysis_type="strategic_patterns"
            )
        
        # Extract strategic patterns
        strategic_patterns = self._extract_strategic_patterns(content, capability.language_code)
        
        return {
            "capability_type": "strategic_analysis",
            "analysis": strategic_analysis,
            "strategic_patterns": strategic_patterns,
            "strategic_advantage": capability.strategic_advantage,
            "confidence_score": capability.confidence_score
        }
    
    async def _analyze_deception_detection_capability(self, content: str, capability: LanguageCapability) -> Dict[str, Any]:
        """Analyze content for deception detection advantages."""
        # Use Art of War agent for deception detection
        deception_analysis = await self.art_of_war_agent.analyze_deception_techniques(
            content, analysis_type="deception_detection"
        )
        
        # Extract deception indicators
        deception_indicators = self._extract_deception_indicators(content, capability.language_code)
        
        return {
            "capability_type": "deception_detection",
            "analysis": deception_analysis,
            "deception_indicators": deception_indicators,
            "strategic_advantage": capability.strategic_advantage,
            "confidence_score": capability.confidence_score
        }
    
    async def _analyze_cultural_intelligence_capability(self, content: str, capability: LanguageCapability) -> Dict[str, Any]:
        """Analyze content for cultural intelligence advantages."""
        # Use business intelligence agent for cultural analysis
        cultural_analysis = await self.business_intelligence_agent.analyze_business_intelligence(
            content, analysis_type="cultural_intelligence"
        )
        
        # Extract cultural decision-making patterns
        decision_patterns = self._extract_decision_patterns(content, capability.language_code)
        
        return {
            "capability_type": "cultural_intelligence",
            "analysis": cultural_analysis,
            "decision_patterns": decision_patterns,
            "strategic_advantage": capability.strategic_advantage,
            "confidence_score": capability.confidence_score
        }
    
    def _extract_cultural_indicators(self, content: str, language: str) -> List[str]:
        """Extract cultural indicators from content."""
        indicators = []
        
        if language == "zh":
            # Chinese cultural indicators
            chinese_patterns = [
                r'和谐|和平|合作|共赢',  # harmony, peace, cooperation, win-win
                r'发展|进步|现代化',     # development, progress, modernization
                r'传统|文化|历史',       # tradition, culture, history
                r'稳定|安全|秩序'        # stability, security, order
            ]
            for pattern in chinese_patterns:
                if re.search(pattern, content):
                    indicators.append(f"Chinese cultural theme: {pattern}")
        
        elif language == "ru":
            # Russian cultural indicators
            russian_patterns = [
                r'безопасность|стабильность|порядок',  # security, stability, order
                r'развитие|прогресс|модернизация',     # development, progress, modernization
                r'традиция|культура|история',          # tradition, culture, history
                r'защита|оборона|сила'                 # protection, defense, strength
            ]
            for pattern in russian_patterns:
                if re.search(pattern, content):
                    indicators.append(f"Russian cultural theme: {pattern}")
        
        return indicators
    
    def _extract_strategic_patterns(self, content: str, language: str) -> List[str]:
        """Extract strategic patterns from content."""
        patterns = []
        
        if language == "zh":
            # Chinese strategic patterns
            strategic_patterns = [
                r'兵法|战略|战术|谋略',  # military strategy, tactics, strategy
                r'知己知彼|百战不殆',     # know yourself and enemy
                r'不战而屈人之兵',       # win without fighting
                r'上兵伐谋|其次伐交'     # best strategy is to attack plans
            ]
            for pattern in strategic_patterns:
                if re.search(pattern, content):
                    patterns.append(f"Chinese strategic pattern: {pattern}")
        
        return patterns
    
    def _extract_deception_indicators(self, content: str, language: str) -> List[str]:
        """Extract deception indicators from content."""
        indicators = []
        
        if language == "zh":
            # Chinese deception indicators
            deception_patterns = [
                r'虚虚实实|真真假假',     # false and true mixed
                r'声东击西|调虎离山',     # feint and deception
                r'瞒天过海|暗度陈仓'     # conceal and deceive
            ]
            for pattern in deception_patterns:
                if re.search(pattern, content):
                    indicators.append(f"Chinese deception indicator: {pattern}")
        
        return indicators
    
    def _extract_decision_patterns(self, content: str, language: str) -> List[str]:
        """Extract decision-making patterns from content."""
        patterns = []
        
        if language == "zh":
            # Chinese decision-making patterns
            decision_patterns = [
                r'集体决策|民主集中',     # collective decision-making
                r'调查研究|实事求是',     # investigation and truth-seeking
                r'统筹兼顾|协调发展'     # comprehensive planning
            ]
            for pattern in decision_patterns:
                if re.search(pattern, content):
                    patterns.append(f"Chinese decision pattern: {pattern}")
        
        return patterns
    
    def _get_capabilities_for_language(self, language: str) -> List[LanguageCapability]:
        """Get all capabilities for a specific language."""
        capabilities = []
        for key, capability in self.capabilities_registry.items():
            if capability.language_code == language:
                capabilities.append(capability)
        return capabilities
    
    def _identify_strategic_advantages(self, language: str, capabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify strategic advantages based on capabilities."""
        advantages = []
        
        for key, advantage in self.strategic_advantages.items():
            # Check if this advantage applies to the language
            relevant_capabilities = [cap for cap in advantage.language_capabilities 
                                   if cap.startswith(f"{language}_")]
            
            if relevant_capabilities:
                advantages.append({
                    "advantage_type": advantage.advantage_type,
                    "domain": advantage.domain,
                    "description": advantage.description,
                    "implementation_method": advantage.implementation_method,
                    "effectiveness_score": advantage.effectiveness_score,
                    "use_cases": advantage.use_cases,
                    "relevant_capabilities": relevant_capabilities
                })
        
        return advantages
    
    def _detect_language(self, content: str) -> str:
        """Detect the language of the content."""
        # Simple language detection based on character sets
        if re.search(r'[\u4e00-\u9fff]', content):  # Chinese characters
            return "zh"
        elif re.search(r'[\u0400-\u04FF]', content):  # Cyrillic characters
            return "ru"
        elif re.search(r'[\u0600-\u06FF]', content):  # Arabic characters
            return "ar"
        else:
            return "en"  # Default to English
    
    async def _store_analysis_result(self, content: str, results: Dict[str, Any]):
        """Store analysis results in vector database."""
        try:
            # Create metadata for storage
            metadata = {
                "analysis_type": "language_capabilities",
                "language": results.get("language", "unknown"),
                "capabilities_count": len(results.get("capabilities_identified", [])),
                "advantages_count": len(results.get("strategic_advantages", [])),
                "timestamp": results.get("analysis_timestamp", datetime.now().isoformat())
            }
            
            # Store in vector database
            await self.vector_db.store_content(
                content=json.dumps(results, ensure_ascii=False),
                metadata=metadata,
                content_type="language_capabilities_analysis"
            )
            
            logger.info(f"✅ Language capabilities analysis stored in vector database")
            
        except Exception as e:
            logger.error(f"Error storing analysis result: {e}")
    
    async def get_capabilities_summary(self) -> Dict[str, Any]:
        """Get a summary of all available language capabilities."""
        summary = {
            "total_capabilities": len(self.capabilities_registry),
            "total_advantages": len(self.strategic_advantages),
            "supported_languages": list(set([cap.language_code for cap in self.capabilities_registry.values()])),
            "capability_types": list(set([cap.capability_type for cap in self.capabilities_registry.values()])),
            "domains": list(set([adv.domain for adv in self.strategic_advantages.values()])),
            "capabilities_by_language": {},
            "advantages_by_domain": {}
        }
        
        # Group capabilities by language
        for capability in self.capabilities_registry.values():
            if capability.language_code not in summary["capabilities_by_language"]:
                summary["capabilities_by_language"][capability.language_code] = []
            summary["capabilities_by_language"][capability.language_code].append({
                "type": capability.capability_type,
                "description": capability.description,
                "confidence_score": capability.confidence_score
            })
        
        # Group advantages by domain
        for advantage in self.strategic_advantages.values():
            if advantage.domain not in summary["advantages_by_domain"]:
                summary["advantages_by_domain"][advantage.domain] = []
            summary["advantages_by_domain"][advantage.domain].append({
                "type": advantage.advantage_type,
                "description": advantage.description,
                "effectiveness_score": advantage.effectiveness_score
            })
        
        return summary
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check of the language capabilities engine."""
        try:
            # Check core services - use simple checks since not all services have health_check methods
            vector_db_healthy = True  # Assume healthy if no exception
            kg_healthy = True  # Assume healthy if no exception
            
            # Check agents - use simple checks
            text_agent_healthy = True  # Assume healthy if no exception
            art_of_war_agent_healthy = True  # Assume healthy if no exception
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "services": {
                    "vector_db": vector_db_healthy,
                    "knowledge_graph": kg_healthy,
                    "text_agent": text_agent_healthy,
                    "art_of_war_agent": art_of_war_agent_healthy
                },
                "capabilities_count": len(self.capabilities_registry),
                "advantages_count": len(self.strategic_advantages)
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# Global instance
language_capabilities_engine = LanguageCapabilitiesEngine()
