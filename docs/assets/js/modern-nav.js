/**
 * Ollama Pulse - Modern Navigation System
 * Professional navigation bar with search, dropdowns, and responsive design
 */

(function() {
  'use strict';

  // Configuration
  const BASE_PATH = '/ollama_pulse/';
  const REPORTS_DIR = BASE_PATH + 'reports/';
  
  let allReports = [];
  let searchDebounceTimer = null;

  /**
   * Initialize modern navigation
   */
  function initModernNav() {
    // Load reports data
    loadReportsData();

    // Setup navigation toggle for mobile
    setupMobileNav();

    // Setup search functionality
    setupNavSearch();

    // Setup recent reports dropdown
    setupRecentReportsDropdown();

    // Setup sticky navigation
    setupStickyNav();

    // Setup breadcrumbs
    setupBreadcrumbs();

    // Highlight active nav link
    highlightActiveNav();
  }

  /**
   * Load reports data from metadata
   */
  function loadReportsData() {
    const metaTag = document.querySelector('meta[name="available-reports"]');
    if (metaTag && metaTag.content) {
      try {
        allReports = JSON.parse(metaTag.content);
      } catch (e) {
        console.warn('Failed to parse reports metadata:', e);
        allReports = generateFallbackReports();
      }
    } else {
      allReports = generateFallbackReports();
    }
  }

  /**
   * Generate fallback reports list
   */
  function generateFallbackReports() {
    const reports = [];
    const today = new Date();
    
    for (let i = 0; i < 30; i++) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];
      
      reports.push({
        date: dateStr,
        title: `Pulse ${dateStr}`,
        url: `${REPORTS_DIR}pulse-${dateStr}.html`
      });
    }
    
    return reports;
  }

  /**
   * Setup mobile navigation toggle
   */
  function setupMobileNav() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (!navToggle || !navMenu) return;

    navToggle.addEventListener('click', function() {
      const isOpen = navMenu.classList.toggle('active');
      navToggle.classList.toggle('active');
      navToggle.setAttribute('aria-expanded', isOpen);
      
      // Prevent body scroll when menu is open
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });

    // Close menu on escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  /**
   * Setup navigation search
   */
  function setupNavSearch() {
    const searchInput = document.getElementById('navSearchInput');
    const searchClear = document.getElementById('navSearchClear');
    const searchResults = document.getElementById('navSearchResults');
    
    if (!searchInput || !searchResults) return;

    searchInput.addEventListener('input', function(e) {
      const query = e.target.value.trim();
      
      // Show/hide clear button
      if (searchClear) {
        searchClear.style.display = query ? 'flex' : 'none';
      }

      // Debounce search
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        performNavSearch(query, searchResults);
      }, 300);
    });

    // Clear search
    if (searchClear) {
      searchClear.addEventListener('click', function() {
        searchInput.value = '';
        searchClear.style.display = 'none';
        searchResults.innerHTML = '';
        searchResults.style.display = 'none';
        searchInput.focus();
      });
    }

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.style.display = 'none';
      }
    });

    // Show results when focusing search input
    searchInput.addEventListener('focus', function() {
      if (searchInput.value.trim() && searchResults.innerHTML) {
        searchResults.style.display = 'block';
      }
    });
  }

  /**
   * Perform navigation search
   */
  function performNavSearch(query, resultsContainer) {
    if (!query) {
      resultsContainer.innerHTML = '';
      resultsContainer.style.display = 'none';
      return;
    }

    const queryLower = query.toLowerCase();
    const matches = allReports.filter(report => {
      return report.title.toLowerCase().includes(queryLower) ||
             report.date.includes(queryLower);
    }).slice(0, 10);

    if (matches.length === 0) {
      resultsContainer.innerHTML = '<div class="search-no-results">No reports found</div>';
      resultsContainer.style.display = 'block';
      return;
    }

    const html = matches.map(report => `
      <a href="${report.url}" class="nav-search-result">
        <i class="fas fa-file-alt"></i>
        <div class="result-content">
          <div class="result-title">${highlightMatch(report.title, query)}</div>
          <div class="result-date">${formatDate(report.date)}</div>
        </div>
      </a>
    `).join('');

    resultsContainer.innerHTML = html;
    resultsContainer.style.display = 'block';
  }

  /**
   * Highlight search matches
   */
  function highlightMatch(text, query) {
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
   * Format date for display
   */
  function formatDate(dateStr) {
    const date = new Date(dateStr);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
  }

  /**
   * Setup recent reports dropdown
   */
  function setupRecentReportsDropdown() {
    const dropdown = document.getElementById('recentDropdown');
    const menu = document.getElementById('recentReportsMenu');
    
    if (!dropdown || !menu) return;

    // Populate recent reports
    const recentReports = allReports.slice(0, 10);
    const html = recentReports.map((report, index) => `
      <a href="${report.url}" class="dropdown-item">
        ${index === 0 ? '<i class="fas fa-star"></i>' : '<i class="fas fa-file-alt"></i>'}
        <span>${report.title}</span>
        <span class="item-date">${formatDate(report.date)}</span>
      </a>
    `).join('');
    
    menu.innerHTML = html || '<div class="dropdown-item disabled">No reports available</div>';

    // Toggle dropdown
    dropdown.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const isOpen = menu.classList.toggle('active');
      dropdown.classList.toggle('active');
      dropdown.setAttribute('aria-expanded', isOpen);
      
      // Close other dropdowns
      document.querySelectorAll('.dropdown-menu').forEach(m => {
        if (m !== menu) {
          m.classList.remove('active');
        }
      });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!dropdown.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove('active');
        dropdown.classList.remove('active');
        dropdown.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /**
   * Setup sticky navigation
   */
  function setupStickyNav() {
    const nav = document.getElementById('mainNav');
    if (!nav) return;

    let lastScrollTop = 0;
    const navHeight = nav.offsetHeight;

    window.addEventListener('scroll', function() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      // Add shadow when scrolled
      if (scrollTop > 10) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }

      // Hide nav on scroll down, show on scroll up
      if (scrollTop > lastScrollTop && scrollTop > navHeight) {
        nav.classList.add('nav-hidden');
      } else {
        nav.classList.remove('nav-hidden');
      }
      
      lastScrollTop = scrollTop;
    });
  }

  /**
   * Setup breadcrumbs
   */
  function setupBreadcrumbs() {
    const breadcrumbContainer = document.getElementById('breadcrumbNav');
    if (!breadcrumbContainer) return;

    const path = window.location.pathname;
    
    // Only show breadcrumbs on report pages
    if (!path.includes('/reports/')) {
      breadcrumbContainer.style.display = 'none';
      return;
    }

    const reportMatch = path.match(/pulse-(\d{4}-\d{2}-\d{2})/);
    if (!reportMatch) {
      breadcrumbContainer.style.display = 'none';
      return;
    }

    const reportDate = reportMatch[1];
    const reportIndex = allReports.findIndex(r => r.date === reportDate);
    
    let breadcrumbHTML = `
      <div class="breadcrumb">
        <a href="${BASE_PATH}" class="breadcrumb-item">
          <i class="fas fa-home"></i>
          <span>Home</span>
        </a>
        <i class="fas fa-chevron-right breadcrumb-separator"></i>
        <a href="${BASE_PATH}reports/" class="breadcrumb-item">
          <span>Reports</span>
        </a>
        <i class="fas fa-chevron-right breadcrumb-separator"></i>
        <span class="breadcrumb-item active">
          <span>${formatDate(reportDate)}</span>
        </span>
      </div>
    `;

    // Add report navigation
    if (reportIndex !== -1) {
      const prevReport = allReports[reportIndex + 1];
      const nextReport = allReports[reportIndex - 1];
      
      breadcrumbHTML += `
        <div class="report-nav-mini">
          ${prevReport ? `
            <a href="${prevReport.url}" class="nav-mini-btn" title="Previous: ${prevReport.title}">
              <i class="fas fa-chevron-left"></i>
              <span>Previous</span>
            </a>
          ` : '<span class="nav-mini-btn disabled"><i class="fas fa-chevron-left"></i><span>Previous</span></span>'}
          
          <span class="report-position">${reportIndex + 1} of ${allReports.length}</span>
          
          ${nextReport ? `
            <a href="${nextReport.url}" class="nav-mini-btn" title="Next: ${nextReport.title}">
              <span>Next</span>
              <i class="fas fa-chevron-right"></i>
            </a>
          ` : '<span class="nav-mini-btn disabled"><span>Next</span><i class="fas fa-chevron-right"></i></span>'}
        </div>
      `;
    }

    breadcrumbContainer.innerHTML = breadcrumbHTML;
    breadcrumbContainer.style.display = 'flex';
  }

  /**
   * Highlight active navigation link
   */
  function highlightActiveNav() {
    const path = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && path.includes(href) && href !== BASE_PATH) {
        link.classList.add('active');
      } else if (href === BASE_PATH && (path === BASE_PATH || path === BASE_PATH + 'index.html')) {
        link.classList.add('active');
      }
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initModernNav);
  } else {
    initModernNav();
  }
})();

