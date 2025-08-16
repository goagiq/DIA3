"""
API routes for Language Capabilities Engine.

Provides endpoints for analyzing content using language capabilities
to identify strategic advantages across multiple domains.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from loguru import logger

from src.core.language_capabilities_engine import language_capabilities_engine

# Create router
router = APIRouter(prefix="/language-capabilities", tags=["Language Capabilities"])


class LanguageCapabilitiesRequest(BaseModel):
    """Request model for language capabilities analysis."""
    content: str = Field(..., description="Content to analyze")
    language: str = Field(default="auto", description="Language code or 'auto' for detection")
    domain: Optional[str] = Field(default=None, description="Specific domain to focus on (defense, intelligence, business, cybersecurity)")


class LanguageCapabilitiesResponse(BaseModel):
    """Response model for language capabilities analysis."""
    success: bool
    language: str
    language_name: str
    capabilities_identified: list
    strategic_advantages: list
    analysis_timestamp: str
    confidence_scores: Dict[str, float]
    domain_focus: Optional[str] = None


@router.post("/analyze", response_model=LanguageCapabilitiesResponse)
async def analyze_language_capabilities(request: LanguageCapabilitiesRequest):
    """
    Analyze content using language capabilities for strategic advantages.
    
    This endpoint analyzes content to identify:
    - Language-specific capabilities (HUMINT, deception detection, strategic analysis, cultural intelligence)
    - Strategic advantages across domains (defense, intelligence, business, cybersecurity)
    - Cultural indicators and patterns
    - Confidence scores for each capability
    """
    try:
        logger.info(f"Starting language capabilities analysis for language: {request.language}")
        
        # Perform analysis
        results = await language_capabilities_engine.analyze_language_capabilities(
            content=request.content,
            language=request.language
        )
        
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        
        # Filter by domain if specified
        if request.domain:
            filtered_advantages = [
                adv for adv in results.get("strategic_advantages", [])
                if adv.get("domain") == request.domain
            ]
            results["strategic_advantages"] = filtered_advantages
            results["domain_focus"] = request.domain
        
        return LanguageCapabilitiesResponse(
            success=True,
            language=results.get("language", "unknown"),
            language_name=results.get("language_name", "Unknown"),
            capabilities_identified=results.get("capabilities_identified", []),
            strategic_advantages=results.get("strategic_advantages", []),
            analysis_timestamp=results.get("analysis_timestamp", ""),
            confidence_scores=results.get("confidence_scores", {}),
            domain_focus=results.get("domain_focus")
        )
        
    except Exception as e:
        logger.error(f"Error in language capabilities analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/capabilities")
async def get_capabilities_summary():
    """
    Get a summary of all available language capabilities and strategic advantages.
    
    Returns:
    - Total capabilities and advantages
    - Supported languages
    - Capability types
    - Domains covered
    - Detailed breakdown by language and domain
    """
    try:
        summary = await language_capabilities_engine.get_capabilities_summary()
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error getting capabilities summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities summary: {str(e)}")


@router.get("/capabilities/{language}")
async def get_language_capabilities(language: str):
    """
    Get capabilities for a specific language.
    
    Args:
        language: Language code (zh, ru, ar, etc.)
    
    Returns:
        Detailed capabilities for the specified language
    """
    try:
        summary = await language_capabilities_engine.get_capabilities_summary()
        
        if language not in summary["capabilities_by_language"]:
            raise HTTPException(status_code=404, detail=f"Language {language} not supported")
        
        return {
            "success": True,
            "language": language,
            "capabilities": summary["capabilities_by_language"][language]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting language capabilities for {language}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get language capabilities: {str(e)}")


@router.get("/advantages/{domain}")
async def get_domain_advantages(domain: str):
    """
    Get strategic advantages for a specific domain.
    
    Args:
        domain: Domain name (defense, intelligence, business, cybersecurity)
    
    Returns:
        Strategic advantages for the specified domain
    """
    try:
        summary = await language_capabilities_engine.get_capabilities_summary()
        
        if domain not in summary["advantages_by_domain"]:
            raise HTTPException(status_code=404, detail=f"Domain {domain} not supported")
        
        return {
            "success": True,
            "domain": domain,
            "advantages": summary["advantages_by_domain"][domain]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting domain advantages for {domain}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get domain advantages: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check for the language capabilities engine.
    
    Returns:
        Health status of all components
    """
    try:
        health = await language_capabilities_engine.health_check()
        return {
            "success": True,
            "health": health
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "health": {
                "status": "unhealthy",
                "timestamp": "unknown"
            }
        }


# Domain-specific analysis endpoints

@router.post("/defense/analyze")
async def analyze_defense_capabilities(request: LanguageCapabilitiesRequest):
    """
    Analyze content for defense domain language capabilities.
    
    Focuses on:
    - HUMINT collection advantages
    - Strategic document analysis
    - Deception detection for counterintelligence
    """
    request.domain = "defense"
    return await analyze_language_capabilities(request)


@router.post("/intelligence/analyze")
async def analyze_intelligence_capabilities(request: LanguageCapabilitiesRequest):
    """
    Analyze content for intelligence domain language capabilities.
    
    Focuses on:
    - Cultural intelligence
    - Real-time analysis capabilities
    - Strategic intent analysis
    """
    request.domain = "intelligence"
    return await analyze_language_capabilities(request)


@router.post("/business/analyze")
async def analyze_business_capabilities(request: LanguageCapabilitiesRequest):
    """
    Analyze content for business domain language capabilities.
    
    Focuses on:
    - Market intelligence
    - Negotiation advantages
    - Cultural business practices
    """
    request.domain = "business"
    return await analyze_language_capabilities(request)


@router.post("/cybersecurity/analyze")
async def analyze_cybersecurity_capabilities(request: LanguageCapabilitiesRequest):
    """
    Analyze content for cybersecurity domain language capabilities.
    
    Focuses on:
    - Threat intelligence
    - Social engineering detection
    - Cyber deception recognition
    """
    request.domain = "cybersecurity"
    return await analyze_language_capabilities(request)


# Batch analysis endpoint

@router.post("/batch/analyze")
async def batch_analyze_language_capabilities(requests: list[LanguageCapabilitiesRequest]):
    """
    Perform batch analysis of multiple content items.
    
    Args:
        requests: List of analysis requests
    
    Returns:
        List of analysis results
    """
    try:
        results = []
        
        for i, request in enumerate(requests):
            try:
                result = await analyze_language_capabilities(request)
                results.append({
                    "index": i,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "index": i,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "total_requests": len(requests),
            "successful_analyses": len([r for r in results if r["success"]]),
            "failed_analyses": len([r for r in results if not r["success"]]),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


# Utility endpoints

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages."""
    try:
        summary = await language_capabilities_engine.get_capabilities_summary()
        return {
            "success": True,
            "supported_languages": summary["supported_languages"]
        }
    except Exception as e:
        logger.error(f"Error getting supported languages: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get supported languages: {str(e)}")


@router.get("/supported-domains")
async def get_supported_domains():
    """Get list of supported domains."""
    try:
        summary = await language_capabilities_engine.get_capabilities_summary()
        return {
            "success": True,
            "supported_domains": summary["domains"]
        }
    except Exception as e:
        logger.error(f"Error getting supported domains: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get supported domains: {str(e)}")


@router.get("/capability-types")
async def get_capability_types():
    """Get list of capability types."""
    try:
        summary = await language_capabilities_engine.get_capabilities_summary()
        return {
            "success": True,
            "capability_types": summary["capability_types"]
        }
    except Exception as e:
        logger.error(f"Error getting capability types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get capability types: {str(e)}")
