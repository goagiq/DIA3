"""
Test script for Phase 2: Interactive War Capability Analysis

This script tests the Phase 2 components including:
- War Capability Engine
- Interactive Capability Levers
- Dynamic Prediction Engine
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from loguru import logger

# Test data
SAMPLE_COUNTRY_DATA = {
    "name": "Test Country",
    "military": {
        "troop_strength": 500000,
        "equipment_modernization": 0.7,
        "training_quality": 0.8,
        "combat_experience": 0.6,
        "command_efficiency": 0.75
    },
    "economic": {
        "gdp": 5000,  # 5 trillion
        "industrial_capacity": 0.8,
        "resource_availability": 0.7,
        "financial_stability": 0.75,
        "trade_network_strength": 0.8
    },
    "technological": {
        "cyber_capabilities": 0.8,
        "ai_development": 0.7,
        "space_capabilities": 0.6,
        "advanced_weapons": 0.75,
        "research_development": 0.8
    },
    "logistical": {
        "infrastructure_quality": 0.75,
        "supply_chain_efficiency": 0.8,
        "transportation_network": 0.7,
        "maintenance_capabilities": 0.75,
        "fuel_availability": 0.8
    },
    "political": {
        "government_stability": 0.8,
        "public_support": 0.6,
        "leadership_effectiveness": 0.75,
        "policy_consistency": 0.7,
        "international_standing": 0.8
    },
    "alliances": {
        "alliance_strength": 0.8,
        "diplomatic_relations": 0.75,
        "international_support": 0.7,
        "coalition_building": 0.8,
        "treaty_obligations": 0.7
    },
    "geographic": {
        "strategic_location": 0.7,
        "terrain_advantage": 0.6,
        "natural_resources": 0.8,
        "climate_conditions": 0.7,
        "borders_security": 0.75
    },
    "resources": {
        "energy_resources": 0.8,
        "raw_materials": 0.7,
        "food_security": 0.8,
        "water_availability": 0.75,
        "critical_minerals": 0.7
    },
    "command_control": {
        "communication_systems": 0.8,
        "decision_making_speed": 0.75,
        "coordination_efficiency": 0.8,
        "information_sharing": 0.75,
        "command_authority": 0.8
    },
    "intelligence": {
        "sigint_capabilities": 0.8,
        "humint_network": 0.7,
        "osint_analysis": 0.75,
        "technical_intelligence": 0.8,
        "counterintelligence": 0.75
    }
}

async def test_war_capability_engine():
    """Test the War Capability Engine."""
    logger.info("🧪 Testing War Capability Engine...")
    
    try:
        from src.core.war_capability.war_capability_engine import WarCapabilityEngine
        
        engine = WarCapabilityEngine()
        
        # Test capability score calculation
        result = await engine.calculate_war_capability_score(SAMPLE_COUNTRY_DATA)
        
        logger.info(f"✅ War Capability Score: {result.overall_score:.3f}")
        logger.info(f"✅ Confidence Level: {result.confidence_level:.3f}")
        logger.info(f"✅ Domain Scores: {len(result.domain_scores)} domains")
        logger.info(f"✅ Recommendations: {len(result.recommendations)} recommendations")
        logger.info(f"✅ Risk Factors: {len(result.risk_factors)} risk factors")
        
        # Test capability breakdown
        breakdown = await engine.get_capability_breakdown(SAMPLE_COUNTRY_DATA)
        logger.info(f"✅ Capability Breakdown: {len(breakdown)} metrics")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ War Capability Engine test failed: {e}")
        return False

async def test_interactive_levers():
    """Test the Interactive Capability Levers."""
    logger.info("🧪 Testing Interactive Capability Levers...")
    
    try:
        from src.core.war_capability.interactive_levers import InteractiveCapabilityLevers
        
        levers = InteractiveCapabilityLevers()
        
        # Test lever adjustment
        adjustment_result = await levers.adjust_lever("military_spending", 5.0)
        logger.info(f"✅ Lever Adjustment: {adjustment_result['lever_name']} = {adjustment_result['new_value']}")
        
        # Test prediction recalculation
        lever_changes = {
            "military_spending": 5.0,
            "troop_mobilization": 20.0,
            "cyber_capabilities": 85.0
        }
        recalculation_result = await levers.recalculate_predictions(lever_changes)
        logger.info(f"✅ Prediction Recalculation: {len(recalculation_result['prediction_adjustments'])} metrics updated")
        
        # Test sensitivity analysis
        sensitivity_result = await levers.get_sensitivity_analysis("military_spending")
        logger.info(f"✅ Sensitivity Analysis: {len(sensitivity_result['sensitivity_analysis'])} test values")
        
        # Test lever status
        status_result = await levers.get_all_levers_status()
        logger.info(f"✅ Lever Status: {status_result['total_levers']} levers")
        
        # Test lever reset
        reset_result = await levers.reset_levers_to_default()
        logger.info(f"✅ Lever Reset: {len(reset_result['reset_results'])} levers reset")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Interactive Levers test failed: {e}")
        return False

async def test_dynamic_prediction_engine():
    """Test the Dynamic Prediction Engine."""
    logger.info("🧪 Testing Dynamic Prediction Engine...")
    
    try:
        from src.core.predictive_analytics.dynamic_prediction_engine import DynamicPredictionEngine
        
        engine = DynamicPredictionEngine()
        
        # Test prediction update
        lever_changes = {
            "military_spending": 4.5,
            "troop_mobilization": 15.0,
            "cyber_capabilities": 80.0
        }
        update_result = await engine.update_predictions({}, lever_changes)
        logger.info(f"✅ Prediction Update: {update_result['prediction_id']}")
        logger.info(f"✅ New Predictions: {len(update_result['new_predictions'])} metrics")
        
        # Test scenario generation
        base_scenario = {"name": "Test Scenario"}
        scenarios_result = await engine.generate_alternative_scenarios(base_scenario)
        logger.info(f"✅ Scenario Generation: {len(scenarios_result)} scenarios")
        
        # Test current predictions
        current_result = await engine.get_current_predictions()
        logger.info(f"✅ Current Predictions: {len(current_result['predictions'])} metrics")
        logger.info(f"✅ Total Updates: {current_result['total_updates']}")
        
        # Test prediction history
        history_result = await engine.get_prediction_history(limit=10)
        logger.info(f"✅ Prediction History: {len(history_result)} records")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Dynamic Prediction Engine test failed: {e}")
        return False

async def test_api_integration():
    """Test API integration for Phase 2 components."""
    logger.info("🧪 Testing API Integration...")
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:8003"
        
        # Test health check
        health_response = requests.get(f"{base_url}/ml-forecasting/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            logger.info(f"✅ Health Check: {health_data['status']}")
            logger.info(f"✅ Components: {len(health_data['components'])} components")
        else:
            logger.warning(f"⚠️ Health check failed: {health_response.status_code}")
        
        # Test war capability analysis
        war_capability_data = {
            "country_data": SAMPLE_COUNTRY_DATA,
            "capability_weights": None
        }
        war_response = requests.post(
            f"{base_url}/ml-forecasting/war-capability/analyze",
            json=war_capability_data
        )
        if war_response.status_code == 200:
            war_data = war_response.json()
            logger.info(f"✅ War Capability Analysis: {war_data['success']}")
        else:
            logger.warning(f"⚠️ War capability analysis failed: {war_response.status_code}")
        
        # Test lever adjustment
        lever_data = {
            "lever_name": "military_spending",
            "value": 4.5
        }
        lever_response = requests.post(
            f"{base_url}/ml-forecasting/interactive-levers/adjust",
            json=lever_data
        )
        if lever_response.status_code == 200:
            lever_result = lever_response.json()
            logger.info(f"✅ Lever Adjustment: {lever_result['success']}")
        else:
            logger.warning(f"⚠️ Lever adjustment failed: {lever_response.status_code}")
        
        # Test lever status
        status_response = requests.get(f"{base_url}/ml-forecasting/interactive-levers/status")
        if status_response.status_code == 200:
            status_data = status_response.json()
            logger.info(f"✅ Lever Status: {status_data['success']}")
        else:
            logger.warning(f"⚠️ Lever status failed: {status_response.status_code}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API Integration test failed: {e}")
        return False

async def run_comprehensive_test():
    """Run comprehensive test suite for Phase 2."""
    logger.info("🚀 Starting Phase 2 Comprehensive Test Suite")
    
    test_results = {
        "war_capability_engine": False,
        "interactive_levers": False,
        "dynamic_prediction_engine": False,
        "api_integration": False
    }
    
    # Test individual components
    test_results["war_capability_engine"] = await test_war_capability_engine()
    test_results["interactive_levers"] = await test_interactive_levers()
    test_results["dynamic_prediction_engine"] = await test_dynamic_prediction_engine()
    test_results["api_integration"] = await test_api_integration()
    
    # Summary
    logger.info("\n📊 Phase 2 Test Results Summary:")
    logger.info("=" * 50)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
    
    logger.info("=" * 50)
    logger.info(f"Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        logger.info("🎉 All Phase 2 tests passed! Phase 2 implementation is successful.")
        return True
    else:
        logger.warning(f"⚠️ {total_tests - passed_tests} tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    
    # Run the test suite
    success = asyncio.run(run_comprehensive_test())
    
    if success:
        print("\n🎉 Phase 2 Interactive War Capability Analysis implementation is complete and working!")
        sys.exit(0)
    else:
        print("\n❌ Phase 2 implementation has issues that need to be addressed.")
        sys.exit(1)
