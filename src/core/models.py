"""
Core data models for the sentiment analysis system.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class SentimentLabel(str, Enum):
    """Sentiment classification labels."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"
    UNCERTAIN = "uncertain"
    DUPLICATE = "duplicate"  # For duplicate detection results


class ProcessingStatus(str, Enum):
    """Processing status for analysis requests."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DataType(str, Enum):
    """Supported data types for analysis."""
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    WEBPAGE = "webpage"
    PDF = "pdf"
    DOCUMENT = "document"  # Generic document type
    COMMUNICATION = "communication"  # Communication data
    REPORT = "report"  # Report data
    API_RESPONSE = "api_response"
    SOCIAL_MEDIA = "social_media"
    DATABASE = "database"
    API = "api"
    MARKET_DATA = "market_data"
    FINANCIAL = "financial"
    GENERAL = "general"
    TIME_SERIES = "time_series"
    NUMERICAL = "numerical"


class ModelType(str, Enum):
    """Supported model types."""
    OLLAMA = "ollama"
    # Removed unused model types: HUGGINGFACE, OPENAI, ANTHROPIC


class ModelCapability(str, Enum):
    """Model capabilities."""
    TEXT = "text"
    VISION = "vision"
    AUDIO = "audio"
    TOOL_CALLING = "tool_calling"
    MULTIMODAL = "multimodal"


class ModelConfig(BaseModel):
    """Configuration for a specific model."""
    model_id: str
    model_type: ModelType
    capabilities: List[ModelCapability]
    host: Optional[str] = "http://localhost:11434"  # Default Ollama host
    api_key: Optional[str] = None  # Not needed for Ollama
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    vision_temperature: Optional[float] = None
    vision_max_tokens: Optional[int] = None
    keep_alive: Optional[str] = "5m"  # Ollama keep_alive parameter
    top_p: Optional[float] = None  # Ollama top_p parameter
    stop_sequences: Optional[List[str]] = None  # Ollama stop sequences
    options: Optional[Dict[str, Any]] = None  # Additional Ollama options
    is_default: bool = False


class PageData(BaseModel):
    """Structured data for a single page."""
    page_number: int
    content: str
    content_length: int
    extraction_method: str  # "pypdf2", "vision_ocr", etc.
    confidence: float = Field(ge=0.0, le=1.0)
    processing_time: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AnalysisRequest(BaseModel):
    """Request for sentiment analysis."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    data_type: DataType
    content: Union[str, bytes, Dict[str, Any]]
    language: str = "en"
    model_preference: Optional[str] = None  # Specific model to use
    # Enable reflection for quality improvement
    reflection_enabled: bool = True
    max_iterations: int = 3  # Maximum reflection iterations
    confidence_threshold: float = 0.8  # Minimum confidence threshold
    # Force reprocessing even if duplicate detected
    force_reprocess: bool = False
    # Enable analytics capabilities
    enable_analytics: bool = False
    # Additional metadata for processing
    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


class SentimentResult(BaseModel):
    """Result of sentiment analysis."""
    label: SentimentLabel
    confidence: float = Field(ge=0.0, le=1.0)
    scores: Dict[str, float] = Field(default_factory=dict)
    reasoning: Optional[str] = None
    context_notes: Optional[str] = None
    uncertainty_factors: Optional[List[str]] = None
    reflection_notes: Optional[List[str]] = None
    iteration_count: int = 1


class AnalysisResult(BaseModel):
    """Result of analysis."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    request_id: str
    data_type: DataType
    sentiment: SentimentResult
    processing_time: float
    status: Optional[str] = None
    raw_content: Optional[str] = None
    extracted_text: Optional[str] = None
    # Structured page data for PDFs
    pages: Optional[List[PageData]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_used: Optional[str] = None
    reflection_enabled: bool = True
    quality_score: Optional[float] = None
    success: bool = True  # Indicates if the analysis was successful
    error_message: Optional[str] = None  # Error message if analysis failed


class ModelRegistry(BaseModel):
    """Registry of available models."""
    models: Dict[str, ModelConfig] = Field(default_factory=dict)
    default_models: Dict[DataType, str] = Field(default_factory=dict)
    
    def get_model(self, model_id: str) -> Optional[ModelConfig]:
        """Get a model by ID."""
        return self.models.get(model_id)
    
    def get_default_model(self, data_type: DataType) -> Optional[ModelConfig]:
        """Get the default model for a data type."""
        model_id = self.default_models.get(data_type)
        if model_id:
            return self.models.get(model_id)
        return None
    
    def register_model(self, model: ModelConfig):
        """Register a new model."""
        self.models[model.model_id] = model
        if model.is_default:
            # Set as default for all supported capabilities
            for capability in model.capabilities:
                if capability in [ModelCapability.VISION, ModelCapability.AUDIO]:
                    if capability == ModelCapability.VISION:
                        self.default_models[DataType.IMAGE] = model.model_id
                        self.default_models[DataType.VIDEO] = model.model_id
                    elif capability == ModelCapability.AUDIO:
                        self.default_models[DataType.AUDIO] = model.model_id


class ReflectionResult(BaseModel):
    """Result of agent reflection."""
    iteration: int
    confidence: float
    reasoning: str
    alternative_hypotheses: List[str] = Field(default_factory=list)
    validation_checks: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    final_assessment: bool = False


# Enhanced Report Generation Models
class ReportComponent(str, Enum):
    """Available report components."""
    EXECUTIVE_SUMMARY = "executive_summary"
    COMPARATIVE_ANALYSIS = "comparative_analysis"
    IMPACT_ANALYSIS = "impact_analysis"
    OPERATIONAL_CHANGES = "operational_changes"
    PREDICTIVE_ANALYSIS = "predictive_analysis"
    FORECASTING = "forecasting"
    STRESS_TESTING = "stress_testing"
    RECOMMENDATIONS = "recommendations"
    INTERACTIVE_VISUALIZATIONS = "interactive_visualizations"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    MERMAID_DIAGRAMS = "mermaid_diagrams"
    CAPTCHA = "captcha"
    RISK_ASSESSMENT = "risk_assessment"
    ANOMALY_DETECTION = "anomaly_detection"
    PATTERN_ANALYSIS = "pattern_analysis"
    POLICY_IMPACT = "policy_impact"
    CROSS_REFERENCE = "cross_reference"
    GEOPOLITICAL_MAPPING = "geopolitical_mapping"
    STRATEGIC_VULNERABILITIES = "strategic_vulnerabilities"
    COOPERATION_OPPORTUNITIES = "cooperation_opportunities"
    COMPETITION_INTENSITY = "competition_intensity"
    STRATEGIC_METRICS = "strategic_metrics"
    MONTE_CARLO_SIMULATION = "monte_carlo_simulation"


class StressTestScenario(str, Enum):
    """Stress testing scenarios."""
    WORST_CASE = "worst_case"
    AVERAGE_CASE = "average_case"
    BEST_CASE = "best_case"


class MonteCarloConfig(BaseModel):
    """Configuration for Monte Carlo simulations."""
    iterations: int = Field(default=10000, ge=1000, le=100000)
    confidence_level: float = Field(
        default=0.95, ge=0.8, le=0.99
    )
    time_horizon: int = Field(default=12, description="Months")
    variables: List[str] = Field(default_factory=list)
    distributions: Dict[str, str] = Field(default_factory=dict)
    correlations: Optional[Dict[str, Dict[str, float]]] = None


class StressTestConfig(BaseModel):
    """Configuration for stress testing."""
    scenarios: List[StressTestScenario] = Field(default_factory=list)
    severity_levels: List[str] = Field(default_factory=lambda: ["low", "medium", "high", "extreme"])
    time_periods: List[int] = Field(default_factory=lambda: [1, 3, 6, 12, 24])
    variables: List[str] = Field(default_factory=list)


class VisualizationConfig(BaseModel):
    """Configuration for visualizations."""
    chart_types: List[str] = Field(default_factory=lambda: ["line", "bar", "scatter", "heatmap", "radar"])
    interactive: bool = True
    drill_down_enabled: bool = True
    real_time_updates: bool = False
    export_formats: List[str] = Field(default_factory=lambda: ["png", "svg", "pdf"])


class KnowledgeGraphConfig(BaseModel):
    """Configuration for knowledge graph analysis."""
    max_nodes: int = Field(default=1000, ge=100, le=10000)
    max_relationships: int = Field(default=5000, ge=500, le=50000)
    include_metadata: bool = True
    relationship_types: List[str] = Field(default_factory=list)
    node_types: List[str] = Field(default_factory=list)


class EnhancedReportRequest(BaseModel):
    """Request for enhanced report generation."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    query: str
    data_sources: List[str] = Field(default_factory=list)
    components: List[ReportComponent] = Field(default_factory=list)
    monte_carlo_config: Optional[MonteCarloConfig] = None
    stress_test_config: Optional[StressTestConfig] = None
    visualization_config: Optional[VisualizationConfig] = None
    knowledge_graph_config: Optional[KnowledgeGraphConfig] = None
    include_historical_data: bool = True
    include_forecasts: bool = True
    export_formats: List[str] = Field(default_factory=lambda: ["pdf", "excel", "word"])
    language: str = "en"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutiveSummary(BaseModel):
    """Executive summary component."""
    key_findings: List[str] = Field(default_factory=list)
    critical_insights: List[str] = Field(default_factory=list)
    strategic_recommendations: List[str] = Field(default_factory=list)
    risk_level: str = Field(default="medium")
    confidence_score: float = Field(ge=0.0, le=1.0)
    generated_at: str = Field(default_factory=lambda: str(uuid4()))


