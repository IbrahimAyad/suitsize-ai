#!/usr/bin/env python3

import requests
import json
import sys
import time
from datetime import datetime

# Test specific fit types
fit_types = ["slim", "classic", "loose", "tailored", "modern", "regular"]
url = "https://suitsize-ai-production.up.railway.app/api/recommend"
headers = {"Content-Type": "application/json"}

print("=== Fit Type Testing Started ===")
print(f"Time: {datetime.now()}")
print(f"URL: {url}")
print("")

for fit_type in fit_types:
    data = {
        "height": "175cm",
        "weight": "75kg", 
        "fit_type": fit_type
    }
    
    try:
        print(f"Testing fit_type='{fit_type}'...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Response Time: {response.elapsed.total_seconds():.3f}s")
        print(f"  Response: {response.text}")
        print(f"  Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"  ✅ ACCEPTED")
        elif response.status_code == 400:
            print(f"  ⚠️  VALIDATION ERROR")
        elif response.status_code == 500:
            print(f"  ❌ SERVER ERROR")
        else:
            print(f"  ❓ UNEXPECTED STATUS")
            
    except Exception as e:
        print(f"  💥 EXCEPTION: {e}")
    
    print("")
    time.sleep(1)  # Small delay between requests

print("=== Testing Complete ===")