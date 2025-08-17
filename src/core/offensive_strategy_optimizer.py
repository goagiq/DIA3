#!/usr/bin/env python3
"""
Offensive Strategy Optimizer
A comprehensive system that combines pattern recognition and Monte Carlo simulation
to identify optimal offensive strategies for eliminating high-value targets under time constraints.
"""

import asyncio
import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import minimize
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TargetType(Enum):
    """Types of high-value targets."""
    LEADERSHIP = "leadership"
    INFRASTRUCTURE = "infrastructure"
    MILITARY_ASSET = "military_asset"
    ECONOMIC_TARGET = "economic_target"
    INTELLIGENCE_ASSET = "intelligence_asset"
    CYBER_TARGET = "cyber_target"
    LOGISTICS_HUB = "logistics_hub"
    COMMAND_CONTROL = "command_control"


class StrategyType(Enum):
    """Types of offensive strategies."""
    DIRECT_ASSAULT = "direct_assault"
    STEALTH_INFILTRATION = "stealth_infiltration"
    CYBER_ATTACK = "cyber_attack"
    ECONOMIC_SABOTAGE = "economic_sabotage"
    PSYCHOLOGICAL_OPERATIONS = "psychological_operations"
    COMBINED_OPERATIONS = "combined_operations"
    DECEPTION_OPERATIONS = "deception_operations"
    PRECISION_STRIKE = "precision_strike"


