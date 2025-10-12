#!/bin/bash
# Repository Cleanup Script
# Run with: bash cleanup_repo.sh [--dry-run] [--phase N]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DRY_RUN=false
PHASE="all"
BACKUP_DIR="cleanup_backups"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --phase)
            PHASE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--dry-run] [--phase N]"
            echo "  --dry-run    Show what would be done without making changes"
            echo "  --phase N    Run only phase N (1, 2, or all)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}   OPTEEE Repository Cleanup Script${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}"
    echo ""
fi

# Function to execute or simulate command
run_cmd() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY RUN]${NC} $@"
    else
        echo -e "${GREEN}[EXECUTING]${NC} $@"
        eval "$@"
    fi
}

# Step 0: Safety checks
echo -e "${BLUE}📋 Step 0: Safety Checks${NC}"
echo "----------------------------------------"

# Check if git repo
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Not a git repository. Aborting for safety.${NC}"
    exit 1
fi

# Check for uncommitted changes
if [ "$DRY_RUN" = false ]; then
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}⚠️  You have uncommitted changes.${NC}"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Cleanup cancelled."
            exit 1
        fi
    fi
fi

echo -e "${GREEN}✅ Safety checks passed${NC}"
echo ""

# Step 1: Create backup
if [ "$DRY_RUN" = false ]; then
    echo -e "${BLUE}💾 Creating backup...${NC}"
    echo "----------------------------------------"
    BACKUP_FILE="${BACKUP_DIR}/pre_cleanup_$(date +%Y%m%d_%H%M%S).tar.gz"
    run_cmd "mkdir -p ${BACKUP_DIR}"
    run_cmd "tar -czf ${BACKUP_FILE} \
        app_enhanced.py app-gradio.py opteee_app.py main.py \
        test_*.py debug*.py benchmark_models.py \
        *cookies*.txt failed_*.txt *.backup \
        2>/dev/null || true"
    echo -e "${GREEN}✅ Backup created: ${BACKUP_FILE}${NC}"
    echo ""
fi

# Step 2: Create directory structure
echo -e "${BLUE}📁 Creating archive structure...${NC}"
echo "----------------------------------------"
run_cmd "mkdir -p archive/data_processing"
run_cmd "mkdir -p archive/utilities"
run_cmd "mkdir -p archive/tests"
run_cmd "mkdir -p docs"
run_cmd "mkdir -p scripts"
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# PHASE 1: Delete unnecessary files
if [ "$PHASE" = "1" ] || [ "$PHASE" = "all" ]; then
    echo -e "${BLUE}🗑️  PHASE 1: Deleting unnecessary files${NC}"
    echo "========================================"
    echo ""
    
    # Old app files
    echo "Removing old app versions..."
    for file in app_enhanced.py app-gradio.py opteee_app.py main.py; do
        if [ -f "$file" ]; then
            run_cmd "rm $file"
        fi
    done
    
    # Test files
    echo "Removing test files..."
    for file in test_*.py debug*.py benchmark_models.py; do
        if [ -f "$file" ]; then
            run_cmd "rm $file"
        fi
    done
    
    # Temporary files
    echo "Removing temporary files..."
    for pattern in "*cookies*.txt" "failed_*.txt" "*.backup" "test_output.txt" "rag_test_results.txt" "download_tracker.html"; do
        for file in $pattern; do
            if [ -f "$file" ]; then
                run_cmd "rm $file"
            fi
        done
    done
    
    echo -e "${GREEN}✅ Phase 1 complete${NC}"
    echo ""
fi

# PHASE 2: Archive scripts
if [ "$PHASE" = "2" ] || [ "$PHASE" = "all" ]; then
    echo -e "${BLUE}📦 PHASE 2: Archiving scripts${NC}"
    echo "========================================"
    echo ""
    
    # Data processing scripts
    echo "Archiving data processing scripts..."
    for pattern in "*downloader*.py" "*transcribe*.py" "*scraper*.py" "save_youtube_transcript.py"; do
        for file in $pattern; do
            if [ -f "$file" ]; then
                run_cmd "mv $file archive/data_processing/"
            fi
        done
    done
    
    # Utility scripts
    echo "Archiving utility scripts..."
    for pattern in "check_*.py" "fix_*.py" "verify_*.py" "convert_*.py" \
                   "get_*.py" "find_*.py" "count_*.py" "organize_*.py" \
                   "generate_*.py" "search_*.py" "show_*.py" \
                   "*_video_*.py" "manual_video_processor.py"; do
        for file in $pattern; do
            if [ -f "$file" ] && [ "$file" != "get_available_providers" ]; then
                run_cmd "mv $file archive/utilities/"
            fi
        done
    done
    
    # Shell scripts
    echo "Archiving shell scripts..."
    for pattern in "*.sh"; do
        for file in $pattern; do
            # Keep cleanup_repo.sh itself!
            if [ -f "$file" ] && [ "$file" != "cleanup_repo.sh" ]; then
                run_cmd "mv $file archive/utilities/"
            fi
        done
    done
    
    # One-time setup scripts
    echo "Archiving setup/migration scripts..."
    for file in download_and_setup.py migrate_to_clean_system.py prepare_production.py \
                rebuild_env.sh rebuild_progress.py patch_sentence_transformers.py \
                load_vectors.py pipeline_config.py; do
        if [ -f "$file" ]; then
            run_cmd "mv $file archive/utilities/"
        fi
    done
    
    echo -e "${GREEN}✅ Phase 2 complete${NC}"
    echo ""
fi

# Keep only essential scripts in /scripts
echo -e "${BLUE}🔧 Moving essential scripts to /scripts${NC}"
echo "----------------------------------------"
for file in create_vector_store.py rebuild_vector_store.py validate_system.py; do
    if [ -f "$file" ]; then
        run_cmd "mv $file scripts/"
    fi
done
echo ""

# Summary
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}✅ Cleanup Complete!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo "📊 Summary:"
echo "  - Old files deleted (Phase 1)"
echo "  - Scripts archived to archive/ (Phase 2)"
echo "  - Essential scripts in scripts/"
if [ "$DRY_RUN" = false ]; then
    echo "  - Backup saved: ${BACKUP_FILE}"
fi
echo ""
echo "Next steps:"
echo "  1. Review the changes: git status"
echo "  2. Test the application still works"
echo "  3. Commit if satisfied: git add . && git commit -m 'chore: cleanup repository structure'"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}💡 Run without --dry-run to execute changes${NC}"
fi

