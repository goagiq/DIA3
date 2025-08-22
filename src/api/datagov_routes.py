"""
Data.gov API Routes
FastAPI routes for Data.gov integration and analysis.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from src.core.models import AnalysisRequest, AnalysisResult, DataType
from src.agents.datagov_agent import DataGovAgent
from src.config.datagov_config import DataGovConfig

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/datagov", tags=["datagov"])

# Initialize Data.gov agent
datagov_agent = DataGovAgent()


@router.post("/trade-analysis")
async def trade_analysis(request: Dict[str, Any]):
    """Analyze trade data from Data.gov APIs."""
    try:
        logger.info(f"Processing trade analysis request: {request}")
        
        # Create analysis request
        analysis_request = AnalysisRequest(
            data_type=DataType.TRADE_DATA,
            parameters=request
        )
        
        # Process with Data.gov agent
        result = await datagov_agent.process(analysis_request)
        
        if result.status == "failed":
            raise HTTPException(status_code=500, detail=result.error)
        
        return {
            "status": "success",
            "data": result.data,
            "metadata": result.metadata,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Trade analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/economic-forecast")
async def economic_forecast(request: Dict[str, Any]):
    """Generate economic forecasts using Data.gov data."""
    try:
        logger.info(f"Processing economic forecast request: {request}")
        
        # Create analysis request
        analysis_request = AnalysisRequest(
            data_type=DataType.ECONOMIC_DATA,
            parameters=request
        )
        
        # Process with Data.gov agent
        result = await datagov_agent.process(analysis_request)
        
        if result.status == "failed":
            raise HTTPException(status_code=500, detail=result.error)
        
        return {
            "status": "success",
            "data": result.data,
            "metadata": result.metadata,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Economic forecast failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/environmental-analysis")
async def environmental_analysis(request: Dict[str, Any]):
    """Analyze environmental data from Data.gov APIs."""
    try:
        logger.info(f"Processing environmental analysis request: {request}")
        
        # Create analysis request
        analysis_request = AnalysisRequest(
            data_type=DataType.ENVIRONMENTAL_DATA,
            parameters=request
        )
        
        # Process with Data.gov agent
        result = await datagov_agent.process(analysis_request)
        
        if result.status == "failed":
            raise HTTPException(status_code=500, detail=result.error)
        
        return {
            "status": "success",
            "data": result.data,
            "metadata": result.metadata,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Environmental analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/natural-language-query")
async def natural_language_query(request: Dict[str, Any]):
    """Process natural language queries against Data.gov data."""
    try:
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        logger.info(f"Processing natural language query: {query}")
        
        # Process with Data.gov agent
        result = await datagov_agent.answer_natural_language_query(query)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Natural language query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trade-data/{country_code}")
async def get_trade_data(country_code: str, time_period: str = "latest"):
    """Get trade data for a specific country."""
    try:
        logger.info(f"Getting trade data for country: {country_code}")
        
        result = await datagov_agent.get_trade_analysis([country_code], time_period)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            "country_code": country_code,
            "time_period": time_period,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get trade data failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economic-forecast/{country_code}")
async def get_economic_forecast(country_code: str, forecast_period: str = "1Y"):
    """Get economic forecast for a specific country."""
    try:
        logger.info(f"Getting economic forecast for country: {country_code}")
        
        result = await datagov_agent.get_economic_forecast(country_code, forecast_period)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            "country_code": country_code,
            "forecast_period": forecast_period,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get economic forecast failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/environmental-data/{country_code}")
async def get_environmental_data(country_code: str):
    """Get environmental data for a specific country."""
    try:
        logger.info(f"Getting environmental data for country: {country_code}")
        
        result = await datagov_agent.get_environmental_analysis([country_code])
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "status": "success",
            "country_code": country_code,
            "data": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get environmental data failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/comprehensive-analysis")
async def comprehensive_analysis(request: Dict[str, Any]):
    """Perform comprehensive analysis across all data types."""
    try:
        logger.info(f"Processing comprehensive analysis request: {request}")
        
        countries = request.get("countries", ["CHN", "RUS"])
        
        # Perform analysis across all data types
        results = {}
        
        # Trade analysis
        trade_result = await datagov_agent.get_trade_analysis(countries)
        results["trade"] = trade_result
        
        # Economic forecast
        economic_results = {}
        for country in countries:
            economic_results[country] = await datagov_agent.get_economic_forecast(country)
        results["economic"] = economic_results
        
        # Environmental analysis
        env_result = await datagov_agent.get_environmental_analysis(countries)
        results["environmental"] = env_result
        
        return {
            "status": "success",
            "countries": countries,
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check the health of Data.gov integration."""
    try:
        logger.info("Performing Data.gov health check")
        
        health_status = await datagov_agent.health_check()
        
        return {
            "status": "success",
            "health": health_status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_config():
    """Get Data.gov configuration."""
    try:
        config = DataGovConfig()
        
        return {
            "status": "success",
            "config": {
                "census_api_key_configured": bool(config.CENSUS_API_KEY),
                "enabled_data_sources": config.ENABLED_DATA_SOURCES,
                "rate_limits": {
                    "census_api": {
                        "requests_per_day": config.CENSUS_RATE_LIMIT_PER_DAY,
                        "requests_per_minute": config.CENSUS_RATE_LIMIT_PER_MINUTE
                    }
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get config failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch-analysis")
async def batch_analysis(background_tasks: BackgroundTasks, request: Dict[str, Any]):
    """Perform batch analysis for multiple countries and data types."""
    try:
        logger.info(f"Processing batch analysis request: {request}")
        
        countries = request.get("countries", ["CHN", "RUS"])
        data_types = request.get("data_types", ["trade", "economic", "environmental"])
        
        # Start background task for batch processing
        background_tasks.add_task(
            _process_batch_analysis,
            countries,
            data_types,
            request.get("callback_url")
        )
        
        return {
            "status": "accepted",
            "message": "Batch analysis started",
            "countries": countries,
            "data_types": data_types,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _process_batch_analysis(countries: List[str], data_types: List[str], callback_url: Optional[str] = None):
    """Background task to process batch analysis."""
    try:
        logger.info(f"Processing batch analysis for {len(countries)} countries and {len(data_types)} data types")
        
        results = {}
        
        for data_type in data_types:
            if data_type == "trade":
                results["trade"] = await datagov_agent.get_trade_analysis(countries)
            elif data_type == "economic":
                economic_results = {}
                for country in countries:
                    economic_results[country] = await datagov_agent.get_economic_forecast(country)
                results["economic"] = economic_results
            elif data_type == "environmental":
                results["environmental"] = await datagov_agent.get_environmental_analysis(countries)
        
        # If callback URL is provided, send results
        if callback_url:
            # In a real implementation, you would send the results to the callback URL
            logger.info(f"Batch analysis completed, results would be sent to: {callback_url}")
        
        logger.info("Batch analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Batch analysis background task failed: {e}")
        if callback_url:
            # Send error notification to callback URL
            logger.info(f"Error notification would be sent to: {callback_url}")

# Phase 3 API Endpoints

@router.post("/train-predictive-models")
async def train_predictive_models(request: Dict[str, Any]):
    """Train predictive models using historical data."""
    try:
        logger.info(f"Training predictive models: {request}")
        
        historical_data = request.get("historical_data", [])
        model_type = request.get("model_type", "all")
        
        result = await datagov_agent.train_predictive_models(historical_data, model_type)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Train predictive models failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/forecast-trade-flows")
async def forecast_trade_flows(request: Dict[str, Any]):
    """Forecast trade flows using trained models."""
    try:
        logger.info(f"Forecasting trade flows: {request}")
        
        input_data = request.get("input_data", {})
        forecast_periods = request.get("forecast_periods", 12)
        
        result = await datagov_agent.forecast_trade_flows(input_data, forecast_periods)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Forecast trade flows failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-economic-indicators")
async def predict_economic_indicators(request: Dict[str, Any]):
    """Predict economic indicators using trained models."""
    try:
        logger.info(f"Predicting economic indicators: {request}")
        
        input_data = request.get("input_data", {})
        
        result = await datagov_agent.predict_economic_indicators(input_data)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Predict economic indicators failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assess-policy-impact")
async def assess_policy_impact(request: Dict[str, Any]):
    """Assess policy impact using trained models."""
    try:
        logger.info(f"Assessing policy impact: {request}")
        
        policy_data = request.get("policy_data", {})
        
        result = await datagov_agent.assess_policy_impact(policy_data)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Assess policy impact failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/identify-trends")
async def identify_trends(request: Dict[str, Any]):
    """Identify trends in time series data."""
    try:
        logger.info(f"Identifying trends: {request}")
        
        time_series_data = request.get("time_series_data", [])
        variable = request.get("variable", "")
        window_size = request.get("window_size", 12)
        
        result = await datagov_agent.identify_trends(time_series_data, variable, window_size)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Identify trends failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/correlation-analysis")
async def correlation_analysis(request: Dict[str, Any]):
    """Perform correlation analysis between variables."""
    try:
        logger.info(f"Performing correlation analysis: {request}")
        
        data = request.get("data", [])
        variables = request.get("variables", [])
        
        result = await datagov_agent.correlation_analysis(data, variables)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Correlation analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect-anomalies")
async def detect_anomalies(request: Dict[str, Any]):
    """Detect anomalies in the data."""
    try:
        logger.info(f"Detecting anomalies: {request}")
        
        data = request.get("data", [])
        variables = request.get("variables", [])
        method = request.get("method", "isolation_forest")
        
        result = await datagov_agent.detect_anomalies(data, variables, method)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Detect anomalies failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cluster-analysis")
async def cluster_analysis(request: Dict[str, Any]):
    """Perform cluster analysis on the data."""
    try:
        logger.info(f"Performing cluster analysis: {request}")
        
        data = request.get("data", [])
        variables = request.get("variables", [])
        method = request.get("method", "kmeans")
        
        result = await datagov_agent.cluster_analysis(data, variables, method)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Cluster analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pattern-recognition")
async def pattern_recognition(request: Dict[str, Any]):
    """Recognize patterns in time series data."""
    try:
        logger.info(f"Recognizing patterns: {request}")
        
        time_series_data = request.get("time_series_data", [])
        variable = request.get("variable", "")
        
        result = await datagov_agent.pattern_recognition(time_series_data, variable)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Pattern recognition failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start-monitoring")
async def start_monitoring():
    """Start real-time monitoring system."""
    try:
        logger.info("Starting real-time monitoring system")
        
        result = await datagov_agent.start_monitoring()
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Start monitoring failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop-monitoring")
async def stop_monitoring():
    """Stop real-time monitoring system."""
    try:
        logger.info("Stopping real-time monitoring system")
        
        result = await datagov_agent.stop_monitoring()
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Stop monitoring failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-dashboard")
async def create_dashboard(request: Dict[str, Any]):
    """Create a new monitoring dashboard."""
    try:
        logger.info(f"Creating dashboard: {request}")
        
        dashboard_id = request.get("dashboard_id", "")
        name = request.get("name", "")
        
        result = await datagov_agent.create_dashboard(dashboard_id, name)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Create dashboard failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/{dashboard_id}")
async def get_dashboard_data(dashboard_id: str):
    """Get dashboard data."""
    try:
        logger.info(f"Getting dashboard data for: {dashboard_id}")
        
        result = await datagov_agent.get_dashboard_data(dashboard_id)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get dashboard data failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
async def get_alerts(severity: str = None, limit: int = 50):
    """Get monitoring alerts."""
    try:
        logger.info(f"Getting alerts with severity: {severity}, limit: {limit}")
        
        result = await datagov_agent.get_alerts(severity, limit)
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get alerts failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance-metrics")
async def get_performance_metrics():
    """Get performance metrics."""
    try:
        logger.info("Getting performance metrics")
        
        result = await datagov_agent.get_performance_metrics()
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get performance metrics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
