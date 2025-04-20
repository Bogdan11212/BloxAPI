// Demo JavaScript for BloxAPI Integrations

document.addEventListener('DOMContentLoaded', function() {
  // Initialize the copy buttons
  initCopyButtons();
  
  // Initialize the API demos
  initApiDemos();
  
  // Initialize animation effects
  initAnimations();
});

// Copy code to clipboard functionality
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', function() {
      const codeTarget = this.getAttribute('data-code-target');
      const codeBlock = document.getElementById(codeTarget);
      
      if (codeBlock) {
        navigator.clipboard.writeText(codeBlock.textContent.trim())
          .then(() => {
            // Add copied class for animation
            this.classList.add('copied');
            // Reset after animation completes
            setTimeout(() => {
              this.classList.remove('copied');
            }, 1500);
          })
          .catch(err => {
            console.error('Could not copy text: ', err);
          });
      }
    });
  });
}

// API Demo functionality
function initApiDemos() {
  // Handle Rolimon's Item Details Demo
  const rolimonItemForm = document.getElementById('rolimon-item-form');
  if (rolimonItemForm) {
    rolimonItemForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const itemId = document.getElementById('rolimon-item-id').value.trim();
      if (!itemId) return;
      
      const resultContainer = document.getElementById('rolimon-result');
      resultContainer.innerHTML = '<div class="d-flex justify-content-center my-5"><div class="loading-spinner"></div></div>';
      
      fetch(`/api/external/rolimon/items/${itemId}`)
        .then(response => response.json())
        .then(data => {
          displayJsonResult(data, resultContainer);
        })
        .catch(error => {
          resultContainer.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    });
  }
  
  // Handle Rblx.Trade Demo
  const rblxTradeForm = document.getElementById('rblx-trade-form');
  if (rblxTradeForm) {
    rblxTradeForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const offerItems = document.getElementById('trade-offer-items').value.trim();
      const requestItems = document.getElementById('trade-request-items').value.trim();
      
      if (!offerItems || !requestItems) {
        alert('Please enter both offer and request items');
        return;
      }
      
      // Parse comma-separated values into arrays of integers
      const offerItemIds = offerItems.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
      const requestItemIds = requestItems.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
      
      if (offerItemIds.length === 0 || requestItemIds.length === 0) {
        alert('Please enter valid item IDs (comma-separated numbers)');
        return;
      }
      
      const resultContainer = document.getElementById('rblx-trade-result');
      resultContainer.innerHTML = '<div class="d-flex justify-content-center my-5"><div class="loading-spinner"></div></div>';
      
      fetch('/api/external/rblx-trade/trade-calculator', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          offer_items: offerItemIds,
          request_items: requestItemIds
        })
      })
        .then(response => response.json())
        .then(data => {
          displayJsonResult(data, resultContainer);
        })
        .catch(error => {
          resultContainer.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    });
  }
  
  // Handle Roliverse Market Trends Demo
  const roliverseForm = document.getElementById('roliverse-form');
  if (roliverseForm) {
    roliverseForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const itemType = document.getElementById('market-item-type').value;
      const timePeriod = document.getElementById('market-time-period').value;
      
      const resultContainer = document.getElementById('roliverse-result');
      resultContainer.innerHTML = '<div class="d-flex justify-content-center my-5"><div class="loading-spinner"></div></div>';
      
      const params = new URLSearchParams({
        item_type: itemType,
        time_period: timePeriod
      });
      
      fetch(`/api/external/roliverse/market/trends?${params}`)
        .then(response => response.json())
        .then(data => {
          displayJsonResult(data, resultContainer);
        })
        .catch(error => {
          resultContainer.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    });
  }
  
  // Handle Rblx Values Rising Items Demo
  const rblxValuesForm = document.getElementById('rblx-values-form');
  if (rblxValuesForm) {
    rblxValuesForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const limit = document.getElementById('rising-items-limit').value;
      const resultContainer = document.getElementById('rblx-values-result');
      resultContainer.innerHTML = '<div class="d-flex justify-content-center my-5"><div class="loading-spinner"></div></div>';
      
      fetch(`/api/external/rblx-values/market/rising?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
          displayJsonResult(data, resultContainer);
        })
        .catch(error => {
          resultContainer.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        });
    });
  }
}

// Display JSON result with syntax highlighting
function displayJsonResult(data, container) {
  // Convert data to formatted JSON string
  const formattedJson = JSON.stringify(data, null, 2);
  
  // Create a code element
  const codeElement = document.createElement('pre');
  codeElement.className = 'code-output';
  
  // Apply syntax highlighting
  const highlightedJson = formattedJson
    .replace(/"([^"]+)":/g, '<span class="json-key">"$1"</span>:')
    .replace(/"([^"]+)"([,\n\r\]}])/g, '<span class="json-string">"$1"</span>$2')
    .replace(/: ([0-9]+)(,?)/g, ': <span class="json-number">$1</span>$2')
    .replace(/: (true|false)(,?)/g, ': <span class="json-boolean">$1</span>$2')
    .replace(/: (null)(,?)/g, ': <span class="json-null">$1</span>$2');
  
  codeElement.innerHTML = highlightedJson;
  
  // Clear the container and add the result
  container.innerHTML = '';
  container.appendChild(codeElement);
  
  // Add a copy button
  const copyBtn = document.createElement('button');
  copyBtn.className = 'btn btn-sm btn-outline-light copy-btn';
  copyBtn.textContent = 'Copy';
  copyBtn.addEventListener('click', function() {
    navigator.clipboard.writeText(formattedJson)
      .then(() => {
        copyBtn.classList.add('copied');
        setTimeout(() => {
          copyBtn.classList.remove('copied');
        }, 1500);
      });
  });
  
  container.appendChild(copyBtn);
}

// Initialize animation effects
function initAnimations() {
  // Add animation classes to elements
  document.querySelectorAll('.fade-in-up').forEach((element, index) => {
    element.classList.add(`delay-${(index % 5) + 1}`);
  });
  
  // Handle scroll animations
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  document.querySelectorAll('.animate-on-scroll').forEach(element => {
    observer.observe(element);
  });
}