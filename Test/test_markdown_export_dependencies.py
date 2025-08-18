#!/usr/bin/env python3
"""
Test script for Markdown Export Dependencies

Tests if all required dependencies for markdown export are properly installed.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_dependencies():
    """Test if all required dependencies are available."""
    print("🧪 Testing Markdown Export Dependencies...")
    
    dependencies = {
        "markdown": "markdown",
        "markdownify": "markdownify", 
        "reportlab": "reportlab",
        "weasyprint": "weasyprint",
        "python-docx": "docx",
        "Pillow": "PIL",
        "requests": "requests",
        "loguru": "loguru",
        "tqdm": "tqdm"
    }
    
    missing_deps = []
    available_deps = []
    
    for dep_name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"✅ {dep_name} - Available")
            available_deps.append(dep_name)
        except ImportError as e:
            print(f"❌ {dep_name} - Missing: {e}")
            missing_deps.append(dep_name)
    
    print("\n📊 Summary:")
    print(f"✅ Available: {len(available_deps)}/{len(dependencies)}")
    print(f"❌ Missing: {len(missing_deps)}/{len(dependencies)}")
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please install missing dependencies using:")
        print("pip install -r requirements_markdown_export.txt")
        return False
    else:
        print("\n✅ All dependencies are available!")
        return True


def test_import_chain():
    """Test if the markdown export modules can be imported."""
    print("\n🧪 Testing Import Chain...")
    
    modules = [
        "src.core.export.markdown_export_service",
        "src.core.export.markdown_parser", 
        "src.core.export.pdf_exporter",
        "src.core.export.word_exporter",
        "src.core.export.mermaid_converter",
        "src.core.export.template_manager",
        "src.core.export.progress_tracker",
        "src.mcp_servers.markdown_export_mcp_tools",
        "src.api.markdown_export_routes"
    ]
    
    failed_imports = []
    successful_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} - Imported successfully")
            successful_imports.append(module)
        except ImportError as e:
            print(f"❌ {module} - Import failed: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"❌ {module} - Error: {e}")
            failed_imports.append(module)
    
    print("\n📊 Import Summary:")
    print(f"✅ Successful: {len(successful_imports)}/{len(modules)}")
    print(f"❌ Failed: {len(failed_imports)}/{len(modules)}")
    
    if failed_imports:
        print(f"\n❌ Failed imports: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True


def test_mcp_tools():
    """Test if MCP tools can be initialized."""
    print("\n🧪 Testing MCP Tools...")
    
    try:
        from src.mcp_servers.markdown_export_mcp_tools import MarkdownExportMCPTools, MARKDOWN_EXPORT_AVAILABLE
        
        if not MARKDOWN_EXPORT_AVAILABLE:
            print("❌ Markdown export service not available")
            return False
        
        mcp_tools = MarkdownExportMCPTools()
        tools = mcp_tools.get_tools()
        
        print(f"✅ MCP tools initialized successfully")
        print(f"📋 Available tools: {len(tools)}")
        
        for tool in tools:
            tool_name = tool["function"]["name"]
            print(f"  - {tool_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

def test_api_routes():
    """Test if API routes can be initialized."""
    print("\n🧪 Testing API Routes...")
    
    try:
        from src.api.markdown_export_routes import router, MARKDOWN_EXPORT_AVAILABLE
        
        if not MARKDOWN_EXPORT_AVAILABLE:
            print("❌ Markdown export service not available")
            return False
        
        print(f"✅ API routes initialized successfully")
        print(f"📋 Router prefix: {router.prefix}")
        
        # Check available endpoints
        routes = []
        for route in router.routes:
            if hasattr(route, 'path'):
                routes.append(f"{route.methods} {route.path}")
        
        print(f"📋 Available endpoints:")
        for route in routes:
            print(f"  - {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ API routes test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Markdown Export Dependency Test Suite")
    print("=" * 50)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n❌ Dependency test failed. Please install missing dependencies first.")
        return False
    
    # Test import chain
    import_ok = test_import_chain()
    
    if not import_ok:
        print("\n❌ Import chain test failed. There are issues with the module imports.")
        return False
    
    # Test MCP tools
    mcp_ok = test_mcp_tools()
    
    # Test API routes
    api_ok = test_api_routes()
    
    print("\n" + "=" * 50)
    print("📊 Final Test Results:")
    print(f"✅ Dependencies: {'PASS' if deps_ok else 'FAIL'}")
    print(f"✅ Import Chain: {'PASS' if import_ok else 'FAIL'}")
    print(f"✅ MCP Tools: {'PASS' if mcp_ok else 'FAIL'}")
    print(f"✅ API Routes: {'PASS' if api_ok else 'FAIL'}")
    
    if all([deps_ok, import_ok, mcp_ok, api_ok]):
        print("\n🎉 All tests passed! Markdown export functionality should work correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please fix the issues before using markdown export.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
