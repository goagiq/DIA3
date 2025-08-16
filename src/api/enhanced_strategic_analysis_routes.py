"""
Enhanced Strategic Analysis API Routes

This module provides API endpoints for enhanced strategic analysis based on The Art of War principles,
with multi-domain support for defense, intelligence, business, and other applications.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from loguru import logger

# Import the enhanced strategic analysis engine
try:
    from src.core.enhanced_strategic_analysis_engine import (
        enhanced_strategic_analysis_engine,
        StrategicAnalysis,
        ArtOfWarPrinciple,
        StrategicMove
    )
    # Initialize the engine if it's not already initialized
    if enhanced_strategic_analysis_engine is None:
        from src.core.enhanced_strategic_analysis_engine import EnhancedStrategicAnalysisEngine
        enhanced_strategic_analysis_engine = EnhancedStrategicAnalysisEngine()
    ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced strategic analysis engine not available: {e}")
    ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE = False
    enhanced_strategic_analysis_engine = None

# Create router
router = APIRouter(prefix="/enhanced-strategic", tags=["Enhanced Strategic Analysis"])


# Pydantic models for request/response
class StrategicAnalysisRequest(BaseModel):
    """Request model for strategic analysis."""
    content: str = Field(..., description="Content to analyze for strategic patterns")
    domain: str = Field(..., description="Analysis domain (defense, intelligence, business, etc.)")
    language: str = Field(default="en", description="Content language")
    analysis_depth: str = Field(default="comprehensive", description="Analysis depth (basic, standard, comprehensive)")


class StrategicMoveResponse(BaseModel):
    """Response model for strategic moves."""
    move_id: str
    principle: str
    domain: str
    description: str
    likelihood: float
    impact: str
    indicators: List[str]
    counter_measures: List[str]
    timeframe: str
    confidence: float


class ArtOfWarPrincipleResponse(BaseModel):
    """Response model for Art of War principles."""
    chinese: str
    translation: str
    explanation: str
    modern_applications: List[str]
    domain_applications: Dict[str, List[str]]
    detection_patterns: List[str]
    counter_strategies: List[str]


class StrategicAnalysisResponse(BaseModel):
    """Response model for strategic analysis."""
    analysis_id: str
    domain: str
    content: str
    principles_detected: List[ArtOfWarPrincipleResponse]
    strategic_moves: List[StrategicMoveResponse]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    confidence_score: float
    timestamp: datetime


class DomainCapabilitiesResponse(BaseModel):
    """Response model for domain capabilities."""
    domain: str
    supported_principles: List[str]
    detection_patterns: Dict[str, List[str]]
    analysis_capabilities: List[str]


# Health check endpoint
@router.get("/health")
async def enhanced_strategic_analysis_health():
    """Health check for enhanced strategic analysis service."""
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    return {
        "status": "healthy",
        "service": "enhanced_strategic_analysis",
        "available": True,
        "timestamp": datetime.now().isoformat()
    }


# Main strategic analysis endpoint
@router.post("/analyze", response_model=StrategicAnalysisResponse)
async def analyze_strategic_content(request: StrategicAnalysisRequest):
    """
    Analyze content for strategic patterns based on Art of War principles.
    
    This endpoint provides comprehensive strategic analysis across multiple domains:
    - Defense and military applications
    - Intelligence and security analysis
    - Business strategy and competitive intelligence
    - Cybersecurity threat assessment
    - Geopolitical analysis
    """
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    try:
        logger.info(f"Starting enhanced strategic analysis for domain: {request.domain}")
        
        # Perform strategic analysis
        analysis = await enhanced_strategic_analysis_engine.analyze_strategic_content(
            content=request.content,
            domain=request.domain,
            language=request.language,
            analysis_depth=request.analysis_depth
        )
        
        # Convert to response model
        response = StrategicAnalysisResponse(
            analysis_id=analysis.analysis_id,
            domain=analysis.domain,
            content=analysis.content,
            principles_detected=[
                ArtOfWarPrincipleResponse(
                    chinese=principle.chinese,
                    translation=principle.translation,
                    explanation=principle.explanation,
                    modern_applications=principle.modern_applications,
                    domain_applications=principle.domain_applications,
                    detection_patterns=principle.detection_patterns,
                    counter_strategies=principle.counter_strategies
                )
                for principle in analysis.principles_detected
            ],
            strategic_moves=[
                StrategicMoveResponse(
                    move_id=move.move_id,
                    principle=move.principle,
                    domain=move.domain,
                    description=move.description,
                    likelihood=move.likelihood,
                    impact=move.impact,
                    indicators=move.indicators,
                    counter_measures=move.counter_measures,
                    timeframe=move.timeframe,
                    confidence=move.confidence
                )
                for move in analysis.strategic_moves
            ],
            risk_assessment=analysis.risk_assessment,
            recommendations=analysis.recommendations,
            confidence_score=analysis.confidence_score,
            timestamp=analysis.timestamp
        )
        
        logger.info(f"Enhanced strategic analysis completed with confidence: {analysis.confidence_score:.2f}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in enhanced strategic analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Strategic analysis failed: {str(e)}")


# Domain-specific analysis endpoints
@router.post("/analyze-defense", response_model=StrategicAnalysisResponse)
async def analyze_defense_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for defense domain strategic patterns."""
    request.domain = "defense"
    return await analyze_strategic_content(request)


