#!/usr/bin/env python3
"""
Advanced Tooltip Generator for DIA3 Reports
Adds interactive tooltips with multiple sources, detailed descriptions, use cases, and recommendations
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedTooltipGenerator:
    """Generates advanced tooltips for interactive visualizations and tables"""
    
    def __init__(self):
        self.tooltip_data = {
            'fleet_comparison': {
                'title': 'Global Submarine Fleet Comparison',
                'description': 'Comprehensive comparison of submarine fleet sizes across major naval powers, showing Pakistan\'s proposed expansion from 5-8 to 50 submarines.',
                'sources': [
                    'International Institute for Strategic Studies (IISS) - Military Balance 2025',
                    'Stockholm International Peace Research Institute (SIPRI) - Arms Transfer Database',
                    'US Department of Defense - Annual Report to Congress on Military Power',
                    'Indian Ministry of Defence - Annual Report 2024-25',
                    'Chinese Defense White Paper 2024'
                ],
                'use_cases': [
                    'Strategic planning and force structure analysis',
                    'Regional security assessment and arms control negotiations',
                    'Defense budget allocation and procurement planning',
                    'International relations and diplomatic engagement',
                    'Military capability gap analysis'
                ],
                'recommendations': [
                    'Implement phased acquisition approach to manage economic burden',
                    'Engage in regional security dialogue to address concerns',
                    'Develop confidence-building measures with neighboring states',
                    'Establish transparency mechanisms for fleet modernization',
                    'Consider alternative force structures for strategic objectives'
                ]
            },
            'economic_impact': {
                'title': 'Economic Impact Analysis',
                'description': 'Detailed cost analysis covering procurement, infrastructure, operations, and economic sustainability of the submarine program.',
                'sources': [
                    'World Bank - Pakistan Economic Indicators 2025',
                    'International Monetary Fund (IMF) - Fiscal Monitor',
                    'Pakistan Ministry of Finance - Budget Documents',
                    'Defense Economics Research Institute',
                    'Center for Strategic and International Studies (CSIS)'
                ],
                'use_cases': [
                    'Budget planning and fiscal sustainability analysis',
                    'Economic feasibility assessment and risk evaluation',
                    'Defense procurement strategy development',
                    'International financial institution engagement',
                    'Economic impact modeling and forecasting'
                ],
                'recommendations': [
                    'Conduct comprehensive economic feasibility study',
                    'Explore international partnerships and financing options',
                    'Implement cost-control measures and efficiency programs',
                    'Develop alternative funding mechanisms',
                    'Establish economic sustainability monitoring framework'
                ]
            },
            'risk_matrix': {
                'title': 'Strategic Risk Assessment Matrix',
                'description': 'Multi-dimensional risk analysis covering strategic, operational, economic, and geopolitical factors.',
                'sources': [
                    'RAND Corporation - Risk Assessment Methodologies',
                    'Center for Naval Analyses (CNA) - Strategic Risk Framework',
                    'Brookings Institution - Regional Security Analysis',
                    'Atlantic Council - Geopolitical Risk Assessment',
                    'International Crisis Group - South Asia Reports'
                ],
                'use_cases': [
                    'Risk management and mitigation strategy development',
                    'Strategic planning and contingency preparation',
                    'Stakeholder communication and decision support',
                    'International engagement and confidence building',
                    'Crisis management and response planning'
                ],
                'recommendations': [
                    'Develop comprehensive risk mitigation strategies',
                    'Establish early warning and monitoring systems',
                    'Create contingency plans for high-risk scenarios',
                    'Implement regular risk assessment reviews',
                    'Build international cooperation mechanisms'
                ]
            },
            'power_balance': {
                'title': 'Regional Power Balance Shift',
                'description': 'Analysis of how Pakistan\'s submarine expansion would fundamentally alter the regional naval balance and strategic dynamics.',
                'sources': [
                    'International Institute for Strategic Studies (IISS) - Asia-Pacific Security',
                    'Center for Strategic and International Studies (CSIS) - South Asia Program',
                    'Brookings Institution - India-Pakistan Relations',
                    'Carnegie Endowment - Regional Security Analysis',
                    'Stimson Center - South Asia Security Studies'
                ],
                'use_cases': [
                    'Regional security architecture planning',
                    'Strategic balance assessment and response development',
                    'International relations and diplomatic strategy',
                    'Arms control and confidence-building measures',
                    'Crisis prevention and conflict resolution'
                ],
                'recommendations': [
                    'Engage in regional security dialogue and transparency measures',
                    'Develop confidence-building mechanisms with neighbors',
                    'Establish communication channels for crisis management',
                    'Participate in regional security cooperation frameworks',
                    'Consider arms control and limitation agreements'
                ]
            },
            'trade_impact': {
                'title': 'Trade Route Impact Assessment',
                'description': 'Analysis of potential impacts on commercial shipping routes, energy flows, and maritime trade security.',
                'sources': [
                    'International Maritime Organization (IMO) - Trade Route Data',
                    'World Trade Organization (WTO) - Maritime Trade Statistics',
                    'Energy Information Administration (EIA) - Energy Flow Analysis',
                    'Lloyd\'s List Intelligence - Shipping Route Analysis',
                    'Maritime Security Center - Trade Route Security'
                ],
                'use_cases': [
                    'Maritime trade security planning and coordination',
                    'Energy security and supply chain analysis',
                    'International shipping and insurance assessment',
                    'Port and infrastructure development planning',
                    'Maritime law enforcement and security cooperation'
                ],
                'recommendations': [
                    'Enhance maritime domain awareness and monitoring',
                    'Develop international maritime security cooperation',
                    'Establish trade route protection mechanisms',
                    'Improve port security and infrastructure',
                    'Create maritime incident response protocols'
                ]
            },
            'escalation_control': {
                'title': 'Escalation Control Mechanisms',
                'description': 'Analysis of how submarines provide escalation control capabilities and crisis management implications.',
                'sources': [
                    'RAND Corporation - Escalation Theory and Practice',
                    'Center for Naval Analyses (CNA) - Crisis Management Studies',
                    'Harvard Kennedy School - Nuclear Crisis Management',
                    'Princeton University - Strategic Stability Analysis',
                    'MIT Security Studies Program - Escalation Control'
                ],
                'use_cases': [
                    'Crisis management and escalation control planning',
                    'Strategic communication and signaling development',
                    'Command and control system design',
                    'International crisis response coordination',
                    'Strategic stability framework development'
                ],
                'recommendations': [
                    'Develop robust crisis communication protocols',
                    'Establish escalation control mechanisms and procedures',
                    'Create strategic signaling and communication channels',
                    'Build international crisis management cooperation',
                    'Implement confidence-building and transparency measures'
                ]
            }
        }
    
    def generate_tooltip_css(self) -> str:
        """Generate CSS for advanced tooltips"""
        return """
        /* Advanced Tooltip Styles */
        .advanced-tooltip {
            position: absolute;
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
            max-width: 450px;
            z-index: 10000;
            display: none;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }
        
        .advanced-tooltip h4 {
            color: #3498db;
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }
        
        .advanced-tooltip .tooltip-section {
            margin-bottom: 15px;
        }
        
        .advanced-tooltip .tooltip-section-title {
            color: #f39c12;
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        .advanced-tooltip .tooltip-content {
            margin-bottom: 12px;
            line-height: 1.5;
        }
        
        .advanced-tooltip .tooltip-sources {
            background: rgba(52, 152, 219, 0.2);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 0.9em;
        }
        
        .advanced-tooltip .tooltip-use-cases {
            background: rgba(46, 204, 113, 0.2);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 0.9em;
        }
        
        .advanced-tooltip .tooltip-recommendations {
            background: rgba(231, 76, 60, 0.2);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 0.9em;
        }
        
        .advanced-tooltip .tooltip-list {
            list-style: none;
            padding-left: 0;
        }
        
        .advanced-tooltip .tooltip-list li {
            margin-bottom: 5px;
            padding-left: 15px;
            position: relative;
        }
        
        .advanced-tooltip .tooltip-list li:before {
            content: "•";
            color: #3498db;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .tooltip-trigger {
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .tooltip-trigger:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        """
    
    def generate_tooltip_html(self, tooltip_id: str, data: Dict[str, Any]) -> str:
        """Generate HTML for a specific tooltip"""
        sources_html = '\n'.join([f'<li>{source}</li>' for source in data['sources']])
        use_cases_html = '\n'.join([f'<li>{use_case}</li>' for use_case in data['use_cases']])
        recommendations_html = '\n'.join([f'<li>{rec}</li>' for rec in data['recommendations']])
        
        return f"""
        <div id="{tooltip_id}" class="advanced-tooltip">
            <h4>{data['title']}</h4>
            <div class="tooltip-section">
                <div class="tooltip-section-title">Description</div>
                <div class="tooltip-content">{data['description']}</div>
            </div>
            <div class="tooltip-section">
                <div class="tooltip-section-title">Sources</div>
                <div class="tooltip-sources">
                    <ul class="tooltip-list">
                        {sources_html}
                    </ul>
                </div>
            </div>
            <div class="tooltip-section">
                <div class="tooltip-section-title">Use Cases</div>
                <div class="tooltip-use-cases">
                    <ul class="tooltip-list">
                        {use_cases_html}
                    </ul>
                </div>
            </div>
            <div class="tooltip-section">
                <div class="tooltip-section-title">Recommendations</div>
                <div class="tooltip-recommendations">
                    <ul class="tooltip-list">
                        {recommendations_html}
                    </ul>
                </div>
            </div>
        </div>
        """
    
    def generate_tooltip_javascript(self) -> str:
        """Generate JavaScript for tooltip functionality"""
        return """
        // Advanced Tooltip System
        class AdvancedTooltipManager {
            constructor() {
                this.activeTooltip = null;
                this.init();
            }
            
            init() {
                // Add event listeners to tooltip triggers
                document.addEventListener('DOMContentLoaded', () => {
                    this.setupTooltipTriggers();
                    this.setupGlobalEventListeners();
                });
            }
            
            setupTooltipTriggers() {
                const triggers = document.querySelectorAll('.tooltip-trigger');
                triggers.forEach(trigger => {
                    trigger.addEventListener('mouseenter', (e) => this.showTooltip(e));
                    trigger.addEventListener('mouseleave', (e) => this.hideTooltip(e));
                });
            }
            
            setupGlobalEventListeners() {
                document.addEventListener('mousemove', (e) => this.updateTooltipPosition(e));
                document.addEventListener('scroll', () => this.hideAllTooltips());
            }
            
            showTooltip(event) {
                const trigger = event.currentTarget;
                const tooltipId = trigger.getAttribute('data-tooltip');
                const tooltip = document.getElementById(tooltipId);
                
                if (tooltip) {
                    this.activeTooltip = tooltip;
                    tooltip.style.display = 'block';
                    this.updateTooltipPosition(event);
                }
            }
            
            hideTooltip(event) {
                const trigger = event.currentTarget;
                const tooltipId = trigger.getAttribute('data-tooltip');
                const tooltip = document.getElementById(tooltipId);
                
                if (tooltip) {
                    setTimeout(() => {
                        if (!tooltip.matches(':hover')) {
                            tooltip.style.display = 'none';
                            this.activeTooltip = null;
                        }
                    }, 100);
                }
            }
            
            updateTooltipPosition(event) {
                if (this.activeTooltip) {
                    const tooltip = this.activeTooltip;
                    const rect = tooltip.getBoundingClientRect();
                    const viewportWidth = window.innerWidth;
                    const viewportHeight = window.innerHeight;
                    
                    let x = event.clientX + 15;
                    let y = event.clientY - 15;
                    
                    // Adjust position if tooltip would go off-screen
                    if (x + rect.width > viewportWidth - 20) {
                        x = event.clientX - rect.width - 15;
                    }
                    
                    if (y + rect.height > viewportHeight - 20) {
                        y = event.clientY - rect.height - 15;
                    }
                    
                    // Ensure tooltip stays within viewport
                    x = Math.max(10, Math.min(x, viewportWidth - rect.width - 10));
                    y = Math.max(10, Math.min(y, viewportHeight - rect.height - 10));
                    
                    tooltip.style.left = x + 'px';
                    tooltip.style.top = y + 'px';
                }
            }
            
            hideAllTooltips() {
                const tooltips = document.querySelectorAll('.advanced-tooltip');
                tooltips.forEach(tooltip => {
                    tooltip.style.display = 'none';
                });
                this.activeTooltip = null;
            }
        }
        
        // Initialize tooltip manager
        const tooltipManager = new AdvancedTooltipManager();
        """
    
    def add_tooltips_to_html(self, html_content: str, report_type: str = 'dashboard') -> str:
        """Add advanced tooltips to HTML content"""
        
        # Add CSS
        css_pattern = r'(</style>)'
        tooltip_css = self.generate_tooltip_css()
        html_content = re.sub(css_pattern, f'{tooltip_css}\n    </style>', html_content, count=1)
        
        # Add tooltip HTML elements
        tooltip_html = ''
        for tooltip_id, data in self.tooltip_data.items():
            tooltip_html += self.generate_tooltip_html(tooltip_id, data)
        
        # Insert tooltip HTML before closing body tag
        body_pattern = r'(</body>)'
        html_content = re.sub(body_pattern, f'{tooltip_html}\n    </body>', html_content)
        
        # Add JavaScript
        js_pattern = r'(</script>)'
        tooltip_js = self.generate_tooltip_javascript()
        html_content = re.sub(js_pattern, f'{tooltip_js}\n    </script>', html_content, count=1)
        
        # Add tooltip triggers to chart sections
        if report_type == 'dashboard':
            html_content = self.add_dashboard_tooltip_triggers(html_content)
        else:
            html_content = self.add_card_analysis_tooltip_triggers(html_content)
        
        return html_content
    
    def add_dashboard_tooltip_triggers(self, html_content: str) -> str:
        """Add tooltip triggers to dashboard chart sections"""
        
        # Add tooltip triggers to chart sections
        chart_sections = [
            ('fleetComparisonChart', 'fleet_comparison'),
            ('economicChart', 'economic_impact'),
            ('riskMatrixChart', 'risk_matrix'),
            ('powerBalanceChart', 'power_balance'),
            ('tradeImpactChart', 'trade_impact'),
            ('escalationChart', 'escalation_control')
        ]
        
        for chart_id, tooltip_id in chart_sections:
            # Find chart wrapper and add tooltip trigger
            pattern = rf'(<div class="chart-wrapper">\s*<canvas id="{chart_id}"></canvas>\s*</div>)'
            replacement = f'<div class="chart-wrapper tooltip-trigger" data-tooltip="{tooltip_id}">\n                    <canvas id="{chart_id}"></canvas>\n                </div>'
            html_content = re.sub(pattern, replacement, html_content)
        
        # Add tooltip triggers to metric cards
        metric_pattern = r'(<div class="metric-card">)'
        replacement = r'\1 tooltip-trigger" data-tooltip="economic_impact">'
        html_content = re.sub(metric_pattern, replacement, html_content)
        
        return html_content
    
    def add_card_analysis_tooltip_triggers(self, html_content: str) -> str:
        """Add tooltip triggers to card analysis sections"""
        
        # Add tooltip triggers to metric cards
        metric_pattern = r'(<div class="metric-card"[^>]*>)'
        replacement = r'\1 tooltip-trigger" data-tooltip="fleet_comparison">'
        html_content = re.sub(metric_pattern, replacement, html_content)
        
        # Add tooltip triggers to module cards
        module_pattern = r'(<div class="module-card"[^>]*>)'
        replacement = r'\1 tooltip-trigger" data-tooltip="risk_matrix">'
        html_content = re.sub(module_pattern, replacement, html_content)
        
        # Add tooltip triggers to chart sections
        chart_pattern = r'(<div class="chart-section">)'
        replacement = r'\1 tooltip-trigger" data-tooltip="economic_impact">'
        html_content = re.sub(chart_pattern, replacement, html_content)
        
        return html_content
    
    def update_template(self, template_path: str, output_path: str):
        """Update template with advanced tooltip functionality"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Add tooltip functionality to template
            updated_content = self.add_tooltips_to_html(template_content, 'template')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info(f"Updated template: {output_path}")
            
        except Exception as e:
            logger.error(f"Error updating template {template_path}: {e}")
    
    def process_report(self, input_path: str, output_path: str, report_type: str = 'dashboard'):
        """Process a report file and add advanced tooltips"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Add tooltip functionality
            updated_content = self.add_tooltips_to_html(html_content, report_type)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            logger.info(f"Processed report: {output_path}")
            
        except Exception as e:
            logger.error(f"Error processing report {input_path}: {e}")

def main():
    """Main function to process reports and update templates"""
    generator = AdvancedTooltipGenerator()
    
    # Define paths
    base_path = Path("Results")
    template_path = Path("templates")
    
    # Process dashboard report
    dashboard_input = base_path / "pakistan_submarine_acquisition_dashboard.html"
    dashboard_output = base_path / "pakistan_submarine_acquisition_dashboard_enhanced.html"
    
    if dashboard_input.exists():
        generator.process_report(str(dashboard_input), str(dashboard_output), 'dashboard')
    
    # Process card analysis report
    card_input = base_path / "pakistan_submarine_card_analysis_2025.html"
    card_output = base_path / "pakistan_submarine_card_analysis_2025_enhanced.html"
    
    if card_input.exists():
        generator.process_report(str(card_input), str(card_output), 'card_analysis')
    
    # Update templates
    card_template = template_path / "card_analysis.html"
    card_template_enhanced = template_path / "card_analysis_enhanced.html"
    
    if card_template.exists():
        generator.update_template(str(card_template), str(card_template_enhanced))
    
    # Create enhanced dashboard template
    dashboard_template_enhanced = template_path / "dashboard_enhanced.html"
    generator.update_template(str(dashboard_input), str(dashboard_template_enhanced))

if __name__ == "__main__":
    main()
