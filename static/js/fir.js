document.addEventListener("DOMContentLoaded", () => {
    const firGrid = document.getElementById("fir-grid");
    const loading = document.getElementById("loading");

    if (firGrid) {
        fetch("/static/data/fir.json") // Changed this path for Django
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (loading) {
                    loading.style.display = 'none';
                }
                displayFIRLinks(data);
            })
            .catch(error => {
                console.error("Failed to load FIR data:", error);
                if (loading) {
                    loading.style.display = 'none';
                }
                if (firGrid) {
                    firGrid.innerHTML = "<p>Error loading FIR links. Please try again later.</p>";
                }
            });
    }

    function displayFIRLinks(links) {
        if (!firGrid) return;
        firGrid.innerHTML = ""; // Clear loading or error message
        links.forEach(link => {
            const card = document.createElement("div");
            card.className = "fir-card";
            card.innerHTML = `
                <div class="fir-card-content">
                    <h3 class="fir-state-name">${link.state}</h3>
                    <a href="${link.url}" class="fir-button" target="_blank" rel="noopener noreferrer">
                        Go to Portal <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>
            `;
            firGrid.appendChild(card);
        });
    }
});
