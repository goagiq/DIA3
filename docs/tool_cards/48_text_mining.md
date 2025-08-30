# Text Mining Tool

## Overview
The Text Mining tool provides comprehensive capabilities for extracting insights, patterns, and knowledge from textual data through advanced text analysis, natural language processing, and document mining techniques to support text intelligence and content understanding.

## Purpose
To analyze large volumes of textual data, extract meaningful patterns, identify key topics, perform sentiment analysis, and discover hidden insights from documents, enabling text-based intelligence and content understanding for business, research, and operational decision-making.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing and statistical analysis
- **matplotlib** (>=3.7.0) - Data visualization and charting
- **seaborn** (>=0.12.0) - Statistical data visualization

### Optional Libraries
- **nltk** (>=3.8.0) - Natural language processing toolkit
- **spacy** (>=3.6.0) - Advanced NLP and text processing
- **gensim** (>=4.3.0) - Topic modeling and document similarity
- **scikit-learn** (>=1.3.0) - Machine learning for text analysis
- **transformers** (>=4.30.0) - Pre-trained language models
- **torch** (>=2.0.0) - Deep learning framework
- **plotly** (>=5.15.0) - Interactive visualizations
- **wordcloud** (>=1.9.0) - Word cloud generation
- **textblob** (>=0.17.0) - Text processing and sentiment analysis
- **pyLDAvis** (>=3.4.0) - Topic model visualization
- **textstat** (>=0.7.0) - Text statistics and readability
- **langdetect** (>=1.0.9) - Language detection
- **polyglot** (>=16.7.0) - Multilingual text processing
- **rake-nltk** (>=1.0.6) - Keyword extraction
- **sumy** (>=0.11.0) - Text summarization

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "text_data": {
      "type": "object",
      "properties": {
        "documents": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {"type": "string"},
              "text": {"type": "string"},
              "metadata": {
                "type": "object",
                "properties": {
                  "title": {"type": "string"},
                  "author": {"type": "string"},
                  "date": {"type": "string"},
                  "source": {"type": "string"},
                  "category": {"type": "string"}
                }
              }
            }
          }
        },
        "language": {"type": "string"},
        "encoding": {"type": "string"}
      }
    },
    "analysis_config": {
      "type": "object",
      "properties": {
        "analysis_type": {
          "type": "string",
          "enum": ["topic_modeling", "keyword_extraction", "sentiment_analysis", "text_classification", "named_entity_recognition", "document_similarity", "text_summarization", "text_clustering"]
        },
        "text_processing": {
          "type": "object",
          "properties": {
            "remove_stopwords": {"type": "boolean"},
            "lemmatization": {"type": "boolean"},
            "stemming": {"type": "boolean"},
            "lowercase": {"type": "boolean"},
            "remove_punctuation": {"type": "boolean"},
            "min_word_length": {"type": "integer"}
          }
        },
        "model_config": {
          "type": "object",
          "properties": {
            "model_type": {
              "type": "string",
              "enum": ["lda", "lsa", "bert", "word2vec", "doc2vec", "tfidf", "count_vectorizer"]
            },
            "num_topics": {"type": "integer"},
            "max_features": {"type": "integer"},
            "ngram_range": {
              "type": "array",
              "items": {"type": "integer"}
            }
          }
        }
      }
    },
    "visualization_config": {
      "type": "object",
      "properties": {
        "chart_type": {
          "type": "string",
          "enum": ["wordcloud", "topic_visualization", "sentiment_distribution", "keyword_network", "document_clustering"]
        },
        "interactive": {"type": "boolean"},
        "color_scheme": {"type": "string"}
      }
    }
  },
  "required": ["text_data", "analysis_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "text_analysis_results": {
      "type": "object",
      "properties": {
        "topic_modeling": {
          "type": "object",
          "properties": {
            "topics": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "topic_id": {"type": "integer"},
                  "keywords": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "word": {"type": "string"},
                        "weight": {"type": "number"}
                      }
                    }
                  },
                  "coherence_score": {"type": "number"}
                }
              }
            },
            "document_topics": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "document_id": {"type": "string"},
                  "topic_distribution": {
                    "type": "object",
                    "additionalProperties": {"type": "number"}
                  },
                  "dominant_topic": {"type": "integer"}
                }
              }
            }
          }
        },
        "keyword_extraction": {
          "type": "object",
          "properties": {
            "keywords": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "keyword": {"type": "string"},
                  "score": {"type": "number"},
                  "frequency": {"type": "integer"},
                  "document_frequency": {"type": "integer"}
                }
              }
            },
            "keyword_phrases": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "phrase": {"type": "string"},
                  "score": {"type": "number"},
                  "frequency": {"type": "integer"}
                }
              }
            }
          }
        },
        "sentiment_analysis": {
          "type": "object",
          "properties": {
            "document_sentiments": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "document_id": {"type": "string"},
                  "sentiment_score": {"type": "number"},
                  "sentiment_label": {"type": "string"},
                  "confidence": {"type": "number"}
                }
              }
            },
            "overall_sentiment": {
              "type": "object",
              "properties": {
                "average_sentiment": {"type": "number"},
                "sentiment_distribution": {
                  "type": "object",
                  "properties": {
                    "positive": {"type": "number"},
                    "neutral": {"type": "number"},
                    "negative": {"type": "number"}
                  }
                }
              }
            }
          }
        },
        "text_classification": {
          "type": "object",
          "properties": {
            "classifications": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "document_id": {"type": "string"},
                  "predicted_class": {"type": "string"},
                  "confidence": {"type": "number"},
                  "class_probabilities": {
                    "type": "object",
                    "additionalProperties": {"type": "number"}
                  }
                }
              }
            },
            "classification_metrics": {
              "type": "object",
              "properties": {
                "accuracy": {"type": "number"},
                "precision": {"type": "number"},
                "recall": {"type": "number"},
                "f1_score": {"type": "number"}
              }
            }
          }
        },
        "named_entity_recognition": {
          "type": "object",
          "properties": {
            "entities": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "document_id": {"type": "string"},
                  "entities": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "text": {"type": "string"},
                        "type": {"type": "string"},
                        "start_pos": {"type": "integer"},
                        "end_pos": {"type": "integer"},
                        "confidence": {"type": "number"}
                      }
                    }
                  }
                }
              }
            },
            "entity_statistics": {
              "type": "object",
              "properties": {
                "entity_types": {
                  "type": "object",
                  "additionalProperties": {"type": "integer"}
                },
                "most_common_entities": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "entity": {"type": "string"},
                      "type": {"type": "string"},
                      "frequency": {"type": "integer"}
                    }
                  }
                }
              }
            }
          }
        },
        "document_similarity": {
          "type": "object",
          "properties": {
            "similarity_matrix": {
              "type": "array",
              "items": {
                "type": "array",
                "items": {"type": "number"}
              }
            },
            "similar_documents": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "document_id": {"type": "string"},
                  "similar_documents": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "similar_document_id": {"type": "string"},
                        "similarity_score": {"type": "number"}
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "text_summarization": {
          "type": "object",
          "properties": {
            "summaries": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "document_id": {"type": "string"},
                  "summary": {"type": "string"},
                  "summary_length": {"type": "integer"},
                  "compression_ratio": {"type": "number"},
                  "key_sentences": {
                    "type": "array",
                    "items": {"type": "string"}
                  }
                }
              }
            }
          }
        }
      }
    },
    "text_statistics": {
      "type": "object",
      "properties": {
        "document_statistics": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "document_id": {"type": "string"},
              "word_count": {"type": "integer"},
              "sentence_count": {"type": "integer"},
              "average_sentence_length": {"type": "number"},
              "readability_score": {"type": "number"},
              "lexical_diversity": {"type": "number"}
            }
          }
        },
        "corpus_statistics": {
          "type": "object",
          "properties": {
            "total_documents": {"type": "integer"},
            "total_words": {"type": "integer"},
            "vocabulary_size": {"type": "integer"},
            "average_document_length": {"type": "number"},
            "most_common_words": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "word": {"type": "string"},
                  "frequency": {"type": "integer"}
                }
              }
            }
          }
        }
      }
    },
    "visualizations": {
      "type": "object",
      "properties": {
        "wordcloud": {"type": "string"},
        "topic_visualization": {"type": "string"},
        "sentiment_distribution": {"type": "string"},
        "keyword_network": {"type": "string"},
        "document_clustering": {"type": "string"}
      }
    },
    "text_insights": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "insight": {"type": "string"},
          "document_id": {"type": "string"},
          "metric": {"type": "string"},
          "value": {"type": "number"},
          "significance": {"type": "string"}
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for text mining analysis in seconds"
    }
  }
}
```

## Intended Use
- **Topic Modeling**: Discover hidden topics and themes in document collections
- **Keyword Extraction**: Identify important keywords and phrases
- **Sentiment Analysis**: Analyze sentiment and emotional tone
- **Text Classification**: Categorize documents into predefined classes
- **Named Entity Recognition**: Extract and classify named entities
- **Document Similarity**: Find similar documents and content
- **Text Summarization**: Generate concise summaries of documents
- **Text Clustering**: Group similar documents together

## Limitations
- Analysis quality depends on text data quality and preprocessing
- Some models may require significant computational resources
- Language-specific models may not work for all languages
- Context-dependent interpretations may vary

## Safety
- Validate text data quality and encoding
- Consider privacy implications of text analysis
- Handle sensitive textual information appropriately
- Ensure text mining methods are appropriate for the data

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn nltk spacy gensim scikit-learn transformers
   ```

