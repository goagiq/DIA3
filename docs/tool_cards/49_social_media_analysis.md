# Social Media Analysis Tool

## Overview
The Social Media Analysis tool provides comprehensive capabilities for analyzing social media data, monitoring online conversations, tracking trends, and extracting insights from social platforms to support social intelligence and digital marketing strategies.

## Purpose
To analyze social media data, monitor brand mentions, track sentiment trends, identify influencers, analyze engagement patterns, and extract actionable insights from social media platforms for business intelligence, marketing, and reputation management.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing and statistical analysis
- **matplotlib** (>=3.7.0) - Data visualization and charting
- **seaborn** (>=0.12.0) - Statistical data visualization

### Optional Libraries
- **tweepy** (>=4.14.0) - Twitter API integration
- **facebook-sdk** (>=3.1.0) - Facebook API integration
- **instagram-scraper** (>=1.9.0) - Instagram data collection
- **reddit-api** (>=1.0.0) - Reddit API integration
- **linkedin-api** (>=2.0.0) - LinkedIn API integration
- **plotly** (>=5.15.0) - Interactive visualizations
- **wordcloud** (>=1.9.0) - Word cloud generation
- **textblob** (>=0.17.0) - Text processing and sentiment analysis
- **vaderSentiment** (>=3.3.0) - Social media sentiment analysis
- **nltk** (>=3.8.0) - Natural language processing
- **spacy** (>=3.6.0) - Advanced NLP
- **networkx** (>=3.1.0) - Network analysis for social networks
- **scikit-learn** (>=1.3.0) - Machine learning for social media analysis
- **requests** (>=2.31.0) - HTTP requests for API calls
- **beautifulsoup4** (>=4.12.0) - Web scraping
- **selenium** (>=4.15.0) - Web automation
- **schedule** (>=1.2.0) - Task scheduling
- **redis** (>=4.6.0) - Caching and data storage
- **elasticsearch** (>=8.0.0) - Search and analytics

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "social_media_data": {
      "type": "object",
      "properties": {
        "platforms": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["twitter", "facebook", "instagram", "linkedin", "reddit", "youtube", "tiktok"]
          }
        },
        "search_terms": {
          "type": "array",
          "items": {"type": "string"}
        },
        "date_range": {
          "type": "object",
          "properties": {
            "start_date": {"type": "string", "format": "date"},
            "end_date": {"type": "string", "format": "date"}
          }
        },
        "api_credentials": {
          "type": "object",
          "properties": {
            "twitter": {
              "type": "object",
              "properties": {
                "consumer_key": {"type": "string"},
                "consumer_secret": {"type": "string"},
                "access_token": {"type": "string"},
                "access_token_secret": {"type": "string"}
              }
            },
            "facebook": {
              "type": "object",
              "properties": {
                "app_id": {"type": "string"},
                "app_secret": {"type": "string"},
                "access_token": {"type": "string"}
              }
            }
          }
        }
      }
    },
    "analysis_config": {
      "type": "object",
      "properties": {
        "analysis_type": {
          "type": "string",
          "enum": ["sentiment_analysis", "trend_analysis", "influencer_analysis", "engagement_analysis", "brand_monitoring", "competitor_analysis", "content_analysis", "audience_analysis"]
        },
        "sentiment_config": {
          "type": "object",
          "properties": {
            "sentiment_model": {
              "type": "string",
              "enum": ["vader", "textblob", "custom"]
            },
            "language": {"type": "string"},
            "confidence_threshold": {"type": "number"}
          }
        },
        "trend_config": {
          "type": "object",
          "properties": {
            "trend_window": {"type": "string"},
            "min_mention_count": {"type": "integer"},
            "trend_algorithm": {
              "type": "string",
              "enum": ["moving_average", "exponential_smoothing", "changepoint_detection"]
            }
          }
        },
        "influencer_config": {
          "type": "object",
          "properties": {
            "metrics": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["follower_count", "engagement_rate", "reach", "influence_score"]
              }
            },
            "min_followers": {"type": "integer"},
            "min_engagement_rate": {"type": "number"}
          }
        }
      }
    },
    "visualization_config": {
      "type": "object",
      "properties": {
        "chart_type": {
          "type": "string",
          "enum": ["sentiment_timeline", "trend_analysis", "influencer_network", "engagement_heatmap", "wordcloud", "geographic_distribution"]
        },
        "interactive": {"type": "boolean"},
        "color_scheme": {"type": "string"}
      }
    }
  },
  "required": ["social_media_data", "analysis_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "social_media_analysis_results": {
      "type": "object",
      "properties": {
        "sentiment_analysis": {
          "type": "object",
          "properties": {
            "overall_sentiment": {
              "type": "object",
              "properties": {
                "positive_percentage": {"type": "number"},
                "negative_percentage": {"type": "number"},
                "neutral_percentage": {"type": "number"},
                "sentiment_score": {"type": "number"}
              }
            },
            "sentiment_timeline": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "date": {"type": "string"},
                  "positive_count": {"type": "integer"},
                  "negative_count": {"type": "integer"},
                  "neutral_count": {"type": "integer"},
                  "sentiment_score": {"type": "number"}
                }
              }
            },
            "platform_sentiment": {
              "type": "object",
              "additionalProperties": {
                "type": "object",
                "properties": {
                  "positive_percentage": {"type": "number"},
                  "negative_percentage": {"type": "number"},
                  "neutral_percentage": {"type": "number"}
                }
              }
            }
          }
        },
        "trend_analysis": {
          "type": "object",
          "properties": {
            "trending_topics": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "topic": {"type": "string"},
                  "mention_count": {"type": "integer"},
                  "growth_rate": {"type": "number"},
                  "sentiment_distribution": {
                    "type": "object",
                    "properties": {
                      "positive": {"type": "number"},
                      "negative": {"type": "number"},
                      "neutral": {"type": "number"}
                    }
                  }
                }
              }
            },
            "trend_timeline": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "date": {"type": "string"},
                  "topics": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "topic": {"type": "string"},
                        "mention_count": {"type": "integer"},
                        "rank": {"type": "integer"}
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "influencer_analysis": {
          "type": "object",
          "properties": {
            "top_influencers": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "username": {"type": "string"},
                  "platform": {"type": "string"},
                  "follower_count": {"type": "integer"},
                  "engagement_rate": {"type": "number"},
                  "influence_score": {"type": "number"},
                  "sentiment_impact": {"type": "number"},
                  "reach": {"type": "integer"}
                }
              }
            },
            "influencer_network": {
              "type": "object",
              "properties": {
                "nodes": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {"type": "string"},
                      "username": {"type": "string"},
                      "influence_score": {"type": "number"},
                      "follower_count": {"type": "integer"}
                    }
                  }
                },
                "edges": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "source": {"type": "string"},
                      "target": {"type": "string"},
                      "interaction_strength": {"type": "number"}
                    }
                  }
                }
              }
            }
          }
        },
        "engagement_analysis": {
          "type": "object",
          "properties": {
            "engagement_metrics": {
              "type": "object",
              "properties": {
                "total_posts": {"type": "integer"},
                "total_engagement": {"type": "integer"},
                "average_engagement_rate": {"type": "number"},
                "engagement_by_platform": {
                  "type": "object",
                  "additionalProperties": {
                    "type": "object",
                    "properties": {
                      "posts": {"type": "integer"},
                      "engagement": {"type": "integer"},
                      "engagement_rate": {"type": "number"}
                    }
                  }
                }
              }
            },
            "engagement_timeline": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "date": {"type": "string"},
                  "posts": {"type": "integer"},
                  "engagement": {"type": "integer"},
                  "engagement_rate": {"type": "number"}
                }
              }
            },
            "content_performance": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "content_type": {"type": "string"},
                  "posts": {"type": "integer"},
                  "engagement": {"type": "integer"},
                  "engagement_rate": {"type": "number"}
                }
              }
            }
          }
        },
        "brand_monitoring": {
          "type": "object",
          "properties": {
            "brand_mentions": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "platform": {"type": "string"},
                  "mention_count": {"type": "integer"},
                  "sentiment_distribution": {
                    "type": "object",
                    "properties": {
                      "positive": {"type": "number"},
                      "negative": {"type": "number"},
                      "neutral": {"type": "number"}
                    }
                  },
                  "top_mentions": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "text": {"type": "string"},
                        "author": {"type": "string"},
                        "date": {"type": "string"},
                        "sentiment": {"type": "string"},
                        "engagement": {"type": "integer"}
                      }
                    }
                  }
                }
              }
            },
            "brand_sentiment_timeline": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "date": {"type": "string"},
                  "mention_count": {"type": "integer"},
                  "sentiment_score": {"type": "number"},
                  "positive_mentions": {"type": "integer"},
                  "negative_mentions": {"type": "integer"}
                }
              }
            }
          }
        }
      }
    },
    "audience_analysis": {
      "type": "object",
      "properties": {
        "demographics": {
          "type": "object",
          "properties": {
            "age_distribution": {
              "type": "object",
              "additionalProperties": {"type": "number"}
            },
            "gender_distribution": {
              "type": "object",
              "properties": {
                "male": {"type": "number"},
                "female": {"type": "number"},
                "other": {"type": "number"}
              }
            },
            "geographic_distribution": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "location": {"type": "string"},
                  "percentage": {"type": "number"},
                  "mention_count": {"type": "integer"}
                }
              }
            }
          }
        },
        "interests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "interest": {"type": "string"},
              "percentage": {"type": "number"},
              "engagement_rate": {"type": "number"}
            }
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "sentiment_timeline": {"type": "string"},
        "trend_analysis": {"type": "string"},
        "influencer_network": {"type": "string"},
        "engagement_heatmap": {"type": "string"},
        "wordcloud": {"type": "string"},
        "geographic_distribution": {"type": "string"}
      }
    },
    "social_media_insights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "insight": {"type": "string"},
          "metric": {"type": "string"},
          "value": {"type": "number"},
          "trend": {"type": "string"},
          "significance": {"type": "string"}
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for social media analysis in seconds"
    }
  }
}
```

## Intended Use
- **Sentiment Analysis**: Analyze sentiment trends across social media platforms
- **Trend Analysis**: Identify trending topics and hashtags
- **Influencer Analysis**: Find and analyze key influencers in specific domains
- **Engagement Analysis**: Measure and analyze engagement patterns
- **Brand Monitoring**: Track brand mentions and reputation
- **Competitor Analysis**: Monitor competitor social media activities
- **Content Analysis**: Analyze content performance and virality
- **Audience Analysis**: Understand audience demographics and interests

## Limitations
- API rate limits may restrict data collection volume
- Some platforms have limited API access or require special permissions
- Sentiment analysis accuracy may vary by language and context
- Historical data access may be limited on some platforms
- Real-time analysis requires continuous data streaming

## Safety
- Respect API rate limits and terms of service
- Handle user privacy and data protection requirements
- Ensure compliance with platform-specific guidelines
- Validate data quality and source authenticity
- Consider ethical implications of social media monitoring

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn tweepy textblob vaderSentiment nltk spacy plotly wordcloud requests beautifulsoup4
   ```

