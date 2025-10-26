# 🎯 GrumpiBlogged Upgrade Plan - Complete Ecosystem Map

**Created**: 2025-10-26  
**Status**: READY TO EXECUTE  
**Context**: Transitioning from Ollama Pulse (completed) to GrumpiBlogged (next)

---

## 📊 **THE COMPLETE ECOSYSTEM**

### **Three Interconnected Repositories**

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRUMPIBLOGGED ECOSYSTEM                       │
│                  (Meta-Aggregator & Publisher)                   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │                   │
         ┌──────────▼─────────┐  ┌─────▼──────────────┐
         │   OLLAMA PULSE     │  │ AI RESEARCH DAILY  │
         │   (EchoVein)       │  │  (The Scholar)     │
         │   08:30 + 16:30 CT │  │    08:05 CT        │
         └────────────────────┘  └────────────────────┘
```

---

## 🏗️ **REPOSITORY DETAILS**

### **1. Ollama Pulse** ✅ COMPLETE
- **URL**: https://github.com/Grumpified-OGGVCT/ollama_pulse
- **Live Site**: https://grumpified-oggvct.github.io/ollama_pulse/
- **Status**: FULLY UPGRADED (2025-10-26)
- **Persona**: EchoVein (vein-tapping, pulse-checking)
- **Schedule**: 08:30 AM CT + 04:30 PM CT daily
- **Data Sources**: 16 sources (Stack Overflow, Model Registry, GitHub, Reddit, HN, YouTube, etc.)

**Infrastructure**:
- ✅ Supabase PostgreSQL (with SQLite fallback)
- ✅ Sentry monitoring (Decision Engine, Browser UI, Relay Services)
- ✅ Honeycomb tracing
- ✅ Dynamic index generation
- ✅ Manual tracking system (`tracked_projects.json`)
- ✅ Webhook trigger to GrumpiBlogged (`.github/workflows/trigger_grumpiblogged.yml`)
- ⚠️ Nostr publishing DEFERRED (should be done by GrumpiBlogged)

**Secrets Available** (Organization-level):
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OLLAMA_API_KEY`
- `NOSTR_PUBLIC_KEY_NPUB`
- `NOSTR_SECRET_KEY_NSEC`

---

