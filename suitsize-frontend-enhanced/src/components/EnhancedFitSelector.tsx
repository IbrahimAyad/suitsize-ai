/**
 * Enhanced FitSelector Component
 * Based on competitive analysis of major menswear brands
 * Implements best practices from Tommy Hilfiger, Brooks Brothers, and Charles Tyrwhitt
 */

import React, { useState } from 'react';
import { Info, CheckCircle2, Circle } from 'lucide-react';

export interface FitOption {
  label: string;
  value: string;
  description: string;
  characteristics: string[];
  popularity?: string; // Based on market research
}

interface EnhancedFitSelectorProps {
  fit: string;
  setFit: (fit: string) => void;
  className?: string;
}

const fitOptions: FitOption[] = [
  {
    label: 'Slim',
    value: 'slim',
    description: 'Contoured fit with tapered waist',
    characteristics: ['Narrower shoulders', 'Tapered waist', 'Modern look'],
    popularity: 'Best for athletic builds'
  },
  {
    label: 'Regular',
    value: 'regular',
    description: 'Classic traditional fit',
    characteristics: ['Standard shoulders', 'Comfortable waist', 'Timeless style'],
    popularity: 'Most popular choice'
  },
  {
    label: 'Relaxed',
    value: 'relaxed',
    description: 'Looser comfort fit',
    characteristics: ['Roomy shoulders', 'Extra room in waist', 'Casual comfort'],
    popularity: 'Best for comfort preference'
  }
];

const EnhancedFitSelector: React.FC<EnhancedFitSelectorProps> = ({ 
  fit, 
  setFit, 
  className = '' 
}) => {
  const [hoveredOption, setHoveredOption] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  const selectedOption = fitOptions.find(option => option.value === fit.toLowerCase());

  return (
    <div className={`w-full ${className}`}>
      {/* Header with info toggle */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Preferred Fit Style</h3>
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center gap-1 text-blue-600 hover:text-blue-700 transition-colors"
          aria-label="Toggle fit information"
        >
          <Info size={16} />
          <span className="text-sm">Details</span>
        </button>
      </div>

      {/* Fit Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {fitOptions.map((option) => {
          const isSelected = option.value === fit.toLowerCase();
          const isHovered = hoveredOption === option.value;

          return (
            <button
              key={option.value}
              onClick={() => setFit(option.value)}
              onMouseEnter={() => setHoveredOption(option.value)}
              onMouseLeave={() => setHoveredOption(null)}
              className={`
                relative p-4 rounded-xl border-2 transition-all duration-200 text-left
                ${isSelected 
                  ? 'border-blue-500 bg-blue-50 shadow-md' 
                  : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm'
                }
                ${isHovered && !isSelected ? 'transform scale-[1.02]' : ''}
              `}
              aria-pressed={isSelected}
              aria-label={`Select ${option.label} fit: ${option.description}`}
            >
              {/* Selection indicator */}
              <div className="absolute top-3 right-3">
                {isSelected ? (
                  <CheckCircle2 className="w-5 h-5 text-blue-600" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-400" />
                )}
              </div>

              {/* Option content */}
              <div className="pr-6">
                <h4 className={`
                  font-semibold text-base mb-1
                  ${isSelected ? 'text-blue-900' : 'text-gray-900'}
                `}>
                  {option.label}
                </h4>
                
                <p className={`
                  text-sm mb-2
                  ${isSelected ? 'text-blue-700' : 'text-gray-600'}
                `}>
                  {option.description}
                </p>

                {/* Characteristics (shown on hover or when selected) */}
                {(isSelected || isHovered || showDetails) && (
                  <div className="mt-3 space-y-1">
                    {option.characteristics.map((char, index) => (
                      <div key={index} className="flex items-center text-xs">
                        <div className="w-1 h-1 bg-gray-400 rounded-full mr-2" />
                        <span className="text-gray-600">{char}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Popularity indicator */}
                {option.popularity && (
                  <div className="mt-2 text-xs text-gray-500 italic">
                    💡 {option.popularity}
                  </div>
                )}
              </div>

              {/* Selection border effect */}
              {isSelected && (
                <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/10 to-blue-600/10 pointer-events-none" />
              )}
            </button>
          );
        })}
      </div>

      {/* Enhanced Information Panel */}
      {showDetails && selectedOption && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h5 className="font-medium text-gray-900 mb-2">
            About {selectedOption.label} Fit
          </h5>
          <div className="text-sm text-gray-600 space-y-1">
            <p>{selectedOption.description}</p>
            <p><strong>Best for:</strong> {selectedOption.popularity}</p>
            <p><strong>Key features:</strong> {selectedOption.characteristics.join(', ')}</p>
          </div>
        </div>
      )}

      {/* Size Recommendation Context */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start gap-2">
          <Info className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm">
            <p className="text-blue-900 font-medium mb-1">
              How this affects your size recommendation
            </p>
            <p className="text-blue-700">
              Your fit preference helps our AI algorithm consider the appropriate garment measurements, 
              ensuring you get the most accurate size recommendation for your style preference.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedFitSelector;