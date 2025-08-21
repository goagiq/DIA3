"""
Core utilities module.

This module provides utility functions and classes for the DIA3 system.
"""

from .file_path_utils import (
    FilePathUtils,
    prepend_file_protocol,
    get_results_path,
    get_reports_path,
    get_docs_path,
    get_white_papers_path,
    get_generated_pdfs_path
)

from .file_generator import (
    FileGenerator,
    file_generator,
    save_json,
    save_text,
    save_binary,
    save_report,
    save_visualization
)

__all__ = [
    'FilePathUtils',
    'prepend_file_protocol',
    'get_results_path',
    'get_reports_path',
    'get_docs_path',
    'get_white_papers_path',
    'get_generated_pdfs_path',
    'FileGenerator',
    'file_generator',
    'save_json',
    'save_text',
    'save_binary',
    'save_report',
    'save_visualization'
]
