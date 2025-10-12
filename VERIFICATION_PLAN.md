# Application Verification Plan

**Purpose:** Ensure the application works correctly after highlighting fixes and cleanup  
**Created:** 2025-10-12

---

## 🎯 Verification Strategy

### Pre-Change Baseline
1. Test current production state
2. Document baseline behavior
3. Create rollback points

### Post-Change Verification
1. Verify highlighting feature works
2. Ensure no regression in core features
3. Check performance metrics

---

## 📋 Phase 1: Pre-Deployment Verification

**Run BEFORE deploying highlighting fix**

### 1.1 Application Health Check

```bash
# Check if app is running
curl http://localhost:7860/api/health

# Expected response:
# {"status": "healthy", "timestamp": "...", "version": "..."}
```

### 1.2 Basic Query Test

```bash
# Test a simple query
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is a covered call?",
    "provider": "claude",
    "num_results": 5
  }' | jq '.answer' | head -20

# Expected: Should return an answer with sources
```

### 1.3 Check Server Logs

```bash
# Monitor logs for errors
docker logs <container-name> --tail 100

# Look for:
# ✅ "RAG service initialized successfully"
# ✅ "Initialized chain for claude"
# ❌ No ERROR or CRITICAL messages
```

### 1.4 Verify Core Files

```bash
# Ensure production files exist
ls -la app/services/formatters.py
ls -la app/services/rag_service.py
ls -la config.py
ls -la rag_pipeline.py

# All should exist and be readable
```

---

## 🔍 Phase 2: Post-Deployment Verification (Highlighting)

**Run AFTER deploying highlighting fix**

### 2.1 Highlighting Feature Test

#### Test 1: Query with Expected Quotes

```bash
# Query that should trigger quoting
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is PEAD?",
    "provider": "claude",
    "num_results": 5
  }' > test_response.json

# Check the response
cat test_response.json | jq '.answer' | grep -o '"[^"]*"' | head -5
```

**Expected in logs:**
```
✅ Extracted 2 quotes for highlighting:
   1. "post earnings announcement drift is a thing"
   2. "There's certain conditions that have to be met"
   ✓ Highlighted: "post earnings announcement drift is a thing"
✅ Applied 2 highlight(s) to source content
```

**Expected in response:**
```json
{
  "answer": "...mentions that \"post earnings announcement drift is a thing\"...",
  "sources": "...<mark class=\"quote-highlight\">post earnings announcement drift is a thing</mark>..."
}
```

#### Test 2: Visual Verification

1. Open the UI in browser
2. Ask: **"What is post-earnings announcement drift?"**
3. Check for:
   - ✅ AI response includes quoted phrases (in "double quotes")
   - ✅ Source snippets show yellow/blue highlighting
   - ✅ Header: "📚 Source Videos with Highlighted Quotes"
   - ✅ Highlighted text matches phrases from AI answer

#### Test 3: No Quotes Scenario

```bash
# Query that might not trigger quotes
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello",
    "provider": "claude",
    "num_results": 5
  }' > test_response2.json
```

**Expected in logs:**
```
⚠️ No quotes extracted from AI answer - highlighting will not work
```

**Expected behavior:**
- App still works normally
- No highlighting (which is fine)
- No errors or crashes

### 2.2 Check for Regressions

#### Test: Core RAG Functionality

```bash
# Multiple test queries
QUERIES=(
  "What are the Greeks in options trading?"
  "Explain implied volatility"
  "How do I manage theta decay?"
  "What is the wheel strategy?"
)

for query in "${QUERIES[@]}"; do
  echo "Testing: $query"
  curl -X POST http://localhost:7860/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$query\", \"provider\": \"claude\", \"num_results\": 5}" \
    | jq -r '.answer' | head -3
  echo "---"
done
```

**Expected:**
- ✅ All queries return answers
- ✅ Sources are included
- ✅ No 500 errors
- ✅ Response time < 10 seconds

#### Test: Source Links

```bash
# Check that video links are properly formatted
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "PEAD", "provider": "claude", "num_results": 3}' \
  | jq '.raw_sources[0]'

# Verify:
# - video_url exists
# - video_url_with_timestamp exists
# - timestamp is valid
# - content is not empty
```

### 2.3 Performance Check

```bash
# Test response time
time curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is delta in options?", "provider": "claude", "num_results": 5}' \
  > /dev/null 2>&1

# Expected: < 10 seconds
```

---

## 🧹 Phase 3: Post-Cleanup Verification

**Run AFTER repository cleanup**

### 3.1 Application Still Starts

```bash
# Rebuild and start
docker-compose build
docker-compose up -d

# Check logs
docker-compose logs --tail 50

# Expected:
# ✅ No import errors
# ✅ "RAG service initialized successfully"
# ✅ Server starts on port 7860
```

### 3.2 All Endpoints Work

```bash
# Test each endpoint
curl http://localhost:7860/api/health
curl http://localhost:7860/
curl -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "provider": "claude", "num_results": 5}'
```

### 3.3 Essential Scripts Still Work

```bash
# Test moved scripts
python scripts/validate_system.py
python scripts/create_vector_store.py --help

# Expected: No import errors
```

### 3.4 Dependencies Intact

```bash
# Verify imports work
python -c "from app.services.formatters import ResponseFormatter; print('✅ Formatters OK')"
python -c "from app.services.rag_service import RAGService; print('✅ RAG Service OK')"
python -c "from rag_pipeline import run_rag_query; print('✅ RAG Pipeline OK')"
python -c "from config import SYSTEM_PROMPT; print('✅ Config OK')"
```

