/**
 * Performance Monitoring Hook
 * Based on API performance analysis findings
 * Tracks response times, cache hits, and user interactions
 */

import { useState, useEffect, useCallback } from 'react';

interface PerformanceMetric {
  name: string;
  value: number;
  timestamp: number;
  cached?: boolean;
  success?: boolean;
}

interface PerformanceStats {
  avgResponseTime: number;
  totalRequests: number;
  cacheHitRate: number;
  successRate: number;
  lastUpdated: number;
}

const STORAGE_KEY = 'suitsize-performance-metrics';

export const usePerformanceMonitoring = () => {
  const [metrics, setMetrics] = useState<PerformanceMetric[]>([]);
  const [stats, setStats] = useState<PerformanceStats>({
    avgResponseTime: 0,
    totalRequests: 0,
    cacheHitRate: 0,
    successRate: 0,
    lastUpdated: 0
  });

  // Load metrics from localStorage on mount
  useEffect(() => {
    const savedMetrics = localStorage.getItem(STORAGE_KEY);
    if (savedMetrics) {
      try {
        const parsed = JSON.parse(savedMetrics);
        setMetrics(parsed);
        calculateStats(parsed);
      } catch (error) {
        console.warn('Failed to load performance metrics:', error);
      }
    }
  }, []);

  // Save metrics to localStorage whenever they change
  useEffect(() => {
    if (metrics.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(metrics));
    }
  }, [metrics]);

  const recordMetric = useCallback((metric: Omit<PerformanceMetric, 'timestamp'>) => {
    const newMetric: PerformanceMetric = {
      ...metric,
      timestamp: Date.now()
    };

    setMetrics(prev => {
      const updated = [...prev, newMetric];
      // Keep only last 100 metrics to prevent storage bloat
      if (updated.length > 100) {
        return updated.slice(-100);
      }
      return updated;
    });

    calculateStats(metrics);
  }, [metrics]);

  const recordAPIRequest = useCallback((
    responseTime: number,
    success: boolean,
    cached: boolean = false
  ) => {
    recordMetric({
      name: 'api_request',
      value: responseTime,
      cached,
      success
    });
  }, [recordMetric]);

  const recordUserInteraction = useCallback((interaction: string, duration?: number) => {
    recordMetric({
      name: 'user_interaction',
      value: duration || 1,
      success: true
    });
  }, [recordMetric]);

  const calculateStats = useCallback((metricList: PerformanceMetric[]) => {
    if (metricList.length === 0) {
      setStats({
        avgResponseTime: 0,
        totalRequests: 0,
        cacheHitRate: 0,
        successRate: 0,
        lastUpdated: Date.now()
      });
      return;
    }

    const apiMetrics = metricList.filter(m => m.name === 'api_request');
    
    if (apiMetrics.length === 0) {
      setStats({
        avgResponseTime: 0,
        totalRequests: 0,
        cacheHitRate: 0,
        successRate: 0,
        lastUpdated: Date.now()
      });
      return;
    }

    const responseTimes = apiMetrics.map(m => m.value);
    const cachedCount = apiMetrics.filter(m => m.cached).length;
    const successCount = apiMetrics.filter(m => m.success).length;

    const newStats: PerformanceStats = {
      avgResponseTime: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
      totalRequests: apiMetrics.length,
      cacheHitRate: (cachedCount / apiMetrics.length) * 100,
      successRate: (successCount / apiMetrics.length) * 100,
      lastUpdated: Date.now()
    };

    setStats(newStats);
  }, []);

  const getRecentMetrics = useCallback((count: number = 10) => {
    return metrics.slice(-count);
  }, [metrics]);

  const clearMetrics = useCallback(() => {
    setMetrics([]);
    localStorage.removeItem(STORAGE_KEY);
    calculateStats([]);
  }, [calculateStats]);

  const getPerformanceGrade = useCallback(() => {
    const { avgResponseTime, cacheHitRate, successRate } = stats;
    
    // Grading based on industry benchmarks from research
    if (avgResponseTime < 100 && cacheHitRate > 50 && successRate > 95) {
      return { grade: 'A+', color: 'green', description: 'Excellent performance' };
    } else if (avgResponseTime < 200 && cacheHitRate > 30 && successRate > 90) {
      return { grade: 'A', color: 'green', description: 'Very good performance' };
    } else if (avgResponseTime < 500 && cacheHitRate > 20 && successRate > 85) {
      return { grade: 'B', color: 'yellow', description: 'Good performance' };
    } else if (avgResponseTime < 1000 && successRate > 80) {
      return { grade: 'C', color: 'orange', description: 'Acceptable performance' };
    } else {
      return { grade: 'D', color: 'red', description: 'Needs improvement' };
    }
  }, [stats]);

  return {
    stats,
    metrics,
    recordAPIRequest,
    recordUserInteraction,
    getRecentMetrics,
    clearMetrics,
    getPerformanceGrade
  };
};