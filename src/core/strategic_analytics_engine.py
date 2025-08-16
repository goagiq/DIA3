"""
Enhanced Strategic Analytics Engine
Integrates Art of War principles with advanced analytics for comprehensive strategic analysis.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


class StrategicDomain(Enum):
    """Strategic analysis domains."""
    MILITARY = "military"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    CYBERSECURITY = "cybersecurity"
    DIPLOMATIC = "diplomatic"


class ArtOfWarPrinciple(Enum):
    """Art of War principles for analysis."""
    THE_WAY = "道"  # Moral influence
    HEAVEN = "天"   # Timing and conditions
    EARTH = "地"    # Terrain and position
    COMMAND = "将"  # Leadership
    METHOD = "法"   # Organization and discipline


@dataclass
class StrategicMetrics:
    """Strategic metrics for analysis."""
    domain: StrategicDomain
    timestamp: str
    five_fundamentals: Dict[str, float]
    deception_effectiveness: float
    resource_efficiency: float
    intelligence_superiority: float
    alliance_strength: float
    risk_factors: List[str]
    opportunities: List[str]
    confidence_score: float


@dataclass
class StrategicRecommendation:
    """Strategic recommendation with implementation details."""
    principle: ArtOfWarPrinciple
    recommendation: str
    priority: float
    implementation_steps: List[str]
    expected_impact: float
    resource_requirements: Dict[str, float]
    timeline: str
    risk_assessment: str


class StrategicAnalyticsEngine:
    """Enhanced strategic analytics engine using Art of War principles."""
    
    def __init__(self):
        self.domain_weights = self._initialize_domain_weights()
        self.risk_thresholds = self._initialize_risk_thresholds()
        self.ml_models = {}
        self.scalers = {}
        
    def _initialize_domain_weights(self) -> Dict[StrategicDomain, Dict[str, float]]:
        """Initialize domain-specific weights for analysis."""
        return {
            StrategicDomain.MILITARY: {
                "the_way": 0.20,    # Morale and political support
                "heaven": 0.15,     # Weather and timing
                "earth": 0.25,      # Terrain and positioning
                "command": 0.20,    # Leadership and decision-making
                "method": 0.20,     # Organization and discipline
            },
            StrategicDomain.INTELLIGENCE: {
                "the_way": 0.15,    # Organizational culture
                "heaven": 0.20,     # Timing and conditions
                "earth": 0.15,      # Geographic and cyber terrain
                "command": 0.25,    # Leadership and coordination
                "method": 0.25,     # Processes and capabilities
            },
            StrategicDomain.BUSINESS: {
                "the_way": 0.25,    # Corporate culture and values
                "heaven": 0.20,     # Market conditions and timing
                "earth": 0.20,      # Market position and geography
                "command": 0.20,    # Leadership and management
                "method": 0.15,     # Operations and efficiency
            },
            StrategicDomain.CYBERSECURITY: {
                "the_way": 0.20,    # Security culture
                "heaven": 0.15,     # Threat landscape and timing
                "earth": 0.25,      # Digital terrain and infrastructure
                "command": 0.20,    # Security leadership
                "method": 0.20,     # Security processes and tools
            },
            StrategicDomain.DIPLOMATIC: {
                "the_way": 0.30,    # Diplomatic culture and values
                "heaven": 0.20,     # Political timing and conditions
                "earth": 0.15,      # Geographic and political terrain
                "command": 0.20,    # Diplomatic leadership
                "method": 0.15,     # Diplomatic processes
            }
        }
    
    def _initialize_risk_thresholds(self) -> Dict[StrategicDomain, Dict[str, float]]:
        """Initialize domain-specific risk thresholds."""
        return {
            StrategicDomain.MILITARY: {
                "resource_shortage": 0.7,
                "intelligence_gap": 0.6,
                "alliance_fragmentation": 0.8,
                "technological_disadvantage": 0.7,
                "morale_crisis": 0.8
            },
            StrategicDomain.INTELLIGENCE: {
                "intelligence_gap": 0.6,
                "counterintelligence_breach": 0.8,
                "technical_disadvantage": 0.7,
                "coordination_failure": 0.7,
                "source_compromise": 0.9
            },
            StrategicDomain.BUSINESS: {
                "market_share_loss": 0.7,
                "competitive_disadvantage": 0.6,
                "financial_stress": 0.8,
                "operational_inefficiency": 0.7,
                "reputation_damage": 0.8
            },
            StrategicDomain.CYBERSECURITY: {
                "vulnerability_exposure": 0.8,
                "threat_intelligence_gap": 0.7,
                "incident_response_delay": 0.6,
                "security_control_failure": 0.8,
                "data_breach": 0.9
            },
            StrategicDomain.DIPLOMATIC: {
                "alliance_fragmentation": 0.8,
                "diplomatic_isolation": 0.7,
                "credibility_loss": 0.8,
                "negotiation_failure": 0.7,
                "international_sanctions": 0.9
            }
        }
    
    def analyze_strategic_position(self, data: Dict[str, Any], 
                                 domain: StrategicDomain) -> StrategicMetrics:
        """Analyze strategic position using Art of War principles."""
        # Calculate five fundamentals
        five_fundamentals = self._calculate_five_fundamentals(data, domain)
        
        # Calculate deception effectiveness
        deception_effectiveness = self._calculate_deception_effectiveness(data, domain)
        
        # Calculate resource efficiency
        resource_efficiency = self._calculate_resource_efficiency(data, domain)
        
        # Calculate intelligence superiority
        intelligence_superiority = self._calculate_intelligence_superiority(data, domain)
        
        # Calculate alliance strength
        alliance_strength = self._calculate_alliance_strength(data, domain)
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(data, domain)
        
        # Identify opportunities
        opportunities = self._identify_opportunities(data, domain)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            five_fundamentals, deception_effectiveness, resource_efficiency,
            intelligence_superiority, alliance_strength
        )
        
        return StrategicMetrics(
            domain=domain,
            timestamp=datetime.now().isoformat(),
            five_fundamentals=five_fundamentals,
            deception_effectiveness=deception_effectiveness,
            resource_efficiency=resource_efficiency,
            intelligence_superiority=intelligence_superiority,
            alliance_strength=alliance_strength,
            risk_factors=risk_factors,
            opportunities=opportunities,
            confidence_score=confidence_score
        )
    
    def _calculate_five_fundamentals(self, data: Dict[str, Any], 
                                   domain: StrategicDomain) -> Dict[str, float]:
        """Calculate the five fundamental factors from Art of War."""
        weights = self.domain_weights[domain]
        fundamentals = {}
        
        # The Way (道) - Moral influence and alignment
        if domain == StrategicDomain.MILITARY:
            fundamentals["the_way"] = self._calculate_military_morale(data)
        elif domain == StrategicDomain.INTELLIGENCE:
            fundamentals["the_way"] = self._calculate_intelligence_culture(data)
        elif domain == StrategicDomain.BUSINESS:
            fundamentals["the_way"] = self._calculate_business_culture(data)
        elif domain == StrategicDomain.CYBERSECURITY:
            fundamentals["the_way"] = self._calculate_security_culture(data)
        elif domain == StrategicDomain.DIPLOMATIC:
            fundamentals["the_way"] = self._calculate_diplomatic_culture(data)
        
        # Heaven (天) - Timing and conditions
        fundamentals["heaven"] = self._calculate_timing_conditions(data, domain)
        
        # Earth (地) - Terrain and position
        fundamentals["earth"] = self._calculate_terrain_position(data, domain)
        
        # Command (将) - Leadership and decision-making
        fundamentals["command"] = self._calculate_leadership_effectiveness(data, domain)
        
        # Method (法) - Organization and discipline
        fundamentals["method"] = self._calculate_organizational_discipline(data, domain)
        
        # Apply domain-specific weights
        weighted_fundamentals = {}
        for key, value in fundamentals.items():
            weighted_fundamentals[key] = value * weights.get(key, 0.2)
        
        return weighted_fundamentals
    
    def _calculate_military_morale(self, data: Dict[str, Any]) -> float:
        """Calculate military morale and political support."""
        factors = [
            data.get("political_support", 0.5),
            data.get("public_opinion", 0.5),
            data.get("troop_morale", 0.5),
            data.get("alliance_support", 0.5),
            data.get("veteran_support", 0.5)
        ]
        return np.mean(factors)
    
    def _calculate_intelligence_culture(self, data: Dict[str, Any]) -> float:
        """Calculate intelligence organizational culture."""
        factors = [
            data.get("information_sharing", 0.5),
            data.get("collaboration_culture", 0.5),
            data.get("security_awareness", 0.5),
            data.get("innovation_mindset", 0.5),
            data.get("analytical_rigor", 0.5)
        ]
        return np.mean(factors)
    
    def _calculate_business_culture(self, data: Dict[str, Any]) -> float:
        """Calculate business organizational culture."""
        factors = [
            data.get("employee_engagement", 0.5),
            data.get("stakeholder_alignment", 0.5),
            data.get("ethical_standards", 0.5),
            data.get("innovation_culture", 0.5),
            data.get("customer_focus", 0.5)
        ]
        return np.mean(factors)
    
    def _calculate_security_culture(self, data: Dict[str, Any]) -> float:
        """Calculate cybersecurity culture."""
        factors = [
            data.get("security_awareness", 0.5),
            data.get("compliance_culture", 0.5),
            data.get("incident_reporting", 0.5),
            data.get("continuous_improvement", 0.5),
            data.get("risk_awareness", 0.5)
        ]
        return np.mean(factors)
    
    def _calculate_diplomatic_culture(self, data: Dict[str, Any]) -> float:
        """Calculate diplomatic culture."""
        factors = [
            data.get("diplomatic_ethics", 0.5),
            data.get("international_cooperation", 0.5),
            data.get("conflict_resolution", 0.5),
            data.get("cultural_sensitivity", 0.5),
            data.get("negotiation_skills", 0.5)
        ]
        return np.mean(factors)
    
    def _calculate_timing_conditions(self, data: Dict[str, Any], 
                                   domain: StrategicDomain) -> float:
        """Calculate timing and conditions factor."""
        if domain == StrategicDomain.MILITARY:
            factors = [
                data.get("weather_conditions", 0.5),
                data.get("seasonal_factors", 0.5),
                data.get("political_timing", 0.5),
                data.get("technological_readiness", 0.5)
            ]
        elif domain == StrategicDomain.INTELLIGENCE:
            factors = [
                data.get("threat_landscape", 0.5),
                data.get("technological_timing", 0.5),
                data.get("political_conditions", 0.5),
                data.get("intelligence_windows", 0.5)
            ]
        elif domain == StrategicDomain.BUSINESS:
            factors = [
                data.get("market_conditions", 0.5),
                data.get("economic_cycle", 0.5),
                data.get("competitive_timing", 0.5),
                data.get("regulatory_environment", 0.5)
            ]
        elif domain == StrategicDomain.CYBERSECURITY:
            factors = [
                data.get("threat_landscape", 0.5),
                data.get("vulnerability_disclosure", 0.5),
                data.get("regulatory_timing", 0.5),
                data.get("technology_maturity", 0.5)
            ]
        elif domain == StrategicDomain.DIPLOMATIC:
            factors = [
                data.get("political_landscape", 0.5),
                data.get("international_timing", 0.5),
                data.get("alliance_dynamics", 0.5),
                data.get("crisis_timing", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5, 0.5]
        
        return np.mean(factors)
    
    def _calculate_terrain_position(self, data: Dict[str, Any], 
                                  domain: StrategicDomain) -> float:
        """Calculate terrain and position factor."""
        if domain == StrategicDomain.MILITARY:
            factors = [
                data.get("geographic_advantage", 0.5),
                data.get("strategic_position", 0.5),
                data.get("logistics_network", 0.5),
                data.get("force_disposition", 0.5)
            ]
        elif domain == StrategicDomain.INTELLIGENCE:
            factors = [
                data.get("geographic_coverage", 0.5),
                data.get("cyber_terrain", 0.5),
                data.get("access_points", 0.5),
                data.get("collection_positions", 0.5)
            ]
        elif domain == StrategicDomain.BUSINESS:
            factors = [
                data.get("market_position", 0.5),
                data.get("geographic_presence", 0.5),
                data.get("supply_chain_position", 0.5),
                data.get("competitive_position", 0.5)
            ]
        elif domain == StrategicDomain.CYBERSECURITY:
            factors = [
                data.get("network_architecture", 0.5),
                data.get("digital_terrain", 0.5),
                data.get("security_perimeter", 0.5),
                data.get("defensive_positions", 0.5)
            ]
        elif domain == StrategicDomain.DIPLOMATIC:
            factors = [
                data.get("diplomatic_presence", 0.5),
                data.get("alliance_position", 0.5),
                data.get("influence_networks", 0.5),
                data.get("negotiation_position", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5, 0.5]
        
        return np.mean(factors)
    
    def _calculate_leadership_effectiveness(self, data: Dict[str, Any], 
                                          domain: StrategicDomain) -> float:
        """Calculate leadership and decision-making effectiveness."""
        if domain == StrategicDomain.MILITARY:
            factors = [
                data.get("command_structure", 0.5),
                data.get("decision_speed", 0.5),
                data.get("strategic_vision", 0.5),
                data.get("tactical_flexibility", 0.5)
            ]
        elif domain == StrategicDomain.INTELLIGENCE:
            factors = [
                data.get("coordination_effectiveness", 0.5),
                data.get("analysis_leadership", 0.5),
                data.get("strategic_guidance", 0.5),
                data.get("operational_oversight", 0.5)
            ]
        elif domain == StrategicDomain.BUSINESS:
            factors = [
                data.get("executive_leadership", 0.5),
                data.get("strategic_planning", 0.5),
                data.get("change_management", 0.5),
                data.get("operational_leadership", 0.5)
            ]
        elif domain == StrategicDomain.CYBERSECURITY:
            factors = [
                data.get("security_leadership", 0.5),
                data.get("incident_command", 0.5),
                data.get("risk_governance", 0.5),
                data.get("technical_leadership", 0.5)
            ]
        elif domain == StrategicDomain.DIPLOMATIC:
            factors = [
                data.get("diplomatic_leadership", 0.5),
                data.get("negotiation_skills", 0.5),
                data.get("crisis_management", 0.5),
                data.get("alliance_leadership", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5, 0.5]
        
        return np.mean(factors)
    
    def _calculate_organizational_discipline(self, data: Dict[str, Any], 
                                           domain: StrategicDomain) -> float:
        """Calculate organizational discipline and processes."""
        if domain == StrategicDomain.MILITARY:
            factors = [
                data.get("training_standards", 0.5),
                data.get("operational_discipline", 0.5),
                data.get("logistics_efficiency", 0.5),
                data.get("maintenance_standards", 0.5)
            ]
        elif domain == StrategicDomain.INTELLIGENCE:
            factors = [
                data.get("analytical_processes", 0.5),
                data.get("security_protocols", 0.5),
                data.get("quality_standards", 0.5),
                data.get("operational_procedures", 0.5)
            ]
        elif domain == StrategicDomain.BUSINESS:
            factors = [
                data.get("operational_efficiency", 0.5),
                data.get("quality_management", 0.5),
                data.get("process_discipline", 0.5),
                data.get("performance_standards", 0.5)
            ]
        elif domain == StrategicDomain.CYBERSECURITY:
            factors = [
                data.get("security_processes", 0.5),
                data.get("incident_procedures", 0.5),
                data.get("compliance_standards", 0.5),
                data.get("response_protocols", 0.5)
            ]
        elif domain == StrategicDomain.DIPLOMATIC:
            factors = [
                data.get("diplomatic_protocols", 0.5),
                data.get("negotiation_processes", 0.5),
                data.get("communication_standards", 0.5),
                data.get("crisis_procedures", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5, 0.5]
        
        return np.mean(factors)
    
    def _calculate_deception_effectiveness(self, data: Dict[str, Any], 
                                         domain: StrategicDomain) -> float:
        """Calculate deception and misdirection effectiveness."""
        deception_factors = [
            data.get("capability_masking", 0.5),
            data.get("intention_deception", 0.5),
            data.get("information_manipulation", 0.5),
            data.get("alliance_manipulation", 0.5),
            data.get("timing_deception", 0.5)
        ]
        return np.mean(deception_factors)
    
    def _calculate_resource_efficiency(self, data: Dict[str, Any], 
                                     domain: StrategicDomain) -> float:
        """Calculate resource efficiency and sustainability."""
        resource_factors = [
            data.get("resource_allocation", 0.5),
            data.get("resource_sustainability", 0.5),
            data.get("resource_optimization", 0.5),
            data.get("resource_effectiveness", 0.5)
        ]
        return np.mean(resource_factors)
    
    def _calculate_intelligence_superiority(self, data: Dict[str, Any], 
                                          domain: StrategicDomain) -> float:
        """Calculate intelligence and information superiority."""
        intel_factors = [
            data.get("intelligence_effectiveness", 0.5),
            data.get("intelligence_coverage", 0.5),
            data.get("intelligence_quality", 0.5),
            data.get("intelligence_timeliness", 0.5)
        ]
        return np.mean(intel_factors)
    
    def _calculate_alliance_strength(self, data: Dict[str, Any], 
                                   domain: StrategicDomain) -> float:
        """Calculate alliance and partnership strength."""
        alliance_factors = [
            data.get("alliance_effectiveness", 0.5),
            data.get("alliance_cohesion", 0.5),
            data.get("alliance_coordination", 0.5),
            data.get("alliance_reliability", 0.5)
        ]
        return np.mean(alliance_factors)
    
    def _identify_risk_factors(self, data: Dict[str, Any], 
                             domain: StrategicDomain) -> List[str]:
        """Identify key risk factors based on domain-specific thresholds."""
        risk_factors = []
        thresholds = self.risk_thresholds[domain]
        
        for risk_type, threshold in thresholds.items():
            risk_value = data.get(risk_type, 0.0)
            if risk_value > threshold:
                risk_factors.append(f"High {risk_type.replace('_', ' ')} risk")
        
        return risk_factors
    
    def _identify_opportunities(self, data: Dict[str, Any], 
                              domain: StrategicDomain) -> List[str]:
        """Identify strategic opportunities."""
        opportunities = []
        
        # Analyze strengths that can be leveraged
        for fundamental, score in data.get("five_fundamentals", {}).items():
            if score > 0.8:
                opportunities.append(f"Leverage {fundamental} advantage")
        
        # Analyze competitive advantages
        if data.get("competitive_advantage", 0.0) > 0.7:
            opportunities.append("Expand competitive advantage")
        
        # Analyze market opportunities
        if data.get("market_opportunity", 0.0) > 0.7:
            opportunities.append("Capture market opportunity")
        
        return opportunities
    
    def _calculate_confidence_score(self, five_fundamentals: Dict[str, float],
                                  deception_effectiveness: float,
                                  resource_efficiency: float,
                                  intelligence_superiority: float,
                                  alliance_strength: float) -> float:
        """Calculate confidence score for the assessment."""
        # Weight different factors for confidence calculation
        fundamental_score = np.mean(list(five_fundamentals.values()))
        
        factors = [
            fundamental_score * 0.4,
            deception_effectiveness * 0.2,
            resource_efficiency * 0.15,
            intelligence_superiority * 0.15,
            alliance_strength * 0.1
        ]
        
        return np.mean(factors)
    
    def generate_strategic_recommendations(self, metrics: StrategicMetrics) -> List[StrategicRecommendation]:
        """Generate strategic recommendations based on assessment."""
        recommendations = []
        
        # Mapping from fundamental names to ArtOfWarPrinciple enum values
        fundamental_mapping = {
            "the_way": ArtOfWarPrinciple.THE_WAY,
            "heaven": ArtOfWarPrinciple.HEAVEN,
            "earth": ArtOfWarPrinciple.EARTH,
            "command": ArtOfWarPrinciple.COMMAND,
            "method": ArtOfWarPrinciple.METHOD
        }
        
        # Analyze five fundamentals and provide recommendations
        for fundamental, score in metrics.five_fundamentals.items():
            if fundamental in fundamental_mapping:
                principle = fundamental_mapping[fundamental]
                if score < 0.6:
                    recommendations.append(self._create_recommendation(
                        principle=principle,
                        recommendation=f"Strengthen {fundamental.replace('_', ' ')} capabilities",
                        priority=0.8,
                        expected_impact=0.7
                    ))
                elif score > 0.8:
                    recommendations.append(self._create_recommendation(
                        principle=principle,
                        recommendation=f"Leverage {fundamental.replace('_', ' ')} advantages",
                        priority=0.6,
                        expected_impact=0.5
                    ))
        
        # Analyze deception patterns
        if metrics.deception_effectiveness < 0.6:
            recommendations.append(self._create_recommendation(
                principle=ArtOfWarPrinciple.THE_WAY,  # Deception relates to moral influence
                recommendation="Enhance deception and misdirection capabilities",
                priority=0.7,
                expected_impact=0.6
            ))
        
        # Analyze resource management
        if metrics.resource_efficiency < 0.6:
            recommendations.append(self._create_recommendation(
                principle=ArtOfWarPrinciple.METHOD,
                recommendation="Optimize resource allocation and efficiency",
                priority=0.8,
                expected_impact=0.7
            ))
        
        # Analyze intelligence capabilities
        if metrics.intelligence_superiority < 0.6:
            recommendations.append(self._create_recommendation(
                principle=ArtOfWarPrinciple.COMMAND,
                recommendation="Strengthen intelligence and information gathering capabilities",
                priority=0.9,
                expected_impact=0.8
            ))
        
        # Analyze alliance management
        if metrics.alliance_strength < 0.6:
            recommendations.append(self._create_recommendation(
                principle=ArtOfWarPrinciple.THE_WAY,
                recommendation="Strengthen alliance and partnership management",
                priority=0.7,
                expected_impact=0.6
            ))
        
        return recommendations
    
    def _create_recommendation(self, principle: ArtOfWarPrinciple, 
                             recommendation: str, priority: float, 
                             expected_impact: float) -> StrategicRecommendation:
        """Create a strategic recommendation with implementation details."""
        return StrategicRecommendation(
            principle=principle,
            recommendation=recommendation,
            priority=priority,
            implementation_steps=self._generate_implementation_steps(recommendation),
            expected_impact=expected_impact,
            resource_requirements=self._estimate_resource_requirements(recommendation),
            timeline=self._estimate_timeline(recommendation),
            risk_assessment=self._assess_implementation_risks(recommendation)
        )
    
    def _generate_implementation_steps(self, recommendation: str) -> List[str]:
        """Generate implementation steps for a recommendation."""
        # This would be enhanced with domain-specific implementation templates
        return [
            "Conduct detailed assessment of current capabilities",
            "Develop implementation plan with milestones",
            "Allocate necessary resources and personnel",
            "Execute implementation with regular progress reviews",
            "Monitor and evaluate effectiveness"
        ]
    
    def _estimate_resource_requirements(self, recommendation: str) -> Dict[str, float]:
        """Estimate resource requirements for implementation."""
        return {
            "personnel": 0.6,
            "technology": 0.4,
            "time": 0.7,
            "budget": 0.5
        }
    
    def _estimate_timeline(self, recommendation: str) -> str:
        """Estimate implementation timeline."""
        return "3-6 months"
    
    def _assess_implementation_risks(self, recommendation: str) -> str:
        """Assess implementation risks."""
        return "Medium risk - requires careful change management"
    
    def train_predictive_models(self, historical_data: List[StrategicMetrics]) -> None:
        """Train predictive models for strategic forecasting."""
        if not historical_data:
            logger.warning("No historical data provided for model training")
            return
        
        # Prepare training data
        X = []
        y = []
        
        for metrics in historical_data:
            features = [
                np.mean(list(metrics.five_fundamentals.values())),
                metrics.deception_effectiveness,
                metrics.resource_efficiency,
                metrics.intelligence_superiority,
                metrics.alliance_strength
            ]
            X.append(features)
            y.append(metrics.confidence_score)
        
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Store model and scaler
        self.ml_models["confidence_predictor"] = model
        self.scalers["confidence_predictor"] = scaler
        
        # Evaluate model
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        logger.info(f"Model training complete - Train score: {train_score:.3f}, "
                   f"Test score: {test_score:.3f}")
    
    def predict_strategic_outcome(self, current_metrics: StrategicMetrics) -> float:
        """Predict strategic outcome using trained models."""
        if "confidence_predictor" not in self.ml_models:
            logger.warning("No trained model available for prediction")
            return current_metrics.confidence_score
        
        # Prepare features
        features = [
            np.mean(list(current_metrics.five_fundamentals.values())),
            current_metrics.deception_effectiveness,
            current_metrics.resource_efficiency,
            current_metrics.intelligence_superiority,
            current_metrics.alliance_strength
        ]
        
        # Scale features
        scaler = self.scalers["confidence_predictor"]
        features_scaled = scaler.transform([features])
        
        # Make prediction
        model = self.ml_models["confidence_predictor"]
        prediction = model.predict(features_scaled)[0]
        
        return prediction
    
    def export_analysis_report(self, metrics: StrategicMetrics, 
                             recommendations: List[StrategicRecommendation]) -> Dict[str, Any]:
        """Export comprehensive analysis report."""
        return {
            "analysis_metadata": {
                "domain": metrics.domain.value,
                "timestamp": metrics.timestamp,
                "confidence_score": metrics.confidence_score,
                "analysis_version": "1.0.0"
            },
            "strategic_metrics": asdict(metrics),
            "recommendations": [asdict(rec) for rec in recommendations],
            "summary": {
                "key_strengths": [k for k, v in metrics.five_fundamentals.items() if v > 0.7],
                "key_weaknesses": [k for k, v in metrics.five_fundamentals.items() if v < 0.5],
                "critical_risks": metrics.risk_factors,
                "strategic_opportunities": metrics.opportunities
            }
        }
