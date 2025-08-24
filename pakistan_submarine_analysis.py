#!/usr/bin/env python3
"""
Pakistan Submarine Acquisition Analysis and Deterrence Enhancement
Comprehensive Strategic Analysis with Interactive Visualizations
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from datetime import datetime
import os


class PakistanSubmarineAnalysis:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = "Results/pakistan_submarine_analysis"
        os.makedirs(self.results_dir, exist_ok=True)
        
    def generate_submarine_fleet_comparison(self):
        """Generate submarine fleet comparison visualization"""
        
        # Pakistan submarine fleet data
        pakistan_fleet = {
            'Agosta 90B (Khalid-class)': {
                'count': 3, 'year': 1999, 'capability': 'AIP'
            },
            'Agosta 70 (Hashmat-class)': {
                'count': 2, 'year': 1979, 'capability': 'Conventional'
            },
            'Hangor-class (Under Construction)': {
                'count': 8, 'year': 2028, 'capability': 'AIP+'
            }
        }
        
        # Indian submarine fleet for comparison
        india_fleet = {
            'Arihant-class (SSBN)': {
                'count': 2, 'year': 2016, 'capability': 'Nuclear'
            },
            'Scorpene-class (Kalvari)': {
                'count': 6, 'year': 2017, 'capability': 'AIP'
            },
            'Sindhughosh-class': {
                'count': 8, 'year': 1986, 'capability': 'Conventional'
            },
            'Shishumar-class': {
                'count': 4, 'year': 1986, 'capability': 'Conventional'
            }
        }
        
        # Create comparison chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Pakistan Submarine Fleet', 'India Submarine Fleet', 
                          'Capability Comparison', 'Timeline Analysis'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Pakistan fleet bars
        pakistan_names = list(pakistan_fleet.keys())
        pakistan_counts = [pakistan_fleet[name]['count'] for name in pakistan_names]
        pakistan_colors = ['#0066cc', '#0066cc', '#ff6600']
        
        fig.add_trace(
            go.Bar(x=pakistan_names, y=pakistan_counts, name='Pakistan',
                   marker_color=pakistan_colors, showlegend=False),
            row=1, col=1
        )
        
        # India fleet bars
        india_names = list(india_fleet.keys())
        india_counts = [india_fleet[name]['count'] for name in india_names]
        india_colors = ['#ff9933', '#ff6600', '#cc3300', '#cc3300']
        
        fig.add_trace(
            go.Bar(x=india_names, y=india_counts, name='India',
                   marker_color=india_colors, showlegend=False),
            row=1, col=2
        )
        
        # Capability comparison
        capabilities = ['Conventional', 'AIP', 'AIP+', 'Nuclear']
        pak_cap_counts = [2, 3, 8, 0]
        ind_cap_counts = [12, 6, 0, 2]
        
        fig.add_trace(
            go.Scatter(x=capabilities, y=pak_cap_counts, mode='lines+markers',
                      name='Pakistan', line=dict(color='#0066cc', width=3)),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=capabilities, y=ind_cap_counts, mode='lines+markers',
                      name='India', line=dict(color='#ff6600', width=3)),
            row=2, col=1
        )
        
        # Timeline analysis
        years = [1979, 1986, 1999, 2016, 2017, 2028]
        pak_timeline = [2, 0, 3, 0, 0, 8]
        ind_timeline = [0, 12, 0, 2, 6, 0]
        
        fig.add_trace(
            go.Scatter(x=years, y=pak_timeline, mode='lines+markers',
                      name='Pakistan', line=dict(color='#0066cc', width=3)),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=years, y=ind_timeline, mode='lines+markers',
                      name='India', line=dict(color='#ff6600', width=3)),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Pakistan vs India Submarine Fleet Comparison",
            height=800,
            showlegend=True
        )
        
        return fig
    
    def generate_geopolitical_impact_analysis(self):
        """Generate geopolitical impact analysis visualization"""
        
        # Impact categories and scores
        categories = ['Regional Balance', 'Trade Security', 'Escalation Risk', 
                     'Deterrence Value', 'Strategic Depth', 'Alliance Dynamics']
        
        pakistan_impact = [8.5, 7.0, 6.5, 9.0, 8.0, 7.5]
        india_response = [7.0, 6.5, 8.0, 8.5, 7.5, 6.0]
        china_benefit = [9.0, 8.5, 5.0, 8.0, 9.0, 9.5]
        us_concern = [6.5, 7.5, 8.5, 7.0, 6.0, 8.0]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=pakistan_impact,
            theta=categories,
            fill='toself',
            name='Pakistan Benefit',
            line_color='#0066cc'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=india_response,
            theta=categories,
            fill='toself',
            name='India Response',
            line_color='#ff6600'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=china_benefit,
            theta=categories,
            fill='toself',
            name='China Benefit',
            line_color='#cc0000'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=us_concern,
            theta=categories,
            fill='toself',
            name='US Concern',
            line_color='#003366'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Geopolitical Impact Analysis of Pakistan Submarine Acquisition"
        )
        
        return fig
    
    def generate_trade_route_analysis(self):
        """Generate trade route impact analysis"""
        
        # Key trade routes and their vulnerability
        routes = ['Strait of Hormuz', 'Arabian Sea', 'Bay of Bengal', 
                 'Malacca Strait', 'Red Sea', 'Persian Gulf']
        
        current_risk = [6.5, 5.0, 4.5, 3.0, 5.5, 7.0]
        post_acquisition_risk = [7.5, 6.5, 5.5, 4.0, 6.5, 8.0]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Current Risk Level',
            x=routes,
            y=current_risk,
            marker_color='#ff9933'
        ))
        
        fig.add_trace(go.Bar(
            name='Post-Acquisition Risk',
            x=routes,
            y=post_acquisition_risk,
            marker_color='#cc0000'
        ))
        
        fig.update_layout(
            title="Trade Route Security Impact Analysis",
            xaxis_title="Trade Routes",
            yaxis_title="Risk Level (1-10)",
            barmode='group'
        )
        
        return fig
    
    def generate_escalation_dynamics(self):
        """Generate escalation dynamics analysis"""
        
        # Escalation scenarios and probabilities
        scenarios = ['Naval Skirmish', 'Blockade', 'Missile Exchange', 
                    'Nuclear Posturing', 'Alliance Involvement', 'Full Conflict']
        
        current_prob = [0.3, 0.1, 0.05, 0.2, 0.15, 0.02]
        post_acquisition_prob = [0.4, 0.2, 0.08, 0.25, 0.2, 0.03]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Current Probability',
            x=scenarios,
            y=current_prob,
            marker_color='#ff9933'
        ))
        
        fig.add_trace(go.Bar(
            name='Post-Acquisition Probability',
            x=scenarios,
            y=post_acquisition_prob,
            marker_color='#cc0000'
        ))
        
        fig.update_layout(
            title="Escalation Dynamics Analysis",
            xaxis_title="Escalation Scenarios",
            yaxis_title="Probability",
            barmode='group'
        )
        
        return fig
    
    def generate_strategic_map(self):
        """Generate strategic map of the region"""
        
        # Create a map centered on the Arabian Sea
        m = folium.Map(
            location=[20, 65],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add Pakistan submarine bases
        pakistan_bases = [
            {'name': 'Karachi Naval Base', 'coords': [24.8607, 66.9905], 'type': 'Main Base'},
            {'name': 'Orkara Naval Base', 'coords': [25.2083, 62.3275], 'type': 'Forward Base'},
            {'name': 'Gwadar Port', 'coords': [25.1264, 62.3223], 'type': 'Strategic Port'}
        ]
        
        for base in pakistan_bases:
            folium.Marker(
                location=base['coords'],
                popup=f"<b>{base['name']}</b><br>Type: {base['type']}",
                icon=folium.Icon(color='blue', icon='anchor')
            ).add_to(m)
        
        # Add Indian naval bases
        india_bases = [
            {'name': 'Mumbai Naval Base', 'coords': [19.0760, 72.8777], 'type': 'Western Command'},
            {'name': 'Visakhapatnam', 'coords': [17.6868, 83.2185], 'type': 'Eastern Command'},
            {'name': 'Kochi Naval Base', 'coords': [9.9312, 76.2673], 'type': 'Southern Command'}
        ]
        
        for base in india_bases:
            folium.Marker(
                location=base['coords'],
                popup=f"<b>{base['name']}</b><br>Type: {base['type']}",
                icon=folium.Icon(color='red', icon='anchor')
            ).add_to(m)
        
        # Add key trade routes
        trade_routes = [
            {'name': 'Strait of Hormuz', 'coords': [26.5920, 56.2474]},
            {'name': 'Malacca Strait', 'coords': [1.3521, 103.8198]},
            {'name': 'Bab el-Mandeb', 'coords': [12.5850, 43.1450]}
        ]
        
        for route in trade_routes:
            folium.Marker(
                location=route['coords'],
                popup=f"<b>{route['name']}</b><br>Critical Trade Chokepoint",
                icon=folium.Icon(color='green', icon='info-sign')
            ).add_to(m)
        
        return m
    
    def generate_enhanced_html_report(self):
        """Generate comprehensive enhanced HTML report"""
        
        # Generate all visualizations
        fleet_comparison = self.generate_submarine_fleet_comparison()
        geopolitical_impact = self.generate_geopolitical_impact_analysis()
        trade_analysis = self.generate_trade_route_analysis()
        escalation_dynamics = self.generate_escalation_dynamics()
        strategic_map = self.generate_strategic_map()
        
        # Save visualizations
        fleet_comparison.write_html(f"{self.results_dir}/fleet_comparison.html")
        geopolitical_impact.write_html(f"{self.results_dir}/geopolitical_impact.html")
        trade_analysis.write_html(f"{self.results_dir}/trade_analysis.html")
        escalation_dynamics.write_html(f"{self.results_dir}/escalation_dynamics.html")
        strategic_map.save(f"{self.results_dir}/strategic_map.html")
        
        # Create comprehensive HTML report
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pakistan Submarine Acquisition Analysis - {self.timestamp}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/js/all.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        
        .header {{
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .section {{
            margin: 40px 0;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #007bff;
        }}
        
        .section h2 {{
            color: #007bff;
            margin-top: 0;
            font-size: 1.8em;
        }}
        
        .tooltip {{
            position: relative;
            display: inline-block;
            cursor: help;
        }}
        
        .tooltip .tooltiptext {{
            visibility: hidden;
            width: 300px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
        
        .key-findings {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .finding-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #28a745;
        }}
        
        .finding-card h3 {{
            color: #28a745;
            margin-top: 0;
        }}
        
        .visualization-container {{
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .nav-tabs {{
            display: flex;
            border-bottom: 2px solid #dee2e6;
            margin-bottom: 20px;
        }}
        
        .nav-tab {{
            padding: 10px 20px;
            cursor: pointer;
            border: none;
            background: none;
            color: #6c757d;
            border-bottom: 2px solid transparent;
        }}
        
        .nav-tab.active {{
            color: #007bff;
            border-bottom-color: #007bff;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .conclusion {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-top: 40px;
        }}
        
        .conclusion h2 {{
            margin-top: 0;
        }}
        
        .recommendations {{
            background: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .recommendations h3 {{
            color: #28a745;
            margin-top: 0;
        }}
        
        .recommendations ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        
        .recommendations li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-submarine"></i> Pakistan Submarine Acquisition Analysis</h1>
            <p>Comprehensive Strategic Analysis of Deterrence Enhancement and Geopolitical Impact</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
        </div>

        <div class="section">
            <h2><i class="fas fa-chart-line"></i> Executive Summary</h2>
            <p>This comprehensive analysis examines Pakistan's submarine acquisition programs, particularly the <span class="tooltip">Hangor-class submarines<span class="tooltiptext">8 advanced submarines being built in collaboration with China, featuring AIP technology and enhanced stealth capabilities</span></span>, and their strategic implications for regional security, trade routes, and global geopolitics.</p>
            
            <div class="key-findings">
                <div class="finding-card">
                    <h3><i class="fas fa-balance-scale"></i> Balance of Power Shift</h3>
                    <p>The acquisition of 8 Hangor-class submarines will significantly enhance Pakistan's naval capabilities, potentially altering the regional military balance in the Indian Ocean.</p>
                </div>
                
                <div class="finding-card">
                    <h3><i class="fas fa-globe-asia"></i> Geopolitical Implications</h3>
                    <p>This acquisition strengthens Pakistan-China strategic partnership while potentially escalating tensions with India and raising concerns among Western powers.</p>
                </div>
                
                <div class="finding-card">
                    <h3><i class="fas fa-ship"></i> Trade Route Impact</h3>
                    <p>Enhanced submarine capabilities will affect security dynamics in critical trade routes including the Strait of Hormuz and Arabian Sea.</p>
                </div>
                
                <div class="finding-card">
                    <h3><i class="fas fa-exclamation-triangle"></i> Escalation Risks</h3>
                    <p>While enhancing deterrence, the acquisition may increase escalation risks in South Asia, particularly in maritime domains.</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2><i class="fas fa-chart-bar"></i> Fleet Comparison Analysis</h2>
            <div class="visualization-container">
                <iframe src="fleet_comparison.html" width="100%" height="800" frameborder="0"></iframe>
            </div>
            <p><strong>Key Insights:</strong> Pakistan's submarine fleet will grow from 5 to 13 vessels by 2028, with 8 advanced AIP-capable submarines. This represents a significant capability leap, though India maintains numerical superiority with 20 submarines including nuclear-powered vessels.</p>
        </div>

        <div class="section">
            <h2><i class="fas fa-globe"></i> Geopolitical Impact Analysis</h2>
            <div class="visualization-container">
                <iframe src="geopolitical_impact.html" width="100%" height="600" frameborder="0"></iframe>
            </div>
            <p><strong>Strategic Implications:</strong> The acquisition provides Pakistan with enhanced deterrence capabilities while strengthening China's strategic position in the Indian Ocean. This development may trigger counter-responses from India and raise concerns among Western powers about regional stability.</p>
        </div>

        <div class="section">
            <h2><i class="fas fa-route"></i> Trade Route Security Analysis</h2>
            <div class="visualization-container">
                <iframe src="trade_analysis.html" width="100%" height="500" frameborder="0"></iframe>
            </div>
            <p><strong>Maritime Security Impact:</strong> Enhanced submarine capabilities will affect security dynamics in critical trade routes. The Strait of Hormuz and Persian Gulf regions show the highest risk increase, potentially impacting global energy supplies.</p>
        </div>

        <div class="section">
            <h2><i class="fas fa-map-marked-alt"></i> Strategic Geographic Analysis</h2>
            <div class="visualization-container">
                <iframe src="strategic_map.html" width="100%" height="600" frameborder="0"></iframe>
            </div>
            <p><strong>Geographic Implications:</strong> Pakistan's naval bases in Karachi, Orkara, and Gwadar provide strategic positioning for submarine operations in the Arabian Sea and Indian Ocean, enabling enhanced maritime domain awareness and potential power projection.</p>
        </div>

        <div class="section">
            <h2><i class="fas fa-exclamation-triangle"></i> Escalation Dynamics Analysis</h2>
            <div class="visualization-container">
                <iframe src="escalation_dynamics.html" width="100%" height="500" frameborder="0"></iframe>
            </div>
            <p><strong>Risk Assessment:</strong> While the acquisition enhances Pakistan's deterrence capabilities, it may increase the probability of various escalation scenarios, particularly naval skirmishes and nuclear posturing. However, the overall risk of full-scale conflict remains low.</p>
        </div>

        <div class="conclusion">
            <h2><i class="fas fa-lightbulb"></i> Strategic Conclusions</h2>
            <p>Pakistan's submarine acquisition represents a significant enhancement of its naval capabilities and strategic deterrence posture. The program will:</p>
            <ul>
                <li>Strengthen Pakistan's maritime security and power projection capabilities</li>
                <li>Enhance the strategic partnership with China</li>
                <li>Potentially trigger counter-responses from India</li>
                <li>Impact regional trade route security dynamics</li>
                <li>Raise concerns among Western powers about regional stability</li>
            </ul>
            
            <div class="recommendations">
                <h3><i class="fas fa-clipboard-list"></i> Policy Recommendations</h3>
                <ul>
                    <li><strong>Regional Dialogue:</strong> Encourage confidence-building measures between Pakistan and India</li>
                    <li><strong>Transparency:</strong> Promote greater transparency in naval modernization programs</li>
                    <li><strong>Conflict Prevention:</strong> Strengthen maritime incident prevention mechanisms</li>
                    <li><strong>International Cooperation:</strong> Enhance regional maritime security cooperation</li>
                    <li><strong>Risk Mitigation:</strong> Develop protocols for submarine encounters and communications</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <h2><i class="fas fa-info-circle"></i> Methodology and Data Sources</h2>
            <p>This analysis is based on:</p>
            <ul>
                <li>Open-source intelligence on naval capabilities and acquisitions</li>
                <li>Strategic analysis of regional military balance</li>
                <li>Geopolitical impact assessment using multi-dimensional analysis</li>
                <li>Trade route security analysis considering maritime chokepoints</li>
                <li>Escalation dynamics modeling based on historical patterns</li>
            </ul>
        </div>
    </div>

    <script>
        // Advanced tooltip functionality
        document.addEventListener('DOMContentLoaded', function() {{
            // Add interactive features
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(tooltip => {{
                tooltip.addEventListener('mouseenter', function() {{
                    this.querySelector('.tooltiptext').style.visibility = 'visible';
                    this.querySelector('.tooltiptext').style.opacity = '1';
                }});
                
                tooltip.addEventListener('mouseleave', function() {{
                    this.querySelector('.tooltiptext').style.visibility = 'hidden';
                    this.querySelector('.tooltiptext').style.opacity = '0';
                }});
            }});
            
            // Add smooth scrolling
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }});
            }});
        }});
    </script>
</body>
</html>
        """
        
        # Save the comprehensive report
        report_path = f"{self.results_dir}/pakistan_submarine_analysis_{self.timestamp}.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Comprehensive analysis report generated: {report_path}")
        return report_path

def main():
    """Main execution function"""
    print("Starting Pakistan Submarine Acquisition Analysis...")
    
    analyzer = PakistanSubmarineAnalysis()
    report_path = analyzer.generate_enhanced_html_report()
    
    print(f"\nAnalysis completed successfully!")
    print(f"Report saved to: {report_path}")
    print(f"Interactive visualizations and advanced tooltips included")
    print(f"Comprehensive analysis covers:")
    print("- Submarine fleet comparison")
    print("- Geopolitical impact assessment")
    print("- Trade route security analysis")
    print("- Escalation dynamics modeling")
    print("- Strategic geographic analysis")

if __name__ == "__main__":
    main()
