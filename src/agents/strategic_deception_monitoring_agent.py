"""
Strategic Deception Monitoring Agent

This agent monitors communications for strategic deception indicators including:
- Linguistic deception patterns
- Behavioral inconsistency detection
- Strategic misdirection identification
- Cultural deception indicators
- Temporal deception patterns
- Cross-source consistency analysis
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from uuid import uuid4
from dataclasses import dataclass, field

from loguru import logger

from src.agents.base_agent import StrandsBaseAgent
from src.core.models import AnalysisRequest, AnalysisResult, DataType, SentimentResult, SentimentLabel
from src.core.error_handler import with_error_handling
from src.core.pattern_recognition import AnomalyDetector, PatternClassifier
from src.core.monitoring.alert_system import AlertSystem


@dataclass
class DeceptionIndicator:
    """Represents a detected deception indicator."""
    indicator_id: str
    indicator_type: str  # linguistic, behavioral, strategic, cultural, temporal
    confidence: float
    severity: str  # low, medium, high, critical
    description: str
    evidence: List[str]
    source_text: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeceptionPattern:
    """Represents a pattern of deception indicators."""
    pattern_id: str
    pattern_type: str
    indicators: List[DeceptionIndicator]
    confidence: float
    description: str
    first_detected: datetime
    last_detected: datetime
    frequency: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class StrategicDeceptionMonitor:
    """Core deception monitoring engine."""
    
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
        
        # Behavioral inconsistency patterns
        self.behavioral_patterns = {
            "emotional_inconsistency": [
                r"\b(calm|peaceful|happy)\b.*\b(angry|furious|outraged)\b",
                r"\b(confident|sure|certain)\b.*\b(unsure|doubtful|hesitant)\b"
            ],
            "commitment_inconsistency": [
                r"\b(commit|promise|guarantee)\b.*\b(maybe|perhaps|possibly)\b",
                r"\b(always|never|forever)\b.*\b(sometimes|occasionally|rarely)\b"
            ]
        }
        
        # Initialize pattern detection
        self.compiled_patterns = self._compile_patterns()
        
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile all regex patterns for efficient matching."""
        compiled = {}
        for category, patterns in self.linguistic_patterns.items():
            compiled[category] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for category, patterns in self.strategic_indicators.items():
            compiled[category] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for category, patterns in self.behavioral_patterns.items():
            compiled[category] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        return compiled
    
    def detect_linguistic_deception(self, text: str) -> List[DeceptionIndicator]:
        """Detect linguistic deception patterns in text."""
        indicators = []
        
        for pattern_type, patterns in self.compiled_patterns.items():
            if pattern_type in self.linguistic_patterns:
                for pattern in patterns:
                    matches = pattern.finditer(text)
                    for match in matches:
                        indicator = DeceptionIndicator(
                            indicator_id=str(uuid4()),
                            indicator_type="linguistic",
                            confidence=0.7,
                            severity="medium",
                            description=f"Linguistic deception pattern: {pattern_type}",
                            evidence=[match.group(0)],
                            source_text=text,
                            timestamp=datetime.now(),
                            metadata={
                                "pattern_type": pattern_type,
                                "match_start": match.start(),
                                "match_end": match.end(),
                                "context": text[max(0, match.start()-50):match.end()+50]
                            }
                        )
                        indicators.append(indicator)
        
        return indicators
    
    def detect_strategic_deception(self, text: str) -> List[DeceptionIndicator]:
        """Detect strategic deception indicators in text."""
        indicators = []
        
        for pattern_type, patterns in self.compiled_patterns.items():
            if pattern_type in self.strategic_indicators:
                for pattern in patterns:
                    matches = pattern.finditer(text)
                    for match in matches:
                        indicator = DeceptionIndicator(
                            indicator_id=str(uuid4()),
                            indicator_type="strategic",
                            confidence=0.8,
                            severity="high",
                            description=f"Strategic deception indicator: {pattern_type}",
                            evidence=[match.group(0)],
                            source_text=text,
                            timestamp=datetime.now(),
                            metadata={
                                "pattern_type": pattern_type,
                                "match_start": match.start(),
                                "match_end": match.end(),
                                "context": text[max(0, match.start()-100):match.end()+100]
                            }
                        )
                        indicators.append(indicator)
        
        return indicators
    
    def detect_cultural_deception(self, text: str, language: str = "en") -> List[DeceptionIndicator]:
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
                indicator = DeceptionIndicator(
                    indicator_id=str(uuid4()),
                    indicator_type="cultural",
                    confidence=0.6,
                    severity="medium",
                    description=f"Cultural deception pattern in {language}",
                    evidence=[match.group(0)],
                    source_text=text,
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


class StrategicDeceptionMonitoringAgent(StrandsBaseAgent):
    """
    Agent for monitoring strategic deception indicators in communications.
    
    Capabilities:
    - Linguistic deception detection
    - Strategic misdirection identification
    - Cultural deception pattern recognition
    - Behavioral inconsistency analysis
    - Cross-source consistency checking
    - Real-time alert generation
    """
    
    def __init__(self, model_name: Optional[str] = None, **kwargs):
        super().__init__(model_name=model_name or "llama3.2:latest", **kwargs)
        
        # Initialize deception monitoring components
        self.deception_monitor = StrategicDeceptionMonitor()
        self.anomaly_detector = AnomalyDetector()
        self.pattern_classifier = PatternClassifier()
        self.alert_system = AlertSystem()
        
        # Monitoring state
        self.detected_indicators: List[DeceptionIndicator] = []
        self.deception_patterns: List[DeceptionPattern] = []
        self.monitoring_active = False
        self.alert_thresholds = {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.7,
            "critical": 0.9
        }
        
        # Set metadata
        self.metadata["agent_type"] = "strategic_deception_monitoring"
        self.metadata["capabilities"] = [
            "linguistic_deception_detection",
            "strategic_deception_identification",
            "cultural_deception_recognition",
            "behavioral_inconsistency_analysis",
            "cross_source_consistency_checking",
            "real_time_alert_generation"
        ]
        self.metadata["supported_data_types"] = [
            "text", "communication", "document", "transcript"
        ]
        
        logger.info("StrategicDeceptionMonitoringAgent initialized successfully")
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        return request.data_type in [
            DataType.TEXT, 
            DataType.GENERAL
        ]
    
    @with_error_handling("strategic_deception_monitoring")
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process strategic deception monitoring requests."""
        try:
            start_time = datetime.now()
            
            # Extract text content
            if isinstance(request.data, str):
                text_content = request.data
            elif isinstance(request.data, dict):
                text_content = request.data.get('text', '')
            else:
                text_content = str(request.data)
            
            # Detect deception indicators
            indicators = await self._detect_deception_indicators(text_content, request.metadata)
            
            # Analyze patterns
            patterns = await self._analyze_deception_patterns(indicators)
            
            # Generate alerts if needed
            alerts = await self._generate_alerts(indicators, patterns)
            
            # Calculate overall deception score
            deception_score = self._calculate_deception_score(indicators, patterns)
            
            # Determine sentiment based on deception level
            if deception_score > self.alert_thresholds["critical"]:
                sentiment_label = SentimentLabel.NEGATIVE
                confidence = deception_score
                reasoning = f"Critical deception indicators detected (score: {deception_score:.2f})"
            elif deception_score > self.alert_thresholds["high"]:
                sentiment_label = SentimentLabel.NEGATIVE
                confidence = deception_score
                reasoning = f"High deception indicators detected (score: {deception_score:.2f})"
            elif deception_score > self.alert_thresholds["medium"]:
                sentiment_label = SentimentLabel.NEUTRAL
                confidence = deception_score
                reasoning = f"Medium deception indicators detected (score: {deception_score:.2f})"
            else:
                sentiment_label = SentimentLabel.POSITIVE
                confidence = 1.0 - deception_score
                reasoning = f"Low deception indicators detected (score: {deception_score:.2f})"
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AnalysisResult(
                id=str(uuid4()),
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label=sentiment_label,
                    confidence=confidence,
                    reasoning=reasoning
                ),
                processing_time=processing_time,
                status="completed",
                metadata={
                    'deception_score': deception_score,
                    'indicators_detected': len(indicators),
                    'patterns_identified': len(patterns),
                    'alerts_generated': len(alerts),
                    'agent_type': self.agent_type,
                    'indicators': [ind.__dict__ for ind in indicators],
                    'patterns': [pat.__dict__ for pat in patterns],
                    'timestamp': datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error in strategic deception monitoring: {e}")
            return AnalysisResult(
                id=str(uuid4()),
                request_id=request.id,
                data_type=request.data_type,
                sentiment=SentimentResult(
                    label=SentimentLabel.UNCERTAIN,
                    confidence=0.0,
                    reasoning=f"Error in deception monitoring: {str(e)}"
                ),
                processing_time=0.0,
                status="failed"
            )
    
    async def _detect_deception_indicators(self, text: str, metadata: Dict[str, Any]) -> List[DeceptionIndicator]:
        """Detect all types of deception indicators in text."""
        indicators = []
        
        # Detect linguistic deception
        linguistic_indicators = self.deception_monitor.detect_linguistic_deception(text)
        indicators.extend(linguistic_indicators)
        
        # Detect strategic deception
        strategic_indicators = self.deception_monitor.detect_strategic_deception(text)
        indicators.extend(strategic_indicators)
        
        # Detect cultural deception based on language
        language = metadata.get('language', 'en')
        cultural_indicators = self.deception_monitor.detect_cultural_deception(text, language)
        indicators.extend(cultural_indicators)
        
        # Store detected indicators
        self.detected_indicators.extend(indicators)
        
        logger.info(f"Detected {len(indicators)} deception indicators")
        return indicators
    
    async def _analyze_deception_patterns(self, indicators: List[DeceptionIndicator]) -> List[DeceptionPattern]:
        """Analyze deception indicators to identify patterns."""
        patterns = []
        
        # Group indicators by type
        indicator_groups = {}
        for indicator in indicators:
            if indicator.indicator_type not in indicator_groups:
                indicator_groups[indicator.indicator_type] = []
            indicator_groups[indicator.indicator_type].append(indicator)
        
        # Create patterns for each group
        for indicator_type, group_indicators in indicator_groups.items():
            if len(group_indicators) >= 2:  # Need at least 2 indicators for a pattern
                pattern = DeceptionPattern(
                    pattern_id=str(uuid4()),
                    pattern_type=indicator_type,
                    indicators=group_indicators,
                    confidence=sum(ind.confidence for ind in group_indicators) / len(group_indicators),
                    description=f"Pattern of {indicator_type} deception indicators",
                    first_detected=min(ind.timestamp for ind in group_indicators),
                    last_detected=max(ind.timestamp for ind in group_indicators),
                    frequency=len(group_indicators)
                )
                patterns.append(pattern)
        
        # Store patterns
        self.deception_patterns.extend(patterns)
        
        logger.info(f"Identified {len(patterns)} deception patterns")
        return patterns
    
    async def _generate_alerts(self, indicators: List[DeceptionIndicator], patterns: List[DeceptionPattern]) -> List[str]:
        """Generate alerts for significant deception indicators."""
        alerts = []
        
        # Check for critical indicators
        critical_indicators = [ind for ind in indicators if ind.severity == "critical"]
        if critical_indicators:
            alert_id = str(uuid4())
            await self.alert_system.generate_alert(
                alert_id=alert_id,
                alert_type="strategic_deception",
                severity="critical",
                message="Critical strategic deception indicators detected",
                decision_id="deception_monitoring",
                metric_name="deception_indicators",
                current_value=len(critical_indicators),
                threshold_value=1,
                notification_channels=["email", "slack"]
            )
            alerts.append(alert_id)
        
        # Check for high confidence patterns
        high_confidence_patterns = [pat for pat in patterns if pat.confidence > 0.8]
        if high_confidence_patterns:
            alert_id = str(uuid4())
            await self.alert_system.generate_alert(
                alert_id=alert_id,
                alert_type="deception_pattern",
                severity="high",
                message="High-confidence deception patterns identified",
                decision_id="deception_monitoring",
                metric_name="deception_patterns",
                current_value=len(high_confidence_patterns),
                threshold_value=1,
                notification_channels=["email"]
            )
            alerts.append(alert_id)
        
        logger.info(f"Generated {len(alerts)} alerts")
        return alerts
    
    def _calculate_deception_score(self, indicators: List[DeceptionIndicator], patterns: List[DeceptionPattern]) -> float:
        """Calculate overall deception score based on indicators and patterns."""
        if not indicators and not patterns:
            return 0.0
        
        # Weight indicators by severity
        severity_weights = {
            "low": 0.1,
            "medium": 0.3,
            "high": 0.6,
            "critical": 1.0
        }
        
        indicator_score = sum(
            ind.confidence * severity_weights.get(ind.severity, 0.1)
            for ind in indicators
        )
        
        # Weight patterns by confidence
        pattern_score = sum(pat.confidence for pat in patterns)
        
        # Normalize scores
        total_score = (indicator_score + pattern_score) / (len(indicators) + len(patterns) + 1)
        
        return min(total_score, 1.0)  # Cap at 1.0
    
    async def start_monitoring(self):
        """Start continuous deception monitoring."""
        if self.monitoring_active:
            logger.warning("Deception monitoring is already active")
            return
        
        self.monitoring_active = True
        logger.info("Strategic deception monitoring started")
    
    async def stop_monitoring(self):
        """Stop continuous deception monitoring."""
        if not self.monitoring_active:
            return
        
        self.monitoring_active = False
        logger.info("Strategic deception monitoring stopped")
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get summary of current monitoring status."""
        return {
            "monitoring_active": self.monitoring_active,
            "total_indicators_detected": len(self.detected_indicators),
            "total_patterns_identified": len(self.deception_patterns),
            "recent_indicators": [
                ind.__dict__ for ind in self.detected_indicators[-10:]  # Last 10 indicators
            ],
            "recent_patterns": [
                pat.__dict__ for pat in self.deception_patterns[-5:]  # Last 5 patterns
            ],
            "alert_thresholds": self.alert_thresholds,
            "timestamp": datetime.now().isoformat()
        }