class ThreatLevel(Enum):
    """Threat levels for targets."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Target:
    """High-value target definition."""
    target_id: str
    name: str
    target_type: TargetType
    threat_level: ThreatLevel
    location: Dict[str, float]  # lat, lon
    value_score: float  # 0-100
    protection_level: float  # 0-100
    time_sensitivity: float  # 0-100
    mobility: float  # 0-100 (0 = static, 100 = highly mobile)
    intelligence_quality: float  # 0-100
    collateral_risk: float  # 0-100
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Strategy:
    """Offensive strategy definition."""
    strategy_id: str
    name: str
    strategy_type: StrategyType
    execution_time: float  # hours
    success_probability: float  # 0-1
    resource_requirements: Dict[str, float]
    risk_level: float  # 0-100
    detection_probability: float  # 0-1
    collateral_damage: float  # 0-100
    weather_dependency: float  # 0-1
    night_operation_capability: float  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationalConstraints:
    """Operational constraints for offensive operations."""
    time_limit: float  # hours
    available_resources: Dict[str, float]
    weather_conditions: Dict[str, float]
    intelligence_quality: float  # 0-100
    political_restrictions: List[str]
    legal_constraints: List[str]
    force_protection_requirements: float  # 0-100
    stealth_requirements: float  # 0-100


@dataclass
class Pattern:
    """Pattern identified in historical data."""
    pattern_id: str
    pattern_type: str
    confidence: float
    conditions: Dict[str, Any]
    outcomes: Dict[str, float]
    frequency: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OptimizationResult:
    """Result of strategy optimization."""
    optimization_id: str
    optimal_strategy: Strategy
    target_prioritization: List[Target]
    execution_sequence: List[Dict[str, Any]]
    expected_success_rate: float
    risk_assessment: Dict[str, float]
    resource_allocation: Dict[str, float]
    timeline: List[Dict[str, Any]]
    confidence_intervals: Dict[str, Dict[str, float]]
    pattern_insights: List[Pattern]
    execution_time: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class PatternRecognitionEngine:
    """Engine for identifying patterns in historical offensive operations."""
    
    def __init__(self):
        self.patterns = []
        self.historical_data = []
        self.pattern_classifiers = {}
        
    def add_historical_data(self, data: Dict[str, Any]):
        """Add historical operation data for pattern analysis."""
        self.historical_data.append(data)
        
    def identify_temporal_patterns(self, target_type: TargetType) -> List[Pattern]:
        """Identify temporal patterns in target behavior."""
        patterns = []
        
        # Filter data by target type
        relevant_data = [d for d in self.historical_data 
                        if d.get('target_type') == target_type.value]
        
        if len(relevant_data) < 10:
            return patterns
            
        # Analyze temporal patterns
        df = pd.DataFrame(relevant_data)
        
        # Time-based patterns
        if 'timestamp' in df.columns:
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
            
            # Identify peak activity hours
            hourly_pattern = df['hour'].value_counts().to_dict()
            peak_hours = [hour for hour, count in hourly_pattern.items() 
                         if count > np.mean(list(hourly_pattern.values()))]
            
            if peak_hours:
                patterns.append(Pattern(
                    pattern_id=f"temporal_{target_type.value}_{uuid.uuid4().hex[:8]}",
                    pattern_type="temporal_activity",
                    confidence=0.8,
                    conditions={"peak_hours": peak_hours, "target_type": target_type.value},
                    outcomes={"optimal_timing": peak_hours},
                    frequency=len(peak_hours) / 24
                ))
        
        return patterns
    
    def identify_behavioral_patterns(self, target_type: TargetType) -> List[Pattern]:
        """Identify behavioral patterns in target responses."""
        patterns = []
        
        relevant_data = [d for d in self.historical_data 
                        if d.get('target_type') == target_type.value]
        
        if len(relevant_data) < 5:
            return patterns
            
        df = pd.DataFrame(relevant_data)
        
        # Analyze response patterns
        if 'response_time' in df.columns and 'threat_level' in df.columns:
            # Response time vs threat level correlation
            correlation = df['response_time'].corr(df['threat_level'])
            
            if abs(correlation) > 0.3:
                patterns.append(Pattern(
                    pattern_id=f"behavioral_{target_type.value}_{uuid.uuid4().hex[:8]}",
                    pattern_type="response_correlation",
                    confidence=abs(correlation),
                    conditions={"target_type": target_type.value, "correlation_threshold": 0.3},
                    outcomes={"response_prediction": correlation},
                    frequency=abs(correlation)
                ))
        
        return patterns
    
    def identify_environmental_patterns(self) -> List[Pattern]:
        """Identify environmental patterns affecting operations."""
        patterns = []
        
        if len(self.historical_data) < 10:
            return patterns
            
        df = pd.DataFrame(self.historical_data)
        
        # Weather impact analysis
        if 'weather_conditions' in df.columns and 'success_rate' in df.columns:
            weather_success = {}
            for _, row in df.iterrows():
                weather = row['weather_conditions'].get('condition', 'unknown')
                success = row['success_rate']
                
                if weather not in weather_success:
                    weather_success[weather] = []
                weather_success[weather].append(success)
            
            # Find optimal weather conditions
            optimal_weather = {}
            for weather, success_rates in weather_success.items():
                if len(success_rates) >= 3:
                    avg_success = np.mean(success_rates)
                    optimal_weather[weather] = avg_success
            
            if optimal_weather:
                best_weather = max(optimal_weather, key=optimal_weather.get)
                patterns.append(Pattern(
                    pattern_id=f"environmental_{uuid.uuid4().hex[:8]}",
                    pattern_type="weather_optimization",
                    confidence=optimal_weather[best_weather],
                    conditions={"optimal_weather": best_weather},
                    outcomes={"weather_success_rates": optimal_weather},
                    frequency=optimal_weather[best_weather]
                ))
        
        return patterns


class MonteCarloStrategySimulator:
    """Monte Carlo simulator for offensive strategy evaluation."""
    
    def __init__(self, num_iterations: int = 10000):
        self.num_iterations = num_iterations
        self.results_cache = {}
        
    def simulate_strategy_execution(self, 
                                  strategy: Strategy, 
                                  target: Target, 
                                  constraints: OperationalConstraints,
                                  patterns: List[Pattern]) -> Dict[str, Any]:
        """Simulate strategy execution using Monte Carlo methods."""
        
        cache_key = f"{strategy.strategy_id}_{target.target_id}_{constraints.time_limit}"
        if cache_key in self.results_cache:
            return self.results_cache[cache_key]
        
        results = {
            'success_rate': [],
            'execution_time': [],
            'resource_consumption': [],
            'risk_level': [],
            'detection_probability': [],
            'collateral_damage': []
        }
        
        # Apply pattern-based adjustments
        pattern_adjustments = self._calculate_pattern_adjustments(strategy, target, patterns)
        
        for _ in range(self.num_iterations):
            # Base success probability
            base_success = strategy.success_probability
            
            # Apply environmental factors
            weather_factor = self._simulate_weather_impact(strategy, constraints)
            time_factor = self._simulate_timing_impact(target, patterns)
            intelligence_factor = self._simulate_intelligence_impact(target, constraints)
            
            # Calculate adjusted success probability
            adjusted_success = base_success * weather_factor * time_factor * intelligence_factor
            adjusted_success = np.clip(adjusted_success, 0, 1)
            
            # Simulate execution
            success = np.random.random() < adjusted_success
            
            # Simulate execution time with variability
            base_time = strategy.execution_time
            time_variability = np.random.normal(0, base_time * 0.2)
            actual_time = max(0.1, base_time + time_variability)
            
            # Simulate resource consumption
            resource_consumption = {}
            for resource, base_amount in strategy.resource_requirements.items():
                variability = np.random.normal(0, base_amount * 0.15)
                resource_consumption[resource] = max(0, base_amount + variability)
            
            # Simulate risk factors
            risk_level = strategy.risk_level * (1 + np.random.normal(0, 0.1))
            detection_prob = strategy.detection_probability * (1 + np.random.normal(0, 0.1))
            collateral_damage = strategy.collateral_damage * (1 + np.random.normal(0, 0.1))
            
            results['success_rate'].append(success)
            results['execution_time'].append(actual_time)
            results['resource_consumption'].append(resource_consumption)
            results['risk_level'].append(risk_level)
            results['detection_probability'].append(detection_prob)
            results['collateral_damage'].append(collateral_damage)
        
        # Calculate statistics
        final_results = {
            'mean_success_rate': np.mean(results['success_rate']),
            'success_rate_std': np.std(results['success_rate']),
            'mean_execution_time': np.mean(results['execution_time']),
            'execution_time_std': np.std(results['execution_time']),
            'mean_risk_level': np.mean(results['risk_level']),
            'mean_detection_probability': np.mean(results['detection_probability']),
            'mean_collateral_damage': np.mean(results['collateral_damage']),
            'resource_consumption_stats': self._calculate_resource_stats(results['resource_consumption']),
            'confidence_intervals': self._calculate_confidence_intervals(results),
            'pattern_adjustments': pattern_adjustments
        }
        
        self.results_cache[cache_key] = final_results
        return final_results
    
    def _calculate_pattern_adjustments(self, 
                                     strategy: Strategy, 
                                     target: Target, 
                                     patterns: List[Pattern]) -> Dict[str, float]:
        """Calculate adjustments based on identified patterns."""
        adjustments = {
            'success_rate_adjustment': 1.0,
            'timing_adjustment': 1.0,
            'resource_adjustment': 1.0
        }
        
        for pattern in patterns:
            if pattern.pattern_type == "temporal_activity":
                # Apply timing adjustments
                current_hour = datetime.now().hour
                if current_hour in pattern.conditions.get('peak_hours', []):
                    adjustments['timing_adjustment'] *= 1.2
                else:
                    adjustments['timing_adjustment'] *= 0.8
                    
            elif pattern.pattern_type == "weather_optimization":
                # Apply weather-based adjustments
                optimal_weather = pattern.conditions.get('optimal_weather', 'clear')
                # This would be compared with actual weather conditions
                adjustments['success_rate_adjustment'] *= pattern.confidence
        
        return adjustments
    
    def _simulate_weather_impact(self, strategy: Strategy, constraints: OperationalConstraints) -> float:
        """Simulate weather impact on strategy execution."""
        weather_factor = 1.0
        
        if strategy.weather_dependency > 0.5:
            # High weather dependency
            weather_conditions = constraints.weather_conditions
            if weather_conditions.get('visibility', 100) < 50:
                weather_factor *= 0.7
            if weather_conditions.get('wind_speed', 0) > 20:
                weather_factor *= 0.8
            if weather_conditions.get('precipitation', 0) > 0.5:
                weather_factor *= 0.6
        
        return weather_factor
    
    def _simulate_timing_impact(self, target: Target, patterns: List[Pattern]) -> float:
        """Simulate timing impact based on patterns."""
        timing_factor = 1.0
        
        for pattern in patterns:
            if pattern.pattern_type == "temporal_activity":
                current_hour = datetime.now().hour
                if current_hour in pattern.conditions.get('peak_hours', []):
                    timing_factor *= 1.3
                else:
                    timing_factor *= 0.9
        
        return timing_factor
    
    def _simulate_intelligence_impact(self, target: Target, constraints: OperationalConstraints) -> float:
        """Simulate intelligence quality impact."""
        intelligence_factor = constraints.intelligence_quality / 100.0
        
        # Intelligence quality affects success probability
        if intelligence_factor < 0.3:
            return 0.5
        elif intelligence_factor < 0.6:
            return 0.8
        else:
            return 1.0
    
    def _calculate_resource_stats(self, resource_consumption_list: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """Calculate statistics for resource consumption."""
        stats = {}
        
        # Get all resource types
        all_resources = set()
        for consumption in resource_consumption_list:
            all_resources.update(consumption.keys())
        
        for resource in all_resources:
            values = [consumption.get(resource, 0) for consumption in resource_consumption_list]
            stats[resource] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values)
            }
        
        return stats
    
    def _calculate_confidence_intervals(self, results: Dict[str, List]) -> Dict[str, Dict[str, float]]:
        """Calculate confidence intervals for key metrics."""
        confidence_intervals = {}
        
        for metric, values in results.items():
            if isinstance(values[0], (int, float)):
                mean = np.mean(values)
                std = np.std(values)
                n = len(values)
                
                # 95% confidence interval
                margin_of_error = 1.96 * (std / np.sqrt(n))
                confidence_intervals[metric] = {
                    'lower': mean - margin_of_error,
                    'upper': mean + margin_of_error,
                    'mean': mean
                }
        
        return confidence_intervals


class OffensiveStrategyOptimizer:
    """Main optimizer that combines pattern recognition and Monte Carlo simulation."""
    
    def __init__(self, cache_dir: str = "cache/offensive_strategy"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.pattern_engine = PatternRecognitionEngine()
        self.monte_carlo_simulator = MonteCarloStrategySimulator()
        
        # Load historical data
        self._load_historical_data()
        
    def _load_historical_data(self):
        """Load historical offensive operation data."""
        # This would typically load from a database or file
        # For demonstration, we'll create sample data
        sample_data = [
            {
                'timestamp': '2024-01-15T14:30:00',
                'target_type': 'leadership',
                'strategy_type': 'stealth_infiltration',
                'success_rate': 0.85,
                'response_time': 45,
                'threat_level': 85,
                'weather_conditions': {'condition': 'clear', 'visibility': 90}
            },
            {
                'timestamp': '2024-01-16T02:15:00',
                'target_type': 'infrastructure',
                'strategy_type': 'precision_strike',
                'success_rate': 0.92,
                'response_time': 30,
                'threat_level': 75,
                'weather_conditions': {'condition': 'clear', 'visibility': 95}
            },
            # Add more sample data...
        ]
        
        for data in sample_data:
            self.pattern_engine.add_historical_data(data)
    
    def optimize_strategy(self, 
                         targets: List[Target],
                         strategies: List[Strategy],
                         constraints: OperationalConstraints) -> OptimizationResult:
        """Optimize offensive strategy for given targets and constraints."""
        
        start_time = datetime.now()
        
        # Step 1: Identify patterns
        logger.info("Identifying patterns in historical data...")
        patterns = []
        for target_type in TargetType:
            temporal_patterns = self.pattern_engine.identify_temporal_patterns(target_type)
            behavioral_patterns = self.pattern_engine.identify_behavioral_patterns(target_type)
            patterns.extend(temporal_patterns + behavioral_patterns)
        
        environmental_patterns = self.pattern_engine.identify_environmental_patterns()
        patterns.extend(environmental_patterns)
        
        # Step 2: Prioritize targets
        logger.info("Prioritizing targets...")
        target_prioritization = self._prioritize_targets(targets, constraints)
        
        # Step 3: Evaluate strategies for each target
        logger.info("Evaluating strategies...")
        strategy_evaluations = {}
        for target in targets:
            strategy_evaluations[target.target_id] = {}
            for strategy in strategies:
                evaluation = self.monte_carlo_simulator.simulate_strategy_execution(
                    strategy, target, constraints, patterns
                )
                strategy_evaluations[target.target_id][strategy.strategy_id] = evaluation
        
        # Step 4: Find optimal strategy combination
        logger.info("Finding optimal strategy combination...")
        optimal_combination = self._find_optimal_combination(
            targets, strategies, strategy_evaluations, constraints
        )
        
        # Step 5: Generate execution sequence
        logger.info("Generating execution sequence...")
        execution_sequence = self._generate_execution_sequence(
            optimal_combination, constraints, patterns
        )
        
        # Step 6: Calculate overall metrics
        overall_success_rate = self._calculate_overall_success_rate(optimal_combination)
        risk_assessment = self._calculate_overall_risk(optimal_combination)
        resource_allocation = self._calculate_resource_allocation(optimal_combination)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        result = OptimizationResult(
            optimization_id=f"opt_{uuid.uuid4().hex[:8]}",
            optimal_strategy=optimal_combination['best_strategy'],
            target_prioritization=target_prioritization,
            execution_sequence=execution_sequence,
            expected_success_rate=overall_success_rate,
            risk_assessment=risk_assessment,
            resource_allocation=resource_allocation,
            timeline=self._generate_timeline(execution_sequence),
            confidence_intervals=self._calculate_overall_confidence_intervals(optimal_combination),
            pattern_insights=patterns,
            execution_time=execution_time,
            timestamp=datetime.now()
        )
        
        # Save results
        self._save_results(result)
        
        return result
    
    def _prioritize_targets(self, targets: List[Target], constraints: OperationalConstraints) -> List[Target]:
        """Prioritize targets based on value, threat, and constraints."""
        target_scores = []
        
        for target in targets:
            # Calculate priority score
            value_score = target.value_score
            threat_score = self._threat_level_to_score(target.threat_level)
            time_sensitivity = target.time_sensitivity
            protection_factor = 1 - (target.protection_level / 100)
            
            # Weighted priority score
            priority_score = (
                value_score * 0.4 +
                threat_score * 0.3 +
                time_sensitivity * 0.2 +
                protection_factor * 0.1
            )
            
            target_scores.append((target, priority_score))
        
        # Sort by priority score (descending)
        target_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [target for target, _ in target_scores]
    
    def _threat_level_to_score(self, threat_level: ThreatLevel) -> float:
        """Convert threat level to numerical score."""
        return {
            ThreatLevel.CRITICAL: 100,
            ThreatLevel.HIGH: 75,
            ThreatLevel.MEDIUM: 50,
            ThreatLevel.LOW: 25
        }[threat_level]
    
    def _find_optimal_combination(self, 
                                targets: List[Target],
                                strategies: List[Strategy],
                                evaluations: Dict[str, Dict[str, Any]],
                                constraints: OperationalConstraints) -> Dict[str, Any]:
        """Find optimal strategy combination using optimization algorithms."""
        
        best_combination = {
            'target_strategy_pairs': [],
            'best_strategy': None,
            'total_success_rate': 0,
            'total_risk': 0,
            'total_resources': {}
        }
        
        # For each target, find the best strategy
        for target in targets:
            target_evaluations = evaluations[target.target_id]
            best_strategy_id = None
            best_score = 0
            
            for strategy in strategies:
                evaluation = target_evaluations[strategy.strategy_id]
                
                # Calculate strategy score
                success_rate = evaluation['mean_success_rate']
                risk_level = evaluation['mean_risk_level']
                execution_time = evaluation['mean_execution_time']
                
                # Penalize if execution time exceeds constraints
                if execution_time > constraints.time_limit:
                    continue
                
                # Score calculation (higher is better)
                score = success_rate * 0.6 - (risk_level / 100) * 0.4
                
                if score > best_score:
                    best_score = score
                    best_strategy_id = strategy.strategy_id
            
            if best_strategy_id:
                best_strategy = next(s for s in strategies if s.strategy_id == best_strategy_id)
                best_combination['target_strategy_pairs'].append({
                    'target': target,
                    'strategy': best_strategy,
                    'evaluation': evaluations[target.target_id][best_strategy_id]
                })
        
        # Calculate overall metrics
        if best_combination['target_strategy_pairs']:
            total_success = np.mean([pair['evaluation']['mean_success_rate'] 
                                   for pair in best_combination['target_strategy_pairs']])
            total_risk = np.mean([pair['evaluation']['mean_risk_level'] 
                                for pair in best_combination['target_strategy_pairs']])
            
            best_combination['total_success_rate'] = total_success
            best_combination['total_risk'] = total_risk
            best_combination['best_strategy'] = best_combination['target_strategy_pairs'][0]['strategy']
        
        return best_combination
    
    def _generate_execution_sequence(self, 
                                   combination: Dict[str, Any],
                                   constraints: OperationalConstraints,
                                   patterns: List[Pattern]) -> List[Dict[str, Any]]:
        """Generate optimal execution sequence."""
        sequence = []
        current_time = 0
        
        # Sort by priority and timing constraints
        sorted_pairs = sorted(combination['target_strategy_pairs'], 
                            key=lambda x: x['target'].time_sensitivity, reverse=True)
        
        for pair in sorted_pairs:
            target = pair['target']
            strategy = pair['strategy']
            evaluation = pair['evaluation']
            
            # Apply timing adjustments based on patterns
            timing_adjustment = 1.0
            for pattern in patterns:
                if pattern.pattern_type == "temporal_activity":
                    timing_adjustment = pattern.conditions.get('timing_adjustment', 1.0)
            
            execution_time = evaluation['mean_execution_time'] * timing_adjustment
            
            if current_time + execution_time <= constraints.time_limit:
                sequence.append({
                    'target': target,
                    'strategy': strategy,
                    'start_time': current_time,
                    'end_time': current_time + execution_time,
                    'expected_success_rate': evaluation['mean_success_rate'],
                    'risk_level': evaluation['mean_risk_level']
                })
                current_time += execution_time
        
        return sequence
    
    def _calculate_overall_success_rate(self, combination: Dict[str, Any]) -> float:
        """Calculate overall success rate for the combination."""
        if not combination['target_strategy_pairs']:
            return 0.0
        
        success_rates = [pair['evaluation']['mean_success_rate'] 
                        for pair in combination['target_strategy_pairs']]
        return np.mean(success_rates)
    
    def _calculate_overall_risk(self, combination: Dict[str, Any]) -> Dict[str, float]:
        """Calculate overall risk assessment."""
        if not combination['target_strategy_pairs']:
            return {'total_risk': 0, 'detection_risk': 0, 'collateral_risk': 0}
        
        total_risks = [pair['evaluation']['mean_risk_level'] 
                      for pair in combination['target_strategy_pairs']]
        detection_risks = [pair['evaluation']['mean_detection_probability'] 
                          for pair in combination['target_strategy_pairs']]
        collateral_risks = [pair['evaluation']['mean_collateral_damage'] 
                           for pair in combination['target_strategy_pairs']]
        
        return {
            'total_risk': np.mean(total_risks),
            'detection_risk': np.mean(detection_risks),
            'collateral_risk': np.mean(collateral_risks)
        }
    
    def _calculate_resource_allocation(self, combination: Dict[str, Any]) -> Dict[str, float]:
        """Calculate total resource allocation."""
        if not combination['target_strategy_pairs']:
            return {}
        
        total_resources = {}
        for pair in combination['target_strategy_pairs']:
            resource_stats = pair['evaluation']['resource_consumption_stats']
            for resource, stats in resource_stats.items():
                if resource not in total_resources:
                    total_resources[resource] = 0
                total_resources[resource] += stats['mean']
        
        return total_resources
    
    def _generate_timeline(self, execution_sequence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate detailed timeline for execution."""
        timeline = []
        
        for i, step in enumerate(execution_sequence):
            timeline.append({
                'step': i + 1,
                'target_name': step['target'].name,
                'strategy_name': step['strategy'].name,
                'start_time': step['start_time'],
                'end_time': step['end_time'],
                'duration': step['end_time'] - step['start_time'],
                'expected_success_rate': step['expected_success_rate'],
                'risk_level': step['risk_level']
            })
        
        return timeline
    
    def _calculate_overall_confidence_intervals(self, combination: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Calculate overall confidence intervals."""
        if not combination['target_strategy_pairs']:
            return {}
        
        # Aggregate confidence intervals from all evaluations
        all_intervals = {}
        for pair in combination['target_strategy_pairs']:
            intervals = pair['evaluation']['confidence_intervals']
            for metric, interval in intervals.items():
                if metric not in all_intervals:
                    all_intervals[metric] = []
                all_intervals[metric].append(interval)
        
        # Calculate overall intervals
        overall_intervals = {}
        for metric, interval_list in all_intervals.items():
            means = [interval['mean'] for interval in interval_list]
            overall_intervals[metric] = {
                'mean': np.mean(means),
                'std': np.std(means),
                'min': np.min([interval['lower'] for interval in interval_list]),
                'max': np.max([interval['upper'] for interval in interval_list])
            }
        
        return overall_intervals
    
    def _save_results(self, result: OptimizationResult):
        """Save optimization results to cache."""
        result_file = self.cache_dir / f"optimization_{result.optimization_id}.json"
        
        # Convert to serializable format
        result_dict = {
            'optimization_id': result.optimization_id,
            'optimal_strategy': {
                'strategy_id': result.optimal_strategy.strategy_id,
                'name': result.optimal_strategy.name,
                'strategy_type': result.optimal_strategy.strategy_type.value
            },
            'target_prioritization': [
                {
                    'target_id': target.target_id,
                    'name': target.name,
                    'target_type': target.target_type.value,
                    'threat_level': target.threat_level.value
                }
                for target in result.target_prioritization
            ],
            'expected_success_rate': result.expected_success_rate,
            'risk_assessment': result.risk_assessment,
            'resource_allocation': result.resource_allocation,
            'execution_time': result.execution_time,
            'timestamp': result.timestamp.isoformat()
        }
        
        with open(result_file, 'w') as f:
            json.dump(result_dict, f, indent=2)
    
    def generate_visualization(self, result: OptimizationResult, output_path: str = None):
        """Generate visualization of optimization results."""
        if output_path is None:
            output_path = self.cache_dir / f"visualization_{result.optimization_id}.png"
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Success Rate vs Risk
        success_rates = [step['expected_success_rate'] for step in result.timeline]
        risk_levels = [step['risk_level'] for step in result.timeline]
        target_names = [step['target_name'] for step in result.timeline]
        
        axes[0, 0].scatter(risk_levels, success_rates, s=100, alpha=0.7)
        for i, name in enumerate(target_names):
            axes[0, 0].annotate(name, (risk_levels[i], success_rates[i]), 
                              xytext=(5, 5), textcoords='offset points')
        axes[0, 0].set_xlabel('Risk Level')
        axes[0, 0].set_ylabel('Expected Success Rate')
        axes[0, 0].set_title('Success Rate vs Risk Level')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Timeline
        steps = [step['step'] for step in result.timeline]
        durations = [step['duration'] for step in result.timeline]
        
        axes[0, 1].bar(steps, durations, alpha=0.7)
        axes[0, 1].set_xlabel('Execution Step')
        axes[0, 1].set_ylabel('Duration (hours)')
        axes[0, 1].set_title('Execution Timeline')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Resource Allocation
        resources = list(result.resource_allocation.keys())
        amounts = list(result.resource_allocation.values())
        
        axes[1, 0].pie(amounts, labels=resources, autopct='%1.1f%%')
        axes[1, 0].set_title('Resource Allocation')
        
        # 4. Risk Assessment
        risk_categories = list(result.risk_assessment.keys())
        risk_values = list(result.risk_assessment.values())
        
        axes[1, 1].bar(risk_categories, risk_values, alpha=0.7)
        axes[1, 1].set_ylabel('Risk Level')
        axes[1, 1].set_title('Risk Assessment')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualization saved to {output_path}")


# Example usage and demonstration
def create_sample_targets() -> List[Target]:
    """Create sample targets for demonstration."""
    return [
        Target(
            target_id="T001",
            name="Enemy Command Center",
            target_type=TargetType.COMMAND_CONTROL,
            threat_level=ThreatLevel.CRITICAL,
            location={"lat": 34.0522, "lon": -118.2437},
            value_score=95,
            protection_level=85,
            time_sensitivity=90,
            mobility=20,
            intelligence_quality=75,
            collateral_risk=60
        ),
        Target(
            target_id="T002",
            name="Military Supply Depot",
            target_type=TargetType.LOGISTICS_HUB,
            threat_level=ThreatLevel.HIGH,
            location={"lat": 34.0522, "lon": -118.2437},
            value_score=80,
            protection_level=70,
            time_sensitivity=70,
            mobility=10,
            intelligence_quality=85,
            collateral_risk=40
        ),
        Target(
            target_id="T003",
            name="Enemy Leader Residence",
            target_type=TargetType.LEADERSHIP,
            threat_level=ThreatLevel.CRITICAL,
            location={"lat": 34.0522, "lon": -118.2437},
            value_score=100,
            protection_level=90,
            time_sensitivity=95,
            mobility=50,
            intelligence_quality=60,
            collateral_risk=80
        )
    ]


def create_sample_strategies() -> List[Strategy]:
    """Create sample strategies for demonstration."""
    return [
        Strategy(
            strategy_id="S001",
            name="Stealth Infiltration",
            strategy_type=StrategyType.STEALTH_INFILTRATION,
            execution_time=4.0,
            success_probability=0.75,
            resource_requirements={"personnel": 8, "equipment": 15, "intelligence": 20},
            risk_level=60,
            detection_probability=0.3,
            collateral_damage=20,
            weather_dependency=0.4,
            night_operation_capability=0.9
        ),
        Strategy(
            strategy_id="S002",
            name="Precision Strike",
            strategy_type=StrategyType.PRECISION_STRIKE,
            execution_time=1.5,
            success_probability=0.85,
            resource_requirements={"personnel": 4, "equipment": 25, "intelligence": 15},
            risk_level=40,
            detection_probability=0.6,
            collateral_damage=30,
            weather_dependency=0.7,
            night_operation_capability=0.8
        ),
        Strategy(
            strategy_id="S003",
            name="Cyber Attack",
            strategy_type=StrategyType.CYBER_ATTACK,
            execution_time=2.0,
            success_probability=0.70,
            resource_requirements={"personnel": 6, "equipment": 10, "intelligence": 30},
            risk_level=30,
            detection_probability=0.2,
            collateral_damage=10,
            weather_dependency=0.1,
            night_operation_capability=1.0
        )
    ]


def create_sample_constraints() -> OperationalConstraints:
    """Create sample operational constraints."""
    return OperationalConstraints(
        time_limit=12.0,  # 12 hours
        available_resources={
            "personnel": 20,
            "equipment": 50,
            "intelligence": 40
        },
        weather_conditions={
            "visibility": 85,
            "wind_speed": 15,
            "precipitation": 0.1
        },
        intelligence_quality=75,
        political_restrictions=["minimize_civilian_casualties"],
        legal_constraints=["comply_with_international_law"],
        force_protection_requirements=80,
        stealth_requirements=70
    )


async def main():
    """Main demonstration function."""
    logger.info("Starting Offensive Strategy Optimization System...")
    
    # Initialize optimizer
    optimizer = OffensiveStrategyOptimizer()
    
    # Create sample data
    targets = create_sample_targets()
    strategies = create_sample_strategies()
    constraints = create_sample_constraints()
    
    # Run optimization
    logger.info("Running strategy optimization...")
    result = optimizer.optimize_strategy(targets, strategies, constraints)
    
    # Display results
    logger.info(f"Optimization completed in {result.execution_time:.2f} seconds")
    logger.info(f"Expected success rate: {result.expected_success_rate:.2%}")
    logger.info(f"Overall risk level: {result.risk_assessment['total_risk']:.1f}")
    
    # Generate visualization
    optimizer.generate_visualization(result)
    
    # Display detailed results
    print("\n=== OPTIMIZATION RESULTS ===")
    print(f"Optimal Strategy: {result.optimal_strategy.name}")
    print(f"Expected Success Rate: {result.expected_success_rate:.2%}")
    print(f"Total Risk: {result.risk_assessment['total_risk']:.1f}")
    print(f"Detection Risk: {result.risk_assessment['detection_risk']:.2%}")
    print(f"Collateral Risk: {result.risk_assessment['collateral_risk']:.1f}")
    
    print("\n=== EXECUTION SEQUENCE ===")
    for step in result.timeline:
        print(f"Step {step['step']}: {step['target_name']} - {step['strategy_name']}")
        print(f"  Duration: {step['duration']:.1f} hours")
        print(f"  Success Rate: {step['expected_success_rate']:.2%}")
        print(f"  Risk Level: {step['risk_level']:.1f}")
    
    print("\n=== RESOURCE ALLOCATION ===")
    for resource, amount in result.resource_allocation.items():
        print(f"{resource}: {amount:.1f}")
    
    print("\n=== PATTERN INSIGHTS ===")
    for pattern in result.pattern_insights:
        print(f"Pattern: {pattern.pattern_type}")
        print(f"  Confidence: {pattern.confidence:.2f}")
        print(f"  Frequency: {pattern.frequency:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
