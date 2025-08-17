#!/usr/bin/env python3
"""
Cleanup script for Monte Carlo integration
Removes unused files and ensures clean integration
"""

import os
import shutil
import sys
from pathlib import Path

def cleanup_unused_files():
    """Remove unused files from Monte Carlo integration"""
    
    # Files to remove (if they exist and are not needed)
    files_to_remove = [
        # Old test files that are no longer needed
        "Test/test_monte_carlo_mcp_client_sample.py",
        "Test/test_monte_carlo_mcp_integration.py",
        "Test/test_phase1_monte_carlo.py",
        "Test/monte_carlo_phase1_retest.py",
        
        # Old result files
        "Test/monte_carlo_test_results_*.json",
        "Test/monte_carlo_mcp_client_results_*.json",
        "Test/monte_carlo_mcp_integration_results_*.json",
        
        # Duplicate test files
        "Test/test_phase7_verification.py",
        "Test/test_phase7_integration.py",
    ]
    
    # Directories to clean (remove empty files)
    dirs_to_clean = [
        "Test/__pycache__",
        "src/__pycache__",
        "src/core/__pycache__",
        "src/api/__pycache__",
        "src/mcp_servers/__pycache__",
    ]
    
    print("🧹 Starting cleanup of unused files...")
    
    # Remove files
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"⚠️ Could not remove {file_path}: {e}")
    
    # Clean directories
    for dir_path in dirs_to_clean:
        if os.path.exists(dir_path):
            try:
                # Remove __pycache__ files
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.pyc'):
                            os.remove(os.path.join(root, file))
                print(f"✅ Cleaned: {dir_path}")
            except Exception as e:
                print(f"⚠️ Could not clean {dir_path}: {e}")
    
    print("✅ Cleanup completed")

def verify_integration_files():
    """Verify that all necessary integration files exist"""
    
    required_files = [
        "src/core/monte_carlo/engine.py",
        "src/core/monte_carlo/config.py",
        "src/core/monte_carlo/distributions.py",
        "src/core/monte_carlo/correlations.py",
        "src/core/monte_carlo/scenarios.py",
        "src/core/monte_carlo/analysis.py",
        "src/core/agents/monte_carlo_agent.py",
        "src/api/routes/monte_carlo_routes.py",
        "src/mcp_servers/monte_carlo_mcp_tools.py",
        "src/mcp_servers/dynamic_tool_manager.py",
        "src/api/routes/mcp_tool_management.py",
        "Test/test_monte_carlo_mcp_integration_comprehensive.py",
        "MONTE_CARLO_IMPLEMENTATION_TRACKER.md",
    ]
    
    print("\n🔍 Verifying integration files...")
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Warning: {len(missing_files)} files are missing")
        return False
    else:
        print("\n✅ All integration files are present")
        return True

def main():
    """Main cleanup function"""
    print("🚀 Monte Carlo Integration Cleanup")
    print("=" * 50)
    
    # Clean up unused files
    cleanup_unused_files()
    
    # Verify integration files
    integration_ok = verify_integration_files()
    
    print("\n" + "=" * 50)
    if integration_ok:
        print("✅ Cleanup and verification completed successfully")
        print("🎯 Ready for Monte Carlo MCP integration testing")
    else:
        print("⚠️ Cleanup completed but some files are missing")
        print("🔧 Please check the missing files before proceeding")
    
    return integration_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
