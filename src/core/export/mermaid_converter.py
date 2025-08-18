"""
Mermaid Diagram Converter

Converts Mermaid diagram code to PNG images for embedding in documents.
"""

import os
import subprocess
import tempfile
import base64
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class MermaidConverter:
    """Converts Mermaid diagrams to PNG images."""
    
    def __init__(self, output_dir: str = "temp/mermaid"):
        """Initialize Mermaid converter.
        
        Args:
            output_dir: Directory to store generated images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._check_mermaid_cli()
    
    def _check_mermaid_cli(self) -> bool:
        """Check if mermaid-cli is available.
        
        Returns:
            True if available, False otherwise
        """
        try:
            result = subprocess.run(
                ['mmdc', '--version'], 
                capture_output=True, 
                text=True,
                shell=True  # Use shell to handle PATH properly
            )
            if result.returncode == 0:
                logger.info("Mermaid CLI is available")
                self.mmdc_path = 'mmdc'
                return True
            else:
                logger.warning("Mermaid CLI not found or not working")
                return False
        except FileNotFoundError:
            logger.warning("Mermaid CLI not found in PATH")
            return False
    
    def convert_to_png(self, 
                      mermaid_code: str, 
                      diagram_name: str,
                      width: int = 800,
                      height: int = 600,
                      theme: str = "default") -> Optional[str]:
        """Convert Mermaid code to PNG image.
        
        Args:
            mermaid_code: Mermaid diagram code
            diagram_name: Name for the diagram
            width: Image width in pixels
            height: Image height in pixels
            theme: Mermaid theme (default, forest, dark, neutral)
            
        Returns:
            Path to generated PNG file or None if failed
        """
        try:
            # Create temporary file for Mermaid code
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.mmd', 
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(mermaid_code)
                temp_input = f.name
            
            # Generate output filename
            output_file = self.output_dir / f"{diagram_name}.png"
            
            # Convert using mermaid-cli
            cmd = [
                getattr(self, 'mmdc_path', 'mmdc'),  # Use stored path or fallback
                '-i', temp_input,
                '-o', str(output_file),
                '-w', str(width),
                '-H', str(height),
                '-t', theme,
                '-b', 'white'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,  # Use shell to handle PATH properly
                timeout=30  # 30 second timeout
            )
            
            # Clean up temporary input file
            os.unlink(temp_input)
            
            if result.returncode == 0 and output_file.exists():
                logger.info(f"Successfully converted Mermaid diagram: {diagram_name}")
                return str(output_file)
            else:
                logger.error(f"Failed to convert Mermaid diagram {diagram_name}: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout converting Mermaid diagram: {diagram_name}")
            return None
        except Exception as e:
            logger.error(f"Error converting Mermaid diagram {diagram_name}: {e}")
            return None
    
    def convert_to_base64(self, 
                         mermaid_code: str, 
                         diagram_name: str,
                         width: int = 800,
                         height: int = 600,
                         theme: str = "default") -> Optional[str]:
        """Convert Mermaid code to base64 encoded PNG.
        
        Args:
            mermaid_code: Mermaid diagram code
            diagram_name: Name for the diagram
            width: Image width in pixels
            height: Image height in pixels
            theme: Mermaid theme
            
        Returns:
            Base64 encoded PNG data or None if failed
        """
        png_path = self.convert_to_png(mermaid_code, diagram_name, width, height, theme)
        
        if png_path and os.path.exists(png_path):
            try:
                with open(png_path, 'rb') as f:
                    png_data = f.read()
                
                # Convert to base64
                base64_data = base64.b64encode(png_data).decode('utf-8')
                
                # Clean up PNG file
                os.unlink(png_path)
                
                return f"data:image/png;base64,{base64_data}"
                
            except Exception as e:
                logger.error(f"Error encoding PNG to base64: {e}")
                return None
        
        return None
    
    def extract_mermaid_blocks(self, markdown_content: str) -> Dict[str, str]:
        """Extract Mermaid code blocks from markdown content.
        
        Args:
            markdown_content: Markdown content to parse
            
        Returns:
            Dictionary mapping diagram names to Mermaid code
        """
        diagrams = {}
        lines = markdown_content.split('\n')
        in_mermaid_block = False
        current_block = []
        diagram_counter = 1
        
        for line in lines:
            if line.strip().startswith('```mermaid'):
                in_mermaid_block = True
                current_block = []
            elif line.strip() == '```' and in_mermaid_block:
                in_mermaid_block = False
                if current_block:
                    diagram_name = f"diagram_{diagram_counter}"
                    diagrams[diagram_name] = '\n'.join(current_block)
                    diagram_counter += 1
            elif in_mermaid_block:
                current_block.append(line)
        
        return diagrams
    
    def process_markdown_diagrams(self, 
                                markdown_content: str,
                                width: int = 800,
                                height: int = 600,
                                theme: str = "default") -> Dict[str, str]:
        """Process all Mermaid diagrams in markdown content.
        
        Args:
            markdown_content: Markdown content to process
            width: Image width in pixels
            height: Image height in pixels
            theme: Mermaid theme
            
        Returns:
            Dictionary mapping diagram names to PNG file paths
        """
        diagrams = self.extract_mermaid_blocks(markdown_content)
        converted_diagrams = {}
        
        for diagram_name, mermaid_code in diagrams.items():
            png_path = self.convert_to_png(
                mermaid_code, 
                diagram_name, 
                width, 
                height, 
                theme
            )
            if png_path:
                converted_diagrams[diagram_name] = png_path
        
        return converted_diagrams
    
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            for file_path in self.output_dir.glob("*.png"):
                file_path.unlink()
            logger.info("Cleaned up temporary Mermaid files")
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {e}")
