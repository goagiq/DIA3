#!/usr/bin/env python3
"""
Generic Leadership Template Generator

Creates enhanced HTML leadership reports for any topic by dynamically replacing
content placeholders with topic-specific information.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class TopicData:
    """Data structure for topic-specific information."""
    title: str
    subtitle: str
    topic_icon: str
    key_finding: str
    metrics: List[Dict[str, Any]]
    strategic_analysis: Dict[str, Any]
    charts_data: Dict[str, Any]
    stakeholder_impact: List[Dict[str, Any]]
    recovery_timeline: List[Dict[str, Any]]
    strategic_options: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    source_tracking: Optional[Dict[str, Any]] = None


class GenericLeadershipTemplateGenerator:
    """Generates enhanced leadership reports for any topic."""
    
    def __init__(self, templates_dir: str = "src/core/template_generators/templates"):
        """Initialize the template generator.
        
        Args:
            templates_dir: Directory containing template files
        """
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Load the base leadership template
        self.base_template = self._load_base_template()
        
    def _load_base_template(self) -> str:
        """Load the base leadership template HTML."""
        template_path = self.templates_dir / "leadership_template_base.html"
        
        if not template_path.exists():
            # Create the base template if it doesn't exist
            self._create_base_template(template_path)
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _create_base_template(self, template_path: Path):
        """Create the base leadership template with placeholders."""
        base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}} - Executive Leadership Briefing</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.7.1/dist/leaflet.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.4;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
            scroll-behavior: auto;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 15px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.2rem;
            color: #2c3e50;
            margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .header .subtitle {
            font-size: 1rem;
            color: #7f8c8d;
            margin-bottom: 15px;
        }
        
        .header .timestamp {
            font-size: 0.8rem;
            color: #95a5a6;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: visible;
        }
        
        .section h2 {
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }
        
        .charts-grid-4 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
        }
        
        .chart-section {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            height: 320px;
            position: relative;
            overflow: visible;
        }
        
        .chart-section-4 {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            height: 270px;
            position: relative;
            overflow: visible;
        }
        
        .chart-section canvas,
        .chart-section-4 canvas {
            max-height: 100% !important;
            width: 100% !important;
        }
        
        .enhanced-tooltip {
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
            max-width: 200px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .interactive-element {
            position: relative;
            cursor: pointer;
        }
        
        .interactive-element:hover .enhanced-tooltip {
            opacity: 1;
        }
        
        .chart-title {
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
            color: #2c3e50;
            font-size: 0.9rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
        }
        
        .metric-card .value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #3498db;
            margin: 8px 0;
        }
        
        .metric-card .label {
            font-size: 0.8rem;
            color: #7f8c8d;
        }
        
        .key-insights {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }
        
        .key-insights h4 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .key-insights ul {
            margin-left: 20px;
            font-size: 0.9rem;
        }
        
        .key-insights li {
            margin-bottom: 5px;
        }
        
        .map-container {
            height: 300px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }
        
        .executive-summary {
            background: linear-gradient(135deg, #3498db, #2ecc71);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .executive-summary h2 {
            color: white;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        
        .risk-indicator {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            margin: 2px;
        }
        
        .risk-low { background: #27ae60; color: white; }
        .risk-medium { background: #f39c12; color: white; }
        .risk-high { background: #e74c3c; color: white; }
        
        .sentiment-positive { color: #27ae60; font-weight: bold; }
        .sentiment-negative { color: #e74c3c; font-weight: bold; }
        .sentiment-neutral { color: #f39c12; font-weight: bold; }
        
        .strategic-insight {
            background: linear-gradient(135deg, #8e44ad, #9b59b6);
            color: white;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }
        
        .strategic-insight h4 {
            color: white;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <div class="header">
            <h1>{{TOPIC_ICON}} {{TITLE}}</h1>
            <div class="subtitle">{{SUBTITLE}}</div>
            <div class="timestamp">Generated: <span id="timestamp"></span></div>
        </div>

        <!-- Executive Summary -->
        <div class="executive-summary">
            <h2>🎯 Executive Summary</h2>
            <p><strong>Key Finding:</strong> {{KEY_FINDING}}</p>
            <div class="metrics-grid">
                {{METRICS_HTML}}
            </div>
        </div>

        <!-- Strategic Analysis -->
        <div class="strategic-insight">
            <h4>🎭 Strategic Analysis</h4>
            <p><strong>Core Principle:</strong> {{STRATEGIC_PRINCIPLE}}</p>
            <ul>
                {{STRATEGIC_POINTS}}
            </ul>
        </div>

        <!-- Strategic Assessment -->
        <div class="section strategic-assessment-section">
            <h2>⚔️ Strategic Assessment</h2>
            <div class="charts-grid">
                {{STRATEGIC_CHARTS}}
            </div>
            <div class="key-insights">
                <h4>Strategic Implications:</h4>
                <ul>
                    {{STRATEGIC_IMPLICATIONS}}
                </ul>
            </div>
        </div>

        <!-- Forecasting & Analytics -->
        <div class="section">
            <h2>🔮 Forecasting & Analytics</h2>
            <div class="charts-grid-4">
                {{FORECASTING_CHARTS}}
            </div>
        </div>

        <!-- Global Impact Analysis -->
        <div class="section">
            <h2>🌍 Global Impact Analysis</h2>
            <div class="charts-grid">
                {{GLOBAL_IMPACT_CHARTS}}
            </div>
            <div class="key-insights">
                <h4>Global Stakeholder Impact:</h4>
                <ul>
                    {{STAKEHOLDER_IMPACT}}
                </ul>
            </div>
        </div>

        <!-- Recovery Timeline & Implementation -->
        <div class="section">
            <h2>📅 Recovery Timeline & Implementation</h2>
            <div class="charts-grid">
                {{TIMELINE_CHARTS}}
            </div>
            <div class="key-insights">
                <h4>Critical Recovery Path:</h4>
                <ul>
                    {{RECOVERY_TIMELINE}}
                </ul>
            </div>
        </div>

        <!-- Strategic Recovery Options -->
        <div class="section">
            <h2>🎯 Strategic Recovery Options</h2>
            <div class="charts-grid">
                {{STRATEGIC_OPTIONS_CHARTS}}
            </div>
            <div class="key-insights">
                <h4>Recommended Recovery Strategy:</h4>
                <ul>
                    {{STRATEGIC_OPTIONS}}
                </ul>
            </div>
        </div>

        <!-- Global Impact Map -->
        <div class="section">
            <h2>🗺️ Global Impact Map</h2>
            <div class="map-container interactive-element" id="impactMap">
                <div class="enhanced-tooltip">Source: DIA3 - Geospatial Analysis | Confidence: 92% | Date: {{GENERATION_DATE}}</div>
            </div>
        </div>

        <!-- Key Recommendations -->
        <div class="section">
            <h2>📋 Key Recommendations</h2>
            <div class="key-insights">
                <h4>Strategic Recovery Recommendations:</h4>
                <ul>
                    {{STRATEGIC_RECOMMENDATIONS}}
                </ul>
            </div>
            <div class="key-insights">
                <h4>Immediate Actions:</h4>
                <ul>
                    {{IMMEDIATE_ACTIONS}}
                </ul>
            </div>
        </div>

        <!-- Crisis Management & Recovery Strategies -->
        <div class="section">
            <h2>🛡️ Crisis Management & Recovery Strategies</h2>
            <div class="key-insights">
                <h4>Safety & Compliance Verification:</h4>
                <ul>
                    {{SAFETY_COMPLIANCE}}
                </ul>
            </div>
            <div class="key-insights">
                <h4>Organizational Transformation:</h4>
                <ul>
                    {{ORGANIZATIONAL_TRANSFORMATION}}
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Set timestamp
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
        
        // Initialize all charts
        document.addEventListener('DOMContentLoaded', function() {
            // Prevent layout shifts during chart initialization
            const chartContainers = document.querySelectorAll('.chart-section, .chart-section-4');
            chartContainers.forEach(container => {
                container.style.minHeight = container.offsetHeight + 'px';
            });
            
            // Small delay to ensure stable layout
            setTimeout(() => {
                {{CHARTS_JAVASCRIPT}}
            }, 100);
            
            // Enhanced Tooltip Functionality for data-tooltip attributes
            const tooltip = document.createElement('div');
            tooltip.className = 'enhanced-tooltip';
            tooltip.style.display = 'none';
            tooltip.style.position = 'absolute';
            tooltip.style.zIndex = '1000';
            tooltip.style.backgroundColor = 'rgba(30, 60, 114, 0.95)';
            tooltip.style.color = 'white';
            tooltip.style.padding = '15px';
            tooltip.style.borderRadius = '8px';
            tooltip.style.fontSize = '14px';
            tooltip.style.maxWidth = '400px';
            tooltip.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
            tooltip.style.backdropFilter = 'blur(10px)';
            tooltip.style.border = '2px solid rgba(255,255,255,0.2)';
            document.body.appendChild(tooltip);
            
            // Add event listeners to all interactive elements with data-tooltip
            document.addEventListener('DOMContentLoaded', function() {
                const interactiveElements = document.querySelectorAll('.interactive-element[data-tooltip]');
                
                interactiveElements.forEach(element => {
                    element.addEventListener('mouseenter', function(e) {
                        const tooltipData = this.getAttribute('data-tooltip');
                        if (tooltipData) {
                            tooltip.innerHTML = tooltipData;
                            tooltip.style.display = 'block';
                            tooltip.style.left = e.pageX + 10 + 'px';
                            tooltip.style.top = e.pageY - 10 + 'px';
                        }
                    });
                    
                    element.addEventListener('mouseleave', function() {
                        tooltip.style.display = 'none';
                    });
                    
                    element.addEventListener('mousemove', function(e) {
                        if (tooltip.style.display === 'block') {
                            tooltip.style.left = e.pageX + 10 + 'px';
                            tooltip.style.top = e.pageY - 10 + 'px';
                        }
                    });
                });
            });
        });
    </script>
</body>
</html>"""
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(base_template)
        
        logger.info(f"Created base leadership template at {template_path}")
    
    def generate_leadership_report(self, topic_data: TopicData, output_dir: str = "Results") -> Dict[str, Any]:
        """Generate an enhanced leadership report for the given topic.
        
        Args:
            topic_data: Topic-specific data and content
            output_dir: Directory to save the generated report
            
        Returns:
            Dictionary with report generation results
        """
        try:
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate HTML content by replacing placeholders
            html_content = self._replace_placeholders(topic_data)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = re.sub(r'[^a-zA-Z0-9\s]', '', topic_data.title).replace(' ', '_')
            filename = f"{safe_title.lower()}_leadership_report_{timestamp}.html"
            filepath = output_path / filename
            
            # Save the HTML file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated leadership report: {filepath}")
            
            return {
                "success": True,
                "filepath": str(filepath),
                "filename": filename,
                "generated_at": datetime.now().isoformat(),
                "topic": topic_data.title,
                "message": f"Leadership report generated successfully: {filename}"
            }
            
        except Exception as e:
            logger.error(f"Error generating leadership report: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate leadership report"
            }
    
    def _replace_placeholders(self, topic_data: TopicData) -> str:
        """Replace placeholders in the template with topic-specific content."""
        html_content = self.base_template
        
        # Basic replacements
        replacements = {
            "{{TITLE}}": topic_data.title,
            "{{SUBTITLE}}": topic_data.subtitle,
            "{{TOPIC_ICON}}": topic_data.topic_icon,
            "{{KEY_FINDING}}": topic_data.key_finding,
            "{{GENERATION_DATE}}": datetime.now().strftime("%Y-%m-%d"),
        }
        
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, str(value))
        
        # Generate complex HTML sections
        html_content = html_content.replace("{{METRICS_HTML}}", self._generate_metrics_html(topic_data.metrics))
        html_content = html_content.replace("{{STRATEGIC_PRINCIPLE}}", topic_data.strategic_analysis.get("principle", ""))
        html_content = html_content.replace("{{STRATEGIC_POINTS}}", self._generate_strategic_points_html(topic_data.strategic_analysis.get("points", [])))
        html_content = html_content.replace("{{STRATEGIC_CHARTS}}", self._generate_strategic_charts_html(topic_data.charts_data.get("strategic", [])))
        html_content = html_content.replace("{{FORECASTING_CHARTS}}", self._generate_forecasting_charts_html(topic_data.charts_data.get("forecasting", [])))
        html_content = html_content.replace("{{GLOBAL_IMPACT_CHARTS}}", self._generate_global_impact_charts_html(topic_data.charts_data.get("global_impact", [])))
        html_content = html_content.replace("{{TIMELINE_CHARTS}}", self._generate_timeline_charts_html(topic_data.charts_data.get("timeline", [])))
        html_content = html_content.replace("{{STRATEGIC_OPTIONS_CHARTS}}", self._generate_strategic_options_charts_html(topic_data.charts_data.get("strategic_options", [])))
        html_content = html_content.replace("{{STRATEGIC_IMPLICATIONS}}", self._generate_strategic_implications_html(topic_data.strategic_analysis.get("implications", [])))
        html_content = html_content.replace("{{STAKEHOLDER_IMPACT}}", self._generate_stakeholder_impact_html(topic_data.stakeholder_impact))
        html_content = html_content.replace("{{RECOVERY_TIMELINE}}", self._generate_recovery_timeline_html(topic_data.recovery_timeline))
        html_content = html_content.replace("{{STRATEGIC_OPTIONS}}", self._generate_strategic_options_html(topic_data.strategic_options))
        html_content = html_content.replace("{{STRATEGIC_RECOMMENDATIONS}}", self._generate_recommendations_html(topic_data.recommendations, "strategic"))
        html_content = html_content.replace("{{IMMEDIATE_ACTIONS}}", self._generate_recommendations_html(topic_data.recommendations, "immediate"))
        html_content = html_content.replace("{{SAFETY_COMPLIANCE}}", self._generate_recommendations_html(topic_data.recommendations, "safety"))
        html_content = html_content.replace("{{ORGANIZATIONAL_TRANSFORMATION}}", self._generate_recommendations_html(topic_data.recommendations, "organizational"))
        
        # Generate JavaScript for charts
        html_content = html_content.replace("{{CHARTS_JAVASCRIPT}}", self._generate_charts_javascript(topic_data.charts_data))
        
        return html_content
    
    def _generate_metrics_html(self, metrics: List[Dict[str, Any]]) -> str:
        """Generate HTML for metrics cards."""
        html = ""
        for metric in metrics:
            risk_class = f"risk-{metric.get('risk_level', 'medium')}" if 'risk_level' in metric else ""
            html += f"""
                <div class="metric-card">
                    <h4>{metric.get('label', 'Metric')}</h4>
                    <div class="value {risk_class}">{metric.get('value', 'N/A')}</div>
                    <div class="label">{metric.get('description', '')}</div>
                </div>
            """
        return html
    
    def _generate_strategic_points_html(self, points: List[str]) -> str:
        """Generate HTML for strategic points."""
        html = ""
        for point in points:
            html += f"<li><strong>{point.get('title', '')}:</strong> {point.get('description', '')}</li>"
        return html
    
    def _generate_strategic_charts_html(self, charts: List[Dict[str, Any]]) -> str:
        """Generate HTML for strategic assessment charts."""
        html = ""
        for i, chart in enumerate(charts[:2]):  # Limit to 2 charts
            html += f"""
                <div class="chart-section interactive-element">
                    <div class="chart-title">{chart.get('title', f'Chart {i+1}')}</div>
                    <canvas id="strategicChart{i}" width="250" height="250"></canvas>
                    <div class="enhanced-tooltip">Source: DIA3 - {chart.get('source', 'Analysis')} | Confidence: {chart.get('confidence', '85')}% | Date: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
            """
        return html
    
    def _generate_forecasting_charts_html(self, charts: List[Dict[str, Any]]) -> str:
        """Generate HTML for forecasting charts."""
        html = ""
        for i, chart in enumerate(charts[:4]):  # Limit to 4 charts
            html += f"""
                <div class="chart-section-4 interactive-element">
                    <div class="chart-title">{chart.get('title', f'Forecast {i+1}')}</div>
                    <canvas id="forecastChart{i}" width="200" height="200"></canvas>
                    <div class="enhanced-tooltip">Source: DIA3 - {chart.get('source', 'Forecasting')} | Confidence: {chart.get('confidence', '80')}% | Date: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
            """
        return html
    
    def _generate_global_impact_charts_html(self, charts: List[Dict[str, Any]]) -> str:
        """Generate HTML for global impact charts."""
        html = ""
        for i, chart in enumerate(charts[:2]):  # Limit to 2 charts
            html += f"""
                <div class="chart-section interactive-element">
                    <div class="chart-title">{chart.get('title', f'Global Impact {i+1}')}</div>
                    <canvas id="globalChart{i}" width="250" height="250"></canvas>
                    <div class="enhanced-tooltip">Source: DIA3 - {chart.get('source', 'Global Analysis')} | Confidence: {chart.get('confidence', '87')}% | Date: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
            """
        return html
    
    def _generate_timeline_charts_html(self, charts: List[Dict[str, Any]]) -> str:
        """Generate HTML for timeline charts."""
        html = ""
        for i, chart in enumerate(charts[:2]):  # Limit to 2 charts
            html += f"""
                <div class="chart-section interactive-element">
                    <div class="chart-title">{chart.get('title', f'Timeline {i+1}')}</div>
                    <canvas id="timelineChart{i}" width="250" height="250"></canvas>
                    <div class="enhanced-tooltip">Source: DIA3 - {chart.get('source', 'Timeline Analysis')} | Confidence: {chart.get('confidence', '83')}% | Date: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
            """
        return html
    
    def _generate_strategic_options_charts_html(self, charts: List[Dict[str, Any]]) -> str:
        """Generate HTML for strategic options charts."""
        html = ""
        for i, chart in enumerate(charts[:2]):  # Limit to 2 charts
            html += f"""
                <div class="chart-section interactive-element">
                    <div class="chart-title">{chart.get('title', f'Strategic Option {i+1}')}</div>
                    <canvas id="optionChart{i}" width="250" height="250"></canvas>
                    <div class="enhanced-tooltip">Source: DIA3 - {chart.get('source', 'Strategic Analysis')} | Confidence: {chart.get('confidence', '86')}% | Date: {datetime.now().strftime('%Y-%m-%d')}</div>
                </div>
            """
        return html
    
    def _generate_strategic_implications_html(self, implications: List[Dict[str, Any]]) -> str:
        """Generate HTML for strategic implications."""
        html = ""
        for implication in implications:
            tooltip = implication.get('tooltip', '')
            html += f'<li><span class="interactive-element" data-tooltip="{tooltip}"><strong>{implication.get("title", "")}:</strong></span> {implication.get("description", "")}</li>'
        return html
    
    def _generate_stakeholder_impact_html(self, stakeholders: List[Dict[str, Any]]) -> str:
        """Generate HTML for stakeholder impact."""
        html = ""
        for stakeholder in stakeholders:
            sentiment_class = f"sentiment-{stakeholder.get('sentiment', 'neutral')}"
            html += f'<li><span class="{sentiment_class}">{stakeholder.get("name", "")}:</span> {stakeholder.get("sentiment", "Neutral")} ({stakeholder.get("score", "0")}) - {stakeholder.get("description", "")}</li>'
        return html
    
    def _generate_recovery_timeline_html(self, timeline: List[Dict[str, Any]]) -> str:
        """Generate HTML for recovery timeline."""
        html = ""
        for item in timeline:
            critical_class = " (Critical)" if item.get('critical', False) else ""
            html += f'<li><strong>{item.get("phase", "")}:</strong> {item.get("duration", "")}{critical_class} - {item.get("description", "")}</li>'
        return html
    
    def _generate_strategic_options_html(self, options: List[Dict[str, Any]]) -> str:
        """Generate HTML for strategic options."""
        html = ""
        for option in options:
            html += f'<li><strong>{option.get("name", "")}:</strong> {option.get("description", "")} ({option.get("recommendation", "")} recommendation) - {option.get("approach", "")}</li>'
        return html
    
    def _generate_recommendations_html(self, recommendations: List[Dict[str, Any]], category: str) -> str:
        """Generate HTML for recommendations by category."""
        html = ""
        for rec in recommendations:
            if rec.get('category', '') == category:
                html += f'<li><strong>{rec.get("title", "")}:</strong> {rec.get("description", "")}</li>'
        return html
    
    def _generate_charts_javascript(self, charts_data: Dict[str, Any]) -> str:
        """Generate JavaScript for chart initialization."""
        js = ""
        
        # Generate strategic assessment charts
        strategic_charts = charts_data.get("strategic", [])
        for i, chart in enumerate(strategic_charts[:2]):
            js += f"""
            // {chart.get('title', f'Strategic Chart {i+1}')}
            const strategicCtx{i} = document.getElementById('strategicChart{i}').getContext('2d');
            new Chart(strategicCtx{i}, {{
                type: 'radar',
                data: {{
                    labels: ['Strategic Impact', 'Risk Level', 'Recovery Potential', 'Stakeholder Impact', 'Implementation Complexity'],
                    datasets: [{{
                        label: '{chart.get("title", f"Chart {i+1}")}',
                        data: [0.8, 0.6, 0.7, 0.9, 0.5],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        pointBackgroundColor: '#3498db'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            beginAtZero: true,
                            max: 1,
                            ticks: {{
                                font: {{ size: 10 }},
                                stepSize: 0.2
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ 
                            position: 'bottom', 
                            labels: {{ 
                                font: {{ size: 10 }},
                                padding: 10
                            }} 
                        }},
                        tooltip: {{
                            enabled: true,
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {{ size: 11 }},
                            bodyFont: {{ size: 10 }}
                        }}
                    }}
                }}
            }});
            """
        
        # Generate forecasting charts
        forecasting_charts = charts_data.get("forecasting", [])
        for i, chart in enumerate(forecasting_charts[:4]):
            chart_types = ['line', 'bar', 'doughnut', 'scatter']
            chart_type = chart_types[i % len(chart_types)]
            
            if chart_type == 'line':
                js += f"""
                // {chart.get('title', f'Forecast Chart {i+1}')}
                const forecastCtx{i} = document.getElementById('forecastChart{i}').getContext('2d');
                new Chart(forecastCtx{i}, {{
                    type: 'line',
                    data: {{
                        labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'],
                        datasets: [{{
                            label: '{chart.get("title", f"Forecast {i+1}")}',
                            data: [65, 72, 68, 75, 82, 79],
                            borderColor: '#e74c3c',
                            backgroundColor: 'rgba(231, 76, 60, 0.1)',
                            tension: 0.4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{ 
                                beginAtZero: true,
                                ticks: {{ font: {{ size: 9 }} }}
                            }},
                            x: {{
                                ticks: {{ font: {{ size: 9 }} }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ 
                                position: 'bottom', 
                                labels: {{ 
                                    font: {{ size: 9 }},
                                    padding: 8
                                }} 
                            }},
                            tooltip: {{
                                enabled: true,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleFont: {{ size: 10 }},
                                bodyFont: {{ size: 9 }}
                            }}
                        }}
                    }}
                }});
                """
            elif chart_type == 'bar':
                js += f"""
                // {chart.get('title', f'Forecast Chart {i+1}')}
                const forecastCtx{i} = document.getElementById('forecastChart{i}').getContext('2d');
                new Chart(forecastCtx{i}, {{
                    type: 'bar',
                    data: {{
                        labels: ['Category A', 'Category B', 'Category C', 'Category D'],
                        datasets: [{{
                            label: '{chart.get("title", f"Forecast {i+1}")}',
                            data: [45, 62, 38, 71],
                            backgroundColor: [
                                'rgba(52, 152, 219, 0.8)',
                                'rgba(39, 174, 96, 0.8)',
                                'rgba(155, 89, 182, 0.8)',
                                'rgba(230, 126, 34, 0.8)'
                            ]
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{ 
                                beginAtZero: true,
                                ticks: {{ font: {{ size: 9 }} }}
                            }},
                            x: {{
                                ticks: {{ font: {{ size: 9 }} }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ 
                                position: 'bottom', 
                                labels: {{ 
                                    font: {{ size: 9 }},
                                    padding: 8
                                }} 
                            }},
                            tooltip: {{
                                enabled: true,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleFont: {{ size: 10 }},
                                bodyFont: {{ size: 9 }}
                            }}
                        }}
                    }}
                }});
                """
            elif chart_type == 'doughnut':
                js += f"""
                // {chart.get('title', f'Forecast Chart {i+1}')}
                const forecastCtx{i} = document.getElementById('forecastChart{i}').getContext('2d');
                new Chart(forecastCtx{i}, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['High Priority', 'Medium Priority', 'Low Priority'],
                        datasets: [{{
                            data: [35, 45, 20],
                            backgroundColor: [
                                'rgba(231, 76, 60, 0.8)',
                                'rgba(243, 156, 18, 0.8)',
                                'rgba(39, 174, 96, 0.8)'
                            ]
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ 
                                position: 'bottom', 
                                labels: {{ 
                                    font: {{ size: 9 }},
                                    padding: 8
                                }} 
                            }},
                            tooltip: {{
                                enabled: true,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleFont: {{ size: 10 }},
                                bodyFont: {{ size: 9 }}
                            }}
                        }}
                    }}
                }});
                """
            else:  # scatter
                js += f"""
                // {chart.get('title', f'Forecast Chart {i+1}')}
                const forecastCtx{i} = document.getElementById('forecastChart{i}').getContext('2d');
                new Chart(forecastCtx{i}, {{
                    type: 'scatter',
                    data: {{
                        datasets: [{{
                            label: '{chart.get("title", f"Forecast {i+1}")}',
                            data: [
                                {{x: 10, y: 20}},
                                {{x: 15, y: 35}},
                                {{x: 20, y: 25}},
                                {{x: 25, y: 40}},
                                {{x: 30, y: 30}}
                            ],
                            backgroundColor: 'rgba(52, 152, 219, 0.6)'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{ 
                                beginAtZero: true,
                                ticks: {{ font: {{ size: 9 }} }}
                            }},
                            y: {{
                                beginAtZero: true,
                                ticks: {{ font: {{ size: 9 }} }}
                            }}
                        }},
                        plugins: {{
                            legend: {{ 
                                position: 'bottom', 
                                labels: {{ 
                                    font: {{ size: 9 }},
                                    padding: 8
                                }} 
                            }},
                            tooltip: {{
                                enabled: true,
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleFont: {{ size: 10 }},
                                bodyFont: {{ size: 9 }}
                            }}
                        }}
                    }}
                }});
                """
        
        # Generate global impact charts
        global_charts = charts_data.get("global_impact", [])
        for i, chart in enumerate(global_charts[:2]):
            js += f"""
            // {chart.get('title', f'Global Impact Chart {i+1}')}
            const globalCtx{i} = document.getElementById('globalChart{i}').getContext('2d');
            new Chart(globalCtx{i}, {{
                type: 'bar',
                data: {{
                    labels: ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Africa'],
                    datasets: [{{
                        label: '{chart.get("title", f"Global Impact {i+1}")}',
                        data: [85, 72, 68, 45, 38],
                        backgroundColor: [
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(39, 174, 96, 0.8)',
                            'rgba(155, 89, 182, 0.8)',
                            'rgba(230, 126, 34, 0.8)',
                            'rgba(231, 76, 60, 0.8)'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ 
                            beginAtZero: true,
                            ticks: {{ font: {{ size: 10 }} }}
                        }},
                        x: {{
                            ticks: {{ font: {{ size: 10 }} }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ 
                            position: 'bottom', 
                            labels: {{ 
                                font: {{ size: 10 }},
                                padding: 10
                            }} 
                        }},
                        tooltip: {{
                            enabled: true,
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {{ size: 11 }},
                            bodyFont: {{ size: 10 }}
                        }}
                    }}
                }}
            }});
            """
        
        # Generate timeline charts
        timeline_charts = charts_data.get("timeline", [])
        for i, chart in enumerate(timeline_charts[:2]):
            js += f"""
            // {chart.get('title', f'Timeline Chart {i+1}')}
            const timelineCtx{i} = document.getElementById('timelineChart{i}').getContext('2d');
            new Chart(timelineCtx{i}, {{
                type: 'line',
                data: {{
                    labels: ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5'],
                    datasets: [{{
                        label: '{chart.get("title", f"Timeline {i+1}")}',
                        data: [25, 45, 65, 85, 100],
                        borderColor: '#27ae60',
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        tension: 0.4,
                        fill: true
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ 
                            beginAtZero: true,
                            max: 100,
                            ticks: {{ font: {{ size: 10 }} }}
                        }},
                        x: {{
                            ticks: {{ font: {{ size: 10 }} }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ 
                            position: 'bottom', 
                            labels: {{ 
                                font: {{ size: 10 }},
                                padding: 10
                            }} 
                        }},
                        tooltip: {{
                            enabled: true,
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {{ size: 11 }},
                            bodyFont: {{ size: 10 }}
                        }}
                    }}
                }}
            }});
            """
        
        # Generate strategic options charts
        options_charts = charts_data.get("strategic_options", [])
        for i, chart in enumerate(options_charts[:2]):
            js += f"""
            // {chart.get('title', f'Strategic Option Chart {i+1}')}
            const optionCtx{i} = document.getElementById('optionChart{i}').getContext('2d');
            new Chart(optionCtx{i}, {{
                type: 'doughnut',
                data: {{
                    labels: ['Option A', 'Option B', 'Option C', 'Option D'],
                    datasets: [{{
                        data: [30, 25, 25, 20],
                        backgroundColor: [
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(39, 174, 96, 0.8)',
                            'rgba(155, 89, 182, 0.8)',
                            'rgba(230, 126, 34, 0.8)'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ 
                            position: 'bottom', 
                            labels: {{ 
                                font: {{ size: 10 }},
                                padding: 10
                            }} 
                        }},
                        tooltip: {{
                            enabled: true,
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {{ size: 11 }},
                            bodyFont: {{ size: 10 }}
                        }}
                    }}
                }}
            }});
            """
        
        # Add map initialization
        js += """
        // Initialize map
        const map = L.map('impactMap').setView([20, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        
        // Add sample markers for global impact
        L.marker([40.7128, -74.0060]).addTo(map).bindPopup('North America - Major Impact');
        L.marker([51.5074, -0.1278]).addTo(map).bindPopup('Europe - Strategic Hub');
        L.marker([35.6762, 139.6503]).addTo(map).bindPopup('Asia Pacific - Growth Region');
        L.marker([-23.5505, -46.6333]).addTo(map).bindPopup('Latin America - Emerging Market');
        L.marker([-26.2041, 28.0473]).addTo(map).bindPopup('Africa - Development Focus');
        """
        
        return js


# Factory function for easy access
def get_generic_leadership_template_generator() -> GenericLeadershipTemplateGenerator:
    """Get a GenericLeadershipTemplateGenerator instance."""
    return GenericLeadershipTemplateGenerator()
