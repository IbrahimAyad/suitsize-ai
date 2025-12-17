#!/usr/bin/env python3

import requests
import time
import threading
from datetime import datetime
import json

def make_concurrent_request(request_id, data, url):
    """Make a single request and record timing"""
    start_time = time.time()
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        end_time = time.time()
        
        return {
            'request_id': request_id,
            'success': True,
            'status_code': response.status_code,
            'response_time': end_time - start_time,
            'response_headers': dict(response.headers),
            'response_body': response.text,
            'request_data': data
        }
    except Exception as e:
        end_time = time.time()
        return {
            'request_id': request_id,
            'success': False,
            'error': str(e),
            'response_time': end_time - start_time,
            'request_data': data
        }

def test_concurrent_requests():
    """Test API with 3 concurrent requests"""
    
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    
    # Test data for each "tab"
    tab_requests = [
        {
            'request_id': 'Tab 1',
            'data': {"height": "160cm", "weight": "60kg", "fit_type": "slim"}
        },
        {
            'request_id': 'Tab 2', 
            'data': {"height": "180cm", "weight": "90kg", "fit_type": "regular"}
        },
        {
            'request_id': 'Tab 3',
            'data': {"height": "190cm", "weight": "110kg", "fit_type": "relaxed"}
        }
    ]
    
    print("=== Concurrent Requests Test ===")
    print(f"Starting at: {datetime.now()}")
    print(f"Testing URL: {url}")
    print("")
    
    # Create threads for concurrent requests
    threads = []
    results = []
    
    for tab_request in tab_requests:
        thread = threading.Thread(
            target=lambda r=tab_request: results.append(make_concurrent_request(
                r['request_id'], r['data'], url
            ))
        )
        threads.append(thread)
    
    # Start all threads simultaneously
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    
    print(f"All requests completed in: {total_time:.3f} seconds")
    print("")
    
    # Display results
    print("=== Results Summary ===")
    for result in results:
        print(f"\n{result['request_id']}:")
        if result['success']:
            print(f"  Status: {result['status_code']}")
            print(f"  Response Time: {result['response_time']:.3f}s")
            print(f"  Response Size: {len(result['response_body'])} bytes")
            print(f"  Response: {result['response_body']}")
            print(f"  Headers: {result['response_headers']}")
        else:
            print(f"  ERROR: {result['error']}")
            print(f"  Response Time: {result['response_time']:.3f}s")
    
    # Analysis
    print("\n=== Concurrent Behavior Analysis ===")
    
    successful_results = [r for r in results if r['success']]
    failed_results = [r for r in results if not r['success']]
    
    print(f"Successful requests: {len(successful_results)}/3")
    print(f"Failed requests: {len(failed_results)}/3")
    
    if successful_results:
        response_times = [r['response_time'] for r in successful_results]
        print(f"Response times: {[f'{t:.3f}s' for t in response_times]}")
        print(f"Average response time: {sum(response_times)/len(response_times):.3f}s")
        print(f"Min response time: {min(response_times):.3f}s")
        print(f"Max response time: {max(response_times):.3f}s")
        
        # Check for race conditions or shared state issues
        status_codes = [r['status_code'] for r in successful_results]
        if len(set(status_codes)) > 1:
            print("⚠️  Different status codes received - possible race condition")
        
        # Check response consistency
        responses = [r['response_body'] for r in successful_results]
        if len(set(responses)) > 1:
            print("⚠️  Different responses received - possible shared state issues")
        else:
            print("✅ Responses are consistent")
    
    return results

if __name__ == "__main__":
    results = test_concurrent_requests()