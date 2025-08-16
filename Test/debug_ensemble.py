#!/usr/bin/env python3
"""
Debug script for ensemble forecasting system
"""

import asyncio
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.advanced_ml.ensemble_forecasting_system import EnsembleForecastingSystem
from core.advanced_ml.enhanced_time_series_models import TimeSeriesData

async def debug_ensemble():
    """Debug the ensemble forecasting system"""
    print("🔍 Debugging Ensemble Forecasting System")
    
    # Create sample time series data
    timestamps = np.array([datetime.now() + timedelta(hours=i) for i in range(100)])
    values = np.random.normal(0.5, 0.1, 100)  # Random values for testing
    
    ts_data = TimeSeriesData(
        timestamps=timestamps,
        values=values,
        metadata={"source": "debug", "type": "numerical"},
        data_type="numerical"
    )
    
    print(f"✅ Created test data with {len(values)} values")
    
    # Initialize ensemble system
    ensemble_system = EnsembleForecastingSystem()
    print(f"✅ Initialized ensemble system with {len(ensemble_system.base_models)} models")
    print(f"   Models: {list(ensemble_system.base_models.keys())}")
    
    # Test training
    print("\n🔍 Testing ensemble training...")
    try:
        training_result = await ensemble_system.train_ensemble(ts_data)
        print(f"✅ Training result: {training_result}")
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return
    
    # Test prediction
    print("\n🔍 Testing ensemble prediction...")
    try:
        forecast_result = await ensemble_system.predict_ensemble(ts_data, horizon=10)
        print(f"✅ Prediction successful!")
        print(f"   Predictions: {len(forecast_result.predictions)} values")
        print(f"   Confidence score: {forecast_result.confidence_score:.3f}")
        print(f"   Model weights: {forecast_result.model_weights}")
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ensemble())
