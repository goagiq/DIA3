"""
Phase 5: Model Interpretability & Explainable AI MCP Tools
Advanced forecasting & prediction system for DoD/Intelligence Community
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger

from src.core.interpretability.model_interpretability_engine import ModelInterpretabilityEngine
from src.core.interpretability.intelligence_explanations import IntelligenceExplanations


class Phase5InterpretabilityMCPTools:
    """Phase 5 MCP tools for Model Interpretability & Explainable AI"""
    
    def __init__(self):
        """Initialize Phase 5 MCP tools"""
        self.model_interpretability_engine = ModelInterpretabilityEngine()
        self.intelligence_explanations_engine = IntelligenceExplanations()
        
        logger.info("✅ Phase 5 Interpretability MCP Tools initialized")
    
    async def explain_model_predictions_tool(self, model_output: str, input_data: str, explanation_type: str = "comprehensive") -> str:
        """Explain model predictions for decision-makers"""
        try:
            logger.info("🔍 MCP Tool: Explaining model predictions")
            
            # Parse input data
            model_output_dict = json.loads(model_output) if isinstance(model_output, str) else model_output
            input_data_dict = json.loads(input_data) if isinstance(input_data, str) else input_data
            
            # Generate explanation
            explanation = await self.model_interpretability_engine.explain_predictions(
                model_output_dict,
                input_data_dict
            )
            
            # Convert to JSON string
            result = {
                "success": True,
                "model_name": explanation.model_name,
                "confidence": explanation.confidence,
                "feature_importance": [fi.__dict__ for fi in explanation.feature_importance],
                "decision_paths": [dp.__dict__ for dp in explanation.decision_paths],
                "key_factors": explanation.key_factors,
                "uncertainty_analysis": explanation.uncertainty_analysis,
                "recommendations": explanation.recommendations,
                "timestamp": explanation.timestamp.isoformat()
            }
            
            logger.info(f"✅ MCP Tool: Generated model explanation for {explanation.model_name}")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error explaining model predictions: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def explain_intelligence_analysis_tool(self, analysis_type: str, analysis_results: str) -> str:
        """Explain intelligence-specific analysis results"""
        try:
            logger.info(f"🔍 MCP Tool: Explaining {analysis_type} intelligence analysis")
            
            # Parse input data
            analysis_results_dict = json.loads(analysis_results) if isinstance(analysis_results, str) else analysis_results
            
            # Generate explanation
            explanation = await self.intelligence_explanations_engine.explain_intelligence_analysis(
                analysis_type,
                analysis_results_dict
            )
            
            # Convert to JSON string
            result = {
                "success": True,
                "analysis_type": analysis_type,
                "explanation": explanation,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ MCP Tool: Generated {analysis_type} intelligence explanation")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error explaining intelligence analysis: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def explain_threat_assessment_tool(self, threat_analysis: str) -> str:
        """Explain threat assessment results"""
        try:
            logger.info("🔍 MCP Tool: Explaining threat assessment")
            
            # Parse input data
            threat_analysis_dict = json.loads(threat_analysis) if isinstance(threat_analysis, str) else threat_analysis
            
            # Generate explanation
            threat_explanation = await self.intelligence_explanations_engine.explain_threat_assessment(
                threat_analysis_dict
            )
            
            # Convert to JSON string
            result = {
                "success": True,
                "threat_level": threat_explanation.threat_level,
                "threat_type": threat_explanation.threat_type,
                "confidence": threat_explanation.confidence,
                "key_indicators": threat_explanation.key_indicators,
                "mitigation_strategies": threat_explanation.mitigation_strategies,
                "timeline": threat_explanation.timeline,
                "escalation_factors": threat_explanation.escalation_factors,
                "timestamp": threat_explanation.timestamp.isoformat()
            }
            
            logger.info(f"✅ MCP Tool: Generated threat assessment explanation for {threat_explanation.threat_type}")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error explaining threat assessment: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def explain_capability_analysis_tool(self, capability_results: str) -> str:
        """Explain capability analysis results"""
        try:
            logger.info("🔍 MCP Tool: Explaining capability analysis")
            
            # Parse input data
            capability_results_dict = json.loads(capability_results) if isinstance(capability_results, str) else capability_results
            
            # Generate explanation
            capability_explanation = await self.intelligence_explanations_engine.explain_capability_analysis(
                capability_results_dict
            )
            
            # Convert to JSON string
            result = {
                "success": True,
                "capability_score": capability_explanation.capability_score,
                "capability_domains": capability_explanation.capability_domains,
                "strengths": capability_explanation.strengths,
                "weaknesses": capability_explanation.weaknesses,
                "improvement_areas": capability_explanation.improvement_areas,
                "competitive_analysis": capability_explanation.competitive_analysis,
                "timestamp": capability_explanation.timestamp.isoformat()
            }
            
            logger.info("✅ MCP Tool: Generated capability analysis explanation")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error explaining capability analysis: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def generate_executive_summary_tool(self, detailed_analysis: str, summary_type: str = "intelligence") -> str:
        """Generate executive summary for decision-makers"""
        try:
            logger.info("📋 MCP Tool: Generating executive summary")
            
            # Parse input data
            detailed_analysis_dict = json.loads(detailed_analysis) if isinstance(detailed_analysis, str) else detailed_analysis
            
            # Generate executive summary
            if summary_type == "intelligence":
                summary = await self.intelligence_explanations_engine.generate_executive_summary(
                    detailed_analysis_dict
                )
            else:
                summary = await self.model_interpretability_engine.generate_executive_summary(
                    detailed_analysis_dict
                )
            
            # Convert to JSON string
            result = {
                "success": True,
                "summary_type": summary_type,
                "executive_summary": summary,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ MCP Tool: Generated executive summary")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error generating executive summary: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def explain_intelligence_domain_tool(self, domain: str, analysis_results: str) -> str:
        """Explain intelligence analysis for specific domain"""
        try:
            logger.info(f"🔍 MCP Tool: Explaining {domain} intelligence domain")
            
            # Parse input data
            analysis_results_dict = json.loads(analysis_results) if isinstance(analysis_results, str) else analysis_results
            
            # Generate domain-specific explanation
            explanation = await self.intelligence_explanations_engine.explain_intelligence_domain(
                domain,
                analysis_results_dict
            )
            
            # Convert to JSON string
            result = {
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
            
            logger.info(f"✅ MCP Tool: Generated {domain} intelligence domain explanation")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error explaining {domain} intelligence domain: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def generate_feature_importance_tool(self, model_output: str, data: str) -> str:
        """Generate feature importance analysis"""
        try:
            logger.info("🔍 MCP Tool: Generating feature importance analysis")
            
            # Parse input data
            model_output_dict = json.loads(model_output) if isinstance(model_output, str) else model_output
            data_dict = json.loads(data) if isinstance(data, str) else data
            
            # Generate feature importance
            feature_importance = await self.model_interpretability_engine.generate_feature_importance(
                model_output_dict,
                data_dict
            )
            
            # Convert to JSON string
            result = {
                "success": True,
                "feature_importance": [fi.__dict__ for fi in feature_importance],
                "total_features": len(feature_importance),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ MCP Tool: Generated feature importance for {len(feature_importance)} features")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error generating feature importance: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def create_decision_paths_tool(self, model_output: str, data: str) -> str:
        """Create decision paths for complex models"""
        try:
            logger.info("🔍 MCP Tool: Creating decision paths")
            
            # Parse input data
            model_output_dict = json.loads(model_output) if isinstance(model_output, str) else model_output
            data_dict = json.loads(data) if isinstance(data, str) else data
            
            # Generate decision paths
            decision_paths = await self.model_interpretability_engine.create_decision_paths(
                model_output_dict,
                data_dict
            )
            
            # Convert to JSON string
            result = {
                "success": True,
                "decision_paths": [dp.__dict__ for dp in decision_paths],
                "total_paths": len(decision_paths),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ MCP Tool: Created {len(decision_paths)} decision paths")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Error creating decision paths: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def phase5_health_check_tool(self) -> str:
        """Health check for Phase 5 components"""
        try:
            logger.info("🏥 MCP Tool: Phase 5 health check")
            
            # Check component availability
            health_status = {
                "phase": "Phase 5: Model Interpretability & Explainable AI",
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "model_interpretability_engine": "available",
                    "intelligence_explanations_engine": "available"
                },
                "mcp_tools": [
                    "explain_model_predictions_tool",
                    "explain_intelligence_analysis_tool",
                    "explain_threat_assessment_tool",
                    "explain_capability_analysis_tool",
                    "generate_executive_summary_tool",
                    "explain_intelligence_domain_tool",
                    "generate_feature_importance_tool",
                    "create_decision_paths_tool",
                    "phase5_health_check_tool"
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
            
            logger.info("✅ MCP Tool: Phase 5 health check completed")
            return json.dumps(health_status, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Phase 5 health check failed: {e}")
            return json.dumps({"error": str(e), "success": False})
    
    async def phase5_status_tool(self) -> str:
        """Get Phase 5 component status"""
        try:
            logger.info("📊 MCP Tool: Phase 5 status check")
            
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
                "mcp_tools": 9,
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
            
            logger.info("✅ MCP Tool: Phase 5 status check completed")
            return json.dumps(status, indent=2)
            
        except Exception as e:
            logger.error(f"❌ MCP Tool: Phase 5 status check failed: {e}")
            return json.dumps({"error": str(e), "success": False})


# Create instance for MCP server integration
phase5_interpretability_mcp_tools = Phase5InterpretabilityMCPTools()
