"""
Executive Summary Generator for Enhanced Report Generation System
Provides AI-generated executive summaries, key insights extraction, and strategic recommendations.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class SummaryType(Enum):
    """Summary types."""
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    FINANCIAL = "financial"


class InsightCategory(Enum):
    """Insight categories."""
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    THREAT = "threat"


class PriorityLevel(Enum):
    """Priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class KeyInsight:
    """Key insight extracted from analysis."""
    insight_id: str
    category: InsightCategory
    description: str
    priority: PriorityLevel
    impact_score: float
    confidence_level: float
    supporting_data: List[str]
    recommendations: List[str]
    timestamp: datetime


@dataclass
class ExecutiveSummary:
    """Executive summary result."""
    summary_id: str
    summary_type: SummaryType
    overview: str
    key_findings: List[str]
    critical_insights: List[KeyInsight]
    strategic_recommendations: List[str]
    risk_highlights: List[str]
    opportunities: List[str]
    next_steps: List[str]
    timestamp: datetime


@dataclass
class ComparativeAnalysis:
    """Comparative analysis result."""
    comparison_id: str
    comparison_periods: List[str]
    key_metrics: Dict[str, Dict[str, float]]
    trend_analysis: Dict[str, str]
    performance_changes: Dict[str, float]
    benchmark_comparison: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    timestamp: datetime


@dataclass
class ImpactAnalysis:
    """Impact analysis result."""
    impact_id: str
    impact_areas: List[str]
    impact_scores: Dict[str, float]
    affected_stakeholders: List[str]
    timeline_impact: Dict[str, str]
    resource_requirements: Dict[str, Any]
    risk_implications: List[str]
    mitigation_strategies: List[str]
    success_metrics: List[str]
    timestamp: datetime


