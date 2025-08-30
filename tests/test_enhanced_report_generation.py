#!/usr/bin/env python3
"""
Test Enhanced Report Generation

Tests the enhanced report generation functionality with:
- Enhanced tooltips with source references
- Detailed data explanations and strategic analysis
- Interactive visualizations
- Both comprehensive and strategic templates
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from loguru import logger

# Import enhanced report generator
try:
    from src.core.enhanced_report_generator import enhanced_report_generator
    ENHANCED_REPORT_AVAILABLE = True
except ImportError as e:
    logger.error(f"Enhanced report generator not available: {e}")
    ENHANCED_REPORT_AVAILABLE = False

# Import MCP tools
try:
    from src.mcp_servers.enhanced_report_mcp_tools import enhanced_report_mcp_tools
    MCP_TOOLS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Enhanced report MCP tools not available: {e}")
    MCP_TOOLS_AVAILABLE = False


async def test_enhanced_report_generation():
    """Test enhanced report generation functionality."""
    
    if not ENHANCED_REPORT_AVAILABLE:
        logger.error("❌ Enhanced report generator not available")
        return False
    
    logger.info("🎯 Testing Enhanced Report Generation")
    
    # Sample analysis data for Pakistan submarine acquisition
    analysis_data = {
        "executive_summary": "Pakistan's submarine acquisition program represents a strategic shift in South Asian naval capabilities with far-reaching geopolitical implications.",
        "strategic_summary": "Strategic analysis with geopolitical focus on regional power dynamics and security implications.",
        "metrics": {
            "geopolitical_impact": "HIGH",
            "trade_disruption_risk": "75%",
            "balance_of_power_shift": "+40%",
            "escalation_probability": "65%"
        },
        "data_sources": {
            "geopolitical_impact": "Regional Analysis Report 2025",
            "trade_disruption_risk": "Trade Flow Analysis",
            "balance_of_power_shift": "Naval Capability Assessment",
            "escalation_probability": "Risk Assessment Model"
        },
        "confidence": {
            "geopolitical_impact": "90%",
            "trade_disruption_risk": "85%",
            "balance_of_power_shift": "88%",
            "escalation_probability": "82%"
        },
        "geopolitical_impact": {
            "india_response": "HIGH",
            "china_partnership": "STRENGTHENING",
            "us_concerns": "MEDIUM",
            "gulf_states": "MEDIUM"
        },
        "risk_assessment": {
            "naval_arms_race": "85%",
            "maritime_incidents": "65%",
            "economic_sanctions": "45%",
            "proxy_conflicts": "35%"
        },
        "strategic_recommendations": [
            "Implement enhanced monitoring systems",
            "Develop strategic partnerships",
            "Strengthen risk mitigation measures",
            "Establish diplomatic communication channels"
        ]
    }
    
    try:
        # Test 1: Generate both enhanced reports
        logger.info("📊 Test 1: Generating both enhanced reports")
        
        result = await enhanced_report_generator.generate_enhanced_reports(
            topic="Pakistan Submarine Acquisition",
            analysis_data=analysis_data,
            report_title="Pakistan Submarine Acquisition: Enhanced Strategic Analysis",
            include_both_templates=True
        )
        
        if result.get("success") is False:
            logger.error(f"❌ Failed to generate enhanced reports: {result.get('error')}")
            return False
        
        logger.info(f"✅ Generated {len(result.get('reports', {}))} enhanced reports")
        
        # Check generated files
        for report_type, report_info in result.get("reports", {}).items():
            if report_info.get("success"):
                file_path = Path(report_info.get("file_path"))
                if file_path.exists():
                    logger.info(f"✅ {report_type} report generated: {file_path}")
                    logger.info(f"   File size: {report_info.get('file_size')} bytes")
                    logger.info(f"   Features: {', '.join(report_info.get('features', []))}")
                else:
                    logger.error(f"❌ {report_type} report file not found: {file_path}")
                    return False
            else:
                logger.error(f"❌ {report_type} report generation failed: {report_info.get('error')}")
                return False
        
        # Test 2: Test MCP tools if available
        if MCP_TOOLS_AVAILABLE:
            logger.info("📊 Test 2: Testing MCP tools")
            
            mcp_result = await enhanced_report_mcp_tools.generate_enhanced_html_report(
                topic="Pakistan Submarine Acquisition MCP Test",
                analysis_data=analysis_data,
                report_title="MCP Test Report",
                include_both_templates=True
            )
            
            if mcp_result.get("success"):
                logger.info(f"✅ MCP tools test successful: {mcp_result.get('reports_generated')} reports generated")
                
                for report_type, report_info in mcp_result.get("report_files", {}).items():
                    file_path = Path(report_info.get("file_path"))
                    if file_path.exists():
                        logger.info(f"✅ MCP {report_type} report: {file_path}")
                    else:
                        logger.error(f"❌ MCP {report_type} report file not found: {file_path}")
                        return False
            else:
                logger.error(f"❌ MCP tools test failed: {mcp_result.get('error')}")
                return False
        
        # Test 3: Verify enhanced tooltips and features
        logger.info("📊 Test 3: Verifying enhanced features")
        
        # Read one of the generated reports to verify enhanced features
        comprehensive_report_path = None
        for report_type, report_info in result.get("reports", {}).items():
            if "comprehensive" in report_type.lower():
                comprehensive_report_path = report_info.get("file_path")
                break
        
        if comprehensive_report_path:
            with open(comprehensive_report_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
                
                # Check for enhanced tooltip features
                if 'enhanced-tooltip' in report_content:
                    logger.info("✅ Enhanced tooltips found in report")
                else:
                    logger.warning("⚠️ Enhanced tooltips not found in report")
                
                if 'showEnhancedTooltip' in report_content:
                    logger.info("✅ Enhanced tooltip JavaScript functions found")
                else:
                    logger.warning("⚠️ Enhanced tooltip JavaScript functions not found")
                
                if 'Chart.js' in report_content:
                    logger.info("✅ Chart.js integration found")
                else:
                    logger.warning("⚠️ Chart.js integration not found")
                
                if 'strategic analysis' in report_content.lower():
                    logger.info("✅ Strategic analysis content found")
                else:
                    logger.warning("⚠️ Strategic analysis content not found")
        
        logger.info("🎉 All enhanced report generation tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during enhanced report generation test: {e}")
        return False


async def test_specific_template_generation():
    """Test specific template generation."""
    
    if not ENHANCED_REPORT_AVAILABLE:
        logger.error("❌ Enhanced report generator not available")
        return False
    
    logger.info("🎯 Testing Specific Template Generation")
    
    # Sample data for strategic analysis
    strategic_data = {
        "strategic_summary": "Strategic analysis with geopolitical focus on regional power dynamics.",
        "geopolitical_impact": {
            "india_response": "HIGH",
            "china_partnership": "STRENGTHENING",
            "us_concerns": "MEDIUM"
        },
        "risk_assessment": {
            "naval_arms_race": "85%",
            "maritime_incidents": "65%"
        },
        "strategic_recommendations": [
            "Implement enhanced monitoring systems",
            "Develop strategic partnerships"
        ]
    }
    
    try:
        # Test strategic template only
        logger.info("📊 Testing strategic template generation")
        
        result = await enhanced_report_generator._generate_strategic_enhanced_report(
            topic="Strategic Analysis Test",
            analysis_data=strategic_data,
            report_title="Strategic Analysis Test Report",
            filename=f"strategic_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        )
        
        if result.get("success"):
            file_path = Path(result.get("file_path"))
            if file_path.exists():
                logger.info(f"✅ Strategic template generated: {file_path}")
                logger.info(f"   File size: {result.get('file_size')} bytes")
                logger.info(f"   Features: {', '.join(result.get('features', []))}")
                return True
            else:
                logger.error(f"❌ Strategic template file not found: {file_path}")
                return False
        else:
            logger.error(f"❌ Strategic template generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during strategic template test: {e}")
        return False


async def main():
    """Main test function."""
    logger.info("🚀 Starting Enhanced Report Generation Tests")
    
    # Test 1: Full enhanced report generation
    success1 = await test_enhanced_report_generation()
    
    # Test 2: Specific template generation
    success2 = await test_specific_template_generation()
    
    if success1 and success2:
        logger.info("🎉 All tests passed successfully!")
        return True
    else:
        logger.error("❌ Some tests failed")
        return False


if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
