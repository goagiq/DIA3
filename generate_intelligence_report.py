#!/usr/bin/env python3
"""
Simple CLI for generating intelligence reports for any topic
Usage: python generate_intelligence_report.py "Your Topic Here"
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from generate_adaptive_intelligence_report import AdaptiveIntelligenceReportGenerator


async def generate_report(topic: str, context: str = "strategic", confidence: float = 0.95):
    """Generate an intelligence report for the given topic."""
    
    print(f"🚀 Generating Comprehensive Intelligence Report")
    print(f"📊 Topic: {topic}")
    print(f"🌍 Context: {context}")
    print(f"📈 Confidence: {confidence:.1%}")
    print("=" * 60)
    
    # Initialize the adaptive generator
    adaptive_generator = AdaptiveIntelligenceReportGenerator()
    
    # Generate the report
    result = await adaptive_generator.generate_adaptive_report(
        topic=topic,
        context=context,
        confidence_score=confidence
    )
    
    if result["success"]:
        print(f"✅ Report generated successfully!")
        print(f"📁 File: {result['output_path']}")
        print(f"📊 Modules: {result['result']['validation_results']['module_coverage']['total_generated']} generated")
        print(f"🎯 Confidence: {result['confidence_score']:.1%}")
        print(f"🔗 Open the HTML file in your browser to view the interactive report")
        
        print("\n🎯 Report Features:")
        print("   • Comprehensive Intelligence Pipeline integration")
        print("   • 22+ analytical modules with interactive visualizations")
        print("   • Vector database and knowledge graph insights")
        print("   • Cross-domain strategic analysis")
        print("   • Advanced tooltips and navigation")
        
        return result["output_path"]
    else:
        print(f"❌ Error generating report: {result['error']}")
        return None


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive intelligence reports for any strategic topic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_intelligence_report.py "Pakistan Submarine Acquisition"
  python generate_intelligence_report.py "China-Taiwan Relations" --context geopolitical
  python generate_intelligence_report.py "Space Militarization" --confidence 0.90
  python generate_intelligence_report.py "Cyber Warfare Capabilities" --context security
        """
    )
    
    parser.add_argument(
        "topic", 
        help="The strategic topic to analyze (e.g., 'Pakistan Submarine Acquisition')"
    )
    
    parser.add_argument(
        "--context", 
        default="strategic",
        choices=["strategic", "geopolitical", "economic", "security", "technological"],
        help="Analysis context (default: strategic)"
    )
    
    parser.add_argument(
        "--confidence", 
        type=float, 
        default=0.95,
        help="Confidence score (0.0-1.0, default: 0.95)"
    )
    
    args = parser.parse_args()
    
    # Validate confidence score
    if not 0.0 <= args.confidence <= 1.0:
        print("❌ Error: Confidence score must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Generate the report
    try:
        output_path = asyncio.run(generate_report(args.topic, args.context, args.confidence))
        if output_path:
            print(f"\n🎉 Report ready! Open: {output_path}")
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Report generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
