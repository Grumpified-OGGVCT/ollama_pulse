# 📚 Ollama Pulse - Comprehensive Documentation

**Version**: 2.0 (2025-10-26)  
**Status**: Production Ready  
**Maintainer**: Grumpified OGGVCT

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Data Sources (16 Total)](#data-sources)
4. [Workflows & Automation](#workflows--automation)
5. [Manual Tracking System](#manual-tracking-system)
6. [Report Generation](#report-generation)
7. [Integration Points](#integration-points)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance](#maintenance)
10. [Future Enhancements](#future-enhancements)

---

## 1. Overview

### What is Ollama Pulse?

Ollama Pulse is a **GitHub-native ecosystem intelligence platform** that continuously monitors the Ollama ecosystem across 16 data sources, mines patterns using AI, and generates actionable daily reports with the EchoVein persona.

### Key Features

- ✅ **16 Data Sources**: Official, community, bounties, Nostr, and manual tracking
- ✅ **Turbo-Centric Scoring**: Every item scored for Ollama Turbo/Cloud relevance (0-1 scale)
- ✅ **AI-Powered Insights**: Embeddings + clustering for pattern detection
- ✅ **EchoVein Persona**: 4 adaptive report styles based on daily patterns
- ✅ **Automated Publishing**: GitHub Pages + Nostr NIP-23 integration
- ✅ **Zero Infrastructure**: Runs entirely on GitHub Actions (free tier)
- ✅ **Manual Tracking**: Add projects via simple JSON file
- ✅ **GrumpiBlogged Integration**: Webhook triggers for meta-blogging

### Architecture Philosophy

**Event-Driven, Modular, Extensible**

- Each data source is an independent ingestion script
- Aggregation layer merges and scores all data
- Mining layer detects patterns and generates insights
- Report generation adapts tone based on patterns
- Publishing layer distributes to multiple channels

---

## 2. Architecture

### Directory Structure

```
ollama_pulse/
├── .github/workflows/          # GitHub Actions automation
│   ├── ingest.yml             # Hourly data collection (all 16 sources)
│   ├── morning_report.yml     # 08:30 AM CT report generation
│   ├── afternoon_report.yml   # 04:30 PM CT report generation
│   ├── reusable-ingest.yml    # Shared ingestion workflow
│   └── trigger_grumpiblogged.yml  # Webhook to GrumpiBlogged
│
├── scripts/                    # Python ingestion & processing
│   ├── ingest_official.py     # Ollama blog RSS
│   ├── ingest_cloud.py        # Ollama Cloud API
│   ├── ingest_community.py    # Reddit, HN, YouTube, HuggingFace
│   ├── ingest_issues.py       # GitHub Issues/PRs
│   ├── ingest_tools.py        # n8n, GitHub integrations
│   ├── ingest_bounties.py     # Bounty platforms
│   ├── ingest_nostr.py        # Nostr NIP-23 content
│   ├── ingest_stackoverflow.py # Stack Overflow questions
│   ├── ingest_model_registry.py # Ollama model registry
│   ├── ingest_releases.py     # GitHub releases
│   ├── ingest_devblogs.py     # Developer blogs
│   ├── ingest_discord.py      # Discord discussions
│   ├── ingest_manual.py       # Manual tracking (tracked_projects.json)
│   ├── aggregate.py           # Merge all sources + Turbo scoring
│   ├── mine_insights.py       # Pattern detection + clustering
│   ├── generate_report.py     # EchoVein report generation
│   └── post_to_nostr.py       # Publish to Nostr network
│
├── data/                       # JSON data storage
│   ├── official/              # {date}.json from blog/cloud
│   ├── community/             # {date}.json from social sources
│   ├── tools/                 # {date}.json from integrations
│   ├── bounties/              # {date}.json from bounty platforms
│   ├── nostr/                 # {date}.json from Nostr
│   ├── manual/                # {date}.json from manual tracking
│   ├── aggregated/            # {date}.json with turbo_scores
│   └── insights/              # {date}.json + {date}_yield.json
│
├── docs/                       # GitHub Pages site
│   ├── index.html             # Modern frontend with search/calendar
│   ├── reports/               # Generated reports (pulse-{date}.md)
│   └── assets/                # CSS, JS, images
│
├── assets/                     # Donation QR codes
│   ├── KofiTipQR_Code_GrumpiFied.png
│   └── lightning_wallet_QR_Code.png
│
├── tracked_projects.json       # Manual tracking configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Main documentation
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    HOURLY INGESTION                         │
│  (16 parallel scripts run every hour via GitHub Actions)   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATA AGGREGATION                          │
│  • Merge all sources into unified JSON                     │
│  • Apply Turbo-centric scoring (0-1 scale)                 │
│  • Filter items with score ≥ 0.3                           │
│  • Calculate yield metrics                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   INSIGHTS MINING                           │
│  • Generate embeddings (sentence-transformers)             │
│  • Cluster patterns (KMeans)                               │
│  • Detect trends (≥5 items = "Vein Bulging")              │
│  • Generate dynamic search queries                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  REPORT GENERATION                          │
│  • Select EchoVein mode (Vein Rush, Artery Audit, etc.)   │
│  • Generate markdown report                                │
│  • Add developer insights section                          │
│  • Include donation links                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    PUBLISHING                               │
│  • Commit to docs/reports/pulse-{date}.md                  │
│  • GitHub Pages auto-deploys                               │
│  • Post to Nostr network (NIP-23)                          │
│  • Trigger GrumpiBlogged webhook                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Data Sources (16 Total)

### Official Sources (3)

| Source | Script | Frequency | Description |
|--------|--------|-----------|-------------|
| **Ollama Blog** | `ingest_official.py` | Hourly | RSS feed from ollama.com/blog |
| **Ollama Cloud** | `ingest_cloud.py` | Hourly | /cloud page scraping + API |
| **GitHub Releases** | `ingest_releases.py` | Hourly | ollama/ollama releases |

### Community Sources (7)

| Source | Script | Frequency | Description |
|--------|--------|-----------|-------------|
| **Reddit** | `ingest_community.py` | Hourly | r/ollama subreddit |
| **GitHub Issues** | `ingest_issues.py` | Hourly | Issues/PRs search |
| **Hacker News** | `ingest_community.py` | Hourly | Algolia API |
| **YouTube** | `ingest_community.py` | Hourly | RSS feed |
| **HuggingFace** | `ingest_community.py` | Hourly | Discussions |
| **Stack Overflow** | `ingest_stackoverflow.py` | Hourly | Tagged questions |
| **Discord** | `ingest_discord.py` | Hourly | Server discussions |

### Integration Sources (2)

| Source | Script | Frequency | Description |
|--------|--------|-----------|-------------|
| **n8n** | `ingest_tools.py` | Hourly | Workflow templates |
| **GitHub Code** | `ingest_tools.py` | Hourly | Code search |

### Bounty & Decentralized (2)

| Source | Script | Frequency | Description |
|--------|--------|-----------|-------------|
| **Bounties** | `ingest_bounties.py` | Hourly | Bountycaster, etc. |
| **Nostr** | `ingest_nostr.py` | Hourly | NIP-23 long-form |

### Specialized Sources (2)

| Source | Script | Frequency | Description |
|--------|--------|-----------|-------------|
| **Model Registry** | `ingest_model_registry.py` | Hourly | Ollama model library |
| **Dev Blogs** | `ingest_devblogs.py` | Hourly | Developer blogs RSS |

### Manual Tracking (1)

| Source | Script | Frequency | Description |
|--------|--------|-----------|-------------|
| **Manual** | `ingest_manual.py` | Hourly | tracked_projects.json |

---

## 4. Workflows & Automation

### Hourly Ingestion (`ingest.yml`)

**Schedule**: Every hour  
**Duration**: ~5-10 minutes  
**Actions**:
1. Install Python dependencies
2. Run all 16 ingestion scripts in parallel
3. Run aggregation (`aggregate.py`)
4. Run insights mining (`mine_insights.py`)
5. Commit data to repository

### Morning Report (`morning_report.yml`)

**Schedule**: 08:30 AM Central Time  
**Duration**: ~3-5 minutes  
**Actions**:
1. Generate report (`generate_report.py`)
2. Publish to GitHub Pages
3. Post to Nostr network
4. Trigger GrumpiBlogged webhook

### Afternoon Report (`afternoon_report.yml`)

**Schedule**: 04:30 PM Central Time  
**Duration**: ~3-5 minutes  
**Actions**: Same as morning report

### GrumpiBlogged Trigger (`trigger_grumpiblogged.yml`)

**Trigger**: On push to `docs/reports/pulse-*.md`  
**Actions**:
1. Send `repository_dispatch` event to GrumpiBlogged
2. Include report URL and metadata in payload

---

## 5. Manual Tracking System

### Overview

The manual tracking system allows you to add projects to daily reports without waiting for automated discovery.

### How to Use

1. **Edit `tracked_projects.json`** in the repository root
2. **Add your project** to the `projects` array
3. **Commit and push** to GitHub
4. **Wait for next report** (08:30 AM or 04:30 PM CT)

### Example Entry

```json
{
  "title": "My Awesome Ollama Project",
  "url": "https://github.com/user/awesome-ollama",
  "summary": "A revolutionary Ollama integration for XYZ",
  "turbo_score": 0.9,
  "highlights": ["integration", "production-ready", "typescript"]
}
```

### Field Reference

- **title** (required): Project name
- **url** (required): Project URL
- **summary** (required): Brief description (1-2 sentences)
- **turbo_score** (optional): Relevance score 0-1 (default: 0.8)
- **highlights** (optional): Tags/keywords array
- **date** (optional): ISO date string (default: today)
- **source** (optional): Source identifier (default: "manual_tracking")

### Best Practices

✅ **DO**:
- Add projects you're actively working on
- Use descriptive titles
- Set appropriate turbo_score (0.8-1.0 for high-quality)
- Keep summaries concise

❌ **DON'T**:
- Add spam or unrelated projects
- Duplicate automated entries
- Set turbo_score below 0.5 (won't appear in reports)

**Full Guide**: See `MANUAL_TRACKING_GUIDE.md`

---

## 6. Report Generation

### EchoVein Persona

Reports use the **EchoVein** persona - a vein-tapping oracle that adapts tone based on daily patterns.

### 4 Adaptive Modes

1. **Vein Rush** (🩸) - High-density surge (3+ voice/multimodal items)
   - Electric, prophetic, hyped about the flow

2. **Artery Audit** (⚙️) - Steady maintenance (incremental tools/fixes)
   - Grounded, practical, appreciative of "essential grime"

3. **Fork Phantom** (🤖) - Niche oddities (zero-star experimental hacks)
   - Playful, probing, unpacking weirdness with "what if" veins

4. **Deep Vein Throb** (📍) - Slow days (aggregated trends)
   - Reflective, prospector mode, weekly artery forecasting

### Report Structure

```markdown
# 🩸 Ollama Pulse - {Date}

## 🎯 Official Veins
- Ollama blog updates
- Cloud API changes
- GitHub releases

## 🛠️ Community Veins
- Reddit discussions
- GitHub Issues/PRs
- Stack Overflow questions
- Discord conversations

## 💰 Bounty Veins
- Active bounties
- Reward opportunities

## 🌐 Nostr Veins
- Decentralized content (NIP-23)

## 📈 Vein Pattern Mapping
- Detected trends
- Clustering results
- Pattern commentary

## 🔔 Prophetic Veins
- Confidence-scored inferences
- Trend predictions

## 🚀 Developer Focus
- What to build
- How to leverage
- Problems solved
- New capabilities

## 💰 Support the Vein Network
- Ko-fi donation link
- Lightning Network addresses
- QR codes

## 🩸 Lingo Legend
- EchoVein terminology decoder
```

---

## 7. Integration Points

### GrumpiBlogged Integration

**Purpose**: Meta-blogging platform that translates Ollama Pulse reports into human-readable content

**Webhook Flow**:
1. Ollama Pulse generates report
2. Commits to `docs/reports/pulse-{date}.md`
3. Triggers `trigger_grumpiblogged.yml` workflow
4. Sends `repository_dispatch` event to GrumpiBlogged
5. GrumpiBlogged fetches report and transforms it

**Payload Structure**:
```json
{
  "event_type": "ollama-pulse-update",
  "client_payload": {
    "report_url": "https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-2025-10-26.md",
    "date": "2025-10-26",
    "source": "ollama_pulse"
  }
}
```

### Nostr Integration

**Purpose**: Decentralized publishing to Nostr network

**Features**:
- Auto-publishes daily reports as NIP-23 long-form content
- Tags: `#ollama`, `#ai`, `#echovein`
- Includes donation links in footer
- Publishes to 8+ relays

**Nostr Account**:
- **npub**: `npub1grumpifiedoggvct...`
- **Profile**: EchoVein Oracle - Vein-tapping oracle excavating Ollama's hidden arteries

---

## 8. Troubleshooting

### Common Issues

#### 1. Workflow Failures

**Symptom**: GitHub Actions workflow fails  
**Causes**:
- API rate limits
- Network timeouts
- Invalid JSON in tracked_projects.json

**Solutions**:
- Check workflow logs in GitHub Actions tab
- Verify API keys in repository secrets
- Validate JSON syntax: `python -m json.tool tracked_projects.json`

#### 2. Manual Tracking Not Appearing

**Symptom**: Projects in tracked_projects.json don't appear in reports  
**Causes**:
- turbo_score too low (< 0.3)
- JSON syntax error
- Workflow hasn't run yet

**Solutions**:
- Set turbo_score ≥ 0.8 for manual entries
- Validate JSON syntax
- Wait for next scheduled report (08:30 AM or 04:30 PM CT)

#### 3. Empty Reports

**Symptom**: Reports generated but contain no data  
**Causes**:
- All sources returned 0 entries
- Turbo-score filtering too aggressive
- Data ingestion failures

**Solutions**:
- Check `data/aggregated/{date}.json` for raw data
- Review `data/insights/{date}_yield.json` for yield metrics
- Lower turbo_score threshold in `aggregate.py` (line 45)

---

## 9. Maintenance

### Regular Tasks

**Daily**:
- ✅ Review generated reports for quality
- ✅ Check GitHub Actions for failures
- ✅ Monitor yield metrics in `data/insights/`

**Weekly**:
- ✅ Review and update `tracked_projects.json`
- ✅ Check for new data sources to add
- ✅ Update dependencies: `pip install -r requirements.txt --upgrade`

**Monthly**:
- ✅ Archive old data (optional)
- ✅ Review and optimize ingestion scripts
- ✅ Update documentation

### Monitoring

**Key Metrics**:
- **Yield Ratio**: High-relevance items / Total items (target: ≥ 0.3)
- **Source Coverage**: Number of active sources (target: 16/16)
- **Report Frequency**: 2 reports/day (08:30 AM, 04:30 PM CT)

**Check Yield**:
```bash
cat data/insights/$(date +%Y-%m-%d)_yield.json
```

---

## 10. Future Enhancements

### Planned Features

- [ ] **AI-Powered Summarization**: Use LLM to generate executive summaries
- [ ] **Sentiment Analysis**: Track community sentiment over time
- [ ] **Trend Forecasting**: Predict future patterns using historical data
- [ ] **Email Notifications**: Send daily digest to subscribers
- [ ] **Slack/Discord Integration**: Post reports to team channels
- [ ] **API Endpoint**: Expose data via REST API
- [ ] **Mobile App**: Native iOS/Android app for reports
- [ ] **RSS Feed**: Subscribe to reports via RSS

### Contribution Guidelines

See `CONTRIBUTING.md` for details on how to contribute.

---

**Last Updated**: 2025-10-26  
**Version**: 2.0  
**Status**: Production Ready  
**Maintainer**: Grumpified OGGVCT  
**License**: MIT

