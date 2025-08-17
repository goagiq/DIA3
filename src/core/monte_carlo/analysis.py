"""
Result Analysis
Statistical analysis and risk metrics for Monte Carlo simulation results with Phase 5 advanced analytics
"""

import numpy as np
from typing import Dict, List, Any, Optional
import logging
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class ResultAnalyzer:
    """Analyze Monte Carlo simulation results with Phase 5 advanced analytics"""
    
    def __init__(self):
        self.supported_risk_metrics = [
            "var_95", "cvar_95", "var_99", "cvar_99",
            "probability_of_failure", "risk_exposure", "impact_assessment"
        ]
        
        # Phase 5: Advanced Analytics
        self.failure_thresholds = {
            "critical": 0.99,
            "high": 0.95,
            "medium": 0.90,
            "low": 0.80
        }
    
    def calculate_statistics(self, samples: np.ndarray) -> Dict[str, Any]:
        """Calculate basic statistics for each variable"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        statistics = {}
        
        for i in range(num_variables):
            var_samples = samples[:, i]
            
            statistics[f"variable_{i}"] = {
                "mean": float(np.mean(var_samples)),
                "median": float(np.median(var_samples)),
                "std": float(np.std(var_samples)),
                "min": float(np.min(var_samples)),
                "max": float(np.max(var_samples)),
                "skewness": float(self._calculate_skewness(var_samples)),
                "kurtosis": float(self._calculate_kurtosis(var_samples)),
                "percentiles": {
                    "5": float(np.percentile(var_samples, 5)),
                    "25": float(np.percentile(var_samples, 25)),
                    "50": float(np.percentile(var_samples, 50)),
                    "75": float(np.percentile(var_samples, 75)),
                    "95": float(np.percentile(var_samples, 95))
                }
            }
        
        return statistics
    
    def calculate_risk_metrics(self, 
                             samples: np.ndarray,
                             confidence_level: float = 0.95) -> Dict[str, Any]:
        """Calculate risk metrics for the simulation results"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        risk_metrics = {}
        
        for i in range(num_variables):
            var_samples = samples[:, i]
            
            risk_metrics[f"variable_{i}"] = {
                "var_95": float(self._calculate_var(var_samples, 0.95)),
                "cvar_95": float(self._calculate_cvar(var_samples, 0.95)),
                "var_99": float(self._calculate_var(var_samples, 0.99)),
                "cvar_99": float(self._calculate_cvar(var_samples, 0.99)),
                "probability_of_failure": float(self._calculate_probability_of_failure(var_samples)),
                "risk_exposure": float(self._calculate_risk_exposure(var_samples)),
                "impact_assessment": float(self._calculate_impact_assessment(var_samples))
            }
        
        return risk_metrics
    
    # Phase 5: Advanced Analytics - Failure Mode Analysis
    def calculate_failure_modes(self, samples: np.ndarray) -> Dict[str, Any]:
        """Calculate failure mode analysis for the simulation results"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        failure_analysis = {}
        
        for i in range(num_variables):
            var_samples = samples[:, i]
            
            # Calculate failure probabilities at different thresholds
            failure_modes = {}
            for threshold_name, threshold_value in self.failure_thresholds.items():
                failure_prob = np.mean(var_samples > threshold_value)
                failure_modes[threshold_name] = {
                    "threshold": threshold_value,
                    "failure_probability": float(failure_prob),
                    "failure_count": int(np.sum(var_samples > threshold_value)),
                    "severity": self._calculate_failure_severity(failure_prob)
                }
            
            # Identify critical failure scenarios
            critical_failures = self._identify_critical_failures(var_samples)
            
            failure_analysis[f"variable_{i}"] = {
                "failure_modes": failure_modes,
                "critical_failures": critical_failures,
                "failure_trends": self._analyze_failure_trends(var_samples)
            }
        
        return failure_analysis
    
    # Phase 5: Advanced Analytics - Risk Prioritization
    def prioritize_risks(self, samples: np.ndarray) -> Dict[str, Any]:
        """Prioritize risks based on multiple criteria"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        risk_prioritization = {}
        
        # Calculate risk scores for each variable
        risk_scores = []
        for i in range(num_variables):
            var_samples = samples[:, i]
            
            # Calculate multiple risk factors
            volatility = np.std(var_samples)
            tail_risk = self._calculate_tail_risk(var_samples)
            failure_prob = self._calculate_probability_of_failure(var_samples)
            impact = self._calculate_impact_assessment(var_samples)
            
            # Combined risk score (weighted average)
            risk_score = (
                0.3 * volatility + 
                0.3 * tail_risk + 
                0.2 * failure_prob + 
                0.2 * impact
            )
            
            risk_scores.append({
                "variable_index": i,
                "risk_score": float(risk_score),
                "volatility": float(volatility),
                "tail_risk": float(tail_risk),
                "failure_probability": float(failure_prob),
                "impact": float(impact)
            })
        
        # Sort by risk score (highest first)
        risk_scores.sort(key=lambda x: x["risk_score"], reverse=True)
        
        # Assign priority levels
        for i, risk in enumerate(risk_scores):
            if i < len(risk_scores) * 0.2:
                risk["priority"] = "critical"
            elif i < len(risk_scores) * 0.4:
                risk["priority"] = "high"
            elif i < len(risk_scores) * 0.6:
                risk["priority"] = "medium"
            else:
                risk["priority"] = "low"
        
        risk_prioritization = {
            "risk_scores": risk_scores,
            "critical_risks": [r for r in risk_scores if r["priority"] == "critical"],
            "high_risks": [r for r in risk_scores if r["priority"] == "high"],
            "medium_risks": [r for r in risk_scores if r["priority"] == "medium"],
            "low_risks": [r for r in risk_scores if r["priority"] == "low"]
        }
        
        return risk_prioritization
    
    # Phase 5: Advanced Analytics - Stress Testing
    def perform_stress_tests(self, samples: np.ndarray, 
                           scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform stress testing on simulation results"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        stress_tests = {}
        
        # Scenario 1: Extreme market conditions
        stress_tests["extreme_market"] = self._stress_test_extreme_market(samples)
        
        # Scenario 2: Correlation breakdown
        stress_tests["correlation_breakdown"] = self._stress_test_correlation_breakdown(samples)
        
        # Scenario 3: Volatility spike
        stress_tests["volatility_spike"] = self._stress_test_volatility_spike(samples)
        
        # Scenario 4: Tail risk events
        stress_tests["tail_risk_events"] = self._stress_test_tail_risk(samples)
        
        # Scenario 5: Systemic risk
        stress_tests["systemic_risk"] = self._stress_test_systemic_risk(samples)
        
        # Aggregate stress test results
        stress_tests["aggregate"] = self._aggregate_stress_test_results(stress_tests)
        
        return stress_tests
    
    def calculate_sensitivity_analysis(self, 
                                     samples: np.ndarray,
                                     variable_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Calculate sensitivity analysis for variables"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        
        if variable_names is None:
            variable_names = [f"variable_{i}" for i in range(num_variables)]
        
        # Calculate correlation matrix
        correlation_matrix = np.corrcoef(samples.T)
        
        # Calculate variance decomposition
        variance_decomposition = self._calculate_variance_decomposition(samples)
        
        sensitivity_analysis = {
            "correlation_matrix": correlation_matrix.tolist(),
            "variance_decomposition": variance_decomposition,
            "variable_names": variable_names
        }
        
        return sensitivity_analysis
    
    def calculate_failure_mode_analysis(self, 
                                      samples: np.ndarray,
                                      thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Calculate failure mode analysis"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        
        if thresholds is None:
            # Use default thresholds based on percentiles
            thresholds = {}
            for i in range(num_variables):
                thresholds[f"variable_{i}"] = np.percentile(samples[:, i], 95)
        
        failure_modes = {}
        
        for i in range(num_variables):
            var_samples = samples[:, i]
            threshold = thresholds.get(f"variable_{i}", np.percentile(var_samples, 95))
            
            failure_probability = np.mean(var_samples > threshold)
            failure_impact = np.mean(var_samples[var_samples > threshold]) if failure_probability > 0 else 0
            
            failure_modes[f"variable_{i}"] = {
                "threshold": float(threshold),
                "failure_probability": float(failure_probability),
                "failure_impact": float(failure_impact),
                "risk_priority": float(failure_probability * failure_impact)
            }
        
        return failure_modes
    
    def calculate_risk_prioritization(self, 
                                    samples: np.ndarray,
                                    weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate risk prioritization based on multiple criteria"""
        
        if samples.ndim == 1:
            samples = samples.reshape(-1, 1)
        
        num_variables = samples.shape[1]
        
        if weights is None:
            weights = [1.0 / num_variables] * num_variables
        
        # Calculate risk scores for each variable
        risk_scores = []
        
        for i in range(num_variables):
            var_samples = samples[:, i]
            
            # Normalize different risk metrics
            var_95_norm = self._normalize_metric(var_samples, self._calculate_var(var_samples, 0.95))
            failure_prob_norm = self._normalize_metric(var_samples, self._calculate_probability_of_failure(var_samples))
            impact_norm = self._normalize_metric(var_samples, self._calculate_impact_assessment(var_samples))
            
            # Calculate weighted risk score
            risk_score = (var_95_norm + failure_prob_norm + impact_norm) / 3
            risk_scores.append(risk_score)
        
        # Sort variables by risk score
        sorted_indices = np.argsort(risk_scores)[::-1]  # Descending order
        
        risk_prioritization = {
            "risk_scores": [float(score) for score in risk_scores],
            "prioritized_variables": [f"variable_{i}" for i in sorted_indices],
            "weights": weights
        }
        
        return risk_prioritization
    
    # Helper methods for Phase 5 advanced analytics
    def _calculate_skewness(self, samples: np.ndarray) -> float:
        """Calculate skewness of samples"""
        mean = np.mean(samples)
        std = np.std(samples)
        if std == 0:
            return 0.0
        return np.mean(((samples - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, samples: np.ndarray) -> float:
        """Calculate kurtosis of samples"""
        mean = np.mean(samples)
        std = np.std(samples)
        if std == 0:
            return 0.0
        return np.mean(((samples - mean) / std) ** 4) - 3
    
    def _calculate_var(self, samples: np.ndarray, confidence_level: float) -> float:
        """Calculate Value at Risk"""
        return np.percentile(samples, (1 - confidence_level) * 100)
    
    def _calculate_cvar(self, samples: np.ndarray, confidence_level: float) -> float:
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        var = self._calculate_var(samples, confidence_level)
        tail_samples = samples[samples >= var]
        if len(tail_samples) == 0:
            return var
        return np.mean(tail_samples)
    
    def _calculate_probability_of_failure(self, samples: np.ndarray) -> float:
        """Calculate probability of failure (exceeding threshold)"""
        threshold = np.percentile(samples, 95)  # 95th percentile as threshold
        return np.mean(samples > threshold)
    
    def _calculate_risk_exposure(self, samples: np.ndarray) -> float:
        """Calculate risk exposure (expected loss)"""
        threshold = np.percentile(samples, 95)
        tail_samples = samples[samples > threshold]
        if len(tail_samples) == 0:
            return 0.0
        return np.mean(tail_samples - threshold)
    
    def _calculate_impact_assessment(self, samples: np.ndarray) -> float:
        """Calculate impact assessment (worst case scenario)"""
        return np.max(samples)
    
    def _calculate_variance_decomposition(self, samples: np.ndarray) -> List[float]:
        """Calculate variance decomposition for sensitivity analysis"""
        # Simple variance decomposition based on individual variances
        variances = np.var(samples, axis=0)
        total_variance = np.sum(variances)
        
        if total_variance == 0:
            return [0.0] * len(variances)
        
        return (variances / total_variance).tolist()
    
    def _normalize_metric(self, samples: np.ndarray, metric_value: float) -> float:
        """Normalize a metric value to [0, 1] range"""
        min_val = np.min(samples)
        max_val = np.max(samples)
        
        if max_val == min_val:
            return 0.5
        
        return (metric_value - min_val) / (max_val - min_val)
    
    def _calculate_failure_severity(self, failure_probability: float) -> str:
        """Calculate failure severity based on probability"""
        if failure_probability > 0.1:
            return "critical"
        elif failure_probability > 0.05:
            return "high"
        elif failure_probability > 0.01:
            return "medium"
        else:
            return "low"
    
    def _identify_critical_failures(self, samples: np.ndarray) -> Dict[str, Any]:
        """Identify critical failure scenarios"""
        critical_threshold = np.percentile(samples, 99)
        critical_failures = samples > critical_threshold
        
        return {
            "critical_threshold": float(critical_threshold),
            "critical_failure_count": int(np.sum(critical_failures)),
            "critical_failure_rate": float(np.mean(critical_failures)),
            "worst_case_scenario": float(np.max(samples))
        }
    
    def _analyze_failure_trends(self, samples: np.ndarray) -> Dict[str, Any]:
        """Analyze failure trends over time"""
        # For time series data, analyze trends
        if len(samples) > 100:
            # Split into chunks and analyze trends
            chunk_size = len(samples) // 10
            failure_rates = []
            
            for i in range(0, len(samples), chunk_size):
                chunk = samples[i:i+chunk_size]
                failure_rate = np.mean(chunk > np.percentile(samples, 95))
                failure_rates.append(failure_rate)
            
            trend = np.polyfit(range(len(failure_rates)), failure_rates, 1)[0]
            
            return {
                "failure_trend": float(trend),
                "trend_direction": "increasing" if trend > 0 else "decreasing",
                "failure_rate_volatility": float(np.std(failure_rates))
            }
        else:
            return {
                "failure_trend": 0.0,
                "trend_direction": "stable",
                "failure_rate_volatility": 0.0
            }
    
    def _calculate_tail_risk(self, samples: np.ndarray) -> float:
        """Calculate tail risk measure"""
        return float(np.percentile(samples, 99) - np.percentile(samples, 95))
    
    def _stress_test_extreme_market(self, samples: np.ndarray) -> Dict[str, Any]:
        """Stress test for extreme market conditions"""
        # Simulate extreme market conditions by applying stress factors
        stress_factor = 2.0
        stressed_samples = samples * stress_factor
        
        return {
            "stress_factor": stress_factor,
            "original_var_95": float(np.percentile(samples, 95)),
            "stressed_var_95": float(np.percentile(stressed_samples, 95)),
            "var_increase": float(np.percentile(stressed_samples, 95) - np.percentile(samples, 95)),
            "failure_probability_increase": float(
                np.mean(stressed_samples > np.percentile(samples, 99)) - 
                np.mean(samples > np.percentile(samples, 99))
            )
        }
    
    def _stress_test_correlation_breakdown(self, samples: np.ndarray) -> Dict[str, Any]:
        """Stress test for correlation breakdown"""
        # Simulate correlation breakdown by randomizing correlations
        if samples.shape[1] > 1:
            # Calculate original correlations
            original_corr = np.corrcoef(samples.T)
            
            # Simulate correlation breakdown
            np.random.shuffle(samples)
            breakdown_corr = np.corrcoef(samples.T)
            
            return {
                "original_correlation": float(np.mean(original_corr[original_corr != 1])),
                "breakdown_correlation": float(np.mean(breakdown_corr[breakdown_corr != 1])),
                "correlation_change": float(
                    np.mean(breakdown_corr[breakdown_corr != 1]) - 
                    np.mean(original_corr[original_corr != 1])
                )
            }
        else:
            return {
                "original_correlation": 1.0,
                "breakdown_correlation": 1.0,
                "correlation_change": 0.0
            }
    
    def _stress_test_volatility_spike(self, samples: np.ndarray) -> Dict[str, Any]:
        """Stress test for volatility spike"""
        # Simulate volatility spike
        original_vol = np.std(samples)
        spike_vol = original_vol * 3.0
        
        # Apply volatility spike
        spike_samples = samples * (spike_vol / original_vol)
        
        return {
            "original_volatility": float(original_vol),
            "spike_volatility": float(spike_vol),
            "volatility_increase": float(spike_vol - original_vol),
            "var_impact": float(
                np.percentile(spike_samples, 95) - np.percentile(samples, 95)
            )
        }
    
    def _stress_test_tail_risk(self, samples: np.ndarray) -> Dict[str, Any]:
        """Stress test for tail risk events"""
        # Simulate tail risk events by increasing tail probability
        tail_threshold = np.percentile(samples, 99)
        tail_events = samples > tail_threshold
        
        # Increase tail risk
        increased_tail_samples = samples.copy()
        increased_tail_samples[tail_events] *= 1.5
        
        return {
            "original_tail_probability": float(np.mean(tail_events)),
            "increased_tail_probability": float(np.mean(increased_tail_samples > tail_threshold)),
            "tail_impact": float(
                np.percentile(increased_tail_samples, 99) - np.percentile(samples, 99)
            )
        }
    
    def _stress_test_systemic_risk(self, samples: np.ndarray) -> Dict[str, Any]:
        """Stress test for systemic risk"""
        # Simulate systemic risk by applying simultaneous shocks
        systemic_shock = 0.5  # 50% simultaneous decline
        
        # Apply systemic shock
        systemic_samples = samples * (1 - systemic_shock)
        
        return {
            "systemic_shock": systemic_shock,
            "original_mean": float(np.mean(samples)),
            "systemic_mean": float(np.mean(systemic_samples)),
            "systemic_impact": float(np.mean(samples) - np.mean(systemic_samples)),
            "systemic_var_95": float(np.percentile(systemic_samples, 95))
        }
    
    def _aggregate_stress_test_results(self, stress_tests: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate results from all stress tests"""
        aggregate = {
            "total_stress_tests": len(stress_tests) - 1,  # Exclude aggregate
            "worst_case_scenario": None,
            "average_impact": 0.0,
            "risk_level": "low"
        }
        
        impacts = []
        for test_name, test_result in stress_tests.items():
            if test_name != "aggregate":
                if "var_impact" in test_result:
                    impacts.append(test_result["var_impact"])
                elif "impact" in test_result:
                    impacts.append(test_result["impact"])
        
        if impacts:
            aggregate["average_impact"] = float(np.mean(impacts))
            aggregate["worst_case_scenario"] = float(np.max(impacts))
            
            # Determine risk level
            if aggregate["average_impact"] > 0.5:
                aggregate["risk_level"] = "critical"
            elif aggregate["average_impact"] > 0.3:
                aggregate["risk_level"] = "high"
            elif aggregate["average_impact"] > 0.1:
                aggregate["risk_level"] = "medium"
            else:
                aggregate["risk_level"] = "low"
        
        return aggregate
    
    def generate_summary_report(self, 
                              samples: np.ndarray,
                              variable_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        
        if variable_names is None:
            variable_names = [f"variable_{i}" for i in range(samples.shape[1])]
        
        # Calculate all analyses
        statistics = self.calculate_statistics(samples)
        risk_metrics = self.calculate_risk_metrics(samples)
        sensitivity_analysis = self.calculate_sensitivity_analysis(samples, variable_names)
        failure_modes = self.calculate_failure_modes(samples) # Changed to new method
        risk_prioritization = self.prioritize_risks(samples) # Changed to new method
        stress_tests = self.perform_stress_tests(samples, {}) # Added stress testing
        
        # Create summary report
        summary_report = {
            "executive_summary": {
                "total_samples": len(samples),
                "num_variables": len(variable_names),
                "variable_names": variable_names,
                "overall_risk_level": self._calculate_overall_risk_level(risk_metrics),
                "key_findings": self._generate_key_findings(statistics, risk_metrics, failure_modes),
                "stress_test_results": stress_tests["aggregate"] # Added stress test results
            },
            "statistics": statistics,
            "risk_metrics": risk_metrics,
            "sensitivity_analysis": sensitivity_analysis,
            "failure_mode_analysis": failure_modes,
            "risk_prioritization": risk_prioritization,
            "recommendations": self._generate_recommendations(risk_metrics, failure_modes, risk_prioritization)
        }
        
        return summary_report
    
    def _calculate_overall_risk_level(self, risk_metrics: Dict[str, Any]) -> str:
        """Calculate overall risk level based on risk metrics"""
        
        # Calculate average VaR across all variables
        var_values = []
        for var_metrics in risk_metrics.values():
            if isinstance(var_metrics, dict) and "var_95" in var_metrics:
                var_values.append(var_metrics["var_95"])
        
        if not var_values:
            return "UNKNOWN"
        
        avg_var = np.mean(var_values)
        
        # Classify risk level
        if avg_var < 0.1:
            return "LOW"
        elif avg_var < 0.3:
            return "MEDIUM"
        elif avg_var < 0.5:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_key_findings(self, 
                             statistics: Dict[str, Any],
                             risk_metrics: Dict[str, Any],
                             failure_modes: Dict[str, Any]) -> List[str]:
        """Generate key findings from analysis"""
        
        findings = []
        
        # Find highest risk variables
        max_risk_var = None
        max_risk_score = 0
        
        for var_name, var_metrics in risk_metrics.items():
            if isinstance(var_metrics, dict) and "var_95" in var_metrics:
                if var_metrics["var_95"] > max_risk_score:
                    max_risk_score = var_metrics["var_95"]
                    max_risk_var = var_name
        
        if max_risk_var:
            findings.append(f"Highest risk variable: {max_risk_var} (VaR95: {max_risk_score:.3f})")
        
        # Find highest failure probability
        max_failure_var = None
        max_failure_prob = 0
        
        for var_name, var_failure in failure_modes.items():
            if isinstance(var_failure, dict) and "failure_probability" in var_failure:
                if var_failure["failure_probability"] > max_failure_prob:
                    max_failure_prob = var_failure["failure_probability"]
                    max_failure_var = var_name
        
        if max_failure_var:
            findings.append(f"Highest failure probability: {max_failure_var} ({max_failure_prob:.3f})")
        
        return findings
    
    def _generate_recommendations(self, 
                                risk_metrics: Dict[str, Any],
                                failure_modes: Dict[str, Any],
                                risk_prioritization: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        # High risk recommendations
        high_risk_vars = []
        for var_name, var_metrics in risk_metrics.items():
            if isinstance(var_metrics, dict) and "var_95" in var_metrics:
                if var_metrics["var_95"] > 0.3:
                    high_risk_vars.append(var_name)
        
        if high_risk_vars:
            recommendations.append(f"Implement risk mitigation strategies for high-risk variables: {', '.join(high_risk_vars)}")
        
        # High failure probability recommendations
        high_failure_vars = []
        for var_name, var_failure in failure_modes.items():
            if isinstance(var_failure, dict) and "failure_probability" in var_failure:
                if var_failure["failure_probability"] > 0.1:
                    high_failure_vars.append(var_name)
        
        if high_failure_vars:
            recommendations.append(f"Strengthen controls for variables with high failure probability: {', '.join(high_failure_vars)}")
        
        # General recommendations
        recommendations.append("Implement continuous monitoring and early warning systems")
        recommendations.append("Develop contingency plans for worst-case scenarios")
        recommendations.append("Regular review and update of risk assessments")
        
        return recommendations
