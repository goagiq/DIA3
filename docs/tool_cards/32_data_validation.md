# Data Validation Tool

## Overview
The Data Validation tool provides comprehensive data validation and quality assessment capabilities for ensuring data integrity, consistency, and compliance with defined schemas and business rules.

## Purpose
To automate data validation processes, identify data quality issues, and ensure data meets specified standards and requirements before processing or analysis.

## Required Libraries

### Core Libraries
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing
- **great-expectations** (>=0.17.0) - Data validation framework
- **cerberus** (>=1.3.0) - Data validation library
- **marshmallow** (>=3.20.0) - Object serialization and validation

### Optional Libraries
- **pydantic** (>=2.0.0) - Data validation using Python type annotations
- **jsonschema** (>=4.17.0) - JSON schema validation
- **voluptuous** (>=0.13.0) - Data validation library
- **schema** (>=0.7.0) - Schema validation library
- **datatest** (>=0.15.0) - Data testing framework
- **pytest** (>=7.4.0) - Testing framework
- **hypothesis** (>=6.75.0) - Property-based testing
- **faker** (>=19.0.0) - Fake data generation for testing

## Input Schema
```json
{
  "type": "object",
  "properties": {
    "data_source": {
      "type": "string",
      "description": "Path to data file or database connection string"
    },
    "validation_config": {
      "type": "object",
      "properties": {
        "schema_validation": {
          "type": "object",
          "properties": {
            "required_columns": {
              "type": "array",
              "items": {"type": "string"}
            },
            "column_types": {
              "type": "object",
              "additionalProperties": {
                "type": "string",
                "enum": ["int", "float", "string", "datetime", "boolean"]
              }
            },
            "column_constraints": {
              "type": "object",
              "additionalProperties": {
                "type": "object",
                "properties": {
                  "min_value": {"type": "number"},
                  "max_value": {"type": "number"},
                  "min_length": {"type": "integer"},
                  "max_length": {"type": "integer"},
                  "pattern": {"type": "string"},
                  "allowed_values": {
                    "type": "array",
                    "items": {"type": "string"}
                  }
                }
              }
            }
          }
        },
        "business_rules": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "rule_name": {"type": "string"},
              "rule_description": {"type": "string"},
              "rule_expression": {"type": "string"},
              "severity": {
                "type": "string",
                "enum": ["error", "warning", "info"]
              }
            }
          }
        },
        "data_quality_checks": {
          "type": "object",
          "properties": {
            "completeness_threshold": {"type": "number"},
            "consistency_threshold": {"type": "number"},
            "accuracy_threshold": {"type": "number"},
            "uniqueness_threshold": {"type": "number"},
            "validity_threshold": {"type": "number"}
          }
        },
        "cross_field_validation": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "fields": {
                "type": "array",
                "items": {"type": "string"}
              },
              "validation_logic": {"type": "string"},
              "error_message": {"type": "string"}
            }
          }
        }
      }
    },
    "output_format": {
      "type": "string",
      "enum": ["json", "html", "csv"],
      "description": "Format for validation report output"
    }
  },
  "required": ["data_source", "validation_config"]
}
```

## Output Schema
```json
{
  "type": "object",
  "properties": {
    "validation_report_path": {
      "type": "string",
      "description": "Path to the validation report file"
    },
    "validation_summary": {
      "type": "object",
      "properties": {
        "total_records": {"type": "integer"},
        "valid_records": {"type": "integer"},
        "invalid_records": {"type": "integer"},
        "validation_score": {"type": "number"},
        "overall_status": {
          "type": "string",
          "enum": ["passed", "failed", "warning"]
        }
      }
    },
    "validation_details": {
      "type": "object",
      "properties": {
        "schema_violations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "column": {"type": "string"},
              "violation_type": {"type": "string"},
              "violation_count": {"type": "integer"},
              "severity": {"type": "string"}
            }
          }
        },
        "business_rule_violations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "rule_name": {"type": "string"},
              "violation_count": {"type": "integer"},
              "affected_records": {"type": "array", "items": {"type": "integer"}},
              "severity": {"type": "string"}
            }
          }
        },
        "data_quality_metrics": {
          "type": "object",
          "properties": {
            "completeness": {"type": "number"},
            "consistency": {"type": "number"},
            "accuracy": {"type": "number"},
            "uniqueness": {"type": "number"},
            "validity": {"type": "number"}
          }
        }
      }
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "issue": {"type": "string"},
          "recommendation": {"type": "string"},
          "priority": {"type": "string"}
        }
      }
    },
    "processing_time": {
      "type": "number",
      "description": "Time taken for validation process in seconds"
    }
  }
}
```

