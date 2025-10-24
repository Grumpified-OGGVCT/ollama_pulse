/**
 * Ollama Pulse - Navigation System
 * Provides Next/Previous/Home navigation and semantic search
 */

(function() {
  'use strict';

  // Configuration
  const REPORTS_DIR = '/ollama_pulse/reports/';
  const BASE_PATH = '/ollama_pulse/';
  
  // Get all available reports from the page or localStorage cache
  let availableReports = [];

  /**
   * Initialize navigation system
   */
  function initNavigation() {
    // Try to get reports list from meta tag or localStorage
    const reportsMetaTag = document.querySelector('meta[name="available-reports"]');
    if (reportsMetaTag) {
      availableReports = JSON.parse(reportsMetaTag.content);
    } else {
      // Fall back to default reports (will be updated by generate_report.py)
      availableReports = [
        'pulse-2025-10-22',
        'pulse-2025-10-23',
        'pulse-2025-10-24'
      ];
    }

    // Sort reports (newest first)
    availableReports.sort().reverse();
    
    // Get current report name from URL
    const currentPath = window.location.pathname;
    const currentReport = getCurrentReportName(currentPath);
    
    if (currentReport) {
      setupReportNavigation(currentReport);
    }
    
    setupSearch();
  }

  /**
   * Extract report name from current URL
   */
  function getCurrentReportName(path) {
    const match = path.match(/pulse-(\d{4}-\d{2}-\d{2})/);
    return match ? match[0] : null;
  }

  /**
   * Setup navigation buttons for a specific report
   */
  function setupReportNavigation(currentReport) {
    const currentIndex = availableReports.indexOf(currentReport);
    
    if (currentIndex === -1) {
      console.warn('Current report not found in available reports list');
      return;
    }

    // Create navigation container if it doesn't exist
    let navContainer = document.querySelector('.report-navigation');
    if (!navContainer) {
      navContainer = createNavigationContainer();
      insertNavigationContainer(navContainer);
    }

    // Setup navigation buttons
    const prevBtn = navContainer.querySelector('.nav-prev');
    const nextBtn = navContainer.querySelector('.nav-next');
    const homeBtn = navContainer.querySelector('.nav-home');

    // Previous (older) report
    if (currentIndex < availableReports.length - 1) {
      const prevReport = availableReports[currentIndex + 1];
      prevBtn.disabled = false;
      prevBtn.onclick = () => navigateToReport(prevReport);
      prevBtn.title = `Previous: ${prevReport}`;
    } else {
      prevBtn.disabled = true;
      prevBtn.title = 'No older reports';
    }

    // Next (newer) report
    if (currentIndex > 0) {
      const nextReport = availableReports[currentIndex - 1];
      nextBtn.disabled = false;
      nextBtn.onclick = () => navigateToReport(nextReport);
      nextBtn.title = `Next: ${nextReport}`;
    } else {
      nextBtn.disabled = true;
      nextBtn.title = 'This is the latest report';
    }

    // Home (latest report)
    homeBtn.onclick = () => window.location.href = BASE_PATH;
    homeBtn.title = 'Go to latest report';

    // Keyboard shortcuts
    setupKeyboardShortcuts(currentIndex);
  }

  /**
   * Create navigation container HTML
   */
  function createNavigationContainer() {
    const container = document.createElement('div');
    container.className = 'report-navigation';
    container.innerHTML = `
      <div class="nav-controls">
        <button class="nav-btn nav-prev" title="Previous report">
          <span>← Previous</span>
        </button>
        <button class="nav-btn nav-home" title="Home (Latest)">
          <span>🏠 Home</span>
        </button>
        <button class="nav-btn nav-next" title="Next report">
          <span>Next →</span>
        </button>
      </div>
      <div class="nav-search-container">
        <input type="text" 
               class="nav-search" 
               placeholder="🔍 Search reports..." 
               aria-label="Search reports">
        <div class="search-results" style="display: none;"></div>
      </div>
    `;
    return container;
  }

  /**
   * Insert navigation container into the page
   */
  function insertNavigationContainer(container) {
    // Try to insert after the h1 or at the top of body
    const h1 = document.querySelector('h1');
    if (h1 && h1.parentNode) {
      h1.parentNode.insertBefore(container, h1.nextSibling);
    } else {
      document.body.insertBefore(container, document.body.firstChild);
    }
  }

  /**
   * Navigate to a specific report
   */
  function navigateToReport(reportName) {
    window.location.href = `${REPORTS_DIR}${reportName}.html`;
  }

  /**
   * Setup keyboard shortcuts for navigation
   */
  function setupKeyboardShortcuts(currentIndex) {
    document.addEventListener('keydown', function(e) {
      // Don't interfere with input fields
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
      }

      switch(e.key) {
        case 'ArrowLeft':
        case 'p':
          // Previous (older) report
          if (currentIndex < availableReports.length - 1) {
            e.preventDefault();
            navigateToReport(availableReports[currentIndex + 1]);
          }
          break;
        case 'ArrowRight':
        case 'n':
          // Next (newer) report
          if (currentIndex > 0) {
            e.preventDefault();
            navigateToReport(availableReports[currentIndex - 1]);
          }
          break;
        case 'h':
          // Home
          e.preventDefault();
          window.location.href = BASE_PATH;
          break;
        case '/':
          // Focus search
          e.preventDefault();
          const searchInput = document.querySelector('.nav-search');
          if (searchInput) searchInput.focus();
          break;
      }
    });
  }

  /**
   * Setup semantic search functionality
   */
  function setupSearch() {
    const searchInput = document.querySelector('.nav-search');
    const searchResults = document.querySelector('.search-results');
    
    if (!searchInput || !searchResults) return;

    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
      clearTimeout(searchTimeout);
      const query = e.target.value.trim().toLowerCase();
      
      if (query.length < 2) {
        searchResults.style.display = 'none';
        return;
      }

      // Debounce search
      searchTimeout = setTimeout(() => {
        performSearch(query, searchResults);
      }, 300);
    });

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.style.display = 'none';
      }
    });

    // Show results when focusing on search input
    searchInput.addEventListener('focus', function() {
      if (searchInput.value.length >= 2) {
        searchResults.style.display = 'block';
      }
    });
  }

  /**
   * Perform semantic search across reports
   */
  function performSearch(query, resultsContainer) {
    // Search current page content
    const pageContent = document.body.innerText.toLowerCase();
    const results = [];

    // Search in current page
    if (pageContent.includes(query)) {
      const currentReport = getCurrentReportName(window.location.pathname);
      if (currentReport) {
        results.push({
          title: currentReport,
          snippet: getSearchSnippet(pageContent, query),
          url: window.location.pathname,
          isCurrent: true
        });
      }
    }

    // Search in report names
    availableReports.forEach(report => {
      const reportName = report.toLowerCase();
      const reportDate = report.replace('pulse-', '');
      
      if (reportName.includes(query) || reportDate.includes(query)) {
        const currentReport = getCurrentReportName(window.location.pathname);
        if (report !== currentReport) {
          results.push({
            title: report,
            snippet: `Report from ${reportDate}`,
            url: `${REPORTS_DIR}${report}.html`,
            isCurrent: false
          });
        }
      }
    });

    // Search for common keywords
    const keywords = ['turbo', 'cloud', 'voice', 'multimodal', 'coding', 'api'];
    keywords.forEach(keyword => {
      if (keyword.includes(query) && !results.find(r => r.snippet.includes(keyword))) {
        results.push({
          title: `Search: ${keyword}`,
          snippet: `Find reports mentioning "${keyword}"`,
          url: '#',
          isKeyword: true,
          keyword: keyword
        });
      }
    });

    displaySearchResults(results, resultsContainer, query);
  }

  /**
   * Get a snippet of text around the search query
   */
  function getSearchSnippet(text, query) {
    const index = text.indexOf(query);
    if (index === -1) return '';
    
    const start = Math.max(0, index - 50);
    const end = Math.min(text.length, index + query.length + 50);
    let snippet = text.substring(start, end).trim();
    
    if (start > 0) snippet = '...' + snippet;
    if (end < text.length) snippet = snippet + '...';
    
    return snippet;
  }

  /**
   * Display search results
   */
  function displaySearchResults(results, container, query) {
    if (results.length === 0) {
      container.innerHTML = '<div class="search-no-results">No results found</div>';
      container.style.display = 'block';
      return;
    }

    const html = results.slice(0, 10).map(result => {
      const className = result.isCurrent ? 'search-result current' : 'search-result';
      const label = result.isCurrent ? ' (current page)' : '';
      
      if (result.isKeyword) {
        return `
          <div class="${className}" data-keyword="${result.keyword}">
            <div class="result-title">${result.title}${label}</div>
            <div class="result-snippet">${result.snippet}</div>
          </div>
        `;
      } else {
        return `
          <a href="${result.url}" class="${className}">
            <div class="result-title">${result.title}${label}</div>
            <div class="result-snippet">${highlightQuery(result.snippet, query)}</div>
          </a>
        `;
      }
    }).join('');

    container.innerHTML = html;
    container.style.display = 'block';

    // Add click handlers for keyword searches
    container.querySelectorAll('[data-keyword]').forEach(el => {
      el.addEventListener('click', function() {
        const keyword = this.dataset.keyword;
        searchKeywordInPage(keyword);
      });
    });
  }

  /**
   * Highlight search query in text
   */
  function highlightQuery(text, query) {
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  /**
   * Escape regex special characters
   */
  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Search for keyword in current page and highlight
   */
  function searchKeywordInPage(keyword) {
    // Use browser's find functionality if available
    if (window.find) {
      window.find(keyword, false, false, true, false, true, false);
    }
    
    // Scroll to first occurrence
    const content = document.body.innerText.toLowerCase();
    const index = content.indexOf(keyword.toLowerCase());
    if (index !== -1) {
      // Simple scroll to approximate position
      const percentage = index / content.length;
      window.scrollTo({
        top: document.body.scrollHeight * percentage,
        behavior: 'smooth'
      });
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNavigation);
  } else {
    initNavigation();
  }
})();
