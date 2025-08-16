"""
Multi-Domain Strategic Analysis API Routes
Provides generic strategic analysis endpoints for multiple domains including business, defense, and intelligence.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from loguru import logger

from src.core.multi_domain_strategic_analyzer import (
    MultiDomainStrategicAnalyzer,
    DomainType,
    AnalysisType,
    StrategicContext,
    StrategicRecommendation
)

# Initialize router
router = APIRouter(prefix="/multi-domain", tags=["Multi-Domain Strategic Analysis"])

# Initialize analyzer
analyzer = MultiDomainStrategicAnalyzer()


# Request Models
class MultiDomainStrategicRequest(BaseModel):
    """Request model for multi-domain strategic analysis."""
    content: str = Field(..., description="Analysis content or query")
    domain: str = Field(..., description="Target domain for analysis")
    analysis_type: str = Field(
        default="comprehensive", 
        description="Type of analysis to perform"
    )
    include_art_of_war: bool = Field(
        default=True, 
        description="Whether to include Art of War principles"
    )
    include_recommendations: bool = Field(
        default=True, 
        description="Whether to include strategic recommendations"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Additional strategic context"
    )


class DomainCapabilitiesRequest(BaseModel):
    """Request model for getting domain capabilities."""
    domain: str = Field(..., description="Domain to get capabilities for")


class StrategicRecommendationResponse(BaseModel):
    """Response model for strategic recommendations."""
    title: str
    description: str
    priority: str
    timeframe: str
    domain: str
    impact_score: float
    implementation_difficulty: str
    resources_required: List[str]
    success_metrics: List[str]


class MultiDomainStrategicResponse(BaseModel):
    """Response model for multi-domain strategic analysis."""
    success: bool
    domain: str
    analysis_type: str
    domain_analysis: Dict[str, Any]
    art_of_war_analysis: Optional[Dict[str, Any]] = None
    strategic_recommendations: Optional[List[StrategicRecommendationResponse]] = None
    metadata: Dict[str, Any]


# API Endpoints
@router.post("/strategic-analysis", response_model=MultiDomainStrategicResponse)
async def multi_domain_strategic_analysis(request: MultiDomainStrategicRequest):
    """
    Perform comprehensive strategic analysis for any supported domain.
    
    Supported domains: business, defense, intelligence, cybersecurity, 
    geopolitical, economic, technological, social, environmental
    """
    try:
        # Validate domain
        try:
            domain = DomainType(request.domain.lower())
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported domain: {request.domain}. "
                       f"Supported domains: {[d.value for d in DomainType]}"
            )
        
        # Validate analysis type
        try:
            analysis_type = AnalysisType(request.analysis_type.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported analysis type: {request.analysis_type}. "
                       f"Supported types: {[at.value for at in AnalysisType]}"
            )
        
        # Create strategic context if provided
        context = None
        if request.context:
            context = StrategicContext(
                domain=domain,
                analysis_type=analysis_type,
                market_conditions=request.context.get("market_conditions"),
                competitive_landscape=request.context.get("competitive_landscape"),
                risk_factors=request.context.get("risk_factors"),
                opportunities=request.context.get("opportunities"),
                threats=request.context.get("threats"),
                trends=request.context.get("trends")
            )
        
        # Perform analysis
        result = await analyzer.analyze_strategic_position(
            content=request.content,
            domain=domain,
            analysis_type=analysis_type,
            context=context,
            include_art_of_war=request.include_art_of_war,
            include_recommendations=request.include_recommendations
        )
        
        # Convert recommendations to response format
        recommendations = None
        if result.get("strategic_recommendations"):
            recommendations = [
                StrategicRecommendationResponse(
                    title=rec.title,
                    description=rec.description,
                    priority=rec.priority,
                    timeframe=rec.timeframe,
                    domain=rec.domain.value,
                    impact_score=rec.impact_score,
                    implementation_difficulty=rec.implementation_difficulty,
                    resources_required=rec.resources_required,
                    success_metrics=rec.success_metrics
                )
                for rec in result["strategic_recommendations"]
            ]
        
        return MultiDomainStrategicResponse(
            success=True,
            domain=domain.value,
            analysis_type=analysis_type.value,
            domain_analysis=result.get("domain_analysis", {}),
            art_of_war_analysis=result.get("art_of_war_analysis"),
            strategic_recommendations=recommendations,
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Multi-domain strategic analysis error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Strategic analysis failed: {str(e)}"
        )


@router.get("/domains", response_model=List[Dict[str, Any]])
async def get_supported_domains():
    """Get list of all supported domains with their capabilities."""
    try:
        domains = await analyzer.get_supported_domains()
        return domains
    except Exception as e:
        logger.error(f"Error getting supported domains: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get supported domains: {str(e)}"
        )


@router.post("/domain-capabilities", response_model=Dict[str, Any])
async def get_domain_capabilities(request: DomainCapabilitiesRequest):
    """Get capabilities and frameworks available for a specific domain."""
    try:
        # Validate domain
        try:
            domain = DomainType(request.domain.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported domain: {request.domain}. "
                       f"Supported domains: {[d.value for d in DomainType]}"
            )
        
        capabilities = await analyzer.get_domain_capabilities(domain)
        return capabilities
        
    except Exception as e:
        logger.error(f"Error getting domain capabilities: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get domain capabilities: {str(e)}"
        )


@router.post("/business-strategic-analysis", response_model=MultiDomainStrategicResponse)
async def business_strategic_analysis(request: MultiDomainStrategicRequest):
    """
    Perform strategic analysis specifically for business domain.
    This is a convenience endpoint that automatically sets the domain to business.
    """
    # Override domain to business
    request.domain = "business"
    return await multi_domain_strategic_analysis(request)


@router.post("/defense-strategic-analysis", response_model=MultiDomainStrategicResponse)
async def defense_strategic_analysis(request: MultiDomainStrategicRequest):
    """
    Perform strategic analysis specifically for defense domain.
    This is a convenience endpoint that automatically sets the domain to defense.
    """
    # Override domain to defense
    request.domain = "defense"
    return await multi_domain_strategic_analysis(request)


@router.post("/intelligence-strategic-analysis", response_model=MultiDomainStrategicResponse)
async def intelligence_strategic_analysis(request: MultiDomainStrategicRequest):
    """
    Perform strategic analysis specifically for intelligence domain.
    This is a convenience endpoint that automatically sets the domain to intelligence.
    """
    # Override domain to intelligence
    request.domain = "intelligence"
    return await multi_domain_strategic_analysis(request)


@router.post("/cybersecurity-strategic-analysis", response_model=MultiDomainStrategicResponse)
async def cybersecurity_strategic_analysis(request: MultiDomainStrategicRequest):
    """
    Perform strategic analysis specifically for cybersecurity domain.
    This is a convenience endpoint that automatically sets the domain to cybersecurity.
    """
    # Override domain to cybersecurity
    request.domain = "cybersecurity"
    return await multi_domain_strategic_analysis(request)


@router.post("/geopolitical-strategic-analysis", response_model=MultiDomainStrategicResponse)
async def geopolitical_strategic_analysis(request: MultiDomainStrategicRequest):
    """
    Perform strategic analysis specifically for geopolitical domain.
    This is a convenience endpoint that automatically sets the domain to geopolitical.
    """
    # Override domain to geopolitical
    request.domain = "geopolitical"
    return await multi_domain_strategic_analysis(request)


@router.get("/health")
async def multi_domain_health_check():
    """Health check for multi-domain strategic analysis service."""
    try:
        # Test basic functionality
        domains = await analyzer.get_supported_domains()
        return {
            "status": "healthy",
            "service": "multi_domain_strategic_analysis",
            "supported_domains": len(domains),
            "domains": [d["domain"] for d in domains],
            "analysis_types": [at.value for at in AnalysisType],
            "art_of_war_integration": True
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "multi_domain_strategic_analysis",
            "error": str(e)
        }
