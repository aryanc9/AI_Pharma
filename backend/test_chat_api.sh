#!/bin/bash
# Test the chat API with error classification

echo "========================================================================"
echo "CHAT API VALIDATION - Error Classification"
echo "========================================================================"

# Start the backend in background
cd /Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend started
if ! curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    cat /tmp/backend.log
    exit 1
fi

echo "✅ Backend started (PID: $BACKEND_PID)"

# Test 1: Successful OTC order
echo ""
echo "📋 Test 1: Successful OTC Order"
echo "------------------------------------------------------------------------"
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "message": "I need paracetamol"}')

echo "$RESPONSE" | python -m json.tool

# Test 2: Excessive quantity
echo ""
echo "📋 Test 2: Excessive Quantity - VALIDATION Error"
echo "------------------------------------------------------------------------"
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "message": "I need 999 pills of paracetamol"}')

echo "$RESPONSE" | python -m json.tool

# Test 3: Multiple medicines
echo ""
echo "📋 Test 3: Multiple Medicines"
echo "------------------------------------------------------------------------"
RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "message": "I need ibuprofen and aspirin"}')

echo "$RESPONSE" | python -m json.tool

# Test 4: Admin medicines endpoint
echo ""
echo "📋 Test 4: Admin Medicines Endpoint (with auth)"
echo "------------------------------------------------------------------------"
RESPONSE=$(curl -s -X GET http://127.0.0.1:8000/admin/medicines/ \
  -H "X-ADMIN-KEY: test-key-123")

echo "$RESPONSE" | python -m json.tool | head -30

# Test 5: Admin refill alerts endpoint
echo ""
echo "📋 Test 5: Admin Refill Alerts Endpoint (with auth)"
echo "------------------------------------------------------------------------"
RESPONSE=$(curl -s -X GET http://127.0.0.1:8000/admin/refill-alerts/ \
  -H "X-ADMIN-KEY: test-key-123")

echo "$RESPONSE" | python -m json.tool

# Cleanup
echo ""
echo "Cleaning up..."
kill $BACKEND_PID 2>/dev/null
wait $BACKEND_PID 2>/dev/null

echo ""
echo "========================================================================"
echo "✅ ALL CHAT API TESTS COMPLETED"
echo "========================================================================"
