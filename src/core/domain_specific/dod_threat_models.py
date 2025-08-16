"""
DoD-Specific Threat Assessment Models
Threat assessment and prediction models for Department of Defense applications
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class MilitaryCapability:
    """Military capability assessment structure"""
    country: str
    capability_score: float
    readiness_level: float
    modernization_index: float
    personnel_strength: int
    equipment_quality: float
    training_level: float
    logistics_capacity: float
    command_effectiveness: float
    assessment_date: datetime
    metadata: Dict[str, Any]

@dataclass
class ConflictProbability:
    """Conflict probability assessment structure"""
    scenario_name: str
    probability: float
    confidence_interval: Tuple[float, float]
    time_horizon: int  # days
    escalation_factors: List[str]
    de_escalation_factors: List[str]
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    assessment_date: datetime
    metadata: Dict[str, Any]

@dataclass
class WeaponsProliferation:
    """Weapons proliferation analysis structure"""
    country: str
    proliferation_risk: float
    weapon_types: List[str]
    technology_level: str
    supply_chain_analysis: Dict[str, Any]
    detection_probability: float
    countermeasures_effectiveness: float
    assessment_date: datetime
    metadata: Dict[str, Any]

class DoDThreatAssessmentModels:
    """DoD-specific threat assessment and prediction models"""
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
            
        self.config = config
        self.capability_models = {}
        self.conflict_models = {}
        self.proliferation_models = {}
        
        logger.info("Initialized DoD Threat Assessment Models")
        
    async def assess_military_capabilities(self, country_data: Dict[str, Any]) -> MilitaryCapability:
        """Assess military capabilities and readiness"""
        logger.info(f"Assessing military capabilities for {country_data.get('country', 'unknown')}")
        
        country = country_data.get('country', 'unknown')
        
        # Extract capability indicators
        personnel = country_data.get('personnel', {})
        equipment = country_data.get('equipment', {})
        training = country_data.get('training', {})
        logistics = country_data.get('logistics', {})
        command = country_data.get('command', {})
        
        # Calculate capability scores
        personnel_score = self._calculate_personnel_score(personnel)
        equipment_score = self._calculate_equipment_score(equipment)
        training_score = self._calculate_training_score(training)
        logistics_score = self._calculate_logistics_score(logistics)
        command_score = self._calculate_command_score(command)
        
        # Calculate overall capability score
        capability_score = (
            personnel_score * 0.25 +
            equipment_score * 0.25 +
            training_score * 0.20 +
            logistics_score * 0.15 +
            command_score * 0.15
        )
        
        # Calculate readiness level
        readiness_level = self._calculate_readiness_level(country_data)
        
        # Calculate modernization index
        modernization_index = self._calculate_modernization_index(equipment)
        
        capability = MilitaryCapability(
            country=country,
            capability_score=capability_score,
            readiness_level=readiness_level,
            modernization_index=modernization_index,
            personnel_strength=personnel.get('total_strength', 0),
            equipment_quality=equipment_score,
            training_level=training_score,
            logistics_capacity=logistics_score,
            command_effectiveness=command_score,
            assessment_date=datetime.now(),
            metadata={
                'assessment_method': 'comprehensive_capability_analysis',
                'data_sources': country_data.get('data_sources', []),
                'confidence_level': 0.85
            }
        )
        
        logger.info(f"Military capability assessment completed for {country}: {capability_score:.3f}")
        return capability
        
    async def predict_conflict_probability(self, geopolitical_data: Dict[str, Any]) -> ConflictProbability:
        """Predict probability of conflict escalation"""
        logger.info("Predicting conflict probability")
        
        # Extract geopolitical indicators
        tensions = geopolitical_data.get('tensions', {})
        historical_conflicts = geopolitical_data.get('historical_conflicts', [])
        economic_factors = geopolitical_data.get('economic_factors', {})
        political_factors = geopolitical_data.get('political_factors', {})
        
        # Calculate base probability
        base_probability = self._calculate_base_conflict_probability(tensions, historical_conflicts)
        
        # Adjust for economic factors
        economic_adjustment = self._calculate_economic_adjustment(economic_factors)
        
        # Adjust for political factors
        political_adjustment = self._calculate_political_adjustment(political_factors)
        
        # Calculate final probability
        final_probability = base_probability + economic_adjustment + political_adjustment
        final_probability = max(0.0, min(1.0, final_probability))  # Clamp to [0, 1]
        
        # Determine risk level
        risk_level = self._determine_risk_level(final_probability)
        
        # Calculate confidence interval
        confidence_interval = self._calculate_conflict_confidence_interval(final_probability)
        
        # Identify escalation and de-escalation factors
        escalation_factors = self._identify_escalation_factors(geopolitical_data)
        de_escalation_factors = self._identify_de_escalation_factors(geopolitical_data)
        
        conflict_prob = ConflictProbability(
            scenario_name=geopolitical_data.get('scenario_name', 'conflict_escalation'),
            probability=final_probability,
            confidence_interval=confidence_interval,
            time_horizon=geopolitical_data.get('time_horizon', 30),
            escalation_factors=escalation_factors,
            de_escalation_factors=de_escalation_factors,
            risk_level=risk_level,
            assessment_date=datetime.now(),
            metadata={
                'assessment_method': 'multi_factor_conflict_analysis',
                'data_sources': geopolitical_data.get('data_sources', []),
                'model_version': '1.0'
            }
        )
        
        logger.info(f"Conflict probability assessment completed: {final_probability:.3f} ({risk_level})")
        return conflict_prob
        
    async def analyze_weapons_proliferation(self, intelligence_data: Dict[str, Any]) -> WeaponsProliferation:
        """Analyze weapons proliferation patterns"""
        logger.info(f"Analyzing weapons proliferation for {intelligence_data.get('country', 'unknown')}")
        
        country = intelligence_data.get('country', 'unknown')
        
        # Extract proliferation indicators
        technology_data = intelligence_data.get('technology', {})
        supply_chain_data = intelligence_data.get('supply_chain', {})
        detection_data = intelligence_data.get('detection', {})
        countermeasures_data = intelligence_data.get('countermeasures', {})
        
        # Calculate proliferation risk
        proliferation_risk = self._calculate_proliferation_risk(intelligence_data)
        
        # Identify weapon types
        weapon_types = self._identify_weapon_types(technology_data)
        
        # Assess technology level
        technology_level = self._assess_technology_level(technology_data)
        
        # Analyze supply chain
        supply_chain_analysis = self._analyze_supply_chain(supply_chain_data)
        
        # Calculate detection probability
        detection_probability = self._calculate_detection_probability(detection_data)
        
        # Assess countermeasures effectiveness
        countermeasures_effectiveness = self._assess_countermeasures(countermeasures_data)
        
        proliferation = WeaponsProliferation(
            country=country,
            proliferation_risk=proliferation_risk,
            weapon_types=weapon_types,
            technology_level=technology_level,
            supply_chain_analysis=supply_chain_analysis,
            detection_probability=detection_probability,
            countermeasures_effectiveness=countermeasures_effectiveness,
            assessment_date=datetime.now(),
            metadata={
                'assessment_method': 'comprehensive_proliferation_analysis',
                'data_sources': intelligence_data.get('data_sources', []),
                'confidence_level': 0.80
            }
        )
        
        logger.info(f"Weapons proliferation analysis completed for {country}: {proliferation_risk:.3f}")
        return proliferation
        
    def _calculate_personnel_score(self, personnel_data: Dict[str, Any]) -> float:
        """Calculate personnel capability score"""
        total_strength = personnel_data.get('total_strength', 0)
        active_duty = personnel_data.get('active_duty', 0)
        reserves = personnel_data.get('reserves', 0)
        experience_level = personnel_data.get('experience_level', 0.5)
        
        # Normalize strength (assuming 1M personnel = 1.0 score)
        strength_score = min(1.0, total_strength / 1000000)
        
        # Calculate active duty ratio
        active_ratio = active_duty / total_strength if total_strength > 0 else 0
        
        # Combine factors
        personnel_score = (strength_score * 0.4 + active_ratio * 0.3 + experience_level * 0.3)
        
        return min(1.0, personnel_score)
        
    def _calculate_equipment_score(self, equipment_data: Dict[str, Any]) -> float:
        """Calculate equipment quality score"""
        modernization_rate = equipment_data.get('modernization_rate', 0.5)
        maintenance_level = equipment_data.get('maintenance_level', 0.5)
        technology_level = equipment_data.get('technology_level', 0.5)
        
        equipment_score = (modernization_rate * 0.4 + maintenance_level * 0.3 + technology_level * 0.3)
        
        return min(1.0, equipment_score)
        
    def _calculate_training_score(self, training_data: Dict[str, Any]) -> float:
        """Calculate training level score"""
        training_frequency = training_data.get('training_frequency', 0.5)
        training_quality = training_data.get('training_quality', 0.5)
        exercise_participation = training_data.get('exercise_participation', 0.5)
        
        training_score = (training_frequency * 0.4 + training_quality * 0.4 + exercise_participation * 0.2)
        
        return min(1.0, training_score)
        
    def _calculate_logistics_score(self, logistics_data: Dict[str, Any]) -> float:
        """Calculate logistics capacity score"""
        supply_chain_efficiency = logistics_data.get('supply_chain_efficiency', 0.5)
        infrastructure_quality = logistics_data.get('infrastructure_quality', 0.5)
        fuel_capacity = logistics_data.get('fuel_capacity', 0.5)
        
        logistics_score = (supply_chain_efficiency * 0.4 + infrastructure_quality * 0.3 + fuel_capacity * 0.3)
        
        return min(1.0, logistics_score)
        
    def _calculate_command_score(self, command_data: Dict[str, Any]) -> float:
        """Calculate command effectiveness score"""
        leadership_quality = command_data.get('leadership_quality', 0.5)
        communication_systems = command_data.get('communication_systems', 0.5)
        decision_making_speed = command_data.get('decision_making_speed', 0.5)
        
        command_score = (leadership_quality * 0.4 + communication_systems * 0.3 + decision_making_speed * 0.3)
        
        return min(1.0, command_score)
        
    def _calculate_readiness_level(self, country_data: Dict[str, Any]) -> float:
        """Calculate overall readiness level"""
        # Placeholder for readiness calculation
        return 0.75
        
    def _calculate_modernization_index(self, equipment_data: Dict[str, Any]) -> float:
        """Calculate modernization index"""
        # Placeholder for modernization calculation
        return equipment_data.get('modernization_rate', 0.5)
        
    def _calculate_base_conflict_probability(self, tensions: Dict[str, Any], 
                                          historical_conflicts: List[Dict[str, Any]]) -> float:
        """Calculate base conflict probability"""
        # Extract tension indicators
        border_disputes = tensions.get('border_disputes', 0)
        diplomatic_tensions = tensions.get('diplomatic_tensions', 0)
        military_buildup = tensions.get('military_buildup', 0)
        
        # Calculate base probability from tensions
        tension_score = (border_disputes * 0.4 + diplomatic_tensions * 0.3 + military_buildup * 0.3)
        
        # Adjust for historical conflict frequency
        historical_frequency = len(historical_conflicts) / 10  # Normalize to 10 years
        historical_adjustment = min(0.3, historical_frequency * 0.1)
        
        base_probability = tension_score * 0.7 + historical_adjustment
        
        return min(1.0, base_probability)
        
    def _calculate_economic_adjustment(self, economic_factors: Dict[str, Any]) -> float:
        """Calculate economic adjustment to conflict probability"""
        gdp_growth = economic_factors.get('gdp_growth', 0)
        unemployment = economic_factors.get('unemployment', 0.05)
        inflation = economic_factors.get('inflation', 0.02)
        
        # Economic stress increases conflict probability
        economic_stress = max(0, -gdp_growth) + unemployment + inflation
        
        return min(0.2, economic_stress * 0.1)
        
    def _calculate_political_adjustment(self, political_factors: Dict[str, Any]) -> float:
        """Calculate political adjustment to conflict probability"""
        political_stability = political_factors.get('political_stability', 0.5)
        regime_type = political_factors.get('regime_type', 'democratic')
        public_support = political_factors.get('public_support', 0.5)
        
        # Political instability increases conflict probability
        instability_factor = 1.0 - political_stability
        
        # Regime type adjustment
        regime_adjustment = 0.1 if regime_type == 'authoritarian' else 0.0
        
        # Public support adjustment
        support_adjustment = (0.5 - public_support) * 0.1
        
        return min(0.2, instability_factor * 0.1 + regime_adjustment + support_adjustment)
        
    def _determine_risk_level(self, probability: float) -> str:
        """Determine risk level based on probability"""
        if probability < 0.2:
            return 'low'
        elif probability < 0.4:
            return 'medium'
        elif probability < 0.7:
            return 'high'
        else:
            return 'critical'
            
    def _calculate_conflict_confidence_interval(self, probability: float) -> Tuple[float, float]:
        """Calculate confidence interval for conflict probability"""
        uncertainty = 0.1 * probability
        lower = max(0.0, probability - uncertainty)
        upper = min(1.0, probability + uncertainty)
        
        return (lower, upper)
        
    def _identify_escalation_factors(self, geopolitical_data: Dict[str, Any]) -> List[str]:
        """Identify factors that could escalate conflict"""
        factors = []
        
        if geopolitical_data.get('tensions', {}).get('border_disputes', 0) > 0.5:
            factors.append('border_disputes')
            
        if geopolitical_data.get('tensions', {}).get('military_buildup', 0) > 0.6:
            factors.append('military_buildup')
            
        if geopolitical_data.get('economic_factors', {}).get('unemployment', 0) > 0.1:
            factors.append('economic_instability')
            
        return factors
        
    def _identify_de_escalation_factors(self, geopolitical_data: Dict[str, Any]) -> List[str]:
        """Identify factors that could de-escalate conflict"""
        factors = []
        
        if geopolitical_data.get('diplomatic_relations', {}).get('dialogue_level', 0) > 0.7:
            factors.append('diplomatic_dialogue')
            
        if geopolitical_data.get('economic_factors', {}).get('trade_interdependence', 0) > 0.6:
            factors.append('economic_interdependence')
            
        if geopolitical_data.get('international_pressure', {}).get('sanctions_threat', 0) > 0.5:
            factors.append('international_pressure')
            
        return factors
        
    def _calculate_proliferation_risk(self, intelligence_data: Dict[str, Any]) -> float:
        """Calculate weapons proliferation risk"""
        technology_level = intelligence_data.get('technology', {}).get('level', 0.5)
        financial_resources = intelligence_data.get('financial_resources', 0.5)
        political_will = intelligence_data.get('political_will', 0.5)
        international_restrictions = intelligence_data.get('international_restrictions', 0.5)
        
        # Higher technology, resources, and political will increase risk
        # International restrictions decrease risk
        risk = (technology_level * 0.3 + financial_resources * 0.2 + political_will * 0.3) * (1 - international_restrictions * 0.2)
        
        return min(1.0, risk)
        
    def _identify_weapon_types(self, technology_data: Dict[str, Any]) -> List[str]:
        """Identify weapon types based on technology data"""
        weapon_types = []
        
        if technology_data.get('nuclear_capability', 0) > 0.3:
            weapon_types.append('nuclear')
            
        if technology_data.get('chemical_capability', 0) > 0.3:
            weapon_types.append('chemical')
            
        if technology_data.get('biological_capability', 0) > 0.3:
            weapon_types.append('biological')
            
        if technology_data.get('missile_capability', 0) > 0.3:
            weapon_types.append('missile')
            
        return weapon_types
        
    def _assess_technology_level(self, technology_data: Dict[str, Any]) -> str:
        """Assess technology level"""
        overall_level = technology_data.get('overall_level', 0.5)
        
        if overall_level < 0.3:
            return 'basic'
        elif overall_level < 0.6:
            return 'intermediate'
        else:
            return 'advanced'
            
    def _analyze_supply_chain(self, supply_chain_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze supply chain vulnerabilities"""
        return {
            'domestic_capability': supply_chain_data.get('domestic_capability', 0.5),
            'international_suppliers': supply_chain_data.get('international_suppliers', []),
            'vulnerabilities': supply_chain_data.get('vulnerabilities', []),
            'sanctions_impact': supply_chain_data.get('sanctions_impact', 0.5)
        }
        
    def _calculate_detection_probability(self, detection_data: Dict[str, Any]) -> float:
        """Calculate probability of detecting proliferation activities"""
        intelligence_coverage = detection_data.get('intelligence_coverage', 0.5)
        technology_visibility = detection_data.get('technology_visibility', 0.5)
        international_cooperation = detection_data.get('international_cooperation', 0.5)
        
        detection_prob = (intelligence_coverage * 0.4 + technology_visibility * 0.3 + international_cooperation * 0.3)
        
        return min(1.0, detection_prob)
        
    def _assess_countermeasures(self, countermeasures_data: Dict[str, Any]) -> float:
        """Assess effectiveness of countermeasures"""
        diplomatic_pressure = countermeasures_data.get('diplomatic_pressure', 0.5)
        economic_sanctions = countermeasures_data.get('economic_sanctions', 0.5)
        military_deterrence = countermeasures_data.get('military_deterrence', 0.5)
        
        effectiveness = (diplomatic_pressure * 0.3 + economic_sanctions * 0.4 + military_deterrence * 0.3)
        
        return min(1.0, effectiveness)
