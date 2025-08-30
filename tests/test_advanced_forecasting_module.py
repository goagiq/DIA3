#!/usr/bin/env python3
"""
Advanced Forecasting Module Test Script

This script tests the Advanced Forecasting Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.advanced_forecasting_module import AdvancedForecastingModule


async def test_advanced_forecasting_module():
    """Test the Advanced Forecasting Module functionality."""
    logger.info("=== Testing Advanced Forecasting Module ===")
    
    # Initialize module
    module = AdvancedForecastingModule()
    
    # Test data for advanced forecasting
    test_data = {
        "advanced_forecasting": {
            "forecasting_models": {
                "models": [
                    {
                        "name": "Time Series ARIMA",
                        "accuracy": 0.89,
                        "complexity": "Medium",
                        "training_time": 45,
                        "prediction_horizon": 12,
                        "confidence_interval": 0.85
                    },
                    {
                        "name": "Neural Network LSTM",
                        "accuracy": 0.92,
                        "complexity": "High",
                        "training_time": 120,
                        "prediction_horizon": 24,
                        "confidence_interval": 0.88
                    },
                    {
                        "name": "Random Forest Ensemble",
                        "accuracy": 0.87,
                        "complexity": "Medium",
                        "training_time": 30,
                        "prediction_horizon": 6,
                        "confidence_interval": 0.82
                    },
                    {
                        "name": "Gradient Boosting",
                        "accuracy": 0.91,
                        "complexity": "High",
                        "training_time": 90,
                        "prediction_horizon": 18,
                        "confidence_interval": 0.86
                    }
                ]
            },
            "predictive_results": {
                "predictions": [
                    {"period": "Q1 2024", "actual": 85, "predicted": 87, "confidence": 0.89, "error": 2.4},
                    {"period": "Q2 2024", "actual": 88, "predicted": 90, "confidence": 0.91, "error": 2.3},
                    {"period": "Q3 2024", "actual": 92, "predicted": 93, "confidence": 0.88, "error": 1.1},
                    {"period": "Q4 2024", "actual": 95, "predicted": 96, "confidence": 0.92, "error": 1.1},
                    {"period": "Q1 2025", "actual": None, "predicted": 98, "confidence": 0.85, "error": None},
                    {"period": "Q2 2025", "actual": None, "predicted": 101, "confidence": 0.82, "error": None},
                    {"period": "Q3 2025", "actual": None, "predicted": 104, "confidence": 0.79, "error": None},
                    {"period": "Q4 2025", "actual": None, "predicted": 107, "confidence": 0.76, "error": None}
                ]
            },
            "advanced_analytics": {
                "metrics": [
                    {"metric": "Mean Absolute Error", "value": 2.1, "unit": "%", "trend": "decreasing"},
                    {"metric": "Root Mean Square Error", "value": 3.2, "unit": "%", "trend": "decreasing"},
                    {"metric": "R-squared Score", "value": 0.89, "unit": "", "trend": "increasing"},
                    {"metric": "Mean Absolute Percentage Error", "value": 4.5, "unit": "%", "trend": "decreasing"},
                    {"metric": "Forecast Bias", "value": 0.8, "unit": "%", "trend": "stable"},
                    {"metric": "Prediction Interval Width", "value": 8.2, "unit": "%", "trend": "stable"}
                ],
                "summary": {
                    "total_predictions": 156,
                    "accuracy_threshold": 0.85,
                    "models_used": 4,
                    "forecast_horizon": 24
                }
            },
            "model_performance": {
                "performance_metrics": [
                    {"model": "ARIMA", "accuracy": 0.89, "precision": 0.87, "recall": 0.91, "f1_score": 0.89},
                    {"model": "LSTM", "accuracy": 0.92, "precision": 0.90, "recall": 0.94, "f1_score": 0.92},
                    {"model": "Random Forest", "accuracy": 0.87, "precision": 0.85, "recall": 0.89, "f1_score": 0.87},
                    {"model": "Gradient Boosting", "accuracy": 0.91, "precision": 0.89, "recall": 0.93, "f1_score": 0.91}
                ]
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Advanced Forecasting Models", "Forecasting models section"),
        ("Predictive Modeling Results", "Predictive results section"),
        ("Advanced Analytics", "Advanced analytics section"),
        ("Model Performance", "Model performance section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("advancedForecastingModelsChart", "Forecasting models chart"),
        ("predictiveModelingResultsChart", "Predictive results chart"),
        ("modelPerformanceChart", "Model performance chart"),
        ("Chart.js", "Chart.js integration"),
        ("radar", "Radar chart"),
        ("line", "Line chart"),
        ("bar", "Bar chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "advanced_forecasting_models",
        "predictive_modeling_results",
        "advanced_analytics",
        "model_performance"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "advancedForecastingModelsChart",
        "predictiveModelingResultsChart",
        "modelPerformanceChart"
    ]
    
    chart_issues = []
    for chart_id in chart_checks:
        if f'id="{chart_id}"' not in content:
            chart_issues.append(f"Missing chart: {chart_id}")
    
    total_issues = len(issues) + len(tooltip_issues) + len(chart_issues)
    
    if issues:
        logger.warning(f"⚠️ Found {len(issues)} content issues:")
        for issue in issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ All content components verified successfully")
    
    if tooltip_issues:
        logger.warning(f"⚠️ Found {len(tooltip_issues)} tooltip issues:")
        for issue in tooltip_issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ All tooltips verified successfully")
    
    if chart_issues:
        logger.warning(f"⚠️ Found {len(chart_issues)} chart issues:")
        for issue in chart_issues:
            logger.warning(f"  - {issue}")
    else:
        logger.info("✅ All charts verified successfully")
    
    if total_issues == 0:
        logger.info("✅ Advanced Forecasting Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Advanced Forecasting Module test")
        return False


async def test_advanced_forecasting_module_defaults():
    """Test the Advanced Forecasting Module with default data."""
    logger.info("=== Testing Advanced Forecasting Module with Defaults ===")
    
    # Initialize module
    module = AdvancedForecastingModule()
    
    # Test with minimal data
    test_data = {
        "advanced_forecasting": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Advanced Forecasting Models",
        "Predictive Modeling Results",
        "Advanced Analytics",
        "Model Performance"
    ]
    
    success = True
    for check in checks:
        if check not in content:
            logger.error(f"Missing: {check}")
            success = False
    
    if success:
        logger.info("✅ Default data test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.error("❌ Default data test failed")
        return False


async def main():
    """Run all advanced forecasting module tests."""
    logger.info("🚀 Starting Advanced Forecasting Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_advanced_forecasting_module()
    
    # Test 2: Default data test
    default_test_result = await test_advanced_forecasting_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Advanced Forecasting Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Advanced Forecasting Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
