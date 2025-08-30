# Market Research Tool

## Overview
The Market Research tool provides comprehensive capabilities for conducting market research, analyzing market trends, identifying customer segments, and gathering market intelligence to support business strategy and decision-making.

## Purpose
To systematically collect, analyze, and interpret market data to understand market dynamics, customer behavior, competitive landscape, and business opportunities for informed strategic planning and market entry decisions.

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
- **wordcloud** (>=1.9.0) - Text visualization for market analysis
- **nltk** (>=3.8.0) - Natural language processing for text analysis
- **textblob** (>=0.17.0) - Sentiment analysis for market sentiment
- **tweepy** (>=4.14.0) - Twitter API for social media analysis
- **google-trends** (>=4.9.0) - Google Trends data collection
- **yfinance** (>=0.2.0) - Financial data collection
- **alpha_vantage** (>=2.3.0) - Market data and economic indicators

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "research_config": {
      "type": "object",
      "properties": {
        "research_type": {
          "type": "string",
          "enum": ["market_size", "customer_segmentation", "trend_analysis", "demand_forecasting", "competitive_landscape", "consumer_behavior"],
          "description": "Type of market research to perform"
        },
        "market_definition": {
          "type": "object",
          "properties": {
            "industry": {"type": "string"},
            "geographic_scope": {
              "type": "array",
              "items": {"type": "string"}
            },
            "target_segments": {
              "type": "array",
              "items": {"type": "string"}
            },
            "product_categories": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        },
        "research_questions": {
          "type": "array",
          "items": {"type": "string"}
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
            "enum": ["primary_survey", "secondary_data", "social_media", "web_scraping", "financial_data", "government_data", "industry_reports"]
          },
          "source_name": {"type": "string"},
          "source_url": {"type": "string"},
          "api_key": {"type": "string"},
          "credentials": {"type": "object"}
        }
      }
    },
    "analysis_config": {
      "type": "object",
      "properties": {
        "statistical_methods": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["descriptive", "inferential", "regression", "clustering", "factor_analysis", "conjoint_analysis"]
          }
        },
        "forecasting_models": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["time_series", "regression", "machine_learning", "expert_judgment"]
          }
        },
        "confidence_level": {"type": "number"},
        "sample_size": {"type": "integer"}
      }
    }
  },
  "required": ["research_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "market_overview": {
      "type": "object",
      "properties": {
        "market_size": {
          "type": "object",
          "properties": {
            "total_addressable_market": {"type": "number"},
            "serviceable_addressable_market": {"type": "number"},
            "serviceable_obtainable_market": {"type": "number"},
            "currency": {"type": "string"},
            "year": {"type": "integer"}
          }
        },
        "market_growth": {
          "type": "object",
          "properties": {
            "growth_rate": {"type": "number"},
            "growth_drivers": {
              "type": "array",
              "items": {"type": "string"}
            },
            "growth_barriers": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        },
        "market_trends": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "trend_name": {"type": "string"},
              "description": {"type": "string"},
              "impact": {"type": "string"},
              "timeframe": {"type": "string"}
            }
          }
        }
      }
    },
    "customer_analysis": {
      "type": "object",
      "properties": {
        "customer_segments": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "segment_name": {"type": "string"},
              "size": {"type": "number"},
              "characteristics": {
                "type": "object",
                "additionalProperties": true
              },
              "preferences": {
                "type": "array",
                "items": {"type": "string"}
              },
              "pain_points": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          }
        },
        "customer_behavior": {
          "type": "object",
          "properties": {
            "purchase_patterns": {
              "type": "object",
              "additionalProperties": true
            },
            "decision_factors": {
              "type": "array",
              "items": {"type": "string"}
            },
            "brand_preferences": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            }
          }
        }
      }
    },
    "competitive_analysis": {
      "type": "object",
      "properties": {
        "key_players": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "company_name": {"type": "string"},
              "market_share": {"type": "number"},
              "strengths": {
                "type": "array",
                "items": {"type": "string"}
              },
              "weaknesses": {
                "type": "array",
                "items": {"type": "string"}
              },
              "strategies": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          }
        },
        "competitive_landscape": {
          "type": "object",
          "properties": {
            "market_concentration": {"type": "string"},
            "entry_barriers": {
              "type": "array",
              "items": {"type": "string"}
            },
            "competitive_intensity": {"type": "string"}
          }
        }
      }
    },
    "demand_forecast": {
      "type": "object",
      "properties": {
        "forecast_periods": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "period": {"type": "string"},
              "forecasted_demand": {"type": "number"},
              "confidence_interval": {
                "type": "object",
                "properties": {
                  "lower": {"type": "number"},
                  "upper": {"type": "number"}
                }
              }
            }
          }
        },
        "forecast_accuracy": {"type": "number"},
        "key_assumptions": {
          "type": "array",
          "items": {"type": "string"}
        }
      }
    },
    "market_opportunities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "opportunity": {"type": "string"},
          "market_size": {"type": "number"},
          "growth_potential": {"type": "string"},
          "entry_difficulty": {"type": "string"},
          "time_to_market": {"type": "string"}
        }
      }
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "recommendation": {"type": "string"},
          "rationale": {"type": "string"},
          "priority": {"type": "string"},
          "implementation_timeline": {"type": "string"},
          "expected_outcome": {"type": "string"}
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "market_size_chart": {"type": "string"},
        "growth_trends_chart": {"type": "string"},
        "customer_segments_chart": {"type": "string"},
        "competitive_landscape_chart": {"type": "string"},
        "demand_forecast_chart": {"type": "string"}
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for market research analysis in seconds"
    }
  }
}
```

## Intended Use
- **Market Size Analysis**: Determine total addressable market and market potential
- **Customer Segmentation**: Identify and analyze customer segments and personas
- **Trend Analysis**: Analyze market trends and emerging opportunities
- **Demand Forecasting**: Predict future market demand and growth
- **Competitive Intelligence**: Analyze competitive landscape and positioning
- **Consumer Behavior**: Understand customer preferences and decision-making
- **Market Entry**: Assess market entry opportunities and strategies
- **Product Development**: Guide product development based on market needs

## Limitations
- Data availability may vary by market and industry
- Survey data quality depends on sample representativeness
- Forecasting accuracy depends on data quality and model assumptions
- Market dynamics may change rapidly, affecting research validity

## Safety
- Ensure compliance with data privacy regulations (GDPR, CCPA)
- Validate data sources and maintain data quality standards
- Handle sensitive market information appropriately
- Respect rate limits and terms of service for data collection

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

3. **Configure Research Environment**:
   - Set up API keys for data sources
   - Configure web scraping settings
   - Set up data storage and caching

### Usage

#### Market Size Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_market_size(market_data):
    """Calculate market size using bottom-up approach"""
    
    # Calculate Total Addressable Market (TAM)
    total_population = market_data['total_population']
    adoption_rate = market_data['adoption_rate']
    average_revenue_per_user = market_data['average_revenue_per_user']
    
    tam = total_population * adoption_rate * average_revenue_per_user
    
    # Calculate Serviceable Addressable Market (SAM)
    target_segment_percentage = market_data['target_segment_percentage']
    sam = tam * target_segment_percentage
    
    # Calculate Serviceable Obtainable Market (SOM)
    market_share_goal = market_data['market_share_goal']
    som = sam * market_share_goal
    
    return {
        'tam': tam,
        'sam': sam,
        'som': som,
        'currency': market_data.get('currency', 'USD'),
        'year': market_data.get('year', 2024)
    }

def visualize_market_size(market_sizes):
    """Visualize market size analysis"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Market size breakdown
    labels = ['TAM', 'SAM', 'SOM']
    sizes = [market_sizes['tam'], market_sizes['sam'], market_sizes['som']]
    colors = ['lightblue', 'lightgreen', 'lightcoral']
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Market Size Breakdown')
    
    # Market size comparison
    ax2.bar(labels, sizes, color=colors)
    ax2.set_title('Market Size Comparison')
    ax2.set_ylabel(f"Market Size ({market_sizes['currency']})")
    
    # Add value labels on bars
    for i, v in enumerate(sizes):
        ax2.text(i, v + max(sizes) * 0.01, f'{v:,.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('market_size_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
market_data = {
    'total_population': 1000000,
    'adoption_rate': 0.15,
    'average_revenue_per_user': 500,
    'target_segment_percentage': 0.30,
    'market_share_goal': 0.10,
    'currency': 'USD',
    'year': 2024
}

market_sizes = calculate_market_size(market_data)
visualize_market_size(market_sizes)
print(f"TAM: ${market_sizes['tam']:,.0f}")
print(f"SAM: ${market_sizes['sam']:,.0f}")
print(f"SOM: ${market_sizes['som']:,.0f}")
```