### **2. AI Research Daily** ⚠️ NEEDS UPGRADE
- **URL**: https://github.com/Grumpified-OGGVCT/AI_Research_Daily
- **Live Site**: https://grumpified-oggvct.github.io/AI_Research_Daily/
- **Status**: BASIC STRUCTURE EXISTS, NEEDS ENHANCEMENTS
- **Persona**: The Scholar (academic, rigorous, deep analysis)
- **Schedule**: 08:05 AM CT daily
- **Data Source**: AI Research Daily feed (https://accidentaljedi.github.io/AI_Research_Daily/)

**Current Features**:
- ✅ GitHub Actions workflow (`daily_lab_blog.yml`)
- ✅ Report generation (`scripts/generate_lab_blog.py`)
- ✅ GitHub Pages deployment
- ✅ Archive system (`docs/reports/index.html`)
- ✅ Crimson-accented dark theme

**Needs to Add** (copy from Ollama Pulse):
- ❌ Supabase PostgreSQL integration
- ❌ Sentry monitoring
- ❌ Honeycomb tracing
- ❌ Webhook trigger to GrumpiBlogged
- ❌ Dynamic index generation
- ❌ Enhanced error handling

---

### **3. GrumpiBlogged** 🎯 NEXT TO UPGRADE
- **URL**: https://github.com/Grumpified-OGGVCT/GrumpiBlogged
- **Live Site**: https://grumpified-oggvct.github.io/GrumpiBlogged/
- **Status**: NEEDS COMPLETE UPGRADE
- **Role**: Meta-aggregator and Nostr publisher
- **Schedule**: 18:00 CT daily (after both sources publish)

**Purpose**:
- Receive webhooks from Ollama Pulse + AI Research Daily
- Aggregate reports into meta-analysis
- **PRIMARY NOSTR PUBLISHER** (NIP-23 long-form content)
- Analytical, practical, innovative forward-thinking content

**Needs to Implement**:
1. ✅ Webhook receivers (`.github/workflows/aggregate_reports.yml`)
2. ✅ Meta-report generator (`scripts/generate_meta_report.py`)
3. ✅ Supabase PostgreSQL integration
4. ✅ Sentry monitoring
5. ✅ Honeycomb tracing
6. ✅ **Nostr NIP-23 publishing** (THIS IS THE RIGHT PLACE!)
7. ✅ Dynamic index generation
8. ✅ Enhanced analytics and insights
9. ✅ QR code donations (Ko-fi + Lightning wallets)

---

## 🎯 **GRUMPIBLOGGED UPGRADE PLAN**

### **Phase 1: Infrastructure Setup** (Priority: CRITICAL)

#### **1.1 Webhook Receivers**
- **File**: `.github/workflows/aggregate_reports.yml`
- **Template**: Already exists in Ollama Pulse as `GRUMPIBLOGGED_WEBHOOK_RECEIVER.yml`
- **Triggers**:
  - `repository_dispatch` event type: `ollama-pulse-update`
  - `repository_dispatch` event type: `ai-research-daily-update`
  - `schedule`: Daily at 18:00 CT (after both sources publish)

**Payload Structure**:
```json
{
  "source": "ollama_pulse" | "ai_research_daily",
  "report_date": "2025-10-26",
  "report_url": "https://grumpified-oggvct.github.io/ollama_pulse/reports/pulse-2025-10-26.html",
  "description": "Brief summary"
}
```

#### **1.2 Secrets Configuration**
Add to GrumpiBlogged repository secrets:
- `SUPABASE_URL` (copy from organization secrets)
- `SUPABASE_KEY` (copy from organization secrets)
- `OLLAMA_API_KEY` (copy from organization secrets)
- `NOSTR_SECRET_KEY_NSEC` (for publishing)
- `GH_PAT` (for committing generated reports)

**Note**: Organization-level secrets are already configured, just need to verify access.

---

### **Phase 2: Meta-Report Generation** (Priority: HIGH)

#### **2.1 Create Meta-Report Generator**
- **File**: `scripts/generate_meta_report.py`
- **Purpose**: Aggregate Ollama Pulse + AI Research Daily into unified analysis

**Features**:
1. **Fetch Source Reports**:
   - Download latest Ollama Pulse report (HTML/JSON)
   - Download latest AI Research Daily report (HTML/JSON)
   - Parse and extract key insights

2. **Cross-Analysis**:
   - Identify overlapping themes (e.g., Ollama models mentioned in research)
   - Synthesize connections between practical tools and academic research
   - Generate "Ecosystem Pulse" section

3. **Analytical Sections**:
   - **Executive Summary**: High-level overview of both ecosystems
   - **Ollama Ecosystem Update**: Condensed from Ollama Pulse
   - **Research Breakthroughs**: Condensed from AI Research Daily
   - **Cross-Pollination**: Where research meets practice
   - **Forward-Thinking Innovations**: Future possibilities
   - **Practical Applications**: How to use today's discoveries

4. **Output Format**:
   - Markdown report: `docs/reports/meta-{date}.md`
   - HTML report: `docs/reports/meta-{date}.html`
   - JSON data: `data/meta/{date}.json`

#### **2.2 Persona: The Synthesizer**
- **Voice**: Analytical, practical, innovative, forward-thinking
- **Tone**: Professional but accessible
- **Focus**: Bridging academic research and practical implementation
- **Style**: Clear explanations, actionable insights, ecosystem thinking

---

### **Phase 3: Nostr NIP-23 Publishing** (Priority: HIGH)

#### **3.1 Nostr Integration**
- **File**: `scripts/post_to_nostr.py` (copy from Ollama Pulse, enhance)
- **Protocol**: NIP-23 (long-form content)
- **Keys**: Use `NOSTR_PUBLIC_KEY_NPUB` and `NOSTR_SECRET_KEY_NSEC`

**Publishing Strategy**:
1. **Daily Meta-Report**: Full aggregated analysis
2. **Format**: Markdown with proper NIP-23 structure
3. **Tags**: `#AI`, `#Ollama`, `#Research`, `#OpenSource`, `#Innovation`
4. **Relays** (48 free relays, deduplicated):

**Primary/Popular Relays** (High reliability):
   - wss://relay.damus.io
   - wss://nos.lol
   - wss://nostr.wine
   - wss://relay.snort.social
   - wss://relay.primal.net
   - wss://nostr.mom
   - wss://relay.nostr.band

**Geographic/Regional Relays**:
   - wss://atlas.nostr.land
   - wss://eden.nostr.land
   - wss://puravida.nostr.land
   - wss://relay-nostr-br.com.br:4848

**Community/Specialized Relays**:
   - wss://relay.bitcoinpark.com
   - wss://lightningrelay.com
   - wss://relay.westernbtc.com
   - wss://nostr.lopp.social
   - wss://purplepag.es
   - wss://yabu.me
   - wss://wot.nostr.party
   - wss://wot.utxo.one
   - wss://seal.cafe

**Technical/Developer Relays**:
   - wss://pyramid.fiatjaf.com
   - wss://relay.basspistol.org
   - wss://offchain.pub
   - wss://nostr-01.yakihonne.com
   - wss://nostr.slothy.win
   - wss://sendit.nosflare.com
   - wss://relay1.gems.xyz
   - wss://relays.pro

**Storage/Archive Relays**:
   - wss://temp.iris.to
   - wss://vault.iris.to
   - wss://blossom.nostr.build

**Alternative/Niche Relays**:
   - wss://front-end.social
   - wss://nicecrew.digital
   - wss://nostr-elites.org
   - wss://nostr-relay.wellorder.net
   - wss://nostr.0xtr.dev
   - wss://nostr.btcmp
   - wss://nostr.czas.plus
   - wss://nostr.ownscale.org
   - wss://nostr.soscary.net
   - wss://nostr.ussenterprise.xyz
   - wss://nostr.vulpem
   - wss://relay.alien.blue
   - wss://rsslay.sovbit.host

**Paid/Premium Relays** (for reference, not using):
   - wss://premium.primal.net
   - wss://nostr-pub.wellorder.net
   - wss://paid.no.str.cr

**Caching Services** (for reference, not for publishing):
   - wss://cache2.primal.net/v1

**Content Structure**:
```markdown
# GrumpiBlogged Meta-Report - {date}

## Executive Summary
[High-level overview]

## Ollama Ecosystem Pulse
[From Ollama Pulse report]

## AI Research Breakthroughs
[From AI Research Daily]

## Cross-Pollination Analysis
[Unique synthesis]

## Practical Applications
[Actionable insights]

## Support This Work
[Ko-fi + Lightning wallets with QR codes]
```

---

### **Phase 4: Database Integration** (Priority: MEDIUM)

#### **4.1 Supabase PostgreSQL**
- **Copy from**: Ollama Pulse implementation
- **Tables**:
  - `meta_reports` (aggregated reports)
  - `source_reports` (tracking Ollama Pulse + AI Research Daily)
  - `nostr_publications` (tracking Nostr posts)
  - `analytics` (engagement metrics)

**Schema**:
```sql
CREATE TABLE meta_reports (
  id SERIAL PRIMARY KEY,
  report_date DATE UNIQUE NOT NULL,
  ollama_pulse_url TEXT,
  ai_research_url TEXT,
  meta_report_url TEXT,
  nostr_event_id TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE source_reports (
  id SERIAL PRIMARY KEY,
  source TEXT NOT NULL, -- 'ollama_pulse' or 'ai_research_daily'
  report_date DATE NOT NULL,
  report_url TEXT NOT NULL,
  fetched_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE nostr_publications (
  id SERIAL PRIMARY KEY,
  event_id TEXT UNIQUE NOT NULL,
  report_date DATE NOT NULL,
  published_at TIMESTAMP DEFAULT NOW(),
  relay_count INTEGER,
  success BOOLEAN
);
```

#### **4.2 SQLite Fallback**
- Same pattern as Ollama Pulse
- Graceful degradation if Supabase unavailable

---

### **Phase 5: Monitoring & Observability** (Priority: MEDIUM)

#### **5.1 Sentry Integration**
- **Copy from**: Ollama Pulse implementation
- **Projects**:
  - `grumpiblogged-meta-generator` (report generation)
  - `grumpiblogged-nostr-publisher` (Nostr publishing)
  - `grumpiblogged-webhook-receiver` (webhook handling)

**Error Tracking**:
- Webhook reception failures
- Report fetching errors
- Meta-report generation issues
- Nostr publishing failures
- Database connection problems

#### **5.2 Honeycomb Tracing**
- **Copy from**: Ollama Pulse implementation
- **Traces**:
  - Webhook → Fetch → Generate → Publish → Store
  - End-to-end latency tracking
  - Performance bottleneck identification

---

### **Phase 6: UI/UX Enhancements** (Priority: LOW)

#### **6.1 Dynamic Index Generation**
- **Copy from**: Ollama Pulse `scripts/update_index.py`
- **Features**:
  - List view of all meta-reports
  - Calendar view
  - Search functionality
  - Filter by source (Ollama/Research/Both)

#### **6.2 QR Code Donations**
- **Copy from**: Ollama Pulse implementation
- **Assets**:
  - `docs/assets/KofiTipQR_Code_GrumpiFied.png` → https://ko-fi.com/grumpified
  - `docs/assets/lightning_wallet_QR_Code.png` → gossamerfalling850577@getalby.com
  - `docs/assets/lightning_wallet_QR_Code_2.png` → havenhelpful360120@getalby.com

#### **6.3 Theme**
- Dark theme with accent color (TBD - not crimson, not EchoVein's colors)
- Professional, clean, modern
- Mobile-responsive

---

## 🔄 **WORKFLOW SEQUENCE**

### **Daily Automation Flow**

```
08:05 CT: AI Research Daily publishes
  ↓
  Triggers webhook to GrumpiBlogged
  ↓
  GrumpiBlogged stores source report URL

08:30 CT: Ollama Pulse publishes (morning)
  ↓
  Triggers webhook to GrumpiBlogged
  ↓
  GrumpiBlogged stores source report URL

16:30 CT: Ollama Pulse publishes (afternoon)
  ↓
  Triggers webhook to GrumpiBlogged
  ↓
  GrumpiBlogged stores source report URL

18:00 CT: GrumpiBlogged scheduled run
  ↓
  1. Fetch latest Ollama Pulse report
  ↓
  2. Fetch latest AI Research Daily report
  ↓
  3. Generate meta-report (aggregate + analyze)
  ↓
  4. Publish to Nostr (NIP-23)
  ↓
  5. Store in Supabase
  ↓
  6. Update index.html
  ↓
  7. Commit and push to GitHub
  ↓
  8. GitHub Pages deploys
```

---

## 📋 **IMPLEMENTATION CHECKLIST**

### **Phase 1: Infrastructure** ✅
- [ ] Copy webhook receiver template to `.github/workflows/aggregate_reports.yml`
- [ ] Verify organization secrets are accessible
- [ ] Add `GH_PAT` secret for committing
- [ ] Test webhook reception (manual trigger)

### **Phase 2: Meta-Report Generation** ✅
- [ ] Create `scripts/generate_meta_report.py`
- [ ] Implement source report fetching
- [ ] Implement cross-analysis logic
- [ ] Implement Synthesizer persona
- [ ] Test local generation

### **Phase 3: Nostr Publishing** ✅
- [ ] Copy `scripts/post_to_nostr.py` from Ollama Pulse
- [ ] Enhance for meta-report format
- [ ] Configure NIP-23 structure
- [ ] Test publishing to relays
- [ ] Verify event propagation

### **Phase 4: Database** ✅
- [ ] Copy Supabase integration from Ollama Pulse
- [ ] Create tables in Supabase
- [ ] Implement SQLite fallback
- [ ] Test database operations

### **Phase 5: Monitoring** ✅
- [ ] Set up Sentry projects
- [ ] Integrate Sentry SDK
- [ ] Configure Honeycomb tracing
- [ ] Test error reporting

### **Phase 6: UI/UX** ✅
- [ ] Copy `scripts/update_index.py`
- [ ] Copy QR code assets
- [ ] Design theme
- [ ] Test responsive layout

---

## 🎯 **SUCCESS CRITERIA**

### **Must Have** (MVP)
1. ✅ Receives webhooks from both sources
2. ✅ Generates meta-reports daily at 18:00 CT
3. ✅ Publishes to Nostr (NIP-23)
4. ✅ Stores in Supabase
5. ✅ Deploys to GitHub Pages

### **Should Have** (V1)
6. ✅ Sentry error tracking
7. ✅ Honeycomb tracing
8. ✅ Dynamic index with search
9. ✅ QR code donations

### **Nice to Have** (V2)
10. ⚠️ Analytics dashboard
11. ⚠️ Email notifications
12. ⚠️ RSS feed
13. ⚠️ API endpoints

---

## 🚨 **CRITICAL REMINDERS**

### **For AI Agent on "The Other Side"**

1. **READ MEMORY FIRST**: Always start with `read_graph()` to restore context
2. **CHECK TASKS**: Use `list_requests()` to see pending work
3. **ECOSYSTEM CONTEXT**: This is part of a 3-repo ecosystem, not standalone
4. **NOSTR IS KEY**: GrumpiBlogged is THE Nostr publisher, not Ollama Pulse
5. **COPY, DON'T REBUILD**: Ollama Pulse has working implementations - copy them!
6. **SECRETS EXIST**: Organization-level secrets are already configured
7. **WEBHOOK TEMPLATE EXISTS**: `GRUMPIBLOGGED_WEBHOOK_RECEIVER.yml` in Ollama Pulse
8. **PERSONA MATTERS**: The Synthesizer - analytical, practical, innovative

### **Files to Reference from Ollama Pulse**
- `.github/workflows/trigger_grumpiblogged.yml` (webhook sender)
- `GRUMPIBLOGGED_WEBHOOK_RECEIVER.yml` (webhook receiver template)
- `PHASE_4_WEBHOOKS_SETUP_GUIDE.md` (setup instructions)
- `scripts/post_to_nostr.py` (Nostr publishing)
- `scripts/update_index.py` (dynamic index)
- Database integration code (Supabase + SQLite)
- Sentry integration code
- Honeycomb integration code

---

## 📊 **CURRENT STATE SUMMARY**

**Ollama Pulse**: ✅ COMPLETE (16 sources, Supabase, Sentry, Honeycomb, webhooks)  
**AI Research Daily**: ⚠️ BASIC (needs enhancements copied from Ollama Pulse)  
**GrumpiBlogged**: ❌ NEEDS UPGRADE (this is the next priority)

**Next Action**: Open GrumpiBlogged workspace and execute this plan!

---

**Last Updated**: 2025-10-26  
**Created By**: The Augster (Ollama Pulse session)  
**For**: The Augster (GrumpiBlogged session)  
**Status**: READY TO EXECUTE 🚀

