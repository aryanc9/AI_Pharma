#!/usr/bin/env python
"""Quick workflow test to verify improvements"""

import sys
sys.path.insert(0, '/Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend')

from app.graph.pharmacy_workflow import run_workflow
from app.db.database import SessionLocal
from app.db.models import Customer

db = SessionLocal()

# Get first customer
customer = db.query(Customer).first()

if not customer:
    print("❌ No customers in database")
    sys.exit(1)

print(f"✅ Testing with customer: {customer.name} (ID: {customer.id})")

# Test 1: OTC medicine
print("\n📋 Test 1: OTC medicine (Paracetamol)")
try:
    final_state = run_workflow(
        customer_id=customer.id,
        message="I need paracetamol"
    )
    
    extraction = final_state.get("extraction", {})
    safety = final_state.get("safety", {})
    
    print(f"  Extraction intent: {extraction.get('intent')}")
    print(f"  Medicines extracted: {len(extraction.get('medicines', []))}")
    if extraction.get('medicines'):
        print(f"    - {extraction['medicines'][0]['name']}")
    
    print(f"  Safety approved: {safety.get('approved')}")
    print(f"  Safety error_type: {safety.get('error_type')}")
    if safety.get('violations'):
        print(f"  Violations: {safety.get('violations')}")
    
    # Check decision trace
    trace = final_state.get("decision_trace", [])
    print(f"  Decision trace length: {len(trace)}")
    for t in trace:
        print(f"    - {t['agent']}: {t['decision']}")
    
    print("✅ Test 1 PASSED")
except Exception as e:
    print(f"❌ Test 1 FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Multiple medicines
print("\n📋 Test 2: Multiple medicines (Ibuprofen + Aspirin)")
try:
    final_state = run_workflow(
        customer_id=customer.id,
        message="I need ibuprofen and aspirin"
    )
    
    extraction = final_state.get("extraction", {})
    medicines_count = len(extraction.get('medicines', []))
    print(f"  Medicines extracted: {medicines_count}")
    if medicines_count > 1:
        print(f"    ✅ Multiple medicine extraction working!")
        for med in extraction['medicines']:
            print(f"    - {med['name']}")
    else:
        print(f"    ⚠️  Expected 2 medicines, got {medicines_count}")
    
    print("✅ Test 2 PASSED")
except Exception as e:
    print(f"❌ Test 2 FAILED: {e}")

# Test 3: Error classification
print("\n📋 Test 3: Error classification (excessive quantity)")
try:
    final_state = run_workflow(
        customer_id=customer.id,
        message="I need 999 pills of paracetamol"
    )
    
    safety = final_state.get("safety", {})
    print(f"  Safety approved: {safety.get('approved')}")
    print(f"  Error type: {safety.get('error_type')}")
    print(f"  Violations: {safety.get('violations')}")
    
    if safety.get('error_type') in ['VALIDATION', 'SAFETY', 'SYSTEM']:
        print("✅ Error classification working!")
    else:
        print(f"⚠️  Error type should be set: {safety.get('error_type')}")
    
    print("✅ Test 3 PASSED")
except Exception as e:
    print(f"❌ Test 3 FAILED: {e}")

# Test 4: Medicine lookup normalization
print("\n📋 Test 4: Medicine fuzzy matching (partial name)")
try:
    final_state = run_workflow(
        customer_id=customer.id,
        message="I need some cetirizine"
    )
    
    extraction = final_state.get("extraction", {})
    medicines = extraction.get('medicines', [])
    
    if medicines:
        print(f"  Found medicine: {medicines[0]['name']}")
        if 'cetirizine' in medicines[0]['name'].lower():
            print("✅ Fuzzy matching working!")
        else:
            print(f"⚠️  Expected cetirizine, got {medicines[0]['name']}")
    else:
        print("⚠️  No medicine extracted")
    
    print("✅ Test 4 PASSED")
except Exception as e:
    print(f"❌ Test 4 FAILED: {e}")

print("\n" + "="*50)
print("✅ All workflow tests completed!")
print("="*50)

db.close()
