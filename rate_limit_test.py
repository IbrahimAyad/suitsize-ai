#!/usr/bin/env python3

import requests
import time
import json
from datetime import datetime

def test_rate_limiting():
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    headers = {"Content-Type": "application/json"}
    data = {"height": "175cm", "weight": "75kg", "fit_type": "regular"}
    
    print("=== Rate Limiting Test - 10 Consecutive Requests ===")
    print(f"Using data: {data}")
    print(f"Starting test at {datetime.now()}")
    print("")
    
    results = []
    
    for i in range(1, 11):
        start_time = time.time()
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            end_time = time.time()
            
            response_time = end_time - start_time
            results.append({
                'request': i,
                'status_code': response.status_code,
                'response_time': response_time,
                'response_size': len(response.content),
                'response_body': response.text,
                'success': response.ok
            })
            
            print(f"Request {i}/10:")
            print(f"  Status: {response.status_code}")
            print(f"  Response Time: {response_time:.3f}s")
            print(f"  Response Size: {len(response.content)} bytes")
            print(f"  Response: {response.text[:100]}{'...' if len(response.text) > 100 else ''}")
            print(f"  Headers: {dict(response.headers)}")
            print("  " + "-"*50)
            print("")
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            results.append({
                'request': i,
                'error': str(e),
                'response_time': response_time,
                'success': False
            })
            
            print(f"Request {i}/10: ERROR - {e}")
            print("")
        
        # Small delay between requests to avoid overwhelming the server
        if i < 10:
            time.sleep(0.1)
    
    print(f"Test completed at {datetime.now()}")
    print("\n=== Summary ===")
    
    # Analyze results
    successful_requests = [r for r in results if r.get('success', False)]
    failed_requests = [r for r in results if not r.get('success', False)]
    
    if successful_requests:
        avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
        min_response_time = min(r['response_time'] for r in successful_requests)
        max_response_time = max(r['response_time'] for r in successful_requests)
        
        print(f"Successful requests: {len(successful_requests)}/10")
        print(f"Failed requests: {len(failed_requests)}/10")
        print(f"Average response time: {avg_response_time:.3f}s")
        print(f"Min response time: {min_response_time:.3f}s")
        print(f"Max response time: {max_response_time:.3f}s")
        
        # Check for patterns
        status_codes = [r['status_code'] for r in successful_requests]
        unique_status_codes = set(status_codes)
        
        if len(unique_status_codes) > 1:
            print(f"Multiple status codes observed: {unique_status_codes}")
        
        # Check for response time patterns
        response_times = [r['response_time'] for r in successful_requests]
        if len(response_times) > 2:
            time_diffs = [response_times[i+1] - response_times[i] for i in range(len(response_times)-1)]
            if any(abs(diff) > 0.1 for diff in time_diffs):
                print("Significant response time variations detected")
    
    else:
        print("All requests failed")
    
    # Check for rate limiting headers
    if successful_requests:
        first_response_headers = results[0].get('response_headers', {})
        rate_limit_headers = ['X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset', 'Retry-After']
        found_headers = [h for h in rate_limit_headers if h in first_response_headers]
        if found_headers:
            print(f"Rate limiting headers found: {found_headers}")
        else:
            print("No rate limiting headers detected")
    
    return results

if __name__ == "__main__":
    results = test_rate_limiting()