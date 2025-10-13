# Deployment Steps - Complete Guide

**Date:** 2025-10-12  
**Purpose:** Deploy highlighting fix and cleanup repository

---

## 📋 **Your Plan**

1. ✅ **Checkpoint** - Create safe rollback point
2. ✅ **Cleanup** - Organize repository  
3. ✅ **Verify** - Check deployment files
4. ✅ **Deploy** - Push to production
5. ✅ **Test** - Verify highlighting works

---

## 🎯 **Step 1: Create Checkpoint (SAFE ROLLBACK)**

### 1.1 Check Current Status
```bash
git status
```

### 1.2 Stage Highlighting Fix Files
```bash
git add config.py \
        app/services/formatters.py \
        HIGHLIGHTING_FIX_SUMMARY.md \
        CLEANUP_PLAN.md \
        CLEANUP_QUICKSTART.md \
        VERIFICATION_PLAN.md \
        DEPLOYMENT_STEPS.md \
        cleanup_repo.sh \
        verify_application.sh
```

### 1.3 Commit Highlighting Fix (Before Cleanup)
```bash
git commit -m "fix: add text highlighting feature to source transcripts

- Updated system prompt to instruct AI to directly quote sources
- Added quote extraction and highlighting in app/services/formatters.py
- Highlighted quotes appear in yellow/blue in transcript snippets
- Added comprehensive logging to track highlighting effectiveness
- Created cleanup plan and verification tools

Changes are additive and non-breaking.
If highlighting doesn't work, app continues to function normally."
```

### 1.4 Create Rollback Tag
```bash
# Tag before cleanup (easy rollback point)
git tag -a pre-cleanup-$(date +%Y%m%d) -m "Checkpoint before repository cleanup"

# Verify tag created
git tag -l "pre-cleanup-*"
```

### 1.5 Push Checkpoint (Optional but Recommended)
```bash
# Push commit and tag
git push origin main
git push origin --tags

# This creates a safe rollback point in the cloud
```

---

## 🧹 **Step 2: Repository Cleanup**

### 2.1 Preview Cleanup (Dry Run)
```bash
# See what will be deleted/moved WITHOUT making changes
bash cleanup_repo.sh --dry-run

# Review the output carefully!
# Make sure nothing critical is being removed
```

**Expected output:**
```
[DRY RUN] Removing old app versions...
[DRY RUN] rm app_enhanced.py
[DRY RUN] rm app-gradio.py
[DRY RUN] Archiving data processing scripts...
[DRY RUN] mv outlier_scraper.py archive/data_processing/
...
```

### 2.2 Execute Cleanup
```bash
# If dry-run looks good, execute for real
bash cleanup_repo.sh

# This will:
# - Create backup in cleanup_backups/
# - Delete ~35 unnecessary files
# - Archive ~50 old scripts to archive/
# - Organize essential scripts in scripts/
```

### 2.3 Review Changes
```bash
# See what changed
git status

# Check new structure
ls -la
ls -la archive/
ls -la scripts/

# Should see:
# - Cleaner root directory (~20 files instead of 150)
# - archive/ directory with old scripts
# - scripts/ directory with essential utils
```

### 2.4 Commit Cleanup
```bash
git add .
git commit -m "chore: cleanup repository structure

- Delete unused test, debug, and temporary files (~35 files)
- Archive old scripts to archive/ for reference (~50 files)
- Move essential scripts to scripts/ directory
- Root directory reduced from 150 to ~20 files for clarity

Backup saved in cleanup_backups/
All production files (app/, frontend/, config.py) untouched."
```

---

## ✅ **Step 3: Verify Deployment Files**

