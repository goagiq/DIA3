"""
Threat Assessment Agent

Comprehensive threat assessment system with deception detection, warning indicators,
and multi-domain support for defense, intelligence, and business applications.
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

from src.agents.base_agent import StrandsBaseAgent
from src.core.models import AnalysisRequest, AnalysisResult, DataType, SentimentResult, SentimentLabel
from src.core.error_handler import with_error_handling
from src.core.pattern_recognition import AnomalyDetector, PatternClassifier
from src.core.monitoring.alert_system import AlertSystem


class ThreatSeverity(str, Enum):
    """Threat severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatDomain(str, Enum):
    """Supported threat assessment domains."""
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


class ThreatType(str, Enum):
    """Types of threats."""
    DECEPTION = "deception"
    CYBER = "cyber"
    PHYSICAL = "physical"
    ECONOMIC = "economic"
    INFORMATION = "information"
    SOCIAL = "social"
    ENVIRONMENTAL = "environmental"
    GEOPOLITICAL = "geopolitical"


@dataclass
class ThreatIndicator:
    """Represents a detected threat indicator."""
    indicator_id: str
    indicator_type: str
    threat_type: ThreatType
    severity: ThreatSeverity
    confidence: float
    description: str
    evidence: List[str]
    source_text: str
    domain: ThreatDomain
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WarningIndicator:
    """Represents a warning indicator."""
    warning_id: str
    warning_type: str
    severity: ThreatSeverity
    confidence: float
    description: str
    indicators: List[str]
    source_text: str
    domain: ThreatDomain
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeceptionPattern:
    """Represents a deception pattern."""
    pattern_id: str
    pattern_type: str
    severity: ThreatSeverity
    confidence: float
    description: str
    patterns: List[str]
    source_text: str
    domain: ThreatDomain
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class ThreatAssessmentEngine:
    """Core threat assessment engine."""
    
    def __init__(self):
        # Linguistic deception patterns
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
        
        # Strategic deception indicators
        self.strategic_indicators = {
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
        
        # Domain-specific patterns
        self.domain_patterns = {
            ThreatDomain.DEFENSE: {
                "military_terminology": [
                    r"\b(strategic|tactical|operational|deployment)\b",
                    r"\b(capability|readiness|preparedness)\b",
                    r"\b(threat|vulnerability|risk)\b"
                ],
                "security_indicators": [
                    r"\b(breach|intrusion|attack|incident)\b",
                    r"\b(alert|warning|notification)\b",
                    r"\b(monitoring|surveillance|intelligence)\b"
                ]
            },
            ThreatDomain.INTELLIGENCE: {
                "intelligence_terminology": [
                    r"\b(source|asset|agent|handler)\b",
                    r"\b(collection|analysis|dissemination)\b",
                    r"\b(compartment|clearance|classification)\b"
                ],
                "deception_indicators": [
                    r"\b(disinformation|misinformation|propaganda)\b",
                    r"\b(cover|legend|identity)\b",
                    r"\b(surveillance|counterintelligence)\b"
                ]
            },
            ThreatDomain.BUSINESS: {
                "business_terminology": [
                    r"\b(market|competition|strategy|position)\b",
                    r"\b(revenue|profit|loss|growth)\b",
                    r"\b(merger|acquisition|partnership)\b"
                ],
                "risk_indicators": [
                    r"\b(volatility|uncertainty|disruption)\b",
                    r"\b(regulatory|compliance|legal)\b",
                    r"\b(reputation|brand|stakeholder)\b"
                ]
            },
            ThreatDomain.CYBERSECURITY: {
                "cyber_terminology": [
                    r"\b(malware|virus|trojan|ransomware)\b",
                    r"\b(phishing|social engineering|spear phishing)\b",
                    r"\b(breach|data leak|exfiltration)\b"
                ],
                "attack_indicators": [
                    r"\b(exploit|vulnerability|zero-day)\b",
                    r"\b(APT|advanced persistent threat)\b",
                    r"\b(botnet|DDoS|distributed denial of service)\b"
                ]
            }
        }
        
        # Cultural deception patterns
        self.cultural_patterns = {
            "chinese_strategic": [
                r"\b(和谐|和平|合作|共赢)\b",  # harmony, peace, cooperation, win-win
                r"\b(发展|进步|现代化)\b",     # development, progress, modernization
                r"\b(传统|文化|历史)\b",       # tradition, culture, history
                r"\b(稳定|安全|秩序)\b"        # stability, security, order
            ],
            "russian_strategic": [
                r"\b(безопасность|стабильность|порядок)\b",  # security, stability, order
                r"\b(развитие|прогресс|модернизация)\b",     # development, progress, modernization
                r"\b(традиция|культура|история)\b",          # tradition, culture, history
                r"\b(защита|оборона|сила)\b"                 # protection, defense, strength
            ]
        }
    
    def detect_linguistic_deception(self, text: str) -> List[ThreatIndicator]:
        """Detect linguistic deception patterns."""
        indicators = []
        
        for pattern_type, patterns in self.linguistic_patterns.items():
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    indicator = ThreatIndicator(
                        indicator_id=str(uuid4()),
                        indicator_type="linguistic_deception",
                        threat_type=ThreatType.DECEPTION,
                        severity=ThreatSeverity.MEDIUM,
                        confidence=0.7,
                        description=f"Linguistic deception pattern: {pattern_type}",
                        evidence=[match.group(0)],
                        source_text=text,
                        domain=ThreatDomain.INTELLIGENCE,
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
    
    def detect_strategic_deception(self, text: str) -> List[ThreatIndicator]:
        """Detect strategic deception patterns."""
        indicators = []
        
        for pattern_type, patterns in self.strategic_indicators.items():
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    indicator = ThreatIndicator(
                        indicator_id=str(uuid4()),
                        indicator_type="strategic_deception",
                        threat_type=ThreatType.DECEPTION,
                        severity=ThreatSeverity.HIGH,
                        confidence=0.8,
                        description=f"Strategic deception pattern: {pattern_type}",
                        evidence=[match.group(0)],
                        source_text=text,
                        domain=ThreatDomain.INTELLIGENCE,
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
    
    def detect_domain_specific_threats(self, text: str, domain: ThreatDomain) -> List[ThreatIndicator]:
        """Detect domain-specific threat patterns."""
        indicators = []
        
        if domain not in self.domain_patterns:
            return indicators
        
        domain_patterns = self.domain_patterns[domain]
        
        for pattern_type, patterns in domain_patterns.items():
            for pattern_str in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                matches = pattern.finditer(text)
                for match in matches:
                    indicator = ThreatIndicator(
                        indicator_id=str(uuid4()),
                        indicator_type=f"domain_specific_{pattern_type}",
                        threat_type=self._get_threat_type_for_domain(domain),
                        severity=ThreatSeverity.MEDIUM,
                        confidence=0.6,
                        description=f"Domain-specific threat pattern: {pattern_type}",
                        evidence=[match.group(0)],
                        source_text=text,
                        domain=domain,
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
    
    def detect_cultural_deception(self, text: str, language: str = "en") -> List[ThreatIndicator]:
        """Detect cultural deception patterns based on language."""
        indicators = []
        
        if language == "zh":
            patterns = self.cultural_patterns.get("chinese_strategic", [])
        elif language == "ru":
            patterns = self.cultural_patterns.get("russian_strategic", [])
        else:
            return indicators
        
        for pattern_str in patterns:
            pattern = re.compile(pattern_str)
            matches = pattern.finditer(text)
            for match in matches:
                indicator = ThreatIndicator(
                    indicator_id=str(uuid4()),
                    indicator_type="cultural_deception",
                    threat_type=ThreatType.DECEPTION,
                    severity=ThreatSeverity.MEDIUM,
                    confidence=0.6,
                    description=f"Cultural deception pattern in {language}",
                    evidence=[match.group(0)],
                    source_text=text,
                    domain=ThreatDomain.INTELLIGENCE,
                    timestamp=datetime.now(),
                    metadata={
                        "language": language,
                        "pattern": pattern_str,
                        "match_start": match.start(),
                        "match_end": match.end(),
                        "context": text[max(0, match.start()-50):match.end()+50]
                    }
                )
                indicators.append(indicator)
        
        return indicators
    
    def _get_threat_type_for_domain(self, domain: ThreatDomain) -> ThreatType:
        """Get the appropriate threat type for a domain."""
        domain_threat_mapping = {
            ThreatDomain.DEFENSE: ThreatType.PHYSICAL,
            ThreatDomain.INTELLIGENCE: ThreatType.INFORMATION,
            ThreatDomain.BUSINESS: ThreatType.ECONOMIC,
            ThreatDomain.CYBERSECURITY: ThreatType.CYBER,
            ThreatDomain.GEOPOLITICAL: ThreatType.GEOPOLITICAL,
            ThreatDomain.FINANCIAL: ThreatType.ECONOMIC,
            ThreatDomain.HEALTHCARE: ThreatType.SOCIAL,
            ThreatDomain.ENERGY: ThreatType.ENVIRONMENTAL,
            ThreatDomain.TRANSPORTATION: ThreatType.PHYSICAL,
            ThreatDomain.CRITICAL_INFRASTRUCTURE: ThreatType.PHYSICAL
        }
        return domain_threat_mapping.get(domain, ThreatType.INFORMATION)
    
    def generate_warning_indicators(self, indicators: List[ThreatIndicator]) -> List[WarningIndicator]:
        """Generate warning indicators from threat indicators."""
        warnings = []
        
        # Group indicators by type and severity
        indicator_groups = {}
        for indicator in indicators:
            key = (indicator.indicator_type, indicator.severity)
            if key not in indicator_groups:
                indicator_groups[key] = []
            indicator_groups[key].append(indicator)
        
        # Generate warnings for significant patterns
        for (indicator_type, severity), group_indicators in indicator_groups.items():
            if len(group_indicators) >= 2:  # At least 2 indicators of same type
                warning = WarningIndicator(
                    warning_id=str(uuid4()),
                    warning_type=f"pattern_warning_{indicator_type}",
                    severity=severity,
                    confidence=min(0.9, 0.5 + len(group_indicators) * 0.1),
                    description=f"Multiple {indicator_type} indicators detected",
                    indicators=[ind.indicator_id for ind in group_indicators],
                    source_text=group_indicators[0].source_text,
                    domain=group_indicators[0].domain,
                    timestamp=datetime.now(),
                    metadata={
                        "indicator_count": len(group_indicators),
                        "indicator_type": indicator_type,
                        "severity": severity.value
                    }
                )
                warnings.append(warning)
        
        return warnings


class ThreatAssessmentAgent(StrandsBaseAgent):
    """
    Agent for comprehensive threat assessment with deception detection and warning indicators.
    
    Capabilities:
    - Multi-domain threat assessment (defense, intelligence, business, cybersecurity, etc.)
    - Linguistic deception detection
    - Strategic deception identification
    - Cultural deception pattern recognition
    - Domain-specific threat detection
    - Warning indicator generation
    - Real-time threat monitoring
    """
    
    def __init__(self, model_name: Optional[str] = None, **kwargs):
        super().__init__(model_name=model_name or "llama3.2:latest", **kwargs)
        
        # Initialize threat assessment components
        self.threat_engine = ThreatAssessmentEngine()
        self.anomaly_detector = AnomalyDetector()
        self.pattern_classifier = PatternClassifier()
        self.alert_system = AlertSystem()
        
        # Assessment state
        self.detected_indicators: List[ThreatIndicator] = []
        self.warning_indicators: List[WarningIndicator] = []
        self.deception_patterns: List[DeceptionPattern] = []
        self.assessment_active = False
        self.alert_thresholds = {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.7,
            "critical": 0.9
        }
        
        # Set metadata
        self.metadata["agent_type"] = "threat_assessment"
        self.metadata["capabilities"] = [
            "multi_domain_threat_assessment",
            "linguistic_deception_detection",
            "strategic_deception_identification",
            "cultural_deception_recognition",
            "domain_specific_threat_detection",
            "warning_indicator_generation",
            "real_time_threat_monitoring"
        ]
        self.metadata["supported_data_types"] = [
            "text", "communication", "document", "transcript", "report"
        ]
        self.metadata["supported_domains"] = [domain.value for domain in ThreatDomain]
        
        logger.info("ThreatAssessmentAgent initialized successfully")
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        return request.data_type in self.metadata["supported_data_types"]
    
    @with_error_handling("threat_assessment")
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process threat assessment request."""
        logger.info(f"Processing threat assessment request: {request.id}")
        
        # Extract text content
        text_content = self._extract_text_content(request)
        if not text_content:
            # Create a basic sentiment result for the error case
            sentiment_result = SentimentResult(
                label=SentimentLabel.NEUTRAL,
                confidence=0.0,
                scores={"neutral": 0.0},
                reasoning="No text content found in request"
            )
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=sentiment_result,
                processing_time=0.0,
                success=False,
                error_message="No text content found in request"
            )
        
        # Detect threat indicators
        indicators = await self._detect_threat_indicators(text_content, request.metadata)
        
        # Generate warning indicators
        warnings = self.threat_engine.generate_warning_indicators(indicators)
        
        # Analyze patterns
        patterns = await self._analyze_threat_patterns(indicators)
        
        # Generate assessment report
        assessment_report = await self._generate_assessment_report(
            indicators, warnings, patterns, request.metadata
        )
        
        # Store results
        self.detected_indicators.extend(indicators)
        self.warning_indicators.extend(warnings)
        self.deception_patterns.extend(patterns)
        
        # Generate alerts for critical threats
        await self._generate_alerts(indicators, warnings)
        
        # Create a basic sentiment result for the analysis
        sentiment_result = SentimentResult(
            label=SentimentLabel.NEUTRAL,
            confidence=0.5,
            scores={"neutral": 0.5},
            reasoning="Threat assessment analysis completed"
        )
        
        return AnalysisResult(
            request_id=request.id,
            data_type=request.data_type,
            sentiment=sentiment_result,
            processing_time=0.1,  # Placeholder processing time
            success=True,
            result=assessment_report,
            metadata={
                "indicators_count": len(indicators),
                "warnings_count": len(warnings),
                "patterns_count": len(patterns),
                "assessment_timestamp": datetime.now().isoformat()
            }
        )
    
    def _extract_text_content(self, request: AnalysisRequest) -> Optional[str]:
        """Extract text content from request."""
        if request.data_type == DataType.TEXT:
            return request.content
        elif request.data_type == DataType.PDF:
            # Extract text from document
            return request.content
        elif request.data_type == DataType.COMMUNICATION:
            # Extract text from communication
            return request.content
        return None
    
    async def _detect_threat_indicators(self, text: str, metadata: Dict[str, Any]) -> List[ThreatIndicator]:
        """Detect all types of threat indicators in text."""
        indicators = []
        
        # Detect linguistic deception
        linguistic_indicators = self.threat_engine.detect_linguistic_deception(text)
        indicators.extend(linguistic_indicators)
        
        # Detect strategic deception
        strategic_indicators = self.threat_engine.detect_strategic_deception(text)
        indicators.extend(strategic_indicators)
        
        # Detect cultural deception based on language
        language = metadata.get('language', 'en')
        cultural_indicators = self.threat_engine.detect_cultural_deception(text, language)
        indicators.extend(cultural_indicators)
        
        # Detect domain-specific threats
        domain = metadata.get('domain', ThreatDomain.INTELLIGENCE)
        if isinstance(domain, str):
            try:
                domain = ThreatDomain(domain)
            except ValueError:
                domain = ThreatDomain.INTELLIGENCE
        
        domain_indicators = self.threat_engine.detect_domain_specific_threats(text, domain)
        indicators.extend(domain_indicators)
        
        logger.info(f"Detected {len(indicators)} threat indicators")
        return indicators
    
    async def _analyze_threat_patterns(self, indicators: List[ThreatIndicator]) -> List[DeceptionPattern]:
        """Analyze threat patterns from indicators."""
        patterns = []
        
        # Group indicators by type
        indicator_groups = {}
        for indicator in indicators:
            if indicator.indicator_type not in indicator_groups:
                indicator_groups[indicator.indicator_type] = []
            indicator_groups[indicator.indicator_type].append(indicator)
        
        # Create patterns for significant groups
        for indicator_type, group_indicators in indicator_groups.items():
            if len(group_indicators) >= 2:
                pattern = DeceptionPattern(
                    pattern_id=str(uuid4()),
                    pattern_type=indicator_type,
                    severity=max(ind.severity for ind in group_indicators),
                    confidence=min(0.9, 0.5 + len(group_indicators) * 0.1),
                    description=f"Pattern of {indicator_type} indicators",
                    patterns=[ind.indicator_id for ind in group_indicators],
                    source_text=group_indicators[0].source_text,
                    domain=group_indicators[0].domain,
                    timestamp=datetime.now(),
                    metadata={
                        "indicator_count": len(group_indicators),
                        "pattern_type": indicator_type
                    }
                )
                patterns.append(pattern)
        
        return patterns
    
    async def _generate_assessment_report(self, indicators: List[ThreatIndicator], 
                                        warnings: List[WarningIndicator], 
                                        patterns: List[DeceptionPattern],
                                        metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive threat assessment report."""
        
        # Calculate overall threat level
        threat_levels = [ind.severity for ind in indicators]
        overall_severity = self._calculate_overall_severity(threat_levels)
        
        # Group indicators by domain
        domain_indicators = {}
        for indicator in indicators:
            domain = indicator.domain.value
            if domain not in domain_indicators:
                domain_indicators[domain] = []
            domain_indicators[domain].append(indicator)
        
        # Generate report
        report = {
            "assessment_id": str(uuid4()),
            "timestamp": datetime.now().isoformat(),
            "overall_severity": overall_severity.value,
            "confidence": self._calculate_confidence(indicators),
            "summary": {
                "total_indicators": len(indicators),
                "total_warnings": len(warnings),
                "total_patterns": len(patterns),
                "domains_affected": list(domain_indicators.keys())
            },
            "indicators": [
                {
                    "id": ind.indicator_id,
                    "type": ind.indicator_type,
                    "threat_type": ind.threat_type.value,
                    "severity": ind.severity.value,
                    "confidence": ind.confidence,
                    "description": ind.description,
                    "evidence": ind.evidence,
                    "domain": ind.domain.value,
                    "timestamp": ind.timestamp.isoformat()
                }
                for ind in indicators
            ],
            "warnings": [
                {
                    "id": warn.warning_id,
                    "type": warn.warning_type,
                    "severity": warn.severity.value,
                    "confidence": warn.confidence,
                    "description": warn.description,
                    "indicators": warn.indicators,
                    "domain": warn.domain.value,
                    "timestamp": warn.timestamp.isoformat()
                }
                for warn in warnings
            ],
            "patterns": [
                {
                    "id": pattern.pattern_id,
                    "type": pattern.pattern_type,
                    "severity": pattern.severity.value,
                    "confidence": pattern.confidence,
                    "description": pattern.description,
                    "patterns": pattern.patterns,
                    "domain": pattern.domain.value,
                    "timestamp": pattern.timestamp.isoformat()
                }
                for pattern in patterns
            ],
            "domain_analysis": {
                domain: {
                    "indicator_count": len(domain_inds),
                    "severity_distribution": self._get_severity_distribution(domain_inds),
                    "threat_types": list(set(ind.threat_type.value for ind in domain_inds))
                }
                for domain, domain_inds in domain_indicators.items()
            },
            "recommendations": self._generate_recommendations(indicators, warnings, patterns),
            "metadata": metadata
        }
        
        return report
    
    def _calculate_overall_severity(self, severities: List[ThreatSeverity]) -> ThreatSeverity:
        """Calculate overall severity from list of severities."""
        severity_values = {
            ThreatSeverity.LOW: 1,
            ThreatSeverity.MEDIUM: 2,
            ThreatSeverity.HIGH: 3,
            ThreatSeverity.CRITICAL: 4
        }
        
        if not severities:
            return ThreatSeverity.LOW
        
        max_severity_value = max(severity_values[sev] for sev in severities)
        for severity, value in severity_values.items():
            if value == max_severity_value:
                return severity
        
        return ThreatSeverity.LOW
    
    def _calculate_confidence(self, indicators: List[ThreatIndicator]) -> float:
        """Calculate overall confidence from indicators."""
        if not indicators:
            return 0.0
        
        total_confidence = sum(ind.confidence for ind in indicators)
        return total_confidence / len(indicators)
    
    def _get_severity_distribution(self, indicators: List[ThreatIndicator]) -> Dict[str, int]:
        """Get severity distribution for indicators."""
        distribution = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }
        
        for indicator in indicators:
            distribution[indicator.severity.value] += 1
        
        return distribution
    
    def _generate_recommendations(self, indicators: List[ThreatIndicator], 
                                warnings: List[WarningIndicator], 
                                patterns: List[DeceptionPattern]) -> List[str]:
        """Generate recommendations based on assessment results."""
        recommendations = []
        
        # Count indicators by severity
        severity_counts = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }
        
        for indicator in indicators:
            severity_counts[indicator.severity.value] += 1
        
        # Generate recommendations based on findings
        if severity_counts["critical"] > 0:
            recommendations.append("Immediate action required for critical threats")
        
        if severity_counts["high"] > 0:
            recommendations.append("Enhanced monitoring recommended for high-severity threats")
        
        if len(warnings) > 0:
            recommendations.append("Implement warning system for pattern detection")
        
        if len(patterns) > 0:
            recommendations.append("Develop countermeasures for identified threat patterns")
        
        # Domain-specific recommendations
        domains = set(ind.domain for ind in indicators)
        for domain in domains:
            if domain == ThreatDomain.CYBERSECURITY:
                recommendations.append("Implement cybersecurity monitoring and response procedures")
            elif domain == ThreatDomain.BUSINESS:
                recommendations.append("Conduct business risk assessment and mitigation planning")
            elif domain == ThreatDomain.DEFENSE:
                recommendations.append("Enhance defense posture and threat monitoring")
            elif domain == ThreatDomain.INTELLIGENCE:
                recommendations.append("Strengthen intelligence collection and analysis capabilities")
        
        return recommendations
    
    async def _generate_alerts(self, indicators: List[ThreatIndicator], 
                             warnings: List[WarningIndicator]):
        """Generate alerts for critical threats."""
        critical_indicators = [ind for ind in indicators if ind.severity == ThreatSeverity.CRITICAL]
        critical_warnings = [warn for warn in warnings if warn.severity == ThreatSeverity.CRITICAL]
        
        if critical_indicators or critical_warnings:
            alert_message = f"Critical threats detected: {len(critical_indicators)} indicators, {len(critical_warnings)} warnings"
            await self.alert_system.send_alert(alert_message, "critical")
    
    async def get_assessment_summary(self) -> Dict[str, Any]:
        """Get summary of all assessments."""
        return {
            "total_indicators": len(self.detected_indicators),
            "total_warnings": len(self.warning_indicators),
            "total_patterns": len(self.deception_patterns),
            "domains_covered": list(set(ind.domain.value for ind in self.detected_indicators)),
            "severity_distribution": self._get_severity_distribution(self.detected_indicators),
            "last_assessment": max(ind.timestamp for ind in self.detected_indicators).isoformat() if self.detected_indicators else None
        }
    
    async def clear_assessment_data(self):
        """Clear all assessment data."""
        self.detected_indicators.clear()
        self.warning_indicators.clear()
        self.deception_patterns.clear()
        logger.info("Threat assessment data cleared")
