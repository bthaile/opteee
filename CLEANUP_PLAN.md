# Repository Cleanup Plan

**Created:** 2025-10-12  
**Purpose:** Reduce confusion, improve maintainability, archive unused code

---

## 🎯 Current Production Stack

**These files are ACTIVE and should be KEPT:**

### Core Application
- ✅ `app/` - FastAPI backend (production)
- ✅ `frontend/` - React frontend
- ✅ `config.py` - System configuration
- ✅ `rag_pipeline.py` - Core RAG logic
- ✅ `vector_search.py` - Vector search utilities

### Infrastructure
- ✅ `Dockerfile` - Container build
- ✅ `docker-compose.yml` - Production compose
- ✅ `requirements.txt` - Python dependencies
- ✅ `pyproject.toml` - Poetry config
- ✅ `poetry.lock` - Lock file

### Data
- ✅ `vector_store/` - Vector database
- ✅ `processed_transcripts/` - Processed data
- ✅ `static/` - CSS, assets
- ✅ `templates/` - HTML templates

### Documentation
- ✅ `README.md` - Main docs
- ✅ `HIGHLIGHTING_FIX_SUMMARY.md` - Recent fix docs

---

## 🗑️ Phase 1: Safe to DELETE (High Priority)

**These files are unused or superseded:**

### Duplicate/Old App Files
```
❌ app_enhanced.py          # Old version, superseded by app/
❌ app-gradio.py             # Gradio interface, not used in production
❌ opteee_app.py             # Old app file
❌ main.py                   # Duplicate/old entry point
```

### Test/Debug Scripts (Move to archive)
```
❌ benchmark_models.py
❌ debug_process.py
❌ debug.py
❌ test_advanced_download.py
❌ test_browser_download.py
❌ test_docker_build.py
❌ test_fastapi.py
❌ test_manual_processor.py
❌ test_pipeline_fixes.py
❌ test_pipeline.py
❌ test_rag.py
❌ test_single_question.py
❌ test_transcript_methods.py
❌ test_working_download.py
❌ test.py
❌ test_output.txt
❌ rag_test_results.txt
```

### One-time Setup/Migration Scripts
```
❌ download_and_setup.py
❌ migrate_to_clean_system.py
❌ prepare_production.py
❌ rebuild_env.sh
❌ rebuild_progress.py
❌ patch_sentence_transformers.py
```

### Temporary/Generated Files
```
❌ cookies.txt
❌ fake_cookies.txt
❌ youtube_cookies.txt
❌ failed_video_ids.txt
❌ failed_video_list.txt
❌ failed_video_urls.txt
❌ download_tracker.html
❌ processing_report.md
❌ README.md.backup
```

**Total: ~35 files to delete (~2MB)**

---

## 📦 Phase 2: ARCHIVE (Medium Priority)

**Move to `/archive` directory - might be useful for reference:**

### Data Processing Scripts
```
📦 collect_video_metadata.py
📦 convert_mp4_to_mp3.py
📦 improved_transcript_downloader.py
📦 outlier_scraper.py
📦 parallel_transcribe.py
📦 process_outlier_videos.py
📦 save_youtube_transcript.py
📦 transcript_downloader.py
📦 whisper_focused_downloader.py
📦 whisper_transcribe.py
```

### Utility/Helper Scripts
```
📦 check_audio_files.py
📦 check_chunks.py
📦 clean_video_tracker.py
📦 convert_favicon.py
📦 count_files.py
📦 find_audio_files.py
📦 fix_timestamp_issue.py
📦 fix_urls.py
📦 fix_vector_store.py
📦 generate_download_urls.py
📦 generate_tracker_page.py
📦 get_dates.py
📦 get_upload_dates.py
📦 load_vectors.py
📦 manual_video_processor.py
📦 organize_processed_audio.py
📦 preprocess_transcripts.py
📦 quick_timestamp_fix.py
📦 search_helper.py
📦 search_transcripts.py
📦 show_clean_state.py
📦 verify_chunks.py
📦 verify_vector_store.py
```

### Setup/Validation Scripts
```
📦 create_vector_store.py      # Keep if rebuilding vector store
📦 prepare_vector_store.py
📦 rebuild_vector_store.py
📦 run_pipeline.py
📦 validate_pipeline.py
📦 validate_system.py
```

### Shell Scripts
```
📦 deploy_fix.sh
📦 dev_ui_simple.sh
📦 dev_ui.sh
📦 download_failed_videos.sh
📦 process_missing_transcripts.sh
📦 run_dev_local.sh
📦 run_dev.sh
📦 run_local.sh
📦 setup.sh
📦 test_hf_deployment.sh
📦 test_setup.sh
```

**Total: ~50 files to archive**

---

## ⚠️ Phase 3: REVIEW (Low Priority)

**Keep for now, review later:**

