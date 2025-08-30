# Data Cleaning Tool

## Overview
The Data Cleaning tool provides comprehensive data cleaning and preprocessing capabilities for identifying, handling, and resolving data quality issues across various data formats and sources.

## Purpose
To automate and streamline data cleaning processes, ensuring data quality and consistency for downstream analysis and machine learning applications.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing
- **scikit-learn** (>=1.3.0) - Machine learning utilities for preprocessing
- **missingno** (>=0.5.0) - Missing data visualization
- **pyjanitor** (>=0.24.0) - Data cleaning utilities

### Optional Libraries
- **openpyxl** (>=3.1.0) - Excel file support
- **xlrd** (>=2.0.0) - Legacy Excel file support
- **sqlalchemy** (>=2.0.0) - Database connectivity
- **psycopg2-binary** (>=2.9.0) - PostgreSQL support
- **pymongo** (>=4.4.0) - MongoDB support
- **redis** (>=4.6.0) - Redis caching
- **great-expectations** (>=0.17.0) - Data validation
- **dask** (>=2023.8.0) - Parallel computing for large datasets

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "data_source": {
      "type": "string",
      "description": "Path to data file or database connection string"
    },
    "data_format": {
      "type": "string",
      "enum": ["csv", "json", "excel", "parquet", "sql", "mongodb"],
      "description": "Format of the input data"
    },
    "cleaning_options": {
      "type": "object",
      "properties": {
        "handle_missing": {
          "type": "string",
          "enum": ["drop", "fill_mean", "fill_median", "fill_mode", "interpolate"],
          "description": "Strategy for handling missing values"
        },
        "remove_duplicates": {
          "type": "boolean",
          "description": "Whether to remove duplicate rows"
        },
        "handle_outliers": {
          "type": "string",
          "enum": ["iqr", "zscore", "isolation_forest", "none"],
          "description": "Method for outlier detection and handling"
        },
        "normalize_columns": {
          "type": "array",
          "items": {"type": "string"},
          "description": "List of columns to normalize"
        },
        "encode_categorical": {
          "type": "boolean",
          "description": "Whether to encode categorical variables"
        },
        "text_cleaning": {
          "type": "object",
          "properties": {
            "remove_special_chars": {"type": "boolean"},
            "lowercase": {"type": "boolean"},
            "remove_stopwords": {"type": "boolean"},
            "lemmatize": {"type": "boolean"}
          }
        }
      }
    },
    "output_format": {
      "type": "string",
      "enum": ["csv", "json", "excel", "parquet"],
      "description": "Format for cleaned data output"
    }
  },
  "required": ["data_source", "data_format"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "cleaned_data_path": {
      "type": "string",
      "description": "Path to the cleaned data file"
    },
    "cleaning_report": {
      "type": "object",
      "properties": {
        "original_rows": {"type": "integer"},
        "cleaned_rows": {"type": "integer"},
        "missing_values_handled": {"type": "integer"},
        "duplicates_removed": {"type": "integer"},
        "outliers_handled": {"type": "integer"},
        "columns_processed": {"type": "array", "items": {"type": "string"}},
        "data_quality_metrics": {
          "type": "object",
          "properties": {
            "completeness": {"type": "number"},
            "consistency": {"type": "number"},
            "accuracy": {"type": "number"}
          }
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for cleaning process in seconds"
    }
  }
}
```

## Intended Use
- **Data Quality Assessment**: Identify and quantify data quality issues
- **Missing Value Handling**: Apply appropriate strategies for missing data
- **Duplicate Removal**: Identify and remove duplicate records
- **Outlier Detection**: Detect and handle outliers using statistical methods
- **Data Normalization**: Standardize numerical data for analysis
- **Categorical Encoding**: Convert categorical variables to numerical format
- **Text Cleaning**: Clean and preprocess text data
- **Data Validation**: Ensure data meets quality standards

## Limitations
- Large datasets may require significant processing time
- Some cleaning operations may require domain-specific knowledge
- Automatic outlier detection may not be suitable for all use cases
- Text cleaning quality depends on the specific language and domain

## Safety
- Always backup original data before cleaning
- Validate cleaning results against business rules
- Consider the impact of cleaning decisions on downstream analysis
- Document all cleaning steps for reproducibility

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy scikit-learn missingno pyjanitor
   ```

2. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   from sklearn.preprocessing import StandardScaler
   import missingno as msno
   import janitor
   ```

3. **Configure Data Sources**:
   - Set up database connections if using SQL/MongoDB
   - Ensure file paths are accessible
   - Verify data format compatibility

### Usage

#### Basic Data Cleaning
```python
# Load data
data = pd.read_csv("raw_data.csv")

# Basic cleaning
cleaned_data = data.clean_names()  # Clean column names
cleaned_data = cleaned_data.remove_empty()  # Remove empty rows
cleaned_data = cleaned_data.dropna()  # Remove rows with missing values
```

#### Advanced Cleaning with Options
```python
# Configure cleaning options
cleaning_config = {
    "handle_missing": "fill_mean",
    "remove_duplicates": True,
    "handle_outliers": "iqr",
    "normalize_columns": ["numeric_col1", "numeric_col2"],
    "encode_categorical": True
}

# Apply cleaning
cleaned_data = clean_dataset(data, cleaning_config)
```

### Error Handling

#### Common Issues
1. **Memory Errors**: Use chunking for large datasets
2. **Encoding Issues**: Specify encoding when reading files
3. **Data Type Conflicts**: Validate data types before processing
4. **Missing Dependencies**: Install required libraries

#### Troubleshooting
```python
# Handle encoding issues
data = pd.read_csv("file.csv", encoding='utf-8')

# Handle memory issues
for chunk in pd.read_csv("large_file.csv", chunksize=10000):
    process_chunk(chunk)

# Validate data types
print(data.dtypes)
data = data.astype({'column': 'int64'})
```

### Monitoring
- Monitor processing time for large datasets
- Track data quality metrics before and after cleaning
- Log cleaning operations for audit purposes
- Validate output data against expected schema

### Best Practices
1. **Data Profiling**: Always profile data before cleaning
2. **Incremental Cleaning**: Apply cleaning steps incrementally
3. **Validation**: Validate results at each step
4. **Documentation**: Document all cleaning decisions and rationale
5. **Testing**: Test cleaning procedures on sample data first
6. **Backup**: Always maintain original data backups
