"""
Data.gov API Integration Agent for DIA3
Handles real-time data fetching, analysis, and natural language querying for China and Russia data.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from src.agents.base_agent import StrandsBaseAgent
from src.core.models import AnalysisRequest, AnalysisResult, DataType
from src.core.datagov.data_ingestion_manager import DataIngestionManager
from src.core.datagov.analysis_engine import DataGovAnalysisEngine
from src.core.datagov.query_processor import NLQueryProcessor
from src.core.datagov.data_processing_engine import DataProcessingEngine
from src.core.datagov.predictive_models import PredictiveModelingEngine
from src.core.datagov.analysis_algorithms import AdvancedAnalysisEngine
from src.core.datagov.real_time_monitoring import RealTimeMonitoringEngine, Metric

logger = logging.getLogger(__name__)


class DataGovAgent(StrandsBaseAgent):
    """Agent for Data.gov API integration and analysis."""
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(agent_id=agent_id, max_capacity=5)
        self.data_manager = DataIngestionManager()
        self.analysis_engine = DataGovAnalysisEngine()
        self.query_processor = NLQueryProcessor()
        self.data_processor = DataProcessingEngine()
        
        # Phase 3 components
        self.predictive_engine = PredictiveModelingEngine()
        self.advanced_analysis = AdvancedAnalysisEngine()
        self.monitoring_engine = RealTimeMonitoringEngine()
        
        self.logger = logging.getLogger(f"{__name__}.{self.agent_id}")
    
    async def can_process(self, request: AnalysisRequest) -> bool:
        """Check if this agent can process the given request."""
        return request.data_type in [
            DataType.TRADE_DATA, 
            DataType.ECONOMIC_DATA, 
            DataType.ENVIRONMENTAL_DATA
        ]
    
    async def process(self, request: AnalysisRequest) -> AnalysisResult:
        """Process Data.gov analysis requests."""
        try:
            self.logger.info(f"Processing Data.gov request: {request.request_id}")
            
            # Extract countries from parameters, default to China and Russia
            countries = request.parameters.get('countries', ['CHN', 'RUS'])
            
            # Fetch live data from Data.gov APIs
            self.logger.info(f"Fetching data for countries: {countries}")
            raw_data = await self.data_manager.fetch_live_data(countries)
            
            # Process data using Phase 2 processing engine
            self.logger.info("Processing data using Phase 2 processing engine")
            if request.data_type == DataType.TRADE_DATA:
                processed_data = await self.data_processor.process_trade_data(raw_data)
            elif request.data_type == DataType.ECONOMIC_DATA:
                processed_data = await self.data_processor.process_macroeconomic_data(raw_data)
            elif request.data_type == DataType.ENVIRONMENTAL_DATA:
                processed_data = await self.data_processor.process_environmental_data(raw_data)
            else:
                # Fallback to original analysis engine for other data types
                self.logger.info("Using fallback analysis engine")
                processed_data = await self.analysis_engine.process_data(raw_data)
            
            # Store processed data in vector DB and knowledge graph
            self.logger.info("Storing processed data in vector DB and knowledge graph")
            storage_success = await self.data_processor.store_processed_data(processed_data)
            
            # Generate quality report
            quality_report = await self.data_processor.get_data_quality_report(processed_data)
            
            # Generate analysis metadata
            metadata = {
                "embeddings_count": len(embeddings),
                "relationships_count": len(relationships),
                "data_sources": list(raw_data.keys()),
                "countries_analyzed": countries,
                "processing_timestamp": datetime.utcnow().isoformat(),
                "agent_id": self.agent_id
            }
            
            self.logger.info(f"Successfully processed request {request.request_id}")
            
            return AnalysisResult(
                request_id=request.request_id,
                status="completed",
                data=processed_data.processed_data if hasattr(processed_data, 'processed_data') else processed_data,
                metadata={
                    "storage_success": storage_success,
                    "quality_report": quality_report,
                    "data_sources": list(raw_data.keys()),
                    "processing_version": "2.0"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Data.gov agent processing failed: {e}")
            return AnalysisResult(
                request_id=request.request_id,
                status="failed",
                error=str(e)
            )
    
    async def answer_natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process natural language queries against Data.gov data."""
        try:
            self.logger.info(f"Processing natural language query: {query}")
            result = await self.query_processor.process_query(query)
            self.logger.info("Natural language query processed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Natural language query failed: {e}")
            return {"error": str(e), "query": query}
    
    async def get_trade_analysis(self, countries: List[str], time_period: str = "latest") -> Dict[str, Any]:
        """Get trade analysis for specified countries."""
        try:
            self.logger.info(f"Getting trade analysis for countries: {countries}")
            trade_data = await self.data_manager.fetch_trade_data(countries, time_period)
            analysis = await self.analysis_engine.analyze_trade_data(trade_data)
            return analysis
        except Exception as e:
            self.logger.error(f"Trade analysis failed: {e}")
            return {"error": str(e)}
    
    async def get_economic_forecast(self, country: str, forecast_period: str = "1Y") -> Dict[str, Any]:
        """Generate economic forecast for specified country."""
        try:
            self.logger.info(f"Generating economic forecast for {country}")
            economic_data = await self.data_manager.fetch_economic_data([country])
            forecast = await self.analysis_engine.generate_economic_forecast(economic_data, forecast_period)
            return forecast
        except Exception as e:
            self.logger.error(f"Economic forecast failed: {e}")
            return {"error": str(e)}
    
    async def get_environmental_analysis(self, countries: List[str]) -> Dict[str, Any]:
        """Get environmental analysis for specified countries."""
        try:
            self.logger.info(f"Getting environmental analysis for countries: {countries}")
            env_data = await self.data_manager.fetch_environmental_data(countries)
            analysis = await self.analysis_engine.analyze_environmental_data(env_data)
            return analysis
        except Exception as e:
            self.logger.error(f"Environmental analysis failed: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on Data.gov agent and its components."""
        try:
            health_status = {
                "agent_id": self.agent_id,
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "components": {}
            }
            
            # Check data manager
            try:
                await self.data_manager.health_check()
                health_status["components"]["data_manager"] = "healthy"
            except Exception as e:
                health_status["components"]["data_manager"] = f"unhealthy: {str(e)}"
                health_status["status"] = "degraded"
            
            # Check analysis engine
            try:
                await self.analysis_engine.health_check()
                health_status["components"]["analysis_engine"] = "healthy"
            except Exception as e:
                health_status["components"]["analysis_engine"] = f"unhealthy: {str(e)}"
                health_status["status"] = "degraded"
            
            # Check query processor
            try:
                await self.query_processor.health_check()
                health_status["components"]["query_processor"] = "healthy"
            except Exception as e:
                health_status["components"]["query_processor"] = f"unhealthy: {str(e)}"
                health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {
                "agent_id": self.agent_id,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    # Phase 3 Methods
    
    async def train_predictive_models(self, historical_data: List[Dict[str, Any]], 
                                    model_type: str = "all") -> Dict[str, Any]:
        """Train predictive models using historical data."""
        try:
            self.logger.info(f"Training predictive models: {model_type}")
            
            results = {}
            
            if model_type in ["all", "trade_forecast"]:
                results["trade_forecast"] = await self.predictive_engine.train_trade_forecast_model(historical_data)
            
            if model_type in ["all", "economic_trends"]:
                results["economic_trends"] = await self.predictive_engine.train_economic_trends_model(historical_data)
            
            if model_type in ["all", "policy_impact"]:
                results["policy_impact"] = await self.predictive_engine.train_policy_impact_model(historical_data)
            
            return {
                "status": "success",
                "models_trained": list(results.keys()),
                "results": results
            }
            
        except Exception as e:
            self.logger.error(f"Error training predictive models: {e}")
            return {"status": "error", "message": str(e)}
    
    async def forecast_trade_flows(self, input_data: Dict[str, Any], 
                                 forecast_periods: int = 12) -> Dict[str, Any]:
        """Forecast trade flows using trained models."""
        try:
            self.logger.info("Forecasting trade flows")
            return await self.predictive_engine.forecast_trade_flows(input_data, forecast_periods)
        except Exception as e:
            self.logger.error(f"Error forecasting trade flows: {e}")
            return {"status": "error", "message": str(e)}
    
    async def predict_economic_indicators(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict economic indicators using trained models."""
        try:
            self.logger.info("Predicting economic indicators")
            return await self.predictive_engine.predict_economic_indicators(input_data)
        except Exception as e:
            self.logger.error(f"Error predicting economic indicators: {e}")
            return {"status": "error", "message": str(e)}
    
    async def assess_policy_impact(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess policy impact using trained models."""
        try:
            self.logger.info("Assessing policy impact")
            return await self.predictive_engine.assess_policy_impact(policy_data)
        except Exception as e:
            self.logger.error(f"Error assessing policy impact: {e}")
            return {"status": "error", "message": str(e)}
    
    async def identify_trends(self, time_series_data: List[Dict[str, Any]], 
                            variable: str, window_size: int = 12) -> Dict[str, Any]:
        """Identify trends in time series data."""
        try:
            self.logger.info(f"Identifying trends for variable: {variable}")
            return await self.advanced_analysis.identify_trends(time_series_data, variable, window_size)
        except Exception as e:
            self.logger.error(f"Error identifying trends: {e}")
            return {"status": "error", "message": str(e)}
    
    async def correlation_analysis(self, data: List[Dict[str, Any]], 
                                 variables: List[str]) -> Dict[str, Any]:
        """Perform correlation analysis between variables."""
        try:
            self.logger.info(f"Performing correlation analysis for variables: {variables}")
            return await self.advanced_analysis.correlation_analysis(data, variables)
        except Exception as e:
            self.logger.error(f"Error performing correlation analysis: {e}")
            return {"status": "error", "message": str(e)}
    
    async def detect_anomalies(self, data: List[Dict[str, Any]], 
                             variables: List[str], method: str = 'isolation_forest') -> Dict[str, Any]:
        """Detect anomalies in the data."""
        try:
            self.logger.info(f"Detecting anomalies using method: {method}")
            return await self.advanced_analysis.detect_anomalies(data, variables, method)
        except Exception as e:
            self.logger.error(f"Error detecting anomalies: {e}")
            return {"status": "error", "message": str(e)}
    
    async def cluster_analysis(self, data: List[Dict[str, Any]], 
                             variables: List[str], method: str = 'kmeans') -> Dict[str, Any]:
        """Perform cluster analysis on the data."""
        try:
            self.logger.info(f"Performing cluster analysis using method: {method}")
            return await self.advanced_analysis.cluster_analysis(data, variables, method)
        except Exception as e:
            self.logger.error(f"Error performing cluster analysis: {e}")
            return {"status": "error", "message": str(e)}
    
    async def pattern_recognition(self, time_series_data: List[Dict[str, Any]], 
                                variable: str) -> Dict[str, Any]:
        """Recognize patterns in time series data."""
        try:
            self.logger.info(f"Recognizing patterns for variable: {variable}")
            return await self.advanced_analysis.pattern_recognition(time_series_data, variable)
        except Exception as e:
            self.logger.error(f"Error recognizing patterns: {e}")
            return {"status": "error", "message": str(e)}
    
    async def start_monitoring(self) -> Dict[str, Any]:
        """Start real-time monitoring system."""
        try:
            self.logger.info("Starting real-time monitoring system")
            return await self.monitoring_engine.start_monitoring()
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")
            return {"status": "error", "message": str(e)}
    
    async def stop_monitoring(self) -> Dict[str, Any]:
        """Stop real-time monitoring system."""
        try:
            self.logger.info("Stopping real-time monitoring system")
            return await self.monitoring_engine.stop_monitoring()
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")
            return {"status": "error", "message": str(e)}
    
    async def create_dashboard(self, dashboard_id: str, name: str) -> Dict[str, Any]:
        """Create a new monitoring dashboard."""
        try:
            self.logger.info(f"Creating dashboard: {dashboard_id}")
            return await self.monitoring_engine.create_dashboard(dashboard_id, name)
        except Exception as e:
            self.logger.error(f"Error creating dashboard: {e}")
            return {"status": "error", "message": str(e)}
    
    async def add_metric_to_dashboard(self, dashboard_id: str, metric: Metric) -> Dict[str, Any]:
        """Add a metric to a dashboard."""
        try:
            self.logger.info(f"Adding metric to dashboard: {dashboard_id}")
            return await self.monitoring_engine.add_metric_to_dashboard(dashboard_id, metric)
        except Exception as e:
            self.logger.error(f"Error adding metric to dashboard: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Get dashboard data."""
        try:
            return await self.monitoring_engine.get_dashboard_data(dashboard_id)
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_alerts(self, severity: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get monitoring alerts."""
        try:
            return await self.monitoring_engine.get_alerts(severity, limit)
        except Exception as e:
            self.logger.error(f"Error getting alerts: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        try:
            return await self.monitoring_engine.get_performance_metrics()
        except Exception as e:
            self.logger.error(f"Error getting performance metrics: {e}")
            return {"status": "error", "message": str(e)}
