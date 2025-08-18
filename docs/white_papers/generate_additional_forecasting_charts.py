#!/usr/bin/env python3
"""
Script to generate additional forecasting charts for the DIA3 whitepaper.
"""

import requests
import base64
from pathlib import Path
import time

# Create images directory if it doesn't exist
images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

# Additional forecasting charts
additional_charts = {
    "capability_evolution_forecasting": """
graph TB
    subgraph "Capability Evolution Forecasting"
        subgraph "Current Capabilities"
            CC1[Military Capabilities]
            CC2[Technology Capabilities]
            CC3[Economic Capabilities]
            CC4[Alliance Capabilities]
        end
        
        subgraph "Development Trajectories"
            DT1[Linear Development]
            DT2[Exponential Growth]
            DT3[Disruptive Innovation]
            DT4[Stagnation/Decline]
        end
        
        subgraph "Time Horizons"
            TH1[Short-term: 6-12 months]
            TH2[Medium-term: 1-3 years]
            TH3[Long-term: 3-10 years]
            TH4[Strategic: 10+ years]
        end
        
        subgraph "Forecast Scenarios"
            FS1[Capability Parity - 35%]
            FS2[Capability Superiority - 40%]
            FS3[Capability Gap - 20%]
            FS4[Disruptive Change - 5%]
        end
    end
    
    CC1 --> DT1
    CC2 --> DT2
    CC3 --> DT3
    CC4 --> DT4
    
    DT1 --> TH1
    DT2 --> TH2
    DT3 --> TH3
    DT4 --> TH4
    
    TH1 --> FS1
    TH2 --> FS2
    TH3 --> FS3
    TH4 --> FS4
    
    style CC1 fill:#e3f2fd
    style CC2 fill:#e3f2fd
    style CC3 fill:#e3f2fd
    style CC4 fill:#e3f2fd
    style DT1 fill:#e1f5fe
    style DT2 fill:#e1f5fe
    style DT3 fill:#e1f5fe
    style DT4 fill:#e1f5fe
    style TH1 fill:#e8f5e8
    style TH2 fill:#e8f5e8
    style TH3 fill:#e8f5e8
    style TH4 fill:#e8f5e8
    style FS1 fill:#fff3e0
    style FS2 fill:#fff3e0
    style FS3 fill:#fff3e0
    style FS4 fill:#fff3e0
    """,
    
    "risk_timeline_forecasting": """
gantt
    title Risk Timeline Forecasting
    dateFormat  YYYY-MM-DD
    section Current Risk Assessment
    Low Risk Period    :low1, 2025-01-01, 2025-06-30
    Medium Risk Period :medium1, 2025-07-01, 2025-12-31
    
    section Risk Evolution Scenarios
    Scenario A: Gradual Escalation    :scenarioA, 2026-01-01, 2026-12-31
    Scenario B: Rapid Escalation      :scenarioB, 2026-01-01, 2026-06-30
    Scenario C: Risk Mitigation       :scenarioC, 2026-01-01, 2027-06-30
    Scenario D: Crisis Event          :scenarioD, 2026-06-01, 2026-08-31
    
    section Response Timeline
    Early Warning Phase    :warning1, 2025-10-01, 2026-03-31
    Preparation Phase      :prep1, 2026-01-01, 2026-06-30
    Response Phase         :response1, 2026-06-01, 2026-12-31
    Recovery Phase         :recovery1, 2026-12-01, 2027-06-30
    """,
    
    "technology_adoption_forecasting": """
graph LR
    subgraph "Technology Adoption Forecasting"
        subgraph "Technology Categories"
            TC1[AI/ML Technologies]
            TC2[Cybersecurity Technologies]
            TC3[Quantum Technologies]
            TC4[Biotechnology]
            TC5[Space Technologies]
        end
        
        subgraph "Adoption Phases"
            AP1[Research & Development]
            AP2[Prototype & Testing]
            AP3[Limited Deployment]
            AP4[Full Integration]
            AP5[Widespread Adoption]
        end
        
        subgraph "Adoption Rates"
            AR1[Early Adopters - 5%]
            AR2[Early Majority - 15%]
            AR3[Late Majority - 35%]
            AR4[Laggards - 45%]
        end
        
        subgraph "Strategic Impact"
            SI1[Game Changer - 20%]
            SI2[Significant Advantage - 45%]
            SI3[Moderate Impact - 25%]
            SI4[Minimal Impact - 10%]
        end
    end
    
    TC1 --> AP1
    TC2 --> AP2
    TC3 --> AP3
    TC4 --> AP4
    TC5 --> AP5
    
    AP1 --> AR1
    AP2 --> AR2
    AP3 --> AR3
    AP4 --> AR4
    AP5 --> AR1
    
    AR1 --> SI1
    AR2 --> SI2
    AR3 --> SI3
    AR4 --> SI4
    
    style TC1 fill:#e3f2fd
    style TC2 fill:#e3f2fd
    style TC3 fill:#e3f2fd
    style TC4 fill:#e3f2fd
    style TC5 fill:#e3f2fd
    style AP1 fill:#e1f5fe
    style AP2 fill:#e1f5fe
    style AP3 fill:#e1f5fe
    style AP4 fill:#e1f5fe
    style AP5 fill:#e1f5fe
    style AR1 fill:#e8f5e8
    style AR2 fill:#e8f5e8
    style AR3 fill:#e8f5e8
    style AR4 fill:#e8f5e8
    style SI1 fill:#fff3e0
    style SI2 fill:#fff3e0
    style SI3 fill:#fff3e0
    style SI4 fill:#fff3e0
    """,
    
    "alliance_dynamics_forecasting": """
graph TB
    subgraph "Alliance Dynamics Forecasting"
        subgraph "Current Alliances"
            CA1[Strategic Alliances]
            CA2[Economic Alliances]
            CA3[Technology Alliances]
            CA4[Security Alliances]
        end
        
        subgraph "Alliance Dynamics"
            AD1[Strengthening]
            AD2[Weakening]
            AD3[Formation]
            AD4[Dissolution]
            AD5[Transformation]
        end
        
        subgraph "Driving Factors"
            DF1[Geopolitical Shifts]
            DF2[Economic Interests]
            DF3[Security Threats]
            DF4[Technology Competition]
            DF5[Cultural Factors]
        end
        
        subgraph "Future Scenarios"
            FS1[Alliance Consolidation - 30%]
            FS2[Alliance Fragmentation - 25%]
            FS3[New Alliance Formation - 35%]
            FS4[Alliance Neutralization - 10%]
        end
    end
    
    CA1 --> AD1
    CA2 --> AD2
    CA3 --> AD3
    CA4 --> AD4
    
    AD1 --> DF1
    AD2 --> DF2
    AD3 --> DF3
    AD4 --> DF4
    AD5 --> DF5
    
    DF1 --> FS1
    DF2 --> FS2
    DF3 --> FS3
    DF4 --> FS4
    DF5 --> FS1
    
    style CA1 fill:#e3f2fd
    style CA2 fill:#e3f2fd
    style CA3 fill:#e3f2fd
    style CA4 fill:#e3f2fd
    style AD1 fill:#e1f5fe
    style AD2 fill:#e1f5fe
    style AD3 fill:#e1f5fe
    style AD4 fill:#e1f5fe
    style AD5 fill:#e1f5fe
    style DF1 fill:#e8f5e8
    style DF2 fill:#e8f5e8
    style DF3 fill:#e8f5e8
    style DF4 fill:#e8f5e8
    style DF5 fill:#e8f5e8
    style FS1 fill:#fff3e0
    style FS2 fill:#fff3e0
    style FS3 fill:#fff3e0
    style FS4 fill:#fff3e0
    """
}

def generate_mermaid_image(mermaid_code, filename):
    """Generate PNG image from Mermaid code using mermaid.ink service"""
    try:
        # Encode the Mermaid code
        encoded_code = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
        
        # Create the URL for mermaid.ink
        url = f"https://mermaid.ink/img/{encoded_code}?type=png&theme=default"
        
        print(f"Generating {filename}...")
        
        # Download the image
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Save the image
        image_path = images_dir / filename
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Successfully generated {filename}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate {filename}: {str(e)}")
        return False

def main():
    print("Generating additional forecasting charts...")
    print("=" * 50)
    
    success_count = 0
    total_count = len(additional_charts)
    
    for name, mermaid_code in additional_charts.items():
        filename = f"{name}.png"
        
        if generate_mermaid_image(mermaid_code.strip(), filename):
            success_count += 1
        
        # Add a small delay to avoid overwhelming the service
        time.sleep(1)
    
    print("=" * 50)
    print(f"Generation complete: {success_count}/{total_count} additional charts created successfully")
    
    if success_count == total_count:
        print("\n✅ All additional forecasting charts generated successfully!")
        print("New charts created:")
        for name in additional_charts.keys():
            print(f"  - {name}.png")

if __name__ == "__main__":
    main()
