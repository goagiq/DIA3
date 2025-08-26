"""
Enhanced Decision Support Agent - Phase 2 Implementation
Integrates knowledge graph intelligence for advanced decision support.
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.agents.base_agent import StrandsBaseAgent
from src.core.models import AnalysisRequest, AnalysisResult, ProcessingStatus, SentimentResult
from src.core.decision_support import (
    RecommendationEngine,
    ActionPrioritizer,
    ImplementationPlanner,
    SuccessPredictor,
    RecommendationContext,
    PrioritizationContext,
    PlanningContext,
    PredictionContext
)
from src.core.decision_support.knowledge_graph_integrator import (
    KnowledgeGraphIntegrator,
    DecisionContext
)
from src.core.knowledge_graph_intelligence_service import (
    KnowledgeGraphIntelligenceService,
    StrategicIntelligence,
    QueryContext
)
from src.core.enhanced_strategic_analytics_engine import (
    EnhancedStrategicAnalyticsEngine,
    StrategicContext,
    StrategicMetrics,
    StrategicRecommendation,
    StrategicDomain
)
from src.config.decision_support_config import (
    get_decision_support_config,
    get_language_decision_config
)

logger = logging.getLogger(__name__)


class EnhancedDecisionSupportAgent(StrandsBaseAgent):
    """Enhanced AI-powered decision support agent with knowledge graph intelligence integration."""
    
    def __init__(self, agent_id: Optional[str] = None, model_name: str = "llama3.2:latest"):
        super().__init__(agent_id, max_capacity=5, model_name=model_name)
        
        # Initialize decision support components
        self.recommendation_engine = RecommendationEngine(model_name)
        self.action_prioritizer = ActionPrioritizer()
        self.implementation_planner = ImplementationPlanner()
        self.success_predictor = SuccessPredictor()
        
        # Initialize knowledge graph integrator
        self.knowledge_graph_integrator = KnowledgeGraphIntegrator()
        
        # Initialize knowledge graph intelligence service
        self.kg_intelligence_service = KnowledgeGraphIntelligenceService()
        
        # Initialize enhanced strategic analytics engine
        self.strategic_analytics_engine = EnhancedStrategicAnalyticsEngine()
        
        # Load configuration
        self.config = get_decision_support_config()
        
        logger.info(f"Initialized Enhanced DecisionSupportAgent: {self.agent_id}")
    
    def _get_tools(self) -> list:
        """Get tools for the decision support agent."""
        # Return empty list to avoid strands tool registration issues
        return []
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        # Decision support agent can handle decision-making and recommendation requests
        decision_keywords = [
            "decision", "recommendation", "strategy", "planning", "prioritization",
            "implementation", "success", "outcome", "analysis", "optimization",
            "knowledge graph", "intelligence", "strategic", "historical patterns"
        ]
        
        content = request.content.lower() if request.content else ""
        return any(keyword in content for keyword in decision_keywords)
    
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process the analysis request for decision support with knowledge graph intelligence."""
        try:
            logger.info(f"Processing enhanced decision support request: {request.id}")
            
            # Parse request content to determine analysis type
            analysis_type = await self._determine_analysis_type(request)
            
            if analysis_type == "comprehensive":
                result = await self._perform_comprehensive_analysis(request)
            elif analysis_type == "recommendations":
                result = await self._generate_recommendations_only(request)
            elif analysis_type == "prioritization":
                result = await self._prioritize_actions_only(request)
            elif analysis_type == "planning":
                result = await self._create_implementation_plan_only(request)
            elif analysis_type == "prediction":
                result = await self._predict_success_only(request)
            elif analysis_type == "strategic":
                result = await self._perform_strategic_analysis(request)
            elif analysis_type == "knowledge_graph":
                result = await self._perform_knowledge_graph_analysis(request)
            else:
                result = await self._perform_comprehensive_analysis(request)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing enhanced decision support request: {e}")
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                status=ProcessingStatus.FAILED,
                content=f"Error processing request: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _determine_analysis_type(self, request: AnalysisRequest) -> str:
        """Determine the type of analysis needed based on request content."""
        content = request.content.lower() if request.content else ""
        
        # Check for knowledge graph specific requests
        if any(keyword in content for keyword in ["knowledge graph", "intelligence", "strategic patterns"]):
            return "knowledge_graph"
        
        # Check for strategic analysis requests
        if any(keyword in content for keyword in ["strategic", "art of war", "five fundamentals"]):
            return "strategic"
        
        # Check for specific analysis types
        if "recommendation" in content:
            return "recommendations"
        elif "prioritize" in content or "priority" in content:
            return "prioritization"
        elif "plan" in content or "implementation" in content:
            return "planning"
        elif "predict" in content or "success" in content:
            return "prediction"
        else:
            return "comprehensive"
    
    async def _perform_comprehensive_analysis(self, request: AnalysisRequest) -> AnalysisResult:
        """Perform comprehensive analysis with knowledge graph intelligence."""
        try:
            # Extract context from request
            context = await self._extract_decision_context(request)
            
            # Get knowledge graph intelligence
            kg_intelligence = await self._get_knowledge_graph_intelligence(context)
            
            # Generate recommendations with knowledge graph insights
            recommendations = await self._generate_enhanced_recommendations(context, kg_intelligence)
            
            # Prioritize actions
            prioritized_actions = await self._prioritize_enhanced_actions(recommendations, kg_intelligence)
            
            # Create implementation plan
            implementation_plan = await self._create_enhanced_implementation_plan(prioritized_actions, kg_intelligence)
            
            # Predict success
            success_prediction = await self._predict_enhanced_success(implementation_plan, kg_intelligence)
            
            # Compile comprehensive result
            result_content = self._compile_comprehensive_result(
                context, kg_intelligence, recommendations, prioritized_actions, 
                implementation_plan, success_prediction
            )
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                status=ProcessingStatus.COMPLETED,
                content=result_content,
                metadata={
                    "analysis_type": "comprehensive",
                    "knowledge_graph_integration": True,
                    "recommendations_count": len(recommendations),
                    "confidence_score": kg_intelligence.confidence_score if kg_intelligence else 0.0
                }
            )
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            raise
    
    async def _perform_strategic_analysis(self, request: AnalysisRequest) -> AnalysisResult:
        """Perform strategic analysis using enhanced strategic analytics engine."""
        try:
            # Extract strategic context
            strategic_context = await self._extract_strategic_context(request)
            
            # Create strategic metrics
            strategic_metrics = await self._create_strategic_metrics(strategic_context)
            
            # Generate strategic recommendations with knowledge graph intelligence
            strategic_recommendations = await self.strategic_analytics_engine.generate_strategic_recommendations(
                strategic_metrics
            )
            
            # Compile strategic analysis result
            result_content = self._compile_strategic_analysis_result(
                strategic_context, strategic_metrics, strategic_recommendations
            )
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                status=ProcessingStatus.COMPLETED,
                content=result_content,
                metadata={
                    "analysis_type": "strategic",
                    "knowledge_graph_integration": True,
                    "strategic_recommendations_count": len(strategic_recommendations),
                    "domain": strategic_context.domain.value
                }
            )
            
        except Exception as e:
            logger.error(f"Error in strategic analysis: {e}")
            raise
    
    async def _perform_knowledge_graph_analysis(self, request: AnalysisRequest) -> AnalysisResult:
        """Perform knowledge graph specific analysis."""
        try:
            # Extract query context
            query_context = await self._extract_query_context(request)
            
            # Extract strategic intelligence from knowledge graph
            strategic_intelligence = await self.kg_intelligence_service.extract_strategic_intelligence(query_context)
            
            # Generate insights and recommendations
            insights = await self._generate_knowledge_graph_insights(strategic_intelligence)
            
            # Compile knowledge graph analysis result
            result_content = self._compile_knowledge_graph_analysis_result(
                query_context, strategic_intelligence, insights
            )
            
            return AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                status=ProcessingStatus.COMPLETED,
                content=result_content,
                metadata={
                    "analysis_type": "knowledge_graph",
                    "confidence_score": strategic_intelligence.confidence_score,
                    "entities_count": len(strategic_intelligence.key_entities),
                    "patterns_count": len(strategic_intelligence.strategic_patterns)
                }
            )
            
        except Exception as e:
            logger.error(f"Error in knowledge graph analysis: {e}")
            raise
    
    async def _extract_decision_context(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Extract decision context from request."""
        # Parse request content to extract context
        content = request.content or ""
        
        # Extract domain, entities, and objectives from content
        context = {
            "domain": "general",
            "entities": [],
            "objectives": [],
            "constraints": [],
            "timeframe": "1y",
            "geographic_scope": "global"
        }
        
        # Simple extraction logic - in practice, this would use NLP
        if "military" in content.lower():
            context["domain"] = "military"
        elif "business" in content.lower():
            context["domain"] = "business"
        elif "intelligence" in content.lower():
            context["domain"] = "intelligence"
        
        return context
    
    async def _extract_strategic_context(self, request: AnalysisRequest) -> StrategicContext:
        """Extract strategic context from request."""
        content = request.content or ""
        
        # Determine domain
        domain = StrategicDomain.BUSINESS  # Default
        if "military" in content.lower():
            domain = StrategicDomain.MILITARY
        elif "intelligence" in content.lower():
            domain = StrategicDomain.INTELLIGENCE
        elif "cybersecurity" in content.lower():
            domain = StrategicDomain.CYBERSECURITY
        elif "diplomatic" in content.lower():
            domain = StrategicDomain.DIPLOMATIC
        
        return StrategicContext(
            domain=domain,
            entities=[],
            timeframe="1y",
            geographic_scope="global",
            strategic_objectives=[],
            constraints=[],
            historical_context={},
            knowledge_graph_entities=[]
        )
    
    async def _extract_query_context(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Extract query context for knowledge graph analysis."""
        content = request.content or ""
        
        return {
            "domain": "general",
            "entities": [],
            "timeframe": "1y",
            "geographic_scope": "global",
            "strategic_objectives": [],
            "constraints": []
        }
    
    async def _get_knowledge_graph_intelligence(self, context: Dict[str, Any]) -> Optional[StrategicIntelligence]:
        """Get knowledge graph intelligence for decision context."""
        try:
            # Create cache key
            cache_key = f"{context['domain']}_{context['timeframe']}_{context['geographic_scope']}"
            
            # Check cache first
            cached_intelligence = await self.kg_intelligence_service.get_cached_intelligence(cache_key)
            if cached_intelligence:
                return cached_intelligence
            
            # Extract intelligence from knowledge graph
            strategic_intelligence = await self.kg_intelligence_service.extract_strategic_intelligence(context)
            
            # Cache the result
            self.kg_intelligence_service.cache_intelligence(cache_key, strategic_intelligence)
            
            return strategic_intelligence
            
        except Exception as e:
            logger.error(f"Error getting knowledge graph intelligence: {e}")
            return None
    
    async def _create_strategic_metrics(self, strategic_context: StrategicContext) -> StrategicMetrics:
        """Create strategic metrics for analysis."""
        # This would typically involve more sophisticated analysis
        # For now, create basic metrics
        return StrategicMetrics(
            domain=strategic_context.domain,
            timestamp=datetime.now().isoformat(),
            five_fundamentals={
                "the_way": 0.7,
                "heaven": 0.6,
                "earth": 0.8,
                "command": 0.7,
                "method": 0.6
            },
            deception_effectiveness=0.6,
            resource_efficiency=0.7,
            intelligence_superiority=0.8,
            alliance_strength=0.6,
            risk_factors=["resource_constraints", "coordination_challenges"],
            opportunities=["technology_advantage", "strategic_positioning"],
            confidence_score=0.7,
            knowledge_graph_insights={}
        )
    
    async def _generate_enhanced_recommendations(self, context: Dict[str, Any], 
                                               kg_intelligence: Optional[StrategicIntelligence]) -> List[Dict[str, Any]]:
        """Generate enhanced recommendations with knowledge graph intelligence."""
        recommendations = []
        
        # Generate base recommendations
        base_recommendations = await self.recommendation_engine.generate_recommendations(
            RecommendationContext(
                domain=context["domain"],
                objectives=context["objectives"],
                constraints=context["constraints"]
            )
        )
        
        # Enhance with knowledge graph intelligence
        if kg_intelligence:
            for rec in base_recommendations:
                enhanced_rec = {
                    **rec,
                    "knowledge_graph_insights": {
                        "strategic_patterns": kg_intelligence.strategic_patterns[:3],
                        "risk_indicators": kg_intelligence.risk_indicators[:2],
                        "opportunities": kg_intelligence.opportunities[:2]
                    },
                    "confidence_score": kg_intelligence.confidence_score
                }
                recommendations.append(enhanced_rec)
        else:
            recommendations = base_recommendations
        
        return recommendations
    
    async def _prioritize_enhanced_actions(self, recommendations: List[Dict[str, Any]], 
                                         kg_intelligence: Optional[StrategicIntelligence]) -> List[Dict[str, Any]]:
        """Prioritize actions with knowledge graph intelligence."""
        # Use knowledge graph insights for prioritization
        prioritization_context = PrioritizationContext(
            recommendations=recommendations,
            constraints=[],
            priorities=[]
        )
        
        if kg_intelligence:
            prioritization_context.constraints = kg_intelligence.risk_indicators
            prioritization_context.priorities = kg_intelligence.opportunities
        
        return await self.action_prioritizer.prioritize_actions(prioritization_context)
    
    async def _create_enhanced_implementation_plan(self, prioritized_actions: List[Dict[str, Any]], 
                                                  kg_intelligence: Optional[StrategicIntelligence]) -> Dict[str, Any]:
        """Create enhanced implementation plan with knowledge graph intelligence."""
        planning_context = PlanningContext(
            actions=prioritized_actions,
            resources={},
            timeline="6 months"
        )
        
        if kg_intelligence:
            # Add knowledge graph insights to planning context
            planning_context.resources["intelligence_insights"] = kg_intelligence.strategic_patterns
        
        return await self.implementation_planner.create_plan(planning_context)
    
    async def _predict_enhanced_success(self, implementation_plan: Dict[str, Any], 
                                       kg_intelligence: Optional[StrategicIntelligence]) -> Dict[str, Any]:
        """Predict success with knowledge graph intelligence."""
        prediction_context = PredictionContext(
            plan=implementation_plan,
            historical_data={},
            risk_factors=[]
        )
        
        if kg_intelligence:
            prediction_context.historical_data["patterns"] = kg_intelligence.historical_insights
            prediction_context.risk_factors = kg_intelligence.risk_indicators
        
        return await self.success_predictor.predict_success(prediction_context)
    
    async def _generate_knowledge_graph_insights(self, strategic_intelligence: StrategicIntelligence) -> Dict[str, Any]:
        """Generate insights from knowledge graph intelligence."""
        return {
            "key_insights": strategic_intelligence.strategic_patterns[:5],
            "risk_assessment": strategic_intelligence.risk_indicators,
            "opportunities": strategic_intelligence.opportunities,
            "historical_context": strategic_intelligence.historical_insights,
            "predictive_trends": strategic_intelligence.predictive_trends,
            "cross_domain_connections": strategic_intelligence.cross_domain_connections
        }
    
    def _compile_comprehensive_result(self, context: Dict[str, Any], 
                                    kg_intelligence: Optional[StrategicIntelligence],
                                    recommendations: List[Dict[str, Any]],
                                    prioritized_actions: List[Dict[str, Any]],
                                    implementation_plan: Dict[str, Any],
                                    success_prediction: Dict[str, Any]) -> str:
        """Compile comprehensive analysis result."""
        result = f"""
# Enhanced Decision Support Analysis

## Context
- Domain: {context['domain']}
- Timeframe: {context['timeframe']}
- Geographic Scope: {context['geographic_scope']}

## Knowledge Graph Intelligence
"""
        
        if kg_intelligence:
            result += f"""
- Confidence Score: {kg_intelligence.confidence_score:.2f}
- Key Entities: {', '.join(kg_intelligence.key_entities[:5])}
- Strategic Patterns: {', '.join(kg_intelligence.strategic_patterns[:3])}
- Risk Indicators: {', '.join(kg_intelligence.risk_indicators[:3])}
- Opportunities: {', '.join(kg_intelligence.opportunities[:3])}
"""
        else:
            result += "- No knowledge graph intelligence available\n"
        
        result += f"""
## Recommendations ({len(recommendations)})
"""
        
        for i, rec in enumerate(recommendations[:5], 1):
            result += f"{i}. {rec.get('recommendation', 'N/A')}\n"
        
        result += f"""
## Prioritized Actions ({len(prioritized_actions)})
"""
        
        for i, action in enumerate(prioritized_actions[:5], 1):
            result += f"{i}. {action.get('action', 'N/A')} (Priority: {action.get('priority', 'N/A')})\n"
        
        result += f"""
## Implementation Plan
- Timeline: {implementation_plan.get('timeline', 'N/A')}
- Resources Required: {len(implementation_plan.get('resources', {}))}
- Milestones: {len(implementation_plan.get('milestones', []))}

## Success Prediction
- Success Probability: {success_prediction.get('success_probability', 'N/A')}
- Key Risk Factors: {', '.join(success_prediction.get('risk_factors', [])[:3])}
- Success Factors: {', '.join(success_prediction.get('success_factors', [])[:3])}
"""
        
        return result
    
    def _compile_strategic_analysis_result(self, strategic_context: StrategicContext,
                                         strategic_metrics: StrategicMetrics,
                                         strategic_recommendations: List[StrategicRecommendation]) -> str:
        """Compile strategic analysis result."""
        result = f"""
# Strategic Analysis Report

## Strategic Context
- Domain: {strategic_context.domain.value}
- Timeframe: {strategic_context.timeframe}
- Geographic Scope: {strategic_context.geographic_scope}

## Strategic Metrics
- Confidence Score: {strategic_metrics.confidence_score:.2f}
- Five Fundamentals:
"""
        
        for fundamental, score in strategic_metrics.five_fundamentals.items():
            result += f"  - {fundamental.replace('_', ' ').title()}: {score:.2f}\n"
        
        result += f"""
- Deception Effectiveness: {strategic_metrics.deception_effectiveness:.2f}
- Resource Efficiency: {strategic_metrics.resource_efficiency:.2f}
- Intelligence Superiority: {strategic_metrics.intelligence_superiority:.2f}
- Alliance Strength: {strategic_metrics.alliance_strength:.2f}

## Strategic Recommendations ({len(strategic_recommendations)})
"""
        
        for i, rec in enumerate(strategic_recommendations[:5], 1):
            result += f"""
{i}. {rec.recommendation}
   - Principle: {rec.principle.value}
   - Priority: {rec.priority:.2f}
   - Expected Impact: {rec.expected_impact:.2f}
   - Historical Effectiveness: {rec.historical_effectiveness:.2f}
   - Timeline: {rec.timeline}
   - Risk Assessment: {rec.risk_assessment}
"""
        
        return result
    
    def _compile_knowledge_graph_analysis_result(self, query_context: Dict[str, Any],
                                               strategic_intelligence: StrategicIntelligence,
                                               insights: Dict[str, Any]) -> str:
        """Compile knowledge graph analysis result."""
        result = f"""
# Knowledge Graph Intelligence Analysis

## Query Context
- Domain: {query_context['domain']}
- Timeframe: {query_context['timeframe']}
- Geographic Scope: {query_context['geographic_scope']}

## Intelligence Summary
- Confidence Score: {strategic_intelligence.confidence_score:.2f}
- Key Entities: {len(strategic_intelligence.key_entities)}
- Relationships: {len(strategic_intelligence.relationships)}
- Strategic Patterns: {len(strategic_intelligence.strategic_patterns)}

## Key Insights
"""
        
        for insight in insights["key_insights"][:5]:
            result += f"- {insight}\n"
        
        result += f"""
## Risk Assessment
"""
        
        for risk in strategic_intelligence.risk_indicators[:5]:
            result += f"- {risk}\n"
        
        result += f"""
## Opportunities
"""
        
        for opportunity in strategic_intelligence.opportunities[:5]:
            result += f"- {opportunity}\n"
        
        result += f"""
## Historical Context
- Historical Insights: {len(strategic_intelligence.historical_insights)}
- Predictive Trends: {len(strategic_intelligence.predictive_trends)}
- Cross-Domain Connections: {len(strategic_intelligence.cross_domain_connections)}
"""
        
        return result
    
    # Implement other required methods for compatibility
    async def _generate_recommendations_only(self, request: AnalysisRequest) -> AnalysisResult:
        """Generate recommendations only."""
        context = await self._extract_decision_context(request)
        kg_intelligence = await self._get_knowledge_graph_intelligence(context)
        recommendations = await self._generate_enhanced_recommendations(context, kg_intelligence)
        
        return AnalysisResult(
            request_id=request.id,
            data_type=request.data_type,
            status=ProcessingStatus.COMPLETED,
            content=f"Generated {len(recommendations)} recommendations with knowledge graph intelligence",
            metadata={"recommendations_count": len(recommendations)}
        )
    
    async def _prioritize_actions_only(self, request: AnalysisRequest) -> AnalysisResult:
        """Prioritize actions only."""
        context = await self._extract_decision_context(request)
        kg_intelligence = await self._get_knowledge_graph_intelligence(context)
        recommendations = await self._generate_enhanced_recommendations(context, kg_intelligence)
        prioritized_actions = await self._prioritize_enhanced_actions(recommendations, kg_intelligence)
        
        return AnalysisResult(
            request_id=request.id,
            data_type=request.data_type,
            status=ProcessingStatus.COMPLETED,
            content=f"Prioritized {len(prioritized_actions)} actions with knowledge graph intelligence",
            metadata={"prioritized_actions_count": len(prioritized_actions)}
        )
    
    async def _create_implementation_plan_only(self, request: AnalysisRequest) -> AnalysisResult:
        """Create implementation plan only."""
        context = await self._extract_decision_context(request)
        kg_intelligence = await self._get_knowledge_graph_intelligence(context)
        recommendations = await self._generate_enhanced_recommendations(context, kg_intelligence)
        prioritized_actions = await self._prioritize_enhanced_actions(recommendations, kg_intelligence)
        implementation_plan = await self._create_enhanced_implementation_plan(prioritized_actions, kg_intelligence)
        
        return AnalysisResult(
            request_id=request.id,
            data_type=request.data_type,
            status=ProcessingStatus.COMPLETED,
            content=f"Created implementation plan with {len(implementation_plan.get('milestones', []))} milestones",
            metadata={"milestones_count": len(implementation_plan.get('milestones', []))}
        )
    
    async def _predict_success_only(self, request: AnalysisRequest) -> AnalysisResult:
        """Predict success only."""
        context = await self._extract_decision_context(request)
        kg_intelligence = await self._get_knowledge_graph_intelligence(context)
        recommendations = await self._generate_enhanced_recommendations(context, kg_intelligence)
        prioritized_actions = await self._prioritize_enhanced_actions(recommendations, kg_intelligence)
        implementation_plan = await self._create_enhanced_implementation_plan(prioritized_actions, kg_intelligence)
        success_prediction = await self._predict_enhanced_success(implementation_plan, kg_intelligence)
        
        return AnalysisResult(
            request_id=request.id,
            data_type=request.data_type,
            status=ProcessingStatus.COMPLETED,
            content=f"Success prediction: {success_prediction.get('success_probability', 'N/A')}",
            metadata={"success_probability": success_prediction.get('success_probability', 0.0)}
        )
