#!/usr/bin/env python3
"""
Test script to verify content verification system and module updates.
Tests that all specified modules have the required content sections and no generic labels.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator


async def test_content_verification():
    """Test the content verification system."""
    print("🧪 Testing Content Verification System")
    print("=" * 50)
    
    # Initialize the generator
    generator = EnhancedHTMLReportGenerator()
    
    # Test data
    test_data = {
        "topic": "Test Strategic Initiative",
        "analysis_type": "strategic_intelligence",
        "source_metadata": [{"source_type": "test", "source_name": "Test Source"}],
        "knowledge_graph_data": {"nodes": [], "edges": []},
        "vector_insights": {"patterns": [], "trends": []}
    }
    
    # Generate a test report
    print("📊 Generating test report...")
    output_path = "Results/test_content_verification_report.html"
    
    try:
        result = await generator.generate_enhanced_report(test_data, output_path)
        
        if result.get("success"):
            print("✅ Report generated successfully")
            
            # Read the generated HTML content
            with open(output_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Run content verification
            print("\n🔍 Running content verification...")
            content_verification = generator._validate_content_requirements(html_content)
            
            # Display results
            print(f"\n📋 Content Verification Results:")
            print(f"   All requirements met: {content_verification.get('all_requirements_met', False)}")
            print(f"   All modules valid: {content_verification.get('all_modules_valid', False)}")
            print(f"   No generic labels: {content_verification.get('no_generic_labels', False)}")
            print(f"   Summary: {content_verification.get('summary', 'N/A')}")
            
            # Check individual modules
            print(f"\n📊 Module Content Validation:")
            module_validation = content_verification.get('module_content_validation', {})
            for module_name, validation in module_validation.items():
                status = "✅" if validation.get('all_sections_present', False) else "❌"
                print(f"   {status} {module_name}")
                
                # Show missing sections if any
                sections_present = validation.get('sections_present', {})
                missing_sections = [section for section, present in sections_present.items() if not present]
                if missing_sections:
                    print(f"      Missing: {', '.join(missing_sections)}")
            
            # Check for generic labels
            generic_labels = content_verification.get('generic_labels_found', [])
            if generic_labels:
                print(f"\n⚠️  Generic labels found: {', '.join(generic_labels)}")
            else:
                print(f"\n✅ No generic labels found")
            
            # Check for generic chart labels
            generic_chart_labels = content_verification.get('generic_chart_labels_found', [])
            if generic_chart_labels:
                print(f"\n⚠️  Generic chart labels found: {', '.join(generic_chart_labels)}")
                print(f"   This indicates incorrect or generic statistical data is being used")
            else:
                print(f"\n✅ No generic chart labels found")
            
            # Check chart label validation
            no_generic_chart_labels = content_verification.get('no_generic_chart_labels', False)
            if no_generic_chart_labels:
                print(f"✅ Chart labels are dynamic and specific")
            else:
                print(f"❌ Chart labels are generic and indicate incorrect data")
            
            # Check module count
            print(f"\n📈 Module Count:")
            print(f"   Total modules configured: {len(generator.complete_modules)}")
            print(f"   Modules requiring sections: {len(content_verification.get('modules_requiring_sections', []))}")
            
            # Verify Interactive Visualizations is removed
            if "Interactive Visualizations" in generator.complete_modules:
                print(f"\n❌ Interactive Visualizations module still present")
            else:
                print(f"\n✅ Interactive Visualizations module successfully removed")
            
        else:
            print(f"❌ Report generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


async def test_adaptive_report_generation():
    """Test adaptive report generation for different topics."""
    print("\n🔄 Testing Adaptive Report Generation")
    print("=" * 50)
    
    from generate_adaptive_intelligence_report import AdaptiveIntelligenceReportGenerator
    
    generator = AdaptiveIntelligenceReportGenerator()
    
    test_topics = [
        "Cybersecurity Threat Analysis",
        "Space Technology Development", 
        "Climate Change Impact Assessment",
        "Digital Transformation Strategy"
    ]
    
    for topic in test_topics:
        print(f"\n📊 Testing topic: {topic}")
        try:
            result = await generator.generate_adaptive_report(topic)
            if result.get("success"):
                print(f"   ✅ Successfully generated report for '{topic}'")
                
                # Check if the report has the required content sections
                output_path = result.get("output_path", "")
                if output_path and Path(output_path).exists():
                    with open(output_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    if "Visualization Insight" in html_content and "Key Takeaway" in html_content:
                        print(f"   ✅ Required content sections present")
                    else:
                        print(f"   ❌ Missing required content sections")
                else:
                    print(f"   ❌ Could not read generated report file")
                    
            else:
                print(f"   ❌ Failed to generate report for '{topic}'")
                
        except Exception as e:
            print(f"   ❌ Error generating report for '{topic}': {e}")


async def main():
    """Main test function."""
    print("🚀 Starting Content Verification Tests")
    print("=" * 60)
    
    # Test content verification
    await test_content_verification()
    
    # Test adaptive report generation
    await test_adaptive_report_generation()
    
    print("\n🎉 Content verification tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
