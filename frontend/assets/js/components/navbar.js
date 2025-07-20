// Componente del navbar superior
class Navbar {
    constructor() {
        this.globalSearchData = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadGlobalSearchData();
    }

    bindEvents() {
        // Búsqueda global
        const globalSearch = document.getElementById('globalSearch');
        const globalSearchBtn = document.getElementById('globalSearchBtn');

        if (globalSearch) {
            // Búsqueda en tiempo real con debounce
            const debouncedSearch = Utils.debounce((query) => {
                this.performGlobalSearch(query);
            }, 300);

            globalSearch.addEventListener('input', (e) => {
                const query = e.target.value.trim();
                if (query.length >= 2) {
                    debouncedSearch(query);
                } else {
                    this.clearGlobalSearchResults();
                }
            });

            // Búsqueda al presionar Enter
            globalSearch.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const query = e.target.value.trim();
                    if (query) {
                        this.performGlobalSearch(query);
                    }
                }
            });
        }

        if (globalSearchBtn) {
            globalSearchBtn.addEventListener('click', () => {
                const query = globalSearch ? globalSearch.value.trim() : '';
                if (query) {
                    this.performGlobalSearch(query);
                }
            });
        }

        // Cerrar resultados al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar') && !e.target.closest('.global-search-results')) {
                this.clearGlobalSearchResults();
            }
        });
    }

    async loadGlobalSearchData() {
        try {
            // Cargar datos de todas las secciones para búsqueda global
            const sections = ['balances', 'sales', 'inventory', 'customers', 'reports'];
            const promises = sections.map(section => 
                Utils.fetchJson(`data/responses/${section}.json`)
            );

            const results = await Promise.allSettled(promises);
            
            this.globalSearchData = results
                .filter(result => result.status === 'fulfilled' && result.value)
                .map((result, index) => ({
                    section: sections[index],
                    data: result.value
                }));

        } catch (error) {
            Utils.handleError(error, 'Cargar datos de búsqueda global');
        }
    }

    async performGlobalSearch(query) {
        if (!query || query.length < 2) {
            this.clearGlobalSearchResults();
            return;
        }

        try {
            const results = [];
            const searchTerm = query.toLowerCase();

            // Buscar en cada sección
            for (const sectionData of this.globalSearchData) {
                const sectionResults = this.searchInSection(sectionData, searchTerm);
                if (sectionResults.length > 0) {
                    results.push({
                        section: sectionData.section,
                        title: this.getSectionTitle(sectionData.section),
                        results: sectionResults.slice(0, 3) // Máximo 3 resultados por sección
                    });
                }
            }

            this.displayGlobalSearchResults(results, query);

        } catch (error) {
            Utils.handleError(error, 'Búsqueda global');
        }
    }

    searchInSection(sectionData, searchTerm) {
        const results = [];
        
        if (sectionData.data && Array.isArray(sectionData.data)) {
            sectionData.data.forEach(item => {
                // Buscar en pregunta y respuesta
                const question = item.question ? item.question.toLowerCase() : '';
                const answer = item.answer ? item.answer.toLowerCase() : '';
                
                if (question.includes(searchTerm) || answer.includes(searchTerm)) {
                    results.push({
                        question: item.question,
                        answer: item.answer,
                        matchType: question.includes(searchTerm) ? 'pregunta' : 'respuesta'
                    });
                }
            });
        }

        return results;
    }

    getSectionTitle(sectionId) {
        const titles = {
            balances: 'Saldos',
            sales: 'Ventas',
            inventory: 'Inventario',
            customers: 'Clientes',
            reports: 'Reportes'
        };
        return titles[sectionId] || sectionId;
    }

    displayGlobalSearchResults(results, query) {
        // Eliminar resultados anteriores
        this.clearGlobalSearchResults();

        if (results.length === 0) {
            this.showNoResults(query);
            return;
        }

        // Crear contenedor de resultados
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'global-search-results';
        resultsContainer.style.cssText = `
            position: absolute;
            top: 100%;
            right: 0;
            width: 500px;
            max-height: 400px;
            overflow-y: auto;
            background: white;
            border: 1px solid #dbdbdb;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            margin-top: 5px;
        `;

        // Crear contenido de resultados
        let resultsHTML = `
            <div class="p-3" style="border-bottom: 1px solid #dbdbdb;">
                <h6 class="title is-6">Resultados para "${query}"</h6>
            </div>
        `;

        results.forEach(section => {
            resultsHTML += `
                <div class="p-3" style="border-bottom: 1px solid #f0f0f0;">
                    <h6 class="title is-6 has-text-primary">${section.title}</h6>
                    ${section.results.map(result => `
                        <div class="mb-2 p-2" style="background: #f9f9f9; border-radius: 4px; cursor: pointer;" 
                             onclick="navbar.navigateToSection('${section.section}')">
                            <div class="is-size-7 has-text-grey">${result.matchType}</div>
                            <div class="is-size-6"><strong>${result.question}</strong></div>
                            <div class="is-size-7">${result.answer.substring(0, 100)}${result.answer.length > 100 ? '...' : ''}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        });

        resultsHTML += `
            <div class="p-3">
                <button class="button is-small is-primary" onclick="navbar.clearGlobalSearchResults()">
                    Cerrar
                </button>
            </div>
        `;

        resultsContainer.innerHTML = resultsHTML;

        // Agregar al navbar
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.position = 'relative';
            navbar.appendChild(resultsContainer);
        }
    }

    showNoResults(query) {
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'global-search-results';
        resultsContainer.style.cssText = `
            position: absolute;
            top: 100%;
            right: 0;
            width: 300px;
            background: white;
            border: 1px solid #dbdbdb;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            margin-top: 5px;
        `;

        resultsContainer.innerHTML = `
            <div class="p-3">
                <div class="has-text-centered">
                    <i class="fas fa-search fa-2x has-text-grey-light mb-2"></i>
                    <p class="is-size-6">No se encontraron resultados para "${query}"</p>
                    <button class="button is-small is-primary mt-2" onclick="navbar.clearGlobalSearchResults()">
                        Cerrar
                    </button>
                </div>
            </div>
        `;

        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.style.position = 'relative';
            navbar.appendChild(resultsContainer);
        }
    }

    clearGlobalSearchResults() {
        const existingResults = document.querySelector('.global-search-results');
        if (existingResults) {
            existingResults.remove();
        }

        // Limpiar campo de búsqueda
        const globalSearch = document.getElementById('globalSearch');
        if (globalSearch) {
            globalSearch.value = '';
        }
    }

    navigateToSection(sectionId) {
        // Disparar evento para cambiar sección
        const event = new CustomEvent('sectionChanged', {
            detail: { sectionId, section: { id: sectionId } }
        });
        document.dispatchEvent(event);
        
        this.clearGlobalSearchResults();
    }

    // Método para actualizar el título de la página
    updatePageTitle(title) {
        const pageTitle = document.getElementById('pageTitle');
        if (pageTitle) {
            pageTitle.textContent = title;
        }
    }

    // Método para mostrar indicador de carga
    showLoading() {
        const globalSearch = document.getElementById('globalSearch');
        if (globalSearch) {
            globalSearch.classList.add('is-loading');
        }
    }

    hideLoading() {
        const globalSearch = document.getElementById('globalSearch');
        if (globalSearch) {
            globalSearch.classList.remove('is-loading');
        }
    }
}

// Crear instancia global
const navbar = new Navbar(); 