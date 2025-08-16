#!/usr/bin/env python3
"""
Simple FastAPI Test Application
Demonstrates the DIA3 environment is working
"""

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import requests
from datetime import datetime

app = FastAPI(title="DIA3 Test App", version="1.0.0")

class TestData(BaseModel):
    message: str
    timestamp: datetime

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "DIA3 Environment is working!",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test-dependencies")
async def test_dependencies():
    """Test all core dependencies."""
    try:
        # Test numpy
        arr = np.array([1, 2, 3, 4, 5])
        numpy_test = f"NumPy array: {arr}, sum: {arr.sum()}"
        
        # Test pandas
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        pandas_test = f"Pandas DataFrame shape: {df.shape}"
        
        # Test requests
        response = requests.get("https://httpbin.org/json")
        requests_test = f"HTTP request status: {response.status_code}"
        
        return {
            "status": "success",
            "dependencies": {
                "numpy": numpy_test,
                "pandas": pandas_test,
                "requests": requests_test,
                "fastapi": "FastAPI is working",
                "pydantic": "Pydantic models working"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/echo")
async def echo_data(data: TestData):
    """Echo back the received data."""
    return {
        "received": data.dict(),
        "processed_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting DIA3 Test Application...")
    print("📊 Test endpoints:")
    print("  - GET  /")
    print("  - GET  /test-dependencies")
    print("  - POST /echo")
    print("\n🌐 Access the API at: http://localhost:8000")
    print("📖 API docs at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
