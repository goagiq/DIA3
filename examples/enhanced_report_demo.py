#!/usr/bin/env python3
"""
Enhanced Report Generation Demo
Demonstrates the enhanced report generation functionality with knowledge graphs
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def demo_enhanced_report_generation():
    """Demonstrate enhanced report generation"""
    
    print("🚀 Enhanced Report Generation Demo")
    print("=" * 50)
    
    try:
        # Import the enhanced report integration
        from core.export.enhanced_report_integration import (
            generate_enhanced_report,
            generate_custom_enhanced_report
        )
        
        print("✅ Successfully imported enhanced report integration")
        
        # Demo 1: Generate Pakistan submarine analysis report
        print("\n📊 Demo 1: Pakistan Submarine Analysis Report")
        print("-" * 40)
        
        report_path1 = generate_enhanced_report(
            analysis_type="pakistan_submarine",
            title="Pakistan's 50-Submarine Acquisition",
            subtitle="Comprehensive Strategic Analysis for Conventional Deterrence"
        )
        
        print(f"✅ Report generated: {report_path1}")
        
        # Demo 2: Generate custom knowledge graph report
        print("\n🧠 Demo 2: Custom Knowledge Graph Report")
        print("-" * 40)
        
        custom_data = {
            'main_entity': 'Strategic Intelligence Analysis',
            'key_concepts': [
                'Intelligence Collection',
                'Analysis Methods',
                'Strategic Planning',
                'Risk Assessment',
                'Decision Support',
                'Technology Integration'
            ],
            'risk_factors': [
                'Data Quality Issues',
                'Analysis Bias',
                'Timeline Constraints',
                'Resource Limitations',
                'Security Concerns'
            ],
            'recommendations': [
                'Enhanced Data Validation',
                'Multi-Source Analysis',
                'Automated Processing',
                'Continuous Monitoring',
                'Stakeholder Engagement'
            ],
            'executive_summary': {
                'description': 'Comprehensive strategic intelligence analysis framework with enhanced visualization capabilities.',
                'key_findings': {
                    'Intelligence Quality': 'High-quality intelligence requires multiple validation layers',
                    'Analysis Efficiency': 'Automated tools can improve analysis speed by 60%',
                    'Risk Mitigation': 'Proactive risk assessment reduces operational failures by 40%',
                    'Strategic Value': 'Integrated intelligence provides 3x better decision support'
                },
                'summary_stats': [
                    {'label': 'Analysis Speed', 'value': '+60%', 'description': 'Improvement with automation'},
                    {'label': 'Risk Reduction', 'value': '40%', 'description': 'Failure rate reduction'},
                    {'label': 'Decision Quality', 'value': '3x', 'description': 'Better decision support'},
                    {'label': 'Data Sources', 'value': '15+', 'description': 'Integrated sources'},
                    {'label': 'Processing Time', 'value': '-70%', 'description': 'Time reduction'},
                    {'label': 'Accuracy', 'value': '95%', 'description': 'Analysis accuracy'}
                ]
            },
            'strategic_context': {
                'table_headers': ['Component', 'Current State', 'Target State', 'Improvement', 'Priority'],
                'table_data': [
                    ['Data Collection', 'Manual', 'Automated', 'High', 'Critical'],
                    ['Analysis Methods', 'Basic', 'Advanced AI', 'Medium', 'High'],
                    ['Visualization', 'Static', 'Interactive', 'High', 'Medium'],
                    ['Reporting', 'Text-based', 'Multi-format', 'Medium', 'Medium'],
                    ['Integration', 'Limited', 'Full-stack', 'High', 'Critical']
                ]
            },
            'fleet_data': {
                'labels': ['Manual Analysis', 'Semi-Automated', 'Fully Automated', 'AI-Enhanced', 'Integrated Platform'],
                'data': [10, 25, 45, 70, 95]
            },
            'cost_data': {
                'labels': ['Infrastructure', 'Software Licenses', 'Training', 'Integration', 'Maintenance'],
                'data': [30, 25, 20, 15, 10]
            },
            'strategic_data': {
                'labels': ['Efficiency', 'Accuracy', 'Speed', 'Integration', 'Scalability', 'Cost-Effectiveness'],
                'data': [85, 90, 75, 80, 70, 65]
            }
        }
        
        report_path2 = generate_custom_enhanced_report(
            analysis_data=custom_data,
            title="Strategic Intelligence Analysis Framework",
            subtitle="Enhanced Intelligence Capabilities with Knowledge Graph Integration"
        )
        
        print(f"✅ Custom report generated: {report_path2}")
        
        # Demo 3: Generate knowledge graph focused report
        print("\n🔗 Demo 3: Knowledge Graph Focused Report")
        print("-" * 40)
        
        # Create a focused knowledge graph analysis
        kg_data = {
            'main_entity': 'Cybersecurity Threat Intelligence',
            'key_concepts': [
                'Threat Actors',
                'Attack Vectors',
                'Vulnerabilities',
                'Mitigation Strategies',
                'Incident Response',
                'Forensic Analysis'
            ],
            'risk_factors': [
                'Zero-day Exploits',
                'Advanced Persistent Threats',
                'Supply Chain Attacks',
                'Social Engineering',
                'Insider Threats'
            ],
            'recommendations': [
                'Threat Hunting',
                'Vulnerability Management',
                'Security Awareness Training',
                'Incident Response Planning',
                'Continuous Monitoring'
            ],
            'executive_summary': {
                'description': 'Comprehensive cybersecurity threat intelligence analysis with interactive knowledge graph visualization.',
                'key_findings': {
                    'Threat Landscape': 'Increasingly sophisticated attack vectors',
                    'Response Time': 'Critical for minimizing damage',
                    'Prevention': 'Proactive measures reduce risk by 80%',
                    'Recovery': 'Proper planning reduces downtime by 60%'
                },
                'summary_stats': [
                    {'label': 'Threat Detection', 'value': '95%', 'description': 'Detection rate'},
                    {'label': 'Response Time', 'value': '<2hrs', 'description': 'Average response'},
                    {'label': 'Risk Reduction', 'value': '80%', 'description': 'With prevention'},
                    {'label': 'Recovery Time', 'value': '-60%', 'description': 'With planning'},
                    {'label': 'Cost Savings', 'value': '$2.5M', 'description': 'Annual savings'},
                    {'label': 'Compliance', 'value': '100%', 'description': 'Regulatory compliance'}
                ]
            }
        }
        
        report_path3 = generate_custom_enhanced_report(
            analysis_data=kg_data,
            title="Cybersecurity Threat Intelligence Analysis",
            subtitle="Interactive Knowledge Graph of Threat Landscape"
        )
        
        print(f"✅ Knowledge graph report generated: {report_path3}")
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 Demo Summary")
        print("=" * 50)
        print("✅ Successfully generated 3 enhanced reports:")
        print(f"   1. Pakistan Submarine Analysis: {report_path1}")
        print(f"   2. Strategic Intelligence Framework: {report_path2}")
        print(f"   3. Cybersecurity Threat Intelligence: {report_path3}")
        
        print("\n🎯 Key Features Demonstrated:")
        print("   • Interactive HTML reports with professional styling")
        print("   • Knowledge graph visualizations with network analysis")
        print("   • Professional data tables with risk assessments")
        print("   • Chart.js integration for dynamic visualizations")
        print("   • Responsive design for multiple screen sizes")
        print("   • Comprehensive strategic analysis templates")
        
        print("\n📝 Next Steps:")
        print("   1. Open the generated HTML files in a web browser")
        print("   2. Explore the interactive knowledge graphs")
        print("   3. Review the professional data tables")
        print("   4. Test the responsive design on different devices")
        print("   5. Use the templates for your own strategic analyses")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install networkx matplotlib seaborn jinja2")
        return False
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        return False

def main():
    """Main demo function"""
    
    success = demo_enhanced_report_generation()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("   Enhanced report generation is working correctly.")
    else:
        print("\n❌ Demo failed!")
        print("   Please check the error messages above.")

if __name__ == "__main__":
    main()
