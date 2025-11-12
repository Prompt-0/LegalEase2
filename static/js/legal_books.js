document.addEventListener("DOMContentLoaded", () => {
    const actsContainer = document.getElementById("acts-container");
    const loadingIndicator = document.getElementById("loading-indicator");
    const searchInput = document.getElementById("book-search");

    let allActsData = []; // To cache the data

    // --- Helper function to create elements ---
    const e = (tag, attributes = {}, children = []) => {
        const element = document.createElement(tag);
        for (const key in attributes) {
            element[key] = attributes[key];
        }
        for (const child of children) {
            element.appendChild(child);
        }
        return element;
    };

    // --- Renders all acts to the DOM ---
    const renderActs = (acts) => {
        actsContainer.innerHTML = '';
        if (acts.length === 0) {
            actsContainer.innerHTML = '<p>No acts found.</p>';
            return;
        }

        acts.forEach(act => {
            const actCard = e('div', { className: 'card accordion' }, [
                e('div', { className: 'card-header accordion-header' }, [
                    e('h3', { textContent: `${act.name} (${act.category})` }),
                    e('i', { className: 'fas fa-chevron-right' })
                ]),
                e('div', { className: 'card-body accordion-content' }, [
                    e('p', { textContent: act.description }),
                    ...act.chapters.map(chapter =>
                        e('div', { className: 'accordion' }, [
                            e('div', { className: 'accordion-header nested' }, [
                                e('h4', { textContent: `Ch. ${chapter.chapter_number}: ${chapter.title}` }),
                                e('i', { className: 'fas fa-chevron-right' })
                            ]),
                            e('div', { className: 'accordion-content nested' }, [
                                ...chapter.sections.map(section =>
                                    e('div', { className: 'section-item' }, [
                                        e('h5', { textContent: `Section ${section.section_number}: ${section.title}` }),
                                        e('p', { textContent: section.content })
                                    ])
                                )
                            ])
                        ])
                    )
                ])
            ]);
            actsContainer.appendChild(actCard);
        });
    };

    // --- Filter the data based on search ---
    const filterData = (query) => {
        const lowerQuery = query.toLowerCase();

        // Deep copy the data to not modify the cache
        const filteredActs = JSON.parse(JSON.stringify(allActsData));

        return filteredActs.filter(act => {
            let actMatches = act.name.toLowerCase().includes(lowerQuery) ||
                             act.description.toLowerCase().includes(lowerQuery);

            act.chapters = act.chapters.filter(chapter => {
                let chapterMatches = chapter.title.toLowerCase().includes(lowerQuery);

                chapter.sections = chapter.sections.filter(section => {
                    return section.title.toLowerCase().includes(lowerQuery) ||
                           section.content.toLowerCase().includes(lowerQuery) ||
                           section.section_number.toLowerCase().includes(lowerQuery);
                });

                return chapter.sections.length > 0 || chapterMatches;
            });

            return act.chapters.length > 0 || actMatches;
        });
    };

    // --- Event listener for search input ---
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value;
        const filteredActs = filterData(query);
        renderActs(filteredActs);
        // If searching, auto-expand all accordions
        if (query) {
            document.querySelectorAll('.accordion-content').forEach(el => el.classList.add('show'));
            document.querySelectorAll('.accordion-header i').forEach(el => el.classList.replace('fa-chevron-right', 'fa-chevron-down'));
        }
    });

    // --- Toggle logic for accordions ---
    actsContainer.addEventListener('click', (e) => {
        const header = e.target.closest('.accordion-header');
        if (header) {
            const content = header.nextElementSibling;
            const icon = header.querySelector('i');

            content.classList.toggle('show');
            if (content.classList.contains('show')) {
                icon.classList.replace('fa-chevron-right', 'fa-chevron-down');
            } else {
                icon.classList.replace('fa-chevron-down', 'fa-chevron-right');
            }
        }
    });

    // --- Initial fetch ---
    const loadActs = async () => {
        try {
            const response = await fetch('/tools/api/acts/');
            if (!response.ok) {
                throw new Error('Failed to load legal acts.');
            }
            allActsData = await response.json();
            renderActs(allActsData);
            loadingIndicator.style.display = 'none';
        } catch (error) {
            console.error(error);
            loadingIndicator.innerHTML = '<p class="alert alert-danger">Could not load legal acts.</p>';
        }
    };

    loadActs();
});