#### Customer Segmentation Analysis
```python
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def perform_customer_segmentation(customer_data, n_clusters=4):
    """Perform customer segmentation using K-means clustering"""
    
    # Prepare data for clustering
    features = ['age', 'income', 'purchase_frequency', 'avg_order_value', 'loyalty_score']
    X = customer_data[features].copy()
    
    # Handle missing values
    X = X.fillna(X.mean())
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    customer_data['segment'] = kmeans.fit_predict(X_scaled)
    
    # Analyze segments
    segment_analysis = {}
    for segment in range(n_clusters):
        segment_data = customer_data[customer_data['segment'] == segment]
        segment_analysis[f'Segment {segment}'] = {
            'size': len(segment_data),
            'percentage': len(segment_data) / len(customer_data) * 100,
            'characteristics': {
                'avg_age': segment_data['age'].mean(),
                'avg_income': segment_data['income'].mean(),
                'avg_purchase_frequency': segment_data['purchase_frequency'].mean(),
                'avg_order_value': segment_data['avg_order_value'].mean(),
                'avg_loyalty_score': segment_data['loyalty_score'].mean()
            }
        }
    
    return customer_data, segment_analysis

def visualize_customer_segments(customer_data, segment_analysis):
    """Visualize customer segmentation results"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Customer Segmentation Analysis', fontsize=16)
    
    # Segment size distribution
    segment_sizes = [seg['size'] for seg in segment_analysis.values()]
    segment_labels = list(segment_analysis.keys())
    
    axes[0, 0].pie(segment_sizes, labels=segment_labels, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Segment Size Distribution')
    
    # Age vs Income scatter plot
    for segment in customer_data['segment'].unique():
        segment_data = customer_data[customer_data['segment'] == segment]
        axes[0, 1].scatter(segment_data['age'], segment_data['income'], 
                          label=f'Segment {segment}', alpha=0.7)
    
    axes[0, 1].set_xlabel('Age')
    axes[0, 1].set_ylabel('Income')
    axes[0, 1].set_title('Age vs Income by Segment')
    axes[0, 1].legend()
    
    # Purchase frequency vs Order value
    for segment in customer_data['segment'].unique():
        segment_data = customer_data[customer_data['segment'] == segment]
        axes[1, 0].scatter(segment_data['purchase_frequency'], segment_data['avg_order_value'], 
                          label=f'Segment {segment}', alpha=0.7)
    
    axes[1, 0].set_xlabel('Purchase Frequency')
    axes[1, 0].set_ylabel('Average Order Value')
    axes[1, 0].set_title('Purchase Behavior by Segment')
    axes[1, 0].legend()
    
    # Segment characteristics heatmap
    characteristics_data = []
    for segment_name, segment_info in segment_analysis.items():
        characteristics_data.append(list(segment_info['characteristics'].values()))
    
    characteristics_df = pd.DataFrame(
        characteristics_data,
        index=segment_labels,
        columns=['Age', 'Income', 'Purchase Freq', 'Order Value', 'Loyalty Score']
    )
    
    sns.heatmap(characteristics_df, annot=True, cmap='YlOrRd', ax=axes[1, 1])
    axes[1, 1].set_title('Segment Characteristics')
    
    plt.tight_layout()
    plt.savefig('customer_segmentation.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
np.random.seed(42)
n_customers = 1000

customer_data = pd.DataFrame({
    'age': np.random.normal(35, 10, n_customers),
    'income': np.random.normal(50000, 20000, n_customers),
    'purchase_frequency': np.random.poisson(3, n_customers),
    'avg_order_value': np.random.normal(100, 30, n_customers),
    'loyalty_score': np.random.uniform(1, 10, n_customers)
})

customer_data, segment_analysis = perform_customer_segmentation(customer_data)
visualize_customer_segments(customer_data, segment_analysis)

for segment_name, segment_info in segment_analysis.items():
    print(f"\n{segment_name}:")
    print(f"  Size: {segment_info['size']} customers ({segment_info['percentage']:.1f}%)")
    print(f"  Average Age: {segment_info['characteristics']['avg_age']:.1f}")
    print(f"  Average Income: ${segment_info['characteristics']['avg_income']:,.0f}")
```

