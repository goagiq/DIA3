"""
Escalation Analysis Agent for Multi-Domain Strategic Assessment

This agent provides comprehensive escalation analysis capabilities across multiple
domains including defense, intelligence, business, cybersecurity, and geopolitical
contexts.
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Any

from loguru import logger
from pydantic import BaseModel, Field

from src.core.models import DataType, AnalysisResult
from src.core.pattern_recognition.pattern_storage import PatternStorage
try:
    from strands import Agent
    STRANDS_AVAILABLE = True
    logger.info("✅ Using real Strands implementation for escalation analysis agent")
except ImportError:
    from src.core.strands_mock import Agent
    STRANDS_AVAILABLE = False
    logger.warning("⚠️ Using mock Strands implementation for escalation analysis agent - real Strands not available")


class EscalationScenario(BaseModel):
    """Model for escalation scenario analysis."""
    scenario_id: str = Field(..., description="Unique identifier for the scenario")
    domain: str = Field(..., description="Domain (defense, intelligence, business, etc.)")
    scenario_type: str = Field(..., description="Type of escalation scenario")
    timeline: str = Field(..., description="Timeline (immediate, medium-term, long-term)")
    historical_pattern: str = Field(
        ..., description="Historical pattern this scenario is based on"
    )
    trigger: str = Field(..., description="Potential trigger for escalation")
    escalation_pathway: List[str] = Field(..., description="Steps in escalation pathway")
    warning_indicators: List[str] = Field(..., description="Warning indicators to monitor")
    risk_level: str = Field(..., description="Risk level (low, medium, high, critical)")
    probability: float = Field(..., description="Probability of occurrence (0.0-1.0)")
    impact_level: str = Field(..., description="Impact level (low, medium, high, critical)")
    mitigation_strategies: List[str] = Field(
        ..., description="Potential mitigation strategies"
    )


class EscalationAnalysisRequest(BaseModel):
    """Request model for escalation analysis."""
    content: str = Field(..., description="Content to analyze for escalation patterns")
    domain: str = Field(..., description="Primary domain for analysis")
    secondary_domains: Optional[List[str]] = Field(default=None, description="Additional domains to consider")
    analysis_depth: str = Field(default="comprehensive", description="Analysis depth (basic, standard, comprehensive)")
    include_historical_patterns: bool = Field(default=True, description="Include historical pattern analysis")
    include_warning_indicators: bool = Field(default=True, description="Include warning indicators")
    include_mitigation_strategies: bool = Field(default=True, description="Include mitigation strategies")
    custom_frameworks: Optional[List[str]] = Field(default=None, description="Custom analysis frameworks to apply")


class EscalationAnalysisResult(BaseModel):
    """Result model for escalation analysis."""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    domain: str = Field(..., description="Primary analysis domain")
    content_summary: str = Field(..., description="Summary of analyzed content")
    escalation_scenarios: List[EscalationScenario] = Field(..., description="Identified escalation scenarios")
    historical_patterns: List[Dict[str, Any]] = Field(..., description="Historical patterns identified")
    warning_indicators: Dict[str, List[str]] = Field(..., description="Warning indicators by category")
    risk_assessment: Dict[str, Any] = Field(..., description="Overall risk assessment")
    mitigation_recommendations: List[Dict[str, Any]] = Field(..., description="Mitigation recommendations")
    confidence_score: float = Field(..., description="Confidence in analysis (0.0-1.0)")
    analysis_metadata: Dict[str, Any] = Field(..., description="Additional analysis metadata")


class EscalationAnalysisAgent:
    """
    Multi-domain escalation analysis agent that applies historical patterns
    and strategic frameworks to identify potential escalation scenarios.
    """
    
    def __init__(self, model_name: str = "llama3.2:latest"):
        self.agent_name = "EscalationAnalysisAgent"
        self.agent_id = f"{self.agent_name}_{int(time.time())}"
        self.supported_data_types = [DataType.TEXT, DataType.PDF, DataType.IMAGE]
        self.metadata = {
            "agent_type": "escalation_analysis",
            "model": model_name,
            "capabilities": ["multi_domain_analysis", "historical_patterns", "risk_assessment"],
            "domains": ["defense", "intelligence", "business", "cybersecurity", "geopolitical"]
        }
        
        # Initialize pattern storage
        self.pattern_storage = PatternStorage()
        
        # Initialize Strands agent for coordination
        self.strands_agent = Agent("escalation_coordinator", model_name)
        
        # Domain-specific escalation frameworks
        self.domain_frameworks = {
            "defense": {
                "historical_patterns": [
                    "arms_race_dynamics",
                    "alliance_fracturing",
                    "territorial_conflicts",
                    "military_posturing",
                    "strategic_depth_mentality"
                ],
                "escalation_types": [
                    "military_escalation",
                    "alliance_conflicts",
                    "territorial_disputes",
                    "arms_competition",
                    "strategic_encirclement"
                ]
            },
            "intelligence": {
                "historical_patterns": [
                    "information_warfare",
                    "espionage_escalation",
                    "psychological_operations",
                    "covert_actions",
                    "intelligence_competition"
                ],
                "escalation_types": [
                    "cyber_espionage",
                    "disinformation_campaigns",
                    "human_intelligence_operations",
                    "technical_intelligence_gathering",
                    "counterintelligence_operations"
                ]
            },
            "business": {
                "historical_patterns": [
                    "market_competition",
                    "economic_warfare",
                    "resource_conflicts",
                    "regulatory_battles",
                    "alliance_formation"
                ],
                "escalation_types": [
                    "price_wars",
                    "regulatory_conflicts",
                    "market_manipulation",
                    "resource_competition",
                    "alliance_formation"
                ]
            },
            "cybersecurity": {
                "historical_patterns": [
                    "cyber_arms_race",
                    "information_warfare",
                    "infrastructure_attacks",
                    "espionage_escalation",
                    "attribution_conflicts"
                ],
                "escalation_types": [
                    "cyber_attacks",
                    "information_warfare",
                    "infrastructure_disruption",
                    "data_breaches",
                    "attribution_conflicts"
                ]
            },
            "geopolitical": {
                "historical_patterns": [
                    "great_power_rivalry",
                    "alliance_dynamics",
                    "territorial_conflicts",
                    "economic_competition",
                    "cultural_conflicts"
                ],
                "escalation_types": [
                    "diplomatic_conflicts",
                    "economic_sanctions",
                    "territorial_disputes",
                    "alliance_formation",
                    "cultural_conflicts"
                ]
            }
        }
        
        # Historical pattern templates
        self.historical_patterns = {
            "arms_race_dynamics": {
                "description": "Competitive military buildup leading to escalation",
                "indicators": ["military modernization", "defense spending increases", "weapons development"],
                "escalation_path": ["capability development", "deployment", "confrontation"]
            },
            "alliance_fracturing": {
                "description": "Efforts to divide and weaken opposing alliances",
                "indicators": ["bilateral diplomacy", "alliance criticism", "divide-and-conquer tactics"],
                "escalation_path": ["alliance weakening", "unilateral actions", "conflict"]
            },
            "information_warfare": {
                "description": "Manipulation of information and perceptions",
                "indicators": ["disinformation campaigns", "media manipulation", "social media operations"],
                "escalation_path": ["information operations", "perception manipulation", "decision influence"]
            },
            "economic_warfare": {
                "description": "Use of economic tools for strategic advantage",
                "indicators": ["sanctions", "trade restrictions", "currency manipulation"],
                "escalation_path": ["economic pressure", "retaliation", "economic conflict"]
            },
            "territorial_conflicts": {
                "description": "Disputes over territory and spheres of influence",
                "indicators": ["border disputes", "territorial claims", "military presence"],
                "escalation_path": ["territorial claims", "military posturing", "conflict"]
            }
        }
        
        logger.info(f"✅ {self.agent_name} initialized successfully")
    
    async def analyze_escalation_patterns(
        self,
        content: str,
        domain: str,
        secondary_domains: Optional[List[str]] = None,
        analysis_depth: str = "comprehensive"
    ) -> EscalationAnalysisResult:
        """
        Analyze content for escalation patterns using domain-specific frameworks.
        """
        try:
            analysis_id = f"escalation_analysis_{int(time.time())}"
            timestamp = datetime.now()
            
            # Validate domain
            if domain not in self.domain_frameworks:
                raise ValueError(f"Unsupported domain: {domain}")
            
            # Get domain framework
            framework = self.domain_frameworks[domain]
            
            # Analyze content using Strands coordination
            analysis_prompt = self._build_analysis_prompt(
                content, domain, framework, analysis_depth
            )
            
            # Coordinate analysis using Strands
            coordination_result = await self.strands_agent.run(analysis_prompt)
            
            # Extract escalation scenarios
            scenarios = await self._extract_escalation_scenarios(
                coordination_result, domain, framework
            )
            
            # Identify historical patterns
            historical_patterns = await self._identify_historical_patterns(
                content, domain, framework
            )
            
            # Generate warning indicators
            warning_indicators = await self._generate_warning_indicators(
                scenarios, domain, framework
            )
            
            # Assess overall risk
            risk_assessment = await self._assess_risk(scenarios, historical_patterns)
            
            # Generate mitigation recommendations
            mitigation_recommendations = await self._generate_mitigation_recommendations(
                scenarios, domain
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                scenarios, historical_patterns, analysis_depth
            )
            
            # Create analysis result
            result = EscalationAnalysisResult(
                analysis_id=analysis_id,
                timestamp=timestamp,
                domain=domain,
                content_summary=self._generate_content_summary(content),
                escalation_scenarios=scenarios,
                historical_patterns=historical_patterns,
                warning_indicators=warning_indicators,
                risk_assessment=risk_assessment,
                mitigation_recommendations=mitigation_recommendations,
                confidence_score=confidence_score,
                analysis_metadata={
                    "analysis_depth": analysis_depth,
                    "secondary_domains": secondary_domains,
                    "framework_used": framework,
                    "patterns_identified": len(historical_patterns)
                }
            )
            
            # Store analysis result
            await self._store_analysis_result(result)
            
            logger.info(f"✅ Escalation analysis completed: {analysis_id}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in escalation analysis: {e}")
            raise
    
    def _build_analysis_prompt(
        self,
        content: str,
        domain: str,
        framework: Dict[str, Any],
        analysis_depth: str
    ) -> str:
        """Build analysis prompt for Strands coordination."""
        prompt = f"""
        Coordinate the escalation analysis of this content using the swarm:
        
        Content: {content[:1000]}...
        
        Domain: {domain}
        Analysis Depth: {analysis_depth}
        
        Framework Elements:
        - Historical Patterns: {framework['historical_patterns']}
        - Escalation Types: {framework['escalation_types']}
        
        Analysis Requirements:
        1. Identify potential escalation scenarios based on historical patterns
        2. Assess risk levels and probabilities for each scenario
        3. Generate warning indicators for monitoring
        4. Consider cross-domain implications
        5. Provide mitigation strategies
        
        Coordinate the analysis across multiple specialized agents to provide comprehensive escalation assessment.
        """
        return prompt
    
    async def _extract_escalation_scenarios(
        self,
        coordination_result: str,
        domain: str,
        framework: Dict[str, Any]
    ) -> List[EscalationScenario]:
        """Extract escalation scenarios from coordination result."""
        scenarios = []
        
        # Parse coordination result to extract scenarios
        # This is a simplified implementation - in practice, you'd use more sophisticated parsing
        
        for escalation_type in framework['escalation_types']:
            scenario = EscalationScenario(
                scenario_id=f"scenario_{len(scenarios) + 1}",
                domain=domain,
                scenario_type=escalation_type,
                timeline=self._determine_timeline(escalation_type),
                historical_pattern=self._identify_historical_pattern(escalation_type),
                trigger=f"Potential trigger for {escalation_type}",
                escalation_pathway=[
                    "Initial trigger",
                    "Escalation phase",
                    "Conflict phase"
                ],
                warning_indicators=[
                    f"Indicator 1 for {escalation_type}",
                    f"Indicator 2 for {escalation_type}"
                ],
                risk_level=self._assess_risk_level(escalation_type),
                probability=0.5,  # Default probability
                impact_level="medium",
                mitigation_strategies=[
                    f"Strategy 1 for {escalation_type}",
                    f"Strategy 2 for {escalation_type}"
                ]
            )
            scenarios.append(scenario)
        
        return scenarios
    
    async def _identify_historical_patterns(
        self,
        content: str,
        domain: str,
        framework: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify historical patterns in content."""
        patterns = []
        
        for pattern_name in framework['historical_patterns']:
            if pattern_name in self.historical_patterns:
                pattern = self.historical_patterns[pattern_name].copy()
                pattern['name'] = pattern_name
                pattern['domain'] = domain
                pattern['relevance_score'] = self._calculate_pattern_relevance(
                    content, pattern_name
                )
                patterns.append(pattern)
        
        return patterns
    
    async def _generate_warning_indicators(
        self,
        scenarios: List[EscalationScenario],
        domain: str,
        framework: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate warning indicators by category."""
        indicators = {
            "political": [],
            "economic": [],
            "military": [],
            "technological": [],
            "social": []
        }
        
        for scenario in scenarios:
            for indicator in scenario.warning_indicators:
                category = self._categorize_indicator(indicator, domain)
                if category in indicators:
                    indicators[category].append(indicator)
        
        return indicators
    
    async def _assess_risk(
        self,
        scenarios: List[EscalationScenario],
        historical_patterns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Assess overall risk based on scenarios and patterns."""
        if not scenarios:
            return {"overall_risk": "low", "risk_score": 0.0}
        
        # Calculate risk metrics
        risk_scores = [self._risk_level_to_score(s.risk_level) for s in scenarios]
        avg_risk_score = sum(risk_scores) / len(risk_scores)
        
        # Determine overall risk level
        if avg_risk_score >= 0.8:
            overall_risk = "critical"
        elif avg_risk_score >= 0.6:
            overall_risk = "high"
        elif avg_risk_score >= 0.4:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        return {
            "overall_risk": overall_risk,
            "risk_score": avg_risk_score,
            "high_risk_scenarios": len([s for s in scenarios if s.risk_level in ["high", "critical"]]),
            "total_scenarios": len(scenarios),
            "pattern_relevance": len([p for p in historical_patterns if p.get('relevance_score', 0) > 0.5])
        }
    
    async def _generate_mitigation_recommendations(
        self,
        scenarios: List[EscalationScenario],
        domain: str
    ) -> List[Dict[str, Any]]:
        """Generate mitigation recommendations."""
        recommendations = []
        
        for scenario in scenarios:
            if scenario.risk_level in ["high", "critical"]:
                recommendation = {
                    "scenario_id": scenario.scenario_id,
                    "priority": "high" if scenario.risk_level == "critical" else "medium",
                    "strategies": scenario.mitigation_strategies,
                    "timeline": "immediate" if scenario.timeline == "immediate" else "short-term",
                    "domain": domain
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_confidence_score(
        self,
        scenarios: List[EscalationScenario],
        historical_patterns: List[Dict[str, Any]],
        analysis_depth: str
    ) -> float:
        """Calculate confidence score for analysis."""
        base_score = 0.5
        
        # Adjust based on number of scenarios
        if scenarios:
            base_score += min(len(scenarios) * 0.1, 0.3)
        
        # Adjust based on historical patterns
        if historical_patterns:
            base_score += min(len(historical_patterns) * 0.05, 0.2)
        
        # Adjust based on analysis depth
        if analysis_depth == "comprehensive":
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    async def _store_analysis_result(self, result: EscalationAnalysisResult):
        """Store analysis result in pattern storage."""
        try:
            # Store in pattern storage
            await self.pattern_storage.store_pattern(
                pattern_id=result.analysis_id,
                pattern_type="escalation_analysis",
                pattern_data=result.dict(),
                metadata={
                    "domain": result.domain,
                    "timestamp": result.timestamp.isoformat(),
                    "confidence_score": result.confidence_score
                }
            )
            
            logger.info(f"✅ Analysis result stored: {result.analysis_id}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to store analysis result: {e}")
    
    def _determine_timeline(self, escalation_type: str) -> str:
        """Determine timeline for escalation type."""
        immediate_types = ["cyber_attacks", "information_warfare", "economic_sanctions"]
        medium_types = ["alliance_conflicts", "regulatory_conflicts", "market_manipulation"]
        
        if escalation_type in immediate_types:
            return "immediate"
        elif escalation_type in medium_types:
            return "medium-term"
        else:
            return "long-term"
    
    def _identify_historical_pattern(self, escalation_type: str) -> str:
        """Identify historical pattern for escalation type."""
        pattern_mapping = {
            "cyber_attacks": "information_warfare",
            "information_warfare": "information_warfare",
            "economic_sanctions": "economic_warfare",
            "alliance_conflicts": "alliance_fracturing",
            "military_escalation": "arms_race_dynamics",
            "territorial_disputes": "territorial_conflicts"
        }
        
        return pattern_mapping.get(escalation_type, "general_escalation")
    
    def _assess_risk_level(self, escalation_type: str) -> str:
        """Assess risk level for escalation type."""
        high_risk_types = ["cyber_attacks", "military_escalation", "economic_sanctions"]
        medium_risk_types = ["information_warfare", "alliance_conflicts", "regulatory_conflicts"]
        
        if escalation_type in high_risk_types:
            return "high"
        elif escalation_type in medium_risk_types:
            return "medium"
        else:
            return "low"
    
    def _calculate_pattern_relevance(self, content: str, pattern_name: str) -> float:
        """Calculate relevance score for historical pattern."""
        # Simplified relevance calculation
        pattern_keywords = {
            "arms_race_dynamics": ["military", "weapons", "defense", "arms"],
            "alliance_fracturing": ["alliance", "coalition", "partnership", "divide"],
            "information_warfare": ["information", "propaganda", "disinformation", "media"],
            "economic_warfare": ["economic", "sanctions", "trade", "financial"],
            "territorial_conflicts": ["territory", "border", "land", "sovereignty"]
        }
        
        keywords = pattern_keywords.get(pattern_name, [])
        if not keywords:
            return 0.0
        
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        return min(matches / len(keywords), 1.0)
    
    def _categorize_indicator(self, indicator: str, domain: str) -> str:
        """Categorize warning indicator."""
        indicator_lower = indicator.lower()
        
        if any(word in indicator_lower for word in ["military", "weapons", "defense"]):
            return "military"
        elif any(word in indicator_lower for word in ["economic", "trade", "financial", "sanctions"]):
            return "economic"
        elif any(word in indicator_lower for word in ["cyber", "technology", "digital"]):
            return "technological"
        elif any(word in indicator_lower for word in ["political", "diplomatic", "government"]):
            return "political"
        else:
            return "social"
    
    def _risk_level_to_score(self, risk_level: str) -> float:
        """Convert risk level to numerical score."""
        mapping = {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
            "critical": 1.0
        }
        return mapping.get(risk_level, 0.5)
    
    def _generate_content_summary(self, content: str) -> str:
        """Generate summary of analyzed content."""
        if len(content) <= 200:
            return content
        
        # Simple summary generation
        words = content.split()
        if len(words) <= 50:
            return content
        
        summary_words = words[:50]
        return " ".join(summary_words) + "..."
    
    async def process(self, data: Any, data_type: DataType) -> AnalysisResult:
        """Process data for escalation analysis."""
        try:
            if data_type not in self.supported_data_types:
                raise ValueError(f"Unsupported data type: {data_type}")
            
            # Convert data to string if needed
            if isinstance(data, str):
                content = data
            else:
                content = str(data)
            
            # Perform escalation analysis
            result = await self.analyze_escalation_patterns(
                content=content,
                domain="general",  # Default domain
                analysis_depth="comprehensive"
            )
            
            return AnalysisResult(
                success=True,
                data=result.dict(),
                metadata={
                    "agent": self.agent_name,
                    "analysis_type": "escalation_analysis",
                    "domain": result.domain,
                    "confidence_score": result.confidence_score
                }
            )
            
        except Exception as e:
            logger.error(f"❌ Error in escalation analysis processing: {e}")
            return AnalysisResult(
                success=False,
                error=str(e),
                metadata={"agent": self.agent_name}
            )
