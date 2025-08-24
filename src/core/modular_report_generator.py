"""
Modular Report Generator

Main generator that assembles modules and creates enhanced reports.
Provides configuration management and module assembly capabilities.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Type
from pathlib import Path
from datetime import datetime
import json

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


class ModularReportGenerator:
    """Main generator for modular enhanced reports."""
    
    def __init__(self):
        """Initialize the modular report generator."""
        self.modules: Dict[str, BaseModule] = {}
        self.config: Dict[str, Any] = {}
        self.output_dir = Path("Results")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
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
                'order': module.get_order(),
                'category': getattr(module, 'category', 'general')
            }
        return modules_info
    
    def get_available_module_ids(self) -> List[str]:
        """Get list of available module IDs (for backward compatibility)."""
        return list(self.modules.keys())
    
    def get_module(self, module_id: str) -> Optional[BaseModule]:
        """Get a module by ID."""
        return self.modules.get(module_id)
    
    def enable_module(self, module_id: str, enabled: bool = True):
        """Enable or disable a module."""
        module = self.get_module(module_id)
        if module:
            module.config.enabled = enabled
    
    def set_module_enabled(self, module_id: str, enabled: bool = True):
        """Set module enabled status (alias for enable_module)."""
        self.enable_module(module_id, enabled)
    
    def set_module_order(self, module_id: str, order: int):
        """Set the display order for a module."""
        module = self.get_module(module_id)
        if module:
            module.config.order = order
    
    def configure_module(self, module_id: str, config: Dict[str, Any]):
        """Configure a module with custom settings."""
        module = self.get_module(module_id)
        if module:
            module.import_config(config)
    
    def get_enabled_modules(self) -> List[BaseModule]:
        """Get list of enabled modules sorted by order."""
        enabled_modules = [m for m in self.modules.values() if m.is_enabled()]
        return sorted(enabled_modules, key=lambda m: m.get_order())
    
    async def generate_modular_report(
        self,
        topic: str,
        data: Dict[str, Any],
        enabled_modules: Optional[List[str]] = None,
        report_title: Optional[str] = None,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a modular enhanced report.
        
        Args:
            topic: The analysis topic
            data: Analysis data for all modules
            enabled_modules: List of module IDs to enable (None for all)
            report_title: Custom report title
            custom_config: Custom configuration for modules
            
        Returns:
            Dictionary with report generation results
        """
        try:
            # Apply custom configuration
            if custom_config:
                self._apply_custom_config(custom_config)
            
            # Enable/disable modules as specified
            if enabled_modules is not None:
                for module_id in self.modules:
                    self.enable_module(module_id, module_id in enabled_modules)
            
            # Get enabled modules
            active_modules = self.get_enabled_modules()
            
            if not active_modules:
                raise ValueError("No modules are enabled for report generation")
            
            # Generate report content
            report_content = await self._generate_report_content(
                topic, data, active_modules, report_title
            )
            
            # Generate filename with proper sanitization
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_topic = self._sanitize_filename(topic.lower())
            filename = f"{sanitized_topic}_modular_enhanced_analysis_{timestamp}.html"
            file_path = self.output_dir / filename
            
            # Write report to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # Generate metadata
            metadata = self._generate_report_metadata(
                topic, active_modules, file_path, data
            )
            
            return {
                "success": True,
                "file_path": str(file_path),
                "filename": filename,
                "file_size": file_path.stat().st_size,
                "modules_used": [m.module_id for m in active_modules],
                "metadata": metadata,
                "generated_at": datetime.now().isoformat(),
                "html_content": report_content
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "topic": topic,
                "generated_at": datetime.now().isoformat()
            }
    
    async def _generate_report_content(
        self,
        topic: str,
        data: Dict[str, Any],
        modules: List[BaseModule],
        report_title: Optional[str] = None
    ) -> str:
        """Generate the complete HTML report content using enhanced template."""
        
        # Try to load the enhanced template from multiple locations
        template_paths = [
            Path(__file__).parent / "templates" / "default_enhanced_html_template.html",
            Path("templates/enhanced_report_template.html"),
            Path(__file__).parent.parent.parent / "templates" / "enhanced_report_template.html"
        ]
        
        template_content = None
        for template_path in template_paths:
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                break
        
        if template_content is None:
            # Fallback to basic template if enhanced template not found
            return self._generate_basic_report_content(topic, data, modules, report_title)
        
        # Prepare template data
        template_data = self._prepare_template_data(topic, data, modules, report_title)
        
        # Replace template placeholders
        html_content = template_content
        
        # Replace basic placeholders
        html_content = html_content.replace("{{title}}", template_data["title"])
        html_content = html_content.replace("{{timestamp}}", template_data["timestamp"])
        html_content = html_content.replace("{{executive_summary}}", template_data["executive_summary"])
        html_content = html_content.replace("{{estimated_cost}}", template_data["estimated_cost"])
        
        # Replace modules section with actual module content
        modules_html = self._generate_modules_html(modules, data)
        html_content = html_content.replace("{{#each modules}}", "")
        html_content = html_content.replace("{{/each}}", "")
        html_content = html_content.replace("{{#each modules}}", "")
        html_content = html_content.replace("{{/each}}", "")
        
        # Insert modules content
        html_content = html_content.replace("<!-- Module Sections -->", modules_html)
        
        # Replace module-specific placeholders
        for module in modules:
            module_id = module.module_id
            html_content = html_content.replace(f"{{{{module_id}}}}", module_id)
            tooltip_data = module.get_tooltip_data()
            chart_data = module.get_chart_data()
            
            # Convert tooltip data to JSON string
            tooltip_json = json.dumps(tooltip_data, default=str)
            chart_json = json.dumps(chart_data, default=str)
            
            html_content = html_content.replace(f"{{{{tooltip_data}}}}", tooltip_json)
            html_content = html_content.replace(f"{{{{chart_data}}}}", chart_json)
        
        return html_content
    
    def _generate_basic_report_content(
        self,
        topic: str,
        data: Dict[str, Any],
        modules: List[BaseModule],
        report_title: Optional[str] = None
    ) -> str:
        """Generate basic HTML report content as fallback."""
        
        # Generate header
        header_html = self._generate_header(topic, report_title)
        
        # Generate module content
        module_content = []
        module_scripts = []
        
        for module in modules:
            try:
                # Validate module data
                module.validate_data(data)
                
                # Generate module content
                content = module.generate_content(data)
                module_content.append(content)
                
                # Generate module scripts
                tooltip_script = module.generate_tooltip_script()
                chart_script = module.generate_chart_script()
                
                if tooltip_script:
                    module_scripts.append(tooltip_script)
                if chart_script:
                    module_scripts.append(chart_script)
                    
            except Exception as e:
                # Log error and continue with other modules
                print(f"Error generating content for module {module.module_id}: {e}")
                continue
        
        # Generate CSS styles
        css_styles = self._generate_css_styles()
        
        # Generate JavaScript
        javascript = self._generate_javascript(module_scripts)
        
        # Assemble complete HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title or f"{topic}: Modular Enhanced Analysis"}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {css_styles}
    </style>
