"""
Force Projection Engine
Advanced force projection capabilities simulator using Monte Carlo analysis
with log-normal distributions for realistic military capability modeling

This engine provides comprehensive intelligence analysis capabilities for:
- Military force projection assessment
- Strategic threat evaluation
- Capability timeline forecasting
- Risk assessment and confidence intervals
- Multi-domain support for defense, intelligence, and business applications
"""

import asyncio
import logging
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum

from ..core.monte_carlo.engine import MonteCarloEngine
from ..core.monte_carlo.distributions import DistributionLibrary
from ..core.advanced_analytics.confidence_intervals import ConfidenceIntervalCalculator
from ..core.orchestrator import SentimentOrchestrator

logger = logging.getLogger(__name__)


class AdversaryType(Enum):
    """Enumeration of adversary types for force projection analysis"""
    PEER_ADVERSARY = "peer_adversary"
    NEAR_PEER = "near_peer"
    REGIONAL_POWER = "regional_power"
    EMERGING_THREAT = "emerging_threat"
    NON_STATE_ACTOR = "non_state_actor"
    BUSINESS_COMPETITOR = "business_competitor"
    CYBER_ADVERSARY = "cyber_adversary"


class DomainType(Enum):
    """Enumeration of domain types for multi-domain analysis"""
    DEFENSE = "defense"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    CYBER = "cyber"
    FINANCIAL = "financial"
    GEOPOLITICAL = "geopolitical"


@dataclass
class CapabilityParameters:
    """Data class for capability parameters"""
    mu: float
    sigma: float
    units: str
    domain: str
    description: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None


@dataclass
class SimulationResult:
    """Data class for simulation results"""
    simulation_id: str
    adversary_type: str
    domain_type: str
    capability_analysis: Dict[str, Any]
    readiness_analysis: Dict[str, Any]
    environmental_analysis: Dict[str, Any]
    effectiveness_analysis: Dict[str, Any]
    threat_assessment: Dict[str, Any]
    recommendations: List[str]
    metadata: Dict[str, Any]
    timestamp: datetime


