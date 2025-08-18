"""
Export Manager

Provides multiple format export capabilities including:
- JSON export
- CSV export
- Excel export
- PDF export
- HTML export
- Markdown to PDF/Word export
"""

import json
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ExportManager:
    """Multi-format export management system."""
    
    def __init__(self, output_dir: str = "exports"):
        """Initialize the export manager.
        
        Args:
            output_dir: Directory to save exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Supported formats
        self.supported_formats = ["json", "csv", "excel", "html", "pdf", "word"]
        
        # Initialize markdown export service
        try:
            from src.core.export import MarkdownExportService
            self.markdown_service = MarkdownExportService(str(self.output_dir))
        except ImportError:
            logger.warning("Markdown export service not available")
            self.markdown_service = None
    
    def export_data(self, 
                   data: Dict[str, Any],
                   format: str = "json",
                   filename: Optional[str] = None) -> Dict[str, Any]:
        """Export data in specified format.
        
        Args:
            data: Data to export
            format: Export format
            filename: Optional custom filename
            
        Returns:
            Export result with file information
        """
        try:
            if format not in self.supported_formats:
                return {
                    "success": False,
                    "error": f"Unsupported format: {format}",
                    "message": f"Supported formats: {self.supported_formats}"
                }
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"export_{timestamp}.{format}"
            
            # Export based on format
            if format == "json":
                filepath = self._export_json(data, filename)
            elif format == "csv":
                filepath = self._export_csv(data, filename)
            elif format == "excel":
                filepath = self._export_excel(data, filename)
            elif format == "html":
                filepath = self._export_html(data, filename)
            else:
                return {
                    "success": False,
                    "error": f"Format not implemented: {format}",
                    "message": "Format export not available"
                }
            
            return {
                "success": True,
                "filename": filename,
                "filepath": str(filepath),
                "format": format,
                "size": filepath.stat().st_size,
                "message": f"Data exported successfully to {filename}"
            }
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to export data"
            }
    
    def _export_json(self, data: Dict[str, Any], filename: str) -> Path:
        """Export data as JSON."""
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return filepath
    
    def _export_csv(self, data: Dict[str, Any], filename: str) -> Path:
        """Export data as CSV."""
        filepath = self.output_dir / filename
        
        # Flatten data for CSV export
        flattened_data = self._flatten_data(data)
        
        if flattened_data:
            # Get all unique keys
            all_keys = set()
            for item in flattened_data:
                all_keys.update(item.keys())
            
            # Write CSV
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                writer.writeheader()
                writer.writerows(flattened_data)
        
        return filepath
    
    def _export_excel(self, data: Dict[str, Any], filename: str) -> Path:
        """Export data as Excel."""
        filepath = self.output_dir / filename
        
        # Convert data to pandas DataFrame(s)
        if isinstance(data, dict):
            # Create multiple sheets for different data types
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, sheet_data in data.items():
                    if isinstance(sheet_data, list):
                        df = pd.DataFrame(sheet_data)
                    elif isinstance(sheet_data, dict):
                        df = pd.DataFrame([sheet_data])
                    else:
                        df = pd.DataFrame({"value": [sheet_data]})
                    
                    # Truncate sheet name if too long
                    safe_sheet_name = str(sheet_name)[:31]
                    df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
        else:
            # Single DataFrame
            df = pd.DataFrame(data)
            df.to_excel(filepath, index=False)
        
        return filepath
    
    def _export_html(self, data: Dict[str, Any], filename: str) -> Path:
        """Export data as HTML."""
        filepath = self.output_dir / filename
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Export</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Data Export</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        # Convert data to HTML
        html_content += self._data_to_html(data)
        
        html_content += "</body></html>"
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def _flatten_data(self, data: Any) -> List[Dict[str, Any]]:
        """Flatten nested data structure for CSV export."""
        if isinstance(data, list):
            flattened = []
            for item in data:
                if isinstance(item, dict):
                    flattened.append(self._flatten_dict(item))
                else:
                    flattened.append({"value": str(item)})
            return flattened
        elif isinstance(data, dict):
            return [self._flatten_dict(data)]
        else:
            return [{"value": str(data)}]
    
    def _flatten_dict(self, data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Flatten nested dictionary."""
        flattened = {}
        for key, value in data.items():
            new_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                flattened.update(self._flatten_dict(value, new_key))
            elif isinstance(value, list):
                # Convert list to string for CSV
                flattened[new_key] = str(value)
            else:
                flattened[new_key] = value
        
        return flattened
    
    def _data_to_html(self, data: Any) -> str:
        """Convert data to HTML representation."""
        if isinstance(data, dict):
            html = "<div class='section'>"
            for key, value in data.items():
                html += f"<h3>{key}</h3>"
                html += self._data_to_html(value)
            html += "</div>"
            return html
        elif isinstance(data, list):
            if data and isinstance(data[0], dict):
                # Create table for list of dictionaries
                html = "<table>"
                # Headers
                headers = list(data[0].keys())
                html += "<tr>"
                for header in headers:
                    html += f"<th>{header}</th>"
                html += "</tr>"
                # Rows
                for item in data:
                    html += "<tr>"
                    for header in headers:
                        html += f"<td>{item.get(header, '')}</td>"
                    html += "</tr>"
                html += "</table>"
                return html
            else:
                # Simple list
                html = "<ul>"
                for item in data:
                    html += f"<li>{item}</li>"
                html += "</ul>"
                return html
        else:
            return f"<p>{data}</p>"
    
    def list_exports(self) -> List[Dict[str, Any]]:
        """List all exported files.
        
        Returns:
            List of export metadata
        """
        exports = []
        for filepath in self.output_dir.glob("*.*"):
            if filepath.suffix in ['.json', '.csv', '.xlsx', '.html']:
                exports.append({
                    "filename": filepath.name,
                    "path": str(filepath),
                    "format": filepath.suffix[1:],
                    "size": filepath.stat().st_size,
                    "created": datetime.fromtimestamp(filepath.stat().st_ctime).isoformat()
                })
        return exports
    
    def get_export(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get a specific export by filename.
        
        Args:
            filename: Name of the export file
            
        Returns:
            Export content or None if not found
        """
        filepath = self.output_dir / filename
        if not filepath.exists():
            return None
        
        try:
            if filepath.suffix == '.json':
                with open(filepath, 'r') as f:
                    return json.load(f)
            elif filepath.suffix == '.csv':
                df = pd.read_csv(filepath)
                return df.to_dict('records')
            elif filepath.suffix == '.xlsx':
                df = pd.read_excel(filepath)
                return df.to_dict('records')
            else:
                with open(filepath, 'r') as f:
                    return {"content": f.read(), "format": filepath.suffix[1:]}
        except Exception as e:
            logger.error(f"Error reading export {filename}: {e}")
            return None
    
    async def export_markdown_to_pdf(self,
                                   markdown_content: str,
                                   output_filename: Optional[str] = None,
                                   template_name: str = "whitepaper",
                                   custom_template: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to PDF.
        
        Args:
            markdown_content: Markdown content to export
            output_filename: Optional custom output filename
            template_name: Template to use for styling
            custom_template: Optional custom template configuration
            
        Returns:
            Export result dictionary
        """
        if not self.markdown_service:
            return {
                "success": False,
                "error": "Markdown export service not available",
                "message": "Markdown export requires additional dependencies"
            }
        
        try:
            result = await self.markdown_service.export_markdown_to_pdf(
                markdown_content,
                output_filename,
                template_name,
                custom_template
            )
            return result
        except Exception as e:
            logger.error(f"Error exporting markdown to PDF: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Markdown to PDF export failed"
            }
    
    async def export_markdown_to_word(self,
                                    markdown_content: str,
                                    output_filename: Optional[str] = None,
                                    template_name: str = "whitepaper",
                                    custom_template: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to Word document.
        
        Args:
            markdown_content: Markdown content to export
            output_filename: Optional custom output filename
            template_name: Template to use for styling
            custom_template: Optional custom template configuration
            
        Returns:
            Export result dictionary
        """
        if not self.markdown_service:
            return {
                "success": False,
                "error": "Markdown export service not available",
                "message": "Markdown export requires additional dependencies"
            }
        
        try:
            result = await self.markdown_service.export_markdown_to_word(
                markdown_content,
                output_filename,
                template_name,
                custom_template
            )
            return result
        except Exception as e:
            logger.error(f"Error exporting markdown to Word: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Markdown to Word export failed"
            }
    
    async def export_markdown_to_both(self,
                                    markdown_content: str,
                                    output_filename: Optional[str] = None,
                                    template_name: str = "whitepaper",
                                    custom_template: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Export markdown content to both PDF and Word documents.
        
        Args:
            markdown_content: Markdown content to export
            output_filename: Optional custom output filename (without extension)
            template_name: Template to use for styling
            custom_template: Optional custom template configuration
            
        Returns:
            Export result dictionary
        """
        if not self.markdown_service:
            return {
                "success": False,
                "error": "Markdown export service not available",
                "message": "Markdown export requires additional dependencies"
            }
        
        try:
            result = await self.markdown_service.export_markdown_to_both(
                markdown_content,
                output_filename,
                template_name,
                custom_template
            )
            return result
        except Exception as e:
            logger.error(f"Error exporting markdown to both formats: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Markdown to both formats export failed"
            }
    
    def get_export_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of an export operation.
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            Status dictionary or None if not found
        """
        if not self.markdown_service:
            return None
        
        return self.markdown_service.get_export_status(operation_id)
    
    def cancel_export(self, operation_id: str) -> bool:
        """Cancel an export operation.
        
        Args:
            operation_id: Operation identifier
            
        Returns:
            True if cancelled, False if not found
        """
        if not self.markdown_service:
            return False
        
        return self.markdown_service.cancel_export(operation_id)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List available templates.
        
        Returns:
            List of template information
        """
        if not self.markdown_service:
            return []
        
        return self.markdown_service.list_templates()
    
    def create_custom_template(self, 
                             template_name: str,
                             template_config: Dict[str, Any]) -> bool:
        """Create a custom template.
        
        Args:
            template_name: Name for the template
            template_config: Template configuration
            
        Returns:
            True if successful, False otherwise
        """
        if not self.markdown_service:
            return False
        
        return self.markdown_service.create_custom_template(template_name, template_config)
