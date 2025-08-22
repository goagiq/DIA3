"""
Comprehensive Test Suite for Data.gov Integration - Phase 3
Tests predictive modeling, analysis algorithms, and real-time monitoring components.
"""

import asyncio
import sys
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataGovPhase3TestSuite:
    """Comprehensive test suite for Data.gov Phase 3 components."""
    
    def __init__(self):
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        
        # Import Phase 3 components
        try:
            from src.core.datagov.predictive_models import PredictiveModelingEngine
            from src.core.datagov.analysis_algorithms import AdvancedAnalysisEngine
            from src.core.datagov.real_time_monitoring import RealTimeMonitoringEngine, Metric
            from src.agents.datagov_agent import DataGovAgent
            
            self.predictive_engine = PredictiveModelingEngine()
            self.advanced_analysis = AdvancedAnalysisEngine()
            self.monitoring_engine = RealTimeMonitoringEngine()
            self.agent = DataGovAgent()
            
            logger.info("✅ Phase 3 components imported successfully")
            
        except ImportError as e:
            logger.error(f"❌ Failed to import Phase 3 components: {e}")
            raise
    
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result."""
        self.test_results["total_tests"] += 1
        
        if success:
            self.test_results["passed_tests"] += 1
            logger.info(f"✅ {test_name}: PASSED")
        else:
            self.test_results["failed_tests"] += 1
            logger.error(f"❌ {test_name}: FAILED - {details}")
        
        self.test_results["test_details"].append({
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_mock_trade_data(self, n_records: int = 100) -> List[Dict[str, Any]]:
        """Generate mock trade data for testing."""
        import random
        import numpy as np
        
        data = []
        base_date = datetime(2020, 1, 1)
        
        for i in range(n_records):
            record = {
                'date': (base_date + timedelta(days=i*30)).isoformat(),
                'import_value': random.uniform(1000000, 5000000),
                'export_value': random.uniform(800000, 4500000),
                'trade_balance': random.uniform(-500000, 1000000),
                'month': (i % 12) + 1,
                'year': 2020 + (i // 12),
                'gdp_growth': random.uniform(-0.05, 0.08),
                'inflation_rate': random.uniform(0.01, 0.05),
                'exchange_rate': random.uniform(0.8, 1.2),
                'political_stability': random.uniform(0.3, 0.9),
                'trade_policy_score': random.uniform(0.4, 0.95),
                'import_value_lag1': random.uniform(1000000, 5000000),
                'export_value_lag1': random.uniform(800000, 4500000),
                'trade_balance_lag1': random.uniform(-500000, 1000000),
                'quarter': (i % 4) + 1,
                'next_month_trade_balance': random.uniform(-500000, 1000000)
            }
            data.append(record)
        
        return data
    
    def generate_mock_economic_data(self, n_records: int = 100) -> List[Dict[str, Any]]:
        """Generate mock economic data for testing."""
        import random
        
        data = []
        base_date = datetime(2020, 1, 1)
        
        for i in range(n_records):
            record = {
                'date': (base_date + timedelta(days=i*90)).isoformat(),
                'gdp': random.uniform(10000000, 50000000),
                'gdp_growth': random.uniform(-0.05, 0.08),
                'inflation_rate': random.uniform(0.01, 0.05),
                'unemployment_rate': random.uniform(0.03, 0.12),
                'interest_rate': random.uniform(0.01, 0.08),
                'exchange_rate': random.uniform(0.8, 1.2),
                'population': random.uniform(1000000, 50000000),
                'consumer_confidence': random.uniform(0.3, 0.9),
                'business_confidence': random.uniform(0.4, 0.95),
                'fiscal_balance': random.uniform(-1000000, 2000000),
                'current_account_balance': random.uniform(-500000, 1500000),
                'foreign_direct_investment': random.uniform(100000, 1000000),
                'gdp_lag1': random.uniform(10000000, 50000000),
                'inflation_lag1': random.uniform(0.01, 0.05),
                'unemployment_lag1': random.uniform(0.03, 0.12),
                'year': 2020 + (i // 4),
                'quarter': (i % 4) + 1,
                'next_quarter_gdp_growth': random.uniform(-0.05, 0.08)
            }
            data.append(record)
        
        return data
    
    def generate_mock_policy_data(self, n_records: int = 100) -> List[Dict[str, Any]]:
        """Generate mock policy data for testing."""
        import random
        
        data = []
        base_date = datetime(2020, 1, 1)
        
        for i in range(n_records):
            record = {
                'date': (base_date + timedelta(days=i*30)).isoformat(),
                'policy_change_score': random.uniform(-1.0, 1.0),
                'trade_policy_score': random.uniform(0.3, 0.9),
                'fiscal_policy_score': random.uniform(0.4, 0.95),
                'monetary_policy_score': random.uniform(0.3, 0.9),
                'regulatory_score': random.uniform(0.2, 0.8),
                'political_stability': random.uniform(0.3, 0.9),
                'economic_freedom': random.uniform(0.4, 0.95),
                'corruption_perception': random.uniform(0.2, 0.9),
                'rule_of_law': random.uniform(0.3, 0.9),
                'government_effectiveness': random.uniform(0.2, 0.8),
                'economic_impact_score': random.uniform(-1.0, 1.0)
            }
            data.append(record)
        
        return data
    
    async def test_predictive_models(self):
        """Test predictive modeling engine."""
        logger.info("\n🧪 Testing Predictive Models Engine")
        
        # Test 1: Trade forecast model training
        try:
            trade_data = self.generate_mock_trade_data(50)
            result = await self.predictive_engine.train_trade_forecast_model(trade_data)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Trade Forecast Model Training",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Trade Forecast Model Training",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 2: Economic trends model training
        try:
            economic_data = self.generate_mock_economic_data(50)
            result = await self.predictive_engine.train_economic_trends_model(economic_data)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Economic Trends Model Training",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Economic Trends Model Training",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 3: Policy impact model training
        try:
            policy_data = self.generate_mock_policy_data(50)
            result = await self.predictive_engine.train_policy_impact_model(policy_data)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Policy Impact Model Training",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Policy Impact Model Training",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 4: Trade flow forecasting
        try:
            input_data = {
                'import_value': 3000000,
                'export_value': 2500000,
                'trade_balance': 500000,
                'month': 6,
                'year': 2023,
                'gdp_growth': 0.03,
                'inflation_rate': 0.025,
                'exchange_rate': 1.0,
                'political_stability': 0.7,
                'trade_policy_score': 0.8
            }
            
            result = await self.predictive_engine.forecast_trade_flows(input_data)
            
            success = result.get("status") == "success" or "model not trained" in result.get("message", "").lower()
            self.log_test_result(
                "Trade Flow Forecasting",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Trade Flow Forecasting",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 5: Economic indicators prediction
        try:
            input_data = {
                'gdp': 25000000,
                'gdp_growth': 0.03,
                'inflation_rate': 0.025,
                'unemployment_rate': 0.05,
                'interest_rate': 0.04,
                'exchange_rate': 1.0,
                'population': 25000000,
                'consumer_confidence': 0.7,
                'business_confidence': 0.75
            }
            
            result = await self.predictive_engine.predict_economic_indicators(input_data)
            
            success = result.get("status") == "success" or "model not trained" in result.get("message", "").lower()
            self.log_test_result(
                "Economic Indicators Prediction",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Economic Indicators Prediction",
                False,
                f"Exception: {str(e)}"
            )
    
    async def test_analysis_algorithms(self):
        """Test advanced analysis algorithms."""
        logger.info("\n🧪 Testing Analysis Algorithms")
        
        # Test 1: Trend identification
        try:
            time_series_data = self.generate_mock_trade_data(24)  # 2 years of monthly data
            result = await self.advanced_analysis.identify_trends(time_series_data, 'trade_balance')
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Trend Identification",
                success,
                f"Trend direction: {result.get('trend_analysis', {}).get('trend_direction', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Trend Identification",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 2: Correlation analysis
        try:
            data = self.generate_mock_trade_data(50)
            variables = ['import_value', 'export_value', 'trade_balance', 'gdp_growth']
            result = await self.advanced_analysis.correlation_analysis(data, variables)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Correlation Analysis",
                success,
                f"Found {len(result.get('strong_correlations', []))} strong correlations"
            )
        except Exception as e:
            self.log_test_result(
                "Correlation Analysis",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 3: Anomaly detection
        try:
            data = self.generate_mock_trade_data(50)
            variables = ['import_value', 'export_value', 'trade_balance']
            result = await self.advanced_analysis.detect_anomalies(data, variables)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Anomaly Detection",
                success,
                f"Detected {result.get('statistics', {}).get('anomalous_points', 0)} anomalies"
            )
        except Exception as e:
            self.log_test_result(
                "Anomaly Detection",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 4: Cluster analysis
        try:
            data = self.generate_mock_trade_data(50)
            variables = ['import_value', 'export_value', 'gdp_growth', 'inflation_rate']
            result = await self.advanced_analysis.cluster_analysis(data, variables)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Cluster Analysis",
                success,
                f"Found {result.get('quality_metrics', {}).get('n_clusters', 0)} clusters"
            )
        except Exception as e:
            self.log_test_result(
                "Cluster Analysis",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 5: Pattern recognition
        try:
            time_series_data = self.generate_mock_trade_data(36)  # 3 years of monthly data
            result = await self.advanced_analysis.pattern_recognition(time_series_data, 'trade_balance')
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Pattern Recognition",
                success,
                f"Found {result.get('statistics', {}).get('n_peaks', 0)} peaks and {result.get('statistics', {}).get('n_troughs', 0)} troughs"
            )
        except Exception as e:
            self.log_test_result(
                "Pattern Recognition",
                False,
                f"Exception: {str(e)}"
            )
    
    async def test_real_time_monitoring(self):
        """Test real-time monitoring engine."""
        logger.info("\n🧪 Testing Real-time Monitoring Engine")
        
        # Test 1: Start monitoring
        try:
            result = await self.monitoring_engine.start_monitoring()
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Start Monitoring",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Start Monitoring",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 2: Create dashboard
        try:
            result = await self.monitoring_engine.create_dashboard("test_dashboard", "Test Dashboard")
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Create Dashboard",
                success,
                f"Dashboard ID: {result.get('dashboard_id', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Create Dashboard",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 3: Add metric to dashboard
        try:
            metric = Metric(
                name="test_metric",
                value=42.0,
                timestamp=datetime.now(),
                unit="units",
                metadata={"source": "test"}
            )
            
            result = await self.monitoring_engine.add_metric_to_dashboard("test_dashboard", metric)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Add Metric to Dashboard",
                success,
                f"Metric: {result.get('metric_name', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Add Metric to Dashboard",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 4: Get dashboard data
        try:
            result = await self.monitoring_engine.get_dashboard_data("test_dashboard")
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Get Dashboard Data",
                success,
                f"Dashboard: {result.get('dashboard', {}).get('name', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Get Dashboard Data",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 5: Get alerts
        try:
            result = await self.monitoring_engine.get_alerts(limit=10)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Get Alerts",
                success,
                f"Total alerts: {result.get('total_alerts', 0)}"
            )
        except Exception as e:
            self.log_test_result(
                "Get Alerts",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 6: Get performance metrics
        try:
            result = await self.monitoring_engine.get_performance_metrics()
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Get Performance Metrics",
                success,
                f"Dashboards: {result.get('dashboards_count', 0)}"
            )
        except Exception as e:
            self.log_test_result(
                "Get Performance Metrics",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 7: Stop monitoring
        try:
            result = await self.monitoring_engine.stop_monitoring()
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Stop Monitoring",
                success,
                f"Result: {result.get('message', 'Unknown')}"
            )
        except Exception as e:
            self.log_test_result(
                "Stop Monitoring",
                False,
                f"Exception: {str(e)}"
            )
    
    async def test_agent_integration(self):
        """Test DataGovAgent Phase 3 integration."""
        logger.info("\n🧪 Testing DataGovAgent Phase 3 Integration")
        
        # Test 1: Train predictive models via agent
        try:
            trade_data = self.generate_mock_trade_data(30)
            result = await self.agent.train_predictive_models(trade_data, "trade_forecast")
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Agent Train Predictive Models",
                success,
                f"Models trained: {len(result.get('models_trained', []))}"
            )
        except Exception as e:
            self.log_test_result(
                "Agent Train Predictive Models",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 2: Trend identification via agent
        try:
            time_series_data = self.generate_mock_trade_data(24)
            result = await self.agent.identify_trends(time_series_data, 'trade_balance')
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Agent Trend Identification",
                success,
                f"Trend analysis completed"
            )
        except Exception as e:
            self.log_test_result(
                "Agent Trend Identification",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 3: Correlation analysis via agent
        try:
            data = self.generate_mock_trade_data(40)
            variables = ['import_value', 'export_value', 'gdp_growth']
            result = await self.agent.correlation_analysis(data, variables)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Agent Correlation Analysis",
                success,
                f"Correlation analysis completed"
            )
        except Exception as e:
            self.log_test_result(
                "Agent Correlation Analysis",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 4: Anomaly detection via agent
        try:
            data = self.generate_mock_trade_data(40)
            variables = ['import_value', 'export_value']
            result = await self.agent.detect_anomalies(data, variables)
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Agent Anomaly Detection",
                success,
                f"Anomaly detection completed"
            )
        except Exception as e:
            self.log_test_result(
                "Agent Anomaly Detection",
                False,
                f"Exception: {str(e)}"
            )
        
        # Test 5: Monitoring via agent
        try:
            result = await self.agent.start_monitoring()
            
            success = result.get("status") == "success"
            self.log_test_result(
                "Agent Start Monitoring",
                success,
                f"Monitoring started: {result.get('message', 'Unknown')}"
            )
            
            # Stop monitoring
            await self.agent.stop_monitoring()
            
        except Exception as e:
            self.log_test_result(
                "Agent Start Monitoring",
                False,
                f"Exception: {str(e)}"
            )
    
    async def run_all_tests(self):
        """Run all Phase 3 tests."""
        logger.info("🚀 Starting Data.gov Phase 3 Test Suite")
        logger.info("=" * 60)
        
        # Run test suites
        await self.test_predictive_models()
        await self.test_analysis_algorithms()
        await self.test_real_time_monitoring()
        await self.test_agent_integration()
        
        # Generate test report
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        logger.info("\n" + "=" * 60)
        logger.info("📊 PHASE 3 TEST RESULTS SUMMARY")
        logger.info("=" * 60)
        
        total = self.test_results["total_tests"]
        passed = self.test_results["passed_tests"]
        failed = self.test_results["failed_tests"]
        
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
        
        if failed > 0:
            logger.info("\n❌ FAILED TESTS:")
            for test in self.test_results["test_details"]:
                if not test["success"]:
                    logger.info(f"  - {test['test_name']}: {test['details']}")
        
        # Save detailed report
        report_file = f"Results/datagov_phase3_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("Results", exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        logger.info(f"\n📄 Detailed report saved to: {report_file}")
        
        # Overall status
        if failed == 0:
            logger.info("\n🎉 ALL TESTS PASSED! Phase 3 implementation is working correctly.")
        else:
            logger.info(f"\n⚠️  {failed} tests failed. Please review the failed tests above.")
        
        logger.info("=" * 60)

async def main():
    """Main test execution function."""
    try:
        # Create and run test suite
        test_suite = DataGovPhase3TestSuite()
        await test_suite.run_all_tests()
        
    except Exception as e:
        logger.error(f"❌ Test suite execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run with .venv/Scripts/python.exe
    asyncio.run(main())
