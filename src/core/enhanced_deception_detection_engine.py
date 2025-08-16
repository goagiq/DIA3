"""
Enhanced Deception Detection Engine

A comprehensive deception detection system that incorporates:
- Art of War deception principles
- Multi-domain support (defense, intelligence, business, cybersecurity, geopolitical)
- Cultural deception patterns
- Strategic misdirection detection
- Early warning indicators
- Real-time monitoring capabilities
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


class DeceptionDomain(str, Enum):
    """Supported deception detection domains."""
    DEFENSE = "defense"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    CYBERSECURITY = "cybersecurity"
    GEOPOLITICAL = "geopolitical"
    GENERAL = "general"


class DeceptionSeverity(str, Enum):
    """Deception severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DeceptionType(str, Enum):
    """Types of deception indicators."""
    LINGUISTIC = "linguistic"
    STRATEGIC = "strategic"
    CULTURAL = "cultural"
    BEHAVIORAL = "behavioral"
    TEMPORAL = "temporal"
    ART_OF_WAR = "art_of_war"


@dataclass
class DeceptionIndicator:
    """Enhanced deception indicator with domain-specific information."""
    indicator_id: str
    indicator_type: DeceptionType
    domain: DeceptionDomain
    confidence: float
    severity: DeceptionSeverity
    description: str
    evidence: List[str]
    source_text: str
    timestamp: datetime
    art_of_war_technique: Optional[str] = None
    cultural_context: Optional[str] = None
    strategic_implications: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeceptionPattern:
    """Enhanced deception pattern with domain-specific analysis."""
    pattern_id: str
    pattern_type: str
    domain: DeceptionDomain
    indicators: List[DeceptionIndicator]
    confidence: float
    description: str
    first_detected: datetime
    last_detected: datetime
    frequency: int
    art_of_war_techniques: List[str] = field(default_factory=list)
    strategic_implications: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeceptionAnalysisResult:
    """Comprehensive deception analysis result."""
    request_id: str
    domain: DeceptionDomain
    overall_deception_score: float
    severity_level: DeceptionSeverity
    indicators_detected: int
    patterns_detected: int
    critical_alerts: int
    indicators: List[DeceptionIndicator]
    patterns: List[DeceptionPattern]
    art_of_war_techniques_detected: List[str]
    cultural_patterns_detected: List[str]
    strategic_implications: List[str]
    recommendations: List[str]
    early_warning_indicators: List[str]
    analysis_timestamp: datetime
    processing_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class ArtOfWarDeceptionTechniques:
    """Art of War deception techniques and detection patterns."""
    
    TECHNIQUES = {
        "show_inability_when_able": {
            "chinese": "能而示之不能",
            "translation": "Show inability when able",
            "patterns": [
                r"\b(downplay|minimize|reduce|cut back|scale down)\b.*\b(capabilities|abilities|strength|power)\b",
                r"\b(weak|limited|insufficient|inadequate)\b.*\b(resources|capabilities|strength)\b",
                r"\b(cannot|unable|incapable)\b.*\b(achieve|accomplish|complete)\b"
            ],
            "indicators": [
                "Public statements downplaying capabilities",
                "Budget cuts or resource reduction announcements",
                "Withdrawal from international commitments"
            ]
        },
        "show_disuse_when_using": {
            "chinese": "用而示之不用",
            "translation": "Show disuse when using",
            "patterns": [
                r"\b(discontinue|stop|end|terminate)\b.*\b(while|but|however)\b.*\b(continue|maintain|keep)\b",
                r"\b(withdraw|pull out|exit)\b.*\b(unofficial|covert|secret)\b",
                r"\b(deny|disclaim)\b.*\b(involvement|participation|role)\b"
            ],
            "indicators": [
                "Public disengagement while maintaining covert activity",
                "Official withdrawal with continued unofficial involvement",
                "Denial of involvement in ongoing operations"
            ]
        },
        "show_distance_when_near": {
            "chinese": "近而示之遠",
            "translation": "Show distance when near",
            "patterns": [
                r"\b(distant|far|remote)\b.*\b(while|but|however)\b.*\b(close|near|proximate)\b",
                r"\b(uninterested|disinterested)\b.*\b(while|but|however)\b.*\b(involved|engaged)\b",
                r"\b(no involvement|no role|no part)\b.*\b(while|but|however)\b.*\b(active|participating)\b"
            ],
            "indicators": [
                "Claims of distance or disinterest in specific issues",
                "Public focus on unrelated matters",
                "Denial of proximity or involvement"
            ]
        },
        "show_nearness_when_far": {
            "chinese": "遠而示之近",
            "translation": "Show nearness when far",
            "patterns": [
                r"\b(close|near|proximate)\b.*\b(while|but|however)\b.*\b(distant|far|remote)\b",
                r"\b(involved|engaged|participating)\b.*\b(while|but|however)\b.*\b(uninvolved|disengaged)\b",
                r"\b(control|influence|power)\b.*\b(while|but|however)\b.*\b(limited|minimal)\b"
            ],
            "indicators": [
                "Claims of close involvement or control",
                "Public demonstrations of influence or presence",
                "Overstated proximity or capabilities"
            ]
        },
        "lure_with_profit": {
            "chinese": "利而誘之",
            "translation": "Lure with profit",
            "patterns": [
                r"\b(generous|beneficial|advantageous)\b.*\b(offer|proposal|agreement)\b",
                r"\b(too good to be true|exceptional|unprecedented)\b.*\b(deal|opportunity|offer)\b",
                r"\b(hidden|concealed|undisclosed)\b.*\b(conditions|terms|requirements)\b"
            ],
            "indicators": [
                "Overly generous offers or proposals",
                "Economic incentives that seem too good to be true",
                "Trade agreements with hidden conditions"
            ]
        },
        "take_advantage_of_disorder": {
            "chinese": "亂而取之",
            "translation": "Take advantage of disorder",
            "patterns": [
                r"\b(exploit|take advantage|capitalize)\b.*\b(chaos|disorder|confusion)\b",
                r"\b(amplify|exacerbate|intensify)\b.*\b(tensions|conflicts|divisions)\b",
                r"\b(support|back|assist)\b.*\b(opposition|dissent|rebellion)\b"
            ],
            "indicators": [
                "Exploitation of internal divisions or conflicts",
                "Support for opposition groups or dissidents",
                "Amplification of existing tensions"
            ]
        },
        "separate_when_united": {
            "chinese": "親而離之",
            "translation": "Separate when united",
            "patterns": [
                r"\b(divide|split|separate)\b.*\b(alliance|coalition|partnership)\b",
                r"\b(undermine|weaken|erode)\b.*\b(unity|cohesion|solidarity)\b",
                r"\b(bilateral|individual)\b.*\b(deal|agreement)\b.*\b(multilateral|collective)\b"
            ],
            "indicators": [
                "Attempts to break up alliances or coalitions",
                "Bilateral deals that undermine multilateral agreements",
                "Playing allies against each other"
            ]
        },
        "attack_unprepared": {
            "chinese": "攻其無備，出其不意",
            "translation": "Attack unprepared, emerge unexpectedly",
            "patterns": [
                r"\b(sudden|unexpected|surprise)\b.*\b(announcement|change|initiative)\b",
                r"\b(catch off guard|unprepared|unaware)\b",
                r"\b(ultimatum|deadline|demand)\b.*\b(immediate|urgent|critical)\b"
            ],
            "indicators": [
                "Sudden policy announcements or changes",
                "Unexpected diplomatic initiatives",
                "Surprise demands or ultimatums"
            ]
        }
    }


