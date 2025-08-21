"""
File Generator Utility

Provides a centralized file generation system that automatically prepends
file:///D:/AI/DIA3/ to all generated files.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import logging

from .file_path_utils import FilePathUtils

logger = logging.getLogger(__name__)


class FileGenerator:
    """Centralized file generation with automatic protocol prefix."""
    
    def __init__(self):
        """Initialize the file generator."""
        self.generated_files: List[Dict[str, Any]] = []
    
    def save_json(
        self,
        data: Any,
        filename: str,
        directory: str = "Results",
        ensure_dir: bool = True
    ) -> Dict[str, Any]:
        """
        Save data as JSON file with protocol prefix.
        
        Args:
            data: Data to save as JSON
            filename: Name of the file
            directory: Directory to save in (relative to workspace)
            ensure_dir: Whether to ensure directory exists
            
        Returns:
            Dictionary with file information including file_url
        """
        try:
            if ensure_dir:
                FilePathUtils.ensure_directory_exists(directory)
            
            file_path = os.path.join(directory, filename)
            full_path = os.path.join(FilePathUtils.WORKSPACE_BASE, file_path)
            
            # Save the file
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            # Get file info
            file_info = self._create_file_info(full_path, filename, "json")
            
            # Add to generated files list
            self.generated_files.append(file_info)
            
            logger.info(f"JSON file saved: {file_info['file_url']}")
            
            return {
                "success": True,
                "file_info": file_info,
                "message": f"JSON file saved successfully"
            }
            
        except Exception as e:
            logger.error(f"Error saving JSON file: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to save JSON file"
            }
    
    def save_text(
        self,
        content: str,
        filename: str,
        directory: str = "Results",
        ensure_dir: bool = True,
        encoding: str = "utf-8"
    ) -> Dict[str, Any]:
        """
        Save text content to file with protocol prefix.
        
        Args:
            content: Text content to save
            filename: Name of the file
            directory: Directory to save in (relative to workspace)
            ensure_dir: Whether to ensure directory exists
            encoding: File encoding
            
        Returns:
            Dictionary with file information including file_url
        """
        try:
            if ensure_dir:
                FilePathUtils.ensure_directory_exists(directory)
            
            file_path = os.path.join(directory, filename)
            full_path = os.path.join(FilePathUtils.WORKSPACE_BASE, file_path)
            
            # Save the file
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            # Get file info
            file_info = self._create_file_info(full_path, filename, "text")
            
            # Add to generated files list
            self.generated_files.append(file_info)
            
            logger.info(f"Text file saved: {file_info['file_url']}")
            
            return {
                "success": True,
                "file_info": file_info,
                "message": f"Text file saved successfully"
            }
            
        except Exception as e:
            logger.error(f"Error saving text file: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to save text file"
            }
    
    def save_binary(
        self,
        data: bytes,
        filename: str,
        directory: str = "Results",
        ensure_dir: bool = True
    ) -> Dict[str, Any]:
        """
        Save binary data to file with protocol prefix.
        
        Args:
            data: Binary data to save
            filename: Name of the file
            directory: Directory to save in (relative to workspace)
            ensure_dir: Whether to ensure directory exists
            
        Returns:
            Dictionary with file information including file_url
        """
        try:
            if ensure_dir:
                FilePathUtils.ensure_directory_exists(directory)
            
            file_path = os.path.join(directory, filename)
            full_path = os.path.join(FilePathUtils.WORKSPACE_BASE, file_path)
            
            # Save the file
            with open(full_path, 'wb') as f:
                f.write(data)
            
            # Get file info
            file_info = self._create_file_info(full_path, filename, "binary")
            
            # Add to generated files list
            self.generated_files.append(file_info)
            
            logger.info(f"Binary file saved: {file_info['file_url']}")
            
            return {
                "success": True,
                "file_info": file_info,
                "message": f"Binary file saved successfully"
            }
            
        except Exception as e:
            logger.error(f"Error saving binary file: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to save binary file"
            }
    
    def save_report(
        self,
        content: str,
        filename: str,
        report_type: str = "analysis",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save a report with protocol prefix.
        
        Args:
            content: Report content
            filename: Name of the file
            report_type: Type of report
            metadata: Additional metadata
            
        Returns:
            Dictionary with file information including file_url
        """
        try:
            # Ensure reports directory exists
            FilePathUtils.ensure_directory_exists("Results/reports")
            
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = Path(filename).stem
            extension = Path(filename).suffix
            final_filename = f"{base_name}_{timestamp}{extension}"
            
            # Save the file
            result = self.save_text(
                content=content,
                filename=final_filename,
                directory="Results/reports",
                ensure_dir=False
            )
            
            if result["success"]:
                # Add report-specific metadata
                file_info = result["file_info"]
                file_info.update({
                    "report_type": report_type,
                    "metadata": metadata or {}
                })
                
                result["file_info"] = file_info
            
            return result
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to save report"
            }
    
    def save_visualization(
        self,
        html_content: str,
        title: str,
        visualization_type: str = "interactive",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save an HTML visualization with protocol prefix.
        
        Args:
            html_content: HTML content
            title: Visualization title
            visualization_type: Type of visualization
            metadata: Additional metadata
            
        Returns:
            Dictionary with file information including file_url
        """
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            
            filename = f"{safe_title}_Visualization_{timestamp}.html"
            
            # Save the file
            result = self.save_text(
                content=html_content,
                filename=filename,
                directory="Results/reports",
                ensure_dir=False
            )
            
            if result["success"]:
                # Add visualization-specific metadata
                file_info = result["file_info"]
                file_info.update({
                    "visualization_type": visualization_type,
                    "title": title,
                    "metadata": metadata or {}
                })
                
                result["file_info"] = file_info
            
            return result
            
        except Exception as e:
            logger.error(f"Error saving visualization: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to save visualization"
            }
    
    def _create_file_info(self, full_path: str, filename: str, file_type: str) -> Dict[str, Any]:
        """Create file information dictionary."""
        file_stat = os.stat(full_path)
        
        return {
            "filename": filename,
            "path": full_path,
            "file_url": FilePathUtils.prepend_file_protocol(full_path),
            "relative_path": os.path.relpath(full_path, FilePathUtils.WORKSPACE_BASE),
            "file_type": file_type,
            "size_bytes": file_stat.st_size,
            "size_kb": round(file_stat.st_size / 1024, 2),
            "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }
    
    def get_generated_files(self) -> List[Dict[str, Any]]:
        """Get list of all generated files."""
        return self.generated_files.copy()
    
    def get_file_urls(self) -> List[str]:
        """Get list of all generated file URLs."""
        return [file_info["file_url"] for file_info in self.generated_files]


# Global instance for easy access
file_generator = FileGenerator()


# Convenience functions for backward compatibility
def save_json(data: Any, filename: str, directory: str = "Results") -> Dict[str, Any]:
    """Save data as JSON file with protocol prefix."""
    return file_generator.save_json(data, filename, directory)


def save_text(content: str, filename: str, directory: str = "Results") -> Dict[str, Any]:
    """Save text content to file with protocol prefix."""
    return file_generator.save_text(content, filename, directory)


def save_binary(data: bytes, filename: str, directory: str = "Results") -> Dict[str, Any]:
    """Save binary data to file with protocol prefix."""
    return file_generator.save_binary(data, filename, directory)


def save_report(content: str, filename: str, report_type: str = "analysis") -> Dict[str, Any]:
    """Save a report with protocol prefix."""
    return file_generator.save_report(content, filename, report_type)


def save_visualization(html_content: str, title: str) -> Dict[str, Any]:
    """Save an HTML visualization with protocol prefix."""
    return file_generator.save_visualization(html_content, title)
