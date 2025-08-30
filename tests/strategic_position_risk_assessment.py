#!/usr/bin/env python3
"""
Strategic Position Risk Assessment using Monte Carlo Simulation
and Historical Strategic Outcomes from Classical Literature

This script evaluates the risk of current strategic position using Monte Carlo 
simulation and compares results against historical strategic outcomes from 
classical literature, particularly Sun Tzu's Art of War and other strategic 
texts.

Author: DIA3 Strategic Intelligence Team
Date: 2025-08-17
"""

import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import beta
import warnings
warnings.filterwarnings('ignore')


# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class StrategicPosition:
    """Represents a strategic position with key metrics."""
    name: str
    the_way: float  # Moral influence and organizational culture (0-100)
    heaven: float   # Timing and external conditions (0-100)
    earth: float    # Terrain and positioning (0-100)
    command: float  # Leadership and decision-making (0-100)
    method: float   # Organization and discipline (0-100)
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def get_overall_score(self) -> float:
        """Calculate overall strategic position score using Art of War weights."""
        weights = {
            'the_way': 0.25,    # Moral influence is fundamental
            'heaven': 0.20,     # Timing and conditions
            'earth': 0.20,      # Positioning and terrain
            'command': 0.20,    # Leadership
            'method': 0.15      # Organization and discipline
        }
        
        return sum(
            getattr(self, key) * weight for key, weight in weights.items()
        )
    
    def get_risk_score(self) -> float:
        """Calculate risk score (inverse of strength)."""
        return 100 - self.get_overall_score()


@dataclass
class HistoricalOutcome:
    """Represents a historical strategic outcome for comparison."""
    conflict_name: str
    period: str
    victor: str
    loser: str
    victor_position: StrategicPosition
    loser_position: StrategicPosition
    outcome_factors: Dict[str, float]
    lessons_learned: List[str]
    source: str  # Classical literature source


