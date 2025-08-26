#!/usr/bin/env python3
"""
Test MCP Report Generation
Tests the enhanced generate_report MCP tool functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_servers.unified_mcp_server import UnifiedMCPServer


async def test_mcp_report_generation():
    """Test the MCP generate_report tool."""
    
    print("🧪 Testing MCP Report Generation Tool")
    print("=" * 50)
    
    # Create MCP server instance
    server = UnifiedMCPServer()
    
    # Test content
    test_content = """
    Cambodia's acquisition of 50 Chinese J-10 fighter jets represents a significant 
    military modernization and strategic realignment in Southeast Asia. This acquisition 
    has profound implications for regional security dynamics, trade relationships, 
    balance of power calculations, escalation risks, and diplomatic relations across 
    Southeast Asia and the broader Indo-Pacific region.
    """
    
    try:
        # Test the generate_report tool
        result = await server.generate_report(
            content=test_content,
            report_type="comprehensive",
            language="en",
            options={},
            topic="Cambodia J-10 Acquisition Test",
            use_case="Strategic Analysis",
            query="Test geopolitical implications",
            output_format="html",
            include_tooltips=True,
            include_visualizations=True,
            output_path=None
        )
        
        if result["success"]:
            print("✅ MCP generate_report tool test successful!")
            print(f"📄 Report saved to: {result['result']['saved_to']}")
            print(f"📊 Categories detected: "
                  f"{result['result']['categories_detected']}")
            print(f"📊 Categories used: "
                  f"{len(result['result']['categories_used'])}")
            print(f"💡 Tooltips created: "
                  f"{result['result']['tooltips_created']}")
            
            print("\n📋 Categories included:")
            for category in result['result']['categories_used']:
                print(f"   • {category.replace('_', ' ').title()}")
                
            return result
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"❌ MCP generate_report tool test failed: {error_msg}")
            return result
            
    except Exception as e:
        print(f"❌ Error testing MCP generate_report tool: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


async def main():
    """Main test function."""
    try:
        result = await test_mcp_report_generation()
        
        if result and result.get("success"):
            print("\n🎉 MCP tool test completed successfully!")
            print("📖 Report generated with enhanced features:")
            print("   • Interactive HTML with tooltips")
            print("   • Advanced category detection")
            print("   • Source tracking with DIA3- prefix")
            print("   • Professional visualization")
        else:
            print("\n❌ MCP tool test failed.")
            
    except Exception as e:
        print(f"❌ Error in main test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
