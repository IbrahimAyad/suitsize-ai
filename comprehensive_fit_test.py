#!/usr/bin/env python3

import requests
import json
import time

def test_api_fit_type(fit_type_value):
    """Test a single fit type value"""
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    data = {
        "height": "175cm",
        "weight": "75kg",
        "fit_type": fit_type_value
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        return {
            'fit_type': fit_type_value,
            'status_code': response.status_code,
            'response_body': response.text,
            'response_time': response.elapsed.total_seconds(),
            'success': True
        }
    except Exception as e:
        return {
            'fit_type': fit_type_value,
            'error': str(e),
            'success': False
        }

# Test the identified fit types
test_cases = [
    # Primary fit types from UI
    "slim",
    "regular", 
    "relaxed",
    
    # Case variations
    "Slim",
    "SLIM",
    "Regular",
    "RELAXED",
    
    # Alternative naming
    "classic",
    "roomy",
    "tight",
    "loose",
    
    # Additional requested types
    "modern",
    "tailored",
    
    # Edge cases
    "custom",
    "",
    None
]

print("=== Fit Type API Testing ===")
print("Testing endpoint: https://suitsize-ai-production.up.railway.app/api/recommend")
print("Test data: height=175cm, weight=75kg")
print("")

results = []

for i, fit_type in enumerate(test_cases, 1):
    print(f"Test {i:2d}: fit_type='{fit_type}'")
    
    result = test_api_fit_type(fit_type)
    results.append(result)
    
    if result['success']:
        status = result['status_code']
        if status == 200:
            print(f"          ✅ SUCCESS (200) - {result['response_time']:.3f}s")
            print(f"          Response: {result['response_body'][:80]}...")
        elif status == 400:
            print(f"          ⚠️  VALIDATION ERROR (400) - {result['response_time']:.3f}s")
            print(f"          Error: {result['response_body']}")
        elif status == 500:
            print(f"          ❌ SERVER ERROR (500) - {result['response_time']:.3f}s")
            print(f"          Error: {result['response_body']}")
        else:
            print(f"          ❓ UNEXPECTED ({status}) - {result['response_time']:.3f}s")
            print(f"          Response: {result['response_body']}")
    else:
        print(f"          💥 EXCEPTION: {result['error']}")
    
    print("")
    time.sleep(0.5)  # Small delay

# Summary
print("=== SUMMARY ===")

successful = [r for r in results if r.get('success') and r.get('status_code') == 200]
validation_errors = [r for r in results if r.get('success') and r.get('status_code') == 400]
server_errors = [r for r in results if r.get('success') and r.get('status_code') == 500]

print(f"ACCEPTED (200): {len(successful)} fit types")
for r in successful:
    print(f"  ✅ '{r['fit_type']}'")

print(f"\nVALIDATION ERRORS (400): {len(validation_errors)} fit types")
for r in validation_errors:
    print(f"  ⚠️  '{r['fit_type']}' - {r['response_body']}")

print(f"\nSERVER ERRORS (500): {len(server_errors)} fit types")
for r in server_errors:
    print(f"  ❌ '{r['fit_type']}' - {r['response_body']}")

# Write results to file
with open('/workspace/fit_type_test_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nDetailed results saved to: fit_type_test_results.json")
print("=== Test Complete ===")