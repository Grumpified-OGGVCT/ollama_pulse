# 📡 Ollama Pulse

**A Complete, Self-Sustaining Innovation Miner Built on GitHub**

Ollama Pulse is a GitHub-native ecosystem radar that continuously scans the Ollama world for signals, mines patterns, and generates actionable intelligence—all without servers or costs beyond GitHub's free tier.

## 🎯 What It Does

- **Polls Sources**: Ollama blog RSS, /cloud page, X/Twitter, Reddit, Product Hunt, community tools
- **Mines Insights**: Uses embeddings + clustering to detect patterns and trends
- **Infers Implications**: Applies heuristics to extrapolate "what's next"
- **Generates Reports**: Creates comprehensive 10K-50K word Markdown reports
- **Auto-Deploys**: Publishes to GitHub Pages as a live "blog"
- **Zero Maintenance**: Runs forever on GitHub Actions (2,000 free minutes/month)

## 🏗️ Architecture

```
ollama_pulse/
├── .github/workflows/
│   └── ingest.yml          # Hourly automation (cron)
├── scripts/
│   ├── ingest_official.py  # Blog RSS, /cloud page
│   ├── ingest_community.py # X/Twitter, Reddit, Product Hunt
│   ├── ingest_tools.py     # n8n, GitHub integrations
│   ├── aggregate.py        # Merge daily JSONs
│   ├── mine_insights.py    # Embeddings + clustering
│   └── generate_report.py  # Markdown templating
├── data/
│   ├── official/           # {date}.json from blog/cloud
│   ├── community/          # {date}.json from social
│   ├── tools/              # {date}.json from integrations
│   ├── aggregated/         # {date}.json merged
│   └── insights/           # {date}.json mined patterns
├── reports/
│   └── pulse-{date}.md     # Generated reports (deployed to Pages)
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Grumpified-OGGVCT/ollama_pulse.git
cd ollama_pulse
pip install -r requirements.txt
```

### 2. Enable GitHub Actions
- Go to Settings → Actions → General
- Enable "Read and write permissions"

### 3. Enable GitHub Pages
- Go to Settings → Pages
- Source: main branch, Folder: /reports

### 4. Test Locally
```bash
python scripts/ingest_official.py
python scripts/aggregate.py
python scripts/mine_insights.py
python scripts/generate_report.py
```

## 📊 Example Output

**From October 22, 2025:**

```markdown
📅 Ollama Cloud Pulse – 2025-10-22

### 🚀 New Cloud Service Changes
| Date | Change | Details |
|------|--------|---------|
| 2025-10-16 | New models | GLM-4.6-cloud, Qwen3-Coder-480B-cloud |

### 🛠️ New Community Tools
| Tool | Integration | Why It Matters |
|------|-------------|----------------|
| n8n Ollama Node | No-code workflows | Automates Cloud queries |

### 📈 Emerging Patterns
- Multimodal Cloud Hybrids (Qwen3-VL + voice STT)
- No-Code Wrappers (n8n/Zapier + Ollama Cloud)

### 🔔 Inferences
- Multimodal exists → Feasible: Low-latency vision agents
- High density in coding models → Alert: Test GLM-4.6
```

## 🔗 Integration with Ollama Proxy

Access via: `http://127.0.0.1:8081/admin/pulse`

## 📄 License

MIT License

---

**Live Dashboard**: https://grumpified-oggvct.github.io/ollama_pulse  
**Repository**: https://github.com/Grumpified-OGGVCT/ollama_pulse

