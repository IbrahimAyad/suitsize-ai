#!/usr/bin/env python3

# Manual fit type testing with file output
import requests
import json

def test_fit_type(fit_type):
    url = "https://suitsize-ai-production.up.railway.app/api/recommend"
    data = {"height": "175cm", "weight": "75kg", "fit_type": fit_type}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        return {
            'fit_type': fit_type,
            'status_code': response.status_code,
            'response': response.text,
            'success': True
        }
    except Exception as e:
        return {
            'fit_type': fit_type,
            'error': str(e),
            'success': False
        }

# Test each fit type
fit_types = ["slim", "classic", "loose", "tailored", "modern", "regular", "relaxed"]
results = []

for fit_type in fit_types:
    result = test_fit_type(fit_type)
    results.append(result)

# Write results to file
with open('/workspace/fit_type_results.txt', 'w') as f:
    f.write("=== Fit Type Test Results ===\n\n")
    for result in results:
        if result['success']:
            f.write(f"fit_type='{result['fit_type']}': {result['status_code']} - {result['response']}\n")
        else:
            f.write(f"fit_type='{result['fit_type']}': ERROR - {result['error']}\n")

print("Test completed. Results written to fit_type_results.txt")