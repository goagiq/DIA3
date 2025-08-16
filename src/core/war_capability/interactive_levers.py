"""
Interactive Capability Levers

This module provides interactive levers for dynamic capability adjustment
in war capability analysis.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class RangeLever:
    """Represents a range lever with min, max, and current value"""
    min_value: float
    max_value: float
    name: str
    current_value: float = 50.0
    description: str = ""
    unit: str = "%"
    
    def __post_init__(self):
        self.current_value = max(self.min_value, min(self.max_value, self.current_value))


@dataclass
class LeverAdjustment:
    """Represents a lever adjustment with metadata"""
    lever_name: str
    old_value: float
    new_value: float
    timestamp: datetime
    impact_score: float
    description: str


class InteractiveCapabilityLevers:
    """Interactive levers for dynamic capability adjustment"""
    
    def __init__(self):
        self.levers = {
            'military_spending': RangeLever(0, 100, "Military Spending (% of GDP)", 3.5, "Percentage of GDP allocated to military spending"),
            'troop_mobilization': RangeLever(0, 100, "Troop Mobilization (%)", 10.0, "Percentage of available troops mobilized"),
            'weapons_modernization': RangeLever(0, 100, "Weapons Modernization (%)", 60.0, "Percentage of weapons systems modernized"),
            'alliance_strength': RangeLever(0, 100, "Alliance Strength (%)", 70.0, "Strength of military alliances"),
            'economic_sanctions': RangeLever(0, 100, "Economic Sanctions Impact (%)", 0.0, "Impact of economic sanctions on adversary"),
            'cyber_capabilities': RangeLever(0, 100, "Cyber Capabilities (%)", 75.0, "Cyber warfare and defense capabilities"),
            'intelligence_network': RangeLever(0, 100, "Intelligence Network Coverage (%)", 80.0, "Coverage of intelligence network"),
            'logistical_infrastructure': RangeLever(0, 100, "Logistical Infrastructure (%)", 65.0, "Quality of logistical infrastructure"),
            'political_unity': RangeLever(0, 100, "Political Unity (%)", 85.0, "Level of political unity and support"),
            'public_support': RangeLever(0, 100, "Public Support for War (%)", 45.0, "Public support for military action")
        }
        
        self.adjustment_history: List[LeverAdjustment] = []
        self.impact_weights = {
            'military_spending': 0.15,
            'troop_mobilization': 0.12,
            'weapons_modernization': 0.10,
            'alliance_strength': 0.08,
            'economic_sanctions': 0.05,
            'cyber_capabilities': 0.12,
            'intelligence_network': 0.10,
            'logistical_infrastructure': 0.08,
            'political_unity': 0.08,
            'public_support': 0.12
        }
        
        logger.info("InteractiveCapabilityLevers initialized successfully")
    
    async def adjust_lever(self, lever_name: str, value: float) -> Dict[str, Any]:
        """Adjust a specific capability lever"""
        try:
            if lever_name not in self.levers:
                raise ValueError(f"Unknown lever: {lever_name}")
            
            lever = self.levers[lever_name]
            old_value = lever.current_value
            
            # Validate and set new value
            new_value = max(lever.min_value, min(lever.max_value, value))
            lever.current_value = new_value
            
            # Calculate impact score
            impact_score = self._calculate_impact_score(lever_name, old_value, new_value)
            
            # Create adjustment record
            adjustment = LeverAdjustment(
                lever_name=lever_name,
                old_value=old_value,
                new_value=new_value,
                timestamp=datetime.now(),
                impact_score=impact_score,
                description=f"Adjusted {lever.name} from {old_value:.1f} to {new_value:.1f}"
            )
            
            self.adjustment_history.append(adjustment)
            
            logger.info(f"Adjusted lever {lever_name}: {old_value:.1f} -> {new_value:.1f} (impact: {impact_score:.3f})")
            
            return {
                'lever_name': lever_name,
                'old_value': old_value,
                'new_value': new_value,
                'impact_score': impact_score,
                'description': adjustment.description,
                'timestamp': adjustment.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error adjusting lever {lever_name}: {e}")
            raise
    
    async def recalculate_predictions(self, lever_changes: Dict[str, float]) -> Dict[str, Any]:
        """Recalculate predictions based on lever adjustments"""
        try:
            # Apply lever changes
            for lever_name, value in lever_changes.items():
                await self.adjust_lever(lever_name, value)
            
            # Calculate overall impact
            total_impact = sum(
                self._calculate_impact_score(name, 0, lever.current_value) * self.impact_weights.get(name, 0)
                for name, lever in self.levers.items()
            )
            
            # Generate prediction adjustments
            prediction_adjustments = {
                'military_effectiveness': self._calculate_military_effectiveness(),
                'economic_resilience': self._calculate_economic_resilience(),
                'technological_advantage': self._calculate_technological_advantage(),
                'logistical_capacity': self._calculate_logistical_capacity(),
                'political_stability': self._calculate_political_stability(),
                'alliance_cohesion': self._calculate_alliance_cohesion(),
                'cyber_defense': self._calculate_cyber_defense(),
                'intelligence_effectiveness': self._calculate_intelligence_effectiveness(),
                'public_morale': self._calculate_public_morale(),
                'overall_capability': total_impact
            }
            
            return {
                'prediction_adjustments': prediction_adjustments,
                'total_impact': total_impact,
                'lever_states': {name: lever.current_value for name, lever in self.levers.items()},
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error recalculating predictions: {e}")
            raise
    
    async def get_sensitivity_analysis(self, lever_name: str) -> Dict[str, Any]:
        """Get sensitivity analysis for a specific lever"""
        try:
            if lever_name not in self.levers:
                raise ValueError(f"Unknown lever: {lever_name}")
            
            lever = self.levers[lever_name]
            base_value = lever.current_value
            
            # Test different values
            test_values = [0, 25, 50, 75, 100]
            sensitivity_results = {}
            
            for test_value in test_values:
                # Temporarily set lever value
                original_value = lever.current_value
                lever.current_value = test_value
                
                # Calculate impact
                impact = self._calculate_impact_score(lever_name, base_value, test_value)
                sensitivity_results[f"{test_value}%"] = {
                    'value': test_value,
                    'impact': impact,
                    'description': f"Impact at {test_value}% setting"
                }
                
                # Restore original value
                lever.current_value = original_value
            
            return {
                'lever_name': lever_name,
                'current_value': base_value,
                'sensitivity_analysis': sensitivity_results,
                'recommendations': self._generate_lever_recommendations(lever_name, base_value),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting sensitivity analysis for {lever_name}: {e}")
            raise
    
    async def get_all_levers_status(self) -> Dict[str, Any]:
        """Get status of all levers"""
        try:
            lever_status = {}
            
            for name, lever in self.levers.items():
                lever_status[name] = {
                    'name': lever.name,
                    'current_value': lever.current_value,
                    'min_value': lever.min_value,
                    'max_value': lever.max_value,
                    'unit': lever.unit,
                    'description': lever.description,
                    'impact_weight': self.impact_weights.get(name, 0.0)
                }
            
            return {
                'levers': lever_status,
                'total_levers': len(self.levers),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting lever status: {e}")
            raise
    
    async def reset_levers_to_default(self) -> Dict[str, Any]:
        """Reset all levers to default values"""
        try:
            default_values = {
                'military_spending': 3.5,
                'troop_mobilization': 10.0,
                'weapons_modernization': 60.0,
                'alliance_strength': 70.0,
                'economic_sanctions': 0.0,
                'cyber_capabilities': 75.0,
                'intelligence_network': 80.0,
                'logistical_infrastructure': 65.0,
                'political_unity': 85.0,
                'public_support': 45.0
            }
            
            reset_results = {}
            
            for lever_name, default_value in default_values.items():
                result = await self.adjust_lever(lever_name, default_value)
                reset_results[lever_name] = result
            
            logger.info("All levers reset to default values")
            
            return {
                'reset_results': reset_results,
                'message': "All levers reset to default values",
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error resetting levers: {e}")
            raise
    
    def _calculate_impact_score(self, lever_name: str, old_value: float, new_value: float) -> float:
        """Calculate impact score for a lever change"""
        try:
            # Base impact calculation
            value_change = abs(new_value - old_value) / 100.0
            
            # Apply lever-specific multipliers
            multipliers = {
                'military_spending': 1.5,  # High impact
                'troop_mobilization': 1.3,  # High impact
                'weapons_modernization': 1.2,  # Medium-high impact
                'alliance_strength': 1.0,  # Medium impact
                'economic_sanctions': 0.8,  # Medium-low impact
                'cyber_capabilities': 1.4,  # High impact
                'intelligence_network': 1.1,  # Medium-high impact
                'logistical_infrastructure': 1.0,  # Medium impact
                'political_unity': 0.9,  # Medium-low impact
                'public_support': 1.2  # Medium-high impact
            }
            
            multiplier = multipliers.get(lever_name, 1.0)
            impact_score = value_change * multiplier
            
            return min(impact_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating impact score: {e}")
            return 0.0
    
    def _calculate_military_effectiveness(self) -> float:
        """Calculate military effectiveness based on levers"""
        try:
            military_spending = self.levers['military_spending'].current_value / 100.0
            troop_mobilization = self.levers['troop_mobilization'].current_value / 100.0
            weapons_modernization = self.levers['weapons_modernization'].current_value / 100.0
            
            effectiveness = (
                military_spending * 0.4 +
                troop_mobilization * 0.35 +
                weapons_modernization * 0.25
            )
            
            return min(effectiveness, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating military effectiveness: {e}")
            return 0.5
    
    def _calculate_economic_resilience(self) -> float:
        """Calculate economic resilience based on levers"""
        try:
            economic_sanctions = self.levers['economic_sanctions'].current_value / 100.0
            logistical_infrastructure = self.levers['logistical_infrastructure'].current_value / 100.0
            
            # Economic sanctions reduce resilience
            resilience = (
                (1.0 - economic_sanctions * 0.3) * 0.6 +
                logistical_infrastructure * 0.4
            )
            
            return max(resilience, 0.0)
            
        except Exception as e:
            logger.error(f"Error calculating economic resilience: {e}")
            return 0.5
    
    def _calculate_technological_advantage(self) -> float:
        """Calculate technological advantage based on levers"""
        try:
            cyber_capabilities = self.levers['cyber_capabilities'].current_value / 100.0
            weapons_modernization = self.levers['weapons_modernization'].current_value / 100.0
            
            advantage = (
                cyber_capabilities * 0.6 +
                weapons_modernization * 0.4
            )
            
            return min(advantage, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating technological advantage: {e}")
            return 0.5
    
    def _calculate_logistical_capacity(self) -> float:
        """Calculate logistical capacity based on levers"""
        try:
            logistical_infrastructure = self.levers['logistical_infrastructure'].current_value / 100.0
            military_spending = self.levers['military_spending'].current_value / 100.0
            
            capacity = (
                logistical_infrastructure * 0.7 +
                military_spending * 0.3
            )
            
            return min(capacity, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating logistical capacity: {e}")
            return 0.5
    
    def _calculate_political_stability(self) -> float:
        """Calculate political stability based on levers"""
        try:
            political_unity = self.levers['political_unity'].current_value / 100.0
            public_support = self.levers['public_support'].current_value / 100.0
            
            stability = (
                political_unity * 0.6 +
                public_support * 0.4
            )
            
            return min(stability, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating political stability: {e}")
            return 0.5
    
    def _calculate_alliance_cohesion(self) -> float:
        """Calculate alliance cohesion based on levers"""
        try:
            alliance_strength = self.levers['alliance_strength'].current_value / 100.0
            
            return alliance_strength
            
        except Exception as e:
            logger.error(f"Error calculating alliance cohesion: {e}")
            return 0.5
    
    def _calculate_cyber_defense(self) -> float:
        """Calculate cyber defense capability based on levers"""
        try:
            cyber_capabilities = self.levers['cyber_capabilities'].current_value / 100.0
            
            return cyber_capabilities
            
        except Exception as e:
            logger.error(f"Error calculating cyber defense: {e}")
            return 0.5
    
    def _calculate_intelligence_effectiveness(self) -> float:
        """Calculate intelligence effectiveness based on levers"""
        try:
            intelligence_network = self.levers['intelligence_network'].current_value / 100.0
            
            return intelligence_network
            
        except Exception as e:
            logger.error(f"Error calculating intelligence effectiveness: {e}")
            return 0.5
    
    def _calculate_public_morale(self) -> float:
        """Calculate public morale based on levers"""
        try:
            public_support = self.levers['public_support'].current_value / 100.0
            political_unity = self.levers['political_unity'].current_value / 100.0
            
            morale = (
                public_support * 0.7 +
                political_unity * 0.3
            )
            
            return min(morale, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating public morale: {e}")
            return 0.5
    
    def _generate_lever_recommendations(self, lever_name: str, current_value: float) -> List[str]:
        """Generate recommendations for a specific lever"""
        try:
            recommendations = []
            
            if lever_name == 'military_spending':
                if current_value < 2.0:
                    recommendations.append("Consider increasing military spending for enhanced capabilities")
                elif current_value > 8.0:
                    recommendations.append("High military spending may impact economic stability")
            elif lever_name == 'troop_mobilization':
                if current_value < 5.0:
                    recommendations.append("Low mobilization may limit operational capacity")
                elif current_value > 50.0:
                    recommendations.append("High mobilization may strain resources and public support")
            elif lever_name == 'cyber_capabilities':
                if current_value < 50.0:
                    recommendations.append("Enhance cyber capabilities for modern warfare requirements")
            elif lever_name == 'public_support':
                if current_value < 30.0:
                    recommendations.append("Low public support may impact long-term sustainability")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating lever recommendations: {e}")
            return []
