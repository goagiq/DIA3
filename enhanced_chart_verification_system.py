#!/usr/bin/env python3
"""
Enhanced Chart Verification System

This script verifies comprehensive consistency between:
1. Chart types and text descriptions
2. Storytelling/analysis and chart data insights
3. Content accuracy and data visualization alignment
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.enhanced_html_report_generator import EnhancedHTMLReportGenerator

class EnhancedChartVerifier:
    """Comprehensive chart verification system."""
    
    def __init__(self):
        self.chart_type_mappings = {
            "Executive Summary": "doughnut",
            "Geopolitical Impact Analysis": "polarArea", 
            "Trade and Economic Impact": "line",
            "Security Implications": "radar",
            "Balance of Power Analysis": "bar",
            "Strategic Analysis": "line",
            "Enhanced Data Analysis": "scatter",
            "Regional Sentiment Analysis": "pie",
            "Implementation Timeline": "line",
            "Acquisition Programs & Modernization": "bar",
            "Forecasting & Predictive Analytics": "line",
            "Operational Considerations": "radar",
            "Regional Security Dynamics": "bar",
            "Economic Cost Analysis": "line",
            "Comparison Analysis & Strategic Options": "radar",
            "Advanced Forecasting Analysis": "line",
            "Forecast Model Performance Comparison": "bar",
            "Strategic Capability Forecasts": "radar",
            "Predictive Analytics & Feature Importance": "bar",
            "Scenario Prediction Analysis": "line"
        }
        
        # Define expected data patterns for each chart type
        self.chart_data_patterns = {
            "doughnut": {
                "description_keywords": ["highest-scoring", "relative importance", "quantitative assessment", "key drivers"],
                "data_characteristics": ["percentage", "proportion", "distribution", "breakdown"]
            },
            "radar": {
                "description_keywords": ["highest-scoring", "strongest", "robust", "capabilities", "assessment"],
                "data_characteristics": ["multi-dimensional", "comparative", "capability", "performance"]
            },
            "line": {
                "description_keywords": ["trend", "peak", "stabilization", "growth", "timeline", "progression"],
                "data_characteristics": ["temporal", "sequential", "trending", "continuous"]
            },
            "bar": {
                "description_keywords": ["comparison", "highest", "strongest", "performance", "ranking"],
                "data_characteristics": ["categorical", "comparative", "ranking", "discrete"]
            },
            "pie": {
                "description_keywords": ["distribution", "breakdown", "composition", "proportion", "share"],
                "data_characteristics": ["percentage", "proportion", "composition", "parts"]
            },
            "scatter": {
                "description_keywords": ["correlation", "relationship", "pattern", "distribution", "clustering"],
                "data_characteristics": ["correlation", "relationship", "scattered", "patterned"]
            },
            "polarArea": {
                "description_keywords": ["multi-dimensional", "radial", "comprehensive", "holistic"],
                "data_characteristics": ["radial", "multi-dimensional", "comprehensive"]
            }
        }
        
        self.generator = EnhancedHTMLReportGenerator()
    
    def verify_chart_consistency(self, html_file: str) -> Dict[str, Any]:
        """Comprehensive chart consistency verification."""
        print(f"🔍 Verifying comprehensive chart consistency in: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            "type_consistency": [],
            "content_consistency": [],
            "data_insight_alignment": [],
            "storytelling_accuracy": [],
            "total_issues": 0,
            "total_charts": len(self.chart_type_mappings)
        }
        
        # Check each module's chart
        for module, expected_type in self.chart_type_mappings.items():
            module_results = self._verify_module_consistency(
                module, expected_type, content
            )
            
            # Aggregate results
            for key in ["type_consistency", "content_consistency", "data_insight_alignment", "storytelling_accuracy"]:
                if module_results[key]:
                    results[key].append(module_results[key])
                    results["total_issues"] += 1
        
        return results
    
    def _verify_module_consistency(self, module: str, expected_type: str, content: str) -> Dict[str, Any]:
        """Verify consistency for a specific module."""
        results = {
            "module": module,
            "type_consistency": None,
            "content_consistency": None,
            "data_insight_alignment": None,
            "storytelling_accuracy": None
        }
        
        # 1. Chart Type Consistency
        chart_pattern = rf'// {re.escape(module)} Chart.*?type: \'([^\']+)\''
        chart_match = re.search(chart_pattern, content, re.DOTALL)
        
        if chart_match:
            actual_type = chart_match.group(1)
            if actual_type != expected_type:
                results["type_consistency"] = {
                    "status": "❌ Mismatch",
                    "expected": expected_type,
                    "actual": actual_type,
                    "issue": f"Chart type mismatch: expected {expected_type}, got {actual_type}"
                }
            else:
                results["type_consistency"] = {
                    "status": "✅ Consistent",
                    "type": actual_type
                }
        else:
            results["type_consistency"] = {
                "status": "❌ Missing",
                "issue": "Chart not found in HTML"
            }
        
        # 2. Content Consistency Check
        content_consistency = self._verify_content_consistency(module, expected_type, content)
        if content_consistency:
            results["content_consistency"] = content_consistency
        
        # 3. Data Insight Alignment
        data_alignment = self._verify_data_insight_alignment(module, expected_type, content)
        if data_alignment:
            results["data_insight_alignment"] = data_alignment
        
        # 4. Storytelling Accuracy
        storytelling_accuracy = self._verify_storytelling_accuracy(module, expected_type, content)
        if storytelling_accuracy:
            results["storytelling_accuracy"] = storytelling_accuracy
        
        return results
    
    def _verify_content_consistency(self, module: str, chart_type: str, content: str) -> Dict[str, Any]:
        """Verify that content descriptions match chart type expectations."""
        # Find the module's content section
        module_pattern = rf'<h3[^>]*>{re.escape(module)}</h3>(.*?)(?=<h3|$)'
        module_match = re.search(module_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not module_match:
            return {
                "status": "❌ Missing Content",
                "issue": f"Module content section not found for {module}"
            }
        
        module_content = module_match.group(1)
        
        # Get expected keywords for this chart type
        expected_patterns = self.chart_data_patterns.get(chart_type, {})
        expected_keywords = expected_patterns.get("description_keywords", [])
        
        # Check if content contains appropriate keywords
        found_keywords = []
        missing_keywords = []
        
        for keyword in expected_keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', module_content, re.IGNORECASE):
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Check for inappropriate keywords (keywords from other chart types)
        inappropriate_keywords = []
        for other_type, patterns in self.chart_data_patterns.items():
            if other_type != chart_type:
                for keyword in patterns.get("description_keywords", []):
                    if re.search(rf'\b{re.escape(keyword)}\b', module_content, re.IGNORECASE):
                        inappropriate_keywords.append(f"{keyword} (from {other_type})")
        
        issues = []
        if missing_keywords:
            issues.append(f"Missing expected keywords: {', '.join(missing_keywords)}")
        if inappropriate_keywords:
            issues.append(f"Inappropriate keywords found: {', '.join(inappropriate_keywords)}")
        
        if issues:
            return {
                "status": "❌ Content Inconsistency",
                "found_keywords": found_keywords,
                "missing_keywords": missing_keywords,
                "inappropriate_keywords": inappropriate_keywords,
                "issues": issues
            }
        else:
            return {
                "status": "✅ Content Consistent",
                "found_keywords": found_keywords
            }
    
    def _verify_data_insight_alignment(self, module: str, chart_type: str, content: str) -> Dict[str, Any]:
        """Verify that data insights align with chart type and content."""
        # Find chart data
        chart_data_pattern = rf'// {re.escape(module)} Chart.*?data: \[([^\]]+)\]'
        chart_data_match = re.search(chart_data_pattern, content, re.DOTALL)
        
        if not chart_data_match:
            return {
                "status": "❌ Missing Data",
                "issue": "Chart data not found"
            }
        
        try:
            # Extract data values
            data_str = chart_data_match.group(1)
            data_values = [int(x.strip()) for x in data_str.split(',') if x.strip().isdigit()]
            
            if not data_values:
                return {
                    "status": "❌ Invalid Data",
                    "issue": "No valid numeric data found"
                }
            
            # Analyze data characteristics
            data_analysis = self._analyze_data_characteristics(data_values, chart_type)
            
            # Find insights mentioned in content
            insight_pattern = rf'<strong>Visualization Insight:</strong>(.*?)(?=<strong|$)'
            insight_match = re.search(insight_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if not insight_match:
                return {
                    "status": "❌ Missing Insights",
                    "issue": "No visualization insights found",
                    "data_analysis": data_analysis
                }
            
            insight_text = insight_match.group(1).strip()
            
            # Check if insights align with data
            alignment_issues = self._check_insight_data_alignment(
                insight_text, data_analysis, chart_type
            )
            
            if alignment_issues:
                return {
                    "status": "❌ Insight-Data Misalignment",
                    "issues": alignment_issues,
                    "data_analysis": data_analysis,
                    "insight_text": insight_text
                }
            else:
                return {
                    "status": "✅ Insight-Data Aligned",
                    "data_analysis": data_analysis
                }
                
        except Exception as e:
            return {
                "status": "❌ Data Analysis Error",
                "issue": f"Error analyzing data: {str(e)}"
            }
    
    def _analyze_data_characteristics(self, data_values: List[int], chart_type: str) -> Dict[str, Any]:
        """Analyze characteristics of the data."""
        if not data_values:
            return {"error": "No data values"}
        
        analysis = {
            "count": len(data_values),
            "min": min(data_values),
            "max": max(data_values),
            "range": max(data_values) - min(data_values),
            "avg": sum(data_values) / len(data_values),
            "highest_values": sorted(data_values, reverse=True)[:3],
            "lowest_values": sorted(data_values)[:3]
        }
        
        # Add chart-type specific analysis
        if chart_type == "line":
            analysis["trend"] = "increasing" if data_values[-1] > data_values[0] else "decreasing"
        elif chart_type in ["doughnut", "pie"]:
            analysis["total"] = sum(data_values)
            analysis["percentages"] = [round(v/sum(data_values)*100, 1) for v in data_values]
        
        return analysis
    
    def _check_insight_data_alignment(self, insight_text: str, data_analysis: Dict[str, Any], chart_type: str) -> List[str]:
        """Check if insights align with actual data."""
        issues = []
        
        # Check for specific value mentions
        highest_value = data_analysis.get("highest_values", [0])[0]
        lowest_value = data_analysis.get("lowest_values", [0])[0]
        
        # Look for specific percentage mentions
        if chart_type in ["doughnut", "pie"]:
            percentages = data_analysis.get("percentages", [])
            if percentages:
                highest_pct = max(percentages)
                # Check if insight mentions the highest percentage
                if f"{highest_pct}%" in insight_text:
                    # Verify it's actually the highest
                    if highest_pct != max(percentages):
                        issues.append(f"Insight mentions {highest_pct}% but actual highest is {max(percentages)}%")
        
        # Check for trend descriptions in line charts
        if chart_type == "line":
            trend = data_analysis.get("trend", "")
            if "increasing" in insight_text.lower() and trend != "increasing":
                issues.append("Insight mentions increasing trend but data shows decreasing")
            elif "decreasing" in insight_text.lower() and trend != "decreasing":
                issues.append("Insight mentions decreasing trend but data shows increasing")
        
        # Check for highest/lowest value mentions
        if f"{highest_value}" in insight_text:
            # Verify it's actually mentioned as highest
            if "highest" in insight_text.lower() or "strongest" in insight_text.lower():
                pass  # This is good
            else:
                issues.append(f"Insight mentions {highest_value} but doesn't identify it as highest/strongest")
        
        return issues
    
    def _verify_storytelling_accuracy(self, module: str, chart_type: str, content: str) -> Dict[str, Any]:
        """Verify that storytelling accurately reflects the chart's purpose and data."""
        # Find the module's content section
        module_pattern = rf'<h3[^>]*>{re.escape(module)}</h3>(.*?)(?=<h3|$)'
        module_match = re.search(module_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not module_match:
            return {
                "status": "❌ Missing Content",
                "issue": "Module content not found"
            }
        
        module_content = module_match.group(1)
        
        # Define storytelling expectations for each module type
        storytelling_expectations = {
            "Executive Summary": {
                "required_elements": ["comprehensive", "strategic", "key findings", "critical insights"],
                "chart_purpose": "overview and summary"
            },
            "Security Implications": {
                "required_elements": ["security", "threat", "capability", "deterrence"],
                "chart_purpose": "security assessment"
            },
            "Economic Cost Analysis": {
                "required_elements": ["cost", "economic", "investment", "financial"],
                "chart_purpose": "economic analysis"
            }
        }
        
        expectations = storytelling_expectations.get(module, {
            "required_elements": ["analysis", "assessment", "evaluation"],
            "chart_purpose": "general analysis"
        })
        
        # Check for required storytelling elements
        missing_elements = []
        for element in expectations["required_elements"]:
            if not re.search(rf'\b{re.escape(element)}\b', module_content, re.IGNORECASE):
                missing_elements.append(element)
        
        # Check for chart purpose alignment
        chart_purpose = expectations["chart_purpose"]
        purpose_alignment = self._check_purpose_alignment(module_content, chart_purpose, chart_type)
        
        issues = []
        if missing_elements:
            issues.append(f"Missing required storytelling elements: {', '.join(missing_elements)}")
        if purpose_alignment:
            issues.append(purpose_alignment)
        
        if issues:
            return {
                "status": "❌ Storytelling Issues",
                "issues": issues,
                "expected_purpose": chart_purpose
            }
        else:
            return {
                "status": "✅ Storytelling Accurate",
                "purpose": chart_purpose
            }
    
    def _check_purpose_alignment(self, content: str, expected_purpose: str, chart_type: str) -> str:
        """Check if content aligns with expected chart purpose."""
        # This is a simplified check - in a real implementation, you might use NLP
        # to analyze semantic alignment between content and chart purpose
        
        purpose_keywords = {
            "overview and summary": ["overview", "summary", "comprehensive", "overall"],
            "security assessment": ["security", "threat", "defense", "capability"],
            "economic analysis": ["economic", "cost", "financial", "investment"],
            "general analysis": ["analysis", "assessment", "evaluation", "examination"]
        }
        
        expected_keywords = purpose_keywords.get(expected_purpose, [])
        found_keywords = []
        
        for keyword in expected_keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', content, re.IGNORECASE):
                found_keywords.append(keyword)
        
        if not found_keywords:
            return f"Content doesn't align with expected purpose: {expected_purpose}"
        
        return None  # No alignment issue
    
    async def generate_test_report(self) -> str:
        """Generate a test report for comprehensive verification."""
        print("📊 Generating comprehensive test report...")
        
        test_data = {
            "title": "Enhanced Chart Verification Test Report",
            "subtitle": "Comprehensive Chart-Text-Data Alignment Verification",
            "topic": "Enhanced Verification Analysis",
            "analysis_type": "verification",
            "confidence_score": 0.95,
            "source_metadata": [
                {
                    "source_type": "verification",
                    "source_name": "Enhanced Chart Verifier",
                    "title": "Comprehensive Alignment Test",
                    "confidence": 0.95,
                    "reliability_score": 0.95,
                    "timestamp": "2025-01-26 12:00"
                }
            ],
            "content": "This is a comprehensive test report to verify chart-text-data alignment and storytelling accuracy."
        }
        
        result = await self.generator.generate_enhanced_report(
            data=test_data,
            output_path="Results/enhanced_chart_verification_test.html"
        )
        
        if result["success"]:
            return result["file_path"]
        else:
            raise Exception(f"Failed to generate test report: {result.get('error')}")

async def main():
    """Main verification function."""
    print("🔍 Enhanced Chart Verification System")
    print("=" * 60)
    print("Verifying: Chart Types, Content Consistency, Data Insights, Storytelling")
    print("=" * 60)
    
    verifier = EnhancedChartVerifier()
    
    try:
        # Generate test report
        test_file = await verifier.generate_test_report()
        print(f"✅ Test report generated: {test_file}")
        
        # Run comprehensive verification
        results = verifier.verify_chart_consistency(test_file)
        
        print(f"\n📊 Comprehensive Verification Results:")
        print(f"   Total Charts: {results['total_charts']}")
        print(f"   Total Issues: {results['total_issues']}")
        
        # Report type consistency issues
        type_issues = [r for r in results['type_consistency'] if r.get('status', '').startswith('❌')]
        if type_issues:
            print(f"\n❌ Chart Type Issues ({len(type_issues)}):")
            for issue in type_issues:
                print(f"   • {issue['module']}: {issue.get('issue', 'Unknown issue')}")
        
        # Report content consistency issues
        content_issues = [r for r in results['content_consistency'] if r.get('status', '').startswith('❌')]
        if content_issues:
            print(f"\n❌ Content Consistency Issues ({len(content_issues)}):")
            for issue in content_issues:
                print(f"   • {issue['module']}: {', '.join(issue.get('issues', []))}")
        
        # Report data insight alignment issues
        data_issues = [r for r in results['data_insight_alignment'] if r.get('status', '').startswith('❌')]
        if data_issues:
            print(f"\n❌ Data Insight Alignment Issues ({len(data_issues)}):")
            for issue in data_issues:
                print(f"   • {issue['module']}: {', '.join(issue.get('issues', []))}")
        
        # Report storytelling accuracy issues
        storytelling_issues = [r for r in results['storytelling_accuracy'] if r.get('status', '').startswith('❌')]
        if storytelling_issues:
            print(f"\n❌ Storytelling Accuracy Issues ({len(storytelling_issues)}):")
            for issue in storytelling_issues:
                print(f"   • {issue['module']}: {', '.join(issue.get('issues', []))}")
        
        if results['total_issues'] == 0:
            print(f"\n✅ All verifications passed! Charts are fully consistent.")
        else:
            print(f"\n⚠️ Found {results['total_issues']} issues requiring attention.")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
