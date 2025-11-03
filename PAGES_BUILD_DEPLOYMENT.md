# GitHub Pages Build & Deployment - Configuration Guide

**About**: The `pages-build-deployment` workflow you see in the Actions tab is **automatically created and managed by GitHub** when you enable GitHub Pages. You cannot and should not edit this workflow.

---

## 🎯 What is pages-build-deployment?

This is a **GitHub-internal workflow** that:
- Triggers automatically when you push to `/docs` folder
- Builds static site using Jekyll (if configured)
- Deploys to GitHub Pages CDN
- Completes in 1-2 minutes

**You cannot**:
- Edit this workflow (no .yml file in your repo)
- Disable this workflow (it's part of Pages service)
- Customize the build process (managed by GitHub)

**You can**:
- Change Pages settings (branch, folder)
- Add Jekyll config (_config.yml)
- Monitor deployment status in Actions tab

---

## ✅ Verify GitHub Pages Configuration

### Step 1: Check Pages Settings

1. Go to: https://github.com/Grumpified-OGGVCT/ollama_pulse/settings/pages

2. Verify these settings:

**Source**:
- ✅ Deploy from a branch (not GitHub Actions)
- ✅ Branch: `main`
- ✅ Folder: `/docs`

**Custom domain**: (leave empty unless you have one)

**Enforce HTTPS**: ✅ Enabled (recommended)

3. Save if you made changes

### Step 2: Verify Site is Live

1. URL: https://grumpified-oggvct.github.io/ollama_pulse
2. Should show: Ollama Pulse index page with reports
3. Click any report link: Should load full report

If site not accessible:
- Wait 1-2 minutes after enabling Pages
- Check Actions tab for "pages build and deployment" workflow
- Verify workflow succeeded (green checkmark)

---

## 🔍 How to Monitor Pages Deployment

### View Deployment Status

1. Go to: https://github.com/Grumpified-OGGVCT/ollama_pulse/actions
2. Look for: "pages build and deployment" workflows
3. These trigger automatically after commits to `docs/**`

### Recent Deployments

```
Actions → Filter by "pages build and deployment"
  ↓
Shows all automatic deployments
  ↓
Click any run to see build logs
  ↓
Should complete in 30-120 seconds
```

### Deployment Timeline

```
Commit to docs/** → Triggers pages-build-deployment
                              ↓
                      Jekyll builds site
                              ↓
                      Validates HTML/CSS
                              ↓
                      Deploys to CDN
                              ↓
                      Site live (~1-2 min total)
```

---

## 🛠️ Customization Options

While you can't edit the deployment workflow, you can customize the **site build**:

### Option 1: Add Jekyll Configuration

Create `docs/_config.yml`:

```yaml
title: Ollama Pulse
description: Daily Ecosystem Intelligence
theme: minima  # or any GitHub-supported theme
markdown: kramdown
highlighter: rouge

# Optional: Custom nav
navigation:
  - title: Home
    url: /
  - title: Latest Report
    url: /reports/
```

### Option 2: Add Custom CSS

Create `docs/assets/css/style.scss`:

```scss
---
---

@import "{{ site.theme }}";

// Custom styles here
body {
  background: #0f172a;
  color: #e2e8f0;
}
```

### Option 3: Add Jekyll Layouts

Create `docs/_layouts/default.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ page.title }} - Ollama Pulse</title>
  <!-- Your custom head content -->
</head>
<body>
  {{ content }}
</body>
</html>
```

---

## 🐛 Troubleshooting Pages

### Issue: Site Not Loading

**Check**:
1. Pages enabled in settings?
2. Correct branch (main) and folder (/docs)?
3. Recent deployment workflow succeeded?

**Solution**:
```powershell
# Trigger a manual commit to docs/
cd "C:\Users\gerry\OLLAMA PROXY\Grumpified-ollama_pulse"
echo "<!-- Force rebuild -->" >> docs/index.html
git add docs/index.html
git commit -m "chore: trigger pages rebuild"
git push origin main
```

### Issue: "404 Not Found"

**Causes**:
- Pages not enabled
- Wrong folder configured
- Jekyll build errors

**Solution**:
1. Go to Settings → Pages
2. Verify Source: main branch, /docs folder
3. Check latest "pages build and deployment" run for errors

### Issue: "Deployment Failed"

**Check**:
1. Actions tab → "pages build and deployment"
2. Click failed run → Read error logs
3. Common issues:
   - Invalid markdown syntax
   - Missing front matter
   - Broken links

**Solution**:
```powershell
# Validate markdown locally
gem install jekyll bundler
cd docs
jekyll build
# Fix any errors shown
```

---

## 📊 Expected Behavior

### After Each Report Commit

```
1. Workflow commits to docs/reports/pulse-{date}.md
                ↓
2. pages-build-deployment automatically triggers
                ↓
3. Jekyll builds site (30-60 sec)
                ↓
4. Deploys to GitHub Pages CDN (30-60 sec)
                ↓
5. Site updates at grumpified-oggvct.github.io/ollama_pulse
                ↓
6. Total time: 1-2 minutes from commit to live
```

### Typical Day

```
08:30 CT: Morning report commits
08:31 CT: Pages deployment triggers
08:33 CT: Morning report live on site

16:30 CT: Afternoon report commits
16:31 CT: Pages deployment triggers
16:33 CT: Afternoon report live on site

Hourly: Ingestion commits (doesn't trigger Pages unless docs/* changed)
```

---

## 🔍 Verify Everything Works

### Quick Health Check

```bash
# 1. Check if Pages is enabled
curl -I https://grumpified-oggvct.github.io/ollama_pulse
# Should return: HTTP/2 200

# 2. Check latest report exists
curl https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-$(date -u '+%Y-%m-%d')
# Should return: HTML content

# 3. Check index page
curl https://grumpified-oggvct.github.io/ollama_pulse/
# Should return: Report listing
```

### Visual Verification

1. Open: https://grumpified-oggvct.github.io/ollama_pulse
2. See: Index page with report cards
3. Click: Any report link
4. See: Full EchoVein report with styling
5. Verify: QR codes display correctly
6. Test: Social sharing links work

---

## 🎯 Key Takeaways

✅ **pages-build-deployment is AUTOMATIC** - don't try to edit it  
✅ **Triggers on ANY commit to docs/**  - reports, index, assets  
✅ **Uses Jekyll to build site** - supports themes and layouts  
✅ **Deploys in 1-2 minutes** - fast CDN propagation  
✅ **Free and unlimited** - no cost for hosting  

**Your workflows commit → Pages auto-deploys → Done!**

---

## 📚 Further Reading

- **Jekyll Documentation**: https://jekyllrb.com/docs/
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Supported Themes**: https://pages.github.com/themes/
- **Custom Domains**: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

---

**Status**: ✅ No configuration needed for pages-build-deployment  
**Action**: Just verify Pages is enabled in repository settings  
**Result**: Automatic deployment of all report commits

