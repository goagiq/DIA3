#!/usr/bin/env python3
"""
Test with faster Ollama models to avoid hanging issues.
"""

import asyncio
from loguru import logger

def test_fast_ollama_model():
    """Test with a faster Ollama model."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        from strands_tools import calculator
        
        # Try faster models in order of preference
        fast_models = [
            "phi3:mini",           # Very fast, small model
            "llama3:latest",       # Fast, good quality
            "llama3.1:8b",         # Fast 8B model
            "gemma3:latest"        # Fast Gemma model
        ]
        
        for model_name in fast_models:
            try:
                logger.info(f"Testing with model: {model_name}")
                
                # Create Ollama model with fast configuration
                ollama_model = OllamaModel(
                    host="http://localhost:11434",
                    model_id=model_name,
                    temperature=0.3,  # Lower temperature for faster responses
                    streaming=False,  # Disable streaming to avoid hanging
                    max_tokens=100    # Limit tokens for faster response
                )
                
                # Create agent with fast model and calculator tool
                agent = Agent(
                    name="fast_test_agent",
                    system_prompt="You are a helpful assistant. Keep responses brief.",
                    model=ollama_model,
                    tools=[calculator]
                )
                
                logger.info(f"✅ Successfully created agent with {model_name}")
                return agent, model_name
                
            except Exception as e:
                logger.warning(f"⚠️ Failed with {model_name}: {e}")
                continue
        
        logger.error("❌ All fast models failed")
        return None, None
        
    except Exception as e:
        logger.error(f"❌ Error creating fast model agent: {e}")
        return None, None

async def test_fast_agent_invocation():
    """Test if fast agent can be invoked quickly."""
    try:
        from strands import Agent
        from strands.models.ollama import OllamaModel
        from strands_tools import calculator
        
        # Use the fastest available model
        fast_models = ["phi3:mini", "llama3:latest", "llama3.1:8b"]
        
        for model_name in fast_models:
            try:
                logger.info(f"Testing invocation with: {model_name}")
                
                # Create Ollama model with fast configuration
                ollama_model = OllamaModel(
                    host="http://localhost:11434",
                    model_id=model_name,
                    temperature=0.3,
                    streaming=False,
                    max_tokens=50  # Very short response for speed
                )
                
                # Create agent with fast model
                agent = Agent(
                    name="fast_test_agent",
                    system_prompt="You are a helpful assistant. Keep responses brief.",
                    model=ollama_model,
                    tools=[calculator]
                )
                
                # Test with a very simple prompt
                logger.info("Testing fast agent invocation...")
                result = await asyncio.wait_for(
                    agent.invoke_async("Say hello briefly."),
                    timeout=15.0  # 15 second timeout
                )
                
                logger.info(f"✅ Fast agent invocation successful with {model_name}: {result[:100]}...")
                return True, model_name
                
            except asyncio.TimeoutError:
                logger.warning(f"⚠️ Timeout with {model_name}")
                continue
            except Exception as e:
                logger.warning(f"⚠️ Failed with {model_name}: {e}")
                continue
        
        logger.error("❌ All fast models failed or timed out")
        return False, None
        
    except Exception as e:
        logger.error(f"❌ Error testing fast agent invocation: {e}")
        return False, None

def main():
    """Run all tests."""
    logger.info("🚀 Fast Model Test Suite")
    logger.info("=" * 50)
    
    # Test 1: Fast model creation
    logger.info("1. Testing fast model creation...")
    agent, model_name = test_fast_ollama_model()
    if not agent:
        logger.error("❌ Fast model creation failed")
        return
    
    logger.info(f"✅ Successfully using model: {model_name}")
    
    # Test 2: Fast agent invocation
    logger.info("2. Testing fast agent invocation...")
    success, working_model = asyncio.run(test_fast_agent_invocation())
    
    if success:
        logger.info(f"✅ Fast agent invocation successful with {working_model}")
        logger.info("🎉 Fast model is working! Use this model for Strands integration.")
    else:
        logger.error("❌ Fast agent invocation failed")
    
    logger.info("✅ All tests completed!")

if __name__ == "__main__":
    main()
