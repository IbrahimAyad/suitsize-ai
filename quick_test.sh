#!/bin/bash
# Quick Deployment Verification Script
# Tests all 4 critical fixes after Railway deployment

echo "🚀 SuitSize.ai Deployment Verification"
echo "======================================"

API_BASE="https://suitsize-ai-production.up.railway.app"
TEST_ENDPOINT="$API_BASE/api/recommend"

echo ""
echo "🧪 Testing All 4 Critical Fixes..."
echo ""

# Test 1: Basic API Stability
echo "1️⃣ Testing API Stability (20% failure rate fix)..."
RESPONSE1=$(curl -s -w "%{http_code}" -X POST "$TEST_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"height": 175, "weight": 75, "fitPreference": "regular", "unit": "metric"}')

if [[ $RESPONSE1 == *"200"* ]]; then
  echo "   ✅ SUCCESS: API is responding"
else
  echo "   ❌ FAILED: API still failing"
fi

# Test 2: Height Scaling (200cm+ support)
echo ""
echo "2️⃣ Testing Height Scaling (200cm+ support)..."
RESPONSE2=$(curl -s -w "%{http_code}" -X POST "$TEST_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"height": 210, "weight": 95, "fitPreference": "regular", "unit": "metric"}')

if [[ $RESPONSE2 == *"200"* ]]; then
  echo "   ✅ SUCCESS: Height scaling works"
else
  echo "   ❌ FAILED: Height scaling still broken"
fi

# Test 3: Enhanced Error Handling (400 errors)
echo ""
echo "3️⃣ Testing Error Handling (specific 400 errors)..."
RESPONSE3=$(curl -s -w "%{http_code}" -X POST "$TEST_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"height": 175, "weight": 75}')  # Missing fitPreference

if [[ $RESPONSE3 == *"400"* ]]; then
  echo "   ✅ SUCCESS: Specific 400 error handling works"
else
  echo "   ❌ FAILED: Still returning generic errors"
fi

# Test 4: Rate Limiting
echo ""
echo "4️⃣ Testing Rate Limiting (API abuse protection)..."
echo "   Sending 11 rapid requests..."

SUCCESS_COUNT=0
for i in {1..11}; do
  RESPONSE=$(curl -s -w "%{http_code}" -X POST "$TEST_ENDPOINT" \
    -H "Content-Type: application/json" \
    -d '{"height": 175, "weight": 75, "fitPreference": "regular", "unit": "metric"}')
  
  if [[ $RESPONSE == *"200"* ]]; then
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
  elif [[ $RESPONSE == *"429"* ]]; then
    echo "   ✅ SUCCESS: Rate limiting activated on request $i"
    break
  fi
done

if [[ $SUCCESS_COUNT -eq 11 ]]; then
  echo "   ❌ FAILED: No rate limiting detected"
else
  echo "   ✅ SUCCESS: Rate limiting is working"
fi

echo ""
echo "📊 Quick Test Summary"
echo "==================="
echo "Basic API Test: $([[ $RESPONSE1 == *"200"* ]] && echo "✅ PASS" || echo "❌ FAIL")"
echo "Height Scaling: $([[ $RESPONSE2 == *"200"* ]] && echo "✅ PASS" || echo "❌ FAIL")"  
echo "Error Handling: $([[ $RESPONSE3 == *"400"* ]] && echo "✅ PASS" || echo "❌ FAIL")"
echo "Rate Limiting: $([[ $SUCCESS_COUNT -lt 11 ]] && echo "✅ PASS" || echo "❌ FAIL")"

echo ""
echo "🎯 For detailed testing, run: python3 test_enhanced_api.py"
echo "📖 Full deployment guide: railway_deployment_guide.md"