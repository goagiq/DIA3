#!/usr/bin/env python3
"""
Enhanced Report Generator with Interactive Tooltips

This module provides functionality to generate enhanced HTML reports with
interactive tooltips that provide detailed explanations for numerical values
and technical terms in the report.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from .enhanced_report_orchestrator import EnhancedReportOrchestrator


class EnhancedReportWithTooltips:
    """
    Enhanced report generator that includes interactive tooltips for better
    user experience and understanding of complex metrics.
    """
    
    def __init__(self, output_dir: str = "Results"):
        """
        Initialize the enhanced report generator with tooltips.
        
        Args:
            output_dir: Directory to save generated reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.orchestrator = EnhancedReportOrchestrator()
        
    def generate_enhanced_report(self, 
                                query: str = "Pakistan submarine capabilities analysis",
                                include_tooltips: bool = True,
                                beautiful_styling: bool = True) -> Dict[str, Any]:
        """
        Generate an enhanced HTML report with interactive tooltips.
        
        Args:
            query: The analysis query
            include_tooltips: Whether to include interactive tooltips
            beautiful_styling: Whether to use enhanced styling
            
        Returns:
            Dictionary containing report details
        """
        # Generate base report using orchestrator
        base_report = self.orchestrator.generate_enhanced_report(
            query=query,
            beautiful_styling=beautiful_styling
        )
        
        if not include_tooltips:
            return base_report
            
        # Read the generated HTML content
        html_file_path = Path(base_report['file_path'])
        if not html_file_path.exists():
            raise FileNotFoundError(f"Generated report not found: {html_file_path}")
            
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Enhance HTML with tooltips
        enhanced_html = self._add_tooltips_to_html(html_content)
        
        # Save enhanced report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        enhanced_filename = f"enhanced_report_with_tooltips_{timestamp}.html"
        enhanced_file_path = self.output_dir / enhanced_filename
        
        with open(enhanced_file_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
            
        return {
            'file_path': str(enhanced_file_path),
            'filename': enhanced_filename,
            'query': query,
            'include_tooltips': include_tooltips,
            'beautiful_styling': beautiful_styling,
            'generated_at': datetime.now().isoformat(),
            'file_size': enhanced_file_path.stat().st_size
        }
        
    def _add_tooltips_to_html(self, html_content: str) -> str:
        """
        Add interactive tooltips to the HTML content.
        
        Args:
            html_content: Original HTML content
            
        Returns:
            Enhanced HTML content with tooltips
        """
        # Add CSS for tooltips
        tooltip_css = self._get_tooltip_css()
        
        # Add JavaScript for tooltip functionality
        tooltip_js = self._get_tooltip_javascript()
        
        # Add HTML modal structure
        tooltip_modal = self._get_tooltip_modal_html()
        
        # Insert CSS in head section
        if '<head>' in html_content:
            html_content = html_content.replace(
                '</head>',
                f'{tooltip_css}\n</head>'
            )
        
        # Insert JavaScript before closing body tag
        if '</body>' in html_content:
            html_content = html_content.replace(
                '</body>',
                f'{tooltip_modal}\n{tooltip_js}\n</body>'
            )
            
        # Add clickable classes to relevant elements
        html_content = self._add_clickable_classes(html_content)
        
        return html_content
        
    def _get_tooltip_css(self) -> str:
        """Get CSS styles for tooltip modal."""
        return """
        <style>
        /* Tooltip Modal Styles */
        .tooltip-modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }
        
        .tooltip-modal-content {
            background-color: #fefefe;
            margin: 5% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 600px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            position: relative;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .tooltip-close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            position: absolute;
            right: 15px;
            top: 10px;
        }
        
        .tooltip-close:hover,
        .tooltip-close:focus {
            color: #000;
            text-decoration: none;
        }
        
        .tooltip-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .tooltip-content {
            line-height: 1.6;
            color: #34495e;
        }
        
        .tooltip-content h3 {
            color: #2c3e50;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        .tooltip-content ul {
            margin-left: 20px;
        }
        
        .tooltip-content li {
            margin-bottom: 8px;
        }
        
        /* Clickable elements */
        .clickable {
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .clickable:hover {
            background-color: rgba(52, 152, 219, 0.1);
            border-radius: 4px;
            padding: 2px 4px;
            margin: -2px -4px;
        }
        
        .feature-score.clickable {
            color: #3498db;
            text-decoration: underline;
            text-decoration-style: dotted;
        }
        
        .table-value.clickable {
            background-color: rgba(52, 152, 219, 0.05);
            border-radius: 3px;
            padding: 1px 3px;
        }
        
        .metric-value.clickable {
            color: #e74c3c;
            font-weight: bold;
        }
        </style>
        """
        
    def _get_tooltip_javascript(self) -> str:
        """Get JavaScript for tooltip functionality."""
        return """
        <script>
        const tooltipData = {
            'feature-importance': {
                title: 'Feature Importance Analysis',
                content: `
                    <h3>Understanding Feature Importance Scores</h3>
                    <p>Feature importance scores (0.0 to 1.0) indicate how much each factor contributes to the overall analysis:</p>
                    <ul>
                        <li><strong>0.9-1.0:</strong> Critical factor - extremely high impact on outcomes</li>
                        <li><strong>0.7-0.89:</strong> Very important factor - significant influence</li>
                        <li><strong>0.5-0.69:</strong> Important factor - moderate but notable impact</li>
                        <li><strong>0.3-0.49:</strong> Somewhat important - limited but measurable effect</li>
                        <li><strong>0.1-0.29:</strong> Minor factor - minimal impact</li>
                        <li><strong>0.0-0.09:</strong> Negligible factor - virtually no impact</li>
                    </ul>
                    <h3>Calculation Method</h3>
                    <p>Scores are calculated using machine learning algorithms that analyze historical data patterns, 
                    expert assessments, and strategic simulations to determine each factor's relative importance 
                    in predicting outcomes.</p>
                `
            },
            'capability-forecast': {
                title: 'Strategic Capability Forecasts',
                content: `
                    <h3>Understanding Capability Forecast Values</h3>
                    <p>Capability forecast values represent predicted capability levels on a scale of 0.0 to 1.0:</p>
                    <ul>
                        <li><strong>0.0-0.2:</strong> Minimal capability - basic functionality only</li>
                        <li><strong>0.21-0.4:</strong> Limited capability - below average performance</li>
                        <li><strong>0.41-0.6:</strong> Moderate capability - average performance</li>
                        <li><strong>0.61-0.8:</strong> Good capability - above average performance</li>
                        <li><strong>0.81-0.9:</strong> High capability - excellent performance</li>
                        <li><strong>0.91-1.0:</strong> Superior capability - world-class performance</li>
                    </ul>
                    <h3>Time Horizon Interpretation</h3>
                    <p>Values are shown for different time periods (1-year, 3-year, 5-year horizons) to show 
                    how capabilities are expected to evolve over time based on current trends, planned 
                    investments, and strategic initiatives.</p>
                `
            },
            'confidence-interval': {
                title: 'Confidence Intervals (±Values)',
                content: `
                    <h3>Understanding Confidence Intervals</h3>
                    <p>Confidence intervals (e.g., ±0.08) indicate the uncertainty range around predictions:</p>
                    <ul>
                        <li><strong>±0.05 or less:</strong> High confidence - very reliable prediction</li>
                        <li><strong>±0.06-0.10:</strong> Good confidence - reasonably reliable</li>
                        <li><strong>±0.11-0.15:</strong> Moderate confidence - some uncertainty</li>
                        <li><strong>±0.16-0.20:</strong> Low confidence - significant uncertainty</li>
                        <li><strong>±0.21 or more:</strong> Very low confidence - highly uncertain</li>
                    </ul>
                    <h3>What This Means</h3>
                    <p>A forecast of 0.75 ±0.08 means we're 95% confident the true value will fall 
                    between 0.67 and 0.83. The smaller the interval, the more confident we are in our prediction.</p>
                `
            },
            'monte-carlo': {
                title: 'Monte Carlo Simulation Results',
                content: `
                    <h3>Understanding Monte Carlo Values</h3>
                    <p>Monte Carlo simulation values represent probability-based outcomes from thousands of simulations:</p>
                    <ul>
                        <li><strong>Probability values (0.0-1.0):</strong> Likelihood of achieving specific outcomes</li>
                        <li><strong>Expected values:</strong> Average outcome across all simulations</li>
                        <li><strong>Percentile values:</strong> Outcomes at specific probability thresholds</li>
                    </ul>
                    <h3>Simulation Process</h3>
                    <p>Each simulation randomly varies input parameters within realistic ranges to model 
                    different possible scenarios. Results show the distribution of possible outcomes 
                    and their associated probabilities.</p>
                `
            }
        };
        
        function showTooltip(type) {
            const modal = document.getElementById('tooltipModal');
            const title = document.getElementById('tooltipTitle');
            const content = document.getElementById('tooltipContent');
            
            if (tooltipData[type]) {
                title.innerHTML = tooltipData[type].title;
                content.innerHTML = tooltipData[type].content;
                modal.style.display = 'block';
            }
        }
        
        function closeTooltip() {
            const modal = document.getElementById('tooltipModal');
            modal.style.display = 'none';
        }
        
        // Close modal when clicking outside of it
        window.onclick = function(event) {
            const modal = document.getElementById('tooltipModal');
            if (event.target === modal) {
                closeTooltip();
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            // Add clickable class and onclick handlers to feature importance scores
            const featureScores = document.querySelectorAll('.feature-score');
            featureScores.forEach(score => {
                score.classList.add('clickable');
                score.onclick = function() {
                    showTooltip('feature-importance');
                };
            });
            
            // Add clickable class and onclick handlers to table values
            const tableValues = document.querySelectorAll('.professional-table td');
            tableValues.forEach(cell => {
                const text = cell.textContent.trim();
                if (/^[0-9.]+$/.test(text) || text.includes('±')) {
                    cell.classList.add('clickable');
                    if (text.includes('±')) {
                        cell.onclick = function() {
                            showTooltip('confidence-interval');
                        };
                    } else {
                        cell.onclick = function() {
                            showTooltip('capability-forecast');
                        };
                    }
                }
            });
            
            // Add clickable class and onclick handlers to metric values
            const metricValues = document.querySelectorAll('.metric-item .metric-value');
            metricValues.forEach(value => {
                value.classList.add('clickable');
                value.onclick = function() {
                    showTooltip('monte-carlo');
                };
            });
            
            // Add clickable class to headers
            const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            headers.forEach(header => {
                if (header.textContent.includes('Feature Importance') || 
                    header.textContent.includes('Capability Forecast') ||
                    header.textContent.includes('Monte Carlo')) {
                    header.classList.add('clickable');
                    header.onclick = function() {
                        if (header.textContent.includes('Feature Importance')) {
                            showTooltip('feature-importance');
                        } else if (header.textContent.includes('Capability Forecast')) {
                            showTooltip('capability-forecast');
                        } else if (header.textContent.includes('Monte Carlo')) {
                            showTooltip('monte-carlo');
                        }
                    };
                }
            });
        });
        </script>
        """
        
    def _get_tooltip_modal_html(self) -> str:
        """Get HTML structure for tooltip modal."""
        return """
        <div id="tooltipModal" class="tooltip-modal">
            <div class="tooltip-modal-content">
                <span class="tooltip-close" onclick="closeTooltip()">&times;</span>
                <div id="tooltipTitle" class="tooltip-title"></div>
                <div id="tooltipContent" class="tooltip-content"></div>
            </div>
        </div>
        """
        
    def _add_clickable_classes(self, html_content: str) -> str:
        """
        Add clickable classes to relevant HTML elements.
        
        Args:
            html_content: HTML content to modify
            
        Returns:
            Modified HTML content with clickable classes
        """
        # This is a simplified approach - in practice, the JavaScript handles
        # the dynamic addition of classes and event handlers
        return html_content
