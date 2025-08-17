#!/usr/bin/env python3
"""
Adversary Force Projection Simulation using Log-Normal Distribution
Specific test script for simulating potential adversary force projection capabilities
using log-normal distribution as requested in MONTE_CARLO_TEST_SCENARIOS.md
"""

import asyncio
import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.force_projection_engine import ForceProjectionEngine, AdversaryType, DomainType


class AdversaryForceProjectionSimulator:
    """Specialized simulator for adversary force projection using log-normal distributions"""
    
    def __init__(self):
        self.engine = ForceProjectionEngine()
        self.results = []
        
    async def simulate_adversary_capabilities(
        self,
        adversary_type: str = "peer_adversary",
        domain_type: str = "defense",
        time_horizon_months: int = 24,
        num_iterations: int = 10000,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Simulate potential adversary force projection capabilities using log-normal distribution
        
        Args:
            adversary_type: Type of adversary (peer_adversary, business_competitor, cyber_adversary)
            domain_type: Domain type (defense, business, cyber, financial)
            time_horizon_months: Time horizon for projection analysis
            num_iterations: Number of Monte Carlo iterations
            confidence_level: Confidence level for intervals
            
        Returns:
            Comprehensive simulation results with log-normal distribution analysis
        """
        
        print(f"🎯 Simulating {adversary_type} force projection capabilities in {domain_type} domain")
        print(f"📊 Using log-normal distribution with {num_iterations:,} iterations")
        print(f"⏰ Time horizon: {time_horizon_months} months")
        print(f"📈 Confidence level: {confidence_level*100}%")
        print("-" * 80)
        
        # Run the simulation
        result = await self.engine.simulate_force_projection_capabilities(
            adversary_type=adversary_type,
            domain_type=domain_type,
            time_horizon_months=time_horizon_months,
            num_iterations=num_iterations,
            confidence_level=confidence_level
        )
        
        # Store results
        self.results.append({
            "adversary_type": adversary_type,
            "domain_type": domain_type,
            "simulation_id": result.simulation_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return self._analyze_log_normal_results(result, adversary_type, domain_type)
    
    def _analyze_log_normal_results(
        self, 
        result: Any, 
        adversary_type: str, 
        domain_type: str
    ) -> Dict[str, Any]:
        """Analyze log-normal distribution results"""
        
        analysis = {
            "simulation_id": result.simulation_id,
            "adversary_type": adversary_type,
            "domain_type": domain_type,
            "threat_assessment": result.threat_assessment,
            "effectiveness_analysis": result.effectiveness_analysis,
            "log_normal_analysis": {},
            "capability_breakdown": {},
            "risk_metrics": {},
            "recommendations": []
        }
        
        # Analyze log-normal distribution characteristics
        if hasattr(result, 'capability_analysis') and result.capability_analysis:
            for area, capabilities in result.capability_analysis.items():
                area_analysis = {}
                
                for capability, data in capabilities.items():
                    if 'distribution_params' in data:
                        mu = data['distribution_params']['mu']
                        sigma = data['distribution_params']['sigma']
                        
                        # Log-normal distribution characteristics
                        mean_theoretical = np.exp(mu + sigma**2 / 2)
                        variance_theoretical = (np.exp(sigma**2) - 1) * np.exp(2*mu + sigma**2)
                        std_theoretical = np.sqrt(variance_theoretical)
                        
                        # Skewness for log-normal distribution
                        skewness = (np.exp(sigma**2) + 2) * np.sqrt(np.exp(sigma**2) - 1)
                        
                        area_analysis[capability] = {
                            "distribution_type": "log_normal",
                            "mu": mu,
                            "sigma": sigma,
                            "theoretical_mean": mean_theoretical,
                            "theoretical_std": std_theoretical,
                            "skewness": skewness,
                            "actual_mean": data.get('mean', 0),
                            "actual_median": data.get('median', 0),
                            "percentiles": data.get('percentiles', {}),
                            "confidence_interval": data.get('confidence_interval', {}),
                            "units": data.get('units', ''),
                            "description": data.get('description', '')
                        }
                
                analysis["capability_breakdown"][area] = area_analysis
        
        # Calculate risk metrics
        analysis["risk_metrics"] = self._calculate_risk_metrics(result)
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _calculate_risk_metrics(self, result: Any) -> Dict[str, Any]:
        """Calculate risk metrics from simulation results"""
        
        threat_level = result.threat_assessment.get("threat_level", "UNKNOWN")
        effectiveness = result.effectiveness_analysis.get("overall_effectiveness", 0)
        
        # Risk scoring based on threat level and effectiveness
        risk_scores = {
            "CRITICAL": 0.9,
            "HIGH": 0.7,
            "MEDIUM": 0.5,
            "LOW": 0.3,
            "MINIMAL_THREAT": 0.1,
            "MINIMAL_COMPETITION": 0.05
        }
        
        base_risk = risk_scores.get(threat_level, 0.5)
        effectiveness_risk = effectiveness * 0.5  # Higher effectiveness = higher risk
        
        total_risk = min(1.0, base_risk + effectiveness_risk)
        
        return {
            "threat_level": threat_level,
            "effectiveness_score": effectiveness,
            "base_risk_score": base_risk,
            "effectiveness_risk_contribution": effectiveness_risk,
            "total_risk_score": total_risk,
            "risk_category": self._categorize_risk(total_risk)
        }
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk based on score"""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        elif risk_score >= 0.2:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        risk_metrics = analysis.get("risk_metrics", {})
        threat_level = risk_metrics.get("threat_level", "UNKNOWN")
        total_risk = risk_metrics.get("total_risk_score", 0)
        
        # Threat level based recommendations
        if threat_level in ["CRITICAL", "HIGH"]:
            recommendations.extend([
                "Implement immediate countermeasures and defensive strategies",
                "Increase monitoring and intelligence gathering efforts",
                "Develop contingency plans for worst-case scenarios",
                "Consider preemptive defensive actions"
            ])
        elif threat_level == "MEDIUM":
            recommendations.extend([
                "Maintain current defensive posture with enhanced monitoring",
                "Develop response plans for potential escalation",
                "Strengthen critical infrastructure protection"
            ])
        else:
            recommendations.extend([
                "Continue routine monitoring and assessment",
                "Maintain baseline defensive capabilities",
                "Periodic review of threat assessment"
            ])
        
        # Log-normal distribution specific recommendations
        recommendations.extend([
            "Monitor for right-skewed capability growth patterns",
            "Prepare for potential rapid capability escalation",
            "Consider asymmetric response strategies"
        ])
        
        return recommendations
    
    def print_detailed_analysis(self, analysis: Dict[str, Any]):
        """Print detailed analysis of the simulation results"""
        
        print(f"\n📊 DETAILED ANALYSIS RESULTS")
        print("=" * 80)
        print(f"🎯 Adversary Type: {analysis['adversary_type']}")
        print(f"🌍 Domain Type: {analysis['domain_type']}")
        print(f"🆔 Simulation ID: {analysis['simulation_id']}")
        
        # Threat Assessment
        threat = analysis['threat_assessment']
        print(f"\n🚨 THREAT ASSESSMENT")
        print(f"   Threat Level: {threat.get('threat_level', 'UNKNOWN')}")
        print(f"   Confidence: {threat.get('confidence', 'N/A')}")
        print(f"   Key Factors: {', '.join(threat.get('key_factors', []))}")
        
        # Effectiveness Analysis
        effectiveness = analysis['effectiveness_analysis']
        print(f"\n📈 EFFECTIVENESS ANALYSIS")
        print(f"   Overall Effectiveness: {effectiveness.get('overall_effectiveness', 0):.3f}")
        print(f"   Capability Score: {effectiveness.get('capability_score', 0):.3f}")
        print(f"   Resource Efficiency: {effectiveness.get('resource_efficiency', 0):.3f}")
        
        # Risk Metrics
        risk = analysis['risk_metrics']
        print(f"\n⚠️  RISK METRICS")
        print(f"   Total Risk Score: {risk.get('total_risk_score', 0):.3f}")
        print(f"   Risk Category: {risk.get('risk_category', 'UNKNOWN')}")
        print(f"   Base Risk: {risk.get('base_risk_score', 0):.3f}")
        print(f"   Effectiveness Risk: {risk.get('effectiveness_risk_contribution', 0):.3f}")
        
        # Log-Normal Distribution Analysis
        print(f"\n📊 LOG-NORMAL DISTRIBUTION ANALYSIS")
        for area, capabilities in analysis.get('capability_breakdown', {}).items():
            print(f"\n   {area.upper()} CAPABILITIES:")
            for capability, data in capabilities.items():
                print(f"     {capability}:")
                print(f"       Distribution: μ={data['mu']:.3f}, σ={data['sigma']:.3f}")
                print(f"       Theoretical Mean: {data['theoretical_mean']:.3f}")
                print(f"       Skewness: {data['skewness']:.3f}")
                print(f"       Units: {data['units']}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        for i, rec in enumerate(analysis.get('recommendations', []), 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "=" * 80)
    
    def save_results(self, filename: str = None):
        """Save simulation results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"adversary_force_projection_results_{timestamp}.json"
        
        output_path = os.path.join("Results", filename)
        
        # Convert results to serializable format
        serializable_results = []
        for result in self.results:
            serializable_result = {
                "adversary_type": result["adversary_type"],
                "domain_type": result["domain_type"],
                "simulation_id": result["simulation_id"],
                "timestamp": result["timestamp"],
                "analysis": self._analyze_log_normal_results(
                    result["result"], 
                    result["adversary_type"], 
                    result["domain_type"]
                )
            }
            serializable_results.append(serializable_result)
        
        with open(output_path, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"💾 Results saved to: {output_path}")
        return output_path


async def main():
    """Main function to run adversary force projection simulations"""
    
    print("🎯 ADVERSARY FORCE PROJECTION SIMULATION")
    print("Using Log-Normal Distribution Monte Carlo Analysis")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Initialize simulator
    simulator = AdversaryForceProjectionSimulator()
    
    # Define simulation scenarios
    scenarios = [
        {
            "adversary_type": "peer_adversary",
            "domain_type": "defense",
            "description": "Peer adversary in defense domain"
        },
        {
            "adversary_type": "cyber_adversary", 
            "domain_type": "cyber",
            "description": "Cyber adversary in cyber domain"
        },
        {
            "adversary_type": "business_competitor",
            "domain_type": "business", 
            "description": "Business competitor in business domain"
        }
    ]
    
    # Run simulations
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔬 SCENARIO {i}: {scenario['description']}")
        print("-" * 60)
        
        try:
            analysis = await simulator.simulate_adversary_capabilities(
                adversary_type=scenario["adversary_type"],
                domain_type=scenario["domain_type"],
                time_horizon_months=24,
                num_iterations=10000,
                confidence_level=0.95
            )
            
            # Print detailed analysis
            simulator.print_detailed_analysis(analysis)
            
        except Exception as e:
            print(f"❌ Error in scenario {i}: {str(e)}")
            continue
    
    # Save all results
    print(f"\n💾 SAVING RESULTS")
    print("-" * 40)
    output_file = simulator.save_results()
    
    print(f"\n🎉 SIMULATION COMPLETED SUCCESSFULLY!")
    print(f"📊 Total simulations run: {len(simulator.results)}")
    print(f"📄 Results saved to: {output_file}")
    
    return True


if __name__ == "__main__":
    # Run the simulation
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
