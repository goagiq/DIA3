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

def get_safe_port(host: str, default_port: int, reserved_ports: List[int] = None) -> int:
    """Get a safe port to use, checking if the default is available and avoiding reserved ports."""
    import socket
    
    if reserved_ports is None:
        reserved_ports = [8000]  # Reserve port 8000 for standalone MCP server
    
    def is_port_available(port):
        if port in reserved_ports:
            return False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return True
            except OSError:
                return False
    
    if is_port_available(default_port):
        return default_port
    
    # Try next 10 ports, avoiding reserved ports
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

def initialize_multi_domain_strategic_engine():
    """Initialize the multi-domain strategic analysis engine."""
    try:
        from src.core.multi_domain_strategic_engine import MultiDomainStrategicEngine
        
        # Initialize the strategic engine
        engine = MultiDomainStrategicEngine()
        print("✅ Multi-domain strategic engine initialized")
        return engine
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize strategic engine: {e}")
        return None

def initialize_enhanced_strategic_analysis_engine():
    """Initialize the enhanced strategic analysis engine."""
    try:
        from src.core.enhanced_strategic_analysis_engine import enhanced_strategic_analysis_engine
        
        # The engine is already initialized as a global instance
        print("✅ Enhanced strategic analysis engine initialized")
        return enhanced_strategic_analysis_engine
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize enhanced strategic analysis engine: {e}")
        return None

def initialize_language_capabilities_engine():
    """Initialize the language capabilities engine."""
    try:
        from src.core.language_capabilities_engine import language_capabilities_engine
        
        # Initialize the language capabilities engine
        print("✅ Language capabilities engine initialized")
        return language_capabilities_engine
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize language capabilities engine: {e}")
        return None

def initialize_force_projection_engine():
    """Initialize the force projection engine."""
    try:
        from src.core.force_projection_engine import ForceProjectionEngine
        
        # Initialize the force projection engine
        engine = ForceProjectionEngine()
        print("✅ Force projection engine initialized")
        return engine
    except Exception as e:
        print(f"⚠️ Warning: Could not initialize force projection engine: {e}")
        return None