@router.post("/analyze-intelligence", response_model=StrategicAnalysisResponse)
async def analyze_intelligence_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for intelligence domain strategic patterns."""
    request.domain = "intelligence"
    return await analyze_strategic_content(request)


@router.post("/analyze-business", response_model=StrategicAnalysisResponse)
async def analyze_business_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for business domain strategic patterns."""
    request.domain = "business"
    return await analyze_strategic_content(request)


@router.post("/analyze-cybersecurity", response_model=StrategicAnalysisResponse)
async def analyze_cybersecurity_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for cybersecurity domain strategic patterns."""
    request.domain = "cybersecurity"
    return await analyze_strategic_content(request)


@router.post("/analyze-geopolitical", response_model=StrategicAnalysisResponse)
async def analyze_geopolitical_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for geopolitical domain strategic patterns."""
    request.domain = "geopolitical"
    return await analyze_strategic_content(request)


@router.post("/analyze-financial", response_model=StrategicAnalysisResponse)
async def analyze_financial_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for financial domain strategic patterns."""
    request.domain = "financial"
    return await analyze_strategic_content(request)


@router.post("/analyze-healthcare", response_model=StrategicAnalysisResponse)
async def analyze_healthcare_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for healthcare domain strategic patterns."""
    request.domain = "healthcare"
    return await analyze_strategic_content(request)


@router.post("/analyze-energy", response_model=StrategicAnalysisResponse)
async def analyze_energy_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for energy domain strategic patterns."""
    request.domain = "energy"
    return await analyze_strategic_content(request)


@router.post("/analyze-transportation", response_model=StrategicAnalysisResponse)
async def analyze_transportation_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for transportation domain strategic patterns."""
    request.domain = "transportation"
    return await analyze_strategic_content(request)


@router.post("/analyze-critical-infrastructure", response_model=StrategicAnalysisResponse)
async def analyze_critical_infrastructure_strategic_content(request: StrategicAnalysisRequest):
    """Analyze content for critical infrastructure domain strategic patterns."""
    request.domain = "critical_infrastructure"
    return await analyze_strategic_content(request)


# Information endpoints
@router.get("/domains")
async def get_supported_domains():
    """Get list of supported analysis domains."""
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    try:
        if enhanced_strategic_analysis_engine:
            domains = await enhanced_strategic_analysis_engine.get_supported_domains()
            return {
                "domains": domains,
                "count": len(domains),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=503, detail="Enhanced strategic analysis engine not available")
    except Exception as e:
        logger.error(f"Error getting supported domains: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get supported domains: {str(e)}")


@router.get("/domain-capabilities/{domain}", response_model=DomainCapabilitiesResponse)
async def get_domain_capabilities(domain: str):
    """Get capabilities for a specific domain."""
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    try:
        if enhanced_strategic_analysis_engine:
            capabilities = await enhanced_strategic_analysis_engine.get_domain_capabilities(domain)
            return DomainCapabilitiesResponse(**capabilities)
        else:
            raise HTTPException(status_code=503, detail="Enhanced strategic analysis engine not available")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting domain capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get domain capabilities: {str(e)}")


