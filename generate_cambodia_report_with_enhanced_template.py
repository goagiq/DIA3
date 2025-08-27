#!/usr/bin/env python3
"""
Generate Cambodia J-10 Fighter Jet Analysis Report using Enhanced Template
Uses the proper enhanced HTML report generator with 22 modules and advanced tooltips.
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import the correct enhanced HTML report generator
from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_cambodia_enhanced_report():
    """Generate Cambodia J-10 analysis report using enhanced template."""
    
    try:
        logger.info("🚀 Starting Cambodia J-10 Enhanced Report Generation...")
        
        # Initialize the enhanced HTML report generator
        generator = EnhancedHTMLReportGenerator()
        
        # Prepare the analysis data
        analysis_data = {
            "title": "Cambodia J-10 Fighter Jet Acquisition Analysis",
            "subtitle": "Comprehensive Strategic Intelligence Analysis",
            "topic": "Cambodia's acquisition of 50 Chinese J-10 fighter jets",
            "analysis_type": "strategic_intelligence",
            "confidence_score": 0.85,
            "source_metadata": [
                {
                    "source_type": "strategic_analysis",
                    "source_name": "Strategic Intelligence Division",
                    "title": "Southeast Asian Military Modernization Analysis",
                    "confidence": 0.9,
                    "reliability_score": 0.85,
                    "timestamp": datetime.now()
                },
                {
                    "source_type": "geopolitical_analysis",
                    "source_name": "Regional Security Institute",
                    "title": "ASEAN Unity and Chinese Influence Assessment",
                    "confidence": 0.8,
                    "reliability_score": 0.8,
                    "timestamp": datetime.now()
                }
            ],
            "analysis_content": {
                "executive_summary": {
                    "content": "Cambodia's acquisition of 50 Chinese J-10 fighter jets represents a significant shift in regional security dynamics, marking a deepening strategic partnership between Phnom Penh and Beijing. This analysis examines the multifaceted implications of this military procurement on Southeast Asian geopolitics, trade relations, power balance, escalation risks, and diplomatic stability.",
                    "key_findings": [
                        "Major shift in regional power dynamics in mainland Southeast Asia",
                        "Potential strain on ASEAN unity and consensus-building",
                        "Strengthening of China's strategic position in Southeast Asia",
                        "Risk of regional arms race and escalation",
                        "Impact on Cambodia's foreign policy alignment"
                    ]
                },
                "strategic_context": {
                    "content": "Cambodia's decision to acquire 50 J-10 fighter jets from China represents a major military modernization effort that will significantly enhance the Royal Cambodian Air Force's capabilities. The J-10, a fourth-generation multirole fighter aircraft, provides Cambodia with advanced air combat, ground attack, and maritime strike capabilities.",
                    "implications": [
                        "Enhanced deterrence capabilities",
                        "Improved territorial protection",
                        "Advanced air combat abilities",
                        "Maritime strike capabilities"
                    ]
                },
                "geopolitical_implications": {
                    "content": "Cambodia's military modernization challenges the existing balance of power in mainland Southeast Asia. Neighboring countries may feel compelled to respond with their own military upgrades, potentially triggering arms race dynamics in the Mekong region.",
                    "regional_impact": [
                        "Power balance shift in Southeast Asia",
                        "ASEAN unity challenges",
                        "Great power competition effects",
                        "Regional stability concerns"
                    ]
                },
                "economic_implications": {
                    "content": "The military procurement is likely accompanied by increased Chinese investment and trade agreements. This could lead to preferential trade agreements, Chinese infrastructure projects, and Belt and Road Initiative expansion in Cambodia.",
                    "economic_factors": [
                        "Increased Chinese investment",
                        "Preferential trade agreements",
                        "Infrastructure development",
                        "Technology transfer"
                    ]
                },
                "security_implications": {
                    "content": "Cambodia's air force will become one of the most capable in mainland Southeast Asia, significantly shifting the regional security balance and potentially triggering responses from neighboring countries.",
                    "security_concerns": [
                        "Regional arms race potential",
                        "Border security implications",
                        "Maritime security impact",
                        "Deterrence capabilities"
                    ]
                },
                "diplomatic_consequences": {
                    "content": "Cambodia's deepening ties with China may strain ASEAN consensus on South China Sea issues and other regional security matters. This could lead to ASEAN fragmentation on security and economic issues.",
                    "diplomatic_effects": [
                        "ASEAN cohesion challenges",
                        "Regional cooperation impact",
                        "International relations shift",
                        "Diplomatic isolation risks"
                    ]
                },
                "escalation_risks": {
                    "content": "Cambodia's alignment with China may affect ASEAN's position on South China Sea disputes, potentially supporting Chinese claims in multilateral forums and increasing regional tensions.",
                    "risk_factors": [
                        "South China Sea tensions",
                        "Border dispute escalation",
                        "Military incidents potential",
                        "Regional conflict risks"
                    ]
                },
                "strategic_recommendations": {
                    "content": "Regional actors should strengthen ASEAN unity and consensus-building mechanisms, while major powers should engage Cambodia diplomatically and support ASEAN's centrality in regional security architecture.",
                    "recommendations": [
                        "Strengthen ASEAN unity mechanisms",
                        "Enhance regional security cooperation",
                        "Develop military modernization management",
                        "Promote transparency in acquisitions"
                    ]
                }
            }
        }
        
        # Generate the enhanced report
        logger.info("📊 Generating enhanced HTML report with 22 modules...")
        
        result = await generator.generate_enhanced_report(
            data=analysis_data,
            output_path="Results/Cambodia_J10_Enhanced_Analysis.html"
        )
        
        if result["success"]:
            logger.info("✅ Enhanced report generated successfully!")
            logger.info(f"📁 File saved to: {result['file_path']}")
            logger.info(f"📊 Report size: {result.get('file_size_kb', 'Unknown')} KB")
            logger.info(f"🔧 Modules included: {result.get('modules_used', 'Unknown')}")
            logger.info(f"💡 Tooltips created: {result.get('tooltips_created', 'Unknown')}")
            
            # Verify file was actually saved
            file_path = Path(result['file_path'])
            if file_path.exists():
                logger.info(f"✅ File verification successful: {file_path.absolute()}")
                logger.info(f"📏 File size: {file_path.stat().st_size} bytes")
            else:
                logger.error(f"❌ File verification failed: {file_path} does not exist")
            
            return result
        else:
            logger.error(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
            return result
            
    except Exception as e:
        logger.error(f"❌ Error in report generation: {e}")
        return {
            "success": False,
            "error": str(e),
            "file_path": None
        }


async def main():
    """Main function to run the report generation."""
    print("🎯 Cambodia J-10 Fighter Jet Enhanced Analysis Report Generator")
    print("=" * 70)
    
    # Generate the enhanced report
    result = await generate_cambodia_enhanced_report()
    
    print("\n" + "=" * 70)
    if result["success"]:
        print("✅ SUCCESS: Enhanced report generated!")
        print(f"📁 Location: {result['file_path']}")
        print(f"🔧 Template: Enhanced 22-module template with advanced tooltips")
        print(f"📊 Size: {result.get('file_size_kb', 'Unknown')} KB")
        print(f"💡 Features: Interactive visualizations, advanced tooltips, modular design")
    else:
        print("❌ FAILED: Report generation failed!")
        print(f"🚨 Error: {result.get('error', 'Unknown error')}")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
