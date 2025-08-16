"""
Strategic Analysis MCP Server
Integrates Art of War principles with modern analytics for defense, intelligence, 
and business applications.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List
from dataclasses import dataclass
from enum import Enum

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    Tool,
    TextContent,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DomainType(Enum):
    """Supported domain types for strategic analysis."""
    MILITARY = "military"
    INTELLIGENCE = "intelligence"
    BUSINESS = "business"
    CYBERSECURITY = "cybersecurity"
    DIPLOMATIC = "diplomatic"

class ArtOfWarPrinciple(Enum):
    """Core Art of War principles for analysis."""
    THE_WAY = "道"  # Moral influence and alignment
    HEAVEN = "天"   # Timing and conditions
    EARTH = "地"    # Terrain and position
    COMMAND = "将"  # Leadership and decision-making
    METHOD = "法"   # Organization and discipline
    DECEPTION = "詭道"  # Deception and misdirection
    RESOURCE_MANAGEMENT = "资源管理"  # Resource allocation and efficiency
    INTELLIGENCE = "情报"  # Information and intelligence
    ALLIANCE_MANAGEMENT = "联盟管理"  # Coalition and partnership management

@dataclass
class StrategicAssessment:
    """Comprehensive strategic assessment result."""
    domain: str
    assessment_date: str
    five_fundamentals: Dict[str, float]
    deception_analysis: Dict[str, Any]
    resource_assessment: Dict[str, Any]
    intelligence_capabilities: Dict[str, Any]
    alliance_analysis: Dict[str, Any]
    recommendations: List[str]
    risk_factors: List[str]
    opportunities: List[str]
    confidence_score: float

@dataclass
class DomainConfiguration:
    """Configuration for different domains."""
    domain_type: DomainType
    assessment_weights: Dict[str, float]
    key_metrics: List[str]
    risk_thresholds: Dict[str, float]
    reporting_templates: Dict[str, str]

class StrategicAnalysisEngine:
    """Core engine for strategic analysis using Art of War principles."""
    
    def __init__(self):
        self.domain_configs = self._initialize_domain_configurations()
        
    def _initialize_domain_configurations(self) -> Dict[DomainType, DomainConfiguration]:
        """Initialize domain-specific configurations."""
        configs = {}
        
        # Military/Defense Configuration
        configs[DomainType.MILITARY] = DomainConfiguration(
            domain_type=DomainType.MILITARY,
            assessment_weights={
                "the_way": 0.20,  # Morale and political support
                "heaven": 0.15,   # Weather and timing
                "earth": 0.25,    # Terrain and positioning
                "command": 0.20,  # Leadership and decision-making
                "method": 0.20,   # Organization and discipline
            },
            key_metrics=[
                "force_strength", "logistics_capability", "intelligence_superiority",
                "alliance_support", "technological_advantage", "economic_sustainability"
            ],
            risk_thresholds={
                "resource_shortage": 0.7,
                "intelligence_gap": 0.6,
                "alliance_fragmentation": 0.8,
                "technological_disadvantage": 0.7
            },
            reporting_templates={
                "executive_summary": "military_executive_summary.md",
                "detailed_analysis": "military_detailed_analysis.md",
                "recommendations": "military_recommendations.md"
            }
        )
        
        # Intelligence Configuration
        configs[DomainType.INTELLIGENCE] = DomainConfiguration(
            domain_type=DomainType.INTELLIGENCE,
            assessment_weights={
                "the_way": 0.15,  # Organizational culture
                "heaven": 0.20,   # Timing and conditions
                "earth": 0.15,    # Geographic and cyber terrain
                "command": 0.25,  # Leadership and coordination
                "method": 0.25,   # Processes and capabilities
            },
            key_metrics=[
                "collection_capability", "analysis_quality", "counterintelligence",
                "technical_superiority", "human_intelligence", "all_source_integration"
            ],
            risk_thresholds={
                "intelligence_gap": 0.6,
                "counterintelligence_breach": 0.8,
                "technical_disadvantage": 0.7,
                "coordination_failure": 0.7
            },
            reporting_templates={
                "executive_summary": "intelligence_executive_summary.md",
                "detailed_analysis": "intelligence_detailed_analysis.md",
                "recommendations": "intelligence_recommendations.md"
            }
        )
        
        # Business Configuration
        configs[DomainType.BUSINESS] = DomainConfiguration(
            domain_type=DomainType.BUSINESS,
            assessment_weights={
                "the_way": 0.25,  # Corporate culture and values
                "heaven": 0.20,   # Market conditions and timing
                "earth": 0.20,    # Market position and geography
                "command": 0.20,  # Leadership and management
                "method": 0.15,   # Operations and efficiency
            },
            key_metrics=[
                "market_position", "competitive_advantage", "financial_strength",
                "operational_efficiency", "innovation_capability", "stakeholder_support"
            ],
            risk_thresholds={
                "market_share_loss": 0.7,
                "competitive_disadvantage": 0.6,
                "financial_stress": 0.8,
                "operational_inefficiency": 0.7
            },
            reporting_templates={
                "executive_summary": "business_executive_summary.md",
                "detailed_analysis": "business_detailed_analysis.md",
                "recommendations": "business_recommendations.md"
            }
        )
        
        # Cybersecurity Configuration
        configs[DomainType.CYBERSECURITY] = DomainConfiguration(
            domain_type=DomainType.CYBERSECURITY,
            assessment_weights={
                "the_way": 0.20,  # Security culture
                "heaven": 0.15,   # Threat landscape and timing
                "earth": 0.25,    # Digital terrain and infrastructure
                "command": 0.20,  # Security leadership
                "method": 0.20,   # Security processes and tools
            },
            key_metrics=[
                "threat_intelligence", "defensive_capability", "incident_response",
                "vulnerability_management", "security_awareness", "technical_controls"
            ],
            risk_thresholds={
                "vulnerability_exposure": 0.8,
                "threat_intelligence_gap": 0.7,
                "incident_response_delay": 0.6,
                "security_control_failure": 0.8
            },
            reporting_templates={
                "executive_summary": "cybersecurity_executive_summary.md",
                "detailed_analysis": "cybersecurity_detailed_analysis.md",
                "recommendations": "cybersecurity_recommendations.md"
            }
        )
        
        return configs
    
    def analyze_five_fundamentals(self, data: Dict[str, Any], domain: DomainType) -> Dict[str, float]:
        """Analyze the five fundamental factors from Art of War."""
        config = self.domain_configs[domain]
        weights = config.assessment_weights
        
        # Extract relevant metrics for each fundamental
        fundamentals = {}
        
        # The Way (道) - Moral influence and alignment
        if domain == DomainType.MILITARY:
            fundamentals["the_way"] = self._calculate_military_morale(data)
        elif domain == DomainType.INTELLIGENCE:
            fundamentals["the_way"] = self._calculate_intelligence_culture(data)
        elif domain == DomainType.BUSINESS:
            fundamentals["the_way"] = self._calculate_business_culture(data)
        elif domain == DomainType.CYBERSECURITY:
            fundamentals["the_way"] = self._calculate_security_culture(data)
        
        # Heaven (天) - Timing and conditions
        fundamentals["heaven"] = self._calculate_timing_conditions(data, domain)
        
        # Earth (地) - Terrain and position
        fundamentals["earth"] = self._calculate_terrain_position(data, domain)
        
        # Command (将) - Leadership and decision-making
        fundamentals["command"] = self._calculate_leadership_effectiveness(data, domain)
        
        # Method (法) - Organization and discipline
        fundamentals["method"] = self._calculate_organizational_discipline(data, domain)
        
        # Apply domain-specific weights
        weighted_fundamentals = {}
        for key, value in fundamentals.items():
            weighted_fundamentals[key] = value * weights.get(key, 0.2)
        
        return weighted_fundamentals
    
    def _calculate_military_morale(self, data: Dict[str, Any]) -> float:
        """Calculate military morale and political support."""
        factors = [
            data.get("political_support", 0.5),
            data.get("public_opinion", 0.5),
            data.get("troop_morale", 0.5),
            data.get("alliance_support", 0.5)
        ]
        return sum(factors) / len(factors)
    
    def _calculate_intelligence_culture(self, data: Dict[str, Any]) -> float:
        """Calculate intelligence organizational culture."""
        factors = [
            data.get("information_sharing", 0.5),
            data.get("collaboration_culture", 0.5),
            data.get("security_awareness", 0.5),
            data.get("innovation_mindset", 0.5)
        ]
        return sum(factors) / len(factors)
    
    def _calculate_business_culture(self, data: Dict[str, Any]) -> float:
        """Calculate business organizational culture."""
        factors = [
            data.get("employee_engagement", 0.5),
            data.get("stakeholder_alignment", 0.5),
            data.get("ethical_standards", 0.5),
            data.get("innovation_culture", 0.5)
        ]
        return sum(factors) / len(factors)
    
    def _calculate_security_culture(self, data: Dict[str, Any]) -> float:
        """Calculate cybersecurity culture."""
        factors = [
            data.get("security_awareness", 0.5),
            data.get("compliance_culture", 0.5),
            data.get("incident_reporting", 0.5),
            data.get("continuous_improvement", 0.5)
        ]
        return sum(factors) / len(factors)
    
    def _calculate_timing_conditions(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Calculate timing and conditions factor."""
        if domain == DomainType.MILITARY:
            factors = [
                data.get("weather_conditions", 0.5),
                data.get("seasonal_factors", 0.5),
                data.get("political_timing", 0.5)
            ]
        elif domain == DomainType.INTELLIGENCE:
            factors = [
                data.get("threat_landscape", 0.5),
                data.get("technological_timing", 0.5),
                data.get("political_conditions", 0.5)
            ]
        elif domain == DomainType.BUSINESS:
            factors = [
                data.get("market_conditions", 0.5),
                data.get("economic_cycle", 0.5),
                data.get("competitive_timing", 0.5)
            ]
        elif domain == DomainType.CYBERSECURITY:
            factors = [
                data.get("threat_landscape", 0.5),
                data.get("vulnerability_disclosure", 0.5),
                data.get("regulatory_timing", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5]
        
        return sum(factors) / len(factors)
    
    def _calculate_terrain_position(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Calculate terrain and position factor."""
        if domain == DomainType.MILITARY:
            factors = [
                data.get("geographic_advantage", 0.5),
                data.get("strategic_position", 0.5),
                data.get("logistics_network", 0.5)
            ]
        elif domain == DomainType.INTELLIGENCE:
            factors = [
                data.get("geographic_coverage", 0.5),
                data.get("cyber_terrain", 0.5),
                data.get("access_points", 0.5)
            ]
        elif domain == DomainType.BUSINESS:
            factors = [
                data.get("market_position", 0.5),
                data.get("geographic_presence", 0.5),
                data.get("supply_chain_position", 0.5)
            ]
        elif domain == DomainType.CYBERSECURITY:
            factors = [
                data.get("network_architecture", 0.5),
                data.get("digital_terrain", 0.5),
                data.get("security_perimeter", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5]
        
        return sum(factors) / len(factors)
    
    def _calculate_leadership_effectiveness(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Calculate leadership and decision-making effectiveness."""
        if domain == DomainType.MILITARY:
            factors = [
                data.get("command_structure", 0.5),
                data.get("decision_speed", 0.5),
                data.get("strategic_vision", 0.5)
            ]
        elif domain == DomainType.INTELLIGENCE:
            factors = [
                data.get("coordination_effectiveness", 0.5),
                data.get("analysis_leadership", 0.5),
                data.get("strategic_guidance", 0.5)
            ]
        elif domain == DomainType.BUSINESS:
            factors = [
                data.get("executive_leadership", 0.5),
                data.get("strategic_planning", 0.5),
                data.get("change_management", 0.5)
            ]
        elif domain == DomainType.CYBERSECURITY:
            factors = [
                data.get("security_leadership", 0.5),
                data.get("incident_command", 0.5),
                data.get("risk_governance", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5]
        
        return sum(factors) / len(factors)
    
    def _calculate_organizational_discipline(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Calculate organizational discipline and processes."""
        if domain == DomainType.MILITARY:
            factors = [
                data.get("training_standards", 0.5),
                data.get("operational_discipline", 0.5),
                data.get("logistics_efficiency", 0.5)
            ]
        elif domain == DomainType.INTELLIGENCE:
            factors = [
                data.get("analytical_processes", 0.5),
                data.get("security_protocols", 0.5),
                data.get("quality_standards", 0.5)
            ]
        elif domain == DomainType.BUSINESS:
            factors = [
                data.get("operational_efficiency", 0.5),
                data.get("quality_management", 0.5),
                data.get("process_discipline", 0.5)
            ]
        elif domain == DomainType.CYBERSECURITY:
            factors = [
                data.get("security_processes", 0.5),
                data.get("incident_procedures", 0.5),
                data.get("compliance_standards", 0.5)
            ]
        else:
            factors = [0.5, 0.5, 0.5]
        
        return sum(factors) / len(factors)
    
    def analyze_deception_patterns(self, data: Dict[str, Any], domain: DomainType) -> Dict[str, Any]:
        """Analyze deception and misdirection patterns."""
        deception_analysis = {
            "capability_masking": self._assess_capability_masking(data, domain),
            "intention_deception": self._assess_intention_deception(data, domain),
            "information_manipulation": self._assess_information_manipulation(data, domain),
            "alliance_manipulation": self._assess_alliance_manipulation(data, domain),
            "timing_deception": self._assess_timing_deception(data, domain)
        }
        
        # Calculate overall deception effectiveness
        deception_scores = list(deception_analysis.values())
        deception_analysis["overall_effectiveness"] = sum(deception_scores) / len(deception_scores)
        
        return deception_analysis
    
    def _assess_capability_masking(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Assess capability masking effectiveness."""
        if domain == DomainType.MILITARY:
            return data.get("force_concealment", 0.5)
        elif domain == DomainType.INTELLIGENCE:
            return data.get("source_protection", 0.5)
        elif domain == DomainType.BUSINESS:
            return data.get("competitive_secrecy", 0.5)
        elif domain == DomainType.CYBERSECURITY:
            return data.get("security_through_obscurity", 0.5)
        return 0.5
    
    def _assess_intention_deception(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Assess intention deception effectiveness."""
        if domain == DomainType.MILITARY:
            return data.get("strategic_misleading", 0.5)
        elif domain == DomainType.INTELLIGENCE:
            return data.get("cover_stories", 0.5)
        elif domain == DomainType.BUSINESS:
            return data.get("market_misleading", 0.5)
        elif domain == DomainType.CYBERSECURITY:
            return data.get("threat_misleading", 0.5)
        return 0.5
    
    def _assess_information_manipulation(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Assess information manipulation effectiveness."""
        if domain == DomainType.MILITARY:
            return data.get("propaganda_effectiveness", 0.5)
        elif domain == DomainType.INTELLIGENCE:
            return data.get("disinformation_capability", 0.5)
        elif domain == DomainType.BUSINESS:
            return data.get("public_relations", 0.5)
        elif domain == DomainType.CYBERSECURITY:
            return data.get("threat_intelligence_manipulation", 0.5)
        return 0.5
    
    def _assess_alliance_manipulation(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Assess alliance manipulation effectiveness."""
        if domain == DomainType.MILITARY:
            return data.get("coalition_management", 0.5)
        elif domain == DomainType.INTELLIGENCE:
            return data.get("partner_manipulation", 0.5)
        elif domain == DomainType.BUSINESS:
            return data.get("stakeholder_management", 0.5)
        elif domain == DomainType.CYBERSECURITY:
            return data.get("vendor_manipulation", 0.5)
        return 0.5
    
    def _assess_timing_deception(self, data: Dict[str, Any], domain: DomainType) -> float:
        """Assess timing deception effectiveness."""
        if domain == DomainType.MILITARY:
            return data.get("operational_timing", 0.5)
        elif domain == DomainType.INTELLIGENCE:
            return data.get("collection_timing", 0.5)
        elif domain == DomainType.BUSINESS:
            return data.get("market_timing", 0.5)
        elif domain == DomainType.CYBERSECURITY:
            return data.get("attack_timing", 0.5)
        return 0.5
    
    def generate_recommendations(self, assessment: StrategicAssessment) -> List[str]:
        """Generate strategic recommendations based on assessment."""
        recommendations = []
        
        # Analyze five fundamentals and provide recommendations
        for fundamental, score in assessment.five_fundamentals.items():
            if score < 0.6:
                recommendations.append(f"Strengthen {fundamental.replace('_', ' ')} capabilities")
            elif score > 0.8:
                recommendations.append(f"Leverage {fundamental.replace('_', ' ')} advantages")
        
        # Analyze deception patterns
        deception_score = assessment.deception_analysis.get("overall_effectiveness", 0.5)
        if deception_score < 0.6:
            recommendations.append("Enhance deception and misdirection capabilities")
        elif deception_score > 0.8:
            recommendations.append("Maintain deception superiority while avoiding overconfidence")
        
        # Analyze resource management
        resource_score = assessment.resource_assessment.get("efficiency", 0.5)
        if resource_score < 0.6:
            recommendations.append("Optimize resource allocation and efficiency")
        
        # Analyze intelligence capabilities
        intel_score = assessment.intelligence_capabilities.get("effectiveness", 0.5)
        if intel_score < 0.6:
            recommendations.append("Strengthen intelligence and information gathering capabilities")
        
        # Analyze alliance management
        alliance_score = assessment.alliance_analysis.get("effectiveness", 0.5)
        if alliance_score < 0.6:
            recommendations.append("Strengthen alliance and partnership management")
        
        return recommendations
    
    def calculate_confidence_score(self, assessment: StrategicAssessment) -> float:
        """Calculate confidence score for the assessment."""
        # Weight different factors for confidence calculation
        factors = [
            assessment.five_fundamentals.get("the_way", 0.5) * 0.2,
            assessment.five_fundamentals.get("heaven", 0.5) * 0.15,
            assessment.five_fundamentals.get("earth", 0.5) * 0.25,
            assessment.five_fundamentals.get("command", 0.5) * 0.2,
            assessment.five_fundamentals.get("method", 0.5) * 0.2
        ]
        
        return sum(factors)
    
    def conduct_strategic_assessment(self, data: Dict[str, Any], domain: DomainType) -> StrategicAssessment:
        """Conduct comprehensive strategic assessment."""
        # Analyze five fundamentals
        five_fundamentals = self.analyze_five_fundamentals(data, domain)
        
        # Analyze deception patterns
        deception_analysis = self.analyze_deception_patterns(data, domain)
        
        # Analyze resource management
        resource_assessment = {
            "efficiency": data.get("resource_efficiency", 0.5),
            "sustainability": data.get("resource_sustainability", 0.5),
            "allocation": data.get("resource_allocation", 0.5)
        }
        
        # Analyze intelligence capabilities
        intelligence_capabilities = {
            "effectiveness": data.get("intelligence_effectiveness", 0.5),
            "coverage": data.get("intelligence_coverage", 0.5),
            "quality": data.get("intelligence_quality", 0.5)
        }
        
        # Analyze alliance management
        alliance_analysis = {
            "effectiveness": data.get("alliance_effectiveness", 0.5),
            "cohesion": data.get("alliance_cohesion", 0.5),
            "coordination": data.get("alliance_coordination", 0.5)
        }
        
        # Create assessment object
        assessment = StrategicAssessment(
            domain=domain.value,
            assessment_date=datetime.now().isoformat(),
            five_fundamentals=five_fundamentals,
            deception_analysis=deception_analysis,
            resource_assessment=resource_assessment,
            intelligence_capabilities=intelligence_capabilities,
            alliance_analysis=alliance_analysis,
            recommendations=[],
            risk_factors=[],
            opportunities=[],
            confidence_score=0.0
        )
        
        # Generate recommendations
        assessment.recommendations = self.generate_recommendations(assessment)
        
        # Calculate confidence score
        assessment.confidence_score = self.calculate_confidence_score(assessment)
        
        return assessment

# Initialize the strategic analysis engine
strategic_engine = StrategicAnalysisEngine()

# Create MCP server
server = Server("strategic-analysis")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="conduct_strategic_assessment",
                description="Conduct comprehensive strategic assessment using Art of War principles",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "enum": ["military", "intelligence", "business", "cybersecurity", "diplomatic"],
                            "description": "Domain type for analysis"
                        },
                        "data": {
                            "type": "object",
                            "description": "Strategic data for analysis"
                        }
                    },
                    "required": ["domain", "data"]
                }
            ),
            Tool(
                name="analyze_deception_patterns",
                description="Analyze deception and misdirection patterns",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "enum": ["military", "intelligence", "business", "cybersecurity", "diplomatic"],
                            "description": "Domain type for analysis"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data for deception analysis"
                        }
                    },
                    "required": ["domain", "data"]
                }
            ),
            Tool(
                name="generate_strategic_recommendations",
                description="Generate strategic recommendations based on assessment",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "assessment": {
                            "type": "object",
                            "description": "Strategic assessment result"
                        }
                    },
                    "required": ["assessment"]
                }
            )
        ]
    )

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "conduct_strategic_assessment":
            domain = DomainType(arguments["domain"])
            data = arguments["data"]
            
            assessment = strategic_engine.conduct_strategic_assessment(data, domain)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Strategic Assessment Complete\n\n"
                             f"Domain: {assessment.domain}\n"
                             f"Date: {assessment.assessment_date}\n"
                             f"Confidence Score: {assessment.confidence_score:.2f}\n\n"
                             f"Five Fundamentals:\n"
                             f"{json.dumps(assessment.five_fundamentals, indent=2)}\n\n"
                             f"Recommendations:\n"
                             f"{chr(10).join(f'- {rec}' for rec in assessment.recommendations)}"
                    )
                ]
            )
        
        elif name == "analyze_deception_patterns":
            domain = DomainType(arguments["domain"])
            data = arguments["data"]
            
            deception_analysis = strategic_engine.analyze_deception_patterns(data, domain)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Deception Analysis Complete\n\n"
                             f"Domain: {domain.value}\n\n"
                             f"Analysis Results:\n"
                             f"{json.dumps(deception_analysis, indent=2)}"
                    )
                ]
            )
        
        elif name == "generate_strategic_recommendations":
            assessment_data = arguments["assessment"]
            
            # Convert dict back to StrategicAssessment object
            assessment = StrategicAssessment(**assessment_data)
            recommendations = strategic_engine.generate_recommendations(assessment)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Strategic Recommendations Generated\n\n"
                             f"Recommendations:\n"
                             f"{chr(10).join(f'- {rec}' for rec in recommendations)}"
                    )
                ]
            )
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool call {name}: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        )

async def main():
    """Main function to run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="strategic-analysis",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
