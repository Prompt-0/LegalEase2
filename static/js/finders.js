document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("search-btn");
    const resultsContainer = document.getElementById("results-container");
    const loadingIndicator = document.getElementById("loading-indicator");

    // Determine which page we're on and set up config
    let config = {};
    if (document.getElementById('lawyer-search')) {
        config = {
            searchInputId: 'lawyer-search',
            apiEndpoint: '/finders/api/lawyers/',
            renderFunction: renderLawyer,
            placeholder: 'No lawyers found matching your search.'
        };
    } else if (document.getElementById('station-search')) {
        config = {
            searchInputId: 'station-search',
            apiEndpoint: '/finders/api/stations/',
            renderFunction: renderStation,
            placeholder: 'No police stations found matching your search.'
        };
    } else if (document.getElementById('case-search')) {
        config = {
            searchInputId: 'case-search',
            apiEndpoint: '/finders/api/cases/',
            renderFunction: renderCase,
            placeholder: 'No cases found matching your search.'
        };
    } else if (document.getElementById('helpline-search')) { // <-- NEW CONFIG
        config = {
            searchInputId: 'helpline-search',
            apiEndpoint: '/finders/api/helplines/',
            renderFunction: renderHelpline,
            placeholder: 'No helplines found matching your search.'
        };
    }

    const searchInput = document.getElementById(config.searchInputId);

    // Attach event listeners
    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
        // Run an initial empty search to show all items
        performSearch();
    }

    // --- Main Search Function ---
    async function performSearch() {
        const query = searchInput.value.trim();

        loadingIndicator.style.display = 'block';
        resultsContainer.innerHTML = '';

        try {
            const response = await fetch(`${config.apiEndpoint}?search=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();

            if (data.length === 0) {
                resultsContainer.innerHTML = `<p>${config.placeholder}</p>`;
            } else {
                data.forEach(item => {
                    resultsContainer.appendChild(config.renderFunction(item));
                });
            }
        } catch (error) {
            console.error('Fetch error:', error);
            resultsContainer.innerHTML = '<p class="alert alert-danger">An error occurred while fetching results. Please try again.</p>';
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    // --- Render Functions ---

    function renderLawyer(lawyer) {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.marginBottom = '1rem';

        let name = lawyer.user.username;
        if (lawyer.user.first_name || lawyer.user.last_name) {
            name = `${lawyer.user.first_name} ${lawyer.user.last_name}`.trim();
        }

        card.innerHTML = `
            <div class="card-body">
                <h3>${name}</h3>
                <p style="margin-bottom: 0.5rem;">
                    <strong>Specialization:</strong> ${lawyer.specialization || 'N/A'}
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong>Location:</strong> ${lawyer.location || 'N/A'}
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong>Experience:</strong> ${lawyer.experience_years || 'N/A'} years
                </p>
                <p style="margin-bottom: 0;">
                    <strong>Contact:</strong> ${lawyer.phone_number || 'N/A'}
                </p>
            </div>
        `;
        return card;
    }

    function renderStation(station) {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.marginBottom = '1rem';
        card.innerHTML = `
            <div class="card-body">
                <h3>${station.name}</h3>
                <p style="margin-bottom: 0.5rem;">
                    <strong>Address:</strong> ${station.address || 'N/A'}
                </p>
                <p style="margin-bottom: 0.5rem;">
                    <strong>District:</strong> ${station.district || 'N/A'} (Pincode: ${station.pincode || 'N/A'})
                </p>
                <p style="margin-bottom: 0;">
                    <strong>Phone:</strong> ${station.phone_number || 'N/A'}
                </p>
            </div>
        `;
        return card;
    }

    function renderCase(legalCase) {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.marginBottom = '1rem';
        card.innerHTML = `
            <div class="card-header">
                <h3>${legalCase.title}</h3>
            </div>
            <div class="card-body">
                <p style="margin-bottom: 0.5rem;">
                    <strong>Category:</strong> ${legalCase.category || 'N/A'}
                </p>
                <p><strong>Summary:</strong> ${legalCase.summary}</p>
            </div>
        `;
        return card;
    }

    // --- NEW: Render function for Helplines ---
    function renderHelpline(helpline) {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.marginBottom = '1rem';
        card.innerHTML = `
            <div class="card-body">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <h3 style="margin-bottom: 0.5rem;">${helpline.name}</h3>
                    <span class="helpline-category">${helpline.category || 'General'}</span>
                </div>
                <h4 class="helpline-number">${helpline.phone_number}</h4>
                <p>${helpline.description || 'No description available.'}</p>
                <a href="tel:${helpline.phone_number}" class="btn btn-primary" style="margin-top: 1rem;">
                    <i class="fas fa-phone"></i> Call Now
                </a>
            </div>
        `;
        return card;
    }
});
