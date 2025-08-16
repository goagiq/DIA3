#!/usr/bin/env python3
"""
Main entry point for the Sentiment Analysis Swarm system.
Provides both MCP server and FastAPI server functionality with comprehensive strategic assessment capabilities.
"""

# Suppress all deprecation warnings BEFORE any other imports
import warnings
import sys

# Set warnings filter to ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="uvicorn")
warnings.filterwarnings("ignore", category=UserWarning, module="websockets")

# Custom warning filter function
def ignore_all_warnings(message, category, filename, lineno, file=None, line=None):
    return

# Apply custom warning filter
warnings.showwarning = ignore_all_warnings

import os
import asyncio
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import configuration
from src.config.config import SentimentConfig

# Initialize configuration
config = SentimentConfig()

# Global flags for strategic assessment capabilities
STRATEGIC_ANALYTICS_AVAILABLE = True

def get_safe_port(host: str, default_port: int) -> int:
    """Get a safe port to use, checking if the default is available."""
    import socket
    
    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return True
            except OSError:
                return False
    
    if is_port_available(default_port):
        return default_port
    
    # Try next 10 ports
    for port in range(default_port + 1, default_port + 11):
        if is_port_available(port):
            print(f"⚠️ Port {default_port} is in use, using port {port}")
            return port
    
    # If all ports are busy, use default and let it fail
    print(f"⚠️ Warning: All ports {default_port}-{default_port+10} are in use")
    return default_port

def initialize_strategic_assessment() -> bool:
    """Initialize strategic assessment capabilities."""
    try:
        # Check if strategic analysis components are available
        from src.agents.art_of_war_deception_agent import ArtOfWarDeceptionAgent
        from src.agents.business_intelligence_agent import BusinessIntelligenceAgent
        from src.agents.market_data_agent import MarketDataManager
        
        print("✅ Strategic assessment components available")
        return True
    except ImportError as e:
        print(f"⚠️ Warning: Strategic assessment components not available: {e}")
        return False

def start_mcp_server():
    """Start the MCP server for integration."""
    try:
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        # Initialize the unified MCP server
        server = UnifiedMCPServer()
        print("✅ MCP server initialized")
        return server
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize MCP server: {e}")
        return None

def start_standalone_mcp_server(host: str = "localhost", port: int = 8000):
    """Start standalone MCP server for Strands integration."""
    try:
        from src.mcp_servers.standalone_mcp_server import start_standalone_mcp_server as start_server
        
        # Start the standalone MCP server
        server = start_server(host, port)
        print("✅ Standalone MCP server started")
        return server
    except Exception as e:
        print(f"⚠️ Warning: Could not start standalone MCP server: {e}")
        return None

def get_mcp_tools_info() -> Optional[List[Dict[str, Any]]]:
    """Get information about available MCP tools."""
    try:
        from src.mcp_servers.unified_mcp_server import UnifiedMCPServer
        
        server = UnifiedMCPServer()
        tools = server.get_tools_info()
        return tools
    except Exception as e:
        print(f"⚠️ Warning: Could not get MCP tools info: {e}")
        return None

def launch_streamlit_apps():
    """Launch Streamlit applications."""
    try:
        print("Launching Streamlit applications...")
        
        # Launch main UI
        main_ui_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "ui/main.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Launch landing page
        landing_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "ui/landing_page.py",
            "--server.port", "8502",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Streamlit applications launched")
        return main_ui_process, landing_process
        
    except Exception as e:
        print(f"⚠️ Error launching Streamlit apps: {e}")
        return None, None