### 3.1 Check Core Production Files
```bash
# Verify essential files still exist and are correct
echo "Checking production files..."

# Core application
test -f config.py && echo "✅ config.py" || echo "❌ config.py MISSING!"
test -f rag_pipeline.py && echo "✅ rag_pipeline.py" || echo "❌ MISSING!"
test -d app/ && echo "✅ app/ directory" || echo "❌ MISSING!"
test -d frontend/ && echo "✅ frontend/ directory" || echo "❌ MISSING!"

# Infrastructure
test -f Dockerfile && echo "✅ Dockerfile" || echo "❌ MISSING!"
test -f docker-compose.yml && echo "✅ docker-compose.yml" || echo "❌ MISSING!"
test -f requirements.txt && echo "✅ requirements.txt" || echo "❌ MISSING!"

# Key updated files
test -f app/services/formatters.py && echo "✅ formatters.py (UPDATED)" || echo "❌ MISSING!"

echo ""
echo "All checks should show ✅"
```

### 3.2 Verify No Import Errors
```bash
# Test Python imports still work
python3 -c "from app.services.formatters import ResponseFormatter; print('✅ Formatters OK')" 2>&1
python3 -c "from app.services.rag_service import RAGService; print('✅ RAG Service OK')" 2>&1
python3 -c "from rag_pipeline import run_rag_query; print('✅ RAG Pipeline OK')" 2>&1
python3 -c "from config import SYSTEM_PROMPT; print('✅ Config OK')" 2>&1

echo ""
echo "All imports should show ✅"
```

### 3.3 Check File Sizes (Sanity Check)
```bash
# Make sure files aren't corrupted or empty
ls -lh config.py app/services/formatters.py rag_pipeline.py

# Expected:
# config.py: ~4-5 KB
# formatters.py: ~20-25 KB  
# rag_pipeline.py: ~25-30 KB
```

---

## 🚀 **Step 4: Deploy to Production**

### 4.1 Final Pre-Deploy Check
```bash
# Ensure everything is committed
git status

# Should show: "nothing to commit, working tree clean"
```

### 4.2 Push to Production
```bash
# Push all changes
git push origin main

# Push tags
git push origin --tags
```

### 4.3 Monitor Deployment
```bash
# Watch your deployment system
# (Depends on your deployment setup - Docker, K8s, etc.)

# If using Docker Compose on server:
# ssh your-server
# cd /path/to/opteee
# git pull
# docker-compose build
# docker-compose up -d
# docker-compose logs -f --tail 100
```

### 4.4 Wait for Deployment
```bash
# Wait 2-3 minutes for:
# - Container rebuild
# - Application startup
# - RAG service initialization
```

---

## 🧪 **Step 5: Test in Production**

### 5.1 Check Application Health
```bash
# Test health endpoint
curl https://your-production-url.com/api/health

# Expected:
# {"status":"healthy","timestamp":"...","version":"..."}
```

### 5.2 Test Basic Query
```bash
# Test a simple query
curl -X POST https://your-production-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is a covered call?",
    "provider": "claude",
    "num_results": 5
  }'

# Should return answer and sources
```

### 5.3 Test Highlighting Feature (KEY TEST)

#### Option A: Via UI (Recommended)
1. Open production URL in browser
2. Ask: **"What is PEAD?"**
3. **Check AI Response:**
   - ✅ Should include quoted phrases like: `"post earnings announcement drift is a thing"`
   - ✅ Multiple quotes (2-3 ideally)

4. **Check Source Snippets:**
   - ✅ Should see yellow/blue highlighted text
   - ✅ Header: "📚 Source Videos with Highlighted Quotes"
   - ✅ Highlighted text matches phrases from AI answer

#### Option B: Via API
```bash
curl -X POST https://your-production-url.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is PEAD?",
    "provider": "claude",
    "num_results": 5
  }' | jq '.answer' | grep -o '"[^"]*"'

# Should see quoted phrases extracted
```

### 5.4 Check Production Logs (CRITICAL)

**Look for these NEW log lines:**
```
✅ Extracted 2 quotes for highlighting:
   1. "post earnings announcement drift is a thing"
   2. "There's certain conditions that have to be met"
   ✓ Highlighted: "post earnings announcement drift is a thing"
✅ Applied 2 highlight(s) to source content
```

