import requests
import time

url = "https://suitsize-ai-production.up.railway.app/api/recommend"
headers = {"Content-Type": "application/json"}
data = {"height": "175cm", "weight": "75kg", "fit_type": "regular"}

print("=== Rate Limiting Test - 10 Consecutive Requests ===")

for i in range(1, 11):
    start = time.time()
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        end = time.time()
        print(f"Request {i}/10: Status={response.status_code}, Time={end-start:.3f}s")
        if i <= 3:  # Show first few responses in detail
            print(f"  Response: {response.text}")
        print("  " + "-"*40)
    except Exception as e:
        print(f"Request {i}/10: ERROR - {e}")
    
    if i < 10:
        time.sleep(0.1)

print("Test completed")

# Analysis
print("\n=== Analysis ===")
print("Check for:")
print("- Consistent response times")
print("- Rate limiting headers (X-RateLimit-*)")
print("- Status code changes")
print("- Retry-After headers")