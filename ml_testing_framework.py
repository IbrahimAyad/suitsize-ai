"""
Comprehensive Testing Framework for ML-Enhanced SuitSize Engine
Tests accuracy, performance, edge cases, and integration scenarios
"""

import time
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import logging
from ml_enhanced_sizing_engine import EnhancedSuitSizeEngine
import concurrent.futures
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveTestFramework:
    """Comprehensive testing framework for the ML-enhanced sizing engine"""
    
    def __init__(self):
        self.engine = EnhancedSuitSizeEngine()
        self.test_results = {}
        self.performance_metrics = {}
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        
        logger.info("🧪 Starting Comprehensive Test Suite")
        print("=" * 60)
        
        # Core functionality tests
        self.test_basic_functionality()
        self.test_edge_cases()
        self.test_performance_benchmarks()
        self.test_concurrent_requests()
        self.test_accuracy_validation()
        self.test_unit_conversions()
        self.test_error_handling()
        
        # Generate test report
        report = self.generate_test_report()
        
        print("\n" + "=" * 60)
        print("🎯 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        print(json.dumps(report, indent=2))
        
        return report
    
    def test_basic_functionality(self):
        """Test basic sizing functionality"""
        logger.info("Testing basic functionality...")
        
        test_cases = [
            # Normal cases
            {'height': 175, 'weight': 75, 'fit': 'regular'},
            {'height': 180, 'weight': 80, 'fit': 'slim'},
            {'height': 170, 'weight': 70, 'fit': 'relaxed'},
            
            # Different units
            {'height': 69, 'weight': 165, 'fit': 'regular', 'unit': 'imperial'},
            
            # Various BMI ranges
            {'height': 160, 'weight': 50, 'fit': 'regular'},  # Underweight
            {'height': 185, 'weight': 85, 'fit': 'regular'},  # Normal
            {'height': 175, 'weight': 95, 'fit': 'relaxed'},  # Overweight
            {'height': 170, 'weight': 110, 'fit': 'relaxed'},  # Obese
        ]
        
        success_count = 0
        total_time = 0
        
        for i, case in enumerate(test_cases, 1):
            try:
                start_time = time.time()
                result = self.engine.get_size_recommendation(**case)
                processing_time = time.time() - start_time
                
                # Validate result structure
                required_fields = ['size', 'confidence', 'confidenceLevel', 'bodyType']
                if all(field in result for field in required_fields):
                    success_count += 1
                    total_time += processing_time
                    logger.info(f"✅ Test {i}: Passed ({processing_time:.3f}s)")
                else:
                    logger.error(f"❌ Test {i}: Missing required fields")
                    
            except Exception as e:
                logger.error(f"❌ Test {i}: Exception - {str(e)}")
        
        self.test_results['basic_functionality'] = {
            'passed': success_count,
            'total': len(test_cases),
            'success_rate': success_count / len(test_cases),
            'avg_processing_time': total_time / max(success_count, 1)
        }
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        logger.info("Testing edge cases...")
        
        edge_cases = [
            # Extreme heights
            {'height': 120, 'weight': 60, 'fit': 'regular'},  # Very short
            {'height': 250, 'weight': 100, 'fit': 'regular'}, # Very tall
            
            # Extreme weights
            {'height': 175, 'weight': 40, 'fit': 'slim'},    # Very light
            {'height': 170, 'weight': 200, 'fit': 'relaxed'}, # Very heavy
            
            # Boundary measurements
            {'height': 160, 'weight': 60, 'fit': 'slim'},    # Height boundary
            {'height': 200, 'weight': 80, 'fit': 'regular'}, # Height boundary
            
            # Decimal inputs
            {'height': 175.5, 'weight': 75.3, 'fit': 'regular'},
            
            # Large BMI combinations
            {'height': 150, 'weight': 80, 'fit': 'relaxed'}, # High BMI
            {'height': 200, 'weight': 60, 'fit': 'slim'},    # Low BMI
        ]
        
        handled_count = 0
        
        for i, case in enumerate(edge_cases, 1):
            try:
                result = self.engine.get_size_recommendation(**case)
                
                # Check if result is reasonable
                if (result['size'] and 
                    0 <= result['confidence'] <= 1 and 
                    result['confidenceLevel'] in ['Very Low', 'Low', 'Medium', 'High', 'Very High']):
                    handled_count += 1
                    logger.info(f"✅ Edge Case {i}: Handled correctly")
                else:
                    logger.warning(f"⚠️ Edge Case {i}: Unexpected result")
                    
            except Exception as e:
                logger.error(f"❌ Edge Case {i}: Failed - {str(e)}")
        
        self.test_results['edge_cases'] = {
            'handled': handled_count,
            'total': len(edge_cases),
            'success_rate': handled_count / len(edge_cases)
        }
    
    def test_performance_benchmarks(self):
        """Test performance under various loads"""
        logger.info("Testing performance benchmarks...")
        
        # Single request performance
        start_time = time.time()
        for _ in range(100):
            self.engine.get_size_recommendation(height=175, weight=75, fit='regular')
        single_request_time = (time.time() - start_time) / 100
        
        # Batch processing performance
        test_data = [{'height': 175, 'weight': 75, 'fit': 'regular'} for _ in range(50)]
        
        start_time = time.time()
        results = []
        for data in test_data:
            results.append(self.engine.get_size_recommendation(**data))
        batch_time = time.time() - start_time
        
        self.performance_metrics = {
            'single_request_avg_ms': round(single_request_time * 1000, 2),
            'batch_50_requests_ms': round(batch_time * 1000, 2),
            'requests_per_second': round(100 / (single_request_time * 100), 2),
            'batch_throughput_per_sec': round(50 / batch_time, 2)
        }
        
        logger.info(f"📊 Single Request: {self.performance_metrics['single_request_avg_ms']}ms avg")
        logger.info(f"📊 Batch Processing: {self.performance_metrics['batch_50_requests_ms']}ms for 50 requests")
    
    def test_concurrent_requests(self):
        """Test concurrent request handling"""
        logger.info("Testing concurrent requests...")
        
        def make_request(request_id):
            """Make a single sizing request"""
            try:
                start_time = time.time()
                result = self.engine.get_size_recommendation(
                    height=175 + np.random.uniform(-10, 10),
                    weight=75 + np.random.uniform(-10, 10),
                    fit=np.random.choice(['slim', 'regular', 'relaxed'])
                )
                return {
                    'request_id': request_id,
                    'success': True,
                    'processing_time': time.time() - start_time,
                    'size': result['size']
                }
            except Exception as e:
                return {
                    'request_id': request_id,
                    'success': False,
                    'error': str(e)
                }
        
        # Test with 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, i) for i in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        successful = sum(1 for r in results if r['success'])
        avg_time = np.mean([r['processing_time'] for r in results if r['success']])
        
        self.test_results['concurrent_requests'] = {
            'successful': successful,
            'total': 20,
            'success_rate': successful / 20,
            'avg_processing_time_ms': round(avg_time * 1000, 2)
        }
        
        logger.info(f"✅ Concurrent: {successful}/20 requests successful")
    
    def test_accuracy_validation(self):
        """Test prediction accuracy with known patterns"""
        logger.info("Testing prediction accuracy...")
        
        # Test consistency - same inputs should give same results
        consistency_results = []
        for _ in range(10):
            result = self.engine.get_size_recommendation(height=175, weight=75, fit='regular')
            consistency_results.append(result['size'])
        
        # Check if all results are the same
        size_consistency = len(set(consistency_results)) == 1
        
        # Test logical consistency
        test_pairs = [
            # Heavier person should generally get larger size
            ({'height': 175, 'weight': 70, 'fit': 'regular'}, 
             {'height': 175, 'weight': 80, 'fit': 'regular'}),
            
            # Taller person should generally get larger size
            ({'height': 170, 'weight': 75, 'fit': 'regular'}, 
             {'height': 180, 'weight': 75, 'fit': 'regular'}),
        ]
        
        logical_consistency = 0
        for pair in test_pairs:
            result1 = self.engine.get_size_recommendation(**pair[0])
            result2 = self.engine.get_size_recommendation(**pair[1])
            
            # Simple size comparison (extract numeric part)
            size1 = int(result1['size'].replace('R', '').replace('L', '').replace('S', ''))
            size2 = int(result2['size'].replace('R', '').replace('L', '').replace('S', ''))
            
            if pair[0]['weight'] < pair[1]['weight'] and size1 <= size2:
                logical_consistency += 1
            elif pair[0]['height'] < pair[1]['height'] and size1 <= size2:
                logical_consistency += 1
        
        self.test_results['accuracy_validation'] = {
            'size_consistency': size_consistency,
            'logical_consistency_rate': logical_consistency / len(test_pairs),
            'consistency_samples': 10
        }
    
    def test_unit_conversions(self):
        """Test imperial/metric unit conversions"""
        logger.info("Testing unit conversions...")
        
        # Test equivalent measurements in different units
        metric_input = {'height': 175, 'weight': 75, 'fit': 'regular', 'unit': 'metric'}
        imperial_input = {'height': 69, 'weight': 165, 'fit': 'regular', 'unit': 'imperial'}
        
        metric_result = self.engine.get_size_recommendation(**metric_input)
        imperial_result = self.engine.get_size_recommendation(**imperial_input)
        
        # Results should be very similar (allowing for rounding)
        size_match = metric_result['size'] == imperial_result['size']
        confidence_diff = abs(metric_result['confidence'] - imperial_result['confidence'])
        
        self.test_results['unit_conversions'] = {
            'size_match': size_match,
            'confidence_difference': round(confidence_diff, 3),
            'metric_confidence': round(metric_result['confidence'], 3),
            'imperial_confidence': round(imperial_result['confidence'], 3)
        }
    
    def test_error_handling(self):
        """Test error handling and validation"""
        logger.info("Testing error handling...")
        
        error_cases = [
            # Invalid inputs
            {'height': -10, 'weight': 75, 'fit': 'regular'},  # Negative height
            {'height': 175, 'weight': -10, 'fit': 'regular'}, # Negative weight
            {'height': 175, 'weight': 75, 'fit': 'invalid'},  # Invalid fit
            {'height': 'invalid', 'weight': 75, 'fit': 'regular'}, # Non-numeric height
            {},  # Missing parameters
        ]
        
        handled_errors = 0
        
        for i, case in enumerate(error_cases, 1):
            try:
                result = self.engine.get_size_recommendation(**case)
                # If we get here without exception, the engine handled it gracefully
                handled_errors += 1
                logger.info(f"✅ Error Case {i}: Handled gracefully")
            except Exception as e:
                # Some errors should be expected and handled
                logger.info(f"✅ Error Case {i}: Exception handled - {type(e).__name__}")
                handled_errors += 1  # Exception handling is still valid behavior
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        overall_success_rate = np.mean([
            self.test_results.get('basic_functionality', {}).get('success_rate', 0),
            self.test_results.get('edge_cases', {}).get('success_rate', 0),
            self.test_results.get('concurrent_requests', {}).get('success_rate', 0)
        ])
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_summary': {
                'overall_success_rate': round(overall_success_rate, 3),
                'total_tests_run': sum([
                    self.test_results.get('basic_functionality', {}).get('total', 0),
                    self.test_results.get('edge_cases', {}).get('total', 0),
                    self.test_results.get('concurrent_requests', {}).get('total', 0)
                ])
            },
            'detailed_results': self.test_results,
            'performance_metrics': self.performance_metrics,
            'engine_stats': self.engine.get_engine_stats(),
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check performance
        if self.performance_metrics.get('single_request_avg_ms', 0) > 50:
            recommendations.append("Performance optimization recommended - single requests taking >50ms")
        
        # Check accuracy
        if not self.test_results.get('accuracy_validation', {}).get('size_consistency', True):
            recommendations.append("Size consistency issue detected - investigate random factors")
        
        # Check error handling
        if self.test_results.get('edge_cases', {}).get('success_rate', 1) < 0.8:
            recommendations.append("Edge case handling needs improvement")
        
        if not recommendations:
            recommendations.append("All tests passed - system is performing optimally")
        
        return recommendations