class ForceProjectionEngine:
    """
    Advanced force projection capabilities simulator using Monte Carlo analysis
    with log-normal distributions for realistic capability modeling across multiple domains
    """
    
    def __init__(self, orchestrator: Optional[SentimentOrchestrator] = None):
        """Initialize the force projection engine"""
        self.orchestrator = orchestrator
        self.monte_carlo = MonteCarloEngine()
        self.distributions = DistributionLibrary()
        self.confidence_calculator = ConfidenceIntervalCalculator()
        
        # Initialize domain-specific capability parameters
        self.capability_parameters = self._initialize_capability_parameters()
        
        # Initialize readiness and environmental factors
        self.readiness_factors = self._initialize_readiness_factors()
        self.environmental_factors = self._initialize_environmental_factors()
        
        # Performance tracking
        self.simulation_history = []
        self.performance_metrics = {}
        
        logger.info("Force Projection Engine initialized successfully")
    
    def _initialize_capability_parameters(self) -> Dict[str, Dict[str, CapabilityParameters]]:
        """Initialize capability parameters for different domains"""
        
        return {
            DomainType.DEFENSE.value: {
                'air_force': {
                    'fighter_aircraft': CapabilityParameters(4.5, 0.8, 'squadrons', 'defense', 'Fighter aircraft squadrons'),
                    'bomber_aircraft': CapabilityParameters(3.2, 0.6, 'wings', 'defense', 'Bomber aircraft wings'),
                    'air_defense_systems': CapabilityParameters(5.1, 0.9, 'batteries', 'defense', 'Air defense system batteries'),
                    'airlift_capacity': CapabilityParameters(4.8, 0.7, 'tonnes/day', 'defense', 'Airlift capacity in tonnes per day')
                },
                'naval_forces': {
                    'surface_combatants': CapabilityParameters(4.2, 0.8, 'vessels', 'defense', 'Surface combatant vessels'),
                    'submarines': CapabilityParameters(3.8, 0.7, 'submarines', 'defense', 'Submarine fleet'),
                    'amphibious_ships': CapabilityParameters(3.5, 0.6, 'ships', 'defense', 'Amphibious assault ships'),
                    'naval_aviation': CapabilityParameters(4.0, 0.7, 'aircraft', 'defense', 'Naval aviation aircraft')
                },
                'ground_forces': {
                    'armored_divisions': CapabilityParameters(4.6, 0.8, 'divisions', 'defense', 'Armored divisions'),
                    'mechanized_infantry': CapabilityParameters(5.2, 0.9, 'brigades', 'defense', 'Mechanized infantry brigades'),
                    'artillery_units': CapabilityParameters(4.8, 0.7, 'battalions', 'defense', 'Artillery battalions'),
                    'special_forces': CapabilityParameters(3.9, 0.6, 'teams', 'defense', 'Special forces teams')
                },
                'strategic_forces': {
                    'icbm_silos': CapabilityParameters(3.2, 0.5, 'silos', 'defense', 'ICBM silos'),
                    'mobile_missiles': CapabilityParameters(3.8, 0.7, 'launchers', 'defense', 'Mobile missile launchers'),
                    'strategic_bombers': CapabilityParameters(3.5, 0.6, 'aircraft', 'defense', 'Strategic bomber aircraft'),
                    'nuclear_submarines': CapabilityParameters(3.0, 0.5, 'submarines', 'defense', 'Nuclear submarines')
                }
            },
            DomainType.BUSINESS.value: {
                'market_presence': {
                    'market_share': CapabilityParameters(4.0, 0.8, 'percentage', 'business', 'Market share percentage'),
                    'geographic_reach': CapabilityParameters(3.8, 0.7, 'countries', 'business', 'Geographic presence in countries'),
                    'brand_recognition': CapabilityParameters(4.2, 0.6, 'score', 'business', 'Brand recognition score'),
                    'customer_base': CapabilityParameters(5.0, 0.9, 'millions', 'business', 'Customer base in millions')
                },
                'financial_capabilities': {
                    'revenue_generation': CapabilityParameters(4.5, 0.8, 'billions', 'business', 'Annual revenue in billions'),
                    'profit_margins': CapabilityParameters(3.5, 0.6, 'percentage', 'business', 'Profit margin percentage'),
                    'cash_reserves': CapabilityParameters(4.2, 0.7, 'billions', 'business', 'Cash reserves in billions'),
                    'investment_capacity': CapabilityParameters(3.8, 0.7, 'billions', 'business', 'Investment capacity in billions')
                },
                'operational_capabilities': {
                    'production_capacity': CapabilityParameters(4.8, 0.8, 'units/day', 'business', 'Production capacity units per day'),
                    'supply_chain_strength': CapabilityParameters(4.0, 0.7, 'score', 'business', 'Supply chain strength score'),
                    'technology_advantage': CapabilityParameters(4.2, 0.8, 'score', 'business', 'Technology advantage score'),
                    'workforce_quality': CapabilityParameters(4.5, 0.6, 'score', 'business', 'Workforce quality score')
                }
            },
            DomainType.CYBER.value: {
                'cyber_offensive': {
                    'malware_capabilities': CapabilityParameters(4.2, 0.8, 'score', 'cyber', 'Malware development capabilities'),
                    'exploit_development': CapabilityParameters(4.0, 0.7, 'score', 'cyber', 'Exploit development capabilities'),
                    'social_engineering': CapabilityParameters(3.8, 0.6, 'score', 'cyber', 'Social engineering capabilities'),
                    'infrastructure_attack': CapabilityParameters(4.5, 0.9, 'score', 'cyber', 'Infrastructure attack capabilities')
                },
                'cyber_defensive': {
                    'threat_detection': CapabilityParameters(4.3, 0.7, 'score', 'cyber', 'Threat detection capabilities'),
                    'incident_response': CapabilityParameters(4.1, 0.8, 'score', 'cyber', 'Incident response capabilities'),
                    'vulnerability_management': CapabilityParameters(4.0, 0.6, 'score', 'cyber', 'Vulnerability management capabilities'),
                    'security_awareness': CapabilityParameters(3.9, 0.7, 'score', 'cyber', 'Security awareness capabilities')
                }
            },
            DomainType.FINANCIAL.value: {
                'trading_capabilities': {
                    'trading_volume': CapabilityParameters(4.5, 0.8, 'millions', 'financial', 'Daily trading volume in millions'),
                    'risk_management': CapabilityParameters(4.2, 0.7, 'score', 'financial', 'Risk management capabilities'),
                    'algorithmic_trading': CapabilityParameters(4.0, 0.8, 'score', 'financial', 'Algorithmic trading capabilities'),
                    'market_making': CapabilityParameters(3.8, 0.6, 'score', 'financial', 'Market making capabilities')
                },
                'investment_capabilities': {
                    'portfolio_size': CapabilityParameters(4.8, 0.9, 'billions', 'financial', 'Portfolio size in billions'),
                    'diversification': CapabilityParameters(4.1, 0.7, 'score', 'financial', 'Portfolio diversification score'),
                    'research_capabilities': CapabilityParameters(4.3, 0.8, 'score', 'financial', 'Research capabilities score'),
                    'execution_speed': CapabilityParameters(4.6, 0.7, 'score', 'financial', 'Trade execution speed score')
                }
            }
        }
    
    def _initialize_readiness_factors(self) -> Dict[str, Dict[str, float]]:
        """Initialize operational readiness factors"""
        return {
            'personnel_training': {'mu': 0.75, 'sigma': 0.15, 'distribution': 'beta'},
            'equipment_maintenance': {'mu': 0.80, 'sigma': 0.12, 'distribution': 'beta'},
            'logistics_support': {'mu': 0.70, 'sigma': 0.18, 'distribution': 'beta'},
            'command_control': {'mu': 0.85, 'sigma': 0.10, 'distribution': 'beta'},
            'technology_readiness': {'mu': 0.78, 'sigma': 0.14, 'distribution': 'beta'},
            'organizational_efficiency': {'mu': 0.72, 'sigma': 0.16, 'distribution': 'beta'}
        }
    
    def _initialize_environmental_factors(self) -> Dict[str, Dict[str, float]]:
        """Initialize environmental factors affecting capability projection"""
        return {
            'geographic_distance': {'mu': 0.65, 'sigma': 0.20, 'distribution': 'beta'},
            'alliance_support': {'mu': 0.60, 'sigma': 0.25, 'distribution': 'beta'},
            'economic_sustainability': {'mu': 0.70, 'sigma': 0.18, 'distribution': 'beta'},
            'political_stability': {'mu': 0.75, 'sigma': 0.15, 'distribution': 'beta'},
            'regulatory_environment': {'mu': 0.68, 'sigma': 0.22, 'distribution': 'beta'},
            'market_conditions': {'mu': 0.73, 'sigma': 0.17, 'distribution': 'beta'}
        }
    
    async def simulate_force_projection_capabilities(
        self,
        adversary_type: str = "peer_adversary",
        domain_type: str = "defense",
        time_horizon_months: int = 24,
        num_iterations: int = 10000,
        confidence_level: float = 0.95,
        custom_parameters: Optional[Dict[str, Any]] = None
    ) -> SimulationResult:
        """
        Simulate adversary force projection capabilities using log-normal distributions
        
        Args:
            adversary_type: Type of adversary
            domain_type: Domain type for analysis
            time_horizon_months: Time horizon for projection analysis
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            custom_parameters: Custom parameters for simulation
            
        Returns:
            Comprehensive simulation results with analysis
        """
        
        simulation_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        logger.info(f"Starting force projection simulation {simulation_id} for {adversary_type} in {domain_type} domain")
        
        try:
            # Get capability parameters for the domain
            domain_capabilities = self.capability_parameters.get(domain_type, {})
            if not domain_capabilities:
                raise ValueError(f"Unsupported domain type: {domain_type}")
            
            # Apply custom parameters if provided
            if custom_parameters:
                domain_capabilities = self._apply_custom_parameters(domain_capabilities, custom_parameters)
            
            # Generate capability projections for each area
            capability_results = {}
            
            for area, capabilities in domain_capabilities.items():
                logger.info(f"Simulating {area} capabilities for {domain_type} domain...")
                
                area_results = {}
                for capability, params in capabilities.items():
                    # Generate log-normal distribution for capability levels
                    samples = np.random.lognormal(mean=params.mu, sigma=params.sigma, size=num_iterations)
                    
                    # Apply time-based growth factor
                    time_growth = np.linspace(1.0, 1.2, time_horizon_months)  # 20% growth over 24 months
                    monthly_samples = []
                    
                    for month in range(time_horizon_months):
                        growth_factor = time_growth[month]
                        monthly_capability = samples * growth_factor
                        monthly_samples.append(monthly_capability)
                    
                    monthly_samples = np.array(monthly_samples)
                    
                    # Calculate statistics
                    mean_capability = np.mean(samples)
                    std_capability = np.std(samples)
                    median_capability = np.median(samples)
                    
                    # Calculate percentiles
                    percentiles = {
                        'p10': np.percentile(samples, 10),
                        'p25': np.percentile(samples, 25),
                        'p50': np.percentile(samples, 50),
                        'p75': np.percentile(samples, 75),
                        'p90': np.percentile(samples, 90),
                        'p95': np.percentile(samples, 95),
                        'p99': np.percentile(samples, 99)
                    }
                    
                    # Calculate confidence intervals
                    confidence_interval = self._calculate_confidence_interval(samples, confidence_level)
                    
                    area_results[capability] = {
                        'units': params.units,
                        'description': params.description,
                        'mean': mean_capability,
                        'median': median_capability,
                        'std': std_capability,
                        'percentiles': percentiles,
                        'confidence_interval': confidence_interval,
                        'monthly_projection': monthly_samples.tolist(),
                        'distribution_params': {'mu': params.mu, 'sigma': params.sigma}
                    }
                
                capability_results[area] = area_results
            
            # Simulate operational readiness
            readiness_results = self._simulate_readiness_factors(num_iterations)
            
            # Simulate environmental factors
            environmental_results = self._simulate_environmental_factors(num_iterations)
            
            # Calculate overall effectiveness
            effectiveness_results = self._calculate_overall_effectiveness(
                capability_results, readiness_results, environmental_results, domain_type
            )
            
            # Generate threat assessment
            threat_assessment = self._generate_threat_assessment(
                capability_results, effectiveness_results, readiness_results, adversary_type, domain_type
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(threat_assessment, domain_type)
            
            # Compile results
            result = SimulationResult(
                simulation_id=simulation_id,
                adversary_type=adversary_type,
                domain_type=domain_type,
                capability_analysis=capability_results,
                readiness_analysis=readiness_results,
                environmental_analysis=environmental_results,
                effectiveness_analysis=effectiveness_results,
                threat_assessment=threat_assessment,
                recommendations=recommendations,
                metadata={
                    'time_horizon_months': time_horizon_months,
                    'num_iterations': num_iterations,
                    'confidence_level': confidence_level,
                    'execution_time_seconds': (datetime.now() - start_time).total_seconds(),
                    'custom_parameters': custom_parameters is not None
                },
                timestamp=datetime.now()
            )
            
            # Store in history
            self.simulation_history.append(result)
            
            # Update performance metrics
            self._update_performance_metrics(result)
            
            logger.info(f"Force projection simulation {simulation_id} completed in {(datetime.now() - start_time).total_seconds():.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error in force projection simulation {simulation_id}: {str(e)}")
            raise
    
    def _apply_custom_parameters(
        self, 
        domain_capabilities: Dict[str, Dict[str, CapabilityParameters]], 
        custom_parameters: Dict[str, Any]
    ) -> Dict[str, Dict[str, CapabilityParameters]]:
        """Apply custom parameters to capability definitions"""
        modified_capabilities = domain_capabilities.copy()
        
        for area, capabilities in modified_capabilities.items():
            for capability, params in capabilities.items():
                # Check if custom parameters exist for this capability
                custom_key = f"{area}_{capability}"
                if custom_key in custom_parameters:
                    custom_params = custom_parameters[custom_key]
                    if 'mu' in custom_params:
                        params.mu = custom_params['mu']
                    if 'sigma' in custom_params:
                        params.sigma = custom_params['sigma']
                    if 'units' in custom_params:
                        params.units = custom_params['units']
                    if 'description' in custom_params:
                        params.description = custom_params['description']
        
        return modified_capabilities
    
    def _calculate_confidence_interval(
        self, 
        data: np.ndarray, 
        confidence_level: float
    ) -> Dict[str, float]:
        """Calculate confidence interval for capability data"""
        try:
            mean_val = np.mean(data)
            std_val = np.std(data)
            n = len(data)
            
            # Z-score for confidence level
            z_score = 1.96  # 95% confidence level
            if confidence_level == 0.90:
                z_score = 1.645
            elif confidence_level == 0.99:
                z_score = 2.576
            
            margin_of_error = z_score * (std_val / np.sqrt(n))
            
            return {
                'lower_bound': mean_val - margin_of_error,
                'upper_bound': mean_val + margin_of_error,
                'confidence_level': confidence_level,
                'margin_of_error': margin_of_error
            }
        except Exception as e:
            logger.error(f"Error calculating confidence interval: {str(e)}")
            return {'lower_bound': 0, 'upper_bound': 0, 'confidence_level': confidence_level, 'margin_of_error': 0}
    
    def _simulate_readiness_factors(self, num_iterations: int) -> Dict[str, Any]:
        """Simulate operational readiness factors using beta distributions"""
        readiness_results = {}
        
        for factor, params in self.readiness_factors.items():
            mu = params['mu']
            sigma = params['sigma']
            
            # Convert to beta distribution parameters
            alpha = mu * ((mu * (1 - mu) / (sigma**2)) - 1)
            beta = (1 - mu) * ((mu * (1 - mu) / (sigma**2)) - 1)
            
            # Generate samples from beta distribution
            samples = np.random.beta(alpha, beta, size=num_iterations)
            
            readiness_results[factor] = {
                'mean': np.mean(samples),
                'median': np.median(samples),
                'std': np.std(samples),
                'percentiles': {
                    'p10': np.percentile(samples, 10),
                    'p25': np.percentile(samples, 25),
                    'p50': np.percentile(samples, 50),
                    'p75': np.percentile(samples, 75),
                    'p90': np.percentile(samples, 90)
                },
                'distribution_params': {'alpha': alpha, 'beta': beta}
            }
        
        return readiness_results
    
    def _simulate_environmental_factors(self, num_iterations: int) -> Dict[str, Any]:
        """Simulate environmental factors affecting capability projection"""
        environmental_results = {}
        
        for factor, params in self.environmental_factors.items():
            mu = params['mu']
            sigma = params['sigma']
            
            # Convert to beta distribution parameters
            alpha = mu * ((mu * (1 - mu) / (sigma**2)) - 1)
            beta = (1 - mu) * ((mu * (1 - mu) / (sigma**2)) - 1)
            
            # Generate samples from beta distribution
            samples = np.random.beta(alpha, beta, size=num_iterations)
            
            environmental_results[factor] = {
                'mean': np.mean(samples),
                'median': np.median(samples),
                'std': np.std(samples),
                'percentiles': {
                    'p10': np.percentile(samples, 10),
                    'p25': np.percentile(samples, 25),
                    'p50': np.percentile(samples, 50),
                    'p75': np.percentile(samples, 75),
                    'p90': np.percentile(samples, 90)
                },
                'distribution_params': {'alpha': alpha, 'beta': beta}
            }
        
        return environmental_results
    
    def _calculate_overall_effectiveness(
        self,
        capability_results: Dict[str, Any],
        readiness_results: Dict[str, Any],
        environmental_results: Dict[str, Any],
        domain_type: str
    ) -> Dict[str, Any]:
        """Calculate overall effectiveness based on domain type"""
        
        # Calculate average readiness
        avg_readiness = np.mean([result['mean'] for result in readiness_results.values()])
        
        # Calculate average environmental factor
        avg_environmental = np.mean([result['mean'] for result in environmental_results.values()])
        
        # Calculate capability scores for each area
        capability_scores = {}
        for area, capabilities in capability_results.items():
            area_scores = []
            for capability, data in capabilities.items():
                # Normalize capability to 0-1 scale
                normalized_capability = min(data['mean'] / (data['mean'] * 2), 1.0)
                area_scores.append(normalized_capability)
            
            capability_scores[area] = np.mean(area_scores)
        
        # Calculate overall effectiveness
        overall_capability = np.mean(list(capability_scores.values()))
        overall_effectiveness = overall_capability * avg_readiness * avg_environmental
        
        return {
            'overall_effectiveness': overall_effectiveness,
            'capability_scores': capability_scores,
            'readiness_score': avg_readiness,
            'environmental_score': avg_environmental,
            'effectiveness_breakdown': {
                'capability_contribution': overall_capability,
                'readiness_contribution': avg_readiness,
                'environmental_contribution': avg_environmental
            }
        }
    
    def _generate_threat_assessment(
        self,
        capability_results: Dict[str, Any],
        effectiveness_results: Dict[str, Any],
        readiness_results: Dict[str, Any],
        adversary_type: str,
        domain_type: str
    ) -> Dict[str, Any]:
        """Generate comprehensive threat assessment"""
        
        overall_effectiveness = effectiveness_results['overall_effectiveness']
        
        # Define threat levels based on effectiveness and domain
        if domain_type == DomainType.DEFENSE.value:
            threat_levels = {
                0.8: "CRITICAL",
                0.6: "HIGH", 
                0.4: "MODERATE",
                0.2: "LOW"
            }
        elif domain_type == DomainType.BUSINESS.value:
            threat_levels = {
                0.8: "HIGH_COMPETITION",
                0.6: "MODERATE_COMPETITION",
                0.4: "LOW_COMPETITION", 
                0.2: "MINIMAL_COMPETITION"
            }
        else:
            threat_levels = {
                0.8: "HIGH_THREAT",
                0.6: "MODERATE_THREAT",
                0.4: "LOW_THREAT",
                0.2: "MINIMAL_THREAT"
            }
        
        # Determine threat level
        threat_level = "MINIMAL"
        for threshold, level in sorted(threat_levels.items(), reverse=True):
            if overall_effectiveness >= threshold:
                threat_level = level
                break
        
        # Generate threat description
        threat_descriptions = {
            "CRITICAL": "Extremely high force projection capability",
            "HIGH": "High force projection capability",
            "MODERATE": "Moderate force projection capability", 
            "LOW": "Low force projection capability",
            "MINIMAL": "Minimal force projection capability",
            "HIGH_COMPETITION": "High competitive threat level",
            "MODERATE_COMPETITION": "Moderate competitive threat level",
            "LOW_COMPETITION": "Low competitive threat level",
            "MINIMAL_COMPETITION": "Minimal competitive threat level",
            "HIGH_THREAT": "High threat level",
            "MODERATE_THREAT": "Moderate threat level",
            "LOW_THREAT": "Low threat level",
            "MINIMAL_THREAT": "Minimal threat level"
        }
        
        threat_description = threat_descriptions.get(threat_level, "Unknown threat level")
        
        # Identify strongest capability areas
        capability_scores = effectiveness_results['capability_scores']
        strongest_areas = sorted(capability_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Identify potential vulnerabilities
        readiness_scores = {k: v['mean'] for k, v in readiness_results.items()}
        vulnerabilities = sorted(readiness_scores.items(), key=lambda x: x[1])[:2]
        
        return {
            'threat_level': threat_level,
            'threat_description': threat_description,
            'overall_effectiveness_score': overall_effectiveness,
            'strongest_capability_areas': strongest_areas,
            'potential_vulnerabilities': vulnerabilities,
            'adversary_type': adversary_type,
            'domain_type': domain_type,
            'assessment_timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, threat_assessment: Dict[str, Any], domain_type: str) -> List[str]:
        """Generate strategic recommendations based on threat assessment and domain"""
        recommendations = []
        
        threat_level = threat_assessment['threat_level']
        strongest_areas = threat_assessment['strongest_capability_areas']
        vulnerabilities = threat_assessment['potential_vulnerabilities']
        
        # Domain-specific recommendations
        if domain_type == DomainType.DEFENSE.value:
            if threat_level in ["CRITICAL", "HIGH"]:
                recommendations.extend([
                    "Immediate intelligence collection focus on adversary force modernization programs",
                    "Enhanced defensive posture and capability development",
                    "Alliance strengthening and coalition building",
                    "Diplomatic engagement to reduce tensions and build confidence measures"
                ])
            elif threat_level == "MODERATE":
                recommendations.extend([
                    "Continued monitoring of adversary capability development",
                    "Selective capability enhancement in critical areas",
                    "Maintenance of current defensive posture"
                ])
            else:
                recommendations.extend([
                    "Routine intelligence monitoring",
                    "Maintenance of basic defensive capabilities",
                    "Focus on diplomatic and economic engagement"
                ])
        
        elif domain_type == DomainType.BUSINESS.value:
            if threat_level in ["HIGH_COMPETITION", "MODERATE_COMPETITION"]:
                recommendations.extend([
                    "Accelerate product development and innovation initiatives",
                    "Strengthen market position through strategic acquisitions",
                    "Enhance customer retention and loyalty programs",
                    "Invest in competitive intelligence and market research"
                ])
            else:
                recommendations.extend([
                    "Maintain current market position and customer relationships",
                    "Focus on operational efficiency and cost optimization",
                    "Monitor competitive landscape for emerging threats"
                ])
        
        elif domain_type == DomainType.CYBER.value:
            if threat_level in ["HIGH_THREAT", "MODERATE_THREAT"]:
                recommendations.extend([
                    "Implement advanced threat detection and response systems",
                    "Enhance cybersecurity training and awareness programs",
                    "Strengthen incident response and recovery capabilities",
                    "Develop cyber threat intelligence sharing partnerships"
                ])
            else:
                recommendations.extend([
                    "Maintain basic cybersecurity hygiene and best practices",
                    "Regular security assessments and vulnerability management",
                    "Monitor emerging cyber threats and attack vectors"
                ])
        
        else:
            # Generic recommendations for other domains
            if "HIGH" in threat_level or "CRITICAL" in threat_level:
                recommendations.extend([
                    "Immediate action required to address high threat level",
                    "Enhanced monitoring and intelligence collection",
                    "Strategic planning for threat mitigation",
                    "Resource allocation for counter-capability development"
                ])
            else:
                recommendations.extend([
                    "Continued monitoring and assessment",
                    "Maintenance of current capabilities",
                    "Strategic planning for future contingencies"
                ])
        
        # Add specific recommendations based on strongest areas
        for area, score in strongest_areas:
            recommendations.append(f"Prioritize counter-capabilities against {area.replace('_', ' ')}")
        
        # Add recommendations based on vulnerabilities
        for vulnerability, score in vulnerabilities:
            recommendations.append(f"Exploit potential vulnerability in {vulnerability.replace('_', ' ')}")
        
        return recommendations
    
    def _update_performance_metrics(self, result: SimulationResult):
        """Update performance metrics with simulation results"""
        execution_time = result.metadata['execution_time_seconds']
        
        if 'execution_times' not in self.performance_metrics:
            self.performance_metrics['execution_times'] = []
        
        self.performance_metrics['execution_times'].append(execution_time)
        
        # Keep only last 100 execution times
        if len(self.performance_metrics['execution_times']) > 100:
            self.performance_metrics['execution_times'] = self.performance_metrics['execution_times'][-100:]
        
        # Update average execution time
        self.performance_metrics['avg_execution_time'] = np.mean(self.performance_metrics['execution_times'])
        self.performance_metrics['total_simulations'] = len(self.simulation_history)
    
    def get_simulation_history(self, limit: int = 50) -> List[SimulationResult]:
        """Get recent simulation history"""
        return self.simulation_history[-limit:] if self.simulation_history else []
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.performance_metrics.copy()
    
    def export_simulation_result(self, result: SimulationResult, format: str = "json") -> str:
        """Export simulation result in specified format"""
        if format.lower() == "json":
            # Convert dataclass to dict for JSON serialization
            result_dict = asdict(result)
            # Convert datetime to string
            result_dict['timestamp'] = result_dict['timestamp'].isoformat()
            return json.dumps(result_dict, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def create_visualization(self, result: SimulationResult, save_path: Optional[str] = None) -> str:
        """Create visualization of simulation results"""
        try:
            # Set up the plotting style
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle(f'Force Projection Analysis - {result.domain_type.title()} Domain', fontsize=16, fontweight='bold')
            
            # 1. Capability Distribution by Area
            ax1 = axes[0, 0]
            capability_areas = list(result.capability_analysis.keys())
            capability_scores = [result.effectiveness_analysis['capability_scores'][area] for area in capability_areas]
            
            bars = ax1.bar(capability_areas, capability_scores, color='skyblue', alpha=0.7)
            ax1.set_title('Capability Scores by Area')
            ax1.set_ylabel('Normalized Capability Score')
            ax1.set_ylim(0, 1)
            
            # Add value labels on bars
            for bar, score in zip(bars, capability_scores):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{score:.3f}', ha='center', va='bottom')
            
            # 2. Readiness Factors
            ax2 = axes[0, 1]
            readiness_factors = list(result.readiness_analysis.keys())
            readiness_scores = [result.readiness_analysis[factor]['mean'] for factor in readiness_factors]
            
            bars = ax2.bar(readiness_factors, readiness_scores, color='lightgreen', alpha=0.7)
            ax2.set_title('Operational Readiness Factors')
            ax2.set_ylabel('Readiness Score')
            ax2.set_ylim(0, 1)
            ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, score in zip(bars, readiness_scores):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{score:.3f}', ha='center', va='bottom')
            
            # 3. Environmental Factors
            ax3 = axes[1, 0]
            environmental_factors = list(result.environmental_analysis.keys())
            environmental_scores = [result.environmental_analysis[factor]['mean'] for factor in environmental_factors]
            
            bars = ax3.bar(environmental_factors, environmental_scores, color='lightcoral', alpha=0.7)
            ax3.set_title('Environmental Factors')
            ax3.set_ylabel('Factor Score')
            ax3.set_ylim(0, 1)
            ax3.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, score in zip(bars, environmental_scores):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{score:.3f}', ha='center', va='bottom')
            
            # 4. Overall Effectiveness Breakdown
            ax4 = axes[1, 1]
            breakdown = result.effectiveness_analysis['effectiveness_breakdown']
            components = list(breakdown.keys())
            values = list(breakdown.values())
            
            colors = ['skyblue', 'lightgreen', 'lightcoral']
            wedges, texts, autotexts = ax4.pie(values, labels=components, autopct='%1.1f%%', 
                                              colors=colors, startangle=90)
            ax4.set_title('Overall Effectiveness Breakdown')
            
            # Add overall effectiveness score as text
            overall_score = result.effectiveness_analysis['overall_effectiveness']
            ax4.text(0, -1.2, f'Overall Effectiveness: {overall_score:.3f}', 
                    ha='center', va='center', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Visualization saved to {save_path}")
                return save_path
            
            # Return base64 encoded image for API responses
            import io
            import base64
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            logger.error(f"Error creating visualization: {str(e)}")
            raise