---

## 🔬 Automated Test Script

Save as `verify_application.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Running Application Verification Tests"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

FAILED=0

# Test 1: Health Check
echo -e "\n📋 Test 1: Health Check"
if curl -f -s http://localhost:7860/api/health > /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}: Health endpoint responding"
else
    echo -e "${RED}❌ FAIL${NC}: Health endpoint not responding"
    FAILED=$((FAILED + 1))
fi

# Test 2: Basic Query
echo -e "\n📋 Test 2: Basic Query"
RESPONSE=$(curl -s -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a call option?", "provider": "claude", "num_results": 3}')

if echo "$RESPONSE" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}: Query returns answer"
else
    echo -e "${RED}❌ FAIL${NC}: Query failed or malformed response"
    FAILED=$((FAILED + 1))
fi

# Test 3: Sources Included
echo -e "\n📋 Test 3: Sources Included"
if echo "$RESPONSE" | jq -e '.raw_sources[0]' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}: Sources are included"
else
    echo -e "${RED}❌ FAIL${NC}: No sources in response"
    FAILED=$((FAILED + 1))
fi

# Test 4: Video URLs Valid
echo -e "\n📋 Test 4: Video URLs"
VIDEO_URL=$(echo "$RESPONSE" | jq -r '.raw_sources[0].video_url_with_timestamp')
if [[ $VIDEO_URL == https://www.youtube.com/* ]]; then
    echo -e "${GREEN}✅ PASS${NC}: Video URL is valid"
else
    echo -e "${RED}❌ FAIL${NC}: Video URL is invalid or missing"
    FAILED=$((FAILED + 1))
fi

# Test 5: Highlighting Test
echo -e "\n📋 Test 5: Highlighting Feature"
PEAD_RESPONSE=$(curl -s -X POST http://localhost:7860/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is PEAD?", "provider": "claude", "num_results": 3}')

QUOTES=$(echo "$PEAD_RESPONSE" | jq -r '.answer' | grep -o '"[^"]*"' | wc -l)
if [ "$QUOTES" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}: AI response includes quotes ($QUOTES found)"
else
    echo -e "${YELLOW}⚠️  WARN${NC}: AI response has no quotes (may need prompt tuning)"
fi

HIGHLIGHTS=$(echo "$PEAD_RESPONSE" | jq -r '.sources' | grep -o '<mark class="quote-highlight">' | wc -l)
if [ "$HIGHLIGHTS" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}: Highlighting applied ($HIGHLIGHTS highlights)"
else
    echo -e "${YELLOW}⚠️  WARN${NC}: No highlights found (check if quotes match source)"
fi

# Summary
echo -e "\n=========================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED test(s) failed${NC}"
    exit 1
fi
```

---

## 📊 Success Criteria

### ✅ **Highlighting Feature (New)**
- [ ] AI responses include direct quotes from sources
- [ ] Transcript snippets show `<mark class="quote-highlight">` tags
- [ ] Logs show "Extracted X quotes" and "Applied X highlights"
- [ ] Visual: Yellow/blue highlighting visible in UI
- [ ] Header appears: "📚 Source Videos with Highlighted Quotes"

### ✅ **Core Functionality (Regression Check)**
- [ ] Health endpoint returns 200 OK
- [ ] Chat endpoint accepts queries
- [ ] Responses include answers and sources
- [ ] Video URLs are properly formatted
- [ ] Timestamps are included
- [ ] Response time < 10 seconds
- [ ] No Python import errors
- [ ] No 500 server errors

### ✅ **After Cleanup**
- [ ] Application builds successfully
- [ ] Application starts without errors
- [ ] All tests above still pass
- [ ] Essential scripts in `/scripts` work
- [ ] No import errors from moved files

---

## 🚨 Rollback Triggers

**Immediately rollback if:**

1. ❌ Health endpoint returns 500 or doesn't respond
2. ❌ Import errors in logs
3. ❌ Application won't start
4. ❌ Queries return 500 errors
5. ❌ Response time > 30 seconds consistently

**Consider rollback if:**

1. ⚠️ Highlighting feature doesn't work (but app works)
2. ⚠️ More than 2 tests fail
3. ⚠️ User complaints about broken features

---

## 📝 Verification Checklist

### Before Deployment
- [ ] Run `verify_application.sh` (baseline)
- [ ] Document current response times
- [ ] Tag current state: `git tag pre-deploy-$(date +%Y%m%d)`
- [ ] Backup production database if applicable

### After Highlighting Deployment
- [ ] Run `verify_application.sh`
- [ ] Test 5-10 queries manually in UI
- [ ] Check logs for quote extraction messages
- [ ] Verify highlighting visible in UI
- [ ] Compare response times to baseline

### After Cleanup
- [ ] Run `verify_application.sh`
- [ ] Rebuild Docker images
- [ ] Test production deployment
- [ ] Verify no import errors

### Final Sign-off
- [ ] All tests passing
- [ ] No errors in logs for 1 hour
- [ ] Response times acceptable
- [ ] Highlighting working (or gracefully failing)
- [ ] Team notified of changes

---

**Status:** Ready to use  
**Estimated Time:** 15-20 minutes for full verification  
**Automation Level:** High (most tests can run automatically)