2. **Download NLTK Data**:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('vader_lexicon')
   ```

3. **Download spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import tweepy
   from textblob import TextBlob
   from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
   import plotly.express as px
   ```

### Usage

#### Social Media Data Collection
```python
import tweepy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

class SocialMediaCollector:
    def __init__(self, api_credentials):
        """Initialize social media collector with API credentials"""
        self.api_credentials = api_credentials
        self.twitter_api = self._setup_twitter_api()
    
    def _setup_twitter_api(self):
        """Setup Twitter API connection"""
        auth = tweepy.OAuthHandler(
            self.api_credentials['twitter']['consumer_key'],
            self.api_credentials['twitter']['consumer_secret']
        )
        auth.set_access_token(
            self.api_credentials['twitter']['access_token'],
            self.api_credentials['twitter']['access_token_secret']
        )
        return tweepy.API(auth, wait_on_rate_limit=True)
    
    def collect_twitter_data(self, search_terms, date_range, max_tweets=1000):
        """Collect Twitter data for given search terms"""
        tweets_data = []
        
        for term in search_terms:
            try:
                # Search tweets
                tweets = tweepy.Cursor(
                    self.twitter_api.search_tweets,
                    q=term,
                    lang="en",
                    tweet_mode="extended",
                    until=date_range['end_date']
                ).items(max_tweets)
                
                for tweet in tweets:
                    tweets_data.append({
                        'platform': 'twitter',
                        'id': tweet.id,
                        'text': tweet.full_text,
                        'author': tweet.user.screen_name,
                        'author_followers': tweet.user.followers_count,
                        'created_at': tweet.created_at,
                        'retweet_count': tweet.retweet_count,
                        'favorite_count': tweet.favorite_count,
                        'search_term': term
                    })
                
                time.sleep(1)  # Respect rate limits
                
            except Exception as e:
                print(f"Error collecting data for term '{term}': {e}")
                continue
        
        return pd.DataFrame(tweets_data)
    
    def collect_reddit_data(self, subreddits, search_terms, date_range):
        """Collect Reddit data (requires praw library)"""
        # Implementation would require praw library
        # This is a placeholder for the structure
        reddit_data = []
        
        for subreddit in subreddits:
            for term in search_terms:
                # Reddit API implementation
                pass
        
        return pd.DataFrame(reddit_data)

def preprocess_social_media_data(df):
    """Preprocess social media data"""
    
    # Convert dates
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Calculate engagement metrics
    df['total_engagement'] = df['retweet_count'] + df['favorite_count']
    df['engagement_rate'] = df['total_engagement'] / df['author_followers']
    
    # Clean text
    df['cleaned_text'] = df['text'].str.replace(r'http\S+|www\S+|https\S+', '', regex=True)
    df['cleaned_text'] = df['cleaned_text'].str.replace(r'@\w+|#\w+', '', regex=True)
    df['cleaned_text'] = df['cleaned_text'].str.strip()
    
    return df

# Usage example
api_credentials = {
    'twitter': {
        'consumer_key': 'your_consumer_key',
        'consumer_secret': 'your_consumer_secret',
        'access_token': 'your_access_token',
        'access_token_secret': 'your_access_token_secret'
    }
}

collector = SocialMediaCollector(api_credentials)
search_terms = ['#AI', '#MachineLearning', '#DataScience']
date_range = {
    'start_date': '2024-01-01',
    'end_date': '2024-01-31'
}

tweets_df = collector.collect_twitter_data(search_terms, date_range, max_tweets=500)
tweets_df = preprocess_social_media_data(tweets_df)

print(f"Collected {len(tweets_df)} tweets")
print(tweets_df.head())
```

