"""
Phase 5: Model Interpretability & Explainable AI API Routes
Advanced forecasting & prediction system for DoD/Intelligence Community
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from loguru import logger

from src.core.interpretability.model_interpretability_engine import ModelInterpretabilityEngine
from src.core.interpretability.intelligence_explanations import IntelligenceExplanations

# Initialize router
router = APIRouter(prefix="/ml-forecasting/phase5", tags=["Phase 5: Model Interpretability & Explainable AI"])

# Initialize engines
model_interpretability_engine = ModelInterpretabilityEngine()
intelligence_explanations_engine = IntelligenceExplanations()

# Request models
class ModelExplanationRequest(BaseModel):
    """Request model for model explanation"""
    model_output: Dict[str, Any] = Field(..., description="Model output to explain")
    input_data: Dict[str, Any] = Field(..., description="Input data used for prediction")
    explanation_type: str = Field(default="comprehensive", description="Type of explanation to generate")
    include_feature_importance: bool = Field(default=True, description="Include feature importance analysis")
    include_decision_paths: bool = Field(default=True, description="Include decision paths")
    include_uncertainty: bool = Field(default=True, description="Include uncertainty analysis")


class IntelligenceExplanationRequest(BaseModel):
    """Request model for intelligence explanation"""
    analysis_type: str = Field(..., description="Type of intelligence analysis")
    analysis_results: Dict[str, Any] = Field(..., description="Analysis results to explain")
    explanation_domain: Optional[str] = Field(default=None, description="Specific intelligence domain")
    include_executive_summary: bool = Field(default=True, description="Include executive summary")


class ThreatExplanationRequest(BaseModel):
    """Request model for threat explanation"""
    threat_analysis: Dict[str, Any] = Field(..., description="Threat analysis results")
    include_mitigation_strategies: bool = Field(default=True, description="Include mitigation strategies")
    include_timeline: bool = Field(default=True, description="Include threat timeline")
    include_escalation_factors: bool = Field(default=True, description="Include escalation factors")


class CapabilityExplanationRequest(BaseModel):
    """Request model for capability explanation"""
    capability_results: Dict[str, Any] = Field(..., description="Capability analysis results")
    include_competitive_analysis: bool = Field(default=True, description="Include competitive analysis")
    include_improvement_areas: bool = Field(default=True, description="Include improvement areas")


class ExecutiveSummaryRequest(BaseModel):
    """Request model for executive summary"""
    detailed_analysis: Dict[str, Any] = Field(..., description="Detailed analysis results")
    summary_type: str = Field(default="intelligence", description="Type of executive summary")
    include_recommendations: bool = Field(default=True, description="Include recommendations")
    include_risk_assessment: bool = Field(default=True, description="Include risk assessment")


# Response models
class ModelExplanationResponse(BaseModel):
    """Response model for model explanation"""
    success: bool
    explanation: Dict[str, Any]
    model_name: str
    confidence: float
    feature_importance: List[Dict[str, Any]]
    decision_paths: List[Dict[str, Any]]
    key_factors: List[str]
    uncertainty_analysis: Dict[str, Any]
    recommendations: List[str]
    timestamp: str


class IntelligenceExplanationResponse(BaseModel):
    """Response model for intelligence explanation"""
    success: bool
    explanation: Dict[str, Any]
    analysis_type: str
    key_insights: List[str]
    confidence_factors: List[str]
    recommendations: List[str]
    risk_assessment: str
    next_steps: List[str]
    timestamp: str


class ThreatExplanationResponse(BaseModel):
    """Response model for threat explanation"""
    success: bool
    threat_level: str
    threat_type: str
    confidence: float
    key_indicators: List[str]
    mitigation_strategies: List[str]
    timeline: str
    escalation_factors: List[str]
    timestamp: str


class CapabilityExplanationResponse(BaseModel):
    """Response model for capability explanation"""
    success: bool
    capability_score: float
    capability_domains: List[str]
    strengths: List[str]
    weaknesses: List[str]
    improvement_areas: List[str]
    competitive_analysis: Dict[str, Any]
    timestamp: str


class ExecutiveSummaryResponse(BaseModel):
    """Response model for executive summary"""
    success: bool
    executive_summary: Dict[str, Any]
    key_findings: List[str]
    critical_recommendations: List[str]
    confidence_level: float
    risk_assessment: str
    next_steps: List[str]
    intelligence_priority: str
    timestamp: str


# API Endpoints

@router.post("/explain-model-predictions", response_model=ModelExplanationResponse)
async def explain_model_predictions(request: ModelExplanationRequest):
    """Explain model predictions for decision-makers"""
    try:
        logger.info("🔍 Explaining model predictions")
        
        # Generate comprehensive explanation
        explanation = await model_interpretability_engine.explain_predictions(
            request.model_output, 
            request.input_data
        )
        
        # Convert to response format
        response = ModelExplanationResponse(
            success=True,
            explanation=explanation.__dict__,
            model_name=explanation.model_name,
            confidence=explanation.confidence,
            feature_importance=[fi.__dict__ for fi in explanation.feature_importance],
            decision_paths=[dp.__dict__ for dp in explanation.decision_paths],
            key_factors=explanation.key_factors,
            uncertainty_analysis=explanation.uncertainty_analysis,
            recommendations=explanation.recommendations,
            timestamp=explanation.timestamp.isoformat()
        )
        
        logger.info(f"✅ Generated model explanation for {explanation.model_name}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error explaining model predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Error explaining model predictions: {str(e)}")


@router.post("/explain-intelligence-analysis", response_model=IntelligenceExplanationResponse)
async def explain_intelligence_analysis(request: IntelligenceExplanationRequest):
    """Explain intelligence-specific analysis results"""
    try:
        logger.info(f"🔍 Explaining {request.analysis_type} intelligence analysis")
        
        # Generate intelligence explanation
        explanation = await intelligence_explanations_engine.explain_intelligence_analysis(
            request.analysis_type,
            request.analysis_results
        )
        
        # Convert to response format
        response = IntelligenceExplanationResponse(
            success=True,
            explanation=explanation,
            analysis_type=request.analysis_type,
            key_insights=explanation.get('key_insights', []),
            confidence_factors=explanation.get('confidence_factors', []),
            recommendations=explanation.get('recommendations', []),
            risk_assessment=explanation.get('risk_assessment', 'unknown'),
            next_steps=explanation.get('next_steps', []),
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✅ Generated {request.analysis_type} intelligence explanation")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error explaining intelligence analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error explaining intelligence analysis: {str(e)}")


@router.post("/explain-threat-assessment", response_model=ThreatExplanationResponse)
async def explain_threat_assessment(request: ThreatExplanationRequest):
    """Explain threat assessment results"""
    try:
        logger.info("🔍 Explaining threat assessment")
        
        # Generate threat explanation
        threat_explanation = await intelligence_explanations_engine.explain_threat_assessment(
            request.threat_analysis
        )
        
        # Convert to response format
        response = ThreatExplanationResponse(
            success=True,
            threat_level=threat_explanation.threat_level,
            threat_type=threat_explanation.threat_type,
            confidence=threat_explanation.confidence,
            key_indicators=threat_explanation.key_indicators,
            mitigation_strategies=threat_explanation.mitigation_strategies,
            timeline=threat_explanation.timeline,
            escalation_factors=threat_explanation.escalation_factors,
            timestamp=threat_explanation.timestamp.isoformat()
        )
        
        logger.info(f"✅ Generated threat assessment explanation for {threat_explanation.threat_type}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error explaining threat assessment: {e}")
        raise HTTPException(status_code=500, detail=f"Error explaining threat assessment: {str(e)}")


@router.post("/explain-capability-analysis", response_model=CapabilityExplanationResponse)
async def explain_capability_analysis(request: CapabilityExplanationRequest):
    """Explain capability analysis results"""
    try:
        logger.info("🔍 Explaining capability analysis")
        
        # Generate capability explanation
        capability_explanation = await intelligence_explanations_engine.explain_capability_analysis(
            request.capability_results
        )
        
        # Convert to response format
        response = CapabilityExplanationResponse(
            success=True,
            capability_score=capability_explanation.capability_score,
            capability_domains=capability_explanation.capability_domains,
            strengths=capability_explanation.strengths,
            weaknesses=capability_explanation.weaknesses,
            improvement_areas=capability_explanation.improvement_areas,
            competitive_analysis=capability_explanation.competitive_analysis,
            timestamp=capability_explanation.timestamp.isoformat()
        )
        
        logger.info("✅ Generated capability analysis explanation")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error explaining capability analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error explaining capability analysis: {str(e)}")


@router.post("/generate-executive-summary", response_model=ExecutiveSummaryResponse)
async def generate_executive_summary(request: ExecutiveSummaryRequest):
    """Generate executive summary for decision-makers"""
    try:
        logger.info("📋 Generating executive summary")
        
        # Generate executive summary
        if request.summary_type == "intelligence":
            summary = await intelligence_explanations_engine.generate_executive_summary(
                request.detailed_analysis
            )
        else:
            summary = await model_interpretability_engine.generate_executive_summary(
                request.detailed_analysis
            )
        
        # Extract summary components
        executive_summary = summary.get('intelligence_executive_summary', summary.get('executive_summary', {}))
        
        # Convert to response format
        response = ExecutiveSummaryResponse(
            success=True,
            executive_summary=summary,
            key_findings=executive_summary.get('key_findings', []),
            critical_recommendations=executive_summary.get('critical_recommendations', []),
            confidence_level=executive_summary.get('confidence_level', 0.5),
            risk_assessment=executive_summary.get('risk_assessment', 'unknown'),
            next_steps=executive_summary.get('next_steps', []),
            intelligence_priority=executive_summary.get('intelligence_priority', 'medium'),
            timestamp=executive_summary.get('timestamp', datetime.now().isoformat())
        )
        
        logger.info("✅ Generated executive summary")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error generating executive summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating executive summary: {str(e)}")


@router.post("/explain-intelligence-domain")
async def explain_intelligence_domain(domain: str, analysis_results: Dict[str, Any]):
    """Explain intelligence analysis for specific domain"""
    try:
        logger.info(f"🔍 Explaining {domain} intelligence domain")
        
        # Generate domain-specific explanation
        explanation = await intelligence_explanations_engine.explain_intelligence_domain(
            domain,
            analysis_results
        )
        
        # Convert to response format
        response = {
            "success": True,
            "domain": domain,
            "analysis_type": explanation.analysis_type,
            "key_insights": explanation.key_insights,
            "confidence_factors": explanation.confidence_factors,
            "recommendations": explanation.recommendations,
            "risk_assessment": explanation.risk_assessment,
            "next_steps": explanation.next_steps,
            "timestamp": explanation.timestamp.isoformat()
        }
        
        logger.info(f"✅ Generated {domain} intelligence domain explanation")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error explaining {domain} intelligence domain: {e}")
        raise HTTPException(status_code=500, detail=f"Error explaining intelligence domain: {str(e)}")


@router.post("/generate-feature-importance")
async def generate_feature_importance(model_output: Dict[str, Any], data: Dict[str, Any]):
    """Generate feature importance analysis"""
    try:
        logger.info("🔍 Generating feature importance analysis")
        
        # Generate feature importance
        feature_importance = await model_interpretability_engine.generate_feature_importance(
            model_output,
            data
        )
        
        # Convert to response format
        response = {
            "success": True,
            "feature_importance": [fi.__dict__ for fi in feature_importance],
            "total_features": len(feature_importance),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Generated feature importance for {len(feature_importance)} features")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error generating feature importance: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating feature importance: {str(e)}")


@router.post("/create-decision-paths")
async def create_decision_paths(model_output: Dict[str, Any], data: Dict[str, Any]):
    """Create decision paths for complex models"""
    try:
        logger.info("🔍 Creating decision paths")
        
        # Generate decision paths
        decision_paths = await model_interpretability_engine.create_decision_paths(
            model_output,
            data
        )
        
        # Convert to response format
        response = {
            "success": True,
            "decision_paths": [dp.__dict__ for dp in decision_paths],
            "total_paths": len(decision_paths),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Created {len(decision_paths)} decision paths")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error creating decision paths: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating decision paths: {str(e)}")


@router.get("/health")
async def phase5_health_check():
    """Health check for Phase 5 components"""
    try:
        logger.info("🏥 Phase 5 health check")
        
        # Check component availability
        health_status = {
            "phase": "Phase 5: Model Interpretability & Explainable AI",
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "model_interpretability_engine": "available",
                "intelligence_explanations_engine": "available"
            },
            "endpoints": [
                "/ml-forecasting/phase5/explain-model-predictions",
                "/ml-forecasting/phase5/explain-intelligence-analysis",
                "/ml-forecasting/phase5/explain-threat-assessment",
                "/ml-forecasting/phase5/explain-capability-analysis",
                "/ml-forecasting/phase5/generate-executive-summary",
                "/ml-forecasting/phase5/explain-intelligence-domain",
                "/ml-forecasting/phase5/generate-feature-importance",
                "/ml-forecasting/phase5/create-decision-paths",
                "/ml-forecasting/phase5/health"
            ],
            "capabilities": [
                "Model prediction explanation",
                "Intelligence analysis explanation",
                "Threat assessment explanation",
                "Capability analysis explanation",
                "Executive summary generation",
                "Feature importance analysis",
                "Decision path creation",
                "Uncertainty analysis",
                "Risk assessment",
                "Recommendation generation"
            ]
        }
        
        logger.info("✅ Phase 5 health check completed")
        return health_status
        
    except Exception as e:
        logger.error(f"❌ Phase 5 health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Phase 5 health check failed: {str(e)}")


@router.get("/status")
async def phase5_status():
    """Get Phase 5 component status"""
    try:
        logger.info("📊 Phase 5 status check")
        
        status = {
            "phase": "Phase 5: Model Interpretability & Explainable AI",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "implementation_status": "completed",
            "components": {
                "model_interpretability_engine": {
                    "status": "operational",
                    "methods": [
                        "explain_predictions",
                        "generate_feature_importance",
                        "create_decision_paths",
                        "explain_intelligence_analysis",
                        "generate_executive_summary"
                    ]
                },
                "intelligence_explanations_engine": {
                    "status": "operational",
                    "methods": [
                        "explain_threat_assessment",
                        "explain_capability_analysis",
                        "explain_intelligence_domain",
                        "generate_executive_summary"
                    ]
                }
            },
            "api_endpoints": 9,
            "explanation_types": [
                "model_predictions",
                "intelligence_analysis",
                "threat_assessment",
                "capability_analysis",
                "executive_summary",
                "intelligence_domains",
                "feature_importance",
                "decision_paths"
            ],
            "intelligence_domains": [
                "military",
                "economic",
                "political",
                "social",
                "technological",
                "geographic"
            ]
        }
        
        logger.info("✅ Phase 5 status check completed")
        return status
        
    except Exception as e:
        logger.error(f"❌ Phase 5 status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Phase 5 status check failed: {str(e)}")