### Configuration Files
```
⚠️ docker-compose.dev.yml    # Dev environment - keep if used
⚠️ minimal_requirements.txt  # Minimal setup - archive?
⚠️ runtime_requirements.txt  # Runtime deps - consolidate?
⚠️ runtime.txt               # Python version - needed?
⚠️ pipeline_config.py        # Pipeline config - still used?
```

### Shell Entry Points
```
⚠️ run.sh                    # Check what this does
⚠️ startup.sh                # Container startup?
⚠️ setup                     # What is this?
⚠️ run_fastapi_dev.py        # Dev server - keep or consolidate?
```

### Documentation
```
⚠️ AUTO_REBUILD_README.md
⚠️ BEGINNER_GUIDE.md
⚠️ CHAT_CONVERSION_SOW.md
⚠️ GITHUB_SETUP.md
⚠️ HUGGINGFACE_SETUP.md
⚠️ manual_download_instructions.md
```

---

## 🗂️ Proposed New Structure

```
opteee/
├── app/                    # FastAPI backend (production)
├── frontend/               # React frontend
├── archive/               # 🆕 Archived scripts
│   ├── data_processing/   # Download, transcribe scripts
│   ├── utilities/         # One-off helper scripts
│   └── tests/            # Old test scripts
├── docs/                  # 🆕 Consolidated documentation
│   ├── SETUP.md
│   ├── DEPLOYMENT.md
│   └── HIGHLIGHTING.md
├── scripts/               # 🆕 Active utility scripts only
│   ├── rebuild_vector_store.py
│   └── validate_system.py
├── config.py
├── rag_pipeline.py
├── vector_search.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Execution Plan

### Step 1: Create Archive Structure
```bash
mkdir -p archive/{data_processing,utilities,tests}
mkdir -p docs
mkdir -p scripts
```

### Step 2: Delete Safe Files (Phase 1)
```bash
# Backup first!
tar -czf backup_before_cleanup_$(date +%Y%m%d).tar.gz \
  app_enhanced.py app-gradio.py opteee_app.py main.py \
  test_*.py debug*.py benchmark_models.py \
  *cookies*.txt failed_*.txt *.backup

# Delete after backup confirmed
rm app_enhanced.py app-gradio.py opteee_app.py main.py
rm test_*.py debug*.py benchmark_models.py
rm *cookies*.txt failed_*.txt *.backup
rm test_output.txt rag_test_results.txt download_tracker.html
```

### Step 3: Archive Scripts (Phase 2)
```bash
# Move data processing scripts
mv *downloader*.py *transcribe*.py *scraper*.py archive/data_processing/

# Move utility scripts
mv check_*.py fix_*.py verify_*.py convert_*.py archive/utilities/
mv get_*.py find_*.py count_*.py organize_*.py archive/utilities/
mv generate_*.py search_*.py show_*.py archive/utilities/

# Move shell scripts
mv *.sh archive/utilities/
```

### Step 4: Keep Active Scripts
```bash
# Keep only essential scripts in /scripts
mv create_vector_store.py scripts/
mv rebuild_vector_store.py scripts/
mv validate_system.py scripts/
```

### Step 5: Consolidate Documentation
```bash
# Move docs to /docs
mv *_README.md *_GUIDE.md *_SETUP.md docs/
mv HIGHLIGHTING_FIX_SUMMARY.md docs/HIGHLIGHTING.md
```

### Step 6: Clean Up Environments
```bash
# Remove unused virtual environments (keep main one)
rm -rf whisper-env/
# Only if not needed: rm -rf env/ venv/
```

---

## 📊 Expected Results

**Before Cleanup:**
- ~150 files in root directory
- Multiple duplicate implementations
- Unclear which files are active

**After Cleanup:**
- ~20 files in root directory
- Clear separation: app/ (production), archive/ (old), scripts/ (utils)
- Easy to understand what's running

**Space Savings:**
- Delete: ~35 files, ~2MB
- Archive: ~50 files, ~5MB
- Root directory: 70% fewer files

---

## ⚠️ Safety Checklist

Before executing cleanup:

- [ ] Backup entire repository
- [ ] Commit all current changes
- [ ] Tag current state: `git tag pre-cleanup-2025-10-12`
- [ ] Test production deployment still works
- [ ] Document any scripts that are periodically run
- [ ] Review with team if applicable
- [ ] Keep archive for 6 months minimum

---

## 🎯 Priority Recommendations

**Do NOW (Before next deployment):**
1. Delete test files and debug scripts ✅
2. Archive old app versions (app-gradio.py, etc.) ✅
3. Remove temporary files (cookies, failed lists) ✅

**Do SOON (Next sprint):**
4. Archive data processing scripts ✅
5. Consolidate documentation ✅
6. Organize utility scripts ✅

**Do LATER (Maintenance):**
7. Review and consolidate requirements files
8. Clean up old virtual environments
9. Review configuration files

---

**Status:** Ready for execution  
**Risk Level:** Low (with backups)  
**Time Required:** ~30 minutes  
**Benefit:** Much clearer codebase structure

