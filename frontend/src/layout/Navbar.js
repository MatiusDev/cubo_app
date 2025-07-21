import { Utils } from '../utils/utils.js'

// Configuración de títulos de secciones
const SECTION_TITLES = {
    balances: 'Saldos',
    sales: 'Ventas',
    inventory: 'Inventario',
    customers: 'Clientes',
    reports: 'Reportes',
    test: 'Test',
    settings: 'Configuración'
};

// Funciones de utilidad
const getSectionTitle = (sectionId) => {
    return SECTION_TITLES[sectionId] || sectionId;
};

const updatePageTitle = (title) => {
    const pageTitle = document.getElementById('pageTitle');
    if (pageTitle) {
        pageTitle.textContent = title;
    }
};

const clearGlobalSearch = () => {
    const globalSearch = document.getElementById('globalSearch');
    if (globalSearch) {
        globalSearch.value = '';
    }
};

// Funciones de búsqueda
const performGlobalSearch = async (query) => {
    if (!query || query.length < 2) {
        Utils.showNotification('Búsqueda global no disponible', 'info');
        return;
    }

    try {
        Utils.showNotification(`Búsqueda global: "${query}" - Funcionalidad no implementada`, 'info');
    } catch (error) {
        Utils.handleError(error, 'Búsqueda global');
    }
};

const navigateToSection = (sectionId) => {
    try {
        // Disparar evento para cambiar sección
        const event = new CustomEvent('sectionChanged', {
            detail: { sectionId, section: { id: sectionId, title: getSectionTitle(sectionId) } }
        });
        document.dispatchEvent(event);
        
        // Limpiar búsqueda
        clearGlobalSearch();
        
    } catch (error) {
        Utils.handleError(error, 'Navegar a sección');
    }
};

// Configuración de eventos
const bindEvents = () => {
    // Búsqueda global (simplificada)
    const globalSearch = document.getElementById('globalSearch');
    const globalSearchBtn = document.getElementById('globalSearchBtn');

    if (globalSearch) {
        // Búsqueda al presionar Enter
        globalSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query) {
                    performGlobalSearch(query);
                }
            }
        });
    }

    if (globalSearchBtn) {
        globalSearchBtn.addEventListener('click', () => {
            const query = globalSearch ? globalSearch.value.trim() : '';
            if (query) {
                performGlobalSearch(query);
            }
        });
    }
};

// Componente Navbar - Estilo Funcional
export function createNavbar(container) {
    // Renderizar el navbar en el contenedor recibido
    if (!container) return;

    container.innerHTML = `
        <div class="navbar-brand">
            <div class="navbar-item">
                <h1 class="title is-4" id="pageTitle">Dashboard</h1>
            </div>
        </div>
        <div class="navbar-end">
            <div class="navbar-item">
                <div class="field has-addons">
                    <div class="control has-icons-left">
                        <input class="input" type="text" placeholder="Búsqueda global..." id="globalSearch">
                        <span class="icon is-left">
                            <i class="fas fa-search"></i>
                        </span>
                    </div>
                    <div class="control">
                        <button class="button is-primary" id="globalSearchBtn">
                            <span class="icon">
                                <i class="fas fa-search"></i>
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Inicialización
    const init = () => {
        bindEvents();
    };

    // Inicializar inmediatamente
    init();

    // Retornar API pública del componente
    return {
        // Acciones
        performGlobalSearch,
        navigateToSection,
        updatePageTitle,
        
        // Utilidades
        getSectionTitle,
        clearGlobalSearch,
        
        // Estados de carga (para futuras implementaciones)
        showLoading: () => {
            // Implementar si es necesario
        },
        hideLoading: () => {
            // Implementar si es necesario
        },
        
        // Reinicialización
        reinit: init
    };
} 