#### Sentiment Analysis
```python
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

class SocialMediaSentimentAnalyzer:
    def __init__(self, method='vader'):
        """Initialize sentiment analyzer"""
        self.method = method
        if method == 'vader':
            self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        if self.method == 'vader':
            scores = self.analyzer.polarity_scores(text)
            compound = scores['compound']
            
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'compound_score': compound,
                'positive_score': scores['pos'],
                'negative_score': scores['neg'],
                'neutral_score': scores['neu']
            }
        
        elif self.method == 'textblob':
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': blob.sentiment.subjectivity
            }
    
    def analyze_batch(self, texts):
        """Analyze sentiment for a batch of texts"""
        results = []
        
        for text in texts:
            if pd.isna(text) or text.strip() == '':
                results.append({
                    'sentiment': 'neutral',
                    'score': 0.0
                })
            else:
                result = self.analyze_sentiment(text)
                results.append({
                    'sentiment': result['sentiment'],
                    'score': result.get('compound_score', result.get('polarity', 0.0))
                })
        
        return results

def perform_sentiment_analysis(df):
    """Perform sentiment analysis on social media data"""
    
    analyzer = SocialMediaSentimentAnalyzer(method='vader')
    
    # Analyze sentiment
    sentiment_results = analyzer.analyze_batch(df['cleaned_text'].tolist())
    
    # Add sentiment columns
    df['sentiment'] = [result['sentiment'] for result in sentiment_results]
    df['sentiment_score'] = [result['score'] for result in sentiment_results]
    
    return df

def analyze_sentiment_trends(df):
    """Analyze sentiment trends over time"""
    
    # Group by date and sentiment
    daily_sentiment = df.groupby([df['created_at'].dt.date, 'sentiment']).size().unstack(fill_value=0)
    
    # Calculate sentiment percentages
    daily_sentiment_pct = daily_sentiment.div(daily_sentiment.sum(axis=1), axis=0) * 100
    
    # Calculate overall sentiment score
    daily_sentiment_score = df.groupby(df['created_at'].dt.date)['sentiment_score'].mean()
    
    return daily_sentiment_pct, daily_sentiment_score

# Usage example
tweets_df = perform_sentiment_analysis(tweets_df)
daily_sentiment_pct, daily_sentiment_score = analyze_sentiment_trends(tweets_df)

print("Sentiment Distribution:")
print(tweets_df['sentiment'].value_counts(normalize=True) * 100)

print("\nDaily Sentiment Trends:")
print(daily_sentiment_pct.head())
```

