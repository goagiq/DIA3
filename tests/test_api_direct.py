#!/usr/bin/env python3
"""
Direct API test for ensemble forecasting
"""

import requests
import json
from datetime import datetime, timedelta
import numpy as np

BASE_URL = "http://localhost:8003"

def test_ensemble_api_direct():
    """Test the ensemble forecasting API directly"""
    print("🔍 Testing Ensemble Forecasting API Directly")
    
    # Create sample time series data
    timestamps = [datetime.now() + timedelta(hours=i) for i in range(100)]
    values = np.random.normal(100, 10, 100).tolist()
    
    request_data = {
        "training_data": {
            "timestamps": [ts.isoformat() for ts in timestamps],
            "values": values,
            "metadata": {"source": "test", "type": "numerical"}
        },
        "validation_data": {
            "timestamps": [ts.isoformat() for ts in timestamps[-20:]],
            "values": values[-20:],
            "metadata": {"source": "test", "type": "numerical"}
        },
        "horizon": 10,
        "optimize_weights": True
    }
    
    print(f"✅ Created request data with {len(values)} values")
    print(f"   Timestamps: {len(request_data['training_data']['timestamps'])}")
    print(f"   Values: {len(request_data['training_data']['values'])}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/ml-forecasting/phase3/ensemble-forecast",
            json=request_data,
            timeout=30
        )
        
        print(f"✅ API Response Status: {response.status_code}")
        print(f"✅ API Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response Success:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ API Response Error:")
            print(f"   Status: {response.status_code}")
            print(f"   Text: {response.text}")
            
            # Try to parse as JSON for better error display
            try:
                error_data = response.json()
                print(f"   JSON Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Raw Text: {response.text}")
                
    except Exception as e:
        print(f"❌ API Request Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ensemble_api_direct()
