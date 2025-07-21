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

// Hook personalizado para el estado de la aplicación
const useAppState = () => {
    const state = {
        isInitialized: false
    };

    const setState = (updates) => {
        Object.assign(state, updates);
    };

    return { state, setState };
};

// Funciones de utilidad
const getSectionTitle = (sectionId) => {
    return SECTION_TITLES[sectionId] || sectionId;
};

const updateURL = (sectionId) => {
    try {
        // Actualizar URL sin recargar la página
        const newURL = `${window.location.pathname}#${sectionId}`;
        window.history.pushState({ sectionId }, '', newURL);
    } catch (error) {
        console.warn('No se pudo actualizar la URL:', error);
    }
};

const closeAllModals = () => {
    // Cerrar todos los modales abiertos
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => modal.remove());
};

// Funciones de manejo de eventos
const handleSectionChange = (detail) => {
    const { sectionId, section } = detail;
    
    try {
        // Actualizar título de la página
        if (window.navbar && window.navbar.updatePageTitle) {
            window.navbar.updatePageTitle(getSectionTitle(sectionId));
        }
        
        // Cargar contenido de la sección
        if (window.sectionContent && window.sectionContent.loadSection) {
            window.sectionContent.loadSection(sectionId);
        }
        
        // Actualizar URL sin recargar la página
        updateURL(sectionId);
        
    } catch (error) {
        Utils.handleError(error, `Cambio de sección a ${sectionId}`);
    }
};

const handleGlobalKeydown = (e) => {
    // Atajos de teclado globales
    switch (e.key) {
        case 'Escape':
            // Cerrar modales
            closeAllModals();
            break;
        case 'F5':
            // Prevenir recarga de página
            e.preventDefault();
            Utils.showNotification('Usa Ctrl+R para recargar', 'info');
            break;
    }
};

const handleResize = () => {
    // Manejar cambios de tamaño de ventana
    if (Utils.isMobile()) {
        // En móvil, cerrar sidebar si está abierta
        if (window.sidebar && window.sidebar.isSidebarCollapsed && !window.sidebar.isSidebarCollapsed()) {
            if (window.sidebar.closeMobileSidebar) {
                window.sidebar.closeMobileSidebar();
            }
        }
    }
};

// Configuración de eventos globales
const setupGlobalEvents = () => {
    // Manejar errores no capturados
    window.addEventListener('error', (e) => {
        Utils.handleError(e.error, 'Error global');
    });

    // Manejar promesas rechazadas
    window.addEventListener('unhandledrejection', (e) => {
        Utils.handleError(new Error(e.reason), 'Promesa rechazada');
    });

    // Manejar cambios de sección
    document.addEventListener('sectionChanged', (e) => {
        handleSectionChange(e.detail);
    });

    // Manejar eventos de teclado globales
    document.addEventListener('keydown', handleGlobalKeydown);

    // Manejar eventos de redimensionamiento
    window.addEventListener('resize', Utils.debounce(handleResize, 250));
};

// Funciones de inicialización
const initializeComponents = async () => {
    try {
        // Verificar que todos los componentes estén disponibles
        if (typeof window.sidebar === 'undefined') {
            throw new Error('Componente Sidebar no está disponible');
        }
        if (typeof window.navbar === 'undefined') {
            throw new Error('Componente Navbar no está disponible');
        }
        if (typeof window.sectionContent === 'undefined') {
            throw new Error('Componente SectionContent no está disponible');
        }

        // Los componentes ya se inicializan automáticamente en sus constructores
        // No es necesario llamar init() nuevamente

    } catch (error) {
        Utils.handleError(error, 'Inicializar componentes');
    }
};

const loadInitialData = async () => {
    try {
        // Los datos iniciales ya se cargan automáticamente en los constructores de los componentes
        // No es necesario cargar datos adicionales aquí

    } catch (error) {
        Utils.handleError(error, 'Cargar datos iniciales');
    }
};

// Funciones de gestión de datos
const exportAppData = () => {
    try {
        const data = {
            settings: {
                sidebarCollapsed: window.sidebar && window.sidebar.isSidebarCollapsed ? window.sidebar.isSidebarCollapsed() : false,
                currentSection: window.sidebar && window.sidebar.getCurrentSection ? window.sidebar.getCurrentSection() : null
            },
            exportDate: new Date().toISOString()
        };
        
        return JSON.stringify(data, null, 2);
        
    } catch (error) {
        Utils.handleError(error, 'Exportar datos');
        return null;
    }
};

const importAppData = (dataString) => {
    try {
        const data = JSON.parse(dataString);
        
        // Importar configuraciones
        if (data.settings) {
            if (data.settings.sidebarCollapsed !== undefined) {
                Utils.saveToLocalStorage('sidebarCollapsed', data.settings.sidebarCollapsed);
            }
            if (data.settings.currentSection) {
                Utils.saveToLocalStorage('currentSection', data.settings.currentSection.id);
            }
        }
        
        Utils.showNotification('Datos importados exitosamente', 'success');
        return true;
        
    } catch (error) {
        Utils.handleError(error, 'Importar datos');
        return false;
    }
};

const restart = async () => {
    try {
        // Limpiar localStorage
        localStorage.clear();
        
        // Recargar la página
        window.location.reload();
        
    } catch (error) {
        Utils.handleError(error, 'Reiniciar aplicación');
    }
};

// Componente App - Estilo Funcional
export const createApp = () => {
    const { state, setState } = useAppState();

    // Inicialización de la aplicación
    const initializeApp = async () => {
        if (state.isInitialized) return;

        try {
            // Inicializar componentes
            await initializeComponents();
            
            // Configurar eventos globales
            setupGlobalEvents();
            
            // Cargar datos iniciales
            await loadInitialData();
            
            // Marcar como inicializada
            setState({ isInitialized: true });
            
            // Mostrar notificación de bienvenida
            Utils.showNotification('¡Bienvenido a TUYA Fast-Data!', 'success', 2000);
            
            console.log('Aplicación TUYA Fast-Data inicializada correctamente');

        } catch (error) {
            Utils.handleError(error, 'Inicialización de la aplicación');
        }
    };

    // Inicialización
    const init = async () => {
        try {
            // Esperar a que el DOM esté listo
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initializeApp);
            } else {
                initializeApp();
            }
        } catch (error) {
            Utils.handleError(error, 'Inicialización de la aplicación');
        }
    };

    // Inicializar inmediatamente
    init();

    // Retornar API pública del componente
    return {
        // Estado
        getState: () => ({ ...state }),
        
        // Acciones
        restart,
        exportAppData,
        importAppData,
        
        // Utilidades
        getSectionTitle,
        updateURL,
        closeAllModals,
        
        // Información de la aplicación
        getAppInfo: () => ({
            name: 'TUYA Fast-Data',
            version: '1.0.0',
            initialized: state.isInitialized,
            currentSection: window.sidebar && window.sidebar.getCurrentSection ? window.sidebar.getCurrentSection() : null,
            sidebarCollapsed: window.sidebar && window.sidebar.isSidebarCollapsed ? window.sidebar.isSidebarCollapsed() : false
        }),
        
        // Reinicialización
        reinit: initializeApp
    };
}; 