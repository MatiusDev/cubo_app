import { Utils } from '../utils.js'

// Componente del navbar superior
export class Navbar {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        // Búsqueda global (simplificada)
        const globalSearch = document.getElementById('globalSearch');
        const globalSearchBtn = document.getElementById('globalSearchBtn');

        if (globalSearch) {
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
    }

    async performGlobalSearch(query) {
        if (!query || query.length < 2) {
            Utils.showNotification('Búsqueda global no disponible', 'info');
            return;
        }

        try {
            Utils.showNotification(`Búsqueda global: "${query}" - Funcionalidad no implementada`, 'info');
        } catch (error) {
            Utils.handleError(error, 'Búsqueda global');
        }
    }

    getSectionTitle(sectionId) {
        const titles = {
            balances: 'Saldos',
            sales: 'Ventas',
            inventory: 'Inventario',
            customers: 'Clientes',
            reports: 'Reportes',
            test: 'Test',
            settings: 'Configuración'
        };
        return titles[sectionId] || sectionId;
    }

    navigateToSection(sectionId) {
        try {
            // Disparar evento para cambiar sección
            const event = new CustomEvent('sectionChanged', {
                detail: { sectionId, section: { id: sectionId, title: this.getSectionTitle(sectionId) } }
            });
            document.dispatchEvent(event);
            
            // Limpiar búsqueda
            const globalSearch = document.getElementById('globalSearch');
            if (globalSearch) {
                globalSearch.value = '';
            }
            
        } catch (error) {
            Utils.handleError(error, 'Navegar a sección');
        }
    }

    updatePageTitle(title) {
        const pageTitle = document.getElementById('pageTitle');
        if (pageTitle) {
            pageTitle.textContent = title;
        }
    }

    showLoading() {
        // Implementar si es necesario
    }

    hideLoading() {
        // Implementar si es necesario
    }
} 