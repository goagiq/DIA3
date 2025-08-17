#!/usr/bin/env python3
"""
Pacific Conflict Force Structure Optimization using Monte Carlo Simulation

This script uses Monte Carlo simulation to optimize force structure for Pacific Conflict
with China and assess the probability of success for different force compositions.

Author: DIA3 System
Date: 2025-08-17
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

class PacificConflictForceOptimizer:
    """
    Monte Carlo simulation system for Pacific Conflict force structure optimization.
    """
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"Results/pacific_conflict_force_optimization_{self.timestamp}"
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Force composition definitions
        self.force_compositions = {
            "carrier_strike_group": {
                "aircraft_carrier": 1,
                "guided_missile_cruiser": 2,
                "guided_missile_destroyer": 4,
                "attack_submarine": 2,
                "supply_ship": 1,
                "air_wing": 1
            },
            "amphibious_ready_group": {
                "amphibious_assault_ship": 1,
                "amphibious_transport_dock": 1,
                "dock_landing_ship": 1,
                "guided_missile_destroyer": 2,
                "attack_submarine": 1,
                "marine_expeditionary_unit": 1
            },
            "surface_action_group": {
                "guided_missile_cruiser": 1,
                "guided_missile_destroyer": 3,
                "frigate": 2,
                "attack_submarine": 1
            },
            "submarine_strike_group": {
                "ballistic_missile_submarine": 2,
                "attack_submarine": 4,
                "guided_missile_destroyer": 2
            },
            "air_combat_element": {
                "fighter_squadron": 4,
                "bomber_squadron": 2,
                "electronic_warfare_squadron": 1,
                "air_refueling_squadron": 1,
                "early_warning_squadron": 1
            }
        }
        
        # Platform capabilities and effectiveness
        self.platform_effectiveness = {
            "aircraft_carrier": {
                "air_power": 0.95,
                "sea_control": 0.90,
                "power_projection": 0.98,
                "survivability": 0.85,
                "cost_factor": 10.0
            },
            "guided_missile_cruiser": {
                "air_defense": 0.92,
                "surface_warfare": 0.88,
                "anti_submarine": 0.75,
                "survivability": 0.80,
                "cost_factor": 3.0
            },
            "guided_missile_destroyer": {
                "air_defense": 0.85,
                "surface_warfare": 0.82,
                "anti_submarine": 0.78,
                "survivability": 0.75,
                "cost_factor": 2.0
            },
            "attack_submarine": {
                "anti_surface": 0.90,
                "anti_submarine": 0.95,
                "intelligence": 0.85,
                "survivability": 0.88,
                "cost_factor": 2.5
            },
            "ballistic_missile_submarine": {
                "strategic_deterrence": 0.98,
                "survivability": 0.95,
                "cost_factor": 8.0
            },
            "fighter_squadron": {
                "air_superiority": 0.88,
                "ground_attack": 0.82,
                "survivability": 0.75,
                "cost_factor": 1.5
            },
            "bomber_squadron": {
                "strategic_strike": 0.92,
                "maritime_strike": 0.85,
                "survivability": 0.70,
                "cost_factor": 2.0
            }
        }
        
        # Scenario parameters
        self.scenarios = {
            "south_china_sea_conflict": {
                "distance": 1200,  # nautical miles
                "threat_level": "high",
                "duration": 30,  # days
                "environmental_factors": 0.85
            },
            "taiwan_strait_crisis": {
                "distance": 800,
                "threat_level": "very_high",
                "duration": 45,
                "environmental_factors": 0.90
            },
            "east_china_sea_dispute": {
                "distance": 600,
                "threat_level": "medium",
                "duration": 20,
                "environmental_factors": 0.88
            },
            "pacific_island_chain_defense": {
                "distance": 2000,
                "threat_level": "medium",
                "duration": 60,
                "environmental_factors": 0.80
            }
        }
        
        # Adversary capabilities (China)
        self.adversary_capabilities = {
            "anti_access_area_denial": {
                "missile_range": 1500,  # km
                "effectiveness": 0.85,
                "quantity": 1200
            },
            "air_force": {
                "fighter_aircraft": 1200,
                "effectiveness": 0.75,
                "modern_aircraft_ratio": 0.60
            },
            "navy": {
                "destroyers": 35,
                "frigates": 50,
                "submarines": 70,
                "aircraft_carriers": 2,
                "effectiveness": 0.70
            },
            "cyber_capabilities": {
                "cyber_attack": 0.80,
                "cyber_defense": 0.75,
                "electronic_warfare": 0.85
            }
        }

    def run_monte_carlo_simulation(self, n_simulations: int = 10000) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for force structure optimization.
        """
        print(f"Running Monte Carlo simulation with {n_simulations:,} iterations...")
        
        results = {
            "simulation_parameters": {
                "n_simulations": n_simulations,
                "timestamp": self.timestamp,
                "scenarios": list(self.scenarios.keys()),
                "force_compositions": list(self.force_compositions.keys())
            },
            "scenario_results": {},
            "force_composition_analysis": {},
            "optimization_recommendations": {}
        }
        
        # Run simulations for each scenario
        for scenario_name, scenario_params in self.scenarios.items():
            print(f"\nAnalyzing scenario: {scenario_name}")
            scenario_results = self._analyze_scenario(scenario_name, scenario_params, n_simulations)
            results["scenario_results"][scenario_name] = scenario_results
        
        # Analyze force composition effectiveness
        results["force_composition_analysis"] = self._analyze_force_compositions(n_simulations)
        
        # Generate optimization recommendations
        results["optimization_recommendations"] = self._generate_recommendations(results)
        
        return results

    def _analyze_scenario(self, scenario_name: str, scenario_params: Dict, n_simulations: int) -> Dict[str, Any]:
        """
        Analyze a specific scenario with Monte Carlo simulation.
        """
        scenario_results = {
            "scenario_parameters": scenario_params,
            "force_composition_performance": {},
            "success_probabilities": {},
            "risk_assessment": {},
            "resource_requirements": {}
        }
        
        for composition_name, composition in self.force_compositions.items():
            print(f"  Testing force composition: {composition_name}")
            
            # Run Monte Carlo simulations for this force composition
            success_count = 0
            casualty_rates = []
            mission_duration = []
            resource_consumption = []
            
            for _ in range(n_simulations):
                # Simulate mission execution
                mission_success, casualties, duration, resources = self._simulate_mission(
                    composition, scenario_params
                )
                
                if mission_success:
                    success_count += 1
                
                casualty_rates.append(casualties)
                mission_duration.append(duration)
                resource_consumption.append(resources)
            
            # Calculate statistics
            success_probability = success_count / n_simulations
            avg_casualty_rate = np.mean(casualty_rates)
            avg_duration = np.mean(mission_duration)
            avg_resources = np.mean(resource_consumption)
            
            scenario_results["force_composition_performance"][composition_name] = {
                "success_probability": success_probability,
                "avg_casualty_rate": avg_casualty_rate,
                "avg_mission_duration": avg_duration,
                "avg_resource_consumption": avg_resources,
                "casualty_distribution": {
                    "mean": np.mean(casualty_rates),
                    "std": np.std(casualty_rates),
                    "min": np.min(casualty_rates),
                    "max": np.max(casualty_rates),
                    "percentiles": {
                        "25": np.percentile(casualty_rates, 25),
                        "50": np.percentile(casualty_rates, 50),
                        "75": np.percentile(casualty_rates, 75),
                        "95": np.percentile(casualty_rates, 95)
                    }
                }
            }
        
        # Calculate overall success probabilities
        scenario_results["success_probabilities"] = {
            comp: data["success_probability"] 
            for comp, data in scenario_results["force_composition_performance"].items()
        }
        
        # Risk assessment
        scenario_results["risk_assessment"] = self._assess_risk(scenario_results["force_composition_performance"])
        
        return scenario_results

    def _simulate_mission(self, force_composition: Dict, scenario_params: Dict) -> Tuple[bool, float, float, float]:
        """
        Simulate a single mission execution with given force composition and scenario.
        """
        # Initialize mission parameters
        distance = scenario_params["distance"]
        threat_level = scenario_params["threat_level"]
        environmental_factors = scenario_params["environmental_factors"]
        
        # Calculate force effectiveness
        total_effectiveness = 0
        total_cost = 0
        
        for platform, quantity in force_composition.items():
            if platform in self.platform_effectiveness:
                effectiveness = self.platform_effectiveness[platform]
                cost = effectiveness.get("cost_factor", 1.0)
                
                # Calculate platform contribution
                platform_contribution = 0
                for capability, value in effectiveness.items():
                    if capability != "cost_factor":
                        # Apply environmental and distance factors
                        distance_factor = max(0.5, 1 - (distance / 3000))
                        environmental_factor = environmental_factors
                        
                        adjusted_value = value * distance_factor * environmental_factor
                        platform_contribution += adjusted_value
                
                total_effectiveness += platform_contribution * quantity
                total_cost += cost * quantity
        
        # Adversary threat assessment
        adversary_threat = self._calculate_adversary_threat(threat_level, distance)
        
        # Mission success determination
        success_threshold = 0.7  # Base success threshold
        if threat_level == "very_high":
            success_threshold = 0.8
        elif threat_level == "high":
            success_threshold = 0.75
        
        # Add randomness to simulation
        effectiveness_variation = np.random.normal(1.0, 0.1)  # 10% standard deviation
        threat_variation = np.random.normal(1.0, 0.15)  # 15% standard deviation
        
        adjusted_effectiveness = total_effectiveness * effectiveness_variation
        adjusted_threat = adversary_threat * threat_variation
        
        mission_success = adjusted_effectiveness > (adjusted_threat * success_threshold)
        
        # Calculate casualties (inverse relationship with effectiveness)
        casualty_rate = max(0.05, min(0.95, 1 - (adjusted_effectiveness / adjusted_threat)))
        
        # Mission duration (affected by distance and effectiveness)
        base_duration = scenario_params["duration"]
        duration_factor = 1 + (distance / 1000) * 0.5
        effectiveness_duration_factor = max(0.8, min(1.2, adjusted_effectiveness / adjusted_threat))
        mission_duration = base_duration * duration_factor * effectiveness_duration_factor
        
        # Resource consumption
        resource_consumption = total_cost * (1 + casualty_rate) * (mission_duration / 30)
        
        return mission_success, casualty_rate, mission_duration, resource_consumption

    def _calculate_adversary_threat(self, threat_level: str, distance: float) -> float:
        """
        Calculate adversary threat level based on capabilities and distance.
        """
        base_threat = {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.7,
            "very_high": 0.9
        }.get(threat_level, 0.5)
        
        # Distance factor (threat decreases with distance)
        distance_factor = max(0.5, 1 - (distance / 3000))
        
        # Adversary capability factors
        a2ad_capability = self.adversary_capabilities["anti_access_area_denial"]["effectiveness"]
        air_capability = self.adversary_capabilities["air_force"]["effectiveness"]
        naval_capability = self.adversary_capabilities["navy"]["effectiveness"]
        cyber_capability = self.adversary_capabilities["cyber_capabilities"]["cyber_attack"]
        
        # Combined threat calculation
        combined_threat = base_threat * distance_factor * (
            0.4 * a2ad_capability +
            0.3 * air_capability +
            0.2 * naval_capability +
            0.1 * cyber_capability
        )
        
        return combined_threat

    def _analyze_force_compositions(self, n_simulations: int) -> Dict[str, Any]:
        """
        Analyze overall effectiveness of different force compositions.
        """
        composition_analysis = {}
        
        for composition_name, composition in self.force_compositions.items():
            print(f"Analyzing force composition: {composition_name}")
            
            # Calculate composition metrics
            total_platforms = sum(composition.values())
            total_cost = sum(
                self.platform_effectiveness.get(platform, {}).get("cost_factor", 1.0) * quantity
                for platform, quantity in composition.items()
            )
            
            # Capability analysis
            capabilities = {
                "air_power": 0,
                "sea_control": 0,
                "anti_submarine": 0,
                "strategic_strike": 0,
                "survivability": 0
            }
            
            for platform, quantity in composition.items():
                if platform in self.platform_effectiveness:
                    effectiveness = self.platform_effectiveness[platform]
                    for capability, value in effectiveness.items():
                        if capability != "cost_factor" and capability in capabilities:
                            capabilities[capability] += value * quantity
            
            composition_analysis[composition_name] = {
                "total_platforms": total_platforms,
                "total_cost": total_cost,
                "capabilities": capabilities,
                "cost_efficiency": sum(capabilities.values()) / total_cost if total_cost > 0 else 0
            }
        
        return composition_analysis

    def _assess_risk(self, performance_data: Dict) -> Dict[str, Any]:
        """
        Assess risk for different force compositions.
        """
        risk_assessment = {}
        
        for composition, data in performance_data.items():
            success_prob = data["success_probability"]
            casualty_rate = data["avg_casualty_rate"]
            
            # Risk scoring (lower is better)
            risk_score = (1 - success_prob) * 0.6 + casualty_rate * 0.4
            
            risk_level = "low"
            if risk_score > 0.6:
                risk_level = "high"
            elif risk_score > 0.3:
                risk_level = "medium"
            
            risk_assessment[composition] = {
                "risk_score": risk_score,
                "risk_level": risk_level,
                "success_probability": success_prob,
                "casualty_risk": casualty_rate
            }
        
        return risk_assessment

    def _generate_recommendations(self, results: Dict) -> Dict[str, Any]:
        """
        Generate optimization recommendations based on simulation results.
        """
        recommendations = {
            "optimal_force_compositions": {},
            "scenario_specific_recommendations": {},
            "resource_allocation": {},
            "risk_mitigation": {}
        }
        
        # Find optimal force composition for each scenario
        for scenario_name, scenario_data in results["scenario_results"].items():
            best_composition = max(
                scenario_data["success_probabilities"].items(),
                key=lambda x: x[1]
            )
            
            recommendations["optimal_force_compositions"][scenario_name] = {
                "composition": best_composition[0],
                "success_probability": best_composition[1],
                "risk_level": scenario_data["risk_assessment"][best_composition[0]]["risk_level"]
            }
        
        # Overall best composition
        overall_success_rates = {}
        for composition in self.force_compositions.keys():
            avg_success = np.mean([
                results["scenario_results"][scenario]["success_probabilities"].get(composition, 0)
                for scenario in self.scenarios.keys()
            ])
            overall_success_rates[composition] = avg_success
        
        best_overall = max(overall_success_rates.items(), key=lambda x: x[1])
        recommendations["overall_best_composition"] = {
            "composition": best_overall[0],
            "avg_success_rate": best_overall[1]
        }
        
        # Resource allocation recommendations
        composition_costs = results["force_composition_analysis"]
        cost_effectiveness = {
            comp: data["cost_efficiency"] 
            for comp, data in composition_costs.items()
        }
        
        recommendations["resource_allocation"] = {
            "most_cost_effective": max(cost_effectiveness.items(), key=lambda x: x[1]),
            "cost_effectiveness_ranking": sorted(cost_effectiveness.items(), key=lambda x: x[1], reverse=True)
        }
        
        return recommendations

    def generate_visualizations(self, results: Dict) -> None:
        """
        Generate comprehensive visualizations of simulation results.
        """
        print("\nGenerating visualizations...")
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Success Probability Comparison
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Pacific Conflict Force Structure Optimization - Success Probabilities', fontsize=16, fontweight='bold')
        
        for idx, (scenario_name, scenario_data) in enumerate(results["scenario_results"].items()):
            ax = axes[idx // 2, idx % 2]
            
            compositions = list(scenario_data["success_probabilities"].keys())
            probabilities = list(scenario_data["success_probabilities"].values())
            
            bars = ax.bar(compositions, probabilities, alpha=0.8)
            ax.set_title(f'{scenario_name.replace("_", " ").title()}', fontweight='bold')
            ax.set_ylabel('Success Probability')
            ax.set_ylim(0, 1)
            
            # Add value labels on bars
            for bar, prob in zip(bars, probabilities):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{prob:.3f}', ha='center', va='bottom', fontweight='bold')
            
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/success_probabilities_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Risk Assessment Heatmap
        fig, ax = plt.subplots(figsize=(12, 8))
        
        risk_data = []
        scenarios = []
        compositions = []
        
        for scenario_name, scenario_data in results["scenario_results"].items():
            for composition, risk_data_point in scenario_data["risk_assessment"].items():
                risk_data.append(risk_data_point["risk_score"])
                scenarios.append(scenario_name.replace("_", " ").title())
                compositions.append(composition.replace("_", " ").title())
        
        # Create pivot table for heatmap
        df_risk = pd.DataFrame({
            'Scenario': scenarios,
            'Force Composition': compositions,
            'Risk Score': risk_data
        })
        
        risk_pivot = df_risk.pivot(index='Force Composition', columns='Scenario', values='Risk Score')
        
        sns.heatmap(risk_pivot, annot=True, cmap='RdYlGn_r', fmt='.3f', ax=ax)
        ax.set_title('Risk Assessment Heatmap - Lower Values Indicate Lower Risk', fontweight='bold')
        ax.set_xlabel('Scenario')
        ax.set_ylabel('Force Composition')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/risk_assessment_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Cost-Effectiveness Analysis
        fig, ax = plt.subplots(figsize=(12, 8))
        
        compositions = list(results["force_composition_analysis"].keys())
        costs = [data["total_cost"] for data in results["force_composition_analysis"].values()]
        efficiencies = [data["cost_efficiency"] for data in results["force_composition_analysis"].values()]
        
        scatter = ax.scatter(costs, efficiencies, s=200, alpha=0.7, c=range(len(compositions)), cmap='viridis')
        
        # Add labels
        for i, composition in enumerate(compositions):
            ax.annotate(composition.replace("_", " ").title(), 
                       (costs[i], efficiencies[i]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=10)
        
        ax.set_xlabel('Total Cost')
        ax.set_ylabel('Cost Efficiency (Capabilities/Cost)')
        ax.set_title('Cost-Effectiveness Analysis of Force Compositions', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/cost_effectiveness_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Capability Radar Chart
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Select top 3 compositions for radar chart
        top_compositions = sorted(
            results["force_composition_analysis"].items(),
            key=lambda x: x[1]["cost_efficiency"],
            reverse=True
        )[:3]
        
        capabilities = ["air_power", "sea_control", "anti_submarine", "strategic_strike", "survivability"]
        angles = np.linspace(0, 2 * np.pi, len(capabilities), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for i, (composition_name, composition_data) in enumerate(top_compositions):
            values = [composition_data["capabilities"].get(cap, 0) for cap in capabilities]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=composition_name.replace("_", " ").title(), alpha=0.7)
            ax.fill(angles, values, alpha=0.1)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([cap.replace("_", " ").title() for cap in capabilities])
        ax.set_ylim(0, max([max(comp[1]["capabilities"].values()) for comp in top_compositions]))
        ax.set_title('Capability Comparison - Top 3 Force Compositions', fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/capability_radar_chart.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualizations saved to: {self.results_dir}")

    def save_results(self, results: Dict) -> None:
        """
        Save simulation results to files.
        """
        print(f"\nSaving results to: {self.results_dir}")
        
        # Save JSON results
        with open(f'{self.results_dir}/pacific_conflict_force_optimization_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Generate markdown report
        self._generate_markdown_report(results)
        
        print("Results saved successfully!")

    def _generate_markdown_report(self, results: Dict) -> None:
        """
        Generate comprehensive markdown report.
        """
        report_path = f'{self.results_dir}/pacific_conflict_force_optimization_report.md'
        
        with open(report_path, 'w') as f:
            f.write("# Pacific Conflict Force Structure Optimization Analysis\n\n")
            f.write(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Simulation Iterations**: {results['simulation_parameters']['n_simulations']:,}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write("This analysis uses Monte Carlo simulation to optimize force structure for Pacific Conflict scenarios with China. ")
            f.write("The simulation evaluates different force compositions across multiple scenarios to identify optimal configurations ")
            f.write("and assess success probabilities.\n\n")
            
            # Overall best composition
            best_overall = results["optimization_recommendations"]["overall_best_composition"]
            f.write(f"### Overall Best Force Composition\n")
            f.write(f"- **Recommended Composition**: {best_overall['composition'].replace('_', ' ').title()}\n")
            f.write(f"- **Average Success Rate**: {best_overall['avg_success_rate']:.3f} ({best_overall['avg_success_rate']*100:.1f}%)\n\n")
            
            # Scenario-specific recommendations
            f.write("### Scenario-Specific Recommendations\n\n")
            for scenario, rec in results["optimization_recommendations"]["optimal_force_compositions"].items():
                f.write(f"**{scenario.replace('_', ' ').title()}**:\n")
                f.write(f"- Optimal Composition: {rec['composition'].replace('_', ' ').title()}\n")
                f.write(f"- Success Probability: {rec['success_probability']:.3f} ({rec['success_probability']*100:.1f}%)\n")
                f.write(f"- Risk Level: {rec['risk_level'].title()}\n\n")
            
            # Detailed analysis
            f.write("## Detailed Analysis\n\n")
            
            # Success probabilities by scenario
            f.write("### Success Probabilities by Scenario\n\n")
            for scenario_name, scenario_data in results["scenario_results"].items():
                f.write(f"#### {scenario_name.replace('_', ' ').title()}\n\n")
                f.write("| Force Composition | Success Probability | Risk Level |\n")
                f.write("|-------------------|-------------------|------------|\n")
                
                for composition, success_prob in scenario_data["success_probabilities"].items():
                    risk_level = scenario_data["risk_assessment"][composition]["risk_level"]
                    f.write(f"| {composition.replace('_', ' ').title()} | {success_prob:.3f} | {risk_level.title()} |\n")
                f.write("\n")
            
            # Cost-effectiveness analysis
            f.write("### Cost-Effectiveness Analysis\n\n")
            f.write("| Force Composition | Total Cost | Cost Efficiency |\n")
            f.write("|-------------------|------------|-----------------|\n")
            
            for composition, data in results["force_composition_analysis"].items():
                f.write(f"| {composition.replace('_', ' ').title()} | {data['total_cost']:.1f} | {data['cost_efficiency']:.3f} |\n")
            f.write("\n")
            
            # Risk assessment
            f.write("### Risk Assessment Summary\n\n")
            f.write("The following risk levels were identified across all scenarios:\n\n")
            
            risk_summary = {"low": 0, "medium": 0, "high": 0}
            for scenario_data in results["scenario_results"].values():
                for risk_data in scenario_data["risk_assessment"].values():
                    risk_summary[risk_data["risk_level"]] += 1
            
            for risk_level, count in risk_summary.items():
                f.write(f"- **{risk_level.title()} Risk**: {count} force composition-scenario combinations\n")
            f.write("\n")
            
            # Recommendations
            f.write("## Strategic Recommendations\n\n")
            
            f.write("### 1. Force Structure Optimization\n\n")
            f.write("Based on the Monte Carlo simulation results, the following force structure optimizations are recommended:\n\n")
            
            for scenario, rec in results["optimization_recommendations"]["optimal_force_compositions"].items():
                f.write(f"- **{scenario.replace('_', ' ').title()}**: Deploy {rec['composition'].replace('_', ' ').title()} ")
                f.write(f"for optimal performance (success probability: {rec['success_probability']*100:.1f}%)\n")
            f.write("\n")
            
            f.write("### 2. Resource Allocation\n\n")
            cost_eff_ranking = results["optimization_recommendations"]["resource_allocation"]["cost_effectiveness_ranking"]
            f.write("**Cost-Effectiveness Ranking (Best to Worst):**\n\n")
            for i, (composition, efficiency) in enumerate(cost_eff_ranking, 1):
                f.write(f"{i}. {composition.replace('_', ' ').title()}: {efficiency:.3f}\n")
            f.write("\n")
            
            f.write("### 3. Risk Mitigation Strategies\n\n")
            f.write("To mitigate identified risks:\n\n")
            f.write("- Implement layered defense strategies for high-risk scenarios\n")
            f.write("- Enhance survivability measures for vulnerable force compositions\n")
            f.write("- Develop contingency plans for worst-case scenarios\n")
            f.write("- Invest in technology to improve force effectiveness\n\n")
            
            # Methodology
            f.write("## Methodology\n\n")
            f.write("### Monte Carlo Simulation Parameters\n\n")
            f.write(f"- **Simulation Iterations**: {results['simulation_parameters']['n_simulations']:,}\n")
            f.write(f"- **Scenarios Analyzed**: {len(results['simulation_parameters']['scenarios'])}\n")
            f.write(f"- **Force Compositions**: {len(results['simulation_parameters']['force_compositions'])}\n")
            f.write(f"- **Random Seed**: Fixed for reproducibility\n\n")
            
            f.write("### Key Assumptions\n\n")
            f.write("- Adversary capabilities based on current intelligence assessments\n")
            f.write("- Environmental factors affect platform effectiveness\n")
            f.write("- Distance impacts force projection capabilities\n")
            f.write("- Success thresholds vary by threat level\n")
            f.write("- Casualty rates inversely related to force effectiveness\n\n")
            
            # Files generated
            f.write("## Generated Files\n\n")
            f.write("This analysis generated the following files:\n\n")
            f.write("- `pacific_conflict_force_optimization_results.json`: Complete simulation results\n")
            f.write("- `pacific_conflict_force_optimization_report.md`: This comprehensive report\n")
            f.write("- `success_probabilities_comparison.png`: Success probability visualization\n")
            f.write("- `risk_assessment_heatmap.png`: Risk assessment heatmap\n")
            f.write("- `cost_effectiveness_analysis.png`: Cost-effectiveness scatter plot\n")
            f.write("- `capability_radar_chart.png`: Capability comparison radar chart\n\n")
            
            f.write("---\n\n")
            f.write("*Analysis performed by DIA3 Monte Carlo Simulation System*")

def main():
    """
    Main execution function.
    """
    print("Pacific Conflict Force Structure Optimization")
    print("=" * 50)
    
    # Initialize optimizer
    optimizer = PacificConflictForceOptimizer()
    
    # Run Monte Carlo simulation
    results = optimizer.run_monte_carlo_simulation(n_simulations=10000)
    
    # Generate visualizations
    optimizer.generate_visualizations(results)
    
    # Save results
    optimizer.save_results(results)
    
    # Print summary
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE")
    print("=" * 50)
    
    best_overall = results["optimization_recommendations"]["overall_best_composition"]
    print(f"Overall Best Force Composition: {best_overall['composition'].replace('_', ' ').title()}")
    print(f"Average Success Rate: {best_overall['avg_success_rate']*100:.1f}%")
    
    print(f"\nResults saved to: {optimizer.results_dir}")
    print(f"Generated files:")
    print(f"- {optimizer.results_dir}/pacific_conflict_force_optimization_results.json")
    print(f"- {optimizer.results_dir}/pacific_conflict_force_optimization_report.md")
    print(f"- {optimizer.results_dir}/*.png (visualizations)")

if __name__ == "__main__":
    main()
