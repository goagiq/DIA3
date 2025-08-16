"""
War Capability Assessment Engine

This module provides comprehensive war capability assessment and analysis
for Department of Defense and intelligence community applications.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class CapabilityDomain:
    """Represents a capability domain with its metrics and weights"""
    name: str
    metrics: Dict[str, float]
    weight: float
    description: str


@dataclass
class WarCapabilityScore:
    """Represents a war capability score with breakdown"""
    overall_score: float
    domain_scores: Dict[str, float]
    confidence_level: float
    timestamp: datetime
    recommendations: List[str]
    risk_factors: List[str]


class MilitaryForceCapability:
    """Military force capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'troop_strength': 0.0,
            'equipment_quality': 0.0,
            'training_level': 0.0,
            'combat_experience': 0.0,
            'command_structure': 0.0
        }
        self.weight = 0.25
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess military force capability"""
        try:
            # Extract military data from country_data
            military_data = country_data.get('military', {})
            
            # Calculate individual metrics
            troop_strength = min(military_data.get('troop_strength', 0) / 1000000, 1.0)
            equipment_quality = military_data.get('equipment_modernization', 0.5)
            training_level = military_data.get('training_quality', 0.5)
            combat_experience = military_data.get('combat_experience', 0.5)
            command_structure = military_data.get('command_efficiency', 0.5)
            
            # Weighted average
            score = (
                troop_strength * 0.3 +
                equipment_quality * 0.25 +
                training_level * 0.2 +
                combat_experience * 0.15 +
                command_structure * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing military force capability: {e}")
            return 0.5


class EconomicStrengthCapability:
    """Economic strength capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'gdp': 0.0,
            'industrial_capacity': 0.0,
            'resource_availability': 0.0,
            'financial_stability': 0.0,
            'trade_networks': 0.0
        }
        self.weight = 0.20
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess economic strength capability"""
        try:
            economic_data = country_data.get('economic', {})
            
            gdp = min(economic_data.get('gdp', 0) / 10000, 1.0)  # Normalized to 10T
            industrial_capacity = economic_data.get('industrial_capacity', 0.5)
            resource_availability = economic_data.get('resource_availability', 0.5)
            financial_stability = economic_data.get('financial_stability', 0.5)
            trade_networks = economic_data.get('trade_network_strength', 0.5)
            
            score = (
                gdp * 0.3 +
                industrial_capacity * 0.25 +
                resource_availability * 0.2 +
                financial_stability * 0.15 +
                trade_networks * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing economic strength capability: {e}")
            return 0.5


class TechnologicalAdvantageCapability:
    """Technological advantage capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'cyber_capabilities': 0.0,
            'ai_development': 0.0,
            'space_capabilities': 0.0,
            'advanced_weapons': 0.0,
            'research_development': 0.0
        }
        self.weight = 0.15
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess technological advantage capability"""
        try:
            tech_data = country_data.get('technological', {})
            
            cyber_capabilities = tech_data.get('cyber_capabilities', 0.5)
            ai_development = tech_data.get('ai_development', 0.5)
            space_capabilities = tech_data.get('space_capabilities', 0.5)
            advanced_weapons = tech_data.get('advanced_weapons', 0.5)
            research_development = tech_data.get('research_development', 0.5)
            
            score = (
                cyber_capabilities * 0.25 +
                ai_development * 0.25 +
                space_capabilities * 0.2 +
                advanced_weapons * 0.2 +
                research_development * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing technological advantage capability: {e}")
            return 0.5


class LogisticalSupportCapability:
    """Logistical support capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'infrastructure_quality': 0.0,
            'supply_chain_efficiency': 0.0,
            'transportation_network': 0.0,
            'maintenance_capabilities': 0.0,
            'fuel_availability': 0.0
        }
        self.weight = 0.10
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess logistical support capability"""
        try:
            logistics_data = country_data.get('logistical', {})
            
            infrastructure_quality = logistics_data.get('infrastructure_quality', 0.5)
            supply_chain_efficiency = logistics_data.get('supply_chain_efficiency', 0.5)
            transportation_network = logistics_data.get('transportation_network', 0.5)
            maintenance_capabilities = logistics_data.get('maintenance_capabilities', 0.5)
            fuel_availability = logistics_data.get('fuel_availability', 0.5)
            
            score = (
                infrastructure_quality * 0.25 +
                supply_chain_efficiency * 0.25 +
                transportation_network * 0.2 +
                maintenance_capabilities * 0.2 +
                fuel_availability * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing logistical support capability: {e}")
            return 0.5


class PoliticalWillCapability:
    """Political will capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'government_stability': 0.0,
            'public_support': 0.0,
            'leadership_effectiveness': 0.0,
            'policy_consistency': 0.0,
            'international_standing': 0.0
        }
        self.weight = 0.10
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess political will capability"""
        try:
            political_data = country_data.get('political', {})
            
            government_stability = political_data.get('government_stability', 0.5)
            public_support = political_data.get('public_support', 0.5)
            leadership_effectiveness = political_data.get('leadership_effectiveness', 0.5)
            policy_consistency = political_data.get('policy_consistency', 0.5)
            international_standing = political_data.get('international_standing', 0.5)
            
            score = (
                government_stability * 0.25 +
                public_support * 0.25 +
                leadership_effectiveness * 0.2 +
                policy_consistency * 0.2 +
                international_standing * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing political will capability: {e}")
            return 0.5


class AllianceNetworksCapability:
    """Alliance networks capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'alliance_strength': 0.0,
            'diplomatic_relations': 0.0,
            'international_support': 0.0,
            'coalition_building': 0.0,
            'treaty_obligations': 0.0
        }
        self.weight = 0.08
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess alliance networks capability"""
        try:
            alliance_data = country_data.get('alliances', {})
            
            alliance_strength = alliance_data.get('alliance_strength', 0.5)
            diplomatic_relations = alliance_data.get('diplomatic_relations', 0.5)
            international_support = alliance_data.get('international_support', 0.5)
            coalition_building = alliance_data.get('coalition_building', 0.5)
            treaty_obligations = alliance_data.get('treaty_obligations', 0.5)
            
            score = (
                alliance_strength * 0.3 +
                diplomatic_relations * 0.25 +
                international_support * 0.25 +
                coalition_building * 0.15 +
                treaty_obligations * 0.05
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing alliance networks capability: {e}")
            return 0.5


class GeographicPositionCapability:
    """Geographic position capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'strategic_location': 0.0,
            'terrain_advantage': 0.0,
            'natural_resources': 0.0,
            'climate_conditions': 0.0,
            'borders_security': 0.0
        }
        self.weight = 0.05
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess geographic position capability"""
        try:
            geographic_data = country_data.get('geographic', {})
            
            strategic_location = geographic_data.get('strategic_location', 0.5)
            terrain_advantage = geographic_data.get('terrain_advantage', 0.5)
            natural_resources = geographic_data.get('natural_resources', 0.5)
            climate_conditions = geographic_data.get('climate_conditions', 0.5)
            borders_security = geographic_data.get('borders_security', 0.5)
            
            score = (
                strategic_location * 0.3 +
                terrain_advantage * 0.25 +
                natural_resources * 0.2 +
                climate_conditions * 0.15 +
                borders_security * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing geographic position capability: {e}")
            return 0.5


class ResourceAvailabilityCapability:
    """Resource availability capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'energy_resources': 0.0,
            'raw_materials': 0.0,
            'food_security': 0.0,
            'water_availability': 0.0,
            'critical_minerals': 0.0
        }
        self.weight = 0.04
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess resource availability capability"""
        try:
            resource_data = country_data.get('resources', {})
            
            energy_resources = resource_data.get('energy_resources', 0.5)
            raw_materials = resource_data.get('raw_materials', 0.5)
            food_security = resource_data.get('food_security', 0.5)
            water_availability = resource_data.get('water_availability', 0.5)
            critical_minerals = resource_data.get('critical_minerals', 0.5)
            
            score = (
                energy_resources * 0.3 +
                raw_materials * 0.25 +
                food_security * 0.2 +
                water_availability * 0.15 +
                critical_minerals * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing resource availability capability: {e}")
            return 0.5


class CommandControlCapability:
    """Command and control capability assessment"""
    
    def __init__(self):
        self.metrics = {
            'communication_systems': 0.0,
            'decision_making_speed': 0.0,
            'coordination_efficiency': 0.0,
            'information_sharing': 0.0,
            'command_authority': 0.0
        }
        self.weight = 0.02
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess command and control capability"""
        try:
            command_data = country_data.get('command_control', {})
            
            communication_systems = command_data.get('communication_systems', 0.5)
            decision_making_speed = command_data.get('decision_making_speed', 0.5)
            coordination_efficiency = command_data.get('coordination_efficiency', 0.5)
            information_sharing = command_data.get('information_sharing', 0.5)
            command_authority = command_data.get('command_authority', 0.5)
            
            score = (
                communication_systems * 0.25 +
                decision_making_speed * 0.25 +
                coordination_efficiency * 0.2 +
                information_sharing * 0.2 +
                command_authority * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing command control capability: {e}")
            return 0.5


class IntelligenceCapabilitiesCapability:
    """Intelligence capabilities assessment"""
    
    def __init__(self):
        self.metrics = {
            'sigint_capabilities': 0.0,
            'humint_network': 0.0,
            'osint_analysis': 0.0,
            'technical_intelligence': 0.0,
            'counterintelligence': 0.0
        }
        self.weight = 0.01
        
    async def assess_capability(self, country_data: Dict[str, Any]) -> float:
        """Assess intelligence capabilities"""
        try:
            intelligence_data = country_data.get('intelligence', {})
            
            sigint_capabilities = intelligence_data.get('sigint_capabilities', 0.5)
            humint_network = intelligence_data.get('humint_network', 0.5)
            osint_analysis = intelligence_data.get('osint_analysis', 0.5)
            technical_intelligence = intelligence_data.get('technical_intelligence', 0.5)
            counterintelligence = intelligence_data.get('counterintelligence', 0.5)
            
            score = (
                sigint_capabilities * 0.25 +
                humint_network * 0.25 +
                osint_analysis * 0.2 +
                technical_intelligence * 0.2 +
                counterintelligence * 0.1
            )
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error assessing intelligence capabilities: {e}")
            return 0.5


class WarCapabilityEngine:
    """Interactive war capability assessment and analysis"""
    
    def __init__(self):
        self.capability_domains = {
            'military_force': MilitaryForceCapability(),
            'economic_strength': EconomicStrengthCapability(),
            'technological_advantage': TechnologicalAdvantageCapability(),
            'logistical_support': LogisticalSupportCapability(),
            'political_will': PoliticalWillCapability(),
            'alliance_networks': AllianceNetworksCapability(),
            'geographic_position': GeographicPositionCapability(),
            'resource_availability': ResourceAvailabilityCapability(),
            'command_control': CommandControlCapability(),
            'intelligence_capabilities': IntelligenceCapabilitiesCapability()
        }
        
        logger.info("WarCapabilityEngine initialized successfully")
        
    async def calculate_war_capability_score(
        self, 
        country_data: Dict[str, Any], 
        capability_weights: Optional[Dict[str, float]] = None
    ) -> WarCapabilityScore:
        """Calculate overall war capability score"""
        try:
            logger.info(f"Calculating war capability score for country: {country_data.get('name', 'Unknown')}")
            
            # Use default weights if none provided
            if capability_weights is None:
                capability_weights = {domain: capability.weight for domain, capability in self.capability_domains.items()}
            
            domain_scores = {}
            total_weighted_score = 0.0
            total_weight = 0.0
            
            # Calculate scores for each domain
            for domain_name, capability in self.capability_domains.items():
                domain_score = await capability.assess_capability(country_data)
                domain_scores[domain_name] = domain_score
                
                weight = capability_weights.get(domain_name, capability.weight)
                total_weighted_score += domain_score * weight
                total_weight += weight
                
                logger.debug(f"Domain {domain_name}: Score={domain_score:.3f}, Weight={weight:.3f}")
            
            # Calculate overall score
            overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
            
            # Calculate confidence level based on data completeness
            confidence_level = self._calculate_confidence_level(country_data)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(domain_scores, country_data)
            
            # Identify risk factors
            risk_factors = await self._identify_risk_factors(domain_scores, country_data)
            
            return WarCapabilityScore(
                overall_score=overall_score,
                domain_scores=domain_scores,
                confidence_level=confidence_level,
                timestamp=datetime.now(),
                recommendations=recommendations,
                risk_factors=risk_factors
            )
            
        except Exception as e:
            logger.error(f"Error calculating war capability score: {e}")
            raise
    
    async def generate_recommendations(self, capability_analysis: WarCapabilityScore) -> List[str]:
        """Generate strategic recommendations based on capability analysis"""
        try:
            recommendations = []
            
            # Analyze weak domains
            weak_domains = [
                domain for domain, score in capability_analysis.domain_scores.items()
                if score < 0.4
            ]
            
            for domain in weak_domains:
                if domain == 'military_force':
                    recommendations.append("Increase military spending and modernize equipment")
                elif domain == 'economic_strength':
                    recommendations.append("Strengthen economic resilience and diversify trade")
                elif domain == 'technological_advantage':
                    recommendations.append("Invest in emerging technologies and cyber capabilities")
                elif domain == 'logistical_support':
                    recommendations.append("Improve infrastructure and supply chain efficiency")
                elif domain == 'political_will':
                    recommendations.append("Strengthen government stability and public support")
                elif domain == 'alliance_networks':
                    recommendations.append("Strengthen diplomatic relations and alliances")
                elif domain == 'geographic_position':
                    recommendations.append("Enhance border security and strategic positioning")
                elif domain == 'resource_availability':
                    recommendations.append("Secure critical resources and energy independence")
                elif domain == 'command_control':
                    recommendations.append("Improve communication systems and decision-making")
                elif domain == 'intelligence_capabilities':
                    recommendations.append("Enhance intelligence gathering and analysis capabilities")
            
            # Add general recommendations
            if capability_analysis.overall_score < 0.5:
                recommendations.append("Consider comprehensive defense strategy review")
            
            if len(weak_domains) > 3:
                recommendations.append("Prioritize multi-domain capability development")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]
    
    def _calculate_confidence_level(self, country_data: Dict[str, Any]) -> float:
        """Calculate confidence level based on data completeness"""
        try:
            required_sections = [
                'military', 'economic', 'technological', 'logistical',
                'political', 'alliances', 'geographic', 'resources',
                'command_control', 'intelligence'
            ]
            
            available_sections = sum(1 for section in required_sections if section in country_data)
            confidence = available_sections / len(required_sections)
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence level: {e}")
            return 0.5
    
    async def _generate_recommendations(self, domain_scores: Dict[str, float], country_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on domain scores"""
        try:
            recommendations = []
            
            # Find weakest domains
            sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1])
            
            for domain, score in sorted_domains[:3]:  # Top 3 weakest
                if score < 0.4:
                    recommendations.append(f"Strengthen {domain.replace('_', ' ')} capabilities")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    async def _identify_risk_factors(self, domain_scores: Dict[str, float], country_data: Dict[str, Any]) -> List[str]:
        """Identify risk factors based on capability analysis"""
        try:
            risk_factors = []
            
            # Check for critical weaknesses
            for domain, score in domain_scores.items():
                if score < 0.3:
                    risk_factors.append(f"Critical weakness in {domain.replace('_', ' ')}")
                elif score < 0.5:
                    risk_factors.append(f"Moderate weakness in {domain.replace('_', ' ')}")
            
            # Check for imbalances
            scores = list(domain_scores.values())
            if max(scores) - min(scores) > 0.4:
                risk_factors.append("Significant capability imbalance across domains")
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error identifying risk factors: {e}")
            return []
    
    async def get_capability_breakdown(self, country_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed capability breakdown"""
        try:
            capability_score = await self.calculate_war_capability_score(country_data)
            
            return {
                'overall_score': capability_score.overall_score,
                'domain_scores': capability_score.domain_scores,
                'confidence_level': capability_score.confidence_level,
                'recommendations': capability_score.recommendations,
                'risk_factors': capability_score.risk_factors,
                'timestamp': capability_score.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting capability breakdown: {e}")
            raise
