"""
Impact Analyzer for Enhanced Report Generation System
Provides impact assessment, change analysis, and operational impact evaluation.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ImpactType(Enum):
    """Impact types."""
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    TECHNOLOGICAL = "technological"
    ORGANIZATIONAL = "organizational"
    ENVIRONMENTAL = "environmental"
    SOCIAL = "social"


class ImpactSeverity(Enum):
    """Impact severity levels."""
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class ChangeType(Enum):
    """Change types."""
    INCREMENTAL = "incremental"
    TRANSFORMATIONAL = "transformational"
    DISRUPTIVE = "disruptive"
    EVOLUTIONARY = "evolutionary"


@dataclass
class ImpactAssessment:
    """Impact assessment result."""
    impact_id: str
    impact_type: ImpactType
    impact_severity: ImpactSeverity
    impact_areas: List[str]
    impact_scores: Dict[str, float]
    affected_stakeholders: List[str]
    timeline_impact: Dict[str, str]
    resource_requirements: Dict[str, Any]
    risk_implications: List[str]
    mitigation_strategies: List[str]
    success_metrics: List[str]
    timestamp: datetime


@dataclass
class ChangeImpact:
    """Change impact analysis result."""
    change_id: str
    change_type: ChangeType
    change_description: str
    impact_assessment: ImpactAssessment
    implementation_timeline: str
    cost_impact: float
    operational_disruption: float
    stakeholder_impact: Dict[str, Any]
    success_probability: float
    recommendations: List[str]
    timestamp: datetime


@dataclass
class OperationalImpact:
    """Operational impact analysis result."""
    operational_id: str
    process_impacts: Dict[str, float]
    system_impacts: Dict[str, float]
    resource_impacts: Dict[str, float]
    efficiency_impacts: Dict[str, float]
    quality_impacts: Dict[str, float]
    capacity_impacts: Dict[str, float]
    mitigation_measures: List[str]
    recovery_timeline: str
    timestamp: datetime


class ImpactAnalyzer:
    """Impact analysis engine."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        
    async def assess_impact(
        self,
        change_data: Dict[str, Any],
        current_state: Dict[str, Any],
        stakeholder_data: Dict[str, Any]
    ) -> ImpactAssessment:
        """Assess impact of changes or initiatives."""
        try:
            self.logger.info("Starting impact assessment")
            
            impact_id = f"impact_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Determine impact type
            impact_type = self._determine_impact_type(change_data)
            
            # Identify impact areas
            impact_areas = self._identify_impact_areas(change_data, current_state)
            
            # Calculate impact scores
            impact_scores = self._calculate_impact_scores(change_data, current_state, impact_areas)
            
            # Determine impact severity
            impact_severity = self._determine_impact_severity(impact_scores)
            
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
            
            result = ImpactAssessment(
                impact_id=impact_id,
                impact_type=impact_type,
                impact_severity=impact_severity,
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
            
            self.logger.info(f"Impact assessment completed: {impact_severity.value}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in impact assessment: {e}")
            raise
    
    async def analyze_change_impact(
        self,
        change_data: Dict[str, Any],
        current_state: Dict[str, Any],
        stakeholder_data: Dict[str, Any]
    ) -> ChangeImpact:
        """Analyze impact of specific changes."""
        try:
            self.logger.info("Starting change impact analysis")
            
            change_id = f"change_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Determine change type
            change_type = self._determine_change_type(change_data)
            
            # Generate change description
            change_description = self._generate_change_description(change_data, change_type)
            
            # Assess impact
            impact_assessment = await self.assess_impact(change_data, current_state, stakeholder_data)
            
            # Determine implementation timeline
            implementation_timeline = self._determine_implementation_timeline(change_data, impact_assessment)
            
            # Calculate cost impact
            cost_impact = self._calculate_cost_impact(change_data, impact_assessment)
            
            # Assess operational disruption
            operational_disruption = self._assess_operational_disruption(change_data, current_state)
            
            # Analyze stakeholder impact
            stakeholder_impact = self._analyze_stakeholder_impact(change_data, stakeholder_data)
            
            # Calculate success probability
            success_probability = self._calculate_success_probability(change_data, impact_assessment)
            
            # Generate recommendations
            recommendations = self._generate_change_recommendations(
                change_data, impact_assessment, success_probability
            )
            
            result = ChangeImpact(
                change_id=change_id,
                change_type=change_type,
                change_description=change_description,
                impact_assessment=impact_assessment,
                implementation_timeline=implementation_timeline,
                cost_impact=cost_impact,
                operational_disruption=operational_disruption,
                stakeholder_impact=stakeholder_impact,
                success_probability=success_probability,
                recommendations=recommendations,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Change impact analysis completed: {change_type.value}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in change impact analysis: {e}")
            raise
    
    async def analyze_operational_impact(
        self,
        operational_data: Dict[str, Any],
        current_operations: Dict[str, Any]
    ) -> OperationalImpact:
        """Analyze operational impact of changes."""
        try:
            self.logger.info("Starting operational impact analysis")
            
            operational_id = f"operational_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyze process impacts
            process_impacts = self._analyze_process_impacts(operational_data, current_operations)
            
            # Analyze system impacts
            system_impacts = self._analyze_system_impacts(operational_data, current_operations)
            
            # Analyze resource impacts
            resource_impacts = self._analyze_resource_impacts(operational_data, current_operations)
            
            # Analyze efficiency impacts
            efficiency_impacts = self._analyze_efficiency_impacts(operational_data, current_operations)
            
            # Analyze quality impacts
            quality_impacts = self._analyze_quality_impacts(operational_data, current_operations)
            
            # Analyze capacity impacts
            capacity_impacts = self._analyze_capacity_impacts(operational_data, current_operations)
            
            # Generate mitigation measures
            mitigation_measures = self._generate_operational_mitigation_measures(
                process_impacts, system_impacts, resource_impacts
            )
            
            # Determine recovery timeline
            recovery_timeline = self._determine_recovery_timeline(
                process_impacts, system_impacts, resource_impacts
            )
            
            result = OperationalImpact(
                operational_id=operational_id,
                process_impacts=process_impacts,
                system_impacts=system_impacts,
                resource_impacts=resource_impacts,
                efficiency_impacts=efficiency_impacts,
                quality_impacts=quality_impacts,
                capacity_impacts=capacity_impacts,
                mitigation_measures=mitigation_measures,
                recovery_timeline=recovery_timeline,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Operational impact analysis completed: {operational_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in operational impact analysis: {e}")
            raise
    
    def _determine_impact_type(self, change_data: Dict[str, Any]) -> ImpactType:
        """Determine the type of impact."""
        change_category = change_data.get('category', 'general')
        
        if change_category == 'strategic':
            return ImpactType.STRATEGIC
        elif change_category == 'operational':
            return ImpactType.OPERATIONAL
        elif change_category == 'financial':
            return ImpactType.FINANCIAL
        elif change_category == 'technology':
            return ImpactType.TECHNOLOGICAL
        elif change_category == 'organizational':
            return ImpactType.ORGANIZATIONAL
        elif change_category == 'environmental':
            return ImpactType.ENVIRONMENTAL
        elif change_category == 'social':
            return ImpactType.SOCIAL
        else:
            return ImpactType.OPERATIONAL
    
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
        elif change_type == 'organizational':
            impact_areas.extend(['structure', 'culture', 'capabilities', 'leadership'])
        elif change_type == 'environmental':
            impact_areas.extend(['sustainability', 'compliance', 'risk_management'])
        elif change_type == 'social':
            impact_areas.extend(['stakeholder_relations', 'reputation', 'community_impact'])
        
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
                'capabilities': 0.8,
                'structure': 0.7,
                'culture': 0.8,
                'leadership': 0.9,
                'sustainability': 0.6,
                'compliance': 0.7,
                'risk_management': 0.8,
                'stakeholder_relations': 0.7,
                'reputation': 0.8,
                'community_impact': 0.6
            }
            
            sensitivity = sensitivity_factors.get(area, 0.5)
            impact_scores[area] = base_score * sensitivity
        
        return impact_scores
    
    def _determine_impact_severity(self, impact_scores: Dict[str, float]) -> ImpactSeverity:
        """Determine overall impact severity."""
        if not impact_scores:
            return ImpactSeverity.NEGLIGIBLE
        
        # Calculate average impact score
        avg_score = sum(impact_scores.values()) / len(impact_scores)
        
        if avg_score < 0.2:
            return ImpactSeverity.NEGLIGIBLE
        elif avg_score < 0.4:
            return ImpactSeverity.LOW
        elif avg_score < 0.6:
            return ImpactSeverity.MODERATE
        elif avg_score < 0.8:
            return ImpactSeverity.HIGH
        else:
            return ImpactSeverity.CRITICAL
    
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
        elif change_type == 'organizational':
            affected_stakeholders.extend(['employees', 'managers', 'leadership'])
        elif change_type == 'environmental':
            affected_stakeholders.extend(['regulators', 'community', 'suppliers'])
        elif change_type == 'social':
            affected_stakeholders.extend(['community', 'customers', 'employees'])
        
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
        
        # Operational risks
        if change_data.get('operational_disruption', 0) > 0.6:
            risk_implications.append("Operational disruption risk")
        
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
            elif "operational disruption" in risk.lower():
                strategies.append("Implement parallel systems during transition")
                strategies.append("Develop rollback procedures")
        
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
            elif area == 'culture':
                success_metrics.append("Employee engagement improvement")
                success_metrics.append("Organizational culture alignment")
        
        # General success metrics
        success_metrics.extend([
            "Timeline adherence",
            "Budget compliance",
            "Stakeholder satisfaction",
            "Risk mitigation effectiveness"
        ])
        
        return success_metrics
    
    def _determine_change_type(self, change_data: Dict[str, Any]) -> ChangeType:
        """Determine the type of change."""
        change_magnitude = change_data.get('magnitude', 0.5)
        change_scope = change_data.get('scope', 'limited')
        
        if change_magnitude > 0.8 and change_scope == 'organization_wide':
            return ChangeType.TRANSFORMATIONAL
        elif change_magnitude > 0.6:
            return ChangeType.DISRUPTIVE
        elif change_magnitude > 0.3:
            return ChangeType.EVOLUTIONARY
        else:
            return ChangeType.INCREMENTAL
    
    def _generate_change_description(
        self, 
        change_data: Dict[str, Any], 
        change_type: ChangeType
    ) -> str:
        """Generate description of the change."""
        change_name = change_data.get('name', 'Unknown Change')
        change_category = change_data.get('category', 'general')
        
        descriptions = {
            ChangeType.TRANSFORMATIONAL: f"Transformational {change_category} change: {change_name}",
            ChangeType.DISRUPTIVE: f"Disruptive {change_category} change: {change_name}",
            ChangeType.EVOLUTIONARY: f"Evolutionary {change_category} change: {change_name}",
            ChangeType.INCREMENTAL: f"Incremental {change_category} change: {change_name}"
        }
        
        return descriptions.get(change_type, f"Change: {change_name}")
    
    def _determine_implementation_timeline(
        self, 
        change_data: Dict[str, Any], 
        impact_assessment: ImpactAssessment
    ) -> str:
        """Determine implementation timeline."""
        base_timeline = change_data.get('implementation_duration', '6 months')
        
        # Adjust based on impact severity
        severity_adjustments = {
            ImpactSeverity.NEGLIGIBLE: 0.5,
            ImpactSeverity.LOW: 0.75,
            ImpactSeverity.MODERATE: 1.0,
            ImpactSeverity.HIGH: 1.5,
            ImpactSeverity.CRITICAL: 2.0
        }
        
        adjustment_factor = severity_adjustments.get(impact_assessment.impact_severity, 1.0)
        
        # Simple timeline adjustment (in practice, more sophisticated logic would be used)
        if 'months' in base_timeline:
            months = int(base_timeline.split()[0])
            adjusted_months = int(months * adjustment_factor)
            return f"{adjusted_months} months"
        
        return base_timeline
    
    def _calculate_cost_impact(
        self, 
        change_data: Dict[str, Any], 
        impact_assessment: ImpactAssessment
    ) -> float:
        """Calculate cost impact of the change."""
        base_cost = change_data.get('estimated_cost', 0.0)
        
        # Adjust based on impact severity
        severity_multipliers = {
            ImpactSeverity.NEGLIGIBLE: 0.5,
            ImpactSeverity.LOW: 0.75,
            ImpactSeverity.MODERATE: 1.0,
            ImpactSeverity.HIGH: 1.5,
            ImpactSeverity.CRITICAL: 2.0
        }
        
        multiplier = severity_multipliers.get(impact_assessment.impact_severity, 1.0)
        
        return base_cost * multiplier
    
    def _assess_operational_disruption(
        self, 
        change_data: Dict[str, Any], 
        current_state: Dict[str, Any]
    ) -> float:
        """Assess operational disruption level."""
        disruption_factors = [
            change_data.get('process_changes', 0),
            change_data.get('system_changes', 0),
            change_data.get('organizational_changes', 0),
            change_data.get('timeline_pressure', 0)
        ]
        
        return sum(disruption_factors) / len(disruption_factors)
    
    def _analyze_stakeholder_impact(
        self, 
        change_data: Dict[str, Any], 
        stakeholder_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze impact on different stakeholder groups."""
        stakeholder_impact = {
            'employees': {
                'impact_level': change_data.get('employee_impact', 0.5),
                'concerns': ['job_security', 'workload', 'training_needs'],
                'benefits': ['career_growth', 'skill_development', 'efficiency_improvement']
            },
            'customers': {
                'impact_level': change_data.get('customer_impact', 0.3),
                'concerns': ['service_disruption', 'quality_changes', 'cost_impact'],
                'benefits': ['improved_service', 'better_quality', 'cost_reduction']
            },
            'management': {
                'impact_level': change_data.get('management_impact', 0.7),
                'concerns': ['implementation_complexity', 'resource_allocation', 'timeline_pressure'],
                'benefits': ['operational_improvement', 'strategic_advantage', 'efficiency_gains']
            }
        }
        
        return stakeholder_impact
    
    def _calculate_success_probability(
        self, 
        change_data: Dict[str, Any], 
        impact_assessment: ImpactAssessment
    ) -> float:
        """Calculate probability of successful implementation."""
        base_probability = 0.7  # Base success probability
        
        # Adjust based on various factors
        adjustments = []
        
        # Impact severity adjustment
        severity_adjustments = {
            ImpactSeverity.NEGLIGIBLE: 0.1,
            ImpactSeverity.LOW: 0.05,
            ImpactSeverity.MODERATE: 0.0,
            ImpactSeverity.HIGH: -0.1,
            ImpactSeverity.CRITICAL: -0.2
        }
        adjustments.append(severity_adjustments.get(impact_assessment.impact_severity, 0.0))
        
        # Resource availability adjustment
        if change_data.get('resource_availability', 'adequate') == 'limited':
            adjustments.append(-0.15)
        elif change_data.get('resource_availability', 'adequate') == 'abundant':
            adjustments.append(0.1)
        
        # Stakeholder support adjustment
        if change_data.get('stakeholder_support', 0.5) > 0.7:
            adjustments.append(0.1)
        elif change_data.get('stakeholder_support', 0.5) < 0.3:
            adjustments.append(-0.15)
        
        # Implementation complexity adjustment
        complexity = change_data.get('implementation_complexity', 0.5)
        if complexity > 0.8:
            adjustments.append(-0.2)
        elif complexity < 0.3:
            adjustments.append(0.1)
        
        # Calculate final probability
        final_probability = base_probability + sum(adjustments)
        return max(0.1, min(0.95, final_probability))
    
    def _generate_change_recommendations(
        self, 
        change_data: Dict[str, Any], 
        impact_assessment: ImpactAssessment, 
        success_probability: float
    ) -> List[str]:
        """Generate recommendations for change implementation."""
        recommendations = []
        
        # Success probability-based recommendations
        if success_probability < 0.5:
            recommendations.extend([
                "Conduct detailed risk assessment",
                "Develop comprehensive mitigation strategies",
                "Consider phased implementation approach",
                "Strengthen stakeholder engagement"
            ])
        elif success_probability < 0.7:
            recommendations.extend([
                "Implement robust change management",
                "Establish clear communication plan",
                "Monitor progress closely",
                "Prepare contingency plans"
            ])
        else:
            recommendations.extend([
                "Proceed with implementation",
                "Maintain stakeholder engagement",
                "Monitor key success factors",
                "Celebrate early wins"
            ])
        
        # Impact severity-based recommendations
        if impact_assessment.impact_severity in [ImpactSeverity.HIGH, ImpactSeverity.CRITICAL]:
            recommendations.extend([
                "Establish dedicated implementation team",
                "Allocate sufficient resources",
                "Implement regular progress reviews",
                "Develop rollback procedures"
            ])
        
        return recommendations
    
    def _analyze_process_impacts(
        self, 
        operational_data: Dict[str, Any], 
        current_operations: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze impacts on business processes."""
        process_impacts = {}
        
        processes = operational_data.get('processes', {})
        for process_name, process_data in processes.items():
            impact_score = process_data.get('impact_score', 0.5)
            process_impacts[process_name] = impact_score
        
        return process_impacts
    
    def _analyze_system_impacts(
        self, 
        operational_data: Dict[str, Any], 
        current_operations: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze impacts on systems."""
        system_impacts = {}
        
        systems = operational_data.get('systems', {})
        for system_name, system_data in systems.items():
            impact_score = system_data.get('impact_score', 0.5)
            system_impacts[system_name] = impact_score
        
        return system_impacts
    
    def _analyze_resource_impacts(
        self, 
        operational_data: Dict[str, Any], 
        current_operations: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze impacts on resources."""
        resource_impacts = {}
        
        resources = operational_data.get('resources', {})
        for resource_name, resource_data in resources.items():
            impact_score = resource_data.get('impact_score', 0.5)
            resource_impacts[resource_name] = impact_score
        
        return resource_impacts
    
    def _analyze_efficiency_impacts(
        self, 
        operational_data: Dict[str, Any], 
        current_operations: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze impacts on efficiency."""
        efficiency_impacts = {}
        
        efficiency_metrics = operational_data.get('efficiency_metrics', {})
        for metric_name, metric_data in efficiency_metrics.items():
            impact_score = metric_data.get('impact_score', 0.5)
            efficiency_impacts[metric_name] = impact_score
        
        return efficiency_impacts
    
    def _analyze_quality_impacts(
        self, 
        operational_data: Dict[str, Any], 
        current_operations: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze impacts on quality."""
        quality_impacts = {}
        
        quality_metrics = operational_data.get('quality_metrics', {})
        for metric_name, metric_data in quality_metrics.items():
            impact_score = metric_data.get('impact_score', 0.5)
            quality_impacts[metric_name] = impact_score
        
        return quality_impacts
    
    def _analyze_capacity_impacts(
        self, 
        operational_data: Dict[str, Any], 
        current_operations: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze impacts on capacity."""
        capacity_impacts = {}
        
        capacity_metrics = operational_data.get('capacity_metrics', {})
        for metric_name, metric_data in capacity_metrics.items():
            impact_score = metric_data.get('impact_score', 0.5)
            capacity_impacts[metric_name] = impact_score
        
        return capacity_impacts
    
    def _generate_operational_mitigation_measures(
        self,
        process_impacts: Dict[str, float],
        system_impacts: Dict[str, float],
        resource_impacts: Dict[str, float]
    ) -> List[str]:
        """Generate mitigation measures for operational impacts."""
        measures = []
        
        # Process impact mitigation
        high_impact_processes = [p for p, s in process_impacts.items() if s > 0.7]
        if high_impact_processes:
            measures.append(f"Develop detailed process maps for {', '.join(high_impact_processes)}")
            measures.append("Implement process monitoring and control mechanisms")
        
        # System impact mitigation
        high_impact_systems = [s for s, score in system_impacts.items() if score > 0.7]
        if high_impact_systems:
            measures.append(f"Implement parallel systems for {', '.join(high_impact_systems)}")
            measures.append("Develop system rollback procedures")
        
        # Resource impact mitigation
        high_impact_resources = [r for r, score in resource_impacts.items() if score > 0.7]
        if high_impact_resources:
            measures.append(f"Develop resource contingency plans for {', '.join(high_impact_resources)}")
            measures.append("Implement resource allocation optimization")
        
        return measures
    
    def _determine_recovery_timeline(
        self,
        process_impacts: Dict[str, float],
        system_impacts: Dict[str, float],
        resource_impacts: Dict[str, float]
    ) -> str:
        """Determine recovery timeline based on impacts."""
        max_impact = max(
            max(process_impacts.values()) if process_impacts else 0,
            max(system_impacts.values()) if system_impacts else 0,
            max(resource_impacts.values()) if resource_impacts else 0
        )
        
        if max_impact > 0.8:
            return "6-12 months"
        elif max_impact > 0.6:
            return "3-6 months"
        elif max_impact > 0.4:
            return "1-3 months"
        else:
            return "Immediate"
    
    async def generate_comprehensive_impact_analysis(
        self,
        change_data: Dict[str, Any],
        current_state: Dict[str, Any],
        stakeholder_data: Dict[str, Any],
        operational_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive impact analysis."""
        try:
            self.logger.info("Starting comprehensive impact analysis")
            
            # Assess general impact
            impact_assessment = await self.assess_impact(change_data, current_state, stakeholder_data)
            
            # Analyze change impact
            change_impact = await self.analyze_change_impact(change_data, current_state, stakeholder_data)
            
            # Analyze operational impact if data provided
            operational_impact = None
            if operational_data:
                operational_impact = await self.analyze_operational_impact(operational_data, current_state)
            
            # Compile comprehensive analysis
            analysis = {
                'impact_assessment': asdict(impact_assessment),
                'change_impact': asdict(change_impact),
                'operational_impact': asdict(operational_impact) if operational_impact else None,
                'summary': {
                    'impact_severity': impact_assessment.impact_severity.value,
                    'change_type': change_impact.change_type.value,
                    'success_probability': change_impact.success_probability,
                    'cost_impact': change_impact.cost_impact,
                    'operational_disruption': change_impact.operational_disruption,
                    'key_recommendations': change_impact.recommendations[:5]
                },
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("Comprehensive impact analysis completed")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in comprehensive impact analysis: {e}")
            raise
