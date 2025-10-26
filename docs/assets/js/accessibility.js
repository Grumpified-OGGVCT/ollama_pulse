/**
 * Ollama Pulse - Accessibility Controls
 * Provides font size and zoom controls with localStorage persistence
 */

(function() {
  'use strict';

  // Configuration
  const STORAGE_KEY_FONT_SIZE = 'ollama-pulse-font-size';
  const STORAGE_KEY_ZOOM = 'ollama-pulse-zoom';
  const DEFAULT_FONT_SIZE = 16; // Base font size in px
  const FONT_SIZE_STEPS = [12, 14, 16, 18, 20, 24, 28, 32];
  const ZOOM_LEVELS = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5];

  let currentFontSize = DEFAULT_FONT_SIZE;
  let currentZoom = 1.0;

  /**
   * Initialize accessibility controls
   */
  function initAccessibility() {
    // Load saved preferences
    loadPreferences();
    
    // Create control panel
    createControlPanel();
    
    // Apply saved settings
    applyFontSize(currentFontSize);
    applyZoom(currentZoom);
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
  }

  /**
   * Load user preferences from localStorage
   */
  function loadPreferences() {
    const savedFontSize = localStorage.getItem(STORAGE_KEY_FONT_SIZE);
    const savedZoom = localStorage.getItem(STORAGE_KEY_ZOOM);
    
    if (savedFontSize) {
      currentFontSize = parseInt(savedFontSize, 10);
    }
    
    if (savedZoom) {
      currentZoom = parseFloat(savedZoom);
    }
  }

  /**
   * Save preference to localStorage
   */
  function savePreference(key, value) {
    localStorage.setItem(key, value);
  }

  /**
   * Create accessibility control panel
   */
  function createControlPanel() {
    const panel = document.createElement('div');
    panel.className = 'accessibility-panel';
    panel.innerHTML = `
      <button class="accessibility-toggle" aria-label="Toggle accessibility controls" title="Accessibility Controls (Alt+A)">
        <span>♿</span>
      </button>
      <div class="accessibility-controls" style="display: none;">
        <h4>Accessibility Controls</h4>
        
        <div class="control-group">
          <label>Font Size: <span class="font-size-value">${currentFontSize}px</span></label>
          <div class="button-group">
            <button class="control-btn font-decrease" title="Decrease font size (Ctrl+-)">A-</button>
            <button class="control-btn font-reset" title="Reset font size (Ctrl+0)">Reset</button>
            <button class="control-btn font-increase" title="Increase font size (Ctrl++)">A+</button>
          </div>
        </div>
        
        <div class="control-group">
          <label>Page Zoom: <span class="zoom-value">${Math.round(currentZoom * 100)}%</span></label>
          <div class="button-group">
            <button class="control-btn zoom-out" title="Zoom out (Alt+-)">-</button>
            <button class="control-btn zoom-reset" title="Reset zoom (Alt+0)">100%</button>
            <button class="control-btn zoom-in" title="Zoom in (Alt++)">+</button>
          </div>
        </div>
        
        <div class="control-group">
          <label>Quick Presets:</label>
          <div class="button-group">
            <button class="control-btn preset-small" title="Small text">Small</button>
            <button class="control-btn preset-medium" title="Medium text">Medium</button>
            <button class="control-btn preset-large" title="Large text">Large</button>
            <button class="control-btn preset-xlarge" title="Extra large text">XL</button>
          </div>
        </div>
        
        <div class="control-group">
          <button class="control-btn reset-all" title="Reset all settings">Reset All</button>
        </div>
        

        <div class="lingo-legend">
          <details>
            <summary>🩸 EchoVein Lingo Legend</summary>
            <div class="legend-content">
              <p class="legend-intro">EchoVein speaks in veins and arteries. Here's the decoder ring:</p>
              
              <div class="legend-section">
                <h5>🔬 Core Terminology</h5>
                <dl>
                  <dt>Vein</dt>
                  <dd>A trend, pattern, or discovery in the Ollama ecosystem</dd>
                  
                  <dt>Ore / High-Purity Ore</dt>
                  <dd>A project, repository, or discovery worth mining</dd>
                  
                  <dt>Artery</dt>
                  <dd>A major ecosystem area or category (e.g., "Coding Artery")</dd>
                  
                  <dt>Vein-Tapping</dt>
                  <dd>The process of discovering and analyzing trends</dd>
                  
                  <dt>Artery Depth</dt>
                  <dd>Number of related items in a category/cluster</dd>
                  
                  <dt>Vein Map</dt>
                  <dd>The daily report showing ecosystem patterns</dd>
                </dl>
              </div>

              <div class="legend-section">
                <h5>⚡ Scoring System</h5>
                <dl>
                  <dt>🔥 0.7+ (High-Purity)</dt>
                  <dd>Highly relevant to Ollama Turbo/Cloud features</dd>
                  
                  <dt>⚡ 0.4-0.6 (Medium)</dt>
                  <dd>Moderately relevant, worth watching</dd>
                  
                  <dt>💡 0.3-0.4 (Low)</dt>
                  <dd>Tangentially related, background noise</dd>
                </dl>
              </div>

              <div class="legend-section">
                <h5>🩸 Confidence Levels</h5>
                <dl>
                  <dt>🩸 HIGH</dt>
                  <dd>"This vein's throbbing — trust the flow"</dd>
                  
                  <dt>⚡ MEDIUM</dt>
                  <dd>"Promising artery, but watch for clots"</dd>
                  
                  <dt>💡 LOW</dt>
                  <dd>"Faint pulse — needs more data"</dd>
                </dl>
              </div>

              <div class="legend-section">
                <h5>📊 Pattern Types</h5>
                <dl>
                  <dt>Vein Maintenance</dt>
                  <dd>Steady, ongoing activity in a category</dd>
                  
                  <dt>Vein Explosion</dt>
                  <dd>Sudden spike in activity (2x+ growth potential)</dd>
                  
                  <dt>Vein Oracle</dt>
                  <dd>Predictive insight about future trends</dd>
                </dl>
              </div>

              <div class="legend-section">
                <h5>🎯 EchoVein's Voice</h5>
                <p class="legend-note">
                  EchoVein doesn't just report — they <em>excavate</em>. 
                  The wry, vein-obsessed tone is intentional: it cuts through 
                  AI-generated fluff and delivers sharp, actionable intelligence. 
                  Think of it as your underground cartographer mapping the 
                  Ollama ecosystem's hidden arteries.
                </p>
              </div>
            </div>
          </details>
        </div>        <div class="keyboard-shortcuts">
          <details>
            <summary>Keyboard Shortcuts</summary>
            <ul>
              <li><kbd>Ctrl</kbd> + <kbd>+</kbd> - Increase font</li>
              <li><kbd>Ctrl</kbd> + <kbd>-</kbd> - Decrease font</li>
              <li><kbd>Ctrl</kbd> + <kbd>0</kbd> - Reset font</li>
              <li><kbd>Alt</kbd> + <kbd>+</kbd> - Zoom in</li>
              <li><kbd>Alt</kbd> + <kbd>-</kbd> - Zoom out</li>
              <li><kbd>Alt</kbd> + <kbd>0</kbd> - Reset zoom</li>
              <li><kbd>Alt</kbd> + <kbd>A</kbd> - Toggle controls</li>
            </ul>
          </details>
        </div>
      </div>
    `;

    // Insert panel into page
    document.body.appendChild(panel);
    
    // Setup event handlers
    setupControlHandlers(panel);
  }

  /**
   * Setup event handlers for control panel
   */
  function setupControlHandlers(panel) {
    // Toggle button
    const toggle = panel.querySelector('.accessibility-toggle');
    const controls = panel.querySelector('.accessibility-controls');
    
    toggle.addEventListener('click', function() {
      const isVisible = controls.style.display !== 'none';
      controls.style.display = isVisible ? 'none' : 'block';
      toggle.setAttribute('aria-expanded', !isVisible);
    });

    // Font size controls
    panel.querySelector('.font-decrease').addEventListener('click', () => decreaseFontSize());
    panel.querySelector('.font-increase').addEventListener('click', () => increaseFontSize());
    panel.querySelector('.font-reset').addEventListener('click', () => resetFontSize());

    // Zoom controls
    panel.querySelector('.zoom-out').addEventListener('click', () => zoomOut());
    panel.querySelector('.zoom-in').addEventListener('click', () => zoomIn());
    panel.querySelector('.zoom-reset').addEventListener('click', () => resetZoom());

    // Presets
    panel.querySelector('.preset-small').addEventListener('click', () => applyPreset(14, 0.9));
    panel.querySelector('.preset-medium').addEventListener('click', () => applyPreset(16, 1.0));
    panel.querySelector('.preset-large').addEventListener('click', () => applyPreset(20, 1.1));
    panel.querySelector('.preset-xlarge').addEventListener('click', () => applyPreset(24, 1.2));

    // Reset all
    panel.querySelector('.reset-all').addEventListener('click', () => resetAll());
  }

  /**
   * Apply font size
   */
  function applyFontSize(size) {
    currentFontSize = size;
    document.documentElement.style.setProperty('--base-font-size', size + 'px');
    document.body.style.fontSize = size + 'px';
    
    updateFontSizeDisplay();
    savePreference(STORAGE_KEY_FONT_SIZE, size);
  }

  /**
   * Apply zoom level
   */
  function applyZoom(zoom) {
    currentZoom = zoom;
    document.documentElement.style.setProperty('--page-zoom', zoom);
    
    // Apply zoom to body wrapper if it exists, otherwise to body
    const wrapper = document.querySelector('.wrapper') || document.body;
    wrapper.style.transform = `scale(${zoom})`;
    wrapper.style.transformOrigin = 'top center';
    
    // Adjust body height to account for scaling
    if (zoom !== 1.0) {
      const originalHeight = document.body.scrollHeight;
      document.body.style.minHeight = (originalHeight * zoom) + 'px';
    } else {
      document.body.style.minHeight = '';
    }
    
    updateZoomDisplay();
    savePreference(STORAGE_KEY_ZOOM, zoom);
  }

  /**
   * Update font size display
   */
  function updateFontSizeDisplay() {
    const display = document.querySelector('.font-size-value');
    if (display) {
      display.textContent = currentFontSize + 'px';
    }
  }

  /**
   * Update zoom display
   */
  function updateZoomDisplay() {
    const display = document.querySelector('.zoom-value');
    if (display) {
      display.textContent = Math.round(currentZoom * 100) + '%';
    }
  }

  /**
   * Increase font size
   */
  function increaseFontSize() {
    const currentIndex = FONT_SIZE_STEPS.indexOf(currentFontSize);
    if (currentIndex < FONT_SIZE_STEPS.length - 1) {
      applyFontSize(FONT_SIZE_STEPS[currentIndex + 1]);
    } else if (currentIndex === -1) {
      // Find nearest larger size
      const larger = FONT_SIZE_STEPS.find(s => s > currentFontSize);
      if (larger) {
        applyFontSize(larger);
      }
    }
  }

  /**
   * Decrease font size
   */
  function decreaseFontSize() {
    const currentIndex = FONT_SIZE_STEPS.indexOf(currentFontSize);
    if (currentIndex > 0) {
      applyFontSize(FONT_SIZE_STEPS[currentIndex - 1]);
    } else if (currentIndex === -1) {
      // Find nearest smaller size
      const smaller = [...FONT_SIZE_STEPS].reverse().find(s => s < currentFontSize);
      if (smaller) {
        applyFontSize(smaller);
      }
    }
  }

  /**
   * Reset font size to default
   */
  function resetFontSize() {
    applyFontSize(DEFAULT_FONT_SIZE);
  }

  /**
   * Zoom in
   */
  function zoomIn() {
    const currentIndex = ZOOM_LEVELS.indexOf(currentZoom);
    if (currentIndex < ZOOM_LEVELS.length - 1) {
      applyZoom(ZOOM_LEVELS[currentIndex + 1]);
    } else if (currentIndex === -1) {
      // Find nearest larger zoom
      const larger = ZOOM_LEVELS.find(z => z > currentZoom);
      if (larger) {
        applyZoom(larger);
      }
    }
  }

  /**
   * Zoom out
   */
  function zoomOut() {
    const currentIndex = ZOOM_LEVELS.indexOf(currentZoom);
    if (currentIndex > 0) {
      applyZoom(ZOOM_LEVELS[currentIndex - 1]);
    } else if (currentIndex === -1) {
      // Find nearest smaller zoom
      const smaller = [...ZOOM_LEVELS].reverse().find(z => z < currentZoom);
      if (smaller) {
        applyZoom(smaller);
      }
    }
  }

  /**
   * Reset zoom to 100%
   */
  function resetZoom() {
    applyZoom(1.0);
  }

  /**
   * Apply preset combination
   */
  function applyPreset(fontSize, zoom) {
    applyFontSize(fontSize);
    applyZoom(zoom);
  }

  /**
   * Reset all settings
   */
  function resetAll() {
    resetFontSize();
    resetZoom();
  }

  /**
   * Setup keyboard shortcuts
   */
  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
      // Don't interfere with input fields
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
      }

      // Font size controls (Ctrl + / Ctrl -)
      if (e.ctrlKey || e.metaKey) {
        if (e.key === '+' || e.key === '=') {
          e.preventDefault();
          increaseFontSize();
        } else if (e.key === '-' || e.key === '_') {
          e.preventDefault();
          decreaseFontSize();
        } else if (e.key === '0') {
          e.preventDefault();
          resetFontSize();
        }
      }

      // Zoom controls (Alt + / Alt -)
      if (e.altKey) {
        if (e.key === '+' || e.key === '=') {
          e.preventDefault();
          zoomIn();
        } else if (e.key === '-' || e.key === '_') {
          e.preventDefault();
          zoomOut();
        } else if (e.key === '0') {
          e.preventDefault();
          resetZoom();
        } else if (e.key === 'a' || e.key === 'A') {
          e.preventDefault();
          const toggle = document.getElementById('navAccessibilityToggle');
          if (toggle) toggle.click();
        }
      }
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAccessibility);
  } else {
    initAccessibility();
  }
})();


