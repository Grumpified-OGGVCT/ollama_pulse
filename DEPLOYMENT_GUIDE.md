# 🚀 Ollama Pulse Deployment Guide

Complete step-by-step guide to deploy Ollama Pulse to GitHub.

## 📋 Prerequisites

- GitHub account (Grumpified-OGGVCT)
- Git installed locally
- Python 3.11+ installed
- Repository: https://github.com/Grumpified-OGGVCT/ollama_pulse

## 🔧 Step 1: Clone and Setup

```powershell
# Navigate to workspace
cd "C:\Users\gerry"

# Clone the repository
git clone https://github.com/Grumpified-OGGVCT/ollama_pulse.git
cd ollama_pulse

# Copy all files from ollama_pulse_repo to this directory
# (Files are in C:\Users\gerry\OLLAMA PROXY\ollama_pulse_repo)
```

## 📁 Step 2: Copy Files

Copy these files from `C:\Users\gerry\OLLAMA PROXY\ollama_pulse_repo\` to the cloned repository:

```
ollama_pulse/
├── README.md
├── DEPLOYMENT_GUIDE.md
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ingest.yml
├── scripts/
│   ├── ingest_official.py
│   ├── ingest_community.py
│   ├── ingest_tools.py
│   ├── aggregate.py
│   ├── mine_insights.py
│   └── generate_report.py
├── data/
│   ├── official/.gitkeep
│   ├── community/.gitkeep
│   ├── tools/.gitkeep
│   ├── aggregated/.gitkeep
│   └── insights/.gitkeep
└── reports/
    └── .gitkeep
```

## 🔑 Step 3: Configure GitHub

### Enable GitHub Actions

1. Go to https://github.com/Grumpified-OGGVCT/ollama_pulse/settings/actions
2. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests
3. Click "Save"

### Enable GitHub Pages

1. Go to https://github.com/Grumpified-OGGVCT/ollama_pulse/settings/pages
2. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/reports**
3. Click "Save"

## 📦 Step 4: Create .gitkeep Files

```powershell
# Create empty .gitkeep files to preserve directory structure
New-Item -ItemType File -Path "data/official/.gitkeep" -Force
New-Item -ItemType File -Path "data/community/.gitkeep" -Force
New-Item -ItemType File -Path "data/tools/.gitkeep" -Force
New-Item -ItemType File -Path "data/aggregated/.gitkeep" -Force
New-Item -ItemType File -Path "data/insights/.gitkeep" -Force
New-Item -ItemType File -Path "reports/.gitkeep" -Force
```

## 🚀 Step 5: Initial Commit and Push

```powershell
# Add all files
git add .

# Commit
git commit -m "Initial Ollama Pulse setup - complete ecosystem miner"

# Push to GitHub
git push origin main
```

## ✅ Step 6: Test Workflow

### Manual Trigger

1. Go to https://github.com/Grumpified-OGGVCT/ollama_pulse/actions
2. Click "Ollama Pulse Ingestion" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for completion (~2-3 minutes)

### Verify Output

1. Check the Actions tab for green checkmark
2. Navigate to https://github.com/Grumpified-OGGVCT/ollama_pulse/tree/main/data
3. Verify JSON files were created in:
   - `data/official/`
   - `data/community/`
   - `data/tools/`
   - `data/aggregated/`
   - `data/insights/`
4. Check `reports/` for generated Markdown

## 🌐 Step 7: Verify GitHub Pages

1. Wait 2-3 minutes for Pages to deploy
2. Visit: https://grumpified-oggvct.github.io/ollama_pulse
3. You should see the generated report!

## 🔗 Step 8: Test Ollama Proxy Integration

1. Start Ollama Proxy:
   ```powershell
   cd "C:\Users\gerry\OLLAMA PROXY"
   .\venv\Scripts\Activate.ps1
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8081
   ```

2. Open browser: http://127.0.0.1:8081/admin/pulse

3. Verify:
   - ✅ Menu item "📡 Ollama Pulse" appears in sidebar
   - ✅ Dashboard loads with stats cards
   - ✅ GitHub Pages iframe shows report
   - ✅ API key is displayed
   - ✅ Refresh button works

## 📅 Step 9: Verify Automation

The workflow runs **every hour** automatically via cron:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour at :00
```

**Next run**: Check Actions tab at the top of the next hour

## 🐛 Troubleshooting

### Workflow Fails

1. Check Actions tab for error logs
2. Common issues:
   - Missing dependencies → Check requirements.txt
   - Permission denied → Verify workflow permissions
   - API rate limits → Add delays in scripts

### GitHub Pages Not Updating

1. Check Settings → Pages is enabled
2. Verify `/reports` folder has content
3. Wait 2-3 minutes for deployment
4. Check Actions tab for "pages build and deployment" workflow

### No Data Generated

1. Run scripts locally first:
   ```powershell
   python scripts/ingest_official.py
   python scripts/aggregate.py
   python scripts/mine_insights.py
   python scripts/generate_report.py
   ```
2. Check for errors
3. Verify internet connection
4. Check API rate limits

## 📊 Monitoring

### Check Workflow Status

```powershell
# View latest workflow run
gh run list --repo Grumpified-OGGVCT/ollama_pulse

# View workflow logs
gh run view --repo Grumpified-OGGVCT/ollama_pulse
```

### Check Data Growth

```powershell
# Count JSON files
Get-ChildItem -Path data -Recurse -Filter *.json | Measure-Object

# View latest report
Get-Content reports/pulse-$(Get-Date -Format yyyy-MM-dd).md
```

## 🎉 Success Criteria

- ✅ Repository has all files
- ✅ GitHub Actions enabled with write permissions
- ✅ GitHub Pages enabled and deployed
- ✅ Workflow runs successfully (green checkmark)
- ✅ Data files generated in `data/` folders
- ✅ Report generated in `reports/`
- ✅ GitHub Pages shows report at https://grumpified-oggvct.github.io/ollama_pulse
- ✅ Ollama Proxy integration works at http://127.0.0.1:8081/admin/pulse

## 🔄 Ongoing Maintenance

### Update Scripts

```powershell
# Edit scripts locally
code scripts/ingest_official.py

# Test locally
python scripts/ingest_official.py

# Commit and push
git add scripts/
git commit -m "Update ingestion logic"
git push
```

### Monitor Usage

- GitHub Actions: 2,000 free minutes/month
- Current usage: ~5 min/run × 24 runs/day = 120 min/day
- Monthly: ~3,600 minutes (well within limit)

### Add New Sources

1. Create new ingestion script in `scripts/`
2. Update `.github/workflows/ingest.yml` to call it
3. Test locally
4. Commit and push

## 📚 Resources

- **Repository**: https://github.com/Grumpified-OGGVCT/ollama_pulse
- **GitHub Pages**: https://grumpified-oggvct.github.io/ollama_pulse
- **Ollama Proxy**: http://127.0.0.1:8081/admin/pulse
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub Pages Docs**: https://docs.github.com/en/pages

---

**Last Updated**: 2025-10-22  
**Status**: Ready for deployment  
**Estimated Setup Time**: 15-20 minutes

