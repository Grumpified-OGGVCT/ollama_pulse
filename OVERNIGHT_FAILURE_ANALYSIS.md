# Overnight Failure Analysis - Root Causes Found

**Analysis Date**: November 3, 2025  
**Failures Analyzed**: 14/20 ingestion runs  
**Root Causes**: 2 critical issues identified

---

## 📊 Failure Pattern

**Ingestion Workflow** (14 failures, 6 success):
- ✅ All 13 parallel ingestion jobs PASS
- ❌ Aggregate job FAILS every time
- ⏭️ Turbo-cloud-deep job SKIPPED (depends on aggregate)

**Pattern**: Data collection works, but combining the data fails

---

## 🔍 Root Causes Identified

### Issue #1: Artifact Download/Merge Problems

**What's Happening**:
```yaml
# Each ingestion job uploads:
path: data/  # Uploads ENTIRE data directory

# Aggregate job downloads:
pattern: ingestion-*
path: data/
merge-multiple: true  # Tries to merge 13 overlapping data/ directories
```

**Result**: Nested directories (data/data/), file overwrites, corrupted structure

**Fix Applied**:
```yaml
# Upload only specific source directory:
path: data/${{ matrix.script.name }}/  # Just official/, community/, etc.

# Download to separate location:
path: ./artifacts/
merge-multiple: false

# Manually merge with control:
cp -r artifacts/ingestion-*/* data/
```

### Issue #2: Model Enhancement Not Running

**What's Happening**:
- Code IS on main (PR #11 merged)
- enhanced_report_generator.py exists
- But reports still use templates

**Likely Causes**:
1. Import failing silently in CI (missing dependency?)
2. OLLAMA_API_KEY not working (authentication failing?)
3. Models throwing errors but being caught by try/except

**Need to investigate**: Actual workflow logs from report generation

---

## ✅ Fixes Deployed

### Fix #1: Artifact Handling (Just Pushed)

**Commit**: 050091e  
**File**: `.github/workflows/ingest.yml`  
**Changes**:
- Upload specific source directories only
- Download to separate ./artifacts/ directory
- Manual merge with verbose logging
- Verification step shows which files exist

**Expected Result**: Aggregate job succeeds

### Fix #2: Model Enhancement (On Main via PR #11)

**Commit**: 60f1328  
**Files**: 
- `scripts/enhanced_report_generator.py`
- `scripts/generate_report.py`
- `scripts/langchain_adaptive.py`
- `requirements.txt`

**Status**: Deployed but NOT RUNNING

---

## 🎯 Next Steps

### Immediate (Fix Aggregate Failures)

1. **Test Fix**: Trigger new ingestion run
   - URL: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/ingest.yml
   - Click "Run workflow"
   - Watch aggregate job logs for verbose output
   - Should show "Merging artifacts/ingestion-*/" messages
   - Should show "Found: data/official/2025-11-03.json" etc.

2. **Verify Success**: Aggregate job turns green ✅

### Then (Debug Model Enhancement)

3. **Trigger Report**: Once aggregation works
   - URL: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/morning_report.yml
   - Enable "Force run" checkbox
   - Watch for these messages in logs:
     - "🤖 Activating multi-model intelligence pipeline..."
     - "🔬 ANALYSIS STAGE: DeepSeek-V3.1..."
     - OR "⚠️ Enhanced generation not available" (import failed)
     - OR "⚠️ Model enhancement error: [error]" (models crashed)

4. **Debug Based on Output**:
   - If import fails → missing dependency in CI
   - If models crash → API key or authentication issue
   - If nothing happens → code not being executed

---

## 💡 What I Learned

**Mistake #1**: Used `merge-multiple: true` without understanding it creates overlapping directories

**Mistake #2**: Pushed model code without verifying dependencies install correctly in CI

**Mistake #3**: Relied on silent fallbacks instead of fail-fast debugging

**Correction**: Fixed artifact handling with explicit merge + diagnostic logging

---

**Status**: Artifact fix deployed (050091e), ready for testing

**Next**: Wait for you to trigger ingestion workflow and see if aggregate succeeds

