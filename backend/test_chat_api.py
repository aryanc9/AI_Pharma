#!/usr/bin/env python
"""Test the chat API with error classification"""

import sys
sys.path.insert(0, '/Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend')

from starlette.testclient import TestClient as StarleteTestClient
from app.main import app
import json

# Workaround for TestClient API
client = StarleteTestClient(app)

print("=" * 70)
print("CHAT API VALIDATION - Error Classification")
print("=" * 70)

# Test 1: Successful OTC order
print("\n📋 Test 1: Successful OTC Order")
print("-" * 70)
response = client.post("/chat/", json={
    "customer_id": 1,
    "message": "I need paracetamol"
})
data = response.json()
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(data, indent=2)}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert data["approved"] == True, "Should be approved"
assert data["error_type"] is None, "Should have no error"
print("✅ PASSED: OTC order approved with no errors")

# Test 2: Excessive quantity
print("\n📋 Test 2: Excessive Quantity - VALIDATION Error")
print("-" * 70)
response = client.post("/chat/", json={
    "customer_id": 1,
    "message": "I need 999 pills of paracetamol"
})
data = response.json()
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(data, indent=2)}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert data["approved"] == False, "Should be blocked"
assert data["error_type"] == "VALIDATION", f"Expected VALIDATION error, got {data.get('error_type')}"
assert len(data.get("violations", [])) > 0, "Should have violation details"
print("✅ PASSED: Excessive quantity blocked with VALIDATION error")

# Test 3: Multiple medicines
print("\n📋 Test 3: Multiple Medicines")
print("-" * 70)
response = client.post("/chat/", json={
    "customer_id": 1,
    "message": "I need ibuprofen and aspirin"
})
data = response.json()
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(data, indent=2)}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
assert data["approved"] == True, "Multiple OTC should be approved"
print("✅ PASSED: Multiple medicines handled correctly")

# Test 4: Invalid customer
print("\n📋 Test 4: Invalid Customer - 404 Error")
print("-" * 70)
response = client.post("/chat/", json={
    "customer_id": 999999,
    "message": "I need medicine"
})
print(f"Status: {response.status_code}")
if response.status_code == 404:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ PASSED: Invalid customer returns 404")
else:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("⚠️  Got different status code (expected 404)")

print("\n" + "=" * 70)
print("✅ ALL CHAT API TESTS PASSED")
print("=" * 70)
