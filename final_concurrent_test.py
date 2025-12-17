#!/usr/bin/env python3

import requests
import time
import threading
from datetime import datetime
import json

def make_request(request_id, data, url):
    """Make a single request and return results"""
    start_time = time.time()
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        end_time = time.time()
        
        return {
            'id': request_id,
            'success': True,
            'status_code': response.status_code,
            'response_time': end_time - start_time,
            'response_headers': dict(response.headers),
            'response_body': response.text,
            'data': data
        }
    except Exception as e:
        end_time = time.time()
        return {
            'id': request_id,
            'success': False,
            'error': str(e),
            'response_time': end_time - start_time,
            'data': data
        }

def test_concurrent():
    """Test 3 concurrent requests (simulating 3 browser tabs)"""
    
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    
    # Different data for each "tab"
    requests_data = [
        ("Tab_1_Slim", {"height": "160cm", "weight": "60kg", "fit_type": "slim"}),
        ("Tab_2_Regular", {"height": "180cm", "weight": "90kg", "fit_type": "regular"}),
        ("Tab_3_Relaxed", {"height": "190cm", "weight": "110kg", "fit_type": "relaxed"})
    ]
    
    print("=== Concurrent Requests Test ===")
    print(f"Starting: {datetime.now()}")
    print(f"URL: {url}")
    print("Simulating 3 browser tabs making requests simultaneously...")
    print("")
    
    # Create and start threads
    threads = []
    results = []
    
    for tab_id, data in requests_data:
        thread = threading.Thread(
            target=lambda r=tab_id, d=data: results.append(make_request(r, d, url))
        )
        threads.append(thread)
    
    # Start all threads at once
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    
    print(f"All requests completed in: {total_time:.3f} seconds")
    print("")
    
    # Display individual results
    print("=== Individual Results ===")
    for result in results:
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        print(f"{result['id']}: {status}")
        
        if result['success']:
            print(f"  Status Code: {result['status_code']}")
            print(f"  Response Time: {result['response_time']:.3f}s")
            print(f"  Response Length: {len(result['response_body'])} chars")
            print(f"  Response: {result['response_body'][:100]}...")
            
            # Check for race condition indicators
            if result['status_code'] != 200:
                print(f"  ⚠️  Non-200 status code")
        else:
            print(f"  Error: {result['error']}")
            print(f"  Response Time: {result['response_time']:.3f}s")
        print("")
    
    # Analysis
    print("=== Concurrent Behavior Analysis ===")
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"Success Rate: {len(successful)}/3 ({len(successful)/3*100:.1f}%)")
    
    if successful:
        # Response time analysis
        times = [r['response_time'] for r in successful]
        print(f"Response Time Analysis:")
        print(f"  Average: {sum(times)/len(times):.3f}s")
        print(f"  Range: {min(times):.3f}s - {max(times):.3f}s")
        print(f"  Times: {[f'{t:.3f}s' for t in times]}")
        
        # Consistency check
        status_codes = [r['status_code'] for r in successful]
        responses = [r['response_body'] for r in successful]
        
        print(f"Status Code Consistency:")
        if len(set(status_codes)) == 1:
            print(f"  ✅ All requests returned same status code: {status_codes[0]}")
        else:
            print(f"  ⚠️  Different status codes: {status_codes}")
        
        print(f"Response Consistency:")
        if len(set(responses)) == 1:
            print(f"  ✅ All responses identical")
        else:
            print(f"  ⚠️  Different responses received")
            
        # Check for concurrent handling issues
        if any(r['status_code'] == 500 for r in successful):
            print(f"  ⚠️  Service errors detected - possible concurrent load issue")
    
    print(f"\nConcurrent handling: {'✅ Good' if len(successful) == 3 else '⚠️  Issues detected'}")
    
    return results

if __name__ == "__main__":
    results = test_concurrent()