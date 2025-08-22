"""
Enhanced Report API Routes
Provides endpoints for generating enhanced reports with beautiful styling and advanced analytics.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.models import (
    EnhancedReportRequest, ReportComponent, MonteCarloConfig,
    StressTestConfig, VisualizationConfig, KnowledgeGraphConfig
)
from src.core.enhanced_report_orchestrator import EnhancedReportOrchestrator

router = APIRouter(prefix="/api/v1/enhanced-reports", tags=["Enhanced Reports"])

# Global orchestrator instance
enhanced_report_orchestrator = None

def get_enhanced_report_orchestrator():
    """Get or create the enhanced report orchestrator."""
    global enhanced_report_orchestrator
    if enhanced_report_orchestrator is None:
        enhanced_report_orchestrator = EnhancedReportOrchestrator()
    return enhanced_report_orchestrator

class EnhancedReportRequestModel(BaseModel):
    """Request model for enhanced report generation."""
    query: str = Field(..., description="Analysis query or topic")
    components: Optional[List[str]] = Field(
        default=[
            "executive_summary", "comparative_analysis", "impact_analysis",
            "predictive_analysis", "monte_carlo_simulation", "stress_testing",
            "risk_assessment", "knowledge_graph", "interactive_visualizations"
        ],
        description="Report components to include"
    )
    monte_carlo_config: Optional[Dict[str, Any]] = Field(
        default={
            "iterations": 20000,
            "scenarios": ["baseline", "optimistic", "pessimistic"],
            "confidence_level": 0.95
        },
        description="Monte Carlo simulation configuration"
    )
    stress_test_config: Optional[Dict[str, Any]] = Field(
        default={
            "scenarios": ["worst_case", "average_case", "best_case"],
            "severity_levels": ["low", "medium", "high"],
            "time_periods": [1, 3, 6, 12]
        },
        description="Stress testing configuration"
    )
    visualization_config: Optional[Dict[str, Any]] = Field(
        default={
            "chart_types": ["line", "bar", "scatter", "heatmap"],
            "interactive": True,
            "export_formats": ["png", "svg", "html"]
        },
        description="Visualization configuration"
    )
    knowledge_graph_config: Optional[Dict[str, Any]] = Field(
        default={
            "entity_types": ["military", "strategic", "economic"],
            "relationship_types": ["alliance", "competition", "dependency"],
            "centrality_metrics": ["degree", "betweenness", "closeness"]
        },
        description="Knowledge graph configuration"
    )

class EnhancedReportResponse(BaseModel):
    """Response model for enhanced report generation."""
    success: bool
    report_id: str
    processing_time: float
    html_file: Optional[str] = None
    markdown_file: Optional[str] = None
    json_file: Optional[str] = None
    timestamp: str
    message: str

@router.get("/health")
async def health_check():
    """Health check for enhanced report service."""
    try:
        orchestrator = get_enhanced_report_orchestrator()
        return {
            "status": "healthy",
            "service": "enhanced_report_service",
            "timestamp": datetime.now().isoformat(),
            "orchestrator_available": orchestrator is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.post("/generate", response_model=EnhancedReportResponse)
async def generate_enhanced_report(request: EnhancedReportRequestModel):
    """Generate an enhanced report with beautiful styling and advanced analytics."""
    try:
        print(f"🚀 Generating Enhanced Report: {request.query}")
        
        # Get orchestrator
        orchestrator = get_enhanced_report_orchestrator()
        if not orchestrator:
            raise HTTPException(status_code=500, detail="Enhanced report orchestrator not available")
        
        # Convert components to ReportComponent enum
        components = []
        for comp in request.components:
            try:
                components.append(ReportComponent(comp))
            except ValueError:
                print(f"Warning: Unknown component {comp}, skipping")
        
        # Create enhanced report request
        enhanced_request = EnhancedReportRequest(
            query=request.query,
            components=components,
            monte_carlo_config=MonteCarloConfig(**request.monte_carlo_config) if request.monte_carlo_config else None,
            stress_test_config=StressTestConfig(**request.stress_test_config) if request.stress_test_config else None,
            visualization_config=VisualizationConfig(**request.visualization_config) if request.visualization_config else None,
            knowledge_graph_config=KnowledgeGraphConfig(**request.knowledge_graph_config) if request.knowledge_graph_config else None
        )
        
        # Generate enhanced report
        start_time = datetime.now()
        result = await orchestrator.generate_report(enhanced_request)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Generate beautiful HTML report
        from Test.enhanced_report_with_original_styling import EnhancedReportWithOriginalStyling
        
        generator = EnhancedReportWithOriginalStyling()
        html_content = generator._generate_beautiful_html_report(result, processing_time)
        
        # Save report files
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_dir = Path("Results")
        results_dir.mkdir(exist_ok=True)
        
        # Save HTML file
        html_filename = f"enhanced_report_{timestamp}.html"
        html_path = results_dir / html_filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save JSON metadata
        json_filename = f"enhanced_report_{timestamp}.json"
        json_path = results_dir / json_filename
        metadata = {
            "report_id": result.request_id,
            "query": request.query,
            "processing_time": processing_time,
            "timestamp": timestamp,
            "components_generated": result.components_generated,
            "status": result.status
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return EnhancedReportResponse(
            success=True,
            report_id=result.request_id,
            processing_time=processing_time,
            html_file=str(html_path),
            json_file=str(json_path),
            timestamp=datetime.now().isoformat(),
            message=f"Enhanced report generated successfully in {processing_time:.2f} seconds"
        )
        
    except Exception as e:
        print(f"❌ Error generating enhanced report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate enhanced report: {str(e)}")

@router.post("/generate-beautiful", response_model=EnhancedReportResponse)
async def generate_beautiful_enhanced_report(request: EnhancedReportRequestModel):
    """Generate an enhanced report with the beautiful original styling."""
    try:
        print(f"🎨 Generating Beautiful Enhanced Report: {request.query}")
        
        # Import the beautiful report generator
        from Test.enhanced_report_with_original_styling import EnhancedReportWithOriginalStyling
        
        # Create generator and generate report
        generator = EnhancedReportWithOriginalStyling()
        result = await generator.generate_enhanced_report()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail="Failed to generate beautiful enhanced report")
        
        # Save the report
        saved_file = generator.save_enhanced_report(
            result["html_content"], 
            "enhanced_beautiful_report"
        )
        
        return EnhancedReportResponse(
            success=True,
            report_id=result["report_id"],
            processing_time=result["processing_time"],
            html_file=saved_file,
            timestamp=result["timestamp"],
            message="Beautiful enhanced report generated successfully"
        )
        
    except Exception as e:
        print(f"❌ Error generating beautiful enhanced report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate beautiful enhanced report: {str(e)}")

@router.post("/generate-with-tooltips", response_model=EnhancedReportResponse)
async def generate_enhanced_report_with_tooltips(request: EnhancedReportRequestModel):
    """Generate an enhanced report with interactive tooltips."""
    try:
        print(f"🔍 Generating Enhanced Report with Tooltips: {request.query}")
        
        # Import the tooltip-enhanced report generator
        from src.core.enhanced_report_with_tooltips import EnhancedReportWithTooltips
        
        # Create generator and generate report
        generator = EnhancedReportWithTooltips()
        result = await generator.generate_enhanced_report()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail="Failed to generate enhanced report with tooltips")
        
        # Save the report
        saved_file = generator.save_enhanced_report(
            result["html_content"], 
            "enhanced_report_with_tooltips"
        )
        
        return EnhancedReportResponse(
            success=True,
            report_id=result["report_id"],
            processing_time=result["processing_time"],
            html_file=saved_file,
            timestamp=result["timestamp"],
            message="Enhanced report with tooltips generated successfully"
        )
        
    except Exception as e:
        print(f"❌ Error generating enhanced report with tooltips: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate enhanced report with tooltips: {str(e)}")

@router.get("/reports")
async def list_enhanced_reports():
    """List all generated enhanced reports."""
    try:
        results_dir = Path("Results")
        if not results_dir.exists():
            return {"reports": []}
        
        reports = []
        for file_path in results_dir.glob("enhanced_*_*.html"):
            # Extract timestamp from filename
            filename = file_path.name
            if "_" in filename:
                parts = filename.split("_")
                if len(parts) >= 3:
                    timestamp = f"{parts[-2]}_{parts[-1].replace('.html', '')}"
                    reports.append({
                        "filename": filename,
                        "timestamp": timestamp,
                        "path": str(file_path),
                        "size": file_path.stat().st_size if file_path.exists() else 0
                    })
        
        return {"reports": sorted(reports, key=lambda x: x["timestamp"], reverse=True)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list reports: {str(e)}")

@router.get("/reports/{report_id}")
async def get_enhanced_report(report_id: str):
    """Get a specific enhanced report by ID."""
    try:
        results_dir = Path("Results")
        
        # Look for HTML file with the report ID
        html_files = list(results_dir.glob(f"*{report_id}*.html"))
        if not html_files:
            raise HTTPException(status_code=404, detail="Report not found")
        
        html_file = html_files[0]
        
        # Read the HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        return {
            "report_id": report_id,
            "html_content": html_content,
            "filename": html_file.name,
            "path": str(html_file)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get report: {str(e)}")

@router.delete("/reports/{report_id}")
async def delete_enhanced_report(report_id: str):
    """Delete a specific enhanced report by ID."""
    try:
        results_dir = Path("Results")
        
        # Find all files with the report ID
        files_to_delete = []
        for pattern in [f"*{report_id}*.html", f"*{report_id}*.json", f"*{report_id}*.md"]:
            files_to_delete.extend(results_dir.glob(pattern))
        
        if not files_to_delete:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Delete the files
        deleted_files = []
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                deleted_files.append(file_path.name)
            except Exception as e:
                print(f"Warning: Could not delete {file_path}: {e}")
        
        return {
            "success": True,
            "report_id": report_id,
            "deleted_files": deleted_files,
            "message": f"Deleted {len(deleted_files)} files"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete report: {str(e)}")

@router.get("/capabilities")
async def get_enhanced_report_capabilities():
    """Get enhanced report generation capabilities."""
    try:
        return {
            "capabilities": {
                "sentiment_analysis": True,
                "forecasting": True,
                "predictive_analytics": True,
                "monte_carlo_simulation": True,
                "stress_testing": True,
                "knowledge_graph": True,
                "interactive_visualizations": True,
                "beautiful_styling": True
            },
            "components": [
                "executive_summary",
                "comparative_analysis", 
                "impact_analysis",
                "predictive_analysis",
                "monte_carlo_simulation",
                "stress_testing",
                "risk_assessment",
                "knowledge_graph",
                "interactive_visualizations"
            ],
            "supported_formats": ["html", "json"],
            "styling_options": ["original_beautiful", "professional", "minimal"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities: {str(e)}")
