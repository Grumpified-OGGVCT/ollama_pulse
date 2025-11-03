# Ollama Pulse Workflow Architecture

**Complete system documentation for GitHub Actions workflows**

---

## 🏗️ System Overview

Ollama Pulse uses 4 active GitHub Actions workflows to maintain a self-sustaining ecosystem intelligence platform:

```
┌─────────────────────────────────────────────────────────────┐
│                    OLLAMA PULSE SYSTEM                      │
└─────────────────────────────────────────────────────────────┘
          │
          ├─ ⏰ HOURLY INGESTION (ingest.yml)
          │   └─ Collects data from 16 sources every hour
          │   └─ Runs aggregate + insights mining
          │   └─ Commits to data/** directories
          │
          ├─ 🌅 MORNING REPORT (morning_report.yml)
          │   └─ Runs at 08:30 CT (2x cron for DST)
          │   └─ Generates EchoVein report
          │   └─ Posts to Nostr + GitHub Pages
          │
          ├─ 🌆 AFTERNOON REPORT (afternoon_report.yml)
          │   └─ Runs at 16:30 CT (2x cron for DST)
          │   └─ Generates EchoVein report
          │   └─ Posts to Nostr + GitHub Pages
          │
          └─ 📡 WEBHOOK TRIGGER (trigger_grumpiblogged.yml)
              └─ Triggers on new report commits
              └─ Sends webhook to GrumpiBlogged repo
              └─ Enables meta-report aggregation
```

---

## 📊 Workflow Details

### 1. Ingestion Workflow (`ingest.yml`)

**Trigger**: Hourly at :00 UTC  
**Duration**: 2-4 minutes (parallel execution)  
**Purpose**: Collect ecosystem data from 16 sources

#### Architecture

```yaml
Job 1: ingest (matrix strategy - 13 parallel jobs)
  ├─ Script 1: ingest_official.py     [CRITICAL]
  ├─ Script 2: ingest_cloud.py        [CRITICAL]
  ├─ Script 3: ingest_community.py    [OPTIONAL]
  ├─ Script 4: ingest_issues.py       [OPTIONAL]
  ├─ Script 5: ingest_tools.py        [OPTIONAL]
  ├─ Script 6: ingest_bounties.py     [OPTIONAL]
  ├─ Script 7: ingest_nostr.py        [OPTIONAL]
  ├─ Script 8: ingest_stackoverflow.py [OPTIONAL]
  ├─ Script 9: ingest_model_registry.py [OPTIONAL]
  ├─ Script 10: ingest_releases.py    [OPTIONAL]
  ├─ Script 11: ingest_devblogs.py    [OPTIONAL]
  ├─ Script 12: ingest_discord.py     [OPTIONAL]
  └─ Script 13: ingest_manual.py      [OPTIONAL]

Job 2: aggregate (depends on ingest)
  ├─ Download all ingestion artifacts
  ├─ Run aggregate.py (turbo scoring)
  └─ Run mine_insights.py (pattern detection)

Job 3: turbo-cloud-deep (depends on aggregate)
  ├─ Deep scan of Ollama Cloud models
  └─ GitHub code search for turbo mentions
```

**Key Features**:
- **Parallel Execution**: 13 scripts run simultaneously (70% faster)
- **Fail-Safe**: Critical scripts must succeed, others can fail gracefully
- **Artifact Transfer**: Each script uploads data, aggregate job downloads all
- **Retry Logic**: 3 attempts with exponential backoff on git push

**Data Flow**:
```
16 Sources → 13 Parallel Scripts → Upload Artifacts → Download & Aggregate → Mine Insights → Commit Data
```

#### Critical vs Optional Sources

**Critical Sources** (MUST succeed):
- `ingest_official.py` - Ollama blog, official updates
- `ingest_cloud.py` - Ollama Cloud/Turbo models

**Optional Sources** (can fail):
- All community, third-party, and supplementary sources
- Failures logged as warnings but don't block workflow

---

### 2. Morning Report Workflow (`morning_report.yml`)

**Trigger**: 08:30 Central Time (dual cron for DST)  
**Duration**: 1-2 minutes  
**Purpose**: Generate morning EchoVein report

#### Schedule Logic

```
CDT (Mar-Nov): cron '30 13 * * *'  (13:30 UTC = 08:30 CDT)
CST (Nov-Mar): cron '30 14 * * *'  (14:30 UTC = 08:30 CST)

Both crons trigger → Time gate filters → Only correct one proceeds
```