if __name__ == "__main__":
    print("Starting Sentiment Analysis Swarm with Comprehensive Strategic Assessment & MCP Integration")
    print("=" * 80)
    
    # Initialize strategic assessment system
    strategic_ready = initialize_strategic_assessment()
    
    # Initialize performance optimizer and data collector
    print("Initializing performance monitoring system...")
    try:
        from src.core.performance_optimizer import get_performance_optimizer
        from src.core.performance_data_collector import get_performance_data_collector
        
        async def init_performance_system():
            # Initialize performance data collector
            collector = await get_performance_data_collector()
            await collector.start_collection()
            print("✅ Performance data collection started")
            
            # Initialize performance optimizer
            optimizer = await get_performance_optimizer()
            await optimizer.start_monitoring()
            print("✅ Performance monitoring started")
        
        # Start performance monitoring in background
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(init_performance_system())
        print("✅ Performance monitoring system initialized")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize performance monitoring system: {e}")
    
    # Initialize data ingestion service
    print("Initializing data ingestion service...")
    try:
        from src.core.data_ingestion_service import data_ingestion_service
        supported_languages = data_ingestion_service.get_supported_languages()
        print(f"✅ Data ingestion service initialized with {len(supported_languages)} supported languages:")
        for code, name in supported_languages.items():
            print(f"   - {code}: {name}")
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize data ingestion service: {e}")
    
    # Create MCP server for integration
    print("Creating MCP server for integration...")
    mcp_server = start_mcp_server()
    
    # Show available tools
    if mcp_server:
        tools = get_mcp_tools_info()
        if tools:
            print(f"🔧 MCP Tools: {len(tools)} tools available")
    
    # Get API configuration and ensure port is available
    api_host = config.api.host
    api_port = get_safe_port(api_host, config.api.port)
    
    print("\nStarting FastAPI server with Comprehensive Strategic Assessment & MCP integration...")
    
    # Integrate MCP server with FastAPI if available
    if mcp_server:
        try:
            # Create MCP app at root path - FastMCP handles routing internally
            mcp_app = mcp_server.get_http_app(path="")
            if mcp_app:
                # Mount the MCP app to the FastAPI app
                from src.api.main import app
                app.mount("/mcp", mcp_app)
                
                # Strategic analysis endpoints are already added in src/api/main.py
                
                print("✅ MCP server integrated with FastAPI at /mcp")
                print("✅ Strategic analysis endpoints added")
                print("   Note: Clients must use MCP protocol with 'initialize' method first")
                
                # Add a simple health check endpoint for MCP
                @app.get("/mcp-health")
                async def mcp_health_check():
                    return {
                        "status": "healthy", 
                        "service": "mcp_server", 
                        "endpoints": ["/mcp"],
                        "protocol": "MCP (Model Context Protocol)",
                        "strategic_assessment": strategic_ready,
                        "strategic_analytics": STRATEGIC_ANALYTICS_AVAILABLE,
                        "note": "Use 'initialize' method to establish session"
                    }
                    
        except Exception as e:
            print(f"⚠️ Warning: Could not integrate MCP server: {e}")
            # Add fallback MCP endpoint
            from src.api.main import app
            @app.get("/mcp")
            async def mcp_fallback():
                return {"error": "MCP server not available", "status": "unavailable"}
            
            @app.get("/mcp/")
            async def mcp_fallback_trailing():
                return {"error": "MCP server not available", "status": "unavailable"}
    
    # Start standalone MCP server for Strands integration
    print("\nStarting standalone MCP server for Strands integration...")
    standalone_mcp_server = None
    try:
        standalone_mcp_server = start_standalone_mcp_server(host="localhost", port=8000)
        if standalone_mcp_server and standalone_mcp_server.is_server_running():
            print("✅ Standalone MCP server started on port 8000")
            print("🔧 Available for Strands integration with Streamable HTTP transport")
        else:
            print("⚠️ Warning: Standalone MCP server failed to start")
    except Exception as e:
        print(f"⚠️ Warning: Could not start standalone MCP server: {e}")
    
    # Launch Streamlit applications
    print("\nLaunching Streamlit applications...")
    main_ui_process, landing_process = launch_streamlit_apps()
    
    # Start the FastAPI server
    print(f"\n🚀 Starting FastAPI server on {api_host}:{api_port}")
    print("=" * 80)
    print("📊 Available endpoints:")
    print("   - /health - System health check")
    print("   - /mcp-health - MCP server health check")
    print("   - /business/strategic-position-analysis - Business strategic position analysis")
    print("   - /business/intelligence-analysis - Business intelligence analysis")
    print("   - /strategic/assessment - Strategic assessment")
    print("   - /strategic/art-of-war-deception - Art of War deception analysis")
    print("   - /advanced-analytics/scenario - Scenario analysis")
    print("   - /integrate/market-data - Market data analysis")
    print("   - /mcp - MCP server integration")
    print("")
    print("🆕 Multi-Domain Strategic Analysis Endpoints:")
    print("   - /multi-domain/strategic-analysis - Generic multi-domain analysis")
    print("   - /multi-domain/business-strategic-analysis - Business domain analysis")
    print("   - /multi-domain/defense-strategic-analysis - Defense domain analysis")
    print("   - /multi-domain/intelligence-strategic-analysis - Intelligence domain analysis")
    print("   - /multi-domain/cybersecurity-strategic-analysis - Cybersecurity domain analysis")
    print("   - /multi-domain/geopolitical-strategic-analysis - Geopolitical domain analysis")
    print("   - /multi-domain/domains - Get supported domains")
    print("   - /multi-domain/domain-capabilities - Get domain capabilities")
    print("   - /multi-domain/health - Multi-domain service health check")
    print("")
    print("🔍 Pattern Analysis Endpoints:")
    print("   - /pattern-analysis/comprehensive - Comprehensive pattern analysis across all documents")
    print("   - /pattern-analysis/single-document - Single document pattern analysis")
    print("   - /pattern-analysis/health - Pattern analysis service health check")
    print("")
    print("🎭 Strategic Deception Monitoring Endpoints:")
    print("   - /strategic-deception/monitor - Single content deception monitoring")
    print("   - /strategic-deception/monitor-batch - Batch deception monitoring")
    print("   - /strategic-deception/dashboard - Deception dashboard data")
    print("   - /strategic-deception/health - Strategic deception service health check")
    print("   - /strategic-deception/defense/monitor - Defense domain monitoring")
    print("   - /strategic-deception/intelligence/monitor - Intelligence domain monitoring")
    print("   - /strategic-deception/business/monitor - Business domain monitoring")
    print("   - /strategic-deception/cybersecurity/monitor - Cybersecurity domain monitoring")
    print("   - /strategic-deception/geopolitical/monitor - Geopolitical domain monitoring")
    print("   - Test: .venv/Scripts/python.exe Test/test_strategic_deception_monitoring.py")
    print("")
    print("📈 Escalation Analysis Endpoints:")
    print("   - /escalation-analysis/analyze - General escalation analysis")
    print("   - /escalation-analysis/analyze-defense - Defense domain escalation analysis")
    print("   - /escalation-analysis/analyze-intelligence - Intelligence domain escalation analysis")
    print("   - /escalation-analysis/analyze-business - Business domain escalation analysis")
    print("   - /escalation-analysis/analyze-cybersecurity - Cybersecurity domain escalation analysis")
    print("   - /escalation-analysis/analyze-geopolitical - Geopolitical domain escalation analysis")
    print("   - /escalation-analysis/domains - Get supported domains")
    print("   - /escalation-analysis/historical-patterns - Get historical patterns")
    print("   - /escalation-analysis/capabilities - Get capabilities")
    print("   - /escalation-analysis/health - Escalation analysis service health check")
    print("   - Test: .venv/Scripts/python.exe Test/test_escalation_analysis.py")
    print("")
    print("🏛️ Classical Chinese HUMINT Analysis Endpoints:")
    print("   - /classical-chinese-humint/analyze - Classical Chinese HUMINT analysis")
    print("   - /classical-chinese-humint/strategic-deception - Strategic deception analysis")
    print("   - /classical-chinese-humint/health - Classical Chinese HUMINT service health check")
    print("   - Test: python Test/test_classical_chinese_humint_simple.py")
    print("=" * 80)
    
    # Import and start the FastAPI server
    try:
        import uvicorn
        from src.api.main import app
        
        # Strategic analysis endpoints are already added in src/api/main.py
        
        uvicorn.run(
            app,
            host=api_host,
            port=api_port,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        if main_ui_process:
            main_ui_process.terminate()
        if landing_process:
            landing_process.terminate()
        print("✅ Shutdown complete")
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        sys.exit(1)
