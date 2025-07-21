import { Utils } from '../../utils/utils.js'
import {
    BalancesView,
    SalesView,
    InventoryView,
    CustomersView,
    ReportsView,
    TestView,
    SettingsView,
    DefaultView,
    VIEWS_MAP
} from './views.js'

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

// Hook personalizado para el estado del contenido
const useSectionContentState = () => {
    const state = {
        currentSection: null
    };

    const setState = (updates) => {
        Object.assign(state, updates);
    };

    return { state, setState };
};

// Mapa de vistas
const VIEWS = {
    balances: BalancesView,
    sales: SalesView,
    inventory: InventoryView,
    customers: CustomersView,
    reports: ReportsView,
    test: TestView,
    settings: SettingsView
};

// Funciones de utilidad
const getSectionTitle = (sectionId) => {
    return SECTION_TITLES[sectionId] || sectionId;
};

const updateIndicatorArea = (content) => {
    const indicatorArea = document.getElementById('indicatorArea');
    if (indicatorArea) {
        indicatorArea.innerHTML = content;
    }
};

// Funciones de renderizado
const renderSectionContent = async (sectionId) => {
    const mainContent = document.getElementById('mainContent');
    if (!mainContent) return;

    let content = '';

    // Obtener la vista correspondiente
    const view = VIEWS[sectionId] || DefaultView;
    content = view.getContent(sectionId);

    mainContent.innerHTML = content;
};

// Funciones de inicialización de secciones
const initializeSectionFeatures = (sectionId) => {
    // Obtener la vista correspondiente y inicializarla
    const view = VIEWS[sectionId] || DefaultView;
    view.initialize(sectionId);
};

// Componente SectionContent - Estilo Funcional
export const createSectionContent = () => {
    const { state, setState } = useSectionContentState();

    // Funciones de acción
    const loadSection = async (sectionId) => {
        try {
            setState({ currentSection: sectionId });
            
            // Renderizar contenido de la sección
            await renderSectionContent(sectionId);
            
            // Inicializar funcionalidades específicas
            initializeSectionFeatures(sectionId);
            
        } catch (error) {
            Utils.handleError(error, `Cargar sección ${sectionId}`);
        }
    };

    // Inicialización
    const init = () => {
        // Eventos globales si es necesario
    };

    // Inicializar inmediatamente
    init();

    // Retornar API pública del componente
    return {
        // Estado
        getState: () => ({ ...state }),
        
        // Acciones
        loadSection,
        
        // Utilidades
        getSectionTitle,
        updateIndicatorArea,
        getCurrentSection: () => state.currentSection,
        isSectionLoaded: (sectionId) => state.currentSection === sectionId,
        
        // Funciones de inicialización
        initializeSectionFeatures,
        
        // Reinicialización
        reinit: init
    };
}; 