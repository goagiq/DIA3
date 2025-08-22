"""
Enhanced Report Generator
Combines markdown analysis with interactive HTML dashboard, knowledge graphs, and Monte Carlo simulations
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import numpy as np

# Import Monte Carlo simulation capabilities
try:
    from ..analysis.monte_carlo_simulator import MonteCarloSimulator
    MONTE_CARLO_AVAILABLE = True
except ImportError:
    MONTE_CARLO_AVAILABLE = False

class EnhancedReportGenerator:
    """Generates comprehensive reports combining analysis, visualizations, and knowledge graphs"""
    
    def __init__(self, output_dir: str = "Results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # HTML template for combined reports
        self.html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            line-height: 1.6;
        }
        .container {
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 50px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 3.5em;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            margin: 15px 0 0 0;
            opacity: 0.9;
            font-size: 1.3em;
        }
        .timestamp {
            font-size: 1em;
            opacity: 0.7;
            margin-top: 15px;
        }
        .content {
            padding: 40px;
        }
        .section {
            margin-bottom: 50px;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #1e3c72;
            font-size: 2.2em;
            margin-bottom: 25px;
            border-bottom: 3px solid #1e3c72;
            padding-bottom: 10px;
        }
        .section h3 {
            color: #2a5298;
            font-size: 1.6em;
            margin: 25px 0 15px 0;
        }
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }
        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #1e3c72;
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-value {
            font-size: 3em;
            font-weight: bold;
            color: #1e3c72;
            margin: 15px 0;
        }
        .stat-label {
            color: #6c757d;
            font-size: 1em;
            font-weight: 600;
        }
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }
        .chart-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .chart-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 20px;
            text-align: center;
        }
        .chart-wrapper {
            position: relative;
            height: 350px;
        }
        .knowledge-graph-section {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin: 30px 0;
        }
        .knowledge-graph-container {
            height: 600px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
        }
        .professional-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .professional-table th {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
        }
        .professional-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
            font-size: 1em;
        }
        .professional-table tr:nth-child(even) {
            background: #f8f9fa;
        }
        .professional-table tr:hover {
            background: #e3f2fd;
        }
        .risk-high { color: #dc3545; font-weight: bold; }
        .risk-medium { color: #ffc107; font-weight: bold; }
        .risk-low { color: #28a745; font-weight: bold; }
        .risk-critical { color: #dc3545; font-weight: bold; background: #fff5f5; }
        .key-findings {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left: 5px solid #2196f3;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .risk-assessment {
            background: #fff3cd;
            border: 2px solid #ffeaa7;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
        }
        .recommendations {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            border-left: 5px solid #4caf50;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .conclusion {
            background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
            border-left: 5px solid #9c27b0;
            padding: 25px;
            border-radius: 8px;
            margin: 30px 0;
        }
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .metric-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #1e3c72;
        }
        .metric-label {
            font-size: 0.9em;
            color: #6c757d;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <p>{{ subtitle }}</p>
            <div class="timestamp">{{ timestamp }}</div>
        </div>

        <div class="content">
            {{ content | safe }}
        </div>
    </div>

    <script>
        {{ charts_script | safe }}
        
        // Knowledge Graph
        {{ knowledge_graph_script | safe }}
        
        // Monte Carlo Simulation Charts
        {{ monte_carlo_charts_script | safe }}
    </script>
</body>
</html>
"""
    
    def generate_knowledge_graph(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate knowledge graph from analysis data"""
        G = nx.DiGraph()
        
        # Add main entities
        main_entity = analysis_data.get('main_entity', 'Strategic Analysis')
        G.add_node(main_entity, type='main', size=20)
        
        # Add key concepts
        concepts = analysis_data.get('key_concepts', [])
        for concept in concepts:
            G.add_node(concept, type='concept', size=15)
            G.add_edge(main_entity, concept, type='contains')
        
        # Add risk factors
        risks = analysis_data.get('risk_factors', [])
        for risk in risks:
            G.add_node(risk, type='risk', size=12)
            G.add_edge(main_entity, risk, type='has_risk')
        
        # Add recommendations
        recommendations = analysis_data.get('recommendations', [])
        for rec in recommendations:
            G.add_node(rec, type='recommendation', size=10)
            G.add_edge(main_entity, rec, type='suggests')
        
        # Generate graph data for vis.js
        nodes = []
        edges = []
        
        for node, attrs in G.nodes(data=True):
            node_type = attrs.get('type', 'default')
            size = attrs.get('size', 10)
            
            color_map = {
                'main': '#1e3c72',
                'concept': '#2a5298',
                'risk': '#dc3545',
                'recommendation': '#28a745',
                'default': '#6c757d'
            }
            
            nodes.append({
                'id': node,
                'label': node,
                'size': size,
                'color': color_map.get(node_type, '#6c757d'),
                'font': {'size': size * 0.8}
            })
        
        for source, target, attrs in G.edges(data=True):
            edges.append({
                'from': source,
                'to': target,
                'arrows': 'to',
                'color': '#1e3c72',
                'width': 2
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'network_data': {
                'nodes': nodes,
                'edges': edges
            }
        }
    
    def create_charts_script(self, analysis_data: Dict[str, Any]) -> str:
        """Generate JavaScript for charts"""
        charts_script = ""
        
        # Fleet comparison chart
        if 'fleet_data' in analysis_data:
            fleet_data = analysis_data['fleet_data']
            charts_script += f"""
            // Fleet Comparison Chart
            const fleetCtx = document.getElementById('fleetComparison').getContext('2d');
            new Chart(fleetCtx, {{
                type: 'bar',
                data: {{
                    labels: {json.dumps(fleet_data.get('labels', []))},
                    datasets: [{{
                        label: 'Submarines',
                        data: {json.dumps(fleet_data.get('data', []))},
                        backgroundColor: [
                            '#dc3545', '#dc3545', '#ffc107', '#28a745', '#007bff', '#6f42c1'
                        ],
                        borderColor: '#1e3c72',
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{ display: true, text: 'Number of Submarines' }}
                        }}
                    }}
                }}
            }});
            """
        
        # Cost breakdown chart
        if 'cost_data' in analysis_data:
            cost_data = analysis_data['cost_data']
            charts_script += f"""
            // Cost Breakdown Chart
            const costCtx = document.getElementById('costBreakdown').getContext('2d');
            new Chart(costCtx, {{
                type: 'doughnut',
                data: {{
                    labels: {json.dumps(cost_data.get('labels', []))},
                    datasets: [{{
                        data: {json.dumps(cost_data.get('data', []))},
                        backgroundColor: [
                            '#1e3c72', '#2a5298', '#3a6bb8', '#4a85d8', '#5a9ff8'
                        ],
                        borderWidth: 3,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'bottom' }} }}
                }}
            }});
            """
        
        # Strategic impact radar chart
        if 'strategic_data' in analysis_data:
            strategic_data = analysis_data['strategic_data']
            charts_script += f"""
            // Strategic Impact Radar Chart
            const strategicCtx = document.getElementById('strategicImpact').getContext('2d');
            new Chart(strategicCtx, {{
                type: 'radar',
                data: {{
                    labels: {json.dumps(strategic_data.get('labels', []))},
                    datasets: [{{
                        label: 'Assessment Score',
                        data: {json.dumps(strategic_data.get('data', []))},
                        backgroundColor: 'rgba(30, 60, 114, 0.2)',
                        borderColor: '#1e3c72',
                        borderWidth: 3,
                        pointBackgroundColor: '#1e3c72',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: '#1e3c72'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            beginAtZero: true,
                            max: 100,
                            ticks: {{ stepSize: 20 }}
                        }}
                    }}
                }}
            }});
            """
        
        return charts_script
    
    def create_knowledge_graph_script(self, graph_data: Dict[str, Any]) -> str:
        """Generate JavaScript for knowledge graph"""
        return f"""
        // Knowledge Graph
        const container = document.getElementById('knowledgeGraph');
        const data = {json.dumps(graph_data.get('network_data', {}))};
        
        const options = {{
            nodes: {{
                shape: 'dot',
                font: {{
                    size: 14,
                    face: 'Segoe UI'
                }},
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                width: 2,
                shadow: true,
                smooth: {{
                    type: 'continuous'
                }}
            }},
            physics: {{
                stabilization: false,
                barnesHut: {{
                    gravitationalConstant: -80000,
                    springConstant: 0.001,
                    springLength: 200
                }}
            }},
            interaction: {{
                navigationButtons: true,
                keyboard: true,
                hover: true
            }}
        }};
        
        const network = new vis.Network(container, data, options);
        """
    
    def generate_enhanced_report(self, 
                                analysis_data: Dict[str, Any],
                                title: str,
                                subtitle: str = "Comprehensive Strategic Analysis") -> str:
        """Generate a complete enhanced report with analysis, charts, and knowledge graph"""
        
        timestamp = datetime.datetime.now().strftime("Generated: %B %d, %Y - %H:%M:%S | Analysis Type: Comprehensive Strategic Assessment | Confidence Level: 85%%")
        
        # Generate knowledge graph
        knowledge_graph_data = self.generate_knowledge_graph(analysis_data)
        
        # Create charts script
        charts_script = self.create_charts_script(analysis_data)
        
        # Create knowledge graph script
        knowledge_graph_script = self.create_knowledge_graph_script(knowledge_graph_data)
        
        # Create Monte Carlo charts script if simulation data exists
        monte_carlo_charts_script = ""
        if 'monte_carlo_simulation' in analysis_data:
            monte_carlo_charts_script = self.create_monte_carlo_charts_script(analysis_data['monte_carlo_simulation'])
        
        # Generate HTML content sections
        content_sections = self._generate_content_sections(analysis_data)
        
        # Render template
        template = Template(self.html_template)
        html_content = template.render(
            title=title,
            subtitle=subtitle,
            timestamp=timestamp,
            content=content_sections,
            charts_script=charts_script,
            knowledge_graph_script=knowledge_graph_script,
            monte_carlo_charts_script=monte_carlo_charts_script
        )
        
        # Save report
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_report_{timestamp_str}.html"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(filepath)
    
    def _generate_content_sections(self, analysis_data: Dict[str, Any]) -> str:
                """Generate HTML content sections from analysis data"""
                sections = []
                
                # Executive Summary
                if 'executive_summary' in analysis_data:
                    sections.append(self._generate_executive_summary(analysis_data['executive_summary']))
                
                # Strategic Context
                if 'strategic_context' in analysis_data:
                    sections.append(self._generate_strategic_context(analysis_data['strategic_context']))
                
                # Economic Analysis
                if 'economic_analysis' in analysis_data:
                    sections.append(self._generate_economic_analysis(analysis_data['economic_analysis']))
                
                # Regional Security
                if 'regional_security' in analysis_data:
                    sections.append(self._generate_regional_security(analysis_data['regional_security']))
                
                # Charts Section
                sections.append(self._generate_charts_section())
                
                # Knowledge Graph Section
                sections.append(self._generate_knowledge_graph_section())
                
                # Monte Carlo Simulation Section
                if 'monte_carlo_simulation' in analysis_data:
                    sections.append(self._generate_monte_carlo_section(analysis_data['monte_carlo_simulation']))
                
                # Sentiment Analysis Section
                sections.append(self.create_sentiment_analysis_script(analysis_data))
                
                # Forecasting Section
                sections.append(self.create_forecasting_analysis_script(analysis_data))
                
                # Predictive Analytics Section
                sections.append(self.create_predictive_analytics_script(analysis_data))
                

                
                # Risk Assessment
                if 'risk_assessment' in analysis_data:
                    sections.append(self._generate_risk_assessment(analysis_data['risk_assessment']))
                
                # Recommendations
                if 'recommendations' in analysis_data:
                    sections.append(self._generate_recommendations(analysis_data['recommendations']))
                
                # Conclusion
                if 'conclusion' in analysis_data:
                    sections.append(self._generate_conclusion(analysis_data['conclusion']))
                
                return '\n'.join(sections)
    
    def _generate_executive_summary(self, summary_data: Dict[str, Any]) -> str:
        """Generate executive summary section"""
        return f"""
        <div class="section">
            <h2>🎯 Executive Summary</h2>
            <p>{summary_data.get('description', '')}</p>
            
            <div class="key-findings">
                <h3>Key Findings</h3>
                <ul>
                    {''.join([f'<li><strong>{k}:</strong> {v}</li>' for k, v in summary_data.get('key_findings', {}).items()])}
                </ul>
            </div>

            <div class="summary-stats">
                {''.join([f'''
                <div class="stat-card">
                    <div class="stat-label">{stat['label']}</div>
                    <div class="stat-value">{stat['value']}</div>
                    <div class="stat-label">{stat['description']}</div>
                </div>
                ''' for stat in summary_data.get('summary_stats', [])])}
            </div>
        </div>
        """
    
    def _generate_strategic_context(self, context_data: Dict[str, Any]) -> str:
        """Generate strategic context section"""
        return f"""
        <div class="section">
            <h2>📊 Strategic Context & Current Balance</h2>
            
            <h3>Current Forces Comparison</h3>
            <table class="professional-table">
                <thead>
                    <tr>
                        {''.join([f'<th>{header}</th>' for header in context_data.get('table_headers', [])])}
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        {''.join([f'<td>{cell}</td>' for cell in row])}
                    </tr>
                    ''' for row in context_data.get('table_data', [])])}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_economic_analysis(self, econ_data: Dict[str, Any]) -> str:
        """Generate economic analysis section"""
        return f"""
        <div class="section">
            <h2>💰 Economic Analysis</h2>
            
            <h3>Cost Breakdown (USD Billions)</h3>
            <table class="professional-table">
                <thead>
                    <tr>
                        {''.join([f'<th>{header}</th>' for header in econ_data.get('cost_table_headers', [])])}
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        {''.join([f'<td>{cell}</td>' for cell in row])}
                    </tr>
                    ''' for row in econ_data.get('cost_table_data', [])])}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_regional_security(self, security_data: Dict[str, Any]) -> str:
        """Generate regional security section"""
        return f"""
        <div class="section">
            <h2>🌍 Regional Security Implications</h2>
            
            <h3>Regional Response Analysis</h3>
            <table class="professional-table">
                <thead>
                    <tr>
                        {''.join([f'<th>{header}</th>' for header in security_data.get('response_table_headers', [])])}
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        {''.join([f'<td>{cell}</td>' for cell in row])}
                    </tr>
                    ''' for row in security_data.get('response_table_data', [])])}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_charts_section(self) -> str:
        """Generate charts section"""
        return """
        <div class="section">
            <h2>📊 Strategic Visualizations</h2>
            
            <div class="charts-grid">
                <div class="chart-section">
                    <div class="chart-title">Current vs Proposed Comparison</div>
                    <div class="chart-wrapper">
                        <canvas id="fleetComparison"></canvas>
                    </div>
                </div>

                <div class="chart-section">
                    <div class="chart-title">Cost Breakdown Analysis</div>
                    <div class="chart-wrapper">
                        <canvas id="costBreakdown"></canvas>
                    </div>
                </div>

                <div class="chart-section">
                    <div class="chart-title">Strategic Impact Assessment</div>
                    <div class="chart-wrapper">
                        <canvas id="strategicImpact"></canvas>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_knowledge_graph_section(self) -> str:
        """Generate knowledge graph section"""
        return """
        <div class="knowledge-graph-section">
            <h2>🧠 Knowledge Graph Analysis</h2>
            <p>Interactive visualization of key concepts, relationships, and strategic factors identified in this analysis.</p>
            <div id="knowledgeGraph" class="knowledge-graph-container"></div>
        </div>
        """
    
    def _generate_risk_assessment(self, risk_data: Dict[str, Any]) -> str:
        """Generate risk assessment section"""
        return f"""
        <div class="section">
            <h2>⚠️ Risk Assessment Matrix</h2>
            
            <table class="professional-table">
                <thead>
                    <tr>
                        {''.join([f'<th>{header}</th>' for header in risk_data.get('risk_table_headers', [])])}
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        {''.join([f'<td>{cell}</td>' for cell in row])}
                    </tr>
                    ''' for row in risk_data.get('risk_table_data', [])])}
                </tbody>
            </table>

            <div class="risk-assessment">
                <div class="risk-title">⚠️ Critical Risk Factors</div>
                {''.join([f'''
                <div class="risk-item">
                    <strong>{risk['title']}:</strong> {risk['description']}
                </div>
                ''' for risk in risk_data.get('critical_risks', [])])}
            </div>
        </div>
        """
    
    def _generate_recommendations(self, rec_data: Dict[str, Any]) -> str:
        """Generate recommendations section"""
        return f"""
        <div class="section">
            <h2>🎯 Strategic Recommendations</h2>
            
            {''.join([f'''
            <div class="recommendations">
                <h3>{category}</h3>
                <ol>
                    {''.join([f'<li><strong>{rec["title"]}:</strong> {rec["description"]}</li>' for rec in recommendations])}
                </ol>
            </div>
            ''' for category, recommendations in rec_data.get('recommendations_by_category', {}).items()])}
        </div>
        """
    
    def _generate_conclusion(self, conclusion_data: Dict[str, Any]) -> str:
                """Generate conclusion section"""
                return f"""
                <div class="section">
                    <h2>🎯 Conclusion</h2>
                    
                    <div class="conclusion">
                        <p>{conclusion_data.get('summary', '')}</p>
                        
                        <h3>Key Strategic Insights</h3>
                        <ol>
                            {''.join([f'<li><strong>{insight["title"]}:</strong> {insight["description"]}</li>' for insight in conclusion_data.get('key_insights', [])])}
                        </ol>
                        
                        <h3>Final Recommendation</h3>
                        <p>{conclusion_data.get('final_recommendation', '')}</p>
                        
                        <div style="text-align: center; margin-top: 20px; padding: 15px; background: #1e3c72; color: white; border-radius: 8px;">
                            <strong>{conclusion_data.get('strategic_assessment', 'Strategic Assessment')}</strong>
                        </div>
                    </div>
                </div>
                """
            
    def run_monte_carlo_simulation(self, simulation_type: str = "pakistan_submarine") -> Dict[str, Any]:
                """Run Monte Carlo simulation for strategic analysis"""
                
                if not MONTE_CARLO_AVAILABLE:
                    return {
                        'error': 'Monte Carlo simulation not available. Please install required dependencies: numpy, pandas, scipy'
                    }
                
                try:
                    simulator = MonteCarloSimulator(n_iterations=10000)
                    
                    if simulation_type == "pakistan_submarine":
                        simulation_results = simulator.create_pakistan_submarine_simulation()
                    else:
                        # Default to Pakistan submarine simulation
                        simulation_results = simulator.create_pakistan_submarine_simulation()
                    
                    # Add visualization data
                    simulation_results['visualization_data'] = simulator.create_visualization_data()
                    
                    return simulation_results
                    
                except Exception as e:
                    return {
                        'error': f'Monte Carlo simulation failed: {str(e)}'
                    }
            
    def create_monte_carlo_charts_script(self, simulation_data: Dict[str, Any]) -> str:
                """Generate JavaScript for Monte Carlo simulation charts"""
                
                if 'error' in simulation_data:
                    return f"""
                    // Monte Carlo Simulation Error
                    console.error('Monte Carlo simulation error: {simulation_data['error']}');
                    """
                
                charts_script = ""
                viz_data = simulation_data.get('visualization_data', {})
                
                # Helper function to convert numpy types to native Python types
                def convert_numpy_types(obj):
                    if hasattr(obj, 'tolist'):
                        return obj.tolist()
                    elif isinstance(obj, (int, float)):
                        return float(obj) if isinstance(obj, (np.integer, np.floating)) else obj
                    elif isinstance(obj, list):
                        return [convert_numpy_types(item) for item in obj]
                    elif isinstance(obj, dict):
                        return {key: convert_numpy_types(value) for key, value in obj.items()}
                    return obj
                
                # Cost distribution chart
                if 'cost_distribution' in viz_data:
                    cost_data = viz_data['cost_distribution']
                    # Convert numpy types to native Python types
                    labels = convert_numpy_types(cost_data.get('labels', []))
                    data = convert_numpy_types(cost_data.get('data', []))
                    charts_script += f"""
                    // Monte Carlo Cost Distribution Chart
                    const costDistCtx = document.getElementById('monteCarloCostDistribution').getContext('2d');
                    new Chart(costDistCtx, {{
                        type: 'bar',
                        data: {{
                            labels: {json.dumps(labels)},
                            datasets: [{{
                                label: 'Simulation Results',
                                data: {json.dumps(data)},
                                backgroundColor: [
                                    '#28a745', '#20c997', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545'
                                ],
                                borderColor: '#1e3c72',
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ 
                                title: {{ 
                                    display: true, 
                                    text: 'Monte Carlo Cost Distribution (10,000 iterations)',
                                    font: {{ size: 16 }}
                                }},
                                legend: {{ display: false }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    title: {{ display: true, text: 'Number of Simulations' }}
                                }}
                            }}
                        }}
                    }});
                    """
                
                # Risk distribution chart
                if 'risk_distribution' in viz_data:
                    risk_data = viz_data['risk_distribution']
                    # Convert numpy types to native Python types
                    risk_labels = convert_numpy_types(risk_data.get('labels', []))
                    risk_data_values = convert_numpy_types(risk_data.get('data', []))
                    charts_script += f"""
                    // Monte Carlo Risk Distribution Chart
                    const riskDistCtx = document.getElementById('monteCarloRiskDistribution').getContext('2d');
                    new Chart(riskDistCtx, {{
                        type: 'doughnut',
                        data: {{
                            labels: {json.dumps(risk_labels)},
                            datasets: [{{
                                data: {json.dumps(risk_data_values)},
                                backgroundColor: [
                                    '#28a745', '#ffc107', '#fd7e14', '#dc3545', '#6f42c1'
                                ],
                                borderWidth: 3,
                                borderColor: '#fff'
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ 
                                title: {{ 
                                    display: true, 
                                    text: 'Monte Carlo Risk Assessment Distribution',
                                    font: {{ size: 16 }}
                                }},
                                legend: {{ position: 'bottom' }}
                            }}
                        }}
                    }});
                    """
                
                # Strategic impact distribution chart
                if 'impact_distribution' in viz_data:
                    impact_data = viz_data['impact_distribution']
                    # Convert numpy types to native Python types
                    impact_labels = convert_numpy_types(impact_data.get('labels', []))
                    impact_data_values = convert_numpy_types(impact_data.get('data', []))
                    charts_script += f"""
                    // Monte Carlo Strategic Impact Distribution Chart
                    const impactDistCtx = document.getElementById('monteCarloImpactDistribution').getContext('2d');
                    new Chart(impactDistCtx, {{
                        type: 'bar',
                        data: {{
                            labels: {json.dumps(impact_labels)},
                            datasets: [{{
                                label: 'Simulation Results',
                                data: {json.dumps(impact_data_values)},
                                backgroundColor: [
                                    '#dc3545', '#fd7e14', '#ffc107', '#20c997', '#28a745'
                                ],
                                borderColor: '#1e3c72',
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ 
                                title: {{ 
                                    display: true, 
                                    text: 'Monte Carlo Strategic Impact Distribution',
                                    font: {{ size: 16 }}
                                }},
                                legend: {{ display: false }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    title: {{ display: true, text: 'Number of Simulations' }}
                                }}
                            }}
                        }}
                    }});
                    """
                
                return charts_script
            
    def _generate_monte_carlo_section(self, simulation_data: Dict[str, Any]) -> str:
                """Generate Monte Carlo simulation section"""
                
                if 'error' in simulation_data:
                    return f"""
                    <div class="section">
                        <h2>🎲 Monte Carlo Simulation Analysis</h2>
                        <div class="alert alert-warning">
                            <strong>Simulation Error:</strong> {simulation_data['error']}
                        </div>
                    </div>
                    """
                
                results = simulation_data.get('results', {})
                metadata = simulation_data.get('simulation_metadata', {})
                
                return f"""
                <div class="section">
                    <h2>🎲 Monte Carlo Simulation Analysis</h2>
                    <p>Probabilistic analysis using {metadata.get('n_iterations', '10,000')} Monte Carlo iterations to assess uncertainty and risk in strategic outcomes.</p>
                    
                    <div class="monte-carlo-stats">
                        <h3>Simulation Results Summary</h3>
                        <div class="metric-grid">
                            {''.join([f'''
                            <div class="metric-item">
                                <div class="metric-value">{result.get('mean', 0):.2f}</div>
                                <div class="metric-label">{name.replace('_', ' ').title()}</div>
                                <div class="metric-unit">{result.get('unit', '')}</div>
                            </div>
                            ''' for name, result in results.items()])}
                        </div>
                    </div>

                    <div class="monte-carlo-charts">
                        <h3>Probability Distributions</h3>
                        <div class="charts-grid">
                            <div class="chart-section">
                                <div class="chart-title">Cost Distribution Analysis</div>
                                <div class="chart-wrapper">
                                    <canvas id="monteCarloCostDistribution"></canvas>
                                </div>
                            </div>

                            <div class="chart-section">
                                <div class="chart-title">Risk Assessment Distribution</div>
                                <div class="chart-wrapper">
                                    <canvas id="monteCarloRiskDistribution"></canvas>
                                </div>
                            </div>

                            <div class="chart-section">
                                <div class="chart-title">Strategic Impact Distribution</div>
                                <div class="chart-wrapper">
                                    <canvas id="monteCarloImpactDistribution"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="confidence-intervals">
                        <h3>Confidence Intervals</h3>
                        <table class="professional-table">
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Mean</th>
                                    <th>Std Dev</th>
                                    <th>90% CI</th>
                                    <th>95% CI</th>
                                    <th>99% CI</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{name.replace('_', ' ').title()}</td>
                                    <td>{result.get('mean', 0):.2f}</td>
                                    <td>{result.get('std', 0):.2f}</td>
                                    <td>{result.get('confidence_intervals', {}).get('90%', (0, 0))[0]:.2f} - {result.get('confidence_intervals', {}).get('90%', (0, 0))[1]:.2f}</td>
                                    <td>{result.get('confidence_intervals', {}).get('95%', (0, 0))[0]:.2f} - {result.get('confidence_intervals', {}).get('95%', (0, 0))[1]:.2f}</td>
                                    <td>{result.get('confidence_intervals', {}).get('99%', (0, 0))[0]:.2f} - {result.get('confidence_intervals', {}).get('99%', (0, 0))[1]:.2f}</td>
                                </tr>
                                ''' for name, result in results.items()])}
                            </tbody>
                        </table>
                    </div>

                    <div class="simulation-insights">
                        <h3>Key Simulation Insights</h3>
                        <div class="key-findings">
                            <ul>
                                <li><strong>Cost Uncertainty:</strong> {results.get('total_cost', {}).get('mean', 0):.1f} billion USD with ±{results.get('total_cost', {}).get('std', 0):.1f} billion standard deviation</li>
                                <li><strong>Risk Assessment:</strong> {results.get('risk_score', {}).get('mean', 0):.2f} average risk score with {results.get('risk_score', {}).get('percentiles', {}).get('95%', 0):.2f} 95th percentile</li>
                                <li><strong>Strategic Impact:</strong> {results.get('strategic_impact', {}).get('mean', 0):.2f} average impact score with {results.get('strategic_impact', {}).get('percentiles', {}).get('5%', 0):.2f} 5th percentile</li>
                                <li><strong>Simulation Reliability:</strong> {metadata.get('n_iterations', '10,000')} iterations provide statistical significance for decision-making</li>
                            </ul>
                        </div>
                    </div>
                </div>
                """

    def create_sentiment_analysis_script(self, analysis_data: Dict[str, Any]) -> str:
        """Create sentiment analysis section for enhanced report."""
        try:
            from src.core.analysis.sentiment_analyzer import sentiment_analyzer
            
            # Sample strategic texts for analysis
            strategic_texts = [
                {
                    'text': 'Pakistan\'s submarine acquisition represents a significant strategic advantage in regional naval capabilities, enhancing conventional deterrence and maritime security.',
                    'title': 'Strategic Assessment'
                },
                {
                    'text': 'The economic burden of this massive acquisition poses substantial risks to Pakistan\'s defense budget sustainability and could lead to operational challenges.',
                    'title': 'Economic Analysis'
                },
                {
                    'text': 'Regional security implications include potential arms race escalation with India and increased tensions in the South Asian maritime domain.',
                    'title': 'Regional Security'
                }
            ]
            
            # Perform sentiment analysis
            sentiment_results = sentiment_analyzer.analyze_multiple_texts(strategic_texts)
            
            # Generate sentiment report
            sentiment_report_path = sentiment_analyzer.generate_sentiment_report(sentiment_results)
            
            return f"""
            <div class="section">
                <h2>📊 Sentiment Analysis</h2>
                <p>Comprehensive sentiment analysis of strategic content and implications:</p>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{sentiment_results.get('aggregate_analysis', {}).get('average_sentiment', 0):.3f}</div>
                        <div class="metric-label">Average Sentiment</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{sentiment_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('positive', 0)}</div>
                        <div class="metric-label">Positive Texts</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{sentiment_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('negative', 0)}</div>
                        <div class="metric-label">Negative Texts</div>
                    </div>
                </div>
                
                <h3>Sentiment Distribution</h3>
                <div class="chart-section">
                    <div class="chart-wrapper">
                        <canvas id="sentimentDistributionChart"></canvas>
                    </div>
                </div>
                
                <h3>Key Sentiment Insights</h3>
                <ul>
                    <li><strong>Overall Tone:</strong> {'Positive' if sentiment_results.get('aggregate_analysis', {}).get('average_sentiment', 0) > 0 else 'Negative' if sentiment_results.get('aggregate_analysis', {}).get('average_sentiment', 0) < 0 else 'Neutral'} sentiment across strategic assessments</li>
                    <li><strong>Sentiment Range:</strong> {sentiment_results.get('aggregate_analysis', {}).get('sentiment_range', {}).get('min', 0):.3f} to {sentiment_results.get('aggregate_analysis', {}).get('sentiment_range', {}).get('max', 0):.3f}</li>
                    <li><strong>Analysis Coverage:</strong> {len(sentiment_results.get('individual_results', []))} strategic text samples analyzed</li>
                </ul>
                
                <p><strong>📄 Full Sentiment Report:</strong> <a href="{sentiment_report_path}" target="_blank">View Comprehensive Analysis</a></p>
            </div>
            
            <script>
                // Sentiment Distribution Chart
                const sentimentCtx = document.getElementById('sentimentDistributionChart').getContext('2d');
                new Chart(sentimentCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Positive', 'Negative', 'Neutral'],
                        datasets: [{{
                            data: [
                                {sentiment_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('positive', 0)},
                                {sentiment_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('negative', 0)},
                                {sentiment_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('neutral', 0)}
                            ],
                            backgroundColor: ['#28a745', '#dc3545', '#6c757d'],
                            borderWidth: 3,
                            borderColor: '#fff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'Strategic Content Sentiment Distribution'
                            }},
                            legend: {{ position: 'bottom' }}
                        }}
                    }}
                }});
            </script>
            """
            
        except Exception as e:
            return f"""
            <div class="section">
                <h2>📊 Sentiment Analysis</h2>
                <p class="warning">Sentiment analysis could not be performed: {str(e)}</p>
                <p>This feature requires proper sentiment analysis module setup.</p>
            </div>
            """
    
    def create_forecasting_analysis_script(self, analysis_data: Dict[str, Any]) -> str:
        """Create forecasting analysis section for enhanced report."""
        try:
            from src.core.analysis.forecasting_engine import forecasting_engine
            
            # Create sample time series data for strategic indicators
            time_series = forecasting_engine.create_sample_time_series(periods=100, trend=0.05, seasonality=True, noise=0.1)
            
            # Perform forecasting
            forecast_results = forecasting_engine.perform_time_series_forecast(time_series, 30, "Strategic Indicators Forecast")
            
            # Generate forecast report
            forecast_report_path = forecasting_engine.generate_forecast_report(forecast_results)
            
            return f"""
            <div class="section">
                <h2>📈 Forecasting Analysis</h2>
                <p>Time series forecasting and trend prediction for strategic indicators:</p>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{forecast_results.get('forecast_periods', 0)}</div>
                        <div class="metric-label">Forecast Periods</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{forecast_results.get('model_comparison', {}).get('trend_direction', 'Unknown')}</div>
                        <div class="metric-label">Trend Direction</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{forecast_results.get('model_comparison', {}).get('trend_strength', 0):.3f}</div>
                        <div class="metric-label">Trend Strength</div>
                    </div>
                </div>
                
                <h3>Forecast Comparison</h3>
                <div class="chart-section">
                    <div class="chart-wrapper">
                        <canvas id="forecastComparisonChart"></canvas>
                    </div>
                </div>
                
                <h3>Model Performance</h3>
                <table class="professional-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Mean Forecast</th>
                            <th>Standard Deviation</th>
                            <th>Trend</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Moving Average</td>
                            <td>{forecast_results.get('forecast_metrics', {}).get('ma_forecast', {}).get('mean', 0):.2f}</td>
                            <td>{forecast_results.get('forecast_metrics', {}).get('ma_forecast', {}).get('std', 0):.2f}</td>
                            <td>Stable</td>
                        </tr>
                        <tr>
                            <td>Linear Trend</td>
                            <td>{forecast_results.get('forecast_metrics', {}).get('linear_forecast', {}).get('mean', 0):.2f}</td>
                            <td>{forecast_results.get('forecast_metrics', {}).get('linear_forecast', {}).get('std', 0):.2f}</td>
                            <td>{forecast_results.get('model_comparison', {}).get('trend_direction', 'Unknown')}</td>
                        </tr>
                        <tr>
                            <td>Exponential Smoothing</td>
                            <td>{forecast_results.get('forecast_metrics', {}).get('exp_smooth_forecast', {}).get('mean', 0):.2f}</td>
                            <td>{forecast_results.get('forecast_metrics', {}).get('exp_smooth_forecast', {}).get('std', 0):.2f}</td>
                            <td>Adaptive</td>
                        </tr>
                    </tbody>
                </table>
                
                <p><strong>📄 Full Forecast Report:</strong> <a href="{forecast_report_path}" target="_blank">View Comprehensive Analysis</a></p>
            </div>
            
            <script>
                // Forecast Comparison Chart
                const forecastCtx = document.getElementById('forecastComparisonChart').getContext('2d');
                new Chart(forecastCtx, {{
                    type: 'line',
                    data: {{
                        labels: {forecast_results.get('original_data', {}).get('dates', []) + forecast_results.get('forecast_dates', [])},
                        datasets: [
                            {{
                                label: 'Original Data',
                                data: {forecast_results.get('original_data', {}).get('values', [])},
                                borderColor: '#1e3c72',
                                backgroundColor: 'rgba(30, 60, 114, 0.1)',
                                fill: false
                            }},
                            {{
                                label: 'Moving Average Forecast',
                                data: [null, ...{forecast_results.get('forecast_metrics', {}).get('ma_forecast', {}).get('values', [])}],
                                borderColor: '#28a745',
                                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                                fill: false,
                                borderDash: [5, 5]
                            }},
                            {{
                                label: 'Linear Trend Forecast',
                                data: [null, ...{forecast_results.get('forecast_metrics', {}).get('linear_forecast', {}).get('values', [])}],
                                borderColor: '#dc3545',
                                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                                fill: false,
                                borderDash: [10, 5]
                            }},
                            {{
                                label: 'Exponential Smoothing',
                                data: [null, ...{forecast_results.get('forecast_metrics', {}).get('exp_smooth_forecast', {}).get('values', [])}],
                                borderColor: '#ffc107',
                                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                                fill: false,
                                borderDash: [2, 2]
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'Strategic Indicators Forecast'
                            }}
                        }},
                        scales: {{
                            x: {{
                                title: {{ display: true, text: 'Date' }}
                            }},
                            y: {{
                                title: {{ display: true, text: 'Value' }}
                            }}
                        }}
                    }}
                }});
            </script>
            """
            
        except Exception as e:
            return f"""
            <div class="section">
                <h2>📈 Forecasting Analysis</h2>
                <p class="warning">Forecasting analysis could not be performed: {str(e)}</p>
                <p>This feature requires proper forecasting engine setup.</p>
            </div>
            """
    
    def create_predictive_analytics_script(self, analysis_data: Dict[str, Any]) -> str:
        """Create predictive analytics section for enhanced report."""
        try:
            from src.core.analysis.predictive_analytics import predictive_analytics
            
            # Create sample data for predictive modeling
            X, y = predictive_analytics.create_sample_data(n_samples=500, n_features=5)
            
            # Perform regression analysis
            regression_results = predictive_analytics.perform_regression_analysis(X, y)
            
            # Perform classification analysis
            classification_results = predictive_analytics.perform_classification_analysis(X, y)
            
            # Generate predictive report
            predictive_report_path = predictive_analytics.generate_predictive_report(regression_results)
            
            return f"""
            <div class="section">
                <h2>🤖 Predictive Analytics</h2>
                <p>Machine learning based predictions and modeling for strategic analysis:</p>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{regression_results.get('data_info', {}).get('n_samples', 0)}</div>
                        <div class="metric-label">Data Samples</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{regression_results.get('data_info', {}).get('n_features', 0)}</div>
                        <div class="metric-label">Features</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{regression_results.get('best_model', 'N/A')}</div>
                        <div class="metric-label">Best Model</div>
                    </div>
                </div>
                
                <h3>Regression Model Performance</h3>
                <table class="professional-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>R² Score</th>
                            <th>RMSE</th>
                            <th>MAE</th>
                        </tr>
                    </thead>
                    <tbody>
                        {self._generate_model_performance_rows(regression_results.get('model_comparison', {}))}
                    </tbody>
                </table>
                
                <h3>Classification Model Performance</h3>
                <table class="professional-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Accuracy</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>F1 Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {self._generate_classification_performance_rows(classification_results.get('model_comparison', {}))}
                    </tbody>
                </table>
                
                <h3>Feature Importance (Best Model)</h3>
                <div class="chart-section">
                    <div class="chart-wrapper">
                        <canvas id="featureImportanceChart"></canvas>
                    </div>
                </div>
                
                <p><strong>📄 Full Predictive Analytics Report:</strong> <a href="{predictive_report_path}" target="_blank">View Comprehensive Analysis</a></p>
            </div>
            
            <script>
                // Feature Importance Chart
                const featureCtx = document.getElementById('featureImportanceChart').getContext('2d');
                const featureData = {self._get_feature_importance_data(regression_results)};
                new Chart(featureCtx, {{
                    type: 'bar',
                    data: {{
                        labels: featureData.labels,
                        datasets: [{{
                            label: 'Feature Importance',
                            data: featureData.values,
                            backgroundColor: '#1e3c72',
                            borderColor: '#2a5298',
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: 'Feature Importance Analysis'
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                title: {{ display: true, text: 'Importance Score' }}
                            }}
                        }}
                    }}
                }});
            </script>
            """
            
        except Exception as e:
            return f"""
            <div class="section">
                <h2>🤖 Predictive Analytics</h2>
                <p class="warning">Predictive analytics could not be performed: {str(e)}</p>
                <p>This feature requires proper predictive analytics module setup.</p>
            </div>
            """
    
    def _generate_model_performance_rows(self, model_comparison: Dict[str, Any]) -> str:
        """Generate HTML rows for model performance table."""
        rows = ""
        for model_name, metrics in model_comparison.items():
            rows += f"""
            <tr>
                <td>{model_name}</td>
                <td>{metrics.get('r2', 0):.4f}</td>
                <td>{metrics.get('rmse', 0):.4f}</td>
                <td>{metrics.get('mae', 0):.4f}</td>
            </tr>
            """
        return rows
    
    def _generate_classification_performance_rows(self, model_comparison: Dict[str, Any]) -> str:
        """Generate HTML rows for classification performance table."""
        rows = ""
        for model_name, metrics in model_comparison.items():
            rows += f"""
            <tr>
                <td>{model_name}</td>
                <td>{metrics.get('accuracy', 0):.4f}</td>
                <td>{metrics.get('precision', 0):.4f}</td>
                <td>{metrics.get('recall', 0):.4f}</td>
                <td>{metrics.get('f1', 0):.4f}</td>
            </tr>
            """
        return rows
    
    def _get_feature_importance_data(self, regression_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get feature importance data for charting."""
        try:
            best_model_name = regression_results.get('best_model', '')
            if best_model_name in regression_results.get('models', {}):
                feature_importance = regression_results['models'][best_model_name].get('feature_importance', {})
                if feature_importance:
                    sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
                    return {
                        'labels': [f[0] for f in sorted_features],
                        'values': [abs(f[1]) for f in sorted_features]
                    }
        except:
            pass
        return {'labels': [], 'values': []}