**If you see:**
```
⚠️ No quotes extracted from AI answer - highlighting will not work
```
- This means the AI didn't follow the prompt to quote sources
- App still works fine, just no highlighting
- May need to adjust system prompt or try different LLM

### 5.5 Test Multiple Queries
```bash
# Test various topics
QUERIES=(
  "What are the Greeks?"
  "Explain implied volatility"
  "What is the wheel strategy?"
  "How does theta decay work?"
)

for query in "${QUERIES[@]}"; do
  echo "Testing: $query"
  curl -X POST https://your-production-url.com/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$query\", \"provider\": \"claude\", \"num_results\": 3}" \
    | jq -r '.answer' | head -3
  echo "---"
done
```

---

## 📊 **Success Criteria**

### ✅ **Minimum Success (App Works)**
- [ ] Application starts without errors
- [ ] Health endpoint responds
- [ ] Queries return answers
- [ ] Sources are included
- [ ] Video URLs are valid
- [ ] No Python import errors

### 🎯 **Full Success (Highlighting Works)**
- [ ] AI responses include direct quotes in "double quotes"
- [ ] Logs show: "Extracted X quotes for highlighting"
- [ ] Logs show: "Applied X highlight(s) to source content"
- [ ] UI shows yellow/blue highlighted text in source snippets
- [ ] Highlighting header appears when quotes are found

---

## 🚨 **Rollback Plan (If Needed)**

### Option 1: Rollback via Git Tag
```bash
# Reset to pre-cleanup state
git reset --hard pre-cleanup-YYYYMMDD

# Force push if needed (CAREFUL!)
git push origin main --force

# Redeploy
```

### Option 2: Rollback Just Cleanup
```bash
# Undo cleanup commit but keep highlighting fix
git revert HEAD~1

# Push
git push origin main
```

### Option 3: Use Cleanup Backup
```bash
# Extract files from backup
tar -xzf cleanup_backups/pre_cleanup_*.tar.gz

# Review and restore needed files
```

---

## 📈 **Expected Results**

### **After Cleanup:**
- Root directory: 150 files → ~20 files ✅
- Better organization and clarity ✅
- All production code intact ✅

### **After Deployment:**
- Highlighting feature active ✅
- AI uses direct quotes in responses ✅
- Source snippets show highlighted text ✅
- App performance unchanged ✅

### **If Highlighting Doesn't Work:**
- App still functions normally ✅
- Users can still read full transcripts ✅
- No errors or crashes ✅
- Can iterate on prompt tuning ✅

---

## 💡 **Tips**

1. **Take your time** - Review each step's output
2. **Check logs** - Production logs are your best friend
3. **Test incrementally** - Don't skip verification steps
4. **Have rollback ready** - Know how to undo if needed
5. **Document issues** - Note anything unexpected

---

## 🎯 **Quick Reference: All Commands in Order**

```bash
# 1. CHECKPOINT
git add config.py app/services/formatters.py *.md *.sh
git commit -m "fix: add text highlighting + cleanup plan"
git tag -a pre-cleanup-$(date +%Y%m%d) -m "Checkpoint before cleanup"
git push origin main --tags

# 2. CLEANUP
bash cleanup_repo.sh --dry-run  # Review first!
bash cleanup_repo.sh             # Execute
git add .
git commit -m "chore: cleanup repository structure"

# 3. VERIFY
test -f config.py && echo "✅" || echo "❌"
python3 -c "from app.services.formatters import ResponseFormatter; print('✅')"

# 4. DEPLOY
git push origin main
# Wait for deployment...

# 5. TEST
curl https://your-prod-url.com/api/health
# Test in UI: "What is PEAD?"
# Check logs for: "Extracted X quotes"
```

---

**Status:** Ready to execute  
**Risk Level:** Low (with rollback plan)  
**Time Required:** 30-45 minutes  
**Go/No-Go:** ✅ Ready to proceed

