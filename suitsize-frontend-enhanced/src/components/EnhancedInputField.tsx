/**
 * Enhanced InputField Component
 * Based on academic research on measurement accuracy and user experience
 * Implements validation patterns and accessibility standards
 */

import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle2, Info, TrendingUp } from 'lucide-react';

export interface InputValidation {
  isValid: boolean;
  message?: string;
  suggestion?: string;
  severity?: 'error' | 'warning' | 'info';
}

interface EnhancedInputFieldProps {
  label: string;
  value: number;
  onChange: (val: number) => void;
  unit: string;
  min: number;
  max: number;
  step?: number;
  className?: string;
  validation?: InputValidation;
  showValidation?: boolean;
  conversionContext?: 'height' | 'weight';
  confidenceIndicator?: boolean;
}

const EnhancedInputField: React.FC<EnhancedInputFieldProps> = ({
  label,
  value,
  onChange,
  unit,
  min,
  max,
  step = 1,
  className = '',
  validation,
  showValidation = true,
  conversionContext,
  confidenceIndicator = false
}) => {
  const [inputValue, setInputValue] = useState(value.toString());
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);

  // Update local input when prop value changes
  useEffect(() => {
    if (value !== Number(inputValue)) {
      setInputValue(value.toString());
    }
  }, [value]);

  // Input validation based on academic research
  const getValidationState = (inputVal: number): InputValidation => {
    if (isNaN(inputVal)) {
      return {
        isValid: false,
        message: 'Please enter a valid number',
        severity: 'error'
      };
    }

    if (inputVal < min) {
      return {
        isValid: false,
        message: `Minimum value is ${min} ${unit}`,
        severity: 'error',
        suggestion: getConversionSuggestion(inputVal, conversionContext)
      };
    }

    if (inputVal > max) {
      return {
        isValid: false,
        message: `Maximum value is ${max} ${unit}`,
        severity: 'error',
        suggestion: getConversionSuggestion(inputVal, conversionContext)
      };
    }

    // Contextual suggestions based on demographic data
    if (conversionContext) {
      const contextualCheck = getContextualValidation(inputVal, conversionContext);
      if (contextualCheck) {
        return contextualCheck;
      }
    }

    return { isValid: true };
  };

  // Contextual validation based on anthropometric data
  const getContextualValidation = (val: number, context: string): InputValidation | null => {
    if (context === 'height') {
      if (val < 160) {
        return {
          isValid: true,
          message: 'Height is shorter than average (15th percentile)',
          severity: 'info',
          suggestion: 'Consider checking if units are correct'
        };
      }
      if (val > 195) {
        return {
          isValid: true,
          message: 'Height is taller than average (85th percentile)',
          severity: 'info',
          suggestion: 'Special sizing may be needed'
        };
      }
    }

    if (context === 'weight') {
      if (val < 55) {
        return {
          isValid: true,
          message: 'Weight is lighter than average',
          severity: 'warning',
          suggestion: 'Slim fit may be recommended'
        };
      }
      if (val > 100) {
        return {
          isValid: true,
          message: 'Weight is heavier than average',
          severity: 'warning',
          suggestion: 'Relaxed fit may be more comfortable'
        };
      }
    }

    return null;
  };

  // Conversion suggestions
  const getConversionSuggestion = (val: number, context?: string): string => {
    if (!context) return '';
    
    if (context === 'height' && unit === 'cm') {
      return `Equivalent to ${(val * 0.393701).toFixed(1)} inches`;
    }
    if (context === 'height' && unit === 'inches') {
      return `Equivalent to ${(val * 2.54).toFixed(0)} cm`;
    }
    if (context === 'weight' && unit === 'kg') {
      return `Equivalent to ${(val * 2.20462).toFixed(1)} lbs`;
    }
    if (context === 'weight' && unit === 'lbs') {
      return `Equivalent to ${(val * 0.453592).toFixed(1)} kg`;
    }
    
    return '';
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    
    // Parse number, allow empty input during typing
    const numValue = parseFloat(newValue);
    if (!isNaN(numValue)) {
      onChange(numValue);
    }
  };

  const handleBlur = () => {
    setIsFocused(false);
    
    // Validate and clamp value if needed
    const numValue = parseFloat(inputValue);
    if (!isNaN(numValue)) {
      const clampedValue = Math.max(min, Math.min(max, numValue));
      if (clampedValue !== numValue) {
        setInputValue(clampedValue.toString());
        onChange(clampedValue);
      }
    }
  };

  const validationState = getValidationState(parseFloat(inputValue));
  const displayValidation = validation || validationState;
  const hasValidation = showValidation && displayValidation;

  return (
    <div className={`w-full ${className}`}>
      {/* Label with unit */}
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-medium text-gray-700">
          {label}
        </label>
        <span className="text-sm text-gray-500">{unit}</span>
      </div>

      {/* Input Container */}
      <div className="relative">
        <input
          type="number"
          value={inputValue}
          onChange={handleInputChange}
          onFocus={() => setIsFocused(true)}
          onBlur={handleBlur}
          min={min}
          max={max}
          step={step}
          className={`
            w-full px-4 py-3 border-2 rounded-lg transition-all duration-200
            ${hasValidation && !displayValidation.isValid
              ? 'border-red-300 bg-red-50 focus:border-red-500 focus:bg-white'
              : hasValidation && displayValidation.severity === 'warning'
              ? 'border-yellow-300 bg-yellow-50 focus:border-yellow-500 focus:bg-white'
              : hasValidation && displayValidation.isValid && isFocused
              ? 'border-blue-300 bg-blue-50 focus:border-blue-500'
              : 'border-gray-300 bg-white focus:border-blue-500'
            }
            focus:outline-none focus:ring-2 focus:ring-blue-500/20
            text-lg font-medium
          `}
          placeholder={`${min}-${max}`}
        />

        {/* Status Icons */}
        <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
          {hasValidation ? (
            displayValidation.isValid ? (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            ) : (
              <AlertCircle className="w-5 h-5 text-red-500" />
            )
          ) : (
            <div className="w-5 h-5" />
          )}
        </div>

        {/* Quick action buttons for common values */}
        {isFocused && conversionContext && (
          <div className="absolute right-12 top-1/2 transform -translate-y-1/2">
            <button
              onClick={() => setShowSuggestions(!showSuggestions)}
              className="p-1 text-gray-400 hover:text-blue-600 transition-colors"
              aria-label="Show suggestions"
            >
              <Info size={14} />
            </button>
          </div>
        )}
      </div>

      {/* Validation Message */}
      {hasValidation && displayValidation.message && (
        <div className={`
          mt-2 flex items-start gap-2 p-2 rounded-md text-sm
          ${displayValidation.isValid 
            ? displayValidation.severity === 'warning'
              ? 'bg-yellow-50 text-yellow-800 border border-yellow-200'
              : displayValidation.severity === 'info'
              ? 'bg-blue-50 text-blue-800 border border-blue-200'
              : 'bg-green-50 text-green-800 border border-green-200'
            : 'bg-red-50 text-red-800 border border-red-200'
          }
        `}>
          <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <div>
            <p>{displayValidation.message}</p>
            {displayValidation.suggestion && (
              <p className="mt-1 opacity-90">
                💡 {displayValidation.suggestion}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Quick Conversion Suggestions */}
      {showSuggestions && conversionContext && (
        <div className="mt-2 p-3 bg-gray-50 rounded-lg border border-gray-200">
          <h5 className="text-sm font-medium text-gray-900 mb-2">Quick Conversions</h5>
          <div className="space-y-1 text-sm text-gray-600">
            {conversionContext === 'height' && unit === 'cm' && (
              <>
                <p>160cm = 5'3"</p>
                <p>175cm = 5'9"</p>
                <p>190cm = 6'3"</p>
              </>
            )}
            {conversionContext === 'height' && unit === 'inches' && (
              <>
                <p>63" = 160cm (5'3")</p>
                <p>69" = 175cm (5'9")</p>
                <p>75" = 190cm (6'3")</p>
              </>
            )}
            {conversionContext === 'weight' && unit === 'kg' && (
              <>
                <p>70kg = 154 lbs</p>
                <p>80kg = 176 lbs</p>
                <p>90kg = 198 lbs</p>
              </>
            )}
            {conversionContext === 'weight' && unit === 'lbs' && (
              <>
                <p>154 lbs = 70kg</p>
                <p>176 lbs = 80kg</p>
                <p>198 lbs = 90kg</p>
              </>
            )}
          </div>
        </div>
      )}

      {/* Confidence Indicator */}
      {confidenceIndicator && (
        <div className="mt-2 flex items-center gap-2 text-sm text-gray-600">
          <TrendingUp size={14} />
          <span>Accuracy: {displayValidation.isValid ? 'High' : 'Check values'}</span>
        </div>
      )}
    </div>
  );
};

export default EnhancedInputField;