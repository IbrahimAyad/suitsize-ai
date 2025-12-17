#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_fit_types():
    """Test different fit types to understand API acceptance criteria"""
    
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    
    # Standard test data with varying fit_types
    test_data = {
        "height": "175cm",
        "weight": "75kg",
        "fit_type": None  # Will be set for each test
    }
    
    # Fit types to test
    fit_types_to_test = [
        "slim",
        "classic", 
        "loose",
        "tailored",
        "modern",
        "regular",  # From previous successful tests
        "relaxed",  # From previous concurrent test
        "custom",   # From previous boundary tests
        "tight",    # Edge case
        "extra-tight",  # Edge case
        "extra-loose",  # Edge case
        "",  # Empty string
        None,  # Null
        123,  # Number
        "Slim",  # Case sensitivity test
        "SLIM",  # Upper case
        "Regular",  # Mixed case
        "random_value"  # Invalid value
    ]
    
    headers = {"Content-Type": "application/json"}
    
    print("=== Fit Type Validation Test ===")
    print(f"Starting at: {datetime.now()}")
    print(f"URL: {url}")
    print(f"Base Data: height=175cm, weight=75kg")
    print("")
    
    results = []
    
    for i, fit_type in enumerate(fit_types_to_test, 1):
        test_case = test_data.copy()
        test_case["fit_type"] = fit_type
        
        print(f"Test {i:2d}: Testing fit_type='{fit_type}'")
        
        start_time = datetime.now()
        
        try:
            response = requests.post(url, headers=headers, json=test_case, timeout=30)
            end_time = datetime.now()
            
            result = {
                'test_number': i,
                'fit_type': fit_type,
                'success': True,
                'status_code': response.status_code,
                'response_time': (end_time - start_time).total_seconds(),
                'response_headers': dict(response.headers),
                'response_body': response.text,
                'test_data': test_case
            }
            
            # Analyze response
            if response.status_code == 200:
                print(f"          ✅ SUCCESS (200) - {result['response_time']:.3f}s")
                print(f"          Response: {response.text[:100]}...")
            elif response.status_code == 400:
                print(f"          ⚠️  VALIDATION ERROR (400) - {result['response_time']:.3f}s")
                print(f"          Error: {response.text}")
            elif response.status_code == 500:
                print(f"          ❌ SERVER ERROR (500) - {result['response_time']:.3f}s")
                print(f"          Error: {response.text}")
            else:
                print(f"          ❓ UNEXPECTED ({response.status_code}) - {result['response_time']:.3f}s")
                print(f"          Response: {response.text}")
                
        except Exception as e:
            end_time = datetime.now()
            result = {
                'test_number': i,
                'fit_type': fit_type,
                'success': False,
                'error': str(e),
                'response_time': (end_time - start_time).total_seconds(),
                'test_data': test_case
            }
            print(f"          💥 EXCEPTION - {result['response_time']:.3f}s")
            print(f"          Error: {e}")
        
        results.append(result)
        print("")
    
    # Analysis
    print("=== Analysis Summary ===")
    
    successful = [r for r in results if r.get('success') and r.get('status_code') == 200]
    validation_errors = [r for r in results if r.get('success') and r.get('status_code') == 400]
    server_errors = [r for r in results if r.get('success') and r.get('status_code') == 500]
    exceptions = [r for r in results if not r.get('success')]
    
    print(f"Successful (200): {len(successful)} cases")
    for r in successful:
        print(f"  ✅ '{r['fit_type']}'")
    
    print(f"\nValidation Errors (400): {len(validation_errors)} cases")
    for r in validation_errors:
        print(f"  ⚠️  '{r['fit_type']}' - {r['response_body']}")
    
    print(f"\nServer Errors (500): {len(server_errors)} cases")
    for r in server_errors:
        print(f"  ❌ '{r['fit_type']}' - {r['response_body']}")
    
    print(f"\nExceptions: {len(exceptions)} cases")
    for r in exceptions:
        print(f"  💥 '{r['fit_type']}' - {r['error']}")
    
    # Pattern Analysis
    print(f"\n=== Pattern Analysis ===")
    
    accepted_types = [r['fit_type'] for r in successful]
    rejected_types = [r['fit_type'] for r in validation_errors + server_errors]
    
    print(f"ACCEPTED fit types: {accepted_types}")
    print(f"REJECTED fit types: {rejected_types}")
    
    # Check for patterns
    if "slim" in accepted_types:
        print("✅ 'slim' is accepted")
    if "regular" in accepted_types:
        print("✅ 'regular' is accepted")
    if "relaxed" in accepted_types:
        print("✅ 'relaxed' is accepted")
    
    if any("tight" in str(ft).lower() for ft in rejected_types):
        print("⚠️  'tight' variations may be rejected")
    
    print(f"\n=== Conclusions ===")
    print(f"Total tests: {len(results)}")
    print(f"Success rate: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.1f}%)")
    
    return results

if __name__ == "__main__":
    results = test_fit_types()