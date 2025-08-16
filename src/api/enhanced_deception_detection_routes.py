"""
Enhanced Deception Detection API Routes

Provides comprehensive deception detection capabilities with:
- Art of War deception techniques
- Multi-domain support (defense, intelligence, business, cybersecurity, geopolitical)
- Cultural deception patterns
- Strategic misdirection detection
- Early warning indicators
- Real-time monitoring capabilities
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from loguru import logger
from uuid import uuid4

from src.core.orchestrator import SentimentOrchestrator
from src.core.models import AnalysisRequest, DataType
from src.core.enhanced_deception_detection_engine import (
    enhanced_deception_detection_engine,
    DeceptionDomain,
    DeceptionSeverity,
    DeceptionType,
    DeceptionIndicator,
    DeceptionPattern,
    DeceptionAnalysisResult
)

# Initialize router
router = APIRouter(prefix="/enhanced-deception-detection", tags=["Enhanced Deception Detection"])

# Global orchestrator reference
orchestrator: Optional[SentimentOrchestrator] = None

# Request/Response models
class EnhancedDeceptionDetectionRequest(BaseModel):
    """Request model for enhanced deception detection."""
    content: str = Field(..., description="Text content to analyze for deception")
    domain: DeceptionDomain = Field(default=DeceptionDomain.GENERAL, description="Domain for analysis")
    language: str = Field(default="en", description="Language code")
    include_art_of_war: bool = Field(default=True, description="Include Art of War deception techniques")
    include_cultural: bool = Field(default=True, description="Include cultural deception patterns")
    include_domain_specific: bool = Field(default=True, description="Include domain-specific deception patterns")
    include_linguistic: bool = Field(default=True, description="Include linguistic deception patterns")
    include_strategic: bool = Field(default=True, description="Include strategic deception patterns")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class DeceptionIndicatorResponse(BaseModel):
    """Response model for deception indicators."""
    indicator_id: str
    indicator_type: str
    domain: str
    confidence: float
    severity: str
    description: str
    evidence: List[str]
    source_text: str
    timestamp: datetime
    art_of_war_technique: Optional[str] = None
    cultural_context: Optional[str] = None
    strategic_implications: Optional[List[str]] = None
    metadata: Dict[str, Any]

class DeceptionPatternResponse(BaseModel):
    """Response model for deception patterns."""
    pattern_id: str
    pattern_type: str
    domain: str
    indicators: List[DeceptionIndicatorResponse]
    confidence: float
    description: str
    first_detected: datetime
    last_detected: datetime
    frequency: int
    art_of_war_techniques: List[str]
    strategic_implications: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]

class EnhancedDeceptionDetectionResponse(BaseModel):
    """Response model for enhanced deception detection."""
    request_id: str
    domain: str
    overall_deception_score: float
    severity_level: str
    indicators_detected: int
    patterns_detected: int
    critical_alerts: int
    indicators: List[DeceptionIndicatorResponse]
    patterns: List[DeceptionPatternResponse]
    art_of_war_techniques_detected: List[str]
    cultural_patterns_detected: List[str]
    strategic_implications: List[str]
    recommendations: List[str]
    early_warning_indicators: List[str]
    analysis_timestamp: datetime
    processing_time_ms: float
    metadata: Dict[str, Any]

class BatchEnhancedDeceptionDetectionRequest(BaseModel):
    """Request model for batch enhanced deception detection."""
    contents: List[str] = Field(..., description="List of text contents to analyze")
    domain: DeceptionDomain = Field(default=DeceptionDomain.GENERAL, description="Domain for analysis")
    language: str = Field(default="en", description="Language code")
    include_art_of_war: bool = Field(default=True, description="Include Art of War deception techniques")
    include_cultural: bool = Field(default=True, description="Include cultural deception patterns")
    include_domain_specific: bool = Field(default=True, description="Include domain-specific deception patterns")
    include_linguistic: bool = Field(default=True, description="Include linguistic deception patterns")
    include_strategic: bool = Field(default=True, description="Include strategic deception patterns")
    parallel_processing: bool = Field(default=True, description="Enable parallel processing")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class BatchEnhancedDeceptionDetectionResponse(BaseModel):
    """Response model for batch enhanced deception detection."""
    batch_id: str
    total_requests: int
    processed_requests: int
    failed_requests: int
    results: List[EnhancedDeceptionDetectionResponse]
    overall_statistics: Dict[str, Any]
    processing_time_ms: float
    metadata: Dict[str, Any]

class DomainCapabilitiesResponse(BaseModel):
    """Response model for domain capabilities."""
    domain: str
    supported_languages: List[str]
    art_of_war_techniques: List[str]
    cultural_patterns: List[str]
    domain_specific_patterns: List[str]
    linguistic_patterns: List[str]
    strategic_patterns: List[str]
    capabilities: Dict[str, Any]

# Helper functions
def set_orchestrator(orch: SentimentOrchestrator):
    """Set the global orchestrator reference."""
    global orchestrator
    orchestrator = orch

def convert_indicator_to_response(indicator: DeceptionIndicator) -> DeceptionIndicatorResponse:
    """Convert DeceptionIndicator to DeceptionIndicatorResponse."""
    return DeceptionIndicatorResponse(
        indicator_id=indicator.indicator_id,
        indicator_type=indicator.indicator_type.value,
        domain=indicator.domain.value,
        confidence=indicator.confidence,
        severity=indicator.severity.value,
        description=indicator.description,
        evidence=indicator.evidence,
        source_text=indicator.source_text,
        timestamp=indicator.timestamp,
        art_of_war_technique=indicator.art_of_war_technique,
        cultural_context=indicator.cultural_context,
        strategic_implications=indicator.strategic_implications,
        metadata=indicator.metadata
    )

def convert_pattern_to_response(pattern: DeceptionPattern) -> DeceptionPatternResponse:
    """Convert DeceptionPattern to DeceptionPatternResponse."""
    return DeceptionPatternResponse(
        pattern_id=pattern.pattern_id,
        pattern_type=pattern.pattern_type,
        domain=pattern.domain.value,
        indicators=[convert_indicator_to_response(indicator) for indicator in pattern.indicators],
        confidence=pattern.confidence,
        description=pattern.description,
        first_detected=pattern.first_detected,
        last_detected=pattern.last_detected,
        frequency=pattern.frequency,
        art_of_war_techniques=pattern.art_of_war_techniques,
        strategic_implications=pattern.strategic_implications,
        recommendations=pattern.recommendations,
        metadata=pattern.metadata
    )

def convert_result_to_response(result: DeceptionAnalysisResult) -> EnhancedDeceptionDetectionResponse:
    """Convert DeceptionAnalysisResult to EnhancedDeceptionDetectionResponse."""
    return EnhancedDeceptionDetectionResponse(
        request_id=result.request_id,
        domain=result.domain.value,
        overall_deception_score=result.overall_deception_score,
        severity_level=result.severity_level.value,
        indicators_detected=result.indicators_detected,
        patterns_detected=result.patterns_detected,
        critical_alerts=result.critical_alerts,
        indicators=[convert_indicator_to_response(indicator) for indicator in result.indicators],
        patterns=[convert_pattern_to_response(pattern) for pattern in result.patterns],
        art_of_war_techniques_detected=result.art_of_war_techniques_detected,
        cultural_patterns_detected=result.cultural_patterns_detected,
        strategic_implications=result.strategic_implications,
        recommendations=result.recommendations,
        early_warning_indicators=result.early_warning_indicators,
        analysis_timestamp=result.analysis_timestamp,
        processing_time_ms=result.processing_time_ms,
        metadata=result.metadata
    )

# API Endpoints
@router.post("/analyze", response_model=EnhancedDeceptionDetectionResponse)
async def analyze_deception_comprehensive(request: EnhancedDeceptionDetectionRequest):
    """Comprehensive deception analysis with all detection methods."""
    try:
        logger.info(f"Processing enhanced deception detection request for domain: {request.domain}")
        
        result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text=request.content,
            domain=request.domain,
            language=request.language,
            include_art_of_war=request.include_art_of_war,
            include_cultural=request.include_cultural,
            include_domain_specific=request.include_domain_specific,
            include_linguistic=request.include_linguistic,
            include_strategic=request.include_strategic
        )
        
        response = convert_result_to_response(result)
        logger.info(f"Enhanced deception detection completed: {result.indicators_detected} indicators, {result.patterns_detected} patterns")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in enhanced deception detection: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced deception detection failed: {str(e)}")

@router.post("/analyze-defense", response_model=EnhancedDeceptionDetectionResponse)
async def analyze_deception_defense(request: EnhancedDeceptionDetectionRequest):
    """Defense domain deception analysis."""
    try:
        logger.info("Processing defense domain deception analysis")
        
        # Override domain to defense
        request.domain = DeceptionDomain.DEFENSE
        
        result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text=request.content,
            domain=DeceptionDomain.DEFENSE,
            language=request.language,
            include_art_of_war=request.include_art_of_war,
            include_cultural=request.include_cultural,
            include_domain_specific=True,  # Always include domain-specific for defense
            include_linguistic=request.include_linguistic,
            include_strategic=request.include_strategic
        )
        
        response = convert_result_to_response(result)
        logger.info(f"Defense domain deception analysis completed: {result.indicators_detected} indicators")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in defense domain deception analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Defense domain deception analysis failed: {str(e)}")

@router.post("/analyze-intelligence", response_model=EnhancedDeceptionDetectionResponse)
async def analyze_deception_intelligence(request: EnhancedDeceptionDetectionRequest):
    """Intelligence domain deception analysis."""
    try:
        logger.info("Processing intelligence domain deception analysis")
        
        result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text=request.content,
            domain=DeceptionDomain.INTELLIGENCE,
            language=request.language,
            include_art_of_war=request.include_art_of_war,
            include_cultural=request.include_cultural,
            include_domain_specific=True,  # Always include domain-specific for intelligence
            include_linguistic=request.include_linguistic,
            include_strategic=request.include_strategic
        )
        
        response = convert_result_to_response(result)
        logger.info(f"Intelligence domain deception analysis completed: {result.indicators_detected} indicators")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in intelligence domain deception analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Intelligence domain deception analysis failed: {str(e)}")

@router.post("/analyze-business", response_model=EnhancedDeceptionDetectionResponse)
async def analyze_deception_business(request: EnhancedDeceptionDetectionRequest):
    """Business domain deception analysis."""
    try:
        logger.info("Processing business domain deception analysis")
        
        result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text=request.content,
            domain=DeceptionDomain.BUSINESS,
            language=request.language,
            include_art_of_war=request.include_art_of_war,
            include_cultural=request.include_cultural,
            include_domain_specific=True,  # Always include domain-specific for business
            include_linguistic=request.include_linguistic,
            include_strategic=request.include_strategic
        )
        
        response = convert_result_to_response(result)
        logger.info(f"Business domain deception analysis completed: {result.indicators_detected} indicators")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in business domain deception analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Business domain deception analysis failed: {str(e)}")

@router.post("/analyze-cybersecurity", response_model=EnhancedDeceptionDetectionResponse)
async def analyze_deception_cybersecurity(request: EnhancedDeceptionDetectionRequest):
    """Cybersecurity domain deception analysis."""
    try:
        logger.info("Processing cybersecurity domain deception analysis")
        
        result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text=request.content,
            domain=DeceptionDomain.CYBERSECURITY,
            language=request.language,
            include_art_of_war=request.include_art_of_war,
            include_cultural=request.include_cultural,
            include_domain_specific=True,  # Always include domain-specific for cybersecurity
            include_linguistic=request.include_linguistic,
            include_strategic=request.include_strategic
        )
        
        response = convert_result_to_response(result)
        logger.info(f"Cybersecurity domain deception analysis completed: {result.indicators_detected} indicators")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in cybersecurity domain deception analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Cybersecurity domain deception analysis failed: {str(e)}")

@router.post("/analyze-geopolitical", response_model=EnhancedDeceptionDetectionResponse)
async def analyze_deception_geopolitical(request: EnhancedDeceptionDetectionRequest):
    """Geopolitical domain deception analysis."""
    try:
        logger.info("Processing geopolitical domain deception analysis")
        
        result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text=request.content,
            domain=DeceptionDomain.GEOPOLITICAL,
            language=request.language,
            include_art_of_war=request.include_art_of_war,
            include_cultural=request.include_cultural,
            include_domain_specific=True,  # Always include domain-specific for geopolitical
            include_linguistic=request.include_linguistic,
            include_strategic=request.include_strategic
        )
        
        response = convert_result_to_response(result)
        logger.info(f"Geopolitical domain deception analysis completed: {result.indicators_detected} indicators")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in geopolitical domain deception analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Geopolitical domain deception analysis failed: {str(e)}")

@router.post("/analyze-batch", response_model=BatchEnhancedDeceptionDetectionResponse)
async def analyze_deception_batch(request: BatchEnhancedDeceptionDetectionRequest):
    """Batch deception analysis for multiple contents."""
    try:
        logger.info(f"Processing batch deception analysis for {len(request.contents)} contents")
        start_time = datetime.now()
        
        results = []
        failed_requests = 0
        
        for i, content in enumerate(request.contents):
            try:
                result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
                    text=content,
                    domain=request.domain,
                    language=request.language,
                    include_art_of_war=request.include_art_of_war,
                    include_cultural=request.include_cultural,
                    include_domain_specific=request.include_domain_specific,
                    include_linguistic=request.include_linguistic,
                    include_strategic=request.include_strategic
                )
                
                response = convert_result_to_response(result)
                results.append(response)
                
            except Exception as e:
                logger.error(f"Error processing content {i}: {e}")
                failed_requests += 1
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Calculate overall statistics
        overall_statistics = {
            "total_indicators": sum(r.indicators_detected for r in results),
            "total_patterns": sum(r.patterns_detected for r in results),
            "total_critical_alerts": sum(r.critical_alerts for r in results),
            "average_deception_score": sum(r.overall_deception_score for r in results) / len(results) if results else 0.0,
            "severity_distribution": {
                "critical": len([r for r in results if r.severity_level == "critical"]),
                "high": len([r for r in results if r.severity_level == "high"]),
                "medium": len([r for r in results if r.severity_level == "medium"]),
                "low": len([r for r in results if r.severity_level == "low"])
            }
        }
        
        response = BatchEnhancedDeceptionDetectionResponse(
            batch_id=str(uuid4()),
            total_requests=len(request.contents),
            processed_requests=len(results),
            failed_requests=failed_requests,
            results=results,
            overall_statistics=overall_statistics,
            processing_time_ms=processing_time,
            metadata=request.metadata or {}
        )
        
        logger.info(f"Batch deception analysis completed: {len(results)} processed, {failed_requests} failed")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in batch deception analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Batch deception analysis failed: {str(e)}")

@router.get("/domains", response_model=List[str])
async def get_supported_domains():
    """Get list of supported deception detection domains."""
    try:
        domains = [domain.value for domain in DeceptionDomain]
        logger.info(f"Retrieved supported domains: {domains}")
        return domains
    except Exception as e:
        logger.error(f"Error retrieving supported domains: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve supported domains: {str(e)}")

@router.get("/domain-capabilities/{domain}", response_model=DomainCapabilitiesResponse)
async def get_domain_capabilities(domain: str):
    """Get capabilities for a specific domain."""
    try:
        # Validate domain
        try:
            domain_enum = DeceptionDomain(domain)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Unsupported domain: {domain}")
        
        # Get capabilities from the engine
        engine = enhanced_deception_detection_engine
        
        capabilities = DomainCapabilitiesResponse(
            domain=domain,
            supported_languages=["en", "zh", "ru", "ar"],  # Add more as needed
            art_of_war_techniques=list(engine.art_of_war_techniques.TECHNIQUES.keys()),
            cultural_patterns=list(engine.cultural_patterns.PATTERNS.keys()),
            domain_specific_patterns=list(engine.domain_patterns.PATTERNS.keys()) if domain_enum in engine.domain_patterns.PATTERNS else [],
            linguistic_patterns=list(engine.linguistic_patterns.keys()),
            strategic_patterns=list(engine.strategic_patterns.keys()),
            capabilities={
                "art_of_war_detection": True,
                "cultural_detection": True,
                "domain_specific_detection": domain_enum in engine.domain_patterns.PATTERNS,
                "linguistic_detection": True,
                "strategic_detection": True,
                "early_warning_indicators": True,
                "recommendations": True
            }
        )
        
        logger.info(f"Retrieved capabilities for domain: {domain}")
        return capabilities
        
    except Exception as e:
        logger.error(f"Error retrieving domain capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve domain capabilities: {str(e)}")

@router.get("/art-of-war-techniques", response_model=Dict[str, Any])
async def get_art_of_war_techniques():
    """Get available Art of War deception techniques."""
    try:
        techniques = enhanced_deception_detection_engine.art_of_war_techniques.TECHNIQUES
        logger.info(f"Retrieved {len(techniques)} Art of War techniques")
        return techniques
    except Exception as e:
        logger.error(f"Error retrieving Art of War techniques: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Art of War techniques: {str(e)}")

@router.get("/cultural-patterns", response_model=Dict[str, Any])
async def get_cultural_patterns():
    """Get available cultural deception patterns."""
    try:
        patterns = enhanced_deception_detection_engine.cultural_patterns.PATTERNS
        logger.info(f"Retrieved cultural patterns for {len(patterns)} languages")
        return patterns
    except Exception as e:
        logger.error(f"Error retrieving cultural patterns: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve cultural patterns: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for enhanced deception detection service."""
    try:
        # Test the engine
        test_result = await enhanced_deception_detection_engine.analyze_deception_comprehensive(
            text="This is a test message for health check.",
            domain=DeceptionDomain.GENERAL,
            language="en",
            include_art_of_war=False,
            include_cultural=False,
            include_domain_specific=False,
            include_linguistic=True,
            include_strategic=False
        )
        
        health_status = {
            "status": "healthy",
            "service": "enhanced_deception_detection",
            "timestamp": datetime.now().isoformat(),
            "engine_status": "operational",
            "test_analysis_completed": True,
            "supported_domains": [domain.value for domain in DeceptionDomain],
            "art_of_war_techniques": len(enhanced_deception_detection_engine.art_of_war_techniques.TECHNIQUES),
            "cultural_patterns": len(enhanced_deception_detection_engine.cultural_patterns.PATTERNS),
            "domain_patterns": len(enhanced_deception_detection_engine.domain_patterns.PATTERNS),
            "linguistic_patterns": len(enhanced_deception_detection_engine.linguistic_patterns),
            "strategic_patterns": len(enhanced_deception_detection_engine.strategic_patterns)
        }
        
        logger.info("Enhanced deception detection health check passed")
        return health_status
        
    except Exception as e:
        logger.error(f"Enhanced deception detection health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/summary")
