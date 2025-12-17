#!/usr/bin/env python3

# Simple test to determine fit type acceptance
import requests
import json

# Test the main fit types identified from UI
test_types = ["slim", "regular", "relaxed", "classic", "modern", "tailored"]

url = "https://suitsize-ai-production.up.railway.app/api/recommend"
base_data = {"height": "175cm", "weight": "75kg"}

results = []

for fit_type in test_types:
    data = base_data.copy()
    data["fit_type"] = fit_type
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = {
            "fit_type": fit_type,
            "status": response.status_code,
            "response": response.text,
            "time": response.elapsed.total_seconds()
        }
    except Exception as e:
        result = {
            "fit_type": fit_type,
            "status": "ERROR",
            "response": str(e),
            "time": 0
        }
    
    results.append(result)

# Save results
with open('/workspace/fit_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Print summary
print("Fit Type Test Results:")
for r in results:
    print(f"{r['fit_type']}: {r['status']} - {r['response'][:50]}...")

print("Results saved to fit_results.json")