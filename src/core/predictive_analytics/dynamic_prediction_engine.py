"""
Dynamic Prediction Engine

This module provides dynamic prediction capabilities with real-time updates
for war capability analysis and forecasting.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class PredictionUpdate:
    """Represents a prediction update with metadata"""
    prediction_id: str
    old_prediction: float
    new_prediction: float
    confidence_interval: Tuple[float, float]
    timestamp: datetime
    update_reason: str
    lever_changes: Dict[str, float]


@dataclass
class Scenario:
    """Represents a scenario with its parameters and predictions"""
    scenario_id: str
    name: str
    description: str
    lever_settings: Dict[str, float]
    predictions: Dict[str, float]
    confidence_level: float
    probability: float
    timestamp: datetime


class DynamicPredictionEngine:
    """Dynamic prediction engine with real-time updates"""
    
    def __init__(self):
        self.prediction_history: List[PredictionUpdate] = []
        self.scenarios: Dict[str, Scenario] = {}
        self.base_predictions: Dict[str, float] = {}
        self.confidence_intervals: Dict[str, Tuple[float, float]] = {}
        self.update_callbacks: List[callable] = []
        
        # Initialize base predictions
        self._initialize_base_predictions()
        
        logger.info("DynamicPredictionEngine initialized successfully")
    
    async def update_predictions(
        self, 
        new_data: Dict[str, Any], 
        lever_changes: Dict[str, float]
    ) -> Dict[str, Any]:
        """Update predictions based on new data and lever changes"""
        try:
            logger.info(f"Updating predictions with {len(lever_changes)} lever changes")
            
            # Store old predictions
            old_predictions = self.base_predictions.copy()
            
            # Calculate new predictions based on lever changes
            new_predictions = await self._calculate_new_predictions(new_data, lever_changes)
            
            # Update base predictions
            self.base_predictions.update(new_predictions)
            
            # Calculate confidence intervals
            confidence_intervals = await self.calculate_confidence_intervals(new_predictions)
            
            # Create prediction update record
            prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for metric, new_value in new_predictions.items():
                old_value = old_predictions.get(metric, 0.0)
                
                update = PredictionUpdate(
                    prediction_id=prediction_id,
                    old_prediction=old_value,
                    new_prediction=new_value,
                    confidence_interval=confidence_intervals.get(metric, (0.0, 1.0)),
                    timestamp=datetime.now(),
                    update_reason=f"Lever changes: {list(lever_changes.keys())}",
                    lever_changes=lever_changes
                )
                
                self.prediction_history.append(update)
            
            # Update confidence intervals
            self.confidence_intervals.update(confidence_intervals)
            
            # Trigger update callbacks
            await self._trigger_update_callbacks(new_predictions, lever_changes)
            
            return {
                'prediction_id': prediction_id,
                'new_predictions': new_predictions,
                'confidence_intervals': confidence_intervals,
                'changes': {
                    metric: {
                        'old': old_predictions.get(metric, 0.0),
                        'new': new_value,
                        'change': new_value - old_predictions.get(metric, 0.0)
                    }
                    for metric, new_value in new_predictions.items()
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error updating predictions: {e}")
            raise
    
    async def calculate_confidence_intervals(self, predictions: Dict[str, float]) -> Dict[str, Tuple[float, float]]:
        """Calculate confidence intervals for predictions"""
        try:
            confidence_intervals = {}
            
            for metric, prediction in predictions.items():
                # Calculate confidence interval based on metric type and historical variance
                confidence_level = 0.95  # 95% confidence interval
                
                # Estimate standard deviation based on metric characteristics
                if 'military' in metric.lower():
                    std_dev = 0.15  # Higher uncertainty for military metrics
                elif 'economic' in metric.lower():
                    std_dev = 0.12  # Medium uncertainty for economic metrics
                elif 'political' in metric.lower():
                    std_dev = 0.18  # Higher uncertainty for political metrics
                else:
                    std_dev = 0.10  # Lower uncertainty for other metrics
                
                # Calculate confidence interval
                z_score = 1.96  # 95% confidence level
                margin_of_error = z_score * std_dev
                
                lower_bound = max(0.0, prediction - margin_of_error)
                upper_bound = min(1.0, prediction + margin_of_error)
                
                confidence_intervals[metric] = (lower_bound, upper_bound)
            
            return confidence_intervals
            
        except Exception as e:
            logger.error(f"Error calculating confidence intervals: {e}")
            return {}
    
    async def generate_alternative_scenarios(self, base_scenario: Dict[str, Any]) -> Dict[str, Scenario]:
        """Generate alternative scenarios based on different lever settings"""
        try:
            logger.info("Generating alternative scenarios")
            
            scenarios = {}
            
            # Scenario 1: Aggressive military buildup
            aggressive_scenario = Scenario(
                scenario_id="aggressive_buildup",
                name="Aggressive Military Buildup",
                description="Maximum military spending and mobilization",
                lever_settings={
                    'military_spending': 8.0,
                    'troop_mobilization': 80.0,
                    'weapons_modernization': 90.0,
                    'cyber_capabilities': 95.0,
                    'intelligence_network': 90.0
                },
                predictions={},
                confidence_level=0.85,
                probability=0.15,
                timestamp=datetime.now()
            )
            
            # Calculate predictions for aggressive scenario
            aggressive_predictions = await self._calculate_scenario_predictions(aggressive_scenario.lever_settings)
            aggressive_scenario.predictions = aggressive_predictions
            scenarios['aggressive_buildup'] = aggressive_scenario
            
            # Scenario 2: Economic focus
            economic_scenario = Scenario(
                scenario_id="economic_focus",
                name="Economic Focus Strategy",
                description="Focus on economic resilience and diplomatic solutions",
                lever_settings={
                    'military_spending': 2.0,
                    'alliance_strength': 90.0,
                    'economic_sanctions': 70.0,
                    'political_unity': 95.0,
                    'public_support': 80.0
                },
                predictions={},
                confidence_level=0.80,
                probability=0.25,
                timestamp=datetime.now()
            )
            
            # Calculate predictions for economic scenario
            economic_predictions = await self._calculate_scenario_predictions(economic_scenario.lever_settings)
            economic_scenario.predictions = economic_predictions
            scenarios['economic_focus'] = economic_scenario
            
            # Scenario 3: Balanced approach
            balanced_scenario = Scenario(
                scenario_id="balanced_approach",
                name="Balanced Approach",
                description="Balanced military and economic capabilities",
                lever_settings={
                    'military_spending': 4.0,
                    'troop_mobilization': 30.0,
                    'weapons_modernization': 70.0,
                    'alliance_strength': 75.0,
                    'cyber_capabilities': 80.0,
                    'intelligence_network': 85.0,
                    'political_unity': 80.0,
                    'public_support': 60.0
                },
                predictions={},
                confidence_level=0.90,
                probability=0.60,
                timestamp=datetime.now()
            )
            
            # Calculate predictions for balanced scenario
            balanced_predictions = await self._calculate_scenario_predictions(balanced_scenario.lever_settings)
            balanced_scenario.predictions = balanced_predictions
            scenarios['balanced_approach'] = balanced_scenario
            
            # Store scenarios
            self.scenarios.update(scenarios)
            
            return scenarios
            
        except Exception as e:
            logger.error(f"Error generating alternative scenarios: {e}")
            raise
    
    async def get_prediction_history(self, metric: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get prediction history for analysis"""
        try:
            history = []
            
            for update in self.prediction_history[-limit:]:
                if metric is None or metric in update.lever_changes:
                    history.append({
                        'prediction_id': update.prediction_id,
                        'old_prediction': update.old_prediction,
                        'new_prediction': update.new_prediction,
                        'confidence_interval': update.confidence_interval,
                        'timestamp': update.timestamp.isoformat(),
                        'update_reason': update.update_reason,
                        'lever_changes': update.lever_changes
                    })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting prediction history: {e}")
            return []
    
    async def add_update_callback(self, callback: callable) -> None:
        """Add a callback function to be called when predictions are updated"""
        try:
            self.update_callbacks.append(callback)
            logger.info(f"Added update callback: {callback.__name__}")
            
        except Exception as e:
            logger.error(f"Error adding update callback: {e}")
    
    async def get_current_predictions(self) -> Dict[str, Any]:
        """Get current predictions with confidence intervals"""
        try:
            return {
                'predictions': self.base_predictions,
                'confidence_intervals': self.confidence_intervals,
                'timestamp': datetime.now().isoformat(),
                'total_updates': len(self.prediction_history)
            }
            
        except Exception as e:
            logger.error(f"Error getting current predictions: {e}")
            raise
    
    def _initialize_base_predictions(self) -> None:
        """Initialize base predictions with default values"""
        try:
            self.base_predictions = {
                'military_effectiveness': 0.65,
                'economic_resilience': 0.70,
                'technological_advantage': 0.75,
                'logistical_capacity': 0.65,
                'political_stability': 0.80,
                'alliance_cohesion': 0.70,
                'cyber_defense': 0.75,
                'intelligence_effectiveness': 0.80,
                'public_morale': 0.60,
                'overall_capability': 0.70
            }
            
            # Initialize confidence intervals
            for metric in self.base_predictions.keys():
                self.confidence_intervals[metric] = (0.0, 1.0)
                
        except Exception as e:
            logger.error(f"Error initializing base predictions: {e}")
    
    async def _calculate_new_predictions(
        self, 
        new_data: Dict[str, Any], 
        lever_changes: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate new predictions based on lever changes"""
        try:
            new_predictions = {}
            
            # Calculate military effectiveness
            military_effectiveness = await self._calculate_military_effectiveness(lever_changes)
            new_predictions['military_effectiveness'] = military_effectiveness
            
            # Calculate economic resilience
            economic_resilience = await self._calculate_economic_resilience(lever_changes)
            new_predictions['economic_resilience'] = economic_resilience
            
            # Calculate technological advantage
            technological_advantage = await self._calculate_technological_advantage(lever_changes)
            new_predictions['technological_advantage'] = technological_advantage
            
            # Calculate logistical capacity
            logistical_capacity = await self._calculate_logistical_capacity(lever_changes)
            new_predictions['logistical_capacity'] = logistical_capacity
            
            # Calculate political stability
            political_stability = await self._calculate_political_stability(lever_changes)
            new_predictions['political_stability'] = political_stability
            
            # Calculate alliance cohesion
            alliance_cohesion = await self._calculate_alliance_cohesion(lever_changes)
            new_predictions['alliance_cohesion'] = alliance_cohesion
            
            # Calculate cyber defense
            cyber_defense = await self._calculate_cyber_defense(lever_changes)
            new_predictions['cyber_defense'] = cyber_defense
            
            # Calculate intelligence effectiveness
            intelligence_effectiveness = await self._calculate_intelligence_effectiveness(lever_changes)
            new_predictions['intelligence_effectiveness'] = intelligence_effectiveness
            
            # Calculate public morale
            public_morale = await self._calculate_public_morale(lever_changes)
            new_predictions['public_morale'] = public_morale
            
            # Calculate overall capability
            overall_capability = sum(new_predictions.values()) / len(new_predictions)
            new_predictions['overall_capability'] = overall_capability
            
            return new_predictions
            
        except Exception as e:
            logger.error(f"Error calculating new predictions: {e}")
            raise
    
    async def _calculate_military_effectiveness(self, lever_changes: Dict[str, float]) -> float:
        """Calculate military effectiveness based on lever changes"""
        try:
            base_effectiveness = self.base_predictions.get('military_effectiveness', 0.65)
            
            # Apply lever impacts
            military_spending_impact = (lever_changes.get('military_spending', 3.5) - 3.5) / 100.0 * 0.3
            troop_mobilization_impact = (lever_changes.get('troop_mobilization', 10.0) - 10.0) / 100.0 * 0.25
            weapons_modernization_impact = (lever_changes.get('weapons_modernization', 60.0) - 60.0) / 100.0 * 0.2
            
            effectiveness = base_effectiveness + military_spending_impact + troop_mobilization_impact + weapons_modernization_impact
            
            return max(0.0, min(1.0, effectiveness))
            
        except Exception as e:
            logger.error(f"Error calculating military effectiveness: {e}")
            return 0.65
    
    async def _calculate_economic_resilience(self, lever_changes: Dict[str, float]) -> float:
        """Calculate economic resilience based on lever changes"""
        try:
            base_resilience = self.base_predictions.get('economic_resilience', 0.70)
            
            # Apply lever impacts
            economic_sanctions_impact = -(lever_changes.get('economic_sanctions', 0.0) / 100.0) * 0.2
            logistical_infrastructure_impact = (lever_changes.get('logistical_infrastructure', 65.0) - 65.0) / 100.0 * 0.15
            
            resilience = base_resilience + economic_sanctions_impact + logistical_infrastructure_impact
            
            return max(0.0, min(1.0, resilience))
            
        except Exception as e:
            logger.error(f"Error calculating economic resilience: {e}")
            return 0.70
    
    async def _calculate_technological_advantage(self, lever_changes: Dict[str, float]) -> float:
        """Calculate technological advantage based on lever changes"""
        try:
            base_advantage = self.base_predictions.get('technological_advantage', 0.75)
            
            # Apply lever impacts
            cyber_capabilities_impact = (lever_changes.get('cyber_capabilities', 75.0) - 75.0) / 100.0 * 0.4
            weapons_modernization_impact = (lever_changes.get('weapons_modernization', 60.0) - 60.0) / 100.0 * 0.3
            
            advantage = base_advantage + cyber_capabilities_impact + weapons_modernization_impact
            
            return max(0.0, min(1.0, advantage))
            
        except Exception as e:
            logger.error(f"Error calculating technological advantage: {e}")
            return 0.75
    
    async def _calculate_logistical_capacity(self, lever_changes: Dict[str, float]) -> float:
        """Calculate logistical capacity based on lever changes"""
        try:
            base_capacity = self.base_predictions.get('logistical_capacity', 0.65)
            
            # Apply lever impacts
            logistical_infrastructure_impact = (lever_changes.get('logistical_infrastructure', 65.0) - 65.0) / 100.0 * 0.5
            military_spending_impact = (lever_changes.get('military_spending', 3.5) - 3.5) / 100.0 * 0.2
            
            capacity = base_capacity + logistical_infrastructure_impact + military_spending_impact
            
            return max(0.0, min(1.0, capacity))
            
        except Exception as e:
            logger.error(f"Error calculating logistical capacity: {e}")
            return 0.65
    
    async def _calculate_political_stability(self, lever_changes: Dict[str, float]) -> float:
        """Calculate political stability based on lever changes"""
        try:
            base_stability = self.base_predictions.get('political_stability', 0.80)
            
            # Apply lever impacts
            political_unity_impact = (lever_changes.get('political_unity', 85.0) - 85.0) / 100.0 * 0.4
            public_support_impact = (lever_changes.get('public_support', 45.0) - 45.0) / 100.0 * 0.3
            
            stability = base_stability + political_unity_impact + public_support_impact
            
            return max(0.0, min(1.0, stability))
            
        except Exception as e:
            logger.error(f"Error calculating political stability: {e}")
            return 0.80
    
    async def _calculate_alliance_cohesion(self, lever_changes: Dict[str, float]) -> float:
        """Calculate alliance cohesion based on lever changes"""
        try:
            base_cohesion = self.base_predictions.get('alliance_cohesion', 0.70)
            
            # Apply lever impacts
            alliance_strength_impact = (lever_changes.get('alliance_strength', 70.0) - 70.0) / 100.0 * 0.6
            
            cohesion = base_cohesion + alliance_strength_impact
            
            return max(0.0, min(1.0, cohesion))
            
        except Exception as e:
            logger.error(f"Error calculating alliance cohesion: {e}")
            return 0.70
    
    async def _calculate_cyber_defense(self, lever_changes: Dict[str, float]) -> float:
        """Calculate cyber defense based on lever changes"""
        try:
            base_defense = self.base_predictions.get('cyber_defense', 0.75)
            
            # Apply lever impacts
            cyber_capabilities_impact = (lever_changes.get('cyber_capabilities', 75.0) - 75.0) / 100.0 * 0.7
            
            defense = base_defense + cyber_capabilities_impact
            
            return max(0.0, min(1.0, defense))
            
        except Exception as e:
            logger.error(f"Error calculating cyber defense: {e}")
            return 0.75
    
    async def _calculate_intelligence_effectiveness(self, lever_changes: Dict[str, float]) -> float:
        """Calculate intelligence effectiveness based on lever changes"""
        try:
            base_effectiveness = self.base_predictions.get('intelligence_effectiveness', 0.80)
            
            # Apply lever impacts
            intelligence_network_impact = (lever_changes.get('intelligence_network', 80.0) - 80.0) / 100.0 * 0.6
            
            effectiveness = base_effectiveness + intelligence_network_impact
            
            return max(0.0, min(1.0, effectiveness))
            
        except Exception as e:
            logger.error(f"Error calculating intelligence effectiveness: {e}")
            return 0.80
    
    async def _calculate_public_morale(self, lever_changes: Dict[str, float]) -> float:
        """Calculate public morale based on lever changes"""
        try:
            base_morale = self.base_predictions.get('public_morale', 0.60)
            
            # Apply lever impacts
            public_support_impact = (lever_changes.get('public_support', 45.0) - 45.0) / 100.0 * 0.5
            political_unity_impact = (lever_changes.get('political_unity', 85.0) - 85.0) / 100.0 * 0.3
            
            morale = base_morale + public_support_impact + political_unity_impact
            
            return max(0.0, min(1.0, morale))
            
        except Exception as e:
            logger.error(f"Error calculating public morale: {e}")
            return 0.60
    
    async def _calculate_scenario_predictions(self, lever_settings: Dict[str, float]) -> Dict[str, float]:
        """Calculate predictions for a specific scenario"""
        try:
            return await self._calculate_new_predictions({}, lever_settings)
            
        except Exception as e:
            logger.error(f"Error calculating scenario predictions: {e}")
            return {}
    
    async def _trigger_update_callbacks(self, new_predictions: Dict[str, float], lever_changes: Dict[str, float]) -> None:
        """Trigger update callbacks"""
        try:
            for callback in self.update_callbacks:
                try:
                    await callback(new_predictions, lever_changes)
                except Exception as e:
                    logger.error(f"Error in update callback {callback.__name__}: {e}")
                    
        except Exception as e:
            logger.error(f"Error triggering update callbacks: {e}")
