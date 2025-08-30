# Competitive Analysis Tool

## Overview
The Competitive Analysis tool provides comprehensive capabilities for analyzing competitors, benchmarking performance, identifying market opportunities, and developing competitive intelligence to support strategic decision-making and market positioning.

## Purpose
To systematically analyze competitors' strengths, weaknesses, strategies, and market positions to identify competitive advantages, market gaps, and strategic opportunities for business growth and market differentiation.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing and statistical analysis
- **scikit-learn** (>=1.3.0) - Machine learning and clustering analysis
- **matplotlib** (>=3.7.0) - Data visualization and charting
- **seaborn** (>=0.12.0) - Statistical data visualization

### Optional Libraries
- **requests** (>=2.31.0) - HTTP requests for data collection
- **beautifulsoup4** (>=4.12.0) - Web scraping and HTML parsing
- **selenium** (>=4.15.0) - Web automation and dynamic content scraping
- **plotly** (>=5.15.0) - Interactive visualizations
- **networkx** (>=3.1.0) - Network analysis and competitor mapping
- **wordcloud** (>=1.9.0) - Text visualization for competitor analysis
- **nltk** (>=3.8.0) - Natural language processing for text analysis
- **textblob** (>=0.17.0) - Sentiment analysis for competitor monitoring
- **yfinance** (>=0.2.0) - Financial data collection
- **alpha_vantage** (>=2.3.0) - Market data and financial analysis

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "analysis_config": {
      "type": "object",
      "properties": {
        "analysis_type": {
          "type": "string",
          "enum": ["comprehensive", "financial", "product", "marketing", "strategic", "swot"],
          "description": "Type of competitive analysis to perform"
        },
        "competitors": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "ticker": {"type": "string"},
              "website": {"type": "string"},
              "industry": {"type": "string"},
              "market_cap": {"type": "number"},
              "revenue": {"type": "number"}
            }
          },
          "description": "List of competitors to analyze"
        },
        "analysis_dimensions": {
          "type": "object",
          "properties": {
            "financial_metrics": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["revenue", "profit_margin", "market_cap", "pe_ratio", "debt_ratio", "roi"]
              }
            },
            "product_features": {
              "type": "array",
              "items": {"type": "string"}
            },
            "marketing_channels": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["social_media", "seo", "ppc", "content_marketing", "email", "pr"]
              }
            },
            "strategic_focus": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["cost_leadership", "differentiation", "niche", "innovation", "acquisition"]
              }
            }
          }
        },
        "time_period": {
          "type": "object",
          "properties": {
            "start_date": {"type": "string"},
            "end_date": {"type": "string"},
            "frequency": {
              "type": "string",
              "enum": ["daily", "weekly", "monthly", "quarterly", "yearly"]
            }
          }
        }
      }
    },
    "data_sources": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source_type": {
            "type": "string",
            "enum": ["financial_api", "web_scraping", "social_media", "news", "patents", "job_postings"]
          },
          "source_url": {"type": "string"},
          "api_key": {"type": "string"},
          "credentials": {"type": "object"}
        }
      }
    },
    "benchmarking_config": {
      "type": "object",
      "properties": {
        "benchmark_metrics": {
          "type": "array",
          "items": {"type": "string"}
        },
        "industry_averages": {"type": "object"},
        "best_practices": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    }
  },
  "required": ["analysis_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "competitive_landscape": {
      "type": "object",
      "properties": {
        "market_positioning": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "competitor_name": {"type": "string"},
              "market_share": {"type": "number"},
              "position": {"type": "string"},
              "strengths": {
                "type": "array",
                "items": {"type": "string"}
              },
              "weaknesses": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          }
        },
        "competitive_matrix": {
          "type": "object",
          "properties": {
            "dimensions": {
              "type": "array",
              "items": {"type": "string"}
            },
            "scores": {
              "type": "object",
              "additionalProperties": {
                "type": "object",
                "additionalProperties": {"type": "number"}
              }
            }
          }
        }
      }
    },
    "financial_analysis": {
      "type": "object",
      "properties": {
        "financial_metrics": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "competitor_name": {"type": "string"},
              "metrics": {
                "type": "object",
                "additionalProperties": {"type": "number"}
              },
              "trend": {
                "type": "string",
                "enum": ["increasing", "decreasing", "stable"]
              }
            }
          }
        },
        "benchmark_comparison": {
          "type": "object",
          "properties": {
            "industry_averages": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            },
            "percentile_rankings": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            }
          }
        }
      }
    },
    "product_analysis": {
      "type": "object",
      "properties": {
        "feature_comparison": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "feature": {"type": "string"},
              "competitors": {
                "type": "object",
                "additionalProperties": {"type": "boolean"}
              },
              "differentiation_potential": {"type": "number"}
            }
          }
        },
        "pricing_analysis": {
          "type": "object",
          "properties": {
            "price_ranges": {
              "type": "object",
              "additionalProperties": {
                "type": "object",
                "properties": {
                  "min": {"type": "number"},
                  "max": {"type": "number"},
                  "average": {"type": "number"}
                }
              }
            },
            "value_proposition": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        }
      }
    },
    "strategic_insights": {
      "type": "object",
      "properties": {
        "opportunities": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "opportunity": {"type": "string"},
              "potential_impact": {"type": "string"},
              "implementation_difficulty": {"type": "string"}
            }
          }
        },
        "threats": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "threat": {"type": "string"},
              "likelihood": {"type": "string"},
              "potential_impact": {"type": "string"}
            }
          }
        },
        "recommendations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "recommendation": {"type": "string"},
              "priority": {"type": "string"},
              "timeline": {"type": "string"},
              "expected_outcome": {"type": "string"}
            }
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "competitive_matrix_chart": {"type": "string"},
        "financial_trends_chart": {"type": "string"},
        "market_positioning_map": {"type": "string"},
        "swot_analysis_chart": {"type": "string"}
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for competitive analysis in seconds"
    }
  }
}
```

## Intended Use
- **Market Positioning**: Analyze competitive landscape and market positioning
- **Financial Benchmarking**: Compare financial performance with competitors
- **Product Analysis**: Evaluate product features and pricing strategies
- **Strategic Planning**: Identify opportunities and threats for strategic planning
- **SWOT Analysis**: Conduct comprehensive SWOT analysis of competitors
- **Market Entry**: Assess market entry opportunities and competitive barriers
- **Performance Monitoring**: Track competitor performance and market changes
- **Innovation Analysis**: Identify innovation gaps and opportunities

## Limitations
- Data availability may vary by competitor and industry
- Web scraping may be limited by terms of service and technical barriers
- Financial data may have reporting delays and accuracy limitations
- Analysis quality depends on data source reliability and completeness

## Safety
- Ensure compliance with data collection terms of service
- Respect rate limits and robots.txt when web scraping
- Validate financial data accuracy and sources
- Handle sensitive competitive information appropriately

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn requests beautifulsoup4
   ```

2. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   from sklearn.cluster import KMeans
   import matplotlib.pyplot as plt
   import seaborn as sns
   import requests
   from bs4 import BeautifulSoup
   ```

3. **Configure Analysis Environment**:
   - Set up API keys for financial data sources
   - Configure web scraping settings
   - Set up data storage and caching

### Usage

#### Basic Competitive Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def perform_basic_competitive_analysis(competitors_data):
    """Perform basic competitive analysis"""
    
    # Create competitor DataFrame
    df = pd.DataFrame(competitors_data)
    
    # Calculate market share
    total_revenue = df['revenue'].sum()
    df['market_share'] = (df['revenue'] / total_revenue) * 100
    
    # Calculate financial ratios
    df['profit_margin'] = (df['net_income'] / df['revenue']) * 100
    df['debt_ratio'] = (df['total_debt'] / df['total_assets']) * 100
    
    # Create competitive matrix
    matrix_data = df[['name', 'market_share', 'profit_margin', 'debt_ratio']].copy()
    
    # Normalize metrics for comparison
    for col in ['market_share', 'profit_margin', 'debt_ratio']:
        matrix_data[f'{col}_normalized'] = (matrix_data[col] - matrix_data[col].min()) / \
                                          (matrix_data[col].max() - matrix_data[col].min())
    
    return matrix_data

# Usage example
competitors = [
    {'name': 'Competitor A', 'revenue': 1000000, 'net_income': 150000, 'total_debt': 500000, 'total_assets': 2000000},
    {'name': 'Competitor B', 'revenue': 800000, 'net_income': 120000, 'total_debt': 400000, 'total_assets': 1500000},
    {'name': 'Competitor C', 'revenue': 1200000, 'net_income': 180000, 'total_debt': 600000, 'total_assets': 2500000}
]

analysis_result = perform_basic_competitive_analysis(competitors)
print(analysis_result)
```

