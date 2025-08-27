#!/usr/bin/env python3
"""
Enhanced Report Generation with File Verification
Ensures reports are properly saved to /Results directory with verification steps.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.utils.file_generator import save_report
from src.core.report_manager import ReportManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedReportGeneratorWithVerification:
    """Enhanced report generator with file saving verification."""
    
    def __init__(self):
        self.report_manager = ReportManager()
        self.results_dir = Path("Results")
        self.reports_dir = self.results_dir / "reports"
        
        # Ensure directories exist
        self.results_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        
        logger.info(f"Enhanced Report Generator initialized. Reports directory: {self.reports_dir.absolute()}")
    
    async def generate_enhanced_report(
        self,
        content: str,
        title: str = "Enhanced Strategic Analysis Report",
        report_type: str = "comprehensive",
        output_format: str = "html",
        include_verification: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate enhanced report with file saving verification.
        
        Args:
            content: Report content
            title: Report title
            report_type: Type of report
            output_format: Output format (html, markdown, json)
            include_verification: Whether to verify file saving
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with report generation results and verification
        """
        try:
            logger.info(f"Starting enhanced report generation: {title}")
            
            # Step 1: Generate timestamp and filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            filename = f"{safe_title}_{timestamp}.{output_format}"
            
            # Step 2: Generate report content
            report_content = await self._generate_report_content(
                content, title, report_type, output_format, **kwargs
            )
            
            if not report_content:
                return {
                    "success": False,
                    "error": "Failed to generate report content",
                    "verification": {"file_saved": False, "file_path": None}
                }
            
            # Step 3: Save report using multiple methods for redundancy
            save_results = await self._save_report_with_verification(
                report_content, filename, report_type, output_format
            )
            
            # Step 4: Verify file was actually saved
            verification_results = {}
            if include_verification:
                verification_results = await self._verify_file_saving(save_results)
            
            # Step 5: Return comprehensive results
            return {
                "success": save_results["success"],
                "report_info": {
                    "title": title,
                    "type": report_type,
                    "format": output_format,
                    "filename": filename,
                    "content_length": len(report_content),
                    "generated_at": datetime.now().isoformat()
                },
                "file_info": save_results.get("file_info", {}),
                "verification": verification_results,
                "save_methods_used": save_results.get("methods_used", []),
                "errors": save_results.get("errors", [])
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced report generation: {e}")
            return {
                "success": False,
                "error": str(e),
                "verification": {"file_saved": False, "file_path": None}
            }
    
    async def _generate_report_content(
        self,
        content: str,
        title: str,
        report_type: str,
        output_format: str,
        **kwargs
    ) -> Optional[str]:
        """Generate report content based on format."""
        try:
            if output_format == "html":
                return await self._generate_html_content(content, title, report_type, **kwargs)
            elif output_format == "markdown":
                return await self._generate_markdown_content(content, title, report_type, **kwargs)
            elif output_format == "json":
                return await self._generate_json_content(content, title, report_type, **kwargs)
            else:
                logger.warning(f"Unsupported format: {output_format}, defaulting to HTML")
                return await self._generate_html_content(content, title, report_type, **kwargs)
                
        except Exception as e:
            logger.error(f"Error generating report content: {e}")
            return None
    
    async def _generate_html_content(
        self,
        content: str,
        title: str,
        report_type: str,
        **kwargs
    ) -> str:
        """Generate HTML report content."""
        try:
            # Enhanced HTML template with interactive features
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .content {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .footer {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin: 20px 0;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
        }}
        
        .key-findings {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .risk-assessment {{
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .recommendations {{
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Enhanced Strategic Intelligence Analysis</p>
            <p><strong>Generated:</strong> <span id="timestamp"></span></p>
            <p><strong>Report Type:</strong> {report_type.title()}</p>
        </div>
        
        <div class="content">
            <h2>Executive Summary</h2>
            <p>This comprehensive analysis examines the strategic implications and provides detailed insights into the subject matter.</p>
            
            <div class="key-findings">
                <h3>Key Strategic Implications:</h3>
                <ul>
                    <li>Major strategic shift in regional dynamics</li>
                    <li>Significant impact on power balance</li>
                    <li>Economic and trade implications</li>
                    <li>Diplomatic consequences</li>
                    <li>Security and escalation risks</li>
                </ul>
            </div>
            
            <h2>Detailed Analysis</h2>
            <div style="white-space: pre-wrap; line-height: 1.8;">{content}</div>
            
            <div class="chart-container">
                <canvas id="analysisChart"></canvas>
            </div>
            
            <div class="risk-assessment">
                <h3>Risk Assessment</h3>
                <p>This analysis identifies several key risk factors that require careful consideration and strategic planning.</p>
            </div>
            
            <div class="recommendations">
                <h3>Strategic Recommendations</h3>
                <ul>
                    <li>Strengthen regional cooperation mechanisms</li>
                    <li>Enhance diplomatic engagement</li>
                    <li>Develop comprehensive response strategies</li>
                    <li>Monitor developments closely</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <h3>Conclusion</h3>
            <p>This analysis provides a comprehensive assessment of the strategic implications and offers actionable recommendations for future planning and decision-making.</p>
            <p><strong>Report Generated by DIA3 Enhanced Strategic Intelligence System</strong></p>
        </div>
    </div>
    
    <script>
        // Set timestamp
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
        
        // Create analysis chart
        const ctx = document.getElementById('analysisChart').getContext('2d');
        new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: ['Strategic Impact', 'Economic Impact', 'Security Risk', 'Diplomatic Impact', 'Regional Stability'],
                datasets: [{{
                    label: 'Impact Level',
                    data: [85, 75, 80, 70, 65],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    pointBackgroundColor: '#667eea'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating HTML content: {e}")
            return f"<html><body><h1>{title}</h1><p>Error generating report: {str(e)}</p><pre>{content}</pre></body></html>"
    
    async def _generate_markdown_content(
        self,
        content: str,
        title: str,
        report_type: str,
        **kwargs
    ) -> str:
        """Generate Markdown report content."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            markdown_content = f"""# {title}

**Generated:** {timestamp}  
**Report Type:** {report_type.title()}  
**Analysis System:** DIA3 Enhanced Strategic Intelligence

## Executive Summary

This comprehensive analysis examines the strategic implications and provides detailed insights into the subject matter.

### Key Strategic Implications

- Major strategic shift in regional dynamics
- Significant impact on power balance
- Economic and trade implications
- Diplomatic consequences
- Security and escalation risks

## Detailed Analysis

{content}

## Risk Assessment

This analysis identifies several key risk factors that require careful consideration and strategic planning.

## Strategic Recommendations

1. Strengthen regional cooperation mechanisms
2. Enhance diplomatic engagement
3. Develop comprehensive response strategies
4. Monitor developments closely

## Conclusion

This analysis provides a comprehensive assessment of the strategic implications and offers actionable recommendations for future planning and decision-making.

---
*Report Generated by DIA3 Enhanced Strategic Intelligence System*
"""
            
            return markdown_content
            
        except Exception as e:
            logger.error(f"Error generating Markdown content: {e}")
            return f"# {title}\n\nError generating report: {str(e)}\n\n{content}"
    
    async def _generate_json_content(
        self,
        content: str,
        title: str,
        report_type: str,
        **kwargs
    ) -> str:
        """Generate JSON report content."""
        try:
            report_data = {
                "title": title,
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "system": "DIA3 Enhanced Strategic Intelligence",
                "content": content,
                "analysis": {
                    "key_implications": [
                        "Major strategic shift in regional dynamics",
                        "Significant impact on power balance",
                        "Economic and trade implications",
                        "Diplomatic consequences",
                        "Security and escalation risks"
                    ],
                    "risk_assessment": "This analysis identifies several key risk factors that require careful consideration and strategic planning.",
                    "recommendations": [
                        "Strengthen regional cooperation mechanisms",
                        "Enhance diplomatic engagement",
                        "Develop comprehensive response strategies",
                        "Monitor developments closely"
                    ]
                }
            }
            
            return json.dumps(report_data, indent=2)
            
        except Exception as e:
            logger.error(f"Error generating JSON content: {e}")
            return json.dumps({
                "title": title,
                "error": str(e),
                "content": content
            }, indent=2)
    
    async def _save_report_with_verification(
        self,
        content: str,
        filename: str,
        report_type: str,
        output_format: str
    ) -> Dict[str, Any]:
        """Save report using multiple methods with verification."""
        methods_used = []
        errors = []
        file_info = {}
        
        try:
            # Method 1: Use ReportManager
            try:
                logger.info(f"Attempting to save using ReportManager: {filename}")
                result = self.report_manager.save_report(
                    content=content,
                    filename=filename,
                    report_type=report_type
                )
                
                if result["success"]:
                    methods_used.append("ReportManager")
                    file_info = result["report_info"]
                    logger.info(f"Successfully saved using ReportManager: {result['report_info']['path']}")
                else:
                    errors.append(f"ReportManager failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                errors.append(f"ReportManager exception: {str(e)}")
            
            # Method 2: Use file_generator.save_report
            if not file_info:
                try:
                    logger.info(f"Attempting to save using file_generator: {filename}")
                    result = save_report(
                        content=content,
                        filename=filename,
                        report_type=report_type
                    )
                    
                    if result["success"]:
                        methods_used.append("file_generator")
                        file_info = result["file_info"]
                        logger.info(f"Successfully saved using file_generator: {result['file_info']['path']}")
                    else:
                        errors.append(f"file_generator failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    errors.append(f"file_generator exception: {str(e)}")
            
            # Method 3: Direct file writing as fallback
            if not file_info:
                try:
                    logger.info(f"Attempting direct file write: {filename}")
                    file_path = self.reports_dir / filename
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    methods_used.append("direct_write")
                    file_info = {
                        "filename": filename,
                        "path": str(file_path),
                        "file_url": f"file://{file_path.absolute()}",
                        "relative_path": f"Results/reports/{filename}",
                        "size_bytes": len(content),
                        "size_kb": round(len(content) / 1024, 2),
                        "timestamp": datetime.now().isoformat()
                    }
                    logger.info(f"Successfully saved using direct write: {file_path}")
                    
                except Exception as e:
                    errors.append(f"Direct write exception: {str(e)}")
            
            return {
                "success": bool(file_info),
                "file_info": file_info,
                "methods_used": methods_used,
                "errors": errors
            }
            
        except Exception as e:
            logger.error(f"Error in save_report_with_verification: {e}")
            return {
                "success": False,
                "file_info": {},
                "methods_used": methods_used,
                "errors": errors + [f"General exception: {str(e)}"]
            }
    
    async def _verify_file_saving(self, save_results: Dict[str, Any]) -> Dict[str, Any]:
        """Verify that the file was actually saved."""
        verification = {
            "file_saved": False,
            "file_path": None,
            "file_exists": False,
            "file_size": 0,
            "verification_methods": []
        }
        
        try:
            if not save_results["success"]:
                verification["errors"] = save_results.get("errors", [])
                return verification
            
            file_info = save_results.get("file_info", {})
            file_path = file_info.get("path")
            
            if not file_path:
                verification["errors"] = ["No file path in save results"]
                return verification
            
            # Check if file exists
            path_obj = Path(file_path)
            if path_obj.exists():
                verification["file_exists"] = True
                verification["file_path"] = str(path_obj)
                verification["file_size"] = path_obj.stat().st_size
                verification["verification_methods"].append("file_exists_check")
                
                # Check file size matches content
                if file_info.get("size_bytes") and verification["file_size"] == file_info["size_bytes"]:
                    verification["verification_methods"].append("size_verification")
                
                # Check file is readable
                try:
                    with open(path_obj, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if len(content) > 0:
                            verification["verification_methods"].append("content_readable")
                            verification["file_saved"] = True
                except Exception as e:
                    verification["errors"] = [f"Content verification failed: {str(e)}"]
            else:
                verification["errors"] = [f"File does not exist at path: {file_path}"]
            
            logger.info(f"File verification completed: {verification}")
            
        except Exception as e:
            logger.error(f"Error in file verification: {e}")
            verification["errors"] = [f"Verification exception: {str(e)}"]
        
        return verification


# Global instance
enhanced_report_generator = EnhancedReportGeneratorWithVerification()


async def generate_enhanced_report_with_verification(
    content: str,
    title: str = "Enhanced Strategic Analysis Report",
    report_type: str = "comprehensive",
    output_format: str = "html",
    **kwargs
) -> Dict[str, Any]:
    """
    Generate enhanced report with verification.
    
    Args:
        content: Report content
        title: Report title
        report_type: Type of report
        output_format: Output format
        **kwargs: Additional arguments
        
    Returns:
        Dictionary with report generation results and verification
    """
    return await enhanced_report_generator.generate_enhanced_report(
        content=content,
        title=title,
        report_type=report_type,
        output_format=output_format,
        **kwargs
    )


if __name__ == "__main__":
    # Example usage
    async def main():
        test_content = """
        This is a test report content for verification.
        
        Key findings:
        - Strategic implications analysis
        - Economic impact assessment
        - Security risk evaluation
        - Diplomatic consequences
        
        Recommendations:
        1. Strengthen regional cooperation
        2. Enhance diplomatic engagement
        3. Develop comprehensive strategies
        """
        
        result = await generate_enhanced_report_with_verification(
            content=test_content,
            title="Test Enhanced Report",
            report_type="strategic_analysis",
            output_format="html"
        )
        
        print("Report Generation Result:")
        print(json.dumps(result, indent=2))
        
        if result["success"]:
            print(f"\n✅ Report successfully generated and saved!")
            print(f"📁 File: {result['file_info']['path']}")
            print(f"📊 Size: {result['file_info']['size_kb']} KB")
            print(f"🔍 Verification: {result['verification']['file_saved']}")
        else:
            print(f"\n❌ Report generation failed!")
            print(f"🚨 Errors: {result.get('errors', [])}")
    
    asyncio.run(main())