@router.get("/analysis-history")
async def get_analysis_history(domain: Optional[str] = Query(None, description="Filter by domain")):
    """Get analysis history, optionally filtered by domain."""
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    try:
        if enhanced_strategic_analysis_engine:
            history = await enhanced_strategic_analysis_engine.get_analysis_history(domain)
            return {
                "analysis_history": [
                    {
                        "analysis_id": analysis.analysis_id,
                        "domain": analysis.domain,
                        "confidence_score": analysis.confidence_score,
                        "timestamp": analysis.timestamp.isoformat(),
                        "principles_detected_count": len(analysis.principles_detected),
                        "strategic_moves_count": len(analysis.strategic_moves)
                    }
                    for analysis in history
                ],
                "total_analyses": len(history),
                "filtered_by_domain": domain,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=503, detail="Enhanced strategic analysis engine not available")
    except Exception as e:
        logger.error(f"Error getting analysis history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analysis history: {str(e)}")


# Batch analysis endpoint
@router.post("/analyze-batch")
async def analyze_strategic_content_batch(requests: List[StrategicAnalysisRequest]):
    """Analyze multiple content items for strategic patterns."""
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    try:
        logger.info(f"Starting batch strategic analysis for {len(requests)} items")
        
        results = []
        for i, request in enumerate(requests):
            try:
                analysis = await enhanced_strategic_analysis_engine.analyze_strategic_content(
                    content=request.content,
                    domain=request.domain,
                    language=request.language,
                    analysis_depth=request.analysis_depth
                )
                
                results.append({
                    "index": i,
                    "success": True,
                    "analysis_id": analysis.analysis_id,
                    "domain": analysis.domain,
                    "confidence_score": analysis.confidence_score,
                    "principles_detected_count": len(analysis.principles_detected),
                    "strategic_moves_count": len(analysis.strategic_moves),
                    "risk_level": analysis.risk_assessment.get("overall_risk_level", "unknown")
                })
                
            except Exception as e:
                logger.error(f"Error analyzing item {i}: {e}")
                results.append({
                    "index": i,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "batch_results": results,
            "total_items": len(requests),
            "successful_analyses": sum(1 for r in results if r["success"]),
            "failed_analyses": sum(1 for r in results if not r["success"]),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in batch strategic analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


# Summary endpoint
@router.get("/summary")
async def get_enhanced_strategic_analysis_summary():
    """Get summary of enhanced strategic analysis capabilities."""
    if not ENHANCED_STRATEGIC_ANALYSIS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Enhanced strategic analysis service not available")
    
    try:
        if enhanced_strategic_analysis_engine:
            domains = await enhanced_strategic_analysis_engine.get_supported_domains()
            history = await enhanced_strategic_analysis_engine.get_analysis_history()
            
            return {
                "service": "Enhanced Strategic Analysis",
                "description": "Comprehensive strategic analysis based on The Art of War principles",
                "supported_domains": domains,
                "total_analyses_performed": len(history),
                "analysis_by_domain": {
                    domain: len([h for h in history if h.domain == domain])
                    for domain in domains
                },
                "capabilities": [
                    "Art of War principle detection",
                    "Strategic move identification",
                    "Risk assessment",
                    "Recommendation generation",
                    "Multi-domain analysis",
                    "Pattern recognition",
                    "Historical analysis tracking"
                ],
                "endpoints": [
                    "POST /enhanced-strategic/analyze - General strategic analysis",
                    "POST /enhanced-strategic/analyze-{domain} - Domain-specific analysis",
                    "GET /enhanced-strategic/domains - Get supported domains",
                    "GET /enhanced-strategic/domain-capabilities/{domain} - Get domain capabilities",
                    "GET /enhanced-strategic/analysis-history - Get analysis history",
                    "POST /enhanced-strategic/analyze-batch - Batch analysis",
                    "GET /enhanced-strategic/health - Health check"
                ],
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=503, detail="Enhanced strategic analysis engine not available")
        
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get summary: {str(e)}")
