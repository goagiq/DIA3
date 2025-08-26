#!/usr/bin/env python3
"""
Comprehensive Category Detection System
Determines which report categories are relevant based on content analysis.
"""

import re
import logging
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class CategoryInfo:
    """Information about a report category."""
    name: str
    description: str
    keywords: List[str]
    required_analysis_types: List[str]
    priority: int  # 1-5, where 1 is highest priority
    always_include: bool = False
    data_sources: List[str] = None
    internal_sources: List[str] = None
    external_sources: List[str] = None
    intelligence_required: bool = False


class ComprehensiveCategoryDetector:
    """Detects relevant report categories based on content analysis."""
    
    def __init__(self):
        self.categories = self._initialize_categories()
        
    def _initialize_categories(self) -> Dict[str, CategoryInfo]:
        """Initialize all available report categories."""
        return {
            "executive_summary": CategoryInfo(
                name="Executive Summary",
                description="High-level overview and key findings for decision-makers",
                keywords=["executive", "summary", "overview", "key findings", "decision", "leadership"],
                required_analysis_types=["summary", "overview"],
                priority=1,
                always_include=True,
                data_sources=["internal_analysis", "key_metrics", "stakeholder_input"],
                internal_sources=["DIA3 - Executive Dashboard", "DIA3 - Key Performance Indicators"],
                external_sources=["industry_reports", "market_analysis"],
                intelligence_required=False
            ),
            "geopolitical_impact_analysis": CategoryInfo(
                name="Geopolitical Impact Analysis",
                description="Analysis of political and geographical implications",
                keywords=["geopolitical", "political", "geography", "international", "diplomatic", "foreign policy", "nation", "country", "region"],
                required_analysis_types=["geopolitical", "political", "international"],
                priority=2,
                data_sources=["political_analysis", "diplomatic_reports", "regional_intelligence"],
                internal_sources=["DIA3 - Geopolitical Intelligence", "DIA3 - Regional Analysis"],
                external_sources=["UN_reports", "diplomatic_correspondence", "regional_news"],
                intelligence_required=True
            ),
            "trade_economic_impact": CategoryInfo(
                name="Trade and Economic Impact",
                description="Analysis of trade relationships and economic consequences",
                keywords=["trade", "economic", "commerce", "import", "export", "market", "economy", "financial", "business", "commercial"],
                required_analysis_types=["economic", "trade", "financial"],
                priority=2,
                data_sources=["trade_data", "economic_indicators", "market_analysis"],
                internal_sources=["DIA3 - Trade Intelligence", "DIA3 - Economic Analysis"],
                external_sources=["WTO_data", "IMF_reports", "central_bank_data"],
                intelligence_required=True
            ),
            "security_implications": CategoryInfo(
                name="Security Implications",
                description="Security and defense-related implications and risks",
                keywords=["security", "defense", "military", "threat", "risk", "vulnerability", "protection", "safety", "cyber", "intelligence"],
                required_analysis_types=["security", "defense", "threat"],
                priority=2,
                data_sources=["threat_intelligence", "security_assessments", "defense_analysis"],
                internal_sources=["DIA3 - Threat Assessment", "DIA3 - Security Analysis"],
                external_sources=["defense_reports", "security_briefings", "intelligence_communities"],
                intelligence_required=True
            ),
            "economic_implications": CategoryInfo(
                name="Economic Implications",
                description="Broader economic consequences and market impacts",
                keywords=["economic", "economy", "market", "financial", "fiscal", "monetary", "inflation", "growth", "recession", "gdp"],
                required_analysis_types=["economic", "financial"],
                priority=2
            ),
            "financial_implications": CategoryInfo(
                name="Financial Implications",
                description="Specific financial impacts and investment considerations",
                keywords=["financial", "investment", "funding", "budget", "cost", "revenue", "profit", "loss", "capital", "finance"],
                required_analysis_types=["financial", "investment"],
                priority=3
            ),
            "regional_analysis": CategoryInfo(
                name="Regional Analysis",
                description="Analysis specific to geographical regions or areas",
                keywords=["regional", "region", "area", "territory", "zone", "district", "province", "state", "local"],
                required_analysis_types=["regional", "geographical"],
                priority=3
            ),
            "comparative_analysis": CategoryInfo(
                name="Comparative Analysis",
                description="Comparison between different options, scenarios, or entities",
                keywords=["compare", "comparison", "versus", "vs", "alternative", "option", "choice", "different", "similar", "contrast"],
                required_analysis_types=["comparative", "analysis"],
                priority=3
            ),
            "predictive_analysis_insights": CategoryInfo(
                name="Predictive Analysis and Insights",
                description="Future predictions and trend analysis",
                keywords=["predict", "forecast", "future", "trend", "projection", "outlook", "prediction", "forecasting", "scenario"],
                required_analysis_types=["predictive", "forecasting"],
                priority=2
            ),
            "strategic_options_assessment": CategoryInfo(
                name="Strategic Options Assessment & Comparison",
                description="Evaluation and comparison of strategic options",
                keywords=["strategic", "strategy", "option", "choice", "decision", "plan", "approach", "method", "tactic"],
                required_analysis_types=["strategic", "planning"],
                priority=2
            ),
            "option_evaluation": CategoryInfo(
                name="Option Evaluation",
                description="Detailed evaluation of specific options or alternatives",
                keywords=["evaluate", "evaluation", "assess", "assessment", "option", "alternative", "choice", "select", "compare"],
                required_analysis_types=["evaluation", "assessment"],
                priority=3
            ),
            "advanced_forecasting": CategoryInfo(
                name="Advanced Forecasting",
                description="Sophisticated forecasting models and predictions",
                keywords=["forecast", "forecasting", "prediction", "model", "simulation", "projection", "future", "trend", "advanced"],
                required_analysis_types=["forecasting", "modeling"],
                priority=2
            ),
            "capability_forecasts": CategoryInfo(
                name="Capability Forecasts",
                description="Predictions about future capabilities and capacities",
                keywords=["capability", "capacity", "ability", "skill", "competence", "forecast", "prediction", "future"],
                required_analysis_types=["capability", "forecasting"],
                priority=3
            ),
            "five_year_strategic_horizon": CategoryInfo(
                name="5-Year Strategic Horizon",
                description="Long-term strategic planning and outlook",
                keywords=["5 year", "five year", "long term", "strategic", "horizon", "planning", "future", "outlook", "vision"],
                required_analysis_types=["strategic", "long_term"],
                priority=2
            ),
            "capability_planning": CategoryInfo(
                name="Capability Planning",
                description="Planning for future capabilities and resource allocation",
                keywords=["capability", "planning", "resource", "allocation", "development", "build", "create", "establish"],
                required_analysis_types=["planning", "capability"],
                priority=3
            ),
            "strategic_use_cases": CategoryInfo(
                name="Strategic Use Cases",
                description="Strategic applications and use case scenarios",
                keywords=["use case", "application", "scenario", "situation", "context", "usage", "implementation"],
                required_analysis_types=["use_case", "application"],
                priority=3
            ),
            "strategic_development": CategoryInfo(
                name="Strategic Development",
                description="Development of strategic initiatives and programs",
                keywords=["development", "strategic", "initiative", "program", "project", "build", "create", "establish"],
                required_analysis_types=["development", "strategic"],
                priority=3
            ),
            "feature_importance_analysis": CategoryInfo(
                name="Feature Importance Analysis",
                description="Analysis of key features and their relative importance",
                keywords=["feature", "importance", "key", "critical", "essential", "priority", "rank", "weight"],
                required_analysis_types=["analysis", "feature"],
                priority=4
            ),
            "scenario_analysis_overview": CategoryInfo(
                name="Scenario Analysis Overview",
                description="Overview of different scenarios and their implications",
                keywords=["scenario", "situation", "case", "condition", "circumstance", "overview", "summary"],
                required_analysis_types=["scenario", "analysis"],
                priority=3
            ),
            "prediction_scenarios": CategoryInfo(
                name="Prediction Scenarios",
                description="Different prediction scenarios and outcomes",
                keywords=["prediction", "scenario", "outcome", "result", "forecast", "projection", "future"],
                required_analysis_types=["prediction", "scenario"],
                priority=3
            ),
            "multi_scenario_analysis": CategoryInfo(
                name="Multi-Scenario Analysis",
                description="Analysis across multiple scenarios and conditions",
                keywords=["multi scenario", "multiple", "scenario", "analysis", "comparison", "different", "various"],
                required_analysis_types=["scenario", "analysis"],
                priority=3
            ),
            "risk_assessment": CategoryInfo(
                name="Risk Assessment",
                description="Comprehensive risk analysis and evaluation",
                keywords=["risk", "threat", "vulnerability", "danger", "hazard", "assessment", "evaluation", "analysis"],
                required_analysis_types=["risk", "assessment"],
                priority=2
            ),
            "strategic_recommendations": CategoryInfo(
                name="Strategic Recommendations",
                description="Strategic recommendations and actionable insights",
                keywords=["recommendation", "suggestion", "advice", "guidance", "strategy", "action", "plan"],
                required_analysis_types=["recommendation", "strategic"],
                priority=1,
                data_sources=["intelligence_synthesis", "strategic_analysis", "expert_consultation"],
                internal_sources=["DIA3 - Intelligence Synthesis", "DIA3 - Strategic Analysis", "DIA3 - Expert Knowledge Base"],
                external_sources=["expert_opinions", "strategic_consultations", "industry_best_practices"],
                intelligence_required=True
            ),
            "conclusion": CategoryInfo(
                name="Conclusion",
                description="Summary of findings and final conclusions",
                keywords=["conclusion", "summary", "final", "end", "result", "finding", "outcome"],
                required_analysis_types=["summary", "conclusion"],
                priority=1,
                always_include=True,
                data_sources=["synthesis_analysis", "key_findings", "final_assessment"],
                internal_sources=["DIA3 - Analysis Synthesis", "DIA3 - Key Findings Database"],
                external_sources=["final_reports", "summary_documents"],
                intelligence_required=False
            )
        }
    
    def detect_relevant_categories(
        self, 
        content: str, 
        topic: str = "", 
        use_case: str = "", 
        query: str = ""
    ) -> Dict[str, Any]:
        """
        Detect which categories are relevant based on content analysis.
        
        Args:
            content: The main content to analyze
            topic: The topic of the report
            use_case: The use case or context
            query: The original query or request
            
        Returns:
            Dictionary with detected categories and their relevance scores
        """
        try:
            # Combine all text for analysis
            combined_text = f"{content} {topic} {use_case} {query}".lower()
            
            detected_categories = {}
            
            for category_id, category_info in self.categories.items():
                relevance_score = self._calculate_relevance_score(
                    combined_text, category_info
                )
                
                if relevance_score > 0 or category_info.always_include:
                    detected_categories[category_id] = {
                        "name": category_info.name,
                        "description": category_info.description,
                        "relevance_score": relevance_score,
                        "priority": category_info.priority,
                        "always_include": category_info.always_include,
                        "keywords_found": self._find_matching_keywords(
                            combined_text, category_info.keywords
                        )
                    }
            
            # Sort by priority and relevance score
            sorted_categories = dict(sorted(
                detected_categories.items(),
                key=lambda x: (x[1]["priority"], -x[1]["relevance_score"])
            ))
            
            return {
                "detected_categories": sorted_categories,
                "total_categories": len(sorted_categories),
                "analysis_timestamp": datetime.now().isoformat(),
                "content_length": len(content),
                "topic": topic,
                "use_case": use_case,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error detecting categories: {e}")
            return {
                "error": str(e),
                "detected_categories": {},
                "total_categories": 0
            }
    
    def _calculate_relevance_score(self, text: str, category_info: CategoryInfo) -> float:
        """Calculate relevance score for a category based on keyword matches."""
        score = 0.0
        
        for keyword in category_info.keywords:
            # Count exact matches
            exact_matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
            score += exact_matches * 2.0
            
            # Count partial matches
            partial_matches = len(re.findall(re.escape(keyword), text))
            score += (partial_matches - exact_matches) * 0.5
        
        # Normalize score
        return min(score / 10.0, 1.0)
    
    def _find_matching_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """Find which keywords from a category are present in the text."""
        found_keywords = []
        
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                found_keywords.append(keyword)
        
        return found_keywords
    
    def get_category_info(self, category_id: str) -> CategoryInfo:
        """Get information about a specific category."""
        return self.categories.get(category_id)
    
    def get_all_categories(self) -> Dict[str, CategoryInfo]:
        """Get all available categories."""
        return self.categories.copy()
    
    def get_required_categories(self) -> List[str]:
        """Get categories that should always be included."""
        return [
            category_id for category_id, info in self.categories.items()
            if info.always_include
        ]
    
    def get_category_data_sources(self, category_id: str) -> Dict[str, Any]:
        """Get data sources for a specific category."""
        category_info = self.categories.get(category_id)
        if not category_info:
            return {}
        
        return {
            "data_sources": category_info.data_sources or [],
            "internal_sources": category_info.internal_sources or [],
            "external_sources": category_info.external_sources or [],
            "intelligence_required": category_info.intelligence_required
        }
    
    def get_intelligence_categories(self) -> List[str]:
        """Get categories that require DIA3 intelligence synthesis."""
        return [
            category_id for category_id, info in self.categories.items()
            if info.intelligence_required
        ]
    
    def get_all_data_sources(self) -> Dict[str, List[str]]:
        """Get all data sources organized by type."""
        all_sources = {
            "internal": [],
            "external": [],
            "data_types": []
        }
        
        for category_info in self.categories.values():
            if category_info.internal_sources:
                all_sources["internal"].extend(category_info.internal_sources)
            if category_info.external_sources:
                all_sources["external"].extend(category_info.external_sources)
            if category_info.data_sources:
                all_sources["data_types"].extend(category_info.data_sources)
        
        # Remove duplicates
        all_sources["internal"] = list(set(all_sources["internal"]))
        all_sources["external"] = list(set(all_sources["external"]))
        all_sources["data_types"] = list(set(all_sources["data_types"]))
        
        return all_sources