class ExecutiveSummaryGenerator:
    """Executive summary generation engine."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        
    async def generate_executive_summary(
        self,
        analysis_data: Dict[str, Any],
        summary_type: SummaryType = SummaryType.EXECUTIVE,
        target_audience: str = "executive"
    ) -> ExecutiveSummary:
        """Generate executive summary from analysis data."""
        try:
            self.logger.info(f"Generating {summary_type.value} executive summary")
            
            summary_id = f"summary_{summary_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate overview
            overview = self._generate_overview(analysis_data, summary_type, target_audience)
            
            # Extract key findings
            key_findings = self._extract_key_findings(analysis_data, summary_type)
            
            # Extract critical insights
            critical_insights = await self._extract_critical_insights(analysis_data, summary_type)
            
            # Generate strategic recommendations
            strategic_recommendations = self._generate_strategic_recommendations(
                analysis_data, critical_insights, summary_type
            )
            
            # Identify risk highlights
            risk_highlights = self._identify_risk_highlights(analysis_data)
            
            # Identify opportunities
            opportunities = self._identify_opportunities(analysis_data)
            
            # Define next steps
            next_steps = self._define_next_steps(analysis_data, strategic_recommendations)
            
            result = ExecutiveSummary(
                summary_id=summary_id,
                summary_type=summary_type,
                overview=overview,
                key_findings=key_findings,
                critical_insights=critical_insights,
                strategic_recommendations=strategic_recommendations,
                risk_highlights=risk_highlights,
                opportunities=opportunities,
                next_steps=next_steps,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Executive summary generated: {summary_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating executive summary: {e}")
            raise
    
    async def perform_comparative_analysis(
        self,
        current_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]],
        benchmark_data: Optional[Dict[str, Any]] = None
    ) -> ComparativeAnalysis:
        """Perform comparative analysis across time periods."""
        try:
            self.logger.info("Starting comparative analysis")
            
            comparison_id = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Define comparison periods
            comparison_periods = self._define_comparison_periods(historical_data)
            
            # Analyze key metrics
            key_metrics = self._analyze_key_metrics(current_data, historical_data)
            
            # Perform trend analysis
            trend_analysis = self._perform_trend_analysis(key_metrics)
            
            # Calculate performance changes
            performance_changes = self._calculate_performance_changes(key_metrics)
            
            # Compare with benchmarks
            benchmark_comparison = self._compare_with_benchmarks(
                current_data, benchmark_data
            ) if benchmark_data else {}
            
            # Generate insights
            insights = self._generate_comparative_insights(
                key_metrics, trend_analysis, performance_changes, benchmark_comparison
            )
            
            # Generate recommendations
            recommendations = self._generate_comparative_recommendations(
                insights, performance_changes, benchmark_comparison
            )
            
            result = ComparativeAnalysis(
                comparison_id=comparison_id,
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
    
    async def analyze_impact(
        self,
        change_data: Dict[str, Any],
        current_state: Dict[str, Any],
        stakeholder_data: Dict[str, Any]
    ) -> ImpactAnalysis:
        """Analyze impact of changes or initiatives."""
        try:
            self.logger.info("Starting impact analysis")
            
            impact_id = f"impact_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Identify impact areas
            impact_areas = self._identify_impact_areas(change_data, current_state)
            
            # Calculate impact scores
            impact_scores = self._calculate_impact_scores(change_data, current_state, impact_areas)
            
            # Identify affected stakeholders
            affected_stakeholders = self._identify_affected_stakeholders(
                change_data, stakeholder_data
            )
            
            # Analyze timeline impact
            timeline_impact = self._analyze_timeline_impact(change_data, current_state)
            
            # Assess resource requirements
            resource_requirements = self._assess_resource_requirements(change_data, current_state)
            
            # Identify risk implications
            risk_implications = self._identify_risk_implications(change_data, current_state)
            
            # Generate mitigation strategies
            mitigation_strategies = self._generate_mitigation_strategies(
                risk_implications, impact_scores
            )
            
            # Define success metrics
            success_metrics = self._define_success_metrics(change_data, impact_areas)
            
            result = ImpactAnalysis(
                impact_id=impact_id,
                impact_areas=impact_areas,
                impact_scores=impact_scores,
                affected_stakeholders=affected_stakeholders,
                timeline_impact=timeline_impact,
                resource_requirements=resource_requirements,
                risk_implications=risk_implications,
                mitigation_strategies=mitigation_strategies,
                success_metrics=success_metrics,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Impact analysis completed: {impact_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in impact analysis: {e}")
            raise
    
    def _generate_overview(
        self, 
        analysis_data: Dict[str, Any], 
        summary_type: SummaryType, 
        target_audience: str
    ) -> str:
        """Generate overview section of executive summary."""
        overview = f"This {summary_type.value} analysis provides a comprehensive assessment of "
        
        if summary_type == SummaryType.EXECUTIVE:
            overview += "the organization's current position, key challenges, and strategic opportunities. "
        elif summary_type == SummaryType.TECHNICAL:
            overview += "technical capabilities, system performance, and technology infrastructure. "
        elif summary_type == SummaryType.OPERATIONAL:
            overview += "operational efficiency, process performance, and resource utilization. "
        elif summary_type == SummaryType.STRATEGIC:
            overview += "strategic positioning, competitive landscape, and market opportunities. "
        elif summary_type == SummaryType.FINANCIAL:
            overview += "financial performance, risk exposure, and investment opportunities. "
        
        # Add key highlights
        key_metrics = analysis_data.get('key_metrics', {})
        if key_metrics:
            overview += f"Key performance indicators show {len(key_metrics)} critical areas requiring attention. "
        
        # Add risk summary
        risks = analysis_data.get('risks', [])
        if risks:
            overview += f"Analysis identified {len(risks)} significant risks that require immediate attention. "
        
        # Add opportunity summary
        opportunities = analysis_data.get('opportunities', [])
        if opportunities:
            overview += f"Several strategic opportunities have been identified for potential growth and improvement. "
        
        return overview
    
    def _extract_key_findings(
        self, 
        analysis_data: Dict[str, Any], 
        summary_type: SummaryType
    ) -> List[str]:
        """Extract key findings from analysis data."""
        findings = []
        
        # Extract findings based on summary type
        if summary_type == SummaryType.EXECUTIVE:
            findings.extend(self._extract_executive_findings(analysis_data))
        elif summary_type == SummaryType.TECHNICAL:
            findings.extend(self._extract_technical_findings(analysis_data))
        elif summary_type == SummaryType.OPERATIONAL:
            findings.extend(self._extract_operational_findings(analysis_data))
        elif summary_type == SummaryType.STRATEGIC:
            findings.extend(self._extract_strategic_findings(analysis_data))
        elif summary_type == SummaryType.FINANCIAL:
            findings.extend(self._extract_financial_findings(analysis_data))
        
        # Limit to top findings
        return findings[:10]
    
    async def _extract_critical_insights(
        self, 
        analysis_data: Dict[str, Any], 
        summary_type: SummaryType
    ) -> List[KeyInsight]:
        """Extract critical insights from analysis data."""
        insights = []
        
        # Extract insights from different analysis components
        if 'strategic_analysis' in analysis_data:
            insights.extend(self._extract_strategic_insights(analysis_data['strategic_analysis']))
        
        if 'risk_analysis' in analysis_data:
            insights.extend(self._extract_risk_insights(analysis_data['risk_analysis']))
        
        if 'performance_analysis' in analysis_data:
            insights.extend(self._extract_performance_insights(analysis_data['performance_analysis']))
        
        if 'market_analysis' in analysis_data:
            insights.extend(self._extract_market_insights(analysis_data['market_analysis']))
        
        # Sort by priority and impact
        insights.sort(key=lambda x: (x.priority.value, x.impact_score), reverse=True)
        
        # Return top insights
        return insights[:15]
    
    def _generate_strategic_recommendations(
        self, 
        analysis_data: Dict[str, Any], 
        critical_insights: List[KeyInsight], 
        summary_type: SummaryType
    ) -> List[str]:
        """Generate strategic recommendations."""
        recommendations = []
        
        # Generate recommendations based on critical insights
        for insight in critical_insights[:5]:  # Top 5 insights
            if insight.priority in [PriorityLevel.HIGH, PriorityLevel.CRITICAL]:
                recommendations.extend(insight.recommendations[:2])
        
        # Add summary-type specific recommendations
        if summary_type == SummaryType.EXECUTIVE:
            recommendations.extend([
                "Establish cross-functional implementation teams",
                "Develop comprehensive change management strategy",
                "Implement regular progress monitoring and reporting"
            ])
        elif summary_type == SummaryType.STRATEGIC:
            recommendations.extend([
                "Conduct detailed market opportunity analysis",
                "Develop competitive positioning strategy",
                "Establish strategic partnerships"
            ])
        
        # Add general recommendations
        recommendations.extend([
            "Monitor key performance indicators regularly",
            "Conduct periodic review and adjustment of strategies",
            "Maintain stakeholder communication and engagement"
        ])
        
        return recommendations[:10]  # Limit to top 10
    
    def _identify_risk_highlights(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Identify key risk highlights."""
        risk_highlights = []
        
        # Extract high-priority risks
        risks = analysis_data.get('risks', [])
        for risk in risks:
            if risk.get('priority', 'low') in ['high', 'critical']:
                risk_highlights.append(f"High-priority risk: {risk.get('description', 'Unknown risk')}")
        
        # Extract risk trends
        risk_trends = analysis_data.get('risk_trends', [])
        for trend in risk_trends:
            if trend.get('trend_direction') == 'increasing':
                risk_highlights.append(f"Increasing risk trend: {trend.get('category', 'Unknown category')}")
        
        return risk_highlights[:5]  # Limit to top 5
    
    def _identify_opportunities(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Identify key opportunities."""
        opportunities = []
        
        # Extract opportunities from analysis
        opps = analysis_data.get('opportunities', [])
        for opp in opps:
            opportunities.append(opp.get('description', 'Unknown opportunity'))
        
        # Extract market opportunities
        market_analysis = analysis_data.get('market_analysis', {})
        market_opps = market_analysis.get('opportunities', [])
        for opp in market_opps:
            opportunities.append(f"Market opportunity: {opp}")
        
        return opportunities[:5]  # Limit to top 5
    
    def _define_next_steps(
        self, 
        analysis_data: Dict[str, Any], 
        strategic_recommendations: List[str]
    ) -> List[str]:
        """Define next steps based on analysis and recommendations."""
        next_steps = []
        
        # Immediate actions (next 30 days)
        next_steps.append("Establish implementation team and assign responsibilities")
        next_steps.append("Develop detailed action plan with timelines")
        next_steps.append("Conduct stakeholder alignment meetings")
        
        # Short-term actions (next 90 days)
        next_steps.append("Begin implementation of high-priority recommendations")
        next_steps.append("Establish monitoring and reporting mechanisms")
        next_steps.append("Conduct initial progress review")
        
        # Medium-term actions (next 6 months)
        next_steps.append("Complete implementation of strategic initiatives")
        next_steps.append("Evaluate effectiveness and adjust strategies")
        next_steps.append("Prepare for next phase of implementation")
        
        return next_steps
    
    def _extract_executive_findings(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Extract executive-level findings."""
        findings = []
        
        # Performance findings
        performance = analysis_data.get('performance', {})
        if performance.get('overall_score', 0) < 0.7:
            findings.append("Overall performance below target levels")
        
        # Strategic findings
        strategic = analysis_data.get('strategic_positioning', {})
        if strategic.get('position') == 'vulnerable':
            findings.append("Strategic position requires immediate attention")
        
        # Financial findings
        financial = analysis_data.get('financial_metrics', {})
        if financial.get('profitability', 0) < 0.1:
            findings.append("Profitability below industry benchmarks")
        
        return findings
    
    def _extract_technical_findings(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Extract technical findings."""
        findings = []
        
        # System performance
        systems = analysis_data.get('system_performance', {})
        if systems.get('availability', 1.0) < 0.99:
            findings.append("System availability below target levels")
        
        # Technology infrastructure
        infrastructure = analysis_data.get('infrastructure', {})
        if infrastructure.get('modernization_needed', False):
            findings.append("Technology infrastructure requires modernization")
        
        return findings
    
    def _extract_operational_findings(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Extract operational findings."""
        findings = []
        
        # Efficiency metrics
        efficiency = analysis_data.get('operational_efficiency', {})
        if efficiency.get('overall_efficiency', 0) < 0.8:
            findings.append("Operational efficiency below optimal levels")
        
        # Process performance
        processes = analysis_data.get('process_performance', {})
        if processes.get('bottlenecks', []):
            findings.append("Process bottlenecks identified")
        
        return findings
    
    def _extract_strategic_findings(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Extract strategic findings."""
        findings = []
        
        # Market position
        market = analysis_data.get('market_position', {})
        if market.get('market_share', 0) < 0.1:
            findings.append("Market share below competitive levels")
        
        # Competitive analysis
        competitive = analysis_data.get('competitive_analysis', {})
        if competitive.get('threat_level', 'low') in ['high', 'critical']:
            findings.append("High competitive threat level")
        
        return findings
    
    def _extract_financial_findings(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Extract financial findings."""
        findings = []
        
        # Financial performance
        financial = analysis_data.get('financial_performance', {})
        if financial.get('revenue_growth', 0) < 0.05:
            findings.append("Revenue growth below target levels")
        
        # Risk exposure
        risk = analysis_data.get('financial_risk', {})
        if risk.get('exposure_level', 'low') in ['high', 'critical']:
            findings.append("High financial risk exposure")
        
        return findings
    
    def _extract_strategic_insights(self, strategic_data: Dict[str, Any]) -> List[KeyInsight]:
        """Extract strategic insights."""
        insights = []
        
        # Position insights
        position = strategic_data.get('position', {})
        if position.get('position') == 'vulnerable':
            insights.append(KeyInsight(
                insight_id=f"strategic_position_{datetime.now().strftime('%H%M%S')}",
                category=InsightCategory.STRATEGIC,
                description="Strategic position is vulnerable and requires immediate attention",
                priority=PriorityLevel.CRITICAL,
                impact_score=0.9,
                confidence_level=0.8,
                supporting_data=["Market share analysis", "Competitive positioning"],
                recommendations=["Develop defensive strategies", "Strengthen competitive advantages"],
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _extract_risk_insights(self, risk_data: Dict[str, Any]) -> List[KeyInsight]:
        """Extract risk insights."""
        insights = []
        
        # High-risk factors
        risks = risk_data.get('high_priority_risks', [])
        for risk in risks[:3]:  # Top 3 risks
            insights.append(KeyInsight(
                insight_id=f"risk_{risk.get('id', 'unknown')}",
                category=InsightCategory.RISK,
                description=f"High-priority risk: {risk.get('description', 'Unknown')}",
                priority=PriorityLevel.HIGH,
                impact_score=risk.get('impact_score', 0.7),
                confidence_level=risk.get('confidence', 0.7),
                supporting_data=risk.get('supporting_data', []),
                recommendations=risk.get('mitigation_measures', []),
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _extract_performance_insights(self, performance_data: Dict[str, Any]) -> List[KeyInsight]:
        """Extract performance insights."""
        insights = []
        
        # Performance gaps
        gaps = performance_data.get('performance_gaps', [])
        for gap in gaps[:3]:  # Top 3 gaps
            insights.append(KeyInsight(
                insight_id=f"performance_gap_{gap.get('id', 'unknown')}",
                category=InsightCategory.OPERATIONAL,
                description=f"Performance gap: {gap.get('description', 'Unknown')}",
                priority=PriorityLevel.MEDIUM,
                impact_score=gap.get('impact_score', 0.6),
                confidence_level=gap.get('confidence', 0.8),
                supporting_data=gap.get('supporting_data', []),
                recommendations=gap.get('improvement_actions', []),
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _extract_market_insights(self, market_data: Dict[str, Any]) -> List[KeyInsight]:
        """Extract market insights."""
        insights = []
        
        # Market opportunities
        opportunities = market_data.get('opportunities', [])
        for opp in opportunities[:3]:  # Top 3 opportunities
            insights.append(KeyInsight(
                insight_id=f"opportunity_{opp.get('id', 'unknown')}",
                category=InsightCategory.OPPORTUNITY,
                description=f"Market opportunity: {opp.get('description', 'Unknown')}",
                priority=PriorityLevel.HIGH,
                impact_score=opp.get('impact_score', 0.8),
                confidence_level=opp.get('confidence', 0.7),
                supporting_data=opp.get('supporting_data', []),
                recommendations=opp.get('action_items', []),
                timestamp=datetime.now()
            ))
        
        return insights
    
    def _define_comparison_periods(self, historical_data: List[Dict[str, Any]]) -> List[str]:
        """Define comparison periods for analysis."""
        periods = []
        
        if len(historical_data) >= 3:
            periods = ["Current", "Previous Quarter", "Previous Year"]
        elif len(historical_data) >= 2:
            periods = ["Current", "Previous Period"]
        else:
            periods = ["Current"]
        
        return periods
    
    def _analyze_key_metrics(
        self, 
        current_data: Dict[str, Any], 
        historical_data: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, float]]:
        """Analyze key metrics across time periods."""
        metrics = {}
        
        # Define key metrics to track
        key_metric_names = ['revenue', 'profitability', 'efficiency', 'market_share', 'customer_satisfaction']
        
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
    
    def _perform_trend_analysis(self, key_metrics: Dict[str, Dict[str, float]]) -> Dict[str, str]:
        """Perform trend analysis on key metrics."""
        trends = {}
        
        for metric_name, periods in key_metrics.items():
            if len(periods) >= 2:
                values = list(periods.values())
                if values[-1] > values[0]:
                    trends[metric_name] = "increasing"
                elif values[-1] < values[0]:
                    trends[metric_name] = "decreasing"
                else:
                    trends[metric_name] = "stable"
            else:
                trends[metric_name] = "insufficient_data"
        
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
        benchmark_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare current performance with benchmarks."""
        comparison = {}
        
        if not benchmark_data:
            return comparison
        
        for metric_name, current_value in current_data.items():
            if metric_name in benchmark_data:
                benchmark_value = benchmark_data[metric_name]
                if benchmark_value != 0:
                    performance_ratio = current_value / benchmark_value
                    comparison[metric_name] = {
                        'current': current_value,
                        'benchmark': benchmark_value,
                        'ratio': performance_ratio,
                        'status': 'above' if performance_ratio > 1 else 'below'
                    }
        
        return comparison
    
    def _generate_comparative_insights(
        self,
        key_metrics: Dict[str, Dict[str, float]],
        trend_analysis: Dict[str, str],
        performance_changes: Dict[str, float],
        benchmark_comparison: Dict[str, Any]
    ) -> List[str]:
        """Generate insights from comparative analysis."""
        insights = []
        
        # Trend insights
        for metric, trend in trend_analysis.items():
            if trend == "increasing":
                insights.append(f"{metric} showing positive trend")
            elif trend == "decreasing":
                insights.append(f"{metric} showing concerning decline")
        
        # Performance change insights
        for metric, change in performance_changes.items():
            if change > 0.1:
                insights.append(f"{metric} improved by {change:.1%}")
            elif change < -0.1:
                insights.append(f"{metric} declined by {abs(change):.1%}")
        
        # Benchmark insights
        for metric, comparison in benchmark_comparison.items():
            if comparison['status'] == 'below':
                insights.append(f"{metric} below industry benchmark")
            elif comparison['status'] == 'above':
                insights.append(f"{metric} above industry benchmark")
        
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
        
        # General recommendations
        recommendations.extend([
            "Continue monitoring key performance indicators",
            "Implement best practices from top performers",
            "Conduct root cause analysis for underperforming areas"
        ])
        
        return recommendations
    
    def _identify_impact_areas(
        self, 
        change_data: Dict[str, Any], 
        current_state: Dict[str, Any]
    ) -> List[str]:
        """Identify areas that will be impacted by changes."""
        impact_areas = []
        
        # Determine impact based on change type
        change_type = change_data.get('type', 'general')
        
        if change_type == 'strategic':
            impact_areas.extend(['market_position', 'competitive_landscape', 'business_model'])
        elif change_type == 'operational':
            impact_areas.extend(['processes', 'efficiency', 'resource_utilization'])
        elif change_type == 'financial':
            impact_areas.extend(['revenue', 'costs', 'profitability', 'cash_flow'])
        elif change_type == 'technology':
            impact_areas.extend(['systems', 'infrastructure', 'capabilities'])
        
        return impact_areas
    
    def _calculate_impact_scores(
        self, 
        change_data: Dict[str, Any], 
        current_state: Dict[str, Any], 
        impact_areas: List[str]
    ) -> Dict[str, float]:
        """Calculate impact scores for different areas."""
        impact_scores = {}
        
        for area in impact_areas:
            # Base impact score
            base_score = change_data.get('impact_magnitude', 0.5)
            
            # Adjust based on area sensitivity
            sensitivity_factors = {
                'market_position': 0.9,
                'competitive_landscape': 0.8,
                'business_model': 0.9,
                'processes': 0.7,
                'efficiency': 0.6,
                'resource_utilization': 0.6,
                'revenue': 0.8,
                'costs': 0.7,
                'profitability': 0.9,
                'cash_flow': 0.8,
                'systems': 0.7,
                'infrastructure': 0.6,
                'capabilities': 0.8
            }
            
            sensitivity = sensitivity_factors.get(area, 0.5)
            impact_scores[area] = base_score * sensitivity
        
        return impact_scores
    
    def _identify_affected_stakeholders(
        self, 
        change_data: Dict[str, Any], 
        stakeholder_data: Dict[str, Any]
    ) -> List[str]:
        """Identify stakeholders affected by changes."""
        affected_stakeholders = []
        
        # Determine affected stakeholders based on change type
        change_type = change_data.get('type', 'general')
        
        if change_type == 'strategic':
            affected_stakeholders.extend(['executives', 'board_members', 'investors'])
        elif change_type == 'operational':
            affected_stakeholders.extend(['employees', 'managers', 'customers'])
        elif change_type == 'financial':
            affected_stakeholders.extend(['investors', 'creditors', 'shareholders'])
        elif change_type == 'technology':
            affected_stakeholders.extend(['IT_staff', 'end_users', 'customers'])
        
        return affected_stakeholders
    
    def _analyze_timeline_impact(
        self, 
        change_data: Dict[str, Any], 
        current_state: Dict[str, Any]
    ) -> Dict[str, str]:
        """Analyze timeline impact of changes."""
        timeline_impact = {
            'implementation_duration': change_data.get('implementation_duration', '6 months'),
            'critical_path': change_data.get('critical_path', 'standard'),
            'milestone_requirements': change_data.get('milestone_requirements', []),
            'resource_availability': change_data.get('resource_availability', 'adequate')
        }
        
        return timeline_impact
    
    def _assess_resource_requirements(
        self, 
        change_data: Dict[str, Any], 
        current_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess resource requirements for implementation."""
        resource_requirements = {
            'human_resources': change_data.get('human_resources', {}),
            'financial_resources': change_data.get('financial_resources', {}),
            'technology_resources': change_data.get('technology_resources', {}),
            'time_requirements': change_data.get('time_requirements', {})
        }
        
        return resource_requirements
    
    def _identify_risk_implications(
        self, 
        change_data: Dict[str, Any], 
        current_state: Dict[str, Any]
    ) -> List[str]:
        """Identify risk implications of changes."""
        risk_implications = []
        
        # Implementation risks
        if change_data.get('implementation_complexity', 0) > 0.7:
            risk_implications.append("High implementation complexity risk")
        
        # Resource risks
        if change_data.get('resource_availability', 'adequate') == 'limited':
            risk_implications.append("Limited resource availability risk")
        
        # Timeline risks
        if change_data.get('timeline_pressure', False):
            risk_implications.append("Timeline pressure risk")
        
        # Stakeholder risks
        if change_data.get('stakeholder_resistance', False):
            risk_implications.append("Stakeholder resistance risk")
        
        return risk_implications
    
    def _generate_mitigation_strategies(
        self, 
        risk_implications: List[str], 
        impact_scores: Dict[str, float]
    ) -> List[str]:
        """Generate mitigation strategies for identified risks."""
        strategies = []
        
        for risk in risk_implications:
            if "implementation complexity" in risk.lower():
                strategies.append("Implement phased approach with clear milestones")
                strategies.append("Establish dedicated implementation team")
            elif "resource availability" in risk.lower():
                strategies.append("Prioritize resource allocation to critical areas")
                strategies.append("Develop resource contingency plans")
            elif "timeline pressure" in risk.lower():
                strategies.append("Establish realistic timeline with buffer periods")
                strategies.append("Implement parallel work streams where possible")
            elif "stakeholder resistance" in risk.lower():
                strategies.append("Develop comprehensive change management plan")
                strategies.append("Establish stakeholder communication strategy")
        
        return strategies
    
    def _define_success_metrics(
        self, 
        change_data: Dict[str, Any], 
        impact_areas: List[str]
    ) -> List[str]:
        """Define success metrics for change implementation."""
        success_metrics = []
        
        for area in impact_areas:
            if area == 'market_position':
                success_metrics.append("Market share improvement")
                success_metrics.append("Competitive positioning enhancement")
            elif area == 'efficiency':
                success_metrics.append("Operational efficiency improvement")
                success_metrics.append("Cost reduction achievement")
            elif area == 'revenue':
                success_metrics.append("Revenue growth targets")
                success_metrics.append("Profitability improvement")
            elif area == 'systems':
                success_metrics.append("System performance improvement")
                success_metrics.append("Technology capability enhancement")
        
        # General success metrics
        success_metrics.extend([
            "Timeline adherence",
            "Budget compliance",
            "Stakeholder satisfaction",
            "Risk mitigation effectiveness"
        ])
        
        return success_metrics
    
    async def generate_comprehensive_summary_analysis(
        self,
        analysis_data: Dict[str, Any],
        historical_data: List[Dict[str, Any]],
        change_data: Optional[Dict[str, Any]] = None,
        benchmark_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive summary analysis."""
        try:
            self.logger.info("Starting comprehensive summary analysis")
            
            # Generate executive summary
            executive_summary = await self.generate_executive_summary(analysis_data)
            
            # Perform comparative analysis
            comparative_analysis = await self.perform_comparative_analysis(
                analysis_data, historical_data, benchmark_data
            )
            
            # Analyze impact if change data provided
            impact_analysis = None
            if change_data:
                current_state = analysis_data.get('current_state', {})
                stakeholder_data = analysis_data.get('stakeholder_data', {})
                impact_analysis = await self.analyze_impact(change_data, current_state, stakeholder_data)
            
            # Compile comprehensive analysis
            analysis = {
                'executive_summary': asdict(executive_summary),
                'comparative_analysis': asdict(comparative_analysis),
                'impact_analysis': asdict(impact_analysis) if impact_analysis else None,
                'summary': {
                    'key_insights_count': len(executive_summary.critical_insights),
                    'recommendations_count': len(executive_summary.strategic_recommendations),
                    'risk_highlights_count': len(executive_summary.risk_highlights),
                    'opportunities_count': len(executive_summary.opportunities),
                    'performance_trends': comparative_analysis.trend_analysis,
                    'impact_assessment': 'completed' if impact_analysis else 'not_applicable'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("Comprehensive summary analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive summary analysis: {e}")
            raise
