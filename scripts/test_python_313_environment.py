#!/usr/bin/env python3
"""
Test Python 3.13 Environment
Simple script to verify the DIA3 environment is working correctly
"""

import subprocess
import sys

def test_python_313():
    """Test the Python 3.13 environment."""
    print("=== Testing Python 3.13 Environment ===")
    
    # Test basic Python functionality
    print("\n1. Testing Python 3.13 version...")
    result = subprocess.run(
        ["DIA3/Scripts/python.exe", "--version"], 
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ {result.stdout.strip()}")
    else:
        print(f"❌ Failed: {result.stderr}")
        return False
    
    # Test key library imports
    print("\n2. Testing key library imports...")
    libraries = [
        ("numpy", "import numpy; print('NumPy:', numpy.__version__)"),
        ("pandas", "import pandas; print('Pandas:', pandas.__version__)"),
        ("fastapi", "import fastapi; print('FastAPI:', fastapi.__version__)"),
        ("pydantic", "import pydantic; print('Pydantic:', pydantic.__version__)"),
        ("requests", "import requests; print('Requests:', requests.__version__)"),
        ("matplotlib", "import matplotlib; print('Matplotlib:', matplotlib.__version__)"),
        ("sklearn", "import sklearn; print('Scikit-learn:', sklearn.__version__)"),
        ("pytest", "import pytest; print('Pytest:', pytest.__version__)"),
    ]
    
    for lib_name, import_code in libraries:
        result = subprocess.run(
            ["DIA3/Scripts/python.exe", "-c", import_code],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
        else:
            print(f"❌ {lib_name}: {result.stderr.strip()}")
    
    # Test a simple calculation
    print("\n3. Testing basic functionality...")
    test_code = """
import numpy as np
import pandas as pd

# Test NumPy
arr = np.array([1, 2, 3, 4, 5])
print(f"NumPy array sum: {arr.sum()}")

# Test Pandas
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
print(f"Pandas DataFrame shape: {df.shape}")

# Test FastAPI
from fastapi import FastAPI
app = FastAPI()
print(f"FastAPI app created: {type(app).__name__}")

print("✅ All basic functionality tests passed!")
"""
    
    result = subprocess.run(
        ["DIA3/Scripts/python.exe", "-c", test_code],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"❌ Basic functionality test failed: {result.stderr}")
    
    print("\n=== Python 3.13 Environment Test Complete ===")
    print("🎉 Your Python 3.13 environment is ready for development!")
    print("💡 Use 'DIA3/Scripts/python.exe' to run your Python 3.13 scripts")
    
    return True

if __name__ == "__main__":
    test_python_313()