</head>
<body>
    {header_html}
    
    <div class="container">
        {''.join(module_content)}
    </div>
    
    <!-- Enhanced Tooltip -->
    <div class="enhanced-tooltip" id="enhancedTooltip">
        <div class="tooltip-title" id="tooltipTitle"></div>
        <div class="tooltip-content" id="tooltipContent"></div>
        <div class="tooltip-source" id="tooltipSource"></div>
        <div class="tooltip-strategic" id="tooltipStrategic"></div>
        <div class="tooltip-recommendations" id="tooltipRecommendations"></div>
        <div class="tooltip-use-cases" id="tooltipUseCases"></div>
    </div>
    
    <script>
        {javascript}
    </script>
</body>
</html>
        """
        
        return html_content
    
    def _prepare_template_data(
        self,
        topic: str,
        data: Dict[str, Any],
        modules: List[BaseModule],
        report_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Prepare data for the enhanced HTML template."""
        return {
            "title": report_title or f"{topic}: Modular Enhanced Analysis",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "executive_summary": data.get("executive_summary", f"Comprehensive analysis of {topic}"),
            "estimated_cost": data.get("estimated_cost", "$2.5B"),
            "modules": modules
        }
    
    def _generate_modules_html(self, modules: List[BaseModule], data: Dict[str, Any]) -> str:
        """Generate HTML content for all modules."""
        modules_html = []
        
        for module in modules:
            try:
                # Validate module data
                module.validate_data(data)
                
                # Generate module content
                content = module.generate_content(data)
                modules_html.append(content)
                    
            except Exception as e:
                # Log error and continue with other modules
                print(f"Error generating content for module {module.module_id}: {e}")
                continue
        
        return ''.join(modules_html)
    
    def _generate_header(self, topic: str, report_title: Optional[str] = None) -> str:
        """Generate the report header."""
        title = report_title or f"{topic}: Modular Enhanced Analysis"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
    <div class="container">
        <div class="header">
            <h1>📊 {title}</h1>
            <div class="subtitle">Modular Enhanced Analysis with Configurable Components</div>
            <div class="timestamp">Generated: {timestamp}</div>
        </div>
        """
    
    def _generate_css_styles(self) -> str:
        """Generate CSS styles for the report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .header h1 {
            font-size: 3rem;
            color: #2c3e50;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 20px;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        
        .section h2 {
            color: #2c3e50;
            font-size: 2rem;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        
        .chart-section {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .chart-container {
            position: relative;
            width: 100%;
            height: 300px;
            margin: 20px 0;
        }
        
        .chart-container canvas {
            max-width: 100% !important;
            max-height: 100% !important;
            width: 100% !important;
            height: 100% !important;
        }
        
        .enhanced-tooltip {
            position: absolute;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            font-size: 0.95em;
            z-index: 1000;
            max-width: 400px;
            display: none;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255,255,255,0.2);
        }
        
        .tooltip-title {
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #fff;
        }
        
        .tooltip-content {
            line-height: 1.5;
        }
        
        .tooltip-source {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.3);
            font-size: 0.85em;
            opacity: 0.9;
        }
        
        .tooltip-strategic {
            margin-top: 8px;
            padding: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 6px;
            font-size: 0.9em;
        }
        
        .tooltip-recommendations {
            margin-top: 8px;
            padding: 8px;
            background: rgba(46, 204, 113, 0.2);
            border-radius: 6px;
            font-size: 0.9em;
            border-left: 3px solid #2ecc71;
        }
        
        .tooltip-use-cases {
            margin-top: 8px;
            padding: 8px;
            background: rgba(155, 89, 182, 0.2);
            border-radius: 6px;
            font-size: 0.9em;
            border-left: 3px solid #9b59b6;
        }
        
        .intelligence-recommendations {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            color: white;
        }
        
        .recommendation-item {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .recommendation-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .charts-grid { grid-template-columns: 1fr; }
        }
        """
    
    def _generate_javascript(self, module_scripts: List[str]) -> str:
        """Generate JavaScript for the report."""
        return f"""
        // Enhanced tooltip functionality
        function showEnhancedTooltip(event, tooltipData) {{
            const tooltip = document.getElementById('enhancedTooltip');
            const title = document.getElementById('tooltipTitle');
            const content = document.getElementById('tooltipContent');
            const source = document.getElementById('tooltipSource');
            const strategic = document.getElementById('tooltipStrategic');
            const recommendations = document.getElementById('tooltipRecommendations');
            const useCases = document.getElementById('tooltipUseCases');
            
            title.textContent = tooltipData.title;
            content.innerHTML = tooltipData.description;
            source.innerHTML = tooltipData.source;
            strategic.innerHTML = tooltipData.strategic_impact;
            
            if (tooltipData.recommendations) {{
                recommendations.innerHTML = '<strong>💡 Recommendations:</strong><br/>' + tooltipData.recommendations;
                recommendations.style.display = 'block';
            }} else {{
                recommendations.style.display = 'none';
            }}
            
            if (tooltipData.use_cases) {{
                useCases.innerHTML = '<strong>🎯 Use Cases:</strong><br/>' + tooltipData.use_cases;
                useCases.style.display = 'block';
            }} else {{
                useCases.style.display = 'none';
            }}
            
            tooltip.style.display = 'block';
            tooltip.style.left = event.pageX + 10 + 'px';
            tooltip.style.top = event.pageY - 10 + 'px';
        }}
        
        function hideEnhancedTooltip() {{
            document.getElementById('enhancedTooltip').style.display = 'none';
        }}
        
        // Module scripts
        {''.join(module_scripts)}
        """
    
    def _apply_custom_config(self, config: Dict[str, Any]):
        """Apply custom configuration to modules."""
        for module_id, module_config in config.items():
            self.configure_module(module_id, module_config)
    
    def _generate_report_metadata(
        self,
        topic: str,
        modules: List[BaseModule],
        file_path: Path,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate metadata for the report."""
        return {
            "topic": topic,
            "modules_used": [m.get_module_metadata() for m in modules],
            "total_modules": len(modules),
            "data_keys_used": list(data.keys()),
            "generation_timestamp": datetime.now().isoformat(),
            "file_size_bytes": file_path.stat().st_size,
            "features": [
                "Modular Architecture",
                "Configurable Components",
                "Advanced Tooltips",
                "Interactive Visualizations",
                "Strategic Recommendations"
            ]
        }
    
    def get_generator_summary(self) -> Dict[str, Any]:
        """Get a summary of the generator capabilities."""
        return {
            "available_modules": self.get_available_modules(),
            "enabled_modules": [m.module_id for m in self.get_enabled_modules()],
            "total_modules": len(self.modules),
            "output_directory": str(self.output_dir),
            "capabilities": [
                "Modular report generation",
                "Configurable module selection",
                "Advanced tooltip system",
                "Interactive visualizations",
                "Strategic recommendations",
                "Custom styling and theming"
            ]
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename by removing or replacing invalid characters.
        
        Args:
            filename: The original filename
            
        Returns:
            Sanitized filename safe for filesystem
        """
        import re
        
        # Replace spaces with underscores
        sanitized = filename.replace(' ', '_')
        
        # Remove or replace invalid characters for Windows/Unix filesystems
        # Invalid characters: < > : " | ? * \ /
        invalid_chars = r'[<>:"|?*\\/]'
        sanitized = re.sub(invalid_chars, '', sanitized)
        
        # Replace multiple underscores with single underscore
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # Ensure filename is not empty
        if not sanitized:
            sanitized = "report"
        
        return sanitized


# Global instance for easy access
modular_report_generator = ModularReportGenerator()
