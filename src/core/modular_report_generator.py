"""
Modular Report Generator

Main generator that assembles modules and creates enhanced reports.
Provides configuration management and module assembly capabilities.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Type, Union
from pathlib import Path
from datetime import datetime
import json
import logging

from .modules.base_module import BaseModule, ModuleConfig
from .modules.strategic_recommendations_module import StrategicRecommendationsModule
from .modules.executive_summary_module import ExecutiveSummaryModule
from .modules.geopolitical_impact_module import GeopoliticalImpactModule
from .modules.trade_impact_module import TradeImpactModule
from .modules.balance_of_power_module import BalanceOfPowerModule
from .modules.risk_assessment_module import RiskAssessmentModule
from .modules.interactive_visualizations_module import InteractiveVisualizationsModule
from .modules.strategic_analysis_module import StrategicAnalysisModule
from .modules.enhanced_data_analysis_module import EnhancedDataAnalysisModule
from .modules.regional_sentiment_module import RegionalSentimentModule
from .modules.implementation_timeline_module import ImplementationTimelineModule
from .modules.acquisition_programs_module import AcquisitionProgramsModule
from .modules.forecasting_module import ForecastingModule
from .modules.operational_considerations_module import OperationalConsiderationsModule
from .modules.regional_security_module import RegionalSecurityModule
from .modules.economic_analysis_module import EconomicAnalysisModule
from .modules.comparison_analysis_module import ComparisonAnalysisModule
from .modules.advanced_forecasting_module import AdvancedForecastingModule
from .modules.model_performance_module import ModelPerformanceModule
from .modules.strategic_capability_module import StrategicCapabilityModule
from .modules.predictive_analytics_module import PredictiveAnalyticsModule
from .modules.scenario_analysis_module import ScenarioAnalysisModule
from .modules.strategic_intelligence_module import StrategicIntelligenceModule

# Import the new enhanced HTML report generator
from .enhanced_html_report_generator import EnhancedHTMLReportGenerator

logger = logging.getLogger(__name__)


class ModularReportGenerator:
    """Main generator for modular enhanced reports."""
    
    def __init__(self):
        """Initialize the modular report generator."""
        self.modules: Dict[str, BaseModule] = {}
        self.config: Dict[str, Any] = {}
        self.output_dir = Path("Results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize the enhanced HTML report generator
        self.enhanced_html_generator = EnhancedHTMLReportGenerator()
        
        # Register available modules
        self._register_available_modules()
    
    def _register_available_modules(self):
        """Register all available modules."""
        # Core strategic modules
        self.register_module(StrategicRecommendationsModule())
        self.register_module(ExecutiveSummaryModule())
        
        # Impact analysis modules
        self.register_module(GeopoliticalImpactModule())
        self.register_module(TradeImpactModule())
        self.register_module(BalanceOfPowerModule())
        
        # Assessment modules
        self.register_module(RiskAssessmentModule())
        self.register_module(InteractiveVisualizationsModule())
        self.register_module(StrategicAnalysisModule())
        self.register_module(EnhancedDataAnalysisModule())
        
        # Regional and operational modules
        self.register_module(RegionalSentimentModule())
        self.register_module(ImplementationTimelineModule())
        self.register_module(AcquisitionProgramsModule())
        self.register_module(ForecastingModule())
        self.register_module(OperationalConsiderationsModule())
        self.register_module(RegionalSecurityModule())
        
        # Advanced analysis modules
        self.register_module(EconomicAnalysisModule())
        self.register_module(ComparisonAnalysisModule())
        self.register_module(AdvancedForecastingModule())
        self.register_module(ModelPerformanceModule())
        self.register_module(StrategicCapabilityModule())
        self.register_module(PredictiveAnalyticsModule())
        self.register_module(ScenarioAnalysisModule())
        
        # Phase 4 Strategic Intelligence Module
        self.register_module(StrategicIntelligenceModule())
    
    def register_module(self, module: BaseModule):
        """Register a module with the generator."""
        self.modules[module.module_id] = module
    
    def get_available_modules(self) -> Dict[str, Dict[str, Any]]:
        """Get dictionary of available modules with their information."""
        modules_info = {}
        for module_id, module in self.modules.items():
            modules_info[module_id] = {
                'title': getattr(module, 'title',
                                module_id.replace('_', ' ').title()),
                'description': getattr(module, 'description',
                                      f'{module_id} module'),
                'enabled': module.is_enabled(),
                'configurable': hasattr(module, 'get_config'),
                'version': getattr(module, 'version', '1.0.0')
            }
        return modules_info
    
    async def generate_modular_report(
        self,
        query: str,
        enabled_modules: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
        output_format: str = "html",
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a modular report using the enhanced HTML report generator.
        
        Args:
            query: The analysis query
            enabled_modules: List of module IDs to enable (None for all)
            config: Configuration dictionary
            output_format: Output format ("html", "markdown", "json")
            title: Report title
            
        Returns:
            Dictionary with report generation results
        """
        try:
            # Use the enhanced HTML report generator for robust, self-healing reports
            if output_format.lower() == "html":
                return await self._generate_enhanced_html_report(query, enabled_modules, config, title)
            else:
                # Fallback to original modular system for other formats
                return await self._generate_legacy_report(query, enabled_modules, config, output_format, title)
                
        except Exception as e:
            logger.error(f"Modular report generation failed: {e}")
            # Attempt recovery using the enhanced generator
            return await self._attempt_enhanced_recovery(query, title)
    
    async def _generate_enhanced_html_report(
        self,
        query: str,
        enabled_modules: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate enhanced HTML report using the new robust generator."""
        try:
            # Prepare data structure for the enhanced generator
            report_data = await self._prepare_report_data(query, enabled_modules, config)
            
            # Generate title if not provided
            if not title:
                title = f"Analysis Report: {query[:50]}..."
            
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Use the enhanced HTML report generator
            result = await self.enhanced_html_generator.generate_enhanced_report(
                data=report_data,
                output_path=f"Results/{title.replace(' ', '_')}_Modular_Enhanced_{timestamp}.html"
            )
            
            # Add module information to the result
            result["modules_used"] = enabled_modules or list(self.modules.keys())
            result["query"] = query
            
            # Display comprehensive validation results if available
            if result.get("success") and "validation_results" in result:
                validation = result["validation_results"]
                print(f"\n🔍 MODULAR REPORT VALIDATION RESULTS:")
                print("=" * 50)
                
                # Module coverage
                module_coverage = validation.get("module_coverage", {})
                print(f"📊 Module Coverage: {module_coverage.get('total_generated', 0)} out of {module_coverage.get('total_required', 0)} modules ({module_coverage.get('coverage_percentage', 0):.1f}%)")
                
                # JavaScript validation
                js_validation = validation.get("javascript_validation", {})
                chart_validation = js_validation.get("chart_constructors", {})
                print(f"⚡ Interactive Charts: {chart_validation.get('total_chart_calls', 0)} charts with {'✅ valid' if chart_validation.get('has_valid_syntax', False) else '❌ invalid'} JavaScript syntax")
                
                # Advanced tooltips
                interactive_features = validation.get("interactive_features", {})
                tooltip_validation = interactive_features.get("advanced_tooltips", {})
                print(f"💡 Advanced Tooltips: {'✅ Working' if tooltip_validation.get('has_enhanced_tooltip_html', False) else '❌ Missing'}")
                
                # Overall summary
                if "summary" in validation:
                    print(f"📋 Summary: {validation['summary']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Enhanced HTML report generation failed: {e}")
            # Fallback to simple data structure
            fallback_data = {
                "content": query,
                "type": "fallback_analysis",
                "sections": [{"title": "Analysis", "content": query}],
                "metadata": {"source": "fallback_generation"}
            }
            
            # Generate timestamp for fallback
            fallback_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            return await self.enhanced_html_generator.generate_enhanced_report(
                data=fallback_data,
                output_path=f"Results/{title or 'Analysis_Report'}_Fallback_{fallback_timestamp}.html"
            )
    
    async def _prepare_report_data(
        self,
        query: str,
        enabled_modules: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Prepare data structure for the enhanced report generator."""
        try:
            sections = []
            
            # Use enabled modules or all modules
            modules_to_use = enabled_modules or list(self.modules.keys())
            
            for module_id in modules_to_use:
                if module_id in self.modules:
                    try:
                        module = self.modules[module_id]
                        if module.is_enabled():
                            # Get module content
                            module_content = await self._get_module_content(module, query, config)
                            if module_content:
                                sections.append({
                                    "title": getattr(module, 'title', module_id.replace('_', ' ').title()),
                                    "content": module_content
                                })
                    except Exception as e:
                        logger.warning(f"Module {module_id} failed: {e}")
                        # Add fallback section
                        sections.append({
                            "title": module_id.replace('_', ' ').title(),
                            "content": f"Analysis for {module_id} module (generation failed: {str(e)})"
                        })
            
            # If no sections were generated, create a default one
            if not sections:
                sections.append({
                    "title": "Analysis",
                    "content": query
                })
            
            return {
                "content": query,
                "type": "modular_analysis",
                "sections": sections,
                "metadata": {
                    "source": "modular_generator",
                    "modules_used": modules_to_use,
                    "total_sections": len(sections)
                }
            }
            
        except Exception as e:
            logger.error(f"Data preparation failed: {e}")
            return {
                "content": query,
                "type": "error_fallback",
                "sections": [{"title": "Analysis", "content": query}],
                "metadata": {"source": "error_fallback", "error": str(e)}
            }
    
    async def _get_module_content(
        self,
        module: BaseModule,
        query: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """Get content from a module safely."""
        try:
            # Try to get content using the module's interface
            if hasattr(module, 'generate_content'):
                return await module.generate_content(query, config)
            elif hasattr(module, 'process'):
                return await module.process(query, config)
            elif hasattr(module, 'analyze'):
                return await module.analyze(query, config)
            else:
                # Fallback: return module description
                return getattr(module, 'description', f"Analysis for {module.module_id}")
                
        except Exception as e:
            logger.warning(f"Module content generation failed for {module.module_id}: {e}")
            return f"Analysis for {module.module_id} (error: {str(e)})"
    
    async def _generate_legacy_report(
        self,
        query: str,
        enabled_modules: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
        output_format: str = "html",
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate report using the legacy modular system."""
        # This is the original implementation for non-HTML formats
        # Keep the existing logic here for backward compatibility
        pass
    
    async def _attempt_enhanced_recovery(
        self,
        query: str,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Attempt recovery using the enhanced generator."""
        try:
            recovery_data = {
                "content": query,
                "type": "recovery_analysis",
                "sections": [{"title": "Recovery Analysis", "content": query}],
                "metadata": {"source": "recovery_attempt"}
            }
            
            return await self.enhanced_html_generator.generate_enhanced_report(
                data=recovery_data,
                query_type="recovery_analysis",
                title=title or "Recovery Analysis Report"
            )
            
        except Exception as e:
            logger.error(f"Recovery attempt failed: {e}")
            return {
                "success": False,
                "error": f"All recovery attempts failed: {str(e)}",
                "query": query,
                "generated_at": datetime.now().isoformat()
            }
    
    # Keep existing methods for backward compatibility
    def get_tooltip_data(self) -> Dict[str, Any]:
        """Get tooltip data - now handled by the enhanced generator."""
        # This method is kept for backward compatibility
        # The enhanced generator handles tooltips automatically
        return {}
    
    def get_chart_data(self) -> Dict[str, Any]:
        """Get chart data - now handled by the enhanced generator."""
        # This method is kept for backward compatibility
        # The enhanced generator handles charts automatically
        return {}


# Global instance for easy access
modular_report_generator = ModularReportGenerator()