def start_standalone_mcp_server(host: str = "localhost", port: int = 8000):
    """Start standalone MCP server for Strands integration."""
    try:
        from src.mcp_servers.standalone_mcp_server import start_standalone_mcp_server as start_server
        import socket
        
        # First, try to use the specified port (8000 for MCP)
        try:
            # Test if port is available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.close()
            
            # Port is available, start the server
            server = start_server(host, port)
            if server and server.is_server_running():
                print(f"✅ Standalone MCP server started on port {port}")
                return server
            else:
                print(f"⚠️ Warning: MCP server failed to start on port {port}")
                
        except OSError:
            print(f"⚠️ Port {port} is in use, trying alternative ports...")
        
        # If the preferred port is not available, try alternative ports
        # but avoid the main API server port range (8003-8013)
        alternative_ports = [8001, 8002, 8014, 8015, 8016, 8017, 8018, 8019, 8020]
        
        for alt_port in alternative_ports:
            try:
                # Test if port is available
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((host, alt_port))
                    s.close()
                
                # Port is available, start the server
                server = start_server(host, alt_port)
                if server and server.is_server_running():
                    print(f"✅ Standalone MCP server started on port {alt_port} (original port {port} was in use)")
                    return server
                else:
                    print(f"⚠️ Warning: MCP server failed to start on port {alt_port}")
                    continue
                    
            except OSError:
                # Port is in use, try next port
                continue
            except Exception as e:
                print(f"⚠️ Warning: Error starting MCP server on port {alt_port}: {e}")
                continue
        
        print(f"⚠️ Warning: Could not find available port for MCP server")
        return None
        
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
    
    # Initialize multi-domain strategic engine
    strategic_engine = initialize_multi_domain_strategic_engine()
    
    # Initialize enhanced strategic analysis engine
    enhanced_strategic_engine = initialize_enhanced_strategic_analysis_engine()
    
    # Initialize language capabilities engine
    language_capabilities_engine = initialize_language_capabilities_engine()
    
    # Initialize force projection engine
    force_projection_engine = initialize_force_projection_engine()
    
    # Initialize Phase 1 ML/DL/RL Forecasting Components
    print("Initializing Phase 1 ML/DL/RL Forecasting Components...")
    try:
        from src.core.reinforcement_learning import ReinforcementLearningEngine
        from src.core.advanced_ml.enhanced_time_series_models import EnhancedTimeSeriesModels
        from src.core.advanced_analytics.enhanced_causal_inference import EnhancedCausalInferenceEngine
        from src.core.domain_specific.dod_threat_models import DoDThreatAssessmentModels
        from src.core.domain_specific.intelligence_analysis_models import IntelligenceAnalysisModels
        
        rl_engine = ReinforcementLearningEngine()
        time_series_models = EnhancedTimeSeriesModels()
        causal_inference_engine = EnhancedCausalInferenceEngine()
        dod_threat_models = DoDThreatAssessmentModels()
        intelligence_models = IntelligenceAnalysisModels()
        
        print("✅ Phase 1 ML/DL/RL Forecasting Components initialized")
    except ImportError as e:
        print(f"⚠️ Warning: Phase 1 ML/DL/RL Forecasting Components not available: {e}")
    except Exception as e:
        print(f"⚠️ Warning: Error initializing Phase 1 ML/DL/RL Forecasting Components: {e}")
    
    # Initialize Phase 3 Advanced Forecasting & Prediction Components
    print("Initializing Phase 3 Advanced Forecasting & Prediction Components...")
    try:
        from src.core.advanced_ml.ensemble_forecasting_system import EnsembleForecastingSystem
        from src.core.scenario_analysis.enhanced_scenario_predictor import EnhancedScenarioPredictor
        from src.core.streaming.intelligence_data_adapter import IntelligenceDataAdapter
        
        ensemble_forecasting_system = EnsembleForecastingSystem()
        enhanced_scenario_predictor = EnhancedScenarioPredictor()
        intelligence_data_adapter = IntelligenceDataAdapter()
        
        print("✅ Phase 3 Advanced Forecasting & Prediction Components initialized")
    except ImportError as e:
        print(f"⚠️ Warning: Phase 3 Advanced Forecasting & Prediction Components not available: {e}")
    except Exception as e:
        print(f"⚠️ Warning: Error initializing Phase 3 Advanced Forecasting & Prediction Components: {e}")
    
    # Initialize Enhanced PDF Generation Service
    print("Initializing Enhanced PDF Generation Service...")
    try:
        from src.core.enhanced_pdf_generation_service import enhanced_pdf_service
        
        print("✅ Enhanced PDF Generation Service initialized")
    except ImportError as e:
        print(f"⚠️ Warning: Enhanced PDF Generation Service not available: {e}")
    except Exception as e:
        print(f"⚠️ Warning: Error initializing Enhanced PDF Generation Service: {e}")
    
    # Initialize Phase 4 Multi-Domain Integration Components
    print("Initializing Phase 4 Multi-Domain Integration Components...")
    try:
        from src.core.multi_domain.dod_domain_integration import DoDDomainIntegration
        from src.core.multi_domain.intelligence_community_integration import IntelligenceCommunityIntegration
        from src.core.federated_learning.federated_learning_engine import FederatedLearningEngine
        
        dod_domain_integration = DoDDomainIntegration()
        intelligence_community_integration = IntelligenceCommunityIntegration()
        federated_learning_engine = FederatedLearningEngine()
        
        print("✅ Phase 4 Multi-Domain Integration Components initialized")
    except ImportError as e:
        print(f"⚠️ Warning: Phase 4 Multi-Domain Integration Components not available: {e}")
    except Exception as e:
        print(f"⚠️ Warning: Error initializing Phase 4 Multi-Domain Integration Components: {e}")
    
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
    api_port = get_safe_port(api_host, config.api.port, reserved_ports=[8000])
    
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
    print("🎯 Enhanced Strategic Analysis Endpoints:")
    print("   - /enhanced-strategic/analyze - General strategic analysis")
    print("   - /enhanced-strategic/analyze-defense - Defense domain analysis")
    print("   - /enhanced-strategic/analyze-intelligence - Intelligence domain analysis")
    print("   - /enhanced-strategic/analyze-business - Business domain analysis")
    print("   - /enhanced-strategic/analyze-cybersecurity - Cybersecurity domain analysis")
    print("   - /enhanced-strategic/analyze-geopolitical - Geopolitical domain analysis")
    print("   - /enhanced-strategic/analyze-financial - Financial domain analysis")
    print("   - /enhanced-strategic/analyze-healthcare - Healthcare domain analysis")
    print("   - /enhanced-strategic/analyze-energy - Energy domain analysis")
    print("   - /enhanced-strategic/analyze-transportation - Transportation domain analysis")
    print("   - /enhanced-strategic/analyze-critical-infrastructure - Critical infrastructure domain analysis")
    print("   - /enhanced-strategic/analyze-batch - Batch strategic analysis")
    print("   - /enhanced-strategic/domains - Get supported domains")
    print("   - /enhanced-strategic/domain-capabilities/{domain} - Get domain capabilities")
    print("   - /enhanced-strategic/analysis-history - Get analysis history")
    print("   - /enhanced-strategic/summary - Get service summary")
    print("   - /enhanced-strategic/health - Enhanced strategic analysis health check")
    print("   - Test: .venv/Scripts/python.exe Test/test_enhanced_strategic_analysis.py")
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
    print("🔍 Enhanced Deception Detection Endpoints:")
    print("   - /enhanced-deception-detection/analyze - Comprehensive deception analysis")
    print("   - /enhanced-deception-detection/analyze-defense - Defense domain analysis")
    print("   - /enhanced-deception-detection/analyze-intelligence - Intelligence domain analysis")
    print("   - /enhanced-deception-detection/analyze-business - Business domain analysis")
    print("   - /enhanced-deception-detection/analyze-cybersecurity - Cybersecurity domain analysis")
    print("   - /enhanced-deception-detection/analyze-geopolitical - Geopolitical domain analysis")
    print("   - /enhanced-deception-detection/analyze-batch - Batch deception analysis")
    print("   - /enhanced-deception-detection/domains - Get supported domains")
    print("   - /enhanced-deception-detection/domain-capabilities/{domain} - Get domain capabilities")
    print("   - /enhanced-deception-detection/art-of-war-techniques - Get Art of War techniques")
    print("   - /enhanced-deception-detection/cultural-patterns - Get cultural patterns")
    print("   - /enhanced-deception-detection/health - Enhanced deception detection health check")
    print("   - /enhanced-deception-detection/summary - Get service summary")
    print("   - Test: .venv/Scripts/python.exe Test/test_enhanced_deception_detection.py")
    print("")
    print("🔍 Threat Assessment Warning Indicators Endpoints:")
    print("   - /threat-assessment/analyze - Comprehensive threat assessment analysis")
    print("   - /threat-assessment/analyze-defense - Defense domain threat analysis")
    print("   - /threat-assessment/analyze-intelligence - Intelligence domain threat analysis")
    print("   - /threat-assessment/analyze-business - Business domain threat analysis")
    print("   - /threat-assessment/analyze-cybersecurity - Cybersecurity domain threat analysis")
    print("   - /threat-assessment/analyze-geopolitical - Geopolitical domain threat analysis")
    print("   - /threat-assessment/analyze-financial - Financial domain threat analysis")
    print("   - /threat-assessment/analyze-healthcare - Healthcare domain threat analysis")
    print("   - /threat-assessment/analyze-energy - Energy domain threat analysis")
    print("   - /threat-assessment/analyze-transportation - Transportation domain threat analysis")
    print("   - /threat-assessment/analyze-critical-infrastructure - Critical infrastructure threat analysis")
    print("   - /threat-assessment/analyze-batch - Batch threat assessment analysis")
    print("   - /threat-assessment/summary - Get threat assessment summary")
    print("   - /threat-assessment/domains - Get supported domains")
    print("   - /threat-assessment/capabilities - Get threat assessment capabilities")
    print("   - /threat-assessment/health - Threat assessment service health check")
    print("   - Test: .venv/Scripts/python.exe Test/test_threat_assessment.py")
    print("")
    print("🤖 Phase 1-4 ML/DL/RL Forecasting Endpoints:")
    print("   - /ml-forecasting/health - ML forecasting service health check")
    print("   - /ml-forecasting/time-series/forecast - Time series forecasting")
    print("   - /ml-forecasting/reinforcement-learning/optimize - RL decision optimization")
    print("   - /ml-forecasting/causal-inference/analyze - Causal inference analysis")
    print("   - /ml-forecasting/domain-specific/defense/analyze - Defense domain analysis")
    print("   - /ml-forecasting/domain-specific/intelligence/analyze - Intelligence domain analysis")
    print("   - /ml-forecasting/war-capability/analyze - War capability analysis")
    print("   - /ml-forecasting/interactive-levers/adjust - Interactive lever adjustment")
    print("   - /ml-forecasting/interactive-levers/status - Lever status")
    print("   - /ml-forecasting/phase3/ensemble-forecast - Phase 3: Ensemble forecasting")
    print("   - /ml-forecasting/phase3/scenario-prediction - Phase 3: Scenario prediction")
    print("   - /ml-forecasting/phase3/intelligence-stream/connect - Phase 3: Intelligence stream connection")
    print("   - /ml-forecasting/phase3/intelligence-stream/process - Phase 3: Intelligence data processing")
    print("   - /ml-forecasting/phase3/intelligence-stream/status - Phase 3: Intelligence stream status")
    print("   - /ml-forecasting/phase3/ensemble-status - Phase 3: Ensemble system status")
    print("   - /ml-forecasting/phase3/scenario-predictor-status - Phase 3: Scenario predictor status")
    print("   - /ml-forecasting/phase4/dod-integration - Phase 4: DoD domain integration")
    print("   - /ml-forecasting/phase4/intelligence-community-integration - Phase 4: Intelligence community integration")
    print("   - /ml-forecasting/phase4/federated-learning - Phase 4: Federated learning operations")
    print("   - /ml-forecasting/phase4/dod-status - Phase 4: DoD integration status")
    print("   - /ml-forecasting/phase4/intelligence-community-status - Phase 4: Intelligence community status")
    print("   - /ml-forecasting/phase4/federated-learning-status - Phase 4: Federated learning status")
    print("   - /ml-forecasting/models - Get available models")
    print("   - /ml-forecasting/summary - Get service summary")
    print("   - Test: .venv/Scripts/python.exe Test/test_ml_forecasting.py")
    print("   - Test: .venv/Scripts/python.exe Test/test_phase4_multi_domain_integration.py")
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
    print("")
    print("🌍 Language Capabilities Strategic Advantages Endpoints:")
    print("   - /language-capabilities/analyze - General language capabilities analysis")
    print("   - /language-capabilities/defense/analyze - Defense domain language capabilities")
    print("   - /language-capabilities/intelligence/analyze - Intelligence domain language capabilities")
    print("   - /language-capabilities/business/analyze - Business domain language capabilities")
    print("   - /language-capabilities/cybersecurity/analyze - Cybersecurity domain language capabilities")
    print("   - /language-capabilities/batch/analyze - Batch language capabilities analysis")
    print("   - /language-capabilities/capabilities - Get all capabilities summary")
    print("   - /language-capabilities/capabilities/{language} - Get language-specific capabilities")
    print("   - /language-capabilities/advantages/{domain} - Get domain-specific advantages")
    print("   - /language-capabilities/supported-languages - Get supported languages")
    print("   - /language-capabilities/supported-domains - Get supported domains")
    print("   - /language-capabilities/capability-types - Get capability types")
    print("   - /language-capabilities/health - Language capabilities service health check")
    print("   - Test: .venv/Scripts/python.exe Test/test_language_capabilities.py")
    print("")
    print("🚀 Phase 6 Advanced Forecasting & Reinforcement Learning Endpoints:")
    print("   - /api/v1/advanced-forecasting/health - Advanced forecasting service health check")
    print("   - /api/v1/advanced-forecasting/ensemble-forecast - Ensemble forecasting")
    print("   - /api/v1/advanced-forecasting/scenario-analysis - Scenario analysis")
    print("   - /api/v1/advanced-forecasting/real-time-forecast - Real-time forecasting")
    print("   - /api/v1/advanced-forecasting/optimize-ensemble - Ensemble optimization")
    print("   - /api/v1/reinforcement-learning/health - Reinforcement learning service health check")
    print("   - /api/v1/reinforcement-learning/train-agent - RL agent training")
    print("   - /api/v1/reinforcement-learning/make-decision - RL decision making")
    print("   - /api/v1/reinforcement-learning/multi-agent-coordination - Multi-agent coordination")
    print("   - /api/v1/reinforcement-learning/optimize-weights - RL weight optimization")
    print("   - Test: .venv/Scripts/python.exe Test/test_phase6_advanced_forecasting.py")
    print("")
    print("🎲 Phase 1 Monte Carlo Simulation Endpoints:")
    print("   - /api/v1/monte-carlo/health - Monte Carlo service health check")
    print("   - /api/v1/monte-carlo/simulate - Run Monte Carlo simulation")
    print("   - /api/v1/monte-carlo/scenario/{type} - Run scenario simulation")
    print("   - /api/v1/monte-carlo/custom - Run custom simulation")
    print("   - /api/v1/monte-carlo/time-series - Run time series simulation")
    print("   - /api/v1/monte-carlo/analyze - Analyze simulation results")
    print("   - /api/v1/monte-carlo/scenarios - List available scenarios")
    print("   - /api/v1/monte-carlo/scenarios/{type} - Get scenario information")
    print("   - /api/v1/monte-carlo/distributions - List available distributions")
    print("   - /api/v1/monte-carlo/distributions/{type} - Get distribution information")
    print("   - /api/v1/monte-carlo/correlation-matrix - Generate correlation matrix")
    print("   - /api/v1/monte-carlo/estimate-correlation - Estimate correlation from samples")
    print("   - /api/v1/monte-carlo/status - Get engine status")
    print("   - /api/v1/monte-carlo/validate-configuration - Validate configuration")
    print("   - Test: .venv/Scripts/python.exe Test/test_phase1_monte_carlo.py")
    print("")
    print("🌐 Multi-Domain Monte Carlo Simulation Endpoints:")
    print("   - /api/v1/multi-domain-monte-carlo/health - Multi-domain Monte Carlo health check")
    print("   - /api/v1/multi-domain-monte-carlo/scenarios - Get available scenarios")
    print("   - /api/v1/multi-domain-monte-carlo/performance - Get performance summary")
    print("   - /api/v1/multi-domain-monte-carlo/simulate/defense - Defense domain simulation")
    print("   - /api/v1/multi-domain-monte-carlo/simulate/business - Business domain simulation")
    print("   - /api/v1/multi-domain-monte-carlo/simulate/financial - Financial domain simulation")
    print("   - /api/v1/multi-domain-monte-carlo/simulate/cybersecurity - Cybersecurity domain simulation")
    print("   - /api/v1/multi-domain-monte-carlo/simulate/custom - Custom domain simulation")
    print("   - /api/v1/multi-domain-monte-carlo/simulate/batch - Batch simulations")
    print("   - /api/v1/multi-domain-monte-carlo/simulation/{id} - Get simulation result")
    print("   - /api/v1/multi-domain-monte-carlo/report - Generate simulation report")
    print("   - Test: .venv/Scripts/python.exe Test/test_multi_domain_monte_carlo.py")
    print("")
    print("🎯 Phase 7 Testing & Deployment Endpoints:")
    print("   - /mcp-health - MCP server health check (standalone)")
    print("   - /mcp - MCP server integration (integrated)")
    print("   - Standalone MCP Server: http://localhost:8000")
    print("   - Streamable HTTP MCP Client: Available for Strands integration")
    print("   - Test: .venv/Scripts/python.exe Test/test_phase7_integration.py")
    print("   - Demo: .venv/Scripts/python.exe examples/phase7_mcp_client_demo.py")
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
