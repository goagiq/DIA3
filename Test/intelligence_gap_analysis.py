#!/usr/bin/env python3
"""
Intelligence Gap Analysis with Monte Carlo Simulation
====================================================

This script identifies intelligence gaps in understanding of 
adversary/capabilities and prioritizes collection requirements using 
Monte Carlo simulation for impact assessment.

Features:
- Intelligence gap identification across multiple domains
- Monte Carlo simulation for impact assessment
- Collection requirement prioritization
- Risk-based gap analysis
- Strategic impact quantification
- Collection strategy recommendations

Author: DIA3 System
Date: 2025-08-17
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
from dataclasses import dataclass, asdict
import random
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


@dataclass
class IntelligenceGap:
    """Represents an identified intelligence gap"""
    id: str
    domain: str
    category: str
    description: str
    current_knowledge_level: float  # 0-1 scale
    required_knowledge_level: float  # 0-1 scale
    strategic_importance: float  # 0-1 scale
    collection_difficulty: float  # 0-1 scale
    time_criticality: float  # 0-1 scale
    adversary_awareness: float  # 0-1 scale
    collection_methods: List[str]
    impact_areas: List[str]
    estimated_collection_cost: float
    estimated_collection_time: int  # days


@dataclass
class CollectionRequirement:
    """Represents a prioritized collection requirement"""
    gap_id: str
    priority_score: float
    collection_methods: List[str]
    timeline: int  # days
    resources_required: Dict[str, float]
    success_probability: float
    risk_factors: List[str]
    mitigation_strategies: List[str]


@dataclass
class MonteCarloResult:
    """Results from Monte Carlo simulation"""
    gap_id: str
    mean_impact: float
    std_impact: float
    min_impact: float
    max_impact: float
    confidence_interval_95: Tuple[float, float]
    risk_level: str
    success_probability: float


class IntelligenceGapAnalyzer:
    """Main class for intelligence gap analysis with Monte Carlo simulation"""
    
    def __init__(self):
        self.gaps: List[IntelligenceGap] = []
        self.collection_requirements: List[CollectionRequirement] = []
        self.monte_carlo_results: List[MonteCarloResult] = []
        self.results_dir = Path("Results/intelligence_gap_analysis")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Define intelligence domains
        self.domains = [
            "military_capabilities",
            "cyber_capabilities", 
            "economic_intentions",
            "political_objectives",
            "technological_advancements",
            "strategic_doctrine",
            "operational_tactics",
            "leadership_decision_making",
            "resource_allocation",
            "alliance_relationships"
        ]
        
        # Define collection methods
        self.collection_methods = [
            "HUMINT", "SIGINT", "OSINT", "GEOINT", "IMINT", 
            "MASINT", "TECHINT", "FININT", "CYBERINT", "SOCMINT"
        ]
        
        # Define impact areas
        self.impact_areas = [
            "strategic_planning", "operational_execution", "tactical_operations",
            "resource_allocation", "risk_assessment", "decision_making",
            "force_structure", "technology_investment", "alliance_management"
        ]

    def generate_sample_gaps(self, num_gaps: int = 20) -> List[IntelligenceGap]:
        """Generate sample intelligence gaps for analysis"""
        gaps = []
        
        gap_templates = [
            {
                "domain": "military_capabilities",
                "category": "force_structure",
                "description": ("Adversary's next-generation weapon system development "
                              "status and capabilities"),
                "collection_methods": ["TECHINT", "IMINT", "OSINT"],
                "impact_areas": ["strategic_planning", "force_structure", 
                               "technology_investment"]
            },
            {
                "domain": "cyber_capabilities", 
                "category": "offensive_cyber",
                "description": ("Advanced persistent threat (APT) group infrastructure "
                              "and operational patterns"),
                "collection_methods": ["CYBERINT", "SIGINT", "OSINT"],
                "impact_areas": ["operational_execution", "risk_assessment", 
                               "decision_making"]
            },
            {
                "domain": "economic_intentions",
                "category": "resource_allocation",
                "description": ("Adversary's defense budget allocation and "
                              "procurement priorities"),
                "collection_methods": ["FININT", "OSINT", "HUMINT"],
                "impact_areas": ["resource_allocation", "strategic_planning", 
                               "force_structure"]
            },
            {
                "domain": "political_objectives",
                "category": "strategic_goals",
                "description": ("Leadership's long-term strategic objectives and "
                              "decision-making calculus"),
                "collection_methods": ["HUMINT", "OSINT", "SIGINT"],
                "impact_areas": ["strategic_planning", "decision_making", 
                               "alliance_management"]
            },
            {
                "domain": "technological_advancements",
                "category": "emerging_tech",
                "description": ("Artificial intelligence and autonomous systems "
                              "development programs"),
                "collection_methods": ["TECHINT", "OSINT", "CYBERINT"],
                "impact_areas": ["technology_investment", "strategic_planning", 
                               "force_structure"]
            },
            {
                "domain": "strategic_doctrine",
                "category": "military_strategy",
                "description": ("Adversary's military doctrine evolution and "
                              "strategic thinking patterns"),
                "collection_methods": ["OSINT", "HUMINT", "SIGINT"],
                "impact_areas": ["strategic_planning", "operational_execution", 
                               "decision_making"]
            },
            {
                "domain": "operational_tactics",
                "category": "tactical_methods",
                "description": ("New operational tactics and procedures being "
                              "developed or employed"),
                "collection_methods": ["IMINT", "SIGINT", "HUMINT"],
                "impact_areas": ["tactical_operations", "operational_execution", 
                               "risk_assessment"]
            },
            {
                "domain": "leadership_decision_making",
                "category": "command_structure",
                "description": ("Command structure and decision-making processes "
                              "within adversary leadership"),
                "collection_methods": ["HUMINT", "SIGINT", "OSINT"],
                "impact_areas": ["decision_making", "strategic_planning", 
                               "alliance_management"]
            },
            {
                "domain": "resource_allocation",
                "category": "logistics",
                "description": ("Logistics and supply chain vulnerabilities and "
                              "capabilities"),
                "collection_methods": ["IMINT", "OSINT", "FININT"],
                "impact_areas": ["resource_allocation", "operational_execution", 
                               "tactical_operations"]
            },
            {
                "domain": "alliance_relationships",
                "category": "diplomatic",
                "description": ("Alliance relationships and potential coalition "
                              "formations"),
                "collection_methods": ["HUMINT", "OSINT", "SIGINT"],
                "impact_areas": ["alliance_management", "strategic_planning", 
                               "decision_making"]
            }
        ]
        
        for i in range(num_gaps):
            template = gap_templates[i % len(gap_templates)]
            
            gap = IntelligenceGap(
                id=f"GAP_{i+1:03d}",
                domain=template["domain"],
                category=template["category"],
                description=template["description"],
                current_knowledge_level=np.random.uniform(0.1, 0.7),
                required_knowledge_level=np.random.uniform(0.7, 0.95),
                strategic_importance=np.random.uniform(0.3, 1.0),
                collection_difficulty=np.random.uniform(0.2, 0.9),
                time_criticality=np.random.uniform(0.1, 1.0),
                adversary_awareness=np.random.uniform(0.1, 0.8),
                collection_methods=template["collection_methods"],
                impact_areas=template["impact_areas"],
                estimated_collection_cost=np.random.uniform(10000, 500000),
                estimated_collection_time=np.random.randint(30, 365)
            )
            gaps.append(gap)
        
        return gaps

    def calculate_gap_priority_score(self, gap: IntelligenceGap) -> float:
        """Calculate priority score for a gap using weighted factors"""
        # Knowledge gap
        knowledge_gap = gap.required_knowledge_level - gap.current_knowledge_level
        
        # Weighted factors
        weights = {
            'knowledge_gap': 0.25,
            'strategic_importance': 0.25,
            'time_criticality': 0.20,
            'collection_difficulty': -0.15,  # Negative weight (easier = higher priority)
            'adversary_awareness': -0.15     # Negative weight (lower awareness = higher priority)
        }
        
        score = (
            weights['knowledge_gap'] * knowledge_gap +
            weights['strategic_importance'] * gap.strategic_importance +
            weights['time_criticality'] * gap.time_criticality +
            weights['collection_difficulty'] * gap.collection_difficulty +
            weights['adversary_awareness'] * gap.adversary_awareness
        )
        
        return max(0, min(1, score))  # Normalize to 0-1

    def run_monte_carlo_simulation(self, gap: IntelligenceGap, num_simulations: int = 10000) -> MonteCarloResult:
        """Run Monte Carlo simulation for impact assessment of a gap"""
        
        impacts = []
        success_probabilities = []
        
        for _ in range(num_simulations):
            # Simulate collection success probability
            base_success = 0.5
            difficulty_factor = 1 - gap.collection_difficulty
            awareness_factor = 1 - gap.adversary_awareness
            time_factor = max(0.1, 1 - (gap.estimated_collection_time / 365))
            
            success_prob = base_success * difficulty_factor * awareness_factor * time_factor
            success_prob = max(0.05, min(0.95, success_prob))
            success_probabilities.append(success_prob)
            
            # Simulate impact if collection is successful
            if np.random.random() < success_prob:
                # Impact factors
                strategic_impact = gap.strategic_importance * np.random.normal(1, 0.2)
                knowledge_impact = (gap.required_knowledge_level - gap.current_knowledge_level) * np.random.normal(1, 0.15)
                time_impact = gap.time_criticality * np.random.normal(1, 0.1)
                
                total_impact = (strategic_impact + knowledge_impact + time_impact) / 3
                impacts.append(total_impact)
            else:
                impacts.append(0)
        
        impacts = np.array(impacts)
        success_probabilities = np.array(success_probabilities)
        
        # Calculate statistics
        mean_impact = np.mean(impacts)
        std_impact = np.std(impacts)
        min_impact = np.min(impacts)
        max_impact = np.max(impacts)
        
        # 95% confidence interval
        confidence_interval_95 = (
            np.percentile(impacts, 2.5),
            np.percentile(impacts, 97.5)
        )
        
        # Risk level classification
        if mean_impact > 0.7:
            risk_level = "HIGH"
        elif mean_impact > 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return MonteCarloResult(
            gap_id=gap.id,
            mean_impact=mean_impact,
            std_impact=std_impact,
            min_impact=min_impact,
            max_impact=max_impact,
            confidence_interval_95=confidence_interval_95,
            risk_level=risk_level,
            success_probability=np.mean(success_probabilities)
        )

    def prioritize_collection_requirements(self) -> List[CollectionRequirement]:
        """Prioritize collection requirements based on gap analysis and Monte Carlo results"""
        requirements = []
        
        for gap in self.gaps:
            # Get Monte Carlo results
            mc_result = next((r for r in self.monte_carlo_results if r.gap_id == gap.id), None)
            if not mc_result:
                continue
            
            # Calculate priority score
            priority_score = self.calculate_gap_priority_score(gap)
            
            # Adjust priority based on Monte Carlo results
            adjusted_priority = priority_score * mc_result.mean_impact * mc_result.success_probability
            
            # Determine timeline based on time criticality
            if gap.time_criticality > 0.8:
                timeline = gap.estimated_collection_time // 2
            elif gap.time_criticality > 0.5:
                timeline = gap.estimated_collection_time
            else:
                timeline = gap.estimated_collection_time * 2
            
            # Estimate resources required
            resources_required = {
                'personnel': gap.estimated_collection_cost * 0.4,
                'technology': gap.estimated_collection_cost * 0.3,
                'operational': gap.estimated_collection_cost * 0.2,
                'analysis': gap.estimated_collection_cost * 0.1
            }
            
            # Identify risk factors
            risk_factors = []
            if gap.collection_difficulty > 0.7:
                risk_factors.append("High collection difficulty")
            if gap.adversary_awareness > 0.6:
                risk_factors.append("High adversary awareness")
            if gap.estimated_collection_time > 180:
                risk_factors.append("Long collection timeline")
            if mc_result.success_probability < 0.3:
                risk_factors.append("Low success probability")
            
            # Generate mitigation strategies
            mitigation_strategies = []
            if "High collection difficulty" in risk_factors:
                mitigation_strategies.append("Employ multiple collection methods")
            if "High adversary awareness" in risk_factors:
                mitigation_strategies.append("Use covert collection techniques")
            if "Long collection timeline" in risk_factors:
                mitigation_strategies.append("Prioritize critical information first")
            if "Low success probability" in risk_factors:
                mitigation_strategies.append("Increase resource allocation")
            
            requirement = CollectionRequirement(
                gap_id=gap.id,
                priority_score=adjusted_priority,
                collection_methods=gap.collection_methods,
                timeline=timeline,
                resources_required=resources_required,
                success_probability=mc_result.success_probability,
                risk_factors=risk_factors,
                mitigation_strategies=mitigation_strategies
            )
            requirements.append(requirement)
        
        # Sort by priority score
        requirements.sort(key=lambda x: x.priority_score, reverse=True)
        return requirements

    def generate_visualizations(self):
        """Generate comprehensive visualizations for the analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Intelligence Gap Analysis with Monte Carlo Simulation', fontsize=16, fontweight='bold')
        
        # 1. Gap Priority Distribution
        priority_scores = [req.priority_score for req in self.collection_requirements]
        axes[0, 0].hist(priority_scores, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Collection Priority Distribution')
        axes[0, 0].set_xlabel('Priority Score')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Domain-wise Gap Analysis
        domain_gaps = {}
        for gap in self.gaps:
            if gap.domain not in domain_gaps:
                domain_gaps[gap.domain] = []
            domain_gaps[gap.domain].append(gap)
        
        domains = list(domain_gaps.keys())
        gap_counts = [len(domain_gaps[domain]) for domain in domains]
        
        axes[0, 1].bar(range(len(domains)), gap_counts, color='lightcoral', alpha=0.7)
        axes[0, 1].set_title('Gaps by Domain')
        axes[0, 1].set_xlabel('Domain')
        axes[0, 1].set_ylabel('Number of Gaps')
        axes[0, 1].set_xticks(range(len(domains)))
        axes[0, 1].set_xticklabels([d.replace('_', '\n') for d in domains], rotation=45, ha='right')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Monte Carlo Impact Distribution
        impact_means = [mc.mean_impact for mc in self.monte_carlo_results]
        axes[0, 2].hist(impact_means, bins=10, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 2].set_title('Monte Carlo Impact Distribution')
        axes[0, 2].set_xlabel('Mean Impact')
        axes[0, 2].set_ylabel('Frequency')
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Success Probability vs Priority
        success_probs = [req.success_probability for req in self.collection_requirements]
        axes[1, 0].scatter(success_probs, priority_scores, alpha=0.6, color='purple')
        axes[1, 0].set_title('Success Probability vs Priority')
        axes[1, 0].set_xlabel('Success Probability')
        axes[1, 0].set_ylabel('Priority Score')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Collection Cost vs Impact
        collection_costs = [gap.estimated_collection_cost for gap in self.gaps]
        axes[1, 1].scatter(collection_costs, impact_means, alpha=0.6, color='orange')
        axes[1, 1].set_title('Collection Cost vs Impact')
        axes[1, 1].set_xlabel('Estimated Collection Cost ($)')
        axes[1, 1].set_ylabel('Mean Impact')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Risk Level Distribution
        risk_levels = [mc.risk_level for mc in self.monte_carlo_results]
        risk_counts = {'LOW': risk_levels.count('LOW'), 
                      'MEDIUM': risk_levels.count('MEDIUM'), 
                      'HIGH': risk_levels.count('HIGH')}
        
        colors = ['green', 'yellow', 'red']
        axes[1, 2].pie(risk_counts.values(), labels=risk_counts.keys(), autopct='%1.1f%%', 
                      colors=colors, startangle=90)
        axes[1, 2].set_title('Risk Level Distribution')
        
        plt.tight_layout()
        plt.savefig(self.results_dir / f'intelligence_gap_analysis_{timestamp}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        return f'intelligence_gap_analysis_{timestamp}.png'

    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram showing the intelligence gap analysis system"""
        mermaid_diagram = """
graph TD
    A[Intelligence Gap Analysis] --> B[Gap Identification]
    A --> C[Monte Carlo Simulation]
    A --> D[Collection Prioritization]
    A --> E[Impact Assessment]
    
    B --> B1[Domain Analysis]
    B --> B2[Category Classification]
    B --> B3[Knowledge Level Assessment]
    B --> B4[Strategic Importance]
    
    C --> C1[Success Probability Simulation]
    C --> C2[Impact Distribution Analysis]
    C --> C3[Risk Level Classification]
    C --> C4[Confidence Interval Calculation]
    
    D --> D1[Priority Score Calculation]
    D --> D2[Resource Allocation]
    D --> D3[Timeline Planning]
    D --> D4[Risk Mitigation Strategies]
    
    E --> E1[Strategic Impact]
    E --> E2[Operational Impact]
    E --> E3[Tactical Impact]
    E --> E4[Resource Impact]
    
    F[Collection Methods] --> F1[HUMINT]
    F --> F2[SIGINT]
    F --> F3[OSINT]
    F --> F4[GEOINT]
    F --> F5[IMINT]
    F --> F6[MASINT]
    F --> F7[TECHINT]
    F --> F8[FININT]
    F --> F9[CYBERINT]
    F --> F10[SOCMINT]
    
    G[Intelligence Domains] --> G1[Military Capabilities]
    G --> G2[Cyber Capabilities]
    G --> G3[Economic Intentions]
    G --> G4[Political Objectives]
    G --> G5[Technological Advancements]
    G --> G6[Strategic Doctrine]
    G --> G7[Operational Tactics]
    G --> G8[Leadership Decision Making]
    G --> G9[Resource Allocation]
    G --> G10[Alliance Relationships]
    
    H[Impact Areas] --> H1[Strategic Planning]
    H --> H2[Operational Execution]
    H --> H3[Tactical Operations]
    H --> H4[Resource Allocation]
    H --> H5[Risk Assessment]
    H --> H6[Decision Making]
    H --> H7[Force Structure]
    H --> H8[Technology Investment]
    H --> H9[Alliance Management]
    
    B --> F
    B --> G
    B --> H
    
    C --> I[Monte Carlo Engine]
    I --> I1[10,000+ Simulations]
    I --> I2[Probability Distributions]
    I --> I3[Risk Assessment]
    I --> I4[Confidence Intervals]
    
    D --> J[Collection Requirements]
    J --> J1[Prioritized List]
    J --> J2[Resource Requirements]
    J --> J3[Timeline Estimates]
    J --> J4[Risk Mitigation]
    
    E --> K[Intelligence Products]
    K --> K1[Gap Matrix]
    K --> K2[Collection Strategy]
    K --> K3[Impact Assessment]
    K --> K4[Recommendations]
    
    style A fill:#e1f5fe
    style I fill:#f3e5f5
    style J fill:#e8f5e8
    style K fill:#fff3e0
    """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        diagram_file = self.results_dir / f'intelligence_gap_analysis_system_{timestamp}.md'
        
        with open(diagram_file, 'w') as f:
            f.write(f"# Intelligence Gap Analysis System Architecture\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## System Components and Data Flow\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_diagram)
            f.write("```\n")
        
        return str(diagram_file)

    def run_analysis(self, num_gaps: int = 20, num_simulations: int = 10000) -> Dict[str, Any]:
        """Run complete intelligence gap analysis"""
        print("🔍 Starting Intelligence Gap Analysis with Monte Carlo Simulation...")
        
        # Generate sample gaps
        print(f"📋 Generating {num_gaps} sample intelligence gaps...")
        self.gaps = self.generate_sample_gaps(num_gaps)
        
        # Run Monte Carlo simulations
        print(f"🎲 Running Monte Carlo simulations ({num_simulations:,} iterations per gap)...")
        for gap in self.gaps:
            mc_result = self.run_monte_carlo_simulation(gap, num_simulations)
            self.monte_carlo_results.append(mc_result)
        
        # Prioritize collection requirements
        print("📊 Prioritizing collection requirements...")
        self.collection_requirements = self.prioritize_collection_requirements()
        
        # Generate visualizations
        print("📈 Generating visualizations...")
        viz_file = self.generate_visualizations()
        
        # Generate Mermaid diagram
        print("🏗️ Generating system architecture diagram...")
        diagram_file = self.generate_mermaid_diagram()
        
        # Prepare results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        results = {
            "analysis_timestamp": timestamp,
            "total_gaps_analyzed": len(self.gaps),
            "monte_carlo_simulations_per_gap": num_simulations,
            "total_simulations": len(self.gaps) * num_simulations,
            "gaps": [asdict(gap) for gap in self.gaps],
            "collection_requirements": [asdict(req) for req in self.collection_requirements],
            "monte_carlo_results": [asdict(result) for result in self.monte_carlo_results],
            "visualization_file": str(self.results_dir / viz_file),
            "system_diagram_file": diagram_file,
            "summary_statistics": {
                "average_priority_score": np.mean([req.priority_score for req in self.collection_requirements]),
                "average_success_probability": np.mean([req.success_probability for req in self.collection_requirements]),
                "average_impact": np.mean([mc.mean_impact for mc in self.monte_carlo_results]),
                "high_priority_gaps": len([req for req in self.collection_requirements if req.priority_score > 0.7]),
                "high_risk_gaps": len([mc for mc in self.monte_carlo_results if mc.risk_level == "HIGH"]),
                "total_estimated_cost": sum([gap.estimated_collection_cost for gap in self.gaps])
            }
        }
        
        # Save results
        results_file = self.results_dir / f'intelligence_gap_analysis_results_{timestamp}.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Generate markdown report
        report_file = self.results_dir / f'intelligence_gap_analysis_report_{timestamp}.md'
        self.generate_markdown_report(results, report_file)
        
        print(f"✅ Analysis complete! Results saved to:")
        print(f"   📄 JSON Results: {results_file}")
        print(f"   📋 Markdown Report: {report_file}")
        print(f"   📊 Visualization: {self.results_dir / viz_file}")
        print(f"   🏗️ System Diagram: {diagram_file}")
        
        return results

    def generate_markdown_report(self, results: Dict[str, Any], report_file: Path):
        """Generate comprehensive markdown report"""
        with open(report_file, 'w') as f:
            f.write(f"# Intelligence Gap Analysis Report\n\n")
            f.write(f"**Generated:** {results['analysis_timestamp']}\n\n")
            f.write(f"**Total Gaps Analyzed:** {results['total_gaps_analyzed']}\n")
            f.write(f"**Monte Carlo Simulations:** {results['total_simulations']:,}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            stats = results['summary_statistics']
            f.write(f"This analysis identified **{results['total_gaps_analyzed']} intelligence gaps** across multiple domains. ")
            f.write(f"Using Monte Carlo simulation with **{results['monte_carlo_simulations_per_gap']:,} iterations per gap**, ")
            f.write(f"we prioritized collection requirements and assessed their strategic impact.\n\n")
            
            f.write(f"**Key Findings:**\n")
            f.write(f"- **{stats['high_priority_gaps']} high-priority gaps** requiring immediate attention\n")
            f.write(f"- **{stats['high_risk_gaps']} high-risk gaps** with significant strategic implications\n")
            f.write(f"- Average success probability: **{stats['average_success_probability']:.1%}**\n")
            f.write(f"- Average strategic impact: **{stats['average_impact']:.2f}**\n")
            f.write(f"- Total estimated collection cost: **${stats['total_estimated_cost']:,.0f}**\n\n")
            
            # Top Priority Gaps
            f.write("## Top Priority Intelligence Gaps\n\n")
            f.write("| Rank | Gap ID | Domain | Priority Score | Success Probability | Risk Level | Estimated Cost |\n")
            f.write("|------|--------|--------|----------------|-------------------|------------|----------------|\n")
            
            for i, req in enumerate(results['collection_requirements'][:10], 1):
                gap = next(g for g in results['gaps'] if g['id'] == req['gap_id'])
                mc_result = next(mc for mc in results['monte_carlo_results'] if mc['gap_id'] == req['gap_id'])
                f.write(f"| {i} | {req['gap_id']} | {gap['domain'].replace('_', ' ').title()} | {req['priority_score']:.3f} | {req['success_probability']:.1%} | {mc_result['risk_level']} | ${gap['estimated_collection_cost']:,.0f} |\n")
            
            f.write("\n")
            
            # Domain Analysis
            f.write("## Gap Analysis by Domain\n\n")
            domain_stats = {}
            for gap in results['gaps']:
                domain = gap['domain']
                if domain not in domain_stats:
                    domain_stats[domain] = {'count': 0, 'avg_priority': 0, 'total_cost': 0}
                domain_stats[domain]['count'] += 1
                domain_stats[domain]['total_cost'] += gap['estimated_collection_cost']
            
            for req in results['collection_requirements']:
                gap = next(g for g in results['gaps'] if g['id'] == req['gap_id'])
                domain = gap['domain']
                domain_stats[domain]['avg_priority'] += req['priority_score']
            
            for domain, stats in domain_stats.items():
                stats['avg_priority'] /= stats['count']
            
            f.write("| Domain | Gap Count | Average Priority | Total Cost |\n")
            f.write("|--------|-----------|------------------|------------|\n")
            for domain, stats in sorted(domain_stats.items(), key=lambda x: x[1]['avg_priority'], reverse=True):
                f.write(f"| {domain.replace('_', ' ').title()} | {stats['count']} | {stats['avg_priority']:.3f} | ${stats['total_cost']:,.0f} |\n")
            
            f.write("\n")
            
            # Collection Strategy Recommendations
            f.write("## Collection Strategy Recommendations\n\n")
            f.write("### High-Priority Collection Methods\n\n")
            method_usage = {}
            for req in results['collection_requirements']:
                for method in req['collection_methods']:
                    if method not in method_usage:
                        method_usage[method] = 0
                    method_usage[method] += 1
            
            f.write("| Collection Method | Usage Frequency |\n")
            f.write("|-------------------|-----------------|\n")
            for method, count in sorted(method_usage.items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {method} | {count} |\n")
            
            f.write("\n")
            
            # Risk Assessment
            f.write("## Risk Assessment Summary\n\n")
            risk_counts = {}
            for mc_result in results['monte_carlo_results']:
                risk_level = mc_result['risk_level']
                if risk_level not in risk_counts:
                    risk_counts[risk_level] = 0
                risk_counts[risk_level] += 1
            
            f.write("| Risk Level | Count | Percentage |\n")
            f.write("|------------|-------|------------|\n")
            for risk_level in ['HIGH', 'MEDIUM', 'LOW']:
                count = risk_counts.get(risk_level, 0)
                percentage = (count / len(results['monte_carlo_results'])) * 100
                f.write(f"| {risk_level} | {count} | {percentage:.1f}% |\n")
            
            f.write("\n")
            
            # Monte Carlo Analysis Details
            f.write("## Monte Carlo Simulation Analysis\n\n")
            f.write(f"The analysis employed **{results['monte_carlo_simulations_per_gap']:,} Monte Carlo simulations per gap** ")
            f.write(f"to assess collection success probability and strategic impact. Key metrics include:\n\n")
            
            f.write("- **Mean Impact**: Average strategic impact if collection is successful\n")
            f.write("- **Standard Deviation**: Variability in impact assessment\n")
            f.write("- **Confidence Intervals**: 95% confidence range for impact estimates\n")
            f.write("- **Success Probability**: Likelihood of successful collection\n")
            f.write("- **Risk Level**: Classification based on impact and uncertainty\n\n")
            
            # Implementation Recommendations
            f.write("## Implementation Recommendations\n\n")
            f.write("### Immediate Actions (Next 30 Days)\n\n")
            high_priority = [req for req in results['collection_requirements'] if req['priority_score'] > 0.7]
            for req in high_priority[:5]:
                gap = next(g for g in results['gaps'] if g['id'] == req['gap_id'])
                f.write(f"1. **{req['gap_id']}**: {gap['description'][:100]}...\n")
                f.write(f"   - Priority Score: {req['priority_score']:.3f}\n")
                f.write(f"   - Collection Methods: {', '.join(req['collection_methods'])}\n")
                f.write(f"   - Timeline: {req['timeline']} days\n")
                f.write(f"   - Risk Factors: {', '.join(req['risk_factors'])}\n\n")
            
            f.write("### Medium-Term Actions (30-90 Days)\n\n")
            medium_priority = [req for req in results['collection_requirements'] if 0.4 <= req['priority_score'] <= 0.7]
            for req in medium_priority[:5]:
                gap = next(g for g in results['gaps'] if g['id'] == req['gap_id'])
                f.write(f"1. **{req['gap_id']}**: {gap['description'][:100]}...\n")
                f.write(f"   - Priority Score: {req['priority_score']:.3f}\n")
                f.write(f"   - Collection Methods: {', '.join(req['collection_methods'])}\n\n")
            
            # Technical Details
            f.write("## Technical Implementation Details\n\n")
            f.write("### System Architecture\n\n")
            f.write("The intelligence gap analysis system integrates:\n\n")
            f.write("- **Monte Carlo Simulation Engine**: Probabilistic impact assessment\n")
            f.write("- **Multi-Domain Analysis**: Coverage across 10 intelligence domains\n")
            f.write("- **Collection Method Optimization**: 10 different collection methods\n")
            f.write("- **Risk Assessment Framework**: Comprehensive risk evaluation\n")
            f.write("- **Resource Allocation Planning**: Cost and timeline estimation\n\n")
            
            f.write("### Analysis Methodology\n\n")
            f.write("1. **Gap Identification**: Systematic identification across intelligence domains\n")
            f.write("2. **Priority Scoring**: Weighted scoring based on multiple factors\n")
            f.write("3. **Monte Carlo Simulation**: Probabilistic impact assessment\n")
            f.write("4. **Collection Planning**: Method selection and resource allocation\n")
            f.write("5. **Risk Mitigation**: Strategy development for high-risk gaps\n\n")
            
            f.write("### Data Sources and Integration\n\n")
            f.write("- **Intelligence Domains**: Military, cyber, economic, political, technological\n")
            f.write("- **Collection Methods**: HUMINT, SIGINT, OSINT, GEOINT, IMINT, MASINT, TECHINT, FININT, CYBERINT, SOCMINT\n")
            f.write("- **Impact Areas**: Strategic planning, operational execution, tactical operations\n")
            f.write("- **Risk Factors**: Collection difficulty, adversary awareness, timeline constraints\n\n")

def main():
    """Main execution function"""
    print("🔍 Intelligence Gap Analysis with Monte Carlo Simulation")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = IntelligenceGapAnalyzer()
    
    # Run analysis
    results = analyzer.run_analysis(num_gaps=20, num_simulations=10000)
    
    # Print summary
    print("\n📊 Analysis Summary:")
    print(f"   • Total gaps analyzed: {results['total_gaps_analyzed']}")
    print(f"   • Monte Carlo simulations: {results['total_simulations']:,}")
    print(f"   • High-priority gaps: {results['summary_statistics']['high_priority_gaps']}")
    print(f"   • High-risk gaps: {results['summary_statistics']['high_risk_gaps']}")
    print(f"   • Average success probability: {results['summary_statistics']['average_success_probability']:.1%}")
    print(f"   • Total estimated cost: ${results['summary_statistics']['total_estimated_cost']:,.0f}")
    
    print("\n🎯 Top 5 Priority Gaps:")
    for i, req in enumerate(results['collection_requirements'][:5], 1):
        gap = next(g for g in results['gaps'] if g['id'] == req['gap_id'])
        print(f"   {i}. {req['gap_id']}: {gap['description'][:80]}...")
        print(f"      Priority: {req['priority_score']:.3f}, Success: {req['success_probability']:.1%}")

if __name__ == "__main__":
    main()