class CulturalDeceptionPatterns:
    """Cultural deception patterns for different regions and languages."""
    
    PATTERNS = {
        "chinese": {
            "harmony_themes": [
                r"\b(和谐|和平|合作|共赢)\b",  # harmony, peace, cooperation, win-win
                r"\b(发展|进步|现代化)\b",     # development, progress, modernization
                r"\b(传统|文化|历史)\b",       # tradition, culture, history
                r"\b(稳定|安全|秩序)\b"        # stability, security, order
            ],
            "strategic_indicators": [
                "Excessive use of harmony terminology",
                "Overemphasis on traditional values",
                "Repetitive development rhetoric",
                "Vague stability claims"
            ]
        },
        "russian": {
            "security_focus": [
                r"\b(безопасность|стабильность|порядок)\b",  # security, stability, order
                r"\b(развитие|прогресс|модернизация)\b",     # development, progress, modernization
                r"\b(традиция|культура|история)\b",          # tradition, culture, history
                r"\b(защита|оборона|сила)\b"                 # protection, defense, strength
            ],
            "strategic_indicators": [
                "Excessive security rhetoric",
                "Overemphasis on protection themes",
                "Repetitive development claims",
                "Vague stability assurances"
            ]
        },
        "arabic": {
            "unity_themes": [
                r"\b(وحدة|سلام|تعاون)\b",  # unity, peace, cooperation
                r"\b(تطور|تقدم|حديث)\b",   # development, progress, modern
                r"\b(تراث|ثقافة|تاريخ)\b",   # heritage, culture, history
                r"\b(استقرار|أمان|نظام)\b"  # stability, security, order
            ],
            "strategic_indicators": [
                "Excessive unity rhetoric",
                "Overemphasis on cultural heritage",
                "Repetitive development themes",
                "Vague stability claims"
            ]
        }
    }


