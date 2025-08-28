#!/usr/bin/env python3
"""
Simple test to check Ollama connection.
"""

import requests
import json
from loguru import logger

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    try:
        # Test basic connection
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            logger.info(f"✅ Ollama is running. Available models: {[m['name'] for m in models.get('models', [])]}")
            return True
        else:
            logger.error(f"❌ Ollama returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to Ollama. Is it running on http://localhost:11434?")
        return False
    except Exception as e:
        logger.error(f"❌ Error connecting to Ollama: {e}")
        return False

def test_ollama_model():
    """Test if the specific model is available."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [m['name'] for m in models.get('models', [])]
            
            # Check for mistral model
            mistral_models = [m for m in model_names if 'mistral' in m.lower()]
            if mistral_models:
                logger.info(f"✅ Found Mistral models: {mistral_models}")
                return mistral_models[0]  # Return first available
            else:
                logger.warning("⚠️ No Mistral models found. Available models:")
                for model in model_names:
                    logger.info(f"   - {model}")
                return None
        else:
            logger.error(f"❌ Ollama returned status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"❌ Error checking models: {e}")
        return None

def test_ollama_generation():
    """Test if Ollama can generate text."""
    try:
        payload = {
            "model": "mistral-small3.1:latest",
            "prompt": "Hello, how are you?",
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", 
                               json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Ollama generation successful: {result.get('response', '')[:100]}...")
            return True
        else:
            logger.error(f"❌ Ollama generation failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Error testing Ollama generation: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Ollama Connection Test Suite")
    logger.info("=" * 50)
    
    # Test 1: Basic connection
    logger.info("1. Testing Ollama connection...")
    if not test_ollama_connection():
        logger.error("❌ Ollama connection failed. Please start Ollama first.")
        return
    
    # Test 2: Model availability
    logger.info("2. Testing model availability...")
    model = test_ollama_model()
    if not model:
        logger.error("❌ No suitable model found.")
        return
    
    # Test 3: Text generation
    logger.info("3. Testing text generation...")
    if not test_ollama_generation():
        logger.error("❌ Text generation failed.")
        return
    
    logger.info("✅ All Ollama tests passed!")

if __name__ == "__main__":
    main()
