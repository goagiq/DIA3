"""
Multi-Domain Strategic Analyzer
Provides generic strategic analysis capabilities across multiple domains including 
business, defense, and intelligence.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import logging

# Import core components
try:
    from src.core.vector_db import VectorDB
    from src.core.improved_knowledge_graph_utility import (
        ImprovedKnowledgeGraphUtility
    )
except ImportError:
    # Fallback for missing dependencies
    VectorDB = None
    ImprovedKnowledgeGraphUtility = None


class DomainType(Enum):
    """Supported domain types for strategic analysis."""
    BUSINESS = "business"
    DEFENSE = "defense"
    INTELLIGENCE = "intelligence"
    CYBERSECURITY = "cybersecurity"
    GEOPOLITICAL = "geopolitical"
    ECONOMIC = "economic"
    TECHNOLOGICAL = "technological"
    SOCIAL = "social"
    ENVIRONMENTAL = "environmental"


class AnalysisType(Enum):
    """Types of strategic analysis available."""
    COMPREHENSIVE = "comprehensive"
    COMPETITIVE = "competitive"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    THREAT = "threat"
    TREND = "trend"
    SCENARIO = "scenario"
    DECEPTION = "deception"
    INTELLIGENCE = "intelligence"


@dataclass
class StrategicContext:
    """Context information for strategic analysis."""
    domain: DomainType
    analysis_type: AnalysisType
    market_conditions: Optional[Dict[str, Any]] = None
    competitive_landscape: Optional[Dict[str, Any]] = None
    risk_factors: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    threats: Optional[List[str]] = None
    trends: Optional[List[str]] = None


@dataclass
class StrategicRecommendation:
    """Strategic recommendation with domain-specific context."""
    title: str
    description: str
    priority: str  # "high", "medium", "low"
    timeframe: str  # "immediate", "short-term", "medium-term", "long-term"
    domain: DomainType
    impact_score: float  # 0.0 to 1.0
    implementation_difficulty: str  # "easy", "moderate", "difficult"
    resources_required: List[str]
    success_metrics: List[str]


class MultiDomainStrategicAnalyzer:
    """
    Generic strategic analyzer that can handle multiple domains with domain-specific adaptations.
    """
    
    def __init__(self, output_dir: str = "Results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging first
        self.logger = logging.getLogger(__name__)
        
        # Initialize core components with fallback
        try:
            if VectorDB is not None:
                self.vector_db = VectorDB()
            else:
                self.vector_db = None
                self.logger.warning("VectorDB not available, using fallback")
        except Exception as e:
            self.vector_db = None
            self.logger.warning(f"VectorDB initialization failed: {e}")
        
        try:
            if ImprovedKnowledgeGraphUtility is not None:
                self.knowledge_graph = ImprovedKnowledgeGraphUtility(
                    output_dir=str(self.output_dir)
                )
            else:
                self.knowledge_graph = None
                self.logger.warning("KnowledgeGraph not available, using fallback")
        except Exception as e:
            self.knowledge_graph = None
            self.logger.warning(f"KnowledgeGraph initialization failed: {e}")
        
        # Domain-specific templates and frameworks
        self.domain_templates = self._initialize_domain_templates()
        self.analysis_frameworks = self._initialize_analysis_frameworks()
    
    def _initialize_domain_templates(self) -> Dict[DomainType, Dict[str, Any]]:
        """Initialize domain-specific analysis templates."""
        return {
            DomainType.BUSINESS: {
                "key_metrics": [
                    "market_share", "revenue_growth", "profit_margins", 
                    "customer_satisfaction"
                ],
                "strategic_principles": [
                    "competitive_advantage", "market_positioning", 
                    "resource_allocation"
                ],
                "risk_categories": [
                    "market_risk", "operational_risk", "financial_risk", 
                    "reputational_risk"
                ],
                "success_factors": [
                    "innovation", "customer_focus", "operational_excellence", 
                    "talent_management"
                ]
            },
            DomainType.DEFENSE: {
                "key_metrics": [
                    "capability_gaps", "threat_assessment", "readiness_levels", 
                    "alliance_strength"
                ],
                "strategic_principles": [
                    "deterrence", "defense_in_depth", "force_projection", 
                    "alliance_building"
                ],
                "risk_categories": [
                    "military_threat", "technological_gap", "alliance_weakness", 
                    "resource_constraint"
                ],
                "success_factors": [
                    "technological_superiority", "alliance_cohesion", 
                    "strategic_flexibility", "intelligence_capability"
                ]
            },
            DomainType.INTELLIGENCE: {
                "key_metrics": [
                    "intelligence_coverage", "threat_detection_rate", 
                    "analysis_accuracy", "response_time"
                ],
                "strategic_principles": [
                    "information_asymmetry", "deception_detection", 
                    "source_protection", "analysis_depth"
                ],
                "risk_categories": [
                    "intelligence_gap", "deception_risk", "source_compromise", 
                    "analysis_bias"
                ],
                "success_factors": [
                    "source_network", "analytical_capability", 
                    "technological_edge", "operational_security"
                ]
            },
            DomainType.CYBERSECURITY: {
                "key_metrics": [
                    "threat_detection", "incident_response_time", 
                    "vulnerability_management", "security_posture"
                ],
                "strategic_principles": [
                    "defense_in_depth", "zero_trust", "threat_intelligence", 
                    "incident_response"
                ],
                "risk_categories": [
                    "cyber_threat", "vulnerability_exposure", "data_breach", 
                    "system_compromise"
                ],
                "success_factors": [
                    "threat_intelligence", "security_automation", 
                    "incident_response", "security_culture"
                ]
            },
            DomainType.GEOPOLITICAL: {
                "key_metrics": [
                    "influence_radius", "alliance_strength", 
                    "diplomatic_relations", "economic_leverage"
                ],
                "strategic_principles": [
                    "balance_of_power", "alliance_building", 
                    "diplomatic_engagement", "economic_statecraft"
                ],
                "risk_categories": [
                    "geopolitical_conflict", "alliance_fragmentation", 
                    "economic_sanctions", "diplomatic_isolation"
                ],
                "success_factors": [
                    "diplomatic_skill", "economic_strength", 
                    "alliance_network", "strategic_patience"
                ]
            }
        }
    
    def _initialize_analysis_frameworks(self) -> Dict[AnalysisType, Dict[str, Any]]:
        """Initialize analysis frameworks for different analysis types."""
        return {
            AnalysisType.COMPREHENSIVE: {
                "components": ["situation_analysis", "competitive_analysis", "risk_assessment", "opportunity_analysis", "strategic_recommendations"],
                "art_of_war_principles": ["strategic_ambiguity", "information_asymmetry", "psychological_positioning"],
                "output_format": "comprehensive_report"
            },
            AnalysisType.COMPETITIVE: {
                "components": ["competitor_analysis", "market_positioning", "competitive_advantage", "threat_assessment"],
                "art_of_war_principles": ["show_inability_when_able", "show_disuse_when_using", "lure_with_profit"],
                "output_format": "competitive_intelligence_report"
            },
            AnalysisType.RISK: {
                "components": ["risk_identification", "risk_assessment", "risk_mitigation", "risk_monitoring"],
                "art_of_war_principles": ["prepare_against_strength", "avoid_the_strong", "take_advantage_of_disorder"],
                "output_format": "risk_assessment_report"
            },
            AnalysisType.OPPORTUNITY: {
                "components": ["opportunity_identification", "opportunity_assessment", "opportunity_prioritization", "opportunity_execution"],
                "art_of_war_principles": ["attack_unprepared", "emerge_unexpectedly", "lure_with_profit"],
                "output_format": "opportunity_analysis_report"
            },
            AnalysisType.DECEPTION: {
                "components": ["deception_detection", "deception_analysis", "counter_deception", "deception_planning"],
                "art_of_war_principles": ["show_inability_when_able", "show_disuse_when_using", "show_distance_when_near"],
                "output_format": "deception_analysis_report"
            }
        }
    
    async def analyze_strategic_position(
        self,
        content: str,
        domain: DomainType,
        analysis_type: AnalysisType = AnalysisType.COMPREHENSIVE,
        context: Optional[StrategicContext] = None,
        include_art_of_war: bool = True,
        include_recommendations: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive strategic analysis for any domain.
        
        Args:
            content: Analysis content or query
            domain: Target domain for analysis
            analysis_type: Type of analysis to perform
            context: Additional strategic context
            include_art_of_war: Whether to include Art of War principles
            include_recommendations: Whether to include strategic recommendations
            
        Returns:
            Comprehensive strategic analysis results
        """
        try:
            self.logger.info(f"Starting strategic analysis for domain: {domain.value}, type: {analysis_type.value}")
            
            # Store content in vector database
            content_id = await self._store_analysis_content(content, domain, analysis_type)
            
            # Get domain-specific template
            domain_template = self.domain_templates.get(domain, {})
            analysis_framework = self.analysis_frameworks.get(analysis_type, {})
            
            # Perform domain-specific analysis
            analysis_result = await self._perform_domain_analysis(
                content, domain, analysis_type, domain_template, analysis_framework
            )
            
            # Add Art of War principles if requested
            if include_art_of_war:
                art_of_war_analysis = await self._apply_art_of_war_principles(
                    content, domain, analysis_framework.get("art_of_war_principles", [])
                )
                analysis_result["art_of_war_analysis"] = art_of_war_analysis
            
            # Generate strategic recommendations if requested
            if include_recommendations:
                recommendations = await self._generate_strategic_recommendations(
                    analysis_result, domain, context
                )
                analysis_result["strategic_recommendations"] = recommendations
            
            # Add metadata
            analysis_result["metadata"] = {
                "domain": domain.value,
                "analysis_type": analysis_type.value,
                "content_id": content_id,
                "timestamp": self._get_timestamp(),
                "framework_used": analysis_framework.get("output_format", "strategic_analysis")
            }
            
            # Store analysis result
            await self._store_analysis_result(analysis_result, domain, analysis_type)
            
            self.logger.info(f"Strategic analysis completed successfully for domain: {domain.value}")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error in strategic analysis: {str(e)}")
            raise
    
    async def _perform_domain_analysis(
        self,
        content: str,
        domain: DomainType,
        analysis_type: AnalysisType,
        domain_template: Dict[str, Any],
        analysis_framework: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform domain-specific analysis using appropriate frameworks."""
        
        analysis_components = analysis_framework.get("components", [])
        analysis_result = {
            "domain_analysis": {},
            "key_metrics": domain_template.get("key_metrics", []),
            "strategic_principles": domain_template.get("strategic_principles", []),
            "risk_categories": domain_template.get("risk_categories", []),
            "success_factors": domain_template.get("success_factors", [])
        }
        
        # Perform component-specific analysis
        for component in analysis_components:
            component_result = await self._analyze_component(
                content, domain, component, domain_template
            )
            analysis_result["domain_analysis"][component] = component_result
        
        return analysis_result
    
    async def _analyze_component(
        self,
        content: str,
        domain: DomainType,
        component: str,
        domain_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze a specific component of the strategic analysis."""
        
        # This would integrate with specific analysis agents based on component
        # For now, we'll provide a generic analysis structure
        
        if component == "situation_analysis":
            return {
                "current_state": "Analyzing current strategic position...",
                "key_factors": domain_template.get("key_metrics", []),
                "trends": ["Digital transformation", "Globalization", "Technology disruption"],
                "challenges": ["Competition", "Regulation", "Resource constraints"]
            }
        
        elif component == "competitive_analysis":
            return {
                "competitors": ["Primary", "Secondary", "Emerging"],
                "competitive_advantages": ["Technology", "Market position", "Resources"],
                "competitive_threats": ["New entrants", "Substitute products", "Bargaining power"],
                "market_position": "Analyzing market position..."
            }
        
        elif component == "risk_assessment":
            return {
                "risk_categories": domain_template.get("risk_categories", []),
                "risk_levels": {"high": [], "medium": [], "low": []},
                "mitigation_strategies": ["Diversification", "Insurance", "Contingency planning"],
                "risk_monitoring": "Continuous risk monitoring recommended"
            }
        
        elif component == "opportunity_analysis":
            return {
                "market_opportunities": ["Emerging markets", "New technologies", "Regulatory changes"],
                "growth_potential": "High growth potential identified",
                "resource_requirements": ["Capital", "Talent", "Technology"],
                "timeline": "Short to medium term opportunities"
            }
        
        else:
            return {
                "analysis": f"Generic analysis for {component}",
                "recommendations": ["Further analysis recommended"],
                "next_steps": ["Detailed assessment", "Stakeholder consultation"]
            }
    
    async def _apply_art_of_war_principles(
        self,
        content: str,
        domain: DomainType,
        principles: List[str]
    ) -> Dict[str, Any]:
        """Apply Art of War principles to the strategic analysis."""
        
        art_of_war_analysis = {
            "core_principles": {
                "fundamental_principle": {
                    "chinese": "兵者，詭道也",
                    "translation": "War is the way of deception",
                    "explanation": "Establishes deception as not merely a tactic but the very essence of strategic conflict"
                },
                "key_concepts": [
                    "Strategic Ambiguity: Maintaining uncertainty about capabilities and intentions",
                    "Information Asymmetry: Creating knowledge gaps that favor one's position",
                    "Psychological Warfare: Manipulating enemy perceptions and morale",
                    "Operational Security: Protecting one's own information while gathering intelligence"
                ]
            },
            "techniques": {},
            "domain_applications": {}
        }
        
        # Apply specific techniques based on principles
        for principle in principles:
            technique_analysis = await self._analyze_art_of_war_technique(principle, domain)
            art_of_war_analysis["techniques"][principle] = technique_analysis
        
        # Add domain-specific applications
        art_of_war_analysis["domain_applications"] = await self._get_domain_applications(domain)
        
        return art_of_war_analysis
    
    async def _analyze_art_of_war_technique(self, technique: str, domain: DomainType) -> Dict[str, Any]:
        """Analyze a specific Art of War technique for the domain."""
        
        technique_mappings = {
            "strategic_ambiguity": {
                "chinese": "能而示之不能",
                "translation": "Show inability when able",
                "explanation": "Downplaying capabilities while maintaining readiness",
                "domain_application": self._get_domain_specific_application(technique, domain)
            },
            "information_asymmetry": {
                "chinese": "用而示之不用",
                "translation": "Show disuse when using",
                "explanation": "Appearing disinterested while actively pursuing influence",
                "domain_application": self._get_domain_specific_application(technique, domain)
            },
            "psychological_positioning": {
                "chinese": "卑而驕之",
                "translation": "Make proud when humble",
                "explanation": "Using humility to build trust while maintaining strategic advantage",
                "domain_application": self._get_domain_specific_application(technique, domain)
            }
        }
        
        return technique_mappings.get(technique, {
            "translation": technique,
            "explanation": f"Application of {technique} in {domain.value} context",
            "domain_application": self._get_domain_specific_application(technique, domain)
        })
    
    def _get_domain_specific_application(self, technique: str, domain: DomainType) -> str:
        """Get domain-specific application of Art of War technique."""
        
        applications = {
            DomainType.BUSINESS: {
                "strategic_ambiguity": "Maintain competitive advantages while appearing modest about capabilities",
                "information_asymmetry": "Pursue market opportunities quietly while competitors focus elsewhere",
                "psychological_positioning": "Position as a collaborative partner rather than aggressive competitor"
            },
            DomainType.DEFENSE: {
                "strategic_ambiguity": "Maintain military capabilities while appearing defensive",
                "information_asymmetry": "Gather intelligence while protecting own information",
                "psychological_positioning": "Build alliances while maintaining strategic independence"
            },
            DomainType.INTELLIGENCE: {
                "strategic_ambiguity": "Maintain operational security while gathering intelligence",
                "information_asymmetry": "Create information advantages through superior collection",
                "psychological_positioning": "Build trust with sources while maintaining operational security"
            }
        }
        
        domain_apps = applications.get(domain, {})
        return domain_apps.get(technique, f"Generic application of {technique} in {domain.value}")
    
    async def _get_domain_applications(self, domain: DomainType) -> Dict[str, Any]:
        """Get comprehensive domain applications of Art of War principles."""
        
        applications = {
            DomainType.BUSINESS: {
                "modern_applications": {
                    "information_warfare": {
                        "technique": "Competitive Intelligence",
                        "art_of_war_basis": "Information Asymmetry",
                        "modern_examples": [
                            "Market research and competitive analysis",
                            "Patent monitoring and technology tracking",
                            "Social media monitoring and sentiment analysis",
                            "Supply chain intelligence"
                        ]
                    }
                },
                "ethical_considerations": {
                    "legitimate": [
                        "Public information gathering",
                        "Market research within legal bounds",
                        "Competitive analysis using open sources",
                        "Strategic planning based on public data"
                    ],
                    "unethical": [
                        "Corporate espionage",
                        "Trade secret theft",
                        "False advertising",
                        "Market manipulation"
                    ]
                }
            },
            DomainType.DEFENSE: {
                "modern_applications": {
                    "information_warfare": {
                        "technique": "Military Deception",
                        "art_of_war_basis": "Strategic Ambiguity",
                        "modern_examples": [
                            "Electronic warfare and cyber operations",
                            "Psychological operations",
                            "Military deception campaigns",
                            "Strategic communication"
                        ]
                    }
                },
                "ethical_considerations": {
                    "legitimate": [
                        "Defensive military operations",
                        "Alliance building and cooperation",
                        "International law compliance",
                        "Humanitarian assistance"
                    ],
                    "unethical": [
                        "War crimes and violations",
                        "Targeting civilians",
                        "Use of prohibited weapons",
                        "Violation of international law"
                    ]
                }
            }
        }
        
        return applications.get(domain, {
            "modern_applications": {"generic": "Domain-specific applications to be developed"},
            "ethical_considerations": {"generic": "Domain-specific ethical considerations to be developed"}
        })
    
    async def _generate_strategic_recommendations(
        self,
        analysis_result: Dict[str, Any],
        domain: DomainType,
        context: Optional[StrategicContext]
    ) -> List[StrategicRecommendation]:
        """Generate strategic recommendations based on analysis results."""
        
        recommendations = []
        
        # Generate recommendations based on domain and analysis results
        if domain == DomainType.BUSINESS:
            recommendations.extend([
                StrategicRecommendation(
                    title="Enhance Digital Capabilities",
                    description="Accelerate digital transformation initiatives to maintain competitive advantage",
                    priority="high",
                    timeframe="short-term",
                    domain=domain,
                    impact_score=0.8,
                    implementation_difficulty="moderate",
                    resources_required=["Technology investment", "Talent acquisition", "Process redesign"],
                    success_metrics=["Digital adoption rate", "Operational efficiency", "Customer satisfaction"]
                ),
                StrategicRecommendation(
                    title="Build Strategic Alliances",
                    description="Form partnerships to counter dominant market players",
                    priority="medium",
                    timeframe="medium-term",
                    domain=domain,
                    impact_score=0.7,
                    implementation_difficulty="moderate",
                    resources_required=["Partnership development", "Legal expertise", "Relationship management"],
                    success_metrics=["Alliance strength", "Market access", "Resource sharing"]
                )
            ])
        
        elif domain == DomainType.DEFENSE:
            recommendations.extend([
                StrategicRecommendation(
                    title="Enhance Intelligence Capabilities",
                    description="Strengthen intelligence collection and analysis capabilities",
                    priority="high",
                    timeframe="short-term",
                    domain=domain,
                    impact_score=0.9,
                    implementation_difficulty="difficult",
                    resources_required=["Technology investment", "Intelligence personnel", "Training programs"],
                    success_metrics=["Intelligence coverage", "Threat detection rate", "Analysis accuracy"]
                ),
                StrategicRecommendation(
                    title="Strengthen Alliances",
                    description="Build and maintain strong international alliances",
                    priority="high",
                    timeframe="medium-term",
                    domain=domain,
                    impact_score=0.8,
                    implementation_difficulty="moderate",
                    resources_required=["Diplomatic resources", "Joint exercises", "Information sharing"],
                    success_metrics=["Alliance cohesion", "Joint capability", "Deterrence effectiveness"]
                )
            ])
        
        # Add generic recommendations for all domains
        recommendations.extend([
            StrategicRecommendation(
                title="Continuous Monitoring",
                description="Implement continuous monitoring of strategic environment",
                priority="medium",
                timeframe="immediate",
                domain=domain,
                impact_score=0.6,
                implementation_difficulty="easy",
                resources_required=["Monitoring systems", "Analytical personnel", "Reporting mechanisms"],
                success_metrics=["Early warning capability", "Response time", "Situational awareness"]
            )
        ])
        
        return recommendations
    
    async def _store_analysis_content(
        self,
        content: str,
        domain: DomainType,
        analysis_type: AnalysisType
    ) -> str:
        """Store analysis content in vector database."""
        metadata = {
            "domain": domain.value,
            "analysis_type": analysis_type.value,
            "content_type": "strategic_analysis"
        }
        
        if self.vector_db is not None:
            content_id = await self.vector_db.store_content(content, metadata)
        else:
            # Fallback: generate a simple ID
            import uuid
            content_id = str(uuid.uuid4())
            self.logger.info(f"Stored content with fallback ID: {content_id}")
        
        return content_id
    
    async def _store_analysis_result(
        self,
        analysis_result: Dict[str, Any],
        domain: DomainType,
        analysis_type: AnalysisType
    ) -> None:
        """Store analysis result for future reference."""
        # Store in knowledge graph if available
        if self.knowledge_graph is not None:
            try:
                await self.knowledge_graph.store_analysis_result(
                    analysis_result,
                    domain.value,
                    analysis_type.value
                )
            except Exception as e:
                self.logger.warning(f"Failed to store analysis result: {e}")
        else:
            self.logger.info("Knowledge graph not available, skipping result storage")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for analysis metadata."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def get_domain_capabilities(self, domain: DomainType) -> Dict[str, Any]:
        """Get capabilities and frameworks available for a specific domain."""
        template = self.domain_templates.get(domain, {})
        return {
            "domain": domain.value,
            "key_metrics": template.get("key_metrics", []),
            "strategic_principles": template.get("strategic_principles", []),
            "risk_categories": template.get("risk_categories", []),
            "success_factors": template.get("success_factors", []),
            "supported_analysis_types": [at.value for at in AnalysisType],
            "art_of_war_integration": True
        }
    
    async def get_supported_domains(self) -> List[Dict[str, Any]]:
        """Get list of all supported domains with their capabilities."""
        domains = []
        for domain in DomainType:
            capabilities = await self.get_domain_capabilities(domain)
            domains.append(capabilities)
        return domains
