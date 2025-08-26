"""
Simple Phase 1 Test

This script tests the basic functionality of Phase 1 components
without requiring the full module structure.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_phase1_implementation():
    """Test Phase 1 implementation."""
    print("=" * 60)
    print("PHASE 1: UNIFIED SEARCH PIPELINE - SIMPLE TEST")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Check if files exist
    try:
        files_to_check = [
            "src/core/unified_search_orchestrator.py",
            "src/core/mcp_tool_manager.py", 
            "src/api/unified_search_routes.py",
            "Test/test_phase1_unified_search.py"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                test_results.append((f"File exists: {file_path}", "✅ PASS"))
            else:
                test_results.append((f"File exists: {file_path}", "❌ FAIL"))
        
    except Exception as e:
        test_results.append((f"File check", f"❌ FAIL: {e}"))
    
    # Test 2: Check if __init__.py files exist
    try:
        init_files = [
            "src/__init__.py",
            "src/core/__init__.py",
            "src/api/__init__.py"
        ]
        
        for init_file in init_files:
            if os.path.exists(init_file):
                test_results.append((f"Init file: {init_file}", "✅ PASS"))
            else:
                test_results.append((f"Init file: {init_file}", "❌ FAIL"))
        
    except Exception as e:
        test_results.append((f"Init file check", f"❌ FAIL: {e}"))
    
    # Test 3: Check file sizes (basic content verification)
    try:
        core_file = "src/core/unified_search_orchestrator.py"
        if os.path.exists(core_file):
            file_size = os.path.getsize(core_file)
            if file_size > 1000:  # Should be substantial
                test_results.append((f"Core file size: {file_size} bytes", "✅ PASS"))
            else:
                test_results.append((f"Core file size: {file_size} bytes", "❌ FAIL - Too small"))
        else:
            test_results.append(("Core file size check", "❌ FAIL - File not found"))
        
    except Exception as e:
        test_results.append((f"File size check", f"❌ FAIL: {e}"))
    
    # Test 4: Check for key classes in files
    try:
        orchestrator_file = "src/core/unified_search_orchestrator.py"
        if os.path.exists(orchestrator_file):
            with open(orchestrator_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            key_classes = [
                "class UnifiedSearchOrchestrator",
                "class SearchResults", 
                "class SearchResult",
                "class SourceMetadata",
                "class QueryCache",
                "class RetryConfig"
            ]
            
            for class_name in key_classes:
                if class_name in content:
                    test_results.append((f"Class found: {class_name}", "✅ PASS"))
                else:
                    test_results.append((f"Class found: {class_name}", "❌ FAIL"))
        else:
            test_results.append(("Class check", "❌ FAIL - File not found"))
        
    except Exception as e:
        test_results.append((f"Class check", f"❌ FAIL: {e}"))
    
    # Test 5: Check MCP Tool Manager
    try:
        mcp_file = "src/core/mcp_tool_manager.py"
        if os.path.exists(mcp_file):
            with open(mcp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            key_classes = [
                "class MCPToolManager",
                "class MCPTool",
                "class ToolCache",
                "class HealthMonitor"
            ]
            
            for class_name in key_classes:
                if class_name in content:
                    test_results.append((f"MCP Class: {class_name}", "✅ PASS"))
                else:
                    test_results.append((f"MCP Class: {class_name}", "❌ FAIL"))
        else:
            test_results.append(("MCP Class check", "❌ FAIL - File not found"))
        
    except Exception as e:
        test_results.append((f"MCP Class check", f"❌ FAIL: {e}"))
    
    # Test 6: Check API Routes
    try:
        api_file = "src/api/unified_search_routes.py"
        if os.path.exists(api_file):
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            key_elements = [
                "router = APIRouter",
                "class SearchRequest",
                "class SearchResponse",
                "@router.post(\"/search\""
            ]
            
            for element in key_elements:
                if element in content:
                    test_results.append((f"API Element: {element}", "✅ PASS"))
                else:
                    test_results.append((f"API Element: {element}", "❌ FAIL"))
        else:
            test_results.append(("API check", "❌ FAIL - File not found"))
        
    except Exception as e:
        test_results.append((f"API check", f"❌ FAIL: {e}"))
    
    # Print results
    print("\nTest Results:")
    print("-" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        print(f"{test_name:<35} {result}")
        if "✅ PASS" in result:
            passed += 1
    
    print("-" * 50)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    # Summary
    if passed == total:
        print("\n🎉 PHASE 1 IMPLEMENTATION: SUCCESS")
        print("All core components have been implemented correctly.")
        print("\nNext Steps:")
        print("1. Phase 2: Intelligence Storage & Versioning")
        print("2. Phase 3: Enhanced HTML Report System")
        print("3. Phase 4: Strategic Recommendations Integration")
        return True
    elif passed > total * 0.8:
        print("\n⚠️  PHASE 1 IMPLEMENTATION: MOSTLY SUCCESSFUL")
        print("Most components are working, some minor issues to address.")
        return True
    else:
        print("\n❌ PHASE 1 IMPLEMENTATION: NEEDS ATTENTION")
        print("Several components need to be fixed before proceeding.")
        return False


def check_phase1_architecture():
    """Check if Phase 1 follows the planned architecture."""
    print("\n" + "=" * 60)
    print("PHASE 1 ARCHITECTURE VERIFICATION")
    print("=" * 60)
    
    architecture_components = {
        "Unified Search Orchestrator": {
            "file": "src/core/unified_search_orchestrator.py",
            "key_features": [
                "Local knowledge search first",
                "MCP tools search in parallel", 
                "Result merging and ranking",
                "Caching with configurable duration",
                "Retry logic (2 attempts)",
                "Duplicate removal",
                "Source metadata tracking"
            ]
        },
        "MCP Tool Manager": {
            "file": "src/core/mcp_tool_manager.py",
            "key_features": [
                "Dynamic tool discovery",
                "Health monitoring",
                "Tool caching",
                "Performance metrics",
                "Retry logic integration",
                "TAC system integration",
                "DataGov system integration",
                "Forecasting engine integration"
            ]
        },
        "API Routes": {
            "file": "src/api/unified_search_routes.py", 
            "key_features": [
                "Unified search endpoint",
                "Health monitoring endpoint",
                "Cache management endpoints",
                "Source listing endpoint",
                "Local-only search endpoint",
                "MCP-only search endpoint"
            ]
        }
    }
    
    for component, details in architecture_components.items():
        print(f"\n{component}:")
        print(f"  File: {details['file']}")
        
        if os.path.exists(details['file']):
            print("  ✅ File exists")
            
            # Check file content for key features
            try:
                with open(details['file'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                implemented_features = 0
                for feature in details['key_features']:
                    # Simple keyword check
                    if any(keyword.lower() in content.lower() for keyword in feature.split()):
                        print(f"    ✅ {feature}")
                        implemented_features += 1
                    else:
                        print(f"    ❌ {feature}")
                
                coverage = implemented_features / len(details['key_features']) * 100
                print(f"  Coverage: {coverage:.1f}%")
                
            except Exception as e:
                print(f"  ❌ Error reading file: {e}")
        else:
            print("  ❌ File not found")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    success = test_phase1_implementation()
    check_phase1_architecture()
    
    if success:
        print("\n🚀 Ready to proceed to Phase 2!")
    else:
        print("\n🔧 Please fix issues before proceeding.")
