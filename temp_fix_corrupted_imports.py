#!/usr/bin/env python3
"""
Temporary script to fix corrupted module imports by commenting them out.
This will allow the FastAPI server to start while we fix the modules.
"""

import re

def comment_out_corrupted_imports():
    """Comment out corrupted module imports in modular_report_generator.py."""
    
    # Read the current file
    with open('src/core/modular_report_generator.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # List of modules that are known to be corrupted
    corrupted_modules = [
        'enhanced_data_analysis_module',
        'regional_sentiment_module', 
        'regional_security_module',
        'model_performance_module'
    ]
    
    # Comment out corrupted imports
    for module in corrupted_modules:
        import_pattern = f'from .modules.{module} import'
        replacement = f'# TEMPORARILY DISABLED: from .modules.{module} import'
        content = content.replace(import_pattern, replacement)
    
    # Comment out corrupted module registrations
    for module in corrupted_modules:
        class_name = ''.join(word.capitalize() for word in module.split('_')) + 'Module'
        register_pattern = f'self.register_module({class_name}())'
        replacement = f'# self.register_module({class_name}())  # TEMPORARILY DISABLED'
        content = content.replace(register_pattern, replacement)
    
    # Write the modified file
    with open('src/core/modular_report_generator.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Temporarily disabled corrupted module imports")

if __name__ == "__main__":
    comment_out_corrupted_imports()