@dataclass
class MonteCarloResult:
    """Results from Monte Carlo simulation."""
    scenario_name: str
    iterations: int
    risk_scores: List[float]
    success_probabilities: List[float]
    failure_probabilities: List[float]
    confidence_intervals: Dict[str, Tuple[float, float]]
    risk_distribution: Dict[str, float]
    historical_comparison: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class StrategicPositionRiskAssessor:
    """
    Comprehensive strategic position risk assessment using Monte Carlo simulation
    and historical strategic outcomes from classical literature.
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8003"):
        self.base_url = base_url
        self.historical_outcomes = self._load_historical_outcomes()
        self.art_of_war_principles = self._load_art_of_war_principles()
        
        # Monte Carlo parameters
        self.default_iterations = 10000
        self.confidence_level = 0.95
        
        logger.info("Strategic Position Risk Assessor initialized")
    
    def _load_historical_outcomes(self) -> List[HistoricalOutcome]:
        """Load historical strategic outcomes from classical literature."""
        outcomes = []
        
        # Art of War examples
        outcomes.append(HistoricalOutcome(
            conflict_name="Battle of Red Cliffs (208 CE)",
            period="Three Kingdoms Period",
            victor="Allied Forces (Liu Bei & Sun Quan)",
            loser="Cao Cao",
            victor_position=StrategicPosition(
                name="Allied Forces",
                the_way=85,  # Strong moral cause
                heaven=90,   # Favorable weather conditions
                earth=80,    # Defensive position advantage
                command=85,  # Good leadership coordination
                method=75    # Effective organization
            ),
            loser_position=StrategicPosition(
                name="Cao Cao's Forces",
                the_way=60,  # Weaker moral position
                heaven=30,   # Unfavorable weather
                earth=40,    # Poor positioning
                command=70,  # Good but overconfident
                method=80    # Well-organized but inflexible
            ),
            outcome_factors={
                'weather_advantage': 0.8,
                'positional_advantage': 0.7,
                'leadership_coordination': 0.6,
                'tactical_flexibility': 0.5
            },
            lessons_learned=[
                "Never underestimate the importance of weather and terrain",
                "Coordination between allies can overcome numerical disadvantage",
                "Flexibility in tactics is crucial for success",
                "Overconfidence can lead to strategic blindness"
            ],
            source="Art of War - Chapter 1: Laying Plans"
        ))
        
        # War and Peace examples
        outcomes.append(HistoricalOutcome(
            conflict_name="Napoleon's Russian Campaign (1812)",
            period="Napoleonic Wars",
            victor="Russian Empire",
            loser="French Empire",
            victor_position=StrategicPosition(
                name="Russian Empire",
                the_way=90,  # Defending homeland
                heaven=85,   # Russian winter
                earth=95,    # Vast territory advantage
                command=80,  # Kutuzov's leadership
                method=70    # Scorched earth strategy
            ),
            loser_position=StrategicPosition(
                name="French Empire",
                the_way=60,  # Aggressive expansion
                heaven=20,   # Unprepared for winter
                earth=30,    # Overextended supply lines
                command=85,  # Napoleon's genius
                method=90    # Well-organized but inflexible
            ),
            outcome_factors={
                'territorial_depth': 0.9,
                'weather_advantage': 0.8,
                'supply_line_vulnerability': 0.7,
                'defensive_morale': 0.8
            },
            lessons_learned=[
                "Territorial depth can be a decisive advantage",
                "Weather and climate must be factored into strategic planning",
                "Overextension of supply lines is a critical vulnerability",
                "Defensive morale can overcome numerical disadvantage"
            ],
            source="War and Peace - Tolstoy's analysis of Napoleon's campaign"
        ))
        
        # Additional classical examples
        outcomes.append(HistoricalOutcome(
            conflict_name="Battle of Marathon (490 BCE)",
            period="Greco-Persian Wars",
            victor="Athenian Forces",
            loser="Persian Empire",
            victor_position=StrategicPosition(
                name="Athenian Forces",
                the_way=95,  # Defending democracy and homeland
                heaven=80,   # Favorable timing
                earth=85,    # Defensive position
                command=90,  # Miltiades' leadership
                method=85    # Well-trained hoplites
            ),
            loser_position=StrategicPosition(
                name="Persian Empire",
                the_way=50,  # Imperial expansion
                heaven=60,   # Adequate timing
                earth=40,    # Poor positioning
                command=70,  # Adequate leadership
                method=80    # Well-organized but less motivated
            ),
            outcome_factors={
                'defensive_morale': 0.9,
                'tactical_advantage': 0.8,
                'leadership_quality': 0.7,
                'terrain_advantage': 0.6
            },
            lessons_learned=[
                "Defending homeland provides significant moral advantage",
                "Quality of troops can overcome numerical disadvantage",
                "Tactical positioning is crucial for success",
                "Leadership quality can be decisive in battle"
            ],
            source="Herodotus - Histories"
        ))
        
        return outcomes
    
    def _load_art_of_war_principles(self) -> Dict[str, Any]:
        """Load key Art of War principles for analysis."""
        return {
            "five_fundamentals": {
                "the_way": {
                    "description": "Moral influence and organizational culture",
                    "key_principles": [
                        "Alignment of purpose and values",
                        "Stakeholder engagement",
                        "Organizational commitment"
                    ],
                    "risk_factors": [
                        "Lack of clear purpose",
                        "Poor stakeholder alignment",
                        "Weak organizational culture"
                    ]
                },
                "heaven": {
                    "description": "Timing and external conditions",
                    "key_principles": [
                        "Market conditions and trends",
                        "Economic cycles",
                        "Seasonal patterns"
                    ],
                    "risk_factors": [
                        "Poor timing",
                        "Unfavorable conditions",
                        "Ignoring external factors"
                    ]
                },
                "earth": {
                    "description": "Terrain and positioning",
                    "key_principles": [
                        "Market positioning",
                        "Geographic advantage",
                        "Resource availability"
                    ],
                    "risk_factors": [
                        "Poor positioning",
                        "Resource constraints",
                        "Geographic disadvantage"
                    ]
                },
                "command": {
                    "description": "Leadership and decision-making",
                    "key_principles": [
                        "Strategic vision",
                        "Decision-making capability",
                        "Execution effectiveness"
                    ],
                    "risk_factors": [
                        "Poor leadership",
                        "Indecisive decision-making",
                        "Weak execution"
                    ]
                },
                "method": {
                    "description": "Organization and discipline",
                    "key_principles": [
                        "Systems and processes",
                        "Resource allocation",
                        "Operational excellence"
                    ],
                    "risk_factors": [
                        "Poor organization",
                        "Inefficient processes",
                        "Lack of discipline"
                    ]
                }
            },
            "risk_assessment_framework": {
                "low_risk": {"score_range": (80, 100), "description": "Strong strategic position"},
                "medium_risk": {"score_range": (60, 79), "description": "Moderate strategic position"},
                "high_risk": {"score_range": (40, 59), "description": "Weak strategic position"},
                "critical_risk": {"score_range": (0, 39), "description": "Critical strategic position"}
            }
        }
    
    def generate_current_strategic_position(self) -> StrategicPosition:
        """Generate a realistic current strategic position for analysis."""
        # This would typically come from actual strategic assessment
        # For demonstration, we'll create a realistic scenario
        
        return StrategicPosition(
            name="Current Strategic Position",
            the_way=75,   # Good organizational culture but room for improvement
            heaven=65,    # Mixed external conditions
            earth=80,     # Strong market positioning
            command=70,   # Adequate leadership
            method=85     # Well-organized operations
        )
    
    def run_monte_carlo_simulation(
        self,
        strategic_position: StrategicPosition,
        iterations: int = None,
        scenario_name: str = "Strategic Position Risk Assessment"
    ) -> MonteCarloResult:
        """
        Run Monte Carlo simulation to assess strategic position risk.
        
        Args:
            strategic_position: Current strategic position to assess
            iterations: Number of Monte Carlo iterations
            scenario_name: Name of the simulation scenario
            
        Returns:
            MonteCarloResult object with comprehensive analysis
        """
        iterations = iterations or self.default_iterations
        logger.info(f"Starting Monte Carlo simulation with {iterations} iterations")
        
        # Initialize results storage
        risk_scores = []
        success_probabilities = []
        failure_probabilities = []
        
        # Define probability distributions for each fundamental
        # Using beta distributions to model realistic uncertainty
        distributions = {
            'the_way': beta(2, 1, loc=strategic_position.the_way-20, scale=40),
            'heaven': beta(1.5, 1.5, loc=strategic_position.heaven-25, scale=50),
            'earth': beta(2, 1, loc=strategic_position.earth-15, scale=30),
            'command': beta(1.5, 1.5, loc=strategic_position.command-20, scale=40),
            'method': beta(2, 1, loc=strategic_position.method-10, scale=20)
        }
        
        # Run Monte Carlo iterations
        for i in range(iterations):
            # Generate random variations for each fundamental
            variations = {}
            for fundamental, dist in distributions.items():
                variations[fundamental] = np.clip(dist.rvs(), 0, 100)
            
            # Create simulated position
            simulated_position = StrategicPosition(
                name=f"Simulation {i+1}",
                the_way=variations['the_way'],
                heaven=variations['heaven'],
                earth=variations['earth'],
                command=variations['command'],
                method=variations['method']
            )
            
            # Calculate risk score
            risk_score = simulated_position.get_risk_score()
            risk_scores.append(risk_score)
            
            # Calculate success/failure probabilities
            overall_score = simulated_position.get_overall_score()
            success_prob = overall_score / 100.0
            failure_prob = 1.0 - success_prob
            
            success_probabilities.append(success_prob)
            failure_probabilities.append(failure_prob)
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(risk_scores)
        
        # Analyze risk distribution
        risk_distribution = self._analyze_risk_distribution(risk_scores)
        
        # Compare with historical outcomes
        historical_comparison = self._compare_with_historical_outcomes(
            strategic_position, risk_scores
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            strategic_position, risk_distribution, historical_comparison
        )
        
        return MonteCarloResult(
            scenario_name=scenario_name,
            iterations=iterations,
            risk_scores=risk_scores,
            success_probabilities=success_probabilities,
            failure_probabilities=failure_probabilities,
            confidence_intervals=confidence_intervals,
            risk_distribution=risk_distribution,
            historical_comparison=historical_comparison,
            recommendations=recommendations
        )
    
    def _calculate_confidence_intervals(self, risk_scores: List[float]) -> Dict[str, Tuple[float, float]]:
        """Calculate confidence intervals for risk assessment."""
        risk_scores = np.array(risk_scores)
        
        # Calculate percentiles for confidence intervals
        ci_95 = np.percentile(risk_scores, [2.5, 97.5])
        ci_90 = np.percentile(risk_scores, [5, 95])
        ci_80 = np.percentile(risk_scores, [10, 90])
        
        return {
            "95_percent": (float(ci_95[0]), float(ci_95[1])),
            "90_percent": (float(ci_90[0]), float(ci_90[1])),
            "80_percent": (float(ci_80[0]), float(ci_80[1])),
            "mean": float(np.mean(risk_scores)),
            "median": float(np.median(risk_scores)),
            "std": float(np.std(risk_scores))
        }
    
    def _analyze_risk_distribution(self, risk_scores: List[float]) -> Dict[str, float]:
        """Analyze the distribution of risk scores."""
        risk_scores = np.array(risk_scores)
        
        # Calculate risk categories
        low_risk = np.sum(risk_scores < 20) / len(risk_scores)
        medium_risk = np.sum((risk_scores >= 20) & (risk_scores < 40)) / len(risk_scores)
        high_risk = np.sum((risk_scores >= 40) & (risk_scores < 60)) / len(risk_scores)
        critical_risk = np.sum(risk_scores >= 60) / len(risk_scores)
        
        return {
            "low_risk_probability": float(low_risk),
            "medium_risk_probability": float(medium_risk),
            "high_risk_probability": float(high_risk),
            "critical_risk_probability": float(critical_risk),
            "overall_risk_level": self._determine_overall_risk_level(np.mean(risk_scores))
        }
    
    def _determine_overall_risk_level(self, mean_risk: float) -> str:
        """Determine overall risk level based on mean risk score."""
        if mean_risk < 20:
            return "Low Risk"
        elif mean_risk < 40:
            return "Medium Risk"
        elif mean_risk < 60:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def _compare_with_historical_outcomes(
        self,
        strategic_position: StrategicPosition,
        risk_scores: List[float]
    ) -> Dict[str, Any]:
        """Compare current position with historical strategic outcomes."""
        current_score = strategic_position.get_overall_score()
        mean_risk = np.mean(risk_scores)
        
        comparisons = []
        for outcome in self.historical_outcomes:
            victor_score = outcome.victor_position.get_overall_score()
            loser_score = outcome.loser_position.get_overall_score()
            
            comparison = {
                "conflict": outcome.conflict_name,
                "period": outcome.period,
                "current_vs_victor": current_score - victor_score,
                "current_vs_loser": current_score - loser_score,
                "victor_score": victor_score,
                "loser_score": loser_score,
                "current_score": current_score,
                "lessons_applicable": self._identify_applicable_lessons(
                    strategic_position, outcome
                )
            }
            comparisons.append(comparison)
        
        # Find most similar historical outcomes
        similar_outcomes = sorted(
            comparisons,
            key=lambda x: abs(x["current_vs_victor"]) + abs(x["current_vs_loser"])
        )[:3]
        
        return {
            "historical_comparisons": comparisons,
            "most_similar_outcomes": similar_outcomes,
            "average_victor_score": np.mean([c["victor_score"] for c in comparisons]),
            "average_loser_score": np.mean([c["loser_score"] for c in comparisons]),
            "current_position_relative": "above_average" if current_score > np.mean([c["victor_score"] for c in comparisons]) else "below_average"
        }
    
    def _identify_applicable_lessons(
        self,
        strategic_position: StrategicPosition,
        historical_outcome: HistoricalOutcome
    ) -> List[str]:
        """Identify which historical lessons are applicable to current position."""
        applicable_lessons = []
        
        # Compare current position with historical outcomes
        current_score = strategic_position.get_overall_score()
        victor_score = historical_outcome.victor_position.get_overall_score()
        loser_score = historical_outcome.loser_position.get_overall_score()
        
        # Identify applicable lessons based on position similarity
        for lesson in historical_outcome.lessons_learned:
            if "weather" in lesson.lower() and strategic_position.heaven < 70:
                applicable_lessons.append(lesson)
            elif "position" in lesson.lower() and strategic_position.earth < 75:
                applicable_lessons.append(lesson)
            elif "leadership" in lesson.lower() and strategic_position.command < 75:
                applicable_lessons.append(lesson)
            elif "organization" in lesson.lower() and strategic_position.method < 80:
                applicable_lessons.append(lesson)
            elif "morale" in lesson.lower() and strategic_position.the_way < 80:
                applicable_lessons.append(lesson)
        
        return applicable_lessons
    
    def _generate_recommendations(
        self,
        strategic_position: StrategicPosition,
        risk_distribution: Dict[str, float],
        historical_comparison: Dict[str, Any]
    ) -> List[str]:
        """Generate strategic recommendations based on analysis."""
        recommendations = []
        
        # Risk-based recommendations
        if risk_distribution["critical_risk_probability"] > 0.1:
            recommendations.append(
                "CRITICAL: Immediate action required to address strategic vulnerabilities. "
                "Focus on strengthening the weakest fundamentals first."
            )
        
        if risk_distribution["high_risk_probability"] > 0.3:
            recommendations.append(
                "HIGH RISK: Significant improvements needed in strategic position. "
                "Develop comprehensive risk mitigation strategies."
            )
        
        # Fundamental-specific recommendations
        if strategic_position.the_way < 80:
            recommendations.append(
                "Strengthen organizational culture and stakeholder alignment (The Way). "
                "Focus on clear communication of purpose and values."
            )
        
        if strategic_position.heaven < 70:
            recommendations.append(
                "Improve timing and external condition assessment (Heaven). "
                "Develop better environmental scanning and trend analysis capabilities."
            )
        
        if strategic_position.earth < 75:
            recommendations.append(
                "Enhance market positioning and resource availability (Earth). "
                "Reassess competitive landscape and resource allocation."
            )
        
        if strategic_position.command < 75:
            recommendations.append(
                "Strengthen leadership and decision-making capabilities (Command). "
                "Invest in leadership development and strategic planning processes."
            )
        
        if strategic_position.method < 80:
            recommendations.append(
                "Improve organizational systems and operational excellence (Method). "
                "Streamline processes and enhance operational discipline."
            )
        
        # Historical lesson-based recommendations
        for outcome in historical_comparison["most_similar_outcomes"]:
            for lesson in outcome.get("lessons_applicable", []):
                recommendations.append(f"Historical lesson: {lesson}")
        
        return recommendations
    
    def create_visualizations(self, result: MonteCarloResult, output_dir: str = "Results"):
        """Create comprehensive visualizations of the analysis."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'Strategic Position Risk Assessment: {result.scenario_name}', fontsize=16, fontweight='bold')
        
        # 1. Risk Score Distribution
        axes[0, 0].hist(result.risk_scores, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].axvline(np.mean(result.risk_scores), color='red', linestyle='--', label=f'Mean: {np.mean(result.risk_scores):.1f}')
        axes[0, 0].axvline(np.median(result.risk_scores), color='green', linestyle='--', label=f'Median: {np.median(result.risk_scores):.1f}')
        axes[0, 0].set_title('Risk Score Distribution')
        axes[0, 0].set_xlabel('Risk Score')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Success Probability Distribution
        axes[0, 1].hist(result.success_probabilities, bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].axvline(np.mean(result.success_probabilities), color='red', linestyle='--', 
                          label=f'Mean: {np.mean(result.success_probabilities):.3f}')
        axes[0, 1].set_title('Success Probability Distribution')
        axes[0, 1].set_xlabel('Success Probability')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Risk Level Breakdown
        risk_levels = ['Low', 'Medium', 'High', 'Critical']
        risk_probs = [
            result.risk_distribution['low_risk_probability'],
            result.risk_distribution['medium_risk_probability'],
            result.risk_distribution['high_risk_probability'],
            result.risk_distribution['critical_risk_probability']
        ]
        colors = ['green', 'yellow', 'orange', 'red']
        axes[0, 2].bar(risk_levels, risk_probs, color=colors, alpha=0.7)
        axes[0, 2].set_title('Risk Level Probability Distribution')
        axes[0, 2].set_ylabel('Probability')
        axes[0, 2].set_ylim(0, 1)
        for i, v in enumerate(risk_probs):
            axes[0, 2].text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
        
        # 4. Historical Comparison
        historical_data = result.historical_comparison['historical_comparisons']
        conflicts = [h['conflict'] for h in historical_data]
        current_scores = [h['current_score'] for h in historical_data]
        victor_scores = [h['victor_score'] for h in historical_data]
        loser_scores = [h['loser_score'] for h in historical_data]
        
        x = np.arange(len(conflicts))
        width = 0.25
        
        axes[1, 0].bar(x - width, current_scores, width, label='Current Position', alpha=0.7)
        axes[1, 0].bar(x, victor_scores, width, label='Historical Victors', alpha=0.7)
        axes[1, 0].bar(x + width, loser_scores, width, label='Historical Losers', alpha=0.7)
        axes[1, 0].set_title('Historical Strategic Position Comparison')
        axes[1, 0].set_xlabel('Historical Conflicts')
        axes[1, 0].set_ylabel('Strategic Score')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels([c[:15] + '...' if len(c) > 15 else c for c in conflicts], rotation=45)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Confidence Intervals
        ci_data = result.confidence_intervals
        intervals = ['80%', '90%', '95%']
        lower_bounds = [ci_data['80_percent'][0], ci_data['90_percent'][0], ci_data['95_percent'][0]]
        upper_bounds = [ci_data['80_percent'][1], ci_data['90_percent'][1], ci_data['95_percent'][1]]
        
        axes[1, 1].errorbar(intervals, [ci_data['mean']] * 3, 
                           yerr=[[ci_data['mean'] - lb for lb in lower_bounds], 
                                 [ub - ci_data['mean'] for ub in upper_bounds]],
                           fmt='o', capsize=5, capthick=2, markersize=8)
        axes[1, 1].set_title('Risk Score Confidence Intervals')
        axes[1, 1].set_ylabel('Risk Score')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Art of War Five Fundamentals
        # This would be populated with the current strategic position data
        fundamentals = ['The Way', 'Heaven', 'Earth', 'Command', 'Method']
        # For demonstration, using placeholder values
        scores = [75, 65, 80, 70, 85]  # These would come from the actual strategic position
        
        axes[1, 2].bar(fundamentals, scores, color='lightblue', alpha=0.7)
        axes[1, 2].set_title('Art of War Five Fundamentals Assessment')
        axes[1, 2].set_ylabel('Score (0-100)')
        axes[1, 2].set_ylim(0, 100)
        for i, v in enumerate(scores):
            axes[1, 2].text(i, v + 1, f'{v}', ha='center', va='bottom')
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save visualization
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"strategic_position_risk_assessment_{timestamp}.png"
        plt.savefig(output_path / filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualization saved: {output_path / filename}")
        return str(output_path / filename)
    
    def generate_report(self, result: MonteCarloResult, output_dir: str = "Results") -> str:
        """Generate comprehensive analysis report."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"strategic_position_risk_assessment_report_{timestamp}.md"
        report_path = output_path / filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Strategic Position Risk Assessment Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Scenario**: {result.scenario_name}\n")
            f.write(f"**Iterations**: {result.iterations:,}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write(f"The Monte Carlo simulation analysis of our current strategic position reveals a **{result.risk_distribution['overall_risk_level']}** assessment.\n\n")
            
            f.write("### Key Findings\n\n")
            f.write(f"- **Overall Risk Level**: {result.risk_distribution['overall_risk_level']}\n")
            f.write(f"- **Mean Risk Score**: {result.confidence_intervals['mean']:.1f}\n")
            f.write(f"- **Risk Score Range (95% CI)**: {result.confidence_intervals['95_percent'][0]:.1f} - {result.confidence_intervals['95_percent'][1]:.1f}\n")
            f.write(f"- **Success Probability**: {np.mean(result.success_probabilities):.1%}\n")
            f.write(f"- **Failure Probability**: {np.mean(result.failure_probabilities):.1%}\n\n")
            
            f.write("### Risk Distribution\n\n")
            f.write(f"- **Low Risk**: {result.risk_distribution['low_risk_probability']:.1%}\n")
            f.write(f"- **Medium Risk**: {result.risk_distribution['medium_risk_probability']:.1%}\n")
            f.write(f"- **High Risk**: {result.risk_distribution['high_risk_probability']:.1%}\n")
            f.write(f"- **Critical Risk**: {result.risk_distribution['critical_risk_probability']:.1%}\n\n")
            
            f.write("## Historical Comparison Analysis\n\n")
            f.write("### Comparison with Historical Strategic Outcomes\n\n")
            
            for comparison in result.historical_comparison['historical_comparisons']:
                f.write(f"#### {comparison['conflict']} ({comparison['period']})\n\n")
                f.write(f"- **Current Position Score**: {comparison['current_score']:.1f}\n")
                f.write(f"- **Victor Score**: {comparison['victor_score']:.1f}\n")
                f.write(f"- **Loser Score**: {comparison['loser_score']:.1f}\n")
                f.write(f"- **Position vs Victor**: {comparison['current_vs_victor']:+.1f}\n")
                f.write(f"- **Position vs Loser**: {comparison['current_vs_loser']:+.1f}\n\n")
                
                if comparison['lessons_applicable']:
                    f.write("**Applicable Lessons**:\n")
                    for lesson in comparison['lessons_applicable']:
                        f.write(f"- {lesson}\n")
                    f.write("\n")
            
            f.write("### Most Similar Historical Outcomes\n\n")
            for i, outcome in enumerate(result.historical_comparison['most_similar_outcomes'], 1):
                f.write(f"{i}. **{outcome['conflict']}** - Current position differs by {abs(outcome['current_vs_victor']):.1f} points from victor\n")
            
            f.write("\n## Art of War Principles Analysis\n\n")
            f.write("### Five Fundamentals Assessment\n\n")
            
            # This would be populated with actual strategic position data
            fundamentals = {
                "The Way (道)": "Moral influence and organizational culture",
                "Heaven (天)": "Timing and external conditions", 
                "Earth (地)": "Terrain and positioning",
                "Command (将)": "Leadership and decision-making",
                "Method (法)": "Organization and discipline"
            }
            
            for fundamental, description in fundamentals.items():
                f.write(f"#### {fundamental}\n")
                f.write(f"**Description**: {description}\n")
                f.write("**Assessment**: [To be populated with actual data]\n\n")
            
            f.write("## Strategic Recommendations\n\n")
            f.write("### Priority Actions\n\n")
            
            for i, recommendation in enumerate(result.recommendations, 1):
                f.write(f"{i}. {recommendation}\n")
            
            f.write("\n### Risk Mitigation Strategies\n\n")
            f.write("Based on the Monte Carlo simulation results and historical comparisons:\n\n")
            
            if result.risk_distribution['critical_risk_probability'] > 0.1:
                f.write("**CRITICAL PRIORITY**: Immediate action required to address strategic vulnerabilities.\n\n")
            
            if result.risk_distribution['high_risk_probability'] > 0.3:
                f.write("**HIGH PRIORITY**: Significant improvements needed in strategic position.\n\n")
            
            f.write("## Methodology\n\n")
            f.write("### Monte Carlo Simulation Parameters\n\n")
            f.write(f"- **Iterations**: {result.iterations:,}\n")
            f.write(f"- **Confidence Level**: {self.confidence_level:.0%}\n")
            f.write(f"- **Distribution Type**: Beta distributions for realistic uncertainty modeling\n")
            f.write(f"- **Risk Calculation**: Inverse of strategic strength score\n\n")
            
            f.write("### Historical Data Sources\n\n")
            f.write("- **Art of War**: Sun Tzu's strategic principles and historical examples\n")
            f.write("- **War and Peace**: Tolstoy's analysis of Napoleon's Russian campaign\n")
            f.write("- **Classical Histories**: Herodotus and other classical sources\n\n")
            
            f.write("## Conclusion\n\n")
            f.write("This analysis provides a comprehensive assessment of our current strategic position ")
            f.write("using Monte Carlo simulation and historical strategic outcomes from classical literature. ")
            f.write("The results should inform strategic planning and risk mitigation efforts.\n\n")
            
            f.write("**Next Steps**:\n")
            f.write("1. Review and validate the strategic position assessment\n")
            f.write("2. Implement priority recommendations\n")
            f.write("3. Establish monitoring mechanisms for key risk indicators\n")
            f.write("4. Conduct regular reassessment using this framework\n")
        
        logger.info(f"Report generated: {report_path}")
        return str(report_path)
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run the complete strategic position risk assessment."""
        logger.info("Starting comprehensive strategic position risk assessment")
        
        # Generate current strategic position
        current_position = self.generate_current_strategic_position()
        
        # Run Monte Carlo simulation
        result = self.run_monte_carlo_simulation(
            strategic_position=current_position,
            scenario_name="Comprehensive Strategic Position Risk Assessment"
        )
        
        # Create visualizations
        viz_path = self.create_visualizations(result)
        
        # Generate report
        report_path = self.generate_report(result)
        
        # Save results as JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"strategic_position_risk_assessment_{timestamp}.json"
        json_path = Path("Results") / json_filename
        
        # Convert result to JSON-serializable format
        result_dict = asdict(result)
        result_dict['current_position'] = asdict(current_position)
        result_dict['visualization_path'] = viz_path
        result_dict['report_path'] = report_path
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, default=str)
        
        logger.info(f"Complete analysis results saved: {json_path}")
        
        # Print summary
        print("\n" + "="*80)
        print("STRATEGIC POSITION RISK ASSESSMENT COMPLETED")
        print("="*80)
        print(f"Overall Risk Level: {result.risk_distribution['overall_risk_level']}")
        print(f"Mean Risk Score: {result.confidence_intervals['mean']:.1f}")
        print(f"Success Probability: {np.mean(result.success_probabilities):.1%}")
        print(f"Critical Risk Probability: {result.risk_distribution['critical_risk_probability']:.1%}")
        print(f"\nFiles Generated:")
        print(f"- Analysis Results: {json_path}")
        print(f"- Visualization: {viz_path}")
        print(f"- Report: {report_path}")
        print("="*80)
        
        return {
            "result": result,
            "current_position": current_position,
            "json_path": str(json_path),
            "visualization_path": viz_path,
            "report_path": report_path
        }

def main():
    """Main function to run the strategic position risk assessment."""
    print("🎯 STRATEGIC POSITION RISK ASSESSMENT")
    print("="*70)
    print("Monte Carlo Simulation with Historical Strategic Outcomes")
    print("="*70)
    
    # Initialize assessor
    assessor = StrategicPositionRiskAssessor()
    
    # Run complete analysis
    analysis_results = assessor.run_complete_analysis()
    
    print("\n✅ Analysis completed successfully!")
    print("📊 Check the generated files for detailed results and recommendations.")
    
    return analysis_results

if __name__ == "__main__":
    main()