2. **Download NLTK Data**:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('averaged_perceptron_tagger')
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
   import nltk
   import spacy
   import gensim
   from sklearn.feature_extraction.text import TfidfVectorizer
   ```

### Usage

#### Text Preprocessing and Basic Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text, remove_stopwords=True, lemmatize=True):
    """Preprocess text data"""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Remove short tokens
    tokens = [token for token in tokens if len(token) > 2]
    
    return ' '.join(tokens)

def analyze_text_statistics(documents):
    """Analyze basic text statistics"""
    
    stats = []
    
    for doc in documents:
        # Basic statistics
        word_count = len(doc['text'].split())
        sentence_count = len(sent_tokenize(doc['text']))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Vocabulary analysis
        words = doc['text'].lower().split()
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words) if words else 0
        
        # Readability (Flesch Reading Ease approximation)
        syllables = sum(1 for word in words for char in word if char in 'aeiou')
        readability = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllables / word_count) if word_count > 0 else 0
        
        stats.append({
            'document_id': doc['id'],
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_sentence_length': avg_sentence_length,
            'vocabulary_size': len(unique_words),
            'lexical_diversity': lexical_diversity,
            'readability_score': readability
        })
    
    return pd.DataFrame(stats)

def create_word_frequency_analysis(documents, top_n=20):
    """Create word frequency analysis"""
    
    # Combine all documents
    all_text = ' '.join([doc['text'] for doc in documents])
    
    # Preprocess
    processed_text = preprocess_text(all_text)
    
    # Count word frequencies
    words = processed_text.split()
    word_freq = {}
    
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top words
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    return dict(top_words)

def visualize_text_statistics(stats_df):
    """Visualize text statistics"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Text Statistics Analysis', fontsize=16)
    
    # Word count distribution
    axes[0, 0].hist(stats_df['word_count'], bins=20, alpha=0.7, color='skyblue')
    axes[0, 0].set_title('Word Count Distribution')
    axes[0, 0].set_xlabel('Word Count')
    axes[0, 0].set_ylabel('Frequency')
    
    # Sentence count distribution
    axes[0, 1].hist(stats_df['sentence_count'], bins=20, alpha=0.7, color='lightgreen')
    axes[0, 1].set_title('Sentence Count Distribution')
    axes[0, 1].set_xlabel('Sentence Count')
    axes[0, 1].set_ylabel('Frequency')
    
    # Lexical diversity
    axes[1, 0].hist(stats_df['lexical_diversity'], bins=20, alpha=0.7, color='salmon')
    axes[1, 0].set_title('Lexical Diversity Distribution')
    axes[1, 0].set_xlabel('Lexical Diversity')
    axes[1, 0].set_ylabel('Frequency')
    
    # Readability scores
    axes[1, 1].hist(stats_df['readability_score'], bins=20, alpha=0.7, color='gold')
    axes[1, 1].set_title('Readability Score Distribution')
    axes[1, 1].set_xlabel('Readability Score')
    axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('text_statistics.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
documents = [
    {'id': 'doc1', 'text': 'This is a sample document about machine learning and artificial intelligence.'},
    {'id': 'doc2', 'text': 'Another document discussing data science and statistical analysis.'},
    {'id': 'doc3', 'text': 'A third document covering natural language processing and text mining.'}
]

# Preprocess documents
for doc in documents:
    doc['processed_text'] = preprocess_text(doc['text'])

# Analyze statistics
stats_df = analyze_text_statistics(documents)
word_freq = create_word_frequency_analysis(documents)
visualize_text_statistics(stats_df)

print("Text Statistics:")
print(stats_df)
print("\nTop Words:")
for word, freq in list(word_freq.items())[:10]:
    print(f"{word}: {freq}")
```

