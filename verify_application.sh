#!/bin/bash
# Application Verification Test Suite
# Tests highlighting feature and core functionality

set -e

echo "🧪 OPTEEE Application Verification Tests"
echo "=========================================="
echo ""

# Configuration
API_URL="${API_URL:-http://localhost:7860}"
PROVIDER="${PROVIDER:-claude}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

FAILED=0
WARNINGS=0

# Helper function to test endpoint
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    
    echo -e "${BLUE}📋 Test: $name${NC}"
    
    if [ "$method" = "GET" ]; then
        RESPONSE=$(curl -f -s "$API_URL$endpoint" 2>&1)
    else
        RESPONSE=$(curl -f -s -X "$method" "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>&1)
    fi
    
    local EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $name"
        echo "$RESPONSE"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}: $name"
        echo "Error: $RESPONSE"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# Test 1: Health Check
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 1: Health Check${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if curl -f -s "$API_URL/api/health" > /dev/null 2>&1; then
    HEALTH_RESPONSE=$(curl -s "$API_URL/api/health" | jq -r '.')
    echo -e "${GREEN}✅ PASS${NC}: Health endpoint responding"
    echo "$HEALTH_RESPONSE"
else
    echo -e "${RED}❌ FAIL${NC}: Health endpoint not responding"
    echo "Make sure the application is running on $API_URL"
    FAILED=$((FAILED + 1))
fi

# Test 2: Basic Query
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 2: Basic Query${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

BASIC_QUERY='{
  "query": "What is a covered call?",
  "provider": "'$PROVIDER'",
  "num_results": 3
}'

RESPONSE=$(curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "$BASIC_QUERY")

if echo "$RESPONSE" | jq -e '.answer' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}: Query returns answer"
    echo "Answer preview:"
    echo "$RESPONSE" | jq -r '.answer' | head -c 200
    echo "..."
else
    echo -e "${RED}❌ FAIL${NC}: Query failed or malformed response"
    echo "$RESPONSE"
    FAILED=$((FAILED + 1))
fi

