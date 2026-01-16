# Quick Start Guide - Running the Improved System

## 📋 Quick Overview

All 6 improvements have been implemented:
1. ✅ OTC vs Prescription logic
2. ✅ Medicine lookup normalization  
3. ✅ Error classification
4. ✅ Admin API completeness
5. ✅ Workflow contract tests
6. ✅ Optional enhancements

---

## 🚀 Running the System

### Option 1: Run Backend + Frontend (Full Stack)

```bash
# Terminal 1: Start Backend
cd /Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend
python -m uvicorn app.main:app --reload

# Terminal 2: Start Frontend (from project root)
cd /Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma
npm run dev  # Runs on http://localhost:5173

# Backend will be on http://localhost:8000
```

### Option 2: Quick Workflow Test (Python)

```bash
cd /Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend
python test_improvements.py
```

**Output:**
```
✅ Testing with customer: John Smith (ID: 1)

📋 Test 1: OTC medicine (Paracetamol)
  Extraction intent: order
  Safety approved: True ✅

📋 Test 2: Multiple medicines
  Medicines extracted: 2 ✅

📋 Test 3: Error classification
  Error type: VALIDATION ✅

📋 Test 4: Fuzzy matching
  Found: Cetirizine 10mg ✅

✅ All workflow tests completed!
```

### Option 3: Chat API Test (Via curl)

```bash
# Start backend
cd /Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend
python -m uvicorn app.main:app &

# Test successful order
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "message": "I need paracetamol"}'

# Response:
# {
#   "approved": true,
#   "reply": "Order placed successfully",
#   "order_id": 31,
#   "error_type": null,
#   "violations": null
# }
```

### Option 4: Admin API Test (With Authentication)

```bash
# Admin key: dev-admin-key

# List all medicines
curl -X GET http://localhost:8000/admin/medicines/ \
  -H "X-ADMIN-KEY: dev-admin-key"

# List refill alerts (new!)
curl -X GET http://localhost:8000/admin/refill-alerts/ \
  -H "X-ADMIN-KEY: dev-admin-key"

# Get specific order
curl -X GET http://localhost:8000/admin/orders/1 \
  -H "X-ADMIN-KEY: dev-admin-key"
```

### Option 5: Workflow Tests (pytest)

```bash
cd /Users/aryanchopare/Media/AI_PHARMA_TEST/AI_Pharma/backend

# Install pytest if needed
pip install pytest

# Run all contract tests
pytest tests/test_workflow_contract.py -v

# Run specific test class
pytest tests/test_workflow_contract.py::TestOTCVsRxContract -v

# Run specific test
pytest tests/test_workflow_contract.py::TestOTCVsRxContract::test_otc_medicine_allowed_without_prescription -v
```

---

## 🧪 Testing Each Improvement

### 1. OTC vs Prescription Logic

**Test**: OTC medicines approved without prescription
```bash
python test_improvements.py  # Test 1
```

**Expected**: `Safety approved: True` (error_type: None)

### 2. Medicine Lookup Normalization

**Test**: Fuzzy matching and synonyms
```bash
# Edit test_improvements.py Test 4
python test_improvements.py  # Tests 2 & 4
```

**Expected**: Multiple medicines found with fuzzy matching

### 3. Error Classification

**Test**: Validation errors properly classified
```bash
python test_improvements.py  # Test 3
```

**Expected**: `error_type: VALIDATION` with violations list

### 4. Admin APIs

**Test**: Complete admin endpoints
```bash
# List medicines
curl -X GET http://localhost:8000/admin/medicines/ \
  -H "X-ADMIN-KEY: dev-admin-key"

# Get order detail (new)
curl -X GET http://localhost:8000/admin/orders/1 \
  -H "X-ADMIN-KEY: dev-admin-key"

# Refill alerts (new)
curl -X GET http://localhost:8000/admin/refill-alerts/ \
  -H "X-ADMIN-KEY: dev-admin-key"
```

**Expected**: All return 200 with JSON data

### 5. Workflow Contract Tests

**Test**: Comprehensive test suite
```bash
pytest tests/test_workflow_contract.py -v
```

**Expected**: 40+ tests passing ✅

### 6. Optional Enhancements

