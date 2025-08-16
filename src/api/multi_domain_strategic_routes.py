"""
Multi-Domain Strategic Analysis API Routes

This module provides API endpoints for comprehensive strategic analysis
across multiple domains including defense, intelligence, and business applications.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from loguru import logger

# Import the multi-domain strategic engine
try:
    from src.core.multi_domain_strategic_engine import (
        MultiDomainStrategicEngine, 
        DomainType, 
        AnalysisType, 
        StrategicContext
    )
    STRATEGIC_ENGINE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Multi-domain strategic engine not available: {e}")
    STRATEGIC_ENGINE_AVAILABLE = False

router = APIRouter(prefix="/strategic", tags=["Multi-Domain Strategic Analysis"])

# Initialize the strategic engine
if STRATEGIC_ENGINE_AVAILABLE:
    strategic_engine = MultiDomainStrategicEngine()


# Request/Response Models
class DomainTypeModel(str, Enum):
    """Domain types for strategic analysis."""
    DEFENSE = "defense"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    CYBER = "cyber"
    DIPLOMATIC = "diplomatic"
    ECONOMIC = "economic"


class AnalysisTypeModel(str, Enum):
    """Types of strategic analysis available."""
    THREAT_ASSESSMENT = "threat_assessment"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    CULTURAL_ANALYSIS = "cultural_analysis"
    DECEPTION_DETECTION = "deception_detection"
    SCENARIO_PLANNING = "scenario_planning"
    RISK_ANALYSIS = "risk_analysis"
    OPPORTUNITY_ANALYSIS = "opportunity_analysis"
    STRATEGIC_POSITIONING = "strategic_positioning"


class StrategicContextRequest(BaseModel):
    """Request model for strategic context analysis."""
    domain: DomainTypeModel = Field(..., description="Domain for analysis")
    region: str = Field(..., description="Geographic region of interest")
    timeframe: str = Field(..., description="Timeframe for analysis")
    stakeholders: List[str] = Field(default=[], description="Key stakeholders")
    objectives: List[str] = Field(default=[], description="Strategic objectives")
    constraints: List[str] = Field(default=[], description="Strategic constraints")
    resources: Dict[str, Any] = Field(default={}, description="Available resources")
    analysis_types: List[AnalysisTypeModel] = Field(..., description="Types of analysis to perform")
    content_data: Optional[str] = Field(None, description="Content data for analysis")


class StrategicAnalysisResponse(BaseModel):
    """Response model for strategic analysis."""
    success: bool
    analysis_id: str
    timestamp: str
    domain: str
    analysis_types: List[str]
    findings: List[Dict[str, Any]]
    strategic_assessment: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    risk_analysis: Dict[str, Any]
    cultural_insights: Dict[str, Any]
    art_of_war_analysis: Dict[str, Any]
    report_path: Optional[str] = None
    error: Optional[str] = None


class StrategicContextResponse(BaseModel):
    """Response model for strategic context."""
    success: bool
    context: Dict[str, Any]
    frameworks: Dict[str, Any]
    indicators: Dict[str, Any]
    error: Optional[str] = None


# API Endpoints
@router.post("/analyze", response_model=StrategicAnalysisResponse)
async def analyze_strategic_context(
    request: StrategicContextRequest,
    background_tasks: BackgroundTasks
) -> StrategicAnalysisResponse:
    """
    Perform comprehensive strategic analysis for a given context.
    
    This endpoint provides multi-domain strategic analysis integrating:
    - Art of War principles and frameworks
    - Cross-cultural strategic patterns
    - Domain-specific threat assessments
    - Strategic recommendations and risk analysis
    """
    if not STRATEGIC_ENGINE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Strategic analysis engine not available"
        )
    
    try:
        logger.info(f"Starting strategic analysis for domain: {request.domain}")
        
        # Convert request to StrategicContext
        context = StrategicContext(
            domain=DomainType(request.domain),
            region=request.region,
            timeframe=request.timeframe,
            stakeholders=request.stakeholders,
            objectives=request.objectives,
            constraints=request.constraints,
            resources=request.resources
        )
        
        # Convert analysis types
        analysis_types = [AnalysisType(at) for at in request.analysis_types]
        
        # Perform strategic analysis
        results = await strategic_engine.analyze_strategic_context(
            context=context,
            analysis_types=analysis_types,
            content_data=request.content_data
        )
        
        if "error" in results:
            raise HTTPException(
                status_code=500,
                detail=f"Strategic analysis failed: {results['error']}"
            )
        
        # Generate analysis ID
        analysis_id = f"strategic_{request.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add background task for report generation
        background_tasks.add_task(
            strategic_engine._save_strategic_analysis_report,
            results
        )
        
        return StrategicAnalysisResponse(
            success=True,
            analysis_id=analysis_id,
            timestamp=results["analysis_metadata"]["timestamp"],
            domain=results["analysis_metadata"]["domain"],
            analysis_types=results["analysis_metadata"]["analysis_types"],
            findings=results.get("findings", []),
            strategic_assessment=results.get("strategic_assessment", {}),
            recommendations=results.get("strategic_recommendations", []),
            risk_analysis=results.get("risk_analysis", {}),
            cultural_insights=results.get("cultural_analysis", {}),
            art_of_war_analysis=results.get("art_of_war_analysis", {}),
            report_path=results.get("report_path")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Strategic analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Strategic analysis failed: {str(e)}"
        )


@router.get("/context/{domain}", response_model=StrategicContextResponse)
async def get_strategic_context(domain: DomainTypeModel) -> StrategicContextResponse:
    """
    Get strategic context information for a specific domain.
    
    Returns frameworks, indicators, and contextual information
    relevant to the specified domain.
    """
    if not STRATEGIC_ENGINE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Strategic analysis engine not available"
        )
    
    try:
        # Get domain-specific information
        context_info = {
            "domain": domain.value,
            "frameworks": strategic_engine.art_of_war_frameworks,
            "cultural_patterns": strategic_engine.cultural_patterns,
            "strategic_indicators": strategic_engine.strategic_indicators.get(domain.value, [])
        }
        
        return StrategicContextResponse(
            success=True,
            context=context_info,
            frameworks=strategic_engine.art_of_war_frameworks,
            indicators=strategic_engine.strategic_indicators
        )
        
    except Exception as e:
        logger.error(f"Get strategic context error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get strategic context: {str(e)}"
        )


@router.get("/domains")
async def get_supported_domains() -> Dict[str, Any]:
    """
    Get list of supported domains for strategic analysis.
    """
    domains = [
        {
            "domain": domain.value,
            "description": f"Strategic analysis for {domain.value} applications",
            "analysis_types": [
                at.value for at in AnalysisType
            ]
        }
        for domain in DomainType
    ]
    
    return {
        "success": True,
        "domains": domains,
        "count": len(domains)
    }


@router.get("/analysis-types")
async def get_analysis_types() -> Dict[str, Any]:
    """
    Get list of available analysis types.
    """
    analysis_types = [
        {
            "type": at.value,
            "description": f"{at.value.replace('_', ' ').title()} analysis",
            "applicable_domains": [
                domain.value for domain in DomainType
            ]
        }
        for at in AnalysisType
    ]
    
    return {
        "success": True,
        "analysis_types": analysis_types,
        "count": len(analysis_types)
    }


@router.post("/deception-detection")
async def detect_deception_patterns(content: str) -> Dict[str, Any]:
    """
    Detect deception patterns in content using strategic analysis.
    """
    if not STRATEGIC_ENGINE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Strategic analysis engine not available"
        )
    
    try:
        # Use the deception agent to analyze content
        deception_analysis = await strategic_engine._detect_deception_patterns(content)
        
        if "error" in deception_analysis:
            raise HTTPException(
                status_code=500,
                detail=f"Deception detection failed: {deception_analysis['error']}"
            )
        
        return {
            "success": True,
            "deception_analysis": deception_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Deception detection error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Deception detection failed: {str(e)}"
        )


@router.post("/cultural-analysis")
async def analyze_cultural_patterns(
    domain: DomainTypeModel,
    region: str,
    content_data: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze cultural patterns for strategic context.
    """
    if not STRATEGIC_ENGINE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Strategic analysis engine not available"
        )
    
    try:
        # Create strategic context
        context = StrategicContext(
            domain=DomainType(domain),
            region=region,
            timeframe="current",
            stakeholders=[],
            objectives=[],
            constraints=[],
            resources={}
        )
        
        # Perform cultural analysis
        cultural_analysis = await strategic_engine._analyze_cultural_patterns(context)
        
        return {
            "success": True,
            "cultural_analysis": cultural_analysis,
            "domain": domain.value,
            "region": region,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cultural analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Cultural analysis failed: {str(e)}"
        )


