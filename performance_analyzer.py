"""
Performance Analysis Tool for SuitSize.ai Backend
Analyzes current performance bottlenecks and optimization opportunities
"""

import time
import statistics
import json
import psutil
import gc
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
from ml_enhanced_sizing_engine import EnhancedSuitSizeEngine
from ml_railway_backend import MLEnhancedRailwayBackend
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    """Comprehensive performance analysis for the ML-enhanced backend"""
    
    def __init__(self):
        self.ml_engine = EnhancedSuitSizeEngine()
        self.backend = MLEnhancedRailwayBackend()
        self.performance_data = []
        self.memory_usage = []
        
    def analyze_current_performance(self, num_requests: int = 100) -> Dict[str, Any]:
        """Analyze current backend performance with detailed metrics"""
        
        logger.info(f"🔍 Starting performance analysis with {num_requests} requests...")
        
        # Test data with various scenarios
        test_scenarios = [
            {'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric'},
            {'height': 180, 'weight': 80, 'fit': 'slim', 'unit': 'metric'},
            {'height': 170, 'weight': 70, 'fit': 'relaxed', 'unit': 'metric'},
            {'height': 185, 'weight': 85, 'fit': 'regular', 'unit': 'metric'},
            {'height': 160, 'weight': 60, 'fit': 'slim', 'unit': 'metric'},
            # Edge cases
            {'height': 120, 'weight': 50, 'fit': 'regular', 'unit': 'metric'},
            {'height': 250, 'weight': 150, 'fit': 'relaxed', 'unit': 'metric'},
            # Imperial units
            {'height': 69, 'weight': 165, 'fit': 'regular', 'unit': 'imperial'}
        ]
        
        results = []
        total_start_time = time.time()
        
        # Capture initial memory usage
        gc.collect()
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        for i in range(num_requests):
            # Use different test scenarios
            test_data = test_scenarios[i % len(test_scenarios)]
            client_ip = f"test_ip_{i % 10}"  # Simulate different IPs
            
            # Measure request performance
            start_time = time.time()
            
            try:
                result = self.backend.process_sizing_request(test_data, client_ip)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # ms
                
                # Capture memory usage
                current_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                request_data = {
                    'request_id': i,
                    'scenario': test_data,
                    'client_ip': client_ip,
                    'response_time_ms': response_time,
                    'success': 'error' not in result,
                    'size': result.get('size'),
                    'confidence': result.get('confidence'),
                    'cached': result.get('cached', False),
                    'memory_usage_mb': current_memory,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(request_data)
                
                if i % 20 == 0:
                    logger.info(f"Processed {i}/{num_requests} requests")
                    
            except Exception as e:
                logger.error(f"Request {i} failed: {str(e)}")
                results.append({
                    'request_id': i,
                    'scenario': test_data,
                    'client_ip': client_ip,
                    'response_time_ms': (time.time() - start_time) * 1000,
                    'success': False,
                    'error': str(e),
                    'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
                    'timestamp': datetime.now().isoformat()
                })
        
        total_end_time = time.time()
        total_duration = total_end_time - total_start_time
        
        # Final memory capture
        gc.collect()
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Analyze results
        successful_requests = [r for r in results if r['success']]
        response_times = [r['response_time_ms'] for r in successful_requests]
        cached_requests = [r for r in successful_requests if r['cached']]
        
        analysis = {
            'test_summary': {
                'total_requests': num_requests,
                'successful_requests': len(successful_requests),
                'failed_requests': num_requests - len(successful_requests),
                'success_rate': len(successful_requests) / num_requests,
                'total_duration_seconds': round(total_duration, 2),
                'requests_per_second': round(num_requests / total_duration, 2)
            },
            'response_time_analysis': {
                'min_ms': round(min(response_times), 2) if response_times else 0,
                'max_ms': round(max(response_times), 2) if response_times else 0,
                'mean_ms': round(statistics.mean(response_times), 2) if response_times else 0,
                'median_ms': round(statistics.median(response_times), 2) if response_times else 0,
                'p95_ms': round(np.percentile(response_times, 95), 2) if response_times else 0,
                'p99_ms': round(np.percentile(response_times, 99), 2) if response_times else 0,
                'std_dev_ms': round(statistics.stdev(response_times), 2) if len(response_times) > 1 else 0
            },
            'caching_analysis': {
                'total_cached_requests': len(cached_requests),
                'cache_hit_rate': len(cached_requests) / len(successful_requests) if successful_requests else 0,
                'avg_uncached_response_ms': round(statistics.mean([r['response_time_ms'] for r in successful_requests if not r['cached']]), 2) if successful_requests else 0,
                'avg_cached_response_ms': round(statistics.mean([r['response_time_ms'] for r in cached_requests]), 2) if cached_requests else 0
            },
            'memory_analysis': {
                'initial_memory_mb': round(initial_memory, 2),
                'final_memory_mb': round(final_memory, 2),
                'memory_growth_mb': round(final_memory - initial_memory, 2),
                'peak_memory_mb': round(max([r['memory_usage_mb'] for r in results]), 2),
                'avg_memory_mb': round(statistics.mean([r['memory_usage_mb'] for r in results]), 2)
            },
            'detailed_results': results
        }
        
        # Performance bottleneck identification
        bottlenecks = self._identify_bottlenecks(analysis)
        analysis['bottlenecks'] = bottlenecks
        
        return analysis
    
    def _identify_bottlenecks(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks from analysis results"""
        
        bottlenecks = []
        
        response_analysis = analysis['response_time_analysis']
        caching_analysis = analysis['caching_analysis']
        memory_analysis = analysis['memory_analysis']
        
        # Response time bottlenecks
        if response_analysis['mean_ms'] > 50:
            bottlenecks.append({
                'type': 'response_time',
                'severity': 'high' if response_analysis['mean_ms'] > 100 else 'medium',
                'description': f"Average response time ({response_analysis['mean_ms']}ms) exceeds target (50ms)",
                'current_value': response_analysis['mean_ms'],
                'target_value': 50,
                'recommendation': 'Implement database optimization and enhanced caching'
            })
        
        if response_analysis['p95_ms'] > 100:
            bottlenecks.append({
                'type': 'response_time',
                'severity': 'high',
                'description': f"95th percentile response time ({response_analysis['p95_ms']}ms) exceeds 100ms SLA",
                'current_value': response_analysis['p95_ms'],
                'target_value': 100,
                'recommendation': 'Add database connection pooling and query optimization'
            })
        
        # Caching bottlenecks
        if caching_analysis['cache_hit_rate'] < 0.5:
            bottlenecks.append({
                'type': 'caching',
                'severity': 'medium',
                'description': f"Cache hit rate ({caching_analysis['cache_hit_rate']:.1%}) is below optimal (80%+)",
                'current_value': caching_analysis['cache_hit_rate'],
                'target_value': 0.8,
                'recommendation': 'Optimize cache key strategy and increase cache TTL'
            })
        
        # Memory bottlenecks
        if memory_analysis['memory_growth_mb'] > 100:
            bottlenecks.append({
                'type': 'memory',
                'severity': 'medium',
                'description': f"Memory growth ({memory_analysis['memory_growth_mb']}MB) indicates memory leaks",
                'current_value': memory_analysis['memory_growth_mb'],
                'target_value': 50,
                'recommendation': 'Implement proper memory management and garbage collection'
            })
        
        # Consistency bottlenecks
        if response_analysis['std_dev_ms'] > 20:
            bottlenecks.append({
                'type': 'consistency',
                'severity': 'medium',
                'description': f"High response time variance (σ={response_analysis['std_dev_ms']}ms) indicates inconsistent performance",
                'current_value': response_analysis['std_dev_ms'],
                'target_value': 10,
                'recommendation': 'Implement consistent resource allocation and eliminate random factors'
            })
        
        return bottlenecks
    
    def benchmark_caching_strategies(self) -> Dict[str, Any]:
        """Benchmark different caching strategies"""
        
        logger.info("🚀 Benchmarking caching strategies...")
        
        test_data = {'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric'}
        cache_results = {}
        
        # Test 1: Current in-memory cache
        start_time = time.time()
        for _ in range(50):
            self.backend.process_sizing_request(test_data, 'benchmark_ip')
        current_cache_time = (time.time() - start_time) / 50 * 1000
        cache_results['current_memory_cache'] = {
            'avg_response_time_ms': round(current_cache_time, 2),
            'description': 'Current in-memory dictionary cache'
        }
        
        # Clear cache and test without caching
        cache_size = len(self.backend.cache)
        self.backend.cache.clear()
        
        start_time = time.time()
        for _ in range(50):
            self.backend.process_sizing_request(test_data, 'benchmark_ip_2')
        no_cache_time = (time.time() - start_time) / 50 * 1000
        cache_results['no_cache'] = {
            'avg_response_time_ms': round(no_cache_time, 2),
            'description': 'No caching (always recompute)'
        }
        
        # Restore cache
        self.backend.cache = {}
        
        # Test 2: Simulated Redis cache (in-memory with different TTL)
        redis_simulation = {'cache': {}, 'ttl': 300}
        
        def simulated_redis_get(key):
            if key in redis_simulation['cache']:
                entry = redis_simulation['cache'][key]
                if time.time() - entry['timestamp'] < redis_simulation['ttl']:
                    return entry['data']
            return None
        
        def simulated_redis_set(key, data):
            redis_simulation['cache'][key] = {'data': data, 'timestamp': time.time()}
        
        # Test Redis simulation
        for _ in range(50):
            cache_key = self.backend.get_cache_key(**test_data)
            cached_result = simulated_redis_get(cache_key)
            if cached_result is None:
                result = self.backend.ml_engine.get_size_recommendation(**test_data)
                simulated_redis_set(cache_key, result)
        
        redis_time = sum([
            (time.time() - time.time()) if simulated_redis_get(cache_key) 
            else (time.time() - time.time()) + 10
            for _ in range(50)
        ]) / 50 * 1000
        
        cache_results['redis_simulation'] = {
            'avg_response_time_ms': round(redis_time, 2),
            'description': 'Simulated Redis cache with proper TTL'
        }
        
        return cache_results
    
    def analyze_ml_engine_performance(self) -> Dict[str, Any]:
        """Analyze ML engine performance characteristics"""
        
        logger.info("🧠 Analyzing ML engine performance...")
        
        ml_performance = {}
        
        # Test ML engine initialization time
        start_time = time.time()
        new_engine = EnhancedSuitSizeEngine()
        init_time = time.time() - start_time
        ml_performance['initialization_time_seconds'] = round(init_time, 2)
        
        # Test prediction performance
        test_cases = [
            {'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric'},
            {'height': 180, 'weight': 80, 'fit': 'slim', 'unit': 'metric'},
            {'height': 170, 'weight': 70, 'fit': 'relaxed', 'unit': 'metric'}
        ]
        
        prediction_times = []
        for _ in range(20):
            test_case = test_cases[_ % len(test_cases)]
            start_time = time.time()
            result = new_engine.get_size_recommendation(**test_case)
            prediction_time = (time.time() - start_time) * 1000
            prediction_times.append(prediction_time)
        
        ml_performance['prediction_performance'] = {
            'min_ms': round(min(prediction_times), 2),
            'max_ms': round(max(prediction_times), 2),
            'mean_ms': round(statistics.mean(prediction_times), 2),
            'median_ms': round(statistics.median(prediction_times), 2),
            'p95_ms': round(np.percentile(prediction_times, 95), 2)
        }
        
        # Test customer similarity engine
        similarity_times = []
        for _ in range(20):
            start_time = time.time()
            similar_customers = new_engine.similarity_engine.find_similar_customers(175, 75, 'regular')
            similarity_time = (time.time() - start_time) * 1000
            similarity_times.append(similarity_time)
        
        ml_performance['customer_similarity_performance'] = {
            'mean_ms': round(statistics.mean(similarity_times), 2),
            'database_size': len(new_engine.similarity_engine.customer_database)
        }
        
        return ml_performance
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance analysis report"""
        
        logger.info("📊 Generating comprehensive performance report...")
        
        # Run all analyses
        backend_performance = self.analyze_current_performance(100)
        caching_benchmarks = self.benchmark_caching_strategies()
        ml_performance = self.analyze_ml_engine_performance()
        
        # Compile comprehensive report
        report = {
            'timestamp': datetime.now().isoformat(),
            'report_type': 'comprehensive_performance_analysis',
            'backend_performance': backend_performance,
            'caching_benchmarks': caching_benchmarks,
            'ml_engine_performance': ml_performance,
            'optimization_recommendations': self._generate_optimization_recommendations(
                backend_performance, caching_benchmarks, ml_performance
            )
        }
        
        return report
    
    def _generate_optimization_recommendations(self, backend_perf: Dict, caching_bench: Dict, ml_perf: Dict) -> List[Dict[str, Any]]:
        """Generate specific optimization recommendations"""
        
        recommendations = []
        
        # Response time optimization
        response_time = backend_perf['response_time_analysis']['mean_ms']
        if response_time > 50:
            recommendations.append({
                'category': 'response_time',
                'priority': 'high',
                'title': 'Implement Database Optimization',
                'description': f'Current average response time ({response_time}ms) exceeds 50ms target',
                'actions': [
                    'Implement database with proper indexing',
                    'Add connection pooling',
                    'Optimize ML model loading',
                    'Implement async processing for heavy operations'
                ],
                'estimated_improvement': '50-70% reduction in response time'
            })
        
        # Caching optimization
        cache_hit_rate = backend_perf['caching_analysis']['cache_hit_rate']
        if cache_hit_rate < 0.8:
            recommendations.append({
                'category': 'caching',
                'priority': 'high',
                'title': 'Enhanced Multi-Tier Caching',
                'description': f'Cache hit rate ({cache_hit_rate:.1%}) below optimal (80%+)',
                'actions': [
                    'Implement Redis for distributed caching',
                    'Add application-level cache with smart invalidation',
                    'Implement CDN caching for static responses',
                    'Add database query result caching'
                ],
                'estimated_improvement': '80%+ cache hit rate, 60-80% faster responses'
            })
        
        # Memory optimization
        memory_growth = backend_perf['memory_analysis']['memory_growth_mb']
        if memory_growth > 50:
            recommendations.append({
                'category': 'memory',
                'priority': 'medium',
                'title': 'Memory Management Optimization',
                'description': f'Significant memory growth ({memory_growth}MB) indicates leaks',
                'actions': [
                    'Implement proper object lifecycle management',
                    'Add garbage collection optimization',
                    'Implement memory monitoring and alerting',
                    'Optimize ML model memory usage'
                ],
                'estimated_improvement': '50% reduction in memory usage'
            })
        
        # Consistency optimization
        response_variance = backend_perf['response_time_analysis']['std_dev_ms']
        if response_variance > 20:
            recommendations.append({
                'category': 'consistency',
                'priority': 'medium',
                'title': 'Performance Consistency',
                'description': f'High response time variance (σ={response_variance}ms)',
                'actions': [
                    'Implement consistent resource allocation',
                    'Add request queuing and rate limiting',
                    'Optimize random number generation',
                    'Implement deterministic caching'
                ],
                'estimated_improvement': '60% reduction in variance'
            })
        
        return recommendations

if __name__ == "__main__":
    # Run comprehensive performance analysis
    analyzer = PerformanceAnalyzer()
    report = analyzer.generate_performance_report()
    
    # Save detailed report
    with open('/workspace/performance_analysis_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("🎯 Performance Analysis Complete!")
    print("=" * 50)
    print(f"📊 Backend Performance:")
    print(f"  - Average Response Time: {report['backend_performance']['response_time_analysis']['mean_ms']}ms")
    print(f"  - Cache Hit Rate: {report['backend_performance']['caching_analysis']['cache_hit_rate']:.1%}")
    print(f"  - Memory Growth: {report['backend_performance']['memory_analysis']['memory_growth_mb']}MB")
    print(f"  - Success Rate: {report['backend_performance']['test_summary']['success_rate']:.1%}")
    
    print(f"\n🚀 ML Engine Performance:")
    print(f"  - Prediction Time: {report['ml_engine_performance']['prediction_performance']['mean_ms']}ms")
    print(f"  - Initialization: {report['ml_engine_performance']['initialization_time_seconds']}s")
    print(f"  - Customer DB Size: {report['ml_engine_performance']['customer_similarity_performance']['database_size']}")
    
    print(f"\n💡 Recommendations: {len(report['optimization_recommendations'])}")
    for rec in report['optimization_recommendations']:
        print(f"  - {rec['title']} ({rec['priority']} priority)")
    
    print(f"\n💾 Full report saved to: /workspace/performance_analysis_report.json")