#### Financial Benchmarking Analysis
```python
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def perform_financial_benchmarking(competitor_tickers, time_period='1y'):
    """Perform financial benchmarking analysis"""
    
    financial_data = {}
    
    for ticker in competitor_tickers:
        try:
            # Get financial data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key metrics
            financial_data[ticker] = {
                'market_cap': info.get('marketCap', 0),
                'revenue': info.get('totalRevenue', 0),
                'profit_margin': info.get('profitMargins', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'return_on_equity': info.get('returnOnEquity', 0)
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(financial_data).T
    
    # Calculate industry averages
    industry_averages = df.mean()
    
    # Calculate percentile rankings
    percentile_rankings = {}
    for metric in df.columns:
        percentile_rankings[metric] = df[metric].rank(pct=True)
    
    return {
        'financial_data': df,
        'industry_averages': industry_averages,
        'percentile_rankings': pd.DataFrame(percentile_rankings, index=df.index)
    }

# Usage example
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
benchmarking_result = perform_financial_benchmarking(tickers)
print(benchmarking_result['financial_data'])
```

#### Product Feature Analysis
```python
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def analyze_product_features(competitors_features):
    """Analyze product features across competitors"""
    
    # Create feature matrix
    feature_matrix = pd.DataFrame(competitors_features)
    
    # Calculate feature differentiation potential
    feature_importance = {}
    for feature in feature_matrix.columns[1:]:  # Exclude competitor name
        feature_coverage = feature_matrix[feature].sum() / len(feature_matrix)
        feature_importance[feature] = 1 - feature_coverage  # Higher value = more differentiation potential
    
    # Calculate competitor similarity
    similarity_matrix = cosine_similarity(feature_matrix.iloc[:, 1:])
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=feature_matrix['competitor'],
        columns=feature_matrix['competitor']
    )
    
    # Identify unique features
    unique_features = {}
    for competitor in feature_matrix['competitor']:
        competitor_features = feature_matrix[feature_matrix['competitor'] == competitor].iloc[0, 1:]
        unique_features[competitor] = competitor_features[competitor_features == True].index.tolist()
    
    return {
        'feature_importance': feature_importance,
        'similarity_matrix': similarity_df,
        'unique_features': unique_features
    }

# Usage example
features_data = [
    {'competitor': 'Competitor A', 'mobile_app': True, 'ai_features': True, 'cloud_sync': True, 'analytics': False},
    {'competitor': 'Competitor B', 'mobile_app': True, 'ai_features': False, 'cloud_sync': True, 'analytics': True},
    {'competitor': 'Competitor C', 'mobile_app': False, 'ai_features': True, 'cloud_sync': False, 'analytics': True}
]

feature_analysis = analyze_product_features(features_data)
print("Feature Importance:", feature_analysis['feature_importance'])
```

#### Strategic SWOT Analysis
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_swot_analysis(competitor_data):
    """Perform SWOT analysis for competitors"""
    
    swot_results = {}
    
    for competitor, data in competitor_data.items():
        # Analyze strengths
        strengths = []
        if data['market_share'] > data['industry_avg_market_share']:
            strengths.append(f"High market share ({data['market_share']:.1f}%)")
        if data['profit_margin'] > data['industry_avg_profit_margin']:
            strengths.append(f"High profitability ({data['profit_margin']:.1f}%)")
        if data['innovation_score'] > 7:
            strengths.append("Strong innovation capabilities")
        
        # Analyze weaknesses
        weaknesses = []
        if data['debt_ratio'] > 0.5:
            weaknesses.append(f"High debt ratio ({data['debt_ratio']:.1f})")
        if data['customer_satisfaction'] < 7:
            weaknesses.append("Low customer satisfaction")
        if data['employee_turnover'] > 0.15:
            weaknesses.append("High employee turnover")
        
        # Analyze opportunities
        opportunities = []
        if data['market_growth_rate'] > 0.1:
            opportunities.append("High market growth potential")
        if data['unserved_market_segments'] > 0:
            opportunities.append("Untapped market segments")
        if data['technology_adoption_gap'] > 0:
            opportunities.append("Technology adoption opportunities")
        
        # Analyze threats
        threats = []
        if data['new_entrants'] > 3:
            threats.append("High threat of new entrants")
        if data['substitute_products'] > 0.3:
            threats.append("Substitute product threat")
        if data['regulatory_changes']:
            threats.append("Regulatory changes")
        
        swot_results[competitor] = {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'opportunities': opportunities,
            'threats': threats
        }
    
    return swot_results

