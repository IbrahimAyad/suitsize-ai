#!/bin/bash

echo "=== Rate Limiting Test - 10 Consecutive Requests ==="
echo "Using valid data: height=175cm, weight=75kg, fit_type=regular"
echo "Starting test at $(date)"
echo ""

for i in {1..10}; do
  echo "Request $i/10:"
  start_time=$(date +%s.%3N)
  
  response=$(curl -X POST "https://suitsize-ai-production.up.railway.app/api/recommend" \
    -H "Content-Type: application/json" \
    -d '{"height": "175cm", "weight": "75kg", "fit_type": "regular"}' \
    -w "ResponseTime:%{time_total}s|Status:%{http_code}|Size:%{size_download}bytes" \
    -s)
  
  end_time=$(date +%s.%3N)
  elapsed=$(echo "$end_time - $start_time" | bc 2>/dev/null || echo "N/A")
  
  echo "$response"
  echo "Actual elapsed time: ${elapsed}s"
  echo "-----------------------------------"
  echo ""
done

echo "Test completed at $(date)"