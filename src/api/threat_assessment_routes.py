"""
Threat Assessment API Routes

Comprehensive threat assessment endpoints with multi-domain support for:
- Defense and intelligence industry
- Business applications
- Cybersecurity
- Geopolitical analysis
- Critical infrastructure
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from loguru import logger

from src.core.models import AnalysisRequest, DataType
from src.agents.threat_assessment_agent import (
    ThreatAssessmentAgent, ThreatDomain, ThreatSeverity, ThreatType
)

# Global agent instance
threat_assessment_agent: Optional[ThreatAssessmentAgent] = None

# Pydantic models for API requests/responses
class ThreatAssessmentRequest(BaseModel):
    """Request model for threat assessment."""
    content: str = Field(..., description="Text content to analyze")
    domain: str = Field(default="intelligence", description="Domain for analysis")
    language: str = Field(default="en", description="Language of content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class ThreatAssessmentResponse(BaseModel):
    """Response model for threat assessment."""
    assessment_id: str
    timestamp: str
    overall_severity: str
    confidence: float
    summary: Dict[str, Any]
    indicators: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    patterns: List[Dict[str, Any]]
    domain_analysis: Dict[str, Any]
    recommendations: List[str]
    metadata: Dict[str, Any]

class BatchThreatAssessmentRequest(BaseModel):
    """Request model for batch threat assessment."""
    contents: List[str] = Field(..., description="List of text contents to analyze")
    domain: str = Field(default="intelligence", description="Domain for analysis")
    language: str = Field(default="en", description="Language of content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class BatchThreatAssessmentResponse(BaseModel):
    """Response model for batch threat assessment."""
    assessments: List[ThreatAssessmentResponse]
    summary: Dict[str, Any]

class ThreatAssessmentSummaryResponse(BaseModel):
    """Response model for threat assessment summary."""
    total_indicators: int
    total_warnings: int
    total_patterns: int
    domains_covered: List[str]
    severity_distribution: Dict[str, int]
    last_assessment: Optional[str]

# Create router
router = APIRouter(prefix="/threat-assessment", tags=["Threat Assessment"])

def get_threat_assessment_agent() -> ThreatAssessmentAgent:
    """Get or create threat assessment agent."""
    global threat_assessment_agent
    if threat_assessment_agent is None:
        threat_assessment_agent = ThreatAssessmentAgent()
    return threat_assessment_agent

@router.post("/analyze", response_model=ThreatAssessmentResponse)
async def analyze_threat_assessment(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """
    Perform comprehensive threat assessment analysis.
    
    Supports multiple domains:
    - defense: Military and defense-related threats
    - intelligence: Intelligence and espionage threats
    - business: Business and economic threats
    - cybersecurity: Cyber threats and attacks
    - geopolitical: Geopolitical and international threats
    - financial: Financial and market threats
    - healthcare: Healthcare and medical threats
    - energy: Energy and resource threats
    - transportation: Transportation and logistics threats
    - critical_infrastructure: Critical infrastructure threats
    """
    try:
        # Validate domain
        try:
            domain = ThreatDomain(request.domain)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain: {request.domain}. Valid domains: {[d.value for d in ThreatDomain]}"
            )
        
        # Create analysis request
        analysis_request = AnalysisRequest(
            id=f"threat_assessment_{datetime.now().timestamp()}",
            content=request.content,
            data_type=DataType.TEXT,
            metadata={
                "domain": domain.value,
                "language": request.language,
                **request.metadata
            }
        )
        
        # Process request
        result = await agent.process(analysis_request)
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        return ThreatAssessmentResponse(**result.result)
        
    except Exception as e:
        logger.error(f"Error in threat assessment analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-defense", response_model=ThreatAssessmentResponse)
async def analyze_defense_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze defense and military threats."""
    request.domain = "defense"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-intelligence", response_model=ThreatAssessmentResponse)
async def analyze_intelligence_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze intelligence and espionage threats."""
    request.domain = "intelligence"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-business", response_model=ThreatAssessmentResponse)
async def analyze_business_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze business and economic threats."""
    request.domain = "business"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-cybersecurity", response_model=ThreatAssessmentResponse)
async def analyze_cybersecurity_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze cybersecurity threats."""
    request.domain = "cybersecurity"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-geopolitical", response_model=ThreatAssessmentResponse)
async def analyze_geopolitical_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze geopolitical threats."""
    request.domain = "geopolitical"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-financial", response_model=ThreatAssessmentResponse)
async def analyze_financial_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze financial and market threats."""
    request.domain = "financial"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-healthcare", response_model=ThreatAssessmentResponse)
async def analyze_healthcare_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze healthcare and medical threats."""
    request.domain = "healthcare"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-energy", response_model=ThreatAssessmentResponse)
