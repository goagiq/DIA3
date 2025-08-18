#!/usr/bin/env python3
"""
Script to generate actual PNG images from Mermaid diagrams for the DIA3 whitepaper.
"""

import requests
import base64
import json
from pathlib import Path
import time

# Create images directory if it doesn't exist
images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

# Mermaid diagrams with their definitions
diagrams = {
    "dia3_system_architecture": """
graph TB
    subgraph "DIA3 System Architecture"
        subgraph "Data Sources"
            DS1[Text Documents]
            DS2[PDF Files]
            DS3[Audio Files]
            DS4[Video Files]
            DS5[Structured Data]
            DS6[Real-time Feeds]
        end
        
        subgraph "Core Processing Engine"
            MCS[Monte Carlo Simulation Engine]
            VDB[Vector Database]
            KG[Knowledge Graph]
            MCP[MCP Tools Integration]
        end
        
        subgraph "AI Agents"
            A1[Threat Assessment Agent]
            A2[Predictive Analytics Agent]
            A3[Pattern Recognition Agent]
            A4[Risk Assessment Agent]
            A5[Strategic Planning Agent]
            A6[Intelligence Fusion Agent]
            A7[Adversary Analysis Agent]
            A8[Technology Assessment Agent]
            A9[Force Planning Agent]
            A10[Gap Analysis Agent]
        end
        
        subgraph "Analysis Categories"
            C1[Adversary Intent & Capability]
            C2[Strategic Risk Assessment]
            C3[Operational Planning]
            C4[Intelligence Fusion]
            C5[Strategic Planning]
        end
        
        subgraph "Output Products"
            OP1[Strategic Intelligence Reports]
            OP2[Predictive Intelligence]
            OP3[Decision Support Products]
            OP4[Risk Assessment Matrices]
            OP5[Visualization Dashboards]
        end
    end
    
    DS1 --> MCS
    DS2 --> MCS
    DS3 --> MCS
    DS4 --> MCS
    DS5 --> VDB
    DS6 --> KG
    
    MCS --> A1
    MCS --> A2
    MCS --> A3
    MCS --> A4
    MCS --> A5
    
    VDB --> A6
    KG --> A7
    MCP --> A8
    MCP --> A9
    MCP --> A10
    
    A1 --> C1
    A2 --> C2
    A3 --> C3
    A4 --> C4
    A5 --> C5
    A6 --> C4
    A7 --> C1
    A8 --> C5
    A9 --> C5
    A10 --> C4
    
    C1 --> OP1
    C2 --> OP4
    C3 --> OP3
    C4 --> OP2
    C5 --> OP1
    
    OP1 --> OP5
    OP2 --> OP5
    OP3 --> OP5
    OP4 --> OP5
    
    style MCS fill:#e1f5fe
    style VDB fill:#f3e5f5
    style KG fill:#e8f5e8
    style MCP fill:#fff3e0
    style A1 fill:#ffebee
    style A2 fill:#e8f5e8
    style A3 fill:#e3f2fd
    style A4 fill:#fff8e1
    style A5 fill:#f1f8e9
    style A6 fill:#fce4ec
    style A7 fill:#e0f2f1
    style A8 fill:#fafafa
    style A9 fill:#f9fbe7
    style A10 fill:#f3e5f5
    """,
    
    "intelligence_framework_process": """
flowchart TD
    Start([Intelligence Requirement]) --> QP[Question Preparation]
    QP --> ID[Identify Intelligence Need]
    ID --> SC[Select Question Category]
    SC --> CQ[Customize Question]
    CQ --> DP[Define Parameters]
    
    DP --> TC[Tool Coordination]
    TC --> PTS[Primary Tool Selection]
    PTS --> STS[Supporting Tools]
    STS --> DSI[Data Source Integration]
    DSI --> AC[Agent Coordination]
    
    AC --> AE[Analysis Execution]
    AE --> SE[Sequential Execution]
    SE --> DF[Data Fusion]
    DF --> VAL[Validation]
    VAL --> SYN[Synthesis]
    
    SYN --> IPG[Intelligence Product Generation]
    IPG --> ES[Executive Summary]
    ES --> DA[Detailed Analysis]
    DA --> VIS[Visualizations]
    VIS --> AR[Actionable Recommendations]
    
    AR --> End([Intelligence Product])
    
    subgraph "Question Categories"
        C1[Category 1: Adversary Intent & Capability]
        C2[Category 2: Strategic Risk Assessment]
        C3[Category 3: Operational Planning]
        C4[Category 4: Intelligence Fusion]
        C5[Category 5: Strategic Planning]
    end
    
    SC --> C1
    SC --> C2
    SC --> C3
    SC --> C4
    SC --> C5
    
    style Start fill:#e3f2fd
    style End fill:#e8f5e8
    style QP fill:#fff3e0
    style TC fill:#f3e5f5
    style AE fill:#e1f5fe
    style IPG fill:#fce4ec
    """,
    
    "monte_carlo_simulation_process": """
graph LR
    subgraph "Monte Carlo Simulation Process"
        subgraph "Input Parameters"
            P1[Scenario Definition]
            P2[Variable Ranges]
            P3[Probability Distributions]
            P4[Constraints]
        end
        
        subgraph "Simulation Engine"
            S1[Random Sampling]
            S2[Model Execution]
            S3[Result Collection]
            S4[Statistical Analysis]
        end
        
        subgraph "Output Analysis"
            O1[Probability Distributions]
            O2[Confidence Intervals]
            O3[Risk Metrics]
            O4[Scenario Rankings]
        end
        
        subgraph "Validation"
            V1[Historical Comparison]
            V2[Sensitivity Analysis]
            V3[Cross-validation]
            V4[Expert Review]
        end
    end
    
    P1 --> S1
    P2 --> S1
    P3 --> S1
    P4 --> S1
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    
    S4 --> O1
    S4 --> O2
    S4 --> O3
    S4 --> O4
    
    O1 --> V1
    O2 --> V2
    O3 --> V3
    O4 --> V4
    
    V1 --> V2
    V2 --> V3
    V3 --> V4
    
    style P1 fill:#e3f2fd
    style P2 fill:#e3f2fd
    style P3 fill:#e3f2fd
    style P4 fill:#e3f2fd
    style S1 fill:#e1f5fe
    style S2 fill:#e1f5fe
    style S3 fill:#e1f5fe
    style S4 fill:#e1f5fe
    style O1 fill:#e8f5e8
    style O2 fill:#e8f5e8
    style O3 fill:#e8f5e8
    style O4 fill:#e8f5e8
    style V1 fill:#fff3e0
    style V2 fill:#fff3e0
    style V3 fill:#fff3e0
    style V4 fill:#fff3e0
    """,
    
    "intelligence_fusion_process": """
graph TB
    subgraph "Intelligence Fusion Process"
        subgraph "Data Sources"
            HUMINT[HUMINT]
            SIGINT[SIGINT]
            OSINT[OSINT]
            GEOINT[GEOINT]
            IMINT[IMINT]
            MASINT[MASINT]
        end
        
        subgraph "Processing Pipeline"
            P1[Data Ingestion]
            P2[Quality Assessment]
            P3[Source Reliability Scoring]
            P4[Correlation Analysis]
            P5[Pattern Recognition]
            P6[Anomaly Detection]
        end
        
        subgraph "Fusion Engine"
            F1[Multi-source Correlation]
            F2[Confidence Assessment]
            F3[Conflict Resolution]
            F4[Gap Identification]
        end
        
        subgraph "Output Products"
            OP1[Fused Intelligence Assessment]
            OP2[Predictive Intelligence]
            OP3[Confidence Intervals]
            OP4[Collection Recommendations]
        end
    end
    
    HUMINT --> P1
    SIGINT --> P1
    OSINT --> P1
    GEOINT --> P1
    IMINT --> P1
    MASINT --> P1
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
    
    P6 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    F4 --> OP1
    F4 --> OP2
    F4 --> OP3
    F4 --> OP4
    
    style HUMINT fill:#e3f2fd
    style SIGINT fill:#e3f2fd
    style OSINT fill:#e3f2fd
    style GEOINT fill:#e3f2fd
    style IMINT fill:#e3f2fd
    style MASINT fill:#e3f2fd
    style P1 fill:#e1f5fe
    style P2 fill:#e1f5fe
    style P3 fill:#e1f5fe
    style P4 fill:#e1f5fe
    style P5 fill:#e1f5fe
    style P6 fill:#e1f5fe
    style F1 fill:#e8f5e8
    style F2 fill:#e8f5e8
    style F3 fill:#e8f5e8
    style F4 fill:#e8f5e8
    style OP1 fill:#fff3e0
    style OP2 fill:#fff3e0
    style OP3 fill:#fff3e0
    style OP4 fill:#fff3e0
    """,
    
    "art_of_war_integration": """
graph TB
    subgraph "Art of War Integration Framework"
        subgraph "Five Fundamentals (五事)"
            F1[道 - The Moral Law]
            F2[天 - Heaven/Weather]
            F3[地 - Earth/Terrain]
            F4[将 - The Commander]
            F5[法 - Method/Discipline]
        end
        
        subgraph "Modern Application"
            M1[Strategic Doctrine]
            M2[Environmental Factors]
            M3[Geographic Analysis]
            M4[Leadership Assessment]
            M5[Organizational Structure]
        end
        
        subgraph "Analysis Components"
            A1[Adversary Mindset]
            A2[Strategic Intent]
            A3[Capability Assessment]
            A4[Decision Patterns]
            A5[Counter-strategy Development]
        end
        
        subgraph "Output Integration"
            O1[Strategic Assessment]
            O2[Behavioral Prediction]
            O3[Risk Analysis]
            O4[Tactical Recommendations]
        end
    end
    
    F1 --> M1
    F2 --> M2
    F3 --> M3
    F4 --> M4
    F5 --> M5
    
    M1 --> A1
    M2 --> A2
    M3 --> A3
    M4 --> A4
    M5 --> A5
    
    A1 --> O1
    A2 --> O2
    A3 --> O3
    A4 --> O4
    A5 --> O1
    
    style F1 fill:#e3f2fd
    style F2 fill:#e3f2fd
    style F3 fill:#e3f2fd
    style F4 fill:#e3f2fd
    style F5 fill:#e3f2fd
    style M1 fill:#e1f5fe
    style M2 fill:#e1f5fe
    style M3 fill:#e1f5fe
    style M4 fill:#e1f5fe
    style M5 fill:#e1f5fe
    style A1 fill:#e8f5e8
    style A2 fill:#e8f5e8
    style A3 fill:#e8f5e8
    style A4 fill:#e8f5e8
    style A5 fill:#e8f5e8
    style O1 fill:#fff3e0
    style O2 fill:#fff3e0
    style O3 fill:#fff3e0
    style O4 fill:#fff3e0
    """,
    
    "predictive_analysis_timeline": """
gantt
    title DIA3 Predictive Analysis Timeline
    dateFormat  YYYY-MM-DD
    section Data Collection
    Historical Data Analysis    :done, hist1, 2025-01-01, 2025-01-07
    Current Intelligence Gathering :active, curr1, 2025-01-08, 2025-01-14
    Pattern Recognition        :pattern1, 2025-01-15, 2025-01-21
    
    section Monte Carlo Simulation
    Parameter Definition       :param1, 2025-01-22, 2025-01-28
    Simulation Execution       :sim1, 2025-01-29, 2025-02-04
    Result Analysis           :result1, 2025-02-05, 2025-02-11
    
    section Intelligence Fusion
    Multi-source Integration   :fusion1, 2025-02-12, 2025-02-18
    Confidence Assessment     :conf1, 2025-02-19, 2025-02-25
    Gap Analysis              :gap1, 2025-02-26, 2025-03-04
    
    section Predictive Output
    Scenario Development       :scenario1, 2025-03-05, 2025-03-11
    Risk Assessment           :risk1, 2025-03-12, 2025-03-18
    Recommendation Generation :rec1, 2025-03-19, 2025-03-25
    """,
    
    "decision_tree_analysis": """
graph TD
    Start([Strategic Decision Point]) --> Q1{Adversary Intent Clear?}
    Q1 -->|Yes| Q2{Capability Assessment}
    Q1 -->|No| A1[Conduct Intent Analysis]
    
    Q2 -->|High| Q3{Strategic Position}
    Q2 -->|Low| A2[Monitor Development]
    
    Q3 -->|Favorable| Q4{Resource Availability}
    Q3 -->|Unfavorable| A3[Reposition Forces]
    
    Q4 -->|Sufficient| A4[Execute Strategy]
    Q4 -->|Insufficient| A5[Resource Optimization]
    
    A1 --> Q2
    A2 --> Q1
    A3 --> Q4
    A5 --> Q4
    
    style Start fill:#e3f2fd
    style Q1 fill:#fff3e0
    style Q2 fill:#fff3e0
    style Q3 fill:#fff3e0
    style Q4 fill:#fff3e0
    style A1 fill:#e8f5e8
    style A2 fill:#e8f5e8
    style A3 fill:#e8f5e8
    style A4 fill:#e8f5e8
    style A5 fill:#e8f5e8
    """,
    
    "risk_assessment_matrix": """
graph TB
    subgraph "Risk Assessment Matrix"
        subgraph "Impact Levels"
            I5[Catastrophic]
            I4[Major]
            I3[Moderate]
            I2[Minor]
            I1[Insignificant]
        end
        
        subgraph "Probability Levels"
            P5[Very High]
            P4[High]
            P3[Medium]
            P2[Low]
            P1[Very Low]
        end
        
        subgraph "Risk Zones"
            R1[Critical Risk - Immediate Action Required]
            R2[High Risk - Priority Management]
            R3[Medium Risk - Monitor Closely]
            R4[Low Risk - Accept with Monitoring]
            R5[Minimal Risk - Accept]
        end
    end
    
    I5 --> R1
    I4 --> R2
    I3 --> R3
    I2 --> R4
    I1 --> R5
    
    P5 --> R1
    P4 --> R2
    P3 --> R3
    P2 --> R4
    P1 --> R5
    
    style I5 fill:#ffebee
    style I4 fill:#ffcdd2
    style I3 fill:#ef9a9a
    style I2 fill:#e57373
    style I1 fill:#ef5350
    style P5 fill:#ffebee
    style P4 fill:#ffcdd2
    style P3 fill:#ef9a9a
    style P2 fill:#e57373
    style P1 fill:#ef5350
    style R1 fill:#d32f2f
    style R2 fill:#f44336
    style R3 fill:#ff9800
    style R4 fill:#ffeb3b
    style R5 fill:#4caf50
    """,
    
    "framework_categories_overview": """
graph LR
    subgraph "DIA3 Framework Categories"
        subgraph "Category 1: Adversary Intent & Capability"
            A1[Decision-Making Analysis]
            A2[Threat Evolution Modeling]
            A3[Strategic Thinking Analysis]
        end
        
        subgraph "Category 2: Strategic Risk Assessment"
            B1[Multi-Scenario Risk Quantification]
            B2[Resource Allocation Risk Analysis]
            B3[Strategic Position Risk Assessment]
        end
        
        subgraph "Category 3: Operational Planning"
            C1[Optimal Strategy Identification]
            C2[Tactical Effectiveness Assessment]
            C3[Decision Point Analysis]
        end
        
        subgraph "Category 4: Intelligence Fusion"
            D1[Multi-Source Intelligence Fusion]
            D2[Emerging Threat Detection]
            D3[Intelligence Gap Analysis]
        end
        
        subgraph "Category 5: Strategic Planning"
            E1[Force Structure Optimization]
            E2[Technology Investment Assessment]
            E3[Strategic Positioning Analysis]
        end
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    B1 --> C1
    B2 --> C2
    B3 --> C3
    C1 --> D1
    C2 --> D2
    C3 --> D3
    D1 --> E1
    D2 --> E2
    D3 --> E3
    
    style A1 fill:#e3f2fd
    style A2 fill:#e3f2fd
    style A3 fill:#e3f2fd
    style B1 fill:#e1f5fe
    style B2 fill:#e1f5fe
    style B3 fill:#e1f5fe
    style C1 fill:#e8f5e8
    style C2 fill:#e8f5e8
    style C3 fill:#e8f5e8
    style D1 fill:#fff3e0
    style D2 fill:#fff3e0
    style D3 fill:#fff3e0
    style E1 fill:#f3e5f5
    style E2 fill:#f3e5f5
    style E3 fill:#f3e5f5
    """,
    
    "threat_evolution_forecasting": """
graph TB
    subgraph "Threat Evolution Forecasting"
        subgraph "Historical Data"
            H1[Past Threat Patterns]
            H2[Adversary Behavior]
            H3[Technology Evolution]
            H4[Strategic Shifts]
        end
        
        subgraph "Current Indicators"
            C1[Intelligence Reports]
            C2[Technology Development]
            C3[Strategic Posturing]
            C4[Economic Indicators]
        end
        
        subgraph "Forecasting Models"
            F1[Linear Projection]
            F2[Exponential Growth]
            F3[Cyclical Patterns]
            F4[Disruptive Events]
        end
        
        subgraph "Future Scenarios"
            S1[Baseline Scenario - 30%]
            S2[Accelerated Growth - 45%]
            S3[Disruptive Change - 20%]
            S4[Regressive Pattern - 5%]
        end
    end
    
    H1 --> F1
    H2 --> F2
    H3 --> F3
    H4 --> F4
    
    C1 --> F1
    C2 --> F2
    C3 --> F3
    C4 --> F4
    
    F1 --> S1
    F2 --> S2
    F3 --> S3
    F4 --> S4
    
    style H1 fill:#e3f2fd
    style H2 fill:#e3f2fd
    style H3 fill:#e3f2fd
    style H4 fill:#e3f2fd
    style C1 fill:#e1f5fe
    style C2 fill:#e1f5fe
    style C3 fill:#e1f5fe
    style C4 fill:#e1f5fe
    style F1 fill:#e8f5e8
    style F2 fill:#e8f5e8
    style F3 fill:#e8f5e8
    style F4 fill:#e8f5e8
    style S1 fill:#fff3e0
    style S2 fill:#fff3e0
    style S3 fill:#fff3e0
    style S4 fill:#fff3e0
    """,
    
    "strategic_position_forecasting": """
graph TB
    subgraph "Strategic Position Forecasting"
        subgraph "Current Position"
            CP1[Geographic Advantage]
            CP2[Resource Availability]
            CP3[Alliance Strength]
            CP4[Technology Edge]
        end
        
        subgraph "Trend Analysis"
            T1[Geographic Trends]
            T2[Resource Depletion]
            T3[Alliance Shifts]
            T4[Technology Race]
        end
        
        subgraph "Monte Carlo Scenarios"
            MC1[Position Strengthening - 40%]
            MC2[Position Weakening - 35%]
            MC3[Radical Shift - 20%]
            MC4[Status Quo - 5%]
        end
        
        subgraph "Strategic Recommendations"
            R1[Reinforce Position]
            R2[Develop Alternatives]
            R3[Strategic Repositioning]
            R4[Maintain Current Course]
        end
    end
    
    CP1 --> T1
    CP2 --> T2
    CP3 --> T3
    CP4 --> T4
    
    T1 --> MC1
    T2 --> MC2
    T3 --> MC3
    T4 --> MC4
    
    MC1 --> R1
    MC2 --> R2
    MC3 --> R3
    MC4 --> R4
    
    style CP1 fill:#e3f2fd
    style CP2 fill:#e3f2fd
    style CP3 fill:#e3f2fd
    style CP4 fill:#e3f2fd
    style T1 fill:#e1f5fe
    style T2 fill:#e1f5fe
    style T3 fill:#e1f5fe
    style T4 fill:#e1f5fe
    style MC1 fill:#e8f5e8
    style MC2 fill:#e8f5e8
    style MC3 fill:#e8f5e8
    style MC4 fill:#e8f5e8
    style R1 fill:#fff3e0
    style R2 fill:#fff3e0
    style R3 fill:#fff3e0
    style R4 fill:#fff3e0
    """,
    
    "predictive_intelligence_forecasting": """
graph TB
    subgraph "Predictive Intelligence Forecasting"
        subgraph "Intelligence Sources"
            IS1[HUMINT]
            IS2[SIGINT]
            IS3[OSINT]
            IS4[GEOINT]
            IS5[IMINT]
            IS6[MASINT]
        end
        
        subgraph "Processing Pipeline"
            PP1[Data Quality Assessment]
            PP2[Source Reliability Scoring]
            PP3[Correlation Analysis]
            PP4[Pattern Recognition]
            PP5[Anomaly Detection]
        end
        
        subgraph "Fusion Engine"
            FE1[Multi-source Correlation]
            FE2[Confidence Assessment]
            FE3[Conflict Resolution]
            FE4[Gap Identification]
        end
        
        subgraph "Predictive Output"
            PO1[Fused Intelligence Assessment]
            PO2[Predictive Intelligence Forecast]
            PO3[Confidence Intervals]
            PO4[Collection Recommendations]
        end
    end
    
    IS1 --> PP1
    IS2 --> PP1
    IS3 --> PP1
    IS4 --> PP1
    IS5 --> PP1
    IS6 --> PP1
    
    PP1 --> PP2
    PP2 --> PP3
    PP3 --> PP4
    PP4 --> PP5
    
    PP5 --> FE1
    FE1 --> FE2
    FE2 --> FE3
    FE3 --> FE4
    
    FE4 --> PO1
    FE4 --> PO2
    FE4 --> PO3
    FE4 --> PO4
    
    style IS1 fill:#e3f2fd
    style IS2 fill:#e3f2fd
    style IS3 fill:#e3f2fd
    style IS4 fill:#e3f2fd
    style IS5 fill:#e3f2fd
    style IS6 fill:#e3f2fd
    style PP1 fill:#e1f5fe
    style PP2 fill:#e1f5fe
    style PP3 fill:#e1f5fe
    style PP4 fill:#e1f5fe
    style PP5 fill:#e1f5fe
    style FE1 fill:#e8f5e8
    style FE2 fill:#e8f5e8
    style FE3 fill:#e8f5e8
    style FE4 fill:#e8f5e8
    style PO1 fill:#fff3e0
    style PO2 fill:#fff3e0
    style PO3 fill:#fff3e0
    style PO4 fill:#fff3e0
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
    print("Generating Mermaid diagram images...")
    print("=" * 50)
    
    success_count = 0
    total_count = len(diagrams)
    
    for name, mermaid_code in diagrams.items():
        filename = f"{name}.png"
        
        if generate_mermaid_image(mermaid_code.strip(), filename):
            success_count += 1
        
        # Add a small delay to avoid overwhelming the service
        time.sleep(1)
    
    print("=" * 50)
    print(f"Generation complete: {success_count}/{total_count} images created successfully")
    
    if success_count < total_count:
        print("\nNote: Some images failed to generate. This may be due to:")
        print("- Network connectivity issues")
        print("- Service limitations")
        print("- Complex diagram syntax")
        print("\nYou can manually generate the remaining images using:")
        print("https://mermaid.ink/")

if __name__ == "__main__":
    main()
