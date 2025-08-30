#!/usr/bin/env python3
"""
Simple test script for Classical Chinese HUMINT Analysis

This script tests the Classical Chinese HUMINT analysis agent directly
without requiring the API server to be running.

Usage:
    python test_classical_chinese_humint_simple.py
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from loguru import logger

# Import DIA3 components
from src.core.models import AnalysisRequest, DataType
from src.agents.classical_chinese_humint_agent import ClassicalChineseHUMINTAnalysisAgent


async def test_classical_chinese_humint_agent():
    """Test the Classical Chinese HUMINT analysis agent."""
    logger.info("🚀 Testing Classical Chinese HUMINT Analysis Agent")
    
    try:
        # Initialize agent
        agent = ClassicalChineseHUMINTAnalysisAgent()
        logger.info("✅ Agent initialized successfully")
        
        # Test content from The Art of War
        test_content = """
        孫子曰：兵者，國之大事，死生之地，存亡之道，不可不察也。
        
        故經之以五事，校之以計，而索其情：一曰道，二曰天，三曰地，四曰將，五曰法。
        
        兵者，詭道也。故能而示之不能，用而示之不用，近而示之遠，遠而示之近。
        利而誘之，亂而取之，實而備之，強而避之，怒而撓之，卑而驕之，佚而勞之，親而離之。
        攻其無備，出其不意。此兵家之勝，不可先傳也。
        
        知己知彼，百戰不殆；不知彼而知己，一勝一負；不知彼，不知己，每戰必殆。
        """
        
        # Create analysis request
        request = AnalysisRequest(
            content=test_content,
            data_type=DataType.TEXT,
            language="zh",
            metadata={
                "source_type": "test",
                "document_type": "strategic_text",
                "author": "Sun Tzu",
                "title": "The Art of War",
                "context": "strategic_communication"
            }
        )
        
        # Test agent processing
        logger.info("Processing Classical Chinese content...")
        result = await agent.process(request)
        
        # Verify results
        if result and result.metadata:
            logger.info("✅ Agent processing successful")
            
            # Extract key metrics from metadata
            analysis_results = result.metadata.get("analysis_results", {})
            classical_analysis = analysis_results.get("classical_chinese_analysis", {})
            classical_score = classical_analysis.get("classical_score", 0)
            strategic_intent = classical_analysis.get("strategic_intent", "unknown")
            formality_level = classical_analysis.get("formality_level", "unknown")
            
            humint_implications = analysis_results.get("humint_implications", {})
            source_assessment = humint_implications.get("source_assessment", {})
            deception_risk = humint_implications.get("deception_risk", {})
            
            # Print results
            print("\n" + "="*80)
            print("CLASSICAL CHINESE HUMINT ANALYSIS RESULTS")
            print("="*80)
            print(f"Classical Score: {classical_score:.2f}")
            print(f"Strategic Intent: {strategic_intent}")
            print(f"Formality Level: {formality_level}")
            print(f"Cultural Authenticity: {source_assessment.get('cultural_authenticity', 'unknown')}")
            print(f"Deception Risk Level: {deception_risk.get('risk_level', 'unknown')}")
            
            # Print strategic indicators
            strategic_indicators = classical_analysis.get("strategic_indicators", [])
            if strategic_indicators:
                print(f"\nStrategic Indicators Found: {len(strategic_indicators)}")
                for indicator in strategic_indicators:
                    print(f"  - {indicator['text']} ({indicator['type']})")
            
            # Print cultural values
            cultural_values = classical_analysis.get("cultural_values", [])
            if cultural_values:
                print(f"\nCultural Values Found: {len(cultural_values)}")
                for value in cultural_values:
                    print(f"  - {value['value']}")
            
            # Print recommendations
            recommendations = analysis_results.get("recommendations", [])
            if recommendations:
                print(f"\nOperational Recommendations:")
                for rec in recommendations:
                    print(f"  - [{rec['priority'].upper()}] {rec['category']}: {rec['recommendation']}")
            
            print("="*80)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = Path(f"Results/classical_chinese_humint_simple_test_{timestamp}.json")
            
            results_file.parent.mkdir(exist_ok=True)
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📄 Results saved to: {results_file}")
            
            # Generate and save report
            report = agent.generate_report(analysis_results)
            report_file = Path(f"Results/classical_chinese_humint_report_{timestamp}.md")
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"📄 Report saved to: {report_file}")
            
            return {
                "success": True,
                "classical_score": classical_score,
                "strategic_intent": strategic_intent,
                "deception_risk_level": deception_risk.get("risk_level", "unknown"),
                "cultural_authenticity": source_assessment.get("cultural_authenticity", "unknown"),
                "strategic_indicators_count": len(strategic_indicators),
                "cultural_values_count": len(cultural_values),
                "recommendations_count": len(recommendations)
            }
        else:
            logger.error("❌ Agent processing failed - no results returned")
            return {"success": False, "error": "No results returned"}
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """Main test function."""
    logger.info("🚀 Starting Classical Chinese HUMINT Simple Test")
    
    try:
        # Run test
        result = await test_classical_chinese_humint_agent()
        
        if result.get("success", False):
            logger.info("✅ Test completed successfully")
            
            # Print summary
            print("\n" + "="*80)
            print("TEST SUMMARY")
            print("="*80)
            print(f"Status: ✅ PASS")
            print(f"Classical Score: {result['classical_score']:.2f}")
            print(f"Strategic Intent: {result['strategic_intent']}")
            print(f"Deception Risk: {result['deception_risk_level']}")
            print(f"Cultural Authenticity: {result['cultural_authenticity']}")
            print(f"Strategic Indicators: {result['strategic_indicators_count']}")
            print(f"Cultural Values: {result['cultural_values_count']}")
            print(f"Recommendations: {result['recommendations_count']}")
            print("="*80)
        else:
            logger.error("❌ Test failed")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
