#!/usr/bin/env python3
"""
Intelligence Fusion with Monte Carlo Simulation

This script provides a comprehensive intelligence fusion system that:
- Fuses intelligence from multiple sources (HUMINT, SIGINT, OSINT, GEOINT, 
  IMINT, MASINT)
- Uses Monte Carlo simulation to generate predictive intelligence
- Calculates confidence intervals for predictions
- Provides risk assessment and uncertainty quantification
- Generates actionable intelligence recommendations

Author: DIA3 Intelligence Fusion System
Date: 2025-01-17
"""

import asyncio
import json
import logging
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid
import matplotlib.pyplot as plt
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntelligenceSource(Enum):
    """Enumeration of intelligence source types."""
    HUMINT = "HUMINT"  # Human Intelligence
    SIGINT = "SIGINT"  # Signals Intelligence
    OSINT = "OSINT"    # Open Source Intelligence
    GEOINT = "GEOINT"  # Geospatial Intelligence
    IMINT = "IMINT"    # Imagery Intelligence
    MASINT = "MASINT"  # Measurement and Signature Intelligence


@dataclass
class IntelligenceReport:
    """Represents an individual intelligence report from a source."""
    source_id: str
    source_type: IntelligenceSource
    content: str
    timestamp: datetime
    location: Optional[Dict[str, float]] = None  # lat, lon
    confidence: float = 0.0
    reliability_score: float = 0.0
    classification: str = "UNCLASSIFIED"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FusedIntelligence:
    """Represents fused intelligence from multiple sources."""
    fused_id: str
    timestamp: datetime
    sources_used: List[str]
    fused_content: str
    overall_confidence: float = 0.0
    source_correlations: Dict[str, float] = field(default_factory=dict)
    intelligence_gaps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictiveIntelligence:
    """Represents predictive intelligence with confidence intervals."""
    prediction_id: str
    timestamp: datetime
    timeframe: str
    scenario: str
    predictions: List[float]
    confidence_intervals: Dict[str, List[float]]
    confidence_level: float
    risk_assessment: Dict[str, float]
    uncertainty_metrics: Dict[str, float]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class IntelligenceFusionEngine:
    """Engine for fusing intelligence from multiple sources."""
    
    def __init__(self):
        self.source_reliability_weights = {
            IntelligenceSource.HUMINT: 0.85,
            IntelligenceSource.SIGINT: 0.90,
            IntelligenceSource.OSINT: 0.70,
            IntelligenceSource.GEOINT: 0.88,
            IntelligenceSource.IMINT: 0.92,
            IntelligenceSource.MASINT: 0.87
        }
        
        self.temporal_correlation_window = timedelta(hours=24)
        self.spatial_correlation_threshold = 50.0  # km
        self.min_confidence_threshold = 0.6
        
        logger.info("IntelligenceFusionEngine initialized successfully")
    
    async def fuse_intelligence_sources(
        self, 
        reports: List[IntelligenceReport]
    ) -> FusedIntelligence:
        """
        Fuse intelligence from multiple sources.
        
        Args:
            reports: List of intelligence reports from different sources
            
        Returns:
            FusedIntelligence object containing combined intelligence
        """
        try:
            if not reports:
                raise ValueError("No intelligence reports provided")
            
            # Filter reports by confidence threshold
            valid_reports = [
                r for r in reports if r.confidence >= self.min_confidence_threshold
            ]
            
            if not valid_reports:
                raise ValueError("No reports meet minimum confidence threshold")
            
            # Calculate source correlations
            source_correlations = await self._calculate_source_correlations(
                valid_reports
            )
            
            # Perform temporal correlation analysis
            temporal_correlations = await self._analyze_temporal_correlations(
                valid_reports
            )
            
            # Perform spatial correlation analysis
            spatial_correlations = await self._analyze_spatial_correlations(
                valid_reports
            )
            
            # Fuse content using weighted approach
            fused_content = await self._fuse_content(valid_reports)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(valid_reports)
            
            # Identify intelligence gaps
            intelligence_gaps = await self._identify_intelligence_gaps(valid_reports)
            
            return FusedIntelligence(
                fused_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                sources_used=[r.source_id for r in valid_reports],
                fused_content=fused_content,
                overall_confidence=overall_confidence,
                source_correlations=source_correlations,
                intelligence_gaps=intelligence_gaps,
                metadata={
                    "temporal_correlations": temporal_correlations,
                    "spatial_correlations": spatial_correlations,
                    "source_count": len(valid_reports)
                }
            )
            
        except Exception as e:
            logger.error(f"Error fusing intelligence sources: {e}")
            raise
    
    async def _calculate_source_correlations(
        self, 
        reports: List[IntelligenceReport]
    ) -> Dict[str, float]:
        """Calculate correlations between different intelligence sources."""
        correlations = {}
        
        for i, report1 in enumerate(reports):
            for j, report2 in enumerate(reports[i+1:], i+1):
                # Calculate semantic similarity (simplified)
                similarity = self._calculate_semantic_similarity(
                    report1.content, report2.content
                )
                
                correlation_key = f"{report1.source_id}_{report2.source_id}"
                correlations[correlation_key] = similarity
        
        return correlations
    
    def _calculate_semantic_similarity(self, content1: str, content2: str) -> float:
        """Calculate semantic similarity between two content pieces."""
        # Simplified semantic similarity calculation
        # In a real implementation, this would use NLP techniques
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    async def _analyze_temporal_correlations(
        self, 
        reports: List[IntelligenceReport]
    ) -> Dict[str, Any]:
        """Analyze temporal correlations between reports."""
        temporal_analysis = {
            "time_gaps": [],
            "temporal_clusters": [],
            "temporal_consistency": 0.0
        }
        
        # Sort reports by timestamp
        sorted_reports = sorted(reports, key=lambda x: x.timestamp)
        
        # Calculate time gaps
        for i in range(1, len(sorted_reports)):
            time_gap = sorted_reports[i].timestamp - sorted_reports[i-1].timestamp
            temporal_analysis["time_gaps"].append(time_gap.total_seconds() / 3600)  # hours
        
        # Identify temporal clusters
        current_cluster = [sorted_reports[0]]
        for report in sorted_reports[1:]:
            time_diff = report.timestamp - current_cluster[-1].timestamp
            if time_diff <= self.temporal_correlation_window:
                current_cluster.append(report)
            else:
                if len(current_cluster) > 1:
                    temporal_analysis["temporal_clusters"].append(current_cluster)
                current_cluster = [report]
        
        if len(current_cluster) > 1:
            temporal_analysis["temporal_clusters"].append(current_cluster)
        
        # Calculate temporal consistency
        if temporal_analysis["time_gaps"]:
            avg_gap = np.mean(temporal_analysis["time_gaps"])
            temporal_analysis["temporal_consistency"] = 1.0 / (1.0 + avg_gap)
        
        return temporal_analysis
    
    async def _analyze_spatial_correlations(
        self, 
        reports: List[IntelligenceReport]
    ) -> Dict[str, Any]:
        """Analyze spatial correlations between reports."""
        spatial_analysis = {
            "spatial_clusters": [],
            "geographic_coverage": 0.0,
            "spatial_consistency": 0.0
        }
        
        # Group reports by location
        location_groups = {}
        for report in reports:
            if report.location:
                location_key = f"{report.location['lat']:.2f}_{report.location['lon']:.2f}"
                if location_key not in location_groups:
                    location_groups[location_key] = []
                location_groups[location_key].append(report)
        
        # Identify spatial clusters
        for location_key, group_reports in location_groups.items():
            if len(group_reports) > 1:
                spatial_analysis["spatial_clusters"].append({
                    "location": location_key,
                    "reports": group_reports,
                    "count": len(group_reports)
                })
        
        # Calculate geographic coverage
        total_locations = len(location_groups)
        spatial_analysis["geographic_coverage"] = min(1.0, total_locations / len(reports))
        
        # Calculate spatial consistency
        if spatial_analysis["spatial_clusters"]:
            cluster_sizes = [cluster["count"] for cluster in spatial_analysis["spatial_clusters"]]
            spatial_analysis["spatial_consistency"] = np.mean(cluster_sizes) / len(reports)
        
        return spatial_analysis
    
    async def _fuse_content(self, reports: List[IntelligenceReport]) -> str:
        """Fuse content from multiple intelligence reports."""
        # Weight reports by reliability and confidence
        weighted_contents = []
        total_weight = 0.0
        
        for report in reports:
            weight = (
                self.source_reliability_weights[report.source_type] * 
                report.confidence * 
                report.reliability_score
            )
            weighted_contents.append((report.content, weight))
            total_weight += weight
        
        if total_weight == 0:
            return "Insufficient reliable intelligence for fusion."
        
        # Create fused content (simplified approach)
        # In a real implementation, this would use advanced NLP techniques
        fused_sentences = []
        for content, weight in weighted_contents:
            normalized_weight = weight / total_weight
            if normalized_weight > 0.1:  # Only include significant contributions
                fused_sentences.append(f"[{normalized_weight:.2f}] {content}")
        
        return " | ".join(fused_sentences)
    
    def _calculate_overall_confidence(self, reports: List[IntelligenceReport]) -> float:
        """Calculate overall confidence for fused intelligence."""
        if not reports:
            return 0.0
        
        # Weighted average of individual confidences
        total_weight = 0.0
        weighted_confidence = 0.0
        
        for report in reports:
            weight = (
                self.source_reliability_weights[report.source_type] * 
                report.reliability_score
            )
            weighted_confidence += weight * report.confidence
            total_weight += weight
        
        return weighted_confidence / total_weight if total_weight > 0 else 0.0
    
    async def _identify_intelligence_gaps(
        self, 
        reports: List[IntelligenceReport]
    ) -> List[str]:
        """Identify gaps in intelligence coverage."""
        gaps = []
        
        # Check for missing source types
        present_sources = {report.source_type for report in reports}
        missing_sources = set(IntelligenceSource) - present_sources
        
        for source in missing_sources:
            gaps.append(f"Missing {source.value} intelligence")
        
        # Check temporal gaps
        if len(reports) > 1:
            sorted_reports = sorted(reports, key=lambda x: x.timestamp)
            max_gap = max(
                (sorted_reports[i].timestamp - sorted_reports[i-1].timestamp).total_seconds() / 3600
                for i in range(1, len(sorted_reports))
            )
            
            if max_gap > 24:  # More than 24 hours
                gaps.append(f"Temporal gap of {max_gap:.1f} hours detected")
        
        # Check spatial coverage
        reports_with_location = [r for r in reports if r.location]
        if len(reports_with_location) < len(reports) * 0.5:
            gaps.append("Limited geospatial intelligence coverage")
        
        return gaps


