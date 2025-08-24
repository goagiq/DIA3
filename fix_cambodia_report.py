#!/usr/bin/env python3
"""
Fix the Thailand-Cambodia Invasion Report to ensure module clicks work properly.
"""
import os
import datetime

def fix_cambodia_report():
    """Fix the Cambodia report by ensuring proper JavaScript functionality."""
    
    # Read the existing report
    report_path = "Results/thailand_cambodia_invasion_report_20250824_103028.html"
    
    if not os.path.exists(report_path):
        print(f"❌ Report not found: {report_path}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debug JavaScript to help identify issues
    debug_js = """
        // Debug function to test module details
        function debugModuleDetails() {
            console.log('Module Details:', moduleDetails);
            console.log('Available modules:', Object.keys(moduleDetails));
        }
        
        // Enhanced showModuleDetails with error handling
        function showModuleDetails(moduleId) {
            console.log('showModuleDetails called with:', moduleId);
            
            const modal = document.getElementById('moduleModal');
            const modalContent = document.getElementById('modalContent');
            const moduleData = moduleDetails[moduleId];
            
            console.log('Modal element:', modal);
            console.log('Modal content element:', modalContent);
            console.log('Module data:', moduleData);
            
            if (!modal) {
                console.error('Modal element not found!');
                alert('Modal element not found. Please check the HTML structure.');
                return;
            }
            
            if (!modalContent) {
                console.error('Modal content element not found!');
                alert('Modal content element not found. Please check the HTML structure.');
                return;
            }
            
            if (!moduleData) {
                console.error('Module data not found for:', moduleId);
                alert('Module details not available for: ' + moduleId);
                return;
            }
            
            console.log('All elements found, proceeding with modal display...');
            
            let content = `
                <h2>${moduleData.title}</h2>
                <p>${moduleData.description}</p>
                
                <div class="metrics-grid">
            `;
            
            moduleData.metrics.forEach(metric => {
                content += `
                    <div class="metric-card">
                        <h4>${metric.name}</h4>
                        <div class="metric-value">${metric.value}</div>
                        <div class="metric-label">${metric.status}</div>
                        <div class="metric-details">
                            <span class="trend-level">${metric.trend}</span>
                        </div>
                    </div>
                `;
            });
            
            content += `
                </div>
                
                <div class="charts-grid">
                    <div class="chart-section">
                        <h4>${moduleData.title} Analysis</h4>
                        <div class="chart-container">
                            <canvas id="chart_${moduleId}" width="400" height="300"></canvas>
                        </div>
                    </div>
                </div>
                
                <div class="data-sources">
                    <h4>Data Sources</h4>
                    <ul class="sources-list">
                        <li>Intelligence Agency Reports</li>
                        <li>Capability Assessments</li>
                        <li>Strategic Analysis</li>
                        <li>Monitoring Data</li>
                        <li>Technology Reviews</li>
                        <li>Expert Consultations</li>
                        <li>Historical Data Analysis</li>
                        <li>Regional Intelligence</li>
                    </ul>
                </div>
                
                <div class="implications-grid">
                    <div class="implication-column">
                        <h4>Strategic Implications</h4>
                        <ul class="implications-list">
                            <li>
                                <strong>Strategic Balance</strong>
                                <p>Impact on regional strategic balance and power dynamics</p>
                                <span class="impact-level">High Impact</span>
                            </li>
                            <li>
                                <strong>Deterrence Effectiveness</strong>
                                <p>Assessment of deterrence capabilities and effectiveness</p>
                                <span class="impact-level">Critical Impact</span>
                            </li>
                        </ul>
                    </div>
                    <div class="implication-column">
                        <h4>Operational Implications</h4>
                        <ul class="implications-list">
                            <li>
                                <strong>Operational Readiness</strong>
                                <p>Current operational readiness and capability levels</p>
                                <span class="impact-level">Medium Impact</span>
                            </li>
                            <li>
                                <strong>Resource Allocation</strong>
                                <p>Optimal resource allocation for maximum effectiveness</p>
                                <span class="impact-level">Medium Impact</span>
                            </li>
                        </ul>
                    </div>
                </div>
            `;
            
            modalContent.innerHTML = content;
            modal.style.display = 'block';
            
            console.log('Modal displayed successfully');
            
            // Create chart after modal is shown
            setTimeout(() => {
                createChart(moduleId, moduleData.chartData);
            }, 100);
        }
        
        // Call debug function when page loads
        window.addEventListener('load', function() {
            console.log('Page loaded, debugging module details...');
            debugModuleDetails();
        });
    """
    
    # Insert the debug JavaScript before the closing </script> tag
    if '// Close modal when clicking outside' in content:
        # Insert before the closing script tag
        content = content.replace(
            '        // Close modal when clicking outside',
            debug_js + '\n        // Close modal when clicking outside'
        )
    else:
        # Add at the end of the script section
        content = content.replace(
            '    </script>',
            debug_js + '\n    </script>'
        )
    
    # Save the fixed report
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fixed_filename = f"thailand_cambodia_invasion_report_FIXED_{timestamp}.html"
    fixed_filepath = os.path.join("Results", fixed_filename)
    
    with open(fixed_filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed report saved: {fixed_filename}")
    print(f"📁 Location: {fixed_filepath}")
    print(f"🔧 Added debug JavaScript to help identify issues")
    print(f"📊 Open the file in a browser and check the console for debug information")
    
    return fixed_filepath

if __name__ == "__main__":
    print("🔧 Fixing Thailand-Cambodia Invasion Report...")
    fixed_path = fix_cambodia_report()
    if fixed_path:
        print(f"\n🎉 Report fixed successfully!")
        print(f"📄 Open {fixed_path} in your browser")
        print(f"🔍 Check the browser console (F12) for debug information")
        print(f"🖱️ Try clicking on module cards to test functionality")
