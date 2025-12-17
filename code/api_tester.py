#!/usr/bin/env python3
"""
SuitSize.ai API Testing Script
Tests various parameter combinations and analyzes responses
"""

import requests
import json
import time
from datetime import datetime
import sys

API_ENDPOINT = "https://suitsize-ai-production.up.railway.app/api/recommend"

def test_api_call(data, description):
    """Test a single API call and return results"""
    try:
        start_time = time.time()
        response = requests.post(
            API_ENDPOINT, 
            json=data, 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        end_time = time.time()
        
        result = {
            "description": description,
            "input": data,
            "status_code": response.status_code,
            "response_time": round(end_time - start_time, 3),
            "response_text": response.text,
            "success": response.status_code == 200
        }
        
        # Try to parse JSON response
        try:
            result["response_json"] = response.json()
        except:
            result["response_json"] = None
            
        return result
        
    except Exception as e:
        return {
            "description": description,
            "input": data,
            "error": str(e),
            "success": False
        }

def main():
    """Run comprehensive API tests"""
    print("=== SuitSize.ai Railway API Analysis ===\n")
    print(f"Endpoint: {API_ENDPOINT}")
    print(f"Test started at: {datetime.now()}\n")
    
    # Test cases covering the specified ranges
    test_cases = [
        # Height 160-200cm (63-79 inches), Weight 50-120kg (110-265 lbs)
        # Fit types: slim, regular, relaxed
        
        # Baseline tests
        {"height": 69, "weight": 165, "body_type": "regular", "fit_preference": "regular", "description": "Baseline: 175cm/75kg regular"},
        {"height": 69, "weight": 165, "body_type": "regular", "fit_preference": "slim", "description": "Regular body, slim fit"},
        {"height": 69, "weight": 165, "body_type": "regular", "fit_preference": "relaxed", "description": "Regular body, relaxed fit"},
        
        # Height variations (160-200cm = 63-79 inches)
        {"height": 63, "weight": 165, "body_type": "regular", "fit_preference": "regular", "description": "Short height: 160cm"},
        {"height": 79, "weight": 165, "body_type": "regular", "fit_preference": "regular", "description": "Tall height: 200cm"},
        
        # Weight variations (50-120kg = 110-265 lbs)
        {"height": 69, "weight": 110, "body_type": "regular", "fit_preference": "regular", "description": "Low weight: 50kg"},
        {"height": 69, "weight": 265, "body_type": "regular", "fit_preference": "regular", "description": "High weight: 120kg"},
        
        # Body type variations
        {"height": 69, "weight": 165, "body_type": "slim", "fit_preference": "regular", "description": "Slim body type"},
        {"height": 69, "weight": 165, "body_type": "athletic", "fit_preference": "regular", "description": "Athletic body type"},
        {"height": 69, "weight": 165, "body_type": "broad", "fit_preference": "regular", "description": "Broad body type"},
        
        # Edge cases
        {"height": 60, "weight": 80, "body_type": "regular", "fit_preference": "regular", "description": "Very short/low weight"},
        {"height": 80, "weight": 300, "body_type": "regular", "fit_preference": "regular", "description": "Very tall/high weight"},
        
        # Invalid inputs
        {"height": "invalid", "weight": 165, "body_type": "regular", "fit_preference": "regular", "description": "Invalid height type"},
        {"height": 69, "weight": "invalid", "body_type": "regular", "fit_preference": "regular", "description": "Invalid weight type"},
        {"height": 69, "weight": 165, "body_type": "invalid", "fit_preference": "regular", "description": "Invalid body type"},
        {"height": 69, "weight": 165, "body_type": "regular", "fit_preference": "invalid", "description": "Invalid fit preference"},
        
        # Missing parameters
        {"height": 69, "weight": 165, "body_type": "regular", "description": "Missing fit preference"},
        {"height": 69, "body_type": "regular", "fit_preference": "regular", "description": "Missing weight"},
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test_case.pop('description', 'No description')}")
        
        # Extract description from test case
        description = test_case.pop('description', 'No description')
        test_case['description'] = description
        
        result = test_api_call(test_case, description)
        results.append(result)
        
        # Print immediate results
        if result.get('error'):
            print(f"  ❌ Error: {result['error']}")
        else:
            print(f"  Status: {result['status_code']} | Time: {result['response_time']}s")
            if result['success']:
                print(f"  ✅ Success")
            else:
                print(f"  ❌ Failed")
                if result.get('response_text'):
                    print(f"  Response: {result['response_text'][:100]}...")
        
        time.sleep(0.1)  # Small delay between requests
        
    # Save results to file
    with open('/workspace/docs/api_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Analysis
    print(f"\n=== ANALYSIS SUMMARY ===")
    print(f"Total tests: {len(results)}")
    print(f"Successful: {sum(1 for r in results if r.get('success', False))}")
    print(f"Failed: {sum(1 for r in results if not r.get('success', True))}")
    print(f"Average response time: {sum(r.get('response_time', 0) for r in results if 'response_time' in r) / len([r for r in results if 'response_time' in r]):.3f}s")
    
    # Check for successful responses to analyze
    successful_responses = [r for r in results if r.get('success') and r.get('response_json')]
    if successful_responses:
        print(f"\nSuccessful responses found: {len(successful_responses)}")
        
        # Analyze response patterns
        print("\n=== RESPONSE PATTERN ANALYSIS ===")
        for result in successful_responses[:5]:  # Show first 5 successful responses
            resp = result['response_json']
            print(f"\nTest: {result['description']}")
            print(f"Input: {result['input']}")
            print(f"Response structure:")
            if isinstance(resp, dict):
                for key in resp.keys():
                    print(f"  - {key}")
                if 'recommendation' in resp:
                    rec = resp['recommendation']
                    print(f"Recommendation size: {rec.get('size', 'N/A')}")
                    print(f"Confidence: {rec.get('confidence', 'N/A')}")
                    print(f"Confidence level: {rec.get('confidenceLevel', 'N/A')}")
    else:
        print("\nNo successful responses found for detailed analysis")
    
    return results

if __name__ == "__main__":
    main()
