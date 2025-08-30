#!/usr/bin/env python3
"""
Model Performance Module Test Script

This script tests the Model Performance Module functionality,
including advanced tooltip integration and chart generation.
"""

import asyncio
from loguru import logger

from src.core.modules.model_performance_module import ModelPerformanceModule


async def test_model_performance_module():
    """Test the Model Performance Module functionality."""
    logger.info("=== Testing Model Performance Module ===")
    
    # Initialize module
    module = ModelPerformanceModule()
    
    # Test data for model performance
    test_data = {
        "model_performance": {
            "performance_metrics": {
                "metrics": [
                    {"model": "Linear Regression", "accuracy": 0.85, "precision": 0.83, "recall": 0.87, "f1_score": 0.85, "mae": 0.12, "rmse": 0.18},
                    {"model": "Random Forest", "accuracy": 0.92, "precision": 0.91, "recall": 0.93, "f1_score": 0.92, "mae": 0.08, "rmse": 0.12},
                    {"model": "Gradient Boosting", "accuracy": 0.94, "precision": 0.93, "recall": 0.95, "f1_score": 0.94, "mae": 0.06, "rmse": 0.09},
                    {"model": "Neural Network", "accuracy": 0.96, "precision": 0.95, "recall": 0.97, "f1_score": 0.96, "mae": 0.04, "rmse": 0.07}
                ]
            },
            "accuracy_comparison": {
                "comparisons": [
                    {"metric": "Overall Accuracy", "linear_regression": 0.85, "random_forest": 0.92, "gradient_boosting": 0.94, "neural_network": 0.96},
                    {"metric": "Training Accuracy", "linear_regression": 0.87, "random_forest": 0.94, "gradient_boosting": 0.96, "neural_network": 0.98},
                    {"metric": "Validation Accuracy", "linear_regression": 0.83, "random_forest": 0.90, "gradient_boosting": 0.92, "neural_network": 0.94},
                    {"metric": "Test Accuracy", "linear_regression": 0.82, "random_forest": 0.89, "gradient_boosting": 0.91, "neural_network": 0.93}
                ]
            },
            "performance_analysis": {
                "analysis_metrics": [
                    {"aspect": "Computational Efficiency", "linear_regression": 0.95, "random_forest": 0.75, "gradient_boosting": 0.70, "neural_network": 0.60},
                    {"aspect": "Interpretability", "linear_regression": 0.90, "random_forest": 0.80, "gradient_boosting": 0.70, "neural_network": 0.30},
                    {"aspect": "Scalability", "linear_regression": 0.85, "random_forest": 0.80, "gradient_boosting": 0.75, "neural_network": 0.90},
                    {"aspect": "Robustness", "linear_regression": 0.70, "random_forest": 0.85, "gradient_boosting": 0.80, "neural_network": 0.75},
                    {"aspect": "Feature Importance", "linear_regression": 0.60, "random_forest": 0.90, "gradient_boosting": 0.85, "neural_network": 0.40}
                ],
                "summary": {
                    "total_models": 4,
                    "best_overall": "Neural Network",
                    "best_interpretable": "Linear Regression",
                    "best_balanced": "Random Forest"
                }
            },
            "model_evaluation": {
                "evaluation_criteria": [
                    {"criterion": "Accuracy", "weight": 0.25, "linear_regression": 0.85, "random_forest": 0.92, "gradient_boosting": 0.94, "neural_network": 0.96},
                    {"criterion": "Interpretability", "weight": 0.20, "linear_regression": 0.90, "random_forest": 0.80, "gradient_boosting": 0.70, "neural_network": 0.30},
                    {"criterion": "Computational Cost", "weight": 0.15, "linear_regression": 0.95, "random_forest": 0.75, "gradient_boosting": 0.70, "neural_network": 0.60},
                    {"criterion": "Robustness", "weight": 0.20, "linear_regression": 0.70, "random_forest": 0.85, "gradient_boosting": 0.80, "neural_network": 0.75},
                    {"criterion": "Scalability", "weight": 0.20, "linear_regression": 0.85, "random_forest": 0.80, "gradient_boosting": 0.75, "neural_network": 0.90}
                ]
            }
        }
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Verify content
    checks = [
        ("Model Performance Metrics", "Performance metrics section"),
        ("Accuracy Comparison", "Accuracy comparison section"),
        ("Performance Analysis", "Performance analysis section"),
        ("Model Evaluation", "Model evaluation section"),
        ("chart-container", "Chart containers"),
        ("data-tooltip", "Tooltip attributes"),
        ("modelPerformanceMetricsChart", "Performance metrics chart"),
        ("accuracyComparisonChart", "Accuracy comparison chart"),
        ("modelEvaluationChart", "Model evaluation chart"),
        ("Chart.js", "Chart.js integration"),
        ("radar", "Radar chart"),
        ("bar", "Bar chart"),
        ("line", "Line chart")
    ]
    
    issues = []
    for check_text, description in checks:
        if check_text not in content:
            issues.append(f"Missing {description}")
    
    # Check tooltip functionality
    tooltip_checks = [
        "performance_metrics",
        "accuracy_comparison",
        "performance_analysis",
        "model_evaluation"
    ]
    
    tooltip_issues = []
    for tooltip_id in tooltip_checks:
        if f'data-tooltip-{module.module_id}="{tooltip_id}"' not in content:
            tooltip_issues.append(f"Missing tooltip: {tooltip_id}")
    
    # Check chart functionality
    chart_checks = [
        "modelPerformanceMetricsChart",
        "accuracyComparisonChart",
        "modelEvaluationChart"
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
        logger.info("✅ Model Performance Module test successful")
        logger.info(f"📄 Generated content length: {len(content)} characters")
        return True
    else:
        logger.warning(f"⚠️ {total_issues} issues found in Model Performance Module test")
        return False


async def test_model_performance_module_defaults():
    """Test the Model Performance Module with default data."""
    logger.info("=== Testing Model Performance Module with Defaults ===")
    
    # Initialize module
    module = ModelPerformanceModule()
    
    # Test with minimal data
    test_data = {
        "model_performance": {}
    }
    
    # Generate content
    content = await module.generate_content(test_data)
    
    # Basic checks
    checks = [
        "Model Performance Metrics",
        "Accuracy Comparison",
        "Performance Analysis",
        "Model Evaluation"
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
    """Run all model performance module tests."""
    logger.info("🚀 Starting Model Performance Module Tests")
    
    # Test 1: Full functionality test
    full_test_result = await test_model_performance_module()
    
    # Test 2: Default data test
    default_test_result = await test_model_performance_module_defaults()
    
    # Summary
    logger.info("📊 Test Summary:")
    logger.info(f"  Full Test: {'✅ PASS' if full_test_result else '❌ FAIL'}")
    logger.info(f"  Default Test: {'✅ PASS' if default_test_result else '❌ FAIL'}")
    
    if full_test_result and default_test_result:
        logger.info("🎉 All Model Performance Module tests passed!")
        return True
    else:
        logger.warning("⚠️ Some Model Performance Module tests failed")
        return False


if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)
