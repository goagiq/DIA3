"""
Intelligence-Specific Explanations for Phase 5: Model Interpretability & Explainable AI
Advanced forecasting & prediction system for DoD/Intelligence Community
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
from dataclasses import dataclass, asdict

from src.core.models import DataType
from src.config.config import config


@dataclass
class IntelligenceExplanation:
    """Intelligence-specific explanation result"""
    analysis_type: str
    key_insights: List[str]
    confidence_factors: List[str]
    recommendations: List[str]
    risk_assessment: str
    next_steps: List[str]
    timestamp: datetime


@dataclass
class ThreatExplanation:
    """Threat assessment explanation"""
    threat_level: str
    threat_type: str
    confidence: float
    key_indicators: List[str]
    mitigation_strategies: List[str]
    timeline: str
    escalation_factors: List[str]


@dataclass
class CapabilityExplanation:
    """Capability analysis explanation"""
    capability_score: float
    capability_domains: List[str]
    strengths: List[str]
    weaknesses: List[str]
    improvement_areas: List[str]
    competitive_analysis: Dict[str, Any]


class IntelligenceExplanations:
    """Intelligence-specific explanation generation"""
    
    def __init__(self):
        """Initialize the intelligence explanations engine"""
        self.explanation_templates = {
            'threat_assessment': self.explain_threat_assessment,
            'capability_analysis': self.explain_capability_analysis,
            'conflict_prediction': self._explain_conflict_prediction,
            'economic_impact': self._explain_economic_impact,
            'geopolitical_analysis': self._explain_geopolitical_analysis,
            'cybersecurity_threats': self._explain_cybersecurity_threats,
            'weapons_proliferation': self._explain_weapons_proliferation,
            'terrorist_activities': self._explain_terrorist_activities,
            'alliance_dynamics': self._explain_alliance_dynamics,
            'resource_availability': self._explain_resource_availability
        }
        
        self.intelligence_domains = {
            'military': self._explain_military_intelligence,
            'economic': self._explain_economic_intelligence,
            'political': self._explain_political_intelligence,
            'social': self._explain_social_intelligence,
            'technological': self._explain_technological_intelligence,
            'geographic': self._explain_geographic_intelligence
        }
        
        logger.info("✅ Intelligence Explanations Engine initialized")
    
    async def explain_threat_assessment(self, threat_analysis: Dict[str, Any]) -> ThreatExplanation:
        """Explain threat assessment results"""
        try:
            logger.info("🔍 Explaining threat assessment")
            
            # Extract threat information
            threat_level = threat_analysis.get('threat_level', 'unknown')
            threat_type = threat_analysis.get('threat_type', 'general')
            confidence = threat_analysis.get('confidence', 0.5)
            
            # Generate threat-specific explanations
            key_indicators = await self._extract_threat_indicators(threat_analysis)
            mitigation_strategies = await self._generate_mitigation_strategies(threat_analysis)
            timeline = await self._assess_threat_timeline(threat_analysis)
            escalation_factors = await self._identify_escalation_factors(threat_analysis)
            
            explanation = ThreatExplanation(
                threat_level=threat_level,
                threat_type=threat_type,
                confidence=confidence,
                key_indicators=key_indicators,
                mitigation_strategies=mitigation_strategies,
                timeline=timeline,
                escalation_factors=escalation_factors
            )
            
            logger.info(f"✅ Generated threat assessment explanation for {threat_type}")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Error explaining threat assessment: {e}")
            raise
    
    async def explain_capability_analysis(self, capability_results: Dict[str, Any]) -> CapabilityExplanation:
        """Explain capability analysis results"""
        try:
            logger.info("🔍 Explaining capability analysis")
            
            # Extract capability information
            capability_score = capability_results.get('capability_score', 0.5)
            capability_domains = capability_results.get('capability_domains', [])
            
            # Generate capability-specific explanations
            strengths = await self._identify_capability_strengths(capability_results)
            weaknesses = await self._identify_capability_weaknesses(capability_results)
            improvement_areas = await self._suggest_improvement_areas(capability_results)
            competitive_analysis = await self._perform_competitive_analysis(capability_results)
            
            explanation = CapabilityExplanation(
                capability_score=capability_score,
                capability_domains=capability_domains,
                strengths=strengths,
                weaknesses=weaknesses,
                improvement_areas=improvement_areas,
                competitive_analysis=competitive_analysis
            )
            
            logger.info(f"✅ Generated capability analysis explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Error explaining capability analysis: {e}")
            raise
    
    async def generate_executive_summary(self, detailed_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary for decision-makers"""
        try:
            logger.info("📋 Generating intelligence executive summary")
            
            # Extract key intelligence insights
            key_insights = await self._extract_intelligence_insights(detailed_analysis)
            
            # Generate intelligence-specific recommendations
            recommendations = await self._generate_intelligence_recommendations(detailed_analysis)
            
            # Assess intelligence risk level
            risk_assessment = await self._assess_intelligence_risk(detailed_analysis)
            
            # Suggest intelligence next steps
            next_steps = await self._suggest_intelligence_next_steps(detailed_analysis)
            
            # Create executive summary
            summary = {
                "intelligence_executive_summary": {
                    "timestamp": datetime.now().isoformat(),
                    "analysis_type": detailed_analysis.get('analysis_type', 'general_intelligence'),
                    "key_insights": key_insights[:5],  # Top 5 insights
                    "critical_recommendations": recommendations[:3],  # Top 3 recommendations
                    "risk_assessment": risk_assessment,
                    "confidence_level": detailed_analysis.get('confidence', 0.5),
                    "next_steps": next_steps,
                    "intelligence_priority": await self._determine_intelligence_priority(detailed_analysis)
                },
                "detailed_analysis_reference": detailed_analysis.get('analysis_id', 'unknown'),
                "intelligence_domains": await self._identify_intelligence_domains(detailed_analysis)
            }
            
            logger.info("✅ Generated intelligence executive summary")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating intelligence executive summary: {e}")
            return {"error": str(e)}
    
    async def explain_intelligence_domain(self, domain: str, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain intelligence analysis for specific domain"""
        try:
            logger.info(f"🔍 Explaining {domain} intelligence analysis")
            
            if domain in self.intelligence_domains:
                explanation = await self.intelligence_domains[domain](analysis_results)
            else:
                explanation = await self._explain_generic_intelligence(analysis_results)
            
            logger.info(f"✅ Generated {domain} intelligence explanation")
            return explanation
            
        except Exception as e:
            logger.error(f"❌ Error explaining {domain} intelligence: {e}")
            return await self._create_error_explanation(str(e))
    
    # Private helper methods for threat assessment
    
    async def _extract_threat_indicators(self, threat_analysis: Dict[str, Any]) -> List[str]:
        """Extract key threat indicators"""
        indicators = []
        
        # Extract from threat analysis
        if 'indicators' in threat_analysis:
            indicators.extend(threat_analysis['indicators'])
        
        # Generate based on threat type
        threat_type = threat_analysis.get('threat_type', 'general')
        if threat_type == 'military':
            indicators.extend([
                "Military buildup and mobilization",
                "Weapons system development",
                "Training and readiness activities"
            ])
        elif threat_type == 'cyber':
            indicators.extend([
                "Cyber reconnaissance activities",
                "Vulnerability exploitation attempts",
                "Data exfiltration patterns"
            ])
        elif threat_type == 'economic':
            indicators.extend([
                "Economic sanctions and restrictions",
                "Resource acquisition patterns",
                "Financial system targeting"
            ])
        
        # Add default indicators if none found
        if not indicators:
            indicators = [
                "Unusual activity patterns",
                "Capability development indicators",
                "Intent signaling"
            ]
        
        return indicators[:5]  # Limit to top 5 indicators
    
    async def _generate_mitigation_strategies(self, threat_analysis: Dict[str, Any]) -> List[str]:
        """Generate threat mitigation strategies"""
        strategies = []
        
        threat_level = threat_analysis.get('threat_level', 'medium')
        threat_type = threat_analysis.get('threat_type', 'general')
        
        if threat_level == 'high':
            strategies.append("Implement immediate defensive measures")
            strategies.append("Activate emergency response protocols")
            strategies.append("Enhance surveillance and monitoring")
        elif threat_level == 'medium':
            strategies.append("Develop contingency plans")
            strategies.append("Strengthen defensive capabilities")
            strategies.append("Increase intelligence collection")
        else:
            strategies.append("Monitor threat developments")
            strategies.append("Maintain readiness posture")
            strategies.append("Conduct regular threat assessments")
        
        # Add threat-type specific strategies
        if threat_type == 'military':
            strategies.append("Enhance military readiness and capabilities")
        elif threat_type == 'cyber':
            strategies.append("Implement cybersecurity measures")
        elif threat_type == 'economic':
            strategies.append("Develop economic resilience strategies")
        
        return strategies[:5]  # Limit to top 5 strategies
    
    async def _assess_threat_timeline(self, threat_analysis: Dict[str, Any]) -> str:
        """Assess threat timeline"""
        confidence = threat_analysis.get('confidence', 0.5)
        threat_level = threat_analysis.get('threat_level', 'medium')
        
        if threat_level == 'high' and confidence > 0.7:
            return "Immediate (0-30 days)"
        elif threat_level == 'high' or confidence > 0.6:
            return "Short-term (1-3 months)"
        elif threat_level == 'medium':
            return "Medium-term (3-6 months)"
        else:
            return "Long-term (6+ months)"
    
    async def _identify_escalation_factors(self, threat_analysis: Dict[str, Any]) -> List[str]:
        """Identify factors that could escalate the threat"""
        escalation_factors = []
        
        threat_type = threat_analysis.get('threat_type', 'general')
        
        if threat_type == 'military':
            escalation_factors.extend([
                "Military provocation or incident",
                "Alliance formation or strengthening",
                "Weapons system deployment"
            ])
        elif threat_type == 'cyber':
            escalation_factors.extend([
                "Successful cyber attack",
                "Critical infrastructure compromise",
                "Data breach or theft"
            ])
        elif threat_type == 'economic':
            escalation_factors.extend([
                "Economic sanctions implementation",
                "Resource blockade or restriction",
                "Financial system disruption"
            ])
        
        # Add general escalation factors
        escalation_factors.extend([
            "Political instability",
            "Diplomatic breakdown",
            "Public opinion shifts"
        ])
        
        return escalation_factors[:5]  # Limit to top 5 factors
    
    # Private helper methods for capability analysis
    
    async def _identify_capability_strengths(self, capability_results: Dict[str, Any]) -> List[str]:
        """Identify capability strengths"""
        strengths = []
        
        # Extract from capability results
        if 'strengths' in capability_results:
            strengths.extend(capability_results['strengths'])
        
        # Generate based on capability score
        capability_score = capability_results.get('capability_score', 0.5)
        if capability_score > 0.8:
            strengths.append("High overall capability level")
        elif capability_score > 0.6:
            strengths.append("Moderate capability level")
        
        # Add domain-specific strengths
        domains = capability_results.get('capability_domains', [])
        for domain in domains:
            if domain == 'military':
                strengths.append("Strong military capabilities")
            elif domain == 'economic':
                strengths.append("Robust economic foundation")
            elif domain == 'technological':
                strengths.append("Advanced technological capabilities")
        
        return strengths[:5]  # Limit to top 5 strengths
    
    async def _identify_capability_weaknesses(self, capability_results: Dict[str, Any]) -> List[str]:
        """Identify capability weaknesses"""
        weaknesses = []
        
        # Extract from capability results
        if 'weaknesses' in capability_results:
            weaknesses.extend(capability_results['weaknesses'])
        
        # Generate based on capability score
        capability_score = capability_results.get('capability_score', 0.5)
        if capability_score < 0.4:
            weaknesses.append("Low overall capability level")
        elif capability_score < 0.6:
            weaknesses.append("Limited capability in key areas")
        
        # Add domain-specific weaknesses
        domains = capability_results.get('capability_domains', [])
        missing_domains = ['military', 'economic', 'technological', 'logistical']
        for domain in missing_domains:
            if domain not in domains:
                weaknesses.append(f"Limited {domain} capabilities")
        
        return weaknesses[:5]  # Limit to top 5 weaknesses
    
    async def _suggest_improvement_areas(self, capability_results: Dict[str, Any]) -> List[str]:
        """Suggest areas for capability improvement"""
        improvement_areas = []
        
        capability_score = capability_results.get('capability_score', 0.5)
        
        if capability_score < 0.6:
            improvement_areas.append("Enhance overall capability development")
        
        # Add domain-specific improvements
        domains = capability_results.get('capability_domains', [])
        if 'military' not in domains:
            improvement_areas.append("Develop military capabilities")
        if 'economic' not in domains:
            improvement_areas.append("Strengthen economic foundation")
        if 'technological' not in domains:
            improvement_areas.append("Advance technological capabilities")
        if 'logistical' not in domains:
            improvement_areas.append("Improve logistical support systems")
        
        return improvement_areas[:5]  # Limit to top 5 areas
    
    async def _perform_competitive_analysis(self, capability_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform competitive analysis"""
        return {
            "competitive_position": "moderate",
            "relative_strengths": ["Technology", "Economic resources"],
            "relative_weaknesses": ["Geographic position", "Alliance networks"],
            "competitive_advantages": ["Innovation capacity", "Resource efficiency"],
            "competitive_disadvantages": ["Geographic constraints", "Limited alliances"]
        }
    
    # Private helper methods for executive summary
    
    async def _extract_intelligence_insights(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Extract key intelligence insights"""
        insights = []
        
        # Extract from analysis results
        if 'key_insights' in detailed_analysis:
            insights.extend(detailed_analysis['key_insights'])
        
        if 'findings' in detailed_analysis:
            insights.extend(detailed_analysis['findings'][:2])
        
        # Add intelligence-specific insights
        analysis_type = detailed_analysis.get('analysis_type', 'general')
        if analysis_type == 'threat_assessment':
            insights.append("Threat level assessment completed")
        elif analysis_type == 'capability_analysis':
            insights.append("Capability analysis results available")
        
        # Add default insights if none found
        if not insights:
            insights = [
                "Intelligence analysis completed successfully",
                "Key patterns and trends identified",
                "Risk factors assessed and prioritized"
            ]
        
        return insights[:5]  # Limit to top 5 insights
    
    async def _generate_intelligence_recommendations(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Generate intelligence-specific recommendations"""
        recommendations = []
        
        # Extract from analysis results
        if 'recommendations' in detailed_analysis:
            recommendations.extend(detailed_analysis['recommendations'])
        
        # Add intelligence-specific recommendations
        analysis_type = detailed_analysis.get('analysis_type', 'general')
        if analysis_type == 'threat_assessment':
            recommendations.append("Enhance threat monitoring and early warning systems")
        elif analysis_type == 'capability_analysis':
            recommendations.append("Develop capability enhancement strategies")
        
        # Add general intelligence recommendations
        recommendations.extend([
            "Increase intelligence collection and analysis",
            "Strengthen intelligence sharing and coordination",
            "Implement intelligence-driven decision making"
        ])
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    async def _assess_intelligence_risk(self, detailed_analysis: Dict[str, Any]) -> str:
        """Assess intelligence risk level"""
        confidence = detailed_analysis.get('confidence', 0.5)
        threat_level = detailed_analysis.get('threat_level', 'medium')
        
        if threat_level == 'high' or confidence < 0.4:
            return "high"
        elif threat_level == 'medium' or confidence < 0.7:
            return "medium"
        else:
            return "low"
    
    async def _suggest_intelligence_next_steps(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Suggest intelligence next steps"""
        next_steps = [
            "Validate intelligence findings with multiple sources",
            "Develop intelligence collection requirements",
            "Implement intelligence-driven response strategies"
        ]
        
        analysis_type = detailed_analysis.get('analysis_type', 'general')
        if analysis_type == 'threat_assessment':
            next_steps.insert(0, "Activate threat response protocols")
        elif analysis_type == 'capability_analysis':
            next_steps.insert(0, "Develop capability enhancement plans")
        
        return next_steps[:5]  # Limit to top 5 steps
    
    async def _determine_intelligence_priority(self, detailed_analysis: Dict[str, Any]) -> str:
        """Determine intelligence priority level"""
        threat_level = detailed_analysis.get('threat_level', 'medium')
        confidence = detailed_analysis.get('confidence', 0.5)
        
        if threat_level == 'high' and confidence > 0.7:
            return "critical"
        elif threat_level == 'high' or confidence > 0.6:
            return "high"
        elif threat_level == 'medium':
            return "medium"
        else:
            return "low"
    
    async def _identify_intelligence_domains(self, detailed_analysis: Dict[str, Any]) -> List[str]:
        """Identify relevant intelligence domains"""
        domains = []
        
        analysis_type = detailed_analysis.get('analysis_type', 'general')
        if analysis_type == 'threat_assessment':
            domains.extend(['military', 'cyber', 'economic'])
        elif analysis_type == 'capability_analysis':
            domains.extend(['military', 'economic', 'technological'])
        
        # Add general domains
        domains.extend(['political', 'social', 'geographic'])
        
        return list(set(domains))  # Remove duplicates
    
    # Intelligence domain explanation methods
    
    async def _explain_military_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain military intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="military_intelligence",
            key_insights=[
                "Military capabilities assessment",
                "Force structure analysis",
                "Operational readiness evaluation"
            ],
            confidence_factors=[
                "Military intelligence quality",
                "Force structure data completeness",
                "Expert military validation"
            ],
            recommendations=[
                "Enhance military intelligence collection",
                "Develop counter-capability strategies",
                "Monitor military developments"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate military intelligence findings",
                "Develop military response strategies",
                "Monitor military capability developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _explain_economic_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain economic intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="economic_intelligence",
            key_insights=[
                "Economic strength assessment",
                "Resource availability analysis",
                "Economic vulnerability evaluation"
            ],
            confidence_factors=[
                "Economic data quality",
                "Market intelligence completeness",
                "Economic expert validation"
            ],
            recommendations=[
                "Enhance economic intelligence collection",
                "Develop economic resilience strategies",
                "Monitor economic indicators"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate economic intelligence findings",
                "Develop economic response strategies",
                "Monitor economic developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _explain_political_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain political intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="political_intelligence",
            key_insights=[
                "Political stability assessment",
                "Leadership analysis",
                "Policy direction evaluation"
            ],
            confidence_factors=[
                "Political intelligence quality",
                "Leadership data completeness",
                "Political expert validation"
            ],
            recommendations=[
                "Enhance political intelligence collection",
                "Develop political engagement strategies",
                "Monitor political developments"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate political intelligence findings",
                "Develop political response strategies",
                "Monitor political developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _explain_social_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain social intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="social_intelligence",
            key_insights=[
                "Social stability assessment",
                "Public opinion analysis",
                "Social movement evaluation"
            ],
            confidence_factors=[
                "Social intelligence quality",
                "Public opinion data completeness",
                "Social expert validation"
            ],
            recommendations=[
                "Enhance social intelligence collection",
                "Develop social engagement strategies",
                "Monitor social developments"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate social intelligence findings",
                "Develop social response strategies",
                "Monitor social developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _explain_technological_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain technological intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="technological_intelligence",
            key_insights=[
                "Technological capability assessment",
                "Innovation capacity analysis",
                "Technology advantage evaluation"
            ],
            confidence_factors=[
                "Technological intelligence quality",
                "Technology data completeness",
                "Technology expert validation"
            ],
            recommendations=[
                "Enhance technological intelligence collection",
                "Develop technology advantage strategies",
                "Monitor technological developments"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate technological intelligence findings",
                "Develop technology response strategies",
                "Monitor technological developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _explain_geographic_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain geographic intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="geographic_intelligence",
            key_insights=[
                "Geographic advantage assessment",
                "Territorial analysis",
                "Strategic location evaluation"
            ],
            confidence_factors=[
                "Geographic intelligence quality",
                "Territorial data completeness",
                "Geographic expert validation"
            ],
            recommendations=[
                "Enhance geographic intelligence collection",
                "Develop geographic advantage strategies",
                "Monitor geographic developments"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate geographic intelligence findings",
                "Develop geographic response strategies",
                "Monitor geographic developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _explain_generic_intelligence(self, analysis_results: Dict[str, Any]) -> IntelligenceExplanation:
        """Explain generic intelligence analysis"""
        return IntelligenceExplanation(
            analysis_type="generic_intelligence",
            key_insights=[
                "Pattern recognition results",
                "Anomaly detection findings",
                "Trend analysis outcomes"
            ],
            confidence_factors=[
                "Intelligence data quality",
                "Analysis methodology validation",
                "Expert review and validation"
            ],
            recommendations=[
                "Enhance intelligence collection",
                "Develop response strategies",
                "Monitor developments"
            ],
            risk_assessment="medium",
            next_steps=[
                "Validate intelligence findings",
                "Develop response strategies",
                "Monitor developments"
            ],
            timestamp=datetime.now()
        )
    
    async def _create_error_explanation(self, error_message: str) -> IntelligenceExplanation:
        """Create error explanation"""
        return IntelligenceExplanation(
            analysis_type="error",
            key_insights=[f"Error in analysis: {error_message}"],
            confidence_factors=["Analysis failed"],
            recommendations=["Review analysis parameters and retry"],
            risk_assessment="unknown",
            next_steps=["Debug analysis issues"],
            timestamp=datetime.now()
        )
    
    # Additional explanation methods for specific analysis types
    
    async def _explain_conflict_prediction(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain conflict prediction analysis"""
        return {
            "analysis_type": "conflict_prediction",
            "key_insights": [
                "Conflict probability assessment",
                "Escalation path analysis",
                "Timeline prediction"
            ],
            "confidence_factors": [
                "Geopolitical data quality",
                "Historical conflict patterns",
                "Diplomatic intelligence"
            ],
            "recommendations": [
                "Enhance diplomatic engagement",
                "Prepare conflict prevention measures",
                "Develop de-escalation strategies"
            ]
        }
    
    async def _explain_economic_impact(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain economic impact analysis"""
        return {
            "analysis_type": "economic_impact",
            "key_insights": [
                "Economic consequence assessment",
                "Market impact prediction",
                "Resource availability analysis"
            ],
            "confidence_factors": [
                "Economic data quality",
                "Market trend analysis",
                "Expert economic validation"
            ],
            "recommendations": [
                "Develop economic resilience strategies",
                "Monitor market indicators",
                "Prepare economic contingency plans"
            ]
        }
    
    async def _explain_geopolitical_analysis(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain geopolitical analysis"""
        return {
            "analysis_type": "geopolitical_analysis",
            "key_insights": [
                "Geopolitical risk assessment",
                "Alliance dynamics analysis",
                "Regional stability evaluation"
            ],
            "confidence_factors": [
                "Geopolitical intelligence quality",
                "Regional expert validation",
                "Historical pattern analysis"
            ],
            "recommendations": [
                "Enhance regional intelligence collection",
                "Strengthen diplomatic relationships",
                "Develop regional stability strategies"
            ]
        }
    
    async def _explain_cybersecurity_threats(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain cybersecurity threats analysis"""
        return {
            "analysis_type": "cybersecurity_threats",
            "key_insights": [
                "Cyber threat assessment",
                "Vulnerability analysis",
                "Attack vector identification"
            ],
            "confidence_factors": [
                "Cyber intelligence quality",
                "Threat actor analysis",
                "Technical validation"
            ],
            "recommendations": [
                "Enhance cybersecurity measures",
                "Implement threat monitoring",
                "Develop incident response plans"
            ]
        }
    
    async def _explain_weapons_proliferation(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain weapons proliferation analysis"""
        return {
            "analysis_type": "weapons_proliferation",
            "key_insights": [
                "Proliferation risk assessment",
                "Technology transfer analysis",
                "Capability development tracking"
            ],
            "confidence_factors": [
                "Proliferation intelligence quality",
                "Technology tracking data",
                "Expert validation"
            ],
            "recommendations": [
                "Enhance proliferation monitoring",
                "Strengthen export controls",
                "Develop counter-proliferation strategies"
            ]
        }
    
    async def _explain_terrorist_activities(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain terrorist activities analysis"""
        return {
            "analysis_type": "terrorist_activities",
            "key_insights": [
                "Terrorist threat assessment",
                "Activity pattern analysis",
                "Capability evaluation"
            ],
            "confidence_factors": [
                "Terrorist intelligence quality",
                "Pattern analysis validation",
                "Multi-source verification"
            ],
            "recommendations": [
                "Enhance terrorist monitoring",
                "Develop counter-terrorism strategies",
                "Strengthen security measures"
            ]
        }
    
    async def _explain_alliance_dynamics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain alliance dynamics analysis"""
        return {
            "analysis_type": "alliance_dynamics",
            "key_insights": [
                "Alliance strength assessment",
                "Relationship dynamics analysis",
                "Cooperation level evaluation"
            ],
            "confidence_factors": [
                "Diplomatic intelligence quality",
                "Relationship data completeness",
                "Expert diplomatic validation"
            ],
            "recommendations": [
                "Strengthen alliance relationships",
                "Enhance diplomatic engagement",
                "Develop cooperation strategies"
            ]
        }
    
    async def _explain_resource_availability(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Explain resource availability analysis"""
        return {
            "analysis_type": "resource_availability",
            "key_insights": [
                "Resource availability assessment",
                "Supply chain analysis",
                "Resource dependency evaluation"
            ],
            "confidence_factors": [
                "Resource intelligence quality",
                "Supply chain data completeness",
                "Expert resource validation"
            ],
            "recommendations": [
                "Diversify resource sources",
                "Develop supply chain resilience",
                "Monitor resource availability"
            ]
        }
