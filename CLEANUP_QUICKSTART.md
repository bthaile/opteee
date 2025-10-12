# Repository Cleanup - Quick Start

## 🎯 TL;DR

Your repository has **~150 files** in the root directory, many unused. This cleanup will:
- ✅ Delete ~35 unnecessary files (tests, debug scripts, temp files)
- ✅ Archive ~50 old scripts for reference
- ✅ Organize into clean structure: `app/`, `scripts/`, `archive/`, `docs/`

**Result:** Root directory goes from 150 files → ~20 files

---

## 🚀 Quick Execution

### Option 1: Dry Run First (Recommended)
```bash
# See what would be deleted/moved WITHOUT making changes
bash cleanup_repo.sh --dry-run
```

### Option 2: Full Cleanup
```bash
# Execute full cleanup (creates backup first)
bash cleanup_repo.sh
```

### Option 3: Phase by Phase
```bash
# Phase 1: Delete unnecessary files only
bash cleanup_repo.sh --phase 1

# Phase 2: Archive scripts only
bash cleanup_repo.sh --phase 2
```

---

## 📋 What Gets Removed

### ❌ **Deleted** (Phase 1)
- Old app versions: `app-gradio.py`, `app_enhanced.py`, `opteee_app.py`
- Test files: `test_*.py`, `debug*.py`
- Temp files: `cookies.txt`, `failed_*.txt`, backups

### 📦 **Archived** (Phase 2)  
Moved to `archive/` for reference:
- Data processing: downloaders, transcribers, scrapers
- Utilities: one-off fix/check/convert scripts  
- Shell scripts: old dev/deploy scripts

### ✅ **Kept**
- `app/` - Production FastAPI backend
- `frontend/` - React frontend
- `config.py`, `rag_pipeline.py` - Core logic
- `requirements.txt`, `Dockerfile` - Infrastructure
- `vector_store/`, `processed_transcripts/` - Data

---

## 🛡️ Safety Features

The script:
1. ✅ Creates automatic backup before changes
2. ✅ Checks for git repository
3. ✅ Warns about uncommitted changes
4. ✅ Supports dry-run mode
5. ✅ Can be run phase by phase

**Backup location:** `cleanup_backups/pre_cleanup_YYYYMMDD_HHMMSS.tar.gz`

---

## 📊 Before vs After

### Before
```
opteee/
├── app.py
├── app_enhanced.py
├── app-gradio.py
├── test_this.py
├── test_that.py
├── debug_something.py
├── fix_issue.py
├── ... (150+ files!)
```

### After
```
opteee/
├── app/                    # Production backend
├── frontend/               # Frontend
├── scripts/                # Essential utils
├── archive/                # Old scripts (reference)
├── docs/                   # Documentation
├── config.py
├── rag_pipeline.py
├── requirements.txt
└── README.md
```

---

## ⚠️ Pre-Cleanup Checklist

Before running cleanup:

- [ ] **Commit current changes** (or stash them)
  ```bash
  git add .
  git commit -m "WIP: before cleanup"
  ```

- [ ] **Tag current state** (easy rollback)
  ```bash
  git tag pre-cleanup-$(date +%Y%m%d)
  ```

- [ ] **Run dry-run first**
  ```bash
  bash cleanup_repo.sh --dry-run
  ```

- [ ] **Review what will be deleted**
  Check the output carefully

---

## 🔄 Post-Cleanup Steps

After cleanup completes:

### 1. Review Changes
```bash
git status
git diff
```

### 2. Test Application
```bash
# Make sure production still works
docker-compose up --build
# Or however you normally test
```

### 3. Commit if Satisfied
```bash
git add .
git commit -m "chore: cleanup repository structure

- Delete unused test and debug files
- Archive old scripts to archive/ directory
- Organize essential scripts in scripts/
- Improve root directory clarity (150 → 20 files)"
```

### 4. Push Changes
```bash
git push origin main
```

---

## 🚨 Rollback (If Needed)

### Option 1: Use Git Tag
```bash
# Reset to pre-cleanup state
git reset --hard pre-cleanup-YYYYMMDD
```

### Option 2: Use Backup
```bash
# Extract backup
tar -xzf cleanup_backups/pre_cleanup_*.tar.gz
```

### Option 3: Undo Commit
```bash
# If you already committed
git revert HEAD
```

---

## 💡 FAQ

**Q: Will this break my production deployment?**  
A: No. The cleanup only affects development/utility scripts. Core app files (`app/`, `frontend/`, `config.py`) are untouched.

**Q: What if I need an archived script later?**  
A: All archived files are in `archive/` directory. You can always move them back or reference them.

**Q: Can I customize what gets deleted?**  
A: Yes! Edit `cleanup_repo.sh` or manually delete/archive files. The script is just a helper.

**Q: Do I need to run this?**  
A: No, but it will make your repository much easier to navigate and reduce confusion.

**Q: How long does it take?**  
A: ~30 seconds for the script to run, ~5 minutes to review changes.

---

## 📞 Support

If you encounter issues:

1. Check `CLEANUP_PLAN.md` for detailed explanation
2. Review the backup: `cleanup_backups/`
3. The cleanup is reversible via git
4. All archived files are still accessible in `archive/`

---

**Created:** 2025-10-12  
**Last Updated:** 2025-10-12  
**Status:** Ready to use

