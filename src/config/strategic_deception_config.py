"""
Strategic Deception Monitoring Configuration

Comprehensive configuration for strategic deception monitoring system including:
- Pattern definitions
- Threshold settings
- Alert configurations
- Language-specific patterns
- Cultural indicators
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum


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


@dataclass
class PatternConfig:
    """Configuration for a deception pattern."""
    pattern_id: str
    pattern_type: str
    regex_patterns: List[str]
    confidence: float
    severity: DeceptionSeverity
    description: str
    examples: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThresholdConfig:
    """Configuration for deception thresholds."""
    low_threshold: float = 0.3
    medium_threshold: float = 0.5
    high_threshold: float = 0.7
    critical_threshold: float = 0.9
    
    # Pattern-specific thresholds
    linguistic_threshold: float = 0.6
    strategic_threshold: float = 0.8
    cultural_threshold: float = 0.7
    behavioral_threshold: float = 0.6


@dataclass
class AlertConfig:
    """Configuration for alert generation."""
    enable_alerts: bool = True
    alert_channels: List[str] = field(default_factory=lambda: ["email", "slack"])
    alert_retention_days: int = 30
    critical_alert_threshold: int = 1
    high_alert_threshold: int = 3
    medium_alert_threshold: int = 5
    
    # Alert message templates
    alert_templates: Dict[str, str] = field(default_factory=lambda: {
        "critical": "🚨 CRITICAL: {count} critical deception indicators detected in {source}",
        "high": "⚠️ HIGH: {count} high-confidence deception patterns identified in {source}",
        "medium": "📊 MEDIUM: {count} medium-level deception indicators found in {source}",
        "low": "ℹ️ LOW: {count} low-level deception indicators detected in {source}"
    })


@dataclass
class DashboardConfig:
    """Configuration for the monitoring dashboard."""
    update_interval: int = 30  # seconds
    metric_history_size: int = 1000
    alert_history_size: int = 500
    trend_analysis_window: int = 24  # hours
    
    # Dashboard metrics
    default_metrics: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "deception_score": {
            "name": "Overall Deception Score",
            "unit": "score",
            "threshold": 0.7,
            "description": "Aggregate deception score across all indicators"
        },
        "indicators_per_hour": {
            "name": "Deception Indicators per Hour",
            "unit": "count",
            "threshold": 10,
            "description": "Number of deception indicators detected per hour"
        },
        "critical_alerts": {
            "name": "Critical Alerts",
            "unit": "count",
            "threshold": 5,
            "description": "Number of critical deception alerts"
        },
        "pattern_confidence": {
            "name": "Pattern Confidence",
            "unit": "percentage",
            "threshold": 80,
            "description": "Average confidence of detected deception patterns"
        },
        "response_time": {
            "name": "Response Time",
            "unit": "seconds",
            "threshold": 5,
            "description": "Average response time for deception detection"
        }
    })


class StrategicDeceptionConfig:
    """Main configuration class for strategic deception monitoring."""
    
    def __init__(self):
        # Initialize configuration components
        self.thresholds = ThresholdConfig()
        self.alerts = AlertConfig()
        self.dashboard = DashboardConfig()
        
        # Initialize pattern configurations
        self.linguistic_patterns = self._initialize_linguistic_patterns()
        self.strategic_patterns = self._initialize_strategic_patterns()
        self.cultural_patterns = self._initialize_cultural_patterns()
        self.behavioral_patterns = self._initialize_behavioral_patterns()
        
        # Language-specific configurations
        self.language_configs = self._initialize_language_configs()
        
        # Performance configurations
        self.performance_config = {
            "max_text_length": 10000,
            "batch_size": 100,
            "timeout_seconds": 30,
            "enable_caching": True,
            "cache_ttl": 3600  # 1 hour
        }
    
    def _initialize_linguistic_patterns(self) -> Dict[str, PatternConfig]:
        """Initialize linguistic deception patterns."""
        return {
            "evasive_language": PatternConfig(
                pattern_id="evasive_language",
                pattern_type=DeceptionType.LINGUISTIC,
                regex_patterns=[
                    r"\b(perhaps|maybe|possibly|might|could|seems like|appears to)\b",
                    r"\b(not sure|don't know|can't say|hard to tell)\b",
                    r"\b(generally|usually|typically|normally)\b",
                    r"\b(some|several|many|various|different)\b"
                ],
                confidence=0.7,
                severity=DeceptionSeverity.MEDIUM,
                description="Evasive or non-committal language patterns",
                examples=[
                    "Perhaps we might consider maybe looking at some options",
                    "I'm not sure, but it seems like this could be the case"
                ]
            ),
            "overqualification": PatternConfig(
                pattern_id="overqualification",
                pattern_type=DeceptionType.LINGUISTIC,
                regex_patterns=[
                    r"\b(to be honest|frankly|truthfully|honestly)\b",
                    r"\b(I swear|I promise|I assure you)\b",
                    r"\b(believe me|trust me|you can trust me)\b"
                ],
                confidence=0.8,
                severity=DeceptionSeverity.HIGH,
                description="Excessive qualification suggesting deception",
                examples=[
                    "To be honest, I swear I'm telling you the truth",
                    "Believe me, you can trust me on this"
                ]
            ),
            "inconsistent_pronouns": PatternConfig(
                pattern_id="inconsistent_pronouns",
                pattern_type=DeceptionType.LINGUISTIC,
                regex_patterns=[
                    r"\b(we|our|us)\b.*\b(I|me|my)\b",
                    r"\b(they|them|their)\b.*\b(we|our|us)\b"
                ],
                confidence=0.6,
                severity=DeceptionSeverity.MEDIUM,
                description="Inconsistent use of pronouns suggesting deception",
                examples=[
                    "We are committed to this, but I have concerns",
                    "They said we should proceed, but our team disagrees"
                ]
            ),
            "temporal_discrepancies": PatternConfig(
                pattern_id="temporal_discrepancies",
                pattern_type=DeceptionType.LINGUISTIC,
                regex_patterns=[
                    r"\b(yesterday|today|tomorrow)\b.*\b(last week|next month)\b",
                    r"\b(recently|lately)\b.*\b(always|never)\b"
                ],
                confidence=0.7,
                severity=DeceptionSeverity.MEDIUM,
                description="Temporal inconsistencies in statements",
                examples=[
                    "We recently started this, but we've always been committed",
                    "Yesterday we decided, but last week we planned differently"
                ]
            )
        }
    
    def _initialize_strategic_patterns(self) -> Dict[str, PatternConfig]:
        """Initialize strategic deception patterns."""
        return {
            "misdirection": PatternConfig(
                pattern_id="misdirection",
                pattern_type=DeceptionType.STRATEGIC,
                regex_patterns=[
                    r"\b(focus on|pay attention to|look at)\b.*\b(not|ignore|forget)\b",
                    r"\b(important|critical|essential)\b.*\b(but|however|although)\b"
                ],
                confidence=0.8,
                severity=DeceptionSeverity.HIGH,
                description="Strategic misdirection attempts",
                examples=[
                    "Focus on the benefits, not the risks",
                    "This is important but we shouldn't worry about the details"
                ]
            ),
            "false_urgency": PatternConfig(
                pattern_id="false_urgency",
                pattern_type=DeceptionType.STRATEGIC,
                regex_patterns=[
                    r"\b(immediate|urgent|critical|emergency)\b",
                    r"\b(now|right away|asap|immediately)\b",
                    r"\b(deadline|time sensitive|expires)\b"
                ],
                confidence=0.7,
                severity=DeceptionSeverity.MEDIUM,
                description="False urgency to pressure decisions",
                examples=[
                    "This is an immediate emergency requiring urgent action",
                    "The deadline expires tomorrow, we must act now"
                ]
            ),
            "authority_appeal": PatternConfig(
                pattern_id="authority_appeal",
                pattern_type=DeceptionType.STRATEGIC,
                regex_patterns=[
                    r"\b(experts say|studies show|research indicates)\b",
                    r"\b(officials|authorities|leaders)\b.*\b(confirm|state|announce)\b"
                ],
                confidence=0.6,
                severity=DeceptionSeverity.MEDIUM,
                description="Appeal to authority without specific sources",
                examples=[
                    "Experts say this is the best approach",
                    "Authorities confirm this is the right decision"
                ]
            ),
            "consensus_fallacy": PatternConfig(
                pattern_id="consensus_fallacy",
                pattern_type=DeceptionType.STRATEGIC,
                regex_patterns=[
                    r"\b(everyone knows|nobody believes|all agree)\b",
                    r"\b(common sense|obvious|clear)\b"
                ],
                confidence=0.7,
                severity=DeceptionSeverity.MEDIUM,
                description="False consensus or appeal to common sense",
                examples=[
                    "Everyone knows this is the obvious solution",
                    "It's common sense that nobody believes the alternative"
                ]
            )
        }
    
    def _initialize_cultural_patterns(self) -> Dict[str, PatternConfig]:
        """Initialize cultural deception patterns."""
        return {
            "chinese_strategic": PatternConfig(
                pattern_id="chinese_strategic",
                pattern_type=DeceptionType.CULTURAL,
                regex_patterns=[
                    r"\b(和谐|和平|合作|共赢)\b",  # harmony, peace, cooperation, win-win
                    r"\b(发展|进步|现代化)\b",     # development, progress, modernization
                    r"\b(传统|文化|历史)\b",       # tradition, culture, history
                    r"\b(稳定|安全|秩序)\b"        # stability, security, order
                ],
                confidence=0.6,
                severity=DeceptionSeverity.MEDIUM,
                description="Chinese strategic cultural deception patterns",
                examples=[
                    "我们致力于和谐发展，促进和平合作",
                    "传统上我们重视文化传承，维护稳定安全秩序"
                ],
                metadata={"language": "zh", "culture": "chinese"}
            ),
            "russian_strategic": PatternConfig(
                pattern_id="russian_strategic",
                pattern_type=DeceptionType.CULTURAL,
                regex_patterns=[
                    r"\b(безопасность|стабильность|порядок)\b",  # security, stability, order
                    r"\b(развитие|прогресс|модернизация)\b",     # development, progress, modernization
                    r"\b(традиция|культура|история)\b",          # tradition, culture, history
                    r"\b(защита|оборона|сила)\b"                 # protection, defense, strength
                ],
                confidence=0.6,
                severity=DeceptionSeverity.MEDIUM,
                description="Russian strategic cultural deception patterns",
                examples=[
                    "Мы стремимся к безопасности и стабильности",
                    "Развитие и прогресс модернизации важны для защиты"
                ],
                metadata={"language": "ru", "culture": "russian"}
            )
        }
    
    def _initialize_behavioral_patterns(self) -> Dict[str, PatternConfig]:
        """Initialize behavioral inconsistency patterns."""
        return {
            "emotional_inconsistency": PatternConfig(
                pattern_id="emotional_inconsistency",
                pattern_type=DeceptionType.BEHAVIORAL,
                regex_patterns=[
                    r"\b(calm|peaceful|happy)\b.*\b(angry|furious|outraged)\b",
                    r"\b(confident|sure|certain)\b.*\b(unsure|doubtful|hesitant)\b"
                ],
                confidence=0.7,
                severity=DeceptionSeverity.MEDIUM,
                description="Inconsistent emotional states",
                examples=[
                    "I'm completely calm about this, but I'm absolutely furious",
                    "I'm confident in our approach, but I'm unsure about the details"
                ]
            ),
            "commitment_inconsistency": PatternConfig(
                pattern_id="commitment_inconsistency",
                pattern_type=DeceptionType.BEHAVIORAL,
                regex_patterns=[
                    r"\b(commit|promise|guarantee)\b.*\b(maybe|perhaps|possibly)\b",
                    r"\b(always|never|forever)\b.*\b(sometimes|occasionally|rarely)\b"
                ],
                confidence=0.8,
                severity=DeceptionSeverity.HIGH,
                description="Inconsistent commitment levels",
                examples=[
                    "I promise to always support this, but maybe we should consider alternatives",
                    "We never compromise on quality, but sometimes we make exceptions"
                ]
            )
        }
    
    def _initialize_language_configs(self) -> Dict[str, Dict[str, Any]]:
        """Initialize language-specific configurations."""
        return {
            "en": {
                "patterns": ["linguistic", "strategic", "behavioral"],
                "confidence_multiplier": 1.0,
                "severity_adjustment": 0.0
            },
            "zh": {
                "patterns": ["linguistic", "strategic", "behavioral", "cultural"],
                "confidence_multiplier": 1.1,
                "severity_adjustment": 0.1,
                "cultural_patterns": ["chinese_strategic"]
            },
            "ru": {
                "patterns": ["linguistic", "strategic", "behavioral", "cultural"],
                "confidence_multiplier": 1.1,
                "severity_adjustment": 0.1,
                "cultural_patterns": ["russian_strategic"]
            },
            "ar": {
                "patterns": ["linguistic", "strategic", "behavioral"],
                "confidence_multiplier": 1.0,
                "severity_adjustment": 0.0
            },
            "es": {
                "patterns": ["linguistic", "strategic", "behavioral"],
                "confidence_multiplier": 1.0,
                "severity_adjustment": 0.0
            }
        }
    
    def get_patterns_for_language(self, language: str) -> Dict[str, PatternConfig]:
        """Get patterns applicable for a specific language."""
        language_config = self.language_configs.get(language, self.language_configs["en"])
        applicable_patterns = {}
        
        for pattern_type in language_config["patterns"]:
            if pattern_type == "linguistic":
                applicable_patterns.update(self.linguistic_patterns)
            elif pattern_type == "strategic":
                applicable_patterns.update(self.strategic_patterns)
            elif pattern_type == "behavioral":
                applicable_patterns.update(self.behavioral_patterns)
            elif pattern_type == "cultural":
                cultural_patterns = language_config.get("cultural_patterns", [])
                for pattern_id in cultural_patterns:
                    if pattern_id in self.cultural_patterns:
                        applicable_patterns[pattern_id] = self.cultural_patterns[pattern_id]
        
        return applicable_patterns
    
    def get_threshold_for_severity(self, severity: DeceptionSeverity) -> float:
        """Get threshold value for a severity level."""
        severity_thresholds = {
            DeceptionSeverity.LOW: self.thresholds.low_threshold,
            DeceptionSeverity.MEDIUM: self.thresholds.medium_threshold,
            DeceptionSeverity.HIGH: self.thresholds.high_threshold,
            DeceptionSeverity.CRITICAL: self.thresholds.critical_threshold
        }
        return severity_thresholds.get(severity, self.thresholds.medium_threshold)
    
    def get_alert_config(self) -> AlertConfig:
        """Get alert configuration."""
        return self.alerts
    
    def get_dashboard_config(self) -> DashboardConfig:
        """Get dashboard configuration."""
        return self.dashboard
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance configuration."""
        return self.performance_config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "thresholds": {
                "low_threshold": self.thresholds.low_threshold,
                "medium_threshold": self.thresholds.medium_threshold,
                "high_threshold": self.thresholds.high_threshold,
                "critical_threshold": self.thresholds.critical_threshold
            },
            "alerts": {
                "enable_alerts": self.alerts.enable_alerts,
                "alert_channels": self.alerts.alert_channels,
                "alert_retention_days": self.alerts.alert_retention_days
            },
            "dashboard": {
                "update_interval": self.dashboard.update_interval,
                "metric_history_size": self.dashboard.metric_history_size,
                "alert_history_size": self.dashboard.alert_history_size
            },
            "performance": self.performance_config,
            "languages": list(self.language_configs.keys()),
            "pattern_types": [pattern_type.value for pattern_type in DeceptionType]
        }


# Global configuration instance
strategic_deception_config = StrategicDeceptionConfig()