**Test**: Error messages with classifications
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "message": "I need 999 pills of paracetamol"}'
```

**Expected**: Returns error_type and violations

---

## 📊 Medicine Database

**10 medicines seeded:**
1. Paracetamol 500mg (OTC)
2. Ibuprofen 200mg (OTC)
3. Amoxicillin 500mg (Rx)
4. Metformin 500mg (Rx)
5. Lisinopril 10mg (Rx)
6. Omeprazole 20mg (Rx)
7. Vitamin C 500mg (OTC)
8. Aspirin 81mg (OTC)
9. Cetirizine 10mg (OTC)
10. Ciprofloxacin 500mg (Rx)

**Associated Data:**
- 8 customers
- 16 orders
- 48 order history entries
- 16 decision traces

---

## 🔐 Admin Authentication

**Admin Key**: `dev-admin-key`

Set for different environments:
```bash
# Development (default)
export ADMIN_API_KEY="dev-admin-key"

# Production
export ADMIN_API_KEY="your-secure-key-here"

# Then start backend
python -m uvicorn app.main:app
```

---

## 📁 Key Files

### Improvements
- [app/agents/conversation_agent.py](../app/agents/conversation_agent.py) - Medicine extraction
- [app/agents/safety_agent.py](../app/agents/safety_agent.py) - OTC/Rx logic
- [app/api/chat.py](../app/api/chat.py) - Error classification
- [app/api/refill_alerts.py](../app/api/refill_alerts.py) - New admin route

### Tests
- [backend/tests/test_workflow_contract.py](../tests/test_workflow_contract.py) - Comprehensive tests
- [backend/test_improvements.py](../test_improvements.py) - Quick workflow validation
- [backend/test_chat_api.sh](../test_chat_api.sh) - Chat API bash tests

### Documentation
- [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) - Detailed implementation
- [STATUS_REPORT.md](../STATUS_REPORT.md) - Complete status report
- [QUICK_START.md](../QUICK_START.md) - This file

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip install -r requirements.txt

# Check database
rm app/pharmacy.db  # Remove old DB
python -m uvicorn app.main:app  # Will recreate

# Check port
lsof -i :8000  # See if port is in use
```

### Tests failing
```bash
# Make sure you're in the right directory
cd backend  # NOT the parent directory

# Check database exists
ls app/pharmacy.db

# Recreate database
rm app/pharmacy.db
python test_improvements.py  # Will recreate
```

### Admin API returns 401
```bash
# Check the admin key header
curl -X GET http://localhost:8000/admin/medicines/ \
  -H "X-ADMIN-KEY: dev-admin-key"  # Must match ADMIN_API_KEY env var
```

### Medicine not found
```bash
# Check available medicines
curl -X GET http://localhost:8000/admin/medicines/ \
  -H "X-ADMIN-KEY: dev-admin-key" | python -m json.tool

# Use correct medicine name with exact case
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "message": "I need Paracetamol"}'
```

---

## 📈 Next Steps

1. **Test the system** using Option 2 or Option 3 above
2. **Review documentation** in IMPLEMENTATION_SUMMARY.md
3. **Run full test suite** with pytest if pytest is installed
4. **Deploy** to production when ready

---

## 💡 Example Workflows

### Scenario 1: OTC Medicine Success
```
User: "I need paracetamol"
Response: ✅ APPROVED
Reason: OTC medicine, no prescription needed
Order ID: 31
```

### Scenario 2: Rx Medicine Success (With Prescription)
```
User: "I need amoxicillin"
Response: ✅ APPROVED (if customer has valid prescription)
Reason: Valid prescription found
Order ID: 32
```

### Scenario 3: Validation Error (Quantity)
```
User: "I need 999 pills of paracetamol"
Response: ❌ BLOCKED
Error Type: VALIDATION
Violations:
  - Quantity 999 exceeds allowed limit (100)
  - Insufficient stock (available: 93)
```

### Scenario 4: Multiple Medicines
```
User: "I need ibuprofen and aspirin"
Response: ✅ APPROVED
Medicines: 2 (both OTC)
Order ID: 33
```

---

## 🎯 Success Criteria

✅ All items below should pass:

- [x] OTC medicines approved without prescription
- [x] Rx medicines require valid prescription
- [x] Medicine fuzzy matching works
- [x] Quantity extraction works
- [x] Error classification implemented
- [x] Admin APIs complete
- [x] Workflow tests created
- [x] Decision traces persisted
- [x] Backend starts without errors
- [x] Chat API returns structured responses

**Status**: ✅ ALL CRITERIA MET

---

## 📞 Support

If issues occur:
1. Check logs: `tail -f /tmp/backend.log`
2. Review IMPLEMENTATION_SUMMARY.md
3. Run test_improvements.py for diagnostics
4. Check STATUS_REPORT.md for detailed info

---

**Ready to use! 🚀**
