#!/usr/bin/env python3
"""
Test script to check if routes are registered in the FastAPI app
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.api.main import app
    
    print("FastAPI app routes:")
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")
        elif hasattr(route, 'routes'):
            print(f"  Router: {route}")
            for sub_route in route.routes:
                if hasattr(sub_route, 'path'):
                    print(f"    {sub_route.methods} {sub_route.path}")
    
    print("\nChecking for PDF and Word routes specifically:")
    pdf_routes = [r for r in app.routes if hasattr(r, 'path') and '/api/pdf' in str(r.path)]
    word_routes = [r for r in app.routes if hasattr(r, 'path') and '/api/word' in str(r.path)]
    
    print(f"PDF routes found: {len(pdf_routes)}")
    print(f"Word routes found: {len(word_routes)}")
    
    if pdf_routes:
        print("PDF routes:")
        for route in pdf_routes:
            print(f"  {route.methods} {route.path}")
    
    if word_routes:
        print("Word routes:")
        for route in word_routes:
            print(f"  {route.methods} {route.path}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
