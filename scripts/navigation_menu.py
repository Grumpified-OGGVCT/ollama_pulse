#!/usr/bin/env python3
"""
Navigation Menu Generator for Ollama Pulse Reports
Creates sticky navigation with section links and back-to-top buttons
"""

def generate_navigation_menu():
    """Generate sticky navigation menu HTML"""
    return """
<nav id="report-navigation" class="report-nav-sticky">
  <div class="nav-header">
    <span class="nav-title">📋 Report Navigation</span>
    <button class="nav-toggle" aria-label="Toggle navigation">☰</button>
  </div>
  <div class="nav-links">
    <a href="#summary" class="nav-link">📊 Intelligence Summary</a>
    <a href="#breakthroughs" class="nav-link">⚡ Breakthroughs</a>
    <a href="#official" class="nav-link">🎯 Official Updates</a>
    <a href="#community" class="nav-link">🛠️ Community Projects</a>
    <a href="#patterns" class="nav-link">📈 Pattern Mapping</a>
    <a href="#prophecies" class="nav-link">🔔 Prophecies</a>
    <a href="#developers" class="nav-link">🚀 For Developers</a>
    <a href="#bounties" class="nav-link">💰 Bounties</a>
    <a href="#watch" class="nav-link">👀 What to Watch</a>
    <a href="#nostr" class="nav-link">🌐 Nostr Network</a>
    <a href="#about" class="nav-link">🔮 About EchoVein</a>
    <a href="#support" class="nav-link">💰 Support</a>
  </div>
</nav>

<script>
// Mobile navigation toggle
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  
  if (toggle && links) {
    toggle.addEventListener('click', function() {
      links.classList.toggle('nav-links-open');
    });
  }
  
  // Smooth scrolling for navigation links
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });
        // Close mobile menu if open
        if (links) links.classList.remove('nav-links-open');
      }
    });
  });
});
</script>
"""

def generate_section_header(section_id, title, emoji):
    """Generate section header with anchor and back-to-top link"""
    return f"""
<div id="{section_id}" class="report-section">

## {emoji} {title}

"""

def generate_back_to_top():
    """Generate back to top link"""
    return """
<div class="back-to-top">
  <a href="#report-navigation" class="btn-back-to-top">⬆️ Back to Top</a>
</div>

---
"""

def get_navigation_css():
    """Generate CSS for navigation menu"""
    return """
/* Report Navigation Menu */
.report-nav-sticky {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
  padding: 1rem;
  margin-bottom: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.nav-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
}

.nav-toggle {
  display: none;
  background: none;
  border: none;
  color: #fff;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
}

.nav-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.nav-link {
  display: block;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.report-section {
  scroll-margin-top: 100px; /* Offset for sticky nav */
}

.back-to-top {
  text-align: right;
  margin: 2rem 0;
}

.btn-back-to-top {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-back-to-top:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(220, 20, 60, 0.4);
  background: linear-gradient(135deg, #A00000 0%, #FF1744 100%);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .nav-toggle {
    display: block;
  }
  
  .nav-links {
    display: none;
    grid-template-columns: 1fr;
    margin-top: 1rem;
  }
  
  .nav-links-open {
    display: grid !important;
  }
  
  .nav-header {
    margin-bottom: 0;
  }
}

/* Accessibility - respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .nav-link, .btn-back-to-top {
    transition: none;
  }
  
  * {
    scroll-behavior: auto !important;
  }
}
"""

