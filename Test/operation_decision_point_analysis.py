"""
Operation Decision Point Analysis
Monte Carlo simulation for identifying critical decision points and 
assessing success probabilities
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
from datetime import datetime
import json
import logging
from dataclasses import dataclass
from enum import Enum
import networkx as nx
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Types of operational decisions"""
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    LOGISTICAL = "logistical"
    INTELLIGENCE = "intelligence"


class RiskLevel(Enum):
    """Risk levels for decision points"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DecisionPoint:
    """Represents a decision point in the operation timeline"""
    id: str
    name: str
    description: str
    decision_type: DecisionType
    timeline_position: float  # 0.0 to 1.0
    dependencies: List[str]
    success_probability: float
    failure_impact: float
    risk_level: RiskLevel
    resource_requirements: Dict[str, float]
    time_required: float
    alternatives: List[str]


@dataclass
class OperationTimeline:
    """Represents an operation timeline with decision points"""
    id: str
    name: str
    description: str
    duration_days: int
    decision_points: List[DecisionPoint]
    objectives: List[str]
    constraints: List[str]
    resources: Dict[str, float]


class DecisionPointAnalyzer:
    """Monte Carlo analysis for operation decision points"""
    
    def __init__(self, num_simulations: int = 10000):
        self.num_simulations = num_simulations
        self.results = {}
        self.critical_paths = []
        self.success_probabilities = {}
        
    def create_sample_operation(self) -> OperationTimeline:
        """Create a sample operation timeline for demonstration"""
        
        decision_points = [
            DecisionPoint(
                id="dp_001",
                name="Intelligence Gathering",
                description="Collect and analyze intelligence on target",
                decision_type=DecisionType.INTELLIGENCE,
                timeline_position=0.1,
                dependencies=[],
                success_probability=0.85,
                failure_impact=0.9,
                risk_level=RiskLevel.MEDIUM,
                resource_requirements={
                    "intelligence_assets": 0.3, 
                    "analysts": 0.4
                },
                time_required=2.0,
                alternatives=[
                    "satellite_intelligence", 
                    "human_intelligence", 
                    "technical_intelligence"
                ]
            ),
            DecisionPoint(
                id="dp_002",
                name="Target Selection",
                description="Select primary and secondary targets",
                decision_type=DecisionType.STRATEGIC,
                timeline_position=0.2,
                dependencies=["dp_001"],
                success_probability=0.75,
                failure_impact=0.8,
                risk_level=RiskLevel.HIGH,
                resource_requirements={
                    "command_team": 0.5, 
                    "intelligence_assets": 0.2
                },
                time_required=1.5,
                alternatives=["target_a", "target_b", "target_c"]
            ),
            DecisionPoint(
                id="dp_003",
                name="Resource Allocation",
                description="Allocate personnel and equipment",
                decision_type=DecisionType.LOGISTICAL,
                timeline_position=0.3,
                dependencies=["dp_002"],
                success_probability=0.9,
                failure_impact=0.6,
                risk_level=RiskLevel.LOW,
                resource_requirements={
                    "personnel": 0.8, 
                    "equipment": 0.7, 
                    "budget": 0.6
                },
                time_required=3.0,
                alternatives=[
                    "minimal_resources", 
                    "standard_resources", 
                    "maximum_resources"
                ]
            ),
            DecisionPoint(
                id="dp_004",
                name="Execution Planning",
                description="Develop detailed execution plan",
                decision_type=DecisionType.OPERATIONAL,
                timeline_position=0.5,
                dependencies=["dp_003"],
                success_probability=0.8,
                failure_impact=0.7,
                risk_level=RiskLevel.MEDIUM,
                resource_requirements={
                    "planners": 0.6, 
                    "intelligence_assets": 0.3
                },
                time_required=4.0,
                alternatives=["plan_a", "plan_b", "plan_c"]
            ),
            DecisionPoint(
                id="dp_005",
                name="Execution",
                description="Execute the operation",
                decision_type=DecisionType.TACTICAL,
                timeline_position=0.8,
                dependencies=["dp_004"],
                success_probability=0.7,
                failure_impact=1.0,
                risk_level=RiskLevel.CRITICAL,
                resource_requirements={
                    "operational_teams": 1.0, 
                    "equipment": 0.9, 
                    "support": 0.8
                },
                time_required=6.0,
                alternatives=[
                    "direct_assault", 
                    "stealth_approach", 
                    "deception_operation"
                ]
            ),
            DecisionPoint(
                id="dp_006",
                name="Extraction",
                description="Extract personnel and equipment",
                decision_type=DecisionType.TACTICAL,
                timeline_position=0.95,
                dependencies=["dp_005"],
                success_probability=0.85,
                failure_impact=0.8,
                risk_level=RiskLevel.HIGH,
                resource_requirements={
                    "extraction_teams": 0.7, 
                    "transport": 0.8
                },
                time_required=2.0,
                alternatives=[
                    "helicopter_extraction", 
                    "ground_extraction", 
                    "sea_extraction"
                ]
            )
        ]
        
        return OperationTimeline(
            id="op_001",
            name="Special Operations Mission",
            description="High-risk special operations mission with multiple decision points",
            duration_days=30,
            decision_points=decision_points,
            objectives=["Neutralize high-value target", "Secure intelligence", "Minimize collateral damage"],
            constraints=["Time sensitive", "Limited resources", "Political considerations"],
            resources={
                "personnel": 100, 
                "equipment": 50, 
                "budget": 1000000, 
                "intelligence_assets": 20,
                "analysts": 10,
                "command_team": 5,
                "planners": 8,
                "operational_teams": 15,
                "support": 20,
                "extraction_teams": 10,
                "transport": 5
            }
        )
    
    def run_monte_carlo_analysis(self, operation: OperationTimeline) -> Dict[str, Any]:
        """Run Monte Carlo simulation for decision point analysis"""
        
        logger.info(f"Starting Monte Carlo analysis with {self.num_simulations} simulations")
        
        # Initialize results storage
        simulation_results = []
        decision_outcomes = {dp.id: [] for dp in operation.decision_points}
        critical_path_analysis = []
        
        # Run simulations
        for sim in range(self.num_simulations):
            sim_result = self._run_single_simulation(operation)
            simulation_results.append(sim_result)
            
            # Track decision outcomes
            for dp_id, outcome in sim_result['decision_outcomes'].items():
                decision_outcomes[dp_id].append(outcome)
            
            # Track critical paths
            critical_path_analysis.append(sim_result['critical_path'])
        
        # Analyze results
        analysis_results = self._analyze_simulation_results(
            simulation_results, decision_outcomes, critical_path_analysis, operation
        )
        
        return analysis_results
    
    def _run_single_simulation(self, operation: OperationTimeline) -> Dict[str, Any]:
        """Run a single Monte Carlo simulation"""
        
        # Initialize simulation state
        current_time = 0.0
        available_resources = operation.resources.copy()
        decision_outcomes = {}
        critical_path = []
        operation_success = True
        
        # Sort decision points by timeline position
        sorted_dps = sorted(operation.decision_points, key=lambda x: x.timeline_position)
        
        for dp in sorted_dps:
            # Check dependencies
            if not self._check_dependencies(dp, decision_outcomes):
                decision_outcomes[dp.id] = False
                operation_success = False
                continue
            
            # Check resource availability
            if not self._check_resources(dp, available_resources):
                decision_outcomes[dp.id] = False
                operation_success = False
                continue
            
            # Simulate decision outcome
            success = np.random.random() < dp.success_probability
            
            # Apply resource consumption
            if success:
                self._consume_resources(dp, available_resources)
                critical_path.append(dp.id)
            
            decision_outcomes[dp.id] = success
            
            # Update time
            current_time += dp.time_required
            
            # Check if operation should continue
            if not success and dp.failure_impact > 0.8:
                operation_success = False
                break
        
        return {
            'simulation_id': len(self.results),
            'operation_success': operation_success,
            'decision_outcomes': decision_outcomes,
            'critical_path': critical_path,
            'total_time': current_time,
            'resources_consumed': {k: operation.resources[k] - v for k, v in available_resources.items()}
        }
    
    def _check_dependencies(self, dp: DecisionPoint, decision_outcomes: Dict[str, bool]) -> bool:
        """Check if all dependencies are satisfied"""
        for dep_id in dp.dependencies:
            if dep_id not in decision_outcomes or not decision_outcomes[dep_id]:
                return False
        return True
    
    def _check_resources(self, dp: DecisionPoint, available_resources: Dict[str, float]) -> bool:
        """Check if required resources are available"""
        for resource, required in dp.resource_requirements.items():
            if resource not in available_resources or available_resources[resource] < required:
                return False
        return True
    
    def _consume_resources(self, dp: DecisionPoint, available_resources: Dict[str, float]):
        """Consume resources for decision point"""
        for resource, required in dp.resource_requirements.items():
            available_resources[resource] -= required
    
    def _analyze_simulation_results(self, simulation_results: List[Dict], 
                                  decision_outcomes: Dict[str, List[bool]], 
                                  critical_path_analysis: List[List[str]],
                                  operation: OperationTimeline) -> Dict[str, Any]:
        """Analyze Monte Carlo simulation results"""
        
        # Calculate overall success rate
        total_successes = sum(1 for result in simulation_results if result['operation_success'])
        overall_success_rate = total_successes / len(simulation_results)
        
        # Calculate decision point success rates
        dp_success_rates = {}
        for dp_id, outcomes in decision_outcomes.items():
            dp_success_rates[dp_id] = sum(outcomes) / len(outcomes)
        
        # Identify critical decision points
        critical_dps = self._identify_critical_decision_points(dp_success_rates, operation)
        
        # Analyze critical paths
        critical_path_analysis = self._analyze_critical_paths(critical_path_analysis, operation)
        
        # Calculate risk metrics
        risk_metrics = self._calculate_risk_metrics(simulation_results, operation)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            dp_success_rates, critical_dps, risk_metrics, operation
        )
        
        return {
            'overall_success_rate': overall_success_rate,
            'decision_point_success_rates': dp_success_rates,
            'critical_decision_points': critical_dps,
            'critical_path_analysis': critical_path_analysis,
            'risk_metrics': risk_metrics,
            'recommendations': recommendations,
            'simulation_metadata': {
                'total_simulations': len(simulation_results),
                'successful_simulations': total_successes,
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
    def _identify_critical_decision_points(self, dp_success_rates: Dict[str, float], 
                                         operation: OperationTimeline) -> List[Dict[str, Any]]:
        """Identify critical decision points based on success rates and impact"""
        
        critical_dps = []
        
        for dp in operation.decision_points:
            success_rate = dp_success_rates.get(dp.id, 0.0)
            
            # Calculate criticality score
            criticality_score = (1 - success_rate) * dp.failure_impact
            
            if criticality_score > 0.3:  # Threshold for critical decision points
                critical_dps.append({
                    'decision_point': dp,
                    'success_rate': success_rate,
                    'criticality_score': criticality_score,
                    'risk_level': dp.risk_level.value,
                    'recommendations': self._generate_dp_recommendations(dp, success_rate)
                })
        
        # Sort by criticality score
        critical_dps.sort(key=lambda x: x['criticality_score'], reverse=True)
        
        return critical_dps
    
    def _analyze_critical_paths(self, critical_paths: List[List[str]], 
                              operation: OperationTimeline) -> Dict[str, Any]:
        """Analyze critical paths from simulations"""
        
        # Count path frequencies
        path_counts = {}
        for path in critical_paths:
            path_key = ' -> '.join(path)
            path_counts[path_key] = path_counts.get(path_key, 0) + 1
        
        # Find most common paths
        sorted_paths = sorted(path_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'most_common_paths': sorted_paths[:5],
            'path_frequency_distribution': path_counts,
            'total_unique_paths': len(path_counts)
        }
    
    def _calculate_risk_metrics(self, simulation_results: List[Dict], 
                              operation: OperationTimeline) -> Dict[str, Any]:
        """Calculate comprehensive risk metrics"""
        
        # Time-based risk
        successful_times = [r['total_time'] for r in simulation_results if r['operation_success']]
        failed_times = [r['total_time'] for r in simulation_results if not r['operation_success']]
        
        time_risk = {
            'successful_operations_avg_time': np.mean(successful_times) if successful_times else 0,
            'failed_operations_avg_time': np.mean(failed_times) if failed_times else 0,
            'time_variance': np.var(successful_times) if successful_times else 0
        }
        
        # Resource risk
        resource_consumption = {}
        for resource in operation.resources.keys():
            consumptions = [r['resources_consumed'].get(resource, 0) for r in simulation_results]
            resource_consumption[resource] = {
                'average_consumption': np.mean(consumptions),
                'max_consumption': np.max(consumptions),
                'consumption_variance': np.var(consumptions)
            }
        
        return {
            'time_risk': time_risk,
            'resource_risk': resource_consumption,
            'overall_risk_score': self._calculate_overall_risk_score(simulation_results, operation)
        }
    
    def _calculate_overall_risk_score(self, simulation_results: List[Dict], 
                                    operation: OperationTimeline) -> float:
        """Calculate overall risk score for the operation"""
        
        success_rate = sum(1 for r in simulation_results if r['operation_success']) / len(simulation_results)
        
        # Calculate average failure impact
        failure_impacts = []
        for result in simulation_results:
            if not result['operation_success']:
                impact = 0
                for dp_id, outcome in result['decision_outcomes'].items():
                    if not outcome:
                        dp = next(dp for dp in operation.decision_points if dp.id == dp_id)
                        impact += dp.failure_impact
                failure_impacts.append(impact)
        
        avg_failure_impact = np.mean(failure_impacts) if failure_impacts else 0
        
        # Risk score combines success rate and failure impact
        risk_score = (1 - success_rate) * avg_failure_impact
        
        return risk_score
    
    def _generate_dp_recommendations(self, dp: DecisionPoint, success_rate: float) -> List[str]:
        """Generate recommendations for a specific decision point"""
        
        recommendations = []
        
        if success_rate < 0.7:
            recommendations.append(f"Improve success probability for {dp.name} through additional planning")
        
        if dp.failure_impact > 0.8:
            recommendations.append(f"Develop contingency plans for {dp.name} failure")
        
        if dp.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append(f"Allocate additional resources to {dp.name}")
        
        if len(dp.alternatives) > 1:
            recommendations.append(f"Evaluate alternative approaches for {dp.name}")
        
        return recommendations
    
    def _generate_recommendations(self, dp_success_rates: Dict[str, float], 
                                critical_dps: List[Dict], 
                                risk_metrics: Dict[str, Any],
                                operation: OperationTimeline) -> List[str]:
        """Generate overall operation recommendations"""
        
        recommendations = []
        
        # Overall success rate recommendations
        overall_success_rate = sum(dp_success_rates.values()) / len(dp_success_rates)
        if overall_success_rate < 0.75:
            recommendations.append("Consider postponing operation until success probability improves")
        
        # Critical decision point recommendations
        if critical_dps:
            recommendations.append(f"Focus resources on {len(critical_dps)} critical decision points")
            for dp_info in critical_dps[:3]:  # Top 3 critical points
                dp = dp_info['decision_point']
                recommendations.append(f"Prioritize {dp.name} (success rate: {dp_info['success_rate']:.2%})")
        
        # Resource recommendations
        for resource, risk_info in risk_metrics['resource_risk'].items():
            if risk_info['average_consumption'] > operation.resources[resource] * 0.8:
                recommendations.append(f"Increase {resource} allocation to reduce risk")
        
        # Time recommendations
        time_risk = risk_metrics['time_risk']
        if time_risk['successful_operations_avg_time'] > operation.duration_days * 0.8:
            recommendations.append("Consider extending operation timeline or reducing scope")
        
        return recommendations
    
    def create_visualizations(self, analysis_results: Dict[str, Any], 
                            operation: OperationTimeline) -> Dict[str, str]:
        """Create visualizations for the analysis results"""
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Create output directory
        output_dir = Path("Results")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"operation_decision_analysis_{timestamp}"
        
        # 1. Decision Point Success Rates
        fig, ax = plt.subplots(figsize=(12, 8))
        dps = list(analysis_results['decision_point_success_rates'].keys())
        success_rates = list(analysis_results['decision_point_success_rates'].values())
        
        colors = ['red' if rate < 0.7 else 'orange' if rate < 0.8 else 'green' for rate in success_rates]
        
        bars = ax.bar(range(len(dps)), success_rates, color=colors, alpha=0.7)
        ax.set_xlabel('Decision Points')
        ax.set_ylabel('Success Rate')
        ax.set_title('Decision Point Success Rates')
        ax.set_xticks(range(len(dps)))
        ax.set_xticklabels([dp.replace('dp_', 'DP ') for dp in dps], rotation=45)
        ax.axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='Target Success Rate')
        ax.legend()
        
        # Add value labels on bars
        for bar, rate in zip(bars, success_rates):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                   f'{rate:.2%}', ha='center', va='bottom')
        
        plt.tight_layout()
        success_rates_path = output_dir / f"{base_filename}_success_rates.png"
        plt.savefig(success_rates_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Critical Decision Points
        if analysis_results['critical_decision_points']:
            fig, ax = plt.subplots(figsize=(10, 6))
            critical_dps = analysis_results['critical_decision_points']
            names = [dp['decision_point'].name for dp in critical_dps]
            criticality_scores = [dp['criticality_score'] for dp in critical_dps]
            
            bars = ax.barh(range(len(names)), criticality_scores, color='red', alpha=0.7)
            ax.set_xlabel('Criticality Score')
            ax.set_title('Critical Decision Points')
            ax.set_yticks(range(len(names)))
            ax.set_yticklabels(names)
            
            # Add value labels
            for bar, score in zip(bars, criticality_scores):
                ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                       f'{score:.3f}', ha='left', va='center')
            
            plt.tight_layout()
            critical_dps_path = output_dir / f"{base_filename}_critical_decision_points.png"
            plt.savefig(critical_dps_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        # 3. Decision Tree Visualization
        self._create_decision_tree_visualization(operation, analysis_results, output_dir, base_filename)
        
        return {
            'success_rates_chart': str(success_rates_path),
            'critical_decision_points_chart': str(critical_dps_path) if analysis_results['critical_decision_points'] else None,
            'decision_tree': str(output_dir / f"{base_filename}_decision_tree.png")
        }
    
    def _create_decision_tree_visualization(self, operation: OperationTimeline, 
                                          analysis_results: Dict[str, Any],
                                          output_dir: Path, base_filename: str):
        """Create decision tree visualization"""
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes
        for dp in operation.decision_points:
            success_rate = analysis_results['decision_point_success_rates'].get(dp.id, 0.0)
            color = 'red' if success_rate < 0.7 else 'orange' if success_rate < 0.8 else 'green'
            
            G.add_node(dp.id, 
                      name=dp.name,
                      success_rate=success_rate,
                      color=color,
                      pos=dp.timeline_position)
        
        # Add edges based on dependencies
        for dp in operation.decision_points:
            for dep_id in dp.dependencies:
                G.add_edge(dep_id, dp.id)
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(15, 10))
        
        # Position nodes based on timeline
        pos = {dp.id: (dp.timeline_position, np.random.uniform(0, 1)) 
               for dp in operation.decision_points}
        
        # Draw nodes
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        node_sizes = [G.nodes[node]['success_rate'] * 1000 + 500 for node in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.7)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
        
        # Add labels
        labels = {node: f"{G.nodes[node]['name']}\n{G.nodes[node]['success_rate']:.2%}" 
                 for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        ax.set_title('Operation Decision Tree with Success Rates')
        ax.set_xlabel('Timeline Position')
        ax.set_ylabel('Random Position')
        plt.tight_layout()
        
        decision_tree_path = output_dir / f"{base_filename}_decision_tree.png"
        plt.savefig(decision_tree_path, dpi=300, bbox_inches='tight')
        plt.close()

def main():
    """Main function to run the decision point analysis"""
    
    print("Operation Decision Point Analysis")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = DecisionPointAnalyzer(num_simulations=10000)
    
    # Create sample operation
    operation = analyzer.create_sample_operation()
    
    print(f"Operation: {operation.name}")
    print(f"Duration: {operation.duration_days} days")
    print(f"Decision Points: {len(operation.decision_points)}")
    print(f"Simulations: {analyzer.num_simulations}")
    print()
    
    # Run Monte Carlo analysis
    print("Running Monte Carlo analysis...")
    analysis_results = analyzer.run_monte_carlo_analysis(operation)
    
    # Display results
    print("\nAnalysis Results:")
    print("-" * 30)
    print(f"Overall Success Rate: {analysis_results['overall_success_rate']:.2%}")
    print(f"Critical Decision Points: {len(analysis_results['critical_decision_points'])}")
    print()
    
    print("Decision Point Success Rates:")
    for dp_id, rate in analysis_results['decision_point_success_rates'].items():
        dp = next(dp for dp in operation.decision_points if dp.id == dp_id)
        print(f"  {dp.name}: {rate:.2%}")
    
    print("\nCritical Decision Points:")
    for dp_info in analysis_results['critical_decision_points']:
        dp = dp_info['decision_point']
        print(f"  {dp.name}: Criticality Score = {dp_info['criticality_score']:.3f}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(analysis_results['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    # Create visualizations
    print("\nCreating visualizations...")
    viz_paths = analyzer.create_visualizations(analysis_results, operation)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = f"Results/operation_decision_analysis_{timestamp}.json"
    
    # Convert to serializable format
    serializable_results = {
        'overall_success_rate': float(analysis_results['overall_success_rate']),
        'decision_point_success_rates': {
            k: float(v) for k, v in analysis_results['decision_point_success_rates'].items()
        },
        'critical_decision_points': [
            {
                'decision_point_id': dp_info['decision_point'].id,
                'decision_point_name': dp_info['decision_point'].name,
                'success_rate': float(dp_info['success_rate']),
                'criticality_score': float(dp_info['criticality_score']),
                'risk_level': dp_info['risk_level'],
                'recommendations': dp_info['recommendations']
            }
            for dp_info in analysis_results['critical_decision_points']
        ],
        'critical_path_analysis': analysis_results['critical_path_analysis'],
        'risk_metrics': {
            'time_risk': {
                'successful_operations_avg_time': float(analysis_results['risk_metrics']['time_risk']['successful_operations_avg_time']),
                'failed_operations_avg_time': float(analysis_results['risk_metrics']['time_risk']['failed_operations_avg_time']),
                'time_variance': float(analysis_results['risk_metrics']['time_risk']['time_variance'])
            },
            'resource_risk': {
                resource: {
                    'average_consumption': float(info['average_consumption']),
                    'max_consumption': float(info['max_consumption']),
                    'consumption_variance': float(info['consumption_variance'])
                }
                for resource, info in analysis_results['risk_metrics']['resource_risk'].items()
            },
            'overall_risk_score': float(analysis_results['risk_metrics']['overall_risk_score'])
        },
        'recommendations': analysis_results['recommendations'],
        'simulation_metadata': analysis_results['simulation_metadata'],
        'visualization_paths': viz_paths
    }
    
    with open(results_path, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\nResults saved to: {results_path}")
    print(f"Visualizations saved to: Results/")
    
    return analysis_results, viz_paths

if __name__ == "__main__":
    main()
