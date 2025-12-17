/**
 * Enhanced App Component
 * Integrates all enhancements based on research findings
 * Implements performance monitoring and improved user experience
 */

import React from 'react';
import EnhancedHome from './EnhancedHome';
import { usePerformanceMonitoring } from '../hooks/usePerformanceMonitoring';
import { BarChart3, TrendingUp, Zap, Award, RefreshCw } from 'lucide-react';

const EnhancedApp: React.FC = () => {
  const { 
    stats, 
    getPerformanceGrade, 
    clearMetrics, 
    getRecentMetrics 
  } = usePerformanceMonitoring();

  const performanceGrade = getPerformanceGrade();
  const recentMetrics = getRecentMetrics(5);

  // Performance monitoring dashboard (can be toggled)
  const [showPerformanceDashboard, setShowPerformanceDashboard] = React.useState(false);

  React.useEffect(() => {
    // Track page load performance
    const loadTime = performance.now();
    console.log(`🚀 App loaded in ${loadTime.toFixed(0)}ms`);

    // Track user engagement
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        console.log('👋 User left the page');
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  return (
    <div className="min-h-screen">
      {/* Performance Dashboard Toggle */}
      <div className="fixed top-4 right-4 z-50">
        <button
          onClick={() => setShowPerformanceDashboard(!showPerformanceDashboard)}
          className={`
            p-3 rounded-full shadow-lg transition-all duration-200
            ${showPerformanceDashboard
              ? 'bg-blue-600 text-white'
              : 'bg-white text-gray-600 hover:bg-gray-50'
            }
          `}
          aria-label="Toggle performance dashboard"
        >
          <BarChart3 size={20} />
        </button>
      </div>

      {/* Performance Dashboard */}
      {showPerformanceDashboard && (
        <div className="fixed top-16 right-4 z-40 w-80 bg-white rounded-lg shadow-xl border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 flex items-center gap-2">
              <TrendingUp size={16} />
              Performance Dashboard
            </h3>
            <button
              onClick={clearMetrics}
              className="p-1 text-gray-400 hover:text-red-600 transition-colors"
              aria-label="Clear performance data"
            >
              <RefreshCw size={14} />
            </button>
          </div>

          <div className="space-y-3">
            {/* Performance Grade */}
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">Performance Grade</span>
              <div className="flex items-center gap-2">
                <span className={`text-lg font-bold text-${performanceGrade.color}-600`}>
                  {performanceGrade.grade}
                </span>
                <Award size={16} className={`text-${performanceGrade.color}-600`} />
              </div>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-2 gap-2">
              <div className="p-2 bg-blue-50 rounded text-center">
                <div className="text-lg font-bold text-blue-700">
                  {stats.avgResponseTime.toFixed(0)}ms
                </div>
                <div className="text-xs text-blue-600">Avg Response</div>
              </div>
              <div className="p-2 bg-green-50 rounded text-center">
                <div className="text-lg font-bold text-green-700">
                  {stats.totalRequests}
                </div>
                <div className="text-xs text-green-600">Total Requests</div>
              </div>
            </div>

            {/* Detailed Stats */}
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Cache Hit Rate</span>
                <span className="font-medium">{stats.cacheHitRate.toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Success Rate</span>
                <span className="font-medium">{stats.successRate.toFixed(1)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Last Updated</span>
                <span className="font-medium">
                  {stats.lastUpdated > 0 
                    ? new Date(stats.lastUpdated).toLocaleTimeString()
                    : 'Never'
                  }
                </span>
              </div>
            </div>

            {/* Recent Activity */}
            {recentMetrics.length > 0 && (
              <div>
                <h4 className="text-xs font-medium text-gray-500 mb-2 uppercase tracking-wide">
                  Recent Activity
                </h4>
                <div className="space-y-1">
                  {recentMetrics.map((metric, index) => (
                    <div key={index} className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-1">
                        {metric.cached && <Zap size={10} className="text-yellow-500" />}
                        <span className="text-gray-600">
                          {metric.success ? 'Success' : 'Failed'}
                        </span>
                      </div>
                      <span className="font-medium">
                        {metric.value.toFixed(0)}ms
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Performance Tips */}
            <div className="p-2 bg-yellow-50 border border-yellow-200 rounded text-xs">
              <p className="text-yellow-800">
                <strong>Tip:</strong> Cache hits significantly improve response times. 
                {stats.cacheHitRate < 30 && ' Consider repeating common measurements.'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Application */}
      <EnhancedHome />

      {/* Development Info */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed bottom-4 left-4 bg-gray-900 text-white p-2 rounded text-xs font-mono opacity-75">
          Enhanced SuitSize.ai v2.0 • Performance Grade: {performanceGrade.grade}
        </div>
      )}
    </div>
  );
};

export default EnhancedApp;