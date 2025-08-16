"""
Strategic Deception Monitoring API Routes

Provides comprehensive strategic deception monitoring capabilities for:
- Defense and intelligence applications
- Business intelligence and competitive analysis
- Multi-domain threat assessment
- Real-time deception detection
- Early warning systems
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from loguru import logger

from src.core.orchestrator import SentimentOrchestrator
from src.core.models import AnalysisRequest, DataType
from src.agents.strategic_deception_monitoring_agent import (
    StrategicDeceptionMonitoringAgent,
    DeceptionIndicator,
    DeceptionPattern
)

# Initialize router
router = APIRouter(prefix="/strategic-deception", tags=["Strategic Deception Monitoring"])

# Global orchestrator reference
orchestrator: Optional[SentimentOrchestrator] = None

# Request/Response models
class DeceptionMonitoringRequest(BaseModel):
    """Request model for deception monitoring."""
    content: str = Field(..., description="Text content to analyze for deception")
    domain: str = Field(default="general", description="Domain: defense, intelligence, business, cybersecurity, geopolitical")
    language: str = Field(default="en", description="Language code")
    monitoring_level: str = Field(default="standard", description="Monitoring level: basic, standard, comprehensive, critical")
    include_cultural_analysis: bool = Field(default=True, description="Include cultural deception patterns")
    include_behavioral_analysis: bool = Field(default=True, description="Include behavioral inconsistency analysis")
    include_strategic_analysis: bool = Field(default=True, description="Include strategic deception analysis")
    alert_threshold: float = Field(default=0.7, description="Alert threshold (0.0-1.0)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class DeceptionIndicatorResponse(BaseModel):
    """Response model for deception indicators."""
    indicator_id: str
    indicator_type: str
    confidence: float
    severity: str
    description: str
    evidence: List[str]
    source_text: str
    timestamp: datetime
    domain: str
    metadata: Dict[str, Any]

class DeceptionPatternResponse(BaseModel):
    """Response model for deception patterns."""
    pattern_id: str
    pattern_type: str
    indicators: List[DeceptionIndicatorResponse]
    confidence: float
    description: str
    first_detected: datetime
    last_detected: datetime
    frequency: int
    domain: str
    metadata: Dict[str, Any]

class DeceptionMonitoringResponse(BaseModel):
    """Response model for deception monitoring."""
    request_id: str
    domain: str
    overall_deception_score: float
    severity_level: str
    indicators_detected: int
    patterns_detected: int
    critical_alerts: int
    indicators: List[DeceptionIndicatorResponse]
    patterns: List[DeceptionPatternResponse]
    recommendations: List[str]
    analysis_timestamp: datetime
    processing_time_ms: float

class BatchDeceptionMonitoringRequest(BaseModel):
    """Request model for batch deception monitoring."""
    contents: List[str] = Field(..., description="List of text contents to analyze")
    domain: str = Field(default="general", description="Domain for analysis")
    language: str = Field(default="en", description="Language code")
    monitoring_level: str = Field(default="standard", description="Monitoring level")
    parallel_processing: bool = Field(default=True, description="Enable parallel processing")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class BatchDeceptionMonitoringResponse(BaseModel):
    """Response model for batch deception monitoring."""
    batch_id: str
    total_requests: int
    processed_requests: int
    failed_requests: int
    overall_deception_score: float
    critical_alerts: int
    high_severity_alerts: int
    results: List[DeceptionMonitoringResponse]
    batch_timestamp: datetime
    processing_time_ms: float

class DeceptionDashboardRequest(BaseModel):
    """Request model for deception dashboard data."""
    domain: Optional[str] = Field(default=None, description="Filter by domain")
    time_range_hours: int = Field(default=24, description="Time range in hours")
    severity_filter: Optional[str] = Field(default=None, description="Filter by severity")
    include_patterns: bool = Field(default=True, description="Include pattern analysis")

class DeceptionDashboardResponse(BaseModel):
    """Response model for deception dashboard data."""
    dashboard_id: str
    time_range: Dict[str, datetime]
    total_indicators: int
    total_patterns: int
    severity_distribution: Dict[str, int]
    domain_distribution: Dict[str, int]
    top_indicators: List[DeceptionIndicatorResponse]
    top_patterns: List[DeceptionPatternResponse]
    trend_analysis: Dict[str, Any]
    alert_summary: Dict[str, int]
    last_updated: datetime

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check for strategic deception monitoring service."""
    try:
        return {
            "status": "healthy",
            "service": "strategic_deception_monitoring",
            "timestamp": datetime.now(),
            "capabilities": [
                "linguistic_deception_detection",
                "strategic_deception_identification", 
                "cultural_deception_recognition",
                "behavioral_inconsistency_analysis",
                "cross_source_consistency_checking",
                "real_time_alert_generation",
                "multi_domain_support"
            ],
            "supported_domains": [
                "defense", "intelligence", "business", 
                "cybersecurity", "geopolitical", "general"
            ],
            "supported_languages": ["en", "zh", "ru", "ar", "es", "fr", "de", "ja", "ko"]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")

# Single content deception monitoring
@router.post("/monitor", response_model=DeceptionMonitoringResponse)
async def monitor_deception(request: DeceptionMonitoringRequest):
    """Monitor single content for strategic deception indicators."""
    try:
        start_time = datetime.now()
        
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # Create analysis request
        analysis_request = AnalysisRequest(
            content=request.content,
            data_type=DataType.TEXT,
            metadata={
                "domain": request.domain,
                "language": request.language,
                "monitoring_level": request.monitoring_level,
                "include_cultural_analysis": request.include_cultural_analysis,
                "include_behavioral_analysis": request.include_behavioral_analysis,
                "include_strategic_analysis": request.include_strategic_analysis,
                "alert_threshold": request.alert_threshold,
                **(request.metadata or {})
            }
        )
        
        # Process with strategic deception monitoring agent
        result = await orchestrator.analyze(analysis_request)
        
        # Extract deception indicators and patterns
        indicators = []
        patterns = []
        overall_score = 0.0
        critical_alerts = 0
        
        if hasattr(result, 'deception_indicators'):
            indicators = result.deception_indicators
            for indicator in indicators:
                if indicator.severity == "critical":
                    critical_alerts += 1
                overall_score = max(overall_score, indicator.confidence)
        
        if hasattr(result, 'deception_patterns'):
            patterns = result.deception_patterns
        
        # Determine severity level
        severity_level = "low"
        if overall_score >= 0.9:
            severity_level = "critical"
        elif overall_score >= 0.7:
            severity_level = "high"
        elif overall_score >= 0.5:
            severity_level = "medium"
        
        # Generate recommendations
        recommendations = _generate_recommendations(indicators, patterns, request.domain)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return DeceptionMonitoringResponse(
            request_id=str(result.request_id) if hasattr(result, 'request_id') else "unknown",
            domain=request.domain,
            overall_deception_score=overall_score,
            severity_level=severity_level,
            indicators_detected=len(indicators),
            patterns_detected=len(patterns),
            critical_alerts=critical_alerts,
            indicators=[_convert_indicator_to_response(i, request.domain) for i in indicators],
            patterns=[_convert_pattern_to_response(p, request.domain) for p in patterns],
            recommendations=recommendations,
            analysis_timestamp=datetime.now(),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Deception monitoring failed: {e}")
        raise HTTPException(status_code=500, detail=f"Deception monitoring failed: {e}")

# Batch deception monitoring
@router.post("/monitor-batch", response_model=BatchDeceptionMonitoringResponse)
async def monitor_deception_batch(request: BatchDeceptionMonitoringRequest):
    """Monitor multiple contents for strategic deception indicators."""
    try:
        start_time = datetime.now()
        
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        results = []
        failed_requests = 0
        critical_alerts = 0
        high_severity_alerts = 0
        overall_scores = []
        
        # Process requests
        for content in request.contents:
            try:
                analysis_request = AnalysisRequest(
                    content=content,
                    data_type=DataType.TEXT,
                    metadata={
                        "domain": request.domain,
                        "language": request.language,
                        "monitoring_level": request.monitoring_level,
                        "batch_processing": True,
                        **(request.metadata or {})
                    }
                )
                
                result = await orchestrator.analyze(analysis_request)
                
                # Extract deception data
                indicators = getattr(result, 'deception_indicators', [])
                patterns = getattr(result, 'deception_patterns', [])
                overall_score = max([i.confidence for i in indicators], default=0.0)
                
                # Count alerts
                for indicator in indicators:
                    if indicator.severity == "critical":
                        critical_alerts += 1
                    elif indicator.severity == "high":
                        high_severity_alerts += 1
                
                overall_scores.append(overall_score)
                
                # Convert to response format
                response = DeceptionMonitoringResponse(
                    request_id=str(getattr(result, 'request_id', 'unknown')),
                    domain=request.domain,
                    overall_deception_score=overall_score,
                    severity_level=_get_severity_level(overall_score),
                    indicators_detected=len(indicators),
                    patterns_detected=len(patterns),
                    critical_alerts=sum(1 for i in indicators if i.severity == "critical"),
                    indicators=[_convert_indicator_to_response(i, request.domain) for i in indicators],
                    patterns=[_convert_pattern_to_response(p, request.domain) for p in patterns],
                    recommendations=_generate_recommendations(indicators, patterns, request.domain),
                    analysis_timestamp=datetime.now(),
                    processing_time_ms=0.0
                )
                
                results.append(response)
                
            except Exception as e:
                logger.error(f"Failed to process content in batch: {e}")
                failed_requests += 1
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        overall_deception_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
        
        return BatchDeceptionMonitoringResponse(
            batch_id=f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            total_requests=len(request.contents),
            processed_requests=len(results),
            failed_requests=failed_requests,
            overall_deception_score=overall_deception_score,
            critical_alerts=critical_alerts,
            high_severity_alerts=high_severity_alerts,
            results=results,
            batch_timestamp=datetime.now(),
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Batch deception monitoring failed: {e}")
        raise HTTPException(status_code=500, detail=f"Batch deception monitoring failed: {e}")

# Dashboard data endpoint
@router.post("/dashboard", response_model=DeceptionDashboardResponse)
async def get_deception_dashboard(request: DeceptionDashboardRequest):
    """Get deception monitoring dashboard data."""
    try:
        # This would typically query a database or cache for historical data
        # For now, return mock data structure
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=request.time_range_hours)
        
        return DeceptionDashboardResponse(
            dashboard_id=f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            time_range={"start": start_time, "end": end_time},
            total_indicators=0,  # Would be populated from database
            total_patterns=0,    # Would be populated from database
            severity_distribution={"low": 0, "medium": 0, "high": 0, "critical": 0},
            domain_distribution={"defense": 0, "intelligence": 0, "business": 0, "cybersecurity": 0, "geopolitical": 0},
            top_indicators=[],   # Would be populated from database
            top_patterns=[],     # Would be populated from database
            trend_analysis={},   # Would be populated from database
            alert_summary={"critical": 0, "high": 0, "medium": 0, "low": 0},
            last_updated=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Dashboard data retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard data retrieval failed: {e}")

# Domain-specific endpoints
@router.post("/defense/monitor", response_model=DeceptionMonitoringResponse)
async def monitor_defense_deception(request: DeceptionMonitoringRequest):
    """Monitor deception specifically for defense domain."""
    request.domain = "defense"
    return await monitor_deception(request)

@router.post("/intelligence/monitor", response_model=DeceptionMonitoringResponse)
async def monitor_intelligence_deception(request: DeceptionMonitoringRequest):
    """Monitor deception specifically for intelligence domain."""
    request.domain = "intelligence"
    return await monitor_deception(request)

@router.post("/business/monitor", response_model=DeceptionMonitoringResponse)
async def monitor_business_deception(request: DeceptionMonitoringRequest):
    """Monitor deception specifically for business domain."""
    request.domain = "business"
    return await monitor_deception(request)

@router.post("/cybersecurity/monitor", response_model=DeceptionMonitoringResponse)
async def monitor_cybersecurity_deception(request: DeceptionMonitoringRequest):
    """Monitor deception specifically for cybersecurity domain."""
    request.domain = "cybersecurity"
    return await monitor_deception(request)

@router.post("/geopolitical/monitor", response_model=DeceptionMonitoringResponse)
async def monitor_geopolitical_deception(request: DeceptionMonitoringRequest):
    """Monitor deception specifically for geopolitical domain."""
    request.domain = "geopolitical"
    return await monitor_deception(request)

# Utility functions
def _convert_indicator_to_response(indicator: DeceptionIndicator, domain: str) -> DeceptionIndicatorResponse:
    """Convert DeceptionIndicator to DeceptionIndicatorResponse."""
    return DeceptionIndicatorResponse(
        indicator_id=indicator.indicator_id,
        indicator_type=indicator.indicator_type,
        confidence=indicator.confidence,
        severity=indicator.severity,
        description=indicator.description,
        evidence=indicator.evidence,
        source_text=indicator.source_text,
        timestamp=indicator.timestamp,
        domain=domain,
        metadata=indicator.metadata
    )

def _convert_pattern_to_response(pattern: DeceptionPattern, domain: str) -> DeceptionPatternResponse:
    """Convert DeceptionPattern to DeceptionPatternResponse."""
    return DeceptionPatternResponse(
        pattern_id=pattern.pattern_id,
        pattern_type=pattern.pattern_type,
        indicators=[_convert_indicator_to_response(i, domain) for i in pattern.indicators],
        confidence=pattern.confidence,
        description=pattern.description,
        first_detected=pattern.first_detected,
        last_detected=pattern.last_detected,
        frequency=pattern.frequency,
        domain=domain,
        metadata=pattern.metadata
    )

def _get_severity_level(score: float) -> str:
    """Get severity level from deception score."""
    if score >= 0.9:
        return "critical"
    elif score >= 0.7:
        return "high"
    elif score >= 0.5:
        return "medium"
    else:
        return "low"

def _generate_recommendations(indicators: List[DeceptionIndicator], patterns: List[DeceptionPattern], domain: str) -> List[str]:
    """Generate recommendations based on detected deception indicators."""
    recommendations = []
    
    if not indicators:
        recommendations.append("No deception indicators detected. Continue monitoring for changes in communication patterns.")
        return recommendations
    
    # Count indicators by type
    indicator_counts = {}
    for indicator in indicators:
        indicator_counts[indicator.indicator_type] = indicator_counts.get(indicator.indicator_type, 0) + 1
    
    # Generate domain-specific recommendations
    if domain == "defense":
        if indicator_counts.get("strategic", 0) > 0:
            recommendations.append("Strategic deception detected. Increase intelligence gathering and cross-source verification.")
        if indicator_counts.get("cultural", 0) > 0:
            recommendations.append("Cultural deception patterns identified. Engage cultural intelligence specialists.")
    
    elif domain == "intelligence":
        if indicator_counts.get("linguistic", 0) > 0:
            recommendations.append("Linguistic deception indicators present. Conduct detailed communication analysis.")
        if indicator_counts.get("behavioral", 0) > 0:
            recommendations.append("Behavioral inconsistencies detected. Review source reliability and motivations.")
    
    elif domain == "business":
        if indicator_counts.get("strategic", 0) > 0:
            recommendations.append("Strategic misdirection detected. Review competitive intelligence and market analysis.")
        if indicator_counts.get("false_urgency", 0) > 0:
            recommendations.append("False urgency indicators present. Verify deadlines and pressure tactics.")
    
    elif domain == "cybersecurity":
        if indicator_counts.get("authority_appeal", 0) > 0:
            recommendations.append("Authority appeal deception detected. Verify source authenticity and credentials.")
        if indicator_counts.get("consensus_fallacy", 0) > 0:
            recommendations.append("Consensus fallacy indicators present. Conduct independent verification.")
    
    # General recommendations
    if any(i.severity == "critical" for i in indicators):
        recommendations.append("Critical deception indicators detected. Immediate investigation required.")
    
    if len(patterns) > 0:
        recommendations.append(f"Deception patterns identified. Monitor for recurring indicators and coordinate response.")
    
    recommendations.append("Maintain continuous monitoring and update threat assessments based on findings.")
    
    return recommendations

# Function to set orchestrator reference
def set_orchestrator(orch: SentimentOrchestrator):
    """Set the orchestrator reference for the routes."""
    global orchestrator
    orchestrator = orch
