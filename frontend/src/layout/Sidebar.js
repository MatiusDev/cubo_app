import { Utils } from '../utils/utils.js'

// Configuración de secciones
const SECTIONS = [
    {
        id: 'balances',
        title: 'Saldos',
        icon: 'fas fa-chart-pie',
        route: '/balances'
    },
    {
        id: 'sales',
        title: 'Ventas',
        icon: 'fas fa-chart-line',
        route: '/sales'
    },
    {
        id: 'inventory',
        title: 'Inventario',
        icon: 'fas fa-boxes',
        route: '/inventory'
    },
    {
        id: 'customers',
        title: 'Clientes',
        icon: 'fas fa-users',
        route: '/customers'
    },
    {
        id: 'reports',
        title: 'Reportes',
        icon: 'fas fa-file-alt',
        route: '/reports'
    },
    {
        id: 'test',
        title: 'Test',
        icon: 'fas fa-flask',
        route: '/test'
    },
    {
        id: 'settings',
        title: 'Configuración',
        icon: 'fas fa-cog',
        route: '/settings'
    }
];

// Hook personalizado para el estado del sidebar
const useSidebarState = () => {
    const state = {
        isCollapsed: Utils.getFromLocalStorage('sidebarCollapsed', false),
        currentSection: Utils.getFromLocalStorage('currentSection', 'balances'),
        sections: SECTIONS
    };

    const setState = (updates) => {
        Object.assign(state, updates);
    };

    const saveState = () => {
        Utils.saveToLocalStorage('sidebarCollapsed', state.isCollapsed);
        Utils.saveToLocalStorage('currentSection', state.currentSection);
    };

    return { state, setState, saveState };
};

// Funciones de renderizado
const renderSidebar = (sections) => {
    const sidebarNav = document.getElementById('sidebarNav');
    if (!sidebarNav) return;

    const navItems = sections.map(section => `
        <a href="#" class="nav-item" data-section="${section.id}" data-route="${section.route}">
            <i class="${section.icon} nav-icon"></i>
            <span class="nav-text">${section.title}</span>
        </a>
    `).join('');

    sidebarNav.innerHTML = navItems;
};

const updateSidebarState = (isCollapsed) => {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    if (sidebar) {
        sidebar.classList.toggle('collapsed', isCollapsed);
    }
    
    if (mainContent) {
        mainContent.classList.toggle('sidebar-collapsed', isCollapsed);
    }

    // Actualizar logo y título
    const logo = document.getElementById('sidebarLogo');
    const title = document.getElementById('sidebarTitle');
    
    if (logo) {
        logo.style.display = isCollapsed ? 'none' : 'block';
    }
    
    if (title) {
        title.style.display = isCollapsed ? 'none' : 'block';
    }
};

const updateActiveSection = (currentSection) => {
    // Remover clase activa de todos los elementos
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));

    // Agregar clase activa al elemento actual
    const activeItem = document.querySelector(`[data-section="${currentSection}"]`);
    if (activeItem) {
        activeItem.classList.add('active');
    }
};

// Funciones de utilidad
const getSectionById = (sectionId, sections) => {
    return sections.find(section => section.id === sectionId);
};

const closeMobileSidebar = () => {
    if (Utils.isMobile()) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.remove('mobile-open');
        }
    }
};

const openMobileSidebar = () => {
    if (Utils.isMobile()) {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.add('mobile-open');
        }
    }
};

// Componente Sidebar - Estilo Funcional
export function createSidebar(container) {
    const { state, setState, saveState } = useSidebarState();

    // Inyectar el HTML base del sidebar
    if (container) {
        container.className = 'sidebar';
        container.innerHTML = `
            <div class="sidebar-header">
                <div class="sidebar-brand">
                    <img src="./assets/logo_tuya.svg" alt="TUYA Fast-Data" class="sidebar-logo" id="sidebarLogo">
                    <span class="sidebar-title" id="sidebarTitle"></span>
                </div>
                <button class="sidebar-toggle" id="sidebarToggle">
                    <i class="fas fa-bars"></i>
                </button>
            </div>
            <nav class="sidebar-nav" id="sidebarNav"></nav>
        `;
    }

    // Funciones de acción
    const toggleSidebar = () => {
        const newIsCollapsed = !state.isCollapsed;
        setState({ isCollapsed: newIsCollapsed });
        updateSidebarState(newIsCollapsed);
        saveState();
    };

    const navigateToSection = (sectionId) => {
        setState({ currentSection: sectionId });
        updateActiveSection(sectionId);
        saveState();
        
        // Disparar evento personalizado para que la app principal maneje la navegación
        const event = new CustomEvent('sectionChanged', {
            detail: { sectionId, section: getSectionById(sectionId, state.sections) }
        });
        document.dispatchEvent(event);
    };

    const setActiveSection = (sectionId) => {
        if (state.sections.find(s => s.id === sectionId)) {
            setState({ currentSection: sectionId });
            updateActiveSection(sectionId);
            saveState();
        }
    };

    // Configuración de eventos
    const bindEvents = () => {
        // Toggle de la barra lateral
        const toggleBtn = document.getElementById('sidebarToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', toggleSidebar);
        }

        // Navegación por secciones
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const sectionId = item.dataset.section;
                navigateToSection(sectionId);
            });
        });

        // Manejo de eventos de teclado
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'b') {
                e.preventDefault();
                toggleSidebar();
            }
        });

        // Responsive: cerrar sidebar en móvil al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (Utils.isMobile() && state.isCollapsed === false) {
                const sidebar = document.getElementById('sidebar');
                const isClickInsideSidebar = sidebar && sidebar.contains(e.target);
                const isClickOnToggle = e.target.closest('#sidebarToggle');
                
                if (!isClickInsideSidebar && !isClickOnToggle) {
                    closeMobileSidebar();
                }
            }
        });

        // Redimensionar ventana
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                closeMobileSidebar();
            }
        });
    };

    // Inicialización
    const init = () => {
        renderSidebar(state.sections);
        bindEvents();
        updateActiveSection(state.currentSection);
        updateSidebarState(state.isCollapsed);
    };

    // Inicializar con delay para asegurar que el DOM esté listo
    setTimeout(init, 10);

    // Retornar API pública del componente
    return {
        // Estado
        getState: () => ({ ...state }),
        
        // Acciones
        toggleSidebar,
        navigateToSection,
        setActiveSection,
        
        // Utilidades
        getCurrentSection: () => getSectionById(state.currentSection, state.sections),
        getAllSections: () => [...state.sections],
        isSidebarCollapsed: () => state.isCollapsed,
        
        // Métodos móviles
        closeMobileSidebar,
        openMobileSidebar,
        
        // Reinicialización
        reinit: init
    };
} 