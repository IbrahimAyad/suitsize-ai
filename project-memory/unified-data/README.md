# Unified Suit Sizing Data Engine

## Overview

This directory contains the unified data tables that power the advanced menswear sizing recommendation system. The engine combines legacy knowledge, empirical research, customer data patterns, and machine learning to provide accurate size recommendations with confidence scoring.

## Data Structure

### Core Tables

1. **`unified_suit_sizing_table.csv`** - Master sizing table
   - Consolidated data from regular, short, and long sizing charts
   - Contains all size variations (34R-54R, S/R/L/XL lengths)
   - Includes chest, waist, shoulder, height, weight, and drop measurements
   - Customer success rates and confidence metrics

2. **`body_type_adjustments.json`** - Body type classification and adjustments
   - Athletic, slim, regular, and broad body type definitions
   - Measurement patterns and proportion ratios
   - S/R/L length nudges and fit preferences
   - Alteration priorities for each body type

3. **`drop_patterns_and_edge_cases.json`** - Drop patterns and edge case detection
   - Body type drop distributions (0-10 inch ranges)
   - Size-based drop patterns
   - Edge case detection for height, weight, and proportion extremes
   - Validation rules and handling strategies

### Supporting Data

- **`project-memory/body-types/`** - Detailed body type profiles
- **`project-memory/core-algorithms/`** - Core calculation and scoring algorithms
- **`project-memory/customer-insights/`** - Customer feedback and satisfaction data
- **`project-memory/validation/`** - Test cases and success metrics

## Recommendation Engine Logic Flow

### 1. Input Processing
```
User Input (height, weight, body type) 
→ Estimate chest measurement 
→ Calculate BMI and proportions
→ Identify potential edge cases
```

### 2. Base Size Calculation
```
Height/Weight Matrix Lookup 
→ Find base size (e.g., 40R)
→ Apply body type adjustments
→ Determine S/R/L/XL length
```

### 3. Drop Pattern Analysis
```
Calculate chest-to-waist drop
→ Compare to body type expectations
→ Apply drop-based adjustments
→ Identify proportion extremes
```

### 4. Edge Case Detection
```
Check for height/weight extremes
→ Analyze proportion ratios
→ Detect statistical outliers
→ Apply confidence penalties
```

### 5. Confidence Scoring
```
Multi-factor confidence calculation:
- Data quality (25%)
- Customer similarity (35%)
- Body type match (20%)
- Edge case risk (20%)
```

### 6. Recommendation Output
```
Primary size recommendation
→ Alternative size options
→ Alteration recommendations
→ Confidence level and rationale
```

## Implementation Guidelines

### Data Loading
```python
import pandas as pd
import json

# Load unified sizing table
sizing_table = pd.read_csv('unified_suit_sizing_table.csv')

# Load body type adjustments
with open('body_type_adjustments.json', 'r') as f:
    body_types = json.load(f)

# Load drop patterns and edge cases
with open('drop_patterns_and_edge_cases.json', 'r') as f:
    drop_patterns = json.load(f)
```

### Core Functions

#### 1. Body Type Classification
```python
def classify_body_type(height, weight, chest=None, waist=None):
    """
    Classify body type based on measurements and proportions
    Returns: body_type, confidence_score
    """
    bmi = calculate_bmi(height, weight)
    
    if chest and waist:
        drop = chest - waist
        # Use drop patterns for classification
    else:
        # Use BMI and height/weight ratios
        pass
    
    return body_type, confidence
```

#### 2. Base Size Calculation
```python
def calculate_base_size(height, weight, body_type):
    """
    Calculate base size using unified sizing table
    Returns: base_size, confidence_score
    """
    # Look up in height/weight matrix
    # Apply body type adjustments
    # Return size and confidence
```

#### 3. Length Determination
```python
def determine_length(height, body_type):
    """
    Determine S/R/L/XL based on height and body type
    Returns: length_code, adjustments
    """
    # Use height ranges from sizing table
    # Apply body type nudges
    # Return length and adjustments
```

#### 4. Edge Case Detection
```python
def detect_edge_cases(height, weight, chest, waist, body_type):
    """
    Detect edge cases and apply confidence penalties
    Returns: edge_cases, confidence_penalty
    """
    edge_cases = []
    penalty = 0
    
    # Check height extremes
    # Check weight extremes
    # Check proportion extremes
    # Check BMI extremes
    
    return edge_cases, penalty
```

#### 5. Confidence Scoring
```python
def calculate_confidence(data_quality, customer_similarity, 
                        body_type_match, edge_case_risk):
    """
    Calculate multi-factor confidence score
    Returns: confidence_score, confidence_level
    """
    # Apply weighted factors
    # Apply edge case penalties
    # Determine confidence level
```

## Usage Examples

### Basic Recommendation
```python
# Input: 5'10", 170 lbs, athletic build
recommendation = get_size_recommendation(
    height=70,  # inches
    weight=170,
    body_type="athletic"
)

# Output:
# {
#   "primary_size": "40R",
#   "alternative_size": "42R", 
#   "confidence": 0.87,
#   "confidence_level": "high",
#   "alterations": ["waist_suppression", "sleeve_width"],
#   "rationale": "Athletic build with 8\" drop requires shoulder-based sizing"
# }
```

### Edge Case Handling
```python
# Input: 6'8", 160 lbs, slim build
recommendation = get_size_recommendation(
    height=80,
    weight=160,
    body_type="slim"
)

# Output:
# {
#   "primary_size": "38XL",
#   "alternative_size": "40XL",
#   "confidence": 0.65,
#   "confidence_level": "medium",
#   "edge_cases": ["very_tall", "tall_slim"],
#   "recommendations": ["Professional fitting recommended"]
# }
```

## Data Quality and Validation

### Success Metrics
- **Target Accuracy**: 90% for high confidence recommendations
- **Return Rate Targets**: 
  - High confidence: <5%
  - Medium confidence: <10%
  - Low confidence: <20%

### Continuous Learning
- Customer feedback integration
- Return reason analysis
- Success pattern tracking
- Monthly algorithm adjustments

## Integration with Web UI

The unified data engine can power:
1. **Standalone web application** - Full-featured sizing tool
2. **Embeddable widget** - Lightweight integration
3. **API endpoints** - RESTful service for external applications
4. **Mobile applications** - Native mobile sizing tools

## Future Enhancements

1. **Machine Learning Integration**
   - Customer data pattern recognition
   - Predictive modeling for new body types
   - Automated confidence calibration

2. **Advanced Analytics**
   - Regional sizing patterns
   - Seasonal trend analysis
   - Brand-specific adjustments

3. **Personalization**
   - Individual customer profiles
   - Style preference learning
   - Alteration history tracking

## Maintenance and Updates

- **Monthly**: Customer feedback analysis and algorithm adjustments
- **Quarterly**: Data quality review and validation rule updates
- **Annually**: Comprehensive data refresh and model retraining

---

*This unified data engine represents the culmination of extensive research, customer data analysis, and algorithmic refinement to provide the most accurate and reliable suit sizing recommendations available.* 