async def analyze_energy_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze energy and resource threats."""
    request.domain = "energy"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-transportation", response_model=ThreatAssessmentResponse)
async def analyze_transportation_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze transportation and logistics threats."""
    request.domain = "transportation"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-critical-infrastructure", response_model=ThreatAssessmentResponse)
async def analyze_critical_infrastructure_threats(
    request: ThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Analyze critical infrastructure threats."""
    request.domain = "critical_infrastructure"
    return await analyze_threat_assessment(request, agent)

@router.post("/analyze-batch", response_model=BatchThreatAssessmentResponse)
async def analyze_batch_threat_assessment(
    request: BatchThreatAssessmentRequest,
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Perform batch threat assessment analysis."""
    try:
        # Validate domain
        try:
            domain = ThreatDomain(request.domain)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid domain: {request.domain}. Valid domains: {[d.value for d in ThreatDomain]}"
            )
        
        assessments = []
        total_indicators = 0
        total_warnings = 0
        total_patterns = 0
        domains_covered = set()
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        # Process each content item
        for i, content in enumerate(request.contents):
            analysis_request = AnalysisRequest(
                id=f"batch_threat_assessment_{i}_{datetime.now().timestamp()}",
                content=content,
                data_type=DataType.TEXT,
                metadata={
                    "domain": domain.value,
                    "language": request.language,
                    "batch_index": i,
                    **request.metadata
                }
            )
            
            result = await agent.process(analysis_request)
            
            if result.success:
                assessment = ThreatAssessmentResponse(**result.result)
                assessments.append(assessment)
                
                # Update summary statistics
                total_indicators += assessment.summary["total_indicators"]
                total_warnings += assessment.summary["total_warnings"]
                total_patterns += assessment.summary["total_patterns"]
                domains_covered.update(assessment.summary["domains_affected"])
                
                # Update severity distribution
                for domain_analysis in assessment.domain_analysis.values():
                    for severity, count in domain_analysis["severity_distribution"].items():
                        severity_counts[severity] += count
            else:
                logger.warning(f"Failed to process batch item {i}: {result.error}")
        
        summary = {
            "total_assessments": len(assessments),
            "total_indicators": total_indicators,
            "total_warnings": total_warnings,
            "total_patterns": total_patterns,
            "domains_covered": list(domains_covered),
            "severity_distribution": severity_counts,
            "success_rate": len(assessments) / len(request.contents) if request.contents else 0
        }
        
        return BatchThreatAssessmentResponse(
            assessments=assessments,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error in batch threat assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", response_model=ThreatAssessmentSummaryResponse)
async def get_threat_assessment_summary(
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Get summary of all threat assessments."""
    try:
        summary = await agent.get_assessment_summary()
        return ThreatAssessmentSummaryResponse(**summary)
    except Exception as e:
        logger.error(f"Error getting threat assessment summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-data")
async def clear_threat_assessment_data(
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Clear all threat assessment data."""
    try:
        await agent.clear_assessment_data()
        return {"message": "Threat assessment data cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing threat assessment data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/domains")
async def get_supported_domains():
    """Get list of supported threat assessment domains."""
    return {
        "domains": [domain.value for domain in ThreatDomain],
        "descriptions": {
            "defense": "Military and defense-related threats",
            "intelligence": "Intelligence and espionage threats",
            "business": "Business and economic threats",
            "cybersecurity": "Cyber threats and attacks",
            "geopolitical": "Geopolitical and international threats",
            "financial": "Financial and market threats",
            "healthcare": "Healthcare and medical threats",
            "energy": "Energy and resource threats",
            "transportation": "Transportation and logistics threats",
            "critical_infrastructure": "Critical infrastructure threats"
        }
    }

@router.get("/capabilities")
async def get_threat_assessment_capabilities(
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Get threat assessment capabilities."""
    return {
        "capabilities": agent.metadata["capabilities"],
        "supported_data_types": agent.metadata["supported_data_types"],
        "supported_domains": agent.metadata["supported_domains"],
        "threat_types": [threat_type.value for threat_type in ThreatType],
        "severity_levels": [severity.value for severity in ThreatSeverity]
    }

@router.get("/health")
async def threat_assessment_health_check(
    agent: ThreatAssessmentAgent = Depends(get_threat_assessment_agent)
):
    """Health check for threat assessment service."""
    try:
        summary = await agent.get_assessment_summary()
        return {
            "status": "healthy",
            "service": "threat_assessment",
            "agent_initialized": agent is not None,
            "total_indicators": summary["total_indicators"],
            "total_warnings": summary["total_warnings"],
            "total_patterns": summary["total_patterns"],
            "domains_covered": summary["domains_covered"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Threat assessment health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "threat_assessment",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
