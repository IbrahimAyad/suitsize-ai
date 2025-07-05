from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from datetime import datetime
import logging

app = Flask(__name__, template_folder='templates')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Update the path for the training data and sizing table to be relative to the app.py location
TRAINING_DATA_PATH = "enhanced_customers_menswear.csv"
SIZING_TABLE_PATH = "project-memory/unified-data/unified_suit_sizing_table.csv"

class SizeRecommendationAI:
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.size_encoders = {}
        self.size_categories = ['jacket', 'vest', 'shirt', 'shoe', 'pants']
        self.load_training_data()
        self.train_models()
    
    def load_training_data(self):
        """Load and prepare training data from enhanced customer database"""
        try:
            # Load the enhanced customer database
            df = pd.read_csv(TRAINING_DATA_PATH)
            
            # Filter customers with size data
            size_columns = ['jacket_size', 'vest_size', 'shirt_size', 'shoe_size', 'pants_size']
            self.training_data = df[df[size_columns].notna().any(axis=1)].copy()
            
            logger.info(f"Loaded {len(self.training_data)} customers with size data for training")
            
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            self.training_data = pd.DataFrame()
    
    def prepare_features(self, df):
        """Prepare features for the AI model"""
        features = []
        
        # Basic customer features
        if 'total_spent' in df.columns:
            features.append('total_spent')
        if 'total_orders' in df.columns:
            features.append('total_orders')
        if 'engagement_score' in df.columns:
            features.append('engagement_score')
        if 'customer_tier' in df.columns:
            features.append('customer_tier')
        
        # Create age feature if we have birth dates (placeholder for now)
        # In real implementation, you'd extract age from birth dates
        
        return features
    
    def train_models(self):
        """Train AI models for each size category"""
        if self.training_data.empty:
            logger.warning("No training data available")
            return
        
        features = self.prepare_features(self.training_data)
        
        for category in self.size_categories:
            size_col = f'{category}_size'
            confidence_col = f'{category}_size_confidence'
            
            if size_col in self.training_data.columns:
                # Filter out empty sizes
                valid_data = self.training_data[
                    (self.training_data[size_col].notna()) & 
                    (self.training_data[size_col] != '') &
                    (self.training_data[confidence_col] > 0.5)  # Only high confidence sizes
                ].copy()
                
                if len(valid_data) > 10:  # Need minimum data to train
                    try:
                        # Prepare features
                        X = valid_data[features].fillna(0)
                        
                        # Encode categorical features
                        for col in X.select_dtypes(include=['object']).columns:
                            if col not in self.label_encoders:
                                self.label_encoders[col] = LabelEncoder()
                            X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
                        
                        # Prepare target (size) - encode string sizes
                        y = valid_data[size_col]
                        
                        # Encode size strings to numbers for ML model
                        if y.dtype == 'object':
                            size_encoder = LabelEncoder()
                            y_encoded = size_encoder.fit_transform(y)
                            self.size_encoders[category] = size_encoder
                        else:
                            y_encoded = y
                        
                        # Train model
                        model = RandomForestRegressor(n_estimators=100, random_state=42)
                        model.fit(X, y_encoded)
                        
                        self.models[category] = model
                        logger.info(f"Trained model for {category} with {len(valid_data)} samples")
                        
                    except Exception as e:
                        logger.error(f"Error training model for {category}: {e}")
    
    def predict_sizes(self, customer_data):
        """Predict sizes for a customer based on their data"""
        predictions = {}
        confidence_scores = {}
        
        if not self.models:
            logger.warning("No trained models available")
            return predictions, confidence_scores
        
        # Prepare input features
        features = self.prepare_features(pd.DataFrame([customer_data]))
        input_data = pd.DataFrame([customer_data])[features].fillna(0)
        
        # Encode categorical features
        for col in input_data.select_dtypes(include=['object']).columns:
            if col in self.label_encoders:
                input_data[col] = self.label_encoders[col].transform(input_data[col].astype(str))
        
        for category in self.size_categories:
            if category in self.models:
                try:
                    # Make prediction
                    prediction_encoded = self.models[category].predict(input_data)[0]
                    
                    # Decode prediction back to size string
                    if category in self.size_encoders:
                        prediction = self.size_encoders[category].inverse_transform([prediction_encoded])[0]
                    else:
                        prediction = prediction_encoded
                    
                    predictions[category] = prediction
                    
                    # Calculate confidence (simplified - in real implementation, you'd use model confidence)
                    confidence_scores[category] = 0.8  # Placeholder confidence
                    
                except Exception as e:
                    logger.error(f"Error predicting {category} size: {e}")
        
        return predictions, confidence_scores
    
    def get_size_recommendations(self, user_input):
        """Get size recommendations based on user input"""
        # Convert user input to customer data format
        customer_data = {
            'total_spent': user_input.get('budget', 200),
            'total_orders': user_input.get('experience_level', 1),
            'engagement_score': 50,  # Default engagement
            'customer_tier': 'Silver'  # Default tier
        }
        
        # Get predictions
        predictions, confidence_scores = self.predict_sizes(customer_data)
        
        # Format recommendations
        recommendations = {}
        for category in self.size_categories:
            if category in predictions:
                recommendations[category] = {
                    'predicted_size': predictions[category],
                    'confidence': confidence_scores[category],
                    'recommendation': self._format_recommendation(category, predictions[category], confidence_scores[category])
                }
        
        return recommendations
    
    def _format_recommendation(self, category, size, confidence):
        """Format size recommendation with helpful text"""
        confidence_text = "high" if confidence > 0.7 else "medium" if confidence > 0.5 else "low"
        
        recommendations = {
            'jacket': f"Based on our analysis, we recommend a {size} jacket. This is a {confidence_text} confidence recommendation.",
            'vest': f"For vests, we suggest size {size}. This recommendation has {confidence_text} confidence.",
            'shirt': f"Our AI recommends a {size} shirt. This is a {confidence_text} confidence prediction.",
            'shoe': f"For shoes, we recommend size {size}. This has {confidence_text} confidence.",
            'pants': f"We suggest {size} pants. This recommendation has {confidence_text} confidence."
        }
        
        return recommendations.get(category, f"Recommended size: {size}")

