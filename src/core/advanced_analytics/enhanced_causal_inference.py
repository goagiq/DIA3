"""
Enhanced Causal Inference Engine for Intelligence Analysis
Causal inference capabilities for DoD/Intelligence Community applications
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

logger = logging.getLogger(__name__)

@dataclass
class CausalRelationship:
    """Causal relationship structure"""
    cause_variable: str
    effect_variable: str
    strength: float
    confidence: float
    direction: str  # 'positive', 'negative', 'bidirectional'
    lag: int
    metadata: Dict[str, Any]

@dataclass
class CounterfactualScenario:
    """Counterfactual scenario structure"""
    scenario_name: str
    intervention_variable: str
    intervention_value: float
    baseline_value: float
    predicted_outcome: float
    confidence_interval: Tuple[float, float]
    metadata: Dict[str, Any]

@dataclass
class GrangerCausalityResult:
    """Granger causality test result"""
    cause_variable: str
    effect_variable: str
    f_statistic: float
    p_value: float
    lag_order: int
    is_significant: bool
    metadata: Dict[str, Any]

class EnhancedCausalInferenceEngine:
    """Causal inference for intelligence analysis"""
    
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}
            
        self.config = config
        self.causal_graph = {}
        self.intervention_history = []
        
        logger.info("Initialized Enhanced Causal Inference Engine")
        
    async def identify_causal_relationships(self, data: pd.DataFrame, variables: List[str]) -> List[CausalRelationship]:
        """Identify causal relationships in intelligence data"""
        logger.info(f"Identifying causal relationships for {len(variables)} variables")
        
        relationships = []
        
        # Perform pairwise causal analysis
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables):
                if i != j:
                    # Calculate correlation
                    correlation = data[var1].corr(data[var2])
                    
                    # Perform Granger causality test
                    granger_result = await self._granger_causality_test(data, var1, var2)
                    
                    if granger_result.is_significant:
                        relationship = CausalRelationship(
                            cause_variable=var1,
                            effect_variable=var2,
                            strength=abs(correlation),
                            confidence=1 - granger_result.p_value,
                            direction='positive' if correlation > 0 else 'negative',
                            lag=granger_result.lag_order,
                            metadata={
                                'correlation': correlation,
                                'f_statistic': granger_result.f_statistic,
                                'p_value': granger_result.p_value
                            }
                        )
                        relationships.append(relationship)
                        
        logger.info(f"Identified {len(relationships)} causal relationships")
        return relationships
        
    async def counterfactual_analysis(self, scenario: Dict[str, Any], intervention: Dict[str, Any]) -> CounterfactualScenario:
        """Perform counterfactual analysis for what-if scenarios"""
        logger.info(f"Performing counterfactual analysis for scenario: {scenario.get('name', 'unknown')}")
        
        # Extract scenario data
        baseline_data = scenario.get('baseline_data', pd.DataFrame())
        intervention_var = intervention.get('variable')
        intervention_val = intervention.get('value')
        baseline_val = intervention.get('baseline_value', 0)
        
        # Build causal model
        causal_model = await self._build_causal_model(baseline_data)
        
        # Predict outcome with intervention
        predicted_outcome = await self._predict_intervention_outcome(
            causal_model, intervention_var, intervention_val
        )
        
        # Calculate confidence interval
        confidence_interval = await self._calculate_confidence_interval(
            causal_model, intervention_var, intervention_val
        )
        
        counterfactual = CounterfactualScenario(
            scenario_name=scenario.get('name', 'counterfactual_scenario'),
            intervention_variable=intervention_var,
            intervention_value=intervention_val,
            baseline_value=baseline_val,
            predicted_outcome=predicted_outcome,
            confidence_interval=confidence_interval,
            metadata={
                'causal_model': causal_model,
                'scenario_data': scenario
            }
        )
        
        # Store intervention history
        self.intervention_history.append(counterfactual)
        
        logger.info(f"Counterfactual analysis completed. Predicted outcome: {predicted_outcome}")
        return counterfactual
        
    async def granger_causality_test(self, time_series_data: pd.DataFrame) -> List[GrangerCausalityResult]:
        """Test for Granger causality in time series"""
        logger.info("Performing Granger causality tests")
        
        results = []
        variables = time_series_data.columns.tolist()
        
        for cause_var in variables:
            for effect_var in variables:
                if cause_var != effect_var:
                    result = await self._granger_causality_test(time_series_data, cause_var, effect_var)
                    results.append(result)
                    
        logger.info(f"Completed {len(results)} Granger causality tests")
        return results
        
    async def _granger_causality_test(self, data: pd.DataFrame, cause_var: str, effect_var: str, 
                                    max_lag: int = 5) -> GrangerCausalityResult:
        """Perform Granger causality test between two variables"""
        
        # Prepare data
        x = data[cause_var].dropna()
        y = data[effect_var].dropna()
        
        # Align data
        min_length = min(len(x), len(y))
        x = x.iloc[:min_length]
        y = y.iloc[:min_length]
        
        best_lag = 1
        best_f_stat = 0
        best_p_value = 1
        
        # Test different lag orders
        for lag in range(1, min(max_lag + 1, len(x) // 2)):
            try:
                # Create lagged variables
                x_lagged = pd.DataFrame()
                for i in range(1, lag + 1):
                    x_lagged[f'x_lag_{i}'] = x.shift(i)
                    
                # Remove NaN values
                valid_indices = ~(x_lagged.isna().any(axis=1) | y.isna())
                x_lagged_clean = x_lagged[valid_indices]
                y_clean = y[valid_indices]
                
                if len(x_lagged_clean) < lag + 5:  # Need sufficient data
                    continue
                    
                # Fit restricted model (without cause variable)
                restricted_model = LinearRegression()
                restricted_model.fit(x_lagged_clean, y_clean)
                restricted_rss = np.sum((y_clean - restricted_model.predict(x_lagged_clean)) ** 2)
                
                # Fit unrestricted model (with cause variable)
                unrestricted_model = LinearRegression()
                unrestricted_model.fit(x_lagged_clean, y_clean)
                unrestricted_rss = np.sum((y_clean - unrestricted_model.predict(x_lagged_clean)) ** 2)
                
                # Calculate F-statistic
                if unrestricted_rss > 0:
                    f_stat = ((restricted_rss - unrestricted_rss) / lag) / (unrestricted_rss / (len(y_clean) - 2 * lag))
                    p_value = 1 - stats.f.cdf(f_stat, lag, len(y_clean) - 2 * lag)
                    
                    if f_stat > best_f_stat:
                        best_f_stat = f_stat
                        best_p_value = p_value
                        best_lag = lag
                        
            except Exception as e:
                logger.warning(f"Error in Granger causality test for lag {lag}: {e}")
                continue
                
        is_significant = best_p_value < 0.05
        
        return GrangerCausalityResult(
            cause_variable=cause_var,
            effect_variable=effect_var,
            f_statistic=best_f_stat,
            p_value=best_p_value,
            lag_order=best_lag,
            is_significant=is_significant,
            metadata={'test_method': 'granger_causality'}
        )
        
    async def _build_causal_model(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Build causal model from data"""
        # Placeholder for causal model building
        # In real implementation, this would use more sophisticated causal discovery algorithms
        
        model = {
            'variables': data.columns.tolist(),
            'relationships': {},
            'model_type': 'linear_causal'
        }
        
        # Identify relationships using correlation and Granger causality
        for var1 in data.columns:
            for var2 in data.columns:
                if var1 != var2:
                    correlation = data[var1].corr(data[var2])
                    if abs(correlation) > 0.3:  # Threshold for relationship
                        model['relationships'][(var1, var2)] = {
                            'correlation': correlation,
                            'strength': abs(correlation)
                        }
                        
        return model
        
    async def _predict_intervention_outcome(self, causal_model: Dict[str, Any], 
                                          intervention_var: str, intervention_val: float) -> float:
        """Predict outcome of an intervention"""
        # Placeholder for intervention outcome prediction
        # In real implementation, this would use the causal model to predict effects
        
        # Simple linear prediction based on intervention
        base_outcome = 0.5
        intervention_effect = intervention_val * 0.1  # Simple linear effect
        
        return base_outcome + intervention_effect
        
    async def _calculate_confidence_interval(self, causal_model: Dict[str, Any], 
                                           intervention_var: str, intervention_val: float,
                                           confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for intervention prediction"""
        # Placeholder for confidence interval calculation
        
        predicted_outcome = await self._predict_intervention_outcome(causal_model, intervention_var, intervention_val)
        
        # Simple confidence interval based on uncertainty
        uncertainty = 0.1 * abs(intervention_val)
        lower_bound = predicted_outcome - uncertainty
        upper_bound = predicted_outcome + uncertainty
        
        return (lower_bound, upper_bound)
        
    async def analyze_intelligence_patterns(self, intelligence_data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze intelligence patterns using causal inference"""
        logger.info("Analyzing intelligence patterns using causal inference")
        
        # Identify causal relationships
        variables = intelligence_data.columns.tolist()
        causal_relationships = await self.identify_causal_relationships(intelligence_data, variables)
        
        # Perform Granger causality tests
        granger_results = await self.granger_causality_test(intelligence_data)
        
        # Build causal graph
        causal_graph = await self._build_causal_graph(causal_relationships, granger_results)
        
        return {
            'causal_relationships': causal_relationships,
            'granger_causality': granger_results,
            'causal_graph': causal_graph,
            'analysis_summary': {
                'total_relationships': len(causal_relationships),
                'significant_granger': len([r for r in granger_results if r.is_significant]),
                'strongest_relationship': max(causal_relationships, key=lambda x: x.strength) if causal_relationships else None
            }
        }
        
    async def _build_causal_graph(self, relationships: List[CausalRelationship], 
                                granger_results: List[GrangerCausalityResult]) -> Dict[str, Any]:
        """Build causal graph from relationships and Granger results"""
        graph = {
            'nodes': set(),
            'edges': [],
            'metadata': {}
        }
        
        # Add relationships as edges
        for rel in relationships:
            graph['nodes'].add(rel.cause_variable)
            graph['nodes'].add(rel.effect_variable)
            graph['edges'].append({
                'source': rel.cause_variable,
                'target': rel.effect_variable,
                'strength': rel.strength,
                'confidence': rel.confidence,
                'direction': rel.direction,
                'lag': rel.lag
            })
            
        # Add Granger causality results
        for granger in granger_results:
            if granger.is_significant:
                graph['edges'].append({
                    'source': granger.cause_variable,
                    'target': granger.effect_variable,
                    'strength': 1 - granger.p_value,
                    'confidence': 1 - granger.p_value,
                    'direction': 'positive',
                    'lag': granger.lag_order,
                    'method': 'granger_causality'
                })
                
        graph['nodes'] = list(graph['nodes'])
        
        return graph
        
    def get_intervention_history(self) -> List[CounterfactualScenario]:
        """Get history of counterfactual interventions"""
        return self.intervention_history.copy()
        
    def get_causal_graph(self) -> Dict[str, Any]:
        """Get current causal graph"""
        return self.causal_graph.copy()