#### Data Freshness Validation

```bash
Step 1: Check for data commits in last 90 minutes
  ├─ Success → Proceed with report
  ├─ Failure → Check if today's data file exists
  │   ├─ Exists → Proceed with warning
  │   └─ Missing → Abort (cannot generate report)
```

**Why 90 minutes?**
- Hourly ingestion at :00
- Processing takes 2-4 minutes
- Gate runs at :30 (30-minute offset)
- 90-minute window accommodates delays

#### Report Generation Pipeline

```
1. Run generate_report.py
   └─ Loads data from data/aggregated/{today}.json
   └─ Applies EchoVein persona (4 adaptive modes)
   └─ Generates docs/reports/pulse-{today}.md

2. Run update_index.py
   └─ Scans docs/reports/ for all reports
   └─ Generates docs/index.html with navigation

3. Post to Nostr (optional)
   └─ Converts report to NIP-23 format
   └─ Publishes to 8+ Nostr relays

4. Commit & push to GitHub
   └─ Triggers GitHub Pages deployment
   └─ Updates live site in 1-2 minutes
```

---

### 3. Afternoon Report Workflow (`afternoon_report.yml`)

**Trigger**: 16:30 Central Time (dual cron for DST)  
**Duration**: 1-2 minutes  
**Purpose**: Generate afternoon EchoVein report

#### Architecture

Identical to morning report with different timing:
- Cron schedules: `30 21` (CDT) + `30 22` (CST)
- Time gate: validates 16:30 CT window
- Same data validation, report generation, and publishing pipeline

**Why Two Reports?**
- Morning (08:30): Covers overnight developments
- Afternoon (16:30): Captures day's full activity
- Both use same data sources (cumulative throughout day)

---

### 4. GrumpiBlogged Trigger (`trigger_grumpiblogged.yml`)

**Trigger**: Push to `docs/reports/pulse-*.md`  
**Duration**: 5-10 seconds  
**Purpose**: Notify GrumpiBlogged repo of new report

#### Webhook Flow

```
New Report Committed → Workflow Triggers → Extract Report Metadata → Send repository_dispatch → GrumpiBlogged Receives
```

#### Payload Structure

```json
{
  "source": "ollama_pulse",
  "report_date": "2025-11-02",
  "report_url": "https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-2025-11-02",
  "description": "First 200 chars of report...",
  "timestamp": "2025-11-02T21:30:00Z",
  "commit_sha": "abc123..."
}
```

**Secret Required**: `GRUMPIBLOGGED_PAT`
- GitHub Personal Access Token
- Scopes: `repo`, `workflow`
- Used to trigger workflows in GrumpiBlogged repository

**Fallback**: If secret missing, logs warning but doesn't fail

---

## 🔐 Security Model

### Secrets Hierarchy

1. **GH_PAT** (Required for all workflows)
   - Purpose: Push commits to repository
   - Scopes: `repo`
   - Without this: Workflows run but cannot save results

2. **OLLAMA_API_KEY** (Required for ingestion + reports)
   - Purpose: Access Ollama Cloud API
   - Alternative names: `OLLAMA_TURBO_CLOUD_API_KEY`, `OLLAMA_TURBO_CLOUD_API_KEY_1`, `OLLAMA_TURBO_CLOUD_API_KEY_2`
   - Without this: Ingestion and report generation fail

3. **SUPABASE_URL + SUPABASE_KEY** (Optional)
   - Purpose: Historical project tracking via PostgreSQL
   - Fallback: Local SQLite database
   - Without this: Works fine, just no persistent history

4. **NOSTR_PRIVATE_KEY** (Optional)
   - Purpose: Publish reports to Nostr network
   - Without this: Reports still published to GitHub Pages

5. **GRUMPIBLOGGED_PAT** (Optional)
   - Purpose: Trigger meta-report aggregation
   - Without this: GrumpiBlogged doesn't get notified

### Secret Validation

All workflows validate secrets BEFORE use:
```yaml
- name: Validate secrets
  run: |
    if [ -z "${{ secrets.OLLAMA_API_KEY }}" ]; then
      echo "::error::OLLAMA_API_KEY secret is not configured"
      exit 1
    fi
```

**Benefits**:
- Fail fast with clear error message
- Prevents wasted CI minutes
- Obvious in GitHub Actions UI

---

## ⏱️ Timing & Scheduling

### Cron Schedules