class ComparativeAnalysis(BaseModel):
    """Comparative analysis component."""
    baseline_metrics: Dict[str, float] = Field(default_factory=dict)
    comparison_metrics: Dict[str, float] = Field(default_factory=dict)
    differences: Dict[str, float] = Field(default_factory=dict)
    percentage_changes: Dict[str, float] = Field(default_factory=dict)
    significance_tests: Dict[str, bool] = Field(default_factory=dict)
    insights: List[str] = Field(default_factory=list)


class ImpactAnalysis(BaseModel):
    """Impact analysis component."""
    direct_impacts: List[str] = Field(default_factory=list)
    indirect_impacts: List[str] = Field(default_factory=list)
    cascading_effects: List[str] = Field(default_factory=list)
    impact_scores: Dict[str, float] = Field(default_factory=dict)
    timeframes: Dict[str, str] = Field(default_factory=dict)
    stakeholders_affected: List[str] = Field(default_factory=list)


class OperationalChanges(BaseModel):
    """Operational changes component."""
    recommended_changes: List[str] = Field(default_factory=list)
    implementation_timeline: Dict[str, str] = Field(default_factory=dict)
    resource_requirements: Dict[str, Any] = Field(default_factory=dict)
    risk_assessments: Dict[str, str] = Field(default_factory=dict)
    success_metrics: List[str] = Field(default_factory=list)


class PredictiveAnalysis(BaseModel):
    """Predictive analysis component."""
    historical_trends: Dict[str, List[float]] = Field(default_factory=dict)
    forecast_values: Dict[str, List[float]] = Field(default_factory=dict)
    confidence_intervals: Dict[str, List[float]] = Field(default_factory=dict)
    model_accuracy: Dict[str, float] = Field(default_factory=dict)
    key_drivers: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class MonteCarloResult(BaseModel):
    """Monte Carlo simulation results."""
    scenario_name: str
    iterations: int
    mean_value: float
    median_value: float
    standard_deviation: float
    confidence_intervals: Dict[str, float] = Field(default_factory=dict)
    percentiles: Dict[str, float] = Field(default_factory=dict)
    risk_metrics: Dict[str, float] = Field(default_factory=dict)
    convergence_analysis: Dict[str, Any] = Field(default_factory=dict)


class StressTestResult(BaseModel):
    """Stress testing results."""
    scenario: StressTestScenario
    severity_level: str
    time_period: int
    impact_scores: Dict[str, float] = Field(default_factory=dict)
    vulnerability_analysis: Dict[str, str] = Field(default_factory=dict)
    mitigation_strategies: List[str] = Field(default_factory=list)
    recovery_time_estimates: Dict[str, int] = Field(default_factory=dict)


class RiskAssessmentMatrix(BaseModel):
    """Risk assessment matrix."""
    risk_categories: List[str] = Field(default_factory=list)
    likelihood_scores: Dict[str, float] = Field(default_factory=dict)
    impact_scores: Dict[str, float] = Field(default_factory=dict)
    risk_scores: Dict[str, float] = Field(default_factory=dict)
    risk_levels: Dict[str, str] = Field(default_factory=dict)
    mitigation_priorities: List[str] = Field(default_factory=list)


class KnowledgeGraphResult(BaseModel):
    """Knowledge graph analysis results."""
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    relationships: List[Dict[str, Any]] = Field(default_factory=list)
    communities: List[List[str]] = Field(default_factory=list)
    centrality_scores: Dict[str, float] = Field(default_factory=dict)
    key_entities: List[str] = Field(default_factory=list)
    relationship_patterns: List[str] = Field(default_factory=list)


class VisualizationResult(BaseModel):
    """Interactive visualization results."""
    chart_data: Dict[str, Any] = Field(default_factory=dict)
    drill_down_options: List[str] = Field(default_factory=list)
    interactive_features: List[str] = Field(default_factory=list)
    export_urls: Dict[str, str] = Field(default_factory=dict)
    mermaid_diagrams: List[str] = Field(default_factory=list)


class EnhancedReportResult(BaseModel):
    """Enhanced report generation result."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    request_id: str
    status: ProcessingStatus
    executive_summary: Optional[ExecutiveSummary] = None
    comparative_analysis: Optional[ComparativeAnalysis] = None
    impact_analysis: Optional[ImpactAnalysis] = None
    operational_changes: Optional[OperationalChanges] = None
    predictive_analysis: Optional[PredictiveAnalysis] = None
    monte_carlo_results: List[MonteCarloResult] = Field(default_factory=list)
    stress_test_results: List[StressTestResult] = Field(default_factory=list)
    risk_assessment_matrix: Optional[RiskAssessmentMatrix] = None
    knowledge_graph_result: Optional[KnowledgeGraphResult] = None
    visualization_result: Optional[VisualizationResult] = None
    processing_time: float
    components_generated: List[ReportComponent] = Field(default_factory=list)
    export_urls: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    success: bool = True
