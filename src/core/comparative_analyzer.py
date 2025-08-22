"""
Comparative Analyzer for Enhanced Report Generation System
Provides comparative analysis across time periods, entities, and benchmarks.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ComparisonType(Enum):
    """Comparison types."""
    TEMPORAL = "temporal"
    ENTITY = "entity"
    BENCHMARK = "benchmark"
    SCENARIO = "scenario"
    PERFORMANCE = "performance"


class TrendDirection(Enum):
    """Trend directions."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"
    CYCLICAL = "cyclical"


class PerformanceLevel(Enum):
    """Performance levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"
    POOR = "poor"


@dataclass
class ComparisonResult:
    """Comparison analysis result."""
    comparison_id: str
    comparison_type: ComparisonType
    comparison_periods: List[str]
    key_metrics: Dict[str, Dict[str, float]]
    trend_analysis: Dict[str, TrendDirection]
    performance_changes: Dict[str, float]
    benchmark_comparison: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    timestamp: datetime


@dataclass
class TrendAnalysis:
    """Trend analysis result."""
    trend_id: str
    metric_name: str
    trend_direction: TrendDirection
    trend_strength: float
    trend_duration: str
    seasonal_patterns: List[str]
    forecast_values: List[float]
    confidence_interval: Tuple[float, float]
    timestamp: datetime


@dataclass
class BenchmarkAnalysis:
    """Benchmark analysis result."""
    benchmark_id: str
    benchmark_source: str
    benchmark_metrics: Dict[str, float]
    performance_gaps: Dict[str, float]
    improvement_opportunities: List[str]
    best_practices: List[str]
    competitive_position: str
    timestamp: datetime


class ComparativeAnalyzer:
    """Comparative analysis engine."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        
    async def perform_comparative_analysis(
        self,
        current_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]],
        benchmark_data: Optional[Dict[str, Any]] = None,
        comparison_type: ComparisonType = ComparisonType.TEMPORAL
    ) -> ComparisonResult:
        """Perform comprehensive comparative analysis."""
        try:
            self.logger.info(f"Starting {comparison_type.value} comparative analysis")
            
            comparison_id = f"comparison_{comparison_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Define comparison periods
            comparison_periods = self._define_comparison_periods(historical_data, comparison_type)
            
            # Analyze key metrics
            key_metrics = self._analyze_key_metrics(current_data, historical_data, comparison_type)
            
            # Perform trend analysis
            trend_analysis = await self._perform_trend_analysis(key_metrics)
            
            # Calculate performance changes
            performance_changes = self._calculate_performance_changes(key_metrics)
            
            # Compare with benchmarks
            benchmark_comparison = self._compare_with_benchmarks(
                current_data, benchmark_data, comparison_type
            ) if benchmark_data else {}
            
            # Generate insights
            insights = self._generate_comparative_insights(
                key_metrics, trend_analysis, performance_changes, benchmark_comparison
            )
            
            # Generate recommendations
            recommendations = self._generate_comparative_recommendations(
                insights, performance_changes, benchmark_comparison
            )
            
            result = ComparisonResult(
                comparison_id=comparison_id,
                comparison_type=comparison_type,
                comparison_periods=comparison_periods,
                key_metrics=key_metrics,
                trend_analysis=trend_analysis,
                performance_changes=performance_changes,
                benchmark_comparison=benchmark_comparison,
                insights=insights,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Comparative analysis completed: {comparison_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in comparative analysis: {e}")
            raise
    
    async def analyze_trends(
        self,
        time_series_data: List[Dict[str, Any]],
        metric_names: List[str]
    ) -> List[TrendAnalysis]:
        """Analyze trends for specific metrics."""
        try:
            self.logger.info("Starting trend analysis")
            
            trend_analyses = []
            
            for metric_name in metric_names:
                # Extract metric values over time
                metric_values = [data.get(metric_name, 0) for data in time_series_data]
                
                if len(metric_values) < 2:
                    continue
                
                # Determine trend direction
                trend_direction = self._determine_trend_direction(metric_values)
                
                # Calculate trend strength
                trend_strength = self._calculate_trend_strength(metric_values)
                
                # Determine trend duration
                trend_duration = self._determine_trend_duration(metric_values)
                
                # Identify seasonal patterns
                seasonal_patterns = self._identify_seasonal_patterns(metric_values)
                
                # Generate forecast values
                forecast_values = self._generate_forecast_values(metric_values)
                
                # Calculate confidence interval
                confidence_interval = self._calculate_confidence_interval(metric_values)
                
                trend_analysis = TrendAnalysis(
                    trend_id=f"trend_{metric_name}_{datetime.now().strftime('%H%M%S')}",
                    metric_name=metric_name,
                    trend_direction=trend_direction,
                    trend_strength=trend_strength,
                    trend_duration=trend_duration,
                    seasonal_patterns=seasonal_patterns,
                    forecast_values=forecast_values,
                    confidence_interval=confidence_interval,
                    timestamp=datetime.now()
                )
                
                trend_analyses.append(trend_analysis)
            
            self.logger.info(f"Trend analysis completed: {len(trend_analyses)} trends analyzed")
            return trend_analyses
            
        except Exception as e:
            self.logger.error(f"Error in trend analysis: {e}")
            raise
    
    async def analyze_benchmarks(
        self,
        current_performance: Dict[str, float],
        benchmark_data: Dict[str, Any]
    ) -> BenchmarkAnalysis:
        """Analyze performance against benchmarks."""
        try:
            self.logger.info("Starting benchmark analysis")
            
            benchmark_id = f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            benchmark_source = benchmark_data.get('source', 'industry_standard')
            benchmark_metrics = benchmark_data.get('metrics', {})
            
            # Calculate performance gaps
            performance_gaps = self._calculate_performance_gaps(current_performance, benchmark_metrics)
            
            # Identify improvement opportunities
            improvement_opportunities = self._identify_improvement_opportunities(performance_gaps)
            
            # Extract best practices
            best_practices = benchmark_data.get('best_practices', [])
            
            # Determine competitive position
            competitive_position = self._determine_competitive_position(performance_gaps)
            
            result = BenchmarkAnalysis(
                benchmark_id=benchmark_id,
                benchmark_source=benchmark_source,
                benchmark_metrics=benchmark_metrics,
                performance_gaps=performance_gaps,
                improvement_opportunities=improvement_opportunities,
                best_practices=best_practices,
                competitive_position=competitive_position,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Benchmark analysis completed: {benchmark_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in benchmark analysis: {e}")
            raise
    
    def _define_comparison_periods(
        self, 
        historical_data: List[Dict[str, Any]], 
        comparison_type: ComparisonType
    ) -> List[str]:
        """Define comparison periods based on comparison type."""
        periods = []
        
        if comparison_type == ComparisonType.TEMPORAL:
            if len(historical_data) >= 4:
                periods = ["Current", "Previous Quarter", "Previous Year", "2 Years Ago"]
            elif len(historical_data) >= 3:
                periods = ["Current", "Previous Quarter", "Previous Year"]
            elif len(historical_data) >= 2:
                periods = ["Current", "Previous Period"]
            else:
                periods = ["Current"]
        elif comparison_type == ComparisonType.ENTITY:
            periods = ["Entity A", "Entity B", "Entity C"]
        elif comparison_type == ComparisonType.BENCHMARK:
            periods = ["Current", "Industry Average", "Best in Class"]
        elif comparison_type == ComparisonType.SCENARIO:
            periods = ["Baseline", "Optimistic", "Pessimistic"]
        elif comparison_type == ComparisonType.PERFORMANCE:
            periods = ["Current", "Target", "Historical Best"]
        
        return periods
    
    def _analyze_key_metrics(
        self, 
        current_data: Dict[str, Any], 
        historical_data: List[Dict[str, Any]], 
        comparison_type: ComparisonType
    ) -> Dict[str, Dict[str, float]]:
        """Analyze key metrics across comparison periods."""
        metrics = {}
        
        # Define key metrics to track based on comparison type
        if comparison_type == ComparisonType.TEMPORAL:
            key_metric_names = ['revenue', 'profitability', 'efficiency', 'market_share', 'customer_satisfaction']
        elif comparison_type == ComparisonType.ENTITY:
            key_metric_names = ['performance_score', 'efficiency_ratio', 'quality_metrics', 'cost_metrics']
        elif comparison_type == ComparisonType.BENCHMARK:
            key_metric_names = ['performance_indicators', 'efficiency_metrics', 'quality_scores', 'cost_ratios']
        elif comparison_type == ComparisonType.SCENARIO:
            key_metric_names = ['outcome_metrics', 'performance_indicators', 'risk_scores', 'opportunity_scores']
        elif comparison_type == ComparisonType.PERFORMANCE:
            key_metric_names = ['kpi_scores', 'performance_ratios', 'achievement_rates', 'improvement_metrics']
        else:
            key_metric_names = ['general_metrics']
        
        for metric_name in key_metric_names:
            metrics[metric_name] = {}
            
            # Current period
            if metric_name in current_data:
                metrics[metric_name]['current'] = current_data[metric_name]
            
            # Historical periods
            for i, historical in enumerate(historical_data):
                period_name = f"period_{i+1}"
                if metric_name in historical:
                    metrics[metric_name][period_name] = historical[metric_name]
        
        return metrics
    
    async def _perform_trend_analysis(self, key_metrics: Dict[str, Dict[str, float]]) -> Dict[str, TrendDirection]:
        """Perform trend analysis on key metrics."""
        trends = {}
        
        for metric_name, periods in key_metrics.items():
            if len(periods) >= 2:
                values = list(periods.values())
                trend_direction = self._determine_trend_direction(values)
                trends[metric_name] = trend_direction
            else:
                trends[metric_name] = TrendDirection.STABLE
        
        return trends
    
    def _calculate_performance_changes(self, key_metrics: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Calculate performance changes."""
        changes = {}
        
        for metric_name, periods in key_metrics.items():
            if 'current' in periods and len(periods) > 1:
                current_value = periods['current']
                # Use the earliest historical period for comparison
                historical_values = [v for k, v in periods.items() if k != 'current']
                if historical_values:
                    baseline_value = historical_values[0]
                    if baseline_value != 0:
                        change = (current_value - baseline_value) / baseline_value
                        changes[metric_name] = change
        
        return changes
    
    def _compare_with_benchmarks(
        self, 
        current_data: Dict[str, Any], 
        benchmark_data: Dict[str, Any], 
        comparison_type: ComparisonType
    ) -> Dict[str, Any]:
        """Compare current performance with benchmarks."""
        comparison = {}
        
        if not benchmark_data:
            return comparison
        
        benchmark_metrics = benchmark_data.get('metrics', {})
        
        for metric_name, current_value in current_data.items():
            if metric_name in benchmark_metrics:
                benchmark_value = benchmark_metrics[metric_name]
                if benchmark_value != 0:
                    performance_ratio = current_value / benchmark_value
                    comparison[metric_name] = {
                        'current': current_value,
                        'benchmark': benchmark_value,
                        'ratio': performance_ratio,
                        'status': 'above' if performance_ratio > 1 else 'below',
                        'gap_percentage': ((current_value - benchmark_value) / benchmark_value) * 100
                    }
        
        return comparison
    
    def _generate_comparative_insights(
        self,
        key_metrics: Dict[str, Dict[str, float]],
        trend_analysis: Dict[str, TrendDirection],
        performance_changes: Dict[str, float],
        benchmark_comparison: Dict[str, Any]
    ) -> List[str]:
        """Generate insights from comparative analysis."""
        insights = []
        
        # Trend insights
        for metric, trend in trend_analysis.items():
            if trend == TrendDirection.INCREASING:
                insights.append(f"{metric} showing positive trend")
            elif trend == TrendDirection.DECREASING:
                insights.append(f"{metric} showing concerning decline")
            elif trend == TrendDirection.VOLATILE:
                insights.append(f"{metric} showing high volatility")
        
        # Performance change insights
        for metric, change in performance_changes.items():
            if change > 0.1:
                insights.append(f"{metric} improved by {change:.1%}")
            elif change < -0.1:
                insights.append(f"{metric} declined by {abs(change):.1%}")
        
        # Benchmark insights
        for metric, comparison in benchmark_comparison.items():
            if comparison['status'] == 'below':
                insights.append(f"{metric} below benchmark by {abs(comparison['gap_percentage']):.1f}%")
            elif comparison['status'] == 'above':
                insights.append(f"{metric} above benchmark by {comparison['gap_percentage']:.1f}%")
        
        return insights
    
    def _generate_comparative_recommendations(
        self,
        insights: List[str],
        performance_changes: Dict[str, float],
        benchmark_comparison: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations from comparative analysis."""
        recommendations = []
        
        # Address declining metrics
        declining_metrics = [m for m, c in performance_changes.items() if c < -0.1]
        if declining_metrics:
            recommendations.append(f"Develop improvement strategies for {', '.join(declining_metrics)}")
        
        # Address below-benchmark performance
        below_benchmark = [m for m, c in benchmark_comparison.items() if c['status'] == 'below']
        if below_benchmark:
            recommendations.append(f"Focus on achieving benchmark performance for {', '.join(below_benchmark)}")
        
        # Leverage above-benchmark performance
        above_benchmark = [m for m, c in benchmark_comparison.items() if c['status'] == 'above']
        if above_benchmark:
            recommendations.append(f"Leverage competitive advantages in {', '.join(above_benchmark)}")
        
        # General recommendations
        recommendations.extend([
            "Continue monitoring key performance indicators",
            "Implement best practices from top performers",
            "Conduct root cause analysis for underperforming areas",
            "Establish continuous improvement processes"
        ])
        
        return recommendations
    
    def _determine_trend_direction(self, values: List[float]) -> TrendDirection:
        """Determine trend direction from a series of values."""
        if len(values) < 2:
            return TrendDirection.STABLE
        
        # Calculate trend using linear regression
        n = len(values)
        x = list(range(n))
        
        # Simple linear regression
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return TrendDirection.STABLE
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        
        # Determine direction based on slope
        if slope > 0.01:
            return TrendDirection.INCREASING
        elif slope < -0.01:
            return TrendDirection.DECREASING
        else:
            return TrendDirection.STABLE
    
    def _calculate_trend_strength(self, values: List[float]) -> float:
        """Calculate trend strength using R-squared."""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        
        # Calculate R-squared
        mean_y = sum(values) / n
        ss_tot = sum((y - mean_y) ** 2 for y in values)
        
        # Simple linear regression
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Calculate predicted values
        predicted = [slope * xi + intercept for xi in x]
        ss_res = sum((values[i] - predicted[i]) ** 2 for i in range(n))
        
        if ss_tot == 0:
            return 0.0
        
        r_squared = 1 - (ss_res / ss_tot)
        return max(0.0, min(1.0, r_squared))
    
    def _determine_trend_duration(self, values: List[float]) -> str:
        """Determine trend duration."""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple duration estimation
        if len(values) <= 3:
            return "short_term"
        elif len(values) <= 6:
            return "medium_term"
        else:
            return "long_term"
    
    def _identify_seasonal_patterns(self, values: List[float]) -> List[str]:
        """Identify seasonal patterns in data."""
        patterns = []
        
        if len(values) < 4:
            return patterns
        
        # Simple seasonal pattern detection
        # This is a basic implementation - more sophisticated methods could be used
        
        # Check for quarterly patterns
        if len(values) >= 4:
            q1_avg = sum(values[::4]) / len(values[::4])
            q2_avg = sum(values[1::4]) / len(values[1::4])
            q3_avg = sum(values[2::4]) / len(values[2::4])
            q4_avg = sum(values[3::4]) / len(values[3::4])
            
            if abs(q1_avg - q2_avg) > 0.1 * max(q1_avg, q2_avg):
                patterns.append("quarterly_variation")
        
        return patterns
    
    def _generate_forecast_values(self, values: List[float]) -> List[float]:
        """Generate forecast values using simple extrapolation."""
        if len(values) < 2:
            return []
        
        # Simple linear extrapolation
        n = len(values)
        x = list(range(n))
        
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return []
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Generate 3 forecast values
        forecast_values = []
        for i in range(3):
            forecast_value = slope * (n + i) + intercept
            forecast_values.append(max(0, forecast_value))  # Ensure non-negative
        
        return forecast_values
    
    def _calculate_confidence_interval(self, values: List[float]) -> Tuple[float, float]:
        """Calculate confidence interval for the data."""
        if len(values) < 2:
            return (0.0, 0.0)
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        std_dev = variance ** 0.5
        
        # 95% confidence interval
        margin_of_error = 1.96 * std_dev / (len(values) ** 0.5)
        
        return (mean - margin_of_error, mean + margin_of_error)
    
    def _calculate_performance_gaps(
        self, 
        current_performance: Dict[str, float], 
        benchmark_metrics: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate performance gaps against benchmarks."""
        gaps = {}
        
        for metric_name, current_value in current_performance.items():
            if metric_name in benchmark_metrics:
                benchmark_value = benchmark_metrics[metric_name]
                if benchmark_value != 0:
                    gap = ((current_value - benchmark_value) / benchmark_value) * 100
                    gaps[metric_name] = gap
        
        return gaps
    
    def _identify_improvement_opportunities(self, performance_gaps: Dict[str, float]) -> List[str]:
        """Identify improvement opportunities based on performance gaps."""
        opportunities = []
        
        for metric_name, gap in performance_gaps.items():
            if gap < -10:  # More than 10% below benchmark
                opportunities.append(f"Improve {metric_name} performance")
            elif gap < -5:  # More than 5% below benchmark
                opportunities.append(f"Enhance {metric_name} efficiency")
        
        return opportunities
    
    def _determine_competitive_position(self, performance_gaps: Dict[str, float]) -> str:
        """Determine overall competitive position."""
        if not performance_gaps:
            return "unknown"
        
        # Calculate average gap
        avg_gap = sum(performance_gaps.values()) / len(performance_gaps)
        
        if avg_gap > 10:
            return "leading"
        elif avg_gap > 0:
            return "above_average"
        elif avg_gap > -10:
            return "average"
        else:
            return "below_average"
    
    async def generate_comprehensive_comparative_analysis(
        self,
        current_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]],
        benchmark_data: Optional[Dict[str, Any]] = None,
        time_series_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive comparative analysis."""
        try:
            self.logger.info("Starting comprehensive comparative analysis")
            
            # Perform temporal comparison
            temporal_comparison = await self.perform_comparative_analysis(
                current_data, historical_data, benchmark_data, ComparisonType.TEMPORAL
            )
            
            # Analyze trends if time series data available
            trend_analyses = []
            if time_series_data:
                metric_names = list(current_data.keys())
                trend_analyses = await self.analyze_trends(time_series_data, metric_names)
            
            # Analyze benchmarks
            benchmark_analysis = None
            if benchmark_data:
                benchmark_analysis = await self.analyze_benchmarks(current_data, benchmark_data)
            
            # Compile comprehensive analysis
            analysis = {
                'temporal_comparison': asdict(temporal_comparison),
                'trend_analyses': [asdict(trend) for trend in trend_analyses],
                'benchmark_analysis': asdict(benchmark_analysis) if benchmark_analysis else None,
                'summary': {
                    'comparison_periods': len(temporal_comparison.comparison_periods),
                    'trends_analyzed': len(trend_analyses),
                    'benchmark_comparison': 'completed' if benchmark_analysis else 'not_applicable',
                    'key_insights': len(temporal_comparison.insights),
                    'recommendations': len(temporal_comparison.recommendations)
                },
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("Comprehensive comparative analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive comparative analysis: {e}")
            raise