#### Trend Analysis
```python
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

class SocialMediaTrendAnalyzer:
    def __init__(self):
        """Initialize trend analyzer"""
        pass
    
    def extract_hashtags(self, text):
        """Extract hashtags from text"""
        hashtags = re.findall(r'#\w+', text.lower())
        return hashtags
    
    def extract_mentions(self, text):
        """Extract mentions from text"""
        mentions = re.findall(r'@\w+', text.lower())
        return mentions
    
    def analyze_trends(self, df, time_window='1D'):
        """Analyze trends over time"""
        
        # Extract hashtags and mentions
        all_hashtags = []
        all_mentions = []
        
        for text in df['text']:
            all_hashtags.extend(self.extract_hashtags(text))
            all_mentions.extend(self.extract_mentions(text))
        
        # Count frequencies
        hashtag_counts = Counter(all_hashtags)
        mention_counts = Counter(all_mentions)
        
        # Analyze trends over time
        df['date'] = df['created_at'].dt.date
        daily_hashtags = df.groupby('date').apply(
            lambda x: Counter([tag for text in x['text'] for tag in self.extract_hashtags(text)])
        )
        
        return {
            'hashtag_counts': hashtag_counts,
            'mention_counts': mention_counts,
            'daily_hashtags': daily_hashtags
        }
    
    def identify_trending_topics(self, df, min_mentions=5):
        """Identify trending topics"""
        
        # Extract hashtags
        all_hashtags = []
        for text in df['text']:
            all_hashtags.extend(self.extract_hashtags(text))
        
        # Count frequencies
        hashtag_counts = Counter(all_hashtags)
        
        # Filter by minimum mentions
        trending_hashtags = {tag: count for tag, count in hashtag_counts.items() 
                           if count >= min_mentions}
        
        # Sort by frequency
        trending_hashtags = dict(sorted(trending_hashtags.items(), 
                                      key=lambda x: x[1], reverse=True))
        
        return trending_hashtags

def visualize_trends(trend_data):
    """Visualize trend analysis results"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Social Media Trend Analysis', fontsize=16)
    
    # Top hashtags
    top_hashtags = dict(list(trend_data['hashtag_counts'].items())[:10])
    axes[0, 0].barh(list(top_hashtags.keys()), list(top_hashtags.values()))
    axes[0, 0].set_title('Top Hashtags')
    axes[0, 0].set_xlabel('Count')
    
    # Top mentions
    top_mentions = dict(list(trend_data['mention_counts'].items())[:10])
    axes[0, 1].barh(list(top_mentions.keys()), list(top_mentions.values()))
    axes[0, 1].set_title('Top Mentions')
    axes[0, 1].set_xlabel('Count')
    
    # Daily hashtag trends
    daily_hashtags = trend_data['daily_hashtags']
    if not daily_hashtags.empty:
        # Get top hashtags for visualization
        top_hashtags_list = list(trend_data['hashtag_counts'].keys())[:5]
        
        for hashtag in top_hashtags_list:
            hashtag_counts = [daily_hashtags.get(date, {}).get(hashtag, 0) 
                            for date in daily_hashtags.index]
            axes[1, 0].plot(daily_hashtags.index, hashtag_counts, label=hashtag)
        
        axes[1, 0].set_title('Daily Hashtag Trends')
        axes[1, 0].set_xlabel('Date')
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].legend()
        axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Sentiment over time
    daily_sentiment_pct, daily_sentiment_score = analyze_sentiment_trends(tweets_df)
    axes[1, 1].plot(daily_sentiment_score.index, daily_sentiment_score.values)
    axes[1, 1].set_title('Sentiment Score Over Time')
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Sentiment Score')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('social_media_trends.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
trend_analyzer = SocialMediaTrendAnalyzer()
trend_data = trend_analyzer.analyze_trends(tweets_df)
trending_topics = trend_analyzer.identify_trending_topics(tweets_df, min_mentions=3)

visualize_trends(trend_data)

print("Trending Topics:")
for topic, count in list(trending_topics.items())[:10]:
    print(f"{topic}: {count} mentions")
```