#### Topic Modeling with LDA
```python
from gensim import corpora, models
from gensim.models import LdaModel
import pyLDAvis
import pyLDAvis.gensim_models
import numpy as np

def create_topic_model(documents, num_topics=3, passes=15):
    """Create LDA topic model"""
    
    # Prepare documents
    processed_docs = [doc['processed_text'].split() for doc in documents]
    
    # Create dictionary
    dictionary = corpora.Dictionary(processed_docs)
    
    # Filter extreme frequencies
    dictionary.filter_extremes(no_below=1, no_above=0.7)
    
    # Create document-term matrix
    corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    
    # Train LDA model
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=passes,
        alpha='auto',
        per_word_topics=True
    )
    
    return lda_model, dictionary, corpus

def analyze_topics(lda_model, num_words=10):
    """Analyze topics from LDA model"""
    
    topics = []
    
    for topic_id in range(lda_model.num_topics):
        topic_words = lda_model.show_topic(topic_id, num_words)
        
        topics.append({
            'topic_id': topic_id,
            'keywords': [{'word': word, 'weight': weight} for word, weight in topic_words],
            'coherence_score': 0.0  # Would need coherence model for actual score
        })
    
    return topics

def get_document_topics(lda_model, corpus, documents):
    """Get topic distribution for each document"""
    
    document_topics = []
    
    for i, doc in enumerate(documents):
        doc_topics = lda_model.get_document_topics(corpus[i])
        
        # Convert to dictionary
        topic_dist = {topic_id: weight for topic_id, weight in doc_topics}
        
        # Find dominant topic
        dominant_topic = max(doc_topics, key=lambda x: x[1])[0]
        
        document_topics.append({
            'document_id': doc['id'],
            'topic_distribution': topic_dist,
            'dominant_topic': dominant_topic
        })
    
    return document_topics

def visualize_topics(lda_model, corpus, dictionary):
    """Create interactive topic visualization"""
    
    # Prepare visualization data
    vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    
    # Save as HTML
    pyLDAvis.save_html(vis_data, 'topic_visualization.html')
    
    return vis_data

def create_topic_summary(topics, document_topics):
    """Create summary of topic modeling results"""
    
    summary = {
        'total_topics': len(topics),
        'topic_summary': [],
        'document_classification': {}
    }
    
    # Topic summary
    for topic in topics:
        top_words = [item['word'] for item in topic['keywords'][:5]]
        summary['topic_summary'].append({
            'topic_id': topic['topic_id'],
            'main_keywords': top_words,
            'keyword_string': ', '.join(top_words)
        })
    
    # Document classification
    for doc_topic in document_topics:
        summary['document_classification'][doc_topic['document_id']] = {
            'dominant_topic': doc_topic['dominant_topic'],
            'topic_confidence': doc_topic['topic_distribution'][doc_topic['dominant_topic']]
        }
    
    return summary

# Usage example
lda_model, dictionary, corpus = create_topic_model(documents, num_topics=2)
topics = analyze_topics(lda_model)
document_topics = get_document_topics(lda_model, corpus, documents)
vis_data = visualize_topics(lda_model, corpus, dictionary)
topic_summary = create_topic_summary(topics, document_topics)

print("Topic Modeling Results:")
for topic in topics:
    print(f"\nTopic {topic['topic_id']}:")
    for keyword in topic['keywords'][:5]:
        print(f"  {keyword['word']}: {keyword['weight']:.3f}")

print("\nDocument Classifications:")
for doc_id, classification in topic_summary['document_classification'].items():
    print(f"{doc_id}: Topic {classification['dominant_topic']} (confidence: {classification['topic_confidence']:.3f})")
```

