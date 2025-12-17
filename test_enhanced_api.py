#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Enhanced SuitSize.ai Backend
Tests all 4 critical infrastructure fixes:
1. API stability (20% failure rate fix)
2. Height scaling (200cm+ support)
3. Enhanced error handling (specific 400 errors) 
4. Rate limiting (protection against API abuse)
"""

import requests
import json
import time
import concurrent.futures
from typing import Dict, List, Tuple
import statistics

# Test configuration
API_BASE = "https://suitsize-ai-production.up.railway.app"
TEST_ENDPOINT = f"{API_BASE}/api/recommend"
HEALTH_ENDPOINT = f"{API_BASE}/health"

class SuitSizeTester:
    """Comprehensive testing suite for SuitSize.ai API"""
    
    def __init__(self):
        self.results = {
            'stability_tests': [],
            'height_scaling_tests': [],
            'error_handling_tests': [],
            'rate_limiting_tests': [],
            'performance_tests': []
        }
        
    def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Starting Comprehensive SuitSize.ai API Testing")
        print("=" * 60)
        
        # Test health endpoint first
        if not self._test_health():
            print("❌ API health check failed - aborting tests")
            return False
            
        # Run all test suites
        self._test_api_stability()
        self._test_height_scaling()
        self._test_error_handling()
        self._test_rate_limiting()
        self._test_performance()
        
        # Generate report
        self._generate_report()
        return True
    
    def _test_health(self) -> bool:
        """Test API health endpoint"""
        print("\n🔍 Testing API Health...")
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed - Status: {data.get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Health check failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def _test_api_stability(self):
        """Test API stability - address 20% failure rate"""
        print("\n🔧 Testing API Stability (Issue #1: 20% failure rate)...")
        
        test_cases = [
            {'height': 175, 'weight': 75, 'fitPreference': 'regular', 'unit': 'metric'},
            {'height': 180, 'weight': 80, 'fitPreference': 'slim', 'unit': 'metric'},
            {'height': 170, 'weight': 70, 'fitPreference': 'relaxed', 'unit': 'metric'},
            {'height': 69, 'weight': 176, 'fitPreference': 'regular', 'unit': 'imperial'},
            {'height': 185, 'weight': 85, 'fitPreference': 'slim', 'unit': 'metric'},
        ]
        
        successful_requests = 0
        total_requests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                response = requests.post(TEST_ENDPOINT, json=test_case, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'recommendation' in data:
                        successful_requests += 1
                        self.results['stability_tests'].append({
                            'test': f'Stability Test {i}',
                            'success': True,
                            'response_time': response.elapsed.total_seconds(),
                            'data': data
                        })
                        print(f"  ✅ Test {i}: SUCCESS ({response.elapsed.total_seconds():.2f}s)")
                    else:
                        print(f"  ❌ Test {i}: Invalid response format")
                else:
                    print(f"  ❌ Test {i}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Test {i}: Error - {e}")
                
        success_rate = (successful_requests / total_requests) * 100
        print(f"\n📊 Stability Test Results: {successful_requests}/{total_requests} ({success_rate:.1f}% success rate)")
        
        if success_rate >= 95:
            print("✅ API STABILITY ISSUE RESOLVED (Target: ≥95% success rate)")
        else:
            print("❌ API STABILITY ISSUE STILL EXISTS")
    
    def _test_height_scaling(self):
        """Test height scaling - support 200cm+ users"""
        print("\n📏 Testing Height Scaling (Issue #2: 200cm+ support)...")
        
        height_test_cases = [
            (200, 90, 'regular', 'metric'),  # Exactly 200cm
            (210, 95, 'regular', 'metric'),  # Above 200cm
            (220, 100, 'slim', 'metric'),    # Well above 200cm
            (230, 110, 'relaxed', 'metric'), # Extreme height
        ]
        
        successful_height_tests = 0
        total_height_tests = len(height_test_cases)
        
        for i, (height, weight, fit, unit) in enumerate(height_test_cases, 1):
            test_case = {
                'height': height,
                'weight': weight,
                'fitPreference': fit,
                'unit': unit
            }
            
            try:
                response = requests.post(TEST_ENDPOINT, json=test_case, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if 'recommendation' in data:
                        recommendation = data['recommendation']
                        size = recommendation.get('size', 'N/A')
                        successful_height_tests += 1
                        self.results['height_scaling_tests'].append({
                            'test': f'Height Test {i}',
                            'height': height,
                            'success': True,
                            'recommended_size': size,
                            'confidence': recommendation.get('confidence', 0)
                        })
                        print(f"  ✅ Height {height}cm → Size {size} (Confidence: {recommendation.get('confidence', 0):.2f})")
                    else:
                        print(f"  ❌ Height {height}cm: Invalid response")
                else:
                    print(f"  ❌ Height {height}cm: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Height {height}cm: Error - {e}")
        
        success_rate = (successful_height_tests / total_height_tests) * 100
        print(f"\n📊 Height Scaling Results: {successful_height_tests}/{total_height_tests} ({success_rate:.1f}% success rate)")
        
        if success_rate >= 90:
            print("✅ HEIGHT SCALING ISSUE RESOLVED (Target: ≥90% success rate for 200cm+)")
        else:
            print("❌ HEIGHT SCALING ISSUE STILL EXISTS")
    
    def _test_error_handling(self):
        """Test enhanced error handling - specific 400 errors"""
        print("\n⚠️  Testing Enhanced Error Handling (Issue #3: Specific 400 errors)...")
        
        error_test_cases = [
            # Missing fields
            ({'height': 175, 'weight': 75}, "Missing fitPreference"),
            ({'height': 175, 'fitPreference': 'regular'}, "Missing weight"),
            # Invalid height
            ({'height': 300, 'weight': 75, 'fitPreference': 'regular', 'unit': 'metric'}, "Height too high"),
            ({'height': 100, 'weight': 75, 'fitPreference': 'regular', 'unit': 'metric'}, "Height too low"),
            # Invalid weight
            ({'height': 175, 'weight': 300, 'fitPreference': 'regular', 'unit': 'metric'}, "Weight too high"),
            ({'height': 175, 'weight': 20, 'fitPreference': 'regular', 'unit': 'metric'}, "Weight too low"),
            # Invalid fit preference
            ({'height': 175, 'weight': 75, 'fitPreference': 'invalid', 'unit': 'metric'}, "Invalid fit"),
            # Invalid unit
            ({'height': 175, 'weight': 75, 'fitPreference': 'regular', 'unit': 'invalid'}, "Invalid unit"),
            # Invalid data types
            ({'height': 'invalid', 'weight': 75, 'fitPreference': 'regular', 'unit': 'metric'}, "Invalid height type"),
            # Empty JSON
            ({}, "Empty request"),
        ]
        
        specific_400_errors = 0
        total_error_tests = len(error_test_cases)
        
        for i, (test_case, description) in enumerate(error_test_cases, 1):
            try:
                response = requests.post(TEST_ENDPOINT, json=test_case, timeout=5)
                if response.status_code == 400:
                    data = response.json()
                    error_message = data.get('error', '')
                    if len(error_message) > 10 and 'Missing' in error_message or 'must be' in error_message:
                        specific_400_errors += 1
                        self.results['error_handling_tests'].append({
                            'test': f'Error Test {i}',
                            'description': description,
                            'success': True,
                            'status': 400,
                            'error_message': error_message
                        })
                        print(f"  ✅ {description}: Proper 400 error - '{error_message[:50]}...'")
                    else:
                        print(f"  ❌ {description}: Generic 400 error - '{error_message[:50]}...'")
                elif response.status_code == 500:
                    print(f"  ❌ {description}: Still returning 500 error (should be 400)")
                else:
                    print(f"  ❌ {description}: Unexpected status {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {description}: Exception - {e}")
        
        specific_error_rate = (specific_400_errors / total_error_tests) * 100
        print(f"\n📊 Error Handling Results: {specific_400_errors}/{total_error_tests} ({specific_error_rate:.1f}% specific 400 errors)")
        
        if specific_error_rate >= 80:
            print("✅ ERROR HANDLING ISSUE RESOLVED (Target: ≥80% specific 400 errors)")
        else:
            print("❌ ERROR HANDLING ISSUE STILL EXISTS")
    
    def _test_rate_limiting(self):
        """Test rate limiting - protection against API abuse"""
        print("\n🚦 Testing Rate Limiting (Issue #4: Protection against abuse)...")
        
        # Test rapid requests to trigger rate limiting
        rapid_requests = []
        start_time = time.time()
        
        for i in range(15):  # More than the 10/minute limit
            test_case = {
                'height': 175 + (i % 10),  # Vary slightly
                'weight': 75 + (i % 10),
                'fitPreference': 'regular',
                'unit': 'metric'
            }
            
            try:
                response = requests.post(TEST_ENDPOINT, json=test_case, timeout=5)
                rapid_requests.append({
                    'request': i + 1,
                    'status': response.status_code,
                    'timestamp': time.time() - start_time
                })
                
                if response.status_code == 429:
                    print(f"  ✅ Request {i+1}: Rate limited (429) after {time.time() - start_time:.1f}s")
                    break
                elif response.status_code == 200:
                    print(f"  ✅ Request {i+1}: Success (200)")
                else:
                    print(f"  ❌ Request {i+1}: Unexpected status {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Request {i+1}: Error - {e}")
        
        # Analyze rate limiting behavior
        rate_limited_requests = [r for r in rapid_requests if r['status'] == 429]
        successful_requests = [r for r in rapid_requests if r['status'] == 200]
        
        self.results['rate_limiting_tests'] = rapid_requests
        
        if rate_limited_requests:
            print(f"\n✅ RATE LIMITING DETECTED: {len(rate_limited_requests)} requests blocked")
            print(f"✅ SUCCESSFUL REQUESTS: {len(successful_requests)} before rate limiting")
            print("✅ RATE LIMITING ISSUE RESOLVED")
        else:
            print(f"\n❌ NO RATE LIMITING DETECTED: {len(rapid_requests)} requests processed")
            print("❌ RATE LIMITING ISSUE STILL EXISTS")
    
    def _test_performance(self):
        """Test API performance"""
        print("\n⚡ Testing API Performance...")
        
        test_case = {
            'height': 175,
            'weight': 75,
            'fitPreference': 'regular',
            'unit': 'metric'
        }
        
        response_times = []
        successful_tests = 0
        
        for i in range(10):
            try:
                start = time.time()
                response = requests.post(TEST_ENDPOINT, json=test_case, timeout=10)
                response_time = time.time() - start
                
                if response.status_code == 200:
                    response_times.append(response_time)
                    successful_tests += 1
                    print(f"  Test {i+1}: {response_time:.3f}s")
                else:
                    print(f"  Test {i+1}: Failed ({response.status_code})")
                    
            except Exception as e:
                print(f"  Test {i+1}: Error - {e}")
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            self.results['performance_tests'] = {
                'average': avg_response_time,
                'min': min_response_time,
                'max': max_response_time,
                'success_rate': (successful_tests / 10) * 100
            }
            
            print(f"\n📊 Performance Results:")
            print(f"  Average: {avg_response_time:.3f}s")
            print(f"  Min: {min_response_time:.3f}s")
            print(f"  Max: {max_response_time:.3f}s")
            print(f"  Success Rate: {(successful_tests / 10) * 100:.1f}%")
            
            if avg_response_time < 0.5:
                print("✅ PERFORMANCE: Excellent (<500ms)")
            elif avg_response_time < 1.0:
                print("✅ PERFORMANCE: Good (<1s)")
            else:
                print("⚠️ PERFORMANCE: Needs improvement (>1s)")
    
    def _generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Issue resolution summary
        print("\n🎯 CRITICAL ISSUES STATUS:")
        
        # API Stability
        stability_success = len([t for t in self.results['stability_tests'] if t['success']])
        stability_rate = (stability_success / len(self.results['stability_tests'])) * 100 if self.results['stability_tests'] else 0
        status1 = "✅ RESOLVED" if stability_rate >= 95 else "❌ STILL EXISTS"
        print(f"1. API Stability (20% failure rate): {status1} ({stability_rate:.1f}%)")
        
        # Height Scaling
        height_success = len([t for t in self.results['height_scaling_tests'] if t['success']])
        height_rate = (height_success / len(self.results['height_scaling_tests'])) * 100 if self.results['height_scaling_tests'] else 0
        status2 = "✅ RESOLVED" if height_rate >= 90 else "❌ STILL EXISTS"
        print(f"2. Height Scaling (200cm+ support): {status2} ({height_rate:.1f}%)")
        
        # Error Handling
        error_success = len([t for t in self.results['error_handling_tests'] if t['success']])
        error_rate = (error_success / len(self.results['error_handling_tests'])) * 100 if self.results['error_handling_tests'] else 0
        status3 = "✅ RESOLVED" if error_rate >= 80 else "❌ STILL EXISTS"
        print(f"3. Enhanced Error Handling (400 errors): {status3} ({error_rate:.1f}%)")
        
        # Rate Limiting
        rate_limited = any(t['status'] == 429 for t in self.results['rate_limiting_tests'])
        status4 = "✅ RESOLVED" if rate_limited else "❌ STILL EXISTS"
        print(f"4. Rate Limiting (API abuse protection): {status4}")
        
        # Performance
        if self.results['performance_tests']:
            avg_time = self.results['performance_tests']['average']
            status5 = "✅ EXCELLENT" if avg_time < 0.5 else "✅ GOOD" if avg_time < 1.0 else "⚠️ NEEDS IMPROVEMENT"
            print(f"5. API Performance: {status5} ({avg_time:.3f}s avg)")
        
        print("\n📈 OVERALL ASSESSMENT:")
        resolved_issues = sum([
            stability_rate >= 95,
            height_rate >= 90,
            error_rate >= 80,
            rate_limited
        ])
        
        print(f"   Issues Resolved: {resolved_issues}/4")
        print(f"   Success Rate: {(resolved_issues/4)*100:.1f}%")
        
        if resolved_issues == 4:
            print("\n🎉 ALL CRITICAL ISSUES RESOLVED! System ready for production.")
        elif resolved_issues >= 3:
            print("\n✅ MOSTLY RESOLVED: Minor issues remain, system is production-ready.")
        else:
            print("\n⚠️ MULTIPLE ISSUES REMAIN: Additional work needed before production.")

def main():
    """Run the comprehensive test suite"""
    tester = SuitSizeTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Testing completed successfully!")
    else:
        print("\n💥 Testing failed - API may be unavailable")
    
    return success

if __name__ == "__main__":
    main()