"""
Enhanced Suit Sizing Recommendation Engine
==========================================

This module provides a comprehensive suit sizing recommendation system that combines:
- Legacy knowledge and industry standards
- Customer data patterns and success rates
- Body type classification and adjustments
- Edge case detection and handling
- Multi-factor confidence scoring

The engine uses the unified data structure from project-memory/unified-data/
to provide accurate, reliable size recommendations with detailed rationale.
"""

import pandas as pd
import json
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SizeRecommendation:
    """Container for size recommendation results"""
    primary_size: str
    alternative_size: Optional[str]
    confidence: float
    confidence_level: str
    body_type: str
    alterations: List[str]
    rationale: str
    edge_cases: List[str]
    measurements: Dict[str, float]
    fit_preferences: Dict[str, str]

class EnhancedSizingEngine:
    """
    Advanced suit sizing recommendation engine using unified data structure
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize the engine with unified data tables"""
        if data_path is None:
            # Try to find the data path relative to the current file
            current_dir = Path(__file__).parent
            self.data_path = current_dir / "project-memory" / "unified-data"
            if not self.data_path.exists():
                # Try parent directory
                self.data_path = current_dir.parent / "project-memory" / "unified-data"
        else:
            self.data_path = Path(data_path)
        self._load_data()
        
    def _load_data(self):
        """Load all unified data tables"""
        # Load master sizing table
        self.sizing_table = pd.read_csv(self.data_path / "unified_suit_sizing_table.csv")
        
        # Load body type adjustments
        with open(self.data_path / "body_type_adjustments.json", 'r') as f:
            self.body_types = json.load(f)
            
        # Load drop patterns and edge cases
        with open(self.data_path / "drop_patterns_and_edge_cases.json", 'r') as f:
            self.drop_patterns = json.load(f)
            
        # Load core algorithms
        with open(self.data_path.parent / "core-algorithms" / "confidence-scoring.json", 'r') as f:
            self.confidence_config = json.load(f)
            
        with open(self.data_path.parent / "core-algorithms" / "edge-case-detection.json", 'r') as f:
            self.edge_case_config = json.load(f)
    
    def get_size_recommendation(
        self, 
        height: float, 
        weight: float, 
        body_type: str = 'regular',
        chest: Optional[float] = None,
        waist: Optional[float] = None,
        shoulder_width: Optional[float] = None,
        age: Optional[int] = None,
        activity_level: Optional[str] = None
    ) -> SizeRecommendation:
        """
        Get comprehensive size recommendation with confidence scoring
        Now: base recommendation is height/weight only; body type is secondary.
        """
        # Step 1: Input validation and preprocessing
        self._validate_inputs(height, weight, body_type)
        # Step 2: Calculate derived measurements
        measurements = self._calculate_measurements(height, weight, chest, waist, shoulder_width)
        # Step 3: Base size calculation (height/weight only)
        base_size, size_confidence = self._calculate_base_size(height, weight, 'regular', measurements)
        # Step 4: Length determination (height only)
        length_code, length_adjustments = self._determine_length(height, 'regular')
        # Step 5: Edge case detection
        edge_cases, edge_penalty = self._detect_edge_cases(height, weight, measurements, body_type)
        # Step 6: Drop pattern analysis
        drop_analysis = self._analyze_drop_pattern(measurements, body_type)
        # Step 7: Confidence scoring
        confidence, confidence_level = self._calculate_confidence(
            measurements, body_type, edge_cases, size_confidence, drop_analysis
        )
        # Step 8: Body type as secondary adjustment (only if confidence is low)
        adjusted_size = f"{base_size[:-1]}{length_code}"
        tailoring_advice = []
        if confidence < 0.75 and body_type:
            # Only nudge if confidence is low
            adjusted_size = self._apply_body_type_adjustment(base_size, body_type, measurements)
            tailoring_advice.append(f"Body type considered for fine-tuning: {body_type}")
        # Step 9: Generate final recommendation
        recommendation = self._generate_recommendation(
            adjusted_size, length_code, confidence, body_type, 
            measurements, edge_cases, drop_analysis
        )
        # Attach tailoring advice for explainability
        recommendation.rationale += (" " + "; ".join(tailoring_advice)) if tailoring_advice else ""
        return recommendation
    
    def _validate_inputs(self, height: float, weight: float, body_type: str):
        """Validate input parameters"""
        if not (48 <= height <= 84):  # 4'0" to 7'0"
            raise ValueError("Height must be between 48 and 84 inches")
        
        if not (80 <= weight <= 400):  # 80 to 400 lbs
            raise ValueError("Weight must be between 80 and 400 pounds")
            
        if body_type not in ['athletic', 'slim', 'regular', 'broad']:
            raise ValueError("Body type must be one of: athletic, slim, regular, broad")
    
    def _calculate_measurements(self, height: float, weight: float, 
                              chest: Optional[float], waist: Optional[float], 
                              shoulder_width: Optional[float]) -> Dict[str, float]:
        """Calculate or estimate missing measurements"""
        measurements = {
            'height': height,
            'weight': weight,
            'bmi': (weight * 703) / (height * height)
        }
        
        # Estimate chest if not provided
        if chest is None:
            measurements['chest'] = self._estimate_chest(height, weight)
        else:
            measurements['chest'] = chest
            
        # Estimate waist if not provided
        if waist is None:
            measurements['waist'] = self._estimate_waist(measurements['chest'])
        else:
            measurements['waist'] = waist
            
        # Calculate drop
        measurements['drop'] = measurements['chest'] - measurements['waist']
        
        # Estimate shoulder width if not provided
        if shoulder_width is None:
            measurements['shoulder_width'] = self._estimate_shoulder(measurements['chest'])
        else:
            measurements['shoulder_width'] = shoulder_width
            
        return measurements
    
    def _estimate_chest(self, height: float, weight: float) -> float:
        """Estimate chest measurement from height and weight"""
        # Use BMI-based estimation with height adjustment
        bmi = (weight * 703) / (height * height)
        
        if bmi < 18.5:  # Underweight
            base_chest = height * 0.45
        elif bmi < 25:  # Normal
            base_chest = height * 0.48
        elif bmi < 30:  # Overweight
            base_chest = height * 0.52
        else:  # Obese
            base_chest = height * 0.56
            
        return round(base_chest, 1)
    
    def _estimate_waist(self, chest: float) -> float:
        """Estimate waist measurement from chest"""
        # Use typical drop patterns
        return round(chest - 6.0, 1)  # Standard 6" drop
    
    def _estimate_shoulder(self, chest: float) -> float:
        """Estimate shoulder width from chest measurement"""
        # Use typical shoulder-to-chest ratios
        return round(chest * 0.45, 1)
    
    def _get_body_type_info(self, body_type: str, measurements: Dict[str, float]) -> Dict[str, Any]:
        """Get body type information and validate against measurements"""
        if body_type not in self.body_types:
            raise ValueError(f"Unknown body type: {body_type}")
            
        body_info = self.body_types[body_type].copy()
        
        # Validate BMI range
        bmi = measurements['bmi']
        bmi_range = body_info['bmi_range']
        
        if not (bmi_range[0] <= bmi <= bmi_range[1]):
            # Adjust body type if BMI is outside expected range
            body_info['bmi_warning'] = True
            body_info['confidence_adjustment'] = -0.1
        else:
            body_info['bmi_warning'] = False
            body_info['confidence_adjustment'] = 0.0
            
        return body_info
    
    def _calculate_base_size(self, height: float, weight: float, body_type: str, 
                           measurements: Dict[str, float]) -> Tuple[str, float]:
        """Calculate base size optimized for slim fit suits"""
        
        # Find closest match in sizing table
        best_size = "40R"  # Default fallback
        best_score = float('inf')
        
        for _, row in self.sizing_table.iterrows():
            # Calculate distance score based on height, weight, and chest
            height_diff = abs(height - float(row['Height_Avg']))
            weight_diff = abs(weight - float(row['Weight_Avg']))
            chest_diff = abs(measurements['chest'] - float(row['Chest_Avg']))
            
            # For slim fit suits, prioritize chest measurement more heavily
            # and weight slightly less (since slim fit handles weight distribution)
            score = (height_diff * 0.25 + weight_diff * 0.25 + chest_diff * 0.5)
            
            if score < best_score:
                best_score = score
                best_size = str(row['Size'])
        
        # Apply body type adjustments optimized for slim fit suits
        adjusted_size = self._apply_body_type_adjustment(best_size, body_type, measurements)
        
        # Calculate confidence based on how well the size matches
        confidence = max(0.5, 1.0 - (best_score / 50))  # Normalize score to confidence
        
        return adjusted_size, confidence
    
    def _apply_body_type_adjustment(self, base_size: str, body_type: str, 
                                  measurements: Dict[str, float]) -> str:
        """Apply body type-specific size adjustments optimized for slim fit suits"""
        
        # Extract size number and length
        size_num = int(base_size[:-1])
        length = base_size[-1]
        
        # Apply body type adjustments optimized for slim fit suits
        if body_type == 'slim':
            # For slim fit suits, slim builds often need to size down more aggressively
            if measurements['bmi'] < 20:
                size_num = max(34, size_num - 2)
            else:
                size_num = max(34, size_num - 1)
                
        elif body_type == 'athletic':
            # Athletic builds for slim fit - may need to size down slightly for waist
            # but ensure shoulders fit
            if measurements['drop'] > 8:
                # High drop - size down for waist, shoulders will still fit
                size_num = max(34, size_num - 1)
            else:
                # Normal drop - keep size for shoulder fit
                size_num = size_num
                
        elif body_type == 'broad':
            # Broad builds for slim fit - may need to size up for shoulders
            # but slim fit will handle the waist
            if measurements['bmi'] > 30:
                size_num = min(54, size_num + 1)
            else:
                size_num = min(54, size_num + 1)
        
        # Ensure size is even-numbered
        size_num = int(round(size_num / 2) * 2)
        size_num = max(34, min(54, size_num))
        
        return f"{size_num}{length}"
    
    def _determine_length(self, height: float, body_type: str) -> Tuple[str, Dict[str, float]]:
        """Determine S/R/L/XL based on height and body type"""
        
        # Base length determination
        if height < 68:  # Under 5'8"
            base_length = 'S'
        elif height < 72:  # 5'8" to 6'0"
            base_length = 'R'
        elif height < 76:  # 6'0" to 6'4"
            base_length = 'L'
        else:  # Over 6'4"
            base_length = 'XL'
        
        # Apply body type nudges (more conservative for athletic builds)
        body_info = self.body_types[body_type]
        sizing_nudge = body_info['sizing_nudge']
        
        if 'prefer longer' in sizing_nudge.lower():
            # For athletic builds, only nudge to longer if clearly in the range
            if body_type == 'athletic':
                # Only nudge if height is in the upper part of the range
                if base_length == 'S' and height >= 67:  # Near S/R cutoff
                    base_length = 'R'
                elif base_length == 'R' and height >= 71:  # Near R/L cutoff
                    base_length = 'L'
            else:
                # For other body types, apply standard nudging
                if base_length == 'S':
                    base_length = 'R'
                elif base_length == 'R':
                    base_length = 'L'
        elif 'prefer shorter' in sizing_nudge.lower():
            if base_length == 'L':
                base_length = 'R'
            elif base_length == 'R':
                base_length = 'S'
        
        # Get length adjustments
        length_adjustments = {
            'sleeve_adjustment': 0.0,
            'jacket_adjustment': 0.0
        }
        
        if base_length == 'S':
            length_adjustments['sleeve_adjustment'] = -1.5
            length_adjustments['jacket_adjustment'] = -3.0
        elif base_length == 'L':
            length_adjustments['sleeve_adjustment'] = 1.5
            length_adjustments['jacket_adjustment'] = 3.0
        elif base_length == 'XL':
            length_adjustments['sleeve_adjustment'] = 3.0
            length_adjustments['jacket_adjustment'] = 4.5
        
        return base_length, length_adjustments
    
    def _detect_edge_cases(self, height: float, weight: float, measurements: Dict[str, float], 
                          body_type: str) -> Tuple[List[str], float]:
        """Detect edge cases and calculate confidence penalty"""
        
        edge_cases = []
        penalty = 0.0
        
        # Height extremes
        if height < 64:  # Very short
            edge_cases.append('very_short')
            penalty += 0.15
        elif height > 78:  # Very tall
            edge_cases.append('very_tall')
            penalty += 0.20
        
        # Weight extremes
        if weight < 120:  # Very light
            edge_cases.append('very_light')
            penalty += 0.12
        elif weight > 300:  # Very heavy
            edge_cases.append('very_heavy')
            penalty += 0.18
        
        # BMI extremes
        bmi = measurements['bmi']
        if bmi < 16:
            edge_cases.append('underweight')
            penalty += 0.14
        elif bmi > 40:
            edge_cases.append('severely_obese')
            penalty += 0.25
        
        # Proportion extremes
        drop = measurements['drop']
        if drop > 8:
            edge_cases.append('athletic_v_shape')
            penalty += 0.08
        elif drop < 4:
            edge_cases.append('rectangular_build')
            penalty += 0.06
        
        # Shoulder width extremes
        shoulder_chest_ratio = measurements['shoulder_width'] / measurements['chest']
        if shoulder_chest_ratio > 0.5:
            edge_cases.append('inverted_triangle')
            penalty += 0.10
        
        return edge_cases, penalty
    
    def _analyze_drop_pattern(self, measurements: Dict[str, float], body_type: str) -> Dict[str, Any]:
        """Analyze chest-to-waist drop pattern"""
        
        drop = measurements['drop']
        body_type_drops = self.drop_patterns['drop_patterns']['body_type_distributions']
        
        # Find matching body type
        body_type_key = None
        if body_type == 'slim':
            body_type_key = 'ectomorph_slim'
        elif body_type == 'athletic':
            body_type_key = 'athletic_build'
        elif body_type == 'broad':
            body_type_key = 'endomorph_heavy'
        else:
            body_type_key = 'mesomorph_athletic'
        
        expected_drop_range = body_type_drops[body_type_key]['typical_drop_range']
        sizing_implications = body_type_drops[body_type_key]['sizing_implications']
        
        # Determine drop category
        if drop >= 8:
            drop_category = 'high_drop_8_plus'
        elif 6 <= drop < 8:
            drop_category = 'medium_drop_6_7'
        elif 4 <= drop < 6:
            drop_category = 'low_drop_4_5'
        else:
            drop_category = 'minimal_drop_0_3'
        
        drop_rules = self.drop_patterns['drop_patterns']['drop_adjustment_rules'][drop_category]
        
        return {
            'drop': drop,
            'expected_range': expected_drop_range,
            'category': drop_category,
            'sizing_strategy': drop_rules['sizing_strategy'],
            'alteration_priority': drop_rules['alteration_priority'],
            'confidence_impact': drop_rules['confidence_impact'],
            'sizing_implications': sizing_implications
        }
    
    def _calculate_confidence(self, measurements: Dict[str, float], body_type: str, 
                            edge_cases: List[str], size_confidence: float, 
                            drop_analysis: Dict[str, Any]) -> Tuple[float, str]:
        """Calculate multi-factor confidence score"""
        
        # Base confidence from size calculation
        confidence = size_confidence
        
        # Apply drop pattern confidence impact
        confidence += drop_analysis['confidence_impact']
        
        # Apply edge case penalties
        edge_penalty = sum([
            self.drop_patterns['edge_cases'].get(case, {}).get('confidence_impact', 0)
            for case in edge_cases
        ])
        confidence -= edge_penalty
        
        # Apply body type confidence adjustment
        body_info = self.body_types[body_type]
        confidence += body_info.get('confidence_adjustment', 0)
        
        # Clamp confidence to valid range
        confidence = max(0.0, min(1.0, confidence))
        
        # Determine confidence level
        if confidence >= 0.85:
            level = 'high'
        elif confidence >= 0.75:
            level = 'medium_high'
        elif confidence >= 0.65:
            level = 'medium'
        elif confidence >= 0.55:
            level = 'low_medium'
        else:
            level = 'low'
        
        return confidence, level
    
    def _generate_recommendation(self, base_size: str, length_code: str, confidence: float,
                               body_type: str, measurements: Dict[str, float], 
                               edge_cases: List[str], drop_analysis: Dict[str, Any]) -> SizeRecommendation:
        """Generate final size recommendation with all details"""
        
        # Construct full size and ensure it's even-numbered (US standard)
        size_num = int(base_size[:-1])
        
        # Always round to nearest even size for retail compatibility
        size_num = int(round(size_num / 2) * 2)
        
        # Ensure size is within valid range (34-54)
        size_num = max(34, min(54, size_num))
        
        full_size = f"{size_num}{length_code}"
        
        # Determine alternative size (also ensure it's even-numbered)
        alternative_size = None
        if confidence < 0.8:
            if length_code == 'R':
                alt_size_num = size_num
                alternative_size = f"{alt_size_num}S"
            else:
                alt_size_num = size_num
                alternative_size = f"{alt_size_num}R"
        
        # Get alterations based on body type and drop analysis
        alterations = self._get_alterations(body_type, drop_analysis, edge_cases)
        
        # Generate rationale
        rationale = self._generate_rationale(body_type, measurements, drop_analysis, edge_cases)
        
        # Get fit preferences
        fit_preferences = self.body_types[body_type]['fit_preferences']
        
        return SizeRecommendation(
            primary_size=full_size,
            alternative_size=alternative_size,
            confidence=confidence,
            confidence_level=self._get_confidence_level(confidence),
            body_type=body_type,
            alterations=alterations,
            rationale=rationale,
            edge_cases=edge_cases,
            measurements=measurements,
            fit_preferences=fit_preferences
        )
    
    def _get_alterations(self, body_type: str, drop_analysis: Dict[str, Any], 
                        edge_cases: List[str]) -> List[str]:
        """Get recommended alterations based on body type and analysis"""
        
        alterations = []
        
        # Add body type specific alterations
        body_info = self.body_types[body_type]
        alterations.extend(body_info['alteration_priority'][:2])  # Top 2 priorities
        
        # Add drop-based alterations
        alterations.extend(drop_analysis['alteration_priority'][:2])
        
        # Add edge case specific alterations
        for edge_case in edge_cases:
            if edge_case in self.drop_patterns['edge_cases']:
                edge_info = self.drop_patterns['edge_cases'][edge_case]
                if 'recommendations' in edge_info:
                    alterations.extend(edge_info['recommendations'])
        
        # Remove duplicates and limit to top 3
        unique_alterations = list(dict.fromkeys(alterations))
        return unique_alterations[:3]
    
    def _generate_rationale(self, body_type: str, measurements: Dict[str, float],
                          drop_analysis: Dict[str, Any], edge_cases: List[str]) -> str:
        """Generate human-readable rationale for the recommendation"""
        
        rationale_parts = []
        
        # Body type explanation
        body_info = self.body_types[body_type]
        rationale_parts.append(f"Your {body_type} build")
        
        # Drop pattern explanation
        drop = measurements['drop']
        if drop > 8:
            rationale_parts.append(f"with a {drop}\" chest-to-waist drop")
        elif drop < 4:
            rationale_parts.append(f"with minimal waist definition ({drop}\" drop)")
        
        # Sizing strategy
        rationale_parts.append(f"requires {drop_analysis['sizing_strategy']}")
        
        # Edge case explanations
        if edge_cases:
            edge_explanations = []
            for case in edge_cases:
                if case == 'very_tall':
                    edge_explanations.append("extra length considerations")
                elif case == 'very_short':
                    edge_explanations.append("proportion adjustments")
                elif case == 'athletic_v_shape':
                    edge_explanations.append("significant waist tailoring")
            
            if edge_explanations:
                rationale_parts.append(f"and {', '.join(edge_explanations)}")
        
        rationale_parts.append("for optimal slim fit suit sizing.")
        
        return " ".join(rationale_parts)
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to human-readable level"""
        if confidence >= 0.85:
            return "high"
        elif confidence >= 0.75:
            return "medium-high"
        elif confidence >= 0.65:
            return "medium"
        elif confidence >= 0.55:
            return "low-medium"
        else:
            return "low"
    
    def get_customer_message(self, recommendation: SizeRecommendation) -> str:
        """Generate customer-friendly message based on confidence level"""
        
        confidence_config = self.confidence_config['confidence_levels']
        level = recommendation.confidence_level
        
        if level in confidence_config:
            base_message = confidence_config[level]['customer_message']
        else:
            base_message = "We recommend this size based on your measurements."
        
        # Add edge case specific messages
        if recommendation.edge_cases:
            edge_messages = []
            for case in recommendation.edge_cases:
                if case in self.drop_patterns['edge_cases']:
                    edge_info = self.drop_patterns['edge_cases'][case]
                    if 'recommendations' in edge_info:
                        edge_messages.extend(edge_info['recommendations'])
            
            if edge_messages:
                base_message += f" {edge_messages[0]}"
        
        return base_message


# Convenience function for easy usage
def get_size_recommendation(height: float, weight: float, body_type: str, **kwargs) -> SizeRecommendation:
    """
    Convenience function to get size recommendation
    
    Args:
        height: Height in inches
        weight: Weight in pounds  
        body_type: One of 'athletic', 'slim', 'regular', 'broad'
        **kwargs: Additional measurements (chest, waist, shoulder_width, etc.)
    
    Returns:
        SizeRecommendation object
    """
    engine = EnhancedSizingEngine()
    return engine.get_size_recommendation(height, weight, body_type, **kwargs)


if __name__ == "__main__":
    # Example usage and testing
    engine = EnhancedSizingEngine()
    
    # Test case 1: Standard athletic build
    print("=== Test Case 1: Athletic Build ===")
    rec1 = engine.get_size_recommendation(
        height=70,  # 5'10"
        weight=170,
        body_type="athletic"
    )
    print(f"Primary Size: {rec1.primary_size}")
    print(f"Confidence: {rec1.confidence:.2f} ({rec1.confidence_level})")
    print(f"Rationale: {rec1.rationale}")
    print(f"Alterations: {', '.join(rec1.alterations)}")
    print()
    
    # Test case 2: Edge case - very tall and slim
    print("=== Test Case 2: Very Tall & Slim ===")
    rec2 = engine.get_size_recommendation(
        height=78,  # 6'6"
        weight=160,
        body_type="slim"
    )
    print(f"Primary Size: {rec2.primary_size}")
    print(f"Confidence: {rec2.confidence:.2f} ({rec2.confidence_level})")
    print(f"Edge Cases: {', '.join(rec2.edge_cases)}")
    print(f"Rationale: {rec2.rationale}")
    print()
    
    # Test case 3: Broad build with measurements
    print("=== Test Case 3: Broad Build with Measurements ===")
    rec3 = engine.get_size_recommendation(
        height=72,  # 6'0"
        weight=220,
        body_type="broad",
        chest=46,
        waist=42
    )
    print(f"Primary Size: {rec3.primary_size}")
    print(f"Confidence: {rec3.confidence:.2f} ({rec3.confidence_level})")
    print(f"Measurements: Chest {rec3.measurements['chest']}\", Waist {rec3.measurements['waist']}\", Drop {rec3.measurements['drop']}\"")
    print(f"Rationale: {rec3.rationale}") 