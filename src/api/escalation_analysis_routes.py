"""
API routes for escalation analysis functionality.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from loguru import logger

from src.agents.escalation_analysis_agent import (
    EscalationAnalysisAgent,
    EscalationAnalysisRequest,
    EscalationAnalysisResult
)

# Create router
router = APIRouter(prefix="/escalation-analysis", tags=["escalation-analysis"])

# Global agent instance
escalation_agent: Optional[EscalationAnalysisAgent] = None


def get_escalation_agent() -> EscalationAnalysisAgent:
    """Get escalation analysis agent instance."""
    global escalation_agent
    if escalation_agent is None:
        escalation_agent = EscalationAnalysisAgent()
    return escalation_agent


class EscalationAnalysisResponse(BaseModel):
    """Response model for escalation analysis."""
    success: bool = Field(..., description="Analysis success status")
    analysis_id: str = Field(..., description="Unique analysis identifier")
    domain: str = Field(..., description="Analysis domain")
    risk_assessment: Dict[str, Any] = Field(..., description="Risk assessment results")
    escalation_scenarios: List[Dict[str, Any]] = Field(..., description="Escalation scenarios")
    warning_indicators: Dict[str, List[str]] = Field(..., description="Warning indicators")
    confidence_score: float = Field(..., description="Analysis confidence score")
    timestamp: str = Field(..., description="Analysis timestamp")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    domains_supported: List[str] = Field(..., description="Supported domains")
    agent_available: bool = Field(..., description="Agent availability")


class DomainSpecificAnalysisRequest(BaseModel):
    """Request model for domain-specific escalation analysis (domain is set automatically)."""
    content: str = Field(..., description="Content to analyze for escalation patterns")
    secondary_domains: Optional[List[str]] = Field(default=None, description="Additional domains to consider")
    analysis_depth: str = Field(default="comprehensive", description="Analysis depth (basic, standard, comprehensive)")
    include_historical_patterns: bool = Field(default=True, description="Include historical pattern analysis")
    include_warning_indicators: bool = Field(default=True, description="Include warning indicators")
    include_mitigation_strategies: bool = Field(default=True, description="Include mitigation strategies")
    custom_frameworks: Optional[List[str]] = Field(default=None, description="Custom analysis frameworks to apply")


@router.post("/analyze", response_model=EscalationAnalysisResponse)
async def analyze_escalation_patterns(
    request: EscalationAnalysisRequest,
    agent: EscalationAnalysisAgent = Depends(get_escalation_agent)
) -> EscalationAnalysisResponse:
    """
    Analyze content for escalation patterns using domain-specific frameworks.
    
    This endpoint provides comprehensive escalation analysis across multiple domains
    including defense, intelligence, business, cybersecurity, and geopolitical contexts.
    """
    try:
        logger.info(f"Starting escalation analysis for domain: {request.domain}")
        
        # Perform escalation analysis
        result = await agent.analyze_escalation_patterns(
            content=request.content,
            domain=request.domain,
            secondary_domains=request.secondary_domains,
            analysis_depth=request.analysis_depth
        )
        
        # Convert scenarios to dict format for response
        scenarios = [scenario.dict() for scenario in result.escalation_scenarios]
        
        response = EscalationAnalysisResponse(
            success=True,
            analysis_id=result.analysis_id,
            domain=result.domain,
            risk_assessment=result.risk_assessment,
            escalation_scenarios=scenarios,
            warning_indicators=result.warning_indicators,
            confidence_score=result.confidence_score,
            timestamp=result.timestamp.isoformat()
        )
        
        logger.info(f"✅ Escalation analysis completed: {result.analysis_id}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error in escalation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-defense")
async def analyze_defense_escalation(
    request: DomainSpecificAnalysisRequest,
    agent: EscalationAnalysisAgent = Depends(get_escalation_agent)
) -> EscalationAnalysisResponse:
    """
    Analyze defense domain escalation patterns.
    
    Focuses on military escalation, alliance conflicts, territorial disputes,
    arms competition, and strategic encirclement scenarios.
    """
    try:
        logger.info("Starting defense domain escalation analysis")
        
        # Create full request with domain set to defense
        full_request = EscalationAnalysisRequest(
            content=request.content,
            domain="defense",
            secondary_domains=request.secondary_domains,
            analysis_depth=request.analysis_depth,
            include_historical_patterns=request.include_historical_patterns,
            include_warning_indicators=request.include_warning_indicators,
            include_mitigation_strategies=request.include_mitigation_strategies,
            custom_frameworks=request.custom_frameworks
        )
        
        return await analyze_escalation_patterns(full_request, agent)
        
    except Exception as e:
        logger.error(f"❌ Error in defense escalation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-intelligence")
async def analyze_intelligence_escalation(
    request: DomainSpecificAnalysisRequest,
    agent: EscalationAnalysisAgent = Depends(get_escalation_agent)
) -> EscalationAnalysisResponse:
    """
    Analyze intelligence domain escalation patterns.
    
    Focuses on cyber espionage, disinformation campaigns, human intelligence
    operations, technical intelligence gathering, and counterintelligence operations.
    """
    try:
        logger.info("Starting intelligence domain escalation analysis")
        
        # Create full request with domain set to intelligence
        full_request = EscalationAnalysisRequest(
            content=request.content,
            domain="intelligence",
            secondary_domains=request.secondary_domains,
            analysis_depth=request.analysis_depth,
            include_historical_patterns=request.include_historical_patterns,
            include_warning_indicators=request.include_warning_indicators,
            include_mitigation_strategies=request.include_mitigation_strategies,
            custom_frameworks=request.custom_frameworks
        )
        
        return await analyze_escalation_patterns(full_request, agent)
        
    except Exception as e:
        logger.error(f"❌ Error in intelligence escalation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-business")
async def analyze_business_escalation(
    request: DomainSpecificAnalysisRequest,
    agent: EscalationAnalysisAgent = Depends(get_escalation_agent)
) -> EscalationAnalysisResponse:
    """
    Analyze business domain escalation patterns.
    
    Focuses on price wars, regulatory conflicts, market manipulation,
    resource competition, and alliance formation scenarios.
    """
    try:
        logger.info("Starting business domain escalation analysis")
        
        # Create full request with domain set to business
        full_request = EscalationAnalysisRequest(
            content=request.content,
            domain="business",
            secondary_domains=request.secondary_domains,
            analysis_depth=request.analysis_depth,
            include_historical_patterns=request.include_historical_patterns,
            include_warning_indicators=request.include_warning_indicators,
            include_mitigation_strategies=request.include_mitigation_strategies,
            custom_frameworks=request.custom_frameworks
        )
        
        return await analyze_escalation_patterns(full_request, agent)
        
    except Exception as e:
        logger.error(f"❌ Error in business escalation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-cybersecurity")
async def analyze_cybersecurity_escalation(
    request: DomainSpecificAnalysisRequest,
    agent: EscalationAnalysisAgent = Depends(get_escalation_agent)
) -> EscalationAnalysisResponse:
    """
    Analyze cybersecurity domain escalation patterns.
    
    Focuses on cyber attacks, information warfare, infrastructure disruption,
    data breaches, and attribution conflicts.
    """
    try:
        logger.info("Starting cybersecurity domain escalation analysis")
        
        # Create full request with domain set to cybersecurity
        full_request = EscalationAnalysisRequest(
            content=request.content,
            domain="cybersecurity",
            secondary_domains=request.secondary_domains,
            analysis_depth=request.analysis_depth,
            include_historical_patterns=request.include_historical_patterns,
            include_warning_indicators=request.include_warning_indicators,
            include_mitigation_strategies=request.include_mitigation_strategies,
            custom_frameworks=request.custom_frameworks
        )
        
        return await analyze_escalation_patterns(full_request, agent)
        
    except Exception as e:
        logger.error(f"❌ Error in cybersecurity escalation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-geopolitical")
async def analyze_geopolitical_escalation(
    request: DomainSpecificAnalysisRequest,
    agent: EscalationAnalysisAgent = Depends(get_escalation_agent)
) -> EscalationAnalysisResponse:
    """
    Analyze geopolitical domain escalation patterns.
    
    Focuses on diplomatic conflicts, economic sanctions, territorial disputes,
    alliance formation, and cultural conflicts.
    """
    try:
        logger.info("Starting geopolitical domain escalation analysis")
        
        # Create full request with domain set to geopolitical
        full_request = EscalationAnalysisRequest(
            content=request.content,
            domain="geopolitical",
            secondary_domains=request.secondary_domains,
            analysis_depth=request.analysis_depth,
            include_historical_patterns=request.include_historical_patterns,
            include_warning_indicators=request.include_warning_indicators,
            include_mitigation_strategies=request.include_mitigation_strategies,
            custom_frameworks=request.custom_frameworks
        )
        
        return await analyze_escalation_patterns(full_request, agent)
        
    except Exception as e:
        logger.error(f"❌ Error in geopolitical escalation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/domains")
async def get_supported_domains() -> Dict[str, Any]:
    """
    Get list of supported domains for escalation analysis.
    """
    try:
        agent = get_escalation_agent()
        domains = list(agent.domain_frameworks.keys())
        
        domain_info = {}
        for domain in domains:
            framework = agent.domain_frameworks[domain]
            domain_info[domain] = {
                "historical_patterns": framework["historical_patterns"],
                "escalation_types": framework["escalation_types"]
            }
        
        return {
            "success": True,
            "domains": domains,
            "domain_info": domain_info,
            "total_domains": len(domains)
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting supported domains: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historical-patterns")
async def get_historical_patterns() -> Dict[str, Any]:
    """
    Get available historical patterns for escalation analysis.
    """
    try:
        agent = get_escalation_agent()
        
        return {
            "success": True,
            "historical_patterns": agent.historical_patterns,
            "total_patterns": len(agent.historical_patterns)
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting historical patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check for escalation analysis service.
    """
    try:
        agent = get_escalation_agent()
        domains = list(agent.domain_frameworks.keys())
        
        return HealthResponse(
            status="healthy",
            service="escalation_analysis",
            domains_supported=domains,
            agent_available=True
        )
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            service="escalation_analysis",
            domains_supported=[],
            agent_available=False
        )


@router.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
    """
    Get escalation analysis capabilities and features.
    """
    try:
        agent = get_escalation_agent()
        
        capabilities = {
            "supported_domains": list(agent.domain_frameworks.keys()),
            "supported_data_types": [dt.value for dt in agent.supported_data_types],
            "analysis_depths": ["basic", "standard", "comprehensive"],
            "risk_levels": ["low", "medium", "high", "critical"],
            "timelines": ["immediate", "medium-term", "long-term"],
            "features": [
                "Historical pattern analysis",
                "Escalation scenario identification",
                "Risk assessment",
                "Warning indicator generation",
                "Mitigation strategy recommendations",
                "Cross-domain analysis",
                "Confidence scoring",
                "Pattern storage and retrieval"
            ]
        }
        
        return {
            "success": True,
            "capabilities": capabilities
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))
