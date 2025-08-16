#!/usr/bin/env python3
"""
Test script for Multi-Domain Strategic Analysis functionality.
Tests the new generic strategic analysis capabilities across different domains.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.multi_domain_strategic_analyzer import (
    MultiDomainStrategicAnalyzer,
    DomainType,
    AnalysisType
)


async def test_multi_domain_analyzer():
    """Test the multi-domain strategic analyzer functionality."""
    
    print("🧪 Testing Multi-Domain Strategic Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = MultiDomainStrategicAnalyzer()
    
    # Test 1: Get supported domains
    print("\n1. Testing supported domains...")
    try:
        domains = await analyzer.get_supported_domains()
        print(f"✅ Found {len(domains)} supported domains:")
        for domain in domains:
            print(f"   - {domain['domain']}: {len(domain['key_metrics'])} metrics")
        print("✅ Domain capabilities test passed")
    except Exception as e:
        print(f"❌ Domain capabilities test failed: {e}")
        return False
    
    # Test 2: Business domain analysis
    print("\n2. Testing business domain analysis...")
    try:
        business_content = "Analyze our business strategic position in current market conditions including competitive landscape, market opportunities, and strategic recommendations"
        
        result = await analyzer.analyze_strategic_position(
            content=business_content,
            domain=DomainType.BUSINESS,
            analysis_type=AnalysisType.COMPREHENSIVE,
            include_art_of_war=True,
            include_recommendations=True
        )
        
        print(f"✅ Business analysis completed")
        print(f"   - Domain: {result['metadata']['domain']}")
        print(f"   - Analysis type: {result['metadata']['analysis_type']}")
        print(f"   - Components analyzed: {len(result['domain_analysis'])}")
        print(f"   - Recommendations: {len(result.get('strategic_recommendations', []))}")
        print("✅ Business domain test passed")
    except Exception as e:
        print(f"❌ Business domain test failed: {e}")
        return False
    
    # Test 3: Defense domain analysis
    print("\n3. Testing defense domain analysis...")
    try:
        defense_content = "Analyze our defense strategic position including threat assessment, capability gaps, and alliance strength"
        
        result = await analyzer.analyze_strategic_position(
            content=defense_content,
            domain=DomainType.DEFENSE,
            analysis_type=AnalysisType.RISK,
            include_art_of_war=True,
            include_recommendations=True
        )
        
        print(f"✅ Defense analysis completed")
        print(f"   - Domain: {result['metadata']['domain']}")
        print(f"   - Analysis type: {result['metadata']['analysis_type']}")
        print(f"   - Components analyzed: {len(result['domain_analysis'])}")
        print(f"   - Recommendations: {len(result.get('strategic_recommendations', []))}")
        print("✅ Defense domain test passed")
    except Exception as e:
        print(f"❌ Defense domain test failed: {e}")
        return False
    
    # Test 4: Intelligence domain analysis
    print("\n4. Testing intelligence domain analysis...")
    try:
        intelligence_content = "Analyze our intelligence capabilities including information asymmetry, deception detection, and source protection"
        
        result = await analyzer.analyze_strategic_position(
            content=intelligence_content,
            domain=DomainType.INTELLIGENCE,
            analysis_type=AnalysisType.DECEPTION,
            include_art_of_war=True,
            include_recommendations=True
        )
        
        print(f"✅ Intelligence analysis completed")
        print(f"   - Domain: {result['metadata']['domain']}")
        print(f"   - Analysis type: {result['metadata']['analysis_type']}")
        print(f"   - Components analyzed: {len(result['domain_analysis'])}")
        print(f"   - Art of War techniques: {len(result.get('art_of_war_analysis', {}).get('techniques', {}))}")
        print("✅ Intelligence domain test passed")
    except Exception as e:
        print(f"❌ Intelligence domain test failed: {e}")
        return False
    
    # Test 5: Cybersecurity domain analysis
    print("\n5. Testing cybersecurity domain analysis...")
    try:
        cybersecurity_content = "Analyze our cybersecurity posture including threat detection, incident response, and security automation"
        
        result = await analyzer.analyze_strategic_position(
            content=cybersecurity_content,
            domain=DomainType.CYBERSECURITY,
            analysis_type=AnalysisType.THREAT,
            include_art_of_war=True,
            include_recommendations=True
        )
        
        print(f"✅ Cybersecurity analysis completed")
        print(f"   - Domain: {result['metadata']['domain']}")
        print(f"   - Analysis type: {result['metadata']['analysis_type']}")
        print(f"   - Components analyzed: {len(result['domain_analysis'])}")
        print(f"   - Risk categories: {len(result.get('risk_categories', []))}")
        print("✅ Cybersecurity domain test passed")
    except Exception as e:
        print(f"❌ Cybersecurity domain test failed: {e}")
        return False
    
    # Test 6: Geopolitical domain analysis
    print("\n6. Testing geopolitical domain analysis...")
    try:
        geopolitical_content = "Analyze our geopolitical position including alliance strength, diplomatic relations, and economic leverage"
        
        result = await analyzer.analyze_strategic_position(
            content=geopolitical_content,
            domain=DomainType.GEOPOLITICAL,
            analysis_type=AnalysisType.COMPETITIVE,
            include_art_of_war=True,
            include_recommendations=True
        )
        
        print(f"✅ Geopolitical analysis completed")
        print(f"   - Domain: {result['metadata']['domain']}")
        print(f"   - Analysis type: {result['metadata']['analysis_type']}")
        print(f"   - Components analyzed: {len(result['domain_analysis'])}")
        print(f"   - Strategic principles: {len(result.get('strategic_principles', []))}")
        print("✅ Geopolitical domain test passed")
    except Exception as e:
        print(f"❌ Geopolitical domain test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All multi-domain strategic analysis tests passed!")
    return True


async def test_api_endpoints():
    """Test the API endpoints for multi-domain strategic analysis."""
    
    print("\n🌐 Testing Multi-Domain Strategic Analysis API Endpoints")
    print("=" * 60)
    
    import httpx
    
    base_url = "http://localhost:8004"
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/multi-domain/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                print(f"   - Supported domains: {data['supported_domains']}")
                print(f"   - Analysis types: {len(data['analysis_types'])}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Get supported domains
    print("\n2. Testing get supported domains...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/multi-domain/domains")
            if response.status_code == 200:
                domains = response.json()
                print(f"✅ Get domains passed: {len(domains)} domains")
                for domain in domains[:3]:  # Show first 3
                    print(f"   - {domain['domain']}")
            else:
                print(f"❌ Get domains failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Get domains failed: {e}")
        return False
    
    # Test 3: Business strategic analysis
    print("\n3. Testing business strategic analysis...")
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "content": "Analyze our business strategic position in current market conditions",
                "analysis_type": "comprehensive",
                "include_art_of_war": True,
                "include_recommendations": True
            }
            response = await client.post(
                f"{base_url}/multi-domain/business-strategic-analysis",
                json=payload
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Business analysis passed")
                print(f"   - Domain: {data['domain']}")
                print(f"   - Analysis type: {data['analysis_type']}")
                print(f"   - Success: {data['success']}")
            else:
                print(f"❌ Business analysis failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Business analysis failed: {e}")
        return False
    
    # Test 4: Defense strategic analysis
    print("\n4. Testing defense strategic analysis...")
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "content": "Analyze our defense strategic position including threat assessment",
                "analysis_type": "risk",
                "include_art_of_war": True,
                "include_recommendations": True
            }
            response = await client.post(
                f"{base_url}/multi-domain/defense-strategic-analysis",
                json=payload
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Defense analysis passed")
                print(f"   - Domain: {data['domain']}")
                print(f"   - Analysis type: {data['analysis_type']}")
                print(f"   - Success: {data['success']}")
            else:
                print(f"❌ Defense analysis failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Defense analysis failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All API endpoint tests passed!")
    return True


async def main():
    """Main test function."""
    
    print("🚀 Multi-Domain Strategic Analysis Test Suite")
    print("=" * 60)
    
    # Test core functionality
    core_success = await test_multi_domain_analyzer()
    
    if core_success:
        # Test API endpoints (only if core tests pass)
        api_success = await test_api_endpoints()
        
        if api_success:
            print("\n🎉 All tests passed! Multi-domain strategic analysis is working correctly.")
            return True
        else:
            print("\n❌ API endpoint tests failed.")
            return False
    else:
        print("\n❌ Core functionality tests failed.")
        return False


if __name__ == "__main__":
    # Run tests
    success = asyncio.run(main())
    
    if success:
        print("\n✅ Test suite completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test suite failed!")
        sys.exit(1)