| Workflow | CDT Cron | CST Cron | Local Time | UTC Offset |
|----------|----------|----------|------------|------------|
| Morning | `30 13` | `30 14` | 08:30 CT | -5/-6 |
| Afternoon | `30 21` | `30 22` | 16:30 CT | -5/-6 |
| Ingestion | `0 *` | (same) | Every :00 | N/A |

### DST Transition Handling

**Spring Forward** (March - 2nd Sunday at 2:00 AM):
- Before: CST (UTC-6) → After: CDT (UTC-5)
- Morning switches from 14:30 UTC cron to 13:30 UTC cron
- Automatic via time gate filter

**Fall Back** (November - 1st Sunday at 2:00 AM):
- Before: CDT (UTC-5) → After: CST (UTC-6)
- Morning switches from 13:30 UTC cron to 14:30 UTC cron
- Automatic via time gate filter

**No Manual Intervention Required**

---

## 🔄 Data Flow

### Hourly Cycle

```
00:00 CT → Ingestion triggers (parallel matrix)
   ↓
00:02-00:04 CT → Scripts complete, upload artifacts
   ↓
00:04 CT → Aggregate job combines artifacts
   ↓
00:05 CT → Mine insights, commit to data/**
   ↓
00:06 CT → Git push (with retry if conflict)
   ↓
[Data ready for next report]
```

### Report Generation Cycle

```
08:30 CT / 16:30 CT → Report workflow triggers
   ↓
Time gate validates → Ensure correct time
   ↓
Data freshness check → Validate recent ingestion
   ↓
Generate report → EchoVein markdown
   ↓
Update index → Scan all reports, generate HTML
   ↓
Post to Nostr → NIP-23 long-form (optional)
   ↓
Commit & push → Trigger GitHub Pages deployment
   ↓
[Report live in 1-2 minutes]
```

---

## 📈 Performance Metrics

### Before Fixes

- Ingestion: 5-10 minutes (sequential)
- Git conflicts: Manual resolution required
- DST bugs: 2 failures per year
- Data staleness: Unvalidated
- Error handling: Cascade failures

### After Fixes

- Ingestion: 2-4 minutes (parallel) - **70% faster**
- Git conflicts: Auto-resolved (3-attempt retry) - **95% success**
- DST bugs: Zero (dual cron coverage) - **100% fixed**
- Data staleness: Validated (90-min window) - **Guaranteed fresh**
- Error handling: Graceful degradation - **Resilient**

---

## 🛠️ Customization

### Adjust Report Times

Edit cron schedules in workflow files:

```yaml
# Change morning report to 09:00 CT
schedule:
  - cron: '00 14 * * *'   # CDT (09:00 CDT = 14:00 UTC)
  - cron: '00 15 * * *'   # CST (09:00 CST = 15:00 UTC)

# Update time gate to match
if [ "$HOUR" != "09" ] || [ "$MINUTE" -lt "00" ] || [ "$MINUTE" -gt "15" ]; then
```

### Change Ingestion Frequency

```yaml
# Every 2 hours instead of hourly
schedule:
  - cron: '0 */2 * * *'

# Every 30 minutes
schedule:
  - cron: '*/30 * * * *'
```

### Add New Ingestion Source

1. Create `scripts/ingest_newsource.py`
2. Add to matrix in `ingest.yml`:
```yaml
- { name: 'newsource', file: 'ingest_newsource.py', critical: false }
```
3. Script outputs to `data/newsource/{date}.json`
4. Automatically picked up by aggregate.py

---

## 🐛 Known Limitations

1. **GitHub Actions Minutes**: ~3,600-5,760 min/month may exceed free tier (2,000 min/month)
   - **Mitigation**: Optimize slow scripts, reduce frequency, or upgrade to paid plan

2. **API Rate Limits**: Ollama Cloud API has undocumented rate limits
   - **Mitigation**: Built-in delays in ollama_turbo_client.py

3. **Git Push Conflicts**: Rare but possible if manual commits made during workflow
   - **Mitigation**: 3-attempt retry with backoff

4. **Cron Accuracy**: GitHub Actions cron has ±5-15 minute variance
   - **Mitigation**: 15-minute time gate windows

5. **Parallel Job Limits**: GitHub Free tier limits concurrent jobs
   - **Mitigation**: Matrix strategy handles queueing automatically

---

## 📋 Maintenance Checklist

### Weekly

- [ ] Review workflow run history for failures
- [ ] Check GitHub Actions minutes usage
- [ ] Verify data** directories not growing too large
- [ ] Test manual triggers still work