@router.post("/art-of-war-analysis")
async def apply_art_of_war_frameworks(
    domain: DomainTypeModel,
    region: str,
    context_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply Art of War frameworks to strategic context.
    """
    if not STRATEGIC_ENGINE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Strategic analysis engine not available"
        )
    
    try:
        # Create strategic context
        context = StrategicContext(
            domain=DomainType(domain),
            region=region,
            timeframe=context_data.get("timeframe", "current"),
            stakeholders=context_data.get("stakeholders", []),
            objectives=context_data.get("objectives", []),
            constraints=context_data.get("constraints", []),
            resources=context_data.get("resources", {})
        )
        
        # Apply Art of War frameworks
        art_of_war_analysis = await strategic_engine._apply_art_of_war_frameworks(context)
        
        return {
            "success": True,
            "art_of_war_analysis": art_of_war_analysis,
            "domain": domain.value,
            "region": region,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Art of War analysis error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Art of War analysis failed: {str(e)}"
        )


@router.get("/health")
async def get_strategic_analysis_health() -> Dict[str, Any]:
    """
    Get health status of strategic analysis engine.
    """
    return {
        "success": True,
        "engine_available": STRATEGIC_ENGINE_AVAILABLE,
        "timestamp": datetime.now().isoformat(),
        "status": "healthy" if STRATEGIC_ENGINE_AVAILABLE else "unavailable"
    }