async def get_service_summary():
    """Get summary of enhanced deception detection service."""
    try:
        engine = enhanced_deception_detection_engine
        
        summary = {
            "service_name": "Enhanced Deception Detection",
            "description": "Comprehensive deception detection system with Art of War principles and multi-domain support",
            "version": "1.0.0",
            "capabilities": {
                "art_of_war_detection": {
                    "enabled": True,
                    "techniques_count": len(engine.art_of_war_techniques.TECHNIQUES),
                    "description": "Detect Art of War deception techniques"
                },
                "cultural_detection": {
                    "enabled": True,
                    "languages_count": len(engine.cultural_patterns.PATTERNS),
                    "description": "Detect cultural deception patterns"
                },
                "domain_specific_detection": {
                    "enabled": True,
                    "domains_count": len(engine.domain_patterns.PATTERNS),
                    "description": "Detect domain-specific deception patterns"
                },
                "linguistic_detection": {
                    "enabled": True,
                    "patterns_count": len(engine.linguistic_patterns),
                    "description": "Detect linguistic deception patterns"
                },
                "strategic_detection": {
                    "enabled": True,
                    "patterns_count": len(engine.strategic_patterns),
                    "description": "Detect strategic deception patterns"
                }
            },
            "supported_domains": [domain.value for domain in DeceptionDomain],
            "supported_languages": ["en", "zh", "ru", "ar"],
            "endpoints": [
                "/analyze",
                "/analyze-defense",
                "/analyze-intelligence", 
                "/analyze-business",
                "/analyze-cybersecurity",
                "/analyze-geopolitical",
                "/analyze-batch",
                "/domains",
                "/domain-capabilities/{domain}",
                "/art-of-war-techniques",
                "/cultural-patterns",
                "/health",
                "/summary"
            ]
        }
        
        logger.info("Enhanced deception detection service summary retrieved")
        return summary
        
    except Exception as e:
        logger.error(f"Error retrieving service summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve service summary: {str(e)}")
