#!/usr/bin/env python3
"""
Test tooltip functionality with a simple example.
"""
import os
import datetime

def create_tooltip_test():
    """Create a simple test to verify tooltip functionality."""
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tooltip Test</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 50px;
            background: #f0f0f0;
        }}
        
        .test-card {{
            background: white;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            cursor: pointer;
            display: inline-block;
        }}
        
        /* Enhanced Tooltip Styles */
        #enhancedTooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            z-index: 10000;
            display: none;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        #enhancedTooltip h4 {{
            color: #3498db;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        #enhancedTooltip .tooltip-content {{
            margin-bottom: 15px;
            line-height: 1.5;
        }}
        
        #enhancedTooltip .tooltip-source {{
            background: rgba(52, 152, 219, 0.2);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        
        #enhancedTooltip .tooltip-strategic {{
            background: rgba(231, 76, 60, 0.2);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        
        #enhancedTooltip .tooltip-recommendations {{
            background: rgba(46, 204, 113, 0.2);
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        
        #enhancedTooltip .tooltip-use-cases {{
            background: rgba(155, 89, 182, 0.2);
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>🔧 Tooltip Functionality Test</h1>
    <p>Hover over the cards below to test tooltip functionality:</p>
    
    <div class="test-card" 
         onmouseover="showEnhancedTooltip(event, {{
             title: 'Test Tooltip',
             description: 'This is a test tooltip to verify functionality.',
             source: '📊 Test Source: This is a test source',
             strategic_impact: '🎯 Test Impact: This is a test strategic impact',
             recommendations: '• Test recommendation 1\\n• Test recommendation 2\\n• Test recommendation 3',
             use_cases: '• Test use case 1\\n• Test use case 2\\n• Test use case 3'
         }})"
         onmouseout="hideEnhancedTooltip()">
        <h3>Test Card 1</h3>
        <p>Hover over this card to see a tooltip</p>
    </div>
    
    <div class="test-card" 
         onmouseover="showEnhancedTooltip(event, {{
             title: 'Another Test Tooltip',
             description: 'This is another test tooltip with different content.',
             source: '📊 Another Source: This is another test source',
             strategic_impact: '🎯 Another Impact: This is another test impact',
             recommendations: '• Another recommendation 1\\n• Another recommendation 2',
             use_cases: '• Another use case 1\\n• Another use case 2'
         }})"
         onmouseout="hideEnhancedTooltip()">
        <h3>Test Card 2</h3>
        <p>Hover over this card to see another tooltip</p>
    </div>
    
    <!-- Enhanced Tooltip -->
    <div id="enhancedTooltip">
        <h4 id="tooltipTitle"></h4>
        <div class="tooltip-content" id="tooltipContent"></div>
        <div class="tooltip-source" id="tooltipSource"></div>
        <div class="tooltip-strategic" id="tooltipStrategic"></div>
        <div class="tooltip-recommendations" id="tooltipRecommendations"></div>
        <div class="tooltip-use-cases" id="tooltipUseCases"></div>
    </div>
    
    <script>
        // Enhanced Tooltip Functions
        function showEnhancedTooltip(event, tooltipData) {{
            console.log('showEnhancedTooltip called with:', tooltipData);
            
            const tooltip = document.getElementById('enhancedTooltip');
            const title = document.getElementById('tooltipTitle');
            const content = document.getElementById('tooltipContent');
            const source = document.getElementById('tooltipSource');
            const strategic = document.getElementById('tooltipStrategic');
            const recommendations = document.getElementById('tooltipRecommendations');
            const useCases = document.getElementById('tooltipUseCases');
            
            console.log('Tooltip elements found:', {{
                tooltip: !!tooltip,
                title: !!title,
                content: !!content,
                source: !!source,
                strategic: !!strategic,
                recommendations: !!recommendations,
                useCases: !!useCases
            }});
            
            title.textContent = tooltipData.title;
            content.innerHTML = tooltipData.description;
            source.innerHTML = tooltipData.source;
            strategic.innerHTML = tooltipData.strategic_impact;
            
            if (tooltipData.recommendations) {{
                recommendations.innerHTML = '<strong>💡 Recommendations:</strong><br/>' + tooltipData.recommendations;
                recommendations.style.display = 'block';
            }} else {{
                recommendations.style.display = 'none';
            }}
            
            if (tooltipData.use_cases) {{
                useCases.innerHTML = '<strong>🎯 Use Cases:</strong><br/>' + tooltipData.use_cases;
                useCases.style.display = 'block';
            }} else {{
                useCases.style.display = 'none';
            }}
            
            tooltip.style.display = 'block';
            tooltip.style.left = event.pageX + 10 + 'px';
            tooltip.style.top = event.pageY - 10 + 'px';
            
            console.log('Tooltip positioned at:', {{
                left: tooltip.style.left,
                top: tooltip.style.top,
                display: tooltip.style.display
            }});
        }}
        
        function hideEnhancedTooltip() {{
            console.log('hideEnhancedTooltip called');
            document.getElementById('enhancedTooltip').style.display = 'none';
        }}
        
        // Debug function
        function debugTooltip() {{
            const tooltip = document.getElementById('enhancedTooltip');
            console.log('Tooltip element:', tooltip);
            console.log('Tooltip display style:', tooltip.style.display);
            console.log('Tooltip position:', {{
                left: tooltip.style.left,
                top: tooltip.style.top
            }});
        }}
        
        // Call debug on load
        window.addEventListener('load', function() {{
            console.log('Page loaded, debugging tooltip...');
            debugTooltip();
        }});
    </script>
</body>
</html>"""
    
    # Save the test file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tooltip_test_{timestamp}.html"
    filepath = os.path.join("Results", filename)
    
    os.makedirs("Results", exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Tooltip test created: {filename}")
    print(f"📁 Location: {filepath}")
    print(f"🔧 Open this file in your browser to test tooltip functionality")
    print(f"💡 Hover over the test cards to see if tooltips appear")
    print(f"🔍 Check browser console (F12) for debug information")
    
    return filepath

if __name__ == "__main__":
    print("🔧 Creating Tooltip Functionality Test...")
    test_path = create_tooltip_test()
    if test_path:
        print(f"\n🎉 Test created successfully!")
        print(f"📄 Open {test_path} in your browser")
        print(f"💡 Hover over the test cards to verify tooltip functionality")
        print(f"🔍 If tooltips don't work, check the browser console for errors")
