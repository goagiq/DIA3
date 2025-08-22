#!/usr/bin/env python3
"""
Sentiment Analysis Module for Enhanced Reports
Provides comprehensive sentiment analysis capabilities for strategic analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class SentimentAnalyzer:
    """Advanced sentiment analysis for strategic content."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        self.results = {}
        self.plots = {}
        
    def analyze_text_sentiment(self, text: str, title: str = "Text Sentiment Analysis") -> Dict[str, Any]:
        """Analyze sentiment of a given text."""
        try:
            # Simple rule-based sentiment analysis (can be enhanced with ML models)
            positive_words = [
                'success', 'advantage', 'benefit', 'improve', 'enhance', 'strong', 
                'capable', 'effective', 'efficient', 'powerful', 'strategic', 'win',
                'gain', 'profit', 'growth', 'development', 'progress', 'advance',
                'superior', 'excellent', 'outstanding', 'positive', 'favorable'
            ]
            
            negative_words = [
                'risk', 'threat', 'danger', 'weak', 'vulnerable', 'fail', 'loss',
                'damage', 'harm', 'problem', 'issue', 'challenge', 'difficulty',
                'weakness', 'deficit', 'decline', 'reduction', 'negative', 'poor',
                'inadequate', 'insufficient', 'unreliable', 'unstable', 'crisis'
            ]
            
            neutral_words = [
                'analysis', 'assessment', 'evaluation', 'review', 'study', 'report',
                'data', 'information', 'fact', 'figure', 'statistic', 'measure',
                'indicator', 'metric', 'parameter', 'variable', 'factor', 'element'
            ]
            
            # Convert to lowercase for analysis
            text_lower = text.lower()
            words = text_lower.split()
            
            # Count sentiment words
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            neutral_count = sum(1 for word in words if word in neutral_words)
            total_words = len(words)
            
            # Calculate sentiment scores
            positive_score = positive_count / total_words if total_words > 0 else 0
            negative_score = negative_count / total_words if total_words > 0 else 0
            neutral_score = neutral_count / total_words if total_words > 0 else 0
            
            # Overall sentiment score (-1 to 1)
            overall_sentiment = (positive_score - negative_score) / (positive_score + negative_score + 1e-8)
            
            # Sentiment classification
            if overall_sentiment > 0.1:
                sentiment_class = "Positive"
                sentiment_color = "#28a745"
            elif overall_sentiment < -0.1:
                sentiment_class = "Negative"
                sentiment_color = "#dc3545"
            else:
                sentiment_class = "Neutral"
                sentiment_color = "#6c757d"
            
            # Emotion analysis (simplified)
            emotions = {
                "confidence": positive_count * 0.3,
                "concern": negative_count * 0.4,
                "optimism": positive_count * 0.2,
                "caution": negative_count * 0.3,
                "neutrality": neutral_count * 0.5
            }
            
            # Key phrases extraction (simplified)
            key_phrases = []
            sentences = text.split('.')
            for sentence in sentences[:5]:  # Top 5 sentences
                if any(word in sentence.lower() for word in positive_words + negative_words):
                    key_phrases.append(sentence.strip())
            
            return {
                "title": title,
                "text_length": len(text),
                "word_count": total_words,
                "sentiment_scores": {
                    "positive": positive_score,
                    "negative": negative_score,
                    "neutral": neutral_score,
                    "overall": overall_sentiment
                },
                "sentiment_classification": {
                    "class": sentiment_class,
                    "color": sentiment_color,
                    "confidence": abs(overall_sentiment)
                },
                "emotions": emotions,
                "key_phrases": key_phrases[:5],
                "word_counts": {
                    "positive": positive_count,
                    "negative": negative_count,
                    "neutral": neutral_count
                }
            }
            
        except Exception as e:
            return {
                "error": f"Sentiment analysis failed: {str(e)}",
                "sentiment_scores": {"positive": 0, "negative": 0, "neutral": 0, "overall": 0},
                "sentiment_classification": {"class": "Error", "color": "#6c757d", "confidence": 0}
            }
    
    def analyze_multiple_texts(self, texts: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze sentiment across multiple text samples."""
        results = []
        overall_sentiments = []
        
        for text_data in texts:
            result = self.analyze_text_sentiment(text_data['text'], text_data.get('title', 'Text Analysis'))
            results.append(result)
            overall_sentiments.append(result['sentiment_scores']['overall'])
        
        # Aggregate analysis
        avg_sentiment = np.mean(overall_sentiments) if overall_sentiments else 0
        sentiment_std = np.std(overall_sentiments) if overall_sentiments else 0
        
        # Sentiment distribution
        positive_count = sum(1 for s in overall_sentiments if s > 0.1)
        negative_count = sum(1 for s in overall_sentiments if s < -0.1)
        neutral_count = sum(1 for s in overall_sentiments if -0.1 <= s <= 0.1)
        
        return {
            "individual_results": results,
            "aggregate_analysis": {
                "average_sentiment": avg_sentiment,
                "sentiment_std": sentiment_std,
                "sentiment_distribution": {
                    "positive": positive_count,
                    "negative": negative_count,
                    "neutral": neutral_count,
                    "total": len(overall_sentiments)
                },
                "sentiment_range": {
                    "min": min(overall_sentiments) if overall_sentiments else 0,
                    "max": max(overall_sentiments) if overall_sentiments else 0
                }
            }
        }
    
    def generate_sentiment_report(self, analysis_results: Dict[str, Any], output_path: str = None) -> str:
        """Generate comprehensive sentiment analysis report."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_path is None:
                output_path = f"Results/sentiment_analysis_report_{timestamp}.html"
            
            # Create HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Sentiment Analysis Report</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 10px; }}
                    .section {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }}
                    .metric {{ display: inline-block; margin: 10px; padding: 15px; background: white; border-radius: 8px; text-align: center; }}
                    .metric-value {{ font-size: 2em; font-weight: bold; }}
                    .positive {{ color: #28a745; }}
                    .negative {{ color: #dc3545; }}
                    .neutral {{ color: #6c757d; }}
                    .chart-container {{ width: 100%; max-width: 600px; margin: 20px auto; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Sentiment Analysis Report</h1>
                    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                
                <div class="section">
                    <h2>Overall Sentiment Summary</h2>
                    <div class="metric">
                        <div class="metric-value {'positive' if analysis_results.get('aggregate_analysis', {}).get('average_sentiment', 0) > 0 else 'negative' if analysis_results.get('aggregate_analysis', {}).get('average_sentiment', 0) < 0 else 'neutral'}">
                            {analysis_results.get('aggregate_analysis', {}).get('average_sentiment', 0):.3f}
                        </div>
                        <div>Average Sentiment</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">
                            {analysis_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('positive', 0)}
                        </div>
                        <div>Positive Texts</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">
                            {analysis_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('negative', 0)}
                        </div>
                        <div>Negative Texts</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Sentiment Distribution</h2>
                    <div class="chart-container">
                        <canvas id="sentimentChart"></canvas>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Individual Text Analysis</h2>
                    {self._generate_individual_analysis_html(analysis_results.get('individual_results', []))}
                </div>
                
                <script>
                    // Sentiment Distribution Chart
                    const ctx = document.getElementById('sentimentChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'doughnut',
                        data: {{
                            labels: ['Positive', 'Negative', 'Neutral'],
                            datasets: [{{
                                data: [
                                    {analysis_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('positive', 0)},
                                    {analysis_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('negative', 0)},
                                    {analysis_results.get('aggregate_analysis', {}).get('sentiment_distribution', {}).get('neutral', 0)}
                                ],
                                backgroundColor: ['#28a745', '#dc3545', '#6c757d']
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                legend: {{ position: 'bottom' }}
                            }}
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            
            # Save report
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
            
        except Exception as e:
            return f"Report generation failed: {str(e)}"
    
    def _generate_individual_analysis_html(self, results: List[Dict[str, Any]]) -> str:
        """Generate HTML for individual text analysis."""
        html = ""
        for i, result in enumerate(results):
            sentiment_class = result.get('sentiment_classification', {}).get('class', 'Unknown')
            sentiment_color = result.get('sentiment_classification', {}).get('color', '#6c757d')
            overall_score = result.get('sentiment_scores', {}).get('overall', 0)
            
            html += f"""
            <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 8px; border-left: 5px solid {sentiment_color};">
                <h3>{result.get('title', f'Text {i+1}')}</h3>
                <p><strong>Sentiment:</strong> <span style="color: {sentiment_color};">{sentiment_class}</span></p>
                <p><strong>Score:</strong> {overall_score:.3f}</p>
                <p><strong>Word Count:</strong> {result.get('word_count', 0)}</p>
            </div>
            """
        
        return html

# Create global instance
sentiment_analyzer = SentimentAnalyzer()


