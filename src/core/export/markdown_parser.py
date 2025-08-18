"""
Markdown Parser

Comprehensive markdown parser that handles all markdown elements for document generation.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ElementType(Enum):
    """Markdown element types."""
    HEADER = "header"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    CODE_BLOCK = "code_block"
    MERMAID = "mermaid"
    IMAGE = "image"
    LINK = "link"
    BLOCKQUOTE = "blockquote"
    HORIZONTAL_RULE = "horizontal_rule"
    TEXT = "text"


@dataclass
class MarkdownElement:
    """Represents a parsed markdown element."""
    element_type: ElementType
    content: str
    level: Optional[int] = None  # For headers
    language: Optional[str] = None  # For code blocks
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


class MarkdownParser:
    """Comprehensive markdown parser for document generation."""
    
    def __init__(self):
        """Initialize markdown parser."""
        # Compile regex patterns for efficiency
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.list_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', re.MULTILINE)
        self.table_pattern = re.compile(r'^\|(.+)\|$', re.MULTILINE)
        self.code_block_pattern = re.compile(r'^```(\w+)?\n(.*?)```', re.DOTALL | re.MULTILINE)
        self.mermaid_pattern = re.compile(r'^```mermaid\n(.*?)```', re.DOTALL | re.MULTILINE)
        self.image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        self.blockquote_pattern = re.compile(r'^>\s+(.+)$', re.MULTILINE)
        self.horizontal_rule_pattern = re.compile(r'^[-*_]{3,}$', re.MULTILINE)
    
    def parse(self, markdown_content: str) -> List[MarkdownElement]:
        """Parse markdown content into structured elements.
        
        Args:
            markdown_content: Raw markdown content
            
        Returns:
            List of parsed markdown elements
        """
        elements = []
        lines = markdown_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].rstrip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Check for headers
            header_match = self.header_pattern.match(line)
            if header_match:
                level = len(header_match.group(1))
                content = header_match.group(2).strip()
                elements.append(MarkdownElement(
                    element_type=ElementType.HEADER,
                    content=content,
                    level=level
                ))
                i += 1
                continue
            
            # Check for horizontal rules
            if self.horizontal_rule_pattern.match(line):
                elements.append(MarkdownElement(
                    element_type=ElementType.HORIZONTAL_RULE,
                    content=""
                ))
                i += 1
                continue
            
            # Check for code blocks (including Mermaid)
            if line.startswith('```'):
                code_block = self._parse_code_block(lines, i)
                if code_block:
                    elements.append(code_block)
                    i = code_block.attributes.get('end_line', i + 1)
                    continue
            
            # Check for blockquotes
            if line.startswith('>'):
                blockquote = self._parse_blockquote(lines, i)
                if blockquote:
                    elements.append(blockquote)
                    i = blockquote.attributes.get('end_line', i + 1)
                    continue
            
            # Check for tables
            if line.startswith('|') and line.endswith('|'):
                table = self._parse_table(lines, i)
                if table:
                    elements.append(table)
                    i = table.attributes.get('end_line', i + 1)
                    continue
            
            # Check for lists
            list_match = self.list_pattern.match(line)
            if list_match:
                list_element = self._parse_list(lines, i)
                if list_element:
                    elements.append(list_element)
                    i = list_element.attributes.get('end_line', i + 1)
                    continue
            
            # Check for standalone image references (lines that are just image references)
            if self.image_pattern.match(line.strip()):
                # This is a standalone image reference, parse it as an image element
                match = self.image_pattern.match(line.strip())
                alt_text = match.group(1)
                url = match.group(2)
                elements.append(MarkdownElement(
                    element_type=ElementType.IMAGE,
                    content=url,
                    attributes={'alt_text': alt_text}
                ))
                i += 1
                continue
            
            # Check for images and links in text
            if self._contains_inline_elements(line):
                text_elements = self._parse_inline_elements(line)
                elements.extend(text_elements)
                i += 1
                continue
            
            # Regular paragraph
            paragraph = self._parse_paragraph(lines, i)
            if paragraph:
                elements.append(paragraph)
                i = paragraph.attributes.get('end_line', i + 1)
                continue
            
            i += 1
        
        return elements
    
    def _parse_code_block(self, lines: List[str], start_index: int) -> Optional[MarkdownElement]:
        """Parse a code block.
        
        Args:
            lines: All lines of markdown content
            start_index: Starting line index
            
        Returns:
            Parsed code block element or None
        """
        if start_index >= len(lines):
            return None
        
        start_line = lines[start_index]
        if not start_line.startswith('```'):
            return None
        
        # Extract language
        language = None
        if len(start_line) > 3:
            language = start_line[3:].strip()
        
        # Check if it's Mermaid
        if language == 'mermaid':
            return self._parse_mermaid_block(lines, start_index)
        
        # Find end of code block
        content_lines = []
        i = start_index + 1
        
        while i < len(lines):
            if lines[i].strip() == '```':
                break
            content_lines.append(lines[i])
            i += 1
        
        if i >= len(lines):
            # No closing ``` found
            return None
        
        content = '\n'.join(content_lines)
        
        return MarkdownElement(
            element_type=ElementType.CODE_BLOCK,
            content=content,
            language=language,
            attributes={'end_line': i + 1}
        )
    
    def _parse_mermaid_block(self, lines: List[str], start_index: int) -> Optional[MarkdownElement]:
        """Parse a Mermaid diagram block.
        
        Args:
            lines: All lines of markdown content
            start_index: Starting line index
            
        Returns:
            Parsed Mermaid element or None
        """
        content_lines = []
        i = start_index + 1
        
        while i < len(lines):
            if lines[i].strip() == '```':
                break
            content_lines.append(lines[i])
            i += 1
        
        if i >= len(lines):
            return None
        
        content = '\n'.join(content_lines)
        
        return MarkdownElement(
            element_type=ElementType.MERMAID,
            content=content,
            language='mermaid',
            attributes={'end_line': i + 1}
        )
    
    def _parse_blockquote(self, lines: List[str], start_index: int) -> Optional[MarkdownElement]:
        """Parse a blockquote.
        
        Args:
            lines: All lines of markdown content
            start_index: Starting line index
            
        Returns:
            Parsed blockquote element or None
        """
        content_lines = []
        i = start_index
        
        while i < len(lines):
            line = lines[i].rstrip()
            if not line:
                break
            if not line.startswith('>'):
                break
            
            # Remove the '>' prefix
            content_line = line[1:].strip()
            if content_line:
                content_lines.append(content_line)
            i += 1
        
        if not content_lines:
            return None
        
        content = '\n'.join(content_lines)
        
        return MarkdownElement(
            element_type=ElementType.BLOCKQUOTE,
            content=content,
            attributes={'end_line': i}
        )
    
    def _parse_table(self, lines: List[str], start_index: int) -> Optional[MarkdownElement]:
        """Parse a table.
        
        Args:
            lines: All lines of markdown content
            start_index: Starting line index
            
        Returns:
            Parsed table element or None
        """
        table_lines = []
        i = start_index
        
        while i < len(lines):
            line = lines[i].rstrip()
            if not line.startswith('|'):
                break
            
            table_lines.append(line)
            i += 1
        
        if len(table_lines) < 2:
            return None
        
        # Parse table structure
        headers = self._parse_table_row(table_lines[0])
        separators = self._parse_table_row(table_lines[1])
        
        # Validate separator row
        if not all(sep.strip().replace('-', '').replace(':', '').replace('|', '') == '' 
                  for sep in separators):
            return None
        
        # Parse data rows
        data_rows = []
        for line in table_lines[2:]:
            row = self._parse_table_row(line)
            if row:
                data_rows.append(row)
        
        table_data = {
            'headers': headers,
            'data': data_rows
        }
        
        return MarkdownElement(
            element_type=ElementType.TABLE,
            content='',
            attributes={
                'table_data': table_data,
                'end_line': i
            }
        )
    
    def _parse_table_row(self, line: str) -> List[str]:
        """Parse a table row.
        
        Args:
            line: Table row line
            
        Returns:
            List of cell contents
        """
        if not line.startswith('|') or not line.endswith('|'):
            return []
        
        # Split by | and remove empty first/last elements
        cells = line.split('|')[1:-1]
        return [cell.strip() for cell in cells]
    
    def _parse_list(self, lines: List[str], start_index: int) -> Optional[MarkdownElement]:
        """Parse a list.
        
        Args:
            lines: All lines of markdown content
            start_index: Starting line index
            
        Returns:
            Parsed list element or None
        """
        list_items = []
        i = start_index
        
        while i < len(lines):
            line = lines[i].rstrip()
            if not line:
                break
            
            list_match = self.list_pattern.match(line)
            if not list_match:
                break
            
            indent = len(list_match.group(1))
            marker = list_match.group(2)
            content = list_match.group(3)
            
            list_items.append({
                'indent': indent,
                'marker': marker,
                'content': content
            })
            i += 1
        
        if not list_items:
            return None
        
        return MarkdownElement(
            element_type=ElementType.LIST,
            content='',
            attributes={
                'list_items': list_items,
                'end_line': i
            }
        )
    
    def _parse_paragraph(self, lines: List[str], start_index: int) -> Optional[MarkdownElement]:
        """Parse a paragraph.
        
        Args:
            lines: All lines of markdown content
            start_index: Starting line index
            
        Returns:
            Parsed paragraph element or None
        """
        content_lines = []
        i = start_index
        
        while i < len(lines):
            line = lines[i].rstrip()
            if not line:
                break
            
            # Check if this line starts a different element type
            if (line.startswith('#') or 
                line.startswith('```') or 
                line.startswith('>') or 
                line.startswith('|') or
                line.startswith('-') or
                line.startswith('*') or
                line.startswith('+') or
                re.match(r'^\d+\.', line) or
                self.horizontal_rule_pattern.match(line)):
                break
            
            content_lines.append(line)
            i += 1
        
        if not content_lines:
            return None
        
        content = '\n'.join(content_lines)
        
        return MarkdownElement(
            element_type=ElementType.PARAGRAPH,
            content=content,
            attributes={'end_line': i}
        )
    
    def _contains_inline_elements(self, text: str) -> bool:
        """Check if text contains inline elements like images or links.
        
        Args:
            text: Text to check
            
        Returns:
            True if contains inline elements
        """
        return bool(self.image_pattern.search(text) or self.link_pattern.search(text))
    
    def _parse_inline_elements(self, text: str) -> List[MarkdownElement]:
        """Parse inline elements in text.
        
        Args:
            text: Text containing inline elements
            
        Returns:
            List of parsed elements
        """
        elements = []
        
        # Find all images and links
        matches = []
        
        # Find images
        for match in self.image_pattern.finditer(text):
            matches.append((match.start(), 'image', match))
        
        # Find links
        for match in self.link_pattern.finditer(text):
            matches.append((match.start(), 'link', match))
        
        # Sort by position
        matches.sort(key=lambda x: x[0])
        
        # Special case: if the entire text is just an image reference, return only the image element
        if len(matches) == 1 and matches[0][1] == 'image':
            match = matches[0][2]
            alt_text = match.group(1)
            url = match.group(2)
            elements.append(MarkdownElement(
                element_type=ElementType.IMAGE,
                content=url,
                attributes={'alt_text': alt_text}
            ))
            return elements
        
        # Split text and create elements
        last_pos = 0
        for pos, element_type, match in matches:
            # Add text before the element
            if pos > last_pos:
                text_before = text[last_pos:pos].strip()
                if text_before:
                    elements.append(MarkdownElement(
                        element_type=ElementType.TEXT,
                        content=text_before
                    ))
            
            # Add the element
            if element_type == 'image':
                alt_text = match.group(1)
                url = match.group(2)
                elements.append(MarkdownElement(
                    element_type=ElementType.IMAGE,
                    content=url,
                    attributes={'alt_text': alt_text}
                ))
                # For images, we don't want to include the original markdown text
                # So we skip adding any text after the image reference
                last_pos = match.end()
                continue
            elif element_type == 'link':
                link_text = match.group(1)
                url = match.group(2)
                elements.append(MarkdownElement(
                    element_type=ElementType.LINK,
                    content=url,
                    attributes={'link_text': link_text}
                ))
            
            last_pos = match.end()
        
        # Add remaining text (but only if we didn't encounter an image)
        if last_pos < len(text):
            text_after = text[last_pos:].strip()
            if text_after:
                elements.append(MarkdownElement(
                    element_type=ElementType.TEXT,
                    content=text_after
                ))
        
        return elements
    
    def extract_images(self, markdown_content: str) -> List[Dict[str, str]]:
        """Extract all image references from markdown content.
        
        Args:
            markdown_content: Markdown content to parse
            
        Returns:
            List of image information dictionaries
        """
        images = []
        
        for match in self.image_pattern.finditer(markdown_content):
            alt_text = match.group(1)
            url = match.group(2)
            images.append({
                'alt_text': alt_text,
                'url': url,
                'position': match.start()
            })
        
        return images
    
    def extract_mermaid_blocks(self, markdown_content: str) -> List[Dict[str, str]]:
        """Extract all Mermaid diagram blocks from markdown content.
        
        Args:
            markdown_content: Markdown content to parse
            
        Returns:
            List of Mermaid diagram information dictionaries
        """
        diagrams = []
        
        for match in self.mermaid_pattern.finditer(markdown_content):
            content = match.group(1)
            diagrams.append({
                'content': content,
                'position': match.start()
            })
        
        return diagrams
