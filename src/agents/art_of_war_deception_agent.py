#!/usr/bin/env python3
"""
Art of War Deception Analysis Agent

This agent provides comprehensive analysis of deception and misdirection techniques 
from Sun Tzu's The Art of War and their modern diplomatic applications.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

# Import core services
from core.vector_db import VectorDBManager
from core.report_manager import report_manager
from core.improved_knowledge_graph_utility import ImprovedKnowledgeGraphUtility


class ArtOfWarDeceptionAgent:
    """Agent for analyzing Art of War deception techniques and modern diplomatic applications."""

    def __init__(self):
        """Initialize the Art of War deception analysis agent."""
        self.vector_store = VectorDBManager()
        self.knowledge_graph = ImprovedKnowledgeGraphUtility()
        
        # Core deception principles from The Art of War
        self.deception_principles = {
            "fundamental_principle": "兵者，詭道也",  # War is the way of deception
            "techniques": [
                "能而示之不能",  # Show inability when able
                "用而示之不用",  # Show disuse when using  
                "近而示之遠",    # Show distance when near
                "遠而示之近",    # Show nearness when far
                "利而誘之",      # Lure with profit
                "亂而取之",      # Take advantage of disorder
                "實而備之",      # Prepare against strength
                "強而避之",      # Avoid the strong
                "怒而撓之",      # Provoke when angry
                "卑而驕之",      # Make proud when humble
                "佚而勞之",      # Make tired when rested
                "親而離之",      # Separate when united
                "攻其無備，出其不意"  # Attack unprepared, emerge unexpectedly
            ]
        }
        
        # Modern diplomatic applications mapping
        self.modern_applications = {
            "information_warfare": {
                "technique": "Disinformation and Propaganda",
                "art_of_war_basis": "利而誘之 (Lure with profit) and 親而離之 (Separate when united)",
                "modern_examples": [
                    "Social media manipulation campaigns",
                    "Deep fake videos and audio",
                    "Coordinated bot networks",
                    "State-sponsored disinformation"
                ],
                "diplomatic_impact": "Undermining trust in democratic institutions and creating social divisions"
            },
            "economic_deception": {
                "technique": "Economic Warfare and Financial Deception",
                "art_of_war_basis": "能而示之不能 (Show inability when able) and 用而示之不用 (Show disuse when using)",
                "modern_examples": [
                    "Currency manipulation",
                    "Hidden subsidies and state support",
                    "Sanction evasion through complex networks",
                    "Trade agreement violations"
                ],
                "diplomatic_impact": "Gaining economic advantages while appearing to follow international rules"
            },
            "alliance_management": {
                "technique": "Divide and Conquer Strategies",
                "art_of_war_basis": "親而離之 (Separate when united) and 亂而取之 (Take advantage of disorder)",
                "modern_examples": [
                    "Bilateral deals that undermine multilateral agreements",
                    "Playing allies against each other",
                    "Supporting opposition groups in allied countries",
                    "Creating divisions within international organizations"
                ],
                "diplomatic_impact": "Breaking up beneficial coalitions and weakening collective responses"
            },
            "crisis_management": {
                "technique": "Escalation and De-escalation Deception",
                "art_of_war_basis": "怒而撓之 (Provoke when angry) and 攻其無備，出其不意 (Attack unprepared)",
                "modern_examples": [
                    "False flag operations",
                    "Controlled escalation for strategic advantage",
                    "Sudden policy reversals",
                    "Crisis creation to justify actions"
                ],
                "diplomatic_impact": "Managing conflict intensity while maintaining strategic advantage"
            },
            "intelligence_operations": {
                "technique": "Espionage and Intelligence Deception",
                "art_of_war_basis": "近而示之遠，遠而示之近 (Show distance when near, nearness when far)",
                "modern_examples": [
                    "Double agents and moles",
                    "Cyber espionage operations",
                    "Diplomatic cover for intelligence activities",
                    "Technology theft and industrial espionage"
                ],
                "diplomatic_impact": "Gathering intelligence while maintaining plausible deniability"
            },
            "public_diplomacy": {
                "technique": "Soft Power and Cultural Influence",
                "art_of_war_basis": "卑而驕之 (Make proud when humble) and 佚而勞之 (Make tired when rested)",
                "modern_examples": [
                    "Cultural exchange programs with hidden agendas",
                    "Educational initiatives that promote specific viewpoints",
                    "Media ownership and editorial influence",
                    "Think tank funding and research direction"
                ],
                "diplomatic_impact": "Shaping public opinion and cultural narratives in target countries"
            }
        }

    async def analyze_deception_techniques(self, 
                                         analysis_type: str = "comprehensive",
                                         focus_areas: List[str] = None,
                                         include_modern_applications: bool = True,
                                         include_ethical_considerations: bool = True) -> Dict[str, Any]:
        """
        Analyze Art of War deception techniques and their modern applications.
        
        Args:
            analysis_type: Type of analysis ("comprehensive", "techniques_only", "modern_only", "ethical_only")
            focus_areas: Specific areas to focus on (e.g., ["information_warfare", "economic_deception"])
            include_modern_applications: Whether to include modern diplomatic applications
            include_ethical_considerations: Whether to include ethical considerations
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            logger.info(f"Starting Art of War deception analysis: {analysis_type}")
            
            result = {
                "success": True,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "core_principles": {},
                "techniques": {},
                "modern_applications": {},
                "ethical_considerations": {},
                "counter_strategies": {},
                "recommendations": {}
            }
            
            # Core deception principles
            if analysis_type in ["comprehensive", "techniques_only"]:
                result["core_principles"] = self._analyze_core_principles()
                result["techniques"] = self._analyze_deception_techniques()
            
            # Modern diplomatic applications
            if include_modern_applications and analysis_type in ["comprehensive", "modern_only"]:
                result["modern_applications"] = self._analyze_modern_applications(focus_areas)
            
            # Ethical considerations
            if include_ethical_considerations and analysis_type in ["comprehensive", "ethical_only"]:
                result["ethical_considerations"] = self._analyze_ethical_considerations()
                result["counter_strategies"] = self._generate_counter_strategies()
                result["recommendations"] = self._generate_recommendations()
            
            # Store analysis in vector database
            await self._store_analysis_result(result)
            
            logger.info("Art of War deception analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in deception analysis: {e}")
            return {"success": False, "error": str(e)}

    def _analyze_core_principles(self) -> Dict[str, Any]:
        """Analyze core deception principles from The Art of War."""
        return {
            "fundamental_principle": {
                "chinese": self.deception_principles["fundamental_principle"],
                "translation": "War is the way of deception",
                "explanation": "Establishes deception as not merely a tactic but the very essence of strategic conflict"
            },
            "key_concepts": [
                "Strategic Ambiguity: Maintaining uncertainty about capabilities and intentions",
                "Information Asymmetry: Creating knowledge gaps that favor one's position",
                "Psychological Warfare: Manipulating enemy perceptions and morale",
                "Operational Security: Protecting one's own information while gathering intelligence"
            ]
        }

    def _analyze_deception_techniques(self) -> Dict[str, Any]:
        """Analyze specific deception techniques from The Art of War."""
        techniques = {}
        
        for i, technique in enumerate(self.deception_principles["techniques"], 1):
            techniques[f"technique_{i}"] = {
                "chinese": technique,
                "translation": self._get_technique_translation(technique),
                "explanation": self._get_technique_explanation(technique),
                "modern_application": self._get_modern_application(technique),
                "diplomatic_example": self._get_diplomatic_example(technique)
            }
        
        return techniques

    def _analyze_modern_applications(self, focus_areas: List[str] = None) -> Dict[str, Any]:
        """Analyze modern diplomatic applications of Art of War techniques."""
        if focus_areas:
            return {area: self.modern_applications[area] 
                   for area in focus_areas 
                   if area in self.modern_applications}
        else:
            return self.modern_applications

    def _analyze_ethical_considerations(self) -> Dict[str, Any]:
        """Analyze ethical implications of applying Art of War techniques to modern diplomacy."""
        return {
            "legitimate_vs_unethical": {
                "legitimate": [
                    "Operational security measures",
                    "Strategic ambiguity for deterrence",
                    "Intelligence gathering within legal frameworks",
                    "Negotiation tactics that don't violate agreements"
                ],
                "unethical": [
                    "Violating international law and treaties",
                    "Harming civilian populations",
                    "Breaking formal diplomatic agreements",
                    "Using deception for personal gain rather than national interest"
                ]
            },
            "international_law_implications": [
                "Treaty obligations and compliance",
                "Human rights considerations",
                "Diplomatic immunity and protocols",
                "Cyber warfare legal frameworks",
                "Economic sanctions and their circumvention"
            ],
            "long_term_consequences": [
                "Erosion of international trust",
                "Reputation costs and credibility loss",
                "Escalation risks and unintended consequences",
                "Alliance fragmentation and isolation",
                "Reciprocal deception and arms races"
            ]
        }

    def _generate_counter_strategies(self) -> Dict[str, Any]:
        """Generate strategies for detecting and countering deception in modern diplomacy."""
        return {
            "intelligence_and_verification": [
                "Multiple source verification and cross-checking",
                "Pattern recognition in deceptive behavior",
                "Technical analysis and digital forensics",
                "Human intelligence networks and informants",
                "Open source intelligence (OSINT) analysis"
            ],
            "organizational_resilience": [
                "Comprehensive training programs for diplomats",
                "Standard operating procedures for verification",
                "Information sharing with allies and partners",
                "Red team exercises and scenario planning",
                "Regular security audits and assessments"
            ],
            "international_cooperation": [
                "Alliance building and intelligence sharing",
                "International norm development and standards",
                "Coordinated sanctions and responses",
                "Diplomatic isolation of deceptive actors",
                "Multilateral verification mechanisms"
            ],
            "technology_and_tools": [
                "Advanced analytics and AI for pattern detection",
                "Blockchain for secure information sharing",
                "Digital forensics and cyber security tools",
                "Social media monitoring and analysis",
                "Satellite and remote sensing capabilities"
            ]
        }

    def _generate_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for diplomatic services and organizations."""
        return {
            "for_diplomatic_services": [
                "Enhanced Training: Comprehensive education on deception detection",
                "Technology Investment: Advanced tools for information verification",
                "International Cooperation: Strengthening alliances and information sharing",
                "Ethical Guidelines: Clear standards for legitimate strategic deception"
            ],
            "for_international_organizations": [
                "Norm Development: Establishing international standards for transparency",
                "Monitoring Systems: Creating mechanisms to detect and report deception",
                "Sanctions Framework: Coordinated responses to deceptive practices",
                "Diplomatic Protocols: Strengthening rules for international conduct"
            ],
            "for_academic_institutions": [
                "Pattern Analysis: Studying historical deception patterns",
                "Technology Development: Creating tools for deception detection",
                "Policy Research: Developing frameworks for ethical strategic deception",
                "Education Programs: Training future diplomats and policymakers"
            ]
        }

    def _get_technique_translation(self, technique: str) -> str:
        """Get English translation for a Chinese technique."""
        translations = {
            "能而示之不能": "Show inability when able",
            "用而示之不用": "Show disuse when using",
            "近而示之遠": "Show distance when near",
            "遠而示之近": "Show nearness when far",
            "利而誘之": "Lure with profit",
            "亂而取之": "Take advantage of disorder",
            "實而備之": "Prepare against strength",
            "強而避之": "Avoid the strong",
            "怒而撓之": "Provoke when angry",
            "卑而驕之": "Make proud when humble",
            "佚而勞之": "Make tired when rested",
            "親而離之": "Separate when united",
            "攻其無備，出其不意": "Attack unprepared, emerge unexpectedly"
        }
        return translations.get(technique, "Unknown technique")

    def _get_technique_explanation(self, technique: str) -> str:
        """Get explanation for a deception technique."""
        explanations = {
            "能而示之不能": "Downplaying capabilities during negotiations while maintaining readiness",
            "用而示之不用": "Appearing disinterested while actively pursuing influence",
            "近而示之遠": "Misleading about location and timing of initiatives",
            "遠而示之近": "Misleading about location and timing of initiatives",
            "利而誘之": "Offering economic incentives to gain diplomatic concessions",
            "亂而取之": "Exploiting internal divisions in rival nations",
            "實而備之": "Building alliances and capabilities against strong adversaries",
            "強而避之": "Avoiding direct confrontation with superior powers",
            "怒而撓之": "Exploiting emotional vulnerabilities in negotiations",
            "卑而驕之": "Using flattery or humility to manipulate perceptions",
            "佚而勞之": "Draining adversary resources through prolonged negotiations",
            "親而離之": "Breaking up alliances and coalitions",
            "攻其無備，出其不意": "Diplomatic initiatives that catch adversaries off guard"
        }
        return explanations.get(technique, "Strategic manipulation for diplomatic advantage")

    def _get_modern_application(self, technique: str) -> str:
        """Get modern application for a deception technique."""
        applications = {
            "能而示之不能": "Publicly reducing defense spending while secretly modernizing",
            "用而示之不用": "Publicly withdrawing from a region while maintaining covert operations",
            "近而示之遠": "Announcing negotiations in one location while secretly meeting elsewhere",
            "遠而示之近": "Announcing negotiations in one location while secretly meeting elsewhere",
            "利而誘之": "Trade agreements that appear beneficial but contain hidden strategic advantages",
            "亂而取之": "Supporting opposition groups during political instability",
            "實而備之": "Forming economic blocs to counter dominant trading partners",
            "強而避之": "Using proxy conflicts instead of direct military engagement",
            "怒而撓之": "Using public shaming or flattery to influence diplomatic positions",
            "卑而驕之": "Cultural exchange programs with hidden agendas",
            "佚而勞之": "Endless rounds of talks that exhaust diplomatic resources",
            "親而離之": "Offering bilateral deals that undermine multilateral agreements",
            "攻其無備，出其不意": "Sudden policy announcements that change the diplomatic landscape"
        }
        return applications.get(technique, "Various applications in international relations")

    def _get_diplomatic_example(self, technique: str) -> str:
        """Get diplomatic example for a deception technique."""
        examples = {
            "能而示之不能": "A nation publicly reducing defense spending while secretly modernizing forces",
            "用而示之不用": "Publicly withdrawing from a region while maintaining covert operations",
            "近而示之遠": "Announcing negotiations in one location while secretly meeting elsewhere",
            "遠而示之近": "Announcing negotiations in one location while secretly meeting elsewhere",
            "利而誘之": "Trade agreements that appear beneficial but contain hidden strategic advantages",
            "亂而取之": "Supporting opposition groups during political instability",
            "實而備之": "Forming economic blocs to counter dominant trading partners",
            "強而避之": "Using proxy conflicts instead of direct military engagement",
            "怒而撓之": "Using public shaming or flattery to influence diplomatic positions",
            "卑而驕之": "Cultural exchange programs with hidden agendas",
            "佚而勞之": "Endless rounds of talks that exhaust diplomatic resources",
            "親而離之": "Offering bilateral deals that undermine multilateral agreements",
            "攻其無備，出其不意": "Sudden policy announcements that change the diplomatic landscape"
        }
        return examples.get(technique, "Various applications in international relations")

    async def _store_analysis_result(self, result: Dict[str, Any]) -> None:
        """Store analysis result in vector database."""
        try:
            # Create a summary for storage
            summary = f"Art of War Deception Analysis - {result['analysis_type']} - {result['timestamp']}"
            
            # Store in vector database
            await self.vector_store.store_document(
                collection_name="art_of_war_analysis",
                content=summary,
                metadata={
                    "type": "art_of_war_deception_analysis",
                    "analysis_type": result["analysis_type"],
                    "timestamp": result["timestamp"],
                    "success": result["success"]
                }
            )
            
            logger.info("Analysis result stored in vector database")
            
        except Exception as e:
            logger.warning(f"Could not store analysis result: {e}")

    async def search_deception_patterns(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for deception patterns in stored analyses.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Dictionary containing search results
        """
        try:
            results = await self.vector_store.query(
                collection_name="art_of_war_analysis",
                query_text=query,
                n_results=n_results
            )
            
            return {
                "success": True,
                "query": query,
                "results": results,
                "count": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error searching deception patterns: {e}")
            return {"success": False, "error": str(e)}

    async def generate_deception_report(self, 
                                      analysis_type: str = "comprehensive",
                                      format: str = "markdown") -> Dict[str, Any]:
        """
        Generate a comprehensive deception analysis report.
        
        Args:
            analysis_type: Type of analysis to include
            format: Report format ("markdown", "json", "html")
            
        Returns:
            Dictionary containing the report
        """
        try:
            # Perform the analysis
            analysis = await self.analyze_deception_techniques(
                analysis_type=analysis_type,
                include_modern_applications=True,
                include_ethical_considerations=True
            )
            
            # Generate report based on format
            if format == "markdown":
                report = self._generate_markdown_report(analysis)
            elif format == "json":
                report = analysis
            elif format == "html":
                report = self._generate_html_report(analysis)
            else:
                report = analysis
            
            # Save report
            report_path = report_manager.save_report(
                content=report,
                report_type="art_of_war_deception_analysis",
                filename=f"art_of_war_deception_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            )
            
            return {
                "success": True,
                "report": report,
                "report_path": str(report_path),
                "format": format
            }
            
        except Exception as e:
            logger.error(f"Error generating deception report: {e}")
            return {"success": False, "error": str(e)}

    def _generate_markdown_report(self, analysis: Dict[str, Any]) -> str:
        """Generate markdown report from analysis results."""
        report = f"""# Art of War Deception Techniques in Modern Diplomacy

*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary

This analysis examines the deception and misdirection techniques described in Sun Tzu's *The Art of War* and their potential applications in contemporary diplomatic conflicts.

---

## Core Deception Principles

### The Way of Deception (詭道)

The fundamental principle of *The Art of War* is that **"{analysis['core_principles']['fundamental_principle']['chinese']}"** - "{analysis['core_principles']['fundamental_principle']['translation']}."

{analysis['core_principles']['fundamental_principle']['explanation']}

### Key Strategic Concepts

"""
        
        for concept in analysis['core_principles']['key_concepts']:
            report += f"- {concept}\n"
        
        report += "\n---\n\n## Specific Deception Techniques\n\n"
        
        # Add techniques
        for technique_id, technique_data in analysis['techniques'].items():
            report += f"### {technique_data['chinese']}\n\n"
            report += f"**Translation**: {technique_data['translation']}\n\n"
            report += f"**Explanation**: {technique_data['explanation']}\n\n"
            report += f"**Modern Application**: {technique_data['modern_application']}\n\n"
            report += f"**Diplomatic Example**: {technique_data['diplomatic_example']}\n\n"
        
        # Add modern applications
        if analysis.get('modern_applications'):
            report += "---\n\n## Modern Diplomatic Applications\n\n"
            for category, details in analysis['modern_applications'].items():
                report += f"### {category.replace('_', ' ').title()}\n\n"
                report += f"**Technique**: {details['technique']}\n\n"
                report += f"**Art of War Basis**: {details['art_of_war_basis']}\n\n"
                report += "**Modern Examples**:\n"
                for example in details['modern_examples']:
                    report += f"- {example}\n"
                report += f"\n**Diplomatic Impact**: {details['diplomatic_impact']}\n\n"
        
        # Add ethical considerations
        if analysis.get('ethical_considerations'):
            report += "---\n\n## Ethical Considerations\n\n"
            report += "### Legitimate vs. Unethical Deception\n\n"
            report += "**Legitimate Strategic Deception:**\n"
            for item in analysis['ethical_considerations']['legitimate_vs_unethical']['legitimate']:
                report += f"- {item}\n"
            report += "\n**Unethical Manipulation:**\n"
            for item in analysis['ethical_considerations']['legitimate_vs_unethical']['unethical']:
                report += f"- {item}\n"
        
        # Add counter strategies
        if analysis.get('counter_strategies'):
            report += "\n---\n\n## Counter-Deception Strategies\n\n"
            for category, items in analysis['counter_strategies'].items():
                report += f"### {category.replace('_', ' ').title()}\n\n"
                for item in items:
                    report += f"- {item}\n"
                report += "\n"
        
        # Add recommendations
        if analysis.get('recommendations'):
            report += "---\n\n## Recommendations\n\n"
            for category, items in analysis['recommendations'].items():
                report += f"### {category.replace('_', ' ').title()}\n\n"
                for item in items:
                    report += f"- {item}\n"
                report += "\n"
        
        report += """---

## Conclusion

The deception techniques described in *The Art of War* remain relevant to modern diplomatic conflicts, but their application requires careful consideration of ethical, legal, and strategic factors.

---

*This analysis was generated using systematic examination of Sun Tzu's The Art of War and its applications to modern diplomatic practice.*
"""
        
        return report

    def _generate_html_report(self, analysis: Dict[str, Any]) -> str:
        """Generate HTML report from analysis results."""
        # Convert markdown to HTML (simplified version)
        markdown_report = self._generate_markdown_report(analysis)
        
        # Simple markdown to HTML conversion
        html = markdown_report.replace("# ", "<h1>").replace("\n", "</h1>\n")
        html = html.replace("## ", "<h2>").replace("\n", "</h2>\n")
        html = html.replace("### ", "<h3>").replace("\n", "</h3>\n")
        html = html.replace("- ", "<li>").replace("\n", "</li>\n")
        html = html.replace("**", "<strong>").replace("**", "</strong>")
        html = html.replace("*", "<em>").replace("*", "</em>")
        
        # Wrap in HTML structure
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Art of War Deception Analysis</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1, h2, h3 {{ color: #333; }}
        .technique {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007acc; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
        
        return html
