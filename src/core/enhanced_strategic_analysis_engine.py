"""
Enhanced Strategic Analysis Engine

This module provides comprehensive strategic analysis capabilities based on The Art of War principles,
integrated with multi-domain support for defense, intelligence, and business applications.
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from uuid import uuid4
from dataclasses import dataclass, field
from enum import Enum

from loguru import logger

from src.core.models import AnalysisRequest, AnalysisResult, DataType
from src.core.error_handler import with_error_handling
from src.core.pattern_recognition import AnomalyDetector, PatternClassifier


class DomainType(Enum):
    """Supported analysis domains."""
    DEFENSE = "defense"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    CYBERSECURITY = "cybersecurity"
    GEOPOLITICAL = "geopolitical"
    FINANCIAL = "financial"
    HEALTHCARE = "healthcare"
    ENERGY = "energy"
    TRANSPORTATION = "transportation"
    CRITICAL_INFRASTRUCTURE = "critical_infrastructure"


@dataclass
class ArtOfWarPrinciple:
    """Represents an Art of War principle with modern applications."""
    chinese: str
    translation: str
    explanation: str
    modern_applications: List[str]
    domain_applications: Dict[str, List[str]]
    detection_patterns: List[str]
    counter_strategies: List[str]


@dataclass
class StrategicMove:
    """Represents a potential strategic move based on Art of War principles."""
    move_id: str
    principle: str
    domain: str
    description: str
    likelihood: float
    impact: str  # low, medium, high, critical
    indicators: List[str]
    counter_measures: List[str]
    timeframe: str  # immediate, short_term, medium_term, long_term
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategicAnalysis:
    """Comprehensive strategic analysis result."""
    analysis_id: str
    domain: str
    content: str
    principles_detected: List[ArtOfWarPrinciple]
    strategic_moves: List[StrategicMove]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class EnhancedStrategicAnalysisEngine:
    """
    Enhanced strategic analysis engine based on The Art of War principles.
    
    Provides multi-domain strategic analysis capabilities for:
    - Defense and military applications
    - Intelligence and security analysis
    - Business strategy and competitive intelligence
    - Cybersecurity threat assessment
    - Geopolitical analysis
    """
    
    def __init__(self):
        """Initialize the enhanced strategic analysis engine."""
        self.art_of_war_principles = self._initialize_art_of_war_principles()
        self.domain_patterns = self._initialize_domain_patterns()
        self.anomaly_detector = AnomalyDetector()
        self.pattern_classifier = PatternClassifier()
        
        # Analysis state
        self.analysis_history: List[StrategicAnalysis] = []
        self.detected_patterns: Dict[str, List[str]] = {}
        self.risk_assessments: Dict[str, Dict[str, Any]] = {}
        
        logger.info("EnhancedStrategicAnalysisEngine initialized successfully")
    
    def _initialize_art_of_war_principles(self) -> Dict[str, ArtOfWarPrinciple]:
        """Initialize Art of War principles with modern applications."""
        return {
            "show_inability_when_able": ArtOfWarPrinciple(
                chinese="能而示之不能",
                translation="Show inability when able",
                explanation="Downplaying capabilities during negotiations while maintaining readiness",
                modern_applications=[
                    "Publicly reducing defense spending while secretly modernizing",
                    "Feigning disinterest in certain regions while actively pursuing influence",
                    "Appearing weak in negotiations while maintaining strong positions"
                ],
                domain_applications={
                    "defense": ["Military posturing", "Capability concealment", "Strategic ambiguity"],
                    "intelligence": ["Source protection", "Operational security", "Cover stories"],
                    "business": ["Competitive positioning", "Market entry strategies", "Negotiation tactics"],
                    "cybersecurity": ["Honeypot deployment", "False vulnerability display", "Deceptive security postures"]
                },
                detection_patterns=[
                    r"\b(weak|limited|constrained|restricted)\b.*\b(capability|ability|capacity)\b",
                    r"\b(reduce|cut|minimize)\b.*\b(spending|budget|resources)\b",
                    r"\b(not interested|disinterested|unconcerned)\b.*\b(region|area|market)\b"
                ],
                counter_strategies=[
                    "Multiple source verification",
                    "Pattern analysis across time",
                    "Behavioral consistency checking",
                    "Resource allocation monitoring"
                ]
            ),
            "show_disuse_when_using": ArtOfWarPrinciple(
                chinese="用而示之不用",
                translation="Show disuse when using",
                explanation="Appearing disinterested while actively pursuing influence",
                modern_applications=[
                    "Publicly withdrawing from a region while maintaining covert operations",
                    "Announcing policy changes while secretly maintaining old approaches",
                    "Appearing inactive while conducting behind-the-scenes activities"
                ],
                domain_applications={
                    "defense": ["Troop withdrawal announcements", "Base closure declarations", "Military reduction claims"],
                    "intelligence": ["Agent withdrawal claims", "Operation termination announcements", "Cover story deployment"],
                    "business": ["Market exit announcements", "Product discontinuation claims", "Service reduction declarations"],
                    "cybersecurity": ["Security tool removal claims", "Monitoring reduction announcements", "Defense capability claims"]
                },
                detection_patterns=[
                    r"\b(withdraw|exit|leave|abandon)\b.*\b(region|market|area)\b",
                    r"\b(terminate|end|stop|discontinue)\b.*\b(operation|activity|service)\b",
                    r"\b(reduce|minimize|eliminate)\b.*\b(presence|involvement|participation)\b"
                ],
                counter_strategies=[
                    "Activity monitoring",
                    "Resource tracking",
                    "Behavioral analysis",
                    "Pattern recognition"
                ]
            ),
            "lure_with_profit": ArtOfWarPrinciple(
                chinese="利而誘之",
                translation="Lure with profit",
                explanation="Offering economic incentives to gain diplomatic concessions",
                modern_applications=[
                    "Trade agreements that appear beneficial but contain hidden strategic advantages",
                    "Investment offers with strategic conditions",
                    "Economic cooperation with political strings attached"
                ],
                domain_applications={
                    "defense": ["Military cooperation offers", "Technology sharing agreements", "Joint exercise invitations"],
                    "intelligence": ["Information sharing proposals", "Joint investigation offers", "Technology exchange agreements"],
                    "business": ["Partnership proposals", "Investment opportunities", "Market access offers"],
                    "cybersecurity": ["Security collaboration offers", "Threat intelligence sharing", "Joint defense initiatives"]
                },
                detection_patterns=[
                    r"\b(beneficial|advantageous|profitable)\b.*\b(agreement|deal|partnership)\b",
                    r"\b(cooperation|collaboration|partnership)\b.*\b(mutual|shared|joint)\b",
                    r"\b(investment|funding|support)\b.*\b(opportunity|proposal|offer)\b"
                ],
                counter_strategies=[
                    "Terms analysis",
                    "Hidden condition identification",
                    "Long-term impact assessment",
                    "Strategic consequence evaluation"
                ]
            ),
            "separate_when_united": ArtOfWarPrinciple(
                chinese="親而離之",
                translation="Separate when united",
                explanation="Breaking up alliances and coalitions",
                modern_applications=[
                    "Bilateral deals that undermine multilateral agreements",
                    "Playing allies against each other",
                    "Creating divisions within international organizations"
                ],
                domain_applications={
                    "defense": ["Bilateral defense agreements", "Alliance weakening strategies", "Coalition disruption"],
                    "intelligence": ["Information sharing restrictions", "Alliance intelligence gaps", "Cooperative framework weakening"],
                    "business": ["Exclusive partnership offers", "Competitive positioning", "Market division strategies"],
                    "cybersecurity": ["Selective threat sharing", "Alliance security gaps", "Cooperative defense weakening"]
                },
                detection_patterns=[
                    r"\b(bilateral|exclusive|private)\b.*\b(agreement|deal|arrangement)\b",
                    r"\b(separate|individual|independent)\b.*\b(approach|strategy|policy)\b",
                    r"\b(direct|private|confidential)\b.*\b(negotiation|discussion|meeting)\b"
                ],
                counter_strategies=[
                    "Alliance monitoring",
                    "Coordination verification",
                    "Unity maintenance",
                    "Collective response coordination"
                ]
            ),
            "attack_unprepared": ArtOfWarPrinciple(
                chinese="攻其無備，出其不意",
                translation="Attack unprepared, emerge unexpectedly",
                explanation="Diplomatic initiatives that catch adversaries off guard",
                modern_applications=[
                    "Sudden policy announcements that change the diplomatic landscape",
                    "Unexpected military movements or exercises",
                    "Surprise economic measures or sanctions"
                ],
                domain_applications={
                    "defense": ["Surprise military operations", "Unexpected troop movements", "Sudden capability demonstrations"],
                    "intelligence": ["Surprise information releases", "Unexpected source activations", "Sudden operational changes"],
                    "business": ["Surprise market entries", "Unexpected product launches", "Sudden strategic announcements"],
                    "cybersecurity": ["Surprise cyber attacks", "Unexpected security breaches", "Sudden vulnerability disclosures"]
                },
                detection_patterns=[
                    r"\b(sudden|unexpected|surprise)\b.*\b(announcement|action|move)\b",
                    r"\b(immediate|urgent|critical)\b.*\b(response|action|measure)\b",
                    r"\b(unprepared|unaware|unexpected)\b.*\b(situation|circumstance|condition)\b"
                ],
                counter_strategies=[
                    "Early warning systems",
                    "Intelligence monitoring",
                    "Preparedness maintenance",
                    "Rapid response capabilities"
                ]
            )
        }
    
    def _initialize_domain_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize domain-specific detection patterns."""
        return {
            "defense": {
                "military_posturing": [
                    r"\b(military|defense|security)\b.*\b(exercise|drill|training)\b",
                    r"\b(troop|force|unit)\b.*\b(movement|deployment|positioning)\b",
                    r"\b(capability|capacity|readiness)\b.*\b(demonstration|showcase|display)\b"
                ],
                "strategic_communication": [
                    r"\b(national|state|government)\b.*\b(security|defense|protection)\b",
                    r"\b(threat|challenge|risk)\b.*\b(response|counter|address)\b",
                    r"\b(alliance|partnership|cooperation)\b.*\b(defense|security|protection)\b"
                ]
            },
            "intelligence": {
                "information_operations": [
                    r"\b(intelligence|information|data)\b.*\b(collection|gathering|analysis)\b",
                    r"\b(source|agent|informant)\b.*\b(activation|deployment|operation)\b",
                    r"\b(surveillance|monitoring|tracking)\b.*\b(target|subject|entity)\b"
                ],
                "deception_operations": [
                    r"\b(cover|disguise|concealment)\b.*\b(operation|activity|mission)\b",
                    r"\b(false|deceptive|misleading)\b.*\b(information|intelligence|data)\b",
                    r"\b(plausible|credible|believable)\b.*\b(deniability|cover|story)\b"
                ]
            },
            "business": {
                "competitive_intelligence": [
                    r"\b(market|competitive|business)\b.*\b(intelligence|analysis|research)\b",
                    r"\b(competitor|rival|opponent)\b.*\b(move|action|strategy)\b",
                    r"\b(market|industry|sector)\b.*\b(position|share|presence)\b"
                ],
                "strategic_positioning": [
                    r"\b(strategic|competitive|market)\b.*\b(advantage|position|edge)\b",
                    r"\b(partnership|alliance|collaboration)\b.*\b(business|commercial|economic)\b",
                    r"\b(investment|acquisition|merger)\b.*\b(strategic|competitive|market)\b"
                ]
            },
            "cybersecurity": {
                "threat_operations": [
                    r"\b(cyber|digital|online)\b.*\b(threat|attack|breach)\b",
                    r"\b(security|defense|protection)\b.*\b(vulnerability|weakness|exposure)\b",
                    r"\b(malware|virus|trojan)\b.*\b(detection|prevention|response)\b"
                ],
                "defense_posturing": [
                    r"\b(cyber|digital|information)\b.*\b(defense|security|protection)\b",
                    r"\b(threat|intelligence|monitoring)\b.*\b(system|platform|capability)\b",
                    r"\b(incident|breach|attack)\b.*\b(response|recovery|mitigation)\b"
                ]
            }
        }
    
    async def analyze_strategic_content(
        self,
        content: str,
        domain: str,
        language: str = "en",
        analysis_depth: str = "comprehensive"
    ) -> StrategicAnalysis:
        """
        Analyze content for strategic patterns based on Art of War principles.
        
        Args:
            content: Text content to analyze
            domain: Analysis domain (defense, intelligence, business, etc.)
            language: Content language
            analysis_depth: Analysis depth (basic, standard, comprehensive)
        
        Returns:
            StrategicAnalysis object with comprehensive results
        """
        analysis_id = str(uuid4())
        timestamp = datetime.now()
        
        logger.info(f"Starting strategic analysis for domain: {domain}")
        
        # Detect Art of War principles
        principles_detected = await self._detect_art_of_war_principles(content, domain)
        
        # Identify strategic moves
        strategic_moves = await self._identify_strategic_moves(content, domain, principles_detected)
        
        # Assess risks
        risk_assessment = await self._assess_strategic_risks(content, domain, strategic_moves)
        
        # Generate recommendations
        recommendations = await self._generate_strategic_recommendations(
            domain, principles_detected, strategic_moves, risk_assessment
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            principles_detected, strategic_moves, risk_assessment
        )
        
        # Create analysis result
        analysis = StrategicAnalysis(
            analysis_id=analysis_id,
            domain=domain,
            content=content,
            principles_detected=principles_detected,
            strategic_moves=strategic_moves,
            risk_assessment=risk_assessment,
            recommendations=recommendations,
            confidence_score=confidence_score,
            timestamp=timestamp
        )
        
        # Store in history
        self.analysis_history.append(analysis)
        
        logger.info(f"Strategic analysis completed with confidence: {confidence_score:.2f}")
        
        return analysis
    
    async def _detect_art_of_war_principles(
        self,
        content: str,
        domain: str
    ) -> List[ArtOfWarPrinciple]:
        """Detect Art of War principles in content."""
        detected_principles = []
        
        for principle_name, principle in self.art_of_war_principles.items():
            # Check detection patterns
            for pattern in principle.detection_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_principles.append(principle)
                    break
            
            # Check domain-specific applications
            if domain in principle.domain_applications:
                domain_patterns = principle.domain_applications[domain]
                for pattern in domain_patterns:
                    if re.search(rf"\b{pattern}\b", content, re.IGNORECASE):
                        if principle not in detected_principles:
                            detected_principles.append(principle)
                        break
        
        return detected_principles
    
    async def _identify_strategic_moves(
        self,
        content: str,
        domain: str,
        principles: List[ArtOfWarPrinciple]
    ) -> List[StrategicMove]:
        """Identify potential strategic moves based on detected principles."""
        strategic_moves = []
        
        for principle in principles:
            # Generate strategic moves based on principle and domain
            moves = await self._generate_strategic_moves_for_principle(
                principle, domain, content
            )
            strategic_moves.extend(moves)
        
        return strategic_moves
    
    async def _generate_strategic_moves_for_principle(
        self,
        principle: ArtOfWarPrinciple,
        domain: str,
        content: str
    ) -> List[StrategicMove]:
        """Generate strategic moves for a specific principle and domain."""
        moves = []
        
        # Get domain-specific applications
        domain_applications = principle.domain_applications.get(domain, [])
        
        for application in domain_applications:
            # Check if application is relevant to content
            if re.search(rf"\b{application}\b", content, re.IGNORECASE):
                move = StrategicMove(
                    move_id=str(uuid4()),
                    principle=principle.chinese,
                    domain=domain,
                    description=f"Potential {application.lower()} based on {principle.translation}",
                    likelihood=self._calculate_move_likelihood(content, application),
                    impact=self._assess_move_impact(domain, application),
                    indicators=self._identify_move_indicators(content, application),
                    counter_measures=principle.counter_strategies,
                    timeframe=self._assess_move_timeframe(content, application),
                    confidence=self._calculate_move_confidence(content, application)
                )
                moves.append(move)
        
        return moves
    
    def _calculate_move_likelihood(self, content: str, application: str) -> float:
        """Calculate likelihood of a strategic move."""
        # Simple heuristic based on keyword frequency and context
        keywords = application.lower().split()
        matches = sum(1 for keyword in keywords if keyword in content.lower())
        return min(matches / len(keywords), 1.0)
    
    def _assess_move_impact(self, domain: str, application: str) -> str:
        """Assess the potential impact of a strategic move."""
        # Domain-specific impact assessment
        impact_mapping = {
            "defense": {"military": "high", "posturing": "medium", "capability": "high"},
            "intelligence": {"information": "high", "source": "critical", "operation": "high"},
            "business": {"market": "medium", "competitive": "high", "strategic": "high"},
            "cybersecurity": {"attack": "critical", "breach": "high", "defense": "medium"}
        }
        
        domain_impacts = impact_mapping.get(domain, {})
        for key, impact in domain_impacts.items():
            if key in application.lower():
                return impact
        
        return "medium"
    
    def _identify_move_indicators(self, content: str, application: str) -> List[str]:
        """Identify indicators of a potential strategic move."""
        indicators = []
        
        # Look for related keywords and phrases
        related_terms = {
            "military": ["troop", "force", "defense", "security"],
            "intelligence": ["information", "source", "operation", "agent"],
            "business": ["market", "competitive", "strategy", "position"],
            "cybersecurity": ["attack", "breach", "security", "threat"]
        }
        
        # Find relevant indicators based on application type
        for category, terms in related_terms.items():
            if category in application.lower():
                for term in terms:
                    if term in content.lower():
                        indicators.append(f"Indicates {category} activity: {term}")
        
        return indicators
    
    def _assess_move_timeframe(self, content: str, application: str) -> str:
        """Assess the timeframe for a potential strategic move."""
        # Look for temporal indicators
        immediate_indicators = ["immediate", "urgent", "now", "asap", "critical"]
        short_term_indicators = ["soon", "shortly", "quickly", "rapid", "fast"]
        medium_term_indicators = ["planning", "preparing", "developing", "building"]
        long_term_indicators = ["long-term", "future", "eventually", "ultimately"]
        
        content_lower = content.lower()
        
        for indicator in immediate_indicators:
            if indicator in content_lower:
                return "immediate"
        
        for indicator in short_term_indicators:
            if indicator in content_lower:
                return "short_term"
        
        for indicator in medium_term_indicators:
            if indicator in content_lower:
                return "medium_term"
        
        for indicator in long_term_indicators:
            if indicator in content_lower:
                return "long_term"
        
        return "medium_term"  # Default
    
    def _calculate_move_confidence(self, content: str, application: str) -> float:
        """Calculate confidence in a strategic move assessment."""
        # Simple confidence calculation based on keyword presence and context
        keywords = application.lower().split()
        matches = sum(1 for keyword in keywords if keyword in content.lower())
        base_confidence = matches / len(keywords)
        
        # Adjust based on context quality
        context_indicators = ["strategy", "plan", "approach", "method", "tactic"]
        context_matches = sum(1 for indicator in context_indicators if indicator in content.lower())
        context_bonus = min(context_matches * 0.1, 0.3)
        
        return min(base_confidence + context_bonus, 1.0)
    
    async def _assess_strategic_risks(
        self,
        content: str,
        domain: str,
        strategic_moves: List[StrategicMove]
    ) -> Dict[str, Any]:
        """Assess strategic risks based on identified moves."""
        risk_assessment = {
            "overall_risk_level": "low",
            "risk_factors": [],
            "vulnerabilities": [],
            "threat_actors": [],
            "mitigation_strategies": []
        }
        
        # Assess risk based on strategic moves
        high_impact_moves = [move for move in strategic_moves if move.impact in ["high", "critical"]]
        immediate_moves = [move for move in strategic_moves if move.timeframe == "immediate"]
        
        if len(high_impact_moves) > 2:
            risk_assessment["overall_risk_level"] = "high"
        elif len(high_impact_moves) > 0:
            risk_assessment["overall_risk_level"] = "medium"
        
        if len(immediate_moves) > 0:
            risk_assessment["risk_factors"].append("Immediate strategic moves detected")
        
        # Identify vulnerabilities
        for move in strategic_moves:
            if move.likelihood > 0.7:
                risk_assessment["vulnerabilities"].append(
                    f"High likelihood {move.description}"
                )
        
        # Generate mitigation strategies
        for move in strategic_moves:
            risk_assessment["mitigation_strategies"].extend(move.counter_measures)
        
        return risk_assessment
    
    async def _generate_strategic_recommendations(
        self,
        domain: str,
        principles: List[ArtOfWarPrinciple],
        strategic_moves: List[StrategicMove],
        risk_assessment: Dict[str, Any]
    ) -> List[str]:
        """Generate strategic recommendations based on analysis."""
        recommendations = []
        
        # Domain-specific recommendations
        if domain == "defense":
            recommendations.extend([
                "Enhance intelligence monitoring for strategic deception indicators",
                "Strengthen alliance coordination and information sharing",
                "Develop rapid response capabilities for immediate threats",
                "Maintain strategic ambiguity while building defensive capabilities"
            ])
        elif domain == "intelligence":
            recommendations.extend([
                "Implement multi-source verification protocols",
                "Enhance pattern recognition for deception detection",
                "Strengthen counterintelligence measures",
                "Develop early warning systems for strategic moves"
            ])
        elif domain == "business":
            recommendations.extend([
                "Conduct competitive intelligence analysis",
                "Strengthen strategic partnerships and alliances",
                "Develop contingency plans for market disruptions",
                "Enhance risk management and monitoring systems"
            ])
        elif domain == "cybersecurity":
            recommendations.extend([
                "Implement advanced threat detection systems",
                "Enhance incident response capabilities",
                "Strengthen security monitoring and alerting",
                "Develop cyber deception detection capabilities"
            ])
        
        # Risk-based recommendations
        if risk_assessment["overall_risk_level"] in ["high", "critical"]:
            recommendations.append("Implement immediate risk mitigation measures")
            recommendations.append("Enhance monitoring and alerting systems")
        
        return recommendations
    
    def _calculate_confidence_score(
        self,
        principles: List[ArtOfWarPrinciple],
        strategic_moves: List[StrategicMove],
        risk_assessment: Dict[str, Any]
    ) -> float:
        """Calculate overall confidence score for the analysis."""
        # Base confidence from principles detected
        principle_confidence = min(len(principles) * 0.2, 0.4)
        
        # Confidence from strategic moves
        move_confidence = sum(move.confidence for move in strategic_moves) / max(len(strategic_moves), 1) * 0.4
        
        # Confidence from risk assessment quality
        risk_confidence = 0.2 if risk_assessment["overall_risk_level"] != "low" else 0.1
        
        return min(principle_confidence + move_confidence + risk_confidence, 1.0)
    
    async def get_supported_domains(self) -> List[str]:
        """Get list of supported analysis domains."""
        return [domain.value for domain in DomainType]
    
    async def get_domain_capabilities(self, domain: str) -> Dict[str, Any]:
        """Get capabilities for a specific domain."""
        if domain not in [d.value for d in DomainType]:
            raise ValueError(f"Unsupported domain: {domain}")
        
        return {
            "domain": domain,
            "supported_principles": list(self.art_of_war_principles.keys()),
            "detection_patterns": self.domain_patterns.get(domain, {}),
            "analysis_capabilities": [
                "principle_detection",
                "strategic_move_identification",
                "risk_assessment",
                "recommendation_generation"
            ]
        }
    
    async def get_analysis_history(self, domain: Optional[str] = None) -> List[StrategicAnalysis]:
        """Get analysis history, optionally filtered by domain."""
        if domain:
            return [analysis for analysis in self.analysis_history if analysis.domain == domain]
        return self.analysis_history


# Global instance
enhanced_strategic_analysis_engine = EnhancedStrategicAnalysisEngine()