# Initialize the AI
ai_model = SizeRecommendationAI()

# Import the enhanced sizing engine
from enhanced_processor import EnhancedSizingEngine

# Initialize the enhanced engine
enhanced_engine = EnhancedSizingEngine()

@app.route('/')
def index():
    """Main page with size recommendation form"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index template: {e}")
        return f"Error loading template: {e}", 500

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """Get size recommendations from AI"""
    try:
        user_data = request.get_json()
        
        # Validate input
        required_fields = ['height', 'weight', 'age', 'experience_level']
        for field in required_fields:
            if field not in user_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get recommendations
        recommendations = ai_model.get_size_recommendations(user_data)
        
        # Add general advice
        advice = {
            'general_tips': [
                "These recommendations are based on our customer data analysis",
                "For best results, we recommend a professional fitting",
                "Sizes may vary between brands and styles",
                "Consider your body type and fit preferences"
            ],
            'next_steps': [
                "Book a fitting appointment for personalized service",
                "Browse our collection with your recommended sizes",
                "Contact us for any questions about sizing"
            ]
        }
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'advice': advice,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/about')
def about():
    """About page explaining how the AI works"""
    return render_template('about.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_trained': len(ai_model.models),
        'training_data_size': len(ai_model.training_data)
    })

@app.route('/api/recommend', methods=['POST'])
def get_enhanced_recommendations():
    """Get enhanced size recommendations using the new engine"""
    try:
        user_data = request.get_json()
        
        # Validate required fields
        required_fields = ['height', 'weight', 'body_type']
        for field in required_fields:
            if field not in user_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate body type
        valid_body_types = ['slim', 'athletic', 'regular', 'broad']
        if user_data['body_type'] not in valid_body_types:
            return jsonify({'error': f'Invalid body type. Must be one of: {", ".join(valid_body_types)}'}), 400
        
        # Get enhanced recommendation
        recommendation = enhanced_engine.get_size_recommendation(
            height=user_data['height'],
            weight=user_data['weight'],
            body_type=user_data['body_type'],
            chest=user_data.get('chest'),
            waist=user_data.get('waist'),
            shoulder_width=user_data.get('shoulder_width')
        )
        
        # Convert to JSON-serializable format
        result = {
            'success': True,
            'recommendation': {
                'primary_size': recommendation.primary_size,
                'alternative_size': recommendation.alternative_size,
                'confidence': recommendation.confidence,
                'confidence_level': recommendation.confidence_level,
                'body_type': recommendation.body_type,
                'alterations': recommendation.alterations,
                'rationale': recommendation.rationale,
                'edge_cases': recommendation.edge_cases,
                'measurements': recommendation.measurements,
                'fit_preferences': recommendation.fit_preferences
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting enhanced recommendations: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 