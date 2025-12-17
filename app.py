"""
Simple, reliable backend API for the suit sizing application
"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import math

app = Flask(__name__, template_folder='templates')

def calculate_bmi(height_inches, weight_lbs):
    """Calculate BMI"""
    return (weight_lbs * 703) / (height_inches * height_inches)

def get_body_type_adjustment(bmi, fit_preference):
    """Get size adjustment based on BMI and fit preference"""
    if bmi < 20:
        return -1  # Slim
    elif bmi > 25:
        return +1  # Broad
    else:
        return 0   # Regular

def calculate_jacket_size(height_inches, weight_lbs, fit_preference):
    """Calculate jacket size based on measurements"""
    # Base calculation: height-based sizing
    base_size = 38 + (height_inches - 66) * 0.5
    
    # Weight adjustment
    weight_adjustment = (weight_lbs - 160) * 0.03
    
    # Fit preference adjustment
    fit_adjustments = {
        'slim': -0.5,
        'regular': 0,
        'relaxed': +0.5
    }
    fit_adjustment = fit_adjustments.get(fit_preference, 0)
    
    # Calculate final size
    final_size = base_size + weight_adjustment + fit_adjustment
    
    # Round to nearest 2 (jacket sizing standard)
    final_size = round(final_size / 2) * 2
    
    return max(34, min(60, final_size))

def calculate_confidence(height_inches, weight_lbs):
    """Calculate confidence score based on data quality"""
    confidence = 0.8  # Base confidence
    
    # Height in reasonable range
    if 65 <= height_inches <= 77:
        confidence += 0.1
    
    # Weight in reasonable range
    if 120 <= weight_lbs <= 250:
        confidence += 0.1
    
    return min(0.95, confidence)

@app.route('/')
def index():
    """Main page with size recommendation form"""
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Get size recommendations"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'height' not in data or 'weight' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: height and weight'
            }), 400
        
        height_inches = float(data['height'])
        weight_lbs = float(data['weight'])
        fit_preference = data.get('fit_preference', 'regular')
        body_type = data.get('body_type', 'regular')
        
        # Get fit preference from radio buttons
        if not fit_preference or fit_preference == 'regular':
            fit_preference = 'regular'
        
        # Calculate recommendations
        jacket_size = calculate_jacket_size(height_inches, weight_lbs, fit_preference)
        confidence = calculate_confidence(height_inches, weight_lbs)
        
        # Format response
        result = {
            'success': True,
            'recommendation': {
                'primary_size': f'{jacket_size}R',
                'alternative_size': f'{jacket_size + 2}R' if jacket_size < 60 else None,
                'confidence': confidence,
                'confidence_level': 'high' if confidence > 0.8 else 'medium',
                'body_type': body_type,
                'fit_preferences': {
                    'jacket_fit': fit_preference,
                    'waist_fit': 'standard'
                },
                'alterations': [
                    'Waist suppression recommended for slim fit',
                    'Trouser hemming recommended'
                ],
                'rationale': f'Based on your height ({height_inches}" / {int(height_inches//12)}\'{height_inches%12:.0f}") and weight ({weight_lbs} lbs), we recommend a {jacket_size}R jacket with {fit_preference} fit.',
                'edge_cases': [],
                'measurements': {
                    'chest': jacket_size,
                    'waist': jacket_size - 6,
                    'drop': 6,
                    'bmi': round(calculate_bmi(height_inches, weight_lbs), 1),
                    'shoulder_width': round(jacket_size * 0.5, 1)
                }
            },
            'message': f'We recommend size {jacket_size}R based on your measurements.',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)