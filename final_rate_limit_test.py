#!/usr/bin/env python3

import requests
import time
from datetime import datetime
import json

def test_rate_limiting():
    """Test rate limiting with 15 consecutive requests"""
    
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    
    # Test data
    data = {"height": "175cm", "weight": "75kg", "fit_type": "regular"}
    headers = {"Content-Type": "application/json"}
    
    print("=== Rate Limiting Test ===")
    print(f"Starting at: {datetime.now()}")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data)}")
    print(f"Requests: 15 consecutive")
    print("")
    
    results = []
    
    for i in range(1, 16):
        start_time = time.time()
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            end_time = time.time()
            
            result = {
                'request_number': i,
                'success': True,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'response_headers': dict(response.headers),
                'response_body': response.text
            }
            
            # Check for rate limiting indicators
            rate_limit_headers = {
                'X-RateLimit-Limit': response.headers.get('X-RateLimit-Limit'),
                'X-RateLimit-Remaining': response.headers.get('X-RateLimit-Remaining'),
                'X-RateLimit-Reset': response.headers.get('X-RateLimit-Reset'),
                'Retry-After': response.headers.get('Retry-After')
            }
            
            if response.status_code == 429:
                print(f"Request {i}: 🚫 RATE LIMITED - {response.status_code}")
                print(f"  Retry-After: {rate_limit_headers['Retry-After']}")
            elif any(rate_limit_headers.values()):
                print(f"Request {i}: 📊 Rate limit headers detected")
                for key, value in rate_limit_headers.items():
                    if value:
                        print(f"    {key}: {value}")
            else:
                print(f"Request {i}: ✅ {response.status_code} - {result['response_time']:.3f}s")
                
        except Exception as e:
            end_time = time.time()
            result = {
                'request_number': i,
                'success': False,
                'error': str(e),
                'response_time': end_time - start_time
            }
            print(f"Request {i}: ❌ ERROR - {e}")
        
        results.append(result)
        time.sleep(0.5)  # Small delay between requests
    
    print("\n=== Analysis ===")
    
    # Successful requests
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]
    
    print(f"Successful: {len(successful)}/15")
    print(f"Failed: {len(failed)}/15")
    
    # Status code distribution
    if successful:
        status_codes = {}
        for result in successful:
            code = result['status_code']
            status_codes[code] = status_codes.get(code, 0) + 1
        
        print("Status codes:")
        for code, count in status_codes.items():
            print(f"  {code}: {count} requests")
    
    # Response times
    if successful:
        response_times = [r['response_time'] for r in successful]
        print(f"Response time stats:")
        print(f"  Average: {sum(response_times)/len(response_times):.3f}s")
        print(f"  Min: {min(response_times):.3f}s")
        print(f"  Max: {max(response_times):.3f}s")
    
    # Rate limiting detection
    rate_limited = [r for r in results if r.get('status_code') == 429]
    if rate_limited:
        print(f"🚫 Rate limiting detected: {len(rate_limited)} requests blocked")
    else:
        print("✅ No rate limiting detected")
    
    return results

if __name__ == "__main__":
    test_rate_limiting()