#### Sentiment Analysis
```python
from textblob import TextBlob
from transformers import pipeline
import numpy as np

def perform_sentiment_analysis(documents, method='textblob'):
    """Perform sentiment analysis on documents"""
    
    if method == 'textblob':
        return perform_textblob_sentiment(documents)
    elif method == 'transformers':
        return perform_transformer_sentiment(documents)
    else:
        raise ValueError("Method must be 'textblob' or 'transformers'")

def perform_textblob_sentiment(documents):
    """Perform sentiment analysis using TextBlob"""
    
    results = []
    
    for doc in documents:
        blob = TextBlob(doc['text'])
        
        # Get polarity (-1 to 1)
        polarity = blob.sentiment.polarity
        
        # Get subjectivity (0 to 1)
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment_label = 'positive'
        elif polarity < -0.1:
            sentiment_label = 'negative'
        else:
            sentiment_label = 'neutral'
        
        # Confidence based on polarity magnitude
        confidence = abs(polarity)
        
        results.append({
            'document_id': doc['id'],
            'sentiment_score': polarity,
            'sentiment_label': sentiment_label,
            'subjectivity': subjectivity,
            'confidence': confidence
        })
    
    return results

def perform_transformer_sentiment(documents):
    """Perform sentiment analysis using transformers"""
    
    # Load sentiment analysis pipeline
    sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
    
    results = []
    
    for doc in documents:
        # Analyze sentiment
        result = sentiment_pipeline(doc['text'][:512])  # Limit text length
        
        # Map labels to standard format
        label_mapping = {
            'LABEL_0': 'negative',
            'LABEL_1': 'neutral', 
            'LABEL_2': 'positive'
        }
        
        sentiment_label = label_mapping.get(result[0]['label'], 'neutral')
        confidence = result[0]['score']
        
        # Convert to polarity score (-1 to 1)
        if sentiment_label == 'positive':
            polarity = confidence
        elif sentiment_label == 'negative':
            polarity = -confidence
        else:
            polarity = 0
        
        results.append({
            'document_id': doc['id'],
            'sentiment_score': polarity,
            'sentiment_label': sentiment_label,
            'confidence': confidence
        })
    
    return results

def analyze_sentiment_distribution(sentiment_results):
    """Analyze overall sentiment distribution"""
    
    # Count sentiment labels
    sentiment_counts = {}
    for result in sentiment_results:
        label = result['sentiment_label']
        sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
    
    # Calculate average sentiment
    avg_sentiment = np.mean([result['sentiment_score'] for result in sentiment_results])
    
    # Calculate sentiment distribution percentages
    total_docs = len(sentiment_results)
    sentiment_distribution = {
        label: count / total_docs for label, count in sentiment_counts.items()
    }
    
    return {
        'average_sentiment': avg_sentiment,
        'sentiment_distribution': sentiment_distribution,
        'sentiment_counts': sentiment_counts
    }

def visualize_sentiment_analysis(sentiment_results, distribution):
    """Visualize sentiment analysis results"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Sentiment Analysis Results', fontsize=16)
    
    # Sentiment distribution pie chart
    labels = list(distribution['sentiment_distribution'].keys())
    sizes = list(distribution['sentiment_distribution'].values())
    colors = ['red', 'gray', 'green']
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Sentiment Distribution')
    
    # Sentiment scores histogram
    sentiment_scores = [result['sentiment_score'] for result in sentiment_results]
    ax2.hist(sentiment_scores, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.axvline(distribution['average_sentiment'], color='red', linestyle='--', 
                label=f'Average: {distribution["average_sentiment"]:.3f}')
    ax2.set_title('Sentiment Score Distribution')
    ax2.set_xlabel('Sentiment Score')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('sentiment_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Usage example
sentiment_results = perform_sentiment_analysis(documents, method='textblob')
sentiment_distribution = analyze_sentiment_distribution(sentiment_results)
visualize_sentiment_analysis(sentiment_results, sentiment_distribution)

print("Sentiment Analysis Results:")
for result in sentiment_results:
    print(f"{result['document_id']}: {result['sentiment_label']} (score: {result['sentiment_score']:.3f})")

print(f"\nOverall Sentiment: {sentiment_distribution['average_sentiment']:.3f}")
print("Sentiment Distribution:")
for label, percentage in sentiment_distribution['sentiment_distribution'].items():
    print(f"  {label}: {percentage:.1%}")
```

### Error Handling
- Validate text data quality and encoding
- Handle missing or malformed text data
- Manage computational complexity for large documents
- Ensure text mining parameters are appropriate

### Monitoring
- Track text mining performance and accuracy
- Monitor model quality and topic coherence
- Review sentiment analysis accuracy
- Validate text classification results

### Best Practices
1. **Data Quality**: Ensure high-quality text data and proper preprocessing
2. **Language Support**: Use appropriate models for different languages
3. **Model Selection**: Choose appropriate models for the analysis type
4. **Interpretation**: Interpret results in domain context
5. **Validation**: Validate text mining results with domain knowledge
6. **Documentation**: Document text mining methods and assumptions
7. **Privacy**: Consider privacy implications of text analysis
8. **Performance**: Optimize text mining for large document collections
