document.addEventListener("DOMContentLoaded", () => {
    const templateSelectionContainer = document.getElementById("template-selection-container");
    const generatorUI = document.getElementById("generator-ui");

    // --- Helper function to dynamically load a script ---
    const loadScript = (src) => {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = () => resolve();
            script.onerror = () => reject(new Error(`Script load error for ${src}`));
            document.head.appendChild(script);
        });
    };

    // --- Renders the template selection cards ---
    const renderTemplateCards = (templates) => {
        if (templates.length === 0) {
            templateSelectionContainer.innerHTML = '<p>No document templates are available at this time.</p>';
            return;
        }

        templates.forEach(template => {
            const card = document.createElement('a');
            card.href = "#"; // Prevent page reload
            card.className = "feature-card";
            card.setAttribute('data-template-name', template.name);
            card.setAttribute('data-template-js', template.js_file_path);

            card.innerHTML = `
                <div class="feature-icon ${template.icon_class.includes('fa-') ? '' : 'blue'}">
                    <i class="${template.icon_class}"></i>
                </div>
                <h3>${template.name}</h3>
                <p>${template.description}</p>
            `;

            // --- Add click listener ---
            card.addEventListener('click', (e) => {
                e.preventDefault();
                loadTemplate(template);
            });

            templateSelectionContainer.appendChild(card);
        });
    };

    // --- Loads a specific template's UI ---
    const loadTemplate = async (template) => {
        // 1. Hide selection, show generator UI
        templateSelectionContainer.style.display = 'none';
        generatorUI.style.display = 'grid'; // Use grid for 2-col layout

        // 2. Load the specific JS file for this template
        try {
            // We get the static path from the template object
            const staticPrefix = template.js_file_path.startsWith('js/') ? '/static/' : '';
            await loadScript(`${staticPrefix}${template.js_file_path}`);

            // 3. Check if the script loaded correctly and initialized itself
            if (typeof window.initializeTemplate === 'function') {
                // This global function is defined in the script we just loaded
                window.initializeTemplate();
            } else {
                throw new Error("Template script loaded but failed to initialize.");
            }
        } catch (error) {
            console.error(error);
            document.getElementById('form-content').innerHTML =
                '<p class="alert alert-danger">Error: Could not load the document template.</p>';
        }
    };

    // --- Initial Fetch ---
    const fetchTemplates = async () => {
        try {
            const response = await fetch('/generator/api/templates/');
            if (!response.ok) {
                throw new Error('Failed to fetch document templates.');
            }
            const templates = await response.json();
            renderTemplateCards(templates);
        } catch (error) {
            console.error(error);
            templateSelectionContainer.innerHTML =
                '<p class="alert alert-danger">Could not load document templates. Please try again later.</p>';
        }
    };

    fetchTemplates();
});