class DomainSpecificPatterns:
    """Domain-specific deception patterns."""
    
    PATTERNS = {
        DeceptionDomain.DEFENSE: {
            "capability_misrepresentation": [
                r"\b(reduce|cut|minimize)\b.*\b(defense|military|weapons)\b",
                r"\b(peaceful|defensive|non-threatening)\b.*\b(while|but)\b.*\b(aggressive|offensive)\b"
            ],
            "strategic_indicators": [
                "Downplaying military capabilities",
                "Emphasizing defensive posture while maintaining offensive capabilities",
                "Public disarmament while secret rearmament"
            ]
        },
        DeceptionDomain.INTELLIGENCE: {
            "information_manipulation": [
                r"\b(transparent|open|honest)\b.*\b(while|but)\b.*\b(secret|classified|hidden)\b",
                r"\b(share|disclose|reveal)\b.*\b(while|but)\b.*\b(conceal|withhold|hide)\b"
            ],
            "strategic_indicators": [
                "Claims of transparency while maintaining secrecy",
                "Selective information sharing",
                "Public disclosure of misleading information"
            ]
        },
        DeceptionDomain.BUSINESS: {
            "financial_misrepresentation": [
                r"\b(profitable|successful|growing)\b.*\b(while|but)\b.*\b(losses|decline|problems)\b",
                r"\b(strong|stable|secure)\b.*\b(while|but)\b.*\b(weak|unstable|risky)\b"
            ],
            "strategic_indicators": [
                "Overstating financial performance",
                "Concealing business problems",
                "Misrepresenting market position"
            ]
        },
        DeceptionDomain.CYBERSECURITY: {
            "threat_misrepresentation": [
                r"\b(secure|protected|safe)\b.*\b(while|but)\b.*\b(vulnerable|exposed|at risk)\b",
                r"\b(no threat|no risk|no concern)\b.*\b(while|but)\b.*\b(active threat|ongoing attack)\b"
            ],
            "strategic_indicators": [
                "Claims of security while vulnerabilities exist",
                "Downplaying cyber threats",
                "Concealing security breaches"
            ]
        },
        DeceptionDomain.GEOPOLITICAL: {
            "intention_misrepresentation": [
                r"\b(peaceful|cooperative|friendly)\b.*\b(while|but)\b.*\b(aggressive|hostile|confrontational)\b",
                r"\b(no intention|no plan|no desire)\b.*\b(while|but)\b.*\b(active planning|preparation)\b"
            ],
            "strategic_indicators": [
                "Claims of peaceful intentions while preparing for conflict",
                "Emphasizing cooperation while pursuing confrontation",
                "Public diplomacy while secret aggression"
            ]
        }
    }