#### Market Trend Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def analyze_market_trends(trend_data):
    """Analyze market trends over time"""
    
    # Convert to datetime if needed
    if 'date' in trend_data.columns:
        trend_data['date'] = pd.to_datetime(trend_data['date'])
        trend_data = trend_data.sort_values('date')
    
    # Calculate trend metrics
    trend_analysis = {}
    
    for metric in ['market_size', 'growth_rate', 'adoption_rate']:
        if metric in trend_data.columns:
            # Calculate moving averages
            trend_data[f'{metric}_ma'] = trend_data[metric].rolling(window=3).mean()
            
            # Calculate trend direction
            recent_values = trend_data[metric].tail(3)
            if len(recent_values) >= 2:
                trend_direction = 'increasing' if recent_values.iloc[-1] > recent_values.iloc[0] else 'decreasing'
            else:
                trend_direction = 'stable'
            
            trend_analysis[metric] = {
                'current_value': trend_data[metric].iloc[-1],
                'trend_direction': trend_direction,
                'growth_rate': ((trend_data[metric].iloc[-1] - trend_data[metric].iloc[0]) / 
                               trend_data[metric].iloc[0]) * 100
            }
    
    return trend_data, trend_analysis

def visualize_market_trends(trend_data, trend_analysis):
    """Visualize market trends"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Market Trend Analysis', fontsize=16)
    
    # Market size trend
    if 'market_size' in trend_data.columns:
        axes[0, 0].plot(trend_data['date'], trend_data['market_size'], marker='o', linewidth=2)
        if 'market_size_ma' in trend_data.columns:
            axes[0, 0].plot(trend_data['date'], trend_data['market_size_ma'], 
                           linestyle='--', alpha=0.7, label='Moving Average')
        axes[0, 0].set_title('Market Size Trend')
        axes[0, 0].set_ylabel('Market Size')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
    
    # Growth rate trend
    if 'growth_rate' in trend_data.columns:
        axes[0, 1].plot(trend_data['date'], trend_data['growth_rate'], marker='s', linewidth=2, color='green')
        if 'growth_rate_ma' in trend_data.columns:
            axes[0, 1].plot(trend_data['date'], trend_data['growth_rate_ma'], 
                           linestyle='--', alpha=0.7, label='Moving Average')
        axes[0, 1].set_title('Growth Rate Trend')
        axes[0, 1].set_ylabel('Growth Rate (%)')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
    
    # Adoption rate trend
    if 'adoption_rate' in trend_data.columns:
        axes[1, 0].plot(trend_data['date'], trend_data['adoption_rate'], marker='^', linewidth=2, color='orange')
        if 'adoption_rate_ma' in trend_data.columns:
            axes[1, 0].plot(trend_data['date'], trend_data['adoption_rate_ma'], 
                           linestyle='--', alpha=0.7, label='Moving Average')
        axes[1, 0].set_title('Adoption Rate Trend')
        axes[1, 0].set_ylabel('Adoption Rate (%)')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
    
    # Trend summary
    trend_summary = []
    for metric, analysis in trend_analysis.items():
        trend_summary.append([
            metric.replace('_', ' ').title(),
            f"{analysis['current_value']:.2f}",
            analysis['trend_direction'],
            f"{analysis['growth_rate']:.1f}%"
        ])
    
    summary_df = pd.DataFrame(trend_summary, columns=['Metric', 'Current Value', 'Trend', 'Growth'])
    axes[1, 1].axis('tight')
    axes[1, 1].axis('off')
    table = axes[1, 1].table(cellText=summary_df.values, colLabels=summary_df.columns, 
                            cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    axes[1, 1].set_title('Trend Summary')
    
    plt.tight_layout()
    plt.savefig('market_trends.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='Q')
np.random.seed(42)

trend_data = pd.DataFrame({
    'date': dates,
    'market_size': np.cumsum(np.random.normal(100, 20, len(dates))),
    'growth_rate': np.random.normal(5, 2, len(dates)),
    'adoption_rate': np.cumsum(np.random.normal(0.5, 0.1, len(dates)))
})

trend_data, trend_analysis = analyze_market_trends(trend_data)
visualize_market_trends(trend_data, trend_analysis)

print("Market Trend Analysis Results:")
for metric, analysis in trend_analysis.items():
    print(f"{metric}: {analysis['current_value']:.2f} ({analysis['trend_direction']}, {analysis['growth_rate']:.1f}% growth)")
```

#### Demand Forecasting
```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

def perform_demand_forecasting(historical_data, forecast_periods=12):
    """Perform demand forecasting using multiple methods"""
    
    # Prepare data
    X = np.arange(len(historical_data)).reshape(-1, 1)
    y = historical_data['demand'].values
    
    # Linear regression model
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    
    # Generate future periods
    future_X = np.arange(len(historical_data), len(historical_data) + forecast_periods).reshape(-1, 1)
    
    # Make predictions
    lr_forecast = lr_model.predict(future_X)
    
    # Calculate confidence intervals (simplified)
    residuals = y - lr_model.predict(X)
    std_residuals = np.std(residuals)
    confidence_interval = 1.96 * std_residuals  # 95% confidence interval
    
    # Create forecast DataFrame
    forecast_dates = pd.date_range(
        start=historical_data.index[-1] + pd.DateOffset(months=1),
        periods=forecast_periods,
        freq='M'
    )
    
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'forecasted_demand': lr_forecast,
        'lower_bound': lr_forecast - confidence_interval,
        'upper_bound': lr_forecast + confidence_interval
    })
    
    # Calculate forecast accuracy metrics
    y_pred = lr_model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    return forecast_df, {
        'model': lr_model,
        'mse': mse,
        'r2': r2,
        'confidence_interval': confidence_interval
    }

def visualize_demand_forecast(historical_data, forecast_df, model_metrics):
    """Visualize demand forecast"""
    
    plt.figure(figsize=(12, 8))
    
    # Plot historical data
    plt.plot(historical_data.index, historical_data['demand'], 
             marker='o', linewidth=2, label='Historical Demand', color='blue')
    
    # Plot forecast
    plt.plot(forecast_df['date'], forecast_df['forecasted_demand'], 
             marker='s', linewidth=2, label='Forecasted Demand', color='red')
    
    # Plot confidence intervals
    plt.fill_between(forecast_df['date'], 
                     forecast_df['lower_bound'], 
                     forecast_df['upper_bound'], 
                     alpha=0.3, color='red', label='95% Confidence Interval')
    
    plt.title('Demand Forecast')
    plt.xlabel('Date')
    plt.ylabel('Demand')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add metrics text
    metrics_text = f'R² = {model_metrics["r2"]:.3f}\nMSE = {model_metrics["mse"]:.2f}'
    plt.text(0.02, 0.98, metrics_text, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('demand_forecast.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='M')

# Generate synthetic demand data with trend and seasonality
trend = np.linspace(100, 150, len(dates))
seasonality = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)  # Annual seasonality
noise = np.random.normal(0, 5, len(dates))
demand = trend + seasonality + noise

historical_data = pd.DataFrame({
    'demand': demand
}, index=dates)

forecast_df, model_metrics = perform_demand_forecasting(historical_data)
visualize_demand_forecast(historical_data, forecast_df, model_metrics)

print(f"Forecast Accuracy - R²: {model_metrics['r2']:.3f}")
print(f"Forecast Accuracy - MSE: {model_metrics['mse']:.2f}")
print("\nForecast Results:")
print(forecast_df[['date', 'forecasted_demand']].head())
```

### Error Handling

#### Common Issues
1. **Data Collection Errors**: Handle API failures and data source issues
2. **Data Quality Issues**: Manage missing, inconsistent, or biased data
3. **Sample Size Issues**: Handle insufficient sample sizes for analysis
4. **Forecasting Errors**: Manage model accuracy and prediction errors

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
def validate_market_data(data):
    """Validate market research data"""
    validation_results = {}
    
    # Check for missing values
    missing_values = data.isnull().sum()
    validation_results['missing_values'] = missing_values[missing_values > 0]
    
    # Check for outliers
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    outliers = {}
    for col in numeric_columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_mask = (data[col] < (Q1 - 1.5 * IQR)) | (data[col] > (Q3 + 1.5 * IQR))
        outliers[col] = data[col][outlier_mask].count()
    
    validation_results['outliers'] = outliers
    
    # Check for data consistency
    if 'date' in data.columns:
        date_range = data['date'].max() - data['date'].min()
        validation_results['date_range'] = date_range
    
    return validation_results

# Handle sample size issues
def check_sample_size_adequacy(data, confidence_level=0.95, margin_of_error=0.05):
    """Check if sample size is adequate for analysis"""
    n = len(data)
    
    # Calculate required sample size for given confidence level and margin of error
    z_score = 1.96  # For 95% confidence level
    required_n = (z_score ** 2 * 0.5 * 0.5) / (margin_of_error ** 2)
    
    adequacy_check = {
        'current_sample_size': n,
        'required_sample_size': int(required_n),
        'adequate': n >= required_n,
        'confidence_level': confidence_level,
        'margin_of_error': margin_of_error
    }
    
    return adequacy_check

# Handle forecasting errors
def validate_forecast_accuracy(actual, predicted):
    """Validate forecast accuracy"""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    r2 = r2_score(actual, predicted)
    
    # Calculate MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    accuracy_metrics = {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'mape': mape,
        'accuracy_rating': 'Good' if mape < 10 else 'Fair' if mape < 20 else 'Poor'
    }
    
    return accuracy_metrics
```

### Monitoring
- Monitor data collection success rates and quality
- Track forecast accuracy and model performance
- Monitor market changes and trend shifts
- Alert on significant market developments

### Best Practices
1. **Data Quality**: Ensure high-quality, reliable data sources
2. **Sample Representativeness**: Use representative samples for analysis
3. **Multiple Methods**: Use multiple research methods for validation
4. **Regular Updates**: Update market research regularly
5. **Context Awareness**: Consider external factors and market conditions
6. **Ethical Practices**: Follow ethical research practices and privacy guidelines
7. **Documentation**: Maintain detailed documentation of research methods
8. **Continuous Learning**: Update research methods based on new insights
