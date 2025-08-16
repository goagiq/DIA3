"""
Intelligence Community-Specific Analysis Models
Intelligence analysis models for intelligence community applications
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class SignalIntelligence:
    """Signals intelligence analysis structure"""
    source: str
    signal_type: str
    frequency_range: Tuple[float, float]
    strength: float
    reliability_score: float
    threat_level: str  # 'low', 'medium', 'high', 'critical'
    pattern_indicators: List[str]
    analysis_date: datetime
    metadata: Dict[str, Any]

@dataclass
class HumanIntelligence:
    """Human intelligence assessment structure"""
    source_id: str
    reliability_score: float
    access_level: str  # 'low', 'medium', 'high'
    reporting_frequency: float
    information_quality: float
    corroboration_level: float
    risk_assessment: str  # 'low', 'medium', 'high'
    last_contact: datetime
    metadata: Dict[str, Any]

@dataclass
class TerroristActivity:
    """Terrorist activity prediction structure"""
    threat_level: str  # 'low', 'medium', 'high', 'critical'
    probability: float
    confidence_interval: Tuple[float, float]
    time_horizon: int  # days
    target_types: List[str]
    attack_methods: List[str]
    indicators: List[str]
    assessment_date: datetime
    metadata: Dict[str, Any]

class IntelligenceAnalysisModels:
    """Intelligence community-specific analysis models"""
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
            
        self.config = config
        self.sigint_models = {}
        self.humint_models = {}
        self.terrorism_models = {}
        
        logger.info("Initialized Intelligence Analysis Models")
        
    async def analyze_signal_intelligence(self, sigint_data: Dict[str, Any]) -> SignalIntelligence:
        """Analyze signals intelligence patterns"""
        logger.info(f"Analyzing signals intelligence from {sigint_data.get('source', 'unknown')}")
        
        source = sigint_data.get('source', 'unknown')
        signal_type = sigint_data.get('signal_type', 'unknown')
        
        # Extract signal characteristics
        frequency_data = sigint_data.get('frequency', {})
        strength_data = sigint_data.get('strength', {})
        pattern_data = sigint_data.get('patterns', {})
        
        # Calculate signal strength
        signal_strength = self._calculate_signal_strength(strength_data)
        
        # Assess reliability
        reliability_score = self._assess_sigint_reliability(sigint_data)
        
        # Determine threat level
        threat_level = self._determine_sigint_threat_level(sigint_data)
        
        # Identify pattern indicators
        pattern_indicators = self._identify_sigint_patterns(pattern_data)
        
        sigint_analysis = SignalIntelligence(
            source=source,
            signal_type=signal_type,
            frequency_range=frequency_data.get('range', (0.0, 0.0)),
            strength=signal_strength,
            reliability_score=reliability_score,
            threat_level=threat_level,
            pattern_indicators=pattern_indicators,
            analysis_date=datetime.now(),
            metadata={
                'analysis_method': 'comprehensive_sigint_analysis',
                'data_sources': sigint_data.get('data_sources', []),
                'confidence_level': 0.85
            }
        )
        
        logger.info(f"Signals intelligence analysis completed: {threat_level} threat level")
        return sigint_analysis
        
    async def assess_human_intelligence(self, humint_data: Dict[str, Any]) -> HumanIntelligence:
        """Assess human intelligence reliability and patterns"""
        logger.info(f"Assessing human intelligence source {humint_data.get('source_id', 'unknown')}")
        
        source_id = humint_data.get('source_id', 'unknown')
        
        # Extract source characteristics
        reliability_indicators = humint_data.get('reliability_indicators', {})
        access_data = humint_data.get('access', {})
        reporting_data = humint_data.get('reporting', {})
        quality_data = humint_data.get('quality', {})
        
        # Calculate reliability score
        reliability_score = self._calculate_humint_reliability(reliability_indicators)
        
        # Assess access level
        access_level = self._assess_access_level(access_data)
        
        # Calculate reporting frequency
        reporting_frequency = self._calculate_reporting_frequency(reporting_data)
        
        # Assess information quality
        information_quality = self._assess_information_quality(quality_data)
        
        # Calculate corroboration level
        corroboration_level = self._calculate_corroboration_level(humint_data)
        
        # Assess risk
        risk_assessment = self._assess_humint_risk(humint_data)
        
        # Get last contact
        last_contact = humint_data.get('last_contact', datetime.now())
        
        humint_assessment = HumanIntelligence(
            source_id=source_id,
            reliability_score=reliability_score,
            access_level=access_level,
            reporting_frequency=reporting_frequency,
            information_quality=information_quality,
            corroboration_level=corroboration_level,
            risk_assessment=risk_assessment,
            last_contact=last_contact,
            metadata={
                'assessment_method': 'comprehensive_humint_analysis',
                'data_sources': humint_data.get('data_sources', []),
                'confidence_level': 0.80
            }
        )
        
        logger.info(f"Human intelligence assessment completed: {reliability_score:.3f} reliability")
        return humint_assessment
        
    async def predict_terrorist_activities(self, threat_data: Dict[str, Any]) -> TerroristActivity:
        """Predict terrorist activities and patterns"""
        logger.info("Predicting terrorist activities")
        
        # Extract threat indicators
        threat_indicators = threat_data.get('threat_indicators', {})
        historical_data = threat_data.get('historical_activities', [])
        intelligence_reports = threat_data.get('intelligence_reports', [])
        environmental_factors = threat_data.get('environmental_factors', {})
        
        # Calculate threat probability
        threat_probability = self._calculate_terrorist_threat_probability(
            threat_indicators, historical_data, intelligence_reports, environmental_factors
        )
        
        # Determine threat level
        threat_level = self._determine_terrorist_threat_level(threat_probability)
        
        # Calculate confidence interval
        confidence_interval = self._calculate_terrorist_confidence_interval(threat_probability)
        
        # Identify target types
        target_types = self._identify_target_types(threat_data)
        
        # Identify attack methods
        attack_methods = self._identify_attack_methods(threat_data)
        
        # Identify indicators
        indicators = self._identify_terrorist_indicators(threat_data)
        
        terrorist_prediction = TerroristActivity(
            threat_level=threat_level,
            probability=threat_probability,
            confidence_interval=confidence_interval,
            time_horizon=threat_data.get('time_horizon', 30),
            target_types=target_types,
            attack_methods=attack_methods,
            indicators=indicators,
            assessment_date=datetime.now(),
            metadata={
                'prediction_method': 'multi_factor_terrorism_analysis',
                'data_sources': threat_data.get('data_sources', []),
                'model_version': '1.0'
            }
        )
        
        logger.info(f"Terrorist activity prediction completed: {threat_level} threat level")
        return terrorist_prediction
        
    def _calculate_signal_strength(self, strength_data: Dict[str, Any]) -> float:
        """Calculate signal strength"""
        power_level = strength_data.get('power_level', 0.5)
        signal_to_noise = strength_data.get('signal_to_noise_ratio', 0.5)
        distance_factor = strength_data.get('distance_factor', 0.5)
        
        # Combine factors to calculate overall strength
        strength = (power_level * 0.4 + signal_to_noise * 0.4 + distance_factor * 0.2)
        
        return min(1.0, strength)
        
    def _assess_sigint_reliability(self, sigint_data: Dict[str, Any]) -> float:
        """Assess reliability of signals intelligence"""
        signal_quality = sigint_data.get('signal_quality', 0.5)
        source_reliability = sigint_data.get('source_reliability', 0.5)
        technical_accuracy = sigint_data.get('technical_accuracy', 0.5)
        
        reliability = (signal_quality * 0.4 + source_reliability * 0.3 + technical_accuracy * 0.3)
        
        return min(1.0, reliability)
        
    def _determine_sigint_threat_level(self, sigint_data: Dict[str, Any]) -> str:
        """Determine threat level from signals intelligence"""
        threat_indicators = sigint_data.get('threat_indicators', {})
        
        # Calculate threat score
        communication_volume = threat_indicators.get('communication_volume', 0.5)
        encryption_level = threat_indicators.get('encryption_level', 0.5)
        frequency_anomalies = threat_indicators.get('frequency_anomalies', 0.5)
        
        threat_score = (communication_volume * 0.4 + encryption_level * 0.3 + frequency_anomalies * 0.3)
        
        if threat_score < 0.3:
            return 'low'
        elif threat_score < 0.6:
            return 'medium'
        elif threat_score < 0.8:
            return 'high'
        else:
            return 'critical'
            
    def _identify_sigint_patterns(self, pattern_data: Dict[str, Any]) -> List[str]:
        """Identify patterns in signals intelligence"""
        patterns = []
        
        if pattern_data.get('encrypted_communications', 0) > 0.6:
            patterns.append('encrypted_communications')
            
        if pattern_data.get('frequency_hopping', 0) > 0.5:
            patterns.append('frequency_hopping')
            
        if pattern_data.get('burst_transmissions', 0) > 0.4:
            patterns.append('burst_transmissions')
            
        if pattern_data.get('covert_channels', 0) > 0.3:
            patterns.append('covert_channels')
            
        return patterns
        
    def _calculate_humint_reliability(self, reliability_indicators: Dict[str, Any]) -> float:
        """Calculate human intelligence reliability score"""
        historical_accuracy = reliability_indicators.get('historical_accuracy', 0.5)
        source_motivation = reliability_indicators.get('source_motivation', 0.5)
        corroboration_history = reliability_indicators.get('corroboration_history', 0.5)
        reporting_consistency = reliability_indicators.get('reporting_consistency', 0.5)
        
        reliability = (
            historical_accuracy * 0.3 +
            source_motivation * 0.2 +
            corroboration_history * 0.3 +
            reporting_consistency * 0.2
        )
        
        return min(1.0, reliability)
        
    def _assess_access_level(self, access_data: Dict[str, Any]) -> str:
        """Assess access level of human intelligence source"""
        access_indicators = access_data.get('indicators', {})
        
        # Calculate access score
        proximity_to_target = access_indicators.get('proximity_to_target', 0.5)
        clearance_level = access_indicators.get('clearance_level', 0.5)
        relationship_quality = access_indicators.get('relationship_quality', 0.5)
        
        access_score = (proximity_to_target * 0.4 + clearance_level * 0.3 + relationship_quality * 0.3)
        
        if access_score < 0.4:
            return 'low'
        elif access_score < 0.7:
            return 'medium'
        else:
            return 'high'
            
    def _calculate_reporting_frequency(self, reporting_data: Dict[str, Any]) -> float:
        """Calculate reporting frequency"""
        reports_per_month = reporting_data.get('reports_per_month', 1)
        average_interval = reporting_data.get('average_interval_days', 30)
        
        # Normalize to 0-1 scale (assuming 10 reports/month = 1.0)
        frequency = min(1.0, reports_per_month / 10)
        
        return frequency
        
    def _assess_information_quality(self, quality_data: Dict[str, Any]) -> float:
        """Assess information quality"""
        detail_level = quality_data.get('detail_level', 0.5)
        timeliness = quality_data.get('timeliness', 0.5)
        specificity = quality_data.get('specificity', 0.5)
        
        quality = (detail_level * 0.4 + timeliness * 0.3 + specificity * 0.3)
        
        return min(1.0, quality)
        
    def _calculate_corroboration_level(self, humint_data: Dict[str, Any]) -> float:
        """Calculate corroboration level"""
        corroborating_sources = humint_data.get('corroborating_sources', [])
        technical_verification = humint_data.get('technical_verification', 0.5)
        open_source_confirmation = humint_data.get('open_source_confirmation', 0.5)
        
        # Calculate corroboration score
        source_corroboration = min(1.0, len(corroborating_sources) / 3)  # Normalize to 3 sources
        technical_corroboration = technical_verification
        open_source_corroboration = open_source_confirmation
        
        corroboration = (source_corroboration * 0.5 + technical_corroboration * 0.3 + open_source_corroboration * 0.2)
        
        return min(1.0, corroboration)
        
    def _assess_humint_risk(self, humint_data: Dict[str, Any]) -> str:
        """Assess risk level for human intelligence source"""
        risk_indicators = humint_data.get('risk_indicators', {})
        
        # Calculate risk score
        exposure_risk = risk_indicators.get('exposure_risk', 0.5)
        counterintelligence_threat = risk_indicators.get('counterintelligence_threat', 0.5)
        source_stability = risk_indicators.get('source_stability', 0.5)
        
        risk_score = (exposure_risk * 0.4 + counterintelligence_threat * 0.4 + (1 - source_stability) * 0.2)
        
        if risk_score < 0.3:
            return 'low'
        elif risk_score < 0.6:
            return 'medium'
        else:
            return 'high'
            
    def _calculate_terrorist_threat_probability(self, threat_indicators: Dict[str, Any],
                                              historical_data: List[Dict[str, Any]],
                                              intelligence_reports: List[Dict[str, Any]],
                                              environmental_factors: Dict[str, Any]) -> float:
        """Calculate terrorist threat probability"""
        
        # Base probability from threat indicators
        base_probability = self._calculate_base_terrorist_probability(threat_indicators)
        
        # Historical adjustment
        historical_adjustment = self._calculate_historical_adjustment(historical_data)
        
        # Intelligence reports adjustment
        intelligence_adjustment = self._calculate_intelligence_adjustment(intelligence_reports)
        
        # Environmental factors adjustment
        environmental_adjustment = self._calculate_environmental_adjustment(environmental_factors)
        
        # Calculate final probability
        final_probability = base_probability + historical_adjustment + intelligence_adjustment + environmental_adjustment
        
        return max(0.0, min(1.0, final_probability))
        
    def _calculate_base_terrorist_probability(self, threat_indicators: Dict[str, Any]) -> float:
        """Calculate base terrorist threat probability"""
        # Extract key indicators
        threat_level = threat_indicators.get('threat_level', 0.5)
        attack_planning = threat_indicators.get('attack_planning', 0.5)
        capability_level = threat_indicators.get('capability_level', 0.5)
        intent_level = threat_indicators.get('intent_level', 0.5)
        
        # Calculate base probability
        base_prob = (threat_level * 0.3 + attack_planning * 0.3 + capability_level * 0.2 + intent_level * 0.2)
        
        return min(1.0, base_prob)
        
    def _calculate_historical_adjustment(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate adjustment based on historical data"""
        if not historical_data:
            return 0.0
            
        # Calculate recent activity frequency
        recent_activities = [d for d in historical_data if d.get('days_ago', 365) < 90]
        activity_frequency = len(recent_activities) / 3  # Normalize to 3 months
        
        return min(0.2, activity_frequency * 0.1)
        
    def _calculate_intelligence_adjustment(self, intelligence_reports: List[Dict[str, Any]]) -> float:
        """Calculate adjustment based on intelligence reports"""
        if not intelligence_reports:
            return 0.0
            
        # Calculate average threat level from reports
        threat_levels = [r.get('threat_level', 0.5) for r in intelligence_reports]
        avg_threat = sum(threat_levels) / len(threat_levels)
        
        return min(0.2, avg_threat * 0.1)
        
    def _calculate_environmental_adjustment(self, environmental_factors: Dict[str, Any]) -> float:
        """Calculate adjustment based on environmental factors"""
        # Extract environmental factors
        political_instability = environmental_factors.get('political_instability', 0.5)
        economic_stress = environmental_factors.get('economic_stress', 0.5)
        social_tensions = environmental_factors.get('social_tensions', 0.5)
        
        # Calculate environmental adjustment
        env_adjustment = (political_instability * 0.4 + economic_stress * 0.3 + social_tensions * 0.3) * 0.1
        
        return min(0.2, env_adjustment)
        
    def _determine_terrorist_threat_level(self, probability: float) -> str:
        """Determine terrorist threat level based on probability"""
        if probability < 0.2:
            return 'low'
        elif probability < 0.4:
            return 'medium'
        elif probability < 0.7:
            return 'high'
        else:
            return 'critical'
            
    def _calculate_terrorist_confidence_interval(self, probability: float) -> Tuple[float, float]:
        """Calculate confidence interval for terrorist threat prediction"""
        uncertainty = 0.15 * probability
        lower = max(0.0, probability - uncertainty)
        upper = min(1.0, probability + uncertainty)
        
        return (lower, upper)
        
    def _identify_target_types(self, threat_data: Dict[str, Any]) -> List[str]:
        """Identify potential target types"""
        target_analysis = threat_data.get('target_analysis', {})
        target_types = []
        
        if target_analysis.get('government_facilities', 0) > 0.5:
            target_types.append('government_facilities')
            
        if target_analysis.get('critical_infrastructure', 0) > 0.5:
            target_types.append('critical_infrastructure')
            
        if target_analysis.get('transportation_hubs', 0) > 0.5:
            target_types.append('transportation_hubs')
            
        if target_analysis.get('crowded_places', 0) > 0.5:
            target_types.append('crowded_places')
            
        if target_analysis.get('military_targets', 0) > 0.5:
            target_types.append('military_targets')
            
        return target_types
        
    def _identify_attack_methods(self, threat_data: Dict[str, Any]) -> List[str]:
        """Identify potential attack methods"""
        method_analysis = threat_data.get('method_analysis', {})
        attack_methods = []
        
        if method_analysis.get('explosive_devices', 0) > 0.5:
            attack_methods.append('explosive_devices')
            
        if method_analysis.get('firearms', 0) > 0.5:
            attack_methods.append('firearms')
            
        if method_analysis.get('vehicle_attacks', 0) > 0.5:
            attack_methods.append('vehicle_attacks')
            
        if method_analysis.get('cyber_attacks', 0) > 0.5:
            attack_methods.append('cyber_attacks')
            
        if method_analysis.get('chemical_biological', 0) > 0.5:
            attack_methods.append('chemical_biological')
            
        return attack_methods
        
    def _identify_terrorist_indicators(self, threat_data: Dict[str, Any]) -> List[str]:
        """Identify terrorist threat indicators"""
        indicators = threat_data.get('indicators', {})
        identified_indicators = []
        
        if indicators.get('surveillance_activity', 0) > 0.6:
            identified_indicators.append('surveillance_activity')
            
        if indicators.get('weapon_acquisition', 0) > 0.5:
            identified_indicators.append('weapon_acquisition')
            
        if indicators.get('training_activity', 0) > 0.5:
            identified_indicators.append('training_activity')
            
        if indicators.get('communication_patterns', 0) > 0.5:
            identified_indicators.append('communication_patterns')
            
        if indicators.get('financial_activity', 0) > 0.5:
            identified_indicators.append('financial_activity')
            
        return identified_indicators