# Test 3: Sources Included
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 3: Sources Included${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if echo "$RESPONSE" | jq -e '.raw_sources[0]' > /dev/null 2>&1; then
    SOURCE_COUNT=$(echo "$RESPONSE" | jq '.raw_sources | length')
    echo -e "${GREEN}✅ PASS${NC}: Sources are included ($SOURCE_COUNT sources)"
    echo "First source:"
    echo "$RESPONSE" | jq -r '.raw_sources[0] | {title, video_id, timestamp: .start_timestamp_seconds}'
else
    echo -e "${RED}❌ FAIL${NC}: No sources in response"
    FAILED=$((FAILED + 1))
fi

# Test 4: Video URLs Valid
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 4: Video URLs${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

VIDEO_URL=$(echo "$RESPONSE" | jq -r '.raw_sources[0].video_url_with_timestamp')
if [[ $VIDEO_URL == https://www.youtube.com/* ]]; then
    echo -e "${GREEN}✅ PASS${NC}: Video URL is valid"
    echo "URL: $VIDEO_URL"
else
    echo -e "${RED}❌ FAIL${NC}: Video URL is invalid or missing: $VIDEO_URL"
    FAILED=$((FAILED + 1))
fi

# Test 5: Highlighting Feature (NEW)
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 5: Highlighting Feature (NEW)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

PEAD_QUERY='{
  "query": "What is PEAD?",
  "provider": "'$PROVIDER'",
  "num_results": 5
}'

PEAD_RESPONSE=$(curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "$PEAD_QUERY")

# Check for quotes in AI answer
ANSWER_TEXT=$(echo "$PEAD_RESPONSE" | jq -r '.answer')
QUOTES_COUNT=$(echo "$ANSWER_TEXT" | grep -o '"[^"]\{20,\}"' | wc -l | tr -d ' ')

echo "Checking for quoted text in AI answer..."
if [ "$QUOTES_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}: AI response includes quotes ($QUOTES_COUNT quotes found)"
    echo "Sample quotes:"
    echo "$ANSWER_TEXT" | grep -o '"[^"]\{20,\}"' | head -3
else
    echo -e "${YELLOW}⚠️  WARN${NC}: AI response has no quotes"
    echo "  This means the AI didn't quote sources directly."
    echo "  Highlighting won't work without quotes."
    echo "  Consider checking system prompt or trying different LLM."
    WARNINGS=$((WARNINGS + 1))
fi

# Check for highlighting markup in sources
SOURCES_HTML=$(echo "$PEAD_RESPONSE" | jq -r '.sources')
HIGHLIGHTS_COUNT=$(echo "$SOURCES_HTML" | grep -o '<mark class="quote-highlight">' | wc -l | tr -d ' ')

echo ""
echo "Checking for highlighting in source snippets..."
if [ "$HIGHLIGHTS_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}: Highlighting applied ($HIGHLIGHTS_COUNT highlights)"
    echo "Highlighted text samples:"
    echo "$SOURCES_HTML" | grep -o '<mark class="quote-highlight">[^<]\{30,60\}' | head -2 | sed 's/<mark class="quote-highlight">/  → /'
else
    if [ "$QUOTES_COUNT" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  WARN${NC}: Quotes found but not highlighted"
        echo "  The AI quoted text, but highlighting didn't match source content."
        echo "  This can happen if AI paraphrased slightly."
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${YELLOW}⚠️  INFO${NC}: No highlights (no quotes to highlight)"
    fi
fi

# Check for highlighting header
if echo "$SOURCES_HTML" | grep -q "Source Videos with Highlighted Quotes"; then
    echo -e "${GREEN}✅ PASS${NC}: Highlighting header present"
else
    echo -e "${YELLOW}⚠️  INFO${NC}: No highlighting header (expected when no quotes)"
fi

# Test 6: Response Time
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 6: Response Time${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

START_TIME=$(date +%s)
curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is delta?", "provider": "'$PROVIDER'", "num_results": 3}' \
  > /dev/null
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $DURATION -lt 15 ]; then
    echo -e "${GREEN}✅ PASS${NC}: Response time acceptable (${DURATION}s)"
else
    echo -e "${YELLOW}⚠️  WARN${NC}: Response time slow (${DURATION}s)"
    WARNINGS=$((WARNINGS + 1))
fi

# Test 7: Multiple Queries (Stress Test)
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test 7: Multiple Queries${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

QUERIES=(
  "What are the Greeks?"
  "Explain implied volatility"
  "What is the wheel strategy?"
)

QUERY_FAILED=0
for query in "${QUERIES[@]}"; do
    echo "  Testing: $query"
    RESULT=$(curl -s -X POST "$API_URL/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"query": "'"$query"'", "provider": "'$PROVIDER'", "num_results": 3}')
    
    if echo "$RESULT" | jq -e '.answer' > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Success"
    else
        echo -e "  ${RED}✗${NC} Failed"
        QUERY_FAILED=$((QUERY_FAILED + 1))
    fi
done

if [ $QUERY_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ PASS${NC}: All queries successful"
else
    echo -e "${RED}❌ FAIL${NC}: $QUERY_FAILED queries failed"
    FAILED=$((FAILED + 1))
fi

# Summary
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo -e "${GREEN}✅ No warnings!${NC}"
    echo ""
    echo "🎉 Application is working perfectly!"
    exit 0
elif [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All critical tests passed${NC}"
    echo -e "${YELLOW}⚠️  $WARNINGS warning(s)${NC}"
    echo ""
    echo "Application is working, but check warnings above."
    echo "Warnings typically relate to highlighting not working perfectly,"
    echo "which is non-critical (app still functions normally)."
    exit 0
else
    echo -e "${RED}❌ $FAILED test(s) failed${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $WARNINGS warning(s)${NC}"
    fi
    echo ""
    echo "❌ Critical issues detected! Review failures above."
    exit 1
fi