class EnhancedDeceptionDetectionEngine:
    """Enhanced deception detection engine with multi-domain support."""
    
    def __init__(self):
        self.art_of_war_techniques = ArtOfWarDeceptionTechniques()
        self.cultural_patterns = CulturalDeceptionPatterns()
        self.domain_patterns = DomainSpecificPatterns()
        
        # Initialize linguistic patterns
        self.linguistic_patterns = {
            "evasive_language": [
                r"\b(perhaps|maybe|possibly|might|could|seems like|appears to)\b",
                r"\b(not sure|don't know|can't say|hard to tell)\b",
                r"\b(generally|usually|typically|normally)\b",
                r"\b(some|several|many|various|different)\b"
            ],
            "overqualification": [
                r"\b(to be honest|frankly|truthfully|honestly)\b",
                r"\b(I swear|I promise|I assure you)\b",
                r"\b(believe me|trust me|you can trust me)\b"
            ],
            "inconsistent_pronouns": [
                r"\b(we|our|us)\b.*\b(I|me|my)\b",
                r"\b(they|them|their)\b.*\b(we|our|us)\b"
            ],
            "temporal_discrepancies": [
                r"\b(yesterday|today|tomorrow)\b.*\b(last week|next month)\b",
                r"\b(recently|lately)\b.*\b(always|never)\b"
            ]
        }
        
        # Initialize strategic patterns
        self.strategic_patterns = {
            "misdirection": [
                r"\b(focus on|pay attention to|look at)\b.*\b(not|ignore|forget)\b",
                r"\b(important|critical|essential)\b.*\b(but|however|although)\b"
            ],
            "false_urgency": [
                r"\b(immediate|urgent|critical|emergency)\b",
                r"\b(now|right away|asap|immediately)\b",
                r"\b(deadline|time sensitive|expires)\b"
            ],
            "authority_appeal": [
                r"\b(experts say|studies show|research indicates)\b",
                r"\b(officials|authorities|leaders)\b.*\b(confirm|state|announce)\b"
            ],
            "consensus_fallacy": [
                r"\b(everyone knows|nobody believes|all agree)\b",
                r"\b(common sense|obvious|clear)\b"
            ]
        }
        
        logger.info("Enhanced Deception Detection Engine initialized")
    
    @with_error_handling("detect_art_of_war_deception")
    async def detect_art_of_war_deception(self, text: str, language: str = "en") -> List[DeceptionIndicator]:
        """Detect Art of War deception techniques in text."""
        indicators = []
        
        for technique_name, technique_info in self.art_of_war_techniques.TECHNIQUES.items():
            for pattern_str in technique_info["patterns"]:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.finditer(text)
                
                for match in matches:
                    indicator = DeceptionIndicator(
                        indicator_id=str(uuid4()),
                        indicator_type=DeceptionType.ART_OF_WAR,
                        domain=DeceptionDomain.GENERAL,
                        confidence=0.8,
                        severity=DeceptionSeverity.HIGH,
                        description=f"Art of War technique detected: {technique_info['translation']}",
                        evidence=[match.group(0)],
                        source_text=text,
                        timestamp=datetime.now(),
                        art_of_war_technique=technique_name,
                        strategic_implications=technique_info["indicators"],
                        metadata={
                            "technique_chinese": technique_info["chinese"],
                            "technique_translation": technique_info["translation"],
                            "pattern": pattern_str,
                            "match_start": match.start(),
                            "match_end": match.end(),
                            "context": text[max(0, match.start()-50):match.end()+50]
                        }
                    )
                    indicators.append(indicator)
        
        return indicators
    
    @with_error_handling("detect_cultural_deception")
    async def detect_cultural_deception(self, text: str, language: str = "en") -> List[DeceptionIndicator]:
        """Detect cultural deception patterns based on language."""
        indicators = []
        
        if language in self.cultural_patterns.PATTERNS:
            cultural_info = self.cultural_patterns.PATTERNS[language]
            
            for pattern_type, patterns in cultural_info.items():
                if pattern_type == "strategic_indicators":
                    continue
                    
                for pattern_str in patterns:
                    pattern = re.compile(pattern_str)
                    matches = pattern.finditer(text)
                    
                    for match in matches:
                        indicator = DeceptionIndicator(
                            indicator_id=str(uuid4()),
                            indicator_type=DeceptionType.CULTURAL,
                            domain=DeceptionDomain.GENERAL,
                            confidence=0.7,
                            severity=DeceptionSeverity.MEDIUM,
                            description=f"Cultural deception pattern in {language}",
                            evidence=[match.group(0)],
                            source_text=text,
                            timestamp=datetime.now(),
                            cultural_context=language,
                            strategic_implications=cultural_info.get("strategic_indicators", []),
                            metadata={
                                "language": language,
                                "pattern_type": pattern_type,
                                "pattern": pattern_str,
                                "match_start": match.start(),
                                "match_end": match.end(),
                                "context": text[max(0, match.start()-50):match.end()+50]
                            }
                        )
                        indicators.append(indicator)
        
        return indicators
    
    @with_error_handling("detect_domain_specific_deception")
    async def detect_domain_specific_deception(self, text: str, domain: DeceptionDomain) -> List[DeceptionIndicator]:
        """Detect domain-specific deception patterns."""
        indicators = []
        
        if domain in self.domain_patterns.PATTERNS:
            domain_info = self.domain_patterns.PATTERNS[domain]
            
            for pattern_type, patterns in domain_info.items():
                if pattern_type == "strategic_indicators":
                    continue
                    
                for pattern_str in patterns:
                    pattern = re.compile(pattern_str, re.IGNORECASE)
                    matches = pattern.finditer(text)
                    
                    for match in matches:
                        indicator = DeceptionIndicator(
                            indicator_id=str(uuid4()),
                            indicator_type=DeceptionType.STRATEGIC,
                            domain=domain,
                            confidence=0.75,
                            severity=DeceptionSeverity.HIGH,
                            description=f"Domain-specific deception pattern: {pattern_type}",
                            evidence=[match.group(0)],
                            source_text=text,
                            timestamp=datetime.now(),
                            strategic_implications=domain_info.get("strategic_indicators", []),
                            metadata={
                                "domain": domain.value,
                                "pattern_type": pattern_type,
                                "pattern": pattern_str,
                                "match_start": match.start(),
                                "match_end": match.end(),
                                "context": text[max(0, match.start()-50):match.end()+50]
                            }
                        )
                        indicators.append(indicator)
        
        return indicators
    
    @with_error_handling("detect_linguistic_deception")
    async def detect_linguistic_deception(self, text: str) -> List[DeceptionIndicator]:
        """Detect linguistic deception patterns."""
        indicators = []
        
        for pattern_type, patterns in self.linguistic_patterns.items():
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.finditer(text)
                
                for match in matches:
                    indicator = DeceptionIndicator(
                        indicator_id=str(uuid4()),
                        indicator_type=DeceptionType.LINGUISTIC,
                        domain=DeceptionDomain.GENERAL,
                        confidence=0.6,
                        severity=DeceptionSeverity.MEDIUM,
                        description=f"Linguistic deception pattern: {pattern_type}",
                        evidence=[match.group(0)],
                        source_text=text,
                        timestamp=datetime.now(),
                        metadata={
                            "pattern_type": pattern_type,
                            "pattern": pattern_str,
                            "match_start": match.start(),
                            "match_end": match.end(),
                            "context": text[max(0, match.start()-50):match.end()+50]
                        }
                    )
                    indicators.append(indicator)
        
        return indicators
    
    @with_error_handling("detect_strategic_deception")
    async def detect_strategic_deception(self, text: str) -> List[DeceptionIndicator]:
        """Detect strategic deception patterns."""
        indicators = []
        
        for pattern_type, patterns in self.strategic_patterns.items():
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.finditer(text)
                
                for match in matches:
                    indicator = DeceptionIndicator(
                        indicator_id=str(uuid4()),
                        indicator_type=DeceptionType.STRATEGIC,
                        domain=DeceptionDomain.GENERAL,
                        confidence=0.7,
                        severity=DeceptionSeverity.HIGH,
                        description=f"Strategic deception pattern: {pattern_type}",
                        evidence=[match.group(0)],
                        source_text=text,
                        timestamp=datetime.now(),
                        metadata={
                            "pattern_type": pattern_type,
                            "pattern": pattern_str,
                            "match_start": match.start(),
                            "match_end": match.end(),
                            "context": text[max(0, match.start()-50):match.end()+50]
                        }
                    )
                    indicators.append(indicator)
        
        return indicators
    
    @with_error_handling("analyze_deception_comprehensive")
    async def analyze_deception_comprehensive(
        self,
        text: str,
        domain: DeceptionDomain = DeceptionDomain.GENERAL,
        language: str = "en",
        include_art_of_war: bool = True,
        include_cultural: bool = True,
        include_domain_specific: bool = True,
        include_linguistic: bool = True,
        include_strategic: bool = True
    ) -> DeceptionAnalysisResult:
        """Comprehensive deception analysis with all detection methods."""
        start_time = datetime.now()
        
        all_indicators = []
        
        # Detect Art of War deception techniques
        if include_art_of_war:
            art_of_war_indicators = await self.detect_art_of_war_deception(text, language)
            all_indicators.extend(art_of_war_indicators)
        
        # Detect cultural deception patterns
        if include_cultural:
            cultural_indicators = await self.detect_cultural_deception(text, language)
            all_indicators.extend(cultural_indicators)
        
        # Detect domain-specific deception patterns
        if include_domain_specific and domain != DeceptionDomain.GENERAL:
            domain_indicators = await self.detect_domain_specific_deception(text, domain)
            all_indicators.extend(domain_indicators)
        
        # Detect linguistic deception patterns
        if include_linguistic:
            linguistic_indicators = await self.detect_linguistic_deception(text)
            all_indicators.extend(linguistic_indicators)
        
        # Detect strategic deception patterns
        if include_strategic:
            strategic_indicators = await self.detect_strategic_deception(text)
            all_indicators.extend(strategic_indicators)
        
        # Calculate overall deception score
        if all_indicators:
            overall_score = sum(indicator.confidence for indicator in all_indicators) / len(all_indicators)
        else:
            overall_score = 0.0
        
        # Determine severity level
        if overall_score >= 0.9:
            severity_level = DeceptionSeverity.CRITICAL
        elif overall_score >= 0.7:
            severity_level = DeceptionSeverity.HIGH
        elif overall_score >= 0.5:
            severity_level = DeceptionSeverity.MEDIUM
        else:
            severity_level = DeceptionSeverity.LOW
        
        # Count critical alerts
        critical_alerts = len([i for i in all_indicators if i.severity == DeceptionSeverity.CRITICAL])
        
        # Extract Art of War techniques detected
        art_of_war_techniques = list(set([
            i.art_of_war_technique for i in all_indicators 
            if i.art_of_war_technique is not None
        ]))
        
        # Extract cultural patterns detected
        cultural_patterns = list(set([
            i.cultural_context for i in all_indicators 
            if i.cultural_context is not None
        ]))
        
        # Generate strategic implications
        strategic_implications = []
        for indicator in all_indicators:
            if indicator.strategic_implications:
                strategic_implications.extend(indicator.strategic_implications)
        strategic_implications = list(set(strategic_implications))
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_indicators, domain, severity_level)
        
        # Generate early warning indicators
        early_warning_indicators = self._generate_early_warning_indicators(all_indicators, domain)
        
        # Group indicators into patterns
        patterns = self._group_indicators_into_patterns(all_indicators)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        result = DeceptionAnalysisResult(
            request_id=str(uuid4()),
            domain=domain,
            overall_deception_score=overall_score,
            severity_level=severity_level,
            indicators_detected=len(all_indicators),
            patterns_detected=len(patterns),
            critical_alerts=critical_alerts,
            indicators=all_indicators,
            patterns=patterns,
            art_of_war_techniques_detected=art_of_war_techniques,
            cultural_patterns_detected=cultural_patterns,
            strategic_implications=strategic_implications,
            recommendations=recommendations,
            early_warning_indicators=early_warning_indicators,
            analysis_timestamp=datetime.now(),
            processing_time_ms=processing_time
        )
        
        return result
    
    def _generate_recommendations(self, indicators: List[DeceptionIndicator], domain: DeceptionDomain, severity: DeceptionSeverity) -> List[str]:
        """Generate recommendations based on detected deception indicators."""
        recommendations = []
        
        if severity == DeceptionSeverity.CRITICAL:
            recommendations.append("Immediate escalation required - critical deception detected")
            recommendations.append("Initiate emergency response protocols")
            recommendations.append("Notify senior leadership immediately")
        
        if severity == DeceptionSeverity.HIGH:
            recommendations.append("High-level deception detected - increase monitoring")
            recommendations.append("Verify information through multiple sources")
            recommendations.append("Prepare counter-narratives")
        
        # Domain-specific recommendations
        if domain == DeceptionDomain.DEFENSE:
            recommendations.append("Conduct capability verification")
            recommendations.append("Review security posture")
        elif domain == DeceptionDomain.INTELLIGENCE:
            recommendations.append("Cross-reference with intelligence sources")
            recommendations.append("Verify through HUMINT networks")
        elif domain == DeceptionDomain.BUSINESS:
            recommendations.append("Conduct due diligence verification")
            recommendations.append("Review financial statements")
        elif domain == DeceptionDomain.CYBERSECURITY:
            recommendations.append("Conduct security audit")
            recommendations.append("Review threat intelligence")
        elif domain == DeceptionDomain.GEOPOLITICAL:
            recommendations.append("Monitor diplomatic communications")
            recommendations.append("Review international relations")
        
        return recommendations
    
    def _generate_early_warning_indicators(self, indicators: List[DeceptionIndicator], domain: DeceptionDomain) -> List[str]:
        """Generate early warning indicators based on detected deception."""
        early_warning_indicators = []
        
        # Check for Art of War techniques
        art_of_war_count = len([i for i in indicators if i.indicator_type == DeceptionType.ART_OF_WAR])
        if art_of_war_count > 0:
            early_warning_indicators.append(f"Art of War deception techniques detected: {art_of_war_count}")
        
        # Check for cultural patterns
        cultural_count = len([i for i in indicators if i.indicator_type == DeceptionType.CULTURAL])
        if cultural_count > 0:
            early_warning_indicators.append(f"Cultural deception patterns detected: {cultural_count}")
        
        # Check for strategic patterns
        strategic_count = len([i for i in indicators if i.indicator_type == DeceptionType.STRATEGIC])
        if strategic_count > 0:
            early_warning_indicators.append(f"Strategic deception patterns detected: {strategic_count}")
        
        # Domain-specific early warnings
        if domain == DeceptionDomain.DEFENSE:
            early_warning_indicators.append("Monitor for capability misrepresentation")
        elif domain == DeceptionDomain.INTELLIGENCE:
            early_warning_indicators.append("Monitor for information manipulation")
        elif domain == DeceptionDomain.BUSINESS:
            early_warning_indicators.append("Monitor for financial misrepresentation")
        elif domain == DeceptionDomain.CYBERSECURITY:
            early_warning_indicators.append("Monitor for threat misrepresentation")
        elif domain == DeceptionDomain.GEOPOLITICAL:
            early_warning_indicators.append("Monitor for intention misrepresentation")
        
        return early_warning_indicators
    
    def _group_indicators_into_patterns(self, indicators: List[DeceptionIndicator]) -> List[DeceptionPattern]:
        """Group individual indicators into patterns."""
        patterns = []
        
        # Group by indicator type
        type_groups = {}
        for indicator in indicators:
            if indicator.indicator_type not in type_groups:
                type_groups[indicator.indicator_type] = []
            type_groups[indicator.indicator_type].append(indicator)
        
        # Create patterns for each type
        for indicator_type, type_indicators in type_groups.items():
            if len(type_indicators) > 1:
                pattern = DeceptionPattern(
                    pattern_id=str(uuid4()),
                    pattern_type=f"{indicator_type.value}_pattern",
                    domain=type_indicators[0].domain,
                    indicators=type_indicators,
                    confidence=sum(i.confidence for i in type_indicators) / len(type_indicators),
                    description=f"Pattern of {len(type_indicators)} {indicator_type.value} indicators",
                    first_detected=min(i.timestamp for i in type_indicators),
                    last_detected=max(i.timestamp for i in type_indicators),
                    frequency=len(type_indicators),
                    art_of_war_techniques=list(set([
                        i.art_of_war_technique for i in type_indicators 
                        if i.art_of_war_technique is not None
                    ])),
                    strategic_implications=list(set([
                        imp for i in type_indicators 
                        if i.strategic_implications 
                        for imp in i.strategic_implications
                    ]))
                )
                patterns.append(pattern)
        
        return patterns


# Global instance
enhanced_deception_detection_engine = EnhancedDeceptionDetectionEngine()