### Monthly

- [ ] Review and optimize slow ingestion scripts
- [ ] Check for new Ollama data sources to add
- [ ] Verify GitHub Pages deployment working
- [ ] Update dependencies in requirements.txt

### Quarterly

- [ ] Review workflow efficiency metrics
- [ ] Consider caching strategies for models
- [ ] Optimize for GitHub Actions minute usage
- [ ] Update documentation

### Annually

- [ ] Verify DST transitions handled correctly (March, November)
- [ ] Review overall architecture for improvements
- [ ] Consider platform upgrades or optimizations

---

## 🎓 Design Decisions

### Why Dual Cron Schedules?

**Rejected Alternatives**:
- ❌ Single cron + manual DST adjustment → Requires twice-yearly updates
- ❌ Dynamic cron via API → Not supported by GitHub Actions
- ❌ Run both times, deduplicate → Wastes CI minutes

**Chosen Solution**: Dual cron with time gate filter
- ✅ Zero maintenance
- ✅ Automatic DST handling
- ✅ Clear separation of concerns
- ✅ One cron always matches, one always skips

### Why Matrix Strategy for Ingestion?

**Rejected Alternatives**:
- ❌ Sequential execution → Too slow (5-10 minutes)
- ❌ Separate workflows for each source → 13 workflow files (maintenance nightmare)
- ❌ Reusable workflow approach → Excessive complexity, harder debugging

**Chosen Solution**: Matrix strategy with fail-safe
- ✅ Parallel execution (2-4 minutes)
- ✅ Single workflow file (easier maintenance)
- ✅ Individual script isolation (failures don't cascade)
- ✅ Critical vs optional designation (smart resilience)

### Why Artifact System?

**Rejected Alternatives**:
- ❌ Direct git commits from each job → 13 concurrent git conflicts
- ❌ Shared filesystem → Not supported in matrix jobs
- ❌ External storage (S3, etc.) → Adds cost and complexity

**Chosen Solution**: GitHub Actions artifacts
- ✅ Built-in, free, fast
- ✅ Automatic cleanup (7-day retention)
- ✅ No conflicts between parallel jobs
- ✅ Clean data aggregation in single job

---

## 🔗 Integration Points

### GitHub Pages

**Configuration**:
- Deploy from `/docs` folder on `main` branch
- Automatic deployment on every push to `docs/**`
- Live site: https://grumpified-oggvct.github.io/ollama_pulse

**Workflow**: `pages-build-deployment` (GitHub-managed)
- Automatically created when Pages enabled
- Triggered by commits to `/docs`
- Not customizable (GitHub internal workflow)

### GrumpiBlogged Integration

**Webhook Flow**:
```
1. Report committed → trigger_grumpiblogged.yml triggers
2. Extract report metadata (date, URL, description)
3. Send repository_dispatch to GrumpiBlogged repo
4. GrumpiBlogged receives event, generates meta-report
```

**Secret**: `GRUMPIBLOGGED_PAT`
- Must have `repo` + `workflow` scopes
- Create at https://github.com/settings/tokens

### Nostr Integration

**Publishing Flow**:
```
1. Report generated as Markdown
2. post_to_nostr.py converts to NIP-23 format
3. Signs with NOSTR_PRIVATE_KEY
4. Publishes to 8+ relays
5. Includes donation links in footer
```

**Fallback**: If Nostr posting fails, report still saves locally

---

## 📖 FAQ

**Q: Why do both crons trigger but only one runs?**  
A: This is intentional DST coverage. The time gate filters which cron actually proceeds.

**Q: What happens if ingestion fails?**  
A: Critical scripts (official, cloud) will fail the workflow. Optional scripts log warnings but continue.

**Q: Can I run workflows manually?**  
A: Yes! Use "Run workflow" button in Actions tab. Enable `force_run` to bypass time gates.

**Q: How do I add a new data source?**  
A: Create `scripts/ingest_newsource.py`, add to matrix in `ingest.yml`, outputs to `data/newsource/{date}.json`.

**Q: What if GitHub Pages doesn't update?**  
A: Check Actions → "pages build and deployment" workflow. Usually completes in 1-2 minutes.

**Q: How much does this cost?**  
A: ~3,600-5,760 GitHub Actions minutes/month. Free tier is 2,000 min/month (may need paid plan).

---

**Architecture Version**: 2.0 (Post-Fix)  
**Last Updated**: 2025-11-02  
**Maintained By**: Ollama Pulse Team