class MonteCarloPredictiveEngine:
    """Engine for generating predictive intelligence using Monte Carlo simulation."""
    
    def __init__(self, num_simulations: int = 10000):
        self.num_simulations = num_simulations
        self.scenario_templates = {
            "optimistic": {"probability": 0.2, "multiplier": 1.5},
            "baseline": {"probability": 0.6, "multiplier": 1.0},
            "pessimistic": {"probability": 0.2, "multiplier": 0.5}
        }
        
        logger.info(f"MonteCarloPredictiveEngine initialized with {num_simulations} simulations")
    
    async def generate_predictive_intelligence(
        self,
        fused_intelligence: FusedIntelligence,
        timeframe: str,
        scenario: str,
        confidence_level: float = 0.95
    ) -> PredictiveIntelligence:
        """
        Generate predictive intelligence using Monte Carlo simulation.
        
        Args:
            fused_intelligence: Fused intelligence from multiple sources
            timeframe: Prediction timeframe (e.g., "30 days", "6 months")
            scenario: Scenario description
            confidence_level: Confidence level for intervals
            
        Returns:
            PredictiveIntelligence object with predictions and confidence intervals
        """
        try:
            # Parse timeframe
            time_periods = self._parse_timeframe(timeframe)
            
            # Generate base predictions
            base_predictions = await self._generate_base_predictions(
                fused_intelligence, time_periods
            )
            
            # Run Monte Carlo simulations
            simulation_results = await self._run_monte_carlo_simulations(
                base_predictions, time_periods
            )
            
            # Calculate confidence intervals
            confidence_intervals = self._calculate_confidence_intervals(
                simulation_results, confidence_level
            )
            
            # Calculate risk assessment
            risk_assessment = self._calculate_risk_assessment(simulation_results)
            
            # Calculate uncertainty metrics
            uncertainty_metrics = self._calculate_uncertainty_metrics(simulation_results)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(
                fused_intelligence, simulation_results, risk_assessment
            )
            
            return PredictiveIntelligence(
                prediction_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                timeframe=timeframe,
                scenario=scenario,
                predictions=base_predictions,
                confidence_intervals=confidence_intervals,
                confidence_level=confidence_level,
                risk_assessment=risk_assessment,
                uncertainty_metrics=uncertainty_metrics,
                recommendations=recommendations,
                metadata={
                    "num_simulations": self.num_simulations,
                    "simulation_results": simulation_results[:100]  # Store first 100 for analysis
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating predictive intelligence: {e}")
            raise
    
    def _parse_timeframe(self, timeframe: str) -> int:
        """Parse timeframe string into number of periods."""
        timeframe_lower = timeframe.lower()
        
        if "day" in timeframe_lower:
            return int(''.join(filter(str.isdigit, timeframe)))
        elif "week" in timeframe_lower:
            return int(''.join(filter(str.isdigit, timeframe))) * 7
        elif "month" in timeframe_lower:
            return int(''.join(filter(str.isdigit, timeframe))) * 30
        elif "year" in timeframe_lower:
            return int(''.join(filter(str.isdigit, timeframe))) * 365
        else:
            return 30  # Default to 30 days
    
    async def _generate_base_predictions(
        self, 
        fused_intelligence: FusedIntelligence, 
        time_periods: int
    ) -> List[float]:
        """Generate base predictions from fused intelligence."""
        # Extract numerical indicators from fused content
        # This is a simplified approach - in practice, you'd use NLP to extract specific metrics
        
        # Simulate base trend based on confidence and source correlations
        base_value = fused_intelligence.overall_confidence * 100
        
        # Generate trend over time periods
        predictions = []
        trend_factor = 1.0
        
        for period in range(time_periods):
            # Add some randomness and trend
            noise = np.random.normal(0, 2.0)
            trend_factor += np.random.normal(0.01, 0.02)
            
            prediction = base_value * trend_factor + noise
            predictions.append(max(0, prediction))  # Ensure non-negative
        
        return predictions
    
    async def _run_monte_carlo_simulations(
        self, 
        base_predictions: List[float], 
        time_periods: int
    ) -> List[List[float]]:
        """Run Monte Carlo simulations to generate multiple scenarios."""
        simulation_results = []
        
        for _ in range(self.num_simulations):
            scenario = np.random.choice(
                list(self.scenario_templates.keys()),
                p=[self.scenario_templates[s]["probability"] for s in self.scenario_templates.keys()]
            )
            
            scenario_multiplier = self.scenario_templates[scenario]["multiplier"]
            
            # Generate scenario-specific predictions
            scenario_predictions = []
            for i, base_pred in enumerate(base_predictions):
                # Add scenario-specific variations
                variation = np.random.normal(0, base_pred * 0.1)
                scenario_pred = base_pred * scenario_multiplier + variation
                scenario_predictions.append(max(0, scenario_pred))
            
            simulation_results.append(scenario_predictions)
        
        return simulation_results
    
    def _calculate_confidence_intervals(
        self, 
        simulation_results: List[List[float]], 
        confidence_level: float
    ) -> Dict[str, List[float]]:
        """Calculate confidence intervals from simulation results."""
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        # Transpose to get time series for each period
        time_series_data = list(zip(*simulation_results))
        
        confidence_intervals = {
            "lower_bound": [],
            "upper_bound": [],
            "mean": [],
            "median": []
        }
        
        for period_data in time_series_data:
            confidence_intervals["lower_bound"].append(np.percentile(period_data, lower_percentile))
            confidence_intervals["upper_bound"].append(np.percentile(period_data, upper_percentile))
            confidence_intervals["mean"].append(np.mean(period_data))
            confidence_intervals["median"].append(np.median(period_data))
        
        return confidence_intervals
    
    def _calculate_risk_assessment(
        self, 
        simulation_results: List[List[float]]
    ) -> Dict[str, float]:
        """Calculate risk assessment metrics."""
        # Calculate various risk metrics
        final_values = [sim[-1] for sim in simulation_results]
        
        risk_metrics = {
            "volatility": np.std(final_values),
            "var_95": np.percentile(final_values, 5),  # Value at Risk (95%)
            "expected_shortfall": np.mean([v for v in final_values if v <= np.percentile(final_values, 5)]),
            "max_drawdown": self._calculate_max_drawdown(simulation_results),
            "tail_risk": np.percentile(final_values, 1),  # 1% tail risk
            "upside_potential": np.percentile(final_values, 95)
        }
        
        return risk_metrics
    
    def _calculate_max_drawdown(self, simulation_results: List[List[float]]) -> float:
        """Calculate maximum drawdown across all simulations."""
        max_drawdowns = []
        
        for sim in simulation_results:
            peak = sim[0]
            max_dd = 0
            
            for value in sim:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak if peak > 0 else 0
                max_dd = max(max_dd, drawdown)
            
            max_drawdowns.append(max_dd)
        
        return np.mean(max_drawdowns)
    
    def _calculate_uncertainty_metrics(
        self, 
        simulation_results: List[List[float]]
    ) -> Dict[str, float]:
        """Calculate uncertainty metrics."""
        # Calculate uncertainty at different time points
        time_series_data = list(zip(*simulation_results))
        
        uncertainty_metrics = {
            "initial_uncertainty": np.std(time_series_data[0]),
            "final_uncertainty": np.std(time_series_data[-1]),
            "uncertainty_growth": np.std(time_series_data[-1]) - np.std(time_series_data[0]),
            "prediction_horizon_effect": len(time_series_data) * 0.1,  # Simplified
            "model_uncertainty": np.mean([np.std(sim) for sim in simulation_results])
        }
        
        return uncertainty_metrics
    
    async def _generate_recommendations(
        self,
        fused_intelligence: FusedIntelligence,
        simulation_results: List[List[float]],
        risk_assessment: Dict[str, float]
    ) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Analyze intelligence gaps
        if fused_intelligence.intelligence_gaps:
            recommendations.append(
                f"Address intelligence gaps: {', '.join(fused_intelligence.intelligence_gaps[:3])}"
            )
        
        # Risk-based recommendations
        if risk_assessment["volatility"] > 50:
            recommendations.append("High volatility detected - implement risk mitigation strategies")
        
        if risk_assessment["var_95"] < 0:
            recommendations.append("Significant downside risk - prepare contingency plans")
        
        # Confidence-based recommendations
        if fused_intelligence.overall_confidence < 0.7:
            recommendations.append("Low confidence in fused intelligence - seek additional sources")
        
        # Source diversity recommendations
        if len(fused_intelligence.sources_used) < 3:
            recommendations.append("Limited source diversity - expand intelligence collection")
        
        # Temporal recommendations
        if len(fused_intelligence.sources_used) > 1:
            recommendations.append("Maintain continuous intelligence monitoring")
        
        return recommendations


class IntelligenceFusionSystem:
    """Main system for intelligence fusion and predictive analysis."""
    
    def __init__(self):
        self.fusion_engine = IntelligenceFusionEngine()
        self.predictive_engine = MonteCarloPredictiveEngine()
        self.results_dir = Path("Results/intelligence_fusion")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("IntelligenceFusionSystem initialized successfully")
    
    async def run_comprehensive_analysis(
        self,
        intelligence_reports: List[IntelligenceReport],
        timeframe: str,
        scenario: str,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Run comprehensive intelligence fusion and predictive analysis.
        
        Args:
            intelligence_reports: List of intelligence reports from multiple sources
            timeframe: Prediction timeframe
            scenario: Scenario description
            confidence_level: Confidence level for intervals
            
        Returns:
            Dictionary containing all analysis results
        """
        try:
            logger.info(f"Starting comprehensive intelligence fusion analysis for scenario: {scenario}")
            
            # Step 1: Fuse intelligence sources
            logger.info("Step 1: Fusing intelligence sources...")
            fused_intelligence = await self.fusion_engine.fuse_intelligence_sources(
                intelligence_reports
            )
            
            # Step 2: Generate predictive intelligence
            logger.info("Step 2: Generating predictive intelligence...")
            predictive_intelligence = await self.predictive_engine.generate_predictive_intelligence(
                fused_intelligence, timeframe, scenario, confidence_level
            )
            
            # Step 3: Generate visualizations
            logger.info("Step 3: Generating visualizations...")
            visualizations = await self._generate_visualizations(
                fused_intelligence, predictive_intelligence
            )
            
            # Step 4: Create comprehensive report
            logger.info("Step 4: Creating comprehensive report...")
            report = await self._create_comprehensive_report(
                fused_intelligence, predictive_intelligence, visualizations
            )
            
            # Step 5: Save results
            logger.info("Step 5: Saving results...")
            results = await self._save_results(
                fused_intelligence, predictive_intelligence, report, visualizations
            )
            
            logger.info("Comprehensive intelligence fusion analysis completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            raise
    
    async def _generate_visualizations(
        self,
        fused_intelligence: FusedIntelligence,
        predictive_intelligence: PredictiveIntelligence
    ) -> Dict[str, str]:
        """Generate visualizations for the analysis."""
        visualizations = {}
        
        try:
            # Set style for plots
            plt.style.use('seaborn-v0_8')
            
            # 1. Prediction with confidence intervals
            fig, ax = plt.subplots(figsize=(12, 8))
            
            time_periods = range(len(predictive_intelligence.predictions))
            ci = predictive_intelligence.confidence_intervals
            
            ax.plot(time_periods, ci["mean"], 'b-', label='Mean Prediction', linewidth=2)
            ax.fill_between(
                time_periods, 
                ci["lower_bound"], 
                ci["upper_bound"], 
                alpha=0.3, 
                color='blue', 
                label=f'{predictive_intelligence.confidence_level*100:.0f}% Confidence Interval'
            )
            ax.plot(time_periods, ci["median"], 'r--', label='Median', linewidth=1)
            
            ax.set_xlabel('Time Period')
            ax.set_ylabel('Predicted Value')
            ax.set_title(f'Predictive Intelligence: {predictive_intelligence.scenario}')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            prediction_plot_path = self.results_dir / f"prediction_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(prediction_plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            visualizations["prediction_plot"] = str(prediction_plot_path)
            
            # 2. Risk assessment visualization
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Volatility distribution
            final_values = [sim[-1] for sim in predictive_intelligence.metadata["simulation_results"]]
            ax1.hist(final_values, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
            ax1.axvline(predictive_intelligence.risk_assessment["var_95"], color='red', linestyle='--', label='VaR (95%)')
            ax1.set_xlabel('Final Value')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Distribution of Final Values')
            ax1.legend()
            
            # Risk metrics
            risk_metrics = list(predictive_intelligence.risk_assessment.keys())
            risk_values = list(predictive_intelligence.risk_assessment.values())
            ax2.bar(risk_metrics, risk_values, color='lightcoral', alpha=0.7)
            ax2.set_xlabel('Risk Metric')
            ax2.set_ylabel('Value')
            ax2.set_title('Risk Assessment Metrics')
            ax2.tick_params(axis='x', rotation=45)
            
            # Uncertainty metrics
            uncertainty_metrics = list(predictive_intelligence.uncertainty_metrics.keys())
            uncertainty_values = list(predictive_intelligence.uncertainty_metrics.values())
            ax3.bar(uncertainty_metrics, uncertainty_values, color='lightgreen', alpha=0.7)
            ax3.set_xlabel('Uncertainty Metric')
            ax3.set_ylabel('Value')
            ax3.set_title('Uncertainty Metrics')
            ax3.tick_params(axis='x', rotation=45)
            
            # Source confidence
            source_ids = fused_intelligence.sources_used
            source_confidences = [fused_intelligence.source_correlations.get(f"{source_ids[0]}_{sid}", 0.5) 
                                for sid in source_ids[1:]] if len(source_ids) > 1 else [0.5]
            ax4.bar(range(len(source_confidences)), source_confidences, color='gold', alpha=0.7)
            ax4.set_xlabel('Source Pair')
            ax4.set_ylabel('Correlation')
            ax4.set_title('Source Correlations')
            
            plt.tight_layout()
            risk_plot_path = self.results_dir / f"risk_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(risk_plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            visualizations["risk_assessment"] = str(risk_plot_path)
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            visualizations["error"] = f"Visualization generation failed: {str(e)}"
        
        return visualizations
    
    async def _create_comprehensive_report(
        self,
        fused_intelligence: FusedIntelligence,
        predictive_intelligence: PredictiveIntelligence,
        visualizations: Dict[str, str]
    ) -> str:
        """Create a comprehensive markdown report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report = f"""# Intelligence Fusion and Predictive Analysis Report

## Executive Summary

**Analysis Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Scenario**: {predictive_intelligence.scenario}  
**Timeframe**: {predictive_intelligence.timeframe}  
**Overall Confidence**: {fused_intelligence.overall_confidence:.2%}

### Key Findings

- **Fused Intelligence Confidence**: {fused_intelligence.overall_confidence:.2%}
- **Sources Utilized**: {len(fused_intelligence.sources_used)} intelligence sources
- **Prediction Confidence Level**: {predictive_intelligence.confidence_level:.2%}
- **Risk Assessment**: High volatility detected with {predictive_intelligence.risk_assessment['volatility']:.2f} standard deviation

### Critical Intelligence Gaps

{fused_intelligence.intelligence_gaps if fused_intelligence.intelligence_gaps else "No significant intelligence gaps identified."}

## Detailed Analysis

### 1. Intelligence Fusion Results

**Fused Intelligence ID**: {fused_intelligence.fused_id}  
**Sources Used**: {', '.join(fused_intelligence.sources_used)}  
**Temporal Consistency**: {fused_intelligence.metadata.get('temporal_correlations', {}).get('temporal_consistency', 0):.2f}  
**Geographic Coverage**: {fused_intelligence.metadata.get('spatial_correlations', {}).get('geographic_coverage', 0):.2f}

**Fused Content Summary**:  
{fused_intelligence.fused_content[:500]}{'...' if len(fused_intelligence.fused_content) > 500 else ''}

### 2. Predictive Intelligence Results

**Prediction ID**: {predictive_intelligence.prediction_id}  
**Monte Carlo Simulations**: {predictive_intelligence.metadata['num_simulations']:,}  
**Time Periods**: {len(predictive_intelligence.predictions)}  
**Confidence Level**: {predictive_intelligence.confidence_level:.2%}

#### Key Predictions

- **Initial Value**: {predictive_intelligence.predictions[0]:.2f}
- **Final Value**: {predictive_intelligence.predictions[-1]:.2f}
- **Growth Rate**: {((predictive_intelligence.predictions[-1] / predictive_intelligence.predictions[0]) - 1) * 100:.2f}%

#### Confidence Intervals

- **Lower Bound (Final)**: {predictive_intelligence.confidence_intervals['lower_bound'][-1]:.2f}
- **Upper Bound (Final)**: {predictive_intelligence.confidence_intervals['upper_bound'][-1]:.2f}
- **Range**: {predictive_intelligence.confidence_intervals['upper_bound'][-1] - predictive_intelligence.confidence_intervals['lower_bound'][-1]:.2f}

### 3. Risk Assessment

| Risk Metric | Value |
|-------------|-------|
| Volatility | {predictive_intelligence.risk_assessment['volatility']:.2f} |
| VaR (95%) | {predictive_intelligence.risk_assessment['var_95']:.2f} |
| Expected Shortfall | {predictive_intelligence.risk_assessment['expected_shortfall']:.2f} |
| Max Drawdown | {predictive_intelligence.risk_assessment['max_drawdown']:.2%} |
| Tail Risk (1%) | {predictive_intelligence.risk_assessment['tail_risk']:.2f} |
| Upside Potential | {predictive_intelligence.risk_assessment['upside_potential']:.2f} |

### 4. Uncertainty Analysis

| Uncertainty Metric | Value |
|-------------------|-------|
| Initial Uncertainty | {predictive_intelligence.uncertainty_metrics['initial_uncertainty']:.2f} |
| Final Uncertainty | {predictive_intelligence.uncertainty_metrics['final_uncertainty']:.2f} |
| Uncertainty Growth | {predictive_intelligence.uncertainty_metrics['uncertainty_growth']:.2f} |
| Prediction Horizon Effect | {predictive_intelligence.uncertainty_metrics['prediction_horizon_effect']:.2f} |
| Model Uncertainty | {predictive_intelligence.uncertainty_metrics['model_uncertainty']:.2f} |

## Recommendations

### Priority Actions

"""
        
        for i, recommendation in enumerate(predictive_intelligence.recommendations, 1):
            report += f"{i}. {recommendation}\n"
        
        report += f"""
### Risk Mitigation Strategies

1. **High Volatility Management**: Implement dynamic risk management strategies
2. **Downside Protection**: Establish contingency plans for worst-case scenarios
3. **Continuous Monitoring**: Maintain real-time intelligence collection and analysis
4. **Source Diversification**: Expand intelligence collection to reduce source dependency

## Visualizations

- **Prediction Plot**: {visualizations.get('prediction_plot', 'Not available')}
- **Risk Assessment**: {visualizations.get('risk_assessment', 'Not available')}

## Technical Details

### Monte Carlo Simulation Parameters

- **Number of Simulations**: {predictive_intelligence.metadata['num_simulations']:,}
- **Scenario Distribution**: 
  - Optimistic: 20%
  - Baseline: 60%
  - Pessimistic: 20%
- **Confidence Level**: {predictive_intelligence.confidence_level:.2%}

### Intelligence Fusion Parameters

- **Minimum Confidence Threshold**: 60%
- **Temporal Correlation Window**: 24 hours
- **Spatial Correlation Threshold**: 50 km
- **Source Reliability Weights**: 
  - HUMINT: 85%
  - SIGINT: 90%
  - OSINT: 70%
  - GEOINT: 88%
  - IMINT: 92%
  - MASINT: 87%

## Conclusion

This comprehensive intelligence fusion and predictive analysis provides a robust foundation for strategic decision-making. The Monte Carlo simulation approach ensures that uncertainty is properly quantified and communicated, while the multi-source fusion methodology maximizes the value of available intelligence.

**Report Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Analysis System**: DIA3 Intelligence Fusion System v1.0
"""
        
        return report
    
    async def _save_results(
        self,
        fused_intelligence: FusedIntelligence,
        predictive_intelligence: PredictiveIntelligence,
        report: str,
        visualizations: Dict[str, str]
    ) -> Dict[str, Any]:
        """Save all analysis results to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_results = {
            "fused_intelligence": {
                "fused_id": fused_intelligence.fused_id,
                "timestamp": fused_intelligence.timestamp.isoformat(),
                "sources_used": fused_intelligence.sources_used,
                "fused_content": fused_intelligence.fused_content,
                "overall_confidence": fused_intelligence.overall_confidence,
                "source_correlations": fused_intelligence.source_correlations,
                "intelligence_gaps": fused_intelligence.intelligence_gaps,
                "metadata": fused_intelligence.metadata
            },
            "predictive_intelligence": {
                "prediction_id": predictive_intelligence.prediction_id,
                "timestamp": predictive_intelligence.timestamp.isoformat(),
                "timeframe": predictive_intelligence.timeframe,
                "scenario": predictive_intelligence.scenario,
                "predictions": predictive_intelligence.predictions,
                "confidence_intervals": predictive_intelligence.confidence_intervals,
                "confidence_level": predictive_intelligence.confidence_level,
                "risk_assessment": predictive_intelligence.risk_assessment,
                "uncertainty_metrics": predictive_intelligence.uncertainty_metrics,
                "recommendations": predictive_intelligence.recommendations,
                "metadata": {
                    "num_simulations": predictive_intelligence.metadata["num_simulations"]
                }
            },
            "visualizations": visualizations,
            "analysis_metadata": {
                "timestamp": datetime.now().isoformat(),
                "system_version": "DIA3 Intelligence Fusion System v1.0"
            }
        }
        
        json_path = self.results_dir / f"intelligence_fusion_results_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(json_results, f, indent=2, default=str)
        
        # Save markdown report
        report_path = self.results_dir / f"intelligence_fusion_report_{timestamp}.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        return {
            "json_results": str(json_path),
            "markdown_report": str(report_path),
            "visualizations": visualizations,
            "fused_intelligence": fused_intelligence,
            "predictive_intelligence": predictive_intelligence
        }


async def create_sample_intelligence_reports() -> List[IntelligenceReport]:
    """Create sample intelligence reports for demonstration."""
    reports = []
    
    # HUMINT Report
    reports.append(IntelligenceReport(
        source_id="HUMINT_001",
        source_type=IntelligenceSource.HUMINT,
        content="Local informant reports increased military activity in the northern region. Multiple convoys observed moving toward border areas. Informant has high reliability rating and previous reports have been 85% accurate.",
        timestamp=datetime.now() - timedelta(hours=2),
        location={"lat": 45.0, "lon": -75.0},
        confidence=0.85,
        reliability_score=0.90,
        classification="SECRET"
    ))
    
    # SIGINT Report
    reports.append(IntelligenceReport(
        source_id="SIGINT_001",
        source_type=IntelligenceSource.SIGINT,
        content="Intercepted communications indicate coordination between multiple units. Encryption patterns suggest military command structure. Signal strength and clarity indicate high-quality intelligence.",
        timestamp=datetime.now() - timedelta(hours=1),
        location={"lat": 44.8, "lon": -74.8},
        confidence=0.90,
        reliability_score=0.95,
        classification="TOP SECRET"
    ))
    
    # OSINT Report
    reports.append(IntelligenceReport(
        source_id="OSINT_001",
        source_type=IntelligenceSource.OSINT,
        content="Social media posts and news reports confirm military movements. Satellite imagery analysis shows vehicle concentrations. Open source analysis suggests coordinated military exercise.",
        timestamp=datetime.now() - timedelta(hours=3),
        location={"lat": 45.2, "lon": -75.2},
        confidence=0.70,
        reliability_score=0.75,
        classification="UNCLASSIFIED"
    ))
    
    # GEOINT Report
    reports.append(IntelligenceReport(
        source_id="GEOINT_001",
        source_type=IntelligenceSource.GEOINT,
        content="Satellite imagery analysis reveals significant military buildup in three locations. Thermal signatures indicate active equipment. Terrain analysis shows optimal defensive positions being established.",
        timestamp=datetime.now() - timedelta(hours=4),
        location={"lat": 45.1, "lon": -75.1},
        confidence=0.88,
        reliability_score=0.92,
        classification="SECRET"
    ))
    
    return reports


async def main():
    """Main function to demonstrate the intelligence fusion system."""
    try:
        logger.info("Starting Intelligence Fusion with Monte Carlo Simulation Demo")
        
        # Create sample intelligence reports
        intelligence_reports = await create_sample_intelligence_reports()
        logger.info(f"Created {len(intelligence_reports)} sample intelligence reports")
        
        # Initialize the intelligence fusion system
        fusion_system = IntelligenceFusionSystem()
        
        # Run comprehensive analysis
        results = await fusion_system.run_comprehensive_analysis(
            intelligence_reports=intelligence_reports,
            timeframe="30 days",
            scenario="Regional Military Buildup Analysis",
            confidence_level=0.95
        )
        
        # Print summary
        logger.info("Analysis completed successfully!")
        logger.info(f"Results saved to: {results['json_results']}")
        logger.info(f"Report saved to: {results['markdown_report']}")
        logger.info(f"Visualizations: {list(results['visualizations'].keys())}")
        
        # Print key findings
        fused_intel = results['fused_intelligence']
        pred_intel = results['predictive_intelligence']
        
        print("\n" + "="*80)
        print("INTELLIGENCE FUSION AND PREDICTIVE ANALYSIS RESULTS")
        print("="*80)
        print(f"Scenario: {pred_intel.scenario}")
        print(f"Timeframe: {pred_intel.timeframe}")
        print(f"Overall Confidence: {fused_intel.overall_confidence:.2%}")
        print(f"Sources Used: {len(fused_intel.sources_used)}")
        print(f"Prediction Confidence Level: {pred_intel.confidence_level:.2%}")
        print(f"Risk - Volatility: {pred_intel.risk_assessment['volatility']:.2f}")
        print(f"Risk - VaR (95%): {pred_intel.risk_assessment['var_95']:.2f}")
        print(f"Intelligence Gaps: {len(fused_intel.intelligence_gaps)}")
        print(f"Recommendations: {len(pred_intel.recommendations)}")
        print("="*80)
        
        return results
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())