def visualize_swot_analysis(swot_results):
    """Create SWOT analysis visualization"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('SWOT Analysis by Competitor', fontsize=16)
    
    for i, (competitor, swot) in enumerate(swot_results.items()):
        row = i // 2
        col = i % 2
        
        # Create SWOT grid
        swot_categories = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
        swot_data = [len(swot['strengths']), len(swot['weaknesses']), 
                     len(swot['opportunities']), len(swot['threats'])]
        
        colors = ['green', 'red', 'blue', 'orange']
        axes[row, col].bar(swot_categories, swot_data, color=colors, alpha=0.7)
        axes[row, col].set_title(f'{competitor} SWOT Analysis')
        axes[row, col].set_ylabel('Number of Factors')
        
        # Add value labels
        for j, v in enumerate(swot_data):
            axes[row, col].text(j, v + 0.1, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('swot_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
competitor_data = {
    'Competitor A': {
        'market_share': 25.0, 'industry_avg_market_share': 20.0,
        'profit_margin': 15.0, 'industry_avg_profit_margin': 12.0,
        'innovation_score': 8.5, 'debt_ratio': 0.3,
        'customer_satisfaction': 8.2, 'employee_turnover': 0.12,
        'market_growth_rate': 0.15, 'unserved_market_segments': 2,
        'technology_adoption_gap': 0.2, 'new_entrants': 2,
        'substitute_products': 0.2, 'regulatory_changes': False
    },
    'Competitor B': {
        'market_share': 18.0, 'industry_avg_market_share': 20.0,
        'profit_margin': 10.0, 'industry_avg_profit_margin': 12.0,
        'innovation_score': 6.5, 'debt_ratio': 0.6,
        'customer_satisfaction': 6.8, 'employee_turnover': 0.18,
        'market_growth_rate': 0.08, 'unserved_market_segments': 1,
        'technology_adoption_gap': 0.1, 'new_entrants': 4,
        'substitute_products': 0.4, 'regulatory_changes': True
    }
}

swot_results = perform_swot_analysis(competitor_data)
visualize_swot_analysis(swot_results)
```

#### Market Positioning Analysis
```python
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def create_market_positioning_map(competitors_data):
    """Create market positioning map using PCA"""
    
    # Prepare data for positioning analysis
    positioning_data = []
    competitor_names = []
    
    for competitor, data in competitors_data.items():
        competitor_names.append(competitor)
        positioning_data.append([
            data['price_position'],  # Low to High price
            data['quality_position'],  # Low to High quality
            data['market_share'],
            data['innovation_score'],
            data['customer_satisfaction']
        ])
    
    # Convert to DataFrame
    df = pd.DataFrame(positioning_data, columns=[
        'price_position', 'quality_position', 'market_share', 
        'innovation_score', 'customer_satisfaction'
    ], index=competitor_names)
    
    # Standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    
    # Apply PCA for dimensionality reduction
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    
    # Create positioning map
    positioning_df = pd.DataFrame(
        pca_result,
        columns=['Dimension 1', 'Dimension 2'],
        index=competitor_names
    )
    
    # Add original metrics for reference
    for col in df.columns:
        positioning_df[col] = df[col]
    
    return positioning_df, pca

def visualize_positioning_map(positioning_df, pca):
    """Visualize market positioning map"""
    
    plt.figure(figsize=(12, 10))
    
    # Create scatter plot
    scatter = plt.scatter(
        positioning_df['Dimension 1'], 
        positioning_df['Dimension 2'],
        s=positioning_df['market_share'] * 100,  # Size based on market share
        c=positioning_df['customer_satisfaction'],  # Color based on satisfaction
        cmap='viridis',
        alpha=0.7
    )
    
    # Add competitor labels
    for idx, competitor in enumerate(positioning_df.index):
        plt.annotate(
            competitor,
            (positioning_df.iloc[idx]['Dimension 1'], positioning_df.iloc[idx]['Dimension 2']),
            xytext=(5, 5), textcoords='offset points',
            fontsize=10, fontweight='bold'
        )
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Customer Satisfaction Score')
    
    # Add quadrant lines
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    
    # Add quadrant labels
    plt.text(0.8, 0.8, 'High Quality\nHigh Price', transform=plt.gca().transAxes, 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    plt.text(0.2, 0.8, 'High Quality\nLow Price', transform=plt.gca().transAxes, 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    plt.text(0.8, 0.2, 'Low Quality\nHigh Price', transform=plt.gca().transAxes, 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    plt.text(0.2, 0.2, 'Low Quality\nLow Price', transform=plt.gca().transAxes, 
             ha='center', va='center', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    plt.xlabel('Dimension 1 (Price vs Quality)')
    plt.ylabel('Dimension 2 (Market Position)')
    plt.title('Market Positioning Map')
    plt.grid(True, alpha=0.3)
    
    plt.savefig('market_positioning_map.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
competitors_data = {
    'Competitor A': {
        'price_position': 0.8, 'quality_position': 0.9, 'market_share': 25.0,
        'innovation_score': 8.5, 'customer_satisfaction': 8.2
    },
    'Competitor B': {
        'price_position': 0.3, 'quality_position': 0.7, 'market_share': 18.0,
        'innovation_score': 6.5, 'customer_satisfaction': 6.8
    },
    'Competitor C': {
        'price_position': 0.6, 'quality_position': 0.4, 'market_share': 15.0,
        'innovation_score': 7.0, 'customer_satisfaction': 7.5
    },
    'Competitor D': {
        'price_position': 0.2, 'quality_position': 0.3, 'market_share': 12.0,
        'innovation_score': 5.5, 'customer_satisfaction': 6.0
    }
}

positioning_df, pca = create_market_positioning_map(competitors_data)
visualize_positioning_map(positioning_df, pca)
```

### Error Handling

#### Common Issues
1. **Data Collection Errors**: Handle API failures and web scraping issues
2. **Data Quality Issues**: Manage missing or inconsistent data
3. **Rate Limiting**: Handle API rate limits and request throttling
4. **Analysis Errors**: Manage computational errors in analysis

#### Troubleshooting
```python
# Handle data collection errors
def safe_data_collection(data_source, max_retries=3):
    """Safely collect data with retry logic"""
    for attempt in range(max_retries):
        try:
            if data_source['type'] == 'api':
                response = requests.get(data_source['url'], timeout=30)
                response.raise_for_status()
                return response.json()
            elif data_source['type'] == 'web_scraping':
                response = requests.get(data_source['url'], timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                return extract_data_from_soup(soup)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print(f"Failed to collect data from {data_source['url']}")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff

# Handle data quality issues
def validate_competitive_data(data):
    """Validate competitive analysis data"""
    validation_results = {}
    
    for competitor, metrics in data.items():
        validation_results[competitor] = {}
        
        # Check for missing values
        missing_values = {k: v for k, v in metrics.items() if pd.isna(v) or v is None}
        validation_results[competitor]['missing_values'] = missing_values
        
        # Check for outliers
        numeric_metrics = {k: v for k, v in metrics.items() if isinstance(v, (int, float))}
        outliers = {}
        for metric, value in numeric_metrics.items():
            if value < 0 or value > 1000000000:  # Reasonable range check
                outliers[metric] = value
        validation_results[competitor]['outliers'] = outliers
    
    return validation_results

# Handle rate limiting
def rate_limited_request(url, delay=1):
    """Make rate-limited requests"""
    time.sleep(delay)
    response = requests.get(url, timeout=30)
    
    if response.status_code == 429:  # Rate limited
        retry_after = int(response.headers.get('Retry-After', 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return rate_limited_request(url, delay)
    
    return response
```

### Monitoring
- Monitor data collection success rates and quality
- Track analysis performance and computational efficiency
- Monitor competitor data freshness and accuracy
- Alert on significant market changes or competitive moves

### Best Practices
1. **Data Quality**: Validate and clean all competitive data before analysis
2. **Regular Updates**: Schedule regular competitive analysis updates
3. **Multiple Sources**: Use multiple data sources for comprehensive analysis
4. **Context Awareness**: Consider industry context and market conditions
5. **Actionable Insights**: Focus on actionable strategic insights
6. **Ethical Collection**: Ensure ethical and legal data collection practices
7. **Documentation**: Maintain detailed documentation of analysis methods
8. **Continuous Learning**: Update analysis models based on new insights