#### Influencer Analysis
```python
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

class InfluencerAnalyzer:
    def __init__(self):
        """Initialize influencer analyzer"""
        pass
    
    def calculate_influence_score(self, df):
        """Calculate influence score for each user"""
        
        # Group by author
        author_stats = df.groupby('author').agg({
            'author_followers': 'first',
            'total_engagement': 'sum',
            'retweet_count': 'sum',
            'favorite_count': 'sum',
            'id': 'count'  # Number of posts
        }).rename(columns={'id': 'post_count'})
        
        # Calculate engagement rate
        author_stats['engagement_rate'] = author_stats['total_engagement'] / author_stats['author_followers']
        
        # Calculate influence score (weighted combination)
        author_stats['influence_score'] = (
            author_stats['engagement_rate'] * 0.4 +
            (author_stats['author_followers'] / author_stats['author_followers'].max()) * 0.3 +
            (author_stats['post_count'] / author_stats['post_count'].max()) * 0.3
        )
        
        return author_stats
    
    def identify_top_influencers(self, df, top_n=10):
        """Identify top influencers"""
        
        author_stats = self.calculate_influence_score(df)
        
        # Sort by influence score
        top_influencers = author_stats.sort_values('influence_score', ascending=False).head(top_n)
        
        return top_influencers
    
    def analyze_influencer_network(self, df, min_interactions=2):
        """Analyze influencer network based on interactions"""
        
        # Extract mentions and create network
        network_data = []
        
        for _, row in df.iterrows():
            mentions = re.findall(r'@(\w+)', row['text'])
            for mention in mentions:
                network_data.append({
                    'source': row['author'],
                    'target': mention,
                    'weight': row['total_engagement']
                })
        
        # Create network
        G = nx.DiGraph()
        
        for edge in network_data:
            if G.has_edge(edge['source'], edge['target']):
                G[edge['source']][edge['target']]['weight'] += edge['weight']
            else:
                G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
        
        # Calculate network metrics
        network_metrics = {
            'nodes': list(G.nodes()),
            'edges': list(G.edges(data=True)),
            'in_degree_centrality': nx.in_degree_centrality(G),
            'out_degree_centrality': nx.out_degree_centrality(G),
            'betweenness_centrality': nx.betweenness_centrality(G),
            'pagerank': nx.pagerank(G)
        }
        
        return G, network_metrics

def visualize_influencer_analysis(top_influencers, network_metrics):
    """Visualize influencer analysis results"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Influencer Analysis', fontsize=16)
    
    # Top influencers by influence score
    top_10 = top_influencers.head(10)
    axes[0, 0].barh(range(len(top_10)), top_10['influence_score'])
    axes[0, 0].set_yticks(range(len(top_10)))
    axes[0, 0].set_yticklabels(top_10.index)
    axes[0, 0].set_title('Top Influencers by Influence Score')
    axes[0, 0].set_xlabel('Influence Score')
    
    # Engagement rate vs follower count
    axes[0, 1].scatter(top_influencers['author_followers'], 
                      top_influencers['engagement_rate'], 
                      alpha=0.6)
    axes[0, 1].set_xlabel('Follower Count')
    axes[0, 1].set_ylabel('Engagement Rate')
    axes[0, 1].set_title('Engagement Rate vs Follower Count')
    axes[0, 1].set_xscale('log')
    
    # Post count distribution
    axes[1, 0].hist(top_influencers['post_count'], bins=20, alpha=0.7)
    axes[1, 0].set_xlabel('Post Count')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Post Count Distribution')
    
    # Network centrality (if network exists)
    if network_metrics['nodes']:
        centrality_data = pd.DataFrame({
            'user': list(network_metrics['in_degree_centrality'].keys()),
            'in_degree': list(network_metrics['in_degree_centrality'].values()),
            'out_degree': list(network_metrics['out_degree_centrality'].values()),
            'betweenness': list(network_metrics['betweenness_centrality'].values()),
            'pagerank': list(network_metrics['pagerank'].values())
        })
        
        # Top users by PageRank
        top_network_users = centrality_data.nlargest(10, 'pagerank')
        axes[1, 1].barh(range(len(top_network_users)), top_network_users['pagerank'])
        axes[1, 1].set_yticks(range(len(top_network_users)))
        axes[1, 1].set_yticklabels(top_network_users['user'])
        axes[1, 1].set_title('Top Users by PageRank')
        axes[1, 1].set_xlabel('PageRank Score')
    
    plt.tight_layout()
    plt.savefig('influencer_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_interactive_influencer_network(G, network_metrics):
    """Create interactive network visualization"""
    
    # Get node positions
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Prepare node data
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = [f"User: {node}<br>PageRank: {network_metrics['pagerank'].get(node, 0):.3f}" 
                for node in G.nodes()]
    
    # Node sizes based on PageRank
    node_sizes = [network_metrics['pagerank'].get(node, 0) * 1000 + 10 for node in G.nodes()]
    
    # Prepare edge data
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    # Create edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_sizes,
            color=node_sizes,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="PageRank"),
            line=dict(width=2, color='white')))
    
    # Create layout
    layout = go.Layout(
        title='Influencer Network',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    
    return fig

# Usage example
influencer_analyzer = InfluencerAnalyzer()
top_influencers = influencer_analyzer.identify_top_influencers(tweets_df, top_n=20)
G, network_metrics = influencer_analyzer.analyze_influencer_network(tweets_df)

visualize_influencer_analysis(top_influencers, network_metrics)

# Create interactive network
if network_metrics['nodes']:
    interactive_network = create_interactive_influencer_network(G, network_metrics)
    interactive_network.write_html('influencer_network.html')

print("Top Influencers:")
print(top_influencers[['author_followers', 'engagement_rate', 'post_count', 'influence_score']].head(10))
```

### Error Handling
- Handle API rate limits and connection errors
- Validate data quality and handle missing values
- Manage platform-specific API restrictions
- Handle authentication and authorization errors
- Ensure data privacy and compliance

### Monitoring
- Track API usage and rate limit consumption
- Monitor data collection performance and accuracy
- Review sentiment analysis quality and consistency
- Validate trend detection accuracy
- Monitor influencer identification relevance

### Best Practices
1. **API Management**: Respect rate limits and implement proper error handling
2. **Data Quality**: Validate and clean social media data before analysis
3. **Privacy Compliance**: Ensure compliance with platform terms and privacy regulations
4. **Sentiment Analysis**: Use appropriate sentiment models for different contexts
5. **Trend Detection**: Implement robust algorithms for trend identification
6. **Influencer Analysis**: Consider multiple metrics for comprehensive influencer evaluation
7. **Real-time Monitoring**: Implement efficient real-time data collection and analysis
8. **Data Storage**: Use appropriate storage solutions for large-scale social media data
