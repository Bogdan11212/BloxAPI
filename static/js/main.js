// Modern JavaScript functionality for the Roblox API documentation

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Modern copy button functionality
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-code-target');
            const codeBlock = document.getElementById(targetId);
            
            if (codeBlock) {
                // Copy text to clipboard
                navigator.clipboard.writeText(codeBlock.textContent.trim()).then(() => {
                    // Change button text temporarily
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    button.classList.add('btn-success');
                    
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.classList.remove('btn-success');
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                    button.textContent = 'Error!';
                    button.classList.add('btn-danger');
                    
                    setTimeout(() => {
                        button.textContent = 'Copy';
                        button.classList.remove('btn-danger');
                    }, 2000);
                });
            }
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            // Check if the link has a hash and it's not just '#'
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();

                // Get the target element
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    // Scroll to the target with smooth behavior
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start',
                        inline: 'nearest'
                    });
                    
                    // Update URL without refreshing the page
                    window.history.pushState(null, '', targetId);
                }
            }
        });
    });

    // Add active class to current section in sidebar
    function setActiveNavItem() {
        // Get current scroll position
        const scrollPosition = window.scrollY + 100; // Add offset for navbar

        // Find all section elements
        document.querySelectorAll('section[id]').forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            // Check if current scroll position is within this section
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                // Remove active class from all nav items
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                
                // Add active class to corresponding nav item
                const correspondingNavItem = document.querySelector(`.nav-link[href="#${sectionId}"]`);
                if (correspondingNavItem) {
                    correspondingNavItem.classList.add('active');
                }
            }
        });
    }

    // Add scroll event listener
    window.addEventListener('scroll', setActiveNavItem);
    
    // Set active nav item on page load
    setActiveNavItem();

    // Advanced API Explorer functionality
    
    // User API Tab
    if (document.querySelector('.user-endpoint-select')) {
        // Handle User API Endpoint selection change
        document.querySelector('.user-endpoint-select').addEventListener('change', function() {
            const selectedEndpoint = this.value;
            
            // Hide all input fields first
            document.querySelector('.user-id-input').classList.add('d-none');
            document.querySelector('.user-keyword-input').classList.add('d-none');
            document.querySelector('.user-ids-input').classList.add('d-none');
            
            // Show relevant input fields based on selected endpoint
            if (selectedEndpoint.includes('{id}')) {
                document.querySelector('.user-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('search')) {
                document.querySelector('.user-keyword-input').classList.remove('d-none');
            } else if (selectedEndpoint === '/api/users') {
                document.querySelector('.user-ids-input').classList.remove('d-none');
            }
        });
        
        // Handle User API Send Request button
        document.querySelector('.user-send-request').addEventListener('click', function() {
            const selectedEndpoint = document.querySelector('.user-endpoint-select').value;
            let endpoint = selectedEndpoint;
            let params = {};
            
            // Replace parameters in endpoint and prepare request
            if (endpoint.includes('{id}')) {
                const userId = document.querySelector('.user-id-input input').value.trim();
                endpoint = endpoint.replace('{id}', userId);
            } else if (endpoint.includes('search')) {
                const keyword = document.querySelector('.user-keyword-input input').value.trim();
                params.keyword = keyword;
                params.limit = 5;
            } else if (endpoint === '/api/users') {
                const userIdsString = document.querySelector('.user-ids-input input').value.trim();
                const userIds = userIdsString.split(',').map(id => id.trim()).filter(id => id);
                return makePostRequest(endpoint, { userIds: userIds }, '.user-result');
            }
            
            makeGetRequest(endpoint, params, '.user-result');
        });
    }
    
    // Game API Tab
    if (document.querySelector('.game-endpoint-select')) {
        // Handle Game API Endpoint selection change
        document.querySelector('.game-endpoint-select').addEventListener('change', function() {
            const selectedEndpoint = this.value;
            
            // Hide all input fields first
            document.querySelector('.game-id-input').classList.add('d-none');
            document.querySelector('.game-user-id-input').classList.add('d-none');
            
            // Show relevant input fields based on selected endpoint
            if (selectedEndpoint.includes('{id}')) {
                document.querySelector('.game-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('user_id')) {
                document.querySelector('.game-user-id-input').classList.remove('d-none');
            }
        });
        
        // Handle Game API Send Request button
        document.querySelector('.game-send-request').addEventListener('click', function() {
            const selectedEndpoint = document.querySelector('.game-endpoint-select').value;
            let endpoint = selectedEndpoint;
            let params = {};
            
            // Replace parameters in endpoint and prepare request
            if (endpoint.includes('{id}')) {
                const gameId = document.querySelector('.game-id-input input').value.trim();
                endpoint = endpoint.replace('{id}', gameId);
            } else if (endpoint.includes('user_id')) {
                const userId = document.querySelector('.game-user-id-input input').value.trim();
                params.user_id = userId;
            }
            
            makeGetRequest(endpoint, params, '.game-result');
        });
    }
    
    // Group API Tab
    if (document.querySelector('.group-endpoint-select')) {
        // Handle Group API Endpoint selection change
        document.querySelector('.group-endpoint-select').addEventListener('change', function() {
            // All group endpoints need the group ID, so nothing to toggle
        });
        
        // Handle Group API Send Request button
        document.querySelector('.group-send-request').addEventListener('click', function() {
            const selectedEndpoint = document.querySelector('.group-endpoint-select').value;
            let endpoint = selectedEndpoint;
            
            // Replace group ID in endpoint
            const groupId = document.querySelector('.group-id-input input').value.trim();
            endpoint = endpoint.replace('{id}', groupId);
            
            makeGetRequest(endpoint, {}, '.group-result');
        });
    }
    
    // Events API Tab
    if (document.querySelector('.events-endpoint-select')) {
        // Handle Events API Endpoint selection change
        document.querySelector('.events-endpoint-select').addEventListener('change', function() {
            const selectedEndpoint = this.value;
            
            // Hide all input fields first
            document.querySelector('.events-user-id-input').classList.add('d-none');
            document.querySelector('.events-game-id-input').classList.add('d-none');
            document.querySelector('.events-group-id-input').classList.add('d-none');
            document.querySelector('.events-entity-input').classList.add('d-none');
            
            // Show relevant input fields based on selected endpoint
            if (selectedEndpoint.includes('users')) {
                document.querySelector('.events-user-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('games')) {
                document.querySelector('.events-game-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('groups')) {
                document.querySelector('.events-group-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('history')) {
                document.querySelector('.events-entity-input').classList.remove('d-none');
            }
        });
        
        // Handle Events API Send Request button
        document.querySelector('.events-send-request').addEventListener('click', function() {
            const selectedEndpoint = document.querySelector('.events-endpoint-select').value;
            let endpoint = selectedEndpoint;
            let params = {max_rows: 10};
            
            // Replace parameters in endpoint and prepare request
            if (endpoint.includes('users')) {
                const userId = document.querySelector('.events-user-id-input input').value.trim();
                endpoint = endpoint.replace('{user_id}', userId);
            } else if (endpoint.includes('games')) {
                const universeId = document.querySelector('.events-game-id-input input').value.trim();
                endpoint = endpoint.replace('{universe_id}', universeId);
            } else if (endpoint.includes('groups')) {
                const groupId = document.querySelector('.events-group-id-input input').value.trim();
                endpoint = endpoint.replace('{group_id}', groupId);
            } else if (endpoint.includes('history')) {
                const entityType = document.querySelector('.events-entity-input select').value.trim();
                const entityId = document.querySelector('.events-entity-input input').value.trim();
                endpoint = endpoint.replace('{entity_type}', entityType).replace('{entity_id}', entityId);
            }
            
            makeGetRequest(endpoint, params, '.events-result');
        });
    }
    
    // Moderation API Tab
    if (document.querySelector('.moderation-endpoint-select')) {
        // Handle Moderation API Endpoint selection change
        document.querySelector('.moderation-endpoint-select').addEventListener('change', function() {
            const selectedEndpoint = this.value;
            
            // Hide all input fields first
            document.querySelector('.moderation-content-input').classList.add('d-none');
            document.querySelector('.moderation-user-id-input').classList.add('d-none');
            document.querySelector('.moderation-asset-id-input').classList.add('d-none');
            document.querySelector('.moderation-text-input').classList.add('d-none');
            
            // Show relevant input fields based on selected endpoint
            if (selectedEndpoint.includes('content')) {
                document.querySelector('.moderation-content-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('users')) {
                document.querySelector('.moderation-user-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('assets')) {
                document.querySelector('.moderation-asset-id-input').classList.remove('d-none');
            } else if (selectedEndpoint.includes('text')) {
                document.querySelector('.moderation-text-input').classList.remove('d-none');
            }
        });
        
        // Handle Moderation API Send Request button
        document.querySelector('.moderation-send-request').addEventListener('click', function() {
            const selectedEndpoint = document.querySelector('.moderation-endpoint-select').value;
            let endpoint = selectedEndpoint;
            let params = {};
            
            // Handle different endpoints
            if (endpoint.includes('content')) {
                const contentType = document.querySelector('.moderation-content-input select').value.trim();
                const contentId = document.querySelector('.moderation-content-input input').value.trim();
                endpoint = endpoint.replace('{content_type}', contentType).replace('{content_id}', contentId);
                makeGetRequest(endpoint, params, '.moderation-result');
            } else if (endpoint.includes('users')) {
                const userId = document.querySelector('.moderation-user-id-input input').value.trim();
                endpoint = endpoint.replace('{user_id}', userId);
                makeGetRequest(endpoint, params, '.moderation-result');
            } else if (endpoint.includes('assets')) {
                const assetId = document.querySelector('.moderation-asset-id-input input').value.trim();
                endpoint = endpoint.replace('{asset_id}', assetId);
                makeGetRequest(endpoint, params, '.moderation-result');
            } else if (endpoint.includes('text')) {
                const text = document.querySelector('.moderation-text-input textarea').value.trim();
                makePostRequest(endpoint, {text: text}, '.moderation-result');
            }
        });
    }
    
    // Statistics API Tab
    if (document.querySelector('.statistics-endpoint-select')) {
        // Handle Statistics API Endpoint selection change
        document.querySelector('.statistics-endpoint-select').addEventListener('change', function() {
            const selectedEndpoint = this.value;
            
            // Hide/Show Universe ID input based on selected endpoint
            if (selectedEndpoint.includes('trending')) {
                document.querySelector('.statistics-game-id-input').classList.add('d-none');
            } else {
                document.querySelector('.statistics-game-id-input').classList.remove('d-none');
            }
            
            // Hide/Show date range based on selected endpoint
            if (selectedEndpoint.includes('playtime') || selectedEndpoint.includes('retention')) {
                document.querySelector('.statistics-params-input').classList.remove('d-none');
            } else {
                document.querySelector('.statistics-params-input').classList.add('d-none');
            }
        });
        
        // Handle Statistics API Send Request button
        document.querySelector('.statistics-send-request').addEventListener('click', function() {
            const selectedEndpoint = document.querySelector('.statistics-endpoint-select').value;
            let endpoint = selectedEndpoint;
            let params = {};
            
            // Replace parameters in endpoint and prepare request
            if (!endpoint.includes('trending')) {
                const universeId = document.querySelector('.statistics-game-id-input input').value.trim();
                endpoint = endpoint.replace('{universe_id}', universeId);
                
                // Add date range parameters if needed
                if (endpoint.includes('playtime') || endpoint.includes('retention')) {
                    const dateInputs = document.querySelectorAll('.statistics-params-input input');
                    if (dateInputs[0].value) params.start_time = dateInputs[0].value;
                    if (dateInputs[1].value) params.end_time = dateInputs[1].value;
                }
            } else {
                // Add trending filters
                params.category = 'all';
                params.limit = 10;
            }
            
            makeGetRequest(endpoint, params, '.statistics-result');
        });
    }
    
    // Custom API Test Form
    const customApiForm = document.getElementById('custom-api-form');
    if (customApiForm) {
        customApiForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const endpointInput = document.getElementById('endpoint-input');
            const methodSelect = document.getElementById('method-select');
            const paramsInput = document.getElementById('params-input');
            const resultOutput = document.getElementById('api-result');
            
            if (!endpointInput || !methodSelect || !resultOutput) return;
            
            const endpoint = endpointInput.value.trim();
            const method = methodSelect.value;
            let params = {};
            
            try {
                if (paramsInput && paramsInput.value.trim()) {
                    params = JSON.parse(paramsInput.value);
                }
            } catch (err) {
                resultOutput.innerHTML = `<div class="text-danger">Error: Invalid JSON in parameters</div>`;
                return;
            }
            
            // Display loading state
            resultOutput.innerHTML = `<div class="text-center p-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Sending request...</p>
            </div>`;
            
            // Make API request based on method
            if (method === 'GET') {
                makeGetRequest(endpoint, params, '#api-result');
            } else if (method === 'POST') {
                makePostRequest(endpoint, params, '#api-result');
            } else {
                makeCustomRequest(endpoint, method, params, '#api-result');
            }
        });
    }
    
    // Helper Functions for API Requests
    
    // Function to make GET requests
    function makeGetRequest(endpoint, params, resultSelector) {
        const resultContainer = document.querySelector(resultSelector);
        resultContainer.innerHTML = `<div class="text-center p-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Fetching data...</p>
        </div>`;
        
        // Build URL with query parameters
        let url = endpoint;
        if (Object.keys(params).length > 0) {
            const queryParams = new URLSearchParams();
            for (const [key, value] of Object.entries(params)) {
                queryParams.append(key, value);
            }
            url = `${endpoint}?${queryParams.toString()}`;
        }
        
        // Make the request
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Format JSON with syntax highlighting
                resultContainer.innerHTML = `<pre class="m-0">${syntaxHighlight(JSON.stringify(data, null, 2))}</pre>`;
            })
            .catch(error => {
                resultContainer.innerHTML = `<div class="text-danger">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Error: ${error.message}
                </div>`;
            });
    }
    
    // Function to make POST requests
    function makePostRequest(endpoint, data, resultSelector) {
        const resultContainer = document.querySelector(resultSelector);
        resultContainer.innerHTML = `<div class="text-center p-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Sending data...</p>
        </div>`;
        
        // Make the request
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Format JSON with syntax highlighting
                resultContainer.innerHTML = `<pre class="m-0">${syntaxHighlight(JSON.stringify(data, null, 2))}</pre>`;
            })
            .catch(error => {
                resultContainer.innerHTML = `<div class="text-danger">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Error: ${error.message}
                </div>`;
            });
    }
    
    // Function to make custom method requests (PUT, DELETE, etc.)
    function makeCustomRequest(endpoint, method, data, resultSelector) {
        const resultContainer = document.querySelector(resultSelector);
        resultContainer.innerHTML = `<div class="text-center p-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Processing ${method} request...</p>
        </div>`;
        
        // Make the request
        fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Format JSON with syntax highlighting
                resultContainer.innerHTML = `<pre class="m-0">${syntaxHighlight(JSON.stringify(data, null, 2))}</pre>`;
            })
            .catch(error => {
                resultContainer.innerHTML = `<div class="text-danger">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    Error: ${error.message}
                </div>`;
            });
    }
    
    // JSON syntax highlighting function
    function syntaxHighlight(json) {
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            let cls = 'text-info'; // strings
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'text-primary'; // keys
                }
            } else if (/true|false/.test(match)) {
                cls = 'text-success'; // booleans
            } else if (/null/.test(match)) {
                cls = 'text-danger'; // null
            } else {
                cls = 'text-warning'; // numbers
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }
    
    // Initialize the endpoint selectors to show the default input fields
    if (document.querySelector('.user-endpoint-select')) {
        document.querySelector('.user-endpoint-select').dispatchEvent(new Event('change'));
    }
    if (document.querySelector('.game-endpoint-select')) {
        document.querySelector('.game-endpoint-select').dispatchEvent(new Event('change'));
    }
});