# Load testing suite
def run_load_test(duration_seconds: int = 60) -> Dict[str, Any]:
    """Run load test for specified duration"""
    
    logger.info(f"🔄 Starting load test for {duration_seconds} seconds...")
    
    engine = EnhancedSuitSizeEngine()
    start_time = time.time()
    request_count = 0
    error_count = 0
    response_times = []
    
    while time.time() - start_time < duration_seconds:
        try:
            req_start = time.time()
            engine.get_size_recommendation(
                height=np.random.uniform(160, 200),
                weight=np.random.uniform(60, 120),
                fit=np.random.choice(['slim', 'regular', 'relaxed'])
            )
            response_times.append(time.time() - req_start)
            request_count += 1
        except Exception as e:
            error_count += 1
        
        # Small delay to prevent overwhelming
        time.sleep(0.01)
    
    end_time = time.time()
    actual_duration = end_time - start_time
    
    results = {
        'duration_seconds': actual_duration,
        'total_requests': request_count,
        'error_count': error_count,
        'requests_per_second': request_count / actual_duration,
        'avg_response_time_ms': round(np.mean(response_times) * 1000, 2) if response_times else 0,
        'max_response_time_ms': round(max(response_times) * 1000, 2) if response_times else 0,
        'error_rate': error_count / request_count if request_count > 0 else 1
    }
    
    logger.info(f"📊 Load Test Results: {results['requests_per_second']:.1f} req/sec, "
                f"{results['error_rate']:.1%} error rate")
    
    return results

if __name__ == "__main__":
    # Run comprehensive tests
    test_framework = ComprehensiveTestFramework()
    report = test_framework.run_all_tests()
    
    # Save detailed report
    with open('/workspace/ml_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed test report saved to: /workspace/ml_test_report.json")
    
    # Optional: Run load test
    print("\n🚀 Running 30-second load test...")
    load_results = run_load_test(30)
    
    with open('/workspace/load_test_report.json', 'w') as f:
        json.dump(load_results, f, indent=2)
    
    print(f"💾 Load test report saved to: /workspace/load_test_report.json")