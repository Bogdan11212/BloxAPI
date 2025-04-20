// Main JavaScript functionality for the Roblox API documentation

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

    // Add copy functionality to code blocks
    document.querySelectorAll('.code-block').forEach(block => {
        // Create a button element
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-info copy-btn';
        copyButton.textContent = 'Copy';
        copyButton.setAttribute('data-bs-toggle', 'tooltip');
        copyButton.setAttribute('data-bs-title', 'Copy to clipboard');

        // Get the parent element and prepend the button
        const parent = block.parentElement;
        const buttonWrapper = document.createElement('div');
        buttonWrapper.className = 'd-flex justify-content-end mb-2';
        buttonWrapper.appendChild(copyButton);
        parent.insertBefore(buttonWrapper, block);

        // Add click event listener to the button
        copyButton.addEventListener('click', () => {
            // Copy text to clipboard
            navigator.clipboard.writeText(block.textContent.trim()).then(() => {
                // Change button text temporarily
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            // Check if the link has a hash
            if (this.hash !== '') {
                e.preventDefault();

                // Get the target element
                const target = document.querySelector(this.hash);
                if (target) {
                    // Scroll to the target
                    window.scrollTo({
                        top: target.offsetTop - 70, // Adjust for fixed navbar
                        behavior: 'smooth'
                    });

                    // Update URL
                    history.pushState(null, null, this.hash);
                }
            }
        });
    });

    // Toggle endpoint examples
    document.querySelectorAll('.toggle-example').forEach(button => {
        button.addEventListener('click', function() {
            const exampleId = this.getAttribute('data-target');
            const exampleElement = document.getElementById(exampleId);
            
            if (exampleElement.classList.contains('d-none')) {
                exampleElement.classList.remove('d-none');
                this.textContent = 'Hide Example';
            } else {
                exampleElement.classList.add('d-none');
                this.textContent = 'Show Example';
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

    // Test API functionality
    const testApiForm = document.getElementById('test-api-form');
    if (testApiForm) {
        testApiForm.addEventListener('submit', function(e) {
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
                resultOutput.textContent = 'Error: Invalid JSON in parameters';
                resultOutput.classList.add('text-danger');
                return;
            }
            
            // Display loading state
            resultOutput.textContent = 'Loading...';
            resultOutput.classList.remove('text-danger');
            
            // Make API request
            let fetchOptions = {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            
            if (method !== 'GET' && Object.keys(params).length > 0) {
                fetchOptions.body = JSON.stringify(params);
            }
            
            let url = endpoint;
            if (method === 'GET' && Object.keys(params).length > 0) {
                const queryParams = new URLSearchParams();
                for (const [key, value] of Object.entries(params)) {
                    queryParams.append(key, value);
                }
                url = `${endpoint}?${queryParams.toString()}`;
            }
            
            fetch(url, fetchOptions)
                .then(response => response.json())
                .then(data => {
                    resultOutput.textContent = JSON.stringify(data, null, 2);
                    resultOutput.classList.remove('text-danger');
                })
                .catch(err => {
                    resultOutput.textContent = `Error: ${err.message}`;
                    resultOutput.classList.add('text-danger');
                });
        });
    }
});
