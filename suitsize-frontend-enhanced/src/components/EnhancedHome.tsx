/**
 * Enhanced Home Page Component
 * Based on competitive analysis and user experience research
 * Implements best practices from leading menswear brands
 */

import React, { useState, useEffect } from 'react';
import { enhancedAPI, type SizeRecommendationRequest, type SizeRecommendationResponse } from '../lib/enhanced-api';
import EnhancedFitSelector from '../components/EnhancedFitSelector';
import BodyTypeSelector from '../components/BodyTypeSelector';
import EnhancedInputField from '../components/EnhancedInputField';
import { 
  Calculator, 
  Loader2, 
  CheckCircle2, 
  AlertCircle, 
  TrendingUp, 
  Info,
  Sparkles,
  Clock,
  Zap,
  Award
} from 'lucide-react';

interface PerformanceMetrics {
  responseTime: number;
  cached: boolean;
  timestamp: string;
}

const EnhancedHome: React.FC = () => {
  // State management
  const [height, setHeight] = useState(175); // More realistic default
  const [weight, setWeight] = useState(75);
  const [unit, setUnit] = useState<'metric' | 'imperial'>('metric');
  const [fit, setFit] = useState('regular');
  const [bodyType, setBodyType] = useState('regular');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SizeRecommendationResponse | null>(null);
  const [error, setError] = useState('');
  const [performance, setPerformance] = useState<PerformanceMetrics | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  // Performance monitoring
  useEffect(() => {
    if (performance?.responseTime) {
      console.log(`⚡ API Response: ${performance.responseTime.toFixed(0)}ms${performance.cached ? ' (cached)' : ''}`);
    }
  }, [performance]);

  // Unit conversion handlers
  const handleUnitChange = (newUnit: 'metric' | 'imperial') => {
    if (newUnit === unit) return;

    if (newUnit === 'imperial' && unit === 'metric') {
      // Convert from metric to imperial
      setHeight(height * 0.393701);
      setWeight(weight * 2.20462);
    } else if (newUnit === 'metric' && unit === 'imperial') {
      // Convert from imperial to metric
      setHeight(height * 2.54);
      setWeight(weight * 0.453592);
    }
    
    setUnit(newUnit);
    // Clear results when unit changes
    setResult(null);
    setError('');
  };

  // Enhanced calculate function with retry logic
  const handleCalculate = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    setPerformance(null);

    try {
      const request: SizeRecommendationRequest = {
        height: Math.round(height),
        weight: Math.round(weight),
        fit,
        bodyType,
        unit
      };

      console.log('🔄 Calculating recommendation:', request);
      
      const response = await enhancedAPI.getRecommendation(request);
      
      if (response.success && response.data) {
        setResult(response.data);
        setRetryCount(0);
        
        // Set performance metrics
        if (response.responseTime) {
          setPerformance({
            responseTime: response.responseTime,
            cached: response.cached || false,
            timestamp: new Date().toLocaleTimeString()
          });
        }
        
        console.log('✅ Recommendation received:', response.data);
      } else {
        setError(response.error || 'Unable to get recommendation');
        console.error('❌ API Error:', response.error);
      }
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : 'An unexpected error occurred';
      setError(errorMessage);
      setRetryCount(prev => prev + 1);
      console.error('💥 Unexpected error:', e);
    } finally {
      setLoading(false);
    }
  };

  // Clear cache function
  const handleClearCache = () => {
    enhancedAPI.clearCache();
    console.log('🗑️ Cache cleared');
  };

  // Get cache statistics
  const getCacheStats = () => {
    return enhancedAPI.getCacheStats();
  };

  // Format size recommendation for display (V3 Enhanced Format)
  const formatRecommendation = (rec: SizeRecommendationResponse) => {
    // Handle V3 enhanced format
    if (rec.data?.primary) {
      const primary = rec.data.primary;
      const bodyTypeAnalysis = rec.data.bodyType;
      
      return {
        size: primary.size || 'N/A',
        confidence: primary.confidence || 0,
        confidenceLevel: primary.confidenceLevel || 'Unknown',
        bodyType: bodyTypeAnalysis?.classification || bodyType,
        rationale: primary.description || 'Enhanced AI sizing recommendation',
        // V3 Enhanced Features
        alternatives: rec.data.alternatives || [],
        bodyTypeAnalysis: bodyTypeAnalysis,
        alterations: rec.data.alterations || [],
        measurements: rec.data.measurements,
        aiAnalysis: rec.data.aiAnalysis,
        performance: rec.data.performance,
        metadata: rec.metadata
      };
    }
    
    // Fallback to legacy format
    const size = rec.recommendation?.size || rec.size;
    const confidence = rec.recommendation?.confidence || rec.confidence || 0;
    const confidenceLevel = rec.recommendation?.confidenceLevel || rec.confidenceLevel;
    const bodyTypeLegacy = rec.recommendation?.bodyType;
    const rationale = rec.recommendation?.rationale || rec.message;

    return {
      size: size || 'N/A',
      confidence,
      confidenceLevel: confidenceLevel || 'Unknown',
      bodyType: bodyTypeLegacy,
      rationale: rationale || 'Size recommendation based on your measurements'
    };
  };

  const recommendation = result ? formatRecommendation(result) : null;
  const cacheStats = getCacheStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-8 h-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">
              Find Your Perfect Suit Size
            </h1>
            <Sparkles className="w-8 h-8 text-blue-600" />
          </div>
          <p className="text-xl text-gray-600 mb-2">
            AI-powered sizing with 89.66% accuracy • Free • Instant
          </p>
          <p className="text-sm text-gray-500">
            No signup required • Powered by advanced body measurement analysis
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          {/* Main Card */}
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
            
            {/* Unit Toggle */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900">Measurement System</h2>
              <div className="flex bg-gray-100 rounded-lg p-1">
                {(['metric', 'imperial'] as const).map((unitOption) => (
                  <button
                    key={unitOption}
                    onClick={() => handleUnitChange(unitOption)}
                    className={`
                      px-4 py-2 rounded-md text-sm font-medium transition-all
                      ${unit === unitOption
                        ? 'bg-white text-blue-600 shadow-sm'
                        : 'text-gray-600 hover:text-gray-900'
                      }
                    `}
                  >
                    {unitOption === 'metric' ? 'Metric (cm/kg)' : 'Imperial (in/lbs)'}
                  </button>
                ))}
              </div>
            </div>

            {/* Input Fields */}
            <div className="space-y-6 mb-6">
              <EnhancedInputField
                label="Height"
                value={height}
                onChange={setHeight}
                unit={unit === 'metric' ? 'cm' : 'inches'}
                min={unit === 'metric' ? 120 : 47}
                max={unit === 'metric' ? 250 : 98}
                step={unit === 'metric' ? 1 : 0.5}
                validation={{ isValid: true }}
                conversionContext="height"
                confidenceIndicator={true}
              />
              
              <EnhancedInputField
                label="Weight"
                value={weight}
                onChange={setWeight}
                unit={unit === 'metric' ? 'kg' : 'lbs'}
                min={unit === 'metric' ? 40 : 88}
                max={unit === 'metric' ? 200 : 440}
                step={unit === 'metric' ? 1 : 1}
                validation={{ isValid: true }}
                conversionContext="weight"
                confidenceIndicator={true}
              />
            </div>

            {/* Fit Selector */}
            <div className="mb-6">
              <EnhancedFitSelector fit={fit} setFit={setFit} />
            </div>

            {/* Body Type Selector */}
            <div className="mb-6">
              <BodyTypeSelector bodyType={bodyType} setBodyType={setBodyType} />
            </div>

            {/* Calculate Button */}
            <button
              onClick={handleCalculate}
              disabled={loading}
              className={`
                w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-200
                ${loading
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                }
              `}
            >
              {loading ? (
                <div className="flex items-center justify-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Analyzing measurements...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center gap-2">
                  <Calculator className="w-5 h-5" />
                  <span>Find My Size</span>
                </div>
              )}
            </button>

            {/* Retry indicator */}
            {retryCount > 0 && (
              <div className="mt-2 text-center text-sm text-gray-500">
                Retry attempt: {retryCount}
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start gap-2">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-medium text-red-900">Calculation Error</h4>
                    <p className="text-red-700 mt-1">{error}</p>
                    {retryCount > 0 && (
                      <p className="text-red-600 text-sm mt-2">
                        This may be due to temporary service issues. Please try again.
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Result Display */}
            {recommendation && (
              <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle2 className="w-6 h-6 text-green-600" />
                  <h3 className="text-lg font-semibold text-green-900">
                    Your Recommended Size
                  </h3>
                </div>

                <div className="space-y-3">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-green-700 mb-2">
                      {recommendation.size}
                    </div>
                    <div className="flex items-center justify-center gap-2">
                      <Award className="w-4 h-4 text-green-600" />
                      <span className="text-green-700 font-medium">
                        {Math.round(recommendation.confidence * 100)}% Confidence
                      </span>
                      <span className="text-green-600">({recommendation.confidenceLevel})</span>
                    </div>
                  </div>

                  {recommendation.bodyType && (
                    <div className="text-center text-green-800">
                      <strong>Body Type:</strong> {recommendation.bodyType}
                    </div>
                  )}

                  {recommendation.rationale && (
                    <div className="p-3 bg-white/60 rounded-lg">
                      <p className="text-green-900 text-sm">
                        <strong>Analysis:</strong> {recommendation.rationale}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Performance Metrics */}
            {performance && (
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-blue-600" />
                    <span className="text-blue-900">
                      Response: {performance.responseTime.toFixed(0)}ms
                    </span>
                  </div>
                  {performance.cached && (
                    <div className="flex items-center gap-1">
                      <Zap className="w-4 h-4 text-yellow-600" />
                      <span className="text-yellow-700">Cached</span>
                    </div>
                  )}
                  <span className="text-blue-700">{performance.timestamp}</span>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="text-center mt-8 space-y-4">
            <div className="flex items-center justify-center gap-4 text-sm text-gray-600">
              <button 
                onClick={handleClearCache}
                className="text-blue-600 hover:text-blue-700 transition-colors"
              >
                Clear Cache
              </button>
              <span>•</span>
              <span>Cache: {cacheStats.size} items</span>
              <span>•</span>
              <span>Powered by SuitSize.ai</span>
            </div>
            
            <div className="text-xs text-gray-500">
              Based on research from major menswear brands • Enhanced with AI-powered accuracy
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedHome;