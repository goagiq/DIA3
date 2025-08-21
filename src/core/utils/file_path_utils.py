"""
File Path Utilities

Provides centralized file path handling with automatic prepending of
file:///D:/AI/DIA3/ prefix for all generated files.
"""

import os
from pathlib import Path
from typing import Union, Optional
from urllib.parse import quote


class FilePathUtils:
    """Utility class for handling file paths with automatic prefix prepending."""
    
    # Base workspace path
    WORKSPACE_BASE = "D:/AI/DIA3"
    
    # File protocol prefix
    FILE_PROTOCOL_PREFIX = "file:///D:/AI/DIA3/"
    
    @classmethod
    def get_workspace_path(cls) -> Path:
        """Get the workspace base path."""
        return Path(cls.WORKSPACE_BASE)
    
    @classmethod
    def prepend_file_protocol(cls, file_path: Union[str, Path]) -> str:
        """
        Prepend file:///D:/AI/DIA3/ to a file path.
        
        Args:
            file_path: The file path to prepend the protocol to
            
        Returns:
            Full file URL with protocol prefix
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)
        
        # Convert to absolute path if relative
        if not os.path.isabs(file_path):
            # If it's a relative path, make it relative to workspace
            abs_path = os.path.join(cls.WORKSPACE_BASE, file_path)
        else:
            abs_path = file_path
        
        # Normalize the path
        normalized_path = os.path.normpath(abs_path)
        
        # Convert Windows path separators to URL format
        url_path = normalized_path.replace('\\', '/')
        
        # Ensure it starts with the correct drive letter
        if not url_path.startswith('D:/'):
            url_path = f"D:/{url_path.lstrip('/')}"
        
        # Prepend the file protocol
        return f"file:///{url_path}"
    
    @classmethod
    def create_file_path(cls, relative_path: str, filename: str) -> str:
        """
        Create a full file path with protocol prefix.
        
        Args:
            relative_path: Relative path within the workspace
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        full_path = os.path.join(relative_path, filename)
        return cls.prepend_file_protocol(full_path)
    
    @classmethod
    def get_results_path(cls, filename: str) -> str:
        """
        Get a file path in the Results directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("Results", filename)
    
    @classmethod
    def get_reports_path(cls, filename: str) -> str:
        """
        Get a file path in the Results/reports directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("Results/reports", filename)
    
    @classmethod
    def get_docs_path(cls, filename: str) -> str:
        """
        Get a file path in the docs directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("docs", filename)
    
    @classmethod
    def get_white_papers_path(cls, filename: str) -> str:
        """
        Get a file path in the docs/white_papers directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("docs/white_papers", filename)
    
    @classmethod
    def get_generated_pdfs_path(cls, filename: str) -> str:
        """
        Get a file path in the docs/white_papers/generated_pdfs directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("docs/white_papers/generated_pdfs", filename)
    
    @classmethod
    def get_cache_path(cls, filename: str) -> str:
        """
        Get a file path in the cache directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("cache", filename)
    
    @classmethod
    def get_temp_path(cls, filename: str) -> str:
        """
        Get a file path in the temp directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("temp", filename)
    
    @classmethod
    def get_logs_path(cls, filename: str) -> str:
        """
        Get a file path in the logs directory with protocol prefix.
        
        Args:
            filename: Name of the file
            
        Returns:
            Full file URL with protocol prefix
        """
        return cls.create_file_path("logs", filename)
    
    @classmethod
    def ensure_directory_exists(cls, relative_path: str) -> None:
        """
        Ensure a directory exists within the workspace.
        
        Args:
            relative_path: Relative path within the workspace
        """
        full_path = os.path.join(cls.WORKSPACE_BASE, relative_path)
        os.makedirs(full_path, exist_ok=True)
    
    @classmethod
    def is_within_workspace(cls, file_path: Union[str, Path]) -> bool:
        """
        Check if a file path is within the workspace.
        
        Args:
            file_path: The file path to check
            
        Returns:
            True if the path is within the workspace
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)
        
        # Convert to absolute path
        if not os.path.isabs(file_path):
            abs_path = os.path.abspath(file_path)
        else:
            abs_path = file_path
        
        # Check if it's within the workspace
        workspace_abs = os.path.abspath(cls.WORKSPACE_BASE)
        return abs_path.startswith(workspace_abs)
    
    @classmethod
    def get_relative_path(cls, file_path: Union[str, Path]) -> Optional[str]:
        """
        Get the relative path from the workspace base.
        
        Args:
            file_path: The file path to get relative path for
            
        Returns:
            Relative path from workspace base, or None if not within workspace
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)
        
        # Convert to absolute path
        if not os.path.isabs(file_path):
            abs_path = os.path.abspath(file_path)
        else:
            abs_path = file_path
        
        # Check if it's within the workspace
        workspace_abs = os.path.abspath(cls.WORKSPACE_BASE)
        if abs_path.startswith(workspace_abs):
            # Remove the workspace base from the path
            relative_path = abs_path[len(workspace_abs):].lstrip(os.sep)
            return relative_path
        
        return None


# Convenience functions for backward compatibility
def prepend_file_protocol(file_path: Union[str, Path]) -> str:
    """Prepend file:///D:/AI/DIA3/ to a file path."""
    return FilePathUtils.prepend_file_protocol(file_path)


def get_results_path(filename: str) -> str:
    """Get a file path in the Results directory with protocol prefix."""
    return FilePathUtils.get_results_path(filename)


def get_reports_path(filename: str) -> str:
    """Get a file path in the Results/reports directory with protocol prefix."""
    return FilePathUtils.get_reports_path(filename)


def get_docs_path(filename: str) -> str:
    """Get a file path in the docs directory with protocol prefix."""
    return FilePathUtils.get_docs_path(filename)


def get_white_papers_path(filename: str) -> str:
    """Get a file path in the docs/white_papers directory with protocol prefix."""
    return FilePathUtils.get_white_papers_path(filename)


def get_generated_pdfs_path(filename: str) -> str:
    """Get a file path in the docs/white_papers/generated_pdfs directory with protocol prefix."""
    return FilePathUtils.get_generated_pdfs_path(filename)
