# Ollama Pulse Workflow Diagrams

**Visual guide to system architecture and data flow**

---

## 🔄 Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      OLLAMA PULSE ECOSYSTEM                         │
│                    Fully Automated Intelligence                      │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────── HOURLY INGESTION (Every :00 UTC) ─────────────────┐
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │         PARALLEL MATRIX STRATEGY (13 Jobs)                  │  │
│  │                                                              │  │
│  │  [Official] ────┐                                           │  │
│  │  [Cloud] ───────┤                                           │  │
│  │  [Community] ───┤                                           │  │
│  │  [Issues] ──────┤                                           │  │
│  │  [Tools] ───────┤                                           │  │
│  │  [Bounties] ────┤                                           │  │
│  │  [Nostr] ───────┼──→ Run in Parallel (2-4 min)             │  │
│  │  [StackOverflow]┤                                           │  │
│  │  [Models] ──────┤                                           │  │
│  │  [Releases] ────┤                                           │  │
│  │  [DevBlogs] ────┤                                           │  │
│  │  [Discord] ─────┤                                           │  │
│  │  [Manual] ──────┘                                           │  │
│  │                                                              │  │
│  │         ↓ (each uploads artifact)                           │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │         AGGREGATE JOB                                │   │  │
│  │  │  - Download all 13 artifacts                        │   │  │
│  │  │  - Combine data into single dataset                 │   │  │
│  │  │  - Apply Turbo scoring (0-1 relevance)              │   │  │
│  │  │  - Save to data/aggregated/{date}.json              │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                                                              │  │
│  │         ↓                                                    │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │         MINE INSIGHTS                                │   │  │
│  │  │  - ML embeddings (sentence-transformers)            │   │  │
│  │  │  - K-Means clustering (pattern detection)           │   │  │
│  │  │  - Heuristic inferences (prophecies)                │   │  │
│  │  │  - Save to data/insights/{date}.json                │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  │                                                              │  │
│  │         ↓                                                    │  │
│  │                                                              │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │         COMMIT & PUSH                                │   │  │
│  │  │  - Commit all data/** changes                       │   │  │
│  │  │  - Retry logic (3 attempts with backoff)            │   │  │
│  │  │  - Auto-resolve conflicts                           │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │         TURBO CLOUD DEEP SCAN (Optional)                    │  │
│  │  - Deep Ollama Cloud model analysis                         │  │
│  │  - GitHub code search for turbo mentions                    │  │
│  │  - Commit supplementary data                                │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘


┌──────────── MORNING REPORT (08:30 CT with DST) ────────────────────┐
│                                                                      │
│  ┌────────────── DUAL CRON TRIGGER ─────────────────┐              │
│  │  CDT: cron '30 13 * * *' (13:30 UTC = 08:30 CDT) │              │
│  │  CST: cron '30 14 * * *' (14:30 UTC = 08:30 CST) │              │
│  │  Both trigger → Time gate filters correct one     │              │
│  └───────────────────────────────────────────────────┘              │
│                           ↓                                         │
│  ┌─────────────── TIME GATE VALIDATION ───────────────┐            │
│  │  Check current time in America/Chicago timezone    │            │
│  │  If HOUR != 08 OR MINUTE not in [30-45]: SKIP      │            │
│  │  Else: PROCEED                                      │            │
│  └─────────────────────────────────────────────────────┘            │
│                           ↓                                         │
│  ┌──────────── DATA FRESHNESS VALIDATION ───────────────┐          │
│  │  Check git log for data commits in last 90 minutes   │          │
│  │  If found: FRESH (proceed)                            │          │
│  │  If not: Check if today's aggregated data exists     │          │
│  │    - Exists: STALE (proceed with warning)            │          │
│  │    - Missing: ABORT (cannot generate report)         │          │
│  └───────────────────────────────────────────────────────┘          │
│                           ↓                                         │
│  ┌─────────────── GENERATE REPORT ────────────────────┐            │
│  │  1. Load data from data/aggregated/{today}.json     │            │
│  │  2. Apply EchoVein persona (4 adaptive modes)       │            │
│  │  3. Generate docs/reports/pulse-{today}.md          │            │
│  │  4. Update docs/index.html (all reports)            │            │
│  └─────────────────────────────────────────────────────┘            │
│                           ↓                                         │
│  ┌─────────────── POST TO NOSTR (Optional) ──────────────┐         │
│  │  1. Convert report to NIP-23 format                    │         │
│  │  2. Sign with NOSTR_PRIVATE_KEY                        │         │
│  │  3. Broadcast to 8+ relays                             │         │
│  │  4. Continue on error (don't block report)             │         │
│  └────────────────────────────────────────────────────────┘         │
│                           ↓                                         │
│  ┌─────────────── COMMIT & DEPLOY ───────────────────┐             │
│  │  1. Commit docs/** with force-with-lease             │             │
│  │  2. Push to GitHub (triggers Pages deployment)       │             │
│  │  3. Upload artifact for debugging                    │             │
│  └──────────────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────────────┘

                            ↓ (on commit to docs/reports/)

┌──────────── GRUMPIBLOGGED TRIGGER (Event-Driven) ──────────────────┐
│                                                                      │
│  ┌──────────────── WEBHOOK VALIDATION ─────────────────┐           │
│  │  Check if GRUMPIBLOGGED_PAT secret exists            │           │
│  │  If missing: Log warning, skip webhook (graceful)    │           │
│  │  If present: Proceed with webhook                    │           │
│  └──────────────────────────────────────────────────────┘           │
│                           ↓                                         │
│  ┌──────────────── EXTRACT METADATA ───────────────────┐           │
│  │  - Get latest report file (ls -t)                    │           │
│  │  - Extract date from filename                        │           │
│  │  - Build report URL                                  │           │
│  │  - Extract 200-char description                      │           │
│  └──────────────────────────────────────────────────────┘           │
│                           ↓                                         │
│  ┌──────────────── SEND WEBHOOK ───────────────────────┐           │
│  │  POST repository_dispatch to GrumpiBlogged           │           │
│  │  Event: ollama-pulse-update                          │           │
│  │  Payload: {date, url, description, commit}           │           │
│  └──────────────────────────────────────────────────────┘           │
│                           ↓                                         │
│            [GrumpiBlogged receives and generates meta-report]       │
└──────────────────────────────────────────────────────────────────────┘


┌──────────── AFTERNOON REPORT (16:30 CT with DST) ──────────────────┐
│                                                                      │
│  (Identical flow to Morning Report, different timing)               │
│                                                                      │
│  CDT: cron '30 21 * * *' (21:30 UTC = 16:30 CDT)                   │
│  CST: cron '30 22 * * *' (22:30 UTC = 16:30 CST)                   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘


┌────────── GITHUB PAGES DEPLOYMENT (Automatic) ─────────────────────┐
│                                                                      │
│  Trigger: Any commit to docs/**                                     │
│  Managed by: GitHub (not customizable)                              │
│  Duration: 1-2 minutes                                              │
│                                                                      │
│  ┌──────────── PAGES BUILD ─────────────────┐                      │
│  │  1. Jekyll processes docs/                │                      │
│  │  2. Builds static HTML                    │                      │
│  │  3. Deploys to GitHub Pages CDN           │                      │
│  │  4. Live at grumpified-oggvct.github.io   │                      │
│  └───────────────────────────────────────────┘                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🌊 Data Flow Timeline

### Typical Day

```
00:00 CT ━━━━━━━━━━━━━━━━━━━━━┓
00:00 CT  Ingestion starts     ┃
00:02 CT  Parallel jobs finish ┃
00:04 CT  Aggregate complete   ┃
00:05 CT  Insights mined       ┃
00:06 CT  Data committed       ┣━━ [Data Available]
                                ┃
01:00 CT ━━━━━━━━━━━━━━━━━━━━━┫
01:00 CT  Ingestion starts     ┃
01:04 CT  Data committed       ┣━━ [Data Updated]
                                ┃
...continues every hour...      ┃
                                ┃
08:30 CT ━━━━━━━━━━━━━━━━━━━━━┫
08:30 CT  Morning report ◀─────┨ (reads latest data)
08:31 CT  Report published     ┃
08:32 CT  Pages deployed       ┃
08:33 CT  Webhook fired        ┣━━ [Morning Report Live]
                                ┃
...ingestion continues...       ┃
                                ┃
16:30 CT ━━━━━━━━━━━━━━━━━━━━━┫
16:30 CT  Afternoon report ◀───┨ (reads cumulative data)
16:31 CT  Report published     ┃
16:32 CT  Pages deployed       ┃
16:33 CT  Webhook fired        ┣━━ [Afternoon Report Live]
                                ┃
...cycle repeats daily...       ┃
```

---

## 🎯 Critical Path Analysis

### Ingestion Critical Path

```
CRITICAL SCRIPTS (must succeed):
├─ ingest_official.py (Blog, official updates) ────── Required
└─ ingest_cloud.py (Cloud/Turbo models) ─────────────── Required
                      ↓
              If either fails
                      ↓
           Workflow FAILS (exit 1)
              Can't proceed

OPTIONAL SCRIPTS (can fail):
├─ ingest_community.py ──┐
├─ ingest_issues.py ─────┤
├─ ingest_tools.py ──────┤
├─ ingest_bounties.py ───┤
├─ ingest_nostr.py ──────┼──→ Run in Parallel
├─ ingest_stackoverflow.py ┤
├─ ingest_model_registry.py ┤
├─ ingest_releases.py ───┤
├─ ingest_devblogs.py ───┤
├─ ingest_discord.py ────┤
└─ ingest_manual.py ─────┘
                      ↓
              If any fails
                      ↓
      Log WARNING (continue-on-error)
         Partial data collected
```

**Why This Design?**
- Official/Cloud data is CORE (must have)
- Community data is ENRICHMENT (nice to have)
- Partial success > total failure
- Graceful degradation maintains service

---

## ⏰ DST Transition Flow

### Spring Forward (March)

```
BEFORE DST CHANGE (CST = UTC-6):
┌────────────────────────────────────┐
│ 08:30 CST = 14:30 UTC              │
│                                    │
│ Cron '30 13' triggers → 07:30 CT   │ ❌ Too early (skips)
│ Cron '30 14' triggers → 08:30 CT   │ ✅ Correct (runs)
└────────────────────────────────────┘

        ↓ (DST changes at 2:00 AM)

AFTER DST CHANGE (CDT = UTC-5):
┌────────────────────────────────────┐
│ 08:30 CDT = 13:30 UTC              │
│                                    │
│ Cron '30 13' triggers → 08:30 CT   │ ✅ Correct (runs)
│ Cron '30 14' triggers → 09:30 CT   │ ❌ Too late (skips)
└────────────────────────────────────┘

RESULT: Automatic switch, no manual intervention
```

### Fall Back (November)

```
BEFORE DST CHANGE (CDT = UTC-5):
┌────────────────────────────────────┐
│ 08:30 CDT = 13:30 UTC              │
│                                    │
│ Cron '30 13' triggers → 08:30 CT   │ ✅ Correct (runs)
│ Cron '30 14' triggers → 09:30 CT   │ ❌ Too late (skips)
└────────────────────────────────────┘

        ↓ (DST changes at 2:00 AM)

AFTER DST CHANGE (CST = UTC-6):
┌────────────────────────────────────┐
│ 08:30 CST = 14:30 UTC              │
│                                    │
│ Cron '30 13' triggers → 07:30 CT   │ ❌ Too early (skips)
│ Cron '30 14' triggers → 08:30 CT   │ ✅ Correct (runs)
└────────────────────────────────────┘

RESULT: Automatic switch, no manual intervention
```

**Genius of Dual Cron**: Only ONE runs at any given time, determined by actual timezone offset!

---

## 🔄 Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING STRATEGY                       │
└─────────────────────────────────────────────────────────────────┘

INGESTION SCRIPT FAILS
        ↓
   Is it CRITICAL?
        ↓
    ┌───┴───┐
    │ YES   │ NO
    ↓       ↓
  Exit 1   Continue with warning
  (fail)   (log ::warning)
    ↓       ↓
Workflow  Other scripts continue
 stops    ↓
          Aggregate runs with
          partial data
          ↓
          Mine insights
          ↓
          Commit what we have
          ↓
    Partial success ✅


GIT PUSH FAILS
        ↓
   Attempt 1
        ↓
    Failed?
        ↓
    Wait 5s
        ↓
   Attempt 2
        ↓
    Failed?
        ↓
    Wait 5s
        ↓
   Attempt 3
        ↓
    Failed?
        ↓
  Exit with error
  (manual intervention)


NOSTR POSTING FAILS
        ↓
   Log warning
        ↓
  Continue workflow
        ↓
Report still saved
   to GitHub
        ↓
   Success ✅
   (Nostr optional)
```

---

## 📊 Concurrency Model

```
┌────────────── CONCURRENCY GROUPS ─────────────────┐
│                                                    │
│  ingestion:                                       │
│    group: ollama-pulse-ingestion                 │
│    cancel-in-progress: true                      │
│    ↓                                              │
│    Only 1 ingestion runs at a time               │
│    Old runs are cancelled when new one starts    │
│                                                   │
│  morning-report:                                 │
│    group: ollama-pulse-morning-report            │
│    cancel-in-progress: false                     │
│    ↓                                              │
│    Let current report finish before starting new │
│                                                   │
│  afternoon-report:                               │
│    group: ollama-pulse-afternoon-report          │
│    cancel-in-progress: false                     │
│    ↓                                              │
│    Let current report finish before starting new │
│                                                   │
│  grumpiblogged-trigger:                          │
│    group: trigger-grumpiblogged                  │
│    cancel-in-progress: true                      │
│    ↓                                              │
│    Only send latest webhook                      │
└────────────────────────────────────────────────────┘

WHY THESE SETTINGS?

Ingestion: cancel-in-progress = true
  → Prevents stacking (only care about latest data)

Reports: cancel-in-progress = false
  → Let reports finish (don't interrupt mid-generation)

Webhook: cancel-in-progress = true
  → Only need latest notification
```

---

## 🔐 Secrets Dependency Graph

```
┌──────────────────────────────────────────┐
│           ALL WORKFLOWS                  │
│         (Required for all)               │
├──────────────────────────────────────────┤
│  GH_PAT ━━━━━━━━━━━━━━━━━━┓             │
│  (GitHub Personal Access   ┃             │
│   Token for commits)       ┃             │
└────────────────────────────┻─────────────┘
                             ┃
                             ┣━━━━━━━━━━━━━━━━━━━━━┓
                             ↓                       ↓
        ┌────────────────────────────┐  ┌───────────────────────┐
        │   INGESTION + REPORTS      │  │ GRUMPIBLOGGED TRIGGER │
        │   (Core functionality)     │  │ (Optional integration)│
        ├────────────────────────────┤  ├───────────────────────┤
        │ OLLAMA_API_KEY ━━━━━━━━┓  │  │ GRUMPIBLOGGED_PAT     │
        │ (Ollama Cloud access)  ┃  │  │ (Webhook to meta-     │
        │                        ┃  │  │  report repo)         │
        │ SUPABASE_URL ──────────┃──┫  └───────────────────────┘
        │ SUPABASE_KEY           ┃  │           ↓
        │ (Optional: Database)   ┃  │    If missing:
        │                        ┃  │    Skip webhook
        │ NOSTR_PRIVATE_KEY ─────┃──┫    (continue)
        │ (Optional: Publishing) ┃  │
        └────────────────────────┻──┘
                    ↓
            Without OLLAMA_API_KEY:
            Ingestion/reports FAIL
                    ↓
            Without database/Nostr:
            Works fine (fallback to local)
```

---

## 📈 Performance Comparison

### Sequential vs Parallel Ingestion

```
BEFORE (Sequential):
00:00:00 ━━ Start
00:00:30 ━━ Script 1 done
00:01:00 ━━ Script 2 done
00:01:30 ━━ Script 3 done
00:02:00 ━━ Script 4 done
00:02:30 ━━ Script 5 done
00:03:00 ━━ Script 6 done
00:03:30 ━━ Script 7 done
00:04:00 ━━ Script 8 done
00:04:30 ━━ Script 9 done
00:05:00 ━━ Script 10 done
00:05:30 ━━ Script 11 done
00:06:00 ━━ Script 12 done
00:06:30 ━━ Script 13 done
00:07:00 ━━ Aggregate
00:08:00 ━━ Insights
00:08:30 ━━ Commit
00:09:00 ━━ Done
         ↑
    9 minutes total

AFTER (Parallel Matrix):
00:00:00 ━━ Start (13 jobs simultaneously)
00:00:30 ━━ Scripts 1-13 all running...
00:01:00 ━━ Scripts 1-13 all running...
00:01:30 ━━ Scripts 1-13 finishing...
00:02:00 ━━ All done, artifacts uploaded
00:02:30 ━━ Aggregate (download artifacts)
00:03:00 ━━ Insights
00:03:30 ━━ Commit
00:04:00 ━━ Done
         ↑
    4 minutes total

IMPROVEMENT: 56% faster (9 min → 4 min)
```

---

## 🎯 Quick Status Check

### How to Know Everything is Working

```bash
# Check latest ingestion
https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/ingest.yml
Status: ✅ Green = Good, ❌ Red = Check logs

# Check morning report
https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/morning_report.yml
Last run: Should be today at ~08:30 CT

# Check afternoon report
https://github.com/Grumpified-OGGVCT/ollama_pulse/actions/workflows/afternoon_report.yml
Last run: Should be today at ~16:30 CT

# Check live site
https://grumpified-oggvct.github.io/ollama_pulse
Updated: Should show today's date
```

---

**Read EXECUTIVE_SUMMARY.md first, then dive into technical docs as needed!** 📚

