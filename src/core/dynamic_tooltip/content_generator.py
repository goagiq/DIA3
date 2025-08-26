"""
Content Generator for Dynamic Tooltips

Generates rich tooltip content based on templates, data sources, and object types.
"""

import re
from typing import Dict, List, Any, Optional
from .configuration import TooltipConfiguration, ContentTemplate, ContentType

class ContentGenerator:
    """Generates tooltip content from multiple data sources."""
    
    def __init__(self, config: TooltipConfiguration):
        self.config = config
    
    async def generate_content(self, object_id: str, object_type: str, 
                              content_data: Dict[str, Any], 
                              template_name: Optional[str] = None) -> Optional[str]:
        """Generate content using appropriate template and data."""
        
        # Determine template to use
        template = self._get_template(object_type, template_name)
        if not template:
            return self._generate_fallback_content(object_id, object_type, content_data)
        
        # Prepare template variables
        variables = self._prepare_template_variables(object_id, object_type, content_data)
        
        # Generate content based on template type
        if template.content_type == ContentType.RICH_TEXT:
            return self._generate_rich_text_content(template, variables)
        elif template.content_type == ContentType.HTML:
            return self._generate_html_content(template, variables)
        elif template.content_type == ContentType.MARKDOWN:
            return self._generate_markdown_content(template, variables)
        elif template.content_type == ContentType.JSON:
            return self._generate_json_content(template, variables)
        else:
            return self._generate_text_content(template, variables)
    
    def _get_template(self, object_type: str, template_name: Optional[str] = None) -> Optional[ContentTemplate]:
        """Get appropriate template for object type."""
        if template_name and template_name in self.config.content_templates:
            return self.config.content_templates[template_name]
        
        # Try to find template by object type
        if object_type in self.config.content_templates:
            return self.config.content_templates[object_type]
        
        # Try common template names
        common_templates = ["entity", "relationship", "simple"]
        for template_name in common_templates:
            if template_name in self.config.content_templates:
                return self.config.content_templates[template_name]
        
        return None
    
    def _prepare_template_variables(self, object_id: str, object_type: str, 
                                   content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare variables for template rendering."""
        variables = {
            "id": object_id,
            "type": object_type,
            "name": object_id,
            "confidence": 0.0,
            "description": "",
            "relationships": "",
            "recommendations": "",
            "evidence": "",
            "source": object_id,
            "target": "",
            "relationship_type": "",
            "strength": 0.0
        }
        
        # Extract data from different sources
        for source_name, data in content_data.items():
            if source_name == "knowledge_graph":
                variables.update(self._extract_knowledge_graph_data(data))
            elif source_name == "semantic_search":
                variables.update(self._extract_semantic_search_data(data))
            elif source_name == "business_intelligence":
                variables.update(self._extract_business_intelligence_data(data))
            elif source_name == "external_api":
                variables.update(self._extract_external_api_data(data))
        
        return variables
    
    def _extract_knowledge_graph_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from knowledge graph source."""
        extracted = {}
        
        if "name" in data:
            extracted["name"] = data["name"]
        
        if "confidence" in data:
            extracted["confidence"] = data["confidence"]
        
        if "description" in data:
            extracted["description"] = data["description"]
        
        if "relationships" in data:
            relationships_html = []
            for rel in data["relationships"]:
                rel_html = f"<li><strong>{rel.get('target', 'Unknown')}</strong> ({rel.get('type', 'related')})</li>"
                relationships_html.append(rel_html)
            
            if relationships_html:
                extracted["relationships"] = f"<ul>{''.join(relationships_html)}</ul>"
        
        if "recommendations" in data:
            recommendations_html = []
            for rec in data["recommendations"]:
                recommendations_html.append(f"<li>{rec}</li>")
            
            if recommendations_html:
                extracted["recommendations"] = f"<ul>{''.join(recommendations_html)}</ul>"
        
        return extracted
    
    def _extract_semantic_search_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from semantic search source."""
        extracted = {}
        
        if "results" in data:
            results_html = []
            for result in data["results"][:3]:  # Limit to top 3 results
                relevance = result.get("relevance", 0.0)
                text = result.get("text", "")
                results_html.append(f"<li><strong>{relevance:.1%}</strong> {text}</li>")
            
            if results_html:
                extracted["description"] = f"<ul>{''.join(results_html)}</ul>"
        
        if "suggestions" in data:
            suggestions_html = []
            for suggestion in data["suggestions"][:3]:  # Limit to top 3 suggestions
                suggestions_html.append(f"<li>{suggestion}</li>")
            
            if suggestions_html:
                extracted["recommendations"] = f"<ul>{''.join(suggestions_html)}</ul>"
        
        return extracted
    
    def _extract_business_intelligence_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from business intelligence source."""
        extracted = {}
        
        if "metrics" in data:
            metrics_html = []
            for key, value in data["metrics"].items():
                if isinstance(value, float):
                    metrics_html.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value:.2f}</li>")
                else:
                    metrics_html.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>")
            
            if metrics_html:
                extracted["description"] = f"<ul>{''.join(metrics_html)}</ul>"
        
        if "insights" in data:
            insights_html = []
            for insight in data["insights"][:3]:  # Limit to top 3 insights
                insights_html.append(f"<li>{insight}</li>")
            
            if insights_html:
                extracted["evidence"] = f"<ul>{''.join(insights_html)}</ul>"
        
        if "recommendations" in data:
            recommendations_html = []
            for rec in data["recommendations"][:3]:  # Limit to top 3 recommendations
                recommendations_html.append(f"<li>{rec}</li>")
            
            if recommendations_html:
                extracted["recommendations"] = f"<ul>{''.join(recommendations_html)}</ul>"
        
        return extracted
    
    def _extract_external_api_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from external API source."""
        extracted = {}
        
        if "external_data" in data:
            external_html = []
            for key, value in data["external_data"].items():
                external_html.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>")
            
            if external_html:
                extracted["description"] = f"<ul>{''.join(external_html)}</ul>"
        
        if "recent_events" in data:
            events_html = []
            for event in data["recent_events"][:3]:  # Limit to top 3 events
                events_html.append(f"<li>{event}</li>")
            
            if events_html:
                extracted["evidence"] = f"<ul>{''.join(events_html)}</ul>"
        
        return extracted
    
    def _generate_rich_text_content(self, template: ContentTemplate, variables: Dict[str, Any]) -> str:
        """Generate rich text content."""
        try:
            content = template.template.format(**variables)
            
            # Clean up empty sections
            content = re.sub(r'<ul></ul>', '', content)
            content = re.sub(r'<p><strong>.*?</strong></p>', '', content)
            content = re.sub(r'\n\s*\n', '\n', content)
            
            return content.strip()
        
        except KeyError as e:
            # If template variable is missing, use fallback
            if template.fallback_template:
                return template.fallback_template.format(**variables)
            else:
                return self._generate_fallback_content(variables.get("id", ""), variables.get("type", ""), {})
    
    def _generate_html_content(self, template: ContentTemplate, variables: Dict[str, Any]) -> str:
        """Generate HTML content."""
        return self._generate_rich_text_content(template, variables)
    
    def _generate_markdown_content(self, template: ContentTemplate, variables: Dict[str, Any]) -> str:
        """Generate markdown content."""
        try:
            content = template.template.format(**variables)
            
            # Convert HTML to markdown if needed
            content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
            content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
            content = re.sub(r'<h3>(.*?)</h3>', r'### \1', content)
            content = re.sub(r'<p>(.*?)</p>', r'\1\n\n', content)
            content = re.sub(r'<ul>(.*?)</ul>', r'\1', content, flags=re.DOTALL)
            content = re.sub(r'<li>(.*?)</li>', r'- \1\n', content)
            
            return content.strip()
        
        except KeyError:
            return self._generate_fallback_content(variables.get("id", ""), variables.get("type", ""), {})
    
    def _generate_json_content(self, template: ContentTemplate, variables: Dict[str, Any]) -> str:
        """Generate JSON content."""
        import json
        return json.dumps(variables, indent=2)
    
    def _generate_text_content(self, template: ContentTemplate, variables: Dict[str, Any]) -> str:
        """Generate plain text content."""
        try:
            content = template.template.format(**variables)
            
            # Strip HTML tags
            content = re.sub(r'<[^>]+>', '', content)
            content = re.sub(r'\n\s*\n', '\n', content)
            
            return content.strip()
        
        except KeyError:
            return self._generate_fallback_content(variables.get("id", ""), variables.get("type", ""), {})
    
    def _generate_fallback_content(self, object_id: str, object_type: str, content_data: Dict[str, Any]) -> str:
        """Generate fallback content when no template is available."""
        fallback_html = f"""
        <div class="tooltip-content">
            <h3>{object_id}</h3>
            <p><strong>Type:</strong> {object_type}</p>
        """
        
        # Add any available data
        if content_data:
            fallback_html += "<p><strong>Available Data:</strong></p><ul>"
            for source_name, data in content_data.items():
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, (str, int, float)):
                            fallback_html += f"<li><strong>{key}:</strong> {value}</li>"
                else:
                    fallback_html += f"<li><strong>{source_name}:</strong> {data}</li>"
            fallback_html += "</ul>"
        
        fallback_html += "</div>"
        return fallback_html
    
    def add_template(self, name: str, template: ContentTemplate):
        """Add a new content template."""
        self.config.add_template(name, template)
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names."""
        return list(self.config.content_templates.keys())
    
    def validate_template(self, template: ContentTemplate) -> bool:
        """Validate a template for required variables."""
        if not template.template:
            return False
        
        # Check for required variables
        required_vars = ["name", "type"]
        for var in required_vars:
            if "{" + var + "}" not in template.template:
                return False
        
        return True
