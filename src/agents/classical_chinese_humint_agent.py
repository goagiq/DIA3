"""
Classical Chinese HUMINT Analysis Agent

This agent provides specialized analysis capabilities for Classical Chinese content
in HUMINT (Human Intelligence) collection applications, including:

1. Classical Chinese pattern detection
2. Strategic deception monitoring
3. Cultural intelligence analysis
4. Source assessment capabilities
5. The Art of War principle recognition

Follows the Design Framework patterns and integrates with the existing agent swarm.
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from loguru import logger

from src.agents.base_agent import StrandsBaseAgent
from src.core.models import (
    AnalysisRequest, AnalysisResult, DataType, 
    SentimentResult, SentimentLabel
)
from src.config.language_config.chinese_config import ChineseConfig


@dataclass
class ClassicalChineseAnalysis:
    """Results of Classical Chinese pattern analysis."""
    classical_score: float = 0.0
    strategic_indicators: List[Dict[str, Any]] = field(default_factory=list)
    deception_patterns: List[Dict[str, Any]] = field(default_factory=list)
    cultural_values: List[Dict[str, Any]] = field(default_factory=list)
    formality_level: str = "unknown"
    strategic_intent: str = "unknown"


@dataclass
class HUMINTImplications:
    """HUMINT implications analysis results."""
    source_assessment: Dict[str, Any] = field(default_factory=dict)
    deception_risk: Dict[str, Any] = field(default_factory=dict)
    cultural_intelligence: Dict[str, Any] = field(default_factory=dict)
    operational_recommendations: List[str] = field(default_factory=list)


class ClassicalChineseHUMINTAnalyzer:
    """Core analyzer for Classical Chinese content in HUMINT applications."""
    
    def __init__(self):
        self.chinese_config = ChineseConfig()
        
        # Classical Chinese strategic indicators from The Art of War
        self.classical_strategic_indicators = {
            "deception_principles": [
                "能而示之不能",  # Show inability when capable
                "用而示之不用",  # Show disuse when using
                "近而示之遠",    # Show distance when near
                "遠而示之近",    # Show nearness when far
                "利而誘之",      # Lure with profit
                "亂而取之",      # Take advantage of chaos
                "實而備之",      # Prepare against strength
                "強而避之",      # Avoid the strong
                "怒而撓之",      # Provoke when angry
                "卑而驕之",      # Make proud when humble
                "佚而勞之",      # Tire when rested
                "親而離之"       # Separate when close
            ],
            "strategic_concepts": [
                "兵者，詭道也",   # War is the way of deception
                "攻其無備，出其不意",  # Attack unprepared, appear unexpected
                "知己知彼，百戰不殆",  # Know yourself and enemy, win every battle
                "上兵伐謀",       # Supreme art: subdue without fighting
                "不戰而屈人之兵", # Subdue enemy without fighting
                "善戰者，求之於勢", # Good warriors seek victory through momentum
                "勢者，因利而制權也"  # Momentum uses advantage to control power
            ],
            "cultural_values": [
                "仁", "义", "礼", "智", "信",  # Classical virtues
                "忠", "孝", "悌", "节", "廉",  # Additional virtues
                "道", "德", "理", "气",        # Philosophical concepts
                "阴阳", "五行", "八卦", "太极"  # Traditional concepts
            ]
        }
    
    def detect_classical_chinese_patterns(self, text: str) -> ClassicalChineseAnalysis:
        """Detect Classical Chinese patterns in text."""
        results = ClassicalChineseAnalysis()
        
        # Check for Classical Chinese particles
        classical_particles = r'之|其|者|也|乃|是|于|以|为|所|所以|而|则|故|然'
        particle_matches = re.findall(classical_particles, text)
        if particle_matches:
            results.classical_score += len(particle_matches) * 0.1
            results.formality_level = "high"
        
        # Check for strategic deception indicators
        for indicator in self.classical_strategic_indicators["deception_principles"]:
            if indicator in text:
                results.strategic_indicators.append({
                    "type": "deception_principle",
                    "text": indicator,
                    "significance": "high"
                })
                results.classical_score += 0.3
        
        # Check for strategic concepts
        for concept in self.classical_strategic_indicators["strategic_concepts"]:
            if concept in text:
                results.strategic_indicators.append({
                    "type": "strategic_concept",
                    "text": concept,
                    "significance": "critical"
                })
                results.classical_score += 0.5
        
        # Check for cultural values
        for value in self.classical_strategic_indicators["cultural_values"]:
            if value in text:
                results.cultural_values.append({
                    "value": value,
                    "context": "classical_chinese"
                })
                results.classical_score += 0.1
        
        # Determine strategic intent
        if results.classical_score > 0.5:
            results.strategic_intent = "high"
        elif results.classical_score > 0.2:
            results.strategic_intent = "medium"
        else:
            results.strategic_intent = "low"
        
        return results
    
    def analyze_humint_implications(self, classical_analysis: ClassicalChineseAnalysis) -> HUMINTImplications:
        """Analyze HUMINT implications of Classical Chinese usage."""
        implications = HUMINTImplications()
        
        # Source assessment
        if classical_analysis.classical_score > 0.5:
            implications.source_assessment = {
                "cultural_authenticity": "high",
                "education_level": "likely_educated",
                "strategic_knowledge": "likely_high",
                "motivation_indicators": ["strategic_communication", "cultural_display"]
            }
        elif classical_analysis.classical_score > 0.2:
            implications.source_assessment = {
                "cultural_authenticity": "medium",
                "education_level": "possibly_educated",
                "strategic_knowledge": "possibly_high",
                "motivation_indicators": ["cultural_reference", "formal_communication"]
            }
        else:
            implications.source_assessment = {
                "cultural_authenticity": "low",
                "education_level": "unknown",
                "strategic_knowledge": "unknown",
                "motivation_indicators": ["minimal_cultural_knowledge"]
            }
        
        # Deception risk assessment
        deception_indicators = classical_analysis.strategic_indicators
        if any(ind["type"] == "deception_principle" for ind in deception_indicators):
            implications.deception_risk = {
                "risk_level": "high",
                "indicators": [ind["text"] for ind in deception_indicators if ind["type"] == "deception_principle"],
                "recommendations": [
                    "Monitor for strategic misdirection",
                    "Validate source authenticity",
                    "Cross-reference with other intelligence sources"
                ]
            }
        elif classical_analysis.strategic_intent == "high":
            implications.deception_risk = {
                "risk_level": "medium",
                "indicators": ["High strategic intent detected"],
                "recommendations": [
                    "Assess source motivations",
                    "Monitor for strategic patterns",
                    "Validate cultural authenticity"
                ]
            }
        else:
            implications.deception_risk = {
                "risk_level": "low",
                "indicators": ["Minimal strategic indicators"],
                "recommendations": ["Standard source validation procedures"]
            }
        
        # Cultural intelligence
        implications.cultural_intelligence = {
            "cultural_depth": "high" if classical_analysis.cultural_values else "low",
            "strategic_culture": "evident" if classical_analysis.strategic_indicators else "not_evident",
            "communication_style": classical_analysis.formality_level,
            "cultural_signals": classical_analysis.cultural_values
        }
        
        # Operational recommendations
        if implications.deception_risk["risk_level"] == "high":
            implications.operational_recommendations.extend([
                "Implement enhanced source validation",
                "Monitor for strategic deception patterns",
                "Cross-reference with cultural intelligence databases",
                "Assess source motivations through cultural lens"
            ])
        
        if implications.source_assessment["cultural_authenticity"] == "high":
            implications.operational_recommendations.extend([
                "Leverage cultural knowledge for relationship building",
                "Use Classical Chinese knowledge for source assessment",
                "Monitor for strategic communication patterns"
            ])
        
        return implications


class ClassicalChineseHUMINTAnalysisAgent(StrandsBaseAgent):
    """
    Agent for Classical Chinese HUMINT analysis.
    
    Capabilities:
    - Classical Chinese pattern detection
    - Strategic deception monitoring
    - Cultural intelligence analysis
    - Source assessment capabilities
    - The Art of War principle recognition
    """
    
    def __init__(self, model_name: Optional[str] = None, **kwargs):
        super().__init__(model_name=model_name or "qwen2.5:7b", **kwargs)
        
        # Initialize analyzer
        self.analyzer = ClassicalChineseHUMINTAnalyzer()
        
        # Set metadata
        self.metadata["agent_type"] = "classical_chinese_humint_analysis"
        self.metadata["capabilities"] = [
            "classical_chinese_pattern_detection",
            "strategic_deception_monitoring",
            "cultural_intelligence_analysis",
            "source_assessment",
            "art_of_war_principle_recognition"
        ]
        self.metadata["supported_data_types"] = [
            "text", "document", "communication"
        ]
        
        logger.info("ClassicalChineseHUMINTAnalysisAgent initialized successfully")
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        # Can process text content, especially Chinese text
        if request.data_type == DataType.TEXT:
            return True
        
        # Can process documents that might contain Classical Chinese
        if request.data_type in [DataType.PDF]:
            return True
        
        return False
    
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process Classical Chinese content for HUMINT analysis."""
        try:
            logger.info("Starting Classical Chinese HUMINT analysis...")
            
            # Extract content
            content = request.content
            if not content:
                raise ValueError("No content provided for analysis")
            
            # Perform Classical Chinese pattern detection
            logger.info("Detecting Classical Chinese patterns...")
            classical_analysis = self.analyzer.detect_classical_chinese_patterns(content)
            
            # Analyze HUMINT implications
            logger.info("Analyzing HUMINT implications...")
            humint_implications = self.analyzer.analyze_humint_implications(classical_analysis)
            
            # Generate comprehensive analysis results
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "source_info": request.metadata or {},
                "classical_chinese_analysis": {
                    "classical_score": classical_analysis.classical_score,
                    "strategic_indicators": classical_analysis.strategic_indicators,
                    "deception_patterns": classical_analysis.deception_patterns,
                    "cultural_values": classical_analysis.cultural_values,
                    "formality_level": classical_analysis.formality_level,
                    "strategic_intent": classical_analysis.strategic_intent
                },
                "humint_implications": {
                    "source_assessment": humint_implications.source_assessment,
                    "deception_risk": humint_implications.deception_risk,
                    "cultural_intelligence": humint_implications.cultural_intelligence,
                    "operational_recommendations": humint_implications.operational_recommendations
                },
                "recommendations": []
            }
            
            # Generate recommendations
            recommendations = []
            
            # Based on Classical Chinese analysis
            if classical_analysis.strategic_intent == "high":
                recommendations.append({
                    "priority": "high",
                    "category": "source_assessment",
                    "recommendation": "Implement enhanced source validation due to high strategic intent"
                })
            
            if classical_analysis.classical_score > 0.5:
                recommendations.append({
                    "priority": "medium",
                    "category": "cultural_intelligence",
                    "recommendation": "Leverage Classical Chinese knowledge for source relationship building"
                })
            
            analysis_results["recommendations"] = recommendations
            
            # Create sentiment result (required by AnalysisResult)
            sentiment_result = SentimentResult(
                label=SentimentLabel.NEUTRAL,  # Default for HUMINT analysis
                confidence=0.8,
                reasoning="Classical Chinese HUMINT analysis completed",
                context_notes="Analysis focused on strategic deception and cultural intelligence"
            )
            
            # Create analysis result
            result = AnalysisResult(
                request_id=request.id,
                data_type=request.data_type,
                sentiment=sentiment_result,
                processing_time=0.1,  # Placeholder
                raw_content=content,
                metadata={
                    "agent": "ClassicalChineseHUMINTAnalysisAgent",
                    "analysis_type": "classical_chinese_humint",
                    "classical_score": classical_analysis.classical_score,
                    "strategic_intent": classical_analysis.strategic_intent,
                    "deception_risk_level": humint_implications.deception_risk["risk_level"],
                    "cultural_authenticity": humint_implications.source_assessment["cultural_authenticity"],
                    "analysis_results": analysis_results
                }
            )
            
            logger.info("✅ Classical Chinese HUMINT analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error during Classical Chinese HUMINT analysis: {e}")
            raise
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a formatted HUMINT analysis report."""
        report = []
        report.append("# Classical Chinese HUMINT Analysis Report")
        report.append(f"**Analysis Date:** {analysis_results['timestamp']}")
        report.append("")
        
        # Source Information
        if analysis_results.get("source_info"):
            report.append("## Source Information")
            for key, value in analysis_results["source_info"].items():
                report.append(f"- **{key}:** {value}")
            report.append("")
        
        # Classical Chinese Analysis
        classical_analysis = analysis_results.get("classical_chinese_analysis", {})
        report.append("## Classical Chinese Analysis")
        report.append(f"- **Classical Score:** {classical_analysis.get('classical_score', 0):.2f}")
        report.append(f"- **Formality Level:** {classical_analysis.get('formality_level', 'unknown')}")
        report.append(f"- **Strategic Intent:** {classical_analysis.get('strategic_intent', 'unknown')}")
        
        if classical_analysis.get("strategic_indicators"):
            report.append("- **Strategic Indicators:**")
            for indicator in classical_analysis["strategic_indicators"]:
                report.append(f"  - {indicator['text']} ({indicator['type']})")
        
        if classical_analysis.get("cultural_values"):
            report.append("- **Cultural Values:**")
            for value in classical_analysis["cultural_values"]:
                report.append(f"  - {value['value']}")
        
        report.append("")
        
        # HUMINT Implications
        humint_implications = analysis_results.get("humint_implications", {})
        report.append("## HUMINT Implications")
        
        source_assessment = humint_implications.get("source_assessment", {})
        report.append("### Source Assessment")
        for key, value in source_assessment.items():
            report.append(f"- **{key}:** {value}")
        
        deception_risk = humint_implications.get("deception_risk", {})
        report.append("### Deception Risk Assessment")
        report.append(f"- **Risk Level:** {deception_risk.get('risk_level', 'unknown')}")
        if deception_risk.get("indicators"):
            report.append("- **Risk Indicators:**")
            for indicator in deception_risk["indicators"]:
                report.append(f"  - {indicator}")
        
        cultural_intelligence = humint_implications.get("cultural_intelligence", {})
        report.append("### Cultural Intelligence")
        for key, value in cultural_intelligence.items():
            report.append(f"- **{key}:** {value}")
        
        report.append("")
        
        # Recommendations
        recommendations = analysis_results.get("recommendations", [])
        if recommendations:
            report.append("## Operational Recommendations")
            for rec in recommendations:
                report.append(f"- **[{rec['priority'].upper()}] {rec['category']}: {rec['recommendation']}")
        
        return "\n".join(report)
