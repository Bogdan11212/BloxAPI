/**
 * BloxAPI main JavaScript file
 */

// Initialize all tooltips on the page
function initTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// Initialize all popovers on the page
function initPopovers() {
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
}

// Copy text to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(
    () => {
      // Success
      console.log('Copied to clipboard');
    },
    (err) => {
      // Error
      console.error('Could not copy text: ', err);
    }
  );
}

// Copy API key functionality
function setupCopyButtons() {
  const copyButtons = document.querySelectorAll('.copy-btn');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const textToCopy = this.getAttribute('data-copy-text');
      copyToClipboard(textToCopy);
      
      // Change button text temporarily
      const originalHTML = this.innerHTML;
      this.innerHTML = '<i data-feather="check"></i> Copied!';
      feather.replace();
      
      // Reset button after 2 seconds
      setTimeout(() => {
        this.innerHTML = originalHTML;
        feather.replace();
      }, 2000);
    });
  });
}

// Interactive API endpoint demo functionality
function setupEndpointDemos() {
  const demoButtons = document.querySelectorAll('.demo-endpoint-btn');
  demoButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const endpoint = this.getAttribute('data-endpoint');
      const resultContainer = document.getElementById(this.getAttribute('data-result-container'));
      const loadingSpinner = this.querySelector('.spinner-border');
      
      // Show loading spinner
      if (loadingSpinner) {
        loadingSpinner.classList.remove('d-none');
      }
      
      // Simulate API call
      setTimeout(() => {
        fetch(endpoint)
          .then(response => response.json())
          .then(data => {
            resultContainer.innerHTML = `<pre><code>${JSON.stringify(data, null, 2)}</code></pre>`;
            if (loadingSpinner) {
              loadingSpinner.classList.add('d-none');
            }
          })
          .catch(error => {
            resultContainer.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
            if (loadingSpinner) {
              loadingSpinner.classList.add('d-none');
            }
          });
      }, 500);
    });
  });
}

// Smooth scrolling for anchor links
function setupSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 70,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Toggle code samples between different languages
function setupCodeToggle() {
  const codeToggles = document.querySelectorAll('.code-toggle-btn');
  codeToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const target = this.getAttribute('data-target');
      const lang = this.getAttribute('data-lang');
      const codeBlocks = document.querySelectorAll(`[data-code-block="${target}"]`);
      
      // Hide all code blocks
      codeBlocks.forEach(block => {
        block.classList.add('d-none');
      });
      
      // Show the selected language block
      document.querySelector(`[data-code-block="${target}"][data-lang="${lang}"]`).classList.remove('d-none');
      
      // Update active button
      document.querySelectorAll(`.code-toggle-btn[data-target="${target}"]`).forEach(btn => {
        btn.classList.remove('active');
      });
      this.classList.add('active');
    });
  });
}

// Stats counter animation
function animateStatCounters() {
  const counters = document.querySelectorAll('.counter');
  
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-target'), 10);
    const duration = 2000; // 2 seconds
    const step = target / (duration / 16); // 60fps
    
    let current = 0;
    const startTime = performance.now();
    
    function updateCounter(timestamp) {
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      current = Math.floor(progress * target);
      counter.textContent = current.toLocaleString();
      
      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = target.toLocaleString();
      }
    }
    
    requestAnimationFrame(updateCounter);
  });
}

// Initialize everything when the DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initTooltips();
  initPopovers();
  setupCopyButtons();
  setupEndpointDemos();
  setupSmoothScrolling();
  setupCodeToggle();
  
  // Check if we have counter elements on the page
  if (document.querySelectorAll('.counter').length > 0) {
    // Only animate counters if they're in viewport
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateStatCounters();
          observer.disconnect();
        }
      });
    });
    
    observer.observe(document.querySelector('.counter'));
  }
});