## Intended Use
- **Schema Validation**: Ensure data conforms to expected structure and types
- **Business Rule Validation**: Validate data against domain-specific business rules
- **Data Quality Assessment**: Measure and report on data quality metrics
- **Cross-field Validation**: Validate relationships between different fields
- **Compliance Checking**: Ensure data meets regulatory and compliance requirements
- **Data Profiling**: Generate comprehensive data profiles and statistics
- **Anomaly Detection**: Identify unusual patterns or outliers in data
- **Data Lineage Tracking**: Track data transformations and validation history

## Limitations
- Complex business rules may require custom validation logic
- Some validation checks may be computationally expensive for large datasets
- Validation rules need to be maintained and updated as business requirements change
- Automated validation may not catch all domain-specific issues

## Safety
- Always backup data before running validation
- Use appropriate severity levels for different validation rules
- Consider the impact of validation failures on downstream processes
- Document all validation rules and their business justification

## Runbook

### Setup
1. **Install Dependencies**:
   ```bash
   pip install pandas numpy great-expectations cerberus marshmallow
   ```

2. **Verify Installation**:
   ```python
   import pandas as pd
   import numpy as np
   import great_expectations as ge
   from cerberus import Validator
   from marshmallow import Schema, fields
   ```

3. **Configure Validation Rules**:
   - Define data schemas and constraints
   - Set up business rule validations
   - Configure quality thresholds

### Usage

#### Basic Schema Validation
```python
# Using Great Expectations
import great_expectations as ge

# Load data
df = ge.read_csv("data.csv")

# Basic expectations
df.expect_column_to_exist("id")
df.expect_column_values_to_be_between("age", 0, 120)
df.expect_column_values_to_not_be_null("email")
```

#### Business Rule Validation
```python
# Using Cerberus
from cerberus import Validator

schema = {
    'amount': {'type': 'number', 'min': 0},
    'email': {'type': 'string', 'regex': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'},
    'status': {'type': 'string', 'allowed': ['active', 'inactive', 'pending']}
}

validator = Validator(schema)
validation_result = validator.validate(data)
```

#### Data Quality Assessment
```python
# Calculate quality metrics
def assess_data_quality(df):
    quality_metrics = {
        'completeness': 1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1]),
        'uniqueness': df.nunique().sum() / (df.shape[0] * df.shape[1]),
        'consistency': calculate_consistency_score(df)
    }
    return quality_metrics
```

### Error Handling

#### Common Issues
1. **Schema Mismatches**: Handle unexpected data types or missing columns
2. **Performance Issues**: Optimize validation for large datasets
3. **Rule Conflicts**: Resolve conflicting validation rules
4. **Data Format Issues**: Handle various data formats and encodings

#### Troubleshooting
```python
# Handle schema mismatches
try:
    validation_result = validate_data(data, schema)
except SchemaError as e:
    print(f"Schema validation failed: {e}")
    # Handle gracefully

# Performance optimization
def validate_in_chunks(data, chunk_size=10000):
    for chunk in data.groupby(data.index // chunk_size):
        validate_chunk(chunk)
```

### Monitoring
- Monitor validation success rates
- Track data quality metrics over time
- Alert on validation failures
- Log validation activities for audit

### Best Practices
1. **Incremental Validation**: Validate data as it's ingested
2. **Clear Error Messages**: Provide actionable error messages
3. **Performance Optimization**: Use efficient validation algorithms
4. **Documentation**: Document all validation rules and their purpose
5. **Testing**: Test validation rules with sample data
6. **Monitoring**: Continuously monitor validation performance
